# Roteiro — slide “Família de protocolos PNCP”

Roteiro falado para **1 slide** (ou 2, se separar tabela e árvore) na apresentação de 10 minutos.

> **Relacionados:** [`APRESENTACAO-CONTEUDO.md`](APRESENTACAO-CONTEUDO.md) · [`REGRAS-E-PROTOCOLOS.md`](REGRAS-E-PROTOCOLOS.md) §10 · [`TRABALHO-CONSOLIDADO.md`](TRABALHO-CONSOLIDADO.md) §5.4 e §6.4 · [`MODEL-CARD.md`](MODEL-CARD.md)

**Tempo sugerido:** 2–3 min  
**Quem fala:** integrante de metodologia / dados  
**Objetivo:** a banca entender **por que existem vários IDs** (`pncp`, `pncp9`, …) e **qual F1 ler em cada contexto**

---

## Slide — título

**Do ComprasNet ao PNCP: família de protocolos**

---

## Abertura (~30 s)

> “A entrega oficial usa **423 editais ComprasNet** — 6 macroáreas, rótulo pelo **órgão**, entrada só no **objeto**.
>
> Depois estendemos com **~20 mil compras PNCP** (DF/2025). Mesma pergunta — *em que área o governo gasta?* — mas textos **mais curtos** e muitos objetos **genéricos**.
>
> Para não comparar coisas diferentes, cada experimento tem um **ID curto** nos JSON e no MLflow. Vou decodificar a família.”

---

## Slide — tabela (copiar na apresentação)

| ID | Nome falado | O que muda |
|----|-------------|------------|
| **ComprasNet** | entrega oficial | 423 editais · 6 áreas · órgão → label |
| **`pncp`** | PNCP honesto | 19.944 · **mesmas 6 áreas** · órgão → label |
| **`pncp9`** | 9 setores, filtrado | Só linhas **com keyword** no objeto (~10,3 mil) |
| **`pncp9full`** | 9 setores, completo | Todas as linhas · sem keyword → **Indeterminado** |
| **`pncp9fb`** | fallback **órgão** | Sem keyword no objeto → label pelo **órgão** |
| **`pncp9fbi`** | fallback + **info** | Igual `fb` + campo **informação complementar** |

**Mnemônico (destaque no slide):**

```
pncp   → PNCP + 6 áreas (igual ComprasNet, em escala)
pncp9  → + 9 setores empíricos
full   → + todas as linhas (Indeterminado)
fb     → + fallback órgão
fbi    → + info complementar
```

Config YAML de referência: `configs/classification_pncp*.yaml`

---

## Decodificar cada nome (~60 s)

> “**`pncp`** — PNCP no protocolo **mais comparável** ao ComprasNet: seis macroáreas, rótulo vem do **nome do órgão**, modelo vê só o objeto limpo. Aqui o BERT fez **F1 0,86** no teste; LogReg **0,76**. É o nosso **protocolo honesto em escala**.
>
> **`pncp9`** — mudamos a taxonomia para **nove setores** (Saúde, TI, Transporte, Cultura…) e o rótulo vem de **palavra-chave no objeto**. Só treinamos onde o objeto **já diz** o setor — por isso **filtramos** para ~10 mil linhas. F1 sobe muito, mas o desafio fica **mais fácil**.
>
> **`pncp9full`** — **full** = corpus **inteiro**, 19.944. Quem não tem keyword vira **Indeterminado** — décima classe.
>
> **`pncp9fb`** — **fb** = **fallback órgão**. Se o objeto é vago — ‘contratação por inexigibilidade’ — usamos plano B: rótulo pela **macroárea do órgão**, como no ComprasNet. Recuperamos compras **escondidas**, ~853, em que o órgão é Saúde ou Polícia mas o texto não ajuda.
>
> **`pncp9fbi`** — **fbi** = fallback + **info** complementar. ~53% das linhas PNCP têm um campo extra; entra no **texto e no rótulo**. BERT chega a **F1 ~0,95** — mas avisamos: há **acoplamento** rótulo↔texto; não é o mesmo que o `pncp` honesto.”

---

## Slide — árvore (opcional)

```
ComprasNet 423 (6 áreas, entrega)
    └── pncp (PNCP, 6 áreas, ~20k)  ← comparável
            └── pncp9 (9 setores, só com keyword)
                    ├── pncp9full (+ Indeterminado, todas)
                    ├── pncp9fb (+ fallback órgão)
                    └── pncp9fbi (+ info complementar)
```

---

## Qual número citar (~45 s)

> “Três mensagens para não confundir a banca:
>
> **1.** Entrega oficial → ComprasNet, LogReg **F1 0,74** (teste, `objeto_html`).
>
> **2.** ‘Deep learning ganha com escala?’ → protocolo **`pncp`**, BERT **F1 0,86** vs LogReg **0,76** — **mesmo desenho** do ComprasNet.
>
> **3.** F1 **0,95–0,97** nos `pncp9*` → exploratório: reproduz **regras de keyword** ou usa **fallback/info**; declaramos isso, não vendemos como generalização cega.
>
> O lema da disciplina é **‘depende’** — depende do **corpus**, do **protocolo** e do **volume**.”

---

## Fechamento do slide (~15 s)

> “Os nomes são IDs de experimento — **`pncp9fb`** não é jargão do governo; é **PNCP + 9 setores + fallback órgão**. Detalhe completo em [`REGRAS-E-PROTOCOLOS.md`](REGRAS-E-PROTOCOLOS.md).”

---

## Perguntas prováveis — respostas curtas

| Pergunta | Resposta |
|----------|----------|
| Por que não só `pncp`? | ~48% dos objetos PNCP são vagos; testamos taxonomias e fallbacks **sem misturar** métricas. |
| Qual é o melhor modelo? | **ComprasNet:** LogReg F1 **0,74**. **PNCP honesto (`pncp`):** BERT F1 **0,86**. |
| `fb` significa o quê? | **Fallback órgão** — plano B quando o objeto não tem keyword setorial. |
| Por que F1 0,97? | Label muitas vezes **é** a keyword do input (`pncp9` / `pncp9fbi`); transparência no relatório. |
| O modelo vê o órgão? | **Não** como feature; fallback afeta só o **rótulo (gold)** no treino. |

---

## Números de referência (teste)

| Protocolo | LogReg | SVM | BERT | Nota |
|-----------|-------:|----:|-----:|------|
| ComprasNet 423 | **0,740** | 0,652 | 0,400 | Entrega oficial |
| `pncp` | 0,756 | 0,783 | **0,858** | Honesto em escala |
| `pncp9` | 0,857 | 0,877 | 0,969 | Só keyword |
| `pncp9full` | 0,816 | 0,862 | 0,970 | + Indeterminado |
| `pncp9fb` | 0,824 | — | — | Fallback órgão |
| `pncp9fbi` | 0,788 | 0,829 | **0,955** | + info complementar |

Runs: `experiments/classification_pncp*` · [`MODEL-CARD.md`](MODEL-CARD.md)

---

## Dicas de ensaio

- **`pncp`** — falar “pê-ene-cê-pê”.
- **`fb`** — “efe bê” (fallback órgão).
- **`fbi`** — “efe bê i” (info).
- Na apresentação, apontar só **três linhas** da tabela: ComprasNet, **`pncp`**, **`pncp9fbi`**.
- Não ler a tabela inteira — usar mnemônico e árvore.

---

*Documento para ensaio oral — ajustar timing com cronômetro antes da apresentação.*
