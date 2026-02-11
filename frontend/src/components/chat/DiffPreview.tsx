'use client'

import { Button } from '@/components/ui'
import { CodeBlock } from './CodeBlock'
import { Check, X, ExternalLink, FileCode } from 'lucide-react'

interface DiffPreviewProps {
  patchType: 'cell' | 'diff' | 'markdown'
  artifact: string
  rationale?: string
  applied: boolean
  onApply: () => void
  onReject: () => void
  onOpenMarimo?: () => void
  isApplying?: boolean
}

export function DiffPreview({
  patchType,
  artifact,
  rationale,
  applied,
  onApply,
  onReject,
  onOpenMarimo,
  isApplying,
}: DiffPreviewProps) {
  const typeLabel = {
    cell: 'New Cell',
    diff: 'Code Changes',
    markdown: 'Markdown',
  }

  return (
    <div className="w-full overflow-hidden rounded-lg border border-slate-200 bg-white">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-200 bg-slate-50 px-3 py-2">
        <div className="flex items-center gap-2">
          <FileCode className="h-3.5 w-3.5 text-slate-400" />
          <span className="text-xs font-medium text-slate-500">
            {typeLabel[patchType]}
          </span>
        </div>
        {applied && (
          <span className="flex items-center gap-1 rounded-full bg-green-100 px-2 py-0.5 text-[11px] font-medium text-green-700">
            <Check className="h-3 w-3" />
            Applied
          </span>
        )}
      </div>

      {/* Rationale */}
      {rationale && (
        <div className="border-b border-slate-200 px-3 py-2">
          <p className="text-xs text-slate-600">{rationale}</p>
        </div>
      )}

      {/* Code */}
      <div className="p-3">
        <CodeBlock
          code={artifact}
          language={patchType === 'markdown' ? 'markdown' : 'python'}
        />
      </div>

      {/* Actions */}
      {!applied && (
        <div className="flex items-center gap-2 border-t border-slate-200 bg-slate-50 px-3 py-2.5">
          <Button
            size="sm"
            variant="accent"
            onClick={onApply}
            isLoading={isApplying}
            disabled={isApplying}
          >
            <Check className="h-3.5 w-3.5" />
            Apply
          </Button>
          <Button
            size="sm"
            variant="ghost"
            onClick={onReject}
            disabled={isApplying}
          >
            <X className="h-3.5 w-3.5" />
            Reject
          </Button>
          {onOpenMarimo && (
            <Button
              size="sm"
              variant="secondary"
              onClick={onOpenMarimo}
              disabled={isApplying}
              className="ml-auto"
            >
              <ExternalLink className="h-3.5 w-3.5" />
              Open in Marimo
            </Button>
          )}
        </div>
      )}
    </div>
  )
}
