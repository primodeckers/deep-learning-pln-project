# Fase 2 — Classificação BERTimbau

Documento técnico da **Fase 2**: fine-tuning de `neuralmind/bert-base-portuguese-cased` no mesmo corpus e split da Fase 1, para comparar deep learning vs baseline TF-IDF + LogReg.

> Fase 1 (baseline LogReg): [`FASE1-CLASSIFICACAO.md`](FASE1-CLASSIFICACAO.md)  
> Fase 3 (SVM): [`FASE3-CLASSIFICACAO.md`](FASE3-CLASSIFICACAO.md)  
> Métricas e decisões: [`metricas_e_decisoes.md`](metricas_e_decisoes.md)  
> Treino na GPU: [`GPU-EQUIPE.md`](GPU-EQUIPE.md)

---

## 1. Objetivo

Testar a hipótese do guia: *Transformers (BERTimbau) superam baseline clássico* na classificação por macroárea, com **mesma entrada** (`objeto_html`), **mesmo split** (`seed=42`, 70/15/15) e **mesmo label proxy**.

**Critério de comparação:** F1 macro no **conjunto de teste**.

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

## 3. Runs e resultados

### Run de referência (oficial — GPU)

**ID:** `classification_bertimbau_20260623-222508`  
**Ambiente:** RTX 4090, PyTorch `2.12.1+cu126` (`check_cuda.py` = sim)  
**JSON:** `experiments/classification_bertimbau_20260623-222508.json`  
**Matriz:** `reports/figures/classification_bertimbau_20260623-222508_confusion.png`

| Conjunto | Accuracy | F1 macro | F1 weighted |
|----------|----------|----------|-------------|
| Validação | 0,703 | **0,425** | 0,624 |
| Teste | 0,719 | **0,518** | 0,652 |

### Comparação com baseline (teste)

| Modelo | Run | F1 macro (teste) | Δ vs baseline |
|--------|-----|------------------|---------------|
| **TF-IDF + LogReg** | `classification_baseline_20260608-190839` | **0,740** | — |
| **BERTimbau** | `classification_bertimbau_20260623-222508` | **0,518** | **−0,22** |

**Decisão:** o **baseline permanece o modelo principal** reportado no relatório. BERTimbau entra como **comparativo de deep learning** no mesmo protocolo.

### F1 por classe (teste) — baseline vs BERT

| Macroárea | Support (teste) | Baseline F1 | BERT F1 |
|-----------|----------------:|------------:|--------:|
| Saúde | 17 | 0,903 | 0,824 |
| Saneamento | 7 | **1,000** | 0,857 |
| Segurança | 9 | 0,462 | **0,000** |
| Educação | 2 | 0,667 | **0,000** |
| Infraestrutura/Obras | 4 | 0,600 | 0,667 |
| Administração/Outros | 25 | 0,807 | 0,762 |

**Padrão BERT:** forte em Saúde/Saneamento; **colapso** em Segurança e Educação (F1 0); tendência a prever `Administracao/Outros` (recall 0,96).

### Run preliminar (CPU)

`classification_bertimbau_20260623-213337` — F1 macro teste **0,401** (mesmo val 0,425). Substituído pelo run GPU acima como referência; mantido no histórico do repo.

---

## 4. Interpretação (para relatório e slides)

### Parágrafo — comparação de modelos

> Treinamos BERTimbau (`neuralmind/bert-base-portuguese-cased`) com o mesmo split estratificado (`seed=42`) e entrada `objeto_html` usados no baseline TF-IDF + Regressão Logística. No conjunto de **teste** (64 editais), o baseline atingiu **F1 macro 0,74**, enquanto o BERTimbau atingiu **0,52**. O Transformer **não superou** o modelo clássico neste corpus (~295 exemplos de treino, 6 classes desbalanceadas). O BERT manteve desempenho razoável em Saúde e Saneamento, mas **não classificou** editais de Segurança e Educação no teste (F1 = 0), convergindo frequentemente para Administração/Outros.

### Parágrafo — limitações estruturais

> O resultado reforça limitações já documentadas: **corpus pequeno para fine-tuning**, **label proxy** por órgão (validação humana ≈83,2% de concordância) e **poucos exemplos** nas classes raras (2–9 no teste). Não interpretamos o F1 inferior do BERT como falha do pipeline, e sim como evidência de que, **neste volume de dados**, o baseline esparso (TF-IDF) generaliza melhor que um modelo com milhões de parâmetros.

### Frase curta (slide)

> *Baseline F1 0,74 · BERT F1 0,52 · mesmo split · BERT não venceu — corpus pequeno + classes raras.*

---

## 5. O que colocar nos slides (checklist Fase 2)

- [ ] Tabela baseline vs BERT (F1 macro **teste**)
- [ ] Matriz de confusão BERT (`222508`) — ou print MLflow
- [ ] F1 por classe: destacar Segurança/Educação = 0 no BERT
- [ ] Mencionar treino na **RTX 4090** (reprodutibilidade de ambiente)
- [ ] **Não** esconder que DL perdeu — interpretar com volume + desbalanceamento
- [ ] Ligar confusões ao label proxy ([`validacao_labels.md`](validacao_labels/validacao_labels.md) — CBMDF, TCDF)

---

## 6. MLflow (print para slide)

Experimento: **`pln-licitacoes`**

```bash
python -m mlflow ui --backend-store-uri sqlite:///experiments/mlflow.db
```

Abrir `http://127.0.0.1:5000` → comparar runs `classification_baseline_*` e `classification_bertimbau_222508`.

---

## 7. Próximos passos (pós Fase 2)

| Prioridade | Tarefa |
|------------|--------|
| Alta | Slides PDF com §4 acima |
| Alta | Fase 3 — TF-IDF + SVM ([`FASE3-CLASSIFICACAO.md`](FASE3-CLASSIFICACAO.md)) |
| Alta | Fase 4 — sumarização ([`FASE4-SUMARIZACAO.md`](FASE4-SUMARIZACAO.md)) |
| Média | Gráfico valor homologado × área predita (baseline) |
| Baixa | Retunar BERT / expandir corpus — **não bloqueia entrega** |

---

## 8. Referências no repositório

| Artefato | Caminho |
|----------|---------|
| Classificador BERT | `src/models/bert_classifier.py` |
| Orquestração | `src/train/train_classification.py` |
| Config GPU | `configs/classification_bert_gpu.yaml` |
| Runs oficiais | [`experiments/README.md`](../experiments/README.md) |

---

*Última atualização: 2026-06-23 — run oficial GPU `222508`.*
