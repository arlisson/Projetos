import tkinter as tk
from tkinter import ttk
from threading import Thread
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO


class ListagemBuscaAsync:
    def __init__(self, parent, buscar_func, render_linha_func, colunas, config=None):
        self.parent = parent
        self.buscar_func = buscar_func
        self.render_linha_func = render_linha_func
        self.colunas = colunas
        self.config = config or {}

        self.image_cache = {}
        self.busca_version = 0
        self.busca_job = None

        self._montar_ui()

    def _montar_ui(self):
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill="both", expand=True)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        # Entrada de busca
        busca_frame = ttk.Frame(self.frame)
        busca_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        busca_frame.columnconfigure(1, weight=1)

        ttk.Label(busca_frame, text="Buscar:").grid(row=0, column=0)
        self.entrada_busca = ttk.Entry(busca_frame)
        self.entrada_busca.grid(row=0, column=1, sticky="ew", padx=5)
        placeholder = self.config.get("filtro_placeholder", "Digite para buscar...")
        self.entrada_busca.insert(0, placeholder)
        self.entrada_busca.bind("<FocusIn>", lambda e: self.entrada_busca.delete(0, tk.END))
        self.entrada_busca.bind("<KeyRelease>", self._on_key_release)

        # Scrollable Frame
        main_frame = ttk.Frame(self.frame)
        main_frame.grid(row=1, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(main_frame)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar_y = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        scrollbar_y.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(yscrollcommand=scrollbar_y.set)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self._ajustar_largura_canvas)

        self._desenhar_cabecalho()
        self._iniciar_busca()

    def _ajustar_largura_canvas(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _desenhar_cabecalho(self):
        for col, header in enumerate(self.colunas):
            ttk.Label(
                self.scrollable_frame, text=header, font=("Segoe UI", 10, "bold"),
                borderwidth=1, relief="solid", padding=5
            ).grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
            self.scrollable_frame.columnconfigure(col, weight=1)

    def _on_key_release(self, event):
        if self.busca_job:
            self.frame.after_cancel(self.busca_job)
        self.busca_job = self.frame.after(self.config.get("debounce", 300), self._iniciar_busca)

    def _iniciar_busca(self):
        termo = self.entrada_busca.get().strip()
        self.busca_version += 1
        version = self.busca_version

        def worker():
            try:
                resultados = self.buscar_func(termo)
            except Exception as e:
                resultados = []
            self.frame.after(0, lambda: self._render_resultados(resultados, version))

        Thread(target=worker, daemon=True).start()

    def _limpar_tabela(self):
        for widget in self.scrollable_frame.winfo_children():
            if int(widget.grid_info().get("row", 0)) > 0:
                widget.destroy()

    def _render_resultados(self, itens, version):
        if version != self.busca_version:
            return

        self._limpar_tabela()
        if not itens:
            ttk.Label(self.scrollable_frame, text="Nenhum item encontrado.",
                      font=("Segoe UI", 10, "italic"), foreground="gray"
                      ).grid(row=1, column=0, columnspan=len(self.colunas), pady=20)
            return

        chunk_size = self.config.get("chunk", 50)

        def render_chunk(start):
            if version != self.busca_version:
                return
            end = min(start + chunk_size, len(itens))
            for idx, item in enumerate(itens[start:end], start=start):
                self.render_linha_func(self.scrollable_frame, item, idx + 1, self._carregar_imagem)
            if end < len(itens):
                self.frame.after(1, lambda: render_chunk(end))

        render_chunk(0)

    def _carregar_imagem(self, url, tamanho=(80, 112)):
        if not url:
            return None

        if url in self.image_cache:
            return self.image_cache[url]

        try:
            with urllib.request.urlopen(url, timeout=5) as u:
                raw_data = u.read()
            im = Image.open(BytesIO(raw_data))
            im.thumbnail(tamanho)
            photo = ImageTk.PhotoImage(im)
            self.image_cache[url] = photo
            return photo
        except Exception:
            return None
