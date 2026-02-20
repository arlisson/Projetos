import json
import os
import re
import time
from typing import Optional, Tuple

from PySide6.QtWidgets import QInputDialog, QMessageBox

APP_NAME = "LeadsApp"
LOGIN_FILE = "user_login.json"
LOGIN_MAX_AGE_SECONDS = 7 * 24 * 3600  # 7 dias (ajuste)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def _try_dir(base: str) -> Optional[str]:
    try:
        d = os.path.join(base, APP_NAME)
        os.makedirs(d, exist_ok=True)

        # teste real de escrita (evita Roaming indisponível)
        test_file = os.path.join(d, f".write_test_{int(time.time())}.tmp")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("ok")
        os.remove(test_file)

        return d
    except Exception:
        return None


def app_state_dir() -> str:
    """
    Diretório de estado com fallback real:
    1) %APPDATA% (Roaming)
    2) %LOCALAPPDATA% (Local)
    3) %PROGRAMDATA%\\LeadsApp\\user_root\\LeadsApp
    """
    p1 = os.environ.get("APPDATA")
    if p1:
        d = _try_dir(p1)
        if d:
            return d

    p2 = os.environ.get("LOCALAPPDATA")
    if p2:
        d = _try_dir(p2)
        if d:
            return d

    p3 = os.environ.get("PROGRAMDATA") or r"C:\ProgramData"
    d = _try_dir(os.path.join(p3, APP_NAME, "user_root"))
    if d:
        return d

    # fallback final extremo
    d = os.path.join(os.path.expanduser("~"), APP_NAME)
    os.makedirs(d, exist_ok=True)
    return d


def login_path() -> str:
    return os.path.join(app_state_dir(), LOGIN_FILE)


def _now_ts() -> int:
    return int(time.time())


def load_login() -> Tuple[Optional[str], Optional[int]]:
    try:
        with open(login_path(), "r", encoding="utf-8") as f:
            data = json.load(f) or {}
        email = (data.get("email") or "").strip().lower() or None
        ts = data.get("ts")
        ts = int(ts) if ts is not None else None
        return email, ts
    except Exception:
        return None, None


def save_login(email: str) -> None:
    data = {"email": email.strip().lower(), "ts": _now_ts()}
    with open(login_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def clear_login() -> None:
    try:
        p = login_path()
        if os.path.exists(p):
            os.remove(p)
    except Exception:
        # não bloquear o fluxo por isso
        pass


def is_login_expired(ts: Optional[int]) -> bool:
    if ts is None:
        return True
    return (_now_ts() - ts) > LOGIN_MAX_AGE_SECONDS


def prompt_email(force: bool = False) -> Optional[str]:
    """
    force=True => pede e-mail mesmo que exista login válido salvo.
    Retorna email válido (salva) ou None se cancelar.
    """
    saved_email, saved_ts = load_login()
    if (not force) and saved_email and not is_login_expired(saved_ts):
        return saved_email

    default_text = saved_email or ""
    while True:
        email, ok = QInputDialog.getText(None, "Login", "Digite seu e-mail:", text=default_text)
        if not ok:
            return None

        email = (email or "").strip().lower()
        if not email:
            QMessageBox.warning(None, "Atenção", "Informe um e-mail.")
            continue
        if not EMAIL_RE.match(email):
            QMessageBox.warning(None, "Atenção", "E-mail inválido.")
            continue

        save_login(email)
        return email