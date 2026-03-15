# formatters.py
from __future__ import annotations

import re
from datetime import datetime, date
from typing import Optional, Any


def normalize_masked_text(value: str) -> str:
    """ Normaliza um texto que pode conter caracteres de máscara (como em campos de formulário) e retorna uma versão limpa e formatada do texto. O método remove caracteres de máscara comuns, como sublinhados, espaços, hífens, pontos, barras e parênteses, e verifica se o texto resultante contém apenas caracteres de separação. Se o texto contiver apenas caracteres de separação sem letras ou dígitos, ele retorna uma string vazia. Além disso, se o texto contiver uma barra sem dígitos, ou se tiver dígitos mas menos de 8 quando houver uma barra, ele também retorna uma string vazia. Caso contrário, retorna o texto limpo e formatado.
    Args:
        value (str): O texto a ser normalizado.
    Returns:
        str: O texto normalizado, sem caracteres de máscara e formatado de acordo com as regras descritas.
    """   
    v = (value or "").strip()

    only_separators = re.sub(r"[0-9A-Za-zÀ-ÿ]", "", v)
    if v and only_separators and all(ch in " _-./()[]" for ch in only_separators):
        if not re.search(r"[0-9A-Za-zÀ-ÿ]", v):
            return ""

    if "/" in v and not re.search(r"\d", v):
        return ""

    digits = re.sub(r"\D", "", v)
    if "/" in v and digits and len(digits) < 8:
        return ""

    return v


def digits_only(value: str) -> str:
    """
    Remove todos os caracteres não numéricos de uma string, retornando apenas os dígitos. O método utiliza uma expressão regular para substituir qualquer caractere que não seja um dígito por uma string vazia, resultando em uma string composta apenas por números. Se a entrada for None ou vazia, o método retorna uma string vazia.
    Args:
        value (str): A string de entrada a ser processada.

    Returns:
        str: A string contendo apenas os dígitos da entrada original.
    """
    return re.sub(r"\D+", "", value or "")


def strip_mask_chars(value: str) -> str:
    """ 
    Remove caracteres de máscara comuns de uma string, como sublinhados, espaços, hífens, pontos, barras e parênteses, e retorna a string limpa. O método utiliza uma expressão regular para substituir esses caracteres por uma string vazia, resultando em uma versão da string sem os caracteres de máscara. Se a entrada for None ou vazia, o método retorna uma string vazia.
    Args:
        value (str): A string de entrada a ser processada, que pode conter caracteres de máscara.

    Returns:
        str: A string limpa, sem caracteres de máscara.
    """
    return (value or "").replace("_", "").strip()


def parse_decimal_br(s: str) -> Optional[float]:
    """ Converte uma string que representa um número no formato brasileiro (com vírgula como separador decimal) para um valor float. O método remove quaisquer caracteres que não sejam dígitos, vírgulas, pontos ou sinais de menos, e então processa a string para garantir que o formato seja interpretado corretamente. Se a string contiver tanto vírgula quanto ponto, o método assume que o ponto é um separador de milhar e a vírgula é o separador decimal. Se a string contiver apenas vírgula, ela é tratada como separador decimal. O método tenta converter a string resultante para float e retorna o valor convertido, ou None se a conversão falhar. 

    Args:
        s (str): A string contendo um valor numérico no formato brasileiro (com vírgula como separador decimal).

    Returns:
        Optional[float]: O valor numérico convertido para float, ou None se a conversão falhar.
    """
    if s is None:
        return None
    s = str(s).strip()
    if not s:
        return None
    s = re.sub(r"[^\d,\.\-]+", "", s)
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    else:
        if "," in s:
            s = s.replace(".", "")
            s = s.replace(",", ".")
    try:
        return float(s)
    except Exception:
        return None


def parse_date_any(s: str) -> Optional[date]:
    """ Converte uma string que representa uma data em um objeto date do Python, tentando vários formatos comuns de data. O método aceita strings em formatos como dd/mm/yyyy, dd-mm-yyyy, yyyy-mm-dd e yyyy/mm/dd. Ele tenta converter a string para um objeto date usando cada um desses formatos, e retorna o primeiro resultado bem-sucedido. Se a conversão falhar para todos os formatos, o método retorna None. Se a entrada for None ou vazia, ele também retorna None.

    Args:
        s (str): A string contendo uma data no formato dd/mm/yyyy, dd-mm-yyyy, yyyy-mm-dd ou yyyy/mm/dd.

    Returns:
        Optional[date]: A data convertida, ou None se a conversão falhar.
    """
    if s is None:
        return None
    s = str(s).strip()
    if not s:
        return None
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            pass
    return None


def normalize_bool_ptbr(s: str) -> Optional[str]:
    """ Normaliza uma string que representa um valor booleano em português, retornando "Sim" para valores que indicam verdadeiro e "Não" para valores que indicam falso. O método aceita várias formas de entrada, como "sim", "s", "yes", "y", "true", "1" para verdadeiro, e "não", "nao", "n", "no", "false", "0" para falso. A comparação é feita de forma case-insensitive e a string de entrada é limpa de espaços antes da comparação. Se a string não corresponder a nenhum dos valores reconhecidos para verdadeiro ou falso, o método retorna a string original limpa.
    Args:
        s (str): A string de entrada que representa um valor booleano em português.
    Returns:
        Optional[str]: "Sim" se a string indicar verdadeiro, "Não" se indicar falso, ou a string original limpa se não corresponder a nenhum dos casos anteriores. Retorna None se a entrada for None ou vazia.
    """
    if s is None:
        return None
    s0 = str(s).strip().lower()
    if not s0:
        return None
    if s0 in {"sim", "s", "yes", "y", "true", "1"}:
        return "Sim"
    if s0 in {"não", "nao", "n", "no", "false", "0"}:
        return "Não"
    return str(s).strip()


def cast_value_by_type(tipo: str, raw: str) -> Any:
    """ Converte uma string bruta para um valor do tipo especificado, com suporte para tipos como "numero", "moeda", "data" e "booleano". O método processa a string de entrada com base no tipo solicitado, utilizando funções de formatação específicas para cada tipo. Para "numero" e "moeda", ele tenta converter a string para um float usando o formato brasileiro. Para "data", ele tenta converter a string para um objeto date. Para "booleano", ele normaliza a string para "Sim" ou "Não". Se a conversão falhar ou se o tipo não for reconhecido, o método retorna a string original limpa.
    Args:
        tipo (str): O tipo para o qual a string deve ser convertida, como "numero", "moeda", "data" ou "booleano". 
        raw (str): A string bruta a ser convertida para o tipo especificado. O método irá processar essa string de acordo com as regras de formatação para o tipo solicitado e retornar o valor convertido, ou a string original limpa se a conversão falhar ou se o tipo não for reconhecido.

    Returns:
        Any: O valor convertido para o tipo especificado, ou a string original limpa se a conversão falhar ou se o tipo não for reconhecido. Para "numero" e "moeda", retorna um float; para "data", retorna um objeto date; para "booleano", retorna "Sim" ou "Não".
    """
    raw = "" if raw is None else str(raw).strip()
    if raw == "":
        return ""

    if tipo == "numero":
        v = parse_decimal_br(raw)
        return v if v is not None else raw

    if tipo == "moeda":
        v = parse_decimal_br(raw)
        return v if v is not None else raw

    if tipo == "data":
        d = parse_date_any(raw)
        return d if d is not None else raw

    if tipo == "booleano":
        b = normalize_bool_ptbr(raw)
        return b if b is not None else ""

    return raw