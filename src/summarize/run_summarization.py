"""Gera resumos cidadãos para uma amostra estratificada de editais (guia §7).

Produz três saídas:
  - JSONL com todos os resumos da amostra (data/processed/resumos_*.jsonl)
  - Markdown "antes/depois" para os slides (reports/slides/resumos_exemplos.md)
  - Registro de experimento (experiments/summarization_*.json)
"""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from src.preprocess.dataset import load_records
from src.preprocess.labels import AREAS
from src.summarize.extractive import summarize_record
from src.utils.experiment_tracking import (
    corpus_fingerprint,
    git_commit_short,
    mlflow_run,
)

# Raiz do repositório, para gravar caminhos relativos (portáveis entre máquinas).
ROOT = Path(__file__).resolve().parents[2]


def _rel(path: Path) -> str:
    """Caminho relativo à raiz do repo, em formato POSIX (estável no Git)."""
    try:
        return Path(path).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def stratified_sample(records: list[dict], n: int, seed: int = 42) -> list[dict]:
    """Amostra ~n editais distribuídos pelas macroáreas (determinístico)."""
    por_area: dict[str, list[dict]] = defaultdict(list)
    for r in records:
        por_area[r["area"]].append(r)

    # Ordena cada área por id para reprodutibilidade sem depender de random.
    for area in por_area:
        por_area[area].sort(key=lambda r: r["id"])

    por_area_count = max(1, n // len(AREAS))
    amostra: list[dict] = []
    for area in AREAS:
        amostra.extend(por_area.get(area, [])[:por_area_count])
    return amostra[:n]


def _build_markdown(resumos: list[dict], by_id: dict[str, dict]) -> str:
    linhas = [
        "# Resumos cidadãos — exemplos antes/depois",
        "",
        "Baseline **extrativo** (regras + regex). Cada bloco mostra o objeto",
        "original do edital e o resumo gerado. Determinístico: não inventa",
        "prazos nem valores.",
        "",
    ]
    for item in resumos:
        rec = by_id[item["id"]]
        linhas += [
            f"## {item['id']} — {rec['area']}",
            "",
            "**Antes (objeto original):**",
            "",
            f"> {(rec.get('objeto_html') or rec.get('objeto_csv') or '').strip()}",
            "",
            "**Depois (resumo cidadão):**",
            "",
            f"> {item['resumo']}",
            "",
            "---",
            "",
        ]
    return "\n".join(linhas)


def run_summarization(
    corpus_path: Path,
    processed_dir: Path,
    slides_dir: Path,
    experiments_dir: Path,
    sample_size: int = 20,
    seed: int = 42,
) -> dict:
    records = load_records(corpus_path)
    by_id = {r["id"]: r for r in records}

    amostra = stratified_sample(records, sample_size, seed=seed)
    resumos = [summarize_record(r) for r in amostra]

    # Cobertura dos campos (qualidade do extrator).
    cobertura = {
        "com_prazo": sum(1 for x in resumos if x["campos"]["prazo"]),
        "com_valor": sum(1 for x in resumos if x["campos"]["valor_homologado"]),
        "total": len(resumos),
    }

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_id = f"summarization_extractive_{timestamp}"
    dataset_info = corpus_fingerprint(corpus_path)
    git_commit = git_commit_short()

    processed_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = processed_dir / "resumos_extrativos.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as f:
        for item in resumos:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    slides_dir.mkdir(parents=True, exist_ok=True)
    md_path = slides_dir / "resumos_exemplos.md"
    md_path.write_text(_build_markdown(resumos, by_id), encoding="utf-8")

    experiments_dir.mkdir(parents=True, exist_ok=True)
    experiment = {
        "run_id": run_id,
        "task": "summarization",
        "model": "extractive",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "seed": seed,
        "dataset": dataset_info,
        "git_commit": git_commit,
        "sample_size": len(resumos),
        "coverage": cobertura,
        "sample_ids": [x["id"] for x in resumos],
        "artifacts": {"jsonl": _rel(jsonl_path), "exemplos_md": _rel(md_path)},
    }
    exp_path = experiments_dir / f"{run_id}.json"
    exp_path.write_text(
        json.dumps(experiment, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    mlflow_tags = {
        "corpus_sha256": dataset_info["sha256"],
        "corpus_path": dataset_info["path"],
        "corpus_n_records": str(dataset_info["n_records"]),
    }
    if git_commit:
        mlflow_tags["git_commit"] = git_commit

    with mlflow_run(
        experiments_dir=experiments_dir,
        run_name=run_id,
        task="summarization",
        model="extractive",
        params={"seed": seed, "sample_size": len(resumos)},
        metrics={
            "coverage_prazo": cobertura["com_prazo"] / max(cobertura["total"], 1),
            "coverage_valor": cobertura["com_valor"] / max(cobertura["total"], 1),
        },
        tags=mlflow_tags,
        artifacts=[jsonl_path, md_path, exp_path],
    ) as mlflow_run_id:
        if mlflow_run_id:
            experiment["mlflow_run_id"] = mlflow_run_id

    print(f"Amostra: {len(resumos)} editais")
    print(
        f"Cobertura — prazo: {cobertura['com_prazo']}/{cobertura['total']}  "
        f"valor: {cobertura['com_valor']}/{cobertura['total']}"
    )
    print(f"JSONL:      {jsonl_path}")
    print(f"Exemplos:   {md_path}")
    print(f"Experimento:{exp_path}")
    if experiment.get("mlflow_run_id"):
        print(f"MLflow run: {experiment['mlflow_run_id']}")
    return experiment
