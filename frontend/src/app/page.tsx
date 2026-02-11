'use client'

import { useState, useRef } from 'react'
import Link from 'next/link'
import { useAuth } from '@clerk/nextjs'
import { Header } from '@/components/layout'
import { Button } from '@/components/ui'
import { ArrowRight, Sparkles, Zap, Cloud, Code2, Play, X, RotateCcw, Pause } from 'lucide-react'

// Animated code block for hero with Run button
function CodePreview() {
  const [showVideo, setShowVideo] = useState(false)
  const [isPlaying, setIsPlaying] = useState(false)
  const videoRef = useRef<HTMLVideoElement>(null)

  const handleRun = () => {
    setShowVideo(true)
    setIsPlaying(true)
    // Small delay to ensure video element is mounted
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

  const handleVideoEnd = () => {
    setIsPlaying(false)
  }

  if (showVideo) {
    return (
      <div className="relative overflow-hidden rounded-lg border border-slate-200 bg-slate-100 shadow-sm">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-200 bg-slate-50 px-4 py-2.5">
          <div className="flex items-center gap-3">
            <span className="font-mono text-[11px] text-slate-500">visualization</span>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={handleReset}
              className="flex h-6 w-6 items-center justify-center rounded text-slate-500 transition-colors hover:bg-slate-200 hover:text-slate-700"
              title="Restart"
            >
              <RotateCcw className="h-3.5 w-3.5" />
            </button>
            <button
              onClick={handlePlayPause}
              className="flex h-6 w-6 items-center justify-center rounded bg-amber-500 text-white transition-colors hover:bg-amber-600"
              title={isPlaying ? 'Pause' : 'Play'}
            >
              {isPlaying ? (
                <Pause className="h-3 w-3" fill="currentColor" />
              ) : (
                <Play className="h-3 w-3 ml-0.5" fill="currentColor" />
              )}
            </button>
            <button
              onClick={handleClose}
              className="flex h-6 w-6 items-center justify-center rounded text-slate-500 transition-colors hover:bg-slate-200 hover:text-slate-700"
              title="Back to code"
            >
              <X className="h-3.5 w-3.5" />
            </button>
          </div>
        </div>

        {/* Video */}
        <video
          ref={videoRef}
          src="/videos/derivative_demo.mp4"
          className="w-full"
          playsInline
          onEnded={handleVideoEnd}
        />
      </div>
    )
  }

  return (
    <div className="relative overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm">
      {/* Window chrome */}
      <div className="relative z-10 flex items-center gap-2 border-b border-slate-200 bg-slate-50 px-4 py-2.5">
        <div className="flex gap-1.5">
          <div className="h-2.5 w-2.5 rounded-full bg-slate-300" />
          <div className="h-2.5 w-2.5 rounded-full bg-slate-300" />
          <div className="h-2.5 w-2.5 rounded-full bg-slate-300" />
        </div>
        <div className="flex-1 text-center">
          <span className="font-mono text-[11px] text-slate-400">notebook.py</span>
        </div>
        {/* Run button */}
        <button
          onClick={handleRun}
          className="flex items-center gap-1.5 rounded-md bg-amber-500 px-2.5 py-1 text-[11px] font-medium text-white transition-colors hover:bg-amber-600"
        >
          <Play className="h-3 w-3" fill="currentColor" />
          Run
        </button>
      </div>

      {/* Code content */}
      <div className="p-4 font-mono text-[13px] leading-relaxed">
        <div className="text-slate-500"># Your prompt</div>
        <div className="mt-2 text-slate-700">
          <span className="text-amber-600">&quot;</span>
          <span>Animate the derivative of x</span>
          <span className="text-amber-600">&sup2;</span>
          <span className="text-amber-600">&quot;</span>
        </div>
        <div className="mt-4 text-slate-500"># AI generates</div>
        <div className="mt-2 space-y-1">
          <div>
            <span className="text-purple-600">class</span>
            <span className="text-slate-700"> DerivativeScene(Scene):</span>
          </div>
          <div className="pl-4">
            <span className="text-purple-600">def</span>
            <span className="text-blue-600"> construct</span>
            <span className="text-slate-700">(self):</span>
          </div>
          <div className="pl-8 text-slate-700">
            axes = Axes(...)
          </div>
          <div className="pl-8 text-slate-700">
            graph = axes.plot(<span className="text-amber-600">lambda</span> x: x**2)
          </div>
          <div className="pl-8 text-slate-700">
            self.play(Create(axes), Create(graph))
          </div>
        </div>
      </div>

      {/* Gradient overlay */}
      <div className="absolute inset-x-0 bottom-0 h-12 bg-gradient-to-t from-white" />
    </div>
  )
}

// Feature card component
function FeatureCard({
  icon: Icon,
  title,
  description,
  delay,
}: {
  icon: React.ElementType
  title: string
  description: string
  delay: number
}) {
  return (
    <div
      className="group relative rounded-lg border border-slate-200 bg-white p-6 transition-all duration-200 hover:border-slate-300 hover:shadow-sm"
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className="mb-4 flex h-10 w-10 items-center justify-center rounded-lg bg-slate-100 text-slate-600 transition-colors group-hover:bg-amber-100 group-hover:text-amber-600">
        <Icon className="h-5 w-5" />
      </div>
      <h3 className="text-[15px] font-semibold text-slate-900">
        {title}
      </h3>
      <p className="mt-2 text-sm leading-relaxed text-slate-600">
        {description}
      </p>
    </div>
  )
}

// Example prompt component
function ExamplePrompt({ text, index }: { text: string; index: number }) {
  return (
    <button
      className="group flex items-center gap-3 rounded-lg border border-slate-200 bg-white px-4 py-3 text-left transition-all duration-150 hover:border-amber-300 hover:bg-amber-50/50"
      style={{ animationDelay: `${index * 50}ms` }}
    >
      <span className="flex h-6 w-6 flex-shrink-0 items-center justify-center rounded bg-slate-100 font-mono text-xs text-slate-500">
        {index + 1}
      </span>
      <span className="text-sm text-slate-700">{text}</span>
      <ArrowRight className="ml-auto h-4 w-4 text-slate-400 opacity-0 transition-all group-hover:translate-x-0.5 group-hover:text-amber-500 group-hover:opacity-100" />
    </button>
  )
}

export default function LandingPage() {
  const { isSignedIn } = useAuth()
  const ctaHref = isSignedIn ? '/dashboard' : '/login'

  const features = [
    {
      icon: Sparkles,
      title: 'Natural language to code',
      description:
        'Describe your animation in plain English. AI generates production-ready Manim code instantly.',
    },
    {
      icon: Zap,
      title: 'Reactive notebooks',
      description:
        'Built on Marimo. Change a variable and dependent cells update automatically. No stale state.',
    },
    {
      icon: Cloud,
      title: 'Cloud rendering',
      description:
        'No local setup required. Each render runs in an isolated container with Manim pre-configured.',
    },
    {
      icon: Code2,
      title: 'Pure Python files',
      description:
        'Notebooks stored as .py files, not JSON. Version control and code review work as expected.',
    },
  ]

  const examplePrompts = [
    'Create a rotating 3D cube with colored faces',
    'Animate the Pythagorean theorem step by step',
    'Show a sine wave transforming into cosine',
    'Visualize matrix multiplication',
    'Draw a fractal tree growing',
    'Demonstrate the derivative of x squared',
  ]

  return (
    <div className="flex min-h-screen flex-col bg-white">
      <Header />

      <main className="flex-1">
        {/* Hero Section */}
        <section className="relative overflow-hidden">
          {/* Background gradient */}
          <div className="absolute inset-0 bg-gradient-to-b from-slate-50 to-white" />

          {/* Grid pattern */}
          <div
            className="absolute inset-0 opacity-[0.4]"
            style={{
              backgroundImage: `linear-gradient(rgba(148, 163, 184, 0.3) 1px, transparent 1px),
                               linear-gradient(90deg, rgba(148, 163, 184, 0.3) 1px, transparent 1px)`,
              backgroundSize: '64px 64px',
            }}
          />

          <div className="relative mx-auto max-w-7xl px-4 py-20 sm:px-6 sm:py-28 lg:px-8 lg:py-32">
            <div className="grid gap-12 lg:grid-cols-2 lg:gap-16">
              {/* Left: Copy */}
              <div className="flex flex-col justify-center">
                {/* Badge */}
                <div className="mb-6 inline-flex w-fit items-center gap-2 rounded-full border border-amber-200 bg-amber-50 px-3 py-1 text-[13px] font-medium text-amber-700">
                  <span className="flex h-1.5 w-1.5 rounded-full bg-amber-500" />
                  AI-powered mathematical animations
                </div>

                {/* Headline */}
                <h1 className="text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl lg:text-[3.5rem] lg:leading-[1.1]">
                  Bring math to life
                  <br />
                  <span className="text-slate-500">
                    with natural language
                  </span>
                </h1>

                {/* Subhead */}
                <p className="mt-6 max-w-lg text-lg leading-relaxed text-slate-600">
                  Skip the installations. Just describe what you want to animate
                  in plain English and let AI write the Manim code.
                </p>

                {/* CTA */}
                <div className="mt-10 flex flex-wrap items-center gap-4">
                  <Link href={ctaHref}>
                    <Button size="lg" variant="accent">
                      <Play className="h-4 w-4" fill="currentColor" />
                      {isSignedIn ? 'Open Dashboard' : 'Get Started Free'}
                    </Button>
                  </Link>
                  <Link
                    href="https://docs.marimo.io"
                    target="_blank"
                    className="text-sm font-medium text-slate-600 transition-colors hover:text-slate-900"
                  >
                    Read the docs
                    <ArrowRight className="ml-1 inline-block h-4 w-4" />
                  </Link>
                </div>

                {/* Social proof placeholder */}
                <div className="mt-12 flex items-center gap-4 text-sm text-slate-500">
                  <div className="flex -space-x-2">
                    {[...Array(4)].map((_, i) => (
                      <div
                        key={i}
                        className="h-8 w-8 rounded-full border-2 border-white bg-slate-200"
                      />
                    ))}
                  </div>
                  <span>Join 500+ educators and creators</span>
                </div>
              </div>

              {/* Right: Code preview */}
              <div className="relative lg:pl-8">
                <div className="relative z-10">
                  <CodePreview />
                </div>
                {/* Decorative element */}
                <div className="pointer-events-none absolute -right-4 -top-4 h-24 w-24 rounded-full bg-amber-200/30 blur-3xl" />
                <div className="pointer-events-none absolute -bottom-8 -left-8 h-32 w-32 rounded-full bg-slate-200/50 blur-3xl" />
              </div>
            </div>
          </div>
        </section>

        {/* See it in action - Conversational workflow */}
        <section className="border-t border-slate-200 py-20 sm:py-24">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl">
                See it in action
              </h2>
              <p className="mx-auto mt-4 max-w-2xl text-base text-slate-600">
                From idea to polished animation through conversation
              </p>
            </div>

            {/* Examples with alternating layout */}
            <div className="space-y-20 lg:space-y-28">

              {/* Example 1: Start from an idea */}
              <div className="grid gap-10 lg:grid-cols-2 lg:gap-16 items-center">
                {/* Content */}
                <div>
                  <div className="font-mono text-xs font-semibold text-amber-600 tracking-wide mb-3">
                    01 / START FROM AN IDEA
                  </div>
                  <h3 className="text-2xl font-bold text-slate-900 mb-4">
                    Describe what you want to see.
                  </h3>
                  <p className="text-base text-slate-600 mb-6 leading-relaxed">
                    No need to memorize Manim syntax. Just tell our AI what concept you want to visualize, and it generates the code for you. Perfect for educators and learners alike.
                  </p>
                  <ul className="space-y-3">
                    <li className="flex items-start gap-3 text-sm text-slate-700">
                      <svg className="h-5 w-5 text-amber-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round"/></svg>
                      Natural language to animation
                    </li>
                    <li className="flex items-start gap-3 text-sm text-slate-700">
                      <svg className="h-5 w-5 text-amber-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round"/></svg>
                      Understands mathematical concepts deeply
                    </li>
                    <li className="flex items-start gap-3 text-sm text-slate-700">
                      <svg className="h-5 w-5 text-amber-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round"/></svg>
                      Generates production-ready Manim code
                    </li>
                  </ul>
                </div>

                {/* Chat window */}
                <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-lg transition-all duration-300 hover:shadow-xl hover:-translate-y-1">
                  <div className="flex items-center gap-3 border-b border-slate-100 bg-slate-50 px-4 py-3">
                    <div className="flex gap-1.5">
                      <div className="h-2.5 w-2.5 rounded-full bg-slate-300" />
                      <div className="h-2.5 w-2.5 rounded-full bg-slate-300" />
                      <div className="h-2.5 w-2.5 rounded-full bg-slate-300" />
                    </div>
                    <span className="font-mono text-xs text-slate-500">AI Assistant</span>
                  </div>
                  <div className="p-4 space-y-4">
                    <div className="rounded-lg bg-amber-50 border border-amber-200 p-3">
                      <div className="mb-2 flex h-6 w-6 items-center justify-center rounded bg-amber-500 text-xs font-bold text-white">U</div>
                      <p className="text-sm text-slate-700">Show me how a 2x2 matrix transforms the unit square. I want to see the basis vectors move.</p>
                    </div>
                    <div className="rounded-lg bg-slate-50 border border-slate-200 p-3">
                      <div className="mb-2 flex h-6 w-6 items-center justify-center rounded bg-slate-900 text-xs font-bold text-white">M</div>
                      <p className="text-sm text-slate-600 mb-3">I&apos;ll create a visualization showing the unit square transforming under a shear matrix, highlighting how the basis vectors i-hat and j-hat change:</p>
                      <div className="rounded-md bg-slate-100 border border-slate-200 p-3 font-mono text-xs text-slate-700">
                        <div><span className="text-slate-400"># Shear transformation</span></div>
                        <div>matrix = [[<span className="text-blue-600">1</span>, <span className="text-blue-600">1</span>], [<span className="text-blue-600">0</span>, <span className="text-blue-600">1</span>]]</div>
                        <div>self.play(</div>
                        <div className="pl-4">plane.animate.apply_matrix(matrix),</div>
                        <div className="pl-4">i_hat.animate.put_start_and_end_on(</div>
                        <div className="pl-8">ORIGIN, [<span className="text-blue-600">1</span>, <span className="text-blue-600">0</span>, <span className="text-blue-600">0</span>]),</div>
                        <div className="pl-4">j_hat.animate.put_start_and_end_on(</div>
                        <div className="pl-8">ORIGIN, [<span className="text-blue-600">1</span>, <span className="text-blue-600">1</span>, <span className="text-blue-600">0</span>])</div>
                        <div>)</div>
                      </div>
                      <p className="text-xs text-slate-500 mt-3">Notice how <code className="bg-slate-200 px-1.5 py-0.5 rounded">j-hat</code> slides along while <code className="bg-slate-200 px-1.5 py-0.5 rounded">i-hat</code> stays fixed. This is the essence of a shear transformation.</p>
                    </div>
                    <div className="rounded-lg border border-slate-200 bg-slate-50 px-4 py-2.5">
                      <span className="text-sm text-slate-400">Describe the visualization you want...</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Example 2: Get expert help - REVERSED */}
              <div className="grid gap-10 lg:grid-cols-2 lg:gap-16 items-center">
                {/* Chat window - first on mobile, second on desktop */}
                <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-lg transition-all duration-300 hover:shadow-xl hover:-translate-y-1 lg:order-2">
                  <div className="flex items-center gap-3 border-b border-slate-100 bg-slate-50 px-4 py-3">
                    <div className="flex gap-1.5">
                      <div className="h-2.5 w-2.5 rounded-full bg-slate-300" />
                      <div className="h-2.5 w-2.5 rounded-full bg-slate-300" />
                      <div className="h-2.5 w-2.5 rounded-full bg-slate-300" />
                    </div>
                    <span className="font-mono text-xs text-slate-500">AI Assistant</span>
                  </div>
                  <div className="p-4 space-y-4">
                    <div className="rounded-lg bg-amber-50 border border-amber-200 p-3">
                      <div className="mb-2 flex h-6 w-6 items-center justify-center rounded bg-amber-500 text-xs font-bold text-white">U</div>
                      <p className="text-sm text-slate-700">How do I make the tangent line animation smoother?</p>
                    </div>
                    <div className="rounded-lg bg-slate-50 border border-slate-200 p-3">
                      <div className="mb-2 flex h-6 w-6 items-center justify-center rounded bg-slate-900 text-xs font-bold text-white">M</div>
                      <p className="text-sm text-slate-600 mb-3">The jerkiness comes from linear interpolation. Use <strong>rate_func</strong> to add easing:</p>
                      <div className="rounded-md bg-slate-100 border border-slate-200 p-3 font-mono text-xs text-slate-700">
                        <div><span className="text-slate-400"># Smooth easing</span></div>
                        <div>self.play(</div>
                        <div className="pl-4">t.animate.set_value(<span className="text-blue-600">2</span>),</div>
                        <div className="pl-4">run_time=<span className="text-blue-600">4</span>,</div>
                        <div className="pl-4">rate_func=<span className="text-amber-600">smooth</span></div>
                        <div>)</div>
                      </div>
                      <p className="text-xs text-slate-500 mt-3"><strong>Pro tip:</strong> <code className="bg-slate-200 px-1.5 py-0.5 rounded">smooth</code> gives viewers time to process what they&apos;re seeing at the start and end of animations.</p>
                    </div>
                    <div className="rounded-lg border border-slate-200 bg-slate-50 px-4 py-2.5">
                      <span className="text-sm text-slate-400">Ask about animation techniques...</span>
                    </div>
                  </div>
                </div>

                {/* Content */}
                <div className="lg:order-1">
                  <div className="font-mono text-xs font-semibold text-amber-600 tracking-wide mb-3">
                    02 / GET EXPERT HELP
                  </div>
                  <h3 className="text-2xl font-bold text-slate-900 mb-4">
                    Get help from an expert.
                  </h3>
                  <p className="text-base text-slate-600 mb-6 leading-relaxed">
                    Stuck on an animation? Our AI assistant understands Manim deeply. Ask it anything — from basic syntax to advanced techniques inspired by 3Blue1Brown&apos;s style.
                  </p>
                  <ul className="space-y-3">
                    <li className="flex items-start gap-3 text-sm text-slate-700">
                      <svg className="h-5 w-5 text-amber-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round"/></svg>
                      Contextual code suggestions
                    </li>
                    <li className="flex items-start gap-3 text-sm text-slate-700">
                      <svg className="h-5 w-5 text-amber-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round"/></svg>
                      Explains the &quot;why&quot; behind techniques
                    </li>
                    <li className="flex items-start gap-3 text-sm text-slate-700">
                      <svg className="h-5 w-5 text-amber-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round"/></svg>
                      Learns from 3Blue1Brown patterns
                    </li>
                  </ul>
                </div>
              </div>

              {/* Example 3: Refine until perfect */}
              <div className="grid gap-10 lg:grid-cols-2 lg:gap-16 items-center">
                {/* Content */}
                <div>
                  <div className="font-mono text-xs font-semibold text-amber-600 tracking-wide mb-3">
                    03 / REFINE UNTIL PERFECT
                  </div>
                  <h3 className="text-2xl font-bold text-slate-900 mb-4">
                    Iterate until it clicks.
                  </h3>
                  <p className="text-base text-slate-600 mb-6 leading-relaxed">
                    Keep refining your visualization through conversation. Add labels, adjust colors, change timing — the AI understands your intent and applies changes intelligently across your entire scene.
                  </p>
                  <ul className="space-y-3">
                    <li className="flex items-start gap-3 text-sm text-slate-700">
                      <svg className="h-5 w-5 text-amber-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round"/></svg>
                      Remembers context from previous requests
                    </li>
                    <li className="flex items-start gap-3 text-sm text-slate-700">
                      <svg className="h-5 w-5 text-amber-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round"/></svg>
                      Suggests improvements proactively
                    </li>
                    <li className="flex items-start gap-3 text-sm text-slate-700">
                      <svg className="h-5 w-5 text-amber-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round"/></svg>
                      Renders changes instantly
                    </li>
                  </ul>
                </div>

                {/* Chat window */}
                <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-lg transition-all duration-300 hover:shadow-xl hover:-translate-y-1">
                  <div className="flex items-center gap-3 border-b border-slate-100 bg-slate-50 px-4 py-3">
                    <div className="flex gap-1.5">
                      <div className="h-2.5 w-2.5 rounded-full bg-slate-300" />
                      <div className="h-2.5 w-2.5 rounded-full bg-slate-300" />
                      <div className="h-2.5 w-2.5 rounded-full bg-slate-300" />
                    </div>
                    <span className="font-mono text-xs text-slate-500">AI Assistant</span>
                  </div>
                  <div className="p-4 space-y-4">
                    <div className="rounded-lg bg-amber-50 border border-amber-200 p-3">
                      <div className="mb-2 flex h-6 w-6 items-center justify-center rounded bg-amber-500 text-xs font-bold text-white">U</div>
                      <p className="text-sm text-slate-700">The Riemann sum rectangles are hard to see. Can you make them more distinct and add a label showing the area converging?</p>
                    </div>
                    <div className="rounded-lg bg-slate-50 border border-slate-200 p-3">
                      <div className="mb-2 flex h-6 w-6 items-center justify-center rounded bg-slate-900 text-xs font-bold text-white">M</div>
                      <p className="text-sm text-slate-600 mb-3">I&apos;ll increase the rectangle opacity, add borders, and animate an area label that updates as we add more rectangles:</p>
                      <div className="rounded-md bg-slate-100 border border-slate-200 p-3 font-mono text-xs text-slate-700">
                        <div><span className="text-slate-400"># Distinct rectangles with borders</span></div>
                        <div>rects = axes.get_riemann_rectangles(</div>
                        <div className="pl-4">graph, dx=<span className="text-blue-600">0.25</span>,</div>
                        <div className="pl-4">stroke_width=<span className="text-blue-600">2</span>,</div>
                        <div className="pl-4">stroke_color=WHITE,</div>
                        <div className="pl-4">fill_opacity=<span className="text-blue-600">0.7</span></div>
                        <div>)</div>
                        <div className="mt-1"><span className="text-slate-400"># Live area counter</span></div>
                        <div>area_label = always_redraw(<span className="text-purple-600">lambda</span>:</div>
                        <div className="pl-4">Text(<span className="text-green-600">f&quot;Area ≈ &#123;sum:.2f&#125;&quot;</span>)</div>
                        <div>)</div>
                      </div>
                      <p className="text-xs text-slate-500 mt-3">The <code className="bg-slate-200 px-1.5 py-0.5 rounded">always_redraw</code> pattern keeps your label in sync with the animation automatically. Want me to also add grid lines?</p>
                    </div>
                    <div className="rounded-lg border border-slate-200 bg-slate-50 px-4 py-2.5">
                      <span className="text-sm text-slate-400">Keep refining your visualization...</span>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </section>

        {/* Example prompts Section */}
        <section className="py-20 sm:py-24">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="mx-auto max-w-2xl text-center">
              <h2 className="text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl">
                Just describe it
              </h2>
              <p className="mt-4 text-base text-slate-600">
                Try these example prompts to see what you can create
              </p>
            </div>

            <div className="mx-auto mt-10 grid max-w-3xl gap-3 sm:grid-cols-2">
              {examplePrompts.map((prompt, i) => (
                <ExamplePrompt key={prompt} text={prompt} index={i} />
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="border-t border-slate-200">
          <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 sm:py-24 lg:px-8">
            <div className="relative overflow-hidden rounded-2xl bg-slate-900 px-6 py-16 text-center sm:px-12 sm:py-20">
              {/* Background pattern */}
              <div
                className="absolute inset-0 opacity-10"
                style={{
                  backgroundImage: `radial-gradient(circle at 25% 25%, rgba(251, 191, 36, 0.4) 0%, transparent 50%),
                                   radial-gradient(circle at 75% 75%, rgba(251, 191, 36, 0.3) 0%, transparent 50%)`,
                }}
              />

              <div className="relative">
                <h2 className="text-2xl font-bold tracking-tight text-white sm:text-3xl">
                  Ready to create?
                </h2>
                <p className="mx-auto mt-4 max-w-xl text-base text-slate-300">
                  Join educators and creators making beautiful math animations.
                  No credit card required.
                </p>
                <div className="mt-8">
                  <Link href={ctaHref}>
                    <Button size="lg" variant="accent">
                      <Play className="h-4 w-4" fill="currentColor" />
                      {isSignedIn ? 'Open Dashboard' : 'Start Creating Free'}
                    </Button>
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-white py-8">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">
            <div className="flex items-center gap-2">
              <div className="flex h-7 w-7 items-center justify-center rounded-md bg-slate-900">
                <Play className="h-3.5 w-3.5 text-white" fill="currentColor" />
              </div>
              <span className="text-sm font-semibold text-slate-900">
                Manimo
              </span>
            </div>
            <p className="text-sm text-slate-500">
              Built with Marimo & Manim
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
