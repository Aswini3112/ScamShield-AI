import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { X, ShieldAlert, CheckCircle2, AlertTriangle, Phone, ArrowRight, Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { submitRecovery } from '@/services/api'
import type { InteractionType, RecoveryGuidance, RecoveryStep } from '@/types'

const INTERACTION_OPTIONS: { value: InteractionType; label: string; icon: string }[] = [
  { value: 'only_received', label: 'I only received the message', icon: '📨' },
  { value: 'clicked_link', label: 'I clicked the link', icon: '🔗' },
  { value: 'entered_credentials', label: 'I entered my login/credentials', icon: '🔑' },
  { value: 'shared_otp', label: 'I shared an OTP', icon: '📲' },
  { value: 'transferred_money', label: 'I transferred money', icon: '💸' },
  { value: 'downloaded_file', label: 'I downloaded a file', icon: '📥' },
  { value: 'not_sure', label: "I'm not sure", icon: '❓' },
]

interface RecoveryModalProps {
  open: boolean
  onClose: () => void
  scanId: number | null
}

const priorityColor: Record<string, string> = {
  immediate: '#EF4444',
  soon: '#F59E0B',
  monitor: '#22C55E',
}
const priorityLabel: Record<string, string> = {
  immediate: 'Act Now',
  soon: 'Do Soon',
  monitor: 'Monitor',
}

export function RecoveryModal({ open, onClose, scanId }: RecoveryModalProps) {
  const [step, setStep] = useState<'select' | 'loading' | 'result'>('select')
  const [selected, setSelected] = useState<InteractionType | null>(null)
  const [guidance, setGuidance] = useState<RecoveryGuidance | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async () => {
    if (!selected) return
    setStep('loading')
    try {
      const res = await submitRecovery(scanId, selected)
      if (res.success) {
        setGuidance(res.data)
        setStep('result')
      } else throw new Error('Failed to get guidance')
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed')
      setStep('select')
    }
  }

  const reset = () => {
    setStep('select')
    setSelected(null)
    setGuidance(null)
    setError(null)
  }

  const severityColor: Record<string, string> = {
    low: '#22C55E',
    medium: '#F59E0B',
    high: '#F97316',
    critical: '#EF4444',
  }

  return (
    <AnimatePresence>
      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 bg-black/70 backdrop-blur-sm"
            onClick={onClose}
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            className="relative w-full max-w-lg glass-card rounded-2xl border border-base-border shadow-card overflow-hidden max-h-[90vh] overflow-y-auto"
          >
            {/* Header */}
            <div className="flex items-center justify-between p-5 border-b border-base-border sticky top-0 bg-base-card/95 backdrop-blur-sm z-10">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-risk-critical/10 border border-risk-critical/30 flex items-center justify-center">
                  <ShieldAlert className="h-4 w-4 text-risk-critical" />
                </div>
                <div>
                  <h2 className="font-bold text-white">Recovery Mode</h2>
                  <p className="text-xs text-slate-500">Get immediate guidance</p>
                </div>
              </div>
              <button
                onClick={onClose}
                className="p-1.5 text-slate-500 hover:text-white transition-colors"
              >
                <X className="h-4 w-4" />
              </button>
            </div>

            <div className="p-5">
              {/* Step: Select */}
              {step === 'select' && (
                <div className="space-y-4">
                  <p className="text-sm text-slate-400">
                    What happened? Select the option that best describes your situation.
                  </p>

                  {error && (
                    <div className="p-3 rounded-lg bg-risk-critical-bg border border-risk-critical/30 text-sm text-risk-critical">
                      {error}
                    </div>
                  )}

                  <div className="space-y-2">
                    {INTERACTION_OPTIONS.map((opt) => (
                      <button
                        key={opt.value}
                        onClick={() => setSelected(opt.value)}
                        className={`w-full flex items-center gap-3 p-3.5 rounded-xl border text-left transition-all ${
                          selected === opt.value
                            ? 'border-risk-critical/40 bg-risk-critical-bg text-white'
                            : 'border-base-border hover:border-base-border/80 hover:bg-base-elevated text-slate-300'
                        }`}
                      >
                        <span className="text-xl">{opt.icon}</span>
                        <span className="text-sm font-medium">{opt.label}</span>
                        {selected === opt.value && (
                          <CheckCircle2 className="h-4 w-4 text-risk-critical ml-auto flex-shrink-0" />
                        )}
                      </button>
                    ))}
                  </div>

                  <Button
                    onClick={handleSubmit}
                    disabled={!selected}
                    className="w-full gap-2"
                  >
                    Get Recovery Guidance
                    <ArrowRight className="h-4 w-4" />
                  </Button>
                </div>
              )}

              {/* Step: Loading */}
              {step === 'loading' && (
                <div className="text-center py-12">
                  <Loader2 className="h-8 w-8 text-cyber-cyan animate-spin mx-auto mb-4" />
                  <p className="text-slate-400">Preparing recovery guidance...</p>
                </div>
              )}

              {/* Step: Result */}
              {step === 'result' && guidance && (
                <div className="space-y-4">
                  {/* Severity header */}
                  <div
                    className="p-4 rounded-xl border"
                    style={{
                      borderColor: `${severityColor[guidance.severity]}30`,
                      backgroundColor: `${severityColor[guidance.severity]}08`,
                    }}
                  >
                    <div className="flex items-center gap-2 mb-1">
                      <AlertTriangle
                        className="h-4 w-4 flex-shrink-0"
                        style={{ color: severityColor[guidance.severity] }}
                      />
                      <span
                        className="font-bold text-sm uppercase tracking-wide"
                        style={{ color: severityColor[guidance.severity] }}
                      >
                        {guidance.severity} severity
                      </span>
                    </div>
                    <p className="text-white font-semibold text-sm">{guidance.headline}</p>
                  </div>

                  {/* Steps */}
                  <div className="space-y-3">
                    {guidance.steps.map((step: RecoveryStep, i: number) => (
                      <div
                        key={i}
                        className="flex gap-3 p-3 rounded-xl border border-base-border bg-base-elevated"
                      >
                        <div
                          className="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold"
                          style={{
                            backgroundColor: `${priorityColor[step.priority]}15`,
                            color: priorityColor[step.priority],
                            border: `1px solid ${priorityColor[step.priority]}30`,
                          }}
                        >
                          {i + 1}
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center justify-between gap-2 mb-1">
                            <span className="text-sm font-semibold text-white">{step.title}</span>
                            <span
                              className="text-xs px-2 py-0.5 rounded-full font-medium flex-shrink-0"
                              style={{
                                color: priorityColor[step.priority],
                                backgroundColor: `${priorityColor[step.priority]}15`,
                              }}
                            >
                              {priorityLabel[step.priority]}
                            </span>
                          </div>
                          <p className="text-xs text-slate-500 leading-relaxed">{step.description}</p>
                          {step.action && (
                            <p className="text-xs text-cyber-cyan mt-1 font-medium">{step.action}</p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Hotlines */}
                  {guidance.hotlines && guidance.hotlines.length > 0 && (
                    <div className="p-4 rounded-xl bg-base-elevated border border-base-border">
                      <div className="flex items-center gap-2 mb-3">
                        <Phone className="h-4 w-4 text-cyber-cyan" />
                        <span className="text-sm font-semibold text-white">
                          Important Contacts
                        </span>
                      </div>
                      {guidance.hotlines.map((h, i) => (
                        <div key={i} className="flex items-center justify-between py-1.5">
                          <span className="text-sm text-slate-400">{h.name}</span>
                          <span className="font-mono font-bold text-cyber-cyan text-sm">
                            {h.number}
                          </span>
                        </div>
                      ))}
                    </div>
                  )}

                  <div className="text-xs text-slate-600 p-3 rounded-lg bg-base-DEFAULT border border-base-border">
                    This guidance is general and informational. For serious financial losses or
                    security incidents, contact official authorities directly.
                  </div>

                  <Button variant="secondary" className="w-full" onClick={reset}>
                    Different Situation
                  </Button>
                </div>
              )}
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  )
}
