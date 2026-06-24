# Model card — licitações ComprasNet DF 2025

Quem avaliar o repositório sem mergulhar no código deve conseguir ler isto em cinco minutos. As tabelas em **Performance** vêm dos JSON em `experiments/` (e do MLflow local, se regenerado).

## O que é isto

Dois pipelines de PLN sobre o mesmo corpus (`data/processed/licitacoes_corpus.jsonl`):

| Tarefa | Modelo atual | Código principal |
|--------|--------------|------------------|
| **Classificação** por macroárea de gasto (6 classes) | TF-IDF + LogReg (**oficial**) · TF-IDF + SVM (comparativo) · BERTimbau (Fase 2) | `baseline_tfidf.py`, `svm_tfidf.py`, `bert_classifier.py` |
| **Sumarização** em linguagem cidadã | Extrativo por regras/regex | `src/summarize/extractive.py` |

**Pendente (Fase 3):** sumarização abstrativa (mT5 ou LLM).

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

### TF-IDF + SVM (comparativo clássico)

**Run:** `classification_svm_20260624-004348`  
**Mesmo corpus, split e `objeto_html` do baseline** · `src/models/svm_tfidf.py`

| Conjunto | Accuracy | F1 macro | F1 weighted |
|----------|----------|----------|-------------|
| Validação | 0,797 | **0,797** | 0,775 |
| Teste | 0,797 | **0,652** | 0,774 |

Matriz: `reports/figures/classification_svm_20260624-004348_confusion.png`

No teste, o SVM ficou **abaixo do LogReg** (0,652 vs 0,740), com queda forte em Educação (F1=0) e Segurança. Mantemos **LogReg como baseline oficial**; o SVM entra na tabela comparativa do relatório.

### Por que não usar `texto` como entrada?

O campo `texto` (HTML completo) repete o nome do órgão em ~97% dos casos — e o label vem justamente do órgão (`orgao_csv`). Com `texto`, o baseline infla para F1 macro ≈ 0,88 (vazamento de label). Com `objeto_html`, a métrica cai para ≈ 0,74, mas reflete generalização mais honesta.

**Entrada oficial:** `objeto_html`. **Não há percentual universal** de vazamento aceitável — documentamos Tabela 7 (~49% residual) e explicamos no relatório conforme [`vazamento_de_label.md`](vazamento_de_label.md). Campo experimental: `objeto_html_limpo` (~47% residual). Ver também [`metricas_e_decisoes.md`](metricas_e_decisoes.md).

### BERTimbau (Fase 2) — run oficial (GPU)

**Run:** `classification_bertimbau_20260623-222508`  
**Modelo:** `neuralmind/bert-base-portuguese-cased` · mesmo split, `text_field` e `seed` do baseline  
**Ambiente:** RTX 4090, PyTorch `+cu126` ([`GPU-EQUIPE.md`](GPU-EQUIPE.md))

| Conjunto | Accuracy | F1 macro | F1 weighted |
|----------|----------|----------|-------------|
| Validação | 0,703 | **0,425** | 0,624 |
| Teste | 0,719 | **0,518** | 0,652 |

Matriz: `reports/figures/classification_bertimbau_20260623-222508_confusion.png`

Detalhes, F1 por classe e textos para o relatório: [`FASE2-CLASSIFICACAO.md`](FASE2-CLASSIFICACAO.md).

### Comparação baseline vs BERT (teste)

| Modelo | Run | F1 macro (teste) |
|--------|-----|------------------|
| **TF-IDF + LogReg** | `classification_baseline_20260608-190839` | **0,740** ← principal |
| **BERTimbau** | `classification_bertimbau_20260623-222508` | **0,518** |

O BERT **não superou** o baseline neste corpus (~295 treino). Classes Segurança e Educação: F1 = 0 no BERT no teste. Resultado válido para o relatório — ver interpretação em [`FASE2-CLASSIFICACAO.md`](FASE2-CLASSIFICACAO.md) §4.

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
- Label é *proxy* derivado do órgão, não de anotação manual por edital. **Validação humana (4/4 integrantes):** 30 editais — média ≈83,2% de concordância (62,5%–96,2% por revisor); ver [`validacao_labels/validacao_labels.md`](validacao_labels/validacao_labels.md).
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

*Última sincronização: baseline `20260608-190839` · BERT `20260623-222508`. Regenerar após novo treino.*
