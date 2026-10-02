# 🛡 ScamShield AI

> **"Don't Just Detect the Scam. Understand the Attack."**

An AI-powered multimodal digital scam investigation, explanation, prevention and recovery platform.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Problem Statement](#2-problem-statement)
3. [Our Solution](#3-our-solution)
4. [Innovation & Differentiation](#4-innovation--differentiation)
5. [Architecture](#5-architecture)
6. [Technology Stack](#6-technology-stack)
7. [Folder Structure](#7-folder-structure)
8. [Installation](#8-installation)
9. [Environment Variables](#9-environment-variables)
10. [Dataset Creation](#10-dataset-creation)
11. [Model Training](#11-model-training)
12. [Running the Backend](#12-running-the-backend)
13. [Running the Frontend](#13-running-the-frontend)
14. [API Documentation](#14-api-documentation)
15. [Demo Instructions](#15-demo-instructions)
16. [Limitations & Disclaimers](#16-limitations--disclaimers)
17. [Future Improvements](#17-future-improvements)
18. [Security Considerations](#18-security-considerations)

---

## 1. Project Overview

ScamShield AI is a hackathon prototype that goes beyond basic scam detection. Given any suspicious message, screenshot, URL, QR code, or document, it:

- **Detects** scam indicators using ML + rule-based analysis
- **Investigates** the content for social-engineering techniques
- **Explains** exactly why the content is suspicious
- **Reconstructs** the likely attack chain step by step
- **Guides** the user on what to do next
- **Supports recovery** for users who have already interacted

**Theme:** Digital Safety & Cybersecurity  
**Status:** Hackathon Prototype

---

## 2. Problem Statement

Modern digital scams are increasingly sophisticated. Users receive suspicious SMS messages, WhatsApp messages, emails, fake job offers, banking/KYC notices, investment schemes, delivery notifications, payment requests, QR codes, URLs, and documents.

Existing security tools may detect individual suspicious items, but ordinary users still don't understand:
1. Why something is suspicious
2. Which manipulation techniques are being used
3. What the possible attack chain is
4. What they should do next
5. What to do if they have already interacted

---

## 3. Our Solution

ScamShield AI performs:

```
Input
  ↓ Input Validation
  ↓ Text / OCR / QR Extraction
  ↓ Normalisation
  ↓ Feature Extraction (35+ features)
  ↓ Rule-Based Indicators
  ↓ ML Risk Prediction (RandomForest + TF-IDF)
  ↓ Scam Classification (12 categories)
  ↓ Social Engineering Technique Detection
  ↓ Evidence Correlation
  ↓ Attack Chain Reconstruction
  ↓ Explainability Layer
  ↓ Prevention / Recovery Guidance
  ↓ Final Report
```

---

## 4. Innovation & Differentiation

There are tools that detect scams. ScamShield AI's differentiation:

| Feature | ScamShield AI | Typical detector |
|---|---|---|
| Multimodal (text + image + URL + QR + doc) | ✅ | Partial |
| Social engineering technique detection | ✅ | ❌ |
| Attack-chain reconstruction | ✅ | ❌ |
| Explainable risk assessment | ✅ | ❌ |
| Recovery guidance | ✅ | ❌ |
| India-focused scam categories | ✅ | Partial |
| Tamil / Tanglish multilingual support | ✅ (prototype) | ❌ |

---

## 5. Architecture

```
┌─────────────────────────────────────────────────────┐
│                 React Frontend                       │
│          (Vite + TypeScript + Tailwind)              │
└────────────────────┬────────────────────────────────┘
                     │ HTTP / Axios
┌────────────────────▼────────────────────────────────┐
│               FastAPI Backend                        │
│   /api/analyze/{text,url,image,qr,document}          │
│   /api/scans   /api/dashboard   /api/recovery        │
└──────┬──────────────────┬────────────────────────────┘
       │                  │
┌──────▼──────┐    ┌──────▼──────────────────────────┐
│   SQLite DB │    │       Analysis Pipeline          │
│ (SQLAlchemy)│    │  ┌─────────────────────────┐    │
└─────────────┘    │  │ Feature Extractor       │    │
                   │  │ (35+ text/URL features) │    │
                   │  └────────────┬────────────┘    │
                   │  ┌────────────▼────────────┐    │
                   │  │ ML Predictor            │    │
                   │  │ RandomForest + TF-IDF   │    │
                   │  └────────────┬────────────┘    │
                   │  ┌────────────▼────────────┐    │
                   │  │ Risk Engine             │    │
                   │  │ Category / SE / Chain   │    │
                   │  └─────────────────────────┘    │
                   └────────────────────────────────┘
```

---

## 6. Technology Stack

### Frontend
- React 18 + TypeScript + Vite
- Tailwind CSS (custom Midnight Cyber Defense theme)
- Framer Motion (animations)
- Recharts (dashboard charts)
- React Router v6
- Axios
- Lucide React icons

### Backend
- Python 3.10+
- FastAPI + Uvicorn
- Pydantic v2 (schema validation)
- SQLAlchemy 2 async + aiosqlite (SQLite → swappable to PostgreSQL)

### ML
- scikit-learn (Logistic Regression, Random Forest)
- XGBoost
- TF-IDF vectorizer
- joblib (model persistence)
- pandas, numpy

### Image / OCR (optional)
- OpenCV (QR detection)
- pytesseract (OCR — requires Tesseract binary)
- PyMuPDF (PDF extraction)

---

## 7. Folder Structure

```
ScamShield-AI/
├── frontend/               React + TypeScript frontend
│   ├── src/
│   │   ├── components/     Navbar, RiskMeter, AttackChain, RecoveryModal…
│   │   ├── pages/          Landing, Analyze, Result, Dashboard, History, Learn
│   │   ├── services/       api.ts — Axios API client
│   │   ├── types/          TypeScript types
│   │   ├── utils/          Colour helpers, formatters
│   │   └── data/           Demo examples
│   └── package.json
│
├── backend/                FastAPI backend
│   ├── app/
│   │   ├── main.py         Application entry point
│   │   ├── config.py       Settings (pydantic-settings)
│   │   ├── database.py     SQLAlchemy async setup
│   │   ├── models/         ORM models (Scan, Evidence, RecoverySession)
│   │   ├── schemas/        Pydantic v2 schemas
│   │   ├── routes/         analyze.py, scans.py, recovery.py
│   │   ├── services/       analysis_service, risk_engine, recovery_service, scan_service
│   │   ├── analyzers/      image_analyzer, document_analyzer
│   │   └── ml/             feature_extractor, predictor
│   ├── requirements.txt
│   └── .env.example
│
├── ml/                     ML pipeline (standalone)
│   ├── data/raw/           Raw synthetic CSV
│   ├── data/processed/     Train/test splits + features
│   ├── models/             Saved model artifacts
│   └── src/
│       ├── generate_dataset.py
│       ├── preprocess.py
│       ├── feature_engineering.py
│       ├── train.py
│       ├── evaluate.py
│       └── predict.py
│
├── tests/
│   ├── backend/test_api.py     API endpoint tests (17 tests)
│   └── ml/test_features.py     Feature + ML unit tests (45 tests)
│
├── docs/
│   ├── architecture.md
│   ├── api.md
│   ├── ml.md
│   ├── threat-model.md
│   └── demo-script.md
│
├── uploads/                Temporary file uploads (gitignored)
├── .gitignore
├── README.md
├── pytest.ini
└── docker-compose.yml
```

---

## 8. Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm 9+

### Quick Start

```bash
# Clone / navigate to project
cd ScamShield-AI

# ── Backend setup ──────────────────────────────────
cd backend
pip install -r requirements.txt
cp .env.example .env

# ── ML pipeline (first time) ───────────────────────
cd ../ml
python src/generate_dataset.py   # generate synthetic data
python src/preprocess.py         # clean & split
python src/feature_engineering.py # add numeric features
python src/train.py              # train & save model

# ── Start backend ──────────────────────────────────
cd ../backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# ── Frontend setup (new terminal) ─────────────────
cd ../frontend
npm install
npm run dev
```

Open **http://localhost:5173** in your browser.

### Optional: OCR support
Tesseract OCR binary is required for screenshot text extraction:
- **Windows:** Download from https://github.com/UB-Mannheim/tesseract/wiki
- **Ubuntu:** `sudo apt install tesseract-ocr`
- **macOS:** `brew install tesseract`

---

## 9. Environment Variables

Copy `backend/.env.example` to `backend/.env` and configure:

```env
APP_ENV=development
DEBUG=true
ALLOWED_ORIGINS=http://localhost:5173

# Database (SQLite for local dev)
DATABASE_URL=sqlite+aiosqlite:///./scamshield.db

# Optional AI provider (leave blank to use deterministic fallback)
GEMINI_API_KEY=
OPENAI_API_KEY=

# Limits
MAX_UPLOAD_MB=10
RATE_LIMIT_PER_MINUTE=30
```

**The application works without any AI API key.** Leaving them blank activates the deterministic ML + rule-based explanation engine.

---

## 10. Dataset Creation

```bash
cd ScamShield-AI
python ml/src/generate_dataset.py
```

Generates `ml/data/raw/scam_dataset.csv` with ~530 synthetic examples across:
- Banking/KYC Scam, UPI/Payment Scam, Job Scam, Investment Scam
- Delivery Scam, Government Impersonation, Customer Support Scam
- Social Media Scam, QR Scam, Tamil scams, Tanglish scams
- Suspicious (borderline), Legitimate (safe)

> **Disclaimer:** All training data is synthetic and uses generic placeholder organisations. It does not represent real-world scam prevalence.

---

## 11. Model Training

```bash
python ml/src/train.py      # train all models, save best
python ml/src/evaluate.py   # print evaluation metrics
python ml/src/predict.py "Your bank KYC expired. Click now."  # CLI test
```

Results on synthetic test set (not representative of real-world performance):

| Model | Accuracy | Macro-F1 |
|---|---|---|
| Logistic Regression | 94.7% | 0.896 |
| Random Forest | **96.5%** | **0.941** |
| XGBoost | 93.0% | 0.909 |

Selected model: **Random Forest**

---

## 12. Running the Backend

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

API docs available at: http://localhost:8000/api/docs

---

## 13. Running the Frontend

```bash
cd frontend
npm run dev
```

Frontend available at: http://localhost:5173  
The Vite dev server proxies `/api/*` → `http://localhost:8000`.

---

## 14. API Documentation

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Health check + model status |
| POST | `/api/analyze/text` | Analyse text message |
| POST | `/api/analyze/url` | Static URL analysis |
| POST | `/api/analyze/image` | Screenshot OCR + analysis |
| POST | `/api/analyze/qr` | QR code decode + analysis |
| POST | `/api/analyze/document` | PDF/TXT document analysis |
| GET | `/api/scans` | Scan history |
| GET | `/api/scans/{id}` | Single scan report |
| GET | `/api/dashboard/stats` | Dashboard statistics |
| POST | `/api/recovery` | Recovery guidance |

Full interactive docs: http://localhost:8000/api/docs

---

## 15. Demo Instructions

See `docs/demo-script.md` for a complete 5-minute hackathon demo script.

**Quick demo:**
1. Open http://localhost:5173
2. Click **Analyze Now**
3. Click demo buttons (Banking, Job, Delivery, etc.)
4. Click **Analyze Threat**
5. See full risk report with attack chain
6. Click **I Already Interacted** for recovery guidance

---

## 16. Limitations & Disclaimers

- **Prototype only** — not a production-grade security product
- **Synthetic training data** — accuracy metrics reflect synthetic test set only, not real-world performance
- **No real-time threat intelligence** — no live database of known scam URLs
- **OCR requires Tesseract** — screenshot analysis is unavailable without the binary
- **Multilingual support is partial** — Tamil/Tanglish keyword matching only, not full NLP
- **AI assessment is an aid, not definitive proof** — always verify through official channels
- **No guarantee of detection** — sophisticated or novel scams may not be detected

---

## 17. Future Improvements

- Real-world scam dataset from verified sources (CERT-In, cybercrime.gov.in)
- Transformer-based multilingual model (IndicBERT, MuRIL)
- Real-time URL reputation lookup (VirusTotal, Google Safe Browsing API)
- Phone number reputation database
- Persistent user accounts and notification history
- Browser extension for on-the-fly URL checking
- WhatsApp bot integration
- Full Tamil NLP pipeline
- Production deployment (PostgreSQL, Redis, Docker)

---

## 18. Security Considerations

See `docs/threat-model.md` for the full threat model.

Key security decisions:
- URLs are analyzed **statically** — no server-side fetching (prevents SSRF)
- Uploaded files are **never executed** — text-only extraction
- File size limit: 10 MB
- MIME type validation on all uploads
- API keys stored in `.env`, never exposed to frontend
- Input sanitisation via Pydantic v2 validators
- SQLAlchemy parameterised queries (no raw SQL)
