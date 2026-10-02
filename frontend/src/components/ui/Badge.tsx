import React from 'react'
import { cn } from '@/utils'

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'default' | 'outline' | 'risk-low' | 'risk-medium' | 'risk-high' | 'risk-critical'
}

export function Badge({ className, variant = 'default', ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors',
        {
          'bg-cyber-blue/10 text-cyber-cyan border border-cyber-cyan/20': variant === 'default',
          'border border-base-border text-slate-300': variant === 'outline',
          'bg-risk-low-bg text-risk-low border border-risk-low/30': variant === 'risk-low',
          'bg-risk-medium-bg text-risk-medium border border-risk-medium/30': variant === 'risk-medium',
          'bg-risk-high-bg text-risk-high border border-risk-high/30': variant === 'risk-high',
          'bg-risk-critical-bg text-risk-critical border border-risk-critical/30': variant === 'risk-critical',
        },
        className
      )}
      {...props}
    />
  )
}
