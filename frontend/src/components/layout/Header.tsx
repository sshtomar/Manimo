'use client'

import Link from 'next/link'
import { useAuth } from '@clerk/nextjs'
import { Play, Menu, X } from 'lucide-react'
import { useState } from 'react'
import { Button } from '@/components/ui'
import { UserMenu } from '@/components/auth'

export function Header() {
  const { isLoaded, isSignedIn } = useAuth()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <header className="sticky top-0 z-40 border-b border-gray-200 bg-white/80 backdrop-blur-sm">
      <div className="mx-auto flex h-14 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Logo */}
        <Link href={isSignedIn ? '/dashboard' : '/'} className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-teal-600">
            <Play className="h-4 w-4 text-white" fill="white" />
          </div>
          <span className="text-lg font-bold text-gray-900">
            Manimo
          </span>
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden items-center gap-6 md:flex">
          <Link
            href="https://docs.marimo.io"
            target="_blank"
            className="text-sm text-gray-600 hover:text-gray-900"
          >
            Docs
          </Link>
        </nav>

        {/* Auth */}
        <div className="flex items-center gap-4">
          {!isLoaded ? (
            <div className="h-8 w-8 animate-pulse rounded-full bg-gray-200" />
          ) : isSignedIn ? (
            <UserMenu />
          ) : (
            <Link href="/login">
              <Button size="sm">Sign in</Button>
            </Link>
          )}

          {/* Mobile menu button */}
          <button
            className="md:hidden p-2"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? (
              <X className="h-5 w-5 text-gray-600" />
            ) : (
              <Menu className="h-5 w-5 text-gray-600" />
            )}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileMenuOpen && (
        <div className="border-t border-gray-200 bg-white px-4 py-4 md:hidden">
          <nav className="flex flex-col gap-4">
            <Link
              href="https://docs.marimo.io"
              target="_blank"
              className="text-sm text-gray-600 hover:text-gray-900"
            >
              Docs
            </Link>
          </nav>
        </div>
      )}
    </header>
  )
}
