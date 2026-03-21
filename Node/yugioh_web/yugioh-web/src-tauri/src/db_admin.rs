use serde::Serialize;
use std::{
    fs,
    path::{PathBuf},
};
use tauri::{AppHandle, Manager};

#[derive(Serialize)]
pub struct DatabaseCounts {
    pub carta: i64,
    pub produto: i64,
    pub venda: i64,
    pub venda_produto: i64,
    pub historico_precos: i64,
    pub historico_lucro: i64,
    pub colecao: i64,
    pub raridade: i64,
    pub qualidade: i64,
}

#[derive(Serialize)]
pub struct DatabaseInfo {
    #[serde(rename = "dbPath")]
    pub db_path: String,
    pub exists: bool,
    #[serde(rename = "fileSizeBytes")]
    pub file_size_bytes: u64,
    #[serde(rename = "fileSizeLabel")]
    pub file_size_label: String,
    #[serde(rename = "lastModified")]
    pub last_modified: String,
    pub counts: DatabaseCounts,
}

fn db_path(app: &AppHandle) -> Result<PathBuf, String> {
    let app_data_dir = app
        .path()
        .app_data_dir()
        .map_err(|e| format!("Erro ao obter app_data_dir: {e}"))?;

    if !app_data_dir.exists() {
        fs::create_dir_all(&app_data_dir)
            .map_err(|e| format!("Erro ao criar diretório de dados da aplicação: {e}"))?;
    }

    Ok(app_data_dir.join("yugioh.db"))
}

fn format_file_size(bytes: u64) -> String {
    const KB: f64 = 1024.0;
    const MB: f64 = 1024.0 * 1024.0;
    const GB: f64 = 1024.0 * 1024.0 * 1024.0;

    let b = bytes as f64;

    if b >= GB {
        format!("{:.2} GB", b / GB)
    } else if b >= MB {
        format!("{:.2} MB", b / MB)
    } else if b >= KB {
        format!("{:.2} KB", b / KB)
    } else {
        format!("{} B", bytes)
    }
}

fn format_modified_time(meta: &fs::Metadata) -> String {
    match meta.modified() {
        Ok(time) => {
            let dt: chrono::DateTime<chrono::Local> = time.into();
            dt.format("%Y-%m-%d %H:%M:%S").to_string()
        }
        Err(_) => String::new(),
    }
}

fn count_table(conn: &rusqlite::Connection, table: &str) -> Result<i64, String> {
    let sql = format!("SELECT COUNT(*) FROM {table}");
    conn.query_row(&sql, [], |row| row.get::<_, i64>(0))
        .map_err(|e| format!("Erro ao contar tabela {table}: {e}"))
}

#[tauri::command]
pub fn get_database_info(app: AppHandle) -> Result<DatabaseInfo, String> {
    let path = db_path(&app)?;
    let exists = path.exists();

    let (file_size_bytes, file_size_label, last_modified) = if exists {
        let meta = fs::metadata(&path)
            .map_err(|e| format!("Erro ao ler metadados do banco: {e}"))?;

        let bytes = meta.len();
        (bytes, format_file_size(bytes), format_modified_time(&meta))
    } else {
        (0, String::from("0 B"), String::new())
    };

    let counts = if exists {
        let conn = rusqlite::Connection::open(&path)
            .map_err(|e| format!("Erro ao abrir banco para leitura: {e}"))?;

        DatabaseCounts {
            carta: count_table(&conn, "carta")?,
            produto: count_table(&conn, "produto")?,
            venda: count_table(&conn, "venda")?,
            venda_produto: count_table(&conn, "venda_produto")?,
            historico_precos: count_table(&conn, "historico_precos")?,
            historico_lucro: count_table(&conn, "historico_lucro")?,
            colecao: count_table(&conn, "colecao")?,
            raridade: count_table(&conn, "raridade")?,
            qualidade: count_table(&conn, "qualidade")?,
        }
    } else {
        DatabaseCounts {
            carta: 0,
            produto: 0,
            venda: 0,
            venda_produto: 0,
            historico_precos: 0,
            historico_lucro: 0,
            colecao: 0,
            raridade: 0,
            qualidade: 0,
        }
    };

    Ok(DatabaseInfo {
        db_path: path.display().to_string(),
        exists,
        file_size_bytes,
        file_size_label,
        last_modified,
        counts,
    })
}

#[tauri::command]
pub fn export_database(app: AppHandle, destination_path: String) -> Result<(), String> {
    let source = db_path(&app)?;

    if !source.exists() {
        return Err("Banco atual não foi encontrado.".to_string());
    }

    let dest = PathBuf::from(destination_path.trim());
    if dest.as_os_str().is_empty() {
        return Err("Destino da exportação não informado.".to_string());
    }

    if let Some(parent) = dest.parent() {
        if !parent.exists() {
            fs::create_dir_all(parent)
                .map_err(|e| format!("Erro ao criar diretório de destino: {e}"))?;
        }
    }

    fs::copy(&source, &dest)
        .map_err(|e| format!("Erro ao exportar banco: {e}"))?;

    Ok(())
}

#[tauri::command]
pub fn import_database(app: AppHandle, source_path: String) -> Result<(), String> {
    let source = PathBuf::from(source_path.trim());

    if source.as_os_str().is_empty() {
        return Err("Arquivo de origem não informado.".to_string());
    }

    if !source.exists() {
        return Err("Arquivo de origem não encontrado.".to_string());
    }

    let dest = db_path(&app)?;

    if let Some(parent) = dest.parent() {
        if !parent.exists() {
            fs::create_dir_all(parent)
                .map_err(|e| format!("Erro ao preparar diretório do banco: {e}"))?;
        }
    }

    fs::copy(&source, &dest)
        .map_err(|e| format!("Erro ao importar banco: {e}"))?;

    Ok(())
}

#[tauri::command]
pub fn clear_database_data(app: AppHandle, mode: String) -> Result<(), String> {
    let path = db_path(&app)?;

    if !path.exists() {
        return Err("Banco atual não foi encontrado.".to_string());
    }

    let mut conn = rusqlite::Connection::open(&path)
        .map_err(|e| format!("Erro ao abrir banco: {e}"))?;

    let tx = conn
        .transaction()
        .map_err(|e| format!("Erro ao iniciar transação: {e}"))?;

    tx.execute("DELETE FROM historico_precos", [])
        .map_err(|e| format!("Erro ao limpar historico_precos: {e}"))?;
    tx.execute("DELETE FROM historico_lucro", [])
        .map_err(|e| format!("Erro ao limpar historico_lucro: {e}"))?;
    tx.execute("DELETE FROM venda_produto", [])
        .map_err(|e| format!("Erro ao limpar venda_produto: {e}"))?;
    tx.execute("DELETE FROM venda", [])
        .map_err(|e| format!("Erro ao limpar venda: {e}"))?;
    tx.execute("DELETE FROM carta", [])
        .map_err(|e| format!("Erro ao limpar carta: {e}"))?;
    tx.execute("DELETE FROM produto", [])
        .map_err(|e| format!("Erro ao limpar produto: {e}"))?;

    if mode == "completo" {
        tx.execute("DELETE FROM colecao", [])
            .map_err(|e| format!("Erro ao limpar colecao: {e}"))?;
        tx.execute("DELETE FROM raridade", [])
            .map_err(|e| format!("Erro ao limpar raridade: {e}"))?;
        tx.execute("DELETE FROM qualidade", [])
            .map_err(|e| format!("Erro ao limpar qualidade: {e}"))?;
    }

    tx.execute(
        "DELETE FROM sqlite_sequence WHERE name IN (
            'historico_precos',
            'historico_lucro',
            'venda_produto',
            'venda',
            'carta',
            'produto',
            'colecao',
            'raridade',
            'qualidade'
        )",
        [],
    )
    .map_err(|e| format!("Erro ao limpar sequências: {e}"))?;

    tx.commit()
        .map_err(|e| format!("Erro ao finalizar transação: {e}"))?;

    Ok(())
}