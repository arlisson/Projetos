import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import urllib.request
from io import BytesIO
from Utils.log import registrar_erro
import platform
import tkinter.font as tkFont

# cache global de imagens
_image_cache = {}


def _medir_tamanho_texto(texto: str, fonte: ImageFont.ImageFont):
    """Retorna (largura, altura) do texto para a fonte informada usando textbbox."""
    tmp = Image.new("RGB", (1, 1), "white")
    draw = ImageDraw.Draw(tmp)
    x0, y0, x1, y1 = draw.textbbox((0, 0), texto, font=fonte)
    return (x1 - x0, y1 - y0)


def carregar_imagem(caminho, largura=80, altura=112, texto_abaixo=None):
    """
    Carrega imagem de um caminho local ou URL, redimensiona
    e adiciona texto opcional abaixo dela (ex: raridade).
    """
    chave_cache = (caminho, largura, altura, texto_abaixo)
    if chave_cache in _image_cache:
        return _image_cache[chave_cache]

    # abre e redimensiona a imagem base
    try:
        if caminho and caminho.startswith("http"):
            with urllib.request.urlopen(caminho) as u:
                raw_data = u.read()
            im = Image.open(BytesIO(raw_data))
        elif caminho:
            im = Image.open(caminho)
        else:
            im = Image.new("RGB", (largura, altura), "gray")
        im = im.resize((largura, altura))
    except Exception as e:
        registrar_erro(f"[Erro imagem] {e}")
        im = Image.new("RGB", (largura, altura), "gray")

    # adiciona texto abaixo, se houver
    if texto_abaixo:
        fonte = ImageFont.load_default()
        w_texto, h_texto = _medir_tamanho_texto(texto_abaixo, fonte)
        nova_altura = altura + h_texto + 6
        canvas = Image.new("RGB", (largura, nova_altura), "white")
        canvas.paste(im, (0, 0))
        draw = ImageDraw.Draw(canvas)
        x = (largura - w_texto) // 2
        y = altura + 2
        draw.text((x, y), texto_abaixo, font=fonte, fill="black")
        im = canvas

    photo = ImageTk.PhotoImage(im)
    _image_cache[chave_cache] = photo
    return photo


class ListagemTreeview(ttk.Frame):
    """
    Componente genérico de listagem em Treeview:
    - Busca com debounce
    - Imagem com texto abaixo
    - Hover nas linhas
    - Zebra stripes
    - Lazy loading (10 por vez)
    - Ajuste automático de largura de colunas
    - Ordenação clicando no cabeçalho
    """

    def __init__(self, parent, headers, fetch_func, on_edit, row_formatter=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.headers = headers
        self.fetch_func = fetch_func
        self.on_edit = on_edit
        self.row_formatter = row_formatter

        # dimensões da coluna da imagem
        self.img_w = 80
        self.img_h = 112
        self._calc_rowheight()

        # estado
        self.busca_timeout = None
        self.result_cache = []
        self.pagina = 0
        self.itens_por_pagina = 10  # lazy loading
        self._hovered_item = None
        self._sort_state = {}  # controle de ordenação por coluna

        # fontes para medir texto
        self._font = tkFont.nametofont("TkDefaultFont")
        self._col_widths = {col: self._font.measure(col) + 30 for col in self.headers}

        self._criar_widgets()
        self._ativar_mousewheel()

        # remove binds ao destruir
        self.bind("<Destroy>", self._on_destroy, add="+")

    # ----------------------------------------------------------------------

    def _calc_rowheight(self):
        """Calcula a altura mínima da linha considerando imagem + texto abaixo."""
        fonte = ImageFont.load_default()
        _, h_texto = _medir_tamanho_texto("Ag", fonte)
        self.rowheight = self.img_h + h_texto + 8

    def _criar_widgets(self):
        # campo de busca
        busca_frame = ttk.Frame(self)
        busca_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.columnconfigure(0, weight=1)

        ttk.Label(busca_frame, text="Buscar:").pack(side="left")
        self.entrada_busca = ttk.Entry(busca_frame)
        self.entrada_busca.pack(side="left", fill="x", expand=True, padx=5)
        self.entrada_busca.bind("<KeyRelease>", self._on_busca)

        # estilo
        style = ttk.Style()
        style.configure("Treeview", rowheight=self.rowheight)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        # container tabela
        container = ttk.Frame(self)
        container.grid(row=1, column=0, sticky="nsew")
        self.rowconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.vsb = ttk.Scrollbar(container, orient="vertical")
        self.hsb = ttk.Scrollbar(container, orient="horizontal")

        self.tree = ttk.Treeview(
            container,
            columns=self.headers,
            show="tree headings",
            yscrollcommand=self.vsb.set,
            xscrollcommand=self.hsb.set,
        )
        self.tree.column("#0", width=self.img_w + 20, anchor="center", stretch=False)
        self.tree.heading("#0", text="Imagem")

        for col in self.headers:
            largura_inicial = self._col_widths[col]
            self.tree.column(col, anchor="center", width=largura_inicial, stretch=True)
            self.tree.heading(col, text=col, command=lambda c=col: self._ordenar_por_coluna(c))

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.vsb.grid(row=0, column=1, sticky="ns")
        self.hsb.grid(row=1, column=0, sticky="ew")

        self.vsb.config(command=lambda *args: self._yview_and_check(*args))
        self.hsb.config(command=self.tree.xview)

        # zebra + hover
        self.tree.tag_configure("oddrow", background="#f9f9f9")
        self.tree.tag_configure("evenrow", background="#ffffff")
        self.tree.tag_configure("hover", background="#e0e0e0")

        # eventos
        self.tree.bind("<Button-1>", self._on_click)
        self.tree.bind("<Motion>", self._on_hover)
        self.tree.bind("<Leave>", self._on_leave)

    # ----------------------------------------------------------------------

    def _ordenar_por_coluna(self, col, reverse=None):
        """
        Ordena os itens pela coluna clicada e adiciona um indicador ▲ ▼ no cabeçalho.
        """
        dados = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]

        # tenta converter para número (se possível)
        def try_num(val):
            try:
                return float(str(val).replace("R$", "").replace(",", ".").strip())
            except Exception:
                return str(val).lower()

        # define direção (default = asc)
        current_state = self._sort_state.get(col, False)
        if reverse is None:
            reverse = current_state

        dados.sort(key=lambda t: try_num(t[0]), reverse=reverse)

        # reordena no treeview
        for index, (val, k) in enumerate(dados):
            self.tree.move(k, "", index)

        # atualiza estado da coluna
        self._sort_state[col] = not reverse

        # limpa títulos de todas as colunas
        for c in self.headers:
            self.tree.heading(c, text=c, command=lambda col=c: self._ordenar_por_coluna(col))

        # adiciona seta na coluna clicada
        seta = "▲" if not reverse else "▼"
        self.tree.heading(col, text=f"{col} {seta}", command=lambda c=col: self._ordenar_por_coluna(c, not reverse))


    def _yview_and_check(self, *args):
        """Scroll + verifica se deve carregar mais conteúdo."""
        self.tree.yview(*args)
        self._check_lazyload()

    def _check_lazyload(self):
        first, last = self.tree.yview()
        if last >= 0.95:
            self._carregar_pagina()

    def _on_busca(self, event):
        if self.busca_timeout:
            self.after_cancel(self.busca_timeout)
        filtro = self.entrada_busca.get().strip()
        self.busca_timeout = self.after(400, lambda: self.carregar(filtro))

    def _on_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if item_id and self.on_edit:
            self.on_edit(item_id)

    def _on_hover(self, event):
        item = self.tree.identify_row(event.y)
        if item != self._hovered_item:
            if self._hovered_item:
                base_tag = "evenrow" if int(self.tree.index(self._hovered_item)) % 2 == 0 else "oddrow"
                self.tree.item(self._hovered_item, tags=(base_tag,))
            if item:
                self.tree.item(item, tags=("hover",))
                self._hovered_item = item

    def _on_leave(self, event):
        if self._hovered_item:
            base_tag = "evenrow" if int(self.tree.index(self._hovered_item)) % 2 == 0 else "oddrow"
            self.tree.item(self._hovered_item, tags=(base_tag,))
            self._hovered_item = None

    def _on_destroy(self, event):
        """Remove binds globais ao destruir para evitar TclError."""
        try:
            self.tree.unbind_all("<MouseWheel>")
            self.tree.unbind_all("<Button-4>")
            self.tree.unbind_all("<Button-5>")
        except Exception:
            pass

    # ----------------------------------------------------------------------
    def carregar(self, filtro=""):
        """Carrega os dados aplicando filtro e reinicia a paginação."""
        self.result_cache = self.fetch_func(filtro)
        self.pagina = 0
        self.tree.delete(*self.tree.get_children())

        if not self.result_cache:
            # Esconde colunas temporariamente
            for col in self.headers:
                self.tree.column(col, width=0, stretch=False)

            # Ajusta a coluna de imagem para ocupar toda a largura
            total_largura = sum(self._col_widths.values()) + self.img_w + 40
            self.tree.column("#0", width=total_largura, anchor="center", stretch=True,)
           
            self.tree.insert(
                "", "end",
                text="Nenhum dado encontrado",
                values=[],
                tags=("empty",)                
            )
            self.tree['show'] = ''  # esconde cabeçalhos
            return

        # Caso tenha dados, restaura colunas
        for col in self.headers:
            self.tree.column(col, width=self._col_widths[col], stretch=True)

        self.tree.column("#0", width=self.img_w + 20, anchor="center", stretch=False)

        self._carregar_pagina()




    def _carregar_pagina(self):
        """Carrega a próxima página de itens (lazy loading)."""
        inicio = self.pagina * self.itens_por_pagina
        fim = inicio + self.itens_por_pagina
        subset = self.result_cache[inicio:fim]

        if not subset:
            return

        for item in subset:
            if self.row_formatter:
                result = self.row_formatter(item)
                if len(result) == 3:
                    valores, iid, texto_imagem = result
                else:
                    valores, iid = result
                    texto_imagem = ""
            else:
                valores = [item.get(col, "") for col in self.headers]
                iid = item.get("id")
                texto_imagem = ""

            img = carregar_imagem(
                item.get("imagem_salva") or item.get("imagem"),
                largura=self.img_w,
                altura=self.img_h,
                texto_abaixo=texto_imagem if texto_imagem else None
            )

            # Ajuste automático da largura da coluna
            for col, valor in zip(self.headers, valores):
                largura_texto = self._font.measure(str(valor)) + 20
                if largura_texto > self._col_widths[col]:
                    self._col_widths[col] = largura_texto
                    self.tree.column(col, width=largura_texto)

            tag = "evenrow" if len(self.tree.get_children()) % 2 == 0 else "oddrow"
            self.tree.insert("", "end", image=img, values=valores, iid=iid, tags=(tag,))

        self.pagina += 1

    # ----------------------------------------------------------------------

    def _ativar_mousewheel(self):
        os = platform.system()
        if os in ("Windows", "Darwin"):
            self.tree.bind_all("<MouseWheel>", lambda e: (self.tree.yview_scroll(int(-1 * (e.delta / 120)), "units"), self._check_lazyload()))
        else:  # Linux
            self.tree.bind_all("<Button-4>", lambda e: (self.tree.yview_scroll(-1, "units"), self._check_lazyload()))
            self.tree.bind_all("<Button-5>", lambda e: (self.tree.yview_scroll(1, "units"), self._check_lazyload()))
