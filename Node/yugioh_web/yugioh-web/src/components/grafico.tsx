// components/Grafico.tsx
import { useMemo, useState } from 'react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts'

export interface SerieConfig {
  /** Chave do campo numérico no objeto de dados (ex.: 'preco', 'lucro_total') */
  key: string
  /** Rótulo exibido na legenda/tooltip */
  label: string
}

export type PontoFinanceiro = Record<string, any>

interface GraficoProps {
  title: string
  /** Dados já carregados pelo componente pai */
  data: PontoFinanceiro[]
  /** Séries numéricas a serem exibidas no gráfico */
  series: SerieConfig[]
  /** Nome do campo de data no objeto (padrão: 'data') */
  dateKey?: string
  /** Altura da área do gráfico (sobrescreve o height do CSS da placeholder) */
  height?: number
  /** Mensagem quando não houver dados no período */
  emptyMessage?: string
}

function parseDate(value: any): Date | null {
  if (!value) return null
  const d = new Date(value)
  if (Number.isNaN(d.getTime())) return null
  return d
}

export function Grafico({
  title,
  data,
  series,
  dateKey = 'data',
  height = 220,
  emptyMessage = 'Nenhum dado encontrado para o período selecionado.',
}: GraficoProps) {
  const [dataInicio, setDataInicio] = useState<string>('')
  const [dataFim, setDataFim] = useState<string>('')

  const dadosFiltrados = useMemo(() => {
    if (!dataInicio && !dataFim) return data

    const inicioDate = dataInicio ? new Date(dataInicio) : null
    const fimDate = dataFim ? new Date(dataFim) : null

    return data.filter((item) => {
      const d = parseDate(item[dateKey])
      if (!d) return false

      if (inicioDate && d < inicioDate) return false
      if (fimDate && d > fimDate) return false
      return true
    })
  }, [data, dataInicio, dataFim, dateKey])

  const temDados = dadosFiltrados.length > 0 && series.length > 0

  return (
    <div className="chart-card">
      {/* título + filtros de período */}
      <div className="chart-header">
        <div className="chart-title">{title}</div>

        <div className="chart-filters">
          <label className="chart-filter-item">
            <span>De:</span>
            <input
              type="date"
              value={dataInicio}
              onChange={(e) => setDataInicio(e.target.value)}
            />
          </label>

          <label className="chart-filter-item">
            <span>Até:</span>
            <input
              type="date"
              value={dataFim}
              onChange={(e) => setDataFim(e.target.value)}
            />
          </label>

          {(dataInicio || dataFim) && (
            <button
              type="button"
              className="chart-clear-button"
              onClick={() => {
                setDataInicio('')
                setDataFim('')
              }}
            >
              Limpar
            </button>
          )}
        </div>
      </div>

      {/* reaproveitando a .chart-placeholder como “área do gráfico” */}
      <div className="chart-placeholder" style={{ height }}>
        {!temDados ? (
          <span>{emptyMessage}</span>
        ) : (
          <div style={{ width: '100%', height: '100%' }}>
            <ResponsiveContainer>
              <LineChart data={dadosFiltrados}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey={dateKey}
                  tickFormatter={(value) => {
                    const d = parseDate(value)
                    return d ? d.toLocaleDateString('pt-BR') : String(value)
                  }}
                  minTickGap={20}
                />
                <YAxis />
                <Tooltip
                  labelFormatter={(value) => {
                    const d = parseDate(value)
                    return d ? d.toLocaleDateString('pt-BR') : String(value)
                  }}
                />
                <Legend />
                {series.map((serie) => (
                  <Line
                    key={serie.key}
                    type="monotone"
                    dataKey={serie.key}
                    name={serie.label}
                    dot={false}
                  />
                ))}
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  )
}
