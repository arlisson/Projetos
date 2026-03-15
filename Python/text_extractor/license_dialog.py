# license_dialog.py
import os
import sys
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QDialogButtonBox


def abs_path(p: str) -> str:
    """ Resolve um caminho de arquivo relativo para um caminho absoluto, considerando o diretório base do aplicativo ou o diretório de execução PyInstaller. O método verifica se o caminho fornecido é absoluto e, se for, retorna-o diretamente. Caso contrário, ele determina o diretório base usando a variável sys._MEIPASS (que é definida pelo PyInstaller durante a execução) ou o diretório do arquivo atual, e então combina esse diretório base com o caminho relativo fornecido para obter o caminho absoluto. Se a entrada for None ou vazia, o método retorna uma string vazia.
    Args:
        p (str): O caminho relativo do arquivo.

    Returns:
        str: O caminho absoluto do arquivo, considerando o diretório base do aplicativo ou o diretório de execução PyInstaller.
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
    Lê o conteúdo de um arquivo de licença a partir de uma lista de nomes de arquivos preferenciais, retornando o conteúdo do primeiro arquivo encontrado. O método itera sobre a lista de nomes de arquivos fornecida (ou uma lista padrão se None for fornecida) e tenta ler o conteúdo de cada arquivo usando o caminho absoluto resolvido. Se um arquivo for encontrado e lido com sucesso, seu conteúdo é retornado. Se nenhum dos arquivos na lista for encontrado ou se ocorrer um erro ao ler os arquivos, o método retorna a mensagem de fallback especificada.
    Args:
        preferred_names (Optional[list[str]], optional): Lista de nomes de arquivos de licença a serem verificados em ordem de preferência. O método tentará ler o conteúdo do arquivo de licença usando cada nome na lista até encontrar um arquivo existente e legível. Se nenhum dos arquivos na lista for encontrado ou se ocorrer um erro ao ler os arquivos, o método retornará a mensagem de fallback. Se a lista for None ou vazia, o método usará uma lista padrão de nomes de arquivos de licença para verificar.
        fallback_message (str, optional):  Defaults to ( "Licença não encontrada.\n\n" "Inclua um arquivo LICENSE.pt-BR.txt (ou LICENSE.txt / LICENSE) junto ao instalador." ).

    Returns:
        str: O conteúdo do arquivo de licença encontrado, ou a mensagem de fallback se nenhum arquivo for encontrado.
    """
    candidates = preferred_names or ["LICENSE.pt-br.txt", "LICENSE.txt", "LICENSE"]
    for name in candidates:
        p = abs_path(name)
        if p and os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
               
                pass
    return fallback_message


class LicenseDialog(QDialog):
    """
        Diálogo para exibir o texto da licença do aplicativo, com suporte para personalização de tema e leitura de arquivos de licença a partir de uma lista de nomes preferenciais. O diálogo é modal e inclui um QTextEdit para exibir o conteúdo da licença, bem como um QDialogButtonBox com um botão de fechar. O método apply_theme permite personalizar as cores do diálogo com base em um dicionário de tema fornecido.
    Args:
        QDialog (_type_): Diálogo para exibir o texto da licença do aplicativo, com suporte para personalização de tema e leitura de arquivos de licença a partir de uma lista de nomes preferenciais. O diálogo é modal e inclui um QTextEdit para exibir o conteúdo da licença, bem como um QDialogButtonBox com um botão de fechar. O método apply_theme permite personalizar as cores do diálogo com base em um dicionário de tema fornecido.
    """
    def __init__(self, parent=None, theme: Optional[dict] = None, license_text: str = ""):
        """
        Inicializa o diálogo de licença, configurando a interface do usuário para exibir o texto da licença e aplicar um tema personalizado, se fornecido. O diálogo é modal e possui um QTextEdit para exibir o conteúdo da licença, que é configurado como somente leitura. O layout do diálogo inclui o QTextEdit e um QDialogButtonBox com um botão de fechar. Se um dicionário de tema for fornecido, as cores do diálogo são personalizadas de acordo com as especificações do tema.
        Args:
            parent (_type_, optional): Widget pai do diálogo. Defaults to None.
            theme (Optional[dict], optional): Dicionário de tema para personalizar as cores do diálogo. O dicionário pode conter as chaves "background", "surface", "text" e "border" com valores de cor hexadecimal para personalizar a aparência do diálogo. Se None for fornecido, o diálogo usará as cores padrão definidas no método apply_theme. Defaults to None.
            license_text (str, optional): Texto da licença a ser exibido no diálogo. Defaults to "".
        """
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
        """
        Aplica um tema personalizado ao diálogo de licença, definindo as cores de fundo, superfície, texto e borda com base nas especificações do dicionário de tema fornecido. O método extrai as cores do dicionário de tema usando as chaves "background", "surface", "text" e "border", e então constrói uma string de estilo CSS para aplicar essas cores aos elementos do diálogo, como o QDialog, QTextEdit e QPushButton. O estilo é aplicado ao diálogo usando o método setStyleSheet.
        Args:
            theme (dict): Dicionário de tema para personalizar as cores do diálogo. O dicionário deve conter as chaves "background", "surface", "text" e "border" com valores de cor hexadecimal para personalizar a aparência do diálogo. O método usará essas cores para construir um estilo CSS que será aplicado ao diálogo, definindo as cores de fundo, superfície, texto e borda dos elementos do diálogo.
        """
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