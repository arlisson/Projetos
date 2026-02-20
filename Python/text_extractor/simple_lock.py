import base64
import hashlib
import hmac
import os
import sys
import time
import ctypes
import ctypes.wintypes as wt
import winreg
from typing import Optional, Tuple

APP_NAME = "LeadsApp"

# Troque por um segredo longo e aleatório (64+ bytes).
# Ideal: gerar uma vez e NÃO mudar depois de distribuir, senão invalida os markers já gerados.
APP_SECRET = b"CHANGE_ME__PUT_A_LONG_RANDOM_SECRET_64_BYTES_MINIMUM________________"

# Marker SOMENTE LEITURA criado pelo instalador em: <pasta do app>\_internal\
# (não será escrito pelo app)
INTERNAL_DIR_NAME = "_internal"
INTERNAL_MARKER_FILE = "_internal.dat"  # o instalador deve criar este arquivo

# Marcador por máquina (gerado APENAS após validação online)
# C:\ProgramData\LeadsApp\cahce_string.dat
PROGRAMDATA_FILE = "cahce_string.dat"

# Registro (apenas status; não guarda token)
REG_PATH = r"Software\LeadsApp"
REG_STATE = "InstallState"
REG_FIRSTSEEN = "FirstSeen"
REG_MIDHASH = "MachineIdHash"


# -------------------------
# Paths
# -------------------------

def exe_dir_base() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def internal_dir() -> str:
    return os.path.join(exe_dir_base(), INTERNAL_DIR_NAME)


def internal_marker_path() -> str:
    return os.path.join(internal_dir(), INTERNAL_MARKER_FILE)


def programdata_dir() -> str:
    base = os.environ.get("PROGRAMDATA") or r"C:\ProgramData"
    d = os.path.join(base, APP_NAME)
    os.makedirs(d, exist_ok=True)
    return d


def license_path_programdata() -> str:
    return os.path.join(programdata_dir(), PROGRAMDATA_FILE)


# -------------------------
# Registro (status)
# -------------------------

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
# Machine ID (estável)
# -------------------------

def _machine_guid() -> str:
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
    val, _ = winreg.QueryValueEx(key, "MachineGuid")
    return str(val).strip()


def machine_id() -> str:
    raw = _machine_guid()
    return hashlib.sha256(raw.encode("utf-8")).hexdigest().upper()


def machine_id_hash(mid: str) -> str:
    return hashlib.sha256(mid.encode("utf-8")).hexdigest().upper()


# -------------------------
# DPAPI (LocalMachine)
# -------------------------

class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", wt.DWORD), ("pbData", ctypes.POINTER(ctypes.c_byte))]


crypt32 = ctypes.WinDLL("crypt32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

CryptProtectData = crypt32.CryptProtectData
CryptProtectData.argtypes = [
    ctypes.POINTER(DATA_BLOB),
    wt.LPCWSTR,
    ctypes.POINTER(DATA_BLOB),
    ctypes.c_void_p,
    ctypes.c_void_p,
    wt.DWORD,
    ctypes.POINTER(DATA_BLOB),
]
CryptProtectData.restype = wt.BOOL

CryptUnprotectData = crypt32.CryptUnprotectData
CryptUnprotectData.argtypes = [
    ctypes.POINTER(DATA_BLOB),
    ctypes.POINTER(wt.LPWSTR),
    ctypes.POINTER(DATA_BLOB),
    ctypes.c_void_p,
    ctypes.c_void_p,
    wt.DWORD,
    ctypes.POINTER(DATA_BLOB),
]
CryptUnprotectData.restype = wt.BOOL

LocalFree = kernel32.LocalFree
LocalFree.argtypes = [ctypes.c_void_p]
LocalFree.restype = ctypes.c_void_p

CRYPTPROTECT_LOCAL_MACHINE = 0x4


def _bytes_to_blob(data: bytes) -> DATA_BLOB:
    buf = (ctypes.c_byte * len(data)).from_buffer_copy(data)
    return DATA_BLOB(len(data), ctypes.cast(buf, ctypes.POINTER(ctypes.c_byte)))


def dpapi_protect_localmachine(plaintext: bytes) -> bytes:
    in_blob = _bytes_to_blob(plaintext)
    out_blob = DATA_BLOB()
    if not CryptProtectData(
        ctypes.byref(in_blob),
        "local_marker",
        None,
        None,
        None,
        CRYPTPROTECT_LOCAL_MACHINE,
        ctypes.byref(out_blob),
    ):
        raise OSError(ctypes.get_last_error())
    try:
        return ctypes.string_at(out_blob.pbData, out_blob.cbData)
    finally:
        LocalFree(out_blob.pbData)


def dpapi_unprotect(ciphertext: bytes) -> bytes:
    in_blob = _bytes_to_blob(ciphertext)
    out_blob = DATA_BLOB()
    p_desc = wt.LPWSTR()

    if not CryptUnprotectData(
        ctypes.byref(in_blob),
        ctypes.byref(p_desc),
        None,
        None,
        None,
        0,
        ctypes.byref(out_blob),
    ):
        raise OSError(ctypes.get_last_error())

    try:
        return ctypes.string_at(out_blob.pbData, out_blob.cbData)
    finally:
        if p_desc:
            LocalFree(p_desc)
        LocalFree(out_blob.pbData)


# -------------------------
# Arquivo (ProgramData)
# -------------------------

def _file_read_bytes(path: str) -> Optional[bytes]:
    try:
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            s = f.read().strip()
        if not s:
            return None
        return base64.b64decode(s.encode("ascii"))
    except Exception:
        return None


def _file_write_bytes(path: str, blob: bytes) -> None:
    s = base64.b64encode(blob).decode("ascii")
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)


# -------------------------
# Payload (dentro do DPAPI)
# -------------------------

def _make_payload(mid: str, token: bytes) -> bytes:
    """
    payload = mid_hash | token | mac
    mac = HMAC(APP_SECRET, mid_hash||token)
    """
    midh = machine_id_hash(mid).encode("ascii")
    mac = hmac.new(APP_SECRET, midh + token, hashlib.sha256).digest()
    return midh + b"|" + token + b"|" + mac


def _parse_payload(payload: bytes) -> Tuple[str, bytes, bytes]:
    parts = payload.split(b"|")
    if len(parts) != 3:
        raise ValueError("payload inválido")
    return parts[0].decode("ascii"), parts[1], parts[2]


# -------------------------
# Core
# -------------------------

def ensure_or_mark(allow_create: bool = False) -> Tuple[bool, str]:
    """
    Política final (conforme combinado):
    - O instalador cria: <pasta app>\\_internal\\_internal.dat (marker somente leitura)
    - O app NUNCA escreve em _internal
    - O marcador por máquina fica em ProgramData e é DPAPI(LocalMachine):
        C:\\ProgramData\\LeadsApp\\cahce_string.dat

    Regras:
    1) Se marker do instalador não existir => bloqueia (evita rodar app copiado solto).
    2) Se o arquivo de ProgramData NÃO existir:
       - allow_create=False => bloqueia pedindo ativação online primeiro.
       - allow_create=True  => cria o marcador por máquina (use somente após validação online OK).
    3) Se o arquivo existir => valida DPAPI + HMAC + machine_id_hash.
    """
    # 1) Exigir marker do instalador
    if not os.path.exists(internal_marker_path()):
        return False, "Instalação inválida (marker do instalador ausente em _internal)."

    mid = machine_id()
    midh = machine_id_hash(mid)

    # 2) Ler marcador por máquina
    blob = _file_read_bytes(license_path_programdata())
    if blob is None:
        if not allow_create:
            _reg_set(REG_STATE, "NEEDS_ONLINE_ACTIVATION")
            _reg_set(REG_MIDHASH, midh)
            _reg_set_if_missing(REG_FIRSTSEEN, str(int(time.time())))
            return False, "Primeira execução requer ativação online."

        # allow_create=True => criar marcador por máquina (após validação online)
        try:
            token = os.urandom(32)
            payload = _make_payload(mid, token)
            protected = dpapi_protect_localmachine(payload)
            _file_write_bytes(license_path_programdata(), protected)
        except Exception:
            return False, "Sem permissão para criar arquivo de controle em ProgramData."

        _reg_set(REG_STATE, "OK")
        _reg_set(REG_MIDHASH, midh)
        _reg_set_if_missing(REG_FIRSTSEEN, str(int(time.time())))
        return True, "OK"

    # 3) Validar marcador existente
    try:
        payload = dpapi_unprotect(blob)  # falha em outro PC
    except Exception:
        _reg_set(REG_STATE, "MOVED_OR_COPIED")
        _reg_set(REG_MIDHASH, midh)
        _reg_set_if_missing(REG_FIRSTSEEN, str(int(time.time())))
        return False, "Arquivo de controle não pode ser aberto neste computador (cópia detectada)."

    try:
        stored_midh, token, mac = _parse_payload(payload)
    except Exception:
        return False, "Arquivo de controle corrompido."

    expected_mac = hmac.new(APP_SECRET, stored_midh.encode("ascii") + token, hashlib.sha256).digest()
    if not hmac.compare_digest(mac, expected_mac):
        return False, "Arquivo de controle adulterado."

    if stored_midh != midh:
        return False, "Arquivo de controle pertence a outro computador."

    _reg_set(REG_STATE, "OK")
    _reg_set(REG_MIDHASH, midh)
    _reg_set_if_missing(REG_FIRSTSEEN, str(int(time.time())))
    return True, "OK"