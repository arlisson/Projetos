import * as cheerio from 'cheerio'
import { fetch } from '@tauri-apps/plugin-http'
import { logInfo, logError } from '../src/services/logger'
import { invoke } from '@tauri-apps/api/core'

const HEADERS = {
  'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}

const IMAGEM_PADRAO =
  'https://i.pinimg.com/736x/71/1e/da/711eda25308c65a7756751088866e181.jpg'

export interface CartaMyP {
  imagem: string
  nome: string
  raridade: string
  preco_atual: string
  codigo: string
  colecao: string
  origem: string
  link_site: string
}

export interface ProdutoLiga {
  imagem: string
  nome: string
  preco_atual: string
  origem: string
  link_site: string
}

function normalizarPreco(valor?: string): string {
  if (!valor) return '0.00'

  return valor
    .replace(/\s+/g, ' ')
    .replace('R$', '')
    .replace(/\./g, '')
    .replace(',', '.')
    .trim()
}

function setPage(url: string, page: number): string {
  const parsed = new URL(url)
  parsed.searchParams.set('page', String(page))
  return parsed.toString()
}

function toAbsoluteUrl(base: string, href: string): string {
  try {
    return new URL(href, base).toString()
  } catch {
    return href
  }
}

export async function buscarCartaMyp(
  url: string,
  chave?: string,
): Promise<CartaMyP[]> {
  try {
    const response = await fetch(url, {
      headers: HEADERS,
      method: 'GET',
    })

    const html = await response.text()
    const $ = cheerio.load(html)

    const dados: CartaMyP[] = []

    const nomeTag = $('span.subtitulo').first()
    const nomeSemTag = $('h1#produto-nome').first()
    const nome =
      (nomeTag.text() || nomeSemTag.text() || 'Desconhecido').trim()

    const imagens = $('img').toArray()
    const imagem =
      (imagens[2] && $(imagens[2]).attr('src')) || IMAGEM_PADRAO

    const precoTag = $('span.moeda').first()
    const precoMinimo = (precoTag.text() || 'R$ 0,00').trim()

    const colecaoLinks = $('a[href*="/yugioh/"]').toArray()
    const colecaoCarta =
      (colecaoLinks[23] && $(colecaoLinks[23]).text().trim()) ||
      'Coleção não identificada'

    let codigoCarta = 'Desconhecido'

    try {
      const partesPath = imagem.split('/')
      const pastaImagem =
        partesPath.length > 1 ? partesPath[partesPath.length - 2] : ''

      const partesCodigo = pastaImagem.split('_').slice(1)
      const codigoPorImagem = partesCodigo.join('_')

      if (codigoPorImagem) {
        codigoCarta = codigoPorImagem
      } else {
        const viewFields = $('div.view-field').toArray()
        if (viewFields[3]) {
          const textoCampo = $(viewFields[3]).text().trim()
          const aposCodigo = textoCampo.split('Código').pop() ?? ''
          const limpo = aposCodigo.trim().split('yugioh_').pop() ?? ''
          if (limpo) {
            codigoCarta = limpo
          }
        }
      }
    } catch {
      codigoCarta = 'Desconhecido'
    }

    const tabela = $('table.table.table-striped.table-bordered').first()
    const textoTabela = tabela.text()

    if (
      tabela.length &&
      !textoTabela.includes('Nenhum resultado foi encontrado.')
    ) {
      tabela.find('tr').each((_, tr) => {
        const cols = $(tr).find('td').toArray()
        const valores = cols.map((td) => $(td).text().trim())

        if (valores.length >= 5) {
          const raridade = valores[1].split(',')[0]
          const preco = valores[4]

          dados.push({
            imagem: imagem || IMAGEM_PADRAO,
            nome,
            raridade,
            preco_atual: normalizarPreco(preco || precoMinimo),
            codigo: codigoCarta.replace(/_/g, '-'),
            colecao: colecaoCarta,
            origem: 'MyPCards',
            link_site: url,
          })
        }
      })
    } else {
      dados.push({
        imagem: imagem || IMAGEM_PADRAO,
        nome,
        raridade: 'Não encontrado',
        preco_atual: normalizarPreco(precoMinimo),
        codigo: codigoCarta.replace(/_/g, '-'),
        colecao: colecaoCarta,
        origem: 'MyPCards',
        link_site: url,
      })
    }

    logInfo(
      `buscarCartaMyp -> nome=${nome}, registros=${dados.length}, colecao=${colecaoCarta}`,
    )

    if (chave) {
      const chaveLower = chave.toLowerCase()

      if (dados.length === 1) {
        return [dados[0]]
      }

      const filtradas = dados.filter((item) =>
        item.raridade.toLowerCase().includes(chaveLower),
      )

      if (filtradas.length > 0) {
        return filtradas
      }

      return dados.length > 0 ? [dados[0]] : []
    }

    return dados.length > 0 ? [dados[0]] : []
  } catch (e) {
    logError(`Erro ao fazer a requisição buscarCartaMyp: ${String(e)}`)
    return []
  }
}

export async function buscarCartasColecao(
  url: string,
): Promise<CartaMyP[]> {
  try {
    const base = 'https://mypcards.com'
    const linksColetados: string[] = []
    const vistos = new Set<string>()
    const cartas: CartaMyP[] = []

    const ajaxHeaders = {
      ...HEADERS,
      'X-Requested-With': 'XMLHttpRequest',
      Accept: 'text/html, */*;q=0.1',
    }

    let page = 1
    const maxPages = 200

    while (page <= maxPages) {
      const pageUrl = setPage(url, page)
      logInfo(`Carregando coleção: page=${page} -> ${pageUrl}`)

      const response = await fetch(pageUrl, {
        method: 'GET',
        headers: ajaxHeaders,
      })

      if (!response.ok) {
        logInfo(`Parando paginação: status=${response.status} em page=${page}`)
        break
      }

      const html = await response.text()
      const $ = cheerio.load(html)
      const itens = $('a.card-img-link').toArray()

      if (!itens.length) {
        logInfo(`Nenhuma carta encontrada em page=${page}. Encerrando.`)
        break
      }

      let novos = 0

      for (const item of itens) {
        const href = ($(item).attr('href') || '').trim()

        if (!href) continue
        if (href.toLowerCase().includes('outros')) continue

        const linkCompleto = toAbsoluteUrl(base, href)

        if (vistos.has(linkCompleto)) continue

        vistos.add(linkCompleto)
        linksColetados.push(linkCompleto)
        novos += 1
      }

      logInfo(
        `page=${page}: itens=${itens.length}, novos=${novos}, total=${linksColetados.length}`,
      )

      if (novos === 0) {
        logInfo(
          `Página ${page} não trouxe links novos. Encerrando paginação para evitar loop.`,
        )
        break
      }

      page += 1
    }

    for (const link of linksColetados) {
      try {
        const resultado = await buscarCartaMyp(link)
        if (resultado.length > 0) {
          cartas.push(resultado[0])
        }
      } catch (e) {
        logError(`Erro ao buscar carta da coleção em ${link}: ${String(e)}`)
      }
    }

    logInfo(
      `Total de cartas encontradas em buscarCartasColecao: ${cartas.length}`,
    )

    return cartas
  } catch (e) {
    logError(`Erro ao fazer a requisição em buscarCartasColecao: ${String(e)}`)
    return []
  }
}

export async function buscarProdutoLiga(
  url: string,
): Promise<ProdutoLiga | null> {
  const result = await invoke<ProdutoLiga | null>('buscar_produto_liga_cmd', {
    url,
  })
  return result
}