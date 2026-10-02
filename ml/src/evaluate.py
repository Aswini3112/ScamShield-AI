"""
ScamShield AI — Model Evaluation
==================================
Loads saved model artifacts and prints full evaluation metrics.

Usage:
    python ml/src/evaluate.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
    accuracy_score,
)
from scipy.sparse import hstack, csr_matrix

ML_DIR = Path(__file__).parent.parent
MODELS_DIR = ML_DIR / "models"
PROCESSED_DIR = ML_DIR / "data" / "processed"

sys.path.insert(0, str(ML_DIR.parent / "backend"))
from app.ml.feature_extractor import extract_text_features

LABEL_NAMES = ["SAFE", "SUSPICIOUS", "SCAM"]

NUMERIC_COLS = [
    "text_length", "word_count", "avg_word_length", "capitalisation_ratio",
    "exclamation_count", "question_count", "url_count", "phone_count",
    "currency_mention_count", "urgency_score", "fear_score", "threat_score",
    "payment_score", "otp_score", "credential_score", "reward_score",
    "impersonation_score", "job_score", "investment_score", "kyc_score",
    "qr_score", "cta_score", "password_score",
    "has_urgency", "has_fear", "has_payment", "has_credential_request",
    "has_impersonation", "has_reward", "has_suspicious_url",
    "has_job_offer", "has_investment", "has_kyc", "has_qr", "has_shortener",
]


def load_model():
    model_path = MODELS_DIR / "model.joblib"
    vec_path = MODELS_DIR / "vectorizer.joblib"
    if not model_path.exists():
        print("Model not found. Run train.py first.")
        sys.exit(1)
    model = joblib.load(model_path)
    vectorizer = joblib.load(vec_path)
    return model, vectorizer


def load_test_data():
    path = PROCESSED_DIR / "test_features.csv"
    if not path.exists():
        path = PROCESSED_DIR / "test.csv"
    if not path.exists():
        print("Test data not found. Run generate_dataset.py and preprocess.py first.")
        sys.exit(1)
    df = pd.read_csv(path)
    if "cleaned_text" not in df.columns:
        sys.path.insert(0, str(ML_DIR.parent / "backend"))
        feat_rows = [extract_text_features(t) for t in df["text"]]
        df = pd.concat([df.reset_index(drop=True), pd.DataFrame(feat_rows)], axis=1)
    return df


def main():
    print("=" * 60)
    print("ScamShield AI — Model Evaluation")
    print("=" * 60)

    model, vectorizer = load_model()
    test_df = load_test_data()
    y_true = test_df["label"].astype(int).values

    text_col = test_df.get("cleaned_text", test_df.get("text", pd.Series([""] * len(test_df))))
    tfidf = vectorizer.transform(text_col.astype(str))
    numeric = csr_matrix(test_df.reindex(columns=NUMERIC_COLS, fill_value=0).values.astype(float))
    X = hstack([tfidf, numeric])

    y_pred = model.predict(X)

    acc = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average="macro")
    cm = confusion_matrix(y_true, y_pred)
    report = classification_report(y_true, y_pred, target_names=LABEL_NAMES)

    print(f"\nAccuracy  : {acc:.4f}")
    print(f"Macro-F1  : {macro_f1:.4f}")
    print(f"\nPer-class report:\n{report}")
    print("Confusion Matrix (SAFE / SUSPICIOUS / SCAM):")
    print(cm)

    # Load meta
    meta_path = MODELS_DIR / "model_meta.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text())
        print(f"\nModel type : {meta.get('best_model', 'unknown')}")
        print(f"\nNote: {meta.get('data_note', '')}")


if __name__ == "__main__":
    main()
