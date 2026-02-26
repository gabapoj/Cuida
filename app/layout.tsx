import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Cuida',
  description: 'Welcome to Cuida',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased bg-cream min-h-screen">{children}</body>
    </html>
  )
}
