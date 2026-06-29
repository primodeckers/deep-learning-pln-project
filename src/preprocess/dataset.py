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

from src.preprocess.clean_objeto import get_text_for_field, texto_objeto_com_info
from src.preprocess.labels import area_for_orgao
from src.preprocess.labels_setores import (
    SETOR_INDETERMINADO,
    setor_label_for_objeto,
    setor_label_with_org_fallback,
)


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


def _label_for_record(
    rec: dict,
    label_scheme: str,
    *,
    unlabeled_label: str | None = None,
    include_info_complementar: bool = False,
) -> str | None:
    objeto = texto_objeto_com_info(rec, include_info=include_info_complementar)
    if label_scheme == "setores_fallback_orgao":
        label, _ = setor_label_with_org_fallback(objeto, rec.get("orgao_csv", ""))
        return label
    if label_scheme == "setores":
        return setor_label_for_objeto(objeto, unlabeled=unlabeled_label)
    return area_for_orgao(rec.get("orgao_csv", ""))


def load_records(
    corpus_path: Path,
    *,
    label_scheme: str = "orgao",
    filter_unlabeled: bool = False,
    unlabeled_label: str | None = None,
    include_info_complementar: bool = False,
) -> list[dict]:
    """Lê o JSONL e anexa o campo ``area`` conforme ``label_scheme``.

    ``orgao`` — macroárea a partir de ``orgao_csv`` (6 classes + fallback).
    ``setores`` — setor empírico a partir do objeto (9 classes). Sem keyword:
    omitido se ``filter_unlabeled=True``; senão ``unlabeled_label`` (ex.:
    ``Indeterminado``) ou erro se não definido.
    ``setores_fallback_orgao`` — keyword no objeto; se ausente, macroárea do
    órgão (5 nomeadas); senão ``Indeterminado``. Entrada continua só texto.
    """
    if label_scheme == "setores" and not filter_unlabeled and unlabeled_label is None:
        unlabeled_label = SETOR_INDETERMINADO

    records: list[dict] = []
    with corpus_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if label_scheme == "setores_fallback_orgao":
                objeto = texto_objeto_com_info(rec, include_info=include_info_complementar)
                area, fonte = setor_label_with_org_fallback(
                    objeto, rec.get("orgao_csv", "")
                )
                rec["area"] = area
                rec["label_source"] = fonte
                records.append(rec)
                continue
            area = _label_for_record(
                rec,
                label_scheme,
                unlabeled_label=unlabeled_label,
                include_info_complementar=include_info_complementar,
            )
            if area is None:
                if filter_unlabeled:
                    continue
                raise ValueError(
                    "Registro sem setor detectável com label_scheme='setores'. "
                    "Use filter_unlabeled=True, unlabeled_label ou include_indeterminado."
                )
            rec["area"] = area
            records.append(rec)
    return records


def _to_split(rows: list[dict], text_field: str) -> Split:
    return Split(
        texts=[get_text_for_field(r, text_field) for r in rows],
        labels=[r["area"] for r in rows],
        ids=[r["id"] for r in rows],
    )


def make_dataset(
    corpus_path: Path,
    text_field: str = "texto",
    seed: int = 42,
    val_size: float = 0.15,
    test_size: float = 0.15,
    *,
    label_scheme: str = "orgao",
    filter_unlabeled: bool = False,
    unlabeled_label: str | None = None,
    include_info_complementar: bool = False,
) -> Dataset:
    """Carrega o corpus e devolve as três partições estratificadas por área."""
    records = load_records(
        corpus_path,
        label_scheme=label_scheme,
        filter_unlabeled=filter_unlabeled,
        unlabeled_label=unlabeled_label,
        include_info_complementar=include_info_complementar,
    )
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
