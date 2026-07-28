import { z } from "zod";
import { logger } from "../shared/logger.js";

// Rejeita string vazia OU só de espaços (o `.min(1)` sozinho aceita " ").
const nonBlank = (field: string) =>
  z.string().trim().min(1, { message: `${field} must be a non-empty string` });

export const responseSchema = z
  .object({
    answer: nonBlank("answer"),
    source_document: nonBlank("source_document"),
    confidence_score: z
      .number()
      .min(0, { message: "confidence_score must be >= 0" })
      .max(1, { message: "confidence_score must be <= 1" }),
  })
  .strict();

export type ResponseOutput = z.infer<typeof responseSchema>;

const SAFE_RESPONSE: ResponseOutput = {
  answer: "Não foi possível fornecer uma resposta confiável no momento; encaminhe ao supervisor.",
  source_document: "N/A",
  confidence_score: 0,
};

// Normaliza acentos + caixa para casar variações de forma determinística.
function normalize(text: string): string {
  return text.normalize("NFD").replace(/\p{Diacritic}/gu, "").toLowerCase();
}

// Gatilhos por radical: cobre singular/plural e formas verbais.
const HAZARD_RE = /cargas?\s+perigosas?/; // carga(s) perigosa(s)
const RETURN_RE = /devolu|devolv/; // devolucao, devolver, devolvida...

// Negativa EXPLÍCITA da devolução. Fail-closed: exige uma destas para NÃO bloquear.
const EXPLICIT_DENIAL_RE =
  /nao (pode|e possivel|e elegivel|sera|deve)|nao elegivel|proibid|vedad|excluid|nao permit|nao aceit/;

/**
 * Valida o structured output do assistente e aplica os guardrails determinísticos.
 * Em qualquer falha, registra o motivo (pino) e retorna uma resposta padrão segura.
 */
export function validateResponse(raw: unknown): ResponseOutput {
  // 1) Structured output: precisa bater com o schema (senão rejeita).
  const parsed = responseSchema.safeParse(raw);
  if (!parsed.success) {
    logger.warn({ issues: parsed.error.issues }, "response-validator: schema validation failed.");
    return SAFE_RESPONSE;
  }
  const data = parsed.data;

  // 2) Guardrail 1 — source_document presente (o schema já garante; defesa explícita).
  if (data.source_document.trim().length === 0) {
    logger.warn("response-validator: rejected due to empty source_document.");
    return SAFE_RESPONSE;
  }

  // 3) Guardrail 2 — carga perigosa + devolução exige negativa EXPLÍCITA (fail-closed).
  const a = normalize(data.answer);
  if (HAZARD_RE.test(a) && RETURN_RE.test(a) && !EXPLICIT_DENIAL_RE.test(a)) {
    logger.warn(
      { answer: data.answer },
      "response-validator: blocked — carga perigosa + devolução sem negativa explícita.",
    );
    return SAFE_RESPONSE;
  }

  return data;
}
