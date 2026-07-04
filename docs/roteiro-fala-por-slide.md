# Roteiro de Fala por Slide
**PLN aplicado a Editais de Licitação Pública · DF 2025**  
**Deep Learning e PLN · Modalidade 2 — PLN no Setor Público**

> Ritmo: ~140 palavras/min. Tempo ao lado do slide = marcador acumulado no ensaio.  
> Navegação: teclas ← → ou botões no rodapé do `apresentacao-final.html`.

---

## CAPA · [0:00 → 0:30]

**Alexandre Ponte**

> "Boa tarde. Somos o grupo da Modalidade 2 — PLN no Setor Público. O nosso projeto parte de um problema concreto de transparência pública: o governo do Distrito Federal publicou 423 editais de licitação em 2025. Cada um descreve uma compra em linguagem jurídica. Para um cidadão ou órgão de controle saber em que área cada gasto se encaixa — Saúde, Obras, Segurança — é preciso ler cada texto manualmente. Isso é inviável. Aplicamos PLN para automatizar essa triagem."

---

## SLIDE 1 — Contexto · [0:30 → 1:30]

**Alexandre Ponte**

> "O campo central de cada edital é o Objeto: um texto livre em jargão jurídico-administrativo, descrevendo o que o governo quer comprar. De 'antimetabólitos oncológicos' a 'tubos de PVC' ou 'digitalização de processos'.
>
> Para um jornalista ou órgão de controle, responder 'quanto o DF gastou em Saúde este ano?' exige ler centenas dessas descrições uma a uma — inviável. Para o pequeno fornecedor, esse jargão afasta exatamente quem o edital deveria alcançar.
>
> Nosso projeto aplica PLN para classificar automaticamente cada edital por área de gasto — para que qualquer pessoa saiba em que o DF está comprando, sem ter que ler centenas de textos em jargão jurídico."

---

## SLIDE 2 — Base Teórica · [1:30 → 2:15]

**Alexandre Ponte**

> "A base teórica tem duas frentes — cinco referências técnicas e cinco de domínio, usadas de forma substantiva, não só listadas.
>
> Na frente técnica: o BERT de Devlin et al. para fine-tuning de Transformers; o BERTimbau de Souza et al., pré-treinado em português brasileiro — escolhemos o modelo PT-BR em vez do multilíngue genérico. E o lema da aula 03–04: 'a arquitetura certa depende do volume de dados e do diagnóstico treino versus teste' — esse lema vai aparecer diretamente nos nossos resultados.
>
> Na frente de domínio: o caso Alice, sistema da CGU e TCU que usa IA para triagem de licitações em escala nacional; estudos de classificação de documentos públicos; e o marco legal — Lei 14.133/2021, a Lei de Acesso à Informação e a Lei 15.263/2025."

---

## SLIDE 3 — Dados · [2:15 → 3:00]

**Alexandre Ponte**

> "Os dados são inéditos — a disciplina proíbe bases prontas como Kaggle. Coletamos de duas fontes, ambas do Distrito Federal em 2025.
>
> ComprasNet, nossa entrega oficial: 423 editais em HTML de detalhe. Tomamos uma decisão ética imediata: o PDF completo de cada edital está protegido por CAPTCHA. Em vez de automatizar o contorno, coletamos o HTML aberto — com intervalo de 0,8 segundo entre requisições, User-Agent identificando o projeto acadêmico, e hash SHA-256 versionado no repositório.
>
> PNCP, nossa extensão em escala: 19.944 compras via planilha da API oficial — sem CAPTCHA, reprodutível.
>
> O rótulo é um proxy: mapeamos o órgão comprador para seis macroáreas por palavras-chave. O classificador nunca recebe o órgão — só o texto do objeto. Validamos à mão 30 editais, quatro fichas por integrante. Concordância média: cerca de 83%. E declaramos as limitações: corpus pequeno e desbalanceado no ComprasNet, e aproximadamente 48% dos objetos do PNCP não têm keyword setorial clara."

---

## SLIDE 4 — Vazamento de label + Protocolo · [3:00 → 4:15]

**Renê Deckers**

> "Antes dos modelos, a decisão metodológica mais importante do trabalho: o vazamento de label.
>
> O rótulo vem do órgão — Secretaria de Saúde vira classe Saúde. Se dermos ao modelo o texto completo de cada edital, o F1 sobe para cerca de 0,88. Número tentador de reportar. Mas em 97% dos casos o HTML completo repete o nome do órgão ou a keyword da área. O modelo não aprende o que está sendo comprado — ele cola na resposta. Isso é vazamento de label.
>
> Por isso nossa entrada oficial é só o campo Objeto. O vazamento cai para 49 a 51 por cento. Preferimos o 0,74 honesto ao 0,88 contaminado.
>
> O protocolo é idêntico para os três modelos: split 70 / 15 / 15, estratificado por área, seed 42 — resultando em 295, 64 e 64 editais no ComprasNet. A métrica primária é o F1 macro no teste — porque acurácia isolada engana: um modelo que chuta sempre 'Administração/Outros' pode ter 40% de acerto sem aprender nada de Saúde ou Educação. Olhamos a validação durante o desenvolvimento, mas reportamos sempre o teste. Cada run vai para JSON e MLflow, com hash do corpus e commit Git."

---

## SLIDE 4b — Família de arquiteturas · [4:15 → 5:00]

**Renê Deckers**

> "Três modelos, duas famílias. Mesmo split, mesma entrada — só muda a arquitetura.
>
> Família clássica, sem rede neural: TF-IDF mais LogReg — nosso oficial — e TF-IDF mais SVM, mesmo vetor, classificador diferente. Família deep learning: BERTimbau, Transformer pré-treinado em português.
>
> Não usamos CNN — é para imagem, não texto livre. Não usamos LSTM — o estado da arte em PLN é Transformer; seria redundante com o BERT.
>
> Hipótese: Transformer vence. ComprasNet: não. PNCP em escala: sim. O 'depende' da aula."

---

## SLIDE 5 — Resultados ComprasNet · [5:00 → 6:30]

**Alexandre Hugo**

> "Chegamos aos resultados no corpus oficial — 64 editais de teste que nenhum modelo viu durante o treino.
>
> O LogReg venceu com F1 macro 0,740. Pode parecer contraintuitivo — o deep learning perdeu. Mas olhem o padrão no gráfico: o SVM teve F1 0,80 na validação e caiu para 0,652 no teste. O BERTimbau foi de 0,559 para 0,400. Ambos se ajustaram demais aos 64 editais de validação. O LogReg manteve 0,743 na validação e 0,740 no teste — praticamente o mesmo número. Isso é generalização.
>
> Olhando por classe no LogReg: Saneamento com F1 1,00 — vocabulário único como 'abastecimento de água' e 'CAESB'. Saúde com 0,90 — mais exemplos, mais estável. O problema está em Segurança, com F1 0,46: Bombeiros que compram material hospitalar recebem label 'Segurança', mas o objeto fala de 'material clínico'. O modelo confunde com Saúde. Isso é uma limitação estrutural do label proxy, não do algoritmo.
>
> No BERTimbau, as classes raras — Segurança, Educação e Infraestrutura — tiveram F1 zero no teste: com 110 milhões de parâmetros e 295 exemplos de treino, o modelo convergiu para prever quase só 'Administração/Outros'."

---

## SLIDE 6 — PNCP + Protocolos · [6:30 → 7:45]

**Alexandre Hugo**

> "A pergunta natural após os resultados com 423 editais: e com muito mais dado?
>
> Entra o PNCP: 19.944 compras, protocolo honesto — mesmas seis macroáreas, label por órgão, mesma honestidade metodológica. Com cerca de 14 mil exemplos de treino, o BERT alcança F1 0,858, superando o LogReg em mais de 10 pontos percentuais. O resultado se inverte completamente.
>
> Isso confirma o diagnóstico: o BERT não é inferior — ele precisava de mais dados. Com 295 exemplos, overfitting severo. Com 14 mil, ele aprende.
>
> Também testamos protocolos exploratórios com 9 setores empíricos — pncp9, pncp9full, pncp9fbi — onde o BERT atinge F1 de até 0,97. Mas declaramos a ressalva: nesses protocolos, o label é construído a partir de keywords que aparecem no próprio objeto. Parte do F1 alto reflete acoplamento rótulo e texto, não generalização. Não confundir 0,97 exploratório com 0,858 honesto.
>
> Três números para a banca: 0,740 no ComprasNet com LogReg, nossa entrega oficial; 0,858 no PNCP com BERT, protocolo honesto; e 0,97 nos exploratórios, com a ressalva declarada."

---

## SLIDE 7 — Discussão · [7:45 → 8:45]

**Elisangela**

> "Limites e vieses — declarados, não escondidos. Esse slide diferencia rigor metodológico de enfeite.
>
> Primeiro: label proxy com cerca de 83% de concordância. Quando o órgão é 'Bombeiros' mas o objeto é material clínico, o rótulo vira Segurança e o modelo confunde com Saúde. Erro estrutural do mapeamento — não do algoritmo.
>
> Segundo: vazamento residual de 49 a 51 por cento. Keywords de domínio legítimas, como 'material hospitalar', aparecem no objeto. O F1 é honesto, mas não é puro — e declaramos.
>
> Terceiro: classes raras no ComprasNet. Educação com 2 exemplos no teste, Infraestrutura com 4. F1 instável estatisticamente — um erro já derruba a métrica pela metade.
>
> Quarto: PNCP e ComprasNet têm perfis distintos. Textos curtos, inexigibilidade dominante, 48% sem keyword clara. O modelo não generaliza automaticamente entre os dois corpora.
>
> E documentamos os runs negativos — BERT com F1 0,40. Erro faz parte do aprendizado científico. O classificador não substitui análise jurídica."

---

## SLIDE 8 — Conclusão + Próximos passos · [8:45 → 10:00]

**Elisangela**

> "Três contribuições.
>
> Uma: pipeline inédito, ético e reprodutível — ComprasNet mais PNCP, coleta sem burlar CAPTCHA, scripts no GitHub, hash versionado, runs rastreáveis no MLflow.
>
> Duas: evidência empírica de que volume e protocolo mudam o melhor modelo. Clássico linear vence com 423 editais. Transformer vence com 20 mil. Demonstramos o 'depende' da aula na prática — com a hipótese refutada no corpus pequeno e confirmada em escala.
>
> Três: ferramenta de triagem por área de gasto para transparência pública — dado um edital, a área predita automaticamente.
>
> Próximos passos claros: expandir o ComprasNet para 2021–2024, chegando a 2 a 2,5 mil editais; cruzar a área predita com o valor homologado, transformando o classificador em ferramenta de política pública; e avaliar o modelo no PNCP de outros estados — a infraestrutura já está pronta.
>
> Repositório público, dados via código, slides em PDF. Obrigado."

---

## FECHAMENTO (tela final)

> *Sem fala — a frase fica na tela durante as perguntas.*  
> "A contribuição não é a melhor métrica. É a mais honesta."

---

---

## Respostas para perguntas frequentes da banca

**"Por que 0,74 e não 0,88?"**
> "0,88 é colagem — o modelo aprendeu o nome do órgão, não o conteúdo da compra. 0,74 mede o que o classificador realmente aprendeu. Para uso real em transparência pública, 0,88 seria uma ilusão."

**"Por que não usaram LSTM?"**
> "LSTM foi o estado da arte antes dos Transformers. Incluir seria redundante — queríamos testar o eixo Transformer vs clássico linear, que é o foco pedagógico da disciplina. O BERT supera LSTM na maioria das tarefas de classificação textual."

**"Por que não usaram CNN?"**
> "CNN é arquitetura para dados em grade — imagens. Para texto livre como editais, o Transformer é o padrão atual. Convolução 1D em texto existe, mas não é o que o curso enfatiza para classificação de documentos."


**"83% de concordância é suficiente?"**
> "É aceitável para um baseline acadêmico, e declaramos como limitação. Os 17% de discordância estão concentrados em casos estruturais — órgão de segurança comprando material de saúde. Isso explica parte da confusão Segurança↔Saúde no modelo."

**"Por que o F1 de Educação com 2 exemplos?"**
> "É estatisticamente instável — um erro já derruba a métrica pela metade. O SVM fez F1 zero em Educação com os mesmos 2 exemplos. O resultado de Educação não é conclusivo e declaramos isso explicitamente."

**"F1 0,97 no pncp9 não seria melhor para a entrega?"**
> "Não. 0,97 reflete reprodução de regras de keyword — label e texto se retroalimentam. Para uma ferramenta real de transparência, o protocolo honesto com 0,858 é o número relevante. Os exploratórios estão no relatório como extensão, não como resultado principal."
