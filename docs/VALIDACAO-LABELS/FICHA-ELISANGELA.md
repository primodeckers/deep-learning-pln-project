# Validação manual de labels — Elisangela Osorio

Revisão humana da qualidade do **label proxy** (órgão → macroárea). Gabarito e instruções: [`VALIDACAO-LABELS.md`](VALIDACAO-LABELS.md).

> **Ficha individual.** Preencha **Concorda?**, **Label humano** e **Observação** na tabela abaixo.

---

## Registro

| Campo | Valor |
|-------|-------|
| **Revisor(a)** | Elisangela Osorio |
| **Data** | 2026-06-21 |
| **Corpus** | `data/processed/licitacoes_corpus.jsonl` |
| **Amostra** | 30 editais · seed 42 |

---

## Tabela (sua revisão)

<!-- AMOSTRA_INICIO -->
> Amostra · seed=42 · 30 editais

| # | `id` | `orgao_csv` | Trecho do `objeto_html` | Label auto | Concorda? | Label humano | Observação |
|---|------|-------------|-------------------------|------------|-----------|--------------|------------|
| 1 | `974002_5_900332025` | EDF - SECRETARIA DE ESTADO DE ECONOMIA DO DF | Objeto: Pregão Eletrônico - Contratação de empresa especializada em serviços de limpeza e higienização de estofados par… | Administracao/Outros | S | | Serviços comuns de limpeza e conservação. |
| 2 | `930686_6_900242025` | EDF-ADMINISTRAÇAO REGIONAL DO CRUZEIRO |  | Administracao/Outros | ? | | Não tem o trecho do objeto. Não é possível definir apenas pelo órgão |
| 3 | `974002_5_900302025` | EDF - SECRETARIA DE ESTADO DE ECONOMIA DO DF | Objeto: Pregão Eletrônico - Registro de preços visando a aquisição de material permanente para recreação infantil, a fi… | Administracao/Outros | N | EDUCACAO | Objeto sugere educação, com alguma insegurança na decisão. |
| 4 | `170394_5_900242025` | CORPO DE BOMBEIROS MILITAR DO DF | Objeto: Pregão Eletrônico - Registro de preços de materiais de consumo utilizados no Atendimento Pré-Hospitalar do CBMD… | Seguranca | N | SAUDE | Objeto fla em material usado em atendimento ligado à saúde.|
| 5 | `930686_6_900262025` | EDF-ADMINISTRAÇAO REGIONAL DO CRUZEIRO |  | Administracao/Outros | ? | | Não tem o trecho do objeto. Não é possível definir apenas pelo órgão. |
| 6 | `926119_5_901092025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de insumo(s) à saúde pertencente(s) ao(s) Grupo: 3601 - ARTIGOS PARA SVS,… | Saude | S | | |
| 7 | `974002_5_900242025` | EDF - SECRETARIA DE ESTADO DE ECONOMIA DO DF | Objeto: Pregão Eletrônico - A fim de atender demanda da Secretaria de Estado da Mulher do Distrito Federal (SMDF) a Sub… | Administracao/Outros | ? | | Não é possível definir pelo trecho da descrição do objeto disponível.|
| 8 | `974200_5_900612025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Serviço de publicação de matéria legal, em jornal de grande circulação nacional. | Saneamento | N | ADMINISTRACAO/OUTROS| Serviço de publicação de matéria se trata de atividades administartivas.|
| 9 | `974200_5_900352025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de tintas e materiais para pintura, na forma do Sistema de Registro de Preços SRP. | Saneamento | N | INFRAESTRUTURA/OBRAS | Objeto sugere obra. Alto grau de indefinição |
| 10 | `926119_5_900302025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de insumos à saúde pertencentes ao Grupo 36.09.09 (FIOS POLIPROPILENO), e… | Saude | S | | |
| 11 | `974200_5_900332025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de motores estacionários para aplicação no sistema de hidrojateamento no processo… | Saneamento | S | | |
| 12 | `170394_5_900312025` | CORPO DE BOMBEIROS MILITAR DO DF | Objeto: Pregão Eletrônico - Aquisição de material de consumo para as atividades clínicas geral da Policlínica Odontológ… | Seguranca | N | SAÚDE | |
| 13 | `926119_5_900482025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de medicamentos pertencentes ao(s) Grupo 09.R.03.B (OUTROS MEDICAMENTOS P… | Saude | S | | |
| 14 | `926119_5_901132025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição de CAPELA DE FLUXO LAMINAR, para atender as necessidades da Secretaria de Estado … | Saude | S | | |
| 15 | `974200_5_900452025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de materiais de fibra de vidro (PRFV), na forma do Sistema de Registro de Preços … | Saneamento | S | | |
| 16 | `926119_5_900602025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de SERINGAS, em sistema de registro de preços, para atender às necessidad… | Saude | S | | |
| 17 | `926119_5_900672025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de medicamento(s) pertencente(s) ao(s) Grupo: 09.S.01.X - OUTROS OFTALMOL… | Saude | S | | |
| 18 | `926119_5_900342025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de material permanente: Seladoras Automáticas e Manuais, em sistema de re… | Saude | S | | |
| 19 | `974200_5_900272025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de Licenças SDWAN para Firewall Check Point, roteadores SDWAN para unidades remot… | Saneamento | N | ADMINISTRACAO/OUTROS | Na falta de um item de Tecnologia, a melhor associaçaõ seria administração/outros.|
| 20 | `926119_5_900702025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de medicamentos, Grupo: 09.N.01.A - ANESTÉSICOS GERAIS e 09.N.05.A - ANTI… | Saude | S | | |
| 21 | `926119_5_900682025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição reg. de med. pert. ao(s) Grupo: 09.A.12.A - CÁLCIO, Grupo: 09.A.09.A - DIGESTIVOS… | Saude | S | | |
| 22 | `170394_5_900432025` | CORPO DE BOMBEIROS MILITAR DO DF | Objeto: Pregão Eletrônico - Contratação de empresa para prestação de serviços contínuos de LAVANDERIA HOSPITALAR (colet… | Seguranca | N | SAUDE | Objeto para em lavanderia hospitalar.|
| 23 | `170394_6_900232025` | CORPO DE BOMBEIROS MILITAR DO DF |  | Seguranca | ? | | Sem trecho do objeto disponíve.|
| 24 | `926119_5_900732025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de insumo(s) à saúde pertencente(s) ao(s) Grupo 36.05.06 (FILTROS), em si… | Saude | S | | |
| 25 | `974200_5_900592025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de hidróxido de sódio 50% em contêiner, na forma do Sistema de Registro de Preços… | Saneamento | S | | |
| 26 | `930686_6_900272025` | EDF-ADMINISTRAÇAO REGIONAL DO CRUZEIRO |  | Administracao/Outros | ? | | Sem trecho do objeto disponível|
| 27 | `926119_5_900882025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de insumo(s) à saúde pertencente(s) ao(s) Grupo: 10.01 - BROCAS ODONTOLÓG… | Saude | S | | |
| 28 | `974200_5_900252025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição, remanejamento, montagem e desmontagem de paredes divisórias, na forma do Sistema… | Saneamento | N | ADMINISTRACAO/OUTROS| Objeto fala em alteração de divisórias, atividades de manutenção de ambiente|
| 29 | `974200_5_900292025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Serviços para Licenças de Software, Suporte Técnico e Garantia por 36 meses para Firewalls … | Saneamento | N | ADMINISTRACAO/OUTROS |Na falta de um item de Tecnologia, a melhor associaçaõ seria administração/outros. |
| 30 | `974003_6_900262025` | TRIBUNAL DE CONTAS DO DISTRITO FEDERAL |  | Administracao/Outros | ? | | Não há o trecho do objeto disponível |

<!-- AMOSTRA_FIM -->

---

## Resumo (preencher após revisão)

| Métrica | Valor |
|---------|-------|
| Total revisado | 30/30 |
| Concordância (`S`) | 15 |
| Discordância (`N`) | 9 |
| Ambíguos (`?`) | 6 |
| **Taxa de concordância** | 62,5% (15/24) ingnorando ? |

### Conclusão (1 parágrafo)

Observa-se que há muitos registros cujas classificações se dão apenas pelo órgão, ignorando-se o objeto, como, por exemplo, as compras de materiais associados à saúde pelo Corpo de Bombeiros, que são classificados como segurança e não como saúde. Além disso, muitos objetos estão sem o trecho disponível, tornando-se difícil afirmar a qual área pertence a contratação.

---

## Referências

- [`FASE1-CLASSIFICACAO.md`](../FASE1-CLASSIFICACAO.md) · [`METRICAS-E-DECISOES.md`](../METRICAS-E-DECISOES.md)
