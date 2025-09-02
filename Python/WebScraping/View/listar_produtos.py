import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO
from DAO.database import (
    listar_todos_produtos,
    calcular_lucro_total_produtos_em_posse,
    calcular_lucro_total_produtos_vendidos,
    calcular_total_gasto_produtos,
    calcular_total_vendido_produtos,
    
)

def abrir_tela_listagem_produtos(app):
    root = tk.Toplevel(app)
    root.title("Listagem de Produtos")

    largura, altura = 1200, 600
    x = (root.winfo_screenwidth() // 2) - (largura // 2)
    y = (root.winfo_screenheight() // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{x}+{y}")
    root.resizable(True, True)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(2, weight=1)

    lucro_frame = ttk.Frame(root, padding=(10, 5))
    lucro_frame.grid(row=0, column=0, sticky="ew")
    lucro_frame.columnconfigure(0, weight=1)
    lucro_frame.columnconfigure(1, weight=1)

    lucro_posse = calcular_lucro_total_produtos_em_posse()
    lucro_venda = calcular_lucro_total_produtos_vendidos()
    total_gasto = calcular_total_gasto_produtos()
    total_vendido = calcular_total_vendido_produtos()

    ttk.Label(lucro_frame, text=f"💰 Lucro em posse: R$ {lucro_posse:.2f}", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")
    ttk.Label(lucro_frame, text=f"💵 Lucro com vendas: R$ {lucro_venda:.2f}", font=("Segoe UI", 10, "bold")).grid(row=0, column=1, sticky="e")
    ttk.Label(lucro_frame, text=f"💵 Total gasto: R$ {total_gasto:.2f}", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w")
    ttk.Label(lucro_frame, text=f"💵 Total vendido: R$ {total_vendido:.2f}", font=("Segoe UI", 10, "bold")).grid(row=1, column=1, sticky="e")

    busca_frame = ttk.Frame(root, padding=5)
    busca_frame.grid(row=1, column=0, sticky="ew")
    busca_frame.columnconfigure(1, weight=1)
    ttk.Label(busca_frame, text="Buscar:").grid(row=0, column=0, padx=5)
    entrada_busca = ttk.Entry(busca_frame)
    entrada_busca.grid(row=0, column=1, padx=5, sticky="ew")

    main_frame = ttk.Frame(root)
    main_frame.grid(row=2, column=0, sticky="nsew")
    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(0, weight=1)

    canvas = tk.Canvas(main_frame)
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    scrollable_frame = ttk.Frame(canvas)
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.bind("<Configure>", lambda event: canvas.itemconfig(canvas_window, width=event.width))
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    headers = [
        "Imagem", "Nome", "Preço Compra", "Preço Atual",
        "Total Pago", "Total Atual",
        "Lucro Unit.", "Lucro Total",
        "Quantidade", "Data", "Origem"
    ]

    for col, header in enumerate(headers):
        ttk.Label(scrollable_frame, text=header, font=("Segoe UI", 10, "bold"), borderwidth=1, relief="solid", padding=5).grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
        scrollable_frame.columnconfigure(col, weight=1)

    def carregar_produtos(filtro=""):
        for widget in scrollable_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        produtos = listar_todos_produtos(filtro)

        for row, produto in enumerate(produtos, start=1):
            try:
                with urllib.request.urlopen(produto["imagem"]) as u:
                    raw_data = u.read()
                im = Image.open(BytesIO(raw_data)).resize((80, 112))
                photo = ImageTk.PhotoImage(im)
                img_label = tk.Label(scrollable_frame, image=photo, borderwidth=1, relief="solid")
                img_label.image = photo
                img_label.grid(row=row, column=0, padx=1, pady=1, sticky="nsew")
            except:
                tk.Label(scrollable_frame, text="Erro img", borderwidth=1, relief="solid").grid(row=row, column=0, sticky="nsew")

            preco_compra = produto['preco_compra'] or 0.0
            preco_atual = produto['preco_atual'] or 0.0
            quantidade = produto.get('quantidade', 1) or 1
            total_pago = preco_compra * quantidade
            total_atual = preco_atual * quantidade
            lucro_unit = preco_atual - preco_compra
            lucro_total = lucro_unit * quantidade

            dados = [
                produto["nome_produto"],
                f"R$ {preco_compra:.2f}",
                f"R$ {preco_atual:.2f}",
                f"R$ {total_pago:.2f}",
                f"R$ {total_atual:.2f}",
                f"R$ {lucro_unit:.2f}",
                f"R$ {lucro_total:.2f}",
                str(quantidade),
                produto["data_scraping"],
                produto["origem"]
            ]

            for col, valor in enumerate(dados, start=1):
                ttk.Label(scrollable_frame, text=valor, borderwidth=1, relief="solid", padding=5).grid(
                    row=row, column=col, sticky="nsew", padx=1, pady=1
                )

    def ao_digitar(event):
        carregar_produtos(entrada_busca.get())

    entrada_busca.bind("<KeyRelease>", ao_digitar)
    carregar_produtos()

if __name__ == "__main__":
    app = tk.Tk()
    app.withdraw()
    abrir_tela_listagem_produtos(app)
    app.mainloop()
