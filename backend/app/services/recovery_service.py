"""Recovery guidance service — returns step-by-step guidance based on interaction type."""
from __future__ import annotations

from app.schemas.analysis import RecoveryGuidance, RecoveryStep, RecoveryHotline

_HOTLINES = [
    RecoveryHotline(name="National Cyber Crime Helpline", number="1930"),
    RecoveryHotline(name="Cyber Crime Portal", number="cybercrime.gov.in"),
]

_BANK_HOTLINES = [
    RecoveryHotline(name="National Cyber Crime Helpline", number="1930"),
    RecoveryHotline(name="Cyber Crime Portal", number="cybercrime.gov.in"),
    RecoveryHotline(name="RBI Sachet Portal", number="sachet.rbi.org.in"),
]

_GUIDANCE: dict[str, RecoveryGuidance] = {
    "only_received": RecoveryGuidance(
        interaction_type="only_received",
        severity="low",
        headline="You're safe — you only received the message.",
        steps=[
            RecoveryStep(
                priority="soon",
                title="Delete the message",
                description="Delete the suspicious SMS, email, or WhatsApp message to reduce the risk of accidentally clicking on it later.",
            ),
            RecoveryStep(
                priority="soon",
                title="Block the sender",
                description="Block the number or email address to prevent further contact.",
            ),
            RecoveryStep(
                priority="monitor",
                title="Warn others",
                description="If you received a scam targeting a specific organisation, consider reporting it to that organisation's official fraud team.",
            ),
        ],
    ),
    "clicked_link": RecoveryGuidance(
        interaction_type="clicked_link",
        severity="medium",
        headline="You clicked the link — act now to stay safe.",
        steps=[
            RecoveryStep(
                priority="immediate",
                title="Close the page immediately",
                description="If the page is still open, close it without entering any information.",
                action="Close the browser tab/app now.",
            ),
            RecoveryStep(
                priority="immediate",
                title="Check if anything was downloaded",
                description="Some malicious pages automatically download files. Check your Downloads folder and delete anything unfamiliar.",
            ),
            RecoveryStep(
                priority="soon",
                title="Run a malware scan",
                description="Use trusted security software to scan your device for malware, especially if on a PC.",
            ),
            RecoveryStep(
                priority="soon",
                title="Change passwords for sensitive accounts",
                description="Change passwords for your bank, email, and social media accounts as a precaution.",
            ),
            RecoveryStep(
                priority="monitor",
                title="Monitor your accounts",
                description="Watch your bank accounts and email for unusual activity over the next few days.",
            ),
        ],
    ),
    "entered_credentials": RecoveryGuidance(
        interaction_type="entered_credentials",
        severity="high",
        headline="Act immediately — your credentials may be compromised.",
        steps=[
            RecoveryStep(
                priority="immediate",
                title="Change your password RIGHT NOW",
                description="Go directly to the REAL website (type the URL yourself) and change your password immediately.",
                action="Type the official website URL directly in your browser.",
            ),
            RecoveryStep(
                priority="immediate",
                title="Enable two-factor authentication",
                description="Enable 2FA on the account to prevent access even if the password is known.",
            ),
            RecoveryStep(
                priority="immediate",
                title="Check active sessions",
                description="Most banks and email providers allow you to see active login sessions. Revoke any you don't recognise.",
            ),
            RecoveryStep(
                priority="soon",
                title="Check for suspicious activity",
                description="Review recent transactions, sent emails, and account changes for anything you didn't do.",
            ),
            RecoveryStep(
                priority="soon",
                title="Contact the organisation directly",
                description="If the account is a bank, call the official helpline on the back of your card and report a possible compromise.",
            ),
            RecoveryStep(
                priority="monitor",
                title="Report to cyber crime",
                description="File a report at cybercrime.gov.in or call 1930.",
            ),
        ],
        hotlines=_HOTLINES,
    ),
    "shared_otp": RecoveryGuidance(
        interaction_type="shared_otp",
        severity="high",
        headline="OTP shared — contact your bank immediately.",
        steps=[
            RecoveryStep(
                priority="immediate",
                title="Call your bank's fraud helpline NOW",
                description="Call the number on the back of your bank card or on the official website. Ask them to review recent transactions and temporarily freeze your account if necessary.",
                action="Call your bank's official fraud helpline immediately.",
            ),
            RecoveryStep(
                priority="immediate",
                title="Block your UPI if applicable",
                description="If UPI was involved, call your bank or use the app to temporarily disable UPI transactions.",
            ),
            RecoveryStep(
                priority="immediate",
                title="Change your mobile banking PIN/password",
                description="Immediately change your internet banking password and UPI PIN.",
            ),
            RecoveryStep(
                priority="soon",
                title="Review recent transactions",
                description="Check your account for any unauthorised transactions. Report them to your bank immediately.",
            ),
            RecoveryStep(
                priority="soon",
                title="File a cyber crime complaint",
                description="Register a complaint at cybercrime.gov.in or call 1930. Quick action may help recover funds.",
                action="Visit cybercrime.gov.in",
            ),
        ],
        hotlines=_BANK_HOTLINES,
    ),
    "transferred_money": RecoveryGuidance(
        interaction_type="transferred_money",
        severity="critical",
        headline="Money transferred — act within the next 30 minutes for best recovery chance.",
        steps=[
            RecoveryStep(
                priority="immediate",
                title="Call 1930 (National Cyber Crime Helpline) NOW",
                description="Call 1930 immediately. Banks can sometimes freeze recipient accounts if a complaint is filed quickly (within 1-2 hours).",
                action="Call 1930 right now.",
            ),
            RecoveryStep(
                priority="immediate",
                title="Call your bank's fraud helpline",
                description="Simultaneously inform your bank. Ask them to put a hold on the transaction and investigate.",
                action="Call your bank's fraud/dispute helpline.",
            ),
            RecoveryStep(
                priority="immediate",
                title="File a complaint on cybercrime.gov.in",
                description="Register an online complaint at cybercrime.gov.in with all transaction details (amount, UTR number, time, recipient UPI/account).",
                action="Go to cybercrime.gov.in",
            ),
            RecoveryStep(
                priority="soon",
                title="Visit your nearest police station",
                description="File an FIR at your nearest police station. Mention cyber fraud (IPC Section 420, IT Act Section 66C/D).",
            ),
            RecoveryStep(
                priority="soon",
                title="Collect all evidence",
                description="Take screenshots of all messages, payment confirmations, and any contact from the scammer. Do not delete anything.",
            ),
            RecoveryStep(
                priority="monitor",
                title="Follow up with the bank and police",
                description="Recovery depends on the speed of action. Follow up regularly with your bank's fraud team and the cybercrime cell.",
            ),
        ],
        hotlines=_BANK_HOTLINES,
    ),
    "downloaded_file": RecoveryGuidance(
        interaction_type="downloaded_file",
        severity="high",
        headline="File downloaded — your device may be compromised.",
        steps=[
            RecoveryStep(
                priority="immediate",
                title="Do NOT open or run the file",
                description="If you haven't opened the file, do not do so. Move it to trash immediately.",
            ),
            RecoveryStep(
                priority="immediate",
                title="Run a full antivirus/malware scan",
                description="Use a trusted security tool (Windows Defender, Malwarebytes, etc.) to run a full scan of your device.",
                action="Run a full device scan now.",
            ),
            RecoveryStep(
                priority="immediate",
                title="Disconnect from the internet temporarily",
                description="If you have already opened the file, briefly disconnect from Wi-Fi/mobile data to limit any potential data exfiltration.",
            ),
            RecoveryStep(
                priority="soon",
                title="Change all important passwords from another device",
                description="If malware may have been installed, change your banking, email, and social media passwords from a clean device.",
            ),
            RecoveryStep(
                priority="soon",
                title="Check for unauthorised account access",
                description="Review your bank account, email sent folder, and social media for any activity you don't recognise.",
            ),
            RecoveryStep(
                priority="monitor",
                title="Consider a device factory reset if malware is confirmed",
                description="If malware is confirmed by antivirus, a factory reset may be the safest option for mobile devices.",
            ),
        ],
        hotlines=_HOTLINES,
    ),
    "not_sure": RecoveryGuidance(
        interaction_type="not_sure",
        severity="medium",
        headline="When unsure, take precautionary steps.",
        steps=[
            RecoveryStep(
                priority="immediate",
                title="Stop any ongoing interaction",
                description="If you are in a call, on a website, or in a chat — stop immediately.",
            ),
            RecoveryStep(
                priority="soon",
                title="Change passwords for sensitive accounts",
                description="Change passwords for your bank, email, and UPI apps as a precaution.",
            ),
            RecoveryStep(
                priority="soon",
                title="Check your accounts for unusual activity",
                description="Review recent bank transactions, email sent folder, and active login sessions.",
            ),
            RecoveryStep(
                priority="soon",
                title="Run a malware scan",
                description="If you may have downloaded something, run a full device scan.",
            ),
            RecoveryStep(
                priority="monitor",
                title="Contact your bank if you suspect financial risk",
                description="If your banking credentials or UPI may have been compromised, call your bank's fraud helpline.",
            ),
        ],
        hotlines=_HOTLINES,
    ),
}


def get_recovery_guidance(interaction_type: str) -> RecoveryGuidance:
    return _GUIDANCE.get(interaction_type, _GUIDANCE["not_sure"])
