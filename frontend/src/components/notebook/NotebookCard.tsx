'use client'

import Link from 'next/link'
import { formatDistanceToNow } from '@/lib/utils'
import { Play, MoreVertical, Trash2, Edit2 } from 'lucide-react'
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
    <div className="group relative rounded-lg border border-gray-200 bg-white transition-all hover:border-gray-300 hover:shadow-md">
      <Link href={`/notebook/${id}`} className="block p-4">
        {/* Thumbnail placeholder */}
        <div className="mb-3 flex h-32 items-center justify-center rounded-md bg-gradient-to-br from-teal-50 to-teal-100">
          <Play className="h-8 w-8 text-teal-600/50" />
        </div>

        {/* Content */}
        <h3 className="font-medium text-gray-900 truncate">
          {title}
        </h3>
        <p className="mt-1 text-sm text-gray-500">
          {formatDistanceToNow(updatedAt)}
        </p>
      </Link>

      {/* Actions menu */}
      <div className="absolute right-2 top-2" ref={menuRef}>
        <button
          onClick={(e) => {
            e.preventDefault()
            setMenuOpen(!menuOpen)
          }}
          className="rounded p-1 opacity-0 transition-opacity group-hover:opacity-100 hover:bg-gray-100"
        >
          <MoreVertical className="h-4 w-4 text-gray-500" />
        </button>

        {menuOpen && (
          <div className="absolute right-0 mt-1 w-36 rounded-md border border-gray-200 bg-white py-1 shadow-lg z-10">
            <button
              onClick={() => {
                const newTitle = prompt('New title:', title)
                if (newTitle && newTitle !== title) {
                  onRename?.(id, newTitle)
                }
                setMenuOpen(false)
              }}
              className="flex w-full items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:bg-gray-100"
            >
              <Edit2 className="h-4 w-4" />
              Rename
            </button>
            <button
              onClick={() => {
                if (confirm('Delete this notebook?')) {
                  onDelete?.(id)
                }
                setMenuOpen(false)
              }}
              className="flex w-full items-center gap-2 px-3 py-2 text-sm text-red-600 hover:bg-gray-100"
            >
              <Trash2 className="h-4 w-4" />
              Delete
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
