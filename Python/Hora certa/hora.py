import requests
from bs4 import *
import time

url = 'https://www.horariodebrasilia.org/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

response = requests.get(url, headers=headers)

content = response.content

site = BeautifulSoup(content, 'html.parser')

hora = site.find('p', attrs={'id': 'relogio'})
dia = site.find('h3', attrs={'id': 'dia-topo'})

print(dia.get_text())
print('A hora atual de Brasília é: {}'.format(hora.get_text()))

time.sleep(60)
