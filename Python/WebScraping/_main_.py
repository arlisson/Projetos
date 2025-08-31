from scraping_cartas import *

cartas = buscar_carta_myp("https://mypcards.com/yugioh/produto/187637/acao-de-gracas-dos-tokens", "Ultra Rare")

print(cartas[0])

produto = buscar_produto_liga('https://www.ligayugioh.com.br/?view=prod/view&pcode=131327&prod=Collector%20Set%20-%20Speed%20Duel:%20Battle%20City%20Finals')
print(produto)
