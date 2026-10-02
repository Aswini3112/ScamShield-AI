import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Navbar } from '@/components/Navbar'
import { LandingPage } from '@/pages/LandingPage'
import { AnalyzePage } from '@/pages/AnalyzePage'
import { ResultPage } from '@/pages/ResultPage'
import { DashboardPage } from '@/pages/DashboardPage'
import { HistoryPage } from '@/pages/HistoryPage'
import { LearnPage } from '@/pages/LearnPage'

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-background cyber-grid-bg">
        <Navbar />
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/analyze" element={<AnalyzePage />} />
          <Route path="/result/:id" element={<ResultPage />} />
          <Route path="/result" element={<ResultPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/history" element={<HistoryPage />} />
          <Route path="/learn" element={<LearnPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}
