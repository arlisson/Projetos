import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Button, Label
from PIL import Image, ImageTk


class EdgeDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Operações lógicas")

        # Variáveis para armazenar a imagem original e as imagens filtradas
        self.image_rgb1 = None
        self.image_rgb2 = None
        self.filtered_image_not = None
        self.filtered_image_xor = None

        # Criar um botão para escolher uma imagem e aplicar filtros
        self.button_choose_image = Button(
            self.root, text="Escolha as imagens", command=self.choose_image)
        self.button_choose_image.pack(pady=10)

        # Label para exibir a imagem original
        self.label_original_image_1 = Label(self.root)
        self.label_original_image_1.pack(side='left')
        self.label_original_image_2 = Label(self.root)
        self.label_original_image_2.pack(side='left')

        # Label para exibir a imagem filtrada com o filtro NOT
        self.label_filtered_image_not = Label(self.root)
        self.label_filtered_image_not.pack(side='right')

        # Label para exibir a imagem filtrada com o filtro XOR
        self.label_filtered_image_xor = Label(self.root)
        self.label_filtered_image_xor.pack(side='right')

    def choose_image(self):
        # Solicitar ao usuário para escolher uma imagem
        image_path1 = filedialog.askopenfilename(title="Escolha uma imagem",
                                                 filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp")])
        image_path2 = filedialog.askopenfilename(title="Escolha uma imagem",
                                                 filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp")])

        if image_path1 and image_path2:
            # Carregar a imagem escolhida
            self.load_image(image_path1, image_path2)

            # Aplicar todos os filtros
            self.apply_all_filters()
        else:
            print("Nenhuma imagem foi selecionada.")

    def load_image(self, image_path1, image_path2):
        # Carregar a imagem do caminho fornecido
        image1 = cv2.imread(image_path1)
        image2 = cv2.imread(image_path2)

        # Converter a imagem para RGB
        self.image_rgb1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
        self.image_rgb2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)

        # Exibir a imagem original na label correspondente
        self.display_image(
            self.image_rgb1, self.label_original_image_1, "Imagem 1")
        self.display_image(
            self.image_rgb2, self.label_original_image_2, "Imagem 2")

    def apply_not_filter(self):
        if self.image_rgb1 is not None and self.image_rgb2 is not None:

            self.image_rgb1 = cv2.resize(
                self.image_rgb1, (self.image_rgb2.shape[1], self.image_rgb2.shape[0]))

            # Aplicar a operação AND entre as duas imagens
            result = cv2.bitwise_not(self.image_rgb1, self.image_rgb1)
            self.display_image(result, self.label_filtered_image_not,
                               "Operação Lógica NOT Imagem 1")
            self.filtered_image_not = result

    def apply_xor_filter(self):
        if self.image_rgb1 is not None and self.image_rgb2 is not None:

            self.image_rgb1 = cv2.resize(
                self.image_rgb1, (self.image_rgb2.shape[1], self.image_rgb2.shape[0]))

            # Aplicar a operação AND entre as duas imagens
            result = cv2.bitwise_xor(self.image_rgb1, self.image_rgb2)
            self.display_image(result, self.label_filtered_image_xor,
                               "Operação Lógica XOR")
            self.filtered_image_and = result

    def apply_all_filters(self):
        # Aplicar todos os filtros
        self.apply_not_filter()
        self.apply_xor_filter()

    def display_image(self, image, label, title):
        # Redimensionar a imagem para o tamanho fixo
        fixed_width = 400
        fixed_height = 300
        img = Image.fromarray(image)
        img = img.resize((fixed_width, fixed_height), Image.ANTIALIAS)

        # Converter a imagem para um formato compatível com Tkinter
        img_tk = ImageTk.PhotoImage(img)

        # Atualizar a label com a imagem redimensionada
        label.config(text=title, image=img_tk,
                     compound='top', font=("Arial", 15))
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
