import { useEffect, useState } from 'react'
import { open, save } from '@tauri-apps/plugin-dialog'
import { Topbar } from '../../components/topBar'
import { Footer } from '../../components/footer'
import { Button } from '../../components/botao'
import {
  clearDatabaseData,
  exportDatabase,
  getDatabaseInfo,
  importDatabase,
  type ClearDatabaseMode,
  type DatabaseInfo,
} from '../../Database/dbAdmin'
import { logError, logInfo } from '../../services/logger'

const infoInicial: DatabaseInfo = {
  dbPath: '',
  exists: false,
  fileSizeBytes: 0,
  fileSizeLabel: '0 B',
  lastModified: '',
  counts: {
    carta: 0,
    produto: 0,
    venda: 0,
    venda_produto: 0,
    historico_precos: 0,
    historico_lucro: 0,
    colecao: 0,
    raridade: 0,
    qualidade: 0,
  },
}

export default function BancoDeDados() {
  const [info, setInfo] = useState<DatabaseInfo>(infoInicial)
  const [carregando, setCarregando] = useState(false)
  const [processandoArquivo, setProcessandoArquivo] = useState(false)
  const [processandoLimpeza, setProcessandoLimpeza] = useState(false)

  const [clearMode, setClearMode] =
    useState<ClearDatabaseMode>('operacional')

  const [mensagem, setMensagem] = useState('')
  const [erro, setErro] = useState('')

  const [modalImportacaoAberto, setModalImportacaoAberto] = useState(false)
  const [modalLimpezaAberto, setModalLimpezaAberto] = useState(false)
  const [arquivoImportacaoPendente, setArquivoImportacaoPendente] = useState('')

  async function carregarInfo() {
    setCarregando(true)
    setErro('')

    try {
      const data = await getDatabaseInfo()
      setInfo(data)
    } catch (e) {
      await logError('Erro ao carregar informações do banco: ' + String(e))
      setErro('Não foi possível carregar as informações do banco.')
    } finally {
      setCarregando(false)
    }
  }

  useEffect(() => {
    carregarInfo()
  }, [])

  async function handleEscolherExportacao() {
    setMensagem('')
    setErro('')
    setProcessandoArquivo(true)

    try {
      const destino = await save({
        title: 'Exportar banco SQLite',
        defaultPath: 'yugioh_backup.db',
        filters: [
          {
            name: 'SQLite Database',
            extensions: ['db', 'sqlite'],
          },
        ],
      })

      if (!destino) {
        return
      }

      await exportDatabase(destino)
      await logInfo('Banco exportado com sucesso para: ' + destino)
      setMensagem('Banco exportado com sucesso.')
      await carregarInfo()
    } catch (e) {
      await logError('Erro ao exportar banco: ' + String(e))
      setErro('Falha ao exportar o banco.')
    } finally {
      setProcessandoArquivo(false)
    }
  }

  async function handleEscolherImportacao() {
    setMensagem('')
    setErro('')
    setProcessandoArquivo(true)

    try {
      const origem = await open({
        title: 'Selecionar banco SQLite',
        multiple: false,
        directory: false,
        filters: [
          {
            name: 'SQLite Database',
            extensions: ['db', 'sqlite'],
          },
        ],
      })

      if (!origem || Array.isArray(origem)) {
        return
      }

      setArquivoImportacaoPendente(origem)
      setModalImportacaoAberto(true)
    } catch (e) {
      await logError('Erro ao selecionar arquivo para importação: ' + String(e))
      setErro('Falha ao selecionar o arquivo de importação.')
    } finally {
      setProcessandoArquivo(false)
    }
  }

  async function confirmarImportacao() {
    if (!arquivoImportacaoPendente) return

    setMensagem('')
    setErro('')
    setProcessandoArquivo(true)

    try {
      await importDatabase(arquivoImportacaoPendente)
      await logInfo('Banco importado com sucesso de: ' + arquivoImportacaoPendente)
      setMensagem('Banco importado com sucesso.')
      setModalImportacaoAberto(false)
      setArquivoImportacaoPendente('')
      await carregarInfo()
    } catch (e) {
      await logError('Erro ao importar banco: ' + String(e))
      setErro('Falha ao importar o banco.')
    } finally {
      setProcessandoArquivo(false)
    }
  }

  function cancelarImportacao() {
    if (processandoArquivo) return
    setModalImportacaoAberto(false)
    setArquivoImportacaoPendente('')
  }

  function handleLimparDados() {
    setMensagem('')
    setErro('')
    setModalLimpezaAberto(true)
  }

  async function confirmarLimpeza() {
    setMensagem('')
    setErro('')
    setProcessandoLimpeza(true)

    try {
      await clearDatabaseData(clearMode)
      await logInfo(`Limpeza de banco executada. Modo: ${clearMode}`)
      setMensagem('Dados do banco apagados com sucesso.')
      setModalLimpezaAberto(false)
      await carregarInfo()
    } catch (e) {
      await logError('Erro ao limpar dados do banco: ' + String(e))
      setErro('Falha ao apagar os dados do banco.')
    } finally {
      setProcessandoLimpeza(false)
    }
  }

  function cancelarLimpeza() {
    if (processandoLimpeza) return
    setModalLimpezaAberto(false)
  }

  const descricaoLimpeza =
    clearMode === 'operacional'
      ? 'Você está prestes a limpar cartas, produtos, vendas e históricos, mantendo coleções, raridades e qualidades.'
      : 'Você está prestes a limpar todo o conteúdo do banco, incluindo coleções, raridades e qualidades, mantendo apenas a estrutura.'

  return (
    <div className="app-shell">
      <Topbar pageTitle="Banco de dados" />

      <main className="dashboard-content">
        <div
          className="section-header"
          style={{ alignItems: 'center', marginBottom: '1rem' }}
        >
          <div>
            <div className="section-title">Banco de dados</div>
            <div className="section-subtitle">
              Exporte, importe e limpe os dados do SQLite preservando a estrutura.
            </div>
          </div>

          <Button
            type="button"
            variant="outline"
            onClick={carregarInfo}
            disabled={carregando || processandoArquivo || processandoLimpeza}
          >
            {carregando ? 'Atualizando...' : 'Atualizar informações'}
          </Button>
        </div>

        {mensagem ? (
          <div className="info-banner" style={{ marginTop: '1rem' }}>
            <div className="info-banner-title">{mensagem}</div>
          </div>
        ) : null}

        {erro ? (
          <div
            className="info-banner"
            style={{
              marginTop: '1rem',
              borderColor: '#7f1d1d',
              background: 'rgba(239, 68, 68, 0.08)',
            }}
          >
            <div className="info-banner-title">{erro}</div>
          </div>
        ) : null}

        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'minmax(320px, 1.2fr) minmax(320px, 0.8fr)',
            gap: '1rem',
            marginTop: '1rem',
          }}
        >
          <section className="summary-card" style={{ marginBottom: 0 }}>
            <div className="section-title">Arquivo atual</div>
            <div className="section-subtitle">
              Informações do banco SQLite em uso pela aplicação.
            </div>

            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(3, minmax(120px, 1fr))',
                gap: '0.75rem',
                marginTop: '1rem',
              }}
            >
              <div
                style={{
                  border: '1px solid var(--color-border)',
                  borderRadius: '10px',
                  padding: '0.85rem',
                }}
              >
                <div className="summary-label">Arquivo encontrado</div>
                <div className="summary-value" style={{ fontSize: '1.1rem' }}>
                  {info.exists ? 'Sim' : 'Não'}
                </div>
              </div>

              <div
                style={{
                  border: '1px solid var(--color-border)',
                  borderRadius: '10px',
                  padding: '0.85rem',
                }}
              >
                <div className="summary-label">Tamanho</div>
                <div className="summary-value" style={{ fontSize: '1.1rem' }}>
                  {info.fileSizeLabel}
                </div>
              </div>

              <div
                style={{
                  border: '1px solid var(--color-border)',
                  borderRadius: '10px',
                  padding: '0.85rem',
                }}
              >
                <div className="summary-label">Última modificação</div>
                <div
                  className="summary-value"
                  style={{ fontSize: '0.95rem', lineHeight: 1.4 }}
                >
                  {info.lastModified || '-'}
                </div>
              </div>
            </div>

            <div style={{ marginTop: '1rem' }}>
              <div className="summary-label" style={{ marginBottom: '0.4rem' }}>
                Caminho do banco
              </div>
              <div
                style={{
                  border: '1px solid var(--color-border)',
                  borderRadius: '10px',
                  padding: '0.85rem',
                  background: 'rgba(15, 23, 42, 0.45)',
                  wordBreak: 'break-word',
                  fontSize: '0.85rem',
                  color: 'var(--color-text)',
                }}
              >
                {info.dbPath || '-'}
              </div>
            </div>
          </section>

          <section className="summary-card" style={{ marginBottom: 0 }}>
            <div className="section-title">Ações de arquivo</div>
            <div className="section-subtitle">
              Use diálogos nativos para importar ou exportar o banco.
            </div>

            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '0.85rem',
                marginTop: '1rem',
              }}
            >
              <div
                style={{
                  border: '1px solid var(--color-border)',
                  borderRadius: '10px',
                  padding: '0.9rem',
                }}
              >
                <div className="summary-label" style={{ marginBottom: '0.35rem' }}>
                  Exportação
                </div>
                <div
                  style={{
                    fontSize: '0.84rem',
                    color: 'var(--color-text-muted)',
                    marginBottom: '0.75rem',
                  }}
                >
                  Gera uma cópia do banco atual em um local escolhido por você.
                </div>
                <Button
                  type="button"
                  onClick={handleEscolherExportacao}
                  disabled={processandoArquivo || carregando || processandoLimpeza}
                  fullWidth
                >
                  {processandoArquivo ? 'Processando...' : 'Exportar banco'}
                </Button>
              </div>

              <div
                style={{
                  border: '1px solid var(--color-border)',
                  borderRadius: '10px',
                  padding: '0.9rem',
                }}
              >
                <div className="summary-label" style={{ marginBottom: '0.35rem' }}>
                  Importação
                </div>
                <div
                  style={{
                    fontSize: '0.84rem',
                    color: 'var(--color-text-muted)',
                    marginBottom: '0.75rem',
                  }}
                >
                  Substitui o banco atual por outro arquivo SQLite selecionado.
                </div>
                <Button
                  type="button"
                  variant="outline"
                  onClick={handleEscolherImportacao}
                  disabled={processandoArquivo || carregando || processandoLimpeza}
                  fullWidth
                >
                  {processandoArquivo ? 'Processando...' : 'Importar banco'}
                </Button>
              </div>
            </div>
          </section>
        </div>

        <section className="section-block">
          <div className="section-title">Resumo do conteúdo</div>
          <div className="section-subtitle">
            Totais por tabela principal do banco atual.
          </div>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(170px, 1fr))',
              gap: '0.9rem',
              marginTop: '1rem',
            }}
          >
            {[
              ['Cartas', info.counts.carta],
              ['Produtos', info.counts.produto],
              ['Vendas de cartas', info.counts.venda],
              ['Vendas de produtos', info.counts.venda_produto],
              ['Histórico de preços', info.counts.historico_precos],
              ['Histórico de lucro', info.counts.historico_lucro],
              ['Coleções', info.counts.colecao],
              ['Raridades', info.counts.raridade],
              ['Qualidades', info.counts.qualidade],
            ].map(([label, value]) => (
              <div className="summary-card" key={String(label)} style={{ marginBottom: 0 }}>
                <div className="summary-label">{label}</div>
                <div className="summary-value">{value}</div>
              </div>
            ))}
          </div>
        </section>

        <section className="section-block">
          <div className="section-title">Zona de risco</div>
          <div className="section-subtitle">
            Apaga somente os dados. A estrutura do banco é preservada.
          </div>

          <div
            className="summary-card"
            style={{
              marginTop: '1rem',
              borderColor: 'rgba(239, 68, 68, 0.35)',
            }}
          >
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'minmax(320px, 1fr) auto',
                gap: '1rem',
                alignItems: 'end',
              }}
            >
              <div className="form-field" style={{ marginBottom: 0 }}>
                <label className="form-field-label">Modo de limpeza</label>

                <div
                  style={{
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '0.65rem',
                    marginTop: '0.5rem',
                  }}
                >
                  <label style={{ display: 'flex', gap: '0.6rem', alignItems: 'flex-start' }}>
                    <input
                      type="radio"
                      name="clear-mode"
                      checked={clearMode === 'operacional'}
                      onChange={() => setClearMode('operacional')}
                    />
                    <span style={{ lineHeight: 1.4 }}>
                      Limpar apenas movimentos: cartas, produtos, vendas e históricos.
                    </span>
                  </label>

                  <label style={{ display: 'flex', gap: '0.6rem', alignItems: 'flex-start' }}>
                    <input
                      type="radio"
                      name="clear-mode"
                      checked={clearMode === 'completo'}
                      onChange={() => setClearMode('completo')}
                    />
                    <span style={{ lineHeight: 1.4 }}>
                      Limpar todo o conteúdo: inclui coleções, raridades e qualidades.
                    </span>
                  </label>
                </div>
              </div>

              <div>
                <Button
                  type="button"
                  variant="danger"
                  onClick={handleLimparDados}
                  disabled={carregando || processandoArquivo || processandoLimpeza}
                >
                  {processandoLimpeza ? 'Apagando...' : 'Apagar dados'}
                </Button>
              </div>
            </div>
          </div>
        </section>
      </main>

      {modalImportacaoAberto && (
        <div className="confirm-modal-backdrop">
          <div className="confirm-modal-card">
            <h3 className="confirm-modal-title">Confirmar importação</h3>
            <p className="confirm-modal-text">
              A importação substituirá o banco atual pelo arquivo selecionado.
              Esta ação não pode ser desfeita.
            </p>

            <div className="confirm-modal-actions">
              <Button
                type="button"
                variant="outline"
                onClick={cancelarImportacao}
                disabled={processandoArquivo}
              >
                Cancelar
              </Button>

              <Button
                type="button"
                onClick={confirmarImportacao}
                disabled={processandoArquivo}
              >
                {processandoArquivo ? 'Importando...' : 'Confirmar'}
              </Button>
            </div>
          </div>
        </div>
      )}

      {modalLimpezaAberto && (
        <div className="confirm-modal-backdrop">
          <div className="confirm-modal-card">
            <h3 className="confirm-modal-title">Confirmar limpeza</h3>
            <p className="confirm-modal-text">
              {descricaoLimpeza} Esta ação não pode ser desfeita.
            </p>

            <div className="confirm-modal-actions">
              <Button
                type="button"
                variant="outline"
                onClick={cancelarLimpeza}
                disabled={processandoLimpeza}
              >
                Cancelar
              </Button>

              <Button
                type="button"
                variant="danger"
                onClick={confirmarLimpeza}
                disabled={processandoLimpeza}
              >
                {processandoLimpeza ? 'Apagando...' : 'Confirmar'}
              </Button>
            </div>
          </div>
        </div>
      )}

      <Footer />
    </div>
  )
}