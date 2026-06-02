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
import { parsePriceNumber } from '../utils/price'

export type DailyUpdateEtapa =
  | 'idle'
  | 'cartas'
  | 'produtos'
  | 'finalizado'
  | 'erro'

export type DailyUpdateScope = 'cartas' | 'produtos' | 'geral'

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
  mensagem: 'Atualizacao manual aguardando comando.',
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
    await logError(`Erro ao garantir diretorio de controle "${dir}": ${String(err)}`)
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
    await logError('Erro ao ler controle de atualizacao diaria: ' + String(err))
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
    await logError('Erro ao salvar controle de atualizacao diaria: ' + String(err))
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
  return parsePriceNumber(valor)
}

async function atualizarCartasEstoque(
  cartas: Awaited<ReturnType<typeof buscarCartasEmEstoque>>,
): Promise<void> {
  setStatus({
    etapa: 'cartas',
    atual: 0,
    total: cartas.length,
    nomeItemAtual: '',
    mensagem: 'Atualizando cartas...',
  })

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
            `Preco alterado para carta ${carta.nome} - ${carta.codigo ?? ''}: de ${String(precoAnterior)} para ${String(novoPreco)}`,
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
}

async function atualizarProdutosEstoque(
  produtos: Awaited<ReturnType<typeof buscarProdutosEmEstoque>>,
): Promise<void> {
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
            `Preco alterado para produto ${produto.nome_produto}: de ${String(precoAnterior)} para ${String(novoPreco)}`,
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
}

async function runDailyUpdate(
  scope: DailyUpdateScope = 'geral',
): Promise<DailyUpdateStatus> {
  const controle = await lerControleAtualizacao()

  setStatus({
    ultimaAtualizacao: controle.ultima_atualizacao,
  })

  const cartas = await buscarCartasEmEstoque()
  const produtos = await buscarProdutosEmEstoque()
  const deveAtualizarCartas = scope === 'cartas' || scope === 'geral'
  const deveAtualizarProdutos = scope === 'produtos' || scope === 'geral'

  setStatus({
    executando: true,
    etapa: deveAtualizarCartas ? 'cartas' : 'produtos',
    mensagem:
      scope === 'cartas'
        ? 'Iniciando atualizacao de cartas...'
        : scope === 'produtos'
          ? 'Iniciando atualizacao de produtos...'
          : 'Iniciando atualizacao geral de precos...',
    atual: 0,
    total: deveAtualizarCartas ? cartas.length : produtos.length,
    nomeItemAtual: '',
    totalCartas: deveAtualizarCartas ? cartas.length : 0,
    totalProdutos: deveAtualizarProdutos ? produtos.length : 0,
    cartasAtualizadas: 0,
    produtosAtualizados: 0,
  })

  try {
    if (deveAtualizarCartas) {
      await atualizarCartasEstoque(cartas)
    }

    if (deveAtualizarProdutos) {
      await atualizarProdutosEstoque(produtos)
    }

    await registrarHistoricoLucro()

    if (scope === 'geral') {
      await salvarControleAtualizacao(todayStr())
    }

    setStatus({
      executando: false,
      etapa: 'finalizado',
      mensagem:
        scope === 'cartas'
          ? 'Atualizacao de cartas concluida com sucesso.'
          : scope === 'produtos'
            ? 'Atualizacao de produtos concluida com sucesso.'
            : 'Atualizacao geral concluida com sucesso.',
      atual: 0,
      total: 0,
      nomeItemAtual: '',
      ultimaAtualizacao:
        scope === 'geral' ? todayStr() : controle.ultima_atualizacao,
    })

    return getDailyUpdateStatus()
  } catch (err) {
    await logError('Erro geral ao atualizar precos e lucros: ' + String(err))

    setStatus({
      executando: false,
      etapa: 'erro',
      mensagem: 'Erro ao atualizar precos.',
    })

    return getDailyUpdateStatus()
  } finally {
    runningPromise = null
  }
}

export async function iniciarAtualizacaoDiaria(
  scope: DailyUpdateScope = 'geral',
): Promise<DailyUpdateStatus> {
  if (runningPromise) {
    return runningPromise
  }

  if (currentStatus.executando) {
    return getDailyUpdateStatus()
  }

  runningPromise = runDailyUpdate(scope)
  return runningPromise
}
