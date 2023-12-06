from tabulate import tabulate

# Lista de graus das notas
degrees = ["I", "ii", "iii", "IV", "V", "vi", "vii°"]


fields = []
c = ["C", "Dm", "Em", "F", "G", "Am", "B°"]
d = ["D", "Em", "F#m", "G", "A", "Bm", "C#°"]
fields.append(c)

fields.append(d)
print("{} Campo Harmônico Maior {}".format("-"*14, "-"*14))# Lista de listas para armazenar os dados da tabela
data = [degrees]

# Preenchendo a lista de listas com os acordes de cada campo harmônico maior
for chords in fields:
    data.append(chords)

# Exibição dos dados formatados como tabela no terminal
print(tabulate(data, headers="firstrow", tablefmt="grid"))
