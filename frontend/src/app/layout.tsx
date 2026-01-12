import type { Metadata } from 'next'
import { ClerkProvider } from '@clerk/nextjs'
import { Plus_Jakarta_Sans, JetBrains_Mono, Crimson_Pro } from 'next/font/google'
import './globals.css'

const jakarta = Plus_Jakarta_Sans({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-sans',
  weight: ['400', '500', '600', '700'],
})

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-mono',
  weight: ['400', '500'],
})

const crimsonPro = Crimson_Pro({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-serif',
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
      <html lang="en" className={`${jakarta.variable} ${jetbrainsMono.variable} ${crimsonPro.variable}`} suppressHydrationWarning>
        <body className="min-h-screen bg-surface text-primary antialiased">
          {children}
        </body>
      </html>
    </ClerkProvider>
  )
}
