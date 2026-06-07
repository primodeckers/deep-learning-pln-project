
# Decisões de coleta de dados

> Registro formal das escolhas metodógicas sobre fonte, download e corpus PLN.  
> Atualizar este arquivo sempre que o grupo tomar uma nova decisão sobre dados.

**Projeto:** PLN aplicado a editais de licitações públicas (ComprasNet, DF 2025)  
**Última atualização:** 2026-06-06

---

## 1. Contexto

O grupo definiu como base o arquivo `data/raw/licitacoes2025.csv`, exportado do [ComprasNet](http://www.comprasnet.gov.br/), contendo licitações do Distrito Federal em 2025. A coluna **Edital** aponta para URLs do portal onde estão os documentos das licitações.

O objetivo é construir um **corpus textual** para treinar/avaliar modelos de PLN, conectado ao setor público (requisito da Modalidade 2 da disciplina).

---

## 2. Log cronológico de decisões

| Data | Decisão | Alternativas consideradas | Motivo | Status |
|---|---|---|---|---|
| 2026-06-06 | Usar `licitacoes2025.csv` como índice principal | Kaggle, bases prontas | Dados inéditos coletados pelo grupo; exigência da disciplina | Adotado |
| 2026-06-06 | Tema: PLN sobre licitações públicas (ComprasNet / DF) | Sentimento em notícias, ouvidorias, sumarização de leis | Alinhamento com setor público + dados já disponíveis | Adotado |
| 2026-06-06 | Estrutura de pastas `data/raw` → `interim` → `processed` | Tudo na raiz do repo | Padrão ML/DL; separa bruto de processado; reprodutibilidade | Adotado |
| 2026-06-06 | Coletar **HTML de detalhe** em vez de PDF (fase 1) | PDF via CAPTCHA; PNCP; quebra de CAPTCHA com IA | HTML acessível sem CAPTCHA; script reprodutível; ética acadêmica | Adotado |
| 2026-06-06 | **Não** automatizar quebra de CAPTCHA | Selenium + OCR/CNN (ex.: projetos no GitHub) | Contra propósito do sistema; risco legal/ético; fora do escopo PLN | Rejeitado |
| 2026-06-06 | PDFs completos ficam como **fase opcional** (download manual) | Baixar 437 PDFs antes de começar PLN | CAPTCHA impede automação; HTML já gera corpus utilizável | Pendente |
| 2026-06-06 | Investigar **PNCP** como fonte complementar | Só ComprasNet | API oficial sem CAPTCHA; pode enriquecer ou validar dados | A investigar |
| 2026-06-06 | Nomear arquivos HTML como `{coduasg}_{modprp}_{numprp}.html` | Número da licitação (`90119_2025`) | Mesmo nº de licitação aparece para órgãos/modalidades diferentes no CSV | Adotado |
| 2026-06-06 | Intervalo de **0,8 s** entre requests HTTP | Sem delay; delay maior | Respeitar servidor público; reduzir risco de bloqueio | Adotado |
| 2026-06-06 | Gerar `manifest.json` após cada coleta | Só arquivos soltos | Rastreabilidade, auditoria e base para relatório | Adotado |
| 2026-06-06 | Pré-processamento HTML → corpus JSONL | Processar só no notebook | Pipeline reprodutível via `run_preprocess.py` | Adotado |
| 2026-06-06 | Volume **423 editais** suficiente para fase 1 | Expandir 2021–2024 (+4 anos) | +4 anos adiado; prazo da disciplina; volume adequado para classificação e sumarização | Adotado |

---

## 3. Descoberta técnica: CAPTCHA no download de PDF

Ao clicar em **Download** no ComprasNet, abre um popup (`Download.asp`) com validação de **6 caracteres** (imagem ou áudio).

| Termo | Significado |
|---|---|
| **CAPTCHA** | Teste anti-robô (*Completely Automated Public Turing test to tell Computers and Humans Apart*) |
| **Sistema usado** | Intercepta (SRF) → endpoint `captcha.aspx` |
| **Finalidade (site)** | Evitar consultas automatizadas que prejudiquem outros usuários |

### Dois fluxos distintos no ComprasNet

```
CSV → coluna Edital (URL)
         │
         ├── download_editais_detalhe.asp  →  HTML (órgão, objeto, itens)     [SEM CAPTCHA]
         │
         └── Download.asp (botão Download)  →  CAPTCHA  →  PDF completo      [COM CAPTCHA]
```

**Implicação:** automação em massa de PDFs **não é viável** sem intervenção humana ou contorno antiético do CAPTCHA.

---

## 4. Estratégia adotada (fase 1)

### Pipeline atual

```
licitacoes2025.csv
       │
       ▼
scripts/run_collect.py  →  src/collect/download_detalhes.py
       │
       ▼
data/raw/detalhes/*.html  (423 arquivos únicos)
       │
       ▼
scripts/run_preprocess.py  →  src/preprocess/extract_html.py, build_dataset.py
       │
       ├── data/interim/text/*.txt
       ├── data/interim/records/*.json
       └── data/processed/licitacoes_corpus.jsonl  (423 registros)
```

### Resultado da coleta (2026-06-06)

| Métrica | Valor |
|---|---|
| Registros no CSV | 437 |
| URLs únicas | 423 |
| Linhas duplicadas no CSV | 14 |
| HTMLs baixados | 423 |
| Erros HTTP | 0 |
| Manifesto de coleta | `data/raw/detalhes/manifest.json` |

### Resultado do pré-processamento (2026-06-06)

| Métrica | Valor |
|---|---|
| HTMLs processados | 423 |
| Erros na extração | 0 |
| Corpus final | `data/processed/licitacoes_corpus.jsonl` |
| Manifesto de pré-processamento | `data/processed/preprocess_manifest.json` |

### Como reproduzir

```bash
pip install -r requirements.txt

# Coleta
python scripts/run_collect.py              # retoma: pula arquivos existentes
python scripts/run_collect.py --limit 5    # teste
python scripts/run_collect.py --overwrite  # baixar tudo de novo
python scripts/run_collect.py --delay 1.0  # intervalo entre requests (segundos)

# Pré-processamento
python scripts/run_preprocess.py
python scripts/run_preprocess.py --overwrite  # reprocessar tudo
```

### Detalhes de implementação

| Aspecto | Decisão |
|---|---|
| Encoding do CSV | `utf-8-sig` (BOM + linha título `Licitacoes2025` ignorada) |
| Separador CSV | `;` |
| Encoding dos HTMLs | ISO-8859-1 (Latin-1) → convertido para UTF-8 no corpus |
| Biblioteca HTTP | `requests` |
| Parsing HTML | `beautifulsoup4` |
| User-Agent | Identifica projeto acadêmico + URL do repositório |
| Idempotência | Reexecução pula arquivos já existentes (salvo `--overwrite`) |

---

## 5. Opções avaliadas e não adotadas (por enquanto)

### 5.1 PDF via CAPTCHA manual

- **Prós:** edital oficial completo (anexos, cláusulas longas)
- **Contras:** ~437 downloads; ~110 por integrante; não reprodutível via script
- **Quando adotar:** se compararmos HTML vs PDF e o HTML for insuficiente

### 5.2 PNCP (Portal Nacional de Contratações Públicas)

- **URL:** https://pncp.gov.br/api/pncp/swagger-ui/index.html
- **Prós:** API pública, sem CAPTCHA, fonte oficial
- **Contras:** pode não cobrir 100% das licitações do export ComprasNet legado
- **Quando adotar:** para validar/cruzar documentos ou enriquecer metadados

### 5.3 Quebra automatizada de CAPTCHA

- **Prós:** automação total de PDFs
- **Contras:** ético/legalmente problemático; contradiz uso responsável de IA
- **Decisão:** **rejeitado** para este trabalho acadêmico

---

## 6. Análise de volume de dados (adequação)

Documento de referência para a discussão do relatório: **423 editais bastam para o projeto?** Precisaríamos de mais anos (2021–2024)?

### 6.1 O que temos hoje

| Métrica | Valor |
|---|---|
| Registros no CSV | 437 |
| URLs únicas / corpus | **423** |
| Período | DF, **2025** (export ComprasNet) |
| Tipo | MATERIAL: 320 (76%) · SERVIÇO: 103 (24%) |
| Tamanho do texto | mediana ~1.600 chars · média ~3.400 · máx. ~41.300 |

### 6.2 Por tarefa de PLN

| Tarefa | Volume necessário (regra prática) | 423 editais |
|---|---|---|
| **Baseline TF-IDF + LogReg** | Centenas de docs por classe | ✅ Adequado |
| **Fine-tuning BERTimbau** (6 classes) | Ideal: 1k+; mínimo acadêmico: ~50–100/classe | ⚠️ Funciona, com ressalvas |
| **Sumarização** (amostra + eval humana) | Dezenas a centenas para demo; 20–30 para nota humana | ✅ Adequado (não precisa rotular 423) |
| **NER / anotação manual** | Centenas por tipo de entidade | ❌ Apertado — não é nosso foco |

Referência da aula ([`aula03-04.pdf`](aula03-04.pdf)): com ~10k amostras tabulares, tree-based models ainda competem com DL; com **texto não estruturado** e **423 docs**, faz sentido usar Transformers, mas o volume é **pequeno** — baseline clássico continua obrigatório para comparação.

### 6.3 Desbalanceamento por macroárea (label proxy via órgão)

Estimativa para split **70% / 15% / 15%** estratificado:

| Macroárea | Total | ~Treino | ~Val | ~Test |
|---|---:|---:|---:|---:|
| Administração / Outros | 176 | 123 | 26 | 27 |
| Saúde | 106 | 74 | 15 | 17 |
| Segurança | 51 | 35 | 7 | 9 |
| Saneamento | 49 | 34 | 7 | 8 |
| Infraestrutura / Obras | 24 | 16 | 3 | 5 |
| Educação | 17 | 11 | 2 | 4 |

**Implicações:**

- **Saúde** e **Administração/Outros** dominam — F1 macro pode ser puxado por elas.
- **Educação** e **Infra/Obras** têm poucos exemplos no teste (4–5) — F1 por classe será **instável**; declarar no relatório.
- Classe "Outros" grande demais — revisar mapeamento dos 20 maiores órgãos pode melhorar sem coletar mais dados.

### 6.4 Comparativo: 1 ano vs +4 anos (2021–2025)

| Critério | Só 2025 (423) | +4 anos (~1.500–2.000 est.) |
|---|---|---|
| Entrega no prazo da disciplina | ✅ Viável | ⚠️ Coleta + reprocessamento pesados |
| Métricas mais estáveis | Limitado | Melhor, especialmente classes raras |
| Generalização temporal | Não testada | Permite validar “funciona em outro ano?” |
| Risco de mudança portal/lei | Baixo (um export) | Médio (HTML/CSV podem diferir) |
| Exigência do professor (dados inéditos coletados) | ✅ Atende | ✅ Atende se o grupo coletar |

**Decisão do grupo (2026-06-06):** **não expandir** para 2021–2024 na fase 1. Volume atual é **suficiente** para classificação + sumarização complementar, desde que limitações e desbalanceamento sejam discutidos. Expansão temporal fica como **próximo passo** (seção 8 e relatório), não bloqueio.

### 6.5 Infraestrutura de treino (local vs cloud)

| Opção | Adequação neste corpus |
|---|---|
| **GPU local (RTX 4090, 24 GB)** | ✅ Recomendada — BERTimbau e mT5-small cabem; treino em minutos; iteração rápida |
| **Databricks / cloud GPU** | Desnecessário para 423 textos — útil só se o grupo quiser aprender a plataforma como extra |

Detalhes operacionais: [`UNIVERSAL-DEEP-LEARNING-GUIDE.md`](UNIVERSAL-DEEP-LEARNING-GUIDE.md) (Fases 1–3).

### 6.6 O que escrever no relatório

1. **Volume:** 423 editais únicos, um ano (DF 2025), coleta reprodutível via script.
2. **Suficiência:** adequado para objetivos do trabalho; não é dataset “grande” para DL.
3. **Limitação principal:** classes desbalanceadas e poucos exemplos em Educação/Infra.
4. **Mitigação:** F1 macro, `class_weight`, validação manual de ~30 labels, análise de erros qualitativa.
5. **Extensão futura:** coletar 2021–2024 ou cruzar PNCP se quiserem robustez temporal.

---

## 7. Limitações documentadas (para relatório e discussão)

1. Corpus fase 1 = **HTML de detalhe**, não PDF integral do edital
2. Campo **Objeto** no CSV pode estar truncado vs. conteúdo completo
3. CSV contém **14 URLs repetidas** (mesma licitação listada mais de uma vez)
4. Mesmo **número de licitação** pode referir **órgãos diferentes** — por isso o ID do arquivo usa parâmetros da URL
5. Links podem expirar ou mudar — coleta deve ser datada e versionada no Git
6. Encoding das páginas HTML: ISO-8859-1 (Latin-1) — tratado no pré-processamento
7. PDFs exigem CAPTCHA — coleta em massa de PDF **não documentada como reprodutível**

---

## 8. Decisões pendentes

| # | Pergunta | Impacto |
|---|---|---|
| 1 | HTML de detalhe basta ou precisamos de amostra de PDFs? | Define escopo da coleta fase 2 |
| 2 | Qual tarefa de PLN? (classificação, sumarização, NER?) | Define labels e métricas |
| 3 | Cruzar com PNCP? | Pode adicionar documentos ou metadados |
| 4 | Filtros no CSV (situação, modalidade, órgão)? | Tamanho e qualidade do corpus |
| 5 | Expandir corpus para 2021–2024? | **Adiado** na fase 1 (decisão 2026-06-06); retomar se precisar robustez temporal ou classes raras |

Ver brainstorm de temas: [`PROPOSALS.md`](PROPOSALS.md)

---

## 9. Referências para o relatório

- ComprasNet — Consulta de Licitações: http://www.comprasnet.gov.br/
- PNCP — API de consultas: https://pncp.gov.br/api/pncp/swagger-ui/index.html
- PNCP — Dados abertos: https://www.gov.br/pncp/pt-br/acesso-a-informacao/dados-abertos
- Código de coleta: `scripts/run_collect.py`, `src/collect/`
- Código de pré-processamento: `scripts/run_preprocess.py`, `src/preprocess/`

---

## 10. Template para novas decisões

Copiar e preencher quando o grupo decidir algo novo:

```markdown
| YYYY-MM-DD | [Decisão] | [Alternativas] | [Motivo] | Adotado / Rejeitado / Pendente |
```

