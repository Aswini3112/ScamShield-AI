# ScamShield AI — API Reference

Base URL: `http://localhost:8000/api`  
Interactive docs: `http://localhost:8000/api/docs`

All responses follow this envelope:
```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

---

## GET /health

Health check.

**Response**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "ml_model_loaded": true,
  "ml_method": "ml_model"
}
```

---

## POST /analyze/text

Analyse a suspicious text message.

**Request**
```json
{
  "text": "Your bank account will be blocked. KYC: http://fake.xyz",
  "language": "en"
}
```
`language`: `"en"` | `"ta"` (Tamil) | `"tg"` (Tanglish)

**Response** — `data` is `AnalysisResult`:
```json
{
  "id": 1,
  "risk_score": 72,
  "risk_level": "HIGH",
  "category": "Banking/KYC Scam",
  "summary": "This content shows strong indicators of a Banking/KYC Scam...",
  "indicators": [
    { "name": "Urgency", "detected": true, "confidence": 80, "evidence": ["today"] }
  ],
  "social_engineering": [
    { "technique": "KYC Pretext", "confidence": 85, "description": "...", "evidence": ["kyc"] }
  ],
  "attack_chain": [
    { "step": 1, "title": "Bank/Authority Impersonation", "description": "..." }
  ],
  "recommendations": [
    { "type": "do", "text": "Verify through official channels." },
    { "type": "dont", "text": "Do not share OTP." }
  ],
  "evidence": [
    { "type": "url", "value": "http://fake.xyz", "risk_indicator": true }
  ],
  "extracted_text": "...",
  "extracted_urls": ["http://fake.xyz"],
  "explanation": "ScamShield assessed this as HIGH risk...",
  "input_type": "text",
  "multilingual_note": null
}
```

---

## POST /analyze/url

Static URL analysis — no network request made to target URL.

**Request**
```json
{ "url": "http://fake-bank-kyc.xyz/verify?id=12345" }
```

**Response** — same `AnalysisResult` shape. Key fields:
```json
{
  "risk_score": 65,
  "risk_level": "HIGH",
  "category": "Suspicious URL",
  "indicators": [
    { "name": "Suspicious TLD", "detected": true, "confidence": 85 },
    { "name": "Suspicious Keywords in URL", "detected": true, "confidence": 75 }
  ]
}
```

---

## POST /analyze/image

Upload a screenshot for OCR analysis.

**Request** — multipart/form-data
```
file: <image file>   (PNG, JPG, WEBP — max 10 MB)
```

**Response** — `AnalysisResult` with additional fields:
```json
{
  "extracted_text": "OCR extracted text...",
  "qr_detected": false,
  "qr_content": null
}
```

---

## POST /analyze/qr

Upload an image containing a QR code.

**Request** — multipart/form-data
```
file: <image file>   (PNG, JPG — max 10 MB)
```

**Response**
```json
{
  "qr_detected": true,
  "qr_content": "http://scam-payment.xyz/collect",
  "risk_score": 78,
  "category": "QR Scam"
}
```

---

## POST /analyze/document

Upload a PDF or text document.

**Request** — multipart/form-data
```
file: <PDF or TXT file — max 10 MB>
```

**Response** — same as text analysis, applied to extracted document text.

---

## GET /scans

Scan history list.

**Query params:** `skip=0`, `limit=50`

**Response** — array of `ScanListItem`:
```json
[
  {
    "id": 1,
    "created_at": "2026-09-30T16:45:00",
    "input_type": "text",
    "category": "Banking/KYC Scam",
    "risk_level": "HIGH",
    "risk_score": 72,
    "summary": "..."
  }
]
```

---

## GET /scans/{id}

Single scan full report.

**Response** — full `AnalysisResult` (same as analyze endpoint).

**404** if scan not found.

---

## GET /dashboard/stats

Dashboard statistics.

**Response**
```json
{
  "total_scans": 24,
  "critical_count": 2,
  "high_risk_count": 5,
  "medium_risk_count": 7,
  "low_risk_count": 10,
  "category_distribution": { "Banking/KYC Scam": 4, "Job/Recruitment Scam": 3 },
  "risk_distribution": { "HIGH": 5, "MEDIUM": 7, "LOW": 10, "CRITICAL": 2 },
  "recent_threats": [ ... ],
  "top_techniques": [
    { "technique": "Urgency", "count": 8 },
    { "technique": "Fear", "count": 6 }
  ]
}
```

---

## POST /recovery

Submit recovery interaction and get guidance.

**Request**
```json
{
  "scan_id": 1,
  "interaction_type": "transferred_money"
}
```

`interaction_type` values:
- `only_received`
- `clicked_link`
- `entered_credentials`
- `shared_otp`
- `transferred_money`
- `downloaded_file`
- `not_sure`

**Response** — `RecoveryGuidance`:
```json
{
  "interaction_type": "transferred_money",
  "severity": "critical",
  "headline": "Money transferred — act within 30 minutes for best recovery chance.",
  "steps": [
    {
      "priority": "immediate",
      "title": "Call 1930 (National Cyber Crime Helpline) NOW",
      "description": "...",
      "action": "Call 1930 right now."
    }
  ],
  "hotlines": [
    { "name": "National Cyber Crime Helpline", "number": "1930" },
    { "name": "Cyber Crime Portal", "number": "cybercrime.gov.in" }
  ]
}
```

---

## Error Responses

| Status | Meaning |
|---|---|
| 422 | Validation error (missing/invalid fields) |
| 404 | Scan not found |
| 413 | File too large |
| 415 | Unsupported file type |
| 429 | Rate limit exceeded |
| 500 | Internal server error (generic message) |
