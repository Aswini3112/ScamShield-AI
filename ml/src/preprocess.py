"""
Preprocessing pipeline — loads raw CSV, cleans text, splits data.
Output: ml/data/processed/train.csv and test.csv
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

RAW_FILE = Path(__file__).parent.parent / "data" / "raw" / "scam_dataset.csv"
PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def clean_text(text: str) -> str:
    """Normalise text: lowercase, collapse whitespace, strip URLs for TF-IDF."""
    if not isinstance(text, str):
        return ""
    text = text.lower().strip()
    # Replace URLs with a token (we handle URLs separately in feature extraction)
    text = re.sub(r"https?://\S+|www\.\S+", " URLTOKEN ", text)
    # Replace phone numbers with token
    text = re.sub(r"\b(\+91[\s-]?)?[6-9]\d{9}\b", " PHONETOKEN ", text)
    # Replace amounts like Rs.500 with token
    text = re.sub(r"(rs\.?|inr|₹)\s*[\d,]+", " AMOUNTTOKEN ", text)
    # Remove excess whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.dropna(subset=["text", "label"])
    df["text"] = df["text"].astype(str)
    df["label"] = df["label"].astype(int)
    df["cleaned_text"] = df["text"].apply(clean_text)
    # Drop duplicates on cleaned text
    df = df.drop_duplicates(subset=["cleaned_text"])
    df = df.reset_index(drop=True)
    return df


def main() -> tuple[pd.DataFrame, pd.DataFrame]:
    if not RAW_FILE.exists():
        print(f"Raw dataset not found at {RAW_FILE}. Run generate_dataset.py first.")
        sys.exit(1)

    df = pd.read_csv(RAW_FILE)
    print(f"Loaded {len(df)} rows from {RAW_FILE}")

    df = preprocess(df)
    print(f"After preprocessing: {len(df)} unique rows")
    print(f"Label distribution:\n{df['label'].value_counts().sort_index()}")

    train_df, test_df = train_test_split(
        df,
        test_size=0.2,
        stratify=df["label"],
        random_state=42,
    )
    print(f"Train: {len(train_df)}  Test: {len(test_df)}")

    train_df.to_csv(PROCESSED_DIR / "train.csv", index=False)
    test_df.to_csv(PROCESSED_DIR / "test.csv", index=False)
    print(f"Saved to {PROCESSED_DIR}")
    return train_df, test_df


if __name__ == "__main__":
    main()
