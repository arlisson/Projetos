// src/views/Cartas/ListarCartas.tsx
import { useEffect, useState } from 'react'
import { Topbar } from '../../components/topBar'
import { Footer } from '../../components/footer'
import { DataTable, type Column } from '../../components/dataTable'
import {   
    buscarTodosProdutos,
  buscarProdutosPorFiltro,
  type ProdutoDetalhado,
} from '../../Database/db'
import { Financeiro } from '../../components/financeiro'



export function ListarProdutos() {
  const [produtos, setProdutos] = useState<ProdutoDetalhado []>([])
  const [busca, setBusca] = useState('')

  
  

  // Carrega e filtra ao digitar (com debounce simples)
  useEffect(() => {
    let cancelado = false
    const timeout = setTimeout(async () => {
      let resultado: ProdutoDetalhado[]
      if (busca.trim() === '') {
        resultado = await buscarTodosProdutos()
      } else {
        resultado = await buscarProdutosPorFiltro(busca)
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

  // Colunas da tabela
  const columns: Column<ProdutoDetalhado>[] = [
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
    {
    key: 'lucro_unitario',
    label: 'Lucro unit.',
    width: '110px',
    sum: true, // normalmente não faz sentido somar lucro unitário
    valueGetter: (row) => {
      const compra = row.preco_compra ?? 0
      const atual = row.preco_atual ?? 0
      return atual - compra
    },
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
      const atual = row.preco_atual ?? 0
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
                value="R$ 0,00"
                footer="Soma de todos os valores investidos em produtos."
              />
              <Financeiro
                label="Lucro em produtos"
                value="R$ 0,00"
                footer="Considerando apenas operações com produtos."
              />                    
              </div>                   
        </section>
        
        <section className="section-block">
          <div className="section-header">
            <h2 className="section-title">Produtos cadastrados</h2>
            <span className="section-header-caption">
              Consulte e filtre os produtos já cadastrados no sistema.
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
