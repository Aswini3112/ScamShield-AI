/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ['class'],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: '2rem',
      screens: {
        '2xl': '1400px',
      },
    },
    extend: {
      colors: {
        // ScamShield Midnight Cyber Defense palette
        base: {
          DEFAULT: '#070B14',
          card: '#0D1422',
          elevated: '#111827',
          border: '#1E2D45',
        },
        cyber: {
          cyan: '#00D4FF',
          blue: '#3B82F6',
          violet: '#8B5CF6',
          'cyan-dim': '#0099BB',
          'blue-dim': '#2563EB',
        },
        risk: {
          low: '#22C55E',
          medium: '#F59E0B',
          high: '#F97316',
          critical: '#EF4444',
          'low-bg': '#052e16',
          'medium-bg': '#451a03',
          'high-bg': '#431407',
          'critical-bg': '#450a0a',
        },
        border: '#1E2D45',
        input: '#1E2D45',
        ring: '#00D4FF',
        background: '#070B14',
        foreground: '#E2E8F0',
        primary: {
          DEFAULT: '#00D4FF',
          foreground: '#070B14',
        },
        secondary: {
          DEFAULT: '#1E2D45',
          foreground: '#E2E8F0',
        },
        muted: {
          DEFAULT: '#0D1422',
          foreground: '#64748B',
        },
        accent: {
          DEFAULT: '#8B5CF6',
          foreground: '#E2E8F0',
        },
        card: {
          DEFAULT: '#0D1422',
          foreground: '#E2E8F0',
        },
      },
      fontFamily: {
        sans: ['Inter', 'Plus Jakarta Sans', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      backgroundImage: {
        'cyber-grid': `linear-gradient(rgba(0, 212, 255, 0.03) 1px, transparent 1px),
                       linear-gradient(90deg, rgba(0, 212, 255, 0.03) 1px, transparent 1px)`,
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'hero-glow': 'radial-gradient(ellipse 80% 50% at 50% -20%, rgba(0,212,255,0.12), transparent)',
      },
      backgroundSize: {
        'cyber-grid': '40px 40px',
      },
      boxShadow: {
        'cyber': '0 0 20px rgba(0, 212, 255, 0.15)',
        'cyber-strong': '0 0 40px rgba(0, 212, 255, 0.25)',
        'violet': '0 0 20px rgba(139, 92, 246, 0.2)',
        'card': '0 4px 24px rgba(0, 0, 0, 0.4)',
        'glow-red': '0 0 20px rgba(239, 68, 68, 0.3)',
        'glow-orange': '0 0 20px rgba(249, 115, 22, 0.3)',
        'glow-green': '0 0 20px rgba(34, 197, 94, 0.3)',
      },
      keyframes: {
        'fade-in': {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'pulse-cyber': {
          '0%, 100%': { opacity: '1', boxShadow: '0 0 8px rgba(0,212,255,0.4)' },
          '50%': { opacity: '0.7', boxShadow: '0 0 20px rgba(0,212,255,0.8)' },
        },
        'scan-line': {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100vh)' },
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-8px)' },
        },
      },
      animation: {
        'fade-in': 'fade-in 0.5s ease-out',
        'pulse-cyber': 'pulse-cyber 2s ease-in-out infinite',
        'float': 'float 3s ease-in-out infinite',
      },
      borderRadius: {
        lg: '0.75rem',
        md: '0.5rem',
        sm: '0.375rem',
      },
    },
  },
  plugins: [],
}
