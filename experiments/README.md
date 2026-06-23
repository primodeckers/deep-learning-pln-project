# Experimentos — o que versionar

JSONs e figuras **oficiais** do grupo ficam aqui no Git. Runs locais de teste podem ser apagados.

## Runs de referência (relatório / slides)

| Arquivo | Modelo | F1 macro (teste) | Papel |
|---------|--------|------------------|--------|
| `classification_baseline_20260608-190839.json` | TF-IDF + LogReg | **0,740** | **Modelo principal** |
| `classification_bertimbau_20260623-222508.json` | BERTimbau (GPU) | **0,518** | Comparativo DL (Fase 2) |

Matrizes: `reports/figures/<run_id>_confusion.png`

Documentação Fase 2: [`docs/FASE2-CLASSIFICACAO.md`](../docs/FASE2-CLASSIFICACAO.md) — textos prontos para relatório §4.

### Run histórico (não usar como referência)

| Arquivo | Nota |
|---------|------|
| `classification_bertimbau_20260623-213337.json` | 1º run (CPU), F1 teste 0,401 — substituído por `222508` |

## Ignorado pelo Git

- `mlflow.db`, `mlartifacts/`, `mlruns/`, `.bert_cache/`
- JSONs `20260618-*`, `20260619-*` (testes locais)

Fluxo GPU vs CPU: [`docs/GPU-EQUIPE.md`](../docs/GPU-EQUIPE.md)
