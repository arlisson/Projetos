import type { ScraperSite, ScraperSiteConfig } from './configurableExtractor'

export const DEFAULT_SCRAPER_CONFIGS: Record<ScraperSite, ScraperSiteConfig> = {
  mypcards: {
    site: 'mypcards',
    label: 'MYPCards',
    baseUrl: 'https://mypcards.com',
    fields: {
      name: {
        selectors: ['span.subtitulo', 'h1#produto-nome'],
        attribute: 'text',
        index: 1,
        transform: 'text',
        fallback: 'Desconhecido',
        active: true,
      },
      price: {
        selectors: ['span.moeda'],
        attribute: 'text',
        index: 1,
        transform: 'currency-brl',
        fallback: '0.00',
        active: true,
      },
      image: {
        selectors: ['img[src*="/storage/"]', '.produto-imagem img', 'img'],
        attribute: 'src',
        index: 1,
        transform: 'absolute-url',
        fallback:
          'https://i.pinimg.com/736x/71/1e/da/711eda25308c65a7756751088866e181.jpg',
        active: true,
      },
      collection: {
        selectors: ['a[href*="/yugioh/"]'],
        attribute: 'text',
        index: 1,
        transform: 'text',
        fallback: 'Colecao nao identificada',
        active: true,
      },
      rarity: {
        selectors: ['table.table.table-striped.table-bordered tbody tr td:nth-child(2)'],
        attribute: 'text',
        index: 1,
        transform: 'text',
        fallback: 'Nao encontrado',
        active: true,
      },
      link: {
        selectors: ['link[rel="canonical"]'],
        attribute: 'href',
        index: 1,
        transform: 'absolute-url',
        fallback: null,
        active: true,
      },
    },
  },
  ligayugioh: {
    site: 'ligayugioh',
    label: 'LigaYugioh',
    baseUrl: 'https://www.ligayugioh.com.br',
    fields: {
      name: {
        selectors: ['div.item-name', 'h1', '.product-title'],
        attribute: 'text',
        index: 1,
        transform: 'text',
        fallback: 'Nao encontrado',
        active: true,
      },
      price: {
        selectors: ['.price', '.product-price', '[data-price]'],
        attribute: 'text',
        index: 1,
        transform: 'currency-brl',
        fallback: '0.00',
        active: true,
      },
      image: {
        selectors: ['img#featuredImage', '.card-image img', '.product-image img'],
        attribute: 'src',
        index: 1,
        transform: 'absolute-url',
        fallback:
          'https://i.pinimg.com/736x/71/1e/da/711eda25308c65a7756751088866e181.jpg',
        active: true,
      },
      link: {
        selectors: ['link[rel="canonical"]'],
        attribute: 'href',
        index: 1,
        transform: 'absolute-url',
        fallback: null,
        active: true,
      },
      availability: {
        selectors: ['.availability', '.stock', '[data-stock]'],
        attribute: 'text',
        index: 1,
        transform: 'text',
        fallback: null,
        active: false,
      },
    },
  },
}

export function getDefaultScraperConfig(site: ScraperSite): ScraperSiteConfig {
  return structuredClone(DEFAULT_SCRAPER_CONFIGS[site])
}
