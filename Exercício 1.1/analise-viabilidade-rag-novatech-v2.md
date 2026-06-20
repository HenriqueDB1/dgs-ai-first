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
| Conversão palavra→token | tokens = palavras ÷ 0,75 | Regra fornecida. **Otimista para PT.** Aplico multiplicador 1,25 para o número de planejamento (ver Bloco 2). |
| Multiplicador de tokenização PT | ×1,25 (faixa 1,15–1,30) | Português gera mais subpalavras que inglês no tokenizer do GPT-4o. Usado para converter o número-base em número de planejamento de custo. |
| Volume de consultas/dia | ~192 (= 320 × 60%) | **Fornecido** no briefing. Piso, pois 1 chamado pode gerar >1 query. |
| Reserva de saída / histórico | ~4K / ~6K tokens | Resposta com citações (2–4K) e 3–5 turnos de diálogo. |

---

## Bloco 1 — Desafios por tipo de fonte

O pipeline de RAG só é tão bom quanto o pior estágio de ingestão. Cada fonte quebra o pipeline em um ponto diferente.

### PDFs com tabelas complexas

**Desafio.** Extratores de texto leem o PDF por coordenadas de caractere, não por estrutura lógica. Uma tabela de frete com 15+ colunas vira sequência linear de números sem cabeçalho associado — a relação "esta célula pertence à coluna *Sudeste* e à linha *carga >100kg*" se perde. Ao fatiar, um chunk pode conter valores órfãos de seus rótulos.

**Impacto na resposta.** É o pior erro possível: o modelo recupera um chunk *aparentemente relevante*, mas com a estrutura destruída associa o número errado à pergunta. O atendente recebe uma tarifa plausível e errada, com citação legítima — erro silencioso e caro em logística.

**Estratégia.** Parsing com reconhecimento de layout (Azure AI Document Intelligence, modelo *layout/tables*), tabela extraída como estrutura e convertida em Markdown/HTML com cabeçalhos preservados; cada linha "achatada" em sentença autocontida no chunking (ex.: "Frete Sudeste, 50–100kg, cliente Premium: R$ X"), repetindo cabeçalhos. Para frete/SLA críticos, **não** confiar no RAG textual e usar *function calling* (ver planilhas e Bloco 5).

### PDFs escaneados (OCR necessário)

**Desafio.** São imagens; sem OCR não há texto. OCR introduz erros de caractere (0/O, 1/l, vírgula/ponto em valores) e perde estrutura de tabelas e fluxogramas.

**Impacto.** Erro de OCR em valor numérico é perigoso em frete/SLA. Conteúdo não-OCRizado simplesmente não existe para o retriever — lacuna invisível.

**Estratégia.** OCR via Document Intelligence (OCR + layout num passo). *Threshold* de confiança: páginas abaixo do limiar vão para fila de revisão humana, não direto ao índice. **Discovery obrigatório:** quantificar quantos dos 800 PDFs são escaneados — esse número move esforço e risco (ver síntese). Negociar substituição dos escaneados críticos por versões nativas.

### Fluxogramas embutidos como imagem

**Desafio (tratado separadamente nesta v2).** Um fluxograma é lógica de processo codificada em diagrama. OCR captura, no máximo, os rótulos soltos das caixas — não as setas, condições e ramos ("se cliente Premium → rota A; senão → rota B"). Um procedimento que só existe como diagrama fica **semanticamente invisível** ao sistema.

**Impacto.** Perguntas de procedimento ("qual o fluxo para reclamação de avaria?") retornam vazio ou um resumo incompleto, sem o sistema sinalizar que a fonte era um diagrama não interpretado.

**Estratégia.** Usar um modelo *multimodal* (GPT-4o aceita imagem) para transcrever cada fluxograma em texto estruturado passo-a-passo no momento da ingestão, com revisão humana dos diagramas críticos. Alternativamente, transcrição manual dos poucos fluxogramas que governam procedimentos de atendimento. Marcar no metadado que o chunk veio de diagrama transcrito.

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
