# deep-learning-pln-project

Projeto final de **Deep Learning e PLN** — modalidade PLN no Setor Público (grupo de 4 pessoas).

**Tema:** processamento de linguagem natural aplicado a **editais de licitações públicas** (ComprasNet, DF 2025).

> O CSV em `data/raw/` indexa as licitações; os **links da coluna Edital** apontam para o corpus textual da rede neural.

---

## Documentação

| Documento | O que contém |
|---|---|
| [`docs/PROJECT-REQUIREMENTS.md`](docs/PROJECT-REQUIREMENTS.md) | Requisitos oficiais da disciplina |
| [`docs/UNIVERSAL-DEEP-LEARNING-GUIDE.md`](docs/UNIVERSAL-DEEP-LEARNING-GUIDE.md) | Guia vivo do projeto — escopo, cronograma, decisões |
| [`docs/DATA-COLLECTION-DECISIONS.md`](docs/DATA-COLLECTION-DECISIONS.md) | Decisões de coleta (CAPTCHA, HTML vs PDF, pipeline) |
| [`docs/TRABALHO-CONSOLIDADO.md`](docs/TRABALHO-CONSOLIDADO.md) | Relatório narrativo consolidado (ComprasNet + PNCP) |
| [`docs/REGRAS-E-PROTOCOLOS.md`](docs/REGRAS-E-PROTOCOLOS.md) | Regras de rotulagem, limpeza e protocolos `pncp*` |
| [`docs/APRESENTACAO-CONTEUDO.md`](docs/APRESENTACAO-CONTEUDO.md) | Roteiro de slides (10 min) |
| [`docs/MODEL-CARD.md`](docs/MODEL-CARD.md) | Model card — performance, dados, limitações dos modelos |
| [`docs/METRICAS-E-DECISOES.md`](docs/METRICAS-E-DECISOES.md) | Métricas, anti-leakage e decisões de avaliação |
| [`docs/VAZAMENTO-DE-LABEL.md`](docs/VAZAMENTO-DE-LABEL.md) | Vazamento de label — mitigações, limiar universal, roteiro para relatório |
| [`docs/GPU-EQUIPE.md`](docs/GPU-EQUIPE.md) | Fluxo GPU vs CPU — treino BERT no grupo |
| [`docs/FASE1-CLASSIFICACAO.md`](docs/FASE1-CLASSIFICACAO.md) | Fase 1 — decisões técnicas, padrões e justificativas |
| [`docs/FASE2-CLASSIFICACAO.md`](docs/FASE2-CLASSIFICACAO.md) | Fase 2 — BERTimbau, comparação baseline, textos para relatório |
| [`docs/FASES.md`](docs/FASES.md) | Índice das fases 1–3 |
| [`docs/FASE3-CLASSIFICACAO.md`](docs/FASE3-CLASSIFICACAO.md) | Fase 3 — TF-IDF + SVM |
| [`notebooks/README.md`](notebooks/README.md) | Notebooks — EDA e demo (sem treino) |
| [`docs/VALIDACAO-LABELS/VALIDACAO-LABELS.md`](docs/VALIDACAO-LABELS/VALIDACAO-LABELS.md) | Gabarito da validação manual de labels |
| [`docs/VALIDACAO-LABELS/`](docs/VALIDACAO-LABELS/) | Ficha individual de cada integrante |
| [`docs/README.md`](docs/README.md) | Índice de todos os arquivos em `docs/` |
| [`data/raw/README.md`](data/raw/README.md) | Dados brutos — CSV, HTMLs coletados, como reproduzir a coleta |

---

## Estrutura do repositório

```
├── configs/          # hiperparâmetros (YAML)
├── docs/             # documentação do projeto
├── data/             # raw → interim → processed
├── experiments/      # registros de experimentos (JSON + MLflow local)
├── models/           # checkpoints (não versionados)
├── notebooks/        # 01_eda · 02_demo_classificacao (sem treino)
├── reports/          # figuras e slides
├── scripts/          # pontos de entrada do pipeline
├── src/              # código reutilizável
├── tests/            # testes automatizados (pytest)
├── pyproject.toml    # dependências, ruff, mypy, pytest
├── Makefile          # atalhos (lint, test, treino, MLflow)
└── requirements*.txt # atalhos para pip install -e .
```

---

## Ambiente virtual (`.venv`)

Cada integrante deve usar um ambiente Python isolado na pasta `.venv/`. Essa pasta **não vai para o Git** — cada pessoa cria localmente após clonar o repositório.

### Pré-requisito

- Python 3.10+ instalado (`python --version`)

### 1. Primeira configuração (uma vez por máquina)

```bash
git clone https://github.com/primodeckers/deep-learning-pln-project.git
cd deep-learning-pln-project

python -m venv .venv
source .venv/Scripts/activate    # Git Bash (Windows)
pip install -r requirements-dev.txt
```

Isso instala o pacote em modo editável (`pip install -e .[dev]`) com runtime + ferramentas de desenvolvimento (pytest, ruff, mypy).

Só para rodar o pipeline, sem dev tools: `pip install -r requirements.txt`

**BERTimbau (Fase 2):** após o install acima, adicione PyTorch + Transformers:

```bash
pip install -e ".[bert]"
# ou: pip install -r requirements-bert.txt
```

**Trabalho em grupo (GPU vs CPU):** quem tem placa treina BERT; demais rodam baseline. Sem branch separada — ver [`docs/GPU-EQUIPE.md`](docs/GPU-EQUIPE.md).

```bash
python scripts/check_cuda.py
python scripts/run_train.py --config configs/classification_bert_gpu.yaml   # GPU
python scripts/run_train.py --model baseline          # qualquer PC
```

**PowerShell:** `.venv\Scripts\Activate.ps1`  
**CMD:** `.venv\Scripts\activate.bat`

No VS Code: **Python: Select Interpreter** → `.venv\Scripts\python.exe` e recarregue a janela após o install.

### 2. Uso no dia a dia

```bash
cd deep-learning-pln-project
source .venv/Scripts/activate
```

O prompt deve mostrar `(.venv)`. Confirme com `which python` (Git Bash).

### 3. Rodar o pipeline

```bash
# coleta e pré-processamento (já executados no repo de referência)
python scripts/run_collect.py
python scripts/run_preprocess.py

# treino e avaliação
python scripts/run_train.py --model baseline

# EDA (exploração — sem treino)
jupyter notebook notebooks/01_eda.ipynb

# Demo para apresentação (métricas + inferência — sem treino)
jupyter notebook notebooks/02_demo_classificacao.ipynb
```

Opções úteis:

| Comando | O que faz |
|---------|-----------|
| `run_collect.py --limit 5` | Coleta só 5 HTMLs (teste) |
| `run_preprocess.py --overwrite` | Reprocessa textos já extraídos |
| `run_train.py --config configs/classification_bert_gpu.yaml` | BERTimbau (GPU recomendada) |
| `python scripts/check_cuda.py` | Verifica se PyTorch vê a placa |

Configuração de classificação: `configs/classification.yaml` (`text_field: objeto_html`, split 70/15/15, `seed: 42`).

> **Corpus completo (423 editais):** o JSONL só inclui licitações cujo HTML está em `data/raw/detalhes/`. Após clonar o repo, se `licitacoes_corpus.jsonl` tiver **menos de 423 linhas**, rode a coleta e o preprocess:
>
> ```bash
> python scripts/run_collect.py          # baixa HTMLs (requer rede)
> python scripts/run_preprocess.py --overwrite
> ```
>
> Confira em `data/processed/preprocess_manifest.json` (`records_written` e `missing_html`).

### 4. Qualidade de código e testes

Lista canônica de dependências em `pyproject.toml`. Atalhos via `Makefile` (se `make` estiver instalado) ou comandos diretos:

| Makefile | Equivalente direto | O que faz |
|----------|-------------------|-----------|
| `make install-dev` | `pip install -r requirements-dev.txt` | Ambiente completo |
| `make lint` | `ruff check src tests && ruff format --check src tests` | Lint + formatação |
| `make lint-fix` | `ruff check --fix src tests && ruff format src tests` | Corrige o automático |
| `make typecheck` | `mypy` | Tipos estáticos em `src/` |
| `make test` | `pytest` | Suite de testes |
| `make train-baseline` | `python scripts/run_train.py --model baseline` | Treina baseline |
| `make train-svm` | `python scripts/run_train.py --model svm` | Treina TF-IDF + SVM (comparativo) |
| `make train-bert` | `python scripts/run_train.py --model bertimbau` | Fine-tune BERTimbau (requer `.[bert]`) |
| `make mlflow-ui` | `mlflow ui --backend-store-uri sqlite:///experiments/mlflow.db` | UI local |

```bash
# fluxo típico antes de commitar
ruff check src tests && ruff format --check src tests
mypy
pytest
```

Testes usam `tests/fixtures/minimal_corpus.jsonl` por padrão; um teste de integração com o corpus real só roda se `data/processed/licitacoes_corpus.jsonl` existir.

**VS Code:** extensões **Ruff** e **Mypy Type Checker** leem `pyproject.toml` automaticamente. Se o Mypy falhar com “connection to server”, confirme o interpretador `.venv` e que `pip install -r requirements-dev.txt` foi executado.

### 5. Adicionar dependências

```bash
pip install nome-do-pacote
# atualize [project.dependencies] ou [project.optional-dependencies.dev] em pyproject.toml
pip install -e ".[dev]"   # reinstala em modo editável
```

### 6. Desativar / recriar

```bash
deactivate
# recriar: rm -rf .venv && python -m venv .venv && pip install -r requirements-dev.txt
```

---

## Status do pipeline

| Etapa | Saída | Status |
|---|---|---|
| Coleta HTML | `data/raw/detalhes/` (423 arquivos) | Concluído |
| Pré-processamento | `data/processed/licitacoes_corpus.jsonl` (423 registros) | Concluído |
| Classificação — baseline TF-IDF + LogReg | `experiments/classification_baseline_20260624-013836.json` | Concluído — **modelo principal** (F1 macro teste **0,74**) |
| Validação manual de labels (proxy) | `docs/VALIDACAO-LABELS/` | Concluído (4/4 fichas — média ≈ 83,2%) |
| Classificação — BERTimbau (Fase 2) | `experiments/classification_bertimbau_20260624-013908.json` | Concluído (F1 teste **0,40** — comparativo DL) |
| Classificação — TF-IDF + SVM (Fase 3) | `experiments/classification_svm_20260624-013851.json` | Concluído (F1 teste **0,65**) — [`FASE3-CLASSIFICACAO.md`](docs/FASE3-CLASSIFICACAO.md) |
| EDA | `notebooks/01_eda.ipynb` | Concluído |
| Demo classificação (Fases 1–3) | `notebooks/02_demo_classificacao.ipynb` | Só lê `experiments/` — ver [`notebooks/README.md`](notebooks/README.md) |
| **PNCP DF/2025** — corpus + EDA | `pncp_corpus_df2025.jsonl` · `03_eda_pncp.ipynb` | Concluído (19.944) |
| **PNCP** — protocolo `pncp` (6 macroáreas) | BERT F1 teste **0,858** | Concluído |
| **PNCP** — protocolo `pncp9fbi` (9 setores + info) | BERT F1 teste **0,955** | Concluído (exploratório) |

Rodar (ou use `make train-baseline` / `make train-svm` / `make train-bert`):

```bash
python scripts/run_train.py --model baseline
python scripts/run_train.py --model svm
jupyter notebook notebooks/01_eda.ipynb     # EDA
jupyter notebook notebooks/02_demo_classificacao.ipynb  # demo apresentação
```

Resultados e decisões metodológicas: [`docs/MODEL-CARD.md`](docs/MODEL-CARD.md) e [`docs/METRICAS-E-DECISOES.md`](docs/METRICAS-E-DECISOES.md).

### Rastreamento de experimentos (MLflow)

Cada treino grava **dois registros**:

| Saída | Onde | Versionado no Git? |
|---|---|---|
| Resumo portátil | `experiments/<run_id>.json` | Sim (runs relevantes) |
| UI comparativa | `experiments/mlflow.db` + `experiments/mlartifacts/` | Não (local, gitignored) |

O JSON e o MLflow incluem **parâmetros**, **métricas**, **hash do corpus** (`dataset.sha256`) e **commit Git** quando disponível.

```bash
# após um ou mais treinos (ou: make mlflow-ui)
mlflow ui --backend-store-uri sqlite:///experiments/mlflow.db
# abrir http://127.0.0.1:5000 — experimento "pln-licitacoes"
```

Detalhes: [`docs/UNIVERSAL-DEEP-LEARNING-GUIDE.md`](docs/UNIVERSAL-DEEP-LEARNING-GUIDE.md) §10.

---

## Integrantes

| Nome | GitHub |
|---|---|
| Elisangela Osorio | [ElisangelaOsorio](https://github.com/ElisangelaOsorio) |
| Alexandre Ferreira Ponte | [pontealexandre](https://github.com/pontealexandre) |
| Renê Estevam Deckers | [primodeckers](https://github.com/primodeckers) |
| Alexandre Hugo Sampaio Netto| [xnetto2](https://github.com/xnetto2) |

---

## Licença

MIT — ver [`LICENSE`](LICENSE).
