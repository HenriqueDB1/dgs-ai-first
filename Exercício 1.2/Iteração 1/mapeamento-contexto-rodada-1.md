# Mapeamento de Contexto — Rodada 1

**System prompt:** v1 (5 regras)
**Chunks:** A, B e C do enunciado (simplificados, compartilhados nas 3 perguntas)

---

## Estrutura de contexto por mensagem

A Rodada 1 foi executada em uma única conversa. O sistema prompt foi enviado na primeira mensagem, seguido da pergunta e dos chunks. A ordem adotada foi:

```
[1] System prompt (estático)
[2] Pergunta do atendente (dinâmico)
[3] Chunks A, B e C (dinâmico)
```

Os chunks foram posicionados ao final da mensagem — após a pergunta — para ficarem na extremidade do contexto e reduzirem o efeito *lost in the middle*: informações posicionadas no meio de contextos longos tendem a receber menos atenção do modelo durante a geração.

---

## Partes estáticas

Enviadas em toda query. Não mudam entre perguntas.

| Seção | Descrição | Palavras aprox. | Tokens aprox. |
|-------|-----------|-----------------|---------------|
| Contexto operacional | Descrição da NovaTech, equipe, stack Microsoft | 80 | 107 |
| Identidade | Papel do assistente e sua natureza documental | 70 | 93 |
| Regras obrigatórias (5 regras) | Guardrails: citar fonte, não inventar, escalar, português, exceções | 200 | 267 |
| Prioridade entre fontes | Hierarquia de documentos conflitantes + exemplo PROC-042 | 90 | 120 |
| Instruções para uso dos chunks | Como tratar cada tipo de fonte (normativo vs FAQ) | 80 | 107 |
| Formato de resposta | Estrutura obrigatória: Resposta / Fonte(s) / Observação | 40 | 53 |
| **Total estático** | | **560** | **~747** |

---

## Partes dinâmicas

Mudam a cada query. Injetadas pelo usuário a cada pergunta.

### Chunks (variam por pergunta — mas na Rodada 1 os 3 foram enviados juntos em todas as queries)

| Chunk | Conteúdo | Palavras aprox. | Tokens aprox. |
|-------|----------|-----------------|---------------|
| Chunk A — POL-001, seção 3.2 | Regra de devolução + exceção cargas perigosas | 55 | 73 |
| Chunk B — Tabela SLA-2024 | SLAs Gold, Silver e Standard (chamados gerais) | 40 | 53 |
| Chunk C — PROC-042-v2, seção 2 | Multiplicadores regionais de frete especial | 50 | 67 |
| **Total chunks** | | **145** | **~193** |

### Pergunta do atendente

| Pergunta | Palavras aprox. | Tokens aprox. |
|----------|-----------------|---------------|
| "Qual o prazo de devolução para carga perigosa?" | 8 | 11 |
| "Meu cliente é Gold, qual o SLA de resolução?" | 9 | 12 |
| "Quanto custa o frete para 600kg para Manaus?" | 9 | 12 |

---

## Total por query

| Componente | Tokens |
|------------|--------|
| Contexto estático (system prompt v1) | ~747 |
| Chunks dinâmicos (A + B + C) | ~193 |
| Pergunta do atendente | ~12 |
| **Total por query** | **~952** |

Com janela de 128.000 tokens (GPT-4o), o total por query representa menos de 1% da capacidade disponível. O orçamento de contexto não é gargalo neste cenário.

---

## Problema identificado na estrutura da Rodada 1

Os 3 chunks foram enviados juntos em todas as queries, independente da pergunta. Isso significa que, na pergunta sobre carga perigosa, o Chunk B (SLA) e o Chunk C (frete) estavam presentes no contexto sem relevância — ocupando atenção do modelo com informação desnecessária. Em produção, o pipeline de RAG resolveria isso automaticamente, selecionando apenas os chunks relevantes para cada pergunta.
