import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar

# Cria um campo de entrada com rótulo
def criar_entrada_padrao(frame, texto, linha, largura=50, somente_leitura=False):
    ttk.Label(frame, text=texto).grid(row=linha, column=0, sticky="w", padx=5, pady=3)
    entrada = ttk.Entry(frame, width=largura)
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

# Cria um campo com calendário associado
def criar_entrada_data_com_calendario(parent_frame, root, linha, label_text, icone=None):
    ttk.Label(parent_frame, text=label_text).grid(row=linha, column=0, sticky="w", padx=5, pady=3)
    
    frame_data = ttk.Frame(parent_frame)
    frame_data.grid(row=linha, column=1, columnspan=2, padx=5, pady=3, sticky="we")
    frame_data.columnconfigure(0, weight=1)

    entrada_data = ttk.Entry(frame_data)
    entrada_data.grid(row=0, column=0, sticky="we", padx=(0, 5))

    def abrir_calendario():
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

    btn = ttk.Button(frame_data, image=icone if icone else None, text="📅" if not icone else "", command=abrir_calendario)
    btn.grid(row=0, column=1)

    return entrada_data
