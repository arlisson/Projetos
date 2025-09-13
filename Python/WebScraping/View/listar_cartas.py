import tkinter as tk
from Components.sumario import criar_summary_frame as sumario
from Components.thread_com_modal import executar_em_thread
from Components.listagem_treeview import ListagemTreeview
from DAO.database import (
    buscar_todas_cartas,
    buscar_carta_por_texto,
    calcula_quantidade,
    calcular_lucro_total_cartas_em_posse,
    calcular_total_gasto_cartas,
    calcular_total_vendido_cartas,
    calcular_lucro_total_cartas_vendidas,
)


def abrir_tela_listagem(app):
    from View.editar_cartas import criar_tela_editar_carta

    # ---- Funções específicas da tela ----
    def fetch_cartas(filtro=""):
        return buscar_carta_por_texto(filtro) if filtro else buscar_todas_cartas()

    def row_formatter(carta):
        preco_pago = carta["preco_da_compra"]
        preco_atual = carta["preco_atual"]
        quantidade = carta["quantidade"]
        total_pago = preco_pago * quantidade
        total_atual = preco_atual * quantidade
        lucro_unit = preco_atual - preco_pago
        lucro_total = lucro_unit * quantidade

        valores = [
            carta["nome"],
            carta["codigo"],
            f"R$ {preco_pago:.2f}",
            f"R$ {preco_atual:.2f}",
            f"R$ {total_pago:.2f}",
            f"R$ {total_atual:.2f}",
            f"R$ {lucro_unit:.2f}",
            f"R$ {lucro_total:.2f}",
            carta["data_da_compra"],
            str(quantidade),
            carta["data_scraping"],
        ]
        return valores, carta["id_carta"], carta.get("raridade_nome", "")

    def on_edit(id_carta):
        root.destroy()
        app.after(50, lambda: criar_tela_editar_carta(app, id_carta))

    headers = [
        "Nome", "Código", "Preço Pago", "Preço Atual",
        "Total Pago", "Total Atual", "Lucro Unit.",
        "Lucro Total", "Data Compra", "Quantidade", "Data Scraping"
    ]

    # ---- Janela ----
    root = tk.Toplevel(app)
    root.title("Listagem de Cartas")
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
    lucro_posse = calcular_lucro_total_cartas_em_posse()
    lucro_venda = calcular_lucro_total_cartas_vendidas()
    total_gasto = calcular_total_gasto_cartas()
    total_vendido = calcular_total_vendido_cartas()
    total_cartas_quantidade = calcula_quantidade("carta")
    total_cartas_unidade = len(buscar_todas_cartas()) or 0

    dados_resumo = [
        {"emoji": "💰", "texto": "Lucro em posse", "valor": lucro_posse, "row": 0, "column": 0, "anchor": "w"},
        {"emoji": "💸", "texto": "Lucro com vendas", "valor": lucro_venda, "row": 0, "column": 1, "anchor": "e"},
        {"emoji": "📉", "texto": "Total gasto", "valor": total_gasto, "row": 1, "column": 0, "anchor": "w"},
        {"emoji": "💵", "texto": "Total vendido", "valor": total_vendido, "row": 1, "column": 1, "anchor": "e"},
        {"emoji": "📦", "texto": "Total Cartas Unidade", "valor": str(total_cartas_unidade), "row": 2, "column": 0, "anchor": "w"},
        {"emoji": "📦", "texto": "Total Cartas Quantidade", "valor": str(total_cartas_quantidade), "row": 2, "column": 1, "anchor": "e"},
    ]

    frame_resumo = sumario(root, "Resumo Financeiro", dados_resumo)
    frame_resumo.grid(row=0, column=0, sticky="ew")

    # ---- Listagem ----
    listagem = ListagemTreeview(
        root,
        headers=headers,
        fetch_func=fetch_cartas,
        on_edit=on_edit,
        row_formatter=row_formatter
    )
    listagem.grid(row=2, column=0, sticky="nsew")

    # Carregar dados iniciais em thread
    executar_em_thread(
        root,
        lambda: listagem.carregar(),
        titulo="Listando Cartas",
        mensagem="Carregando cartas do banco..."
    )

    return root


if __name__ == "__main__":
    app = tk.Tk()
    app.withdraw()
    abrir_tela_listagem(app)
    app.mainloop()
