"""Sumarização extrativa cidadã — baseline (guia §7).

Gera um resumo curto e acessível de um edital respondendo às quatro perguntas
do §7.1: o que está sendo contratado, quem pode participar, qual o prazo e qual
o valor. É um baseline **extrativo/baseado em regras** (sem rede neural): extrai
campos do `texto`/`objeto_html` com regex e os encaixa num parágrafo-modelo.

Serve de referência honesta para comparar com o modelo abstrativo (mT5/LLM) da
Fase 3, e — por ser determinístico — **não alucina** prazos ou valores.
"""

from __future__ import annotations

import re
import unicodedata

# "Entrega da Proposta: 16/05/2025 às 08:00Hs"
_RE_PROPOSTA = re.compile(
    r"Entrega da Proposta:\s*([0-3]?\d/[01]?\d/\d{4})", re.IGNORECASE
)
# "Edital a partir de: 16/05/2025 das 08:00..."
_RE_EDITAL = re.compile(
    r"Edital a partir de:\s*([0-3]?\d/[01]?\d/\d{4})", re.IGNORECASE
)


def _strip_accents_lower(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text or "")
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()


def clean_objeto(objeto_html: str, max_chars: int = 240) -> str:
    """Limpa o objeto: remove 'Objeto:' duplicado e corta na 1ª frase/limite."""
    texto = (objeto_html or "").strip()
    # O HTML às vezes traz "Objeto: Objeto: ..." e o tipo de pregão como prefixo.
    texto = re.sub(r"^\s*(Objeto:\s*)+", "", texto, flags=re.IGNORECASE)
    texto = re.sub(
        r"^\s*Preg[aã]o Eletr[oô]nico\s*-\s*", "", texto, flags=re.IGNORECASE
    )
    texto = texto.strip()
    if len(texto) <= max_chars:
        return texto
    # Corta no fim de frase mais próximo antes do limite; senão, corte seco.
    corte = texto[:max_chars]
    ponto = corte.rfind(". ")
    if ponto > max_chars * 0.5:
        return corte[: ponto + 1]
    return corte.rstrip() + "…"


def extract_prazo(texto: str) -> str | None:
    """Data de entrega da proposta (preferida) ou de abertura do edital."""
    m = _RE_PROPOSTA.search(texto or "")
    if m:
        return m.group(1)
    m = _RE_EDITAL.search(texto or "")
    return m.group(1) if m else None


def extract_participacao(texto: str) -> str:
    """Quem pode participar, a partir do tratamento diferenciado ME/EPP."""
    alvo = _strip_accents_lower(texto)
    if "participacao exclusiva" in alvo or "exclusiva de me" in alvo:
        return "exclusiva para microempresas e empresas de pequeno porte (ME/EPP)"
    if "me/epp" in alvo or "tratamento diferenciado: tipo" in alvo:
        return "aberta a todas as empresas, com benefícios para ME/EPP"
    return "aberta a empresas que atendam às exigências do edital"


def format_valor(total_homologado: str | None) -> str | None:
    """Formata 'R$ 62.800,00' a partir do campo BR; None se ausente/zero."""
    if not total_homologado:
        return None
    s = str(total_homologado).replace("R$", "").strip()
    num = s.replace(".", "").replace(",", ".")
    try:
        valor = float(num)
    except ValueError:
        return None
    if valor <= 0:
        return None
    return "R$ " + s


def summarize_record(rec: dict) -> dict:
    """Devolve resumo cidadão + os campos extraídos de um registro do corpus."""
    objeto = clean_objeto(rec.get("objeto_html") or rec.get("objeto_csv", ""))
    texto = rec.get("texto", "")
    modalidade = (rec.get("modalidade") or "").strip().capitalize()
    tipo = (rec.get("tipo") or "").strip().lower()
    orgao = rec.get("orgao_html") or rec.get("orgao_csv", "")

    verbo = "adquirir" if tipo == "material" else "contratar"
    quem = extract_participacao(texto)
    prazo = extract_prazo(texto)
    valor = format_valor(rec.get("total_homologado"))

    frases = [f"O órgão {orgao} pretende {verbo}: {objeto}".rstrip(". …") + "."]
    if modalidade:
        frases.append(f"A contratação ocorre na modalidade {modalidade}.")
    frases.append(f"A participação é {quem}.")
    if prazo:
        frases.append(f"As propostas podem ser entregues a partir de {prazo}.")
    if valor:
        frases.append(f"O valor homologado foi de {valor}.")

    return {
        "id": rec.get("id"),
        "resumo": " ".join(frases),
        "campos": {
            "objeto": objeto,
            "quem_pode_participar": quem,
            "prazo": prazo,
            "valor_homologado": valor,
            "modalidade": modalidade,
            "tipo": tipo,
        },
    }
