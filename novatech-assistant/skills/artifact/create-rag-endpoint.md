---
name: create-rag-endpoint
description: >-
  Receita para gerar um endpoint Azure Functions v4 com padrão RAG no NovaTech Assistant.
  Use ao criar um endpoint que recebe pergunta, recupera chunks e responde com a fonte.
  Compõe as skills de Domain (azure-functions-endpoint, azure-ai-search-integration) +
  Foundation (typescript-conventions, error-handling, logging, env-config) e encoda as
  decisões arquiteturais do cenário 1 (ADR-0001..0004).
---

# create-rag-endpoint (Artifact)

## Composição
Esta skill Artifact **compõe** outras (não repete convenções):
- **Foundation:** `typescript-conventions`, `error-handling`, `logging`, `env-config`
- **Domain:** `azure-functions-endpoint` (estrutura handler/validator), `azure-ai-search-integration` (busca)

## Decisões do cenário 1 que o endpoint DEVE respeitar (ADRs)
- **ADR-0001 (modelo):** completion via **GPT-4o** e embeddings via **Azure OpenAI** — não trocar de modelo sem ADR.
- **ADR-0002 (context budget):** montar o prompt com ~**4K tokens** de system + ~**8K** de chunks
  (**5 chunks de ~1.500 tokens**) + pergunta + histórico limitado a **3 turnos**. Nunca estourar a janela.
- **ADR-0003 (documentos contraditórios):** usar o **metadado de vigência** dos chunks; priorizar a
  versão mais recente; jamais citar documento obsoleto como fonte.
- **ADR-0004 (chunking de tabelas):** tabelas de frete/SLA podem ter sido mal fragmentadas na ingestão;
  ao recuperar um chunk de tabela, validar que cabeçalho + linha estão íntegros **antes** de responder
  um valor numérico.

## Passos da receita
1. Handler Azure Functions v4 (POST) + validação Zod do input (seguir `azure-functions-endpoint`).
2. Gerar embedding da pergunta (Azure OpenAI) com retry/backoff.
3. Buscar top-5 chunks (Azure AI Search) respeitando a vigência (**ADR-0003**).
4. Montar o prompt dentro do context budget (**ADR-0002**): system + chunks + pergunta.
5. Completion GPT-4o (**ADR-0001**); resposta com `source_document`.
6. Validar output com Zod; logging estruturado com `requestId`.

## Guardrails / anti-padrões
- **Não** responder valor de frete/SLA sem chunk de tabela íntegro (**ADR-0004**).
- Sem chunk relevante → dizer que não encontrou e sugerir escalar ao supervisor; **não alucinar**.
- **Nunca** hardcodar budget/limites (5 chunks, 4K/8K) — ler de `env-config`; os números vêm da ADR-0002.
- Sempre citar a fonte (guardrail de produto): resposta sem `source_document` é inválida.
