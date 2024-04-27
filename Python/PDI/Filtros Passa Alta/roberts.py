import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Button, Label
from PIL import Image, ImageTk


class EdgeDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Detector de Bordas - Roberts")

        # Variáveis para armazenar a imagem original e a imagem filtrada
        self.image_rgb = None
        self.filtered_image = None

        # Criar um botão para escolher uma imagem
        self.button_choose_image = Button(
            self.root, text="Escolha uma imagem", command=self.choose_image)
        self.button_choose_image.pack(pady=10)

        # Criar um botão para aplicar o filtro de detecção de bordas Roberts
        self.button_apply_filter = Button(
            self.root, text="Aplicar filtro Roberts", command=self.apply_roberts_filter)
        self.button_apply_filter.pack(pady=10)

        # Label para exibir a imagem original
        self.label_original_image = Label(self.root)
        self.label_original_image.pack(side='left')

        # Label para exibir a imagem filtrada
        self.label_filtered_image = Label(self.root)
        self.label_filtered_image.pack(side='right')

    def choose_image(self):
        # Solicitar ao usuário para escolher uma imagem
        image_path = filedialog.askopenfilename(title="Escolha uma imagem",
                                                filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp")])

        if image_path:
            # Carregar a imagem escolhida
            self.load_image(image_path)
        else:
            print("Nenhuma imagem foi selecionada.")

    def load_image(self, image_path):
        # Carregar a imagem do caminho fornecido
        image = cv2.imread(image_path)

        # Converter a imagem para RGB para exibir com matplotlib
        self.image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Exibir a imagem original na label correspondente
        self.display_image(
            self.image_rgb, self.label_original_image, "Imagem Original")

    def apply_roberts_filter(self):
        if self.image_rgb is not None:
            # Aplicar filtro de detecção de bordas roberts
            sobel_x = cv2.Sobel(self.image_rgb, cv2.CV_64F, 1, 0, ksize=3)
            sobel_y = cv2.Sobel(self.image_rgb, cv2.CV_64F, 0, 1, ksize=3)
            sobel_combined = cv2.magnitude(sobel_x, sobel_y)

            # Normalizar valores para exibição
            sobel_normalized = cv2.normalize(
                sobel_combined, None, 0, 255, cv2.NORM_MINMAX)

            # Converter para imagem RGB para exibição
            roberts_rgb = np.uint8(np.absolute(sobel_normalized))

            # Exibir a imagem filtrada na label correspondente
            self.display_image(roberts_rgb, self.label_filtered_image,
                               "Imagem Filtrada (Detector de Bordas Roberts)")

    def display_image(self, image, label, title):
        # Definir o tamanho fixo da imagem
        fixed_width = 600
        fixed_height = 400

        # Converter a imagem para um formato que pode ser exibido pelo tkinter
        img = Image.fromarray(image)

        # Redimensionar a imagem para o tamanho fixo
        img = img.resize((fixed_width, fixed_height), Image.ANTIALIAS)

        # Converter a imagem para um formato compatível com Tkinter
        img_tk = ImageTk.PhotoImage(img)

        # Atualizar a label com a imagem redimensionada
        label.config(text=title, image=img_tk,
                     compound='top', font=("Arial", 30))
        label.image = img_tk  # Manter uma referência para evitar garbage collection


def main():
    # Inicializar a interface Tkinter
    root = tk.Tk()

    # Definir a janela para ocupar a tela inteira
    root.state("zoomed")  # Modo de tela cheia

    # Criar a aplicação
    app = EdgeDetectionApp(root)

    # Iniciar a interface Tkinter
    root.mainloop()


if __name__ == "__main__":
    main()