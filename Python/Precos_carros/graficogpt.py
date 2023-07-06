import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

links = []
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

        for j in range(len(desc_carro)):
            descricao = desc_carro[j].get_text()
            ano = int(re.search(r'\d{4}', ano_carro[j].get_text()).group())
            preco = preco_carro[j].get_text().replace('R$', '')[:7]
            link = link_carro[j].get('href')

            carros.append(descricao)
            anos.append(ano)
            precos.append(preco)
            links.append(link)

except IndexError:
    print("A lista acabou na página: {}".format(i))

# Criar um DataFrame com os dados coletados
data = {
    'Descrição': carros,
    'Ano': anos,
    'Preço': precos,
    'Link': links
}

df = pd.DataFrame(data)

# Salvar o DataFrame em um arquivo Excel
df.to_excel('dados_carros.xlsx', index=False)
