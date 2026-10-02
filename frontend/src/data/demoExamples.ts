import type { DemoExample } from '@/types'

export const demoExamples: DemoExample[] = [
  {
    id: 'banking_kyc',
    label: 'Banking / KYC',
    type: 'text',
    language: 'English',
    description: 'Fake bank KYC update threat',
    content:
      'URGENT: Your Example Bank account will be BLOCKED today. Your KYC verification is incomplete. Click immediately to update: http://exmpl-bank-kyc-update.xyz/verify?id=98712 Failure to comply within 2 hours will result in permanent account suspension. Call us at 1800-FAKE-123.',
  },
  {
    id: 'job_scam',
    label: 'Job Scam',
    type: 'text',
    language: 'English',
    description: 'Fake high-paying job offer',
    content:
      'Congratulations! You have been selected for a Work From Home job at Example Global Corp. Earn Rs.50,000/month. No experience needed. Send your Aadhaar card, PAN card and Rs.999 registration fee to get your offer letter. Reply NOW - limited slots available! WhatsApp: 9876543210',
  },
  {
    id: 'upi_scam',
    label: 'UPI / Payment',
    type: 'text',
    language: 'English',
    description: 'Fake UPI payment request',
    content:
      "Hi, I saw your item on OLX. I want to buy it. I've sent Rs.500 advance via UPI to your number. Please scan this QR code to RECEIVE the money: [QR attached]. My bank says you need to enter your UPI PIN to accept the payment. Hurry, the transaction will expire in 5 minutes!",
  },
  {
    id: 'delivery_scam',
    label: 'Delivery Scam',
    type: 'text',
    language: 'English',
    description: 'Fake courier delivery fee scam',
    content:
      'Dear Customer, Your package from Example Courier is held at customs. Pay Rs.149 customs clearance fee to release your parcel. Failure to pay within 24 hours will result in return. Pay here: http://exmpl-courier-pay.xyz/customs Track: EC887123456IN',
  },
  {
    id: 'investment_scam',
    label: 'Investment Scam',
    type: 'text',
    language: 'English',
    description: 'Fake investment scheme',
    content:
      'EXCLUSIVE OFFER: Join our AI-powered trading platform and earn guaranteed 40% monthly returns! Our algorithm has 99% success rate. Invest as little as Rs.10,000 and double your money in 30 days. Limited slots. Register now: http://exmpl-ai-invest.xyz/join WhatsApp our expert: 9123456789',
  },
  {
    id: 'safe_message',
    label: 'Safe Message',
    type: 'text',
    language: 'English',
    description: 'Legitimate bank OTP message',
    content:
      'Your OTP for login to ExampleBank NetBanking is 847291. Valid for 5 minutes. Do NOT share this OTP with anyone including bank staff. ExampleBank never asks for your OTP. If you did not request this, please ignore.',
  },
  {
    id: 'tamil_scam',
    label: 'Tamil Scam',
    type: 'text',
    language: 'Tamil',
    description: 'Fake bank message in Tamil',
    content:
      'அவசரம்! உங்கள் Example Bank கணக்கு இன்று block ஆகும். உடனடியாக KYC புதுப்பிக்கவும். இணைப்பை கிளிக் செய்யுங்கள்: http://exmpl-bank-kyc.xyz/tamil உங்கள் Aadhaar மற்றும் PAN விவரங்களை சமர்ப்பிக்கவும்.',
  },
  {
    id: 'tanglish_scam',
    label: 'Tanglish Scam',
    type: 'text',
    language: 'Tanglish',
    description: 'Bank KYC scam in Tanglish',
    content:
      'Ungaloda Example Bank account KYC update pannala na account block aagum. Immediate ah indha link click pannunga: http://exmpl-kyc-verify.xyz/tn Ungal Aadhaar number, OTP share pannunga. 2 mani neram ullah pannala na permanent block aagum.',
  },
  {
    id: 'govt_impersonation',
    label: 'Govt Impersonation',
    type: 'text',
    language: 'English',
    description: 'Fake government notice',
    content:
      'NOTICE from Income Tax Department, Government of India. Our records show you owe Rs.47,500 in unpaid taxes. Failure to pay within 48 hours will result in ARREST WARRANT. Pay immediately at: http://incometax-gov-in.xyz/pay?case=IT882 For queries: 011-FAKE-1234',
  },
  {
    id: 'qr_scam',
    label: 'QR Scam',
    type: 'text',
    language: 'English',
    description: 'Fake QR code payment scam',
    content:
      "Hello, I'm the buyer for your product. I will pay via QR scan. Please scan this QR code I'm sending you to COLLECT payment. You will need to enter your UPI PIN to confirm receipt. The money is already in transit - just scan and confirm to receive Rs.8,500.",
  },
]

export const getDemoById = (id: string): DemoExample | undefined =>
  demoExamples.find((d) => d.id === id)
