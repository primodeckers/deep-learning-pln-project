# Validação manual de labels — Alexandre Hugo

Revisão humana da qualidade do **label proxy** (órgão → macroárea).
Gabarito e instruções: [`validacao_labels.md`](validacao_labels.md).

> **Ficha individual.** Preencha **Concorda?**, **Label humano** e **Observação** na tabela abaixo.

---

## Registro

| Campo          | Valor                                    |
| -------------- | ---------------------------------------- |
| **Revisor(a)** | Alexandre Hugo                           |
| **Data**       | 2026-06-19                               |
| **Corpus**     | `data/processed/licitacoes_corpus.jsonl` |
| **Amostra**    | 30 editais · seed 42                     |

---

## Tabela (sua revisão)

> Amostra · seed=42 · 30 editais

| #  | `id`                 | `orgao_csv`                                   | Trecho do `objeto_html`                                                                                                  | Label auto           | Concorda? | Label humano         | Observação                                                                                                                                            |
| -- | -------------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | -------------------- | --------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1  | `974002_5_900332025` | EDF - SECRETARIA DE ESTADO DE ECONOMIA DO DF  | Objeto: Pregão Eletrônico - Contratação de empresa especializada em serviços de limpeza e higienização de estofados par… | Administracao/Outros | S         |                      | Serviço-meio administrativo.                                                                                                                          |
| 2  | `930686_6_900242025` | EDF-ADMINISTRAÇAO REGIONAL DO CRUZEIRO        |                                                                                                                          | Administracao/Outros | ?         |                      | Órgão administrativo regional, sem indício claro de macroárea setorial específica; pode haver relação indireta com educação, segurança ou outra área. |
| 3  | `974002_5_900302025` | EDF - SECRETARIA DE ESTADO DE ECONOMIA DO DF  | Objeto: Pregão Eletrônico - Registro de preços visando a aquisição de material permanente para recreação infantil, a fi… | Administracao/Outros | ?         |                      | Objeto ligado à recreação infantil; pode tangenciar Educação ou Assistência, embora o órgão seja Economia.                                            |
| 4  | `170394_5_900242025` | CORPO DE BOMBEIROS MILITAR DO DF              | Objeto: Pregão Eletrônico - Registro de preços de materiais de consumo utilizados no Atendimento Pré-Hospitalar do CBMD… | Seguranca            | N         | Saude                | Atendimento pré-hospitalar aproxima o gasto de Saúde.                                                                                                 |
| 5  | `930686_6_900262025` | EDF-ADMINISTRAÇAO REGIONAL DO CRUZEIRO        |                                                                                                                          | Administracao/Outros | S         |                      | Administração regional sem objeto que justifique reclassificação.                                                                                     |
| 6  | `926119_5_901092025` | SECRETARIA DE ESTADO DE SAÚDE - DF            | Objeto: Pregão Eletrônico - Aquisição regular de insumo(s) à saúde pertencente(s) ao(s) Grupo: 3601 - ARTIGOS PARA SVS,… | Saude                | S         |                      | Insumos de saúde.                                                                                                                                     |
| 7  | `974002_5_900242025` | EDF - SECRETARIA DE ESTADO DE ECONOMIA DO DF  | Objeto: Pregão Eletrônico - A fim de atender demanda da Secretaria de Estado da Mulher do Distrito Federal (SMDF) a Sub… | Administracao/Outros | S         |                      | Apesar de atender outro órgão, o proxy administrativo é aceitável como baseline.                                                                      |
| 8  | `974200_5_900612025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Serviço de publicação de matéria legal, em jornal de grande circulação nacional.             | Saneamento           | ?         |                      | Pode ser serviço-meio ou ação de suporte vinculada à atividade da CAESB.                                                                              |
| 9  | `974200_5_900352025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de tintas e materiais para pintura, na forma do Sistema de Registro de Preços SRP. | Saneamento           | ?         |                      | Pode ser insumo de atividade-meio ou material necessário à operação da companhia.                                                                     |
| 10 | `926119_5_900302025` | SECRETARIA DE ESTADO DE SAÚDE - DF            | Objeto: Pregão Eletrônico - Aquisição regular de insumos à saúde pertencentes ao Grupo 36.09.09 (FIOS POLIPROPILENO), e… | Saude                | S         |                      | Insumo médico-hospitalar.                                                                                                                             |
| 11 | `974200_5_900332025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de motores estacionários para aplicação no sistema de hidrojateamento no processo… | Saneamento           | S         |                      | Equipamento aplicado à operação de saneamento.                                                                                                        |
| 12 | `170394_5_900312025` | CORPO DE BOMBEIROS MILITAR DO DF              | Objeto: Pregão Eletrônico - Aquisição de material de consumo para as atividades clínicas geral da Policlínica Odontológ… | Seguranca            | N         | Saude                | Atividade clínica odontológica sugere Saúde; o proxy por órgão puxou para Segurança.                                                                  |
| 13 | `926119_5_900482025` | SECRETARIA DE ESTADO DE SAÚDE - DF            | Objeto: Pregão Eletrônico - Aquisição regular de medicamentos pertencentes ao(s) Grupo 09.R.03.B (OUTROS MEDICAMENTOS P… | Saude                | S         |                      | Medicamentos.                                                                                                                                         |
| 14 | `926119_5_901132025` | SECRETARIA DE ESTADO DE SAÚDE - DF            | Objeto: Pregão Eletrônico - Aquisição de CAPELA DE FLUXO LAMINAR, para atender as necessidades da Secretaria de Estado … | Saude                | S         |                      | Equipamento de laboratório/saúde.                                                                                                                     |
| 15 | `974200_5_900452025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de materiais de fibra de vidro (PRFV), na forma do Sistema de Registro de Preços … | Saneamento           | S         |                      | Material relacionado à infraestrutura de saneamento.                                                                                                  |
| 16 | `926119_5_900602025` | SECRETARIA DE ESTADO DE SAÚDE - DF            | Objeto: Pregão Eletrônico - Aquisição regular de SERINGAS, em sistema de registro de preços, para atender às necessidad… | Saude                | S         |                      | Insumo de saúde.                                                                                                                                      |
| 17 | `926119_5_900672025` | SECRETARIA DE ESTADO DE SAÚDE - DF            | Objeto: Pregão Eletrônico - Aquisição regular de medicamento(s) pertencente(s) ao(s) Grupo: 09.S.01.X - OUTROS OFTALMOL… | Saude                | S         |                      | Medicamentos oftalmológicos.                                                                                                                          |
| 18 | `926119_5_900342025` | SECRETARIA DE ESTADO DE SAÚDE - DF            | Objeto: Pregão Eletrônico - Aquisição regular de material permanente: Seladoras Automáticas e Manuais, em sistema de re… | Saude                | S         |                      | Equipamento/instrumental de saúde.                                                                                                                    |
| 19 | `974200_5_900272025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de Licenças SDWAN para Firewall Check Point, roteadores SDWAN para unidades remot… | Saneamento           | S         |                      | Tecnologia aplicada à operação de companhia de saneamento.                                                                                            |
| 20 | `926119_5_900702025` | SECRETARIA DE ESTADO DE SAÚDE - DF            | Objeto: Pregão Eletrônico - Aquisição regular de medicamentos, Grupo: 09.N.01.A - ANESTÉSICOS GERAIS e 09.N.05.A - ANTI… | Saude                | S         |                      | Medicamentos.                                                                                                                                         |
| 21 | `926119_5_900682025` | SECRETARIA DE ESTADO DE SAÚDE - DF            | Objeto: Pregão Eletrônico - Aquisição reg. de med. pert. ao(s) Grupo: 09.A.12.A - CÁLCIO, Grupo: 09.A.09.A - DIGESTIVOS… | Saude                | S         |                      | Medicamentos/insumos de saúde.                                                                                                                        |
| 22 | `170394_5_900432025` | CORPO DE BOMBEIROS MILITAR DO DF              | Objeto: Pregão Eletrônico - Contratação de empresa para prestação de serviços contínuos de LAVANDERIA HOSPITALAR (colet… | Seguranca            | N         | Saude                | Lavanderia hospitalar aproxima o gasto de Saúde, embora vinculada ao Corpo de Bombeiros.                                                              |
| 23 | `170394_6_900232025` | CORPO DE BOMBEIROS MILITAR DO DF              |                                                                                                                          | Seguranca            | ?         |                      | Sem elemento textual suficiente para afastar ou confirmar o proxy por órgão.                                                                          |
| 24 | `926119_5_900732025` | SECRETARIA DE ESTADO DE SAÚDE - DF            | Objeto: Pregão Eletrônico - Aquisição regular de insumo(s) à saúde pertencente(s) ao(s) Grupo 36.05.06 (FILTROS), em si… | Saude                | S         |                      | Insumos de saúde.                                                                                                                                     |
| 25 | `974200_5_900592025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de hidróxido de sódio 50% em contêiner, na forma do Sistema de Registro de Preços… | Saneamento           | S         |                      | Insumo químico típico de operação de saneamento.                                                                                                      |
| 26 | `930686_6_900272025` | EDF-ADMINISTRAÇAO REGIONAL DO CRUZEIRO        |                                                                                                                          | Administracao/Outros | ?         |                      | Administração regional, mas sem contexto suficiente no objeto para validar a macroárea com segurança.                                                 |
| 27 | `926119_5_900882025` | SECRETARIA DE ESTADO DE SAÚDE - DF            | Objeto: Pregão Eletrônico - Aquisição regular de insumo(s) à saúde pertencente(s) ao(s) Grupo: 10.01 - BROCAS ODONTOLÓG… | Saude                | S         |                      | Insumo odontológico de saúde.                                                                                                                         |
| 28 | `974200_5_900252025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição, remanejamento, montagem e desmontagem de paredes divisórias, na forma do Sistema… | Saneamento           | N         | Administracao/Outros | Gasto de suporte administrativo, embora realizado dentro da companhia de saneamento.                                                                  |
| 29 | `974200_5_900292025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Serviços para Licenças de Software, Suporte Técnico e Garantia por 36 meses para Firewalls … | Saneamento           | ?         |                      | Pode ser serviço de TI de suporte, mas também pode estar ligado à atividade-fim da companhia.                                                         |
| 30 | `974003_6_900262025` | TRIBUNAL DE CONTAS DO DISTRITO FEDERAL        |                                                                                                                          | Administracao/Outros | N         | Saude                | Objeto envolve insumos odontológicos; o proxy por órgão caiu em Administração/Outros, mas a área de gasto parece Saúde.                               |

---

## Resumo (preencher após revisão)

| Métrica | Valor |
|---------|-------|
| Total revisado | 30/30 |
| Concordância (`S`) | 18 |
| Discordância (`N`) | 5 |
| Ambíguos (`?`) | 7 |
| Taxa de concordância bruta | 60,0% (18/30) |
| Taxa de concordância líquida* | 78,3% (18/23) |
| Taxa de discordância líquida* | 21,7% (5/23) |
| Taxa de ambiguidade | 23,3% (7/30) |

\* Cálculo líquido desconsidera os casos ambíguos (`?`).

### Conclusão (1 parágrafo)

A validação manual indica que o label proxy órgão → macroárea pode ser utilizado como baseline inicial, mas com limitações mais relevantes do que o estimado anteriormente. Nesta revisão, houve 18 concordâncias (`S`), 5 discordâncias (`N`) e 7 casos ambíguos (`?`), o que resulta em taxa de concordância líquida de 78,3% ao desconsiderar os casos ambíguos. As divergências e ambiguidades concentram-se sobretudo em editais ligados a atividades de saúde executadas por órgãos de segurança, em compras de suporte ou tecnologia associadas à CAESB e em casos de administração regional sem contexto suficiente no objeto. Assim, o mapeamento por órgão se mostra útil como estratégia de rotulagem fraca na Fase 1, mas ainda exige refinamento com revisão humana, regras complementares baseadas no objeto do edital e eventual recategorização manual de casos sensíveis.

---

## Referências

* [`FASE1-CLASSIFICACAO.md`](../FASE1-CLASSIFICACAO.md)
* [`metricas_e_decisoes.md`](../metricas_e_decisoes.md)
