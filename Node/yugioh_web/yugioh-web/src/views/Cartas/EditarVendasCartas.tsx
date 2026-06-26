import { useEffect, useState } from 'react'
import { Topbar } from '../../components/topBar'
import { Footer } from '../../components/footer'
import { FormField } from '../../components/formField'
import { FormSelect } from '../../components/formSelect'
import { Button } from '../../components/botao'
import { PageHelpButton } from '../../components/PageHelpButton'
import {
  listarRaridadeQualidade,
  listarColecoes,
  type QualidadeDB,
  type RaridadeDB,
  type OpcaoSelect,
  buscarQualidadeRaridadeId,
  buscarColecao,
  inserirColecao,
  buscarVendaCartaId,
  atualizarVendaCarta,
  deletarVendaCarta,
  type InserirVendaCartaPayload,
} from '../../Database/db'
import { buscarCartaMyp, type CartaMyP } from '../../../scraping/webScraping'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { logError } from '../../services/logger'

async function buscarCarta(url: string, chave?: string): Promise<CartaMyP[]> {
  const carta = await buscarCartaMyp(url, chave)
  return carta
}

export function EditarVendasCartas() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const idParam = searchParams.get('id')
  const idCarta = idParam ? Number(idParam) : null

  const [dataVenda, setDataVenda] = useState('')
  const [linkCarta, setLinkCarta] = useState('')
  const [nome, setNome] = useState('')
  const [codigo, setCodigo] = useState('')
  const [precoPago, setPrecoPago] = useState('')
  const [precoAtual, setPrecoAtual] = useState('')
  const [dataCompra, setDataCompra] = useState('')
  const [quantidade, setQuantidade] = useState('')
  const [urlImagem, setUrlImagem] = useState('')

  const [origem, setOrigem] = useState('')
  const [raridade, setRaridade] = useState('')
  const [qualidade, setQualidade] = useState('')
  const [colecao, setColecao] = useState('')
  const [opcoesRaridade, setOpcoesRaridade] = useState<OpcaoSelect[]>([])
  const [opcoesQualidade, setOpcoesQualidade] = useState<OpcaoSelect[]>([])
  const [opcoesColecao, setOpcoesColecao] = useState<OpcaoSelect[]>([])
  const [precoVenda, setPrecoVenda] = useState('')

  const [buscandoScraping, setBuscandoScraping] = useState(false)
  const [modalAtualizarAberto, setModalAtualizarAberto] = useState(false)
  const [modalExcluirAberto, setModalExcluirAberto] = useState(false)
  const [salvandoAtualizacao, setSalvandoAtualizacao] = useState(false)
  const [excluindoVenda, setExcluindoVenda] = useState(false)

  useEffect(() => {
    if (!idCarta) return

    async function carregarDadosCarta() {
      try {
        const carta = await buscarVendaCartaId(idCarta!)

        if (carta) {
          setLinkCarta(carta.link_site || '')
          setNome(carta.nome || '')
          setCodigo(carta.codigo || '')
          setPrecoPago(
            carta.preco_da_compra !== null && carta.preco_da_compra !== undefined
              ? String(carta.preco_da_compra)
              : '',
          )
          setPrecoAtual(
            carta.preco_atual !== null && carta.preco_atual !== undefined
              ? String(carta.preco_atual)
              : '',
          )
          setDataCompra(
            carta.data_da_compra
              ? carta.data_da_compra.toString().split('T')[0]
              : '',
          )
          setQuantidade(
            carta.quantidade !== null && carta.quantidade !== undefined
              ? String(carta.quantidade)
              : '',
          )
          setUrlImagem(carta.imagem || '')
          setDataVenda(
            carta.data_da_venda
              ? carta.data_da_venda.toString().split('T')[0]
              : '',
          )
          setPrecoVenda(
            carta.preco_da_venda !== null && carta.preco_da_venda !== undefined
              ? String(carta.preco_da_venda)
              : '',
          )

          if (carta.origem?.toUpperCase() === 'MYPCARDS') {
            setOrigem('myp')
          } else if (carta.origem?.toUpperCase() === 'LIGA YUGIOH') {
            setOrigem('liga')
          } else {
            setOrigem('')
          }

          setRaridade(carta.raridade ? String(carta.raridade) : '')
          setQualidade(carta.qualidade ? String(carta.qualidade) : '')
          setColecao(carta.colecao ? String(carta.colecao) : '')
        }
      } catch (error) {
        alert('Erro ao carregar dados da venda da carta.')
        void logError('Erro ao carregar dados da venda da carta: ' + error)
      }
    }

    async function carregarQualidades() {
      try {
        const dadosQualidade = (await listarRaridadeQualidade(
          'qualidade',
        )) as unknown as QualidadeDB[]

        setOpcoesQualidade(
          dadosQualidade.map((q) => ({
            value: String(q.id_qualidade),
            label: q.nome,
          })),
        )

        const dadosRaridade = (await listarRaridadeQualidade(
          'raridade',
        )) as unknown as RaridadeDB[]

        setOpcoesRaridade(
          dadosRaridade.map((r) => ({
            value: String(r.id_raridade),
            label: r.nome,
          })),
        )

        const dadosColecao = (await listarColecoes()) as unknown as {
          id_colecao: number
          nome: string
        }[]

        setOpcoesColecao(
          dadosColecao.map((c) => ({
            value: String(c.id_colecao),
            label: c.nome,
          })),
        )
      } catch (error) {
        void logError('Erro ao carregar opções da tela: ' + error)
      }
    }

    void carregarQualidades()
    void carregarDadosCarta()
  }, [idCarta])

  const opcoesOrigem = [
    { value: 'myp', label: 'MyPCards' },
    { value: 'liga', label: 'Liga Yugioh' },
  ]

  function validarFormulario(): boolean {
    if (
      !nome ||
      !codigo ||
      !precoPago ||
      !precoAtual ||
      !dataCompra ||
      !quantidade ||
      !origem ||
      !raridade ||
      !colecao ||
      !dataVenda ||
      !precoVenda
    ) {
      alert('Por favor, preencha todos os campos obrigatórios.')
      return false
    }

    return true
  }

  function handleFormKeyDown(e: React.KeyboardEvent<HTMLFormElement>) {
    if (e.key !== 'Enter') return

    const target = e.target as HTMLElement
    const tag = target.tagName.toLowerCase()

    if (tag !== 'textarea') {
      e.preventDefault()
    }
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()

    if (!validarFormulario()) return

    setModalAtualizarAberto(true)
  }

  async function confirmarAtualizacao(): Promise<void> {
    if (!idCarta || salvandoAtualizacao) return

    setSalvandoAtualizacao(true)

    try {
      const payload: InserirVendaCartaPayload = {
        id_carta: idCarta,
        preco_da_venda: precoVenda ? parseFloat(precoVenda) : null,
        data_da_venda: dataVenda || null,
        quantidade: quantidade ? parseInt(quantidade, 10) : null,
      }

      const ok = await atualizarVendaCarta(idCarta, payload)

      if (!ok) {
        alert(`Erro ao atualizar venda da carta "${nome}".`)
        return
      }

      setModalAtualizarAberto(false)
      alert(`Venda da carta "${nome}" atualizada com sucesso.`)
    } catch (error) {
      alert('Erro ao salvar venda da carta: ' + error)
      void logError('Erro ao salvar venda da carta: ' + error)
    } finally {
      setSalvandoAtualizacao(false)
    }
  }

  function cancelarAtualizacao(): void {
    if (salvandoAtualizacao) return
    setModalAtualizarAberto(false)
  }

  async function handleScraping() {
    if (!linkCarta.trim()) {
      alert('Informe o link da carta antes de buscar via scraping.')
      return
    }

    if (raridade === '') {
      alert('Por favor, selecione a raridade antes de buscar via scraping.')
      return
    }

    setBuscandoScraping(true)

    try {
      const raridadeNome = await buscarQualidadeRaridadeId(
        parseInt(raridade, 10),
        'raridade',
      )

      const cartas = await buscarCarta(linkCarta, raridadeNome || undefined)

      if (cartas.length > 0) {
        const carta = cartas[0]
        const colecaoEncontrada = await buscarColecao(carta.colecao)

        if (colecaoEncontrada) {
          setColecao(String(colecaoEncontrada.id_colecao))
        } else {
          const novoId = await inserirColecao(carta.colecao, '')

          const dadosColecao = (await listarColecoes()) as {
            id_colecao: number
            nome: string
          }[]

          const opcoesColecaoAtualizadas: OpcaoSelect[] = dadosColecao.map(
            (c) => ({
              value: String(c.id_colecao),
              label: c.nome,
            }),
          )

          setOpcoesColecao(opcoesColecaoAtualizadas)
          setColecao(String(novoId))
        }

        setNome(carta.nome || '')
        setCodigo(carta.codigo || '')
        setUrlImagem(carta.imagem || '')
        setPrecoAtual(
          carta.preco_atual !== null && carta.preco_atual !== undefined
            ? String(carta.preco_atual)
            : '',
        )

        if (carta.origem?.toUpperCase() === 'MYPCARDS') {
          setOrigem('myp')
        } else if (carta.origem?.toUpperCase() === 'LIGA YUGIOH') {
          setOrigem('liga')
        } else {
          setOrigem(carta.origem || '')
        }
      } else {
        alert('Nenhuma carta encontrada no link fornecido.')
      }
    } catch (error) {
      console.error('Erro ao buscar carta:', error)
      alert('Erro ao buscar carta. ' + String(error))
    } finally {
      setBuscandoScraping(false)
    }
  }

  function handleCancelar() {
    navigate(-1)
  }

  function handleExcluir(): void {
    setModalExcluirAberto(true)
  }

  async function confirmarExclusao(): Promise<void> {
    if (!idCarta || excluindoVenda) return

    setExcluindoVenda(true)

    try {
      await deletarVendaCarta(idCarta)
      setModalExcluirAberto(false)
      alert(`Venda da carta "${nome}" excluída com sucesso.`)
      navigate(-1)
    } catch (error) {
      alert('Erro ao excluir venda da carta: ' + error)
      void logError('Erro ao excluir venda da carta: ' + error)
    } finally {
      setExcluindoVenda(false)
    }
  }

  function cancelarExclusao(): void {
    if (excluindoVenda) return
    setModalExcluirAberto(false)
  }

  return (
    <div className="app-shell">
      <Topbar pageTitle="Editar carta" />

      <main className="form-page-content">
        <section className="form-page-left">
          <h2 className="section-title section-title-with-help">
            Editar {nome}
            <PageHelpButton
              configKey="cartas.vendas.editar"
              fallbackTitle="Como editar uma venda de carta"
            />
          </h2>
          <p className="section-subtitle">
            Preencha os dados básicos da carta antes de salvar.
          </p>

          <form onSubmit={handleSubmit} onKeyDown={handleFormKeyDown}>
            <div className="form-row-inline">
              <FormField
                label="Link da carta"
                name="linkCarta"
                kind="texto"
                value={linkCarta}
                onChange={setLinkCarta}
                placeholder="URL da página da carta"
                required
              />
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={handleScraping}
                disabled={buscandoScraping}
              >
                {buscandoScraping ? 'Buscando...' : 'Buscar via scraping'}
              </Button>
            </div>

            <FormField
              label="Nome"
              name="nome"
              kind="texto"
              value={nome}
              onChange={setNome}
              readOnly
            />

            <FormField
              label="Código"
              name="codigo"
              kind="texto"
              value={codigo}
              onChange={setCodigo}
              readOnly
            />

            <div className="form-row-inline">
              <FormField
                label="Preço pago"
                name="precoPago"
                kind="numero"
                value={precoPago}
                onChange={setPrecoPago}
                placeholder="Somente números"
                readOnly
              />
              <FormField
                label="Preço atual"
                name="precoAtual"
                kind="numero"
                value={precoAtual}
                onChange={setPrecoAtual}
                placeholder="Somente números"
              />
            </div>

            <div className="form-row-inline">
              <FormField
                label="Data da compra"
                name="dataCompra"
                kind="data"
                value={dataCompra}
                onChange={setDataCompra}
                readOnly
              />
              <FormField
                label="Quantidade vendida"
                name="quantidade"
                kind="numero"
                value={quantidade}
                onChange={setQuantidade}
                required
              />
            </div>

            <FormField
              label="URL da imagem"
              name="urlImagem"
              kind="texto"
              value={urlImagem}
              onChange={setUrlImagem}
              placeholder="Link direto para a imagem, se houver"
            />

            <div className="form-row-inline">
              <FormField
                label="Data da venda"
                name="dataVenda"
                kind="data"
                value={dataVenda}
                onChange={setDataVenda}
                required
              />
              <FormField
                label="Preço da venda"
                name="precoVenda"
                kind="numero"
                value={precoVenda}
                onChange={setPrecoVenda}
                required
              />
            </div>

            <div className="form-row-inline">
              <FormSelect
                label="Origem"
                name="origem"
                value={origem}
                onChange={setOrigem}
                options={opcoesOrigem}
                placeholder="Selecione a origem"
                readonly
              />
              <FormSelect
                label="Raridade"
                name="raridade"
                value={raridade}
                onChange={setRaridade}
                options={opcoesRaridade}
                placeholder="Selecione a raridade"
                readonly
              />
            </div>

            <div className="form-row-inline">
              <FormSelect
                label="Qualidade"
                name="qualidade"
                value={qualidade}
                onChange={setQualidade}
                options={opcoesQualidade}
                placeholder="Selecione a qualidade"
                readonly
              />
              <FormSelect
                label="Coleção"
                name="colecao"
                value={colecao}
                onChange={setColecao}
                options={opcoesColecao}
                placeholder="Selecione a coleção"
                readonly
              />
            </div>

            <div className="form-actions">
              <Button type="submit">Atualizar Venda</Button>
              <Button type="button" variant="outline" onClick={handleCancelar}>
                Cancelar
              </Button>
              <Button type="button" variant="danger" onClick={handleExcluir}>
                Excluir Venda
              </Button>
            </div>
          </form>
        </section>

        <aside className="form-page-right">
          <div className="form-image-label">Imagem da carta</div>

          <div className="form-image-placeholder">
            {urlImagem ? (
              <img
                src={urlImagem}
                alt={nome ? `Imagem da carta ${nome}` : 'Imagem da carta'}
                className="card-image-preview"
              />
            ) : (
              <>Pré-visualização da imagem da carta.</>
            )}
          </div>
        </aside>
      </main>

      {modalAtualizarAberto && (
        <div className="confirm-modal-backdrop">
          <div className="confirm-modal-card">
            <h3 className="confirm-modal-title">Confirmar atualização</h3>
            <p className="confirm-modal-text">
              Deseja realmente salvar as alterações da venda da carta "{nome}"?
            </p>
            <div className="confirm-modal-actions">
              <Button
                type="button"
                variant="outline"
                onClick={cancelarAtualizacao}
                disabled={salvandoAtualizacao}
              >
                Cancelar
              </Button>
              <Button
                type="button"
                onClick={confirmarAtualizacao}
                disabled={salvandoAtualizacao}
              >
                {salvandoAtualizacao ? 'Salvando...' : 'Confirmar'}
              </Button>
            </div>
          </div>
        </div>
      )}

      {modalExcluirAberto && (
        <div className="confirm-modal-backdrop">
          <div className="confirm-modal-card">
            <h3 className="confirm-modal-title">Confirmar exclusão</h3>
            <p className="confirm-modal-text">
              Confirma a exclusão da venda da carta "{nome}"? Esta ação não pode
              ser desfeita.
            </p>
            <div className="confirm-modal-actions">
              <Button
                type="button"
                variant="outline"
                onClick={cancelarExclusao}
                disabled={excluindoVenda}
              >
                Cancelar
              </Button>
              <Button
                type="button"
                variant="danger"
                onClick={confirmarExclusao}
                disabled={excluindoVenda}
              >
                {excluindoVenda ? 'Excluindo...' : 'Excluir'}
              </Button>
            </div>
          </div>
        </div>
      )}

      <Footer />
    </div>
  )
}
