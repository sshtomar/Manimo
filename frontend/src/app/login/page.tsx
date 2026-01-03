'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@clerk/nextjs'
import { LoginButton } from '@/components/auth'
import { Play } from 'lucide-react'

export default function LoginPage() {
  const { isLoaded, isSignedIn } = useAuth()
  const router = useRouter()

  // Redirect to dashboard if already signed in
  useEffect(() => {
    if (isLoaded && isSignedIn) {
      router.replace('/dashboard')
    }
  }, [isLoaded, isSignedIn, router])

  // Show loading while checking auth
  if (!isLoaded) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-b from-gray-50 to-white">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-gray-200 border-t-teal-600" />
      </div>
    )
  }

  // Don't render login form if signed in (will redirect)
  if (isSignedIn) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-b from-gray-50 to-white">
        <div className="text-center">
          <div className="h-8 w-8 mx-auto animate-spin rounded-full border-4 border-gray-200 border-t-teal-600" />
          <p className="mt-4 text-gray-600">Redirecting to dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-gray-50 to-white">
      <div className="w-full max-w-sm space-y-8 px-4">
        {/* Logo */}
        <div className="flex flex-col items-center">
          <div className="flex items-center gap-2 mb-2">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-teal-600">
              <Play className="h-5 w-5 text-white" fill="white" />
            </div>
            <span className="text-2xl font-bold text-gray-900">
              Manimo
            </span>
          </div>
          <p className="text-center text-gray-600">
            Create mathematical animations with AI
          </p>
        </div>

        {/* Login Card */}
        <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
          <h1 className="mb-6 text-center text-lg font-semibold text-gray-900">
            Sign in to continue
          </h1>

          <div className="space-y-3">
            <LoginButton provider="google" />
            <LoginButton provider="github" />
          </div>

          <p className="mt-6 text-center text-xs text-gray-500">
            By signing in, you agree to our Terms of Service and Privacy Policy
          </p>
        </div>
      </div>
    </div>
  )
}
