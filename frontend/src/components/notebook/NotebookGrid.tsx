'use client'

import { NotebookCard } from './NotebookCard'
import { Spinner } from '@/components/ui'

interface Notebook {
  notebook_id: string
  title: string
  updated_at: string
}

interface NotebookGridProps {
  notebooks: Notebook[]
  isLoading?: boolean
  onDelete?: (id: string) => void
  onRename?: (id: string, newTitle: string) => void
}

export function NotebookGrid({ notebooks, isLoading, onDelete, onRename }: NotebookGridProps) {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Spinner size="lg" />
      </div>
    )
  }

  if (notebooks.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-center">
        <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-gray-100">
          <svg
            className="h-8 w-8 text-gray-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
            />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-gray-900">
          No notebooks yet
        </h3>
        <p className="mt-1 text-sm text-gray-500">
          Create your first notebook to get started
        </p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      {notebooks.map((notebook) => (
        <NotebookCard
          key={notebook.notebook_id}
          id={notebook.notebook_id}
          title={notebook.title}
          updatedAt={notebook.updated_at}
          onDelete={onDelete}
          onRename={onRename}
        />
      ))}
    </div>
  )
}
