import { Topbar } from '../components/topBar'
import { Financeiro } from '../components/financeiro'
import { Grafico } from '../components/grafico' 
import { CarrosselItem } from '../components/carrosselItem'
import  { Footer } from '../components/footer'


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
              label="Total gasto Cartas"
              value="R$ 0,00"
              footer="Soma de todos os valores investidos em cartas."
            />
            <Financeiro
              label="Lucro em cartas"
              value="R$ 0,00"
              footer="Considerando apenas operações com cartas."
            />
            <Financeiro
              label="Total gasto Produtos"
              value="R$ 0,00"
              footer='Considerando apenas operações com Produtos'
            />
            </div>
            <div className="summary-grid">
            <Financeiro
              label="Lucro em produtos"
              value="R$ 0,00"
              footer="Considerando apenas operações com produtos."
            />
            <Financeiro
              label="Total gasto (cartas + produtos)"
              value="R$ 0,00"
              footer="Soma do total gasto em cartas e produtos."
            />
            <Financeiro
              label="Lucro total"
              value="R$ 0,00"
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

        {/* 3) HISTÓRICO DE PREÇOS – GRÁFICOS EMPILHADOS EM LARGURA TOTAL */}
        <section className="section-block">
          <div className="section-header">
            <h2 className="section-title">Histórico de preços</h2>
            <span className="section-header-caption">
              Gráficos de cartas, produtos e total, um abaixo do outro.
            </span>
          </div>

          <div className="chart-stack">
            <Grafico
              title="Cartas"
              placeholderText="Gráfico de histórico de preços das cartas"
            />
            <Grafico
              title="Produtos"
              placeholderText="Gráfico de histórico de preços dos produtos"
            />
            <Grafico
              title="Total (cartas + produtos)"
              placeholderText="Gráfico consolidado de histórico de preços"
            />
          </div>
        </section>
      </main>
      <Footer />
    </div>
  )
}
