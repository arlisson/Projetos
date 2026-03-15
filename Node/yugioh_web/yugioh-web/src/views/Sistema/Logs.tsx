import { useEffect, useMemo, useState } from 'react'
import { Topbar } from '../../components/topBar'
import { Footer } from '../../components/footer'
import { FormField } from '../../components/formField'
import { Button } from '../../components/botao'
import { Loading } from '../../components/Loading'
import { listarLogs, limparLogs, type LogItem } from '../../services/logger'

function formatarDataHora(valor: string) {
  if (!valor) return '-'

  const data = new Date(valor)
  if (Number.isNaN(data.getTime())) return valor

  return data.toLocaleString('pt-BR')
}

export function Logs() {
  const [logs, setLogs] = useState<LogItem[]>([])
  const [busca, setBusca] = useState('')
  const [nivel, setNivel] = useState('TODOS')
  const [carregando, setCarregando] = useState(true)
  const [limpando, setLimpando] = useState(false)

  async function carregarLogs() {
    setCarregando(true)
    try {
      const dados = await listarLogs()
      setLogs(dados)
    } finally {
      setCarregando(false)
    }
  }

  useEffect(() => {
    void carregarLogs()
  }, [])

  async function handleLimparLogs() {
    const confirmar = window.confirm(
      'Deseja realmente apagar todos os logs?',
    )

    if (!confirmar) return

    setLimpando(true)
    try {
      const ok = await limparLogs()

      if (!ok) {
        alert('Não foi possível apagar os logs.')
        return
      }

      setLogs([])
      alert('Logs apagados com sucesso.')
    } finally {
      setLimpando(false)
    }
  }

  const niveisDisponiveis = useMemo(() => {
    const valores = new Set<string>()
    logs.forEach((log) => valores.add((log.level || '').toUpperCase()))
    return ['TODOS', ...Array.from(valores).filter(Boolean)]
  }, [logs])

  const logsFiltrados = useMemo(() => {
    const termo = busca.trim().toLowerCase()

    return logs.filter((log) => {
      const bateNivel =
        nivel === 'TODOS' || (log.level || '').toUpperCase() === nivel

      const bateBusca =
        !termo ||
        (log.message || '').toLowerCase().includes(termo) ||
        (log.timestamp || '').toLowerCase().includes(termo) ||
        (log.raw || '').toLowerCase().includes(termo)

      return bateNivel && bateBusca
    })
  }, [logs, busca, nivel])

  return (
    <div className="app-shell">
      <Topbar pageTitle="Logs do sistema" />

      <main className="form-page-content">
        <section className="form-page-left" style={{ maxWidth: '100%' }}>
          <h2 className="section-title">Visualização de logs</h2>
          <p className="section-subtitle">
            Consulte os registros do sistema, filtre por texto e apague o
            histórico quando necessário.
          </p>

          <div className="form-row-inline">
            <FormField
              label="Buscar nos logs"
              name="buscaLogs"
              kind="texto"
              value={busca}
              onChange={setBusca}
              placeholder="Digite parte da mensagem, data ou conteúdo"
            />

            <div style={{ minWidth: 220 }}>
              <label
                style={{
                  display: 'block',
                  marginBottom: '0.45rem',
                  fontSize: '0.95rem',
                }}
              >
                Nível
              </label>

              <select
                value={nivel}
                onChange={(e) => setNivel(e.target.value)}
                style={{
                  width: '100%',
                  height: '46px',
                  borderRadius: '12px',
                  border: '1px solid rgba(255,255,255,0.08)',
                  background: 'rgba(255,255,255,0.02)',
                  color: 'white',
                  padding: '0 0.9rem',
                  outline: 'none',
                }}
              >
                {niveisDisponiveis.map((item) => (
                  <option key={item} value={item}>
                    {item}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div
            className="form-actions"
            style={{ justifyContent: 'flex-start', marginTop: '1rem' }}
          >
            <Button
              type="button"
              variant="outline"
              onClick={carregarLogs}
              disabled={carregando || limpando}
            >
              Atualizar
            </Button>

            <Button
              type="button"
              variant="danger"
              onClick={handleLimparLogs}
              disabled={carregando || limpando || logs.length === 0}
            >
              {limpando ? 'Apagando...' : 'Apagar logs'}
            </Button>
          </div>

          <div style={{ marginTop: '1.5rem' }}>
            {carregando ? (
              <Loading message="Carregando logs..." />
            ) : logsFiltrados.length === 0 ? (
              <div
                style={{
                  border: '1px solid rgba(255,255,255,0.08)',
                  borderRadius: '12px',
                  padding: '1rem',
                  background: 'rgba(255,255,255,0.02)',
                }}
              >
                Nenhum log encontrado.
              </div>
            ) : (
              <div
                style={{
                  display: 'grid',
                  gap: '0.9rem',
                }}
              >
                {logsFiltrados.map((log, idx) => {
                  const nivelAtual = (log.level || '').toUpperCase()
                  const isError = nivelAtual === 'ERROR'
                  const isWarn = nivelAtual === 'WARN'

                  return (
                    <div
                      key={`${log.timestamp}-${idx}`}
                      style={{
                        border: '1px solid rgba(255,255,255,0.08)',
                        borderLeft: isError
                          ? '4px solid #ff4d4d'
                          : isWarn
                          ? '4px solid #f59e0b'
                          : '4px solid #57c5ea',
                        borderRadius: '12px',
                        padding: '1rem',
                        background: 'rgba(255,255,255,0.02)',
                      }}
                    >
                      <div
                        style={{
                          display: 'flex',
                          justifyContent: 'space-between',
                          gap: '1rem',
                          marginBottom: '0.65rem',
                          flexWrap: 'wrap',
                        }}
                      >
                        <strong>{nivelAtual || 'INFO'}</strong>
                        <span style={{ opacity: 0.85 }}>
                          {formatarDataHora(log.timestamp)}
                        </span>
                      </div>

                      <div
                        style={{
                          whiteSpace: 'pre-wrap',
                          wordBreak: 'break-word',
                          lineHeight: 1.5,
                        }}
                      >
                        {log.message || log.raw || '-'}
                      </div>
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        </section>
      </main>

      <Footer />
    </div>
  )
}