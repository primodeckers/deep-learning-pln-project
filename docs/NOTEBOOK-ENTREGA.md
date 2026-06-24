# Notebook de entrega — TF-IDF + SVM + PTT5

Documento que explica o papel do notebook integrado de apresentação e como ele se relaciona com o **pipeline oficial** em `scripts/`.

## Arquivo

| Notebook | Conteúdo |
|---|---|
| [`notebooks/projeto_final_pln_macroareas_tfidf_svm_ptt5_anti_vazamento2.ipynb`](../notebooks/projeto_final_pln_macroareas_tfidf_svm_ptt5_anti_vazamento2.ipynb) | Classificação **TF-IDF + SVM**, auditoria anti-vazamento e sumarização abstrativa com **PTT5** |

## Duas trilhas no repositório

| Trilha | Onde | Para quê |
|---|---|---|
| **Oficial (métricas de referência)** | `scripts/run_train.py` + `configs/*.yaml` | Comparar baseline, BERTimbau e runs versionados em `experiments/*.json` |
| **Entrega / narrativa integrada** | Notebook acima | Apresentação Colab/Jupyter: classificação + sumarização no mesmo fluxo, com anti-vazamento explícito |

Use o **pipeline oficial** para citar números no relatório quando a pergunta for *“qual modelo venceu na avaliação padronizada do grupo?”*. Use o **notebook** para demonstrar o produto final (classificar + resumir) e para discutir mitigações de vazamento passo a passo.

## O que o notebook faz

1. Carrega a planilha `data/raw/licitacoes2025.csv` e cruza com textos extraídos dos editais.
2. Remove o nome do órgão do texto de classificação e audita **vazamento residual** (ver [`vazamento_de_label.md`](vazamento_de_label.md)).
3. Remove **13 registros** em que o órgão ainda aparece no texto de entrada.
4. Treina **TF-IDF + SVM** (sklearn) para classificar em 6 macroáreas.
5. Opcionalmente roda **sumarização abstrativa** com PTT5 (`RUN_PTT5_SUMMARIZATION = True`).

## Diferenças em relação ao pipeline oficial

| Aspecto | Pipeline oficial | Notebook de entrega |
|---|---|---|
| Classificador | TF-IDF + **LogReg** (baseline) e **BERTimbau** (Fase 2) | TF-IDF + **SVM** |
| Corpus | `data/processed/licitacoes_corpus.jsonl` (423 editais) | CSV + textos; **410 editais** após remover vazamento residual |
| Campo de texto | `objeto_html` (config YAML) | `texto_classificacao` reconstruído (objeto + modalidade + trecho do edital, sem órgão) |
| Split | 70 / 15 / 15 (`seed=42`) | 64 / 16 / 20 (20% teste; 20% do restante para validação) |
| Métricas versionadas | `experiments/classification_*.json` | Saídas nas células do notebook (não substituem o JSON oficial) |
| Sumarização | Script extrativo (`run_train.py --task summarization`) | PTT5 abstrativo (protótipo Fase 3) |

## Métricas observadas no notebook (referência interna)

Após anti-vazamento e split 64/16/20:

| Conjunto | Accuracy | F1 macro |
|---|---:|---:|
| Treino | ≈ 0,95 | ≈ 0,95 |
| Validação | ≈ 0,76 | ≈ 0,76 |
| **Teste** | ≈ 0,84 | **≈ 0,83** |

**Não compare diretamente** com o baseline oficial (F1 macro teste ≈ **0,74**, run `classification_baseline_20260608-190839`) sem alinhar: classificador (SVM vs LogReg), tamanho do corpus (410 vs 423), campo textual e proporção do split.

Para o relatório, mantenha a tabela **baseline vs BERT** da Fase 2 ([`FASE2-CLASSIFICACAO.md`](FASE2-CLASSIFICACAO.md)) como referência principal. O notebook entra como **evidência complementar** de que SVM + anti-vazamento rigoroso melhora a generalização na trilha exploratória.

## Como executar

```bash
cd deep-learning-pln-project
source .venv/Scripts/activate
pip install -r requirements-dev.txt   # sklearn, pandas, jupyter já inclusos
jupyter notebook notebooks/projeto_final_pln_macroareas_tfidf_svm_ptt5_anti_vazamento2.ipynb
```

Para sumarização com PTT5, instale também Transformers + PyTorch (`pip install -e ".[bert]"` ou dependências equivalentes) e defina `RUN_PTT5_SUMMARIZATION = True` na célula de configuração.

## Outros notebooks

| Notebook | Papel |
|---|---|
| [`notebooks/01_eda.ipynb`](../notebooks/01_eda.ipynb) | EDA oficial — distribuição de classes, tamanho de texto, vazamento quantificado (Tabela 7) |
