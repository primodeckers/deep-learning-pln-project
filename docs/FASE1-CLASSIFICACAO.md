# Fase 1 — Classificação baseline (TF-IDF + LogReg)

Notas da Fase 1: o que implementamos, por que fizemos assim, e onde está no código. É o modelo que o grupo leva pro relatório como principal.

> Métricas de treino: [`METRICAS-E-DECISOES.md`](METRICAS-E-DECISOES.md) · Val vs teste (3 fases): [`COMPARATIVO-FASES.md`](COMPARATIVO-FASES.md)  
> Números do run: [`MODEL-CARD.md`](MODEL-CARD.md) · Regras PNCP: [`REGRAS-E-PROTOCOLOS.md`](REGRAS-E-PROTOCOLOS.md) · EDA PNCP DF: [`03_eda_pncp.ipynb`](../notebooks/03_eda_pncp.ipynb)  
> Guia: [`UNIVERSAL-DEEP-LEARNING-GUIDE.md`](UNIVERSAL-DEEP-LEARNING-GUIDE.md) §6

---

## 1. Objetivo da fase

Montar um baseline clássico reprodutível — classificar editais/compras em **6 macroáreas de gasto** — antes de testar BERT (Fase 2) e SVM (Fase 3).

Na prática precisávamos de:

- Script que qualquer um do grupo roda: `make train-baseline`
- Avaliação sem “colar” no nome do órgão → entrada `objeto_html` (corpus ComprasNet), não `texto`
- F1 macro no **teste** como número do relatório
- Mesmo split (`seed=42`, 70/15/15) pros comparativos depois

**Resultado oficial (corpus ComprasNet HTML):** F1 macro ≈ **0,74** no teste (`classification_baseline_20260624-013836`). Validação ficou em 0,743 — praticamente igual.

**Contexto de dados (PNCP DF/2025):** o EDA em [`03_eda_pncp.ipynb`](../notebooks/03_eda_pncp.ipynb) mostra **~19.944** compras no DF com o mesmo mapeamento órgão→área — escala ~47× maior que o corpus de treino (423). O treino da Fase 1 continua no corpus HTML; o PNCP orienta decisões de label, desbalanceamento e vazamento.

---

## 2. Fluxo do pipeline (treino oficial)

```
licitacoes_corpus.jsonl          ← 423 editais DF/2025 (HTML ComprasNet)
        │
        ▼
  load_records()                 ← anexa label `area` a partir de orgao_csv
        │
        ▼
  make_dataset()                 ← split estratificado 70/15/15
        │
        ▼
  build_baseline()               ← Pipeline sklearn (TF-IDF → LogReg)
        │
        ▼
  fit / predict                  ← treino só no train; métricas em val e test
        │
        ▼
  compute_metrics()              ← F1 macro, por classe, matriz de confusão
        │
        ▼
  experiments/*.json             ← registro portátil + MLflow local
  models/*.joblib
  reports/figures/*_confusion.png
```

**Fonte complementar (só EDA, ainda não no treino):** `data/comprasGOV-anual-VW_FT_PNCP_COMPRA-2025.xls` — CSV UTF-8, filtrado `UF=DF` e `ano=2025`.

---

## 3. Decisões de dados e labels

### 3.0 Duas fontes, mesmo label proxy

| Fonte | Registros | Texto para PLN | Uso na Fase 1 |
|-------|----------:|----------------|---------------|
| **Corpus ComprasNet** (`licitacoes_corpus.jsonl`) | **423** | `objeto_html` (HTML do objeto) | **Treino e avaliação oficial** |
| **PNCP DF/2025** (`comprasGOV-anual-VW_FT_PNCP_COMPRA-2025.xls`) | **19.944** | `objeto_compra` (resumo curto) | **EDA** — perfil, vazamento, escala |

Ambos usam a mesma taxonomia em `src/preprocess/labels.py`: palavras-chave no **nome do órgão** → macroárea. No PNCP o campo é `orgao_entidade_razao_social`; no corpus, `orgao_csv`.

### 3.1 Label proxy: órgão → macroárea

Não tínhamos tempo de rotular edital por edital na mão. O label vem do órgão comprador; quem não casa com keyword cai em `Administracao/Outros`.

Importante: o modelo **não** recebe o órgão como feature — só o texto. Se recebesse, viraria lookup, não PLN.

**Distribuição no PNCP DF/2025** (Tabela 2 do EDA PNCP):

| Macroárea | N compras | % |
|-----------|----------:|--:|
| Administração/Outros | 16.471 | 82,6% |
| Saúde | 1.428 | 7,2% |
| Segurança | 1.164 | 5,8% |
| Infraestrutura/Obras | 333 | 1,7% |
| Educação | 260 | 1,3% |
| Saneamento | 288 | 1,4% |

**215 órgãos distintos** no recorte DF. O desbalanceamento é **estrutural** — não é artefato dos 423 editais do HTML. Com ~20 mil registros, Saúde e Segurança ganham volume, mas Administração/Outros continua dominante.

**Validação manual (corpus ComprasNet):** 30 editais sorteados; concordância média com o proxy ≈ **83%**. Detalhe: [`VALIDACAO-LABELS/VALIDACAO-LABELS.md`](VALIDACAO-LABELS/VALIDACAO-LABELS.md).

**Código:** `src/preprocess/labels.py`

### 3.2 Campo de entrada: objeto isolado (não texto completo)

#### Corpus ComprasNet (treino)

No [`01_eda.ipynb`](../notebooks/01_eda.ipynb), o HTML completo (`texto`) traz o órgão em ~97% dos casos — e o label vem do órgão. Com `texto`, F1 macro ≈ **0,88** (inflado); com `objeto_html`, ≈ **0,74** (honesto).

Config: `text_field: objeto_html` em `configs/classification.yaml`.

#### PNCP DF/2025 (EDA)

No PNCP, `objeto_compra` é **metadado curto** — mediana **32 palavras** (máx. 349; **0** compras acima de 512 palavras). O “texto completo” montado no EDA (órgão + unidade + objeto + complemento) tem mediana **53 palavras** — muito menor que o HTML do ComprasNet (~239 palavras no corpus).

**Vazamento de label no PNCP DF** (3.473 compras com keyword; exclui Admin/Outros):

| Campo analisado | Taxa de vazamento |
|-----------------|------------------:|
| texto (órgão + objeto + complemento) | **100,0%** |
| objeto_compra (só objeto) | **50,6%** |
| objeto_limpo (`limpar_objeto()`) | **48,7%** |

**Vazamento residual:** nome do órgão ainda aparece em `objeto_compra` em **2.185 / 19.944** compras (**11,0%**).

Conclusão para a Fase 1: a regra “**não usar texto que repete o órgão**” vale nos dois mundos. No corpus HTML usamos `objeto_html`; num pipeline futuro sobre PNCP, `objeto_compra` seria a entrada honesta (com taxa de vazamento documentada).

Discussão longa: [`VAZAMENTO-DE-LABEL.md`](VAZAMENTO-DE-LABEL.md).

**Código:** `src/preprocess/dataset.py` · `src/preprocess/clean_objeto.py`

### 3.3 Modalidade e perfil do DF (PNCP)

No PNCP DF/2025, o mix de procedimentos **diferente** do export ComprasNet usado no corpus HTML:

| Modalidade (PNCP DF) | N | % |
|----------------------|---:|--:|
| Inexigibilidade | 7.744 | 38,8% |
| Dispensa | 6.452 | 32,4% |
| Pregão Eletrônico | 5.269 | 26,4% |
| Concorrência Eletrônica | 278 | 1,4% |
| Credenciamento | 144 | 0,7% |

No corpus ComprasNet (423), **pregão** domina (~66%). Isso explica parte da diferença de escala: o PNCP inclui muitas compras diretas (dispensa/inexigibilidade) que não entraram no pipeline HTML.

### 3.4 Valor homologado por macroárea (PNCP DF)

Referência financeira do EDA PNCP (compras com valor homologado > 0):

| Macroárea | N c/ valor | Mediana (R$) |
|-----------|----------:|-------------:|
| Saúde | 1.163 | ~110.575 |
| Saneamento | 213 | ~432.439 |
| Segurança | 1.013 | ~38.921 |
| Educação | 198 | ~80.000 |
| Infraestrutura/Obras | 283 | ~24.600 |
| Administração/Outros | 14.241 | ~17.713 |

Saúde e Administração/Outros concentram volume absoluto; medianas por área ajudam a discutir gasto típico sem outliers.

### 3.5 Split treino / validação / teste (corpus oficial)

70% treino, 15% val, 15% teste — estratificado por `area`, `random_state=42`. Com **423** editais: **295 / 64 / 64**.

Se o mesmo protocolo fosse aplicado ao PNCP DF (~19.944), o split seria ~**13.961 / 2.992 / 2.991** — classes raras (Educação, Infra) teriam centenas de exemplos no treino em vez de dezenas.

**Código:** `src/preprocess/dataset.py`

---

## 4. Decisões de modelagem (baseline clássico)

### 4.1 Por que TF-IDF + Regressão Logística?

Começamos pelo que a aula recomenda: simples, interpretável, baseline forte em texto curto com poucos dados. TF-IDF + LogReg virou nossa referência; depois testamos SVM (Fase 3) e BERT (Fase 2) no mesmo protocolo.

O EDA PNCP reforça: com desbalanceamento forte e textos curtos, um baseline linear bem regularizado é ponto de partida sensato antes de Transformers — especialmente enquanto o treino oficial tem só 423 exemplos HTML.

**Código:** `src/models/baseline_tfidf.py`

### 4.2 Hiperparâmetros do vetorizador

| Parâmetro | Valor | Justificativa |
|-----------|-------|---------------|
| `ngram_range` (1, 2) | Bigramas ("pregão eletrônico", "material hospitalar") | |
| `min_df=2` | Ignora hapax legomena | |
| `max_features=20000` | Teto de vocabulário | |
| `sublinear_tf=True` | Suaviza termos muito frequentes | |
| `strip_accents="unicode"` | Unifica acentos em PT-BR | |
| Stopwords PT **mínimas** | Lista curta, sem acento | Termos de domínio ("secretaria", "edital") são sinais |

### 4.3 Hiperparâmetros do classificador

| Parâmetro | Valor | Justificativa |
|-----------|-------|---------------|
| `class_weight='balanced'` | Pesa classes inversamente à frequência | **Obrigatório** — EDA PNCP confirma ~83% Admin/Outros no DF |
| `C=1.0` | Regularização L2 padrão | |
| `max_iter=1000` | Convergência em features esparsas | |
| `random_state=42` | Reprodutibilidade | |

**Config:** `configs/classification.yaml`

---

## 5. Métricas consolidadas e explicação

Tudo que medimos, em um lugar. **Treino oficial** = corpus ComprasNet HTML (423). **EDA PNCP** = contexto de escala no DF (19.944) — ainda não treinamos classificador em cima dele.

### 5.1 Glossário (como ler os números)

| Métrica | O que é | Por que usamos |
|---------|---------|----------------|
| **F1 macro** | Média do F1 das 6 áreas, **peso igual** | Métrica **principal** — se o modelo ignora Educação, a nota cai |
| **Accuracy** | % de acertos no total | Contexto — pode esconder erro em classe rara |
| **F1 por classe** | Desempenho em **uma** macroárea | Diagnóstico — onde o modelo falha |
| **Support** | Quantos exemplos da classe no conjunto | Abaixo de 5 no teste = número **instável** |
| **Vazamento de label** | Texto repete pista do órgão (origem do label) | Quanto maior, mais “inflada” a métrica |
| **Val / teste** | 64 editais cada; modelo **não** treina neles | Val = desenvolvimento; **teste** = número do relatório |

**F1 de uma classe** equilibra precisão e recall. **F1 macro** não deixa o modelo “passar de ano” só acertando Administração/Outros.

---

### 5.2 Bloco A — Perfil dos dados

| Fonte | N | Entrada de texto | Papel |
|-------|--:|------------------|-------|
| Corpus ComprasNet (`licitacoes_corpus.jsonl`) | **423** | `objeto_html` (~239 palavras mediana) | **Treino + avaliação** |
| PNCP DF/2025 (`comprasGOV-anual-…xls`) | **19.944** | `objeto_compra` (~32 palavras mediana) | **EDA** |

**Distribuição de labels — corpus 423 (treino):**

| Macroárea | N | % |
|-----------|--:|--:|
| Administração/Outros | 163 | 38,5% |
| Saúde | 112 | 26,5% |
| Segurança | 58 | 13,7% |
| Saneamento | 49 | 11,6% |
| Infraestrutura/Obras | 24 | 5,7% |
| Educação | 17 | 4,0% |

**Distribuição de labels — PNCP DF/2025 (EDA):**

| Macroárea | N | % |
|-----------|--:|--:|
| Administração/Outros | 16.471 | 82,6% |
| Saúde | 1.428 | 7,2% |
| Segurança | 1.164 | 5,8% |
| Infraestrutura/Obras | 333 | 1,7% |
| Educação | 260 | 1,3% |
| Saneamento | 288 | 1,4% |

**Leitura:** no PNCP o desbalanceamento é **pior** (83% Admin/Outros), mas Saúde e Segurança têm **muito mais** exemplos. O corpus HTML é mais equilibrado porque veio sobretudo de **pregões** exportados no ComprasNet, não de dispensa/inexigibilidade.

**Label proxy:** concordância humana ≈ **83%** em amostra de 30 editais ([`VALIDACAO-LABELS/VALIDACAO-LABELS.md`](VALIDACAO-LABELS/VALIDACAO-LABELS.md)).

---

### 5.3 Bloco B — Vazamento de label (por que não usamos `texto` completo)

O label vem do **órgão**. Se o texto repete o órgão, o modelo “cola” no label sem ler o objeto da compra.

**Corpus ComprasNet** (260 editais com keyword; exclui Admin/Outros):

| Campo | Taxa de vazamento |
|-------|------------------:|
| `texto` (HTML completo) | **96,9%** |
| **`objeto_html`** (oficial) | **49,2%** |
| `objeto_html_limpo` | 47,3% |

**PNCP DF/2025** (3.473 compras com keyword):

| Campo | Taxa de vazamento |
|-------|------------------:|
| texto (órgão + objeto + complemento) | **100,0%** |
| **`objeto_compra`** | **50,6%** |
| objeto_limpo | 48,7% |
| Nome do órgão dentro de `objeto_compra` (residual) | **11,0%** (2.185/19.944) |

**Leitura:** usar só o **objeto** corta o vazamento pela metade. Ainda há ~50% de pista lexical (ex.: “insumo à saúde”). Por isso F1 ≈ **0,74** é “honesto”; com `texto` seria ≈ **0,88** (inflado).

---

### 5.4 Bloco C — Desempenho dos classificadores (corpus 423, teste = 64 editais)

Protocolo: `objeto_html`, split 70/15/15, `seed=42`. Runs `20260624-*`.

#### Tabela principal (F1 macro no teste)

| Modelo | F1 val | F1 **teste** | Accuracy teste | Veredicto |
|--------|-------:|-------------:|---------------:|-----------|
| **TF-IDF + LogReg** | 0,743 | **0,740** | 0,797 | **Escolhido** — estável val≈teste |
| TF-IDF + SVM | 0,797 | 0,652 | 0,797 | Overfitting na val (−0,15 no teste) |
| BERTimbau | 0,559 | 0,400 | 0,688 | Pouco treino; colapsa classes raras |

#### F1 por classe no teste — LogReg (modelo reportado)

| Macroárea | Support | F1 teste | Interpretação |
|-----------|--------:|---------:|-----------------|
| Saneamento | 7 | **1,00** | Acertou todos |
| Saúde | 17 | **0,90** | Muito bom |
| Administração/Outros | 25 | **0,81** | Bom (classe maior) |
| Educação | 2 | 0,67 | Só 2 editais — **instável** |
| Infraestrutura/Obras | 4 | 0,60 | Poucos exemplos |
| Segurança | 9 | **0,46** | Pior área — confunde com Saúde/Admin |

#### Por que o SVM “enganou” na validação?

Mesma accuracy no teste (~80%), mas F1 macro caiu de **0,80 → 0,65**. Ele acertou a **classe grande** e errou mais as **pequenas** — a accuracy esconde isso; o F1 macro não.

#### Por que o BERT perdeu?

~295 editais de treino vs milhões de parâmetros. No teste, **Segurança, Educação e Infra = F1 0** — empurrou tudo para Administração/Outros.

---

### 5.5 Bloco D — Sumarização extrativa (tarefa separada, Fase 4)

Amostra: **18** editais estratificados. Não usa F1.

| Campo extraído | Resultado |
|----------------|-----------|
| Prazo de entrega | **15/18** (83%) |
| Valor homologado | **18/18** (100%) |

Extrai campos do HTML; não reescreve o edital (não alucina, mas também não parafraseia).

---

### 5.6 Conclusões em uma frase cada

1. **Dados:** 423 editais HTML para treinar; PNCP DF confirma desbalanceamento e mostra escala ~47× maior.
2. **Entrada:** `objeto_html` porque vazamento cai de ~97% para ~49%.
3. **Modelo:** LogReg com F1 **0,74** no teste — único estável entre os três classificadores.
4. **Limite:** Segurança (F1 0,46) e classes com support ≤ 4 no teste.
5. **Próximo passo:** retreinar no PNCP DF com `objeto_compra` e split 70/15/15 (~14k treino).

Detalhe ampliado: [`METRICAS-E-DECISOES.md`](METRICAS-E-DECISOES.md) · [`COMPARATIVO-FASES.md`](COMPARATIVO-FASES.md) · [`MODEL-CARD.md`](MODEL-CARD.md)

**Código:** `src/evaluate/metrics_classification.py`

---

## 6. Padrões de código adotados

| Padrão | Onde | Motivo |
|--------|------|--------|
| Separação por etapa | `src/preprocess/`, `src/models/`, `src/train/`, `src/evaluate/` | Pipeline legível |
| Config YAML | `configs/classification.yaml` | Hiperparâmetros versionados |
| Dataclasses (`Split`, `Dataset`) | `dataset.py` | Contrato texto / label / id |
| sklearn Pipeline | `baseline_tfidf.py` | TF-IDF fit só no treino |
| Registro JSON + MLflow | `train_classification.py` | Reprodutibilidade |
| Docstrings em português | `src/` | Grupo e avaliador BR |

---

## 7. Mapa código ↔ responsabilidade

| Arquivo | Responsabilidade |
|---------|------------------|
| `src/preprocess/labels.py` | Taxonomia órgão → área (ComprasNet e PNCP) |
| `src/preprocess/dataset.py` | Carga JSONL + split estratificado |
| `src/models/baseline_tfidf.py` | Pipeline TF-IDF + LogReg |
| `src/evaluate/metrics_classification.py` | Métricas e figuras |
| `src/train/train_classification.py` | Orquestração treino → artefatos |
| `configs/classification.yaml` | Hiperparâmetros e `text_field` |
| `scripts/run_train.py` | CLI |
| `notebooks/03_eda_pncp.ipynb` | EDA PNCP DF/2025 (não treina) |

---

## 8. Como reproduzir

```bash
source .venv/Scripts/activate
pip install -r requirements-dev.txt

# corpus HTML (treino oficial)
python scripts/run_preprocess.py

python scripts/run_train.py --task classification --model baseline

# EDA PNCP DF (exploratório)
jupyter notebook notebooks/03_eda_pncp.ipynb
```

**Saídas do treino:**

- `models/classification_baseline_<timestamp>.joblib`
- `experiments/classification_baseline_<timestamp>.json`
- `reports/figures/classification_baseline_<timestamp>_confusion.png`

---

## 9. Limitações (discussão no relatório)

- **Treino oficial pequeno (423 HTML)** — F1 de classes raras instável; PNCP DF mostra que o problema de escala é real (~20 mil), mas ainda desbalanceado.
- **Label proxy por órgão** — válido em ~83% na amostra manual; PNCP amplia o mesmo viés estrutural.
- **Dois tipos de texto** — `objeto_html` (rico, HTML) vs `objeto_compra` PNCP (curto); comparar F1 entre fontes exige harmonizar entrada.
- **PNCP ≠ edital integral** — metadado PNCP não substitui HTML/PDF para sumarização cidadã.
- **Mix modal** — PNCP DF tem mais dispensa/inexigibilidade que o export ComprasNet.
- **Só DF/2025** — não generaliza para outros estados/anos sem retreino.

Depois das Fases 2 e 3, o LogReg manteve melhor F1 no teste ComprasNet (**0,74**). Comparativo: [`COMPARATIVO-FASES.md`](COMPARATIVO-FASES.md).

---

## 10. Checklist de documentação da Fase 1

- [x] Pipeline executável e documentado no README
- [x] Decisão `objeto_html` justificada (EDA ComprasNet + vazamento)
- [x] EDA PNCP DF integrado ([`03_eda_pncp.ipynb`](../notebooks/03_eda_pncp.ipynb))
- [x] Hiperparâmetros em YAML
- [x] Model card e doc de métricas
- [x] Este documento (`FASE1-CLASSIFICACAO.md`)
- [x] Validação manual 30 editais (4/4 fichas, ≈83%)
- [x] Tabela F1 por classe — [`METRICAS-E-DECISOES.md`](METRICAS-E-DECISOES.md) §6
- [ ] 5+ referências bibliográficas (TF-IDF, métricas multiclasse, domínio público)

---

## 11. Depois da Fase 1

BERT ([`FASE2`](FASE2-CLASSIFICACAO.md)) e SVM ([`FASE3`](FASE3-CLASSIFICACAO.md)) no mesmo split ComprasNet. Nenhum bateu o LogReg no teste.

**Próximo passo sugerido (dados):** cruzar PNCP DF com `licitacoes2025.csv`, enriquecer corpus HTML ou retreinar sobre `objeto_compra` PNCP com split 70/15/15 — ver §8 do EDA PNCP.
