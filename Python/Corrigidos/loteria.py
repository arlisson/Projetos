import random

processos = [
    ('Processo 1', {'id': 1, 'tempo_chegada': 1,
     'tempo_execucao': 8, 'bilhetes': 10}),
    ('Processo 2', {'id': 2, 'tempo_chegada': 1,
     'tempo_execucao': 10, 'bilhetes': 20}),
    ('Processo 3', {'id': 3, 'tempo_chegada': 1,
     'tempo_execucao': 10, 'bilhetes': 30})
]


def loteria(processos, quantum=3):
    tempo_atual = 0

    bilhetes = sum(info['bilhetes'] for _, info in processos)

    while processos:
        numero_aleatorio = random.randint(1, bilhetes)

        for id, info in processos:
            for i in range(info['bilhetes']):
                if numero_aleatorio == i:
                    if info['tempo_execucao'] >= quantum:
                        print(
                            f'{id} executando do tempo {tempo_atual} até {tempo_atual+quantum}')
                        tempo_atual += quantum
                        info['tempo_execucao'] -= quantum
                    else:
                        print(
                            f"{id} executando do tempo {tempo_atual} até {tempo_atual+info['tempo_execucao']}")
                        tempo_atual += info['tempo_execucao']
                        info['tempo_execucao'] = 0

            if info['tempo_execucao'] <= 0:                
                processos.remove((id,info))
                bilhetes = sum(info['bilhetes'] for _, info in processos)


loteria(processos)
