# Documentação do projeto

Índice da pasta `docs/`. O ponto de entrada principal do repositório é o [`README.md`](../README.md) na raiz.

## Documentos

| Documento | Descrição |
|---|---|
| [`PROJECT-REQUIREMENTS.md`](PROJECT-REQUIREMENTS.md) | Requisitos oficiais da disciplina |
| [`UNIVERSAL-DEEP-LEARNING-GUIDE.md`](UNIVERSAL-DEEP-LEARNING-GUIDE.md) | Guia vivo do projeto (preencher em conjunto) |
| [`DATA-COLLECTION-DECISIONS.md`](DATA-COLLECTION-DECISIONS.md) | Decisões de coleta de dados (CAPTCHA, HTML vs PDF, etc.) |
| [`PROPOSALS.md`](PROPOSALS.md) | Brainstorm de temas/tarefas de PLN para o projeto |
| [`model_card.md`](model_card.md) | Model card — performance, dados, limitações |
| [`metricas_e_decisoes.md`](metricas_e_decisoes.md) | Métricas, anti-leakage e decisões de avaliação |
| [`GPU-EQUIPE.md`](GPU-EQUIPE.md) | Fluxo GPU vs CPU — quem treina o quê, o que vai pro Git |
| [`vazamento_de_label.md`](vazamento_de_label.md) | Vazamento de label — mitigações, §9 roteiro para relatório/slides |
| [`FASES.md`](FASES.md) | Índice das fases 1–4 |
| [`FASE1-CLASSIFICACAO.md`](FASE1-CLASSIFICACAO.md) | Fase 1 — TF-IDF + LogReg |
| [`FASE2-CLASSIFICACAO.md`](FASE2-CLASSIFICACAO.md) | Fase 2 — BERTimbau |
| [`FASE3-CLASSIFICACAO.md`](FASE3-CLASSIFICACAO.md) | Fase 3 — TF-IDF + SVM |
| [`FASE4-SUMARIZACAO.md`](FASE4-SUMARIZACAO.md) | Fase 4 — sumarização cidadã |
| [`NOTEBOOK-ENTREGA.md`](NOTEBOOK-ENTREGA.md) | Atalho → [`notebooks/README.md`](../notebooks/README.md) |
| [`../notebooks/README.md`](../notebooks/README.md) | Notebooks: EDA + demo classificação |
| [`validacao_labels/validacao_labels.md`](validacao_labels/validacao_labels.md) | Gabarito, consolidação e status das fichas |
| [`validacao_labels/ficha_*.md`](validacao_labels/) | Ficha individual (4/4 preenchidas — média ≈83,2%) |

## Materiais de referência

| Arquivo | Descrição |
|---|---|
| [`aula03-04.pdf`](referencias/aula03-04.pdf) | Material de aula |

## Documentação técnica (fora de `docs/`)

| Documento | Descrição |
|---|---|
| [`README.md`](../README.md) | Setup, pipeline, ferramentas de dev (ruff, mypy, pytest, Makefile) |
| [`data/raw/README.md`](../data/raw/README.md) | Dados brutos, pipeline de coleta e estrutura do CSV |
| [`pyproject.toml`](../pyproject.toml) | Dependências, ruff, mypy e pytest (fonte canônica) |
| [`Makefile`](../Makefile) | Atalhos: `lint`, `test`, `typecheck`, treino, MLflow UI |

## Ferramentas de desenvolvimento

| Ferramenta | Config | Uso |
|---|---|---|
| **Ruff** | `[tool.ruff]` em `pyproject.toml` | `ruff check src tests` · `ruff format src tests` |
| **Mypy** | `[tool.mypy]` em `pyproject.toml` | `mypy` (analisa só `src/`) |
| **Pytest** | `[tool.pytest.ini_options]` + `tests/` | `pytest` |
| **MLflow** | `src/utils/experiment_tracking.py` | Ver guia §10 e `make mlflow-ui` |

Instalação: `pip install -r requirements-dev.txt` na raiz do repositório.
