import cv2
import numpy as np
import matplotlib.pyplot as plt


def exibir_imagem_preto_branco(caminho_imagem):
    # Carrega a imagem
    imagem = cv2.imread(caminho_imagem)

    # Verifica se a imagem foi carregada corretamente
    if imagem is None:
        print(f'Erro ao carregar a imagem em {caminho_imagem}')
        return

    # Converte a imagem para preto e branco
    imagem_pb = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Calcula os histogramas usando numpy
    hist_canais = [np.histogram(imagem[:, :, i], bins=256, range=[0, 256])[
        0] for i in range(3)]
    hist_pb = np.histogram(imagem_pb, bins=256, range=[0, 256])[0]

    # Exibe a imagem original
    plt.subplot(2, 2, 1)
    plt.imshow(cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB))
    plt.title('Imagem Original')
    plt.axis('off')

    # Exibe a imagem em preto e branco
    plt.subplot(2, 2, 2)
    plt.imshow(imagem_pb, cmap='gray')
    plt.title('Imagem em Preto e Branco')
    plt.axis('off')

    # Exibe o histograma por canal de cores
    plt.subplot(2, 2, 3)
    plt.plot(hist_canais[0], color='blue', label='Canal Azul')
    plt.plot(hist_canais[1], color='green', label='Canal Verde')
    plt.plot(hist_canais[2], color='red', label='Canal Vermelho')
    plt.title('Histograma por Canal de Cores')
    plt.xlabel("Nível de intensidade")
    plt.ylabel("Quantidade de pixels")
    plt.legend()

    # Exibe o histograma em escala de cinza
    plt.subplot(2, 2, 4)
    plt.plot(hist_pb, color='black', label='Escala de Cinza')
    plt.title('Histograma em Escala de Cinza')
    plt.xlabel("Nível de intensidade")
    plt.ylabel("Quantidade de pixels")
    plt.legend()

    # Exibe as imagens na mesma tela
    plt.show()


# Caminho da imagem que você deseja carregar
caminho_imagem = '0000ff.jpg'

# Chama a função para exibir a imagem em preto e branco
exibir_imagem_preto_branco(caminho_imagem)
