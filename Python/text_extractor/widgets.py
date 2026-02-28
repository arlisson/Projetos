# widgets.py
from __future__ import annotations

from typing import List, Optional, Tuple

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
)


class EmailInputWidget(QWidget):
    """
    Encapsula:
    - QLineEdit (parte local) + QComboBox (domínio)
    - Monta e lê email final
    - Atualiza lista de domínios preservando seleção
    """

    def __init__(self, domains: List[str], parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.inp_local = QLineEdit()
        self.inp_local.setPlaceholderText("usuario (ou cole e-mail completo)")

        self.cmb_domain = QComboBox()
        self.cmb_domain.setEditable(True)
        self.cmb_domain.setInsertPolicy(QComboBox.InsertAtTop)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.inp_local, 1)
        layout.addWidget(self.cmb_domain, 0)
        self.setLayout(layout)

        self.set_domains(domains)

    def set_domains(self, domains: List[str]) -> None:
        cur = (self.domain() or "").strip()

        self.cmb_domain.blockSignals(True)

        self.cmb_domain.setEditable(False)  # garante que não é editável
        self.cmb_domain.clear()

        # popula
        items = [str(d).strip() for d in (domains or []) if str(d).strip()]
        for d in items:
            self.cmb_domain.addItem(d)

        # seleção:
        # - se o domínio anterior ainda existir na lista, mantém
        # - senão, marca a primeira opção (se existir)
        if cur and cur in items:
            self.cmb_domain.setCurrentText(cur)
        elif self.cmb_domain.count() > 0:
            self.cmb_domain.setCurrentIndex(0)

        self.cmb_domain.blockSignals(False)

    def local(self) -> str:
        return (self.inp_local.text() or "").strip()

    def domain(self) -> str:
        return (self.cmb_domain.currentText() or "").strip()

    def set_parts(self, local: str, domain: str) -> None:
        self.inp_local.setText((local or "").strip())
        self.cmb_domain.setCurrentText((domain or "").strip())

    def set_email(self, email: str) -> None:
        s = (email or "").strip()
        if "@" in s:
            u, d = s.split("@", 1)
            self.set_parts(u, ("@" + d) if d else "")
        else:
            self.set_parts(s, "")

    def get_email(self) -> Tuple[str, bool]:
        """
        Retorna (email_final, ok).
        Regras:
        - Se o local contém '@', considera colado completo e retorna ok=True
        - Se local não vazio e domínio vazio => ok=False
        - Se local vazio => retorna "" e ok=True (campo em branco)
        """
        local = self.local()
        dom = self.domain()

        if not local:
            return ("", True)

        if "@" in local:
            return (local, True)

        if dom and not dom.startswith("@"):
            dom = "@" + dom

        if not dom:
            return ("", False)

        return (local + dom, True)


class FieldRowWidget(QWidget):
    editRequested = Signal(str)
    deleteRequested = Signal(str)

    def __init__(
        self,
        field_id: str,
        label_text: str,
        input_widget: QWidget,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)
        self.field_id = field_id

        self.lbl = QLabel(label_text)
        self.lbl.setMinimumWidth(160)

        self.btn_edit = QPushButton("Editar")
        self.btn_del = QPushButton("Excluir")
        self.btn_del.setProperty("variant", "danger")

        self.btn_edit.clicked.connect(lambda: self.editRequested.emit(self.field_id))
        self.btn_del.clicked.connect(lambda: self.deleteRequested.emit(self.field_id))

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.addWidget(self.lbl)
        row.addWidget(input_widget, 1)
        row.addWidget(self.btn_edit)
        row.addWidget(self.btn_del)

        self.setLayout(row)

# widgets.py (adicione)


class BoolInputWidget(QWidget):
    """
    Booleano como seleção (não texto).
    Guarda: "" | "Sim" | "Não"
    """
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.cmb = QComboBox()
        # self.cmb.addItem("")      # vazio permitido
        self.cmb.addItem("Sim")
        self.cmb.addItem("Não")

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.cmb, 1)
        self.setLayout(layout)

    def value(self) -> str:
        return (self.cmb.currentText() or "").strip()

    def set_value(self, v: str) -> None:
        s = (v or "").strip()
        # aceita variações comuns
        low = s.lower()
        if low in {"sim", "s", "yes", "y", "true", "1"}:
            s = "Sim"
        elif low in {"não", "nao", "n", "no", "false", "0"}:
            s = "Não"
        elif s not in {"", "Sim", "Não"}:
            s = ""
        self.cmb.setCurrentText(s)