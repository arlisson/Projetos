import tkinter as tk
from tkinter import ttk

from DAO.database import (
    calcular_quantidade_vendida,
    listar_venda_filtro,
    calcular_lucro_total_produtos_em_posse,
    calcular_lucro_total_produtos_vendidos,
    calcular_total_gasto_produtos,
    calcular_total_vendido_produtos,
)

from View.editar_venda_produto import criar_tela_editar_venda_produto
from Components.sumario import criar_summary_frame as sumario
from Components.listagem_treeview import ListagemTreeview
from Components.thread_com_modal import executar_em_thread


def abrir_tela_listagem_venda_produtos(app):
    root = tk.Toplevel(app)
    root.title("Listagem de Produtos Vendidos")
    root.grab_set()
    root.focus_force()

    largura, altura = 1200, 600
    x = (root.winfo_screenwidth() // 2) - (largura // 2)
    y = (root.winfo_screenheight() // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{x}+{y}")
    root.resizable(True, True)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    # --- Resumo financeiro ---
    lucro_posse = calcular_lucro_total_produtos_em_posse()
    lucro_venda = calcular_lucro_total_produtos_vendidos()
    total_gasto = calcular_total_gasto_produtos()
    total_vendido = calcular_total_vendido_produtos()
    total_produtos_vendidos_unidade = len(listar_venda_filtro("produto")) or 0
    total_produtos_vendidos_quantidade = calcular_quantidade_vendida("venda_produto")

    dados_resumo = [
        {"emoji": "💰", "texto": "Lucro em posse", "valor": lucro_posse, "row": 0, "column": 0, "anchor": "w"},
        {"emoji": "💸", "texto": "Lucro com vendas", "valor": lucro_venda, "row": 0, "column": 1, "anchor": "e"},
        {"emoji": "📉", "texto": "Total gasto", "valor": total_gasto, "row": 1, "column": 0, "anchor": "w"},
        {"emoji": "💵", "texto": "Total vendido", "valor": total_vendido, "row": 1, "column": 1, "anchor": "e"},
        {"emoji": "📦", "texto": "Total Vendas Unidade", "valor": str(total_produtos_vendidos_unidade), "row": 2, "column": 0, "anchor": "w"},
        {"emoji": "📦", "texto": "Total Vendas Quantidade", "valor": str(total_produtos_vendidos_quantidade), "row": 2, "column": 1, "anchor": "e"},
    ]

    frame_resumo = sumario(root, "Resumo Financeiro", dados_resumo)
    frame_resumo.grid(row=0, column=0, sticky="ew")

    # --- Cabeçalhos da listagem ---
    headers = [
        "Nome", "Preço Compra", "Preço Atual",
        "Total Pago", "Total Atual", "Lucro Unit.", "Lucro Total",
        "Quantidade", "Data da compra", "Origem",
        "Preço da venda", "Data da Venda", "Data Scraping"
    ]

    # --- Função que busca no banco ---
    def fetch_func(filtro=""):
        return listar_venda_filtro(tipo="produto", filtro=filtro)

    # --- Formata cada linha ---
    def row_formatter(produto):
        preco_compra = produto["preco_compra"] or 0.0
        preco_atual = produto["preco_atual"] or 0.0
        quantidade = produto.get("quantidade", 1) or 1
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
            f"R$ {produto['preco_venda']:.2f}",
            produto["data_venda"],
            produto["data_scraping"],
        ]
        iid = produto["id_produto"]
        return valores, iid  # não tem raridade

    # --- Ação ao clicar ---
    def on_edit(id_produto):
        root.destroy()
        criar_tela_editar_venda_produto(app, id_produto)

    # --- Componente de listagem ---
    listagem = ListagemTreeview(
        root,
        headers=headers,
        fetch_func=fetch_func,
        on_edit=on_edit,
        row_formatter=row_formatter,
    )
    listagem.grid(row=1, column=0, sticky="nsew")

    executar_em_thread(
        root,
        lambda: listagem.carregar(),
        titulo="Listando Vendas de Produtos",
        mensagem="Carregando vendas do banco..."
    )

    return root


if __name__ == "__main__":
    app = tk.Tk()
    app.withdraw()
    abrir_tela_listagem_venda_produtos(app)
    app.mainloop()
