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
