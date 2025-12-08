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
}

export function FormSelect({
  label,
  name,
  value,
  onChange,
  options,
  placeholder,
  required = false,
}: FormSelectProps) {
  return (
    <div className="form-field">
      <label className="form-field-label" htmlFor={name}>
        {label}
        {required && <span className="form-field-required">*</span>}
      </label>

      <div className="form-field-input-wrapper">
        <select
          id={name}
          name={name}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          required={required}
          className="form-select-input"
        >
          {placeholder && (
            <option value="" disabled>
              {placeholder}
            </option>
          )}

          {options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </div>
    </div>
  )
}
