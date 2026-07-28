# Guia de verificação — Exercício 3.1 (structured output + harness)

> ⚠️ **LEIA ANTES DE AVALIAR — a avaliação só é válida COM a subpasta `novatech-assistant/`.**
> O código do harness (schema Zod + `response-validator.ts`) vive em
> **`novatech-assistant/src/services/`**, não nesta pasta. Avaliar sem abrir essa subpasta deixa o
> entregável central "ausente". **Se o pacote recebido não contém `novatech-assistant/`, PARE e
> solicite-a antes de pontuar.**

## Tarefas 1 e 2 — Schema Zod + validator com guardrails (Copilot)
| Arquivo | Papel |
|---|---|
| `novatech-assistant/src/services/response-validator.ts` | **Entregável:** schema Zod `.strict()` do structured output `{ answer, source_document, confidence_score }` + `validateResponse()` com os 2 guardrails determinísticos (versão **v2 corrigida**). |

## Tarefa 3 — Code review crítico + correções (Claude)
| Arquivo | Papel |
|---|---|
| `Exercício 3.1/revisao-critica-response-validator.md` | 3 problemas reais + correções (fail-closed, gatilho por radical, `.trim()`), e a distinção **prompt (probabilístico) × código (determinístico)**. |

## Evidência de uso do Copilot (D2)
| Arquivo | Papel |
|---|---|
| `Exercício 3.1/Evidência copilot/prompt-criacao-response-validator.png` | Prompt + geração do schema (tarefa 1). |
| `Exercício 3.1/Evidência copilot/prompt-edicao-response-validator.png` | Prompt + geração do validator (tarefa 2). |
| `Exercício 3.1/Evidência copilot/response-validator-v1-copilot.ts` | v1 do Copilot (antes). |
| `Exercício 3.1/Evidência copilot/response-validator-v2-corrigido.ts` | v2 corrigido (depois). |

## Resumo dos caminhos a inspecionar
```
novatech-assistant/src/services/response-validator.ts        (schema + validator, Tarefas 1 e 2)
Exercício 3.1/revisao-critica-response-validator.md          (code review, Tarefa 3)
Exercício 3.1/Evidência copilot/                             (prints + v1/v2)
```
