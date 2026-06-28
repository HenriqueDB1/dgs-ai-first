"""
Passo 5 — Teste com 5 perguntas do Anexo B (mapa de cobertura).

Para cada pergunta:
  1. Monta o prompt completo via RAG (busca + montar_prompt)
  2. Exibe os chunks recuperados (fonte, seção, score)
  3. Salva o prompt completo em prompt_{N}.txt para envio manual ao LLM

Após rodar, cole os resultados no chat para geração do relatório.
"""

import os
from montar_prompt import montar_prompt

# ─── 5 perguntas selecionadas do mapa de cobertura (Anexo B) ─────

PERGUNTAS = [
    {
        "id": 1,
        "pergunta": "Qual o prazo de devolução?",
    },
    {
        "id": 2,
        "pergunta": "Posso devolver carga perigosa?",
    },
    {
        "id": 3,
        "pergunta": "Meu cliente é Gold. Qual o SLA de resolução?",
    },
    {
        "id": 4,
        "pergunta": "O cliente diz que é Platinum. Qual o SLA dele?",
    },
    {
        "id": 5,
        "pergunta": "Quanto custa o frete para 600kg para Manaus?",
    },
]

# ─── Execução ─────────────────────────────────────────────────────

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

print("=" * 70)
print("TESTE DO PIPELINE RAG — 5 PERGUNTAS DO ANEXO B")
print("=" * 70)

for item in PERGUNTAS:
    pid = item["id"]
    pergunta = item["pergunta"]

    print(f"\n{'─'*70}")
    print(f"[Pergunta {pid}] {pergunta}")

    resultado = montar_prompt(pergunta)
    chunks = resultado["chunks"]

    print(f"\n{'#':<4} {'Score':<8} {'Fonte':<40} Seção")
    print(f"{'─'*4} {'─'*8} {'─'*40} {'─'*40}")
    for i, c in enumerate(chunks):
        fonte = c["source"].replace(".md", "")
        secao = c["section"]
        print(f"{i+1:<4} {c['score']:<8.4f} {fonte:<40} {secao}")

    arquivo_prompt = os.path.join(OUTPUT_DIR, f"prompt_{pid}.txt")
    with open(arquivo_prompt, "w", encoding="utf-8") as f:
        f.write("=== SYSTEM PROMPT ===\n\n")
        f.write(resultado["system"])
        f.write("\n\n=== USER MESSAGE ===\n\n")
        f.write(resultado["user"])

    print(f"\n  ✅ Prompt salvo em: prompt_{pid}.txt")

print(f"\n{'='*70}")
print("Prompts gerados (prompt_1.txt … prompt_5.txt).")
print("Cole os resultados acima no chat para geração do relatório.")
print("=" * 70)
