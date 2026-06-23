# Experimentos — o que versionar

JSONs e figuras **oficiais** do grupo ficam aqui no Git. Runs locais de teste podem ser apagados.

## Runs de referência (relatório / slides)

| Arquivo | Modelo | F1 macro (teste) |
|---------|--------|------------------|
| `classification_baseline_20260608-190839.json` | TF-IDF + LogReg | ≈ 0,74 |
| `classification_bertimbau_20260623-213337.json` | BERTimbau (1º run) | ≈ 0,40 |

Matrizes: `reports/figures/<run_id>_confusion.png`

## Ignorado pelo Git

- `mlflow.db`, `mlartifacts/`, `mlruns/`, `.bert_cache/`
- JSONs de testes locais não aprovados pelo grupo

Fluxo GPU vs CPU: [`docs/GPU-EQUIPE.md`](../docs/GPU-EQUIPE.md)
