import tkinter as tk
from tkinter import ttk, messagebox


def abrir_popup_venda(parent, nome_item, quantidade_disponivel, callback):
    popup = tk.Toplevel(parent)
    popup.title(f"Vender: {nome_item}")
    popup.transient(parent)
    popup.grab_set()
    popup.resizable(False, False)

    largura, altura = 320, 200
    x = parent.winfo_rootx() + 100
    y = parent.winfo_rooty() + 100
    popup.geometry(f"{largura}x{altura}+{x}+{y}")

    frame = ttk.Frame(popup, padding=15)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text=f"Quantidade disponível: {quantidade_disponivel}", font=("Segoe UI", 10, "bold"), foreground="gray").pack(anchor="w", pady=(0, 10))

    ttk.Label(frame, text="Preço de venda (R$):").pack(anchor="w")
    entrada_preco = ttk.Entry(frame)
    entrada_preco.pack(fill="x", pady=5)

    ttk.Label(frame, text="Quantidade a vender:").pack(anchor="w")
    entrada_quantidade = ttk.Entry(frame)
    entrada_quantidade.pack(fill="x", pady=5)

    def confirmar():
        try:
            preco = float(entrada_preco.get().replace(",", "."))
            quantidade = int(entrada_quantidade.get())

            if preco <= 0:
                raise ValueError("O preço deve ser maior que zero.")
            if quantidade <= 0:
                raise ValueError("A quantidade deve ser maior que zero.")
            if quantidade > quantidade_disponivel:
                raise ValueError(f"A quantidade não pode ser maior que {quantidade_disponivel}.")

            popup.destroy()
            callback(preco, quantidade)

        except ValueError as ve:
            messagebox.showerror("Erro de validação", str(ve), parent=popup)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {e}", parent=popup)

    btns = ttk.Frame(frame)
    btns.pack(fill="x", pady=(15, 0))

    # Ordem corrigida: Confirmar à direita, Cancelar à esquerda
    ttk.Button(btns, text="Confirmar Venda", command=confirmar).pack(side="right", padx=(5, 0))
    ttk.Button(btns, text="Cancelar", command=popup.destroy).pack(side="right")
