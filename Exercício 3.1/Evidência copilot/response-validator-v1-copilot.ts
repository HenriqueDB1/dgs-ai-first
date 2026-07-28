import { z } from "zod";
import { logger } from "../shared/logger.js";

export const responseSchema = z
  .object({
    answer: z.string().min(1, { message: "answer must be a non-empty string" }),
    source_document: z.string().min(1, { message: "source_document must be a non-empty string" }),
    confidence_score: z.number().min(0, { message: "confidence_score must be >= 0" }).max(1, { message: "confidence_score must be <= 1" }),
  })
  .strict();

export type ResponseOutput = z.infer<typeof responseSchema>;

const SAFE_RESPONSE: ResponseOutput = {
  answer: "Não foi possível fornecer uma resposta confiável no momento; encaminhe ao supervisor.",
  source_document: "N/A - encaminhar ao supervisor",
  confidence_score: 0,
};

export function validateResponse(raw: unknown): ResponseOutput {
  const parsed = responseSchema.safeParse(raw);
  if (!parsed.success) {
    logger.warn({ issues: parsed.error.issues }, "response-validator: schema validation failed.");
    return SAFE_RESPONSE;
  }

  const data = parsed.data;

  // Guardrail 1: source_document deve existir e ser não-vazio (defesa em profundidade).
  if (data.source_document.trim().length === 0) {
    logger.warn({ data }, "response-validator: rejected due to empty source_document.");
    return SAFE_RESPONSE;
  }

  // Guardrail 2: respostas que mencionam "carga perigosa" e "devolução" e afirmam que devolução é possível
  // (não apresentam negação) devem ser bloqueadas.
  const answerLower = data.answer.toLowerCase();
  const mentionsCarga = answerLower.includes("carga perigosa");
  const mentionsDevolucao = answerLower.includes("devolução") || answerLower.includes("devolucao");

  if (mentionsCarga && mentionsDevolucao) {
    const negativeIndicators = [
      "não",
      "nao",
      "impossível",
      "impossivel",
      "inviável",
      "inviavel",
      "impraticável",
      "impraticavel",
      "não é",
      "nao é",
      "não será",
      "nao sera",
      "não pode",
      "nao pode",
      "não é possível",
      "nao é possivel",
    ];

    const hasNegation = negativeIndicators.some((neg) => answerLower.includes(neg));

    if (!hasNegation) {
      logger.warn({ answer: data.answer }, "response-validator: blocked answer that affirms return of hazardous cargo.");
      return SAFE_RESPONSE;
    }
  }

  return data;
}
