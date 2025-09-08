def popular_dropdown(combo, dados, valor_padrao=(1, "Nenhum cadastrado")):
    if not dados:
        dados = [valor_padrao]

    valores = [f"{item[0]} - {item[1]}" for item in dados]
    combo["values"] = valores
    combo.current(0)
