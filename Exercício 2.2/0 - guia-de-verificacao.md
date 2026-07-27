# Guia de verificação — Exercício 2.2 (Spec Driven Development)

> **Para quem vai avaliar (humano ou LLM):** os artefatos deste exercício **não estão todos nesta
> pasta**. O código e os specs vivem na subpasta **`novatech-assistant/`** (o starter do Anexo D,
> centralizado dentro do repo do curso — não é mais um repositório git aninhado). Para avaliar,
> **consulte os arquivos listados abaixo nessa subpasta.** Esta pasta (`Exercício 2.2/`) contém
> apenas a revisão crítica (Tarefa 3).

Caminho base da subpasta: `novatech-assistant/` (relativo à raiz do repo do curso `dgs-ai-first`).

---

## Tarefa 1 — Converter o plan em tasks atômicas
| Arquivo | Papel |
|---|---|
| `novatech-assistant/specs/query-endpoint/plan.md` | Input do Tech Lead (o plan fornecido no enunciado). |
| `novatech-assistant/specs/query-endpoint/tasks.md` | **Entregável:** 7 tasks atômicas (QE-01…QE-07) com ID, descrição, critérios de aceite, dependências e estimativa P/M/G. |

## Tarefa 2 — Implementar a 1ª task (QE-01) com IA (Claude Code)
| Arquivo | Papel |
|---|---|
| `novatech-assistant/src/functions/query/handler.ts` | HTTP trigger `POST /api/query` (Azure Functions v4): valida via Zod, `400` em input inválido, `200` com stub. |
| `novatech-assistant/src/functions/query/validator.ts` | Schema Zod do input (`question` obrigatória, ≤1000 chars; `conversationId` opcional). |
| `novatech-assistant/src/shared/types.ts` | Tipos de domínio do input/output. |
| `novatech-assistant/src/shared/logger.ts` | Logger pino (criado junto — pertence à QE-07; ver ponto 2 da revisão). |
| `novatech-assistant/tests/unit/query-validator.test.ts` | 10 casos de teste do schema. |
| `novatech-assistant/tests/unit/query-handler.test.ts` | 4 casos de teste do handler. |
| `novatech-assistant/package.json` | Dependências adicionadas: `@azure/functions`, `pino`, `zod`. |

Como conferir que compila/testa: na subpasta, `npm install` → `npm run build` → `npm test`
(reportado: build limpo, 14/14 testes passando).

## Tarefa 3 — Revisão crítica
| Arquivo | Papel |
|---|---|
| `Exercício 2.2/revisao-critica-qe-01.md` | **Entregável desta pasta:** 5 pontos reais de ajuste (+ secundários) antes de um code review. |

---

## Arquivos de apoio (constitution do projeto, usados pela IA ao gerar)
| Arquivo | Papel |
|---|---|
| `novatech-assistant/AGENTS.md` | Convenções do projeto (Tech Stack, Coding Standards, Estrutura). Lido pelos agentes antes de gerar código. |
| `novatech-assistant/CLAUDE.md` | Faz o Claude Code carregar o `AGENTS.md` via `@AGENTS.md`. |

## Resumo dos caminhos a inspecionar
```
novatech-assistant/specs/query-endpoint/plan.md
novatech-assistant/specs/query-endpoint/tasks.md
novatech-assistant/src/functions/query/handler.ts
novatech-assistant/src/functions/query/validator.ts
novatech-assistant/src/shared/types.ts
novatech-assistant/src/shared/logger.ts
novatech-assistant/tests/unit/query-validator.test.ts
novatech-assistant/tests/unit/query-handler.test.ts
novatech-assistant/package.json
novatech-assistant/AGENTS.md
novatech-assistant/CLAUDE.md
Exercício 2.2/revisao-critica-qe-01.md   (esta pasta)
```
