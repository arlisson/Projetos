processos = [('Processo 1', {'id': 1, 'tempo_execucao': 10, 'prioridade': 9}),
             ('Processo 2', {'id': 2, 'tempo_execucao': 13, 'prioridade': 8}),
             ('Processo 3', {'id': 3, 'tempo_execucao': 9, 'prioridade': 7})]


def aging(processos, quantum=3):

    list_aux = sorted(
        processos, key=lambda x: x[1]['prioridade'], reverse=False)

    tempo_atual = 0

    while list_aux:

        if list_aux[0][1]['tempo_execucao'] > quantum:
            print(
                f"Executando {list_aux[0][0]}, do tempo {tempo_atual} até {tempo_atual+quantum}, prioridade {list_aux[0][1]['prioridade']}, Tempo restante: {list_aux[0][1]['tempo_execucao']}")
            tempo_atual += quantum
            list_aux[0][1]['tempo_execucao'] -= quantum
            if list_aux[0][1]['tempo_execucao'] == 0:
                list_aux.remove(list_aux[0])
        else:
            print(
                f"Executando {list_aux[0][0]}, do tempo {tempo_atual} até {tempo_atual+list_aux[0][1]['tempo_execucao']}, prioridade {list_aux[0][1]['prioridade']}, Tempo restante: {list_aux[0][1]['tempo_execucao']}")
            tempo_atual += list_aux[0][1]['tempo_execucao']
            list_aux[0][1]['tempo_execucao'] = 0
            list_aux.remove(list_aux[0])

        for i, info in list_aux:
            if info['id'] != list_aux[0][1]['id']:
                info['prioridade'] -= 1

        list_aux = sorted(
            list_aux, key=lambda x: x[1]['prioridade'], reverse=False)


aging(processos)
