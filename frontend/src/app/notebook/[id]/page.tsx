'use client'

import { useAuth } from '@clerk/nextjs'
import { useParams } from 'next/navigation'
import { useState, useEffect, useCallback } from 'react'

type LoadingState = 'loading' | 'ready' | 'error'

const LOADING_MESSAGES = [
  'Creating container...',
  'Downloading notebook...',
  'Configuring AI...',
  'Starting Marimo server...',
  'Loading notebook...',
]

function LoadingSpinner({ messages }: { messages: string[] }) {
  const [currentIndex, setCurrentIndex] = useState(0)

  useEffect(() => {
    if (currentIndex >= messages.length - 1) return

    const timer = setInterval(() => {
      setCurrentIndex((prev) => Math.min(prev + 1, messages.length - 1))
    }, 1500)

    return () => clearInterval(timer)
  }, [currentIndex, messages.length])

  const isLastStep = currentIndex === messages.length - 1

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-50 grid-lines">
      <div className="flex flex-col items-center gap-8">
        {/* Spinner */}
        <div className="relative h-12 w-12">
          <div className="absolute inset-0 rounded-full border-2 border-gray-200" />
          <div
            className="absolute inset-0 rounded-full border-2 border-transparent border-t-teal-600 animate-spin"
            style={{ animationDuration: '0.8s' }}
          />
        </div>

        {/* Message */}
        <div className="text-center">
          <p className="text-lg font-medium text-gray-900">
            {messages[currentIndex]}
          </p>
          <p className="mt-2 text-sm text-gray-500">
            This usually takes a few seconds
          </p>
        </div>

        {/* Progress bar */}
        <div className="w-48">
          <div className="h-1 w-full rounded-full bg-gray-200 overflow-hidden">
            {isLastStep ? (
              <div className="h-full w-full bg-teal-600 rounded-full animate-pulse" />
            ) : (
              <div
                className="h-full bg-teal-600 rounded-full transition-all duration-500 ease-out"
                style={{ width: `${((currentIndex + 1) / messages.length) * 100}%` }}
              />
            )}
          </div>
          {!isLastStep && (
            <p className="mt-2 text-center text-xs text-gray-400">
              {currentIndex + 1} of {messages.length}
            </p>
          )}
        </div>
      </div>
    </div>
  )
}

function ErrorDisplay({ message, onRetry }: { message: string; onRetry: () => void }) {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-50">
      <div className="max-w-md text-center">
        <div className="mb-4 text-6xl">😵</div>
        <h2 className="mb-2 text-xl font-semibold text-gray-900">
          Failed to launch notebook
        </h2>
        <p className="mb-6 text-gray-600">{message}</p>
        <button
          onClick={onRetry}
          className="rounded-lg bg-blue-600 px-6 py-3 font-medium text-white transition-colors hover:bg-blue-700"
        >
          Try Again
        </button>
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

  // Auth loading state
  if (!isLoaded) {
    return <LoadingSpinner messages={['Authenticating...']} />
  }

  // Not authenticated
  if (!userId) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center bg-gray-50">
        <div className="text-center">
          <h2 className="mb-2 text-xl font-semibold text-gray-900">
            Please sign in
          </h2>
          <p className="text-gray-600">
            You need to be signed in to access notebooks.
          </p>
        </div>
      </div>
    )
  }

  // Error state
  if (status === 'error') {
    return <ErrorDisplay message={errorMessage} onRetry={launchNotebook} />
  }

  // Show loading spinner until iframe is fully loaded
  // Render iframe hidden in background so it can load while spinner shows
  const showLoading = status === 'loading' || !iframeLoaded

  return (
    <>
      {showLoading && <LoadingSpinner messages={LOADING_MESSAGES} />}
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
