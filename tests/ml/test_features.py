"""
ML feature extraction and risk engine tests.
Run: cd ScamShield-AI && python -m pytest tests/ml/ -v
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "backend"))

from app.ml.feature_extractor import (
    extract_text_features,
    extract_url_features,
    extract_urls,
    get_evidence_keywords,
)
from app.ml.predictor import ScamPredictor, get_predictor
from app.services.risk_engine import (
    score_to_risk_level,
    detect_category,
    build_indicators,
    detect_social_engineering,
    build_attack_chain,
    generate_summary,
)


# ── Feature extractor ─────────────────────────────────────────────────────────

class TestTextFeatures:
    SCAM_TEXT = "URGENT: Your bank account will be BLOCKED today. Complete KYC immediately: http://fake-kyc.xyz"
    SAFE_TEXT = "Your OTP is 847291. Valid 5 minutes. Do NOT share with anyone."

    def test_urgency_detected(self):
        f = extract_text_features(self.SCAM_TEXT)
        assert f["has_urgency"] == 1
        assert f["urgency_score"] >= 1

    def test_fear_detected(self):
        f = extract_text_features(self.SCAM_TEXT)
        assert f["has_fear"] == 1

    def test_kyc_detected(self):
        f = extract_text_features(self.SCAM_TEXT)
        assert f["has_kyc"] == 1

    def test_url_count(self):
        f = extract_text_features(self.SCAM_TEXT)
        assert f["url_count"] == 1

    def test_safe_message_low_scores(self):
        f = extract_text_features(self.SAFE_TEXT)
        # Safe messages should have low urgency/fear scores
        assert f["urgency_score"] <= 1
        assert f["fear_score"] == 0

    def test_otp_detected(self):
        f = extract_text_features(self.SAFE_TEXT)
        assert f["otp_score"] >= 1

    def test_features_are_numeric(self):
        f = extract_text_features(self.SCAM_TEXT)
        for k, v in f.items():
            assert isinstance(v, (int, float)), f"Feature {k} is not numeric: {v}"

    def test_capitalisation_ratio(self):
        f = extract_text_features("ALL CAPS MESSAGE URGENT URGENT")
        assert f["capitalisation_ratio"] > 0.5

    def test_investment_detected(self):
        f = extract_text_features("Earn 40% guaranteed returns. Invest now in our crypto scheme.")
        assert f["has_investment"] == 1

    def test_job_detected(self):
        f = extract_text_features("Work from home job. Earn Rs.50000/month. No experience needed.")
        assert f["has_job_offer"] == 1


class TestUrlFeatures:
    def test_suspicious_tld(self):
        f = extract_url_features("http://fake-bank.xyz/login")
        assert f["has_suspicious_tld"] is True

    def test_https_detection(self):
        f = extract_url_features("https://www.example.com")
        assert f["has_https"] is True
        f2 = extract_url_features("http://example.com")
        assert f2["has_https"] is False

    def test_ip_address(self):
        f = extract_url_features("http://192.168.1.100/verify")
        assert f["has_ip_address"] is True

    def test_url_shortener(self):
        f = extract_url_features("https://bit.ly/abc123")
        assert f["is_url_shortener"] is True

    def test_subdomain_count(self):
        f = extract_url_features("https://sub1.sub2.example.com/path")
        assert f["subdomain_count"] >= 1

    def test_suspicious_keywords(self):
        f = extract_url_features("https://example.com/verify-kyc-login")
        assert f["has_suspicious_keywords"] is True

    def test_domain_extracted(self):
        f = extract_url_features("https://www.testbank.com/netbanking")
        assert "testbank.com" in f["domain"]


class TestUrlExtraction:
    def test_extracts_http(self):
        urls = extract_urls("Visit http://example.com for more info.")
        assert len(urls) == 1

    def test_extracts_https(self):
        urls = extract_urls("Go to https://secure.example.com/verify?id=1")
        assert len(urls) == 1

    def test_extracts_multiple(self):
        urls = extract_urls("Visit http://a.com and https://b.com now.")
        assert len(urls) == 2

    def test_no_urls(self):
        urls = extract_urls("No links in this message.")
        assert len(urls) == 0


class TestEvidenceKeywords:
    def test_urgency_keywords(self):
        kw = get_evidence_keywords("Please act immediately today or face consequences.")
        assert len(kw["urgency"]) > 0

    def test_kyc_keywords(self):
        kw = get_evidence_keywords("Complete your KYC update now.")
        assert len(kw["kyc"]) > 0


# ── Risk engine ───────────────────────────────────────────────────────────────

class TestRiskLevel:
    def test_low(self):
        assert score_to_risk_level(20) == "LOW"
        assert score_to_risk_level(0) == "LOW"
        assert score_to_risk_level(29) == "LOW"

    def test_medium(self):
        assert score_to_risk_level(30) == "MEDIUM"
        assert score_to_risk_level(59) == "MEDIUM"

    def test_high(self):
        assert score_to_risk_level(60) == "HIGH"
        assert score_to_risk_level(79) == "HIGH"

    def test_critical(self):
        assert score_to_risk_level(80) == "CRITICAL"
        assert score_to_risk_level(100) == "CRITICAL"


class TestCategoryDetection:
    def test_kyc_category(self):
        text = "Your bank account KYC is incomplete. Update now."
        f = extract_text_features(text)
        cat = detect_category(text, f)
        assert cat == "Banking/KYC Scam"

    def test_job_category(self):
        text = "Work from home job. Earn Rs.50000/month. No experience."
        f = extract_text_features(text)
        cat = detect_category(text, f)
        assert cat == "Job/Recruitment Scam"

    def test_investment_category(self):
        text = "Earn 40% guaranteed monthly returns. Invest now."
        f = extract_text_features(text)
        cat = detect_category(text, f)
        assert cat == "Investment Scam"


class TestSocialEngineering:
    def test_urgency_detected(self):
        text = "URGENT: Act immediately or account blocked today."
        f = extract_text_features(text)
        techs = detect_social_engineering(text, f)
        names = [t.technique for t in techs]
        assert "Urgency" in names

    def test_fear_detected(self):
        text = "Your account will be suspended and blocked if you don't act."
        f = extract_text_features(text)
        techs = detect_social_engineering(text, f)
        names = [t.technique for t in techs]
        assert "Fear" in names

    def test_kyc_pretext(self):
        text = "Complete KYC now or face account suspension."
        f = extract_text_features(text)
        techs = detect_social_engineering(text, f)
        names = [t.technique for t in techs]
        assert "KYC Pretext" in names

    def test_confidence_range(self):
        text = "Urgent KYC update immediately or blocked."
        f = extract_text_features(text)
        techs = detect_social_engineering(text, f)
        for t in techs:
            assert 0 <= t.confidence <= 100


class TestIndicatorBuilding:
    def test_indicators_have_required_fields(self):
        text = "Urgent! Your bank account blocked. KYC: http://fake.xyz"
        f = extract_text_features(text)
        indicators = build_indicators(text, f)
        assert len(indicators) > 0
        for ind in indicators:
            assert hasattr(ind, "name")
            assert hasattr(ind, "detected")
            assert hasattr(ind, "confidence")
            assert 0 <= ind.confidence <= 100

    def test_some_detected_in_scam(self):
        text = "Urgent! Your bank account blocked. KYC: http://fake.xyz"
        f = extract_text_features(text)
        indicators = build_indicators(text, f)
        detected = [i for i in indicators if i.detected]
        assert len(detected) >= 2


class TestAttackChain:
    def test_chain_for_kyc(self):
        chain = build_attack_chain("Banking/KYC Scam", {})
        assert len(chain) >= 5
        assert chain[0].step == 1

    def test_chain_for_job(self):
        chain = build_attack_chain("Job/Recruitment Scam", {})
        assert len(chain) >= 4

    def test_chain_for_unknown(self):
        chain = build_attack_chain("Unknown Category", {})
        assert len(chain) >= 2

    def test_steps_are_numbered(self):
        chain = build_attack_chain("UPI/Payment Scam", {})
        for i, step in enumerate(chain):
            assert step.step == i + 1


# ── Predictor ─────────────────────────────────────────────────────────────────

class TestPredictor:
    def setup_method(self):
        self.predictor = ScamPredictor()

    def test_predict_returns_dict(self):
        result = self.predictor.predict("Test message")
        assert isinstance(result, dict)
        assert "ml_label" in result
        assert "rule_score" in result
        assert "features" in result

    def test_scam_gets_high_score(self):
        text = "URGENT: Your bank account BLOCKED today. Complete KYC immediately: http://fake-kyc.xyz/verify. Share your OTP now."
        result = self.predictor.predict(text)
        assert result["rule_score"] >= 40

    def test_safe_gets_low_score(self):
        text = "Your appointment is confirmed for tomorrow at 10 AM. No action needed."
        result = self.predictor.predict(text)
        assert result["rule_score"] <= 20

    def test_ml_label_valid(self):
        result = self.predictor.predict("Test message")
        assert result["ml_label"] in ("SAFE", "SUSPICIOUS", "SCAM")

    def test_predict_handles_empty(self):
        result = self.predictor.predict("")
        assert result is not None
        assert "ml_label" in result
