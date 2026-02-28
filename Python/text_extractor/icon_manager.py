# icon_manager.py
from __future__ import annotations

import os
from typing import Callable, Optional, Dict

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QColor, QPainter
from PySide6.QtWidgets import QPushButton


class IconManager:
    """
    Centraliza:
    - Resolução de caminho (ex.: PyInstaller _MEIPASS via resolver externo)
    - Cache de QPixmap
    - Tint dos ícones (SourceIn)
    - Aplicação em botões por key (lido do ui_cfg["button_icons"])
    """

    def __init__(
        self,
        ui_cfg: dict,
        abs_path: Callable[[str], str],
        file_exists: Callable[[str], bool],
    ) -> None:
        self.ui_cfg = ui_cfg
        self.abs_path = abs_path
        self.file_exists = file_exists
        self._pixmap_cache: Dict[str, QPixmap] = {}

    def _load_pixmap(self, path: str) -> Optional[QPixmap]:
        ap = self.abs_path(path)
        if not ap or not os.path.exists(ap):
            return None
        if ap in self._pixmap_cache:
            return self._pixmap_cache[ap]
        pm = QPixmap(ap)
        if pm.isNull():
            return None
        self._pixmap_cache[ap] = pm
        return pm

    @staticmethod
    def _tint_pixmap(pixmap: QPixmap, tint_hex: str) -> QPixmap:
        tinted = QPixmap(pixmap.size())
        tinted.fill(Qt.transparent)

        painter = QPainter(tinted)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(tinted.rect(), QColor(tint_hex))
        painter.end()

        return tinted

    def icon_for_key(self, key: str, tint_hex: str) -> Optional[QIcon]:
        icons = self.ui_cfg.get("button_icons", {}) or {}
        p = icons.get(key, "")
        if not p or not self.file_exists(p):
            return None
        pm = self._load_pixmap(p)
        if not pm:
            return None
        return QIcon(self._tint_pixmap(pm, tint_hex))

    def apply_button_icon(self, btn: QPushButton, key: str, tint_hex: str) -> None:
        ic = self.icon_for_key(key, tint_hex)
        if ic:
            btn.setIcon(ic)

    def clear_cache(self) -> None:
        self._pixmap_cache.clear()