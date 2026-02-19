"""
Aplicativo desktop para cadastro de leads em planilha Excel (XLSX).

Funcionalidades:
- Campos fixos: Nome, Telefone, Email
- Campos dinâmicos: criar, editar título e excluir (reflete em colunas do Excel)
- Planilha persistida: caminho salvo em controle_planilha.json
- UI customizável: ícones e tema via controle_ui.json
- Tema com sliders: usuário ajusta a cor de fundo (H/S/L); demais cores derivadas automaticamente
- Ícones tintados: ícones originalmente pretos passam a seguir a cor do tema
- Salvamento: adiciona linha nova (append) sem sobrescrever
- Ao salvar: limpa automaticamente os campos

Arquivos de controle:
- controle_campos.json
- controle_planilha.json
- controle_ui.json

Dependências:
pip install PySide6 openpyxl
"""

import json
import os
import colorsys
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from openpyxl import Workbook, load_workbook

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QColor, QPainter
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
    QDialog,
    QSlider,
    QFormLayout,
    QDialogButtonBox,
)

CONFIG_FIELDS_PATH = "controle_campos.json"
CONFIG_SHEET_PATH = "controle_planilha.json"
CONFIG_UI_PATH = "controle_ui.json"


# =========================
# Utilitários de caminho
# =========================

def abs_path(p: str) -> str:
    if not p:
        return ""
    if os.path.isabs(p):
        return p
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, p)


def file_exists(p: str) -> bool:
    ap = abs_path(p)
    return bool(ap) and os.path.exists(ap)


# =========================
# Cores / tema
# =========================

DEFAULT_THEME = {
    "background": "#0B1220",
    "surface": "#0F1A2B",
    "surface_alt": "#111F33",
    "text": "#E6EDF7",
    "muted_text": "#A7B3C6",
    "primary": "#3B82F6",
    "danger": "#EF4444",
    "border": "#1F2A44",
}


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    h = (hex_color or "").lstrip("#")
    if len(h) != 6:
        return (0, 0, 0)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))
    return f"#{r:02X}{g:02X}{b:02X}"


def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[int, int, int]:
    rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
    h, l, s = colorsys.rgb_to_hls(rf, gf, bf)
    return int(round(h * 359)), int(round(s * 100)), int(round(l * 100))


def hsl_to_rgb(h: int, s: int, l: int) -> Tuple[int, int, int]:
    hf = (h % 360) / 360.0
    sf = max(0, min(100, s)) / 100.0
    lf = max(0, min(100, l)) / 100.0
    r, g, b = colorsys.hls_to_rgb(hf, lf, sf)
    return int(round(r * 255)), int(round(g * 255)), int(round(b * 255))


def luminance(rgb: Tuple[int, int, int]) -> float:
    r, g, b = rgb
    # luminância relativa simples
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0


def blend(a: Tuple[int, int, int], b: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
    t = max(0.0, min(1.0, t))
    return (
        int(round(a[0] * (1 - t) + b[0] * t)),
        int(round(a[1] * (1 - t) + b[1] * t)),
        int(round(a[2] * (1 - t) + b[2] * t)),
    )


def derive_theme_from_background(bg_hex: str, base_theme: dict) -> dict:
    """
    Deriva as demais cores a partir do background, preservando primary/danger.
    Padrão:
    - surface / surface_alt: pequenos increments/decrements em relação ao fundo
    - border: mais contraste
    - text: claro se fundo escuro, escuro se fundo claro
    - muted_text: blend entre text e border
    """
    bg_rgb = hex_to_rgb(bg_hex)
    is_dark = luminance(bg_rgb) < 0.5

    white = (255, 255, 255)
    black = (0, 0, 0)

    # Ajustes suaves derivados do fundo
    if is_dark:
        surface_rgb = blend(bg_rgb, white, 0.06)
        surface_alt_rgb = blend(bg_rgb, white, 0.10)
        border_rgb = blend(bg_rgb, white, 0.16)
        text_rgb = hex_to_rgb(base_theme.get("text", "#E6EDF7"))
    else:
        surface_rgb = blend(bg_rgb, black, 0.06)
        surface_alt_rgb = blend(bg_rgb, black, 0.10)
        border_rgb = blend(bg_rgb, black, 0.16)
        text_rgb = (15, 23, 42)  # escuro legível

    muted_rgb = blend(text_rgb, border_rgb, 0.55)

    out = dict(base_theme)
    out["background"] = bg_hex
    out["surface"] = rgb_to_hex(*surface_rgb)
    out["surface_alt"] = rgb_to_hex(*surface_alt_rgb)
    out["border"] = rgb_to_hex(*border_rgb)
    out["text"] = rgb_to_hex(*text_rgb)
    out["muted_text"] = rgb_to_hex(*muted_rgb)
    # primary/danger preserva do base_theme
    return out


# =========================
# Modelos / Configuração
# =========================

@dataclass
class Campo:
    id: str
    titulo: str
    tipo: str = "texto"
    fixo: bool = False


def default_fields_config() -> dict:
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
    if not os.path.exists(CONFIG_FIELDS_PATH):
        cfg = default_fields_config()
        save_fields_config(cfg)
        return cfg
    with open(CONFIG_FIELDS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


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
    # Mantém o tema padrão informado como base
    bg = DEFAULT_THEME["background"]
    r, g, b = hex_to_rgb(bg)
    h, s, l = rgb_to_hsl(r, g, b)
    return {
        "window_icon": "assets/app.ico",
        "button_icons": {
            "choose_file": "assets/icons/pasta.png",
            "add_field": "assets/icons/adicionar.png",
            "save_lead": "assets/icons/salvar.png",
            "clear": "assets/icons/limpar.png",
            "edit_title": "assets/icons/editar.png",
            "delete_field": "assets/icons/lixeira.png",
            "settings": "assets/icons/engrenagem.png",
        },
        "theme": dict(DEFAULT_THEME),
        "background_hsl": {"h": h, "s": s, "l": l},
    }


def load_ui_config() -> dict:
    if not os.path.exists(CONFIG_UI_PATH):
        cfg = default_ui_config()
        save_ui_config(cfg)
        return cfg
    try:
        with open(CONFIG_UI_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            # garante defaults mínimos
            cfg.setdefault("theme", dict(DEFAULT_THEME))
            cfg.setdefault("button_icons", {})
            if "background_hsl" not in cfg:
                r, g, b = hex_to_rgb(cfg["theme"].get("background", DEFAULT_THEME["background"]))
                h, s, l = rgb_to_hsl(r, g, b)
                cfg["background_hsl"] = {"h": h, "s": s, "l": l}
            return cfg
    except Exception:
        cfg = default_ui_config()
        save_ui_config(cfg)
        return cfg


def save_ui_config(cfg: dict) -> None:
    with open(CONFIG_UI_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


# =========================
# Excel helpers (openpyxl)
# =========================

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


def append_row(path: str, sheet_name: str, headers: List[str], row: Dict[str, str]) -> None:
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


# =========================
# Dialog: Configuração de fundo (sliders)
# =========================

class ThemeDialog(QDialog):
    def __init__(self, parent: QWidget, h: int, s: int, l: int):
        super().__init__(parent)
        self.setWindowTitle("Ajustar tema")
        self.setModal(True)
        self.setMinimumWidth(420)

        self.slider_h = QSlider(Qt.Horizontal)
        self.slider_s = QSlider(Qt.Horizontal)
        self.slider_l = QSlider(Qt.Horizontal)

        self.slider_h.setRange(0, 359)
        self.slider_s.setRange(0, 100)
        self.slider_l.setRange(0, 100)

        self.slider_h.setValue(h)
        self.slider_s.setValue(s)
        self.slider_l.setValue(l)

        self.lbl_preview = QLabel("Prévia")
        self.lbl_preview.setAlignment(Qt.AlignCenter)
        self.lbl_preview.setMinimumHeight(60)

        form = QFormLayout()
        form.addRow("Hue", self.slider_h)
        form.addRow("Saturation", self.slider_s)
        form.addRow("Lightness", self.slider_l)

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.lbl_preview)
        layout.addWidget(btns)
        self.setLayout(layout)

        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)

    def values(self) -> Tuple[int, int, int]:
        return self.slider_h.value(), self.slider_s.value(), self.slider_l.value()


# =========================
# UI / Aplicação
# =========================

class App(QWidget):
    def __init__(self):
        super().__init__()

        # configs
        self.cfg_fields = load_fields_config()
        self.cfg_ui = load_ui_config()

        self.sheet_name: str = self.cfg_fields.get("aba", "Leads")
        self.file_path: Optional[str] = get_last_sheet_path()

        self.campos: List[Campo] = [Campo(**c) for c in self.cfg_fields.get("campos", [])]
        self.inputs: Dict[str, QLineEdit] = {}

        # cache de pixmaps para tint (evita reler disco)
        self._pixmap_cache: Dict[str, QPixmap] = {}

        # aplica ícone da janela
        self._apply_window_icon()

        # monta UI
        self._build_ui()

        # aplica tema padrão + estado persistido do slider
        self._apply_theme_from_config()

        # se já existe planilha salva
        if self.file_path:
            self._apply_file_path(self.file_path, prepare=True, silent=True)

    # ---------- ícones / tint ----------

    def _apply_window_icon(self) -> None:
        icon_path = self.cfg_ui.get("window_icon", "")
        if file_exists(icon_path):
            self.setWindowIcon(QIcon(abs_path(icon_path)))

    def _load_pixmap(self, path: str) -> Optional[QPixmap]:
        ap = abs_path(path)
        if not ap or not os.path.exists(ap):
            return None
        if ap in self._pixmap_cache:
            return self._pixmap_cache[ap]
        pm = QPixmap(ap)
        if pm.isNull():
            return None
        self._pixmap_cache[ap] = pm
        return pm

    def _tint_pixmap(self, pixmap: QPixmap, tint_hex: str) -> QPixmap:
        """
        Aplica tint usando o alpha do pixmap. Requer PNG com transparência para melhor resultado.
        """
        tinted = QPixmap(pixmap.size())
        tinted.fill(Qt.transparent)

        painter = QPainter(tinted)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(tinted.rect(), QColor(tint_hex))
        painter.end()

        return tinted

    def _icon_for_key(self, key: str, tint_hex: str) -> Optional[QIcon]:
        icons = self.cfg_ui.get("button_icons", {}) or {}
        p = icons.get(key, "")
        if not p or not file_exists(p):
            return None
        pm = self._load_pixmap(p)
        if not pm:
            return None
        return QIcon(self._tint_pixmap(pm, tint_hex))

    def _apply_button_icon(self, btn: QPushButton, key: str, tint_hex: str) -> None:
        ic = self._icon_for_key(key, tint_hex)
        if ic:
            btn.setIcon(ic)

    # ---------- tema (cores) ----------

    def _apply_theme_from_config(self) -> None:
        base_theme = dict(DEFAULT_THEME)
        # se o json tiver theme, usa como base (mas garantindo defaults)
        base_theme.update(self.cfg_ui.get("theme", {}) or {})

        hsl = self.cfg_ui.get("background_hsl", {}) or {}
        h = int(hsl.get("h", 210))
        s = int(hsl.get("s", 49))
        l = int(hsl.get("l", 8))

        r, g, b = hsl_to_rgb(h, s, l)
        bg_hex = rgb_to_hex(r, g, b)

        derived = derive_theme_from_background(bg_hex, base_theme)

        # persiste tema derivado também (registro em arquivo)
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

        # Após aplicar tema, retinta ícones
        self._retint_all_icons(theme)

    def _retint_all_icons(self, theme: dict) -> None:
        text = theme["text"]
        # botões principais: ícone branco faz mais sentido
        white = "#FFFFFF"

        self._apply_button_icon(self.btn_file, "choose_file", text)
        self._apply_button_icon(self.btn_add_field, "add_field", text)
        self._apply_button_icon(self.btn_clear, "clear", text)
        self._apply_button_icon(self.btn_save, "save_lead", white)
        self._apply_button_icon(self.btn_settings, "settings", text)

        # botões por campo são recriados; então retint ocorre no render_fields()
        self._last_theme_for_fields = theme  # usado no render_fields()

        # Força re-render para retint dos botões de linha
        self.render_fields()

    # ---------- build UI ----------

    def _build_ui(self) -> None:
        self.setWindowTitle("Cadastro de Leads (Local)")
        self.setMinimumWidth(980)

        root = QVBoxLayout()

        # Linha de arquivo + engrenagem
        file_row = QHBoxLayout()

        self.btn_file = QPushButton("Escolher planilha…")
        self.lbl_file = QLabel("Arquivo: (não selecionado)")
        self.lbl_file.setWordWrap(True)
        self.btn_file.clicked.connect(self.choose_file)

        self.btn_settings = QPushButton("")
        self.btn_settings.setToolTip("Configurações de tema")
        self.btn_settings.setFixedWidth(44)
        self.btn_settings.clicked.connect(self.open_theme_settings)

        file_row.addWidget(self.btn_file)
        file_row.addWidget(self.lbl_file, 1)
        file_row.addWidget(self.btn_settings)
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
        self.btn_save = QPushButton("Salvar lead (nova linha)")
        self.btn_clear = QPushButton("Limpar")

        self.btn_save.setProperty("variant", "primary")

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
        self.lbl_status.setObjectName("Status")
        root.addWidget(self.lbl_status)

        self.setLayout(root)

        self._last_theme_for_fields = dict(DEFAULT_THEME)
        self.render_fields()

        if self.file_path:
            self.lbl_file.setText(f"Arquivo: {self.file_path}")

    def render_fields(self) -> None:
        while self.fields_layout.count():
            item = self.fields_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        self.inputs.clear()
        theme = getattr(self, "_last_theme_for_fields", dict(DEFAULT_THEME))
        text = theme.get("text", "#E6EDF7")
        white = "#FFFFFF"

        for campo in self.campos:
            row = QHBoxLayout()

            lbl = QLabel(campo.titulo)
            lbl.setMinimumWidth(240)

            inp = QLineEdit()
            inp.setPlaceholderText(f"Digite ou cole: {campo.titulo}")
            self.inputs[campo.id] = inp

            btn_edit = QPushButton("Editar")
            btn_del = QPushButton("Excluir")

            self._apply_button_icon(btn_edit, "edit_title", text)
            self._apply_button_icon(btn_del, "delete_field", white)

            btn_edit.clicked.connect(lambda _=False, cid=campo.id: self.edit_field_title(cid))
            btn_del.clicked.connect(lambda _=False, cid=campo.id: self.delete_field(cid))
            btn_del.setProperty("variant", "danger")

            row.addWidget(lbl)
            row.addWidget(inp, 1)
            row.addWidget(btn_edit)
            row.addWidget(btn_del)

            wrap = QWidget()
            wrap.setLayout(row)
            self.fields_layout.addWidget(wrap)

        self.fields_layout.addStretch(1)

    # ---------- persistência ----------

    def _persist_campos(self) -> None:
        self.cfg_fields["campos"] = [c.__dict__ for c in self.campos]
        save_fields_config(self.cfg_fields)

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

    # ---------- ações gerais ----------

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

    # ---------- configurações (engrenagem) ----------

    def open_theme_settings(self) -> None:
        hsl = self.cfg_ui.get("background_hsl", {}) or {}
        h = int(hsl.get("h", 210))
        s = int(hsl.get("s", 49))
        l = int(hsl.get("l", 8))

        before_cfg = json.loads(json.dumps(self.cfg_ui))
        before_theme = dict(self.cfg_ui.get("theme", dict(DEFAULT_THEME)))

        dlg = ThemeDialog(self, h, s, l)

        # live update: ao mover slider, aplica imediatamente
        def on_change():
            hh, ss, ll = dlg.values()
            rr, gg, bb = hsl_to_rgb(hh, ss, ll)
            bg_hex = rgb_to_hex(rr, gg, bb)
            base = dict(DEFAULT_THEME)
            base.update(before_theme)  # base do padrão
            derived = derive_theme_from_background(bg_hex, base)
            self._apply_theme(derived)

        dlg.slider_h.valueChanged.connect(on_change)
        dlg.slider_s.valueChanged.connect(on_change)
        dlg.slider_l.valueChanged.connect(on_change)

        # primeira prévia
        on_change()

        if dlg.exec() == QDialog.Accepted:
            hh, ss, ll = dlg.values()
            # recalcula e persiste
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
            # cancel: restaura
            self.cfg_ui = before_cfg
            save_ui_config(self.cfg_ui)
            self._apply_theme(before_theme)


def main() -> None:
    app = QApplication([])
    w = App()
    w.show()
    app.exec()


if __name__ == "__main__":
    main()
