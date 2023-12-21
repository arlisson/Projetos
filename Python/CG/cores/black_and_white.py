import cv2
from matplotlib import pyplot as plt

# Função para carregar a imagem e exibir em preto e branco


def exibir_imagem_preto_branco(caminho_imagem):
    # Carrega a imagem
    imagem = cv2.imread(caminho_imagem)

    # Converte a imagem para preto e branco
    imagem_pb = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Exibe a imagem original
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB))
    plt.title('Imagem Original')
    plt.axis('off')

    # Exibe a imagem em preto e branco
    plt.subplot(1, 2, 2)
    plt.imshow(imagem_pb, cmap='gray')
    plt.title('Imagem em Preto e Branco')
    plt.axis('off')

    # Exibe as imagens na mesma tela
    plt.show()


# Caminho da imagem que você deseja carregar
caminho_imagem = 'flores.jpg'

# Chama a função para exibir a imagem em preto e branco
exibir_imagem_preto_branco(caminho_imagem)
