import sqlite3

DB_PATH = "yugioh.db"

def conectar():
    return sqlite3.connect(DB_PATH)

def inserir_carta(dados):
    '''
    Insere uma nova carta no banco de dados.
    '''
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
            preco_atual
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        dados.get("link_site"),
        dados.get("nome"),
        dados.get("colecao"),
        dados.get("codigo"),
        float(dados.get("preco")),             # preco pago
        dados.get("data_da_compra"),
        dados.get("raridade"),
        dados.get("qualidade"),
        int(dados.get("quantidade")),
        dados.get("imagem"),
        dados.get("origem", "MypCards"),
        float(dados.get("preco_atual"))        # preco atual correto agora ✅
    ))

    conn.commit()
    conn.close()


def buscar_valores_tabela(tabela):
    '''
    Busca os valores de uma tabela no banco de dados.

    args:
        tabela (str): O nome da tabela a ser consultada.

    returns:
        list: Uma lista de tuplas contendo os valores encontrados.
    '''
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id_{tabela}, nome FROM {tabela}")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def buscar_colecao_por_nome(nome):
    '''
    Busca uma coleção pelo nome.

    args:
        nome (str): O nome da coleção a ser buscada.
    returns:
        int: O ID da coleção, ou None se não encontrada.
    '''
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_colecao FROM colecao WHERE nome = ?", (nome,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

def inserir_colecao(nome, codigo=""):
    '''
    Insere uma nova coleção no banco de dados.

    args:
        nome (str): O nome da coleção.
        codigo (str): O código da coleção.

    returns:
        int: O ID da nova coleção inserida.
    '''
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO colecao (nome, codigo) VALUES (?, ?)", (nome, codigo))
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    return novo_id

import sqlite3

def buscar_todas_cartas():
    '''
    Busca todas as cartas no banco de dados.
    returns:
        list: Uma lista de dicionários contendo as informações das cartas.

    '''
    conn = conectar()
    cursor = conn.cursor()

    query = """
        SELECT
            imagem,
            nome,
            codigo,
            preco_da_compra, 
            preco_atual,
            data_da_compra,
            quantidade
        FROM carta
    """

    cursor.execute(query)
    resultados = cursor.fetchall()

    colunas = [desc[0] for desc in cursor.description]

    cartas = []
    for linha in resultados:
        carta = dict(zip(colunas, linha))
        cartas.append(carta)

    conn.close()
    return cartas

def buscar_carta_por_texto(texto):
    '''
    Busca uma carta pelo nome ou código.
    args:
        texto (str): O texto a ser buscado no nome ou código da carta.

    returns:
        list: Uma lista de dicionários contendo as informações das cartas encontradas.
    '''
    conn = conectar()
    cursor = conn.cursor()

    query = """
        SELECT
            imagem,
            nome,
            codigo,
            preco_da_compra,
            preco_atual,
            data_da_compra,
            quantidade
        FROM carta
        WHERE nome LIKE ? OR codigo LIKE ?
    """

    texto_param = f"%{texto}%"
    cursor.execute(query, (texto_param, texto_param))
    resultados = cursor.fetchall()

    colunas = [desc[0] for desc in cursor.description]
    cartas = [dict(zip(colunas, linha)) for linha in resultados]

    conn.close()
    return cartas

def calcular_lucro_total_cartas_em_posse():
    '''
    Calcula o lucro total das cartas em posse.
    returns:
        float: O lucro total das cartas em posse, ou 0.0 se não houver cartas.
    '''
    query = """
        SELECT SUM((preco_atual - preco_da_compra) * quantidade) AS lucro_total
        FROM carta
        WHERE preco_atual IS NOT NULL AND preco_da_compra IS NOT NULL;
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query)
        resultado = cursor.fetchone()
        return resultado[0] if resultado[0] is not None else 0.0
    except Exception as e:
        print("Erro ao calcular lucro de cartas em posse:", e)
        return None
    finally:
        conn.close()
    
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
        return resultado[0] if resultado[0] is not None else 0.0
    except Exception as e:
        print("Erro ao calcular lucro de cartas vendidas:", e)
        return None
    finally:
        conn.close()

def calcular_total_gasto_cartas():
    '''
    Calcula o total gasto em cartas.
    returns:
        float: O total gasto em cartas, ou 0.0 se não houver cartas.
    '''
    query = """
        SELECT SUM(preco_da_compra * quantidade) AS valor_total
        FROM carta
        WHERE preco_da_compra IS NOT NULL;
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query)
        resultado = cursor.fetchone()
        return resultado[0] if resultado[0] is not None else 0.0
    except Exception as e:
        print("Erro ao calcular valor total de cartas em posse:", e)
        return None
    finally:
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
        return resultado[0] if resultado[0] is not None else 0.0
    except Exception as e:
        print("Erro ao calcular total vendido em cartas:", e)
        return None
    finally:
        conn.close()