'use client'

import { useEffect, useRef } from 'react'
import { ChatMessage } from './ChatMessage'
import { ChatInput } from './ChatInput'
import { Spinner } from '@/components/ui'
import { useChatStore } from '@/stores'
import { MessageSquare } from 'lucide-react'

interface ChatContainerProps {
  notebookId: string
  userId: string
  onOpenMarimo?: () => void
}

export function ChatContainer({ notebookId, userId, onOpenMarimo }: ChatContainerProps) {
  const { messages, isGenerating, sendMessage, applyDiff, rejectDiff } = useChatStore()
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const applyingRef = useRef<string | null>(null)

  // Auto-scroll to bottom on new messages
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

  return (
    <div className="flex h-full flex-col">
      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-4">
        {messages.length === 0 ? (
          <div className="flex h-full flex-col items-center justify-center text-center">
            <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-teal-100">
              <MessageSquare className="h-8 w-8 text-teal-600" />
            </div>
            <h3 className="text-lg font-medium text-gray-900">
              Describe your animation
            </h3>
            <p className="mt-2 max-w-sm text-sm text-gray-500">
              Tell me what mathematical animation you'd like to create, and I'll generate the Manim code for you.
            </p>
            <div className="mt-6 space-y-2 text-left">
              <p className="text-xs font-medium text-gray-500 uppercase">
                Try asking:
              </p>
              <div className="space-y-1">
                {[
                  'Create a rotating 3D cube',
                  'Animate the Pythagorean theorem',
                  'Show a sine wave transforming into a cosine wave',
                ].map((suggestion) => (
                  <button
                    key={suggestion}
                    onClick={() => handleSend(suggestion)}
                    className="block w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-left text-sm text-gray-700 hover:bg-gray-50"
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
              // Find the original user prompt for this message thread
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
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-200">
                  <Spinner size="sm" />
                </div>
                <span className="text-sm text-gray-500">
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
