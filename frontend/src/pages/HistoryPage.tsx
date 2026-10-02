import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  Search,
  Filter,
  ChevronRight,
  FileText,
  Image,
  Link2,
  QrCode,
  File,
  AlertTriangle,
} from 'lucide-react'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { Card } from '@/components/ui/Card'
import { getScans } from '@/services/api'
import type { ScanRecord, RiskLevel } from '@/types'
import { getRiskHex, formatDate } from '@/utils'

const typeIcons: Record<string, React.ElementType> = {
  text: FileText,
  image: Image,
  url: Link2,
  qr: QrCode,
  document: File,
}

const RISK_LEVELS: RiskLevel[] = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']

export function HistoryPage() {
  const [scans, setScans] = useState<ScanRecord[]>([])
  const [filtered, setFiltered] = useState<ScanRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [search, setSearch] = useState('')
  const [filterLevel, setFilterLevel] = useState<RiskLevel | 'ALL'>('ALL')

  useEffect(() => {
    getScans(0, 100)
      .then((r) => {
        setScans(r.data)
        setFiltered(r.data)
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    let result = scans
    if (filterLevel !== 'ALL') {
      result = result.filter((s) => s.risk_level === filterLevel)
    }
    if (search.trim()) {
      const q = search.toLowerCase()
      result = result.filter(
        (s) =>
          s.category.toLowerCase().includes(q) ||
          s.summary?.toLowerCase().includes(q) ||
          s.input_type.includes(q)
      )
    }
    setFiltered(result)
  }, [scans, search, filterLevel])

  return (
    <div className="min-h-screen pt-20 pb-16">
      <div className="max-w-5xl mx-auto px-4 space-y-6">
        {/* Header */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="text-3xl font-bold text-white">Scan History</h1>
          <p className="text-slate-500 text-sm mt-1">All previously analyzed content</p>
        </motion.div>

        {/* Filters */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="flex flex-wrap gap-3"
        >
          {/* Search */}
          <div className="flex-1 min-w-48 flex items-center gap-2 bg-base-card border border-base-border rounded-xl px-3 py-2.5 focus-within:border-cyber-cyan/50 transition-colors">
            <Search className="h-4 w-4 text-slate-600 flex-shrink-0" />
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by category, type..."
              className="flex-1 bg-transparent text-sm text-slate-200 placeholder-slate-600 focus:outline-none"
            />
          </div>

          {/* Risk filter */}
          <div className="flex items-center gap-1">
            <Filter className="h-4 w-4 text-slate-600 mr-1" />
            {(['ALL', ...RISK_LEVELS] as const).map((level) => (
              <button
                key={level}
                onClick={() => setFilterLevel(level)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-all ${
                  filterLevel === level
                    ? 'bg-cyber-cyan/10 text-cyber-cyan border-cyber-cyan/30'
                    : 'border-base-border text-slate-500 hover:text-slate-300'
                }`}
              >
                {level}
              </button>
            ))}
          </div>
        </motion.div>

        {/* Table */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
        >
          <Card className="p-0 overflow-hidden">
            {loading ? (
              <div className="p-12 text-center">
                <div className="w-7 h-7 border-2 border-cyber-cyan border-t-transparent rounded-full animate-spin mx-auto mb-3" />
                <p className="text-slate-500 text-sm">Loading history...</p>
              </div>
            ) : error ? (
              <div className="p-12 text-center">
                <AlertTriangle className="h-8 w-8 text-risk-high mx-auto mb-3" />
                <p className="text-slate-500 text-sm">{error}</p>
              </div>
            ) : filtered.length === 0 ? (
              <div className="p-12 text-center">
                <FileText className="h-8 w-8 text-slate-700 mx-auto mb-3" />
                <p className="text-white font-medium mb-1">No scans found</p>
                <p className="text-slate-500 text-sm mb-4">
                  {scans.length === 0
                    ? 'Analyze some content to see it here.'
                    : 'No scans match your filters.'}
                </p>
                <Link to="/analyze">
                  <Button size="sm">Analyze Content</Button>
                </Link>
              </div>
            ) : (
              <>
                {/* Header row */}
                <div className="hidden md:grid grid-cols-12 gap-3 px-5 py-3 border-b border-base-border text-xs text-slate-600 font-semibold uppercase tracking-wider">
                  <div className="col-span-1">Type</div>
                  <div className="col-span-4">Category</div>
                  <div className="col-span-3">Date</div>
                  <div className="col-span-2">Risk</div>
                  <div className="col-span-2">Action</div>
                </div>

                {filtered.map((scan, i) => {
                  const TypeIcon = typeIcons[scan.input_type] || FileText
                  const color = getRiskHex(scan.risk_level)
                  const badgeVariant =
                    scan.risk_level === 'CRITICAL'
                      ? 'risk-critical'
                      : scan.risk_level === 'HIGH'
                      ? 'risk-high'
                      : scan.risk_level === 'MEDIUM'
                      ? 'risk-medium'
                      : 'risk-low'

                  return (
                    <motion.div
                      key={scan.id}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: i * 0.03 }}
                      className="grid grid-cols-2 md:grid-cols-12 gap-3 px-5 py-4 border-b border-base-border hover:bg-base-elevated transition-colors items-center"
                    >
                      <div className="col-span-1 flex items-center">
                        <div
                          className="w-7 h-7 rounded-lg flex items-center justify-center"
                          style={{ backgroundColor: `${color}15`, border: `1px solid ${color}30` }}
                        >
                          <TypeIcon className="h-3.5 w-3.5" style={{ color }} />
                        </div>
                      </div>
                      <div className="col-span-1 md:col-span-4 min-w-0">
                        <div className="text-sm font-medium text-white truncate">
                          {scan.category}
                        </div>
                        <div className="text-xs text-slate-500 capitalize">{scan.input_type}</div>
                      </div>
                      <div className="col-span-2 md:col-span-3">
                        <div className="text-xs text-slate-400">{formatDate(scan.created_at)}</div>
                      </div>
                      <div className="col-span-1 md:col-span-2">
                        <Badge variant={badgeVariant}>{scan.risk_score}</Badge>
                      </div>
                      <div className="col-span-1 md:col-span-2">
                        <Link to={`/result/${scan.id}`}>
                          <Button variant="ghost" size="sm" className="gap-1">
                            View <ChevronRight className="h-3.5 w-3.5" />
                          </Button>
                        </Link>
                      </div>
                    </motion.div>
                  )
                })}
              </>
            )}
          </Card>
        </motion.div>

        {filtered.length > 0 && (
          <p className="text-xs text-slate-600 text-center">
            Showing {filtered.length} of {scans.length} records
          </p>
        )}
      </div>
    </div>
  )
}
