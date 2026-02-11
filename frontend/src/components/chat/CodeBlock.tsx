'use client'

import { useState } from 'react'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { Copy, Check } from 'lucide-react'

interface CodeBlockProps {
  code: string
  language?: string
  filename?: string
}

export function CodeBlock({ code, language = 'python', filename }: CodeBlockProps) {
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="group relative overflow-hidden rounded-lg border border-slate-200">
      {/* Header */}
      {filename && (
        <div className="flex items-center justify-between border-b border-slate-200 bg-slate-50 px-3 py-2">
          <span className="font-mono text-xs text-slate-500">
            {filename}
          </span>
        </div>
      )}

      {/* Copy button */}
      <button
        onClick={handleCopy}
        className="absolute right-2 top-2 flex h-7 w-7 items-center justify-center rounded-md bg-slate-800/80 opacity-0 backdrop-blur transition-opacity hover:bg-slate-700 group-hover:opacity-100"
        aria-label="Copy code"
      >
        {copied ? (
          <Check className="h-3.5 w-3.5 text-green-400" />
        ) : (
          <Copy className="h-3.5 w-3.5 text-slate-300" />
        )}
      </button>

      {/* Code */}
      <SyntaxHighlighter
        language={language}
        style={oneDark}
        customStyle={{
          margin: 0,
          borderRadius: filename ? 0 : '0.5rem',
          fontSize: '13px',
          lineHeight: '1.6',
          padding: '16px',
        }}
        codeTagProps={{
          style: {
            fontFamily: 'var(--font-mono), JetBrains Mono, monospace',
          },
        }}
      >
        {code}
      </SyntaxHighlighter>
    </div>
  )
}
