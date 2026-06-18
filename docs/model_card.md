# Model card — licitações ComprasNet DF 2025

Quem avaliar o repositório sem mergulhar no código deve conseguir ler isto em cinco minutos. As tabelas em **Performance** vêm dos JSON em `experiments/` (e do MLflow local, se regenerado).

## O que é isto

Dois pipelines de PLN sobre o mesmo corpus (`data/processed/licitacoes_corpus.jsonl`):

| Tarefa | Modelo atual | Código principal |
|--------|--------------|------------------|
| **Classificação** por macroárea de gasto (6 classes) | TF-IDF + Regressão Logística | `src/models/baseline_tfidf.py`, `scripts/run_train.py` |
| **Sumarização** em linguagem cidadã | Extrativo por regras/regex | `src/summarize/extractive.py` |

**Pendente (Fases 2–3):** BERTimbau para classificação; sumarização abstrativa (mT5 ou LLM).

## Uso pretendido

- **Classificação:** apoio à triagem de editais por área de gasto (Saúde, Saneamento, Segurança, Educação, Infraestrutura/Obras, Administração/Outros).
- **Sumarização:** gerar resumos legíveis para cidadãos (objeto, modalidade, quem pode participar, prazo, valor).

Nenhum dos modelos substitui análise jurídica ou decisão administrativa — são baselines acadêmicos.

## Performance — classificação

**Run de referência:** `classification_baseline_20260608-190839`  
**Entrada:** `objeto_html` (descrição do objeto, sem cabeçalho do órgão)  
**Split:** 70/15/15 estratificado por macroárea, `seed=42`  
**Corpus:** 423 registros no manifesto de pré-processamento; 423 exemplos rotulados no split completo

| Conjunto | Accuracy | F1 macro | F1 weighted |
|----------|----------|----------|-------------|
| Validação | 0,766 | **0,743** | 0,750 |
| Teste | 0,797 | **0,740** | 0,788 |

Matriz de confusão: `reports/figures/classification_baseline_20260608-190839_confusion.png`

### Por que não usar `texto` como entrada?

O campo `texto` (HTML completo) repete o nome do órgão em ~97% dos casos — e o label vem justamente do órgão (`orgao_csv`). Com `texto`, o baseline infla para F1 macro ≈ 0,88 (vazamento de label). Com `objeto_html`, a métrica cai para ≈ 0,74, mas reflete generalização mais honesta.

**Entrada oficial:** `objeto_html`. **Não há percentual universal** de vazamento aceitável — documentamos Tabela 7 (~49% residual) e explicamos no relatório conforme [`vazamento_de_label.md`](vazamento_de_label.md). Campo experimental: `objeto_html_limpo` (~47% residual). Ver também [`metricas_e_decisoes.md`](metricas_e_decisoes.md).

## Performance — sumarização extrativa

**Run de referência:** `summarization_extractive_20260608-190841`  
**Amostra:** 18 editais do conjunto de teste da classificação

| Cobertura | Valor |
|-----------|-------|
| Com prazo extraído | 15/18 |
| Com valor extraído | 18/18 |

Exemplos qualitativos: `reports/slides/resumos_exemplos.md`  
Saída estruturada: `data/processed/resumos_extrativos.jsonl`

Avaliação quantitativa (ROUGE) e humana (escala 1–5) estão previstas na Fase 3.

## Dados

| Campo | Papel |
|-------|--------|
| `orgao_csv` | Gera o label (`area`) por palavras-chave — **não** entra como feature |
| `objeto_html` | Entrada recomendada do classificador |
| `texto` | HTML completo; útil para sumarização, mas vaza label na classificação |
| `modalidade`, `tipo`, `total_homologado` | Usados pelo resumidor extrativo |

**Limitações declaradas:**

- Corpus pequeno (~400 editais) para deep learning — classes raras (Educação, Infraestrutura) têm poucos exemplos.
- Label é *proxy* derivado do órgão, não de anotação manual por edital. **Validação humana (parcial):** 30 editais revisados por 1 integrante — 96,2% de concordância com o mapeamento automático; ver [`validacao_labels/validacao_labels.md`](validacao_labels/validacao_labels.md).
- **Vazamento de label:** entrada oficial `objeto_html` reduz pistas do órgão no texto (~49% residual na Tabela 7); não existe limiar universal — ver [`vazamento_de_label.md`](vazamento_de_label.md).
- Dados de um único estado (DF) e ano (2025) — não generalizam para todo o Brasil.

## Onde o modelo engana ou fica cego

- **Classes minoritárias** (Segurança, Educação, Infraestrutura): F1 instável; confusão com Administração/Outros.
- **Órgãos ambíguos** no mapeamento por palavra-chave caem em `Administracao/Outros`.
- **Objetos genéricos** (“aquisição de materiais”) dificultam a classificação só pelo texto do objeto.
- **Sumarização extrativa** não parafraseia — só monta frases a partir de campos extraídos; não cobre cláusulas complexas.

## Artefatos

| Artefato | Caminho |
|----------|---------|
| Modelo baseline | `models/classification_baseline_*.joblib` (não versionado) |
| Registro portátil | `experiments/<run_id>.json` |
| MLflow local | `experiments/mlflow.db` (gitignored) |

---

*Última sincronização com `experiments/classification_baseline_20260608-190839.json`. Regenerar após novo treino com `make train-baseline`.*
