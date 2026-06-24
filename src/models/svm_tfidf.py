"""Classificador clássico alternativo: TF-IDF + SVM linear (comparativo).

Mesmo vetorizador TF-IDF do baseline (``baseline_tfidf.PORTUGUESE_STOPWORDS``),
com ``SVC(kernel='linear')`` para comparar LogReg vs SVM no mesmo split e corpus.

Hiperparâmetros: ``configs/classification.yaml`` (bloco ``params``).
Treino: ``python scripts/run_train.py --model svm``.
"""

from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

from src.models.baseline_tfidf import PORTUGUESE_STOPWORDS


def build_svm(
    ngram_max: int = 2,
    min_df: int = 2,
    max_features: int | None = 20000,
    C: float = 1.0,
    class_weight: str | None = "balanced",
    kernel: str = "linear",
    probability: bool = True,
    seed: int = 42,
) -> Pipeline:
    """Monta o pipeline TF-IDF + SVM (não treinado).

    ``probability=True`` habilita ``predict_proba`` (calibração de Platt).
    """
    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=(1, ngram_max),
                    min_df=min_df,
                    max_features=max_features,
                    stop_words=PORTUGUESE_STOPWORDS,
                    sublinear_tf=True,
                    strip_accents="unicode",
                    lowercase=True,
                ),
            ),
            (
                "clf",
                SVC(
                    kernel=kernel,
                    C=C,
                    class_weight=class_weight,
                    probability=probability,
                    random_state=seed,
                ),
            ),
        ]
    )
