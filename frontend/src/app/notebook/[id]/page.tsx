'use client'

import { useAuth } from '@clerk/nextjs'
import { useParams } from 'next/navigation'
import { useState, useEffect, useCallback } from 'react'
import { Play, RefreshCw, AlertCircle } from 'lucide-react'
import { Button } from '@/components/ui'
import Link from 'next/link'

type LoadingState = 'loading' | 'ready' | 'error'

const LOADING_STEPS = [
  { label: 'Creating container', duration: 1500 },
  { label: 'Downloading notebook', duration: 1500 },
  { label: 'Configuring AI assistant', duration: 1500 },
  { label: 'Starting Marimo server', duration: 2000 },
  { label: 'Loading notebook', duration: 2000 },
]

function LoadingScreen() {
  const [currentStep, setCurrentStep] = useState(0)

  useEffect(() => {
    if (currentStep >= LOADING_STEPS.length - 1) return

    const timer = setTimeout(() => {
      setCurrentStep((prev) => Math.min(prev + 1, LOADING_STEPS.length - 1))
    }, LOADING_STEPS[currentStep].duration)

    return () => clearTimeout(timer)
  }, [currentStep])

  const progress = ((currentStep + 1) / LOADING_STEPS.length) * 100
  const isLastStep = currentStep === LOADING_STEPS.length - 1

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-slate-50">
      {/* Grid background */}
      <div
        className="fixed inset-0 opacity-[0.3]"
        style={{
          backgroundImage: `linear-gradient(rgba(148, 163, 184, 0.3) 1px, transparent 1px),
                           linear-gradient(90deg, rgba(148, 163, 184, 0.3) 1px, transparent 1px)`,
          backgroundSize: '48px 48px',
        }}
      />

      <div className="relative flex flex-col items-center gap-8">
        {/* Logo */}
        <div className="flex items-center gap-2.5">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-slate-900">
            <Play className="h-5 w-5 text-white" fill="currentColor" />
          </div>
          <span className="text-xl font-semibold tracking-tight text-slate-900">
            Manimo
          </span>
        </div>

        {/* Loading indicator */}
        <div className="flex flex-col items-center gap-4">
          <div className="relative h-10 w-10">
            <div className="absolute inset-0 rounded-full border-2 border-slate-200" />
            <div
              className="absolute inset-0 animate-spin rounded-full border-2 border-transparent border-t-amber-500"
              style={{ animationDuration: '0.8s' }}
            />
          </div>

          <div className="text-center">
            <p className="text-sm font-medium text-slate-900">
              {LOADING_STEPS[currentStep].label}
            </p>
            <p className="mt-1 text-xs text-slate-500">
              This usually takes a few seconds
            </p>
          </div>
        </div>

        {/* Progress bar */}
        <div className="w-48">
          <div className="h-1 w-full overflow-hidden rounded-full bg-slate-200">
            {isLastStep ? (
              <div className="h-full w-full animate-pulse rounded-full bg-amber-500" />
            ) : (
              <div
                className="h-full rounded-full bg-amber-500 transition-all duration-500 ease-out"
                style={{ width: `${progress}%` }}
              />
            )}
          </div>
          {!isLastStep && (
            <p className="mt-2 text-center text-xs text-slate-400">
              Step {currentStep + 1} of {LOADING_STEPS.length}
            </p>
          )}
        </div>
      </div>
    </div>
  )
}

function ErrorScreen({ message, onRetry }: { message: string; onRetry: () => void }) {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-slate-50">
      {/* Grid background */}
      <div
        className="fixed inset-0 opacity-[0.3]"
        style={{
          backgroundImage: `linear-gradient(rgba(148, 163, 184, 0.3) 1px, transparent 1px),
                           linear-gradient(90deg, rgba(148, 163, 184, 0.3) 1px, transparent 1px)`,
          backgroundSize: '48px 48px',
        }}
      />

      <div className="relative max-w-md text-center">
        <div className="mb-6 flex justify-center">
          <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-red-100">
            <AlertCircle className="h-7 w-7 text-red-600" />
          </div>
        </div>

        <h2 className="text-lg font-semibold text-slate-900">
          Failed to launch notebook
        </h2>
        <p className="mt-2 text-sm text-slate-600">
          {message}
        </p>

        <div className="mt-8 flex items-center justify-center gap-3">
          <Button onClick={onRetry} variant="primary">
            <RefreshCw className="h-4 w-4" />
            Try Again
          </Button>
          <Link href="/dashboard">
            <Button variant="secondary">Back to Dashboard</Button>
          </Link>
        </div>
      </div>
    </div>
  )
}

function AuthRequiredScreen() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-slate-50">
      <div className="text-center">
        <h2 className="text-lg font-semibold text-slate-900">
          Please sign in
        </h2>
        <p className="mt-2 text-sm text-slate-600">
          You need to be signed in to access notebooks.
        </p>
        <div className="mt-6">
          <Link href="/login">
            <Button>Sign In</Button>
          </Link>
        </div>
      </div>
    </div>
  )
}

export default function NotebookPage() {
  const { id } = useParams<{ id: string }>()
  const { userId, isLoaded } = useAuth()
  const [marimoUrl, setMarimoUrl] = useState<string | null>(null)
  const [status, setStatus] = useState<LoadingState>('loading')
  const [iframeLoaded, setIframeLoaded] = useState(false)
  const [errorMessage, setErrorMessage] = useState<string>('')

  const launchNotebook = useCallback(async () => {
    if (!id || !userId) return

    setStatus('loading')
    setIframeLoaded(false)
    setErrorMessage('')

    try {
      const response = await fetch('/api/marimo/launch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ notebook_id: id, user_id: userId }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.error || 'Failed to launch notebook')
      }

      const data = await response.json()
      setMarimoUrl(data.url)
      setStatus('ready')
    } catch (error) {
      console.error('Failed to launch notebook:', error)
      setErrorMessage(error instanceof Error ? error.message : 'Unknown error')
      setStatus('error')
    }
  }, [id, userId])

  useEffect(() => {
    if (isLoaded && userId && id) {
      launchNotebook()
    }
  }, [isLoaded, userId, id, launchNotebook])

  if (!isLoaded) {
    return <LoadingScreen />
  }

  if (!userId) {
    return <AuthRequiredScreen />
  }

  if (status === 'error') {
    return <ErrorScreen message={errorMessage} onRetry={launchNotebook} />
  }

  const showLoading = status === 'loading' || !iframeLoaded

  return (
    <>
      {showLoading && <LoadingScreen />}
      {marimoUrl && (
        <iframe
          src={marimoUrl}
          className={`h-screen w-screen border-0 ${showLoading ? 'hidden' : ''}`}
          allow="clipboard-read; clipboard-write"
          title="Marimo Notebook"
          onLoad={() => setIframeLoaded(true)}
        />
      )}
    </>
  )
}
