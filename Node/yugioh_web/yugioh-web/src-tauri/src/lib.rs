// src-tauri/src/lib.rs
mod log; // se você tiver o módulo de logs (logging.rs -> log.rs, por exemplo)

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(
            tauri_plugin_sql::Builder::default()
                .build(),
        )
        .invoke_handler(tauri::generate_handler![
            log::init_logs,
            log::log_info,
            log::log_error,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
