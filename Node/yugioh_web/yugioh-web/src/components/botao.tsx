import type { ButtonHTMLAttributes, ReactNode } from 'react'

type ButtonVariant = 'solid' | 'outline' | 'danger' | 'ghost'
type ButtonSize = 'sm' | 'md' | 'lg'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant
  size?: ButtonSize
  fullWidth?: boolean
  leftIcon?: ReactNode
  rightIcon?: ReactNode
}

export function Button({
  variant = 'solid',
  size = 'md',
  fullWidth = false,
  leftIcon,
  rightIcon,
  className,
  children,
  ...rest
}: ButtonProps) {
  const base = 'btn'

  const variantClass =
    variant === 'outline'
      ? 'btn-outline'
      : variant === 'danger'
      ? 'btn-danger'
      : variant === 'ghost'
      ? 'btn-ghost'
      : ''

  const sizeStyle =
    size === 'sm'
      ? { padding: '0.35rem 0.7rem', fontSize: '0.8rem' }
      : size === 'lg'
      ? { padding: '0.55rem 1.1rem', fontSize: '0.9rem' }
      : undefined

  const fullClass = fullWidth ? 'btn-full' : ''

  const classes = [base, variantClass, fullClass, className]
    .filter(Boolean)
    .join(' ')

  return (
    <button className={classes} style={sizeStyle} {...rest}>
      {leftIcon && <span>{leftIcon}</span>}
      <span>{children}</span>
      {rightIcon && <span>{rightIcon}</span>}
    </button>
  )
}
