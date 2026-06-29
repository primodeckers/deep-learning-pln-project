"""Limpeza do campo objeto para reduzir boilerplate e vazamento de label.

Remove prefixos administrativos repetidos (``Objeto:``, ``Pregão Eletrônico -``)
e, opcionalmente, o nome do órgão quando copiado no texto do objeto.

Ver ``docs/VAZAMENTO-DE-LABEL.md`` e EDA Tabela 7 (``objeto_html_limpo``).
"""

from __future__ import annotations

import re

from src.preprocess.labels import normalize

_URL = re.compile(r"https?://\S+")
_OBJETO_LABEL = re.compile(r"^(?:objeto\s*:\s*)+", re.IGNORECASE)
_MODALIDADE_PREFIX = re.compile(
    r"^(?:"
    r"preg[aã]o\s+eletr[oô]nico"
    r"|dispensa\s+eletr[oô]nica"
    r"|concorr[eê]ncia(?:\s+p[uú]blica)?"
    r"|tomada\s+de\s+prec[oô]s"
    r"|inexigibilidade(?:\s+de\s+licita[cç][aã]o)?"
    r"|credenciamento"
    r")\s*[-:\u2013\u2014]+\s*",
    re.IGNORECASE,
)

KNOWN_TEXT_FIELDS = frozenset(
    {"texto", "objeto_html", "objeto_csv", "objeto_html_limpo", "objeto_info_limpo"}
)


def _orgaos_para_limpeza(*orgaos: str | None) -> list[str]:
    """Lista única de nomes de órgão (CSV/HTML) usados para tirar vazamento do objeto."""
    seen: set[str] = set()
    out: list[str] = []
    for raw in orgaos:
        o = (raw or "").strip()
        if len(o) < 8:
            continue
        key = normalize(o)
        if key not in seen:
            seen.add(key)
            out.append(o)
    return out


def limpar_objeto(
    texto: str,
    orgao: str | None = None,
    *,
    orgaos: list[str] | None = None,
) -> str:
    """Remove boilerplate do objeto; opcionalmente tira nomes de órgão repetidos no texto."""
    t = (texto or "").strip()
    for _ in range(3):
        t = _OBJETO_LABEL.sub("", t).strip()
        t = _MODALIDADE_PREFIX.sub("", t).strip()
    alvos = orgaos if orgaos is not None else _orgaos_para_limpeza(orgao)
    for nome in alvos:
        t = _strip_orgao(t, nome)
    return re.sub(r"\s+", " ", t).strip()


def limpar_info_complementar(texto: str) -> str:
    """Remove URLs e normaliza espaços em ``informacao_complementar``."""
    t = _URL.sub(" ", texto or "").strip()
    return re.sub(r"\s+", " ", t).strip()


def texto_objeto_com_info(rec: dict, *, include_info: bool) -> str:
    """Concatena objeto bruto com info complementar (se houver e ``include_info``)."""
    objeto = rec.get("objeto_html") or rec.get("objeto_compra") or ""
    if not include_info:
        return objeto
    info = (rec.get("informacao_complementar") or "").strip()
    if info:
        return f"{objeto} {info}".strip()
    return objeto


def _strip_orgao(texto: str, orgao: str) -> str:
    orgao = (orgao or "").strip()
    if len(orgao) < 8:
        return texto
    # Remove ocorrência literal (case-insensitive) do nome do órgão no objeto.
    pattern = re.compile(re.escape(orgao), flags=re.IGNORECASE)
    if not pattern.search(texto):
        org_norm = normalize(orgao)
        if len(org_norm) >= 8 and org_norm in normalize(texto):
            # Fallback: remove tokens longos do órgão (≥4 chars) presentes no texto.
            for token in org_norm.split():
                if len(token) >= 4 and token not in {"ESTADO", "DISTRITO", "FEDERAL"}:
                    texto = re.sub(rf"\b{re.escape(token)}\b", " ", texto, flags=re.IGNORECASE)
        return re.sub(r"\s+", " ", texto).strip()
    return pattern.sub(" ", texto).strip()


def get_text_for_field(rec: dict, text_field: str) -> str:
    """Resolve o texto de entrada conforme ``text_field`` (inclui ``objeto_html_limpo``)."""
    if text_field == "objeto_html_limpo":
        raw = rec.get("objeto_html") or rec.get("objeto_csv") or ""
        orgaos = _orgaos_para_limpeza(rec.get("orgao_csv"), rec.get("orgao_html"))
        return limpar_objeto(raw, orgaos=orgaos)
    if text_field == "objeto_info_limpo":
        orgaos = _orgaos_para_limpeza(rec.get("orgao_csv"), rec.get("orgao_html"))
        raw_obj = rec.get("objeto_html") or rec.get("objeto_csv") or ""
        obj = limpar_objeto(raw_obj, orgaos=orgaos)
        info = limpar_info_complementar(rec.get("informacao_complementar") or "")
        return " ".join(p for p in (obj, info) if p).strip()
    if text_field not in KNOWN_TEXT_FIELDS:
        raise ValueError(
            f"text_field desconhecido: {text_field!r}. "
            f"Use um de: {sorted(KNOWN_TEXT_FIELDS)}"
        )
    return rec.get(text_field) or ""
