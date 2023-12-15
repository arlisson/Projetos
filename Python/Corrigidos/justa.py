processos = [('Processo 1', {
    'id': 1,
    'tempo_chegada': 1,
    'tempo_execucao': 9,
    'peso': 1
}), ('Processo 2', {
    'id': 2,
    'tempo_chegada': 2,
    'tempo_execucao': 10,
    'peso': 3
}), ('Processo 3', {
    'id': 3,
    'tempo_chegada': 3,
    'tempo_execucao': 10,
    'peso': 3
})]


def justa(processos):

    list_aux = sorted(processos, key=lambda x: x[1]['tempo_chegada'])

    tempo_atual = 0

    while list_aux:

        for id, info in list_aux:
            for _ in range(info['peso']):
                if info['tempo_execucao'] > 0:
                    print(f"{id} executando no tempo {tempo_atual}")
                    tempo_atual += 1
                    info['tempo_execucao'] -= 1

            if info['tempo_execucao'] <= 0:                
                list_aux.remove((id,info))


justa(processos)
