"""Ponto de entrada para treino e avaliação dos modelos de PLN.

Exemplos (guia §10):
    python scripts/run_train.py --task classification --model baseline
    python scripts/run_train.py --task classification --model bertimbau
    python scripts/run_train.py --task classification --config configs/classification.yaml
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.summarize.run_summarization import run_summarization
from src.train.train_classification import train_classification

DEFAULT_CORPUS = ROOT / "data" / "processed" / "licitacoes_corpus.jsonl"
DEFAULT_CONFIG = ROOT / "configs" / "classification.yaml"
EXPERIMENTS_DIR = ROOT / "experiments"
MODELS_DIR = ROOT / "models"
FIGURES_DIR = ROOT / "reports" / "figures"
PROCESSED_DIR = ROOT / "data" / "processed"
SLIDES_DIR = ROOT / "reports" / "slides"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Treina e avalia modelos de PLN sobre o corpus de licitações."
    )
    parser.add_argument(
        "--task",
        choices=["classification", "summarization"],
        default="classification",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Sobrescreve o modelo definido no config (ex.: baseline, bertimbau).",
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument(
        "--text-field",
        default=None,
        help="Sobrescreve o campo de texto do config (ex.: texto, objeto_html).",
    )
    return parser


def load_config(path: Path) -> dict:
    if path.exists():
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {}


def main() -> None:
    args = build_parser().parse_args()

    if args.task == "summarization":
        model = args.model or "extractive"
        if model != "extractive":
            raise NotImplementedError(
                f"Sumarização '{model}' (abstrativo mT5/LLM) ainda não implementada "
                "— ver guia §7.2. Use --model extractive."
            )
        run_summarization(
            corpus_path=args.corpus,
            processed_dir=PROCESSED_DIR,
            slides_dir=SLIDES_DIR,
            experiments_dir=EXPERIMENTS_DIR,
        )
        return

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
