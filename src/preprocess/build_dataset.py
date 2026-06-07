"""Monta dataset unificado (HTML + metadados do CSV)."""

from __future__ import annotations

import json
from pathlib import Path

from src.collect.load_licitacoes import load_licitacoes


def build_corpus_jsonl(
    csv_path: Path,
    records_dir: Path,
    output_path: Path,
) -> dict:
    records_by_id = {
        p.stem: json.loads(p.read_text(encoding="utf-8"))
        for p in records_dir.glob("*.json")
    }

    licitacoes = load_licitacoes(csv_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    written = 0
    missing_html = 0
    seen_ids: set[str] = set()

    with output_path.open("w", encoding="utf-8") as out:
        for row in licitacoes:
            file_id = row.file_stem
            if file_id in seen_ids:
                continue
            seen_ids.add(file_id)

            html_data = records_by_id.get(file_id)
            if not html_data:
                missing_html += 1
                continue

            record = {
                "id": file_id,
                "numero_licitacao": row.numero,
                "modalidade": row.modalidade,
                "situacao": row.situacao,
                "orgao_csv": row.orgao,
                "orgao_html": html_data.get("orgao", ""),
                "tipo": row.tipo,
                "objeto_csv": row.objeto,
                "objeto_html": html_data.get("objeto", ""),
                "total_homologado": row.total_homologado,
                "edital_url": row.edital_url,
                "texto": html_data.get("texto_completo", ""),
                "num_caracteres": html_data.get("num_caracteres", 0),
                "num_itens": html_data.get("num_itens", 0),
            }
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            written += 1

    return {
        "output": str(output_path),
        "records_written": written,
        "missing_html": missing_html,
        "csv_rows": len(licitacoes),
        "unique_ids": len(seen_ids),
    }
