from PIL import Image, ImageFilter
from tkinter import filedialog, Tk
from matplotlib import pyplot as plt


def apply_mode_filter(image_path):
    # Carregar a imagem do caminho fornecido
    image = Image.open(image_path)

    mode_filtered_image = image.filter(ImageFilter.MedianFilter)

    for _ in range(0, 1):

        mode_filtered_image = mode_filtered_image.filter(
            ImageFilter.ModeFilter)

    # Exibir a imagem original e a imagem filtrada lado a lado
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(image)
    plt.title("Imagem Original")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(mode_filtered_image)
    plt.title("Imagem Filtrada (Filtro de Mediana)")
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
        # Aplicar o filtro de moda à imagem escolhida
        apply_mode_filter(image_path)
    else:
        print("Nenhuma imagem foi selecionada.")


if __name__ == "__main__":
    main()
