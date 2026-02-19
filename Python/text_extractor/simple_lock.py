import base64
import hashlib
import hmac
import os
import subprocess
import sys
import time
import winreg
from typing import Optional, Tuple

APP_NAME = "LeadsApp"

# Troque por um segredo longo e aleatório (64+ bytes).
APP_SECRET = b"CHANGE_ME__PUT_A_LONG_RANDOM_SECRET_64_BYTES_MINIMUM________________"

REG_PATH = r"Software\LeadsApp"
REG_TOKEN = "LicenseToken"
REG_STATE = "InstallState"
REG_MIDHASH = "MachineIdHash"
REG_FIRSTSEEN = "FirstSeen"


# -------------------------
# Machine ID
# -------------------------

def _machine_guid() -> str:
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
    val, _ = winreg.QueryValueEx(key, "MachineGuid")
    return str(val).strip()


def _smbios_uuid() -> str:
    try:
        out = subprocess.check_output(["wmic", "csproduct", "get", "uuid"], text=True, errors="ignore")
        lines = [l.strip() for l in out.splitlines() if l.strip()]
        return lines[1] if len(lines) > 1 else ""
    except Exception:
        return ""


def machine_id() -> str:
    raw = "|".join([p for p in (_machine_guid(), _smbios_uuid()) if p])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest().upper()


def machine_id_hash(mid: str) -> str:
    return hashlib.sha256(mid.encode("utf-8")).hexdigest().upper()


def _token_for(mid: str) -> str:
    sig = hmac.new(APP_SECRET, mid.encode("utf-8"), hashlib.sha256).digest()
    return base64.urlsafe_b64encode(sig).decode("ascii").rstrip("=")


# -------------------------
# Paths
# -------------------------

def exe_dir() -> str:
    # Pasta onde está o executável (PyInstaller) ou script (dev)
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def appdata_dir() -> str:
    base = os.environ.get("APPDATA") or os.path.expanduser("~")
    d = os.path.join(base, APP_NAME)
    os.makedirs(d, exist_ok=True)
    return d


def license_path_exe() -> str:
    return os.path.join(exe_dir(), "license.dat")


def license_path_appdata() -> str:
    return os.path.join(appdata_dir(), "license.dat")


# -------------------------
# IO helpers
# -------------------------

def _file_read(path: str) -> Optional[str]:
    try:
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            v = f.read().strip()
            return v or None
    except Exception:
        return None


def _file_write(path: str, token: str) -> bool:
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(token)
        return True
    except Exception:
        return False


def _reg_get(name: str) -> Optional[str]:
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
        val, _ = winreg.QueryValueEx(key, name)
        v = str(val).strip()
        return v or None
    except Exception:
        return None


def _reg_set(name: str, value: str) -> None:
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
    winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)


def _reg_set_if_missing(name: str, value: str) -> None:
    if _reg_get(name) is None:
        _reg_set(name, value)


# -------------------------
# Core logic
# -------------------------

def ensure_or_mark() -> Tuple[bool, str]:
    """
    Retorna (ok, motivo). Se ok=False, o app deve bloquear.

    Regras:
    A) Instalação nova legítima:
       - não existe license no exe
       - não existe license no appdata
       - não existe LicenseToken no HKCU
       => cria os 3 (exe/appdata/HKCU)

    B) Tentativa de cópia (EXE-only):
       - existe license no exe
       - não existe license no appdata
       - não existe LicenseToken no HKCU
       => BLOQUEIA e grava InstallState=COPIED_ATTEMPT + MachineIdHash no HKCU (sem criar token)

    C) Instalação válida:
       - existem os 3
       - tokens batem e correspondem ao PC
       => ok

    D) Qualquer estado parcial/adulterado:
       => bloqueia
    """
    mid = machine_id()
    midh = machine_id_hash(mid)

    t_exe = _file_read(license_path_exe())
    t_app = _file_read(license_path_appdata())
    t_reg = _reg_get(REG_TOKEN)

    has_exe = t_exe is not None
    has_app = t_app is not None
    has_reg = t_reg is not None

    # A) Instalação nova legítima (permitir mesmo que HKCU tenha COPIED_ATTEMPT)
    if (not has_exe) and (not has_app) and (not has_reg):
        tok = _token_for(mid)

        ok_exe = _file_write(license_path_exe(), tok)
        ok_app = _file_write(license_path_appdata(), tok)
        if not (ok_exe and ok_app):
            # Sem permissão para escrever (ex.: Program Files)
            return False, "Sem permissão para criar arquivos de licença na pasta do app ou AppData."

        _reg_set(REG_TOKEN, tok)
        _reg_set(REG_STATE, "OK")
        _reg_set(REG_MIDHASH, midh)
        _reg_set(REG_FIRSTSEEN, str(int(time.time())))
        return True, "OK"

    # B) Tentativa de cópia (EXE-only)
    if has_exe and (not has_app) and (not has_reg):
        _reg_set(REG_STATE, "COPIED_ATTEMPT")
        _reg_set(REG_MIDHASH, midh)
        _reg_set_if_missing(REG_FIRSTSEEN, str(int(time.time())))
        return False, "Cópia detectada (license.dat do exe sem marca local)."

    # C) Supostamente instalado, mas faltando alguma parte -> adulteração
    # (ex.: apagaram appdata, apagaram exe, apagaram registro)
    if not (has_exe and has_app and has_reg):
        return False, "Instalação incompleta/adulterada (faltando marcador de licença)."

    # D) Existem os 3: validar consistência + vínculo ao PC
    # Tokens devem ser idênticos
    if not (hmac.compare_digest(t_exe, t_app) and hmac.compare_digest(t_exe, t_reg)):
        return False, "Licença inconsistente entre exe/appdata/registro."

    # Token deve corresponder ao machine_id atual
    expected = _token_for(mid)
    if not hmac.compare_digest(t_exe, expected):
        return False, "Licença não corresponde a este computador."

    # Atualiza estado (caso tenha ficado COPIED_ATTEMPT antes)
    _reg_set(REG_STATE, "OK")
    _reg_set(REG_MIDHASH, midh)
    _reg_set_if_missing(REG_FIRSTSEEN, str(int(time.time())))
    return True, "OK"
