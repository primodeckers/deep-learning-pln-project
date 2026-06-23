"""Testes do classificador BERTimbau (Fase 2)."""

from __future__ import annotations

import pytest

from src.preprocess.labels import AREAS


def test_build_bert_classifier_labels() -> None:
    pytest.importorskip("torch")
    pytest.importorskip("transformers")

    from src.models.bert_classifier import build_bert_classifier

    clf = build_bert_classifier(seed=42)
    assert clf.label_list == AREAS
    assert len(clf.label2id) == len(AREAS)


def test_bert_import_error_message() -> None:
    """Sem torch, build deve falhar com mensagem clara (se torch ausente)."""
    try:
        import torch  # noqa: F401
    except ImportError:
        from src.models.bert_classifier import _require_bert_deps

        with pytest.raises(ImportError, match=r'\[bert\]'):
            _require_bert_deps()
        return
    pytest.skip("torch instalado — teste de ImportError não se aplica")
