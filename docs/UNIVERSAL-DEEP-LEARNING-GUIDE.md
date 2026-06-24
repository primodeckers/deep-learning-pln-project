# Universal Deep Learning Guide

Guia vivo do projeto — roteiro metodológico para o grupo seguir do problema à apresentação.

> Requisitos da disciplina: [`PROJECT-REQUIREMENTS.md`](PROJECT-REQUIREMENTS.md)  
> Brainstorm de temas: [`PROPOSALS.md`](PROPOSALS.md)  
> Coleta de dados: [`DATA-COLLECTION-DECISIONS.md`](DATA-COLLECTION-DECISIONS.md)  
> Material de aula (referência): [`aula03-04.pdf`](referencias/aula03-04.pdfula03-04.pdf)

---

## Visão geral

| Campo | Valor |
|---|---|
| **Título provisório** | Classificação de editais por área de gasto + resumos em linguagem cidadã (ComprasNet DF 2025) |
| **Modalidade** | PLN no Setor Público |
| **Formato** | Grupo de 4 pessoas |
| **Status** | Fases 0–2 concluídas (baseline F1 ≈ 0,74 · BERT F1 ≈ 0,52 teste) — notebook de entrega SVM+PTT5 pronto; próximo: slides + avaliação humana da sumarização (Fase 3) |
| **Última atualização** | 2026-06-23 |

### Decisão de escopo (Ideia 1 + Ideia 4)

O grupo adota **duas tarefas complementares** sobre o mesmo corpus:

| Papel | Tarefa | Tipo de modelo | Entrega principal |
|---|---|---|---|
| **Principal** | Classificar edital por **área de gasto público** (Saúde, Saneamento…) | Classificação multiclasse | F1, matriz de confusão, comparação baseline vs BERTimbau |
| **Complemento** | **Resumir** edital em linguagem acessível ao cidadão | Sumarização | 5–10 exemplos antes/depois + avaliação humana |

A classificação responde *"em que o DF gasta?"*; a sumarização responde *"o que esse edital significa pra quem não é especialista?"*. Na apresentação, a demo de resumo ilustra o impacto aplicado; as métricas vêm da classificação.

### Integrantes

| Nome | GitHub | Foco sugerido |
|---|---|---|
| Elisangela Osorio | ElisangelaOsorio | _a definir_ |
| _nome_ | pontealexandre | _a definir_ |
| Renê Estevam Deckers | primodeckers | _a definir_ |
| _nome_ | xnetto2 | _a definir_ |

---

## 1. Problema e hipótese

### 1.1 Pergunta central

> É possível, a partir do texto de editais públicos do ComprasNet, **(a)** classificar automaticamente a área de gasto e **(b)** gerar resumos compreensíveis para cidadãos e pequenos fornecedores?

### 1.2 Contexto

- **Domínio:** licitações e contratações públicas (Distrito Federal, 2025)
- **Corpus:** 423 editais extraídos de HTML (`licitacoes_corpus.jsonl`)
- **Público impactado:** gestores, órgãos de controle, cidadãos, MEIs que participam de licitações

### 1.3 Hipóteses

1. Modelos baseados em **Transformers** (BERTimbau) superam um **baseline clássico** (TF-IDF + Regressão Logística) na classificação por área.
2. Resumos gerados por PLN reduzem o jargão jurídico mantendo informações críticas (objeto, prazo, quem pode participar).
3. Cruzar área predita com valor homologado e modalidade gera **insights de transparência** além da métrica pura.

### 1.4 Escopo

**Dentro:** corpus ComprasNet DF 2025, classificação em 6 macroáreas, sumarização de amostra representativa, comparação de modelos, análise crítica.

**Fora:** PDF com CAPTCHA, licitações fora do DF/2025, bases prontas (Kaggle), quebra automatizada de CAPTCHA.

---

## 2. Fluxo do Learning (adaptado à aula)

O professor define o ciclo: **Problema → Dados → Modelo → Avaliação → Decisão**. Nosso projeto percorre esse fluxo duas vezes (classificação e sumarização), compartilhando a base de dados.

```
                    ┌─────────────────────────────────────┐
                    │  1. PROBLEMA                        │
                    │  Transparência + acessibilidade     │
                    └───────────────┬──────────────────────────────┘
                                   ▼
                    ┌─────────────────────────────────────┐
                    │  2. DADOS (✅ feito)                 │
                    │  CSV + HTML → corpus JSONL           │
                    └───────────────┬──────────────────────────────┘
                                   ▼
          ┌────────────────────────┬──────────────────────────┐
          │  3a. MODELO (classificação)  │  3b. MODELO (resumo)   │
          │  TF-IDF → BERTimbau     │  extrativo → abstrativo│
          └──────────┬──────────┴─────────┬─────────────────┘
                    ▼                        ▼
          ┌────────────────────────┬──────────────────────────┐
          │  4a. AVALIAÇÃO (F1, CM)   │  4b. AVALIAÇÃO (ROUGE+★)│
          └──────────┬──────────┴─────────┬─────────────────┘
                    ▼
                    ┌─────────────────────────────────────┐
                    │  5. DECISÃO / IMPACTO               │
                    │  Slides, insights, limitações      │
                    └─────────────────────────────────────┘
```

---

## 3. Guia universal de Rede Neural — aplicado ao nosso PLN

O material [`aula03-04.pdf`](referencias/aula03-04.pdf) propõe um guia prático cujo lema é **"depende"** — cada escolha depende do problema, do volume de dados e do diagnóstico treino vs validação. Abaixo traduzimos cada bloco para **texto + classificação + sumarização**.

### 3.1 Dados: split, normalização e volume

**Quantas amostras temos?** ~423 editais. Para esse porte, a aula recomenda split **70% treino / 15% validação / 15% teste** (estratificado por área). Com ~10k amostras o split muda; com 423, esse recorte é adequado.

**Regra de ouro (aula):** estatísticas de normalização só no **treino**; aplicar a mesma transformação em val/test.

| Aspecto | Classificação | Sumarização |
|---|---|---|
| Entrada | Campo `texto` ou `objeto_html` | Campo `texto` (truncar se >512 tokens) |
| Label | Macroárea (6 classes) derivada de `orgao_csv` | Resumo de referência fraco: `objeto_html` + datas extraídas |
| Split | Estratificado por área | Mesmo split ou subconjunto fixo de 20 editais para avaliação humana |
| Normalização | TF-IDF: fit só no treino; BERT: tokenizer próprio | Tokenizer do modelo seq2seq ou LLM |
| Data augmentation | Sinônimos, back-translation leve (opcional) | Paraphrase leve (cuidado com alterar prazos/valores) |

**Por que Deep Learning aqui?** Texto é dado **não estruturado** e **sequencial** (aula 04: ordem importa; premissa I.I.D. não vale). Com ~423 amostras, ainda faz sentido comparar baseline clássico vs fine-tuning de Transformer — volume pequeno, mas típico de projetos acadêmicos com texto.

### 3.2 Modelo: arquitetura, input e output

| Componente | Classificação (aula → projeto) | Sumarização |
|---|---|---|
| **Input** | Sequência de tokens do edital | Mesmo texto, possivelmente truncado |
| **Output** | Softmax sobre 6 classes (multiclasse) | Sequência de tokens (resumo) ou texto gerado |
| **Arquitetura baseline** | TF-IDF + LogReg (ML clássico) | TextRank / primeiras frases + regex de datas |
| **Arquitetura principal** | BERTimbau + camada linear | mT5-small fine-tuned **ou** prompt LLM |
| **Alternativa (aula seq.)** | BiLSTM (menos usado hoje em PLN) | Seq2seq com LSTM (legado) |
| **Ativação (MLP head)** | ReLU na cabeça; GELU no BERT (já embutido) | — |
| **Inicialização** | Pesos pré-treinados do BERTimbau | Pesos pré-treinados mT5 |

**Nota da aula:** CNN é para grades (imagem); **não** é nossa arquitetura principal. Para texto sequencial, o mercado usa **Transformers** (BERT, T5); LSTM aparece como referência histórica.

### 3.3 Treinamento: loss, otimizador, batch, épocas

| Hiperparâmetro | Classificação (ponto de partida) | Sumarização |
|---|---|---|
| **Loss** | Cross-entropy (multiclasse); `class_weight` se desbalanceado | Cross-entropy seq2seq **ou** ROUGE como métrica offline |
| **Otimizador** | AdamW (padrão de mercado; aula: "comece com Adam") | AdamW |
| **Learning rate** | 2e-5 (BERT fine-tuning); 1e-3 (LogReg) | 3e-5 (mT5) |
| **Batch size** | 16 (BERT); aula sugere 32 como default, reduzir se overfit | 4–8 (memória) |
| **Épocas** | 3–5 com early stopping | 3–5 |
| **Max length** | 512 tokens (BERTimbau) | 512 input / 128 output |

**Early stopping (aula):** parar quando `val_loss` ou `val_f1` deixa de melhorar por N épocas. Salvar o melhor checkpoint em `models/`.

### 3.4 Regularização e diagnóstico viés–variância

A aula ensina: comparar **baseline**, **erro de treino** e **erro de validação** para diagnosticar underfitting vs overfitting.

| Cenário | Treino | Validação | O que fazer (aula) |
|---|---|---|---|
| **Ideal** | F1 alto | F1 próximo | Seguir para teste |
| **Underfitting** | F1 baixo | F1 baixo | Modelo simples demais → BERT, mais épocas, revisar LR |
| **Overfitting** | F1 muito alto | F1 cai | Dropout, weight decay, batch menor, menos épocas, data aug. |
| **Pior caso** | Ruim | Pior ainda | Revisar labels, features, arquitetura |

**Técnicas de regularização aplicáveis:**

| Técnica | Onde usar | Valor inicial |
|---|---|---|
| **Dropout** | Cabeça do classificador / fine-tuning | 0.1–0.3 |
| **Weight decay (L2)** | AdamW | 0.01 |
| **Data augmentation** | Texto: substituição de sinônimos (EDA) | 1–2 versões por amostra |
| **Early stopping** | Ambas tarefas | patience = 2 |

---

## 4. Roteiro do projeto (passo a passo)

### Fase 0 — Coleta e corpus (concluída)

1. Exportar CSV do ComprasNet
2. Baixar HTML de detalhe (`run_collect.py`) — 423 arquivos
3. Extrair texto e montar JSONL (`run_preprocess.py`)
4. Documentar decisões em `DATA-COLLECTION-DECISIONS.md`

### Fase 1 — Preparar labels e baseline (classificação)

1. Definir taxonomia de **6 macroáreas** e mapeamento `orgao_csv` → área
2. Gerar `data/processed/labels_areas.json` ou coluna `area` no dataset
3. Split estratificado treino/val/test (seed fixa para reprodutibilidade)
4. Implementar baseline **TF-IDF (1–2 grams) + Logistic Regression**
5. Calcular **F1 macro**, F1 por classe, matriz de confusão
6. Validar manualmente ~30 editais sorteados (qualidade do label proxy) — **concluído:** 4/4 fichas em `docs/validacao_labels/`; média ≈83,2% (ver gabarito § Síntese)

**Script alvo:** `scripts/run_train.py --task classification --model baseline`

### Fase 2 — Modelo principal (BERTimbau)

1. Fine-tuning `neuralmind/bert-base-portuguese-cased` com Hugging Face `Trainer`
2. Mesmo split da Fase 1 (comparabilidade)
3. Hiperparâmetros iniciais: lr=2e-5, batch=16, epochs=4, max_len=512
4. Early stopping em `val_f1_macro`
5. Comparar tabela baseline vs BERT no relatório
6. Análise de erros: top confusões, cruzamento com `total_homologado` e `modalidade`

**Script alvo:** `scripts/run_train.py --task classification --model bertimbau`

### Fase 3 — Sumarização (complemento)

1. **Baseline extrativa:** TextRank ou lead-3 frases do objeto + datas via regex
2. **Modelo abstrativo (escolher um):**
   - Opção A: fine-tune `unicamp-dl/ptt5-base-portuguese-vocab` (seq2seq)
   - Opção B: prompt estruturado em LLM (5–10 editais piloto; documentar prompt)
3. Gerar resumos para **mesma amostra de 20 editais** (estratificada por área)
4. Avaliação:
   - ROUGE-1 / ROUGE-L (automática, referência fraca)
   - **Escala humana 1–5** (clareza, correção, completude) — 2 integrantes, média
   - Contar **alucinações** (prazo/valor inventado)
5. Selecionar **3 exemplos** para slide antes/depois

**Script alvo:** `scripts/run_train.py --task summarization` (baseline extrativo) **ou** protótipo PTT5 em [`NOTEBOOK-ENTREGA.md`](NOTEBOOK-ENTREGA.md)

### Fase 4 — Análise aplicada e integração

1. Gráfico: distribuição de valor homologado por área predita
2. Opcional: resumir os 5 editais **mais mal classificados** (liga tarefa 1 e 4)
3. Redigir limitações: label proxy, corpus HTML vs PDF, desbalanceamento de classes
4. Registrar experimentos em `experiments/` (JSON + MLflow em `experiments/mlflow.db`)

### Fase 5 — Entrega e apresentação

1. Atualizar README com comandos de execução
2. Montar slides (10 min) — roteiro na seção 8
3. Ensaio cronometrado
4. PDF dos slides em `reports/slides/`

---

## 5. O que o mercado usa (e o que vamos adotar)

Práticas comuns em produção de PLN em 2024–2025, mapeadas para o nosso escopo acadêmico:

| Prática de mercado | Ferramenta / método | Nós usamos? |
|---|---|---|
| Baseline clássico antes de DL | TF-IDF + LogReg / LinearSVM | Sim (Fase 1) |
| Transformer pré-treinado em PT | BERTimbau, Legal-BERT-PT | Sim — BERTimbau |
| Fine-tuning com Hugging Face | `transformers` + `Trainer` | Sim |
| Experiment tracking | MLflow (local) + JSON em `experiments/` | Sim — desde Fase 2 |
| Hiperparâmetros | Grid/random search, Optuna | Manual (suficiente para o prazo) |
| Classificação desbalanceada | `class_weight`, focal loss | `class_weight` |
| Sumarização | T5/mT5, BART, GPT com RAG | mT5 ou prompt LLM (amostra) |
| Avaliação de resumo | ROUGE + avaliação humana | Sim (ambos) |
| MLOps / deploy | FastAPI + modelo serializado | Fora do escopo (mencionar como próximo passo) |
| RAG sobre documentos | Embeddings + busca + LLM | Fora do escopo (citável na discussão) |
| Data versioning | DVC | Opcional; Git + manifestos já documentados |

**O que não precisamos copiar do mercado:** infra de GPU em escala, AutoML tabular (TabPFN), CNNs, pipelines MLOps completos. O professor também alerta que **tree-based models** ainda ganham em dados tabulares pequenos — nosso problema é **texto**, então Transformers são a escolha correta.

---

## 6. Tarefa principal — classificação por área

### 6.1 Taxonomia de labels

Implementado em [`src/preprocess/labels.py`](../src/preprocess/labels.py) — palavras-chave casadas sobre `orgao_csv` normalizado (maiúsculas, sem acento), na ordem da tabela (primeira que casar vence). Contagens **reais** sobre os 423 registros:

| Macroárea | Palavras-chave (normalizadas) | N |
|---|---|---|
| Saúde | SAUDE, HEMOCENTRO | 112 |
| Saneamento | CAESB, SANEAMENTO | 49 |
| Segurança | POLICIA, BOMBEIRO, SEGURANCA, PENITENCI | 58 |
| Educação | EDUCACAO | 17 |
| Infraestrutura / Obras | ESTRADAS, RODAGEM, OBRAS, INFRAESTRUTURA | 24 |
| Administração / Outros | demais | 163 |

O modelo **não** recebe o órgão como feature — só o texto. O órgão gera o label inicial (limitação "label proxy" a declarar no relatório).

> ⚠️ **Vazamento de label no campo `texto`.** O HTML completo (`texto`) repete o nome do órgão (ex.: "Secretaria de Estado de Saúde…"), que é a própria fonte do label. Medido empiricamente: o baseline atinge **F1 macro ≈ 0,88 (teste) usando `texto`**, mas cai para **≈ 0,74 usando `objeto_html`** (descrição do que é comprado, sem o cabeçalho do órgão). Para uma avaliação honesta, usar `objeto_html` como entrada (padrão recomendado) **ou** remover o cabeçalho identificador de `texto`. Os ~0,88 de `texto` devem ser tratados como teto otimista contaminado por vazamento.

### 6.2 Métricas

- **Primária:** F1 macro (seleção de modelo)
- **Secundárias:** F1 por classe, accuracy, matriz de confusão
- **Análise:** curva treino vs val (detectar overfitting conforme aula)

### 6.3 Estrutura de código prevista

```
src/
  models/
    baseline_tfidf.py      # LogReg + pipeline sklearn
    bert_classifier.py    # fine-tune BERTimbau
  train/
    train_classification.py
  evaluate/
    metrics_classification.py
configs/
  classification.yaml     # hiperparâmetros
```

---

## 7. Tarefa complementar — sumarização cidadã

### 7.1 Formato do resumo

Parágrafo de 3–5 frases respondendo:

1. O que está sendo contratado?
2. Quem pode participar?
3. Qual o prazo para propostas?
4. Valor estimado (se constar no texto)?

> ✅ **Baseline extrativo implementado** — [`src/summarize/extractive.py`](../src/summarize/extractive.py).
> Extrai os 4 campos por regras/regex (objeto, ME/EPP, data de entrega, valor homologado)
> e monta o parágrafo. É **determinístico → não alucina** prazo/valor (vantagem sobre o LLM).
> Rodar: `python scripts/run_train.py --task summarization --model extractive`.
> Saídas: amostra estratificada de 18 editais, exemplos antes/depois em
> [`reports/slides/resumos_exemplos.md`](../reports/slides/resumos_exemplos.md).
> Cobertura medida: prazo 15/18, valor 18/18 (dispensas costumam não ter "Entrega da Proposta").

### 7.2 Pipeline recomendado

```
Texto do edital
    → baseline extrativo (TextRank)
    → mT5 fine-tuned OU LLM com prompt fixo
    → revisão humana (20 amostras)
    → 3 exemplos para slides
```

### 7.3 Cuidados (uso responsável)

- LLM pode **inventar** prazo ou valor — contar alucinações e incluir disclaimer nos slides
- Não usar resumo como única fonte legal; é ferramenta de **acessibilidade**, não substituto do edital

### 7.4 Integração com a classificação

Na apresentação, mostrar fluxo:

> Edital → **área predita** (Saúde) + **resumo cidadã** (1 parágrafo)

Isso materializa o diferencial aplicado exigido pela disciplina.

---

## 8. Referencial teórico

Mínimo: **5 artigos de domínio** + **5 de técnica** (ver requisitos).

### 8.1 Domínio (licitações, transparência, setor público)

| # | Referência | Uso no trabalho |
|---|---|---|
| 1 | _a buscar_ | Lei 14.133 / contratações públicas |
| 2 | | Transparência e dados abertos |
| 3 | | PLN aplicado a documentos governamentais |
| 4 | | |
| 5 | | |

### 8.2 Técnica (PLN, DL, Transformers)

| # | Referência | Técnica |
|---|---|---|
| 1 | Devlin et al. (2019) BERT | Fine-tuning classificação |
| 2 | Souza et al. BERTimbau | Modelo em português |
| 3 | Raffel et al. (2020) T5 | Sumarização seq2seq |
| 4 | Goodfellow, Bengio & Courville (2016) Cap. 10 | Sequências / RNN (contexto aula) |
| 5 | Srivastava et al. (2014) Dropout | Regularização |

### 8.3 Notas de leitura

_Espaço para insights do grupo conforme leem os papers._

---

## 9. Dados (referência rápida)

| Recurso | Caminho |
|---|---|
| CSV índice | `data/raw/licitacoes2025.csv` |
| HTML bruto | `data/raw/detalhes/` (423) |
| Corpus PLN | `data/processed/licitacoes_corpus.jsonl` |
| Manifestos | `detalhes/manifest.json`, `preprocess_manifest.json` |

Campos principais do JSONL: `texto`, `objeto_html`, `orgao_csv`, `tipo`, `modalidade`, `total_homologado`.

### Volume: é suficiente?

**Sim, para o escopo do trabalho** (classificação em 6 áreas + sumarização em amostra). **Não** é um corpus grande para deep learning — esperar F1 irregular em classes pequenas (Educação ~17, Infra ~24) e documentar isso na discussão.

| Pergunta | Resposta curta |
|---|---|
| 423 editais bastam? | Sim, com baseline + BERT e limitações explícitas |
| Precisa de 2021–2024? | Não obrigatório; melhoraria robustez, não bloqueia entrega |
| GPU 4090 local vs Databricks? | 4090 local — corpus pequeno, treino rápido, sem custo cloud |

Análise completa (split por classe, comparativo temporal, infra): [`DATA-COLLECTION-DECISIONS.md` §6](DATA-COLLECTION-DECISIONS.md#6-análise-de-volume-de-dados-adequação).

Detalhes de coleta e CAPTCHA: [`DATA-COLLECTION-DECISIONS.md`](DATA-COLLECTION-DECISIONS.md).

---

## 10. Repositório

```
deep-learning-pln-project/
├── configs/              # YAML de hiperparâmetros
├── data/
│   ├── raw/              # CSV + HTML
│   ├── interim/          # textos e records extraídos
│   └── processed/        # corpus JSONL + labels
├── docs/                 # documentação (+ model_card, métricas)
├── experiments/          # JSON por run + mlflow.db (tracking local)
├── models/               # checkpoints (gitignored)
├── notebooks/            # EDA (`01_eda`) + entrega integrada SVM+PTT5
├── reports/figures|slides/
├── scripts/
│   ├── run_collect.py
│   ├── run_preprocess.py
│   └── run_train.py
├── src/                  # collect, preprocess, models, train, evaluate
├── tests/                # pytest (+ fixtures/minimal_corpus.jsonl)
├── pyproject.toml        # deps, ruff, mypy, pytest
└── Makefile              # atalhos de dev e pipeline
```

### Como executar

```bash
python -m venv .venv && source .venv/Scripts/activate
pip install -r requirements-dev.txt   # runtime + pytest, ruff, mypy

python scripts/run_collect.py       # já executado
python scripts/run_preprocess.py    # já executado
python scripts/run_train.py --task classification --model baseline
python scripts/run_train.py --task classification --model bertimbau
python scripts/run_train.py --task summarization --model extractive
```

Atalhos equivalentes: `make train-baseline`, `make train-summarize`, `make mlflow-ui` (requer `make` no PATH).

### Qualidade de código

Antes de commitar alterações em `src/`:

```bash
ruff check src tests && ruff format --check src tests
mypy
pytest
```

| Ferramenta | Escopo | Config |
|---|---|---|
| Ruff | estilo, imports, formatação | `pyproject.toml` → `[tool.ruff]` |
| Mypy | tipos estáticos | `pyproject.toml` → `[tool.mypy]` |
| Pytest | regressão rápida | `tests/`; corpus real opcional (`skipif`) |

Documentação de resultados: [`model_card.md`](model_card.md), [`metricas_e_decisoes.md`](metricas_e_decisoes.md).

### Rastreamento de experimentos (MLflow)

Implementado em [`src/utils/experiment_tracking.py`](../src/utils/experiment_tracking.py) e chamado por `train_classification` / `run_summarization`.

**O que cada run registra**

| Campo | JSON (`experiments/*.json`) | MLflow (`experiments/mlflow.db`) |
|---|---|---|
| Parâmetros do modelo | `params` | `log_param` |
| Métricas (val/teste) | `metrics` | `log_metric` |
| Versão do dataset | `dataset.sha256`, `n_records`, `path` | tags `corpus_*` |
| Código | `git_commit` | tag `git_commit` |
| Artefatos | caminhos relativos | modelo, figuras, JSON da run |

**Por que os dois formatos?**

- **JSON** — portátil, legível no Git, suficiente para o relatório e slides.
- **MLflow** — compara runs lado a lado na UI; essencial na Fase 2 (BERTimbau) com vários hiperparâmetros.

**Comandos**

```bash
python scripts/run_train.py --task classification --model baseline

# UI local (após pelo menos uma run)
mlflow ui --backend-store-uri sqlite:///experiments/mlflow.db
# http://127.0.0.1:5000 — experimento "pln-licitacoes"
```

`experiments/mlflow.db` e `experiments/mlartifacts/` estão no `.gitignore` (gerados localmente). Os JSONs em `experiments/` podem ser commitados quando forem runs de referência.

**BERTimbau (Fase 2):** ao implementar o fine-tuning, usar o callback `MLflowCallback` do Hugging Face `Trainer` no mesmo tracking URI, para logar `loss` por época automaticamente.

---

## 11. Apresentação (10 minutos)

| Min | Slide | Conteúdo |
|---|---|---|
| 0–1 | Problema | Edital é inacessível; DF 2025; 423 licitações |
| 1–2 | Dados | ComprasNet, HTML sem CAPTCHA, corpus JSONL |
| 2–3 | Metodologia | Guia universal: baseline → BERT + resumo cidadã |
| 3–5 | Resultados classificação | F1, matriz de confusão, baseline vs BERT |
| 5–6 | Demo sumarização | 1 edital antes/depois ao vivo |
| 6–7 | Impacto aplicado | Área + valor homologado; quem se beneficia |
| 7–8 | Limitações | Label proxy, HTML vs PDF, amostra pequena |
| 8–9 | Conclusão | O que aprendemos; contribuição |
| 9–10 | Próximos passos | PDF, PNCP, deploy |

**Mensagem principal (1 frase):** _"PLN pode classificar gastos públicos e traduzir editais para a linguagem do cidadão — com limites que precisamos reconhecer."_

---

## 12. Cronograma sugerido

| Semana | Foco |
|---|---|
| 1 | Labels + baseline TF-IDF + início bibliografia |
| 2 | Fine-tuning BERTimbau + análise de erros |
| 3 | Sumarização (baseline + modelo) + avaliação humana |
| 4 | Gráficos, slides, redação, ensaio |

_Ajustar datas conforme calendário real da disciplina._

---

## 13. Log de decisões

| Data | Decisão | Motivo |
|---|---|---|
| 2026-06-06 | Tema: PLN em licitações ComprasNet DF 2025 | Setor público + dados inéditos |
| 2026-06-06 | Coleta HTML (não PDF) | Sem CAPTCHA; reprodutível |
| 2026-06-06 | Corpus JSONL pronto (423 registros) | Pipeline preprocess |
| 2026-06-06 | **Ideia 1 principal + Ideia 4 complemento** | Métricas sólidas + impacto na apresentação |
| 2026-06-06 | Labels via mapeamento órgão → macroárea | Viável no prazo; validação amostral |
| 2026-06-06 | Volume 423 (2025) suficiente; sem coleta 2021–2024 na fase 1 | Prazo + limitações documentadas |
| 2026-06-08 | Fase 1 implementada: labels (6 áreas) + split estratificado 70/15/15 (seed 42) + baseline TF-IDF/LogReg | Pipeline `run_train.py` funcional; métricas reais |
| 2026-06-08 | Entrada honesta = `objeto_html` (não `texto`) | `texto` repete o nome do órgão → vazamento de label (§6.1) |
| 2026-06-08 | EDA em `notebooks/01_eda.ipynb` | Vazamento quantificado: órgão em 97% dos `texto` vs 49% dos `objeto_html` |
| 2026-06-08 | Baseline de sumarização = extrativo por regras (não TextRank puro) | Determinístico, não alucina; cobre objeto/quem/prazo/valor (§7) |
| 2026-06-18 | Rastreamento com MLflow local + JSON | Comparar baseline vs BERTimbau; versionar corpus por hash SHA-256 |
| 2026-06-18 | Dev: ruff + mypy + pytest + Makefile + `pyproject.toml` instalável | Qualidade de código e onboarding do grupo; model card e doc de métricas |
| 2026-06-22 | Validação manual de labels: **4/4 fichas**; média ≈83,2% | Consolidação em `validacao_labels.md` § Síntese |
| 2026-06-23 | Fase 2 BERTimbau — run GPU `222508`; F1 teste ≈0,52 | Documentado em `FASE2-CLASSIFICACAO.md`; abaixo do baseline |
| 2026-06-18 | Notebook de entrega TF-IDF+SVM+PTT5 com anti-vazamento | Trilha integrada para apresentação; ver `NOTEBOOK-ENTREGA.md` |

---

## 14. Notas livres

_Espaço do grupo: dúvidas pro professor, links úteis, resultados de experimentos._

---

*Documento vivo — atualizar conforme experimentos avançam.*
