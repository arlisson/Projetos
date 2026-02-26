# license_dialog.py
import os
import sys
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QDialogButtonBox


def abs_path(p: str) -> str:
    """
    Resolve caminho absoluto considerando PyInstaller (sys._MEIPASS).
    """
    if not p:
        return ""
    if os.path.isabs(p):
        return p
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, p)


def read_license_text(
    preferred_names: Optional[list[str]] = None,
    fallback_message: str = (
        "Licença não encontrada.\n\n"
        "Inclua um arquivo LICENSE.pt-BR.txt (ou LICENSE.txt / LICENSE) junto ao instalador."
    ),
) -> str:
    """
    Lê o texto de licença de arquivos comuns no diretório do app (ou empacotado).
    Ordem padrão:
      - LICENSE.pt-BR.txt
      - LICENSE.txt
      - LICENSE
    """
    candidates = preferred_names or ["LICENSE.pt-br.txt", "LICENSE.txt", "LICENSE"]
    for name in candidates:
        p = abs_path(name)
        if p and os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                # tenta próximo candidato
                pass
    return fallback_message


class LicenseDialog(QDialog):
    def __init__(self, parent=None, theme: Optional[dict] = None, license_text: str = ""):
        super().__init__(parent)
        self.setWindowTitle("Licença")
        self.setModal(True)
        self.resize(720, 520)

        self.txt = QTextEdit()
        self.txt.setReadOnly(True)
        self.txt.setPlainText(license_text or "")
        self.txt.setLineWrapMode(QTextEdit.WidgetWidth)

        f = QFont()
        f.setPointSize(11)
        self.txt.setFont(f)

        btns = QDialogButtonBox(QDialogButtonBox.Close)
        btns.rejected.connect(self.reject)
        btns.accepted.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.txt, 1)
        layout.addWidget(btns)
        self.setLayout(layout)

        if theme:
            self.apply_theme(theme)

    def apply_theme(self, theme: dict) -> None:
        bg = theme.get("background", "#0B1220")
        surface = theme.get("surface", "#0F1A2B")
        text = theme.get("text", "#E6EDF7")
        border = theme.get("border", "#1F2A44")

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {bg};
                color: {text};
            }}
            QTextEdit {{
                background-color: {surface};
                color: {text};
                border: 1px solid {border};
                border-radius: 10px;
                padding: 10px;
            }}
            QPushButton {{
                background-color: {surface};
                color: {text};
                border: 1px solid {border};
                border-radius: 10px;
                padding: 8px 12px;
            }}
        """)