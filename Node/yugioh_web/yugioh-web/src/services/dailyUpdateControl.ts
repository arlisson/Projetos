import { exists, mkdir, readTextFile, writeTextFile } from '@tauri-apps/plugin-fs'
import { appDataDir, join } from '@tauri-apps/api/path'
import { logError } from './logger'

const CONTROLE_DIR = 'controle'
const CONTROLE_FILE = 'atualizacao_diaria.json'

export interface ControleAtualizacaoDiaria {
  ultima_atualizacao: string | null
}

function hojeStr(): string {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

async function getControleFilePath(): Promise<string> {
  const baseDir = await appDataDir()
  const controlDir = await join(baseDir, CONTROLE_DIR)
  const controlFile = await join(controlDir, CONTROLE_FILE)

  const dirExists = await exists(controlDir)
  if (!dirExists) {
    await mkdir(controlDir, { recursive: true })
  }

  return controlFile
}

export async function lerControleAtualizacaoDiaria(): Promise<ControleAtualizacaoDiaria> {
  try {
    const filePath = await getControleFilePath()
    const fileExists = await exists(filePath)

    if (!fileExists) {
      const inicial: ControleAtualizacaoDiaria = {
        ultima_atualizacao: null,
      }

      await writeTextFile(filePath, JSON.stringify(inicial, null, 2))
      return inicial
    }

    const raw = await readTextFile(filePath)
    const parsed = JSON.parse(raw) as ControleAtualizacaoDiaria

    return {
      ultima_atualizacao: parsed?.ultima_atualizacao ?? null,
    }
  } catch (error) {
    await logError('Erro ao ler controle de atualização diária: ' + String(error))
    return {
      ultima_atualizacao: null,
    }
  }
}

export async function salvarControleAtualizacaoDiaria(
  data: string = hojeStr(),
): Promise<void> {
  try {
    const filePath = await getControleFilePath()

    const payload: ControleAtualizacaoDiaria = {
      ultima_atualizacao: data,
    }

    await writeTextFile(filePath, JSON.stringify(payload, null, 2))
  } catch (error) {
    await logError('Erro ao salvar controle de atualização diária: ' + String(error))
  }
}

export async function jaAtualizouHoje(): Promise<boolean> {
  const controle = await lerControleAtualizacaoDiaria()
  return controle.ultima_atualizacao === hojeStr()
}

export { hojeStr }