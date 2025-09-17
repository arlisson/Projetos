import functools
import traceback
import tkinter as tk
from tkinter import ttk

from Utils.log import log_info, registrar_erro

# lista global para acumular erros
_erros_acumulados = []


def log_excecoes(func):
    """
    Decorador que registra erros automaticamente, acumula numa lista
    e mostra em uma janela com scroll quando solicitado.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            log_info(f"Executando função: {func.__qualname__}")
            return func(*args, **kwargs)
        except Exception as e:
            # mensagem resumida
            msg_curta = f"Erro na função {func.__qualname__}: {str(e)}"
            _erros_acumulados.append(msg_curta)

            # log detalhado
            registrar_erro(msg_curta, e)
            registrar_erro(traceback.format_exc())

            raise  # relança para não engolir a exceção
    return wrapper


def mostrar_erros_acumulados(parent=None):
    """
    Exibe todos os erros acumulados em uma janela com scroll.
    """
    global _erros_acumulados
    if not _erros_acumulados:
        return

    popup = tk.Toplevel(parent)
    popup.title("Erros acumulados")
    
    # Centralizar
    largura, altura = 1000, 700
    x = (popup.winfo_screenwidth() // 2) - (largura // 2)
    y = (popup.winfo_screenheight() // 2) - (altura // 2)
    popup.geometry(f"{largura}x{altura}+{x}+{y}")
    popup.resizable(True, True)

    


    frame = ttk.Frame(popup)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar = ttk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    text = tk.Text(frame, wrap="word", yscrollcommand=scrollbar.set)
    text.pack(fill="both", expand=True)

    scrollbar.config(command=text.yview)

    # insere os erros acumulados
    mensagem = "\n\n".join(_erros_acumulados)
    text.insert("1.0", mensagem)
    text.config(state="disabled")

    ttk.Button(popup, text="Fechar", command=popup.destroy).pack(pady=5)

    # limpa lista após mostrar
    _erros_acumulados.clear()
