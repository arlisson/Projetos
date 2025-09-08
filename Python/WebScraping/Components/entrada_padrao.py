import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from tkinter import filedialog


def configurar_estilo_padrao():
    style = ttk.Style()

    style.configure("Custom.TEntry", padding=5, font=("Segoe UI", 10))
    style.configure("Custom.TButton", padding=5, font=("Segoe UI", 10), width=3)
    style.configure("Custom.TLabel", font=("Segoe UI", 10))


# Cria um campo de entrada com rótulo
def criar_entrada_padrao(frame, texto, linha, largura=50, somente_leitura=False):
    ttk.Label(frame, text=texto, style="Custom.TLabel").grid(row=linha, column=0, sticky="w", padx=5, pady=3)
    entrada = ttk.Entry(frame, width=largura, style="Custom.TEntry")
    if somente_leitura:
        entrada.configure(state="readonly")
    entrada.grid(row=linha, column=1, columnspan=2, padx=5, pady=3, sticky="we")
    return entrada


# Cria um campo de entrada simples sem coluna extra
def criar_entrada_simples(frame, texto, linha):
    ttk.Label(frame, text=texto).grid(row=linha, column=0, sticky="w", padx=5, pady=3)
    entry = ttk.Entry(frame)
    entry.grid(row=linha, column=1, sticky="ew", padx=5, pady=3)
    return entry


# Cria um campo de entrada de data com calendário'
def criar_entrada_data_com_calendario(frame, root, linha, texto_label, icone=None, largura=50):
    ttk.Label(frame, text=texto_label, style="Custom.TLabel").grid(row=linha, column=0, sticky="w", padx=5, pady=3)

    frame_data = ttk.Frame(frame)
    frame_data.grid(row=linha, column=1, columnspan=2, padx=5, pady=3, sticky="we")
    frame_data.columnconfigure(0, weight=1)

    entrada_data = ttk.Entry(frame_data, width=largura, style="Custom.TEntry")
    entrada_data.grid(row=0, column=0, sticky="we", padx=(0, 5))

    def abrir_calendario(event=None):
        top = tk.Toplevel(root)
        top.title("Selecionar Data")
        top.grab_set()
        top.resizable(False, False)
        top.geometry(f"+{root.winfo_rootx() + 200}+{root.winfo_rooty() + 150}")
        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(padx=10, pady=10)

        def selecionar_data():
            entrada_data.delete(0, tk.END)
            entrada_data.insert(0, cal.get_date())
            top.destroy()

        ttk.Button(top, text="Selecionar", command=selecionar_data).pack(pady=5)

    entrada_data.bind("<Button-1>", abrir_calendario)

    botao = ttk.Button(
        frame_data,
        image=icone if icone else None,
        text="" if icone else "📅",
        style="Custom.TButton",
        command=abrir_calendario
    )
    botao.grid(row=0, column=1)

    return entrada_data



def criar_entrada_com_botao_imagem(frame, texto, linha, largura=50, ao_selecionar=None, path="imagens/imagens_cartas", icone=None):
    ttk.Label(frame, text=texto, style="Custom.TLabel").grid(row=linha, column=0, sticky="w", padx=5, pady=3)

    frame_input = ttk.Frame(frame)
    frame_input.grid(row=linha, column=1, columnspan=2, padx=5, pady=3, sticky="we")
    frame_input.columnconfigure(0, weight=1)

    entrada = ttk.Entry(frame_input, width=largura, style="Custom.TEntry")
    entrada.grid(row=0, column=0, sticky="we", padx=(0, 5))

    def escolher_imagem():
        caminho = filedialog.askopenfilename(
            title="Selecionar Imagem",
            initialdir=path,
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.webp")]
        )
        if caminho:
            caminho_formatado = caminho.replace("\\", "/")
            entrada.delete(0, tk.END)
            entrada.insert(0, caminho_formatado)

            if ao_selecionar:
                ao_selecionar(caminho_formatado)

    botao = ttk.Button(
        frame_input,
        image=icone if icone else None,
        text="" if icone else "📁",
        style="Custom.TButton",
        command=escolher_imagem
    )
    botao.grid(row=0, column=1)

    return entrada
