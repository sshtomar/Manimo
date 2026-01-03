'use client'

import { Button } from '@/components/ui'
import { CodeBlock } from './CodeBlock'
import { Check, X, ExternalLink } from 'lucide-react'

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
  return (
    <div className="rounded-lg border border-gray-200 bg-gray-50">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-gray-200 px-4 py-2">
        <span className="text-xs font-medium text-gray-500 uppercase">
          {patchType === 'cell' ? 'New Cell' : patchType === 'diff' ? 'Code Changes' : 'Markdown'}
        </span>
        {applied && (
          <span className="flex items-center gap-1 text-xs text-green-600">
            <Check className="h-3 w-3" />
            Applied
          </span>
        )}
      </div>

      {/* Code */}
      <div className="p-4">
        <CodeBlock code={artifact} language={patchType === 'markdown' ? 'markdown' : 'python'} />
      </div>

      {/* Actions */}
      {!applied && (
        <div className="flex items-center gap-2 border-t border-gray-200 px-4 py-3">
          <Button
            size="sm"
            onClick={onApply}
            isLoading={isApplying}
            disabled={isApplying}
          >
            <Check className="mr-1 h-4 w-4" />
            Apply to Notebook
          </Button>
          <Button
            size="sm"
            variant="ghost"
            onClick={onReject}
            disabled={isApplying}
          >
            <X className="mr-1 h-4 w-4" />
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
              <ExternalLink className="mr-1 h-4 w-4" />
              Open in Marimo
            </Button>
          )}
        </div>
      )}
    </div>
  )
}
