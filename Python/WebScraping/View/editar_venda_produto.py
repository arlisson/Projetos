import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import urllib.request
from io import BytesIO
from datetime import datetime
import threading

from tkcalendar import Calendar

from Components.entrada_padrao import criar_entrada_com_botao_imagem, criar_entrada_com_botao_imagem, criar_entrada_data_com_calendario, criar_entrada_padrao
from Components.thread_com_modal import executar_em_thread
from Utils.baixar_carta import salvar_imagem_local
from Utils.log import registrar_erro
from scraping.scraping_cartas import buscar_produto_liga  # reutilizado para produto
from DAO.database import (
    deletar,
    listar_venda_por_id,
    atualizar_venda_generica,
)

IMAGEM_PADRAO = "https://i.pinimg.com/736x/71/1e/da/711eda25308c65a7756751088866e181.jpg"


def criar_tela_editar_venda_produto(app, id_venda_produto):
    from View.listar_venda_produtos import abrir_tela_listagem_venda_produtos

    root = tk.Toplevel(app)

    def ao_fechar():
        root.destroy()
        abrir_tela_listagem_venda_produtos(app)

    root.protocol("WM_DELETE_WINDOW", ao_fechar)
    root.grab_set()
    root.focus_force()

    # --------- CARREGA VENDA ----------
    venda = listar_venda_por_id(tipo="produto", id=id_venda_produto)
    if not venda:
        messagebox.showerror("Erro", "Venda de produto não encontrada.")
        ao_fechar()
        return

    # Esperado do DAO: chaves:
    # id_venda_produto, nome_produto, link, imagem, preco_compra, data_compra,
    # preco_venda, data_venda, origem, preco_atual, quantidade, data_scraping

    root.title("Editar Venda de Produto")
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

    # --------- ÍCONE CALENDÁRIO ----------
    try:
        calendar_img = Image.open("imagens/calendario.png").resize((20, 20))
        CALENDAR_ICON = ImageTk.PhotoImage(calendar_img)
        file_icon_img = Image.open("imagens/pasta-aberta.png").resize((20, 20))
        FILE_ICON = ImageTk.PhotoImage(file_icon_img)
    except Exception as e:
        CALENDAR_ICON = None
        FILE_ICON = None
        registrar_erro(f"Erro ao carregar ícone do calendário: {e}")

    campos = {}

    
    
    form_frame = ttk.LabelFrame(main_frame, text="Dados da Venda (Produto)", padding=10)
    form_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    form_frame.columnconfigure(1, weight=1)

    campos["link"] = criar_entrada_padrao(form_frame, "Link:", 0)
    campos["nome_produto"] = criar_entrada_padrao(form_frame, "Nome do Produto:", 1)
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
        ao_selecionar=atualizar_imagem,
        path="imagens/imagens_produtos",
        icone=FILE_ICON  # ou None para usar "📁"
    )

    campos["preco_compra"] = criar_entrada_padrao(form_frame, "Preço Compra (unit):", 4)
    campos["preco_atual"] = criar_entrada_padrao(form_frame, "Preço Atual (unit):", 5)

    campos["data_compra"] = criar_entrada_data_com_calendario(
            frame=form_frame,
            root=root,
            linha=6,
            texto_label="Data da Compra:",
            icone=CALENDAR_ICON  # ou None para usar 📅
    )
    

    campos["quantidade"] = criar_entrada_padrao(form_frame, "Quantidade vendida:", 7)
    campos["origem"] = criar_entrada_padrao(form_frame, "Origem:", 8)

    campos["data_venda"] = criar_entrada_data_com_calendario(
            frame=form_frame,
            root=root,
            linha=9,
            texto_label="Data da Venda:",
            icone=CALENDAR_ICON  # ou None para usar 📅
    )

    campos["preco_venda"] = criar_entrada_padrao(form_frame, "Preço da Venda (unit):", 10)

    campos["data_scraping"] = criar_entrada_data_com_calendario(
            frame=form_frame,
            root=root,
            linha=11,
            texto_label="Data do Scraping:",
            icone=CALENDAR_ICON  # ou None para usar 📅
    )

    # ------- Imagem -------
    imagem_frame = ttk.LabelFrame(main_frame, text="Imagem", padding=10, width=320)
    imagem_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ns")
    imagem_label = ttk.Label(imagem_frame)
    imagem_label.pack()

    

    def to_decimal(valor: str) -> float:
        try:
            return float(str(valor).replace("R$", "").replace(",", ".").strip())
        except Exception:
            return 0.0

    # ---------- Preenche com dados da VENDA ----------
    campos["link"].insert(0, venda.get("link", "") or "")
    campos["nome_produto"].insert(0, venda.get("nome_produto", "") or "")
    campos["imagem"].insert(0, venda.get("imagem", "") or IMAGEM_PADRAO)
    campos["preco_compra"].insert(0, str(venda.get("preco_compra", "") or ""))
    campos["preco_atual"].insert(0, str(venda.get("preco_atual", "") or ""))
    campos["data_compra"].insert(0, venda.get("data_compra", "") or "")
    campos["quantidade"].insert(0, str(venda.get("quantidade", "") or "1"))
    campos["origem"].insert(0, venda.get("origem", "") or "Liga Yugioh")
    campos["data_venda"].insert(0, venda.get("data_venda", "") or datetime.today().strftime("%Y-%m-%d"))
    campos["preco_venda"].insert(0, str(venda.get("preco_venda", "") or ""))
    campos["imagem_salva"].insert(0, venda.get("imagem_salva", "") or IMAGEM_PADRAO)
    campos["data_scraping"].insert(0, venda.get("data_scraping", "") or datetime.today().strftime("%Y-%m-%d"))

    atualizar_imagem(campos["imagem_salva"].get() or campos["imagem"].get() or IMAGEM_PADRAO)

    # ---------- Scraping (atualiza preco_atual/imagem/nome) ----------
    def preencher_via_scraping():
        def _buscar():
            try:
                url = (campos["link"].get() or "").strip()
                if not url:
                    return root.after(0, lambda: messagebox.showwarning("Aviso", "Informe o link do produto.", parent=root))

                dados = buscar_produto_liga(url)
                if not dados:
                    return root.after(0, lambda: messagebox.showwarning("Aviso", "Nenhum dado retornado do scraping.", parent=root))

                def preencher():
                    # Nome (só preenche se estiver vazio para não sobrescrever manual)
                    if not campos["nome_produto"].get().strip():
                        campos["nome_produto"].delete(0, tk.END)
                        campos["nome_produto"].insert(0, dados.get("nome", "") or "")

                    # Imagem
                    if dados.get("imagem"):
                        campos["imagem"].delete(0, tk.END)
                        campos["imagem"].insert(0, dados.get("imagem"))
                        atualizar_imagem(dados.get("imagem"))

                    # Preço atual
                    preco = (dados.get("preco_atual", "") or "").replace("R$", "").replace(",", ".").strip()
                    if preco:
                        campos["preco_atual"].delete(0, tk.END)
                        campos["preco_atual"].insert(0, preco)

                    # Data scraping (agora)
                    campos["data_scraping"].delete(0, tk.END)
                    campos["data_scraping"].insert(0, datetime.today().strftime("%Y-%m-%d"))

                    nome_arquivo = f"{dados['nome']}.jpg"
                    caminho_local = salvar_imagem_local(url_imagem=dados["imagem"], nome_arquivo=nome_arquivo, pasta="imagens/imagens_produtos")

                    if caminho_local:
                        campos["imagem_salva"].delete(0, tk.END)
                        campos["imagem_salva"].insert(0, caminho_local.replace("\\", "/"))
                        atualizar_imagem(caminho_local)
                    else:
                        atualizar_imagem(dados["imagem"])  # fallback

                    messagebox.showinfo("Sucesso", "Dados atualizados via scraping!", parent=root)

                root.after(0, preencher)

            except Exception as e:
                root.after(0, lambda: messagebox.showerror("Erro", f"Erro no scraping: {e}", parent=root))

        executar_em_thread(
            root,
            _buscar,
            titulo="Buscando Produto",
            mensagem="Coletando informações do produto via scraping..."
        )

    # ---------- Salvar ----------
    def salvar():
        try:
            venda_atualizada = {
                "id_produto": venda.get("id_produto"),   # <--- ESSENCIAL
                "nome_produto": campos["nome_produto"].get(),
                "link": campos["link"].get(),
                "imagem": campos["imagem"].get() or IMAGEM_PADRAO,
                "preco_compra": to_decimal(campos["preco_compra"].get()),
                "data_compra": campos["data_compra"].get(),
                "preco_venda": to_decimal(campos["preco_venda"].get()),
                "data_venda": campos["data_venda"].get(),   # seu schema é DOUBLE, mas SQLite aceita string
                "origem": campos["origem"].get() or "Liga Yugioh",
                "preco_atual": to_decimal(campos["preco_atual"].get()),
                "quantidade": int(campos["quantidade"].get() or 0),
                "imagem_salva": campos["imagem_salva"].get() or "",
                "data_scraping": campos["data_scraping"].get() or datetime.today().strftime("%Y-%m-%d"),
            }

            if venda_atualizada["quantidade"] <= 0:
                raise ValueError("Quantidade deve ser maior que zero.")
            if venda_atualizada["preco_venda"] < 0 or venda_atualizada["preco_compra"] < 0:
                raise ValueError("Preços não podem ser negativos.")

            ok = atualizar_venda_generica(venda=venda_atualizada, tipo="produto")
            if ok:
                messagebox.showinfo("Sucesso", "Venda de produto atualizada com sucesso!", parent=root)
                ao_fechar()
            else:
                messagebox.showerror("Erro", "Não foi possível atualizar a venda.", parent=root)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}", parent=root)
            registrar_erro(f"Erro ao salvar venda de produto: {e}")

    def apagar():
        if messagebox.askokcancel("Confirmar", "Tem certeza que deseja deletar esta venda?", parent=root):
            if deletar(id=id_venda_produto, tabela="venda_produto", tipo="produto"):
                messagebox.showinfo("Sucesso", f"Venda: {campos['nome_produto'].get()} deletada com sucesso!", parent=root)
                ao_fechar()
            else:
                messagebox.showerror("Erro", f"Erro ao deletar a venda: {campos['nome_produto'].get()}.", parent=root)


    # ---------- Botões ----------
    botoes_frame = ttk.Frame(main_frame)
    botoes_frame.grid(row=1, column=0, columnspan=2, pady=10)

    ttk.Button(botoes_frame, text="Atualizar via Scraping", command=preencher_via_scraping).pack(side="left", padx=20, pady=5)
    ttk.Button(botoes_frame, text="Salvar Alterações", command=salvar).pack(side="left", padx=20, pady=5)
    ttk.Button(botoes_frame, text="Deletar", command=apagar).pack(side="left", padx=20, pady=5)

    root.mainloop()
