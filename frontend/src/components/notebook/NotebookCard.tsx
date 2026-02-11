'use client'

import Link from 'next/link'
import { formatDistanceToNow } from '@/lib/utils'
import { Play, MoreHorizontal, Trash2, Pencil } from 'lucide-react'
import { useState, useRef, useEffect } from 'react'

interface NotebookCardProps {
  id: string
  title: string
  updatedAt: string
  onDelete?: (id: string) => void
  onRename?: (id: string, newTitle: string) => void
}

export function NotebookCard({ id, title, updatedAt, onDelete, onRename }: NotebookCardProps) {
  const [menuOpen, setMenuOpen] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setMenuOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  return (
    <div className="group relative rounded-lg border border-slate-200 bg-white transition-all duration-150 hover:border-slate-300 hover:shadow-sm">
      <Link href={`/notebook/${id}`} className="block p-4">
        {/* Thumbnail */}
        <div className="mb-4 flex aspect-[4/3] items-center justify-center rounded-md bg-slate-100">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-slate-200/80">
            <Play className="h-5 w-5 text-slate-400" />
          </div>
        </div>

        {/* Content */}
        <h3 className="truncate text-sm font-medium text-slate-900">
          {title}
        </h3>
        <p className="mt-1 text-xs text-slate-500">
          {formatDistanceToNow(updatedAt)}
        </p>
      </Link>

      {/* Actions menu */}
      <div className="absolute right-3 top-3" ref={menuRef}>
        <button
          onClick={(e) => {
            e.preventDefault()
            e.stopPropagation()
            setMenuOpen(!menuOpen)
          }}
          className="flex h-7 w-7 items-center justify-center rounded-md bg-white/80 text-slate-500 opacity-0 backdrop-blur transition-all hover:bg-slate-100 hover:text-slate-700 group-hover:opacity-100"
        >
          <MoreHorizontal className="h-4 w-4" />
        </button>

        {menuOpen && (
          <div className="absolute right-0 top-8 z-10 w-36 rounded-lg border border-slate-200 bg-white py-1 shadow-lg">
            <button
              onClick={(e) => {
                e.preventDefault()
                e.stopPropagation()
                const newTitle = prompt('Rename notebook:', title)
                if (newTitle && newTitle !== title) {
                  onRename?.(id, newTitle)
                }
                setMenuOpen(false)
              }}
              className="flex w-full items-center gap-2 px-3 py-2 text-sm text-slate-600 hover:bg-slate-50"
            >
              <Pencil className="h-3.5 w-3.5" />
              Rename
            </button>
            <button
              onClick={(e) => {
                e.preventDefault()
                e.stopPropagation()
                if (confirm('Delete this notebook?')) {
                  onDelete?.(id)
                }
                setMenuOpen(false)
              }}
              className="flex w-full items-center gap-2 px-3 py-2 text-sm text-red-600 hover:bg-red-50"
            >
              <Trash2 className="h-3.5 w-3.5" />
              Delete
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
