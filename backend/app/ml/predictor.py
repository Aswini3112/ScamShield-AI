"""
ML model inference layer.
Loads model + vectorizer from disk (trained by ml/src/train.py).
Falls back to rule-based scoring if models aren't available yet.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import numpy as np

from app.config import get_settings
from app.ml.feature_extractor import extract_text_features

logger = logging.getLogger(__name__)
settings = get_settings()

# Label mapping
LABEL_MAP = {0: "SAFE", 1: "SUSPICIOUS", 2: "SCAM"}

# Category keywords → category name
CATEGORY_MAP = [
    (["kyc", "has_kyc"], "Banking/KYC Scam"),
    (["has_payment", "payment_score"], "UPI/Payment Scam"),
    (["has_investment", "investment_score"], "Investment Scam"),
    (["has_job_offer", "job_score"], "Job/Recruitment Scam"),
    (["has_qr", "qr_score"], "QR Scam"),
    (["has_impersonation", "impersonation_score"], "Government Impersonation"),
    (["has_credential_request", "credential_score"], "Credential Phishing"),
    (["has_reward", "reward_score"], "Social Media Scam"),
]


class ScamPredictor:
    """
    Wraps the trained sklearn pipeline.
    Thread-safe — loads once at startup.
    """

    def __init__(self) -> None:
        self._model = None
        self._vectorizer = None
        self._feature_names: list[str] = []
        self._loaded = False
        self._load()

    def _load(self) -> None:
        model_dir = settings.model_path
        model_path = model_dir / "model.joblib"
        vec_path = model_dir / "vectorizer.joblib"
        meta_path = model_dir / "feature_names.joblib"

        # Also try path relative to this file (works when running from backend/)
        if not model_path.exists():
            alt = Path(__file__).parent.parent.parent.parent / "ml" / "models" / "model.joblib"
            if alt.exists():
                model_path = alt
                vec_path = alt.parent / "vectorizer.joblib"
                meta_path = alt.parent / "feature_names.joblib"

        if not model_path.exists():
            logger.warning(
                "ML model not found at %s. Rule-based fallback will be used. "
                "Run ml/src/train.py to generate models.",
                model_path,
            )
            return

        try:
            import joblib

            self._model = joblib.load(model_path)
            if vec_path.exists():
                self._vectorizer = joblib.load(vec_path)
            if meta_path.exists():
                self._feature_names = joblib.load(meta_path)
            self._loaded = True
            logger.info("ML model loaded from %s", model_path)
        except Exception as exc:
            logger.error("Failed to load ML model: %s", exc)

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    def predict(self, text: str) -> dict:
        """
        Returns:
          ml_label      : "SAFE" | "SUSPICIOUS" | "SCAM"
          ml_confidence : 0-100 (%)
          probabilities : list[float] for [SAFE, SUSPICIOUS, SCAM]
          rule_score    : 0-100 rule-based backup score
        """
        features = extract_text_features(text)
        rule_score = self._rule_score(features)

        if not self._loaded or self._model is None:
            # Fallback to pure rule-based
            label = self._rule_label(rule_score)
            return {
                "ml_label": label,
                "ml_confidence": rule_score,
                "probabilities": self._fake_proba(rule_score),
                "rule_score": rule_score,
                "features": features,
                "method": "rule_based",
            }

        try:
            feature_vector = self._build_vector(text, features)
            proba = self._model.predict_proba([feature_vector])[0]
            pred_class = int(np.argmax(proba))
            confidence = int(proba[pred_class] * 100)

            # Blend: weight rule_score more heavily when it's very high
            # so that clear multi-signal scams aren't dampened by ML
            ml_component = int(proba[2] * 100 * 0.55 + proba[1] * 100 * 0.25)
            rule_weight = 0.2 if rule_score < 60 else 0.4  # more rule weight for high rule scores
            ml_score = int(ml_component * (1 - rule_weight) + rule_score * rule_weight)
            ml_score = min(100, ml_score)

            return {
                "ml_label": LABEL_MAP[pred_class],
                "ml_confidence": confidence,
                "probabilities": proba.tolist(),
                "rule_score": rule_score,
                "features": features,
                "method": "ml_model",
                "ml_score": ml_score,
            }
        except Exception as exc:
            logger.warning("ML predict error: %s — falling back to rules", exc)
            label = self._rule_label(rule_score)
            return {
                "ml_label": label,
                "ml_confidence": rule_score,
                "probabilities": self._fake_proba(rule_score),
                "rule_score": rule_score,
                "features": features,
                "method": "rule_based_fallback",
            }

    def _build_vector(self, text: str, features: dict) -> list[float]:
        """Combine TF-IDF and numeric features into one vector."""
        numeric = [float(features.get(k, 0)) for k in sorted(features.keys())]
        if self._vectorizer is not None:
            tfidf = self._vectorizer.transform([text]).toarray()[0]
            return list(tfidf) + numeric
        return numeric

    @staticmethod
    def _rule_score(features: dict) -> int:
        """Deterministic rule-based risk score 0-100."""
        score = 0

        # Urgency + fear drive the score significantly
        score += min(features.get("urgency_score", 0) * 10, 25)
        score += min(features.get("fear_score", 0) * 8, 20)
        score += min(features.get("threat_score", 0) * 8, 16)

        # Credential / payment requests
        score += features.get("has_credential_request", 0) * 15
        score += features.get("has_payment", 0) * 8
        score += features.get("otp_score", 0) * 12
        score += features.get("password_score", 0) * 12

        # Specific scam signals
        score += features.get("has_kyc", 0) * 10
        score += features.get("has_suspicious_url", 0) * 15
        score += features.get("has_shortener", 0) * 8
        score += features.get("has_qr", 0) * 5

        # Low-signal extras
        score += features.get("has_impersonation", 0) * 6
        score += features.get("has_job_offer", 0) * 5
        score += features.get("has_investment", 0) * 5
        score += min(features.get("url_count", 0) * 5, 10)
        score += min(features.get("capitalisation_ratio", 0) * 20, 8)
        score += min(features.get("exclamation_count", 0) * 2, 6)
        score += features.get("cta_score", 0) * 3

        return min(int(score), 100)

    @staticmethod
    def _rule_label(score: int) -> str:
        if score >= 60:
            return "SCAM"
        if score >= 30:
            return "SUSPICIOUS"
        return "SAFE"

    @staticmethod
    def _fake_proba(rule_score: int) -> list[float]:
        scam_p = rule_score / 100
        safe_p = 1 - scam_p
        return [safe_p * 0.7, safe_p * 0.3, scam_p]


# Module-level singleton — loaded once at import time
_predictor: Optional[ScamPredictor] = None


def get_predictor() -> ScamPredictor:
    global _predictor
    if _predictor is None:
        _predictor = ScamPredictor()
    return _predictor
