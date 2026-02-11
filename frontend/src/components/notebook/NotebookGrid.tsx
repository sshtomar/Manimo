'use client'

import { NotebookCard } from './NotebookCard'
import { FileText } from 'lucide-react'

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

function SkeletonCard() {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4">
      <div className="mb-4 aspect-[4/3] animate-pulse rounded-md bg-slate-100" />
      <div className="h-4 w-3/4 animate-pulse rounded bg-slate-100" />
      <div className="mt-2 h-3 w-1/2 animate-pulse rounded bg-slate-100" />
    </div>
  )
}

function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-slate-300 bg-slate-50/50 py-16 text-center">
      <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-slate-100">
        <FileText className="h-6 w-6 text-slate-400" />
      </div>
      <h3 className="text-sm font-medium text-slate-900">
        No notebooks yet
      </h3>
      <p className="mt-1 text-sm text-slate-500">
        Create your first notebook to get started
      </p>
    </div>
  )
}

export function NotebookGrid({ notebooks, isLoading, onDelete, onRename }: NotebookGridProps) {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {[...Array(4)].map((_, i) => (
          <SkeletonCard key={i} />
        ))}
      </div>
    )
  }

  if (notebooks.length === 0) {
    return <EmptyState />
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
