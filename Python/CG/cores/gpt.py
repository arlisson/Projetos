import tkinter as tk
from tkinter import ttk
from colorsys import rgb_to_hsv, rgb_to_yiq, rgb_to_hls
from colormath.color_objects import sRGBColor, XYZColor
from colormath.color_conversions import convert_color

def rgb_to_cmyk(rgb):
    r, g, b = rgb
    c = 1 - r
    m = 1 - g
    y = 1 - b
    k = min(c, m, y)
    if k == 1:
        return 0, 0, 0, 1
    c = (c - k) / (1 - k)
    m = (m - k) / (1 - k)
    y = (y - k) / (1 - k)
    return c, m, y, k

def rgb_to_xyz(rgb):
    rgb_color = sRGBColor(*rgb)
    xyz_color = convert_color(rgb_color, XYZColor)
    return xyz_color.get_value_tuple()

def update_color(*args):
    r = int(red_var.get())
    g = int(green_var.get())
    b = int(blue_var.get())

    rgb_label.config(text=f'RGB: ({r}, {g}, {b})')

    hsv = rgb_to_hsv(r / 255, g / 255, b / 255)
    hsv_label.config(
        text=f'HSV: ({hsv[0]*360:.2f}, {hsv[1]*100:.2f}%, {hsv[2]*100:.2f}%)')
    hsv_square.config(bg=color_to_hex(r, g, b))

    cmyk = rgb_to_cmyk((r / 255, g / 255, b / 255))
    cmyk_label.config(
        text=f'CMYK: ({cmyk[0]*100:.2f}%, {cmyk[1]*100:.2f}%, {cmyk[2]*100:.2f}%, {cmyk[3]*100:.2f}%)')
    cmyk_square.config(bg=color_to_hex(r, g, b))

    hsl = rgb_to_hls(r / 255, g / 255, b / 255)
    hsl_label.config(
        text=f'HSL: ({hsl[0]*360:.2f}, {hsl[2]*100:.2f}%, {hsl[1]*100:.2f}%)')
    hsl_square.config(bg=color_to_hex(r, g, b))

    yiq = rgb_to_yiq(r / 255, g / 255, b / 255)
    yiq_label.config(
        text=f'YIQ: ({yiq[0]:.2f}, {yiq[1]*100:.2f}%, {yiq[2]*100:.2f}%)')
    yiq_square.config(bg=color_to_hex(r, g, b))

    xyz = rgb_to_xyz((r / 255, g / 255, b / 255))
    xyz_label.config(
        text=f'XYZ: ({xyz[0]:.2f}, {xyz[1]:.2f}, {xyz[2]:.2f})')
    xyz_square.config(bg=color_to_hex(r, g, b))

    hex_label.config(text=f'Hex: {color_to_hex(r, g, b)}')

def color_to_hex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

root = tk.Tk()
root.title("Conversor de cor")

red_var = tk.StringVar(value='0')
green_var = tk.StringVar(value='0')
blue_var = tk.StringVar(value='0')

red_label = ttk.Label(root, text="Red:")
red_entry = ttk.Entry(root, textvariable=red_var, width=5)
green_label = ttk.Label(root, text="Green:")
green_entry = ttk.Entry(root, textvariable=green_var, width=5)
blue_label = ttk.Label(root, text="Blue:")
blue_entry = ttk.Entry(root, textvariable=blue_var, width=5)

rgb_label = ttk.Label(root, text="RGB: (0, 0, 0)")
hsv_label = ttk.Label(root, text="HSV: (0.00, 0.00%, 0.00%)")
cmyk_label = ttk.Label(root, text="CMYK: (0.00%, 0.00%, 0.00%, 0.00%)")
hsl_label = ttk.Label(root, text="HSL: (0.00, 0.00%, 0.00%)")
yiq_label = ttk.Label(root, text="YIQ: (0.00, 0.00%, 0.00%)")

hsv_square = tk.Label(root, text="HSV", width=10, height=2, relief="solid")
cmyk_square = tk.Label(root, text="CMYK", width=10, height=2, relief="solid")
hsl_square = tk.Label(root, text="HSL", width=10, height=2, relief="solid")
yiq_square = tk.Label(root, text="YIQ", width=10, height=2, relief="solid")

red_label.grid(row=0, column=0, padx=5, pady=5, sticky="E")
red_entry.grid(row=0, column=1, padx=5, pady=5)
green_label.grid(row=1, column=0, padx=5, pady=5, sticky="E")
green_entry.grid(row=1, column=1, padx=5, pady=5)
blue_label.grid(row=2, column=0, padx=5, pady=5, sticky="E")
blue_entry.grid(row=2, column=1, padx=5, pady=5)

rgb_label.grid(row=3, column=0, columnspan=2, pady=5)
hsv_label.grid(row=4, column=0, columnspan=2, pady=5)
cmyk_label.grid(row=5, column=0, columnspan=2, pady=5)
hsl_label.grid(row=6, column=0, columnspan=2, pady=5)
yiq_label.grid(row=7, column=0, columnspan=2, pady=5)

hsv_square.grid(row=4, column=2, padx=5, pady=5)
cmyk_square.grid(row=5, column=2, padx=5, pady=5)
hsl_square.grid(row=6, column=2, padx=5, pady=5)
yiq_square.grid(row=7, column=2, padx=5, pady=5)

xyz_label = ttk.Label(root, text="XYZ: (0.00, 0.00, 0.00)")
xyz_square = tk.Label(root, text="XYZ", width=10, height=2, relief="solid")

xyz_label.grid(row=8, column=0, columnspan=2, pady=5)
xyz_square.grid(row=8, column=2, padx=5, pady=5)

hex_label = ttk.Label(root, text="Hex: #000000")
hex_label.grid(row=9, column=0, columnspan=3, pady=5)

red_var.trace_add("write", update_color)
green_var.trace_add("write", update_color)
blue_var.trace_add("write", update_color)

root.mainloop()
