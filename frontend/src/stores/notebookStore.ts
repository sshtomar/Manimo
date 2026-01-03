import { create } from 'zustand'
import { notebooksApi } from '@/lib/api-client'

interface Notebook {
  notebook_id: string
  title: string
  content?: string
  created_at: string
  updated_at: string
}

interface NotebookState {
  notebooks: Notebook[]
  currentNotebook: Notebook | null
  isLoading: boolean
  error: string | null

  fetchNotebooks: (userId: string) => Promise<void>
  fetchNotebook: (notebookId: string, userId: string) => Promise<void>
  createNotebook: (userId: string, title?: string) => Promise<string>
  updateContent: (notebookId: string, content: string, userId: string) => Promise<void>
  setCurrentNotebook: (notebook: Notebook | null) => void
  clearError: () => void
}

export const useNotebookStore = create<NotebookState>((set, get) => ({
  notebooks: [],
  currentNotebook: null,
  isLoading: false,
  error: null,

  fetchNotebooks: async (userId: string) => {
    set({ isLoading: true, error: null })
    try {
      const notebooks = await notebooksApi.list(userId)
      set({ notebooks, isLoading: false })
    } catch (error) {
      set({ error: 'Failed to fetch notebooks', isLoading: false })
      throw error
    }
  },

  fetchNotebook: async (notebookId: string, userId: string) => {
    set({ isLoading: true, error: null })
    try {
      const content = await notebooksApi.get(notebookId, userId)
      const notebooks = get().notebooks
      const existing = notebooks.find((n) => n.notebook_id === notebookId)

      const notebook: Notebook = {
        notebook_id: notebookId,
        title: existing?.title || 'Untitled',
        content,
        created_at: existing?.created_at || new Date().toISOString(),
        updated_at: new Date().toISOString(),
      }

      set({ currentNotebook: notebook, isLoading: false })
    } catch (error) {
      set({ error: 'Failed to fetch notebook', isLoading: false })
      throw error
    }
  },

  createNotebook: async (userId: string, title?: string) => {
    set({ isLoading: true, error: null })
    try {
      const notebookId = await notebooksApi.create(userId, title)
      set({ isLoading: false })
      return notebookId
    } catch (error) {
      set({ error: 'Failed to create notebook', isLoading: false })
      throw error
    }
  },

  updateContent: async (notebookId: string, content: string, userId: string) => {
    try {
      await notebooksApi.save(notebookId, content, userId)
      const current = get().currentNotebook
      if (current && current.notebook_id === notebookId) {
        set({
          currentNotebook: {
            ...current,
            content,
            updated_at: new Date().toISOString(),
          },
        })
      }
    } catch (error) {
      set({ error: 'Failed to save notebook' })
      throw error
    }
  },

  setCurrentNotebook: (notebook: Notebook | null) => {
    set({ currentNotebook: notebook })
  },

  clearError: () => {
    set({ error: null })
  },
}))
