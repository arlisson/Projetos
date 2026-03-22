// src-tauri/src/lib.rs
mod log;
mod db_admin;

use std::process::Command as StdCommand;
use tauri::command;
use serde_json::Value;

#[command]
fn buscar_produto_liga_cmd(url: String) -> Result<Value, String> {
    let output = StdCommand::new("node")
        .current_dir("../scraping-server")
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
        .plugin(tauri_plugin_sql::Builder::default().build())
        .plugin(tauri_plugin_http::init())
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_fs::init())
        .invoke_handler(tauri::generate_handler![
            log::init_logs,
            log::log_info,
            log::log_error,
            log::read_logs,
            log::clear_logs,
            buscar_produto_liga_cmd,
            db_admin::get_database_info,
            db_admin::export_database,
            db_admin::import_database,
            db_admin::clear_database_data,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}