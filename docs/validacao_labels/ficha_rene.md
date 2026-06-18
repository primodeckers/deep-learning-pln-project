# Validação manual de labels — Renê Estevam Deckers

Revisão humana da qualidade do **label proxy** (órgão → macroárea). Instruções e consolidação do grupo: [`validacao_labels.md`](validacao_labels.md).

> **Ficha individual — concluída em 2026-06-18.**

---

## Registro

| Campo | Valor |
|-------|-------|
| **Revisor(a)** | Renê Estevam Deckers |
| **Data** | 2026-06-18 |
| **Corpus** | `data/processed/licitacoes_corpus.jsonl` |
| **Script de labels** | `src/preprocess/labels.py` (commit: `3f34890`) |
| **Amostra** | 30 editais · seed 42 |

---

## Tabela (revisão)

<!-- AMOSTRA_INICIO -->
> Amostra · seed=42 · 30 editais

| # | `id` | `orgao_csv` | Trecho do `objeto_html` | Label auto | Concorda? | Label humano | Observação |
|---|------|-------------|-------------------------|------------|-----------|--------------|------------|
| 1 | `974002_5_900332025` | EDF - SECRETARIA DE ESTADO DE ECONOMIA DO DF | Objeto: Pregão Eletrônico - Contratação de empresa especializada em serviços de limpeza e higienização de estofados par… | Administracao/Outros | S | | Gasto administrativo de apoio |
| 2 | `930686_6_900242025` | EDF-ADMINISTRAÇAO REGIONAL DO CRUZEIRO | | Administracao/Outros | S | | Objeto (CSV): ferramentas de poda — administração regional |
| 3 | `974002_5_900302025` | EDF - SECRETARIA DE ESTADO DE ECONOMIA DO DF | Objeto: Pregão Eletrônico - Registro de preços visando a aquisição de material permanente para recreação infantil, a fi… | Administracao/Outros | ? | | Recreação infantil; comprador é AR via Economia — proxy ok, objeto sugere Educação |
| 4 | `170394_5_900242025` | CORPO DE BOMBEIROS MILITAR DO DF | Objeto: Pregão Eletrônico - Registro de preços de materiais de consumo utilizados no Atendimento Pré-Hospitalar do CBMD… | Seguranca | ? | | Material clínico, mas orçamento do CBMDF (Segurança) |
| 5 | `930686_6_900262025` | EDF-ADMINISTRAÇAO REGIONAL DO CRUZEIRO | | Administracao/Outros | S | | Objeto (CSV): copos descartáveis — consumo administrativo |
| 6 | `926119_5_901092025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de insumo(s) à saúde pertencente(s) ao(s) Grupo: 3601 - ARTIGOS PARA SVS,… | Saude | S | | |
| 7 | `974002_5_900242025` | EDF - SECRETARIA DE ESTADO DE ECONOMIA DO DF | Objeto: Pregão Eletrônico - A fim de atender demanda da Secretaria de Estado da Mulher do Distrito Federal (SMDF) a Sub… | Administracao/Outros | S | | Compra centralizada pela Economia para outro órgão |
| 8 | `974200_5_900612025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Serviço de publicação de matéria legal, em jornal de grande circulação nacional. | Saneamento | S | | Despesa operacional da CAESB |
| 9 | `974200_5_900352025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de tintas e materiais para pintura, na forma do Sistema de Registro de Preços SRP. | Saneamento | S | | |
| 10 | `926119_5_900302025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de insumos à saúde pertencentes ao Grupo 36.09.09 (FIOS POLIPROPILENO), e… | Saude | S | | |
| 11 | `974200_5_900332025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de motores estacionários para aplicação no sistema de hidrojateamento no processo… | Saneamento | S | | Infraestrutura de água/esgoto |
| 12 | `170394_5_900312025` | CORPO DE BOMBEIROS MILITAR DO DF | Objeto: Pregão Eletrônico - Aquisição de material de consumo para as atividades clínicas geral da Policlínica Odontológ… | Seguranca | ? | | Objeto odontológico/clínico; label segue órgão (Bombeiros) |
| 13 | `926119_5_900482025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de medicamentos pertencentes ao(s) Grupo 09.R.03.B (OUTROS MEDICAMENTOS P… | Saude | S | | |
| 14 | `926119_5_901132025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição de CAPELA DE FLUXO LAMINAR, para atender as necessidades da Secretaria de Estado … | Saude | S | | |
| 15 | `974200_5_900452025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de materiais de fibra de vidro (PRFV), na forma do Sistema de Registro de Preços … | Saneamento | S | | |
| 16 | `926119_5_900602025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de SERINGAS, em sistema de registro de preços, para atender às necessidad… | Saude | S | | |
| 17 | `926119_5_900672025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de medicamento(s) pertencente(s) ao(s) Grupo: 09.S.01.X - OUTROS OFTALMOL… | Saude | S | | |
| 18 | `926119_5_900342025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de material permanente: Seladoras Automáticas e Manuais, em sistema de re… | Saude | S | | |
| 19 | `974200_5_900272025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de Licenças SDWAN para Firewall Check Point, roteadores SDWAN para unidades remot… | Saneamento | S | | TI operacional da CAESB |
| 20 | `926119_5_900702025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de medicamentos, Grupo: 09.N.01.A - ANESTÉSICOS GERAIS e 09.N.05.A - ANTI… | Saude | S | | |
| 21 | `926119_5_900682025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição reg. de med. pert. ao(s) Grupo: 09.A.12.A - CÁLCIO, Grupo: 09.A.09.A - DIGESTIVOS… | Saude | S | | |
| 22 | `170394_5_900432025` | CORPO DE BOMBEIROS MILITAR DO DF | Objeto: Pregão Eletrônico - Contratação de empresa para prestação de serviços contínuos de LAVANDERIA HOSPITALAR (colet… | Seguranca | ? | | Serviço hospitalar, mas contratante é CBMDF |
| 23 | `170394_6_900232025` | CORPO DE BOMBEIROS MILITAR DO DF | | Seguranca | S | | Objeto (CSV): scanners para viaturas operacionais |
| 24 | `926119_5_900732025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de insumo(s) à saúde pertencente(s) ao(s) Grupo 36.05.06 (FILTROS), em si… | Saude | S | | |
| 25 | `974200_5_900592025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de hidróxido de sódio 50% em contêiner, na forma do Sistema de Registro de Preços… | Saneamento | S | | Insumo de tratamento de água |
| 26 | `930686_6_900272025` | EDF-ADMINISTRAÇAO REGIONAL DO CRUZEIRO | | Administracao/Outros | S | | Objeto (CSV): shampoo automotivo — manutenção de frota local |
| 27 | `926119_5_900882025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de insumo(s) à saúde pertencente(s) ao(s) Grupo: 10.01 - BROCAS ODONTOLÓG… | Saude | S | | |
| 28 | `974200_5_900252025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição, remanejamento, montagem e desmontagem de paredes divisórias, na forma do Sistema… | Saneamento | S | | |
| 29 | `974200_5_900292025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Serviços para Licenças de Software, Suporte Técnico e Garantia por 36 meses para Firewalls … | Saneamento | S | | |
| 30 | `974003_6_900262025` | TRIBUNAL DE CONTAS DO DISTRITO FEDERAL | | Administracao/Outros | N | Saude | Objeto (CSV): insumos odontológicos para divisão de saúde do TCDF |

<!-- AMOSTRA_FIM -->

---

## Resumo

| Métrica | Valor |
|---------|-------|
| Total revisado | 30/30 |
| Concordância (`S`) | 25 |
| Discordância (`N`) | 1 |
| Ambíguos (`?`) | 4 |
| **Taxa de concordância** | 96,2% (25/26, ignorando `?`) |

### Por macroárea (label automático)

| Área | Revisados | Concordam (`S`) | Discordam (`N`) |
|------|-----------|-----------------|-----------------|
| Saude | 11 | 11 | 0 |
| Saneamento | 8 | 8 | 0 |
| Seguranca | 4 | 1 | 0 |
| Educacao | 0 | 0 | 0 |
| Infraestrutura/Obras | 0 | 0 | 0 |
| Administracao/Outros | 7 | 5 | 1 |

### Principais causas de erro

1. Órgãos sem palavra-chave caem em `Administracao/Outros` mesmo com objeto claramente de Saúde (ex.: TCDF — insumos odontológicos).
2. CBMDF compra material/serviço clínico: label `Seguranca` reflete o órgão, não o domínio do objeto.
3. `objeto_html` vazio em dispensas — precisei consultar `objeto_csv` no JSONL.

### Conclusão

Em 30 editais (seed 42), concordei com o label automático em 25 casos (96,2% sobre S+N). O único erro claro foi o TCDF com insumos odontológicos classificado como Administração. Quatro casos ficaram ambíguos — sobretudo Bombeiros com objeto clínico/hospitalar, onde o proxy por órgão faz sentido administrativo mas conflita com a leitura só pelo texto do objeto. Para o escopo do trabalho, o mapeamento é **aceitável**, com ressalva de documentar essa limitação; ajustar `AREA_KEYWORDS` para órgãos com divisão de saúde seria melhoria futura, não crítica para o baseline atual.

---

## Referências

- [`FASE1-CLASSIFICACAO.md`](../FASE1-CLASSIFICACAO.md) · [`metricas_e_decisoes.md`](../metricas_e_decisoes.md)
