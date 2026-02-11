import { clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

type SpinnerSize = 'sm' | 'md' | 'lg'

interface SpinnerProps {
  size?: SpinnerSize
  className?: string
}

const sizeStyles: Record<SpinnerSize, string> = {
  sm: 'h-4 w-4 border-[2px]',
  md: 'h-5 w-5 border-2',
  lg: 'h-6 w-6 border-2',
}

export function Spinner({ size = 'md', className }: SpinnerProps) {
  return (
    <div
      className={twMerge(
        clsx(
          'rounded-full',
          'border-slate-200',
          'border-t-slate-900',
          'animate-spin',
          sizeStyles[size],
          className
        )
      )}
    />
  )
}

export function LoadingScreen({ message = 'Loading...' }: { message?: string }) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50">
      <div className="flex flex-col items-center gap-4">
        <Spinner size="lg" />
        <p className="text-sm text-slate-500">{message}</p>
      </div>
    </div>
  )
}
