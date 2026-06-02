import { useState } from 'react'
import { Topbar } from '../../components/topBar'
import { Footer } from '../../components/footer'
import { FormField } from '../../components/formField'
import { FormSelect } from '../../components/formSelect'
import { Button } from '../../components/botao'
import {
  type ProdutoLiga,
  buscarProdutoLiga,
} from '../../../scraping/webScraping'
import {
  inserirProduto,
  type InserirProdutoPayload,
} from '../../Database/db'
import { normalizePriceText, parsePriceNumber } from '../../utils/price'

export function CadastrarProduto() {
  const [link, setLink] = useState('')
  const [nome, setNome] = useState('')
  const [urlImagem, setUrlImagem] = useState('')
  const [precoCompra, setPrecoCompra] = useState('')
  const [precoAtual, setPrecoAtual] = useState('')
  const [dataCompra, setDataCompra] = useState('')
  const [quantidade, setQuantidade] = useState('')
  const [origem, setOrigem] = useState('')

  const [buscandoScraping, setBuscandoScraping] = useState(false)
  const [modalSalvarAberto, setModalSalvarAberto] = useState(false)
  const [salvando, setSalvando] = useState(false)

  const opcoesOrigem = [
    { value: 'myp', label: 'MyPCards' },
    { value: 'liga', label: 'Liga Yugioh' },
  ]

  function limparFormulario() {
    setLink('')
    setNome('')
    setUrlImagem('')
    setPrecoCompra('')
    setPrecoAtual('')
    setDataCompra('')
    setQuantidade('')
    setOrigem('')
  }

  function validarFormulario(): boolean {
    if (
      !nome ||
      !precoCompra ||
      !precoAtual ||
      !dataCompra ||
      !quantidade ||
      !origem
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

    setModalSalvarAberto(true)
  }

  async function confirmarSalvar() {
    if (salvando) return

    setSalvando(true)

    try {
      const origemMapeada =
        origem === 'liga'
          ? 'Liga Yugioh'
          : origem === 'myp'
          ? 'MyPCards'
          : origem

      const novoProduto: InserirProdutoPayload = {
        link,
        nome_produto: nome,
        imagem: urlImagem,
        preco_compra: parsePriceNumber(precoCompra),
        preco_atual: parsePriceNumber(precoAtual),
        data_compra: dataCompra,
        quantidade: parseInt(quantidade, 10),
        origem: origemMapeada,
      }

      const ok = await inserirProduto(novoProduto)

      if (!ok) {
        alert('Erro ao cadastrar produto.')
        return
      }

      setModalSalvarAberto(false)
      alert('Produto cadastrado com sucesso!')
      limparFormulario()
    } catch (error) {
      alert('Erro ao cadastrar produto: ' + error)
    } finally {
      setSalvando(false)
    }
  }

  function cancelarSalvar() {
    if (salvando) return
    setModalSalvarAberto(false)
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
    if (salvando || buscandoScraping) return
    limparFormulario()
  }

  return (
    <div className="app-shell">
      <Topbar pageTitle="Cadastrar produto" />

      <main className="form-page-content">
        <section className="form-page-left">
          <h2 className="section-title">Cadastrar novo produto</h2>
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
                disabled={buscandoScraping || salvando}
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
                label="Quantidade"
                name="quantidade"
                kind="numero"
                value={quantidade}
                onChange={setQuantidade}
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
              required
            />

            <div className="form-actions">
              <Button type="submit" disabled={salvando || buscandoScraping}>
                {salvando ? 'Salvando...' : 'Salvar produto'}
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={handleCancelar}
                disabled={salvando || buscandoScraping}
              >
                Cancelar
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

      {modalSalvarAberto && (
        <div className="confirm-modal-backdrop">
          <div className="confirm-modal-card">
            <h3 className="confirm-modal-title">Confirmar cadastro</h3>
            <p className="confirm-modal-text">
              Deseja realmente cadastrar este produto?
            </p>

            <div className="confirm-modal-actions">
              <Button
                type="button"
                variant="outline"
                onClick={cancelarSalvar}
                disabled={salvando}
              >
                Cancelar
              </Button>

              <Button
                type="button"
                onClick={confirmarSalvar}
                disabled={salvando}
              >
                {salvando ? 'Salvando...' : 'Confirmar'}
              </Button>
            </div>
          </div>
        </div>
      )}

      <Footer appName="YU-GI-OH! Manager" />
    </div>
  )
}
