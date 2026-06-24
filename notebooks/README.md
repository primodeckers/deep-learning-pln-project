# Notebooks — responsabilidades

**Regra:** notebooks **não treinam**. Treino = `scripts/run_train.py` + docs `FASE*-*.md`.

## Mapa de fases (classificação vs sumarização)

| Fase | Tarefa | Treino | Documento |
|------|--------|--------|-----------|
| 1 | TF-IDF + LogReg | `make train-baseline` | [`FASE1-CLASSIFICACAO.md`](../docs/FASE1-CLASSIFICACAO.md) |
| 2 | BERTimbau | `make train-bert` | [`FASE2-CLASSIFICACAO.md`](../docs/FASE2-CLASSIFICACAO.md) |
| 3 | TF-IDF + SVM | `make train-svm` | [`FASE3-CLASSIFICACAO.md`](../docs/FASE3-CLASSIFICACAO.md) |
| 4 | Sumarização cidadã | `make train-summarize` | [`FASE4-SUMARIZACAO.md`](../docs/FASE4-SUMARIZACAO.md) |

Fases 1–3 = **mesmo protocolo** (423 editais, `objeto_html`, split 70/15/15). Fase 4 = **outra tarefa**.

## Notebooks

| Notebook | Faz | Não faz |
|----------|-----|---------|
| [`01_eda.ipynb`](01_eda.ipynb) | EDA, tabelas estilizadas, vazamento | coleta, treino |
| [`02_demo_classificacao.ipynb`](02_demo_classificacao.ipynb) | Lê JSON das Fases 1–3, matrizes | treino, sumarização |

Regenerar demo: `python notebooks/_build_demo_classificacao.py`

`01_eda.ipynb` é editado diretamente (estilizado). `_build_eda.py` não sobrescreve sem `--force`.
