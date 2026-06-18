"""Carrega o corpus JSONL e faz split estratificado treino/val/test (Fase 1).

Split 70/15/15 estratificado por ``area``, ``seed`` fixa — mesmas partições
para baseline e BERTimbau (comparabilidade). O campo de texto padrão em código
é ``texto``; a config de produção usa ``objeto_html`` (anti-leakage).

Decisões: ``docs/FASE1-CLASSIFICACAO.md`` §3.2 e §3.3.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from sklearn.model_selection import train_test_split

from src.preprocess.labels import area_for_orgao


@dataclass
class Split:
    """Um conjunto de exemplos: textos (X) e labels (y) alinhados por índice."""

    texts: list[str]
    labels: list[str]
    ids: list[str]

    def __len__(self) -> int:
        return len(self.texts)


@dataclass
class Dataset:
    train: Split
    val: Split
    test: Split


def load_records(corpus_path: Path) -> list[dict]:
    """Lê o JSONL e anexa o campo ``area`` (label derivado de ``orgao_csv``)."""
    records: list[dict] = []
    with corpus_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            rec["area"] = area_for_orgao(rec.get("orgao_csv", ""))
            records.append(rec)
    return records


def _to_split(rows: list[dict], text_field: str) -> Split:
    return Split(
        texts=[r.get(text_field) or "" for r in rows],
        labels=[r["area"] for r in rows],
        ids=[r["id"] for r in rows],
    )


def make_dataset(
    corpus_path: Path,
    text_field: str = "texto",
    seed: int = 42,
    val_size: float = 0.15,
    test_size: float = 0.15,
) -> Dataset:
    """Carrega o corpus e devolve as três partições estratificadas por área."""
    records = load_records(corpus_path)
    labels = [r["area"] for r in records]

    # Dois cortes: sklearn não oferece train/val/test numa chamada. Primeiro
    # reservamos o teste; depois dividimos o restante com val_rel reescalado.
    rest, test = train_test_split(
        records,
        test_size=test_size,
        stratify=labels,
        random_state=seed,
    )
    # val_rel = proporção de val sobre (train+val), não sobre o corpus inteiro.
    rest_labels = [r["area"] for r in rest]
    val_rel = val_size / (1.0 - test_size)
    train, val = train_test_split(
        rest,
        test_size=val_rel,
        stratify=rest_labels,
        random_state=seed,
    )

    return Dataset(
        train=_to_split(train, text_field),
        val=_to_split(val, text_field),
        test=_to_split(test, text_field),
    )
