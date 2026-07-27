<!--
EVIDÊNCIA — v1 gerado pelo GitHub Copilot (CLI), do zero, a partir do prompt.
Reproduzido verbatim para avaliação. Análise em "Exercício 2.3/2 - evidencia-copilot-e-reflexao.md".
-->
---
name: typescript-conventions
description: Foundation TypeScript conventions for strict ESM projects using Zod, pino, and Azure Functions v4
---
# Context
This skill defines TypeScript conventions for projects using:
- TypeScript with `strict` mode enabled
- ECMAScript modules (ESM)
- Zod for runtime validation and schema inference
- pino for structured logging
- Azure Functions v4 as the serverless runtime
The goal is consistent, safe, and maintainable TypeScript code across functions, validation, logging, and module boundaries.
# Rules
1. Enable and respect strict TypeScript settings:
   - `strict: true`
   - `noImplicitAny`, `strictNullChecks`, `strictPropertyInitialization`, `noImplicitReturns`, `noUncheckedIndexedAccess`
   - Prefer explicit typing for public APIs and function boundaries.
2. Always use ESM import/export syntax:
   - `import { x } from "./x.js"`
   - `export const handler = ...`
   - Avoid `require`, `module.exports`, and default exports in shared libraries.
3. Prefer typed function signatures and return types:
   - Export handlers with explicit Azure Function types (`AzureFunction`, `Context`, `HttpRequest`).
   - Do not rely on inferred `any` for request or response shapes.
4. Use Zod for validation and inference:
   - Define request, response, and config shapes with `z.object(...)`.
   - Use `z.infer<typeof schema>` for type inference.
   - Validate as early as possible, especially at Azure Function entrypoints.
5. Keep runtime validation and compile-time types aligned:
   - Avoid separate duplicated TS interfaces for the same payload.
   - Use Zod schemas as the single source of truth.
6. Log structured context with pino:
   - Use child loggers or bound loggers for per-request metadata.
   - Avoid plain `console.log`; use `logger.info`, `logger.error`, `logger.debug`.
   - Include useful context such as request id, function name, and correlation ids.
7. Keep Azure Function execution fast and side-effect aware:
   - Do not perform heavy work before validation.
   - Keep context binding and response creation clear and explicit.
8. Prefer immutable values and functional patterns:
   - Use `const` by default.
   - Avoid mutating request objects, config, or shared state.
9. Fail fast when validation or required environment config is missing:
   - Throw or return a meaningful Azure Function error response on invalid input.
   - Do not silently ignore invalid payloads or missing env vars.
10. Organize modules by responsibility:
    - Validation schemas, handlers, and shared utilities should be separate but small.
    - Export only the minimal public API needed.
# DO
- `import { z } from "zod";`
- `import { AzureFunction, Context, HttpRequest } from "@azure/functions";`
- `const schema = z.object({ userId: z.string().uuid() });`
- `type RequestBody = z.infer<typeof schema>;`
- `const parsed = schema.safeParse(req.body);`
- `if (!parsed.success) return badRequest(context, parsed.error);`
- `const logger = pino({ level: "info" });`
- `logger.info({ functionName: "userCreate", requestId }, "handling request");`
- `export const httpTrigger: AzureFunction = async (context, req) => { ... };`
- `const envSchema = z.object({ DATABASE_URL: z.string().url() });`
- `export const config = envSchema.parse(process.env);`
# DON'T
- Do not use `any` or disable strict checks with `// @ts-ignore`
- Do not use `require()` or `module.exports`
- Do not parse JSON manually instead of Zod validation
- Do not log unstructured strings with `console.log`
- Do not mutate `req.body` or `context.bindingData`
- Do not define separate TS interfaces and Zod schemas for the same shape
- Do not assume runtime data matches compile-time types
- Do not return ambiguous responses without explicit status codes
- Do not use default exports for shared Azure Function utilities
- Do not rely on non-null assertions (`!`) to silence type errors instead of fixing the contract
# Anti-patterns
- `const body: any = req.body;` followed by unchecked property access.
- `const data = schema.parse(req.body);` inside deep business logic instead of at the entrypoint.
- `export default function handler(...) { ... }` in Azure Functions code.
- `logger.info("user created");` without structured properties for correlation.
- `const config = { db: process.env.DB_URL! };` using `!` to bypass missing env detection.
- Building response objects with loose object literals rather than typed helpers.
- Mixing `import` with `require` in the same file.
- Using `const foo = JSON.parse(req.body as string);` instead of Zod validation.
- Embedding environment-specific strings or untyped constants directly in handler code.
