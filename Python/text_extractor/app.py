"""
Aplicativo desktop para cadastro de leads em planilha Excel (XLSX).

Funcionalidades:
- Campos fixos: Nome, Telefone, Email
- Campos dinâmicos: criar, editar título e excluir (reflete em colunas do Excel)
- Salvamento: adiciona linha nova (append) sem sobrescrever
- Ao salvar: limpa automaticamente os campos

Controle:
- controle_campos.json guarda a lista de campos e configurações.

Dependências:
pip install PySide6 openpyxl
"""
from PySide6.QtGui import QIcon
import json
import os
from dataclasses import dataclass
from typing import Dict, List, Optional

from openpyxl import Workbook, load_workbook
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

CONFIG_PATH = "controle_campos.json"


# =========================
# Modelos / Configuração
# =========================

@dataclass
class Campo:
    """
    Representa um campo do formulário (coluna na planilha).
    """
    id: str
    titulo: str
    tipo: str = "texto"
    fixo: bool = False


def default_config() -> dict:
    """
    Configuração padrão para primeira execução.
    """
    return {
        "arquivo_padrao": "leads.xlsx",
        "aba": "Leads",
        "campos": [
            {"id": "nome", "titulo": "Nome", "tipo": "texto", "fixo": True},
            {"id": "telefone", "titulo": "Telefone", "tipo": "telefone", "fixo": True},
            {"id": "email", "titulo": "Email", "tipo": "email", "fixo": True},
        ],
    }


def load_config() -> dict:
    """
    Carrega o arquivo de controle; se não existir, cria padrão.
    """
    if not os.path.exists(CONFIG_PATH):
        cfg = default_config()
        save_config(cfg)
        return cfg
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(cfg: dict) -> None:
    """
    Salva o arquivo de controle.
    """
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


# =========================
# Excel helpers (openpyxl)
# =========================

def ensure_workbook(path: str, sheet_name: str, headers: List[str]) -> None:
    """
    Garante que a planilha exista, a aba exista e que o cabeçalho contenha todas as colunas.
    Se o arquivo não existir, cria e escreve o cabeçalho.
    """
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


def append_row(path: str, sheet_name: str, headers: List[str], row: Dict[str, str]) -> None:
    """
    Insere uma linha nova ao final (append) sem sobrescrever.
    """
    ensure_workbook(path, sheet_name, headers)
    wb = load_workbook(path)
    ws = wb[sheet_name]

    existing = [c.value for c in ws[1]]
    existing = [v for v in existing if v is not None]
    col_idx = {h: (existing.index(h) + 1) for h in existing}

    next_row = ws.max_row + 1
    for h in headers:
        ws.cell(row=next_row, column=col_idx[h], value=row.get(h, ""))

    wb.save(path)


def delete_column_by_header(path: str, sheet_name: str, header_name: str) -> None:
    """
    Remove uma coluna do Excel pelo nome do cabeçalho (destrutivo).
    """
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
    """
    Renomeia o cabeçalho de uma coluna no Excel (apenas a célula do cabeçalho).
    """
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


# =========================
# UI / Aplicação
# =========================

class App(QWidget):
    """
    Janela principal do aplicativo (sem captura assistida).
    """

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("assets/app.ico"))
        self.cfg = load_config()
        self.sheet_name: str = self.cfg.get("aba", "Leads")
        self.file_path: Optional[str] = None

        self.campos: List[Campo] = [Campo(**c) for c in self.cfg.get("campos", [])]
        self.inputs: Dict[str, QLineEdit] = {}

        self._build_ui()

    def _build_ui(self) -> None:
        self.setWindowTitle("Cadastro de Leads (Local)")
        self.setMinimumWidth(900)

        root = QVBoxLayout()

        # Arquivo
        file_row = QHBoxLayout()
        self.btn_file = QPushButton("Escolher planilha…")
        self.lbl_file = QLabel("Arquivo: (não selecionado)")
        self.lbl_file.setWordWrap(True)
        self.btn_file.clicked.connect(self.choose_file)
        file_row.addWidget(self.btn_file)
        file_row.addWidget(self.lbl_file, 1)
        root.addLayout(file_row)

        # Campos roláveis
        self.fields_container = QWidget()
        self.fields_layout = QVBoxLayout()
        self.fields_container.setLayout(self.fields_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.fields_container)
        root.addWidget(scroll, 1)

        # Ações
        actions = QHBoxLayout()
        self.btn_add_field = QPushButton("+ Campo")
        self.btn_save = QPushButton("Salvar lead (nova linha)")
        self.btn_clear = QPushButton("Limpar")
        actions.addWidget(self.btn_add_field)
        actions.addWidget(self.btn_clear)
        actions.addWidget(self.btn_save)

        self.btn_add_field.clicked.connect(self.add_field)
        self.btn_save.clicked.connect(self.save_lead)
        self.btn_clear.clicked.connect(self.clear_fields)
        root.addLayout(actions)

        # Status
        self.lbl_status = QLabel("Preencha os campos (copie/cole) e clique em Salvar.")
        self.lbl_status.setWordWrap(True)
        root.addWidget(self.lbl_status)

        self.setLayout(root)
        self.render_fields()

    def render_fields(self) -> None:
        while self.fields_layout.count():
            item = self.fields_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        self.inputs.clear()

        for campo in self.campos:
            row = QHBoxLayout()

            lbl = QLabel(campo.titulo)
            lbl.setMinimumWidth(220)

            inp = QLineEdit()
            inp.setPlaceholderText(f"Digite ou cole: {campo.titulo}")
            self.inputs[campo.id] = inp

            btn_edit = QPushButton("Editar título")
            btn_edit.clicked.connect(lambda _=False, cid=campo.id: self.edit_field_title(cid))

            btn_del = QPushButton("Excluir")
            # se quiser bloquear exclusão de fixos:
            # btn_del.setEnabled(not campo.fixo)
            btn_del.clicked.connect(lambda _=False, cid=campo.id: self.delete_field(cid))

            row.addWidget(lbl)
            row.addWidget(inp, 1)
            row.addWidget(btn_edit)
            row.addWidget(btn_del)

            wrap = QWidget()
            wrap.setLayout(row)
            self.fields_layout.addWidget(wrap)

        self.fields_layout.addStretch(1)

    def _persist_campos(self) -> None:
        self.cfg["campos"] = [c.__dict__ for c in self.campos]
        save_config(self.cfg)

    def choose_file(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Escolher planilha",
            self.cfg.get("arquivo_padrao", "leads.xlsx"),
            "Planilha Excel (*.xlsx)",
        )
        if not path:
            return
        if not path.lower().endswith(".xlsx"):
            path += ".xlsx"

        self.file_path = path
        self.lbl_file.setText(f"Arquivo: {path}")

        try:
            headers = [c.titulo for c in self.campos]
            ensure_workbook(self.file_path, self.sheet_name, headers)
            self.lbl_status.setText("Planilha preparada.")
        except Exception as e:
            self.lbl_status.setText(f"Erro ao preparar planilha: {e}")

    def add_field(self) -> None:
        title, ok = QInputDialog.getText(self, "Novo campo", "Título do campo:")
        if not ok or not title.strip():
            return

        title = title.strip()
        existing_titles = {c.titulo for c in self.campos}
        if title in existing_titles:
            QMessageBox.warning(self, "Atenção", "Já existe um campo com esse título.")
            return

        cid = title.lower().replace(" ", "_")
        existing_ids = {c.id for c in self.campos}
        base = cid
        i = 2
        while cid in existing_ids:
            cid = f"{base}_{i}"
            i += 1

        self.campos.append(Campo(id=cid, titulo=title, tipo="texto", fixo=False))
        self._persist_campos()

        self.render_fields()
        self.lbl_status.setText("Campo criado e salvo no arquivo de controle.")

        if self.file_path:
            try:
                headers = [c.titulo for c in self.campos]
                ensure_workbook(self.file_path, self.sheet_name, headers)
            except Exception as e:
                self.lbl_status.setText(f"Campo criado, mas falhou ao atualizar Excel: {e}")

    def edit_field_title(self, field_id: str) -> None:
        campo = next((c for c in self.campos if c.id == field_id), None)
        if not campo:
            return

        new_title, ok = QInputDialog.getText(self, "Editar título", "Novo título:", text=campo.titulo)
        if not ok:
            return

        new_title = new_title.strip()
        if not new_title:
            QMessageBox.warning(self, "Atenção", "Título não pode ser vazio.")
            return

        existing_titles = {c.titulo for c in self.campos if c.id != field_id}
        if new_title in existing_titles:
            QMessageBox.warning(self, "Atenção", "Já existe um campo com esse título.")
            return

        old_title = campo.titulo
        campo.titulo = new_title
        self._persist_campos()

        try:
            if self.file_path:
                rename_column_header(self.file_path, self.sheet_name, old_title, new_title)
        except Exception as e:
            self.lbl_status.setText(f"Título atualizado no controle, mas falhou no Excel: {e}")

        self.render_fields()
        self.lbl_status.setText("Título do campo atualizado.")

    def delete_field(self, field_id: str) -> None:
        campo = next((c for c in self.campos if c.id == field_id), None)
        if not campo:
            return

        msg = (
            f"Confirma excluir o campo '{campo.titulo}'?\n\n"
            "Isso também removerá a coluna correspondente na planilha Excel.\n"
            "Os dados dessa coluna serão removidos definitivamente."
        )
        if QMessageBox.question(self, "Confirmar exclusão", msg) != QMessageBox.Yes:
            return

        self.campos = [c for c in self.campos if c.id != field_id]
        self._persist_campos()

        try:
            if self.file_path:
                delete_column_by_header(self.file_path, self.sheet_name, campo.titulo)
        except Exception as e:
            self.lbl_status.setText(f"Campo removido do controle, mas falhou ao remover coluna no Excel: {e}")

        self.render_fields()
        self.lbl_status.setText("Campo excluído (e coluna removida, quando aplicável).")

    def clear_fields(self) -> None:
        for inp in self.inputs.values():
            inp.setText("")
        self.lbl_status.setText("Campos limpos.")

    def save_lead(self) -> None:
        if not self.file_path:
            QMessageBox.warning(self, "Atenção", "Selecione uma planilha primeiro.")
            return

        headers = [c.titulo for c in self.campos]
        row = {c.titulo: (self.inputs[c.id].text().strip() if c.id in self.inputs else "") for c in self.campos}

        if all(not v for v in row.values()):
            QMessageBox.information(self, "Info", "Nada para salvar (todos os campos vazios).")
            return

        try:
            append_row(self.file_path, self.sheet_name, headers, row)
        except Exception as e:
            self.lbl_status.setText(f"Erro ao salvar: {e}")
            return

        # Limpa automaticamente após salvar
        self.clear_fields()
        self.lbl_status.setText("Lead salvo (nova linha adicionada). Campos limpos automaticamente.")


def main() -> None:
    app = QApplication([])    
    w = App()
    w.show()
    app.exec()


if __name__ == "__main__":
    
    main()
