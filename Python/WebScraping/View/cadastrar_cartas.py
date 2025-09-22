import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import urllib.request
from io import BytesIO
from Utils.limpar_preco import limpar_preco
from scraping.scraping_cartas import *
from DAO.database import *
from Utils.combo_utils import popular_dropdown
from Utils.baixar_carta import salvar_imagem_local
from Components.entrada_padrao import criar_entrada_com_botao_imagem, criar_entrada_padrao, criar_entrada_data_com_calendario
from Components.thread_com_modal import executar_em_thread

IMAGEM_PADRAO = "imagens/imagem_padrao.jpg"

def criar_tela_cadastro(app):
    root = tk.Toplevel(app)
    root.grab_set()
    root.focus_force()
    root.title("Cadastro de Carta")
    root.resizable(True, True)

    largura, altura = 960, 640
    x = (root.winfo_screenwidth() // 2) - (largura // 2)
    y = (root.winfo_screenheight() // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{x}+{y}")

    main_frame = ttk.Frame(root, padding=10)
    main_frame.pack(fill="both", expand=True)
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=0)
    main_frame.rowconfigure(0, weight=1)

    try:
        calendar_img = Image.open("imagens/calendario.png").resize((20, 20))
        file_img = Image.open("imagens/pasta-aberta.png").resize((20, 20))
        FILE_ICON = ImageTk.PhotoImage(file_img)
        CALENDAR_ICON = ImageTk.PhotoImage(calendar_img)
    except Exception as e:
        CALENDAR_ICON = None
        FILE_ICON = None
        registrar_erro(f"Erro ao carregar ícone do calendário: {e}")

    campos = {}

    form_frame = ttk.LabelFrame(main_frame, text="Dados da Carta", padding=10)
    form_frame.grid(row=0, column=0, sticky="nsew")
    form_frame.columnconfigure(1, weight=1)

    campos["link"] = criar_entrada_padrao(form_frame, "Link da carta:", 0)
    campos["nome"] = criar_entrada_padrao(form_frame, "Nome:", 1)
    campos["codigo"] = criar_entrada_padrao(form_frame, "Código:", 2)
    campos["preco_da_compra"] = criar_entrada_padrao(form_frame, "Preço pago:", 3)
    campos["preco_atual"] = criar_entrada_padrao(form_frame, "Preço atual:", 4)
    
    campos["data"] = criar_entrada_data_com_calendario(
        frame=form_frame,
        root=root,
        linha=5,
        texto_label="Data da Compra:",
        icone=CALENDAR_ICON  # ou None para usar 📅
   )

    campos["quantidade"] = criar_entrada_padrao(form_frame, "Quantidade:", 6)    
    campos["imagem"] = criar_entrada_padrao(form_frame, "Imagem URL:", 7)

    def atualizar_imagem(caminho):
        try:
            if caminho.startswith("http://") or caminho.startswith("https://"):
                with urllib.request.urlopen(caminho) as u:
                    raw_data = u.read()
                im = Image.open(BytesIO(raw_data))
            else:
                im = Image.open(caminho)

            im.thumbnail((300, 420))
            photo = ImageTk.PhotoImage(im)
            imagem_label.configure(image=photo)
            imagem_label.image = photo
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar imagem: {e}", parent=root)
            registrar_erro(f"[Erro] Falha ao carregar imagem: {e}")
            imagem_label.configure(image='')
            imagem_label.image = None


    # Criar campo
    campos["imagem_salva"] = criar_entrada_com_botao_imagem(
        frame=form_frame,
        texto="Imagem:",
        linha=8,
        ao_selecionar=atualizar_imagem,
        path="imagens/imagens_cartas",
        icone=FILE_ICON  # ou None para usar "📁"
    )


    # Atualiza os campos seguintes para as próximas linhas
    campos["origem"] = criar_entrada_padrao(form_frame, "Origem:", 9)    


    ttk.Label(form_frame, text="Raridade:").grid(row=10, column=0, sticky="w", padx=5, pady=3)
    campos["raridade"] = ttk.Combobox(form_frame, state="readonly")
    campos["raridade"].grid(row=10, column=1, columnspan=2, padx=5, pady=3, sticky="we")
    popular_dropdown(campos["raridade"], buscar_valores_tabela("raridade"))

    ttk.Label(form_frame, text="Qualidade:").grid(row=11, column=0, sticky="w", padx=5, pady=3)
    campos["qualidade"] = ttk.Combobox(form_frame, state="readonly")
    campos["qualidade"].grid(row=11, column=1, columnspan=2, padx=5, pady=3, sticky="we")
    popular_dropdown(campos["qualidade"], buscar_valores_tabela("qualidade"))

    ttk.Label(form_frame, text="Coleção:").grid(row=12, column=0, sticky="w", padx=5, pady=3)
    campos["colecao"] = ttk.Combobox(form_frame, state="readonly")
    campos["colecao"].grid(row=12, column=1, columnspan=2, padx=5, pady=3, sticky="we")
    popular_dropdown(campos["colecao"], buscar_valores_tabela("colecao"))

    mapa_raridades = popular_dropdown(campos["raridade"], buscar_valores_tabela("raridade"))
    mapa_qualidades = popular_dropdown(campos["qualidade"], buscar_valores_tabela("qualidade"))
    mapa_colecoes = popular_dropdown(campos["colecao"], buscar_valores_tabela("colecao"))


    imagem_frame = ttk.LabelFrame(main_frame, text="Imagem", padding=10)
    imagem_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

    imagem_label = ttk.Label(imagem_frame)
    imagem_label.pack()

    


    def executar_scraping():
        try:
            raridade_nome = campos["raridade"].get()
            resultados = buscar_carta_myp(url=campos["link"].get(), chave=raridade_nome)
            if not resultados:
                root.after(0, lambda: messagebox.showwarning("Aviso", f"Nenhum resultado encontrado para {raridade_nome}.", parent=root))
                return

            dados = resultados[0]

            def preencher():
                campos["nome"].delete(0, tk.END)
                campos["nome"].insert(0, dados["nome"])
                campos["codigo"].delete(0, tk.END)
                campos["codigo"].insert(0, dados["codigo"])
                campos["preco_atual"].delete(0, tk.END)
                campos["preco_atual"].insert(0, limpar_preco(dados["preco_atual"]))
                # Preenche URL da imagem
                campos["imagem"].delete(0, tk.END)
                campos["imagem"].insert(0, dados["imagem"])

                # Baixa e preenche caminho salvo
                nome_arquivo = f"{dados['codigo']}.jpg"
                caminho_local = salvar_imagem_local(dados["imagem"], nome_arquivo)

                if caminho_local:
                    campos["imagem_salva"].delete(0, tk.END)
                    campos["imagem_salva"].insert(0, caminho_local)
                    atualizar_imagem(caminho_local)
                else:
                    atualizar_imagem(dados["imagem"])  # fallback

                campos["origem"].delete(0, tk.END)
                campos["origem"].insert(0, dados["origem"])

                colecao_nome = dados["colecao"].strip().lower()
                colecao_id = buscar_colecao_por_nome(colecao_nome)
                if not colecao_id:
                    colecao_id = inserir_colecao(colecao_nome)

                popular_dropdown(campos["colecao"], buscar_valores_tabela("colecao"))
                for i, val in enumerate(campos["colecao"].cget("values")):
                    if colecao_nome in val.lower():
                        campos["colecao"].current(i)
                        break

                messagebox.showinfo("Sucesso", "Dados preenchidos com sucesso!", parent=root)

            root.after(0, preencher)

        except Exception as e:
            root.after(0, lambda: messagebox.showerror("Erro", f"Erro ao buscar: {e}", parent=root))

    def salvar():
        try:
            campos_obrigatorios = [
                ("link", "Link da carta"),
                ("nome", "Nome"),
                ("codigo", "Código"),
                ("preco_da_compra", "Preço pago"),
                ("preco_atual", "Preço atual"),
                ("data", "Data da compra"),
                ("quantidade", "Quantidade"),
                ("imagem", "Imagem"),
                ("origem", "Origem"),
                ("raridade", "Raridade"),
                ("qualidade", "Qualidade"),
                ("colecao", "Coleção"),
                ("imagem_salva", "Imagem Salva")
                
            ]

            for chave, nome in campos_obrigatorios:
                valor = campos[chave].get().strip()
                if not valor:
                    messagebox.showerror("Erro", f"O campo '{nome}' não pode estar vazio.", parent=root)
                    return

            carta = {
                "link_site": campos["link"].get(),
                "nome": campos["nome"].get(),
                "codigo": campos["codigo"].get(),
                "preco_da_compra": limpar_preco(campos["preco_da_compra"].get()),
                "preco_atual": limpar_preco(campos["preco_atual"].get()),
                "data_da_compra": campos["data"].get(),
                "quantidade": int(campos["quantidade"].get()),
                "imagem": campos["imagem"].get() or IMAGEM_PADRAO,
                "origem": campos["origem"].get(),
                "raridade": mapa_raridades.get(campos["raridade"].get(), 1),
                "qualidade": mapa_qualidades.get(campos["qualidade"].get(), 1),
                "colecao": mapa_colecoes.get(campos["colecao"].get(), 1),
                "imagem_salva": campos["imagem_salva"].get(),

            }

            inserir_carta(carta)        

            
            messagebox.showinfo("Sucesso", "Carta cadastrada com sucesso!", parent=root)
            campos["link"].delete(0, tk.END)
            campos["nome"].delete(0, tk.END)   
            campos["codigo"].delete(0, tk.END)
            campos["preco_da_compra"].delete(0, tk.END)
            campos["preco_atual"].delete(0, tk.END)
            campos["data"].delete(0, tk.END)
            campos["quantidade"].delete(0, tk.END)
            campos["imagem"].delete(0, tk.END)
            campos["imagem_salva"].delete(0, tk.END)
            campos["imagem_salva"].insert(0, IMAGEM_PADRAO)
            atualizar_imagem(IMAGEM_PADRAO)
            campos["origem"].delete(0, tk.END)     
            campos["quantidade"].insert(0, "1")            
            campos["raridade"].current(0)
            campos["qualidade"].current(0)
            campos["colecao"].set("")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar no banco: {e}", parent=root)

    botoes_frame = ttk.Frame(main_frame)
    botoes_frame.grid(row=2, column=0, pady=10)
    ttk.Button(botoes_frame, text="Buscar via scraping", command=lambda: executar_em_thread(root, executar_scraping, titulo="Scraping", mensagem="Buscando dados da carta...")).grid(row=0, column=0, padx=10)
    ttk.Button(botoes_frame, text="Salvar Carta", command=salvar).grid(row=0, column=1, padx=10)

    campos["quantidade"].insert(0, "1")
    campos["imagem_salva"].insert(0, IMAGEM_PADRAO)
    atualizar_imagem(IMAGEM_PADRAO)
    campos["origem"].insert(0, "MyPCards")

    root.mainloop()


if __name__ == "__main__":
    app = tk.Tk()
    app.withdraw()
    criar_tela_cadastro(app)
    app.mainloop()
