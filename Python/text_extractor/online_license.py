# online_license.py
import hashlib
import json
import os
import time
import winreg
from typing import Tuple

import requests

APP_NAME = "LeadsApp"

# URL do Web App do Apps Script (termina com /exec)
API_URL = "https://script.google.com/macros/s/AKfycbznxprQ97DT5cYK2AXKSDNOr8N_kzi-YvZYiipHR0GXYnRUWhMhJFXm-8tcLqZ6DdG8/exec"

LICENSE_CACHE_FILE = "license_cache.json"

RENEW_EVERY_SECONDS = 24 * 3600         # revalidar a cada 24h
OFFLINE_GRACE_SECONDS = 3 * 24 * 3600   # tolerar 3 dias sem internet


def _ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def app_state_dir() -> str:
    """
    Diretório de estado com fallback:
    1) %APPDATA% (Roaming)
    2) %LOCALAPPDATA% (Local)
    3) %PROGRAMDATA%\\LeadsApp\\user
    """
    p1 = os.environ.get("APPDATA")
    if p1:
        try:
            return _ensure_dir(os.path.join(p1, APP_NAME))
        except Exception:
            pass

    p2 = os.environ.get("LOCALAPPDATA")
    if p2:
        try:
            return _ensure_dir(os.path.join(p2, APP_NAME))
        except Exception:
            pass

    p3 = os.environ.get("PROGRAMDATA") or r"C:\ProgramData"
    return _ensure_dir(os.path.join(p3, APP_NAME, "user"))


def cache_path() -> str:
    return os.path.join(app_state_dir(), LICENSE_CACHE_FILE)


def now_ts() -> int:
    return int(time.time())


def load_cache() -> dict:
    try:
        with open(cache_path(), "r", encoding="utf-8") as f:
            return json.load(f) or {}
    except Exception:
        return {}


def save_cache(data: dict) -> None:
    with open(cache_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_machine_guid() -> str:
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
    val, _ = winreg.QueryValueEx(key, "MachineGuid")
    return str(val).strip()


def device_id() -> str:
    return hashlib.sha256(get_machine_guid().encode("utf-8")).hexdigest().upper()


def call_api(action: str, email: str, dev_id: str) -> dict:
    payload = {"action": action, "email": email, "device_id": dev_id}
    r = requests.post(API_URL, json=payload, timeout=15)

    ct = (r.headers.get("Content-Type") or "").lower()
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code}: {r.text[:400]}")
    if "application/json" not in ct:
        raise RuntimeError(f"Resposta não-JSON (Content-Type={ct}): {r.text[:400]}")

    return r.json()


def ensure_online_license(email: str) -> Tuple[bool, str]:
    email = (email or "").strip().lower()
    dev_id = device_id()

    cache = load_cache()
    cached_email = (cache.get("email") or "").strip().lower()
    cached_dev = (cache.get("device_id") or "").strip()
    last_ok = int(cache.get("last_ok_ts") or 0)

    age = (now_ts() - last_ok) if last_ok else 10**9

    # cache recente e compatível
    if cached_email == email and cached_dev == dev_id and last_ok > 0 and age <= RENEW_EVERY_SECONDS:
        return True, "OK (cache)"

    # Se cache não bate (trocou email/PC), força activate
    action = "activate" if last_ok == 0 or cached_email != email or cached_dev != dev_id else "renew"

    try:
        resp = call_api(action, email, dev_id)
    except Exception as e:
        # Sem internet/erro: aplica grace period apenas se já teve validação OK e é o mesmo email/PC
        if last_ok > 0 and cached_email == email and cached_dev == dev_id and age <= OFFLINE_GRACE_SECONDS:
            return True, "OK (offline grace)"
        return False, f"Falha ao validar licença: {type(e).__name__}: {e}"

    if resp.get("ok") is True:
        save_cache({"email": email, "device_id": dev_id, "last_ok_ts": now_ts(), "last_resp": resp})
        return True, "OK"

    err = resp.get("error") or "unknown"
    if err == "no_license":
        return False, "E-mail não autorizado (sem licença)."
    if err == "blocked":
        return False, "Acesso bloqueado para este e-mail."
    if err == "device_limit":
        md = resp.get("max_devices")
        return False, f"Limite de computadores atingido para este e-mail. (max={md})"
    if err == "not_activated":
        return False, "Este computador ainda não foi ativado para este e-mail."
    if err == "revoked":
        return False, "Este computador foi revogado para este e-mail."

    return False, f"Licença inválida: {err}"