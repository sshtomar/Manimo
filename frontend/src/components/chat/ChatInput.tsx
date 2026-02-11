'use client'

import { useState, useRef, useEffect, KeyboardEvent } from 'react'
import { ArrowUp } from 'lucide-react'

interface ChatInputProps {
  onSend: (message: string) => void
  isLoading?: boolean
  placeholder?: string
}

export function ChatInput({ onSend, isLoading, placeholder = 'Describe your animation...' }: ChatInputProps) {
  const [message, setMessage] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    const textarea = textareaRef.current
    if (textarea) {
      textarea.style.height = 'auto'
      textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`
    }
  }, [message])

  const handleSubmit = () => {
    const trimmed = message.trim()
    if (trimmed && !isLoading) {
      onSend(trimmed)
      setMessage('')
    }
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  const canSubmit = message.trim() && !isLoading

  return (
    <div className="border-t border-slate-200 bg-white p-4">
      <div className="relative">
        <textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={isLoading}
          rows={1}
          className="w-full resize-none rounded-lg border border-slate-200 bg-white py-3 pl-4 pr-12 text-sm text-slate-900 placeholder:text-slate-400 focus:border-amber-500 focus:outline-none focus:ring-2 focus:ring-amber-500/20 disabled:cursor-not-allowed disabled:opacity-50"
        />
        <button
          onClick={handleSubmit}
          disabled={!canSubmit}
          className="absolute bottom-2 right-2 flex h-8 w-8 items-center justify-center rounded-md bg-slate-900 text-white transition-all hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-40"
        >
          {isLoading ? (
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
          ) : (
            <ArrowUp className="h-4 w-4" />
          )}
        </button>
      </div>
      <p className="mt-2 text-xs text-slate-400">
        Enter to send, Shift+Enter for new line
      </p>
    </div>
  )
}
