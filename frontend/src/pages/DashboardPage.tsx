import React, { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts'
import {
  Shield,
  AlertTriangle,
  TrendingUp,
  Activity,
  Eye,
  ChevronRight,
} from 'lucide-react'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { getDashboardStats } from '@/services/api'
import type { DashboardStats, RiskLevel } from '@/types'
import { getRiskHex, formatDate } from '@/utils'

const RISK_COLORS = {
  CRITICAL: '#EF4444',
  HIGH: '#F97316',
  MEDIUM: '#F59E0B',
  LOW: '#22C55E',
}

function StatCard({
  icon: Icon,
  label,
  value,
  color,
  delay = 0,
}: {
  icon: React.ElementType
  label: string
  value: number | string
  color: string
  delay?: number
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
    >
      <Card className="hover:border-cyber-cyan/20 transition-all duration-300">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-xs text-slate-500 mb-1">{label}</p>
            <p className="text-3xl font-bold" style={{ color }}>
              {value}
            </p>
          </div>
          <div
            className="w-10 h-10 rounded-xl flex items-center justify-center"
            style={{ backgroundColor: `${color}15`, border: `1px solid ${color}30` }}
          >
            <Icon className="h-5 w-5" style={{ color }} />
          </div>
        </div>
      </Card>
    </motion.div>
  )
}

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload?.length) {
    return (
      <div className="glass-card border border-base-border rounded-lg p-3 shadow-card text-xs">
        <p className="text-slate-400 mb-1">{label}</p>
        {payload.map((p: any) => (
          <p key={p.name} className="font-semibold" style={{ color: p.color || p.fill }}>
            {p.name}: {p.value}
          </p>
        ))}
      </div>
    )
  }
  return null
}

export function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getDashboardStats()
      .then((r) => setStats(r.data))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen pt-20 flex items-center justify-center">
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-cyber-cyan border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-slate-400 text-sm">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  if (error || !stats) {
    return (
      <div className="min-h-screen pt-20 flex items-center justify-center">
        <Card className="text-center max-w-md p-8">
          <AlertTriangle className="h-10 w-10 text-risk-high mx-auto mb-3" />
          <p className="text-white font-semibold mb-2">Dashboard Unavailable</p>
          <p className="text-slate-500 text-sm mb-4">{error}</p>
          <Link to="/analyze">
            <Button size="sm">Analyze Content First</Button>
          </Link>
        </Card>
      </div>
    )
  }

  const categoryData = Object.entries(stats.category_distribution).map(([name, value]) => ({
    name: name.replace(' Scam', '').replace(' Impersonation', ''),
    value,
  }))

  const riskData = Object.entries(stats.risk_distribution).map(([level, count]) => ({
    name: level,
    value: count,
    fill: RISK_COLORS[level as RiskLevel] || '#64748B',
  }))

  return (
    <div className="min-h-screen pt-20 pb-16">
      <div className="max-w-7xl mx-auto px-4 space-y-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between"
        >
          <div>
            <h1 className="text-3xl font-bold text-white">Threat Dashboard</h1>
            <p className="text-slate-500 text-sm mt-1">Overview of all analyzed content</p>
          </div>
          <Link to="/analyze">
            <Button size="sm" className="gap-1.5">
              <Shield className="h-3.5 w-3.5" /> New Analysis
            </Button>
          </Link>
        </motion.div>

        {/* Stat cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <StatCard
            icon={Activity}
            label="Total Scans"
            value={stats.total_scans}
            color="#00D4FF"
            delay={0}
          />
          <StatCard
            icon={AlertTriangle}
            label="Critical / High Risk"
            value={stats.critical_count + stats.high_risk_count}
            color="#EF4444"
            delay={0.05}
          />
          <StatCard
            icon={TrendingUp}
            label="Medium Risk"
            value={stats.medium_risk_count}
            color="#F59E0B"
            delay={0.1}
          />
          <StatCard
            icon={Shield}
            label="Low Risk / Safe"
            value={stats.low_risk_count}
            color="#22C55E"
            delay={0.15}
          />
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {/* Category Chart */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Eye className="h-4 w-4 text-cyber-cyan" />
                  Scam Category Distribution
                </CardTitle>
              </CardHeader>
              <CardContent>
                {categoryData.length > 0 ? (
                  <ResponsiveContainer width="100%" height={220}>
                    <BarChart data={categoryData} layout="vertical" margin={{ left: 0 }}>
                      <XAxis type="number" tick={{ fill: '#475569', fontSize: 11 }} />
                      <YAxis
                        type="category"
                        dataKey="name"
                        tick={{ fill: '#94A3B8', fontSize: 10 }}
                        width={100}
                      />
                      <Tooltip content={<CustomTooltip />} />
                      <Bar dataKey="value" fill="#00D4FF" radius={[0, 4, 4, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="h-48 flex items-center justify-center text-slate-600 text-sm">
                    No data yet — analyze some content first
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>

          {/* Risk Distribution */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.25 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-4 w-4 text-cyber-violet" />
                  Risk Distribution
                </CardTitle>
              </CardHeader>
              <CardContent>
                {riskData.some((d) => d.value > 0) ? (
                  <ResponsiveContainer width="100%" height={220}>
                    <PieChart>
                      <Pie
                        data={riskData}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={90}
                        paddingAngle={3}
                        dataKey="value"
                      >
                        {riskData.map((entry, index) => (
                          <Cell key={index} fill={entry.fill} />
                        ))}
                      </Pie>
                      <Tooltip content={<CustomTooltip />} />
                      <Legend
                        formatter={(value) => (
                          <span style={{ color: '#94A3B8', fontSize: 12 }}>{value}</span>
                        )}
                      />
                    </PieChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="h-48 flex items-center justify-center text-slate-600 text-sm">
                    No data yet
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Top Techniques */}
        {stats.top_techniques?.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <AlertTriangle className="h-4 w-4 text-risk-high" />
                  Top Social Engineering Techniques Detected
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-3">
                  {stats.top_techniques.slice(0, 8).map((t, i) => (
                    <div
                      key={i}
                      className="p-3 rounded-xl bg-base-elevated border border-base-border"
                    >
                      <div className="text-2xl font-bold text-risk-high mb-1">{t.count}</div>
                      <div className="text-xs text-slate-400">{t.technique}</div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* Recent Threats */}
        {stats.recent_threats?.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.35 }}
          >
            <Card>
              <CardHeader className="flex items-center justify-between">
                <CardTitle className="flex items-center gap-2">
                  <Activity className="h-4 w-4 text-cyber-cyan" />
                  Recent Threats
                </CardTitle>
                <Link to="/history">
                  <Button variant="ghost" size="sm" className="gap-1">
                    View All <ChevronRight className="h-3.5 w-3.5" />
                  </Button>
                </Link>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {stats.recent_threats.slice(0, 5).map((scan) => (
                    <Link
                      key={scan.id}
                      to={`/result/${scan.id}`}
                      className="flex items-center gap-3 p-3 rounded-xl bg-base-elevated border border-base-border hover:border-cyber-cyan/20 transition-all group"
                    >
                      <div
                        className="w-2 h-2 rounded-full flex-shrink-0"
                        style={{ backgroundColor: getRiskHex(scan.risk_level) }}
                      />
                      <div className="flex-1 min-w-0">
                        <div className="text-sm font-medium text-white truncate">
                          {scan.category}
                        </div>
                        <div className="text-xs text-slate-500">{formatDate(scan.created_at)}</div>
                      </div>
                      <Badge
                        variant={
                          scan.risk_level === 'CRITICAL'
                            ? 'risk-critical'
                            : scan.risk_level === 'HIGH'
                            ? 'risk-high'
                            : scan.risk_level === 'MEDIUM'
                            ? 'risk-medium'
                            : 'risk-low'
                        }
                      >
                        {scan.risk_score}
                      </Badge>
                      <ChevronRight className="h-4 w-4 text-slate-700 group-hover:text-cyber-cyan transition-colors" />
                    </Link>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </div>
    </div>
  )
}
