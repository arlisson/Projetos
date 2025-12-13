// src/views/Cartas/ListarCartas.tsx
import { useEffect, useState } from 'react'
import { Topbar } from '../../components/topBar'
import { Footer } from '../../components/footer'
import { DataTable, type Column } from '../../components/dataTable'
import {   
  listarVendasProdutos,
    buscarVendasProdutosPorFiltro,
  type VendaProdutoDetalhado,
  type ResumoLucro,
  calculaTotalGasto,  
  buscarHistoricoPrecos,
  type TotalGastoResult,
  
} from '../../Database/db'
import { Financeiro } from '../../components/financeiro'



export function ListarVendasProdutos() {
  const [produtos, setProdutos] = useState<VendaProdutoDetalhado[]>([])
  const [busca, setBusca] = useState('')
  const [totalGastoProdutos, setTotalGastoProdutos] = useState<number|TotalGastoResult>(0)  
  const [resumoLucro, setResumoLucro] = useState<ResumoLucro | null>(null)
  

  const {
    lucro_produtos = 0,
    total_vendas_produtos = 0,
  } = resumoLucro ?? {}
  
  const{       
      gastoProdutosEstoque = 0,
      gastoProdutosVendidos = 0,      
    } = (typeof totalGastoProdutos === 'object' ? totalGastoProdutos : {}) ?? {}
  
  

  // Carrega e filtra ao digitar (com debounce simples)
  useEffect(() => {
    let cancelado = false
    const timeout = setTimeout(async () => {
      let resultado: VendaProdutoDetalhado[]
      if (busca.trim() === '') {
        resultado = await listarVendasProdutos()
      } else {
        resultado = await buscarVendasProdutosPorFiltro(busca)
      }
      if (!cancelado) {
        setProdutos(resultado)
      }
    }, 300) // 300ms de debounce

    return () => {
      cancelado = true
      clearTimeout(timeout)
    }


  }, [busca])

  useEffect(() => {
      async function carregarTotal() {
        const totalGasto = await calculaTotalGasto()
        setTotalGastoProdutos(totalGasto)      
  
        // Carregar resumo de lucro
        const resumo = (await buscarHistoricoPrecos(undefined, undefined, true
                )) as ResumoLucro
              setResumoLucro(resumo)
        
        
      }
      carregarTotal()
    }, [])

  // Colunas da tabela
  const columns: Column<VendaProdutoDetalhado>[] = [
    {
      key: 'imagem',
      label: 'Produto',
      width: '170px',
      render: (_value, row) => {
        const imgSrc = row.imagem ?? '' // depois você pode tratar imagem_salva/local
        return (
          <div className="card-table-cell">
            <div className="card-table-name">{row.nome_produto}</div>
            <div className="card-table-image-wrapper">
              {imgSrc ? (
                <img
                  src={imgSrc}
                  alt={row.nome_produto}
                  className="card-table-image"
                />
              ) : (
                <div className="card-table-image-placeholder">
                  Sem imagem
                </div>
              )}
            </div>           
          </div>
        )
      },
    },
    
    {
      key: 'preco_compra',
      label: 'Preço pago',
      width: '110px',
      sum: true,
      formatSum: (sum) => `R$ ${sum.toFixed(2)}`,
      render: (value) =>
        value != null ? `R$ ${Number(value).toFixed(2)}` : '—',
    },
    {
      key: 'preco_atual',
      label: 'Preço atual',
      width: '110px',
      sum: true,
      formatSum: (sum) => `R$ ${sum.toFixed(2)}`,
      render: (value) =>
        value != null ? `R$ ${Number(value).toFixed(2)}` : '—',
    },
    {key:'preco_venda', label:'Preço de venda', width:'110px',
    sum: true,
    formatSum: (sum) => `R$ ${sum.toFixed(2)}`,
    render: (value) =>
      value != null ? `R$ ${Number(value).toFixed(2)}` : '—',
  },
    {
    key: 'lucro_unitario',
    label: 'Lucro unit.',
    width: '110px',
    sum: true, // normalmente não faz sentido somar lucro unitário
    valueGetter: (row) => {
      const compra = row.preco_compra ?? 0
      const atual = row.preco_venda ?? 0
      return atual - compra
    },
      formatSum: (sum) => `R$ ${sum.toFixed(2)}`,
    render: (value) =>
      value != null ? `R$ ${Number(value).toFixed(2)}` : '—',
  },

  // LUCRO TOTAL = (preco_atual - preco_compra) * quantidade
  {
    key: 'lucro_total',
    label: 'Lucro total',
    width: '120px',
    sum: true, // aqui queremos somar na linha de totais
    valueGetter: (row) => {
      const compra = row.preco_compra ?? 0
      const atual = row.preco_venda ?? 0
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
    { key: 'data_compra', label: 'Data da compra', width: '130px' },
    {key:'data_venda', label:'Data da venda', width:'130px' },
    {key:'data_scraping', label:'Data do scraping', width:'130px' }
  ]

  return (
    <div className="app-shell">
      <Topbar pageTitle="Listar produtos" />

      <main className="dashboard-content">
        {/* 2) DADOS FINANCEIROS (LUCROS NO TOPO) */}
          <section className="section-block">
            <h2 className="section-title">Dados financeiros</h2>
            <p className="section-subtitle">
              Valores referentes a produtos: total gasto, lucros
              separados e lucro total. (Apenas layout; dados reais virão do banco.)
            </p>
  
            <div className="summary-grid">
              <Financeiro
                label="Total gasto Produtos"
                value={gastoProdutosEstoque + gastoProdutosVendidos}
                footer="Soma de todos os valores investidos em produtos."
              />
              <Financeiro
                label="Lucro em vendas de produtos"
                value={lucro_produtos + total_vendas_produtos}
                footer="Considerando apenas operações com produtos."
              />                    
              </div> 
               <div className="summary-grid">
              <Financeiro
                label="Valor vendidos em produtos"
                value={total_vendas_produtos}
                footer="Valor total de produtos vendidos."
              />
              <Financeiro
                label="Total Produtos Vendidos"
                value={produtos.length}
                footer="Total de produtos vendidos no sistema."
                isCurrency={false}
              />                    
              </div>                   
                     
        </section>
        
        <section className="section-block">
          <div className="section-header">
            <h2 className="section-title">Produtos vendidos</h2>
            <span className="section-header-caption">
              Consulte e filtre os produtos já vendidos no sistema.
            </span>
          </div>

          <div className="table-toolbar">
            <input
              className="search-input"
              type="text"
              placeholder="Buscar por nome"
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
            />
          </div>

          <DataTable
            columns={columns}
            data={produtos}
            rowKey="id_produto"
          />
        </section>
      </main>

      <Footer appName="YU-GI-OH! Manager" />
    </div>
  )
}
