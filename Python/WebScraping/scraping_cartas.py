import requests
from bs4 import BeautifulSoup
import cloudscraper
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

SCRAPER = cloudscraper.create_scraper()
SESSION = requests.Session()

SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36"
})


def buscar_carta(url):
    """
    Faz scraping da página de um produto no mypcards
    e retorna uma lista de dicionários com nome, imagem, raridade e preço.
    """
    try:
        dados = []
        response = SCRAPER.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")    

        # Nome e imagem
        nome = soup.find("span", class_="subtitulo").get_text(strip=True)
        imagem = soup.find_all("img")[3]["src"]

        # Tabela de preços/raridades
        tabela = soup.find("table", class_="table table-striped table-bordered")   
        for linha in tabela.find_all("tr"):
            colunas = linha.find_all("td")
            valores = [coluna.get_text(strip=True) for coluna in colunas]        

            if valores:
                raridade = valores[1].split(",")[0]  # antes da vírgula
                preco = valores[4]

                dados.append({
                    "imagem": imagem,
                    "nome": nome,
                    "raridade": raridade,
                    "preco": preco
                })

        return dados

    except requests.RequestException as e:
        print("Erro ao fazer a requisição:", e)
        return []



def buscar_por_raridade(lista, chave):
    chave = chave.lower()
    return [item for item in lista if chave in item["raridade"].lower()]



def buscar_produtos(url):
    try:
        # with open("session_token.json", "r") as f:
        #     cookies = json.load(f)
        
        resultados = SESSION.get(url, headers=HEADERS)
        cookies = SESSION.cookies.get_dict()
        resultados = SESSION.get(url, headers=HEADERS, cookies=cookies)
        soup = BeautifulSoup(resultados.content, "html.parser")
        produtos = soup.find_all("div", class_="new-price price-with-image")

        return produtos

    except Exception as e:
        print("Erro ao fazer a requisição:", e)
        return []

resultado = buscar_produtos('https://www.ligayugioh.com.br/?view=prod/view&pcode=131327&prod=Collector%20Set%20-%20Speed%20Duel:%20Battle%20City%20Finals')

print(resultado)