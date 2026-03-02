# excel_io.py
from __future__ import annotations

import os
from typing import Dict, List, Tuple

from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

from models import Campo, EXCEL_NUMBER_FORMAT
from formatters import cast_value_by_type


def is_excel_lock_present(xlsx_path: str) -> bool:
    folder = os.path.dirname(xlsx_path) or "."
    name = os.path.basename(xlsx_path)
    lock_name = "~$" + name
    return os.path.exists(os.path.join(folder, lock_name))


def get_sheet_headers(xlsx_path: str, sheet_name: str) -> list[str]:
    wb = load_workbook(xlsx_path)
    ws = wb[sheet_name] if sheet_name in wb.sheetnames else wb.active
    headers: list[str] = []
    for cell in ws[1]:
        v = (cell.value or "")
        v = str(v).strip()
        if v:
            headers.append(v)
    return headers


def read_headers_from_excel(path: str, preferred_sheet: str) -> Tuple[str, List[str], bool]:
    """
    Lê a linha 1 e retorna (sheet_name_usado, headers, has_header).
    has_header = True se encontrou pelo menos 1 valor não vazio na linha 1.
    - Se preferred_sheet não existir, usa a aba ativa.
    """
    wb = load_workbook(path)
    sheet_name = preferred_sheet if preferred_sheet in wb.sheetnames else wb.active.title
    ws = wb[sheet_name]

    if ws.max_row < 1:
        return sheet_name, [], False

    headers: List[str] = []
    has_any = False

    for cell in ws[1]:
        v = cell.value
        if v is None:
            continue
        s = str(v).strip()
        if s:
            has_any = True
            if s not in headers:
                headers.append(s)

    return sheet_name, headers, has_any


def write_headers_from_campos(path: str, sheet_name: str, campos: List[Campo]) -> None:
    """
    Garante que a linha 1 tenha cabeçalhos (títulos) baseados em campos do app.
    Se a aba não existir, cria.
    """
    headers = [c.titulo for c in campos]

    wb = load_workbook(path)
    ws = wb[sheet_name] if sheet_name in wb.sheetnames else wb.create_sheet(sheet_name)

    for col_idx, h in enumerate(headers, start=1):
        ws.cell(row=1, column=col_idx, value=h)

    wb.save(path)


def ensure_workbook(path: str, sheet_name: str, headers: List[str]) -> None:
    if not os.path.exists(path):
        wb = Workbook()
        ws = wb.active
        ws.title = sheet_name
        ws.append(headers)
        wb.save(path)
        return

    wb = load_workbook(path)
    ws = wb[sheet_name] if sheet_name in wb.sheetnames else wb.create_sheet(sheet_name)

    if ws.max_row < 1:
        ws.append(headers)
        wb.save(path)
        return

    existing = [c.value for c in ws[1]]
    existing = [v for v in existing if v is not None]

    changed = False
    for h in headers:
        if h not in existing:
            existing.append(h)
            changed = True

    if changed:
        for col_idx, h in enumerate(existing, start=1):
            ws.cell(row=1, column=col_idx, value=h)

    wb.save(path)


def apply_column_type_rules(path: str, sheet_name: str, campos: List[Campo]) -> None:
    if not path or not os.path.exists(path):
        return

    wb = load_workbook(path)
    ws = wb[sheet_name] if sheet_name in wb.sheetnames else wb.create_sheet(sheet_name)

    if ws.max_row < 1:
        wb.save(path)
        return

    headers = [c.value for c in ws[1]]
    headers = [h for h in headers if h is not None]
    header_to_col = {h: (headers.index(h) + 1) for h in headers}

    try:
        ws.data_validations.dataValidation = []
    except Exception:
        pass

    max_row = max(ws.max_row, 2)

    for c in campos:
        if c.titulo not in header_to_col:
            continue

        col_idx = header_to_col[c.titulo]
        col_letter = get_column_letter(col_idx)
        fmt = EXCEL_NUMBER_FORMAT.get(c.tipo, "@")

        for r in range(2, max_row + 1):
            ws.cell(row=r, column=col_idx).number_format = fmt

        rng = f"{col_letter}2:{col_letter}1048576"

        if c.tipo == "numero":
            dv = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True)
            dv.errorTitle = "Valor inválido"
            dv.error = "Digite um número válido (>= 0)."
            ws.add_data_validation(dv)
            dv.add(rng)

        elif c.tipo == "moeda":
            dv = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True)
            dv.errorTitle = "Valor inválido"
            dv.error = "Digite um valor válido (>= 0)."
            ws.add_data_validation(dv)
            dv.add(rng)

        elif c.tipo == "data":
            dv = DataValidation(
                type="date",
                operator="between",
                formula1="DATE(1900,1,1)",
                formula2="DATE(2099,12,31)",
                allow_blank=True,
            )
            dv.errorTitle = "Data inválida"
            dv.error = "Digite uma data válida."
            ws.add_data_validation(dv)
            dv.add(rng)

        elif c.tipo == "booleano":
            dv = DataValidation(type="list", formula1='"Sim,Não"', allow_blank=True)
            dv.errorTitle = "Valor inválido"
            dv.error = 'Use "Sim" ou "Não".'
            ws.add_data_validation(dv)
            dv.add(rng)

    wb.save(path)

def _next_data_row(ws) -> int:
    # começa em 2 (linha 1 é cabeçalho)
    r = 2
    # considera “ocupada” se qualquer célula da linha tiver valor
    while True:
        if any(cell.value not in (None, "") for cell in ws[r]):
            r += 1
            continue
        return r

def append_row_typed(path: str, sheet_name: str, campos: List[Campo], row_by_title: Dict[str, str]) -> None:
    headers = [c.titulo for c in campos]
    ensure_workbook(path, sheet_name, headers)

    wb = load_workbook(path)
    ws = wb[sheet_name]

    existing = [c.value for c in ws[1]]
    existing = [v for v in existing if v is not None]
    col_idx = {h: (existing.index(h) + 1) for h in existing}

    next_row = _next_data_row(ws)

    for c in campos:
        h = c.titulo
        if h not in col_idx:
            continue

        value = cast_value_by_type(c.tipo, row_by_title.get(h, ""))
        cell = ws.cell(row=next_row, column=col_idx[h], value=value)
        cell.number_format = EXCEL_NUMBER_FORMAT.get(c.tipo, "@")

    wb.save(path)


def delete_column_by_header(path: str, sheet_name: str, header_name: str) -> None:
    if not path or not os.path.exists(path):
        return

    wb = load_workbook(path)
    if sheet_name not in wb.sheetnames:
        wb.save(path)
        return

    ws = wb[sheet_name]
    if ws.max_row < 1:
        wb.save(path)
        return

    headers = [c.value for c in ws[1]]
    if header_name not in headers:
        wb.save(path)
        return

    col = headers.index(header_name) + 1
    ws.delete_cols(col, 1)
    wb.save(path)


def rename_column_header(path: str, sheet_name: str, old_header: str, new_header: str) -> None:
    if not path or not os.path.exists(path):
        return

    wb = load_workbook(path)
    if sheet_name not in wb.sheetnames:
        wb.save(path)
        return

    ws = wb[sheet_name]
    if ws.max_row < 1:
        wb.save(path)
        return

    headers = [c.value for c in ws[1]]
    if old_header not in headers:
        wb.save(path)
        return

    col = headers.index(old_header) + 1
    ws.cell(row=1, column=col, value=new_header)
    wb.save(path)