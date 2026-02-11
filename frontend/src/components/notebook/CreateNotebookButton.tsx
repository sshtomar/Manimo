'use client'

import { useState } from 'react'
import { Plus } from 'lucide-react'
import { Button } from '@/components/ui'

interface CreateNotebookButtonProps {
  onCreate: (title?: string) => Promise<void>
}

export function CreateNotebookButton({ onCreate }: CreateNotebookButtonProps) {
  const [isCreating, setIsCreating] = useState(false)

  const handleCreate = async () => {
    setIsCreating(true)
    try {
      await onCreate()
    } finally {
      setIsCreating(false)
    }
  }

  return (
    <Button onClick={handleCreate} isLoading={isCreating} size="sm">
      <Plus className="h-4 w-4" />
      New Notebook
    </Button>
  )
}
