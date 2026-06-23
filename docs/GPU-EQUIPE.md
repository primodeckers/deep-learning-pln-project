# Fluxo GPU vs CPU — trabalho em grupo

Como treinar **BERTimbau** na máquina com placa (ex.: RTX 4090) sem bloquear quem só tem CPU.

> **Regra:** mesma branch `main` para todos. GPU define **quem executa** o treino pesado, não um fork permanente do código.

---

## 1. Divisão de responsabilidades

| Integrante | Máquina | O que roda |
|------------|---------|------------|
| **Quem tem GPU** | CUDA disponível | BERTimbau (`classification_bert_gpu.yaml`), compartilha métricas + opcionalmente pesos |
| **Demais** | Só CPU | Baseline, EDA, validação labels, slides, sumarização extrativa, docs |

Todos usam o **mesmo repositório** e o **mesmo corpus** (`licitacoes_corpus.jsonl`, 423 editais).

---

## 2. O que vai para o Git (e o que não vai)

| Artefato | Git? | Motivo |
|----------|------|--------|
| Código (`src/`, `scripts/`, `configs/`) | ✅ Sim | Reprodutível por todos |
| `experiments/classification_*_REF.json` | ✅ Sim | Runs **oficiais** de referência |
| `reports/figures/*_confusion.png` (oficiais) | ✅ Sim | Slides e relatório |
| `models/*` (pesos `.bin`, pastas BERT) | ❌ Não | Grande; `.gitignore` |
| `experiments/mlflow.db`, `.bert_cache/` | ❌ Não | Local |
| Runs experimentais descartáveis (`20260618-*` locais) | ❌ Não | Só teste |

**Pesos do BERT** (se alguém precisar inferir fora da GPU): zip no Drive/Discord — caminho anotado no model card ou no WhatsApp do grupo.

---

## 3. Comandos por perfil

### Antes de qualquer treino BERT

```bash
python scripts/check_cuda.py
```

### Quem tem GPU (Renê / máquina com 4090)

```bash
pip install -e ".[bert]"
# PyTorch com CUDA: https://pytorch.org/get-started/locally/

python scripts/check_cuda.py
python scripts/run_train.py --config configs/classification_bert_gpu.yaml
```

### Quem não tem GPU

```bash
pip install -r requirements.txt   # ou requirements-dev.txt — sem [bert] obrigatório

python scripts/run_train.py --task classification --model baseline
```

Smoke test BERT em CPU (opcional, **lento**):

```bash
pip install -e ".[bert]"
python scripts/run_train.py --config configs/classification_bert_cpu.yaml
```

### Sem `make` (Windows)

Use os comandos `python` acima — equivalentes aos atalhos do `Makefile`.

---

## 4. Depois do treino na GPU — checklist do integrante GPU

1. Conferir métricas no terminal e em `experiments/classification_bertimbau_*.json`
2. **Commitar** o JSON + PNG do run **oficial** (se for referência do grupo)
3. **Não commitar** `models/classification_bertimbau_*`
4. Atualizar [`model_card.md`](model_card.md) se o run virar referência
5. Avisar o grupo (métricas + link do commit)

---

## 5. Runs de referência atuais

| Modelo | Run ID | F1 macro (teste) | Onde |
|--------|--------|------------------|------|
| Baseline TF-IDF | `classification_baseline_20260608-190839` | **≈ 0,74** | `experiments/` |
| BERTimbau (1º run) | `classification_bertimbau_20260623-213337` | **≈ 0,40** | `experiments/` |

O primeiro run BERT ficou **abaixo** do baseline — esperado com corpus pequeno (~295 treino) e possível treino em CPU. **Próximo passo:** repetir na **4090 com CUDA** (`check_cuda.py` = sim) e comparar; documentar no relatório mesmo se BERT não superar (resultado válido).

---

## 6. Perguntas frequentes

**Preciso de branch `gpu`?**  
Não. Branch só para **feature em desenvolvimento**; merge na `main` quando estável.

**Colega sem GPU consegue reproduzir o relatório?**  
Sim — baseline + JSON/figuras commitados. BERT completo só quem baixar pesos do Drive ou treinar na GPU.

**Instalar `[bert]` quebra o ambiente de quem não tem GPU?**  
Não — é **opcional** (`pip install -e ".[bert]"`). Baseline não usa torch.

---

## 7. Referências

- Config GPU: [`configs/classification_bert_gpu.yaml`](../configs/classification_bert_gpu.yaml)
- Config CPU smoke: [`configs/classification_bert_cpu.yaml`](../configs/classification_bert_cpu.yaml)
- Código BERT: [`src/models/bert_classifier.py`](../src/models/bert_classifier.py)
- Fase 1 / baseline: [`FASE1-CLASSIFICACAO.md`](FASE1-CLASSIFICACAO.md)
