# Notebooks — responsabilidades

**Regra:** notebooks **não treinam**. Treino = `scripts/run_train.py` + docs `FASE*-*.md`.

## Mapa de fases (classificação)

| Fase | Tarefa | Treino | Documento |
|------|--------|--------|-----------|
| 1 | TF-IDF + LogReg | `make train-baseline` | [`FASE1-CLASSIFICACAO.md`](../docs/FASE1-CLASSIFICACAO.md) |
| 2 | BERTimbau | `make train-bert` | [`FASE2-CLASSIFICACAO.md`](../docs/FASE2-CLASSIFICACAO.md) |
| 3 | TF-IDF + SVM | `make train-svm` | [`FASE3-CLASSIFICACAO.md`](../docs/FASE3-CLASSIFICACAO.md) |

Fases 1–3 = **mesmo protocolo** (423 editais, `objeto_html`, split 70/15/15).

## Notebooks

| Notebook | Faz | Não faz |
|----------|-----|---------|
| [`01_eda.ipynb`](01_eda.ipynb) | EDA corpus ComprasNet DF, vazamento de label | coleta, treino |
| [`03_eda_pncp.ipynb`](03_eda_pncp.ipynb) | EDA PNCP **DF/2025** (~20k compras) — espelha análises do 01 | coleta, treino, corpus ComprasNet |
| [`02_demo_classificacao.ipynb`](02_demo_classificacao.ipynb) | Lê JSON das Fases 1–3, matrizes | treino |

Regenerar demo: `python notebooks/_build_demo_classificacao.py`

`01_eda.ipynb` e `03_eda_pncp.ipynb` são editados **diretamente** no Cursor. `_build_eda.py` não sobrescreve `01_eda` sem `--force`.
