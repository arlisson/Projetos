// src/services/database.ts
import Database from '@tauri-apps/plugin-sql'
import { logError, logInfo } from '../services/logger'

// mesmo arquivo do Python: DB_PATH = "yugioh.db"
const DB_URL = 'sqlite:yugioh.db'


// data scraping no formato YYYY-MM-DD (mesmo do Python)
function todayStr(): string {
  return new Date().toISOString().slice(0, 10)
}

let dbPromise: Promise<Database> | null = null

async function getDb(): Promise<Database> {
  if (!dbPromise) {
    dbPromise = Database.load(DB_URL)
  }
  console.log('Conectado ao banco de dados.')
  return dbPromise
}


export async function testDbConnection(): Promise<{ ok: boolean; message: string }> {
  try {
    const db = await getDb()
    await db.select('SELECT 1 as value')

    await logInfo('Conexão com o banco de dados bem-sucedida.')
    return { ok: true, message: 'Conexão com o banco OK.' }
  } catch (err) {
    console.error('Erro ao conectar no banco:', err)
    await logError('Erro ao conectar no banco: ' + String(err))
    return { ok: false, message: String(err) }
  }
}

// ------------------------------------------
// Helpers genéricos
// ------------------------------------------

async function singleNumber(
  query: string,
  params: unknown[] = [],
): Promise<number> {
  const db = await getDb()
  const rows = await db.select<{ value: number | string | null }[]>(query, params)

  if (!rows.length) return 0

  const raw = rows[0]?.value ?? 0
  const num =
    typeof raw === 'number'
      ? raw
      : Number(raw)

  return Number.isNaN(num) ? 0 : num
}


// ------------------------------------------
// Tipos (cartas / produtos)
// ------------------------------------------

export interface InserirCartaPayload {
  link_site?: string | null
  nome: string
  colecao?: string | null
  codigo?: string | null
  preco_da_compra?: number | null
  data_da_compra?: string | null // "YYYY-MM-DD"
  raridade?: number | null       // id_raridade
  qualidade?: number | null      // id_qualidade
  quantidade?: number | null
  imagem?: string | null
  origem?: string | null
  preco_atual?: number | null
  imagem_salva?: string | null
}

export interface CartaDetalhada {
    raridade_nome: string
    id_carta: number    
    link_site?: string | null
    nome: string
    colecao?: string | null
    codigo?: string | null
    preco_da_compra?: number | null
    data_da_compra?: string | null // "YYYY-MM-DD"
    raridade?: number | null       // id_raridade
    qualidade?: number | null      // id_qualidade
    quantidade?: number | null
    imagem?: string | null
    origem?: string | null
    preco_atual?: number | null
    imagem_salva?: string | null
}

export interface InserirProdutoPayload {
  nome_produto: string
  link?: string | null
  imagem?: string | null
  preco_compra?: number | null
  data_compra?: string | null     // YYYY-MM-DD
  origem?: string | null
  preco_atual?: number | null
  quantidade?: number | null
  imagem_salva?: string | null
}

export interface ProdutoDetalhado {
    id_produto: number
    nome_produto: string
    link?: string | null
    imagem?: string | null
    preco_compra?: number | null
    data_compra?: string | null     // YYYY-MM-DD
    origem?: string | null
    preco_atual?: number | null
    quantidade?: number | null
    imagem_salva?: string | null
    data_scraping?: string | null
}

  export interface VendaCartaDetalhada {
    id_carta: number
    link_site?: string | null
    nome: string
    codigo?: string | null
    preco_da_compra?: number | null
    data_da_compra?: string | null
    preco_da_venda?: number | null
    data_da_venda?: string | null
    preco_atual?: number | null
    quantidade?: number | null
    imagem?: string | null
    imagem_salva?: string | null
    origem?: string | null
    data_scraping?: string | null
    colecao_nome?: string | null
    colecao_codigo?: string | null
    raridade_nome?: string | null
    qualidade_nome?: string | null
  }

  export interface VendaProdutoDetalhado {
    id_produto: number
    nome_produto: string
    link?: string | null
    imagem?: string | null
    preco_compra?: number | null
    data_compra?: string | null     // YYYY-MM-DD
    preco_venda?: number | null
    data_venda?: string | null
    preco_atual?: number | null
    quantidade?: number | null
    imagem_salva?: string | null
    origem?: string | null
    data_scraping?: string | null
  }

// ------------------------------------------
// Histórico genérico (tabela historico_precos)
// registrar_historico_generico do Python
// ------------------------------------------

export interface HistoricoGenericoParams {
  tipo: 'carta' | 'produto'
  id: number
  preco: number | null
  data: string // YYYY-MM-DD
  origem?: string
}

/**
 * Retorna todas as cartas da view vw_cartas_detalhadas.
 * Equivalente ao buscar_todas_cartas do Python.
 */
export async function buscarTodasCartas(): Promise<CartaDetalhada[]> {
  try {
    const db = await getDb()

    const rows = await db.select<CartaDetalhada[]>(
      'SELECT * FROM vw_cartas_detalhadas',
    )

    return rows
  } catch (err) {
    console.error('Erro ao buscar todas as cartas:', err)
    // Se quiser integrar com seu logger em Rust:
    await logError('Erro ao buscar todas as cartas: ' + String(err))
    return []
  }
}

/**
 * Busca com filtro de texto (nome, código, coleção, raridade).
 * Usado no "buscar ao digitar".
 */
export async function buscarCartasPorFiltro(
  filtro: string,
): Promise<CartaDetalhada[]> {
  const termo = filtro.trim()
  if (!termo) {
    return buscarTodasCartas()
  }

  try {
    const db = await getDb()
    const like = `%${termo.toUpperCase()}%`

    const rows = await db.select<CartaDetalhada[]>(
      `
      SELECT *
      FROM vw_cartas_detalhadas
      WHERE
        UPPER(nome) LIKE ?
        OR UPPER(codigo) LIKE ?
        OR UPPER(colecao_nome) LIKE ?
        OR UPPER(raridade_nome) LIKE ?
      ORDER BY id_carta DESC
    `,
      [like, like, like, like],
    )

    return rows
  } catch (err) {
    console.error('Erro ao buscar cartas com filtro:', err)
    await logError('Erro ao buscar cartas com filtro: ' + String(err))
    return []
  }
}

/**
 * Retorna todas as cartas da view vw_cartas_detalhadas.
 * Equivalente ao buscar_todas_cartas do Python.
 */
export async function buscarTodosProdutos(): Promise<ProdutoDetalhado[]> {
  try {
    const db = await getDb()

    const rows = await db.select<ProdutoDetalhado[]>(
      'SELECT * FROM vw_produtos_detalhados',
    )

    return rows
  } catch (err) {
    console.error('Erro ao buscar todos os produtos:', err)
    // Se quiser integrar com seu logger em Rust:
    await logError('Erro ao buscar todos os produtos: ' + String(err))
    return []
  }
}

/**
 * 
 * @param filtro 
 * @returns 
 */
export async function buscarProdutosPorFiltro(
  filtro: string,
): Promise<ProdutoDetalhado[]> {
  const termo = filtro.trim()
  if (!termo) {
    return buscarTodosProdutos()
  }  
  try {
    const db = await getDb()
    const like = `%${termo.toUpperCase()}%`
    const rows = await db.select<ProdutoDetalhado[]>(
      `
      SELECT *
      FROM vw_produtos_detalhados
      WHERE
        UPPER(nome_produto) LIKE ?
        OR UPPER(origem) LIKE ?
      ORDER BY id_produto DESC
    `,
      [like, like],
    )
    return rows
  } catch (err) {
    console.error('Erro ao buscar produtos com filtro:', err)
    await logError('Erro ao buscar produtos com filtro: ' + String(err))
    return []
  }
}

/**
 * 
 * @returns 
 */
export async function listarVendasCartas(): Promise<VendaCartaDetalhada[]> {
  try {
    const db = await getDb()  
    const rows = await db.select<VendaCartaDetalhada[]>(
      'SELECT * FROM vw_vendas_detalhadas',
    )  
    return rows
  } catch (err) {
    console.error('Erro ao buscar vendas de cartas:', err)
    await logError('Erro ao buscar vendas de cartas: ' + String(err))
    return []
  }
}

export async function buscarVendasCartasPorFiltro(
  filtro: string,
): Promise<VendaCartaDetalhada[]> {
  const termo = filtro.trim()
  if (!termo) {
    return listarVendasCartas()
  }
  try {
    const db = await getDb()
    const like = `%${termo.toUpperCase()}%`
    const rows = await db.select<VendaCartaDetalhada[]>(
      `
      SELECT *
      FROM vw_vendas_detalhadas
      WHERE
        UPPER(nome) LIKE ?
        OR UPPER(codigo) LIKE ?
        OR UPPER(origem) LIKE ?
        OR UPPER(colecao_nome) LIKE ?
        OR UPPER(raridade_nome) LIKE ?
        OR UPPER(qualidade_nome) LIKE ?
      ORDER BY id_carta DESC
    `,
      [like, like, like, like, like, like],
    )
    return rows
  }
    catch (err) {
    console.error('Erro ao buscar vendas de cartas com filtro:', err)
    await logError('Erro ao buscar vendas de cartas com filtro: ' + String(err))
    return []
  } 
}

export async function listarVendasProdutos(): Promise<VendaProdutoDetalhado[]> {
  try {
    const db = await getDb()  
    const rows = await db.select<VendaProdutoDetalhado[]>(
      'SELECT * FROM vw_venda_produto_detalhado',
    )  
    return rows
  } catch (err) {
    console.error('Erro ao buscar vendas de produtos:', err)
    await logError('Erro ao buscar vendas de produtos: ' + String(err))
    return []
  } 
}

export async function buscarVendasProdutosPorFiltro(
  filtro: string,
): Promise<VendaProdutoDetalhado[]> {
  const termo = filtro.trim()
  if (!termo) {
    return listarVendasProdutos()
  }
  try {
    const db = await getDb()
    const like = `%${termo.toUpperCase()}%`
    const rows = await db.select<VendaProdutoDetalhado[]>(
      `
      SELECT *
      FROM vw_venda_produto_detalhado
      WHERE
        UPPER(nome_produto) LIKE ?
        OR UPPER(origem) LIKE ?
      ORDER BY id_produto DESC
    `,
      [like, like],
    )
    return rows
  }
    catch (err) {
    console.error('Erro ao buscar vendas de produtos com filtro:', err)
    await logError('Erro ao buscar vendas de produtos com filtro: ' + String(err))
    return []
  }

}

// ------------------------------------------
// Histórico de Preços e Lucro
// ------------------------------------------

export interface HistoricoPrecos {
  id_historico_precos: number
  id_carta?: number | null
  id_produto?: number | null
  data: string
  preco: number | null
  origem?: string | null
}

export interface HistoricoLucro {
  id_lucro: number
  data: string
  lucro_cartas: number
  lucro_produtos: number
  lucro_total: number
}

export interface ResumoLucro {
  lucro_cartas: number
  lucro_produtos: number
  total_vendas_cartas: number
  total_vendas_produtos: number
  lucro_total: number
}

/**
 * Busca histórico de preços ou resumo de lucro.
 * Se resumo=true, retorna cálculo de lucro em posse.
 * Se tipo e id fornecidos, retorna histórico específico.
 * Caso contrário, retorna histórico geral.
 */
export async function buscarHistoricoPrecos(
  tipo?: 'carta' | 'produto' | 'lucro',
  id?: number,
  resumo: boolean = false,
): Promise<ResumoLucro | HistoricoPrecos[] | HistoricoLucro[]> {
  try {
    const db = await getDb()

    // =================== RESUMO (em posse) ===================
    if (resumo) {
      const lucroCarta = await singleNumber(`
        SELECT COALESCE(
                SUM(
                  (COALESCE(preco_atual, 0) - COALESCE(preco_da_compra, 0))
                  * COALESCE(quantidade, 0)
                ),
                0
              ) AS value
        FROM carta
        WHERE COALESCE(quantidade, 0) > 0
      `)

      const lucroProduto = await singleNumber(`
        SELECT COALESCE(
                SUM(
                  (COALESCE(preco_atual, 0) - COALESCE(preco_compra, 0))
                  * COALESCE(quantidade, 0)
                ),
                0
              ) AS value
        FROM produto
        WHERE COALESCE(quantidade, 0) > 0
      `)

      const totalVendasCartas = await singleNumber(`
        SELECT COALESCE(
                SUM(COALESCE(preco_da_venda, 0) * COALESCE(quantidade, 0)),
                0
              ) AS value
        FROM venda
      `)

      const totalVendasProdutos = await singleNumber(`
        SELECT COALESCE(
                SUM(COALESCE(preco_venda, 0) * COALESCE(quantidade, 0)),
                0
              ) AS value
        FROM venda_produto
      `)

      return {
        lucro_cartas: lucroCarta,
        lucro_produtos: lucroProduto,
        total_vendas_cartas: totalVendasCartas,
        total_vendas_produtos: totalVendasProdutos,
        lucro_total:
          lucroCarta + lucroProduto + totalVendasCartas + totalVendasProdutos,
      }
    }

    // =================== HISTÓRICO POR ID ===================
    if (tipo && id !== undefined) {
      if (tipo === 'carta') {
        const rows = await db.select<HistoricoPrecos[]>(
          `
          SELECT id_historico_precos, id_carta, data, preco, origem
          FROM historico_precos
          WHERE id_carta = ?
          ORDER BY data
        `,
          [id],
        )
        return rows
      } else if (tipo === 'produto') {
        const rows = await db.select<HistoricoPrecos[]>(
          `
          SELECT id_historico_precos, id_produto, data, preco, origem
          FROM historico_precos
          WHERE id_produto = ?
          ORDER BY data
        `,
          [id],
        )
        return rows
      } else {
        throw new Error("Tipo inválido. Use 'carta', 'produto' ou 'lucro'.")
      }
    }

    // =================== HISTÓRICO GERAL ===================
    if (tipo === 'lucro') {
      const rows = await db.select<HistoricoLucro[]>(
        `
        SELECT id_lucro, data, lucro_cartas, lucro_produtos, lucro_total
        FROM historico_lucro
        ORDER BY data
      `,
      )
      return rows
    } else {
      const rows = await db.select<HistoricoPrecos[]>(
        `
        SELECT id_historico_precos, id_carta, id_produto, data, preco, origem
        FROM historico_precos
        ORDER BY data
      `,
      )
      return rows
    }
  } catch (err) {
    console.error('Erro ao buscar histórico:', err)
    await logError('Erro ao buscar histórico: ' + String(err))
    return []
  }
}

export interface TotalGastoResult {
  totalGasto: number
  gastoCartasEstoque: number
  gastoCartasVendidas: number
  gastoProdutosEstoque: number
  gastoProdutosVendidos: number
}
/**
 * Calcula o total gasto em cartas e produtos
 * (estoque + já vendidos), com base nas tabelas:
 * - carta
 * - venda
 * - produto
 * - venda_produto
 */
export async function calculaTotalGasto(): Promise<TotalGastoResult> {
  try {
    // Gasto em cartas que ainda estão no estoque
    const gastoCartasEstoque = await singleNumber(`
      SELECT COALESCE(
               SUM(COALESCE(preco_da_compra, 0) * COALESCE(quantidade, 0)),
               0
             ) AS value
      FROM carta
    `)

    // Gasto em cartas já vendidas (snapshot salvo na tabela de venda)
    const gastoCartasVendidas = await singleNumber(`
      SELECT COALESCE(
               SUM(COALESCE(preco_da_compra, 0) * COALESCE(quantidade, 0)),
               0
             ) AS value
      FROM venda
    `)

    // Gasto em produtos no estoque
    const gastoProdutosEstoque = await singleNumber(`
      SELECT COALESCE(
               SUM(COALESCE(preco_compra, 0) * COALESCE(quantidade, 0)),
               0
             ) AS value
      FROM produto
    `)

    // Gasto em produtos vendidos
    // Se a coluna de custo não existir em venda_produto, tratamos como 0
    let gastoProdutosVendidos = 0

    try {
      gastoProdutosVendidos = await singleNumber(`
        SELECT COALESCE(
                 SUM(COALESCE(preco_compra, 0) * COALESCE(quantidade, 0)),
                 0
               ) AS value
        FROM venda_produto
      `)
    } catch (err) {
      // Se der erro (ex.: coluna não existe), mantemos 0
      console.warn('Coluna de custo em venda_produto não encontrada ou erro na query:', err)
      gastoProdutosVendidos = 0
    }

    const totalGasto =
      gastoCartasEstoque +
      gastoCartasVendidas +
      gastoProdutosEstoque +
      gastoProdutosVendidos

    return {
      totalGasto: totalGasto,
      gastoCartasEstoque: gastoCartasEstoque,
      gastoCartasVendidas: gastoCartasVendidas,
      gastoProdutosEstoque: gastoProdutosEstoque,
      gastoProdutosVendidos: gastoProdutosVendidos
    }
  } catch (err) {
    console.error('Erro ao calcular total gasto:', err)
    await logError('Erro ao calcular total gasto: ' + String(err))
    return null as any
  }
}

/**
 * Calcula a soma da coluna `quantidade` de uma tabela.
 * ATENÇÃO: para evitar SQL injection, use apenas nomes de tabela conhecidos.
 */
export async function calculaQuantidade(tabela: string): Promise<number> {
  // Opcional: whitelist de tabelas permitidas
  const tabelasPermitidas = new Set(['carta', 'produto', 'venda', 'venda_produto'])
  if (!tabelasPermitidas.has(tabela)) {
    await logError(`Tabela inválida em calculaQuantidade: ${tabela}`)
    return 0
  }

  const query = `SELECT SUM(quantidade) AS value FROM ${tabela};`

  try {
    const db = await getDb()
    const rows = await db.select<{ value: number | string | null }[]>(query)

    if (!rows.length) return 0

    const raw = rows[0]?.value ?? 0
    const num = typeof raw === 'number' ? raw : Number(raw)

    return Number.isNaN(num) ? 0 : num
  } catch (e) {
    console.error('Erro ao calcular quantidade:', e)
    await logError('Erro ao calcular quantidade: ' + String(e))
    return 0
  }
}
/**
 * Calcula o lucro total das cartas vendidas.
 * @returns Lucro total das cartas vendidas ou 0 em caso de erro/ausência de dados.
 */
export async function calcularLucroTotalCartasVendidas(): Promise<number> {
  const query = `
    SELECT
      SUM((preco_da_venda - preco_da_compra) * quantidade) AS lucro_total
    FROM venda
    WHERE preco_da_venda IS NOT NULL
      AND preco_da_compra IS NOT NULL;
  `

  try {
    const db = await getDb()
    const rows = await db.select<{ lucro_total: number | string | null }[]>(query)

    if (!rows.length) {
      return 0
    }

    const raw = rows[0]?.lucro_total ?? 0
    const num = typeof raw === 'number' ? raw : Number(raw)

    return Number.isNaN(num) ? 0 : num
  } catch (e) {
    console.error('Erro ao calcular lucro de cartas vendidas:', e)
    await logError('Erro ao calcular lucro de cartas vendidas: ' + String(e))
    return 0
  }
}

/**
 * Calcula o lucro total dos produtos vendidos.
 * @returns Lucro total dos produtos vendidos ou 0 em caso de erro/ausência de dados.
 */
export async function calcularLucroTotalProdutosVendidos(): Promise<number> {
  const query = `
    SELECT
      SUM((preco_venda - preco_compra) * quantidade) AS lucro_total
    FROM venda_produto
    WHERE preco_venda IS NOT NULL
      AND preco_compra IS NOT NULL;
  `

  try {
    const db = await getDb()
    const rows = await db.select<{ lucro_total: number | string | null }[]>(query)

    if (!rows.length) {
      return 0
    }

    const raw = rows[0]?.lucro_total ?? 0
    const num = typeof raw === 'number' ? raw : Number(raw)

    return Number.isNaN(num) ? 0 : num
  } catch (e) {
    console.error('Erro ao calcular lucro de produtos vendidos:', e)
    await logError('Erro ao calcular lucro de produtos vendidos: ' + String(e))
    return 0
  }
}