# Regras e protocolos implementados

Referência única das regras de **rotulagem**, **limpeza de texto**, **montagem de corpus**, **split** e **protocolos de treino**. Código: `src/preprocess/labels.py`, `labels_setores.py`, `clean_objeto.py`, `dataset.py`.

---

## 1. Normalização (base de todas as keywords)

- Texto → NFKD → remove acentos → **MAIÚSCULAS**
- Casamento por **substring** (`kw in texto_normalizado`)

---

## 2. Rótulo por órgão — 6 macroáreas (`label_scheme: orgao`)

**Protocolo:** `pncp` · **Arquivo:** `labels.py`

| Ordem | Classe | Keywords no `orgao_csv` |
|------:|--------|-------------------------|
| 1 | Saúde | SAUDE, HEMOCENTRO |
| 2 | Saneamento | CAESB, SANEAMENTO |
| 3 | Segurança | POLICIA, BOMBEIRO, SEGURANCA, PENITENCI |
| 4 | Educação | EDUCACAO |
| 5 | Infraestrutura/Obras | ESTRADAS, RODAGEM, OBRAS, INFRAESTRUTURA |
| — | **Administracao/Outros** | fallback |

**Regras:** primeira keyword vence; o modelo **não** recebe o órgão como feature.

---

## 3. Rótulo por setor — 9 classes (`label_scheme: setores`)

**Arquivo:** `labels_setores.py` · ordem de prioridade fixa:

| Ordem | Setor | Keywords (resumo) |
|------:|-------|-------------------|
| 1 | Saúde | SAUDE, HOSPITAL, MEDIC, CLINIC, FARMAC, ODONTO, LABORATOR, HEMOCENTRO, AMBULANC, ENFERMAG |
| 2 | Educação | EDUCAC, ESCOLA, UNIVERSID, ENSINO, PEDAGOG, ALUNO, BIBLIOTEC |
| 3 | Segurança | POLICI, BOMBEIRO, SEGURANC, PENITENCI, CARCER, GUARDA, DEFESA CIVIL |
| 4 | Saneamento | SANEAMENT, ESGOTO, AGUA POT, CAESB, TRATAMENTO DE EFLUENT, DRENAG |
| 5 | Infraestrutura/Obras | OBRA, PAVIMENT, INFRAESTRUTUR, RODOVI, CONSTRUC, REFORMA |
| 6 | TI/Administracao | SOFTWARE, LICENCA, INFORMAT, COMPUT, SISTEMA, HOSPEDAGEM, MOBILIARIO |
| 7 | Transporte | VEICUL, COMBUSTIV, TRANSPORT, ONIBUS, AUTOMOVEL |
| 8 | Cultura | CULTUR, MUSEU, EVENTO, ARTISTIC |
| 9 | Meio Ambiente | AMBIENT, FLOREST, RESIDUO, RECICL |

Sem keyword → `None`, ou **`Indeterminado`** se `filter_unlabeled: false`.

---

## 4. Fallback híbrido (`label_scheme: setores_fallback_orgao`)

**Protocolos:** `pncp9fb`, `pncp9fbi`

```
1. Keyword no texto (objeto [+ info])?  → setor (fonte: objeto)
2. Senão, órgão em macroárea nomeada?   → mesma macroárea (fonte: orgao)
3. Senão                                → Indeterminado (fonte: indeterminado)
```

`Administracao/Outros` **não** vira setor — vira `Indeterminado`. TI, Transporte, Cultura e Meio Ambiente **só** vêm de keyword no objeto.

---

## 5. Info complementar (`include_info_complementar: true`)

**Protocolo:** `pncp9fbi`

- Concatena `objeto` + `informacao_complementar` para **rotulagem** e para `objeto_info_limpo`
- ~53% das linhas PNCP têm info; ~23% dos vagos ganham setor por keyword na info

---

## 6. Limpeza de texto (`clean_objeto.py`)

### `objeto_html_limpo`

| Regra | Efeito |
|-------|--------|
| Remove `Objeto:` | Até 3 passadas |
| Remove prefixo de modalidade | Pregão, Dispensa, Concorrência, etc. |
| Remove nome do órgão | ≥8 chars; literal ou tokens ≥4 chars |
| Normaliza espaços | Colapsa whitespace |

### `objeto_info_limpo`

- Objeto limpo + info complementar (URLs removidas, espaços normalizados)

---

## 7. Split e filtro (`dataset.py`)

| Regra | Valor |
|-------|-------|
| Partição | 70% treino / 15% val / 15% teste |
| Estratificação | Por classe |
| Seed | 42 |
| `filter_unlabeled: true` | Exclui sem keyword (`pncp9`) |
| `filter_unlabeled: false` | Mantém; sem keyword → Indeterminado |

---

## 8. Corpus PNCP (`build_pncp_corpus.py`)

Filtros opcionais: esfera `D`, UF (ex. `DF`), ano `2025`. Descarta objeto ou órgão vazios.

---

## 9. Coortes do benchmark (`run_benchmark_pncp_dificeis.py`)

| Coorte | Condição |
|--------|----------|
| `com_keyword` | Keyword setorial no objeto |
| `sem_keyword_macroarea_nomeada` | Sem keyword + órgão nomeado (**escondidas**, ~853) |
| `sem_keyword_admin` | Sem keyword + Admin/Outros |

---

## 10. Protocolos de treino (configs)

| ID | Config | Rótulo | Texto | Filtro | Info |
|----|--------|--------|-------|--------|------|
| **ComprasNet 423** | `classification.yaml` | 6 macroáreas (órgão) | `objeto_html` | todos | não |
| **`pncp`** | `classification_pncp.yaml` | 6 macroáreas (órgão) | `objeto_html_limpo` | todos | não |
| **`pncp9`** | `classification_pncp_9setores.yaml` | 9 setores | `objeto_html_limpo` | só keyword | não |
| **`pncp9full`** | `classification_pncp_9setores_full.yaml` | 9 + Indeterminado | `objeto_html_limpo` | todos | não |
| **`pncp9fb`** | `classification_pncp_9setores_fb.yaml` | fallback órgão | `objeto_html_limpo` | todos | não |
| **`pncp9fbi`** | `classification_pncp_9setores_fb_info.yaml` | fallback + info | `objeto_info_limpo` | todos | **sim** |

Comando genérico:

```bash
python scripts/run_train.py --model bertimbau \
  --config configs/classification_pncp_9setores_fb_info.yaml \
  --corpus data/processed/pncp_corpus_df2025.jsonl
```

---

## 11. Regras de modelagem

- `class_weight: balanced` (sklearn)
- BERT: early stopping (patience 2), `fp16` + CUDA quando disponível
- Métrica primária: **F1 macro no teste**
- Relatório oficial ComprasNet 423: **LogReg F1 0,74** (`objeto_html`)

Ver métricas completas: [`METRICAS-E-DECISOES.md`](METRICAS-E-DECISOES.md).
