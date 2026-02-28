# formatters.py
from __future__ import annotations

import re
from datetime import datetime, date
from typing import Optional, Any


def normalize_masked_text(value: str) -> str:
    """
    Remove entradas que são apenas máscara/separadores (ex.: "//", "__/__/____").
    """
    v = (value or "").strip()

    only_separators = re.sub(r"[0-9A-Za-zÀ-ÿ]", "", v)
    if v and only_separators and all(ch in " _-./()[]" for ch in only_separators):
        if not re.search(r"[0-9A-Za-zÀ-ÿ]", v):
            return ""

    if "/" in v and not re.search(r"\d", v):
        return ""

    digits = re.sub(r"\D", "", v)
    if "/" in v and digits and len(digits) < 8:
        return ""

    return v


def digits_only(value: str) -> str:
    return re.sub(r"\D+", "", value or "")


def strip_mask_chars(value: str) -> str:
    return (value or "").replace("_", "").strip()


def parse_decimal_br(s: str) -> Optional[float]:
    if s is None:
        return None
    s = str(s).strip()
    if not s:
        return None
    s = re.sub(r"[^\d,\.\-]+", "", s)
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    else:
        if "," in s:
            s = s.replace(".", "")
            s = s.replace(",", ".")
    try:
        return float(s)
    except Exception:
        return None


def parse_date_any(s: str) -> Optional[date]:
    if s is None:
        return None
    s = str(s).strip()
    if not s:
        return None
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            pass
    return None


def normalize_bool_ptbr(s: str) -> Optional[str]:
    if s is None:
        return None
    s0 = str(s).strip().lower()
    if not s0:
        return None
    if s0 in {"sim", "s", "yes", "y", "true", "1"}:
        return "Sim"
    if s0 in {"não", "nao", "n", "no", "false", "0"}:
        return "Não"
    return str(s).strip()


def cast_value_by_type(tipo: str, raw: str) -> Any:
    raw = "" if raw is None else str(raw).strip()
    if raw == "":
        return ""

    if tipo == "numero":
        v = parse_decimal_br(raw)
        return v if v is not None else raw

    if tipo == "moeda":
        v = parse_decimal_br(raw)
        return v if v is not None else raw

    if tipo == "data":
        d = parse_date_any(raw)
        return d if d is not None else raw

    if tipo == "booleano":
        b = normalize_bool_ptbr(raw)
        return b if b is not None else ""

    return raw