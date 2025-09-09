import tkinter as tk
from tkinter import ttk, messagebox

from DAO.database import (
    buscar_raridade_qualidade_nome,
    buscar_valores_tabela,
    inserir_raridade_qualidade,
    atualizar_raridade_qualidade,
    deletar
)


def abrir_tela_gerenciar_raridade_qualidade(tabela="raridade"):
    """
    Cria uma tela para cadastrar, editar e excluir raridades ou qualidades.
    Parâmetros:
        tabela (str): "raridade" ou "qualidade"
    """
    root = tk.Toplevel()
    root.title(f"Gerenciar {tabela.capitalize()}")
    root.resizable(False, False)
    largura, altura = 400, 300
    x = (root.winfo_screenwidth() // 2) - (largura // 2)
    y = (root.winfo_screenheight() // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{x}+{y}")
    root.grab_set()
    root.focus_force()

    frame = ttk.LabelFrame(root, text=f"Nova {tabela.capitalize()}", padding=15)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    ttk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="w")
    entrada_nome = ttk.Entry(frame, width=35)
    entrada_nome.grid(row=0, column=1, pady=5, padx=5)

    lista_existentes = tk.Listbox(frame, height=8)
    lista_existentes.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=(10, 5))

    ttk.Label(frame, text=f"{tabela.capitalize()}s já cadastradas:").grid(
        row=1, column=0, columnspan=2, sticky="n", pady=(0, 0)
    )

    def atualizar_lista():
        lista_existentes.delete(0, tk.END)
        for _, nome in buscar_valores_tabela(tabela):
            lista_existentes.insert(tk.END, nome)

    def salvar():
        nome = entrada_nome.get().strip()
        if not nome:
            messagebox.showwarning("Atenção", "Digite um nome válido.")
            return

        nome_existente = buscar_raridade_qualidade_nome(nome, tabela)
        if nome_existente:
            messagebox.showerror("Erro", f"{tabela.capitalize()} já cadastrada!")
            return

        novo_id = inserir_raridade_qualidade(nome, tabela)
        if novo_id:
            messagebox.showinfo("Sucesso", f"{tabela.capitalize()} cadastrada com sucesso!")
            entrada_nome.delete(0, tk.END)
            atualizar_lista()
        else:
            messagebox.showerror("Erro", f"Erro ao cadastrar {tabela}.")

    def abrir_edicao(nome):
        edicao = tk.Toplevel(root)
        edicao.title(f"Editar {tabela}")
        edicao.geometry("350x160")

        largura, altura = 350, 160
        x = (root.winfo_screenwidth() // 2) - (largura // 2)
        y = (root.winfo_screenheight() // 2) - (altura // 2)
        edicao.geometry(f"{largura}x{altura}+{x}+{y}")

        edicao.transient(root)      # <- Garante que a janela é filha da principal
        edicao.grab_set()           # <- Bloqueia interação com a janela principal
        edicao.focus_force()

        edicao.resizable(False, False)
       

        id_item = buscar_raridade_qualidade_nome(nome, tabela)

        ttk.Label(edicao, text=f"Editar {tabela.capitalize()}:", font=("Segoe UI", 10)).pack(pady=(15, 5))
        entrada_edit = ttk.Entry(edicao, width=35)
        entrada_edit.pack(pady=5)
        entrada_edit.insert(0, nome)

        def salvar_edicao():
            novo_nome = entrada_edit.get().strip()
            if not novo_nome:
                messagebox.showwarning("Atenção", "Digite um nome válido.")
                return

            existente = buscar_raridade_qualidade_nome(novo_nome, tabela)
            if existente and existente != id_item:
                messagebox.showerror("Erro", f"{tabela.capitalize()} já existe com esse nome.")
                return

            sucesso = atualizar_raridade_qualidade(id_item, novo_nome, tabela)
            if sucesso:
                messagebox.showinfo("Sucesso", f"{tabela.capitalize()} atualizada!")
                edicao.destroy()
                atualizar_lista()
            else:
                messagebox.showerror("Erro", f"Erro ao atualizar {tabela}.")

        def excluir_item():
            resposta = messagebox.askyesno("Confirmar", f"Deseja excluir esta {tabela}?")
            if resposta:
                sucesso = deletar(id_item, tabela, tipo=tabela)
                if sucesso:
                    messagebox.showinfo("Removido", f"{tabela.capitalize()} excluída.")
                    edicao.destroy()
                    atualizar_lista()
                else:
                    messagebox.showerror("Erro", f"Erro ao excluir {tabela}.")

        botoes = ttk.Frame(edicao)
        botoes.pack(pady=10)
        ttk.Button(botoes, text="Salvar", command=salvar_edicao).grid(row=0, column=0, padx=5)
        ttk.Button(botoes, text="Excluir", command=excluir_item).grid(row=0, column=1, padx=5)

        root.wait_window(edicao)

    def on_duplo_clique(evento):
        selecionado = lista_existentes.curselection()
        if selecionado:
            nome = lista_existentes.get(selecionado[0])
            
            abrir_edicao(nome)

    lista_existentes.bind("<Double-Button-1>", on_duplo_clique)

    ttk.Button(frame, text="Salvar", command=salvar).grid(row=2, column=0, columnspan=2, pady=10)
    atualizar_lista()
   
