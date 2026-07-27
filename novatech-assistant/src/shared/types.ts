// Tipos de domínio compartilhados (AGENTS.md: "Tipos de domínio compartilhados em src/shared/types.ts").
// Contrato de entrada/saída do endpoint POST /api/query.

/** Corpo da requisição do endpoint POST /api/query. */
export interface QueryRequest {
  /** Pergunta do atendente, em linguagem natural. */
  question: string;
  /** Identificador opcional da conversa (usado para histórico multi-turno — ADR-0002). */
  conversationId?: string;
}

/** Fonte citada em uma resposta. Guardrail (AGENTS.md): toda resposta cita a fonte. */
export interface SourceReference {
  /** Documento oficial de origem do chunk usado na resposta. */
  documentId: string;
  /** Título legível do documento, para exibição ao atendente. */
  title: string;
}

/**
 * Resposta do endpoint POST /api/query.
 * O schema Zod de saída e o formato final são responsabilidade da QE-06.
 */
export interface QueryResponse {
  /** Resposta gerada, fundamentada nos chunks recuperados. */
  answer: string;
  /** Fontes citadas (referentes aos chunks usados). Vazio no stub da QE-01. */
  sources: SourceReference[];
}
