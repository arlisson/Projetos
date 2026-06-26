import { useEffect, useMemo, useState } from 'react'
import { Topbar } from '../../components/topBar'
import { Footer } from '../../components/footer'
import { FormField } from '../../components/formField'
import { FormSelect } from '../../components/formSelect'
import { Button } from '../../components/botao'
import { Grafico } from '../../components/grafico'
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
  buscarCartaId,
  deletar,
  atualizarCarta,
  type InserirCartaPayload,
  type InserirVendaCartaPayload,
  venderCarta,
  todayStr,
  buscarHistoricoPrecos,
  type HistoricoPrecos,
} from '../../Database/db'
import { buscarCartaMyp, type CartaMyP } from '../../../scraping/webScraping'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { logError } from '../../services/logger'

async function buscarCarta(url: string, chave?: string): Promise<CartaMyP[]> {
  const carta = await buscarCartaMyp(url, chave)
  return carta
}

export function EditarCarta() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const idParam = searchParams.get('id')
  const idCarta = idParam ? Number(idParam) : null

  const [quantidadeVenda, setQuantidadeVenda] = useState('')
  const [valorVenda, setValorVenda] = useState('')
  const [modalVenderAberto, setModalVenderAberto] = useState(false)

  const [modalAtualizarAberto, setModalAtualizarAberto] = useState(false)
  const [modalExcluirAberto, setModalExcluirAberto] = useState(false)
  const [salvandoAtualizacao, setSalvandoAtualizacao] = useState(false)
  const [excluindoCarta, setExcluindoCarta] = useState(false)
  const [buscandoScraping, setBuscandoScraping] = useState(false)

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

  const [historicoPrecos, setHistoricoPrecos] = useState<HistoricoPrecos[]>([])
  const [carregandoHistorico, setCarregandoHistorico] = useState(false)

  useEffect(() => {
    if (!idCarta) return

    async function carregarDadosCarta() {
      try {
        const carta = await buscarCartaId(idCarta!)
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
        await logError('Erro ao carregar dados da carta: ' + String(error))
        alert('Erro ao carregar dados da carta.')
      }
    }

    async function carregarHistoricoCarta() {
      try {
        setCarregandoHistorico(true)
        const historico = await buscarHistoricoPrecos('carta', idCarta!)
        setHistoricoPrecos(
          Array.isArray(historico) ? (historico as HistoricoPrecos[]) : [],
        )
      } catch (error) {
        setHistoricoPrecos([])
        await logError('Erro ao carregar histórico da carta: ' + String(error))
      } finally {
        setCarregandoHistorico(false)
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
        await logError('Erro ao carregar opções da tela: ' + String(error))
      }
    }

    void carregarQualidades()
    void carregarDadosCarta()
    void carregarHistoricoCarta()
  }, [idCarta])

  const dadosGraficoHistorico = useMemo(() => {
    return historicoPrecos
      .filter(
        (item) => item.preco !== null && item.preco !== undefined && item.data,
      )
      .map((item) => ({
        data: item.data,
        preco: Number(item.preco),
        origem: item.origem ?? '',
      }))
      .sort((a, b) => new Date(a.data).getTime() - new Date(b.data).getTime())
  }, [historicoPrecos])

  const opcoesOrigem = [
    { value: 'myp', label: 'MyPCards' },
    { value: 'liga', label: 'Liga Yugioh' },
  ]

  async function recarregarHistorico(): Promise<void> {
    if (!idCarta) return

    try {
      setCarregandoHistorico(true)
      const historicoAtualizado = await buscarHistoricoPrecos('carta', idCarta)
      setHistoricoPrecos(
        Array.isArray(historicoAtualizado)
          ? (historicoAtualizado as HistoricoPrecos[])
          : [],
      )
    } catch (error) {
      await logError('Erro ao recarregar histórico da carta: ' + String(error))
    } finally {
      setCarregandoHistorico(false)
    }
  }

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
      !colecao
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
      const origemFormatada =
        origem === 'myp' ? 'MyPCards' : origem === 'liga' ? 'Liga Yugioh' : ''

      const payload: InserirCartaPayload = {
        link_site: linkCarta,
        imagem: urlImagem,
        nome,
        codigo,
        preco_da_compra: precoPago ? parseFloat(precoPago) : null,
        preco_atual: precoAtual ? parseFloat(precoAtual) : null,
        data_da_compra: dataCompra,
        quantidade: quantidade ? parseInt(quantidade, 10) : null,
        origem: origemFormatada,
        raridade: raridade ? parseInt(raridade, 10) : null,
        qualidade: qualidade ? parseInt(qualidade, 10) : null,
        colecao: colecao || null,
      }

      const ok = await atualizarCarta(idCarta, payload)

      if (!ok) {
        alert(`Erro ao atualizar carta "${nome}".`)
        return
      }

      setModalAtualizarAberto(false)
      alert(`Carta "${nome}" atualizada com sucesso.`)
      await recarregarHistorico()
    } catch (error) {
      alert('Erro ao salvar carta: ' + error)
      void logError('Erro ao salvar carta: ' + error)
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

          setOpcoesColecao(
            dadosColecao.map((c) => ({
              value: String(c.id_colecao),
              label: c.nome,
            })),
          )

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

        if (carta.origem.toUpperCase() === 'MYPCARDS') {
          setOrigem('myp')
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
    if (!idCarta || excluindoCarta) return

    setExcluindoCarta(true)

    try {
      await deletar('carta', idCarta)
      setModalExcluirAberto(false)
      alert(`Carta "${nome}" excluída com sucesso.`)
      navigate(-1)
    } catch (error) {
      alert('Erro ao excluir carta: ' + error)
      await logError('Erro ao excluir carta: ' + error)
    } finally {
      setExcluindoCarta(false)
    }
  }

  function cancelarExclusao(): void {
    if (excluindoCarta) return
    setModalExcluirAberto(false)
  }

  function handleVender(): void {
    setQuantidadeVenda('')
    setValorVenda('')
    setModalVenderAberto(true)
  }

  async function confirmarVenda(): Promise<void> {
    const qtd = Number(quantidadeVenda)

    if (!Number.isFinite(qtd) || qtd <= 0) {
      alert('Informe uma quantidade válida.')
      return
    } else if (qtd > Number(quantidade)) {
      alert('Quantidade a vender não pode ser maior que a quantidade em estoque.')
      return
    }

    if (valorVenda) {
      const valor = Number(valorVenda)
      if (!Number.isFinite(valor) || valor <= 0) {
        alert('Informe um valor de venda válido.')
        return
      }
    }

    try {
      const payload: InserirVendaCartaPayload = {
        id_carta: idCarta!,
        preco_da_venda: valorVenda ? parseFloat(valorVenda) : null,
        data_da_venda: todayStr(),
        quantidade: qtd,
      }

      const origemFormatada =
        origem === 'myp' ? 'MyPCards' : origem === 'liga' ? 'Liga Yugioh' : ''

      const payloadCarta: InserirCartaPayload = {
        link_site: linkCarta,
        imagem: urlImagem,
        nome,
        codigo,
        preco_da_compra: precoPago ? parseFloat(precoPago) : null,
        preco_atual: precoAtual ? parseFloat(precoAtual) : null,
        data_da_compra: dataCompra,
        quantidade: quantidade ? parseInt(quantidade, 10) : null,
        origem: origemFormatada,
        raridade: raridade ? parseInt(raridade, 10) : null,
        qualidade: qualidade ? parseInt(qualidade, 10) : null,
        colecao: colecao || null,
      }

      const ok = await venderCarta(payloadCarta, payload, qtd)

      if (!ok) {
        alert(`Erro ao registrar venda da carta: ${nome}`)
        return
      }

      alert(`${qtd} unidade(s) de ${nome} vendida(s).`)
      setModalVenderAberto(false)
      setQuantidade(String(Number(quantidade) - qtd))
    } catch (err) {
      alert(`Erro ao registrar venda da carta: ${nome}\n${err}`)
    }
  }

  function cancelarVenda(): void {
    setModalVenderAberto(false)
  }

  return (
    <div className="app-shell">
      <Topbar pageTitle="Editar carta" />

      <main className="form-page-content">
        <section className="form-page-left">
          <h2 className="section-title section-title-with-help">
            Editar {nome}
            <PageHelpButton
              configKey="cartas.editar"
              fallbackTitle="Como editar uma carta"
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
              required
            />

            <FormField
              label="Código"
              name="codigo"
              kind="texto"
              value={codigo}
              onChange={setCodigo}
              required
            />

            <div className="form-row-inline">
              <FormField
                label="Preço pago"
                name="precoPago"
                kind="numero"
                value={precoPago}
                onChange={setPrecoPago}
                placeholder="Somente números"
                required
              />
              <FormField
                label="Preço atual"
                name="precoAtual"
                kind="numero"
                value={precoAtual}
                onChange={setPrecoAtual}
                placeholder="Somente números"
                required
              />
            </div>

            <div className="form-row-inline">
              <FormField
                label="Data da compra"
                name="dataCompra"
                kind="data"
                value={dataCompra}
                onChange={setDataCompra}
                required
              />
              <FormField
                label="Quantidade comprada"
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
              <FormSelect
                label="Origem"
                name="origem"
                value={origem}
                onChange={setOrigem}
                options={opcoesOrigem}
                placeholder="Selecione a origem"
                required
              />
              <FormSelect
                label="Raridade"
                name="raridade"
                value={raridade}
                onChange={setRaridade}
                options={opcoesRaridade}
                placeholder="Selecione a raridade"
                required
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
              />
              <FormSelect
                label="Coleção"
                name="colecao"
                value={colecao}
                onChange={setColecao}
                options={opcoesColecao}
                placeholder="Selecione a coleção"
                required
              />
            </div>

            <div className="form-actions">
              <Button type="submit">Salvar carta</Button>
              <Button type="button" variant="outline" onClick={handleCancelar}>
                Cancelar
              </Button>
              <Button type="button" variant="outline" onClick={handleVender}>
                Vender Carta
              </Button>
              <Button type="button" variant="danger" onClick={handleExcluir}>
                Excluir carta
              </Button>
            </div>
          </form>
        </section>

        {modalVenderAberto && (
          <div className="modal-backdrop">
            <div className="modal-card">
              <div className="modal-title">Vender carta</div>
              <div className="modal-body">
                <label className="modal-label">
                  Quantidade a vender:
                  <input
                    type="number"
                    min={1}
                    className="modal-input"
                    value={quantidadeVenda}
                    onChange={(e) => setQuantidadeVenda(e.target.value)}
                    autoFocus
                  />
                </label>
                <label className="modal-label">
                  Valor da venda:
                  <input
                    type="number"
                    min={1}
                    className="modal-input"
                    value={valorVenda}
                    onChange={(e) => setValorVenda(e.target.value)}
                  />
                </label>
              </div>
              <div className="modal-actions">
                <button type="button" onClick={confirmarVenda}>
                  Confirmar
                </button>
                <button type="button" onClick={cancelarVenda}>
                  Cancelar
                </button>
              </div>
            </div>
          </div>
        )}

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

      {idCarta && (
        <section className="form-history-section">
          <Grafico
            title={`Histórico de preços${nome ? ` - ${nome}` : ''}`}
            data={dadosGraficoHistorico}
            series={[{ key: 'preco', label: 'Preço' }]}
            dateKey="data"
            height={220}
            emptyMessage={
              carregandoHistorico
                ? 'Carregando histórico de preços...'
                : 'Nenhum histórico de preços encontrado para esta carta.'
            }
          />
        </section>
      )}

      {modalAtualizarAberto && (
        <div className="confirm-modal-backdrop">
          <div className="confirm-modal-card">
            <h3 className="confirm-modal-title">Confirmar atualização</h3>
            <p className="confirm-modal-text">
              Deseja realmente salvar as alterações da carta "{nome}"?
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
              Confirma a exclusão de "{nome}"? Esta ação não pode ser desfeita.
            </p>
            <div className="confirm-modal-actions">
              <Button
                type="button"
                variant="outline"
                onClick={cancelarExclusao}
                disabled={excluindoCarta}
              >
                Cancelar
              </Button>
              <Button
                type="button"
                variant="danger"
                onClick={confirmarExclusao}
                disabled={excluindoCarta}
              >
                {excluindoCarta ? 'Excluindo...' : 'Excluir'}
              </Button>
            </div>
          </div>
        </div>
      )}

      <Footer />
    </div>
  )
}
