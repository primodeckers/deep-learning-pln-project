"""Testes de rastreamento de experimentos e fingerprint do corpus."""

from pathlib import Path

from tests.conftest import FIXTURE_CORPUS

from src.utils.experiment_tracking import (
    corpus_fingerprint,
    mlflow_tracking_uri,
)


def test_corpus_fingerprint_counts_records() -> None:
    fp = corpus_fingerprint(FIXTURE_CORPUS)
    assert fp["n_records"] == 30
    assert fp["size_bytes"] > 0
    assert len(fp["sha256"]) == 64


def test_corpus_fingerprint_is_stable() -> None:
    first = corpus_fingerprint(FIXTURE_CORPUS)
    second = corpus_fingerprint(FIXTURE_CORPUS)
    assert first["sha256"] == second["sha256"]


def test_corpus_fingerprint_relative_path() -> None:
    fp = corpus_fingerprint(FIXTURE_CORPUS)
    assert fp["path"].startswith("tests/fixtures/")


def test_mlflow_tracking_uri_uses_sqlite(tmp_path: Path) -> None:
    uri = mlflow_tracking_uri(tmp_path / "experiments")
    assert uri.startswith("sqlite:///")
    assert uri.endswith("mlflow.db")
