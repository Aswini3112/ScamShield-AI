import React from 'react'
import { motion } from 'framer-motion'
import type { RiskLevel } from '@/types'
import { getRiskHex } from '@/utils'

interface RiskMeterProps {
  score: number
  level: RiskLevel
  size?: 'sm' | 'md' | 'lg'
}

export function RiskMeter({ score, level, size = 'md' }: RiskMeterProps) {
  const color = getRiskHex(level)
  const radius = size === 'lg' ? 54 : size === 'md' ? 42 : 32
  const stroke = size === 'lg' ? 7 : 5
  const svgSize = (radius + stroke) * 2
  const circumference = 2 * Math.PI * radius
  const dashOffset = circumference - (score / 100) * circumference

  const fontSize = size === 'lg' ? 'text-4xl' : size === 'md' ? 'text-3xl' : 'text-xl'
  const labelSize = size === 'lg' ? 'text-sm' : 'text-xs'

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative" style={{ width: svgSize, height: svgSize }}>
        <svg width={svgSize} height={svgSize} style={{ transform: 'rotate(-90deg)' }}>
          {/* Background track */}
          <circle
            cx={svgSize / 2}
            cy={svgSize / 2}
            r={radius}
            fill="none"
            stroke="rgba(30,45,69,0.8)"
            strokeWidth={stroke}
          />
          {/* Progress arc */}
          <motion.circle
            cx={svgSize / 2}
            cy={svgSize / 2}
            r={radius}
            fill="none"
            stroke={color}
            strokeWidth={stroke}
            strokeLinecap="round"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: dashOffset }}
            transition={{ duration: 1.2, ease: 'easeOut' }}
            style={{
              filter: `drop-shadow(0 0 6px ${color}80)`,
            }}
          />
        </svg>
        {/* Center content */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <motion.span
            className={`${fontSize} font-bold`}
            style={{ color }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            {score}
          </motion.span>
          <span className="text-xs text-slate-500">/100</span>
        </div>
      </div>
      <div
        className={`${labelSize} font-bold tracking-widest uppercase px-3 py-1 rounded-full border`}
        style={{
          color,
          borderColor: `${color}40`,
          backgroundColor: `${color}10`,
        }}
      >
        {level}
      </div>
    </div>
  )
}
