"""Rastreamento de experimentos: fingerprint do corpus + MLflow local.

Cada run grava um JSON portátil em ``experiments/`` e, quando o MLflow está
disponível, replica parâmetros, métricas, tags e artefatos em
``experiments/mlflow.db`` (backend SQLite local).
"""

from __future__ import annotations

import hashlib
import subprocess
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MLFLOW_EXPERIMENT = "pln-licitacoes"


def _rel(path: Path) -> str:
    try:
        return Path(path).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def corpus_fingerprint(corpus_path: Path) -> dict[str, Any]:
    """Identifica a versão do dataset usada em um experimento."""
    resolved = corpus_path.resolve()
    raw = resolved.read_bytes()
    n_records = 0
    if resolved.suffix == ".jsonl":
        with resolved.open(encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    n_records += 1
    return {
        "path": _rel(resolved),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "size_bytes": len(raw),
        "n_records": n_records,
    }


def git_commit_short() -> str | None:
    """Hash curto do HEAD, se o repositório for Git."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    commit = result.stdout.strip()
    return commit or None


def mlflow_tracking_uri(experiments_dir: Path) -> str:
    """Backend SQLite local (substitui o file store deprecado do MLflow 3.x)."""
    db_path = (experiments_dir / "mlflow.db").resolve()
    return f"sqlite:///{db_path.as_posix()}"


def mlflow_artifact_root(experiments_dir: Path) -> Path:
    return experiments_dir / "mlartifacts"


def _flatten_metrics(metrics: dict[str, Any], prefix: str = "") -> dict[str, float]:
    """Achata métricas aninhadas (ex.: val/test) para ``mlflow.log_metric``."""
    flat: dict[str, float] = {}
    for key, value in metrics.items():
        name = f"{prefix}{key}" if not prefix else f"{prefix}.{key}"
        if isinstance(value, dict):
            if {"accuracy", "f1_macro", "f1_weighted"} & value.keys():
                for metric_name, metric_value in value.items():
                    if metric_name in {"accuracy", "f1_macro", "f1_weighted"}:
                        flat[f"{name}.{metric_name}"] = float(metric_value)
            else:
                flat.update(_flatten_metrics(value, name))
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            flat[name] = float(value)
    return flat


@dataclass
class MlflowHandle:
    """Permite log incremental de métricas e artefatos dentro de uma run."""

    run_id: str
    _flatten: Any = field(default=None, repr=False)

    def log_metrics(self, metrics: dict[str, Any]) -> None:
        import mlflow

        for key, value in _flatten_metrics(metrics).items():
            mlflow.log_metric(key, value)

    def log_artifact(self, path: Path) -> None:
        import mlflow

        p = Path(path)
        if p.exists():
            if p.is_dir():
                mlflow.log_artifacts(str(p))
            else:
                mlflow.log_artifact(str(p))


@contextmanager
def mlflow_run(
    *,
    experiments_dir: Path,
    run_name: str,
    task: str,
    model: str,
    params: dict[str, Any],
    tags: dict[str, str],
    metrics: dict[str, Any] | None = None,
    artifacts: list[Path] | None = None,
) -> Iterator[MlflowHandle | None]:
    """Abre uma run MLflow; em falha, segue sem interromper o pipeline."""
    try:
        import mlflow
        from mlflow.tracking import MlflowClient
    except ImportError:
        yield None
        return

    try:
        tracking_uri = mlflow_tracking_uri(experiments_dir)
        artifact_root = mlflow_artifact_root(experiments_dir)
        artifact_root.mkdir(parents=True, exist_ok=True)

        mlflow.set_tracking_uri(tracking_uri)
        client = MlflowClient()
        if client.get_experiment_by_name(MLFLOW_EXPERIMENT) is None:
            client.create_experiment(
                MLFLOW_EXPERIMENT,
                artifact_location=artifact_root.resolve().as_uri(),
            )
        mlflow.set_experiment(MLFLOW_EXPERIMENT)

        with mlflow.start_run(run_name=run_name) as run:
            mlflow.set_tags(
                {
                    "task": task,
                    "model": model,
                    **tags,
                }
            )
            for key, value in params.items():
                mlflow.log_param(key, value)

            handle = MlflowHandle(run_id=run.info.run_id)

            if metrics:
                handle.log_metrics(metrics)
            if artifacts:
                for a in artifacts:
                    handle.log_artifact(a)

            yield handle
    except Exception as exc:
        print(f"Aviso: MLflow nao registrou a run ({exc})")
        yield None
