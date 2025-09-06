import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO

from DAO.database import (    
    calcular_lucro_total_cartas_em_posse,
    calcular_quantidade_vendida,    
    calcular_total_gasto_cartas,
    calcular_total_vendido_cartas,
    calcular_lucro_total_cartas_vendidas,
    listar_venda_filtro,
    listar_vendas
)

from Components.thread_com_modal import executar_em_thread

def abrir_tela_listagem_venda(app):
    from View.editar_venda_cartas import criar_tela_editar_venda_carta

    root = tk.Toplevel(app)
    root.title("Listagem de Cartas Vendidas")

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

    lucro_posse = calcular_lucro_total_cartas_em_posse()
    lucro_venda = calcular_lucro_total_cartas_vendidas()
    total_gasto = calcular_total_gasto_cartas()
    total_vendido = calcular_total_vendido_cartas()

    ttk.Label(lucro_frame, text=f"💰 Lucro em posse: R$ {lucro_posse:.2f}", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=2)
    ttk.Label(lucro_frame, text=f"💸 Lucro com vendas: R$ {lucro_venda:.2f}", font=("Segoe UI", 10, "bold")).grid(row=0, column=1, sticky="e", padx=5, pady=2)
    ttk.Label(lucro_frame, text=f"📉 Total gasto: R$ {total_gasto:.2f}", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w", padx=5, pady=2)
    ttk.Label(lucro_frame, text=f"💵 Total vendido: R$ {total_vendido:.2f}", font=("Segoe UI", 10, "bold")).grid(row=1, column=1, sticky="e", padx=5, pady=2)

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

    scrollbar_y = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollbar_y.grid(row=0, column=1, sticky="ns")

    scrollbar_x = ttk.Scrollbar(main_frame, orient="horizontal", command=canvas.xview)
    scrollbar_x.grid(row=1, column=0, sticky="ew")

    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    scrollable_frame = ttk.Frame(canvas)
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def ajustar_canvas(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", ajustar_canvas)

    def ajustar_largura_canvas(event):
        canvas.itemconfig(canvas_window, width=max(event.width, scrollable_frame.winfo_reqwidth()))

    canvas.bind("<Configure>", ajustar_largura_canvas)

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    headers = [
        "Imagem", "Nome", "Código", "Preço Pago", "Preço Atual",
        "Total Pago", "Total Atual",
        "Lucro Unit.", "Lucro Total",
        "Data Compra", "Quantidade", "Data da Venda",
        "Preço da Venda", "Data Scraping"
    ]

    for col, header in enumerate(headers):
        ttk.Label(
            scrollable_frame,
            text=header,
            font=("Segoe UI", 10, "bold"),
            borderwidth=1,
            relief="solid",
            padding=5
        ).grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

    for col in range(len(headers)):
        scrollable_frame.columnconfigure(col, weight=1)

    def carregar_cartas(filtro=""):
        for widget in scrollable_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        cartas = listar_venda_filtro('carta', filtro) if filtro else listar_vendas('carta')

        ttk.Label(lucro_frame, text=f"# Total Cartas unidade: {len(cartas)}", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w")
        ttk.Label(lucro_frame, text=f"# Total Cartas quantidade: {calcular_quantidade_vendida('venda')}", font=("Segoe UI", 10, "bold")).grid(row=2, column=1, sticky="e")

        if not cartas:
            ttk.Label(
                scrollable_frame,
                text="Nenhuma carta encontrada",
                font=("Segoe UI", 10, "italic"),
                foreground="gray"
            ).grid(row=1, column=0, columnspan=len(headers), pady=20)
            return

        for row, carta in enumerate(cartas, start=1):
            id_carta = carta['id_carta']
            widgets_linha = []

            frame_img = ttk.Frame(scrollable_frame, relief="solid", borderwidth=1)
            frame_img.grid(row=row, column=0, padx=1, pady=1, sticky="nsew")

            try:
                with urllib.request.urlopen(carta['imagem']) as u:
                    raw_data = u.read()
                im = Image.open(BytesIO(raw_data)).resize((80, 112))
                photo = ImageTk.PhotoImage(im)
                lbl_img = tk.Label(frame_img, image=photo, bg="white")
                lbl_img.image = photo
            except:
                lbl_img = tk.Label(frame_img, text="Erro img", bg="white")

            lbl_img.pack()

            lbl_raridade = ttk.Label(
                frame_img,
                text=carta.get('raridade_nome', 'N/A'),
                font=("Segoe UI", 8),
                anchor="center",
                justify="center",
                wraplength=80
            )
            lbl_raridade.pack(fill="x", padx=2, pady=(2, 4))

            for w in [frame_img, lbl_img, lbl_raridade]:
                w.bind("<Button-1>", lambda evt, id=id_carta: abrir_edicao(evt, id))

            widgets_linha.append(lbl_img)

            preco_pago = carta['preco_da_compra']
            preco_atual = carta['preco_atual']
            quantidade = carta['quantidade']
            total_pago = preco_pago * quantidade
            total_atual = preco_atual * quantidade
            lucro_unit = preco_atual - preco_pago
            lucro_total = lucro_unit * quantidade

            dados = [
                carta['nome'],
                carta['codigo'],
                f"R$ {preco_pago:.2f}",
                f"R$ {preco_atual:.2f}",
                f"R$ {total_pago:.2f}",
                f"R$ {total_atual:.2f}",
                f"R$ {lucro_unit:.2f}",
                f"R$ {lucro_total:.2f}",
                carta['data_da_compra'],
                str(quantidade),
                carta['data_da_venda'],
                f"R$ {carta['preco_da_venda']:.2f}",
                carta['data_scraping']
            ]

            for col, valor in enumerate(dados, start=1):
                lbl = tk.Label(scrollable_frame, text=valor, borderwidth=1, relief="solid", bg="white", padx=5, pady=3)
                lbl.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
                lbl.bind("<Button-1>", lambda evt, id=id_carta: abrir_edicao(evt, id))
                widgets_linha.append(lbl)

            def on_enter(event, widgets=widgets_linha):
                for w in widgets:
                    try: w.configure(bg="#e0e0e0")
                    except: pass

            def on_leave(event, widgets=widgets_linha):
                for w in widgets:
                    try: w.configure(bg="white")
                    except: pass

            for widget in widgets_linha:
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)

    def abrir_edicao(evt, id_carta):
        root.destroy()
        criar_tela_editar_venda_carta(app, id_carta)

    entrada_busca.bind("<KeyRelease>", lambda e: carregar_cartas(entrada_busca.get()))

    executar_em_thread(
        root,
        lambda: carregar_cartas(),
        titulo="Listando Cartas",
        mensagem="Carregando cartas do banco..."
    )

if __name__ == "__main__":
    app = tk.Tk()
    app.withdraw()
    abrir_tela_listagem_venda(app)
    app.mainloop()
