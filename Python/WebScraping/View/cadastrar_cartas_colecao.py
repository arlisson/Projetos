import tkinter as tk
from tkinter import ttk, messagebox
from Components.entrada_padrao import criar_entrada_padrao, criar_entrada_data_com_calendario
from Utils.limpar_preco import limpar_preco
from Utils.log import registrar_erro
from scraping.scraping_cartas import buscar_cartas_colecao
from DAO.database import buscar_raridade_qualidade_nome, inserir_carta, inserir_colecao, buscar_colecao_por_nome
from PIL import Image, ImageTk
from Utils.baixar_carta import salvar_imagem_local
import threading
from Components.modal_progresso import ModalProgresso

IMAGEM_PADRAO = "imagens/imagens_cartas/imagem_padrao.jpg"


def criar_tela_cadastro_colecao(app):
    largura = 700
    altura = 450

    root = tk.Toplevel(app)
    root.title("Cadastro de Coleção por Scraping")
    root.resizable(False, False)

    # 🔲 Centraliza a janela
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (largura // 2)
    y = (root.winfo_screenheight() // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{x}+{y}")

    root.grab_set()
    root.focus_force()


    try:
        calendar_img = Image.open("imagens/calendario.png").resize((20, 20))
        root.CALENDAR_ICON = ImageTk.PhotoImage(calendar_img)
    except Exception as e:
        root.CALENDAR_ICON = None
        registrar_erro(f"Erro ao carregar ícone do calendário: {e}")

    campos = {}

    frame = ttk.LabelFrame(root, text="Informações da Coleção", padding=20)
    frame.pack(fill="both", expand=True, padx=10, pady=10)    

    campos["link"] = criar_entrada_padrao(frame=frame, texto="Link da 1ª página:", linha=0)
    campos["preco_unitario"] = criar_entrada_padrao(frame=frame, texto="Preço unitário por carta:", linha=1)
    campos["quantidade_unitaria"] = criar_entrada_padrao(frame=frame, texto="Quantidade por carta:", linha=2)

    campos["data"] = criar_entrada_data_com_calendario(
            frame=frame,
            root=root,
            linha=3,
            texto_label="Data da Compra:",
            icone=root.CALENDAR_ICON  # ou None para usar 📅
    )

    campos["quantidade_unitaria"].insert(0, "1")

    def salvar_colecao_thread(modal):
        try:
            link = campos["link"].get().strip()
            preco_unitario = limpar_preco(campos["preco_unitario"].get())
            quantidade = int(campos["quantidade_unitaria"].get())
            data = campos["data"].get().strip()

            if not link or preco_unitario <= 0 or quantidade <= 0 or not data:
                modal.fechar()
                messagebox.showerror("Erro", "Preencha todos os campos corretamente.", parent=root)
                return

            cartas = buscar_cartas_colecao(link)

            if not cartas:
                modal.fechar()
                messagebox.showwarning("Atenção", "Nenhuma carta foi encontrada via scraping.", parent=root)
                return

            modal.atualizar_mensagem("Salvando cartas no banco...")

            total_inseridas = 0
            for carta in cartas:
                link_carta = carta.get("link_site")
                nome = carta.get("nome")
                codigo = carta.get("codigo", "")
                preco_atual = limpar_preco(carta.get("preco_atual", 0.0))
                imagem_url = carta.get("imagem") or IMAGEM_PADRAO
                raridade = carta.get("raridade") or "Common"
                qualidade = carta.get("qualidade") or "Nova"
                colecao_nome = carta.get("colecao") or "Desconhecida"

                id_colecao = buscar_colecao_por_nome(colecao_nome)
                if not id_colecao:
                    id_colecao = inserir_colecao(colecao_nome)

                id_raridade = buscar_raridade_qualidade_nome(raridade, "raridade") or 1
                id_qualidade = buscar_raridade_qualidade_nome(qualidade, "qualidade") or 1

                # 🔽 NOVO: Salva a imagem no disco
                nome_arquivo = f"{codigo}.jpg" if codigo else re.sub(r'\W+', '_', nome.lower()) + ".jpg"
                caminho_imagem_local = salvar_imagem_local(imagem_url, nome_arquivo)

                dados_carta = {
                    "link_site": link_carta,
                    "nome": nome,
                    "colecao": id_colecao,
                    "codigo": codigo,
                    "preco_da_compra": preco_unitario,
                    "data_da_compra": data,
                    "raridade": id_raridade,
                    "qualidade": id_qualidade,
                    "quantidade": quantidade,
                    "imagem": imagem_url,
                    "imagem_salva": caminho_imagem_local.replace("\\", "/") or "",  # ✅ novo campo
                    "origem": "MyPCards",
                    "preco_atual": preco_atual
                }

                inserir_carta(dados_carta)
                total_inseridas += 1

            modal.fechar()
            messagebox.showinfo("Sucesso", f"{total_inseridas} cartas inseridas com sucesso!", parent=root)
            root.destroy()

        except Exception as e:
            modal.fechar()
            messagebox.showerror("Erro", f"Erro ao salvar coleção: {e}", parent=root)

    def iniciar_processamento():
        modal = ModalProgresso(root, titulo="Aguarde", mensagem="Buscando cartas via scraping...")
        thread = threading.Thread(target=salvar_colecao_thread, args=(modal,), daemon=True)
        thread.start()

    botoes = ttk.Frame(root)
    botoes.pack(pady=10)
    ttk.Button(botoes, text="Buscar e Salvar Cartas", command=iniciar_processamento).grid(row=0, column=0, padx=20)
