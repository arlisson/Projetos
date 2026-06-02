import { buscarProdutoLigaConfiguravel } from './buscarProdutoLiga'
import type { ScraperSiteConfig } from './configurableExtractor'
import { DEFAULT_LIGA_CONFIG } from './scraperDefaults'

async function main() {
  const url = process.argv[2]
  if (!url) {
    console.error('URL obrigatoria')
    process.exit(1)
  }

  let config: ScraperSiteConfig = DEFAULT_LIGA_CONFIG
  const configJson = process.argv[3]

  if (configJson) {
    try {
      config = JSON.parse(configJson) as ScraperSiteConfig
    } catch (e) {
      console.error('Configuracao do scraper invalida:', e)
      process.exit(1)
    }
  }

  try {
    const produto = await buscarProdutoLigaConfiguravel(url, config)
    console.log(JSON.stringify(produto ?? null))
  } catch (e) {
    console.error('Erro no scraping:', e)
    process.exit(1)
  }
}

void main()
