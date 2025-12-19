// src-tauri/src/lib.rs
mod log;

use std::process::Command as StdCommand;
use tauri::command;
use serde_json::Value;

#[command]
fn buscar_produto_liga_cmd(url: String) -> Result<Value, String> {
    // Ajuste o caminho conforme a estrutura do seu projeto.
    // Aqui estou assumindo que o binário roda em `src-tauri/target/...`
    // e que `scraping-server` está na raiz do projeto ao lado de `src-tauri`.
    let output = StdCommand::new("node")
        .current_dir("../scraping-server") // ajuste se necessário
        .arg("dist/cli.js")
        .arg(&url)
        .output()
        .map_err(|e| format!("Erro ao executar Node: {e}"))?;

    if !output.status.success() {
        let stderr = String::from_utf8_lossy(&output.stderr);
        return Err(format!("Node retornou erro: {stderr}"));
    }

    let stdout = String::from_utf8_lossy(&output.stdout);
    let json: Value = serde_json::from_str(&stdout)
        .map_err(|e| format!("Erro ao parsear JSON: {e}\nSaída: {stdout}"))?;

    Ok(json)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        // plugin do banco
        .plugin(
            tauri_plugin_sql::Builder::default()
                .build(),
        )
        // plugin HTTP (se você ainda usa em outras partes da app)
        .plugin(tauri_plugin_http::init())
        .invoke_handler(tauri::generate_handler![
            log::init_logs,
            log::log_info,
            log::log_error,
            buscar_produto_liga_cmd,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
