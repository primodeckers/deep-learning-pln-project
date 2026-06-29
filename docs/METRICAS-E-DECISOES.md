# Métricas e decisões de avaliação

Anotações do grupo sobre o que medimos, como ler os números e por que o relatório usa o LogReg da Fase 1 como modelo principal.

> Números consolidados: [`MODEL-CARD.md`](MODEL-CARD.md)  
> Validação vs teste (as três fases): [`COMPARATIVO-FASES.md`](COMPARATIVO-FASES.md)  
> Tuning e melhoria de métricas: [`HIPERPARAMETROS-E-MELHORIAS.md`](HIPERPARAMETROS-E-MELHORIAS.md)  
> Regras e protocolos PNCP: [`REGRAS-E-PROTOCOLOS.md`](REGRAS-E-PROTOCOLOS.md)  
> Guia do projeto: [`UNIVERSAL-DEEP-LEARNING-GUIDE.md`](UNIVERSAL-DEEP-LEARNING-GUIDE.md) §6

---

## 1. O que cada métrica significa

### Classificação multiclasse (6 macroáreas)

| Métrica | Fórmula (intuição) | Quando usar | Armadilha |
|---------|-------------------|-------------|-----------|
| **F1 macro** | Média do F1 de **cada classe**, com peso igual | **Métrica primária** — corpus desbalanceado | Uma classe com F1=0 puxa o macro para baixo (correto para nosso caso) |
| **F1 weighted** | Média do F1 ponderada pelo `support` de cada classe | Referência secundária | Favorece Saúde e Administração/Outros (classes grandes) |
| **Accuracy** | Acertos / total | Contexto em slides | 79% de accuracy pode esconder F1=0 em Educação (só 2 exemplos no teste) |
| **F1 por classe** | Harmônica de precisão e recall **por macroárea** | Diagnóstico — onde o modelo falha | Classes com `support < 5` no teste são **instáveis** (não comparar com rigor estatístico) |
| **Precisão** | Dos preditos como X, quantos eram X de verdade | Ver confusão “para onde vai” | Alta precisão + recall baixo = modelo raramente prevê a classe |
| **Recall** | Dos verdadeiros X, quantos o modelo achou | Ver classes “cegas” | BERT costuma recall alto em `Administracao/Outros` (classe majoritária) |
| **Matriz de confusão** | Tabela verdadeiro × predito | Slides e relatório | Mostra se erros são entre áreas semanticamente próximas |

**F1 de uma classe:** \(F1 = 2 \cdot \frac{\text{precision} \cdot \text{recall}}{\text{precision} + \text{recall}}\). Penaliza tanto falsos positivos quanto falsos negativos — adequado quando errar Segurança como Administração tem o mesmo custo metodológico que o inverso.

**Por que não só accuracy?** Com 25/64 exemplos de teste em Administração/Outros, um modelo que **sempre** prevê essa classe teria accuracy ≈ 39% só nessa classe, mas o padrão real é pior: mascaramos falhas em Educação (2 exemplos) e Segurança (9).

---

## 2. Protocolo experimental (igual para todos os classificadores)

| Item | Valor fixo | Por quê |
|------|------------|---------|
| Corpus | `licitacoes_corpus.jsonl` — 423 editais | `sha256=46c6e761…` em cada JSON |
| Entrada | `objeto_html` | Evita vazamento de label (~49% residual vs ~97% em `texto`) |
| Split | 70% treino / 15% val / 15% teste | ~295 / 64 / 64 exemplos |
| Estratificação | Por `area` | Preserva proporção de classes em cada fold |
| `seed` | 42 | Mesmas partições para LogReg, SVM e BERT |
| Seleção de modelo | Olhar **val** durante desenvolvimento | **Relatório final reporta teste** (nunca “só val”) |

**Código:** `src/preprocess/dataset.py` · `configs/classification.yaml`

---

## 3. Qual modelo ficou no relatório

Retreino de jun/2026 (`20260624-*`). Critério: F1 macro no **teste**.

| Fase | Modelo | Run | F1 teste | Papel |
|------|--------|-----|----------|--------|
| 1 | TF-IDF + LogReg | `classification_baseline_20260624-013836` | **0,740** | Principal |
| 3 | TF-IDF + SVM | `classification_svm_20260624-013851` | 0,652 | Comparativo |
| 2 | BERTimbau | `classification_bertimbau_20260624-013908` | 0,400 | Comparativo |

### LogReg em vez de SVM

Mesmo vetorizador TF-IDF. O SVM foi melhor na validação (F1 0,797) e pior no teste (0,652). O LogReg ficou estável (0,743 → 0,740). Parece overfitting nos 64 editais de val — ver [`COMPARATIVO-FASES.md`](COMPARATIVO-FASES.md).

### LogReg em vez de BERT

O BERT tem muitos parâmetros e pouco treino (~295 editais). Nos runs que fizemos o teste ficou entre 0,40 e 0,52; o LogReg ficou em 0,74. A hipótese do trabalho era testar o Transformer; no nosso volume de dados o clássico ganhou. Detalhe por classe no comparativo.

### Sobre o BERT ter “piorado” no retreino

Run antigo (`222508`): teste 0,518. Run novo (`013908`): teste 0,400, mas validação subiu. Mesmo seed no split — o treino neural não é 100% reprodutível. De qualquer forma, nos dois ficou abaixo do LogReg.

---

## 4. Campo de entrada e vazamento de label

| Campo | F1 macro (teste, baseline) | Vazamento (Tabela 7 EDA) | Papel |
|-------|------------------------------|--------------------------|--------|
| `texto` | ≈ 0,88 | ~97% | Contraste — teto inflado |
| **`objeto_html`** | **≈ 0,74** | ~49% | **Entrada oficial** |
| `objeto_html_limpo` | _(experimento)_ | ~47% | Limpeza extra — ganho marginal |

**Decisão:** `text_field: objeto_html` em `configs/classification.yaml`.

Não há limiar universal de vazamento aceitável — critério **metodológico**. Ver [`VAZAMENTO-DE-LABEL.md`](VAZAMENTO-DE-LABEL.md) §5.1 e §9.

O modelo **não** recebe `orgao_csv` como feature.

---

## 5. Validação humana do label proxy

| Item | Valor |
|------|-------|
| Amostra | 30 editais, seed 42 |
| Gabarito | [`VALIDACAO-LABELS/VALIDACAO-LABELS.md`](VALIDACAO-LABELS/VALIDACAO-LABELS.md) |
| Status | 4/4 fichas (2026-06-18 a 2026-06-22) |
| Concordância média | **≈83,2%** (62,5%–96,2% por revisor) |

Conclusão: proxy por órgão é **rotulagem fraca aceitável** para baseline; erros estruturais (ex.: CBMDF com objeto clínico) explicam parte das confusões Segurança ↔ Saúde.

---

## 6. F1 por classe (teste) — três classificadores

| Macroárea | Support | LogReg | SVM | BERT |
|-----------|--------:|-------:|----:|-----:|
| Saúde | 17 | 0,903 | 0,903 | 0,875 |
| Saneamento | 7 | 1,000 | 1,000 | 0,800 |
| Segurança | 9 | 0,462 | 0,462 | **0,000** |
| Educação | 2 | 0,667 | **0,000** | **0,000** |
| Infraestrutura/Obras | 4 | 0,600 | 0,750 | **0,000** |
| Administração/Outros | 25 | 0,807 | 0,800 | 0,727 |

**Leitura:** classes com poucos exemplos (Educação n=2) têm F1 instável. BERT colapsa nas classes raras e converge para Administração/Outros.

---

## 7. Hiperparâmetros de referência

Valores **em produção** nos runs oficiais. Ideias de grid, pesos no BERT e backlog: [`HIPERPARAMETROS-E-MELHORIAS.md`](HIPERPARAMETROS-E-MELHORIAS.md).

### Baseline (Fase 1) — `configs/classification.yaml`

| Parâmetro | Valor | Nota |
|-----------|-------|------|
| `ngram_max` | 2 | Unigramas + bigramas |
| `min_df` | 2 | Ignora termos únicos |
| `max_features` | 20 000 | Teto de vocabulário |
| `C` | 1.0 | Regularização L2 |
| `class_weight` | balanced | Mitiga desbalanceamento |

### SVM (Fase 3)

Mesmo vetorizador; `kernel=linear`, `probability=true`, `class_weight=balanced`.

### BERTimbau (Fase 2) — `configs/classification_bert_gpu.yaml`

| Parâmetro | Valor |
|-----------|-------|
| `model_name` | `neuralmind/bert-base-portuguese-cased` |
| `max_length` | 512 |
| `batch_size` | 16 |
| `learning_rate` | 2e-5 |
| `epochs` | 4 (early stopping patience 2) |

---

## 8. Rastreamento (JSON + MLflow)

Cada treino gera:

1. **`experiments/<run_id>.json`** — versionável no Git; métricas + `dataset.sha256` + `git_commit`.
2. **`experiments/mlflow.db`** — comparação local (`make mlflow-ui`, Windows: `--workers 1`).
3. **`models/`** — LogReg/SVM `.joblib`; BERT pasta `model.safetensors` (~416 MB, gitignored).

Baseline e SVM aparecem na aba **Models** do MLflow via autolog sklearn. BERT usa `mlflow.transformers.log_model` (desde retreino com código atualizado).

---

## 12. EDA PNCP DF/2025 (exploratório — não treinado)

Fonte: `data/comprasGOV-anual-VW_FT_PNCP_COMPRA-2025.xls` · Notebook: [`03_eda_pncp.ipynb`](../notebooks/03_eda_pncp.ipynb)  
Filtro: `UF=DF`, `ano=2025` → **19.944** compras · **215** órgãos

| Métrica / achado | Valor | Nota |
|------------------|------:|------|
| Mediana palavras (`objeto_compra`) | 32 | Texto curto vs HTML (~239 no corpus) |
| Compras > 512 palavras | 0 | BERT `max_len=512` irrelevante neste metadado |
| Vazamento em `objeto_compra` | 50,6% | Análogo ao ~49% do `objeto_html` |
| Vazamento residual (órgão no objeto) | 11,0% | 2.185 compras |
| Modalidade dominante | Inexigibilidade 38,8% | Perfil ≠ corpus pregão (~66%) |
| Mediana valor homologado (Saúde) | ~R$ 110.575 | Ver §3.4 em [`FASE1-CLASSIFICACAO.md`](FASE1-CLASSIFICACAO.md) |

---

## 10. Extensão PNCP DF/2025 (~19.944 compras)

Corpus: `data/processed/pncp_corpus_df2025.jsonl` · split 70/15/15 · seed 42 · F1 macro **teste**.

### Protocolo honesto — 6 macroáreas por órgão (`pncp`)

| Modelo | F1 teste | Run |
|--------|----------|-----|
| LogReg | 0,756 | `classification_pncp_baseline_20260628-232841` |
| SVM | 0,783 | `classification_pncp_svm_20260628-232909` |
| **BERTimbau** | **0,858** | `classification_pncp_bertimbau_20260628-233442` |

Referência conservadora em escala grande: BERT supera baselines quando o rótulo é órgão→macroárea.

### Protocolos 9 setores (exploratórios)

| Protocolo | Descrição | LogReg | SVM | BERT |
|-----------|-----------|-------:|----:|-----:|
| **`pncp9`** | Só compras com keyword (~10,3k) | 0,857 | 0,877 | **0,969** |
| **`pncp9full`** | 9 + Indeterminado (19,9k) | 0,816 | 0,862 | **0,970** |
| **`pncp9fb`** | Fallback órgão, só objeto | **0,824** | — | — |
| **`pncp9fbi`** | Fallback + info complementar | 0,788 | 0,829 | **0,955** |

**Leitura:**

- F1 ~0,97 (`pncp9`, `pncp9full`, `pncp9fbi`+BERT) reflete **reprodução de regras keyword** + acoplamento rótulo↔texto quando info entra nos dois — não substitui o protocolo honesto (`pncp` 0,858).
- Info complementar **piora** LogReg (0,824→0,788) mas **dispara** BERT (0,829→0,955).
- Benchmark de coortes difíceis: `python scripts/run_benchmark_pncp_dificeis.py`.

Detalhe das regras: [`REGRAS-E-PROTOCOLOS.md`](REGRAS-E-PROTOCOLOS.md).

---

## 11. O que não fazemos (escopo consciente)

- Limiar de probabilidade de negócio — classificação multiclasse pura.
- API de produção — pipeline batch via `scripts/run_train.py`.
- Retreino automático — runs manuais documentados.

---

## 12. Checklist antes de apresentar

- [x] `objeto_html` documentado como entrada oficial
- [x] Validação manual 4/4 (≈83,2%)
- [x] F1 macro no **teste** para os três classificadores
- [x] Tabela comparativa Fases 1–3 + decisão LogReg
- [x] Classes com `support < 5` discutidas (Educação n=2)
- [x] Hash do corpus citado
- [ ] Slides PDF com matrizes e §3 deste documento
