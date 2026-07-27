# AGENTS.md — NovaTech Assistant

> Constitution do projeto. Todo agente de IA (Copilot, Claude Code) lê este arquivo antes de gerar qualquer artefato.
> As seções abaixo são preenchidas por papéis diferentes nos exercícios do Cenário 2.

## Project Overview
Assistente de IA (RAG) para o atendimento da NovaTech. Atendentes fazem perguntas em linguagem
natural e recebem respostas fundamentadas na documentação oficial da empresa, **sempre com citação
da fonte**. Integrado ao Microsoft Teams (bot) e a um painel web interno. Objetivo de negócio:
reduzir o tempo médio de busca de ~12 min para < 2 min por chamado.

## Tech Stack & Architecture
- **Linguagem:** TypeScript (strict), ESM (`"type": "module"` no `package.json`).
- **Backend:** Azure Functions v4 (HTTP triggers).
- **IA:** Azure OpenAI — GPT-4o (completion) e embeddings; Azure AI Search (retrieval).
- **Validação:** Zod (entrada **e** saída).
- **Resiliência:** retry com exponential backoff em toda chamada a serviço Azure.
- **Logging:** `pino` (structured logging). Sem `console.log`.
- **Testes:** `vitest`.
- **IaC:** Bicep (estado narrativo nesta fase — nenhum recurso Azure real é provisionado).
- **Gerenciamento de contexto (ADR-0002):** context budget de ~4K tokens de system prompt +
  ~8K de chunks (5 chunks de ~1.5K) + pergunta + histórico limitado a 3 turnos.
- **Documentos contraditórios (ADR-0003):** metadado de vigência; priorizar a versão mais recente;
  obsoletos marcados, não excluídos.
- **Componentes:** (1) pipeline de ingestão, (2) API do assistente (Functions + AI Search +
  OpenAI), (3) bot no Teams, (4) painel web (React).
- **Organização de diretórios:** ver Anexo C (`src/functions`, `src/services`, `src/pipeline`,
  `src/shared`, `specs`, `prompts`, `tests`, `infra`).

## Estrutura do projeto
Resumo do layout (árvore completa em `Prática 2/anexo-c-estrutura-repositorio.md`):
- `src/functions/<nome>/` — endpoints (Azure Functions): `handler.ts`, `validator.ts`, `response-builder.ts`
- `src/services/` — lógica de negócio: `search.ts`, `completion.ts`, `prompt-builder.ts`, `response-validator.ts`
- `src/pipeline/` — ingestão: `extractor.ts`, `chunker.ts`, `embedder.ts`, `indexer.ts`
- `src/bot/` — bot do Teams · `src/web/` — painel React
- `src/shared/` — `types.ts`, `config.ts`, `logger.ts`, `errors.ts`
- `specs/<modulo>/` — `requirements.md`, `plan.md`, `tasks.md` (SDD)
- `prompts/` — system prompt versionado + eval · `skills/` — foundation/domain/artifact
- `tests/` — unit/integration/e2e/fixtures · `docs/adr/` — ADRs (`NNNN-titulo.md`)

**Regras de colocação:** um handler por função em `src/functions/<nome>/handler.ts`; tipos de
domínio em `src/shared/types.ts`; lógica de negócio não fica no handler — vai em `src/services/`.

## Coding Standards (Tech Lead)
- **TypeScript strict**; imports ESM. Um handler HTTP por função (`src/functions/<nome>/handler.ts`).
- **Sem `console.log`** — usar o logger `pino` em `src/shared/logger.ts`.
- **Validação com Zod:** todo input e output passa por um schema (nunca validar "na mão"). Schema do
  input fica no `validator.ts` do endpoint; input inválido → HTTP `400` com o detalhe do erro.
- **Configuração e segredos via env**, lidos em `src/shared/config.ts`. Nada hardcoded.
- **Erros tipados** em `src/shared/errors.ts`, mapeados para status HTTP corretos (`400`/`500`).
- **Chamadas externas (Azure)** sempre com retry + exponential backoff.
- **Tipos de domínio** compartilhados em `src/shared/types.ts`.
- **Guardrails de resposta** (ver seção de Product Rules): citar a fonte, nunca inventar
  prazos/valores, e dizer explicitamente quando não encontrar (não alucinar).

## Product Rules & Guardrails (Product Specialist)
<!-- TODO (Product Specialist — Ex. 2.3) -->

## Testing Standards (QA)
<!-- TODO (QA — Ex. 2.1) -->

## Project Management Rules (Delivery Manager)
<!-- TODO (Delivery Manager — Ex. 2.3) -->

## Build & Deploy
- `npm run build` → `tsc -p .` · `npm test` → `vitest run` · `npm run lint` → `eslint .`
- Nesta fase **não há deploy real** — a infraestrutura Bicep é estado narrativo.
