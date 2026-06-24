# Notebook de entrega — baseline + PTT5

Documento que explica o papel do notebook integrado de apresentação e como ele se relaciona com o **pipeline oficial** em `scripts/`.

## Arquivo

| Notebook | Conteúdo |
|---|---|
| [`notebooks/projeto_final_pln_macroareas_tfidf_svm_ptt5_anti_vazamento2.ipynb`](../notebooks/projeto_final_pln_macroareas_tfidf_svm_ptt5_anti_vazamento2.ipynb) | **Baseline TF-IDF + LogReg** (Fase 1) + sumarização PTT5 (Fase 3) |

## Papel do notebook

Este notebook é a **trilha integrada para apresentação** (Colab/Jupyter): classificação + sumarização no mesmo fluxo. A classificação usa **o mesmo padrão** do restante do repositório — não é um experimento paralelo com SVM ou split diferente.

| Componente | Padrão do projeto |
|---|---|
| Corpus | `data/processed/licitacoes_corpus.jsonl` (423 editais) |
| Campo de texto | `objeto_html` |
| Labels | `src/preprocess/labels.py` |
| Modelo | TF-IDF + LogReg (`src/models/baseline_tfidf.py`) |
| Split | 70 / 15 / 15, `seed=42` |
| Métrica de referência | F1 macro teste ≈ **0,74** (run `classification_baseline_20260608-190839`) |

Comparação com BERTimbau (Fase 2): [`FASE2-CLASSIFICACAO.md`](FASE2-CLASSIFICACAO.md).

## O que o notebook faz

1. Exploração e auditoria anti-vazamento (seções iniciais — didático).
2. **Classificação oficial:** carrega o JSONL e treina via `make_dataset` + `build_baseline`.
3. **Sumarização (Fase 3):** protótipo PTT5 (`RUN_PTT5_SUMMARIZATION`).

## Sumarização

| Trilha | Onde |
|---|---|
| Extrativo (oficial) | `scripts/run_train.py --task summarization --model extractive` |
| Abstrativo (protótipo) | PTT5 neste notebook |

## Como executar

```bash
cd deep-learning-pln-project
source .venv/Scripts/activate
pip install -r requirements-dev.txt
jupyter notebook notebooks/projeto_final_pln_macroareas_tfidf_svm_ptt5_anti_vazamento2.ipynb
```

Para PTT5: `pip install -e ".[bert]"` e `RUN_PTT5_SUMMARIZATION = True`.

## Outros notebooks

| Notebook | Papel |
|---|---|
| [`notebooks/01_eda.ipynb`](../notebooks/01_eda.ipynb) | EDA oficial — vazamento quantificado (Tabela 7) |
