# deep-learning-pln-project

Projeto final de **Deep Learning e PLN** — modalidade **PLN no Setor Público** (grupo de 4).

**Tema:** classificação automática de editais e compras públicas por **área de gasto** (ComprasNet + PNCP, DF/2025).

**Escopo:** só **classificação textual** (Fases 1–3 no ComprasNet + protocolos PNCP). Sumarização **não faz parte** desta entrega.

> Dados inéditos coletados pelo grupo (sem Kaggle). O CSV em `data/raw/` indexa licitações; o HTML de detalhe alimenta o corpus textual.

---

## Comece por aqui

| Documento | Papel |
|-----------|--------|
| [`docs/TRABALHO-CONSOLIDADO.md`](docs/TRABALHO-CONSOLIDADO.md) | **Relatório narrativo completo** (estrutura da disciplina) |
| [`docs/REGRAS-E-PROTOCOLOS.md`](docs/REGRAS-E-PROTOCOLOS.md) | Rotulagem, limpeza, família `pncp*` |
| [`docs/roteiro_10min.md`](docs/roteiro_10min.md) | Roteiro falado da apresentação (10 min) |
| [`docs/ROTEIRO-FAMILIA-PROTOCOLOS-PNCP.md`](docs/ROTEIRO-FAMILIA-PROTOCOLOS-PNCP.md) | Slide família de protocolos PNCP |
| [`docs/README.md`](docs/README.md) | Índice de toda a pasta `docs/` |

---

## Dois corpora, um problema

| Corpus | Registros | Papel | Melhor modelo (F1 macro teste) |
|--------|----------:|-------|--------------------------------|
| **ComprasNet** HTML | 423 | **Entrega oficial** | **TF-IDF + LogReg 0,74** |
| **PNCP** DF/2025 | 19.944 | Extensão em escala | **BERTimbau 0,86** (`pncp`) |

Mesma pergunta: *em que áreas o governo está comprando?* (rotulagem temática — **não** estimativa de valor em reais nesta entrega).

**Achado central:** com poucos dados o clássico vence; com ~20 mil o Transformer vence — lema **“depende”** da disciplina.

---

## Documentação

| Documento | O que contém |
|-----------|--------------|
| [`docs/PROJECT-REQUIREMENTS.md`](docs/PROJECT-REQUIREMENTS.md) | Requisitos oficiais da disciplina |
| [`docs/TRABALHO-CONSOLIDADO.md`](docs/TRABALHO-CONSOLIDADO.md) | Relatório consolidado (ComprasNet + PNCP) |
| [`docs/REGRAS-E-PROTOCOLOS.md`](docs/REGRAS-E-PROTOCOLOS.md) | Regras e protocolos `pncp` / `pncp9*` |
| [`docs/METRICAS-E-DECISOES.md`](docs/METRICAS-E-DECISOES.md) | Métricas, anti-leakage, decisões |
| [`docs/MODEL-CARD.md`](docs/MODEL-CARD.md) | Model card — performance e limitações |
| [`docs/VAZAMENTO-DE-LABEL.md`](docs/VAZAMENTO-DE-LABEL.md) | Vazamento de label e mitigações |
| [`docs/COMPARATIVO-FASES.md`](docs/COMPARATIVO-FASES.md) | Val vs teste (Fases 1–3) |
| [`docs/FASES.md`](docs/FASES.md) | Índice Fases 1–3 (ComprasNet) |
| [`docs/FASE1-CLASSIFICACAO.md`](docs/FASE1-CLASSIFICACAO.md) | TF-IDF + LogReg |
| [`docs/FASE2-CLASSIFICACAO.md`](docs/FASE2-CLASSIFICACAO.md) | BERTimbau |
| [`docs/FASE3-CLASSIFICACAO.md`](docs/FASE3-CLASSIFICACAO.md) | TF-IDF + SVM |
| [`docs/APRESENTACAO-CONTEUDO.md`](docs/APRESENTACAO-CONTEUDO.md) | Conteúdo ampliado dos slides |
| [`docs/roteiro_10min.md`](docs/roteiro_10min.md) | Roteiro falado 10 min |
| [`docs/ROTEIRO-FAMILIA-PROTOCOLOS-PNCP.md`](docs/ROTEIRO-FAMILIA-PROTOCOLOS-PNCP.md) | Família `pncp*` (fala) |
| [`docs/UNIVERSAL-DEEP-LEARNING-GUIDE.md`](docs/UNIVERSAL-DEEP-LEARNING-GUIDE.md) | Guia vivo do projeto |
| [`docs/DATA-COLLECTION-DECISIONS.md`](docs/DATA-COLLECTION-DECISIONS.md) | Coleta (CAPTCHA, HTML vs PDF) |
| [`docs/HIPERPARAMETROS-E-MELHORIAS.md`](docs/HIPERPARAMETROS-E-MELHORIAS.md) | Tuning e backlog |
| [`docs/GPU-EQUIPE.md`](docs/GPU-EQUIPE.md) | Fluxo GPU vs CPU |
| [`docs/VALIDACAO-LABELS/`](docs/VALIDACAO-LABELS/) | Validação humana do label proxy (~83%) |
| [`notebooks/README.md`](notebooks/README.md) | EDA e demo (sem treino) |
| [`experiments/README.md`](experiments/README.md) | Runs oficiais versionados |
| [`data/raw/README.md`](data/raw/README.md) | Dados brutos e coleta |

---

## Modelos (família de arquitetura)

| Modelo | Família | Rede neural? | Papel |
|--------|---------|--------------|--------|
| TF-IDF + **LogReg** | ML clássico (linear) | Não | **Principal** no ComprasNet (F1 0,74) |
| TF-IDF + **SVM** | ML clássico (margem) | Não | Comparativo |
| **BERTimbau** | **Transformer** (encoder) | Sim | Comparativo DL; **melhor** no PNCP `pncp` (F1 0,86) |

**Não usamos CNN** (visão/grades) nem **RNN/LSTM** (legado sequencial — o experimento de DL é o Transformer).

---

## Protocolos PNCP (IDs curtos)

| ID | Significado |
|----|-------------|
| `pncp` | 6 macroáreas por **órgão** — honesto em escala |
| `pncp9` | 9 setores, só linhas com keyword no objeto |
| `pncp9full` | 9 setores + **Indeterminado**, todas as linhas |
| `pncp9fb` | 9 setores + **fallback órgão** |
| `pncp9fbi` | fallback + **info complementar** |

Detalhe: [`docs/REGRAS-E-PROTOCOLOS.md`](docs/REGRAS-E-PROTOCOLOS.md) · fala: [`docs/ROTEIRO-FAMILIA-PROTOCOLOS-PNCP.md`](docs/ROTEIRO-FAMILIA-PROTOCOLOS-PNCP.md).

---

## Estrutura do repositório

```
├── configs/          # hiperparâmetros (YAML) — classification*.yaml, pncp*
├── docs/             # documentação do projeto
├── data/             # raw → interim → processed
├── experiments/      # registros de experimentos (JSON + MLflow local)
├── models/           # checkpoints (não versionados)
├── notebooks/        # 01_eda · 02_demo_classificacao · 03_eda_pncp
├── reports/          # figuras e slides
├── scripts/          # pontos de entrada do pipeline
├── src/              # código reutilizável (sem módulo de sumarização)
├── tests/            # pytest
├── pyproject.toml
├── Makefile
└── requirements*.txt
```

---

## Ambiente virtual (`.venv`)

Cada integrante usa um ambiente Python isolado em `.venv/` (**não** vai para o Git).

### Pré-requisito

- Python 3.10+ (`python --version`)

### 1. Primeira configuração

```bash
git clone https://github.com/primodeckers/deep-learning-pln-project.git
cd deep-learning-pln-project

python -m venv .venv
source .venv/Scripts/activate    # Git Bash (Windows)
pip install -r requirements-dev.txt
```

Só pipeline, sem dev tools: `pip install -r requirements.txt`

**BERTimbau:**

```bash
pip install -e ".[bert]"
# ou: pip install -r requirements-bert.txt
```

**GPU vs CPU:** quem tem placa treina BERT; demais rodam baseline — [`docs/GPU-EQUIPE.md`](docs/GPU-EQUIPE.md).

```bash
python scripts/check_cuda.py
python scripts/run_train.py --config configs/classification_bert_gpu.yaml
python scripts/run_train.py --model baseline
```

**PowerShell:** `.venv\Scripts\Activate.ps1` · **CMD:** `.venv\Scripts\activate.bat`

### 2. Uso no dia a dia

```bash
cd deep-learning-pln-project
source .venv/Scripts/activate
```

### 3. Pipeline

```bash
# ComprasNet
python scripts/run_collect.py
python scripts/run_preprocess.py
python scripts/run_train.py --model baseline

# PNCP (após planilha em data/)
python scripts/run_preprocess_pncp.py
python scripts/run_train.py --model bertimbau \
  --config configs/classification_pncp.yaml \
  --corpus data/processed/pncp_corpus_df2025.jsonl

# EDA / demo (sem treino)
jupyter notebook notebooks/01_eda.ipynb
jupyter notebook notebooks/02_demo_classificacao.ipynb
jupyter notebook notebooks/03_eda_pncp.ipynb
```

| Comando | O que faz |
|---------|-----------|
| `run_collect.py --limit 5` | Coleta só 5 HTMLs (teste) |
| `run_preprocess.py --overwrite` | Reprocessa textos |
| `run_train.py --config configs/classification_bert_gpu.yaml` | BERTimbau (GPU) |
| `run_benchmark_pncp_dificeis.py` | Coortes difíceis PNCP |

Config ComprasNet: `configs/classification.yaml` (`text_field: objeto_html` ou `objeto_html_limpo`, split 70/15/15, `seed: 42`).

> **Corpus 423 editais:** se `licitacoes_corpus.jsonl` tiver menos de 423 linhas após clonar:
>
> ```bash
> python scripts/run_collect.py
> python scripts/run_preprocess.py --overwrite
> ```

### 4. Qualidade de código e testes

| Makefile | Equivalente | O que faz |
|----------|-------------|-----------|
| `make install-dev` | `pip install -r requirements-dev.txt` | Ambiente completo |
| `make lint` | `ruff check src tests && ruff format --check src tests` | Lint |
| `make lint-fix` | `ruff check --fix src tests && ruff format src tests` | Corrige |
| `make typecheck` | `mypy` | Tipos |
| `make test` | `pytest` | Testes |
| `make train-baseline` | `python scripts/run_train.py --model baseline` | LogReg |
| `make train-svm` | `python scripts/run_train.py --model svm` | SVM |
| `make train-bert` | `python scripts/run_train.py --model bertimbau` | BERT |
| `make mlflow-ui` | `mlflow ui --backend-store-uri sqlite:///experiments/mlflow.db` | UI |

```bash
ruff check src tests && ruff format --check src tests
mypy
pytest
```

### 5. Dependências e recriar venv

```bash
pip install nome-do-pacote
# atualize pyproject.toml
pip install -e ".[dev]"

deactivate
# rm -rf .venv && python -m venv .venv && pip install -r requirements-dev.txt
```

---

## Status do pipeline

| Etapa | Saída | Status |
|-------|-------|--------|
| Coleta HTML ComprasNet | `data/raw/detalhes/` (423) | Concluído |
| Pré-processamento ComprasNet | `licitacoes_corpus.jsonl` (423) | Concluído |
| **Fase 1** TF-IDF + LogReg | `classification_baseline_20260624-013836` | **Principal** — F1 teste **0,74** |
| **Fase 2** BERTimbau | `classification_bertimbau_20260624-013908` | Comparativo — F1 **0,40** |
| **Fase 3** TF-IDF + SVM | `classification_svm_20260624-013851` | Comparativo — F1 **0,65** |
| Validação humana de labels | `docs/VALIDACAO-LABELS/` | ~83,2% (4/4 fichas) |
| EDA ComprasNet / PNCP | `01_eda` · `03_eda_pncp` | Concluído |
| Demo classificação | `02_demo_classificacao.ipynb` | Só lê `experiments/` |
| PNCP corpus | `pncp_corpus_df2025.jsonl` (19.944) | Concluído |
| PNCP `pncp` | BERT F1 **0,858** | Concluído |
| PNCP `pncp9fbi` | BERT F1 **0,955** | Exploratório (ressalvas) |

```bash
make train-baseline   # ou: python scripts/run_train.py --model baseline
make train-svm
make train-bert
```

Números e decisões: [`docs/MODEL-CARD.md`](docs/MODEL-CARD.md) · [`docs/METRICAS-E-DECISOES.md`](docs/METRICAS-E-DECISOES.md).

### MLflow

| Saída | Onde | No Git? |
|-------|------|---------|
| Resumo portátil | `experiments/<run_id>.json` | Sim (runs oficiais) |
| UI | `experiments/mlflow.db` | Não (local) |

```bash
make mlflow-ui
# http://127.0.0.1:5000 — experimento "pln-licitacoes"
```

---

## Integrantes

| Nome | GitHub |
|------|--------|
| Elisangela Osorio | [ElisangelaOsorio](https://github.com/ElisangelaOsorio) |
| Alexandre Ferreira Ponte | [pontealexandre](https://github.com/pontealexandre) |
| Renê Estevam Deckers | [primodeckers](https://github.com/primodeckers) |
| Alexandre Hugo Sampaio Netto | [xnetto2](https://github.com/xnetto2) |

---

## Licença

MIT — ver [`LICENSE`](LICENSE).
