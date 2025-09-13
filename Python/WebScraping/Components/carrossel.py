# Components/carrossel.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from DAO.database import buscar_todas_cartas, listar_todos_produtos


def carregar_itens_do_banco():
    itens = []

    # Cartas
    for carta in buscar_todas_cartas() or []:
        itens.append({
            "nome": carta.get("nome", "Carta"),
            "preco": carta.get("preco_atual", 0.0) or 0.0,
            "imagem": carta.get("imagem_salva") or carta.get("imagem") or ""
        })

    # Produtos
    for prod in listar_todos_produtos() or []:
        itens.append({
            "nome": prod.get("nome_produto", "Produto"),
            "preco": prod.get("preco_atual", 0.0) or 0.0,
            "imagem": prod.get("imagem_salva") or prod.get("imagem") or ""
        })

    return itens


class CarrosselLateral(ttk.Frame):
    def __init__(
        self,
        parent,
        itens,
        imagens_visiveis=3,
        largura=150,
        altura=200,
        intervalo=3000,
        travar_largura_visivel=True,
        *args, **kwargs
    ):
        super().__init__(parent, *args, **kwargs)

        self.largura = int(largura)
        self.altura = int(altura)
        self.intervalo = int(intervalo)
        self.imagens_visiveis = max(1, imagens_visiveis)
        self.travar_largura_visivel = bool(travar_largura_visivel)
        self._indice = 0
        self._imagens_cache = []
        self._item_px = None
        self._gap = 24  # espaço “entre” itens

        self.itens = list(itens or [])
        # Se poucos itens, duplicar para manter a rotação fluida e “bordas”
        if 0 < len(self.itens) < (self.imagens_visiveis + 2):
            reps = (self.imagens_visiveis + 2) // len(self.itens) + 1
            self.itens = self.itens * reps

        # Canvas: mostramos só N itens — as laterais ficam cortadas
        altura_canvas = self.altura + 68  # espaço para texto
        self.canvas = tk.Canvas(self, height=altura_canvas, bg="white", highlightthickness=0)

        if self.travar_largura_visivel:
            # mostra N inteiros + sobra nas laterais
            largura_visivel = (self.imagens_visiveis - 1) * (self.largura + self._gap) + int(self.largura * 1.2)
            self.canvas.config(width=largura_visivel)

        self.canvas.pack(pady=5)  # sem fill="x"


        # Frame que contém os itens
        self.frame_itens = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window(0, 0, window=self.frame_itens, anchor="nw")

        # Criar os itens (um ao lado do outro)
        self._labels = []
        for i in range(len(self.itens)):
            frame_item = ttk.Frame(self.frame_itens, padding=6, relief="ridge")
            frame_item.grid(row=0, column=i, padx=(self._gap // 2), pady=10, sticky="n")

            lbl_img = ttk.Label(frame_item)
            lbl_img.pack()

            lbl_txt = ttk.Label(frame_item, text="", font=("Segoe UI", 9), justify="center", width=22)
            lbl_txt.pack(pady=(6, 0))

            self._labels.append((lbl_img, lbl_txt))

        if self.itens:
            self._atualizar()        # carrega imagens e textos
            self._medir_item_px()    # mede largura real de um “card”
            self._reposicionar()     # posiciona no índice inicial
            self.after(self.intervalo, self._rotacionar)
        else:
            ttk.Label(self, text="Nenhum item encontrado.", foreground="gray").pack(pady=20)

    # -------- utilidades internas --------

    def _carregar_imagem(self, caminho):
        try:
            if caminho:
                img = Image.open(caminho)
                img.thumbnail((self.largura, self.altura))
            else:
                raise FileNotFoundError
        except Exception:
            img = Image.new("RGB", (self.largura, self.altura), "gray")
        return ImageTk.PhotoImage(img)

    def _atualizar(self):
        # manter referência aos PhotoImage
        self._imagens_cache.clear()
        for i, item in enumerate(self.itens):
            foto = self._carregar_imagem(item.get("imagem"))
            self._imagens_cache.append(foto)
            self._labels[i][0].configure(image=foto)
            self._labels[i][1].configure(text=f"{item.get('nome', 'Item')}\nR$ {float(item.get('preco', 0.0)):.2f}")

        self.update_idletasks()

    def _medir_item_px(self):
        # mede a largura real do primeiro card (incluindo padding/borda)
        try:
            primeiro = self.frame_itens.winfo_children()[0]
            self.update_idletasks()
            w = primeiro.winfo_width()
            # soma o gap entre colunas (aprox.) para deslocamento ficar “card a card”
            self._item_px = max(1, w + self._gap)
        except Exception:
            self._item_px = self.largura + self._gap
        return self._item_px

    def _reposicionar(self):
        if not self._item_px:
            self._medir_item_px()
        offset_px = self._indice * self._item_px
        # move a janela do frame para a esquerda em pixels → cria o “corte” lateral
        self.canvas.coords(self.canvas_window, -offset_px, 0)

    def _rotacionar(self):
        if not self.itens:
            return
        self._indice = (self._indice + 1) % len(self.itens)
        self._reposicionar()
        self.after(self.intervalo, self._rotacionar)


# Debug manual:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Carrossel lateral (debug)")

    itens = carregar_itens_do_banco()
    carrossel = CarrosselLateral(root, itens, imagens_visiveis=3, intervalo=2000)
    carrossel.pack(pady=20)

    root.mainloop()
