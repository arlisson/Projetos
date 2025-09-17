import tkinter as tk
from tkinter import ttk, messagebox
from Components.entrada_padrao import criar_entrada_padrao, criar_entrada_data_com_calendario
from Decorators.log_execao import log_excecoes
from Utils.limpar_preco import limpar_preco
from Utils.log import registrar_erro
from scraping.scraping_cartas import buscar_cartas_colecao
from DAO.database import buscar_raridade_qualidade_nome, inserir_carta, inserir_colecao, buscar_colecao_por_nome
from PIL import Image, ImageTk
from Utils.baixar_carta import mostrar_erros_acumulados, salvar_imagem_local
import threading
from Components.modal_progresso import ModalProgresso
import re

IMAGEM_PADRAO = "imagens/imagem_padrao.jpg"

def criar_tela_cadastro_colecao(app):

    contador_cartas_var = tk.StringVar(value="")


    largura = 700
    altura = 500

    root = tk.Toplevel(app)
    root.title("Cadastro de Coleção por Scraping")
    root.resizable(False, False)
    root.geometry(f"{largura}x{altura}+{(root.winfo_screenwidth() - largura) // 2}+{(root.winfo_screenheight() - altura) // 2}")
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
    campos["data"] = criar_entrada_data_com_calendario(frame=frame, root=root, linha=3, texto_label="Data da Compra:", icone=root.CALENDAR_ICON)

    campos["quantidade_unitaria"].insert(0, "1")

    lista_cartas = []

    def salvar_cartas_selecionadas():
        selecionadas = [c for c in lista_cartas if c["var"].get() == 1]

        if not selecionadas:
            messagebox.showwarning("Aviso", "Nenhuma carta selecionada.", parent=root)
            return

        for carta in selecionadas:
            dados = carta["dados"]
            inserir_carta(dados)

        messagebox.showinfo("Sucesso", f"{len(selecionadas)} cartas inseridas com sucesso!", parent=root)
        root.destroy()

    @log_excecoes
    def exibir_selecao(cartas, preco_unitario, quantidade, data):
        for widget in frame.winfo_children():
            widget.destroy()

        ttk.Label(frame, text="Buscar:").grid(row=0, column=0, sticky="w")
        filtro_entry = ttk.Entry(frame)
        filtro_entry.grid(row=0, column=1, sticky="ew", padx=5)
        frame.columnconfigure(1, weight=1)



        lista_frame = ttk.Frame(frame)
        lista_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        lista_frame.columnconfigure(0, weight=1)

        canvas = tk.Canvas(lista_frame)
        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        selecionar_todos_var = tk.IntVar()

        def filtrar():
            texto = filtro_entry.get().lower()
            for carta in lista_cartas:
                nome_codigo = f"{carta['dados']['nome']} {carta['dados']['codigo']}".lower()
                visible = texto in nome_codigo
                carta["frame"].pack_forget() if not visible else carta["frame"].pack(fill="x", padx=5, pady=2)

        filtro_entry.bind("<KeyRelease>", lambda e: filtrar())

        def toggle_selecionar_todos():
            for carta in lista_cartas:
                carta["var"].set(selecionar_todos_var.get())

        chk_todos = ttk.Checkbutton(frame, text="Selecionar Todas", variable=selecionar_todos_var, command=toggle_selecionar_todos)
        chk_todos.grid(row=2, column=0, columnspan=2, pady=5)

      
        for carta in cartas:            
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

            nome_arquivo = f"{codigo}.jpg" if codigo else re.sub(r'\W+', '_', nome.lower()) + ".jpg"
            caminho_imagem_local = salvar_imagem_local(imagem_url, nome_arquivo)

            dados_carta = {
                "link_site": carta.get("link_site"),
                "nome": nome,
                "colecao": id_colecao,
                "codigo": codigo,
                "preco_da_compra": preco_unitario,
                "data_da_compra": data,
                "raridade": id_raridade,
                "qualidade": id_qualidade,
                "quantidade": quantidade,
                "imagem": imagem_url,
                "imagem_salva": caminho_imagem_local.replace("\\", "/") if caminho_imagem_local else IMAGEM_PADRAO,
                "origem": "MyPCards",
                "preco_atual": preco_atual
            }

            var = tk.IntVar(value=1)
            frame_carta = ttk.Frame(scroll_frame)
            chk = ttk.Checkbutton(frame_carta, variable=var)
            chk.pack(side="left")
            ttk.Label(frame_carta, text=f"{nome} ({codigo})").pack(side="left", padx=5)
            frame_carta.pack(fill="x", padx=5, pady=2)

            lista_cartas.append({"var": var, "dados": dados_carta, "frame": frame_carta})
            
        
        mostrar_erros_acumulados()

        ttk.Label(frame, text=f"Total de cartas encontradas: {len(cartas)}").grid(row=3, column=0, sticky="w", pady=5)

        ttk.Button(frame, text="Salvar Selecionadas", command=lambda:iniciar_processamento(t="Aguarde", m="Salvando cartas selecionadas...", f=lambda modal: salvar_cartas_selecionadas())).grid(row=3, column=0, columnspan=2, pady=10)

    def buscar_cartas_thread(modal: ModalProgresso):
        try:
            link = campos["link"].get().strip()
            preco_unitario = limpar_preco(campos["preco_unitario"].get())
            quantidade = int(campos["quantidade_unitaria"].get())
            data = campos["data"].get().strip()

            if not link or preco_unitario <= 0 or quantidade <= 0 or not data:
                root.after(0, modal.fechar_async)  # ✅ agenda no mainloop
                messagebox.showerror("Erro", "Preencha todos os campos corretamente.", parent=root)
                return

            cartas = buscar_cartas_colecao(link)

            if not cartas:
                root.after(0, modal.fechar_async)  # ✅
                messagebox.showwarning("Atenção", "Nenhuma carta encontrada via scraping.", parent=root)
                return

            root.after(0, modal.fechar_async)  # ✅
            exibir_selecao(cartas, preco_unitario, quantidade, data)

        except Exception as e:
            root.after(0, modal.fechar_async)  # ✅
            messagebox.showerror("Erro", f"Erro ao buscar cartas: {e}", parent=root)
            registrar_erro("Erro na thread de busca de cartas", e)


    def iniciar_processamento(t="Aguarde", m="Buscando cartas via scraping...",f=buscar_cartas_thread):
        modal = ModalProgresso(root, titulo=t, mensagem=m)
        thread = threading.Thread(target=f, args=(modal,), daemon=True)
        thread.start()

    botoes = ttk.Frame(root)
    botoes.pack(pady=10)
    ttk.Button(botoes, text="Buscar Cartas", command=iniciar_processamento).grid(row=0, column=0, padx=20)
