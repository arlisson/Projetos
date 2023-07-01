from ctypes import sizeof
from email import header
from tkinter import DoubleVar
import requests
from bs4 import *
import re

url = 'https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-rj/norte-do-estado-do-rio/norte-do-estado?pe=50000&motp=1'

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

'''last_page = site.find(
    'span', attrs={'class': 'sc-1mi5vq6-0 dQbOE sc-ifAKCX lgjPoE'})
last_page = float(re.search(r'\d+\.\d+', last_page.get_text()).group())'''


for i in range(len(desc_carro)):
    print('Descrição: {}\nAno: {}\nPreço: {}\nLink: {}\n'.format(desc_carro[i].get_text(), int(re.search(
        r'\d{4}', ano_carro[i].get_text()).group()), re.search(r'\d+\.\d+', preco_carro[i].get_text()).group(), link_carro[i].get('href')))
