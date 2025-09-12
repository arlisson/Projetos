import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime


class GraficoHistorico(ttk.Frame):
    def __init__(self, parent, dados, titulo="Histórico", campos_numericos=["preco"], campo_data="data", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.dados = dados or []
        self.titulo = titulo
        self.campos_numericos = campos_numericos
        self.campo_data = campo_data

        self._construir_grafico()

    def _construir_grafico(self):
        if not self.dados:
            label = ttk.Label(self, text="Sem dados para exibir.", foreground="gray")
            label.pack(padx=10, pady=10)
            return

        try:
            # Tenta converter as datas para datetime
            for d in self.dados:
                d[self.campo_data] = datetime.strptime(d[self.campo_data], "%Y-%m-%d")

            fig = Figure(figsize=(6, 3), dpi=100)
            ax = fig.add_subplot(111)
            ax.set_title(self.titulo)
            ax.grid(True)

            datas = [d[self.campo_data] for d in self.dados]

            for campo in self.campos_numericos:
                valores = [d.get(campo, 0) for d in self.dados]
                ax.plot(datas, valores, label=campo.capitalize(), marker="o")

            ax.legend(loc="best")

            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        except Exception as e:
            ttk.Label(self, text=f"Erro ao exibir gráfico: {e}", foreground="red").pack(padx=10, pady=10)
