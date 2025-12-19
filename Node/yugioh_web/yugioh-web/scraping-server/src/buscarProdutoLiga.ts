// scraping-server/src/buscarProdutoLiga.ts
import * as cheerio from 'cheerio'
import { chromium } from 'playwright'

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
  let browser
  try {
    browser = await chromium.launch({ headless: true })

    const page = await browser.newPage({ extraHTTPHeaders: HEADERS })
    await page.goto(url, { waitUntil: 'domcontentloaded' })

    // Espera o JS renderizar o preço
    await page.waitForSelector('.price', { timeout: 15000 })

    const html = await page.content()
    const $ = cheerio.load(html)

    const produtos = $('div.item-name')
    const nome =
      produtos.length > 0 ? produtos.first().text().trim() : 'Não encontrado'

    const imagemEl = $('img#featuredImage').first()
    const src = imagemEl.attr('src')
    const imagem =
      src != null
        ? src.startsWith('http')
          ? src
          : `https:${src}`
        : IMAGEM_PADRAO

    let preco = $('.price').first().text().trim()
    if (!preco) preco = '0,00'
    
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
