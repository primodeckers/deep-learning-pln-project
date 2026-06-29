"""Ponto de entrada para treino e avaliação de classificação de editais.

Exemplos:
    python scripts/run_train.py --model baseline
    python scripts/run_train.py --model svm
    python scripts/run_train.py --model bertimbau
    python scripts/run_train.py --config configs/classification_pncp.yaml \\
        --corpus data/processed/pncp_corpus_df2025.jsonl
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import mlflow

from src.train.train_classification import train_classification
from src.utils.experiment_tracking import MLFLOW_EXPERIMENT, mlflow_tracking_uri

DEFAULT_CORPUS = ROOT / "data" / "processed" / "licitacoes_corpus.jsonl"
DEFAULT_CONFIG = ROOT / "configs" / "classification.yaml"
EXPERIMENTS_DIR = ROOT / "experiments"
MODELS_DIR = ROOT / "models"
FIGURES_DIR = ROOT / "reports" / "figures"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Treina e avalia classificadores de PLN sobre o corpus de licitações."
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Sobrescreve o modelo do config (baseline, svm, bertimbau).",
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument(
        "--text-field",
        default=None,
        help="Sobrescreve o campo de texto do config (ex.: objeto_html).",
    )
    return parser


def load_config(path: Path) -> dict:
    if path.exists():
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {}


def main() -> None:
    mlflow.set_tracking_uri(mlflow_tracking_uri(EXPERIMENTS_DIR))
    mlflow.set_experiment(MLFLOW_EXPERIMENT)
    mlflow.autolog()

    args = build_parser().parse_args()
    config = load_config(args.config)
    if args.model:
        config["model"] = args.model
    if args.text_field:
        config["text_field"] = args.text_field
    config.setdefault("model", "baseline")

    train_classification(
        corpus_path=args.corpus,
        config=config,
        experiments_dir=EXPERIMENTS_DIR,
        models_dir=MODELS_DIR,
        figures_dir=FIGURES_DIR,
    )


if __name__ == "__main__":
    main()
