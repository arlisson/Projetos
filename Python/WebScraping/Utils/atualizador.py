import threading
from datetime import datetime
import json
import os

from rich import _console

from DAO.database import (    
    buscar_todas_cartas,
    buscar_produto_por_id,
    buscar_carta_por_id,
    atualizar_carta,
    atualizar_produto,
    registrar_historico_lucro,
    listar_todos_produtos,
    buscar_cartas_em_estoque,
    buscar_produtos_em_estoque
)
from Utils.limpar_preco import limpar_preco
from scraping.scraping_cartas import buscar_carta_myp, buscar_produto_liga
from Utils.log import registrar_erro, log_info

CAMINHO_JSON = "ultima_atualizacao.json"


def _ja_atualizado_hoje():
    try:
        if os.path.exists(CAMINHO_JSON):
            with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
                dados = json.load(f)
                return dados.get("data") == datetime.now().strftime("%Y-%m-%d")
        return False
    except:
        return False


def _marcar_como_atualizado():
    with open(CAMINHO_JSON, "w", encoding="utf-8") as f:
        json.dump({"data": datetime.now().strftime("%Y-%m-%d")}, f)


def _atualizar_precos_e_lucro(callback_status=None):
    """
    Realiza a atualização dos preços de cartas e produtos,
    atualiza os históricos e permite feedback visual via callback opcional.

    Args:
        callback_status (func): Função opcional para atualizar interface, como uma Label.
    """
    def atualizar_status(msg):
        if callable(callback_status):
            try:
                callback_status(msg)
            except:
                pass  # Silencia erros da UI

    try:
        cartas = buscar_cartas_em_estoque()
        total_cartas = len(cartas)

        atualizar_status("🔄 Atualizando cartas...")

        for i, carta in enumerate(cartas, start=1):
            id_carta = carta.get("id_carta")
            url = carta.get("link_site")           
            raridade = carta.get("raridade_nome", "")
            preco_old = carta.get("preco_atual", 0.0)
            codigo_carta = carta.get("codigo", "")    

            if not id_carta or not url:
                continue

            try:
                novas_infos = buscar_carta_myp(url,raridade)
                if novas_infos:
                    nova = novas_infos[0]
                    carta_atual = buscar_carta_por_id(id_carta)
                    if carta_atual:
                        nome = carta_atual.get("nome", "Carta")
                        atualizar_status(f"🔄 Atualizando carta ({i}/{total_cartas}): {nome}")
                        carta_atual["preco_atual"] = limpar_preco(nova.get("preco_atual", 0.0))
                        carta_atual["data_scraping"] = datetime.now().strftime("%Y-%m-%d")
                        if preco_old != carta_atual["preco_atual"]:
                            log_info(f"Preço alterado para carta {carta_atual.get('nome', 'Carta')} - {codigo_carta}: de {preco_old} para {carta_atual['preco_atual']}")
                        atualizar_carta(carta_atual)
                        #log_info(f"Atualizada carta {id_carta} - {nome}")
            except Exception as e:
                registrar_erro(f"Erro ao atualizar carta ID {id_carta}: {e}")

        produtos = buscar_produtos_em_estoque()
        total_produtos = len(produtos)
        
        atualizar_status("🔄 Atualizando produtos...")

        for i, produto in enumerate(produtos, start=1):
            id_produto = produto.get("id_produto")
            url = produto.get("link")
            preco_old_produto = produto.get("preco_atual", 0.0)
           

            if not id_produto or not url:
                continue

            try:
                nova_info = buscar_produto_liga(url)
                if nova_info:
                    produto_atual = buscar_produto_por_id(id_produto)
                    if produto_atual:
                        nome = produto_atual.get("nome_produto", "Produto")
                        atualizar_status(f"🔄 Atualizando produto ({i}/{total_produtos}): {nome}")
                        produto_atual["preco_atual"] = limpar_preco(nova_info.get("preco_atual", 0.0))
                        produto_atual["data_scraping"] = datetime.now().strftime("%Y-%m-%d")

                        if preco_old_produto != produto_atual["preco_atual"]:
                            log_info(f"Preço alterado para produto {produto_atual.get('nome_produto', 'Produto')}: de {preco_old_produto} para {produto_atual['preco_atual']}")
                        atualizar_produto(produto_atual)
                        
                        #log_info(f"Atualizado produto {id_produto} - {nome}")
            except Exception as e:
                registrar_erro(f"Erro ao atualizar produto ID {id_produto}: {e}")

        registrar_historico_lucro()
        _marcar_como_atualizado()
        atualizar_status("✅ Atualização concluída!")

    except Exception as e:
        registrar_erro(f"Erro geral ao atualizar preços e lucros: {e}")
        atualizar_status("❌ Erro ao atualizar preços.")


def iniciar_atualizacao_diaria(callback_status=None):
    """
    Inicia a atualização diária de forma assíncrona. Se já foi feita hoje, apenas loga.

    Args:
        callback_status (func): Função opcional para atualizar interface visual.
    """
    if _ja_atualizado_hoje():
        log_info(f"Atualização já feita hoje: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. Pulando.")
        if callable(callback_status):
            callback_status("✔️ Preços já atualizados hoje.")
        return

    thread = threading.Thread(
        target=_atualizar_precos_e_lucro,
        kwargs={'callback_status': callback_status},
        daemon=True
    )
    thread.start()
