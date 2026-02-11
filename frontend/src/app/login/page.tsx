'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@clerk/nextjs'
import { LoginButton } from '@/components/auth'
import { Play } from 'lucide-react'
import Link from 'next/link'

function LoadingSpinner() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50">
      <div className="h-5 w-5 rounded-full border-2 border-slate-200 border-t-slate-900 animate-spin" />
    </div>
  )
}

export default function LoginPage() {
  const { isLoaded, isSignedIn } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (isLoaded && isSignedIn) {
      router.replace('/dashboard')
    }
  }, [isLoaded, isSignedIn, router])

  if (!isLoaded) {
    return <LoadingSpinner />
  }

  if (isSignedIn) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center bg-slate-50">
        <div className="text-center">
          <div className="mx-auto h-5 w-5 rounded-full border-2 border-slate-200 border-t-slate-900 animate-spin" />
          <p className="mt-4 text-sm text-slate-500">
            Redirecting to dashboard...
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex min-h-screen flex-col bg-slate-50">
      {/* Grid background */}
      <div
        className="fixed inset-0 opacity-[0.3]"
        style={{
          backgroundImage: `linear-gradient(rgba(148, 163, 184, 0.3) 1px, transparent 1px),
                           linear-gradient(90deg, rgba(148, 163, 184, 0.3) 1px, transparent 1px)`,
          backgroundSize: '48px 48px',
        }}
      />

      <div className="relative flex flex-1 flex-col items-center justify-center px-4">
        <div className="w-full max-w-sm">
          {/* Logo */}
          <div className="mb-8 flex flex-col items-center">
            <Link href="/" className="flex items-center gap-2.5 transition-opacity hover:opacity-80">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-slate-900">
                <Play className="h-5 w-5 text-white" fill="currentColor" />
              </div>
              <span className="text-xl font-semibold tracking-tight text-slate-900">
                Manimo
              </span>
            </Link>
            <p className="mt-3 text-center text-sm text-slate-500">
              Create mathematical animations with AI
            </p>
          </div>

          {/* Login Card */}
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h1 className="mb-6 text-center text-base font-semibold text-slate-900">
              Sign in to continue
            </h1>

            <div className="space-y-3">
              <LoginButton provider="google" />
              <LoginButton provider="github" />
            </div>

            <div className="mt-6 border-t border-slate-100 pt-6">
              <p className="text-center text-xs text-slate-400">
                By signing in, you agree to our{' '}
                <a href="#" className="text-slate-600 hover:underline">
                  Terms
                </a>{' '}
                and{' '}
                <a href="#" className="text-slate-600 hover:underline">
                  Privacy Policy
                </a>
              </p>
            </div>
          </div>

          {/* Back link */}
          <div className="mt-6 text-center">
            <Link
              href="/"
              className="text-sm text-slate-500 transition-colors hover:text-slate-700"
            >
              Back to home
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
