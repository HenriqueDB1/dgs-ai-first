# Mapeamento de Contexto — Rodada 2

**System prompt:** v2 (9 regras)
**Chunks:** do Anexo B, selecionados por pergunta (conversa separada por questão)

---

## Estrutura de contexto por mensagem

A Rodada 2 foi executada em 3 conversas independentes — uma por pergunta. A ordem adotada foi a mesma da Rodada 1:

```
[1] System prompt (estático)
[2] Pergunta do atendente (dinâmico)
[3] Chunks selecionados (dinâmico)
```

Os chunks foram posicionados ao final — após a pergunta — para ficarem na extremidade do contexto e reduzirem o efeito *lost in the middle*. A separação em conversas independentes simulou com mais fidelidade o comportamento de produção de um pipeline RAG: cada query recebe apenas os chunks relevantes para aquela pergunta específica.

---

## Partes estáticas

Enviadas em toda query. Não mudam entre perguntas.

| Seção | Descrição | Palavras aprox. | Tokens aprox. |
|-------|-----------|-----------------|---------------|
| Contexto operacional | Descrição da NovaTech, equipe, stack Microsoft | 80 | 107 |
| Identidade | Papel do assistente e sua natureza documental | 70 | 93 |
| Regras obrigatórias (9 regras) | Guardrails v2: inclui regras 6–9 (SLA, tier inexistente, FAQ único, multi-domínio) | 350 | 467 |
| Prioridade entre fontes | Hierarquia de documentos conflitantes + exemplo PROC-042 | 90 | 120 |
| Instruções para uso dos chunks | Como tratar cada tipo de fonte (normativo vs FAQ) | 80 | 107 |
| Formato de resposta | Estrutura obrigatória: Resposta / Fonte(s) / Observação | 40 | 53 |
| **Total estático** | | **710** | **~947** |

*O crescimento de ~200 tokens em relação à Rodada 1 deve-se à adição das regras 6 a 9 no system prompt v2.*

---

## Partes dinâmicas

Mudam a cada query. Na Rodada 2, cada conversa recebeu apenas os chunks relevantes para aquela pergunta.

### Pergunta 1 — "Qual o prazo de devolução para carga perigosa?"

| Chunk | Conteúdo | Palavras aprox. | Tokens aprox. |
|-------|----------|-----------------|---------------|
| POL-001-A — Seção 3.1 | Prazo geral de 7 dias úteis | 40 | 53 |
| POL-001-B — Seção 3.2 | Exceções: cargas perigosas + ramal 4500 | 90 | 120 |
| Pergunta do atendente | "Qual o prazo de devolução para carga perigosa?" | 8 | 11 |
| **Total dinâmico** | | **138** | **~184** |
| **Total da query** | | **848** | **~1.131** |

### Pergunta 2 — "Meu cliente é Gold, qual o SLA de resolução?"

| Chunk | Conteúdo | Palavras aprox. | Tokens aprox. |
|-------|----------|-----------------|---------------|
| SLA-2024-A — Seção 1 | Classificação de tiers (Gold, Silver, Standard) | 60 | 80 |
| SLA-2024-B — Seção 2 | SLAs para chamados gerais | 40 | 53 |
| SLA-2024-C — Seção 2 | SLAs para incidentes críticos | 30 | 40 |
| Pergunta do atendente | "Meu cliente é Gold, qual o SLA de resolução?" | 9 | 12 |
| **Total dinâmico** | | **139** | **~185** |
| **Total da query** | | **849** | **~1.132** |

### Pergunta 3 — "Quanto custa o frete para 600kg para Manaus?"

| Chunk | Conteúdo | Palavras aprox. | Tokens aprox. |
|-------|----------|-----------------|---------------|
| PROC-042-B — Seção 2.1 | Multiplicadores regionais v1 (março/2023) — incluído intencionalmente para testar conflito | 20 | 27 |
| PROC-042v2-A — Seção 2 | Fórmula completa com fator de peso (novembro/2023) | 60 | 80 |
| PROC-042v2-B — Seção 2.1 | Multiplicadores regionais v2 (novembro/2023) | 20 | 27 |
| Pergunta do atendente | "Quanto custa o frete para 600kg para Manaus?" | 9 | 12 |
| **Total dinâmico** | | **109** | **~146** |
| **Total da query** | | **819** | **~1.093** |

---

## Resumo do orçamento de contexto

| Query | Estático | Dinâmico | Total | % da janela (128K) |
|-------|----------|----------|-------|---------------------|
| Pergunta 1 | ~947 | ~184 | ~1.131 | < 1% |
| Pergunta 2 | ~947 | ~185 | ~1.132 | < 1% |
| Pergunta 3 | ~947 | ~146 | ~1.093 | < 1% |

O orçamento de contexto não é gargalo. Em produção, com dezenas de chunks por query e histórico de conversa acumulado, esse número cresceria significativamente — mas ainda estaria dentro da janela de 128K do GPT-4o.

---

## Melhoria da Rodada 1 para a Rodada 2

| Aspecto | Rodada 1 | Rodada 2 |
|---------|----------|----------|
| Chunks por query | 3 fixos (A, B e C) independente da pergunta | Selecionados por relevância para cada pergunta |
| Conversas | 1 (todas as perguntas em sequência) | 3 (uma por pergunta) |
| Isolamento de contexto | ❌ Chunks irrelevantes presentes | ✅ Apenas chunks relevantes por query |
| Simulação de RAG | Parcial | Mais fiel ao comportamento de produção |
