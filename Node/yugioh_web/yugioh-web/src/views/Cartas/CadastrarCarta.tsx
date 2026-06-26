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
  type InserirCartaPayload,
  inserirCarta,
} from '../../Database/db'
import { buscarCartaMyp, type CartaMyP } from '../../../scraping/webScraping'

async function buscarCarta(url: string, chave?: string): Promise<CartaMyP[]> {
  const carta = await buscarCartaMyp(url, chave)
  return carta
}

function extrairCodigoColecao(codigoCarta: string): string {
  const codigoLimpo = String(codigoCarta || '').trim()
  if (!codigoLimpo) return ''

  const separador = codigoLimpo.includes('-') ? '-' : '_'
  const [codigoColecao] = codigoLimpo.split(separador)

  return codigoColecao || ''
}

export function CadastrarCarta() {
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
  const [colecaoPendenteSelecao, setColecaoPendenteSelecao] = useState('')

  const [confirmarCadastroAberto, setConfirmarCadastroAberto] = useState(false)
  const [salvando, setSalvando] = useState(false)
  const [buscandoScraping, setBuscandoScraping] = useState(false)

  const opcoesOrigem = [
    { value: 'myp', label: 'MyPCards' },
    { value: 'liga', label: 'Liga Yugioh' },
  ]

  useEffect(() => {
    async function carregarDados() {
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
    }

    void carregarDados()
  }, [])

  useEffect(() => {
    if (!colecaoPendenteSelecao) return

    const existeOpcao = opcoesColecao.some(
      (opcao) => opcao.value === colecaoPendenteSelecao,
    )

    if (!existeOpcao) return

    setColecao(colecaoPendenteSelecao)
    setColecaoPendenteSelecao('')
  }, [colecaoPendenteSelecao, opcoesColecao])

  function limparFormulario() {
    setLinkCarta('')
    setNome('')
    setCodigo('')
    setPrecoPago('')
    setPrecoAtual('')
    setDataCompra('')
    setQuantidade('')
    setUrlImagem('')
    setOrigem('')
    setRaridade('')
    setQualidade('')
    setColecao('')
  }

  function validarFormulario() {
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

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()

    if (!validarFormulario()) return

    setConfirmarCadastroAberto(true)
  }

  async function confirmarCadastro() {
    if (salvando) return

    setSalvando(true)

    try {
      const origemMapeada =
        origem === 'liga'
          ? 'Liga Yugioh'
          : origem === 'myp'
          ? 'MyPCards'
          : origem

      const novaCarta: InserirCartaPayload = {
        link_site: linkCarta,
        nome,
        codigo,
        preco_da_compra: parseFloat(precoPago),
        preco_atual: parseFloat(precoAtual),
        data_da_compra: dataCompra,
        quantidade: parseInt(quantidade, 10),
        imagem: urlImagem,
        origem: origemMapeada,
        raridade: parseInt(raridade, 10),
        qualidade: qualidade ? parseInt(qualidade, 10) : null,
        colecao: String(parseInt(colecao, 10)),
      }

      const ok = await inserirCarta(novaCarta)

      if (!ok) {
        alert('Erro ao cadastrar carta.')
        return
      }

      setConfirmarCadastroAberto(false)
      alert('Carta cadastrada com sucesso!')
      limparFormulario()
    } catch (error) {
      console.error('Erro ao cadastrar carta:', error)
      alert('Erro ao cadastrar carta.')
    } finally {
      setSalvando(false)
    }
  }

  function cancelarConfirmacao() {
    if (salvando) return
    setConfirmarCadastroAberto(false)
  }

  async function recarregarColecoes(idSelecionado?: number | string | null) {
    const dadosColecao = (await listarColecoes()) as {
      id_colecao: number
      nome: string
      codigo: string
    }[]

    setOpcoesColecao(
      dadosColecao.map((c) => ({
        value: String(c.id_colecao),
        label: c.nome,
      })),
    )

    if (idSelecionado !== undefined && idSelecionado !== null) {
      setColecaoPendenteSelecao(String(idSelecionado))
    }

    return dadosColecao
  }

  async function selecionarColecaoDoScraping(
    nomeColecao: string,
    codigoCarta: string,
  ): Promise<number | null> {
    const nomeLimpo = String(nomeColecao || '').trim()

    if (!nomeLimpo) {
      await recarregarColecoes()
      setColecao('')
      return null
    }

    const existente = await buscarColecao(nomeLimpo)

    if (existente) {
      await recarregarColecoes(existente.id_colecao)
      setColecao(String(existente.id_colecao))
      return existente.id_colecao
    }

    const idCriado = await inserirColecao(
      nomeLimpo,
      extrairCodigoColecao(codigoCarta),
    )

    const colecoesAtualizadas = await recarregarColecoes(idCriado)
    const criadaOuEncontrada =
      idCriado != null
        ? colecoesAtualizadas.find((item) => item.id_colecao === idCriado)
        : colecoesAtualizadas.find(
            (item) =>
              item.nome.trim().toUpperCase() === nomeLimpo.toUpperCase(),
          )

    if (!criadaOuEncontrada) {
      setColecao('')
      return null
    }

    setColecao(String(criadaOuEncontrada.id_colecao))
    setColecaoPendenteSelecao(String(criadaOuEncontrada.id_colecao))

    return criadaOuEncontrada.id_colecao
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

      if (cartas.length === 0) {
        alert('Nenhuma carta encontrada no link fornecido.')
        return
      }

      const carta = cartas[0]

      await selecionarColecaoDoScraping(carta.colecao, carta.codigo)

      const nomeColecao = String(carta.colecao || '').trim()
      let colecaoEncontrada = nomeColecao
        ? await buscarColecao(nomeColecao)
        : null

      if (!colecaoEncontrada && nomeColecao) {
        const idColecaoCriada = await inserirColecao(
          nomeColecao,
          extrairCodigoColecao(carta.codigo),
        )

        const colecoesAtualizadas = await recarregarColecoes(idColecaoCriada)
        if (idColecaoCriada != null) {
          setColecao(String(idColecaoCriada))
        }
        const colecaoCriada =
          idColecaoCriada != null
            ? colecoesAtualizadas.find(
                (item) => item.id_colecao === idColecaoCriada,
              )
            : colecoesAtualizadas.find(
                (item) =>
                  item.nome.trim().toUpperCase() === nomeColecao.toUpperCase(),
              )

        colecaoEncontrada = colecaoCriada ?? null
      }

      if (colecaoEncontrada) {
        await recarregarColecoes(colecaoEncontrada.id_colecao)
        setColecao(String(colecaoEncontrada.id_colecao))
      } else {
        await recarregarColecoes()
        setColecao('')
        alert(
          `A coleção "${carta.colecao}" não existe no banco. Selecione uma coleção manualmente antes de salvar.`,
        )
      }

      if (carta.origem?.toUpperCase() === 'MYPCARDS') {
        setOrigem('myp')
      } else if (carta.origem?.toUpperCase() === 'LIGA YUGIOH') {
        setOrigem('liga')
      } else {
        setOrigem('')
      }

      setNome(carta.nome || '')
      setCodigo(carta.codigo || '')
      setUrlImagem(carta.imagem || '')
      setPrecoAtual(carta.preco_atual ? String(carta.preco_atual) : '')
    } catch (error) {
      console.error('Erro ao buscar carta:', error)
      alert('Erro ao buscar carta.')
    } finally {
      setBuscandoScraping(false)
    }
  }

  function handleCancelar() {
    limparFormulario()
  }

  return (
    <div className="app-shell">
      <Topbar pageTitle="Cadastrar carta" />

      <main className="form-page-content">
        <section className="form-page-left">
          <h2 className="section-title section-title-with-help">
            Cadastrar nova carta
            <PageHelpButton
              configKey="cartas.cadastrar"
              fallbackTitle="Como cadastrar uma carta"
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
                key={`colecao-${colecao}-${opcoesColecao.length}`}
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

      {confirmarCadastroAberto && (
        <div className="confirm-modal-backdrop">
          <div className="confirm-modal-card">
            <h3 className="confirm-modal-title">Confirmar cadastro</h3>

            <p className="confirm-modal-text">
              Deseja realmente cadastrar esta carta?
            </p>

            <div className="confirm-modal-actions">
              <Button
                type="button"
                variant="outline"
                onClick={cancelarConfirmacao}
                disabled={salvando}
              >
                Cancelar
              </Button>

              <Button
                type="button"
                onClick={confirmarCadastro}
                disabled={salvando}
              >
                {salvando ? 'Salvando...' : 'Confirmar'}
              </Button>
            </div>
          </div>
        </div>
      )}

      <Footer />
    </div>
  )
}
