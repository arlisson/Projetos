# models.py
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List


FIELD_TYPES: List[str] = [
    "texto",
    "telefone",
    "email",
    "numero",
    "moeda",
    "data",
    "booleano",
]

EXCEL_NUMBER_FORMAT: Dict[str, str] = {
    "texto": "@",
    "telefone": "@",
    "email": "@",
    "numero": "0.00",
    "moeda": '"R$" #,##0.00',
    "data": "dd/mm/yyyy",
    "booleano": "@",
}


@dataclass
class Campo:
    """
    Representa um campo de extração, com propriedades como id, título, tipo, e flags para indicar se o campo é fixo ou bloqueado. O campo é identificado por um id único gerado a partir do título, e possui um tipo que pode ser inferido a partir do título ou definido explicitamente. A flag "fixo" indica se o campo é obrigatório e não pode ser removido, enquanto a flag "locked" indica se o campo está bloqueado para edição. A classe Campo é usada para definir os campos que serão extraídos dos documentos, e suas propriedades são utilizadas para configurar a extração e a exportação dos dados.
    """
    id: str
    titulo: str
    tipo: str = "texto"
    fixo: bool = False
    locked: bool = False


def sanitize_id(title: str) -> str:
    """Gera um ID sanitizado a partir de um título, convertendo-o para minúsculas, substituindo espaços por underscores, e removendo caracteres especiais. O método processa o título de entrada para criar um ID que seja seguro para uso em código e arquivos, garantindo que ele contenha apenas caracteres alfanuméricos e underscores. O resultado é um ID único e legível que pode ser usado para identificar campos de extração de forma consistente.
    Args:
        title (str): O título a partir do qual o ID será gerado. O método irá processar essa string para criar um ID sanitizado, convertendo-a para minúsculas, substituindo espaços por underscores, e removendo caracteres especiais, resultando em um ID seguro para uso em código e arquivos.

    Returns:
        str: O ID sanitizado gerado a partir do título, contendo apenas caracteres alfanuméricos e underscores, e convertido para minúsculas. O método garante que o ID seja legível e consistente para identificar campos de extração.
    """
    s = (title or "").strip().lower()
    s = s.replace(" ", "_")
    s = re.sub(r"[^a-z0-9_]+", "", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "campo"


def make_unique_id(base_id: str, used: set) -> str:
    """ Gera um ID único a partir de um ID base, garantindo que ele não esteja presente em um conjunto de IDs já utilizados. O método verifica se o ID base já está no conjunto de IDs utilizados, e se estiver, ele adiciona um sufixo numérico incremental (começando com "_2") até encontrar um ID que seja único. O ID gerado é adicionado ao conjunto de IDs utilizados para garantir que futuras chamadas ao método também considerem esse ID como utilizado. O resultado é um ID único que pode ser usado para identificar campos de extração ou outros elementos de forma consistente e sem conflitos.
    Args:
        base_id (str): O ID base a ser usado como base para gerar um ID único.
        used (set): Um conjunto de IDs já utilizados, para garantir unicidade.

    Returns:
        str: Um ID único gerado a partir do base_id e do conjunto de IDs utilizados.
    """
    cid = base_id
    i = 2
    while cid in used:
        cid = f"{base_id}_{i}"
        i += 1
    used.add(cid)
    return cid


def infer_type_from_title(header: str) -> str:
    """ Infere o tipo de um campo a partir do título do campo, utilizando palavras-chave comuns para identificar tipos como "email", "telefone", "data", "moeda", "numero" e "booleano". O método processa o título de entrada, convertendo-o para minúsculas e verificando a presença de palavras-chave específicas que indicam cada tipo. Se uma palavra-chave correspondente for encontrada, o método retorna o tipo inferido. Se nenhuma palavra-chave for encontrada, ele retorna "texto" como tipo padrão.
    Args:
        header (str): O título do campo a partir do qual o tipo será inferido.

    Returns:
        str: O tipo inferido a partir do título do campo.   
    """
    h = (header or "").strip().lower()
    if "email" in h or "e-mail" in h:
        return "email"
    if "tel" in h or "fone" in h or "whats" in h or "cel" in h:
        return "telefone"
    if "data" in h or "dt" == h:
        return "data"
    if "preço" in h or "preco" in h or "valor" in h or "custo" in h:
        return "moeda"
    if "qtd" in h or "quant" in h or "numero" in h or "número" in h:
        return "numero"
    if "ativo" in h or "status" in h:
        return "booleano"
    return "texto"