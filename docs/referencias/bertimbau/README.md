Referências sobre BERTimbau

Esta pasta reúne artigos científicos utilizados como base teórica para o projeto de PLN aplicado à sumarização de editais públicos em linguagem cidadã.

O objetivo dessas referências é fundamentar o uso de modelos Transformer em português, especialmente o BERTimbau, em tarefas de compreensão semântica, segmentação textual, tokenização, pré-treinamento e representação de textos em português brasileiro.

Artigos incluídos

1. Segmentação Textual Baseada em Tópicos em Português Utilizando BERTimbau

Este artigo é relevante para o projeto porque discute o uso do BERTimbau em segmentação textual baseada em tópicos. Essa técnica pode ser útil para dividir editais longos em blocos temáticos, como objeto da contratação, critérios de participação, prazos, documentação exigida, julgamento das propostas e penalidades.

No projeto de sumarização de editais em linguagem cidadã, a segmentação textual pode ser usada como etapa intermediária antes da geração do resumo final, permitindo que o sistema identifique quais partes do edital são mais relevantes para o cidadão comum ou para pequenas empresas interessadas em participar da licitação.

Arquivo local:

segmentacao-textual-topicos-portugues-bertimbau.pdf

2. BERT models for Brazilian Portuguese: pretraining, evaluation and tokenization analysis

Este artigo é uma referência central sobre o BERTimbau, pois apresenta modelos BERT treinados para o português brasileiro, discute o processo de pré-treinamento, avalia o desempenho em tarefas de PLN e analisa aspectos de tokenização.

A referência é importante para justificar o uso de modelos Transformer especializados em português, em vez de utilizar apenas modelos multilíngues genéricos. No projeto, esse artigo apoia a escolha de modelos como BERTimbau para representar semanticamente trechos de editais públicos em português brasileiro.

Arquivo local:

bert-models-brazilian-portuguese-pretraining-evaluation-tokenization.pdf

Relação com o projeto

No projeto final, o BERTimbau poderá ser utilizado como modelo de apoio para:

- geração de embeddings de trechos dos editais;
- classificação de seções do edital;
- identificação de trechos relevantes;
- segmentação textual por tópicos;
- seleção de partes importantes antes da sumarização;
- comparação com modelos generativos, como T5, PTT5, mT5 ou LLMs.

Como o BERTimbau é um modelo do tipo encoder-only, ele não é a melhor opção para gerar diretamente o resumo final. Entretanto, é útil para compreender e classificar.
