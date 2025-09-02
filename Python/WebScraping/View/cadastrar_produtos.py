import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import urllib.request
from io import BytesIO
from datetime import datetime
from scraping.scraping_cartas import buscar_produto_liga
from DAO.database import inserir_produto
from tkcalendar import Calendar

IMAGEM_PADRAO = "https://i.pinimg.com/736x/71/1e/da/711eda25308c65a7756751088866e181.jpg"

def criar_tela_cadastro_produto(app):
    root = tk.Toplevel(app)
    root.title("Cadastro de Produto")
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
            campos["data_compra"].delete(0, tk.END)
            campos["data_compra"].insert(0, cal.get_date())
            top.destroy()

        ttk.Button(top, text="Selecionar", command=selecionar_data).pack(pady=5)

    def criar_entrada(frame, label, row):
        ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", padx=5, pady=3)
        entry = ttk.Entry(frame)
        entry.grid(row=row, column=1, sticky="ew", padx=5, pady=3)
        return entry

    form_frame = ttk.LabelFrame(main_frame, text="Dados do Produto", padding=10)
    form_frame.grid(row=0, column=0, sticky="nsew")
    for i in range(9):
        form_frame.rowconfigure(i, weight=1)
    form_frame.columnconfigure(1, weight=1)

    campos["link"] = criar_entrada(form_frame, "Link:", 0)
    campos["nome"] = criar_entrada(form_frame, "Nome:", 1)
    campos["imagem"] = criar_entrada(form_frame, "URL da Imagem:", 2)
    campos["preco_compra"] = criar_entrada(form_frame, "Preço Compra:", 3)
    campos["preco_atual"] = criar_entrada(form_frame, "Preço Atual:", 4)

    ttk.Label(form_frame, text="Data da Compra:").grid(row=5, column=0, sticky="w", padx=5, pady=3)
    data_frame = ttk.Frame(form_frame)
    data_frame.grid(row=5, column=1, padx=5, pady=3, sticky="we")
    data_frame.columnconfigure(0, weight=1)

    campos["data_compra"] = ttk.Entry(data_frame)
    campos["data_compra"].grid(row=0, column=0, sticky="we", padx=(0, 5))
    btn = ttk.Button(data_frame, image=CALENDAR_ICON, command=abrir_calendario)
    btn.image = CALENDAR_ICON
    btn.grid(row=0, column=1)

    campos["quantidade"] = criar_entrada(form_frame, "Quantidade:", 6)
    campos["origem"] = criar_entrada(form_frame, "Origem:", 7)

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

    def buscar_info_scraping():
        url = campos["link"].get().strip()
        if not url:
            messagebox.showwarning("Aviso", "Informe o link do produto.")
            return

        dados = buscar_produto_liga(url)
        if not dados:
            messagebox.showwarning("Aviso", "Nenhum dado retornado do scraping.")
            return

        campos["nome"].delete(0, tk.END)
        campos["nome"].insert(0, dados.get("nome", ""))

        campos["imagem"].delete(0, tk.END)
        campos["imagem"].insert(0, dados.get("imagem", ""))

        preco = dados.get("preco_atual", "").replace("R$", "").replace(",", ".").strip()
        campos["preco_atual"].delete(0, tk.END)
        campos["preco_atual"].insert(0, preco)

        campos["data_compra"].delete(0, tk.END)
        campos["data_compra"].insert(0, datetime.today().strftime("%Y-%m-%d"))

        atualizar_imagem(campos["imagem"].get())

    def salvar():
        try:
            produto = {
                "nome_produto": campos["nome"].get(),
                "link": campos["link"].get(),
                "imagem": campos["imagem"].get() or IMAGEM_PADRAO,
                "preco_compra": float(campos["preco_compra"].get().replace(",", ".")),
                "preco_atual": float(campos["preco_atual"].get().replace(",", ".")),
                "data_scraping": campos["data_compra"].get(),
                "quantidade": int(campos["quantidade"].get()),
                "origem": campos["origem"].get() or "Liga Yugioh"
            }
            inserir_produto(produto)
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            root.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    botoes_frame = ttk.Frame(main_frame)
    botoes_frame.grid(row=1, column=0, pady=10)
    ttk.Button(botoes_frame, text="Buscar via Scraping", command=buscar_info_scraping).grid(row=0, column=0, padx=10)
    ttk.Button(botoes_frame, text="Salvar Produto", command=salvar).grid(row=0, column=1, padx=10)

    campos["data_compra"].insert(0, datetime.today().strftime("%Y-%m-%d"))
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
