# Conteúdo da apresentação — PLN aplicado a editais de licitação

**Título:** Classificação automática de editais de licitação por área de gasto público (ComprasNet, Distrito Federal, 2025)
**Modalidade:** 2 — PLN no Setor Público · Grupo de 4
**Integrantes:** Elisangela Osorio · Alexandre Ferreira Ponte · Renê Estevam Deckers · Alexandre Hugo Sampaio Netto

---

## 1. Contexto — o problema real

Todo edital de licitação tem um campo **Objeto**: um texto livre, em linguagem jurídico-administrativa, dizendo o que o governo quer comprar ou contratar (de "medicamentos antimetabólitos" a "tubos de PVC" ou "digitalização técnica").

- **Para o controle social** (cidadão, jornalista, órgão de controle), saber ***em que áreas* o DF compra** — e quantas licitações caem em Saúde, Obras, etc. — exige ler ou classificar centenas de descrições à mão; inviável sem automação.
- **Para o pequeno fornecedor**, o jargão ("sistema de registro de preços", "qualificação técnica") afasta exatamente quem o edital deveria alcançar.

O projeto concentra-se em **triagem automática por área de gasto** (classificação).

---

## 2. Base teórica — artigos que sustentam o projeto

**Técnica (PLN / Deep Learning / Transformers):**

- **Devlin et al. (2019) — BERT:** fundamenta o fine-tuning de Transformers para classificação textual.
- **Souza et al. — BERTimbau:** modelo BERT pré-treinado em português brasileiro.
- **Srivastava et al. (2014) — Dropout** e **Goodfellow, Bengio & Courville (2016), cap. 10:** regularização e modelagem de sequências (contexto teórico de DL).
- **Material da disciplina (aula 03–04):** guia prático cujo lema é *"depende"* — a escolha do modelo depende do problema, do volume de dados e do diagnóstico treino × validação. Sustenta a decisão de comparar baseline clássico com Transformer.

**Domínio (licitações / transparência / linguagem cidadã) — lista fechada (ver §9):**

- **Souto, Gomes & Riveros (2025):** IA aplicada a editais de licitação (caso Alice, CGU/TCU) — precedente direto da triagem automática.
- **Ferreira (2019, UnB):** PLN e classificação de atos de contratos e licitações do **GDF** — mesmo domínio (DF).
- **Watanabe & Sousa (2023):** aprendizado de máquina para classificação automática de documentos do setor público.
- **Macedo et al. (2025):** governo aberto e transparência nas capitais — fundamenta o problema (controle social).
- *Marco legal:* Lei 14.133/2021 (licitações), Lei 12.527/2011 (LAI) + Decreto 8.777/2016 (dados abertos), Lei 15.263/2025 (linguagem simples).

---

## 3. Dados — como foram obtidos

- **Fonte:** [ComprasNet](http://www.comprasnet.gov.br/) — export manual de *Consulta de Licitações* (filtro **UF = DF**, ano **2025**). **Dados inéditos coletados pelo grupo** (a disciplina proíbe bases prontas / Kaggle).
- **Índice:** `licitacoes2025.csv` — 437 linhas → **423 URLs únicas** (14 duplicatas), **52 órgãos** distintos.
- **Decisão metodológica e ética:** coletar o **HTML de detalhe** (sem CAPTCHA) em vez do PDF completo (protegido por CAPTCHA). Quebra automatizada de CAPTCHA foi **rejeitada** por ser antiética e fora do escopo.
- **Pipeline reprodutível** (`scripts/run_collect.py` → `run_preprocess.py`):
  - `requests` + `BeautifulSoup`; intervalo de **0,8 s** entre requisições (respeito ao servidor público); User-Agent identifica o projeto acadêmico.
  - Encoding ISO-8859-1 → UTF-8; geração de `manifest.json` para auditoria.
  - Resultado: **423 HTMLs**, 0 erros → corpus `licitacoes_corpus.jsonl` (**423 registros**, hash SHA-256 versionado).
- **Perfil do corpus:** 320 material / 103 serviço; 278 pregões, 134 dispensas, 11 concorrências; texto com mediana ~1.600 caracteres (máx. ~41.300).
- **Rótulo (label):** *proxy* via **órgão → 6 macroáreas** (Saúde, Saneamento, Segurança, Educação, Infraestrutura/Obras, Administração/Outros). **Validação humana** de 30 editais (4/4 fichas) → concordância média **≈ 83,2%**.
- **Limitações dos dados:** corpus pequeno (423) e **desbalanceado** (Educação 17, Infra 24, Admin/Outros 176); apenas DF/2025; HTML de detalhe (não o PDF integral).

---

## 4. Metodologia — arquitetura e protocolo

**Tarefa principal:** classificação multiclasse em **6 macroáreas**.

**Protocolo único (anti-comparação injusta):**

- **Entrada:** `objeto_html` — **e não** o texto completo. O texto completo repete o nome do órgão em ~~97% dos casos → **vazamento de label** (F1 inflado ≈ 0,88). Com `objeto_html` o vazamento residual cai a ~49% e o F1 fica **honesto** (~~0,74).
- **Split:** 70/15/15 **estratificado por área**, `seed = 42` → 295 treino / 64 val / 64 teste.
- **Seleção pela validação; relatório reporta o TESTE.**

**Três modelos comparados:**

| Fase               | Modelo                                                  | Configuração-chave                                                              |
| ------------------ | ------------------------------------------------------- | ------------------------------------------------------------------------------- |
| 1 (oficial)        | **TF-IDF + Regressão Logística**                        | n-grama até 2, `min_df=2`, `max_features=20k`, `C=1.0`, `class_weight=balanced` |
| 3 (comparativo)    | TF-IDF + **SVM linear**                                 | mesmo vetorizador, `class_weight=balanced`                                      |
| 2 (comparativo DL) | **BERTimbau** (`neuralmind/bert-base-portuguese-cased`) | `max_len=512`, `batch=16`, `lr=2e-5`, 4 épocas + early stopping; GPU RTX 4090   |

**Avaliação e rastreamento:** F1 macro (métrica primária, por causa do desbalanceamento), F1 por classe, matriz de confusão; cada run gravado em JSON + MLflow com hash do corpus e commit Git.

**Extensão PNCP (~20 mil compras):** protocolos `pncp`, `pncp9`, `pncp9full`, `pncp9fb`, `pncp9fbi` — roteiro falado do slide: [`ROTEIRO-FAMILIA-PROTOCOLOS-PNCP.md`](ROTEIRO-FAMILIA-PROTOCOLOS-PNCP.md). Regras: [`REGRAS-E-PROTOCOLOS.md`](REGRAS-E-PROTOCOLOS.md) §10.

---

## 5. Resultados — métricas e achados

### O que testamos

Separamos **64 editais** que o modelo **nunca viu** (conjunto de teste). Para cada um, perguntamos: *“Em qual macroárea de gasto este edital se encaixa?”* (Saúde, Saneamento, Segurança, Educação, Infraestrutura/Obras ou Administração/Outros).

**F1 macro (nota de 0 a 1):** média do desempenho nas **6 áreas com peso igual**. Se o modelo ignora Segurança ou Educação, a nota cai — mesmo que acerte quase sempre Administração/Outros (a classe mais frequente).

**Accuracy (~80%):** percentual de acertos no total. Útil como contexto, mas **sozinha engana** — um modelo pode ter 80% de acerto e falhar sempre nas áreas raras.

---

### Classificação — comparação dos 3 modelos (teste, 64 editais)

| Modelo                            | F1 macro | Accuracy | Leitura simples                                                                                              |
| --------------------------------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------ |
| **TF-IDF + LogReg** *(escolhido)* | **0,74** | 0,80     | **Venceu.** Modelo simples, estável, acerta bem nas áreas com mais exemplos                                  |
| TF-IDF + SVM                      | 0,65     | 0,80     | Mesma accuracy, mas pior F1 — se adaptou demais aos 64 editais de validação                                  |
| BERTimbau                         | 0,40     | 0,69     | **Perdeu.** Rede neural grande com pouco treino (~295 editais) — chutou quase tudo como Administração/Outros |

**Por que escolhemos o LogReg e não o SVM?** Os dois tiveram accuracy parecida (~80%), mas o SVM foi melhor na validação (F1 0,80) e pior no teste (0,65). O LogReg manteve o mesmo desempenho nos dois (0,74) — sinal de que **generaliza melhor**.

> **Em uma frase:** o SVM foi bem na “prova” de validação, mas caiu no teste — memorizou detalhes daqueles 64 editais em vez de aprender a classificar editais novos.

**Por que o BERT perdeu?** Com ~295 editais de treino e 6 classes (Educação tem só 12 no treino), o Transformer **não teve dados suficientes**. Nas classes raras do teste, o F1 foi **zero**: Segurança, Educação e Infraestrutura — o modelo simplesmente não as aprendeu.

---

### Onde o LogReg acerta e onde erra (teste)

| Área                 | Editais no teste | F1   | O que isso quer dizer                                                                                                    |
| -------------------- | ---------------- | ---- | ------------------------------------------------------------------------------------------------------------------------ |
| Saneamento           | 7                | 1,00 | Acertou **todos**                                                                                                        |
| Saúde                | 17               | 0,90 | Muito bom — maior volume de exemplos ajuda                                                                               |
| Administração/Outros | 25               | 0,81 | Bom — é a classe mais comum (25 de 64 editais)                                                                           |
| Educação             | 2                | 0,67 | Só **2 editais** no teste — número pouco confiável                                                                       |
| Infraestrutura/Obras | 4                | 0,60 | Razoável, mas poucos exemplos                                                                                            |
| Segurança            | 9                | 0,46 | **Pior resultado** — confunde com Saúde (ex.: Bombeiros comprando material clínico; rótulo veio do órgão, não do objeto) |

---

### Achado central (1 frase)

Com **423 editais** e classes **desbalanceadas**, o **modelo clássico simples superou o BERT** — contrário à expectativa inicial. Para este volume de dados, TF-IDF + LogReg (F1 **0,74**) é a escolha certa; o BERT (F1 **0,40**) precisaria de muito mais editais para valer a pena.

---

## 6. Discussão — resolveu? quais os limites?

**Resolveu, parcialmente e com rigor.** A triagem automática por área funciona bem nas classes majoritárias (Saúde, Saneamento, Admin/Outros, F1 ≥ 0,80) e é instável nas raras.

**Por que o clássico ganhou:**

- BERT tem dezenas de milhões de parâmetros para apenas ~295 exemplos de treino → overfitting/colapso nas classes raras.
- O **SVM** foi melhor na validação (0,80) e pior no teste (0,65): ajustou-se demais aos 64 editais de validação. O **LogReg** manteve val ≈ teste (0,74) — estabilidade é o que pesou na escolha.

> **Em uma frase:** o SVM foi bem na “prova” de validação, mas caiu no teste — memorizou detalhes daqueles 64 editais em vez de aprender a classificar editais novos.

**Limites e vieses (declarados, não escondidos):**

- Corpus pequeno (423) e desbalanceado — F1 de Educação (n=2 no teste) é estatisticamente instável.
- **Label proxy** por órgão (~83% de concordância humana): erros estruturais (ex.: Bombeiros com objeto clínico) geram confusão Segurança ↔ Saúde.
- **Vazamento residual** (~49%) mesmo em `objeto_html` — optou-se conscientemente pela métrica honesta em vez do número inflado de ~0,88.
- Cobertura só **DF/2025** — não generaliza para o Brasil nem para outros anos.

---

## 7. Conclusão — contribuição principal

1. **Dados e pipeline inéditos e reprodutíveis** de transparência pública (ComprasNet DF 2025): coleta ética (sem CAPTCHA), corpus versionado com hash, rastreamento de experimentos.
2. **Evidência empírica com rigor metodológico:** num corpus pequeno, um baseline clássico bem construído (TF-IDF + LogReg, **F1 0,74**) pode **superar** um Transformer (BERTimbau, 0,40) — desde que se controle **vazamento de label**, se reporte o **teste** (não a validação) e se valide o rótulo com humanos.
3. **Ferramenta aplicada:** dado um edital, o sistema infere **área de gasto**, apoiando triagem e controle social.

> A contribuição não é "a melhor métrica", e sim **explicar o que a métrica significa, por que ela importa e o cuidado metodológico** por trás dela.

---

## 8. Próximos passos — melhorias e escala

- **Expandir o corpus no tempo (2021–2024):** classes raras mais estáveis e teste de **robustez temporal**.
- **Enriquecer com o PNCP** (já iniciado — 19.944 compras DF/2025).
- **Reduzir a classe "Outros"** revisando o mapeamento órgão→área.
- **Diferencial aplicado:** cruzar áreas previstas com **valor homologado** e **modalidade**.

---

## 9. Referências

**Técnica (PLN / Deep Learning / Transformers):**

1. DEVLIN, J. et al. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. **NAACL**, 2019.
2. SOUZA, F.; NOGUEIRA, R.; LOTUFO, R. BERTimbau: Pretrained BERT Models for Brazilian Portuguese. **BRACIS**, 2020.
3. SRIVASTAVA, N. et al. Dropout: A Simple Way to Prevent Neural Networks from Overfitting. **JMLR**, 2014.
4. GOODFELLOW, I.; BENGIO, Y.; COURVILLE, A. **Deep Learning**, cap. 10 (modelagem de sequências). MIT Press, 2016.

**Domínio (licitações, transparência, setor público, linguagem cidadã):**

1. SOUTO, A. de L.; GOMES, V. C.; RIVEROS, J. L. T. Inteligência Artificial em Auditoria de Licitações: o caso Alice na CGU e no TCU. **Revista Síntese**, v. 2, n. 1, 2025. DOI: 10.70690/f9axse22.
2. FERREIRA, H. H. **Processamento de linguagem natural e classificação de textos em sistemas modulares**. 2019. TCC (Bacharelado em Ciência da Computação) — Universidade de Brasília.
3. WATANABE, E.; SOUSA, R. T. B. de. Uso do aprendizado de máquina para a classificação automática de documentos de arquivo: experimento inicial em uma organização pública. **Tendências da Pesquisa Brasileira em Ciência da Informação**, v. 16, 2023.
4. MACEDO, J. M. A. et al. Avaliação de sistemas de governo aberto e de transparência pública nas capitais brasileiras. **Cadernos Gestão Pública e Cidadania (FGV)**, v. 30, n. 1, 2025. DOI: 10.12660/cgpc.v30.90832.
5. ROSADO, K. M. L.; DIAS, C. da C. Promovendo acessibilidade e compreensão na área da informação jurídica. **Ciência da Informação em Revista**, v. 11, e16631, 2024. DOI: 10.28998/cirev.2024v11e16631.

**Marco legal (fontes normativas):** Lei nº 14.133/2021 (Licitações) · Lei nº 12.527/2011 (LAI) + Decreto nº 8.777/2016 (dados abertos) · Lei nº 15.263/2025 (Política Nacional de Linguagem Simples).

---

*Fonte dos números: runs ComprasNet `20260624-*` e PNCP `classification_pncp*`. Detalhes em `docs/MODEL-CARD.md`, `docs/METRICAS-E-DECISOES.md` e `docs/COMPARATIVO-FASES.md`.*