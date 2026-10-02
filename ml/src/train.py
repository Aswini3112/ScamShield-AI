"""
ScamShield AI — Model Training
================================
Trains Logistic Regression, Random Forest, and XGBoost (if available)
on TF-IDF + numeric features. Selects best model by macro F1.

Usage:
    cd ScamShield-AI
    python ml/src/train.py

Outputs (ml/models/):
    model.joblib          — best trained model
    vectorizer.joblib     — TF-IDF vectorizer
    feature_names.joblib  — feature name list
    training_report.txt   — metrics summary
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    classification_report, f1_score, accuracy_score,
    confusion_matrix
)
from scipy.sparse import hstack, csr_matrix

# Paths
ML_DIR = Path(__file__).parent.parent
PROCESSED_DIR = ML_DIR / "data" / "processed"
MODELS_DIR = ML_DIR / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Add backend to path for feature extractor
sys.path.insert(0, str(ML_DIR.parent / "backend"))
from app.ml.feature_extractor import extract_text_features

LABEL_NAMES = ["SAFE", "SUSPICIOUS", "SCAM"]

# ── Numeric feature columns (must match feature_extractor output) ─────────────
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


def load_data(split: str) -> tuple[pd.DataFrame, np.ndarray]:
    path = PROCESSED_DIR / f"{split}_features.csv"
    if not path.exists():
        # Fall back to non-feature CSV and compute on the fly
        path = PROCESSED_DIR / f"{split}.csv"
        if not path.exists():
            raise FileNotFoundError(f"Data not found: {path}. Run generate_dataset.py and preprocess.py first.")
        df = pd.read_csv(path)
        print(f"Computing features for {split} split...")
        feat_rows = [extract_text_features(t) for t in df["text"]]
        feat_df = pd.DataFrame(feat_rows)
        df = pd.concat([df.reset_index(drop=True), feat_df], axis=1)
    else:
        df = pd.read_csv(path)

    labels = df["label"].astype(int).values
    return df, labels


def build_feature_matrix(df: pd.DataFrame, vectorizer: TfidfVectorizer, fit: bool = False):
    """Combine TF-IDF on cleaned_text with hand-crafted numeric features."""
    text_col = df.get("cleaned_text", df.get("text", pd.Series([""] * len(df))))

    if fit:
        tfidf_matrix = vectorizer.fit_transform(text_col.astype(str))
    else:
        tfidf_matrix = vectorizer.transform(text_col.astype(str))

    # Numeric features — fill missing with 0
    numeric_data = df.reindex(columns=NUMERIC_COLS, fill_value=0).values.astype(float)
    numeric_sparse = csr_matrix(numeric_data)

    return hstack([tfidf_matrix, numeric_sparse])


def train_and_evaluate():
    print("=" * 60)
    print("ScamShield AI — Model Training")
    print("=" * 60)

    # ── Load data ────────────────────────────────────────────────
    train_df, y_train = load_data("train")
    test_df, y_test = load_data("test")
    print(f"Train: {len(train_df)}  Test: {len(test_df)}")
    print(f"Label distribution (train): {dict(zip(*np.unique(y_train, return_counts=True)))}")

    # ── TF-IDF vectorizer ────────────────────────────────────────
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=5000,
        min_df=2,
        sublinear_tf=True,
        strip_accents="unicode",
    )

    X_train = build_feature_matrix(train_df, vectorizer, fit=True)
    X_test = build_feature_matrix(test_df, vectorizer, fit=False)
    print(f"Feature matrix: {X_train.shape}")

    # ── Models to compare ────────────────────────────────────────
    models: dict[str, object] = {
        "LogisticRegression": LogisticRegression(
            C=5.0,
            max_iter=1000,
            class_weight="balanced",
            multi_class="multinomial",
            solver="lbfgs",
            random_state=42,
        ),
        "RandomForest": RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        ),
    }

    # XGBoost if available
    try:
        import xgboost as xgb
        models["XGBoost"] = xgb.XGBClassifier(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=6,
            use_label_encoder=False,
            eval_metric="mlogloss",
            random_state=42,
        )
        print("XGBoost available — including in comparison.")
    except ImportError:
        print("XGBoost not available — skipping.")

    results: dict[str, dict] = {}
    report_lines: list[str] = []

    for name, model in models.items():
        print(f"\nTraining {name}...")
        t0 = time.time()
        model.fit(X_train, y_train)
        elapsed = time.time() - t0

        y_pred = model.predict(X_test)
        f1 = f1_score(y_test, y_pred, average="macro")
        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, target_names=LABEL_NAMES)
        cm = confusion_matrix(y_test, y_pred).tolist()

        print(f"  Accuracy: {acc:.4f}  Macro-F1: {f1:.4f}  ({elapsed:.1f}s)")
        print(report)

        results[name] = {"f1": f1, "accuracy": acc, "model": model, "cm": cm}
        report_lines.append(f"{'=' * 50}")
        report_lines.append(f"Model: {name}")
        report_lines.append(f"Accuracy: {acc:.4f}   Macro-F1: {f1:.4f}   Time: {elapsed:.1f}s")
        report_lines.append(report)
        report_lines.append(f"Confusion Matrix: {cm}")

    # ── Select best model ────────────────────────────────────────
    best_name = max(results, key=lambda k: results[k]["f1"])
    best_model = results[best_name]["model"]
    best_f1 = results[best_name]["f1"]
    best_acc = results[best_name]["accuracy"]
    print(f"\nBest model: {best_name}  (Macro-F1={best_f1:.4f}, Accuracy={best_acc:.4f})")

    # ── Save artifacts ───────────────────────────────────────────
    joblib.dump(best_model, MODELS_DIR / "model.joblib")
    joblib.dump(vectorizer, MODELS_DIR / "vectorizer.joblib")
    joblib.dump(NUMERIC_COLS, MODELS_DIR / "feature_names.joblib")

    meta = {
        "best_model": best_name,
        "macro_f1": round(best_f1, 4),
        "accuracy": round(best_acc, 4),
        "label_names": LABEL_NAMES,
        "data_note": (
            "Trained on SYNTHETIC data generated for demo purposes. "
            "Metrics reflect performance on synthetic test set only — "
            "NOT real-world scam detection effectiveness."
        ),
    }
    with open(MODELS_DIR / "model_meta.json", "w") as f:
        json.dump(meta, f, indent=2)

    report_lines.insert(0, f"BEST MODEL: {best_name}  Macro-F1={best_f1:.4f}\n")
    report_lines.append("\n" + meta["data_note"])
    with open(MODELS_DIR / "training_report.txt", "w") as f:
        f.write("\n".join(report_lines))

    print(f"\nArtifacts saved to: {MODELS_DIR}")
    print(f"  model.joblib       ({best_name})")
    print(f"  vectorizer.joblib  (TF-IDF)")
    print(f"  feature_names.joblib")
    print(f"  model_meta.json")
    print(f"  training_report.txt")
    print("\nDISCLAIMER: Metrics are on synthetic data — see training_report.txt")


if __name__ == "__main__":
    train_and_evaluate()
