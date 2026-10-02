"""
Feature engineering — adds numeric hand-crafted features to the dataset.
These complement TF-IDF and improve the ML model for scam detection.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import numpy as np

# Add backend to path so we can reuse feature extractor
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "backend"))
from app.ml.feature_extractor import extract_text_features

PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract numeric features and add as columns."""
    print("Extracting features (this may take a moment)...")
    feature_rows = [extract_text_features(text) for text in df["text"]]
    features_df = pd.DataFrame(feature_rows)
    return pd.concat([df.reset_index(drop=True), features_df], axis=1)


def main():
    for split in ("train", "test"):
        path = PROCESSED_DIR / f"{split}.csv"
        if not path.exists():
            print(f"{path} not found — run preprocess.py first.")
            continue

        df = pd.read_csv(path)
        df = add_features(df)
        out = PROCESSED_DIR / f"{split}_features.csv"
        df.to_csv(out, index=False)
        print(f"Saved {split} features to {out} ({len(df)} rows, {len(df.columns)} cols)")


if __name__ == "__main__":
    main()
