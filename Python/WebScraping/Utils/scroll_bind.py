import tkinter as tk

def bind_scroll_mousewheel(canvas, scrollable_widget):
    def _on_mousewheel(event):
        try:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except tk.TclError:
            # O canvas foi destruído
            canvas.unbind_all("<MouseWheel>")

    def _on_enter(event):
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def _on_leave(event):
        canvas.unbind_all("<MouseWheel>")

    scrollable_widget.bind("<Enter>", _on_enter)
    scrollable_widget.bind("<Leave>", _on_leave)

    # Suporte a Linux
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
