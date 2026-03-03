import base64
import hashlib
import hmac
import os
import sys
import time
import ctypes
import ctypes.wintypes as wt
import winreg
from typing import Optional, Tuple
import shutil
from datetime import datetime

APP_NAME = "LeadsApp"

# Troque por um segredo longo e aleatório (64+ bytes).
# Ideal: gerar uma vez e NÃO mudar depois de distribuir, senão invalida os markers já gerados.
APP_SECRET = b"CHANGE_ME__PUT_A_LONG_RANDOM_SECRET_64_BYTES_MINIMUM________________"

# Marker SOMENTE LEITURA criado pelo instalador em: <pasta do app>\_internal\
# (não será escrito pelo app)
INTERNAL_DIR_NAME = "_internal"
INTERNAL_MARKER_FILE = "_internal.dat"  # o instalador deve criar este arquivo

# Marcador por máquina (gerado APENAS após validação online)
# C:\ProgramData\LeadsApp\cahce_string.dat
PROGRAMDATA_FILE = "cahce_string.dat"

# Registro (apenas status; não guarda token)
REG_PATH = r"Software\LeadsApp"
REG_STATE = "InstallState"
REG_FIRSTSEEN = "FirstSeen"
REG_MIDHASH = "MachineIdHash"


def _atomic_write_text(path: str, text: str) -> None:
    """
    Escreve texto em um arquivo de forma atômica, garantindo que o arquivo seja criado ou atualizado de maneira segura e consistente. O método cria um arquivo temporário com a extensão ".tmp" no mesmo diretório do arquivo de destino, escreve o texto nesse arquivo temporário, e então substitui o arquivo de destino pelo arquivo temporário usando os.replace, que é uma operação atômica no nível do sistema operacional. Isso garante que o arquivo de destino nunca fique em um estado parcialmente escrito, mesmo se ocorrer uma falha durante a escrita. O método também garante que o diretório do arquivo de destino exista antes de tentar escrever o arquivo.
    Args:
        path (str): O caminho do arquivo onde o texto será escrito de forma atômica.
        text (str): O texto a ser escrito no arquivo.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)

def _backup_file(path: str, reason: str) -> Optional[str]:
    """
    Faz um backup de um arquivo existente, copiando-o para um novo arquivo com um sufixo que inclui a razão do backup e um timestamp. O método verifica se o arquivo especificado existe, e se existir, ele gera um nome de arquivo de backup usando o nome original do arquivo, a razão fornecida e um timestamp no formato "YYYYMMDD-HHMMSS". O arquivo original é então copiado para o novo caminho de backup usando shutil.copy2, que preserva os metadados do arquivo. Se o backup for criado com sucesso, o caminho do arquivo de backup é retornado; caso contrário, se ocorrer um erro durante o processo de backup ou se o arquivo original não existir, o método retorna None.
    Args:
        path (str): O caminho do arquivo a ser copiado.
        reason (str): A razão do backup. Essa string é usada para criar o nome do arquivo de backup, indicando o motivo pelo qual o backup foi realizado (por exemplo, "before_update", "pre_install", etc.). O método inclui essa razão no nome do arquivo de backup para facilitar a identificação do propósito do backup posteriormente.

    Returns:
        Optional[str]: O caminho do arquivo de backup criado, ou None se o backup falhar ou o arquivo original não existir.
    """
    if not os.path.exists(path):
        return None
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    bak = f"{path}.{reason}.{ts}.bak"
    try:
        shutil.copy2(path, bak)
        return bak
    except Exception:
        return None

def _file_write_bytes(path: str, blob: bytes) -> None:
    """
    Escreve bytes em um arquivo de forma atômica, garantindo que o arquivo seja criado ou atualizado de maneira segura e consistente. O método cria um arquivo temporário com a extensão ".tmp" no mesmo diretório do arquivo de destino, escreve os bytes nesse arquivo temporário, e então substitui o arquivo de destino pelo arquivo temporário usando os.replace, que é uma operação atômica no nível do sistema operacional. Isso garante que o arquivo de destino nunca fique em um estado parcialmente escrito, mesmo se ocorrer uma falha durante a escrita. O método também garante que o diretório do arquivo de destino exista antes de tentar escrever o arquivo.
    Args:
        path (str): O caminho do arquivo onde os bytes serão escritos de forma atômica.
        blob (bytes): Os bytes a serem escritos no arquivo.
    """
    s = base64.b64encode(blob).decode("ascii")
    _atomic_write_text(path, s)

# -------------------------
# Paths
# -------------------------

def exe_dir_base() -> str:
    """
    Retorna o diretório base do executável, considerando o ambiente de execução (PyInstaller ou desenvolvimento). O método verifica se o atributo sys._MEIPASS está presente, o que indica que o aplicativo está sendo executado a partir de um pacote criado pelo PyInstaller, e retorna esse diretório como base. Caso contrário, ele retorna o diretório do arquivo atual como base. O resultado é o caminho do diretório onde o aplicativo está sendo executado, que pode ser usado para localizar recursos e arquivos relacionados ao aplicativo.
    Returns:
        str: O diretório base do executável, considerando o ambiente de execução (PyInstaller ou desenvolvimento). O método verifica se o atributo sys._MEIPASS está presente, o que indica que o aplicativo está sendo executado a partir de um pacote criado pelo PyInstaller, e retorna esse diretório como base. Caso contrário, ele retorna o diretório do arquivo atual como base. O resultado é o caminho do diretório onde o aplicativo está sendo executado, que pode ser usado para localizar recursos e arquivos relacionados ao aplicativo.
    """
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def internal_dir() -> str:
    """
    Retorna o caminho do diretório interno do aplicativo, que é uma subpasta chamada "_internal" localizada dentro do diretório base do executável. O método utiliza a função exe_dir_base para obter o diretório base do executável e, em seguida, combina esse diretório com o nome da subpasta "_internal" para formar o caminho completo do diretório interno. Esse diretório é usado para armazenar arquivos relacionados ao aplicativo que não devem ser acessados ou modificados diretamente pelo usuário, como o marcador de licença e outros arquivos de configuração ou estado.
    Returns:
        str: O caminho do diretório interno do aplicativo, que é uma subpasta chamada "_internal" localizada dentro do diretório base do executável. O método utiliza a função exe_dir_base para obter o diretório base do executável e, em seguida, combina esse diretório com o nome da subpasta "_internal" para formar o caminho completo do diretório interno. Esse diretório é usado para armazenar arquivos relacionados ao aplicativo que não devem ser acessados ou modificados diretamente pelo usuário, como o marcador de licença e outros arquivos de configuração ou estado.
    """
    return os.path.join(exe_dir_base(), INTERNAL_DIR_NAME)


def internal_marker_path() -> str:
    """
    Retorna o caminho do arquivo de marcador interno, que é um arquivo chamado "_internal.dat" localizado dentro do diretório interno do aplicativo. O método utiliza a função internal_dir para obter o caminho do diretório interno e, em seguida, combina esse diretório com o nome do arquivo de marcador para formar o caminho completo do arquivo de marcador. Esse arquivo é criado pelo instalador e serve como um indicador de que o aplicativo foi instalado corretamente, além de ser usado para armazenar informações relacionadas à licença e ao estado do aplicativo.
    Returns:
        str: O caminho do arquivo de marcador interno, que é um arquivo chamado "_internal.dat" localizado dentro do diretório interno do aplicativo. O método utiliza a função internal_dir para obter o caminho do diretório interno e, em seguida, combina esse diretório com o nome do arquivo de marcador para formar o caminho completo do arquivo de marcador. Esse arquivo é criado pelo instalador e serve como um indicador de que o aplicativo foi instalado corretamente, além de ser usado para armazenar informações relacionadas à licença e ao estado do aplicativo.
    """
    return os.path.join(internal_dir(), INTERNAL_MARKER_FILE)


def programdata_dir() -> str:
    """
    Retorna o caminho do diretório ProgramData específico para o aplicativo, que é uma subpasta com o nome do aplicativo localizada dentro do diretório ProgramData do sistema. O método obtém o caminho do diretório ProgramData usando a variável de ambiente "PROGRAMDATA" (ou um valor padrão se a variável não estiver definida), e então combina esse caminho com o nome do aplicativo para formar o caminho completo do diretório específico do aplicativo dentro do ProgramData. O método também garante que esse diretório exista, criando-o se necessário, para que possa ser usado para armazenar arquivos relacionados ao estado e à configuração do aplicativo.
    Returns:
        str: O caminho do diretório ProgramData específico para o aplicativo, que é uma subpasta com o nome do aplicativo localizada dentro do diretório ProgramData do sistema. O método obtém o caminho do diretório ProgramData usando a variável de ambiente "PROGRAMDATA" (ou um valor padrão se a variável não estiver definida), e então combina esse caminho com o nome do aplicativo para formar o caminho completo do diretório específico do aplicativo dentro do ProgramData. O método também garante que esse diretório exista, criando-o se necessário, para que possa ser usado para armazenar arquivos relacionados ao estado e à configuração do aplicativo.
    """
    base = os.environ.get("PROGRAMDATA") or r"C:\ProgramData"
    d = os.path.join(base, APP_NAME)
    os.makedirs(d, exist_ok=True)
    return d


def license_path_programdata() -> str:
    """
    Retorna o caminho do arquivo de licença localizado no diretório ProgramData específico para o aplicativo. O método utiliza a função programdata_dir para obter o caminho do diretório específico do aplicativo dentro do ProgramData, e então combina esse diretório com o nome do arquivo de licença (definido pela constante PROGRAMDATA_FILE) para formar o caminho completo do arquivo de licença. Esse arquivo é usado para armazenar informações relacionadas à licença do aplicativo, e o método garante que o caminho retornado seja válido para uso na leitura e escrita de dados relacionados à licença.
    Returns:
        str: O caminho completo do arquivo de licença localizado no diretório ProgramData específico para o aplicativo.
    """
    return os.path.join(programdata_dir(), PROGRAMDATA_FILE)


# -------------------------
# Registro (status)
# -------------------------

def _reg_get(name: str) -> Optional[str]:
    """
    Lê um valor do registro do Windows para uma chave específica, retornando o valor como uma string ou None se a chave não existir ou se ocorrer um erro durante o acesso ao registro. O método tenta abrir a chave de registro definida pela constante REG_PATH e ler o valor associado à chave fornecida. Se a chave ou o valor não existirem, ou se ocorrer um erro durante o acesso ao registro, o método retorna None para indicar que o valor não pôde ser obtido. Caso contrário, ele retorna o valor do registro como uma string, removendo quaisquer espaços em branco extras.
    Args:
        name (str): O nome da chave do registro a ser lida. O método tentará abrir a chave de registro definida pela constante REG_PATH e ler o valor associado a essa chave. Se a chave ou o valor não existirem, ou se ocorrer um erro durante o acesso ao registro, o método retornará None para indicar que o valor não pôde ser obtido.

    Returns:
        Optional[str]: O valor do registro para a chave especificada, ou None se a chave não existir ou se ocorrer um erro ao acessar o registro. O método tenta abrir a chave de registro definida pela constante REG_PATH e ler o valor associado à chave fornecida. Se a chave ou o valor não existirem, ou se ocorrer um erro durante o acesso ao registro, o método retorna None para indicar que o valor não pôde ser obtido.
    """
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
        val, _ = winreg.QueryValueEx(key, name)
        v = str(val).strip()
        return v or None
    except Exception:
        return None


def _reg_set(name: str, value: str) -> None:
    """ 
    Escreve um valor no registro do Windows para uma chave específica, criando a chave de registro se ela não existir. O método tenta criar ou abrir a chave de registro definida pela constante REG_PATH e, em seguida, define o valor associado à chave fornecida usando winreg.SetValueEx. Se a chave de registro não existir, ela será criada automaticamente. O método não retorna nenhum valor, mas garante que o valor seja escrito no registro para a chave especificada.
    Args:
        name (str): O nome da chave do registro a ser escrita. O método tentará criar ou abrir a chave de registro definida pela constante REG_PATH e, em seguida, definir o valor associado a essa chave usando winreg.SetValueEx. Se a chave de registro não existir, ela será criada automaticamente.
        value (str):  O valor a ser escrito no registro para a chave especificada. O método tentará criar ou abrir a chave de registro definida pela constante REG_PATH e, em seguida, definir o valor associado a essa chave usando winreg.SetValueEx. Se a chave de registro não existir, ela será criada automaticamente. O método não retorna nenhum valor, mas garante que o valor seja escrito no registro para a chave especificada.
    """
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
    winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)


def _reg_set_if_missing(name: str, value: str) -> None:
    """ 
    Escreve um valor no registro do Windows para uma chave específica somente se a chave ainda não tiver um valor definido. O método verifica se a chave de registro especificada já possui um valor usando a função _reg_get, e se o valor retornado for None (indicando que a chave não existe ou não tem um valor definido), ele chama a função _reg_set para escrever o valor fornecido no registro. Se a chave já tiver um valor definido, o método não faz nada, garantindo que o valor existente no registro seja preservado.
    Args:
        name (str): O nome da chave do registro a ser escrita. O método verificará se essa chave já possui um valor definido usando a função _reg_get, e se o valor retornado for None (indicando que a chave não existe ou não tem um valor definido), ele chamará a função _reg_set para escrever o valor fornecido no registro. Se a chave já tiver um valor definido, o método não fará nada, garantindo que o valor existente no registro seja preservado.
        value (str): O valor a ser escrito no registro para a chave especificada, caso a chave ainda não tenha um valor definido. O método verificará se a chave de registro especificada já possui um valor usando a função _reg_get, e se o valor retornado for None (indicando que a chave não existe ou não tem um valor definido), ele chamará a função _reg_set para escrever o valor fornecido no registro. Se a chave já tiver um valor definido, o método não fará nada, garantindo que o valor existente no registro seja preservado.
    """
    if _reg_get(name) is None:
        _reg_set(name, value)


# -------------------------
# Machine ID (estável)
# -------------------------

def _machine_guid() -> str:
    """
    Obtém o MachineGuid do registro do Windows, que é um identificador único para a máquina. O método abre a chave de registro localizada em "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Cryptography" e lê o valor associado à chave "MachineGuid". O valor é retornado como uma string, removendo quaisquer espaços em branco extras. O MachineGuid é um identificador estável que pode ser usado para identificar de forma única uma máquina, e é comumente utilizado em cenários onde é necessário associar informações ou licenças a um dispositivo específico.
    Returns:
        str: O MachineGuid lido do registro do Windows. O método abre a chave de registro localizada em "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Cryptography" e lê o valor associado à chave "MachineGuid". O valor é retornado como uma string, removendo quaisquer espaços em branco extras. O MachineGuid é um identificador estável que pode ser usado para identificar de forma única uma máquina, e é comumente utilizado em cenários onde é necessário associar informações ou licenças a um dispositivo específico.
    """
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
    val, _ = winreg.QueryValueEx(key, "MachineGuid")
    return str(val).strip()


def machine_id() -> str:
    """
    Calcula o hash SHA-256 do MachineGuid do registro do Windows e retorna como uma string em letras maiúsculas. O método chama a função _machine_guid para obter o MachineGuid da máquina e, em seguida, calcula o hash SHA-256 desse valor usando a biblioteca hashlib. O resultado é convertido para uma string hexadecimal e transformado em letras maiúsculas antes de ser retornado. Esse hash é usado como um identificador único para a máquina, permitindo que o aplicativo associe informações ou licenças a um dispositivo específico de forma segura.
    Returns:
        str: O hash SHA-256 do MachineGuid do registro do Windows, retornado como uma string em letras maiúsculas. O método chama a função _machine_guid para obter o MachineGuid da máquina e, em seguida, calcula o hash SHA-256 desse valor usando a biblioteca hashlib. O resultado é convertido para uma string hexadecimal e transformado em letras maiúsculas antes de ser retornado. Esse hash é usado como um identificador único para a máquina, permitindo que o aplicativo associe informações ou licenças a um dispositivo específico de forma segura.
    """
    raw = _machine_guid()
    return hashlib.sha256(raw.encode("utf-8")).hexdigest().upper()


def machine_id_hash(mid: str) -> str:
    """
    Calcula o hash SHA-256 de um identificador de máquina (Machine ID) fornecido como argumento e retorna o resultado como uma string em letras maiúsculas. O método recebe um valor de identificador de máquina (mid) como entrada, codifica esse valor em UTF-8 e calcula o hash SHA-256 usando a biblioteca hashlib. O resultado é convertido para uma string hexadecimal e transformado em letras maiúsculas antes de ser retornado. Esse hash é usado para criar um identificador único e seguro para a máquina, permitindo que o aplicativo associe informações ou licenças a um dispositivo específico de forma segura.
    Args:
        mid (str): O valor do identificador da máquina (Machine ID) a ser convertido em hash SHA-256.

    Returns:
        str: O hash SHA-256 do valor passado como argumento `mid`, retornado como uma string em letras maiúsculas.
    """
    return hashlib.sha256(mid.encode("utf-8")).hexdigest().upper()


# -------------------------
# DPAPI (LocalMachine)
# -------------------------

class DATA_BLOB(ctypes.Structure):
    """
    Representa a estrutura DATA_BLOB usada pela API de criptografia do Windows (DPAPI). Essa estrutura é usada para armazenar dados binários que serão protegidos ou desprotegidos usando as funções CryptProtectData e CryptUnprotectData. A estrutura contém dois campos: cbData, que é um valor DWORD que indica o tamanho dos dados em bytes, e pbData, que é um ponteiro para os dados binários a serem protegidos ou desprotegidos. Essa estrutura é essencial para a interação com a API de criptografia do Windows, permitindo que os dados sejam manipulados de forma segura e eficiente.
    Args:
        ctypes (_type_): A classe DATA_BLOB herda de ctypes.Structure, o que permite que ela seja usada para definir uma estrutura de dados compatível com a API de criptografia do Windows. A estrutura é definida usando a sintaxe de classes do Python, e os campos da estrutura são especificados na lista _fields_, onde cada campo é representado por uma tupla contendo o nome do campo e seu tipo de dados correspondente (por exemplo, wt.DWORD para cbData e ctypes.POINTER(ctypes.c_byte) para pbData). Essa definição permite que a estrutura seja usada para armazenar e manipular dados binários de forma segura ao interagir com as funções de criptografia do Windows.
    """
    _fields_ = [("cbData", wt.DWORD), ("pbData", ctypes.POINTER(ctypes.c_byte))]


crypt32 = ctypes.WinDLL("crypt32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

CryptProtectData = crypt32.CryptProtectData
CryptProtectData.argtypes = [
    ctypes.POINTER(DATA_BLOB),
    wt.LPCWSTR,
    ctypes.POINTER(DATA_BLOB),
    ctypes.c_void_p,
    ctypes.c_void_p,
    wt.DWORD,
    ctypes.POINTER(DATA_BLOB),
]
CryptProtectData.restype = wt.BOOL

CryptUnprotectData = crypt32.CryptUnprotectData
CryptUnprotectData.argtypes = [
    ctypes.POINTER(DATA_BLOB),
    ctypes.POINTER(wt.LPWSTR),
    ctypes.POINTER(DATA_BLOB),
    ctypes.c_void_p,
    ctypes.c_void_p,
    wt.DWORD,
    ctypes.POINTER(DATA_BLOB),
]
CryptUnprotectData.restype = wt.BOOL

LocalFree = kernel32.LocalFree
LocalFree.argtypes = [ctypes.c_void_p]
LocalFree.restype = ctypes.c_void_p

CRYPTPROTECT_LOCAL_MACHINE = 0x4


def _bytes_to_blob(data: bytes) -> DATA_BLOB:
    """
    Converte um objeto de bytes em uma estrutura DATA_BLOB compatível com a API de criptografia do Windows (DPAPI). O método recebe um objeto de bytes como entrada, cria um buffer de bytes usando ctypes, e então preenche a estrutura DATA_BLOB com o tamanho dos dados (cbData) e um ponteiro para os dados binários (pbData). O resultado é uma instância da estrutura DATA_BLOB que pode ser usada para proteger ou desproteger os dados usando as funções CryptProtectData e CryptUnprotectData da API de criptografia do Windows. Essa conversão é essencial para garantir que os dados sejam manipulados corretamente ao interagir com a API de criptografia do Windows.
    Args:
        data (bytes): Os dados binários a serem convertidos em uma estrutura DATA_BLOB.

    Returns:
        DATA_BLOB: Uma instância da estrutura DATA_BLOB criada a partir dos dados binários fornecidos.
    """
    buf = (ctypes.c_byte * len(data)).from_buffer_copy(data)
    return DATA_BLOB(len(data), ctypes.cast(buf, ctypes.POINTER(ctypes.c_byte)))


def dpapi_protect_localmachine(plaintext: bytes) -> bytes:
    """
    Protege um objeto de bytes usando a API de criptografia do Windows (DPAPI) com a opção CRYPTPROTECT_LOCAL_MACHINE, que vincula os dados protegidos à máquina em que foram protegidos. O método recebe um objeto de bytes como entrada, converte esses bytes em uma estrutura DATA_BLOB usando a função _bytes_to_blob, e então chama a função CryptProtectData para proteger os dados. O resultado é um novo objeto de bytes que representa os dados protegidos, que pode ser armazenado ou transmitido com segurança. Se ocorrer um erro durante o processo de proteção, o método levanta uma exceção OSError com o código de erro correspondente.
    Args:
        plaintext (bytes): 

    Raises:
        OSError: Se ocorrer um erro durante o processo de proteção dos dados usando a API de criptografia do Windows, o método levanta uma exceção OSError com o código de erro correspondente, que pode ser obtido usando ctypes.get_last_error() para fornecer informações sobre a natureza do erro ocorrido.

    Returns:
        bytes: Um novo objeto de bytes que representa os dados protegidos usando a API de criptografia do Windows (DPAPI) com a opção CRYPTPROTECT_LOCAL_MACHINE. O método converte os bytes de entrada em uma estrutura DATA_BLOB, chama a função CryptProtectData para proteger os dados, e retorna o resultado como um objeto de bytes. Se ocorrer um erro durante o processo de proteção, o método levanta uma exceção OSError com o código de erro correspondente.
    """
    in_blob = _bytes_to_blob(plaintext)
    out_blob = DATA_BLOB()
    if not CryptProtectData(
        ctypes.byref(in_blob),
        "local_marker",
        None,
        None,
        None,
        CRYPTPROTECT_LOCAL_MACHINE,
        ctypes.byref(out_blob),
    ):
        raise OSError(ctypes.get_last_error())
    try:
        return ctypes.string_at(out_blob.pbData, out_blob.cbData)
    finally:
        LocalFree(out_blob.pbData)


def dpapi_unprotect(ciphertext: bytes) -> bytes:
    """
    Desprotege um objeto de bytes protegido usando a API de criptografia do Windows (DPAPI). O método recebe um objeto de bytes protegido como entrada, converte esses bytes em uma estrutura DATA_BLOB usando a função _bytes_to_blob, e então chama a função CryptUnprotectData para desproteger os dados. O resultado é um novo objeto de bytes que representa os dados desprotegidos, que pode ser usado ou processado conforme necessário. Se ocorrer um erro durante o processo de desproteção, o método levanta uma exceção OSError com o código de erro correspondente.
    Args:
        ciphertext (bytes): Um objeto de bytes protegido usando a API de criptografia do Windows (DPAPI).

    Raises:
        OSError: Se ocorrer um erro durante o processo de desproteção dos dados usando a API de criptografia do Windows, o método levanta uma exceção OSError com o código de erro correspondente, que pode ser obtido usando ctypes.get_last_error() para fornecer informações sobre a natureza do erro ocorrido.

    Returns:
        bytes: Um novo objeto de bytes que representa os dados desprotegidos usando a API de criptografia do Windows (DPAPI). O método recebe um objeto de bytes protegido como entrada, converte esses bytes em uma estrutura DATA_BLOB usando a função _bytes_to_blob, chama a função CryptUnprotectData para desproteger os dados, e retorna o resultado como um objeto de bytes. Se ocorrer um erro durante o processo de desproteção, o método levanta uma exceção OSError com o código de erro correspondente.
    """
    in_blob = _bytes_to_blob(ciphertext)
    out_blob = DATA_BLOB()
    p_desc = wt.LPWSTR()

    if not CryptUnprotectData(
        ctypes.byref(in_blob),
        ctypes.byref(p_desc),
        None,
        None,
        None,
        0,
        ctypes.byref(out_blob),
    ):
        raise OSError(ctypes.get_last_error())

    try:
        return ctypes.string_at(out_blob.pbData, out_blob.cbData)
    finally:
        if p_desc:
            LocalFree(p_desc)
        LocalFree(out_blob.pbData)


# -------------------------
# Arquivo (ProgramData)
# -------------------------

def _file_read_bytes(path: str) -> Optional[bytes]:
    """
    Lê um arquivo de texto contendo dados codificados em base64, decodifica esses dados e retorna o resultado como um objeto de bytes. O método verifica se o arquivo especificado existe, e se existir, ele lê o conteúdo do arquivo como uma string, remove quaisquer espaços em branco extras, e então decodifica a string usando base64 para obter os dados binários originais. Se o arquivo não existir ou se ocorrer um erro durante a leitura ou decodificação, o método retorna None para indicar que os dados não puderam ser obtidos.
    Args:
        path (str): O caminho do arquivo de texto que contém os dados codificados em base64 a serem lidos e decodificados. O método verifica se o arquivo especificado existe, e se existir, ele lê o conteúdo do arquivo como uma string, remove quaisquer espaços em branco extras, e então decodifica a string usando base64 para obter os dados binários originais. Se o arquivo não existir ou se ocorrer um erro durante a leitura ou decodificação, o método retorna None para indicar que os dados não puderam ser obtidos.

    Returns:
        Optional[bytes]: Um objeto de bytes que representa os dados decodificados do arquivo de texto codificado em base64. O método verifica se o arquivo especificado existe, e se existir, ele lê o conteúdo do arquivo como uma string, remove quaisquer espaços em branco extras, e então decodifica a string usando base64 para obter os dados binários originais. Se o arquivo não existir ou se ocorrer um erro durante a leitura ou decodificação, o método retorna None para indicar que os dados não puderam ser obtidos.
    """
    try:
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            s = f.read().strip()
        if not s:
            return None
        return base64.b64decode(s.encode("ascii"))
    except Exception:
        return None


def _file_write_bytes(path: str, blob: bytes) -> None:
    """
    Escreve um objeto de bytes em um arquivo de texto, codificando os bytes em base64 antes de escrevê-los. O método recebe um objeto de bytes como entrada, codifica esses bytes usando base64 para obter uma string legível, e então escreve essa string em um arquivo de texto no caminho especificado. O método garante que o diretório do arquivo de destino exista antes de tentar escrever o arquivo. Se ocorrer um erro durante a escrita do arquivo, o método levanta uma exceção correspondente.
    Args:
        path (str): O caminho do arquivo de texto onde os bytes codificados em base64 serão escritos. O método garante que o diretório do arquivo de destino exista antes de tentar escrever o arquivo. Se ocorrer um erro durante a escrita do arquivo, o método levanta uma exceção correspondente.
        blob (bytes): O objeto de bytes a ser codificado em base64 e escrito no arquivo de texto. O método recebe esse objeto de bytes como entrada, codifica os bytes usando base64 para obter uma string legível, e então escreve essa string em um arquivo de texto no caminho especificado. Se ocorrer um erro durante a escrita do arquivo, o método levanta uma exceção correspondente.
    """
    s = base64.b64encode(blob).decode("ascii")
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)


# -------------------------
# Payload (dentro do DPAPI)
# -------------------------

def _make_payload(mid: str, token: bytes) -> bytes:
    """
    Cria um payload formatado contendo o hash da máquina, o token e o MAC calculado usando HMAC-SHA256. O método recebe um identificador de máquina (mid) e um token como entrada, calcula o hash do identificador de máquina usando a função machine_id_hash, e então calcula um código de autenticação de mensagem (MAC) usando HMAC com a chave secreta do aplicativo (APP_SECRET) e os dados combinados do hash da máquina e do token. O resultado é um objeto de bytes que contém o hash da máquina, o token e o MAC, separados por caracteres de pipe ("|"), que pode ser protegido usando a API de criptografia do Windows (DPAPI) para garantir a segurança dos dados.
    Args:
        mid (str): O ID da máquina.
        token (bytes): O token gerado para a máquina.

    Returns:
        bytes: Um objeto de bytes contendo o payload formatado com o hash da máquina, o token e o MAC calculado.
    """


    midh = machine_id_hash(mid).encode("ascii")
    mac = hmac.new(APP_SECRET, midh + token, hashlib.sha256).digest()
    return midh + b"|" + token + b"|" + mac


def _parse_payload(payload: bytes) -> Tuple[str, bytes, bytes]:
    parts = payload.split(b"|")
    if len(parts) != 3:
        raise ValueError("payload inválido")
    return parts[0].decode("ascii"), parts[1], parts[2]


# -------------------------
# Core
# -------------------------

def ensure_or_mark(allow_create: bool = False) -> Tuple[bool, str]:
    """
        Política final (conforme combinado):
        - O instalador cria: <pasta app>\\_internal\\_internal.dat (marker somente leitura)
        - O app NUNCA escreve em _internal
        - O marcador por máquina fica em ProgramData e é DPAPI(LocalMachine):
            C:\\ProgramData\\LeadsApp\\cahce_string.dat

        Regras:
        1) Se marker do instalador não existir => bloqueia (evita rodar app copiado solto).
        2) Se o arquivo de ProgramData NÃO existir:
        - allow_create=False => bloqueia pedindo ativação online primeiro.
        - allow_create=True  => cria o marcador por máquina (use somente após validação online OK).
        3) Se o arquivo existir => valida DPAPI + HMAC + machine_id_hash.

        Args:
          allow_create (bool): Indica se o método deve criar um novo marcador por máquina no diretório ProgramData caso o arquivo de marcador não exista. Se allow_create for False, o método bloqueia a execução e solicitará ativação online. Se allow_create for True, o método tentará criar um novo marcador por máquina usando DPAPI para proteger os dados, e se a criação for bem-sucedida, permitirá a execução do aplicativo. Essa opção é útil para permitir que o aplicativo seja ativado online pela primeira vez, criando o marcador por máquina necessário para futuras validações.
    """
    # 1) Exigir marker do instalador
    if not os.path.exists(internal_marker_path()):
        return False, "Instalação inválida (marker do instalador ausente em _internal)."

    mid = machine_id()
    midh = machine_id_hash(mid)

    # 2) Ler marcador por máquina
    blob = _file_read_bytes(license_path_programdata())
    if blob is None:
        if not allow_create:
            _reg_set(REG_STATE, "NEEDS_ONLINE_ACTIVATION")
            _reg_set(REG_MIDHASH, midh)
            _reg_set_if_missing(REG_FIRSTSEEN, str(int(time.time())))
            return False, "Primeira execução requer ativação online."

        # allow_create=True => criar marcador por máquina (após validação online)
        try:
            token = os.urandom(32)
            payload = _make_payload(mid, token)
            protected = dpapi_protect_localmachine(payload)
            _file_write_bytes(license_path_programdata(), protected)
        except Exception:
            return False, "Sem permissão para criar arquivo de controle em ProgramData."

        _reg_set(REG_STATE, "OK")
        _reg_set(REG_MIDHASH, midh)
        _reg_set_if_missing(REG_FIRSTSEEN, str(int(time.time())))
        return True, "OK"

        # 3) Validar marcador existente
    lp = license_path_programdata()  # caminho do arquivo em ProgramData

    try:
        payload = dpapi_unprotect(blob)  # falha em outro PC
    except Exception:
        _reg_set(REG_STATE, "MOVED_OR_COPIED")
        _reg_set(REG_MIDHASH, midh)
        _reg_set_if_missing(REG_FIRSTSEEN, str(int(time.time())))
        return False, f"Arquivo de controle não pode ser aberto neste computador (cópia detectada).\n\nArquivo:\n{lp}"

    try:
        stored_midh, token, mac = _parse_payload(payload)
    except Exception:
        # backup do arquivo problemático
        bak = _backup_file(lp, "corrupted")
        _reg_set(REG_STATE, "CORRUPTED")
        _reg_set(REG_MIDHASH, midh)
        _reg_set_if_missing(REG_FIRSTSEEN, str(int(time.time())))

        # opcional: recriar automaticamente se allow_create=True (ou seja, após validação online)
        if allow_create:
            try:
                token_new = os.urandom(32)
                payload_new = _make_payload(mid, token_new)
                protected_new = dpapi_protect_localmachine(payload_new)
                _file_write_bytes(lp, protected_new)
                _reg_set(REG_STATE, "OK")
                return True, "OK"
            except Exception:
                pass

        extra = f"\nBackup:\n{bak}" if bak else ""
        return False, f"Arquivo de controle corrompido.\n\nArquivo:\n{lp}{extra}"

    expected_mac = hmac.new(APP_SECRET, stored_midh.encode("ascii") + token, hashlib.sha256).digest()
    if not hmac.compare_digest(mac, expected_mac):
        bak = _backup_file(lp, "tampered")
        _reg_set(REG_STATE, "TAMPERED")
        extra = f"\nBackup:\n{bak}" if bak else ""
        return False, f"Arquivo de controle adulterado.\n\nArquivo:\n{lp}{extra}"

    if stored_midh != midh:
        bak = _backup_file(lp, "wrongpc")
        _reg_set(REG_STATE, "WRONG_PC")
        extra = f"\nBackup:\n{bak}" if bak else ""
        return False, f"Arquivo de controle pertence a outro computador.\n\nArquivo:\n{lp}{extra}"


    _reg_set(REG_STATE, "OK")
    _reg_set(REG_MIDHASH, midh)
    _reg_set_if_missing(REG_FIRSTSEEN, str(int(time.time())))
    return True, "OK"