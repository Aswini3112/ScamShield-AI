import React, { useState } from 'react'
import { motion } from 'framer-motion'
import {
  Shield,
  AlertTriangle,
  Link2,
  QrCode,
  Briefcase,
  CreditCard,
  Users,
  LifeBuoy,
  ChevronDown,
  CheckCircle2,
} from 'lucide-react'
import { Card } from '@/components/ui/Card'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/Button'

const articles = [
  {
    id: 'phishing',
    icon: Link2,
    color: '#00D4FF',
    title: 'How Phishing Works',
    summary: 'Attackers impersonate trusted organisations to steal credentials.',
    content: `Phishing is a social engineering attack where criminals send fraudulent messages that appear to come from reputable sources — banks, government agencies, courier companies, or tech giants.

The goal is to trick you into clicking a malicious link, entering your login credentials, or sharing sensitive information.

How to spot it:
• The sender's email/number looks slightly off (exmplbank.com instead of examplebank.com)
• The message creates urgency: "Your account will be blocked in 2 hours"
• The link doesn't match the claimed organisation's official domain
• You're asked to "verify" information you never initiated
• Poor grammar and generic greetings ("Dear Customer")

What to do: Never click links in unsolicited messages. Go directly to the official website by typing it yourself.`,
  },
  {
    id: 'job',
    icon: Briefcase,
    color: '#8B5CF6',
    title: 'How Job Scams Work',
    summary: 'Fake recruiters offer lucrative remote jobs to extract money or data.',
    content: `Job scams target people looking for work, especially high-paying remote positions.

Typical patterns:
• "No experience required — earn ₹50,000/month from home"
• Contact via WhatsApp or Telegram, not official HR channels
• Request for Aadhaar/PAN upfront
• Ask for a "registration fee", "training fee", or "security deposit"
• Promise unrealistic salaries for simple tasks

Red flags:
• No official company email — only WhatsApp or personal Gmail
• Job description is vague ("data entry", "product reviewing")
• You're asked to pay money before starting work — legitimate employers never do this
• No verifiable company address or registration

Always verify the company independently. Search for it on MCA21, LinkedIn, or official websites.`,
  },
  {
    id: 'upi',
    icon: CreditCard,
    color: '#F59E0B',
    title: 'How UPI / Payment Scams Work',
    summary: 'Attackers trick victims into entering their UPI PIN to "receive" money.',
    content: `UPI scams exploit a critical misunderstanding: you never need to enter your PIN to RECEIVE money — only to SEND it.

Common UPI scam patterns:
• "I want to buy your item. Scan this QR to receive payment."
• "I've sent you ₹1,000 by mistake. Enter PIN to confirm receipt."
• Fake payment screenshots showing money transferred
• Asking you to "accept" payment through a collect request

How the scam works:
1. Attacker sends a "collect request" or a fake QR
2. Victim thinks they're receiving money
3. Victim enters their UPI PIN
4. Money is actually SENT from victim's account

Golden rule: You NEVER need your UPI PIN to receive money. If someone asks for it, it's a scam.`,
  },
  {
    id: 'qr',
    icon: QrCode,
    color: '#22C55E',
    title: 'How QR Code Scams Work',
    summary: 'Malicious QR codes redirect victims to phishing sites or trigger payments.',
    content: `QR codes are convenient but invisible — you can't tell where they lead without scanning them.

QR scam methods:
• Fake QR codes stuck over legitimate ones (parking meters, restaurant menus)
• QR codes sent via WhatsApp/email that lead to phishing pages
• "Scan to receive prize money" — actually a payment request
• QR codes in job offer documents linking to credential-stealing sites

How to stay safe:
• Preview the URL after scanning before tapping "Open"
• Never scan QR codes from unsolicited messages
• Physical QR codes in public places may have been tampered — look for stickers placed on top
• Use a QR scanner app that shows the destination URL before opening it

If you scan a suspicious QR code, do not proceed if the URL looks unfamiliar.`,
  },
  {
    id: 'kyc',
    icon: Shield,
    color: '#EF4444',
    title: 'How Fake KYC Scams Work',
    summary: 'Fraudsters impersonate banks or telecom operators to steal identity documents.',
    content: `KYC (Know Your Customer) scams exploit mandatory verification processes that real banks and operators do perform — making them easy to fake.

How it typically works:
1. You receive an SMS/call claiming your account/SIM will be blocked if KYC isn't updated
2. You're directed to a fake website or asked to video-call a "KYC officer"
3. You're asked to show/submit Aadhaar, PAN, or bank details
4. The attacker now has enough to commit identity fraud

Legitimate KYC never requires:
• OTP sharing over phone/chat
• Sending document photos via WhatsApp
• Clicking a link sent in an SMS
• Paying any "KYC fee"

What to do: Call the official customer care number (found on the back of your card or official website) to verify any KYC request.`,
  },
  {
    id: 'social_engineering',
    icon: Users,
    color: '#3B82F6',
    title: 'How Social Engineering Works',
    summary: 'Psychological manipulation techniques used in all scam types.',
    content: `Social engineering is the art of manipulating people into giving up confidential information or taking harmful actions.

Key psychological techniques scammers use:

URGENCY: "Act in the next 2 hours or your account is blocked." Creates panic and bypasses rational thinking.

FEAR: "You have an arrest warrant" or "Your account has been compromised." Triggers fight-or-flight response.

AUTHORITY: Impersonating police, banks, income tax, RBI, or government officials. We're conditioned to comply with authority.

SCARCITY: "Only 3 slots remaining for this offer." Fear of missing out drives hasty decisions.

RECIPROCITY: "We're giving you ₹500 free — just verify your account." Small gifts create obligation.

TRUST EXPLOITATION: Using logos, official-looking messages, or real employee names to appear legitimate.

Defence: When you feel urgency, fear, or excitement — slow down. That emotional reaction is exactly what scammers are engineering.`,
  },
  {
    id: 'urls',
    icon: Link2,
    color: '#F97316',
    title: 'How to Identify Suspicious URLs',
    summary: 'Learn to read URLs and spot the signs of a fake website.',
    content: `URLs are the most reliable indicator of a fake website — if you know how to read them.

Anatomy of a URL: https://subdomain.domain.tld/path?query

Red flags to look for:
• Domain mismatch: "sbi-online-banking.xyz" is NOT sbi.co.in
• Hyphens in domain: "state-bank-of-india-kyc.com" — real sites rarely have hyphens
• Extra words: "hdfc-bank-kyc-update.com" instead of "hdfcbank.com"
• Suspicious TLDs: .xyz, .tk, .ml, .ga are cheap/free and commonly used for fraud
• IP address instead of domain: http://192.168.1.1/login
• URL shorteners: bit.ly, tinyurl — hide the real destination
• Excessive path depth: legitimate banking sites are rarely at /verify/kyc/update/confirm/
• HTTP instead of HTTPS for sensitive operations

Before clicking any link: Hover over it (desktop) or long-press (mobile) to see the actual URL. Better yet — type the official URL yourself.`,
  },
  {
    id: 'after_click',
    icon: LifeBuoy,
    color: '#EC4899',
    title: 'What to Do After Clicking a Suspicious Link',
    summary: 'Immediate steps to take if you suspect you\'ve been compromised.',
    content: `If you've already clicked a suspicious link, act quickly. The sooner you respond, the better.

IMMEDIATE steps (within minutes):

1. Do NOT enter any information on the page — close it immediately
2. Disconnect from Wi-Fi/mobile data briefly if you suspect malware download
3. Run a malware scan if you're on a PC
4. Change passwords for any accounts you may have accessed

If you entered credentials:
• Change your password immediately on the REAL website (type the URL yourself)
• Enable two-factor authentication
• Check recent login activity and active sessions
• Contact the service's official support

If you shared an OTP:
• Call your bank's official helpline (number on card back) immediately
• Request a temporary account freeze if money is at risk

If you transferred money:
• File a complaint at cybercrime.gov.in immediately
• Call the national cybercrime helpline: 1930
• Inform your bank immediately — quick action can reverse transactions

Remember: Use cybercrime.gov.in or call 1930 for official assistance in India.`,
  },
]

function ArticleCard({ article, index }: { article: typeof articles[0]; index: number }) {
  const [expanded, setExpanded] = useState(false)
  const Icon = article.icon

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.05 }}
    >
      <Card className="cursor-pointer hover:border-cyber-cyan/20 transition-all duration-300">
        <button
          onClick={() => setExpanded(!expanded)}
          className="w-full text-left"
        >
          <div className="flex items-start gap-4">
            <div
              className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0"
              style={{
                backgroundColor: `${article.color}15`,
                border: `1px solid ${article.color}30`,
              }}
            >
              <Icon className="h-5 w-5" style={{ color: article.color }} />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between gap-2">
                <h3 className="font-semibold text-white">{article.title}</h3>
                <ChevronDown
                  className={`h-4 w-4 text-slate-600 flex-shrink-0 transition-transform duration-300 ${
                    expanded ? 'rotate-180' : ''
                  }`}
                />
              </div>
              <p className="text-sm text-slate-500 mt-0.5">{article.summary}</p>
            </div>
          </div>
        </button>

        {expanded && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mt-4 pt-4 border-t border-base-border"
          >
            <div className="prose-invert text-sm text-slate-300 leading-relaxed whitespace-pre-line">
              {article.content}
            </div>
          </motion.div>
        )}
      </Card>
    </motion.div>
  )
}

export function LearnPage() {
  return (
    <div className="min-h-screen pt-20 pb-16">
      <div className="max-w-3xl mx-auto px-4 space-y-6">
        {/* Header */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <div className="text-center">
            <h1 className="text-4xl font-bold text-white mb-3">
              Cybersecurity Awareness
            </h1>
            <p className="text-slate-400 max-w-xl mx-auto">
              Understanding how scams work is your best defense. Learn the tactics, spot the
              signs, and know what to do.
            </p>
          </div>
        </motion.div>

        {/* Quick tips */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass-card rounded-xl p-5 border border-cyber-cyan/20"
        >
          <div className="flex items-center gap-2 mb-4">
            <Shield className="h-5 w-5 text-cyber-cyan" />
            <h3 className="font-semibold text-white">Quick Safety Reminders</h3>
          </div>
          <div className="grid sm:grid-cols-2 gap-3">
            {[
              'You never need to enter your UPI PIN to receive money',
              'Legitimate banks never ask for OTP or password over phone',
              'Check the full URL before entering credentials anywhere',
              'No government agency will threaten you into paying immediately',
              'No legitimate job asks you to pay before starting work',
              'Scan QR codes only from trusted, verified sources',
            ].map((tip, i) => (
              <div key={i} className="flex items-start gap-2">
                <CheckCircle2 className="h-4 w-4 text-risk-low flex-shrink-0 mt-0.5" />
                <span className="text-sm text-slate-300">{tip}</span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Articles */}
        <div className="space-y-4">
          {articles.map((article, i) => (
            <ArticleCard key={article.id} article={article} index={i} />
          ))}
        </div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="text-center py-8"
        >
          <AlertTriangle className="h-10 w-10 text-risk-medium mx-auto mb-4" />
          <h3 className="text-xl font-bold text-white mb-2">
            Think something looks suspicious?
          </h3>
          <p className="text-slate-500 text-sm mb-5">
            Don't guess. Analyze it with ScamShield.
          </p>
          <Link to="/analyze">
            <Button size="lg">Analyze Now</Button>
          </Link>
        </motion.div>
      </div>
    </div>
  )
}
