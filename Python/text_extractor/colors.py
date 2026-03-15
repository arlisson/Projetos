# colors.py
from __future__ import annotations

import colorsys
from typing import Dict, Tuple

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
    """Convert a hexadecimal color string to an RGB tuple.

    Accepts strings in the form ``#RRGGBB`` or ``RRGGBB``. If the input is not a
    6-digit hex color, returns ``(0, 0, 0)``.

    Args:
        hex_color: Hex color string.

    Returns:
        A tuple ``(r, g, b)`` with values in the range 0..255.
    """
    h = (hex_color or "").lstrip("#")
    if len(h) != 6:
        return (0, 0, 0)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB components to a hexadecimal color string.

    Components are clamped to the range 0..255.

    Args:
        r: Red component (0..255).
        g: Green component (0..255).
        b: Blue component (0..255).

    Returns:
        Uppercase hex string in the form ``#RRGGBB``.
    """
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))
    return f"#{r:02X}{g:02X}{b:02X}"


def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """Convert RGB (0..255) to HSL-like integers.

    Internally uses Python's ``colorsys.rgb_to_hls`` which returns (H, L, S).
    This function returns an integer tuple that matches your UI needs:

    - H: 0..359 (degrees)
    - S: 0..100 (percent)
    - L: 0..100 (percent)

    Args:
        r: Red component (0..255).
        g: Green component (0..255).
        b: Blue component (0..255).

    Returns:
        Tuple ``(h, s, l)`` with integer values.
    """
    rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
    h, l, s = colorsys.rgb_to_hls(rf, gf, bf)
    return int(round(h * 359)), int(round(s * 100)), int(round(l * 100))


def hsl_to_rgb(h: int, s: int, l: int) -> Tuple[int, int, int]:
    """Convert HSL-like integers to RGB (0..255).

    This function expects H in degrees and S/L in percent. Values are clamped
    where appropriate, and H is normalized with modulo 360.

    Note: ``colorsys.hls_to_rgb`` expects (H, L, S), hence the parameter order.

    Args:
        h: Hue in degrees (any int; normalized to 0..359).
        s: Saturation in percent (0..100).
        l: Lightness in percent (0..100).

    Returns:
        Tuple ``(r, g, b)`` with integer values 0..255.
    """
    hf = (h % 360) / 360.0
    sf = max(0, min(100, s)) / 100.0
    lf = max(0, min(100, l)) / 100.0
    r, g, b = colorsys.hls_to_rgb(hf, lf, sf)
    return int(round(r * 255)), int(round(g * 255)), int(round(b * 255))


def luminance(rgb: Tuple[int, int, int]) -> float:
    """Compute a simple perceived luminance from an RGB tuple.

    Uses weighted coefficients (Rec. 709-like) and normalizes the result to 0..1.

    Args:
        rgb: Tuple ``(r, g, b)`` with values 0..255.

    Returns:
        Luminance value in the range 0..1.
    """
    r, g, b = rgb
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0


def blend(a: Tuple[int, int, int], b: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
    """Blend two RGB colors.

    Linear interpolation between color ``a`` and ``b`` by factor ``t``.

    - ``t = 0`` returns ``a``
    - ``t = 1`` returns ``b``

    Args:
        a: First color as ``(r, g, b)``.
        b: Second color as ``(r, g, b)``.
        t: Blend factor in the range 0..1 (clamped).

    Returns:
        Blended color as ``(r, g, b)``.
    """
    t = max(0.0, min(1.0, t))
    return (
        int(round(a[0] * (1 - t) + b[0] * t)),
        int(round(a[1] * (1 - t) + b[1] * t)),
        int(round(a[2] * (1 - t) + b[2] * t)),
    )


def derive_theme_from_background(bg_hex: str, base_theme: dict) -> dict:
    """Derive a full theme palette from a background color.

    Given a background color, this function computes:
    - surface colors (slightly blended toward white/black)
    - border color
    - text color (pulled toward white/black but influenced by the background)
    - muted text color (between text and border)

    The algorithm adapts depending on whether the background is considered dark
    (luminance < 0.5) or light.

    Args:
        bg_hex: Background color as ``#RRGGBB``.
        base_theme: Base theme dictionary to copy and override. Must contain keys
            like ``text``, ``primary``, ``danger`` etc. Missing keys are kept as-is.

    Returns:
        A new dict with updated keys:
        ``background``, ``surface``, ``surface_alt``, ``border``, ``text``,
        and ``muted_text``.
    """
    bg_rgb = hex_to_rgb(bg_hex)
    is_dark = luminance(bg_rgb) < 0.5

    white = (255, 255, 255)
    black = (0, 0, 0)

    if is_dark:
        surface_rgb = blend(bg_rgb, white, 0.06)
        surface_alt_rgb = blend(bg_rgb, white, 0.10)
        border_rgb = blend(bg_rgb, white, 0.16)

        # Texto “puxa” um pouco a cor do fundo, mas continua claro
        text_rgb = blend(bg_rgb, white, 0.92)
    else:
        surface_rgb = blend(bg_rgb, black, 0.06)
        surface_alt_rgb = blend(bg_rgb, black, 0.10)
        border_rgb = blend(bg_rgb, black, 0.16)

        # Texto escuro, também pode variar um pouco com o fundo
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