import tkinter as tk
from Components.sumario import criar_summary_frame as sumario
from Components.thread_com_modal import executar_em_thread
from Components.listagem_treeview import ListagemTreeview
from DAO.database import (
    calcula_quantidade,
    listar_todos_produtos,
    calcular_lucro_total_produtos_em_posse,
    calcular_lucro_total_produtos_vendidos,
    calcular_total_gasto_produtos,
    calcular_total_vendido_produtos,
)


def abrir_tela_editar_produto(app, id_produto):
    from View.editar_produto import criar_tela_editar_produto
    app.after(50, lambda: criar_tela_editar_produto(app, id_produto))


def abrir_tela_listagem_produtos(app):
    # ---- Funções específicas da tela ----
    def fetch_produtos(filtro=""):
        return listar_todos_produtos(filtro)

    def row_formatter(produto):
        preco_compra = produto['preco_compra'] or 0.0
        preco_atual = produto['preco_atual'] or 0.0
        qtd_raw = produto.get('quantidade')
        quantidade = int(qtd_raw) if (qtd_raw is not None and str(qtd_raw) != "") else 0
        total_pago = preco_compra * quantidade
        total_atual = preco_atual * quantidade
        lucro_unit = preco_atual - preco_compra
        lucro_total = lucro_unit * quantidade

        valores = [
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
        return valores, produto["id_produto"]

    def on_edit(id_produto):
        try:
            root.grab_release()  # libera o grab antes
        except Exception:
            pass
        root.destroy()
        abrir_tela_editar_produto(app, id_produto)


    headers = [
        "Nome", "Preço Compra", "Preço Atual",
        "Total Pago", "Total Atual", "Lucro Unit.", "Lucro Total",
        "Quantidade", "Data da compra", "Origem", "Data Scraping"
    ]

    # ---- Janela ----
    root = tk.Toplevel(app)
    root.title("Listagem de Produtos")
    root.grab_set()
    root.focus_force()

    largura, altura = 1200, 600
    x = (root.winfo_screenwidth() // 2) - (largura // 2)
    y = (root.winfo_screenheight() // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{x}+{y}")
    root.resizable(True, True)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(2, weight=1)

    # ---- Resumo financeiro ----
    lucro_posse = calcular_lucro_total_produtos_em_posse()
    lucro_venda = calcular_lucro_total_produtos_vendidos()
    total_gasto = calcular_total_gasto_produtos()
    total_vendido = calcular_total_vendido_produtos()
    total_quantidade = calcula_quantidade("produto")
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
    frame_resumo.grid(row=0, column=0, sticky="ew")

    # ---- Listagem ----
    listagem = ListagemTreeview(
        root,
        headers=headers,
        fetch_func=fetch_produtos,
        on_edit=on_edit,
        row_formatter=row_formatter
    )
    listagem.grid(row=2, column=0, sticky="nsew")

    # Carregar dados iniciais em thread
    executar_em_thread(
        root,
        lambda: listagem.carregar(),
        titulo="Listando Produtos",
        mensagem="Carregando produtos do banco..."
    )

    return root


if __name__ == "__main__":
    app = tk.Tk()
    app.withdraw()
    abrir_tela_listagem_produtos(app)
    app.mainloop()
