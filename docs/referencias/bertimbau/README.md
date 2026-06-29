Referências sobre BERTimbau

Esta pasta reúne artigos científicos utilizados como base teórica para o projeto de PLN aplicado à **classificação de editais públicos** por área de gasto.

O objetivo dessas referências é fundamentar o uso de modelos Transformer em português, especialmente o BERTimbau, em tarefas de compreensão semântica, segmentação textual, tokenização, pré-treinamento e representação de textos em português brasileiro.

Artigos incluídos

1. Segmentação Textual Baseada em Tópicos em Português Utilizando BERTimbau

Este artigo discute o uso do BERTimbau em segmentação textual baseada em tópicos. Essa técnica pode ser útil para dividir editais longos em blocos temáticos (objeto, prazos, julgamento), como etapa opcional de pré-processamento antes da classificação.

Arquivo local:

segmentacao-textual-topicos-portugues-bertimbau.pdf

2. BERT models for Brazilian Portuguese: pretraining, evaluation and tokenization analysis

Referência central sobre o BERTimbau: pré-treinamento, avaliação em tarefas de PLN e análise de tokenização. Justifica o uso de modelos especializados em português brasileiro em vez de multilíngues genéricos — base da Fase 2 (fine-tuning para classificação).

Arquivo local:

bert-models-brazilian-portuguese-pretraining-evaluation-tokenization.pdf

Relação com o projeto

No projeto, o BERTimbau é usado para **classificação textual** (Fase 2), comparado ao baseline TF-IDF + LogReg e ao SVM linear sobre o mesmo split.
