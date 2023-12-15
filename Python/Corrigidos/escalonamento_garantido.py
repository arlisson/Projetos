processos = [('Processo 1', {'id': 1, 'tempo_chegada': 1, 'tempo_execucao': 9}),
             ('Processo 2', {
              'id': 2, 'tempo_chegada': 1, 'tempo_execucao': 10}),
             ('Processo 3', {'id': 3, 'tempo_chegada': 1, 'tempo_execucao': 10})]


def escalonamento_garantido(processos, quantum=1/len(processos)):
    rr = sorted(processos, key=lambda x: x[1]['tempo_chegada'])
    tempo_atual = rr[0][1]['tempo_chegada']

    processos_concluidos = []

    while processos:

        for i in processos:

            if i[1]['tempo_execucao'] < quantum and i[1]['tempo_execucao'] > 0:
                print(
                    f"{i[0]} executando no tempo {tempo_atual:.2f} até {tempo_atual+i[1]['tempo_execucao']:.2f}")
                tempo_atual += i[1]['tempo_execucao']
                i[1]['tempo_execucao'] = 0
            else:
                print(
                    f"{i[0]} executando no tempo {tempo_atual:.2f} até {tempo_atual+quantum:.2f}")
                i[1]['tempo_execucao'] -= quantum
                tempo_atual += quantum

            if i[1]['tempo_execucao'] <= 0:
                processos_concluidos.append(i)
                tempo_atual += quantum

            if i[1]['tempo_execucao']<=0:
                processos.remove(i)
                if processos:
                    quantum=1/len(processos)

        


escalonamento_garantido(processos)
