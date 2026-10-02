"""
ScamShield AI — CLI Prediction Tool
======================================
Test the trained model with a sample message from the command line.

Usage:
    python ml/src/predict.py "Your bank account will be blocked today."
    python ml/src/predict.py  (interactive mode)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ML_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ML_DIR.parent / "backend"))

from app.ml.predictor import get_predictor
from app.services.risk_engine import (
    score_to_risk_level, detect_category,
    detect_social_engineering, build_indicators,
)


def predict_message(text: str) -> None:
    predictor = get_predictor()
    result = predictor.predict(text)

    features = result["features"]
    risk_score = result.get("ml_score") or result["rule_score"]
    risk_level = score_to_risk_level(risk_score)
    category = detect_category(text, features)
    techs = detect_social_engineering(text, features)
    indicators = build_indicators(text, features)

    print("\n" + "=" * 55)
    print(f"ScamShield AI Analysis")
    print("=" * 55)
    print(f"Text     : {text[:80]}{'...' if len(text) > 80 else ''}")
    print(f"Method   : {result.get('method', 'unknown')}")
    print(f"ML Label : {result['ml_label']}")
    print(f"Score    : {risk_score}/100")
    print(f"Risk     : {risk_level}")
    print(f"Category : {category}")

    detected = [i.name for i in indicators if i.detected]
    if detected:
        print(f"Indicators: {', '.join(detected)}")

    if techs:
        print(f"Social Eng: {', '.join(t.technique for t in techs)}")

    print("=" * 55 + "\n")


def main():
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        predict_message(text)
    else:
        print("ScamShield AI — Interactive Prediction")
        print("Type a message and press Enter. Ctrl+C to exit.\n")
        while True:
            try:
                text = input("Message: ").strip()
                if text:
                    predict_message(text)
            except (KeyboardInterrupt, EOFError):
                print("\nExiting.")
                break


if __name__ == "__main__":
    main()
