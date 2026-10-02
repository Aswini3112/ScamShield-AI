import React, { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Shield, Activity, Menu, X, Zap } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { Button } from '@/components/ui/Button'
import { cn } from '@/utils'

const navLinks = [
  { to: '/', label: 'Home' },
  { to: '/analyze', label: 'Analyze' },
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/history', label: 'History' },
  { to: '/learn', label: 'Learn' },
]

export function Navbar() {
  const location = useLocation()
  const [scrolled, setScrolled] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)

  useEffect(() => {
    const handler = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', handler)
    return () => window.removeEventListener('scroll', handler)
  }, [])

  useEffect(() => setMobileOpen(false), [location.pathname])

  return (
    <nav
      className={cn(
        'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
        scrolled
          ? 'bg-base-DEFAULT/95 backdrop-blur-md border-b border-base-border shadow-card'
          : 'bg-transparent'
      )}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="relative">
              <Shield className="h-7 w-7 text-cyber-cyan group-hover:drop-shadow-[0_0_8px_rgba(0,212,255,0.8)] transition-all duration-300" />
              <span className="absolute -top-0.5 -right-0.5 w-2 h-2 bg-cyber-cyan rounded-full animate-pulse-cyber" />
            </div>
            <span className="font-bold text-lg text-white tracking-tight">
              Scam<span className="text-cyber-cyan">Shield</span>{' '}
              <span className="text-slate-400 font-normal text-sm">AI</span>
            </span>
          </Link>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                className={cn(
                  'px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200',
                  location.pathname === link.to
                    ? 'text-cyber-cyan bg-cyber-cyan/10'
                    : 'text-slate-400 hover:text-white hover:bg-base-card'
                )}
              >
                {link.label}
              </Link>
            ))}
          </div>

          {/* Right side */}
          <div className="hidden md:flex items-center gap-3">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-risk-low-bg border border-risk-low/30">
              <span className="live-dot w-2 h-2 rounded-full bg-risk-low" />
              <span className="text-xs text-risk-low font-medium">Live Protection</span>
            </div>
            <Link to="/analyze">
              <Button size="sm" className="gap-1.5">
                <Zap className="h-3.5 w-3.5" />
                Analyze Now
              </Button>
            </Link>
          </div>

          {/* Mobile toggle */}
          <button
            className="md:hidden p-2 text-slate-400 hover:text-white"
            onClick={() => setMobileOpen(!mobileOpen)}
          >
            {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden bg-base-DEFAULT/98 backdrop-blur-md border-b border-base-border"
          >
            <div className="px-4 py-4 space-y-1">
              {navLinks.map((link) => (
                <Link
                  key={link.to}
                  to={link.to}
                  className={cn(
                    'block px-4 py-2.5 rounded-lg text-sm font-medium transition-colors',
                    location.pathname === link.to
                      ? 'text-cyber-cyan bg-cyber-cyan/10'
                      : 'text-slate-400 hover:text-white'
                  )}
                >
                  {link.label}
                </Link>
              ))}
              <Link to="/analyze" className="block pt-2">
                <Button className="w-full" size="sm">
                  <Zap className="h-3.5 w-3.5" /> Analyze Now
                </Button>
              </Link>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  )
}
