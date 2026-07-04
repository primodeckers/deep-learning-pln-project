# Índice de fases do projeto

**Escopo:** classificação por área de gasto. Sumarização **fora do escopo**.

## ComprasNet 423 — entrega oficial

| Fase | Tarefa | Modelo | Família | F1 macro (teste) | Doc |
|------|--------|--------|---------|------------------|-----|
| **1** | Classificação | TF-IDF + **LogReg** | ML clássico (linear) | **0,740** | [`FASE1-CLASSIFICACAO.md`](FASE1-CLASSIFICACAO.md) |
| 2 | Classificação | BERTimbau | **Transformer** (DL) | 0,400 | [`FASE2-CLASSIFICACAO.md`](FASE2-CLASSIFICACAO.md) |
| 3 | Classificação | TF-IDF + SVM | ML clássico (margem) | 0,652 | [`FASE3-CLASSIFICACAO.md`](FASE3-CLASSIFICACAO.md) |

**Modelo principal do relatório (ComprasNet):** Fase 1 (LogReg) — melhor generalização no teste.

**Não implementados:** CNN (visão) · RNN/LSTM (legado sequencial — DL coberto pelo BERT).

**Comparativo val × teste:** [`COMPARATIVO-FASES.md`](COMPARATIVO-FASES.md) · [`METRICAS-E-DECISOES.md`](METRICAS-E-DECISOES.md)

**Runs oficiais:** `experiments/classification_*_20260624-013*.json` · [`experiments/README.md`](../experiments/README.md)

## Extensão PNCP (~20 mil)

Protocolos `pncp`, `pncp9`, `pncp9full`, `pncp9fb`, `pncp9fbi` — ver [`REGRAS-E-PROTOCOLOS.md`](REGRAS-E-PROTOCOLOS.md).

| Protocolo | Melhor F1 teste (BERT, quando treinado) | Nota |
|-----------|----------------------------------------:|------|
| `pncp` | **0,858** | Honesto em escala (6 áreas por órgão) |
| `pncp9fbi` | 0,955 | Exploratório — acoplamento rótulo↔texto |

Relatório narrativo: [`TRABALHO-CONSOLIDADO.md`](TRABALHO-CONSOLIDADO.md) · fala: [`ROTEIRO-FAMILIA-PROTOCOLOS-PNCP.md`](ROTEIRO-FAMILIA-PROTOCOLOS-PNCP.md)

Notebooks: [`notebooks/README.md`](../notebooks/README.md) · Demo: `02_demo_classificacao.ipynb`
