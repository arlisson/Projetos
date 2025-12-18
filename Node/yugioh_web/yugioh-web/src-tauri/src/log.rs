use std::{
    fs::{self, OpenOptions},
    io::Write,
    path::{Path, PathBuf},
    time::{Duration},
};

fn logs_dir() -> PathBuf {
    // Pasta "logs" ao lado do executável/projeto
    let mut dir = std::env::current_dir().unwrap_or_else(|_| PathBuf::from("."));
    dir.push("logs");
    if !dir.exists() {
        let _ = fs::create_dir_all(&dir);
    }
    dir
}

fn log_file_path(kind: &str) -> PathBuf {
    let mut path = logs_dir();
    match kind {
        "error" => path.push("error.log"),
        "info" => path.push("info.log"),
        _ => path.push("app.log"),
    }
    path
}

fn older_than_30_days(path: &Path) -> bool {
    if let Ok(meta) = fs::metadata(path) {
        if let Ok(modified) = meta.modified() {
            if let Ok(elapsed) = modified.elapsed() {
                return elapsed > Duration::from_secs(60 * 60 * 24 * 30);
            }
        }
    }
    false
}

fn append_line(path: &Path, level: &str, message: &str) -> Result<(), String> {
    let file = OpenOptions::new()
        .create(true)
        .append(true)
        .open(path)
        .map_err(|e| format!("Erro ao abrir arquivo de log: {e}"))?;

    let mut writer = std::io::BufWriter::new(file);

    // timestamp simples
    let now = chrono::Local::now().format("%Y-%m-%d %H:%M:%S").to_string();
    let line = format!("[{now}] [{level}] {message}\n");

    writer
        .write_all(line.as_bytes())
        .map_err(|e| format!("Erro ao escrever no log: {e}"))?;

    Ok(())
}

#[tauri::command]
pub fn init_logs() -> Result<(), String> {
    // error.log
    let error_path = log_file_path("error");
    if error_path.exists() && older_than_30_days(&error_path) {
        fs::remove_file(&error_path)
            .map_err(|e| format!("Erro ao remover error.log: {e}"))?;
    }

    // info.log
    let info_path = log_file_path("info");
    if info_path.exists() && older_than_30_days(&info_path) {
        fs::remove_file(&info_path)
            .map_err(|e| format!("Erro ao remover info.log: {e}"))?;
    }

    Ok(())
}

#[tauri::command]
pub fn log_info(message: String) -> Result<(), String> {
    let path = log_file_path("info");
    append_line(&path, "INFO", &message)
}

#[tauri::command]
pub fn log_error(message: String) -> Result<(), String> {
    let path = log_file_path("error");
    append_line(&path, "ERROR", &message)
}
