processos = [('Processo 1', {
    'id': 1,
    'tempo_chegada': 1,
    'tempo_execucao': 10,
    'tempo_restante': 10
}), ('Processo 2', {
    'id': 2,
    'tempo_chegada': 2,
    'tempo_execucao': 10,
    'tempo_restante': 7
}), ('Processo 3', {
    'id': 3,
    'tempo_chegada': 4,
    'tempo_execucao': 30,
    'tempo_restante': 3
})]


def srtn(processos):

    tempo_atual = 0
    while processos:
        processo_atual = None

        for processo, info in processos:
            if info['tempo_chegada'] <= tempo_atual:
                if processo_atual is None or info['tempo_restante'] < processo_atual[1]['tempo_restante']:
                    processo_atual = (processo, info)

        if processo_atual is not None:
            processo, info = processo_atual
            print(
                f"Executando {processo} no tempo {tempo_atual}, tempo restante: {info['tempo_restante']}")
            info['tempo_restante'] -= 1
            tempo_atual += 1

            if info['tempo_restante'] == 0:
                processos.remove((processo, info))
        else:
            tempo_atual += 1


srtn(processos)
