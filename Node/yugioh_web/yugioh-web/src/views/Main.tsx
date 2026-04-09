import { useEffect, useRef, useState } from 'react'
import { Topbar } from '../components/topBar'
import { Financeiro } from '../components/financeiro'
import { Grafico } from '../components/grafico'
import { CarrosselItem } from '../components/carrosselItem'
import { Footer } from '../components/footer'
import {
  buscarHistoricoPrecos,
  calculaTotalGasto,
  type HistoricoLucro,
  type ResumoLucro,
  buscarTodasCartas,
  buscarTodosProdutos,
  precoMaximoMinimo,
} from '../Database/db'
import {
  iniciarAtualizacaoDiaria,
  getDailyUpdateStatus,
  subscribeDailyUpdateStatus,
  type DailyUpdateStatus,
} from '../services/dailyPriceUpdate'

type ItemKind = 'Carta' | 'Produto'

type DestaqueItem = {
  id: string | number
  name: string
  kind: ItemKind
  imageUrl?: string | null
  currentPrice: string
  maxPrice: string
  minPrice: string
  rarity?: string
}

function formatBRL(value: number) {
  return value.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  })
}

export function Main() {
  const ITEM_W = 260
  const GAP_PX = 14
  const INTERVAL_MS = 2500

  const [index, setIndex] = useState(0)
  const [paused, setPaused] = useState(false)

  const [historicoLucro, setHistoricoLucro] = useState<HistoricoLucro[]>([])
  const [resumoLucro, setResumoLucro] = useState<ResumoLucro | null>(null)
  const [total_gasto, setTotalGasto] = useState<number>(0)
  const [totalGastoCartas, setTotalGastoCartas] = useState<number>(0)
  const [totalGastoProdutos, setTotalGastoProdutos] = useState<number>(0)
  const [quantidadeCartas, setQuantidadeCartas] = useState<number>(0)
  const [quantidadeProdutos, setQuantidadeProdutos] = useState<number>(0)
  const [destaqueItems, setDestaqueItems] = useState<DestaqueItem[]>([])

  const [updateStatus, setUpdateStatus] = useState<DailyUpdateStatus>(
    getDailyUpdateStatus(),
  )

  const updateStartedRef = useRef(false)

  const {
    lucro_cartas = 0,
    lucro_produtos = 0,
    total_vendas_cartas = 0,
    total_vendas_produtos = 0,
    lucro_total = 0,
  } = resumoLucro ?? {}

  async function carregarDashboard() {
    const resumo = (await buscarHistoricoPrecos(
      undefined,
      undefined,
      true,
    )) as ResumoLucro
    setResumoLucro(resumo)

    const histLucro = (await buscarHistoricoPrecos(
      'lucro',
    )) as HistoricoLucro[]
    setHistoricoLucro(histLucro)

    const totalGasto = await calculaTotalGasto()
    setTotalGasto(totalGasto.totalGasto)

    const gastoCartas =
      totalGasto.gastoCartasEstoque + totalGasto.gastoCartasVendidas
    setTotalGastoCartas(gastoCartas)

    const gastoProdutos =
      totalGasto.gastoProdutosEstoque + totalGasto.gastoProdutosVendidos
    setTotalGastoProdutos(gastoProdutos)

    const cartas = await buscarTodasCartas()
    setQuantidadeCartas(cartas.length)

    const produtos = await buscarTodosProdutos()
    setQuantidadeProdutos(produtos.length)

    const cartasMap = await Promise.all(
      cartas.map(async (c: any) => {
        const { preco_maximo, preco_minimo } = await precoMaximoMinimo(
          'carta',
          c.id_carta,
        )

        const atual = Number(c.preco_atual ?? 0)
        const max = preco_maximo ?? atual
        const min = preco_minimo ?? atual

        return {
          id: c.id_carta,
          name: c.nome,
          kind: 'Carta' as const,
          imageUrl: c.imagem,
          currentPrice: formatBRL(atual),
          maxPrice: formatBRL(max),
          minPrice: formatBRL(min),
          rarity: c.raridade_nome,
        }
      }),
    )

    const produtosMap = await Promise.all(
      produtos.map(async (p: any) => {
        const { preco_maximo, preco_minimo } = await precoMaximoMinimo(
          'produto',
          p.id_produto,
        )

        const atual = Number(p.preco_atual ?? p.preco ?? 0)
        const max = preco_maximo ?? atual
        const min = preco_minimo ?? atual

        return {
          id: p.id_produto,
          name: p.nome_produto,
          kind: 'Produto' as const,
          imageUrl: p.imagem,
          currentPrice: formatBRL(atual),
          maxPrice: formatBRL(max),
          minPrice: formatBRL(min),
        }
      }),
    )

    const top = [...cartasMap, ...produtosMap].sort((a, b) => {
      const pa =
        Number(
          String(a.currentPrice).replace(/[^\d,]/g, '').replace(',', '.'),
        ) || 0
      const pb =
        Number(
          String(b.currentPrice).replace(/[^\d,]/g, '').replace(',', '.'),
        ) || 0
      return pb - pa
    })

    setDestaqueItems(top)
  }

  useEffect(() => {
    void carregarDashboard()
  }, [])

  useEffect(() => {
    const unsubscribe = subscribeDailyUpdateStatus((status) => {
      setUpdateStatus(status)
    })

    return unsubscribe
  }, [])

  useEffect(() => {
    if (updateStartedRef.current) return
    updateStartedRef.current = true

    async function iniciar() {
      const statusAntes = getDailyUpdateStatus()
      const estavaExecutando = statusAntes.executando

      const resultado = await iniciarAtualizacaoDiaria()

      if (!estavaExecutando && resultado.etapa === 'finalizado') {
        await carregarDashboard()
      }
    }

    void iniciar()
  }, [])

  useEffect(() => {
    if (!updateStatus.executando && updateStatus.etapa === 'finalizado') {
      void carregarDashboard()
    }
  }, [updateStatus.executando, updateStatus.etapa])

  useEffect(() => {
    if (destaqueItems.length <= 1) return

    const t = window.setInterval(() => {
      if (paused) return
      setIndex((prev) => (prev + 1) % destaqueItems.length)
    }, INTERVAL_MS)

    return () => window.clearInterval(t)
  }, [paused, destaqueItems.length])

  return (
    <div className="app-shell">
      <Topbar pageTitle="Painel inicial" />

      <main className="dashboard-content">
        <section className="carousel-wrapper">
          <div className="section-header">
            <h2 className="section-title">Cartas e produtos em destaque</h2>
            <span className="section-header-caption">
              Itens com base nos maiores preços atuais cadastrados.
            </span>
          </div>

          <div
            className="carousel-viewport"
            onMouseEnter={() => setPaused(true)}
            onMouseLeave={() => setPaused(false)}
          >
            <div
              className="carousel-track"
              style={{
                transform: `translateX(-${index * (ITEM_W + GAP_PX)}px)`,
              }}
            >
              {destaqueItems.map((item) => (
                <div key={`${item.kind}-${item.id}`} className="carousel-slide">
                  <CarrosselItem
                    name={item.name}
                    kind={item.kind}
                    imageUrl={item.imageUrl || null}
                    currentPrice={item.currentPrice}
                    maxPrice={item.maxPrice}
                    minPrice={item.minPrice}
                    rarity={item.kind === 'Carta' ? item.rarity : undefined}
                  />
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="section-block">
          <h2 className="section-title">Dados financeiros</h2>
          <p className="section-subtitle">
            Valores referentes a cartas e produtos cadastrados, vendas e lucro
            consolidado.
          </p>

          <div className="summary-grid">
            <Financeiro
              label="Total gasto geral"
              value={total_gasto}
              footer="Soma do valor investido em cartas e produtos."
            />
            <Financeiro
              label="Total gasto Cartas"
              value={totalGastoCartas}
              footer="Considerando apenas operações com cartas."
            />
            <Financeiro
              label="Lucro em cartas"
              value={lucro_cartas + total_vendas_cartas}
              isCurrency
              footer="Considerando apenas operações com cartas."
            />
            <Financeiro
              label="Total Cartas Cadastradas"
              value={quantidadeCartas}
              footer="Total unitário de cartas cadastradas no sistema."
              isCurrency={false}
            />
          </div>

          <div className="summary-grid">
            <Financeiro
              label="Total gasto Produtos"
              value={totalGastoProdutos}
              footer="Considerando apenas operações com produtos."
            />
            <Financeiro
              label="Lucro em produtos"
              value={lucro_produtos + total_vendas_produtos}
              footer="Considerando apenas operações com produtos."
            />
            <Financeiro
              label="Total Produtos Cadastrados"
              value={quantidadeProdutos}
              footer="Total unitário de produtos cadastrados no sistema."
              isCurrency={false}
            />
          </div>

          <div className="summary-grid">
            <Financeiro
              label="Vendas em Cartas"
              value={total_vendas_cartas}
              footer="Considerando apenas operações com cartas."
            />
            <Financeiro
              label="Vendas em Produtos"
              value={total_vendas_produtos}
              footer="Considerando apenas operações com produtos."
            />
            <Financeiro
              label="Lucro total"
              value={lucro_total}
              footer="Lucro combinado de cartas + produtos."
            />
          </div>

          <div className="info-banner info-banner-update">
            <div>
              <div className="info-banner-title">
                Atualização automática diária de preços
              </div>

              <div className="info-banner-text">{updateStatus.mensagem}</div>

              <div className="info-banner-text">
                Última atualização registrada:{' '}
                <strong>{updateStatus.ultimaAtualizacao || 'nenhuma'}</strong>
              </div>

              {(updateStatus.executando ||
                updateStatus.etapa === 'finalizado') && (
                <div className="update-progress-list">
                  <div className="info-banner-text">
                    Cartas: <strong>{updateStatus.cartasAtualizadas}</strong> /{' '}
                    {updateStatus.totalCartas}
                  </div>

                  <div className="info-banner-text">
                    Produtos: <strong>{updateStatus.produtosAtualizados}</strong> /{' '}
                    {updateStatus.totalProdutos}
                  </div>

                  {updateStatus.nomeItemAtual && (
                    <div className="info-banner-text">
                      Atualizando agora:{' '}
                      <strong>{updateStatus.nomeItemAtual}</strong>
                    </div>
                  )}

                  {updateStatus.executando && updateStatus.total > 0 && (
                    <div className="info-banner-text">
                      Progresso da etapa atual: <strong>{updateStatus.atual}</strong> /{' '}
                      {updateStatus.total}
                    </div>
                  )}
                </div>
              )}
            </div>

            <div className="info-banner-text">
              Status:{' '}
              <strong>
                {updateStatus.executando
                  ? 'em execução'
                  : updateStatus.etapa === 'finalizado'
                    ? 'concluído'
                    : updateStatus.etapa === 'erro'
                      ? 'erro'
                      : 'aguardando'}
              </strong>
            </div>
          </div>
        </section>

        <section className="section-block">
          <div className="section-header">
            <h2 className="section-title">Histórico de Lucros</h2>
            <span className="section-header-caption">
              Gráficos de cartas, produtos e total, um abaixo do outro.
            </span>
          </div>

          <div className="chart-stack">
            <Grafico
              title="Lucro total (cartas + produtos)"
              data={historicoLucro}
              dateKey="data"
              series={[{ key: 'lucro_total', label: 'Lucro total' }]}
            />

            <Grafico
              title="Lucro em cartas"
              data={historicoLucro}
              dateKey="data"
              series={[{ key: 'lucro_cartas', label: 'Lucro cartas' }]}
            />

            <Grafico
              title="Lucro em produtos"
              data={historicoLucro}
              dateKey="data"
              series={[{ key: 'lucro_produtos', label: 'Lucro produtos' }]}
            />
          </div>
        </section>
      </main>

      <Footer appName="YU-GI-OH! Manager" />
    </div>
  )
}