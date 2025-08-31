import requests
from bs4 import BeautifulSoup
import cloudscraper
import asyncio
from playwright.sync_api import sync_playwright

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
IMAGEM = 'https://i.pinimg.com/736x/71/1e/da/711eda25308c65a7756751088866e181.jpg'

def buscar_carta(url, chave):
    """
    Faz scraping da página de um produto no mypcards,
    filtra por raridade e retorna uma lista de dicionários com nome, imagem, raridade e preço.
    """
    try:
        dados = []
        response = SCRAPER.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")    

        # Nome e imagem
        nome = soup.find("span", class_="subtitulo").get_text(strip=True)
        imagem = soup.find_all("img")[3]["src"]
        preco_minimo = soup.find("span", class_="moeda").get_text(strip=True)        
        colecao = soup.find_all("a", href=lambda h: h and "/yugioh/" in h)        

        colecao_carta = colecao[23].text
        codigo_carta = imagem.split("/")[-2].split("_")[1]
       
        # Tabela de preços/raridades
        tabela = soup.find("table", class_="table table-striped table-bordered")

        if tabela and "Nenhum resultado foi encontrado." not in tabela.get_text():
            for linha in tabela.find_all("tr"):
                colunas = linha.find_all("td")
                valores = [coluna.get_text(strip=True) for coluna in colunas]        

                if valores:
                    raridade = valores[1].split(",")[0]  # antes da vírgula
                    preco = valores[4]

                    dados.append({
                        "imagem": imagem if imagem else IMAGEM,
                        "nome": nome,
                        "raridade": raridade,
                        "preco": preco if preco else preco_minimo,
                        "codigo": codigo_carta,
                        "colecao": colecao_carta
                    })
        else:
            dados.append({
                "imagem": IMAGEM,
                "nome": nome,
                "raridade": "Não encontrado",
                "preco": preco_minimo,
                "codigo": codigo_carta,
                "colecao": colecao_carta
            })

        # Filtro por raridade
        chave = chave.lower()
        if len(dados) == 1:
            return [{
                "imagem": IMAGEM,
                "nome": nome if nome else "Não encontrado",
                "raridade": "Não encontrado",
                "preco": preco_minimo,
                "codigo": codigo_carta,
                "colecao": colecao_carta
            }]

        return [item for item in dados if chave in item["raridade"].lower()]

    except requests.RequestException as e:
        print("Erro ao fazer a requisição:", e)
        return []


def buscar_produtos(url):
    try:               
        resultados = SESSION.get(url, headers=HEADERS)
        cookies = SESSION.cookies.get_dict()
        resultados = SESSION.get(url, headers=HEADERS, cookies=cookies)
        soup = BeautifulSoup(resultados.content, "html.parser")
        produtos = soup.find_all("div", class_="item-name")
        imagem = soup.find("img", id="featuredImage")     
     
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # Sem janela
            page = browser.new_page()
            page.goto(url)
            page.wait_for_selector(".price")  # Espera o JS renderizar o preço
            preco = page.locator(".price").first.text_content()          

            browser.close()
        produto = {
            "imagem": "https:" + imagem["src"] if imagem else IMAGEM,
            "nome": produtos[0].text.strip() if produtos else "Não encontrado",
            "preco": preco.strip() if preco else 0.00,
            
        }

        return produto

    except Exception as e:
        print("Erro ao fazer a requisição:", e)
        return []
    