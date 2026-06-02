import type { ScraperSiteConfig } from './configurableExtractor'

export const DEFAULT_LIGA_CONFIG: ScraperSiteConfig = {
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
  },
}
