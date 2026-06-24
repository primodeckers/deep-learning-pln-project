# Notebooks — responsabilidades

Cada notebook tem **um papel**. Treino e coleta ficam em `scripts/` e `src/`.

| Notebook | Responsabilidade | Não faz |
|----------|------------------|---------|
| [`01_eda.ipynb`](../notebooks/01_eda.ipynb) | EDA estilizado — exploração e vazamento (Tabelas 1–8) |
| [`02_demo_apresentacao.ipynb`](../notebooks/02_demo_apresentacao.ipynb) | Demo slides — métricas + inferência (sem treino) |

## Regenerar notebooks

Os `.ipynb` são gerados a partir de scripts Python (revisão em diff):

```bash
python notebooks/_build_eda.py
python notebooks/_build_demo.py
```

## Pipeline fora dos notebooks

```bash
python scripts/run_collect.py          # coleta
python scripts/run_preprocess.py       # JSONL
make train-baseline                    # TF-IDF + LogReg
make train-svm                         # TF-IDF + SVM
make train-bert                        # BERTimbau
make train-summarize                   # sumarização extrativa
```

Runs versionados: `experiments/classification_*.json` · ver [`experiments/README.md`](../experiments/README.md).
