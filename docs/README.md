# Documentação do projeto

Índice canônico da pasta `docs/`. Entrada na raiz: [`README.md`](../README.md).

**Escopo do projeto:** classificação por área de gasto (ComprasNet Fases 1–3 + extensão PNCP). **Sumarização fora do escopo.**

---

## Documento principal

| Documento | Descrição |
|-----------|-----------|
| [`TRABALHO-CONSOLIDADO.md`](TRABALHO-CONSOLIDADO.md) | **Relatório narrativo completo** — estrutura da disciplina, ComprasNet + PNCP |
| [`REGRAS-E-PROTOCOLOS.md`](REGRAS-E-PROTOCOLOS.md) | Rotulagem, limpeza, protocolos `pncp` / `pncp9*` (incl. fallback órgão) |

---

## Métricas, modelos e avaliação

| Documento | Descrição |
|-----------|-----------|
| [`METRICAS-E-DECISOES.md`](METRICAS-E-DECISOES.md) | Glossário de métricas, runs oficiais, decisão LogReg / BERT |
| [`MODEL-CARD.md`](MODEL-CARD.md) | Model card — performance, dados, limitações |
| [`COMPARATIVO-FASES.md`](COMPARATIVO-FASES.md) | Validação vs teste (Fases 1–3 ComprasNet) |
| [`VAZAMENTO-DE-LABEL.md`](VAZAMENTO-DE-LABEL.md) | Vazamento de label — mitigações e roteiro para relatório |
| [`VALIDACAO-LABELS/VALIDACAO-LABELS.md`](VALIDACAO-LABELS/VALIDACAO-LABELS.md) | Validação humana do label proxy (4/4 fichas, ≈83,2%) |

---

## Fases do pipeline (ComprasNet 423)

| Documento | Descrição |
|-----------|-----------|
| [`FASES.md`](FASES.md) | Índice das fases 1–3 + ponte para PNCP |
| [`FASE1-CLASSIFICACAO.md`](FASE1-CLASSIFICACAO.md) | TF-IDF + LogReg — decisões técnicas + EDA PNCP |
| [`FASE2-CLASSIFICACAO.md`](FASE2-CLASSIFICACAO.md) | BERTimbau (Transformer) |
| [`FASE3-CLASSIFICACAO.md`](FASE3-CLASSIFICACAO.md) | TF-IDF + SVM |

---

## Apresentação, tuning e operação

| Documento | Descrição |
|-----------|-----------|
| [`roteiro_10min.md`](roteiro_10min.md) | **Roteiro falado 10 min** — critérios da disciplina + arquitetura |
| [`ROTEIRO-FAMILIA-PROTOCOLOS-PNCP.md`](ROTEIRO-FAMILIA-PROTOCOLOS-PNCP.md) | Roteiro falado — família `pncp*` (2–3 min) |
| [`APRESENTACAO-CONTEUDO.md`](APRESENTACAO-CONTEUDO.md) | Conteúdo ampliado da apresentação |
| [`HIPERPARAMETROS-E-MELHORIAS.md`](HIPERPARAMETROS-E-MELHORIAS.md) | Tuning e backlog de melhorias |
| [`GPU-EQUIPE.md`](GPU-EQUIPE.md) | Fluxo GPU vs CPU no grupo |
| [`NOTEBOOK-ENTREGA.md`](NOTEBOOK-ENTREGA.md) | Atalho → [`notebooks/README.md`](../notebooks/README.md) |

---

## Projeto e coleta

| Documento | Descrição |
|-----------|-----------|
| [`PROJECT-REQUIREMENTS.md`](PROJECT-REQUIREMENTS.md) | Requisitos oficiais da disciplina (enunciado) |
| [`UNIVERSAL-DEEP-LEARNING-GUIDE.md`](UNIVERSAL-DEEP-LEARNING-GUIDE.md) | Guia vivo do projeto |
| [`DATA-COLLECTION-DECISIONS.md`](DATA-COLLECTION-DECISIONS.md) | Coleta: CAPTCHA, HTML vs PDF |
| [`PROPOSALS.md`](PROPOSALS.md) | Brainstorm inicial (Ideia 4 / sumarização descartada) |

---

## Validação manual (fichas)

| Documento | Integrante |
|-----------|------------|
| [`VALIDACAO-LABELS/FICHA-ELISANGELA.md`](VALIDACAO-LABELS/FICHA-ELISANGELA.md) | Elisangela Osorio |
| [`VALIDACAO-LABELS/FICHA-ALEXANDRE.md`](VALIDACAO-LABELS/FICHA-ALEXANDRE.md) | Alexandre Ferreira Ponte |
| [`VALIDACAO-LABELS/FICHA-RENE.md`](VALIDACAO-LABELS/FICHA-RENE.md) | Renê Estevam Deckers |
| [`VALIDACAO-LABELS/FICHA-INTEGRANTE4.md`](VALIDACAO-LABELS/FICHA-INTEGRANTE4.md) | Alexandre Hugo Sampaio Netto |

---

## Referências e materiais

| Caminho | Descrição |
|---------|-----------|
| [`referencias/aula03-04.pdf`](referencias/aula03-04.pdf) | Material de aula |
| [`referencias/bertimbau/`](referencias/bertimbau/) | Artigos BERTimbau |
| [`referencias/SVM/`](referencias/SVM/) | Artigos SVM / classificação |

---

## Fora de `docs/`

| Documento | Descrição |
|-----------|-----------|
| [`../README.md`](../README.md) | Setup, pipeline, Makefile, status |
| [`../notebooks/README.md`](../notebooks/README.md) | EDA e demo |
| [`../data/raw/README.md`](../data/raw/README.md) | Dados brutos e coleta |
| [`../experiments/README.md`](../experiments/README.md) | Registros JSON de runs |

*Convenção: arquivos `.md` em `docs/` preferem **UPPERCASE-WITH-HYPHENS** (exceção legada: `roteiro_10min.md`).*
