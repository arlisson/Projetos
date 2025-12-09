import { useState } from 'react'
import { Topbar } from '../../components/topBar'
import { Footer } from '../../components/footer'
import { FormField } from '../../components/formField'
import { FormSelect } from '../../components/formSelect'
import { Button } from '../../components/botao'

export function CadastrarProduto() {
  const [link, setLink] = useState('')
  const [nome, setNome] = useState('')
  const [urlImagem, setUrlImagem] = useState('')
  const [caminhoImagemLocal, setCaminhoImagemLocal] = useState('')
  const [precoCompra, setPrecoCompra] = useState('')
  const [precoAtual, setPrecoAtual] = useState('')
  const [dataCompra, setDataCompra] = useState('')
  const [quantidade, setQuantidade] = useState('')
  const [origem, setOrigem] = useState('')

  // Futuramente estes valores virão do banco
  const opcoesOrigem = [
    { value: 'compra', label: 'Compra' },
    { value: 'troca', label: 'Troca' },
    { value: 'presente', label: 'Presente' },
  ]

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    // lógica de salvar produto
  }

  function handleScraping() {
    // lógica de scraping para o produto
  }

  function handleCancelar() {
    // limpar ou navegar de volta
  }

  return (
    <div className="app-shell">
      <Topbar pageTitle="Cadastrar produto" />

      <main className="form-page-content">
        {/* Coluna esquerda – formulário */}
        <section className="form-page-left">
          <h2 className="section-title">Cadastrar novo produto</h2>
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
            <FormField
              label="Caminho para imagem local"
              name="caminhoImagemLocal"
              kind="texto"
              value={caminhoImagemLocal}
              onChange={setCaminhoImagemLocal}
              placeholder="Caminho/local no disco após download"
            />

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
            </div>
          </form>
        </section>

        {/* Coluna direita – imagem do produto */}
        <aside className="form-page-right">
          <div className="form-image-label">Imagem do produto</div>
          <div className="form-image-placeholder">
            Pré-visualização da imagem do produto.
            <br />
            (Componente de upload / preview será implementado aqui.)
          </div>
        </aside>
      </main>

      <Footer appName="YU-GI-OH! Manager" />
    </div>
  )
}
