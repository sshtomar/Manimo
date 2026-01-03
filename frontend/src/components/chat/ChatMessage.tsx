'use client'

import { formatDistanceToNow } from '@/lib/utils'
import { DiffPreview } from './DiffPreview'
import { User, Bot } from 'lucide-react'
import type { ChatMessage as ChatMessageType } from '@/stores'

interface ChatMessageProps {
  message: ChatMessageType
  onApply?: () => void
  onReject?: () => void
  onOpenMarimo?: () => void
  isApplying?: boolean
}

export function ChatMessage({
  message,
  onApply,
  onReject,
  onOpenMarimo,
  isApplying,
}: ChatMessageProps) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex gap-3 ${isUser ? 'flex-row-reverse' : ''}`}>
      {/* Avatar */}
      <div
        className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full ${
          isUser
            ? 'bg-teal-600 text-white'
            : 'bg-gray-200 text-gray-600'
        }`}
      >
        {isUser ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
      </div>

      {/* Content */}
      <div className={`flex max-w-[80%] flex-col gap-2 ${isUser ? 'items-end' : 'items-start'}`}>
        <div
          className={`rounded-lg px-4 py-2 ${
            isUser
              ? 'bg-teal-600 text-white'
              : 'bg-gray-100 text-gray-900'
          }`}
        >
          <p className="text-sm whitespace-pre-wrap">{message.content}</p>
        </div>

        {/* Diff Preview for assistant messages */}
        {message.diff && !isUser && (
          <DiffPreview
            patchType={message.diff.patchType}
            artifact={message.diff.artifact}
            rationale={message.diff.rationale}
            applied={message.diff.applied}
            onApply={onApply || (() => {})}
            onReject={onReject || (() => {})}
            onOpenMarimo={onOpenMarimo}
            isApplying={isApplying}
          />
        )}

        {/* Timestamp */}
        <span className="text-xs text-gray-400">
          {formatDistanceToNow(message.timestamp)}
        </span>
      </div>
    </div>
  )
}
