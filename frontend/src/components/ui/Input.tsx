'use client'

import { clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'
import { forwardRef, InputHTMLAttributes, TextareaHTMLAttributes } from 'react'

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  error?: string
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, error, ...props }, ref) => {
    return (
      <div className="w-full">
        <input
          ref={ref}
          className={twMerge(
            clsx(
              // Base
              'w-full h-9 px-3 text-sm',
              'rounded-md',
              'bg-white',
              'text-slate-900',
              'placeholder:text-slate-400',
              // Border
              'border',
              error
                ? 'border-red-500'
                : 'border-slate-200',
              // Focus
              'focus:outline-none focus:ring-2 focus:ring-offset-0',
              error
                ? 'focus:ring-red-500/20 focus:border-red-500'
                : 'focus:ring-amber-500/20 focus:border-amber-500',
              // Transition
              'transition-colors duration-150',
              // Disabled
              'disabled:cursor-not-allowed disabled:opacity-50 disabled:bg-slate-50',
              className
            )
          )}
          {...props}
        />
        {error && (
          <p className="mt-1.5 text-[13px] text-red-500">{error}</p>
        )}
      </div>
    )
  }
)

Input.displayName = 'Input'

interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  error?: string
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, error, ...props }, ref) => {
    return (
      <div className="w-full">
        <textarea
          ref={ref}
          className={twMerge(
            clsx(
              // Base
              'w-full px-3 py-2 text-sm',
              'rounded-md',
              'bg-white',
              'text-slate-900',
              'placeholder:text-slate-400',
              'resize-none',
              // Border
              'border',
              error
                ? 'border-red-500'
                : 'border-slate-200',
              // Focus
              'focus:outline-none focus:ring-2 focus:ring-offset-0',
              error
                ? 'focus:ring-red-500/20 focus:border-red-500'
                : 'focus:ring-amber-500/20 focus:border-amber-500',
              // Transition
              'transition-colors duration-150',
              // Disabled
              'disabled:cursor-not-allowed disabled:opacity-50 disabled:bg-slate-50',
              className
            )
          )}
          {...props}
        />
        {error && (
          <p className="mt-1.5 text-[13px] text-red-500">{error}</p>
        )}
      </div>
    )
  }
)

Textarea.displayName = 'Textarea'
