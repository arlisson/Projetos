import { useEffect, useState } from 'react'
import { Topbar } from '../../components/topBar'
import { Footer } from '../../components/footer'
import { FormField } from '../../components/formField'
import { FormSelect } from '../../components/formSelect'
import { Button } from '../../components/botao'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { buscarProdutoId,
  deletar,
  type InserirProdutoPayload,
  atualizarProduto
 } from '../../Database/db'
import { type ProdutoLiga, buscarProdutoLiga } from '../../../scraping/webScraping'
import { logError } from '../../services/logger'

export function EditarProduto() {
  const navigate = useNavigate()

  const [link, setLink] = useState('')
  const [nome, setNome] = useState('')
  const [urlImagem, setUrlImagem] = useState('')
  // const [caminhoImagemLocal, setCaminhoImagemLocal] = useState('')
  const [precoCompra, setPrecoCompra] = useState('')
  const [precoAtual, setPrecoAtual] = useState('')
  const [dataCompra, setDataCompra] = useState('')
  const [quantidade, setQuantidade] = useState('')
  const [origem, setOrigem] = useState('')

  // Futuramente estes valores virão do banco
  const opcoesOrigem = [
    { value: 'myp', label: 'MyPCards' },
    { value: 'liga', label: 'Liga Yugioh' },
    
  ]

  const [searchParams] = useSearchParams()
    const idParam = searchParams.get('id')
    const idProduto = idParam ? Number(idParam) : null

  useEffect(() => {
    // Carregar dados do produto pelo idProduto
    if (!idProduto) return
    async function carregarProduto() {
      try {
        const produtoDetalhado = await buscarProdutoId(idProduto!)
        if (produtoDetalhado) {
          setLink(produtoDetalhado.link || '')
          setNome(produtoDetalhado.nome_produto || '')
          setUrlImagem(produtoDetalhado.imagem || '')
          // setCaminhoImagemLocal(produtoDetalhado.imagem_salva || '')
          setPrecoCompra(produtoDetalhado.preco_compra?.toString() || '')
          setPrecoAtual(produtoDetalhado.preco_atual?.toString() || '')
          setDataCompra(produtoDetalhado.data_compra || '')
          setQuantidade(produtoDetalhado.quantidade?.toString() || '')
          if(produtoDetalhado.origem?.toUpperCase() === 'MYPCARDS') {
              setOrigem('myp')
          }else if(produtoDetalhado.origem?.toUpperCase() === 'LIGA YUGIOH') {
              setOrigem('liga')
          }else{
              setOrigem('')
          }

        }
      } catch (err) {
        //console.error('Erro ao carregar produto:', err)
      }
    }

    carregarProduto()
  }, [idProduto])



  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if(!nome || !precoCompra || !precoAtual || !dataCompra || !quantidade){
      alert('Por favor, preencha todos os campos obrigatórios.')
      return
    }
    try {
      const origemFormatada = origem === 'myp' ? 'MyPCards' : origem === 'liga' ? 'Liga Yugioh' : ''
      const payload: InserirProdutoPayload = {
        link,
        nome_produto: nome,
        imagem: urlImagem,
        preco_compra: parseFloat(precoCompra),
        preco_atual: parseFloat(precoAtual),
        data_compra: dataCompra,
        quantidade: parseInt(quantidade, 10),
        origem: origemFormatada
      }
      confirm('Salvar alterações do produto "'+nome+'"?') && atualizarProduto(idProduto!, payload)
      .then(() => {
        alert('Produto "'+nome+'" atualizado com sucesso.')
        
      })
    } catch (error) {
      alert('Erro ao salvar produto: ' + error)
      logError('Erro ao salvar produto: ' + error)
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
          setPrecoAtual(produto.preco_atual.replace('R$ ', '').replace('.', '').replace(',', '.'))
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
        try{
          if (confirm('Confirma a exclusão de "'+nome+'"? Esta ação não pode ser desfeita.')) {
            await deletar('produto', idProduto!)
            alert('Produto "'+nome+'" excluído com sucesso.')
            navigate(-1)
          }
        } catch (error) {
          alert('Erro ao excluir produto: ' + error)
          logError('Erro ao excluir produto: ' + error)
        }
    }

  return (
    <div className="app-shell">
      <Topbar pageTitle="Editar produto" />

      <main className="form-page-content">
        {/* Coluna esquerda – formulário */}
        <section className="form-page-left">
          <h2 className="section-title">Editar {nome}</h2>
          <p className="section-subtitle">
            Preencha os dados básicos do produto antes de salvar.
          </p>

          <form onSubmit={handleSubmit}>
            {/* Link + botão de scraping */}
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

            {/* Nome */}
            <FormField
              label="Nome"
              name="nome"
              kind="texto"
              value={nome}
              onChange={setNome}
              required
            />

            {/* URL da imagem */}
            <FormField
              label="URL da imagem"
              name="urlImagem"
              kind="texto"
              value={urlImagem}
              onChange={setUrlImagem}
              placeholder="Link direto para a imagem, se houver"
            />

            {/* Caminho da imagem local */}
            {/* <FormField
              label="Caminho para imagem local"
              name="caminhoImagemLocal"
              kind="texto"
              value={caminhoImagemLocal}
              onChange={setCaminhoImagemLocal}
              placeholder="Caminho/local no disco após download"
            /> */}

            {/* Preços */}
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

            {/* Data e quantidade */}
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

            {/* Origem (dropdown) */}
            <FormSelect
              label="Origem"
              name="origem"
              value={origem}
              onChange={setOrigem}
              options={opcoesOrigem}
              placeholder="Selecione a origem"
            />

            {/* Ações */}
            <div className="form-actions">
              <Button type="submit">Salvar produto</Button>
              <Button type="button" variant="outline" onClick={handleCancelar}>
                Cancelar
              </Button>
               <Button type="button" variant="danger" onClick={handleExcluir}>
                Excluir Produto
              </Button>
            </div>
          </form>
        </section>

        {/* Coluna direita – imagem do produto */}
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
              <>
                Pré-visualização da imagem do produto.                               
              </>
            )}
          </div>
        </aside>
      </main>

      <Footer appName="YU-GI-OH! Manager" />
    </div>
  )
}
