# dialogs.py
from __future__ import annotations

from typing import Tuple, List

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QSlider,
    QLabel,
    QFormLayout,
    QDialogButtonBox,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QInputDialog,
    QLineEdit,
)


class ThemeDialog(QDialog):
    def __init__(self, parent: QWidget, h: int, s: int, l: int):
        """ Método construtor do diálogo de ajuste de tema.
 
        Args:
            parent (QWidget): Widget pai do diálogo.
            h (int): Valor do tom da cor (0-359).
            s (int): Valor da saturação (0-100).
            l (int): Valor do brilho (0-100).
        """
        super().__init__(parent)
        self.setWindowTitle("Ajustar tema")
        self.setModal(True)
        self.setMinimumWidth(240)

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
        form.addRow("Tom da cor", self.slider_h)
        form.addRow("Saturação", self.slider_s)
        form.addRow("Brilho", self.slider_l)

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.lbl_preview)
        layout.addWidget(btns)
        self.setLayout(layout)

        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)

    def values(self) -> Tuple[int, int, int]:
        """ Retorna os valores atuais dos sliders de cor.
 
        Returns:
            Tuple[int, int, int]: Valores do tom, saturação e brilho.
        """
        return self.slider_h.value(), self.slider_s.value(), self.slider_l.value()


class CursorStartLineEdit(QLineEdit):
    """
    QLineEdit que força o cursor para o início ao receber foco/clique.
    Útil para campos com inputMask (telefone, data) para facilitar colar.

    """

    def __init__(self, *args, force_cursor_start: bool = False, **kwargs):
        """ Inicializa o CursorStartLineEdit.

        Args:
            force_cursor_start (bool, optional): Se True, o cursor será forçado para o início ao receber foco ou clique. Defaults to False.
        """
        super().__init__(*args, **kwargs)
        self._force_cursor_start = force_cursor_start

    def set_force_cursor_start(self, enabled: bool) -> None:
        """ Define se o cursor será forçado para o início ao receber foco ou clique.
        
        Args:
            enabled (bool): Se True, o cursor será forçado para o início ao receber foco ou clique.
        """
        self._force_cursor_start = bool(enabled)

    def _move_cursor_to_start(self) -> None:
        """ Move o cursor para o início do campo de texto e desmarca qualquer seleção.
        """
        if self._force_cursor_start:
            self.setCursorPosition(0)
            self.deselect()

    def focusInEvent(self, event):
        """ Sobrescreve o evento de foco para mover o cursor para o início se a opção estiver habilitada.    

        Args:
            event (_type_): Evento de foco recebido.
        """
        super().focusInEvent(event)
        if self._force_cursor_start:
            QTimer.singleShot(0, self._move_cursor_to_start)

    def mousePressEvent(self, event):
        """ Sobrescreve o evento de clique do mouse para mover o cursor para o início se a opção estiver habilitada.
        Args:
            event (_type_): Evento de clique do mouse recebido.
        """
        super().mousePressEvent(event)
        if self._force_cursor_start:
            QTimer.singleShot(0, self._move_cursor_to_start)


class EmailDomainsDialog(QDialog):
    def __init__(self, parent: QWidget, domains: List[str]):
        super().__init__(parent)
        self.setWindowTitle("Domínios de e-mail")
        self.setModal(True)
        self.setMinimumWidth(360)

        self.listw = QListWidget()
        for d in list(domains):
            QListWidgetItem(d, self.listw)

        self.btn_add = QPushButton("Adicionar")
        self.btn_edit = QPushButton("Editar")
        self.btn_del = QPushButton("Remover")

        row = QHBoxLayout()
        row.addWidget(self.btn_add)
        row.addWidget(self.btn_edit)
        row.addWidget(self.btn_del)

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Domínios disponíveis (inclua ou não '@', o app normaliza):"))
        layout.addWidget(self.listw, 1)
        layout.addLayout(row)
        layout.addWidget(btns)
        self.setLayout(layout)

        self.btn_add.clicked.connect(self._add)
        self.btn_edit.clicked.connect(self._edit)
        self.btn_del.clicked.connect(self._del)

        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)

    def domains(self) -> List[str]:
        out: List[str] = []
        for i in range(self.listw.count()):
            s = (self.listw.item(i).text() or "").strip()
            if not s:
                continue
            if not s.startswith("@"):
                s = "@" + s
            if s not in out:
                out.append(s)
        return out

    def _add(self):
        v, ok = QInputDialog.getText(self, "Adicionar domínio", "Domínio (ex.: @gmail.com):")
        if not ok:
            return
        s = (v or "").strip()
        if not s:
            return
        if not s.startswith("@"):
            s = "@" + s
        for i in range(self.listw.count()):
            if self.listw.item(i).text() == s:
                return
        QListWidgetItem(s, self.listw)

    def _edit(self):
        item = self.listw.currentItem()
        if not item:
            return
        cur = item.text()
        v, ok = QInputDialog.getText(self, "Editar domínio", "Domínio:", text=cur)
        if not ok:
            return
        s = (v or "").strip()
        if not s:
            return
        if not s.startswith("@"):
            s = "@" + s
        item.setText(s)

    def _del(self):
        row = self.listw.currentRow()
        if row < 0:
            return
        self.listw.takeItem(row)