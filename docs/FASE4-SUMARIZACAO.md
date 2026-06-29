# Fase 4 — Sumarização cidadã

Tarefa à parte da classificação: mesmo corpus, objetivo diferente — um parágrafo legível pra quem não é da área jurídica.

> Classificação: [`COMPARATIVO-FASES.md`](COMPARATIVO-FASES.md) · [`METRICAS-E-DECISOES.md`](METRICAS-E-DECISOES.md)

---

## Objetivo

Responder, em linguagem simples:

1. O que está sendo contratado?
2. Quem pode participar?
3. Prazo para propostas?
4. Valor (se tiver no HTML)?

Não substitui o edital — é acessibilidade.

```bash
make train-summarize
```

---

## Baseline extrativo (feito)

Extrativo por regex/regras em `src/summarize/extractive.py`. Run: `summarization_extractive_20260624-013951`.

| O quê | Resultado |
|-------|-----------|
| Amostra | 18 editais (uma por área, mais ou menos) |
| Prazo extraído | 15/18 |
| Valor extraído | 18/18 |
| Exemplos | `reports/slides/resumos_exemplos.md` |

Os 3 sem prazo em geral são dispensas ou HTML sem campo de entrega — não é o modelo inventando errado; é o dado que não tem.

Vantagem frente a LLM: não alucina prazo nem valor.

---

## O que falta (se der tempo)

- mT5 / PTT5 em amostra pequena
- ROUGE e avaliação humana (escala 1–5)
- Comparar extrativo vs abstrativo nos slides

---

## Na apresentação

Mostramos o fluxo: edital → área (LogReg, F1 0,74) + resumo cidadã.

As métricas duras do relatório vêm da classificação; sumarização mostra o “pra que serve” na prática.
