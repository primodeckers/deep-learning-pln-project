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
| [`docs/PROPOSALS.md`](docs/PROPOSALS.md) | Propostas de tema/tarefa de PLN (brainstorm do grupo) |
| [`docs/README.md`](docs/README.md) | Índice de todos os arquivos em `docs/` |
| [`data/raw/README.md`](data/raw/README.md) | Dados brutos — CSV, HTMLs coletados, como reproduzir a coleta |

---

## Estrutura do repositório

```
├── docs/             # documentação do projeto
├── data/             # raw → interim → processed
├── configs/          # hiperparâmetros
├── experiments/      # registros de experimentos
├── models/           # checkpoints (não versionados)
├── notebooks/        # exploração e EDA
├── reports/          # figuras e slides
├── scripts/          # pontos de entrada do pipeline
└── src/              # código reutilizável
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
pip install -r requirements.txt
```

**PowerShell:** `.venv\Scripts\Activate.ps1`  
**CMD:** `.venv\Scripts\activate.bat`

### 2. Uso no dia a dia

```bash
cd deep-learning-pln-project
source .venv/Scripts/activate
```

O prompt deve mostrar `(.venv)`. Confirme com `which python` (Git Bash).

### 3. Rodar o pipeline

```bash
python scripts/run_collect.py
python scripts/run_preprocess.py
```

Opções: `--limit 5` (teste) · `--overwrite` (reprocessar)

### 4. Adicionar dependências

```bash
pip install nome-do-pacote
# atualize requirements.txt para o grupo
```

### 5. Desativar / recriar

```bash
deactivate
# recriar: rm -rf .venv && python -m venv .venv && pip install -r requirements.txt
```

Detalhes completos: seção acima ou pergunte no grupo.

---

## Status do pipeline

| Etapa | Saída | Status |
|---|---|---|
| Coleta HTML | `data/raw/detalhes/` (423 arquivos) | Concluído |
| Pré-processamento | `data/processed/licitacoes_corpus.jsonl` | Concluído |
| Classificação — baseline TF-IDF + LogReg | `experiments/classification_baseline_*.json` | Concluído (F1 macro ≈ 0,74 com `objeto_html`) |
| Classificação — BERTimbau | `src/models/bert_classifier.py` | Pendente (Fase 2) |
| EDA | `notebooks/01_eda.ipynb` | Concluído |
| Sumarização cidadão — baseline extrativo | `reports/slides/resumos_exemplos.md` | Concluído |
| Sumarização — abstrativo (mT5/LLM) | — | Pendente (Fase 3) |

Rodar:

```bash
python scripts/run_train.py --task classification --model baseline
python scripts/run_train.py --task summarization --model extractive
jupyter notebook notebooks/01_eda.ipynb     # análise exploratória
```

---

## Integrantes

| Nome | GitHub |
|---|---|
| Elisangela Osorio | [ElisangelaOsorio](https://github.com/ElisangelaOsorio) |
| Alexandre Ferreira Ponte | [pontealexandre](https://github.com/pontealexandre) |
| Renê Estevam Deckers | [primodeckers](https://github.com/primodeckers) |
| _a definir_ | [xnetto2](https://github.com/xnetto2) |

---

## Licença

MIT — ver [`LICENSE`](LICENSE).
