from urllib import response
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, urljoin
import requests
from bs4 import BeautifulSoup
import cloudscraper
import asyncio
from playwright.sync_api import sync_playwright
import re

from Utils.log import log_info, registrar_erro

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

def buscar_carta_myp(url, chave=None):
    """
    Faz o scraping da página de uma carta no MyPCards e retorna os dados da carta.
    """
    try:
        dados = []
        response = SCRAPER.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")    

        # Nome
        nome_tag = soup.find("span", class_="subtitulo")
        nome_sem_tag = soup.find("h1", id="produto-nome")
        nome = nome_tag.get_text(strip=True) if nome_tag else nome_sem_tag.get_text(strip=True) if nome_sem_tag else "Desconhecido"

        # Imagem
        imagens = soup.find_all("img")
        imagem = imagens[3]["src"] if len(imagens) >= 4 else IMAGEM

        # Preço
        preco_tag = soup.find("span", class_="moeda")
        preco_minimo = preco_tag.get_text(strip=True) if preco_tag else "R$ 0,00"

        # Coleção
        colecao = soup.find_all("a", href=lambda h: h and "/yugioh/" in h)
        colecao_carta = colecao[23].text if len(colecao) > 23 else "Coleção não identificada"

        soup.find_all("div", class_="view-field")[3].text.strip()
        # Código
        try:
            codigo_carta = "_".join(imagem.split("/")[-2].split("_")[1:]) or soup.find_all("div", class_="view-field")[3].text.strip().split("Código")[-1].strip().split("yugioh_")[-1]
        except:
            codigo_carta = "Desconhecido"

        # Tabela de raridades/preços
        tabela = soup.find("table", class_="table table-striped table-bordered")
        if tabela and "Nenhum resultado foi encontrado." not in tabela.get_text():
            for linha in tabela.find_all("tr"):
                colunas = linha.find_all("td")
                valores = [coluna.get_text(strip=True) for coluna in colunas]

                if valores and len(valores) >= 5:
                    raridade = valores[1].split(",")[0]
                    preco = valores[4]

                    dados.append({
                        "imagem": imagem if imagem else IMAGEM,
                        "nome": nome,
                        "raridade": raridade,
                        "preco_atual": preco if preco else preco_minimo,
                        "codigo": codigo_carta,
                        "colecao": colecao_carta,
                        "origem": "MyPCards",
                        "link_site": url
                    })
        else:
            # fallback
            dados.append({
                "imagem": imagem,
                "nome": nome,
                "raridade": "Não encontrado",
                "preco_atual": preco_minimo,
                "codigo": codigo_carta,
                "colecao": colecao_carta,
                "origem": "MYPCards",
                "link_site": url
            })

        # Filtro por raridade
        if chave:
            chave = chave.lower()
            if len(dados) == 1:
                log_info(f"Encontrada 1 carta em buscar_carta_myp: {dados[0]['nome']}")
                return [dados[0]]
            return [item for item in dados if chave in item["raridade"].lower()]
        log_info(f"Encontradas {len(dados)} cartas em buscar_carta_myp: {nome}")
        return [dados[0]] if dados else []

    except requests.RequestException as e:
        registrar_erro("Erro ao fazer a requisição buscar carta MyPCards:", e)
        return []

    except Exception as e:
        registrar_erro("Erro inesperado ao processar página de carta:", e)
        return []



def buscar_produto_liga(url):
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
            "preco_atual": preco.strip() if preco else 0.00,
            "origem": "Liga Yu-Gi-Oh",
            "link_site": url
        }
        log_info(f"Produto encontrado em buscar_produto_liga: {produto.get('nome')}")
        return produto

    except Exception as e:
        registrar_erro("Erro ao fazer a requisição buscar produto Liga Yu-Gi-Oh:", e)
        return []


def _set_page(url: str, page: int) -> str:
    """Garante que o URL tenha ?...&page=N (substitui se já existir)."""
    p = urlparse(url)
    q = parse_qs(p.query, keep_blank_values=True)
    q["page"] = [str(page)]
    new_query = urlencode(q, doseq=True)
    return urlunparse(p._replace(query=new_query))

def buscar_cartas_colecao(url):
    try:
        base = "https://mypcards.com"
        dados_links = []
        cartas = []
        vistos = set()

        # headers opcionais úteis quando o endpoint é de "load more" (ajax)
        ajax_headers = dict(HEADERS)
        ajax_headers.update({
            "X-Requested-With": "XMLHttpRequest",
            "Referer": url,
            "Accept": "text/html, */*;q=0.1",
        })

        page = 1
        max_pages = 500  # proteção contra loop infinito

        while page <= max_pages:
            page_url = _set_page(url, page)
            log_info(f"Carregando página via endpoint: page={page} -> {page_url}")

            resp = SCRAPER.get(page_url, headers=ajax_headers)
            if resp.status_code != 200:
                log_info(f"Parando: status {resp.status_code} em page={page}")
                break

            soup = BeautifulSoup(resp.text, "html.parser")
            itens = soup.find_all("a", class_="card-img-link")

            # condição de parada pedida: quando a página retornar 0 cartas
            if not itens or len(itens) == 0:
                log_info(f"Nenhuma carta encontrada em page={page}. Encerrando paginação.")
                break

            novos = 0
            for item in itens:
                href = item.get("href", "") or ""
                if "outros" in href.lower():
                    continue
                link_completo = urljoin(base, href)
                if link_completo in vistos:
                    continue
                vistos.add(link_completo)
                dados_links.append({
                    "id": len(dados_links) + 1,
                    "link": link_completo
                })
                novos += 1

            log_info(f"page={page}: {len(itens)} cartas no HTML, {novos} links novos.")

            page += 1  # próxima página

        # 📥 Coleta os dados de cada carta
        for link in dados_links:
            try:
                carta = buscar_carta_myp(link["link"])
                if carta:
                    cartas.append(carta[0])  # pega a primeira variação (ou ajuste sua regra)
            except Exception as e:
                registrar_erro(f"Erro ao buscar carta: {link['link']}", e)

        log_info(f"Total de cartas encontradas em buscar_cartas_colecao: {len(cartas)} "
                 f"(links únicos coletados: {len(dados_links)})")
        return cartas

    except Exception as e:
        registrar_erro("Erro ao fazer a requisição em buscar_cartas_colecao", e)
        return []