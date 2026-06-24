"""Gera notebooks/01_eda.ipynb — EDA e exploração (sem treino de modelos).

Coleta e preprocess: scripts/run_collect.py e scripts/run_preprocess.py.
Treino: scripts/run_train.py.

Rode: python notebooks/_build_eda.py
"""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf

NB_PATH = Path(__file__).resolve().parent / "01_eda.ipynb"


def md(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_markdown_cell(text.strip("\n"))


def code(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_code_cell(text.strip("\n"))


cells = [
    md(
        """
# EDA — Corpus de licitações ComprasNet DF 2025

**Responsabilidade deste notebook:** explorar dados já processados — **não** coletar HTML,
**não** treinar modelos.

| Etapa | Onde fica |
|-------|-----------|
| Coleta HTML | `python scripts/run_collect.py` |
| Pré-processamento → JSONL | `python scripts/run_preprocess.py` |
| Treino (baseline / SVM / BERT) | `python scripts/run_train.py` |
| Demo / apresentação | `notebooks/02_demo_apresentacao.ipynb` |

Corpus: `data/processed/licitacoes_corpus.jsonl` (423 editais quando coleta + preprocess completos).

Objetivos: distribuição das **macroáreas**, modalidade/tipo, **tamanho dos textos**,
**valor homologado** por área e **vazamento de label** (guia §6.1, `docs/vazamento_de_label.md`).
"""
    ),
    code(
        """
import json
import sys
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path.cwd()
if not (ROOT / "src").exists() and (ROOT.parent / "src").exists():
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))

from src.preprocess.labels import AREAS, AREA_KEYWORDS, area_for_orgao, normalize

CORPUS = ROOT / "data" / "processed" / "licitacoes_corpus.jsonl"
FIGURES = ROOT / "reports" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

if not CORPUS.is_file():
    raise FileNotFoundError(
        f"Corpus não encontrado: {CORPUS}\\n"
        "Rode: python scripts/run_collect.py && python scripts/run_preprocess.py"
    )

records = []
with CORPUS.open(encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            r = json.loads(line)
            r["area"] = area_for_orgao(r.get("orgao_csv", ""))
            records.append(r)

print(f"{len(records)} editais carregados")
print("Campos:", list(records[0].keys()))
"""
    ),
    md(
        """
## 1. Distribuição das macroáreas (label)

Label derivado de `orgao_csv` por palavras-chave — `src/preprocess/labels.py`.
"""
    ),
    code(
        """
area_counts = Counter(r["area"] for r in records)
ordered = [(a, area_counts.get(a, 0)) for a in AREAS]
for a, n in ordered:
    print(f"{n:4d}  {a}")

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar([a for a, _ in ordered], [n for _, n in ordered], color="#4C72B0")
ax.set_ylabel("nº de editais")
ax.set_title("Distribuição de editais por macroárea")
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
for i, (_, n) in enumerate(ordered):
    ax.text(i, n + 1, str(n), ha="center", fontsize=9)
fig.tight_layout()
fig.savefig(FIGURES / "eda_areas.png", dpi=120)
plt.show()
"""
    ),
    md(
        """
> **Desbalanceamento:** Administração/Outros e Saúde dominam; Educação e Infraestrutura
> são minoritárias — reportar F1 por classe e usar `class_weight='balanced'`.
"""
    ),
    md("## 2. Modalidade e tipo de contratação"),
    code(
        """
for campo in ("modalidade", "tipo"):
    print(f"--- {campo} ---")
    for valor, n in Counter(r.get(campo, "") for r in records).most_common():
        print(f"  {n:4d}  {valor}")
    print()
"""
    ),
    md("## 3. Tamanho dos textos (em palavras)"),
    code(
        """
word_counts = [len((r.get("texto") or "").split()) for r in records]
word_counts_sorted = sorted(word_counts)
n = len(word_counts_sorted)
mediana = word_counts_sorted[n // 2]
print(f"min={min(word_counts)}  mediana={mediana}  max={max(word_counts)}")
print(
    f"acima de 512 palavras: {sum(1 for w in word_counts if w > 512)} editais "
    "(truncamento BERT = 512 tokens)"
)

fig, ax = plt.subplots(figsize=(8, 4))
ax.hist([min(w, 2000) for w in word_counts], bins=40, color="#55A868")
ax.set_xlabel("nº de palavras (truncado em 2000)")
ax.set_ylabel("nº de editais")
ax.set_title("Distribuição do tamanho dos editais")
fig.tight_layout()
fig.savefig(FIGURES / "eda_tamanho_texto.png", dpi=120)
plt.show()
"""
    ),
    md("## 4. Valor homologado por área"),
    code(
        """
def parse_valor(v: str) -> float | None:
    if not v:
        return None
    s = str(v).replace("R$", "").strip().replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None

por_area = {a: [] for a in AREAS}
for r in records:
    val = parse_valor(r.get("total_homologado"))
    if val is not None and val > 0:
        por_area[r["area"]].append(val)

print(f"{'área':<24}{'n c/ valor':>10}{'soma (R$)':>18}{'mediana (R$)':>16}")
for a in AREAS:
    vals = sorted(por_area[a])
    if vals:
        soma = sum(vals)
        med = vals[len(vals) // 2]
        print(f"{a:<24}{len(vals):>10}{soma:>18,.0f}{med:>16,.0f}")
    else:
        print(f"{a:<24}{0:>10}{'-':>18}{'-':>16}")

somas = [sum(por_area[a]) for a in AREAS]
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(AREAS, somas, color="#C44E52")
ax.set_ylabel("soma do valor homologado (R$)")
ax.set_title("Gasto homologado total por macroárea")
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
fig.tight_layout()
fig.savefig(FIGURES / "eda_valor_por_area.png", dpi=120)
plt.show()
"""
    ),
    md(
        """
## 5. Vazamento de label — palavras-chave da área no texto

Se a **palavra-chave do órgão/área** aparece no texto de entrada, o classificador pode
"colar" no label. Comparamos `texto` (HTML completo) vs `objeto_html` (entrada oficial).
"""
    ),
    code(
        """
kw_by_area = dict(AREA_KEYWORDS)

def contem_keyword(texto: str, area: str) -> bool:
    kws = kw_by_area.get(area)
    if not kws:
        return False
    alvo = normalize(texto)
    return any(kw in alvo for kw in kws)

com_kw = [r for r in records if r["area"] in kw_by_area]
vaz_texto = sum(contem_keyword(r.get("texto", ""), r["area"]) for r in com_kw)
vaz_obj = sum(contem_keyword(r.get("objeto_html", ""), r["area"]) for r in com_kw)
base = len(com_kw)
print(f"Editais de áreas com palavra-chave: {base}")
print(f"  keyword da área em 'texto'      : {vaz_texto}/{base} ({vaz_texto/base:.0%})")
print(f"  keyword da área em 'objeto_html'  : {vaz_obj}/{base} ({vaz_obj/base:.0%})")
print("\\n→ Entrada oficial da classificação: objeto_html (ver docs/vazamento_de_label.md)")
"""
    ),
    md(
        """
## 6. Vazamento residual — nome do órgão em `objeto_html`

Auditoria complementar: o **nome normalizado do órgão** ainda aparece no campo de classificação?
"""
    ),
    code(
        """
def orgao_aparece_no_texto(orgao: str, texto: str) -> bool:
    org = normalize(orgao or "")
    if len(org) < 8:
        return False
    return org in normalize(texto or "")

residual = [r for r in records if orgao_aparece_no_texto(r.get("orgao_csv", ""), r.get("objeto_html", ""))]
print(f"Registros com nome do órgão em objeto_html: {len(residual)}/{len(records)}")
if residual:
    print("\\nExemplos (até 5):")
    for r in residual[:5]:
        print(f"  {r.get('numero_licitacao')} | {r.get('orgao_csv', '')[:50]}")
"""
    ),
    md(
        """
## Conclusões da EDA

- **Desbalanceamento** entre macroáreas → F1 macro + F1 por classe no relatório.
- Muitos editais **> 512 palavras** → truncamento do BERTimbau.
- **Gasto** concentrado em Saúde/Saneamento — insight para slides.
- **Vazamento:** `texto` >> `objeto_html`; auditoria residual quantifica órgão no objeto.
- Próximo passo: treinar em `scripts/run_train.py` — **não neste notebook**.
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
