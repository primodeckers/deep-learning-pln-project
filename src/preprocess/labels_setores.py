"""Rótulos empíricos de setor a partir do texto do objeto (9 classes).

Detecta domínio no ``objeto_compra`` / ``objeto_html`` por palavras-chave,
na mesma ordem de prioridade usada na EDA PNCP (``03_eda_pncp``). Compras
multi-setor recebem o **primeiro** setor que casar.

Decisão: ``docs/FASE1-CLASSIFICACAO.md`` — taxonomia alternativa às 6 macroáreas
derivadas do órgão (``labels.py``).
"""

from __future__ import annotations

import unicodedata

from src.preprocess.labels import DEFAULT_AREA, area_for_orgao

# Ordem importa: primeira keyword que casar define o rótulo exclusivo.
SETOR_KEYWORDS: list[tuple[str, tuple[str, ...]]] = [
    (
        "Saude",
        (
            "SAUDE",
            "HOSPITAL",
            "MEDIC",
            "CLINIC",
            "FARMAC",
            "ODONTO",
            "LABORATOR",
            "HEMOCENTRO",
            "AMBULANC",
            "ENFERMAG",
        ),
    ),
    (
        "Educacao",
        ("EDUCAC", "ESCOLA", "UNIVERSID", "ENSINO", "PEDAGOG", "ALUNO", "BIBLIOTEC"),
    ),
    (
        "Seguranca",
        (
            "POLICI",
            "BOMBEIRO",
            "SEGURANC",
            "PENITENCI",
            "CARCER",
            "GUARDA",
            "DEFESA CIVIL",
        ),
    ),
    (
        "Saneamento",
        (
            "SANEAMENT",
            "ESGOTO",
            "AGUA POT",
            "CAESB",
            "TRATAMENTO DE EFLUENT",
            "DRENAG",
        ),
    ),
    (
        "Infraestrutura/Obras",
        ("OBRA", "PAVIMENT", "INFRAESTRUTUR", "RODOVI", "CONSTRUC", "REFORMA"),
    ),
    (
        "TI/Administracao",
        (
            "SOFTWARE",
            "LICENCA",
            "INFORMAT",
            "COMPUT",
            "SISTEMA",
            "HOSPEDAGEM",
            "MOBILIARIO",
        ),
    ),
    ("Transporte", ("VEICUL", "COMBUSTIV", "TRANSPORT", "ONIBUS", "AUTOMOVEL")),
    ("Cultura", ("CULTUR", "MUSEU", "EVENTO", "ARTISTIC")),
    ("MeioAmbiente", ("AMBIENT", "FLOREST", "RESIDUO", "RECICL")),
]

SETORES: list[str] = [name for name, _ in SETOR_KEYWORDS]

# Fallback quando ``objeto_compra`` não contém keyword setorial (~48% PNCP DF/2025).
SETOR_INDETERMINADO = "Indeterminado"
SETORES_COM_INDETERMINADO: list[str] = SETORES + [SETOR_INDETERMINADO]


def normalize(text: str) -> str:
    """Maiúsculas e sem acentos, para casamento robusto de palavras-chave."""
    nfkd = unicodedata.normalize("NFKD", text or "")
    sem_acento = "".join(c for c in nfkd if not unicodedata.combining(c))
    return sem_acento.upper()


def setor_for_objeto(objeto: str) -> str | None:
    """Retorna o setor empírico do objeto ou ``None`` se não houver sinal."""
    alvo = normalize(objeto)
    for setor, keywords in SETOR_KEYWORDS:
        if any(kw in alvo for kw in keywords):
            return setor
    return None


def setor_label_for_objeto(
    objeto: str,
    *,
    unlabeled: str | None = None,
) -> str | None:
    """Como ``setor_for_objeto``, com fallback opcional para ``unlabeled``."""
    found = setor_for_objeto(objeto)
    if found is not None:
        return found
    return unlabeled


def setor_label_with_org_fallback(objeto: str, orgao: str) -> tuple[str, str]:
    """Rótulo híbrido: keyword no objeto; senão macroárea do órgão; senão Indeterminado.

    Retorna ``(label, fonte)`` com ``fonte`` em ``objeto``, ``orgao`` ou
    ``indeterminado``. Macroáreas nomeadas (5) casam 1:1 com setores homônimos;
    ``Administracao/Outros`` vira ``Indeterminado``.
    """
    found = setor_for_objeto(objeto)
    if found is not None:
        return found, "objeto"
    area = area_for_orgao(orgao)
    if area != DEFAULT_AREA:
        return area, "orgao"
    return SETOR_INDETERMINADO, "indeterminado"
