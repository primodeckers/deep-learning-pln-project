"""Testes do pipeline TF-IDF + SVM."""

from src.models.svm_tfidf import build_svm

_TEXTS = [
    "aquisicao de medicamentos hospitalares",
    "obras de pavimentacao asfaltica",
    "material de escritorio",
    "servico de limpeza predial",
]
_LABELS = ["Saude", "Infraestrutura/Obras", "Administracao/Outros", "Administracao/Outros"]


def test_build_svm_fits_and_predicts() -> None:
    texts = _TEXTS + _TEXTS
    labels = _LABELS + _LABELS
    pipe = build_svm(max_features=100, min_df=1, seed=42)
    pipe.fit(texts, labels)
    pred = pipe.predict(texts[:2])
    assert len(pred) == 2
    probs = pipe.predict_proba(texts[:1])
    assert probs.shape[1] == len(set(labels))
