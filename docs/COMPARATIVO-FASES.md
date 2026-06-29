# Comparativo das três fases — validação e teste

Notas do grupo para montar relatório e slides. A ideia é explicar o que aconteceu quando comparamos validação e teste nos três classificadores, e por que ficamos com o LogReg da Fase 1.

Runs que usamos: `experiments/classification_*_20260624-013*.json`. Detalhe de cada métrica em [`METRICAS-E-DECISOES.md`](METRICAS-E-DECISOES.md).

---

## O que todo mundo usou (pra não comparar laranja com banana)

Todos os modelos viram o mesmo corpus (423 editais), o mesmo campo `objeto_html`, o mesmo split 70/15/15 com `seed=42` — ou seja, 295 treino, 64 validação e 64 teste. A gente escolhe o modelo pelo **F1 macro no teste**, não pela validação.

Validação serve pra parar o treino do BERT (early stopping) e pra enxergar se o modelo “decorou” aquele pedaço dos dados. Teste é o número que vai pro relatório: ninguém mexeu em hiperparâmetro olhando pro teste.

---

## Resumo em uma tabela

| Fase | Modelo | F1 val | F1 teste | Caiu quanto? |
|------|--------|-------:|---------:|-------------:|
| 1 | TF-IDF + LogReg | 0,743 | 0,740 | quase nada (−0,003) |
| 3 | TF-IDF + SVM | 0,797 | 0,652 | bastante (−0,145) |
| 2 | BERTimbau | 0,559 | 0,400 | bastante (−0,159) |

O LogReg foi o único em que validação e teste contaram a mesma história. SVM e BERT pareciam melhores (ou diferentes) na val, mas não seguraram no teste.

---

## Fase 1 — LogReg (baseline)

Run: `classification_baseline_20260624-013836`

Na validação: F1 macro 0,743, accuracy 0,766.  
No teste: F1 macro 0,740, accuracy 0,797.

Isso é o que a gente queria ver: o modelo não “quebrou” quando mudou o conjunto. Faz sentido — é TF-IDF com regressão logística, modelo simples pro tamanho do corpus. Palavras como “material hospitalar” ou “abastecimento de água” pesam bastante e o `class_weight=balanced` ajuda nas classes menores sem exagerar.

Onde ainda erra (val e teste):

- **Segurança** — F1 ~0,36–0,46. Muita confusão com Administração/Outros; o texto do objeto nem sempre fala em polícia/bombeiro.
- **Educação** — no teste só tem **2** editais; um erro já derruba o F1.
- **Infraestrutura** — poucos exemplos; F1 oscila.

Saúde e Saneamento vão bem (F1 ≥ 0,90 no teste).

**Conclusão:** melhor F1 macro no teste entre os três. Por isso é o modelo que o grupo reporta como principal.

---

## Fase 3 — SVM

Run: `classification_svm_20260624-013851`

Aqui ficou curioso. Na validação o SVM foi **melhor** que o LogReg (F1 macro 0,797 contra 0,743). No teste, caiu pra 0,652 — abaixo do LogReg (0,740).

A accuracy no teste ficou 0,797, **igual** à da validação. Ou seja: acertou a mesma proporção de editais, mas errou mais nas classes pequenas. O F1 macro capta isso; accuracy esconde.

O que aconteceu na prática:

- **Educação:** na val tinha 3 exemplos e acertou tudo (F1 1,0). No teste são 2 e errou os dois (F1 0).
- **Infraestrutura:** na val foi melhor que o LogReg (0,80 vs 0,50); no teste ainda ganha um pouco (0,75 vs 0,60), mas não compensa o resto.
- **Segurança:** parecido com o LogReg — problema do corpus/label, não do algoritmo em si.

Mesmo TF-IDF do baseline; só mudou o classificador. Parece que a fronteira do SVM linear se ajustou demais aos 64 editais de validação.

**Conclusão:** bom experimento comparativo, mas não substitui o LogReg. Não escolheríamos um modelo só porque a validação foi 0,80.

---

## Fase 2 — BERTimbau

Run atual: `classification_bertimbau_20260624-013908`

Validação: F1 macro 0,559. Teste: 0,400. Gap grande.

Quando retreinamos, o BERT **piorou no teste** em relação a um run anterior (`222508`: teste 0,518), mas **melhorou na validação** (0,559 vs 0,425). Mesmo `seed`, mesmo split — o fine-tuning não sai idêntico toda vez. O early stopping escolheu um checkpoint bom pra val, não pro teste.

No teste o BERT praticamente ignora algumas classes:

| Classe | F1 teste |
|--------|----------|
| Segurança (9 editais) | 0,00 |
| Educação (2) | 0,00 |
| Infraestrutura (4) | 0,00 |

Saúde e Saneamento ainda ok (~0,80–0,88). O modelo empurra muita coisa pra Administração/Outros (recall 0,96).

Com ~295 exemplos de treino e dezenas de milhões de parâmetros, era esperado que o Transformer não brilhasse aqui. A hipótese do trabalho era testar se o BERT ganhava do clássico — no nosso corpus, **não ganhou** (ficou entre 0,40 e 0,52 nos runs que rodamos, contra 0,74 do LogReg).

**Conclusão:** entra no relatório como comparativo de deep learning, não como modelo escolhido.

---

## Teste — F1 por classe nos três modelos

| Área | n | LogReg | SVM | BERT |
|------|--:|-------:|----:|-----:|
| Saúde | 17 | 0,90 | 0,90 | 0,88 |
| Saneamento | 7 | 1,00 | 1,00 | 0,80 |
| Segurança | 9 | 0,46 | 0,46 | 0,00 |
| Educação | 2 | 0,67 | 0,00 | 0,00 |
| Infraestrutura | 4 | 0,60 | 0,75 | 0,00 |
| Administração/Outros | 25 | 0,81 | 0,80 | 0,73 |

Só o LogReg manteve F1 acima de zero em todas as áreas no teste.

---

## O que colocar na apresentação

Texto que a gente costuma usar:

> Treinamos três classificadores no mesmo split e na mesma entrada (`objeto_html`). LogReg: validação 0,74, teste 0,74. SVM: validação 0,80, teste 0,65. BERT: validação 0,56, teste 0,40. Ficamos com o LogReg porque o teste é o que importa e ele foi o mais estável.

Limitações que aparecem nos três (não é bug no código):

- Label vem do órgão, não de anotação manual — validamos 30 editais e a concordância média ficou ~83%.
- Classes raras (Educação com 2 no teste) deixam o F1 instável.
- Usamos `objeto_html` de propósito, mesmo sabendo que ainda tem vazamento residual (~49%); com `texto` o F1 sobe pra ~0,88 mas aí o modelo “cola” no nome do órgão.

---

Atualizado em jun/2026 — runs `013836`, `013851`, `013908`.
