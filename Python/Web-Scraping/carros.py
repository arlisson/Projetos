from ctypes import sizeof
from email import header
from tkinter import DoubleVar
import requests
from bs4 import *
import re

'''url = 'https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-rj/norte-do-estado-do-rio/norte-do-estado?pe=50000&motp=1'
'''
links= []
carros = []
precos = []
anos = []


last_page = 50

try:
    for i in range(last_page):
        url = 'https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-rj/norte-do-estado-do-rio/norte-do-estado?o={}&pe=50000&motp=1'.format(
            i+1)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

        response = requests.get(url, headers=headers)

        content = response.content

        site = BeautifulSoup(content, 'html.parser')

        desc_carro = site.findAll(
            'h2', attrs={'class': 'horizontal title sc-ifAKCX hUnWqk'})

        link_carro = site.findAll(
            'a', attrs={'class': 'sc-dRFtgE etGiBL'})

        ano_carro = site.findAll(
            'div', attrs={'class': 'horizontal sc-iIHSe hrShZb'})

        preco_carro = site.findAll(
            'div', attrs={'class': 'horizontal sc-gldTML fphJhh'})


        with open('precos_carros.csv','a', newline = '', encoding = 'UTF-8') as arquivo:                
        
            for j in range(len(desc_carro)):
            
                linha = 'Descrição: {} Ano: {} Preço: {} Link: {}\n'.format(desc_carro[j].get_text(), int(re.search(
                    r'\d{4}', ano_carro[j].get_text()).group()), preco_carro[j].get_text().replace('R$', '')[:7], link_carro[j].get('href'))

                arquivo.write(linha)
            ''' print('Descrição: {}\nAno: {}\nPreço: {}\nLink: {}\n'.format(desc_carro[j].get_text(), int(re.search(
                    r'\d{4}', ano_carro[j].get_text()).group()), preco_carro[j].get_text().replace('R$', '')[:7], link_carro[j].get('href')))
            '''
           
except IndexError:
    print("A lista acabou na página: {}".format(i))
