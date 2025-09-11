import tkinter as tk
from tkinter import ttk
import platform


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.canvas = tk.Canvas(self)
        scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)

        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self._bind_mousewheel()

    def _bind_mousewheel(self):
        os_name = platform.system()

        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _on_mousewheel_linux(event):
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")

        if os_name == "Windows" or os_name == "Darwin":
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        else:
            self.canvas.bind_all("<Button-4>", _on_mousewheel_linux)
            self.canvas.bind_all("<Button-5>", _on_mousewheel_linux)
