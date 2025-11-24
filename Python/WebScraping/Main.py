import threading
import tkinter as tk
from tkinter import ttk, messagebox
import hashlib

from Components.sumario import criar_summary_frame as sumario
from Components.modal_progresso import ModalProgresso
from Utils.atualizador import iniciar_atualizacao_diaria
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
from View.logs import abrir_tela_logs
from Components.thread_com_modal import executar_em_thread

import os, sys
from pathlib import Path

from DAO.database import (
    apagar_todos_os_dados,
    calcula_total_gasto,
    criar_banco_inicial,
    buscar_historico_precos,
)

from Components.grafico_historico import GraficoHistorico
from Components.scrollable_frame import ScrollableFrame

def _config_playwright_browsers_path():
    if getattr(sys, "frozen", False):  # executável PyInstaller
        exe_dir = Path(sys.executable).parent
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(exe_dir / "playwright-browsers")
    else:
        # em dev, se a pasta existir, usa ela (opcional)
        here = Path(__file__).resolve().parent
        local = here / "playwright-browsers"
        if local.exists():
            os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(local)

_config_playwright_browsers_path()

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
    
    root.columnconfigure(0, weight=1)
    root.rowconfigure(2, weight=1)

    label_status = tk.Label(root, text="", font=("Arial", 10), fg="blue")
    label_status.pack(pady=(5, 0))

    # Atualização diária
    iniciar_atualizacao_diaria(callback_status=lambda msg: label_status.config(text=msg))


    # container para o resumo
    container = ttk.Frame(root)
    container.pack(fill="x", padx=10, pady=10)
    container.columnconfigure(0, weight=1)

    # placeholder para o resumo
    frame_resumo = None




    # ======================== Funções Auxiliares ========================
    def atualizar_tela():
        nonlocal frame_resumo

        # limpa o resumo antigo
        if frame_resumo:
            frame_resumo.destroy()

        # ---- Resumo financeiro ----
        resumo = buscar_historico_precos(resumo=True)
        dados_resumo = [
            {"emoji": "🃏", "texto": "Lucro Cartas", "valor": resumo.get("lucro_cartas", 0.0) + resumo.get("total_vendas_cartas", 0.0), "row": 0, "column": 0, "anchor": "w"},
            {"emoji": "📦", "texto": "Lucro Produtos", "valor": resumo.get("lucro_produtos", 0.0) + resumo.get("total_vendas_produtos", 0.0), "row": 0, "column": 1, "anchor": "e"},
            {"emoji": "💰", "texto": "Lucro Total", "valor": resumo.get("lucro_total", 0.0), "row": 1, "column": 0, "anchor": "w"},
            {"emoji": "💵", "texto": "Vendas Cartas", "valor": resumo.get("total_vendas_cartas", 0.0), "row": 1, "column": 1, "anchor": "e"},
            {"emoji": "📊", "texto": "Vendas Produtos", "valor": resumo.get("total_vendas_produtos", 0.0), "row": 2, "column": 0, "anchor": "w"},
            {"emoji": "📉", "texto": "Total gasto", "valor": calcula_total_gasto(), "row": 2, "column": 1, "anchor": "e"},
        ]
        
        frame_resumo = sumario(container, "Resumo Financeiro", dados_resumo)
        frame_resumo.grid(row=0, column=0, sticky="ew")

        # limpa os gráficos
        for widget in frame_scroll.scrollable_frame.winfo_children():
            widget.destroy()

        # ==== Gráfico geral ====
        dados_lucro = buscar_historico_precos(tipo="lucro")
        dados_formatados = [{"data": row["data"], "lucro_total": row["lucro_total"]}
                            for row in dados_lucro] if dados_lucro else []

        grafico_geral = GraficoHistorico(
            frame_scroll.scrollable_frame,
            dados=dados_formatados,
            titulo="Histórico de Lucros Totais",
            campos_numericos=("lucro_total",),
            campo_data="data",
        )
        grafico_geral.pack(fill="both", expand=True, pady=20)

        # ==== Gráfico cartas ====
        dados_cartas = buscar_historico_precos(tipo="lucro")
        dados_formatados_cartas = [{"data": row["data"], "lucro_total": row["lucro_cartas"]}
                                   for row in dados_cartas] if dados_cartas else []

        grafico_cartas = GraficoHistorico(
            frame_scroll.scrollable_frame,
            dados=dados_formatados_cartas,
            titulo="Histórico de Lucros - Cartas",
            campos_numericos=("lucro_total",),
            campo_data="data",
        )
        grafico_cartas.pack(fill="both", expand=True, pady=20)

        # ==== Gráfico produtos ====
        dados_produtos = buscar_historico_precos(tipo="lucro")
        dados_formatados_produtos = [{"data": row["data"], "lucro_total": row["lucro_produtos"]}
                                     for row in dados_produtos] if dados_produtos else []

        grafico_produtos = GraficoHistorico(
            frame_scroll.scrollable_frame,
            dados=dados_formatados_produtos,
            titulo="Histórico de Lucros - Produtos",
            campos_numericos=("lucro_total",),
            campo_data="data",
        )
        grafico_produtos.pack(fill="both", expand=True, pady=20)

    # ======================== Menu ========================
    menu_bar = tk.Menu(root)

    menu_cartas = tk.Menu(menu_bar, tearoff=0)
    menu_cartas.add_command(label="Cadastrar Carta", command=lambda: criar_tela_cadastro(root))
    menu_cartas.add_command(label="Listar Cartas", command=lambda: abrir_tela_listagem(root))
    menu_cartas.add_command(label="Cadastrar Coleção", command=lambda: criar_tela_cadastro_colecao(root))
    menu_bar.add_cascade(label="Cartas", menu=menu_cartas)

    menu_produtos = tk.Menu(menu_bar, tearoff=0)
    menu_produtos.add_command(label="Cadastrar Produto", command=lambda: criar_tela_cadastro_produto(root))
    menu_produtos.add_command(label="Listar Produtos", command=lambda: abrir_tela_listagem_produtos(root))
    menu_bar.add_cascade(label="Produtos", menu=menu_produtos)

    menu_vendas = tk.Menu(menu_bar, tearoff=0)
    menu_vendas.add_command(label="Listar Vendas de Cartas", command=lambda: abrir_tela_listagem_venda(root))
    menu_vendas.add_command(label="Listar Vendas de Produtos", command=lambda: abrir_tela_listagem_venda_produtos(root))
    menu_bar.add_cascade(label="Vendas", menu=menu_vendas)

    menu_outros = tk.Menu(menu_bar, tearoff=0)
    menu_outros.add_command(label="Gerenciar Coleções", command=abrir_tela_gerenciar_colecoes)
    menu_outros.add_command(label="Gerenciar Raridades", command=lambda: abrir_tela_gerenciar_raridade_qualidade("raridade"))
    menu_outros.add_command(label="Gerenciar Qualidades", command=lambda: abrir_tela_gerenciar_raridade_qualidade("qualidade"))
    menu_bar.add_cascade(label="Outras Gestões", menu=menu_outros)

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

    
    menu_logs = tk.Menu(menu_bar, tearoff=0)
    menu_logs.add_command(label="Ver Logs", command=lambda: abrir_tela_logs(root, "logs/log_info.txt", "logs/log_erros.txt"))
    menu_bar.add_cascade(label="Logs", menu=menu_logs)

    menu_bar.add_command(label="Sair", command=root.quit)
    root.config(menu=menu_bar)

    # ======================== Scrollable Frame Inicial ========================
    frame_scroll = ScrollableFrame(root)
    frame_scroll.pack(fill="both", expand=True)

    # Exibe os gráficos logo na abertura
    atualizar_tela()

    # ======================== Botão de Atualizar ========================
    btn_atualizar = ttk.Button(
        root,
        text="🔄 Atualizar Tela",
        command=lambda: executar_em_thread(
            root,
            atualizar_tela,
            titulo="Carregando",
            mensagem="Atualizando dados..."
        )
    )
    btn_atualizar.pack(pady=(0, 10))

    root.mainloop()


if __name__ == "__main__":
    criar_tela_principal()
