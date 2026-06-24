# Model card — licitações ComprasNet DF 2025

Resumo do que o projeto faz e dos números que usamos no relatório. Runs em `experiments/` (`20260624-*`).

## O que é isto

Dois pipelines no mesmo corpus (`licitacoes_corpus.jsonl`, 423 editais):

| Tarefa | Modelos | Papel |
|--------|---------|-------|
| Classificação (6 macroáreas) | LogReg · SVM · BERTimbau | LogReg = o que reportamos; SVM e BERT = comparativos |
| Sumarização cidadã | Extrativo (regex/regras) | Complementar |

Ficamos com o LogReg porque teve o melhor F1 macro no teste (0,74). Explicação em [`metricas_e_decisoes.md`](metricas_e_decisoes.md) e [`COMPARATIVO-FASES.md`](COMPARATIVO-FASES.md).

## Uso pretendido

- **Classificação:** triagem de editais por área de gasto (Saúde, Saneamento, Segurança, Educação, Infraestrutura/Obras, Administração/Outros).
- **Sumarização:** parágrafo legível para cidadãos (objeto, quem participa, prazo, valor).

Não substitui análise jurídica nem decisão administrativa.

---

## Performance — classificação

**Protocolo comum:** `objeto_html` · split 70/15/15 estratificado · `seed=42` · label proxy órgão→área

### Modelo principal — TF-IDF + LogReg (Fase 1)

**Run:** `classification_baseline_20260624-013836`

| Conjunto | Accuracy | F1 macro | F1 weighted |
|----------|----------|----------|-------------|
| Validação | 0,766 | **0,743** | 0,750 |
| Teste | 0,797 | **0,740** | 0,788 |

Matriz: `reports/figures/classification_baseline_20260624-013836_confusion.png`

### Comparativo — TF-IDF + SVM (Fase 3)

**Run:** `classification_svm_20260624-013851`

| Conjunto | Accuracy | F1 macro | F1 weighted |
|----------|----------|----------|-------------|
| Validação | 0,797 | **0,797** | 0,775 |
| Teste | 0,797 | **0,652** | 0,774 |

Queda val→teste sugere overfitting relativo ao LogReg. Matriz: `reports/figures/classification_svm_20260624-013851_confusion.png`

### Comparativo — BERTimbau (Fase 2)

**Run:** `classification_bertimbau_20260624-013908`  
**Modelo:** `neuralmind/bert-base-portuguese-cased` · GPU RTX 4090

| Conjunto | Accuracy | F1 macro | F1 weighted |
|----------|----------|----------|-------------|
| Validação | 0,734 | **0,559** | 0,667 |
| Teste | 0,688 | **0,400** | 0,604 |

Matriz: `reports/figures/classification_bertimbau_20260624-013908_confusion.png`  
Detalhes: [`FASE2-CLASSIFICACAO.md`](FASE2-CLASSIFICACAO.md)

### Tabela resumo (teste)

| Modelo | F1 macro | Δ vs LogReg |
|--------|----------|-------------|
| **TF-IDF + LogReg** | **0,740** | — |
| TF-IDF + SVM | 0,652 | −0,09 |
| BERTimbau | 0,400 | −0,34 |

### Por que não `texto` como entrada?

`texto` (HTML completo) repete o órgão em ~97% dos casos → F1 macro ≈ 0,88 (vazamento). Com `objeto_html`: ≈ 0,74 (honesto). Ver [`vazamento_de_label.md`](vazamento_de_label.md).

---

## Performance — sumarização extrativa (Fase 4)

**Run:** `summarization_extractive_20260624-013951`  
**Amostra:** 18 editais do teste (estratificados)

| Cobertura | Valor |
|-----------|-------|
| Com prazo | 15/18 (83%) |
| Com valor | 18/18 (100%) |

Exemplos: `reports/slides/resumos_exemplos.md` · JSONL: `data/processed/resumos_extrativos.jsonl`

---

## Dados e limitações

| Campo | Papel |
|-------|--------|
| `orgao_csv` | Gera label — **não** é feature |
| `objeto_html` | Entrada do classificador |
| `texto` | Sumarização; vaza label na classificação |

- Corpus pequeno (~423) — classes raras (Educação: 2 no teste).
- Label proxy — validação humana ≈83,2% ([`validacao_labels/`](validacao_labels/validacao_labels.md)).
- Só ComprasNet DF 2025 — não generaliza para todo o Brasil.

## Onde o modelo engana

- **Segurança / Educação / Infra:** F1 instável; BERT chega a F1=0.
- **Objetos genéricos** (“aquisição de materiais”) confundem áreas.
- **Sumarização extrativa** não parafraseia — só extrai campos.

## Artefatos

| Artefato | Caminho |
|----------|---------|
| LogReg / SVM | `models/classification_*_<timestamp>.joblib` |
| BERT | `models/classification_bertimbau_<timestamp>/` (pasta, ~416 MB) |
| Registro | `experiments/<run_id>.json` |
| MLflow | `experiments/mlflow.db` — `make mlflow-ui` |

---

*Sincronizado com runs `20260624-013836`, `013851`, `013908`, `013951`.*
