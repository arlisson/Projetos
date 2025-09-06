from logging import root
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import urllib.request
from io import BytesIO
from datetime import datetime

from numpy import vander
from Components.pop_up_venda import abrir_popup_venda
from Components.thread_com_modal import executar_em_thread
from scraping.scraping_cartas import buscar_produto_liga
from DAO.database import atualizar_produto, buscar_produto_por_id, deletar, inserir_venda_generica
from tkcalendar import Calendar
from decimal import Decimal
import threading

IMAGEM_PADRAO = "https://i.pinimg.com/736x/71/1e/da/711eda25308c65a7756751088866e181.jpg"

def criar_tela_editar_produto(app, id_produto):
    from View.listar_produtos import abrir_tela_listagem_produtos

    root = tk.Toplevel(app)

    def ao_fechar():
        root.destroy()
        abrir_tela_listagem_produtos(app)
        
    root.protocol("WM_DELETE_WINDOW", ao_fechar)

    root.grab_set()
    root.focus_force()

    produto = buscar_produto_por_id(id_produto)
    if not produto:
        messagebox.showerror("Erro", "Produto não encontrado.")
        ao_fechar()
        return

    root.title("Editar Produto")
    root.resizable(True, True)
    largura, altura = 960, 640
    x = (root.winfo_screenwidth() // 2) - (largura // 2)
    y = (root.winfo_screenheight() // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{x}+{y}")

    main_frame = ttk.Frame(root, padding=10)
    main_frame.pack(fill="both", expand=True)
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=0)
    main_frame.rowconfigure(0, weight=1)
    main_frame.rowconfigure(1, weight=0)

    try:
        calendar_img = Image.open("imagens/calendario.png").resize((20, 20))
        CALENDAR_ICON = ImageTk.PhotoImage(calendar_img)
        icon_ok = True
    except:
        CALENDAR_ICON = None
        icon_ok = False

    campos = {}

    def abrir_calendario():
        top = tk.Toplevel(root)
        top.title("Selecionar Data")
        top.grab_set()
        top.resizable(False, False)
        top.geometry(f"+{root.winfo_rootx() + 200}+{root.winfo_rooty() + 150}")
        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(padx=10, pady=10)

        def selecionar_data():
            campos["data_compra"].delete(0, tk.END)
            campos["data_compra"].insert(0, cal.get_date())
            top.destroy()

        ttk.Button(top, text="Selecionar", command=selecionar_data).pack(pady=5)

    def criar_entrada(frame, label, row):
        ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", padx=5, pady=3)
        entry = ttk.Entry(frame)
        entry.grid(row=row, column=1, sticky="ew", padx=5, pady=3)
        return entry

    form_frame = ttk.LabelFrame(main_frame, text="Dados do Produto", padding=10)
    form_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    form_frame.columnconfigure(1, weight=1)

    campos["link"] = criar_entrada(form_frame, "Link:", 0)
    campos["nome"] = criar_entrada(form_frame, "Nome:", 1)
    campos["imagem"] = criar_entrada(form_frame, "URL da Imagem:", 2)
    campos["preco_compra"] = criar_entrada(form_frame, "Preço Compra:", 3)
    campos["preco_atual"] = criar_entrada(form_frame, "Preço Atual:", 4)

    ttk.Label(form_frame, text="Data da Compra:").grid(row=5, column=0, sticky="w", padx=5, pady=3)
    data_frame = ttk.Frame(form_frame)
    data_frame.grid(row=5, column=1, padx=5, pady=3, sticky="ew")
    data_frame.columnconfigure(0, weight=1)

    campos["data_compra"] = ttk.Entry(data_frame)
    campos["data_compra"].grid(row=0, column=0, sticky="ew", padx=(0, 5))

    btn = ttk.Button(data_frame, image=CALENDAR_ICON if icon_ok else None,
                     text="🗕" if not icon_ok else "", command=abrir_calendario)
    btn.grid(row=0, column=1)

    campos["quantidade"] = criar_entrada(form_frame, "Quantidade:", 6)
    campos["origem"] = criar_entrada(form_frame, "Origem:", 7)

    imagem_frame = ttk.LabelFrame(main_frame, text="Imagem", padding=10, width=320)
    imagem_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ns")
    imagem_label = ttk.Label(imagem_frame)
    imagem_label.pack()

    def atualizar_imagem(url):
        def _baixar():
            try:
                with urllib.request.urlopen(url) as u:
                    raw_data = u.read()
                im = Image.open(BytesIO(raw_data))
                im.thumbnail((300, 420))
                photo = ImageTk.PhotoImage(im)
                root.after(0, lambda: (imagem_label.configure(image=photo), setattr(imagem_label, 'image', photo)))
            except:
                root.after(0, lambda: (imagem_label.configure(image=''), setattr(imagem_label, 'image', None)))
        threading.Thread(target=_baixar, daemon=True).start()

    def to_decimal(valor):
        try:
            return float(str(valor).replace("R$", "").replace(",", ".").strip())
        except:
            return 0.0

    def buscar_info_scraping():
        def _buscar():
            url = campos["link"].get().strip()
            if not url:
                return root.after(0, lambda: messagebox.showwarning("Aviso", "Informe o link do produto.", parent=root))

            try:
                dados = buscar_produto_liga(url)
                if not dados:
                    return root.after(0, lambda: messagebox.showwarning("Aviso", "Nenhum dado retornado do scraping.", parent=root))

                def preencher():
                    campos["nome"].delete(0, tk.END)
                    campos["nome"].insert(0, dados.get("nome", ""))

                    campos["imagem"].delete(0, tk.END)
                    campos["imagem"].insert(0, dados.get("imagem", ""))

                    preco = dados.get("preco_atual", "").replace("R$", "").replace(",", ".").strip()
                    campos["preco_atual"].delete(0, tk.END)
                    campos["preco_atual"].insert(0, preco)

                    campos["data_compra"].delete(0, tk.END)
                    campos["data_compra"].insert(0, datetime.today().strftime("%Y-%m-%d"))

                    atualizar_imagem(campos["imagem"].get())

                root.after(0, preencher)

            except Exception as e:
                root.after(0, lambda: messagebox.showerror("Erro", f"Erro no scraping: {e}", parent=root))

        executar_em_thread(
            root,
            _buscar,
            titulo="Buscando Produto",
            mensagem="Coletando informações do produto via scraping..."
        )


    def salvar():
        try:
            produto = {
                "id_produto": id_produto,
                "nome_produto": campos["nome"].get(),
                "link": campos["link"].get(),
                "imagem": campos["imagem"].get() or IMAGEM_PADRAO,
                "preco_compra": to_decimal(campos["preco_compra"].get()),
                "preco_atual": to_decimal(campos["preco_atual"].get()),
                "data_compra": campos["data_compra"].get(),
                "quantidade": int(campos["quantidade"].get()),
                "origem": campos["origem"].get() or "Liga Yugioh",
                "data_scraping": datetime.today().strftime("%Y-%m-%d")
            }

            def _salvar():
                try:
                    atualizar_produto(produto)
                    root.after(0, lambda: (
                        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!", parent=root),
                        ao_fechar()
                    ))
                except Exception as e:
                    root.after(0, lambda: messagebox.showerror("Erro", f"Erro ao salvar: {e}", parent=root))

            executar_em_thread(
                root,
                _salvar,
                titulo="Salvando Produto",
                mensagem="Atualizando dados no banco de dados..."
            )

        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {e}", parent=root)


    def apagar_produto():
        if messagebox.askokcancel("Confirmar", "Tem certeza que deseja deletar este produto?", parent=root):
            if deletar(id=id_produto, tabela="produto"):
                messagebox.showinfo("Sucesso", f"Produto: {campos['nome'].get()} deletado com sucesso!", parent=root)
                ao_fechar()
            else:
                messagebox.showerror("Erro", f"Erro ao deletar o produto: {campos['nome'].get()}.", parent=root)

    def vender():
        """
        Abre o popup de venda, valida quantidade/preço, registra a venda via DAO
        e ajusta a quantidade disponível na UI (e no banco, via DAO).
        """
        def ao_confirmar(preco_venda, quantidade_vendida):
            try:
                # conversões básicas
                preco_venda = float(preco_venda)
                quantidade_vendida = int(quantidade_vendida)
                quantidade_disponivel = int(campos["quantidade"].get() or 0)

                if quantidade_vendida <= 0:
                    raise ValueError("Informe uma quantidade maior que zero.")
                if preco_venda < 0:
                    raise ValueError("Informe um preço de venda válido (>= 0).")
                if quantidade_vendida > quantidade_disponivel:
                    raise ValueError("Quantidade vendida excede a disponível.")

                # monta um payload só para eventual logging/uso futuro
                dados_venda = {
                    "id_item": id_produto,
                    "tipo": "produto",
                    "nome": campos["nome"].get(),
                    "link": campos["link"].get(),
                    "imagem": campos["imagem"].get() or IMAGEM_PADRAO,
                    "preco_compra": to_decimal(campos["preco_compra"].get()),
                    "preco_atual": to_decimal(campos["preco_atual"].get()),
                    "data_compra": campos["data_compra"].get(),
                    "quantidade_vendida": quantidade_vendida,
                    "data_da_venda": datetime.today().strftime("%Y-%m-%d"),
                    "preco_da_venda": preco_venda,
                    "origem": campos["origem"].get() or "Liga Yugioh",
                }

                # registra a venda genérica (o DAO deve decrementar o estoque do item)
                inserir_venda_generica(
                    id_item=id_produto,
                    quantidade_vendida=quantidade_vendida,
                    preco_venda=preco_venda,
                    tipo="produto"
                )

                # atualiza a quantidade visível
                nova_qtd = quantidade_disponivel - quantidade_vendida
                campos["quantidade"].delete(0, tk.END)
                campos["quantidade"].insert(0, str(nova_qtd))

                messagebox.showinfo("Sucesso", "Venda registrada com sucesso!", parent=root)
                ao_fechar()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao registrar venda: {e}", parent=root)

        # abre o popup usando o mesmo componente já usado em cartas
        nome_item = campos["nome"].get() or "Produto"
        try:
            quantidade_disponivel = int(campos["quantidade"].get() or 0)
        except:
            quantidade_disponivel = 0

        abrir_popup_venda(root, nome_item, quantidade_disponivel, ao_confirmar)


    # Criar frame dos botões corretamente
    botoes_frame = ttk.Frame(main_frame)
    botoes_frame.grid(row=1, column=0, columnspan=2, pady=10)

    # Botões dentro do frame
    ttk.Button(botoes_frame, text="Buscar via Scraping", command=buscar_info_scraping).pack(side="left", padx=20, pady=5)
    ttk.Button(botoes_frame, text="Salvar Produto", command=salvar).pack(side="left", padx=20, pady=5)
    ttk.Button(botoes_frame, text="Deletar Produto", command=apagar_produto).pack(side="left", padx=20, pady=5)
    ttk.Button(botoes_frame, text="Vender Produto", command=vender).pack(side="left", padx=20, pady=5)  # <-- novo

    # Preencher campos com os dados do produto existente
    campos["link"].insert(0, produto["link"] or "")
    campos["nome"].insert(0, produto["nome_produto"] or "")
    campos["imagem"].insert(0, produto["imagem"] or IMAGEM_PADRAO)
    campos["preco_compra"].insert(0, str(produto["preco_compra"] or ""))
    campos["preco_atual"].insert(0, str(produto["preco_atual"] or ""))
    campos["data_compra"].insert(0, produto["data_compra"] or "")
    campos["quantidade"].insert(0, str(produto["quantidade"] or "1"))
    campos["origem"].insert(0, produto["origem"] or "Liga Yugioh")

    atualizar_imagem(produto["imagem"] or IMAGEM_PADRAO)

    root.mainloop()


if __name__ == "__main__":
    app = tk.Tk()
    app.withdraw()
    criar_tela_editar_produto(app)
    app.mainloop()
