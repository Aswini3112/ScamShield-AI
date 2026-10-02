"""
Core analysis service — orchestrates the full pipeline:
  Input → Features → ML → Risk → Social Eng → Attack Chain → Report
"""
from __future__ import annotations

import logging
from typing import Any

from app.ml.predictor import get_predictor
from app.ml.feature_extractor import extract_text_features, extract_urls, get_evidence_keywords
from app.services.risk_engine import (
    score_to_risk_level,
    detect_category,
    build_indicators,
    detect_social_engineering,
    build_attack_chain,
    build_recommendations,
    generate_summary,
    generate_explanation,
)
from app.schemas.analysis import AnalysisResult, EvidenceItem

logger = logging.getLogger(__name__)


def _evidence_items(text: str, features: dict) -> list[EvidenceItem]:
    items: list[EvidenceItem] = []
    for url in extract_urls(text):
        items.append(EvidenceItem(type="url", value=url, risk_indicator=features.get("has_suspicious_url", False)))
    kw_evidence = get_evidence_keywords(text)
    for cat, kws in kw_evidence.items():
        for kw in kws[:2]:  # limit
            items.append(EvidenceItem(type="keyword", value=kw, risk_indicator=True))
    return items[:20]


def analyze_text(text: str, language: str = "en") -> AnalysisResult:
    """Full analysis pipeline for text input."""
    predictor = get_predictor()
    prediction = predictor.predict(text)

    features: dict[str, Any] = prediction["features"]
    rule_score: int = prediction["rule_score"]
    method: str = prediction.get("method", "rule_based")

    # Final risk score: prefer ML blend when available
    if method == "ml_model" and "ml_score" in prediction:
        risk_score = prediction["ml_score"]
    else:
        risk_score = rule_score

    risk_level = score_to_risk_level(risk_score)
    category = detect_category(text, features)

    indicators = build_indicators(text, features)
    social_eng = detect_social_engineering(text, features)
    attack_chain = build_attack_chain(category, features)
    recommendations = build_recommendations(category, features, risk_level)
    summary = generate_summary(category, risk_level, features)
    explanation = generate_explanation(category, risk_level, features, method)
    evidence = _evidence_items(text, features)
    urls = extract_urls(text)

    multilingual_note = None
    if language in ("ta", "tg"):
        multilingual_note = (
            "Prototype multilingual analysis — Tamil/Tanglish keyword patterns applied. "
            "Full language understanding is not yet available."
        )

    return AnalysisResult(
        risk_score=risk_score,
        risk_level=risk_level,
        category=category,
        summary=summary,
        indicators=indicators,
        social_engineering=social_eng,
        attack_chain=attack_chain,
        recommendations=recommendations,
        evidence=evidence,
        extracted_text=text[:2000],
        extracted_urls=urls[:10],
        explanation=explanation,
        input_type="text",
        multilingual_note=multilingual_note,
    )


def analyze_url_content(url: str) -> AnalysisResult:
    """Static URL analysis — no network requests made."""
    from app.ml.feature_extractor import extract_url_features

    url_feats = extract_url_features(url)

    # Build a combined text from URL tokens for text analysis
    fake_text = url.replace("/", " ").replace("?", " ").replace("=", " ").replace("-", " ")
    text_result = analyze_text(fake_text)

    # Override risk score with URL-specific signals
    url_risk = 0
    if url_feats.get("has_ip_address"):
        url_risk += 30
    if url_feats.get("has_suspicious_tld"):
        url_risk += 25
    if url_feats.get("is_url_shortener"):
        url_risk += 20
    if url_feats.get("has_suspicious_keywords"):
        url_risk += 20
    if url_feats.get("has_encoded_chars"):
        url_risk += 10
    if not url_feats.get("has_https"):
        url_risk += 10
    if url_feats.get("subdomain_count", 0) > 2:
        url_risk += 10
    if url_feats.get("url_length", 0) > 100:
        url_risk += 5
    if url_feats.get("special_char_count", 0) > 2:
        url_risk += 5

    # Blend
    final_score = min(int(url_risk * 0.6 + text_result.risk_score * 0.4), 100)
    risk_level = score_to_risk_level(final_score)

    # Build URL-specific indicators
    from app.schemas.analysis import Indicator
    url_indicators = [
        Indicator(name="HTTPS", detected=bool(url_feats.get("has_https")),
                  confidence=90 if url_feats.get("has_https") else 80, evidence=[]),
        Indicator(name="Suspicious TLD", detected=bool(url_feats.get("has_suspicious_tld")),
                  confidence=85 if url_feats.get("has_suspicious_tld") else 15,
                  evidence=[url_feats.get("tld", "")]),
        Indicator(name="IP Address Instead of Domain",
                  detected=bool(url_feats.get("has_ip_address")), confidence=90, evidence=[]),
        Indicator(name="URL Shortener", detected=bool(url_feats.get("is_url_shortener")),
                  confidence=85 if url_feats.get("is_url_shortener") else 10, evidence=[]),
        Indicator(name="Suspicious Keywords in URL",
                  detected=bool(url_feats.get("has_suspicious_keywords")),
                  confidence=75 if url_feats.get("has_suspicious_keywords") else 15, evidence=[]),
        Indicator(name="Encoded Characters",
                  detected=bool(url_feats.get("has_encoded_chars")), confidence=65, evidence=[]),
        Indicator(name="Excessive Path Depth",
                  detected=url_feats.get("path_depth", 0) > 3,
                  confidence=55 if url_feats.get("path_depth", 0) > 3 else 10, evidence=[]),
        Indicator(name="Multiple Subdomains",
                  detected=url_feats.get("subdomain_count", 0) > 1,
                  confidence=60 if url_feats.get("subdomain_count", 0) > 1 else 10, evidence=[]),
    ]

    summary = (
        f"This URL has been analyzed statically (no network request made). "
        f"Risk level: {risk_level}. "
        f"Domain: {url_feats.get('domain', 'unknown')}."
    )
    if url_feats.get("has_suspicious_tld"):
        summary += f" The TLD '{url_feats.get('tld')}' is commonly associated with fraudulent sites."
    if url_feats.get("is_url_shortener"):
        summary += " This is a shortened URL — the real destination is hidden."

    return AnalysisResult(
        risk_score=final_score,
        risk_level=risk_level,
        category="Suspicious URL" if final_score >= 40 else "URL (Low Risk)",
        summary=summary,
        indicators=url_indicators,
        social_engineering=[],
        attack_chain=build_attack_chain("Credential Phishing", {}),
        recommendations=build_recommendations("Credential Phishing", {}, risk_level),
        evidence=[EvidenceItem(type="url", value=url, risk_indicator=final_score >= 40)],
        extracted_urls=[url],
        explanation=f"Static URL analysis detected {sum(1 for i in url_indicators if i.detected)} risk signals.",
        input_type="url",
    )
