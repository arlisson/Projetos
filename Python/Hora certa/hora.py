import requests
from bs4 import *
import time
from tkinter import *


def pegar_hora():

    url = 'https://www.horariodebrasilia.org/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

    response = requests.get(url, headers=headers)

    content = response.content

    site = BeautifulSoup(content, 'html.parser')

    hora = site.find('p', attrs={'id': 'relogio'})
    dia = site.find('h3', attrs={'id': 'dia-topo'})

    print(dia.get_text())
    texto = 'A hora atual de Brasília é: {}'.format(hora.get_text())
    print(texto)

    hora_texto["text"] = texto  # editar o texto que será exibido dinâmicamente


janela = Tk()  # Criar a janela

janela.title('Hora Certa')  # Título da Janela


# Definições da janela
texto = Label(janela, text='Horário Oficial de Brasília')
texto.grid(column=0, row=0, padx=20, pady=10)

botao = Button(janela, text='Exibir Hora', command=pegar_hora)
botao.grid(column=0, row=1, padx=20, pady=10)

hora_texto = Label(janela, text='')
hora_texto.grid(column=0, row=2, padx=20, pady=10)

janela.mainloop()  # manter a janela aberta
