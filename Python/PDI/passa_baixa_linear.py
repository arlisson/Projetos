import cv2
import numpy as np
from tkinter import filedialog, Tk
from matplotlib import pyplot as plt


def apply_low_pass_filter(image_path, tamanho_filtro):
    # Carregar a imagem do caminho fornecido
    image = cv2.imread(image_path)

    # Converter a imagem para RGB para exibir com matplotlib
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Aplicar filtro passa-baixa linear (filtro de média)
    filtered_image = cv2.blur(image_rgb, (tamanho_filtro, tamanho_filtro))

    # Exibir a imagem original e a imagem filtrada lado a lado
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(image_rgb)
    plt.title("Imagem Original")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(filtered_image)
    plt.title("Imagem Filtrada (Máscara: {}x{} )".format(
        tamanho_filtro, tamanho_filtro))
    plt.axis("off")

    plt.show()


def main():
    # Inicializar a interface Tkinter
    root = Tk()
    root.withdraw()  # Esconder a janela principal

    # Solicitar ao usuário para escolher uma imagem
    image_path = filedialog.askopenfilename(title="Escolha uma imagem",
                                            filetypes=[("Imagens", "*.png;*.jpg;*.jpeg;*.bmp")])

    if image_path:
        # Solicitar ao usuário para definir o tamanho da máscara
        tamanho_filtro = 10
        apply_low_pass_filter(image_path, tamanho_filtro)

    else:
        print("Nenhuma imagem foi selecionada.")


if __name__ == "__main__":
    main()
