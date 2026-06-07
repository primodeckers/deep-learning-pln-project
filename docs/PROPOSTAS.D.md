# Propostas de tema — o que a gente pode fazer com os editais

Documento de brainstorm do grupo. A ideia é escolher **uma tarefa de PLN** pro projeto final (Modalidade 2 — PLN no Setor Público) e parar de ficar em cima do muro.

Links úteis:

- Requisitos da disciplina → [`PROJECT-REQUIREMENTS.md`](PROJECT-REQUIREMENTS.md)
- Dados prontos → [`licitacoes_corpus.jsonl`](../data/processed/licitacoes_corpus.jsonl) (423 editais)
- Como a gente coletou → [`DATA-COLLECTION-DECISIONS.md`](DATA-COLLECTION-DECISIONS.md)

---

## O que já temos na mão

A coleta e o pré-processamento já rodaram. Não estamos começando do zero.

- **423 editais** do DF (2025), baixados do ComprasNet em HTML
- Cada um virou um registro no corpus com o **texto completo** extraído
- O CSV original traz metadados: órgão, modalidade, tipo (material/serviço), valor homologado, etc.
- PDF completo ainda **não** — tem CAPTCHA, então ficou pra depois se precisar

Alguns números que ajudam a pensar:

- **320** licitações de material, **103** de serviço
- Maioria é **pregão** (278); tem também dispensa (134) e pouquíssima concorrência (11)
- Os textos variam muito: alguns têm só 2 linhas, outros passam de 40 mil caracteres
- Quem mais aparece: Saúde (~99), CAESB (~49), Bombeiros, Educação, Estradas de Rodagem…

Ou seja: dá pra treinar modelo, dá pra fazer gráfico, dá pra contar história — só falta **escolher o foco**.

---

## As quatro ideias (visão geral)

| # | Em uma frase | Dá trabalho? | Impacto na apresentação |
|---|---|---|---|
| **1** | Classificar edital por área de gasto (Saúde, Saneamento…) | Médio | Alto — responde “em que o DF gasta?” |
| **2** | Puxar datas, valores e prazos automaticamente do texto | Alto | Alto — mas anotar entidade é chato |
| **3** | Achar editais parecidos e agrupar por tema | Médio-baixo | Médio — gráfico bonito, menos “modelo clássico” |
| **4** | Resumir edital em português que qualquer um entende | Médio-alto | Muito alto — demo “antes/depois” fica show |

**Leitura honesta do grupo (por enquanto):** a **Ideia 1** parece o melhor equilíbrio — dá métrica clara (F1, matriz de confusão), usa Transformers, e ainda conecta com transparência pública. Mas não é consenso fechado ainda; é só a tendência.

---

## Ideia 1 — Classificar por área de gasto público

### O problema (sem jargão)

Todo edital tem um campo **Objeto** — é um textão livre dizendo o que o governo quer comprar ou contratar. Um fala em “medicamentos antimetabólitos”, outro em “digitalização técnica”, outro em “tubos de PVC”.

Se você é cidadão, jornalista ou servidor de controle, olhar 423 descrições diferentes e tentar responder **“quanto foi pra saúde? quanto foi pra obras?”** é inviável na mão.

### O que a gente faria

O modelo lê o texto do edital e devolve uma **categoria**, tipo:

- Saúde
- Saneamento
- Segurança
- Educação
- Infraestrutura / Obras
- Administração / Outros

**Exemplo rápido:** edital que fala em compra de medicamentos oncológicos pra Secretaria de Saúde → **Saúde**.

### Como resolver o label sem enlouquecer

Rotular 423 editais na mão dá preguiça (e tempo). A saída pragmática:

1. Usar o **órgão** do CSV como label inicial (Saúde → área Saúde, CAESB → Saneamento…)
2. Treinar o modelo no **texto**, não no nome do órgão
3. Pegar uns **30 editais** e revisar na mão pra ver se o label faz sentido
4. No relatório, ser transparente: “label veio do órgão, não de anotação humana completa”

Distribuição aproximada se a gente fizer assim:

| Área | ~Quantos editais |
|---|---|
| Saúde | 106 |
| Saneamento | 49 |
| Segurança | 33 |
| Educação | 17 |
| Infra / Obras | 24 |
| Administração / Outros | 194 |

A classe “Outros” vai ficar grande — isso é uma limitação real, não tem problema admitir.

### Caminho técnico (o que o professor quer ver)

1. Limpar e preparar o texto
2. Separar treino / validação / teste (tipo 70/15/15)
3. **Baseline:** TF-IDF + Regressão Logística (simples, rápido, funciona)
4. **Modelo principal:** BERTimbau fine-tuned
5. Comparar F1, matriz de confusão, ver onde erra
6. **Extra que pontua:** cruzar erros com valor homologado, modalidade, material vs serviço

### Título que serviria pro trabalho

> *Classificação automática de editais de licitação por área de gasto público (Distrito Federal, 2025)*

### Quem faz o quê (rascunho)

- **Pessoa A:** taxonomia, mapeamento órgão→área, artigos de domínio
- **Pessoa B:** baseline sklearn + métricas
- **Pessoa C:** BERTimbau + comparação de modelos + artigos de técnica
- **Pessoa D:** validação manual da amostra, gráficos, slides

### O que pode dar errado

- Modelo “decorar” o órgão em vez de entender o tema → testar só com o campo objeto
- Poucos exemplos de Educação (17) → F1 baixo nessa classe, explicar no slide
- Textos muito curtos → tirar ou tratar à parte

**Veredicto:** factível, entregável, boa história pra contar na banca.

---

## Ideia 2 — Extrair informações do edital (NER)

### O problema

Editais são longos. Pra achar **até quando manda proposta**, **quanto custa** ou **quais documentos precisa**, você precisa ler tudo — ou Ctrl+F e torcer.

### O que a gente faria

Um extrator que marca no texto coisas como:

- Valores (R$ 62.800,00)
- Datas (16/05/2025)
- Prazos (90 dias, 12 meses)
- Modalidade / lei citada
- Requisitos técnicos

### Caminho técnico

- Começar com **regex** (datas, dinheiro) — baseline honesto
- Tentar spaCy em português
- Fine-tuning só se alguém topar **anotar** dezenas de editais na mão

### O problema real desta ideia

**Anotação.** Sem labels de entidade, o projeto vira só regex — funciona, mas é fraco pras referências de NER/Transformers que a disciplina pede.

**Veredicto:** ótima ideia de produto, pesada pro prazo. Só se 1 pessoa assumir anotação desde já.

---

## Ideia 3 — Achar editais parecidos (similaridade)

### O problema

Dois órgãos podem descrever a **mesma compra** com palavras diferentes. “Notebook” num edital, “equipamento de informática portátil” noutro. Isso atrapalha comparar preço e ver se alguém está fragmentando licitação.

### O que a gente faria

1. Transformar cada edital em um vetor (embedding)
2. Medir quão parecidos são (similaridade de cosseno)
3. Agrupar os parecidos (cluster)
4. Olhar na mão os grupos: faz sentido? mesmo órgão? valor parecido?

Dá um insight legal tipo: *“12 editais de material de escritório, órgãos diferentes, valores entre 5 e 15 mil”*.

### Caminho técnico

- Sentence-Transformers ou BERTimbau
- K-Means ou HDBSCAN
- Gráfico UMAP/t-SNE pro slide (fica visual)

### O porém

Não tem “acertou/errou” clássico. É mais análise exploratória. O professor pode querer ver treino supervisionado explícito.

**Veredicto:** funciona muito bem como **complemento** da Ideia 1 (um gráfico extra no relatório). Sozinha, é mais arriscado.

---

## Ideia 4 — Resumir edital em linguagem de gente

### O problema

Editais falam “sistema de registro de preços”, “qualificação técnica”, “declaração de responsabilidade”. Meu pai, que tem padaria, não ia entender nada — e ele é exatamente o tipo de pequeno fornecedor que edital deveria alcançar.

### O que a gente faria

Entrada: texto do edital.  
Saída: 3–5 frases respondendo:

- O que está sendo comprado?
- Quem pode participar?
- Até quando?

**Exemplo:**

> *Original:* “Pregão Eletrônico nº 90119/2025… Aquisição dos medicamento(s)… ANTIMETABÓLITOS… Entrega da Proposta: 16/05/2025…”

> *Resumo:* “O DF quer comprar medicamentos contra câncer pra Secretaria de Saúde. Farmacêuticas podem participar. Propostas até 16/05/2025.”

### Caminho técnico

- Baseline extrativo (TextRank) — rápido, resumo meio robótico
- Modelo abstrativo ou LLM com prompt — fica bonito, mas cuidado com **inventar prazo ou valor**
- Avaliar: ROUGE ajuda, mas o que convence a banca é **ler 20 resumos e dar nota**

**Veredicto:** impacto emocional na apresentação é forte. Difícil defender só com número. Boa como extra (“classificamos E resumimos 5 exemplos”).

---

## E aquela ideia de MATERIAL vs SERVIÇO?

Apareceu numa conversa à parte. Não está no brainstorm original, mas vale registrar:

- O CSV **já tem** a coluna `tipo` (320 material, 103 serviço)
- Dá pra treinar rápido, comparar TF-IDF vs BERTimbau, entregar métrica
- **Mas** o ComprasNet já mostra isso — o impacto é menor que classificar por área de gasto

**Uso que faz sentido:** piloto na primeira semana (“validamos que o pipeline funciona”) e depois partir pra Ideia 1 de verdade. Não como tema final sozinho.

---

## Combinações que a gente considerou

| Combo | Faz sentido? |
|---|---|
| **Ideia 1 sozinha** | Sim — foco claro, entregável |
| Ideia 1 + gráfico da Ideia 3 | Sim — classificação + um mapa de similaridade no apêndice |
| Ideia 1 + 5 resumos da Ideia 4 | Sim — se sobrar tempo e alguém curtir prompt/LLM |
| Ideia 4 sozinha | Arriscado — difícil provar qualidade |
| Ideia 2 sozinha | Só se alguém amar anotação |

---

## Como a gente decide (sem reunir 3 horas)

1. Cada um lê este doc (10 min)
2. Vota: **1, 2, 3 ou 4** (pode votar em 2 opções)
3. Se empatar entre 1 e 4 → combina 1 + demo de resumo
4. Anota no [`UNIVERSAL-DEEP-LEARNING-GUIDE.md`](UNIVERSAL-DEEP-LEARNING-GUIDE.md)
5. Divide tarefas e segue

---

## Quando fecharmos, marcar aqui

- [ ] Tema escolhido: Ideia ___
- [ ] Título do projeto definido
- [ ] Entrada do modelo: texto completo ou só objeto?
- [ ] Papéis dos 4 integrantes
- [ ] Registrado no guia universal

---

## Próximo passo concreto

Depois da votação:

1. Atualizar o guia universal (seções 1 e 2)
2. Se for Ideia 1: montar mapeamento órgão → área (`labels_areas.json`)
3. Rodar baseline TF-IDF em `scripts/run_train.py`

---

*Documento vivo — editar quando o grupo decidir ou mudar de ideia.*
