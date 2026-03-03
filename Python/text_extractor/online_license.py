import hashlib
import json
import os
import time
import winreg
from typing import Tuple

import requests

APP_NAME = "LeadsApp"

API_URL = "https://script.google.com/macros/s/AKfycbznxprQ97DT5cYK2AXKSDNOr8N_kzi-YvZYiipHR0GXYnRUWhMhJFXm-8tcLqZ6DdG8/exec"

LICENSE_CACHE_FILE = "license_cache.json"

RENEW_EVERY_SECONDS = 24 * 3600         # revalidar a cada 24h
OFFLINE_GRACE_SECONDS = 3 * 24 * 3600   # tolerar 3 dias sem internet


def _ensure_dir(path: str) -> str:
    """
    Garante que um diretório exista, criando-o se necessário. O método utiliza a função os.makedirs para criar o diretório especificado no caminho fornecido, com a opção exist_ok=True para evitar erros se o diretório já existir. Após garantir que o diretório exista, o método retorna o caminho do diretório. Se a entrada for None ou vazia, o método retorna uma string vazia.
    Args:
        path (str): O caminho do diretório a ser garantido. O método irá criar esse diretório se ele não existir, e retornará o caminho do diretório garantido. Se a entrada for None ou vazia, o método retornará uma string vazia.

    Returns:
        str: O caminho do diretório garantido, que existe após a execução do método. Se a entrada for None ou vazia, retorna uma string vazia.
    """
    os.makedirs(path, exist_ok=True)
    return path


def _try_dir(base: str):
    """
    Tenta criar um subdiretório com o nome do aplicativo dentro de um caminho base fornecido, e verifica se é possível escrever nesse diretório criando um arquivo de teste temporário. O método constrói o caminho do diretório combinando o caminho base com o nome do aplicativo, e então utiliza a função os.makedirs para criar o diretório se ele não existir. Em seguida, ele tenta criar um arquivo de teste temporário dentro desse diretório para verificar se é possível escrever nele. Se a criação do diretório ou do arquivo de teste falhar, o método retorna None. Caso contrário, ele retorna o caminho do diretório criado com sucesso.
    Args:
        base (str): O caminho base onde o diretório será criado. O método tentará criar um subdiretório com o nome do aplicativo dentro desse caminho base, e verificará se é possível escrever nesse diretório criando um arquivo de teste temporário. Se a criação do diretório ou do arquivo de teste falhar, o método retornará None.

    Returns:
        _type_: O caminho do diretório criado com sucesso, ou None se a criação falhar.
    """
    try:
        d = os.path.join(base, APP_NAME)
        os.makedirs(d, exist_ok=True)
        test_file = os.path.join(d, f".write_test_{int(time.time())}.tmp")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("ok")
        os.remove(test_file)
        return d
    except Exception:
        return None


def app_state_dir() -> str:
    """
    Retorna o caminho do diretório de estado do aplicativo, onde dados como cache de licença podem ser armazenados. O método tenta criar um subdiretório com o nome do aplicativo dentro de vários caminhos base comuns (APPDATA, LOCALAPPDATA, PROGRAMDATA) e verifica se é possível escrever nesse diretório. Se nenhum dos caminhos base permitir a criação de um diretório gravável, o método cria um diretório com o nome do aplicativo dentro do diretório home do usuário. O resultado é um caminho de diretório garantido onde o aplicativo pode armazenar seus dados de estado.
    Returns:
        str: O caminho do diretório de estado do aplicativo, onde dados como cache de licença podem ser armazenados. O método tenta criar um subdiretório com o nome do aplicativo dentro de vários caminhos base comuns (APPDATA, LOCALAPPDATA, PROGRAMDATA) e verifica se é possível escrever nesse diretório. Se nenhum dos caminhos base permitir a criação de um diretório gravável, o método cria um diretório com o nome do aplicativo dentro do diretório home do usuário. O resultado é um caminho de diretório garantido onde o aplicativo pode armazenar seus dados de estado.
    """
    p1 = os.environ.get("APPDATA")
    if p1:
        d = _try_dir(p1)
        if d:
            return d

    p2 = os.environ.get("LOCALAPPDATA")
    if p2:
        d = _try_dir(p2)
        if d:
            return d

    p3 = os.environ.get("PROGRAMDATA") or r"C:\ProgramData"
    d = _try_dir(os.path.join(p3, APP_NAME, "user_root"))
    if d:
        return d

    d = os.path.join(os.path.expanduser("~"), APP_NAME)
    os.makedirs(d, exist_ok=True)
    return d


def cache_path() -> str:
    """
    Retorna o caminho completo do arquivo de cache de licença, que é construído combinando o diretório de estado do aplicativo (obtido pela função app_state_dir) com o nome do arquivo de cache definido na constante LICENSE_CACHE_FILE. O resultado é um caminho absoluto para o arquivo de cache onde os dados de licença podem ser armazenados e recuperados.
    Returns:
        str: O caminho completo do arquivo de cache de licença, que é construído combinando o diretório de estado do aplicativo (obtido pela função app_state_dir) com o nome do arquivo de cache definido na constante LICENSE_CACHE_FILE. O resultado é um caminho absoluto para o arquivo de cache onde os dados de licença podem ser armazenados e recuperados.
    """
    return os.path.join(app_state_dir(), LICENSE_CACHE_FILE)


def clear_cache() -> None:
    """
    Limpa o cache de licença removendo o arquivo de cache se ele existir. O método obtém o caminho do arquivo de cache usando a função cache_path, verifica se o arquivo existe e, se for encontrado, tenta removê-lo usando a função os.remove. Se ocorrer um erro durante a remoção do arquivo, o método ignora a exceção e continua, garantindo que o cache seja limpo sem causar falhas no aplicativo.
    """
    try:
        p = cache_path()
        if os.path.exists(p):
            os.remove(p)
    except Exception:
        pass


def now_ts() -> int:
    """
    Retorna o timestamp atual em segundos desde a época (1 de janeiro de 1970). O método utiliza a função time.time para obter o tempo atual em segundos como um número de ponto flutuante, e então converte esse valor para um inteiro antes de retorná-lo. O resultado é o número de segundos inteiros que se passaram desde a época, representando o momento atual.
    Returns:
        int: O timestamp atual em segundos desde a época (1 de janeiro de 1970), obtido usando a função time.time e convertido para um inteiro.
    """
    return int(time.time())


def load_cache() -> dict:
    """
    Carrega o cache de licença a partir do arquivo de cache, retornando um dicionário com os dados armazenados. O método tenta abrir o arquivo de cache usando o caminho obtido pela função cache_path, lê seu conteúdo como JSON e retorna o resultado como um dicionário. Se o arquivo não existir ou se ocorrer um erro durante a leitura ou a conversão do JSON, o método retorna um dicionário vazio, indicando que não há dados de cache disponíveis.
    Returns:
        dict: O conteúdo do cache de licença carregado a partir do arquivo de cache, ou um dicionário vazio se o arquivo não existir ou se ocorrer um erro ao ler o arquivo. O método tenta abrir o arquivo de cache usando o caminho obtido pela função cache_path, lê seu conteúdo como JSON e retorna o resultado como um dicionário. Se o arquivo não existir ou se ocorrer um erro durante a leitura ou a conversão do JSON, o método retorna um dicionário vazio.
    """
    try:
        with open(cache_path(), "r", encoding="utf-8") as f:
            return json.load(f) or {}
    except Exception:
        return {}


def save_cache(data: dict) -> None:
    """
    Salva os dados de licença no cache escrevendo um dicionário como JSON em um arquivo de cache. O método recebe um dicionário de dados, converte-o para uma string JSON formatada usando a função json.dump, e escreve essa string no arquivo de cache localizado pelo caminho obtido pela função cache_path. Se ocorrer um erro durante a escrita do arquivo, o método irá lançar uma exceção, indicando que o processo de salvamento do cache falhou.
    Args:
        data (dict): O dicionário de dados a ser salvo no cache de licença. O método irá converter esse dicionário para JSON e escrevê-lo no arquivo de cache usando o caminho obtido pela função cache_path. Se ocorrer um erro durante a escrita do arquivo, o método irá lançar uma exceção.
    """
    with open(cache_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_machine_guid() -> str:
    """
    Obtém o valor do MachineGuid do sistema a partir do registro do Windows. O método abre a chave de registro HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Cryptography, consulta o valor da chave "MachineGuid" e retorna esse valor como uma string. O MachineGuid é um identificador único para o computador, e é comumente usado para fins de licenciamento e identificação de dispositivos. Se ocorrer um erro ao acessar o registro ou ao obter o valor, o método irá lançar uma exceção, indicando que a obtenção do MachineGuid falhou.
    Returns:
        str: O valor do MachineGuid do sistema, obtido a partir do registro do Windows. O método abre a chave de registro HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Cryptography, consulta o valor da chave "MachineGuid" e retorna esse valor como uma string. Se ocorrer um erro ao acessar o registro ou ao obter o valor, o método irá lançar uma exceção.
    """
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
    val, _ = winreg.QueryValueEx(key, "MachineGuid")
    return str(val).strip()


def device_id() -> str:
    """
    Gera um identificador de dispositivo único a partir do valor do MachineGuid do sistema, utilizando o hash SHA-256 para criar um identificador seguro e consistente. O método obtém o MachineGuid usando a função get_machine_guid, converte esse valor para bytes usando a codificação UTF-8, e então calcula o hash SHA-256 desses bytes usando a função hashlib.sha256. O resultado é um hash hexadecimal em letras maiúsculas que representa o identificador único do dispositivo, que pode ser usado para fins de licenciamento e identificação de hardware.
    Returns:
        str:  O identificador do dispositivo, gerado a partir do valor do MachineGuid do sistema. O método obtém o MachineGuid usando a função get_machine_guid, converte esse valor para bytes usando a codificação UTF-8, e então calcula o hash SHA-256 desses bytes usando a função hashlib.sha256. O resultado é um hash hexadecimal em letras maiúsculas que representa o identificador único do dispositivo, que pode ser usado para fins de licenciamento e identificação de hardware.
    """
    return hashlib.sha256(get_machine_guid().encode("utf-8")).hexdigest().upper()


def call_api(action: str, email: str, dev_id: str) -> dict:
    """
    Faz uma chamada POST para a API de licenciamento, enviando um payload JSON com a ação, o e-mail do usuário e o identificador do dispositivo. O método constrói um dicionário de payload contendo os parâmetros fornecidos, e então utiliza a função requests.post para enviar esse payload como JSON para a URL da API definida na constante API_URL. A chamada tem um timeout de 15 segundos para evitar bloqueios prolongados. Após receber a resposta, o método verifica o status HTTP e o tipo de conteúdo da resposta para garantir que seja uma resposta JSON válida. Se a resposta indicar sucesso (status code 200 e Content-Type contendo "application/json"), o método retorna o conteúdo da resposta como um dicionário. Caso contrário, ele lança uma exceção RuntimeError com uma mensagem apropriada indicando o erro ocorrido.
    Args:
        action (str): A ação a ser realizada na API, como "activate" ou "renew", que indica o tipo de operação de licenciamento
        email (str): O e-mail do usuário para o qual a licença está sendo verificada ou ativada. O método inclui esse e-mail no payload enviado para a API, e é usado para identificar o usuário associado à licença.
        dev_id (str): O identificador do dispositivo, gerado a partir do MachineGuid do sistema, que é enviado no payload para a API de licenciamento. Esse identificador é usado para associar a licença a um dispositivo específico e garantir que as verificações de licença sejam feitas corretamente com base no hardware do usuário.

    Raises:
        RuntimeError: Se a resposta da API indicar um erro, como um status HTTP diferente de 200 ou um Content-Type que não contenha "application/json", o método lança uma exceção RuntimeError com uma mensagem que descreve o erro ocorrido, incluindo o status code e o conteúdo da resposta para facilitar a depuração. Se ocorrer um erro durante a chamada HTTP, como um timeout ou uma falha de conexão, a exceção correspondente será propagada para o chamador, indicando que a comunicação com a API falhou.
        RuntimeError: Se a resposta da API indicar um erro, como um status HTTP diferente de 200 ou um Content-Type que não contenha "application/json", o método lança uma exceção RuntimeError com uma mensagem que descreve o erro ocorrido, incluindo o status code e o conteúdo da resposta para facilitar a depuração. Se ocorrer um erro durante a chamada HTTP, como um timeout ou uma falha de conexão, a exceção correspondente será propagada para o chamador, indicando que a comunicação com a API falhou.

    Returns:
        dict: O conteúdo da resposta da API de licenciamento, retornado como um dicionário. O método faz uma chamada POST para a API, enviando um payload JSON com a ação, o e-mail do usuário e o identificador do dispositivo. Após receber a resposta, o método verifica o status HTTP e o tipo de conteúdo para garantir que seja uma resposta JSON válida. Se a resposta indicar sucesso (status code 200 e Content-Type contendo "application/json"), o método retorna o conteúdo da resposta como um dicionário. Caso contrário, ele lança uma exceção RuntimeError com uma mensagem apropriada indicando o erro ocorrido.
    """
    payload = {"action": action, "email": email, "device_id": dev_id}
    r = requests.post(API_URL, json=payload, timeout=15)

    ct = (r.headers.get("Content-Type") or "").lower()
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code}: {r.text[:400]}")
    if "application/json" not in ct:
        raise RuntimeError(f"Resposta não-JSON (Content-Type={ct}): {r.text[:400]}")

    return r.json()


def ensure_online_license(email: str) -> Tuple[bool, str, str]:
    """ 
    Verifica a validade da licença online para um usuário específico, utilizando o e-mail do usuário para consultar a API de licenciamento e retornando uma tupla com o resultado da verificação. O método processa o e-mail de entrada, obtém o identificador do dispositivo usando a função device_id, e então verifica se há um cache de licença válido que corresponda ao e-mail e ao dispositivo. Se um cache válido for encontrado, ele retorna um resultado positivo indicando que a licença é válida (True) junto com uma mensagem de "OK (cache)" e um código de status "ok_cache". Se não houver um cache válido, o método determina a ação apropriada ("activate" ou "renew") com base no estado do cache, e faz uma chamada para a API usando a função call_api. Dependendo da resposta da API, o método salva os dados no cache se a licença for válida, ou retorna mensagens de erro específicas para diferentes condições de falha (como "no_license", "blocked", "device_limit", etc.). O resultado final é uma tupla que indica se a licença é válida, uma mensagem descritiva do resultado, e um código de status que pode ser usado para identificar o resultado específico da verificação.

    Args:
        email (str): O e-mail do usuário para o qual a licença está sendo verificada ou ativada. O método inclui esse e-mail no payload enviado para a API, e é usado para identificar o usuário associado à licença.

    Returns:
        Tuple[bool, str, str]: Uma tupla contendo três elementos: um booleano indicando se a licença é válida (True) ou não (False), uma string com uma mensagem descritiva do resultado da verificação da licença, e uma string com um código de status que pode ser usado para identificar o resultado específico da verificação (como "ok", "no_license", "blocked", etc.). O método realiza a verificação da licença online, utilizando o e-mail fornecido para consultar a API de licenciamento, e retorna os resultados dessa verificação na forma de uma tupla estruturada.
    """
    email = (email or "").strip().lower()
    dev_id = device_id()

    cache = load_cache()
    cached_email = (cache.get("email") or "").strip().lower()
    cached_dev = (cache.get("device_id") or "").strip()
    last_ok = int(cache.get("last_ok_ts") or 0)

    age = (now_ts() - last_ok) if last_ok else 10**9

    if cached_email == email and cached_dev == dev_id and last_ok > 0 and age <= RENEW_EVERY_SECONDS:
        return True, "OK (cache)", "ok_cache"

    action = "activate" if last_ok == 0 or cached_email != email or cached_dev != dev_id else "renew"

    try:
        resp = call_api(action, email, dev_id)
    except Exception as e:
        if last_ok > 0 and cached_email == email and cached_dev == dev_id and age <= OFFLINE_GRACE_SECONDS:
            return True, "OK (offline grace)", "ok_offline_grace"
        return False, f"Falha ao validar licença: {type(e).__name__}: {e}", "network_error"

    if resp.get("ok") is True:
        save_cache({"email": email, "device_id": dev_id, "last_ok_ts": now_ts(), "last_resp": resp})
        return True, "OK", "ok"

    err = resp.get("error") or "unknown"

    if err == "no_license":
        return False, "E-mail não autorizado (sem licença).", "no_license"
    if err == "blocked":
        return False, "Acesso bloqueado para este e-mail.", "blocked"
    if err == "device_limit":
        md = resp.get("max_devices")
        return False, f"Limite de computadores atingido para este e-mail. (max={md})", "device_limit"
    if err == "not_activated":
        return False, "Este computador ainda não foi ativado para este e-mail.", "not_activated"
    if err == "revoked":
        return False, "Este computador foi revogado para este e-mail.", "revoked"

    return False, f"Licença inválida: {err}", "unknown"