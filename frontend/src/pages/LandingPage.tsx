import React from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  Shield,
  Zap,
  Eye,
  Link2,
  QrCode,
  FileText,
  Image,
  ArrowRight,
  ChevronRight,
  AlertTriangle,
  Activity,
  Lock,
} from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'

const fadeUp = {
  initial: { opacity: 0, y: 30 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.6, ease: 'easeOut' },
}

const stagger = {
  animate: { transition: { staggerChildren: 0.1 } },
}

function HeroThreatCard() {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9, y: 20 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ delay: 0.4, duration: 0.8 }}
      className="animate-float"
    >
      <div className="glass-card rounded-2xl p-5 w-72 shadow-cyber border border-cyber-cyan/20">
        <div className="flex items-center justify-between mb-4">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Threat Analysis
          </span>
          <span className="live-dot w-2 h-2 rounded-full bg-risk-critical" />
        </div>

        {/* Risk score */}
        <div className="text-center py-3 mb-4 rounded-xl bg-risk-critical-bg border border-risk-critical/20">
          <div className="text-4xl font-bold text-risk-critical">92</div>
          <div className="text-xs text-risk-critical/80 font-medium tracking-widest uppercase mt-1">
            Critical Risk
          </div>
        </div>

        {/* Category */}
        <div className="text-xs text-slate-500 mb-1">Category</div>
        <div className="text-sm font-semibold text-white mb-4">Banking / KYC Scam</div>

        {/* Indicators */}
        <div className="space-y-2">
          {['Urgency Detected', 'Impersonation', 'Suspicious URL', 'Credential Harvesting'].map(
            (ind) => (
              <div key={ind} className="flex items-center gap-2">
                <AlertTriangle className="h-3.5 w-3.5 text-risk-critical flex-shrink-0" />
                <span className="text-xs text-slate-300">{ind}</span>
              </div>
            )
          )}
        </div>

        {/* Pipeline viz */}
        <div className="mt-4 pt-4 border-t border-base-border">
          <div className="flex items-center justify-between text-xs">
            {['Input', 'Detect', 'Analyze', 'Report'].map((s, i) => (
              <React.Fragment key={s}>
                <span className="text-cyber-cyan font-medium">{s}</span>
                {i < 3 && <ChevronRight className="h-3 w-3 text-slate-600" />}
              </React.Fragment>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  )
}

const capabilities = [
  {
    icon: FileText,
    label: 'Text',
    desc: 'SMS, email, WhatsApp',
    color: '#00D4FF',
  },
  {
    icon: Image,
    label: 'Screenshot',
    desc: 'OCR + visual analysis',
    color: '#8B5CF6',
  },
  {
    icon: Link2,
    label: 'URL',
    desc: 'Safe static analysis',
    color: '#3B82F6',
  },
  {
    icon: QrCode,
    label: 'QR Code',
    desc: 'Decode & investigate',
    color: '#F59E0B',
  },
  {
    icon: FileText,
    label: 'Document',
    desc: 'PDF & text extraction',
    color: '#22C55E',
  },
]

const pipeline = [
  { label: 'Input', icon: Eye },
  { label: 'Evidence Analysis', icon: Activity },
  { label: 'Threat Detection', icon: AlertTriangle },
  { label: 'Attack Chain', icon: Link2 },
  { label: 'Risk Assessment', icon: Shield },
]

const differentiators = [
  {
    icon: Eye,
    title: 'Multimodal Evidence Analysis',
    desc: 'Text, images, URLs, QR codes, and documents analyzed together for a complete threat picture.',
  },
  {
    icon: Link2,
    title: 'Attack Chain Reconstruction',
    desc: 'See exactly how a scammer is building up to steal your data or money, step by step.',
  },
  {
    icon: Activity,
    title: 'Social Engineering Detection',
    desc: 'Identifies urgency, fear, authority impersonation, and credential harvesting techniques.',
  },
  {
    icon: Lock,
    title: 'Recovery Guidance',
    desc: 'Already interacted? Get immediate, actionable guidance to limit the damage.',
  },
  {
    icon: Zap,
    title: 'Explainable AI',
    desc: 'Every risk decision is explained — not just a score, but the reasoning behind it.',
  },
  {
    icon: Shield,
    title: 'India-Focused Categories',
    desc: 'UPI scams, KYC fraud, fake job offers, investment scams — built for Indian users.',
  },
]

export function LandingPage() {
  return (
    <div className="relative overflow-hidden">
      {/* Hero glow */}
      <div className="absolute inset-0 bg-hero-glow pointer-events-none" />

      {/* ── HERO ─────────────────────────────────────────────────────────── */}
      <section className="relative min-h-screen flex items-center pt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          <div className="grid lg:grid-cols-2 gap-12 items-center py-20">
            {/* Left: copy */}
            <motion.div
              variants={stagger}
              initial="initial"
              animate="animate"
              className="space-y-8"
            >
              <motion.div variants={fadeUp}>
                <Badge className="mb-4 text-xs py-1 px-3">
                  <span className="live-dot w-1.5 h-1.5 rounded-full bg-cyber-cyan mr-2" />
                  AI-Powered Scam Investigation Platform
                </Badge>
                <h1 className="text-5xl lg:text-6xl font-bold text-white leading-tight">
                  Don't Just{' '}
                  <span className="text-cyber-cyan glow-cyan">Detect</span>
                  <br />
                  the Scam.
                </h1>
                <h2 className="text-4xl lg:text-5xl font-bold text-slate-300 leading-tight mt-2">
                  Understand the{' '}
                  <span className="text-cyber-violet">Attack.</span>
                </h2>
              </motion.div>

              <motion.p
                variants={fadeUp}
                className="text-lg text-slate-400 max-w-lg leading-relaxed"
              >
                Analyze suspicious messages, screenshots, URLs and QR codes with AI-powered
                threat intelligence and explainable risk analysis.
              </motion.p>

              <motion.div variants={fadeUp} className="flex flex-wrap gap-3">
                <Link to="/analyze">
                  <Button size="lg" className="gap-2 shadow-cyber-strong">
                    <Zap className="h-5 w-5" />
                    Analyze a Scam
                  </Button>
                </Link>
                <Link to="/analyze">
                  <Button variant="outline" size="lg" className="gap-2">
                    Try Demo
                    <ArrowRight className="h-4 w-4" />
                  </Button>
                </Link>
              </motion.div>

              {/* Stats */}
              <motion.div
                variants={fadeUp}
                className="flex flex-wrap gap-6 pt-4 border-t border-base-border"
              >
                {[
                  { value: '12+', label: 'Scam Categories' },
                  { value: '8+', label: 'Attack Techniques' },
                  { value: '5', label: 'Input Modalities' },
                ].map((stat) => (
                  <div key={stat.label}>
                    <div className="text-2xl font-bold text-cyber-cyan">{stat.value}</div>
                    <div className="text-xs text-slate-500">{stat.label}</div>
                  </div>
                ))}
              </motion.div>
            </motion.div>

            {/* Right: threat card */}
            <div className="flex justify-center lg:justify-end">
              <HeroThreatCard />
            </div>
          </div>
        </div>
      </section>

      {/* ── PIPELINE ─────────────────────────────────────────────────────── */}
      <section className="py-16 border-t border-base-border bg-base-card/30">
        <div className="max-w-5xl mx-auto px-4">
          <div className="text-center mb-10">
            <h3 className="text-xl font-bold text-white">Analysis Pipeline</h3>
            <p className="text-sm text-slate-500 mt-2">
              Detect → Investigate → Explain → Protect
            </p>
          </div>
          <div className="flex flex-wrap items-center justify-center gap-2">
            {pipeline.map((step, i) => (
              <React.Fragment key={step.label}>
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.1 }}
                  className="flex items-center gap-2 px-4 py-2.5 rounded-xl glass-card border border-base-border"
                >
                  <step.icon className="h-4 w-4 text-cyber-cyan" />
                  <span className="text-sm font-medium text-white">{step.label}</span>
                </motion.div>
                {i < pipeline.length - 1 && (
                  <ChevronRight className="h-5 w-5 text-slate-700 flex-shrink-0" />
                )}
              </React.Fragment>
            ))}
          </div>
        </div>
      </section>

      {/* ── CAPABILITIES ─────────────────────────────────────────────────── */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl font-bold text-white">Multimodal Protection</h2>
            <p className="text-slate-400 mt-3 max-w-xl mx-auto">
              Paste, upload, or describe anything suspicious. ScamShield investigates every
              modality with the same depth of analysis.
            </p>
          </motion.div>

          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            {capabilities.map((cap, i) => (
              <motion.div
                key={cap.label}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.08 }}
                whileHover={{ y: -4, transition: { duration: 0.2 } }}
              >
                <Link to="/analyze">
                  <Card className="text-center cursor-pointer hover:border-cyber-cyan/30 transition-all duration-300 group">
                    <div
                      className="w-10 h-10 rounded-xl flex items-center justify-center mx-auto mb-3"
                      style={{ backgroundColor: `${cap.color}15`, border: `1px solid ${cap.color}30` }}
                    >
                      <cap.icon className="h-5 w-5" style={{ color: cap.color }} />
                    </div>
                    <div className="font-semibold text-white text-sm group-hover:text-cyber-cyan transition-colors">
                      {cap.label}
                    </div>
                    <div className="text-xs text-slate-500 mt-1">{cap.desc}</div>
                  </Card>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ── DIFFERENTIATORS ──────────────────────────────────────────────── */}
      <section className="py-20 bg-base-card/20 border-t border-base-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl font-bold text-white">
              Beyond Detection — We Explain It
            </h2>
            <p className="text-slate-400 mt-3 max-w-xl mx-auto">
              Existing tools detect suspicious content. ScamShield goes further — it tells you
              why it's dangerous and what to do about it.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
            {differentiators.map((d, i) => (
              <motion.div
                key={d.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.08 }}
              >
                <Card className="h-full hover:border-cyber-cyan/20 transition-all duration-300">
                  <div className="w-9 h-9 rounded-lg bg-cyber-cyan/10 border border-cyber-cyan/20 flex items-center justify-center mb-3">
                    <d.icon className="h-4.5 w-4.5 text-cyber-cyan h-4 w-4" />
                  </div>
                  <h3 className="font-semibold text-white mb-2">{d.title}</h3>
                  <p className="text-sm text-slate-400 leading-relaxed">{d.desc}</p>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ──────────────────────────────────────────────────────────── */}
      <section className="py-24 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="max-w-2xl mx-auto px-4"
        >
          <Shield className="h-12 w-12 text-cyber-cyan mx-auto mb-6 drop-shadow-[0_0_16px_rgba(0,212,255,0.5)]" />
          <h2 className="text-3xl font-bold text-white mb-4">
            Received something suspicious?
          </h2>
          <p className="text-slate-400 mb-8">
            Don't click, don't share, don't pay. Analyze it first.
          </p>
          <Link to="/analyze">
            <Button size="lg" className="gap-2 shadow-cyber-strong">
              <Zap className="h-5 w-5" />
              Analyze Now — It's Free
            </Button>
          </Link>
          <p className="text-xs text-slate-600 mt-4">
            Prototype · AI assessment is an aid, not definitive proof · Always verify through official channels
          </p>
        </motion.div>
      </section>
    </div>
  )
}
