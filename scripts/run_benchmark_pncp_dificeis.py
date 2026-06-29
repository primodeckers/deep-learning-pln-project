"""Benchmark PNCP: compras excluídas do pncp9 e detecção de sinal setorial.

Gera ``reports/benchmark_pncp_casos_dificeis.json`` com:
- coortes (com keyword / sem keyword Admin / sem keyword macroárea nomeada)
- vazamento lexical (%)
- avaliação LogReg (macroárea órgão) no subconjunto difícil (~853)

Uso:
    python scripts/run_benchmark_pncp_dificeis.py
    python scripts/run_benchmark_pncp_dificeis.py --corpus data/processed/pncp_corpus_df2025.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split

from src.evaluate.metrics_classification import compute_metrics
from src.models.baseline_tfidf import build_baseline
from src.preprocess.clean_objeto import get_text_for_field
from src.preprocess.labels import DEFAULT_AREA, area_for_orgao
from src.preprocess.labels_setores import (
    SETOR_INDETERMINADO,
    SETORES,
    setor_for_objeto,
    setor_label_for_objeto,
)

DEFAULT_CORPUS = ROOT / "data" / "processed" / "pncp_corpus_df2025.jsonl"
DEFAULT_OUT = ROOT / "reports" / "benchmark_pncp_casos_dificeis.json"


def _load_corpus(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _cohort(rec: dict) -> str:
    objeto = rec.get("objeto_html") or rec.get("objeto_compra") or ""
    has_kw = setor_for_objeto(objeto) is not None
    area = area_for_orgao(rec.get("orgao_csv", ""))
    if has_kw:
        return "com_keyword"
    if area != DEFAULT_AREA:
        return "sem_keyword_macroarea_nomeada"
    return "sem_keyword_admin"


def _leakage_stats(records: list[dict]) -> dict:
    labeled = [
        r
        for r in records
        if setor_for_objeto(r.get("objeto_html") or r.get("objeto_compra") or "")
    ]
    n = len(labeled)
    oracle = 0
    for r in labeled:
        raw = r.get("objeto_html") or r.get("objeto_compra") or ""
        limpo = get_text_for_field(r, "objeto_html_limpo")
        if setor_for_objeto(raw) == setor_for_objeto(limpo):
            oracle += 1
    return {
        "n_rotulavel_keyword": n,
        "oracle_match_limpo_pct": round(100 * oracle / n, 1) if n else 0.0,
        "sem_vazamento_pct": round(100 * (n - oracle) / n, 1) if n else 0.0,
    }


def _eval_org_on_escondidas(
    records: list[dict],
    escondidas: list[dict],
    seed: int,
) -> dict:
    """Treina LogReg (label órgão) no restante; testa nas compras escondidas."""
    named_areas = [a for a in records if area_for_orgao(a.get("orgao_csv", "")) != DEFAULT_AREA]
    train_pool = [r for r in named_areas if r not in escondidas]
    if len(escondidas) < 10 or len(train_pool) < 50:
        return {"status": "skipped", "reason": "amostra insuficiente"}

    def xy(rows: list[dict]) -> tuple[list[str], list[str]]:
        texts = [get_text_for_field(r, "objeto_html_limpo") for r in rows]
        labels = [area_for_orgao(r.get("orgao_csv", "")) for r in rows]
        return texts, labels

    labels_all = [area_for_orgao(r.get("orgao_csv", "")) for r in train_pool]
    label_set = sorted(set(labels_all))
    train, val = train_test_split(
        train_pool,
        test_size=0.15,
        stratify=labels_all,
        random_state=seed,
    )
    x_train, y_train = xy(train)
    x_val, y_val = xy(val)
    x_test, y_test = xy(escondidas)

    model = build_baseline(class_weight="balanced", seed=seed)
    model.fit(x_train, y_train)
    val_pred = list(model.predict(x_val))
    test_pred = list(model.predict(x_test))

    val_m = compute_metrics(y_val, val_pred, label_set)
    test_m = compute_metrics(y_test, test_pred, label_set)
    return {
        "status": "ok",
        "n_train": len(train),
        "n_val": len(val),
        "n_test_escondidas": len(escondidas),
        "labels": label_set,
        "metrics_val": {
            "f1_macro": val_m["f1_macro"],
            "accuracy": val_m["accuracy"],
        },
        "metrics_test_escondidas": {
            "f1_macro": test_m["f1_macro"],
            "accuracy": test_m["accuracy"],
            "per_class": test_m["per_class"],
        },
    }


def _eval_indeterminado_detection(records: list[dict], seed: int) -> dict:
    """Binário: tem keyword setorial no objeto (rotulado pelo raw)."""
    texts = [get_text_for_field(r, "objeto_html_limpo") for r in records]
    y_true = [
        setor_for_objeto(r.get("objeto_html") or r.get("objeto_compra") or "") is not None
        for r in records
    ]
    pos = sum(y_true)
    train_idx, test_idx = train_test_split(
        list(range(len(records))),
        test_size=0.15,
        stratify=y_true,
        random_state=seed,
    )
    x_train = [texts[i] for i in train_idx]
    y_train = [y_true[i] for i in train_idx]
    x_test = [texts[i] for i in test_idx]
    y_test = [y_true[i] for i in test_idx]

    model = build_baseline(class_weight="balanced", seed=seed)
    model.fit(x_train, [str(y) for y in y_train])
    y_pred = [p.lower() == "true" for p in model.predict(x_test)]
    return {
        "n_total": len(records),
        "n_com_keyword": pos,
        "n_sem_keyword": len(records) - pos,
        "test_accuracy": round(accuracy_score(y_test, y_pred), 4),
        "test_f1_positivo": round(
            f1_score(y_test, y_pred, pos_label=True, zero_division=0), 4
        ),
    }


def run_benchmark(corpus_path: Path, output_path: Path, seed: int = 42) -> dict:
    records = _load_corpus(corpus_path)
    cohorts: dict[str, list[dict]] = {
        "com_keyword": [],
        "sem_keyword_admin": [],
        "sem_keyword_macroarea_nomeada": [],
    }
    for r in records:
        cohorts[_cohort(r)].append(r)

    escondidas = cohorts["sem_keyword_macroarea_nomeada"]
    area_dist = Counter(area_for_orgao(r.get("orgao_csv", "")) for r in escondidas)

    setor_dist = Counter(r["area"] for r in load_records_with_indeterminado(records))

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "corpus": str(corpus_path.relative_to(ROOT)).replace("\\", "/"),
        "n_total": len(records),
        "cohorts": {
            name: {
                "n": len(rows),
                "pct": round(100 * len(rows) / len(records), 1),
            }
            for name, rows in cohorts.items()
        },
        "escondidas_por_macroarea_orgao": dict(area_dist.most_common()),
        "distribuicao_10_classes": dict(setor_dist.most_common()),
        "leakage": _leakage_stats(records),
        "eval_org_logreg_escondidas": _eval_org_on_escondidas(records, escondidas, seed),
        "eval_detecao_sinal_binario": _eval_indeterminado_detection(records, seed),
        "tratamentos_sugeridos": [
            {
                "id": "pncp9_filter",
                "descricao": "Excluir sem keyword (atual pncp9)",
                "n_treino": len(cohorts["com_keyword"]),
            },
            {
                "id": "pncp9full_indeterminado",
                "descricao": "10 classes com Indeterminado",
                "n_treino": len(records),
                "n_indeterminado": len(cohorts["sem_keyword_admin"])
                + len(cohorts["sem_keyword_macroarea_nomeada"]),
            },
            {
                "id": "benchmark_escondidas",
                "descricao": "Gold proxy = macroárea órgão nas ~853 escondidas",
                "n": len(escondidas),
            },
        ],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return report


def load_records_with_indeterminado(records: list[dict]) -> list[dict]:
    out = []
    for rec in records:
        objeto = rec.get("objeto_html") or rec.get("objeto_compra") or ""
        area = setor_label_for_objeto(objeto, unlabeled=SETOR_INDETERMINADO)
        row = dict(rec)
        row["area"] = area
        out.append(row)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark casos difíceis PNCP.")
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if not args.corpus.exists():
        raise SystemExit(f"Corpus não encontrado: {args.corpus}")

    report = run_benchmark(args.corpus, args.output, seed=args.seed)
    print(f"Benchmark salvo em: {args.output}")
    print(f"  Total: {report['n_total']:,}")
    for name, info in report["cohorts"].items():
        print(f"  {name}: {info['n']:,} ({info['pct']}%)")
    leak = report["leakage"]
    print(f"  Vazamento oraculo (com keyword): {leak['oracle_match_limpo_pct']}%")
    ev = report["eval_org_logreg_escondidas"]
    if ev.get("status") == "ok":
        m = ev["metrics_test_escondidas"]
        print(
            f"  LogReg orgao -> escondidas: F1 macro={m['f1_macro']:.3f} "
            f"acc={m['accuracy']:.3f} (n={ev['n_test_escondidas']})"
        )
    det = report["eval_detecao_sinal_binario"]
    print(
        f"  Detecao sinal (binario): acc={det['test_accuracy']:.3f} "
        f"F1+={det['test_f1_positivo']:.3f}"
    )


if __name__ == "__main__":
    main()
