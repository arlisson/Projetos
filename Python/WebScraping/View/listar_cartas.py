import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO

from DAO.database import (
    buscar_todas_cartas,
    buscar_carta_por_texto,
    calcula_quantidade,
    calcular_lucro_total_cartas_em_posse,    
    calcular_total_gasto_cartas,
    calcular_total_vendido_cartas,
    calcular_lucro_total_cartas_vendidas
)


def abrir_tela_listagem(app):
    from View.editar_cartas import criar_tela_editar_carta
    root = tk.Toplevel(app)
    root.title("Listagem de Cartas")
    #root.protocol("WM_DELETE_WINDOW", app.destroy)  # Comentar esta linha depois

    # Centraliza a janela
    largura, altura = 1200, 600
    x = (root.winfo_screenwidth() // 2) - (largura // 2)
    y = (root.winfo_screenheight() // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{x}+{y}")
    root.resizable(True, True)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(2, weight=1)

    # Frame com lucros
    lucro_frame = ttk.Frame(root, padding=(10, 5))
    lucro_frame.grid(row=0, column=0, sticky="ew")
    lucro_frame.columnconfigure(0, weight=1)
    lucro_frame.columnconfigure(1, weight=1)

    lucro_posse = calcular_lucro_total_cartas_em_posse()
    lucro_venda = calcular_lucro_total_cartas_vendidas()
    total_gasto = calcular_total_gasto_cartas()
    total_vendido = calcular_total_vendido_cartas()

    lbl_lucro_posse = ttk.Label(
        lucro_frame,
        text=f"💰 Lucro em posse: R$ {lucro_posse:.2f}",
        font=("Segoe UI", 10, "bold")
    )
    lbl_lucro_posse.grid(row=0, column=0, sticky="w", padx=5, pady=2)

    lbl_lucro_venda = ttk.Label(
        lucro_frame,
        text=f"💸 Lucro com vendas: R$ {lucro_venda:.2f}",
        font=("Segoe UI", 10, "bold")
    )
    lbl_lucro_venda.grid(row=0, column=1, sticky="e", padx=5, pady=2)

    lbl_total_gasto = ttk.Label(
        lucro_frame,
        text=f"📉 Total gasto: R$ {total_gasto:.2f}",
        font=("Segoe UI", 10, "bold")
    )
    lbl_total_gasto.grid(row=1, column=0, sticky="w", padx=5, pady=2)

    lbl_total_vendido = ttk.Label(
        lucro_frame,
        text=f"💵 Total vendido: R$ {total_vendido:.2f}",
        font=("Segoe UI", 10, "bold")
    )
    lbl_total_vendido.grid(row=1, column=1, sticky="e", padx=5, pady=2)

    # Campo de busca
    busca_frame = ttk.Frame(root, padding=5)
    busca_frame.grid(row=1, column=0, sticky="ew")
    busca_frame.columnconfigure(1, weight=1)

    ttk.Label(busca_frame, text="Buscar:").grid(row=0, column=0, padx=5)
    entrada_busca = ttk.Entry(busca_frame)
    entrada_busca.grid(row=0, column=1, padx=5, sticky="ew")

    # Frame com Canvas e Scroll
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
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Para Windows e Linux
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # Para MacOS (caso deseje compatibilidade)
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    # Ajusta largura do frame interno com o canvas
    def ajustar_largura(event):
        canvas.itemconfig(canvas_window, width=event.width)

    canvas.bind("<Configure>", ajustar_largura)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Cabeçalhos da tabela
    headers = [
        "Imagem", "Nome", "Código", "Preço Pago", "Preço Atual",
        "Total Pago", "Total Atual",
        "Lucro Unit.", "Lucro Total",
        "Data Compra", "Quantidade", "Data Scraping"
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

    for col in range(len(headers)):
        scrollable_frame.columnconfigure(col, weight=1)

    # Função para carregar as cartas
    def carregar_cartas(filtro=""):
        for widget in scrollable_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        if filtro:
            cartas = buscar_carta_por_texto(filtro)
            ttk.Label(lucro_frame, text=f"# Total Cartas unidade: {len(cartas)}", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w")
            ttk.Label(lucro_frame, text=f"# Total Cartas quantidade: {calcula_quantidade('carta')}", font=("Segoe UI", 10, "bold")).grid(row=2, column=1, sticky="e")
        else:
            cartas = buscar_todas_cartas()
            ttk.Label(lucro_frame, text=f"# Total Cartas unidade: {len(cartas)}", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w")
            ttk.Label(lucro_frame, text=f"# Total Cartas quantidade: {calcula_quantidade('carta')}", font=("Segoe UI", 10, "bold")).grid(row=2, column=1, sticky="e")



        if not cartas:
            lbl_vazio = ttk.Label(
                scrollable_frame,
                text="Nenhuma carta encontrada",
                font=("Segoe UI", 10, "italic"),
                foreground="gray"
            )
            lbl_vazio.grid(row=1, column=0, columnspan=len(headers), pady=20)
            return
       
        for row, carta in enumerate(cartas, start=1):
            id_carta = carta['id_carta']

            # Imagem
            try:
                with urllib.request.urlopen(carta['imagem']) as u:
                    raw_data = u.read()
                im = Image.open(BytesIO(raw_data)).resize((80, 112))
                photo = ImageTk.PhotoImage(im)
                lbl_img = tk.Label(scrollable_frame, image=photo, borderwidth=1, relief="solid")
                lbl_img.image = photo
                lbl_img.grid(row=row, column=0, padx=1, pady=1, sticky="nsew")

                # Clique na imagem
                lbl_img.bind("<Button-1>", lambda evt, id=id_carta: abrir_edicao(evt, id))

            except:
                lbl_img = tk.Label(scrollable_frame, text="Erro img", borderwidth=1, relief="solid")
                lbl_img.grid(row=row, column=0, sticky="nsew")
                lbl_img.bind("<Button-1>", lambda evt, id=id_carta: abrir_edicao(evt, id))

            # Dados da carta
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
                carta['data_scraping']
            ]

            for col, valor in enumerate(dados, start=1):
                lbl = ttk.Label(scrollable_frame, text=valor, borderwidth=1, relief="solid", padding=5)
                lbl.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

                # Clique nos dados
                lbl.bind("<Button-1>", lambda evt, id=id_carta: abrir_edicao(evt, id))

    def abrir_edicao(evt, id_carta):
        # print(f"[Clique] Editar carta ID: {id_carta}")
        # Exemplo:   
        root.destroy()     
        criar_tela_editar_carta(app, id_carta)
       


    # Atualizar ao digitar
    def ao_digitar(event):
        texto = entrada_busca.get()
        carregar_cartas(texto)

    entrada_busca.bind("<KeyRelease>", ao_digitar)    


    # Carregamento inicial
    carregar_cartas()


if __name__ == "__main__":
    app = tk.Tk()
    app.withdraw()
    abrir_tela_listagem(app)
    app.mainloop()
