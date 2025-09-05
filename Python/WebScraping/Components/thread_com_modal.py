# Components/thread_com_modal.py

import threading
from Components.modal_progresso import ModalProgresso

def executar_em_thread(root, funcao_alvo, args=(), titulo="Aguarde", mensagem="Processando..."):
    """
    Executa uma função em uma nova thread com um modal de carregamento.
    
    Parâmetros:
        - root: janela/tela principal.
        - funcao_alvo: função a ser executada em thread.
        - args: tupla de argumentos para a função.
        - titulo: título do modal.
        - mensagem: mensagem do modal.
    """
    modal = ModalProgresso(root, titulo=titulo, mensagem=mensagem)

    def wrapper():
        try:
            funcao_alvo(*args)
        finally:
            modal.fechar()

    threading.Thread(target=wrapper, daemon=True).start()
