"""Testes de load com classe Indeterminado."""

from pathlib import Path

import json

from src.preprocess.dataset import load_records
from src.preprocess.labels_setores import SETOR_INDETERMINADO


def test_load_setores_com_indeterminado(tmp_path: Path) -> None:
    corpus = tmp_path / "mini.jsonl"
    rows = [
        {"id": "1", "objeto_html": "Aquisicao de medicamentos hospitalares", "orgao_csv": "X"},
        {"id": "2", "objeto_html": "Credenciamento conforme edital", "orgao_csv": "Y"},
    ]
    corpus.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
        encoding="utf-8",
    )
    recs = load_records(corpus, label_scheme="setores", filter_unlabeled=False)
    assert len(recs) == 2
    areas = {r["id"]: r["area"] for r in recs}
    assert areas["1"] == "Saude"
    assert areas["2"] == "Indeterminado"


def test_load_setores_fallback_orgao(tmp_path: Path) -> None:
    corpus = tmp_path / "fb.jsonl"
    rows = [
        {"id": "1", "objeto_html": "Medicamentos hospitalares", "orgao_csv": "X"},
        {"id": "2", "objeto_html": "Credenciamento edital", "orgao_csv": "FUNDACAO NACIONAL DE SAUDE"},
        {"id": "3", "objeto_html": "Credenciamento edital", "orgao_csv": "ORGAO GENERICO"},
    ]
    corpus.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
        encoding="utf-8",
    )
    recs = load_records(corpus, label_scheme="setores_fallback_orgao")
    assert len(recs) == 3
    assert recs[0]["area"] == "Saude" and recs[0]["label_source"] == "objeto"
    assert recs[1]["area"] == "Saude" and recs[1]["label_source"] == "orgao"
    assert recs[2]["area"] == SETOR_INDETERMINADO and recs[2]["label_source"] == "indeterminado"
