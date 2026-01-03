'use client'

import { useAuth } from '@clerk/nextjs'
import { useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'
import { Header } from '@/components/layout'
import { NotebookGrid, CreateNotebookButton } from '@/components/notebook'
import { notebooksApi } from '@/lib/api-client'
import { Play } from 'lucide-react'

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
    // TODO: Implement delete API
    setNotebooks((prev) => prev.filter((n) => n.notebook_id !== id))
  }

  const handleRename = async (id: string, newTitle: string) => {
    // TODO: Implement rename API
    setNotebooks((prev) =>
      prev.map((n) => (n.notebook_id === id ? { ...n, title: newTitle } : n))
    )
  }

  return (
    <div className="flex min-h-screen flex-col">
      <Header />

      <main className="flex-1">
        <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
          {/* Welcome Banner */}
          <div className="mb-8 rounded-xl bg-gradient-to-r from-teal-600 to-teal-500 p-6 text-white shadow-lg sm:p-8">
            <div className="flex items-start justify-between">
              <div>
                <h1 className="text-2xl font-bold sm:text-3xl">
                  Welcome to Manimo
                </h1>
                <p className="mt-2 max-w-xl text-teal-100">
                  Create, run, and share mathematical animations powered by Manim and AI.
                  Just describe what you want to animate, and let AI write the code.
                </p>
              </div>
              <div className="hidden sm:block">
                <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-white/20 backdrop-blur">
                  <Play className="h-8 w-8 text-white" fill="white" />
                </div>
              </div>
            </div>
          </div>

          {/* Notebooks Section */}
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-900">
              Your Notebooks
            </h2>
            <CreateNotebookButton onCreate={handleCreate} />
          </div>

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
