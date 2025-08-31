import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import urllib.request
from io import BytesIO
from datetime import datetime
from scraping_cartas import *
from DAO import *
from tkcalendar import Calendar

IMAGEM_PADRAO = "https://i.pinimg.com/736x/71/1e/da/711eda25308c65a7756751088866e181.jpg"

def criar_tela_cadastro(app):
    root = tk.Toplevel(app)
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

    calendar_img = Image.open("imagens/calendario.png").resize((20, 20))
    CALENDAR_ICON = ImageTk.PhotoImage(calendar_img)

    campos = {}

    def abrir_calendario():
        top = tk.Toplevel(root)
        top.title("Selecionar Data")
        top.grab_set()
        top.resizable(False, False)
        top.geometry(f"+{root.winfo_rootx() + 200}+{root.winfo_rooty() + 150}")
        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(padx=10, pady=10)

        def selecionar_data():
            campos["data"].delete(0, tk.END)
            campos["data"].insert(0, cal.get_date())
            top.destroy()

        ttk.Button(top, text="Selecionar", command=selecionar_data).pack(pady=5)

    def criar_rotulo_entrada(frame, texto, linha, largura=50, somente_leitura=False):
        ttk.Label(frame, text=texto).grid(row=linha, column=0, sticky="w", padx=5, pady=3)
        entrada = ttk.Entry(frame, width=largura)
        if somente_leitura:
            entrada.configure(state="readonly")
        entrada.grid(row=linha, column=1, columnspan=2, padx=5, pady=3, sticky="we")
        return entrada

    form_frame = ttk.LabelFrame(main_frame, text="Dados da Carta", padding=10)
    form_frame.grid(row=0, column=0, sticky="nsew")
    form_frame.columnconfigure(1, weight=1)

    campos["link"] = criar_rotulo_entrada(form_frame, "Link da carta:", 0)
    campos["nome"] = criar_rotulo_entrada(form_frame, "Nome:", 1)
    campos["codigo"] = criar_rotulo_entrada(form_frame, "Código:", 2)
    campos["preco"] = criar_rotulo_entrada(form_frame, "Preço pago:", 3)
    campos["preco_atual"] = criar_rotulo_entrada(form_frame, "Preço atual:", 4, somente_leitura=True)

    # Campo de data com botão de calendário
    ttk.Label(form_frame, text="Data da compra:").grid(row=5, column=0, sticky="w", padx=5, pady=3)
    data_frame = ttk.Frame(form_frame)
    data_frame.grid(row=5, column=1, columnspan=2, padx=5, pady=3, sticky="we")
    data_frame.columnconfigure(0, weight=1)

    campos["data"] = ttk.Entry(data_frame)
    campos["data"].grid(row=0, column=0, sticky="we", padx=(0, 5))

    btn = ttk.Button(data_frame, image=CALENDAR_ICON, command=abrir_calendario)
    btn.image = CALENDAR_ICON
    btn.grid(row=0, column=1)

    campos["quantidade"] = criar_rotulo_entrada(form_frame, "Quantidade:", 6)
    campos["imagem"] = criar_rotulo_entrada(form_frame, "Imagem URL:", 7)

    def popular_dropdown(combo, dados):
        valores = [f"{item[0]} - {item[1]}" for item in dados]
        combo["values"] = valores
        if valores:
            combo.current(0)

    ttk.Label(form_frame, text="Raridade:").grid(row=8, column=0, sticky="w", padx=5, pady=3)
    campos["raridade"] = ttk.Combobox(form_frame, state="readonly")
    campos["raridade"].grid(row=8, column=1, padx=5, pady=3, sticky="we")
    popular_dropdown(campos["raridade"], buscar_valores_tabela("raridade"))

    ttk.Label(form_frame, text="Qualidade:").grid(row=9, column=0, sticky="w", padx=5, pady=3)
    campos["qualidade"] = ttk.Combobox(form_frame, state="readonly")
    campos["qualidade"].grid(row=9, column=1, padx=5, pady=3, sticky="we")
    popular_dropdown(campos["qualidade"], buscar_valores_tabela("qualidade"))

    ttk.Label(form_frame, text="Coleção:").grid(row=10, column=0, sticky="w", padx=5, pady=3)
    campos["colecao"] = ttk.Combobox(form_frame, state="readonly")
    campos["colecao"].grid(row=10, column=1, padx=5, pady=3, sticky="we")
    popular_dropdown(campos["colecao"], buscar_valores_tabela("colecao"))

    imagem_frame = ttk.LabelFrame(main_frame, text="Imagem", padding=10)
    imagem_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

    imagem_label = ttk.Label(imagem_frame)
    imagem_label.pack()

    def atualizar_imagem(url):
        try:
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()
            im = Image.open(BytesIO(raw_data))
            im.thumbnail((300, 420))
            photo = ImageTk.PhotoImage(im)
            imagem_label.configure(image=photo)
            imagem_label.image = photo
        except:
            imagem_label.configure(image='')
            imagem_label.image = None

    def limpar_preco(preco_str):
        try:
            preco_str = preco_str.replace("R$", "").replace(",", ".").strip()
            return float(preco_str)
        except:
            return 0.0

    def preencher_com_scraping():
        try:
            raridade_nome = campos["raridade"].get().split(" - ")[1]
            resultados = buscar_carta_myp(url=campos["link"].get(), chave=raridade_nome)
            if not resultados:
                messagebox.showwarning("Aviso", "Nenhum resultado encontrado.")
                return
            dados = resultados[0]

            campos["nome"].delete(0, tk.END)
            campos["nome"].insert(0, dados["nome"])
            campos["codigo"].delete(0, tk.END)
            campos["codigo"].insert(0, dados["codigo"])

            # Preencher somente o campo de preço atual (somente leitura)
            campos["preco_atual"].configure(state="normal")
            campos["preco_atual"].delete(0, tk.END)
            campos["preco_atual"].insert(0, limpar_preco(dados["preco_atual"]))
            campos["preco_atual"].configure(state="readonly")

            campos["imagem"].delete(0, tk.END)
            campos["imagem"].insert(0, dados["imagem"])
            atualizar_imagem(dados["imagem"])

            colecao_nome = dados["colecao"]
            colecao_id = buscar_colecao_por_nome(colecao_nome)
            if not colecao_id:
                colecao_id = inserir_colecao(colecao_nome)
            popular_dropdown(campos["colecao"], buscar_valores_tabela("colecao"))
            for i, val in enumerate(campos["colecao"].cget("values")):
                if val.startswith(f"{colecao_id} -"):
                    campos["colecao"].current(i)
                    break

            messagebox.showinfo("Sucesso", "Dados preenchidos com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar: {e}")

    def salvar():
        try:
            carta = {
                "link_site": campos["link"].get(),
                "nome": campos["nome"].get(),
                "codigo": campos["codigo"].get(),
                "preco": limpar_preco(campos["preco"].get()),
                "preco_atual": limpar_preco(campos["preco_atual"].get()),
                "data_da_compra": campos["data"].get(),
                "quantidade": int(campos["quantidade"].get()),
                "imagem": campos["imagem"].get() or IMAGEM_PADRAO,
                "raridade": int(campos["raridade"].get().split(" - ")[0]),
                "qualidade": int(campos["qualidade"].get().split(" - ")[0]),
                "colecao": int(campos["colecao"].get().split(" - ")[0]),
            }
            inserir_carta(carta)
            messagebox.showinfo("Sucesso", "Carta cadastrada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar no banco: {e}")

    botoes_frame = ttk.Frame(main_frame)
    botoes_frame.grid(row=2, column=0, pady=10)
    ttk.Button(botoes_frame, text="Buscar via scraping", command=preencher_com_scraping).grid(row=0, column=0, padx=10)
    ttk.Button(botoes_frame, text="Salvar Carta", command=salvar).grid(row=0, column=1, padx=10)

    campos["data"].insert(0, datetime.today().strftime("%Y-%m-%d"))
    campos["quantidade"].insert(0, "1")
    campos["imagem"].insert(0, IMAGEM_PADRAO)
    atualizar_imagem(IMAGEM_PADRAO)

    root.mainloop()


if __name__ == "__main__":
    app = tk.Tk()
    app.withdraw()
    criar_tela_cadastro(app)
    app.mainloop()