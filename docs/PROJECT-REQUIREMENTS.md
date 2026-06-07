# Projeto Final da Disciplina – Deep Learning e PLN

O Projeto Final da Disciplina corresponde a **60% da nota total** e tem como objetivo aplicar, de forma prática e analítica, os conceitos estudados ao longo do curso. A proposta é que cada estudante ou grupo desenvolva uma solução baseada em Deep Learning ou Processamento de Linguagem Natural, articulando pesquisa científica, coleta ou uso de dados reais, implementação de modelos, avaliação de resultados e reflexão crítica sobre impacto, limitações e uso responsável da IA.

A disciplina adota uma abordagem de **Project Based Learning** — aprendizagem baseada em projetos. Portanto, o projeto final será o principal espaço de integração entre teoria, prática, experimentação computacional e análise aplicada.

---

## Objetivo da Atividade

O projeto final deve demonstrar que o grupo é capaz de:

- identificar um problema real que possa ser tratado com PLN;
- fundamentar o problema com literatura científica adequada;
- coletar, organizar ou utilizar dados de forma reprodutível;
- implementar modelos de aprendizagem profunda ou PLN;
- avaliar o desempenho do modelo com métricas apropriadas;
- interpretar os resultados de forma crítica;
- comunicar os achados de maneira clara, objetiva e tecnicamente consistente.

---

## Nossa Modalidade – PLN no Setor Público

| | |
|---|---|
| **Formato** | Grupo de 4 pessoas |
| **Base disciplinar** | Modalidade 2 (dupla ou trio) — PLN no Setor Público |

Esta modalidade tem como objetivo aplicar técnicas de Processamento de Linguagem Natural a dados textuais coletados pelos próprios estudantes, preferencialmente em problemas relacionados ao setor público.

- **Tarefa:** realizar a coleta de dados textuais por meio de scraping, APIs ou outras fontes públicas.
- **Métodos esperados:** aplicar modelos de análise de sentimento, classificação textual, extração de entidades, sumarização, embeddings, Transformers ou outros algoritmos de PLN apresentados durante o curso.
- **Restrição:** é estritamente proibido o uso de bases prontas ou plataformas como Kaggle. Os dados devem ser inéditos e coletados pelo próprio grupo.
- **Foco aplicado:** o trabalho deve buscar responder a um problema real, preferencialmente conectado à administração pública, políticas públicas, serviços públicos, justiça, ouvidorias, comunicação governamental ou transparência.

---

## Exemplos de Projetos

1. **Análise de sentimento de notícias sobre políticas públicas** — coletar manchetes e textos de portais de notícias sobre determinada política pública e classificar o tom da cobertura como positivo, negativo ou neutro.

2. **Extração de entidades em processos judiciais** — desenvolver um modelo para identificar automaticamente informações em decisões ou petições públicas, como valores, varas, citações legais ou tipos de demanda.

3. **Categorização automática de demandas em ouvidorias** — coletar reclamações de cidadãos e treinar um classificador para direcionar automaticamente as demandas para setores como iluminação pública, saneamento, transporte, saúde ou educação.

4. **Sumarização de projetos de lei ou diários oficiais** — utilizar modelos de linguagem para gerar resumos curtos, acessíveis e compreensíveis para a população.

5. **Análise de discursos, audiências ou consultas públicas** — aplicar PLN para identificar temas recorrentes, polarização, demandas sociais ou mudanças de opinião ao longo do tempo.

---

## Entregáveis

### 1. Repositório no GitHub

Link para repositório público contendo:

- scripts de coleta, pré-processamento, análise e estimações de PLN;
- todos os arquivos de código necessários para reproduzir o projeto.

### 2. Descrição da coleta

O grupo deve explicar claramente:

- de onde os dados foram coletados;
- qual período foi analisado;
- quais filtros foram utilizados;
- quais limitações existem na base.

### 3. Acesso aos dados

- Sempre que possível, os dados devem estar disponíveis no repositório ou acessíveis via código.
- Caso a coleta gere grande volume de dados, o grupo deverá conversar previamente com o professor para definir uma solução adequada.

### 4. Apresentação em PDF

Arquivo contendo os slides apresentados em sala, com síntese da coleta, metodologia de PLN, resultados, métricas e principais insights do caso prático explorado.

---

## Critérios Obrigatórios de Referências

Para garantir rigor científico e embasamento metodológico, o trabalho deverá conter uma seção de referências bibliográficas com, no mínimo:

| Tipo | Quantidade mínima |
|---|---|
| Artigos sobre o **tema ou domínio de aplicação** do projeto | 5 |
| Artigos sobre a **técnica de modelagem** utilizada (redes neurais, CNNs, RNNs, LSTMs, Transformers, embeddings, análise de sentimento, classificação textual, extração de entidades, sumarização, etc.) | 5 |

As referências devem ser utilizadas de forma **substantiva** no trabalho — não basta listar artigos ao final. Elas devem apoiar:

- a definição do problema;
- a escolha metodológica;
- a interpretação dos resultados;
- a discussão das limitações.

---

## Estrutura Recomendada do Trabalho

| Seção | Conteúdo esperado |
|---|---|
| **Título do projeto** | Claro, objetivo e alinhado ao problema investigado |
| **Integrantes** | Nome dos estudantes e modalidade escolhida |
| **Contexto e problema** | Descrição do problema real a ser resolvido ou investigado |
| **Justificativa** | Relevância científica, técnica ou aplicada do tema |
| **Referencial teórico** | Discussão dos artigos relacionados ao domínio do problema e à técnica utilizada |
| **Dados** | Descrição do dataset, fonte, forma de coleta, período, variáveis, volume de dados e limitações |
| **Metodologia** | Pré-processamento, arquitetura do modelo, parâmetros principais, estratégia de treino, validação e teste |
| **Resultados** | Métricas, tabelas, gráficos, comparações e principais achados |
| **Discussão** | Interpretação crítica dos resultados, limitações, riscos, possíveis vieses e implicações práticas |
| **Conclusão** | Síntese dos aprendizados e indicação de próximos passos |
| **Referências** | Artigos, livros, documentos técnicos e fontes utilizadas |
| **Apêndice técnico** *(se necessário)* | Instruções de execução, detalhes adicionais do código ou documentação do repositório |

---

## Apresentação Final em Sala

A apresentação final é **obrigatória** e ocorrerá no último dia de aula.

| Item | Detalhe |
|---|---|
| **Duração** | Até 10 minutos por projeto |
| **Formato** | Apresentação oral com apoio de slides em PDF |
| **Foco** | Clareza, objetividade e capacidade de resumir o projeto dentro do tempo |
| **Entrega** | Repositório público no GitHub, dados acessíveis via código e slides em PDF finalizados até o momento da apresentação |

### Estrutura sugerida para os slides

1. **Contexto** — qual problema real está sendo resolvido?
2. **Base teórica** — quais artigos sustentam o projeto?
3. **Dados** — como os dados foram obtidos, coletados ou selecionados?
4. **Metodologia** — qual arquitetura de Deep Learning ou modelo de PLN foi aplicado?
5. **Resultados** — quais foram as principais métricas e achados?
6. **Discussão** — o modelo resolveu o problema? Quais foram os limites?
7. **Conclusão** — qual é a principal contribuição do projeto?
8. **Próximos passos** — como o projeto poderia ser aprimorado ou aplicado em escala?

---

## O Diferencial: Ir Além da Técnica

Um modelo de Deep Learning ou PLN não deve ser tratado como um fim em si mesmo. Ele deve ser usado como ferramenta para compreender, explicar ou resolver problemas reais. Por isso, projetos que forem além da simples aplicação da técnica serão especialmente valorizados.

O diferencial do trabalho estará na capacidade de cruzar os resultados do modelo com o mundo real, gerando insights práticos, interpretações relevantes, correlações substantivas ou propostas de impacto.

**Exemplos aplicáveis à nossa modalidade:**

- Se o grupo fizer **análise de sentimento de notícias políticas**, pode cruzar os resultados com pesquisas de opinião, eventos públicos ou decisões governamentais.
- Se o grupo **categorizar reclamações de cidadãos**, pode cruzar os dados com informações geográficas para identificar onde o poder público deveria alocar mais recursos.

---

## Critérios de Avaliação

| Critério | O que será avaliado |
|---|---|
| **Clareza do problema** | Definição objetiva do problema real investigado |
| **Fundamentação científica** | Uso adequado dos artigos obrigatórios e relação entre literatura, problema e metodologia |
| **Qualidade dos dados** | Adequação da fonte, transparência da coleta, organização e reprodutibilidade |
| **Implementação técnica** | Coerência do modelo escolhido, qualidade do código, documentação e execução |
| **Avaliação do modelo** | Uso de métricas apropriadas e interpretação correta dos resultados |
| **Análise crítica** | Discussão de limitações, vieses, riscos, erros e possibilidades de melhoria |
| **Reprodutibilidade** | Repositório organizado, dados acessíveis e instruções claras para execução |
| **Comunicação** | Apresentação clara, objetiva, visualmente organizada e dentro do tempo |
| **Impacto aplicado** | Capacidade de conectar os resultados do modelo a problemas reais e gerar insights relevantes |

---

## Boas Práticas

- Escolha um problema factível e bem delimitado.
- Evite projetos excessivamente amplos ou impossíveis de concluir no prazo da disciplina.
- Documente todas as etapas do projeto no GitHub.
- Explique como instalar dependências e executar o notebook ou scripts.
- Use nomes claros para arquivos, pastas e notebooks.
- Registre decisões de modelagem, parâmetros testados e limitações encontradas.
- Compare modelos quando fizer sentido.
- Inclua tabelas, gráficos e métricas para apoiar os resultados.
- Não esconda resultados negativos: erros e limitações fazem parte do aprendizado científico.
- Valorize a interpretação dos resultados, não apenas a execução do código.

---

## Considerações Finais

O Projeto Final é o momento de demonstrar maturidade técnica, rigor científico e capacidade de aplicação prática. A expectativa é que cada trabalho evidencie não apenas a implementação de um modelo, mas também a compreensão crítica de seus resultados, limites e possibilidades de uso em problemas reais.

Um bom projeto não é apenas aquele que apresenta a melhor métrica, mas aquele que explica **o que a métrica significa**, **por que ela importa** e **como ela pode gerar valor** para a sociedade, para a pesquisa ou para o setor público.
