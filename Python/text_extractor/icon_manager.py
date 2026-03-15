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
        """Carrega um QPixmap a partir de um caminho de arquivo, utilizando um cache para evitar recarregamentos desnecessários. O método primeiro resolve o caminho absoluto usando a função fornecida, verifica se o arquivo existe e, se estiver no cache, retorna o QPixmap armazenado. Se o arquivo não estiver no cache, ele tenta carregar o QPixmap do caminho resolvido e, se for bem-sucedido, armazena-o no cache antes de retorná-lo. Se o arquivo não existir ou se o QPixmap for inválido, o método retorna None.
        Args:
            path (str): O caminho do arquivo de imagem a ser carregado como QPixmap. O método irá resolver esse caminho usando a função abs_path fornecida, verificar se o arquivo existe usando file_exists, e então carregar o QPixmap correspondente, utilizando um cache para otimizar o desempenho em chamadas subsequentes com o mesmo caminho.

        Returns:
            Optional[QPixmap]: O QPixmap carregado a partir do caminho especificado, ou None se o arquivo não existir ou se o QPixmap for inválido.
        """
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
        """
        Aplica uma tintura a um QPixmap usando o modo de composição SourceIn. O método cria um novo QPixmap transparente do mesmo tamanho que o original, desenha o pixmap original nele, e então preenche o pixmap resultante com a cor de tintura especificada usando o modo de composição SourceIn, que mantém apenas as partes do pixmap original onde a tintura é aplicada. O resultado é um novo QPixmap com a tintura aplicada, que é retornado pelo método.
        Args:
            pixmap (QPixmap): O QPixmap a ser tinto.
            tint_hex (str): A cor hexadecimal da tintura a ser aplicada.

        Returns:
            QPixmap: O QPixmap com a tintura aplicada.
        """
        tinted = QPixmap(pixmap.size())
        tinted.fill(Qt.transparent)

        painter = QPainter(tinted)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(tinted.rect(), QColor(tint_hex))
        painter.end()

        return tinted

    def icon_for_key(self, key: str, tint_hex: str) -> Optional[QIcon]:
        """Retorna um QIcon para uma chave de ícone específica, aplicando uma tintura se necessário. O método busca o caminho do ícone correspondente à chave fornecida no dicionário de configuração ui_cfg["button_icons"], verifica se o arquivo existe e, se for encontrado, carrega o QPixmap usando o método _load_pixmap. Se o QPixmap for carregado com sucesso, ele aplica a tintura usando o método _tint_pixmap e retorna um QIcon criado a partir do pixmap tinturado. Se a chave não for encontrada, se o arquivo não existir ou se o QPixmap for inválido, o método retorna None.
        Args:
            key (str): A chave do ícone a ser buscada no dicionário de configuração ui_cfg["button_icons"] para obter o caminho do arquivo de ícone correspondente.
            tint_hex (str): A cor hexadecimal da tintura a ser aplicada ao ícone, caso o arquivo de ícone seja encontrado e carregado com sucesso.

        Returns:
            Optional[QIcon]: Um QIcon criado a partir do QPixmap tinturado correspondente à chave fornecida, ou None se a chave não for encontrada, se o arquivo de ícone não existir ou se o QPixmap for inválido.
        """
        icons = self.ui_cfg.get("button_icons", {}) or {}
        p = icons.get(key, "")
        if not p or not self.file_exists(p):
            return None
        pm = self._load_pixmap(p)
        if not pm:
            return None
        return QIcon(self._tint_pixmap(pm, tint_hex))

    def apply_button_icon(self, btn: QPushButton, key: str, tint_hex: str) -> None:
        """
        Aplica um ícone a um QPushButton com base em uma chave de ícone específica, utilizando o método icon_for_key para obter o QIcon correspondente. O método busca o QIcon usando a chave fornecida e, se um ícone válido for retornado, ele é aplicado ao botão usando o método setIcon do QPushButton. Se o ícone não for encontrado ou for inválido, o método não faz nenhuma alteração no botão.
        Args:
            btn (QPushButton): O botão ao qual o ícone será aplicado.
            key (str): A chave do ícone a ser buscada no dicionário de configuração ui_cfg["button_icons"] para obter o caminho do arquivo de ícone correspondente.
            tint_hex (str): A cor hexadecimal da tintura a ser aplicada ao ícone, caso o arquivo de ícone seja encontrado e carregado com sucesso.
        """
        ic = self.icon_for_key(key, tint_hex)
        if ic:
            btn.setIcon(ic)

    def clear_cache(self) -> None:
        """
        Limpa o cache de QPixmap armazenados no IconManager. O método remove todas as entradas do dicionário _pixmap_cache, liberando a memória ocupada pelos QPixmaps armazenados. Isso pode ser útil para liberar recursos quando os ícones não são mais necessários ou quando se deseja forçar o recarregamento dos ícones a partir dos arquivos.
        """
        self._pixmap_cache.clear()