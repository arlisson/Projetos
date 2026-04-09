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
  const [modalLimpezaAberto, setModalLimpezaAberto] = useState(false)

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

  function handleLimparLogs() {
    setModalLimpezaAberto(true)
  }

  async function confirmarLimpezaLogs() {
    if (limpando) return

    setLimpando(true)
    try {
      const ok = await limparLogs()

      if (!ok) {
        alert('Não foi possível apagar os logs.')
        return
      }

      setLogs([])
      setModalLimpezaAberto(false)
      alert('Logs apagados com sucesso.')
    } finally {
      setLimpando(false)
    }
  }

  function cancelarLimpezaLogs() {
    if (limpando) return
    setModalLimpezaAberto(false)
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
                  color: 'var(--color-text)',
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
                  color: '#f8fafc',
                  padding: '0 0.9rem',
                  outline: 'none',
                  appearance: 'none',
                  WebkitAppearance: 'none',
                  MozAppearance: 'none',
                  backgroundImage:
                    "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 20 20' fill='none'><path d='M6 8L10 12L14 8' stroke='%23f8fafc' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'/></svg>\")",
                  backgroundRepeat: 'no-repeat',
                  backgroundPosition: 'right 0.9rem center',
                  paddingRight: '2.4rem',
                }}
              >
                {niveisDisponiveis.map((item) => (
                  <option
                    key={item}
                    value={item}
                    style={{
                      background: '#0f172a',
                      color: '#f8fafc',
                    }}
                  >
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
                  color: 'var(--color-text)',
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
                        <strong style={{ color: '#f8fafc' }}>
                          {nivelAtual || 'INFO'}
                        </strong>
                        <span style={{ opacity: 0.85, color: '#cbd5e1' }}>
                          {formatarDataHora(log.timestamp)}
                        </span>
                      </div>

                      <div
                        style={{
                          whiteSpace: 'pre-wrap',
                          wordBreak: 'break-word',
                          lineHeight: 1.5,
                          color: '#e5e7eb',
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

      {modalLimpezaAberto && (
        <div className="confirm-modal-backdrop">
          <div className="confirm-modal-card">
            <h3 className="confirm-modal-title">Confirmar exclusão</h3>
            <p className="confirm-modal-text">
              Deseja realmente apagar todos os logs? Esta ação não pode ser
              desfeita.
            </p>

            <div className="confirm-modal-actions">
              <Button
                type="button"
                variant="outline"
                onClick={cancelarLimpezaLogs}
                disabled={limpando}
              >
                Cancelar
              </Button>

              <Button
                type="button"
                variant="danger"
                onClick={confirmarLimpezaLogs}
                disabled={limpando}
              >
                {limpando ? 'Apagando...' : 'Confirmar'}
              </Button>
            </div>
          </div>
        </div>
      )}

      <Footer />
    </div>
  )
}