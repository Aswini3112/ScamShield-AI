"""
Text feature extraction for scam detection.
Returns a flat dict of numeric features used by both training and inference.
"""
from __future__ import annotations

import re
import math
from typing import Any

# ── Keyword lists ─────────────────────────────────────────────────────────────

URGENCY_WORDS = [
    "immediately", "urgent", "urgently", "right now", "right away",
    "hurry", "quick", "quickly", "asap", "today", "within 24 hours",
    "within 2 hours", "expire", "expiring", "last chance", "deadline",
    "avasaram", "urgent ah", "immediate ah",  # Tamil/Tanglish
]

FEAR_WORDS = [
    "block", "blocked", "suspend", "suspended", "deactivate", "deactivated",
    "arrest", "legal action", "police", "court", "penalty", "fine",
    "account closure", "termination", "warning", "alert", "violation",
    "criminal", "warrant", "freeze", "frozen",
]

THREAT_WORDS = [
    "you will be", "you will face", "failure to", "if you do not",
    "consequences", "punished", "prosecuted", "reported",
]

PAYMENT_WORDS = [
    "pay", "payment", "transfer", "send money", "upi", "neft", "imps",
    "wire transfer", "paytm", "gpay", "phonepe", "google pay",
    "rs.", "inr", "rupees", "₹", "amount", "fee", "charge",
    "customs", "clearance fee", "registration fee", "processing fee",
]

OTP_WORDS = [
    "otp", "one time password", "verification code", "pin",
    "share otp", "enter otp", "confirm otp",
]

PASSWORD_WORDS = [
    "password", "passcode", "credentials", "login details",
    "account details", "banking details",
]

CREDENTIAL_REQUEST = [
    "enter your", "provide your", "submit your", "share your",
    "aadhaar", "aadhar", "pan card", "pan number", "dob", "date of birth",
    "account number", "ifsc", "card number", "cvv", "expiry",
]

REWARD_WORDS = [
    "congratulations", "winner", "won", "prize", "lucky", "reward",
    "bonus", "cashback", "offer", "free", "gift", "selected",
    "exclusive", "guaranteed", "double", "triple",
]

IMPERSONATION_WORDS = [
    "bank", "rbi", "sebi", "income tax", "it department", "police",
    "government", "ministry", "helpdesk", "customer care", "support team",
    "official", "authorized", "verified",
]

JOB_WORDS = [
    "work from home", "wfh", "job offer", "hiring", "recruitment",
    "apply now", "vacancy", "salary", "earn per month", "per day",
    "no experience", "part time", "full time", "remote job",
]

INVESTMENT_WORDS = [
    "invest", "investment", "returns", "profit", "trading", "crypto",
    "bitcoin", "forex", "guaranteed returns", "daily profit",
    "monthly returns", "portfolio", "scheme",
]

KYC_WORDS = [
    "kyc", "know your customer", "kyc update", "kyc verification",
    "kyc pending", "complete kyc", "kyc expiry",
]

QR_WORDS = [
    "scan qr", "qr code", "scan to pay", "scan to receive",
    "qr attached", "scan this",
]

SUSPICIOUS_CTA = [
    "click here", "click the link", "visit the link", "open the link",
    "tap here", "go to", "login at", "verify at", "confirm at",
    "download the app", "install the app", "call us at",
]

# Suspicious TLDs commonly used in fraud
SUSPICIOUS_TLDS = {
    ".xyz", ".tk", ".ml", ".ga", ".cf", ".gq", ".top",
    ".click", ".download", ".win", ".loan", ".online", ".site",
}

# Known URL shortener domains
URL_SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly",
    "tiny.cc", "is.gd", "buff.ly", "rebrand.ly",
}


# ── URL helpers ───────────────────────────────────────────────────────────────

_URL_RE = re.compile(
    r"https?://[^\s<>\"]+|www\.[^\s<>\"]+", re.IGNORECASE
)
_PHONE_RE = re.compile(r"\b(\+91[\-\s]?)?[6-9]\d{9}\b")
_CURRENCY_RE = re.compile(r"(rs\.?|inr|₹)\s*\d+", re.IGNORECASE)


def extract_urls(text: str) -> list[str]:
    return _URL_RE.findall(text)


def extract_phones(text: str) -> list[str]:
    return _PHONE_RE.findall(text)


def _count_keywords(text: str, keywords: list[str]) -> int:
    tl = text.lower()
    return sum(1 for kw in keywords if kw in tl)


def _has_keyword(text: str, keywords: list[str]) -> bool:
    tl = text.lower()
    return any(kw in tl for kw in keywords)


def _get_keyword_evidence(text: str, keywords: list[str], max_items: int = 5) -> list[str]:
    tl = text.lower()
    return [kw for kw in keywords if kw in tl][:max_items]


# ── URL feature extraction ────────────────────────────────────────────────────

def extract_url_features(url: str) -> dict[str, Any]:
    """Static analysis of a single URL — no network requests made."""
    from urllib.parse import urlparse, parse_qs

    feats: dict[str, Any] = {
        "url_length": len(url),
        "has_https": url.startswith("https://"),
        "has_ip_address": bool(re.search(r"https?://\d{1,3}(\.\d{1,3}){3}", url)),
        "is_url_shortener": False,
        "has_suspicious_tld": False,
        "subdomain_count": 0,
        "special_char_count": 0,
        "has_encoded_chars": "%" in url,
        "path_depth": 0,
        "has_suspicious_keywords": False,
        "domain_length": 0,
        "query_param_count": 0,
        "domain": "",
        "tld": "",
    }

    try:
        parsed = urlparse(url)
        hostname = parsed.netloc.lower().split(":")[0]
        feats["domain"] = hostname
        feats["domain_length"] = len(hostname)

        # TLD
        parts = hostname.split(".")
        tld = "." + parts[-1] if parts else ""
        feats["tld"] = tld
        feats["has_suspicious_tld"] = tld in SUSPICIOUS_TLDS

        # Subdomain count
        feats["subdomain_count"] = max(0, len(parts) - 2)

        # Shortener
        bare = ".".join(parts[-2:]) if len(parts) >= 2 else hostname
        feats["is_url_shortener"] = bare in URL_SHORTENERS

        # Special characters in hostname
        feats["special_char_count"] = sum(1 for c in hostname if c in "-_~")

        # Path depth
        path = parsed.path
        feats["path_depth"] = len([p for p in path.split("/") if p])

        # Query params
        feats["query_param_count"] = len(parse_qs(parsed.query))

        # Suspicious keywords in full URL
        url_lower = url.lower()
        suspicious_url_keywords = [
            "login", "verify", "secure", "update", "confirm", "account",
            "kyc", "otp", "bank", "credential", "password", "signin",
        ]
        feats["has_suspicious_keywords"] = any(k in url_lower for k in suspicious_url_keywords)

    except Exception:
        pass

    return feats


# ── Main text feature extraction ──────────────────────────────────────────────

def extract_text_features(text: str) -> dict[str, Any]:
    """
    Extract ~30 numeric/boolean features from raw text.
    These features feed directly into the ML model.
    """
    text_lower = text.lower()
    words = text_lower.split()
    word_count = max(len(words), 1)
    char_count = max(len(text), 1)

    urls = extract_urls(text)
    phones = extract_phones(text)
    currencies = _CURRENCY_RE.findall(text_lower)

    # Capitalisation ratio
    upper_chars = sum(1 for c in text if c.isupper())
    cap_ratio = upper_chars / char_count

    # Punctuation excess
    exclamation_count = text.count("!")
    question_count = text.count("?")

    feats: dict[str, Any] = {
        # Length features
        "text_length": len(text),
        "word_count": word_count,
        "avg_word_length": char_count / word_count,
        "capitalisation_ratio": round(cap_ratio, 3),
        "exclamation_count": exclamation_count,
        "question_count": question_count,

        # Entity counts
        "url_count": len(urls),
        "phone_count": len(phones),
        "currency_mention_count": len(currencies),

        # Keyword categories (counts)
        "urgency_score": _count_keywords(text, URGENCY_WORDS),
        "fear_score": _count_keywords(text, FEAR_WORDS),
        "threat_score": _count_keywords(text, THREAT_WORDS),
        "payment_score": _count_keywords(text, PAYMENT_WORDS),
        "otp_score": _count_keywords(text, OTP_WORDS),
        "credential_score": _count_keywords(text, CREDENTIAL_REQUEST),
        "reward_score": _count_keywords(text, REWARD_WORDS),
        "impersonation_score": _count_keywords(text, IMPERSONATION_WORDS),
        "job_score": _count_keywords(text, JOB_WORDS),
        "investment_score": _count_keywords(text, INVESTMENT_WORDS),
        "kyc_score": _count_keywords(text, KYC_WORDS),
        "qr_score": _count_keywords(text, QR_WORDS),
        "cta_score": _count_keywords(text, SUSPICIOUS_CTA),
        "password_score": _count_keywords(text, PASSWORD_WORDS),

        # Boolean flags
        "has_urgency": int(_has_keyword(text, URGENCY_WORDS)),
        "has_fear": int(_has_keyword(text, FEAR_WORDS)),
        "has_payment": int(_has_keyword(text, PAYMENT_WORDS)),
        "has_credential_request": int(_has_keyword(text, CREDENTIAL_REQUEST)),
        "has_impersonation": int(_has_keyword(text, IMPERSONATION_WORDS)),
        "has_reward": int(_has_keyword(text, REWARD_WORDS)),
        "has_suspicious_url": int(any(
            any(tld in u.lower() for tld in SUSPICIOUS_TLDS) or
            _has_keyword(u, ["login", "verify", "kyc", "otp", "confirm"])
            for u in urls
        )),
        "has_job_offer": int(_has_keyword(text, JOB_WORDS)),
        "has_investment": int(_has_keyword(text, INVESTMENT_WORDS)),
        "has_kyc": int(_has_keyword(text, KYC_WORDS)),
        "has_qr": int(_has_keyword(text, QR_WORDS)),
        "has_shortener": int(any(
            any(s in u.lower() for s in URL_SHORTENERS) for u in urls
        )),
    }

    return feats


def get_evidence_keywords(text: str) -> dict[str, list[str]]:
    """Return keyword evidence grouped by category — used for UI display."""
    return {
        "urgency": _get_keyword_evidence(text, URGENCY_WORDS),
        "fear": _get_keyword_evidence(text, FEAR_WORDS),
        "payment": _get_keyword_evidence(text, PAYMENT_WORDS),
        "credential": _get_keyword_evidence(text, CREDENTIAL_REQUEST),
        "impersonation": _get_keyword_evidence(text, IMPERSONATION_WORDS),
        "reward": _get_keyword_evidence(text, REWARD_WORDS),
        "kyc": _get_keyword_evidence(text, KYC_WORDS),
        "job": _get_keyword_evidence(text, JOB_WORDS),
        "investment": _get_keyword_evidence(text, INVESTMENT_WORDS),
        "otp": _get_keyword_evidence(text, OTP_WORDS),
    }
