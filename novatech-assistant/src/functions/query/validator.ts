// Schema Zod do input do endpoint POST /api/query (AGENTS.md: validação de input mora no validator.ts).
// Não validar "na mão" — o handler consome este schema.

import { z } from "zod";
import type { QueryRequest } from "../../shared/types.js";

const MAX_QUESTION_LENGTH = 1000;

/**
 * Schema de validação do corpo da requisição.
 * - `question`: obrigatória, não vazia (após trim) e no máximo 1000 caracteres.
 * - `conversationId`: opcional; se presente, não pode ser string vazia.
 * O tipo inferido é compatível com {@link QueryRequest}.
 */
export const queryRequestSchema = z.object({
  question: z
    .string({ required_error: "question é obrigatória.", invalid_type_error: "question deve ser uma string." })
    .trim()
    .min(1, "question não pode ser vazia.")
    .max(MAX_QUESTION_LENGTH, `question não pode exceder ${MAX_QUESTION_LENGTH} caracteres.`),
  conversationId: z
    .string({ invalid_type_error: "conversationId deve ser uma string." })
    .min(1, "conversationId não pode ser vazio.")
    .optional(),
});

// Garante, em tempo de compilação, que o schema permanece alinhado ao contrato de domínio.
type _AlignedWithDomain = z.infer<typeof queryRequestSchema> extends QueryRequest ? true : never;
const _assertAligned: _AlignedWithDomain = true;
void _assertAligned;
