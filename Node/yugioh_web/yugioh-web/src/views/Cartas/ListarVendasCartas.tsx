// src/views/Cartas/ListarCartas.tsx
import { useEffect, useState } from 'react'
import { Topbar } from '../../components/topBar'
import { Footer } from '../../components/footer'
import { DataTable, type Column } from '../../components/dataTable'
import {
   
  type ResumoLucro,
  type VendaCartaDetalhada,  
  buscarHistoricoPrecos,  
  buscarVendasCartasPorFiltro,
  calculaTotalGasto,
  listarVendasCartas,
  calcularLucroTotalCartasVendidas
} from '../../Database/db'
import { Financeiro } from '../../components/financeiro'
import { useNavigate } from 'react-router-dom'



export function ListarVendasCartas() {
  const [cartas, setCartas] = useState<VendaCartaDetalhada[]>([])
  const [busca, setBusca] = useState('')
  const [totalGastoCartas, setTotalGastoCartas] = useState<number>(0)  
  const [resumoLucro, setResumoLucro] = useState<ResumoLucro | null>(null)
  const [lucroTotalCartasVendidas, setLucroTotalCartasVendidas] = useState<number>(0)
  const navigate = useNavigate()
  
  

  // Carrega e filtra ao digitar (com debounce simples)
  useEffect(() => {
    let cancelado = false
    const timeout = setTimeout(async () => {
      let resultado: VendaCartaDetalhada[]
      if (busca.trim() === '') {
        resultado = await listarVendasCartas()
      } else {
        resultado = await buscarVendasCartasPorFiltro(busca)
      }
      if (!cancelado) {
        setCartas(resultado)
      }
    }, 300) // 300ms de debounce

    return () => {
      cancelado = true
      clearTimeout(timeout)
    }


  }, [busca])

  useEffect(() => {
    async function carregarResumo() {
      const resumo = (await buscarHistoricoPrecos(undefined, undefined, true
              )) as ResumoLucro
            setResumoLucro(resumo)
      const totalGasto = await calculaTotalGasto()
          
            
      const gastoCartas = totalGasto.gastoCartasEstoque + totalGasto.gastoCartasVendidas
      setTotalGastoCartas(gastoCartas)     
      
      const lucroTotal = await calcularLucroTotalCartasVendidas()
      setLucroTotalCartasVendidas(lucroTotal)
    } 
    carregarResumo()
  }, [])

  const {
    
    total_vendas_cartas = 0,    
  } = resumoLucro ?? {}

  // Colunas da tabela
  const columns: Column<VendaCartaDetalhada>[] = [
    {
      key: 'imagem',
      label: 'Carta',
      width: '170px',
      render: (_value, row) => {
        const imgSrc = row.imagem ?? '' // depois você pode tratar imagem_salva/local
        return (
          <div className="card-table-cell">
            <div className="card-table-name">{row.nome}</div>
            <div className="card-table-image-wrapper">
              {imgSrc ? (
                <img
                  src={imgSrc}
                  alt={row.nome}
                  className="card-table-image"
                />
              ) : (
                <div className="card-table-image-placeholder">
                  Sem imagem
                </div>
              )}
            </div>
            <div className="card-table-rarity">
              {row.raridade_nome || '—'}
            </div>
          </div>
        )
      },
    },
    { key: 'codigo', label: 'Código', width: '110px' },
    { key: 'colecao_nome', label: 'Coleção', width: '140px' },
    {
      key: 'preco_da_compra',
      label: 'Preço pago',
      width: '110px',
      sum: true,
      formatSum: (sum) => `R$ ${sum.toFixed(2)}`,
      render: (value) =>
        value != null ? `R$ ${Number(value).toFixed(2)}` : '—',
    },
    {
      key: 'preco_da_venda',
      label: 'Preço da venda',
      width: '110px',
      sum: true,
      formatSum: (sum) => `R$ ${sum.toFixed(2)}`,
      render: (value) =>
            value != null ? `R$ ${Number(value).toFixed(2)}` : '—',
        },
    {key:'preco_atual', label:'Preço atual', width:'110px',
    render:(value) =>
      value != null ? `R$ ${Number(value).toFixed(2)}` : '—',
    sum: true,
    formatSum: (sum) => `R$ ${sum.toFixed(2)}`
    },
    {
    key: 'lucro_unitario',
    label: 'Lucro unit.',
    width: '110px',
    sum: true, // normalmente não faz sentido somar lucro unitário
    valueGetter: (row) => {
      const compra = row.preco_da_compra ?? 0
      const atual = row.preco_da_venda ?? 0
      return atual - compra
    },
      formatSum: (sum) => `R$ ${sum.toFixed(2)}`,
    render: (value) =>
      value != null ? `R$ ${Number(value).toFixed(2)}` : '—',
  },

  // LUCRO TOTAL = (preco_atual - preco_da_compra) * quantidade
  {
    key: 'lucro_total',
    label: 'Lucro total',
    width: '120px',
    sum: true, // aqui queremos somar na linha de totais
    valueGetter: (row) => {
      const compra = row.preco_da_compra ?? 0
      const atual = row.preco_da_venda ?? 0
      const qtd = row.quantidade ?? 0
      return (atual - compra) * qtd
    },
    formatSum: (sum) => `R$ ${sum.toFixed(2)}`,
    render: (value) =>
      value != null ? `R$ ${Number(value).toFixed(2)}` : '—',
  },
    {
      key: 'quantidade',
      label: 'Qtd.',
      width: '80px',
      sum: true,
      formatSum: (sum) => sum.toString(),
    },
    { key: 'data_da_compra', label: 'Data da compra', width: '130px' },
    { key: 'data_da_venda', label: 'Data da venda', width: '130px' },
    {key:'data_scraping', label:'Data do scraping', width:'130px' }
  ]

  return (
    <div className="app-shell">
      <Topbar pageTitle="Listar cartas" />

      <main className="dashboard-content">
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
                value={totalGastoCartas}
                footer="Soma de todos os valores investidos em cartas."
              />
              <Financeiro
                label="Total Cartas Vendidas"
                value={cartas.length}
                footer="Total unitário de cartas vendidas no sistema."
                isCurrency={false}
              />                             
              </div>    
              <div className="summary-grid">
                <Financeiro
                  label="Valor total Cartas vendidas"
                  value={total_vendas_cartas}
                  footer="Soma do total gasto em cartas e produtos."
                />     
                <Financeiro
                label="Lucro em vendas de cartas"
                value={lucroTotalCartasVendidas}
                footer="Considerando apenas operações com cartas."
              />       

              </div>
                                         
        </section>
        
        <section className="section-block">
          <div className="section-header">
            <h2 className="section-title">Cartas vendidas</h2>
            <span className="section-header-caption">
              Consulte e filtre as cartas já vendidas no sistema.
            </span>
          </div>

          <div className="table-toolbar">
            <input
              className="search-input"
              type="text"
              placeholder="Buscar por nome, código, coleção ou raridade..."
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
            />
          </div>

          <DataTable
            columns={columns}
            data={cartas}
            rowKey="id_carta"
            onRowClick={(row) => {
              navigate(`/cartas/vendas/editar?id=${row.id_carta}`)
            }}
          />
        </section>
      </main>

      <Footer appName="YU-GI-OH! Manager" />
    </div>
  )
}
