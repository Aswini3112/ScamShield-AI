#!/usr/bin/env bash
# Render build script — runs from repo root
# Installs backend deps, then trains the ML model.
set -e

echo "=== ScamShield AI — Render Build ==="

# Install Python deps
echo "Installing backend dependencies..."
pip install -r backend/requirements.txt

# Train ML model (synthetic data — fast, ~10 seconds)
echo "Generating dataset..."
python ml/src/generate_dataset.py

echo "Preprocessing..."
python ml/src/preprocess.py

echo "Feature engineering..."
python ml/src/feature_engineering.py

echo "Training model..."
python ml/src/train.py

echo "=== Build complete ==="
