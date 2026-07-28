# Exercício 3.2 — Revisão crítica de código gerado por IA (módulo de feedback)

> **Entregável:** a sua revisão, a revisão do Claude, a comparação, e o código reescrito.
> Código reescrito (Tarefa 3) em `novatech-assistant/src/functions/feedback/handler.ts`.

## Código revisado (gerado pelo "Copilot", fornecido no enunciado)
```ts
import { app, HttpRequest, HttpResponseInit } from '@azure/functions';
export async function feedbackHandler(request: HttpRequest): Promise<HttpResponseInit> {
  const body = await request.json() as any;
  const feedback = {
    queryId: body.queryId, rating: body.rating, comment: body.comment,
    attendantEmail: body.attendantEmail, timestamp: new Date().toISOString()
  };
  console.log('Feedback recebido:', JSON.stringify(feedback));
  const { CosmosClient } = require('@azure/cosmos');
  const client = new CosmosClient(process.env.COSMOS_CONNECTION_STRING);
  const database = client.database('novatech');
  const container = database.container('feedbacks');
  await container.items.create(feedback);
  return { status: 200, body: 'OK' };
}
app.http('feedback', { methods: ['POST'], handler: feedbackHandler });
```

Regras do AGENTS.md: TS strict · Zod no input · pino (nunca console.log) · nunca logar dado pessoal · imports estáticos (nunca require dinâmico).

## 1. Revisão do humano (feita antes do Claude)
- Não usou o padrão de log (console.log estava proibido). → violação AGENTS
- Não usou Zod. → violação AGENTS
- Está logando dados sensíveis. → segurança
- Não usou strict. → violação AGENTS

## 2. Revisão do Claude
**Violações do AGENTS.md**
1. `console.log(...)` em vez de pino.
2. Sem Zod — `body` usado sem schema.
3. `request.json() as any` — o `as any` contorna o strict e o "validar com Zod".
4. `require('@azure/cosmos')` dinâmico no meio da função (deveria ser import estático no topo).

**Segurança**
5. Loga `attendantEmail` (dado pessoal) — viola "nunca logar dados pessoais" (LGPD).
6. `COSMOS_CONNECTION_STRING` lido solto de `process.env`, sem validação/centralização.

**Bugs / robustez**
7. Sem validação: body sem `queryId`/`rating` grava lixo no Cosmos.
8. Sem tratamento de erro: `request.json()` e `items.create` podem lançar.
9. Cliente Cosmos criado a cada request (deveria ser singleton).
10. Resposta `200 'OK'` não estruturada (não retorna o id criado).

## 3. Comparação (humano × Claude)
| Problema | Humano | Claude |
|---|---|---|
| `console.log` em vez de pino | ✅ | ✅ |
| Sem Zod | ✅ | ✅ |
| Loga dado pessoal (`attendantEmail`) | ✅ | ✅ |
| `as any` / strict | ✅ (como "não usou strict") | ✅ (é o `as any` que contorna o strict) |
| `require` dinâmico | ❌ | ✅ |
| Sem tratamento de erro | ❌ | ✅ |
| Cliente Cosmos por request | ❌ | ✅ |
| Env sem validação / resposta não estruturada | ❌ | ✅ |

**Leitura honesta:** o humano acertou os 4 itens do núcleo exigido (console.log, sem Zod, dado pessoal, `as any`/strict); escapou o `require` dinâmico (também da lista mínima) e os bugs de robustez (erro/singleton). A revisão do humano focou nas violações de regra; a do Claude somou os problemas de runtime.
**Ajuste de precisão:** "não usou strict" → o strict já está ligado no projeto; o problema é o `as any` que o **contorna**.

## 4. Reescrita (Copilot) + verificação
Código reescrito em `novatech-assistant/src/functions/feedback/handler.ts` (+ `src/shared/config.ts`
com `getCosmosConnectionString()`). Os 10 pontos foram corrigidos:

| Item da revisão | Corrigido na reescrita? |
|---|---|
| console.log → pino | ✅ `withRequestId`, `log.info/warn/error` |
| Sem Zod | ✅ `feedbackRequestSchema` (queryId, rating 1..5, comment?, email) |
| `as any` | ✅ `unknown` + `safeParse` |
| `require` dinâmico | ✅ `import { CosmosClient } from "@azure/cosmos"` no topo |
| Loga `attendantEmail` | ✅ loga só `queryId`/`rating`/`feedbackId`; e-mail armazenado, não logado |
| Env sem centralização | ✅ `getCosmosConnectionString()` em `config.ts` |
| Sem validação | ✅ Zod (400 em input inválido) |
| Sem tratamento de erro | ✅ try/catch no parse e na escrita (400/500) |
| Cliente por request | ✅ singleton fora do handler |
| Resposta não estruturada | ✅ 201 `jsonBody { id }` |

### Resíduos (revisão da reescrita) — corrigidos
1. ✅ `@azure/cosmos` adicionado ao `package.json` (`^4.0.0`). Falta só rodar `npm install` localmente.
2. ✅ `config.ts` regravado em UTF-8 **sem BOM**.
3. ✅ Singleton refatorado para **init preguiçoso** (`getFeedbackContainer()`): o client é criado na
   1ª requisição, não no load do módulo — importar o handler (ex.: em teste) não exige env nem conecta;
   config ausente vira 500 na requisição, não crash de startup; o client segue reutilizado.

