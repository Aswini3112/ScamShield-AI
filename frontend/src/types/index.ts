// ─── Core Analysis Types ─────────────────────────────────────────────────────

export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'
export type InputType = 'text' | 'url' | 'image' | 'qr' | 'document'
export type AnalysisStatus = 'idle' | 'analyzing' | 'complete' | 'error'

export interface Indicator {
  name: string
  detected: boolean
  confidence: number
  evidence?: string[]
}

export interface SocialEngineeringTechnique {
  technique: string
  confidence: number
  description: string
  evidence: string[]
}

export interface AttackChainStep {
  step: number
  title: string
  description: string
  technique?: string
}

export interface Evidence {
  type: string
  value: string
  risk_indicator: boolean
}

export interface Recommendation {
  type: 'do' | 'dont'
  text: string
}

export interface AnalysisResult {
  id?: number
  risk_score: number
  risk_level: RiskLevel
  category: string
  summary: string
  indicators: Indicator[]
  social_engineering: SocialEngineeringTechnique[]
  attack_chain: AttackChainStep[]
  recommendations: Recommendation[]
  evidence: Evidence[]
  extracted_text?: string
  extracted_urls?: string[]
  qr_detected?: boolean
  qr_content?: string
  explanation: string
  created_at?: string
  input_type?: InputType
  multilingual_note?: string
}

// ─── Dashboard Types ──────────────────────────────────────────────────────────

export interface DashboardStats {
  total_scans: number
  high_risk_count: number
  medium_risk_count: number
  low_risk_count: number
  critical_count: number
  category_distribution: Record<string, number>
  risk_distribution: Record<string, number>
  recent_threats: ScanRecord[]
  top_techniques: { technique: string; count: number }[]
}

export interface ScanRecord {
  id: number
  created_at: string
  input_type: InputType
  category: string
  risk_level: RiskLevel
  risk_score: number
  summary: string
}

// ─── Recovery Types ───────────────────────────────────────────────────────────

export type InteractionType =
  | 'only_received'
  | 'clicked_link'
  | 'entered_credentials'
  | 'shared_otp'
  | 'transferred_money'
  | 'downloaded_file'
  | 'not_sure'

export interface RecoveryStep {
  priority: 'immediate' | 'soon' | 'monitor'
  title: string
  description: string
  action?: string
}

export interface RecoveryGuidance {
  interaction_type: InteractionType
  severity: 'low' | 'medium' | 'high' | 'critical'
  headline: string
  steps: RecoveryStep[]
  hotlines?: { name: string; number: string }[]
}

// ─── API Types ────────────────────────────────────────────────────────────────

export interface ApiResponse<T> {
  success: boolean
  data: T
  error?: string
}

export interface AnalyzeTextRequest {
  text: string
  language?: string
}

export interface AnalyzeUrlRequest {
  url: string
}

// ─── Demo Examples ────────────────────────────────────────────────────────────

export interface DemoExample {
  id: string
  label: string
  type: InputType
  content: string
  language: string
  description: string
}
