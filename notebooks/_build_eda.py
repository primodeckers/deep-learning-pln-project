"""Gera notebooks/01_eda.ipynb a partir de células declaradas aqui.

Manter o notebook em código (e não JSON solto) facilita revisão e regeneração.
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

Análise exploratória do corpus `data/processed/licitacoes_corpus.jsonl` (423 editais).
Objetivos: entender a distribuição das **macroáreas** (label da classificação), de
modalidade/tipo, o **tamanho dos textos**, o **valor homologado** por área e checar o
**vazamento de label** discutido no guia (§6.1).
"""
    ),
    code(
        """
import json
import sys
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt

# Permite importar src.* ao rodar o notebook de dentro de notebooks/.
ROOT = Path.cwd()
if (ROOT / "src").exists():
    pass
elif (ROOT.parent / "src").exists():
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))

from src.preprocess.labels import AREAS, area_for_orgao, normalize

CORPUS = ROOT / "data" / "processed" / "licitacoes_corpus.jsonl"
FIGURES = ROOT / "reports" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

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

O label é derivado do órgão (`orgao_csv`) por palavras-chave — ver `src/preprocess/labels.py`.
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
> Classes muito **desbalanceadas**: Administração/Outros e Saúde dominam; Educação (17) e
> Infraestrutura (24) são minoritárias — esperar F1 instável nelas (documentar na discussão).
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
print(f"acima de 512 palavras: {sum(1 for w in word_counts if w > 512)} editais "
      f"(relevante para o truncamento do BERT em 512 tokens)")

fig, ax = plt.subplots(figsize=(8, 4))
ax.hist([min(w, 2000) for w in word_counts], bins=40, color="#55A868")
ax.set_xlabel("nº de palavras (truncado em 2000 para visualização)")
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
    \"\"\"Converte 'R$ 1.234,56' (formato BR) para float; None se não numérico.\"\"\"
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
## 5. Vazamento de label: o órgão aparece no texto?

O label vem do órgão. Se o **nome do órgão** estiver dentro do `texto`, o classificador
pode "colar" em vez de aprender o conteúdo. Medimos quantos editais contêm uma das
palavras-chave da sua própria área no `texto` vs no `objeto_html`.
"""
    ),
    code(
        """
from src.preprocess.labels import AREA_KEYWORDS

kw_by_area = dict(AREA_KEYWORDS)  # área -> tuple de palavras-chave

def contem_keyword(texto: str, area: str) -> bool:
    kws = kw_by_area.get(area)
    if not kws:
        return False  # Administração/Outros não tem palavra-chave própria
    alvo = normalize(texto)
    return any(kw in alvo for kw in kws)

com_kw = [r for r in records if r["area"] in kw_by_area]
vaz_texto = sum(contem_keyword(r.get("texto", ""), r["area"]) for r in com_kw)
vaz_obj = sum(contem_keyword(r.get("objeto_html", ""), r["area"]) for r in com_kw)
base = len(com_kw)
print(f"Editais de áreas com palavra-chave: {base}")
print(f"  palavra-chave da área aparece em 'texto'      : {vaz_texto}/{base} ({vaz_texto/base:.0%})")
print(f"  palavra-chave da área aparece em 'objeto_html': {vaz_obj}/{base} ({vaz_obj/base:.0%})")
print()
print("→ Por isso usamos objeto_html como entrada honesta (ver guia §6.1).")
"""
    ),
    md(
        """
## Conclusões da EDA

- **Desbalanceamento forte** entre macroáreas → usar `class_weight`, reportar F1 por classe.
- Boa parte dos editais passa de **512 palavras** → BERTimbau truncará; considerar isso.
- O **gasto** concentra-se em poucas áreas (Saúde/Saneamento) — insight para a apresentação.
- **Vazamento confirmado**: o órgão aparece no `texto` com frequência muito maior que no
  `objeto_html`, justificando a escolha de entrada da classificação.
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
