// Acesso centralizado à configuração da aplicação.
// Lê variáveis de ambiente obrigatórias e falha de forma clara quando ausentes.

export function getCosmosConnectionString(): string {
  const value = process.env.COSMOS_CONNECTION_STRING;
  if (!value) {
    throw new Error("Missing required environment variable: COSMOS_CONNECTION_STRING");
  }
  return value;
}
