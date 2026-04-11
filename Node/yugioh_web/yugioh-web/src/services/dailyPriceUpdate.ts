import { exists, mkdir, readTextFile, writeTextFile } from '@tauri-apps/plugin-fs'
import { join, appDataDir } from '@tauri-apps/api/path'
import {
  buscarCartasEmEstoque,
  buscarProdutosEmEstoque,
  atualizarPrecoCartaPorScraping,
  atualizarPrecoProdutoPorScraping,
  registrarHistoricoLucro,
  todayStr,
} from '../Database/db'
import { buscarCartaMyp, buscarProdutoLiga } from '../../scraping/webScraping'
import { logError, logInfo } from './logger'

export type DailyUpdateEtapa =
  | 'idle'
  | 'cartas'
  | 'produtos'
  | 'finalizado'
  | 'erro'

export interface DailyUpdateStatus {
  executando: boolean
  etapa: DailyUpdateEtapa
  mensagem: string
  atual: number
  total: number
  nomeItemAtual: string
  totalCartas: number
  totalProdutos: number
  cartasAtualizadas: number
  produtosAtualizados: number
  ultimaAtualizacao?: string | null
}

interface ControleAtualizacaoJson {
  ultima_atualizacao: string | null
}

const CONTROLE_DIR = 'controle'
const CONTROLE_ARQUIVO = 'atualizacao_diaria.json'

let currentStatus: DailyUpdateStatus = {
  executando: false,
  etapa: 'idle',
  mensagem: 'Aguardando verificação diária.',
  atual: 0,
  total: 0,
  nomeItemAtual: '',
  totalCartas: 0,
  totalProdutos: 0,
  cartasAtualizadas: 0,
  produtosAtualizados: 0,
  ultimaAtualizacao: null,
}

let runningPromise: Promise<DailyUpdateStatus> | null = null
const listeners = new Set<(status: DailyUpdateStatus) => void>()

function emitStatus() {
  for (const listener of listeners) {
    try {
      listener({ ...currentStatus })
    } catch {
      //
    }
  }
}

function setStatus(partial: Partial<DailyUpdateStatus>) {
  currentStatus = {
    ...currentStatus,
    ...partial,
  }
  emitStatus()
}

export function getDailyUpdateStatus(): DailyUpdateStatus {
  return { ...currentStatus }
}

export function subscribeDailyUpdateStatus(
  listener: (status: DailyUpdateStatus) => void,
): () => void {
  listeners.add(listener)
  listener({ ...currentStatus })

  return () => {
    listeners.delete(listener)
  }
}

async function getControlePath(): Promise<string> {
  const base = await appDataDir()
  const dir = await join(base, CONTROLE_DIR)

  try {
    const dirExiste = await exists(dir)
    if (!dirExiste) {
      await mkdir(dir, { recursive: true })
    }
  } catch (err) {
    await logError(`Erro ao garantir diretório de controle "${dir}": ${String(err)}`)
    throw err
  }

  return await join(dir, CONTROLE_ARQUIVO)
}

export async function lerControleAtualizacao(): Promise<ControleAtualizacaoJson> {
  try {
    const path = await getControlePath()
    const arquivoExiste = await exists(path)

    if (!arquivoExiste) {
      const inicial: ControleAtualizacaoJson = { ultima_atualizacao: null }
      await writeTextFile(path, JSON.stringify(inicial, null, 2))
      return inicial
    }

    const raw = await readTextFile(path)
    const parsed = JSON.parse(raw) as ControleAtualizacaoJson

    return {
      ultima_atualizacao: parsed?.ultima_atualizacao ?? null,
    }
  } catch (err) {
    await logError('Erro ao ler controle de atualização diária: ' + String(err))
    return { ultima_atualizacao: null }
  }
}

export async function salvarControleAtualizacao(data: string): Promise<void> {
  try {
    const path = await getControlePath()
    const payload: ControleAtualizacaoJson = {
      ultima_atualizacao: data,
    }
    await writeTextFile(path, JSON.stringify(payload, null, 2))
  } catch (err) {
    await logError('Erro ao salvar controle de atualização diária: ' + String(err))
  }
}

export async function jaAtualizadoHoje(): Promise<boolean> {
  const controle = await lerControleAtualizacao()
  return controle.ultima_atualizacao === todayStr()
}

function normalizarNumeroCarta(valor: string | number): number {
  if (typeof valor === 'number') {
    return Number.isFinite(valor) ? valor : 0
  }

  let texto = String(valor || '').trim()

  if (!texto) return 0

  texto = texto.replace(/\s+/g, '')

  const temVirgula = texto.includes(',')
  const temPonto = texto.includes('.')

  if (temVirgula && temPonto) {
    if (texto.lastIndexOf(',') > texto.lastIndexOf('.')) {
      texto = texto.replace(/\./g, '').replace(',', '.')
    } else {
      texto = texto.replace(/,/g, '')
    }
  } else if (temVirgula) {
    texto = texto.replace(',', '.')
  }

  const numero = Number(texto)
  return Number.isFinite(numero) ? numero : 0
}

function normalizarNumeroProduto(valor: string | number): number {
  if (typeof valor === 'number') {
    return Number.isFinite(valor) ? valor : 0
  }

  const texto = String(valor || '').trim()

  if (!texto) return 0

  const valoresComRS = [
    ...texto.matchAll(/R\$\s*(\d{1,3}(?:\.\d{3})*,\d{2}|\d+(?:[.,]\d{2})?)/g),
  ].map((m) => m[1])

  if (valoresComRS.length > 0) {
    const escolhido =
      valoresComRS.length >= 2
        ? valoresComRS[1]
        : valoresComRS[valoresComRS.length - 1]

    const numero = Number(escolhido.replace(/\./g, '').replace(',', '.'))
    return Number.isFinite(numero) ? numero : 0
  }

  const matches = texto.match(
    /\d{1,3}(?:\.\d{3})*,\d{2}|\d+(?:[.,]\d{2})?/g,
  )

  if (!matches || matches.length === 0) {
    return 0
  }

  const escolhido = matches.length >= 2 ? matches[1] : matches[0]
  const numero = Number(escolhido.replace(/\./g, '').replace(',', '.'))

  return Number.isFinite(numero) ? numero : 0
}

async function runDailyUpdate(): Promise<DailyUpdateStatus> {
  const controle = await lerControleAtualizacao()

  setStatus({
    ultimaAtualizacao: controle.ultima_atualizacao,
  })

  if (controle.ultima_atualizacao === todayStr()) {
    setStatus({
      executando: false,
      etapa: 'finalizado',
      mensagem: 'Preços já atualizados hoje.',
      atual: 0,
      total: 0,
      nomeItemAtual: '',
    })
    return getDailyUpdateStatus()
  }

  const cartas = await buscarCartasEmEstoque()
  const produtos = await buscarProdutosEmEstoque()

  setStatus({
    executando: true,
    etapa: 'cartas',
    mensagem: 'Iniciando atualização diária...',
    atual: 0,
    total: cartas.length,
    nomeItemAtual: '',
    totalCartas: cartas.length,
    totalProdutos: produtos.length,
    cartasAtualizadas: 0,
    produtosAtualizados: 0,
  })

  try {
    for (let i = 0; i < cartas.length; i++) {
      const carta = cartas[i]

      setStatus({
        etapa: 'cartas',
        atual: i + 1,
        total: cartas.length,
        nomeItemAtual: carta.nome,
        mensagem: `Atualizando carta ${i + 1}/${cartas.length}: ${carta.nome}`,
      })

      if (!carta.id_carta || !carta.link_site) {
        setStatus({ cartasAtualizadas: i + 1 })
        continue
      }

      try {
        const retorno = await buscarCartaMyp(
          carta.link_site,
          carta.raridade_nome || undefined,
        )
        const primeira = retorno?.[0]

        if (primeira) {
          const novoPreco = normalizarNumeroCarta(primeira.preco_atual)
          const precoAnterior = carta.preco_atual ?? null

          await atualizarPrecoCartaPorScraping(
            carta.id_carta,
            novoPreco,
            todayStr(),
            'MyPCards',
          )

          if (precoAnterior !== novoPreco) {
            await logInfo(
              `Preço alterado para carta ${carta.nome} - ${carta.codigo ?? ''}: de ${String(precoAnterior)} para ${String(novoPreco)}`,
            )
          }
        }
      } catch (err) {
        await logError(`Erro ao atualizar carta ID ${carta.id_carta}: ${String(err)}`)
      }

      setStatus({
        cartasAtualizadas: i + 1,
      })

      await new Promise((resolve) => setTimeout(resolve, 30))
    }

    setStatus({
      etapa: 'produtos',
      atual: 0,
      total: produtos.length,
      nomeItemAtual: '',
      mensagem: 'Atualizando produtos...',
    })

    for (let i = 0; i < produtos.length; i++) {
      const produto = produtos[i]

      setStatus({
        etapa: 'produtos',
        atual: i + 1,
        total: produtos.length,
        nomeItemAtual: produto.nome_produto,
        mensagem: `Atualizando produto ${i + 1}/${produtos.length}: ${produto.nome_produto}`,
      })

      if (!produto.id_produto || !produto.link) {
        setStatus({ produtosAtualizados: i + 1 })
        continue
      }

      try {
        const retorno = await buscarProdutoLiga(produto.link)

        if (retorno) {
          const novoPreco = normalizarNumeroProduto(retorno.preco_atual)
          const precoAnterior = produto.preco_atual ?? null

          await atualizarPrecoProdutoPorScraping(
            produto.id_produto,
            novoPreco,
            todayStr(),
            'Liga Yugioh',
          )

          if (precoAnterior !== novoPreco) {
            await logInfo(
              `Preço alterado para produto ${produto.nome_produto}: de ${String(precoAnterior)} para ${String(novoPreco)}`,
            )
          }
        }
      } catch (err) {
        await logError(`Erro ao atualizar produto ID ${produto.id_produto}: ${String(err)}`)
      }

      setStatus({
        produtosAtualizados: i + 1,
      })

      await new Promise((resolve) => setTimeout(resolve, 30))
    }

    await registrarHistoricoLucro()
    await salvarControleAtualizacao(todayStr())

    setStatus({
      executando: false,
      etapa: 'finalizado',
      mensagem: 'Atualização concluída com sucesso.',
      atual: 0,
      total: 0,
      nomeItemAtual: '',
      ultimaAtualizacao: todayStr(),
    })

    return getDailyUpdateStatus()
  } catch (err) {
    await logError('Erro geral ao atualizar preços e lucros: ' + String(err))

    setStatus({
      executando: false,
      etapa: 'erro',
      mensagem: 'Erro ao atualizar preços.',
    })

    return getDailyUpdateStatus()
  } finally {
    runningPromise = null
  }
}

export async function iniciarAtualizacaoDiaria(): Promise<DailyUpdateStatus> {
  if (runningPromise) {
    return runningPromise
  }

  if (currentStatus.executando) {
    return getDailyUpdateStatus()
  }

  runningPromise = runDailyUpdate()
  return runningPromise
}