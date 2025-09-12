import tkinter as tk
from tkinter import ttk
import platform


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self._scroll_ativo = False  # controle do estado do scroll

        # Adiciona o frame interno no canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Scroll vinculado ao canvas
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Redimensiona o frame interno com o canvas
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.scrollable_frame.bind("<Configure>", lambda e: self._ajustar_scroll())

        # Prepara eventos de rolagem
        self._preparar_scroll_eventos()

    def _on_canvas_configure(self, event):
        """Mantém a largura do conteúdo igual à largura do canvas"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _ajustar_scroll(self):
        """Atualiza o scrollregion e visibilidade da barra/scroll do mouse"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self._atualizar_scroll_visivel()

    def _atualizar_scroll_visivel(self):
        """Exibe/oculta scrollbar e ativa/desativa scroll do mouse"""
        bbox = self.canvas.bbox("all")
        if not bbox:
            return

        canvas_height = self.canvas.winfo_height()
        content_height = bbox[3]  # inferior da região

        if content_height <= canvas_height:
            self.scrollbar_y.grid_remove()
            self._desativar_mousewheel()
        else:
            self.scrollbar_y.grid()
            self._ativar_mousewheel()

    def _preparar_scroll_eventos(self):
        """Define os métodos de scroll adequados para cada SO"""
        self._os = platform.system()
        if self._os in ("Windows", "Darwin"):
            self._on_mousewheel = lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        else:
            self._on_mousewheel_linux = lambda e: self.canvas.yview_scroll(-1 if e.num == 4 else 1, "units")

    def _ativar_mousewheel(self):
        if self._scroll_ativo:
            return
        self._scroll_ativo = True

        if self._os in ("Windows", "Darwin"):
            self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        else:
            self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)
            self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)

    def _desativar_mousewheel(self):
        if not self._scroll_ativo:
            return
        self._scroll_ativo = False

        if self._os in ("Windows", "Darwin"):
            self.canvas.unbind_all("<MouseWheel>")
        else:
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
