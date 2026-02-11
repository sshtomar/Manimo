import { create } from 'zustand'
import { aiApi } from '@/lib/api-client'

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: string
  diff?: {
    patchType: 'cell' | 'diff' | 'markdown'
    artifact: string
    rationale?: string
    applied: boolean
  }
}

interface ChatState {
  messages: ChatMessage[]
  isGenerating: boolean
  error: string | null

  sendMessage: (
    notebookId: string,
    userId: string,
    prompt: string
  ) => Promise<void>
  applyDiff: (
    messageId: string,
    notebookId: string,
    userId: string,
    prompt: string
  ) => Promise<void>
  rejectDiff: (messageId: string) => void
  clearMessages: () => void
  clearError: () => void
}

function generateId(): string {
  return Math.random().toString(36).substring(2, 11)
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  isGenerating: false,
  error: null,

  sendMessage: async (notebookId: string, userId: string, prompt: string) => {
    const userMessage: ChatMessage = {
      id: generateId(),
      role: 'user',
      content: prompt,
      timestamp: new Date().toISOString(),
    }

    set((state) => ({
      messages: [...state.messages, userMessage],
      isGenerating: true,
      error: null,
    }))

    try {
      const response = await aiApi.ask(notebookId, userId, prompt, false)

      const assistantMessage: ChatMessage = {
        id: generateId(),
        role: 'assistant',
        content: response.rationale || 'Here is the generated code:',
        timestamp: new Date().toISOString(),
        diff: {
          patchType: response.patch_type,
          artifact: response.artifact,
          rationale: response.rationale,
          applied: false,
        },
      }

      set((state) => ({
        messages: [...state.messages, assistantMessage],
        isGenerating: false,
      }))
    } catch (error) {
      const errorMessage: ChatMessage = {
        id: generateId(),
        role: 'assistant',
        content: `Sorry, I encountered an error: ${error instanceof Error ? error.message : 'Unknown error'}`,
        timestamp: new Date().toISOString(),
      }

      set((state) => ({
        messages: [...state.messages, errorMessage],
        isGenerating: false,
        error: 'Failed to generate response',
      }))
    }
  },

  applyDiff: async (
    messageId: string,
    notebookId: string,
    userId: string,
    prompt: string
  ) => {
    try {
      await aiApi.ask(notebookId, userId, prompt, true)

      set((state) => ({
        messages: state.messages.map((msg) =>
          msg.id === messageId && msg.diff
            ? { ...msg, diff: { ...msg.diff, applied: true } }
            : msg
        ),
      }))
    } catch (error) {
      set({ error: 'Failed to apply changes' })
      throw error
    }
  },

  rejectDiff: (messageId: string) => {
    set((state) => ({
      messages: state.messages.filter((msg) => msg.id !== messageId),
    }))
  },

  clearMessages: () => {
    set({ messages: [], error: null })
  },

  clearError: () => {
    set({ error: null })
  },
}))
