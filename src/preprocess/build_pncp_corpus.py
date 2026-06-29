"""Monta corpus JSONL a partir do PNCP (Compras.gov.br) para classificação PLN.

Espelha o schema do corpus ComprasNet (`licitacoes_corpus.jsonl`) para reutilizar
``dataset.py`` e ``clean_objeto.py``. Recorte padrão: esfera **D** (distrital / GDF) + ano 2025 (EDA ``03_eda_pncp``).
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.preprocess.labels import area_for_orgao

# PNCP: orgao_entidade_esfera_id — D = distrital (GDF), F = federal, E = estadual, ...
ESFERA_DISTRITAL_GDF = "D"


def build_pncp_corpus_jsonl(
    pncp_path: Path,
    output_path: Path,
    *,
    esfera_id: str | None = ESFERA_DISTRITAL_GDF,
    uf: str | None = None,
    ano: int | None = 2025,
) -> dict:
    """Filtra PNCP, mapeia colunas e grava JSONL compatível com ``load_records``."""
    df = pd.read_csv(pncp_path, encoding="utf-8", low_memory=False)

    if esfera_id is not None:
        df = df[df["orgao_entidade_esfera_id"] == esfera_id]
    if uf is not None:
        df = df[df["unidade_orgao_uf_sigla"] == uf]
    if ano is not None:
        df = df[df["ano_compra_pncp"] == ano]

    df = df.copy()
    df["objeto_compra"] = df["objeto_compra"].fillna("").astype(str).str.strip()
    df = df[df["objeto_compra"] != ""]
    if "informacao_complementar" in df.columns:
        df["informacao_complementar"] = (
            df["informacao_complementar"].fillna("").astype(str).str.strip()
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    area_counts: dict[str, int] = {}

    with output_path.open("w", encoding="utf-8") as out:
        for row in df.itertuples(index=False):
            orgao = str(getattr(row, "orgao_entidade_razao_social", "") or "").strip()
            objeto = str(getattr(row, "objeto_compra", "") or "").strip()
            info = ""
            if "informacao_complementar" in df.columns:
                info = str(getattr(row, "informacao_complementar", "") or "").strip()
            if not orgao or not objeto:
                continue

            cod = getattr(row, "cod_compra", None)
            ctrl = str(getattr(row, "numero_controle_PNCP", "") or "").strip()
            rec_id = str(cod) if cod is not None and str(cod).strip() else ctrl
            if not rec_id:
                continue

            area = area_for_orgao(orgao)
            area_counts[area] = area_counts.get(area, 0) + 1

            record = {
                "id": rec_id,
                "fonte": "pncp",
                "esfera_id": str(getattr(row, "orgao_entidade_esfera_id", "") or "").strip(),
                "numero_controle_pncp": ctrl,
                "orgao_csv": orgao,
                "orgao_html": str(
                    getattr(row, "unidade_orgao_nome_unidade", "") or ""
                ).strip(),
                "objeto_html": objeto,
                "objeto_csv": objeto,
                "informacao_complementar": info,
                "modalidade": str(getattr(row, "modalidade_nome", "") or "").strip(),
                "uf": str(getattr(row, "unidade_orgao_uf_sigla", "") or "").strip(),
                "ano": int(getattr(row, "ano_compra_pncp", 0) or 0),
                "total_homologado": getattr(row, "valor_total_homologado", None),
            }
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            written += 1

    return {
        "output": str(output_path),
        "records_written": written,
        "esfera_id_filter": esfera_id,
        "uf_filter": uf,
        "ano_filter": ano,
        "source_rows_after_filter": len(df),
        "area_distribution": area_counts,
    }
