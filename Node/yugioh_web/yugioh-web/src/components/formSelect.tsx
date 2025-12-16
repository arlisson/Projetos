import { useMemo, useState, useRef, useEffect } from 'react'

interface Option {
  value: string
  label: string
}

interface FormSelectProps {
  label: string
  name: string
  value: string
  onChange: (value: string) => void
  options: Option[]
  placeholder?: string
  required?: boolean
  /** Se false, desativa o botão "Limpar seleção" */
  clearable?: boolean
}

export function FormSelect({
  label,
  name,
  value,
  onChange,
  options,
  placeholder,
  required = false,
  clearable = true,
}: FormSelectProps) {
  const [query, setQuery] = useState('')
  const [open, setOpen] = useState(false)
  const containerRef = useRef<HTMLDivElement | null>(null)

  const selected = options.find((o) => o.value === value) || null

  const filteredOptions = useMemo(() => {
    const q = query.trim().toLowerCase()
    if (!q) return options
    return options.filter(
      (opt) =>
        opt.label.toLowerCase().includes(q) ||
        opt.value.toLowerCase().includes(q),
    )
  }, [options, query])

  // Fecha dropdown ao clicar fora
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (
        containerRef.current &&
        !containerRef.current.contains(e.target as Node)
      ) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  function handleSelect(opt: Option) {
    onChange(opt.value)
    setQuery('')
    setOpen(false)
  }

  function handleClear() {
    onChange('')
    setQuery('')
    setOpen(false)
  }

  return (
    <div className="form-field">
      <label className="form-field-label" htmlFor={name}>
        {label}
        {required && <span className="form-field-required">*</span>}
      </label>

      <div className="form-field-input-wrapper" ref={containerRef}>
        {/* Campo que funciona como select + filtro */}
        <input
          id={name}
          name={name}
          required={required}
          className="form-select-input"
          value={open ? query : selected?.label ?? ''}
          placeholder={placeholder}
          onChange={(e) => {
            setQuery(e.target.value)
            if (!open) setOpen(true)
          }}
          onFocus={() => setOpen(true)}
        />

        {/* Botão "Limpar seleção" */}
        {clearable && value && (
          <button
            type="button"
            className="form-select-clear"
            onClick={handleClear}
          >
            Limpar seleção
          </button>
        )}

        {open && (
          <div className="form-select-dropdown">
            {filteredOptions.length === 0 && (
              <div className="form-select-empty">
                Nenhuma opção encontrada
              </div>
            )}
            {filteredOptions.map((opt) => (
              <div
                key={opt.value}
                className="form-select-option"
                onClick={() => handleSelect(opt)}
              >
                {opt.label}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
