import type { Metadata } from 'next'
import { ClerkProvider } from '@clerk/nextjs'
import './globals.css'

export const metadata: Metadata = {
  title: 'Manimo - AI-Native Animation Notebooks',
  description: 'Create mathematical animations with Manim using AI assistance',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="en" suppressHydrationWarning>
        <body className="min-h-screen bg-white text-gray-900 antialiased">
          {children}
        </body>
      </html>
    </ClerkProvider>
  )
}
