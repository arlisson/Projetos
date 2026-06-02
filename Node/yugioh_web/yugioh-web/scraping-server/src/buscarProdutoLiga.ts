import * as cheerio from 'cheerio'
import { chromium } from 'playwright'
import {
  extractConfiguredData,
  type ScraperSiteConfig,
} from './configurableExtractor'
import { DEFAULT_LIGA_CONFIG } from './scraperDefaults'

const HEADERS = {
  'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}

const IMAGEM_PADRAO =
  'https://i.pinimg.com/736x/71/1e/da/711eda25308c65a7756751088866e181.jpg'

export interface ProdutoLiga {
  imagem: string
  nome: string
  preco_atual: string
  origem: string
  link_site: string
}

export async function buscarProdutoLiga(url: string): Promise<ProdutoLiga | null> {
  return buscarProdutoLigaConfiguravel(url, DEFAULT_LIGA_CONFIG)
}

export async function buscarProdutoLigaConfiguravel(
  url: string,
  config: ScraperSiteConfig = DEFAULT_LIGA_CONFIG,
): Promise<ProdutoLiga | null> {
  let browser

  try {
    browser = await chromium.launch({ headless: true })

    const page = await browser.newPage({ extraHTTPHeaders: HEADERS })
    await page.goto(url, { waitUntil: 'domcontentloaded' })

    const priceSelectors = config.fields.price?.selectors?.filter(Boolean) || [
      '.price',
    ]
    await page.waitForSelector(priceSelectors.join(', '), { timeout: 15000 })

    const html = await page.content()
    const $ = cheerio.load(html)
    const values = extractConfiguredData($, config, url)

    const nome =
      String(values.name || '').trim() ||
      $('div.item-name').first().text().trim() ||
      'Nao encontrado'

    const src = $('img#featuredImage').first().attr('src')
    const imagem =
      String(values.image || '').trim() ||
      (src
        ? src.startsWith('http')
          ? src
          : new URL(src, url).toString()
        : IMAGEM_PADRAO)

    const preco =
      String(values.price || '').trim() || $('.price').first().text().trim() || '0.00'

    return {
      imagem,
      nome,
      preco_atual: preco,
      origem: 'Liga Yugioh',
      link_site: url,
    }
  } catch (e) {
    console.error('Erro em buscarProdutoLiga:', e)
    return null
  } finally {
    if (browser) {
      await browser.close()
    }
  }
}
