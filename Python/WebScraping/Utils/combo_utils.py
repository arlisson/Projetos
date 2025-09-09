def popular_dropdown(combo, dados, valor_padrao=(1, "Nenhum cadastrado")):
    if not dados:
        dados = [valor_padrao]

    nomes = [item[1] for item in dados]
    mapa_ids = {item[1]: item[0] for item in dados}

    combo["values"] = nomes
    combo.current(0)

    return mapa_ids  # <- importante
