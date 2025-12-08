interface GraficoProps {
  title: string
  placeholderText?: string
}

export function Grafico({ title, placeholderText }: GraficoProps) {
  return (
    <div className="chart-card">
      <div className="chart-title">{title}</div>
      <div className="chart-placeholder">
        {placeholderText ?? 'Gráfico a ser implementado'}
      </div>
    </div>
  )
}
