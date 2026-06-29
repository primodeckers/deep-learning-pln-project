"""Testes de montagem do corpus PNCP."""

from pathlib import Path

import pytest

from src.preprocess.build_pncp_corpus import ESFERA_DISTRITAL_GDF, build_pncp_corpus_jsonl

ROOT = Path(__file__).resolve().parents[1]
PNCP_PATH = ROOT / "data" / "comprasGOV-anual-VW_FT_PNCP_COMPRA-2025.xls"

requires_pncp = pytest.mark.skipif(
    not PNCP_PATH.exists(),
    reason="arquivo PNCP ausente",
)


@requires_pncp
def test_build_pncp_corpus_gdf2025(tmp_path: Path) -> None:
    out = tmp_path / "pncp.jsonl"
    summary = build_pncp_corpus_jsonl(
        PNCP_PATH, out, esfera_id=ESFERA_DISTRITAL_GDF, ano=2025
    )
    assert summary["records_written"] >= 2_500
    assert summary["esfera_id_filter"] == "D"
    assert out.exists()
    lines = out.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == summary["records_written"]
    first = __import__("json").loads(lines[0])
    assert first["fonte"] == "pncp"
    assert first["esfera_id"] == "D"
    assert first["orgao_csv"]
    assert first["objeto_html"]


@requires_pncp
def test_build_pncp_corpus_uf_df_larger_than_gdf(tmp_path: Path) -> None:
    gdf = build_pncp_corpus_jsonl(
        PNCP_PATH, tmp_path / "gdf.jsonl", esfera_id="D", ano=2025
    )
    uf_df = build_pncp_corpus_jsonl(
        PNCP_PATH, tmp_path / "uf.jsonl", esfera_id=None, uf="DF", ano=2025
    )
    assert gdf["records_written"] < uf_df["records_written"]
