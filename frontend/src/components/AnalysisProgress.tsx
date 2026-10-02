import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { CheckCircle2, Circle, Loader2 } from 'lucide-react'

const STEPS = [
  { id: 1, label: 'Extracting evidence', duration: 600 },
  { id: 2, label: 'Inspecting indicators', duration: 700 },
  { id: 3, label: 'Evaluating threat patterns', duration: 800 },
  { id: 4, label: 'Building attack chain', duration: 600 },
  { id: 5, label: 'Preparing security report', duration: 500 },
]

interface AnalysisProgressProps {
  active: boolean
}

export function AnalysisProgress({ active }: AnalysisProgressProps) {
  const [currentStep, setCurrentStep] = useState(0)

  useEffect(() => {
    if (!active) {
      setCurrentStep(0)
      return
    }

    let step = 0
    let timeout: ReturnType<typeof setTimeout>

    const advance = () => {
      if (step < STEPS.length) {
        setCurrentStep(step + 1)
        step++
        timeout = setTimeout(advance, STEPS[step - 1]?.duration || 600)
      }
    }

    timeout = setTimeout(advance, 200)
    return () => clearTimeout(timeout)
  }, [active])

  if (!active) return null

  return (
    <div className="w-full max-w-md mx-auto py-8">
      <div className="text-center mb-6">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-cyber-cyan/10 border border-cyber-cyan/20">
          <Loader2 className="h-4 w-4 text-cyber-cyan animate-spin" />
          <span className="text-sm text-cyber-cyan font-medium">Analyzing evidence...</span>
        </div>
      </div>

      <div className="space-y-3">
        {STEPS.map((step, index) => {
          const isComplete = currentStep > index
          const isActive = currentStep === index + 1

          return (
            <motion.div
              key={step.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: isComplete || isActive ? 1 : 0.3, x: 0 }}
              transition={{ delay: index * 0.05 }}
              className="flex items-center gap-3"
            >
              <div className="flex-shrink-0">
                {isComplete ? (
                  <CheckCircle2 className="h-5 w-5 text-risk-low" />
                ) : isActive ? (
                  <Loader2 className="h-5 w-5 text-cyber-cyan animate-spin" />
                ) : (
                  <Circle className="h-5 w-5 text-slate-700" />
                )}
              </div>
              <span
                className={`text-sm font-medium transition-colors ${
                  isComplete
                    ? 'text-risk-low'
                    : isActive
                    ? 'text-cyber-cyan'
                    : 'text-slate-600'
                }`}
              >
                {step.label}
              </span>
            </motion.div>
          )
        })}
      </div>

      {/* Scan beam animation */}
      <div className="mt-6 relative h-1 bg-base-border rounded-full overflow-hidden">
        <motion.div
          className="absolute inset-y-0 left-0 bg-gradient-to-r from-cyber-cyan/0 via-cyber-cyan to-cyber-cyan/0 rounded-full"
          animate={{ x: ['0%', '100%'] }}
          transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
          style={{ width: '30%' }}
        />
      </div>
    </div>
  )
}
