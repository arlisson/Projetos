import { useEffect, useMemo, useState } from 'react'
import { Topbar } from '../../components/topBar'
import { Footer } from '../../components/footer'
import { FormField } from '../../components/formField'
import { FormSelect } from '../../components/formSelect'
import { Button } from '../../components/botao'
import { Loading } from '../../components/Loading'
import {
  listarRaridadeQualidade,
  listarColecoes,
  type QualidadeDB,
  type RaridadeDB,
  type OpcaoSelect,
  buscarColecao,
  inserirColecao,
  type InserirCartaPayload,
  inserirCarta,
} from '../../Database/db'
import {
  buscarCartasColecao,
  type CartaMyP,
} from '../../../scraping/webScraping'

type CartaSelecionavel = CartaMyP & {
  selecionada: boolean
  precoPago: string
  raridadeId: string
  qualidadeId: string
  colecaoId: string
  quantidade: string
}

function normalizarNumero(valor: string | number): number {
  if (typeof valor === 'number') {
    return Number.isFinite(valor) ? valor : 0
  }

  let texto = String(valor || '').trim()

  if (!texto) return 0

  texto = texto.replace(/\s+/g, '')

  const temVirgula = texto.includes(',')
  const temPonto = texto.includes('.')

  if (temVirgula && temPonto) {
    // Ex.: 1.234,56 -> remove milhares e troca decimal
    if (texto.lastIndexOf(',') > texto.lastIndexOf('.')) {
      texto = texto.replace(/\./g, '').replace(',', '.')
    } else {
      // Ex.: 1,234.56 -> remove milhares com vírgula
      texto = texto.replace(/,/g, '')
    }
  } else if (temVirgula) {
    // Ex.: 122,94
    texto = texto.replace(',', '.')
  } else {
    // Ex.: 122.94
    // mantém como está
  }

  const numero = Number(texto)
  return Number.isFinite(numero) ? numero : 0
}

function isValidUrl(value: string): boolean {
  try {
    new URL(value)
    return true
  } catch {
    return false
  }
}

export function CadastrarCartasColecao() {
  const [linkColecao, setLinkColecao] = useState('')
  const [dataCompra, setDataCompra] = useState('')
  const [carregando, setCarregando] = useState(false)
  const [salvando, setSalvando] = useState(false)
  const [filtro, setFiltro] = useState('')
  const [cartas, setCartas] = useState<CartaSelecionavel[]>([])

  const [opcoesQualidade, setOpcoesQualidade] = useState<OpcaoSelect[]>([])
  const [opcoesRaridade, setOpcoesRaridade] = useState<OpcaoSelect[]>([])

  useEffect(() => {
    async function carregarDados() {
      const dadosQualidade = (await listarRaridadeQualidade(
        'qualidade',
      )) as unknown as QualidadeDB[]

      const qualidades = dadosQualidade.map((q) => ({
        value: String(q.id_qualidade),
        label: q.nome,
      }))

      setOpcoesQualidade(qualidades)

      const dadosRaridade = (await listarRaridadeQualidade(
        'raridade',
      )) as unknown as RaridadeDB[]

      const raridades = dadosRaridade.map((r) => ({
        value: String(r.id_raridade),
        label: r.nome,
      }))

      setOpcoesRaridade(raridades)
    }

    void carregarDados()
  }, [])

  async function garantirColecao(nomeColecao: string): Promise<string> {
    const colecaoExistente = await buscarColecao(nomeColecao)

    if (colecaoExistente) {
      return String(colecaoExistente.id_colecao)
    }

    await inserirColecao(nomeColecao, '')

    const todasColecoes = (await listarColecoes()) as unknown as {
      id_colecao: number
      nome: string
    }[]

    const encontrada = todasColecoes.find(
      (c) => c.nome.trim().toLowerCase() === nomeColecao.trim().toLowerCase(),
    )

    return encontrada ? String(encontrada.id_colecao) : ''
  }

  function resolverRaridadeIdPorNome(raridadeNome: string): string {
    const encontrada = opcoesRaridade.find(
      (item) =>
        item.label.trim().toLowerCase() === raridadeNome.trim().toLowerCase(),
    )

    return encontrada?.value || ''
  }

  const podeBuscarColecao =
    linkColecao.trim() !== '' &&
    dataCompra.trim() !== '' &&
    !carregando &&
    !salvando

  async function handleBuscarColecao() {
    if (!linkColecao.trim() || !dataCompra.trim()) {
      alert('Preencha os campos obrigatórios antes de buscar a coleção.')
      return
    }

    if (!isValidUrl(linkColecao.trim())) {
      alert('Informe uma URL válida da coleção.')
      return
    }

    setCarregando(true)
    setCartas([])

    try {
      const resultado = await buscarCartasColecao(linkColecao.trim())

      if (!resultado.length) {
        alert('Nenhuma carta foi encontrada para esta coleção.')
        return
      }

      const cartasPreparadas: CartaSelecionavel[] = []

      for (const carta of resultado) {
        const colecaoId = await garantirColecao(carta.colecao)
        const raridadeId = resolverRaridadeIdPorNome(carta.raridade)

        cartasPreparadas.push({
          ...carta,
          selecionada: true,
          precoPago: '',
          raridadeId,
          qualidadeId: '',
          colecaoId,
          quantidade: '1',
        })
      }

      setCartas(cartasPreparadas)
    } catch (error) {
      console.error(error)
      alert('Erro ao buscar cartas da coleção.')
    } finally {
      setCarregando(false)
    }
  }

  function atualizarCarta(
    linkSite: string,
    campo: keyof CartaSelecionavel,
    valor: string | boolean,
    ) {
    setCartas((prev) =>
        prev.map((c) => (c.link_site === linkSite ? { ...c, [campo]: valor } : c)),
    )
    }

  function selecionarTodas(valor: boolean) {
    setCartas((prev) => prev.map((c) => ({ ...c, selecionada: valor })))
  }

  const cartasFiltradas = useMemo(() => {
    const termo = filtro.trim().toLowerCase()

    if (!termo) return cartas

    return cartas.filter(
      (c) =>
        c.nome.toLowerCase().includes(termo) ||
        c.codigo.toLowerCase().includes(termo) ||
        c.raridade.toLowerCase().includes(termo) ||
        c.colecao.toLowerCase().includes(termo),
    )
  }, [cartas, filtro])

  async function handleSalvar() {
    const selecionadas = cartas.filter((c) => c.selecionada)

    if (!linkColecao.trim() || !dataCompra.trim()) {
      alert('Preencha o link da coleção e a data da compra.')
      return
    }

    if (!selecionadas.length) {
      alert('Selecione ao menos uma carta.')
      return
    }

    for (const carta of selecionadas) {
      if (!carta.precoPago.trim()) {
        alert(`Informe o preço pago para a carta "${carta.nome}".`)
        return
      }

      if (!carta.raridadeId) {
        alert(`Selecione a raridade comprada para a carta "${carta.nome}".`)
        return
      }

      if (!carta.qualidadeId) {
        alert(`Selecione a qualidade comprada para a carta "${carta.nome}".`)
        return
      }

      if (!carta.quantidade.trim() || Number(carta.quantidade) <= 0) {
        alert(`Informe uma quantidade válida para a carta "${carta.nome}".`)
        return
      }
    }

    setSalvando(true)

    try {
      for (const carta of selecionadas) {
        const payload: InserirCartaPayload = {
          link_site: carta.link_site,
          nome: carta.nome,
          codigo: carta.codigo,
          preco_da_compra: normalizarNumero(carta.precoPago),
          preco_atual: normalizarNumero(carta.preco_atual),
          data_da_compra: dataCompra,
          quantidade: parseInt(carta.quantidade, 10),
          imagem: carta.imagem,
          origem: 'MyPCards',
          raridade: parseInt(carta.raridadeId, 10),
          qualidade: parseInt(carta.qualidadeId, 10),
          colecao: carta.colecaoId || null,
        }

        await inserirCarta(payload)
      }

      alert('Cartas cadastradas com sucesso.')
      handleCancelar()
    } catch (error) {
      console.error(error)
      alert('Erro ao salvar cartas da coleção.')
    } finally {
      setSalvando(false)
    }
  }

  function handleCancelar() {
    setCartas([])
    setFiltro('')
    setLinkColecao('')
    setDataCompra('')
  }

  return (
    <div className="app-shell">
      <Topbar pageTitle="Cadastrar cartas por coleção" />

      <main className="form-page-content">
        <section className="form-page-left" style={{ maxWidth: '100%' }}>
          <h2 className="section-title">Cadastro em lote por coleção</h2>
          <p className="section-subtitle">
            Busque uma coleção do MyPCards e preencha os dados de compra de cada
            carta individualmente.
          </p>

          <div className="form-row-inline">
            <FormField
              label="Link da coleção"
              name="linkColecao"
              kind="texto"
              value={linkColecao}
              onChange={setLinkColecao}
              placeholder="URL da coleção no MyPCards"
              required
            />

            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={handleBuscarColecao}
              disabled={!podeBuscarColecao}
            >
              {carregando ? 'Buscando...' : 'Buscar coleção'}
            </Button>
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
          </div>

          {carregando && (
            <div style={{ marginTop: '1.5rem' }}>
              <Loading message="Buscando cartas da coleção..." />
            </div>
          )}

          {!carregando && cartas.length > 0 && (
            <>
              <div className="form-row-inline" style={{ marginTop: '1rem' }}>
                <FormField
                  label="Filtrar cartas"
                  name="filtro"
                  kind="texto"
                  value={filtro}
                  onChange={setFiltro}
                  placeholder="Nome, código, raridade ou coleção"
                />
              </div>

              <div
                className="form-actions"
                style={{ justifyContent: 'flex-start', marginTop: '1rem' }}
              >
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => selecionarTodas(true)}
                >
                  Selecionar todas
                </Button>

                <Button
                  type="button"
                  variant="outline"
                  onClick={() => selecionarTodas(false)}
                >
                  Desmarcar todas
                </Button>
              </div>

              <div style={{ marginTop: '1.5rem' }}>
                {cartasFiltradas.map((carta) => (
                    <div
                        key={carta.link_site}
                        style={{
                        display: 'grid',
                        gridTemplateColumns: '110px 1fr',
                        gap: '1rem',
                        border: '1px solid rgba(255,255,255,0.08)',
                        borderRadius: '12px',
                        padding: '1rem',
                        marginBottom: '1rem',
                        background: 'rgba(255,255,255,0.02)',
                        }}
                    >
                        <div>
                        <img
                            src={carta.imagem}
                            alt={carta.nome}
                            style={{
                            width: '100%',
                            borderRadius: '10px',
                            objectFit: 'cover',
                            }}
                        />
                        </div>

                        <div>
                        <div
                            style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            gap: '1rem',
                            alignItems: 'flex-start',
                            marginBottom: '0.9rem',
                            }}
                        >
                            <div>
                            <strong>{carta.nome}</strong>
                            <div>Código: {carta.codigo}</div>
                            <div>Raridade encontrada: {carta.raridade}</div>
                            <div>Coleção: {carta.colecao}</div>
                            <div>Preço atual: R$ {carta.preco_atual}</div>
                            </div>

                            <label style={{ whiteSpace: 'nowrap' }}>
                            <input
                                type="checkbox"
                                checked={carta.selecionada}
                                onChange={(e) =>
                                atualizarCarta(
                                    carta.link_site,
                                    'selecionada',
                                    e.target.checked,
                                )
                                }
                            />{' '}
                            Selecionar
                            </label>
                        </div>

                        <div
                            style={{
                            display: 'grid',
                            gridTemplateColumns: '1fr 1fr',
                            gap: '1rem',
                            marginBottom: '1rem',
                            }}
                        >
                            <FormField
                            label="Preço pago"
                            name={`precoPago-${carta.link_site}`}
                            kind="numero"
                            value={carta.precoPago}
                            onChange={(value) =>
                                atualizarCarta(carta.link_site, 'precoPago', value)
                            }
                            placeholder="Valor pago nesta carta"
                            required
                            />

                            <FormField
                            label="Quantidade"
                            name={`quantidade-${carta.link_site}`}
                            kind="numero"
                            value={carta.quantidade}
                            onChange={(value) =>
                                atualizarCarta(carta.link_site, 'quantidade', value)
                            }
                            required
                            />
                        </div>

                        <div
                            style={{
                            display: 'grid',
                            gridTemplateColumns: '1fr 1fr',
                            gap: '1rem',
                            }}
                        >
                            <FormSelect
                            label="Raridade comprada"
                            name={`raridade-${carta.link_site}`}
                            value={carta.raridadeId}
                            onChange={(value) =>
                                atualizarCarta(carta.link_site, 'raridadeId', value)
                            }
                            options={opcoesRaridade}
                            placeholder="Selecione a raridade"
                            required
                            />

                            <FormSelect
                            label="Qualidade comprada"
                            name={`qualidade-${carta.link_site}`}
                            value={carta.qualidadeId}
                            onChange={(value) =>
                                atualizarCarta(carta.link_site, 'qualidadeId', value)
                            }
                            options={opcoesQualidade}
                            placeholder="Selecione a qualidade"
                            required
                            />
                        </div>
                        </div>
                    </div>
                ))}
              </div>
            </>
          )}

          <div className="form-actions" style={{ marginTop: '1.5rem' }}>
            <Button
              type="button"
              onClick={handleSalvar}
              disabled={carregando || salvando || cartas.length === 0}
            >
              {salvando ? 'Salvando...' : 'Salvar cartas selecionadas'}
            </Button>

            <Button
              type="button"
              variant="outline"
              onClick={handleCancelar}
              disabled={carregando || salvando}
            >
              Cancelar
            </Button>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  )
}