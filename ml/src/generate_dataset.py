"""
ScamShield AI — Synthetic Dataset Generator
============================================
IMPORTANT DISCLAIMER
--------------------
All examples below are SYNTHETIC and generated for training/demo purposes only.
They use generic placeholder organisations (e.g. "Example Bank", "Example Courier").
This data does NOT represent real-world scam prevalence statistics.
It is NOT sourced from any real incident database.
Accuracy metrics produced from this data reflect only prototype performance on
synthetic examples — not real-world detection effectiveness.

Run: python ml/src/generate_dataset.py
Output: ml/data/raw/scam_dataset.csv
"""
from __future__ import annotations

import csv
import random
import sys
from pathlib import Path
from itertools import product

# ── Configuration ────────────────────────────────────────────────────────────
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "scam_dataset.csv"

# ── Label constants ────────────────────────────────────────────────────────
SAFE = 0
SUSPICIOUS = 1
SCAM = 2

# ── Template banks ────────────────────────────────────────────────────────────

# --- Banking / KYC Scam ---
BANKING_KYC_SCAM = [
    "URGENT: Your {bank} account will be BLOCKED today. Complete KYC immediately: {url}",
    "Dear Customer, your {bank} account KYC is incomplete. Update NOW or face suspension: {url}",
    "Your {bank} KYC has expired. Account will be deactivated in 24 hours. Click here: {url}",
    "ALERT: {bank} requires immediate KYC verification. Failure results in account closure. Visit: {url}",
    "Your {bank} Net Banking access is suspended due to incomplete KYC. Verify at: {url}",
    "{bank} KYC UPDATE REQUIRED. Submit Aadhaar and PAN immediately to avoid blocking: {url}",
    "FINAL WARNING: {bank} account activation requires KYC within 2 hours. Link: {url}",
    "Due to RBI mandate, your {bank} account needs KYC update. Do it now: {url}",
    "Your {bank} credit card will be cancelled unless KYC is updated today. Click: {url}",
    "Attention {bank} customer: incomplete KYC detected. Account freeze in 6 hours. Update: {url}",
    "Security Alert: {bank} has flagged your account for KYC non-compliance. Verify now: {url}",
    "Your {bank} UPI ID will be deactivated. Complete KYC verification: {url}",
    "Important: {bank} customer, your KYC expires today. Re-verify to continue banking: {url}",
]

# --- UPI / Payment Scam ---
UPI_PAYMENT_SCAM = [
    "Hi, I want to buy your item. Scan this QR to RECEIVE Rs.{amount}: {url}",
    "I've transferred Rs.{amount} to your UPI. Enter your PIN to confirm receipt. Hurry!",
    "You have received Rs.{amount} in UPI wallet. Scan QR to accept payment before it expires.",
    "Buyer for your OLX listing. Sending Rs.{amount}. Accept via UPI: {url}. Enter PIN to confirm.",
    "UPI payment of Rs.{amount} pending. Scan to accept: {url}. Valid for 5 minutes only.",
    "Your UPI collect request approved. Rs.{amount} awaiting. Enter PIN to receive: {url}",
    "Refund of Rs.{amount} initiated. Scan QR attached to receive your money back.",
    "Google Pay: You have a pending payment of Rs.{amount}. Tap to collect: {url}",
    "PhonePe: Incoming payment Rs.{amount}. Accept via PIN entry. Link: {url}",
    "Received Rs.{amount} from buyer. To unlock payment, enter UPI MPIN at: {url}",
]

# --- Job / Recruitment Scam ---
JOB_SCAM = [
    "Congratulations! Selected for WFH role at {company}. Earn Rs.{salary}/month. No experience. Apply: {url}",
    "Urgent Hiring: {company} needs 50 data entry operators. Work from home. Rs.{salary} monthly. WhatsApp: {phone}",
    "You are selected for Part Time Job at {company}! Earn Rs.{salary}/day. Register fee Rs.999. Contact: {phone}",
    "Job Alert: {company} hiring freshers. Rs.{salary}/month package. Send Aadhaar+PAN to confirm. Reply now.",
    "Excellent WFH opportunity at {company}. Guaranteed Rs.{salary} weekly. No experience needed. Fee: Rs.1499",
    "{company} is hiring! Earn Rs.{salary} from home doing simple tasks. Register at: {url}. Limited seats!",
    "Final Interview selected: {company} offers Rs.{salary} CTC. Pay Rs.2000 security deposit to confirm slot.",
    "URGENT: {company} requires 100 remote workers immediately. Rs.{salary}/month. WhatsApp CV: {phone}",
    "Genuine WFH Job: Type and earn Rs.{salary} daily. {company} is hiring. Register: {url}",
    "Congratulations! Your profile matches our requirements at {company}. Earn Rs.{salary}. Pay joining fee: Rs.500",
]

# --- Investment Scam ---
INVESTMENT_SCAM = [
    "Earn 40% monthly returns with our AI trading platform {company}. Guaranteed profits! Invest now: {url}",
    "Exclusive investment: Double your money in 30 days with {company}. Join {phone}",
    "Bitcoin/Crypto trading: Rs.10,000 becomes Rs.50,000 in 30 days. {company} guaranteed profits: {url}",
    "Join {company} investment group. Our algorithm has 99% success. Min invest Rs.5000. WhatsApp: {phone}",
    "Stock market expert signals: Earn Rs.{salary}/week guaranteed. Join {company}: {url}",
    "Forex trading with {company}: 150% monthly ROI. Limited seats. Register: {url}",
    "Mutual fund scam alert: {company} offers 35% p.a. guaranteed. No risk. Invest: {url}",
    "Ponzi scheme warning: {company} promises Rs.{salary} weekly for Rs.10,000 investment. Join: {phone}",
    "Crypto multiplier: Send Rs.5000, receive Rs.25,000 in 7 days via {company}. Hurry: {url}",
    "SEBI-unlicensed investment app {company}: Earn daily passive income. Download: {url}",
]

# --- Delivery / Courier Scam ---
DELIVERY_SCAM = [
    "Your {courier} parcel is held at customs. Pay Rs.{amount} clearance fee: {url}",
    "Delivery failed for your {courier} package. Pay Rs.{amount} redelivery fee at: {url}",
    "{courier}: Your shipment EC{tracking} requires customs duty Rs.{amount}. Pay now: {url}",
    "NOTICE: Your {courier} package will be returned if Rs.{amount} fee not paid in 24h: {url}",
    "{courier} Alert: Package held due to incomplete address. Update & pay Rs.{amount}: {url}",
    "Your Amazon order via {courier} requires Rs.{amount} import clearance. Pay: {url}",
    "Urgent: {courier} parcel needs address confirmation & Rs.{amount} payment: {url}",
    "{courier} delivery notification: Pay Rs.{amount} tax to release package. Click: {url}",
    "Your {courier} shipment {tracking} is on hold. Pay Rs.{amount} to proceed: {url}",
]

# --- Government Impersonation ---
GOVT_SCAM = [
    "NOTICE: Income Tax Dept. Tax dues Rs.{amount}. Pay immediately or face ARREST: {url}",
    "Cyber Crime Branch: Your Aadhaar used in fraud. Report immediately by calling {phone} or pay Rs.{amount}",
    "GST Dept: Your business has unpaid GST of Rs.{amount}. Pay now to avoid prosecution: {url}",
    "Ministry of Finance: FIR filed in your name. Clear dues Rs.{amount} to avoid arrest: {phone}",
    "TRAI: Your mobile number has been used for illegal activities. Pay Rs.{amount} or face disconnection: {url}",
    "Income Tax notice: Rs.{amount} tax refund pending. Submit bank details at: {url}",
    "Aadhaar suspension alert: Your Aadhaar linked to criminal case. Contact UIDAI at {phone} urgently.",
    "CBI notice: Your account flagged for money laundering. Pay Rs.{amount} or face arrest warrant.",
    "Electricity Board: Power will be cut in 2 hours if Rs.{amount} outstanding bill not paid: {phone}",
    "EPFO: Your PF account has an issue. Update KYC immediately or lose Rs.{amount}: {url}",
]

# --- Customer Support / Tech Support Scam ---
SUPPORT_SCAM = [
    "Microsoft Alert: Your PC has {count} viruses. Call our support: {phone} immediately. Do not ignore.",
    "Amazon Customer Care: Your account will be closed. Call {phone} to verify identity.",
    "Your Google account has been compromised. Call Google support: {phone} to secure your data.",
    "Bank customer support: Suspicious login detected on your account. Call {phone} now.",
    "PayTM Support: Your wallet is suspended. Share OTP to reactivate via {phone}.",
    "Netflix Account: Unusual activity detected. Call {phone} or account suspended.",
    "Your SIM will be deactivated in 2 hours. Call {phone} for verification immediately.",
    "Flipkart Support: Order issue with refund Rs.{amount}. Call {phone} to resolve.",
    "IRCTC help desk: Ticket booking problem. Share OTP for refund via {phone}.",
    "Your email account password expired. Call {phone} for technical support immediately.",
]

# --- Social Media / Romance Scam ---
SOCIAL_SCAM = [
    "Congratulations! You won Rs.{amount} in {company} lucky draw. Claim at: {url}",
    "You are selected for {company} free iPhone giveaway! First 100 winners. Register: {url}",
    "Share this message and win Rs.{amount} cash prize from {company}. Click: {url}",
    "Your Instagram account has Rs.{amount} in ad revenue. Claim via: {url}",
    "You've won a {company} gift voucher worth Rs.{amount}. Redeem at: {url}. Valid today only!",
    "Investment opportunity: Foreign friend needs your bank account. Transfer Rs.{amount} for 50% share.",
    "You have been gifted Rs.{amount} by an anonymous donor. Accept via: {url}. Expires today.",
    "Lottery winner: Your phone number selected in {company} draw. Claim Rs.{amount}: {url}",
]

# --- QR Scam ---
QR_SCAM = [
    "Scan this QR code to RECEIVE payment Rs.{amount}. You must enter your UPI PIN to accept.",
    "QR code attached for your payment collection of Rs.{amount}. Scan & confirm with PIN.",
    "Your winnings of Rs.{amount} attached as QR. Scan to receive in your UPI wallet.",
    "Merchant refund: Rs.{amount} refund QR enclosed. Scan to receive amount to your account.",
    "Reseller payment QR: Scan to collect Rs.{amount} advance. Enter PIN to confirm receipt.",
]

# --- SUSPICIOUS (borderline) ---
SUSPICIOUS_MSGS = [
    "Exclusive offer: {company} sale up to 80% off. Shop now: {url}. Limited time.",
    "Dear user, verify your account at {url} to continue using our services.",
    "Click here to claim your {company} reward points: {url}",
    "Your subscription will expire. Renew at: {url} to avoid service disruption.",
    "IMPORTANT: Please update your account information at {url} before {date}.",
    "Transaction alert: Rs.{amount} debited from your account. Not you? Click {url}",
    "{company} offers you a pre-approved personal loan of Rs.{amount}. Apply: {url}",
    "Reminder: Your KYC update is due. Please complete it at your earliest convenience.",
    "Last chance: Register for {company} loyalty program before offer expires: {url}",
    "Account activity notice: Recent login from new device. Verify if it was you: {url}",
    "Job application update: Your resume for {company} has been shortlisted. Respond: {url}",
    "Investment webinar: Learn high-return strategies from experts. Register free: {url}",
]

# --- SAFE / LEGITIMATE ---
SAFE_MSGS = [
    "Your OTP for {bank} NetBanking is {otp}. Valid for 5 minutes. Do NOT share this with anyone.",
    "{bank} Alert: Rs.{amount} debited from A/c **{acct} on {date}. Available bal: Rs.{balance}. Not you? Call 1800-XXX-XXXX.",
    "Your {bank} credit card payment of Rs.{amount} is due on {date}. Pay at netbanking.{bank}.com.",
    "Hi {name}, your order from Flipkart has been shipped. Delivery by {date}. Track: {url}",
    "Amazon: Your order #{order} will be delivered today by 8 PM. No action needed.",
    "Zomato: Your order is on the way. Arriving in 25 minutes. Track in the app.",
    "HDFC Bank: Your fixed deposit of Rs.{amount} has been renewed for 1 year at 7.1% p.a.",
    "Your Aadhaar-based e-KYC was successful at {company}. Welcome aboard.",
    "SBI: Your NEFT of Rs.{amount} to {name} (A/c **{acct}) was successful on {date}. Ref: {ref}",
    "Paytm: Payment of Rs.{amount} received from {name}. Your balance: Rs.{balance}.",
    "UPI: Rs.{amount} credited to your account from {company}. UTR: {ref}",
    "Your appointment at {company} is confirmed for {date}. No payment required.",
    "IRCTC: Ticket booking PNR {ref} confirmed for {date}. Total: Rs.{amount}.",
    "Your EPF withdrawal of Rs.{amount} has been processed. Credited in 3-5 days.",
    "{company}: Your subscription is active until {date}. No action required.",
    "Reminder: Your credit card bill of Rs.{amount} is due in 3 days. AutoPay is set.",
    "GST return for {date} has been filed successfully. ARN: {ref}.",
    "Your loan EMI of Rs.{amount} has been auto-debited. Next due: {date}.",
    "Security tip: {bank} will never ask for your OTP, PIN or card details over phone.",
    "Your mobile number is linked to Aadhaar. For queries call UIDAI at 1947.",
]

# --- Tamil Scam ---
TAMIL_SCAM = [
    "அவசரம்! உங்கள் {bank} கணக்கு இன்று block ஆகும். KYC புதுப்பிக்கவும்: {url}",
    "உங்கள் {bank} கணக்கு 24 மணி நேரத்தில் நிறுத்தப்படும். இப்போதே சரிபார்க்கவும்: {url}",
    "{bank} KYC தேவை. Aadhaar மற்றும் PAN அனுப்புங்கள். நேரம் முடிவடைகிறது: {url}",
    "வருமான வரி துறை: Rs.{amount} வரி பாக்கி உள்ளது. இப்போதே செலுத்துங்கள்: {url}",
]

# --- Tanglish Scam ---
TANGLISH_SCAM = [
    "Ungaloda {bank} account KYC update pannala na account block aagum. Immediate ah link click pannunga: {url}",
    "{bank} account suspend aagum. Ungal Aadhaar number share pannunga OTP kooda: {phone}",
    "Neenga Rs.{amount} win panneeringa! {company} lucky draw la. Claim pannanga: {url}. Today only!",
    "WFH job opportunity at {company}. Earn Rs.{salary}/month. No experience needed. Register pannunga: {url}",
    "Ungal {courier} parcel customs la irukku. Rs.{amount} pay pannunga release aaga: {url}",
    "UPI payment Rs.{amount} pending. QR scan pannunga pin enter pannunga receipt kku: {url}",
    "{bank} KYC expire aaguthu. Aadhaar, PAN submit pannunga suspend aagaama irukkanum: {url}",
]

# ── Filler pools ──────────────────────────────────────────────────────────────

BANKS = ["Example Bank", "Demo Bank", "Sample National Bank", "TestBank India"]
COMPANIES = ["Example Corp", "Demo Ltd", "Sample Pvt Ltd", "TestCo India"]
COURIERS = ["Example Courier", "Demo Logistics", "Sample Express", "TestParcel"]
URLS_SCAM = [
    "http://exmpl-bank-kyc.xyz/verify",
    "http://testbank-update.tk/login",
    "https://bit.ly/scam123",
    "http://192.168.1.99/verify",
    "http://demobank-kyc-update.com/secure",
    "http://exmpl-courier-pay.xyz/customs",
    "http://income-tax-refund.ml/claim",
    "http://upi-payment-receive.ga/accept",
    "https://tinyurl.com/fakejob99",
    "http://invest-profit-ai.cf/join",
]
URLS_LEGIT = [
    "https://www.examplebank.com/netbanking",
    "https://track.flipkart.com/order/12345",
    "https://irctc.co.in/booking/pnr",
    "https://www.incometax.gov.in/iec/foportal",
]
PHONES = ["9876543210", "8765432109", "7654321098", "9123456789"]
AMOUNTS = ["149", "499", "999", "1499", "2000", "5000", "47500", "10000", "500", "250"]
SALARIES = ["15000", "25000", "50000", "75000", "1000", "5000"]
OTPS = ["847291", "523174", "918374"]
ACCTS = ["1234", "5678", "9012"]
BALANCES = ["12,450", "8,320", "45,200"]
DATES = ["01/12/2026", "15/11/2026", "30/09/2026"]
NAMES = ["Rajesh", "Priya", "Amit", "Sunita"]
ORDERS = ["FLP-123456", "AMZ-987654"]
REFS = ["NEFT123456", "UPI987654", "GST456789"]
TRACKINGS = ["887123456IN", "DL98765432"]


def _fill(template: str) -> str:
    """Fill a template string with random placeholder values."""
    return (
        template
        .replace("{bank}", random.choice(BANKS))
        .replace("{company}", random.choice(COMPANIES))
        .replace("{courier}", random.choice(COURIERS))
        .replace("{url}", random.choice(URLS_SCAM))
        .replace("{phone}", random.choice(PHONES))
        .replace("{amount}", random.choice(AMOUNTS))
        .replace("{salary}", random.choice(SALARIES))
        .replace("{otp}", random.choice(OTPS))
        .replace("{acct}", random.choice(ACCTS))
        .replace("{balance}", random.choice(BALANCES))
        .replace("{date}", random.choice(DATES))
        .replace("{name}", random.choice(NAMES))
        .replace("{order}", random.choice(ORDERS))
        .replace("{ref}", random.choice(REFS))
        .replace("{tracking}", random.choice(TRACKINGS))
        .replace("{count}", str(random.randint(5, 47)))
    )


def _fill_safe(template: str) -> str:
    """Fill safe message templates — uses legit URLs."""
    return (
        template
        .replace("{bank}", random.choice(BANKS))
        .replace("{company}", random.choice(COMPANIES))
        .replace("{url}", random.choice(URLS_LEGIT))
        .replace("{amount}", random.choice(AMOUNTS))
        .replace("{otp}", random.choice(OTPS))
        .replace("{acct}", random.choice(ACCTS))
        .replace("{balance}", random.choice(BALANCES))
        .replace("{date}", random.choice(DATES))
        .replace("{name}", random.choice(NAMES))
        .replace("{order}", random.choice(ORDERS))
        .replace("{ref}", random.choice(REFS))
    )


# ── Category metadata ─────────────────────────────────────────────────────────

def _make_rows(
    templates: list[str],
    label: int,
    category: str,
    fill_fn=_fill,
    repeats: int = 3,
) -> list[dict]:
    rows = []
    for tmpl in templates:
        for _ in range(repeats):
            rows.append({
                "text": fill_fn(tmpl),
                "label": label,
                "category": category,
            })
    return rows


# ── Main generation ───────────────────────────────────────────────────────────

def generate() -> list[dict]:
    rows: list[dict] = []

    rows += _make_rows(BANKING_KYC_SCAM, SCAM, "Banking/KYC Scam", repeats=4)
    rows += _make_rows(UPI_PAYMENT_SCAM, SCAM, "UPI/Payment Scam", repeats=4)
    rows += _make_rows(JOB_SCAM, SCAM, "Job/Recruitment Scam", repeats=4)
    rows += _make_rows(INVESTMENT_SCAM, SCAM, "Investment Scam", repeats=4)
    rows += _make_rows(DELIVERY_SCAM, SCAM, "Delivery/Courier Scam", repeats=4)
    rows += _make_rows(GOVT_SCAM, SCAM, "Government Impersonation", repeats=4)
    rows += _make_rows(SUPPORT_SCAM, SCAM, "Customer Support Scam", repeats=3)
    rows += _make_rows(SOCIAL_SCAM, SCAM, "Social Media Scam", repeats=3)
    rows += _make_rows(QR_SCAM, SCAM, "QR Scam", repeats=5)
    rows += _make_rows(TAMIL_SCAM, SCAM, "Banking/KYC Scam", fill_fn=_fill, repeats=5)
    rows += _make_rows(TANGLISH_SCAM, SCAM, "Banking/KYC Scam", fill_fn=_fill, repeats=5)

    rows += _make_rows(SUSPICIOUS_MSGS, SUSPICIOUS, "Suspicious Activity", repeats=4)

    rows += _make_rows(SAFE_MSGS, SAFE, "Legitimate", fill_fn=_fill_safe, repeats=5)

    random.shuffle(rows)
    return rows


def main():
    rows = generate()
    print(f"Generated {len(rows)} samples")

    label_counts = {0: 0, 1: 0, 2: 0}
    for r in rows:
        label_counts[r["label"]] += 1
    print(f"  SAFE={label_counts[0]}  SUSPICIOUS={label_counts[1]}  SCAM={label_counts[2]}")

    fieldnames = ["text", "label", "category"]
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Dataset saved to: {OUTPUT_FILE}")
    return OUTPUT_FILE


if __name__ == "__main__":
    main()
