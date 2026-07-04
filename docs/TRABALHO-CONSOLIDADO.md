# Classificação de editais por área de gasto — Distrito Federal, 2025

**Projeto Final — Deep Learning e PLN · Modalidade 2: PLN no Setor Público**

**Integrantes:** Elisangela Osorio · Alexandre Ferreira Ponte · Renê Estevam Deckers · Alexandre Hugo Sampaio Netto

**Documentação complementar:** `[README.md](README.md)` · `[PROJECT-REQUIREMENTS.md](PROJECT-REQUIREMENTS.md)` · `[REGRAS-E-PROTOCOLOS.md](REGRAS-E-PROTOCOLOS.md)` · `[METRICAS-E-DECISOES.md](METRICAS-E-DECISOES.md)` · `[MODEL-CARD.md](MODEL-CARD.md)` · `[APRESENTACAO-CONTEUDO.md](APRESENTACAO-CONTEUDO.md)` · `[roteiro_10min.md](roteiro_10min.md)`

Este documento segue a **Estrutura Recomendada do Trabalho** e atende aos **Critérios de Avaliação** definidos em `[PROJECT-REQUIREMENTS.md](PROJECT-REQUIREMENTS.md)`:


| Critério                 | Onde está no documento                     |
| ------------------------ | ------------------------------------------ |
| Clareza do problema      | §1 Contexto e problema                     |
| Fundamentação científica | §3 Referencial teórico · §9 Referências    |
| Qualidade dos dados      | §4 Dados                                   |
| Implementação técnica    | §5 Metodologia (§5.3)                      |
| Avaliação do modelo      | §5.2 · §6 Resultados                       |
| Análise crítica          | §7 Discussão                               |
| Reprodutibilidade        | §5.5 · §10 Apêndice técnico                |
| Comunicação              | §10 Apêndice (slides e roteiro oral)       |
| Impacto aplicado         | §2 Justificativa · §6.5 Insights aplicados |


---

## 1. Contexto e problema

Editais de licitação pública descrevem, em linguagem jurídica e técnica, o que o governo pretende comprar ou contratar. No Distrito Federal, centenas desses documentos são publicados todo ano no portal ComprasNet — e dezenas de milhares de compras aparecem no Portal Nacional de Contratações Públicas (PNCP). Para um cidadão, um pequeno empresário ou um órgão de controle, saber ***em que áreas* o governo está comprando** — quantas licitações são de Saúde, quantas de Obras, quais descrições ainda precisam de leitura humana — exige classificar centenas de textos manualmente. Isso é inviável na mão.

**Para o pequeno fornecedor**, a pergunta é outra: *“O que preciso ter para participar?”* O edital responde em jargão (“sistema de registro de preços”, “qualificação técnica”). Quem tem padaria, oficina ou MEI muitas vezes **não entende e desiste**. A política pública quer **mais concorrência** e inclusão de micro e pequenas empresas; a **linguagem** do edital afasta exatamente esse público (Rosado & Dias, 2024).

**Problema investigado:** dado o campo **Objeto** de um edital ou compra pública, **classificar automaticamente a macroárea ou setor de gasto** (Saúde, Saneamento, Segurança, Educação, Infraestrutura/Obras, Administração/Outros) para apoiar triagem e transparência pública. (Linguagem mais clara / resumo cidadão fica como próximo passo — esta entrega é **classificação**.)

**Delimitação:** o projeto **não estima valores em reais** nesta entrega; concentra-se em **rotulagem temática** a partir de texto. O campo *valor homologado* existe nos dados e aparece como cruzamento futuro (§8).

**Restrição da disciplina:** dados **inéditos**, coletados pelo grupo — sem bases prontas (Kaggle ou equivalentes).

---

## 2. Justificativa

**Relevância aplicada:** licitações são instrumento central de execução orçamentária; automatizar sua leitura apoia fiscalização, jornalismo de dados e participação de micro e pequenas empresas — alinhado ao uso de IA em auditoria de contratos públicos (Souto et al., 2025) e à demanda por linguagem acessível em documentos jurídicos (Rosado & Dias, 2024).

**Relevância técnica:** o corpus ComprasNet (423 editais) permite comparar TF-IDF + LogReg, SVM e BERTimbau no **mesmo protocolo** — respondendo se, com poucos dados, deep learning supera métodos clássicos. A extensão PNCP (~20 mil compras) testa se **escala** e **taxonomias alternativas** (9 setores empíricos) invertem esse veredito.

**Hipótese inicial:** BERTimbau supera TF-IDF + LogReg. Nos 423 editais **não se confirmou**; no PNCP em escala grande, **sim** — achado metodológico central, coerente com o lema **“depende”** do material da disciplina (volume, diagnóstico treino × teste e protocolo).

---

## 3. Referencial teórico

As referências (§9) são usadas **de forma substantiva** — não apenas listadas — para sustentar problema, metodologia, interpretação e limitações.

### 3.1 Domínio — licitações, transparência e setor público

- **Marco legal:** Lei nº 14.133/2021 (Nova Lei de Licitações), Lei nº 12.527/2011 (LAI) e Lei nº 15.263/2025 (Linguagem Simples) fundamentam o contexto de contratações públicas e acessibilidade da informação.
- **Souto et al. (2025)** — caso **Alice** (CGU/TCU): IA aplicada a auditoria de licitações; valida o problema de classificação temática em contratos públicos.
- **Ferreira (2019)** — classificação de textos em sistemas modulares no GDF; precedente local de PLN em administração pública.
- **Watanabe & Sousa (2023)** — classificação automática de documentos em organização pública; apoia a escolha de baseline clássico antes de redes profundas.
- **Macedo et al. (2025)** — transparência e governo aberto; conecta o projeto a controle social e fiscalização.
- **Rosado & Dias (2024)** — jargão jurídico como barreira; justifica foco no campo Objeto e triagem para cidadãos e MPEs.

### 3.2 Técnica — PLN, classificação e deep learning

- **Devlin et al. (2019)** — arquitetura **BERT** e fine-tuning de Transformers; base teórica da Fase 2.
- **Souza et al. (2020)** — **BERTimbau**, pré-treino em português brasileiro; escolha de checkpoint PT-BR (`neuralmind/bert-base-portuguese-cased`) em vez de modelo multilíngue genérico.
- **Pedregosa et al. (2011)** — **scikit-learn**: TF-IDF, LogReg e SVM linear nas Fases 1 e 3.
- **Goodfellow et al. (2016)** — modelagem de sequências; contextualiza por que **RNN/LSTM** não foram implementados (substituídos pelo experimento Transformer).
- **Srivastava et al. (2014)** — dropout e regularização; relevante ao overfitting observado (SVM na validação vs teste; BERT com poucos dados).

### 3.3 Decisões metodológicas derivadas da literatura


| Decisão                                           | Fundamentação                                               |
| ------------------------------------------------- | ----------------------------------------------------------- |
| F1 **macro no teste** como métrica primária       | Classes desbalanceadas; acurácia sozinha engana             |
| Baseline **TF-IDF + LogReg** antes do Transformer | Watanabe & Sousa (2023); boas práticas da disciplina        |
| Entrada `**objeto_html**`, não HTML completo      | Controle de **vazamento de label** (§5.1)                   |
| Comparar **clássico linear vs Transformer**       | Devlin; Souza; exigência de DL + comparação justa           |
| **Não usar CNN nem RNN/LSTM**                     | Problema = texto livre; Transformer cobre DL moderno (§5.3) |


---

## 4. Dados

### 4.1 ComprasNet — corpus principal (entrega oficial)


| Aspecto                                         | Valor                                                                                                                                                                                                               |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Fonte                                           | [ComprasNet](http://www.comprasnet.gov.br/) — CSV DF 2025 (437 linhas → **423 URLs** únicas)                                                                                                                        |
| Período / filtro                                | Distrito Federal · **2025**                                                                                                                                                                                         |
| Coleta                                          | HTML de detalhe (**sem** burlar CAPTCHA; PDF exige CAPTCHA — rejeitado por ética)                                                                                                                                   |
| Corpus                                          | `licitacoes_corpus.jsonl` — **423 registros**                                                                                                                                                                       |
| Material / Serviço                              | 320 / 103                                                                                                                                                                                                           |
| **Entrada oficial**                             | `objeto_html` — só a descrição do objeto                                                                                                                                                                            |
| Tamanho `**objeto_html**` (palavras)            | mediana **~33** · média **~31** · máx. **80** · **0%** acima de 512 palavras                                                                                                                                        |
| Tamanho `**objeto_html**` (caracteres)          | mediana **~225** · média **~216** · máx. **~518**                                                                                                                                                                   |
| Tamanho `**texto**` (HTML completo, referência) | mediana **~239 palavras** / **~1.600 caracteres** · média **~461 palavras** / **~3.400 caracteres** · máx. **~5.524 palavras** / **~41.300 caracteres** · **27%** dos editais com > 512 palavras (truncamento BERT) |
| Modalidade                                      | Pregão (278) · Dispensa (134)                                                                                                                                                                                       |


**Transparência da coleta:** delay **0,8 s** entre requisições; User-Agent identificando projeto acadêmico; hash SHA-256 versionado. Pipeline: `scripts/run_collect.py` → `scripts/run_preprocess.py`.

### 4.2 PNCP — extensão exploratória


| Aspecto                     | Valor                                                                                                                                                                                           |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Fonte                       | PNCP / Compras.gov.br — planilha/API oficial                                                                                                                                                    |
| Filtro                      | UF = **DF**, ano = **2025**                                                                                                                                                                     |
| Corpus                      | `pncp_corpus_df2025.jsonl` — **19.944 compras**                                                                                                                                                 |
| Campo principal             | `objeto_compra` — mediana **~32 palavras** (máx. 349; 0% > 512) vs `**objeto_html`** ComprasNet mediana **~33 palavras**; HTML completo (`texto`) mediana **~239 palavras**                     |
| Modalidade dominante        | Inexigibilidade (~39%) — perfil distinto do ComprasNet                                                                                                                                          |
| **Informação complementar** | Campo extra do PNCP em **~53%** das linhas — texto adicional de justificativa ou detalhe (ex.: fundamento legal, escopo técnico). **Não existe** como coluna separada no corpus ComprasNet HTML |


Pipeline: `scripts/run_preprocess_pncp.py` · EDA: `notebooks/01_eda.ipynb` · `notebooks/03_eda_pncp.ipynb`.

### 4.3 Rotulagem (labels)

**ComprasNet e protocolo `pncp`:** rótulo **proxy** por **órgão → 6 macroáreas**. Regra em `src/preprocess/labels.py`: palavras-chave no **nome do órgão** (`orgao_csv` / `orgao_entidade_razao_social`); primeira match vence.

| # | Macroárea (6) | Exemplos de keyword no **órgão** |
|:-:|---------------|----------------------------------|
| 1 | Saúde | SAUDE, HOSPITAL, SES |
| 2 | Saneamento | CAESB, SANEAMENT, AGUA |
| 3 | Segurança | POLICI, BOMBEIRO, SEGURANC |
| 4 | Educação | EDUCAC, ESCOLA |
| 5 | Infraestrutura/Obras | OBRA, INFRAESTRUTUR, RODOVI |
| 6 | Administração/Outros | *fallback* — órgão sem keyword das cinco acima |

#### Protocolos `pncp9*` — **9 setores empíricos** (keyword no **objeto**)

Taxonomia **alternativa** às 6 macroáreas: o rótulo vem de palavras-chave no **texto da compra**, não no órgão (`src/preprocess/labels_setores.py`). Ordem importa — **primeira** keyword que casar define o setor.

| # | Setor (9) | Exemplos de keyword no **objeto** |
|:-:|-----------|-----------------------------------|
| 1 | Saúde | SAUDE, HOSPITAL, MEDIC, FARMAC, ODONTO |
| 2 | Educação | EDUCAC, ESCOLA, UNIVERSID, ENSINO |
| 3 | Segurança | POLICI, BOMBEIRO, SEGURANC, PENITENCI |
| 4 | Saneamento | SANEAMENT, ESGOTO, CAESB, DRENAG |
| 5 | Infraestrutura/Obras | OBRA, PAVIMENT, RODOVI, CONSTRUC |
| 6 | TI/Administração | SOFTWARE, INFORMAT, SISTEMA, MOBILIARIO |
| 7 | Transporte | VEICUL, COMBUSTIV, TRANSPORT, ONIBUS |
| 8 | Cultura | CULTUR, MUSEU, EVENTO, ARTISTIC |
| 9 | Meio Ambiente | AMBIENT, FLOREST, RESIDUO, RECICL |

Nos protocolos `pncp9full`, `pncp9fb` e `pncp9fbi`, compras **sem** keyword viram **Indeterminado** (10ª classe) ou usam **fallback** pela macroárea do órgão (`pncp9fb` / `pncp9fbi`). Variantes: `pncp9` (só com keyword, ~10,3 mil), `pncp9full`, `pncp9fb`, `pncp9fbi`. Regras: [`REGRAS-E-PROTOCOLOS.md`](REGRAS-E-PROTOCOLOS.md).

**Diferença em uma frase:** as **6 macroáreas** respondem *“quem comprou?”* (órgão); os **9 setores** respondem *“o texto fala de qual domínio?”* (objeto). Cinco nomes se repetem (Saúde, Educação…); TI, Transporte, Cultura e Meio Ambiente **só** existem na taxonomia de 9 setores.

#### O classificador **não recebe o órgão como feature** — o que isso significa?

Há **duas coisas separadas** no pipeline:


| Papel                                                  | Campo                                                       | Exemplo                                                    |
| ------------------------------------------------------ | ----------------------------------------------------------- | ---------------------------------------------------------- |
| **Resposta esperada** (só para treinar e medir acerto) | Derivada do **órgão**                                       | “Secretaria de Estado de **Saúde** do DF” → área **Saúde** |
| **Texto que o modelo lê**                              | Só o **objeto** da compra (`objeto_html` / `objeto_compra`) | “Aquisição de seringas descartáveis…”                      |


O nome do órgão **não entra** como coluna, campo extra ou concatenação explícita no vetor de features. O TF-IDF, o SVM e o BERT recebem **apenas a descrição da compra** — não `"Órgão: Secretaria de Saúde | Objeto: …"`.

**Por quê?** Se passássemos o órgão como input, a tarefa vira quase trivial: o modelo aprende *“vi SAÚDE no órgão → predigo Saúde”* em vez de inferir a área **pelo que está sendo comprado**. Isso infla a métrica (F1 ≈ **0,88** com HTML completo) sem testar PLN de verdade.

**O que ainda pode vazar:** mesmo sem passar o órgão como feature, o **texto do objeto** às vezes **repete** o nome da secretaria ou uma keyword da área (“insumo à saúde”, “CAESB”…). Isso é **vazamento lexical residual** (~49% no ComprasNet) — diferente de dar o órgão de bandeja ao modelo. Por isso usamos `objeto_html` (não `texto` completo) e documentamos o vazamento (§5.1).

**Resumo para a banca:** no protocolo honesto (`pncp` / ComprasNet), o **label vem do órgão** (proxy validado ~83%) e o **modelo só vê o objeto**. Nos `pncp9*`, o label vem de **keyword no objeto** (9 setores acima) — por isso F1 alto exige ressalva (§6.4).

**Validação humana (ComprasNet):** 30 editais, 4 fichas por integrante → concordância média **≈83,2%** (`[VALIDACAO-LABELS/VALIDACAO-LABELS.md](VALIDACAO-LABELS/VALIDACAO-LABELS.md)`).

### 4.4 Limitações dos dados

- ComprasNet: corpus **pequeno** (~295 treino); Educação com **2 exemplos no teste**; HTML ≠ PDF integral.
- PNCP: textos **curtos e burocráticos** (~48% sem keyword setorial); rótulos derivados de regras, não anotação manual completa.
- Ambos: escopo **DF/2025**; vazamento lexical residual (~49% em `objeto_html` ComprasNet).

---

## 5. Metodologia

### 5.1 Análise exploratória e vazamento de label

No ComprasNet, o HTML completo (`texto`) repete o órgão em **≈97%** dos casos onde a keyword da área aparece → F1 inflado **≈0,88**. O campo `**objeto_html`** reduz vazamento para **≈49%** → F1 honesto **≈0,74**. Preferimos métrica honesta a número contaminado.

#### Dois conceitos distintos — não confundir


|                      | **Label proxy** (rótulo aproximado)                                         | **Vazamento de label**                                           |
| -------------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **O que é**          | Como **definimos a área “certa”** de cada edital **sem ler tudo à mão**     | Quando o **texto que o modelo lê** já **entrega a resposta**     |
| **No nosso projeto** | Olhamos o **órgão**: “Secretaria de Saúde” → área **Saúde** (validado ~83%) | O objeto ou o HTML repete “Saúde”, “CAESB”, nome da secretaria…  |
| **É problema?**      | **Não** — é o melhor rótulo que temos sem anotação manual                   | **Sim** — o modelo **cola** na pista em vez de entender a compra |
| **O que fazemos**    | Documentamos e validamos com humanos                                        | Usamos só `objeto_html`; medimos quanto ainda vaza (~49%)        |


**Exemplo:** edital do **Bombeiros** comprando **material clínico**. O **proxy** classifica como **Segurança** (porque o comprador é Bombeiros) — pode estar errado, mas é a resposta que usamos no treino. **Vazamento** seria outra coisa: o modelo ler *“Corpo de Bombeiros…”* no texto e acertar **sem olhar o que está sendo comprado** — nota alta, aprendizado falso.

**Resumo:** ter proxy **não é** vazamento. Vazamento é quando a **mesma pista** que define a área **aparece de novo** no texto que o modelo enxerga. Detalhes: `[VAZAMENTO-DE-LABEL.md](VAZAMENTO-DE-LABEL.md)`.

`**limpar_objeto()**` tira do texto do objeto os trechos repetitivos de formulário (como “Objeto:”, “Pregão Eletrônico -”) e o nome do órgão quando ele aparece copiado ali, deixando só a descrição do que está sendo comprado para o modelo não “colar” na área pelo nome da secretaria — gera o campo `**objeto_html_limpo**`, usado nos protocolos PNCP (`src/preprocess/clean_objeto.py`).

### 5.2 Protocolo experimental — ComprasNet 423


| Decisão          | Valor                                                 |
| ---------------- | ----------------------------------------------------- |
| Entrada oficial  | `objeto_html`                                         |
| Partição         | 70% / 15% / 15%, estratificada, **seed 42**           |
| Tamanhos         | 295 treino · 64 val · 64 teste                        |
| Métrica primária | **F1 macro no teste**                                 |
| Seleção          | Desenvolvimento olha val; **relatório reporta teste** |


#### O que é **F1 macro** (versão simples)

**F1** de uma área = média harmônica de **precisão** (predi Saúde → era Saúde?) e **recall** (era Saúde → eu peguei?). Equilibra “quando acusa uma área, acerta?” e “quando a área é aquela, eu encontro?”.

**F1 macro** = nota **média** do F1 nas **6 áreas** (Saúde, Saneamento, Segurança, Educação, Infraestrutura e Administração/Outros). Cada área conta **por igual** — Educação com 17 editais pesa o mesmo que Administração com 163.

- **0,74** = em média o modelo vai **bem**, mas **não perfeito** — erra mais onde há poucos exemplos (Segurança, Educação).

**Para que serve:** medir se o modelo **classifica bem cada área**, não só se “acerta muito no geral”. Se chutasse sempre a área mais comum, a acurácia poderia parecer boa e ele seria **ruim** nas áreas pequenas — F1 macro evita esse truque.

**“No teste”** = medimos em **64 editais novos**, que o modelo **nunca viu** no treino.

**Frase oral:** “F1 macro 0,74 significa: nas seis macroáreas, o classificador acerta de forma razoável em média — útil para triagem, mas não infalível.”

### 5.3 Modelos comparados

A disciplina pede **PLN clássico** e **deep learning**. Nosso plano em três passos:

1. **Baseline clássico** (Fase 1) — obrigatório e interpretável.
2. **Deep learning moderno** (Fase 2) — Transformer em português (BERTimbau).
3. **Segundo clássico** (Fase 3) — mesmo texto da Fase 1, classificador diferente (SVM), para isolar o efeito do algoritmo.

**Comparação justa:** mesmo split 70/15/15, seed 42, mesma entrada (`objeto_html` no ComprasNet). Fases 1 e 3 compartilham o **mesmo TF-IDF**; só muda o classificador. Código: `src/models/`, `scripts/run_train.py`, configs em `configs/`.

#### Siglas usadas no projeto


| Sigla         | Nome completo                                                               | É rede neural?                       |
| ------------- | --------------------------------------------------------------------------- | ------------------------------------ |
| **TF-IDF**    | *Term Frequency – Inverse Document Frequency* — peso das palavras no texto  | Não (só transforma texto em números) |
| **LogReg**    | *Logistic Regression* — Regressão Logística                                 | **Não**                              |
| **SVM**       | *Support Vector Machine* — Máquina de Vetores de Suporte                    | **Não**                              |
| **BERT**      | *Bidirectional Encoder Representations from Transformers*                   | **Sim**                              |
| **BERTimbau** | BERT pré-treinado em português BR (`neuralmind/bert-base-portuguese-cased`) | **Sim**                              |


#### Fase 1 — TF-IDF + LogReg (modelo oficial)

**O que é:** aprendizado clássico em duas etapas. O **TF-IDF** conta palavras e n-gramas e dá peso a termos relevantes. A **Regressão Logística** aprende pesos lineares — “se aparece *seringa* e *medicamento*, tende a Saúde”.

**TF-IDF com bigramas** (*n-grama 2*): transforma o objeto em **números** a partir de **palavras isoladas** e de **pares de palavras adjacentes** (ex.: `aquisição de`, `de seringas`). Unigrama = 1 palavra; bigrama = 2 palavras seguidas — ajuda a capturar expressões curtas que uma palavra sozinha não distingue.

**Família:** machine learning clássico. **Não é** CNN, RNN nem Transformer.

**Config:** n-grama 2 (unigramas + bigramas), 20k features, `C=1.0`, `class_weight=balanced`.


| Parâmetro                   | O que faz (em português)                                                                                                                                                                                                                                                                            |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `**C=1.0**`                 | Força da **regularização** na Regressão Logística. `C` **grande** = modelo mais “confiante”, ajusta mais aos dados de treino (risco de overfitting). `C` **pequeno** = modelo mais “conservador”, suaviza pesos. **1.0** é o **padrão do scikit-learn** — começamos sem apertar nem relaxar demais. |
| `**class_weight=balanced**` | O corpus é **desbalanceado** (Saúde ~112 editais, Educação ~17). Com `balanced`, o algoritmo **dá mais peso a erros nas classes raras** — como se dissesse: “errar Educação custa mais que errar Administração/Outros”. Compensa a falta de exemplos **sem** duplicar editais artificialmente.      |


**Frase oral:** “Usamos `class_weight=balanced` porque as áreas não têm o mesmo tamanho; e `C=1.0` como regularização padrão, sem grid search neste projeto.”

**Resultado (ComprasNet, teste):** F1 macro **0,74** — **vencedor** no corpus de 423 editais; estável entre validação e teste. O F1 macro serve para medir se o modelo **classifica bem cada área**, não só se “acerta muito no geral” (ver §5.2).

**Por que escolhemos:** baseline obrigatório da disciplina; interpretável; funciona bem com **poucos dados** (~295 treinos).

#### Fase 2 — BERTimbau (deep learning)

**O que é:** fine-tuning de um **Transformer** que lê o texto **nos dois sentidos** (atenção multi-cabeça) e captura contexto entre palavras distantes — não depende só de contagem de termos.

**Família:** deep learning, arquitetura **Transformer** (encoder). **Não é** CNN nem RNN/LSTM.

**Config:** `max_len=512`, batch 16, lr 2e-5, 4 épocas, early stopping; GPU RTX 4090, fp16.

| Parâmetro | O que é / o que faz |
|-----------|---------------------|
| **`max_len=512`** | Tamanho máximo do texto em **tokens** (pedaços de palavra). O BERT lê no máximo **512** tokens por edital; o que passar disso é **cortado**. No nosso `objeto_html` quase nada passa de 512 — o limite quase não corta. |
| **batch 16** | Quantos editais o modelo vê **de uma vez** antes de atualizar os pesos. 16 = lote pequeno, cabe na memória da GPU e treina de forma estável. |
| **lr 2e-5** | *Learning rate* = **taxa de aprendizado** (0,00002). Controla **quanto** os pesos mudam a cada passo. Valor **baixo** típico de fine-tuning: adapta o BERTimbau sem “apagar” o que ele já sabe de português. |
| **4 épocas** | Uma **época** = uma passagem completa pelo conjunto de treino. Rodamos no máximo **4** voltas nos dados. |
| **early stopping** | Para o treino **antes** se a validação **parar de melhorar** — evita treinar à toa e overfitting. |
| **GPU RTX 4090** | Placa de vídeo usada no treino — BERT é pesado; na CPU seria muito mais lento. |
| **fp16** | *Half precision* (números com **16 bits** em vez de 32). Treino **mais rápido** e com **menos memória**, sem mudar o sentido do modelo. |

**Frase oral:** “Fine-tuning padrão: textos até 512 tokens, lotes de 16, taxa baixa 2e-5, no máximo 4 épocas com parada antecipada, na RTX 4090 em precisão mista.”

**Resultado:** F1 **0,40** (ComprasNet — pouco treino, colapsa em classes raras) · **0,86** (PNCP `pncp` — ~20 mil compras).

**Por que escolhemos:** exigência de DL do curso; estado da arte em PLN; testar se Transformer vence o baseline quando há **escala**.

#### Fase 3 — TF-IDF + SVM linear (comparativo clássico)

**O que é:** **mesmo TF-IDF** da Fase 1 (mesmos números por edital), mas o classificador é **SVM linear** (*Support Vector Machine* — Máquina de Vetores de Suporte).

**Como decide a área (bem simples):**

1. Cada edital vira uma **lista de números** (TF-IDF) — igual na Fase 1.
2. O modelo precisa de uma **regra de decisão**: “se o texto parece com estes números → Saúde; se parece com aqueles → Segurança”.
3. Essa regra é o que chamamos de **separação**: não é cortar o edital ao meio — é o **critério** que coloca cada texto em **uma área ou outra**.

**O que é “mais folga” (margem máxima):**

Imagine duas pilhas de editais já rotulados: uma de **Saúde**, outra de **Segurança**. Dá para inventar várias regras que separam as duas pilhas no treino. O SVM escolhe a regra que deixa **mais espaço de segurança** entre elas — não fica “colada” nos exemplos. Assim, um edital **novo** um pouco diferente ainda tende a cair no lado certo.

Em uma frase: **separação** = *como o modelo divide as áreas*; **mais folga** = *a divisão não fica apertada nos exemplos de treino*.

**LogReg vs SVM (mesmo texto, decisão diferente):**

| | **LogReg** | **SVM** |
|---|------------|---------|
| **Pergunta que responde** | “Qual a **chance** de ser Saúde?” | “Este texto fica do **lado Saúde** ou do **lado Segurança** da regra?” |
| **Como aprende** | Pesos por palavra/par de palavras | Regra de divisão com **mais espaço** entre as áreas |

**Linear** = a regra de divisão é **simples** (reta no espaço dos números), sem curva. Continua **ML clássico** — **não** é rede neural.

**Família:** machine learning clássico. **Não é** CNN, RNN nem Transformer.

**Resultado (ComprasNet, teste):** F1 **0,65** — pior que LogReg; melhor na validação (0,80) → **overfitting** (decorou demais os 64 de val e falhou no teste).

**Por que escolhemos:** mesmo TF-IDF, só muda o classificador — dá para ver se o SVM **bate** a LogReg no mesmo problema.

**Frase oral:** “LogReg e SVM leem o mesmo TF-IDF. A LogReg fala em probabilidade; o SVM aprende uma regra que divide as áreas deixando o maior espaço possível entre elas.”

#### O que **não** usamos (CNN e RNN/LSTM)


| Arquitetura                              | Por que ficou de fora                                                           |
| ---------------------------------------- | ------------------------------------------------------------------------------- |
| **CNN** (*Convolutional Neural Network*) | Problema é **texto livre**, não imagem ou grade                                 |
| **RNN / LSTM**                           | Sequências textuais hoje usam **Transformer**; BiLSTM seria redundante com BERT |


O eixo pedagógico do trabalho é **clássico linear (LogReg, SVM) vs Transformer (BERTimbau)**.

#### Síntese de métricas — tabela consolidada

Métrica primária: **F1 macro**. Reportamos **teste**; validação só para desenvolvimento. Detalhe e runs: §6.

**ComprasNet 423** (entrega oficial · `objeto_html` · teste = 64 editais)

| Fase | Modelo | F1 macro val | F1 macro teste | Accuracy teste | Veredito |
|:----:|--------|-------------:|---------------:|---------------:|----------|
| 1 | **TF-IDF + LogReg** | 0,743 | **0,740** | 0,797 | **Modelo oficial** — estável val≈teste |
| 3 | TF-IDF + SVM | 0,797 | 0,652 | 0,797 | Overfit (val alta, teste cai) |
| 2 | BERTimbau | 0,559 | 0,400 | 0,688 | Colapsa em classes raras |

**PNCP `pncp`** (~20 mil compras · 6 macroáreas por órgão · honesto em escala)

| Modelo | F1 macro val | F1 macro teste | Accuracy teste | Veredito |
|--------|-------------:|---------------:|---------------:|----------|
| TF-IDF + LogReg | 0,768 | 0,756 | 0,926 | Forte, mas atrás do BERT |
| TF-IDF + SVM | 0,813 | 0,783 | 0,939 | Melhor que LogReg; atrás do BERT |
| **BERTimbau** | 0,860 | **0,858** | 0,960 | **Vencedor em escala** |

**Leitura rápida:** no corpus **pequeno**, LogReg vence (F1 teste **0,74**). No corpus **grande**, BERT vence (F1 teste **0,86**). Accuracy sozinha engana — no ComprasNet LogReg e SVM têm a **mesma** accuracy (0,797), mas F1 macro diferente (0,74 vs 0,65).

**Hipótese “Transformer vence baseline”:** **refutada** no ComprasNet · **confirmada** no PNCP. O vencedor **depende do volume**.

**Resposta oral (15 s):** “LogReg e SVM são clássicos, sem rede neural, sobre TF-IDF. BERTimbau é Transformer. Com 423 editais vence LogReg (F1 0,74); com ~20 mil no PNCP vence BERT (F1 0,86).”

### 5.4 Extensão PNCP — protocolos e benchmark

Mesmo split 70/15/15 · seed 42 · entrada `objeto_html_limpo` ou `objeto_info_limpo` conforme protocolo.


| ID          | Config                                      | Descrição                                                 |
| ----------- | ------------------------------------------- | --------------------------------------------------------- |
| `pncp`      | `classification_pncp.yaml`                  | 6 macroáreas por órgão — **referência honesta em escala** |
| `pncp9`     | `classification_pncp_9setores.yaml`         | 9 setores; filtra sem keyword                             |
| `pncp9full` | `classification_pncp_9setores_full.yaml`    | 9 + Indeterminado                                         |
| `pncp9fb`   | `classification_pncp_9setores_fb.yaml`      | Fallback órgão                                            |
| `pncp9fbi`  | `classification_pncp_9setores_fb_info.yaml` | Fallback + info complementar                              |


Benchmark de coortes difíceis: `scripts/run_benchmark_pncp_dificeis.py`.

#### Por que usamos **informação complementar** no PNCP? (`pncp9fbi`)

**Contexto:** no PNCP, o `objeto_compra` costuma ser **curto e burocrático** — muitas linhas são genéricas (“contratação por inexigibilidade de licitação”, “aquisição de material de consumo”). No EDA, **~48%** das compras **não têm keyword setorial** só no objeto; **~853** ficam “escondidas” (órgão setorial, texto vago). O ComprasNet **não tem** esse campo extra; por isso a análise é **específica do PNCP**.

**Motivação (exploratória):** a planilha PNCP traz `**informacao_complementar`** em **~53%** das compras — parágrafo adicional que às vezes detalha *o quê* ou *por quê* se compra. Hipótese: concatenar objeto + info (`objeto_info_limpo`) pode **recuperar contexto semântico** que falta no objeto sozinho e ajudar — sobretudo o **BERT** — a classificar compras vagas.

**Como entra no pipeline (`pncp9fbi` apenas):**

1. **Entrada do modelo:** `objeto_info_limpo` = `limpar_objeto(objeto)` + `limpar_info_complementar(info)` (URLs removidas).
2. **Rotulagem (9 setores):** keywords são buscadas no **objeto + info**; se não achar, fallback pelo órgão (`pncp9fb`); senão → `Indeterminado`.
3. **Efeito na rotulagem:** em compras antes “vagas”, **~23%** ganham setor porque a keyword aparece **só na info**, não no objeto.

**O que aprendemos (não é protocolo oficial):**


| Modelo | Só objeto (`pncp9fb`) | Com info (`pncp9fbi`) | Leitura                                           |
| ------ | --------------------- | --------------------- | ------------------------------------------------- |
| LogReg | 0,824                 | **0,788**             | Info extra = **ruído** para sacola de palavras    |
| BERT   | 0,829                 | **0,955**             | Info extra = **sinal semântico** para Transformer |


**Ressalva metodológica:** em `pncp9fbi`, a **mesma info** entra no **rótulo** (regras de keyword) **e** no **texto** — há **acoplamento rótulo↔texto**; F1 alto (~0,95) reflete em parte **reprodução das regras**, não generalização cega. Por isso o protocolo **honesto de referência** continua sendo `**pncp`** (6 macroáreas, só `objeto_html_limpo`, F1 BERT **0,858**). Info complementar é **experimento exploratório** — próximo passo sensato: usá-la **só quando o objeto for vago**, não em todas as linhas.

**Resumo para a banca:** usamos info complementar **porque o PNCP tem objeto curto demais** e um campo extra com contexto; testamos se isso destrava classificação semântica (BERT sim, LogReg não), **declarando** o acoplamento e **sem** substituir a entrega honesta por órgão.

### 5.5 Reprodutibilidade

Cada treino gera `experiments/<run_id>.json` (métricas, hash do corpus, commit Git) + MLflow local. Matrizes de confusão em `reports/figures/`. Instruções completas: `[README.md](README.md)` e §10.

---

## 6. Resultados

Tabela consolidada (F1 macro val / F1 macro teste / accuracy teste) nos dois corpora: **§5.3 — Síntese de métricas**.

### 6.1 ComprasNet 423 — comparativo geral


| Modelo | F1 macro val | F1 macro teste | Accuracy val | Accuracy teste |
|--------|-------------:|---------------:|-------------:|---------------:|
| **TF-IDF + LogReg** | 0,743 | **0,740** | 0,766 | 0,797 |
| TF-IDF + SVM | 0,797 | 0,652 | 0,797 | 0,797 |
| BERTimbau | 0,559 | 0,400 | 0,734 | 0,688 |

#### Por que os números são diferentes?

**1. LogReg — val e teste quase iguais (0,743 ≈ 0,740)**  
O modelo **generalizou**: o que viu na validação se repetiu no teste. Por isso é o **oficial**. Accuracy no teste (0,797) é um pouco maior que o F1 (0,740) porque acerta bastante nas áreas **grandes** (Saúde, Administração); o F1 puxa a nota para baixo nas áreas **pequenas** (Segurança, Educação) — e é isso que queremos medir.

**2. SVM — val alta (0,797), teste cai (0,652)**  
Na validação o SVM **parece** o melhor. No teste **piora**. Isso é **overfitting**: com só **64** editais de val, a regra de “mais folga” se ajustou demais àquele pedaço e **não se manteve** em outros 64 nunca vistos. Accuracy no teste **igual** à do LogReg (0,797), mas F1 **menor** (0,652) — acerta o total parecido, porém **erra mais nas áreas raras** (Educação F1 0 no teste; ver §6.2).

**3. BERTimbau — pior nos dois (val 0,559 → teste 0,400)**  
Muitos parâmetros e **poucos** exemplos de treino (~295). Nas áreas com poucos editais (Segurança, Educação, Infraestrutura) o F1 vai a **zero** no teste — o modelo empurra quase tudo para Administração/Outros. Accuracy (0,688) ainda parece “razoável” porque a classe grande é frequente; o **F1 macro** mostra o colapso.

**4. Por que accuracy e F1 não batem?**  
Accuracy = “quantos editais acertei no total?”. F1 macro = “qual a nota **média por área**?”. Com classes desbalanceadas, dá para ter accuracy **igual** (LogReg e SVM = 0,797) e F1 **diferente** (0,74 vs 0,65). Por isso a métrica primária é **F1 macro no teste**, não accuracy.

**Decisão:** LogReg como modelo principal — melhor F1 no teste e estabilidade val≈teste.

Runs: `classification_baseline_20260624-013836` · `classification_svm_20260624-013851` · `classification_bertimbau_20260624-013908`.

### 6.2 ComprasNet — F1 por classe (teste)


| Área                 | n   | LogReg | SVM  | BERT |
| -------------------- | --- | ------ | ---- | ---- |
| Saúde                | 17  | 0,90   | 0,90 | 0,88 |
| Saneamento           | 7   | 1,00   | 1,00 | 0,80 |
| Segurança            | 9   | 0,46   | 0,46 | 0,00 |
| Educação             | 2   | 0,67   | 0,00 | 0,00 |
| Infraestrutura/Obras | 4   | 0,60   | 0,75 | 0,00 |
| Administração/Outros | 25  | 0,81   | 0,80 | 0,73 |


### 6.3 Vazamento de label — contraste de entradas


| Campo                   | F1 macro (teste)   | Vazamento lexical |
| ----------------------- | ------------------ | ----------------- |
| `texto` (HTML completo) | ≈ 0,88             | ≈ 97%             |
| `**objeto_html**`       | **≈ 0,74**         | ≈ 49%             |
| `objeto_html_limpo`     | marginal vs objeto | ≈ 47%             |


### 6.4 PNCP DF/2025 — extensão em escala

No PNCP (~20 mil compras DF/2025) testamos **vários protocolos**. Três são os que a banca precisa distinguir — F1 macro **no teste**:

| Protocolo | O que é (em uma frase) | LogReg | SVM | BERT | Papel no trabalho |
|-----------|------------------------|-------:|----:|-----:|-------------------|
| **`pncp`** | Honesto: **6 macroáreas**, rótulo pelo **órgão**, modelo lê só o **objeto** (igual espírito do ComprasNet, em escala) | 0,756 | 0,783 | **0,858** | **Referência principal** |
| **`pncp9`** | **9 setores** no objeto; **só** compras em que a keyword **já aparece** no texto (~10,3 mil) | 0,857 | 0,877 | **0,969\*** | Exploratório |
| **`pncp9full`** | **9 setores** em **todas** as 19,9k linhas; sem keyword → classe **Indeterminado** | 0,816 | 0,862 | **0,970\*** | Exploratório |

\*F1 alto — ler com ressalva abaixo.

#### Os três protocolos, explicados

**1. `pncp` — honesto (referência principal)**  
Mesma lógica da entrega ComprasNet: **seis áreas** (Saúde, Saneamento, Segurança, Educação, Infraestrutura/Obras, Administração/Outros), rótulo vem do **nome do órgão**, o modelo **não** recebe o órgão — só o objeto limpo. Serve para responder: *com muito mais dado, o BERT passa o clássico?* **Sim** — BERT **0,858** vs LogReg **0,756**. É o número que comparamos com o ComprasNet (LogReg **0,74** / BERT **0,40**).

**2. `pncp9` — 9 setores, só onde o texto já “diz” o setor**  
Mudamos o rótulo: em vez do órgão, usamos **palavra-chave no objeto** (lista completa no §4.3: Saúde, Educação, Segurança, Saneamento, Infraestrutura/Obras, **TI/Administração**, **Transporte**, **Cultura**, **Meio Ambiente**). **Filtramos** compras sem keyword — ficam ~10,3 mil. O desafio fica **mais fácil**: o setor muitas vezes está **escrito** no texto que o modelo lê. Por isso F1 sobe (BERT **0,969**). Não é trapaça escondida — é **reprodução de keyword**: o modelo aprende a repetir pistas que já definiram o rótulo. Por isso marcamos com \* e **não** usamos como entrega oficial.

**3. `pncp9full` — 9 setores em todas as linhas**  
Igual ao `pncp9`, mas **sem filtrar**: as ~48% sem keyword viram **Indeterminado**. Corpus completo (19,9k). BERT **0,970** — de novo alto, em parte porque a classe Indeterminado e as keywords no texto facilitam. Continua **exploratório**: mostra o que acontece com taxonomia mais fina e objetos vagos rotulados à parte, **não** substitui o `pncp` honesto.

#### Como ler os três juntos

| Pergunta | Protocolo que responde | Número a citar |
|----------|------------------------|----------------|
| “Com ~20 mil compras, quem vence de forma **honesta**?” | **`pncp`** | BERT **0,86** |
| “E se o rótulo vier do **texto** (keyword)?” | **`pncp9`** / **`pncp9full`** | até **0,97\*** — com ressalva |
| “Qual é a entrega / referência?” | **`pncp`** (+ ComprasNet LogReg **0,74**) | não os 0,97 |

**Frase oral:** “Três números: honesto em escala **0,86** (`pncp`); exploratório com keyword **0,97** (`pncp9` / `pncp9full`) — alto porque o rótulo e o texto compartilham a mesma pista; entrega oficial continua **0,74** no ComprasNet.”

Detalhe de `pncp9fb` / `pncp9fbi` (fallback e info complementar): §5.4. Runs `pncp`: `classification_pncp_*_20260628-23*`.

### 6.5 Insights aplicados — conexão com o mundo real

O modelo não é fim em si: cruzamos predições e labels com **distribuição temática** e **valor homologado** (EDA):

**ComprasNet 423 — distribuição por macroárea (label proxy):**


| Macroárea            | N editais | %     |
| -------------------- | --------- | ----- |
| Saúde                | 112       | 26,5% |
| Saneamento           | 49        | 11,6% |
| Segurança            | 58        | 13,7% |
| Educação             | 17        | 4,0%  |
| Infraestrutura/Obras | 24        | 5,7%  |
| Administração/Outros | 163       | 38,5% |


**Insight 1 — triagem:** com F1 **0,74**, o classificador permite **priorizar leitura humana** em dezenas de editais por macroárea sem ler os 423 um a um — útil para jornalismo de dados e controle social.

**Insight 2 — gasto concentrado:** Saúde concentra **26,5%** dos editais e **≈R$ 268 milhões** em valor homologado somado (mediana **≈R$ 482 mil** por edital) — poucos editais de Infraestrutura podem ter soma alta por contratos grandes; a **área predita** ajuda a orientar onde aprofundar a fiscalização.

**Insight 3 — objetos vagos (PNCP):** **~48%** das compras não têm keyword setorial no objeto; **~853** compras “escondidas” (órgão setorial, texto burocrático) exigem info complementar ou revisão humana — taxonomia com `Indeterminado` e fallback orgânico são necessários em produção.

**Insight 4 — escala muda a ferramenta:** para **triagem em massa** (~20 mil compras DF/2025), BERT (F1 **0,858**) supera LogReg (**0,756**); para **corpus pequeno e entrega oficial** (423 editais), LogReg (**0,74**) é mais estável que BERT (**0,40**).

---

## 7. Discussão

### 7.1 Dois corpora, dois vereditos sobre BERT


| Corpus        | n treino | BERT F1 teste | LogReg F1 teste | Lição                         |
| ------------- | -------- | ------------- | --------------- | ----------------------------- |
| ComprasNet    | ~295     | 0,40          | **0,74**        | Poucos dados → clássico ganha |
| PNCP (`pncp`) | ~14.000  | **0,858**     | 0,756           | Escala → Transformer ganha    |


O resultado **depende do volume e do protocolo** — alinhado ao material da disciplina.

### 7.2 Limitações, vieses e riscos

- **Label proxy** (~83% concordância): erros estruturais (Bombeiros + objeto clínico → label Segurança vs confusão Saúde).
- **Classes raras** no ComprasNet: F1 instável (Educação n=2 no teste).
- **Vazamento residual** (~49%) e **acoplamento rótulo↔texto** nos protocolos `pncp9`*.
- **PNCP ≠ ComprasNet:** textos curtos, inexigibilidade dominante, perfil burocrático.
- **Overfitting:** SVM val **0,80** → teste **0,65**; BERT colapsa em classes raras com ~295 treinos.

### 7.3 Possibilidades de melhoria

- Expandir corpus temporalmente (2021–2024); anotação manual parcial de labels.
- Info complementar **condicional** (só quando objeto vago).
- Revisar mapeamento órgão→área para reduzir Administração/Outros (**38,5%** no ComprasNet).
- Avaliar BERT na coorte **~853 escondidas** (LogReg F1 **~0,65** no benchmark; BERT pendente).

### 7.4 Uso responsável

Classificador **não substitui** análise jurídica. CAPTCHA do ComprasNet **não foi contornado**. Métricas altas em protocolos keyword devem ser lidas como **reprodução de regras**, não garantia de generalização em produção. Runs **negativos** (BERT 0,40) documentados — erros fazem parte do aprendizado científico.

---

## 8. Conclusão

O projeto percorreu o ciclo completo de PLN aplicado ao setor público: problema real delimitado, coleta ética, fundamentação bibliográfica, implementação comparativa, métricas adequadas e interpretação crítica.

**Principais aprendizados:**

1. **Entrega oficial (ComprasNet 423):** TF-IDF + LogReg — **F1 macro 0,74** no teste, superando SVM (0,65) e BERT (0,40).
2. **Extensão PNCP (~20 mil):** BERT — **F1 0,858** no protocolo honesto; escala + contexto semântico mudam o jogo.
3. **~48%** das compras PNCP são lexicalmente vagas — taxonomia com `Indeterminado` e fallback são necessários.
4. **Transparência metodológica** (proxy validado, vazamento documentado, val vs teste) é tão importante quanto a métrica.

**Próximos passos:** anos anteriores; cruzamento sistemático área predita × valor homologado × modalidade; BERT nas compras escondidas.

> A contribuição não é “a melhor métrica”, e sim **explicar o que a métrica significa**, **por que ela importa** e **como pode gerar valor** para transparência pública.

---

## 9. Referências

### Domínio (licitações, transparência, setor público)

1. FERREIRA, H. H. **Processamento de linguagem natural e classificação de textos em sistemas modulares**. 2019. TCC (Bacharelado em Ciência da Computação) — Universidade de Brasília.
2. MACEDO, J. M. A. et al. Avaliação de sistemas de governo aberto e de transparência pública nas capitais brasileiras. **Cadernos Gestão Pública e Cidadania (FGV)**, v. 30, n. 1, 2025. DOI: 10.12660/cgpc.v30.90832.
3. ROSADO, K. M. L.; DIAS, C. da C. Promovendo acessibilidade e compreensão na área da informação jurídica. **Ciência da Informação em Revista**, v. 11, e16631, 2024. DOI: 10.28998/cirev.2024v11e16631.
4. SOUTO, A. de L.; GOMES, V. C.; RIVEROS, J. L. T. Inteligência Artificial em Auditoria de Licitações: o caso Alice na CGU e no TCU. **Revista Síntese**, v. 2, n. 1, 2025. DOI: 10.70690/f9axse22.
5. WATANABE, E.; SOUSA, R. T. B. de. Uso do aprendizado de máquina para a classificação automática de documentos de arquivo: experimento inicial em uma organização pública. **Tendências da Pesquisa Brasileira em Ciência da Informação**, v. 16, 2023.

**Marco legal:** Lei nº 14.133/2021 · Lei nº 12.527/2011 · Lei nº 15.263/2025 · Decreto nº 8.777/2016 (dados abertos).

### Técnica (PLN / deep learning / classificação)

1. DEVLIN, J. et al. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. **NAACL**, 2019.
2. GOODFELLOW, I.; BENGIO, Y.; COURVILLE, A. **Deep Learning**, cap. 10 (modelagem de sequências). MIT Press, 2016.
3. PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. **JMLR**, v. 12, p. 2825-2830, 2011.
4. SOUZA, F.; NOGUEIRA, R.; LOTUFO, R. BERTimbau: Pretrained BERT Models for Brazilian Portuguese. **BRACIS**, 2020.
5. SRIVASTAVA, N. et al. Dropout: A Simple Way to Prevent Neural Networks from Overfitting. **JMLR**, v. 15, p. 1929-1958, 2014.

**Operacional:** [https://pncp.gov.br/](https://pncp.gov.br/) · `neuralmind/bert-base-portuguese-cased` · PDFs em `[docs/referencias/](referencias/)`.

---

## 10. Apêndice técnico

### Pipeline ComprasNet

```
CSV ComprasNet DF 2025
  → download HTML (423, delay 0,8 s)
  → licitacoes_corpus.jsonl
  → split 70/15/15
  → LogReg / SVM / BERTimbau
```

### Pipeline PNCP

```
PNCP XLS (DF 2025)
  → run_preprocess_pncp.py
  → pncp_corpus_df2025.jsonl (19.944)
  → protocolos pncp / pncp9 / pncp9full / pncp9fb / pncp9fbi
  → benchmark coortes difíceis
```

### Reprodução

```bash
pip install -r requirements-dev.txt
pip install -e ".[bert]"
python scripts/run_collect.py && python scripts/run_preprocess.py
python scripts/run_preprocess_pncp.py
python scripts/run_train.py --model baseline --config configs/classification.yaml
python scripts/run_train.py --model bertimbau --config configs/classification_pncp.yaml \
  --corpus data/processed/pncp_corpus_df2025.jsonl
python scripts/run_benchmark_pncp_dificeis.py
```

Repositório público GitHub; dados acessíveis via scripts de coleta; dependências em `requirements-dev.txt` e `pyproject.toml`.

### Comunicação — apresentação oral (10 min)

Slides e roteiro alinhados à estrutura sugerida da disciplina:


| Slide | Conteúdo                                | Documento                                                                                       |
| ----- | --------------------------------------- | ----------------------------------------------------------------------------------------------- |
| 1     | Contexto                                | `[APRESENTACAO-CONTEUDO.md](APRESENTACAO-CONTEUDO.md)` · `[roteiro_10min.md](roteiro_10min.md)` |
| 2     | Base teórica (5+5)                      | idem                                                                                            |
| 3     | Dados                                   | idem                                                                                            |
| 4     | Metodologia + vazamento                 | idem                                                                                            |
| 4b    | Arquitetura (CNN/RNN/Transformer)       | idem                                                                                            |
| 5–6   | Resultados ComprasNet + PNCP            | idem                                                                                            |
| 7–8   | Discussão · Conclusão · Próximos passos | idem                                                                                            |


PDF final dos slides: entregável da disciplina (repositório + apresentação em sala).

### Síntese oral (10 min)

> Coletamos **423 editais** ComprasNet (DF 2025). LogReg F1 **0,74** no teste venceu SVM (0,65) e BERT (0,40) — corpus pequeno favorece o clássico. Estendemos com **19.944 compras PNCP**: BERT F1 **0,858** no protocolo por órgão. Exploramos 9 setores empíricos, fallback orgânico e info complementar — F1 até 0,97, mas com acoplamento rótulo↔texto que declaramos. A contribuição é explicar **o que a métrica significa** e o cuidado metodológico por trás dela.

---

*Documento consolidado · junho/2026 · ComprasNet runs 24/06/2026 · PNCP runs 28–29/06/2026*