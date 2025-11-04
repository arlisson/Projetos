# View/ver_logs.py
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

ENCODINGS = ("utf-8", "latin-1", "cp1252")  # tenta na ordem

def abrir_tela_logs(app, caminho_info: str, caminho_erro: str):
    """
    Abre uma janela com 2 abas para visualizar logs .txt (info e erro).
    - Busca por texto (Enter ou botão)
    - Atualizar (reload do arquivo)
    - Auto-rolagem ao final (tail "leve")
    - Copiar tudo / Copiar seleção
    - Abrir no Explorer / Abrir em editor padrão
    - Limpar visualização (não apaga arquivo)
    """

    # ----------------- Helpers de arquivo/decodificação -----------------
    def _ler_arquivo(caminho, max_bytes=2_000_000):
        if not os.path.exists(caminho):
            return f"[Arquivo não encontrado]\n{caminho}"
        try:
            size = os.path.getsize(caminho)
            start = max(0, size - max_bytes)  # lê só o final se for muito grande
            with open(caminho, "rb") as f:
                f.seek(start)
                dados = f.read()
            for enc in ENCODINGS:
                try:
                    return dados.decode(enc, errors="replace")
                except Exception:
                    continue
            return dados.decode("utf-8", errors="replace")
        except Exception as e:
            return f"[Erro ao ler arquivo] {e}"

    def _abrir_explorer(caminho):
        try:
            if os.path.exists(caminho):
                os.system(f'explorer /select,"{os.path.abspath(caminho)}"')
            else:
                pasta = os.path.dirname(os.path.abspath(caminho)) or "."
                os.startfile(pasta)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao abrir Explorer: {e}", parent=root)

    def _abrir_editor(caminho):
        try:
            if os.path.exists(caminho):
                os.startfile(os.path.abspath(caminho))
            else:
                messagebox.showwarning("Aviso", "Arquivo não encontrado.", parent=root)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao abrir arquivo: {e}", parent=root)

    # ----------------- Classe de aba de log -----------------
    class LogTab(ttk.Frame):
        def __init__(self, parent, caminho_arquivo, titulo):
            super().__init__(parent)
            self.caminho = caminho_arquivo
            self.titulo = titulo
            self._tail_on = tk.BooleanVar(value=True)
            self._tail_interval_ms = 1200
            self._stop = False
            self._last_size = 0

            # Top bar (busca + ações)
            top = ttk.Frame(self)
            top.pack(fill="x", padx=6, pady=(6, 2))

            ttk.Label(top, text="Buscar:").pack(side="left")
            self._busca = ttk.Entry(top, width=30)
            self._busca.pack(side="left", padx=(4, 8))
            self._busca.bind("<Return>", lambda e: self.find_next())

            ttk.Button(top, text="Localizar", command=self.find_next).pack(side="left")
            ttk.Button(top, text="Atualizar", command=self.reload).pack(side="left", padx=(6, 0))
            ttk.Button(top, text="Copiar seleção", command=self.copy_sel).pack(side="left", padx=(6, 0))
            ttk.Button(top, text="Copiar tudo", command=self.copy_all).pack(side="left", padx=(6, 0))

            ttk.Separator(top, orient="vertical").pack(side="left", fill="y", padx=8)

            ttk.Button(top, text="Abrir no Explorer", command=lambda: _abrir_explorer(self.caminho)).pack(side="left")
            ttk.Button(top, text="Abrir no editor", command=lambda: _abrir_editor(self.caminho)).pack(side="left", padx=(6, 0))

            ttk.Separator(top, orient="vertical").pack(side="left", fill="y", padx=8)

            ttk.Checkbutton(top, text="Auto-rolagem", variable=self._tail_on).pack(side="left")
            ttk.Button(top, text="Ir ao fim", command=self.scroll_end).pack(side="left", padx=(6, 0))
            ttk.Button(top, text="Limpar visualização", command=self.clear_view).pack(side="right")

            # Text + Scroll
            txt_frame = ttk.Frame(self)
            txt_frame.pack(fill="both", expand=True, padx=6, pady=(0, 6))

            self.text = tk.Text(
                txt_frame, wrap="none", undo=False, state="normal",
                font=("Consolas", 10), tabs=("1c",)  # monoespaçado + tab visual
            )
            ysb = ttk.Scrollbar(txt_frame, orient="vertical", command=self.text.yview)
            xsb = ttk.Scrollbar(txt_frame, orient="horizontal", command=self.text.xview)
            self.text.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)

            self.text.grid(row=0, column=0, sticky="nsew")
            ysb.grid(row=0, column=1, sticky="ns")
            xsb.grid(row=1, column=0, sticky="ew")
            txt_frame.rowconfigure(0, weight=1)
            txt_frame.columnconfigure(0, weight=1)

            # tags de cor
            self.text.tag_configure("ERR", foreground="#b00020")    # vermelho
            self.text.tag_configure("WARN", foreground="#b8860b")   # âmbar
            self.text.tag_configure("INFO", foreground="#00695c")   # teal

            self.reload()      # carrega conteúdo inicial
            self._schedule_tail()  # inicia tail periódico

        # ------------ Ações UI ------------
        def reload(self):
            conteudo = _ler_arquivo(self.caminho)
            self.text.config(state="normal")
            self.text.delete("1.0", "end")
            self.text.insert("1.0", conteudo)
            self._apply_highlight(conteudo)
            self.text.config(state="disabled")
            self.scroll_end()
            try:
                self._last_size = os.path.getsize(self.caminho)
            except Exception:
                self._last_size = 0

        def _apply_highlight(self, conteudo: str):
            # limpa tags
            self.text.tag_remove("ERR", "1.0", "end")
            self.text.tag_remove("WARN", "1.0", "end")
            self.text.tag_remove("INFO", "1.0", "end")

            # marca linhas por prefixos comuns
            start = "1.0"
            while True:
                line_start = self.text.search("\n", start, "end")
                if not line_start:
                    line_end = "end-1c"
                    linha = self.text.get(start, line_end)
                    self._tag_line(start, line_end, linha)
                    break
                line_end = f"{line_start}"
                linha = self.text.get(start, line_end)
                self._tag_line(start, line_end, linha)
                start = f"{line_start}+1c"

        def _tag_line(self, start, end, linha: str):
            l = linha.lower()
            if "error" in l or "[error]" in l or "erro" in l:
                self.text.tag_add("ERR", start, end)
            elif "warn" in l or "[warn]" in l or "aviso" in l:
                self.text.tag_add("WARN", start, end)
            elif "info" in l or "[info]" in l:
                self.text.tag_add("INFO", start, end)

        def find_next(self):
            termo = self._busca.get().strip()
            if not termo:
                return
            self.text.tag_remove("sel", "1.0", "end")
            pos = self.text.search(termo, self.text.index("insert"), "end", nocase=True)
            if not pos:
                # volta do início
                pos = self.text.search(termo, "1.0", "end", nocase=True)
                if not pos:
                    app.bell()
                    return
            end_pos = f"{pos}+{len(termo)}c"
            self.text.tag_add("sel", pos, end_pos)
            self.text.mark_set("insert", end_pos)
            self.text.see(pos)

        def copy_sel(self):
            try:
                sel = self.text.get("sel.first", "sel.last")
            except tk.TclError:
                sel = ""
            if not sel:
                return
            self.clipboard_clear()
            self.clipboard_append(sel)

        def copy_all(self):
            tudo = self.text.get("1.0", "end-1c")
            self.clipboard_clear()
            self.clipboard_append(tudo)

        def scroll_end(self):
            self.text.see("end")

        def clear_view(self):
            self.text.config(state="normal")
            self.text.delete("1.0", "end")
            self.text.config(state="disabled")

        # ------------ Tail "leve" ------------
        def _schedule_tail(self):
            if self._stop:
                return
            root.after(self._tail_interval_ms, self._tail_tick)

        def _tail_tick(self):
            if self._stop:
                return
            try:
                size = os.path.getsize(self.caminho) if os.path.exists(self.caminho) else 0
                if size < self._last_size:
                    # arquivo rotacionado/truncado -> recarrega
                    self.reload()
                elif size > self._last_size:
                    # anexou novas linhas -> lê só o delta
                    with open(self.caminho, "rb") as f:
                        f.seek(self._last_size)
                        delta = f.read()
                    texto = None
                    for enc in ENCODINGS:
                        try:
                            texto = delta.decode(enc, errors="replace")
                            break
                        except Exception:
                            continue
                    if texto is None:
                        texto = delta.decode("utf-8", errors="replace")
                    if texto:
                        self.text.config(state="normal")
                        insert_at = self.text.index("end-1c")
                        self.text.insert("end", texto)
                        # colore apenas trecho novo
                        self._apply_highlight(self.text.get(insert_at, "end-1c"))
                        self.text.config(state="disabled")
                        if self._tail_on.get():
                            self.scroll_end()
                    self._last_size = size
            except Exception:
                # falhas silenciosas no tail (arquivo em uso etc.)
                pass
            finally:
                self._schedule_tail()

        def stop(self):
            self._stop = True

    # ----------------- Janela -----------------
    root = tk.Toplevel(app)
    root.title("Visualizador de Logs")
    root.geometry("1000x600+100+60")
    root.minsize(800, 450)
    root.grab_set()
    root.focus_force()

    # Notebook com duas abas
    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True)

    tab_info = LogTab(nb, caminho_info, "Info")
    tab_erro = LogTab(nb, caminho_erro, "Erro")

    nb.add(tab_info, text="ℹ️  Info")
    nb.add(tab_erro, text="⛔  Erro")

    def ao_fechar():
        tab_info.stop()
        tab_erro.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", ao_fechar)
    return root

# --- Execução isolada para teste ---
if __name__ == "__main__":
    dummy_app = tk.Tk()
    dummy_app.withdraw()
    # troque pelos seus caminhos reais:
    abrir_tela_logs(dummy_app, "logs/info.txt", "logs/erro.txt")
    dummy_app.mainloop()
