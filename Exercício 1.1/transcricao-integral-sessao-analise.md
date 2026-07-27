# Transcrição Integral da Sessão

---

## Turno 1 — Usuário

````markdown
Você é um especialista em arquitetura de soluções de IA. Preciso que produza uma análise técnica de viabilidade para um assistente de IA com RAG (Retrieval-Augmented Generation) considerando as características da documentação da empresa NovaTech e o impacto do gerenciamento da janela de contexto na arquitetura.

## O Cenário

A NovaTech é uma empresa de médio porte do setor de logística com 1.200 funcionários. Sua operação depende de um conjunto extenso de documentação interna: manuais de procedimento operacional, políticas de compliance, tabelas de SLA por tipo de cliente, regras de cálculo de frete, e normas de segurança de carga.

Hoje, essa documentação está espalhada em três fontes: um SharePoint corporativo com ~800 documentos (PDFs e Word), uma wiki interna no Confluence com ~400 páginas, e uma pasta de rede com planilhas de referência atualizadas mensalmente.

O problema: a equipe de atendimento ao cliente (45 pessoas) gasta em média 12 minutos por chamado buscando informações nessas fontes para responder dúvidas de clientes sobre prazos, regras de frete, políticas de devolução e procedimentos de reclamação. Isso gera atrasos, respostas inconsistentes e frustração tanto dos atendentes quanto dos clientes.

A NovaTech nos contratou para construir um assistente de IA que permita aos atendentes fazer perguntas em linguagem natural e receber respostas fundamentadas na documentação oficial da empresa, com indicação da fonte. O assistente será integrado ao ambiente Microsoft da NovaTech (Teams + SharePoint).

### Informações adicionais fornecidas pela NovaTech

- O volume médio é de 320 chamados/dia, dos quais ~60% envolvem consulta a documentação.
- A documentação é atualizada mensalmente por 3 áreas diferentes (Operações, Compliance, Comercial), sem processo unificado de revisão.
- Alguns documentos se contradizem entre versões — a equipe de atendimento hoje resolve isso "perguntando para quem sabe".
- A NovaTech já tem licenças Microsoft 365 E3 e está disposta a provisionar Azure AI Services.
- O projeto tem orçamento para 3 meses de discovery + desenvolvimento + go-live.
- A expectativa da diretoria é reduzir o tempo médio de busca de 12 para menos de 2 minutos por chamado.

### Informações técnicas adicionais

Os PDFs do SharePoint incluem documentos com tabelas complexas (tabelas de frete com 15+ colunas), fluxogramas embutidos como imagens, e alguns documentos escaneados (OCR necessário). A wiki do Confluence tem links internos entre páginas e usa macros customizadas. As planilhas têm fórmulas interdependentes.

---

## Framework conceitual: Context Engineering aplicado a RAG

O contexto que o LLM recebe a cada pergunta é limitado pela janela de contexto do modelo. A qualidade da resposta depende de:
- **Quais chunks são selecionados** (relevância)
- **Quantos chunks cabem no contexto** (orçamento de atenção)
- **Onde ficam posicionados no prompt** — informação no meio de contextos longos é "esquecida" (efeito *lost in the middle*)
- **O que mais está no contexto competindo por atenção** (system prompt, histórico de conversa, instruções)

Este framework deve embasar toda a análise, especialmente os blocos de orçamento de contexto e estratégia de chunking.

---

## Missão

Produza uma análise técnica de viabilidade cobrindo os blocos abaixo. Para qualquer valor não fornecido, assuma uma estimativa explicitamente justificada — nunca use números sem explicar de onde vieram.

**Bloco 1 — Desafios por tipo de fonte**
Para cada tipo (PDFs com tabelas complexas, PDFs escaneados, wiki com links e macros, planilhas com fórmulas): qual o desafio para o pipeline de RAG, como isso afeta a qualidade das respostas, e a estratégia de tratamento recomendada.

**Bloco 2 — Estimativa de tamanho da base em tokens**
Calcule o total considerando: ~800 documentos PDF (média de 10 páginas cada), ~400 páginas wiki (média de 1.500 palavras cada), e ~50 planilhas (estime o tamanho com justificativa). Use a regra prática de ~0,75 palavras por token.

**Bloco 3 — Análise de orçamento de contexto**
Dado que o GPT-4o tem 128K tokens de janela e o system prompt + instruções consomem ~2K tokens, quantos chunks de ~500 tokens cabem em cada query? Como isso afeta a estratégia de chunking e retrieval?

**Bloco 4 — Estratégia de chunking recomendada**
Recomende uma estratégia justificada pelo tipo de pergunta que o atendente fará e pelo efeito *lost in the middle*.

---

## Formato do output

O output deve ser um arquivo markdown (.md) com a seguinte estrutura:
- Um H2 por bloco (ex: `## Bloco 1 — Desafios por tipo de fonte`)
- No Bloco 1, um H3 por tipo de fonte (ex: `### PDFs com tabelas complexas`)
- No Bloco 2, mostre os cálculos explicitamente antes do total

````

---

## Turno 1 — Claude

Análise pronta, seguindo a estrutura pedida (um H2 por bloco, H3 por fonte no Bloco 1, cálculos explícitos no Bloco 2).

Números-chave:

- **Base total: ~6,4M tokens** (PDFs 5,33M + wiki 0,8M + planilhas 0,27M) — 50× a janela do GPT-4o, o que torna RAG obrigatório.
- **Orçamento de contexto:** cabem ~232 chunks de 500 tokens, mas a recomendação é enviar só **8–15** após reranking, por causa do *lost in the middle* e diluição de relevância.

Todas as premissas não fornecidas (500 palavras/página, ~4.000 tokens/planilha, reservas de saída/histórico) estão justificadas numa tabela no topo. Dois pontos que destaquei como decisivos para a NovaTech: tabelas de frete e planilhas de cálculo pedem *function calling* em vez de RAG textual puro, e as contradições entre versões precisam de metadado de vigência + sinalização de conflito.

*(Arquivo gerado: `analise-viabilidade-rag-novatech.md`)*

---

## Turno 2 — Usuário

Considere as críticas realizadas abaixo:

````
Revisão crítica, organizada pelas quatro categorias que você pediu.
Estimativas otimistas ou sem justificativa
O "10 páginas/doc" não existe na tabela de premissas, mas sustenta 83% da base. Todo o número de PDFs (5,33M tokens) sai de 800 × 10 páginas × 500 palavras. A premissa de 500 palavras/página está justificada; a de 10 páginas/documento — que é a mais sensível das duas — aparece do nada no Bloco 2. Logística mistura procedimentos de 2 páginas com manuais e tabelões de 40+. Sem essa premissa explícita e justificada, o "6,4M tokens" é um chute com aparência de cálculo.
500 palavras/página ignora o que a própria análise disse no Bloco 1. Uma página que é um fluxograma-imagem ou uma tabela de 15 colunas tem ~0 palavras extraíveis de texto corrido, mas entra contando 500. Já uma página densa de tabela pode virar 1.000+ "valores". A média editorial de 500 não se aplica a um corpus que a análise mesma classificou como cheio de tabelas, escaneados e imagens.
O 320 chamados/dia × 60% = ~190 queries/dia do Bloco 3 é inventado. Nenhum desses três números (320, 60%, e portanto 190) vem do briefing. O briefing dá 45 pessoas e 12 min/chamado, nada de volume diário. Como o argumento de custo depende desse volume, ele fica sem chão.
A ressalva do português é levantada e depois ignorada. A análise reconhece que PT tokeniza 15–30% pior e diz "trate 6,4M como piso". Mas mantém 6,4M como número-título e não propaga o ajuste para nada. Se o real é 7,5–8,3M, muda custo de embeddings e de Document Intelligence — deveria ter usado o multiplicador maior, não só sinalizado.
Pontos fracos na argumentação
O perfil de perguntas "factuais e pontuais" é assumido, não validado — e é a base de todo o Bloco 4. Toda a estratégia de chunking (chunks pequenos, 8–15 trechos) decorre da afirmação de que ninguém faz pergunta agregativa. Mas "quais clientes Premium têm SLA acima de X?" ou "liste os procedimentos alterados em maio" são perguntas plausíveis de atendimento e exigem muitos chunks — 8–15 não cobrem. Isso precisa sair de log de queries real, não de suposição.
"Sem sacrificar recall — porque o reranker faz a seleção fina" confunde recall com precisão. Recall é determinado pelo retrieval inicial (top-30 a top-50). Se o chunk certo não está nesses 50, nenhum reranker o recupera. Mandar 8–15 ao LLM em vez de 50 melhora precisão/posição, mas o risco de recall mora no tamanho do candidate set, não na janela. A frase está solta e mascara o ponto real.
A priorização do "documento vigente" por data é um proxy fraco. Data de última modificação ≠ versão autoritativa. Um documento mais antigo pode ser o oficial; um recém-tocado pode ser rascunho. Resolver contradição por max(data) vai escolher errado em alguns casos.
A sinalização de conflito só funciona se as duas versões forem recuperadas juntas — e o resto do pipeline foi desenhado para não fazer isso. O Bloco 3 afina para mandar só o top relevante; o Bloco 4 quer que o modelo avise "há divergência entre A e B". Se o reranker mandar só a versão A, não há conflito a sinalizar. Isso exige dedupe/clustering por documento antes do top-k, o que não foi previsto.
Excesso de engenharia contra lost-in-the-middle. A análise dá peso enorme ao efeito e ao posicionamento topo/base, e na mesma seção admite que com 8–15 chunks "praticamente não existe meio perigoso". As duas coisas não podem ser verdade ao mesmo tempo — ou o problema é central, ou a recomendação já o neutralizou. Em 7,5K tokens dentro de 128K num GPT-4o, é quase não-problema.
Riscos técnicos não considerados
Permissões/ACL — ausência grave. São 1.200 funcionários e o SharePoint tem permissões por documento. Um índice vetorial achata isso por padrão e pode expor ao atendimento conteúdo restrito (RH, jurídico, contratos). Não há uma palavra sobre security trimming / filtro por ACL no retrieval. É o risco enterprise mais óbvio e está fora.
Plano de avaliação — inexistente. Não há eval set, perguntas-douradas, métrica de acurácia nem medição de alucinação. Para um caso onde "frete plausível e errado" custa dinheiro, entregar sem QA é o maior buraco do documento.
O alvo de "2 minutos" é trivial em latência — o risco real é confiança, e isso não foi conectado. Qualquer RAG medíocre responde em segundos; os 12→2 min se ganham fácil no relógio. O que destrói a meta é o atendente não confiar na resposta e voltar a buscar manualmente. Ou seja: a viabilidade depende de acurácia/confiança, exatamente o que não tem plano de medição. A análise nunca faz essa ligação.
O function calling para frete é tratado como detalhe e é, na verdade, um projeto à parte. A lógica vive em fórmulas Excel interdependentes. Expor isso como tool significa construir e manter um serviço de cálculo com paridade garantida com a planilha — quem mantém? Como se versiona? Isso pode estourar o "viável em 3 meses" sozinho, e foi mencionado de passagem.
Fluxogramas-imagem não têm estratégia. O Bloco 1 cita fluxogramas como imagem no desafio, mas a estratégia de escaneados só trata OCR. OCR não captura a lógica de um fluxograma. Um procedimento que só existe como diagrama fica invisível ao sistema — precisaria de visão multimodal ou transcrição manual, e nada disso aparece.
Modelo de embeddings nunca é escolhido. Para PT, a qualidade do embedding (ex.: text-embedding-3-large vs. alternativas) afeta diretamente o recall. O documento fala de Azure AI Search mas não define o modelo de vetorização — decisão central omitida.
Pipeline de freshness/re-ingestão só existe para planilhas. Reconhece atualização mensal das planilhas, mas não há estratégia de detecção de mudança e reindexação incremental para os 1.200 documentos no geral.
Inconsistências internas entre blocos
O alvo de 500 tokens/chunk briga com "repetir cabeçalhos + metadados ricos". Bloco 1 e 4 mandam embutir cabeçalhos de tabela repetidos e metadados (título, breadcrumb, fonte, data, área) em cada chunk. Isso infla o chunk bem além de 500 tokens de conteúdo. Se os 500 incluem metadados, sobra pouco conteúdo; se excluem, o chunk real é maior — e aí tanto a contagem de 12.800 chunks (Bloco 2) quanto o orçamento de 8–15 chunks ≈ 7,5K (Bloco 3) estão subestimados.
A contagem de chunks ignora o overlap que o próprio Bloco 4 recomenda. 6,4M ÷ 500 = 12.800 pressupõe zero sobreposição. Com os 10–15% de overlap do Bloco 4, são ~14.000–14.700 chunks. Não muda a conclusão ("volume modesto"), mas é incoerência entre blocos.
"Viável em 3 meses" colide com os próprios discovery items. A síntese afirma viabilidade em 3 meses, enquanto Bloco 1 admite que o número de escaneados "muda o esforço e o risco do projeto" e que o serviço de cálculo de frete é o caminho recomendado. Afirmar prazo antes de resolver duas incógnitas que a própria análise classifica como determinantes de esforço/risco é contraditório. O correto seria condicionar o prazo ao discovery, não afirmá-lo.
````

---

## Turno 2 — Claude

A maioria dessas críticas procede e vou incorporá-las. Há um ponto, porém, em que a crítica está factualmente errada — vou apontá-lo em vez de aceitá-lo cegamente: os números 320 chamados/dia e ~60% **estão** no briefing original ("O volume médio é de 320 chamados/dia, dos quais ~60% envolvem consulta a documentação"), então a query/dia derivada tem chão. Vou defender esse ponto e corrigir todo o resto.

V2 pronta com uma seção de changelog explicando o que mudou. Como ficou:

**Aceitei e corrigi** a grande maioria das críticas:

- Premissa de **páginas/doc** agora é explícita, justificada por distribuição (50% curtos / 35% médios / 15% manuais → média ponderada ~11≈10) e apresentada como **faixa 7–14**.
- **Palavras/página** virou um blend declarado (imagem ~0, texto ~500, tabela 1.000+), não a média editorial pura.
- **Ajuste do português (×1,25) propagado**: o número de planejamento passou a ser **~8,0M tokens (faixa 6–10,7M)**, não os 6,4M "regra".
- **recall × precisão** corrigido (recall mora no candidate set, não na janela); **lost-in-the-middle rebaixado**; **versão autoritativa em vez de data**; **dedupe/clustering** para que o conflito seja sinalizável; perfil de query agora é hipótese a validar + roteamento que cobre perguntas agregativas.
- **Bloco 5 novo**: ACL/security trimming, plano de avaliação (eval set + groundedness), conexão acurácia→confiança→meta, function calling de frete como subprojeto, escolha de embedding (`text-embedding-3-large` + híbrido), fluxogramas via multimodal, freshness geral.
- **Prazo condicionado** ao discovery, com faseamento (gate na Fase 0).

**Rejeitei um ponto, com evidência:** a crítica diz que "320 chamados/dia e 60% não vêm do briefing" — mas vêm, está textual no enunciado original ("O volume médio é de 320 chamados/dia, dos quais ~60% envolvem consulta a documentação"). Mantive os ~192 queries/dia, explicitando a origem e tratando como piso.

*(Arquivo gerado: `analise-viabilidade-rag-novatech-v2.md`)*

---

## Turno 3 — Usuário

A v2 absorveu bem a maioria dos pontos. Foco no que ainda está aberto ou no que as próprias mudanças introduziram.
Inconsistência nova/remanescente (a mais importante)
A contagem de chunks ainda usa 6,4M, mas o resto do documento migrou para 8,0M. Esse é o furo central da v2. O Passo 3 conclui que o número de planejamento é ~8,0M tokens (PT) e que 6,4M é a subcontagem. O Passo 0–2 reforça "~60× a janela" (= 8,0M/128K). Mas o Passo 4 calcula chunks como `6,4M ÷ 500 = 12.800`. Se o chunk de 500 tokens é medido no mesmo tokenizer do corpus, e o corpus real é 8,0M tokens, então são ~16.000 chunks (com overlap, ~17.500–18.400), não 12.800–14.700. Você fez questão de propagar o ×1,25 para todos os números — e deixou justamente este de fora. A conclusão ("volume modesto") não muda, mas a coerência que a v2 se propôs a ter, sim. Use 8,0M aqui também.
A faixa de sensibilidade dá falsa precisão
A premissa de páginas/documento agora é explícita — bom — mas a faixa 7–14 mede sensibilidade a uma variável (páginas/doc) mantendo fixa a distribuição inventada de tipos (50/35/15%). Essas frações não têm fonte; são chute igual ao "10" da v1, só que com aparência de modelo. A incerteza real (quantos escaneados, qual o mix) é maior que a banda 7–14 sugere e pode cair fora dela. O honesto seria dizer que a banda é condicional à distribuição assumida e que o discovery de inventário pode movê-la inteira, não só deslocar dentro dela.
Subponto: a média ponderada dá 10,95 e você arredonda para 10, para baixo (~9% otimista). Pequeno, mas é arredondamento na direção conveniente — 11 seria o número honesto.
Outro: o blend de "palavras/página" e a contagem de páginas são tratados como independentes, mas não são. Páginas escaneadas com erro de OCR e páginas-imagem/fluxograma rendem texto extraível abaixo do blend de 500 — então quanto maior a fração de escaneados (a incógnita do discovery), mais o produto `páginas × 500` superestima o conteúdo indexável real. O modelo de tokens e o risco de OCR puxam em direções opostas e isso não é reconciliado.
A resposta ao caso agregativo é nomeada, não demonstrada
O roteamento por tipo de query (Bloco 4, item 4) é a parte mais frágil das adições. Para "quais clientes Premium têm SLA > X?" você propõe "consulta filtrada por metadados (`SLA > X AND tipo=Premium`)". Dois problemas:
Primeiro, um filtro de range pode retornar centenas de linhas que continuam não cabendo na janela nem se resumindo trivialmente — o problema do contexto não desaparece, só muda de lugar. Você não mostra como o resultado é agregado/contado/sintetizado.
Segundo, e mais de fundo: para filtrar por `SLA` e `tipo` esses campos precisam existir como dados estruturados por linha no índice. Se você os tem, já construiu metade de um banco de dados — o que enfraquece o enquadramento "RAG-sobre-documentos" para essa classe de pergunta e reforça que a camada estruturada / function calling é mais central do que o documento assume. Essas perguntas não são RAG; são query de banco. Vale assumir isso explicitamente em vez de encaixá-las como "filtro de metadados sobre chunks".
Some-se a isso o risco — não analisado — de misroteamento do classificador: uma agregativa classificada como factual cai num top-k pequeno e responde errado por baixo recall, silenciosamente.
Custo é invocado três vezes e nunca calculado
"Desperdício de ordem de magnitude", "dimensionar custo de embeddings e Document Intelligence", "subprojeto com custo próprio" — o custo é argumento recorrente, mas não há um número. A diferença para a v1 é que agora você tem todos os insumos para uma estimativa grosseira de OPEX: 192 queries/dia × ~6–10K tokens de entrada × preço GPT-4o, + embeddings one-time sobre 8,0M tokens, + Document Intelligence (~8.000 páginas no modelo layout). Sem ao menos uma ordem de grandeza mensal, o argumento de custo fica retórico. Se o briefing não pediu OPEX, então pare de usar custo como justificativa; se vai usar, quantifique.
Riscos menores ainda abertos
Freshness de ACL. Você adicionou security trimming (ótimo, era o buraco nº 1), mas manter as ACLs e os grupos do Entra sincronizados quando as permissões do SharePoint mudam é um pipeline próprio — distinto do freshness de conteúdo. Permissão revogada e não re-sincronizada = exposição. Não está coberto.
Reserva de saída de 4K vs. resposta de conflito. Quando o sistema tiver que expor duas versões divergentes, explicar ambas e citar as duas fontes, 4K pode apertar. A própria feature de sinalização de conflito que você fortaleceu no Bloco 4 é a que mais consome saída.
Transcrição multimodal de fluxograma é otimista. GPT-4o transcrevendo diagramas complexos (ramos, condições) erra com frequência, e "revisão humana dos críticos" pressupõe saber quais são críticos sem antes lê-los. O esforço/erro não é quantificado nem entra no risco de prazo, embora você tenha (corretamente) feito isso com o serviço de frete.
Resumindo o que eu corrigiria antes de circular: alinhar a contagem de chunks ao número de 8,0M (inconsistência objetiva), rebaixar a faixa 7–14 a "condicional à distribuição assumida", e fechar o caso agregativo de verdade — assumindo a camada estruturada como tal em vez de fingir que filtro-de-metadados-sobre-chunks resolve.

---

## Turno 3 — Claude

Preços obtidos. Vou produzir a v3 com a estimativa de OPEX real e os demais ajustes.

V3 fecha todos os pontos. O que mudou de fato:

**A incoerência objetiva (chunks vs 8,0M)** — corrigida e propagada. Como já estava propagando o ×1,25, recalculei a base inteira com páginas=11: **6,9M tokens (regra) → ~8,7M (PT)**, e os chunks agora saem de 8,7M: **~17.400 sem overlap, ~19.100–20.000 com overlap**. Tudo bate entre si.

**Faixa de sensibilidade** — rebaixada a "condicional à distribuição assumida" (as frações 50/35/15% são chute igual ao "10"); o inventário do discovery pode mover a banda inteira. Arredondei para 11, não para baixo. E reconciliei o que você apontou: `páginas × 500` **superestima** quanto mais escaneados houver — PT infla, OCR/imagem deflaciona, e só o inventário fecha.

**Caso agregativo** — assumido como o que é: **query de banco, não RAG**. Existe uma camada estruturada (tabelas de SLA/frete materializadas, consultáveis), a agregação acontece na própria consulta (COUNT/GROUP BY/TOP N) e só o sumário vai ao LLM. Adicionei o risco de **misroteamento silencioso** do classificador e a mitigação (em baixa confiança, rotear para a camada estruturada).

**Custo — quantificado, e o resultado mudou o argumento.** A ~192 queries/dia: LLM ~**$175/mês**, embeddings ~**$1**, Document Intelligence ~**$90–140** one-time. O "desperdício" de encher a janela é real em proporção (~14×) mas pequeno em valor absoluto. Conclusão honesta: **limitar a 8–15 chunks se justifica por qualidade, não por custo**; o TCO real está na infra de busca e na mão de obra (serviço de frete + governança).

**Riscos menores:** freshness de ACL virou pipeline próprio; reserva de saída subiu para 6K (a resposta de conflito era a que mais apertava); e a transcrição multimodal de fluxograma virou subprojeto com risco de prazo, equiparada ao serviço de frete — com revisão humana 100%, já que "saber quais são críticos" exige lê-los antes.

Preços com data (jun/2026) e fontes no rodapé do documento.

Sources:
- [Azure OpenAI Pricing 2026 — CloudZero](https://www.cloudzero.com/blog/azure-openai-pricing/)
- [Azure AI Document Intelligence Pricing 2026 — Star Nova AI](https://starnovai.com/azure-ai-document-intelligence-pricing)
- [text-embedding-3-large pricing — Future AGI](https://futureagi.com/llm-cost-calculator/azure-openai/text-embedding-3-large/)

*(Arquivo gerado: `analise-viabilidade-rag-novatech-v3.md`)*

---

## Turno 4 — Usuário

Analise a revisão abaixo realizada sobre a v3

````
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

````

---

## Turno 4 — Claude

Convergiu — esses pontos são de segunda ordem e o substantivo (consolidar a camada estruturada) é uma boa pegada. Vou produzir a v4 fechando os cinco itens. Confirmo de antemão que a deriva aritmética que você apontou está certa: a faixa correta é **6,0–10,7M** (a 7pg: 3,6M palavras ÷0,75 ×1,25 = 6,0M; a 14pg = 10,7M).

A revisão está correta em todos os pontos e a v4 os fecha:

**Substantivo — camada estruturada.** Você tinha razão: o function-calling de frete e a camada agregativa eram o mesmo data layer descrito duas vezes. Consolidei numa **camada estruturada única** que expõe dois padrões de acesso sobre o mesmo dado (lookup exato parametrizado + agregação/contagem), com fonte, dono, versionamento e teste de paridade definidos uma vez só. Isso reduz o esforço e mata o risco de dupla contagem.

**NL→SQL.** Parei de oscilar: a recomendação agora é explícita — **function calling parametrizado para o caminho numérico de alto risco**, NL→SQL apenas como exceção controlada (allow-list, sem DDL) e com **eval de correção da consulta gerada** (não só da resposta final), já que NL→SQL produz o mesmo "número plausível e errado" do RAG, com autoridade ainda maior.

**Acabamentos:**
- **Reranker** especificado (semantic ranker nativo do Azure, limite de 50 docs que casa com o candidate set) e incluído no OPEX, junto de embedding de query e re-ingestão; a tabela agora se declara **não exaustiva**.
- **Faixa PT corrigida** para **6,0–10,7M**, com a conferência aritmética no próprio texto.
- **Latência decomposta**: roteamento + retrieval + rerank + geração ≈ poucos segundos; a transcrição de fluxograma é ingestão, não query — confirma que o gargalo é confiança, não relógio.
- **Fontes oficiais** da Azure no rodapé + nota de que a conclusão de TCO é **insensível a erro de preço** (mesmo 3× off, tokens continuam pequenos perante mão de obra).

Sources:
- [Azure OpenAI Service — Pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/)
- [Azure AI Document Intelligence — Pricing](https://azure.microsoft.com/en-us/pricing/details/ai-document-intelligence/)
- [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)

*(Arquivo gerado: `analise-viabilidade-rag-novatech-v4.md`)*

---

## Turno 5 — Usuário

Exporte o histórico deste chat

---

## Turno 5 — Claude

Histórico exportado. O arquivo cobre os cinco turnos desta conversa — solicitação inicial e v1, as três rodadas de crítica com as respectivas respostas (v2, v3, v4) e este export — mais uma tabela rastreando a evolução das estimativas-chave (páginas/doc, tokens, faixa PT, nº de chunks, OPEX e a consolidação da camada estruturada) entre as quatro versões.

*(Arquivo gerado: `historico-chat-novatech-rag.md`)*

---

## Turno 6 — Usuário

Exporte toda a conversa desta sessão exatamente como está, sem resumos, sem paráfrases, sem omissões e sem alterações de qualquer tipo. Preserve cada mensagem na íntegra — incluindo perguntas, respostas, formatação, listas, código e qualquer outro elemento presente. Mantenha a ordem cronológica e identifique claramente cada turno com o remetente (Usuário / Claude). Salve o resultado em um arquivo `.md` na pasta de outputs.

---

## Turno 6 — Claude

Vou reproduzir a conversa na íntegra, turno a turno, sem alterações.

*(Arquivo gerado: `transcricao-integral-sessao.md` — este arquivo)*
