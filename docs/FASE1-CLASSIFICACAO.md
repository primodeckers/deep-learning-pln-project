# Fase 1 — Classificação baseline (TF-IDF + LogReg)

Documento técnico da **Fase 1** do pipeline de classificação. Serve para o relatório, slides e onboarding do grupo: explica **o que** foi feito, **por que** cada escolha foi tomada e **onde** está no código.

> Métricas e anti-leakage: [`metricas_e_decisoes.md`](metricas_e_decisoes.md)  
> Performance consolidada: [`model_card.md`](model_card.md)  
> Guia metodológico geral: [`UNIVERSAL-DEEP-LEARNING-GUIDE.md`](UNIVERSAL-DEEP-LEARNING-GUIDE.md) §6

---

## 1. Objetivo da fase

Estabelecer uma **linha de base reprodutível** para classificar editais em **6 macroáreas de gasto público**, antes de comparar com BERTimbau (Fase 2).

| Critério de sucesso | Como medimos |
|---------------------|--------------|
| Pipeline executável por script | `python scripts/run_train.py --task classification --model baseline` |
| Avaliação honesta (sem vazamento de label) | Entrada = `objeto_html`, não `texto` |
| Métrica principal reportável | F1 macro no **conjunto de teste** |
| Comparabilidade futura | Mesmo split (`seed=42`, 70/15/15) para baseline e BERT |

**Resultado de referência:** F1 macro ≈ **0,74** no teste (`experiments/classification_baseline_20260608-190839.json`).

---

## 2. Fluxo do pipeline

```
licitacoes_corpus.jsonl
        │
        ▼
  load_records()          ← anexa label `area` a partir de orgao_csv
        │
        ▼
  make_dataset()          ← split estratificado 70/15/15
        │
        ▼
  build_baseline()        ← Pipeline sklearn (TF-IDF → LogReg)
        │
        ▼
  fit / predict           ← treino só no train; métricas em val e test
        │
        ▼
  compute_metrics()       ← F1 macro, por classe, matriz de confusão
        │
        ▼
  experiments/*.json      ← registro portátil + MLflow local
  models/*.joblib
  reports/figures/*_confusion.png
```

---

## 3. Decisões de dados e labels

### 3.1 Label proxy: órgão → macroárea

| Decisão | Justificativa |
|---------|---------------|
| Label derivado de `orgao_csv`, não anotação manual por edital | Viável no prazo; corpus de 423 editais; taxonomia alinhada ao gasto público do DF |
| Modelo **não** recebe `orgao_csv` como feature | Senão a tarefa vira lookup do órgão, não PLN sobre o texto |
| 6 macroáreas + `Administracao/Outros` como fallback | Cobre o escopo do trabalho sem explodir granularidade (dezenas de secretarias) |
| Palavras-chave com ordem fixa | Primeiro match vence — ex.: "Secretaria de Educação" não cai em Saúde |

**Limitação declarada:** o label é *proxy* — um edital de "material hospitalar" comprado por órgão administrativo pode estar mal rotulado.

**Mitigação — validação manual (30 editais, seed 42):** gabarito e fichas em [`validacao_labels/validacao_labels.md`](validacao_labels/validacao_labels.md). **Status (2026-06-18):** 1/4 fichas concluídas; Renê Estevam Deckers — **96,2%** de concordância (25/26, ignorando ambíguos). Único erro claro: TCDF com insumos odontológicos rotulado como Administração. Conclusão: mapeamento **aceitável** para o escopo, com ressalva documentada.

**Código:** `src/preprocess/labels.py`

### 3.2 Campo de entrada: `objeto_html` (não `texto`)

| Campo | Papel | Problema |
|-------|-------|----------|
| `texto` | HTML completo do edital | Nome do órgão em ~97% dos casos → **vazamento** (F1 macro ≈ 0,88) |
| `objeto_html` | Descrição do objeto da compra | Sem cabeçalho identificador → **F1 macro ≈ 0,74** (honesto) |

**Decisão:** `text_field: objeto_html` em `configs/classification.yaml`.

**Evidência:** EDA em `notebooks/01_eda.ipynb`; discussão em [`metricas_e_decisoes.md`](metricas_e_decisoes.md).

**Código:** `src/preprocess/dataset.py` → `make_dataset(..., text_field=...)`

### 3.3 Split treino / validação / teste

| Parâmetro | Valor | Justificativa |
|-----------|-------|---------------|
| Proporção | 70% / 15% / 15% | Recomendação do guia (§3.1) para corpus ~400 amostras |
| Estratificação | Por `area` | Classes desbalanceadas (Saúde e Administração dominam) |
| `random_state` | 42 | Reprodutibilidade entre integrantes e entre baseline vs BERT |
| Dois cortes sequenciais | `test` primeiro, depois `val` no restante | Padrão sklearn quando se quer três conjuntos com `train_test_split` |

**Código:** `src/preprocess/dataset.py` → `make_dataset()`

---

## 4. Decisões de modelagem (baseline clássico)

### 4.1 Por que TF-IDF + Regressão Logística?

| Alternativa | Por que não (agora) |
|-------------|---------------------|
| Apenas bag-of-words / contagem | TF-IDF penaliza termos frequentes em todo o corpus |
| Random Forest / SVM | LogReg é interpretável, rápida, baseline padrão em NLP clássico |
| BERTimbau direto | Fase 2; precisamos de referência clássica para comparar ganho do Transformer |
| Rede neural do zero | Corpus pequeno (~423); alto risco de overfitting sem transfer learning |

**Referência metodológica:** guia universal §6.3; material de aula (`aula03-04.pdf`) — começar simples, diagnosticar, depois complexificar.

**Código:** `src/models/baseline_tfidf.py`

### 4.2 Hiperparâmetros e técnicas do vetorizador

| Parâmetro | Valor | Justificativa |
|-----------|-------|---------------|
| `ngram_range` (1, 2) | Bigramas capturam expressões ("pregão eletrônico", "material hospitalar") | |
| `min_df=2` | Ignora hapax legomena (ruído em corpus pequeno) | |
| `max_features=20000` | Teto de vocabulário — evita matriz esparsa gigante | |
| `sublinear_tf=True` | Suaviza termos muito frequentes (log TF) | |
| `strip_accents="unicode"` | "Saúde" e "saude" unificados — importante em PT-BR | |
| Stopwords PT **mínimas** | Lista curta e **sem acento** | Termos de domínio ("secretaria", "edital") são sinais; stopwords genéricas só |

### 4.3 Hiperparâmetros do classificador

| Parâmetro | Valor | Justificativa |
|-----------|-------|---------------|
| `class_weight='balanced'` | Pesa classes inversamente à frequência | Mitiga desbalanceamento sem oversampling artificial |
| `C=1.0` | Regularização padrão L2 | Ponto de partida; tuning fino opcional na Fase 2 |
| `max_iter=1000` | Convergência em features esparsas de alta dimensão | |
| `random_state=42` | Reprodutibilidade da LogReg (onde aplicável) | |

**Config externa:** `configs/classification.yaml` — separa hiperparâmetros do código (padrão do projeto).

---

## 5. Decisões de avaliação

| Decisão | Justificativa |
|---------|---------------|
| **F1 macro** como métrica primária | Trata classes minoritárias (Educação, Infra) com mesmo peso que majoritárias |
| Accuracy e F1 weighted como secundárias | Accuracy mascara falhas em classes pequenas; weighted favorece frequentes |
| `zero_division=0` | Classe ausente no fold não quebra o pipeline |
| Matriz de confusão no **teste** | Seleção de modelo pode olhar val; relatório final reporta test |
| Figura PNG da matriz | Entrega visual para slides (`reports/figures/`) |

**Código:** `src/evaluate/metrics_classification.py`

---

## 6. Padrões de código adotados

| Padrão | Onde | Motivo |
|--------|------|--------|
| **Separação por etapa** | `src/preprocess/`, `src/models/`, `src/train/`, `src/evaluate/` | Pipeline legível; cada módulo com uma responsabilidade |
| **Config YAML** | `configs/classification.yaml` | Hiperparâmetros versionados sem alterar código |
| **Dataclasses** (`Split`, `Dataset`) | `dataset.py` | Contrato claro entre texto, label e id |
| **sklearn Pipeline** | `baseline_tfidf.py` | TF-IDF fit só no treino; mesma transformação em val/test |
| **Registro de experimento JSON** | `train_classification.py` | Reprodutibilidade e diff entre runs no Git |
| **Caminhos relativos no JSON** | `_rel()` em `train_classification.py` | Artefatos portáveis entre máquinas |
| **Docstrings em português** | Todo `src/` | Grupo e avaliador brasileiros; termos técnicos em inglês quando padrão (TF-IDF, F1) |

**O que evitamos:** comentar o óbvio (`# importa json`); comentários ficam em decisões não triviais (stopwords, split em dois passos, filtro de params por modelo).

---

## 7. Mapa código ↔ responsabilidade

| Arquivo | Responsabilidade | Decisões documentadas |
|---------|------------------|------------------------|
| `src/preprocess/labels.py` | Taxonomia e mapeamento órgão → área | §3.1 |
| `src/preprocess/dataset.py` | Carga JSONL + split estratificado | §3.2, §3.3 |
| `src/models/baseline_tfidf.py` | Pipeline TF-IDF + LogReg | §4 |
| `src/evaluate/metrics_classification.py` | Métricas e figuras | §5 |
| `src/train/train_classification.py` | Orquestração treino → artefatos | §2, §6 |
| `configs/classification.yaml` | Hiperparâmetros e `text_field` | §3.2, §4 |
| `scripts/run_train.py` | CLI de entrada | — |

---

## 8. Como reproduzir

```bash
source .venv/Scripts/activate
pip install -r requirements-dev.txt

# garantir corpus processado
python scripts/run_preprocess.py

# treinar baseline (usa configs/classification.yaml por padrão)
python scripts/run_train.py --task classification --model baseline

# ou explicitamente
python scripts/run_train.py --task classification --config configs/classification.yaml
```

**Saídas esperadas:**

- `models/classification_baseline_<timestamp>.joblib`
- `experiments/classification_baseline_<timestamp>.json`
- `reports/figures/classification_baseline_<timestamp>_confusion.png`

---

## 9. Limitações conhecidas (para discussão no relatório)

1. **Corpus pequeno** (~423) para deep learning — classes raras têm F1 instável.
2. **Label proxy** — qualidade depende do mapeamento por palavra-chave, não de anotação por edital.
3. **Baseline bag-of-words** — não captura ordem longa nem contexto semântico profundo (motivo da Fase 2).
4. **Só HTML ComprasNet DF 2025** — não generaliza para outros estados ou PDF com CAPTCHA.
5. **Validação manual de 30 labels** — [`validacao_labels/validacao_labels.md`](validacao_labels/validacao_labels.md); `python scripts/export_validacao_sample.py`

---

## 10. Checklist de documentação da Fase 1

Use este checklist antes de considerar a fase fechada para entrega:

- [x] Pipeline executável e documentado no README
- [x] Decisão `objeto_html` justificada (EDA + métricas)
- [x] Hiperparâmetros em YAML comentados
- [x] Model card e doc de métricas
- [x] Este documento (`FASE1-CLASSIFICACAO.md`)
- [x] Template de validação manual (`validacao_labels/validacao_labels.md` + 4 fichas)
- [ ] Quatro fichas preenchidas + consolidação final no gabarito _(1/4 — Renê concluída; ver consolidação parcial no gabarito)_
- [ ] Tabela F1 por classe copiada para slides
- [ ] 5+ referências bibliográficas citando TF-IDF, métricas multiclasse e domínio público

---

## 11. Próximo passo (Fase 2)

Mesmo split e `text_field`; substituir `build_baseline()` por fine-tuning de `neuralmind/bert-base-portuguese-cased`. Comparar tabela baseline vs BERT no `model_card.md` e nos slides.
