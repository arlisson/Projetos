from tkinter import messagebox
from DAO.database import buscar_historico_precos
from Utils.baixar_carta import salvar_imagem_local
from scraping.scraping_cartas import *

# cartas = buscar_carta_myp("https://mypcards.com/yugioh?ProdutoSearch%5Bmarca%5D=yugioh&ProdutoSearch%5Bquery%5D=sbc1&page=10")

# print(cartas)

# produto = buscar_produto_liga('https://www.ligayugioh.com.br/?view=prod/view&pcode=131327&prod=Collector%20Set%20-%20Speed%20Duel:%20Battle%20City%20Finals')
# print(produto)

cartas = buscar_cartas_colecao('https://mypcards.com/yugioh?ProdutoSearch%5Bmarca%5D=yugioh&ProdutoSearch%5Bquery%5D=sbc1')

for carta in cartas:
     print(carta)

#salvar_imagem_local("https://i.pinimg.com/736x/71/1e/da/711eda25308c65a7756751088866e181.jpg", "imagem_padrao.jpg")


# historico = buscar_historico_precos(resumo=True)

# print(historico)