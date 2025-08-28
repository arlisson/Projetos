from scraping_cartas import *

cartas = buscar_carta("https://mypcards.com/yugioh/produto/263986/donzela-de-branco")
carta = buscar_por_raridade(cartas, "Secret Rare")[0]
print(carta)