# Components/modal_progresso.py

import tkinter as tk
from tkinter import ttk

class ModalProgresso:
    def __init__(self, parent, titulo="Carregando", mensagem="Aguarde..."):
        self.parent = parent
        self.popup = tk.Toplevel(parent)
        self.popup.title(titulo)
        self.popup.resizable(False, False)
        self.popup.transient(parent)
        self.popup.grab_set()

        # Tamanho fixo do modal
        largura = 320
        altura = 120

        # 🧮 Calcula a posição para centralizar na tela (ou sobre a janela pai)
        self.popup.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (largura // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (altura // 2)

        self.popup.geometry(f"{largura}x{altura}+{x}+{y}")

        # 🧾 Mensagem e barra de progresso
        self.label = ttk.Label(self.popup, text=mensagem)
        self.label.pack(pady=(20, 10), padx=10)

        self.barra = ttk.Progressbar(self.popup, mode='indeterminate')
        self.barra.pack(padx=20, fill="x")
        self.barra.start(10)

        # ❌ Impede fechamento manual
        self.popup.protocol("WM_DELETE_WINDOW", self._ignorar_fechar)

    def atualizar_mensagem(self, nova_mensagem: str):
        self.label.config(text=nova_mensagem)
        self.popup.update()

    def fechar(self):
        try:
            if self.barra.winfo_exists():  # verifica se a barra ainda existe
                self.barra.stop()
            if self.popup.winfo_exists():  # verifica se a janela ainda existe
                self.popup.destroy()
        except tk.TclError:
            # Se já tiver sido destruído, ignora silenciosamente
            pass
    
    def fechar_async(self):
        """Agenda o fechamento seguro a partir de qualquer thread."""
        if self.parent and self.parent.winfo_exists():
            self.parent.after(0, self.fechar)



    def _ignorar_fechar(self):
        pass  # Impede o usuário de fechar o modal
