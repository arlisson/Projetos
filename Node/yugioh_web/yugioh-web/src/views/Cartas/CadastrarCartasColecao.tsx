import { useEffect, useMemo, useState } from 'react'
import { Topbar } from '../../components/topBar'
import { Footer } from '../../components/footer'
import { FormField } from '../../components/formField'
import { FormSelect } from '../../components/formSelect'
import { Button } from '../../components/botao'
import { Loading } from '../../components/Loading'
import { PageHelpButton } from '../../components/PageHelpButton'
import {
  listarRaridadeQualidade,
  listarColecoes,
  type QualidadeDB,
  type RaridadeDB,
  type OpcaoSelect,
  buscarColecao,
  inserirColecao,
  garantirRaridade,
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
    if (texto.lastIndexOf(',') > texto.lastIndexOf('.')) {
      texto = texto.replace(/\./g, '').replace(',', '.')
    } else {
      texto = texto.replace(/,/g, '')
    }
  } else if (temVirgula) {
    texto = texto.replace(',', '.')
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
  const [valorPagoPadrao, setValorPagoPadrao] = useState('')
  const [qualidadePadrao, setQualidadePadrao] = useState('')
  const [carregando, setCarregando] = useState(false)
  const [salvando, setSalvando] = useState(false)
  const [filtro, setFiltro] = useState('')
  const [cartas, setCartas] = useState<CartaSelecionavel[]>([])
  const [modalSalvarAberto, setModalSalvarAberto] = useState(false)

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

  async function resolverOuCriarRaridadeId(
    raridadeNome: string,
  ): Promise<string> {
    const nomeLimpo = String(raridadeNome || '').trim()

    if (!nomeLimpo) return ''

    const encontrada = opcoesRaridade.find(
      (item) => item.label.trim().toLowerCase() === nomeLimpo.toLowerCase(),
    )

    if (encontrada) {
      return encontrada.value
    }

    const id = await garantirRaridade(nomeLimpo)

    if (!id) return ''

    await recarregarRaridades()
    return String(id)
  }

  const podeBuscarColecao =
    linkColecao.trim() !== '' &&
    dataCompra.trim() !== '' &&
    !carregando &&
    !salvando

  async function recarregarRaridades() {
    const dadosRaridade = (await listarRaridadeQualidade(
      'raridade',
    )) as unknown as RaridadeDB[]

    const raridades = dadosRaridade.map((r) => ({
      value: String(r.id_raridade),
      label: r.nome,
    }))

    setOpcoesRaridade(raridades)
  }

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
        const raridadeId = await resolverOuCriarRaridadeId(carta.raridade)

        cartasPreparadas.push({
          ...carta,
          selecionada: true,
          precoPago: valorPagoPadrao.trim(),
          raridadeId,
          qualidadeId: qualidadePadrao.trim(),
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

  function aplicarValorPagoPadraoNasSelecionadas() {
    if (!valorPagoPadrao.trim()) {
      alert('Informe um valor pago padrão para aplicar.')
      return
    }

    setCartas((prev) =>
      prev.map((c) =>
        c.selecionada ? { ...c, precoPago: valorPagoPadrao.trim() } : c,
      ),
    )
  }

  function aplicarQualidadePadraoNasSelecionadas() {
    if (!qualidadePadrao.trim()) {
      alert('Selecione uma qualidade padrão para aplicar.')
      return
    }

    setCartas((prev) =>
      prev.map((c) =>
        c.selecionada ? { ...c, qualidadeId: qualidadePadrao } : c,
      ),
    )
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

  function validarAntesDeSalvar(): boolean {
    const selecionadas = cartas.filter((c) => c.selecionada)

    if (!linkColecao.trim() || !dataCompra.trim()) {
      alert('Preencha o link da coleção e a data da compra.')
      return false
    }

    if (!selecionadas.length) {
      alert('Selecione ao menos uma carta.')
      return false
    }

    for (const carta of selecionadas) {
      if (!carta.precoPago.trim()) {
        alert(`Informe o preço pago para a carta "${carta.nome}".`)
        return false
      }

      if (!carta.raridadeId) {
        alert(`Selecione a raridade comprada para a carta "${carta.nome}".`)
        return false
      }

      if (!carta.qualidadeId) {
        alert(`Selecione a qualidade comprada para a carta "${carta.nome}".`)
        return false
      }

      if (!carta.quantidade.trim() || Number(carta.quantidade) <= 0) {
        alert(`Informe uma quantidade válida para a carta "${carta.nome}".`)
        return false
      }
    }

    return true
  }

  function handleSalvar() {
    if (!validarAntesDeSalvar()) return
    setModalSalvarAberto(true)
  }

  async function confirmarSalvar() {
    const selecionadas = cartas.filter((c) => c.selecionada)

    if (salvando || !selecionadas.length) return

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

      setModalSalvarAberto(false)
      alert('Cartas cadastradas com sucesso.')
      handleCancelar()
    } catch (error) {
      console.error(error)
      alert('Erro ao salvar cartas da coleção.')
    } finally {
      setSalvando(false)
    }
  }

  function cancelarSalvar() {
    if (salvando) return
    setModalSalvarAberto(false)
  }

  function handleCancelar() {
    if (salvando) return

    setCartas([])
    setFiltro('')
    setLinkColecao('')
    setDataCompra('')
    setValorPagoPadrao('')
    setQualidadePadrao('')
  }

  return (
    <div className="app-shell">
      <Topbar pageTitle="Cadastrar cartas por coleção" />

      <main className="form-page-content">
        <section className="form-page-left" style={{ maxWidth: '100%' }}>
          <h2 className="section-title section-title-with-help">
            Cadastro em lote por coleção
            <PageHelpButton
              configKey="cartas.cadastrarColecao"
              fallbackTitle="Como cadastrar cartas por colecao"
            />
          </h2>
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

            <FormField
              label="Valor pago padrão"
              name="valorPagoPadrao"
              kind="numero"
              value={valorPagoPadrao}
              onChange={setValorPagoPadrao}
              placeholder="Valor inicial para todas as cartas"
            />

            <FormSelect
              label="Qualidade padrão"
              name="qualidadePadrao"
              value={qualidadePadrao}
              onChange={setQualidadePadrao}
              options={opcoesQualidade}
              placeholder="Selecione a qualidade padrão"
            />
          </div>

          {!carregando && cartas.length > 0 && (
            <div
              className="form-actions"
              style={{
                justifyContent: 'flex-start',
                marginTop: '0.5rem',
                flexWrap: 'wrap',
              }}
            >
              <Button
                type="button"
                variant="outline"
                onClick={aplicarValorPagoPadraoNasSelecionadas}
                disabled={!valorPagoPadrao.trim() || salvando}
              >
                Aplicar valor padrão nas selecionadas
              </Button>

              <Button
                type="button"
                variant="outline"
                onClick={aplicarQualidadePadraoNasSelecionadas}
                disabled={!qualidadePadrao.trim() || salvando}
              >
                Aplicar qualidade padrão nas selecionadas
              </Button>
            </div>
          )}

          {carregando && (
            <div style={{ marginTop: '1.5rem' }}>
              <Loading message="Buscando cartas da coleção..." />
            </div>
          )}

          {!carregando && cartas.length > 0 && (
            <>
              <div
                className="form-actions"
                style={{
                  justifyContent: 'flex-start',
                  marginTop: '1rem',
                  flexWrap: 'wrap',
                }}
              >
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
                  onClick={() => selecionarTodas(true)}
                  disabled={salvando}
                >
                  Selecionar todas
                </Button>

                <Button
                  type="button"
                  variant="outline"
                  onClick={() => selecionarTodas(false)}
                  disabled={salvando}
                >
                  Desmarcar todas
                </Button>
              </div>

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
              variant="outline"
              onClick={handleCancelar}
              disabled={carregando || salvando}
            >
              Cancelar
            </Button>
          </div>
        </section>
      </main>

      {modalSalvarAberto && (
        <div className="confirm-modal-backdrop">
          <div className="confirm-modal-card">
            <h3 className="confirm-modal-title">Confirmar cadastro</h3>
            <p className="confirm-modal-text">
              Deseja realmente cadastrar as cartas selecionadas desta coleção?
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

      <Footer />
    </div>
  )
}
