"""Baseline clássico de classificação: TF-IDF + Regressão Logística.

Pipeline sklearn (guia §6.3): vetorização TF-IDF (1–2 grams, stopwords PT) +
LogisticRegression com ``class_weight='balanced'`` para mitigar o
desbalanceamento entre macroáreas. Serve de referência antes do BERTimbau.
"""

from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Stopwords mínimas em português. Mantida pequena de propósito: termos de domínio
# (ex.: "secretaria", "edital") são informativos e não são removidos.
# Sem acento de propósito: o vetorizador usa strip_accents="unicode", então as
# stopwords precisam estar na mesma forma normalizada (evita o UserWarning do
# sklearn sobre stopwords inconsistentes com o pré-processamento).
PORTUGUESE_STOPWORDS = [
    "a", "ao", "aos", "as", "com", "como", "da", "das", "de", "do",
    "dos", "e", "em", "entre", "essa", "esse", "esta", "este", "eu", "na", "nas",
    "no", "nos", "o", "os", "ou", "para", "pela", "pelas", "pelo", "pelos", "por",
    "que", "se", "sem", "ser", "seu", "sua", "sao", "tambem", "um", "uma", "uns",
    "umas",
]


def build_baseline(
    ngram_max: int = 2,
    min_df: int = 2,
    max_features: int | None = 20000,
    C: float = 1.0,
    max_iter: int = 1000,
    class_weight: str | None = "balanced",
    seed: int = 42,
) -> Pipeline:
    """Monta o pipeline TF-IDF + Regressão Logística (não treinado)."""
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
                LogisticRegression(
                    C=C,
                    max_iter=max_iter,
                    class_weight=class_weight,
                    random_state=seed,
                    n_jobs=None,
                ),
            ),
        ]
    )
