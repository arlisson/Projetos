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
   buscarCartaId,
   deletar,
   atualizarCarta,
   type InserirCartaPayload,
   type InserirVendaCartaPayload,
   venderCarta,
   todayStr
   } from '../../Database/db'
import { buscarCartaMyp, type CartaMyP } from '../../../scraping/webScraping'
import { useSearchParams,useNavigate } from 'react-router-dom'
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
    const [quantidadeVenda, setQuantidadeVenda] = useState('');
    const [valorVenda, setValorVenda] = useState('');
    const [modalVenderAberto, setModalVenderAberto] = useState(false)

  
    useEffect(() => {
        if (!idCarta) return
        async function carregarDadosCarta() {
            const carta = await buscarCartaId(idCarta!)
            if (carta) {
                setLinkCarta(carta.link_site || '')
                setNome(carta.nome || '')
                setCodigo(carta.codigo || '')
                setPrecoPago(carta.preco_da_compra ? String(carta.preco_da_compra) : '')
                setPrecoAtual(carta.preco_atual ? String(carta.preco_atual) : '')
                setDataCompra(carta.data_da_compra ? carta.data_da_compra.toString().split('T')[0] : '')
                setQuantidade(carta.quantidade ? String(carta.quantidade) : '')
                setUrlImagem(carta.imagem || '')
                if(carta.origem?.toUpperCase() === 'MYPCARDS') {
                    setOrigem('myp')
                }else if(carta.origem?.toUpperCase() === 'LIGA YUGIOH') {
                    setOrigem('liga')
                }else{
                    setOrigem('')
                }
                
                setRaridade(carta.raridade ? String(carta.raridade) : '')
                setQualidade(carta.qualidade ? String(carta.qualidade) : '')
                setColecao(carta.colecao ? String(carta.colecao) : '')
            }
        }




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
        void carregarDadosCarta()
    }, [idCarta])



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
    { value: 'myp', label: 'MyPCards' },
    { value: 'liga', label: 'Liga Yugioh' },   
  ] 


  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    // Validar campos obrigatórios
    if (!nome || !codigo || !precoPago || !precoAtual || !dataCompra || !quantidade || !origem || !raridade || !colecao) {
      alert('Por favor, preencha todos os campos obrigatórios.')
      return
    }
    try {
      const origemFormatada = origem === 'myp' ? 'MyPCards' : origem === 'liga' ? 'Liga Yugioh' : ''
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
        colecao: colecao || null
      }
      confirm('Salvar alterações da carta "'+nome+'"?') && atualizarCarta(idCarta!, payload)
      .then(() => {
        alert('Carta "'+nome+'" atualizada com sucesso.')
        
      })       
        
     
    } catch (error) {
      alert('Erro ao salvar carta: ' + error)
      logError('Erro ao salvar carta: ' + error)
    }
    
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
        if(carta.origem.toUpperCase()==='MYPCARDS'){
          setOrigem('myp')
        }else{
          setOrigem(carta.origem || '')
        }

      } else {
        alert('Nenhuma carta encontrada no link fornecido.')
      }
    } catch (error) {
      console.error('Erro ao buscar carta:', error)
      alert('Erro ao buscar carta.' + String(error))
    }
  }

  function handleCancelar() {
    navigate(-1)
  }

  async function handleExcluir(): Promise<void> {
      try{
        if (confirm('Confirma a exclusão de "'+nome+'"? Esta ação não pode ser desfeita.')) {
          await deletar('carta', idCarta!)
          alert('Carta "'+nome+'" excluída com sucesso.')
          navigate(-1)
        }
      } catch (error) {
        alert('Erro ao excluir carta: ' + error)
        logError('Erro ao excluir carta: ' + error)
      }
  }

   function handleVender(): void {
    setQuantidadeVenda('')
    setModalVenderAberto(true)
  }

  async function confirmarVenda(): Promise<void> {
    const qtd = Number(quantidadeVenda)

    if (!Number.isFinite(qtd) || qtd <= 0) {
      alert('Informe uma quantidade válida.')
      return
    }else if (qtd > Number(quantidade)) {
      alert('Quantidade a vender não pode ser maior que a quantidade em estoque.')
      return
    }

    if (valorVenda){
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
      }
      const origemFormatada = origem === 'myp' ? 'MyPCards' : origem === 'liga' ? 'Liga Yugioh' : ''
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
        colecao: colecao || null
      }

      await venderCarta(payloadCarta, payload, qtd)
      alert(`${qtd} unidade(s) de ${nome} vendida(s).`)
      setModalVenderAberto(false)
      setQuantidade(String(Number(quantidade) - qtd))
    } catch (err) {
      alert(`Erro ao registrar venda da carta:${nome}\n ${err}`)
    }
  }

  function cancelarVenda(): void {
    setModalVenderAberto(false)
  }

  return (
    <div className="app-shell">
      <Topbar pageTitle="Editar carta" />

      <main className="form-page-content">
        {/* Coluna esquerda – formulário */}
        <section className="form-page-left">
          <h2 className="section-title">Editar {nome}</h2>
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
