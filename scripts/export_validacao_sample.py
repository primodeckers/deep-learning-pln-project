"""Atualiza amostra no gabarito e nas fichas individuais (Fase 1).

Saídas:
  - docs/validacao_labels/validacao_labels.md  — gabarito (amostra + consolidação)
  - docs/validacao_labels/ficha_*.md           — cópia por integrante

Uso:
    python scripts/export_validacao_sample.py

Atenção: regerar apaga respostas já preenchidas nas fichas.
"""

from __future__ import annotations

import random
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.preprocess.dataset import load_records
from src.preprocess.labels import AREAS

CORPUS = ROOT / "data" / "processed" / "licitacoes_corpus.jsonl"
GABARITO = ROOT / "docs" / "validacao_labels" / "validacao_labels.md"
FICHAS_DIR = ROOT / "docs" / "validacao_labels"
PER_AREA = 5
SEED = 42
MARKER_START = "<!-- AMOSTRA_INICIO -->"
MARKER_END = "<!-- AMOSTRA_FIM -->"


@dataclass(frozen=True)
class Revisor:
    slug: str
    nome: str


REVISORES: tuple[Revisor, ...] = (
    Revisor("elisangela", "Elisangela Osorio"),
    Revisor("alexandre", "Alexandre Ferreira Ponte"),
    Revisor("rene", "Renê Estevam Deckers"),
    Revisor("integrante4", "Integrante 4 (a definir)"),
)

TABLE_HEADER = (
    "| # | `id` | `orgao_csv` | Trecho do `objeto_html` | Label auto | "
    "Concorda? | Label humano | Observação |"
)
TABLE_SEPARATOR = (
    "|---|------|-------------|-------------------------|------------"
    "|-----------|--------------|------------|"
)


def _truncate(text: str, max_len: int = 120) -> str:
    text = (text or "").replace("\n", " ").strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 1] + "…"


def _escape_cell(text: str) -> str:
    return (text or "").replace("|", "/")


def sample_records(
    records: list[dict], per_area: int, seed: int, target_total: int = 30
) -> list[dict]:
    by_area: dict[str, list[dict]] = defaultdict(list)
    for rec in records:
        by_area[rec["area"]].append(rec)

    rng = random.Random(seed)
    picked: list[dict] = []
    picked_ids: set[str] = set()

    for area in AREAS:
        pool = by_area.get(area, [])
        if not pool:
            continue
        n = min(per_area, len(pool))
        for rec in rng.sample(pool, n):
            picked.append(rec)
            picked_ids.add(rec["id"])

    if len(picked) < target_total:
        remainder = [r for r in records if r["id"] not in picked_ids]
        extra = min(target_total - len(picked), len(remainder))
        if extra:
            picked.extend(rng.sample(remainder, extra))

    rng.shuffle(picked)
    return picked


TABLE_HEADER_GABARITO = (
    "| # | `id` | `orgao_csv` | Trecho do `objeto_html` | Label auto |"
)
TABLE_SEPARATOR_GABARITO = (
    "|---|------|-------------|-------------------------|------------|"
)


def render_table(rows: list[dict], *, include_review: bool = True) -> str:
    if include_review:
        header, sep = TABLE_HEADER, TABLE_SEPARATOR
    else:
        header, sep = TABLE_HEADER_GABARITO, TABLE_SEPARATOR_GABARITO
    lines = [header, sep]
    for i, rec in enumerate(rows, start=1):
        orgao = _escape_cell(rec.get("orgao_csv") or "")
        objeto = _escape_cell(_truncate(rec.get("objeto_html") or ""))
        review = " | | |" if include_review else ""
        lines.append(
            f"| {i} | `{rec['id']}` | {orgao} | {objeto} | "
            f"{rec['area']}{review} |"
        )
    return "\n".join(lines)


def patch_markers(doc_path: Path, inner: str) -> str:
    text = doc_path.read_text(encoding="utf-8")
    if MARKER_START not in text or MARKER_END not in text:
        raise SystemExit(f"Marcadores ausentes em {doc_path}")
    block = f"{MARKER_START}\n{inner}\n{MARKER_END}"
    pattern = re.compile(
        re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
        flags=re.DOTALL,
    )
    updated = pattern.sub(block, text, count=1)
    doc_path.write_text(updated, encoding="utf-8")
    return updated


def render_ficha_template(
    revisor: Revisor, rows: list[dict], n_rows: int, table: str
) -> str:
    """Gera ficha vazia a partir do gabarito (usado só ao regerar amostra)."""
    return f"""# Validação manual de labels — {revisor.nome}

Revisão humana da qualidade do **label proxy** (órgão → macroárea). Gabarito e instruções: [`validacao_labels.md`](validacao_labels.md).

> **Ficha individual.** Preencha **Concorda?**, **Label humano** e **Observação** na tabela abaixo.

---

## Registro

| Campo | Valor |
|-------|-------|
| **Revisor(a)** | {revisor.nome} |
| **Data** | _AAAA-MM-DD_ |
| **Corpus** | `data/processed/licitacoes_corpus.jsonl` |
| **Amostra** | {n_rows} editais · seed {SEED} |

---

## Tabela (sua revisão)

<!-- AMOSTRA_INICIO -->
> Amostra · seed={SEED} · {n_rows} editais

{table}

<!-- AMOSTRA_FIM -->

---

## Resumo (preencher após revisão)

| Métrica | Valor |
|---------|-------|
| Total revisado | /{n_rows} |
| Concordância (`S`) | |
| Discordância (`N`) | |
| Ambíguos (`?`) | |
| **Taxa de concordância** | _S / (S+N)_ |

### Conclusão (1 parágrafo)

_Espaço livre._

---

## Referências

- [`FASE1-CLASSIFICACAO.md`](../FASE1-CLASSIFICACAO.md) · [`metricas_e_decisoes.md`](../metricas_e_decisoes.md)
"""


def main() -> None:
    if not CORPUS.exists():
        raise SystemExit(
            f"Corpus não encontrado: {CORPUS}\n"
            "Rode: python scripts/run_preprocess.py"
        )
    if not GABARITO.exists():
        raise SystemExit(f"Gabarito não encontrado: {GABARITO}")

    records = load_records(CORPUS)
    rows = sample_records(records, PER_AREA, SEED)
    n = len(rows)
    table_gabarito = render_table(rows, include_review=False)
    table_ficha = render_table(rows, include_review=True)

    inner = (
        f"> Amostra fixa · seed={SEED} · {n} editais · "
        f"`export_validacao_sample.py`\n\n{table_gabarito}"
    )
    patch_markers(GABARITO, inner)
    print(f"Gabarito: {GABARITO} ({n} editais)")

    for revisor in REVISORES:
        if revisor.slug == "rene":
            print(f"  ficha: {FICHAS_DIR / f'ficha_{revisor.slug}.md'} (mantida — já preenchida)")
            continue
        path = FICHAS_DIR / f"ficha_{revisor.slug}.md"
        path.write_text(render_ficha_template(revisor, rows, n, table_ficha), encoding="utf-8")
        print(f"  ficha: {path} (regenerada)")


if __name__ == "__main__":
    main()
