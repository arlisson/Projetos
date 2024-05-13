vetor = [54, 23, 17, 89, 42, 36, 70, 12, 58, 91, 67, 25, 49, 31, 83]
aux = len(vetor)

maior = vetor[0]
for i in range(1, aux):

    if(vetor[i] > vetor[aux-1]):
        maior = vetor[i]
print(maior)
