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
| **`objeto_html_limpo`** (objeto sem boilerplate) | 123 / 260 | **47,3%** |

**Impacto nas métricas (baseline TF-IDF + LogReg, mesmo split):**

| `text_field` | F1 macro (teste, ref.) | Interpretação |
|--------------|------------------------|---------------|
| `texto` | ≈ 0,88 | Teto **otimista** — vazamento grave |
| `objeto_html` | ≈ 0,74 | Avaliação **oficial** — entrada adotada |
| `objeto_html_limpo` | _(experimento)_ | Limpeza extra; ganho pequeno na Tabela 7 — ver §6.3 |

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

## 5.1 Existe um “limiar universal” de vazamento?

**Não.** Não há padrão do tipo “vazamento ≤ 5%” ou “≤ 10%” válido para todo projeto de ML/PLN.

| O que existe na prática | O que **não** existe |
|-------------------------|----------------------|
| Evitar usar no input a **mesma fonte** do label | Percentual mágico aceitável em todo domínio |
| Comparar entrada contaminada vs honesta (`texto` vs `objeto_html`) | Certificação “zero vazamento” |
| Documentar limitações no relatório | Ignorar vazamento porque F1 ficou alto |

**Para o nosso trabalho:** o critério é **metodológico**, não numérico:

1. Escolhemos a entrada que **não repete o cabeçalho/órgão** (`objeto_html`).
2. Medimos quanto a keyword da área ainda aparece (Tabela 7).
3. Reportamos **F1 ≈ 0,74** (teste), não **≈ 0,88**.
4. Separamos **vazamento** (este doc) de **label proxy** (validação manual).

**~49% residual** em `objeto_html` **não invalida** o experimento: muitas ocorrências são termos legítimos do objeto (“insumo à saúde”, “material da CAESB”). O professor espera **transparência**, não vazamento zero.

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
| `objeto_html_limpo` | ⚗️ experimento (`text_field` alternativo) | mesma limpeza do resumo extrativo |
| Cabeçalho “Pregão Eletrônico” | removido em `objeto_html_limpo` | `limpar_objeto()` no extrativo |

---

## 9. O que explicar no relatório e nos slides

Use este roteiro (copiar/adaptar):

### 9.1 Problema (1 slide ou parágrafo)

> O label da classificação vem do **órgão comprador** (`orgao_csv` → palavras-chave), não de anotação manual. Se o **texto de entrada** repetir o nome do órgão ou a keyword da área, o modelo pode **colar** no label em vez de aprender o conteúdo da compra — isso é **vazamento de label**.

### 9.2 O que fizemos (evidência)

> Medimos na EDA (Tabela 7, 260 editais com keyword de área): com `texto` completo, **96,9%** ainda expõem a área; com **`objeto_html`**, **49,2%**. Por isso adotamos `objeto_html` como entrada — F1 macro no teste **≈ 0,74**, não **≈ 0,88** (run `classification_baseline_20260608-190839`).

### 9.3 O que **não** prometemos

> Não há limiar universal de “quanto pode vazar”. **~49%** residual é esperado enquanto o label vier do órgão e o objeto citar saúde/saneamento. Implementamos limpeza opcional (`objeto_html_limpo`, **47,3%**) — ganho modesto; **entrada oficial permanece `objeto_html`**.

### 9.4 Label proxy (complemento — outro slide)

> O mapeamento órgão → área é **proxy**. Validamos manualmente 30 editais (1/4 fichas): **96,2%** de concordância. Isso trata a **qualidade do rótulo**, não substitui a discussão de vazamento no texto.

### 9.5 Frase de fechamento sugerida

> *“Reduzimos vazamento grosseiro escolhendo `objeto_html`; reportamos métricas honestas e documentamos limitações residual e de label proxy.”*

---

## 10. Checklist para slides e relatório

- [ ] Explicar diferença vazamento vs label proxy (§1)
- [ ] Mostrar Tabela 7 (3 linhas: `texto`, `objeto_html`, `objeto_html_limpo`)
- [ ] Declarar `text_field: objeto_html` como entrada **oficial**
- [ ] Citar F1 ≈ 0,74 (teste), **não** 0,88
- [ ] Dizer que **não há limiar universal** de vazamento (§5.1)
- [ ] Mencionar validação manual do proxy (96,2% parcial)
- [ ] Limitação: ~49% de keyword residual em `objeto_html`

---

## 11. Log de discussão do grupo

_Preencher em reunião — data, quem participou, decisão._

| Data | Participantes | Tópico | Decisão |
|------|-------------|--------|---------|
| _AAAA-MM-DD_ | | Mitigação principal (§4) | |
| | | Run comparativo `texto` (§6.2) | |
| | | Limpeza de texto (§6.3) | |
| | | Texto para slide de limitações | |

---

## 12. Referências no repositório

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
