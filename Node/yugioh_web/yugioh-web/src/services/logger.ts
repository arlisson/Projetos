import { invoke } from '@tauri-apps/api/core'

export type LogItem = {
  level: 'INFO' | 'ERROR' | 'WARN' | 'DEBUG' | string
  message: string
  timestamp: string
  raw?: string
}

export async function initLogs() {
  try {
    await invoke('init_logs')
  } catch (e) {
    console.error(`Falha ao inicializar logs: ${e}`)
  }
}

export async function logInfo(message: string) {
  try {
    await invoke('log_info', { message })
  } catch (e) {
    console.error(`Falha ao registrar log de informação: ${e}`)
  }
}

export async function logError(message: string) {
  try {
    await invoke('log_error', { message })
  } catch (e) {
    console.error(`Falha ao registrar log de erro: ${e}`)
  }
}

export async function listarLogs(): Promise<LogItem[]> {
  try {
    const logs = await invoke<LogItem[]>('read_logs')
    return Array.isArray(logs) ? logs : []
  } catch (e) {
    console.error(`Falha ao ler logs: ${e}`)
    return []
  }
}

export async function limparLogs(): Promise<boolean> {
  try {
    await invoke('clear_logs')
    return true
  } catch (e) {
    console.error(`Falha ao limpar logs: ${e}`)
    return false
  }
}