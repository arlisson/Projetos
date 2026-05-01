// src/services/database.ts
import Database from '@tauri-apps/plugin-sql'
import { logError } from '../services/logger'

// mesmo arquivo do Python: DB_PATH = "yugioh.db"
const DB_URL = 'sqlite:yugioh.db'



// Aqui deixo uma função auxiliar para gerar a data AAAA-MM-DD.
export function todayStr(): string {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

let dbPromise: Promise<Database> | null = null

async function getDb(): Promise<Database> {
  if (!dbPromise) {
    dbPromise = Database.load(DB_URL)
  }
  // logInfo('Conectado ao banco de dados.')
  return dbPromise
}


// export async function testDbConnection(): Promise<{ ok: boolean; message: string }> {
//   try {
//     const db = await getDb()
//     await db.select('SELECT 1 as value')

//     await logInfo('Conexão com o banco de dados bem-sucedida.')
//     return { ok: true, message: 'Conexão com o banco OK.' }
//   } catch (err) {
//     ////console.error('Erro ao conectar no banco:', err)
//     await logError('Erro ao conectar no banco: ' + String(err))
//     return { ok: false, message: String(err) }
//   }
// }

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
export interface VendaProduto{
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
  data_venda?: string | null
  preco_venda?: number | null
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

  //Com os IDs de coleção e raridade, para facilitar edição
  export interface VendaCarta{
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
    colecao?: string | null    
    raridade?: string | null
    qualidade?: string | null

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


export async function registrarHistoricoLucro(): Promise<void> {
  const db = await getDb()

  try {
    // resumo = buscar_historico_precos(resumo=True)
    const resumo = (await buscarHistoricoPrecos(
      undefined,
      undefined,
      true,
    )) as ResumoLucro

    const lucroCartas =
      (resumo.lucro_cartas ?? 0) + (resumo.total_vendas_cartas ?? 0)

    const lucroProdutos =
      (resumo.lucro_produtos ?? 0) + (resumo.total_vendas_produtos ?? 0)

    const total = lucroCartas + lucroProdutos

    // Data atual sem hora (equivalente ao DATA_SCRAPING)
    const dataHoje = todayStr()

    // Verifica se já existe registro hoje
    const existentes = await db.select<{ id_lucro: number }[]>(
      `
      SELECT id_lucro
      FROM historico_lucro
      WHERE DATE(data) = ?
    `,
      [dataHoje],
    )

    const existente = existentes[0]

    if (existente) {
      // Atualiza registro existente
      await db.execute(
        `
        UPDATE historico_lucro
        SET lucro_cartas = ?, lucro_produtos = ?, lucro_total = ?
        WHERE id_lucro = ?
      `,
        [lucroCartas, lucroProdutos, total, existente.id_lucro],
      )
    } else {
      // Insere novo registro
      await db.execute(
        `
        INSERT INTO historico_lucro (lucro_cartas, lucro_produtos, lucro_total, data)
        VALUES (?, ?, ?, ?)
      `,
        [lucroCartas, lucroProdutos, total, dataHoje],
      )
    }
  } catch (err) {
    //console.error('Erro ao registrar histórico de lucro:', err)
    await logError('Erro ao registrar histórico de lucro: ' + String(err))
  }
}

export async function registrarHistoricoGenerico(
  tipo: 'carta' | 'produto' = 'carta',
  id?: number | null,
  preco?: number | null,
  data?: string | null,
  origem: string = 'MYPCards',
): Promise<void> {
  if (tipo !== 'carta' && tipo !== 'produto') {
    throw new Error("Tipo inválido. Use 'carta' ou 'produto'.")
  }

  try {
    const db = await getDb()

    if (tipo === 'carta') {
      await db.execute(
        `
        INSERT INTO historico_precos (id_carta, id_produto, data, preco, origem)
        VALUES (?, NULL, ?, ?, ?)
      `,
        [id ?? null, data ?? null, preco ?? null, origem],
      )
    } else {
      await db.execute(
        `
        INSERT INTO historico_precos (id_carta, id_produto, data, preco, origem)
        VALUES (NULL, ?, ?, ?, ?)
      `,
        [id ?? null, data ?? null, preco ?? null, origem],
      )
    }
  } catch (err) {
    //console.error('Erro ao registrar histórico:', err)
    await logError('Erro ao registrar histórico: ' + String(err))
  }
}

export async function updateHistoricoGenerico(
  tipo: 'carta' | 'produto' = 'carta',
  id?: number | null,
  preco?: number | null,
  data?: string | null,
  origem: string = 'MYPCards',
): Promise<void> {
  if (tipo !== 'carta' && tipo !== 'produto') {
    throw new Error("Tipo inválido. Use 'carta' ou 'produto'.")
  }

  try {
    const db = await getDb()

    if (tipo === 'carta') {
      await db.execute(
        `
        UPDATE historico_precos
        SET data = ?, preco = ?, origem = ?
        WHERE id_carta = ?
          AND data = (
            SELECT MAX(data)
            FROM historico_precos
            WHERE id_carta = ?
          )
      `,
        [data ?? null, preco ?? null, origem, id ?? null, id ?? null],
      )
    } else {
      await db.execute(
        `
        UPDATE historico_precos
        SET data = ?, preco = ?, origem = ?
        WHERE id_produto = ?
          AND data = (
            SELECT MAX(data)
            FROM historico_precos
            WHERE id_produto = ?
          )
      `,
        [data ?? null, preco ?? null, origem, id ?? null, id ?? null],
      )
    }
  } catch (err) {
    //console.error('Erro ao atualizar histórico:', err)
    await logError('Erro ao atualizar histórico: ' + String(err))
  }
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
    //console.error('Erro ao buscar todas as cartas:', err)
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
    //console.error('Erro ao buscar cartas com filtro:', err)
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
    //console.error('Erro ao buscar todos os produtos:', err)
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
    //console.error('Erro ao buscar produtos com filtro:', err)
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
    //console.error('Erro ao buscar vendas de cartas:', err)
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
    //console.error('Erro ao buscar vendas de cartas com filtro:', err)
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
    //console.error('Erro ao buscar vendas de produtos:', err)
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
    //console.error('Erro ao buscar vendas de produtos com filtro:', err)
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
    //console.error('Erro ao buscar histórico:', err)
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
    //console.error('Erro ao calcular total gasto:', err)
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
    //console.error('Erro ao calcular quantidade:', e)
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
    //console.error('Erro ao calcular lucro de cartas vendidas:', e)
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
    //console.error('Erro ao calcular lucro de produtos vendidos:', e)
    await logError('Erro ao calcular lucro de produtos vendidos: ' + String(e))
    return 0
  }
}

export async function listarRaridadeQualidade(nome_tabela: string): Promise<
  { id: number; nome: string }[]
> {
  try {
    const db = await getDb()
    const rows = await db.select<{ id: number; nome: string }[]>(
      `SELECT * FROM ${nome_tabela};`,
    )
    return rows
  } catch (err) {
    //console.error(`Erro ao listar ${nome_tabela}:`, err)
    await logError(`Erro ao listar ${nome_tabela}: ` + String(err))
    return []
  }
}

export interface QualidadeDB {
  id_qualidade: number
  nome: string
}

export interface RaridadeDB {
  id_raridade: number
  nome: string
}

export type OpcaoSelect = {
  value: string
  label: string
}
export interface ColecaoDB {
  id_colecao: number
  nome: string
  codigo: string
}
export async function listarColecoes() {
  try {
    const db = await getDb()
    const rows = await db.select<ColecaoDB[]>(
      `SELECT * FROM colecao;`,
    )
    return rows
  } catch (err) {
    //console.error(`Erro ao listar coleções:`, err)
    await logError(`Erro ao listar coleções: ` + String(err))
    return []
  }  
}

export async function buscarQualidadeRaridadeId(id: number, tabela: 'qualidade' | 'raridade'): Promise<string | null> {
  try {
    const db = await getDb()
    const rows = await db.select<{ nome: string }[]>(
      `SELECT nome FROM ${tabela} WHERE id_${tabela} = ?;`,
      [id]
    )
    return rows.length > 0 ? rows[0].nome : null
  } catch (err) {
    //console.error(`Erro ao buscar ${tabela}:`, err)
    await logError(`Erro ao buscar ${tabela}: ` + String(err))
    return null
  }
}

export async function inserirColecao(nome: string, codigo: string): Promise<number | null> {
  try {
    const db = await getDb()
    const nomeLimpo = String(nome || '').trim().toUpperCase()
    const codigoLimpo = String(codigo || '').trim().toUpperCase()

    if (!nomeLimpo) {
      return null
    }

    const existente = await db.select<{ id_colecao: number }[]>(
      `
      SELECT id_colecao
      FROM colecao
      WHERE UPPER(nome) = ?
      LIMIT 1
      `,
      [nomeLimpo],
    )

    if (existente.length > 0) {
      return null
    }

    await db.execute(
      `INSERT INTO colecao (nome, codigo) VALUES (?, ?)`,
      [nomeLimpo, codigoLimpo]
    )
    const result = await db.select<{ id_colecao: number }[]>(
      `SELECT last_insert_rowid() as id_colecao`
    )
    return result.length > 0 ? result[0].id_colecao : null
  } catch (err) {
    //console.error(`Erro ao inserir coleção:`, err)
    await logError(`Erro ao inserir coleção: ` + String(err))
    return null
  }
}

export async function buscarColecao(nome:String) {

  try { 
    const db = await getDb()
    const rows = await db.select<ColecaoDB[]>(
      `SELECT * FROM colecao WHERE nome = ?`,
      [nome.toUpperCase()]
    )
    return rows.length > 0 ? rows[0] : null
  } catch (err) {
    //console.error(`Erro ao buscar coleção:`, err)
    await logError(`Erro ao buscar coleção: ` + String(err))
    return null    
  }
}

export async function atualizarColecao(
  id: number,
  nome: string,
  codigo: string,
): Promise<boolean> {
  try {
    const db = await getDb()
    const nomeLimpo = String(nome || '').trim().toUpperCase()
    const codigoLimpo = String(codigo || '').trim().toUpperCase()

    if (!nomeLimpo) {
      return false
    }

    const duplicada = await db.select<{ id_colecao: number }[]>(
      `
      SELECT id_colecao
      FROM colecao
      WHERE UPPER(nome) = ?
        AND id_colecao <> ?
      LIMIT 1
      `,
      [nomeLimpo, id],
    )

    if (duplicada.length > 0) {
      return false
    }

    await db.execute(
      `
      UPDATE colecao
      SET nome = ?, codigo = ?
      WHERE id_colecao = ?
      `,
      [nomeLimpo, codigoLimpo, id],
    )

    return true
  } catch (err) {
    await logError(`Erro ao atualizar colecao: ` + String(err))
    return false
  }
}

export async function excluirColecao(
  id: number,
): Promise<{ ok: boolean; motivo?: string }> {
  try {
    const db = await getDb()

    const usoCartas = await db.select<{ total: number }[]>(
      `
      SELECT COUNT(*) AS total
      FROM carta
      WHERE colecao = ?
      `,
      [id],
    )

    if ((usoCartas[0]?.total ?? 0) > 0) {
      return {
        ok: false,
        motivo: 'Nao e possivel excluir a colecao porque ela esta vinculada a cartas cadastradas.',
      }
    }

    const usoVendas = await db.select<{ total: number }[]>(
      `
      SELECT COUNT(*) AS total
      FROM venda
      WHERE colecao = ?
      `,
      [id],
    )

    if ((usoVendas[0]?.total ?? 0) > 0) {
      return {
        ok: false,
        motivo: 'Nao e possivel excluir a colecao porque ela esta vinculada a vendas cadastradas.',
      }
    }

    await db.execute(
      `
      DELETE FROM colecao
      WHERE id_colecao = ?
      `,
      [id],
    )

    return { ok: true }
  } catch (err) {
    await logError(`Erro ao excluir colecao: ` + String(err))
    return {
      ok: false,
      motivo: 'Erro interno ao excluir colecao.',
    }
  }
}

export async function garantirRaridade(nome: string): Promise<number | null> {
  try {
    const nomeLimpo = String(nome || '').trim().toUpperCase()

    if (!nomeLimpo) {
      return null
    }

    const db = await getDb()

    const existente = await db.select<{ id_raridade: number }[]>(
      `SELECT id_raridade FROM raridade WHERE UPPER(nome) = ? LIMIT 1`,
      [nomeLimpo]
    )

    if (existente.length > 0) {
      return existente[0].id_raridade
    }

    await db.execute(
      `INSERT INTO raridade (nome) VALUES (?)`,
      [nomeLimpo]
    )

    const criada = await db.select<{ id_raridade: number }[]>(
      `SELECT id_raridade FROM raridade WHERE UPPER(nome) = ? LIMIT 1`,
      [nomeLimpo]
    )

    return criada.length > 0 ? criada[0].id_raridade : null
  } catch (err) {
    await logError(`Erro ao garantir raridade: ${String(err)}`)
    return null
  }
}

export async function inserirCarta(carta: InserirCartaPayload): Promise<boolean> {
  try {
    const db = await getDb()

    const inserida = await db.select<{ id_carta: number }[]>(
      `
      INSERT INTO carta (
        link_site, nome, codigo, preco_da_compra, preco_atual,
        data_da_compra, quantidade, imagem, imagem_salva,
        origem, raridade, qualidade, colecao, data_scraping
      )
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      RETURNING id_carta
      `,
      [
        carta.link_site,
        carta.nome.toUpperCase(),
        carta.codigo?.toUpperCase(),
        carta.preco_da_compra,
        carta.preco_atual,
        carta.data_da_compra,
        carta.quantidade,
        carta.imagem,
        carta.imagem_salva,
        carta.origem?.toUpperCase(),
        carta.raridade,
        carta.qualidade,
        carta.colecao,
        todayStr(),
      ]
    )

    if (!inserida.length || !inserida[0].id_carta) {
      throw new Error('Não foi possível obter o id da carta inserida.')
    }

    const idCarta = inserida[0].id_carta

    await registrarHistoricoLucro()

    await salvarHistoricoPrecoCarta(
      idCarta,
      carta.preco_atual ?? null,
      todayStr(),
      carta.origem ?? 'MYPCards'
    )

    return true
  } catch (err) {
    await logError('Erro ao inserir a carta: ' + String(err))
    return false
  }
}

export async function salvarHistoricoPrecoCarta(
  idCarta: number,
  preco: number | null,
  data: string = todayStr(),
  origem: string = 'MYPCards',
): Promise<void> {
  try {
    const db = await getDb()

    const cartaExiste = await db.select<{ id_carta: number }[]>(
      `
      SELECT id_carta
      FROM carta
      WHERE id_carta = ?
      LIMIT 1
      `,
      [idCarta],
    )

    if (cartaExiste.length === 0) {
      throw new Error(`Carta com id ${idCarta} não existe.`)
    }

    const existentes = await db.select<{ id_historico_precos: number }[]>(
      `
      SELECT id_historico_precos
      FROM historico_precos
      WHERE id_carta = ?
        AND DATE(data) = DATE(?)
      LIMIT 1
      `,
      [idCarta, data],
    )

    if (existentes.length > 0) {
      await db.execute(
        `
        UPDATE historico_precos
        SET preco = ?, origem = ?, data = ?
        WHERE id_historico_precos = ?
        `,
        [preco, origem, data, existentes[0].id_historico_precos],
      )
    } else {
      await db.execute(
        `
        INSERT INTO historico_precos (id_carta, id_produto, data, preco, origem)
        VALUES (?, NULL, ?, ?, ?)
        `,
        [idCarta, data, preco, origem],
      )
    }
  } catch (err) {
    await logError('Erro ao salvar histórico de preço da carta: ' + String(err))
    throw err
  }
}

export async function buscarCartaId( id: number ): Promise<CartaDetalhada | null> {
  try {
    const db = await getDb()
    const rows = await db.select<CartaDetalhada[]>(
      `SELECT * FROM carta WHERE id_carta = ?`,
      [id]
    )
    return rows.length > 0 ? rows[0] : null
  } catch (err) {
    //console.error(`Erro ao buscar carta:`, err)
    await logError(`Erro ao buscar carta: ` + String(err))
    return null
  }
}

export async function buscarProdutoId(id: number): Promise<ProdutoDetalhado | null> {
  try {
    const db = await getDb()
    const rows = await db.select<ProdutoDetalhado[]>(
      `SELECT * FROM produto WHERE id_produto = ?`,
      [id]
    )
    return rows.length > 0 ? rows[0] : null
  } catch (err) {
    //console.error(`Erro ao buscar produto:`, err)
    await logError(`Erro ao buscar produto: ` + String(err))
    return null
  }
}

export async function inserirProduto(produto: InserirProdutoPayload): Promise<boolean> {
  try {
    const db = await getDb()
    await db.execute(
      `INSERT INTO produto (nome_produto, link, imagem, preco_compra, preco_atual, data_compra, quantidade, imagem_salva, origem, data_scraping) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      [
        produto.nome_produto.toUpperCase(),
        produto.link,
        produto.imagem,
        produto.preco_compra,
        produto.preco_atual,
        produto.data_compra,
        produto.quantidade,
        produto.imagem_salva,
        produto.origem?.toUpperCase(),
        todayStr()
      ]
    )
    const last_id = await db.select<{ last_insert_rowid: number }[]>(
      `SELECT last_insert_rowid() as last_insert_rowid`
    )
    registrarHistoricoLucro();
    registrarHistoricoGenerico('produto', last_id[0].last_insert_rowid, produto.preco_atual ?? null, todayStr(), produto.origem ?? 'MYPCards');
    return true;
  }catch (err) {
    //console.error('Erro ao inserir o produto:', err)
    await logError('Erro ao inserir o produto: ' + String(err))
    return false;
  }
}

export async function deletar(tipo: 'carta' | 'produto', id: number): Promise<boolean> {
  try {
    const db = await getDb()
    await db.execute(
      `DELETE FROM ${tipo} WHERE id_${tipo} = ?`,
      [id]
    )
    return true;
  } catch (err) {
    //console.error(`Erro ao deletar ${tipo}:`, err)
    await logError(`Erro ao deletar ${tipo}: ` + String(err))
    return false;
  }
}

export async function deletarVendaCarta(id: number): Promise<boolean> {
  try {
    const db = await getDb()
    await db.execute(
      `DELETE FROM venda WHERE id_carta = ?`,
      [id]
    )
    return true;
  } catch (err) {
    //console.error(`Erro ao deletar ${tipo}:`, err)
    await logError(`Erro ao deletar venda: ` + String(err))
    return false;
  }
}

export async function deletarVendaProduto(id: number): Promise<boolean> {
  try {
    const db = await getDb()  
    await db.execute(
      `DELETE FROM venda_produto WHERE id_produto = ?`,
      [id]
    )
    return true;
  } catch (err) {
    //console.error(`Erro ao deletar venda:`, err)
    await logError(`Erro ao deletar venda: ` + String(err))
    return false;
  }
}

export async function atualizarCarta(id: number, carta: InserirCartaPayload): Promise<boolean> {
  try {
    const db = await getDb()  
    await db.execute(
      `UPDATE carta SET link_site = ?, nome = ?, codigo = ?, preco_da_compra = ?, preco_atual = ?, data_da_compra = ?, quantidade = ?, imagem = ?, imagem_salva = ?, origem = ?, raridade = ?, qualidade = ?, colecao = ? WHERE id_carta = ?`,
      [
        carta.link_site,
        carta.nome.toUpperCase(),
        carta.codigo?.toUpperCase(),
        carta.preco_da_compra,
        carta.preco_atual,
        carta.data_da_compra,
        carta.quantidade,
        carta.imagem,
        carta.imagem_salva,
        carta.origem?.toUpperCase(),
        carta.raridade,
        carta.qualidade,
        carta.colecao,
        id
      ]
    )
    registrarHistoricoGenerico('carta', id, carta.preco_atual ?? null, todayStr(), carta.origem ?? 'MYPCards');
    return true;
  } catch (err) {
    //console.error('Erro ao atualizar a carta:', err)
    await logError('Erro ao atualizar a carta: ' + String(err))
    return false;
  } 
}

export async function atualizarProduto(id: number, produto: InserirProdutoPayload): Promise<boolean> {
  try {
    const db = await getDb()  
    await db.execute(
      `UPDATE produto SET nome_produto = ?, link = ?, imagem = ?, preco_compra = ?, preco_atual = ?, data_compra = ?, quantidade = ?, imagem_salva = ?, origem = ? WHERE id_produto = ?`,
      [
        produto.nome_produto.toUpperCase(),
        produto.link,
        produto.imagem,
        produto.preco_compra,
        produto.preco_atual,
        produto.data_compra,
        produto.quantidade,
        produto.imagem_salva,
        produto.origem?.toUpperCase(),
        id
      ]
    )
    registrarHistoricoGenerico('produto', id, produto.preco_atual ?? null, todayStr(), produto.origem ?? 'MYPCards');
    return true;
  } catch (err) {
    //console.error('Erro ao atualizar o produto:', err)
    await logError('Erro ao atualizar o produto: ' + String(err))
    return false;
  } 
}

export interface InserirVendaCartaPayload {
  id_carta: number
  preco_da_venda: number | null
  data_da_venda: string | null // "YYYY-MM-DD"
  quantidade: number | null
}

export function venderCarta(inserirCarta: InserirCartaPayload, inserirVenda: InserirVendaCartaPayload, quantidade: number): Promise<boolean> {
  return new Promise(async (resolve) => {
    try {
      const db = await getDb()
      await db.execute(
        `UPDATE carta SET quantidade = quantidade - ? WHERE id_carta = ?`,
        [quantidade, inserirVenda.id_carta]
      )
      await db.execute(
        `INSERT INTO venda ( link_site, nome, codigo, preco_da_compra, preco_atual, data_da_compra, quantidade, imagem, imagem_salva, origem, raridade, qualidade, colecao, data_scraping, preco_da_venda, data_da_venda) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
        [ inserirCarta.link_site, inserirCarta.nome, inserirCarta.codigo, inserirCarta.preco_da_compra, inserirCarta.preco_atual, inserirCarta.data_da_compra, quantidade, inserirCarta.imagem, inserirCarta.imagem_salva, inserirCarta.origem, inserirCarta.raridade, inserirCarta.qualidade, inserirCarta.colecao, todayStr(), inserirVenda.preco_da_venda, inserirVenda.data_da_venda]
      )
      registrarHistoricoLucro();
      resolve(true);
    } catch (err) {
      //console.error('Erro ao registrar venda da carta:', err)
      await logError('Erro ao registrar venda da carta: ' + String(err))
      resolve(false);
    } 
  });
}

export interface InserirVendaProdutoPayload {
  id_produto: number
  preco_venda: number | null
  data_venda: string | null // "YYYY-MM-DD"
  quantidade: number | null
}

export async function venderProduto(inserirProduto: InserirProdutoPayload, inserirVenda: InserirVendaProdutoPayload, quantidade: number): Promise<boolean> {
  return new Promise(async (resolve) => {
    try {
      const db = await getDb()
      await db.execute(
        `INSERT INTO venda_produto (nome_produto, link, imagem, preco_compra, preco_atual, data_compra, quantidade, imagem_salva, origem, data_scraping, preco_venda, data_venda) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
        [ inserirProduto.nome_produto, inserirProduto.link, inserirProduto.imagem, inserirProduto.preco_compra, inserirProduto.preco_atual, inserirProduto.data_compra, quantidade, inserirProduto.imagem_salva, inserirProduto.origem, todayStr(), inserirVenda.preco_venda, inserirVenda.data_venda]
      )
      await db.execute(
        `UPDATE produto SET quantidade = quantidade - ? WHERE id_produto = ?`,
        [quantidade, inserirVenda.id_produto]
      )
      registrarHistoricoLucro();
      resolve(true);
    } catch (err) {
      console.error('Erro ao registrar venda do produto:', err)
      await logError('Erro ao registrar venda do produto: ' + String(err))
      resolve(false);
    }
  });
}

export function precoMaximoMinimo(tipo: 'carta' | 'produto', id: number): Promise<{ preco_maximo: number | null; preco_minimo: number | null }> {
  return new Promise(async (resolve) => {
    try {
      const db = await getDb()
      const colunaId = tipo === 'carta' ? 'id_carta' : 'id_produto'
      const rows = await db.select<{ preco_maximo: number | null; preco_minimo: number | null }[]>(
        `
        SELECT
          MAX(preco) AS preco_maximo,
          MIN(preco) AS preco_minimo
        FROM historico_precos
        WHERE ${colunaId} = ?
      `,
        [id],
      )
      if (rows.length > 0) {
        resolve({ preco_maximo: rows[0].preco_maximo, preco_minimo: rows[0].preco_minimo })
      } else {
        resolve({ preco_maximo: null, preco_minimo: null })
      }

    } catch (err) {
      //console.error('Erro ao calcular preço máximo e mínimo:', err)
      await logError('Erro ao calcular preço máximo e mínimo: ' + String(err))
      resolve({ preco_maximo: null, preco_minimo: null })
    } 
  });
} 

export function buscarVendaCartaId(id: number): Promise<VendaCarta | null> {
  return new Promise(async (resolve) => {
    try {
      const db = await getDb()
      const rows = await db.select<VendaCarta[]>(
        `SELECT * FROM venda WHERE id_carta = ?`,
        [id]
      )
      resolve(rows.length > 0 ? rows[0] : null)
    } catch (err) {
      //console.error(`Erro ao buscar venda de carta:`, err)
      await logError(`Erro ao buscar venda de carta: ` + String(err))
      resolve(null)
    }
  });
}

export async function atualizarVendaCarta(id: number, venda: InserirVendaCartaPayload): Promise<boolean> {
  try {
    const db = await getDb()
    await db.execute(
      `UPDATE venda SET preco_da_venda = ?, data_da_venda = ?, quantidade = ? WHERE id_carta = ?`,
      [venda.preco_da_venda, venda.data_da_venda, venda.quantidade, id]
    )
    registrarHistoricoLucro();
    return true;
  } catch (err) {
    //console.error('Erro ao atualizar a venda da carta:', err)
    await logError('Erro ao atualizar a venda da carta: ' + String(err))
    return false;
  } 
}

export function buscarVendaProdutoId(id: number): Promise<VendaProduto | null> {
  return new Promise(async (resolve) => {
    try { 
      const db = await getDb()
      const rows = await db.select<VendaProduto[]>(
        `SELECT * FROM venda_produto WHERE id_produto = ?`,
        [id]
      )
      resolve(rows.length > 0 ? rows[0] : null)
    } catch (err) {
      //console.error(`Erro ao buscar venda de produto:`, err)
      await logError(`Erro ao buscar venda de produto: ` + String(err))
      resolve(null)    
    }
  });
}

export interface AtualizarVendaProdutoPayload {
  id_produto: number  
  preco_venda: number | null
  data_venda: string | null // "YYYY-MM-DD"
  quantidade: number | null
}

export async function atualizarVendaProduto(id: number, venda: AtualizarVendaProdutoPayload): Promise<boolean> {
  try {
    const db = await getDb()
    await db.execute(
      `UPDATE venda_produto SET preco_venda = ?, data_venda = ?, quantidade = ? WHERE id_produto = ?`,
      [venda.preco_venda, venda.data_venda, venda.quantidade, id]
    )
    registrarHistoricoLucro();
    return true;
  } catch (err) {
    //console.error('Erro ao atualizar a venda do produto:', err)
    await logError('Erro ao atualizar a venda do produto: ' + String(err))
    return false;
  }
}

export type TipoCadastroBase = 'raridade' | 'qualidade'

export interface ItemCadastroBase {
  id: number
  nome: string
}

function getIdColumnByTipo(tipo: TipoCadastroBase): string {
  return tipo === 'raridade' ? 'id_raridade' : 'id_qualidade'
}

export async function listarCadastroBase(
  tipo: TipoCadastroBase,
): Promise<ItemCadastroBase[]> {
  try {
    const db = await getDb()
    const idCol = getIdColumnByTipo(tipo)

    const rows = await db.select<ItemCadastroBase[]>(
      `
      SELECT ${idCol} AS id, nome
      FROM ${tipo}
      ORDER BY nome ASC
      `,
    )

    return rows
  } catch (err) {
    await logError(`Erro ao listar ${tipo}: ` + String(err))
    return []
  }
}

export async function inserirCadastroBase(
  tipo: TipoCadastroBase,
  nome: string,
): Promise<boolean> {
  try {
    const db = await getDb()
    const nomeLimpo = String(nome || '').trim().toUpperCase()

    if (!nomeLimpo) {
      return false
    }

    const existente = await db.select<{ id: number }[]>(
      `
      SELECT ${getIdColumnByTipo(tipo)} AS id
      FROM ${tipo}
      WHERE UPPER(nome) = ?
      LIMIT 1
      `,
      [nomeLimpo],
    )

    if (existente.length > 0) {
      return false
    }

    await db.execute(
      `INSERT INTO ${tipo} (nome) VALUES (?)`,
      [nomeLimpo],
    )

    return true
  } catch (err) {
    await logError(`Erro ao inserir ${tipo}: ` + String(err))
    return false
  }
}

export async function atualizarCadastroBase(
  tipo: TipoCadastroBase,
  id: number,
  nome: string,
): Promise<boolean> {
  try {
    const db = await getDb()
    const nomeLimpo = String(nome || '').trim().toUpperCase()

    if (!nomeLimpo) {
      return false
    }

    const idCol = getIdColumnByTipo(tipo)

    const duplicado = await db.select<{ id: number }[]>(
      `
      SELECT ${idCol} AS id
      FROM ${tipo}
      WHERE UPPER(nome) = ?
        AND ${idCol} <> ?
      LIMIT 1
      `,
      [nomeLimpo, id],
    )

    if (duplicado.length > 0) {
      return false
    }

    await db.execute(
      `
      UPDATE ${tipo}
      SET nome = ?
      WHERE ${idCol} = ?
      `,
      [nomeLimpo, id],
    )

    return true
  } catch (err) {
    await logError(`Erro ao atualizar ${tipo}: ` + String(err))
    return false
  }
}

export async function excluirCadastroBase(
  tipo: TipoCadastroBase,
  id: number,
): Promise<{ ok: boolean; motivo?: string }> {
  try {
    const db = await getDb()
    const idCol = getIdColumnByTipo(tipo)

    if (tipo === 'raridade') {
      const uso = await db.select<{ total: number }[]>(
        `
        SELECT COUNT(*) AS total
        FROM carta
        WHERE raridade = ?
        `,
        [id],
      )

      if ((uso[0]?.total ?? 0) > 0) {
        return {
          ok: false,
          motivo: 'Não é possível excluir a raridade porque ela está vinculada a cartas cadastradas.',
        }
      }
    }

    if (tipo === 'qualidade') {
      const uso = await db.select<{ total: number }[]>(
        `
        SELECT COUNT(*) AS total
        FROM carta
        WHERE qualidade = ?
        `,
        [id],
      )

      if ((uso[0]?.total ?? 0) > 0) {
        return {
          ok: false,
          motivo: 'Não é possível excluir a qualidade porque ela está vinculada a cartas cadastradas.',
        }
      }
    }

    await db.execute(
      `
      DELETE FROM ${tipo}
      WHERE ${idCol} = ?
      `,
      [id],
    )

    return { ok: true }
  } catch (err) {
    await logError(`Erro ao excluir ${tipo}: ` + String(err))
    return {
      ok: false,
      motivo: 'Erro interno ao excluir registro.',
    }
  }
}

export interface CartaEstoqueAtualizacao {
  id_carta: number
  nome: string
  link_site?: string | null
  raridade_nome?: string | null
  preco_atual?: number | null
  codigo?: string | null
  data_da_compra?: string | null
  preco_da_compra?: number | null
  quantidade?: number | null
  imagem?: string | null
  imagem_salva?: string | null
  origem?: string | null
  raridade?: number | null
  qualidade?: number | null
  colecao?: string | null
}

export interface ProdutoEstoqueAtualizacao {
  id_produto: number
  nome_produto: string
  link?: string | null
  preco_atual?: number | null
  data_compra?: string | null
  preco_compra?: number | null
  quantidade?: number | null
  imagem?: string | null
  imagem_salva?: string | null
  origem?: string | null
}

export async function buscarCartasEmEstoque(): Promise<CartaEstoqueAtualizacao[]> {
  try {
    const db = await getDb()
    return await db.select<CartaEstoqueAtualizacao[]>(
      `
      SELECT
        c.id_carta,
        c.nome,
        c.link_site,
        c.preco_atual,
        c.codigo,
        c.data_da_compra,
        c.preco_da_compra,
        c.quantidade,
        c.imagem,
        c.imagem_salva,
        c.origem,
        c.raridade,
        c.qualidade,
        c.colecao,
        r.nome AS raridade_nome
      FROM carta c
      LEFT JOIN raridade r ON r.id_raridade = c.raridade
      WHERE COALESCE(c.quantidade, 0) > 0
      ORDER BY c.nome ASC
      `,
    )
  } catch (err) {
    await logError('Erro ao buscar cartas em estoque: ' + String(err))
    return []
  }
}

export async function buscarProdutosEmEstoque(): Promise<ProdutoEstoqueAtualizacao[]> {
  try {
    const db = await getDb()
    return await db.select<ProdutoEstoqueAtualizacao[]>(
      `
      SELECT
        id_produto,
        nome_produto,
        link,
        preco_atual,
        data_compra,
        preco_compra,
        quantidade,
        imagem,
        imagem_salva,
        origem
      FROM produto
      WHERE COALESCE(quantidade, 0) > 0
      ORDER BY nome_produto ASC
      `,
    )
  } catch (err) {
    await logError('Erro ao buscar produtos em estoque: ' + String(err))
    return []
  }
}

export async function atualizarPrecoCartaPorScraping(
  idCarta: number,
  novoPreco: number | null,
  dataScraping: string = todayStr(),
  origem: string = 'MyPCards',
): Promise<boolean> {
  try {
    const db = await getDb()

    await db.execute(
      `
      UPDATE carta
      SET preco_atual = ?, data_scraping = ?, origem = ?
      WHERE id_carta = ?
      `,
      [novoPreco, dataScraping, origem.toUpperCase(), idCarta],
    )

    await salvarHistoricoPrecoCarta(idCarta, novoPreco, dataScraping, origem)
    return true
  } catch (err) {
    await logError('Erro ao atualizar preço da carta por scraping: ' + String(err))
    return false
  }
}

export async function salvarHistoricoPrecoProduto(
  idProduto: number,
  preco: number | null,
  data: string = todayStr(),
  origem: string = 'Liga Yugioh',
): Promise<void> {
  try {
    const db = await getDb()

    const existentes = await db.select<{ id_historico_precos: number }[]>(
      `
      SELECT id_historico_precos
      FROM historico_precos
      WHERE id_produto = ?
        AND DATE(data) = DATE(?)
      LIMIT 1
      `,
      [idProduto, data],
    )

    if (existentes.length > 0) {
      await db.execute(
        `
        UPDATE historico_precos
        SET preco = ?, origem = ?, data = ?
        WHERE id_historico_precos = ?
        `,
        [preco, origem, data, existentes[0].id_historico_precos],
      )
    } else {
      await db.execute(
        `
        INSERT INTO historico_precos (id_carta, id_produto, data, preco, origem)
        VALUES (NULL, ?, ?, ?, ?)
        `,
        [idProduto, data, preco, origem],
      )
    }
  } catch (err) {
    await logError('Erro ao salvar histórico de preço do produto: ' + String(err))
  }
}

export async function atualizarPrecoProdutoPorScraping(
  idProduto: number,
  novoPreco: number | null,
  dataScraping: string = todayStr(),
  origem: string = 'Liga Yugioh',
): Promise<boolean> {
  try {
    const db = await getDb()

    await db.execute(
      `
      UPDATE produto
      SET preco_atual = ?, data_scraping = ?, origem = ?
      WHERE id_produto = ?
      `,
      [novoPreco, dataScraping, origem.toUpperCase(), idProduto],
    )

    await salvarHistoricoPrecoProduto(idProduto, novoPreco, dataScraping, origem)
    return true
  } catch (err) {
    await logError('Erro ao atualizar preço do produto por scraping: ' + String(err))
    return false
  }
}
