'use client'

import Link from 'next/link'
import { useAuth } from '@clerk/nextjs'
import { Header } from '@/components/layout'
import { Button } from '@/components/ui'
import { Play, MessageSquare, Video, Sparkles, ArrowRight } from 'lucide-react'

export default function LandingPage() {
  const { isSignedIn } = useAuth()

  // Where CTAs should link based on auth state
  const ctaHref = isSignedIn ? '/dashboard' : '/login'

  return (
    <div className="flex min-h-screen flex-col">
      <Header />

      <main className="flex-1">
        {/* Hero Section */}
        <section className="relative overflow-hidden grid-lines">
          <div className="mx-auto max-w-7xl px-4 py-24 sm:px-6 sm:py-32 lg:px-8">
            <div className="text-center">
              {/* Badge */}
              <div className="mb-8 inline-flex items-center rounded-full border border-teal-200 bg-teal-50 px-4 py-1.5 text-sm text-teal-700">
                AI-powered mathematical animations
              </div>

              <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl md:text-6xl">
                Bring Your Math Concepts to Life
              </h1>

              <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600 sm:text-xl">
                AI-powered Manim animation—zero setup, full control.
              </p>

              <p className="mx-auto mt-4 max-w-xl text-base text-gray-500">
                Skip the installations and configuration.
                <br className="hidden sm:block" />
                Just type what you want to animate in plain English.
              </p>

              <div className="mt-10">
                <Link href={ctaHref}>
                  <Button size="lg" shadow>
                    {isSignedIn ? 'Go to Dashboard' : 'Get Started Free'}
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Button>
                </Link>
              </div>
            </div>

            {/* Demo Window */}
            <div className="mx-auto mt-16 max-w-5xl">
              <div className="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-2xl">
                {/* Browser chrome */}
                <div className="flex items-center gap-2 border-b border-gray-200 bg-gray-50 px-4 py-3">
                  <div className="flex gap-1.5">
                    <div className="h-3 w-3 rounded-full bg-red-400" />
                    <div className="h-3 w-3 rounded-full bg-yellow-400" />
                    <div className="h-3 w-3 rounded-full bg-green-400" />
                  </div>
                  <div className="ml-4 flex-1">
                    <div className="mx-auto max-w-md rounded-md bg-gray-200 px-3 py-1 text-center text-xs text-gray-500">
                      manimo.app
                    </div>
                  </div>
                </div>
                {/* Demo content placeholder */}
                <div className="aspect-video bg-gradient-to-br from-gray-50 to-gray-100">
                  <div className="flex h-full items-center justify-center">
                    <div className="text-center">
                      <Play className="mx-auto h-16 w-16 text-teal-600/30" />
                      <p className="mt-4 text-sm text-gray-400">Demo video coming soon</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </section>

        {/* How it works */}
        <section className="border-t border-gray-200 bg-gray-50 py-24">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="text-center">
              <h2 className="text-3xl font-bold text-gray-900 sm:text-4xl">
                How it works
              </h2>
              <p className="mt-4 text-lg text-gray-600">
                Three simple steps to create stunning animations
              </p>
            </div>

            <div className="mt-16 grid gap-8 sm:grid-cols-3">
              {/* Step 1 */}
              <div className="card-hover rounded-xl border border-gray-200 bg-white p-8">
                <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-teal-100">
                  <MessageSquare className="h-7 w-7 text-teal-600" />
                </div>
                <h3 className="mt-6 text-xl font-semibold text-gray-900">
                  1. Describe
                </h3>
                <p className="mt-3 text-gray-600">
                  Tell the AI what animation you want in plain English. No coding required.
                </p>
              </div>

              {/* Step 2 */}
              <div className="card-hover rounded-xl border border-gray-200 bg-white p-8">
                <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-indigo-100">
                  <Sparkles className="h-7 w-7 text-indigo-600" />
                </div>
                <h3 className="mt-6 text-xl font-semibold text-gray-900">
                  2. Review
                </h3>
                <p className="mt-3 text-gray-600">
                  AI generates Manim code. Review it, accept, or ask for changes.
                </p>
              </div>

              {/* Step 3 */}
              <div className="card-hover rounded-xl border border-gray-200 bg-white p-8">
                <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-purple-100">
                  <Video className="h-7 w-7 text-purple-600" />
                </div>
                <h3 className="mt-6 text-xl font-semibold text-gray-900">
                  3. Render
                </h3>
                <p className="mt-3 text-gray-600">
                  Render in the cloud. Download and share your video.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Example prompts */}
        <section className="py-24">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="text-center">
              <h2 className="text-3xl font-bold text-gray-900 sm:text-4xl">
                Just describe it
              </h2>
              <p className="mt-4 text-lg text-gray-600">
                See what you can create with simple prompts
              </p>
            </div>

            <div className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {[
                'Create a rotating 3D cube with colored faces',
                'Animate the Pythagorean theorem step by step',
                'Show a sine wave transforming into cosine',
                'Visualize matrix multiplication',
                'Draw a fractal tree growing',
                'Demonstrate the derivative of x²',
              ].map((prompt, i) => (
                <div
                  key={i}
                  className="group cursor-pointer rounded-lg border border-gray-200 bg-white p-4 transition-all hover:border-teal-300 hover:bg-teal-50/50"
                >
                  <p className="text-gray-700">"{prompt}"</p>
                  <div className="mt-2 flex items-center text-sm text-teal-600 opacity-0 transition-opacity group-hover:opacity-100">
                    Try this prompt
                    <ArrowRight className="ml-1 h-4 w-4" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="relative overflow-hidden bg-gray-900 py-24">
          <div className="absolute inset-0 radial-gradient opacity-50" />
          <div className="relative mx-auto max-w-7xl px-4 text-center sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-white sm:text-4xl">
              Ready to create?
            </h2>
            <p className="mt-4 text-lg text-gray-300">
              Join educators and creators making beautiful math animations.
            </p>
            <div className="mt-10">
              <Link href={ctaHref}>
                <Button size="lg" shadow className="bg-teal-500 hover:bg-teal-400 border-teal-600">
                  <Play className="mr-2 h-5 w-5" fill="currentColor" />
                  {isSignedIn ? 'Open Dashboard' : 'Start Creating — it\'s free'}
                </Button>
              </Link>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-white py-12">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">
            <div className="flex items-center gap-2">
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-teal-600">
                <Play className="h-5 w-5 text-white" fill="white" />
              </div>
              <span className="text-lg font-semibold text-gray-900">
                Manimo
              </span>
            </div>
            <p className="text-sm text-gray-500">
              Built with Marimo & Manim
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
