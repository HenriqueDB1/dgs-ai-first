// Logger estruturado da aplicação (AGENTS.md: usar pino; sem console.log; logs em JSON).
// Nível lido de env (LOG_LEVEL); default "info".

import pino from "pino";

export const logger = pino({
  level: process.env.LOG_LEVEL ?? "info",
  base: { service: "novatech-assistant" },
});

/**
 * Cria um logger filho com correlação por `requestId` (QE-07).
 * Todo log emitido por ele carrega o mesmo `requestId`, ligando as linhas de uma requisição.
 */
export function withRequestId(requestId: string): pino.Logger {
  return logger.child({ requestId });
}
