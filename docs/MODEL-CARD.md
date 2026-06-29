# Model card — licitações ComprasNet DF 2025 + extensão PNCP

Resumo de performance e limitações. Runs em `experiments/`.

## Escopo

| Corpus | Registros | Papel no relatório |
|--------|----------:|--------------------|
| **ComprasNet HTML** | 423 | **Entrega oficial** — LogReg F1 0,74 |
| **PNCP DF/2025** | 19.944 | Extensão exploratória — escala e protocolos `pncp*` |

Decisão metodológica: [`METRICAS-E-DECISOES.md`](METRICAS-E-DECISOES.md) · Regras: [`REGRAS-E-PROTOCOLOS.md`](REGRAS-E-PROTOCOLOS.md)

---

## ComprasNet 423 — classificação (6 macroáreas)

**Protocolo:** `objeto_html` · split 70/15/15 · seed 42 · label proxy órgão→área

### Modelo principal — TF-IDF + LogReg

**Run:** `classification_baseline_20260624-013836`

| Conjunto | Accuracy | F1 macro | F1 weighted |
|----------|----------|----------|-------------|
| Validação | 0,766 | **0,743** | 0,750 |
| Teste | 0,797 | **0,740** | 0,788 |

### Comparativos (teste)

| Modelo | F1 macro | Run |
|--------|----------|-----|
| **TF-IDF + LogReg** | **0,740** | `013836` |
| TF-IDF + SVM | 0,652 | `013851` |
| BERTimbau | 0,400 | `013908` |

`texto` (HTML completo) → F1 ≈ 0,88 (vazamento). Ver [`VAZAMENTO-DE-LABEL.md`](VAZAMENTO-DE-LABEL.md).

### Protocolo anti-leakage — `objeto_html_limpo` (20260628)

Mesmo corpus 423, mesmo split/seed, mas campo `objeto_html_limpo` (HTML limpo sem cabeçalho de órgão). Referência para quantificar o impacto do vazamento residual presente em `objeto_html`.

| Modelo | F1 macro (teste) | Δ vs. oficial | Run |
|--------|-----------------|---------------|-----|
| TF-IDF + LogReg | 0,726 | −0,014 | `classification_baseline_20260628-232301` |
| TF-IDF + SVM | 0,671 | +0,019 | `classification_svm_20260628-232322` |
| BERTimbau | 0,401 | +0,001 | `classification_bertimbau_20260628-232344` |

A queda de ~1,4 p.p. no LogReg confirma vazamento residual pequeno em `objeto_html`. O SVM sobe ligeiramente porque o texto mais limpo reduz ruído que prejudicava a margem do kernel linear. BERT permanece estável — o campo de entrada não era o gargalo.

---

## PNCP 19.944 — protocolo honesto (`pncp`)

**Entrada:** `objeto_html_limpo` · **Rótulo:** 6 macroáreas por órgão

| Modelo | F1 teste | Accuracy teste |
|--------|----------|----------------|
| LogReg | 0,756 | 0,926 |
| SVM | 0,783 | 0,939 |
| **BERTimbau** | **0,858** | 0,960 |

Com ~20k exemplos, BERT supera baselines no protocolo por órgão — contraste com corpus 423.

---

## PNCP — protocolos 9 setores (exploratório)

| Protocolo | LogReg | SVM | BERT | Nota |
|-----------|-------:|----:|-----:|------|
| `pncp9` (filtrado) | 0,857 | 0,877 | 0,969 | Só keyword no objeto |
| `pncp9full` | 0,816 | 0,862 | 0,970 | + Indeterminado |
| `pncp9fb` | 0,824 | — | — | Fallback órgão |
| `pncp9fbi` | 0,788 | 0,829 | **0,955** | + info complementar |

F1 alto (~0,95–0,97) indica reprodução de regras keyword, não generalização “cega” em objetos vagos.

---

## Sumarização extrativa (Fase 4)

**Run:** `summarization_extractive_20260624-013951` · 18 editais

| Cobertura | Valor |
|-----------|-------|
| Com prazo | 15/18 (83%) |
| Com valor | 18/18 (100%) |

---

## Dados e limitações

- Label proxy — validação humana ≈83,2% ([`VALIDACAO-LABELS/VALIDACAO-LABELS.md`](VALIDACAO-LABELS/VALIDACAO-LABELS.md))
- ComprasNet: corpus pequeno; Educação n=2 no teste
- PNCP: perfil distinto (inexigibilidade ~39%, textos curtos)
- Modelo **não** recebe `orgao_csv` como feature na classificação

## Artefatos

| Tipo | Caminho |
|------|---------|
| LogReg / SVM | `models/classification_*.joblib` |
| BERT | `models/classification_*_bertimbau_*/` |
| JSON | `experiments/<run_id>.json` |
| MLflow | `experiments/mlflow.db` |

---

*Atualizado jun/2026 — runs ComprasNet `20260624-*` + PNCP `20260628–20260629`*
