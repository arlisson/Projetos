import os
from tkinter import messagebox
import urllib.request
import tkinter as tk
from tkinter import ttk

from Utils.log import registrar_erro

# Lista global para acumular erros
_erros_acumulados = []

def salvar_imagem_local(url_imagem: str, nome_arquivo: str, pasta: str = "imagens/imagens_cartas") -> str | None:
    """
    Baixa uma imagem da internet e salva localmente em uma pasta.

    :param url_imagem: URL da imagem a ser baixada
    :param nome_arquivo: Nome com o qual a imagem será salva (ex: "abc123.jpg")
    :param pasta: Pasta onde salvar a imagem (default: "imagens_cartas")
    :return: Caminho completo da imagem salva, ou None em caso de erro
    """
    global _erros_acumulados

    try:
        os.makedirs(pasta, exist_ok=True)
        caminho_completo = os.path.join(pasta, nome_arquivo)

        if not os.path.exists(caminho_completo):
            urllib.request.urlretrieve(url_imagem, caminho_completo)

        return caminho_completo or "imagens/imagem_padrao.jpg"

    except Exception as e:
        erro_msg = f"[ERRO] Falha ao baixar imagem: {url_imagem}\n{e}"
        _erros_acumulados.append(erro_msg)
        registrar_erro("Erro ao baixar imagem em salvar_imagem_local", e)
        return None


def mostrar_erros_acumulados(parent=None):
    """
    Exibe todos os erros acumulados em uma janela com scroll.
    """
    global _erros_acumulados
    if not _erros_acumulados:
        return

    # Criar janela separada
    popup = tk.Toplevel(parent)
    popup.title("Erros acumulados")
    popup.geometry("600x400")  # tamanho inicial
    popup.resizable(True, True)

    # Frame para organizar
    frame = ttk.Frame(popup)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Scrollbar + Text
    scrollbar = ttk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    text = tk.Text(frame, wrap="word", yscrollcommand=scrollbar.set)
    text.pack(fill="both", expand=True)

    scrollbar.config(command=text.yview)

    # Inserir erros
    mensagem = "\n\n".join(_erros_acumulados)
    text.insert("1.0", mensagem)
    text.config(state="disabled")  # deixa somente leitura

    # Botão de fechar
    ttk.Button(popup, text="Fechar", command=popup.destroy).pack(pady=5)

    # Limpa lista depois de mostrar
    _erros_acumulados.clear()
