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
  const rows = await db.select<{ value: number }[]>(query, params)
  const raw = rows[0]?.value
  return typeof raw === 'number' && !Number.isNaN(raw) ? raw : 0
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