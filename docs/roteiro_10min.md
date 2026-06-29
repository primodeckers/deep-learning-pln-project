# Apresentação de 10 minutos — roteiro alinhado aos critérios da disciplina

**Trabalho:** Classificação automática de editais/compras por área de gasto público (ComprasNet + PNCP, DF/2025)  
**Modalidade:** 2 — PLN no Setor Público · Grupo de 4  
**Integrantes:** Elisangela Osorio · Alexandre Ferreira Ponte · Renê Estevam Deckers · Alexandre Hugo Sampaio Netto  

> **Base normativa:** [`PROJECT-REQUIREMENTS.md`](PROJECT-REQUIREMENTS.md) — §Apresentação Final, §Estrutura sugerida para os slides, §Critérios de Avaliação  
> **Detalhe PNCP:** [`ROTEIRO-FAMILIA-PROTOCOLOS-PNCP.md`](ROTEIRO-FAMILIA-PROTOCOLOS-PNCP.md) · **Conteúdo ampliado:** [`APRESENTACAO-CONTEUDO.md`](APRESENTACAO-CONTEUDO.md)

---

## Mapa: slides × critérios de avaliação

Cada slide cobre um ou mais critérios obrigatórios da disciplina:

| Critério (disciplina) | Onde aparece no roteiro |
|------------------------|-------------------------|
| **Clareza do problema** | Slides 1 |
| **Fundamentação científica** | Slide 2 (5+5 refs citadas) |
| **Qualidade dos dados** | Slide 3 (coleta, limitações, validação) |
| **Implementação técnica** | Slides 4–5 (pipeline, 3 modelos, protocolos) |
| **Avaliação do modelo** | Slides 6–7 (F1 teste, métrica, split) |
| **Análise crítica** | Slides 4, 7 (vazamento, proxy, protocolos) |
| **Reprodutibilidade** | Slide 3 ou 9 (GitHub, scripts, hash, seed) |
| **Comunicação** | Todo o roteiro (10 min, 4 falantes) |
| **Impacto aplicado** | Slides 1, 7, 8 (transparência, triagem de gasto) |

---

## Estrutura dos slides (8 + capa + encerramento)

Conforme [`PROJECT-REQUIREMENTS.md`](PROJECT-REQUIREMENTS.md) §“Estrutura sugerida para os slides”:

| # | Seção exigida | Tempo acum. |
|---|---------------|------------:|
| capa | Título + integrantes | 0:00 |
| 1 | **Contexto** — problema real | 0:00 → 1:00 |
| 2 | **Base teórica** — artigos | 1:00 → 1:45 |
| 3 | **Dados** — coleta e limitações | 1:45 → 3:00 |
| 4 | **Metodologia** — modelos + vazamento | 3:00 → 5:00 |
| 5 | **Resultados** — ComprasNet 423 | 5:00 → 6:30 |
| 6 | **Resultados** — PNCP + família `pncp*` | 6:30 → 8:00 |
| 7 | **Discussão** — limites e vieses | 8:00 → 9:00 |
| 8 | **Conclusão** + **Próximos passos** | 9:00 → 10:00 |

---

## RESUMO EXECUTIVO (6 frases)

1. Coletamos **dados públicos inéditos** DF/2025: **423 editais ComprasNet** (entrega oficial) e **19.944 compras PNCP** (extensão em escala).
2. **Tarefa:** classificar por **área de gasto** (6 macroáreas) a partir da descrição do objeto — triagem para transparência pública.
3. Comparamos **TF-IDF + LogReg**, **TF-IDF + SVM** e **BERTimbau** no **mesmo protocolo** (split 70/15/15, seed 42).
4. **Achado central:** com **423 editais**, LogReg **F1 0,74** vence BERT **0,40**; com **~20 mil** (protocolo `pncp`), BERT **0,86** vence LogReg **0,76** — o lema **“depende”** na prática.
5. **Rigor metodológico:** controlamos **vazamento de label** (`objeto` vs texto completo), reportamos **teste** (não validação), validamos rótulo proxy (~**83%** concordância humana).
6. **Contribuição:** explicar **o que a métrica significa**, não só exibir o número mais alto.

> **Frase de efeito:** *"A contribuição não é a melhor métrica — é entender o que ela significa, e por que o vencedor muda quando o volume e o protocolo mudam."*

---

## ROTEIRO FALADO — 4 integrantes · ~10:00

Marcos **[mm:ss]** · ~140 palavras/min

---

### Integrante 1 — Contexto + Teoria + Dados · ~3:00

**[Critérios: clareza do problema · fundamentação · qualidade dos dados · reprodutibilidade]**

**Slide 1 — Contexto** · [0:00 → 1:00]  
"Boa tarde. **Modalidade 2 — PLN no Setor Público**. Todo edital tem um campo **Objeto**: texto em juridiquês sobre o que o governo compra ou contrata.

Para **controle social** — cidadão, jornalista, órgão de controle — responder *'quanto o DF gastou em Saúde?'* exige ler centenas de descrições à mão. Nosso projeto **classifica automaticamente** por **área de gasto**, apoiando triagem e transparência."

**Slide 2 — Base teórica** · [1:00 → 1:45]  
"**Técnica:** BERT (Devlin), **BERTimbau** (Souza) para português, e o guia da disciplina — *depende* do volume e do diagnóstico treino × teste.  
**Domínio:** IA em licitações (Alice/CGU/TCU), classificação de documentos públicos, transparência (Macedo et al.), PLN no GDF (Ferreira/UnB). Marco legal: Lei 14.133, LAI e Linguagem Simples.  
Atendemos o requisito de **5+5 referências** usadas de forma substantiva no relatório."

**Slide 3 — Dados** · [1:45 → 3:00]  
"Dados **inéditos** — sem Kaggle. **ComprasNet:** 423 editais HTML, coleta ética (**sem** burlar CAPTCHA), delay 0,8 s, corpus versionado com hash. **PNCP:** 19.944 compras DF/2025, API/planilha oficial.  
**Rótulo proxy:** órgão → 6 macroáreas; validação humana em 30 editais → **~83%** de concordância.  
**Limitações declaradas:** corpus pequeno e desbalanceado (ComprasNet); objetos curtos e vagos no PNCP (~**48%** sem keyword setorial). Repositório público com scripts reprodutíveis."

---

### Integrante 2 — Metodologia · ~2:00

**[Critérios: implementação técnica · avaliação do modelo · análise crítica]**

**Slide 4 — Metodologia + vazamento** · [3:00 → 5:00]  
"**Vazamento de label** — decisão central: o rótulo vem do **órgão**. Se o modelo vê o **texto completo**, F1 ≈ **0,88** — inflado (~**97%** repetem pista do órgão). Usamos **só o objeto** → F1 honesto **~0,74** (ComprasNet). Preferimos métrica honesta.

**Protocolo único:** entrada `objeto_html` / `objeto_html_limpo`, split **70/15/15** estratificado, **seed 42**, **F1 macro no teste** como métrica primária. Escolhemos pela validação; **reportamos o teste**.

**Três modelos:** TF-IDF + **LogReg** (oficial), TF-IDF + **SVM**, **BERTimbau** fine-tuned (GPU). Runs em JSON + MLflow."

---

### Integrante 3 — Resultados · ~3:00

**[Critérios: avaliação do modelo · impacto aplicado · análise crítica]**

**Slide 5 — ComprasNet 423 (entrega oficial)** · [5:00 → 6:30]  
"No **teste** (64 editais nunca vistos): **LogReg F1 0,74** · SVM **0,65** · BERT **0,40**.  
Hipótese 'BERT vence' **não se confirmou** com ~295 treinos — Transformer colapsa em classes raras (Segurança, Educação, Infra com F1 **0**). LogReg estável val ≈ teste.  
**Impacto:** triagem automática por macroárea no corpus que a disciplina exige como entrega principal."

**Slide 6 — PNCP + família de protocolos** · [6:30 → 8:00]  
"**Mesma pergunta, mais dados:** protocolo **`pncp`** (6 áreas, label por órgão, ~20k) — **BERT F1 0,86** vs LogReg **0,76**. Volume **inverte** o veredito.

Exploramos protocolos **`pncp9*`** (9 setores, fallback órgão, info complementar). F1 até **~0,97** — mas declaramos: muitas vezes o label **reproduz regras de keyword**, não generalização cega.  
**Três números para a banca:** entrega **0,74** (ComprasNet) · escala honesta **0,86** (`pncp`) · exploratório **0,95+** (`pncp9fbi`, com ressalvas).  
Detalhe dos IDs: slide auxiliar ou [`ROTEIRO-FAMILIA-PROTOCOLOS-PNCP.md`](ROTEIRO-FAMILIA-PROTOCOLOS-PNCP.md)."

---

### Integrante 4 — Discussão + Conclusão · ~2:00

**[Critérios: análise crítica · impacto aplicado · comunicação · reprodutibilidade]**

**Slide 7 — Discussão** · [8:00 → 9:00]  
"**Limites e vieses — declarados, não escondidos:**  
- **Label proxy** (~83% concordância) — Bombeiros + objeto clínico → confusão Segurança/Saúde.  
- **Vazamento residual** ~49–50% (keyword da área ainda no objeto).  
- **Classes raras** no ComprasNet (Educação n=2 no teste).  
- **PNCP ≠ ComprasNet** — textos curtos, inexigibilidade dominante.  
- Classificador **não substitui** análise jurídica.  
Erros e limitações fazem parte do aprendizado — comparamos modelos e documentamos runs negativos (BERT 0,40)."

**Slide 8 — Conclusão + Próximos passos** · [9:00 → 10:00]  
"**Contribuições:** (1) pipeline **inédito e reprodutível** de transparência pública; (2) evidência de que **volume e protocolo** mudam o melhor modelo; (3) ferramenta de **triagem por área de gasto**.  
**Próximos passos:** expandir corpus no tempo, revisar mapeamento órgão→área, cruzar área predita com **valor homologado**, avaliar BERT nas ~**853 compras escondidas**.  
Repositório, dados via código, slides em PDF — conforme entregáveis da disciplina. **Obrigado!**"

---

## NÚMEROS-CHAVE (cola rápida)

| Item | Valor |
|------|------:|
| Editais ComprasNet | 423 |
| Compras PNCP | 19.944 |
| Concordância humana (labels) | ~83% |
| Split ComprasNet | 295 / 64 / 64 |
| **ComprasNet — LogReg F1 teste** | **0,740** |
| ComprasNet — SVM | 0,652 |
| ComprasNet — BERT | 0,400 |
| **PNCP `pncp` — BERT F1 teste** | **0,858** |
| PNCP `pncp` — LogReg | 0,756 |
| PNCP — sem keyword no objeto | ~48% |
| Vazamento c/ texto completo | ~97% |
| Vazamento c/ só objeto | ~49–51% |

---

## REGRAS DE TEMPO

**Nunca cortar:** slide 4 (vazamento), slide 5 (ComprasNet 0,74 vs 0,40), slide 6 (PNCP inverte veredito).

**Cortar primeiro se estourar:** slide 2 (teoria → 1 frase + logos dos artigos); detalhe da família `pncp9*` (remeter ao doc auxiliar).

**Se sobrar tempo:** ~853 **escondidas** (objeto vago, órgão setorial) — LogReg F1 **~0,65** no benchmark; BERT ainda não avaliado nessa coorte.

---

## CHECKLIST PRÉ-APRESENTAÇÃO (entregáveis + critérios)

- [ ] Repositório GitHub público com scripts e README de execução
- [ ] Dados acessíveis via código (ou acordado com professor)
- [ ] PDF dos slides entregue
- [ ] 5 refs domínio + 5 refs técnica citadas nos slides ou relatório
- [ ] F1 **teste** (não só validação) visível no slide de resultados
- [ ] Limitações e vazamento mencionados oralmente
- [ ] Cronômetro: ensaio completo ≤ 10 min
- [ ] Impacto aplicado (transparência / triagem de gasto) explícito no fechamento

---

*Roteiro alinhado a [`PROJECT-REQUIREMENTS.md`](PROJECT-REQUIREMENTS.md). Atualizar se runs ou protocolos mudarem.*
