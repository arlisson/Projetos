import { invoke } from '@tauri-apps/api/core'

export async function initLogs() {
  try {
    await invoke('init_logs')
  } catch (e) {
    // await invoke('log_error', { message: `Falha ao inicializar logs: ${e}` })
    console.error(`Falha ao inicializar logs: ${e}`)
  }
}

export async function logInfo(message: string) {
  try {
    await invoke('log_info', { message })
  } catch (e) {
    // await invoke('log_error', { message: `Falha ao registrar log de informação: ${e}` })
    console.error(`Falha ao registrar log de informação: ${e}`)
  }
}

export async function logError(message: string) {
  try {
    await invoke('log_error', { message })
  } catch (e) {
    // await invoke('log_error', { message: `Falha ao registrar log de erro: ${e}` })
    console.error(`Falha ao registrar log de erro: ${e}`)
  }
}
