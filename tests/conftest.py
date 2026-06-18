"""Fixtures compartilhadas dos testes."""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CORPUS_PATH = ROOT / "data" / "processed" / "licitacoes_corpus.jsonl"
FIXTURE_CORPUS = Path(__file__).parent / "fixtures" / "minimal_corpus.jsonl"

requires_corpus = pytest.mark.skipif(
    not CORPUS_PATH.exists(),
    reason="corpus ausente — rode scripts/run_preprocess.py",
)
