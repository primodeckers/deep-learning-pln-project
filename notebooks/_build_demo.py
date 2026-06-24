"""Gera notebooks/02_demo_apresentacao.ipynb — demo para slides (sem treino).

Carrega métricas de experiments/*.json e modelos já treinados (se existirem localmente).
Treino: make train-baseline / train-svm / train-bert.

Rode: python notebooks/_build_demo.py
"""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf

NB_PATH = Path(__file__).resolve().parent / "02_demo_apresentacao.ipynb"

# Runs oficiais versionados no Git
REF_RUNS = {
    "baseline": "classification_baseline_20260608-190839",
    "svm": "classification_svm_20260624-004348",
    "bertimbau": "classification_bertimbau_20260623-222508",
}


def md(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_markdown_cell(text.strip("\n"))


def code(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_code_cell(text.strip("\n"))


cells = [
    md(
        """
# Demo — Classificação + Sumarização Cidadã

**Responsabilidade deste notebook:** apresentação e inferência sobre artefatos já treinados.
**Não treina modelos** — use `scripts/run_train.py` ou `make train-*`.

| Tarefa | Pipeline oficial |
|--------|------------------|
| EDA / exploração | `notebooks/01_eda.ipynb` |
| Treino classificação | `make train-baseline` · `make train-svm` · `make train-bert` |
| Sumarização extrativa | `make train-summarize` |
| Este notebook | Comparar resultados + demo ao vivo |
"""
    ),
    code(
        """
import json
import sys
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path.cwd()
if not (ROOT / "src").exists() and (ROOT.parent / "src").exists():
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))

from src.preprocess.labels import AREAS

EXPERIMENTS = ROOT / "experiments"
FIGURES = ROOT / "reports" / "figures"
CORPUS = ROOT / "data" / "processed" / "licitacoes_corpus.jsonl"
MODELS = ROOT / "models"
SLIDES = ROOT / "reports" / "slides" / "resumos_exemplos.md"

REF_RUNS = {
    "baseline": "classification_baseline_20260608-190839",
    "svm": "classification_svm_20260624-004348",
    "bertimbau": "classification_bertimbau_20260623-222508",
}

RUN_PTT5_DEMO = False  # True = inferência PTT5 em 1 exemplo (pip install -e ".[bert]")
PTT5_MODEL = "recogna-nlp/ptt5-base-summ"

print("Raiz:", ROOT)
"""
    ),
    md("## 1. Resultados oficiais (experiments/*.json)"),
    code(
        """
def carregar_run(run_id: str) -> dict:
    path = EXPERIMENTS / f"{run_id}.json"
    if not path.is_file():
        raise FileNotFoundError(f"Run não encontrado: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


rows = []
for nome, run_id in REF_RUNS.items():
    exp = carregar_run(run_id)
    t = exp["metrics"]["test"]
    rows.append({
        "modelo": nome,
        "run_id": run_id,
        "f1_macro_teste": t["f1_macro"],
        "accuracy_teste": t["accuracy"],
    })

tabela = pd.DataFrame(rows).sort_values("f1_macro_teste", ascending=False)
display(tabela)

print("\\nMatrizes de confusão em reports/figures/<run_id>_confusion.png")
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
## 3. Inferência — classificar um edital (modelo baseline)

Carrega o `.joblib` do run oficial **se existir** em `models/` (não versionado no Git).
Se ausente, rode localmente: `make train-baseline`.
"""
    ),
    code(
        """
import json as _json

# Carrega 1 edital de exemplo do corpus
with CORPUS.open(encoding="utf-8") as f:
    exemplo = _json.loads(f.readline())

texto_entrada = exemplo.get("objeto_html") or exemplo.get("texto", "")
print("Licitação:", exemplo.get("numero_licitacao"))
print("Órgão (label proxy):", exemplo.get("orgao_csv"))
print("\\nTrecho objeto_html:")
print(texto_entrada[:600])

baseline_run = carregar_run(REF_RUNS["baseline"])
model_rel = baseline_run.get("artifacts", {}).get("model", "")
model_path = ROOT / model_rel if model_rel else None

# Fallback: qualquer joblib baseline local
if model_path is None or not model_path.is_file():
    candidatos = sorted(MODELS.glob("classification_baseline_*.joblib"))
    model_path = candidatos[-1] if candidatos else None

if model_path and model_path.is_file():
    clf = joblib.load(model_path)
    pred = clf.predict([texto_entrada])[0]
    if hasattr(clf, "predict_proba"):
        prob = clf.predict_proba([texto_entrada])[0]
        conf = float(prob.max())
    else:
        conf = None
    print(f"\\nMacroárea predita (baseline): {pred}")
    if conf is not None:
        print(f"Confiança: {conf:.2%}")
else:
    print("\\nModelo local não encontrado. Rode: make train-baseline")
"""
    ),
    md("## 4. Sumarização extrativa (baseline oficial)"),
    code(
        """
if SLIDES.is_file():
    print(SLIDES.read_text(encoding="utf-8")[:3000])
    print("\\n[... arquivo completo em reports/slides/resumos_exemplos.md]")
else:
    print("Rode: make train-summarize")
    print("Saída esperada:", SLIDES)
"""
    ),
    md(
        """
## 5. Sumarização abstrativa — demo PTT5 (opcional)

Protótipo Fase 3. **Inferência apenas** — não fine-tune aqui.
Defina `RUN_PTT5_DEMO = True` na célula de configuração.
"""
    ),
    code(
        """
if RUN_PTT5_DEMO:
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(PTT5_MODEL)
    model = AutoModelForSeq2SeqLM.from_pretrained(PTT5_MODEL).to(device)

    texto_demo = (exemplo.get("objeto_html") or "")[:4000]
    inputs = tokenizer(texto_demo, return_tensors="pt", truncation=True, max_length=512).to(device)
    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=90, num_beams=4)
    resumo = tokenizer.decode(out[0], skip_special_tokens=True)
    print("Resumo PTT5:")
    print(resumo)
else:
    print("RUN_PTT5_DEMO=False — pulando PTT5. Ative para demo ao vivo.")
"""
    ),
    md(
        """
## 6. Produto integrado (narrativa para slides)

> **Edital** → **macroárea predita** (classificação) + **resumo cidadã** (sumarização)

Limitações: label proxy (órgão), corpus pequeno, PTT5 pode alucinar prazo/valor —
sempre linkar o edital oficial.

Documentação: `docs/FASE1-CLASSIFICACAO.md`, `docs/FASE2-CLASSIFICACAO.md`, `docs/model_card.md`.
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
