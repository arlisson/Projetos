import { invoke } from '@tauri-apps/api/core'

export type ClearDatabaseMode = 'operacional' | 'completo'

export interface DatabaseCounts {
  carta: number
  produto: number
  venda: number
  venda_produto: number
  historico_precos: number
  historico_lucro: number
  colecao: number
  raridade: number
  qualidade: number
}

export interface DatabaseInfo {
  dbPath: string
  exists: boolean
  fileSizeBytes: number
  fileSizeLabel: string
  lastModified: string
  counts: DatabaseCounts
}

export async function getDatabaseInfo(): Promise<DatabaseInfo> {
  return await invoke<DatabaseInfo>('get_database_info')
}

export async function exportDatabase(destinationPath: string): Promise<void> {
  await invoke('export_database', {
    destinationPath,
  })
}

export async function importDatabase(sourcePath: string): Promise<void> {
  await invoke('import_database', {
    sourcePath,
  })
}

export async function clearDatabaseData(
  mode: ClearDatabaseMode,
): Promise<void> {
  await invoke('clear_database_data', {
    mode,
  })
}