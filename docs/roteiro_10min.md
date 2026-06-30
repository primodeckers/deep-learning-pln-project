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
| 4 | **Metodologia** — vazamento + protocolo | 3:00 → 4:15 |
| 4b | **Metodologia** — por que estes modelos (CNN? RNN? Transformer?) | 4:15 → 5:30 |
| 5 | **Resultados** — ComprasNet 423 | 5:30 → 7:00 |
| 6 | **Resultados** — PNCP + família `pncp*` | 7:00 → 8:15 |
| 7 | **Discussão** — limites e vieses | 8:15 → 9:15 |
| 8 | **Conclusão** + **Próximos passos** | 9:15 → 10:00 |

---

## RESUMO EXECUTIVO (6 frases)

1. Coletamos **dados públicos inéditos** DF/2025: **423 editais ComprasNet** (entrega oficial) e **19.944 compras PNCP** (extensão em escala).
2. **Tarefa:** classificar por **área de gasto** (6 macroáreas) a partir da descrição do objeto — triagem para transparência pública.
3. Comparamos **três modelos** no **mesmo protocolo**, cobrindo **aprendizado clássico** e **deep learning**: TF-IDF + LogReg, TF-IDF + SVM e **BERTimbau** (Transformer). **Não usamos CNN nem RNN/LSTM** — explicamos por quê no slide de arquitetura.
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
"Boa tarde. Somos o grupo da **Modalidade 2 — PLN no Setor Público**. O problema que escolhemos é concreto: todo edital ou compra pública tem um campo **Objeto** — um texto livre, em linguagem jurídico-administrativa, dizendo o que o governo quer comprar ou contratar. Pode ir de 'medicamentos antimetabólitos' a 'tubos de PVC' ou 'contratação por inexigibilidade'.

Para o **controle social** — cidadão, jornalista, órgão de controle — saber ***em que áreas* o Distrito Federal está comprando** — quantas licitações são de Saúde, quantas de Obras, quais descrições ainda precisam de leitura humana — exige classificar centenas de textos uma a uma. Isso é inviável na mão. Nosso projeto aplica PLN para **rotular automaticamente** cada registro por **área de gasto**. **Não estimamos valores em reais** nesta entrega; o campo *valor homologado* existe nos dados e aparece nos próximos passos como cruzamento com a área predita."

**Slide 2 — Base teórica** · [1:00 → 1:45]  
"Fundamentamos o trabalho em duas frentes, como a disciplina exige — **cinco referências de domínio** e **cinco de técnica**, usadas de forma substantiva, não só listadas no final.

Na frente **técnica**: o **BERT** de Devlin et al. para fine-tuning de Transformers em classificação textual; o **BERTimbau** de Souza et al., pré-treinado em português brasileiro — escolhemos modelo PT-BR em vez de multilíngue genérico; e o material da aula 03–04, cujo lema é **'depende'**: a arquitetura certa depende do problema, do volume de dados e do diagnóstico treino versus teste.

Na frente de **domínio**: o caso **Alice** de IA em auditoria de licitações na CGU e TCU; estudos de classificação de documentos públicos; transparência e governo aberto; e o marco legal — Lei de Licitações 14.133, Lei de Acesso à Informação e a nova Lei de Linguagem Simples."

**Slide 3 — Dados** · [1:45 → 3:00]  
"Os dados são **inéditos** — a disciplina proíbe bases prontas como Kaggle. Coletamos de **duas fontes**, ambas DF/2025.

**ComprasNet**, nossa **entrega oficial**: **423 editais** em HTML de detalhe. Decisão **ética**: o PDF completo tem CAPTCHA; em vez de burlar, coletamos o HTML aberto, com intervalo de 0,8 segundo entre requisições, User-Agent identificando o projeto acadêmico, e hash SHA-256 versionado no repositório.

**PNCP**, extensão em **escala**: **19.944 compras** via planilha/API oficial, sem CAPTCHA. Textos mais curtos — mediana de ~32 palavras no objeto — e perfil distinto, com muita inexigibilidade.

O **rótulo** é um *proxy*: mapeamos o **órgão comprador** para seis macroáreas — Saúde, Saneamento, Segurança, Educação, Infraestrutura/Obras e Administração/Outros. Validamos à mão **30 editais**, quatro fichas por integrante, com concordância média de **~83%**. Declaramos as limitações: corpus pequeno e desbalanceado no ComprasNet; ~**48%** dos objetos PNCP sem keyword setorial."

---

### Integrante 2 — Metodologia · ~2:30

**[Critérios: implementação técnica · avaliação do modelo · análise crítica · fundamentação científica]**

**Slide 4 — Vazamento de label + protocolo experimental** · [3:00 → 4:15]  
"Antes de falar dos modelos, a decisão metodológica mais importante do trabalho: o **vazamento de label**.

O rótulo vem do **órgão** — por exemplo, 'Secretaria de Saúde' vira classe Saúde. Se dermos ao modelo o **texto completo** do edital, ele acerta demais — F1 de **~0,88** no teste. Mas isso é **inflado**: em **97%** dos casos o HTML completo repete o nome do órgão ou a keyword da área. O modelo não aprende *o que está sendo comprado*; ele **cola** no rótulo.

Por isso a entrada oficial é **só o campo Objeto** — `objeto_html` no ComprasNet, `objeto_html_limpo` no PNCP. O vazamento cai para **~49–51%**. Preferimos o **0,74 honesto** ao 0,88 contaminado.

O **protocolo é idêntico** pros três modelos: split **70% treino, 15% validação, 15% teste**, estratificado por área, **seed 42** — 295, 64 e 64 editais no ComprasNet. Métrica primária: **F1 macro no teste**, porque as classes estão desbalanceadas e a acurácia sozinha engana. Olhamos a validação durante o desenvolvimento, mas **reportamos sempre o teste**. Cada run vai para JSON e MLflow, com hash do corpus e commit Git."

**Slide 4b — Por que estes três modelos? (família de arquitetura)** · [4:15 → 5:30]  
"A disciplina pede comparar abordagens de PLN e deep learning. Escolhemos **três modelos** que cobrem **duas famílias** distintas — e **deliberadamente não usamos CNN nem RNN/LSTM**. Explico.

**Primeira família — aprendizado clássico em texto, sem rede neural profunda:**

**Fase 1 — TF-IDF + Regressão Logística** — nosso **modelo oficial**. O TF-IDF transforma o texto em vetor esparso de n-gramas — sacola de palavras com peso. A LogReg é um **classificador linear**: aprende pesos por termo e decide a área por combinação linear. **Não é CNN, não é RNN** — é machine learning clássico, interpretável e forte com **poucos dados**. A aula recomenda **sempre começar por um baseline** antes de deep learning; com ~295 editais de treino, isso faz sentido.

**Fase 3 — TF-IDF + SVM linear** — **mesmo vetorizador**, classificador diferente. O SVM busca a **margem máxima** entre classes; comparamos se a fronteira de decisão do SVM supera a LogReg. Continua na família **linear sobre TF-IDF** — ainda não é rede neural.

**Segunda família — deep learning / Transformer:**

**Fase 2 — BERTimbau** — aqui entra **deep learning de verdade**. BERT é um **Transformer encoder-only**: usa **atenção multi-cabeça** para ler o texto **bidirecionalmente**, capturando contexto entre palavras distantes. Fine-tuning em cima do checkpoint `neuralmind/bert-base-portuguese-cased` — milhões de parâmetros pré-treinados em português.

**Por que BERT e não RNN ou LSTM?** Texto é sequencial — RNNs e LSTMs foram a arquitetura clássica para sequências. Mas o estado da arte em PLN hoje é **Transformer**: BERT supera LSTM na maioria das tarefas de classificação textual, e a disciplina enfatiza Transformers. Não implementamos BiLSTM porque seria **redundante** com o experimento BERT — queríamos testar a hipótese moderna.

**Por que não CNN?** Na aula, CNN é arquitetura para **dados em grade** — imagens, mapas. Para texto, convolução 1D até existe, mas **não é o padrão** do mercado nem o foco do curso para classificação de documentos. Nosso problema é **texto livre**, não imagem nem série temporal tabular — por isso **CNN ficou fora do escopo**.

**Por que três e não mais?** Queríamos **comparação justa**: Fases 1 e 3 compartilham **exatamente** o mesmo TF-IDF; Fase 2 compartilha **mesmo split e mesma entrada**. Assim isolamos o efeito da **arquitetura** — linear clássica versus Transformer — sem mudar os dados.

**Hipótese inicial:** Transformer vence baseline. **Resultado ComprasNet:** **não confirmado** — pouco treino. **Resultado PNCP (~20 mil):** **confirmado** — escala muda o vencedor. Isso amarra direto ao lema **'depende'** da aula."

#### Tabela para o slide 4b (família de arquitetura)

| Modelo | Fase | Família | É rede neural? | Por que incluímos |
|--------|------|---------|----------------|-------------------|
| TF-IDF + **LogReg** | 1 | ML clássico (linear) | Não | Baseline obrigatório; interpretável; robusto com poucos dados |
| TF-IDF + **SVM linear** | 3 | ML clássico (margem max.) | Não | Mesmos features; testa se margem bate regressão logística |
| **BERTimbau** | 2 | **Transformer** (encoder) | Sim (DL) | Estado da arte em PLN; pré-treino PT-BR; exigência DL do curso |
| CNN | — | Visão / grades | Sim | **Não usamos** — texto livre, não imagem |
| RNN / LSTM | — | Sequência recorrente | Sim | **Não usamos** — substituído por Transformer no experimento |

---

### Integrante 3 — Resultados · ~3:00

**[Critérios: avaliação do modelo · impacto aplicado · análise crítica]**

**Slide 5 — ComprasNet 423 (entrega oficial)** · [5:30 → 7:00]  
"Os resultados no corpus oficial de **423 editais**, teste com **64 editais nunca vistos**:

**LogReg: F1 macro 0,74** — escolhido como modelo principal. Validação 0,743, teste 0,740 — **estável**, sem surpresa desagradável.

**SVM: F1 0,65** — pior no teste, embora tenha ido **melhor na validação** (0,80). Interpretamos como **overfitting**: o SVM se ajustou demais aos 64 editais de val e **não generalizou**. Mesmo TF-IDF, fronteira de decisão mais rígida — mas com pouco dado, a estabilidade da LogReg pesou mais.

**BERTimbau: F1 0,40** — **hipótese Transformer vence baseline: refutada** neste volume. Com ~295 treinos e dezenas de milhões de parâmetros, o BERT **colapsa nas classes raras**: Segurança, Educação e Infraestrutura com **F1 zero** no teste — empurra tudo para Administração/Outros. Onde há muitos exemplos — Saúde, Saneamento — o BERT até compete; onde há poucos, falha.

**Leitura por família:** o **clássico linear** venceu o **Transformer** aqui porque **dados >> parâmetros** não se invertem — faltam dados. Impacto aplicado: triagem automática por macroárea no corpus que entregamos como resultado principal."

**Slide 6 — PNCP + família de protocolos** · [7:00 → 8:15]  
"A pergunta natural: e com **muito mais dado**? Entra o PNCP — **19.944 compras**, protocolo **`pncp`**: mesmas **seis macroáreas**, label por órgão, mesma honestidade metodológica.

**BERT F1 0,86** versus **LogReg 0,76** — o veredito **se inverte**. Mesma família de modelos, **volume diferente**. O Transformer deixa de colapsar; o baseline clássico continua forte, mas não basta.

Exploramos ainda protocolos **`pncp9*`** — nove setores empíricos, fallback órgão, info complementar. F1 até **~0,97** no BERT — mas **declaramos**: muitas vezes o label **reproduz regras de keyword** no texto; não confundir com generalização em produção.

**Três números para a banca:** entrega **0,74** (ComprasNet, LogReg) · escala honesta **0,86** (`pncp`, BERT) · exploratório **0,95+** (`pncp9fbi`, com ressalvas). Detalhe dos IDs no doc [`ROTEIRO-FAMILIA-PROTOCOLOS-PNCP.md`](ROTEIRO-FAMILIA-PROTOCOLOS-PNCP.md)."

---

### Integrante 4 — Discussão + Conclusão · ~2:00

**[Critérios: análise crítica · impacto aplicado · comunicação · reprodutibilidade]**

**Slide 7 — Discussão** · [8:15 → 9:15]  
"Limites e vieses — **declarados**, não escondidos.

**Label proxy** com ~83% de concordância humana: quando o órgão diz 'Bombeiros' mas o objeto é material clínico, o rótulo vira Segurança e o modelo confunde com Saúde — erro **estrutural**, não só do algoritmo.

**Vazamento residual** de ~49–51%: keyword da área ainda aparece no objeto; F1 honesto, mas não é 'puro'.

**Classes raras** no ComprasNet — Educação com **2 exemplos no teste** — F1 instável estatisticamente.

**PNCP ≠ ComprasNet** — textos curtos, inexigibilidade dominante, perfil burocrático.

**Escolha de arquitetura:** CNN e LSTM ficaram **fora** por adequação ao problema; comparar LogReg, SVM e BERT cobre **clássico versus Transformer**, que é o eixo pedagógico da disciplina.

O classificador **não substitui** análise jurídica. Documentamos runs **negativos** — BERT 0,40 — porque erro faz parte do aprendizado científico."

**Slide 8 — Conclusão + Próximos passos** · [9:15 → 10:00]  
"Três contribuições. **Uma:** pipeline **inédito, ético e reprodutível** — ComprasNet mais PNCP, scripts no GitHub, hash versionado. **Duas:** evidência empírica de que **volume e protocolo mudam o melhor modelo** — clássico linear vence com 423 editais; Transformer vence com ~20 mil — o **'depende'** da aula na prática. **Três:** ferramenta de **triagem por área de gasto** para transparência pública.

Próximos passos: expandir corpus no tempo, revisar mapeamento órgão→área, cruzar área predita com **valor homologado**, avaliar BERT nas ~853 compras **escondidas**.

Repositório público, dados via código, slides em PDF — conforme entregáveis. **Obrigado!**"

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

**Nunca cortar:** slide 4 (vazamento), **slide 4b (por que estes modelos / CNN vs RNN vs Transformer)**, slide 5 (ComprasNet 0,74 vs 0,40).

**Cortar primeiro se estourar 10 min:**
- Slide 2 (teoria → citar 2 artigos + “5+5 no relatório”).
- Slide 6 (detalhe `pncp9*` → uma frase + doc auxiliar).
- Slide 7 (lista de limites → top 3).

**Nota:** com slide 4b expandido, o ensaio pode ir a **~10:30**. Ensaiar com cronômetro; Integrante 2 é o gargalo — falar slide 4b **sem pressa**, é o que a banca espera em **implementação técnica**.

**Se sobrar tempo:** ~853 **escondidas** — LogReg F1 **~0,65**; BERT ainda não avaliado nessa coorte.

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
