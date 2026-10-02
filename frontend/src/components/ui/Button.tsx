import React from 'react'
import { cn } from '@/utils'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
}

export function Button({
  className,
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled,
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center gap-2 font-semibold rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 focus:ring-offset-background disabled:opacity-50 disabled:cursor-not-allowed',
        {
          // Variants
          'bg-cyber-cyan text-base-DEFAULT hover:bg-cyber-cyan/90 shadow-cyber hover:shadow-cyber-strong':
            variant === 'primary',
          'bg-base-card border border-base-border text-slate-300 hover:border-cyber-cyan/40 hover:text-white':
            variant === 'secondary',
          'text-slate-400 hover:text-white hover:bg-base-card': variant === 'ghost',
          'bg-risk-critical/10 border border-risk-critical/30 text-risk-critical hover:bg-risk-critical/20':
            variant === 'danger',
          'border border-base-border text-slate-300 hover:border-cyber-cyan/40 hover:text-cyber-cyan bg-transparent':
            variant === 'outline',
          // Sizes
          'text-xs px-3 py-1.5': size === 'sm',
          'text-sm px-4 py-2.5': size === 'md',
          'text-base px-6 py-3': size === 'lg',
        },
        className
      )}
      disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
          />
        </svg>
      )}
      {children}
    </button>
  )
}
