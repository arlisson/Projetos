# ... imports
import re
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
import urllib.request
from io import BytesIO
from datetime import datetime

from Components.entrada_padrao import criar_entrada_com_botao_imagem, criar_entrada_data_com_calendario
from Components.pop_up_venda import abrir_popup_venda
from Utils.combo_utils import popular_dropdown
from Utils.limpar_preco import limpar_preco
from scraping.scraping_cartas import buscar_carta_myp
from DAO.database import *
from tkcalendar import Calendar
from Components.thread_com_modal import executar_em_thread
from Utils.baixar_carta import salvar_imagem_local



IMAGEM_PADRAO = "imagens/imagens_cartas/imagem_padrao.jpg"

def criar_tela_editar_carta(app, id_carta):
    from View.listar_cartas import abrir_tela_listagem
    carta = buscar_carta_por_id(id_carta)
    if not carta:
        messagebox.showerror("Erro", "Carta não encontrada.")
        return

    root = tk.Toplevel(app)

    def ao_fechar():
        abrir_tela_listagem(app)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", ao_fechar)

    root.grab_set()
    root.focus_force()
    root.title("Editar Carta")
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

    

    def criar_rotulo_entrada(frame, texto, linha, largura=50, somente_leitura=False):
        ttk.Label(frame, text=texto).grid(row=linha, column=0, sticky="w", padx=5, pady=3)
        entrada = ttk.Entry(frame, width=largura)
        if somente_leitura:
            entrada.configure(state="readonly")
        entrada.grid(row=linha, column=1, columnspan=2, padx=5, pady=3, sticky="we")
        return entrada

    form_frame = ttk.LabelFrame(main_frame, text="Dados da Carta", padding=10)
    form_frame.grid(row=0, column=0, sticky="nsew")
    form_frame.columnconfigure(1, weight=1)

    campos["link"] = criar_rotulo_entrada(form_frame, "Link da carta:", 0)
    campos["nome"] = criar_rotulo_entrada(form_frame, "Nome:", 1)
    campos["codigo"] = criar_rotulo_entrada(form_frame, "Código:", 2)
    campos["preco"] = criar_rotulo_entrada(form_frame, "Preço pago:", 3)
    campos["preco_atual"] = criar_rotulo_entrada(form_frame, "Preço atual:", 4)

    campos["data"] = criar_entrada_data_com_calendario(
        frame=form_frame,
        root=root,
        linha=5,
        texto_label="Data da Compra:",
        icone=CALENDAR_ICON  # ou None para usar 📅
    )

    campos["quantidade"] = criar_rotulo_entrada(form_frame, "Quantidade:", 6)
    campos["imagem"] = criar_rotulo_entrada(form_frame, "Imagem URL:", 7)

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


    # Criar campo
    campos["imagem_salva"] = criar_entrada_com_botao_imagem(
        frame=form_frame,
        texto="Imagem:",
        linha=8,
        ao_selecionar=atualizar_imagem,
        path="imagens/imagens_cartas",
        icone=FILE_ICON  # ou None para usar "📁"
    )

    campos["origem"] = criar_rotulo_entrada(form_frame, "Origem:", 13)

   
    # raridade agora vai na linha 9
    ttk.Label(form_frame, text="Raridade:").grid(row=10, column=0, sticky="w", padx=5, pady=3)
    campos["raridade"] = ttk.Combobox(form_frame, state="readonly")
    campos["raridade"].grid(row=10, column=1, columnspan=2, padx=5, pady=3, sticky="we")
    popular_dropdown(campos["raridade"], buscar_valores_tabela("raridade"))

    ttk.Label(form_frame, text="Qualidade:").grid(row=11, column=0, sticky="w", padx=5, pady=3)
    campos["qualidade"] = ttk.Combobox(form_frame, state="readonly")
    campos["qualidade"].grid(row=11, column=1, columnspan=2, padx=5, pady=3, sticky="we")
    popular_dropdown(campos["qualidade"], buscar_valores_tabela("qualidade"))

    ttk.Label(form_frame, text="Coleção:").grid(row=12, column=0, sticky="w", padx=5, pady=3)
    campos["colecao"] = ttk.Combobox(form_frame, state="readonly")
    campos["colecao"].grid(row=12, column=1, columnspan=2, padx=5, pady=3, sticky="we")
    popular_dropdown(campos["colecao"], buscar_valores_tabela("colecao"))

    imagem_frame = ttk.LabelFrame(main_frame, text="Imagem", padding=10)
    imagem_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

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
        except:
            imagem_label.configure(image='')
            imagem_label.image = None


    
    def preencher_com_scraping():
        def _buscar():
            try:
                url = campos["link"].get().strip()
                if not url:
                    return root.after(0, lambda: messagebox.showwarning("Aviso", "Informe o link da carta.", parent=root))

                raridade_texto = campos["raridade"].get()
                if not raridade_texto:
                    return root.after(0, lambda: messagebox.showwarning("Aviso", "Selecione a raridade antes de buscar.", parent=root))

                raridade_nome = raridade_texto.split(" - ")[1]
                resultados = buscar_carta_myp(url=url, chave=raridade_nome)

                if not resultados:
                    return root.after(0, lambda: messagebox.showwarning("Aviso", "Nenhum resultado encontrado.", parent=root))

                dados = resultados[0]
                
                def preencher():
                    campos["nome"].delete(0, tk.END)
                    campos["nome"].insert(0, dados["nome"])

                    campos["codigo"].delete(0, tk.END)
                    campos["codigo"].insert(0, dados["codigo"])

                    campos["preco_atual"].delete(0, tk.END)
                    campos["preco_atual"].insert(0, limpar_preco(dados["preco_atual"]))

                    imagem_url = dados["imagem"]
                    codigo = dados["codigo"] or re.sub(r'\W+', '_', dados["nome"].lower())
                    nome_arquivo = f"{codigo}.jpg"
                    caminho_local = salvar_imagem_local(imagem_url, nome_arquivo)

                    campos["imagem"].delete(0, tk.END)
                    campos["imagem"].insert(0, imagem_url)

                    campos["imagem_salva"].delete(0, tk.END)
                    campos["imagem_salva"].insert(0, caminho_local or "")

                    atualizar_imagem(caminho_local or imagem_url)


                    campos["origem"].delete(0, tk.END)
                    campos["origem"].insert(0, dados["origem"])

                    # Atualiza dropdown de coleção
                    colecao_nome = dados["colecao"]
                    colecao_id = buscar_colecao_por_nome(colecao_nome)
                    if not colecao_id:
                        colecao_id = inserir_colecao(colecao_nome)

                    popular_dropdown(campos["colecao"], buscar_valores_tabela("colecao"))
                    for i, val in enumerate(campos["colecao"].cget("values")):
                        if val.startswith(f"{colecao_id} -"):
                            campos["colecao"].current(i)
                            break

                    messagebox.showinfo("Sucesso", "Dados preenchidos com sucesso!", parent=root)

                root.after(0, preencher)

            except Exception as e:
                root.after(0, lambda: messagebox.showerror("Erro", f"Erro ao buscar via scraping: {e}", parent=root))

        # Executa com modal de progresso
        executar_em_thread(
            root,
            _buscar,
            titulo="Buscando Dados da Carta",
            mensagem="Realizando scraping da carta selecionada..."
        )


    # Preenche os campos com os dados da carta
    campos["link"].insert(0, carta["link_site"])
    campos["nome"].insert(0, carta["nome"])
    campos["codigo"].insert(0, carta["codigo"])
    campos["preco"].insert(0, str(carta["preco_da_compra"]))
    campos["preco_atual"].insert(0, str(carta["preco_atual"]))
    campos["data"].insert(0, carta["data_da_compra"])
    campos["quantidade"].insert(0, str(carta["quantidade"]))    
    campos["origem"].insert(0, carta["origem"])
    campos["imagem"].insert(0, carta["imagem"])
    campos["imagem_salva"].insert(0, carta.get("imagem_salva", ""))
    atualizar_imagem(carta.get("imagem_salva") or carta["imagem"])


    for i, val in enumerate(campos["raridade"].cget("values")):
        if val.startswith(f"{carta['raridade']} -"):
            campos["raridade"].current(i)
            break
    for i, val in enumerate(campos["qualidade"].cget("values")):
        if val.startswith(f"{carta['qualidade']} -"):
            campos["qualidade"].current(i)
            break
    for i, val in enumerate(campos["colecao"].cget("values")):
        if val.startswith(f"{carta['colecao']} -"):
            campos["colecao"].current(i)
            break

    def salvar():
        try:
            # Validação e montagem do dicionário
            carta_atualizada = {
                "id_carta": id_carta,
                "link_site": campos["link"].get(),
                "nome": campos["nome"].get(),
                "codigo": campos["codigo"].get(),
                "preco_da_compra": limpar_preco(campos["preco"].get()),
                "preco_atual": limpar_preco(campos["preco_atual"].get()),
                "data_da_compra": campos["data"].get(),
                "quantidade": int(campos["quantidade"].get()),
                "imagem": campos["imagem"].get() or IMAGEM_PADRAO,
                "origem": campos["origem"].get(),
                "raridade": int(campos["raridade"].get().split(" - ")[0]),
                "qualidade": int(campos["qualidade"].get().split(" - ")[0]),
                "colecao": int(campos["colecao"].get().split(" - ")[0]),
                "data_scraping": datetime.today().strftime("%Y-%m-%d"),
                "imagem_salva": campos["imagem_salva"].get().replace("\\", "/") or ""
            }
           
            def _salvar():
                try:
                    atualizar_carta(carta_atualizada)
                    root.after(0, lambda: (
                        messagebox.showinfo("Sucesso", "Carta atualizada com sucesso!", parent=root),
                        ao_fechar()
                    ))
                except Exception as e:
                    root.after(0, lambda: messagebox.showerror("Erro", f"Erro ao atualizar carta: {e}", parent=root))

            executar_em_thread(
                root,
                _salvar,
                titulo="Salvando Alterações",
                mensagem="Atualizando os dados da carta..."
            )

        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {e}", parent=root)


    def apagar():
        if messagebox.askokcancel("Confirmar", "Tem certeza que deseja deletar esta carta?", parent=root):
            if deletar(id=id_carta, tabela="carta"):
                messagebox.showinfo("Sucesso", f"Carta: {campos['nome'].get()} deletada com sucesso!", parent=root)
                ao_fechar()
            else:
                messagebox.showerror("Erro", f"Erro ao deletar a carta: {campos['nome'].get()}.", parent=root)
    
    def vender():
        def ao_confirmar(preco_venda, quantidade_vendida):
            try:
                preco_venda = float(preco_venda)
                quantidade_vendida = int(quantidade_vendida)
                quantidade_disponivel = int(campos["quantidade"].get())

                if quantidade_vendida > quantidade_disponivel:
                    raise ValueError("Quantidade vendida excede a disponível")

                dados_venda = {
                    "link_site": campos["link"].get(),
                    "nome": campos["nome"].get(),
                    "codigo": campos["codigo"].get(),
                    "preco_da_compra": limpar_preco(campos["preco"].get()),
                    "data_da_compra": campos["data"].get(),
                    "raridade": int(campos["raridade"].get().split(" - ")[0]),
                    "qualidade": int(campos["qualidade"].get().split(" - ")[0]),
                    "colecao": int(campos["colecao"].get().split(" - ")[0]),
                    "quantidade": quantidade_vendida,
                    "data_da_venda": datetime.today().strftime("%Y-%m-%d"),
                    "preco_da_venda": preco_venda,
                    "imagem": campos["imagem"].get(),
                    "origem": campos["origem"].get(),
                    "preco_atual": limpar_preco(campos["preco_atual"].get()),
                    "data_scraping": datetime.today().strftime("%Y-%m-%d"),
                    "imagem_salva": campos["imagem_salva"].get().replace("\\", "/") or ""
                }

                inserir_venda_generica(
                    id_item=id_carta,
                    quantidade_vendida=quantidade_vendida,
                    preco_venda=preco_venda,
                    tipo="carta"
                )


                nova_qtd = quantidade_disponivel - quantidade_vendida
                campos["quantidade"].delete(0, tk.END)
                campos["quantidade"].insert(0, str(nova_qtd))

                messagebox.showinfo("Sucesso", "Venda registrada com sucesso!", parent=root)
                ao_fechar()

            except Exception as e:
                registrar_erro("Erro ao registrar venda:", e)
                messagebox.showerror("Erro", f"Erro ao registrar venda: {e}", parent=root)

        nome_item = campos["nome"].get()
        quantidade_disponivel = int(campos["quantidade"].get())
        abrir_popup_venda(root, nome_item, quantidade_disponivel, ao_confirmar)


    botoes_frame = ttk.Frame(main_frame)
    botoes_frame.grid(row=2, column=0, pady=10)
    ttk.Button(botoes_frame, text="Buscar via scraping", command=preencher_com_scraping).grid(row=0, column=0, padx=10)
    ttk.Button(botoes_frame, text="Salvar Alterações", command=salvar).grid(row=0, column=1, padx=10)
    ttk.Button(botoes_frame, text="Deletar", command=apagar).grid(row=0, column=2, padx=10)
    ttk.Button(botoes_frame, text="Vender Carta", command=vender).grid(row=0, column=3, padx=10)

    root.mainloop()


if __name__ == "__main__":
    app = tk.Tk()
    app.withdraw()
    criar_tela_editar_carta(app)
    app.mainloop()