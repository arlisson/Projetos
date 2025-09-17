import logging
import os
from datetime import datetime, timedelta
import inspect

# Configurações
LOG_DIR = "logs"
LOG_FILE_ERROS = os.path.join(LOG_DIR, "log_erros.txt")
LOG_FILE_INFO = os.path.join(LOG_DIR, "log_info.txt")
ROTACAO_MENSAL = True  # Ativa ou desativa limpeza mensal

# Cria a pasta "logs" se não existir
os.makedirs(LOG_DIR, exist_ok=True)


def verificar_data_ultimo_log(log_file: str):
    """
    Lê a última data do log e limpa o arquivo se a última entrada for de 1 mês atrás ou mais.
    """
    if not os.path.exists(log_file):
        return  # Nada a fazer se o log ainda não existe

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            linhas = f.readlines()

        for linha in reversed(linhas):
            try:
                data_str = linha.split(" [")[0].strip()
                data_log = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S,%f")
                if datetime.now() - data_log >= timedelta(days=30):
                    with open(log_file, "w", encoding="utf-8") as f:
                        f.write("")  # Apaga o conteúdo
                break
            except:
                continue
    except Exception as e:
        registrar_erro(f"[log.py] Erro ao verificar rotação de log: {e}")


# Rotação (se ativada)
if ROTACAO_MENSAL:
    verificar_data_ultimo_log(LOG_FILE_ERROS)
    verificar_data_ultimo_log(LOG_FILE_INFO)


# Configuração separada para INFO
logger_info = logging.getLogger("info_logger")
logger_info.setLevel(logging.INFO)
info_handler = logging.FileHandler(LOG_FILE_INFO, encoding="utf-8")
info_handler.setFormatter(logging.Formatter("%(asctime)s [INFO] - %(message)s"))
logger_info.addHandler(info_handler)


# Configuração separada para ERRO
logger_erro = logging.getLogger("erro_logger")
logger_erro.setLevel(logging.ERROR)
erro_handler = logging.FileHandler(LOG_FILE_ERROS, encoding="utf-8")
erro_handler.setFormatter(logging.Formatter("%(asctime)s [ERROR] - %(message)s"))
logger_erro.addHandler(erro_handler)


def log_info(mensagem: str):
    """
    Registra uma mensagem informativa no log_info.txt
    """
    logger_info.info(mensagem)


def registrar_erro(mensagem: str, exception: Exception = None):
    frame = inspect.currentframe().f_back
    func_name = frame.f_code.co_name
    cls_name = frame.f_locals.get("self", None).__class__.__name__ if "self" in frame.f_locals else ""
    prefix = f"{cls_name}.{func_name}" if cls_name else func_name

    if exception:
        logger_erro.error(f"[{prefix}] {mensagem} | Exceção: {str(exception)}")
    else:
        logger_erro.error(f"[{prefix}] {mensagem}")

