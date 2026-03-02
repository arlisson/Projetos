# models.py
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List


FIELD_TYPES: List[str] = [
    "texto",
    "telefone",
    "email",
    "numero",
    "moeda",
    "data",
    "booleano",
]

EXCEL_NUMBER_FORMAT: Dict[str, str] = {
    "texto": "@",
    "telefone": "@",
    "email": "@",
    "numero": "0.00",
    "moeda": '"R$" #,##0.00',
    "data": "dd/mm/yyyy",
    "booleano": "@",
}


@dataclass
class Campo:
    id: str
    titulo: str
    tipo: str = "texto"
    fixo: bool = False
    locked: bool = False


def sanitize_id(title: str) -> str:
    s = (title or "").strip().lower()
    s = s.replace(" ", "_")
    s = re.sub(r"[^a-z0-9_]+", "", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "campo"


def make_unique_id(base_id: str, used: set) -> str:
    cid = base_id
    i = 2
    while cid in used:
        cid = f"{base_id}_{i}"
        i += 1
    used.add(cid)
    return cid


def infer_type_from_title(header: str) -> str:
    h = (header or "").strip().lower()
    if "email" in h or "e-mail" in h:
        return "email"
    if "tel" in h or "fone" in h or "whats" in h or "cel" in h:
        return "telefone"
    if "data" in h or "dt" == h:
        return "data"
    if "preço" in h or "preco" in h or "valor" in h or "custo" in h:
        return "moeda"
    if "qtd" in h or "quant" in h or "numero" in h or "número" in h:
        return "numero"
    if "ativo" in h or "status" in h:
        return "booleano"
    return "texto"