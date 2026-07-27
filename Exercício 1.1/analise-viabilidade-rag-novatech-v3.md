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

---

## Bloco 5 — Riscos técnicos e decisões de arquitetura

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

**Conclusão honesta:** a 192 queries/dia o **custo de tokens é pequeno** (centenas de dólares/mês). O "desperdício de ordem de magnitude" de encher a janela é real em **proporção** (116K vs ~8K de entrada ≈ **14×** → entrada saltaria de ~$100 para ~$1.450/mês), mas em **valor absoluto** continua modesto. Portanto, **a razão para limitar a 8–15 chunks é qualidade da resposta (precisão, menos distratores), não economia.** O TCO real não está nos tokens, e sim na **infra de busca** e, sobretudo, na **mão de obra**: manter o serviço de frete e a governança de conteúdo. Onde o briefing não pediu OPEX detalhado, paro de usar custo como argumento de design e o registro apenas como ordem de grandeza.

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

O risco dominante não é modelo, latência **nem custo de tokens** (este é pequeno e quantificado acima). É **ingestão** (tabelas, escaneados, fluxogramas, frete) e **governança** (versão autoritativa, ACL e sua sincronização, freshness). A meta de 12→2 min só se sustenta com **acurácia mensurável** e um **dono do processo de atualização** — sem confiança, o atendente volta a "perguntar para quem sabe".

---

**Fontes (preços):**
- [Azure OpenAI Pricing 2026 — CloudZero](https://www.cloudzero.com/blog/azure-openai-pricing/)
- [Azure AI Document Intelligence Pricing 2026 — Star Nova AI](https://starnovai.com/azure-ai-document-intelligence-pricing)
- [text-embedding-3-large pricing — Azure OpenAI / Future AGI](https://futureagi.com/llm-cost-calculator/azure-openai/text-embedding-3-large/)
