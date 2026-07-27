import { describe, expect, it } from "vitest";
import { queryRequestSchema } from "../../src/functions/query/validator.js";

describe("queryRequestSchema", () => {
  it("aceita uma pergunta válida sem conversationId", () => {
    const result = queryRequestSchema.safeParse({ question: "Qual o prazo de troca?" });
    expect(result.success).toBe(true);
  });

  it("aceita uma pergunta válida com conversationId", () => {
    const result = queryRequestSchema.safeParse({
      question: "E a garantia?",
      conversationId: "conv-123",
    });
    expect(result.success).toBe(true);
  });

  it("faz trim da pergunta", () => {
    const result = queryRequestSchema.safeParse({ question: "  olá  " });
    expect(result.success).toBe(true);
    if (result.success) expect(result.data.question).toBe("olá");
  });

  it("rejeita quando question está ausente", () => {
    const result = queryRequestSchema.safeParse({});
    expect(result.success).toBe(false);
  });

  it("rejeita question vazia", () => {
    const result = queryRequestSchema.safeParse({ question: "" });
    expect(result.success).toBe(false);
  });

  it("rejeita question só com espaços", () => {
    const result = queryRequestSchema.safeParse({ question: "     " });
    expect(result.success).toBe(false);
  });

  it("rejeita question acima de 1000 caracteres", () => {
    const result = queryRequestSchema.safeParse({ question: "a".repeat(1001) });
    expect(result.success).toBe(false);
  });

  it("aceita question com exatamente 1000 caracteres", () => {
    const result = queryRequestSchema.safeParse({ question: "a".repeat(1000) });
    expect(result.success).toBe(true);
  });

  it("rejeita question de tipo errado", () => {
    const result = queryRequestSchema.safeParse({ question: 42 });
    expect(result.success).toBe(false);
  });

  it("rejeita conversationId vazio quando presente", () => {
    const result = queryRequestSchema.safeParse({ question: "ok", conversationId: "" });
    expect(result.success).toBe(false);
  });
});
