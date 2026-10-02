import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'
import type { RiskLevel } from '@/types'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function getRiskColor(level: RiskLevel): string {
  switch (level) {
    case 'CRITICAL': return 'text-risk-critical'
    case 'HIGH': return 'text-risk-high'
    case 'MEDIUM': return 'text-risk-medium'
    case 'LOW': return 'text-risk-low'
    default: return 'text-slate-400'
  }
}

export function getRiskBgColor(level: RiskLevel): string {
  switch (level) {
    case 'CRITICAL': return 'bg-risk-critical-bg border-risk-critical/30'
    case 'HIGH': return 'bg-risk-high-bg border-risk-high/30'
    case 'MEDIUM': return 'bg-risk-medium-bg border-risk-medium/30'
    case 'LOW': return 'bg-risk-low-bg border-risk-low/30'
    default: return 'bg-slate-900 border-slate-700'
  }
}

export function getRiskHex(level: RiskLevel): string {
  switch (level) {
    case 'CRITICAL': return '#EF4444'
    case 'HIGH': return '#F97316'
    case 'MEDIUM': return '#F59E0B'
    case 'LOW': return '#22C55E'
    default: return '#64748B'
  }
}

export function getRiskFromScore(score: number): RiskLevel {
  if (score >= 80) return 'CRITICAL'
  if (score >= 60) return 'HIGH'
  if (score >= 30) return 'MEDIUM'
  return 'LOW'
}

export function formatDate(iso: string): string {
  return new Date(iso).toLocaleString('en-IN', {
    dateStyle: 'medium',
    timeStyle: 'short',
  })
}

export function truncate(text: string, max: number): string {
  return text.length > max ? text.slice(0, max) + '…' : text
}

export function getConfidenceLabel(confidence: number): string {
  if (confidence >= 90) return 'Very High'
  if (confidence >= 70) return 'High'
  if (confidence >= 50) return 'Moderate'
  if (confidence >= 30) return 'Low'
  return 'Uncertain'
}
