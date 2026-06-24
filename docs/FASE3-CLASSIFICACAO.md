# Fase 3 — Classificação TF-IDF + SVM

Documento técnico da **Fase 3**: segundo classificador **clássico** no **mesmo protocolo** das Fases 1 e 2 (corpus, `objeto_html`, split 70/15/15, `seed=42`).

> Fase 1 (baseline LogReg): [`FASE1-CLASSIFICACAO.md`](FASE1-CLASSIFICACAO.md)  
> Fase 2 (BERTimbau): [`FASE2-CLASSIFICACAO.md`](FASE2-CLASSIFICACAO.md)  
> Fase 4 (sumarização — **outra tarefa**): [`FASE4-SUMARIZACAO.md`](FASE4-SUMARIZACAO.md)

---

## 1. Objetivo

Testar se **SVM linear** sobre os mesmos features TF-IDF do baseline **supera** a Regressão Logística, mantendo comparabilidade total com Fases 1 e 2.

**Critério:** F1 macro no **conjunto de teste**.

**Treino:** sempre via script — **não** em notebook.

```bash
make train-svm
# ou: python scripts/run_train.py --task classification --model svm
```

---

## 2. Setup (idêntico às Fases 1 e 2)

| Item | Valor |
|------|--------|
| Corpus | `licitacoes_corpus.jsonl` — 423 editais |
| `text_field` | `objeto_html` |
| Split | 295 treino / 64 val / 64 teste |
| Label | Proxy órgão → área (`labels.py`) |
| Config | `configs/classification.yaml` (`model: svm`) |

### Hiperparâmetros SVM

| Parâmetro | Valor |
|-----------|--------|
| Vetorizador | Igual ao baseline (`baseline_tfidf.PORTUGUESE_STOPWORDS`) |
| `ngram_max` | 2 |
| `max_features` | 20000 |
| `C` | 1.0 |
| `kernel` | `linear` |
| `class_weight` | `balanced` |
| `probability` | `true` (Platt — `predict_proba`) |
| `seed` | 42 |

**Código:** `src/models/svm_tfidf.py` · `src/train/train_classification.py`

---

## 3. Run de referência

**ID:** `classification_svm_20260624-004348`  
**JSON:** `experiments/classification_svm_20260624-004348.json`  
**Matriz:** `reports/figures/classification_svm_20260624-004348_confusion.png`

| Conjunto | Accuracy | F1 macro | F1 weighted |
|----------|----------|----------|-------------|
| Validação | 0,797 | **0,797** | 0,775 |
| Teste | 0,797 | **0,652** | 0,774 |

### Comparação dos três classificadores (teste)

| Fase | Modelo | Run | F1 macro (teste) |
|------|--------|-----|------------------|
| 1 | TF-IDF + **LogReg** | `classification_baseline_20260608-190839` | **0,740** |
| 3 | TF-IDF + **SVM** | `classification_svm_20260624-004348` | **0,652** |
| 2 | **BERTimbau** | `classification_bertimbau_20260623-222508` | **0,518** |

**Decisão:** **Fase 1 (LogReg) permanece o modelo principal** do relatório. Fase 3 mostra que trocar LogReg por SVM **não melhorou** generalização no teste. Fase 2 (BERT) ficou abaixo dos dois clássicos.

### F1 por classe (teste) — SVM

| Macroárea | Support | F1 |
|-----------|--------:|---:|
| Saúde | 17 | 0,903 |
| Saneamento | 7 | 1,000 |
| Segurança | 9 | 0,462 |
| Educação | 2 | **0,000** |
| Infraestrutura/Obras | 4 | 0,750 |
| Administração/Outros | 25 | 0,800 |

---

## 4. Interpretação (para relatório)

> Treinamos TF-IDF + SVM linear com o mesmo split e entrada `objeto_html` das Fases 1 e 2. No **teste**, o SVM atingiu **F1 macro 0,65**, abaixo do baseline LogReg (**0,74**) e acima do BERTimbau (**0,52**). O SVM teve validação alta (F1 0,80) e queda no teste — sinal de **overfitting** relativo ao LogReg no mesmo protocolo.

### Frase curta (slide)

> *Fase 1 LogReg 0,74 · Fase 3 SVM 0,65 · Fase 2 BERT 0,52 — mesmo split.*

---

## 5. O que colocar nos slides

- [ ] Tabela **três modelos** (Fases 1, 2, 3)
- [ ] Matriz de confusão SVM (`004348`)
- [ ] Deixar claro: SVM seguiu o **mesmo processo** (`run_train.py` + JSON em `experiments/`)

---

## 6. Artefatos

| Artefato | Caminho |
|----------|---------|
| Pipeline SVM | `src/models/svm_tfidf.py` |
| Run oficial | `experiments/classification_svm_20260624-004348.json` |
| Demo (só leitura) | `notebooks/02_demo_classificacao.ipynb` |

---

*Última atualização: 2026-06-24 — run `004348`.*
