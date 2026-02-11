'use client'

import { useState, useEffect, useRef } from 'react'
import Link from 'next/link'
import { useAuth } from '@clerk/nextjs'
import { ArrowRight, Play, Pause, RotateCcw } from 'lucide-react'

// Animated mathematical curve that morphs between functions
function MathCurve() {
  const [phase, setPhase] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setPhase(p => (p + 0.02) % (Math.PI * 2))
    }, 50)
    return () => clearInterval(interval)
  }, [])

  // Generate smooth curve points
  const generatePath = () => {
    const points: string[] = []
    const width = 400
    const height = 200
    const centerY = height / 2

    for (let i = 0; i <= 100; i++) {
      const x = (i / 100) * width
      const t = (i / 100) * Math.PI * 2

      // Morph between different mathematical functions
      const sine = Math.sin(t + phase) * 60
      const cosine = Math.cos(t * 2 + phase) * 40
      const y = centerY + sine * 0.6 + cosine * 0.4

      if (i === 0) {
        points.push(`M ${x} ${y}`)
      } else {
        points.push(`L ${x} ${y}`)
      }
    }
    return points.join(' ')
  }

  // Generate derivative curve (visual approximation)
  const generateDerivativePath = () => {
    const points: string[] = []
    const width = 400
    const height = 200
    const centerY = height / 2

    for (let i = 0; i <= 100; i++) {
      const x = (i / 100) * width
      const t = (i / 100) * Math.PI * 2

      // Derivative-like curve
      const derivative = Math.cos(t + phase) * 60 * 0.6 - Math.sin(t * 2 + phase) * 40 * 0.4 * 2
      const y = centerY + derivative * 0.5

      if (i === 0) {
        points.push(`M ${x} ${y}`)
      } else {
        points.push(`L ${x} ${y}`)
      }
    }
    return points.join(' ')
  }

  return (
    <svg
      viewBox="0 0 400 200"
      className="w-full h-auto"
      style={{ maxWidth: '500px' }}
    >
      {/* Grid lines */}
      <defs>
        <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
          <path d="M 40 0 L 0 0 0 40" fill="none" stroke="currentColor" strokeWidth="0.5" opacity="0.1"/>
        </pattern>
      </defs>
      <rect width="400" height="200" fill="url(#grid)" />

      {/* Axes */}
      <line x1="0" y1="100" x2="400" y2="100" stroke="currentColor" strokeWidth="1" opacity="0.2"/>
      <line x1="200" y1="0" x2="200" y2="200" stroke="currentColor" strokeWidth="1" opacity="0.2"/>

      {/* Main curve - warm amber */}
      <path
        d={generatePath()}
        fill="none"
        stroke="rgb(245, 158, 11)"
        strokeWidth="3"
        strokeLinecap="round"
        className="drop-shadow-sm"
      />

      {/* Derivative curve - slate blue */}
      <path
        d={generateDerivativePath()}
        fill="none"
        stroke="rgb(100, 116, 139)"
        strokeWidth="2"
        strokeLinecap="round"
        strokeDasharray="8 4"
        opacity="0.7"
      />

      {/* Moving point on curve */}
      <circle
        cx={200 + Math.cos(phase * 2) * 150}
        cy={100 + Math.sin(phase * 2 + phase) * 50}
        r="6"
        fill="rgb(245, 158, 11)"
        className="drop-shadow-md"
      />

      {/* Tangent line at moving point */}
      <line
        x1={200 + Math.cos(phase * 2) * 150 - 30}
        y1={100 + Math.sin(phase * 2 + phase) * 50 - Math.cos(phase * 2 + phase) * 20}
        x2={200 + Math.cos(phase * 2) * 150 + 30}
        y2={100 + Math.sin(phase * 2 + phase) * 50 + Math.cos(phase * 2 + phase) * 20}
        stroke="rgb(239, 68, 68)"
        strokeWidth="2"
        strokeLinecap="round"
        opacity="0.8"
      />
    </svg>
  )
}

// Typing animation for the hero
function TypewriterText({ texts, className }: { texts: string[], className?: string }) {
  const [currentTextIndex, setCurrentTextIndex] = useState(0)
  const [displayText, setDisplayText] = useState('')
  const [isDeleting, setIsDeleting] = useState(false)

  useEffect(() => {
    const currentFullText = texts[currentTextIndex]

    const timeout = setTimeout(() => {
      if (!isDeleting) {
        if (displayText.length < currentFullText.length) {
          setDisplayText(currentFullText.slice(0, displayText.length + 1))
        } else {
          // Wait before deleting
          setTimeout(() => setIsDeleting(true), 2000)
        }
      } else {
        if (displayText.length > 0) {
          setDisplayText(displayText.slice(0, -1))
        } else {
          setIsDeleting(false)
          setCurrentTextIndex((prev) => (prev + 1) % texts.length)
        }
      }
    }, isDeleting ? 30 : 80)

    return () => clearTimeout(timeout)
  }, [displayText, isDeleting, currentTextIndex, texts])

  return (
    <span className={className}>
      {displayText}
      <span className="animate-pulse text-amber-500">|</span>
    </span>
  )
}

// Interactive code demo
function InteractiveDemo() {
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

  const handleClose = () => {
    setShowVideo(false)
    setIsPlaying(false)
    if (videoRef.current) {
      videoRef.current.pause()
    }
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
      <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-2xl">
        <div className="flex items-center justify-between border-b border-slate-100 bg-slate-50 px-4 py-3">
          <span className="font-mono text-xs text-slate-400">Output</span>
          <div className="flex items-center gap-2">
            <button onClick={handleReset} className="p-1.5 text-slate-400 hover:text-slate-600 transition-colors">
              <RotateCcw className="h-4 w-4" />
            </button>
            <button
              onClick={handlePlayPause}
              className="flex items-center justify-center h-7 w-7 rounded-full bg-amber-500 text-white hover:bg-amber-600 transition-colors"
            >
              {isPlaying ? <Pause className="h-3 w-3" fill="currentColor" /> : <Play className="h-3 w-3 ml-0.5" fill="currentColor" />}
            </button>
            <button onClick={handleClose} className="p-1.5 text-slate-400 hover:text-slate-600 transition-colors">
              <span className="text-lg leading-none">&times;</span>
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
    <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-2xl">
      {/* Editor header */}
      <div className="flex items-center justify-between border-b border-slate-100 bg-slate-50 px-4 py-3">
        <div className="flex items-center gap-3">
          <div className="flex gap-1.5">
            <div className="h-3 w-3 rounded-full bg-red-400" />
            <div className="h-3 w-3 rounded-full bg-yellow-400" />
            <div className="h-3 w-3 rounded-full bg-green-400" />
          </div>
          <span className="font-mono text-xs text-slate-400">derivative.py</span>
        </div>
        <button
          onClick={handleRun}
          className="flex items-center gap-2 rounded-lg bg-amber-500 px-4 py-1.5 text-sm font-medium text-white hover:bg-amber-600 transition-colors"
        >
          <Play className="h-3.5 w-3.5" fill="currentColor" />
          Run
        </button>
      </div>

      {/* Code content */}
      <div className="p-6 font-mono text-sm leading-relaxed">
        <div className="text-slate-400 italic"># Describe what you want</div>
        <div className="mt-3 text-slate-800">
          prompt = <span className="text-amber-600">&quot;Animate the derivative of x&sup2;&quot;</span>
        </div>

        <div className="mt-6 text-slate-400 italic"># AI generates production-ready code</div>
        <div className="mt-3 space-y-1 text-slate-700">
          <div>
            <span className="text-purple-600">class</span>{' '}
            <span className="text-blue-600">DerivativeScene</span>
            <span className="text-slate-500">(Scene):</span>
          </div>
          <div className="pl-6">
            <span className="text-purple-600">def</span>{' '}
            <span className="text-amber-600">construct</span>
            <span className="text-slate-500">(self):</span>
          </div>
          <div className="pl-12 text-slate-600">
            axes = Axes(x_range=[<span className="text-blue-600">-3</span>, <span className="text-blue-600">3</span>])
          </div>
          <div className="pl-12 text-slate-600">
            curve = axes.plot(<span className="text-purple-600">lambda</span> x: x**<span className="text-blue-600">2</span>)
          </div>
          <div className="pl-12 text-slate-600">
            tangent = TangentLine(curve, alpha=<span className="text-blue-600">0</span>)
          </div>
          <div className="pl-12 text-slate-600">
            self.play(Create(axes), Create(curve))
          </div>
          <div className="pl-12 text-slate-600">
            self.play(tangent.animate.move_along(curve))
          </div>
        </div>
      </div>
    </div>
  )
}

// Feature component with elegant styling
function Feature({
  number,
  title,
  description
}: {
  number: string
  title: string
  description: string
}) {
  return (
    <div className="group">
      <div className="flex items-start gap-6">
        <span className="font-serif text-5xl font-light text-slate-200 group-hover:text-amber-300 transition-colors">
          {number}
        </span>
        <div>
          <h3 className="text-xl font-semibold text-slate-900">{title}</h3>
          <p className="mt-2 text-slate-600 leading-relaxed">{description}</p>
        </div>
      </div>
    </div>
  )
}

// Testimonial style quote
function Quote({ text, author, role }: { text: string; author: string; role: string }) {
  return (
    <blockquote className="relative">
      <span className="absolute -top-4 -left-2 font-serif text-7xl text-amber-200 select-none">&ldquo;</span>
      <p className="font-serif text-2xl text-slate-700 italic leading-relaxed pl-8">
        {text}
      </p>
      <footer className="mt-6 pl-8">
        <span className="font-medium text-slate-900">{author}</span>
        <span className="text-slate-400 mx-2">&mdash;</span>
        <span className="text-slate-500">{role}</span>
      </footer>
    </blockquote>
  )
}

export default function EditorialLandingPage() {
  const { isSignedIn } = useAuth()
  const ctaHref = isSignedIn ? '/dashboard' : '/login'

  const prompts = [
    'Animate the derivative of x squared',
    'Visualize matrix multiplication',
    'Show Fourier series convergence',
    'Draw a rotating 3D cube',
  ]

  return (
    <div className="min-h-screen bg-[#fefcf9]">
      {/* Subtle paper texture overlay */}
      <div
        className="fixed inset-0 pointer-events-none opacity-30"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`,
        }}
      />

      {/* Navigation */}
      <nav className="relative z-10 border-b border-slate-200/60">
        <div className="mx-auto max-w-6xl px-6 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="flex items-center gap-3 group">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-slate-900 group-hover:bg-amber-500 transition-colors">
                <Play className="h-4 w-4 text-white" fill="currentColor" />
              </div>
              <span className="font-serif text-xl font-semibold text-slate-900">Manimo</span>
            </Link>

            <div className="flex items-center gap-8">
              <Link href="/dashboard" className="text-sm text-slate-600 hover:text-slate-900 transition-colors">
                Dashboard
              </Link>
              <Link href="https://docs.marimo.io" target="_blank" className="text-sm text-slate-600 hover:text-slate-900 transition-colors">
                Documentation
              </Link>
              <Link
                href={ctaHref}
                className="rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800 transition-colors"
              >
                {isSignedIn ? 'Open App' : 'Get Started'}
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative z-10 overflow-hidden">
        <div className="mx-auto max-w-6xl px-6 py-24 lg:py-32">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            {/* Left: Editorial typography */}
            <div className="space-y-8">
              <div className="inline-flex items-center gap-2 rounded-full border border-amber-200 bg-amber-50 px-3 py-1">
                <span className="h-1.5 w-1.5 rounded-full bg-amber-500 animate-pulse" />
                <span className="text-xs font-medium text-amber-700">Mathematical animations, simplified</span>
              </div>

              <h1 className="font-serif text-5xl lg:text-6xl xl:text-7xl font-medium leading-[1.1] text-slate-900">
                Describe.
                <br />
                <span className="text-slate-400">Generate.</span>
                <br />
                <span className="text-amber-500">Animate.</span>
              </h1>

              <p className="text-xl text-slate-600 leading-relaxed max-w-lg">
                Transform natural language into beautiful mathematical animations.
                No installations, no syntax memorization&mdash;just your ideas, rendered in motion.
              </p>

              {/* Animated prompt showcase */}
              <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
                <span className="text-sm text-slate-400 mb-2 block">Try describing:</span>
                <div className="font-mono text-lg text-slate-800">
                  <TypewriterText texts={prompts} />
                </div>
              </div>

              <div className="flex flex-wrap items-center gap-4 pt-4">
                <Link
                  href={ctaHref}
                  className="inline-flex items-center gap-2 rounded-lg bg-amber-500 px-6 py-3 text-base font-medium text-white hover:bg-amber-600 transition-all hover:shadow-lg hover:shadow-amber-500/25"
                >
                  <Play className="h-4 w-4" fill="currentColor" />
                  {isSignedIn ? 'Open Dashboard' : 'Start Creating Free'}
                </Link>
                <Link
                  href="#features"
                  className="inline-flex items-center gap-2 text-slate-600 hover:text-slate-900 transition-colors group"
                >
                  Learn more
                  <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                </Link>
              </div>
            </div>

            {/* Right: Animated mathematical visualization */}
            <div className="relative">
              <div className="absolute -inset-4 bg-gradient-to-br from-amber-100 via-transparent to-slate-100 rounded-3xl opacity-60" />
              <div className="relative bg-white rounded-2xl border border-slate-200 p-8 shadow-xl">
                <div className="text-center mb-6">
                  <span className="text-sm font-medium text-slate-400 uppercase tracking-wider">Live Preview</span>
                </div>
                <MathCurve />
                <div className="flex justify-center gap-8 mt-6 text-sm">
                  <div className="flex items-center gap-2">
                    <span className="h-3 w-3 rounded-full bg-amber-500" />
                    <span className="text-slate-600">f(x)</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="h-3 w-0.5 bg-slate-400" style={{ width: '12px', height: '3px', borderRadius: '2px' }} />
                    <span className="text-slate-600">f&apos;(x)</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="h-3 w-3 rounded-full bg-red-400" />
                    <span className="text-slate-600">tangent</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Interactive Demo Section */}
      <section className="relative z-10 border-t border-slate-200/60 bg-white">
        <div className="mx-auto max-w-6xl px-6 py-24">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div className="order-2 lg:order-1">
              <InteractiveDemo />
            </div>

            <div className="order-1 lg:order-2 space-y-6">
              <h2 className="font-serif text-4xl font-medium text-slate-900">
                From prompt to production
              </h2>
              <p className="text-lg text-slate-600 leading-relaxed">
                Write what you want in plain English. Our AI understands mathematical concepts
                and generates Manim code that follows 3Blue1Brown-style animation principles.
              </p>
              <ul className="space-y-4 text-slate-600">
                <li className="flex items-start gap-3">
                  <span className="mt-1 h-5 w-5 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center text-xs font-bold">1</span>
                  <span>Describe your animation in natural language</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="mt-1 h-5 w-5 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center text-xs font-bold">2</span>
                  <span>AI generates production-ready Manim code</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="mt-1 h-5 w-5 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center text-xs font-bold">3</span>
                  <span>Cloud rendering&mdash;no local setup required</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="relative z-10 border-t border-slate-200/60">
        <div className="mx-auto max-w-6xl px-6 py-24">
          <div className="text-center mb-16">
            <h2 className="font-serif text-4xl font-medium text-slate-900">
              Built for educators and creators
            </h2>
            <p className="mt-4 text-lg text-slate-600 max-w-2xl mx-auto">
              Every feature designed to help you focus on teaching, not debugging.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-12 lg:gap-16">
            <Feature
              number="01"
              title="Reactive Notebooks"
              description="Built on Marimo's reactive runtime. Change a variable and all dependent cells update automatically. No more stale state, no more manual re-runs."
            />
            <Feature
              number="02"
              title="Pure Python Files"
              description="Your notebooks are stored as .py files, not JSON. Git diff works. Code review works. Import functions from one notebook to another."
            />
            <Feature
              number="03"
              title="Cloud Rendering"
              description="Each animation renders in an isolated cloud container with Manim pre-configured. No local installations, no dependency conflicts."
            />
            <Feature
              number="04"
              title="Pedagogical AI"
              description="Our AI doesn't just write code&mdash;it understands animation principles. Proper timing, easing, and visual hierarchy come built-in."
            />
          </div>
        </div>
      </section>

      {/* Testimonial / Philosophy Section */}
      <section className="relative z-10 border-t border-slate-200/60 bg-white">
        <div className="mx-auto max-w-4xl px-6 py-24">
          <Quote
            text="The best mathematical explanations don't just show the answer&mdash;they reveal the thinking. Good animation is the same."
            author="Design Philosophy"
            role="Inspired by 3Blue1Brown"
          />
        </div>
      </section>

      {/* Example Prompts Section */}
      <section className="relative z-10 border-t border-slate-200/60">
        <div className="mx-auto max-w-6xl px-6 py-24">
          <div className="text-center mb-12">
            <h2 className="font-serif text-4xl font-medium text-slate-900">
              What will you create?
            </h2>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {[
              'Visualize the Pythagorean theorem',
              'Animate eigenvalue decomposition',
              'Show Taylor series convergence',
              'Draw a Mandelbrot zoom',
              'Demonstrate integration by parts',
              'Render a 3D surface plot',
            ].map((prompt, i) => (
              <Link
                key={prompt}
                href={ctaHref}
                className="group flex items-center gap-4 rounded-xl border border-slate-200 bg-white p-5 hover:border-amber-300 hover:shadow-lg hover:shadow-amber-100/50 transition-all"
              >
                <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-100 font-mono text-sm text-slate-500 group-hover:bg-amber-100 group-hover:text-amber-600 transition-colors">
                  {i + 1}
                </span>
                <span className="text-slate-700 group-hover:text-slate-900 transition-colors">{prompt}</span>
                <ArrowRight className="ml-auto h-4 w-4 text-slate-300 group-hover:text-amber-500 group-hover:translate-x-1 transition-all" />
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="relative z-10 border-t border-slate-200/60">
        <div className="mx-auto max-w-6xl px-6 py-24">
          <div className="relative overflow-hidden rounded-3xl bg-slate-900 px-8 py-16 lg:px-16 lg:py-24">
            {/* Decorative elements */}
            <div className="absolute top-0 right-0 w-1/2 h-full opacity-10">
              <svg viewBox="0 0 400 400" className="w-full h-full">
                <path
                  d="M 0 200 Q 100 100 200 200 T 400 200"
                  fill="none"
                  stroke="rgb(245, 158, 11)"
                  strokeWidth="2"
                />
                <path
                  d="M 0 250 Q 100 150 200 250 T 400 250"
                  fill="none"
                  stroke="rgb(245, 158, 11)"
                  strokeWidth="1.5"
                  opacity="0.6"
                />
                <path
                  d="M 0 300 Q 100 200 200 300 T 400 300"
                  fill="none"
                  stroke="rgb(245, 158, 11)"
                  strokeWidth="1"
                  opacity="0.3"
                />
              </svg>
            </div>

            <div className="relative z-10 max-w-2xl">
              <h2 className="font-serif text-4xl lg:text-5xl font-medium text-white leading-tight">
                Ready to bring your math to life?
              </h2>
              <p className="mt-6 text-lg text-slate-300 leading-relaxed">
                Join educators and creators making beautiful mathematical animations.
                No credit card required.
              </p>
              <div className="mt-10 flex flex-wrap items-center gap-4">
                <Link
                  href={ctaHref}
                  className="inline-flex items-center gap-2 rounded-lg bg-amber-500 px-6 py-3 text-base font-medium text-white hover:bg-amber-400 transition-colors"
                >
                  <Play className="h-4 w-4" fill="currentColor" />
                  {isSignedIn ? 'Open Dashboard' : 'Start Creating Free'}
                </Link>
                <span className="text-slate-400 text-sm">
                  Free tier includes 10 renders/day
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 border-t border-slate-200/60 bg-white">
        <div className="mx-auto max-w-6xl px-6 py-12">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="flex items-center gap-3">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-900">
                <Play className="h-3.5 w-3.5 text-white" fill="currentColor" />
              </div>
              <span className="font-serif text-lg font-semibold text-slate-900">Manimo</span>
            </div>

            <p className="text-sm text-slate-500">
              Built with <span className="text-amber-500">Marimo</span> &amp; <span className="text-amber-500">Manim</span>
            </p>

            <div className="flex items-center gap-6 text-sm text-slate-500">
              <Link href="/privacy" className="hover:text-slate-900 transition-colors">Privacy</Link>
              <Link href="/terms" className="hover:text-slate-900 transition-colors">Terms</Link>
              <Link href="https://github.com/manimo" target="_blank" className="hover:text-slate-900 transition-colors">GitHub</Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
