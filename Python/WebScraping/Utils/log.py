import logging
import os
from datetime import datetime, timedelta

# Configurações
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "log_erros.txt")
ROTACAO_MENSAL = True  # Ativa ou desativa limpeza mensal

def registrar_erro(mensagem: str, exception: Exception = None):
    """
    Registra um erro com ou sem exceção anexada.
    """
    if exception:
        logging.error(f"{mensagem} | Exceção: {str(exception)}")
    else:
        logging.error(mensagem)

# Cria a pasta "logs" se não existir
os.makedirs(LOG_DIR, exist_ok=True)

def verificar_data_ultimo_log():
    """
    Lê a última data do log, e limpa o arquivo se a última entrada for de 1 mês atrás ou mais.
    """
    if not os.path.exists(LOG_FILE):
        return  # Nada a fazer se o log ainda não existe

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            linhas = f.readlines()

        # Procura a última linha com uma data válida
        for linha in reversed(linhas):
            try:
                data_str = linha.split(" [")[0].strip()
                data_log = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S,%f")
                if datetime.now() - data_log >= timedelta(days=30):
                    with open(LOG_FILE, "w", encoding="utf-8") as f:
                        f.write("")  # Apaga o conteúdo
                break
            except:
                continue  # Pula linhas que não contêm data válida
    except Exception as e:
        registrar_erro(f"[log.py] Erro ao verificar rotação de log: {e}")

# Chama verificação antes de configurar o logger
if ROTACAO_MENSAL:
    verificar_data_ultimo_log()

# Configuração do logger
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()  # Opcional: também exibe no console
    ]
)


