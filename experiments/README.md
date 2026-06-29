# Experimentos — o que versionar

JSONs e figuras **oficiais** do grupo ficam aqui no Git. Runs locais de teste podem ser apagados.

## Runs de referência (relatório / slides)

Retreino completo **2026-06-24** — mesmo `seed=42`, `objeto_html`, corpus `sha256=46c6e761…`.

| Arquivo | Modelo | F1 macro (teste) | Papel |
|---------|--------|------------------|--------|
| `classification_baseline_20260624-013836.json` | TF-IDF + LogReg | **0,740** | **Fase 1 — modelo principal** |
| `classification_svm_20260624-013851.json` | TF-IDF + SVM | **0,652** | **Fase 3** — comparativo clássico |
| `classification_bertimbau_20260624-013908.json` | BERTimbau (GPU) | **0,400** | **Fase 2** — comparativo DL |
| `summarization_extractive_20260624-013951.json` | Extrativo | 15/18 prazo · 18/18 valor | **Fase 4** |

Matrizes: `reports/figures/<run_id>_confusion.png`

**Decisão:** LogReg vence no F1 macro teste → modelo principal do relatório. Ver [`docs/METRICAS-E-DECISOES.md`](../docs/METRICAS-E-DECISOES.md).

Documentação: [`FASE1`](../docs/FASE1-CLASSIFICACAO.md) · [`FASE2`](../docs/FASE2-CLASSIFICACAO.md) · [`FASE3`](../docs/FASE3-CLASSIFICACAO.md) · [`FASE4`](../docs/FASE4-SUMARIZACAO.md)

### Runs históricos (não usar como referência)

| Arquivo | Nota |
|---------|------|
| `classification_baseline_20260608-190839.json` | Mesmas métricas que `013836` (determinístico) |
| `classification_bertimbau_20260623-222508.json` | F1 teste 0,518 — run GPU anterior |
| `classification_svm_20260624-004348.json` | Mesmas métricas que `013851` |
| `20260618-*`, `20260619-*` | Testes locais |

## Ignorado pelo Git

- `mlflow.db`, `mlartifacts/`, `mlruns/`, `.bert_cache/`
- `models/*` (checkpoints `.joblib` e pastas BERT ~416 MB)

MLflow: `make mlflow-ui` (Windows: `--workers 1`). Fluxo GPU: [`docs/GPU-EQUIPE.md`](../docs/GPU-EQUIPE.md)
