import * as cheerio from 'cheerio'
import {  fetch } from '@tauri-apps/plugin-http'
import { logInfo, logError } from '../src/services/logger' // ajuste o caminho
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

export async function buscarCartaMyp(
  url: string,
  chave?: string,
): Promise<CartaMyP[]> {
  try {
    const response = await fetch(url, {
      headers: HEADERS, method: 'GET',
    })

    const html = await response.text()
    const $ = cheerio.load(html)

    const dados: CartaMyP[] = []

    // Nome
    const nomeTag = $('span.subtitulo').first()
    const nomeSemTag = $('h1#produto-nome').first()
    const nome =
      (nomeTag.text() || nomeSemTag.text() || 'Desconhecido').trim()

    // Imagem
    const imagens = $('img').toArray()
    const imagem =
      (imagens[2] && $(imagens[2]).attr('src')) || IMAGEM_PADRAO

    // Preço mínimo
    const precoTag = $('span.moeda').first()
    const precoMinimo = (precoTag.text() || 'R$ 0,00').trim()

    // Coleção
    const colecaoLinks = $('a[href*="/yugioh/"]').toArray()
    const colecaoCarta =
      (colecaoLinks[23] && $(colecaoLinks[23]).text().trim()) ||
      'Coleção não identificada'

    // Código
    let codigoCarta = 'Desconhecido'
    try {
      const partesPath = imagem.split('/')
      const pastaImagem =
        partesPath.length > 1
          ? partesPath[partesPath.length - 2]
          : ''
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

    // Tabela de raridades / preços
    const tabela = $('table.table.table-striped.table-bordered').first()
    const textoTabela = tabela.text()

    if (tabela.length && !textoTabela.includes('Nenhum resultado foi encontrado.')) {
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
            preco_atual: (preco.split('R$')[1] || precoMinimo.split('R$')[1] || '0,00').trim().replace(/\s+/g, ' ').replace(',','.'),
            codigo: codigoCarta.replace('_','-'),
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
        preco_atual: precoMinimo,
        codigo: codigoCarta,
        colecao: colecaoCarta,
        origem: 'MyPCards',
        link_site: url,
      })
    }

    logInfo(
      `DEBUG buscarCartaMyp – nome: ${nome}, registros: ${dados.length},coleção: ${colecaoCarta}
        .join(' | ')}`,
    )

    // Filtro por raridade
    if (chave) {
      const chaveLower = chave.toLowerCase()

      if (dados.length === 1) {
        logInfo(`Encontrada 1 carta em buscarCartaMyp: ${dados[0].nome}`)
        return [dados[0]]
      }

      const filtradas = dados.filter((item) =>
        item.raridade.toLowerCase().includes(chaveLower),
      )

      if (filtradas.length > 0) {
        logInfo(
          `Encontradas ${filtradas.length} cartas em buscarCartaMyp (filtradas por "${chaveLower}")`,
        )
        return filtradas
      }

      // Nenhuma raridade compatível → fallback
      logInfo(
        `Nenhuma carta com raridade contendo "${chaveLower}". Retornando primeiro resultado sem filtro.`,
      )
      return dados.length > 0 ? [dados[0]] : []
    }



    logInfo(`Encontradas ${dados.length} cartas em buscarCartaMyp: ${nome}`)
    return dados.length > 0 ? [dados[0]] : []
  } catch (e) {
    logError('Erro ao fazer a requisição buscar carta MyPCards:'+e)
    return []
  }
}


export async function buscarProdutoLiga(url: string): Promise<ProdutoLiga | null> {
  const result = await invoke<ProdutoLiga | null>('buscar_produto_liga_cmd', { url })
  return result
}