import { Topbar } from '../components/topBar'
import { Financeiro } from '../components/financeiro'
import { Grafico } from '../components/grafico' 
import { CarrosselItem } from '../components/carrosselItem'
import  { Footer } from '../components/footer'
import { buscarHistoricoPrecos,
  calculaTotalGasto,  
  type HistoricoLucro,
  type ResumoLucro,
  buscarTodasCartas,
  buscarTodosProdutos } from '../Database/db'
import { useEffect, useState } from 'react'


// Dados estáticos de exemplo para o carrossel
const destaqueItems = [
  {
    name: 'Nome da carta de exemplo',
    kind: 'Carta' as const,
    currentPrice: 'R$ 0,00',
    maxPrice: 'R$ 0,00',
    minPrice: 'R$ 0,00',
  },
  {
    name: 'Nome do produto de exemplo',
    kind: 'Produto' as const,
    currentPrice: 'R$ 0,00',
    maxPrice: 'R$ 0,00',
    minPrice: 'R$ 0,00',
  },
  {
    name: 'Outro item em destaque',
    kind: 'Carta' as const,
    currentPrice: 'R$ 0,00',
    maxPrice: 'R$ 0,00',
    minPrice: 'R$ 0,00',
  },
]



export function Main() {

  
  const [historicoLucro, setHistoricoLucro] = useState<HistoricoLucro[]>([])
  const [resumoLucro, setResumoLucro] = useState<ResumoLucro | null>(null)
  const [total_gasto, setTotalGasto] = useState<number>(0)
  const [totalGastoCartas, setTotalGastoCartas] = useState<number>(0)
  const [totalGastoProdutos, setTotalGastoProdutos] = useState<number>(0)
  const [quantidadeCartas, setQuantidadeCartas] = useState<number>(0)
  const [quantidadeProdutos, setQuantidadeProdutos] = useState<number>(0)

  const {
  lucro_cartas = 0,
  lucro_produtos = 0,
  total_vendas_cartas = 0,
  total_vendas_produtos = 0,
  lucro_total = 0,
} = resumoLucro ?? {}

  useEffect(() => {
    async function carregarDados() {

      // 1) Resumo (objeto único)
      const resumo = (await buscarHistoricoPrecos(undefined, undefined, true
        )) as ResumoLucro
      setResumoLucro(resumo)
      
      // 2) Histórico de lucro (array)
      const histLucro = (await buscarHistoricoPrecos(
        'lucro',
      )) as HistoricoLucro[]
      setHistoricoLucro(histLucro)
      
     
    
      const totalGasto = await calculaTotalGasto()
      setTotalGasto(totalGasto.totalGasto)

      const gastoCartas = totalGasto.gastoCartasEstoque + totalGasto.gastoCartasVendidas
      setTotalGastoCartas(gastoCartas)

      const gastoProdutos = totalGasto.gastoProdutosEstoque + totalGasto.gastoProdutosVendidos
      setTotalGastoProdutos(gastoProdutos)

      const quantidadeC = await buscarTodasCartas()   
      setQuantidadeCartas(quantidadeC.length)

      const quantidadeP = await buscarTodosProdutos()
      setQuantidadeProdutos(quantidadeP.length)
      
    }

    carregarDados()
    
    
  }, [])


  return (
    <div className="app-shell">
      {/* HEADER / MENU SUPERIOR COMPONENTIZADO */}
      <Topbar pageTitle="Painel inicial" />

      {/* CONTEÚDO PRINCIPAL */}
      <main className="dashboard-content">
        {/* 1) CARROSSEL LOGO ABAIXO DO HEADER */}
        <section className="carousel-wrapper">
          <div className="section-header">
            <h2 className="section-title">Cartas e produtos em destaque</h2>
            <span className="section-header-caption">
              Componente estático. Os itens reais virão do banco de dados.
            </span>
          </div>

          <div className="carousel-track">
            {destaqueItems.map((item) => (
              <CarrosselItem
                key={item.name}
                name={item.name}
                kind={item.kind}
                currentPrice={item.currentPrice}
                maxPrice={item.maxPrice}
                minPrice={item.minPrice}
              />
            ))}
          </div>
        </section>

        {/* 2) DADOS FINANCEIROS (LUCROS NO TOPO) */}
        <section className="section-block">
          <h2 className="section-title">Dados financeiros</h2>
          <p className="section-subtitle">
            Valores referentes a cartas e produtos: total gasto, lucros
            separados e lucro total. (Apenas layout; dados reais virão do banco.)
          </p>

           <div className="summary-grid">
           <Financeiro
              label="Total gasto (cartas + produtos)"
              value={total_gasto}
              footer="Soma do total gasto em cartas e produtos."
            />        
          </div>

          <div className="summary-grid">
            <Financeiro
              label="Total gasto Cartas"
              value={totalGastoCartas}
              footer="Soma de todos os valores investidos em cartas."
            />
            <Financeiro
              label="Lucro em cartas"
              value={lucro_cartas+total_vendas_cartas}
              isCurrency
              footer="Considerando apenas operações com cartas."
            />
            <Financeiro
              label="Total Cartas Cadastradas"
              value={quantidadeCartas}
              footer='Total unitário de cartas cadastradas no sistema.'
              isCurrency={false}
            />
            </div>
            <div className="summary-grid">
            <Financeiro
              label="Total gasto Produtos"
              value={totalGastoProdutos}
              footer='Considerando apenas operações com Produtos'
            />
            <Financeiro
              label="Lucro em produtos"
              value={lucro_produtos+total_vendas_produtos}
              footer="Considerando apenas operações com produtos."
            />
            <Financeiro
              label="Total Produtos Cadastrados"
              value={quantidadeProdutos}
              footer='Total unitário de produtos cadastrados no sistema.'
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
         


          {/* Banner sobre atualização automática via scraping */}
          <div className="info-banner">
            <div>
              <div className="info-banner-title">
                Atualização automática de preços (scraping)
              </div>
              <div className="info-banner-text">
                Ao iniciar o sistema, os preços de cartas e produtos serão
                atualizados via scraping. (Funcionalidade ainda não implementada.)
              </div>
            </div>
            <div className="info-banner-text">
              Status: <strong>não implementado</strong>
            </div>
          </div>
        </section>

        {/* 3) HISTÓRICO DE LUCROS – GRÁFICOS EMPILHADOS EM LARGURA TOTAL */}
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
              series={[
                { key: 'lucro_total', label: 'Lucro total' },
              ]}
            />

            {/* Lucro apenas de cartas */}
            <Grafico
              title="Lucro em cartas"
              data={historicoLucro}
              dateKey="data"
              series={[
                { key: 'lucro_cartas', label: 'Lucro cartas' },
              ]}
            />

            {/* Lucro apenas de produtos */}
            <Grafico
              title="Lucro em produtos"
              data={historicoLucro}
              dateKey="data"
              series={[
                { key: 'lucro_produtos', label: 'Lucro produtos' },
              ]}
            />    
          </div>
        </section>
      </main>
      <Footer />
    </div>
  )
}
