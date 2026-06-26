import { useEffect, useState } from 'react'
import { Topbar } from '../../components/topBar'
import { Footer } from '../../components/footer'
import { FormField } from '../../components/formField'
import { FormSelect } from '../../components/formSelect'
import { Button } from '../../components/botao'
import { PageHelpButton } from '../../components/PageHelpButton'
import { useNavigate, useSearchParams } from 'react-router-dom'
import {
  deletarVendaProduto,
  buscarVendaProdutoId,
  atualizarVendaProduto,
  type AtualizarVendaProdutoPayload,
} from '../../Database/db'
import { type ProdutoLiga, buscarProdutoLiga } from '../../../scraping/webScraping'
import { logError } from '../../services/logger'
import { normalizePriceText, parsePriceNumber } from '../../utils/price'

export function EditarVendasProdutos() {
  const navigate = useNavigate()

  const [link, setLink] = useState('')
  const [nome, setNome] = useState('')
  const [urlImagem, setUrlImagem] = useState('')
  const [precoCompra, setPrecoCompra] = useState('')
  const [precoAtual, setPrecoAtual] = useState('')
  const [dataCompra, setDataCompra] = useState('')
  const [quantidade, setQuantidade] = useState('')
  const [origem, setOrigem] = useState('')
  const [dataVenda, setDataVenda] = useState('')
  const [precoVenda, setPrecoVenda] = useState('')

  const [buscandoScraping, setBuscandoScraping] = useState(false)
  const [modalAtualizarAberto, setModalAtualizarAberto] = useState(false)
  const [modalExcluirAberto, setModalExcluirAberto] = useState(false)
  const [salvandoAtualizacao, setSalvandoAtualizacao] = useState(false)
  const [excluindoVenda, setExcluindoVenda] = useState(false)

  const opcoesOrigem = [
    { value: 'myp', label: 'MyPCards' },
    { value: 'liga', label: 'Liga Yugioh' },
  ]

  const [searchParams] = useSearchParams()
  const idParam = searchParams.get('id')
  const idProduto = idParam ? Number(idParam) : null

  useEffect(() => {
    if (!idProduto) return

    async function carregarProduto() {
      try {
        const produtoDetalhado = await buscarVendaProdutoId(idProduto!)

        if (produtoDetalhado) {
          setLink(produtoDetalhado.link || '')
          setNome(produtoDetalhado.nome_produto || '')
          setUrlImagem(produtoDetalhado.imagem || '')
          setPrecoCompra(produtoDetalhado.preco_compra?.toString() || '')
          setPrecoAtual(produtoDetalhado.preco_atual?.toString() || '')
          setDataCompra(produtoDetalhado.data_compra || '')
          setQuantidade(produtoDetalhado.quantidade?.toString() || '')
          setDataVenda(produtoDetalhado.data_venda || '')
          setPrecoVenda(produtoDetalhado.preco_venda?.toString() || '')

          if (produtoDetalhado.origem?.toUpperCase() === 'MYPCARDS') {
            setOrigem('myp')
          } else if (produtoDetalhado.origem?.toUpperCase() === 'LIGA YUGIOH') {
            setOrigem('liga')
          } else {
            setOrigem('')
          }
        }
      } catch (err) {
        await logError('Erro ao carregar venda do produto: ' + String(err))
        alert('Erro ao carregar venda do produto.')
      }
    }

    void carregarProduto()
  }, [idProduto])

  function validarFormulario(): boolean {
    if (
      !nome ||
      !precoCompra ||
      !precoAtual ||
      !dataCompra ||
      !quantidade ||
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
    if (!idProduto || salvandoAtualizacao) return

    setSalvandoAtualizacao(true)

    try {
      const payload: AtualizarVendaProdutoPayload = {
        id_produto: idProduto,
        preco_venda: precoVenda ? parsePriceNumber(precoVenda) : null,
        data_venda: dataVenda || null,
        quantidade: quantidade ? parseInt(quantidade, 10) : null,
      }

      const ok = await atualizarVendaProduto(idProduto, payload)

      if (!ok) {
        alert(`Erro ao atualizar venda do produto "${nome}".`)
        return
      }

      setModalAtualizarAberto(false)
      alert(`Venda do produto "${nome}" atualizada com sucesso.`)
    } catch (error) {
      alert('Erro ao salvar produto: ' + error)
      void logError('Erro ao salvar produto: ' + error)
    } finally {
      setSalvandoAtualizacao(false)
    }
  }

  function cancelarAtualizacao(): void {
    if (salvandoAtualizacao) return
    setModalAtualizarAberto(false)
  }

  async function handleScraping() {
    if (!link.trim()) {
      alert('Por favor, insira uma URL para buscar o produto.')
      return
    }

    setBuscandoScraping(true)

    try {
      const produto: ProdutoLiga | null = await buscarProdutoLiga(link)

      if (produto) {
        setNome(produto.nome || '')
        setUrlImagem(produto.imagem || '')
        setPrecoAtual(normalizePriceText(produto.preco_atual))
        setOrigem('liga')
      } else {
        alert('Produto não encontrado ou erro ao buscar.')
      }
    } catch (error) {
      alert('Erro ao buscar o produto: ' + error)
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
    if (!idProduto || excluindoVenda) return

    setExcluindoVenda(true)

    try {
      await deletarVendaProduto(idProduto)
      setModalExcluirAberto(false)
      alert(`Venda "${nome}" excluída com sucesso.`)
      navigate(-1)
    } catch (error) {
      alert('Erro ao excluir venda: ' + error)
      await logError('Erro ao excluir venda: ' + error)
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
      <Topbar pageTitle="Editar produto" />

      <main className="form-page-content">
        <section className="form-page-left">
          <h2 className="section-title section-title-with-help">
            Editar {nome}
            <PageHelpButton
              configKey="produtos.vendas.editar"
              fallbackTitle="Como editar uma venda de produto"
            />
          </h2>
          <p className="section-subtitle">
            Preencha os dados básicos do produto antes de salvar.
          </p>

          <form onSubmit={handleSubmit} onKeyDown={handleFormKeyDown}>
            <div className="form-row-inline">
              <FormField
                label="Link"
                name="linkProduto"
                kind="texto"
                value={link}
                onChange={setLink}
                placeholder="URL da página do produto"
                required
              />
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={handleScraping}
                disabled={buscandoScraping || salvandoAtualizacao || excluindoVenda}
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
              label="URL da imagem"
              name="urlImagem"
              kind="texto"
              value={urlImagem}
              onChange={setUrlImagem}
              placeholder="Link direto para a imagem, se houver"
            />

            <div className="form-row-inline">
              <FormField
                label="Preço de compra"
                name="precoCompra"
                kind="numero"
                value={precoCompra}
                onChange={setPrecoCompra}
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
                readOnly
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
                label="Quantidade"
                name="quantidade"
                kind="numero"
                value={quantidade}
                onChange={setQuantidade}
                required
              />
            </div>

            <div className="form-row-inline">
              <FormField
                label="Data da Venda"
                name="dataVenda"
                kind="data"
                value={dataVenda}
                onChange={setDataVenda}
                required
              />
              <FormField
                label="Preço da Venda"
                name="precoVenda"
                kind="numero"
                value={precoVenda}
                onChange={setPrecoVenda}
                required
              />
            </div>

            <FormSelect
              label="Origem"
              name="origem"
              value={origem}
              onChange={setOrigem}
              options={opcoesOrigem}
              placeholder="Selecione a origem"
              readonly
            />

            <div className="form-actions">
              <Button type="submit" disabled={salvandoAtualizacao || excluindoVenda}>
                {salvandoAtualizacao ? 'Salvando...' : 'Salvar produto'}
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={handleCancelar}
                disabled={salvandoAtualizacao || excluindoVenda}
              >
                Cancelar
              </Button>
              <Button
                type="button"
                variant="danger"
                onClick={handleExcluir}
                disabled={salvandoAtualizacao || excluindoVenda}
              >
                {excluindoVenda ? 'Excluindo...' : 'Excluir Venda'}
              </Button>
            </div>
          </form>
        </section>

        <aside className="form-page-right">
          <div className="form-image-label">Imagem do produto</div>
          <div className="form-image-placeholder">
            {urlImagem ? (
              <img
                src={urlImagem}
                alt={nome ? `Imagem do Produto ${nome}` : 'Imagem do Produto'}
                className="card-image-preview"
              />
            ) : (
              <>Pré-visualização da imagem do produto.</>
            )}
          </div>
        </aside>
      </main>

      {modalAtualizarAberto && (
        <div className="confirm-modal-backdrop">
          <div className="confirm-modal-card">
            <h3 className="confirm-modal-title">Confirmar atualização</h3>
            <p className="confirm-modal-text">
              Deseja realmente salvar as alterações da venda do produto "{nome}"?
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
              Confirma a exclusão da venda "{nome}"? Esta ação não pode ser
              desfeita.
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

      <Footer appName="YU-GI-OH! Manager" />
    </div>
  )
}
