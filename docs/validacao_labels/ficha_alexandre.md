# Validação manual de labels — Alexandre Ferreira Ponte

Revisão humana da qualidade do **label proxy** (órgão → macroárea). Gabarito e instruções: [`validacao_labels.md`](validacao_labels.md).

> **Ficha individual.** Preencha **Concorda?**, **Label humano** e **Observação** na tabela abaixo.

---

## Registro

| Campo | Valor |
|-------|-------|
| **Revisor(a)** | Alexandre Ferreira Ponte |
| **Data** | 2026-06-22 |
| **Corpus** | `data/processed/licitacoes_corpus.jsonl` |
| **Amostra** | 30 editais · seed 42 |

---

## Tabela (sua revisão)

<!-- AMOSTRA_INICIO -->
> Amostra · seed=42 · 30 editais

| # | `id` | `orgao_csv` | Trecho do `objeto_html` | Label auto | Concorda? | Label humano | Observação |
|---|------|-------------|-------------------------|------------|-----------|--------------|------------|
| 1 | `974002_5_900332025` | EDF - SECRETARIA DE ESTADO DE ECONOMIA DO DF | Objeto: Pregão Eletrônico - Contratação de empresa especializada em serviços de limpeza e higienização de estofados par… | Administracao/Outros | S | | Serviço de limpeza; órgão central administrativo, sem setor finalístico no objeto. |
| 2 | `930686_6_900242025` | EDF-ADMINISTRAÇAO REGIONAL DO CRUZEIRO |  | Administracao/Outros | S | | Objeto ausente no recorte; label por órgão (administração regional). |
| 3 | `974002_5_900302025` | EDF - SECRETARIA DE ESTADO DE ECONOMIA DO DF | Objeto: Pregão Eletrônico - Registro de preços visando a aquisição de material permanente para recreação infantil, a fi… | Administracao/Outros | ? | | Objeto sugere finalidade educacional/social (recreação infantil); compra centralizada da SEFAZ/Economia → cai em Administração. |
| 4 | `170394_5_900242025` | CORPO DE BOMBEIROS MILITAR DO DF | Objeto: Pregão Eletrônico - Registro de preços de materiais de consumo utilizados no Atendimento Pré-Hospitalar do CBMD… | Seguranca | ? | | Insumos de saúde (APH); é atividade-fim do CBMDF → fronteira Saúde/Segurança. |
| 5 | `930686_6_900262025` | EDF-ADMINISTRAÇAO REGIONAL DO CRUZEIRO |  | Administracao/Outros | S | | Objeto ausente no recorte; label por órgão (administração regional). |
| 6 | `926119_5_901092025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de insumo(s) à saúde pertencente(s) ao(s) Grupo: 3601 - ARTIGOS PARA SVS,… | Saude | S | | |
| 7 | `974002_5_900242025` | EDF - SECRETARIA DE ESTADO DE ECONOMIA DO DF | Objeto: Pregão Eletrônico - A fim de atender demanda da Secretaria de Estado da Mulher do Distrito Federal (SMDF) a Sub… | Administracao/Outros | S | | Compra centralizada para a Sec. da Mulher; sem classe Social, Administração/Outros é o balde correto. |
| 8 | `974200_5_900612025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Serviço de publicação de matéria legal, em jornal de grande circulação nacional. | Saneamento | ? | | Serviço administrativo/jurídico (publicação legal), não saneamento; órgão é do setor saneamento. |
| 9 | `974200_5_900352025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de tintas e materiais para pintura, na forma do Sistema de Registro de Preços SRP. | Saneamento | S | | Insumo operacional da CAESB. |
| 10 | `926119_5_900302025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de insumos à saúde pertencentes ao Grupo 36.09.09 (FIOS POLIPROPILENO), e… | Saude | S | | |
| 11 | `974200_5_900332025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de motores estacionários para aplicação no sistema de hidrojateamento no processo… | Saneamento | S | | Atividade-fim (hidrojateamento da rede). |
| 12 | `170394_5_900312025` | CORPO DE BOMBEIROS MILITAR DO DF | Objeto: Pregão Eletrônico - Aquisição de material de consumo para as atividades clínicas geral da Policlínica Odontológ… | Seguranca | ? | | Insumos odontológicos da policlínica do CBMDF → fronteira Saúde/Segurança. |
| 13 | `926119_5_900482025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de medicamentos pertencentes ao(s) Grupo 09.R.03.B (OUTROS MEDICAMENTOS P… | Saude | S | | |
| 14 | `926119_5_901132025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição de CAPELA DE FLUXO LAMINAR, para atender as necessidades da Secretaria de Estado … | Saude | S | | Equipamento laboratorial/saúde. |
| 15 | `974200_5_900452025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de materiais de fibra de vidro (PRFV), na forma do Sistema de Registro de Preços … | Saneamento | S | | |
| 16 | `926119_5_900602025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de SERINGAS, em sistema de registro de preços, para atender às necessidad… | Saude | S | | |
| 17 | `926119_5_900672025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de medicamento(s) pertencente(s) ao(s) Grupo: 09.S.01.X - OUTROS OFTALMOL… | Saude | S | | |
| 18 | `926119_5_900342025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de material permanente: Seladoras Automáticas e Manuais, em sistema de re… | Saude | S | | Equipamento de saúde. |
| 19 | `974200_5_900272025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de Licenças SDWAN para Firewall Check Point, roteadores SDWAN para unidades remot… | Saneamento | ? | | TI/infraestrutura de rede (SDWAN/firewall); objeto não é saneamento. |
| 20 | `926119_5_900702025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de medicamentos, Grupo: 09.N.01.A - ANESTÉSICOS GERAIS e 09.N.05.A - ANTI… | Saude | S | | |
| 21 | `926119_5_900682025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição reg. de med. pert. ao(s) Grupo: 09.A.12.A - CÁLCIO, Grupo: 09.A.09.A - DIGESTIVOS… | Saude | S | | |
| 22 | `170394_5_900432025` | CORPO DE BOMBEIROS MILITAR DO DF | Objeto: Pregão Eletrônico - Contratação de empresa para prestação de serviços contínuos de LAVANDERIA HOSPITALAR (colet… | Seguranca | ? | | Serviço hospitalar (lavanderia) vinculado à policlínica do CBMDF → fronteira Saúde/Segurança. |
| 23 | `170394_6_900232025` | CORPO DE BOMBEIROS MILITAR DO DF |  | Seguranca | S | | Objeto ausente no recorte; label por órgão (CBMDF). |
| 24 | `926119_5_900732025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de insumo(s) à saúde pertencente(s) ao(s) Grupo 36.05.06 (FILTROS), em si… | Saude | S | | |
| 25 | `974200_5_900592025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de hidróxido de sódio 50% em contêiner, na forma do Sistema de Registro de Preços… | Saneamento | S | | Insumo de tratamento de água. |
| 26 | `930686_6_900272025` | EDF-ADMINISTRAÇAO REGIONAL DO CRUZEIRO |  | Administracao/Outros | S | | Objeto ausente no recorte; label por órgão (administração regional). |
| 27 | `926119_5_900882025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de insumo(s) à saúde pertencente(s) ao(s) Grupo: 10.01 - BROCAS ODONTOLÓG… | Saude | S | | |
| 28 | `974200_5_900252025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição, remanejamento, montagem e desmontagem de paredes divisórias, na forma do Sistema… | Saneamento | S | | Item predial/operacional da CAESB; aceitável pelo órgão. |
| 29 | `974200_5_900292025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Serviços para Licenças de Software, Suporte Técnico e Garantia por 36 meses para Firewalls … | Saneamento | ? | | TI (licenças de software/firewall); idem #19, objeto não é saneamento. |
| 30 | `974003_6_900262025` | TRIBUNAL DE CONTAS DO DISTRITO FEDERAL |  | Administracao/Outros | N | Saude | Objeto (CSV/JSONL): insumos odontológicos da divisão de saúde do TCDF → a área de gasto é Saúde; o proxy por órgão caiu em Administração/Outros. |

<!-- AMOSTRA_FIM -->

---

## Resumo (preencher após revisão)

| Métrica | Valor |
|---------|-------|
| Total revisado | 30/30 |
| Concordância (`S`) | 22 |
| Discordância (`N`) | 1 |
| Ambíguos (`?`) | 7 |
| **Taxa de concordância** | **95,7%** (22/23, ignorando `?`) · 73,3% (22/30) se contar `?` como não-concordância |

### Conclusão (1 parágrafo)

A validação da amostra demonstrou a eficácia geral da categorização básica do mapeamento entre órgão e macroárea, com a confirmação de vinte e dois objetos alinhados à atividade-fim das respectivas instituições e apenas uma atribuição incorreta para o setor — o Tribunal de Contas do DF (TCDF), cujos insumos odontológicos foram classificados como "Administração/Outros" em vez de "Saúde". Contudo, constatou-se também uma vulnerabilidade no label proxy relacionada à perda de especificidade em aquisições transversais, evidenciada por sete casos ambíguos, que representam aproximadamente 23% da amostra. Entre essas ambiguidades, destacam-se a classificação de tecnologia da informação e serviços administrativos da CAESB como "Saneamento"; a categorização de insumos e serviços médicos do CBMDF como "Segurança"; e a inclusão de compras centralizadas da SEFAZ, com finalidade educacional, na rubrica "Administração/Outros". Diante disso, corrobora-se a limitação previamente documentada: o rótulo reflete a missão institucional do órgão, mas não isola com precisão a finalidade específica da despesa. Consequentemente, a existência de estruturas internas de saúde em órgãos de segurança ou a aquisição de tecnologia por empresas estatais resultam em classificações tecnicamente justificáveis, porém pouco granulares em relação ao objeto contratado. Assim, para a etapa de machine learning, infere-se que o ruído observado entre determinadas classes, sobretudo nas fronteiras entre Saúde e Segurança, constitui um artefato estrutural inerente à base de dados original. Portanto, tais desvios não devem ser interpretados como falhas de aprendizado do classificador, mas sim devidamente contextualizados na análise da matriz de confusão.

---

## Referências

- [`FASE1-CLASSIFICACAO.md`](../FASE1-CLASSIFICACAO.md) · [`metricas_e_decisoes.md`](../metricas_e_decisoes.md)
