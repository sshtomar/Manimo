'use client'

import { formatDistanceToNow } from '@/lib/utils'
import { DiffPreview } from './DiffPreview'
import { User, Sparkles } from 'lucide-react'
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
        className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-md ${
          isUser
            ? 'bg-slate-900 text-white'
            : 'bg-amber-100 text-amber-600'
        }`}
      >
        {isUser ? (
          <User className="h-3.5 w-3.5" />
        ) : (
          <Sparkles className="h-3.5 w-3.5" />
        )}
      </div>

      {/* Content */}
      <div className={`flex max-w-[85%] flex-col gap-2 ${isUser ? 'items-end' : 'items-start'}`}>
        <div
          className={`rounded-lg px-3 py-2 ${
            isUser
              ? 'bg-slate-900 text-white'
              : 'bg-slate-100 text-slate-900'
          }`}
        >
          <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
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
        <span className="text-[11px] text-slate-400">
          {formatDistanceToNow(message.timestamp)}
        </span>
      </div>
    </div>
  )
}
