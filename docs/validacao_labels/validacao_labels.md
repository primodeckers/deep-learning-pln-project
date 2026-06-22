# Validação manual de labels — Fase 1

Revisão humana da qualidade do **label proxy** (órgão → macroárea). Mitiga a limitação documentada em [`FASE1-CLASSIFICACAO.md`](../FASE1-CLASSIFICACAO.md) §3.1 e sustenta a discussão de vieses no relatório.

> **Gabarito (amostra fixa).** Cada integrante preenche sua ficha em [`ficha_*.md`](.) — não preencha as colunas de revisão neste arquivo.

---

## Objetivo

Verificar se o mapeamento automático em `src/preprocess/labels.py` reflete a **área de gasto** que um humano atribuiria ao edital, olhando órgão + objeto da compra.

**Meta:** revisar **~30 editais**, estratificados por macroárea (≈5 por classe quando houver exemplos suficientes).

---

## Fichas individuais

| Integrante | Arquivo |
|------------|---------|
| Elisangela Osorio | [`ficha_elisangela.md`](ficha_elisangela.md) |
| Alexandre Ferreira Ponte | [`ficha_alexandre.md`](ficha_alexandre.md) |
| Renê Estevam Deckers | [`ficha_rene.md`](ficha_rene.md) |
| Integrante 4 _(a definir)_ | [`ficha_integrante4.md`](ficha_integrante4.md) |

---

## Como gerar / regerar a amostra na tabela

Se o corpus ou `labels.py` mudar, rode:

```bash
source .venv/Scripts/activate
python scripts/export_validacao_sample.py
```

Atualiza a **amostra** neste gabarito e nas fichas ainda vazias. A ficha já preenchida (`ficha_rene.md`) **não é sobrescrita**.

> **Atenção:** a amostra de 30 editais abaixo foi fixada com o corpus completo. **Não regerar** depois que fichas estiverem preenchidas — senão apaga respostas e pode mudar os IDs sorteados.

---

## Status das fichas

| Integrante | Arquivo | Status | Taxa (S / S+N) |
|------------|---------|--------|----------------|
| Elisangela Osorio | [`ficha_elisangela.md`](ficha_elisangela.md) | **Concluída** (2026-06-21) | **62,5%** (15/24) |
| Alexandre Ferreira Ponte | [`ficha_alexandre.md`](ficha_alexandre.md) | **Concluída** (2026-06-22) | **95,7%** (22/23) |
| Renê Estevam Deckers | [`ficha_rene.md`](ficha_rene.md) | **Concluída** (2026-06-18) | **96,2%** (25/26) |
| Alexandre Hugo | [`ficha_integrante4.md`](ficha_integrante4.md) | **Concluída** (2026-06-19) | **78,3%** (18/23) |

---

## O que preencher (nas fichas individuais)

| Coluna | Quando preencher |
|--------|------------------|
| **Concorda?** | Sempre — `S` (certo), `N` (errado) ou `?` (ambíguo) |
| **Label humano** | Só se **Concorda?** = `N` — uma das 6 classes abaixo |
| **Observação** | Opcional em `S`; recomendado em `N` e `?` |

---

## Critérios de revisão

Para cada edital, leia:

1. **`orgao_csv`** — quem compra
2. **`objeto_html`** — o que está sendo contratado (abrir o JSONL ou o HTML se precisar de contexto)

Pergunta central:

> *"Este edital deveria ser classificado nesta macroárea de gasto público?"*

| Resposta | Marcar em **Concorda?** |
|----------|------------------------|
| Label automático está correto | `S` |
| Label automático está errado | `N` — preencher **Label humano** |
| Caso ambíguo / não dá para decidir | `?` — explicar em **Observação** |

### Classes válidas (label humano)

Use exatamente um destes rótulos:

- `Saude`
- `Saneamento`
- `Seguranca`
- `Educacao`
- `Infraestrutura/Obras`
- `Administracao/Outros`

### Exemplos de discordância esperada

| Situação | Por que pode dar `N` |
|----------|----------------------|
| Órgão administrativo compra material de saúde | Objeto é Saúde, label cai em Administração |
| "Obras" em objeto genérico de órgão misto | Infraestrutura vs Administração |
| Secretaria com nome atípico sem palavra-chave | Cai no fallback `Administracao/Outros` |

---

## Amostra fixa (gabarito)

<!-- AMOSTRA_INICIO -->
> Amostra fixa · seed=42 · 30 editais · `export_validacao_sample.py`

| # | `id` | `orgao_csv` | Trecho do `objeto_html` | Label auto |
|---|------|-------------|-------------------------|------------|
| 1 | `974002_5_900332025` | EDF - SECRETARIA DE ESTADO DE ECONOMIA DO DF | Objeto: Pregão Eletrônico - Contratação de empresa especializada em serviços de limpeza e higienização de estofados par… | Administracao/Outros |
| 2 | `930686_6_900242025` | EDF-ADMINISTRAÇAO REGIONAL DO CRUZEIRO |  | Administracao/Outros |
| 3 | `974002_5_900302025` | EDF - SECRETARIA DE ESTADO DE ECONOMIA DO DF | Objeto: Pregão Eletrônico - Registro de preços visando a aquisição de material permanente para recreação infantil, a fi… | Administracao/Outros |
| 4 | `170394_5_900242025` | CORPO DE BOMBEIROS MILITAR DO DF | Objeto: Pregão Eletrônico - Registro de preços de materiais de consumo utilizados no Atendimento Pré-Hospitalar do CBMD… | Seguranca |
| 5 | `930686_6_900262025` | EDF-ADMINISTRAÇAO REGIONAL DO CRUZEIRO |  | Administracao/Outros |
| 6 | `926119_5_901092025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de insumo(s) à saúde pertencente(s) ao(s) Grupo: 3601 - ARTIGOS PARA SVS,… | Saude |
| 7 | `974002_5_900242025` | EDF - SECRETARIA DE ESTADO DE ECONOMIA DO DF | Objeto: Pregão Eletrônico - A fim de atender demanda da Secretaria de Estado da Mulher do Distrito Federal (SMDF) a Sub… | Administracao/Outros |
| 8 | `974200_5_900612025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Serviço de publicação de matéria legal, em jornal de grande circulação nacional. | Saneamento |
| 9 | `974200_5_900352025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de tintas e materiais para pintura, na forma do Sistema de Registro de Preços SRP. | Saneamento |
| 10 | `926119_5_900302025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de insumos à saúde pertencentes ao Grupo 36.09.09 (FIOS POLIPROPILENO), e… | Saude |
| 11 | `974200_5_900332025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de motores estacionários para aplicação no sistema de hidrojateamento no processo… | Saneamento |
| 12 | `170394_5_900312025` | CORPO DE BOMBEIROS MILITAR DO DF | Objeto: Pregão Eletrônico - Aquisição de material de consumo para as atividades clínicas geral da Policlínica Odontológ… | Seguranca |
| 13 | `926119_5_900482025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de medicamentos pertencentes ao(s) Grupo 09.R.03.B (OUTROS MEDICAMENTOS P… | Saude |
| 14 | `926119_5_901132025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição de CAPELA DE FLUXO LAMINAR, para atender as necessidades da Secretaria de Estado … | Saude |
| 15 | `974200_5_900452025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de materiais de fibra de vidro (PRFV), na forma do Sistema de Registro de Preços … | Saneamento |
| 16 | `926119_5_900602025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de SERINGAS, em sistema de registro de preços, para atender às necessidad… | Saude |
| 17 | `926119_5_900672025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de medicamento(s) pertencente(s) ao(s) Grupo: 09.S.01.X - OUTROS OFTALMOL… | Saude |
| 18 | `926119_5_900342025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de material permanente: Seladoras Automáticas e Manuais, em sistema de re… | Saude |
| 19 | `974200_5_900272025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de Licenças SDWAN para Firewall Check Point, roteadores SDWAN para unidades remot… | Saneamento |
| 20 | `926119_5_900702025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de medicamentos, Grupo: 09.N.01.A - ANESTÉSICOS GERAIS e 09.N.05.A - ANTI… | Saude |
| 21 | `926119_5_900682025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição reg. de med. pert. ao(s) Grupo: 09.A.12.A - CÁLCIO, Grupo: 09.A.09.A - DIGESTIVOS… | Saude |
| 22 | `170394_5_900432025` | CORPO DE BOMBEIROS MILITAR DO DF | Objeto: Pregão Eletrônico - Contratação de empresa para prestação de serviços contínuos de LAVANDERIA HOSPITALAR (colet… | Seguranca |
| 23 | `170394_6_900232025` | CORPO DE BOMBEIROS MILITAR DO DF |  | Seguranca |
| 24 | `926119_5_900732025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de insumo(s) à saúde pertencente(s) ao(s) Grupo 36.05.06 (FILTROS), em si… | Saude |
| 25 | `974200_5_900592025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição de hidróxido de sódio 50% em contêiner, na forma do Sistema de Registro de Preços… | Saneamento |
| 26 | `930686_6_900272025` | EDF-ADMINISTRAÇAO REGIONAL DO CRUZEIRO |  | Administracao/Outros |
| 27 | `926119_5_900882025` | SECRETARIA DE ESTADO DE SAÚDE - DF | Objeto: Pregão Eletrônico - Aquisição regular de insumo(s) à saúde pertencente(s) ao(s) Grupo: 10.01 - BROCAS ODONTOLÓG… | Saude |
| 28 | `974200_5_900252025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Aquisição, remanejamento, montagem e desmontagem de paredes divisórias, na forma do Sistema… | Saneamento |
| 29 | `974200_5_900292025` | COMPANHIA DE SANEAMENTO AMBIENTAL DO DF CAESB | Objeto: Pregão Eletrônico - Serviços para Licenças de Software, Suporte Técnico e Garantia por 36 meses para Firewalls … | Saneamento |
| 30 | `974003_6_900262025` | TRIBUNAL DE CONTAS DO DISTRITO FEDERAL |  | Administracao/Outros |
<!-- AMOSTRA_FIM -->

---

## Consolidação do grupo

_Completo — 4 de 4 fichas entregues (Renê 2026-06-18; Alexandre Hugo 2026-06-19; Elisangela 2026-06-21; Alexandre Ferreira Ponte 2026-06-22)._

### Resultado — Renê Estevam Deckers

| Métrica | Valor |
|---------|-------|
| Total revisado | 30/30 |
| Concordância (`S`) | 25 |
| Discordância (`N`) | 1 |
| Ambíguos (`?`) | 4 |
| **Taxa** | **96,2%** (25/26, ignorando `?`) |

**Único erro claro (`N`):** `974003_6_900262025` (TCDF) — insumos odontológicos rotulados como `Administracao/Outros`; label humano: `Saude`.

**Casos ambíguos (`?`):** Bombeiros com objeto clínico/hospitalar (linhas 4, 12, 22); recreação infantil via Secretaria de Economia (linha 3).

**Conclusão:** o mapeamento por órgão é **aceitável** para o escopo do trabalho, com ressalva documentada. Ajuste fino em `AREA_KEYWORDS` (ex.: órgãos com divisão de saúde) é melhoria futura, não bloqueante para o baseline.

Detalhes linha a linha: [`ficha_rene.md`](ficha_rene.md).

### Resultado — Alexandre Ferreira Ponte

| Métrica | Valor |
|---------|-------|
| Total revisado | 30/30 |
| Concordância (`S`) | 22 |
| Discordância (`N`) | 1 |
| Ambíguos (`?`) | 7 |
| **Taxa** | **95,7%** (22/23, ignorando `?`) |

**Único erro claro (`N`):** `974003_6_900262025` (TCDF) — insumos odontológicos da divisão de saúde do TCDF rotulados como `Administracao/Outros`; label humano: `Saude`.

**Casos ambíguos (`?`):** compras transversais — TI/serviços administrativos da CAESB rotulados como `Saneamento` (linhas 8, 19, 29); insumos/serviços de saúde do CBMDF rotulados como `Seguranca` (linhas 4, 12, 22); compra centralizada da SEFAZ com objeto educacional em `Administracao/Outros` (linha 3).

**Conclusão:** o label proxy é **aceitável** para o escopo; a fragilidade não está em erros de mapeamento por órgão, mas na perda de granularidade em aquisições transversais — ruído estrutural a contextualizar na matriz de confusão (fronteiras Saúde↔Segurança e Saneamento↔Administração).

Detalhes linha a linha: [`ficha_alexandre.md`](ficha_alexandre.md).

### Resultado — Elisangela Osorio

| Métrica | Valor |
|---------|-------|
| Total revisado | 30/30 |
| Concordância (`S`) | 15 |
| Discordância (`N`) | 9 |
| Ambíguos (`?`) | 6 |
| **Taxa** | **62,5%** (15/24, ignorando `?`) |

Revisão mais rigorosa do grupo: marca `N` sempre que o objeto aponta para área diferente da do órgão — CBMDF→`Saude` (4, 12, 22), CAESB→`Administracao/Outros` (8, 19, 28, 29) ou `Infraestrutura/Obras` (9), e SEFAZ→`Educacao` (3). Trata os editais sem `objeto_html` como `?`. Detalhes: [`ficha_elisangela.md`](ficha_elisangela.md).

### Resultado — Alexandre Hugo

| Métrica | Valor |
|---------|-------|
| Total revisado | 30/30 |
| Concordância (`S`) | 18 |
| Discordância (`N`) | 5 |
| Ambíguos (`?`) | 7 |
| **Taxa** | **78,3%** (18/23, ignorando `?`) |

Posição intermediária: marca `N` nos casos de saúde em órgão de segurança (4, 12, 22), TCDF→`Saude` (30) e CAESB divisórias→`Administracao/Outros` (28); deixa TI/serviços da CAESB como `?`. Detalhes: [`ficha_integrante4.md`](ficha_integrante4.md).

### Síntese para o relatório

As **4 fichas** foram concluídas. A **média das taxas individuais** de concordância (S/(S+N), ignorando ambíguos) é **≈83,2%** (Renê 96,2% · Alexandre Ponte 95,7% · Alexandre Hugo 78,3% · Elisangela 62,5%). A dispersão entre revisores (62,5%–96,2%) reflete **critério**, não erro: parte do grupo marca compras transversais como `N`, outra parte como `?`.

**Editais com discordância (`N`) em ≥2 revisores** — candidatos a recategorização manual ou a regra complementar em `src/preprocess/labels.py`:

| # | `id` | Órgão | Label auto | Label humano (consenso) | Nº de `N` |
|---|------|-------|------------|-------------------------|-----------|
| 30 | `974003_6_900262025` | TCDF | `Administracao/Outros` | `Saude` | 3 |
| 4 | `170394_5_900242025` | CBMDF | `Seguranca` | `Saude` | 2 |
| 12 | `170394_5_900312025` | CBMDF | `Seguranca` | `Saude` | 2 |
| 22 | `170394_5_900432025` | CBMDF | `Seguranca` | `Saude` | 2 |
| 28 | `974200_5_900252025` | CAESB | `Saneamento` | `Administracao/Outros` | 2 |

**Parágrafo (seção de limitações):** O label proxy órgão→macroárea é **aceitável como rotulagem fraca** para o baseline da Fase 1 (concordância média ≈83%), porém apresenta viés sistemático em órgãos cujas atividades-meio cruzam outras áreas. O CBMDF mantém estrutura interna de saúde (atendimento pré-hospitalar, policlínica odontológica, lavanderia hospitalar) cujos gastos são rotulados como `Seguranca`; o TCDF, com divisão de saúde própria, cai em `Administracao/Outros`; e a CAESB concentra os casos ambíguos de TI e serviços administrativos. Esses desvios são **estruturais da base** — decorrem do mapeamento por órgão, não do classificador — e devem ser contextualizados na análise da matriz de confusão, sobretudo nas fronteiras **Saúde↔Segurança** e **Saneamento↔Administração**. Como melhoria futura (não bloqueante para o baseline), sugere-se refinar `AREA_KEYWORDS` ou adicionar regras baseadas no objeto para órgãos com divisão de saúde.

---

## Referências no projeto

- Mapeamento automático: `src/preprocess/labels.py`
- Guia da Fase 1: [`FASE1-CLASSIFICACAO.md`](../FASE1-CLASSIFICACAO.md)
- Discussão label proxy: [`metricas_e_decisoes.md`](../metricas_e_decisoes.md)
