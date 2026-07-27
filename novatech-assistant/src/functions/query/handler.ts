// HTTP trigger do query endpoint — POST /api/query (Azure Functions v4).
// QE-01: validação de input (Zod) + resposta stub. O fluxo RAG
// (embedding → busca → prompt → completion) é implementado em QE-02..QE-06.
// Padrões (AGENTS.md): TypeScript strict, ESM, Zod, logger pino (sem console.log).

import { app, type HttpRequest, type HttpResponseInit, type InvocationContext } from "@azure/functions";
import { queryRequestSchema } from "./validator.js";
import { withRequestId } from "../../shared/logger.js";
import type { QueryResponse } from "../../shared/types.js";

export async function queryHandler(
  request: HttpRequest,
  context: InvocationContext,
): Promise<HttpResponseInit> {
  const log = withRequestId(context.invocationId);

  // Corpo precisa ser JSON válido antes de passar pela validação de schema.
  let rawBody: unknown;
  try {
    rawBody = await request.json();
  } catch {
    log.warn("query: corpo da requisição não é JSON válido.");
    return {
      status: 400,
      jsonBody: { error: "Corpo da requisição inválido: JSON malformado." },
    };
  }

  // Validação de input via Zod. Input inválido → 400 com o detalhe do erro.
  const parsed = queryRequestSchema.safeParse(rawBody);
  if (!parsed.success) {
    log.warn({ issues: parsed.error.issues }, "query: input reprovado na validação de schema.");
    return {
      status: 400,
      jsonBody: {
        error: "Falha de validação do input.",
        details: parsed.error.flatten(),
      },
    };
  }

  // Input válido. Stub enquanto o fluxo RAG não está completo (QE-02..QE-06).
  log.info("query: input válido; retornando stub (fluxo RAG pendente — QE-02..QE-06).");
  const response: QueryResponse = {
    answer:
      "Endpoint disponível. O fluxo de recuperação e geração de resposta ainda não está implementado (QE-02..QE-06).",
    sources: [],
  };

  return { status: 200, jsonBody: response };
}

app.http("query", {
  methods: ["POST"],
  authLevel: "function",
  route: "query",
  handler: queryHandler,
});
