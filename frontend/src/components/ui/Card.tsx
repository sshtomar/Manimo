import { clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'
import { HTMLAttributes } from 'react'

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  interactive?: boolean
  padding?: 'none' | 'sm' | 'md' | 'lg'
}

const paddingStyles = {
  none: '',
  sm: 'p-4',
  md: 'p-6',
  lg: 'p-8',
}

export function Card({
  className,
  interactive = false,
  padding = 'md',
  children,
  ...props
}: CardProps) {
  return (
    <div
      className={twMerge(
        clsx(
          // Base surface
          'bg-white',
          'border border-slate-200',
          'rounded-lg',
          // Padding
          paddingStyles[padding],
          // Interactive states
          interactive && [
            'transition-all duration-150',
            'hover:border-slate-300',
            'hover:shadow-sm',
            'cursor-pointer',
          ],
          className
        )
      )}
      {...props}
    >
      {children}
    </div>
  )
}

export function CardHeader({ className, children, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={twMerge('mb-4', className)} {...props}>
      {children}
    </div>
  )
}

export function CardTitle({ className, children, ...props }: HTMLAttributes<HTMLHeadingElement>) {
  return (
    <h3
      className={twMerge(
        'text-base font-semibold text-slate-900',
        'tracking-tight',
        className
      )}
      {...props}
    >
      {children}
    </h3>
  )
}

export function CardDescription({ className, children, ...props }: HTMLAttributes<HTMLParagraphElement>) {
  return (
    <p
      className={twMerge(
        'text-sm text-slate-500',
        'mt-1',
        className
      )}
      {...props}
    >
      {children}
    </p>
  )
}

export function CardContent({ className, children, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={twMerge(className)} {...props}>
      {children}
    </div>
  )
}

export function CardFooter({ className, children, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={twMerge(
        'mt-4 pt-4',
        'border-t border-slate-100',
        'flex items-center gap-3',
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
}
