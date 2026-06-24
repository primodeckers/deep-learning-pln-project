# Hiperparâmetros, pesos e melhoria de métricas

Notas do grupo para **discutir depois** — o que dá para ajustar hoje no código, o que ainda falta implementar e o que é realista esperar de ganho com o corpus atual (423 editais).

> Contexto: runs oficiais `20260624-*` · decisão atual → LogReg F1 teste **0,740**  
> Métricas e protocolo: [`metricas_e_decisoes.md`](metricas_e_decisoes.md) · val vs teste: [`COMPARATIVO-FASES.md`](COMPARATIVO-FASES.md)

---

## 1. Resumo executivo

| Pergunta | Resposta curta |
|----------|----------------|
| Dá para tunar hiperparâmetros? | **Sim** — via `configs/classification.yaml` + `scripts/run_train.py` |
| Dá para ajustar “pesos”? | **Depende do modelo** — sklearn já usa `class_weight`; BERT ainda **não** |
| Rede neural (BERT) é tunável aqui? | **Sim** — LR, épocas, batch, `max_length`, early stopping já expostos; falta warmup, freeze, peso por classe |
| Vale a pena para a entrega? | LogReg: ganho marginal. BERT: maior espaço de experimento, mas teto baixo sem mais dados |
| Risco metodológico | Buscar hiperparâmetro olhando o **teste** → vazamento; usar **val** na busca, teste **uma vez** no final |

---

## 2. O que o projeto já suporta

### Onde configurar

| Arquivo | Uso |
|---------|-----|
| [`configs/classification.yaml`](../configs/classification.yaml) | Padrão CPU — baseline, SVM e BERT no mesmo YAML |
| [`configs/classification_bert_gpu.yaml`](../configs/classification_bert_gpu.yaml) | BERT na GPU (mesmos parâmetros, `model: bertimbau`) |
| [`src/train/train_classification.py`](../src/train/train_classification.py) | Orquestra treino; filtra params por modelo |
| [`scripts/run_train.py`](../scripts/run_train.py) | CLI de treino |

Cada run gera `experiments/<run_id>.json` e (opcional) registro no MLflow (`make mlflow-ui`).

### Parâmetros por modelo (estado atual)

#### Fase 1 — TF-IDF + LogReg

| Parâmetro | Valor atual | O que faz |
|-----------|-------------|-----------|
| `ngram_max` | 2 | Unigramas + bigramas |
| `min_df` | 2 | Ignora termos que aparecem em &lt; 2 documentos |
| `max_features` | 20 000 | Teto do vocabulário TF-IDF |
| `C` | 1.0 | Inverso da força da regularização L2 |
| `max_iter` | 1000 | Limite de iterações do solver |
| `class_weight` | `balanced` | Pesa classes inversamente à frequência no treino |
| `seed` | 42 | Reprodutibilidade do vetorizador + split |

**Sobre “pesos”:** o LogReg **aprende** os coeficientes automaticamente no `fit()`. O que controlamos é regularização (`C`) e reponderação de classes (`class_weight`), não editamos pesos à mão.

#### Fase 3 — TF-IDF + SVM

Mesmo vetorizador do baseline. Parâmetros extras:

| Parâmetro | Valor atual |
|-----------|-------------|
| `C` | 1.0 |
| `svm_kernel` | `linear` |
| `svm_probability` | `true` |
| `class_weight` | `balanced` |

#### Fase 2 — BERTimbau

| Parâmetro | Valor atual | Exposto no YAML? |
|-----------|-------------|------------------|
| `model_name` | `neuralmind/bert-base-portuguese-cased` | Sim |
| `max_length` | 512 | Sim |
| `batch_size` | 16 | Sim |
| `learning_rate` | 2e-5 | Sim |
| `epochs` | 4 | Sim |
| `early_stopping_patience` | 2 | Sim |
| `seed` | 42 | Sim |
| `weight_decay` | 0.01 | **Não** — fixo em [`bert_classifier.py`](../src/models/bert_classifier.py) |
| `warmup_ratio` | — | **Não implementado** |
| `class_weight` / loss ponderado | — | **Não implementado** |
| freeze de camadas do encoder | — | **Não implementado** |

O Trainer já escolhe o melhor checkpoint por **F1 macro na validação** (`metric_for_best_model="f1_macro"`).

---

## 3. Por que as métricas estão onde estão

Não é só “falta tunar”. Limites estruturais do corpus:

| Fator | Impacto |
|-------|---------|
| **Poucos exemplos** | ~295 treino, 64 val, 64 teste |
| **Desbalanceamento** | Administração/Outros ≈ 40% do corpus |
| **Classes raras no teste** | Educação: **2** exemplos; Segurança: 9 |
| **BERT vs dados** | Milhões de parâmetros, centenas de amostras → tendência a colapsar para classe majoritária |
| **SVM na val** | F1 val 0,797, teste 0,652 — possível overfitting nos 64 editais de validação |
| **LogReg estável** | Val 0,743 → teste 0,740 — pouco espaço sem mudar dados ou features |

Hiperparâmetros podem **afinar**; raramente **resolvem** classe com 2 exemplos no teste.

---

## 4. Ideias de tuning — por modelo

### 4.1 LogReg (prioridade baixa, baixo risco)

Grid manual pequeno — comparar **F1 macro na val**, confirmar no teste só no melhor candidato.

| Parâmetro | Valores para testar | Hipótese |
|-----------|---------------------|----------|
| `C` | 0.1, 0.5, 1.0, 2.0, 5.0 | `C` menor → menos overfitting; maior → ajuste mais agressivo |
| `ngram_max` | 1, 2, 3 | Trigramas podem captar frases do objeto; também aumentam sparsity |
| `max_features` | 10k, 20k, 30k | Vocabulário maior vs ruído |
| `min_df` | 1, 2, 3 | `min_df=1` inclui termos raros (útil ou ruído?) |

**Ganho esperado:** 0 a +0,05 F1 macro no teste. Pode não mudar nada — modelo já está bem calibrado.

### 4.2 SVM (prioridade baixa, cuidado com overfitting)

| Parâmetro | Valores | Nota |
|-----------|---------|------|
| `C` | 0.1, 0.25, 0.5, 1.0 | Reduzir `C` pode aliviar o gap val→teste |
| `svm_kernel` | manter `linear` | Kernel RBF com 295 amostras costuma piorar |

### 4.3 BERT (prioridade média — é a rede neural do projeto)

| Parâmetro | Valores sugeridos | Motivo |
|-----------|-------------------|--------|
| `learning_rate` | 1e-5, 2e-5, 3e-5, 5e-5 | LR é o knob mais sensível no fine-tuning |
| `epochs` | 3–8 | Pouco dado → poucas épocas; early stopping já limita |
| `early_stopping_patience` | 1, 2, 3 | Patience 1 para menos overfitting na val |
| `batch_size` | 4, 8, 16 | Batch menor → mais updates por época |
| `max_length` | 256, 384, 512 | Textos longos truncados; 256 pode reduzir ruído e tempo |
| `weight_decay` | 0.01, 0.05, 0.1 | Regularização L2 — hoje fixo no código |
| **Peso por classe no loss** | inverso à frequência | Equivalente ao `class_weight` do LogReg — **a implementar** |
| **Warmup** | ~10% dos steps | Estabiliza treino; **a implementar** |
| **Freeze encoder** | 1–2 épocas só na cabeça, depois fine-tune total | Comum com pouco dado — **a implementar** |
| `model_name` | base vs `distilbert` PT (se existir checkpoint) | Modelo menor às vezes generaliza melhor com N pequeno |

**Ganho esperado:** BERT de 0,40 para ~0,45–0,55 com tuning cuidadoso — **ainda provavelmente abaixo do LogReg** sem mais dados ou augmentation.

### 4.4 O que provavelmente ajuda mais que hiperparâmetro

| Ação | Impacto esperado | Esforço |
|------|------------------|---------|
| Mais editais / revisão de labels (Segurança, Educação) | Alto | Alto |
| Data augmentation (paráfrase, back-translation) | Médio–alto no BERT | Médio |
| K-fold estratificado (ex. 5×) para métrica estável | Médio (metodologia) | Médio |
| Trocar `objeto_html` por campo com menos ruído (sem vazamento) | Variável | Já documentado em [`vazamento_de_label.md`](vazamento_de_label.md) |

---

## 5. Protocolo de busca (para não invalidar o relatório)

```
1. Fixar split (seed=42) e corpus (sha256 atual)
2. Definir grid ou estudo Optuna
3. Para cada combinação:
   - treinar
   - registrar F1 macro na VALIDAÇÃO no MLflow / JSON
4. Escolher melhor config só pela val
5. Rodar UMA vez no teste → número do relatório
6. Documentar runs em experiments/ e citar no model card
```

**Não fazer:** repetir busca até o teste “ficar bonito” — isso contamina a avaliação.

Para o trabalho acadêmico, um **grid pequeno documentado** (mesmo sem ganho) mostra rigor metodológico.

---

## 6. Como rodar hoje (manual)

```bash
# Baseline — editar configs/classification.yaml (model: baseline)
python scripts/run_train.py --task classification

# SVM
# model: svm no YAML

# BERT (GPU)
python scripts/run_train.py --task classification --config configs/classification_bert_gpu.yaml
```

Entre runs, alterar só os params do bloco relevante. Comparar JSONs em `experiments/` ou aba Runs do MLflow.

---

## 7. O que falta no código (backlog de discussão)

Itens para decidir em reunião — implementar só se o grupo achar que vale o tempo antes da entrega.

| # | Item | Arquivo provável | Esforço | Prioridade sugerida |
|---|------|------------------|---------|---------------------|
| 1 | `class_weight` no loss do BERT | `src/models/bert_classifier.py` | Baixo | **Alta** |
| 2 | Expor `weight_decay` e `warmup_ratio` no YAML | `bert_classifier.py` + configs | Baixo | Média |
| 3 | Opção `freeze_encoder_epochs` | `bert_classifier.py` | Médio | Média |
| 4 | Script `scripts/tune_classification.py` (grid ou Optuna) | novo | Médio | Média |
| 5 | Integração Optuna + MLflow | novo + guia §5 | Médio | Baixa (se grid manual bastar) |
| 6 | K-fold no orquestrador | `train_classification.py` | Alto | Baixa para entrega |
| 7 | Focal loss (alternativa a class_weight) | `bert_classifier.py` | Médio | Baixa |

Referência de mercado: [`UNIVERSAL-DEEP-LEARNING-GUIDE.md`](UNIVERSAL-DEEP-LEARNING-GUIDE.md) §5 — hoje marcamos “hiperparâmetros: manual”.

---

## 8. Perguntas para a próxima reunião

1. **Objetivo:** queremos subir F1 do LogReg ou só documentar que tentamos e o baseline já era bom?
2. **BERT:** vale mais um ciclo de tuning (GPU + tempo) ou aceitamos como comparativo negativo bem explicado?
3. **Escopo:** grid manual (3–5 configs) ou investir em Optuna?
4. **Implementar `class_weight` no BERT** antes de qualquer sweep?
5. **Teste:** quando rodamos a avaliação final — só depois de fechar o grid?
6. **Relatório:** como citar busca de hiperparâmetros na seção de metodologia (tabela de configs testadas)?

---

## 9. Decisões pendentes (preencher depois)

| Data | Decisão | Responsável | Runs gerados |
|------|---------|-------------|--------------|
| _a definir_ | | | |

---

## 10. Links relacionados

| Documento | Conteúdo |
|-----------|----------|
| [`metricas_e_decisoes.md`](metricas_e_decisoes.md) | Glossário, runs oficiais, hiperparâmetros de referência §7 |
| [`COMPARATIVO-FASES.md`](COMPARATIVO-FASES.md) | Por que SVM/BERT caíram val→teste |
| [`FASE2-CLASSIFICACAO.md`](FASE2-CLASSIFICACAO.md) | Detalhe do pipeline BERT |
| [`model_card.md`](model_card.md) | Números para slides |
| [`configs/classification.yaml`](../configs/classification.yaml) | Fonte canônica dos defaults |
