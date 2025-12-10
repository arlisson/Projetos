interface FinanceiroProps {
  label: string
  value: number          // valor cru (number)
  isCurrency?: boolean   // true = formata como R$, false = apenas número
  footer?: string
}

export function Financeiro({ label, value, isCurrency = true, footer }: FinanceiroProps) {
  const formatCurrency = (v: number) =>
    v.toLocaleString('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    })

  const formatNumber = (v: number) =>
    v.toLocaleString('pt-BR', {
      maximumFractionDigits: 0,
    })

  const displayValue = isCurrency ? formatCurrency(value) : formatNumber(value)

  return (
    <div className="summary-card">
      <span className="summary-label">{label}</span>
      <span className="summary-value">{displayValue}</span>
      {footer && <div className="summary-footer">{footer}</div>}
    </div>
  )
}
