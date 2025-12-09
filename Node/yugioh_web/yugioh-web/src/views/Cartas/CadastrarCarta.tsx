import { useEffect, useState } from 'react'
import { Topbar } from '../../components/topBar'
import { Footer } from '../../components/footer'
import { FormField } from '../../components/formField'
import { FormSelect } from '../../components/formSelect'
import { Button } from '../../components/botao'
import { testDbConnection } from '../../Database/db'

export function CadastrarCarta() {

  useEffect(() => {
      
    
  
      testDbConnection().then((res) => {
        console.log(res.message)
      })
    }, [])


  const [linkCarta, setLinkCarta] = useState('')
  const [nome, setNome] = useState('')
  const [codigo, setCodigo] = useState('')
  const [precoPago, setPrecoPago] = useState('')
  const [precoAtual, setPrecoAtual] = useState('')
  const [dataCompra, setDataCompra] = useState('')
  const [quantidade, setQuantidade] = useState('')
  const [urlImagem, setUrlImagem] = useState('')
  const [localImagem, setLocalImagem] = useState('')

  const [origem, setOrigem] = useState('')
  const [raridade, setRaridade] = useState('')
  const [qualidade, setQualidade] = useState('')
  const [colecao, setColecao] = useState('')

  // Estes arrays futuramente virão do banco de dados
  const opcoesOrigem = [
    { value: 'compra', label: 'Compra' },
    { value: 'troca', label: 'Troca' },
    { value: 'presente', label: 'Presente' },
  ]

  const opcoesRaridade = [
    { value: 'comum', label: 'Comum' },
    { value: 'rara', label: 'Rara' },
    { value: 'sr', label: 'Super Rara' },
    { value: 'ur', label: 'Ultra Rara' },
    { value: 'secret', label: 'Secret' },
  ]

  const opcoesQualidade = [
    { value: 'nm', label: 'Near Mint' },
    { value: 'lp', label: 'Lightly Played' },
    { value: 'mp', label: 'Moderately Played' },
    { value: 'hp', label: 'Heavily Played' },
  ]

  const opcoesColecao = [
    { value: 'lob', label: 'LOB' },
    { value: 'mrd', label: 'MRD' },
    { value: 'sd', label: 'Structure Deck' },
    // etc. – depois você carrega do banco
  ]

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    // lógica de salvar carta
  }

  function handleScraping() {
    // lógica de scraping
  }

  function handleCancelar() {
    // limpar ou navegar de volta
  }

  return (
    <div className="app-shell">
      <Topbar pageTitle="Cadastrar carta" />

      <main className="form-page-content">
        {/* Coluna esquerda – formulário */}
        <section className="form-page-left">
          <h2 className="section-title">Cadastrar nova carta</h2>
          <p className="section-subtitle">
            Preencha os dados básicos da carta antes de salvar.
          </p>

          <form onSubmit={handleSubmit}>
            {/* Link da carta + scraping */}
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

            {/* Código */}
            <FormField
              label="Código"
              name="codigo"
              kind="texto"
              value={codigo}
              onChange={setCodigo}
              required
            />

            {/* Preços */}
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

            {/* Data + quantidade */}
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

            {/* URLs de imagem */}
            <FormField
              label="URL da imagem"
              name="urlImagem"
              kind="texto"
              value={urlImagem}
              onChange={setUrlImagem}
              placeholder="Link direto para a imagem, se houver"
            />

            <FormField
              label="Local da imagem baixada"
              name="localImagem"
              kind="texto"
              value={localImagem}
              onChange={setLocalImagem}
              placeholder="Caminho/local no disco após download"
            />

            {/* Dropdowns: origem, raridade, qualidade, coleção */}
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

            {/* Ações */}
            <div className="form-actions">
              <Button type="submit">Salvar carta</Button>
              <Button type="button" variant="outline" onClick={handleCancelar}>
                Cancelar
              </Button>
            </div>
          </form>
        </section>

        {/* Coluna direita – imagem da carta */}
        <aside className="form-page-right">
          <div className="form-image-label">Imagem da carta</div>
          <div className="form-image-placeholder">
            Pré-visualização da imagem da carta.
            <br />
            (Componente de upload / preview será implementado aqui.)
          </div>
        </aside>
      </main>

      <Footer  />
    </div>
  )
}
