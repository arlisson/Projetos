import { useEffect, useState } from 'react'
import { Topbar } from '../../components/topBar'
import { Footer } from '../../components/footer'
import { FormField } from '../../components/formField'
import { FormSelect } from '../../components/formSelect'
import { Button } from '../../components/botao'
import { listarRaridadeQualidade,
   listarColecoes,
   type QualidadeDB, 
   type RaridadeDB, 
   type OpcaoSelect, 
   buscarQualidadeRaridadeId,
   buscarColecao,
   inserirColecao,
   type InserirCartaPayload,
   inserirCarta } from '../../Database/db'
import { buscarCartaMyp, type CartaMyP } from '../../../scraping/webScraping'


async function buscarCarta(url: string, chave?: string): Promise<CartaMyP[]> {
  const carta = await buscarCartaMyp(url, chave)
  return carta
}



export function CadastrarCarta() {

    useEffect(() => {
      async function carregarQualidades() {
        const dados_qualidade = (await listarRaridadeQualidade(
          'qualidade'
        )) as unknown as QualidadeDB[]      

        

        const opcoes = dados_qualidade.map((q) => ({
          value: String(q.id_qualidade), // ou q.nome, se preferir
          label: q.nome,
        }))

        setOpcoesQualidade(opcoes)

        const dados_raridade = (await listarRaridadeQualidade(
          'raridade'
        )) as unknown as RaridadeDB[]
        const opcoes_raridade = dados_raridade.map((r) => ({
          value: String(r.id_raridade), // ou r.nome, se preferir
          label: r.nome,
        }))
        setOpcoesRaridade(opcoes_raridade)

        const dados_colecao = (await listarColecoes()) as unknown as {
          id_colecao: number
          nome: string
        }[]
        const opcoes_colecao = dados_colecao.map((c) => ({
          value: String(c.id_colecao), // ou c.nome, se preferir
          label: c.nome,
        }))
        setOpcoesColecao(opcoes_colecao)
      }

      void carregarQualidades()
    }, [])



  const [linkCarta, setLinkCarta] = useState('')
  const [nome, setNome] = useState('')
  const [codigo, setCodigo] = useState('')
  const [precoPago, setPrecoPago] = useState('')
  const [precoAtual, setPrecoAtual] = useState('')
  const [dataCompra, setDataCompra] = useState('')
  const [quantidade, setQuantidade] = useState('')
  const [urlImagem, setUrlImagem] = useState('')
  //const [localImagem, setLocalImagem] = useState('')

  const [origem, setOrigem] = useState('')
  const [raridade, setRaridade] = useState('')
  const [qualidade, setQualidade] = useState('')
  const [colecao, setColecao] = useState('')
  const [opcoesRaridade, setOpcoesRaridade] = useState<OpcaoSelect[]>([])
  const [opcoesQualidade, setOpcoesQualidade] = useState<OpcaoSelect[]>([])
  const [opcoesColecao, setOpcoesColecao] = useState<OpcaoSelect[]>([])


  // Estes arrays futuramente virão do banco de dados
  const opcoesOrigem = [
    { value: 'myp', label: 'MYPCards' },
    { value: 'liga', label: 'Liga Yugioh' },   
  ]

  


  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    // Validar campos obrigatórios
    if (!nome || !codigo || !precoPago || !precoAtual || !dataCompra || !quantidade || !origem || !raridade || !colecao) {
      alert('Por favor, preencha todos os campos obrigatórios.')
      return
    }
    // Preparar dados para inserção
    const novaCarta: InserirCartaPayload = {
      link_site: linkCarta,
      nome: nome,
      codigo: codigo,
      preco_da_compra: parseFloat(precoPago),
      preco_atual: parseFloat(precoAtual),
      data_da_compra: dataCompra,
      quantidade: parseInt(quantidade, 10),
      imagem: urlImagem,
      //local_imagem: localImagem,
      origem: origem,
      raridade: parseInt(raridade, 10),
      qualidade: qualidade ? parseInt(qualidade, 10) : null,
      colecao: String(parseInt(colecao, 10)),
    }
    // Inserir no banco de dados
    confirm('Confirma o cadastro desta carta?') && inserirCarta(novaCarta)
      .then(() => {
        alert('Carta cadastrada com sucesso!')
        // Limpar formulário
        setLinkCarta('')
        setNome('')
        setCodigo('')
        setPrecoPago('')
        setPrecoAtual('')
        setDataCompra('')
        setQuantidade('')
        setUrlImagem('')
        //setLocalImagem('')
        setOrigem('')
        setRaridade('')
        setQualidade('')
        setColecao('')
      })
      .catch((err) => {
        console.error('Erro ao cadastrar carta:', err)
        alert('Erro ao cadastrar carta. Verifique o console para mais detalhes.')
      })
  }

  async function handleScraping() {
    if (raridade === '') {
      alert('Por favor, selecione a raridade antes de buscar via scraping.')
      return
    }
    try {
      const raridadeNome = await buscarQualidadeRaridadeId(parseInt(raridade, 10), 'raridade')
      const cartas = await buscarCarta(linkCarta, raridadeNome || undefined)
      if (cartas.length > 0) {
        const carta = cartas[0]
        const colecaoEncontrada = await buscarColecao(carta.colecao)

      if (colecaoEncontrada) {
        // Já existe no banco: só seleciona
        setColecao(String(colecaoEncontrada.id_colecao))
      } else {
        // Insere nova coleção
        const novoId = await inserirColecao(carta.colecao, '')

        // Recarrega todas as coleções para atualizar as opções
        const dados_colecao = (await listarColecoes()) as {
          id_colecao: number
          nome: string
        }[]

        const opcoes_colecao: OpcaoSelect[] = dados_colecao.map((c) => ({
          value: String(c.id_colecao),
          label: c.nome,
        }))

        setOpcoesColecao(opcoes_colecao)

        // Seleciona a nova coleção (id recém inserido)
        setColecao(String(novoId))
      }
        setNome(carta.nome || '')
        setCodigo(carta.codigo || '')
        setUrlImagem(carta.imagem || '')
        setPrecoAtual(carta.preco_atual ? String(carta.preco_atual) : '')

      } else {
        alert('Nenhuma carta encontrada no link fornecido.')
      }
    } catch (error) {
      console.error('Erro ao buscar carta:', error)
      alert('Erro ao buscar carta.')
    }
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

            {/* <FormField
              label="Local da imagem baixada"
              name="localImagem"
              kind="texto"
              value={localImagem}
              onChange={setLocalImagem}
              placeholder="Caminho/local no disco após download"
            /> */}

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
            {urlImagem ? (
              <img
                src={urlImagem}
                alt={nome ? `Imagem da carta ${nome}` : 'Imagem da carta'}
                className="card-image-preview"
              />
            ) : (
              <>
                Pré-visualização da imagem da carta.                               
              </>
            )}
          </div>
        </aside>

      </main>

      <Footer  />
    </div>
  )
}
