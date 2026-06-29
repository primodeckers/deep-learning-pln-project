# Classificação de editais por área de gasto — Distrito Federal, 2025

**Projeto Final — Deep Learning e PLN · Modalidade 2: PLN no Setor Público**

**Integrantes:** Elisangela Osorio · Alexandre Ferreira Ponte · Renê Estevam Deckers · Alexandre Hugo Sampaio Netto

**Documentação complementar:** [`README.md`](README.md) · [`REGRAS-E-PROTOCOLOS.md`](REGRAS-E-PROTOCOLOS.md) · [`METRICAS-E-DECISOES.md`](METRICAS-E-DECISOES.md) · [`MODEL-CARD.md`](MODEL-CARD.md)

---

## 1. Contexto e problema

Editais de licitação pública descrevem, em linguagem jurídica e técnica, o que o governo pretende comprar ou contratar. No Distrito Federal, centenas desses documentos são publicados todo ano no portal ComprasNet — e dezenas de milhares de compras aparecem no Portal Nacional de Contratações Públicas (PNCP). Para um cidadão, um pequeno empresário ou um órgão de controle, ler cada descrição manualmente para responder *“em que áreas o governo está gastando?”* ou *“o que esta compra significa na prática?”* é inviável.

Este projeto aplica técnicas de Processamento de Linguagem Natural a **dados inéditos coletados pelo grupo** (sem bases prontas de plataformas como Kaggle), com foco em **classificação automática de macroárea ou setor de gasto** a partir da descrição do objeto da licitação/compra.

A escolha conecta PLN a transparência no setor público: triagem temática de licitações para responder *“em que áreas o governo está gastando?”*.

---

## 2. Justificativa

**Dimensão aplicada:** licitações são instrumento central de execução orçamentária; automatizar sua leitura apoia fiscalização, jornalismo de dados e participação de micro e pequenas empresas.

**Dimensão técnica:** o corpus ComprasNet (423 editais) permite comparar TF-IDF + LogReg, SVM e BERTimbau no **mesmo protocolo** — respondendo se, com poucos dados, deep learning supera métodos clássicos. A extensão PNCP (~20 mil compras) testa se **escala** e **taxonomias alternativas** (9 setores empíricos) invertem esse veredito.

A hipótese inicial era que o BERTimbau superaria TF-IDF + LogReg. Nos 423 editais **não se confirmou**; no PNCP em escala grande, **sim** — achado metodológico central do trabalho.

---

## 3. Referencial teórico

**Domínio:** contratações públicas (Lei 14.133/2021), ComprasNet, PNCP; classificação temática de gastos; acessibilidade de informação pública.

**Técnica:** TF-IDF e classificadores lineares; fine-tuning BERTimbau (Souza et al.); F1 macro em classes desbalanceadas; vazamento de label e label proxy em PLN supervisionado.

Decisões derivadas: F1 macro como métrica primária; baseline clássico antes do Transformer; entrada `objeto_html` (não HTML completo) para reduzir vazamento.

---

## 4. Dados

### 4.1 ComprasNet — corpus principal (entrega oficial)

| Aspecto | Valor |
|---------|------:|
| Fonte | [ComprasNet](http://www.comprasnet.gov.br/) — CSV DF 2025 (437 linhas → **423 URLs** únicas) |
| Coleta | HTML de detalhe (sem CAPTCHA; PDF exige CAPTCHA — rejeitado por ética) |
| Corpus | `licitacoes_corpus.jsonl` — **423 registros** |
| Material / Serviço | 320 / 103 |
| Mediana do objeto | ~1.600 caracteres |
| Modalidade | Pregão (278) · Dispensa (134) |

Pipeline: `run_collect.py` → `run_preprocess.py` (delay 0,8 s entre requisições).

### 4.2 PNCP — extensão exploratória

| Aspecto | Valor |
|---------|------:|
| Fonte | PNCP / Compras.gov.br — `comprasGOV-anual-VW_FT_PNCP_COMPRA-2025.xls` |
| Filtro | UF = **DF**, ano = **2025** |
| Corpus | `pncp_corpus_df2025.jsonl` — **19.944 compras** |
| Campo principal | `objeto_compra` (mediana ~32 palavras vs ~239 no HTML ComprasNet) |
| Modalidade dominante | Inexigibilidade (~39%) — perfil distinto do ComprasNet |
| Info complementar | Presente em ~53% das linhas |

Pipeline: `scripts/run_preprocess_pncp.py` · EDA: `notebooks/03_eda_pncp.ipynb`.

### 4.3 Rotulagem (labels)

**ComprasNet e protocolo `pncp`:** rótulo **proxy** por **órgão → 6 macroáreas** (Saúde, Saneamento, Segurança, Educação, Infraestrutura/Obras, Administração/Outros). Palavras-chave no nome do órgão; primeira match vence. O classificador **não recebe o órgão como feature**.

**Protocolos `pncp9*`:** taxonomia de **9 setores empíricos** (keyword no objeto) + classe **`Indeterminado`**, com variantes:

- **`pncp9`:** só registros com keyword (~10,3 mil)
- **`pncp9full`:** todos; sem keyword → Indeterminado
- **`pncp9fb`:** fallback — sem keyword, usa macroárea do órgão (5 homônimas)
- **`pncp9fbi`:** idem + **informação complementar** no rótulo e no texto

Regras completas: [`REGRAS-E-PROTOCOLOS.md`](REGRAS-E-PROTOCOLOS.md).

**Validação humana (ComprasNet):** 30 editais, 4/4 fichas → concordância média **≈83,2%** ([`VALIDACAO-LABELS/VALIDACAO-LABELS.md`](VALIDACAO-LABELS/VALIDACAO-LABELS.md)).

### 4.4 Limitações dos dados

- ComprasNet: corpus **pequeno** (~295 treino); Educação com **2 exemplos no teste**; HTML ≠ PDF integral.
- PNCP: textos **curtos e burocráticos** (~48% sem keyword setorial); rótulos derivados de regras, não anotação manual.
- Ambos: escopo **DF/2025**; vazamento lexical residual (~49% em `objeto_html` ComprasNet).

---

## 5. Metodologia

### 5.1 Análise exploratória e vazamento de label

No ComprasNet, o HTML completo (`texto`) repete o órgão em **≈97%** dos casos onde a keyword da área aparece → F1 inflado **≈0,88**. O campo **`objeto_html`** reduz vazamento para **≈49%** → F1 honesto **≈0,74**. Limpeza adicional (`objeto_html_limpo`) remove boilerplate e nome do órgão copiado no texto.

Dois conceitos distintos: **vazamento de label** (pista do rótulo no input) vs **label proxy** (rótulo derivado do órgão, não anotado). Ver [`VAZAMENTO-DE-LABEL.md`](VAZAMENTO-DE-LABEL.md).

### 5.2 Protocolo experimental — ComprasNet 423

| Decisão | Valor |
|---------|-------|
| Entrada oficial | `objeto_html` |
| Partição | 70% / 15% / 15%, estratificada, **seed 42** |
| Tamanhos | 295 treino · 64 val · 64 teste |
| Métrica primária | **F1 macro no teste** |
| Seleção | Desenvolvimento olha val; **relatório reporta teste** |

### 5.3 Modelos (Fases 1–3)

| Fase | Modelo | Configuração-chave |
|------|--------|-------------------|
| 1 (oficial) | **TF-IDF + LogReg** | n-grama 2, 20k features, `C=1.0`, `class_weight=balanced` |
| 2 (comparativo DL) | **BERTimbau** | `max_len=512`, batch 16, lr 2e-5, 4 épocas, early stopping; GPU RTX 4090, fp16 |
| 3 (comparativo) | TF-IDF + **SVM linear** | Mesmo vetorizador da Fase 1 |

### 5.4 Extensão PNCP — protocolos e benchmark

Mesmo split 70/15/15 · seed 42 · entrada `objeto_html_limpo` ou `objeto_info_limpo` conforme protocolo.

| ID | Config | Descrição |
|----|--------|-----------|
| `pncp` | `classification_pncp.yaml` | 6 macroáreas por órgão — **referência honesta em escala** |
| `pncp9` | `classification_pncp_9setores.yaml` | 9 setores; filtra sem keyword |
| `pncp9full` | `classification_pncp_9setores_full.yaml` | 9 + Indeterminado |
| `pncp9fb` | `classification_pncp_9setores_fb.yaml` | Fallback órgão |
| `pncp9fbi` | `classification_pncp_9setores_fb_info.yaml` | Fallback + info complementar |

Benchmark de coortes difíceis: `scripts/run_benchmark_pncp_dificeis.py` — separa compras com keyword, “escondidas” (~853) e admin genérico.

### 5.5 Reprodutibilidade

Cada treino gera `experiments/<run_id>.json` (métricas, hash do corpus, commit Git) + MLflow local. Matrizes de confusão em `reports/figures/`.

---

## 6. Resultados

### 6.1 ComprasNet 423 — comparativo geral (teste)

| Modelo | F1 val | F1 teste | Accuracy teste |
|--------|-------:|---------:|---------------:|
| **TF-IDF + LogReg** | 0,743 | **0,740** | 0,797 |
| TF-IDF + SVM | 0,797 | 0,652 | 0,797 |
| BERTimbau | 0,559 | 0,400 | 0,688 |

**Decisão:** LogReg como modelo principal — melhor F1 no teste e estabilidade val≈teste. SVM overfitou na validação (64 exemplos). BERT colapsou em classes raras.

Runs: `classification_*_20260624-013*`.

### 6.2 ComprasNet — F1 por classe (teste)

| Área | n | LogReg | SVM | BERT |
|------|--:|-------:|----:|-----:|
| Saúde | 17 | 0,90 | 0,90 | 0,88 |
| Saneamento | 7 | 1,00 | 1,00 | 0,80 |
| Segurança | 9 | 0,46 | 0,46 | 0,00 |
| Educação | 2 | 0,67 | 0,00 | 0,00 |
| Infraestrutura/Obras | 4 | 0,60 | 0,75 | 0,00 |
| Administração/Outros | 25 | 0,81 | 0,80 | 0,73 |

### 6.3 Vazamento de label — contraste de entradas

| Campo | F1 macro (teste) | Vazamento lexical |
|-------|------------------:|-------------------|
| `texto` (HTML completo) | ≈ 0,88 | ≈ 97% |
| **`objeto_html`** | **≈ 0,74** | ≈ 49% |
| `objeto_html_limpo` | marginal vs objeto | ≈ 47% |

### 6.4 PNCP DF/2025 — resultados por protocolo (F1 macro teste)

#### Protocolo honesto — 6 macroáreas por órgão (`pncp`)

| Modelo | F1 teste | Accuracy |
|--------|----------|----------|
| LogReg | 0,756 | 0,926 |
| SVM | 0,783 | 0,939 |
| **BERTimbau** | **0,858** | 0,960 |

Com ~20 mil exemplos, **BERT supera baselines** — inverso ao corpus 423.

#### Protocolos 9 setores (exploratórios)

| Protocolo | LogReg | SVM | BERT | Nota |
|-----------|-------:|----:|-----:|------|
| `pncp9` (filtrado, ~10,3k) | 0,857 | 0,877 | **0,969** | Só keyword |
| `pncp9full` (19,9k) | 0,816 | 0,862 | **0,970** | + Indeterminado |
| `pncp9fb` | **0,824** | — | — | Fallback órgão, só objeto |
| `pncp9fbi` | 0,788 | 0,829 | **0,955** | + info complementar |

**Interpretação dos F1 altos (~0,95–0,97):** refletem reprodução das **regras de keyword** e, em `pncp9fbi`, **acoplamento rótulo↔texto** (info entra nos dois). Não invalidam o trabalho, mas exigem transparência — distintos do protocolo honesto `pncp` (0,858).

**Info complementar:** piora LogReg (0,824→0,788) mas **dispara BERT** (0,829→0,955) — sinal semântico só emerge com Transformer.

**Coortes PNCP:** ~48% sem keyword no objeto; ~853 “escondidas” (órgão setorial, objeto burocrático); benchmark documentado em `reports/benchmark_pncp_casos_dificeis.json`.

### 6.5 Impacto aplicado

- **ComprasNet:** triagem automática por macroárea de gasto.
- **PNCP:** escala permite cruzar área/setor com valor homologado e modalidade; base para jornalismo de dados e controle social em DF/2025.

---

## 7. Discussão

### 7.1 Dois corpora, dois vereditos sobre BERT

| Corpus | n treino | BERT F1 teste | LogReg F1 teste | Lição |
|--------|----------|---------------|-----------------|-------|
| ComprasNet | ~295 | 0,40 | **0,74** | Poucos dados → clássico ganha |
| PNCP (`pncp`) | ~14.000 | **0,858** | 0,756 | Escala → Transformer ganha |

O resultado do projeto **depende do volume e do protocolo** — alinhado ao lema “depende” da disciplina.

### 7.2 Limitações e vieses

- **Label proxy** (~83% concordância humana): erros estruturais (Bombeiros + objeto clínico → label Segurança).
- **Classes raras** no ComprasNet: F1 instável (Educação n=2 no teste).
- **Vazamento residual** e **acoplamento rótulo↔texto** nos protocolos `pncp9*`.
- **PNCP ≠ ComprasNet:** textos curtos, inexigibilidade dominante, perfil burocrático.

### 7.3 Uso responsável

Classificador **não substitui** análise jurídica. CAPTCHA do ComprasNet **não foi contornado**. Métricas altas em protocolos keyword devem ser lidas como **reprodução de regras**, não garantia de generalização em produção.

---

## 8. Conclusão

O projeto percorreu o ciclo completo de PLN aplicado ao setor público: problema real, coleta ética, múltiplos modelos, métricas adequadas e interpretação crítica.

**Principais aprendizados:**

1. **Entrega oficial (ComprasNet 423):** TF-IDF + LogReg classifica editais em 6 macroáreas com **F1 macro 0,74** no teste, superando SVM (0,65) e BERT (0,40) neste volume.
2. **Extensão PNCP (~20 mil):** BERT atinge **F1 0,858** no protocolo honesto por órgão; protocolos de 9 setores mostram que **escala + contexto semântico** mudam o jogo frente a TF-IDF.
3. **~48%** das compras PNCP são lexicalmente vagas — taxonomia com `Indeterminado` e fallback orgânico são necessários; info complementar ajuda BERT, atrapalha modelos lineares.
4. **Transparência metodológica** (proxy validado, vazamento documentado, val vs teste) é tão importante quanto a métrica.

**Próximos passos:** anos anteriores (2021–2024); info complementar **condicional** (só quando objeto vago); anotação manual parcial de labels.

---

## 9. Referências

*(Completar ABNT/IEEE no PDF final — mínimo 5 domínio + 5 técnica.)*

**Domínio:** Lei 14.133/2021; ComprasNet; PNCP; transparência e classificação temática de gastos; linguagem cidadã (Rosado & Dias, 2024); IA em licitações (Souto et al., 2025).

**Técnica:** Devlin et al. (BERT); Souza et al. (BERTimbau); scikit-learn; F1 em classes desbalanceadas.

**Operacional:** https://pncp.gov.br/ · `neuralmind/bert-base-portuguese-cased` · lista completa em [`APRESENTACAO-CONTEUDO.md`](APRESENTACAO-CONTEUDO.md) §9.

---

## 10. Apêndice técnico

### Pipeline ComprasNet

```
CSV ComprasNet DF 2025
  → download HTML (423, delay 0,8 s)
  → licitacoes_corpus.jsonl
  → split 70/15/15
  → LogReg / SVM / BERTimbau
```

### Pipeline PNCP

```
PNCP XLS (DF 2025)
  → run_preprocess_pncp.py
  → pncp_corpus_df2025.jsonl (19.944)
  → protocolos pncp / pncp9 / pncp9full / pncp9fb / pncp9fbi
  → benchmark coortes difíceis
```

### Reprodução

```bash
pip install -r requirements-dev.txt
pip install -e ".[bert]"
python scripts/run_collect.py && python scripts/run_preprocess.py
python scripts/run_preprocess_pncp.py
python scripts/run_train.py --model baseline --config configs/classification.yaml
python scripts/run_train.py --model bertimbau --config configs/classification_pncp.yaml \
  --corpus data/processed/pncp_corpus_df2025.jsonl
python scripts/run_benchmark_pncp_dificeis.py
```

### Síntese para apresentação (10 min)

> Coletamos **423 editais** ComprasNet (DF 2025). LogReg F1 **0,74** no teste venceu SVM (0,65) e BERT (0,40) — corpus pequeno favorece o clássico. Estendemos com **19.944 compras PNCP**: BERT F1 **0,858** no protocolo por órgão. Exploramos 9 setores empíricos, fallback orgânico e info complementar — F1 até 0,97, mas com acoplamento rótulo↔texto que declaramos. A contribuição é explicar **o que a métrica significa** e o cuidado metodológico por trás dela.

---

*Documento consolidado · junho/2026 · ComprasNet runs 24/06/2026 · PNCP runs 28–29/06/2026*
