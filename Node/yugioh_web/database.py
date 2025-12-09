import sqlite3
from datetime import datetime
from tkinter import messagebox

from Utils.log import registrar_erro
from Utils.thread_lock_safe import com_lock

DB_PATH = "yugioh.db"
DATA_SCRAPING = datetime.today().strftime('%Y-%m-%d')

def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")  # Habilita as constraints de chave estrangeira
    return conn


def registrar_historico_generico(tipo="carta", id=None, preco=None, data=None, origem="MYPCards"):
    if tipo not in ["carta", "produto"]:
        raise ValueError("Tipo inválido. Use 'carta' ou 'produto'.")

    try:
        conn = conectar()
        cursor = conn.cursor()

        if tipo == "carta":
            cursor.execute("""
                INSERT INTO historico_precos (id_carta, id_produto, data, preco, origem)
                VALUES (?, NULL, ?, ?, ?)
            """, (id, data, preco, origem))
        else:  # tipo == "produto"
            cursor.execute("""
                INSERT INTO historico_precos (id_carta, id_produto, data, preco, origem)
                VALUES (NULL, ?, ?, ?, ?)
            """, (id, data, preco, origem))

        conn.commit()
        conn.close()

    except Exception as e:
        registrar_erro(f"Erro ao registrar histórico: {e}")
        conn.close()
        return


def update_historico_generico(tipo="carta", id=None, preco=None, data=None, origem="MYPCards"):
    if tipo not in ["carta", "produto"]:
        raise ValueError("Tipo inválido. Use 'carta' ou 'produto'.")

    try:
        conn = conectar()
        cursor = conn.cursor()

        if tipo == "carta":
            cursor.execute("""
                UPDATE historico_precos
                SET data = ?, preco = ?, origem = ?
                WHERE id_carta = ? AND data = (SELECT MAX(data) FROM historico_precos WHERE id_carta = ?)
            """, (data, preco, origem, id, id))
        else:  # tipo == "produto"
            cursor.execute("""
                UPDATE historico_precos
                SET data = ?, preco = ?, origem = ?
                WHERE id_produto = ? AND data = (SELECT MAX(data) FROM historico_precos WHERE id_produto = ?)
            """, (data, preco, origem, id, id))

        conn.commit()
        conn.close()

    except Exception as e:
        registrar_erro(f"Erro ao atualizar histórico: {e}")
        conn.close()
        return



def registrar_historico_lucro():
    conn = conectar()
    cursor = conn.cursor()
    resumo = buscar_historico_precos(resumo=True)
    try:
        # # Calcula lucro total
        # cursor.execute("""
        #     SELECT SUM((preco_atual - preco_da_compra) * quantidade) FROM carta
        # """)
        lucro_cartas = resumo.get("lucro_cartas", 0.0) + resumo.get("total_vendas_cartas", 0.0)

        # cursor.execute("""
        #     SELECT SUM((preco_atual - preco_compra) * quantidade) FROM produto
        # """)
        lucro_produtos = resumo.get("lucro_produtos", 0.0) + resumo.get("total_vendas_produtos", 0.0)

        total = lucro_cartas + lucro_produtos

        # Data atual sem hora
        data_hoje = DATA_SCRAPING

        # Verifica se já existe registro hoje
        cursor.execute("""
            SELECT id_lucro FROM historico_lucro
            WHERE DATE(data) = ?
        """, (data_hoje,))
        existente = cursor.fetchone()

        if existente:
            # Atualiza registro existente
            cursor.execute("""
                UPDATE historico_lucro
                SET lucro_cartas = ?, lucro_produtos = ?, lucro_total = ?
                WHERE id_lucro = ?
            """, (lucro_cartas, lucro_produtos, total, existente[0]))
        else:
            # Insere novo registro
            cursor.execute("""
                INSERT INTO historico_lucro (lucro_cartas, lucro_produtos, lucro_total, data)
                VALUES (?, ?, ?, ?)
            """, (lucro_cartas, lucro_produtos, total, DATA_SCRAPING))

        conn.commit()
    except Exception as e:
        registrar_erro(f"Erro ao registrar histórico de lucro: {e}")
    finally:
        conn.close()



def inserir_carta(dados):
    '''
    Insere uma nova carta no banco de dados, incluindo a data atual como data_scraping.
    args:
        dados (dict): Um dicionário contendo os dados da carta a ser inserida.

    returns:
        None
    '''
    try:
        conn = conectar()
        cursor = conn.cursor()

        

        cursor.execute("""
            INSERT INTO carta (
                link_site,
                nome,
                colecao,
                codigo,
                preco_da_compra,
                data_da_compra,
                raridade,
                qualidade,
                quantidade,
                imagem,
                origem,
                preco_atual,
                imagem_salva,
                data_scraping
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            dados.get("link_site"),
            dados.get("nome").upper(),
            dados.get("colecao"),
            dados.get("codigo").upper(),
            float(dados.get("preco_da_compra")),             # preco pago
            dados.get("data_da_compra"),
            dados.get("raridade"),
            dados.get("qualidade"),
            int(dados.get("quantidade")),
            dados.get("imagem"),
            dados.get("origem", "MYPCards"),
            float(dados.get("preco_atual")),       # preco atual
            dados.get("imagem_salva", ""),  # caminho da imagem salva localmente
            DATA_SCRAPING                          # NOVO campo
        ))
        
        conn.commit()              
        novo_id = cursor.lastrowid
        conn.close()
        registrar_historico_lucro()
        registrar_historico_generico(tipo="carta",
                                       id=novo_id,
                                       preco=dados.get("preco_atual"),
                                       data=DATA_SCRAPING,
                                       origem=dados.get("origem", "MYPCards"))
        return novo_id
    except Exception as e:
        
        conn.rollback()
        conn.close()
        registrar_erro("Erro ao inserir carta", e)



def buscar_raridade_qualidade_nome(nome, tabela):
    '''
    Busca o ID da raridade ou qualidade pelo nome.
    args:
        nome (str): O nome a ser buscado.
        tabela (str): "raridade" ou "qualidade".

    returns:
        int: O ID correspondente ao nome, ou None se não encontrado.
    '''
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(f"SELECT id_{tabela} FROM {tabela} WHERE nome = ?", (nome.upper(),))
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado else None
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar {tabela} por nome: {e}")
        conn.close()
        registrar_erro(f"Erro ao buscar {tabela} por nome", e)
        return None



def inserir_raridade_qualidade(nome, tabela):
    '''
    Insere uma nova raridade ou qualidade no banco de dados.
    args:
        nome (str): O nome a ser inserido.
        tabela (str): "raridade" ou "qualidade".

    returns:
        int: O ID da nova raridade ou qualidade inserida.
    '''
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {tabela} (nome) VALUES (?)", (nome.upper(),))
        conn.commit()
        novo_id = cursor.lastrowid
        conn.close()
        return novo_id
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao inserir {tabela}: {e}")
        conn.rollback()
        conn.close()
        registrar_erro(f"Erro ao inserir {tabela}", e)
        return None



def atualizar_raridade_qualidade(id, nome, tabela):
    '''
    Atualiza o nome de uma raridade ou qualidade existente.
    args:
        id (int): O ID a ser atualizado.
        nome (str): O novo nome.
        tabela (str): "raridade" ou "qualidade".

    returns:
        bool: True se a atualização foi bem-sucedida, False caso contrário.
    '''
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(f"UPDATE {tabela} SET nome = ? WHERE id_{tabela} = ?", (nome.upper(), id))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar {tabela}: {e}")
        conn.rollback()
        conn.close()
        registrar_erro(f"Erro ao atualizar {tabela}", e)
        return False



def buscar_raridade_qualidade_id(id, tabela):
    '''
    Busca o nome da raridade ou qualidade pelo ID.
    args:
        id (int): O ID a ser buscado.
        tabela (str): "raridade" ou "qualidade".

    returns:
        str: O nome correspondente ao ID, ou None se não encontrado.
    '''
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(f"SELECT nome FROM {tabela} WHERE id_{tabela} = ?", (id,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado else None
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar {tabela} por ID: {e}")
        conn.close()
        registrar_erro(f"Erro ao buscar {tabela} por ID", e)
        return None



def buscar_valores_tabela(tabela):
    '''
    Busca os valores de uma tabela no banco de dados.

    args:
        tabela (str): O nome da tabela a ser consultada.

    returns:
        list: Uma lista de tuplas contendo os valores encontrados.
    '''
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(f"SELECT id_{tabela}, nome FROM {tabela}")
        resultados = cursor.fetchall()
        conn.close()
        return resultados
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar valores da tabela {tabela}: {e}")
        conn.close()
        registrar_erro(f"Erro ao buscar valores da tabela {tabela}", e)
        return []


def buscar_colecao_por_nome(nome):
    '''
    Busca uma coleção pelo nome.

    args:
        nome (str): O nome da coleção a ser buscada.
    returns:
        int: O ID da coleção, ou None se não encontrada.
    '''
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_colecao FROM colecao WHERE nome = ?", (nome.upper(),))
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado else None
    except Exception as e:        
        conn.close()
        registrar_erro("Erro ao buscar coleção por nome", e)
        return None



def inserir_colecao(nome, codigo=""):
    '''
    Insere uma nova coleção no banco de dados.

    args:
        nome (str): O nome da coleção.
        codigo (str): O código da coleção.

    returns:
        int: O ID da nova coleção inserida.
    '''
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO colecao (nome, codigo) VALUES (?, ?)", (nome.upper(), codigo.upper()))
        conn.commit()
        novo_id = cursor.lastrowid
        conn.close()
        return novo_id
    except Exception as e:
        conn.rollback()
        conn.close()
        messagebox.showerror("Erro", f"Erro ao inserir coleção: {e}")
        registrar_erro("Erro ao inserir coleção", e)
        return None



def buscar_todas_cartas():
    """
    Retorna todas as cartas da view vw_cartas_detalhadas, sem cache interno.
    O cache é controlado externamente pela interface.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vw_cartas_detalhadas")
        resultados = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description]
        cartas = [dict(zip(colunas, linha)) for linha in resultados]
        conn.close()
        return cartas
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar todas as cartas: {e}")
        registrar_erro("Erro ao buscar todas as cartas", e)
        return []



def buscar_carta_por_texto(texto):
    '''
    Busca uma carta pelo nome ou código.
    args:
        texto (str): O texto a ser buscado no nome ou código da carta.

    returns:
        list: Uma lista de dicionários contendo as informações das cartas encontradas.
    '''
    try:
        conn = conectar()
        cursor = conn.cursor()

        query = """
            SELECT            
                *
            FROM vw_cartas_detalhadas
            WHERE (
                nome COLLATE NOCASE LIKE ? OR
                codigo COLLATE NOCASE LIKE ? OR
                qualidade_nome COLLATE NOCASE LIKE ? OR
                raridade_nome COLLATE NOCASE LIKE ?
            )
            ORDER BY id_carta DESC
        """

        texto_param = f"%{texto.strip()}%"
        cursor.execute(query, (texto_param.upper(),) * 4)
        resultados = cursor.fetchall()

        colunas = [desc[0] for desc in cursor.description]
        cartas = [dict(zip(colunas, linha)) for linha in resultados]

        conn.close()
        return cartas

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar carta por texto: {e}")
        conn.close()
        registrar_erro("Erro ao buscar carta por texto", e)
        return []



def calcular_lucro_total_cartas_em_posse():
    """
    Lucro total = lucro em posse (quantidade > 0) + lucro de vendas (snapshot da venda;
    se faltar custo na venda, usa custo da carta).
    """
    conn, cursor = None, None
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Lucro em posse: só itens com quantidade > 0
        cursor.execute("""
            SELECT COALESCE(SUM(
                     (COALESCE(preco_atual,0) - COALESCE(preco_da_compra,0))
                     * COALESCE(quantidade,0)
                   ), 0)
            FROM carta
            WHERE COALESCE(quantidade,0) > 0
        """)
        lucro_posse = cursor.fetchone()[0] or 0.0

        # Lucro de vendas:
        # usa preco_da_compra da venda; se NULL, usa o da carta.
        cursor.execute("""
            SELECT COALESCE(SUM(
                     (COALESCE(v.preco_da_venda,0) - COALESCE(v.preco_da_compra, c.preco_da_compra, 0))
                     * COALESCE(v.quantidade, 0)
                   ), 0)
            FROM venda v
            LEFT JOIN carta c ON c.id_carta = v.id_carta
        """)
        lucro_vendas = cursor.fetchone()[0] or 0.0

        return float(lucro_posse) + float(lucro_vendas)

    except Exception as e:
        registrar_erro(f"[calcular_lucro_total_cartas_em_posse] {e}")
        return 0.0
    finally:
        try:
            if cursor: cursor.close()
        except Exception:
            pass
        try:
            if conn: conn.close()
        except Exception:
            pass


 
def calcular_lucro_total_cartas_vendidas():
    '''
    Calcula o lucro total das cartas vendidas.
    returns:
        float: O lucro total das cartas vendidas, ou 0.0 se não houver cartas.
    '''
    query = """
        SELECT SUM((preco_da_venda - preco_da_compra) * quantidade) AS lucro_total
        FROM venda
        WHERE preco_da_venda IS NOT NULL AND preco_da_compra IS NOT NULL;
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query)
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado[0] is not None else 0.0
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao calcular lucro de cartas vendidas: {e}")
        conn.close()
        registrar_erro("Erro ao calcular lucro de cartas vendidas", e)
        return None
    finally:
        conn.close()



def calcular_total_gasto_cartas():
    '''
    Calcula o total gasto em cartas (em posse + vendidas).
    Returns:
        float: O total gasto em cartas, ou 0.0 se não houver dados.
    '''
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Total gasto em cartas em posse
        query_posse = """
            SELECT SUM(preco_da_compra * quantidade) AS valor_posse
            FROM carta
            WHERE preco_da_compra IS NOT NULL;
        """
        cursor.execute(query_posse)
        resultado_posse = cursor.fetchone()
        total_posse = resultado_posse[0] if resultado_posse[0] is not None else 0.0

        # Total gasto em cartas vendidas
        query_vendas = """
            SELECT SUM(preco_da_compra * quantidade) AS valor_vendas
            FROM venda
            WHERE preco_da_compra IS NOT NULL;
        """
        cursor.execute(query_vendas)
        resultado_vendas = cursor.fetchone()
        total_vendas = resultado_vendas[0] if resultado_vendas[0] is not None else 0.0

        return total_posse + total_vendas

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao calcular valor total de cartas: {e}")
        registrar_erro("Erro ao calcular valor total de cartas", e)
        return 0.0

    finally:
        if conn:
            conn.close()



def calcular_total_vendido_cartas():
    '''
    Calcula o total vendido em cartas.
    returns:
        float: O total vendido em cartas, ou 0.0 se não houver cartas.
    '''
    query = """
        SELECT SUM(preco_da_venda * quantidade) AS total_vendido
        FROM venda
        WHERE preco_da_venda IS NOT NULL;
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query)
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado[0] is not None else 0.0
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao calcular total vendido em cartas: {e}")
        conn.close()
        registrar_erro("Erro ao calcular total vendido em cartas", e)
        return None
    finally:
        conn.close()



def inserir_produto(produto):
    """
    Insere um novo produto no banco de dados.

    Args:
        produto (dict): Dicionário com as chaves:
            - nome_produto
            - link
            - imagem
            - preco_compra
            - data_compra
            - origem
            - preco_atual
            - quantidade
            - imagem_salva
            - data_scraping

    Returns:
        int: ID do produto inserido (ou None se falhar)
    """
    try:
        conn = conectar()
        cursor = conn.cursor()

        query = """
            INSERT INTO produto (
                nome_produto, link, imagem, preco_compra,
                data_compra, origem, preco_atual, quantidade, imagem_salva,
                data_scraping
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        valores = (
            produto["nome_produto"].upper(),
            produto["link"],
            produto["imagem"],
            produto["preco_compra"],
            produto["data_compra"],
            produto.get("origem", "LIGA YUGIOH").upper(),  # padrão se não vier
            produto["preco_atual"],
            produto["quantidade"],
            produto.get("imagem_salva", ""),  # caminho da imagem salva localmente
            DATA_SCRAPING
        )

        cursor.execute(query, valores)
        conn.commit()
        novo_id = cursor.lastrowid
        conn.close()
        registrar_historico_lucro()
        registrar_historico_generico(tipo="produto",
                                       id=novo_id,
                                       preco=produto["preco_atual"],
                                       data=DATA_SCRAPING,
                                       origem=produto.get("origem", "LIGA YUGIOH").upper())

        return novo_id

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao inserir produto: {e}")
        conn.rollback()
        conn.close()
        registrar_erro("Erro ao inserir produto", e)
        return None

    finally:
        conn.close()



def listar_todos_produtos(filtro=""):
    """
    Lista todos os produtos cadastrados no banco de dados.
    args:
        filtro (str): Um filtro opcional para buscar produtos pelo nome.
    returns:
        list: Uma lista de dicionários representando os produtos.

    """
    try:
        conn = conectar()
        cursor = conn.cursor()

        if filtro:
            cursor.execute("""
                SELECT
                   *
                FROM vw_produtos_detalhados
                WHERE nome_produto LIKE ?
                ORDER BY id_produto DESC
            """, (f"%{filtro.upper()}%",))
        else:
            cursor.execute("""
                SELECT
                    *
                FROM vw_produtos_detalhados
                ORDER BY id_produto DESC
            """)

        colunas = [desc[0] for desc in cursor.description]
        resultados = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]
        conn.close()
        return resultados

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao listar produtos: {e}")
        conn.close()
        registrar_erro("Erro ao listar produtos", e)
        return []
    finally:
        conn.close()


def calcular_lucro_total_produtos_em_posse():
    """
    Lucro total = lucro em posse (quantidade > 0) + lucro de vendas (snapshot da venda_produto;
    se faltar custo na venda, usa custo do produto).
    """
    conn, cursor = None, None
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Lucro em posse: apenas itens com quantidade > 0
        cursor.execute("""
            SELECT COALESCE(SUM(
                     (COALESCE(preco_atual,0) - COALESCE(preco_compra,0))
                     * COALESCE(quantidade,0)
                   ), 0)
            FROM produto
            WHERE COALESCE(quantidade,0) > 0
        """)
        lucro_posse = cursor.fetchone()[0] or 0.0

        # Lucro de vendas (venda_produto):
        # usa preco_compra da venda; se NULL, usa o preco_compra do produto.
        cursor.execute("""
            SELECT COALESCE(SUM(
                     (COALESCE(v.preco_venda,0) - COALESCE(v.preco_compra, p.preco_compra, 0))
                     * COALESCE(v.quantidade, 0)
                   ), 0)
            FROM venda_produto v
            LEFT JOIN produto p ON p.id_produto = v.id_produto
        """)
        lucro_vendas = cursor.fetchone()[0] or 0.0

        return float(lucro_posse) + float(lucro_vendas)

    except Exception as e:
        registrar_erro(f"[calcular_lucro_total_produtos_em_posse] {e}")
        return 0.0
    finally:
        try:
            if cursor: cursor.close()
        except Exception:
            pass
        try:
            if conn: conn.close()
        except Exception:
            pass

def calcular_lucro_total_produtos_vendidos():
    '''
    Calcula o lucro total dos produtos vendidos.
    returns:
        float: O lucro total dos produtos vendidos, ou 0.0 se não houver produtos.
    '''
    query = """
        SELECT SUM((preco_venda - preco_compra) * quantidade) AS lucro_total
        FROM venda_produto
        WHERE preco_venda IS NOT NULL AND preco_compra IS NOT NULL;
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query)
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado[0] is not None else 0.0
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao calcular lucro de produtos vendidos: {e}")
        conn.close()
        registrar_erro("Erro ao calcular lucro de produtos vendidos", e)
        return 0.0
    finally:
        conn.close()


def calcular_total_gasto_produtos():
    """
    Calcula o total gasto em produtos (estoque + vendidos).
    Retorna:
        float: total gasto.
    """
    conn, cursor = None, None
    try:
        conn = conectar()
        cursor = conn.cursor()

        # 1) Gasto no estoque (inclui itens com quantidade = 0; não perde histórico)
        cursor.execute("""
            SELECT COALESCE(SUM(COALESCE(preco_compra,0) * COALESCE(quantidade,0)), 0)
            FROM produto
        """)
        gasto_estoque = cursor.fetchone()[0] or 0.0

        # 2) Gasto dos vendidos (preferindo snapshot do custo na venda_produto)
        #    Se a coluna v.preco_compra não existir, faz fallback para p.preco_compra.
        try:
            cursor.execute("""
                SELECT COALESCE(SUM(COALESCE(v.preco_compra,0) * COALESCE(v.quantidade,0)), 0)
                FROM venda_produto v
            """)
            gasto_vendidos = cursor.fetchone()[0] or 0.0
        except Exception:
            # Fallback: usa custo do produto no momento conhecido (se não houver snapshot na venda)
            cursor.execute("""
                SELECT COALESCE(SUM(COALESCE(p.preco_compra,0) * COALESCE(v.quantidade,0)), 0)
                FROM venda_produto v
                LEFT JOIN produto p ON p.id_produto = v.id_produto
            """)
            gasto_vendidos = cursor.fetchone()[0] or 0.0

        return float(gasto_estoque) + float(gasto_vendidos)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao calcular total gasto em produtos: {e}")
        registrar_erro(f"[calcular_total_gasto_produtos] {e}")
        return 0.0
    finally:
        try:
            if cursor: cursor.close()
        except Exception:
            pass
        try:
            if conn: conn.close()
        except Exception:
            pass



def calcular_total_vendido_produtos():
    '''
    Calcula o total vendido em produtos.
    returns:
        float: O total vendido em produtos, ou 0.0 se não houver vendas.
    '''
    query = """
        SELECT SUM(preco_venda * quantidade) AS total_vendido
        FROM venda_produto
        WHERE preco_venda IS NOT NULL;
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query)
        resultado = cursor.fetchone()
        return resultado[0] if resultado[0] is not None else 0.0
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao calcular total vendido em produtos: {e}")
        conn.close()
        registrar_erro("Erro ao calcular total vendido em produtos", e)
        return 0.0
    finally:
        conn.close()



def calcular_total_valor_produtos():
    '''
    Calcula o valor atual total dos produtos em posse.
    returns:
        float: O valor atual, ou 0.0 se não houver produtos.
    '''
    query = """
        SELECT SUM(preco_atual * quantidade) AS total_atual
        FROM produto
        WHERE preco_atual IS NOT NULL;
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query)
        resultado = cursor.fetchone()
        return resultado[0] if resultado[0] is not None else 0.0
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao calcular valor total atual de produtos: {e}")
        conn.rollback()
        conn.close()
        registrar_erro("Erro ao calcular valor total atual de produtos", e)
        return 0.0
    finally:
        conn.close()



def apagar_todos_os_dados():
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Desabilitar restrições temporariamente
        cursor.execute("PRAGMA foreign_keys = OFF;")

        # Apagar os dados (ordem importa por causa das FK)
        tabelas = [
            "historico_precos",
            "venda_produto",
            "venda",
            "carta",
            "produto",
            "raridade",
            "qualidade",
            "colecao",
            "historico_lucro"
        ]

        for tabela in tabelas:
            cursor.execute(f"DELETE FROM {tabela};")
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{tabela}';")  # Zera autoincremento

        # Reabilitar restrições
        cursor.execute("PRAGMA foreign_keys = ON;")

        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Todos os dados foram apagados.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao apagar dados: {e}")
        conn.rollback()
        conn.close()
        registrar_erro("Erro ao apagar dados", e)



def criar_banco_inicial():
    """
    Cria o banco de dados inicial com as tabelas e dados padrão.
    args:
        None
    return:
        None
    """
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Raridades
        raridades = [
            ('COMMON',), ('RARE',), ('SUPER RARE',),
            ('ULTRA RARE',), ('SECRET RARE',), ('QUARTER CENTURY',)
        ]
        cursor.executemany("INSERT INTO raridade (nome) VALUES (?)", raridades)

        # Qualidades
        qualidades = [
            ('NOVA',), ('QUASE NOVA',), ('POUCO JOGADA',),
            ('MUITO JOGADA',), ('DANIFICADA',)
        ]
        cursor.executemany("INSERT INTO qualidade (nome) VALUES (?)", qualidades)
        
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Banco inicial criado com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao criar banco inicial: {e}")
        conn.rollback()
        conn.close()
        registrar_erro("Erro ao criar banco inicial", e)



def buscar_carta_por_id(id):
    """
    Busca uma carta pelo seu ID.
    args:
        id (int): O ID da carta a ser buscada.
    returns:
        dict: Os dados da carta, ou None se não encontrada.
    """
    query = """
        SELECT * FROM carta WHERE id_carta = ?;
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query, (id,))
        resultado = cursor.fetchone()
        if resultado:
            colunas = [desc[0] for desc in cursor.description]
            return dict(zip(colunas, resultado))
        return None
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar carta por ID: {e}")
        conn.close()
        registrar_erro("Erro ao buscar carta por ID", e)
        return None
    finally:
        conn.close()



def atualizar_carta(carta):
    query = """
        UPDATE carta
        SET link_site = ?, nome = ?, codigo = ?, preco_da_compra = ?, preco_atual = ?,
            data_da_compra = ?, quantidade = ?, imagem = ?, origem = ?,
            raridade = ?, qualidade = ?, colecao = ?, data_scraping = ?, imagem_salva = ?
        WHERE id_carta = ?;
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query, (
            carta["link_site"], carta["nome"].upper(), carta["codigo"].upper(),
            carta["preco_da_compra"], carta["preco_atual"],
            carta["data_da_compra"], carta["quantidade"],
            carta["imagem"], carta["origem"],
            carta["raridade"], carta["qualidade"],
            carta["colecao"], carta["data_scraping"],
            carta["imagem_salva"],
            carta["id_carta"]
        ))
        conn.commit()
        cursor.close()
        conn.close()
        registrar_historico_lucro()
        registrar_historico_generico(tipo="carta",
                                       id=carta["id_carta"],
                                       data=carta["data_scraping"],
                                       preco=carta["preco_atual"])
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar carta: {e}")
        conn.rollback()
        registrar_erro("Erro ao atualizar carta", e)
    finally:
        conn.close()



def buscar_produto_por_id(id):
    """
    Busca um produto pelo seu ID.
    args:
        id (int): O ID do produto a ser buscado.
    returns:
        dict: Os dados do produto, ou None se não encontrado.
    """
    query = """
        SELECT * FROM vw_produtos_detalhados WHERE id_produto = ?;
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query, (id,))
        resultado = cursor.fetchone()
        if resultado:
            colunas = [desc[0] for desc in cursor.description]
            return dict(zip(colunas, resultado))
        return None
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar produto por ID: {e}")
        conn.close()
        registrar_erro("Erro ao buscar produto por ID", e)
        return None
    finally:
        conn.close()



def atualizar_produto(produto):
    query = """
        UPDATE produto
        SET nome_produto = ?, link = ?, imagem = ?, preco_compra = ?,
            data_scraping = ?, origem = ?, preco_atual = ?, data_compra = ?, quantidade = ?,
            imagem_salva = ?
        WHERE id_produto = ?;
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query, (
            produto["nome_produto"].upper(), produto["link"], produto["imagem"],
            produto["preco_compra"], produto["data_scraping"],
            produto["origem"], produto["preco_atual"],
            produto["data_compra"], produto["quantidade"],
            produto["imagem_salva"],
            produto["id_produto"]
        ))
        conn.commit()
        cursor.close()
        conn.close()
        registrar_historico_lucro()
        registrar_historico_generico(tipo="produto",
                                       id=produto["id_produto"],
                                       data=produto["data_scraping"],
                                       preco=produto["preco_atual"])
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar produto: {e}")
        conn.rollback()
        registrar_erro("Erro ao atualizar produto", e)
    finally:
        conn.close()



def deletar(id, tabela, tipo="carta"):
    query = f"DELETE FROM {tabela} WHERE id_{tipo} = ?;"
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query, (id,))
        conn.commit()        
        return True
    except Exception as e:        
        conn.rollback()
        messagebox.showerror("Erro", f"Erro ao apagar dados: {e}")
        registrar_erro("Erro ao apagar dados", e)
        return False
    finally:
        conn.close()



def calcula_quantidade(tabela):
    query = f"SELECT SUM(quantidade) FROM {tabela};"
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query)
        resultado = cursor.fetchone()
        return resultado[0] if resultado else 0
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao calcular quantidade: {e}")
        conn.close()
        registrar_erro("Erro ao calcular quantidade", e)
        return 0
    finally:
        conn.close()



def inserir_venda_generica(id_item, quantidade_vendida, preco_venda, tipo="carta"):
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        data_hoje = datetime.today().strftime("%Y-%m-%d")

        if tipo == "carta":
            cursor.execute("SELECT * FROM carta WHERE id_carta = ?", (id_item,))
            dados = cursor.fetchone()
            if not dados:
                registrar_erro("Carta não encontrada para venda:", id_item)
                raise Exception("Carta não encontrada.")
            colunas = [desc[0] for desc in cursor.description]
            carta = dict(zip(colunas, dados))

            if quantidade_vendida > carta["quantidade"]:
                registrar_erro("Quantidade vendida maior do que o estoque para carta:", id_item)
                raise Exception("Quantidade vendida maior do que o estoque.")

            # Inserir na tabela de vendas
            cursor.execute("""
                INSERT INTO venda (
                    link_site, nome, colecao, codigo, preco_da_compra, data_da_compra,
                    raridade, qualidade, quantidade, data_da_venda, preco_da_venda,
                    imagem, origem, preco_atual, data_scraping, imagem_salva
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                carta["link_site"],
                carta["nome"].upper(),
                carta["colecao"],
                carta["codigo"],
                carta["preco_da_compra"],
                carta["data_da_compra"],
                carta["raridade"],
                carta["qualidade"],
                quantidade_vendida,
                data_hoje,
                preco_venda,
                carta["imagem"],
                carta["origem"],
                carta["preco_atual"],
                carta["data_scraping"],
                carta["imagem_salva"]
            ))

            # Atualizar estoque
            nova_quantidade = carta["quantidade"] - quantidade_vendida            
            cursor.execute("UPDATE carta SET quantidade = ? WHERE id_carta = ?", (nova_quantidade, id_item))
            

        elif tipo == "produto":
            cursor.execute("SELECT * FROM produto WHERE id_produto = ?", (id_item,))
            dados = cursor.fetchone()
            if not dados:
                registrar_erro("Produto não encontrado para venda:", id_item)
                raise Exception("Produto não encontrado.")
            colunas = [desc[0] for desc in cursor.description]
            produto = dict(zip(colunas, dados))

            if quantidade_vendida > produto["quantidade"]:
                registrar_erro("Quantidade vendida maior do que o estoque para produto:", id_item)
                raise Exception("Quantidade vendida maior do que o estoque.")

            # Inserir na tabela de vendas de produto
            cursor.execute("""
                INSERT INTO venda_produto (
                    nome_produto, link, imagem, preco_compra, data_compra,
                    preco_venda, data_venda, origem, preco_atual, quantidade, data_scraping, imagem_salva
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                produto["nome_produto"].upper(),
                produto["link"],
                produto["imagem"],
                produto["preco_compra"],
                produto["data_compra"],
                preco_venda,
                data_hoje,
                produto["origem"],
                produto["preco_atual"],
                quantidade_vendida,
                produto["data_scraping"],
                produto["imagem_salva"]
            ))

            # Atualizar estoque
            nova_quantidade = produto["quantidade"] - quantidade_vendida           
            cursor.execute("UPDATE produto SET quantidade = ? WHERE id_produto = ?", (nova_quantidade, id_item))
          

        else:
            registrar_erro("Tipo inválido para venda:", tipo)
            raise Exception("Tipo inválido. Use 'carta' ou 'produto'.")

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        registrar_erro("Erro ao inserir venda:", e)
        raise

    finally:
        conn.close()



def calcular_quantidade_vendida(tabela):
    query = f"SELECT SUM(quantidade) FROM {tabela};"
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query)
        resultado = cursor.fetchone()
        return resultado[0] if resultado else 0
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao calcular quantidade vendida: {e}")
        conn.close()
        registrar_erro("Erro ao calcular quantidade vendida", e)
        return 0
    finally:
        conn.close()



def listar_vendas(tipo='carta'):
    """
    Retorna a lista de vendas de cartas ou produtos, baseada nas views detalhadas.
    
    :param tipo: 'carta' ou 'produto'
    :return: Lista de dicionários com os dados das vendas
    """
    conn = conectar()
    cursor = conn.cursor()

    try:
        if tipo == 'carta':
            cursor.execute("SELECT * FROM vw_vendas_detalhadas ORDER BY data_da_venda DESC")
        elif tipo == 'produto':
            cursor.execute("SELECT * FROM vw_venda_produto_detalhado ORDER BY data_venda DESC")
        else:
            registrar_erro("Tipo inválido para listar vendas:", tipo)
            raise ValueError("Tipo inválido. Use 'carta' ou 'produto'.")

        resultados = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description]
        vendas = [dict(zip(colunas, linha)) for linha in resultados]

        return vendas

    except Exception as e:
        registrar_erro(f"Erro ao listar vendas ({tipo}):", e)
        return []

    finally:
        conn.close()
        


def listar_venda_por_id(id, tipo='carta'):
    """
    Retorna os detalhes de uma venda específica de carta ou produto pelo ID.
    
    :param id: ID da venda
    :param tipo: 'carta' ou 'produto'
    :return: Dicionário com os dados da venda ou None se não encontrada
    """
    conn = conectar()
    cursor = conn.cursor()

    try:
        if tipo == 'carta':
            cursor.execute("SELECT * FROM venda WHERE id_carta = ?", (id,))
        elif tipo == 'produto':
            cursor.execute("SELECT * FROM vw_venda_produto_detalhado WHERE id_produto = ?", (id,))
        else:
            registrar_erro("Tipo inválido para listar venda por ID:", tipo)
            raise ValueError("Tipo inválido. Use 'carta' ou 'produto'.")

        resultado = cursor.fetchone()
        if resultado:
            colunas = [desc[0] for desc in cursor.description]
            return dict(zip(colunas, resultado))
        return None

    except Exception as e:
        registrar_erro(f"Erro ao listar venda por ID ({tipo}):", e)
        return None

    finally:
        conn.close()



def listar_venda_filtro(tipo='carta', filtro=""):
    """
    Retorna a lista de vendas de cartas ou produtos, baseada nas views detalhadas, com filtro opcional.
    
    :param tipo: 'carta' ou 'produto'
    :param filtro: Texto para filtrar pelo nome do item vendido
    :return: Lista de dicionários com os dados das vendas
    """
    conn = conectar()
    cursor = conn.cursor()

    try:
        if tipo == 'carta':
            if filtro:
                cursor.execute("""
                    SELECT * FROM vw_vendas_detalhadas
                    WHERE 
                        nome LIKE ?
                    OR raridade_nome LIKE ?
                    OR codigo LIKE ?
                    OR qualidade_nome LIKE ?
                    ORDER BY data_da_venda DESC

                """, (f"%{filtro.upper()}%",)*4)
            else:
                cursor.execute("SELECT * FROM vw_vendas_detalhadas ORDER BY data_da_venda DESC")
        elif tipo == 'produto':
            if filtro:
                cursor.execute("""
                    SELECT * FROM vw_venda_produto_detalhado 
                    WHERE nome_produto LIKE ? 
                    ORDER BY data_venda DESC
                """, (f"%{filtro.upper()}%",))
            else:
                cursor.execute("SELECT * FROM vw_venda_produto_detalhado ORDER BY data_venda DESC")
        else:
            registrar_erro("Tipo inválido para listar vendas com filtro:", tipo)
            raise ValueError("Tipo inválido. Use 'carta' ou 'produto'.")

        resultados = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description]
        vendas = [dict(zip(colunas, linha)) for linha in resultados]

        return vendas

    except Exception as e:
        registrar_erro(f"Erro ao listar vendas com filtro ({tipo}):", e)
        return []

    finally:
        conn.close()



def atualizar_venda_generica(venda, tipo="carta"):
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        if tipo == "carta":
            cursor.execute("""
                UPDATE venda
                SET link_site = ?, nome = ?, colecao = ?, codigo = ?, preco_da_compra = ?, data_da_compra = ?,
                    raridade = ?, qualidade = ?, quantidade = ?, data_da_venda = ?, preco_da_venda = ?,
                    imagem = ?, origem = ?, preco_atual = ?, data_scraping = ?, imagem_salva = ?
                WHERE id_carta = ?
            """, (
                venda["link_site"],
                venda["nome"].upper(),
                venda["colecao"],
                venda["codigo"].upper(),
                venda["preco_da_compra"],
                venda["data_da_compra"],
                venda["raridade"],
                venda["qualidade"],
                venda["quantidade"],
                venda["data_da_venda"],
                venda["preco_da_venda"],
                venda["imagem"],
                venda["origem"],
                venda["preco_atual"],
                venda["data_scraping"],
                venda["imagem_salva"],
                venda["id_venda"]
            ))

        elif tipo == "produto":
            cursor.execute("""
                UPDATE venda_produto
                SET nome_produto = ?, link = ?, imagem = ?, preco_compra = ?, data_compra = ?,
                    preco_venda = ?, data_venda = ?, origem = ?, preco_atual = ?, quantidade = ?, data_scraping = ?, imagem_salva = ?
                WHERE id_produto = ?
            """, (
                venda["nome_produto"].upper(),
                venda["link"],
                venda["imagem"],
                venda["preco_compra"],
                venda["data_compra"],
                venda["preco_venda"],
                venda["data_venda"],
                venda["origem"],
                venda["preco_atual"],
                venda["quantidade"],
                venda["data_scraping"],
                venda["imagem_salva"],
                venda["id_produto"]
            ))

        else:
            registrar_erro("Tipo inválido para atualizar venda:", tipo)
            raise Exception("Tipo inválido. Use 'carta' ou 'produto'.")

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        registrar_erro("Erro ao atualizar venda:", e)
        messagebox.showerror("Erro", f"Erro ao atualizar venda: {e}")
        return False

    finally:
        conn.close()



def desativar_se_vinculado_ou_deletar(id_item, tabela, tipo="raridade"):
    """
    Em vez de deletar diretamente, verifica se há vínculos com cartas/vendas.
    Se houver, atualiza o nome para indicar desativado. Se não houver, deleta.

    Args:
        id_item (int): ID do item na tabela.
        tabela (str): Nome da tabela (ex: "raridade", "colecao", "qualidade").
        tipo (str): Tipo usado para mensagens/logs. Geralmente igual ao nome da tabela.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Verificar vínculo em carta e venda
        vinculado_carta = cursor.execute(
            f"SELECT COUNT(*) FROM carta WHERE {tabela} = ?", (id_item,)
        ).fetchone()[0]

        vinculado_venda = cursor.execute(
            f"SELECT COUNT(*) FROM venda WHERE {tabela} = ?", (id_item,)
        ).fetchone()[0]

        if vinculado_carta > 0 or vinculado_venda > 0:
            # Está vinculado: atualizar nome para marcar como desativado
            cursor.execute(f"SELECT nome FROM {tabela} WHERE id_{tabela} = ?", (id_item,))
            nome_atual = cursor.fetchone()[0]
            novo_nome = nome_atual + " (DESATIVADO)"

            cursor.execute(
                f"UPDATE {tabela} SET nome = ? WHERE id_{tabela} = ?",
                (novo_nome, id_item)
            )
            conn.commit()
            return "desativado"

        else:
            # Sem vínculos, pode excluir
            cursor.execute(f"DELETE FROM {tabela} WHERE id_{tabela} = ?", (id_item,))
            conn.commit()
            return "excluido"

    except Exception as e:
        registrar_erro(f"[Erro ao excluir/desativar {tipo}] {e}")
        return None

    finally:
        conn.close()



def buscar_historico_precos(tipo=None, id=None, resumo=False):
    conn = conectar()
    cursor = conn.cursor()

    def rows_como_dict(cursor, rows):
        colunas = [col[0] for col in cursor.description]
        return [dict(zip(colunas, row)) for row in rows]

    try:
        # =================== RESUMO (em posse) ===================
        if resumo:
            resultados = {}

            # Lucro (em posse) de cartas: (preco_atual - preco_da_compra) * quantidade, apenas quantidade > 0
            cursor.execute("""
                SELECT COALESCE(SUM( (COALESCE(preco_atual,0) - COALESCE(preco_da_compra,0))
                                     * COALESCE(quantidade,0) ), 0)
                FROM carta
                WHERE COALESCE(quantidade,0) > 0
            """)
            resultados["lucro_cartas"] = cursor.fetchone()[0] or 0.0

            # Lucro (em posse) de produtos: (preco_atual - preco_compra) * quantidade, apenas quantidade > 0
            cursor.execute("""
                SELECT COALESCE(SUM( (COALESCE(preco_atual,0) - COALESCE(preco_compra,0))
                                     * COALESCE(quantidade,0) ), 0)
                FROM produto
                WHERE COALESCE(quantidade,0) > 0
            """)
            resultados["lucro_produtos"] = cursor.fetchone()[0] or 0.0

            # Vendas realizadas de cartas (histórico de vendas não muda)
            cursor.execute("""
                SELECT COALESCE(SUM(COALESCE(preco_da_venda,0) * COALESCE(quantidade,0)), 0)
                FROM venda
            """)
            resultados["total_vendas_cartas"] = cursor.fetchone()[0] or 0.0

            # Vendas realizadas de produtos
            cursor.execute("""
                SELECT COALESCE(SUM(COALESCE(preco_venda,0) * COALESCE(quantidade,0)), 0)
                FROM venda_produto
            """)
            resultados["total_vendas_produtos"] = cursor.fetchone()[0] or 0.0

            # Lucro total em posse (cartas + produtos)
            resultados["lucro_total"] = (resultados.get("lucro_cartas", 0.0)
                                         + resultados.get("lucro_produtos", 0.0)
                                         + resultados.get("total_vendas_cartas", 0.0)
                                         + resultados.get("total_vendas_produtos", 0.0))

            return resultados

        # =================== HISTÓRICO POR ID (inalterado) ===================
        if tipo and id is not None:
            if tipo == "carta":
                cursor.execute("""
                    SELECT id_historico_precos, id_carta, data, preco, origem
                    FROM historico_precos
                    WHERE id_carta = ?
                    ORDER BY data
                """, (id,))
            elif tipo == "produto":
                cursor.execute("""
                    SELECT id_historico_precos, id_produto, data, preco, origem
                    FROM historico_precos
                    WHERE id_produto = ?
                    ORDER BY data
                """, (id,))
            else:
                raise ValueError("Tipo inválido. Use 'carta', 'produto', 'lucro' ou None.")
            rows = cursor.fetchall()
            return rows_como_dict(cursor, rows)

        # =================== HISTÓRICO GERAL (inalterado) ===================
        if tipo == "lucro":
            cursor.execute("""
                SELECT id_lucro, data, lucro_cartas, lucro_produtos, lucro_total
                FROM historico_lucro
                ORDER BY data
            """)
        else:
            cursor.execute("""
                SELECT id_historico_precos, id_carta, id_produto, data, preco, origem
                FROM historico_precos
                ORDER BY data
            """)
        rows = cursor.fetchall()
        return rows_como_dict(cursor, rows)

    except Exception as e:
        registrar_erro(f"Erro ao buscar histórico: {e}")
        return []
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass


def calcula_total_gasto():
    conn, cursor = None, None
    try:
        conn = conectar()
        cursor = conn.cursor()

        # --- Gasto em cartas que ainda estão no estoque (podem ter quantidade 0, não há problema) ---
        cursor.execute("""
            SELECT COALESCE(SUM(COALESCE(preco_da_compra,0) * COALESCE(quantidade,0)), 0)
            FROM carta
        """)
        gasto_cartas_estoque = cursor.fetchone()[0] or 0.0

        # --- Gasto em cartas já vendidas (usa snapshot salvo na tabela de vendas) ---
        # Requer coluna preco_da_compra na tabela de 'venda'
        cursor.execute("""
            SELECT COALESCE(SUM(COALESCE(preco_da_compra,0) * COALESCE(quantidade,0)), 0)
            FROM venda
        """)
        gasto_cartas_vendidas = cursor.fetchone()[0] or 0.0

        # --- Gasto em produtos no estoque ---
        cursor.execute("""
            SELECT COALESCE(SUM(COALESCE(preco_compra,0) * COALESCE(quantidade,0)), 0)
            FROM produto
        """)
        gasto_produtos_estoque = cursor.fetchone()[0] or 0.0

        # --- Gasto em produtos vendidos (se houver coluna de custo na venda_produto) ---
        # Ajuste o nome da coluna caso seja diferente (ex.: preco_da_compra_produto).
        try:
            cursor.execute("""
                SELECT COALESCE(SUM(COALESCE(preco_compra,0) * COALESCE(quantidade,0)), 0)
                FROM venda_produto
            """)
            gasto_produtos_vendidos = cursor.fetchone()[0] or 0.0
        except Exception:
            # Caso sua tabela de vendas de produto não guarde o custo, considere 0
            gasto_produtos_vendidos = 0.0

        total_gasto = (
            gasto_cartas_estoque + gasto_cartas_vendidas +
            gasto_produtos_estoque + gasto_produtos_vendidos
        )
        return total_gasto

    except Exception as e:
        registrar_erro(f"Erro ao calcular total gasto: {e}")
        return 0.0
    finally:
        try:
            if cursor: cursor.close()
        except Exception:
            pass
        try:
            if conn: conn.close()
        except Exception:
            pass



def buscar_cartas_em_estoque():
    try:
        with conectar() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT c.*, r.nome AS raridade_nome
                FROM carta c
                LEFT JOIN raridade r ON r.id_raridade = c.raridade
                WHERE IFNULL(c.quantidade, 0) > 0
            """)
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        try: cur.close()
        except: pass

def buscar_produtos_em_estoque():
    try:
        with conectar() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT p.*
                FROM produto p
                WHERE IFNULL(p.quantidade, 0) > 0
            """)
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        try: cur.close()
        except: pass
