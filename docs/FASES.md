# Índice de fases do projeto

| Fase | Tarefa | Modelo | F1 macro (teste) | Doc |
|------|--------|--------|------------------|-----|
| **1** | Classificação | TF-IDF + **LogReg** | **0,740** | [`FASE1-CLASSIFICACAO.md`](FASE1-CLASSIFICACAO.md) |
| 2 | Classificação | BERTimbau | 0,400 | [`FASE2-CLASSIFICACAO.md`](FASE2-CLASSIFICACAO.md) |
| 3 | Classificação | TF-IDF + SVM | 0,652 | [`FASE3-CLASSIFICACAO.md`](FASE3-CLASSIFICACAO.md) |
| 4 | Sumarização cidadã | Extrativo | cobertura 15/18 prazo | [`FASE4-SUMARIZACAO.md`](FASE4-SUMARIZACAO.md) |

**Modelo principal do relatório:** Fase 1 (LogReg) — mesmo protocolo, melhor generalização no teste.

**Comparativo val × teste (por que melhorou/piorou):** [`COMPARATIVO-FASES.md`](COMPARATIVO-FASES.md) · [`METRICAS-E-DECISOES.md`](METRICAS-E-DECISOES.md)

**Runs oficiais:** `experiments/classification_*_20260624-013*.json` · [`experiments/README.md`](../experiments/README.md)

Notebooks: [`notebooks/README.md`](../notebooks/README.md) · Demo: `02_demo_classificacao.ipynb`
