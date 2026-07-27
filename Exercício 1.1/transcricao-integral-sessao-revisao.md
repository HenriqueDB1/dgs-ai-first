> Nota: os blocos de análise enviados pelo usuário continham cercas de código de três crases (```). Para preservá-los na íntegra dentro deste export, eles foram envolvidos em cercas de quatro crases (````). Nenhum caractere do conteúdo foi alterado, removido ou resumido.

---

## Turno 1 — Usuário

Você é um revisor técnico especialista em arquitetura de IA e RAG. 
Vou te enviar uma análise técnica de viabilidade produzida por outro analista.
Sua tarefa é revisá-la criticamente.

## Contexto do projeto
A NovaTech é uma empresa de logística com 1.200 funcionários. Fomos contratados para construir um assistente de IA que permita à equipe de atendimento (45 pessoas) consultar documentação interna em linguagem natural, com indicação de fonte. A documentação está em três fontes: SharePoint (~800 PDFs), Confluence (~400 páginas wiki) e planilhas (~50 arquivos). O problema atual é que cada chamado consome ~12 minutos de busca manual; a meta é reduzir para menos de 2 minutos.
Detalhes técnicos relevantes:
- PDFs incluem tabelas complexas (15+ colunas), fluxogramas como imagem e documentos escaneados (OCR necessário)
- Wiki usa macros customizadas e links internos entre páginas
- Planilhas têm fórmulas interdependentes
- Alguns documentos se contradizem entre versões
- Stack disponível: Microsoft 365 E3 + Azure AI Services
- Modelo de referência: GPT-4o (128K tokens de janela)

## O que a análise deveria cobrir
- **Bloco 1:** Desafios por tipo de fonte e estratégia de tratamento
- **Bloco 2:** Estimativa de tamanho da base em tokens
- **Bloco 3:** Análise de orçamento de contexto por query
- **Bloco 4:** Estratégia de chunking justificada pelo tipo de pergunta e pelo efeito *lost in the middle*

## Sua tarefa
Revise a análise abaixo e identifique:
- Pontos fracos na argumentação
- Estimativas otimistas demais ou sem justificativa suficiente
- Riscos técnicos que não foram considerados
- Inconsistências internas entre os blocos
Seja direto e crítico. Não elogie o que está bom — foque no que pode melhorar ou está errado.

## Análise a revisar

````markdown
# Análise Técnica de Viabilidade — Assistente de IA com RAG para a NovaTech

**Cliente:** NovaTech (logística, 1.200 funcionários)
**Escopo:** Assistente de IA com RAG sobre documentação interna, integrado a Teams + SharePoint
**Stack alvo:** Microsoft 365 E3 + Azure AI Services, modelo GPT-4o (janela de 128K tokens)
**Data:** Junho de 2026

---

## Premissas e estimativas adotadas

Onde a NovaTech não forneceu números, adoto as estimativas abaixo e justifico cada uma. Elas são usadas de forma consistente em todos os blocos.

| Parâmetro | Valor adotado | Justificativa |
|---|---|---|
| Palavras por página de PDF | 500 | Página A4 com corpo de texto técnico, espaçamento normal e algumas tabelas/figuras fica entre 400–600 palavras. 500 é o ponto médio conservador usado pela indústria editorial. |
| Palavras por página de wiki | 1.500 | Valor **fornecido** pela NovaTech. |
| Tamanho médio por planilha | ~4.000 "palavras-equivalentes" | Planilhas de referência (frete, SLA) têm muitas células curtas (números, códigos). Estimo ~200 linhas úteis × 15 colunas = 3.000 células; somando cabeçalhos, abas auxiliares e fórmulas serializadas em texto, chego a ~4.000 tokens-equivalentes/planilha. É uma aproximação grosseira porque planilha não vira texto linearmente. |
| Conversão palavra→token | tokens = palavras ÷ 0,75 | Regra prática **fornecida**: ~0,75 palavra por token. Para português, que tokeniza pior que inglês, isso é otimista — o real tende a ser maior. |
| Reserva de saída (resposta) | ~4K tokens | Resposta fundamentada com citação de fontes raramente passa de 2–4K tokens. |
| Reserva de histórico de conversa | ~6K tokens | Permite 3–5 turnos de diálogo antes de truncar/resumir. |

---

## Bloco 1 — Desafios por tipo de fonte

O pipeline de RAG só é tão bom quanto o pior estágio de ingestão. Cada fonte da NovaTech quebra o pipeline em um ponto diferente: a extração, o chunking ou a fidelidade semântica do chunk.

### PDFs com tabelas complexas

**Desafio.** Extratores de texto de PDF leem o documento por coordenadas de caractere, não por estrutura lógica. Uma tabela de frete com 15+ colunas vira uma sequência linear de números sem cabeçalho associado — a relação "esta célula pertence à coluna *Região Sudeste* e à linha *carga acima de 100kg*" se perde. Quando esse texto é fatiado em chunks, um chunk pode conter valores numéricos órfãos de seus rótulos.

**Impacto na resposta.** É o pior tipo de erro possível: o modelo recupera um chunk *aparentemente relevante*, mas com a estrutura destruída ele associa o número errado à pergunta. O atendente recebe uma tarifa de frete plausível e errada, com citação de fonte legítima — um erro silencioso e de alto risco em logística.

**Estratégia recomendada.** Usar parsing com reconhecimento de layout (Azure AI Document Intelligence, modelo de *layout*/*tables*) em vez de extração de texto plana. As tabelas devem ser extraídas como estrutura e convertidas em Markdown ou HTML preservando cabeçalhos, e cada linha deve ser "achatada" em sentenças autocontidas no momento do chunking (ex.: "Frete para Sudeste, carga 50–100kg, cliente Premium: R$ X"). Cada chunk de tabela precisa carregar os cabeçalhos repetidos. Para as tabelas mais críticas (frete, SLA), considerar não confiar no RAG textual e sim expor a planilha-fonte via *function calling* (ver planilhas, abaixo).

### PDFs escaneados (OCR necessário)

**Desafio.** Documentos escaneados são imagens; não há texto a extrair. É preciso OCR antes de qualquer indexação. OCR introduz erros de caractere (0/O, 1/l, vírgula/ponto em valores monetários) e perde completamente a estrutura de tabelas e fluxogramas.

**Impacto na resposta.** Erros de OCR em valores numéricos são especialmente perigosos em frete e SLA. Além disso, conteúdo não-OCRizado simplesmente não existe para o retriever — a resposta fica incompleta sem que ninguém perceba a lacuna.

**Estratégia recomendada.** OCR via Azure AI Document Intelligence (que combina OCR + detecção de layout num só passo). Estabelecer um *threshold* de confiança do OCR: páginas abaixo do limiar entram em fila de revisão humana em vez de irem direto ao índice. Como discovery, levantar quantos dos 800 PDFs são realmente escaneados — esse número muda o esforço e o risco do projeto. Idealmente, negociar com Operações/Compliance a substituição dos escaneados críticos por versões digitais nativas.

### Wiki Confluence (links internos e macros customizadas)

**Desafio.** Páginas de wiki não são autocontidas: o sentido depende de páginas linkadas ("ver procedimento X"). Macros customizadas (tabelas dinâmicas, inclusões de outras páginas, *status labels*) ou são exportadas como código bruto da macro — poluindo o chunk — ou são silenciosamente omitidas, removendo conteúdo real.

**Impacto na resposta.** Chunks com lixo de macro desperdiçam orçamento de contexto e confundem o embedding. Páginas que dependem de links viram respostas parciais ("o procedimento está descrito em outra página" — sem dizer qual).

**Estratégia recomendada.** Ingerir via API REST do Confluence (que resolve grande parte das macros para conteúdo renderizado) em vez de raspar HTML. Mapear os tipos de macro presentes e tratar os mais comuns explicitamente; descartar as decorativas. Preservar os links como metadados do chunk para permitir recuperação em grafo (puxar a página linkada quando relevante). Incluir no metadado o título da página e a hierarquia (breadcrumb) para dar contexto a chunks curtos.

### Planilhas com fórmulas interdependentes

**Desafio.** Uma planilha não é documento de texto: é uma base de dados com lógica de cálculo. Uma célula pode conter `=VLOOKUP(...)` cujo valor só existe em tempo de cálculo. RAG textual sobre o "texto" de uma planilha captura rótulos e valores estáticos, mas **não** a lógica das fórmulas — e é justamente a regra de cálculo de frete que o atendente quer.

**Impacto na resposta.** Tentar responder "qual o frete para X?" via chunks de texto da planilha tende a recuperar um valor desatualizado ou a célula errada. Como as planilhas são atualizadas mensalmente, o índice fica defasado entre re-ingestões.

**Estratégia recomendada.** Tratar planilhas de cálculo de forma diferente das fontes textuais. Para tabelas de referência (SLA por cliente, faixas de frete), extrair os valores calculados em tempo de ingestão e indexar cada linha como um fato autocontido. Para regras de cálculo dinâmicas, o caminho mais robusto é **não** usar RAG e sim expor a planilha/serviço de cálculo como uma *tool* (function calling): o assistente chama a função de cálculo de frete com os parâmetros do cliente e recebe o valor correto e atual. Reservar RAG para o "como/por quê" (políticas) e *tools* para o "quanto" (números exatos).

---

## Bloco 2 — Estimativa de tamanho da base em tokens

Cálculos explícitos, na ordem fontes → palavras → tokens (tokens = palavras ÷ 0,75).

**PDFs do SharePoint**
- 800 documentos × 10 páginas/doc = 8.000 páginas
- 8.000 páginas × 500 palavras/página = **4.000.000 palavras**
- 4.000.000 ÷ 0,75 = **5.333.333 tokens**

**Wiki Confluence**
- 400 páginas × 1.500 palavras/página = **600.000 palavras**
- 600.000 ÷ 0,75 = **800.000 tokens**

**Planilhas de referência**
- 50 planilhas × ~4.000 palavras-equivalentes = **200.000 palavras**
- 200.000 ÷ 0,75 = **266.667 tokens**

**Total da base de conhecimento**

| Fonte | Palavras | Tokens |
|---|---:|---:|
| PDFs (SharePoint) | 4.000.000 | 5.333.333 |
| Wiki (Confluence) | 600.000 | 800.000 |
| Planilhas | 200.000 | 266.667 |
| **Total** | **4.800.000** | **≈ 6.400.000 (6,4M tokens)** |

**Leitura do número.** A base inteira (~6,4M tokens) é **50× maior** que a janela de 128K do GPT-4o. Isso elimina de saída qualquer abordagem de "jogar tudo no contexto" e confirma que RAG (recuperar apenas os trechos relevantes) é arquiteturalmente obrigatório, não opcional. Em embeddings, a 6,4M tokens com chunks de 500 tokens, falamos de aproximadamente **12.800 chunks** no índice vetorial — volume modesto, perfeitamente atendido por Azure AI Search. Ressalva: em português a contagem real de tokens tende a ser 15–30% maior que a regra de 0,75; trate 6,4M como piso, não teto.

---

## Bloco 3 — Análise de orçamento de contexto

**Janela total disponível (GPT-4o):** 128.000 tokens.

Cálculo do orçamento, descontando o que compete por atenção antes dos chunks:

```
Janela total                         128.000
(-) System prompt + instruções        -2.000
(-) Reserva p/ resposta do modelo      -4.000
(-) Reserva p/ histórico de conversa   -6.000
---------------------------------------------
= Orçamento p/ chunks recuperados     116.000 tokens
```

**Quantos chunks de 500 tokens cabem?**
- Teto absoluto e ingênuo (só descontando o system prompt): (128.000 − 2.000) ÷ 500 = **252 chunks**
- Teto realista (descontando saída e histórico): 116.000 ÷ 500 = **232 chunks**

**Por que NÃO se deve usar esse teto.** O fato de caberem ~230 chunks não significa que se deva enviá-los. Três forças puxam o número ótimo para baixo:

1. **Lost in the middle.** Modelos atendem melhor ao início e ao fim do prompt; informação enterrada no meio de um contexto longo é efetivamente "esquecida". Encher a janela com 200 chunks faz com que o chunk decisivo, se cair no meio, seja ignorado mesmo estando presente.
2. **Diluição de relevância.** Recuperação tem cauda longa: os primeiros chunks são muito relevantes, os demais cada vez menos. Adicionar chunks de baixa relevância introduz ruído e distratores que pioram a resposta, além de aumentar o risco de o modelo citar a fonte errada.
3. **Custo e latência.** Cada token enviado é pago e processado. 116K tokens por query, em 320 chamados/dia × 60% = ~190 queries/dia, é desperdício de ordem de magnitude sobre o necessário.

**Recomendação de orçamento operacional.** Recuperar um conjunto amplo de candidatos (ex.: top-30 a top-50 no vetor), aplicar *reranking* e enviar ao modelo apenas os **8 a 15 chunks** mais relevantes (≈ 4K–7,5K tokens). Isso mantém a janela folgada, reduz lost-in-the-middle e corta custo, sem sacrificar recall — porque o reranker, não a janela, faz a seleção fina.

**Efeito sobre chunking e retrieval.** Como o gargalo não é "quanto cabe" e sim "qual a qualidade do que enviamos", o esforço de engenharia migra do tamanho da janela para: (a) qualidade do chunk (autocontido, com cabeçalhos e metadados), (b) um estágio de reranking, e (c) posicionamento — colocar os chunks de maior score nas extremidades do prompt.

---

## Bloco 4 — Estratégia de chunking recomendada

A estratégia deve ser ditada pelo **tipo de pergunta do atendente** e mitigar o **lost in the middle**.

**Perfil das perguntas.** Os atendentes perguntam coisas factuais e pontuais: "qual o prazo de entrega para cliente Premium na região Sul?", "qual o procedimento para registrar uma reclamação de avaria?", "a política de devolução cobre produto sem nota?". São perguntas que se respondem com **um trecho específico e bem delimitado** — um parágrafo de política, uma linha de tabela de SLA, um passo de procedimento. Não são perguntas que exigem sintetizar um documento inteiro. Isso favorece chunks **menores e precisos** em vez de chunks grandes e abrangentes.

**Estratégia recomendada: chunking semântico, consciente de estrutura, com sobreposição e enriquecido por metadados.**

1. **Respeitar fronteiras estruturais (não fatiar cegamente por N caracteres).** Quebrar por seções/cabeçalhos do documento, itens de procedimento e linhas de tabela. Um passo de procedimento ou uma linha de SLA deve ficar inteiro em um chunk — nunca partido ao meio. Isso casa diretamente com o formato das respostas que o atendente precisa.

2. **Tamanho-alvo de ~500 tokens com sobreposição (overlap) de ~10–15%.** 500 tokens é grande o bastante para conter um parágrafo de política com seu contexto e pequeno o bastante para ser preciso e barato. A sobreposição evita que uma resposta seja cortada exatamente na fronteira entre dois chunks.

3. **Cada chunk autocontido + metadados ricos.** Anexar a cada chunk: título do documento, seção/breadcrumb, fonte (SharePoint/Confluence/planilha), data da última atualização e área responsável (Operações/Compliance/Comercial). Para chunks de tabela, repetir os cabeçalhos das colunas dentro do texto. Metadados habilitam filtragem (ex.: só políticas de Compliance vigentes) e, crucialmente, a **citação de fonte** exigida pela NovaTech.

4. **Posicionamento contra lost in the middle.** Após reranking (Bloco 3), ordenar os chunks no prompt de modo que os de maior relevância ocupem o **topo e a base** do bloco de contexto, deixando os de menor score no meio. Manter o conjunto enxuto (8–15 chunks) para que praticamente não exista "meio" perigoso.

5. **Resolver contradições entre versões — problema específico da NovaTech.** Como os documentos se contradizem entre versões e três áreas atualizam sem revisão unificada, o chunking sozinho não basta. Usar o metadado de data/versão para, em empate de relevância, priorizar o documento **vigente**; e instruir o modelo a sinalizar quando duas fontes conflitam ("há divergência entre o documento A (jan) e B (mai)") em vez de escolher arbitrariamente. Isso transforma a fragilidade atual ("perguntar para quem sabe") em um alerta explícito.

**Por que não chunks grandes (ex.: 2.000 tokens)?** Chunks grandes inflam o prompt, agravam o lost in the middle e misturam vários assuntos num só bloco, reduzindo a precisão da citação — exatamente o oposto do que o perfil de perguntas pontuais da NovaTech exige.

---

## Síntese da viabilidade

O projeto é **viável** dentro de 3 meses e do stack Microsoft/Azure, com duas ressalvas que devem ser endereçadas no discovery: (1) o risco está na **ingestão**, não no modelo — tabelas de frete, escaneados e planilhas de cálculo são onde a qualidade se ganha ou se perde, e exigem tratamento diferenciado (Document Intelligence + *function calling* para números exatos); (2) a falta de processo unificado de revisão e as contradições entre versões são um risco de **governança de conteúdo** que a arquitetura mitiga (metadados de vigência + sinalização de conflito), mas não resolve sozinha — a NovaTech precisará de um dono do processo de atualização para sustentar a meta de reduzir a busca de 12 para menos de 2 minutos.
````

---

## Turno 2 — Claude

Revisão crítica, organizada pelas quatro categorias que você pediu.

## Estimativas otimistas ou sem justificativa

**O "10 páginas/doc" não existe na tabela de premissas, mas sustenta 83% da base.** Todo o número de PDFs (5,33M tokens) sai de `800 × 10 páginas × 500 palavras`. A premissa de 500 palavras/página está justificada; a de 10 páginas/documento — que é a mais sensível das duas — aparece do nada no Bloco 2. Logística mistura procedimentos de 2 páginas com manuais e tabelões de 40+. Sem essa premissa explícita e justificada, o "6,4M tokens" é um chute com aparência de cálculo.

**500 palavras/página ignora o que a própria análise disse no Bloco 1.** Uma página que é um fluxograma-imagem ou uma tabela de 15 colunas tem ~0 palavras extraíveis de texto corrido, mas entra contando 500. Já uma página densa de tabela pode virar 1.000+ "valores". A média editorial de 500 não se aplica a um corpus que a análise mesma classificou como cheio de tabelas, escaneados e imagens.

**O `320 chamados/dia × 60% = ~190 queries/dia` do Bloco 3 é inventado.** Nenhum desses três números (320, 60%, e portanto 190) vem do briefing. O briefing dá 45 pessoas e 12 min/chamado, nada de volume diário. Como o argumento de custo depende desse volume, ele fica sem chão.

**A ressalva do português é levantada e depois ignorada.** A análise reconhece que PT tokeniza 15–30% pior e diz "trate 6,4M como piso". Mas mantém 6,4M como número-título e não propaga o ajuste para nada. Se o real é 7,5–8,3M, muda custo de embeddings e de Document Intelligence — deveria ter usado o multiplicador maior, não só sinalizado.

## Pontos fracos na argumentação

**O perfil de perguntas "factuais e pontuais" é assumido, não validado — e é a base de todo o Bloco 4.** Toda a estratégia de chunking (chunks pequenos, 8–15 trechos) decorre da afirmação de que ninguém faz pergunta agregativa. Mas "quais clientes Premium têm SLA acima de X?" ou "liste os procedimentos alterados em maio" são perguntas plausíveis de atendimento e exigem muitos chunks — 8–15 não cobrem. Isso precisa sair de log de queries real, não de suposição.

**"Sem sacrificar recall — porque o reranker faz a seleção fina" confunde recall com precisão.** Recall é determinado pelo retrieval inicial (top-30 a top-50). Se o chunk certo não está nesses 50, nenhum reranker o recupera. Mandar 8–15 ao LLM em vez de 50 melhora precisão/posição, mas o risco de recall mora no tamanho do candidate set, não na janela. A frase está solta e mascara o ponto real.

**A priorização do "documento vigente" por data é um proxy fraco.** Data de última modificação ≠ versão autoritativa. Um documento mais antigo pode ser o oficial; um recém-tocado pode ser rascunho. Resolver contradição por `max(data)` vai escolher errado em alguns casos.

**A sinalização de conflito só funciona se as duas versões forem recuperadas juntas — e o resto do pipeline foi desenhado para não fazer isso.** O Bloco 3 afina para mandar só o top relevante; o Bloco 4 quer que o modelo avise "há divergência entre A e B". Se o reranker mandar só a versão A, não há conflito a sinalizar. Isso exige dedupe/clustering por documento *antes* do top-k, o que não foi previsto.

**Excesso de engenharia contra lost-in-the-middle.** A análise dá peso enorme ao efeito e ao posicionamento topo/base, e na mesma seção admite que com 8–15 chunks "praticamente não existe meio perigoso". As duas coisas não podem ser verdade ao mesmo tempo — ou o problema é central, ou a recomendação já o neutralizou. Em 7,5K tokens dentro de 128K num GPT-4o, é quase não-problema.

## Riscos técnicos não considerados

**Permissões/ACL — ausência grave.** São 1.200 funcionários e o SharePoint tem permissões por documento. Um índice vetorial achata isso por padrão e pode expor ao atendimento conteúdo restrito (RH, jurídico, contratos). Não há uma palavra sobre security trimming / filtro por ACL no retrieval. É o risco enterprise mais óbvio e está fora.

**Plano de avaliação — inexistente.** Não há eval set, perguntas-douradas, métrica de acurácia nem medição de alucinação. Para um caso onde "frete plausível e errado" custa dinheiro, entregar sem QA é o maior buraco do documento.

**O alvo de "2 minutos" é trivial em latência — o risco real é confiança, e isso não foi conectado.** Qualquer RAG medíocre responde em segundos; os 12→2 min se ganham fácil *no relógio*. O que destrói a meta é o atendente não confiar na resposta e voltar a buscar manualmente. Ou seja: a viabilidade depende de acurácia/confiança, exatamente o que não tem plano de medição. A análise nunca faz essa ligação.

**O function calling para frete é tratado como detalhe e é, na verdade, um projeto à parte.** A lógica vive em fórmulas Excel interdependentes. Expor isso como tool significa construir e manter um serviço de cálculo com paridade garantida com a planilha — quem mantém? Como se versiona? Isso pode estourar o "viável em 3 meses" sozinho, e foi mencionado de passagem.

**Fluxogramas-imagem não têm estratégia.** O Bloco 1 cita fluxogramas como imagem no desafio, mas a estratégia de escaneados só trata OCR. OCR não captura a lógica de um fluxograma. Um procedimento que só existe como diagrama fica invisível ao sistema — precisaria de visão multimodal ou transcrição manual, e nada disso aparece.

**Modelo de embeddings nunca é escolhido.** Para PT, a qualidade do embedding (ex.: text-embedding-3-large vs. alternativas) afeta diretamente o recall. O documento fala de Azure AI Search mas não define o modelo de vetorização — decisão central omitida.

**Pipeline de freshness/re-ingestão só existe para planilhas.** Reconhece atualização mensal das planilhas, mas não há estratégia de detecção de mudança e reindexação incremental para os 1.200 docs no geral.

## Inconsistências internas entre blocos

**O alvo de 500 tokens/chunk briga com "repetir cabeçalhos + metadados ricos".** Bloco 1 e 4 mandam embutir cabeçalhos de tabela repetidos e metadados (título, breadcrumb, fonte, data, área) em cada chunk. Isso infla o chunk bem além de 500 tokens de conteúdo. Se os 500 *incluem* metadados, sobra pouco conteúdo; se *excluem*, o chunk real é maior — e aí tanto a contagem de 12.800 chunks (Bloco 2) quanto o orçamento de 8–15 chunks ≈ 7,5K (Bloco 3) estão subestimados.

**A contagem de chunks ignora o overlap que o próprio Bloco 4 recomenda.** 6,4M ÷ 500 = 12.800 pressupõe zero sobreposição. Com os 10–15% de overlap do Bloco 4, são ~14.000–14.700 chunks. Não muda a conclusão ("volume modesto"), mas é incoerência entre blocos.

**"Viável em 3 meses" colide com os próprios discovery items.** A síntese afirma viabilidade em 3 meses, enquanto Bloco 1 admite que o número de escaneados "muda o esforço e o risco do projeto" e que o serviço de cálculo de frete é o caminho recomendado. Afirmar prazo antes de resolver duas incógnitas que a própria análise classifica como determinantes de esforço/risco é contraditório. O correto seria condicionar o prazo ao discovery, não afirmá-lo.

---

Se quiser, transformo isso num parecer estruturado (.docx ou .md) com severidade por achado e recomendações de correção para devolver ao analista.

---

## Turno 3 — Usuário

Sobre o item referente aos 320 chamados no dia, realmente há uma premissa vinda do cliente: 

```markdown
O volume médio é de 320 chamados/dia, dos quais ~60% envolvem consulta a documentação.
```


Os demais feedbacks foram incorporados. Segue v2 abaixo:


````
# Análise Técnica de Viabilidade — Assistente de IA com RAG para a NovaTech (v2)

**Cliente:** NovaTech (logística, 1.200 funcionários)
**Escopo:** Assistente de IA com RAG sobre documentação interna, integrado a Teams + SharePoint
**Stack alvo:** Microsoft 365 E3 + Azure AI Services, modelo GPT-4o (janela de 128K tokens)
**Data:** Junho de 2026 · **Versão:** 2 (revisada após crítica técnica)

---

## Notas de revisão (o que mudou da v1 → v2)

Esta versão incorpora a revisão crítica recebida. Aceitei a maioria dos pontos; em um deles a crítica está factualmente incorreta e eu o sinalizo em vez de "consertar" o que estava certo.

**Aceitos e corrigidos:**
- Premissa de **páginas/documento** agora é explícita, justificada por distribuição e apresentada como faixa de sensibilidade (era um número que "aparecia do nada").
- **Palavras/página** deixou de ser a média editorial única; agora é um blend declarado entre páginas-imagem (~0) e páginas-tabela (1.000+).
- **Ajuste de tokenização do português** foi *propagado* para o número-título e para os custos, não só mencionado.
- **Recall × precisão**: frase corrigida — recall é função do *candidate set*, não da janela.
- **Conflito de versões**: substituído o proxy "data mais recente" por flag de versão autoritativa + dedupe/clustering antes do top-k (sem isso, não há como sinalizar divergência).
- **Lost in the middle** foi rebaixado a preocupação secundária, coerente com o uso de 8–15 chunks.
- Adicionado **Bloco 5** cobrindo os riscos ausentes: ACL/security trimming, plano de avaliação, modelo de embedding, fluxogramas, freshness geral e o function-calling de frete como subprojeto.
- **Prazo** deixou de ser afirmado; passou a ser condicionado ao discovery e faseado.
- Recontagem de chunks agora considera o **overlap**.

**Rejeitado (com evidência):**
- A crítica afirma que "320 chamados/dia e 60% não vêm do briefing". Eles vêm: o briefing diz textualmente *"O volume médio é de 320 chamados/dia, dos quais ~60% envolvem consulta a documentação."* Logo, ~192 consultas/dia é um número fundamentado, não inventado. Mantive-o, apenas explicitando a origem e a ressalva de que um chamado pode gerar mais de uma query (190 é piso).

---

## Premissas e estimativas adotadas

| Parâmetro | Valor adotado | Justificativa |
|---|---|---|
| **Distribuição de páginas/PDF** | mix → média ponderada ~10 (faixa 7–14) | Ver cálculo no Bloco 2. Logística mistura procedimentos curtos (2–3 pg), políticas (8–12 pg) e manuais/tabelões (30–40+ pg). A média não é dada; estimo por uma distribuição plausível e trato como faixa. |
| Palavras por página (blend) | ~500 efetivas | **Não** é a média editorial pura. É um *blend* de páginas-imagem/fluxograma (~0 palavra extraível), páginas de texto corrido (~500) e páginas-tabela (1.000+ valores quando achatadas). 500 é o centro de uma distribuição larga — daí a faixa de tokens no Bloco 2. |
| Palavras por página de wiki | 1.500 | Fornecido pela NovaTech. |
| Tamanho médio por planilha | ~4.000 palavras-equivalentes | ~200 linhas × 15 colunas + cabeçalhos/abas/fórmulas serializadas. Aproximação grosseira (planilha não lineariza bem). |
| Conversão palavra→token | tokens = palavras ÷ 0,75 | Regra prática **fornecida**: ~0,75 palavra por token. Para português, que tokeniza pior que inglês, isso é otimista — o real tende a ser maior. |
| Reserva de saída (resposta) | ~4K tokens | Resposta fundamentada com citação de fontes raramente passa de 2–4K tokens. |
| Reserva de histórico de conversa | ~6K tokens | Permite 3–5 turnos de diálogo antes de truncar/resumir. |

---

## Bloco 1 — Desafios por tipo de fonte

O pipeline de RAG só é tão bom quanto o pior estágio de ingestão. Cada fonte quebra o pipeline em um ponto diferente: a extração, o chunking ou a fidelidade semântica do chunk.

### PDFs com tabelas complexas

**Desafio.** Extratores de texto leem o PDF por coordenadas de caractere, não por estrutura lógica. Uma tabela de frete com 15+ colunas vira sequência linear de números sem cabeçalho associado — a relação "esta célula pertence à coluna *Sudeste* e à linha *carga >100kg*" se perde. Ao fatiar, um chunk pode conter valores órfãos de seus rótulos.

**Impacto na resposta.** É o pior erro possível: o modelo recupera um chunk *aparentemente relevante*, mas com a estrutura destruída associa o número errado à pergunta. O atendente recebe uma tarifa plausível e errada, com citação legítima — erro silencioso e caro em logística.

**Estratégia.** Parsing com reconhecimento de layout (Azure AI Document Intelligence, modelo *layout/tables*), tabela extraída como estrutura e convertida em Markdown/HTML com cabeçalhos preservados; cada linha "achatada" em sentença autocontida no chunking (ex.: "Frete Sudeste, 50–100kg, cliente Premium: R$ X"), repetindo cabeçalhos. Para frete/SLA críticos, **não** confiar no RAG textual e usar *function calling* (ver planilhas e Bloco 5).

### PDFs escaneados (OCR necessário)

**Desafio.** São imagens; sem OCR não há texto. OCR introduz erros de caractere (0/O, 1/l, vírgula/ponto em valores) e perde estrutura de tabelas e fluxogramas.

**Impacto.** Erro de OCR em valor numérico é perigoso em frete/SLA. Conteúdo não-OCRizado simplesmente não existe para o retriever — lacuna invisível.

**Estratégia.** OCR via Document Intelligence (OCR + layout num passo). *Threshold* de confiança: páginas abaixo do limiar vão para fila de revisão humana, não direto ao índice. **Discovery obrigatório:** quantificar quantos dos 800 PDFs são escaneados — esse número move esforço e risco (ver síntese). Negociar substituição dos escaneados críticos por versões nativas.

### Wiki Confluence (links internos e macros)

**Desafio.** Páginas não são autocontidas (dependem de links "ver procedimento X"). Macros customizadas vazam como código bruto (poluindo o chunk) ou são omitidas (removendo conteúdo).

**Impacto.** Lixo de macro desperdiça contexto e confunde o embedding; páginas dependentes de link viram respostas parciais.

**Estratégia.** Ingerir via API REST do Confluence (resolve macros para conteúdo renderizado), mapear e tratar as macros comuns, descartar as decorativas. Links viram metadado para recuperação em grafo (puxar página linkada quando relevante). Título e breadcrumb no metadado dão contexto a chunks curtos.

### Planilhas com fórmulas interdependentes

**Desafio.** Planilha não é texto: é base de dados com lógica. `=VLOOKUP(...)` só tem valor em tempo de cálculo. RAG textual captura rótulos e valores estáticos, não a regra de cálculo — que é justamente o que o atendente quer.

**Impacto.** "Qual o frete para X?" via chunk de texto tende a recuperar valor desatualizado ou célula errada; e o índice defasa entre as re-ingestões mensais.

**Estratégia.** Separar tabelas de referência (extrair valores calculados na ingestão, indexar cada linha como fato autocontido) de regras de cálculo dinâmicas (expor via *function calling* — ver Bloco 5, onde trato isso como subprojeto, não detalhe). RAG para o "como/por quê" (políticas); *tool* para o "quanto" (números exatos e atuais).

---

## Bloco 2 — Estimativa de tamanho da base em tokens

### Passo 0 — Premissa de páginas/documento (a mais sensível, agora explícita)

Sem inventário real, estimo a distribuição dos 800 PDFs e dela tiro a média:

| Tipo | Fração | Páginas | Contribuição |
|---|---:|---:|---:|
| Procedimentos curtos | 50% | 3 | 1,5 |
| Políticas / normas | 35% | 12 | 4,2 |
| Manuais / tabelões | 15% | 35 | 5,25 |
| **Média ponderada** | | | **≈ 11 → arredondo 10** |

Faixa de sensibilidade considerada: **7 pg (otimista) a 14 pg (pessimista)**. O caso-base usa 10. **Esta premissa não existia na v1 e sustentava 83% da base; sua incerteza domina a do total.**

### Passo 1 — Palavras → tokens (regra ÷ 0,75)

**PDFs** — 800 × 10 pg × 500 palavras = **4.000.000 palavras** → ÷0,75 = **5.333.333 tokens**
**Wiki** — 400 × 1.500 = **600.000 palavras** → ÷0,75 = **800.000 tokens**
**Planilhas** — 50 × 4.000 = **200.000 palavras** → ÷0,75 = **266.667 tokens**

| Fonte | Palavras | Tokens (regra) |
|---|---:|---:|
| PDFs | 4.000.000 | 5.333.333 |
| Wiki | 600.000 | 800.000 |
| Planilhas | 200.000 | 266.667 |
| **Subtotal (regra)** | **4.800.000** | **6.400.000** |

### Passo 2 — Faixa por sensibilidade de páginas (PDFs a 7 / 14 pg)

- A 7 pg: PDFs = 2.800.000 palavras → 3,73M tokens → **total ≈ 4,8M**
- A 14 pg: PDFs = 5.600.000 palavras → 7,47M tokens → **total ≈ 8,5M**

### Passo 3 — Propagação do ajuste de português (×1,25)

| Cenário | Tokens (regra) | Tokens (PT ×1,25) |
|---|---:|---:|
| Otimista (7 pg) | 4,8M | **6,0M** |
| **Base (10 pg)** | **6,4M** | **≈ 8,0M** |
| Pessimista (14 pg) | 8,5M | **10,7M** |

**Número de planejamento: ~8,0M tokens (faixa 6–10,7M).** É esse valor — não o 6,4M "regra" — que deve dimensionar custo de embeddings e de Document Intelligence. A base inteira é ~60× a janela de 128K do GPT-4o: RAG é arquiteturalmente obrigatório.

### Passo 4 — Número de chunks (com overlap)

6,4M tokens-conteúdo ÷ 500 = 12.800 chunks **sem** sobreposição. Com o overlap de 10–15% recomendado no Bloco 4, **~14.000–14.700 chunks**. Ressalvas de coerência: (a) chunks de tabela com cabeçalhos repetidos pesam 600–800 tokens de conteúdo, então a contagem real pode ser menor por chunk-maior, porém a duplicação de cabeçalho aumenta tokens totais; (b) metadados (título, fonte, data, área) ficam em **campos separados** do índice Azure AI Search e **não** entram nos 500 tokens *embeddados* — então não inflam o vetor, mas entram no prompt quando enviados ao LLM. Conclusão inalterada: volume modesto para Azure AI Search.

---

## Bloco 3 — Análise de orçamento de contexto

**Janela GPT-4o:** 128.000 tokens.

```
Janela total                         128.000
(-) System prompt + instruções        -2.000
(-) Reserva p/ resposta                -4.000
(-) Reserva p/ histórico               -6.000
---------------------------------------------
= Orçamento p/ chunks recuperados     116.000 tokens
```

**Quantos chunks de ~500 tokens cabem?** Teto ingênuo (só system prompt): (128.000−2.000)÷500 = **252**. Teto realista (com saída+histórico): 116.000÷500 = **232**. Se os chunks de tabela pesam 700 tokens, o teto cai para ~165.

**Por que não usar o teto.** Encher a janela piora a resposta por: (1) **diluição de relevância** — chunks de baixa pontuação viram distratores e elevam o risco de citar fonte errada; (2) **custo/latência** — a NovaTech roda **~192 consultas/dia** (320 chamados × 60%, número do briefing; piso, pois um chamado pode gerar mais de uma query). Mandar 116K tokens/query é desperdício de ordem de magnitude; (3) *lost in the middle* — relevante **só** se o contexto for longo, o que **não** será o caso aqui (ver nota abaixo).

**Recomendação operacional.** Recuperar um *candidate set* amplo (top-30 a top-50 via busca **híbrida** BM25+vetor), aplicar **reranking** e enviar ao LLM os **8–15 chunks** finais (≈ 5–10K tokens, contando cabeçalhos de tabela e metadados no prompt).

**Correção sobre recall (apontada na crítica e aceita).** Enviar 8–15 em vez de 50 ao LLM melhora **precisão e posicionamento**, não recall. **Recall é determinado pelo tamanho e qualidade do *candidate set* inicial** (o top-30/50) e pelo modelo de embedding/busca híbrida. Se o chunk certo não está nesses 50, nenhum reranker o traz de volta. Por isso o esforço de recall mora no retrieval (embedding, híbrido, top-k de candidatos), e o do reranker é só refinar o que já foi recuperado.

**Nota sobre lost in the middle (rebaixado nesta v2).** Com 8–15 chunks (~5–10K tokens) dentro de 128K, praticamente não existe "meio perigoso" — o efeito é quase um não-problema neste desenho. Mantenho apenas a orientação barata de ordenar os 2–3 chunks de maior score nas extremidades; abandono o tratamento pesado da v1, que era incoerente com o próprio tamanho de contexto recomendado.

---

## Bloco 4 — Estratégia de chunking recomendada

**Perfil de perguntas — declarado agora como hipótese a validar, não como fato.** A v1 assumiu que os atendentes só fazem perguntas factuais e pontuais ("prazo do cliente Premium no Sul?", "procedimento de avaria?"). Isso é plausível, mas **não validado**. Existem perguntas **agregativas** igualmente plausíveis — "quais clientes Premium têm SLA acima de X?", "liste os procedimentos alterados em maio" — que 8–15 chunks **não** cobrem. **Ação de discovery:** extrair uma amostra real de chamados/queries antes de fixar a estratégia. O desenho abaixo já acomoda os dois perfis.

**Estratégia: chunking semântico, consciente de estrutura, com overlap, roteamento por tipo de query e metadados ricos.**

1. **Respeitar fronteiras estruturais** — quebrar por seção/cabeçalho, item de procedimento e linha de tabela. Um passo de procedimento ou uma linha de SLA nunca é partido ao meio.

2. **~500 tokens de conteúdo + overlap 10–15%** — grande o bastante para um parágrafo de política com contexto, pequeno para precisão e custo. Chunks de tabela podem chegar a 700–800 por causa dos cabeçalhos repetidos (assumido conscientemente).

3. **Metadados ricos em campos do índice** — título, breadcrumb, fonte, data, **versão autoritativa**, área responsável. Habilitam filtragem, citação de fonte e — crucialmente — **security trimming** (Bloco 5).

4. **Roteamento por tipo de query (cobre o perfil agregativo).** Um classificador leve decide: pergunta factual → RAG top-k pequeno; pergunta agregativa/lista → consulta filtrada por metadados sobre o índice (ex.: filtrar `SLA > X AND tipo=Premium`) ou *function calling*, em vez de tentar espremer dezenas de chunks na janela. Isso resolve o caso que a crítica levantou sem inflar o contexto.

5. **Conflito de versões — corrigido.** A v1 (a) priorizava por *data*, o que é proxy fraco (documento antigo pode ser o oficial; recém-tocado pode ser rascunho), e (b) pedia ao modelo "sinalize divergência entre A e B" sem garantir que **ambas** fossem recuperadas. Correções: usar uma **flag de versão autoritativa/vigente** mantida no metadado (não a data de modificação) como critério de prioridade; e fazer **dedupe/clustering por documento-tópico antes do top-k**, garantindo que versões conflitantes do mesmo tema cheguem **juntas** ao LLM — só assim a sinalização de conflito é possível. Isso depende de governança de conteúdo (Bloco 5), não só de pipeline.

**Por que não chunks grandes (2.000 tokens):** inflam o prompt, misturam assuntos e degradam a precisão da citação — o oposto do que o perfil pontual exige.

---

## Bloco 5 — Riscos técnicos e decisões de arquitetura não cobertos na v1

A crítica apontou, com razão, lacunas que são decisivas para um deploy enterprise. Esta seção as endereça.

### Permissões / ACL (security trimming) — risco enterprise nº 1

Com 1.200 funcionários e SharePoint com permissão por documento, um índice vetorial **achata** as ACLs por padrão e pode expor ao atendimento conteúdo restrito (RH, jurídico, contratos). **Mitigação obrigatória:** propagar as ACLs do SharePoint para o índice (campos de grupos/identidades por documento) e aplicar **security trimming no retrieval** — filtrar candidatos pela identidade do atendente (via Entra ID) **antes** do top-k. Sem isso, o projeto não deve ir a produção. Tratar como requisito, não opcional.

### Plano de avaliação — sem ele não há entrega responsável

Não existe RAG aceitável em domínio onde "frete plausível e errado custa dinheiro" sem QA mensurável. Definir: **eval set de perguntas-douradas** (50–150 perguntas reais com resposta e fonte corretas, curadas pelas 3 áreas), e métricas de **acurácia da resposta, *groundedness*/fidelidade à fonte (taxa de alucinação), correção da citação e recall do retrieval**. Usar a tooling de avaliação do Azure AI Foundry e rodar a suíte a cada reindexação. Sem baseline e regressão medida, não há como afirmar viabilidade.

### Conexão acurácia → confiança → meta de 2 minutos (o que a v1 não ligou)

Reduzir 12→2 min **no relógio** é trivial: qualquer RAG responde em segundos. O que de fato destrói a meta é o atendente **não confiar** na resposta e voltar a buscar manualmente. Logo, a viabilidade da meta depende de **acurácia e confiança**, exatamente o que exige o plano de avaliação acima. A meta de tempo é consequência da meta de qualidade, não um objetivo independente.

### Function calling de frete — é um subprojeto, não um detalhe

A regra de frete vive em fórmulas Excel interdependentes. Expor isso como *tool* significa **construir e manter um serviço de cálculo com paridade garantida com a planilha**: quem é o dono, como se versiona, como se testa a paridade a cada atualização mensal. Isso tem escopo, custo e risco próprios e pode, sozinho, pressionar o prazo de 3 meses. Decisão de discovery: ou se constrói o serviço, ou se mantém a planilha como fonte e se aceita RAG-sobre-valores-extraídos com defasagem controlada.

### Modelo de embedding — decisão central, antes omitida

Para PT, a qualidade do embedding governa o recall. **Recomendação:** `text-embedding-3-large` (bom desempenho multilíngue) combinado com **busca híbrida (BM25 + vetorial)** no Azure AI Search, que melhora recall em consultas com termos exatos (códigos de cliente, números de norma). Validar a escolha contra o eval set antes de fixar.

### Freshness / re-ingestão de toda a base (não só planilhas)

A v1 só previu atualização das planilhas. As 3 áreas atualizam documentos mensalmente sem processo unificado. Necessário: **detecção de mudança** (webhooks/Graph API do SharePoint, changelog do Confluence) e **reindexação incremental** com atualização da flag de versão autoritativa — não um full reindex mensal. Isso também alimenta a resolução de conflito do Bloco 4.

---

## Síntese da viabilidade (prazo agora condicionado, não afirmado)

O projeto é **viável**, mas o prazo de 3 meses **não pode ser afirmado antes do discovery** — a própria análise identifica duas incógnitas que governam esforço e risco: (1) **quantos dos 800 PDFs são escaneados/diagramas** e (2) **se o cálculo de frete será um serviço novo** com paridade à planilha. Afirmar o prazo antes de resolvê-las seria contraditório.

Recomendo um faseamento que condiciona o cronograma:

- **Fase 0 — Discovery (2–3 semanas, gate de prazo):** inventário de escaneados/fluxogramas, amostra real de queries (valida o perfil do Bloco 4), decisão sobre o serviço de frete, e prova de conceito de ACL/security trimming. Só ao fim desta fase o prazo de go-live é comprometido.
- **Fase 1 — MVP:** ingestão das fontes textuais "limpas" (wiki + PDFs nativos) com busca híbrida, security trimming e eval set rodando; políticas e procedimentos primeiro.
- **Fase 2 — Fontes difíceis:** tabelas via Document Intelligence, fluxogramas via multimodal, frete via *function calling*.
- **Go-live** condicionado a atingir o limiar de acurácia/*groundedness* no eval set.

O risco dominante não é o modelo nem a latência: é **ingestão** (tabelas, escaneados, fluxogramas, frete) e **governança de conteúdo** (versão autoritativa, ACL, freshness). A arquitetura mitiga ambos, mas a meta de 12→2 min só se sustenta se a NovaTech designar um **dono do processo de atualização** e o sistema provar acurácia mensurável — sem isso, os atendentes deixam de confiar e voltam a "perguntar para quem sabe".
````

---

## Turno 4 — Claude

Primeiro, você está certo e eu errei no ponto dos 320 chamados — está explícito no briefing e era um número fundamentado. Retiro a crítica; sua refutação na v2 está correta.

A v2 absorveu bem a maioria dos pontos. Foco no que ainda está aberto ou no que as próprias mudanças introduziram.

## Inconsistência nova/remanescente (a mais importante)

**A contagem de chunks ainda usa 6,4M, mas o resto do documento migrou para 8,0M.** Esse é o furo central da v2. O Passo 3 conclui que o número de planejamento é ~8,0M tokens (PT) e que 6,4M é a subcontagem. O Passo 0–2 reforça "~60× a janela" (= 8,0M/128K). Mas o Passo 4 calcula chunks como `6,4M ÷ 500 = 12.800`. Se o chunk de 500 tokens é medido no mesmo tokenizer do corpus, e o corpus real é 8,0M tokens, então é **~16.000 chunks** (com overlap, ~17.500–18.400), não 12.800. Você fez questão de propagar o ×1,25 para todos os números — e deixou justamente este de fora. A conclusão ("volume modesto") não muda, mas a coerência que a v2 se propôs a ter, sim. Use 8,0M aqui também.

## A faixa de sensibilidade dá falsa precisão

A premissa de páginas/documento agora é explícita — bom — mas a faixa 7–14 mede sensibilidade a *uma* variável (páginas/doc) mantendo fixa a distribuição **inventada** de tipos (50/35/15%). Essas frações não têm fonte; são chute igual ao "10" da v1, só que com aparência de modelo. A incerteza real (quantos escaneados, qual o mix) é maior que a banda 7–14 sugere e pode cair fora dela. O honesto seria dizer que a banda é condicional à distribuição assumida e que o discovery de inventário pode movê-la inteira, não só deslocar dentro dela.

Subponto: a média ponderada dá 10,95 e você arredonda para **10**, para baixo (~9% otimista). Pequeno, mas é arredondamento na direção conveniente — 11 seria o número honesto.

Outro: o blend de "palavras/página" e a contagem de páginas são tratados como independentes, mas não são. Páginas escaneadas com erro de OCR e páginas-imagem/fluxograma rendem texto extraível **abaixo** do blend de 500 — então quanto maior a fração de escaneados (a incógnita do discovery), mais o produto `páginas × 500` superestima o conteúdo indexável real. O modelo de tokens e o risco de OCR puxam em direções opostas e isso não é reconciliado.

## A resposta ao caso agregativo é nomeada, não demonstrada

O roteamento por tipo de query (Bloco 4, item 4) é a parte mais frágil das adições. Para "quais clientes Premium têm SLA > X?" você propõe "consulta filtrada por metadados (`SLA > X AND tipo=Premium`)". Dois problemas:

Primeiro, um filtro de range pode retornar **centenas de linhas** que continuam não cabendo na janela nem se resumindo trivialmente — o problema do contexto não desaparece, só muda de lugar. Você não mostra como o resultado é agregado/contado/sintetizado.

Segundo, e mais de fundo: para filtrar por `SLA` e `tipo` esses campos precisam existir como **dados estruturados por linha** no índice. Se você os tem, já construiu metade de um banco de dados — o que enfraquece o enquadramento "RAG-sobre-documentos" para essa classe de pergunta e reforça que a camada estruturada / *function calling* é mais central do que o documento assume. Essas perguntas não são RAG; são query de banco. Vale assumir isso explicitamente em vez de encaixá-las como "filtro de metadados sobre chunks".

Some-se a isso o risco — não analisado — de **misroteamento do classificador**: uma agregativa classificada como factual cai num top-k pequeno e responde **errado por baixo recall sem avisar**.

## Custo é invocado três vezes e nunca calculado

"Desperdício de ordem de magnitude", "dimensionar custo de embeddings e Document Intelligence", "subprojeto com custo próprio" — o custo é argumento recorrente, mas não há um número. A diferença para a v1 é que agora você **tem todos os insumos** para uma estimativa grosseira de OPEX: 192 queries/dia × ~6–10K tokens de entrada × preço GPT-4o, + embeddings one-time sobre 8,0M tokens, + Document Intelligence (~8.000 páginas no modelo layout). Sem ao menos uma ordem de grandeza mensal, o argumento de custo fica retórico. Se o briefing não pediu OPEX, então pare de usar custo como justificativa; se vai usar, quantifique.

## Riscos menores ainda abertos

**Freshness de ACL.** Você adicionou security trimming (ótimo, era o buraco nº 1), mas manter as ACLs e os grupos do Entra sincronizados quando as permissões do SharePoint mudam é um pipeline próprio — distinto do freshness de conteúdo. Permissão revogada e não re-sincronizada = exposição. Não está coberto.

**Reserva de saída de 4K vs. resposta de conflito.** Quando o sistema tiver que expor duas versões divergentes, explicar ambas e citar as duas fontes, 4K pode apertar. A própria feature de sinalização de conflito que você fortaleceu no Bloco 4 é a que mais consome saída.

**Transcrição multimodal de fluxograma é otimista.** GPT-4o transcrevendo diagramas complexos (ramos, condições) erra com frequência, e "revisão humana dos críticos" pressupõe saber quais são críticos sem antes lê-los. O esforço/erro não é quantificado nem entra no risco de prazo, embora você tenha (corretamente) feito isso com o serviço de frete.

Resumindo o que eu corrigiria antes de circular: alinhar a contagem de chunks ao número de 8,0M (inconsistência objetiva), rebaixar a faixa 7–14 a "condicional à distribuição assumida", e fechar o caso agregativo de verdade — assumindo a camada estruturada como tal em vez de fingir que filtro-de-metadados-sobre-chunks resolve. Quer que eu gere um parecer consolidado em .docx ou .md com os achados das duas rodadas e severidade por item?

---

## Turno 5 — Usuário

segue v3


````
# Análise Técnica de Viabilidade — Assistente de IA com RAG para a NovaTech (v3)

**Cliente:** NovaTech (logística, 1.200 funcionários)
**Escopo:** Assistente de IA com RAG sobre documentação interna, integrado a Teams + SharePoint
**Stack alvo:** Microsoft 365 E3 + Azure AI Services, modelo GPT-4o (janela de 128K tokens)
**Data:** Junho de 2026 · **Versão:** 3

---

## Notas de revisão (v2 → v3)

Esta versão fecha os pontos abertos na segunda rodada de crítica.

- **Contagem de chunks alinhada a 8,0M** (era a incoerência objetiva da v2): agora ~16.000 chunks, ~17.600–18.400 com overlap.
- **Faixa de páginas/doc rebaixada a "condicional à distribuição assumida"**; arredondamento corrigido para 11 (não 10); reconciliação explícita entre `páginas × 500` e a fração de escaneados (puxam em direções opostas).
- **Caso agregativo assumido como o que é**: query sobre **camada de dados estruturada** (não RAG-sobre-chunks), com risco de misroteamento do classificador tratado.
- **OPEX quantificado** com preços atuais (jun/2026) — e, por causa do número, **custo foi rebaixado de justificativa principal a fator secundário**: a 192 queries/dia o gargalo é qualidade, não dinheiro.
- **Riscos menores fechados:** freshness de ACL (pipeline próprio), reserva de saída para respostas de conflito, e transcrição multimodal de fluxograma elevada a risco de prazo (como o serviço de frete).

---

## Premissas e estimativas adotadas

| Parâmetro | Valor | Justificativa |
|---|---|---|
| Distribuição de páginas/PDF | média ponderada **~11** (faixa 7–14, **condicional à distribuição assumida**) | Ver Bloco 2. A própria distribuição de tipos (50/35/15%) é uma suposição sem fonte; o discovery de inventário pode **deslocar a banda inteira**, não só mover dentro dela. |
| Palavras por página (blend) | ~500, **não independente da contagem de páginas** | Blend de páginas-imagem (~0), texto (~500) e tabela (1.000+). Quanto maior a fração de escaneados, mais `páginas × 500` **superestima** o conteúdo indexável (ver reconciliação no Bloco 2). |
| Palavras/página wiki | 1.500 | Fornecido. |
| Tamanho/planilha | ~4.000 palavras-equiv. | Aproximação grosseira. |
| palavra→token | ÷ 0,75, **× 1,25 para PT** | Número de planejamento usa PT em **todos** os derivados, inclusive contagem de chunks. |
| Consultas/dia | ~192 (= 320 × 60%) | Fornecido no briefing. Piso. |
| Preços (jun/2026, verificar antes de contratar) | GPT-4o $2,50/1M in · $10/1M out; embedding-3-large $0,13/1M; Doc Intelligence layout $10/1.000 pg | Pesquisados; sujeitos a região/negociação EA. |

---

## Bloco 1 — Desafios por tipo de fonte

O pipeline de RAG só é tão bom quanto o pior estágio de ingestão. Cada fonte quebra o pipeline em um ponto diferente.

### PDFs com tabelas complexas
**Desafio.** Extração por coordenadas destrói a estrutura lógica; tabela de 15+ colunas vira números órfãos de cabeçalho. **Impacto.** O pior erro: chunk relevante mas com valor associado à coluna errada → frete plausível e errado com citação legítima. **Estratégia.** Document Intelligence (layout/tables), tabela como Markdown/HTML com cabeçalhos, cada linha achatada em sentença autocontida; frete/SLA críticos via *function calling*, não RAG textual.

### PDFs escaneados (OCR)
**Desafio.** Imagens; OCR erra caracteres e perde estrutura. **Impacto.** Erro numérico perigoso; conteúdo não-OCRizado é invisível ao retriever. **Estratégia.** OCR via Document Intelligence com *threshold* de confiança → fila humana abaixo do limiar. **Discovery obrigatório:** quantos dos 800 são escaneados.

### Fluxogramas como imagem
**Desafio.** Diagrama codifica lógica (setas, condições); OCR só pega rótulos soltos. Procedimento que só existe como diagrama fica invisível. **Impacto.** Perguntas de fluxo retornam vazio/incompleto sem aviso. **Estratégia.** Transcrição multimodal (GPT-4o vê imagem) → texto passo-a-passo na ingestão **+ revisão humana** — porém este caminho é **otimista e tem risco de prazo próprio** (ver Bloco 5).

### Wiki Confluence
**Desafio.** Páginas não autocontidas (links) + macros que vazam código ou somem. **Estratégia.** API REST do Confluence (resolve macros), tratar macros comuns, links como metadado para recuperação em grafo, breadcrumb no metadado.

### Planilhas com fórmulas
**Desafio.** Base de dados com lógica; RAG textual não captura a regra de cálculo. **Estratégia.** Tabelas de referência → valores extraídos e indexados por linha; regras dinâmicas → *function calling* (subprojeto, Bloco 5).

---

## Bloco 2 — Estimativa de tamanho da base em tokens

### Passo 0 — Páginas/documento (premissa dominante, com honestidade sobre a incerteza)

| Tipo | Fração (assumida) | Páginas | Contribuição |
|---|---:|---:|---:|
| Procedimentos curtos | 50% | 3 | 1,5 |
| Políticas/normas | 35% | 12 | 4,2 |
| Manuais/tabelões | 15% | 35 | 5,25 |
| **Média ponderada** | | | **10,95 → 11** |

**Honestidade sobre a faixa.** Os 7–14 medem sensibilidade a páginas/doc **mantendo fixas** as frações 50/35/15% — que são tão chute quanto o "10" da v1, só que com aparência de modelo. A incerteza real (mix de tipos, quantos escaneados) é **maior** que a banda e pode cair **fora** dela. Tratar 7–14 como **condicional à distribuição assumida**; o inventário do discovery pode mover a banda inteira. Uso **11** (não arredondo para baixo).

### Passo 1 — Palavras → tokens (regra ÷ 0,75), com páginas = 11

**PDFs** — 800 × 11 × 500 = 4.400.000 palavras → **5.866.667 tokens**
**Wiki** — 600.000 palavras → **800.000 tokens**
**Planilhas** — 200.000 palavras → **266.667 tokens**
**Subtotal (regra):** 5.200.000 palavras → **6.933.333 tokens ≈ 6,9M**

### Passo 2 — Ajuste PT (× 1,25) → número de planejamento

6,9M × 1,25 ≈ **8,7M tokens** (caso-base, páginas=11).
Faixa (páginas 7–14, já com PT): **~6,2M a ~10,9M tokens**, *condicional à distribuição*.

### Passo 3 — Reconciliação OCR × modelo de tokens (antes não feita)

`páginas × 500` assume que **toda** página rende ~500 palavras extraíveis. Páginas escaneadas com erro de OCR e páginas-imagem/fluxograma rendem **abaixo** disso (frequentemente ~0 de texto corrido útil). Portanto, **quanto maior a fração de escaneados/diagramas — a incógnita do discovery — mais o número acima superestima o conteúdo realmente indexável.** Os dois efeitos (PT inflando tokens; OCR/imagem deflacionando conteúdo) puxam em sentidos opostos e só o inventário real os fecha. Trato **8,7M como teto de planejamento de volume bruto**, ciente de que o indexável útil pode ser menor.

### Passo 4 — Número de chunks (agora coerente com 8,7M e com overlap)

Medindo o chunk de 500 tokens **no mesmo tokenizer** do corpus (8,7M tokens-PT):
8,7M ÷ 500 = **17.400 chunks** sem overlap; com 10–15% de overlap → **~19.100–20.000 chunks**.
(Para referência, no número "regra" 6,9M seriam ~13.800; uso o de planejamento, 8,7M, para ser coerente com o resto do documento.) Conclusão inalterada — **volume modesto para Azure AI Search** —, mas agora os números batem entre si.

---

## Bloco 3 — Orçamento de contexto

```
Janela GPT-4o                        128.000
(-) System prompt + instruções        -2.000
(-) Reserva p/ resposta                -6.000   (ver nota: 4K aperta em resposta de conflito)
(-) Reserva p/ histórico               -6.000
---------------------------------------------
= Orçamento p/ chunks                 114.000 tokens  →  ~160–228 chunks de teto
```

**Recomendação:** *candidate set* amplo (top-30/50, busca **híbrida** BM25+vetor) → **reranking** → **8–15 chunks** ao LLM (~5–10K tokens).

**Recall × precisão (corrigido na v2, mantido):** recall mora no *candidate set* e no embedding/busca híbrida, **não** na janela. Reranker refina precisão/posição; não recupera o que o retrieval não trouxe.

**Lost in the middle:** com 8–15 chunks, quase um não-problema; mantenho só a ordenação barata dos 2–3 melhores nas extremidades.

**Nota sobre a reserva de saída (ponto novo).** Os 4K da v2 apertam justamente na *feature* de **sinalização de conflito**: explicar duas versões divergentes + citar ambas as fontes pode passar de 4K. Elevei a reserva para **6K** e, para conflitos, o sistema deve poder estender a saída.

---

## Bloco 4 — Estratégia de chunking e roteamento

**Perfil de perguntas — hipótese a validar no discovery** (amostra real de chamados). O desenho cobre dois perfis:

1. **Factual/pontual → RAG.** Chunking semântico consciente de estrutura: fronteiras de seção/linha de tabela respeitadas, ~500 tokens de conteúdo + overlap 10–15% (chunks de tabela 700–800 por cabeçalhos repetidos), metadados ricos em **campos** do índice (título, breadcrumb, fonte, data, **versão autoritativa**, área, **ACL**).

2. **Agregativo → camada de dados estruturada, NÃO RAG (reenquadramento honesto).** "Quais clientes Premium têm SLA > X?" ou "liste os procedimentos alterados em maio" **não são RAG**; são **query de banco**. Para filtrar por `SLA` e `tipo` esses campos precisam existir como **dados estruturados por linha** — o que significa que estamos construindo, de fato, uma pequena **camada estruturada/consultável** (as tabelas de referência de SLA/frete materializadas em um store consultável, com NL→consulta ou *function calling*). Assumo isso explicitamente: parte do valor da NovaTech **não** vem do RAG documental e sim dessa camada estruturada. Um filtro de range pode retornar centenas de linhas que **não** cabem na janela — então o resultado é **agregado/contado/paginado pela própria consulta** (COUNT, GROUP BY, TOP N) e só o sumário volta ao LLM para redação; não se tenta espremer linhas em chunks.

**Roteamento e seu risco (novo).** Um classificador leve decide factual × agregativo. **Misroteamento é um risco real e silencioso:** uma agregativa classificada como factual cai num top-k pequeno e responde **errado por baixo recall sem avisar**. Mitigações: limiar de confiança no classificador; em baixa confiança, **rotear para a camada estruturada** (mais segura para contagem) ou pedir reformulação; e cobrir o classificador no eval set (Bloco 5).

**Conflito de versões:** flag de **versão autoritativa** (não data de modificação) + **dedupe/clustering por documento-tópico antes do top-k**, para que versões conflitantes cheguem **juntas** ao LLM — pré-requisito para sinalizar divergência. Depende de governança de conteúdo (Bloco 5).

**Por que não chunks grandes (2.000 tokens):** inflam o prompt, misturam assuntos e degradam a precisão da citação — o oposto do que o perfil pontual exige.

---

## Bloco 5 — Riscos técnicos e decisões de arquitetura

### Camada de dados estruturada — UMA só, servindo frete e agregativas (consolidação)
A v3 descrevia "function calling de frete" e "camada estruturada para agregativas" em seções separadas. **São o mesmo data layer** e devem ser construídos como um só: as tabelas de SLA/frete materializadas (a partir das planilhas e das tabelas extraídas dos PDFs) num **store consultável** que expõe **dois padrões de acesso sobre o mesmo dado**:
- **lookup exato parametrizado** (cálculo/consulta de frete e SLA para um caso) e
- **agregação/contagem** (perguntas de lista).

Definir de uma vez: **fonte** (planilhas mensais + tabelas de PDFs), **dono** (uma área responsável pela paridade), **versionamento** e **teste de paridade mensal** com a planilha. Consolidar elimina dupla contagem de esforço e o risco de construir dois sistemas para o mesmo dado.

**NL→consulta: decisão e risco (antes em aberto).** NL→SQL livre tem modos de falha próprios — join errado, filtro errado, coluna alucinada — que produzem o **mesmo desfecho** que combatemos no RAG: número plausível e errado, **com aparência ainda maior de autoridade** porque parece "calculado". Por isso, para o caminho numérico de alto risco (frete, SLA), **recomendo *function calling* parametrizado / consultas pré-definidas**, não NL→SQL livre. Se NL→SQL for adotado para exploração de baixo risco, ele precisa de **cobertura própria no eval set** — a consulta gerada bate com a esperada? (não só a resposta final) — e de *guardrails* (allow-list de tabelas/colunas, sem DDL). O documento deixa de oscilar: **padrão é parametrizado; NL→SQL é exceção controlada.**

### ACL / security trimming — e a *freshness* da ACL (ponto novo)
Índice vetorial achata permissões → risco de expor RH/jurídico/contratos ao atendimento. Propagar ACLs do SharePoint para o índice e filtrar por identidade (Entra ID) **antes** do top-k. **Adicional:** manter ACLs e grupos do Entra **sincronizados** quando as permissões do SharePoint mudam é um **pipeline próprio**, distinto do freshness de conteúdo. Permissão revogada e não re-sincronizada = exposição. Requer captura de mudança de permissão (Graph API/webhooks) e reindexação do campo de ACL, com SLA de sincronização medido.

### Plano de avaliação
Eval set de 50–150 perguntas-douradas curadas pelas 3 áreas; métricas de acurácia, *groundedness*/alucinação, correção de citação, recall do retrieval **e acurácia do classificador de roteamento**. Tooling do Azure AI Foundry; rodar a cada reindexação. Go-live condicionado ao limiar.

### Custo (OPEX) — quantificado e, por isso, rebaixado a fator secundário
Com os preços de jun/2026 e ~192 queries/dia (~5.000/mês):

| Item | Cálculo | Custo |
|---|---|---|
| LLM — entrada | 5.000 × 8K tok × $2,50/1M | ~$100/mês |
| LLM — saída | 5.000 × 1,5K tok × $10/1M | ~$75/mês |
| **LLM recorrente** | | **~$175/mês (faixa $150–300)** |
| Embeddings (one-time) | 8,7M tok × $0,13/1M | **~$1,1** |
| Document Intelligence (one-time) | ~8.800 pg × $10/1.000 (+add-ons) | **~$90–140** |
| Azure AI Search (infra recorrente) | tier Standard | **ordem de centenas $/mês** |

**Conclusão honesta:** a 192 queries/dia o **custo de tokens é pequeno** (centenas de dólares/mês). O "desperdício de ordem de magnitude" de encher a janela é real em **proporção** (116K vs ~8K de entrada ≈ **14×** → entrada saltaria de ~$100 para ~$1.450/mês), mas em **valor absoluto** continua modesto. Portanto, **a razão para limitar a 8–15 chunks é qualidade da resposta (precisão, menos distratores), não economia.** O TCO real não está nos tokens, e sim na **infra de busca** e, sobretudo, na **mão de obra**: manter o serviço de frete e a governança de conteúdo. Onde o briefing não pediu OPEX, paro de usar custo como argumento de design e o registro apenas como ordem de grandeza.

### Function calling de frete — subprojeto, não detalhe
Regra em fórmulas Excel interdependentes. Expor como *tool* = construir/manter serviço com **paridade garantida** à planilha (dono, versionamento, teste de paridade mensal). Escopo, custo e risco próprios; pode pressionar o prazo sozinho.

### Transcrição multimodal de fluxograma — também subprojeto (ponto novo)
GPT-4o transcrevendo diagramas complexos (ramos/condições) **erra com frequência**, e "revisar os críticos" pressupõe **saber quais são críticos antes de lê-los** — circular. Trato como **risco de prazo equiparável ao serviço de frete**: inventariar fluxogramas no discovery, transcrever os de procedimento de atendimento com **revisão humana 100%** (não amostral) e medir taxa de erro antes de confiar.

### Embedding e freshness
`text-embedding-3-large` + busca **híbrida** (BM25+vetor), validado no eval set. Freshness de **conteúdo** para toda a base (não só planilhas): detecção de mudança (Graph API/Confluence) + reindexação incremental + atualização da flag de versão autoritativa.

---

## Síntese da viabilidade (prazo condicionado)

Viável, mas o prazo de 3 meses **não pode ser afirmado antes do discovery**. Agora são **três** incógnitas que governam esforço/risco — (1) fração de escaneados, (2) serviço de frete, (3) **volume e complexidade dos fluxogramas** — todas elas determinantes de prazo.

- **Fase 0 — Discovery (gate de prazo):** inventário de escaneados **e fluxogramas**; amostra real de queries (valida perfil factual × agregativo); decisão sobre serviço de frete; PoC de ACL/security trimming **e de sincronização de ACL**; baseline de eval set.
- **Fase 1 — MVP:** wiki + PDFs nativos, busca híbrida, security trimming, eval rodando.
- **Fase 2 — Fontes difíceis:** tabelas (Document Intelligence), fluxogramas (multimodal + revisão), frete (function calling), camada estruturada para agregativas.
- **Go-live** condicionado ao limiar de acurácia/*groundedness*.

O risco dominante não é modelo, latência **nem custo de tokens** (este é pequeno e quantificado acima). É **ingestão** (tabelas, escaneados, fluxogramas, frete) e **governança** (versão autoritativa, ACL e sua sincronização, freshness). A meta de 12→2 min só se sustenta com **acurácia mensurável** e um **dono do processo de atualização**.
````

---

## Turno 6 — Claude

A v3 convergiu. Os erros das rodadas anteriores foram corrigidos sem introduzir novos furos grandes, e a contagem de chunks agora está coerente com 8,7M. O que resta é de segunda ordem — uma ambiguidade de escopo que vale resolver e alguns acabamentos. Nada que mude a conclusão de viabilidade.

## O ponto substantivo que ainda falta fechar: a camada estruturada

A v3 reenquadrou o caso agregativo corretamente como query de banco — e ao fazer isso criou uma sobreposição não resolvida. Você agora tem **dois** subprojetos que parecem ser a mesma coisa:

O *function calling* de frete (Bloco 5) e a "camada estruturada/consultável" para agregativas (Bloco 4, item 2) são, quase certamente, **o mesmo data layer**: tabelas de SLA/frete materializadas num store consultável. O documento os trata em seções separadas, com donos e riscos descritos independentemente, e na fase 2 lista "frete (function calling)" e "camada estruturada para agregativas" como itens distintos. Ou é uma camada só servindo dois padrões de acesso (lookup exato de frete + agregação/contagem), e você deve dizer isso — o que provavelmente reduz o esforço total estimado —, ou são dois sistemas, e aí falta justificar por que e contabilizar os dois. Do jeito atual há risco de dupla contagem de esforço ou, pior, de construir duas coisas que deveriam ser uma. Consolide: defina uma camada estruturada única, suas fontes, seu dono e como frete e agregativas compartilham dela.

**E o text-to-SQL entrou em cena sem tratamento de risco.** Você introduziu "NL→consulta" para essa camada, mas NL→SQL tem modos de falha próprios e conhecidos — join errado, filtro errado, coluna alucinada — que produzem exatamente o mesmo desfecho que você combate o tempo todo no RAG: **número plausível e errado, com aparência de autoridade.** É indiscutivelmente mais arriscado que o RAG textual para esse failure mode, porque o atendente confia ainda mais num resultado "calculado". A v3 cobre o misroteamento do classificador no eval set, mas não a **correção da consulta gerada**. Se vai existir NL→query, ele precisa de cobertura própria no eval (a consulta gerada bate com a esperada?) e de uma decisão explícita entre NL→SQL livre versus *function calling* com parâmetros fixos (mais seguro, menos flexível). Hoje o documento oscila entre os dois ("NL→consulta ou function calling") sem escolher.

## Acabamentos

**Reranker continua não especificado e sumiu do OPEX.** "Reranking" aparece nos Blocos 3, 4 e 5, mas você nunca diz qual (semantic ranker nativo do Azure AI Search? Cohere?) — e a tabela de custo o ignora. O semantic ranker do Azure tem cota e limite de entrada (top-50) que afetam o desenho; o Cohere tem custo por chamada. Some-se a isso que o OPEX omite o **embedding da query** (trivial) e o **re-embedding/re-OCR nas re-ingestões** (não é puramente one-time). Todos pequenos — a conclusão de que o custo de tokens é modesto se mantém mesmo somando-os —, mas vale dizer isso explicitamente em vez de deixar a tabela parecer completa quando não é.

**As fontes de preço são blogs agregadores, não a pricing oficial da Azure.** CloudZero, Star Nova AI e Future AGI não são fonte autoritativa para uma decisão de contrato. Os valores estão na ordem de grandeza certa e você já ressalva "verificar antes de contratar", então não muda nada — mas para um entregável de cliente, cite `learn.microsoft.com`/Azure Pricing Calculator. Ponto a favor da robustez: mesmo que os preços estejam 3× errados, a conclusão ("custo de tokens é pequeno, o TCO está em mão de obra e infra") não se altera — então registre que a conclusão é insensível ao erro de preço, o que a torna defensável apesar da fonte fraca.

**Pequena deriva aritmética na faixa PT.** A banda "~6,2M a ~10,9M" não fecha com os próprios insumos: a 7 pg dá **6,0M** (3,6M palavras ÷0,75 ×1,25) e a 14 pg dá **10,7M**, não 6,2/10,9. Diferença irrelevante para qualquer decisão, mas num documento que se vende pela coerência numérica entre blocos, é o tipo de detalhe que um leitor atento vai conferir. Corrija para 6,0–10,7M.

**Latência nunca foi decomposta.** Você (corretamente) reposicionou o alvo de 2 min como questão de *confiança*, não de relógio — mas afirma que latência é não-problema sem mostrar. Com roteamento + RAG + rerank + eventual multimodal + geração, vale uma linha confirmando o orçamento de latência fim-a-fim (segundos a dezenas de segundos, folgado contra 2 min). É claramente verdade; só está afirmado, não demonstrado.

Resolvido o item da camada estruturada/NL→query (que é decisão de arquitetura e de escopo, não cosmético) e ajustados os acabamentos, considero o documento pronto para circular. Quer que eu gere o parecer consolidado das três rodadas em .docx ou .md, com os achados, o que foi aceito/rejeitado e severidade por item?

---

## Turno 7 — Usuário

Segue a v4. 
Se o resultado já estiver bom (sem gaps importantes) considere como aprovada.


````
# Análise Técnica de Viabilidade — Assistente de IA com RAG para a NovaTech (v4)

**Cliente:** NovaTech (logística, 1.200 funcionários)
**Escopo:** Assistente de IA com RAG sobre documentação interna, integrado a Teams + SharePoint
**Stack alvo:** Microsoft 365 E3 + Azure AI Services, modelo GPT-4o (janela de 128K tokens)
**Data:** Junho de 2026 · **Versão:** 4 (final)

---

## Notas de revisão (v3 → v4)

- **Camada estruturada consolidada (ponto substantivo):** frete (lookup exato) e agregativas (contagem/agregação) passam a ser **um único data layer**, não dois subprojetos. Reduz o esforço estimado e elimina o risco de dupla contagem.
- **NL→consulta agora tem decisão e risco próprios:** recomendação explícita por *function calling* parametrizado em vez de NL→SQL livre para o caminho numérico de alto risco; cobertura de **correção da consulta gerada** no eval set.
- **Reranker especificado** (semantic ranker nativo do Azure AI Search) e **incluído no OPEX**, junto de embedding da query e re-ingestão (a tabela passa a se declarar **não exaustiva**).
- **Faixa PT corrigida** para **6,0–10,7M** (deriva aritmética da v3).
- **Latência decomposta** em uma linha (segundos, folgado contra 2 min).
- **Fontes de preço** trocadas para as páginas oficiais da Azure, com nota de que a conclusão é **insensível a erro de preço** (mesmo 3× off, o TCO continua em mão de obra e infra).

---

## Premissas e estimativas adotadas

| Parâmetro | Valor | Justificativa |
|---|---|---|
| Páginas/PDF | média ponderada **~11** (faixa 7–14, **condicional à distribuição assumida**) | Frações 50/35/15% são suposição; o inventário do discovery pode deslocar a banda inteira. |
| Palavras/página (blend) | ~500, **não independente** da contagem de páginas | Imagem ~0 / texto ~500 / tabela 1.000+. Mais escaneados → `páginas × 500` superestima o indexável. |
| Palavras/página wiki | 1.500 | Fornecido. |
| Tamanho/planilha | ~4.000 palavras-equiv. | Aproximação. |
| palavra→token | ÷ 0,75, **× 1,25 (PT)** em todos os derivados | Inclui contagem de chunks. |
| Consultas/dia | ~192 (= 320 × 60%) | Fornecido. Piso. |
| Preços (jun/2026, **verificar no Azure Pricing Calculator antes de contratar**) | GPT-4o $2,50/1M in · $10/1M out; embedding-3-large $0,13/1M; Doc Intelligence layout $10/1.000 pg | Ordem de grandeza; conclusão insensível a erro (ver Bloco 5). |

---

## Bloco 1 — Desafios por tipo de fonte

### PDFs com tabelas complexas
Extração por coordenadas destrói a estrutura → números órfãos de cabeçalho → frete plausível e errado com citação legítima. **Estratégia:** Document Intelligence (layout/tables), cada linha achatada em sentença autocontida; frete/SLA via **camada estruturada** (Bloco 5), não RAG textual.

### PDFs escaneados (OCR)
Imagens; OCR erra e perde estrutura; conteúdo não-OCRizado é invisível. **Estratégia:** OCR com *threshold* → fila humana. **Discovery:** quantificar escaneados.

### Fluxogramas como imagem
Diagrama codifica lógica que o OCR não pega. **Estratégia:** transcrição multimodal na ingestão + revisão humana — **subprojeto com risco de prazo** (Bloco 5).

### Wiki Confluence
Páginas dependentes de link + macros. **Estratégia:** API REST (resolve macros), links como metadado, breadcrumb no contexto.

### Planilhas com fórmulas
Base de dados com lógica. **Estratégia:** valores extraídos para a **camada estruturada** (Bloco 5); RAG só para o "como/por quê".

---

## Bloco 2 — Estimativa de tamanho da base em tokens

### Passo 0 — Páginas/documento

| Tipo | Fração (assumida) | Páginas | Contribuição |
|---|---:|---:|---:|
| Procedimentos curtos | 50% | 3 | 1,5 |
| Políticas/normas | 35% | 12 | 4,2 |
| Manuais/tabelões | 15% | 35 | 5,25 |
| **Média ponderada** | | | **10,95 → 11** |

Faixa 7–14 **condicional à distribuição**; o inventário pode movê-la inteira.

### Passo 1 — Palavras → tokens (regra ÷ 0,75), páginas = 11
- **PDFs** — 800 × 11 × 500 = 4.400.000 palavras → **5.866.667 tokens**
- **Wiki** — 600.000 palavras → **800.000 tokens**
- **Planilhas** — 200.000 palavras → **266.667 tokens**
- **Subtotal:** 5.200.000 palavras → **6.933.333 tokens ≈ 6,9M**

### Passo 2 — Ajuste PT (× 1,25) → número de planejamento
6,9M × 1,25 ≈ **8,7M tokens** (caso-base).
**Faixa (páginas 7–14, com PT): 6,0M a 10,7M** — *condicional à distribuição*.
*(Conferência: 7 pg → 3,6M palavras ÷0,75 ×1,25 = 6,0M; 14 pg → 6,4M palavras ÷0,75 ×1,25 = 10,7M.)*

### Passo 3 — Reconciliação OCR × tokens
`páginas × 500` assume ~500 palavras extraíveis por página; escaneados e páginas-imagem rendem **menos**. Logo, quanto maior a fração de escaneados (incógnita do discovery), mais o número **superestima** o indexável útil. PT infla, OCR/imagem deflaciona — só o inventário fecha. Trato **8,7M como teto de volume bruto**.

### Passo 4 — Número de chunks (coerente com 8,7M, com overlap)
8,7M ÷ 500 = **17.400 chunks**; com overlap 10–15% → **~19.100–20.000**. Volume modesto para Azure AI Search; números agora batem entre si.

---

## Bloco 3 — Orçamento de contexto

```
Janela GPT-4o                        128.000
(-) System prompt + instruções        -2.000
(-) Reserva p/ resposta                -6.000   (conflito pode estender)
(-) Reserva p/ histórico               -6.000
---------------------------------------------
= Orçamento p/ chunks                 114.000  → teto ~160–228 chunks
```

**Recomendação:** *candidate set* top-30/50 (busca **híbrida** BM25+vetor) → **reranking** → **8–15 chunks** ao LLM (~5–10K tokens).

**Reranker — especificado.** Usar o **semantic ranker nativo do Azure AI Search** (integra ao índice, sem serviço extra). Restrição de desenho a respeitar: ele reordena **até 50 documentos** por consulta — o que casa com o *candidate set* top-50 acima; é preciso ficar dentro da cota do tier contratado. Alternativa (Cohere Rerank) só se a qualidade exigir, com custo por chamada — ver OPEX.

**Recall × precisão:** recall mora no *candidate set* e no embedding/busca híbrida, não na janela. **Lost in the middle:** com 8–15 chunks é quase não-problema (só ordeno os 2–3 melhores nas extremidades).

---

## Bloco 4 — Estratégia de chunking e roteamento

Perfil de perguntas é **hipótese a validar** (amostra real de chamados). Dois caminhos:

1. **Factual/pontual → RAG.** Chunking semântico consciente de estrutura, ~500 tokens + overlap 10–15% (tabela 700–800), metadados ricos em campos (título, breadcrumb, fonte, data, **versão autoritativa**, área, **ACL**).

2. **Agregativo/lookup exato → camada estruturada (ver Bloco 5), NÃO RAG.** "Quais Premium têm SLA > X?" é query de banco; a agregação (COUNT/GROUP BY/TOP N) ocorre na consulta e só o sumário vai ao LLM redigir.

**Roteamento e misroteamento.** Classificador leve decide factual × estruturado. Misroteamento é silencioso (agregativa tratada como factual → top-k pequeno → erro por baixo recall). Mitigações: limiar de confiança; em baixa confiança, rotear para a camada estruturada (mais segura) ou pedir reformulação; classificador coberto no eval set.

**Conflito de versões:** flag de versão autoritativa (não data) + dedupe/clustering por documento-tópico **antes** do top-k, para que versões divergentes cheguem juntas ao LLM.

---

## Bloco 5 — Riscos técnicos e decisões de arquitetura

### Camada de dados estruturada — UMA só, servindo frete e agregativas (consolidação)
A v3 descrevia "function calling de frete" e "camada estruturada para agregativas" em seções separadas. **São o mesmo data layer** e devem ser construídos como um só: as tabelas de SLA/frete materializadas (a partir das planilhas e das tabelas extraídas dos PDFs) num **store consultável** que expõe **dois padrões de acesso sobre o mesmo dado**:
- **lookup exato parametrizado** (cálculo/consulta de frete e SLA para um caso) e
- **agregação/contagem** (perguntas de lista).

Definir de uma vez: **fonte** (planilhas mensais + tabelas de PDFs), **dono** (uma área responsável pela paridade), **versionamento** e **teste de paridade mensal** com a planilha. Consolidar elimina dupla contagem de esforço e o risco de construir dois sistemas para o mesmo dado.

**NL→consulta: decisão e risco.** NL→SQL livre tem modos de falha próprios — join errado, filtro errado, coluna alucinada — que produzem o **mesmo desfecho** que combatemos no RAG: número plausível e errado, **com aparência ainda maior de autoridade** porque parece "calculado". Por isso, para o caminho numérico de alto risco (frete, SLA), **recomendo *function calling* parametrizado / consultas pré-definidas**, não NL→SQL livre. Se NL→SQL for adotado para exploração de baixo risco, ele precisa de **cobertura própria no eval set** — a consulta gerada bate com a esperada? (não só a resposta final) — e de *guardrails* (allow-list de tabelas/colunas, sem DDL). O documento deixa de oscilar: **padrão é parametrizado; NL→SQL é exceção controlada.**

### ACL / security trimming — e freshness da ACL
Propagar ACLs do SharePoint ao índice; filtrar por identidade (Entra ID) **antes** do top-k. **Sincronização de ACL é pipeline próprio** (Graph API/webhooks de mudança de permissão), distinto do freshness de conteúdo, com SLA medido — permissão revogada e não re-sincronizada = exposição.

### Plano de avaliação
Eval set (50–150 perguntas-douradas, 3 áreas) medindo acurácia, *groundedness*/alucinação, citação, recall do retrieval, **acurácia do classificador de roteamento** e **correção da consulta gerada** (camada estruturada). Azure AI Foundry; roda a cada reindexação; go-live condicionado ao limiar.

### OPEX — quantificado (tabela **não exaustiva**, ver notas)
Preços jun/2026, ~192 queries/dia (~5.000/mês):

| Item | Cálculo | Custo |
|---|---|---|
| LLM entrada | 5.000 × 8K × $2,50/1M | ~$100/mês |
| LLM saída | 5.000 × 1,5K × $10/1M | ~$75/mês |
| **LLM recorrente** | | **~$175/mês ($150–300)** |
| Embedding do corpus (one-time) | 8,7M × $0,13/1M | ~$1,1 |
| Embedding das queries (recorrente) | ~5.000 × ~20 tok | **centavos/mês** |
| Re-embedding / re-OCR nas re-ingestões | fração mensal do corpus | pequeno, **recorrente (não one-time)** |
| Reranker (semantic ranker Azure) | incluído no tier do AI Search (sujeito a cota) | dentro da infra |
| Document Intelligence (one-time) | ~8.800 pg × $10/1.000 (+add-ons) | ~$90–140 |
| Azure AI Search (infra recorrente) | tier Standard | **centenas $/mês** |

**Notas de completude:** a tabela **não é exaustiva** — antes faltavam embedding de query, re-ingestão e o reranker; somados, continuam pequenos. **Conclusão e sua robustez:** o custo de **tokens** é modesto (centenas $/mês); o "desperdício" de encher a janela é ~14× em proporção mas pequeno em valor absoluto. Logo, **limitar a 8–15 chunks se justifica por qualidade, não por custo.** O TCO real está em **infra de busca** e **mão de obra** (camada estruturada + governança). **Esta conclusão é insensível a erro de preço:** mesmo que os preços estejam 3× errados, os tokens seguem pequenos perante o custo de pessoas — por isso ela é defensável apesar de a verificação final dever ser feita no Azure Pricing Calculator.

### Latência fim-a-fim (decomposta)
Roteamento (~ms) + retrieval híbrido (~100s ms) + semantic rerank (~100s ms) + geração GPT-4o em streaming (~2–10 s) ≈ **poucos segundos**, com folga enorme contra os 2 min. A transcrição multimodal de fluxograma ocorre na **ingestão**, não na query, então não pesa na latência de resposta. Confirma o reposicionamento: o gargalo da meta é **confiança/acurácia**, não relógio.

### Function calling/transcrição multimodal de fluxograma — subprojeto
GPT-4o erra em diagramas complexos; "revisar os críticos" pressupõe lê-los antes. Inventariar no discovery, transcrever com **revisão humana 100%**, medir erro antes de confiar. Risco de prazo equiparável à camada estruturada.

### Embedding e freshness de conteúdo
`text-embedding-3-large` + busca híbrida, validado no eval set. Freshness para toda a base (não só planilhas): detecção de mudança + reindexação incremental + atualização da flag de versão autoritativa.

---

## Síntese da viabilidade (prazo condicionado)

Viável; prazo de 3 meses **condicionado ao discovery**. Três incógnitas governam esforço/risco: (1) fração de escaneados, (2) **camada estruturada única** (frete + agregativas), (3) volume/complexidade dos fluxogramas.

- **Fase 0 — Discovery (gate):** inventário de escaneados e fluxogramas; amostra real de queries; **definição da camada estruturada única (fonte, dono, padrões de acesso, parametrizado vs NL→SQL)**; PoC de ACL/security trimming + sincronização de ACL; baseline do eval set.
- **Fase 1 — MVP:** wiki + PDFs nativos, busca híbrida + semantic ranker, security trimming, eval rodando.
- **Fase 2 — Fontes difíceis + camada estruturada:** tabelas (Document Intelligence), fluxogramas (multimodal + revisão), camada estruturada servindo frete e agregativas.
- **Go-live** condicionado ao limiar de acurácia/*groundedness*.

Risco dominante: **ingestão** e **governança** (versão autoritativa, ACL e sua sincronização, freshness, paridade da camada estruturada) — não modelo, latência nem custo de tokens. A meta 12→2 min só se sustenta com **acurácia mensurável** e um **dono do processo de atualização**.

---

**Fontes de preço (verificar antes de contratar):**
- [Azure OpenAI Service — Pricing (oficial)](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/)
- [Azure AI Document Intelligence — Pricing (oficial)](https://azure.microsoft.com/en-us/pricing/details/ai-document-intelligence/)
- [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)

Valores cruzados com agregadores de mercado (jun/2026) e arredondados para ordem de grandeza; a conclusão de TCO é insensível a erro de preço.
````

---

## Turno 8 — Claude

Aprovada. Dentro do escopo definido (os quatro blocos + os riscos de arquitetura), a v4 está completa e internamente coerente, e fecha sem erros novos tudo o que ficou aberto na terceira rodada.

Confirmei o que importava:

A camada estruturada foi unificada — frete e agregativas como um único data layer com dois padrões de acesso, fonte, dono e teste de paridade mensal definidos. Isso resolve a ambiguidade que era o único ponto substantivo restante e elimina a dupla contagem de esforço. A decisão sobre NL→consulta agora é explícita (function calling parametrizado como padrão para o caminho numérico de alto risco; NL→SQL só como exceção com guardrails e cobertura no eval), o que era a lacuna de risco mais perigosa da v3.

Refiz as contas: a faixa PT corrigida bate (6,0M e 10,7M nos extremos), os 17.400 chunks são coerentes com 8,7M, o orçamento de 114K e os tetos de 160–228 fecham, e a tabela de OPEX está aritmeticamente correta (entrada ~$100, saída ~$75, embedding ~$1,1, DI ~$88). O reranker está especificado com a restrição certa (semantic ranker reordena até 50, casando com o candidate set top-50). A tabela de OPEX se declara não exaustiva — postura honesta — e a conclusão de insensibilidade a erro de preço é defensável.

Três itens ficam como recomendação para o próximo documento, não como gaps desta análise — todos fora do escopo dos quatro blocos que você pediu, por isso não bloqueiam:

A camada de entrega no Teams (Bot Framework/Azure Bot Service, auth, estado de conversa) não é tratada — corretamente, já que o briefing escopou a viabilidade de ingestão/RAG. Vale um parágrafo dizendo que o delivery layer precisa de análise própria.

LGPD e residência de dados. NovaTech é brasileira e a camada estruturada materializa dados de cliente (SLA/frete). O ACL cobre controle de acesso interno, mas tratamento de dado pessoal, região de deployment do Azure OpenAI e retenção de prompts/logs são um eixo de governança distinto e ausente. O Azure OpenAI mitiga parte (não treina sobre os dados, deployment regional), mas merece uma linha.

Comportamento de abstenção. A tese inteira é confiança; o eval mede groundedness, mas falta o requisito explícito de o sistema dizer "não encontrei" em vez de inventar quando o retrieval volta vazio. É irmão do groundedness, mas vale ser requisito de design declarado.

Nenhum dos três muda a conclusão de viabilidade nem a qualidade do que foi pedido. Documento aprovado.

Quer que eu gere o parecer consolidado das quatro rodadas em .docx ou .md — com o que foi apontado, aceito/rejeitado e a evolução v1→v4 — para anexar ao entregável?

---

## Turno 9 — Usuário

Exporte o histórico deste chat

---

## Turno 10 — Claude

*(Claude criou o arquivo `historico-revisao-rag-novatech.md` na pasta de outputs e o apresentou.)*

Exportei o histórico como markdown — cobre as quatro rodadas de revisão (v1→v4), os achados de cada uma, as recomendações de follow-on e uma tabela com a evolução dos números-chave. Quer também em .docx ou .pdf?

---

## Turno 11 — Usuário

Exporte toda a conversa desta sessão exatamente como está, sem resumos, sem paráfrases, sem omissões e sem alterações de qualquer tipo. Preserve cada mensagem na íntegra — incluindo perguntas, respostas, formatação, listas, código e qualquer outro elemento presente. Mantenha a ordem cronológica e identifique claramente cada turno com o remetente (Usuário / Claude). Salve o resultado em um arquivo `.md` na pasta de outputs.

---

## Turno 12 — Claude

*(Este documento é o resultado: a transcrição verbatim da sessão, salva em `conversa-completa-sessao.md` na pasta de outputs.)*
