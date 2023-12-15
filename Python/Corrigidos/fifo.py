processos = [('Processo 1', {
    'id': 1,
    'tempo_chegada': 1,
    'tempo_execucao': 10
}), ('Processo 2', {
    'id': 2,
    'tempo_chegada': 2,
    'tempo_execucao': 20
}), ('Processo 3', {
    'id': 3,
    'tempo_chegada': 1,
    'tempo_execucao': 30
})]


def fifo(list_procces):
    list_aux = sorted(list_procces, key=lambda x: x[1]['tempo_chegada'])
    list_p = []
    tempo_atual = list_aux[0][1]['tempo_chegada'] + \
        list_aux[0][1]['tempo_execucao']
    list_p.append(list_aux[0])
    for i in list_aux:

        if i[1]['tempo_chegada'] > tempo_atual:
            tempo_atual = i[1]['tempo_chegada']
            tempo_atual = tempo_atual + i[1]['tempo_execucao']
            list_p.append(i)

        if (i[1]['tempo_chegada'] + i[1]['tempo_execucao']) > tempo_atual or (i[1]['tempo_chegada'] + i[1]['tempo_execucao']) < tempo_atual:
            i[1]['tempo_chegada'] = tempo_atual
            tempo_atual = tempo_atual + i[1]['tempo_execucao']
            list_p.append(i)

    return list_p


for i in fifo(processos):
    print(f"{i[0]} executando do tempo {i[1]['tempo_chegada']} até o tempo {i[1]['tempo_chegada'] + i[1]['tempo_execucao']}")
