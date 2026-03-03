# app.py (editado: footer via controle_ui.json e engrenagem abre tema + domínios + abas com sync automático)
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

from PySide6.QtCore import QUrl, Qt, QTimer
from PySide6.QtGui import QDesktopServices, QIcon, QPixmap
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
    QComboBox,
)

from colors import (
    DEFAULT_THEME,
    hsl_to_rgb,
    rgb_to_hex,
    derive_theme_from_background,
)

from config import (
    get_sheet_campos,
    load_fields_config,
    save_fields_config,
    load_ui_config,
    save_ui_config,
    get_last_sheet_path,
    save_sheet_config,
    load_email_domains_config,
    save_email_domains_config,
    set_sheet_campos,
    rename_sheet_key,  # <-- necessário para refletir rename de abas no controle
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
    ensure_sheet_exists,
    is_excel_lock_present,
    list_sheets_with_ids,
    read_headers_from_excel,
    write_headers_from_campos,
    ensure_workbook,
    apply_column_type_rules,
    append_row_typed,
    delete_column_by_header,
    rename_column_header,
    list_sheets, 
)

from dialogs import (
    ThemeDialog,
    CursorStartLineEdit,
    EmailDomainsDialog,
)

from icon_manager import IconManager
from widgets import EmailInputWidget, FieldRowWidget, BoolInputWidget


def abs_path(p: str) -> str:
    """    
    Resolve um caminho de arquivo para um caminho absoluto.

    Esta função é crucial para lidar com recursos em um aplicativo que pode ser
    executado tanto em um ambiente de desenvolvimento quanto como um executável
    "congelado" (por exemplo, com PyInstaller).

    - Se o caminho já for absoluto, ele é retornado sem modificação.
    - Se o caminho for relativo, a função determina o diretório base:
        - Em um executável PyInstaller, usa o diretório temporário `_MEIPASS`.
        - Em um script Python normal, usa o diretório do próprio script.
    - O caminho relativo é então combinado com este diretório base.

    Args:
       
        p (str): O caminho do arquivo a ser resolvido.

    Returns:
      
        str: O caminho absoluto correspondente, ou uma string vazia se a entrada for nula/vazia.
    """
    if not p:
        return ""
    if os.path.isabs(p):
        return p
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, p)


def file_exists(p: str) -> bool:
    """
    Verifica se um arquivo existe e pode ser lido.

    Args:
        p (str): String que representa o caminho para o arquivo a ser verificado.

    Returns:
        bool: True se o arquivo existe e pode ser lido, False caso contrário.
    """
    ap = abs_path(p)
    return bool(ap) and os.path.exists(ap)


class SettingsDialog(QDialog):
    """
    Classe de diálogo para gerenciar as configurações globais do aplicativo, permitindo ao usuário acessar os ajustes de tema visual e a lista de domínios de e-mail sugeridos.
    
    Args:
        QDialog (_type_): Objeto do tipo QDialog.
    """
    def __init__(self, parent: "App"):
        """
        Funcção de inicialização do diálogo de configurações.
        
        Args:
            parent (App): A instância principal do aplicativo que gerencia o estado e as configurações.
            
        """
        super().__init__(parent)
        self.setWindowTitle("Configurações")
        self.setModal(True)
        self.setMinimumWidth(360)

        self.parent_app = parent

        self.lbl = QLabel("Escolha o que deseja editar:")
        self.btn_theme = QPushButton("Tema de cores")
        self.btn_theme.setToolTip("Configurar o tema de cores do aplicativo")
        self.btn_domains = QPushButton("Domínios de e-mail")
        self.btn_domains.setToolTip("Configurar a lista de domínios sugeridos para campos de email")

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
        """ 
        Abre o diálogo de ajuste de tema de cores, permitindo ao usuário modificar a aparência visual do aplicativo.
        
        """
        self.parent_app.open_theme_settings()

    def _open_domains(self) -> None:
        """
        Abre o diálogo de gerenciamento de domínios de e-mail. Após o fechamento do diálogo, 
        atualiza a lista de domínios no aplicativo e sincroniza os widgets de entrada de e-mail existentes.
        
        """
        self.parent_app.open_email_domains()
        self.btn_domains.setEnabled(self.parent_app._has_email_fields())


class App(QWidget):
    """
    Interface principal do aplicativo "Preenche Fácil".
    Gerencia a configuração de campos, a interface de usuário dinâmica,
    a integração com planilhas Excel e a persistência de dados.

    
    Args:
        QWidget (_type_): Objeto do tipo QWidget. 
    """
    def __init__(self):
        """
        Inicializa a aplicação, carrega as configurações de campos, UI e domínios de e-mail, 
        e configura a interface do usuário e o monitoramento da planilha.        

        """
        super().__init__()

        self.cfg_fields = load_fields_config(FIELD_TYPES)
        self.cfg_ui = load_ui_config()

        self.cfg_email = load_email_domains_config()
        self.email_domains: List[str] = self.cfg_email.get("dominios", [])

        self.sheet_name: str = self.cfg_fields.get("aba", "Preenche Fácil")
        self.file_path: Optional[str] = get_last_sheet_path()

        sheet_campos = get_sheet_campos(self.cfg_fields, self.sheet_name)
        self.campos: List[Campo] = [Campo(**c) for c in (sheet_campos or [])]

        # inputs[field_id] = QLineEdit | EmailInputWidget
        self.inputs: Dict[str, Any] = {}

        self.icon_mgr = IconManager(self.cfg_ui, abs_path=abs_path, file_exists=file_exists)

        # monitor state
        self._sheet_last_sig = None  # (mtime, size)
        self._sheet_monitor_timer: Optional[QTimer] = None
        self._last_sheets_meta: List[Tuple[int, str]] = []

        self._apply_window_icon()
        self._build_ui()
        self._apply_theme_from_config()

        if self.file_path:
            self._apply_file_path(self.file_path, prepare=True, silent=True)

        # só começa o monitor depois da UI existir e depois de aplicar planilha
        self._start_sheet_monitor()

    def open_license(self) -> None:
        """
        Abre o diálogo de informações da licença, exibindo o texto da licença
        e aplicando o tema visual atual do aplicativo.
        """
        theme = (self.cfg_ui.get("theme") or dict(DEFAULT_THEME))
        text = read_license_text()
        dlg = LicenseDialog(self, theme=theme, license_text=text)
        dlg.exec()

    def _apply_window_icon(self) -> None:
        """
        Aplica o ícone da janela do aplicativo a partir das configurações da UI.
        """
        icon_path = self.cfg_ui.get("window_icon", "")
        if file_exists(icon_path):
            self.setWindowIcon(QIcon(abs_path(icon_path)))

    # ---------- tema ----------

    def _apply_theme_from_config(self) -> None:
        """
        Aplica o tema visual do aplicativo com base nas configurações carregadas.
        Calcula as cores derivadas a partir dos valores HSL do plano de fundo e
        atualiza o folha de estilos (stylesheet) e os ícones.
        
        
        """
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
        """
        Aplica o tema visual (cores e estilos) a todos os widgets da interface.
        
        Args:
            theme (dict): Dicionário contendo as cores hexadecimais para cada elemento da UI.
    
        
        """
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
           QWidget#PromoFooter {{
                /* Banner discreto e consistente com o tema */
                background-color: {surface_alt};
                border: 1px solid {border};
                border-radius: 12px;
            }}

            /* Barra de destaque à esquerda (chama atenção sem gritar) */
            QWidget#PromoFooter {{
                border-left: 6px solid {primary};
            }}

            /* IMPORTANTÍSSIMO: evita o “retângulo preto” interno */
            QWidget#PromoFooter QLabel,
            QWidget#PromoFooter QPushButton {{
                background-color: transparent;
            }}

            /* Tipografia do texto do rodapé */
            QWidget#PromoFooter QLabel {{
                font-size: 13px;
                font-weight: 650;
                color: {text};
            }}

            /* Botão Licença mais “neutro” dentro do banner */
            QWidget#PromoFooter QPushButton {{
                background-color: transparent;
                border: 1px solid {border};
                padding: 6px 10px;
                border-radius: 10px;
            }}

            QWidget#PromoFooter QPushButton:hover {{
                border-color: {primary};
            }}
                           

        """)

        self._retint_all_icons(theme)

    def _retint_all_icons(self, theme: dict) -> None:
        """
        Atualiza a cor de todos os ícones da interface para que correspondam ao tema atual.
    
        
        Args:
            theme (dict): Um dicionário contendo cores hexadecimais para cada elemento da UI.
        
        """
        text = theme["text"]
        white = "#FFFFFF"

        self.icon_mgr.apply_button_icon(self.btn_file, "choose_file", text)
        self.icon_mgr.apply_button_icon(self.btn_add_field, "add_field", text)
        self.icon_mgr.apply_button_icon(self.btn_clear, "clear", text)
        self.icon_mgr.apply_button_icon(self.btn_save, "save_lead", white)
        self.icon_mgr.apply_button_icon(self.btn_settings, "settings", text)
        self.icon_mgr.apply_button_icon(self.btn_refresh_sheets, "refresh", text)
        self.icon_mgr.apply_button_icon(self.btn_help, "help", text)

        self._last_theme_for_fields = theme
        self.render_fields()

    # ---------- domínios email ----------

    def _has_email_fields(self) -> bool:
        """

        Verifica se a lista de campos atual contém ao menos um campo do tipo 'email'.
        
        Returns:
            bool: True se houver campos de e-mail, False caso contrário.
        
        
        """
        return any(c.tipo == "email" for c in self.campos)

    def open_email_domains(self) -> None:
        """
        Abre o diálogo de gerenciamento de domínios de e-mail. 
        Permite adicionar, editar ou remover domínios da lista de sugestões.
        Ao aceitar, salva as alterações e atualiza todos os widgets de e-mail ativos.
        
        
        """
        dlg = EmailDomainsDialog(self, domains=list(self.email_domains))
        if dlg.exec() == QDialog.Accepted:
            self.email_domains = dlg.domains()
            self.cfg_email["dominios"] = list(self.email_domains)
            save_email_domains_config(self.cfg_email)
            self._refresh_email_domain_widgets()

    def _refresh_email_domain_widgets(self) -> None:
        """
        Atualiza a lista de domínios em todos os widgets de entrada de e-mail ativos, 
        preservando o texto já digitado pelo usuário.
        

        """
        for c in self.campos:
            if c.tipo != "email":
                continue
            w = self.inputs.get(c.id)
            if isinstance(w, EmailInputWidget):
                w.set_domains(self.email_domains)

    # ----------- Abas Excel (UI + Sync) -----------

    def _reload_sheet_list(self) -> None:
        """Recarrega combobox de abas a partir do Excel e atualiza snapshot interno."""
        if not self.file_path or not os.path.exists(self.file_path):
            self.cmb_sheet.blockSignals(True)
            self.cmb_sheet.clear()
            self.cmb_sheet.blockSignals(False)
            self._last_sheets_meta = []
            return

        meta: List[Tuple[int, str]] = []

        # 1) tenta ler com IDs (melhor para detectar rename)
        try:
            meta = list_sheets_with_ids(self.file_path)
        except Exception:
            meta = []

        # 2) fallback: lê só os nomes e cria IDs artificiais
        if not meta:
            try:
                names = list_sheets(self.file_path)
                meta = [(i + 1, name) for i, name in enumerate(names)]
            except Exception:
                meta = []

        self._last_sheets_meta = meta
        self._reload_sheet_list_from_meta(meta)

    def _reload_sheet_list_from_meta(self, meta) -> None:
        """
        Atualiza o QComboBox de abas com base nos metadados fornecidos e sincroniza a aba selecionada.
                
        Args:
            meta (_type_): List[Tuple[int, str]] 
            
        """
        self.cmb_sheet.blockSignals(True)
        self.cmb_sheet.clear()

        titles = [t for _, t in meta]
        for t in titles:
            self.cmb_sheet.addItem(t)

        if self.sheet_name in titles:
            self.cmb_sheet.setCurrentText(self.sheet_name)
        elif titles:
            self.sheet_name = titles[0]
            self.cfg_fields["aba"] = self.sheet_name
            self.cmb_sheet.setCurrentIndex(0)

        self.cmb_sheet.blockSignals(False)

    def on_sheet_changed(self, new_sheet: str) -> None:
        """
        Atualiza a aba ativa e recarrega os campos correspondentes. Se a aba for nova, 
        tenta sincronizar os cabeçalhos a partir do arquivo Excel.        

        Args:
            new_sheet (str): String representando a nova aba
        """
        if not new_sheet or not self.file_path:
            return

        self.sheet_name = new_sheet
        self.cfg_fields["aba"] = self.sheet_name

        sheet_campos = get_sheet_campos(self.cfg_fields, self.sheet_name)
        if sheet_campos:
            self.campos = [Campo(**c) for c in sheet_campos]
            self.render_fields()
            save_fields_config(self.cfg_fields)
            return

        self.sync_fields_from_existing_excel(self.file_path)

    def create_new_sheet(self) -> None:
        """Função responsável por criar uma nova aba na planilha
        """
        if not self.file_path:
            QMessageBox.warning(self, "Atenção", "Selecione uma planilha primeiro.")
            return

        name, ok = QInputDialog.getText(self, "Nova aba", "Nome da nova aba:")
        if not ok or not name.strip():
            return

        name = name.strip()

        try:
            ensure_sheet_exists(self.file_path, name)

            headers = [c.titulo for c in self.campos]
            ensure_workbook(self.file_path, name, headers)
            apply_column_type_rules(self.file_path, name, self.campos)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao criar aba: {e}")
            return

        self._reload_sheet_list()
        self.cmb_sheet.setCurrentText(name)  # dispara on_sheet_changed

    def _snapshot_current_inputs(self) -> Dict[str, str]:
        """
        Captura o estado atual de todos os campos de entrada, mapeando o título do campo ao seu valor textual.
        Isso permite preservar os dados digitados pelo usuário durante operações de sincronização ou troca de abas.
        
        
        Returns:
            Dict[str, str]: Dicionário representando Título, Valor dos campos
        """
        by_title: Dict[str, str] = {}
        for c in self.campos:
            w = self.inputs.get(c.id)
            if isinstance(w, EmailInputWidget):
                val, _ = w.get_email()
                by_title[c.titulo] = val or ""
            elif isinstance(w, BoolInputWidget):
                by_title[c.titulo] = w.value() or ""
            elif isinstance(w, QLineEdit):
                by_title[c.titulo] = w.text() or ""
            else:
                by_title[c.titulo] = ""
        return by_title

    def _restore_inputs_by_title(self, by_title: Dict[str, str]) -> None:
        """
        Restaura os valores dos campos de entrada a partir de um dicionário de títulos e valores.
    
        

        Args:
            by_title (Dict[str, str]): Dicionário contendo os títulos dos campos como chaves e seus respectivos valores atuais como valores.
            
        """
        for c in self.campos:
            if c.titulo not in by_title:
                continue
            w = self.inputs.get(c.id)
            val = by_title.get(c.titulo, "")
            if isinstance(w, EmailInputWidget):
                w.set_email(val)
            elif isinstance(w, BoolInputWidget):
                w.set_value(val)
            elif isinstance(w, QLineEdit):
                w.setText(val)

    def _maybe_sync_sheets_from_excel(self) -> None:
        """        Verifica se houve mudanças nas abas do arquivo Excel (renomeação, exclusão ou adição) 
        e sincroniza o estado interno do aplicativo e a interface (combobox) sem perder o foco.
        """
        if not self.file_path or not os.path.exists(self.file_path):
            return

        # tenta com IDs; se falhar, tenta só nomes
        try:
            new_meta = list_sheets_with_ids(self.file_path)
        except Exception:
            new_meta = []

        if not new_meta:
            try:
                names = list_sheets(self.file_path)
                new_meta = [(i + 1, name) for i, name in enumerate(names)]
            except Exception:
                return

    def _maybe_sync_headers_from_excel(self) -> None:
        """        Verifica se o cabeçalho da planilha Excel mudou em relação aos campos atuais do aplicativo.
        Se houver divergência, sincroniza os campos automaticamente, preservando os valores
        que o usuário já digitou nos inputs.
        
        """
        if not self.file_path:
            return

        if self.focusWidget() and isinstance(self.focusWidget(), QLineEdit):
            return

        try:
            _sheet_used, headers, has_header = read_headers_from_excel(self.file_path, self.sheet_name)
        except Exception:
            return

        if not has_header or not headers:
            return

        current_titles = [c.titulo for c in self.campos]
        if headers == current_titles:
            return

        draft = self._snapshot_current_inputs()

        ok = self.sync_fields_from_existing_excel(self.file_path)
        if not ok:
            return

        self._restore_inputs_by_title(draft)
        self.lbl_status.setText("Campos atualizados automaticamente a partir do cabeçalho da planilha.")
    
    def refresh_sheets(self) -> None:
      
        if not self.file_path or not os.path.exists(self.file_path):
            QMessageBox.warning(self, "Atenção", "Selecione uma planilha primeiro.")
            return

        # Recarrega a lista de abas do arquivo
        self._reload_sheet_list()

        # Se a aba atual não existir mais, força fallback e carrega campos
        titles = [self.cmb_sheet.itemText(i) for i in range(self.cmb_sheet.count())]
        if self.sheet_name and self.sheet_name not in titles:
            old = self.sheet_name
            self.sheet_name = titles[0] if titles else ""
            self.cfg_fields["aba"] = self.sheet_name
            save_fields_config(self.cfg_fields)

            if self.sheet_name:
                # tenta carregar do controle; se não existir, importa do Excel
                sheet_campos = get_sheet_campos(self.cfg_fields, self.sheet_name)
                if sheet_campos:
                    self.campos = [Campo(**c) for c in sheet_campos]
                    self.render_fields()
                else:
                    self.sync_fields_from_existing_excel(self.file_path)

            self.lbl_status.setText(f"Aba '{old}' não existe mais. Alternando para '{self.sheet_name}'.")
            return

        # Aba existe: opcionalmente atualizar cabeçalhos desta aba também
        self._maybe_sync_headers_from_excel()
        self.lbl_status.setText("Abas atualizadas.")

    # ---------- configurações (engrenagem) ----------

    def open_settings(self) -> None:
        dlg = SettingsDialog(self)
        dlg.exec()

    def open_help(self) -> None:        
        try:
            url = self.cfg_ui.get("help_url", "").strip()
            if url:
                QDesktopServices.openUrl(QUrl(url))
            else:
                QMessageBox.information(self, "Ajuda", "Nenhum link de ajuda configurado.")
        except Exception:
            QMessageBox.warning(self, "Erro", "Não foi possível abrir o link de ajuda.")

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

        self.btn_help = QPushButton("")
        self.btn_help.setToolTip("Ajuda")
        self.btn_help.setFixedWidth(44)
        self.btn_help.clicked.connect(self.open_help)

        file_row.addWidget(self.btn_file)
        file_row.addWidget(self.lbl_file, 1)
        file_row.addWidget(self.btn_settings)
        file_row.addWidget(self.btn_help)
        root.addLayout(file_row)

        sheet_row = QHBoxLayout()

        self.cmb_sheet = QComboBox()
        self.cmb_sheet.setMinimumWidth(180)
        self.cmb_sheet.currentTextChanged.connect(self.on_sheet_changed)

        self.btn_new_sheet = QPushButton("Nova aba")
        self.btn_new_sheet.setToolTip("Criar nova aba na planilha")
        self.btn_new_sheet.clicked.connect(self.create_new_sheet)

        sheet_row.addWidget(QLabel("Aba:"))

        self.btn_refresh_sheets = QPushButton("↻ Atualizar")       
        self.btn_refresh_sheets.setToolTip("Atualizar abas da planilha")
        self.btn_refresh_sheets.setFixedWidth(100)
        self.btn_refresh_sheets.clicked.connect(self.refresh_sheets)

        sheet_row.addWidget(self.cmb_sheet, 1)
        sheet_row.addWidget(self.btn_new_sheet)
        sheet_row.addWidget(self.btn_refresh_sheets)
        
        self.cmb_sheet.setMinimumWidth(180)
        self.cmb_sheet.currentTextChanged.connect(self.on_sheet_changed)      
        

        root.addLayout(sheet_row)

        self.fields_container = QWidget()
        self.fields_layout = QVBoxLayout()
        self.fields_container.setLayout(self.fields_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.fields_container)
        root.addWidget(scroll, 1)

        actions = QHBoxLayout()

        self.btn_add_field = QPushButton("Adicionar Campo")
        self.btn_add_field.setToolTip("Adicionar novo campo de preenchimento")
        self.btn_save = QPushButton("Salvar (nova linha)")
        self.btn_save.setToolTip("Salvar os dados preenchidos como nova linha na planilha")
        self.btn_clear = QPushButton("Limpar")
        self.btn_clear.setToolTip("Limpar os campos para preencher com novos dados")


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

        # --- Rodapé (banner) com logo + CTA clicável ---
        footer_wrap = QWidget()
        footer_wrap.setObjectName("PromoFooter")

        footer_row = QHBoxLayout(footer_wrap)
        footer_row.setContentsMargins(12, 10, 12, 10)
        footer_row.setSpacing(10)

        default_footer = "<b>Se precisar de telefonia para sua empresa</b> → WhatsApp (22) 98812-4656"
        footer_html = (self.cfg_ui.get("footer_left_html") or default_footer)

        # Link do banner (WhatsApp/site)
        footer_link = (self.cfg_ui.get("footer_link") or "").strip()

        # Logo (opcional)
        logo_path = (self.cfg_ui.get("footer_logo_path") or "").strip()
        logo_h = int(self.cfg_ui.get("footer_logo_height") or 28)

        self.lbl_footer_logo = QLabel()
        self.lbl_footer_logo.setFixedHeight(logo_h)
        self.lbl_footer_logo.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        if logo_path:
            pix = QPixmap(abs_path(logo_path))
            if not pix.isNull():
                self.lbl_footer_logo.setPixmap(pix.scaledToHeight(logo_h, Qt.SmoothTransformation))

        self.lbl_footer_left = QLabel(footer_html)
        self.lbl_footer_left.setTextFormat(Qt.RichText)
        self.lbl_footer_left.setWordWrap(True)
        self.lbl_footer_left.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        footer_row.addWidget(self.lbl_footer_logo, 0)
        footer_row.addWidget(self.lbl_footer_left, 1)

        self.btn_license = QPushButton("Licença")
        self.btn_license.setToolTip("Ver informações da licença de uso do software")
        self.btn_license.clicked.connect(self.open_license)
        footer_row.addWidget(self.btn_license, 0, Qt.AlignRight)

        # Banner inteiro clicável
        if footer_link:
            footer_wrap.setCursor(Qt.PointingHandCursor)
            footer_wrap.mousePressEvent = lambda ev: QDesktopServices.openUrl(QUrl(footer_link))

        root.addWidget(footer_wrap)
        # --- fim rodapé ---

        self.setLayout(root)

        self._last_theme_for_fields = dict(DEFAULT_THEME)
        self.render_fields()

        if self.file_path:
            self.lbl_file.setText(f"Arquivo: {self.file_path}")
            self._reload_sheet_list()
            

    def _build_footer(self) -> QWidget:
        ui = self.cfg_ui  # ou como você já carrega controle_ui.json

        footer = QWidget()
        footer.setObjectName("promoFooter")

        row = QHBoxLayout(footer)
        row.setContentsMargins(12, 10, 12, 10)
        row.setSpacing(10)

        # Logo
        self.lbl_footer_logo = QLabel()
        self.lbl_footer_logo.setFixedHeight(int(ui.get("footer_logo_height", 28)))
        self.lbl_footer_logo.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        logo_path = ui.get("footer_logo_path", "")
        if logo_path:
            pix = QPixmap(abs_path(logo_path))  # use seu resolvedor (PyInstaller)
            if not pix.isNull():
                h = int(ui.get("footer_logo_height", 28))
                self.lbl_footer_logo.setPixmap(pix.scaledToHeight(h, Qt.SmoothTransformation))

        # Texto/CTA
        self.lbl_footer_left = QLabel(ui.get("footer_left_html", ""))
        self.lbl_footer_left.setTextFormat(Qt.RichText)
        self.lbl_footer_left.setOpenExternalLinks(False)  # vamos tratar clique no banner todo
        self.lbl_footer_left.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        # Botão licença (mantém, mas “menos chamativo”)
        self.btn_license = QPushButton("Licença")
        self.btn_license.setFixedWidth(90)

        row.addWidget(self.lbl_footer_logo, 0)
        row.addWidget(self.lbl_footer_left, 1)
        row.addWidget(self.btn_license, 0)

        # Banner clicável (WhatsApp/site)
        link = ui.get("footer_link", "").strip()
        if link:
            footer.mousePressEvent = lambda ev: QDesktopServices.openUrl(QUrl(link))

            # opcional: cursor “mão”
            footer.setCursor(Qt.PointingHandCursor)

        return footer

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
        prev_value: Dict[str, str] = {}
        prev_email_parts: Dict[str, Tuple[str, str]] = {}

        for cid, w in self.inputs.items():
            try:
                if isinstance(w, EmailInputWidget):
                    full, _ok = w.get_email()
                    prev_value[cid] = full or ""
                    prev_email_parts[cid] = (w.local(), w.domain())
                elif isinstance(w, BoolInputWidget):
                    prev_value[cid] = w.value()
                elif isinstance(w, QLineEdit):
                    prev_value[cid] = w.text() or ""
                else:
                    prev_value[cid] = ""
            except Exception:
                prev_value[cid] = ""

        while self.fields_layout.count():
            item = self.fields_layout.takeAt(0)
            ww = item.widget()
            if ww:
                ww.deleteLater()

        self.inputs.clear()

        theme = getattr(self, "_last_theme_for_fields", dict(DEFAULT_THEME))
        text = theme.get("text", "#E6EDF7")
        white = "#FFFFFF"

        for campo in self.campos:
            label_text = f"{campo.titulo}  [{campo.tipo}]"
           
            if campo.tipo == "email":
                emailw = EmailInputWidget(domains=self.email_domains)

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
                inp.setText(prev_value.get(campo.id, ""))
                self.inputs[campo.id] = inp
                input_widget = inp

            roww = FieldRowWidget(field_id=campo.id, label_text=label_text, input_widget=input_widget)
            roww.editRequested.connect(self.edit_field)
            roww.deleteRequested.connect(self.delete_field)

            self.icon_mgr.apply_button_icon(roww.btn_edit, "edit_title", text)
            self.icon_mgr.apply_button_icon(roww.btn_del, "delete_field", white)

            # estado do toggle
            locked = bool(getattr(campo, "locked", False))
            roww.set_locked(locked)
            roww.lockToggled.connect(self.on_field_lock_toggled)

            # NOVO: ícone aberto/fechado no botão de cadeado
            lock_icon_key = "lock_closed" if locked else "lock_open"
            self.icon_mgr.apply_button_icon(roww.btn_lock, lock_icon_key, text)

            # se estiver bloqueado, desabilita ações
            if getattr(campo, "locked", False):
                roww.btn_edit.setEnabled(False)
                roww.btn_del.setEnabled(False)
                roww.btn_edit.setToolTip("Campo protegido: não pode ser alterado.")
                roww.btn_del.setToolTip("Campo protegido: não pode ser excluído.")

            self.fields_layout.addWidget(roww)

        self.fields_layout.addStretch(1)

    # ---------- persistência ----------

    def _persist_campos(self) -> None:
        set_sheet_campos(self.cfg_fields, self.sheet_name, [c.__dict__ for c in self.campos])
        self.cfg_fields["aba"] = self.sheet_name
        save_fields_config(self.cfg_fields)

    def _apply_file_path(self, path: str, prepare: bool, silent: bool = False) -> None:
        self.file_path = path
        self.lbl_file.setText(f"Arquivo: {path}")
        save_sheet_config(path)

        # atualiza assinatura e lista de abas imediatamente
        try:
            self._sheet_last_sig = self._file_signature(path)
        except Exception:
            self._sheet_last_sig = None

        self._reload_sheet_list()

        if prepare:
            try:
                headers = [c.titulo for c in self.campos]
                ensure_workbook(self.file_path, self.sheet_name, headers)
                apply_column_type_rules(self.file_path, self.sheet_name, self.campos)
                if not silent:
                    self.lbl_status.setText("Planilha preparada e salva como padrão.")
            except Exception as e:
                self.lbl_status.setText(f"Erro ao preparar planilha: {e}")

    # ---------- monitor de mudanças do arquivo ----------

    def _start_sheet_monitor(self) -> None:
        if self._sheet_monitor_timer is not None:
            return               

        self._sheet_monitor_timer = QTimer(self)
        self._sheet_monitor_timer.setInterval(1200)
        self._sheet_monitor_timer.timeout.connect(self._check_sheet_changed)
        self._sheet_monitor_timer.start()

        # roda uma vez no início
        self._check_sheet_changed()

        # rodar uma vez no início (se existir planilha)
        if self.file_path and os.path.exists(self.file_path):
            try:
                self._sheet_last_sig = self._file_signature(self.file_path)
            except Exception:
                self._sheet_last_sig = None

            if hasattr(self, "_maybe_sync_sheets_from_excel"):
                self._maybe_sync_sheets_from_excel()
            if hasattr(self, "_maybe_sync_headers_from_excel"):
                self._maybe_sync_headers_from_excel()

    def _file_signature(self, path: str):
        st = os.stat(path)
        return (int(st.st_mtime), int(st.st_size))

    def _check_sheet_changed(self) -> None:
        if not self.file_path or not os.path.exists(self.file_path):
            return

        # 1) Sempre tenta sincronizar abas (deleção/rename/criação)
        # (se não mudou, a função retorna rápido)
        self._maybe_sync_sheets_from_excel()

        # 2) Só sincroniza cabeçalho quando o arquivo mudar de fato
        try:
            sig = self._file_signature(self.file_path)
        except Exception:
            return

        if self._sheet_last_sig is None:
            self._sheet_last_sig = sig
            return

        if sig != self._sheet_last_sig:
            self._sheet_last_sig = sig
            self._maybe_sync_headers_from_excel()

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
                locked = getattr(old, "locked", False)
                used_ids.add(cid)
            else:
                cid = make_unique_id(sanitize_id(h), used_ids)
                tipo = infer_type_from_title(h)
                if tipo not in FIELD_TYPES:
                    tipo = "texto"
                fixo = False
                locked = False

            new_campos.append(Campo(id=cid, titulo=h, tipo=tipo, fixo=fixo, locked=locked))

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

    

    # ---------- ações de campos ----------]
 
    def on_field_lock_toggled(self, field_id: str, locked: bool) -> None:
        campo = next((c for c in self.campos if c.id == field_id), None)
        if not campo:
            return

        campo.locked = bool(locked)
        self._persist_campos()
        self.render_fields()

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

        self.campos.append(Campo(id=cid, titulo=title, tipo=tipo, fixo=False, locked=False))
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

        if getattr(campo, "locked", False):
            QMessageBox.warning(self, "Campo protegido", "Este campo está bloqueado e não pode ser alterado.")
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
        
        if getattr(campo, "locked", False):
            QMessageBox.warning(self, "Campo protegido", "Este campo está bloqueado e não pode ser excluído.")
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

        if dlg.exec() == QDialog.Accepted:
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