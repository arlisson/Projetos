import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO
from DAO.database import (
    calcula_quantidade,
    listar_todos_produtos,
    calcular_lucro_total_produtos_em_posse,
    calcular_lucro_total_produtos_vendidos,
    calcular_total_gasto_produtos,
    calcular_total_vendido_produtos,
)
from Utils.log import registrar_erro
from Components.sumario import criar_summary_frame as sumario
from Components.scrollable_frame import ScrollableFrame

def abrir_tela_editar_produto(app, id_produto):
    from View.editar_produto import criar_tela_editar_produto
    app.after(100, lambda: criar_tela_editar_produto(app, id_produto))

def abrir_tela_listagem_produtos(app):
    root = tk.Toplevel(app)
    root.title("Listagem de Produtos")
    root.grab_set()
    root.focus_force()
    busca_timeout = None

    largura, altura = 1200, 600
    x = (root.winfo_screenwidth() // 2) - (largura // 2)
    y = (root.winfo_screenheight() // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{x}+{y}")
    root.resizable(True, True)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(2, weight=1)

    lucro_posse = calcular_lucro_total_produtos_em_posse()
    lucro_venda = calcular_lucro_total_produtos_vendidos()
    total_gasto = calcular_total_gasto_produtos()
    total_vendido = calcular_total_vendido_produtos()
    total_quantidade = calcula_quantidade('produto')
    total_quantidade_unidade = len(listar_todos_produtos()) or 0

    dados_resumo = [
        {"emoji": "💰", "texto": "Lucro em posse", "valor": lucro_posse, "row": 0, "column": 0, "anchor": "w"},
        {"emoji": "💸", "texto": "Lucro com vendas", "valor": lucro_venda, "row": 0, "column": 1, "anchor": "e"},
        {"emoji": "📉", "texto": "Total gasto", "valor": total_gasto, "row": 1, "column": 0, "anchor": "w"},
        {"emoji": "💵", "texto": "Total vendido", "valor": total_vendido, "row": 1, "column": 1, "anchor": "e"},
        {"emoji": "📦", "texto": "Total Produtos Unidade", "valor": str(total_quantidade_unidade), "row": 2, "column": 0, "anchor": "w"},
        {"emoji": "📦", "texto": "Total Produtos Quantidade", "valor": str(total_quantidade), "row": 2, "column": 1, "anchor": "e"},
    ]

    frame_resumo = sumario(root, "Resumo Financeiro", dados_resumo)
    frame_resumo.grid(row=0, column=0, columnspan=2, sticky="ew")

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

    scrollable = ScrollableFrame(main_frame)
    scrollable.grid(row=0, column=0, sticky="nsew")
    scrollable_frame = scrollable.scrollable_frame

    headers = [
        "Imagem", "Nome", "Preço Compra", "Preço Atual",
        "Total Pago", "Total Atual", "Lucro Unit.", "Lucro Total",
        "Quantidade", "Data da compra", "Origem", "Data Scraping"
    ]

    for col, header in enumerate(headers):
        ttk.Label(scrollable_frame, text=header, font=("Segoe UI", 10, "bold"), borderwidth=1, relief="solid", padding=5).grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
        scrollable_frame.columnconfigure(col, weight=1)

    def abrir_edicao(evt, id_produto):
        root.destroy()
        abrir_tela_editar_produto(app, id_produto)

    def carregar_produtos(filtro=""):
        for widget in scrollable_frame.winfo_children():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        produtos = listar_todos_produtos(filtro)

        if not produtos:
            ttk.Label(
                scrollable_frame,
                text="Nenhum produto encontrado",
                font=("Segoe UI", 10, "italic"),
                foreground="gray"
            ).grid(row=1, column=0, columnspan=len(headers), pady=20)
            return

        for row, produto in enumerate(produtos, start=1):
            id_produto = produto["id_produto"]
            widgets_linha = []

            frame_img = ttk.Frame(scrollable_frame, relief="solid", borderwidth=1)
            frame_img.grid(row=row, column=0, padx=1, pady=1, sticky="nsew")

            try:
                caminho_imagem = produto.get('imagem_salva') or produto.get('imagem')

                if caminho_imagem.startswith("http://") or caminho_imagem.startswith("https://"):
                    with urllib.request.urlopen(caminho_imagem) as u:
                        raw_data = u.read()
                    im = Image.open(BytesIO(raw_data))
                else:
                    im = Image.open(caminho_imagem)

                im = im.resize((80, 112))
                photo = ImageTk.PhotoImage(im)
                lbl_img = tk.Label(frame_img, image=photo, bg="white")
                lbl_img.image = photo
            except Exception as e:
                registrar_erro(f"[Erro imagem] {e}")
                lbl_img = tk.Label(frame_img, text="Erro img", bg="white")

            lbl_img.pack()

            for w in [frame_img, lbl_img]:
                w.bind("<Button-1>", lambda evt, id=id_produto: abrir_edicao(evt, id))
            widgets_linha.append(lbl_img)

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
                produto["data_compra"],
                produto["origem"],
                produto["data_scraping"]
            ]

            for col, valor in enumerate(dados, start=1):
                lbl = tk.Label(scrollable_frame, text=valor, borderwidth=1, relief="solid", bg="white", padx=5, pady=3)
                lbl.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
                lbl.bind("<Button-1>", lambda e, id=id_produto: abrir_edicao(e, id))
                widgets_linha.append(lbl)

            def on_enter(event, widgets=widgets_linha):
                for w in widgets:
                    w.configure(bg="#e0e0e0")

            def on_leave(event, widgets=widgets_linha):
                for w in widgets:
                    w.configure(bg="white")

            for widget in widgets_linha:
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)

    def on_busca_keyrelease(event):
        nonlocal busca_timeout
        if busca_timeout:
            root.after_cancel(busca_timeout)
        busca_timeout = root.after(300, lambda: carregar_produtos(entrada_busca.get()))

    def iniciar_carregamento():
        entrada_busca.bind("<KeyRelease>", on_busca_keyrelease)
        carregar_produtos()

    from Components.thread_com_modal import executar_em_thread
    executar_em_thread(root, iniciar_carregamento, titulo="Listando Produtos", mensagem="Carregando produtos do banco...")

if __name__ == "__main__":
    app = tk.Tk()
    app.withdraw()
    abrir_tela_listagem_produtos(app)
    app.mainloop()