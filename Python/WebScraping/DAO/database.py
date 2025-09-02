import sqlite3
from datetime import datetime
from tkinter import messagebox

DB_PATH = "yugioh.db"
DATA_SCRAPING = datetime.today().strftime('%Y-%m-%d')
def conectar():
    return sqlite3.connect(DB_PATH)

from datetime import datetime

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
                data_scraping
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            float(dados.get("preco_atual")),       # preco atual
            DATA_SCRAPING                          # NOVO campo
        ))

        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao inserir carta: {e}")
        conn.rollback()
        conn.close()



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
        cursor.execute("SELECT id_colecao FROM colecao WHERE nome = ?", (nome,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado else None
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar coleção por nome: {e}")
        conn.close()
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
        cursor.execute("INSERT INTO colecao (nome, codigo) VALUES (?, ?)", (nome, codigo))
        conn.commit()
        novo_id = cursor.lastrowid
        conn.close()
        return novo_id
    except Exception as e:
        conn.rollback()
        conn.close()
        messagebox.showerror("Erro", f"Erro ao inserir coleção: {e}")
        return None

def buscar_todas_cartas():
    '''
    Busca todas as cartas no banco de dados.
    returns:
        list: Uma lista de dicionários contendo as informações das cartas.

    '''
    try:
            
        conn = conectar()
        cursor = conn.cursor()

        query = """
            SELECT
                *
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
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar todas as cartas: {e}")
        conn.close()
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
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar carta por texto: {e}")
        conn.close()
        return []

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
        messagebox.showerror("Erro", f"Erro ao calcular lucro de cartas em posse: {e}")
        conn.close()
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
        messagebox.showerror("Erro", f"Erro ao calcular lucro de cartas vendidas: {e}")
        conn.close()
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
        messagebox.showerror("Erro", f"Erro ao calcular valor total de cartas em posse: {e}")
        conn.close()
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
        messagebox.showerror("Erro", f"Erro ao calcular total vendido em cartas: {e}")
        conn.close()
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
            - data_scraping
            - origem
            - preco_atual
            - quantidade
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
                data_scraping, origem, preco_atual, quantidade,
                data_scraping
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        valores = (
            produto["nome_produto"],
            produto["link"],
            produto["imagem"],
            produto["preco_compra"],
            produto["data_scraping"],
            produto.get("origem", "Liga Yugioh"),  # padrão se não vier
            produto["preco_atual"],
            produto["quantidade"],
            DATA_SCRAPING
        )

        cursor.execute(query, valores)
        conn.commit()
        return cursor.lastrowid

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao inserir produto: {e}")
        conn.rollback()
        conn.close()
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
                FROM produto
                WHERE nome_produto LIKE ?
                ORDER BY id_produto DESC
            """, (f"%{filtro}%",))
        else:
            cursor.execute("""
                SELECT
                    *
                FROM produto
                ORDER BY id_produto DESC
            """)

        colunas = [desc[0] for desc in cursor.description]
        resultados = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]
        return resultados

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao listar produtos: {e}")
        conn.close()
        return []
    finally:
        conn.close()


def calcular_lucro_total_produtos_em_posse():
    '''
    Calcula o lucro total dos produtos em posse.
    returns:
        float: O lucro total dos produtos em posse, ou 0.0 se não houver produtos.
    '''
    query = """
        SELECT SUM((preco_atual - preco_compra) * quantidade) AS lucro_total
        FROM produto
        WHERE preco_atual IS NOT NULL AND preco_compra IS NOT NULL;
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query)
        resultado = cursor.fetchone()
        
        return resultado[0] if resultado[0] is not None else 0.0
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao calcular lucro de produtos em posse: {e}")
        conn.close()
        return None
    finally:
        conn.close()


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
        return resultado[0] if resultado[0] is not None else 0.0
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao calcular lucro de produtos vendidos: {e}")
        conn.close()
        return 0.0
    finally:
        conn.close()

def calcular_total_gasto_produtos():
    '''
    Calcula o total gasto em produtos em posse.
    returns:
        float: O total gasto em produtos, ou 0.0 se não houver produtos.
    '''
    query = """
        SELECT SUM(preco_compra * quantidade) AS valor_total
        FROM produto
        WHERE preco_compra IS NOT NULL;
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query)
        resultado = cursor.fetchone()
        return resultado[0] if resultado[0] is not None else 0.0
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao calcular valor total de produtos: {e}")
        conn.close()
        return None
    finally:
        conn.close()


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
            "colecao"
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
            ('Common',), ('Rare',), ('Super Rare',),
            ('Ultra Rare',), ('Secret Rare',), ('Quarter Century',)
        ]
        cursor.executemany("INSERT INTO raridade (nome) VALUES (?)", raridades)

        # Qualidades
        qualidades = [
            ('Nova',), ('Quase Nova',), ('Pouco Jogada',),
            ('Muito Jogada',), ('Danificada',)
        ]
        cursor.executemany("INSERT INTO qualidade (nome) VALUES (?)", qualidades)

        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao criar banco inicial: {e}")
        conn.rollback()
        conn.close()


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
        return None
    finally:
        conn.close()

def atualizar_carta(carta):
    query = """
        UPDATE carta
        SET link_site = ?, nome = ?, codigo = ?, preco_da_compra = ?, preco_atual = ?,
            data_da_compra = ?, quantidade = ?, imagem = ?, origem = ?,
            raridade = ?, qualidade = ?, colecao = ?, data_scraping = ?
        WHERE id_carta = ?;
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query, (
            carta["link_site"], carta["nome"], carta["codigo"],
            carta["preco_da_compra"], carta["preco_atual"],
            carta["data_da_compra"], carta["quantidade"],
            carta["imagem"], carta["origem"],
            carta["raridade"], carta["qualidade"],
            carta["colecao"],carta["data_scraping"],
            carta["id_carta"]
        ))
        conn.commit()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar carta: {e}")
        conn.rollback()
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
        SELECT * FROM produto WHERE id_produto = ?;
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
        return None
    finally:
        conn.close()

def atualizar_produto(produto):
    query = """
        UPDATE produto
        SET nome_produto = ?, link = ?, imagem = ?, preco_compra = ?,
            data_scraping = ?, origem = ?, preco_atual = ?, quantidade = ?
        WHERE id_produto = ?;
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query, (
            produto["nome_produto"], produto["link"], produto["imagem"],
            produto["preco_compra"], produto["data_scraping"],
            produto["origem"], produto["preco_atual"],
            produto["quantidade"], produto["id_produto"]
        ))
        conn.commit()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar produto: {e}")
        conn.rollback()
    finally:
        conn.close()

def deletar(id, tabela):
    query = f"DELETE FROM {tabela} WHERE id_{tabela} = ?;"
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(query, (id,))
        conn.commit()        
        return True
    except Exception as e:        
        conn.rollback()
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
        return 0
    finally:
        conn.close()