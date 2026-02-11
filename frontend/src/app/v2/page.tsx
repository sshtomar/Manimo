'use client'

import Link from 'next/link'
import { SignInButton, SignedIn, SignedOut } from '@clerk/nextjs'
import { Play, Pause, RotateCcw } from 'lucide-react'
import { useState, useRef } from 'react'

function ArrowIcon({ className }: { className?: string }) {
  return (
    <svg className={className} width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M3 8H13M13 8L8.5 3.5M13 8L8.5 12.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  )
}

function ChevronDown({ className }: { className?: string }) {
  return (
    <svg className={className} width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M5 7.5L10 12.5L15 7.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  )
}

// Interactive video demo component
function VideoDemo() {
  const [showVideo, setShowVideo] = useState(false)
  const [isPlaying, setIsPlaying] = useState(false)
  const videoRef = useRef<HTMLVideoElement>(null)

  const handleRun = () => {
    setShowVideo(true)
    setIsPlaying(true)
    setTimeout(() => {
      if (videoRef.current) {
        videoRef.current.currentTime = 0
        videoRef.current.play()
      }
    }, 100)
  }

  const handlePlayPause = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause()
      } else {
        videoRef.current.play()
      }
      setIsPlaying(!isPlaying)
    }
  }

  const handleReset = () => {
    if (videoRef.current) {
      videoRef.current.currentTime = 0
      videoRef.current.play()
      setIsPlaying(true)
    }
  }

  if (showVideo) {
    return (
      <div className="marimo-cell overflow-hidden">
        <div className="flex items-center justify-between px-3 py-2 bg-[#F8FAFC] border-b border-[#E5E7EB]">
          <span className="font-mono text-[10px] text-slate-light">Output: derivative_scene.mp4</span>
          <div className="flex items-center gap-2">
            <button onClick={handleReset} className="p-1 text-slate-light hover:text-ink transition-colors">
              <RotateCcw className="h-3.5 w-3.5" />
            </button>
            <button
              onClick={handlePlayPause}
              className="flex items-center justify-center h-6 w-6 rounded bg-gold text-white hover:bg-gold-dark transition-colors"
            >
              {isPlaying ? <Pause className="h-3 w-3" fill="currentColor" /> : <Play className="h-3 w-3 ml-0.5" fill="currentColor" />}
            </button>
          </div>
        </div>
        <video
          ref={videoRef}
          src="/videos/derivative_demo.mp4"
          className="w-full"
          playsInline
          onEnded={() => setIsPlaying(false)}
        />
      </div>
    )
  }

  return (
    <div className="marimo-cell">
      <div className="marimo-cell-body">
        <div className="marimo-line-numbers">
          <span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span>
        </div>
        <div className="marimo-code-content">
          <code>
            <span className="marimo-comment"># AI-generated Manim code</span>{'\n'}
            <span className="marimo-keyword">class</span> <span className="marimo-function">DerivativeScene</span>(Scene):{'\n'}
            {'  '}<span className="marimo-keyword">def</span> <span className="marimo-function">construct</span>(self):{'\n'}
            {'    '}axes = Axes(x_range=[<span className="marimo-number">-3</span>, <span className="marimo-number">3</span>]){'\n'}
            {'    '}graph = axes.plot(<span className="marimo-keyword">lambda</span> x: x**<span className="marimo-number">2</span>){'\n'}
            {'    '}tangent = TangentLine(graph, alpha=<span className="marimo-number">0</span>){'\n'}
            {'    '}self.play(Create(axes), Create(graph)){'\n'}
            {'    '}self.play(tangent.animate.move_along(graph))
          </code>
        </div>
      </div>
      <div className="flex items-center justify-between px-3 py-2 bg-[#F1F5F9] border-t border-[#E5E7EB]">
        <span className="font-mono text-[10px] text-slate-light">derivative_scene</span>
        <button
          onClick={handleRun}
          className="flex items-center gap-1.5 px-3 py-1 bg-gold text-white text-[10px] font-medium rounded hover:bg-gold-dark transition-colors"
        >
          <Play className="h-3 w-3" fill="currentColor" />
          Run
        </button>
      </div>
    </div>
  )
}

export default function InquiroStyleLanding() {
  return (
    <main className="min-h-screen bg-ivory">
      {/* Hero Section */}
      <section className="relative min-h-[85vh] md:min-h-[90vh] flex flex-col justify-center bg-grid-editorial">
        {/* Decorative math symbols */}
        <div className="hidden md:block absolute top-20 right-[15%] math-decoration select-none" aria-hidden="true">
          &part;
        </div>
        <div className="hidden md:block absolute bottom-32 left-[10%] math-decoration select-none" style={{ fontSize: '6rem' }} aria-hidden="true">
          &int;
        </div>

        <div className="max-w-7xl mx-auto px-5 sm:px-6 md:px-12 lg:px-20 pt-20 sm:pt-24 pb-16 sm:pb-20">
          <div className="max-w-4xl mx-auto text-center stagger-children">
            <h1 className="font-display text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl font-medium text-ink leading-[1.15] sm:leading-[1.1] mb-6 sm:mb-8">
              From natural language to<br />
              <span className="sm:whitespace-nowrap">
                <span className="italic text-slate">beautiful</span> animations
              </span>
            </h1>

            <p className="text-base sm:text-lg md:text-xl text-slate leading-relaxed mb-8 sm:mb-10 max-w-2xl mx-auto px-2">
              Less syntax. More teaching.
            </p>

            <div className="flex flex-wrap justify-center gap-3 sm:gap-4 mb-12 sm:mb-16">
              <SignedOut>
                <SignInButton mode="modal">
                  <button className="btn-editorial-primary">
                    <span>Launch Dashboard</span>
                  </button>
                </SignInButton>
              </SignedOut>
              <SignedIn>
                <Link href="/dashboard" className="btn-editorial-primary">
                  <span>Launch Dashboard</span>
                </Link>
              </SignedIn>
            </div>
          </div>
        </div>

        {/* Scroll indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 text-slate-light">
          <span className="text-xs tracking-wider uppercase">Scroll</span>
          <ChevronDown className="w-5 h-5 animate-bounce-gentle" />
        </div>
      </section>

      {/* Product Preview Section */}
      <section className="py-16 sm:py-24 md:py-32 bg-ivory border-t border-cream overflow-hidden">
        <div className="max-w-7xl mx-auto px-5 sm:px-6 md:px-12 lg:px-20">
          <div className="mb-10 sm:mb-16 max-w-3xl">
            <p className="text-xs sm:text-sm font-medium tracking-[0.2em] uppercase text-gold mb-4 sm:mb-6">
              See It In Action
            </p>
            <h2 className="font-display text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-medium text-ink leading-tight mb-4 sm:mb-6">
              3Blue1Brown-quality animations,<br className="hidden sm:block" /> built-in best practices
            </h2>
            <p className="text-base sm:text-lg text-slate leading-relaxed">
              Describe what you want to visualize. Get code with proper timing, easing, and pedagogical structure—ready to render.
            </p>
          </div>

          {/* Two-panel preview */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8">
            {/* Panel 1: Marimo Notebook */}
            <div className="preview-window w-full">
              <div className="preview-title">Reactive notebook</div>
              <div className="flex items-center gap-3 px-3 py-2 bg-[#FAFBFC] border-b border-cream text-xs text-slate font-mono">
                ~/notebooks/derivative_visualization.py
              </div>
              <div className="p-4 max-h-[420px] overflow-y-auto">
                <h3 className="font-display text-lg font-semibold text-ink mb-1">
                  Derivative Visualization
                </h3>
                <p className="text-xs text-slate mb-4">
                  Animate the tangent line moving along f(x) = x²
                </p>

                {/* Animation strategy */}
                <div className="rounded-md border-l-[3px] border-gold bg-ivory-warm p-3 mb-4">
                  <h4 className="font-display text-sm font-semibold text-ink mb-2">
                    Animation Strategy
                  </h4>
                  <ul className="text-xs space-y-1 pl-4 list-disc text-slate">
                    <li>Show the parabola first, establish context</li>
                    <li>Introduce a moving point with tangent line</li>
                    <li>Display slope value updating in real-time</li>
                  </ul>
                </div>

                {/* Code cell with video demo */}
                <VideoDemo />

                {/* Animation preview chart */}
                <div className="border border-cream rounded-lg p-4 bg-white">
                  <h4 className="font-display text-sm font-semibold text-ink mb-2">
                    Tangent Line Animation Preview
                  </h4>
                  <svg viewBox="0 0 200 80" className="w-full h-20">
                    {/* Grid */}
                    <line x1="20" y1="40" x2="180" y2="40" stroke="#94A3B8" strokeWidth="1"/>
                    <line x1="100" y1="10" x2="100" y2="70" stroke="#94A3B8" strokeWidth="0.5"/>
                    {/* Parabola */}
                    <path d="M 20 70 Q 60 10 100 40 T 180 70" fill="none" stroke="#0D9488" strokeWidth="2"/>
                    {/* Moving point */}
                    <circle cx="100" cy="40" r="4" fill="#B8860B"/>
                    {/* Tangent line */}
                    <line x1="70" y1="55" x2="130" y2="25" stroke="#DC2626" strokeWidth="1.5"/>
                    {/* Labels */}
                    <text x="185" y="72" fontSize="8" fill="#94A3B8">x</text>
                    <text x="102" y="8" fontSize="8" fill="#94A3B8">y</text>
                  </svg>
                  <p className="text-[9px] text-slate-light italic mt-2">
                    Point traces curve while tangent line updates continuously
                  </p>
                </div>
              </div>
            </div>

            {/* Panel 2: AI Chat */}
            <div className="preview-window w-full">
              <div className="preview-title">Animation guidance</div>
              <div className="flex items-center justify-between px-3 py-2 border-b border-cream">
                <div className="flex items-center gap-2 text-sm">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-slate">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
                  </svg>
                  <span className="font-medium text-ink">Manim patterns</span>
                </div>
                <div className="flex gap-2">
                  <button className="px-3 py-1 text-xs border border-cream rounded hover:bg-ivory-warm transition-colors">
                    Export
                  </button>
                  <button className="px-3 py-1 text-xs bg-gold text-white rounded hover:bg-gold-dark transition-colors">
                    Apply
                  </button>
                </div>
              </div>

              <div className="p-4 max-h-[360px] overflow-y-auto">
                {/* User message */}
                <div className="chat-thread-item user">
                  <div className="chat-avatar user">U</div>
                  <div className="leading-relaxed">
                    How do I make the tangent line animation smoother? It feels jerky at the endpoints.
                  </div>
                </div>

                {/* Assistant message */}
                <div className="chat-thread-item assistant">
                  <div className="chat-avatar assistant">M</div>
                  <div className="thinking-indicator">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <circle cx="12" cy="12" r="10"/>
                      <path d="M12 6v6l4 2"/>
                    </svg>
                    Loaded skill: manim-api-patterns
                  </div>
                  <div className="leading-relaxed mb-2">
                    The jerkiness comes from linear interpolation. Use <strong>rate_func</strong> to add easing:
                  </div>
                  <div className="chat-code-block">
                    <span style={{color: '#64748B'}}># Smooth easing for natural motion</span>{'\n'}
                    self.play({'\n'}
                    {'  '}t.animate.set_value(<span style={{color: '#2563EB'}}>2</span>),{'\n'}
                    {'  '}run_time=<span style={{color: '#2563EB'}}>4</span>,{'\n'}
                    {'  '}rate_func=<span style={{color: '#D97706'}}>smooth</span>{'\n'}
                    )
                  </div>
                  <div className="leading-relaxed mt-3">
                    <strong>3Blue1Brown tip:</strong>
                    <br />Use <code className="bg-[#F1F5F9] px-1 py-0.5 rounded text-xs">smooth</code> for math animations—it gives viewers time to process at start and end.
                  </div>
                </div>
              </div>

              <div className="p-4 border-t border-cream">
                <input
                  type="text"
                  className="w-full px-4 py-2.5 border border-cream rounded-lg text-sm bg-ivory-warm text-slate-light"
                  placeholder="Ask about animation techniques..."
                  readOnly
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Philosophy Section */}
      <section className="pt-16 sm:pt-24 md:pt-32 pb-12 sm:pb-16 md:pb-20 bg-ivory-warm border-t border-cream">
        <div className="max-w-7xl mx-auto px-5 sm:px-6 md:px-12 lg:px-20">
          <div className="max-w-3xl">
            <p className="text-xs sm:text-sm font-medium tracking-[0.2em] uppercase text-gold mb-4 sm:mb-6">
              Our Philosophy
            </p>
            <h2 className="font-display text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-medium text-ink leading-tight mb-6 sm:mb-8">
              Pedagogical excellence should be the default, not an afterthought
            </h2>
            <p className="text-base sm:text-lg text-slate leading-relaxed mb-6 sm:mb-8">
              We optimize for understanding. Every animation includes proper timing. Every transition
              uses appropriate easing. Every visual hierarchy guides the viewer. Because good teaching
              requires good tools.
            </p>
            <p className="text-base sm:text-lg text-slate leading-relaxed">
              We didn&apos;t invent these principles—we learned from the best: {' '}
              <a href="https://www.3blue1brown.com" target="_blank" rel="noopener noreferrer" className="text-ink underline decoration-gold/50 hover:decoration-gold transition-colors">
                3Blue1Brown
              </a>
              &apos;s visual storytelling,{' '}
              <a href="https://www.manim.community" target="_blank" rel="noopener noreferrer" className="text-ink underline decoration-gold/50 hover:decoration-gold transition-colors">
                Manim Community
              </a>
              {' '}API patterns, and{' '}
              <a href="https://marimo.io" target="_blank" rel="noopener noreferrer" className="text-ink underline decoration-gold/50 hover:decoration-gold transition-colors">
                Marimo
              </a>
              {' '}reactive notebooks.
            </p>
          </div>
        </div>
      </section>

      {/* Example Animations Section */}
      <section className="pt-12 sm:pt-16 md:pt-20 pb-16 sm:pb-24 md:pb-32 bg-ivory-warm">
        <div className="max-w-7xl mx-auto px-5 sm:px-6 md:px-12 lg:px-20">
          <div className="mb-10 sm:mb-16">
            <p className="text-xs sm:text-sm font-medium tracking-[0.2em] uppercase text-gold mb-4 sm:mb-6">
              Made with Manimo
            </p>
            <h2 className="font-display text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-medium text-ink leading-tight">
              Example animations
            </h2>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
            {/* Example 1 */}
            <Link href="/dashboard" className="card-editorial p-4 sm:p-6 block group">
              <div className="aspect-[4/3] bg-gradient-to-br from-ink/5 to-transparent rounded mb-4 sm:mb-6 flex items-center justify-center">
                <svg viewBox="0 0 120 90" className="w-3/4 h-auto opacity-60 group-hover:opacity-100 transition-opacity">
                  <line x1="20" y1="70" x2="100" y2="70" stroke="#94A3B8" strokeWidth="1"/>
                  <line x1="20" y1="70" x2="20" y2="20" stroke="#94A3B8" strokeWidth="1"/>
                  <path d="M 20 60 Q 40 20 60 50 T 100 30" fill="none" stroke="#0D9488" strokeWidth="2"/>
                  <circle cx="60" cy="50" r="4" fill="#B8860B"/>
                </svg>
              </div>
              <p className="text-xs font-medium tracking-wider uppercase text-gold mb-1.5 sm:mb-2">
                Calculus
              </p>
              <h3 className="font-display text-lg sm:text-xl font-medium text-ink mb-1.5 sm:mb-2 group-hover:text-gold transition-colors">
                Derivative Visualization
              </h3>
              <p className="text-xs sm:text-sm text-slate">
                Tangent line animation with slope updates
              </p>
            </Link>

            {/* Example 2 */}
            <Link href="/dashboard" className="card-editorial p-4 sm:p-6 block group">
              <div className="aspect-[4/3] bg-gradient-to-br from-ink/5 to-transparent rounded mb-4 sm:mb-6 flex items-center justify-center">
                <svg viewBox="0 0 120 90" className="w-3/4 h-auto opacity-60 group-hover:opacity-100 transition-opacity">
                  <rect x="30" y="30" width="25" height="25" fill="none" stroke="#0D9488" strokeWidth="1.5"/>
                  <rect x="65" y="30" width="25" height="25" fill="none" stroke="#B8860B" strokeWidth="1.5"/>
                  <path d="M 42 55 L 42 70 L 78 70 L 78 55" fill="none" stroke="#94A3B8" strokeWidth="1" strokeDasharray="3,2"/>
                </svg>
              </div>
              <p className="text-xs font-medium tracking-wider uppercase text-gold mb-1.5 sm:mb-2">
                Linear Algebra
              </p>
              <h3 className="font-display text-lg sm:text-xl font-medium text-ink mb-1.5 sm:mb-2 group-hover:text-gold transition-colors">
                Matrix Multiplication
              </h3>
              <p className="text-xs sm:text-sm text-slate">
                Step-by-step transformation visualization
              </p>
            </Link>

            {/* Example 3 */}
            <Link href="/dashboard" className="card-editorial p-4 sm:p-6 block group sm:col-span-2 lg:col-span-1">
              <div className="aspect-[4/3] bg-gradient-to-br from-ink/5 to-transparent rounded mb-4 sm:mb-6 flex items-center justify-center">
                <svg viewBox="0 0 120 90" className="w-3/4 h-auto opacity-60 group-hover:opacity-100 transition-opacity">
                  <path d="M 20 45 Q 35 20 50 45 T 80 45 T 110 45" fill="none" stroke="#0D9488" strokeWidth="2"/>
                  <path d="M 20 55 Q 35 80 50 55 T 80 55 T 110 55" fill="none" stroke="#B8860B" strokeWidth="1.5" strokeDasharray="4,2"/>
                </svg>
              </div>
              <p className="text-xs font-medium tracking-wider uppercase text-gold mb-1.5 sm:mb-2">
                Trigonometry
              </p>
              <h3 className="font-display text-lg sm:text-xl font-medium text-ink mb-1.5 sm:mb-2 group-hover:text-gold transition-colors">
                Sine &amp; Cosine Waves
              </h3>
              <p className="text-xs sm:text-sm text-slate">
                Phase relationship and unit circle connection
              </p>
            </Link>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 sm:py-24 md:py-32 bg-ink text-ivory">
        <div className="max-w-7xl mx-auto px-5 sm:px-6 md:px-12 lg:px-20 text-center">
          <h2 className="font-display text-2xl sm:text-3xl md:text-4xl lg:text-5xl xl:text-6xl font-medium leading-tight mb-6 sm:mb-8">
            Ready to create beautiful<br />math animations?
          </h2>
          <p className="text-base sm:text-lg text-slate-light max-w-xl mx-auto mb-8 sm:mb-10 px-2">
            Join educators and creators using Manimo for pedagogically effective visualizations.
          </p>
          <div className="flex flex-wrap justify-center gap-3 sm:gap-4">
            <SignedOut>
              <SignInButton mode="modal">
                <button className="btn-editorial-primary" style={{ background: 'var(--gold)' }}>
                  <span>Get started free</span>
                  <ArrowIcon className="w-4 h-4" />
                </button>
              </SignInButton>
            </SignedOut>
            <SignedIn>
              <Link href="/dashboard" className="btn-editorial-primary" style={{ background: 'var(--gold)' }}>
                <span>Go to Dashboard</span>
                <ArrowIcon className="w-4 h-4" />
              </Link>
            </SignedIn>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 sm:py-12 bg-ink border-t border-white/10">
        <div className="max-w-7xl mx-auto px-5 sm:px-6 md:px-12 lg:px-20">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 sm:gap-4">
            <p className="font-display text-lg sm:text-xl text-ivory">
              manimo
            </p>
            <p className="text-xs sm:text-sm text-slate-light">
              2025 Manimo. Built for beautiful teaching.
            </p>
          </div>
        </div>
      </footer>
    </main>
  )
}
