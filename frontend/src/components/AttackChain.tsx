import React from 'react'
import { motion } from 'framer-motion'
import type { AttackChainStep } from '@/types'
import { Shield, AlertTriangle, Target, Link2, Eye, CreditCard, Lock } from 'lucide-react'

const stepIcons = [Shield, AlertTriangle, Target, Link2, Eye, CreditCard, Lock]

const stepColors = [
  '#8B5CF6', // violet
  '#EF4444', // red
  '#F97316', // orange
  '#F59E0B', // amber
  '#00D4FF', // cyan
  '#EF4444', // red
  '#DC2626', // dark red
]

interface AttackChainProps {
  steps: AttackChainStep[]
}

export function AttackChain({ steps }: AttackChainProps) {
  if (!steps || steps.length === 0) return null

  return (
    <div className="flex flex-col items-center gap-0">
      {steps.map((step, index) => {
        const Icon = stepIcons[index % stepIcons.length]
        const color = stepColors[index % stepColors.length]
        const isLast = index === steps.length - 1

        return (
          <div key={index} className="flex flex-col items-center w-full max-w-xs">
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.15, duration: 0.4 }}
              className="relative w-full"
            >
              <div
                className="flex items-center gap-3 px-4 py-3 rounded-xl border w-full"
                style={{
                  borderColor: `${color}30`,
                  backgroundColor: `${color}08`,
                }}
              >
                <div
                  className="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center"
                  style={{ backgroundColor: `${color}20`, border: `1px solid ${color}40` }}
                >
                  <Icon className="h-4 w-4" style={{ color }} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-semibold text-white">{step.title}</div>
                  {step.description && (
                    <div className="text-xs text-slate-500 mt-0.5 leading-relaxed">
                      {step.description}
                    </div>
                  )}
                </div>
                <div
                  className="flex-shrink-0 text-xs font-bold px-2 py-0.5 rounded-full"
                  style={{ color, backgroundColor: `${color}15` }}
                >
                  {index + 1}
                </div>
              </div>
            </motion.div>

            {/* Connector arrow */}
            {!isLast && (
              <motion.div
                initial={{ opacity: 0, scaleY: 0 }}
                animate={{ opacity: 1, scaleY: 1 }}
                transition={{ delay: index * 0.15 + 0.1, duration: 0.3 }}
                className="flex flex-col items-center my-1"
              >
                <div
                  className="w-0.5 h-4"
                  style={{
                    background: `linear-gradient(to bottom, ${color}, ${stepColors[(index + 1) % stepColors.length]})`,
                  }}
                />
                <div
                  className="w-0 h-0"
                  style={{
                    borderLeft: '4px solid transparent',
                    borderRight: '4px solid transparent',
                    borderTop: `6px solid ${stepColors[(index + 1) % stepColors.length]}`,
                  }}
                />
              </motion.div>
            )}
          </div>
        )
      })}
    </div>
  )
}
