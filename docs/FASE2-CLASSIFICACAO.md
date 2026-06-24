# Fase 2 — Classificação BERTimbau

Fine-tuning do `neuralmind/bert-base-portuguese-cased` no mesmo corpus e split do baseline — pra ver se Transformer ganha do clássico.

> Fase 1: [`FASE1-CLASSIFICACAO.md`](FASE1-CLASSIFICACAO.md) · Comparativo: [`COMPARATIVO-FASES.md`](COMPARATIVO-FASES.md)  
> GPU: [`GPU-EQUIPE.md`](GPU-EQUIPE.md)

---

## 1. Objetivo

Testar a hipótese do guia: *Transformers (BERTimbau) superam baseline clássico* na classificação por macroárea, com **mesma entrada** (`objeto_html`), **mesmo split** (`seed=42`, 70/15/15) e **mesmo label proxy**.

**Critério de comparação:** F1 macro no **conjunto de teste**.

**Resultado:** hipótese **não confirmada** — BERT ficou abaixo do LogReg e do SVM.

---

## 2. Setup (igual ao baseline)

| Item | Valor |
|------|--------|
| Corpus | `licitacoes_corpus.jsonl` — 423 editais |
| `text_field` | `objeto_html` |
| Split | 295 treino / 64 val / 64 teste |
| Label | Proxy órgão → área (`labels.py`) |
| Config treino GPU | `configs/classification_bert_gpu.yaml` |

### Hiperparâmetros BERTimbau

| Parâmetro | Valor |
|-----------|--------|
| `model_name` | `neuralmind/bert-base-portuguese-cased` |
| `max_length` | 512 |
| `batch_size` | 16 |
| `learning_rate` | 2e-5 |
| `epochs` | 4 (early stopping, patience 2) |
| `seed` | 42 |

**Código:** `src/models/bert_classifier.py` · `scripts/run_train.py --config configs/classification_bert_gpu.yaml`

---

## 3. Run de referência (oficial)

**ID:** `classification_bertimbau_20260624-013908`  
**Ambiente:** RTX 4090, PyTorch `2.12.1+cu126`  
**JSON:** `experiments/classification_bertimbau_20260624-013908.json`  
**Modelo em disco:** `models/classification_bertimbau_20260624-013908/` (~416 MB)  
**Matriz:** `reports/figures/classification_bertimbau_20260624-013908_confusion.png`  
**MLflow:** logged model `transformers` na aba Models (run `pln-licitacoes`)

| Conjunto | Accuracy | F1 macro | F1 weighted |
|----------|----------|----------|-------------|
| Validação | 0,734 | **0,559** | 0,667 |
| Teste | 0,688 | **0,400** | 0,604 |

### Comparação dos três classificadores (teste)

| Fase | Modelo | Run | F1 macro (teste) | Δ vs LogReg |
|------|--------|-----|------------------|-------------|
| 1 | TF-IDF + **LogReg** | `classification_baseline_20260624-013836` | **0,740** | — |
| 3 | TF-IDF + SVM | `classification_svm_20260624-013851` | 0,652 | −0,09 |
| 2 | **BERTimbau** | `classification_bertimbau_20260624-013908` | **0,400** | **−0,34** |

**Decisão:** baseline **permanece o modelo principal**; BERT é **comparativo de deep learning**.

### F1 por classe (teste) — LogReg vs BERT

| Macroárea | Support | LogReg F1 | BERT F1 |
|-----------|--------:|----------:|--------:|
| Saúde | 17 | 0,903 | 0,875 |
| Saneamento | 7 | 1,000 | 0,800 |
| Segurança | 9 | 0,462 | **0,000** |
| Educação | 2 | 0,667 | **0,000** |
| Infraestrutura/Obras | 4 | 0,600 | **0,000** |
| Administração/Outros | 25 | 0,807 | 0,727 |

**Padrão BERT:** razoável em Saúde/Saneamento; **colapso** em classes raras; tendência a prever `Administracao/Outros`.

### Run histórico (referência)

| Run | F1 macro (teste) | Nota |
|-----|------------------|------|
| `20260623-222508` | 0,518 | Retreino anterior GPU |
| `20260623-213337` | 0,401 | CPU — preliminar |

Variância entre runs BERT é esperada (fine-tuning estocástico); em todos os casos **abaixo** do LogReg (0,74).

---

## 4. O que a gente tira disso (relatório / slides)

O BERT não ganhou do LogReg no teste (0,40 vs 0,74). Principais motivos que citamos na discussão:

- Pouco treino (~295 editais) pro tamanho do modelo.
- Classes desbalanceadas — Educação tem 12 no treino e 2 no teste.
- Label vem do órgão; o texto do objeto nem sempre bate com a área.
- TF-IDF + LogReg já pega bem palavras-chave do domínio sem fine-tuning.

No retreino de junho o teste caiu em relação ao run `222508` (0,52 → 0,40), mas a validação melhorou. Fine-tuning não sai igual toda vez, mesmo com o mesmo split.

Texto pronto pra colar no relatório:

> Treinamos BERTimbau com o mesmo split e `objeto_html` do baseline. No teste, LogReg ficou com F1 macro 0,74 e BERT com 0,40. O Transformer não superou o clássico. Segurança, Educação e Infraestrutura zeraram no teste; o modelo empurra muita coisa pra Administração/Outros.

Slide curto: *LogReg 0,74 · SVM 0,65 · BERT 0,40 — mesmo split.*

Mais detalhe val vs teste: [`COMPARATIVO-FASES.md`](COMPARATIVO-FASES.md).

---

## 5. O que colocar nos slides

- [ ] Tabela **três modelos** (Fases 1, 2, 3) — F1 macro **teste**
- [ ] Matriz de confusão BERT (`013908`)
- [ ] F1 por classe: Segurança/Educação/Infra = 0 no BERT
- [ ] Mencionar GPU (reprodutibilidade de ambiente)
- [ ] **Não** esconder que DL perdeu — interpretar com volume + desbalanceamento

---

## 6. MLflow

```bash
make mlflow-ui
# Windows: http://127.0.0.1:5001 se porta 5000 ocupada
```

Experimento `pln-licitacoes` — comparar runs `classification_*_20260624-*`.

---

## 7. Artefatos

| Artefato | Caminho |
|----------|---------|
| Classificador BERT | `src/models/bert_classifier.py` |
| Config GPU | `configs/classification_bert_gpu.yaml` |
| Runs oficiais | [`experiments/README.md`](../experiments/README.md) |

---

*Última atualização: 2026-06-24 — run oficial `013908`.*
