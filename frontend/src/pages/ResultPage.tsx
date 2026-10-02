import React, { useState, useEffect } from 'react'
import { useLocation, useNavigate, useParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  AlertTriangle,
  CheckCircle2,
  XCircle,
  Shield,
  Link2,
  Eye,
  ChevronRight,
  RefreshCw,
  AlertCircle,
  Info,
  ShieldAlert,
} from 'lucide-react'
import { RiskMeter } from '@/components/RiskMeter'
import { AttackChain } from '@/components/AttackChain'
import { Button } from '@/components/ui/Button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { RecoveryModal } from '@/components/RecoveryModal'
import { getScan } from '@/services/api'
import type { AnalysisResult, RiskLevel } from '@/types'
import { getRiskColor, getRiskBgColor, formatDate } from '@/utils'

export function ResultPage() {
  const location = useLocation()
  const navigate = useNavigate()
  const { id } = useParams()
  const [result, setResult] = useState<AnalysisResult | null>(
    (location.state as { result?: AnalysisResult })?.result ?? null
  )
  const [loading, setLoading] = useState(!result && !!id)
  const [error, setError] = useState<string | null>(null)
  const [recoveryOpen, setRecoveryOpen] = useState(false)

  useEffect(() => {
    if (!result && id) {
      getScan(Number(id))
        .then((r) => setResult(r.data))
        .catch((e) => setError(e.message))
        .finally(() => setLoading(false))
    }
  }, [id])

  if (loading) {
    return (
      <div className="min-h-screen pt-20 flex items-center justify-center">
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-cyber-cyan border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-slate-400">Loading report...</p>
        </div>
      </div>
    )
  }

  if (error || !result) {
    return (
      <div className="min-h-screen pt-20 flex items-center justify-center">
        <Card className="text-center max-w-md">
          <AlertCircle className="h-10 w-10 text-risk-critical mx-auto mb-3" />
          <p className="text-white font-semibold mb-2">Report not found</p>
          <p className="text-slate-500 text-sm mb-4">{error}</p>
          <Button onClick={() => navigate('/analyze')}>Analyze New Content</Button>
        </Card>
      </div>
    )
  }

  const riskLevel = result.risk_level as RiskLevel
  const riskBadgeVariant =
    riskLevel === 'CRITICAL'
      ? 'risk-critical'
      : riskLevel === 'HIGH'
      ? 'risk-high'
      : riskLevel === 'MEDIUM'
      ? 'risk-medium'
      : 'risk-low'

  return (
    <div className="min-h-screen pt-20 pb-16">
      <div className="max-w-5xl mx-auto px-4 space-y-6">
        {/* ── TOP HEADER ── */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between"
        >
          <div>
            <h1 className="text-2xl font-bold text-white">Threat Assessment</h1>
            {result.created_at && (
              <p className="text-xs text-slate-500 mt-1">{formatDate(result.created_at)}</p>
            )}
          </div>
          <div className="flex gap-2">
            <Button
              variant="secondary"
              size="sm"
              onClick={() => navigate('/analyze')}
            >
              <RefreshCw className="h-3.5 w-3.5" /> New Analysis
            </Button>
          </div>
        </motion.div>

        {/* ── RISK OVERVIEW ── */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <Card
            glow={riskLevel === 'CRITICAL' || riskLevel === 'HIGH'}
            className={`border ${getRiskBgColor(riskLevel)}`}
          >
            <div className="flex flex-col sm:flex-row items-center gap-8">
              <RiskMeter score={result.risk_score} level={riskLevel} size="lg" />
              <div className="flex-1 text-center sm:text-left">
                <Badge variant={riskBadgeVariant} className="mb-3 text-sm px-4 py-1.5">
                  {riskLevel} RISK
                </Badge>
                <h2 className="text-2xl font-bold text-white mb-1">{result.category}</h2>
                <p className="text-slate-400 text-sm leading-relaxed max-w-xl">
                  {result.summary}
                </p>
                {result.multilingual_note && (
                  <p className="text-xs text-cyber-cyan/70 mt-2 flex items-center gap-1">
                    <Info className="h-3.5 w-3.5" />
                    {result.multilingual_note}
                  </p>
                )}
              </div>
            </div>
          </Card>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-6">
          {/* ── WHY SUSPICIOUS ── */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <AlertTriangle className="h-4 w-4 text-risk-high" />
                  Why This Is Suspicious
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {result.indicators?.map((ind, i) => (
                    <div
                      key={i}
                      className={`flex items-start gap-3 p-3 rounded-lg border ${
                        ind.detected
                          ? 'bg-risk-high-bg border-risk-high/20'
                          : 'bg-base-elevated border-base-border'
                      }`}
                    >
                      {ind.detected ? (
                        <AlertTriangle className="h-4 w-4 text-risk-high flex-shrink-0 mt-0.5" />
                      ) : (
                        <CheckCircle2 className="h-4 w-4 text-slate-600 flex-shrink-0 mt-0.5" />
                      )}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between gap-2">
                          <span
                            className={`text-sm font-medium ${
                              ind.detected ? 'text-white' : 'text-slate-500'
                            }`}
                          >
                            {ind.name}
                          </span>
                          {ind.detected && (
                            <span className="text-xs text-risk-high font-bold flex-shrink-0">
                              {ind.confidence}%
                            </span>
                          )}
                        </div>
                        {ind.evidence && ind.evidence.length > 0 && (
                          <div className="mt-1 flex flex-wrap gap-1">
                            {ind.evidence.slice(0, 3).map((e, j) => (
                              <span
                                key={j}
                                className="text-xs text-slate-500 bg-base-DEFAULT px-2 py-0.5 rounded font-mono"
                              >
                                "{e}"
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* ── SOCIAL ENGINEERING ── */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.25 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Eye className="h-4 w-4 text-cyber-violet" />
                  Social Engineering Techniques
                </CardTitle>
              </CardHeader>
              <CardContent>
                {result.social_engineering?.length > 0 ? (
                  <div className="space-y-3">
                    {result.social_engineering.map((tech, i) => (
                      <div
                        key={i}
                        className="p-3 rounded-lg bg-base-elevated border border-base-border"
                      >
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-sm font-semibold text-white">
                            {tech.technique}
                          </span>
                          <span className="text-xs font-bold text-cyber-violet">
                            {tech.confidence}%
                          </span>
                        </div>
                        <p className="text-xs text-slate-500 mb-2">{tech.description}</p>
                        {/* Confidence bar */}
                        <div className="h-1.5 bg-base-border rounded-full overflow-hidden">
                          <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${tech.confidence}%` }}
                            transition={{ duration: 0.8, delay: i * 0.1 }}
                            className="h-full rounded-full bg-gradient-to-r from-cyber-violet to-cyber-cyan"
                          />
                        </div>
                        {tech.evidence?.length > 0 && (
                          <div className="mt-2 flex flex-wrap gap-1">
                            {tech.evidence.slice(0, 3).map((e, j) => (
                              <span
                                key={j}
                                className="text-xs text-slate-600 bg-base-DEFAULT px-2 py-0.5 rounded font-mono"
                              >
                                {e}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-slate-500 text-sm">No manipulation techniques detected.</p>
                )}
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* ── ATTACK CHAIN ── */}
        {result.attack_chain?.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Link2 className="h-4 w-4 text-cyber-cyan" />
                  Attack Chain
                </CardTitle>
                <p className="text-xs text-slate-500 mt-1">
                  Reconstructed attacker strategy — how this scam is designed to work
                </p>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-2 gap-6 items-start">
                  <AttackChain steps={result.attack_chain} />
                  <div className="space-y-3">
                    <div className="p-4 rounded-xl bg-base-elevated border border-base-border">
                      <h4 className="text-sm font-semibold text-white mb-2">
                        AI Explanation
                      </h4>
                      <p className="text-sm text-slate-400 leading-relaxed">
                        {result.explanation}
                      </p>
                    </div>
                    <div className="text-xs text-slate-600 p-3 rounded-lg bg-base-DEFAULT border border-base-border">
                      <Info className="h-3.5 w-3.5 inline mr-1.5 text-slate-500" />
                      AI assessment is an aid, not definitive proof. Always verify through
                      official channels.
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* ── EVIDENCE ── */}
        {(result.extracted_text ||
          (result.extracted_urls && result.extracted_urls.length > 0) ||
          result.qr_content) && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.35 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Shield className="h-4 w-4 text-slate-400" />
                  Extracted Evidence
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {result.extracted_text && (
                  <div>
                    <div className="text-xs text-slate-500 mb-2">Extracted Text</div>
                    <div className="p-3 rounded-lg bg-base-elevated border border-base-border font-mono text-xs text-slate-300 max-h-32 overflow-y-auto">
                      {result.extracted_text}
                    </div>
                  </div>
                )}
                {result.extracted_urls && result.extracted_urls.length > 0 && (
                  <div>
                    <div className="text-xs text-slate-500 mb-2">Detected URLs</div>
                    {result.extracted_urls.map((u, i) => (
                      <div
                        key={i}
                        className="flex items-center gap-2 p-2 rounded-lg bg-base-elevated border border-risk-high/20 mb-1"
                      >
                        <Link2 className="h-3.5 w-3.5 text-risk-high flex-shrink-0" />
                        <span className="text-xs font-mono text-slate-400 break-all">{u}</span>
                      </div>
                    ))}
                  </div>
                )}
                {result.qr_content && (
                  <div>
                    <div className="text-xs text-slate-500 mb-2">QR Code Content</div>
                    <div className="p-3 rounded-lg bg-base-elevated border border-cyber-violet/20 font-mono text-xs text-slate-300">
                      {result.qr_content}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* ── WHAT TO DO ── */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <ShieldAlert className="h-4 w-4 text-cyber-cyan" />
                What You Should Do
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid sm:grid-cols-2 gap-4">
                <div>
                  <div className="text-xs font-semibold text-risk-low uppercase tracking-wider mb-3 flex items-center gap-1.5">
                    <CheckCircle2 className="h-3.5 w-3.5" /> Do
                  </div>
                  <div className="space-y-2">
                    {result.recommendations
                      ?.filter((r) => r.type === 'do')
                      .map((r, i) => (
                        <div key={i} className="flex items-start gap-2">
                          <CheckCircle2 className="h-4 w-4 text-risk-low flex-shrink-0 mt-0.5" />
                          <span className="text-sm text-slate-300">{r.text}</span>
                        </div>
                      ))}
                  </div>
                </div>
                <div>
                  <div className="text-xs font-semibold text-risk-critical uppercase tracking-wider mb-3 flex items-center gap-1.5">
                    <XCircle className="h-3.5 w-3.5" /> Don't
                  </div>
                  <div className="space-y-2">
                    {result.recommendations
                      ?.filter((r) => r.type === 'dont')
                      .map((r, i) => (
                        <div key={i} className="flex items-start gap-2">
                          <XCircle className="h-4 w-4 text-risk-critical flex-shrink-0 mt-0.5" />
                          <span className="text-sm text-slate-300">{r.text}</span>
                        </div>
                      ))}
                  </div>
                </div>
              </div>

              {/* Recovery CTA */}
              <div className="mt-6 pt-5 border-t border-base-border text-center">
                <p className="text-sm text-slate-500 mb-3">
                  Did you already interact with this content?
                </p>
                <Button
                  variant="danger"
                  onClick={() => setRecoveryOpen(true)}
                  className="gap-2"
                >
                  <ShieldAlert className="h-4 w-4" />
                  I Already Interacted — Get Recovery Help
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Recovery Modal */}
      <RecoveryModal
        open={recoveryOpen}
        onClose={() => setRecoveryOpen(false)}
        scanId={result.id ?? null}
      />
    </div>
  )
}
