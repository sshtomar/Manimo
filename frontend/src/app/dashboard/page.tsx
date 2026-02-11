'use client'

import { useAuth } from '@clerk/nextjs'
import { useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'
import { Header } from '@/components/layout'
import { NotebookGrid, CreateNotebookButton } from '@/components/notebook'
import { notebooksApi } from '@/lib/api-client'
import { Plus, Sparkles } from 'lucide-react'
import { Button } from '@/components/ui'

interface Notebook {
  notebook_id: string
  title: string
  created_at: string
  updated_at: string
}

export default function DashboardPage() {
  const { userId, isLoaded } = useAuth()
  const router = useRouter()
  const [notebooks, setNotebooks] = useState<Notebook[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    async function fetchNotebooks() {
      if (!userId) return

      try {
        const data = await notebooksApi.list(userId)
        setNotebooks(data)
      } catch (error) {
        console.error('Failed to fetch notebooks:', error)
      } finally {
        setIsLoading(false)
      }
    }

    if (isLoaded && userId) {
      fetchNotebooks()
    }
  }, [isLoaded, userId])

  const handleCreate = async (title?: string) => {
    if (!userId) return

    try {
      const notebookId = await notebooksApi.create(userId, title || 'Untitled Notebook')
      router.push(`/notebook/${notebookId}`)
    } catch (error) {
      console.error('Failed to create notebook:', error)
    }
  }

  const handleDelete = async (id: string) => {
    setNotebooks((prev) => prev.filter((n) => n.notebook_id !== id))
  }

  const handleRename = async (id: string, newTitle: string) => {
    setNotebooks((prev) =>
      prev.map((n) => (n.notebook_id === id ? { ...n, title: newTitle } : n))
    )
  }

  return (
    <div className="flex min-h-screen flex-col bg-slate-50">
      <Header />

      <main className="flex-1">
        <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
          {/* Welcome Section */}
          <div className="mb-8">
            <div className="flex items-start justify-between">
              <div>
                <h1 className="text-2xl font-semibold tracking-tight text-slate-900">
                  Your Notebooks
                </h1>
                <p className="mt-1 text-sm text-slate-500">
                  Create, run, and share mathematical animations powered by AI
                </p>
              </div>
              <CreateNotebookButton onCreate={handleCreate} />
            </div>
          </div>

          {/* Quick Start - Only shown when no notebooks */}
          {!isLoading && notebooks.length === 0 && (
            <div className="mb-8 rounded-xl border border-slate-200 bg-white p-8">
              <div className="mx-auto max-w-md text-center">
                <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-amber-100">
                  <Sparkles className="h-6 w-6 text-amber-600" />
                </div>
                <h2 className="text-lg font-semibold text-slate-900">
                  Create your first notebook
                </h2>
                <p className="mt-2 text-sm text-slate-500">
                  Describe what you want to animate in plain English and let AI write the Manim code for you.
                </p>
                <div className="mt-6">
                  <Button variant="accent" onClick={() => handleCreate()}>
                    <Plus className="h-4 w-4" />
                    New Notebook
                  </Button>
                </div>
              </div>
            </div>
          )}

          {/* Notebooks Grid */}
          <NotebookGrid
            notebooks={notebooks}
            isLoading={isLoading}
            onDelete={handleDelete}
            onRename={handleRename}
          />
        </div>
      </main>
    </div>
  )
}
