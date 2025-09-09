import tkinter as tk
from tkinter import ttk, messagebox

from DAO.database import (
    buscar_colecao_por_nome,
    buscar_valores_tabela,
    buscar_raridade_qualidade_nome,
    desativar_se_vinculado_ou_deletar,
    inserir_raridade_qualidade,
    atualizar_raridade_qualidade,
    deletar
)

def abrir_tela_gerenciar_colecoes():
    tabela = "colecao"

    root = tk.Toplevel()
    root.title("Gerenciar Coleções")
    root.resizable(False, False)
    largura, altura = 400, 300
    x = (root.winfo_screenwidth() // 2) - (largura // 2)
    y = (root.winfo_screenheight() // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{x}+{y}")
    root.grab_set()
    root.focus_force()

    frame = ttk.LabelFrame(root, text="Nova Coleção", padding=15)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    ttk.Label(frame, text="Nome:").grid(row=0, column=0, sticky="w")
    entrada_nome = ttk.Entry(frame, width=35)
    entrada_nome.grid(row=0, column=1, pady=5, padx=5)

    lista_existentes = tk.Listbox(frame, height=8)
    lista_existentes.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=(5, 5))

    ttk.Label(frame, text="Coleções já cadastradas:").grid(
        row=1, column=0, columnspan=2, sticky="n", pady=(10, 0)
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

        if buscar_raridade_qualidade_nome(nome, tabela):
            messagebox.showerror("Erro", "Coleção já cadastrada!")
            return

        novo_id = inserir_raridade_qualidade(nome, tabela)
        if novo_id:
            messagebox.showinfo("Sucesso", "Coleção cadastrada com sucesso!")
            entrada_nome.delete(0, tk.END)
            atualizar_lista()
        else:
            messagebox.showerror("Erro", "Erro ao cadastrar coleção.")

    def abrir_edicao(nome):
        edicao = tk.Toplevel(root)
        edicao.title("Editar Coleção")
        largura, altura = 350, 160
        x = (root.winfo_screenwidth() // 2) - (largura // 2)
        y = (root.winfo_screenheight() // 2) - (altura // 2)
        edicao.geometry(f"{largura}x{altura}+{x}+{y}")
        edicao.transient(root)
        edicao.grab_set()
        edicao.focus_force()
        edicao.resizable(False, False)

        id_item = buscar_colecao_por_nome(nome)

        ttk.Label(edicao, text="Editar Coleção:", font=("Segoe UI", 10)).pack(pady=(15, 5))
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
                messagebox.showerror("Erro", "Já existe uma coleção com esse nome.")
                return

            sucesso = atualizar_raridade_qualidade(id_item, novo_nome, tabela)
            if sucesso:
                messagebox.showinfo("Sucesso", "Coleção atualizada!")
                edicao.destroy()
                atualizar_lista()
            else:
                messagebox.showerror("Erro", "Erro ao atualizar coleção.")

        def excluir_item():
            resposta = messagebox.askyesno("Confirmar", "Deseja excluir esta coleção?")
            if not resposta:
                return

            resultado = desativar_se_vinculado_ou_deletar(id_item, tabela, tipo=tabela)

            if resultado == "excluido":
                messagebox.showinfo("Removido", "Coleção excluída com sucesso.")
                edicao.destroy()
                atualizar_lista()
            elif resultado == "desativado":
                messagebox.showinfo("Coleção vinculada", "Coleção está em uso e foi marcada como (DESATIVADA).")
                edicao.destroy()
                atualizar_lista()
            else:
                messagebox.showerror("Erro", "Erro ao excluir/desativar a coleção.")

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

    ttk.Button(frame, text="Salvar", command=salvar).grid(row=3, column=0, columnspan=2, pady=10)
    atualizar_lista()
