import cv2

# Carregar as duas imagens
image1 = cv2.imread('tartaruga.jpg')
image2 = cv2.imread('peixe.jpg')

# Verificar se as imagens foram carregadas corretamente
if image1 is None or image2 is None:
    print("Erro ao carregar as imagens.")
else:
    # Redimensionar as imagens para terem o mesmo tamanho (opcional)
    image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]))

    # Aplicar a operação AND entre as duas imagens
    result = cv2.bitwise_and(image1, image2)

    # Exibir as imagens original e o resultado lado a lado para comparação
    cv2.imshow('Image 1', image1)
    cv2.imshow('Image 2', image2)
    cv2.imshow('Result', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
