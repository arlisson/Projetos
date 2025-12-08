interface FinanceiroProps {
  label: string
  value: string
  footer?: string
}

export function Financeiro({ label, value, footer }: FinanceiroProps) {
  return (
    <div className="summary-card">
      <span className="summary-label">{label}</span>
      <span className="summary-value">{value}</span>
      {footer && <div className="summary-footer">{footer}</div>}
    </div>
  )
}
