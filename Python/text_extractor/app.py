# app.py (editado: footer via controle_ui.json e engrenagem abre tema + domínios)
from __future__ import annotations

from license_dialog import LicenseDialog, read_license_text
from user_login import prompt_email, clear_login
from online_license import ensure_online_license, clear_cache
from simple_lock import ensure_or_mark
from loading_screen import LoadingScreen


EMAIL_RETRY_CODES = {"no_license", "blocked", "device_limit", "not_activated", "revoked"}

import json
import sys
import os
from typing import Dict, List, Optional, Any, Tuple

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
    QFrame,
    QDialog,
    QDialogButtonBox,
)

from colors import (
    DEFAULT_THEME,
    hsl_to_rgb,
    rgb_to_hex,
    derive_theme_from_background,
)

from config import (
    load_fields_config,
    save_fields_config,
    load_ui_config,
    save_ui_config,
    get_last_sheet_path,
    save_sheet_config,
    load_email_domains_config,
    save_email_domains_config,
)

from models import (
    Campo,
    FIELD_TYPES,
    sanitize_id,
    make_unique_id,
    infer_type_from_title,
)

from formatters import (
    normalize_masked_text,
    digits_only,
    strip_mask_chars,
)

from excel_io import (
    is_excel_lock_present,
    read_headers_from_excel,
    write_headers_from_campos,
    ensure_workbook,
    apply_column_type_rules,
    append_row_typed,
    delete_column_by_header,
    rename_column_header,
)

from dialogs import (
    ThemeDialog,
    CursorStartLineEdit,
    EmailDomainsDialog,
)

from icon_manager import IconManager
from widgets import EmailInputWidget, FieldRowWidget, BoolInputWidget


def abs_path(p: str) -> str:
    if not p:
        return ""
    if os.path.isabs(p):
        return p
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, p)


def file_exists(p: str) -> bool:
    ap = abs_path(p)
    return bool(ap) and os.path.exists(ap)


class SettingsDialog(QDialog):
    def __init__(self, parent: "App"):
        super().__init__(parent)
        self.setWindowTitle("Configurações")
        self.setModal(True)
        self.setMinimumWidth(360)

        self.parent_app = parent

        self.lbl = QLabel("Escolha o que deseja editar:")
        self.btn_theme = QPushButton("Tema de cores")
        self.btn_domains = QPushButton("Domínios de e-mail")
        # self.btn_domains.setEnabled(self.parent_app._has_email_fields())

        self.btn_domains.setEnabled(True)

        self.btn_theme.clicked.connect(self._open_theme)
        self.btn_domains.clicked.connect(self._open_domains)

        btns = QDialogButtonBox(QDialogButtonBox.Close)
        btns.rejected.connect(self.reject)
        btns.accepted.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl)
        layout.addWidget(self.btn_theme)
        layout.addWidget(self.btn_domains)
        layout.addStretch(1)
        layout.addWidget(btns)
        self.setLayout(layout)

    def _open_theme(self) -> None:
        self.parent_app.open_theme_settings()

    def _open_domains(self) -> None:
        self.parent_app.open_email_domains()
        self.btn_domains.setEnabled(self.parent_app._has_email_fields())


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.cfg_fields = load_fields_config(FIELD_TYPES)
        self.cfg_ui = load_ui_config()

        self.cfg_email = load_email_domains_config()
        self.email_domains: List[str] = self.cfg_email.get("dominios", [])

        self.sheet_name: str = self.cfg_fields.get("aba", "Preenche Fácil")
        self.file_path: Optional[str] = get_last_sheet_path()

        self.campos: List[Campo] = [Campo(**c) for c in self.cfg_fields.get("campos", [])]

        # inputs[field_id] = QLineEdit | EmailInputWidget
        self.inputs: Dict[str, Any] = {}

        self.icon_mgr = IconManager(self.cfg_ui, abs_path=abs_path, file_exists=file_exists)

        self._apply_window_icon()
        self._build_ui()
        self._apply_theme_from_config()

        if self.file_path:
            self._apply_file_path(self.file_path, prepare=True, silent=True)

    def open_license(self) -> None:
        theme = (self.cfg_ui.get("theme") or dict(DEFAULT_THEME))
        text = read_license_text()
        dlg = LicenseDialog(self, theme=theme, license_text=text)
        dlg.exec()

    def _apply_window_icon(self) -> None:
        icon_path = self.cfg_ui.get("window_icon", "")
        if file_exists(icon_path):
            self.setWindowIcon(QIcon(abs_path(icon_path)))

    # ---------- tema ----------

    def _apply_theme_from_config(self) -> None:
        base_theme = dict(DEFAULT_THEME)
        base_theme.update(self.cfg_ui.get("theme", {}) or {})

        hsl = self.cfg_ui.get("background_hsl", {}) or {}
        h = int(hsl.get("h", 210))
        s = int(hsl.get("s", 49))
        l = int(hsl.get("l", 8))

        r, g, b = hsl_to_rgb(h, s, l)
        bg_hex = rgb_to_hex(r, g, b)

        derived = derive_theme_from_background(bg_hex, base_theme)

        self.cfg_ui["theme"] = derived
        self.cfg_ui["background_hsl"] = {"h": h, "s": s, "l": l}
        save_ui_config(self.cfg_ui)

        self._apply_theme(derived)

    def _apply_theme(self, theme: dict) -> None:
        bg = theme["background"]
        surface = theme["surface"]
        surface_alt = theme["surface_alt"]
        text = theme["text"]
        muted = theme["muted_text"]
        primary = theme["primary"]
        danger = theme["danger"]
        border = theme["border"]

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg};
                color: {text};
                font-size: 13px;
            }}

            QLabel {{
                color: {text};
            }}

            QLineEdit {{
                background-color: {surface};
                color: {text};
                border: 1px solid {border};
                border-radius: 8px;
                padding: 8px;
            }}

            QComboBox {{
                background-color: {surface};
                color: {text};
                border: 1px solid {border};
                border-radius: 8px;
                padding: 6px;
                min-width: 120px;
            }}

            QComboBox QAbstractItemView {{
                background-color: {surface_alt};
                color: {text};
                border: 1px solid {border};
                selection-background-color: {primary};
                selection-color: #FFFFFF;
            }}

            QScrollArea {{
                background-color: transparent;
                border: none;
            }}

            QScrollArea QWidget {{
                background-color: transparent;
            }}

            QPushButton {{
                background-color: {surface_alt};
                color: {text};
                border: 1px solid {border};
                border-radius: 10px;
                padding: 8px 10px;
            }}

            QPushButton:hover {{
                border-color: {primary};
            }}

            QPushButton:pressed {{
                background-color: {surface};
            }}

            QPushButton[variant="primary"] {{
                background-color: {primary};
                color: #FFFFFF;
                border: 1px solid {primary};
                font-weight: 600;
            }}

            QPushButton[variant="danger"] {{
                background-color: {danger};
                color: #FFFFFF;
                border: 1px solid {danger};
                font-weight: 600;
            }}

            QLabel#Status {{
                color: {muted};
            }}
        """)

        self._retint_all_icons(theme)

    def _retint_all_icons(self, theme: dict) -> None:
        text = theme["text"]
        white = "#FFFFFF"

        self.icon_mgr.apply_button_icon(self.btn_file, "choose_file", text)
        self.icon_mgr.apply_button_icon(self.btn_add_field, "add_field", text)
        self.icon_mgr.apply_button_icon(self.btn_clear, "clear", text)
        self.icon_mgr.apply_button_icon(self.btn_save, "save_lead", white)
        self.icon_mgr.apply_button_icon(self.btn_settings, "settings", text)

        self._last_theme_for_fields = theme
        self.render_fields()

    # ---------- domínios email ----------

    def _has_email_fields(self) -> bool:
        return any(c.tipo == "email" for c in self.campos)

    def open_email_domains(self) -> None:
        dlg = EmailDomainsDialog(self, domains=list(self.email_domains))
        if dlg.exec() == dlg.accepted:
            # sempre persiste, mesmo que não existam campos email
            self.email_domains = dlg.domains()
            self.cfg_email["dominios"] = list(self.email_domains)
            save_email_domains_config(self.cfg_email)

            # se houver widgets de email renderizados, atualiza
            self._refresh_email_domain_widgets()

    def _refresh_email_domain_widgets(self) -> None:
        for c in self.campos:
            if c.tipo != "email":
                continue
            w = self.inputs.get(c.id)
            if isinstance(w, EmailInputWidget):
                w.set_domains(self.email_domains)

    # ---------- configurações (engrenagem) ----------

    def open_settings(self) -> None:
        dlg = SettingsDialog(self)
        dlg.exec()

    # ---------- build UI ----------

    def _build_ui(self) -> None:
        self.setWindowTitle("Preenche Fácil - Avance")
        self.setMinimumWidth(490)

        root = QVBoxLayout()

        file_row = QHBoxLayout()

        self.btn_file = QPushButton("Escolher planilha…")
        self.lbl_file = QLabel("Arquivo: (não selecionado)")
        self.lbl_file.setWordWrap(True)
        self.btn_file.clicked.connect(self.choose_file)

        self.btn_settings = QPushButton("")
        self.btn_settings.setToolTip("Configurações")
        self.btn_settings.setFixedWidth(44)
        self.btn_settings.clicked.connect(self.open_settings)

        file_row.addWidget(self.btn_file)
        file_row.addWidget(self.lbl_file, 1)
        file_row.addWidget(self.btn_settings)
        root.addLayout(file_row)

        self.fields_container = QWidget()
        self.fields_layout = QVBoxLayout()
        self.fields_container.setLayout(self.fields_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.fields_container)
        root.addWidget(scroll, 1)

        actions = QHBoxLayout()

        self.btn_add_field = QPushButton("Adicionar Campo")
        self.btn_save = QPushButton("Salvar (nova linha)")
        self.btn_clear = QPushButton("Limpar")

        self.btn_save.setProperty("variant", "primary")

        actions.addWidget(self.btn_add_field)
        actions.addWidget(self.btn_clear)
        actions.addWidget(self.btn_save)

        self.btn_add_field.clicked.connect(self.add_field)
        self.btn_save.clicked.connect(self.save_lead)
        self.btn_clear.clicked.connect(self.clear_fields)

        root.addLayout(actions)

        self.lbl_status = QLabel("Preencha os campos (copie/cole) e clique em Salvar.")
        self.lbl_status.setWordWrap(True)
        self.lbl_status.setObjectName("Status")
        root.addWidget(self.lbl_status)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Plain)
        sep.setFixedHeight(1)
        root.addWidget(sep)

        footer_row = QHBoxLayout()

        default_footer = "<b>Se precisar de telefonia para sua empresa -> WhatsApp (22) 98812-4656</b>"
        footer_html = (self.cfg_ui.get("footer_left_html") or default_footer)

        self.lbl_footer_left = QLabel(footer_html)
        self.lbl_footer_left.setTextFormat(Qt.RichText)
        footer_row.addWidget(self.lbl_footer_left, 1)

        self.btn_license = QPushButton("Licença")
        self.btn_license.clicked.connect(self.open_license)
        footer_row.addWidget(self.btn_license, 0, Qt.AlignRight)

        footer_wrap = QWidget()
        footer_wrap.setLayout(footer_row)
        root.addWidget(footer_wrap)

        self.setLayout(root)

        self._last_theme_for_fields = dict(DEFAULT_THEME)
        self.render_fields()

        if self.file_path:
            self.lbl_file.setText(f"Arquivo: {self.file_path}")

    def _apply_input_mask(self, inp: QLineEdit, tipo: str) -> None:
        if isinstance(inp, CursorStartLineEdit):
            inp.set_force_cursor_start(tipo in ("telefone", "data"))

        if tipo == "telefone":
            inp.setInputMask("(00) 00000-0000;_")
        elif tipo == "data":
            inp.setInputMask("00/00/0000;_")
        else:
            inp.setInputMask("")

    def render_fields(self) -> None:
        # 1) Snapshot dos valores atuais antes de destruir os widgets
        prev_value: Dict[str, str] = {}
        prev_email_parts: Dict[str, Tuple[str, str]] = {}

        for cid, w in self.inputs.items():
            try:
                if isinstance(w, EmailInputWidget):
                    full, _ok = w.get_email()
                    prev_value[cid] = full or ""                  # SEMPRE string
                    prev_email_parts[cid] = (w.local(), w.domain())  # partes (opcional)
                elif isinstance(w, BoolInputWidget):
                    prev_value[cid] = w.value()
                elif isinstance(w, QLineEdit):
                    prev_value[cid] = w.text() or ""
                else:
                    prev_value[cid] = ""
            except Exception:
                prev_value[cid] = ""

        # 2) Limpa o layout e remove widgets
        while self.fields_layout.count():
            item = self.fields_layout.takeAt(0)
            ww = item.widget()
            if ww:
                ww.deleteLater()

        # 3) Recria os campos
        self.inputs.clear()

        theme = getattr(self, "_last_theme_for_fields", dict(DEFAULT_THEME))
        text = theme.get("text", "#E6EDF7")
        white = "#FFFFFF"

        for campo in self.campos:
            label_text = f"{campo.titulo}  [{campo.tipo}]"

            if campo.tipo == "email":
                emailw = EmailInputWidget(domains=self.email_domains)

                # Se antes era email, restaura as partes; senão tenta usar o texto completo
                if campo.id in prev_email_parts:
                    loc, dom = prev_email_parts[campo.id]
                    emailw.set_parts(loc, dom)
                else:
                    emailw.set_email(prev_value.get(campo.id, ""))

                self.inputs[campo.id] = emailw
                input_widget = emailw

            elif campo.tipo == "booleano":
                bw = BoolInputWidget()
                bw.set_value(prev_value.get(campo.id, ""))
                self.inputs[campo.id] = bw
                input_widget = bw

            else:
                inp = CursorStartLineEdit()
                inp.setPlaceholderText(f"Digite ou cole: {campo.titulo}")
                self._apply_input_mask(inp, campo.tipo)

                # Aqui SEMPRE vem string, nunca tupla
                inp.setText(prev_value.get(campo.id, ""))

                self.inputs[campo.id] = inp
                input_widget = inp

            roww = FieldRowWidget(field_id=campo.id, label_text=label_text, input_widget=input_widget)
            roww.editRequested.connect(self.edit_field)
            roww.deleteRequested.connect(self.delete_field)

            self.icon_mgr.apply_button_icon(roww.btn_edit, "edit_title", text)
            self.icon_mgr.apply_button_icon(roww.btn_del, "delete_field", white)

            self.fields_layout.addWidget(roww)

        self.fields_layout.addStretch(1)

    # ---------- persistência ----------

    def _persist_campos(self) -> None:
        self.cfg_fields["campos"] = [c.__dict__ for c in self.campos]
        self.cfg_fields["aba"] = self.sheet_name
        save_fields_config(self.cfg_fields)

    def _apply_file_path(self, path: str, prepare: bool, silent: bool = False) -> None:
        self.file_path = path
        self.lbl_file.setText(f"Arquivo: {path}")
        save_sheet_config(path)

        if prepare:
            try:
                headers = [c.titulo for c in self.campos]
                ensure_workbook(self.file_path, self.sheet_name, headers)
                apply_column_type_rules(self.file_path, self.sheet_name, self.campos)
                if not silent:
                    self.lbl_status.setText("Planilha preparada e salva como padrão.")
            except Exception as e:
                self.lbl_status.setText(f"Erro ao preparar planilha: {e}")

    # ---------- sincronizar campos ----------

    def sync_fields_from_existing_excel(self, path: str) -> bool:
        try:
            sheet_used, headers, has_header = read_headers_from_excel(path, self.sheet_name)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao ler a planilha: {e}")
            return False

        self.sheet_name = sheet_used
        self.cfg_fields["aba"] = self.sheet_name

        if not has_header:
            try:
                write_headers_from_campos(path, self.sheet_name, self.campos)
                apply_column_type_rules(path, self.sheet_name, self.campos)
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha ao criar cabeçalho na planilha: {e}")
                return False

            self._persist_campos()
            self.render_fields()
            self.lbl_status.setText("Planilha sem cabeçalho: cabeçalhos foram criados a partir do controle_campos.json.")
            return True

        if not headers:
            QMessageBox.warning(self, "Sem cabeçalho", "A planilha não possui cabeçalho válido na linha 1.")
            return False

        existing_by_title = {c.titulo.strip().lower(): c for c in self.campos}

        used_ids: set = set()
        new_campos: List[Campo] = []

        for h in headers:
            key = h.strip().lower()
            old = existing_by_title.get(key)

            if old:
                cid = old.id
                tipo = old.tipo if old.tipo in FIELD_TYPES else "texto"
                fixo = old.fixo
                used_ids.add(cid)
            else:
                cid = make_unique_id(sanitize_id(h), used_ids)
                tipo = infer_type_from_title(h)
                if tipo not in FIELD_TYPES:
                    tipo = "texto"
                fixo = False

            new_campos.append(Campo(id=cid, titulo=h, tipo=tipo, fixo=fixo))

        self.campos = new_campos
        self._persist_campos()

        try:
            apply_column_type_rules(path, self.sheet_name, self.campos)
        except Exception:
            pass

        self.render_fields()
        self.lbl_status.setText("Campos importados da planilha e salvos no controle.")
        return True

    def choose_file(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Escolher planilha",
            self.cfg_fields.get("arquivo_padrao", "PreencheFacil.xlsx"),
            "Planilha Excel (*.xlsx)",
        )
        if not path:
            return

        if not path.lower().endswith(".xlsx"):
            path += ".xlsx"

        existed = os.path.exists(path)

        if existed:
            resp = QMessageBox.question(
                self,
                "Planilha existente",
                "Esta planilha já existe.\n\n"
                "Deseja importar os campos do cabeçalho (linha 1) para o aplicativo?\n\n"
                "Sim: substitui os campos do app pelos campos da planilha (linha 1).\n"
                "Não: mantém os campos atuais e garante as colunas no Excel.\n\n"
                "Obs.: se a planilha não tiver cabeçalho, o app criará os títulos automaticamente a partir do controle."
            )
            if resp == QMessageBox.Yes:
                self._apply_file_path(path, prepare=False, silent=True)
                ok = self.sync_fields_from_existing_excel(path)
                if ok:
                    self.lbl_file.setText(f"Arquivo: {path}  (aba: {self.sheet_name})")
                return

        self._apply_file_path(path, prepare=True, silent=False)

    # ---------- ações de campos ----------

    def add_field(self) -> None:
        title, ok = QInputDialog.getText(self, "Novo campo", "Título do campo:")
        if not ok or not title.strip():
            return

        title = title.strip()
        existing_titles = {c.titulo for c in self.campos}
        if title in existing_titles:
            QMessageBox.warning(self, "Atenção", "Já existe um campo com esse título.")
            return

        tipo, ok_tipo = QInputDialog.getItem(self, "Tipo do campo", "Selecione o tipo:", FIELD_TYPES, 0, False)
        if not ok_tipo:
            return
        tipo = str(tipo)

        used_ids = {c.id for c in self.campos}
        cid = make_unique_id(sanitize_id(title), used_ids)

        self.campos.append(Campo(id=cid, titulo=title, tipo=tipo, fixo=False))
        self._persist_campos()

        self.render_fields()
        self.lbl_status.setText("Campo criado e salvo no arquivo de controle.")

        if self.file_path:
            try:
                headers = [c.titulo for c in self.campos]
                ensure_workbook(self.file_path, self.sheet_name, headers)
                apply_column_type_rules(self.file_path, self.sheet_name, self.campos)
            except Exception as e:
                self.lbl_status.setText(f"Campo criado, mas falhou ao atualizar Excel: {e}")

    def edit_field(self, field_id: str) -> None:
        campo = next((c for c in self.campos if c.id == field_id), None)
        if not campo:
            return

        old_tipo = campo.tipo

        old_value = ""
        old_email_parts: Tuple[str, str] = ("", "")
        w0 = self.inputs.get(field_id)

        if isinstance(w0, EmailInputWidget):
            old_value, _ = w0.get_email()
            old_email_parts = (w0.local(), w0.domain())
        elif isinstance(w0, QLineEdit):
            old_value = w0.text()

        new_title, ok = QInputDialog.getText(self, "Editar campo", "Título:", text=campo.titulo)
        if not ok:
            return
        new_title = new_title.strip()
        if not new_title:
            QMessageBox.warning(self, "Atenção", "Título não pode ser vazio.")
            return

        idx = FIELD_TYPES.index(campo.tipo) if campo.tipo in FIELD_TYPES else 0
        new_tipo, ok_tipo = QInputDialog.getItem(self, "Editar campo", "Tipo:", FIELD_TYPES, idx, False)
        if not ok_tipo:
            return
        new_tipo = str(new_tipo)

        existing_titles = {c.titulo for c in self.campos if c.id != field_id}
        if new_title in existing_titles:
            QMessageBox.warning(self, "Atenção", "Já existe um campo com esse título.")
            return

        old_title = campo.titulo
        campo.titulo = new_title
        campo.tipo = new_tipo
        self._persist_campos()

        try:
            if self.file_path:
                if old_title != new_title:
                    rename_column_header(self.file_path, self.sheet_name, old_title, new_title)
                apply_column_type_rules(self.file_path, self.sheet_name, self.campos)
        except Exception as e:
            self.lbl_status.setText(f"Atualizado no controle, mas falhou no Excel: {e}")

        self.render_fields()

        masked = {"telefone", "data"}

        if new_tipo == "email":
            w = self.inputs.get(field_id)
            if isinstance(w, EmailInputWidget):
                if old_tipo == "email":
                    w.set_parts(old_email_parts[0], old_email_parts[1])
                else:
                    w.set_email(old_value)
        else:
            w = self.inputs.get(field_id)
            if isinstance(w, QLineEdit):
                if old_tipo in masked and new_tipo not in masked:
                    w.setText(digits_only(old_value))
                elif old_tipo not in masked and new_tipo in masked:
                    w.setText(digits_only(old_value))
                else:
                    if new_tipo not in masked:
                        w.setText(strip_mask_chars(w.text()))

        self.lbl_status.setText("Campo atualizado (título/tipo).")

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
                apply_column_type_rules(self.file_path, self.sheet_name, self.campos)
        except Exception as e:
            self.lbl_status.setText(f"Campo removido do controle, mas falhou ao remover coluna no Excel: {e}")

        self.render_fields()
        self.lbl_status.setText("Campo excluído (e coluna removida, quando aplicável).")

    # ---------- ações gerais ----------

    def clear_fields(self) -> None:
        for _, w in self.inputs.items():
            if isinstance(w, EmailInputWidget):
                w.set_parts("", w.domain())
            elif isinstance(w, QLineEdit):
                w.setText("")
        self.lbl_status.setText("Campos limpos.")

    def save_lead(self) -> None:
        if not self.file_path:
            QMessageBox.warning(self, "Atenção", "Selecione uma planilha primeiro.")
            return

        try:
            if is_excel_lock_present(self.file_path):
                msg = (
                    "Não foi possível salvar porque a planilha parece estar aberta no Excel.\n\n"
                    "Feche o arquivo no Excel e tente novamente."
                )
                self.lbl_status.setText("Planilha aberta no Excel (bloqueada).")
                QMessageBox.warning(self, "Planilha em uso", msg)
                return
        except Exception:
            pass

        row_by_title: Dict[str, str] = {}

        for c in self.campos:
            w = self.inputs.get(c.id)

            if c.tipo == "email" and isinstance(w, EmailInputWidget):
                w.inp_local.setText(normalize_masked_text(w.local()))
                email_final, ok = w.get_email()
                if not ok:
                    QMessageBox.warning(
                        self,
                        "Atenção",
                        f"No campo '{c.titulo}', informe um domínio (ex.: @gmail.com) ou cole o e-mail completo.",
                    )
                    return
                row_by_title[c.titulo] = email_final
                continue
            
            if c.tipo == "booleano" and isinstance(w, BoolInputWidget):
                row_by_title[c.titulo] = w.value()
                continue

            raw = w.text().strip() if isinstance(w, QLineEdit) else ""
            txt = normalize_masked_text(raw)
            row_by_title[c.titulo] = txt

        if all(not v for v in row_by_title.values()):
            QMessageBox.information(self, "Info", "Nada para salvar (todos os campos vazios).")
            return

        import time
        last_err = None
        for attempt in range(6):
            try:
                append_row_typed(self.file_path, self.sheet_name, self.campos, row_by_title)
                last_err = None
                break
            except PermissionError as e:
                last_err = e
                try:
                    if is_excel_lock_present(self.file_path):
                        msg = (
                            "Não foi possível salvar porque a planilha está aberta no Excel.\n\n"
                            "Feche o arquivo no Excel e tente novamente."
                        )
                        self.lbl_status.setText("Planilha aberta no Excel (bloqueada).")
                        QMessageBox.warning(self, "Planilha em uso", msg)
                        return
                except Exception:
                    pass
                time.sleep(0.2 * (2 ** attempt))
            except Exception as e:
                self.lbl_status.setText(f"Erro ao salvar: {e}")
                QMessageBox.critical(self, "Erro", f"Erro ao salvar: {e}")
                return

        if last_err is not None:
            msg = (
                "Não foi possível salvar a planilha.\n\n"
                "Possíveis causas:\n"
                "- O arquivo está aberto no Excel\n"
                "- O antivírus está verificando/bloqueando a gravação\n"
                "- A pasta/arquivo não permite escrita\n\n"
                "Feche o Excel (se estiver aberto), aguarde alguns segundos e tente novamente.\n"
                "Se o problema persistir, escolha outra pasta para a planilha."
            )
            self.lbl_status.setText(f"Erro ao salvar (arquivo bloqueado): {last_err}")
            QMessageBox.critical(self, "Erro ao salvar", msg)
            return

        self.clear_fields()
        self.lbl_status.setText("Dados salvos (nova linha adicionada). Campos limpos automaticamente.")
        QMessageBox.information(self, "Info", "Dados salvos (nova linha adicionada). Campos limpos automaticamente.")

    # ---------- tema ----------

    def open_theme_settings(self) -> None:
        hsl = self.cfg_ui.get("background_hsl", {}) or {}
        h = int(hsl.get("h", 210))
        s = int(hsl.get("s", 49))
        l = int(hsl.get("l", 8))

        before_cfg = json.loads(json.dumps(self.cfg_ui))
        before_theme = dict(self.cfg_ui.get("theme", dict(DEFAULT_THEME)))

        dlg = ThemeDialog(self, h, s, l)

        def on_change():
            hh, ss, ll = dlg.values()
            rr, gg, bb = hsl_to_rgb(hh, ss, ll)
            bg_hex = rgb_to_hex(rr, gg, bb)
            base = dict(DEFAULT_THEME)
            base.update(before_theme)
            derived = derive_theme_from_background(bg_hex, base)
            self._apply_theme(derived)

        dlg.slider_h.valueChanged.connect(on_change)
        dlg.slider_s.valueChanged.connect(on_change)
        dlg.slider_l.valueChanged.connect(on_change)

        on_change()

        if dlg.exec() == dlg.accepted:
            hh, ss, ll = dlg.values()
            rr, gg, bb = hsl_to_rgb(hh, ss, ll)
            bg_hex = rgb_to_hex(rr, gg, bb)

            base = dict(DEFAULT_THEME)
            base.update(before_theme)

            derived = derive_theme_from_background(bg_hex, base)
            self.cfg_ui = before_cfg
            self.cfg_ui["background_hsl"] = {"h": hh, "s": ss, "l": ll}
            self.cfg_ui["theme"] = derived
            save_ui_config(self.cfg_ui)

            self._apply_theme(derived)
        else:
            self.cfg_ui = before_cfg
            save_ui_config(self.cfg_ui)
            self._apply_theme(before_theme)


def main() -> None:
    app = QApplication([])

    loader = LoadingScreen(app, title="Validando acesso")
    loader.show("Preparando validação...")

    while True:
        loader.hide()
        email = prompt_email(force=False)
        if not email:
            loader.close()
            return

        loader.show("Validando licença online...")
        ok, msg, code = ensure_online_license(email)
        if ok:
            loader.update("Licença validada com sucesso.")
            break

        if code in EMAIL_RETRY_CODES:
            loader.hide()
            QMessageBox.warning(None, "Validação", msg + "\n\nDigite um e-mail válido para continuar.")
            clear_login()
            clear_cache()
            loader.show("Reiniciando validação...")
            continue

        loader.hide()
        QMessageBox.critical(None, "Acesso negado", msg)
        loader.close()
        return

    loader.update("Validando dispositivo (marcador local)...")
    ok_local, reason = ensure_or_mark(allow_create=True)
    if not ok_local:
        loader.hide()
        QMessageBox.critical(None, "Acesso negado", reason)
        loader.close()
        return

    loader.update("Carregando interface...")
    w = App()
    w.show()
    app.processEvents()

    loader.finish_and_close(w)
    app.exec()


if __name__ == "__main__":
    main()