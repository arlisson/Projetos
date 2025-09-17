import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from matplotlib.dates import date2num

from Utils.log import registrar_erro


class GraficoHistorico(ttk.Frame):
    def __init__(
        self,
        parent,
        dados,
        titulo="Histórico de Preço da Carta",
        campos_numericos=("preco",),
        campo_data="data",
        formato_tick="%Y-%m-%d",
        *args, **kwargs
    ):
        super().__init__(parent, *args, **kwargs)
        self.dados_brutos = dados or []
        self.titulo = titulo
        self.campos_numericos = list(campos_numericos)
        self.campo_data = campo_data
        self.formato_tick = formato_tick

        self.filtro_dias = tk.IntVar(value=30)  # padrão: 30 dias

        self._criar_filtros()
        self._construir_grafico()

    def _criar_filtros(self):
        frame_filtro = ttk.Frame(self)
        frame_filtro.pack(pady=(0, 6))

        ttk.Label(frame_filtro, text="Exibir últimos:").pack(side="left")

        opcoes = [
            ("7 dias", 7),
            ("15 dias", 15),
            ("1 mês", 30),
            ("3 meses", 90),
            ("6 meses", 180),
            ("1 ano", 365),
            ("Tudo", 0)
        ]

        for texto, dias in opcoes:
            ttk.Radiobutton(
                frame_filtro,
                text=texto,
                variable=self.filtro_dias,
                value=dias,
                command=self._construir_grafico
            ).pack(side="left", padx=4)

    def _conv_data(self, v):
        if isinstance(v, datetime):
            return v
        v = str(v).strip()
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(v, fmt)
            except ValueError:
                continue
        registrar_erro(f"Formato de data inválido: {v}")
        raise ValueError(f"Formato de data inválido: {v}")

    def _filtrar_dados(self):
        dados = []
        try:
            dias = self.filtro_dias.get()
            data_limite = datetime.now() - timedelta(days=dias) if dias > 0 else None
            for d in self.dados_brutos:
                d = d.copy()
                d[self.campo_data] = self._conv_data(d[self.campo_data])
                if not data_limite or d[self.campo_data] >= data_limite:
                    dados.append(d)
        except Exception as e:
            registrar_erro(f"Erro ao filtrar dados: {e}")
        return dados

    def _construir_grafico(self):
        # Remove todos os widgets filhos exceto o frame de filtro (índice 0)
        for widget in self.winfo_children()[1:]:
            widget.destroy()


        dados = self._filtrar_dados()
        if not dados:
            ttk.Label(self, text="Sem dados para exibir.", foreground="gray").pack(padx=10, pady=10)
            return

        try:
            fig = Figure(figsize=(6, 3), dpi=100)
            ax = fig.add_subplot(111)
            ax.set_title(self.titulo)
            ax.grid(True)

            self._canvas = FigureCanvasTkAgg(fig, master=self)
            self._canvas.draw()
            self._canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
            


            todas_as_datas_plotadas = set()
            self._pontos_plotados = []

            for campo in self.campos_numericos:
                pontos_validos = []
                for d in dados:
                    v = d.get(campo)
                    if v in (None, "", 0):
                        continue
                    try:
                        v = float(v)
                    except Exception:
                        continue
                    pontos_validos.append((d[self.campo_data], v))

                if not pontos_validos:
                    continue

                pontos_validos.sort(key=lambda p: p[0])
                datas, valores = zip(*pontos_validos)
                ax.plot(datas, valores, label=campo.capitalize(), marker="o")
                self._pontos_plotados.extend([(date2num(x), y, f"{campo.capitalize()}: R$ {y:.2f}\n{x.strftime('%d/%m/%Y')}") for x, y in zip(datas, valores)])
                todas_as_datas_plotadas.update(datas)

            if not todas_as_datas_plotadas:
                ttk.Label(self, text="Sem pontos válidos para exibir.", foreground="gray").pack(padx=10, pady=10)
                return

            xticks = sorted(todas_as_datas_plotadas)
            ax.set_xticks(xticks)
            ax.xaxis.set_major_formatter(mdates.DateFormatter(self.formato_tick))
            ax.tick_params(axis='x', rotation=45)
            fig.subplots_adjust(bottom=0.3)
            ax.margins(x=0.1)
            ax.legend(loc="best")
            self._canvas.draw()

            self._tooltip = fig.text(
                0.5, 0.95, "", ha="center", va="bottom",
                fontsize=9, color="black",
                bbox=dict(boxstyle="round", fc="lightyellow", ec="gray", lw=1)
            )
            self._tooltip.set_visible(False)

            def on_hover(event):
                vis = False
                if event.inaxes == ax and event.xdata and event.ydata:
                    for x, y, label in self._pontos_plotados:
                        if abs(x - event.xdata) < 0.2 and abs(y - event.ydata) < 0.5:
                            fig_x = event.x / self._canvas.get_tk_widget().winfo_width()
                            fig_y = 1 - (event.y / self._canvas.get_tk_widget().winfo_height())
                            self._tooltip.set_position((fig_x, fig_y))
                            self._tooltip.set_text(label)
                            self._tooltip.set_visible(True)
                            vis = True
                            break
                if not vis:
                    self._tooltip.set_visible(False)
                self._canvas.draw_idle()

            self._canvas.mpl_connect("motion_notify_event", on_hover)

            min_x = date2num(min(xticks))
            max_x = date2num(max(xticks))
            range_x = max_x - min_x

            span = range_x * 0.8
            ax.set_xlim(max_x - span, max_x)


            self._dragging = False
            self._last_mouse_x = None

            def on_press(event):
                if event.button == 1 and event.inaxes == ax:
                    self._dragging = True
                    self._last_mouse_x = event.xdata

            def on_release(event):
                if event.button == 1:
                    self._dragging = False
                    self._last_mouse_x = None

            def on_motion(event):
                on_hover(event)
                if self._dragging and event.inaxes == ax and self._last_mouse_x and event.xdata:
                    dx = self._last_mouse_x - event.xdata
                    cur_xlim = ax.get_xlim()
                    new_xlim = cur_xlim[0] + dx, cur_xlim[1] + dx

                    span = new_xlim[1] - new_xlim[0]
                    if new_xlim[0] < min_x:
                        new_xlim = (min_x, min_x + span)
                    elif new_xlim[1] > max_x:
                        new_xlim = (max_x - span, max_x)

                    ax.set_xlim(new_xlim)
                    self._canvas.draw()
                    self._last_mouse_x = event.xdata

            self._canvas.mpl_connect("button_press_event", on_press)
            self._canvas.mpl_connect("button_release_event", on_release)
            self._canvas.mpl_connect("motion_notify_event", on_motion)

            ax.set_facecolor("white")
            fig.patch.set_facecolor("none")

        except Exception as e:
            ttk.Label(self, text=f"Erro ao exibir gráfico: {e}", foreground="red").pack(padx=10, pady=10)
            registrar_erro(f"Erro ao construir gráfico: {e}")