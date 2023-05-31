
# criando função de busca
def busca(lista, valor):
    '''Retorna elemento da lista'''
    for i in range(len(lista)):
        if lista[i] == valor:
            return i

    return None


lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
valor = 0

retorno = busca(lista, valor)

if retorno is not None:
    print("Valor {} encontrado na posição {} ".format(valor, retorno))
else:
    print("Valor não encontrado!")
