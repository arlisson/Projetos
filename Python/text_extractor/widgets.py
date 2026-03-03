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
        - Se o local contém '@', considera colado completo e retorna ok=True
        - Se local não vazio e domínio vazio => ok=False
        - Se local vazio => retorna "" e ok=True (campo em branco)
    Args:
        parent (Optional[QWidget], optional): O widget pai opcional. Defaults to None
    """

    def __init__(self, domains: List[str], parent: Optional[QWidget] = None):
        """ Inicializa o widget de entrada de e-mail com uma lista de domínios disponíveis para seleção. O widget é composto por um QLineEdit para a parte local do e-mail (antes do '@') e um QComboBox para a parte do domínio (após o '@'). O método configura o layout do widget, adiciona os componentes necessários e preenche o QComboBox com a lista de domínios fornecida. A função set_domains() é chamada para garantir que a lista de domínios seja exibida corretamente, permitindo que o usuário selecione um domínio específico para compor seu endereço de e-mail. O widget também inclui métodos para obter e definir o e-mail completo, bem como para atualizar dinamicamente a lista de domínios enquanto preserva a seleção atual do usuário.
        Args:
            domains (List[str]): A lista de domínios a ser exibida no QComboBox. O método recebe uma lista de strings que representam os domínios disponíveis para seleção. Esses domínios são usados para preencher o QComboBox, permitindo que o usuário escolha um domínio específico para compor seu endereço de e-mail. A lista de domínios pode ser atualizada dinamicamente usando o método set_domains(), que garante que a seleção atual seja preservada sempre que a lista for modificada.
            parent (Optional[QWidget], optional): O widget pai opcional. Defaults to None.
        """
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
        """Atualiza a lista de domínios disponíveis no QComboBox.

        Args:
            domains (List[str]): A lista de domínios a ser exibida no QComboBox. O método atualiza o conteúdo do QComboBox com os domínios fornecidos, preservando a seleção atual do usuário sempre que possível.
        """
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
        """Retorna a parte local do e-mail (antes do '@') inserida pelo usuário. O método obtém o texto do QLineEdit, que representa a parte local do e-mail, e remove quaisquer espaços em branco extras antes de retornar o valor. Se o campo estiver vazio, o método retorna uma string vazia. Este método é usado para acessar a parte local do e-mail que o usuário digitou ou colou no campo de entrada, permitindo que outras partes do aplicativo possam compor o endereço de e-mail completo combinando a parte local com o domínio selecionado.

        Returns:
            str: A parte local do e-mail inserida pelo usuário, sem espaços em branco extras. Se o campo estiver vazio, retorna uma string vazia.
        """
        return (self.inp_local.text() or "").strip()

    def domain(self) -> str:
        """ Retorna a parte do domínio do e-mail (após o '@') selecionada pelo usuário. O método obtém o texto atualmente selecionado no QComboBox, que representa a parte do domínio do e-mail, e remove quaisquer espaços em branco extras antes de retornar o valor. Se nenhum domínio estiver selecionado ou se o campo estiver vazio, o método retorna uma string vazia. Este método é usado para acessar a parte do domínio do e-mail que o usuário selecionou, permitindo que outras partes do aplicativo possam compor o endereço de e-mail completo combinando a parte local com o domínio selecionado.

        Returns:
            str: A parte do domínio do e-mail selecionada pelo usuário, sem espaços em branco extras. Se nenhum domínio estiver selecionado ou se o campo estiver vazio, retorna uma string vazia.
        """
        return (self.cmb_domain.currentText() or "").strip()

    def set_parts(self, local: str, domain: str) -> None:
        """ Define as partes local e de domínio do e-mail no widget. O método recebe a parte local e a parte do domínio como argumentos, limpa quaisquer espaços em branco extras e atualiza os campos correspondentes no QLineEdit e no QComboBox. A parte local é definida no QLineEdit, enquanto a parte do domínio é selecionada no QComboBox. Se a parte do domínio fornecida não estiver presente na lista de domínios do QComboBox, o método pode optar por adicionar o domínio à lista ou simplesmente deixar o campo de domínio vazio, dependendo da implementação desejada. Este método é útil para configurar o widget com um endereço de e-mail específico, dividindo-o em suas partes componentes para exibição e edição pelo usuário.

        Args:
            local (str): A parte local do e-mail a ser definida no QLineEdit. O método limpa quaisquer espaços em branco extras antes de definir o valor no campo de entrada.
            domain (str): A parte do domínio do e-mail a ser selecionada no QComboBox. O método limpa quaisquer espaços em branco extras antes de tentar selecionar o domínio na lista. Se o domínio não estiver presente na lista, o comportamento pode variar dependendo da implementação (por exemplo, adicionar o domínio à lista ou deixar o campo de domínio vazio).
        """
        self.inp_local.setText((local or "").strip())
        self.cmb_domain.setCurrentText((domain or "").strip())

    def set_email(self, email: str) -> None:
        """ Define o endereço de e-mail completo no widget, dividindo-o em partes local e de domínio. O método recebe um endereço de e-mail completo como argumento, limpa quaisquer espaços em branco extras e verifica se o endereço contém o caractere '@'. Se o endereço contiver '@', ele é dividido em parte local (antes do '@') e parte de domínio (após o '@'), e os campos correspondentes no QLineEdit e no QComboBox são atualizados usando o método set_parts(). Se o endereço não contiver '@', ele é tratado como a parte local do e-mail, e a parte do domínio é deixada vazia. Este método é útil para configurar o widget com um endereço de e-mail completo, permitindo que o usuário veja e edite as partes local e de domínio separadamente.

        Args:
            email (str): O endereço de e-mail completo a ser definido no widget. O método limpa quaisquer espaços em branco extras antes de processar o endereço. Se o endereço contiver '@', ele será dividido em parte local e parte de domínio; caso contrário, será tratado como parte local com domínio vazio.
        """
        s = (email or "").strip()
        if "@" in s:
            u, d = s.split("@", 1)
            self.set_parts(u, ("@" + d) if d else "")
        else:
            self.set_parts(s, "")

    def get_email(self) -> Tuple[str, bool]:
        """ Retorna o endereço de e-mail completo composto pela parte local e a parte do domínio, juntamente com um indicador de validade. O método obtém a parte local do QLineEdit e a parte do domínio do QComboBox, limpa quaisquer espaços em branco extras e verifica se a parte local contém o caractere '@'. Se a parte local contiver '@', o método considera que o usuário colou um endereço de e-mail completo na parte local, e retorna esse valor como o endereço de e-mail completo, juntamente com um indicador de validade True. Se a parte local não contiver '@', o método verifica se a parte local está vazia; se estiver vazia, retorna uma string vazia como o endereço de e-mail completo e um indicador de validade True (campo em branco é considerado válido). Se a parte local não estiver vazia e a parte do domínio estiver vazia, o método retorna a parte local como o endereço de e-mail completo e um indicador de validade False (indica que falta o domínio). Se ambas as partes estiverem presentes, o método combina a parte local com a parte do domínio para formar o endereço de e-mail completo e retorna esse valor juntamente com um indicador de validade True.

        Returns:
                 Tuple[str, bool]: Uma tupla contendo o endereço de e-mail completo composto pela parte local e a parte do domínio, e um indicador de validade. O primeiro elemento da tupla é o endereço de e-mail completo resultante da combinação da parte local e do domínio, ou uma string vazia se a parte local estiver vazia. O segundo elemento é um booleano que indica se o endereço de e-mail é considerado válido (True) ou inválido (False) com base nas regras descritas acima.
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
    """ Widget para exibir um campo com opções de editar, excluir e bloquear. O widget é composto por um QLabel para exibir o título do campo, um widget de entrada (input_widget) para mostrar o valor do campo, e três botões: "Editar", "Excluir" e um botão de bloqueio (cadeado). O botão de bloqueio é um QPushButton configurado como checkable, permitindo que o usuário bloqueie ou desbloqueie o campo. O widget emite sinais quando os botões são clicados: editRequested quando o botão "Editar" é clicado, deleteRequested quando o botão "Excluir" é clicado, e lockToggled quando o estado do botão de bloqueio é alterado. O layout do widget é organizado horizontalmente, com o botão de bloqueio posicionado antes do título, seguido pelo QLabel, o widget de entrada e os botões de ação. Este widget é útil para exibir campos de dados em uma interface de usuário, permitindo que os usuários interajam com os campos por meio das opções de edição, exclusão e bloqueio.

    Args:
        QWidget (_type_): O widget base do PySide6 que é estendido para criar o FieldRowWidget personalizado. Este widget serve como a classe base para o FieldRowWidget, permitindo que ele seja integrado em interfaces de usuário criadas com PySide6.
    """
    editRequested = Signal(str)
    deleteRequested = Signal(str)

    # NOVO: emite (field_id, locked)
    lockToggled = Signal(str, bool)

    def __init__(
        self,
        field_id: str,
        label_text: str,
        input_widget: QWidget,
        parent: Optional[QWidget] = None,
    ):
        """
        Inicializa o widget de linha de campo com um identificador, texto de rótulo, widget de entrada e um widget pai opcional. O método configura o layout do widget, adiciona os componentes necessários (botão de bloqueio, rótulo, widget de entrada e botões de ação) e conecta os sinais dos botões para emitir eventos apropriados quando as ações são realizadas pelo usuário. O botão de bloqueio é configurado para emitir um sinal com o estado atual (bloqueado ou desbloqueado) sempre que for alternado, permitindo que outras partes do aplicativo respondam a essa mudança de estado. O layout é organizado horizontalmente para garantir uma apresentação clara e acessível dos elementos do campo.
        Args:
            field_id (str): O identificador único para o campo representado por este widget. Este valor é usado para identificar o campo específico quando os sinais de edição, exclusão ou bloqueio são emitidos, permitindo que outras partes do aplicativo saibam qual campo está sendo interagido.
            label_text (str): O texto a ser exibido no QLabel como rótulo do campo. Este texto serve para identificar visualmente o campo para o usuário, indicando o tipo de informação que o campo representa.
            input_widget (QWidget): O widget de entrada que será exibido ao lado do rótulo. Este widget é usado para mostrar o valor do campo e pode ser qualquer tipo de widget de entrada (por exemplo, QLineEdit, QComboBox, etc.) dependendo do tipo de dados que o campo representa.
            parent (Optional[QWidget], optional): O widget pai opcional. Este valor é passado para o construtor da classe base QWidget, permitindo que o FieldRowWidget seja integrado em uma hierarquia de widgets dentro da interface de usuário do aplicativo. Se nenhum widget pai for fornecido, o FieldRowWidget será um widget independente.
        """
        super().__init__(parent)
        self.field_id = field_id

        # NOVO: botão só com ícone (sem texto)
        self.btn_lock = QPushButton()
        self.btn_lock.setCheckable(True)
        self.btn_lock.setFixedSize(28, 28)
        self.btn_lock.setToolTip("Bloquear/desbloquear este campo")

        self.btn_lock.toggled.connect(lambda checked: self.lockToggled.emit(self.field_id, bool(checked)))

        self.lbl = QLabel(label_text)
        self.lbl.setMinimumWidth(160)

        self.btn_edit = QPushButton("Editar")
        self.btn_del = QPushButton("Excluir")
        self.btn_del.setProperty("variant", "danger")

        self.btn_edit.clicked.connect(lambda: self.editRequested.emit(self.field_id))
        self.btn_del.clicked.connect(lambda: self.deleteRequested.emit(self.field_id))

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)

        # NOVO: cadeado antes do título
        row.addWidget(self.btn_lock)
        row.addWidget(self.lbl)

        row.addWidget(input_widget, 1)
        row.addWidget(self.btn_edit)
        row.addWidget(self.btn_del)

        self.setLayout(row)

    
    def set_locked(self, locked: bool) -> None:
        """ Atualiza o estado do botão de bloqueio sem disparar o evento lockToggled. Este método é usado para definir o estado do botão de bloqueio (bloqueado ou desbloqueado) programaticamente, sem emitir o sinal lockToggled que normalmente seria acionado quando o usuário interage com o botão. Isso é útil para evitar loops de eventos ou para atualizar o estado do botão com base em mudanças externas sem causar efeitos colaterais indesejados. O método bloqueia temporariamente os sinais do botão de bloqueio, define o estado do botão de acordo com o valor fornecido e, em seguida, desbloqueia os sinais para permitir que futuras interações do usuário sejam processadas normalmente.

        Args:
            locked (bool): O estado a ser definido para o botão de bloqueio. Se True, o botão será marcado como bloqueado; se False, será marcado como desbloqueado. O método garante que o estado do botão seja atualizado de acordo com o valor fornecido, sem disparar o evento lockToggled.
        """
        self.btn_lock.blockSignals(True)
        self.btn_lock.setChecked(bool(locked))
        self.btn_lock.blockSignals(False)

class BoolInputWidget(QWidget):
    """ 
    Widget de entrada booleana baseado em QComboBox.

    Exibe uma lista suspensa com as opções “Sim” e “Não” e fornece métodos
    para ler e atribuir o valor selecionado, aceitando variações comuns de
    entrada (ex.: "yes", "true", "1", "nao", "false", "0").

    Uso típico:
        w = BoolInputWidget()
        w.set_value("true")   # seleciona "Sim"
        w.value()             # retorna "Sim" ou "Não"         
    Args:
        parent (Optional[QWidget]): Widget pai do Qt (opcional).
    """
    def __init__(self, parent: Optional[QWidget] = None):
        """
        Inicializa o widget com um QComboBox contendo as opções “Sim” e “Não” e
        define um layout horizontal sem margens.

        Args:
            parent (Optional[QWidget], optional): Widget pai do Qt. Defaults to None.
        """
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
        """
        Retorna o texto atualmente selecionado no combo (“Sim” ou “Não”),
        removendo espaços em branco. Se não houver seleção válida, retorna
        string vazia.

        Returns:
            str: Valor selecionado (“Sim”/“Não”) ou "".
        """
        return (self.cmb.currentText() or "").strip()

    def set_value(self, v: str) -> None:
        """
        Define a seleção do combo com base na string fornecida, aceitando variações
        comuns de verdadeiro/falso.

        Normalização aplicada:
        - {"sim","s","yes","y","true","1"} -> "Sim"
        - {"não","nao","n","no","false","0"} -> "Não"
        - Se `v` for vazio (ou apenas espaços), define "".
        - Se `v` não corresponder e não for "Sim"/"Não", define "".

        Observação:
        - Para o estado vazio funcionar, é necessário adicionar um item vazio no
            QComboBox (linha comentada `self.cmb.addItem("")`).

        Args:
            v (str): Valor de entrada a ser normalizado e aplicado ao combo.
        """
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