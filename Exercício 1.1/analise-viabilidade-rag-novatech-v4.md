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

**NL→consulta: decisão e risco (antes em aberto).** NL→SQL livre tem modos de falha próprios — join errado, filtro errado, coluna alucinada — que produzem o **mesmo desfecho** que combatemos no RAG: número plausível e errado, **com aparência ainda maior de autoridade** porque parece "calculado". Por isso, para o caminho numérico de alto risco (frete, SLA), **recomendo *function calling* parametrizado / consultas pré-definidas**, não NL→SQL livre. Se NL→SQL for adotado para exploração de baixo risco, ele precisa de **cobertura própria no eval set** — a consulta gerada bate com a esperada? (não só a resposta final) — e de *guardrails* (allow-list de tabelas/colunas, sem DDL). O documento deixa de oscilar: **padrão é parametrizado; NL→SQL é exceção controlada.**

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
