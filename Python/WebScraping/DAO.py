import sqlite3

DB_PATH = "yugioh.db"

def conectar():
    return sqlite3.connect(DB_PATH)

def inserir_carta(dados):
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
        float(dados.get("preco")),
        dados.get("data_da_compra"),
        dados.get("raridade"),
        dados.get("qualidade"),
        int(dados.get("quantidade")),
        dados.get("imagem"),
        dados.get("origem", "MypCards"),
        float(dados.get("preco"))  # ou outro valor se diferente do de compra
    ))

    conn.commit()
    conn.close()

def buscar_valores_tabela(tabela):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id_{tabela}, nome FROM {tabela}")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def buscar_colecao_por_nome(nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_colecao FROM colecao WHERE nome = ?", (nome,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

def inserir_colecao(nome, codigo=""):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO colecao (nome, codigo) VALUES (?, ?)", (nome, codigo))
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    return novo_id

import sqlite3

def buscar_todas_cartas():
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
