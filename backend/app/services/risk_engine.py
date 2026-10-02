"""
Risk Engine — converts raw ML/rule scores into structured risk levels,
categories, social-engineering detections, attack chains, and recommendations.
"""
from __future__ import annotations

from typing import Any

from app.ml.feature_extractor import (
    get_evidence_keywords,
    extract_urls,
    URGENCY_WORDS, FEAR_WORDS, IMPERSONATION_WORDS,
    REWARD_WORDS, KYC_WORDS, PAYMENT_WORDS, OTP_WORDS,
    CREDENTIAL_REQUEST, JOB_WORDS, INVESTMENT_WORDS, QR_WORDS,
)
from app.schemas.analysis import (
    Indicator, SocialEngineeringTechnique, AttackChainStep,
    Recommendation, EvidenceItem,
)


# ── Risk level mapping ────────────────────────────────────────────────────────

def score_to_risk_level(score: int) -> str:
    """
    Product-level risk bands (prototype thresholds — not scientifically validated).
    0-29  LOW
    30-59 MEDIUM
    60-79 HIGH
    80+   CRITICAL
    """
    if score >= 80:
        return "CRITICAL"
    if score >= 60:
        return "HIGH"
    if score >= 30:
        return "MEDIUM"
    return "LOW"


# ── Category detection ────────────────────────────────────────────────────────

def detect_category(text: str, features: dict[str, Any]) -> str:
    """Heuristic category detection from features."""
    tl = text.lower()

    if features.get("kyc_score", 0) >= 1 or features.get("has_kyc"):
        return "Banking/KYC Scam"
    if features.get("job_score", 0) >= 2 or features.get("has_job_offer"):
        return "Job/Recruitment Scam"
    if features.get("investment_score", 0) >= 2 or features.get("has_investment"):
        return "Investment Scam"
    if features.get("qr_score", 0) >= 2 or features.get("has_qr"):
        return "QR Scam"
    if features.get("otp_score", 0) >= 1:
        return "UPI/Payment Scam"
    if features.get("has_payment") and features.get("url_count", 0) >= 1:
        return "UPI/Payment Scam"
    if features.get("has_credential_request") and features.get("has_suspicious_url"):
        return "Credential Phishing"
    if features.get("impersonation_score", 0) >= 2:
        # Determine which authority
        if any(w in tl for w in ["income tax", "it department", "police", "ministry", "government"]):
            return "Government Impersonation"
        if any(w in tl for w in ["delivery", "courier", "parcel", "package", "shipment"]):
            return "Delivery/Courier Scam"
        return "Customer Support Scam"
    if features.get("has_reward") and features.get("url_count", 0) >= 1:
        return "Social Media Scam"
    if features.get("has_suspicious_url") or features.get("url_count", 0) >= 1:
        return "Credential Phishing"
    if features.get("urgency_score", 0) >= 2 or features.get("fear_score", 0) >= 2:
        return "Financial Scam"
    return "Other Suspicious Activity"


# ── Indicators ────────────────────────────────────────────────────────────────

def build_indicators(text: str, features: dict[str, Any]) -> list[Indicator]:
    evidence = get_evidence_keywords(text)
    urls = extract_urls(text)

    def _conf(score: float, multiplier: float = 15) -> int:
        return min(int(score * multiplier + 50), 98) if score > 0 else 30

    indicators: list[Indicator] = [
        Indicator(
            name="Urgency",
            detected=bool(features.get("has_urgency")),
            confidence=_conf(features.get("urgency_score", 0)),
            evidence=evidence["urgency"],
        ),
        Indicator(
            name="Fear / Threat",
            detected=bool(features.get("has_fear")),
            confidence=_conf(features.get("fear_score", 0)),
            evidence=evidence["fear"],
        ),
        Indicator(
            name="Payment Request",
            detected=bool(features.get("has_payment")),
            confidence=_conf(features.get("payment_score", 0), 12),
            evidence=evidence["payment"],
        ),
        Indicator(
            name="OTP / PIN Request",
            detected=features.get("otp_score", 0) > 0,
            confidence=_conf(features.get("otp_score", 0), 25),
            evidence=evidence["otp"],
        ),
        Indicator(
            name="Credential Request",
            detected=bool(features.get("has_credential_request")),
            confidence=_conf(features.get("credential_score", 0), 18),
            evidence=evidence["credential"],
        ),
        Indicator(
            name="Impersonation",
            detected=bool(features.get("has_impersonation")),
            confidence=_conf(features.get("impersonation_score", 0), 12),
            evidence=evidence["impersonation"],
        ),
        Indicator(
            name="Suspicious URL",
            detected=bool(features.get("has_suspicious_url") or (urls and features.get("has_suspicious_url"))),
            confidence=80 if features.get("has_suspicious_url") else (50 if urls else 10),
            evidence=[u[:60] for u in urls[:3]],
        ),
        Indicator(
            name="KYC Request",
            detected=bool(features.get("has_kyc")),
            confidence=_conf(features.get("kyc_score", 0), 25),
            evidence=evidence["kyc"],
        ),
        Indicator(
            name="Fake Job Offer",
            detected=bool(features.get("has_job_offer")),
            confidence=_conf(features.get("job_score", 0), 15),
            evidence=evidence["job"],
        ),
        Indicator(
            name="Investment Scheme",
            detected=bool(features.get("has_investment")),
            confidence=_conf(features.get("investment_score", 0), 15),
            evidence=evidence["investment"],
        ),
        Indicator(
            name="Reward / Prize Manipulation",
            detected=bool(features.get("has_reward")),
            confidence=_conf(features.get("reward_score", 0), 12),
            evidence=evidence["reward"],
        ),
        Indicator(
            name="QR Code Related",
            detected=bool(features.get("has_qr")),
            confidence=_conf(features.get("qr_score", 0), 20),
            evidence=[],
        ),
        Indicator(
            name="URL Shortener",
            detected=bool(features.get("has_shortener")),
            confidence=75 if features.get("has_shortener") else 5,
            evidence=[],
        ),
    ]
    return indicators


# ── Social Engineering ────────────────────────────────────────────────────────

def detect_social_engineering(
    text: str, features: dict[str, Any]
) -> list[SocialEngineeringTechnique]:
    techs: list[SocialEngineeringTechnique] = []
    evidence = get_evidence_keywords(text)

    if features.get("has_urgency"):
        techs.append(SocialEngineeringTechnique(
            technique="Urgency",
            confidence=min(50 + features.get("urgency_score", 1) * 15, 97),
            description="Creates time pressure to bypass rational decision-making.",
            evidence=evidence["urgency"][:4],
        ))

    if features.get("has_fear"):
        techs.append(SocialEngineeringTechnique(
            technique="Fear",
            confidence=min(50 + features.get("fear_score", 1) * 12, 96),
            description="Triggers fight-or-flight response by threatening negative consequences.",
            evidence=evidence["fear"][:4],
        ))

    if features.get("has_impersonation"):
        techs.append(SocialEngineeringTechnique(
            technique="Authority Impersonation",
            confidence=min(50 + features.get("impersonation_score", 1) * 12, 95),
            description="Impersonates trusted authorities (bank, government, police) to demand compliance.",
            evidence=evidence["impersonation"][:4],
        ))

    if features.get("has_reward"):
        techs.append(SocialEngineeringTechnique(
            technique="Reward Manipulation",
            confidence=min(50 + features.get("reward_score", 1) * 10, 90),
            description="Uses prizes, winnings, or bonuses to lower the victim's guard.",
            evidence=evidence["reward"][:4],
        ))

    if features.get("has_credential_request") or features.get("otp_score", 0) > 0:
        techs.append(SocialEngineeringTechnique(
            technique="Credential Harvesting",
            confidence=min(60 + features.get("credential_score", 1) * 10, 97),
            description="Solicits OTP, passwords, Aadhaar, or account details under a false pretext.",
            evidence=(evidence["credential"] + evidence["otp"])[:4],
        ))

    if features.get("has_suspicious_url"):
        techs.append(SocialEngineeringTechnique(
            technique="Fake Verification Page",
            confidence=82,
            description="Directs victim to a fraudulent lookalike website to steal credentials.",
            evidence=["suspicious link detected"],
        ))

    if features.get("has_kyc"):
        techs.append(SocialEngineeringTechnique(
            technique="KYC Pretext",
            confidence=85,
            description="Uses mandatory KYC compliance as a cover story to extract identity documents.",
            evidence=evidence["kyc"][:4],
        ))

    if features.get("has_job_offer"):
        techs.append(SocialEngineeringTechnique(
            technique="Trust Exploitation",
            confidence=min(55 + features.get("job_score", 1) * 8, 88),
            description="Exploits the victim's desire for employment to extract fees or documents.",
            evidence=evidence["job"][:4],
        ))

    # Scarcity (a subset of reward manipulation)
    tl = text.lower()
    if any(w in tl for w in ["limited slots", "only 3 left", "last offer", "expires today"]):
        techs.append(SocialEngineeringTechnique(
            technique="Scarcity",
            confidence=78,
            description="Creates an artificial sense of scarcity to pressure immediate action.",
            evidence=[w for w in ["limited slots", "only 3 left", "last offer", "expires today"] if w in tl],
        ))

    return techs


# ── Attack Chain ──────────────────────────────────────────────────────────────

_CHAIN_TEMPLATES: dict[str, list[tuple[str, str]]] = {
    "Banking/KYC Scam": [
        ("Bank/Authority Impersonation", "Message appears to come from a legitimate bank or RBI."),
        ("Fear / Urgency", "Victim is told account will be blocked or penalised."),
        ("KYC / Verification Pretext", "A fake KYC update requirement is presented."),
        ("Link / QR Redirect", "Victim is directed to a fraudulent verification page."),
        ("Credential Harvesting", "OTP, passwords, and identity documents are collected."),
        ("Account Takeover", "Attacker gains full access to banking account."),
        ("Financial Loss", "Funds transferred or identity used for fraud."),
    ],
    "Job/Recruitment Scam": [
        ("Attractive Job Offer", "Victim receives a high-paying, low-barrier job offer."),
        ("Trust Building", "Fake job portal, LinkedIn profile, or company branding presented."),
        ("Document Collection", "Aadhaar, PAN, bank details requested for 'onboarding'."),
        ("Fee Extraction", "Registration, security deposit, or training fee demanded."),
        ("Disappearance", "After payment, attacker becomes unreachable."),
    ],
    "UPI/Payment Scam": [
        ("Buyer/Seller Approach", "Victim is approached as a buyer or seller on a platform."),
        ("Fake Payment Claim", "Attacker claims to have sent money or sends a fake screenshot."),
        ("QR / Collect Request", "Victim is asked to 'accept' payment via QR or collect request."),
        ("PIN Entry", "Victim enters UPI PIN — actually authorising a payment OUT."),
        ("Fund Loss", "Money is debited from victim's account."),
    ],
    "Investment Scam": [
        ("Attractive Returns", "Promised guaranteed high monthly returns with 'AI trading'."),
        ("Initial Trust", "Small withdrawals allowed to build trust."),
        ("Larger Investment Pressure", "Victim encouraged to invest more to unlock earnings."),
        ("Withdrawal Block", "'Tax' or 'processing fees' demanded to release funds."),
        ("Total Loss", "All invested funds become unreachable."),
    ],
    "Credential Phishing": [
        ("Impersonation", "Message appears to come from a trusted source."),
        ("Urgency / Fear", "Victim is pressured to act immediately."),
        ("Link Delivery", "Victim clicks a link to a lookalike website."),
        ("Credential Entry", "Login details, OTP, or card numbers are entered."),
        ("Account Compromise", "Attacker uses stolen credentials for fraud."),
    ],
    "Government Impersonation": [
        ("Official-Looking Notice", "Message pretends to be from police, IT dept, or ministry."),
        ("Legal Threat", "Arrest warrant, penalty, or tax demand threatened."),
        ("Panic Response", "Victim panics and tries to 'resolve' the issue quickly."),
        ("Payment / Data Demand", "Fine, tax, or personal documents demanded."),
        ("Fraud Completed", "Money transferred or identity compromised."),
    ],
}

_DEFAULT_CHAIN = [
    ("Suspicious Message", "Victim receives an unexpected, unsolicited communication."),
    ("Social Engineering", "Psychological pressure techniques applied."),
    ("Action Request", "Victim is asked to click, pay, or share information."),
    ("Exploitation", "Attacker achieves their goal — financial gain or data theft."),
]


def build_attack_chain(category: str, features: dict[str, Any]) -> list[AttackChainStep]:
    template = _CHAIN_TEMPLATES.get(category, _DEFAULT_CHAIN)
    return [
        AttackChainStep(step=i + 1, title=title, description=desc)
        for i, (title, desc) in enumerate(template)
    ]


# ── Recommendations ───────────────────────────────────────────────────────────

_BASE_DO = [
    "Verify this through the official website or customer care number (found on the card/official site).",
    "If in doubt, call the claimed organisation directly using a number you look up independently.",
    "Report suspicious messages to your bank's official fraud helpline.",
]

_BASE_DONT = [
    "Do not share your OTP, PIN, or password with anyone — including callers claiming to be from a bank.",
    "Do not click links in unsolicited SMS or WhatsApp messages.",
    "Do not transfer money based on instructions received via message.",
]

_EXTRA_RULES: dict[str, dict[str, list[str]]] = {
    "Banking/KYC Scam": {
        "do": ["Contact your bank directly via the number on the back of your card."],
        "dont": ["Do not enter Aadhaar/PAN on any website reached via an SMS link."],
    },
    "Job/Recruitment Scam": {
        "do": ["Verify the company on MCA21, LinkedIn, or their official website."],
        "dont": ["Do not pay any 'registration' or 'training' fee to get a job."],
    },
    "UPI/Payment Scam": {
        "do": ["Remember: you never need to enter your UPI PIN to RECEIVE money."],
        "dont": ["Do not scan QR codes sent by buyers to 'receive' payment."],
    },
    "Investment Scam": {
        "do": ["Check SEBI registration of any investment platform at sebi.gov.in."],
        "dont": ["Do not invest in schemes promising guaranteed returns."],
    },
    "Government Impersonation": {
        "do": ["All legitimate government notices arrive via official post or registered email."],
        "dont": ["Do not pay any 'fine' or 'tax' via WhatsApp links or QR codes."],
    },
}


def build_recommendations(
    category: str, features: dict[str, Any], risk_level: str
) -> list[Recommendation]:
    recs: list[Recommendation] = []

    for t in _BASE_DO:
        recs.append(Recommendation(type="do", text=t))
    for t in _BASE_DONT:
        recs.append(Recommendation(type="dont", text=t))

    extra = _EXTRA_RULES.get(category, {})
    for t in extra.get("do", []):
        recs.append(Recommendation(type="do", text=t))
    for t in extra.get("dont", []):
        recs.append(Recommendation(type="dont", text=t))

    return recs


# ── Summary generation ────────────────────────────────────────────────────────

def generate_summary(
    category: str, risk_level: str, features: dict[str, Any]
) -> str:
    parts = []

    if risk_level in ("CRITICAL", "HIGH"):
        parts.append(f"This content shows strong indicators of a {category}.")
    elif risk_level == "MEDIUM":
        parts.append(f"This content contains several suspicious patterns consistent with a {category}.")
    else:
        parts.append("This content appears mostly safe, but contains some minor caution signals.")

    if features.get("has_urgency"):
        parts.append("It uses urgency tactics to pressure the recipient into acting quickly.")
    if features.get("has_fear"):
        parts.append("It employs fear — threatening account suspension, legal action, or financial penalties.")
    if features.get("has_credential_request") or features.get("otp_score", 0) > 0:
        parts.append("It attempts to collect sensitive credentials, OTP, or personal documents.")
    if features.get("has_suspicious_url"):
        parts.append("It contains links that do not match legitimate organisations' domains.")
    if features.get("has_kyc"):
        parts.append("It uses a KYC compliance pretext to demand personal information.")

    return " ".join(parts)


# ── Explanation ───────────────────────────────────────────────────────────────

def generate_explanation(
    category: str,
    risk_level: str,
    features: dict[str, Any],
    method: str = "rule_based",
) -> str:
    note = "(assessed using rule-based analysis)" if method == "rule_based" else "(assessed using ML model)"

    base = f"ScamShield assessed this as {risk_level} risk {note}. "

    active = []
    if features.get("has_urgency"):
        active.append("urgency pressure")
    if features.get("has_fear"):
        active.append("fear / threat language")
    if features.get("has_impersonation"):
        active.append("authority impersonation")
    if features.get("has_credential_request") or features.get("otp_score", 0):
        active.append("credential harvesting attempt")
    if features.get("has_suspicious_url"):
        active.append("suspicious or domain-mismatched link")
    if features.get("has_kyc"):
        active.append("KYC pretext")
    if features.get("has_payment") and features.get("has_urgency"):
        active.append("payment under pressure")

    if active:
        base += "Key signals detected: " + ", ".join(active) + ". "

    base += (
        "This AI assessment is a decision-support tool. "
        "Always verify independently through official channels before taking any action."
    )
    return base
