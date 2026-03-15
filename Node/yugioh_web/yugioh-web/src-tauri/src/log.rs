use serde::Serialize;
use std::{
    fs::{self, OpenOptions},
    io::Write,
    path::{Path, PathBuf},
    time::Duration,
};

#[derive(Serialize)]
pub struct LogItem {
    pub level: String,
    pub message: String,
    pub timestamp: String,
    pub raw: String,
    pub source: String,
}

fn logs_dir() -> PathBuf {
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

    let now = chrono::Local::now().format("%Y-%m-%d %H:%M:%S").to_string();
    let line = format!("[{now}] [{level}] {message}\n");

    writer
        .write_all(line.as_bytes())
        .map_err(|e| format!("Erro ao escrever no log: {e}"))?;

    Ok(())
}

fn parse_log_line(line: &str, source: &str) -> LogItem {
    let raw = line.to_string();
    let mut timestamp = String::new();
    let mut level = String::from("INFO");
    let mut message = raw.clone();

    if line.starts_with('[') {
        if let Some(first_close) = line.find(']') {
            timestamp = line[1..first_close].to_string();

            let rest = line[first_close + 1..].trim();
            if rest.starts_with('[') {
                if let Some(second_close) = rest.find(']') {
                    level = rest[1..second_close].to_string();
                    message = rest[second_close + 1..].trim().to_string();
                }
            }
        }
    }

    LogItem {
        level,
        message,
        timestamp,
        raw,
        source: source.to_string(),
    }
}

fn read_log_file(path: &Path, source: &str) -> Result<Vec<LogItem>, String> {
    if !path.exists() {
        return Ok(vec![]);
    }

    let content =
        fs::read_to_string(path).map_err(|e| format!("Erro ao ler arquivo de log: {e}"))?;

    let mut items: Vec<LogItem> = content
        .lines()
        .filter(|line| !line.trim().is_empty())
        .map(|line| parse_log_line(line, source))
        .collect();

    items.reverse();
    Ok(items)
}

#[tauri::command]
pub fn init_logs() -> Result<(), String> {
    let error_path = log_file_path("error");
    if error_path.exists() && older_than_30_days(&error_path) {
        fs::remove_file(&error_path)
            .map_err(|e| format!("Erro ao remover error.log: {e}"))?;
    }

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

#[tauri::command]
pub fn read_logs() -> Result<Vec<LogItem>, String> {
    let info_path = log_file_path("info");
    let error_path = log_file_path("error");

    let mut items = Vec::new();
    items.extend(read_log_file(&info_path, "info.log")?);
    items.extend(read_log_file(&error_path, "error.log")?);

    items.sort_by(|a, b| b.timestamp.cmp(&a.timestamp));

    Ok(items)
}

#[tauri::command]
pub fn clear_logs() -> Result<(), String> {
    let info_path = log_file_path("info");
    let error_path = log_file_path("error");

    if info_path.exists() {
        fs::write(&info_path, "").map_err(|e| format!("Erro ao limpar info.log: {e}"))?;
    }

    if error_path.exists() {
        fs::write(&error_path, "").map_err(|e| format!("Erro ao limpar error.log: {e}"))?;
    }

    Ok(())
}