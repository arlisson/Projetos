import Database from '@tauri-apps/plugin-sql'
import { fetch } from '@tauri-apps/plugin-http'
import { invoke } from '@tauri-apps/api/core'
import * as cheerio from 'cheerio'
import {
  extractConfiguredData,
  listFieldOccurrences,
  validateScraperConfig,
  type ConfiguredExtractionResult,
  type FieldOccurrenceResult,
  type ScraperSite,
  type ScraperSiteConfig,
} from '../../scraping/configurableExtractor'
import { getDefaultScraperConfig } from '../../scraping/scraperDefaults'
import { logError } from './logger'

const DB_URL = 'sqlite:yugioh.db'
const MAX_TEST_HTML_BYTES = 2_000_000

let dbPromise: Promise<Database> | null = null
let ensured = false

export interface ScraperConfigHistoryItem {
  id: number
  site: ScraperSite
  previous_config_json: string | null
  new_config_json: string
  created_at: string
}

export interface ScraperSelectorTestResult extends ConfiguredExtractionResult {
  url: string
  ok: boolean
  message: string
}

export interface ScraperFieldOccurrencesResult {
  ok: boolean
  message: string
  field: string
  occurrences: FieldOccurrenceResult[]
}

interface ProdutoLigaTeste {
  imagem: string
  nome: string
  preco_atual: string
  origem: string
  link_site: string
}

async function getDb(): Promise<Database> {
  if (!dbPromise) dbPromise = Database.load(DB_URL)
  return dbPromise
}

async function ensureScraperTables(): Promise<void> {
  if (ensured) return

  const db = await getDb()

  await db.execute(`
    CREATE TABLE IF NOT EXISTS scraper_config (
      site TEXT PRIMARY KEY,
      config_json TEXT NOT NULL,
      updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
  `)

  await db.execute(`
    CREATE TABLE IF NOT EXISTS scraper_config_history (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      site TEXT NOT NULL,
      previous_config_json TEXT,
      new_config_json TEXT NOT NULL,
      created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
  `)

  ensured = true
}

function parseConfig(site: ScraperSite, value: string): ScraperSiteConfig {
  const parsed = JSON.parse(value) as ScraperSiteConfig
  return {
    ...parsed,
    site,
  }
}

export function getScraperSites(): ScraperSite[] {
  return ['mypcards', 'ligayugioh']
}

export async function getCustomScraperConfig(
  site: ScraperSite,
): Promise<ScraperSiteConfig | null> {
  await ensureScraperTables()

  try {
    const db = await getDb()
    const rows = await db.select<{ config_json: string }[]>(
      'SELECT config_json FROM scraper_config WHERE site = ? LIMIT 1',
      [site],
    )

    if (!rows.length) return null

    return parseConfig(site, rows[0].config_json)
  } catch (error) {
    await logError(`Erro ao carregar configuracao do scraper: ${String(error)}`)
    return null
  }
}

export async function getEffectiveScraperConfig(
  site: ScraperSite,
): Promise<ScraperSiteConfig> {
  const custom = await getCustomScraperConfig(site)
  return custom ?? getDefaultScraperConfig(site)
}

export async function saveScraperConfig(
  config: ScraperSiteConfig,
): Promise<{ ok: boolean; errors: string[] }> {
  await ensureScraperTables()

  const errors = validateScraperConfig(config)
  if (errors.length > 0) return { ok: false, errors }

  try {
    const db = await getDb()
    const previous = await db.select<{ config_json: string }[]>(
      'SELECT config_json FROM scraper_config WHERE site = ? LIMIT 1',
      [config.site],
    )

    const nextJson = JSON.stringify(config)
    const previousJson = previous[0]?.config_json ?? null

    await db.execute(
      `
      INSERT INTO scraper_config (site, config_json, updated_at)
      VALUES (?, ?, CURRENT_TIMESTAMP)
      ON CONFLICT(site) DO UPDATE SET
        config_json = excluded.config_json,
        updated_at = CURRENT_TIMESTAMP
      `,
      [config.site, nextJson],
    )

    await db.execute(
      `
      INSERT INTO scraper_config_history
        (site, previous_config_json, new_config_json, created_at)
      VALUES (?, ?, ?, CURRENT_TIMESTAMP)
      `,
      [config.site, previousJson, nextJson],
    )

    return { ok: true, errors: [] }
  } catch (error) {
    await logError(`Erro ao salvar configuracao do scraper: ${String(error)}`)
    return { ok: false, errors: [String(error)] }
  }
}

export async function restoreDefaultScraperConfig(
  site: ScraperSite,
): Promise<void> {
  await saveScraperConfig(getDefaultScraperConfig(site))
}

export async function listScraperConfigHistory(
  site: ScraperSite,
): Promise<ScraperConfigHistoryItem[]> {
  await ensureScraperTables()

  try {
    const db = await getDb()
    return await db.select<ScraperConfigHistoryItem[]>(
      `
      SELECT id, site, previous_config_json, new_config_json, created_at
      FROM scraper_config_history
      WHERE site = ?
      ORDER BY id DESC
      LIMIT 30
      `,
      [site],
    )
  } catch (error) {
    await logError(`Erro ao listar historico do scraper: ${String(error)}`)
    return []
  }
}

export async function restoreScraperConfigVersion(
  historyItem: ScraperConfigHistoryItem,
): Promise<{ ok: boolean; errors: string[] }> {
  const config = parseConfig(historyItem.site, historyItem.new_config_json)
  return saveScraperConfig(config)
}

export async function testScraperConfig(
  config: ScraperSiteConfig,
  url: string,
): Promise<ScraperSelectorTestResult> {
  const errors = validateScraperConfig(config)
  if (errors.length > 0) {
    return {
      site: config.site,
      url,
      ok: false,
      message: errors.join(' '),
      values: {},
      diagnostics: {},
    }
  }

  try {
    if (config.site === 'ligayugioh') {
      const produto = await invoke<ProdutoLigaTeste | null>(
        'buscar_produto_liga_cmd',
        {
          url,
          configJson: JSON.stringify(config),
        },
      )

      const values = {
        name: produto?.nome ?? null,
        price: produto?.preco_atual ?? null,
        image: produto?.imagem ?? null,
        link: produto?.link_site ?? url,
      }

      return {
        site: config.site,
        url,
        ok: produto !== null,
        message: produto
          ? 'Teste concluido com Playwright.'
          : 'Nenhum valor encontrado pelo scraper.',
        values,
        diagnostics: Object.entries(values).reduce(
          (acc, [field, value]) => {
            acc[field] = {
              field,
              found: Boolean(value),
              selectorUsed: null,
              rawValue: value === null ? null : String(value),
              normalizedValue: value,
              fallbackApplied: false,
              indexUsed: null,
              matchCount: value ? 1 : 0,
              error: value ? null : 'Nenhum valor encontrado',
            }
            return acc
          },
          {} as ScraperSelectorTestResult['diagnostics'],
        ),
      }
    }

    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'User-Agent':
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
      },
    })

    const html = await response.text()
    if (html.length > MAX_TEST_HTML_BYTES) {
      return {
        site: config.site,
        url,
        ok: false,
        message: 'HTML muito grande para teste local.',
        values: {},
        diagnostics: {},
      }
    }

    const $ = cheerio.load(html)
    const result = extractConfiguredData($, config, url || config.baseUrl)

    return {
      ...result,
      url,
      ok: true,
      message: 'Teste concluido.',
    }
  } catch (error) {
    return {
      site: config.site,
      url,
      ok: false,
      message: String(error),
      values: {},
      diagnostics: {},
    }
  }
}

export async function testScraperFieldOccurrences(
  config: ScraperSiteConfig,
  field: string,
  url: string,
): Promise<ScraperFieldOccurrencesResult> {
  const fieldConfig = config.fields[field]

  if (!fieldConfig) {
    return {
      ok: false,
      message: 'Campo nao encontrado na configuracao.',
      field,
      occurrences: [],
    }
  }

  if (config.site === 'ligayugioh') {
    return {
      ok: false,
      message:
        'Teste individual de ocorrencias ainda usa HTML direto. Use este recurso no MYPCards ou o teste geral para LigaYugioh.',
      field,
      occurrences: [],
    }
  }

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'User-Agent':
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
      },
    })

    const html = await response.text()
    if (html.length > MAX_TEST_HTML_BYTES) {
      return {
        ok: false,
        message: 'HTML muito grande para teste local.',
        field,
        occurrences: [],
      }
    }

    const $ = cheerio.load(html)
    const occurrences = listFieldOccurrences(
      $,
      fieldConfig,
      url || config.baseUrl,
    )

    return {
      ok: true,
      message:
        occurrences.length > 0
          ? `${occurrences.length} ocorrencia(s) encontrada(s).`
          : 'Nenhuma ocorrencia encontrada.',
      field,
      occurrences,
    }
  } catch (error) {
    return {
      ok: false,
      message: String(error),
      field,
      occurrences: [],
    }
  }
}
