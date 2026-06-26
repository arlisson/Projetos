import { useEffect, useMemo, useState } from 'react'
import { Topbar } from '../../components/topBar'
import { Footer } from '../../components/footer'
import { Button } from '../../components/botao'
import { FormField } from '../../components/formField'
import { PageHelpButton } from '../../components/PageHelpButton'
import {
  atualizarCadastroBase,
  excluirCadastroBase,
  inserirCadastroBase,
  listarCadastroBase,
  type ItemCadastroBase,
  type TipoCadastroBase,
} from '../../Database/db'
import { logError, logInfo } from '../../services/logger'

type AbaAtiva = 'raridade' | 'qualidade'

type EstadoEdicao = {
  id: number
  nome: string
} | null

function tituloPlural(tipo: TipoCadastroBase): string {
  return tipo === 'raridade' ? 'Raridades' : 'Qualidades'
}

function tituloSingular(tipo: TipoCadastroBase): string {
  return tipo === 'raridade' ? 'Raridade' : 'Qualidade'
}

function nomeSingular(tipo: TipoCadastroBase): string {
  return tipo === 'raridade' ? 'raridade' : 'qualidade'
}

export default function GerenciarRaridadeQualidade() {
  const [abaAtiva, setAbaAtiva] = useState<AbaAtiva>('raridade')

  const [raridades, setRaridades] = useState<ItemCadastroBase[]>([])
  const [qualidades, setQualidades] = useState<ItemCadastroBase[]>([])

  const [novoNomeRaridade, setNovoNomeRaridade] = useState('')
  const [novoNomeQualidade, setNovoNomeQualidade] = useState('')

  const [filtroRaridade, setFiltroRaridade] = useState('')
  const [filtroQualidade, setFiltroQualidade] = useState('')

  const [edicaoRaridade, setEdicaoRaridade] = useState<EstadoEdicao>(null)
  const [edicaoQualidade, setEdicaoQualidade] = useState<EstadoEdicao>(null)

  const [carregando, setCarregando] = useState(false)
  const [mensagem, setMensagem] = useState<string>('')
  const [erro, setErro] = useState<string>('')

  async function carregarDados() {
    setCarregando(true)
    setErro('')

    try {
      const [listaRaridades, listaQualidades] = await Promise.all([
        listarCadastroBase('raridade'),
        listarCadastroBase('qualidade'),
      ])

      setRaridades(listaRaridades)
      setQualidades(listaQualidades)
    } catch (e) {
      await logError('Erro ao carregar raridade/qualidade: ' + String(e))
      setErro('Erro ao carregar os dados.')
    } finally {
      setCarregando(false)
    }
  }

  useEffect(() => {
    carregarDados()
  }, [])

  const raridadesFiltradas = useMemo(() => {
    const termo = filtroRaridade.trim().toUpperCase()
    if (!termo) return raridades
    return raridades.filter((item) => item.nome.toUpperCase().includes(termo))
  }, [raridades, filtroRaridade])

  const qualidadesFiltradas = useMemo(() => {
    const termo = filtroQualidade.trim().toUpperCase()
    if (!termo) return qualidades
    return qualidades.filter((item) => item.nome.toUpperCase().includes(termo))
  }, [qualidades, filtroQualidade])

  async function handleInserir(tipo: TipoCadastroBase) {
    setMensagem('')
    setErro('')

    const nome = tipo === 'raridade' ? novoNomeRaridade : novoNomeQualidade
    const nomeLimpo = nome.trim()

    if (!nomeLimpo) {
      setErro(`Informe o nome da ${nomeSingular(tipo)}.`)
      return
    }

    const ok = await inserirCadastroBase(tipo, nomeLimpo)

    if (!ok) {
      setErro(
        `Não foi possível inserir a ${nomeSingular(tipo)}. Verifique se ela já existe.`,
      )
      return
    }

    await logInfo(`${tituloSingular(tipo)} inserida com sucesso: ${nomeLimpo}`)

    if (tipo === 'raridade') {
      setNovoNomeRaridade('')
    } else {
      setNovoNomeQualidade('')
    }

    await carregarDados()
    setMensagem(`${tituloSingular(tipo)} inserida com sucesso.`)
  }

  async function handleSalvarEdicao(tipo: TipoCadastroBase) {
    setMensagem('')
    setErro('')

    const edicao = tipo === 'raridade' ? edicaoRaridade : edicaoQualidade

    if (!edicao || !edicao.nome.trim()) {
      setErro(`Informe o nome da ${nomeSingular(tipo)}.`)
      return
    }

    const ok = await atualizarCadastroBase(tipo, edicao.id, edicao.nome)

    if (!ok) {
      setErro(
        `Não foi possível atualizar a ${nomeSingular(tipo)}. Verifique se já existe outro item com esse nome.`,
      )
      return
    }

    await logInfo(
      `${tituloSingular(tipo)} atualizada com sucesso: id=${edicao.id}`,
    )

    if (tipo === 'raridade') {
      setEdicaoRaridade(null)
    } else {
      setEdicaoQualidade(null)
    }

    await carregarDados()
    setMensagem(`${tituloSingular(tipo)} atualizada com sucesso.`)
  }

  async function handleExcluir(tipo: TipoCadastroBase, item: ItemCadastroBase) {
    setMensagem('')
    setErro('')

    const confirmar = window.confirm(
      `Deseja realmente excluir a ${nomeSingular(tipo)} "${item.nome}"?`,
    )

    if (!confirmar) return

    const resultado = await excluirCadastroBase(tipo, item.id)

    if (!resultado.ok) {
      setErro(
        resultado.motivo ||
          `Não foi possível excluir a ${nomeSingular(tipo)}.`,
      )
      return
    }

    await logInfo(
      `${tituloSingular(tipo)} excluída com sucesso: id=${item.id}`,
    )

    await carregarDados()
    setMensagem(`${tituloSingular(tipo)} excluída com sucesso.`)
  }

  function renderSecao(
    tipo: TipoCadastroBase,
    itens: ItemCadastroBase[],
    filtro: string,
    setFiltro: (value: string) => void,
    novoNome: string,
    setNovoNome: (value: string) => void,
    edicao: EstadoEdicao,
    setEdicao: (value: EstadoEdicao) => void,
  ) {
    return (
      <section className="section-block">
        <div className="section-header">
          <div>
            <div className="section-title">{tituloPlural(tipo)}</div>
            <div className="section-subtitle">
              Inserir, editar e excluir {tituloPlural(tipo).toLowerCase()}.
            </div>
          </div>
        </div>

        <div className="summary-card" style={{ marginTop: '1rem' }}>
          <div className="form-row-inline">
            <div style={{ flex: 1 }}>
              <FormField
                label={`Nova ${nomeSingular(tipo)}`}
                name={`nova-${tipo}`}
                value={novoNome}
                onChange={setNovoNome}
                placeholder={`Digite o nome da ${nomeSingular(tipo)}`}
              />
            </div>

            <Button
              type="button"
              onClick={() => handleInserir(tipo)}
            >
              Inserir {nomeSingular(tipo)}
            </Button>
          </div>
        </div>

        <div className="summary-card" style={{ marginTop: '1rem' }}>
          <FormField
            label={`Filtrar ${tituloPlural(tipo).toLowerCase()}`}
            name={`filtro-${tipo}`}
            value={filtro}
            onChange={setFiltro}
            placeholder={`Digite para filtrar ${tituloPlural(tipo).toLowerCase()}`}
          />
        </div>

        <div className="summary-card" style={{ marginTop: '1rem' }}>
          {itens.length === 0 ? (
            <div className="section-subtitle">Nenhum registro encontrado.</div>
          ) : (
            <table className="table" style={{ width: '100%' }}>
              <thead>
                <tr>
                  <th style={{ width: '100px' }}>ID</th>
                  <th>Nome</th>
                  <th style={{ width: '280px' }}>Ações</th>
                </tr>
              </thead>
              <tbody>
                {itens.map((item) => {
                  const emEdicao = edicao?.id === item.id

                  return (
                    <tr key={`${tipo}-${item.id}`}>
                      <td>{item.id}</td>

                      <td>
                        {emEdicao ? (
                          <FormField
                            label=""
                            name={`editar-${tipo}-${item.id}`}
                            value={edicao.nome}
                            onChange={(value) =>
                              setEdicao({
                                id: item.id,
                                nome: value,
                              })
                            }
                            placeholder={`Nome da ${nomeSingular(tipo)}`}
                          />
                        ) : (
                          item.nome
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
                              <Button
                                type="button"
                                onClick={() => handleSalvarEdicao(tipo)}
                              >
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
                                    id: item.id,
                                    nome: item.nome,
                                  })
                                }
                              >
                                Editar
                              </Button>

                              <Button
                                type="button"
                                variant="danger"
                                onClick={() => handleExcluir(tipo, item)}
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
    )
  }

  return (
    <div className="app-shell">
      <Topbar pageTitle="Gerenciar raridade e qualidade" />

      <main className="dashboard-content">
        <div className="section-title section-title-with-help">
          Gerenciar raridade e qualidade
          <PageHelpButton
            configKey="gestao.raridadeQualidade"
            fallbackTitle="Como gerenciar raridades e qualidades"
          />
        </div>
        <div className="section-subtitle">
          Tela única para manutenção de raridades e qualidades.
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
            variant={abaAtiva === 'raridade' ? 'solid' : 'outline'}
            onClick={() => setAbaAtiva('raridade')}
          >
            Raridades
          </Button>

          <Button
            type="button"
            variant={abaAtiva === 'qualidade' ? 'solid' : 'outline'}
            onClick={() => setAbaAtiva('qualidade')}
          >
            Qualidades
          </Button>

          <Button
            type="button"
            variant="ghost"
            onClick={carregarDados}
            disabled={carregando}
          >
            {carregando ? 'Carregando...' : 'Atualizar'}
          </Button>
        </div>

        {abaAtiva === 'raridade'
          ? renderSecao(
              'raridade',
              raridadesFiltradas,
              filtroRaridade,
              setFiltroRaridade,
              novoNomeRaridade,
              setNovoNomeRaridade,
              edicaoRaridade,
              setEdicaoRaridade,
            )
          : renderSecao(
              'qualidade',
              qualidadesFiltradas,
              filtroQualidade,
              setFiltroQualidade,
              novoNomeQualidade,
              setNovoNomeQualidade,
              edicaoQualidade,
              setEdicaoQualidade,
            )}
      </main>

      <Footer />
    </div>
  )
}
