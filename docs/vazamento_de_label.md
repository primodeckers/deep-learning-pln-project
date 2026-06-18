# Vazamento de label e mitigações — classificação Fase 1

Documento para **discussão do grupo**: o que é vazamento de label no nosso projeto, o que já fazemos para contornar, o que não dá para eliminar totalmente e quais experimentos opcionais valem a pena.

> **Relacionados:** [`FASE1-CLASSIFICACAO.md`](FASE1-CLASSIFICACAO.md) §3 · [`metricas_e_decisoes.md`](metricas_e_decisoes.md) · EDA [`notebooks/01_eda.ipynb`](../notebooks/01_eda.ipynb) (Tabela 7) · [`validacao_labels/validacao_labels.md`](validacao_labels/validacao_labels.md)

---

## 1. Dois problemas diferentes (não confundir)

| Conceito | O que é | Onde aparece |
|----------|---------|--------------|
| **Vazamento de label** (*label leakage*) | O **texto de entrada** repete a informação usada para criar o **rótulo** — o modelo “cola” em vez de generalizar | Tabela 7 da EDA; comparação `texto` vs `objeto_html` |
| **Label proxy** | O **rótulo** vem do órgão (`orgao_csv` → palavras-chave), não de anotação humana edital a edital | `src/preprocess/labels.py`; validação manual de ~30 editais |

Mitigar vazamento ≠ corrigir label proxy. Este documento foca no **vazamento**; o proxy é discutido na validação manual e em [`FASE1-CLASSIFICACAO.md`](FASE1-CLASSIFICACAO.md) §3.1.

---

## 2. Como o label é criado (fonte do vazamento)

1. Lemos `orgao_csv` (ex.: “SECRETARIA DE ESTADO DE SAÚDE - DF”).
2. `area_for_orgao()` em [`src/preprocess/labels.py`](../src/preprocess/labels.py) busca palavras-chave (`SAUDE`, `CAESB`, `BOMBEIRO`, …).
3. A macroárea vira o **label** (`Saude`, `Saneamento`, …).
4. O classificador **não** recebe `orgao_csv` — só o campo de texto escolhido em `configs/classification.yaml` (`text_field`).

**Risco:** se esse mesmo texto contiver “SAÚDE”, “CAESB”, “BOMBEIROS”, o modelo aprende a **reconhecer o órgão no texto**, não necessariamente o **domínio da compra**.

---

## 3. Evidência quantitativa (Tabela 7 — EDA)

Medição (423 editais; **260** com keyword de área — exclui 163 em `Administracao/Outros`):

| Campo de entrada | Com keyword da área no texto | Taxa |
|------------------|------------------------------|------|
| **`texto`** (HTML completo) | 252 / 260 | **96,9%** |
| **`objeto_html`** (só objeto) | 128 / 260 | **49,2%** |

**Impacto nas métricas (baseline TF-IDF + LogReg, mesmo split):**

| `text_field` | F1 macro (teste, ref.) | Interpretação |
|--------------|------------------------|---------------|
| `texto` | ≈ 0,88 | Teto **otimista** — muito vazamento |
| `objeto_html` | ≈ 0,74 | Avaliação **mais honesta** — entrada oficial do projeto |

Run de referência com `objeto_html`: `experiments/classification_baseline_20260608-190839.json`.

---

## 4. Decisão adotada (mitigação principal)

| Medida | Status | Onde |
|--------|--------|------|
| **Não** passar `orgao_csv` ao modelo | ✅ Implementado | `make_dataset()` — label sim, feature não |
| Entrada = **`objeto_html`**, não `texto` | ✅ Implementado | `configs/classification.yaml` → `text_field: objeto_html` |
| Limpeza opcional **`objeto_html_limpo`** | ✅ Implementado | `src/preprocess/clean_objeto.py`; vazamento 47,3% vs 49,2% |
| Documentar vazamento na EDA | ✅ | `notebooks/01_eda.ipynb` §5, Tabela 7 |
| Baseline e BERTimbau no **mesmo** `text_field` | 📋 Fase 2 | Mesmo YAML / split |

**Conclusão para o relatório:** reportamos métricas com `objeto_html`. Runs com `texto` servem só como **contraste** (opcional), nunca como resultado oficial.

---

## 5. O que ainda vaza com `objeto_html` (~49%)

Mesmo sem cabeçalho do órgão, o objeto pode conter:

- termos de domínio (“insumos à saúde”, “material hospitalar”);
- siglas/nomes (“CAESB”, “Corpo de Bombeiros”);
- referências administrativas no corpo do objeto.

Isso **não é bug** — parte é sinal legítimo da compra. O limite é filosófico: o label veio do **órgão**, mas o texto fala do **objeto**.

**Não prometemos** vazamento zero sem mudar a definição do label ou anotar manualmente.

---

## 6. Opções de mitigação (para discutir)

### 6.1 Manter como está — **recomendado para entrega**

- Pipeline atual + Tabela 7 no slide.
- Frase tipo: *“Optamos por `objeto_html` para reduzir vazamento; F1 com `texto` seria teto inflado.”*

| Prós | Contras |
|------|---------|
| Zero esforço extra | ~49% de pista residual documentada |
| Metodologia defensável | Label proxy permanece |

**Voto do grupo:** _[ ] adotado · [ ] revisar_

---

### 6.2 Run comparativo `texto` vs `objeto_html` — **opcional, baixo esforço**

```bash
# oficial (já feito)
python scripts/run_train.py --task classification --model baseline

# contraste — só para slide/relatório
python scripts/run_train.py --task classification --model baseline \
  --config configs/classification.yaml
# (temporariamente alterar text_field para texto no YAML ou via flag, se existir)
```

Tabela de 2 linhas no relatório reforça a decisão da §4.

**Voto do grupo:** _[ ] fazer run de contraste · [ ] não necessário_

---

### 6.3 Limpeza leve do texto — **implementado (experimento)**

Campo derivado **`objeto_html_limpo`** via [`src/preprocess/clean_objeto.py`](../src/preprocess/clean_objeto.py) → `limpar_objeto()`:

| Ação | Implementado |
|------|--------------|
| Remover prefixo `Objeto:` | ✅ |
| Remover `Pregão Eletrônico -` / modalidades similares | ✅ |
| Mascarar nome do órgão se repetido no objeto | ✅ (heurística) |

**Medição (Tabela 7, 260 editais com keyword):**

| Campo | Taxa de vazamento |
|-------|-------------------|
| `objeto_html` | 49,2% (128/260) |
| `objeto_html_limpo` | **47,3%** (123/260) |

Ganho modesto (~2 p.p.) — termos de domínio legítimos permanecem. Entrada **oficial** do pipeline: `objeto_html`. Para experimentar:

```yaml
# configs/classification.yaml
text_field: objeto_html_limpo
```

**Voto do grupo:** _[ ] adotar como oficial · [x] manter objeto_html · [ ] testar run comparativo_

---

### 6.4 Mudar o label (conteúdo do objeto, não órgão) — **fora do escopo atual**

Exigiria anotação manual ou modelo auxiliar de alto custo. A validação manual (~30 editais) avalia o **proxy por órgão**, não substitui rotular 423 editais pelo objeto.

**Voto do grupo:** _[ ] manter proxy · [ ] explorar subset anotado_

---

## 7. O que NÃO fazer

| Prática | Por quê evitar |
|---------|----------------|
| Treinar só com `texto` e reportar F1 ≈ 0,88 como principal | Vazamento evidente; contradiz EDA |
| Incluir `orgao_csv` como feature TF-IDF/BERT | Tarefa vira lookup, não PLN |
| Stripping agressivo de palavras de domínio | Remove sinal real (“medicamento”, “obra”) |
| Ignorar Tabela 7 na apresentação | Perde o argumento metodológico |

---

## 8. Uso por tarefa (o que tirar / o que manter)

| Campo | Classificação | Sumarização cidadã |
|-------|---------------|-------------------|
| `orgao_csv` | ❌ nunca como feature | ✅ contexto no extrativo |
| `texto` | ❌ evitar (vazamento) | ✅ texto completo |
| `objeto_html` | ✅ **entrada oficial** | referência fraca (ROUGE) |
| Cabeçalho “Pregão Eletrônico” | opcional limpar | irrelevante |

---

## 9. Checklist para slides e relatório

- [ ] Explicar diferença vazamento vs label proxy (§1)
- [ ] Mostrar Tabela 7 ou figura equivalente
- [ ] Declarar `text_field: objeto_html` como entrada oficial
- [ ] Citar F1 ≈ 0,74 (teste), não 0,88
- [ ] Mencionar validação manual do proxy (96,2% parcial)
- [ ] Limitação: ~49% de keyword residual em `objeto_html`

---

## 10. Log de discussão do grupo

_Preencher em reunião — data, quem participou, decisão._

| Data | Participantes | Tópico | Decisão |
|------|-------------|--------|---------|
| _AAAA-MM-DD_ | | Mitigação principal (§4) | |
| | | Run comparativo `texto` (§6.2) | |
| | | Limpeza de texto (§6.3) | |
| | | Texto para slide de limitações | |

---

## 11. Referências no repositório

| Artefato | Caminho |
|----------|---------|
| Keywords e label | `src/preprocess/labels.py` |
| Limpeza de objeto | `src/preprocess/clean_objeto.py` |
| Campo de texto no dataset | `src/preprocess/dataset.py` |
| Config | `configs/classification.yaml` |
| EDA Tabela 7 | `notebooks/01_eda.ipynb` |
| Model card | `docs/model_card.md` |

---

*Documento vivo — atualizar após reunião do grupo ou novos experimentos.*
