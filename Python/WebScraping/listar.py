import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO
from DAO import buscar_todas_cartas


def abrir_tela_listagem():
    root = tk.Toplevel()
    root.title("Listagem de Cartas")
    root.geometry("1200x600")
    root.resizable(True, True)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    main_frame = ttk.Frame(root)
    main_frame.grid(row=0, column=0, sticky="nsew")
    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(0, weight=1)

    canvas = tk.Canvas(main_frame)
    canvas.grid(row=0, column=0, sticky="nsew")

    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")

    scrollable_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Cabeçalhos das colunas
    headers = [
        "Imagem", "Nome", "Código", "Preço Pago", "Preço Atual",
        "Preço Pago x Qtde", "Preço Atual x Qtde",
        "Lucro Unit.", "Lucro Total",
        "Data Compra", "Quantidade"
    ]

    for col, header in enumerate(headers):
        lbl = ttk.Label(
            scrollable_frame,
            text=header,
            font=("Segoe UI", 10, "bold"),
            borderwidth=1,
            relief="solid",
            padding=5
        )
        lbl.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

    # Permitir expansão das colunas
    for col in range(len(headers)):
        scrollable_frame.columnconfigure(col, weight=1)

    cartas = buscar_todas_cartas()

    for row, carta in enumerate(cartas, start=1):
        # Carregar imagem
        try:
            with urllib.request.urlopen(carta['imagem']) as u:
                raw_data = u.read()
            im = Image.open(BytesIO(raw_data)).resize((80, 112))
            photo = ImageTk.PhotoImage(im)
            lbl = tk.Label(scrollable_frame, image=photo)
            lbl.image = photo
            lbl.grid(row=row, column=0, padx=2, pady=2)
        except:
            tk.Label(scrollable_frame, text="Erro img").grid(row=row, column=0)

        # Cálculos
        preco_pago = carta['preco_da_compra']
        preco_atual = carta['preco_atual']
        quantidade = carta['quantidade']
        total_pago = preco_pago * quantidade
        total_atual = preco_atual * quantidade
        lucro_unit = preco_atual - preco_pago
        lucro_total = lucro_unit * quantidade

        # Dados textuais
        ttk.Label(scrollable_frame, text=carta['nome'], anchor="w").grid(row=row, column=1, sticky="w", padx=2)
        ttk.Label(scrollable_frame, text=carta['codigo']).grid(row=row, column=2, padx=2)
        ttk.Label(scrollable_frame, text=f"R$ {preco_pago:.2f}").grid(row=row, column=3, padx=2)
        ttk.Label(scrollable_frame, text=f"R$ {preco_atual:.2f}").grid(row=row, column=4, padx=2)

        ttk.Label(scrollable_frame, text=f"R$ {total_pago:.2f}").grid(row=row, column=5, padx=2)
        ttk.Label(scrollable_frame, text=f"R$ {total_atual:.2f}").grid(row=row, column=6, padx=2)
        ttk.Label(scrollable_frame, text=f"R$ {lucro_unit:.2f}").grid(row=row, column=7, padx=2)
        ttk.Label(scrollable_frame, text=f"R$ {lucro_total:.2f}").grid(row=row, column=8, padx=2)

        ttk.Label(scrollable_frame, text=carta['data_da_compra']).grid(row=row, column=9, padx=2)
        ttk.Label(scrollable_frame, text=quantidade).grid(row=row, column=10, padx=2)


if __name__ == "__main__":
    app = tk.Tk()
    app.withdraw()
    abrir_tela_listagem()
    app.mainloop()
