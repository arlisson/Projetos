"""
Aplicativo desktop para cadastro de leads em planilha Excel (XLSX).

Funcionalidades:
- Campos fixos: Nome, Telefone, Email
- Campos dinâmicos: criar, editar título e excluir (reflete em colunas do Excel)
- Planilha persistida: caminho salvo em controle_planilha.json
- UI customizável: ícones e fundo via controle_ui.json
- Salvamento: adiciona linha nova (append) sem sobrescrever
- Ao salvar: limpa automaticamente os campos

Arquivos de controle:
- controle_campos.json   -> campos e configurações
- controle_planilha.json -> último caminho de planilha
- controle_ui.json       -> caminhos de ícones e imagem de fundo

Dependências:
pip install PySide6 openpyxl
"""

import json
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from openpyxl import Workbook, load_workbook

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
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

CONFIG_FIELDS_PATH = "controle_campos.json"
CONFIG_SHEET_PATH = "controle_planilha.json"
CONFIG_UI_PATH = "controle_ui.json"


# =========================
# Utilitários de caminho
# =========================

def abs_path(p: str) -> str:
    """
    Resolve um caminho relativo para absoluto usando a pasta do script como base.

    Args:
        p (str): caminho relativo ou absoluto

    Returns:
        str: caminho absoluto
    """
    if not p:
        return ""
    if os.path.isabs(p):
        return p
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, p)


def file_exists(p: str) -> bool:
    """
    Verifica existência (considerando resolução para absoluto).

    Args:
        p (str): caminho relativo/absoluto

    Returns:
        bool: True se existir
    """
    ap = abs_path(p)
    return bool(ap) and os.path.exists(ap)


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


def default_fields_config() -> dict:
    """
    Configuração padrão de campos para primeira execução.
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


def load_fields_config() -> dict:
    """
    Carrega o controle de campos; se não existir, cria padrão.
    """
    if not os.path.exists(CONFIG_FIELDS_PATH):
        cfg = default_fields_config()
        save_fields_config(cfg)
        return cfg
    with open(CONFIG_FIELDS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_fields_config(cfg: dict) -> None:
    """
    Salva o controle de campos.
    """
    with open(CONFIG_FIELDS_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def load_sheet_config() -> dict:
    """
    Carrega o controle da planilha (caminho). Se não existir, retorna vazio.
    """
    if not os.path.exists(CONFIG_SHEET_PATH):
        return {}
    try:
        with open(CONFIG_SHEET_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_sheet_config(path: str) -> None:
    """
    Salva o caminho da planilha no controle.
    """
    with open(CONFIG_SHEET_PATH, "w", encoding="utf-8") as f:
        json.dump({"last_sheet_path": path}, f, ensure_ascii=False, indent=2)


def get_last_sheet_path() -> Optional[str]:
    """
    Obtém o caminho da última planilha usada, se existir e ainda estiver acessível.
    """
    cfg = load_sheet_config()
    p = cfg.get("last_sheet_path")
    if not p:
        return None
    return p if os.path.exists(p) else None


def default_ui_config() -> dict:
    """
    Configuração padrão de UI (caso o arquivo não exista).
    Ajuste os caminhos conforme sua estrutura.
    """
    return {
        "window_icon": "assets/app.ico",
        "background_image": "assets/backgrounds/bg.png",
        "button_icons": {
            "choose_file": "assets/icons/pasta.png",
            "add_field": "assets/icons/adicionar.png",
            "save_lead": "assets/icons/salvar.png",
            "clear": "assets/icons/limpar.png",
            "edit_title": "assets/icons/editar.png",
            "delete_field": "assets/icons/lixeira.png"
        }
    }


def load_ui_config() -> dict:
    """
    Carrega controle de UI; se não existir, cria padrão.
    """
    if not os.path.exists(CONFIG_UI_PATH):
        cfg = default_ui_config()
        save_ui_config(cfg)
        return cfg
    try:
        with open(CONFIG_UI_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        cfg = default_ui_config()
        save_ui_config(cfg)
        return cfg


def save_ui_config(cfg: dict) -> None:
    """
    Salva controle de UI.
    """
    with open(CONFIG_UI_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


# =========================
# Excel helpers (openpyxl)
# =========================

def ensure_workbook(path: str, sheet_name: str, headers: List[str]) -> None:
    """
    Garante que o arquivo exista, a aba exista e que o cabeçalho contenha todas as colunas.
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
    Adiciona nova linha sem sobrescrever.
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
    Remove coluna do Excel pelo cabeçalho (destrutivo).
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
    Renomeia o cabeçalho de uma coluna no Excel.
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
    Janela principal do aplicativo.
    - Ícones e imagem de fundo são carregados de controle_ui.json.
    """

    def __init__(self):
        super().__init__()

        # Carrega configs
        self.cfg_fields = load_fields_config()
        self.cfg_ui = load_ui_config()

        self.sheet_name: str = self.cfg_fields.get("aba", "Leads")
        self.file_path: Optional[str] = get_last_sheet_path()

        self.campos: List[Campo] = [Campo(**c) for c in self.cfg_fields.get("campos", [])]
        self.inputs: Dict[str, QLineEdit] = {}

        # Aplica ícone da janela
        self._apply_window_icon()

        # Monta UI
        self._build_ui()

        # Aplica plano de fundo
        self._apply_background()

        # Se já existe planilha salva, prepara e mostra
        if self.file_path:
            self._apply_file_path(self.file_path, prepare=True, silent=True)

    # ---------- UI Theme ----------

    def _apply_window_icon(self) -> None:
        """
        Aplica o ícone da janela a partir do controle_ui.json.
        """
        icon_path = self.cfg_ui.get("window_icon", "")
        if file_exists(icon_path):
            self.setWindowIcon(QIcon(abs_path(icon_path)))

    def _apply_background(self) -> None:
        """
        Aplica uma imagem de fundo na janela principal via stylesheet.

        Observação:
        - O fundo é aplicado ao QWidget raiz (janela).
        - Ajuste conforme desejar (contain/cover). Aqui usa "stretch" para cobrir.
        """
        bg = self.cfg_ui.get("background_image", "")
        if file_exists(bg):
            bg_abs = abs_path(bg).replace("\\", "/")
            self.setStyleSheet(f"""
                QWidget#MainWindow {{
                    background-image: url("{bg_abs}");
                    background-repeat: no-repeat;
                    background-position: center;
                    background-attachment: fixed;
                }}
            """)
            self.setObjectName("MainWindow")

    def _set_button_icon(self, btn: QPushButton, key: str) -> None:
        """
        Define o ícone de um botão usando a chave configurada em controle_ui.json.

        Args:
            btn (QPushButton): botão a customizar
            key (str): chave em button_icons
        """
        icons = self.cfg_ui.get("button_icons", {}) or {}
        p = icons.get(key, "")
        if file_exists(p):
            btn.setIcon(QIcon(abs_path(p)))

    # ---------- Build UI ----------

    def _build_ui(self) -> None:
        self.setWindowTitle("Cadastro de Leads (Local)")
        self.setMinimumWidth(900)

        root = QVBoxLayout()

        # Arquivo
        file_row = QHBoxLayout()
        self.btn_file = QPushButton("Escolher planilha…")
        self._set_button_icon(self.btn_file, "choose_file")

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

        self.btn_add_field = QPushButton("Adicionar Campo")
        self._set_button_icon(self.btn_add_field, "add_field")

        self.btn_save = QPushButton("Salvar lead (nova linha)")
        self._set_button_icon(self.btn_save, "save_lead")

        self.btn_clear = QPushButton("Limpar")
        self._set_button_icon(self.btn_clear, "clear")

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

        if self.file_path:
            self.lbl_file.setText(f"Arquivo: {self.file_path}")

    def render_fields(self) -> None:
        """
        Renderiza os campos do formulário. Botões "Editar título" e "Excluir" recebem ícones.
        """
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

            btn_edit = QPushButton("Editar")
            self._set_button_icon(btn_edit, "edit_title")
            btn_edit.clicked.connect(lambda _=False, cid=campo.id: self.edit_field_title(cid))

            btn_del = QPushButton("Excluir")
            self._set_button_icon(btn_del, "delete_field")
            btn_del.clicked.connect(lambda _=False, cid=campo.id: self.delete_field(cid))

            row.addWidget(lbl)
            row.addWidget(inp, 1)
            row.addWidget(btn_edit)
            row.addWidget(btn_del)

            wrap = QWidget()
            wrap.setLayout(row)
            self.fields_layout.addWidget(wrap)

        self.fields_layout.addStretch(1)

    # ---------- Persistência de campos ----------

    def _persist_campos(self) -> None:
        self.cfg_fields["campos"] = [c.__dict__ for c in self.campos]
        save_fields_config(self.cfg_fields)

    # ---------- Persistência de planilha ----------

    def _apply_file_path(self, path: str, prepare: bool, silent: bool = False) -> None:
        self.file_path = path
        self.lbl_file.setText(f"Arquivo: {path}")
        save_sheet_config(path)

        if prepare:
            try:
                headers = [c.titulo for c in self.campos]
                ensure_workbook(self.file_path, self.sheet_name, headers)
                if not silent:
                    self.lbl_status.setText("Planilha preparada e salva como padrão.")
            except Exception as e:
                self.lbl_status.setText(f"Erro ao preparar planilha: {e}")

    def choose_file(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Escolher planilha",
            self.cfg_fields.get("arquivo_padrao", "leads.xlsx"),
            "Planilha Excel (*.xlsx)",
        )
        if not path:
            return
        if not path.lower().endswith(".xlsx"):
            path += ".xlsx"

        self._apply_file_path(path, prepare=True, silent=False)

    # ---------- Ações de campos ----------

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

    # ---------- Ações gerais ----------

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

        self.clear_fields()
        self.lbl_status.setText("Lead salvo (nova linha adicionada). Campos limpos automaticamente.")


def main() -> None:
    app = QApplication([])
    w = App()
    w.show()
    app.exec()


if __name__ == "__main__":
    main()
