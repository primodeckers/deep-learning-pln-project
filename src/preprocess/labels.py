"""Mapeamento órgão → macroárea de gasto público.

Taxonomia definida no guia (UNIVERSAL-DEEP-LEARNING-GUIDE.md §6.1). O label é
derivado do campo ``orgao_csv`` por palavras-chave. O modelo NÃO recebe o órgão
como feature — apenas o texto do edital; o órgão só gera o label inicial
(limitação "label proxy" declarada no relatório).
"""

from __future__ import annotations

import unicodedata

# Rótulo padrão para órgãos que não casam com nenhuma regra.
DEFAULT_AREA = "Administracao/Outros"

# Ordem importa: a primeira macroárea cuja palavra-chave casar vence.
# Palavras-chave já normalizadas (maiúsculas, sem acento).
AREA_KEYWORDS: list[tuple[str, tuple[str, ...]]] = [
    ("Saude", ("SAUDE", "HEMOCENTRO")),
    ("Saneamento", ("CAESB", "SANEAMENTO")),
    ("Seguranca", ("POLICIA", "BOMBEIRO", "SEGURANCA", "PENITENCI")),
    ("Educacao", ("EDUCACAO",)),
    ("Infraestrutura/Obras", ("ESTRADAS", "RODAGEM", "OBRAS", "INFRAESTRUTURA")),
]

# Lista canônica de classes (índice estável para matrizes de confusão).
AREAS: list[str] = [area for area, _ in AREA_KEYWORDS] + [DEFAULT_AREA]


def normalize(text: str) -> str:
    """Maiúsculas e sem acentos, para casamento robusto de palavras-chave."""
    nfkd = unicodedata.normalize("NFKD", text or "")
    sem_acento = "".join(c for c in nfkd if not unicodedata.combining(c))
    return sem_acento.upper()


def area_for_orgao(orgao: str) -> str:
    """Retorna a macroárea de gasto para um nome de órgão (``orgao_csv``)."""
    alvo = normalize(orgao)
    for area, keywords in AREA_KEYWORDS:
        if any(kw in alvo for kw in keywords):
            return area
    return DEFAULT_AREA
