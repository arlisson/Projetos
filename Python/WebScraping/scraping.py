import requests
from bs4 import BeautifulSoup
import cloudscraper

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

scraper = cloudscraper.create_scraper()

url = "https://mypcards.com/yugioh/produto/263986/donzela-de-branco"
try:
    response = scraper.get(url, headers=headers)
    print(response.status_code)  # Verifica se a requisição foi bem-sucedida
    soup = BeautifulSoup(response.content, "html.parser")
    precos = soup.find_all("span", class_="moeda")
    raridade = soup.find_all("td", class_="estoque-lista-nomeenfoil")
    imagem = soup.find_all("img")
    nome = soup.find("span", class_="subtitulo").get_text(strip=True)

    dados = []

    for r, p in zip(raridade, precos[4:]):
        dados.append({
            "raridade": r.get_text().split(",")[0].strip(),
            "preco": p.get_text(strip=True)
        })

    
       
except requests.RequestException as e:
    print("Erro ao fazer a requisição:", e)
    exit()

def buscar_por_raridade(lista, chave):
    chave = chave.lower()
    return [item for item in lista if chave in item["raridade"].lower()]



carta = buscar_por_raridade(dados, "Secret")[0]

print(f'Nome encontrado: {nome}')
print(carta["raridade"], "-", carta["preco"])
print(f'Imagem encontrada: {imagem[3]["src"]}')
