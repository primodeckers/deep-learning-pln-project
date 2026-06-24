# Fase 3 — Classificação TF-IDF + SVM

Mesmo protocolo das Fases 1 e 2 — só trocamos o classificador em cima do mesmo TF-IDF.

> Fase 1: [`FASE1-CLASSIFICACAO.md`](FASE1-CLASSIFICACAO.md) · Fase 2: [`FASE2-CLASSIFICACAO.md`](FASE2-CLASSIFICACAO.md)  
> Comparativo val/teste: [`COMPARATIVO-FASES.md`](COMPARATIVO-FASES.md)

---

## 1. Objetivo

Testar se **SVM linear** sobre os **mesmos features TF-IDF** do baseline **supera** a Regressão Logística.

**Critério:** F1 macro no **conjunto de teste**.

**Resultado:** SVM **não superou** LogReg (0,652 vs 0,740); validação alta com queda no teste indica **overfitting** relativo.

```bash
make train-svm
```

---

## 2. Setup (idêntico às Fases 1 e 2)

| Item | Valor |
|------|--------|
| Corpus | 423 editais · `sha256=46c6e761…` |
| `text_field` | `objeto_html` |
| Split | 295 / 64 / 64 · `seed=42` |
| Config | `configs/classification.yaml` (`model: svm`) |

### Hiperparâmetros SVM

| Parâmetro | Valor |
|-----------|--------|
| Vetorizador | Igual ao baseline |
| `kernel` | `linear` |
| `C` | 1.0 |
| `class_weight` | `balanced` |
| `probability` | `true` |

**Código:** `src/models/svm_tfidf.py`

---

## 3. Run de referência

**ID:** `classification_svm_20260624-013851`  
**JSON:** `experiments/classification_svm_20260624-013851.json`  
**Matriz:** `reports/figures/classification_svm_20260624-013851_confusion.png`

| Conjunto | Accuracy | F1 macro | F1 weighted |
|----------|----------|----------|-------------|
| Validação | 0,797 | **0,797** | 0,775 |
| Teste | 0,797 | **0,652** | 0,774 |

### Comparação dos três classificadores (teste)

| Fase | Modelo | F1 macro (teste) |
|------|--------|------------------|
| **1** | TF-IDF + **LogReg** | **0,740** ← principal |
| 3 | TF-IDF + SVM | 0,652 |
| 2 | BERTimbau | 0,400 |

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

## 4. Interpretação

Treinamos SVM linear com o mesmo TF-IDF e split do LogReg. No teste o F1 macro foi 0,65 — abaixo do LogReg (0,74) e acima do BERT (0,40). Na validação chegou a 0,80, então a queda val→teste chamou atenção: parece que o SVM se ajustou demais aos 64 editais de val. Educação zerou no teste (só 2 exemplos). Mantemos o LogReg como baseline do relatório.

Para slides: *LogReg 0,74 · SVM 0,65 · BERT 0,40 — mesmo split.*

---

## 5. Slides

- [ ] Tabela três modelos
- [ ] Matriz SVM (`013851`)
- [ ] Mesmo processo: `run_train.py` + JSON + MLflow

---

*Última atualização: 2026-06-24 — run `013851`.*
