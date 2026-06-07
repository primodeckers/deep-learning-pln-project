# -*- coding: utf-8 -*-
"""Extracao de texto e campos dos HTMLs de detalhe do ComprasNet."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from html import unescape
from pathlib import Path

from bs4 import BeautifulSoup


@dataclass
class DetalheExtraido:
    file_id: str
    orgao: str
    codigo_uasg: str
    titulo_licitacao: str
    objeto: str
    secao_itens: str
    texto_completo: str
    num_caracteres: int
    num_itens: int


def _decode_html(raw: bytes) -> str:
    for encoding in ("iso-8859-1", "latin-1", "utf-8"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("iso-8859-1", errors="replace")


def _clean_text(text: str) -> str:
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _extract_between_label(html_chunk: str, label: str) -> str:
    pattern = rf"<b>{label}:</b>&nbsp;(.*?)<br>"
    match = re.search(pattern, html_chunk, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return ""
    return _clean_text(re.sub(r"<[^>]+>", " ", match.group(1)))


def extract_from_html(html_path: Path) -> DetalheExtraido:
    raw = html_path.read_bytes()
    html = _decode_html(raw)
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "iframe"]):
        tag.decompose()

    body = soup.body or soup
    paragraphs = [_clean_text(p.get_text(" ", strip=True)) for p in body.find_all("p")]
    paragraphs = [p for p in paragraphs if p]

    orgao = ""
    codigo_uasg = ""
    for p in paragraphs[:6]:
        uasg_match = re.search(r"UASG:\s*(\d+)", p, flags=re.IGNORECASE)
        if uasg_match:
            codigo_uasg = uasg_match.group(1)
            continue
        if "GOVERNO DO DISTRITO" in p.upper():
            continue
        if not orgao and len(p) > 5:
            orgao = p

    titulo_match = re.search(
        r"(Preg.o Eletr[^<]+|Dispensa Eletr[^<]+|Concorr[^<]+)",
        html,
        flags=re.IGNORECASE,
    )
    titulo_licitacao = _clean_text(titulo_match.group(0)) if titulo_match else ""

    objeto = _extract_between_label(html, "Objeto")

    item_titles = [
        _clean_text(tag.get_text(" ", strip=True))
        for tag in body.find_all("span", class_="tex3b")
        if re.match(r"^\d+\s+-", tag.get_text(strip=True))
    ]
    secao_itens = "\n".join(item_titles)
    texto_completo = _clean_text(body.get_text("\n", strip=True))

    return DetalheExtraido(
        file_id=html_path.stem,
        orgao=orgao,
        codigo_uasg=codigo_uasg,
        titulo_licitacao=titulo_licitacao,
        objeto=objeto,
        secao_itens=secao_itens,
        texto_completo=texto_completo,
        num_caracteres=len(texto_completo),
        num_itens=len(item_titles),
    )


def extract_all_html(
    input_dir: Path,
    text_dir: Path,
    records_dir: Path,
    *,
    overwrite: bool = False,
) -> dict:
    text_dir.mkdir(parents=True, exist_ok=True)
    records_dir.mkdir(parents=True, exist_ok=True)

    html_files = sorted(input_dir.glob("*.html"))
    results = []

    for html_path in html_files:
        text_path = text_dir / f"{html_path.stem}.txt"
        record_path = records_dir / f"{html_path.stem}.json"

        if text_path.exists() and record_path.exists() and not overwrite:
            results.append({"file_id": html_path.stem, "status": "skipped"})
            continue

        extracted = extract_from_html(html_path)
        text_path.write_text(extracted.texto_completo, encoding="utf-8")
        record_path.write_text(
            json.dumps(asdict(extracted), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        results.append(
            {
                "file_id": html_path.stem,
                "status": "ok",
                "num_caracteres": extracted.num_caracteres,
                "num_itens": extracted.num_itens,
            }
        )

    summary = {
        "input_dir": str(input_dir),
        "text_dir": str(text_dir),
        "records_dir": str(records_dir),
        "total": len(html_files),
        "ok": sum(1 for r in results if r["status"] == "ok"),
        "skipped": sum(1 for r in results if r["status"] == "skipped"),
        "items": results,
    }
    return summary
