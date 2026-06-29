# Documentação do projeto

Índice canônico da pasta `docs/`. Entrada na raiz: [`README.md`](../README.md).

---

## Documento principal

| Documento | Descrição |
|-----------|-----------|
| [`TRABALHO-CONSOLIDADO.md`](TRABALHO-CONSOLIDADO.md) | **Relatório narrativo completo** — contexto, dados, metodologia, resultados ComprasNet + extensão PNCP, conclusão |
| [`REGRAS-E-PROTOCOLOS.md`](REGRAS-E-PROTOCOLOS.md) | **Regras implementadas** — rotulagem, limpeza, protocolos `pncp*` |

---

## Métricas, modelos e avaliação

| Documento | Descrição |
|-----------|-----------|
| [`METRICAS-E-DECISOES.md`](METRICAS-E-DECISOES.md) | Glossário de métricas, runs oficiais ComprasNet + PNCP, decisão LogReg |
| [`MODEL-CARD.md`](MODEL-CARD.md) | Model card — performance, dados, limitações |
| [`COMPARATIVO-FASES.md`](COMPARATIVO-FASES.md) | Validação vs teste (Fases 1–3 ComprasNet) |
| [`VAZAMENTO-DE-LABEL.md`](VAZAMENTO-DE-LABEL.md) | Vazamento de label — mitigações e roteiro para relatório |
| [`VALIDACAO-LABELS/VALIDACAO-LABELS.md`](VALIDACAO-LABELS/VALIDACAO-LABELS.md) | Validação humana do label proxy (4/4 fichas, ≈83,2%) |

---

## Fases do pipeline (ComprasNet 423)

| Documento | Descrição |
|-----------|-----------|
| [`FASES.md`](FASES.md) | Índice das fases 1–3 |
| [`FASE1-CLASSIFICACAO.md`](FASE1-CLASSIFICACAO.md) | TF-IDF + LogReg — decisões técnicas + EDA PNCP |
| [`FASE2-CLASSIFICACAO.md`](FASE2-CLASSIFICACAO.md) | BERTimbau |
| [`FASE3-CLASSIFICACAO.md`](FASE3-CLASSIFICACAO.md) | TF-IDF + SVM |

---

## Apresentação, tuning e operação

| Documento | Descrição |
|-----------|-----------|
| [`APRESENTACAO-CONTEUDO.md`](APRESENTACAO-CONTEUDO.md) | Conteúdo ampliado da apresentação |
| [`roteiro_10min.md`](roteiro_10min.md) | **Roteiro falado 10 min** — alinhado aos critérios da disciplina |
| [`ROTEIRO-FAMILIA-PROTOCOLOS-PNCP.md`](ROTEIRO-FAMILIA-PROTOCOLOS-PNCP.md) | Roteiro falado — slide família `pncp*` (2–3 min) |
| [`HIPERPARAMETROS-E-MELHORIAS.md`](HIPERPARAMETROS-E-MELHORIAS.md) | Tuning e backlog de melhorias |
| [`GPU-EQUIPE.md`](GPU-EQUIPE.md) | Fluxo GPU vs CPU no grupo |
| [`NOTEBOOK-ENTREGA.md`](NOTEBOOK-ENTREGA.md) | Atalho → [`notebooks/README.md`](../notebooks/README.md) |

---

## Projeto e coleta

| Documento | Descrição |
|-----------|-----------|
| [`PROJECT-REQUIREMENTS.md`](PROJECT-REQUIREMENTS.md) | Requisitos oficiais da disciplina |
| [`UNIVERSAL-DEEP-LEARNING-GUIDE.md`](UNIVERSAL-DEEP-LEARNING-GUIDE.md) | Guia vivo do projeto |
| [`DATA-COLLECTION-DECISIONS.md`](DATA-COLLECTION-DECISIONS.md) | Coleta: CAPTCHA, HTML vs PDF |
| [`PROPOSALS.md`](PROPOSALS.md) | Brainstorm inicial de temas |

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

---

## Fora de `docs/`

| Documento | Descrição |
|-----------|-----------|
| [`../README.md`](../README.md) | Setup, pipeline, Makefile |
| [`../notebooks/README.md`](../notebooks/README.md) | EDA e demo |
| [`../data/raw/README.md`](../data/raw/README.md) | Dados brutos e coleta |
| [`../experiments/README.md`](../experiments/README.md) | Registros JSON de runs |

*Convenção de nomes: arquivos `.md` em `docs/` usam **UPPERCASE-WITH-HYPHENS**.*
