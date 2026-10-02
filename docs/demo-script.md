# ScamShield AI — Hackathon Demo Script

**Duration:** 4–5 minutes  
**URL:** http://localhost:5173  
**Presenter tip:** Have the application open and loaded before you start. Keep the browser full-screen.

---

## 00:00 — Hook (30 seconds)

> "Every day, millions of Indians receive messages like this:"

*(Show a phone or read aloud:)*
> *"URGENT: Your bank account will be BLOCKED today. Complete KYC immediately: http://exmpl-bank-kyc.xyz/verify"*

> "Most existing tools tell you: 'This looks suspicious.' And then... nothing. No explanation. No context. No guidance."

> "ScamShield AI goes further. We don't just detect the scam. We explain how the attack works — and tell you exactly what to do."

---

## 00:30 — Landing Page (20 seconds)

> "This is ScamShield AI — a multimodal scam investigation platform."

*(Scroll slowly through the landing page)*

> "Notice the analysis pipeline: Input → Evidence Analysis → Threat Detection → Attack Chain → Risk Assessment. That's our differentiation."

> "Five input types: text, screenshots, URLs, QR codes, and documents."

---

## 00:50 — Text Analysis: Banking Scam (90 seconds)

1. Click **"Analyze Now"**
2. On the Analyze page, click demo button **"Banking / KYC"**
   - This auto-fills the text area with a fake KYC scam
3. Point out: *"This is the kind of message that gets thousands of people every day."*
4. Click **"Analyze Threat"**
5. Watch the 5-step progress animation:
   - *"Extracting evidence... Inspecting indicators... Evaluating threat patterns... Building attack chain... Preparing security report"*

**On the result page:**

> "Risk score: HIGH. 72 out of 100. Category: Banking/KYC Scam."

**WHY THIS IS SUSPICIOUS section:**
> "ScamShield detected Urgency — it found the words 'immediately' and 'today'. Fear — 'blocked' and 'suspended'. A suspicious URL with a .xyz domain. KYC pretext."

**SOCIAL ENGINEERING section:**
> "Five techniques identified. Notice these aren't just labels — each has a confidence score and actual evidence from the text. KYC Pretext at 85%. Fake Verification Page at 82%."

**ATTACK CHAIN section:**
> "This is what makes ScamShield unique. We reconstruct the attacker's strategy step by step: Impersonation → Fear → KYC Pretext → Link Redirect → Credential Harvesting → Account Takeover → Financial Loss. The judge sees exactly how the scam is designed to work."

---

## 02:20 — Recovery Mode (40 seconds)

> "Now here's a question: what about the person who already clicked the link?"

1. Scroll down to **"I Already Interacted"** button
2. Click it — the Recovery Modal opens
3. Select **"I transferred money"**
4. Click **"Get Recovery Guidance"**

> "Severity: CRITICAL. First action: Call 1930 — that's India's National Cyber Crime Helpline — within 30 minutes. Banks can sometimes reverse transactions if reported fast enough."

> "ScamShield provides step-by-step guidance with priority levels: Act Now, Do Soon, Monitor. Not just 'be careful' — actual actionable steps."

---

## 03:00 — URL Analysis (30 seconds)

1. Go back to **Analyze**
2. Click the **URL** tab
3. Type or paste: `http://fake-bank-kyc.xyz/verify?user=12345`
4. Click **Analyze Threat**

> "URLs are analyzed statically — the backend never fetches the URL, eliminating SSRF risk. But it detects suspicious TLD (.xyz), suspicious keywords (kyc, verify), excessive path depth, no HTTPS."

---

## 03:30 — Tanglish Demo (20 seconds)

1. Back to **Analyze → Text** tab
2. Click demo button **"Tanglish Scam"**

> "ScamShield supports English, Tamil, and Tanglish — the code-switched language millions of Indians actually use. This is a prototype multilingual feature, not full NLP, but it correctly identifies the KYC scam pattern."

3. Click Analyze — show the risk result

---

## 03:50 — Dashboard (30 seconds)

1. Navigate to **Dashboard**

> "After analyzing multiple scams, the dashboard shows you the threat landscape: category distribution, risk distribution, recent high-risk threats, and top social engineering techniques."

> "All data is real — backed by SQLite, powered by actual analysis results."

---

## 04:20 — Technical Architecture (30 seconds)

> "Under the hood: React + TypeScript frontend. FastAPI backend. SQLAlchemy with async SQLite. A Random Forest classifier trained on TF-IDF plus 35 hand-crafted features — things like urgency score, fear score, credential request detection, suspicious URL patterns."

> "The model achieves 96.5% accuracy on our synthetic test set. Important caveat: that's synthetic data, so real-world performance would require a proper labelled dataset from actual incidents."

> "If no ML model is trained yet, the system falls back to a deterministic rule-based engine — the application never fails."

---

## 04:50 — Closing Pitch (15 seconds)

> "ScamShield AI: we detect, investigate, explain, and guide. Because knowing 'this is a scam' isn't enough — you need to understand the attack, and know exactly what to do next."

> "Thank you."

---

## Backup scenarios (if time allows)

- **Job scam demo:** Click "Job Scam" demo → shows recruitment fraud attack chain
- **Investment scam:** Click "Investment Scam" → shows Ponzi/trading scam pattern
- **Safe message:** Click "Safe Message" → show LOW risk (correct non-detection)
- **Learn page:** Navigate to Learn → show cybersecurity awareness content
- **History page:** Show history with multiple scans, filter by HIGH risk

---

## Key talking points (for Q&A)

**"Why not just use ChatGPT for this?"**
> "LLMs are optional in ScamShield. The core risk score is determined by a trained ML model — it can't be overridden by text content or prompt injection. LLMs improve the explanation layer only."

**"How do you handle Tamil/Tanglish?"**
> "Currently keyword-based — we look for scam patterns in transliterated Tamil. Full multilingual NLP with IndicBERT or MuRIL would be the next step."

**"Is this production-ready?"**
> "This is a prototype built in a hackathon. For production, we'd need: a real labelled dataset from verified scam reports, real-time URL reputation APIs, user authentication, and rigorous security review."

**"What's the attack chain based on?"**
> "Template-based reconstruction per scam category, derived from research on how each scam type typically operates. For example, banking KYC scams always follow: impersonation → fear → KYC pretext → link → credential harvest. Verified against public cybercrime reporting patterns."
