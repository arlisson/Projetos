# config.py
from __future__ import annotations

import json
import os
from typing import Optional, Dict, Any, List

CONFIG_FIELDS_PATH = "controle_campos.json"
CONFIG_SHEET_PATH = "controle_planilha.json"
CONFIG_UI_PATH = "controle_ui.json"
CONFIG_EMAIL_DOMAINS_PATH = "controle_email_dominios.json"


def default_fields_config() -> dict:
    # Agora com "abas"
    base_campos = [
        {"id": "nome", "titulo": "Nome", "tipo": "texto", "fixo": True},
        {"id": "telefone", "titulo": "Telefone", "tipo": "telefone", "fixo": True},
        {"id": "email", "titulo": "Email", "tipo": "email", "fixo": True},
    ]
    default_sheet = "Preenche Fácil"
    return {
        "arquivo_padrao": "PreencheFacil.xlsx",
        "aba": default_sheet,
        "abas": {
            default_sheet: {"campos": base_campos}
        },
    }

def _normalize_campos(campos: list, field_types: List[str]) -> list:
    out = []
    for c in campos or []:
        if not isinstance(c, dict):
            continue
        c = dict(c)
        c.setdefault("tipo", "texto")
        c.setdefault("fixo", False)
        if c.get("tipo") not in field_types:
            c["tipo"] = "texto"
        # garante chaves mínimas
        c.setdefault("id", "")
        c.setdefault("titulo", "")
        out.append(c)
    return out

def get_sheet_campos(cfg: dict, sheet_name: str) -> list:
    abas = cfg.get("abas") or {}
    sheet = abas.get(sheet_name) or {}
    return sheet.get("campos") or []


def set_sheet_campos(cfg: dict, sheet_name: str, campos: list) -> None:
    cfg.setdefault("abas", {})
    cfg["abas"].setdefault(sheet_name, {})
    cfg["abas"][sheet_name]["campos"] = campos


def load_fields_config(field_types: List[str]) -> dict:
    if not os.path.exists(CONFIG_FIELDS_PATH):
        cfg = default_fields_config()
        save_fields_config(cfg)
        return cfg

    with open(CONFIG_FIELDS_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f) or {}

    # defaults
    d = default_fields_config()
    cfg.setdefault("arquivo_padrao", d["arquivo_padrao"])
    cfg.setdefault("aba", d["aba"])

    # migração do formato antigo:
    # - se existir cfg["campos"] no topo e não existir cfg["abas"], move para a aba atual
    if "abas" not in cfg or not isinstance(cfg.get("abas"), dict):
        cfg["abas"] = {}
    if "campos" in cfg and isinstance(cfg.get("campos"), list):
        campos_legacy = cfg.get("campos") or []
        sheet = cfg.get("aba") or d["aba"]
        if sheet not in cfg["abas"]:
            cfg["abas"][sheet] = {}
        if not cfg["abas"][sheet].get("campos"):
            cfg["abas"][sheet]["campos"] = campos_legacy
        # opcional: remover o legado para não confundir
        try:
            del cfg["campos"]
        except Exception:
            pass

    # garante que exista a aba atual dentro de "abas"
    sheet = cfg.get("aba") or d["aba"]
    if sheet not in cfg["abas"]:
        cfg["abas"][sheet] = {"campos": d["abas"][d["aba"]]["campos"]}

    # normaliza campos de todas as abas
    for sheet_name, payload in (cfg.get("abas") or {}).items():
        if not isinstance(payload, dict):
            cfg["abas"][sheet_name] = {"campos": []}
            continue
        payload.setdefault("campos", [])
        payload["campos"] = _normalize_campos(payload.get("campos"), field_types)

    return cfg


def save_fields_config(cfg: dict) -> None:
    with open(CONFIG_FIELDS_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def load_sheet_config() -> dict:
    if not os.path.exists(CONFIG_SHEET_PATH):
        return {}
    try:
        with open(CONFIG_SHEET_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_sheet_config(path: str) -> None:
    with open(CONFIG_SHEET_PATH, "w", encoding="utf-8") as f:
        json.dump({"last_sheet_path": path}, f, ensure_ascii=False, indent=2)


def get_last_sheet_path() -> Optional[str]:
    cfg = load_sheet_config()
    p = cfg.get("last_sheet_path")
    if not p:
        return None
    return p if os.path.exists(p) else None


def default_ui_config() -> dict:
    # Mantém compatível com seu padrão anterior (icons + theme + background_hsl)
    return {
        "window_icon": "assets/A.ico",
        "button_icons": {
            "choose_file": "assets/icons/pasta.png",
            "add_field": "assets/icons/adicionar.png",
            "save_lead": "assets/icons/salvar.png",
            "clear": "assets/icons/limpar.png",
            "edit_title": "assets/icons/editar.png",
            "delete_field": "assets/icons/lixeira.png",
            "settings": "assets/icons/engrenagem.png",
        },
        "theme": {
            "background": "#0B1220",
            "surface": "#0F1A2B",
            "surface_alt": "#111F33",
            "text": "#E6EDF7",
            "muted_text": "#A7B3C6",
            "primary": "#3B82F6",
            "danger": "#EF4444",
            "border": "#1F2A44",
        },
        "background_hsl": {"h": 210, "s": 49, "l": 8},
        "footer_left_html": "<b>Se precisar de telefonia para sua empresa -> WhatsApp (22) 98812-4656</b>",
    }


def load_ui_config() -> dict:
    if not os.path.exists(CONFIG_UI_PATH):
        cfg = default_ui_config()
        save_ui_config(cfg)
        return cfg

    try:
        with open(CONFIG_UI_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f) or {}
    except Exception:
        cfg = default_ui_config()
        save_ui_config(cfg)
        return cfg

    # defaults (não sobrescreve o que o usuário já configurou)
    d = default_ui_config()
    cfg.setdefault("window_icon", d["window_icon"])
    cfg.setdefault("button_icons", d["button_icons"])
    cfg.setdefault("theme", d["theme"])
    cfg.setdefault("background_hsl", d["background_hsl"])
    cfg.setdefault("footer_left_html", d["footer_left_html"])

    # garante subchaves mínimas do tema
    for k, v in d["theme"].items():
        cfg["theme"].setdefault(k, v)

    return cfg


def save_ui_config(cfg: dict) -> None:
    with open(CONFIG_UI_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def default_email_domains_config() -> dict:
    return {
        "dominios": [
            "@gmail.com",
            "@hotmail.com",
            "@yahoo.com",
            "@outlook.com",
        ]
    }


def load_email_domains_config() -> dict:
    if not os.path.exists(CONFIG_EMAIL_DOMAINS_PATH):
        cfg = default_email_domains_config()
        save_email_domains_config(cfg)
        return cfg

    try:
        with open(CONFIG_EMAIL_DOMAINS_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f) or {}
    except Exception:
        cfg = default_email_domains_config()
        save_email_domains_config(cfg)
        return cfg

    cfg.setdefault("dominios", default_email_domains_config()["dominios"])
    # normaliza: garante '@' e remove vazios/duplicados
    out: List[str] = []
    for d in cfg.get("dominios", []) or []:
        s = str(d or "").strip()
        if not s:
            continue
        if not s.startswith("@"):
            s = "@" + s
        if s not in out:
            out.append(s)
    cfg["dominios"] = out

    return cfg


def save_email_domains_config(cfg: dict) -> None:
    with open(CONFIG_EMAIL_DOMAINS_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)