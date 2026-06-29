# Classificação de editais por área de gasto e sumarização em linguagem cidadã — Distrito Federal, 2025

**Projeto Final — Deep Learning e PLN · Modalidade 2: PLN no Setor Público**

**Integrantes:** Elisangela Osorio · Alexandre Ferreira Ponte · Renê Estevam Deckers · Alexandre Hugo Sampaio Netto

---

## 1. Contexto e problema

Editais de licitação pública descrevem, em linguagem jurídica e técnica, o que o governo pretende comprar ou contratar. No Distrito Federal, centenas desses documentos são publicados todo ano no portal ComprasNet. Para um cidadão, um pequeno empresário ou um órgão de controle, ler cada edital manualmente para responder perguntas como *“em que áreas o governo está gastando?”* ou *“o que este edital significa na prática?”* é inviável.

Este projeto aplica técnicas de Processamento de Linguagem Natural a **423 editais reais** do DF em 2025, coletados pelo próprio grupo — atendendo à exigência da disciplina de usar dados inéditos, sem bases prontas de plataformas como Kaggle. O trabalho desenvolve duas tarefas complementares sobre o mesmo corpus:

1. **Classificação (tarefa principal):** inferir automaticamente a **macroárea de gasto público** a partir da descrição do objeto da licitação — Saúde, Saneamento, Segurança, Educação, Infraestrutura/Obras ou Administração/Outros.


A escolha conecta PLN a um problema concreto de transparência e acessibilidade no setor público: facilitar a triagem temática de licitações e reduzir a barreira de entrada para quem não domina o jargão administrativo.

---

## 2. Justificativa

O tema é relevante em três dimensões. **Na dimensão aplicada**, licitações são instrumento central de execução orçamentária; automatizar sua leitura apoia fiscalização, jornalismo de dados e participação de micro e pequenas empresas. **Na dimensão técnica**, o corpus permite comparar, no mesmo protocolo experimental, um baseline clássico (TF-IDF), um classificador SVM e um Transformer em português (BERTimbau) — respondendo empiricamente se, com ~423 documentos, o deep learning supera métodos mais simples. **Na dimensão social**, resumos em linguagem acessível ilustram como a IA pode servir ao cidadão, e não apenas gerar métricas.

A hipótese inicial era que o BERTimbau, por capturar contexto semântico, superaria TF-IDF + Regressão Logística. Os experimentos mostraram o contrário neste volume de dados — o que, por si só, é um achado metodológico relevante para o relatório.

---

## 3. Referencial teórico

O trabalho se apoia em duas linhas de literatura, conforme exigido pela disciplina (mínimo cinco referências de domínio e cinco de técnica, citadas no corpo do texto).

**Domínio:** contratações públicas e transparência (Lei 14.133/2021, ComprasNet, Portal Nacional de Contratações Públicas); classificação temática de gastos governamentais; acessibilidade de informação pública para cidadãos e pequenos fornecedores.

**Técnica:** representação sparse de texto (TF-IDF) e classificadores lineares; fine-tuning de Transformers para português brasileiro (BERTimbau, Souza et al.); métricas para classificação multiclasse desbalanceada (F1 macro); sumarização extrativa versus abstrativa; diagnóstico de viés-variância e vazamento de label (*label leakage*) em tarefas de PLN supervisionado.

Essas referências fundamentam decisões concretas do projeto: usar F1 macro em vez de accuracy isolada; incluir baseline clássico antes do Transformer; evitar o HTML completo como entrada por vazamento de label; preferir sumarização extrativa inicialmente, para não inventar prazos ou valores.

---

## 4. Dados

### 4.1 Fonte e coleta

Os dados vêm do **ComprasNet** (http://www.comprasnet.gov.br/). O grupo exportou um CSV com licitações do **Distrito Federal em 2025** (437 linhas). A coluna *Edital* contém URLs para páginas de detalhe de cada licitação.

A coleta textual seguiu duas etapas reprodutíveis:

1. **Download das páginas HTML** de detalhe — 423 URLs únicas (14 duplicatas no CSV). Intervalo de 0,8 segundo entre requisições para respeitar o servidor público. Nenhum erro HTTP.
2. **Extração e normalização** do texto: parsing do HTML, conversão de Latin-1 para UTF-8, geração de um corpus estruturado com 423 registros.

**Por que HTML e não PDF?** O botão de download de PDF no ComprasNet exige CAPTCHA (validação anti-robô). Automatizar centenas de PDFs exigiria contorno antiético do sistema — rejeitado pelo grupo. O HTML de detalhe traz órgão, objeto, itens e metadados suficientes para PLN, sem CAPTCHA.

### 4.2 Volume e características

| Aspecto | Valor |
|---------|------:|
| Editais únicos | 423 |
| Período | DF, 2025 |
| Material / Serviço | 320 / 103 (76% / 24%) |
| Tamanho do objeto (texto) | mediana ~1.600 caracteres; média ~3.400; máximo ~41.300 |
| Modalidade predominante | Pregão eletrônico (278); dispensa (134) |

### 4.3 Rotulagem (labels)

Não houve tempo para rotular manualmente os 423 editais. O **rótulo proxy** vem do nome do órgão comprador no CSV: palavras-chave mapeiam cada órgão a uma das seis macroáreas (ex.: Secretaria de Saúde → Saúde; CAESB → Saneamento; Bombeiros → Segurança).

Distribuição aproximada: Administração/Outros 176 · Saúde 106 · Segurança 51 · Saneamento 49 · Infraestrutura/Obras 24 · Educação 17.

O classificador **não recebe o nome do órgão como entrada** — apenas o texto do objeto. Caso contrário, o modelo faria lookup de metadados, não PLN.

Para avaliar a qualidade desse proxy, os quatro integrantes revisaram **30 editais** sorteados (estratificados por área). A concordância média com o label automático foi de **≈83%** (variando de 62% a 96% entre revisores). Conclusão: rotulagem fraca aceitável para baseline acadêmico, mas limitação a declarar na discussão.

### 4.4 Limitações dos dados

- Corpus **pequeno** para fine-tuning de Transformer (~295 exemplos de treino).
- **Desbalanceamento**: Educação e Infraestrutura têm poucos exemplos; no conjunto de teste, Educação tem apenas 2 editais.
- Documento = **HTML de detalhe**, não PDF integral; o campo Objeto do CSV pode estar truncado.
- Escopo **geográfico e temporal restrito** (só DF 2025) — generalização não testada.
- Coleta datada: links podem expirar; o CSV versionado e o script de download garantem reprodutibilidade.

---

## 5. Metodologia

### 5.1 Análise exploratória

Antes do treino, foi feita análise exploratória sobre os 423 editais: distribuição por área, órgão, modalidade, tamanho de texto, material versus serviço, e comparação entre campos de entrada possíveis. Um achado crítico: o HTML completo (`texto`) repete o nome do órgão em **≈97%** dos casos em que a keyword da área aparece — porque o label veio justamente do órgão. Usar esse campo inflaria artificialmente a performance (F1 macro ≈ 0,88). O campo **`objeto_html`** (só a descrição da compra) reduz esse vazamento para **≈49%** e foi adotado como **entrada oficial** do classificador, com F1 macro ≈ 0,74 — número mais honesto, embora ainda com vazamento residual.

Dois conceitos distintos: **vazamento de label** (informação do rótulo aparece no texto de entrada) e **label proxy** (rótulo derivado do órgão, não anotado humanamente). Mitigar um não resolve o outro.

### 5.2 Protocolo experimental (classificação)

Todos os classificadores compartilharam o mesmo protocolo:

| Decisão | Valor |
|---------|-------|
| Entrada | Texto do objeto (`objeto_html`) |
| Partição | 70% treino / 15% validação / 15% teste, estratificada por área |
| Tamanhos | 295 treino · 64 validação · 64 teste |
| Seed | 42 (mesmas partições nos três modelos) |
| Métrica primária | **F1 macro no conjunto de teste** |
| Critério de escolha | Melhor F1 no **teste**, nunca só na validação |

F1 macro calcula a média do F1 de cada classe com peso igual — adequado quando Saúde e Administração dominam o corpus, mas Educação tem só 2 exemplos no teste. Accuracy sozinha seria enganosa: 79% de acertos pode esconder F1 zero em classes raras.

### 5.3 Modelos treinados

**Fase 1 — TF-IDF + Regressão Logística (modelo principal):** vetorização TF-IDF (unigramas e bigramas, até 20.000 features, `min_df=2`), classificador com `class_weight=balanced` e regularização L2 (`C=1.0`). Baseline clássico, rápido e interpretável.

**Fase 2 — BERTimbau (comparativo de deep learning):** fine-tuning de `neuralmind/bert-base-portuguese-cased`, `max_length=512`, batch 16, learning rate 2e-5, até 4 épocas com early stopping (patience 2). Treinado em GPU (RTX 4090).

**Fase 3 — TF-IDF + SVM linear (comparativo clássico):** mesmo vetorizador da Fase 1; kernel linear, `class_weight=balanced`.

**Fase 4 — Sumarização extrativa (complementar):** regras e expressões regulares extraem objeto, modalidade, tipo de participante, prazo e valor homologado. Amostra de 18 editais estratificados por área. Escolhido por ser determinístico — não inventa prazos nem valores, ao contrário de modelos generativos que poderiam alucinar.

### 5.4 Avaliação e reprodutibilidade

Cada treino gera registro com métricas, hash do corpus e commit Git. Matrizes de confusão foram geradas para os três classificadores. O conjunto de teste não foi usado para escolher hiperparâmetros — apenas para o número final do relatório.

---

## 6. Resultados

### 6.1 Classificação — comparativo geral

| Modelo | F1 validação | F1 teste | Accuracy teste |
|--------|-------------:|---------:|---------------:|
| **TF-IDF + LogReg** | 0,743 | **0,740** | 0,797 |
| TF-IDF + SVM | 0,797 | 0,652 | 0,797 |
| BERTimbau | 0,559 | 0,400 | 0,688 |

O **LogReg** foi escolhido como modelo principal: melhor F1 macro no teste e estabilidade entre validação e teste (queda de apenas 0,003). O **SVM** parecia superior na validação (0,797) mas caiu para 0,652 no teste — sinal de ajuste excessivo aos 64 editais de validação. O **BERT** teve gap ainda maior (0,559 → 0,400) e praticamente ignorou classes minoritárias no teste.

### 6.2 Desempenho por classe (teste)

| Área | Exemplos no teste | LogReg | SVM | BERT |
|------|------------------:|-------:|----:|-----:|
| Saúde | 17 | 0,90 | 0,90 | 0,88 |
| Saneamento | 7 | 1,00 | 1,00 | 0,80 |
| Segurança | 9 | 0,46 | 0,46 | 0,00 |
| Educação | 2 | 0,67 | 0,00 | 0,00 |
| Infraestrutura/Obras | 4 | 0,60 | 0,75 | 0,00 |
| Administração/Outros | 25 | 0,81 | 0,80 | 0,73 |

Saúde e Saneamento funcionam bem nos três modelos clássicos — palavras como “medicamentos”, “insumos hospitalares” ou “abastecimento de água” discriminam bem. Segurança confunde-se frequentemente com Administração/Outros quando o texto do objeto não menciona polícia ou bombeiros. Educação, com apenas 2 exemplos no teste, produz F1 instável: um erro já derruba a métrica. O BERT colapsou nas classes raras e convergiu para prever Administração/Outros (recall 0,96 nessa classe).

### 6.3 Vazamento de label — contraste de entradas

| Campo de entrada | F1 macro (teste) | Keywords da área no texto |
|------------------|------------------|---------------------------|
| HTML completo | ≈ 0,88 | ≈ 97% |
| **Objeto da licitação** | **≈ 0,74** | ≈ 49% |

A diferença confirma que métricas altas com o HTML completo refletem, em grande parte, memorização do órgão — não compreensão semântica do gasto.

### 6.5 Impacto aplicado

Além das métricas, o projeto permite cruzamentos úteis à transparência: distribuição de licitações por área predita, relação entre área e valor homologado, concentração por modalidade (pregão versus dispensa). A classificação responde *“em que o DF gasta?”*; a sumarização responde *“o que este edital significa para quem quer participar?”* — duas faces do mesmo problema de acessibilidade.

---

## 7. Discussão

### 7.1 Interpretação dos resultados

O baseline TF-IDF + LogReg venceu não por acaso, mas por adequação ao **tamanho do corpus**. Com ~295 exemplos de treino e seis classes, um modelo com dezenas de milhões de parâmetros (BERT) tende a overfitting — especialmente nas classes com dezenas de exemplos. Termos discriminativos no objeto (“medicamentos antimetabólitos”, “tubos de PVC”, “combustível”) são capturados eficientemente por TF-IDF. O `class_weight=balanced` mitigou parcialmente o desbalanceamento sem destabilizar a generalização.

A lição do SVM é metodológica: **validação alta não garante teste alto** quando o conjunto de validação tem apenas 64 exemplos e classes raras com 2–3 amostras. Educação teve F1 1,0 na validação (3 exemplos, todos corretos) e F1 0,0 no teste (2 exemplos, ambos errados).

### 7.2 Limitações e vieses

- **Label proxy:** um edital de material hospitalar comprado por órgão de segurança recebe label errado — explica confusões Segurança ↔ Saúde.
- **Volume insuficiente** para conclusões robustas sobre Educação e Infraestrutura.
- **Vazamento residual** (~49%) ainda permite que keywords do órgão apareçam no objeto.
- **HTML ≠ edital oficial completo** — cláusulas longas podem estar ausentes.
- **Fine-tuning não determinístico:** retreinos do BERT variaram (teste entre 0,40 e 0,52) mesmo com mesmo seed de split.
- **Sumarização extrativa** não parafraseia — o texto ainda pode ser denso; modelos abstrativos exigiriam avaliação humana rigorosa.

### 7.3 Uso responsável

O classificador **não substitui** análise jurídica ou decisão administrativa. Resumos automatizados devem ser verificados contra o edital original. O grupo **não contornou** o CAPTCHA do ComprasNet — decisão ética alinhada ao uso responsável de IA exigido pela disciplina.

---

## 8. Conclusão

O projeto demonstrou, na prática, o ciclo completo de um trabalho de PLN aplicado ao setor público: identificação de problema real, coleta reprodutível de dados, implementação de múltiplos modelos, avaliação com métricas adequadas e interpretação crítica dos resultados.

**Principais aprendizados:**

1. Foi possível classificar editais do ComprasNet (DF 2025) em seis macroáreas de gasto com **F1 macro 0,74** no teste, usando TF-IDF + Regressão Logística sobre a descrição do objeto.
2. A hipótese de superioridade do BERTimbau **não se confirmou** neste corpus (F1 teste 0,40); o deep learning não é automaticamente superior quando os dados são escassos e desbalanceados.
3. A transparência metodológica — proxy de label validado (~83%), vazamento documentado, comparação honesta de três arquiteturas — é tão importante quanto a métrica final.
4. A sumarização extrativa complementa o trabalho com resumos legíveis e verificáveis, ilustrando impacto social sem risco de alucinação.

**Próximos passos:** expandir o corpus para anos anteriores (2021–2024) e estabilizar classes raras; corrigir labels com anotação manual parcial; experimentar sumarização abstrativa (mT5) com avaliação humana; cruzar área predita com valor homologado e geografia para insights de política pública.

---

## 5.5 Extensão PNCP DF/2025 (exploratória)

Além dos 423 editais ComprasNet, o grupo montou corpus PNCP com **19.944 compras** (`UF=DF`, `ano=2025`) via `scripts/run_preprocess_pncp.py`. Objetivo: testar escala, taxonomia de **9 setores empíricos** (keyword no objeto) e mitigações para textos vagos.

### Protocolos implementados

| ID | Rótulo | Corpus | F1 macro teste (melhor modelo) |
|----|--------|--------|-------------------------------|
| `pncp` | 6 macroáreas (órgão) | 19.944 | **BERT 0,858** |
| `pncp9` | 9 setores, só keyword | ~10.311 | BERT 0,969 |
| `pncp9full` | 9 + Indeterminado | 19.944 | BERT 0,970 |
| `pncp9fb` | fallback órgão | 19.944 | LogReg 0,824 |
| `pncp9fbi` | fallback + info complementar | 19.944 | **BERT 0,955** |

### Achados principais

1. **Escala muda o veredito BERT vs clássico:** no PNCP honesto por órgão, BERT (0,858) supera LogReg (0,756) — oposto ao corpus 423 (0,40 vs 0,74).
2. **~48%** das compras não têm keyword setorial no objeto; classe `Indeterminado` é necessária.
3. **Fallback por órgão** resgata ~853 “escondidas” (órgão nomeado, objeto burocrático).
4. **Info complementar:** piora modelos lineares (0,824→0,788) mas BERT sobe para 0,955 — valor semântico só emerge com Transformer.
5. F1 ~0,97 nos protocolos keyword **não invalida** o trabalho, mas exige **declarar acoplamento rótulo↔texto** (regras documentadas em [`REGRAS-E-PROTOCOLOS.md`](REGRAS-E-PROTOCOLOS.md)).

A **entrega oficial da disciplina** permanece o protocolo ComprasNet 423 com LogReg F1 **0,74**. PNCP é extensão analítica documentada.

---

## 9. Referências

*(Completar formatação ABNT/IEEE no PDF final — mínimo 5 domínio + 5 técnica.)*

**Domínio:** Lei nº 14.133/2021 (Nova Lei de Licitações); Portal ComprasNet; Portal Nacional de Contratações Públicas (PNCP); literatura sobre transparência e classificação temática de gastos públicos; acessibilidade de informação governamental.

**Técnica:** Souza et al. — BERT models for Brazilian Portuguese (BERTimbau); Devlin et al. — BERT; Pedregosa et al. — scikit-learn; Manning & Schütze — Foundations of Statistical NLP; artigos sobre F1 em classificação desbalanceada; Mani & Maybury — Advances in Automatic Text Summarization.

**Fontes operacionais:** http://www.comprasnet.gov.br/ · https://pncp.gov.br/ · modelo `neuralmind/bert-base-portuguese-cased`.

---

## 10. Apêndice técnico

**Pipeline completo:**

```
Export CSV (ComprasNet DF 2025)
    → download HTML de detalhe (423 arquivos, delay 0,8 s)
    → extração de texto e metadados
    → corpus JSONL (423 registros)
    → split estratificado 70/15/15
    → treino LogReg / SVM / BERTimbau
    → sumarização extrativa (amostra de 18)
```

**Hiperparâmetros principais:** TF-IDF com ngramas até 2, max 20.000 features; LogReg `C=1.0`, `class_weight=balanced`; SVM kernel linear; BERTimbau lr 2e-5, batch 16, early stopping patience 2.

**Reprodução:** Python 3.10+, dependências via `pip install -r requirements-dev.txt`; scripts `run_collect.py`, `run_preprocess.py`, `run_train.py`; atalhos `make train-baseline`, `make train-bert`, `make train-svm`, `make train-summarize`.

**Entregáveis da disciplina:** repositório público no GitHub com código reprodutível; descrição da coleta (seção 4 deste documento); dados acessíveis via script de download; slides em PDF para apresentação oral de 10 minutos.

**Síntese para apresentação:**

> Coletamos 423 editais do ComprasNet (DF 2025) e treinamos três classificadores no mesmo split. LogReg: validação 0,74, teste 0,74. SVM: validação 0,80, teste 0,65. BERT: validação 0,56, teste 0,40. Escolhemos LogReg porque o teste é o que importa. Complementamos com resumos extrativos para cidadãos — 83% dos prazos e 100% dos valores extraídos na amostra.

---

*Documento consolidado · junho/2026 · runs ComprasNet 24/06/2026 · extensão PNCP 28–29/06/2026*
