import re
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import urllib.request
from io import BytesIO
from datetime import datetime


from Components.entrada_padrao import criar_entrada_com_botao_imagem, criar_entrada_data_com_calendario, criar_entrada_padrao
from Components.grafico_historico import GraficoHistorico
from Components.pop_up_venda import abrir_popup_venda
from Components.scrollable_frame import ScrollableFrame
from Components.thread_com_modal import executar_em_thread
from Utils.baixar_carta import salvar_imagem_local
from Utils.log import registrar_erro
from scraping.scraping_cartas import buscar_produto_liga
from DAO.database import atualizar_produto, buscar_historico_precos, buscar_produto_por_id, deletar, inserir_venda_generica

import threading

IMAGEM_PADRAO = "imagens/imagens_produtos/imagem_padrao.jpg"

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
        file_img = Image.open("imagens/pasta-aberta.png").resize((20, 20))
        FILE_ICON = ImageTk.PhotoImage(file_img)
        CALENDAR_ICON = ImageTk.PhotoImage(calendar_img)
    except Exception as e:
        CALENDAR_ICON = None
        FILE_ICON = None
        registrar_erro(f"Erro ao carregar ícone do calendário: {e}")

    campos = {} 

   

    # Cria o scroll
    scroll_frame = ScrollableFrame(main_frame)
    scroll_frame.grid(row=0, column=0, sticky="nsew")

   
    # Cria o frame de formulário com título
    form_frame = ttk.LabelFrame(scroll_frame.scrollable_frame, text="Dados do Produto", padding=10)
    form_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    # Força expansão total horizontal
    form_frame.grid(sticky="nsew")
    
    scroll_frame.scrollable_frame.columnconfigure(0, weight=1)

    scroll_frame.scrollable_frame.rowconfigure(0, weight=1)

    form_frame.columnconfigure(0, weight=1)
    form_frame.columnconfigure(1, weight=1)
    form_frame.columnconfigure(2, weight=1)


    campos["link"] = criar_entrada_padrao(form_frame, "Link:", 0)
    campos["nome"] = criar_entrada_padrao(form_frame, "Nome:", 1)
    campos["imagem"] = criar_entrada_padrao(form_frame, "URL da Imagem:", 2)

    def atualizar_imagem(caminho):
        try:
            if caminho.startswith("http://") or caminho.startswith("https://"):
                with urllib.request.urlopen(caminho) as u:
                    raw_data = u.read()
                im = Image.open(BytesIO(raw_data))
            else:
                im = Image.open(caminho)

            im.thumbnail((300, 420))
            photo = ImageTk.PhotoImage(im)
            imagem_label.configure(image=photo)
            imagem_label.image = photo
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar imagem: {e}", parent=root)
            registrar_erro(f"[Erro] Falha ao carregar imagem: {e}")
            imagem_label.configure(image='')
            imagem_label.image = None            
    
    campos["imagem_salva"] = criar_entrada_com_botao_imagem(
        frame=form_frame,
        texto="Imagem:",
        linha=3,
        ao_selecionar=atualizar_imagem,  # <- callback automático
        path="imagens/imagens_produtos",
        icone=FILE_ICON
    )

    campos["preco_compra"] = criar_entrada_padrao(form_frame, "Preço Compra:", 4)
    campos["preco_atual"] = criar_entrada_padrao(form_frame, "Preço Atual:", 5)

    campos["data_compra"] = criar_entrada_data_com_calendario(
        frame=form_frame,
        root=root,
        linha=6,
        texto_label="Data da Compra:",
        icone=CALENDAR_ICON
    )

    campos["quantidade"] = criar_entrada_padrao(form_frame, "Quantidade:", 7)
    campos["origem"] = criar_entrada_padrao(form_frame, "Origem:", 8)

    campos["data_scraping"] = criar_entrada_data_com_calendario(
        frame=form_frame,
        root=root,
        linha=9,
        texto_label="Data do Scraping:",
        icone=CALENDAR_ICON
    )


    # dentro da função ou método da tela
    historico = buscar_historico_precos(tipo="produto", id=id_produto)

    frame_grafico_container = ttk.LabelFrame(main_frame, text="Histórico", padding=10)
    frame_grafico_container.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

    grafico = GraficoHistorico(
        parent=frame_grafico_container,
        dados=historico,
        titulo="Histórico de Preços do Produto",       
        campos_numericos=["preco"]
    )
    grafico.pack(fill="both", expand=True)


    main_frame.rowconfigure(1, weight=1)

    imagem_frame = ttk.LabelFrame(main_frame, text="Imagem", padding=10, width=320)
    imagem_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ns")
    imagem_label = ttk.Label(imagem_frame)
    imagem_label.pack()

    def atualizar_imagem(caminho):
        try:
            if caminho.startswith("http://") or caminho.startswith("https://"):
                with urllib.request.urlopen(caminho) as u:
                    raw_data = u.read()
                im = Image.open(BytesIO(raw_data))
            else:
                im = Image.open(caminho)

            im.thumbnail((300, 420))
            photo = ImageTk.PhotoImage(im)
            imagem_label.configure(image=photo)
            imagem_label.image = photo
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar imagem: {e}", parent=root)
            registrar_erro(f"[Erro] Falha ao carregar imagem: {e}")
            imagem_label.configure(image='')
            imagem_label.image = None

    def to_decimal(valor):
        try:
            return float(str(valor).replace("R$", "").replace(",", ".").strip())
        except:
            return 0.0

    def buscar_info_scraping():
        url = campos["link"].get().strip()
        if not url:
            messagebox.showwarning("Aviso", "Informe o link do produto.", parent=root)
            return

        def _buscar():
            try:
                dados = buscar_produto_liga(url)
                if not dados:
                    # qualquer interação com UI precisa voltar pra main thread
                    return root.after(0, lambda: messagebox.showwarning(
                        "Aviso", "Nenhum dado retornado do scraping.", parent=root))

                # Atualize a UI sempre via main thread
                def preencher():
                    campos["nome"].delete(0, tk.END)
                    campos["nome"].insert(0, dados.get("nome", ""))

                    campos["imagem"].delete(0, tk.END)
                    campos["imagem"].insert(0, dados.get("imagem", ""))

                    preco = dados.get("preco_atual", "").replace("R$", "").replace(",", ".").strip()
                    campos["preco_atual"].delete(0, tk.END)
                    campos["preco_atual"].insert(0, preco)     

                    campos["data_scraping"].delete(0, tk.END)
                    campos["data_scraping"].insert(0, datetime.today().strftime("%Y-%m-%d"))

                   # Baixa e preenche caminho salvo
                    nome_arquivo = f"{dados['nome']}.jpg"
                    caminho_local = salvar_imagem_local(url_imagem=dados["imagem"], nome_arquivo=nome_arquivo, pasta="imagens/imagens_produtos")

                    if caminho_local:
                        campos["imagem_salva"].delete(0, tk.END)
                        campos["imagem_salva"].insert(0, caminho_local.replace("\\", "/"))
                        atualizar_imagem(caminho_local)
                    else:
                        atualizar_imagem(dados["imagem"])  # fallback
                    
                root.after(0, preencher)

            except Exception as e:
                root.after(0, lambda: messagebox.showerror("Erro", f"Erro no scraping: {e}", parent=root))

        # Aqui entra o seu modal com thread 👇
        executar_em_thread(
            root,
            _buscar,
            titulo="Buscando dados",
            mensagem="Coletando informações do produto..."
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
                "data_scraping": campos["data_scraping"].get() or datetime.today().strftime("%Y-%m-%d"),
                "imagem_salva": campos["imagem_salva"].get() or "",
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
            if deletar(id=id_produto, tabela="produto", tipo="produto"):
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
                    "imagem_salva": campos["imagem_salva"].get() or "",
                    "data_scraping": campos["data_scraping"].get() or datetime.today().strftime("%Y-%m-%d"),
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

    def clonar_produto():
        if messagebox.askokcancel("Confirmar", "Deseja clonar este produto?", parent=root):
            try:
                novo_produto = {
                    "nome_produto": campos["nome"].get(),
                    "link": campos["link"].get(),
                    "imagem": campos["imagem"].get() or IMAGEM_PADRAO,
                    "preco_compra": to_decimal(campos["preco_compra"].get()),
                    "preco_atual": to_decimal(campos["preco_atual"].get()),
                    "data_compra": campos["data_compra"].get(),
                    "quantidade": int(campos["quantidade"].get()),
                    "origem": campos["origem"].get() or "Liga Yugioh",
                    "data_scraping": campos["data_scraping"].get() or datetime.today().strftime("%Y-%m-%d"),
                    "imagem_salva": campos["imagem_salva"].get() or "",
                }
                atualizar_produto(novo_produto, novo=True)
                messagebox.showinfo("Sucesso", "Produto clonado com sucesso!", parent=root)
                ao_fechar()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao clonar produto: {e}", parent=root)
                registrar_erro(f"Erro ao clonar produto: {e}")

    # Criar frame dos botões corretamente
    botoes_frame = ttk.Frame(main_frame)
    botoes_frame.grid(row=2, column=0, columnspan=2, pady=10)
    main_frame.rowconfigure(2, weight=0)


    # Botões dentro do frame
    ttk.Button(botoes_frame, text="Buscar via Scraping", command=buscar_info_scraping).grid(row=0, column=0, padx=10)
    ttk.Button(botoes_frame, text="Salvar Produto", command=salvar).grid(row=0, column=1, padx=10)
    ttk.Button(botoes_frame, text="Deletar Produto", command=apagar_produto).grid(row=0, column=2, padx=10)
    ttk.Button(botoes_frame, text="Vender Produto", command=vender).grid(row=0, column=3, padx=10)
    ttk.Button(botoes_frame, text="Clonar Produto", command=clonar_produto).grid(row=0, column=4, padx=10)


    # Preencher campos com os dados do produto existente
    campos["link"].insert(0, produto["link"] or "")
    campos["nome"].insert(0, produto["nome_produto"] or "")
    campos["imagem"].insert(0, produto["imagem"] or IMAGEM_PADRAO)
    campos["preco_compra"].insert(0, str(produto["preco_compra"] or ""))
    campos["preco_atual"].insert(0, str(produto["preco_atual"] or ""))
    campos["data_compra"].insert(0, produto["data_compra"] or "")
    campos["quantidade"].insert(0, str(produto["quantidade"] or "1"))
    campos["origem"].insert(0, produto["origem"] or "Liga Yugioh")
    campos["imagem_salva"].insert(0, produto["imagem_salva"] or "")
    campos["data_scraping"].insert(0, produto.get("data_scraping", ""))

    # Tenta exibir imagem salva local, senão usa a da URL, senão usa a padrão
    caminho_imagem = produto["imagem_salva"] or produto["imagem"] or IMAGEM_PADRAO
    atualizar_imagem(caminho_imagem)


    root.mainloop()


if __name__ == "__main__":
    app = tk.Tk()
    app.withdraw()
    criar_tela_editar_produto(app)
    app.mainloop()
