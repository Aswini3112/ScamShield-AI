import React, { useState, useRef, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  FileText,
  Image,
  Link2,
  QrCode,
  File,
  Upload,
  Zap,
  ChevronRight,
  AlertCircle,
  Globe,
} from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { AnalysisProgress } from '@/components/AnalysisProgress'
import { demoExamples } from '@/data/demoExamples'
import { analyzeText, analyzeUrl, analyzeImage, analyzeQR, analyzeDocument } from '@/services/api'
import type { InputType } from '@/types'

type Tab = InputType

const tabs: { id: Tab; label: string; icon: React.ElementType }[] = [
  { id: 'text', label: 'Text', icon: FileText },
  { id: 'image', label: 'Screenshot', icon: Image },
  { id: 'url', label: 'URL', icon: Link2 },
  { id: 'qr', label: 'QR Code', icon: QrCode },
  { id: 'document', label: 'Document', icon: File },
]

export function AnalyzePage() {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState<Tab>('text')
  const [text, setText] = useState('')
  const [url, setUrl] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [filePreview, setFilePreview] = useState<string | null>(null)
  const [analyzing, setAnalyzing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [language, setLanguage] = useState('en')
  const fileRef = useRef<HTMLInputElement>(null)
  const [dragOver, setDragOver] = useState(false)

  const handleFile = (f: File) => {
    const maxMB = 10
    if (f.size > maxMB * 1024 * 1024) {
      setError(`File too large. Maximum ${maxMB}MB allowed.`)
      return
    }
    setFile(f)
    setError(null)
    if (f.type.startsWith('image/')) {
      const reader = new FileReader()
      reader.onload = (e) => setFilePreview(e.target?.result as string)
      reader.readAsDataURL(f)
    } else {
      setFilePreview(null)
    }
  }

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      setDragOver(false)
      const dropped = e.dataTransfer.files[0]
      if (dropped) handleFile(dropped)
    },
    []
  )

  const loadDemo = (id: string) => {
    const demo = demoExamples.find((d) => d.id === id)
    if (!demo) return
    setActiveTab(demo.type)
    if (demo.type === 'text') setText(demo.content)
    else if (demo.type === 'url') setUrl(demo.content)
    setError(null)
  }

  const handleAnalyze = async () => {
    setError(null)
    setAnalyzing(true)

    try {
      let result

      if (activeTab === 'text') {
        if (!text.trim()) throw new Error('Please enter text to analyze.')
        result = await analyzeText(text, language)
      } else if (activeTab === 'url') {
        if (!url.trim()) throw new Error('Please enter a URL to analyze.')
        result = await analyzeUrl(url)
      } else if (activeTab === 'image') {
        if (!file) throw new Error('Please upload an image.')
        result = await analyzeImage(file)
      } else if (activeTab === 'qr') {
        if (!file) throw new Error('Please upload a QR code image.')
        result = await analyzeQR(file)
      } else if (activeTab === 'document') {
        if (!file) throw new Error('Please upload a document.')
        result = await analyzeDocument(file)
      }

      if (result?.success && result.data) {
        navigate('/result', { state: { result: result.data } })
      } else {
        throw new Error(result?.error || 'Analysis failed. Please try again.')
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed. Please try again.')
    } finally {
      setAnalyzing(false)
    }
  }

  const canAnalyze =
    (activeTab === 'text' && text.trim().length > 0) ||
    (activeTab === 'url' && url.trim().length > 0) ||
    (['image', 'qr', 'document'].includes(activeTab) && file !== null)

  return (
    <div className="min-h-screen pt-20 pb-16">
      <div className="max-w-3xl mx-auto px-4">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-10"
        >
          <h1 className="text-4xl font-bold text-white mb-3">
            Analyze Suspicious Content
          </h1>
          <p className="text-slate-400 text-lg">
            Upload or paste anything suspicious. ScamShield will investigate the evidence.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
        >
          <Card className="overflow-hidden">
            {/* Tabs */}
            <div className="flex border-b border-base-border -mx-5 -mt-5 mb-6 px-5 overflow-x-auto">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => {
                    setActiveTab(tab.id)
                    setError(null)
                    setFile(null)
                    setFilePreview(null)
                  }}
                  className={`flex items-center gap-2 px-4 py-3.5 text-sm font-medium border-b-2 transition-all duration-200 whitespace-nowrap ${
                    activeTab === tab.id
                      ? 'text-cyber-cyan border-cyber-cyan'
                      : 'text-slate-500 border-transparent hover:text-slate-300'
                  }`}
                >
                  <tab.icon className="h-4 w-4" />
                  {tab.label}
                </button>
              ))}
            </div>

            {/* ── TEXT TAB ──────────────────────────────────────────────── */}
            {activeTab === 'text' && (
              <div className="space-y-4">
                <div className="flex items-center gap-3 mb-2">
                  <label className="text-sm text-slate-400">Language:</label>
                  <div className="flex gap-2">
                    {[
                      { value: 'en', label: 'English' },
                      { value: 'ta', label: 'Tamil' },
                      { value: 'tg', label: 'Tanglish' },
                    ].map((l) => (
                      <button
                        key={l.value}
                        onClick={() => setLanguage(l.value)}
                        className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
                          language === l.value
                            ? 'bg-cyber-cyan/10 text-cyber-cyan border-cyber-cyan/30'
                            : 'border-base-border text-slate-500 hover:text-slate-300'
                        }`}
                      >
                        {l.label}
                      </button>
                    ))}
                  </div>
                </div>

                <textarea
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  placeholder="Paste a suspicious SMS, WhatsApp message, email, job offer, payment request, or any other message..."
                  className="w-full h-48 bg-base-elevated border border-base-border rounded-xl p-4 text-sm text-slate-200 placeholder-slate-600 resize-none focus:outline-none focus:border-cyber-cyan/50 transition-colors font-mono"
                />

                <div className="flex items-center gap-2 text-xs text-slate-500">
                  <Globe className="h-3.5 w-3.5" />
                  Prototype multilingual analysis · English, Tamil, Tanglish supported
                </div>
              </div>
            )}

            {/* ── URL TAB ───────────────────────────────────────────────── */}
            {activeTab === 'url' && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm text-slate-400 mb-2">
                    Suspicious URL
                  </label>
                  <div className="flex gap-2">
                    <div className="flex-1 flex items-center gap-2 bg-base-elevated border border-base-border rounded-xl px-4 py-3 focus-within:border-cyber-cyan/50 transition-colors">
                      <Link2 className="h-4 w-4 text-slate-600 flex-shrink-0" />
                      <input
                        type="text"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        placeholder="https://suspicious-url.example.com/verify?id=..."
                        className="flex-1 bg-transparent text-sm text-slate-200 placeholder-slate-600 focus:outline-none font-mono"
                      />
                    </div>
                  </div>
                </div>
                <div className="text-xs text-slate-600 p-3 rounded-lg bg-base-elevated border border-base-border">
                  <AlertCircle className="h-3.5 w-3.5 inline mr-1.5 text-amber-500" />
                  URLs are analyzed statically. ScamShield does not fetch or visit the target URL.
                </div>
              </div>
            )}

            {/* ── FILE UPLOAD TABS ──────────────────────────────────────── */}
            {['image', 'qr', 'document'].includes(activeTab) && (
              <div className="space-y-4">
                <div
                  onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
                  onDragLeave={() => setDragOver(false)}
                  onDrop={handleDrop}
                  onClick={() => fileRef.current?.click()}
                  className={`relative flex flex-col items-center justify-center gap-3 h-48 rounded-xl border-2 border-dashed cursor-pointer transition-all duration-200 ${
                    dragOver
                      ? 'border-cyber-cyan bg-cyber-cyan/5'
                      : file
                      ? 'border-risk-low/40 bg-risk-low-bg'
                      : 'border-base-border hover:border-cyber-cyan/40 hover:bg-base-elevated'
                  }`}
                >
                  {filePreview ? (
                    <img
                      src={filePreview}
                      alt="Preview"
                      className="h-40 object-contain rounded-lg"
                    />
                  ) : file ? (
                    <>
                      <File className="h-8 w-8 text-risk-low" />
                      <span className="text-sm text-risk-low font-medium">{file.name}</span>
                      <span className="text-xs text-slate-500">
                        {(file.size / 1024).toFixed(1)} KB
                      </span>
                    </>
                  ) : (
                    <>
                      <Upload className="h-8 w-8 text-slate-600" />
                      <div className="text-center">
                        <div className="text-sm text-slate-300 font-medium">
                          Drop file here or click to browse
                        </div>
                        <div className="text-xs text-slate-600 mt-1">
                          {activeTab === 'image' && 'PNG, JPG, WEBP up to 10MB'}
                          {activeTab === 'qr' && 'Image containing QR code, up to 10MB'}
                          {activeTab === 'document' && 'PDF, TXT, PNG, JPG up to 10MB'}
                        </div>
                      </div>
                    </>
                  )}
                </div>

                <input
                  ref={fileRef}
                  type="file"
                  className="hidden"
                  accept={
                    activeTab === 'document'
                      ? 'application/pdf,text/plain,image/png,image/jpeg'
                      : 'image/png,image/jpeg,image/webp,image/gif'
                  }
                  onChange={(e) => {
                    const f = e.target.files?.[0]
                    if (f) handleFile(f)
                  }}
                />

                {activeTab === 'document' && (
                  <div className="text-xs text-slate-600 p-3 rounded-lg bg-base-elevated border border-base-border">
                    <AlertCircle className="h-3.5 w-3.5 inline mr-1.5 text-amber-500" />
                    Uploaded files are never executed. Only text content is extracted and analyzed.
                  </div>
                )}
              </div>
            )}

            {/* Error */}
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-4 flex items-start gap-2 p-3 rounded-lg bg-risk-critical-bg border border-risk-critical/30"
              >
                <AlertCircle className="h-4 w-4 text-risk-critical flex-shrink-0 mt-0.5" />
                <span className="text-sm text-risk-critical">{error}</span>
              </motion.div>
            )}

            {/* Analyze button */}
            <div className="mt-6 flex justify-center">
              <Button
                size="lg"
                onClick={handleAnalyze}
                loading={analyzing}
                disabled={!canAnalyze || analyzing}
                className="gap-2 min-w-48"
              >
                <Zap className="h-5 w-5" />
                {analyzing ? 'Analyzing...' : 'Analyze Threat'}
              </Button>
            </div>

            {/* Analysis progress */}
            {analyzing && <AnalysisProgress active={analyzing} />}
          </Card>
        </motion.div>

        {/* Demo examples */}
        {(activeTab === 'text' || activeTab === 'url') && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="mt-6"
          >
            <p className="text-xs text-slate-500 mb-3 text-center">
              Try a demo example:
            </p>
            <div className="flex flex-wrap justify-center gap-2">
              {demoExamples
                .filter((d) => d.type === activeTab || (activeTab === 'text'))
                .slice(0, 8)
                .map((demo) => (
                  <button
                    key={demo.id}
                    onClick={() => loadDemo(demo.id)}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium border border-base-border text-slate-400 hover:text-white hover:border-cyber-cyan/30 transition-all"
                  >
                    <ChevronRight className="h-3 w-3" />
                    {demo.label}
                  </button>
                ))}
            </div>
          </motion.div>
        )}
      </div>
    </div>
  )
}
