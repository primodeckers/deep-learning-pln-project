# Métricas e decisões de avaliação

Documento de referência para escolhas metodológicas — equivalente ao espírito do `metricas_e_limiar.md` do projeto tech-challenge, adaptado para PLN em licitações.

> Guia completo: [`UNIVERSAL-DEEP-LEARNING-GUIDE.md`](UNIVERSAL-DEEP-LEARNING-GUIDE.md) §6  
> Model card com números: [`model_card.md`](model_card.md)

---

## Tarefa principal: classificação por macroárea

### Métrica primária — F1 macro

**Por quê:** o corpus é desbalanceado (Saúde e Administração/Outros dominam; Educação e Infraestrutura são raras). Accuracy alta mascara falhas nas classes pequenas. F1 macro trata todas as classes com peso igual.

**Uso:** comparar baseline TF-IDF vs BERTimbau no **mesmo split** (`seed=42`, proporções em `configs/classification.yaml`).

### Métricas secundárias

| Métrica | Papel |
|---------|--------|
| F1 por classe | Diagnosticar qual macroárea falha |
| F1 weighted | Referência, mas favorece classes frequentes |
| Accuracy | Contexto, não critério de seleção |
| Matriz de confusão | Visualizar confusões entre áreas parecidas |

### Decisão crítica — campo de entrada (`text_field`)

| Campo | F1 macro (teste, baseline) | Vazamento (Tabela 7) | Papel |
|-------|------------------------------|----------------------|--------|
| `texto` | ≈ 0,88 | ~97% | ❌ Contraste — teto inflado |
| `objeto_html` | ≈ 0,74 | ~49% | ✅ **Entrada oficial** |
| `objeto_html_limpo` | _(experimento)_ | ~47% | ⚗️ Limpeza extra — ganho pequeno |

**Decisão adotada:** `text_field: objeto_html` em `configs/classification.yaml`.

**Não há limiar universal** de “quanto pode vazar” — o critério é metodológico: não repetir a fonte do label no input e documentar limitações. Ver [`vazamento_de_label.md`](vazamento_de_label.md) §5.1 e §9 (roteiro para relatório/slides).

O modelo **não** recebe `orgao_csv` como feature — o órgão só gera o label inicial (limitação *label proxy* declarada no relatório).

### Validação humana do label proxy

| Item | Valor |
|------|-------|
| Amostra | 30 editais, seed 42 (`scripts/export_validacao_sample.py`) |
| Gabarito | [`validacao_labels/validacao_labels.md`](validacao_labels/validacao_labels.md) |
| Status | **4/4 fichas** (2026-06-18 a 2026-06-22) |
| Taxa de concordância | **Média ≈83,2%** (Renê 96,2% · Ponte 95,7% · Hugo 78,3% · Elisangela 62,5%) |
| Consenso (≥2 `N`) | TCDF #30 → `Saude`; CBMDF #4, 12, 22 → `Saude`; CAESB #28 → `Administracao/Outros` |

Conclusão: o proxy por órgão é **aceitável como rotulagem fraca** para o baseline; dispersão entre revisores reflete critério em compras transversais. Ajuste em `AREA_KEYWORDS` ou regras por objeto é melhoria futura — ver [`validacao_labels/validacao_labels.md`](validacao_labels/validacao_labels.md) § Síntese.

### Split e reprodutibilidade

```
Treino 70% ─┐
Val    15% ─┼─ estratificado por `area`, random_state=42
Teste  15% ─┘
```

- Mesmas partições para baseline e BERTimbau (`src/preprocess/dataset.py`).
- Cada run grava `dataset.sha256` e `git_commit` em `experiments/*.json`.

### Hiperparâmetros do baseline (referência)

Definidos em `configs/classification.yaml` → bloco `params`:

| Parâmetro | Valor | Nota |
|-----------|-------|------|
| `ngram_max` | 2 | Unigramas + bigramas |
| `min_df` | 2 | Ignora termos muito raros |
| `max_features` | 20 000 | Limite de vocabulário TF-IDF |
| `C` | 1.0 | Regularização da LogReg |
| `class_weight` | balanced | Mitiga desbalanceamento |

---

## Tarefa complementar: sumarização cidadã

### Baseline atual — extrativo por regras

Não usa ROUGE ainda. Cobertura medida na run JSON:

- `com_prazo` / `com_valor` — quantos resumos extraíram esses campos.

### Avaliação prevista (Fase 3)

| Tipo | Método |
|------|--------|
| Automática | ROUGE-L (referência fraca: `objeto_html` + datas) |
| Humana | Escala 1–5: clareza, completude, fidelidade (3 avaliadores) |

---

## Rastreamento de experimentos

Cada treino produz:

1. **JSON portátil** em `experiments/<run_id>.json` — versionável no Git.
2. **MLflow** em `experiments/mlflow.db` — comparação local (`make mlflow-ui`).

Fingerprint do corpus garante que duas runs comparáveis usaram o mesmo `licitacoes_corpus.jsonl`.

---

## O que não fazemos (escopo consciente)

- **Limiar de decisão** — classificação multiclasse, não binária; sem corte de probabilidade de negócio (diferente do churn).
- **Serving em produção** — sem API FastAPI; pipeline batch via scripts.
- **Validação Pandera** — corpus é JSONL/texto; validação futura seria schema do corpus, não linhas tabulares.

---

## Checklist antes de apresentar resultados

- [x] `text_field` documentado como `objeto_html`
- [x] Validação manual de labels concluída (4/4 fichas; média ≈83,2%; ver `validacao_labels/`)
- [ ] F1 macro reportado no **teste**, não só na validação
- [ ] Classes com `support < 5` discutidas explicitamente
- [ ] Hash do corpus (`dataset.sha256`) citado na tabela de experimentos
- [ ] Baseline e BERTimbau no mesmo split (quando Fase 2 estiver pronta)
