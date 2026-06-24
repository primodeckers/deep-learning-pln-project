# Fase 1 — Classificação baseline (TF-IDF + LogReg)

Notas da Fase 1: o que implementamos, por que fizemos assim, e onde está no código. É o modelo que o grupo leva pro relatório como principal.

> Métricas: [`metricas_e_decisoes.md`](metricas_e_decisoes.md) · Val vs teste (3 fases): [`COMPARATIVO-FASES.md`](COMPARATIVO-FASES.md)  
> Números: [`model_card.md`](model_card.md) · Guia: [`UNIVERSAL-DEEP-LEARNING-GUIDE.md`](UNIVERSAL-DEEP-LEARNING-GUIDE.md) §6

---

## 1. Objetivo da fase

Montar um baseline clássico reprodutível — classificar editais em 6 macroáreas de gasto — antes de testar BERT (Fase 2) e SVM (Fase 3).

Na prática precisávamos de:

- Script que qualquer um do grupo roda: `make train-baseline`
- Avaliação sem “colar” no nome do órgão → entrada `objeto_html`, não `texto`
- F1 macro no **teste** como número do relatório
- Mesmo split (`seed=42`, 70/15/15) pros comparativos depois

**Resultado:** F1 macro ≈ **0,74** no teste (`classification_baseline_20260624-013836`). Validação ficou em 0,743 — praticamente igual, o que nos deu confiança pra usar esse modelo.
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

Não tínhamos tempo de rotular edital por edital na mão. O label vem do `orgao_csv`: palavras-chave no nome do órgão mapeiam pra uma das 6 macroáreas (Saúde, Saneamento, etc.). Quem não casa cai em `Administracao/Outros`.

Importante: o modelo **não** recebe o órgão como feature — só o texto. Se recebesse, virava lookup, não PLN.

Limitação óbvia: um edital de “material hospitalar” comprado por órgão administrativo pode estar com label errado.

**Validação manual:** sorteamos 30 editais (`seed=42`); os quatro integrantes preencheram ficha. Média de concordância com o proxy ≈ **83%** (varia por revisor). Detalhe em [`validacao_labels/validacao_labels.md`](validacao_labels/validacao_labels.md). Conclusão do grupo: dá pra usar como rotulagem fraca, mas citar a limitação no relatório.

**Código:** `src/preprocess/labels.py`
### 3.2 Campo de entrada: `objeto_html` (não `texto`)

No EDA vimos que o HTML completo (`texto`) traz o nome do órgão em quase todos os editais — e o label vem justamente do órgão. Com `texto`, o baseline sobe pra F1 macro ≈ **0,88** no teste; com `objeto_html` (só a descrição do que está sendo comprado) cai pra ≈ **0,74**. Preferimos o número menor e mais honesto.

Config: `text_field: objeto_html` em `configs/classification.yaml`.

Discussão longa (Tabela 7, slides): [`vazamento_de_label.md`](vazamento_de_label.md).

**Código:** `src/preprocess/dataset.py` · limpeza opcional em `clean_objeto.py`
### 3.3 Split treino / validação / teste

70% treino, 15% val, 15% teste — estratificado por `area`, `random_state=42`. Com ~423 editais isso dá 295 / 64 / 64. O guia da disciplina sugere proporção parecida pra corpus desse tamanho.

Dois `train_test_split` em sequência (primeiro separa teste, depois val do resto) — padrão sklearn.

**Código:** `src/preprocess/dataset.py`
---

## 4. Decisões de modelagem (baseline clássico)

### 4.1 Por que TF-IDF + Regressão Logística?

Começamos pelo que a aula recomenda: simples, interpretável, baseline forte em texto curto com poucos dados. TF-IDF + LogReg virou nossa referência; depois testamos SVM (Fase 3) e BERT (Fase 2) no mesmo protocolo.

Não testamos Random Forest nem rede do zero — com 423 editais o risco de overfitting sem transfer learning era alto.

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

## 5. Como avaliamos

Usamos **F1 macro** como métrica principal — trata todas as classes com o mesmo peso, o que importa porque Saúde e Administração dominam o corpus. Accuracy e F1 weighted entram como contexto, mas accuracy sozinha esconde falha em Educação (2 exemplos no teste).

Matriz de confusão e figura PNG saem do conjunto de **teste** (`reports/figures/`). Durante o desenvolvimento olhamos val; no relatório vai teste.

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

## 9. Limitações (discussão no relatório)

- Corpus pequeno (~423) — F1 de classes raras oscila muito.
- Label proxy por órgão, não anotação manual por edital.
- TF-IDF não captura ordem longa nem semântica profunda (motivo de ter testado BERT).
- Só ComprasNet DF 2025 em HTML — não generaliza pra PDF ou outros estados.
- Validação manual em 30 editais — ver [`validacao_labels/`](validacao_labels/validacao_labels.md).

Depois das Fases 2 e 3, o LogReg continuou com melhor F1 no teste (0,74). Comparativo: [`COMPARATIVO-FASES.md`](COMPARATIVO-FASES.md).
---

## 10. Checklist de documentação da Fase 1

Use este checklist antes de considerar a fase fechada para entrega:

- [x] Pipeline executável e documentado no README
- [x] Decisão `objeto_html` justificada (EDA + métricas)
- [x] Hiperparâmetros em YAML comentados
- [x] Model card e doc de métricas
- [x] Este documento (`FASE1-CLASSIFICACAO.md`)
- [x] Template de validação manual (`validacao_labels/validacao_labels.md` + 4 fichas)
- [x] Quatro fichas preenchidas + consolidação final no gabarito _(4/4 — média ≈83,2%; ver [`validacao_labels.md`](validacao_labels/validacao_labels.md) § Síntese)_
- [x] Tabela F1 por classe copiada para slides — ver [`metricas_e_decisoes.md`](metricas_e_decisoes.md) §6
- [ ] 5+ referências bibliográficas citando TF-IDF, métricas multiclasse e domínio público

---

## 11. Depois da Fase 1

Rodamos BERT ([`FASE2`](FASE2-CLASSIFICACAO.md)) e SVM ([`FASE3`](FASE3-CLASSIFICACAO.md)) no mesmo split. Nenhum bateu o LogReg no teste. Tabela e explicação val vs teste em [`COMPARATIVO-FASES.md`](COMPARATIVO-FASES.md).
