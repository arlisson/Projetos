import os
from tkinter import messagebox
import urllib.request

from Utils.log import registrar_erro

def salvar_imagem_local(url_imagem: str, nome_arquivo: str, pasta: str = "imagens/imagens_cartas") -> str | None:
    """
    Baixa uma imagem da internet e salva localmente em uma pasta.

    :param url_imagem: URL da imagem a ser baixada
    :param nome_arquivo: Nome com o qual a imagem será salva (ex: "abc123.jpg")
    :param pasta: Pasta onde salvar a imagem (default: "imagens_cartas")
    :return: Caminho completo da imagem salva, ou None em caso de erro
    """
    try:
        os.makedirs(pasta, exist_ok=True)
        caminho_completo = os.path.join(pasta, nome_arquivo)

        if not os.path.exists(caminho_completo):
            urllib.request.urlretrieve(url_imagem, caminho_completo)

        return caminho_completo

    except Exception as e:
        messagebox.showerror("Erro", f"[ERRO] Falha ao baixar imagem: {url_imagem}\n{e}")
        registrar_erro("Erro ao baixar imagem em salvar_imagem_local", e)
        return None
