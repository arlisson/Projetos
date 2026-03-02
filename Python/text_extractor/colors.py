# colors.py
from __future__ import annotations

import colorsys
from typing import Tuple, Dict


DEFAULT_THEME: Dict[str, str] = {
    "background": "#0B1220",
    "surface": "#0F1A2B",
    "surface_alt": "#111F33",
    "text": "#E6EDF7",
    "muted_text": "#A7B3C6",
    "primary": "#3B82F6",
    "danger": "#EF4444",
    "border": "#1F2A44",
}


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    h = (hex_color or "").lstrip("#")
    if len(h) != 6:
        return (0, 0, 0)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))
    return f"#{r:02X}{g:02X}{b:02X}"


def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[int, int, int]:
    rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
    h, l, s = colorsys.rgb_to_hls(rf, gf, bf)
    return int(round(h * 359)), int(round(s * 100)), int(round(l * 100))


def hsl_to_rgb(h: int, s: int, l: int) -> Tuple[int, int, int]:
    hf = (h % 360) / 360.0
    sf = max(0, min(100, s)) / 100.0
    lf = max(0, min(100, l)) / 100.0
    r, g, b = colorsys.hls_to_rgb(hf, lf, sf)
    return int(round(r * 255)), int(round(g * 255)), int(round(b * 255))


def luminance(rgb: Tuple[int, int, int]) -> float:
    r, g, b = rgb
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0


def blend(a: Tuple[int, int, int], b: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
    t = max(0.0, min(1.0, t))
    return (
        int(round(a[0] * (1 - t) + b[0] * t)),
        int(round(a[1] * (1 - t) + b[1] * t)),
        int(round(a[2] * (1 - t) + b[2] * t)),
    )


def derive_theme_from_background(bg_hex: str, base_theme: dict) -> dict:
    bg_rgb = hex_to_rgb(bg_hex)
    is_dark = luminance(bg_rgb) < 0.5

    white = (255, 255, 255)
    black = (0, 0, 0)

    if is_dark:
        surface_rgb = blend(bg_rgb, white, 0.06)
        surface_alt_rgb = blend(bg_rgb, white, 0.10)
        border_rgb = blend(bg_rgb, white, 0.16)

        # Antes: text_rgb = hex_to_rgb(base_theme.get("text", "#E6EDF7"))
        # Depois: texto “puxa” um pouco a cor do fundo, mas continua claro
        text_rgb = blend(bg_rgb, white, 0.92)
    else:
        surface_rgb = blend(bg_rgb, black, 0.06)
        surface_alt_rgb = blend(bg_rgb, black, 0.10)
        border_rgb = blend(bg_rgb, black, 0.16)

        # texto escuro, também pode variar um pouco com o fundo
        text_rgb = blend(bg_rgb, black, 0.92)

    muted_rgb = blend(text_rgb, border_rgb, 0.55)

    out = dict(base_theme)
    out["background"] = bg_hex
    out["surface"] = rgb_to_hex(*surface_rgb)
    out["surface_alt"] = rgb_to_hex(*surface_alt_rgb)
    out["border"] = rgb_to_hex(*border_rgb)
    out["text"] = rgb_to_hex(*text_rgb)
    out["muted_text"] = rgb_to_hex(*muted_rgb)
    return out