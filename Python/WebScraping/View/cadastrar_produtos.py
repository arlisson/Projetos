import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
import urllib.request
from io import BytesIO
from datetime import datetime
from Utils.baixar_carta import salvar_imagem_local
from Utils.log import registrar_erro
from scraping.scraping_cartas import buscar_produto_liga
from DAO.database import inserir_produto
from decimal import Decimal
import threading
from Components.thread_com_modal import executar_em_thread

from Components.entrada_padrao import criar_entrada_com_botao_imagem, criar_entrada_padrao, criar_entrada_data_com_calendario

IMAGEM_PADRAO = "imagens/imagens_produtos/imagem_padrao.jpg"

def criar_tela_cadastro_produto(app):
    root = tk.Toplevel(app)
    root.grab_set()
    root.focus_force()
    root.title("Cadastro de Produto")
    root.resizable(True, True)

    largura, altura = 960, 640
    x = (root.winfo_screenwidth() // 2) - (largura // 2)
    y = (root.winfo_screenheight() // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{x}+{y}")
    root.attributes('-topmost', False)
    root.focus_set()

    main_frame = ttk.Frame(root, padding=10)
    main_frame.pack(fill="both", expand=True)

    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=0)
    main_frame.rowconfigure(0, weight=1)
    main_frame.rowconfigure(1, weight=0)

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

    form_frame = ttk.LabelFrame(main_frame, text="Dados do Produto", padding=10)
    form_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    form_frame.columnconfigure(1, weight=1)

    campos["link"] = criar_entrada_padrao(form_frame, "Link:", 0)
    campos["nome"] = criar_entrada_padrao(form_frame, "Nome:", 1)
    campos["imagem"] = criar_entrada_padrao(form_frame, "URL da Imagem:", 2)   

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
    
    campos["imagem_salva"] = criar_entrada_com_botao_imagem(
        frame=form_frame,
        texto="Imagem:",
        linha=3,
        ao_selecionar=atualizar_imagem,  # <- callback automático
        path="imagens/imagens_produtos",
        icone=FILE_ICON
    )

    
    campos["preco_compra"] = criar_entrada_padrao(form_frame, "Preço Compra:",  4)
    campos["preco_atual"] = criar_entrada_padrao(form_frame, "Preço Atual:", 5)

    campos["data_compra"] = criar_entrada_data_com_calendario(
        frame=form_frame,
        root=root,
        linha=6,
        texto_label="Data da Compra:",
        icone=CALENDAR_ICON
    )

    campos["quantidade"] = criar_entrada_padrao(form_frame, "Quantidade:", 7)
    campos["origem"] = criar_entrada_padrao(form_frame, "Origem:", 8)

    imagem_frame = ttk.LabelFrame(main_frame, text="Imagem", padding=10, width=320)
    imagem_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ns")

    imagem_label = ttk.Label(imagem_frame)
    imagem_label.pack()

    
    def to_decimal(valor):
        try:
            return float(str(valor).replace("R$", "").replace(",", ".").strip())
        except:
            return 0.0

    def buscar_info_scraping():
        url = campos["link"].get().strip()
        if not url:
            messagebox.showwarning("Aviso", "Informe o link do produto.", parent=root)
            return

        def _buscar():
            try:
                dados = buscar_produto_liga(url)
                if not dados:
                    # qualquer interação com UI precisa voltar pra main thread
                    return root.after(0, lambda: messagebox.showwarning(
                        "Aviso", "Nenhum dado retornado do scraping.", parent=root))

                # Atualize a UI sempre via main thread
                def preencher():
                    campos["nome"].delete(0, tk.END)
                    campos["nome"].insert(0, dados.get("nome", ""))

                    campos["imagem"].delete(0, tk.END)
                    campos["imagem"].insert(0, dados.get("imagem", ""))

                    preco = dados.get("preco_atual", "").replace("R$", "").replace(",", ".").strip()
                    campos["preco_atual"].delete(0, tk.END)
                    campos["preco_atual"].insert(0, preco)
                   
                   # Baixa e preenche caminho salvo
                    nome_arquivo = f"{dados['nome']}.jpg"
                    caminho_local = salvar_imagem_local(url_imagem=dados["imagem"], nome_arquivo=nome_arquivo, pasta="imagens/imagens_produtos")

                    if caminho_local:
                        campos["imagem_salva"].delete(0, tk.END)
                        campos["imagem_salva"].insert(0, caminho_local.replace("\\", "/"))
                        atualizar_imagem(caminho_local)
                    else:
                        atualizar_imagem(dados["imagem"])  # fallback
                    
                root.after(0, preencher)

            except Exception as e:
                root.after(0, lambda: messagebox.showerror("Erro", f"Erro no scraping: {e}", parent=root))

        # Aqui entra o seu modal com thread 👇
        executar_em_thread(
            root,
            _buscar,
            titulo="Buscando dados",
            mensagem="Coletando informações do produto..."
        )


    def salvar():
        try:
            # Validações na thread principal (importante!)
            campos_obrigatorios = [
                ("link", "Link"),
                ("nome", "Nome"),
                ("imagem", "Imagem"),
                ("preco_compra", "Preço Compra"),
                ("preco_atual", "Preço Atual"),
                ("data_compra", "Data da Compra"),
                ("quantidade", "Quantidade"),
                ("origem", "Origem"),
                ("imagem_salva", "Imagem Salva")
            ]

            for chave, nome in campos_obrigatorios:
                valor = campos[chave].get().strip()
                if not valor:
                    messagebox.showerror("Erro", f"O campo '{nome}' não pode estar vazio.", parent=root)
                    return

            produto = {
                "nome_produto": campos["nome"].get(),
                "link": campos["link"].get(),
                "imagem": campos["imagem"].get() or IMAGEM_PADRAO,
                "imagem_salva": campos["imagem_salva"].get().strip() or IMAGEM_PADRAO,
                "preco_compra": to_decimal(campos["preco_compra"].get()),
                "preco_atual": to_decimal(campos["preco_atual"].get()),
                "data_compra": campos["data_compra"].get(),
                "quantidade": int(campos["quantidade"].get()),
                "origem": campos["origem"].get() or "Liga Yugioh",
            }


            # Função que será executada na thread
            def _salvar():
                try:
                    inserir_produto(produto)
                    root.after(0, lambda: messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!", parent=root))
                    # campos["link"].delete(0, tk.END)
                    # campos["nome"].delete(0, tk.END)
                    # campos["imagem"].delete(0, tk.END)
                    # campos["imagem_salva"].delete(0, tk.END)
                    # campos["imagem_salva"].insert(0, IMAGEM_PADRAO)
                    # atualizar_imagem(IMAGEM_PADRAO)
                    # campos["preco_compra"].delete(0, tk.END)
                    # campos["preco_atual"].delete(0, tk.END)
                    # campos["data_compra"].delete(0, tk.END)
                    # campos["quantidade"].delete(0, tk.END)
                    # campos["quantidade"].insert(0, "1")
                    # campos["origem"].delete(0, tk.END)
                    # campos["origem"].insert(0, "Liga Yugioh")
                    
                except Exception as e:
                    root.after(0, lambda: messagebox.showerror("Erro", f"Erro ao salvar: {e}", parent=root))

            # Executa com modal de progresso
            executar_em_thread(
                root,
                _salvar,
                titulo="Salvando Produto",
                mensagem="Gravando dados no banco..."
            )

        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {e}", parent=root)


    botoes_frame = ttk.Frame(main_frame)
    botoes_frame.grid(row=1, column=0, columnspan=2, pady=10)

    ttk.Button(botoes_frame, text="Buscar via Scraping", command=buscar_info_scraping).pack(side="left", padx=20, pady=5)
    ttk.Button(botoes_frame, text="Salvar Produto", command=salvar).pack(side="left", padx=20, pady=5)

    
    campos["quantidade"].insert(0, "1")
    campos["imagem_salva"].insert(0, IMAGEM_PADRAO)
    campos["origem"].insert(0, "Liga Yugioh")
    atualizar_imagem(IMAGEM_PADRAO)

    root.mainloop()


if __name__ == "__main__":
    app = tk.Tk()
    app.withdraw()
    criar_tela_cadastro_produto(app)
    app.mainloop()
