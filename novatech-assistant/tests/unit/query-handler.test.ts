import type { HttpRequest, InvocationContext } from "@azure/functions";
import { describe, expect, it } from "vitest";
import { queryHandler } from "../../src/functions/query/handler.js";

// Mocks mínimos: o handler só usa request.json() e context.invocationId.
function makeRequest(json: () => Promise<unknown>): HttpRequest {
  return { json } as unknown as HttpRequest;
}

function makeContext(): InvocationContext {
  return { invocationId: "test-invocation" } as unknown as InvocationContext;
}

describe("queryHandler", () => {
  it("retorna 200 com stub quando o input é válido", async () => {
    const res = await queryHandler(
      makeRequest(async () => ({ question: "Qual o prazo de troca?" })),
      makeContext(),
    );

    expect(res.status).toBe(200);
    const body = res.jsonBody as { answer: string; sources: unknown[] };
    expect(typeof body.answer).toBe("string");
    expect(body.sources).toEqual([]);
  });

  it("retorna 400 com detalhe quando question está ausente", async () => {
    const res = await queryHandler(
      makeRequest(async () => ({})),
      makeContext(),
    );

    expect(res.status).toBe(400);
    const body = res.jsonBody as { error: string; details: unknown };
    expect(body.error).toContain("validação");
    expect(body.details).toBeDefined();
  });

  it("retorna 400 quando question está vazia", async () => {
    const res = await queryHandler(
      makeRequest(async () => ({ question: "   " })),
      makeContext(),
    );
    expect(res.status).toBe(400);
  });

  it("retorna 400 quando o corpo não é JSON válido", async () => {
    const res = await queryHandler(
      makeRequest(async () => {
        throw new SyntaxError("Unexpected token");
      }),
      makeContext(),
    );

    expect(res.status).toBe(400);
    const body = res.jsonBody as { error: string };
    expect(body.error).toContain("JSON malformado");
  });
});
