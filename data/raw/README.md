# Dados brutos

Arquivos exatamente como coletados da fonte — **não editar manualmente**.

| Documento | Descrição |
|---|---|
| [`README.md`](../../README.md) | Índice principal do repositório |
| [`docs/DATA-COLLECTION-DECISIONS.md`](../../docs/DATA-COLLECTION-DECISIONS.md) | Decisões de coleta (CAPTCHA, HTML vs PDF) |
| [`docs/README.md`](../../docs/README.md) | Índice de toda a documentação |

---

## Arquivos

| Arquivo / pasta | Fonte | Descrição |
|---|---|---|
| `licitacoes2025.csv` | [ComprasNet](http://www.comprasnet.gov.br/) | Índice de licitações DF 2025 (437 linhas; 423 URLs únicas) |
| `detalhes/` | `download_editais_detalhe.asp` | **423 HTMLs** coletados via script (sem CAPTCHA) |
| `detalhes/manifest.json` | Gerado pelo script | Log da coleta (status, URLs, erros) |
| `editais/` | `Download.asp` (PDF) | _Pendente_ — exige CAPTCHA manual |

---

## Pipeline de dados (decisão do grupo)

```
licitacoes2025.csv
       │
       ├──► detalhes/*.html     ✅ Fase 1 — automatizado (run_collect.py)
       │
       └──► editais/*.pdf       ⏳ Fase 2 opcional — CAPTCHA manual
                │
                ▼
        data/interim/           texto extraído
                │
                ▼
        data/processed/         dataset PLN (licitacoes_corpus.jsonl)
```

**Após clonar:** HTMLs em `detalhes/` **não** vão para o Git (`.gitignore`). O JSONL versionado traz **423 registros**; para regerar localmente: `run_collect.py` + `run_preprocess.py --overwrite`. Se o preprocess rodar com poucos HTMLs locais, o JSONL fica incompleto (ex.: 114 linhas) — não é amostra da EDA, é corpus parcial.

**Decisão (2026-06-06):** priorizar HTML de detalhe porque é reprodutível e não exige contornar CAPTCHA. PDF completo fica como opção se o HTML for insuficiente para a tarefa de PLN.

---

## Coleta HTML — resumo

| Item | Valor |
|---|---|
| Script | `python scripts/run_collect.py` |
| Data da coleta | 2026-06-06 |
| Arquivos | 423 HTML |
| Erros | 0 |
| Nomenclatura | `{coduasg}_{modprp}_{numprp}.html` |

---

## Colunas do CSV

`Nº da Licitação` · `Modalidade` · `Situação` · `Órgão` · `Código COMPRASNET` · `Tipo` · `Objeto` · **`Edital`** · `Total Homologado`

| Detalhe técnico | Valor |
|---|---|
| Separador | `;` |
| Encoding | `utf-8-sig` |
| Linha 1 | Título `Licitacoes2025` — ignorada no parse |
| Linha 2 | Cabeçalho das colunas |

---

## CAPTCHA (PDF)

O botão **Download** no ComprasNet abre validação de **6 caracteres** (CAPTCHA / anti-robô). Por isso PDFs **não** foram baixados automaticamente. Ver [`docs/DATA-COLLECTION-DECISIONS.md`](../../docs/DATA-COLLECTION-DECISIONS.md) seção 3.
