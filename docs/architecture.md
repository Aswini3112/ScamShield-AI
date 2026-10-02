# ScamShield AI — System Architecture

## Overview

ScamShield AI is structured as a three-tier application:

```
┌──────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                          │
│  Landing → Analyze → Result → Dashboard → History → Learn   │
│  Framer Motion · Recharts · Tailwind · Axios                 │
└──────────────────────┬───────────────────────────────────────┘
                       │  HTTP/JSON  (proxy: /api → :8000)
┌──────────────────────▼───────────────────────────────────────┐
│                  FASTAPI BACKEND                             │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ /analyze/*   │  │  /scans/*    │  │ /dashboard/stats │  │
│  │ /recovery    │  │              │  │                  │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘  │
│         │                 │                   │             │
│  ┌──────▼───────────────────────────────────────────────┐  │
│  │                 Analysis Pipeline                     │  │
│  │                                                       │  │
│  │  Input → Validation → Extraction → Normalisation     │  │
│  │       → Feature Engineering → ML Prediction          │  │
│  │       → Risk Scoring → Category Detection            │  │
│  │       → Social Engineering → Attack Chain            │  │
│  │       → Explainability → Recommendations             │  │
│  └──────────────────────────────────┬────────────────────┘  │
│                                     │                        │
│  ┌──────────────────┐    ┌──────────▼──────────────────┐   │
│  │  SQLite / PG DB  │    │  ML Model (RandomForest)     │   │
│  │  (SQLAlchemy)    │    │  TF-IDF + Numeric Features   │   │
│  └──────────────────┘    └─────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

---

## Component Details

### Frontend

| File/Directory | Responsibility |
|---|---|
| `src/pages/LandingPage.tsx` | Hero, pipeline viz, capability cards, CTA |
| `src/pages/AnalyzePage.tsx` | Tabbed input (text/image/URL/QR/doc), demo buttons |
| `src/pages/ResultPage.tsx` | Full threat report: risk meter, indicators, SE, chain |
| `src/pages/DashboardPage.tsx` | Stats cards, Recharts bar/pie charts |
| `src/pages/HistoryPage.tsx` | Searchable/filterable scan list |
| `src/pages/LearnPage.tsx` | Expandable cybersecurity awareness articles |
| `src/components/RiskMeter.tsx` | Animated SVG arc meter |
| `src/components/AttackChain.tsx` | Animated step-by-step attack chain |
| `src/components/RecoveryModal.tsx` | Recovery guided questionnaire modal |
| `src/components/AnalysisProgress.tsx` | 5-step analysis progress animation |
| `src/services/api.ts` | Axios API client — all backend calls |

### Backend

| Module | Responsibility |
|---|---|
| `app/main.py` | FastAPI app, CORS, lifespan, routes |
| `app/config.py` | Pydantic-settings configuration |
| `app/database.py` | SQLAlchemy async engine + session |
| `app/models/scan.py` | ORM: Scan, Evidence, RecoverySession |
| `app/schemas/analysis.py` | All Pydantic v2 request/response models |
| `app/routes/analyze.py` | POST /analyze/{text,url,image,qr,document} |
| `app/routes/scans.py` | GET /scans, /scans/{id}, /dashboard/stats |
| `app/routes/recovery.py` | POST /recovery |
| `app/services/analysis_service.py` | Orchestrates full analysis pipeline |
| `app/services/risk_engine.py` | Risk scoring, categories, SE detection, attack chains |
| `app/services/recovery_service.py` | Recovery guidance by interaction type |
| `app/services/scan_service.py` | DB persistence and query layer |
| `app/ml/feature_extractor.py` | 35+ text/URL feature extraction functions |
| `app/ml/predictor.py` | ML model loader + inference + rule fallback |
| `app/analyzers/image_analyzer.py` | OpenCV OCR + QR detection |
| `app/analyzers/document_analyzer.py` | PDF/text extraction |

---

## Analysis Pipeline (detailed)

```
1. INPUT VALIDATION
   - File size check (<10 MB)
   - MIME type validation
   - Text length validation (Pydantic)

2. CONTENT EXTRACTION
   Text    → raw text (strip, normalise)
   Image   → OpenCV + pytesseract OCR
   QR      → OpenCV QRCodeDetector
   URL     → urlparse (static, no fetch)
   Document→ PyMuPDF (PDF) / text decode

3. FEATURE ENGINEERING (feature_extractor.py)
   - Text features: urgency_score, fear_score, kyc_score, job_score…
   - URL features: suspicious_tld, is_shortener, has_ip…
   - Structural: url_count, phone_count, cap_ratio, exclamation…
   Total: 35+ numeric/boolean features

4. ML PREDICTION (predictor.py)
   - TF-IDF on cleaned text (5000 features, 1-2 ngrams)
   - Concatenate TF-IDF + numeric features
   - RandomForest.predict_proba() → [SAFE, SUSPICIOUS, SCAM]
   - Blend ML score with rule score for robustness
   - Fallback: rule-based scoring if model unavailable

5. RISK SCORING
   Blended score 0–100
   0–29 LOW | 30–59 MEDIUM | 60–79 HIGH | 80+ CRITICAL
   (prototype thresholds — not scientifically validated)

6. CATEGORY DETECTION (risk_engine.py)
   Feature-based heuristic mapping to 12 scam categories

7. SOCIAL ENGINEERING DETECTION
   Per-technique confidence from feature subscores:
   Urgency | Fear | Authority Impersonation | Reward Manipulation
   Credential Harvesting | Fake Verification Page | KYC Pretext | Scarcity

8. ATTACK CHAIN RECONSTRUCTION
   Template-based chains per category, e.g.
   Banking/KYC: Impersonation → Fear → KYC Pretext → Link → Credential Theft → Loss

9. EXPLAINABILITY
   Deterministic narrative from active features + risk level
   Optional LLM enhancement if API key configured

10. RECOMMENDATIONS
    Category-specific DO/DONT lists

11. EVIDENCE CORRELATION
    URLs, keywords, phone numbers tagged as risk indicators

12. DATABASE PERSISTENCE
    Scan → Evidence → (optional) RecoverySession
```

---

## Database Schema

```sql
CREATE TABLE scans (
  id            INTEGER PRIMARY KEY,
  created_at    DATETIME DEFAULT NOW,
  input_type    VARCHAR(20),         -- text|url|image|qr|document
  raw_text      TEXT,
  extracted_text TEXT,
  risk_score    FLOAT,
  risk_level    VARCHAR(10),          -- LOW|MEDIUM|HIGH|CRITICAL
  category      VARCHAR(100),
  summary       TEXT,
  analysis_json TEXT                  -- full result JSON blob
);

CREATE TABLE evidence (
  id            INTEGER PRIMARY KEY,
  scan_id       INTEGER REFERENCES scans(id),
  type          VARCHAR(50),           -- url|phone|keyword|qr
  value         TEXT,
  risk_indicator BOOLEAN
);

CREATE TABLE recovery_sessions (
  id               INTEGER PRIMARY KEY,
  scan_id          INTEGER REFERENCES scans(id) NULLABLE,
  interaction_type VARCHAR(50),
  created_at       DATETIME DEFAULT NOW
);
```

---

## Data Flow: Text Analysis Request

```
POST /api/analyze/text  { text: "...", language: "en" }
  │
  ├─ Pydantic validates text (min_length=1, max_length=10000)
  ├─ analyze_text(text, language)
  │   ├─ get_predictor().predict(text)
  │   │   ├─ extract_text_features(text)  → 35 numeric features
  │   │   ├─ vectorizer.transform(text)   → TF-IDF 5000 dims
  │   │   ├─ model.predict_proba()        → [p_safe, p_sus, p_scam]
  │   │   └─ blend ML + rule score        → final risk_score 0-100
  │   ├─ score_to_risk_level(score)       → "HIGH"
  │   ├─ detect_category(text, features)  → "Banking/KYC Scam"
  │   ├─ build_indicators(...)            → list[Indicator]
  │   ├─ detect_social_engineering(...)   → list[Technique]
  │   ├─ build_attack_chain(category)     → list[Step]
  │   ├─ build_recommendations(...)       → list[Rec]
  │   └─ generate_summary/explanation     → str
  ├─ save_scan(db, result, "text")        → scan_id
  └─ return ApiResponse { success, data }
```
