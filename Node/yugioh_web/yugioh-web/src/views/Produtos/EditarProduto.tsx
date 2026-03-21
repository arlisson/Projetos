import { useEffect, useMemo, useState } from 'react'
import { Topbar } from '../../components/topBar'
import { Footer } from '../../components/footer'
import { FormField } from '../../components/formField'
import { FormSelect } from '../../components/formSelect'
import { Button } from '../../components/botao'
import { Grafico } from '../../components/grafico'
import { useNavigate, useSearchParams } from 'react-router-dom'
import {
  buscarProdutoId,
  deletar,
  type InserirProdutoPayload,
  atualizarProduto,
  todayStr,
  type InserirVendaProdutoPayload,
  venderProduto,
  buscarHistoricoPrecos,
  type HistoricoPrecos,
} from '../../Database/db'
import { type ProdutoLiga, buscarProdutoLiga } from '../../../scraping/webScraping'
import { logError } from '../../services/logger'

export function EditarProduto() {
  const navigate = useNavigate()

  const [link, setLink] = useState('')
  const [nome, setNome] = useState('')
  const [urlImagem, setUrlImagem] = useState('')
  const [precoCompra, setPrecoCompra] = useState('')
  const [precoAtual, setPrecoAtual] = useState('')
  const [dataCompra, setDataCompra] = useState('')
  const [quantidade, setQuantidade] = useState('')
  const [origem, setOrigem] = useState('')

  const [modalVenderAberto, setModalVenderAberto] = useState(false)
  const [quantidadeVenda, setQuantidadeVenda] = useState('')
  const [valorVenda, setValorVenda] = useState('')

  const [historicoPrecos, setHistoricoPrecos] = useState<HistoricoPrecos[]>([])
  const [carregandoHistorico, setCarregandoHistorico] = useState(false)

  const opcoesOrigem = [
    { value: 'myp', label: 'MyPCards' },
    { value: 'liga', label: 'Liga Yugioh' },
  ]

  const [searchParams] = useSearchParams()
  const idParam = searchParams.get('id')
  const idProduto = idParam ? Number(idParam) : null

  useEffect(() => {
    if (!idProduto) return

    const produtoId = idProduto

    async function carregarProduto() {
      try {
        const produtoDetalhado = await buscarProdutoId(produtoId)
        if (produtoDetalhado) {
          setLink(produtoDetalhado.link || '')
          setNome(produtoDetalhado.nome_produto || '')
          setUrlImagem(produtoDetalhado.imagem || '')
          setPrecoCompra(
            produtoDetalhado.preco_compra !== null &&
              produtoDetalhado.preco_compra !== undefined
              ? produtoDetalhado.preco_compra.toString()
              : '',
          )
          setPrecoAtual(
            produtoDetalhado.preco_atual !== null &&
              produtoDetalhado.preco_atual !== undefined
              ? produtoDetalhado.preco_atual.toString()
              : '',
          )
          setDataCompra(produtoDetalhado.data_compra || '')
          setQuantidade(
            produtoDetalhado.quantidade !== null &&
              produtoDetalhado.quantidade !== undefined
              ? produtoDetalhado.quantidade.toString()
              : '',
          )

          if (produtoDetalhado.origem?.toUpperCase() === 'MYPCARDS') {
            setOrigem('myp')
          } else if (produtoDetalhado.origem?.toUpperCase() === 'LIGA YUGIOH') {
            setOrigem('liga')
          } else {
            setOrigem('')
          }
        }
      } catch (err) {
        await logError('Erro ao carregar produto: ' + String(err))
        alert('Erro ao carregar produto.')
      }
    }

    async function carregarHistoricoProduto() {
      try {
        setCarregandoHistorico(true)
        const historico = await buscarHistoricoPrecos('produto', produtoId)
        setHistoricoPrecos(
          Array.isArray(historico) ? (historico as HistoricoPrecos[]) : [],
        )
      } catch (err) {
        setHistoricoPrecos([])
        await logError('Erro ao carregar histórico do produto: ' + String(err))
      } finally {
        setCarregandoHistorico(false)
      }
    }

    void carregarProduto()
    void carregarHistoricoProduto()
  }, [idProduto])

  const dadosGraficoHistorico = useMemo(() => {
    return historicoPrecos
      .filter((item) => item.preco !== null && item.preco !== undefined && item.data)
      .map((item) => ({
        data: item.data,
        preco: Number(item.preco),
        origem: item.origem ?? '',
      }))
      .sort(
        (a, b) =>
          new Date(a.data).getTime() - new Date(b.data).getTime(),
      )
  }, [historicoPrecos])

  async function recarregarHistorico(): Promise<void> {
    if (!idProduto) return

    try {
      setCarregandoHistorico(true)
      const historicoAtualizado = await buscarHistoricoPrecos('produto', idProduto)
      setHistoricoPrecos(
        Array.isArray(historicoAtualizado)
          ? (historicoAtualizado as HistoricoPrecos[])
          : [],
      )
    } catch (error) {
      await logError('Erro ao recarregar histórico do produto: ' + String(error))
    } finally {
      setCarregandoHistorico(false)
    }
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()

    if (!nome || !precoCompra || !precoAtual || !dataCompra || !quantidade) {
      alert('Por favor, preencha todos os campos obrigatórios.')
      return
    }

    try {
      const origemFormatada =
        origem === 'myp' ? 'MyPCards' : origem === 'liga' ? 'Liga Yugioh' : ''

      const payload: InserirProdutoPayload = {
        link,
        nome_produto: nome,
        imagem: urlImagem,
        preco_compra: parseFloat(precoCompra),
        preco_atual: parseFloat(precoAtual),
        data_compra: dataCompra,
        quantidade: parseInt(quantidade, 10),
        origem: origemFormatada,
      }

      confirm(`Salvar alterações do produto "${nome}"?`) &&
        atualizarProduto(idProduto!, payload).then(async (ok) => {
          if (!ok) {
            alert(`Erro ao atualizar produto "${nome}".`)
            return
          }

          alert(`Produto "${nome}" atualizado com sucesso.`)
          await recarregarHistorico()
        })
    } catch (error) {
      alert('Erro ao salvar produto: ' + error)
      void logError('Erro ao salvar produto: ' + error)
    }
  }

  function handleScraping() {
    if (!link) {
      alert('Por favor, insira uma URL para buscar o produto.')
      return
    }

    try {
      buscarProdutoLiga(link).then((produto: ProdutoLiga | null) => {
        if (produto) {
          setNome(produto.nome)
          setUrlImagem(produto.imagem)
          setPrecoAtual(
            produto.preco_atual
              .replace('R$ ', '')
              .replace('.', '')
              .replace(',', '.'),
          )
          setOrigem('liga')
        } else {
          alert('Produto não encontrado ou erro ao buscar.')
        }
      })
    } catch (error) {
      alert('Erro ao buscar o produto: ' + error)
    }
  }

  function handleCancelar() {
    navigate(-1)
  }

  async function handleExcluir(): Promise<void> {
    try {
      if (confirm(`Confirma a exclusão de "${nome}"? Esta ação não pode ser desfeita.`)) {
        await deletar('produto', idProduto!)
        alert(`Produto "${nome}" excluído com sucesso.`)
        navigate(-1)
      }
    } catch (error) {
      alert('Erro ao excluir produto: ' + error)
      await logError('Erro ao excluir produto: ' + error)
    }
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
      const payloadVenda: InserirVendaProdutoPayload = {
        id_produto: idProduto!,
        preco_venda: valorVenda ? parseFloat(valorVenda) : null,
        data_venda: todayStr(),
        quantidade: qtd,
      }

      const origemFormatada =
        origem === 'myp' ? 'MyPCards' : origem === 'liga' ? 'Liga Yugioh' : ''

      const payloadProduto: InserirProdutoPayload = {
        link,
        nome_produto: nome,
        imagem: urlImagem,
        preco_compra: parseFloat(precoCompra),
        preco_atual: parseFloat(precoAtual),
        data_compra: dataCompra,
        quantidade: parseInt(quantidade, 10) - qtd,
        origem: origemFormatada,
      }

      const ok = await venderProduto(payloadProduto, payloadVenda, qtd)

      if (!ok) {
        alert(`Erro ao registrar venda do produto: ${nome}`)
        return
      }

      alert(`${qtd} unidade(s) de ${nome} vendida(s).`)
      setModalVenderAberto(false)
      setQuantidade(String(Number(quantidade) - qtd))
    } catch (err) {
      alert(`Erro ao registrar venda do produto: ${nome}\n${err}`)
    }
  }

  function cancelarVenda(): void {
    setModalVenderAberto(false)
  }

  return (
    <div className="app-shell">
      <Topbar pageTitle="Editar produto" />

      <main className="form-page-content">
        <section className="form-page-left">
          <h2 className="section-title">Editar {nome}</h2>
          <p className="section-subtitle">
            Preencha os dados básicos do produto antes de salvar.
          </p>

          <form onSubmit={handleSubmit}>
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
              >
                Buscar via scraping
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
            />

            <div className="form-actions">
              <Button type="submit">Salvar produto</Button>
              <Button type="button" variant="outline" onClick={handleCancelar}>
                Cancelar
              </Button>
              <Button type="button" variant="outline" onClick={handleVender}>
                Vender Produto
              </Button>
              <Button type="button" variant="danger" onClick={handleExcluir}>
                Excluir Produto
              </Button>
            </div>
          </form>
        </section>

        {modalVenderAberto && (
          <div className="modal-backdrop">
            <div className="modal-card">
              <div className="modal-title">Vender Produto</div>
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

      {idProduto && (
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
                : 'Nenhum histórico de preços encontrado para este produto.'
            }
          />
        </section>
      )}

      <Footer appName="YU-GI-OH! Manager" />
    </div>
  )
}