import axios from 'axios'
import type {
  ApiResponse,
  AnalysisResult,
  DashboardStats,
  ScanRecord,
  RecoveryGuidance,
  InteractionType,
} from '@/types'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
})

// ─── Response interceptor for error normalisation ─────────────────────────────
api.interceptors.response.use(
  (res) => res,
  (err) => {
    const message =
      err.response?.data?.detail ||
      err.response?.data?.error ||
      err.message ||
      'An unexpected error occurred'
    return Promise.reject(new Error(message))
  }
)

// ─── Health ───────────────────────────────────────────────────────────────────
export async function checkHealth(): Promise<{ status: string; version: string }> {
  const { data } = await api.get('/health')
  return data
}

// ─── Text Analysis ────────────────────────────────────────────────────────────
export async function analyzeText(
  text: string,
  language = 'en'
): Promise<ApiResponse<AnalysisResult>> {
  const { data } = await api.post('/analyze/text', { text, language })
  return data
}

// ─── URL Analysis ─────────────────────────────────────────────────────────────
export async function analyzeUrl(url: string): Promise<ApiResponse<AnalysisResult>> {
  const { data } = await api.post('/analyze/url', { url })
  return data
}

// ─── Image / Screenshot Analysis ─────────────────────────────────────────────
export async function analyzeImage(file: File): Promise<ApiResponse<AnalysisResult>> {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post('/analyze/image', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

// ─── QR Analysis ─────────────────────────────────────────────────────────────
export async function analyzeQR(file: File): Promise<ApiResponse<AnalysisResult>> {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post('/analyze/qr', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

// ─── Document Analysis ────────────────────────────────────────────────────────
export async function analyzeDocument(file: File): Promise<ApiResponse<AnalysisResult>> {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post('/analyze/document', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

// ─── Scan History ─────────────────────────────────────────────────────────────
export async function getScans(
  skip = 0,
  limit = 50
): Promise<ApiResponse<ScanRecord[]>> {
  const { data } = await api.get('/scans', { params: { skip, limit } })
  return data
}

export async function getScan(id: number): Promise<ApiResponse<AnalysisResult>> {
  const { data } = await api.get(`/scans/${id}`)
  return data
}

// ─── Dashboard ────────────────────────────────────────────────────────────────
export async function getDashboardStats(): Promise<ApiResponse<DashboardStats>> {
  const { data } = await api.get('/dashboard/stats')
  return data
}

// ─── Recovery ─────────────────────────────────────────────────────────────────
export async function submitRecovery(
  scanId: number | null,
  interactionType: InteractionType
): Promise<ApiResponse<RecoveryGuidance>> {
  const { data } = await api.post('/recovery', {
    scan_id: scanId,
    interaction_type: interactionType,
  })
  return data
}
