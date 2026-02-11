'use client'

import { useEffect, useRef } from 'react'
import { ChatMessage } from './ChatMessage'
import { ChatInput } from './ChatInput'
import { useChatStore } from '@/stores'
import { Sparkles } from 'lucide-react'

interface ChatContainerProps {
  notebookId: string
  userId: string
  onOpenMarimo?: () => void
}

export function ChatContainer({ notebookId, userId, onOpenMarimo }: ChatContainerProps) {
  const { messages, isGenerating, sendMessage, applyDiff, rejectDiff } = useChatStore()
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const applyingRef = useRef<string | null>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = (prompt: string) => {
    sendMessage(notebookId, userId, prompt)
  }

  const handleApply = async (messageId: string, prompt: string) => {
    applyingRef.current = messageId
    try {
      await applyDiff(messageId, notebookId, userId, prompt)
    } finally {
      applyingRef.current = null
    }
  }

  const suggestions = [
    'Create a rotating 3D cube',
    'Animate the Pythagorean theorem',
    'Show a sine wave transforming into a cosine wave',
  ]

  return (
    <div className="flex h-full flex-col bg-white">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-4">
        {messages.length === 0 ? (
          <div className="flex h-full flex-col items-center justify-center text-center">
            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-amber-100">
              <Sparkles className="h-6 w-6 text-amber-600" />
            </div>
            <h3 className="text-base font-semibold text-slate-900">
              Describe your animation
            </h3>
            <p className="mt-2 max-w-sm text-sm text-slate-500">
              Tell me what mathematical animation you'd like to create, and I'll generate the Manim code for you.
            </p>

            {/* Suggestions */}
            <div className="mt-8 w-full max-w-sm space-y-2">
              <p className="text-[11px] font-medium uppercase tracking-wide text-slate-400">
                Try asking
              </p>
              <div className="space-y-2">
                {suggestions.map((suggestion) => (
                  <button
                    key={suggestion}
                    onClick={() => handleSend(suggestion)}
                    className="block w-full rounded-lg border border-slate-200 bg-white px-3 py-2.5 text-left text-sm text-slate-700 transition-all hover:border-slate-300 hover:bg-slate-50"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {messages.map((message) => {
              const userPrompt = messages
                .slice(0, messages.indexOf(message))
                .reverse()
                .find((m) => m.role === 'user')?.content || ''

              return (
                <ChatMessage
                  key={message.id}
                  message={message}
                  onApply={() => handleApply(message.id, userPrompt)}
                  onReject={() => rejectDiff(message.id)}
                  onOpenMarimo={onOpenMarimo}
                  isApplying={applyingRef.current === message.id}
                />
              )
            })}

            {/* Loading indicator */}
            {isGenerating && (
              <div className="flex items-center gap-3">
                <div className="flex h-7 w-7 items-center justify-center rounded-md bg-amber-100">
                  <div className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-amber-600 border-t-transparent" />
                </div>
                <span className="text-sm text-slate-500">
                  Generating code...
                </span>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input */}
      <ChatInput onSend={handleSend} isLoading={isGenerating} />
    </div>
  )
}
