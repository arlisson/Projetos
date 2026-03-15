import json
import os
import re
import time
from typing import Optional, Tuple

from PySide6.QtWidgets import QInputDialog, QMessageBox

APP_NAME = "LeadsApp"
LOGIN_FILE = "user_login.json"
LOGIN_MAX_AGE_SECONDS = 7 * 24 * 3600  # 7 dias (ajuste)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _ensure_dir(path: str) -> str:
    """ Garante que o diretório especificado exista, criando-o se necessário.

    Args:
        path (str): Caminho do diretório a ser criado, se não existir.

    Returns:
        str: O caminho do diretório garantido, que foi criado se não existia. Se o diretório já existia, retorna o mesmo caminho sem alterações.
    """
    os.makedirs(path, exist_ok=True)
    return path


def _try_dir(base: str) -> Optional[str]:
    """
    Tenta criar um diretório específico para o aplicativo dentro do diretório base fornecido. O método realiza um teste real de escrita para garantir que o diretório seja utilizável, evitando problemas com diretórios de roaming indisponíveis.
    Args:
        base (str): O caminho do diretório base onde o diretório do aplicativo deve ser criado. O método tentará criar um subdiretório com o nome do aplicativo dentro deste diretório base.

    Returns:
        Optional[str]: O caminho do diretório criado para o aplicativo se a criação e o teste de escrita forem bem-sucedidos. Se ocorrer qualquer erro durante a criação do diretório ou o teste de escrita, o método retorna None, indicando que o diretório não é utilizável.
    """
    try:
        d = os.path.join(base, APP_NAME)
        os.makedirs(d, exist_ok=True)

        # teste real de escrita (evita Roaming indisponível)
        test_file = os.path.join(d, f".write_test_{int(time.time())}.tmp")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("ok")
        os.remove(test_file)

        return d
    except Exception:
        return None


def app_state_dir() -> str:
    """
    Diretório de estado com fallback real:
    1) %APPDATA% (Roaming)
    2) %LOCALAPPDATA% (Local)
    3) %PROGRAMDATA%\\LeadsApp\\user_root\\LeadsApp

    Returns:
        str: O caminho do diretório de estado do aplicativo, determinado por meio de uma série de tentativas. O método verifica primeiro o diretório de roaming (%APPDATA%), seguido pelo diretório local (%LOCALAPPDATA%), e finalmente tenta criar um diretório específico para o aplicativo dentro do diretório de dados do programa (%PROGRAMDATA%). Se todas as tentativas falharem, o método retorna um caminho de fallback dentro do diretório do usuário.
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

    # fallback final extremo
    d = os.path.join(os.path.expanduser("~"), APP_NAME)
    os.makedirs(d, exist_ok=True)
    return d


def login_path() -> str:
    """
    Retorna o caminho completo do arquivo de login do aplicativo. O método constrói o caminho do arquivo de login combinando o diretório de estado do aplicativo, obtido por meio da função app_state_dir(), com o nome do arquivo de login definido pela constante LOGIN_FILE. O resultado é o caminho completo onde as informações de login do usuário serão armazenadas ou recuperadas.
    Returns:
        str: O caminho completo do arquivo de login do aplicativo.
    """
    return os.path.join(app_state_dir(), LOGIN_FILE)


def _now_ts() -> int:
    """ Retorna o timestamp atual em segundos desde a época Unix (1º de janeiro de 1970). O método utiliza a função time.time() para obter o tempo atual em segundos como um número de ponto flutuante, e em seguida converte esse valor para um inteiro, descartando a parte decimal. O resultado é o número total de segundos que se passaram desde a época Unix até o momento atual.
    Returns:
        int: O timestamp atual em segundos desde a época Unix.
    """
    return int(time.time())


def load_login() -> Tuple[Optional[str], Optional[int]]:
    """Carrega o e-mail e o timestamp do login salvo.

    Returns:
        Tuple[Optional[str], Optional[int]]: Uma tupla contendo o e-mail salvo (ou None se não houver) e o timestamp do login (ou None se não houver).
    """
    try:
        with open(login_path(), "r", encoding="utf-8") as f:
            data = json.load(f) or {}
        email = (data.get("email") or "").strip().lower() or None
        ts = data.get("ts")
        ts = int(ts) if ts is not None else None
        return email, ts
    except Exception:
        return None, None


def save_login(email: str) -> None:
    """Salva o e-mail do login com um timestamp atual.

    Args:
        email (str): O e-mail a ser salvo. O método irá limpar espaços em branco e converter o e-mail para letras minúsculas antes de salvar. O e-mail é armazenado junto com um timestamp que indica quando o login foi salvo, permitindo que o aplicativo determine se o login é válido ou expirado com base no tempo decorrido desde o último login.
    """
    data = {"email": email.strip().lower(), "ts": _now_ts()}
    with open(login_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def clear_login() -> None:
    """ Limpa o login salvo removendo o arquivo de login. O método tenta excluir o arquivo de login do sistema, que contém as informações de e-mail e timestamp do login. Se o arquivo existir, ele é removido, efetivamente limpando o login salvo. Se ocorrer qualquer erro durante a tentativa de remoção do arquivo (por exemplo, se o arquivo não existir ou se houver problemas de permissão), o método captura a exceção e continua sem bloquear o fluxo do programa, garantindo que a limpeza do login seja realizada de forma segura sem causar interrupções.
    """
    try:
        p = login_path()
        if os.path.exists(p):
            os.remove(p)
    except Exception:
        # não bloquear o fluxo por isso
        pass


def is_login_expired(ts: Optional[int]) -> bool:
    """ Verifica se o login é expirado com base no timestamp fornecido. O método compara o timestamp do login com o timestamp atual para determinar se o tempo decorrido desde o último login excede o limite definido por LOGIN_MAX_AGE_SECONDS. Se o timestamp fornecido for None, o método considera o login como expirado. Caso contrário, ele calcula a diferença entre o timestamp atual e o timestamp do login e verifica se essa diferença é maior que o limite de idade máxima do login.
    Args:
        ts (Optional[int]): O timestamp do login a ser verificado. Este valor representa o momento em que o login foi salvo e é usado para determinar se o login é válido ou expirado com base no tempo decorrido desde então.

    Returns:
        bool: Retorna True se o login for considerado expirado (ou seja, se o timestamp for None ou se o tempo decorrido desde o login exceder o limite definido por LOGIN_MAX_AGE_SECONDS), e False caso contrário (ou seja, se o login ainda for válido).
    """
    if ts is None:
        return True
    return (_now_ts() - ts) > LOGIN_MAX_AGE_SECONDS


def prompt_email(force: bool = False) -> Optional[str]:
    """
    Exibe um diálogo para o usuário inserir seu e-mail de login. O método verifica se há um e-mail salvo anteriormente e se ele ainda é válido (não expirado). Se houver um e-mail válido salvo, ele é retornado imediatamente, a menos que o parâmetro force seja definido como True, o que força o usuário a inserir um novo e-mail. Se não houver um e-mail válido salvo ou se force for True, o método exibe um diálogo de entrada para o usuário digitar seu e-mail. O método valida o formato do e-mail inserido usando uma expressão regular e continua solicitando até que um e-mail válido seja fornecido ou até que o usuário cancele a operação. Se um e-mail válido for inserido, ele é salvo para uso futuro e retornado pelo método. Se o usuário cancelar a operação, o método retorna None.
    Args:
        force (bool, optional): Se True, força o usuário a inserir um novo e-mail mesmo que haja um e-mail salvo válido. Defaults to False.

    Returns:
        Optional[str]: O e-mail inserido pelo usuário se for válido, ou o e-mail salvo anteriormente se ainda for válido, ou None se o usuário cancelar a operação.
    """
    saved_email, saved_ts = load_login()
    if (not force) and saved_email and not is_login_expired(saved_ts):
        return saved_email

    default_text = saved_email or ""
    while True:
        email, ok = QInputDialog.getText(None, "Login", "Digite seu e-mail:", text=default_text)
        if not ok:
            return None

        email = (email or "").strip().lower()
        if not email:
            QMessageBox.warning(None, "Atenção", "Informe um e-mail.")
            continue
        if not EMAIL_RE.match(email):
            QMessageBox.warning(None, "Atenção", "E-mail inválido.")
            continue

        save_login(email)
        return email