processos = [('Processo 1', {
    'id': 1,
    'tempo_chegada': 1,
    'tempo_execucao': 10,
    'prioridade': 10
}), ('Processo 2', {
    'id': 2,
    'tempo_chegada': 2,
    'tempo_execucao': 20,
    'prioridade': 20
}), ('Processo 3', {
    'id': 3,
    'tempo_chegada': 3,
    'tempo_execucao': 30,
    'prioridade': 30
})]


def prioridade(processos):

    tempo_atual = 0
    while processos:
        processo_atual = None

        for processo, info in processos:
            if info['tempo_chegada'] <= tempo_atual:
                if processo_atual is None or info['prioridade'] > processo_atual[1]['prioridade']:
                    processo_atual = (processo, info)

        if processo_atual is not None:
            processo, info = processo_atual
            print(
                f"Executando {processo} no tempo {tempo_atual}, prioridade: {info['prioridade']}")
            info['prioridade'] -= 1
            info['tempo_execucao'] -= 1
            tempo_atual += 1

            if info['tempo_execucao'] == 0:
                processos.remove((processo, info))
        else:
            tempo_atual += 1


prioridade(processos)
