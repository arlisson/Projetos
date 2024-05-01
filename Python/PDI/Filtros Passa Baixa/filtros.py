import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Button, Label
from PIL import Image, ImageTk


class EdgeDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Detector de Bordas - Sobel")

        # Variáveis para armazenar a imagem original e as imagens filtradas
        self.image_rgb = None
        self.filtered_image_sobel = None
        self.filtered_image_roberts = None
        self.filtered_image_linear = None

        # Criar um botão para escolher uma imagem e aplicar filtros
        self.button_choose_image = Button(
            self.root, text="Escolha uma imagem", command=self.choose_image)
        self.button_choose_image.pack(pady=10)

        # Label para exibir a imagem original
        self.label_original_image = Label(self.root)
        self.label_original_image.pack(side='left')

        # Label para exibir a imagem filtrada com o filtro Linear
        self.label_filtered_image_linear = Label(self.root)
        self.label_filtered_image_linear.pack(side='left')

        # Label para exibir a imagem filtrada com o filtro de Sobel
        self.label_filtered_image_sobel = Label(self.root)
        self.label_filtered_image_sobel.pack(side='right')

        # Label para exibir a imagem filtrada com o filtro de Roberts
        self.label_filtered_image_roberts = Label(self.root)
        self.label_filtered_image_roberts.pack(side='left')

    def choose_image(self):
        # Solicitar ao usuário para escolher uma imagem
        image_path = filedialog.askopenfilename(title="Escolha uma imagem",
                                                filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp")])

        if image_path:
            # Carregar a imagem escolhida
            self.load_image(image_path)
            # Aplicar todos os filtros
            self.apply_all_filters()
        else:
            print("Nenhuma imagem foi selecionada.")

    def load_image(self, image_path):
        # Carregar a imagem do caminho fornecido
        image = cv2.imread(image_path)

        # Converter a imagem para RGB
        self.image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Exibir a imagem original na label correspondente
        self.display_image(
            self.image_rgb, self.label_original_image, "Imagem Original")

    def apply_roberts_filter(self):
        if self.image_rgb is not None:
            # Aplicar filtro de detecção de bordas Roberts
            roberts_x = cv2.Sobel(self.image_rgb, cv2.CV_64F, 1, 0, ksize=1)
            roberts_y = cv2.Sobel(self.image_rgb, cv2.CV_64F, 0, 1, ksize=1)
            roberts_combined = cv2.bitwise_or(
                np.uint8(np.absolute(roberts_x)), np.uint8(np.absolute(roberts_y)))

            # Normalizar valores para exibição
            roberts_normalized = cv2.normalize(
                roberts_combined, None, 0, 255, cv2.NORM_MINMAX)

            # Converter para imagem RGB para exibição
            roberts_rgb = np.uint8(np.absolute(roberts_normalized))

            # Exibir a imagem filtrada na label correspondente
            self.display_image(roberts_rgb, self.label_filtered_image_roberts,
                               "Detector de Bordas Roberts")
            self.filtered_image_roberts = roberts_rgb

    def apply_sobel_filter(self):
        if self.image_rgb is not None:

            # Obter largura e altura da imagem
            height, width, _ = self.image_rgb.shape

            # Criar uma cópia da imagem para armazenar o resultado
            output_image = np.zeros_like(self.image_rgb)

            # Definir os kernels Sobel
            sobel_x = np.array([[1, 0, -1],
                                [2, 0, -2],
                                [1, 0, -1]])

            sobel_y = np.array([[1, 2, 1],
                                [0, 0, 0],
                                [-1, -2, -1]])

            # Função para convolução
            def convolution(x, y, p, kernel):
                sum_value = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        #pixel_index = ((y + j) * width + (x + i))
                        value = self.image_rgb[y + j, x + i, p]
                        sum_value += value * kernel[j + 1][i + 1]
                return sum_value

            # Função para normalizar um valor entre 0 e 255
            def normalize(value):
                return max(0, min(255, value))

            # Aplicar o filtro Sobel
            for y in range(1, height - 1):
                for x in range(1, width - 1):
                    total_red = convolution(x, y, 0, sobel_x)
                    temp_calculation = convolution(x, y, 0, sobel_y)
                    total_red = np.sqrt(total_red * total_red +
                                        temp_calculation * temp_calculation)
                    total_green = convolution(x, y, 1, sobel_x)
                    temp_calculation = convolution(x, y, 1, sobel_y)
                    total_green = np.sqrt(
                        total_green * total_green + temp_calculation * temp_calculation)
                    total_blue = convolution(x, y, 2, sobel_x)
                    temp_calculation = convolution(x, y, 2, sobel_y)
                    total_blue = np.sqrt(total_blue * total_blue +
                                         temp_calculation * temp_calculation)

                    # Normalizar o gradiente para o intervalo entre 0 e 255
                    temp_red = normalize(total_red)
                    temp_green = normalize(total_green)
                    temp_blue = normalize(total_blue)

                    output_image[y, x] = [temp_red, temp_green, temp_blue]

            self.display_image(output_image, self.label_filtered_image_sobel,
                               "Detector de Bordas Sobel")
            self.filtered_image_sobel = output_image

    def apply_linear_filter(self):
        custom_kernel = np.array([[-1, -1, -1],
                                  [-1, 8, -1],
                                  [-1, -1, -1]])
        # Aplicar o filtro de convolução personalizado
        self.filtered_image = cv2.filter2D(
            self.image_rgb, -1, custom_kernel)

        # Exibir a imagem filtrada na label correspondente
        self.display_image(self.filtered_image, self.label_filtered_image_linear,
                           "Passa-Alta Linear")
        self.filtered_linear_image = self.filtered_image

    def apply_all_filters(self):
        # Aplicar todos os filtros
        self.apply_linear_filter()
        self.apply_roberts_filter()
        self.apply_sobel_filter()

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
