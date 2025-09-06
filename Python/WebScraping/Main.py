import tkinter as tk
from tkinter import ttk, messagebox
from View.cadastrar_cartas import criar_tela_cadastro
from View.cadastrar_cartas_colecao import criar_tela_cadastro_colecao
from View.listar_cartas import abrir_tela_listagem  
from View.cadastrar_produtos import criar_tela_cadastro_produto
from View.listar_produtos import abrir_tela_listagem_produtos  
from DAO.database import ( 
    
    apagar_todos_os_dados,
    criar_banco_inicial
)
from View.listar_venda_cartas import abrir_tela_listagem_venda

def criar_tela_principal():
    root = tk.Tk()
    root.title("Gerenciador de Coleção")
    root.geometry("800x600")
    root.resizable(True, True)

    # Centralizar
    largura, altura = 800, 600
    x = (root.winfo_screenwidth() // 2) - (largura // 2)
    y = (root.winfo_screenheight() // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{x}+{y}")

    # ===== Menu bar =====
    menu_bar = tk.Menu(root)

    # --- Cartas ---
    menu_cartas = tk.Menu(menu_bar, tearoff=0)
    menu_cartas.add_command(label="Cadastrar Carta", command= lambda: criar_tela_cadastro(root))
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
    # menu_vendas.add_command(label="Listar Vendas de Produtos")
    menu_bar.add_cascade(label="Vendas", menu=menu_vendas)

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
    menu_bar.add_cascade(label="Opções", menu=menu_opcoes)

    # --- Sair ---
    menu_bar.add_command(label="Sair", command=root.quit)

    root.config(menu=menu_bar)

    # Tela de boas-vindas ou conteúdo inicial
    label = ttk.Label(root, text="Bem-vindo ao Gerenciador de Coleção!", font=("Segoe UI", 16))
    label.pack(pady=50)
    
    root.mainloop()

if __name__ == "__main__":
    criar_tela_principal()
