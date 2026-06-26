"""
Auto-desenho no Microsoft Paint (ou qualquer app) usando mouse.

Modo de desenho: "impressora" (varredura por linhas / raster scan).
Isso reduz drasticamente riscos indesejados, pois o mouse só fica pressionado
durante segmentos horizontais onde há pixels a desenhar.

GUI (Tkinter) com:
- URL da imagem
- Velocidade (1 a 10)
- Botão "Definir largura" (define a ÁREA de desenho com 2 cliques)
- Botão "Desenhar" (desenha com a cor/ferramenta já selecionadas no Paint)

Como usar (resumo):
1) Abra o Paint e selecione a cor + ferramenta (lápis/pincel) manualmente.
2) Rode este script.
3) Cole a URL da imagem.
4) Ajuste a velocidade (1=mais lento, 10=mais rápido).
5) Clique "Definir largura" e então clique 2x na tela:
   - 1º clique: canto superior esquerdo da área de desenho
   - 2º clique: canto inferior direito da área de desenho
6) Volte ao Paint (deixe a área em foco) e clique "Desenhar".

Cancelamento:
- Tecla ESC cancela o desenho.
- PyAutoGUI FailSafe: mover o mouse para o canto superior esquerdo também aborta.

Dependências:
pip install requests pillow numpy opencv-python pyautogui pynput
"""

import io
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox

import requests
import numpy as np
from PIL import Image
import cv2

import pyautogui
from pynput import mouse, keyboard

pyautogui.FAILSAFE = True


class PaintAutoDrawerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Auto-Desenho (Paint) — Modo Impressora")

        # Estado
        self.area = None  # (x1, y1, x2, y2)
        self._click_points = []
        self._listener = None
        self._busy = False

        self.cancel_event = threading.Event()
        self._kbd_listener = None

        # UI
        main = ttk.Frame(root, padding=12)
        main.grid(row=0, column=0, sticky="nsew")

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)

        ttk.Label(main, text="Link da imagem:").grid(row=0, column=0, sticky="w", pady=4)
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(main, textvariable=self.url_var)
        self.url_entry.grid(row=0, column=1, sticky="ew", pady=4)

        ttk.Label(main, text="Velocidade (1–10):").grid(row=1, column=0, sticky="w", pady=4)
        self.speed_var = tk.StringVar(value="7")
        self.speed_entry = ttk.Entry(main, textvariable=self.speed_var, width=8)
        self.speed_entry.grid(row=1, column=1, sticky="w", pady=4)

        btns = ttk.Frame(main)
        btns.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 6))
        btns.columnconfigure(0, weight=1)
        btns.columnconfigure(1, weight=1)

        self.btn_define = ttk.Button(btns, text="Definir largura", command=self.define_area)
        self.btn_define.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        self.btn_draw = ttk.Button(btns, text="Desenhar", command=self.draw)
        self.btn_draw.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        self.status_var = tk.StringVar(value="Pronto. Defina a área e informe a URL.")
        ttk.Label(main, textvariable=self.status_var).grid(row=3, column=0, columnspan=2, sticky="w", pady=(6, 0))

        tip = (
            "Dicas:\n"
            "- Selecione cor e ferramenta no Paint manualmente (este script não altera cor).\n"
            "- ESC cancela o desenho.\n"
            "- FailSafe: mover o mouse para o canto superior esquerdo também aborta.\n"
            "- Velocidade alta pode perder precisão, dependendo do PC."
        )
        ttk.Label(main, text=tip, justify="left").grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 0))

    def set_status(self, text: str):
        self.status_var.set(text)
        self.root.update_idletasks()

    def _set_busy(self, busy: bool):
        self._busy = busy
        state = "disabled" if busy else "normal"
        self.btn_define.config(state=state)
        self.btn_draw.config(state=state)

    def define_area(self):
        if self._busy:
            return

        self._click_points = []
        self.set_status("Clique 2x na tela para delimitar a área: 1) canto sup-esq 2) canto inf-dir")

        def _listen():
            try:
                self._listener = mouse.Listener(on_click=self._on_global_click)
                self._listener.start()
                self._listener.join()
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Erro", f"Falha ao capturar cliques: {e}"))

        threading.Thread(target=_listen, daemon=True).start()

    def _on_global_click(self, x, y, button, pressed):
        if not pressed:
            return

        self._click_points.append((x, y))
        if len(self._click_points) == 1:
            self.root.after(0, lambda: self.set_status(f"1º ponto capturado: ({x}, {y}). Agora clique o 2º ponto."))
        elif len(self._click_points) >= 2:
            (x1, y1), (x2, y2) = self._click_points[0], self._click_points[1]
            left = min(x1, x2)
            top = min(y1, y2)
            right = max(x1, x2)
            bottom = max(y1, y2)

            if (right - left) < 50 or (bottom - top) < 50:
                self._click_points = []
                self.root.after(0, lambda: self.set_status("Área muito pequena. Clique novamente 2 pontos bem separados."))
                return

            self.area = (left, top, right, bottom)
            self.root.after(
                0,
                lambda: self.set_status(
                    f"Área definida: ({left}, {top}) -> ({right}, {bottom}). Abra/focalize o Paint e clique 'Desenhar'."
                ),
            )

            try:
                if self._listener:
                    self._listener.stop()
            except Exception:
                pass

            return False

    def _parse_speed(self) -> int:
        try:
            v = int(self.speed_var.get().strip())
        except Exception:
            raise ValueError("Velocidade inválida. Use um inteiro de 1 a 10.")
        if v < 1 or v > 10:
            raise ValueError("Velocidade fora do intervalo. Use 1 a 10.")
        return v

    def _download_image_safe(self, url: str) -> Image.Image:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        return Image.open(io.BytesIO(r.content)).convert("RGB")

    def _image_to_mask(self, pil_img: Image.Image, out_w: int, out_h: int) -> np.ndarray:
        """
        Gera máscara binária (0/255) para desenhar em modo "impressora".
        Usa Canny + dilatação leve para produzir linhas desenháveis.
        """
        img = pil_img.copy()
        img.thumbnail((out_w, out_h), Image.Resampling.LANCZOS)

        canvas = Image.new("RGB", (out_w, out_h), (255, 255, 255))
        ox = (out_w - img.width) // 2
        oy = (out_h - img.height) // 2
        canvas.paste(img, (ox, oy))

        arr = np.array(canvas)
        gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        edges = cv2.Canny(gray, 60, 160)

        # Engrossa um pouco para melhorar continuidade no Paint
        edges = cv2.dilate(edges, np.ones((2, 2), np.uint8), iterations=1)

        return edges  # 0/255

    def draw(self):
        if self._busy:
            return

        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Atenção", "Informe o link (URL) da imagem.")
            return
        if not self.area:
            messagebox.showwarning("Atenção", "Defina a área de desenho com 'Definir largura' antes de desenhar.")
            return

        try:
            speed = self._parse_speed()
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            return

        def _run():
            self.root.after(0, lambda: self._set_busy(True))
            self.cancel_event.clear()

            def _on_key_press(key):
                if key == keyboard.Key.esc:
                    self.cancel_event.set()
                    return False

            self._kbd_listener = keyboard.Listener(on_press=_on_key_press)
            self._kbd_listener.start()

            try:
                self.root.after(0, lambda: self.set_status("Baixando imagem..."))
                img = self._download_image_safe(url)

                left, top, right, bottom = self.area
                w = right - left
                h = bottom - top

                margin = 8
                draw_w = max(10, w - 2 * margin)
                draw_h = max(10, h - 2 * margin)

                self.root.after(0, lambda: self.set_status("Processando (modo impressora)..."))
                mask = self._image_to_mask(img, draw_w, draw_h)

                # Velocidade -> parâmetros
                # move_duration controla a velocidade dos arrastos
                move_duration = float(np.interp(speed, [1, 10], [0.02, 0.0]))
                # ROW_STEP: maior = mais rápido, menos detalhado
                row_step = int(np.interp(speed, [1, 10], [1, 3]))
                row_step = max(1, min(3, row_step))

                # Pequenas pausas ajudam o Paint a não "perder" eventos
                pyautogui.PAUSE = float(np.interp(speed, [1, 10], [0.01, 0.0]))

                # Limiar para considerar pixel "ligado"
                pixel_on = 128

                self.root.after(
                    0,
                    lambda: self.set_status(
                        f"Pronto. Focalize o Paint em até 3s... (row_step={row_step})"
                    ),
                )
                time.sleep(3)

                if self.cancel_event.is_set():
                    self.root.after(0, lambda: self.set_status("Cancelado (ESC)."))
                    return

                base_x = left + margin
                base_y = top + margin

                # Segurança: garante mouse solto antes de iniciar
                pyautogui.mouseUp()
                time.sleep(0.05)

                H, W = mask.shape[:2]
                total_rows = (H + row_step - 1) // row_step
                done_rows = 0

                # Parâmetro: ignora segmentos muito curtos (reduz ruído)
                min_run_len = 2

                for y in range(0, H, row_step):
                    if self.cancel_event.is_set():
                        pyautogui.mouseUp()
                        self.root.after(0, lambda: self.set_status("Cancelado (ESC)."))
                        return

                    row = mask[y, :]

                    # Varredura serpentina (vai e volta) reduz deslocamentos
                    if (done_rows % 2) == 0:
                        xs = range(0, W, 1)
                    else:
                        xs = range(W - 1, -1, -1)

                    in_run = False
                    run_start = None
                    last_x = None

                    for x in xs:
                        on = row[x] >= pixel_on

                        if on and not in_run:
                            in_run = True
                            run_start = x
                            last_x = x
                            continue

                        if in_run:
                            # detecta quebra do run:
                            # 1) pixel desligou, ou
                            # 2) não contíguo (pula por causa do sentido/step)
                            expected_next = last_x + (1 if xs.step == 1 else -1)
                            non_contiguous = (x != expected_next)

                            if (not on) or non_contiguous:
                                run_end = last_x
                                in_run = False

                                x1, x2 = run_start, run_end
                                if x1 > x2:
                                    x1, x2 = x2, x1

                                if (x2 - x1) >= min_run_len:
                                    # REGRAS DE OURO:
                                    # - Sempre mouseUp antes de qualquer reposicionamento
                                    pyautogui.mouseUp()
                                    pyautogui.moveTo(base_x + x1, base_y + y, duration=0)
                                    time.sleep(0.001)
                                    pyautogui.mouseDown()
                                    pyautogui.moveTo(base_x + x2, base_y + y, duration=move_duration)
                                    pyautogui.mouseUp()

                                # se o motivo foi "non_contiguous", precisamos reavaliar o x atual
                                if on and non_contiguous:
                                    in_run = True
                                    run_start = x
                                    last_x = x
                                else:
                                    run_start = None
                                    last_x = None
                                continue

                            last_x = x

                    # fecha run se a linha terminou "ligada"
                    if in_run and run_start is not None and last_x is not None:
                        x1, x2 = run_start, last_x
                        if x1 > x2:
                            x1, x2 = x2, x1
                        if (x2 - x1) >= min_run_len:
                            pyautogui.mouseUp()
                            pyautogui.moveTo(base_x + x1, base_y + y, duration=0)
                            time.sleep(0.001)
                            pyautogui.mouseDown()
                            pyautogui.moveTo(base_x + x2, base_y + y, duration=move_duration)
                            pyautogui.mouseUp()

                    done_rows += 1
                    if done_rows % 10 == 0:
                        self.root.after(
                            0,
                            lambda dr=done_rows, tr=total_rows: self.set_status(f"Desenhando... ({dr}/{tr} linhas)")
                        )

                self.root.after(0, lambda: self.set_status("Concluído."))
            except pyautogui.FailSafeException:
                self.root.after(0, lambda: self.set_status("Abortado (FailSafe)."))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Erro", str(e)))
                self.root.after(0, lambda: self.set_status("Falha."))
            finally:
                try:
                    pyautogui.mouseUp()
                except Exception:
                    pass

                try:
                    if self._kbd_listener:
                        self._kbd_listener.stop()
                except Exception:
                    pass

                self.root.after(0, lambda: self._set_busy(False))

        threading.Thread(target=_run, daemon=True).start()


def main():
    root = tk.Tk()
    try:
        style = ttk.Style(root)
        if "vista" in style.theme_names():
            style.theme_use("vista")
    except Exception:
        pass

    PaintAutoDrawerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
