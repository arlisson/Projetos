// src-tauri/src/lib.rs
mod log;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        // plugin do banco (já existia)
        .plugin(
            tauri_plugin_sql::Builder::default()
                .build(),
            
        )
        // plugin HTTP (NOVO)
        .plugin(tauri_plugin_http::init())
        .invoke_handler(tauri::generate_handler![
            log::init_logs,
            log::log_info,
            log::log_error,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
