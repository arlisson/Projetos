# loading_screen.py
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QSplashScreen


class LoadingScreen:
    """ Classe para exibir uma tela de carregamento personalizada durante a inicialização do aplicativo, com suporte para mensagens dinâmicas e personalização de cores. O método construtor recebe parâmetros para configurar o título, subtítulo, dimensões e cores da tela de carregamento, e cria um QPixmap personalizado usando o método _make_pixmap. A classe inclui métodos para mostrar a tela de carregamento, atualizar a mensagem exibida, ocultar a tela e finalizar o splash de forma confiável em relação à janela principal do aplicativo.
    
    """
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
        """ Inicializa a tela de carregamento personalizada, configurando o título, subtítulo, dimensões e cores da tela. O método construtor recebe um objeto QApplication para associar a tela de carregamento ao aplicativo, bem como parâmetros opcionais para personalizar o título, subtítulo, largura, altura e cores de fundo, destaque, texto e texto secundário da tela. Ele cria um QPixmap personalizado usando o método _make_pixmap, que desenha a interface da tela de carregamento com base nas configurações fornecidas. A tela de carregamento é configurada para permanecer no topo das janelas usando a flag Qt.WindowStaysOnTopHint.
        Args:
            app (QApplication): O objeto QApplication ao qual a tela de carregamento estará associada. 
            title (str, optional): O título exibido na tela de carregamento. Defaults to "Iniciando".
            subtitle (str, optional): O subtítulo exibido na tela de carregamento. Defaults to "Aguarde enquanto validamos o acesso...".
            width (int, optional): A largura da tela de carregamento em pixels. Defaults to 520.
            height (int, optional): A altura da tela de carregamento em pixels. Defaults to 220.
            bg (str, optional): A cor de fundo da tela de carregamento em formato hexadecimal. Defaults to "#0B1220".
            accent (str, optional): A cor de destaque da tela de carregamento em formato hexadecimal. Defaults to "#3B82F6".
            text (str, optional): A cor do texto principal da tela de carregamento em formato hexadecimal. Defaults to "#E6EDF7".
            muted (str, optional): A cor do texto secundário da tela de carregamento em formato hexadecimal. Defaults to "#A7B3C6".
        """
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
        """
        Cria um QPixmap personalizado para a tela de carregamento, desenhando o título, subtítulo e elementos visuais com base nas propriedades da classe. O método cria um QPixmap com as dimensões especificadas, preenche o fundo com a cor de fundo configurada, e então utiliza um QPainter para desenhar uma barra de destaque, o título e o subtítulo na tela de carregamento. As cores do texto e do destaque são aplicadas conforme configurado nas propriedades da classe. O resultado é um QPixmap que representa a interface visual da tela de carregamento, que é retornado pelo método.
        Returns:
            QPixmap: O QPixmap personalizado criado para a tela de carregamento, contendo o título, subtítulo e elementos visuais configurados com base nas propriedades da classe. O método desenha a interface da tela de carregamento usando um QPainter, aplicando as cores de fundo, destaque, texto e texto secundário conforme especificado, e retorna o QPixmap resultante.
        """
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
        """
        Exibe a tela de carregamento e atualiza a mensagem exibida. O método mostra o splash usando o método show do QSplashScreen, e então chama o método update para definir a mensagem exibida na tela de carregamento. A mensagem é alinhada à parte inferior esquerda da tela usando as flags Qt.AlignBottom | Qt.AlignLeft, e a cor do texto é definida como a cor de texto secundário configurada na classe. O método processa os eventos do aplicativo para garantir que a interface seja atualizada corretamente.
        Args:
            message (str, optional): A mensagem a ser exibida na tela de carregamento. Defaults to "Preparando...".
        """
        self._splash.show()
        self.update(message)

    def update(self, message: str) -> None:
        """
        Atualiza a mensagem exibida na tela de carregamento. O método utiliza o método showMessage do QSplashScreen para definir a nova mensagem, alinhando-a à parte inferior esquerda da tela e usando a cor de texto secundário configurada na classe. Após atualizar a mensagem, o método processa os eventos do aplicativo para garantir que a interface seja atualizada e a nova mensagem seja exibida corretamente.
        Args:
            message (str): A nova mensagem a ser exibida na tela de carregamento.
        """
        self._splash.showMessage(message, Qt.AlignBottom | Qt.AlignLeft, self._muted)
        self._app.processEvents()

    def hide(self) -> None:
        """
        Oculta a tela de carregamento. O método chama o método hide do QSplashScreen para ocultar a tela de carregamento, e então processa os eventos do aplicativo para garantir que a interface seja atualizada corretamente após ocultar o splash.
        """
        self._splash.hide()
        self._app.processEvents()

    def close(self) -> None:
        """
        Fecha a tela de carregamento de forma confiável. O método chama o método close do QSplashScreen para fechar a tela de carregamento, e processa os eventos do aplicativo antes e depois de fechar o splash para garantir que a interface seja atualizada corretamente e que o fechamento ocorra de forma suave.
        """
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