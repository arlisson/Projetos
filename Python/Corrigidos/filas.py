fila1 = [('Processo 1', {'id': 1, 'tempo_chegada': 1, 'tempo_execucao': 20}),
         ('Processo 2', {'id': 2, 'tempo_chegada': 3, 'tempo_execucao': 10}),
         ('Processo 3', {'id': 3, 'tempo_chegada': 2, 'tempo_execucao': 30})]

fila2 = [('Processo 1', {'id': 1, 'tempo_chegada': 63, 'tempo_execucao': 20}),
         ('Processo 2', {'id': 2, 'tempo_chegada': 64, 'tempo_execucao': 10}),
         ('Processo 3', {'id': 3, 'tempo_chegada': 65, 'tempo_execucao': 30})]

fila1 = sorted(fila1, key=lambda x:x[1]['tempo_chegada'])
fila2 = sorted(fila2, key=lambda x:x[1]['tempo_chegada'])

filas = [('Fila 1', fila1, 1), ('Fila 2', fila2, 2)]

filas = sorted(filas, key=lambda x:x[2], reverse=True)

def multi_fila(filas):
    tempo_atual = 0

    while filas:
        fila_atual = None
        for nome_fila, fila, prioridade in filas:
            if fila:                
                processo, info = fila[0]
                if info['tempo_chegada'] >= tempo_atual:
                    tempo_atual = info['tempo_chegada']
                    if fila_atual is None:
                        fila_atual = (nome_fila, prioridade)
                elif info['tempo_chegada'] <= tempo_atual:                    
                    if fila_atual is None:
                        fila_atual = (nome_fila, prioridade)
        if fila_atual is not None:            
            nome_fila, prioridade = fila_atual            
            fila = [f for n, f, _ in filas if n == nome_fila][0]
            processo, info = fila.pop(0)

            print(
                f"Executando {processo} da {nome_fila} no tempo {tempo_atual} até o tempo: {tempo_atual+info['tempo_execucao']}")
            tempo_atual = tempo_atual + info['tempo_execucao']
            print(f"{processo} da {nome_fila} concluído.")

        else:
            tempo_atual += 1

        
        filas = [(nome_fila, fila, prioridade)
                 for nome_fila, fila, prioridade in filas if fila]


multi_fila(filas)
