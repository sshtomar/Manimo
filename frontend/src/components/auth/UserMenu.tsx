'use client'

import { useUser, useClerk } from '@clerk/nextjs'
import { useState, useRef, useEffect } from 'react'
import { LogOut, ChevronDown } from 'lucide-react'

export function UserMenu() {
  const { user } = useUser()
  const { signOut } = useClerk()
  const [isOpen, setIsOpen] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  if (!user) return null

  const initials = user.fullName
    ?.split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2) || 'U'

  return (
    <div className="relative" ref={menuRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-1.5 rounded-md p-1 transition-colors hover:bg-slate-100"
      >
        {user.imageUrl ? (
          <img
            src={user.imageUrl}
            alt={user.fullName || 'User'}
            className="h-7 w-7 rounded-md"
          />
        ) : (
          <div className="flex h-7 w-7 items-center justify-center rounded-md bg-slate-900 text-xs font-medium text-white">
            {initials}
          </div>
        )}
        <ChevronDown className="h-3.5 w-3.5 text-slate-400" />
      </button>

      {isOpen && (
        <div className="absolute right-0 z-50 mt-2 w-56 rounded-lg border border-slate-200 bg-white py-1 shadow-lg">
          <div className="border-b border-slate-100 px-4 py-3">
            <p className="text-sm font-medium text-slate-900">
              {user.fullName}
            </p>
            <p className="truncate text-xs text-slate-500">
              {user.primaryEmailAddress?.emailAddress}
            </p>
          </div>

          <button
            onClick={() => signOut({ redirectUrl: '/' })}
            className="flex w-full items-center gap-2 px-4 py-2.5 text-sm text-slate-600 transition-colors hover:bg-slate-50 hover:text-slate-900"
          >
            <LogOut className="h-4 w-4" />
            Sign out
          </button>
        </div>
      )}
    </div>
  )
}
