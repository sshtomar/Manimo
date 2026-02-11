import type { Metadata } from 'next'
import { ClerkProvider } from '@clerk/nextjs'
import { Source_Sans_3, JetBrains_Mono, Cormorant_Garamond } from 'next/font/google'
import './globals.css'

const sourceSans = Source_Sans_3({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-sans',
  weight: ['300', '400', '500', '600', '700'],
})

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-mono',
  weight: ['400', '500'],
})

const cormorant = Cormorant_Garamond({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-display',
  weight: ['400', '500', '600', '700'],
  style: ['normal', 'italic'],
})

export const metadata: Metadata = {
  title: 'Manimo — AI-Powered Mathematical Animations',
  description: 'Create beautiful mathematical animations with natural language. No setup required.',
  icons: {
    icon: '/favicon.svg',
    apple: '/logos/manimo-icon.svg',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="en" className={`${sourceSans.variable} ${jetbrainsMono.variable} ${cormorant.variable}`} suppressHydrationWarning>
        <body className="min-h-screen bg-surface text-primary antialiased">
          {children}
        </body>
      </html>
    </ClerkProvider>
  )
}
