import { useEffect, useMemo, useState } from 'react'
import { Topbar } from '../../components/topBar'
import { Footer } from '../../components/footer'
import { Button } from '../../components/botao'
import { FormField } from '../../components/formField'
import {
  atualizarColecao,
  excluirColecao,
  inserirColecao,
  listarColecoes,
  type ColecaoDB,
} from '../../Database/db'
import { logError, logInfo } from '../../services/logger'

type EstadoEdicao = {
  id_colecao: number
  nome: string
  codigo: string
} | null

export default function Colecoes() {
  const [colecoes, setColecoes] = useState<ColecaoDB[]>([])
  const [novoNome, setNovoNome] = useState('')
  const [novoCodigo, setNovoCodigo] = useState('')
  const [filtro, setFiltro] = useState('')
  const [edicao, setEdicao] = useState<EstadoEdicao>(null)
  const [carregando, setCarregando] = useState(false)
  const [mensagem, setMensagem] = useState('')
  const [erro, setErro] = useState('')
  const [colecaoExclusaoPendente, setColecaoExclusaoPendente] =
    useState<ColecaoDB | null>(null)
  const [excluindo, setExcluindo] = useState(false)

  async function carregarDados() {
    setCarregando(true)
    setErro('')

    try {
      const dados = await listarColecoes()
      setColecoes(dados)
    } catch (e) {
      await logError('Erro ao carregar colecoes: ' + String(e))
      setErro('Erro ao carregar as colecoes.')
    } finally {
      setCarregando(false)
    }
  }

  useEffect(() => {
    void carregarDados()
  }, [])

  const colecoesFiltradas = useMemo(() => {
    const termo = filtro.trim().toUpperCase()
    if (!termo) return colecoes

    return colecoes.filter(
      (item) =>
        item.nome.toUpperCase().includes(termo) ||
        String(item.codigo || '').toUpperCase().includes(termo),
    )
  }, [colecoes, filtro])

  async function handleInserir() {
    setMensagem('')
    setErro('')

    const nomeLimpo = novoNome.trim()
    const codigoLimpo = novoCodigo.trim()

    if (!nomeLimpo) {
      setErro('Informe o nome da colecao.')
      return
    }

    const id = await inserirColecao(nomeLimpo, codigoLimpo)

    if (!id) {
      setErro('Nao foi possivel inserir a colecao. Verifique se ela ja existe.')
      return
    }

    await logInfo(`Colecao inserida com sucesso: ${nomeLimpo}`)
    setNovoNome('')
    setNovoCodigo('')
    await carregarDados()
    setMensagem('Colecao inserida com sucesso.')
  }

  async function handleSalvarEdicao() {
    setMensagem('')
    setErro('')

    if (!edicao || !edicao.nome.trim()) {
      setErro('Informe o nome da colecao.')
      return
    }

    const ok = await atualizarColecao(
      edicao.id_colecao,
      edicao.nome,
      edicao.codigo,
    )

    if (!ok) {
      setErro(
        'Nao foi possivel atualizar a colecao. Verifique se ja existe outra colecao com esse nome.',
      )
      return
    }

    await logInfo(`Colecao atualizada com sucesso: id=${edicao.id_colecao}`)
    setEdicao(null)
    await carregarDados()
    setMensagem('Colecao atualizada com sucesso.')
  }

  function handleExcluir(item: ColecaoDB) {
    setMensagem('')
    setErro('')
    setColecaoExclusaoPendente(item)
  }

  function cancelarExclusao() {
    if (excluindo) return
    setColecaoExclusaoPendente(null)
  }

  async function confirmarExclusao() {
    if (!colecaoExclusaoPendente || excluindo) return

    setMensagem('')
    setErro('')
    setExcluindo(true)

    const resultado = await excluirColecao(
      colecaoExclusaoPendente.id_colecao,
    )

    if (!resultado.ok) {
      setErro(resultado.motivo || 'Nao foi possivel excluir a colecao.')
      setExcluindo(false)
      return
    }

    await logInfo(
      `Colecao excluida com sucesso: id=${colecaoExclusaoPendente.id_colecao}`,
    )
    setColecaoExclusaoPendente(null)
    setExcluindo(false)
    await carregarDados()
    setMensagem('Colecao excluida com sucesso.')
  }

  return (
    <div className="app-shell">
      <Topbar pageTitle="Gerenciar colecoes" />

      <main className="dashboard-content">
        <div className="section-title">Gerenciar colecoes</div>
        <div className="section-subtitle">
          Cadastre, edite e exclua colecoes usadas no cadastro de cartas.
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

        <div style={{ display: 'flex', gap: '0.75rem', marginTop: '1.2rem' }}>
          <Button
            type="button"
            variant="ghost"
            onClick={carregarDados}
            disabled={carregando}
          >
            {carregando ? 'Carregando...' : 'Atualizar'}
          </Button>
        </div>

        <section className="section-block">
          <div className="section-header">
            <div>
              <div className="section-title">Colecoes</div>
              <div className="section-subtitle">
                Informe o nome da colecao e, se houver, o codigo abreviado.
              </div>
            </div>
          </div>

          <div className="summary-card" style={{ marginTop: '1rem' }}>
            <div className="form-row-inline">
              <div style={{ flex: 2 }}>
                <FormField
                  label="Nova colecao"
                  name="nova-colecao"
                  value={novoNome}
                  onChange={setNovoNome}
                  placeholder="Digite o nome da colecao"
                />
              </div>

              <div style={{ flex: 1 }}>
                <FormField
                  label="Codigo"
                  name="novo-codigo"
                  value={novoCodigo}
                  onChange={setNovoCodigo}
                  placeholder="Ex.: LOB"
                />
              </div>

              <Button type="button" onClick={handleInserir}>
                Inserir colecao
              </Button>
            </div>
          </div>

          <div className="summary-card" style={{ marginTop: '1rem' }}>
            <FormField
              label="Filtrar colecoes"
              name="filtro-colecao"
              value={filtro}
              onChange={setFiltro}
              placeholder="Digite para filtrar por nome ou codigo"
            />
          </div>

          <div className="summary-card" style={{ marginTop: '1rem' }}>
            {colecoesFiltradas.length === 0 ? (
              <div className="section-subtitle">Nenhum registro encontrado.</div>
            ) : (
              <table className="table" style={{ width: '100%' }}>
                <thead>
                  <tr>
                    <th style={{ width: '100px' }}>ID</th>
                    <th>Nome</th>
                    <th style={{ width: '180px' }}>Codigo</th>
                    <th style={{ width: '280px' }}>Acoes</th>
                  </tr>
                </thead>
                <tbody>
                  {colecoesFiltradas.map((item) => {
                    const emEdicao = edicao?.id_colecao === item.id_colecao

                    return (
                      <tr key={item.id_colecao}>
                        <td>{item.id_colecao}</td>

                        <td>
                          {emEdicao && edicao ? (
                            <FormField
                              label=""
                              name={`editar-colecao-${item.id_colecao}`}
                              value={edicao.nome}
                              onChange={(value) =>
                                setEdicao({
                                  ...edicao,
                                  nome: value,
                                })
                              }
                              placeholder="Nome da colecao"
                            />
                          ) : (
                            item.nome
                          )}
                        </td>

                        <td>
                          {emEdicao && edicao ? (
                            <FormField
                              label=""
                              name={`editar-codigo-${item.id_colecao}`}
                              value={edicao.codigo}
                              onChange={(value) =>
                                setEdicao({
                                  ...edicao,
                                  codigo: value,
                                })
                              }
                              placeholder="Codigo"
                            />
                          ) : (
                            item.codigo || '-'
                          )}
                        </td>

                        <td>
                          <div
                            style={{
                              display: 'flex',
                              gap: '0.5rem',
                              justifyContent: 'center',
                              flexWrap: 'wrap',
                            }}
                          >
                            {emEdicao ? (
                              <>
                                <Button type="button" onClick={handleSalvarEdicao}>
                                  Salvar
                                </Button>

                                <Button
                                  type="button"
                                  variant="outline"
                                  onClick={() => setEdicao(null)}
                                >
                                  Cancelar
                                </Button>
                              </>
                            ) : (
                              <>
                                <Button
                                  type="button"
                                  variant="outline"
                                  onClick={() =>
                                    setEdicao({
                                      id_colecao: item.id_colecao,
                                      nome: item.nome,
                                      codigo: item.codigo || '',
                                    })
                                  }
                                >
                                  Editar
                                </Button>

                                <Button
                                  type="button"
                                  variant="danger"
                                  onClick={() => handleExcluir(item)}
                                >
                                  Excluir
                                </Button>
                              </>
                            )}
                          </div>
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            )}
          </div>
        </section>
      </main>

      {colecaoExclusaoPendente && (
        <div className="confirm-modal-backdrop">
          <div className="confirm-modal-card">
            <h3 className="confirm-modal-title">Confirmar exclusao</h3>
            <p className="confirm-modal-text">
              Deseja realmente excluir a colecao "{colecaoExclusaoPendente.nome}"?
              Esta acao nao pode ser desfeita.
            </p>

            <div className="confirm-modal-actions">
              <Button
                type="button"
                variant="outline"
                onClick={cancelarExclusao}
                disabled={excluindo}
              >
                Cancelar
              </Button>

              <Button
                type="button"
                variant="danger"
                onClick={confirmarExclusao}
                disabled={excluindo}
              >
                {excluindo ? 'Excluindo...' : 'Confirmar'}
              </Button>
            </div>
          </div>
        </div>
      )}

      <Footer />
    </div>
  )
}
