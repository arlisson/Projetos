import tkinter as tk
from tkinter import ttk, messagebox

from View.cadastrar_cartas import criar_tela_cadastro
from View.cadastrar_cartas_colecao import criar_tela_cadastro_colecao
from View.cadastrar_colecao import abrir_tela_gerenciar_colecoes
from View.cadastrar_raridade_qualidade import abrir_tela_gerenciar_raridade_qualidade
from View.exportar import exportar_banco_completo
from View.listar_cartas import abrir_tela_listagem
from View.cadastrar_produtos import criar_tela_cadastro_produto
from View.listar_produtos import abrir_tela_listagem_produtos
from View.listar_venda_cartas import abrir_tela_listagem_venda
from View.listar_venda_produtos import abrir_tela_listagem_venda_produtos
import hashlib

from DAO.database import (
    apagar_todos_os_dados,
    criar_banco_inicial,
    buscar_historico_precos,
)

# novos imports
from Components.carrossel import CarrosselLateral, carregar_itens_do_banco
from Components.grafico_historico import GraficoHistorico


def criar_tela_principal():
    root = tk.Tk()
    root.title("Gerenciador de Coleção")
    root.geometry("1000x700")
    root.resizable(True, True)

    # Centralizar
    largura, altura = 1000, 700
    x = (root.winfo_screenwidth() // 2) - (largura // 2)
    y = (root.winfo_screenheight() // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{x}+{y}")


    itens = carregar_itens_do_banco()
    

    # --- Funções de atualização dinâmica ---
    def gerar_hash_dados(itens):
        string_dados = "".join(f"{item['nome']}{item['preco']}" for item in itens)
        return hashlib.md5(string_dados.encode()).hexdigest()

    def atualizar_tela():
        nonlocal hash_atual, carrossel, grafico

        novos_itens = carregar_itens_do_banco()
        novo_hash = gerar_hash_dados(novos_itens)

        if novo_hash != hash_atual:
            # Atualizou! → refaz os widgets
            for widget in frame_inicial.winfo_children():
                widget.destroy()

            carrossel = CarrosselLateral(frame_inicial, novos_itens, imagens_visiveis=10, intervalo=3000)
            carrossel.pack(pady=10)

            dados_lucro = buscar_historico_precos(tipo="lucro")
            dados_formatados = [
                {"data": row["data"], "lucro_total": row["lucro_total"]}
                for row in dados_lucro
            ] if dados_lucro else []

            grafico = GraficoHistorico(
                frame_inicial,
                dados=dados_formatados,
                titulo="Histórico de Lucros Totais",
                campos_numericos=("lucro_total",),
                campo_data="data",
            )
            grafico.pack(fill="both", expand=True, pady=20)

            hash_atual = novo_hash

        root.after(5000, atualizar_tela)  # Verifica novamente após 5s

    hash_atual = gerar_hash_dados(itens)

    # ===== Menu bar =====
    menu_bar = tk.Menu(root)

    # --- Cartas ---
    menu_cartas = tk.Menu(menu_bar, tearoff=0)
    menu_cartas.add_command(label="Cadastrar Carta", command=lambda: criar_tela_cadastro(root))
    menu_cartas.add_command(label="Listar Cartas", command=lambda: abrir_tela_listagem(root))
    menu_cartas.add_command(label="Cadastrar Coleção", command=lambda: criar_tela_cadastro_colecao(root))
    menu_bar.add_cascade(label="Cartas", menu=menu_cartas)

    # --- Produtos ---
    menu_produtos = tk.Menu(menu_bar, tearoff=0)
    menu_produtos.add_command(label="Cadastrar Produto", command=lambda: criar_tela_cadastro_produto(root))
    menu_produtos.add_command(label="Listar Produtos", command=lambda: abrir_tela_listagem_produtos(root))
    menu_bar.add_cascade(label="Produtos", menu=menu_produtos)

    # --- Vendas ---
    menu_vendas = tk.Menu(menu_bar, tearoff=0)
    menu_vendas.add_command(label="Listar Vendas de Cartas", command=lambda: abrir_tela_listagem_venda(root))
    menu_vendas.add_command(label="Listar Vendas de Produtos", command=lambda: abrir_tela_listagem_venda_produtos(root))
    menu_bar.add_cascade(label="Vendas", menu=menu_vendas)

    # --- Outras Gestões ---
    menu_outros = tk.Menu(menu_bar, tearoff=0)
    menu_outros.add_command(label="Gerenciar Coleções", command=abrir_tela_gerenciar_colecoes)
    menu_outros.add_command(label="Gerenciar Raridades", command=lambda: abrir_tela_gerenciar_raridade_qualidade("raridade"))
    menu_outros.add_command(label="Gerenciar Qualidades", command=lambda: abrir_tela_gerenciar_raridade_qualidade("qualidade"))
    menu_bar.add_cascade(label="Outras Gestões", menu=menu_outros)

    # --- Opções ---
    def confirmar_e_apagar():
        resp = messagebox.askyesno("Confirmar", "Tem certeza que deseja apagar todos os dados?\nEssa ação não pode ser desfeita.")
        if resp:
            apagar_todos_os_dados()

    def confirmar_e_criar():
        resp = messagebox.askyesno("Confirmar", "Deseja carregar os dados padrão de raridade e qualidade?")
        if resp:
            criar_banco_inicial()

    menu_opcoes = tk.Menu(menu_bar, tearoff=0)
    menu_opcoes.add_command(label="Apagar todos os dados", command=confirmar_e_apagar)
    menu_opcoes.add_command(label="Criar banco", command=confirmar_e_criar)
    menu_opcoes.add_command(label="Exportar banco de dados", command=exportar_banco_completo)
    menu_bar.add_cascade(label="Opções", menu=menu_opcoes)

    # --- Sair ---
    menu_bar.add_command(label="Sair", command=root.quit)

    root.config(menu=menu_bar)

    # ===== Tela inicial =====
    frame_inicial = ttk.Frame(root, padding=10)
    frame_inicial.pack(fill="both", expand=True)

    # --- Carrossel ---
    itens = carregar_itens_do_banco()
    carrossel = CarrosselLateral(frame_inicial, itens, imagens_visiveis=10, intervalo=3000)
    carrossel.pack(pady=10)

    # --- Gráfico de lucros ---
    dados_lucro = buscar_historico_precos(tipo="lucro")
    dados_formatados = [
        {"data": row["data"], "lucro_total": row["lucro_total"]}
        for row in dados_lucro
    ] if dados_lucro else []

    grafico = GraficoHistorico(
        frame_inicial,
        dados=dados_formatados,
        titulo="Histórico de Lucros Totais",
        campos_numericos=("lucro_total",),
        campo_data="data",
    )
    grafico.pack(fill="both", expand=True, pady=20)

     # Inicia loop de verificação
    root.after(10000, atualizar_tela)
    root.mainloop()
   


if __name__ == "__main__":
    criar_tela_principal()
