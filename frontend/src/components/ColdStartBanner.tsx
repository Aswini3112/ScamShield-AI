import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Loader2, X, Zap } from 'lucide-react'
import { checkHealth } from '@/services/api'

/**
 * Shown on first load when the Render backend is cold-starting.
 * Polls /api/health until the backend responds, then hides itself.
 * Only visible in production (when VITE_API_URL is set).
 */
export function ColdStartBanner() {
  const [visible, setVisible] = useState(false)
  const [dismissed, setDismissed] = useState(false)

  useEffect(() => {
    // Only show in production builds where we point to a real backend
    if (!import.meta.env.VITE_API_URL) return

    let attempts = 0
    const MAX = 20
    let timer: ReturnType<typeof setTimeout>

    const ping = async () => {
      attempts++
      try {
        await checkHealth()
        setVisible(false)   // backend is up
      } catch {
        if (attempts === 2) setVisible(true)   // show after 2 failed pings
        if (attempts < MAX) timer = setTimeout(ping, 3000)
      }
    }

    // First ping after 1 second
    timer = setTimeout(ping, 1000)
    return () => clearTimeout(timer)
  }, [])

  if (!visible || dismissed) return null

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: -60 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -60 }}
        className="fixed top-16 left-0 right-0 z-40 flex justify-center px-4"
      >
        <div className="flex items-center gap-3 px-4 py-3 rounded-xl bg-amber-500/10 border border-amber-500/30 shadow-lg backdrop-blur-sm max-w-lg w-full">
          <Loader2 className="h-4 w-4 text-amber-400 animate-spin flex-shrink-0" />
          <div className="flex-1 min-w-0">
            <p className="text-sm text-amber-300 font-medium">
              Backend is waking up…
            </p>
            <p className="text-xs text-amber-500 mt-0.5">
              Render free tier sleeps after inactivity. First request takes ~30s. Hang tight!
            </p>
          </div>
          <button
            onClick={() => setDismissed(true)}
            className="text-amber-600 hover:text-amber-400 flex-shrink-0"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
      </motion.div>
    </AnimatePresence>
  )
}
