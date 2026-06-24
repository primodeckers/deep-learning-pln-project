"""Orquestra treino e avaliação da classificação por macroárea (Fase 1).

Fluxo: corpus → split → ``fit`` no treino → métricas em val/test → artefatos
(modelo joblib, JSON em ``experiments/``, matriz PNG, MLflow opcional).

Padrões de registro e mapa de módulos: ``docs/FASE1-CLASSIFICACAO.md`` §2 e §6.
"""

from __future__ import annotations

import collections
import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import mlflow
from mlflow.entities import SpanType

from src.evaluate.metrics_classification import (
    compute_metrics,
    format_metrics,
    save_confusion_matrix,
)
from src.models.baseline_tfidf import build_baseline
from src.models.bert_classifier import build_bert_classifier
from src.models.svm_tfidf import build_svm
from src.preprocess.dataset import Dataset, make_dataset
from src.preprocess.labels import AREAS
from src.utils.experiment_tracking import (
    MlflowHandle,
    corpus_fingerprint,
    git_commit_short,
    mlflow_run,
)

# Raiz do repositório, para gravar caminhos relativos (portáveis entre máquinas).
ROOT = Path(__file__).resolve().parents[2]

# Hiperparâmetros relevantes por modelo. O config junta baseline + bert no mesmo
# bloco `params`; ao registrar o experimento, guardamos só os do modelo que rodou
# para o JSON não misturar parâmetros não usados.
_MODEL_PARAM_KEYS = {
    "baseline": (
        "ngram_max",
        "min_df",
        "max_features",
        "C",
        "max_iter",
        "class_weight",
        "seed",
    ),
    "svm": (
        "ngram_max",
        "min_df",
        "max_features",
        "C",
        "class_weight",
        "svm_kernel",
        "svm_probability",
        "seed",
    ),
    "bertimbau": (
        "model_name",
        "max_length",
        "batch_size",
        "learning_rate",
        "epochs",
        "early_stopping_patience",
        "seed",
    ),
}


def _relevant_params(model_name: str, params: dict) -> dict:
    """Filtra `params` para as chaves usadas pelo modelo (fallback: tudo)."""
    keys = _MODEL_PARAM_KEYS.get(model_name)
    if keys is None:
        return dict(params)
    return {k: params[k] for k in keys if k in params}


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
    if model_name == "svm":
        return build_svm(
            ngram_max=params.get("ngram_max", 2),
            min_df=params.get("min_df", 2),
            max_features=params.get("max_features", 20000),
            C=params.get("C", 1.0),
            class_weight=params.get("class_weight", "balanced"),
            kernel=params.get("svm_kernel", "linear"),
            probability=params.get("svm_probability", True),
            seed=params.get("seed", 42),
        )
    if model_name == "bertimbau":
        return build_bert_classifier(
            label_list=AREAS,
            model_name=params.get(
                "model_name", "neuralmind/bert-base-portuguese-cased"
            ),
            max_length=params.get("max_length", 512),
            batch_size=params.get("batch_size", 16),
            learning_rate=params.get("learning_rate", 2.0e-5),
            epochs=params.get("epochs", 4),
            early_stopping_patience=params.get("early_stopping_patience", 2),
            seed=params.get("seed", 42),
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


@mlflow.trace(name="train_classification", span_type=SpanType.CHAIN)
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

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_id = f"classification_{model_name}_{timestamp}"
    dataset_info = corpus_fingerprint(corpus_path)
    git_commit = git_commit_short()

    mlflow_tags = {
        "corpus_sha256": dataset_info["sha256"],
        "corpus_path": dataset_info["path"],
        "corpus_n_records": str(dataset_info["n_records"]),
        "text_field": text_field,
    }
    if git_commit:
        mlflow_tags["git_commit"] = git_commit

    with mlflow_run(
        experiments_dir=experiments_dir,
        run_name=run_id,
        task="classification",
        model=model_name,
        params={
            "text_field": text_field,
            "seed": seed,
            **_relevant_params(model_name, params),
        },
        tags=mlflow_tags,
    ) as handle:
        print(f"Treinando modelo '{model_name}'...")
        model = _build_model(model_name, params)
        bert_cache = experiments_dir / ".bert_cache" / run_id
        with mlflow.start_span(name="fit", span_type=SpanType.TOOL) as span:
            span.set_inputs({"model": model_name, "n_samples": len(dataset.train)})
            if model_name == "bertimbau":
                model.fit(
                    dataset.train.texts,
                    dataset.train.labels,
                    val_texts=dataset.val.texts,
                    val_labels=dataset.val.labels,
                    output_dir=bert_cache,
                )
            else:
                model.fit(dataset.train.texts, dataset.train.labels)
            span.set_outputs({"status": "fitted"})

        with mlflow.start_span(name="evaluate_val", span_type=SpanType.TOOL) as span:
            span.set_inputs({"split": "val", "n_samples": len(dataset.val)})
            print("\nValidação:")
            val_pred = list(model.predict(dataset.val.texts))
            val_metrics = compute_metrics(dataset.val.labels, val_pred, AREAS)
            print(format_metrics(val_metrics))
            span.set_outputs(val_metrics)

        with mlflow.start_span(name="evaluate_test", span_type=SpanType.TOOL) as span:
            span.set_inputs({"split": "test", "n_samples": len(dataset.test)})
            print("\nTeste:")
            test_pred = list(model.predict(dataset.test.texts))
            test_metrics = compute_metrics(dataset.test.labels, test_pred, AREAS)
            print(format_metrics(test_metrics))
            span.set_outputs(test_metrics)

        models_dir.mkdir(parents=True, exist_ok=True)
        if model_name == "bertimbau":
            model_path = models_dir / run_id
            model.save(model_path)
        else:
            model_path = models_dir / f"{run_id}.joblib"
            joblib.dump(model, model_path)

        fig_path = figures_dir / f"{run_id}_confusion.png"
        save_confusion_matrix(
            test_metrics,
            fig_path,
            title=f"Matriz de confusão — {model_name} (teste)",
        )

        experiment = {
            "run_id": run_id,
            "task": "classification",
            "model": model_name,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "text_field": text_field,
            "seed": seed,
            "dataset": dataset_info,
            "git_commit": git_commit,
            "params": _relevant_params(model_name, params),
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

        if isinstance(handle, MlflowHandle):
            handle.log_metrics(experiment["metrics"])
            if model_name == "bertimbau":
                handle.log_transformers_model(model_path)
            else:
                handle.log_artifact(model_path)
            handle.log_artifact(fig_path)
            handle.log_artifact(exp_path)
            experiment["mlflow_run_id"] = handle.run_id

    print(f"\nModelo salvo em: {model_path}")
    print(f"Experimento salvo em: {exp_path}")
    if experiment.get("mlflow_run_id"):
        print(f"MLflow run: {experiment['mlflow_run_id']}")
    return experiment
