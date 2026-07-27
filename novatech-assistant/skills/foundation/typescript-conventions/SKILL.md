---
name: typescript-conventions
description: >-
  Convenções de TypeScript do NovaTech Assistant. Use ao escrever ou gerar qualquer
  código TypeScript no projeto (endpoints, serviços, testes, componentes React). Define
  strict mode, imports ESM, Zod nas bordas, logging com pino, imutabilidade e os
  anti-padrões a barrar. É a skill Foundation base — as demais skills a pressupõem.
---

# TypeScript Conventions (Foundation)

**Tier:** Foundation · **Base de:** todas as outras skills (Domain e Artifact) pressupõem estas convenções.

## Contexto
Skill Foundation basilar do NovaTech Assistant. Todo código gerado — endpoints, serviços, testes,
componentes — nasce em TypeScript e **deve** seguir as regras abaixo. As skills de Domain e Artifact
referenciam esta skill em vez de repetir convenções. Stack: TypeScript strict, ESM
(`"type": "module"`), Azure Functions v4, Zod, pino.

## Regras prescritivas (obrigatórias)
1. **`strict: true` sempre** — inclua também `noUncheckedIndexedAccess` e `noImplicitReturns`.
   Proibido `any`; use `unknown` + narrowing quando o tipo for incerto.
2. **ESM com extensão nos imports relativos:** `import { x } from "./validator.js"` (o `.js` é
   obrigatório em ESM no runtime Node, mesmo o arquivo sendo `.ts`).
3. **Named exports** — nada de `export default` (facilita refactor e rastreio de uso).
4. **Tipos explícitos no contorno:** funções exportadas declaram tipos de parâmetro e de retorno.
5. **Tipos de domínio** ficam em `src/shared/types.ts` e são importados; não redeclarar localmente.
6. **Validação nas bordas com Zod** (input/output); nunca validar "na mão" com `if`s espalhados.
7. **Sem `console.*`** — usar o logger `pino` de `src/shared/logger.ts`.
8. **Sem non-null assertion (`!`)** e sem type assertion (`as`) para "calar" o compilador; corrigir o tipo
   (use type guards `x is T` para estreitar `unknown`).
9. **Imutabilidade por padrão:** `const`, `readonly` em campos que não mudam; evitar mutação de parâmetros.
10. **`async/await`** com erros tratados; nada de promise solta (floating promise).

## DO / DON'T

**DO — type guard para estreitar `unknown` (sem `as`):**
```ts
function hasName(input: unknown): input is { name: unknown } {
  return typeof input === "object" && input !== null && "name" in input;
}

function getName(input: unknown): string {
  if (!hasName(input)) throw new ValidationError("input sem 'name'");
  return String(input.name); // já estreitado pelo type guard — sem `as`
}
```
**DON'T:**
```ts
function getName(input: any): string {
  return input.name; // any desliga o compilador; quebra em runtime
}
```

**DO — export nomeado + tipos explícitos + import ESM:**
```ts
import type { QueryRequest } from "../../shared/types.js";
export function buildKey(req: QueryRequest): string { ... }
```
**DON'T:**
```ts
export default function (req) { ... } // default export + parâmetro sem tipo
```

**DO — logger estruturado:**
```ts
import { logger } from "../../shared/logger.js";
logger.info({ requestId }, "query recebida");
```
**DON'T:**
```ts
console.log("query recebida " + requestId); // console.* proibido; concatena string
```

## Anti-padrões (o que a IA tende a gerar e deve ser barrado)
- **`any` implícito ou explícito** — inclusive `catch (e)` usando `e` sem `e: unknown` + narrowing.
- **Import relativo sem `.js`** (`from "./validator"`) — compila com `moduleResolution` de bundler,
  mas **quebra no runtime ESM do Node**.
- **`export default`** — some do autocomplete e dificulta "find references".
- **`as SomeType` / `!`** para silenciar erro do compilador em vez de tipar corretamente (use type guard).
- **`console.log` de debug** deixado no código — viola o padrão de logging e polui a saída.
- **Redeclarar tipos** de domínio localmente em vez de importar de `src/shared/types.ts`.
- **Configuração de ambiente lida diretamente em vários pontos** — centralizar em `src/shared/config.ts`.

## Como as outras skills usam esta
- `error-handling`, `logging`, `env-config` assumem strict + narrowing + ESM daqui.
- Toda skill de Domain/Artifact que gera `.ts` referencia: "seguir `typescript-conventions`".
