// HTTP trigger do endpoint POST /api/feedback — Azure Functions v4
// Reescrito conforme AGENTS.md: TypeScript strict, ESM, Zod validation, pino logger, Cosmos client reutilizado.

import { app, type HttpRequest, type HttpResponseInit, type InvocationContext } from "@azure/functions";
import { z } from "zod";
import { CosmosClient, type Container } from "@azure/cosmos";
import { randomUUID } from "crypto";
import { withRequestId } from "../../shared/logger.js";
import { getCosmosConnectionString } from "../../shared/config.js";

// Zod schema para validação de entrada.
const feedbackRequestSchema = z.object({
  queryId: z.string().min(1, "queryId não pode ser vazio"),
  rating: z.number().int().min(1).max(5),
  comment: z.string().optional(),
  attendantEmail: z.string().email(),
});

type FeedbackRequest = z.infer<typeof feedbackRequestSchema>;

// Cosmos container reutilizado (singleton via init preguiçoso).
// Criado na 1ª chamada — NÃO no load do módulo — para que importar este arquivo (ex.: em testes)
// não exija a env nem tente conectar. A falha de config vira 500 na requisição, não crash de startup.
let container: Container | undefined;
function getFeedbackContainer(): Container {
  if (!container) {
    const client = new CosmosClient(getCosmosConnectionString());
    container = client.database("novatech").container("feedbacks");
  }
  return container;
}

export async function feedbackHandler(
  request: HttpRequest,
  context: InvocationContext,
): Promise<HttpResponseInit> {
  const log = withRequestId(context.invocationId);

  // Ler corpo como JSON — erro sintático do JSON => 400.
  let rawBody: unknown;
  try {
    rawBody = await request.json();
  } catch {
    log.warn("feedback: corpo da requisição não é JSON válido.");
    return {
      status: 400,
      jsonBody: { error: "Corpo da requisição inválido: JSON malformado." },
    };
  }

  // Validar com Zod. Input inválido => 400 com detalhes.
  const parsed = feedbackRequestSchema.safeParse(rawBody);
  if (!parsed.success) {
    log.warn({ issues: parsed.error.issues }, "feedback: input reprovado na validação de schema.");
    return {
      status: 400,
      jsonBody: {
        error: "Falha de validação do input.",
        details: parsed.error.flatten(),
      },
    };
  }

  const data: FeedbackRequest = parsed.data;

  // Nunca logar dados pessoais (attendantEmail). Logar somente campos não sensíveis.
  log.info({ queryId: data.queryId, rating: data.rating }, "feedback: recebendo feedback.");

  const feedbackDocument = {
    id: randomUUID(),
    queryId: data.queryId,
    rating: data.rating,
    comment: data.comment ?? null,
    attendantEmail: data.attendantEmail, // armazenado, mas NÃO logado
    createdAt: new Date().toISOString(),
  };

  // Persistência com tratamento de erro — não vazar detalhes internos.
  try {
    const { resource } = await getFeedbackContainer().items.create(feedbackDocument);
    log.info(
      { queryId: data.queryId, rating: data.rating, feedbackId: resource?.id },
      "feedback: gravado com sucesso.",
    );
    return {
      status: 201,
      jsonBody: { id: resource?.id },
    };
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    log.error({ err: message }, "feedback: falha ao persistir o feedback.");
    return {
      status: 500,
      jsonBody: { error: "Erro interno ao persistir o feedback." },
    };
  }
}

app.http("feedback", {
  methods: ["POST"],
  authLevel: "function",
  route: "feedback",
  handler: feedbackHandler,
});
