"""Gera notebooks/02_demo_classificacao.ipynb — só classificação (Fases 1–3).

Lê experiments/*.json versionados. Não treina. Não inclui sumarização (Fase 4).

Rode: python notebooks/_build_demo_classificacao.py
"""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf

NB_PATH = Path(__file__).resolve().parent / "02_demo_classificacao.ipynb"


def md(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_markdown_cell(text.strip("\n"))


def code(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_code_cell(text.strip("\n"))


cells = [
    md(
        """
# Demo — Classificação (Fases 1, 2 e 3)

**Só leitura** dos resultados oficiais em `experiments/`. **Não treina modelos.**

| Fase | Modelo | Documento |
|------|--------|-----------|
| 1 | TF-IDF + LogReg | `docs/FASE1-CLASSIFICACAO.md` |
| 2 | BERTimbau | `docs/FASE2-CLASSIFICACAO.md` |
| 3 | TF-IDF + SVM | `docs/FASE3-CLASSIFICACAO.md` |

**Sumarização (Fase 4)** é outra tarefa → `docs/FASE4-SUMARIZACAO.md` e `make train-summarize`.

**Treinar:** `make train-baseline` · `make train-svm` · `make train-bert`
"""
    ),
    code(
        """
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path.cwd()
if not (ROOT / "src").exists() and (ROOT.parent / "src").exists():
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))

EXPERIMENTS = ROOT / "experiments"
FIGURES = ROOT / "reports" / "figures"

# Runs oficiais versionados no Git (mesmo protocolo: objeto_html, split 70/15/15)
REF_RUNS = {
    "Fase 1 — LogReg": "classification_baseline_20260608-190839",
    "Fase 3 — SVM": "classification_svm_20260624-004348",
    "Fase 2 — BERTimbau": "classification_bertimbau_20260623-222508",
}

print("Raiz:", ROOT)
"""
    ),
    md("## 1. Tabela comparativa (F1 macro — teste)"),
    code(
        """
def carregar_run(run_id: str) -> dict:
    path = EXPERIMENTS / f"{run_id}.json"
    if not path.is_file():
        raise FileNotFoundError(f"Run não encontrado: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


rows = []
for fase, run_id in REF_RUNS.items():
    exp = carregar_run(run_id)
    t = exp["metrics"]["test"]
    rows.append({
        "fase": fase,
        "modelo": exp["model"],
        "run_id": run_id,
        "f1_macro_teste": t["f1_macro"],
        "accuracy_teste": t["accuracy"],
    })

tabela = pd.DataFrame(rows).sort_values("f1_macro_teste", ascending=False)
display(tabela)

print("\\nModelo principal do relatório: Fase 1 (LogReg), F1 teste ≈ 0,74")
print("Documentação: docs/FASE1-CLASSIFICACAO.md · FASE2 · FASE3")
"""
    ),
    md("## 2. Matrizes de confusão (teste)"),
    code(
        """
for run_id in REF_RUNS.values():
    img = FIGURES / f"{run_id}_confusion.png"
    if img.is_file():
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.imshow(plt.imread(img))
        ax.axis("off")
        ax.set_title(run_id.replace("classification_", ""), fontsize=10)
        plt.show()
    else:
        print("Figura ausente:", img)
"""
    ),
    md(
        """
## 3. Nota sobre inferência local

Para classificar **um edital ao vivo** na apresentação, é preciso o `.joblib` em `models/` (gerado ao rodar `make train-baseline` na sua máquina — **não vai pro Git**).

As **métricas oficiais** deste notebook vêm só dos JSON em `experiments/` — não dependem de treino local.
"""
    ),
]

nb = nbf.v4.new_notebook()
nb.cells = cells
nb.metadata = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python"},
}
NB_PATH.write_text(nbf.writes(nb), encoding="utf-8")
print(f"Notebook escrito em {NB_PATH}")
