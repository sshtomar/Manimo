'use client'

import Link from 'next/link'
import { useAuth } from '@clerk/nextjs'
import { Menu, X } from 'lucide-react'
import { useState } from 'react'
import { Button } from '@/components/ui'
import { UserMenu } from '@/components/auth'

function Logo() {
  return (
    <>
      {/* Full wordmark on desktop */}
      <img
        src="/logos/manimo-logo.svg"
        alt="Manimo"
        className="hidden h-7 w-auto sm:block"
      />
      {/* Icon only on mobile */}
      <img
        src="/logos/manimo-icon.svg"
        alt="Manimo"
        className="h-8 w-8 sm:hidden"
      />
    </>
  )
}

export function Header() {
  const { isLoaded, isSignedIn } = useAuth()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-200 bg-white/80 backdrop-blur-sm">
      <div className="mx-auto flex h-14 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Logo */}
        <Link
          href={isSignedIn ? '/dashboard' : '/'}
          className="flex items-center transition-opacity hover:opacity-80"
        >
          <Logo />
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden items-center gap-1 md:flex">
          <Link
            href="https://docs.marimo.io"
            target="_blank"
            className="px-3 py-1.5 text-[13px] font-medium text-slate-600 transition-colors hover:text-slate-900"
          >
            Docs
          </Link>
          <Link
            href="https://github.com"
            target="_blank"
            className="px-3 py-1.5 text-[13px] font-medium text-slate-600 transition-colors hover:text-slate-900"
          >
            GitHub
          </Link>
        </nav>

        {/* Auth */}
        <div className="flex items-center gap-3">
          {!isLoaded ? (
            <div className="h-8 w-8 animate-pulse rounded-full bg-slate-200" />
          ) : isSignedIn ? (
            <UserMenu />
          ) : (
            <Link href="/login">
              <Button size="sm">Sign in</Button>
            </Link>
          )}

          {/* Mobile menu button */}
          <button
            className="flex h-8 w-8 items-center justify-center rounded-md text-slate-600 transition-colors hover:bg-slate-100 hover:text-slate-900 md:hidden"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? (
              <X className="h-5 w-5" />
            ) : (
              <Menu className="h-5 w-5" />
            )}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileMenuOpen && (
        <div className="border-t border-slate-200 bg-white px-4 py-3 md:hidden">
          <nav className="flex flex-col gap-1">
            <Link
              href="https://docs.marimo.io"
              target="_blank"
              className="rounded-md px-3 py-2 text-sm text-slate-600 transition-colors hover:bg-slate-100 hover:text-slate-900"
            >
              Docs
            </Link>
            <Link
              href="https://github.com"
              target="_blank"
              className="rounded-md px-3 py-2 text-sm text-slate-600 transition-colors hover:bg-slate-100 hover:text-slate-900"
            >
              GitHub
            </Link>
          </nav>
        </div>
      )}
    </header>
  )
}
