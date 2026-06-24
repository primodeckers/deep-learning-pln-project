# Fase 4 — Sumarização cidadã

Documento da **Fase 4** — tarefa **complementar** à classificação (Fases 1–3). Mesmo corpus, **outro objetivo**: resumir editais em linguagem acessível.

> Classificação: Fases 1–3 em [`FASE1`](FASE1-CLASSIFICACAO.md) · [`FASE2`](FASE2-CLASSIFICACAO.md) · [`FASE3`](FASE3-CLASSIFICACAO.md)

---

## 1. Objetivo

Gerar **resumos em linguagem cidadã** (objeto, quem participa, prazo, valor quando houver), sem substituir o edital oficial.

**Treino / geração:** via script — **não** misturar com notebook de classificação.

```bash
make train-summarize
# ou: python scripts/run_train.py --task summarization --model extractive
```

---

## 2. Baseline extrativo (concluído)

| Item | Valor |
|------|--------|
| Código | `src/summarize/extractive.py` |
| Orquestração | `src/summarize/run_summarization.py` |
| Saída slides | `reports/slides/resumos_exemplos.md` |
| Amostra | ~18 editais estratificados por área |

**Vantagem:** determinístico — **não alucina** prazo/valor.

---

## 3. Pendente (protótipo abstrativo)

| Item | Status |
|------|--------|
| PTT5 / mT5 inferência em amostra | Pendente |
| Comparação extrativo vs abstrativo | Pendente |
| Avaliação humana (escala 1–5) | Pendente |
| 3 exemplos antes/depois para slides | Pendente |

Quando implementar abstrativo, usar **script ou notebook dedicado** (`03_demo_sumarizacao.ipynb` — opcional), nunca o notebook de classificação.

---

## 4. Formato do resumo

Parágrafo curto respondendo:

1. O que está sendo contratado?
2. Quem pode participar?
3. Prazo para propostas?
4. Valor estimado (se constar)?

Ver exemplos em [`reports/slides/resumos_exemplos.md`](../reports/slides/resumos_exemplos.md).

---

## 5. Integração na apresentação

Na **demo ao vivo**, mostrar fluxo conceitual:

> Edital → **área predita** (Fases 1–3) + **resumo cidadã** (Fase 4)

Métricas do relatório vêm da **classificação**; sumarização ilustra **impacto aplicado**.

---

*Última atualização: 2026-06-24.*
