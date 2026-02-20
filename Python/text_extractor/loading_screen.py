# loading_screen.py
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QSplashScreen


class LoadingScreen:
    def __init__(
        self,
        app: QApplication,
        title: str = "Iniciando",
        subtitle: str = "Aguarde enquanto validamos o acesso...",
        width: int = 520,
        height: int = 220,
        bg: str = "#0B1220",
        accent: str = "#3B82F6",
        text: str = "#E6EDF7",
        muted: str = "#A7B3C6",
    ) -> None:
        self._app = app
        self._title = title
        self._subtitle = subtitle
        self._width = width
        self._height = height

        self._bg = QColor(bg)
        self._accent = QColor(accent)
        self._text = QColor(text)
        self._muted = QColor(muted)

        pixmap = self._make_pixmap()
        self._splash = QSplashScreen(pixmap)
        self._splash.setWindowFlag(Qt.WindowStaysOnTopHint, True)

    def _make_pixmap(self) -> QPixmap:
        pm = QPixmap(self._width, self._height)
        pm.fill(self._bg)

        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing, True)

        p.fillRect(0, 0, self._width, 6, self._accent)

        p.setPen(self._text)
        ft = QFont()
        ft.setPointSize(16)
        ft.setBold(True)
        p.setFont(ft)
        p.drawText(24, 70, self._title)

        p.setPen(self._muted)
        fs = QFont()
        fs.setPointSize(10)
        p.setFont(fs)
        p.drawText(24, 100, self._subtitle)

        p.end()
        return pm

    def show(self, message: str = "Preparando...") -> None:
        self._splash.show()
        self.update(message)

    def update(self, message: str) -> None:
        self._splash.showMessage(message, Qt.AlignBottom | Qt.AlignLeft, self._muted)
        self._app.processEvents()

    def hide(self) -> None:
        self._splash.hide()
        self._app.processEvents()

    def close(self) -> None:
        self._splash.close()
        self._app.processEvents()

    def finish_and_close(self, main_window) -> None:
        """
        Fecha o splash de forma confiável.
        - finish() tenta sincronizar com a janela principal
        - close() garante o fechamento mesmo se a janela ainda não foi "exposta"
        """
        self._app.processEvents()
        self._splash.finish(main_window)
        self._app.processEvents()
        self._splash.close()
        self._app.processEvents()