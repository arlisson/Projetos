import { useRef } from 'react'

type FieldKind = 'texto' | 'numero' | 'data'

interface FormFieldProps {
  label: string
  name: string
  kind?: FieldKind
  value: string
  onChange: (value: string) => void
  placeholder?: string
  required?: boolean
}

export function FormField({
  label,
  name,
  kind = 'texto',
  value,
  onChange,
  placeholder,
  required = false,
}: FormFieldProps) {
  const inputRef = useRef<HTMLInputElement | null>(null)

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    let val = e.target.value

    if (kind === 'numero') {
    // Permite apenas dígitos e ponto
    val = val.replace(/[^0-9.]/g, '')

    // Garante no máximo um ponto decimal
    const firstDotIndex = val.indexOf('.')
    if (firstDotIndex !== -1) {
      // Mantém o primeiro ponto e remove os demais
      const before = val.slice(0, firstDotIndex + 1)
      const after = val.slice(firstDotIndex + 1).replace(/\./g, '')
      val = before + after
    }
  }


    onChange(val)
  }

  function handleOpenDatePicker() {
    if (kind !== 'data') return
    const input = inputRef.current
    if (!input) return

    // Em navegadores modernos, tenta abrir o date picker nativo
    // fallback: apenas foca o input
    const anyInput = input as any
    if (typeof anyInput.showPicker === 'function') {
      anyInput.showPicker()
    } else {
      input.focus()
    }
  }

  const inputType =
    kind === 'data' ? 'date' : kind === 'numero' ? 'text' : 'text'

  return (
    <div className="form-field">
      <label className="form-field-label" htmlFor={name}>
        {label}
        {required && <span className="form-field-required">*</span>}
      </label>

      <div className="form-field-input-wrapper">
        <input
          ref={inputRef}
          id={name}
          name={name}
          type={inputType}
          value={value}
          onChange={handleChange}
          placeholder={placeholder}
          required={required}
          className="form-field-input"
          inputMode={kind === 'numero' ? 'numeric' : 'text'}
        />

        {kind === 'data' && (
          <button
            type="button"
            className="form-field-date-button"
            onClick={handleOpenDatePicker}
          >
            Selecionar
          </button>
        )}
      </div>
    </div>
  )
}
