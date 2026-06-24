# Notebook de entrega — baseline + SVM + PTT5

Notebook integrado para apresentação (Colab/Jupyter): **dois classificadores clássicos** + sumarização.

## Arquivo

| Notebook | Conteúdo |
|---|---|
| [`notebooks/projeto_final_pln_baseline_svm_ptt5.ipynb`](../notebooks/projeto_final_pln_baseline_svm_ptt5.ipynb) | EDA/anti-vazamento · **LogReg + SVM** · PTT5 |

## Classificação — padrão do repositório

Ambos os modelos usam o **mesmo** corpus, split e campo de texto:

| Item | Valor |
|---|---|
| Corpus | `data/processed/licitacoes_corpus.jsonl` (423 editais) |
| Campo | `objeto_html` |
| Split | 70 / 15 / 15, `seed=42` |
| Labels | `src/preprocess/labels.py` |

| Modelo | Código | Treino | F1 macro (teste) |
|---|---|---|---|
| **Baseline (oficial)** | `baseline_tfidf.py` | `make train-baseline` | ≈ **0,74** |
| **SVM (comparativo)** | `svm_tfidf.py` | `make train-svm` | ≈ **0,65** (`classification_svm_20260624-004348`) |
| BERTimbau (Fase 2) | `bert_classifier.py` | `make train-bert` | ≈ 0,52 |

Runs versionados: `experiments/classification_*.json`

## Sumarização (Fase 3)

| Trilha | Onde |
|---|---|
| Extrativo | `make train-summarize` |
| PTT5 (protótipo) | Notebook (`RUN_PTT5_SUMMARIZATION`) |

## Como executar

```bash
cd deep-learning-pln-project
source .venv/Scripts/activate
pip install -r requirements-dev.txt
jupyter notebook notebooks/projeto_final_pln_baseline_svm_ptt5.ipynb
```

## Outros notebooks

| Notebook | Papel |
|---|---|
| [`notebooks/01_eda.ipynb`](../notebooks/01_eda.ipynb) | EDA oficial |
