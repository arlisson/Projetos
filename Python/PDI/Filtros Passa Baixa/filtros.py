import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Button, Entry, Label
from matplotlib import pyplot as plt
from PIL import Image, ImageTk


class LowPassFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Filtro Passa-baixa")

        # Variáveis para armazenar a imagem original e a imagem filtrada
        self.image_rgb = None
        self.filtered_image = None

        # Criar um botão para escolher uma imagem
        self.button_choose_image = Button(
            self.root, text="Escolha uma imagem", command=self.choose_image)
        self.button_choose_image.pack(pady=10)

        # Criar um campo de entrada para ajustar o tamanho do filtro
        self.entry_filter_size = Entry(self.root)
        self.entry_filter_size.insert(0, "3")  # Valor padrão 3
        self.entry_filter_size.pack()

        # Criar um botão para aplicar o filtro passa-baixa
        self.button_apply_filter = Button(
            self.root, text="Aplicar filtro", command=self.apply_filter)
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

    def apply_filter(self):
        # Obter o tamanho do filtro do campo de entrada
        filter_size = self.get_filter_size()
        custom_kernel = np.array([[0.1, 0.1, 0.1],
                                  [0.1, 0.1, 0.1],
                                  [0.1, 0.1, 0.1]])

        # Aplicar o filtro de convolução personalizado
        self.filtered_image = cv2.filter2D(self.image_rgb, -1, custom_kernel)
        '''if self.image_rgb is not None and filter_size:
            # Aplicar filtro passa-baixa linear (filtro de média)
            self.filtered_image = cv2.blur(
                self.image_rgb, (filter_size, filter_size), anchor=(-1, -1))

            # Imprimir os valores da matriz
            print("Matriz do Filtro Blur:")
            print(self.filtered_image)'''

        # Exibir a imagem filtrada na label correspondente
        self.display_image(self.filtered_image, self.label_filtered_image,
                           f"Imagem Filtrada (Filtro:{filter_size})")

    def get_filter_size(self):
        # Obter o valor inserido no campo de entrada
        filter_size = self.entry_filter_size.get()
        try:
            filter_size = int(filter_size)
            # Verificar se o tamanho do filtro é ímpar
            if filter_size % 2 == 0:
                raise ValueError("O tamanho do filtro deve ser ímpar.")
            return filter_size
        except ValueError as e:
            # Exibir uma mensagem de erro para o usuário
            tk.messagebox.showerror("Erro", f"Valor inválido: {e}")
            return None

    def display_image(self, image, label, title):

        # Definir o tamanho fixo da imagem
        fixed_width = 600
        fixed_height = 400

        # Converter a imagem para um formato que pode ser exibido pelo tkinter
        img = Image.fromarray(image)

        # Redimensionar a imagem para o tamanho fixo (400x400)
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
    app = LowPassFilterApp(root)

    # Iniciar a interface Tkinter
    root.mainloop()


if __name__ == "__main__":
    main()
