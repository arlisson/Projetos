from tabulate import tabulate

# Lista de graus das notas
degrees = ["I", "ii", "iii", "IV", "V", "vi", "vii°"]

# Lista de acordes para cada campo harmônico maior
fields = []

C = ["C", "Dm", "Em", "F", "G", "Am", "B°"]
d = ["D", "Em", "F#m", "G", "A", "Bm", "C#°"]
e = ["E", "F#m", "G#m", "A", "B", "C#m", "D#°"]
f = ["F", "Gm", "Am", "Bb", "C", "Dm", "E°"]
g = ["G", "Am", "Bm", "C", "D", "Em", "F#°"]
a = ["A", "Bm", "C#m", "D", "E", "F#m", "G#°"]
b = ["B", "C#m", "D#m", "E", "F#", "G#m", "A#°"]

fields.append(C)
fields.append(d)
for i in range():
    fields.append()
print("{} Campo Harmônico Maior {}".format("-"*14, "-"*14))

# Lista de listas para armazenar os dados da tabela
data = [degrees]

# Preenchendo a lista de listas com os acordes de cada campo harmônico maior
for chords in fields:
    data.append(chords)

# Exibição dos dados formatados como tabela no terminal
print(tabulate(data, headers="firstrow", tablefmt="grid"))
