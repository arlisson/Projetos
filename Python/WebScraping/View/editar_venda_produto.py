import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import urllib.request
from io import BytesIO
from datetime import datetime
import threading

from tkcalendar import Calendar

from Components.thread_com_modal import executar_em_thread
from Utils.log import registrar_erro
from scraping.scraping_cartas import buscar_produto_liga  # reutilizado para produto
from DAO.database import (
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
        icon_ok = True
    except Exception:
        CALENDAR_ICON = None
        icon_ok = False

    campos = {}

    def abrir_calendario(campo_destino_key: str, titulo: str):
        top = tk.Toplevel(root)
        top.title(titulo)
        top.grab_set()
        top.resizable(False, False)
        top.geometry(f"+{root.winfo_rootx() + 200}+{root.winfo_rooty() + 150}")
        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(padx=10, pady=10)

        def selecionar_data():
            campos[campo_destino_key].delete(0, tk.END)
            campos[campo_destino_key].insert(0, cal.get_date())
            top.destroy()

        ttk.Button(top, text="Selecionar", command=selecionar_data).pack(pady=5)

    def criar_entrada(frame, label, row, width=None):
        ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", padx=5, pady=3)
        entry = ttk.Entry(frame, width=width)
        entry.grid(row=row, column=1, sticky="ew", padx=5, pady=3)
        return entry

    form_frame = ttk.LabelFrame(main_frame, text="Dados da Venda (Produto)", padding=10)
    form_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    form_frame.columnconfigure(1, weight=1)

    campos["link"] = criar_entrada(form_frame, "Link:", 0)
    campos["nome_produto"] = criar_entrada(form_frame, "Nome do Produto:", 1)
    campos["imagem"] = criar_entrada(form_frame, "URL da Imagem:", 2)
    campos["preco_compra"] = criar_entrada(form_frame, "Preço Compra (unit):", 3)
    campos["preco_atual"] = criar_entrada(form_frame, "Preço Atual (unit):", 4)

    # Data da compra
    ttk.Label(form_frame, text="Data da Compra:").grid(row=5, column=0, sticky="w", padx=5, pady=3)
    data_compra_frame = ttk.Frame(form_frame)
    data_compra_frame.grid(row=5, column=1, padx=5, pady=3, sticky="ew")
    data_compra_frame.columnconfigure(0, weight=1)
    campos["data_compra"] = ttk.Entry(data_compra_frame)
    campos["data_compra"].grid(row=0, column=0, sticky="ew", padx=(0, 5))
    ttk.Button(
        data_compra_frame,
        image=CALENDAR_ICON if icon_ok else None,
        text="📅" if not icon_ok else "",
        command=lambda: abrir_calendario("data_compra", "Selecionar Data de Compra")
    ).grid(row=0, column=1)

    campos["quantidade"] = criar_entrada(form_frame, "Quantidade vendida:", 6)
    campos["origem"] = criar_entrada(form_frame, "Origem:", 7)

    # Data da venda
    ttk.Label(form_frame, text="Data da Venda:").grid(row=8, column=0, sticky="w", padx=5, pady=3)
    data_venda_frame = ttk.Frame(form_frame)
    data_venda_frame.grid(row=8, column=1, padx=5, pady=3, sticky="ew")
    data_venda_frame.columnconfigure(0, weight=1)
    campos["data_venda"] = ttk.Entry(data_venda_frame)
    campos["data_venda"].grid(row=0, column=0, sticky="ew", padx=(0, 5))
    ttk.Button(
        data_venda_frame,
        image=CALENDAR_ICON if icon_ok else None,
        text="📅" if not icon_ok else "",
        command=lambda: abrir_calendario("data_venda", "Selecionar Data de Venda")
    ).grid(row=0, column=1)

    campos["preco_venda"] = criar_entrada(form_frame, "Preço da Venda (unit):", 9)

    # Somente leitura (auto): data_scraping
    ttk.Label(form_frame, text="Data Scraping:").grid(row=10, column=0, sticky="w", padx=5, pady=3)
    campos["data_scraping"] = ttk.Entry(form_frame)
    campos["data_scraping"].grid(row=10, column=1, sticky="ew", padx=5, pady=3)

    # ------- Imagem -------
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
            except Exception:
                root.after(0, lambda: (imagem_label.configure(image=''), setattr(imagem_label, 'image', None)))
        threading.Thread(target=_baixar, daemon=True).start()

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
    campos["data_scraping"].insert(0, venda.get("data_scraping", "") or datetime.today().strftime("%Y-%m-%d"))

    atualizar_imagem(campos["imagem"].get() or IMAGEM_PADRAO)

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

    # ---------- Botões ----------
    botoes_frame = ttk.Frame(main_frame)
    botoes_frame.grid(row=1, column=0, columnspan=2, pady=10)

    ttk.Button(botoes_frame, text="Atualizar via Scraping", command=preencher_via_scraping).pack(side="left", padx=20, pady=5)
    ttk.Button(botoes_frame, text="Salvar Alterações", command=salvar).pack(side="left", padx=20, pady=5)
    ttk.Button(botoes_frame, text="Fechar", command=ao_fechar).pack(side="left", padx=20, pady=5)

    root.mainloop()
