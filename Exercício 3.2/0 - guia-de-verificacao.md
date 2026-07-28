# Guia de verificação — Exercício 3.2 (revisão crítica de código gerado por IA)

> ⚠️ **LEIA ANTES DE AVALIAR — a avaliação só é válida COM a subpasta `novatech-assistant/`.**
> O código reescrito (`feedback/handler.ts` + `config.ts`) vive em **`novatech-assistant/src/`**, não
> nesta pasta. **Se o pacote recebido não contém `novatech-assistant/`, PARE e solicite-a antes de
> pontuar.**

## Tarefas 1 e 2 — Revisão humana + revisão Claude + comparação
| Arquivo | Papel |
|---|---|
| `Exercício 3.2/1 - revisao-e-comparacao.md` | **Entregável:** o código com bug (fornecido), a **revisão do humano** (feita antes), a **revisão do Claude** (classificada), a **comparação honesta** (humano × Claude) e a verificação da reescrita. |

## Tarefa 3 — Código reescrito (Copilot)
| Arquivo | Papel |
|---|---|
| `novatech-assistant/src/functions/feedback/handler.ts` | Módulo corrigido: Zod, pino (sem `console.log`), **não loga** `attendantEmail`, imports estáticos (sem `require`), tratamento de erro, Cosmos por init preguiçoso, resposta estruturada. |
| `novatech-assistant/src/shared/config.ts` | `getCosmosConnectionString()` — acesso centralizado à config. |
| `novatech-assistant/package.json` | Dependência `@azure/cosmos` adicionada. |

> **Cópia autossuficiente no pacote:** o código reescrito também está em
> `Exercício 3.2/codigo-reescrito/` (`handler.ts` + `config.ts`), para verificar a Tarefa 3 **mesmo
> sem** a subpasta `novatech-assistant/`. A versão canônica/versionada segue em `novatech-assistant/src/`.

## Verificação dos itens mínimos do enunciado
Todos identificados na revisão e corrigidos na reescrita: `as any` sem Zod ✅ · `console.log` em vez
de pino ✅ · `require` dinâmico ✅ · `attendantEmail` (dado pessoal) logado ✅.

## Evidência de uso do Copilot (D2)
Anexar em `Exercício 3.2/` os prints do Copilot (revisão/reescrita).

## Resumo dos caminhos a inspecionar
```
Exercício 3.2/1 - revisao-e-comparacao.md                    (revisões + comparação, Tarefas 1 e 2)
novatech-assistant/src/functions/feedback/handler.ts         (código reescrito, Tarefa 3)
novatech-assistant/src/shared/config.ts                      (config centralizada)
Exercício 3.2/codigo-reescrito/handler.ts + config.ts        (cópia autossuficiente do código reescrito)
```
