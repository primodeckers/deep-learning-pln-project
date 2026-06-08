"""Orquestra o treino e a avaliação da classificação por macroárea.

Fluxo: carrega corpus → split estratificado → treina o modelo escolhido →
avalia em validação e teste → salva o modelo e um registro de experimento JSON
em ``experiments/`` (guia Fase 1/2 e §4).
"""

from __future__ import annotations

import collections
import json
from datetime import datetime, timezone
from pathlib import Path

import joblib

from src.evaluate.metrics_classification import (
    compute_metrics,
    format_metrics,
    save_confusion_matrix,
)
from src.models.baseline_tfidf import build_baseline
from src.preprocess.dataset import Dataset, make_dataset
from src.preprocess.labels import AREAS

# Raiz do repositório, para gravar caminhos relativos (portáveis entre máquinas).
ROOT = Path(__file__).resolve().parents[2]


def _rel(path: Path) -> str:
    """Caminho relativo à raiz do repo, em formato POSIX (estável no Git)."""
    try:
        return Path(path).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def _build_model(model_name: str, params: dict):
    """Resolve o nome do modelo para um estimador (não treinado)."""
    if model_name == "baseline":
        return build_baseline(
            ngram_max=params.get("ngram_max", 2),
            min_df=params.get("min_df", 2),
            max_features=params.get("max_features", 20000),
            C=params.get("C", 1.0),
            max_iter=params.get("max_iter", 1000),
            class_weight=params.get("class_weight", "balanced"),
            seed=params.get("seed", 42),
        )
    if model_name == "bertimbau":
        # Fase 2: fine-tuning de neuralmind/bert-base-portuguese-cased.
        # Requer torch + transformers (ainda não no ambiente). Ver src/models.
        raise NotImplementedError(
            "BERTimbau (Fase 2) ainda não implementado — ver guia §6.3."
        )
    raise ValueError(f"Modelo desconhecido: {model_name!r}")


def _class_distribution(dataset: Dataset) -> dict:
    def dist(labels: list[str]) -> dict:
        c = collections.Counter(labels)
        return {area: c.get(area, 0) for area in AREAS}

    return {
        "train": dist(dataset.train.labels),
        "val": dist(dataset.val.labels),
        "test": dist(dataset.test.labels),
    }


def train_classification(
    corpus_path: Path,
    config: dict,
    experiments_dir: Path,
    models_dir: Path,
    figures_dir: Path,
) -> dict:
    """Treina e avalia; devolve (e persiste) o registro do experimento."""
    model_name = config.get("model", "baseline")
    text_field = config.get("text_field", "texto")
    seed = config.get("seed", 42)
    params = config.get("params", {})
    params.setdefault("seed", seed)

    print(f"Carregando corpus de {corpus_path} (campo de texto: '{text_field}')")
    dataset = make_dataset(
        corpus_path,
        text_field=text_field,
        seed=seed,
        val_size=config.get("val_size", 0.15),
        test_size=config.get("test_size", 0.15),
    )
    print(
        f"  treino={len(dataset.train)}  val={len(dataset.val)}  "
        f"teste={len(dataset.test)}"
    )

    print(f"Treinando modelo '{model_name}'...")
    model = _build_model(model_name, params)
    model.fit(dataset.train.texts, dataset.train.labels)

    print("\nValidação:")
    val_pred = list(model.predict(dataset.val.texts))
    val_metrics = compute_metrics(dataset.val.labels, val_pred, AREAS)
    print(format_metrics(val_metrics))

    print("\nTeste:")
    test_pred = list(model.predict(dataset.test.texts))
    test_metrics = compute_metrics(dataset.test.labels, test_pred, AREAS)
    print(format_metrics(test_metrics))

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_id = f"classification_{model_name}_{timestamp}"

    # Salva o modelo treinado.
    models_dir.mkdir(parents=True, exist_ok=True)
    model_path = models_dir / f"{run_id}.joblib"
    joblib.dump(model, model_path)

    # Salva a matriz de confusão do teste como figura.
    fig_path = figures_dir / f"{run_id}_confusion.png"
    save_confusion_matrix(
        test_metrics, fig_path, title=f"Matriz de confusão — {model_name} (teste)"
    )

    # Registro do experimento.
    experiment = {
        "run_id": run_id,
        "task": "classification",
        "model": model_name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "text_field": text_field,
        "seed": seed,
        "params": params,
        "labels": AREAS,
        "class_distribution": _class_distribution(dataset),
        "splits": {
            "train": len(dataset.train),
            "val": len(dataset.val),
            "test": len(dataset.test),
        },
        "metrics": {"val": val_metrics, "test": test_metrics},
        "artifacts": {
            "model": _rel(model_path),
            "confusion_matrix": _rel(fig_path),
        },
    }

    experiments_dir.mkdir(parents=True, exist_ok=True)
    exp_path = experiments_dir / f"{run_id}.json"
    exp_path.write_text(
        json.dumps(experiment, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"\nModelo salvo em: {model_path}")
    print(f"Experimento salvo em: {exp_path}")
    return experiment
