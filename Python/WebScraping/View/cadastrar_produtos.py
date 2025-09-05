import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import urllib.request
from io import BytesIO
from datetime import datetime
from scraping.scraping_cartas import buscar_produto_liga
from DAO.database import inserir_produto
from decimal import Decimal
import threading
from Components.thread_com_modal import executar_em_thread

from Components.entrada_padrao import criar_entrada_padrao, criar_entrada_data_com_calendario

IMAGEM_PADRAO = "https://i.pinimg.com/736x/71/1e/da/711eda25308c65a7756751088866e181.jpg"

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
        CALENDAR_ICON = ImageTk.PhotoImage(calendar_img)
    except:
        CALENDAR_ICON = None

    campos = {}

    form_frame = ttk.LabelFrame(main_frame, text="Dados do Produto", padding=10)
    form_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    form_frame.columnconfigure(1, weight=1)

    campos["link"] = criar_entrada_padrao(form_frame, "Link:", 0)
    campos["nome"] = criar_entrada_padrao(form_frame, "Nome:", 1)
    campos["imagem"] = criar_entrada_padrao(form_frame, "URL da Imagem:", 2)
    campos["preco_compra"] = criar_entrada_padrao(form_frame, "Preço Compra:", 3)
    campos["preco_atual"] = criar_entrada_padrao(form_frame, "Preço Atual:", 4)
    campos["data_compra"] = criar_entrada_data_com_calendario(form_frame, root, 5, "Data da Compra:", CALENDAR_ICON)
    campos["quantidade"] = criar_entrada_padrao(form_frame, "Quantidade:", 6)
    campos["origem"] = criar_entrada_padrao(form_frame, "Origem:", 7)

    imagem_frame = ttk.LabelFrame(main_frame, text="Imagem", padding=10, width=320)
    imagem_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ns")

    imagem_label = ttk.Label(imagem_frame)
    imagem_label.pack()

    def atualizar_imagem(url):
        def _baixar():
            try:
                with urllib.request.urlopen(url) as u:
                    raw_data = u.read()
                im = Image.open(BytesIO(raw_data))
                im.thumbnail((300, 420))
                photo = ImageTk.PhotoImage(im)
                root.after(0, lambda: (imagem_label.configure(image=photo), setattr(imagem_label, 'image', photo)))
            except:
                root.after(0, lambda: (imagem_label.configure(image=''), setattr(imagem_label, 'image', None)))
        threading.Thread(target=_baixar, daemon=True).start()

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

                    campos["data_compra"].delete(0, tk.END)
                    campos["data_compra"].insert(0, "")

                    atualizar_imagem(campos["imagem"].get())

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
                ("origem", "Origem")
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
    campos["imagem"].insert(0, IMAGEM_PADRAO)
    campos["origem"].insert(0, "Liga Yugioh")
    atualizar_imagem(IMAGEM_PADRAO)

    root.mainloop()


if __name__ == "__main__":
    app = tk.Tk()
    app.withdraw()
    criar_tela_cadastro_produto(app)
    app.mainloop()
