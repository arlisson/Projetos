# config.py
from __future__ import annotations

import json
import os
from typing import Optional, Dict, Any, List

CONFIG_FIELDS_PATH = "controle_campos.json"
CONFIG_SHEET_PATH = "controle_planilha.json"
CONFIG_UI_PATH = "controle_ui.json"
CONFIG_EMAIL_DOMAINS_PATH = "controle_email_dominios.json"


def default_fields_config() -> dict:
    """Configurações padrão para campos e abas.

    Returns:
        dict: Configurações iniciais com uma aba "Preenche Fácil" contendo campos básicos.
    """
    # Agora com "abas"
    base_campos = [
        {"id": "nome", "titulo": "Nome", "tipo": "texto", "fixo": True, "locked": False},
        {"id": "telefone", "titulo": "Telefone", "tipo": "telefone", "fixo": True, "locked": False},
        {"id": "email", "titulo": "Email", "tipo": "email", "fixo": True, "locked": False},
    ]
    default_sheet = "Preenche Fácil"
    return {
        "arquivo_padrao": "PreencheFacil.xlsx",
        "aba": default_sheet,
        "abas": {
            default_sheet: {"campos": base_campos}
        },
    }

def _normalize_campos(campos: list, field_types: List[str]) -> list:
    """Normaliza a lista de campos, garantindo que cada campo seja um dicionário com chaves mínimas e tipos válidos.

    Args:
        campos (list): Lista de campos a normalizar. Cada campo deve ser um dicionário, mas o formato é flexível.
        field_types (List[str]): Lista de tipos de campo válidos. Se o campo tiver um tipo não listado, será definido como "texto".

    Returns:
        list: Lista de campos normalizada, onde cada campo é um dicionário com chaves "id", "titulo", "tipo" e "fixo".
    """
    out = []
    for c in campos or []:
        if not isinstance(c, dict):
            continue
        c = dict(c)
        c.setdefault("tipo", "texto")
        c.setdefault("fixo", False)
        c.setdefault("locked", False) 

        if "locked" not in c:
            c["locked"] = bool(c.get("fixo", False))

        if c.get("tipo") not in field_types:
            c["tipo"] = "texto"
        # garante chaves mínimas
        c.setdefault("id", "")
        c.setdefault("titulo", "")
        out.append(c)
    return out

def rename_sheet_key(cfg: dict, old_name: str, new_name: str) -> None:
    """Renomeia uma aba (sheet) dentro da configuração, movendo os campos associados para a nova chave.

    Args:
        cfg (dict): Configuração completa onde as abas estão definidas. Deve conter a chave "abas" que é um dicionário de abas.
        old_name (str): Nome atual da aba que se deseja renomear. Se não existir, a função apenas garante que a nova aba exista sem campos.
        new_name (str): Novo nome para a aba. Se já existir, os campos só serão movidos se a aba de destino estiver vazia. Se for igual ao old_name, não faz nada.
    """
    if old_name == new_name:
        return
    abas = cfg.get("abas") or {}
    if old_name not in abas:
        # nada para mover
        cfg.setdefault("abas", {})
        cfg["abas"].setdefault(new_name, {"campos": []})
        return
    cfg.setdefault("abas", {})
    # se já existir destino, você pode escolher mesclar; aqui eu preservo destino e só movo se vazio
    if new_name not in cfg["abas"]:
        cfg["abas"][new_name] = abas[old_name]
    else:
        if not (cfg["abas"][new_name].get("campos") or []):
            cfg["abas"][new_name] = abas[old_name]
    try:
        del cfg["abas"][old_name]
    except Exception:
        pass

def get_sheet_campos(cfg: dict, sheet_name: str) -> list:
    """Obtém os campos configurados para uma aba específica dentro da configuração.

    Args:
        cfg (dict): Configuração completa onde as abas estão definidas. Deve conter a chave "abas" que é um dicionário de abas, cada uma com uma lista de campos.
        sheet_name (str): Nome da aba para a qual se deseja obter os campos. Se a aba não existir, retorna uma lista vazia.

    Returns:
        list: Lista de campos configurados para a aba especificada. Cada campo é um dicionário com chaves como "id", "titulo", "tipo" e "fixo". Se a aba ou os campos não estiverem definidos, retorna uma lista vazia.
    """
    abas = cfg.get("abas") or {}
    sheet = abas.get(sheet_name) or {}
    return sheet.get("campos") or []


def set_sheet_campos(cfg: dict, sheet_name: str, campos: list) -> None:
    """ Define os campos para uma aba específica dentro da configuração, normalizando a lista de campos e garantindo a estrutura correta.

    Args:
        cfg (dict): Configuração completa onde as abas estão definidas. Deve conter a chave "abas" que é um dicionário de abas, cada uma com uma lista de campos.
        sheet_name (str):   Nome da aba para a qual se deseja definir os campos. Se a aba não existir, será criada automaticamente.
        campos (list): Lista de campos a ser definida para a aba especificada. Cada campo deve ser um dicionário, mas o formato é flexível. A função irá normalizar os campos, garantindo que cada um tenha as chaves mínimas e tipos válidos, conforme definido na função _normalize_campos.
    """
    cfg.setdefault("abas", {})
    cfg["abas"].setdefault(sheet_name, {})
    cfg["abas"][sheet_name]["campos"] = campos


def load_fields_config(field_types: List[str]) -> dict:
    """ Carrega a configuração de campos e abas a partir do arquivo JSON, aplicando normalização e migração de formato se necessário.

    Args:
        field_types (List[str]): Lista de tipos de campo válidos para normalização. Usada para garantir que os campos carregados tenham tipos reconhecidos, definindo como "texto" se o tipo for inválido ou ausente.

    Returns:
        dict: Configuração de campos carregada e normalizada.
    """
    if not os.path.exists(CONFIG_FIELDS_PATH):
        cfg = default_fields_config()
        save_fields_config(cfg)
        return cfg

    with open(CONFIG_FIELDS_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f) or {}

    # defaults
    d = default_fields_config()
    cfg.setdefault("arquivo_padrao", d["arquivo_padrao"])
    cfg.setdefault("aba", d["aba"])

    # migração do formato antigo:
    # - se existir cfg["campos"] no topo e não existir cfg["abas"], move para a aba atual
    if "abas" not in cfg or not isinstance(cfg.get("abas"), dict):
        cfg["abas"] = {}
    if "campos" in cfg and isinstance(cfg.get("campos"), list):
        campos_legacy = cfg.get("campos") or []
        sheet = cfg.get("aba") or d["aba"]
        if sheet not in cfg["abas"]:
            cfg["abas"][sheet] = {}
        if not cfg["abas"][sheet].get("campos"):
            cfg["abas"][sheet]["campos"] = campos_legacy
        # opcional: remover o legado para não confundir
        try:
            del cfg["campos"]
        except Exception:
            pass

    # garante que exista a aba atual dentro de "abas"
    sheet = cfg.get("aba") or d["aba"]
    if sheet not in cfg["abas"]:
        cfg["abas"][sheet] = {"campos": d["abas"][d["aba"]]["campos"]}

    # normaliza campos de todas as abas
    for sheet_name, payload in (cfg.get("abas") or {}).items():
        if not isinstance(payload, dict):
            cfg["abas"][sheet_name] = {"campos": []}
            continue
        payload.setdefault("campos", [])
        payload["campos"] = _normalize_campos(payload.get("campos"), field_types)

    return cfg


def save_fields_config(cfg: dict) -> None:
    """ Salva a configuração de campos e abas em um arquivo JSON, mantendo a estrutura esperada. 

    Args:
        cfg (dict): Configuração de campos a ser salva. Deve conter a estrutura esperada, incluindo "abas" como um dicionário de abas, cada uma com uma lista de campos. A função não realiza validação ou normalização, portanto, é responsabilidade do chamador garantir que a configuração esteja no formato correto antes de chamar esta função. 
    """
    with open(CONFIG_FIELDS_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def load_sheet_config() -> dict:
    """ Carrega a configuração de planilha a partir do arquivo JSON. Se o arquivo não existir ou ocorrer um erro durante a leitura, retorna um dicionário vazio. A função não realiza validação ou normalização da configuração, portanto, é responsabilidade do chamador garantir que a configuração esteja no formato correto após o carregamento. 

    Returns:
        dict: Configuração de planilha carregada a partir do arquivo JSON. Se o arquivo não existir ou ocorrer um erro durante a leitura, retorna um dicionário vazio. A função não realiza validação ou normalização da configuração, portanto, é responsabilidade do chamador garantir que a configuração esteja no formato correto após o carregamento. 
    """
    if not os.path.exists(CONFIG_SHEET_PATH):
        return {}
    try:
        with open(CONFIG_SHEET_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_sheet_config(path: str) -> None:
    """ Salva o caminho da planilha na configuração, escrevendo em um arquivo JSON. A função irá criar ou sobrescrever o arquivo de configuração com um dicionário contendo a chave "last_sheet_path" e o valor do caminho fornecido. A função não realiza validação do caminho fornecido, portanto, é responsabilidade do chamador garantir que o caminho seja válido e acessível antes de chamar esta função.

    Args:
        path (str): Caminho da planilha a ser salvo na configuração. A função irá salvar este caminho no arquivo de configuração JSON, substituindo o valor existente. A função não realiza validação do caminho fornecido, portanto, é responsabilidade do chamador garantir que o caminho seja válido e acessível antes de chamar esta função.
    """
    with open(CONFIG_SHEET_PATH, "w", encoding="utf-8") as f:
        json.dump({"last_sheet_path": path}, f, ensure_ascii=False, indent=2)


def get_last_sheet_path() -> Optional[str]:
    """ Obtém o caminho da última planilha salvo na configuração. A função lê o arquivo de configuração JSON para obter o valor associado à chave "last_sheet_path". Se o arquivo de configuração não existir, se a chave "last_sheet_path" não estiver presente ou se o caminho armazenado não corresponder a um arquivo existente no sistema de arquivos, a função retorna None. Caso contrário, retorna o caminho da última planilha como uma string.

    Returns:
        Optional[str]: Caminho da última planilha salvo na configuração. Se o caminho não estiver presente na configuração ou se o arquivo de configuração não existir, retorna None. Se o caminho estiver presente mas o arquivo correspondente não existir no sistema de arquivos, também retorna None. Caso contrário, retorna o caminho da última planilha como uma string.
    """
    cfg = load_sheet_config()
    p = cfg.get("last_sheet_path")
    if not p:
        return None
    return p if os.path.exists(p) else None


def default_ui_config() -> dict:
    """    Configurações padrão para a interface do usuário, incluindo ícones, tema de cores e HTML para o rodapé. Esta configuração é usada como base para a personalização da aparência da aplicação. A função retorna um dicionário contendo as seguintes chaves:

    Returns:
        dict: Configurações padrão para a interface do usuário, incluindo ícones, tema de cores e HTML para o rodapé. Esta configuração é usada como base para a personalização da aparência da aplicação. A função retorna um dicionário contendo as seguintes chaves:
- "window_icon": Caminho para o ícone da janela principal. 
- "button_icons": Dicionário de caminhos para ícones de botões específicos, como "choose_file", "add_field", "save_lead", "clear", "edit_title", "delete_field" e "settings".
- "theme": Dicionário de cores para a interface, incluindo "background", "surface
", "surface_alt", "text", "muted_text", "primary", "danger" e "border".
- "background_hsl": Dicionário com valores de matiz (h), saturação (s) e luminosidade (l) para a cor de fundo, usado para ajustes dinâmicos de tema.
- "footer_left_html": String contendo HTML para o conteúdo do rodapé à esquerda, permitindo personalização de mensagens ou links.

    """
    # Mantém compatível com seu padrão anterior (icons + theme + background_hsl)
    return {
        "window_icon": "assets/A.ico",
        "button_icons": {
            "choose_file": "assets/icons/pasta.png",
            "add_field": "assets/icons/adicionar.png",
            "save_lead": "assets/icons/salvar.png",
            "clear": "assets/icons/limpar.png",
            "edit_title": "assets/icons/editar.png",
            "delete_field": "assets/icons/lixeira.png",
            "settings": "assets/icons/engrenagem.png",
            "lock_open": "assets/icons/cadeado-aberto.png",
            "lock_closed": "assets/icons/cadeado.png",
            "help": "assets/icons/ajuda.png"
        },
        "theme": {
            "background": "#0B1220",
            "surface": "#0F1A2B",
            "surface_alt": "#111F33",
            "text": "#E6EDF7",
            "muted_text": "#A7B3C6",
            "primary": "#3B82F6",
            "danger": "#EF4444",
            "border": "#1F2A44",
        },
        "background_hsl": {"h": 210, "s": 49, "l": 8},
        "footer_left_html": "<b>Se precisar de telefonia para sua empresa</b> → WhatsApp (22) 98812-4656",
        "footer_link": "https://hub-avance.vercel.app",
        "footer_logo_path": "assets/icons/A.png",
        "footer_logo_height": 28,
        "help_url": "https://arlisson.github.io/Leads-App/"
    }


def load_ui_config() -> dict:
    """Carrega as configurações da interface do usuário a partir de um arquivo JSON. Se o arquivo não existir ou ocorrer um erro durante a leitura, retorna as configurações padrão definidas pela função default_ui_config(). A função garante que as chaves principais estejam presentes na configuração carregada, preenchendo com valores padrão para quaisquer chaves ausentes. A configuração inclui temas de cores, ícones e HTML para o rodapé, permitindo personalização da aparência da aplicação.
    Returns:
        dict: Configurações da interface do usuário carregadas a partir do arquivo JSON. Se o arquivo não existir ou ocorrer um erro durante a leitura, retorna as configurações padrão definidas pela função default_ui_config(). A função garante que as chaves principais estejam presentes na configuração carregada, preenchendo com valores padrão para quaisquer chaves ausentes. A configuração inclui temas de cores, ícones e HTML para o rodapé, permitindo personalização da aparência da aplicação.
    """
    if not os.path.exists(CONFIG_UI_PATH):
        cfg = default_ui_config()
        save_ui_config(cfg)
        return cfg

    try:
        with open(CONFIG_UI_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f) or {}
    except Exception:
        cfg = default_ui_config()
        save_ui_config(cfg)
        return cfg

    # defaults (não sobrescreve o que o usuário já configurou)
    d = default_ui_config()
    cfg.setdefault("window_icon", d["window_icon"])
    cfg.setdefault("button_icons", d["button_icons"])
    cfg.setdefault("theme", d["theme"])
    cfg.setdefault("background_hsl", d["background_hsl"])
    cfg.setdefault("footer_left_html", d["footer_left_html"])

    # garante subchaves mínimas do tema
    for k, v in d["theme"].items():
        cfg["theme"].setdefault(k, v)

    return cfg


def save_ui_config(cfg: dict) -> None:
    """ Salva as configurações da interface do usuário em um arquivo JSON. A função recebe um dicionário de configurações e escreve seu conteúdo em um arquivo de configuração JSON, criando ou sobrescrevendo o arquivo existente. A configuração deve conter chaves principais como "window_icon", "button_icons", "theme", "background_hsl" e "footer_left_html". A função não realiza validação ou normalização da configuração, portanto, é responsabilidade do chamador garantir que a configuração esteja no formato correto antes de chamar esta função. O arquivo JSON resultante terá uma estrutura legível, com indentação para facilitar a edição manual se necessário.

    Args:
        cfg (dict): Configurações da interface do usuário a ser salva. Deve conter as chaves principais como "window_icon", "button_icons", "theme", "background_hsl" e "footer_left_html". A função não realiza validação ou normalização da configuração, portanto, é responsabilidade do chamador garantir que a configuração esteja no formato correto antes de chamar esta função. A função irá criar ou sobrescrever o arquivo de configuração JSON com o conteúdo fornecido. 
    """
    with open(CONFIG_UI_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def default_email_domains_config() -> dict:
    """ Configurações padrão para domínios de email, contendo uma lista de domínios comuns usados para preenchimento automático em campos de email. Esta configuração é usada como base para a personalização dos domínios de email disponíveis na aplicação. A função retorna um dicionário com a chave "dominios", que é uma lista de strings representando os domínios de email padrão, como "@gmail.com", "@hotmail.com", "@yahoo.com" e "@outlook.com".

    Returns:
        dict: Configurações padrão para domínios de email, contendo uma lista de domínios comuns usados para preenchimento automático em campos de email. Esta configuração é usada como base para a personalização dos domínios de email disponíveis na aplicação. A função retorna um dicionário com a chave "dominios", que é uma lista de strings representando os domínios de email padrão, como "@gmail.com", "@hotmail.com", "@yahoo.com" e "@outlook.com".
    """
    return {
        "dominios": [
            "@gmail.com",
            "@hotmail.com",
            "@yahoo.com",
            "@outlook.com",
        ]
    }


def load_email_domains_config() -> dict:
    """ Carrega as configurações de domínios de email a partir de um arquivo JSON. Se o arquivo não existir ou ocorrer um erro durante a leitura, retorna as configurações padrão definidas pela função default_email_domains_config(). A função garante que a chave "dominios" esteja presente na configuração carregada, preenchendo com valores padrão para quaisquer chaves ausentes. A configuração inclui uma lista de domínios de email usados para preenchimento automático em campos de email, permitindo personalização dos domínios disponíveis na aplicação.

    Returns:
        dict: Configurações de domínios de email carregadas do arquivo JSON ou as configurações padrão caso o arquivo não exista ou ocorra um erro durante a leitura.
    """
    if not os.path.exists(CONFIG_EMAIL_DOMAINS_PATH):
        cfg = default_email_domains_config()
        save_email_domains_config(cfg)
        return cfg

    try:
        with open(CONFIG_EMAIL_DOMAINS_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f) or {}
    except Exception:
        cfg = default_email_domains_config()
        save_email_domains_config(cfg)
        return cfg

    cfg.setdefault("dominios", default_email_domains_config()["dominios"])
    # normaliza: garante '@' e remove vazios/duplicados
    out: List[str] = []
    for d in cfg.get("dominios", []) or []:
        s = str(d or "").strip()
        if not s:
            continue
        if not s.startswith("@"):
            s = "@" + s
        if s not in out:
            out.append(s)
    cfg["dominios"] = out

    return cfg


def save_email_domains_config(cfg: dict) -> None:
    """ Salva as configurações de domínios de email em um arquivo JSON. A função recebe um dicionário de configurações contendo a chave "dominios", que é uma lista de strings representando os domínios de email. O conteúdo do dicionário é escrito em um arquivo de configuração JSON, criando ou sobrescrevendo o arquivo existente. A função não realiza validação ou normalização da configuração, portanto, é responsabilidade do chamador garantir que a configuração esteja no formato correto antes de chamar esta função. O arquivo JSON resultante terá uma estrutura legível, com indentação para facilitar a edição manual se necessário.

    Args:
        cfg (dict): Configurações de domínios de email a ser salva. Deve conter a chave "dominios", que é uma lista de strings representando os domínios de email. A função não realiza validação ou normalização da configuração, portanto, é responsabilidade do chamador garantir que a configuração esteja no formato correto antes de chamar esta função. A função irá criar ou sobrescrever o arquivo de configuração JSON com o conteúdo fornecido, mantendo uma estrutura legível com indentação.
    """
    with open(CONFIG_EMAIL_DOMAINS_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)