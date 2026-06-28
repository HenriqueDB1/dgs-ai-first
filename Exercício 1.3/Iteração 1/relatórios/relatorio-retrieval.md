# Relatório de Retrieval — Exercício 1.3 — Iteração 1

**Modelo de embeddings:** all-MiniLM-L6-v2
**Vector store:** ChromaDB
**TOP_K:** 5
**Métrica:** distância coseno (menor = mais similar)

> O gabarito do Anexo B distingue duas categorias:
> - **DEVE** — chunks obrigatórios para uma resposta correta
> - **PODE** — chunks de relevância menor que podem aparecer sem ser erros

---

## Pergunta 1: _Qual o prazo de devolução?_

**Tipo:** pergunta direta — resposta clara na documentação

### Gabarito (Anexo B)

- **DEVE:** POL-001-A (seção 3.1: Prazo geral), POL-001-B (seção 3.2: Exceções)
- **PODE:** POL-001-C (seção 3.3: Procedimento)

### Chunks recuperados

| # | Score  | Fonte                        | Seção                                                   |
|---|--------|------------------------------|---------------------------------------------------------|
| 1 | 0.8704 | POL-001-politica-devolucao   | 3. Regras de Devolução > 3.5. Custos de devolução       |
| 2 | 0.9390 | POL-001-politica-devolucao   | 3. Regras de Devolução > 3.3. Procedimento de devolução |
| 3 | 0.9492 | PROC-042-frete-especial-v1   | 3. Prazo de entrega para frete especial                 |
| 4 | 0.9882 | SLA-2024-tabela-sla-clientes | 3. Definição de incidente crítico                       |
| 5 | 1.0514 | FAQ-atendimento              | Item 8 — "Como funciona o frete especial?"              |

### Avaliação

- ❌ POL-001-A (seção 3.1) — **não recuperado**
- ❌ POL-001-B (seção 3.2) — **não recuperado**
- ✅ POL-001-C (seção 3.3 = Procedimento) — recuperado no rank 2 (PODE)

**Resultado DEVE: 0/2.** O pipeline identificou o documento correto (POL-001), mas recuperou seções que não contêm o prazo de 7 dias úteis nem as exceções. O chunk 2 corresponde ao POL-001-C (que pode aparecer), mas os dois obrigatórios — o prazo explícito (3.1) e as exceções (3.2) — ficaram fora.

---

## Pergunta 2: _Posso devolver carga perigosa?_

**Tipo:** regra + exceção — risco de inversão

### Gabarito (Anexo B)

- **DEVE:** POL-001-B (seção 3.2: Exceções)
- **PODE:** FAQ-03 (carga perigosa), POL-001-A (seção 3.1: Prazo geral)

### Chunks recuperados

| # | Score  | Fonte                               | Seção                                                  |
|---|--------|-------------------------------------|--------------------------------------------------------|
| 1 | 0.8680 | PROC-042-frete-especial-v1          | 4. Condições especiais                                 |
| 2 | 0.9103 | FAQ-atendimento                     | Item 22 — "Cliente quer saber sobre seguro de carga"   |
| 3 | 0.9310 | SLA-2024-tabela-sla-clientes        | 3. Definição de incidente crítico                      |
| 4 | 0.9795 | PROC-042-v2-frete-especial-revisado | 4. Condições especiais                                 |
| 5 | 1.0111 | POL-001-politica-devolucao          | 3. Regras de Devolução > 3.5. Custos de devolução      |

### Avaliação

- ❌ POL-001-B (seção 3.2) — **não recuperado**

**Resultado DEVE: 0/1.** Nenhum chunk obrigatório foi recuperado. Os chunks 1 e 4 mencionam "carga perigosa" no contexto do PROC-042 (frete, não devolução), indicando que o modelo confundiu o tema com o contexto errado. Nem o FAQ-03 nem o POL-001-A (ambos "pode") foram recuperados.

---

## Pergunta 3: _Meu cliente é Gold. Qual o SLA de resolução?_

**Tipo:** diferenciação de tipo de chamado — regra 6 do system prompt

### Gabarito (Anexo B)

- **DEVE:** SLA-2024-B (seção 2: Tabela de SLAs — chamados gerais)
- **PODE:** SLA-2024-A (seção 1: Classificação), SLA-2024-C (seção 2: incidentes críticos)

### Chunks recuperados

| # | Score  | Fonte                        | Seção                                                          |
|---|--------|------------------------------|----------------------------------------------------------------|
| 1 | 0.6735 | FAQ-atendimento              | Item 41 — "Qual a diferença entre SLA de resposta e resolução?"|
| 2 | 0.8669 | SLA-2024-tabela-sla-clientes | 5. Medição e reportes                                          |
| 3 | 0.9534 | POL-001-politica-devolucao   | 3. Regras de Devolução > 3.5. Custos de devolução              |
| 4 | 0.9599 | SLA-2024-tabela-sla-clientes | 3. Definição de incidente crítico                              |
| 5 | 0.9613 | FAQ-atendimento              | Item 27 — "O tracking mostra 'em trânsito' há 5 dias"         |

### Avaliação

- ❌ SLA-2024-B (seção 2: chamados gerais) — **não recuperado**

**Resultado DEVE: 0/1.** O pipeline encontrou o documento certo (SLA-2024), mas as seções erradas: "Medição e reportes" (seção 5) e "Definição de incidente crítico" (seção 3). A tabela de SLAs por tier (seção 2) — onde estão os valores de 2h/24h para Gold — não foi recuperada em nenhuma de suas subseções.

---

## Pergunta 4: _O cliente diz que é Platinum. Qual o SLA dele?_

**Tipo:** tier inexistente — risco de alucinação

### Gabarito (Anexo B)

- **DEVE:** SLA-2024-A (seção 1: Classificação — confirma que o tier não existe)
- **PODE:** FAQ-15 (Item 15: Platinum)

### Chunks recuperados

| # | Score  | Fonte                        | Seção                                                        |
|---|--------|------------------------------|--------------------------------------------------------------|
| 1 | 0.9300 | POL-001-politica-devolucao   | 3. Regras de Devolução > 3.5. Custos de devolução            |
| 2 | 0.9655 | FAQ-atendimento              | Item 3 — "Cliente perguntou se pode devolver carga perigosa" |
| 3 | 0.9709 | SLA-2024-tabela-sla-clientes | 3. Definição de incidente crítico                            |
| 4 | 0.9916 | FAQ-atendimento              | Item 15 — "Cliente diz que é Platinum. Existe esse tier?"    |
| 5 | 0.9966 | SLA-2024-tabela-sla-clientes | 5. Medição e reportes                                        |

### Avaliação

- ❌ SLA-2024-A (seção 1: Classificação) — **não recuperado**
- ✅ FAQ-15 (Item 15: Platinum) — recuperado em rank 4, score 0.9916 (PODE)

**Resultado DEVE: 0/1.** O chunk normativo obrigatório (SLA-2024-A, seção 1) não foi recuperado. Sem ele, o modelo não tem a confirmação formal de que o tier Platinum não existe — depende apenas do FAQ-15 (fonte informal), que apareceu como "pode" no rank 4.

---

## Pergunta 5: _Quanto custa o frete para 600kg para Manaus?_

**Tipo:** conflito de versões — risco de misturar v1 e v2

### Gabarito (Anexo B)

- **DEVE:** PROC-042v2-A (seção 2: Fórmula atualizada), PROC-042v2-B (seção 2.1: Multiplicadores atualizados)
- **PODE:** PROC-042-B (seção 2.1 da versão antiga — risco de contradição)

### Chunks recuperados

| # | Score  | Fonte                               | Seção                                                  |
|---|--------|-------------------------------------|--------------------------------------------------------|
| 1 | 0.8495 | PROC-042-frete-especial-v1          | 1. Objetivo                                            |
| 2 | 0.9162 | PROC-042-v2-frete-especial-revisado | 1. Objetivo                                            |
| 3 | 0.9774 | PROC-042-frete-especial-v1          | 3. Prazo de entrega para frete especial                |
| 4 | 0.9955 | FAQ-atendimento                     | Item 27 — "O tracking mostra 'em trânsito' há 5 dias" |
| 5 | 0.9956 | PROC-042-frete-especial-v1          | 4. Condições especiais                                 |

### Avaliação

- ❌ PROC-042v2-A (seção 2: fórmula) — **não recuperado**
- ❌ PROC-042v2-B (seção 2.1: multiplicadores) — **não recuperado**

**Resultado DEVE: 0/2.** A fórmula e os multiplicadores regionais (seções 2 e 2.1 do PROC-042v2) não foram recuperados. O pipeline trouxe apenas as seções "Objetivo" de ambas as versões — conteúdo introdutório que não contém os parâmetros necessários para o cálculo.

---

## Síntese geral

| Pergunta | Chunks DEVE esperados | Chunks DEVE recuperados | Chunks PODE recuperados |
|----------|-----------------------|-------------------------|-------------------------|
| 1 — Prazo de devolução | POL-001-A, POL-001-B (2) | 0 | POL-001-C ✅ (rank 2) |
| 2 — Carga perigosa | POL-001-B (1) | 0 | — |
| 3 — SLA Gold | SLA-2024-B (1) | 0 | — |
| 4 — Tier Platinum | SLA-2024-A (1) | 0 | FAQ-15 ✅ (rank 4) |
| 5 — Frete Manaus 600kg | PROC-042v2-A, PROC-042v2-B (2) | 0 | — |
| **Total** | **7** | **0 (0%)** | 2/5 perguntas |

## Problemas identificados

**Problema 1 — Seções erradas dentro do documento correto.**
Nas perguntas 1, 3 e 4, o pipeline identificou o documento certo (POL-001, SLA-2024), mas recuperou seções periféricas em vez das seções com a informação solicitada. Isso indica que o modelo `all-MiniLM-L6-v2` não diferencia bem o conteúdo semântico entre seções curtas de um mesmo documento — provavelmente porque os títulos das seções têm peso insuficiente na representação vetorial dos chunks.

**Problema 2 — Chunks com conteúdo numérico/tabular não são recuperados por perguntas em linguagem natural.**
Na pergunta 5, as seções da fórmula e dos multiplicadores regionais (seção 2 e 2.1 do PROC-042v2) — que contêm tabelas e valores numéricos — não foram recuperadas. O modelo de embedding associou melhor a pergunta a seções de texto discursivo ("Objetivo") do que às seções de cálculo. Isso é uma limitação conhecida do `all-MiniLM-L6-v2` para conteúdo predominantemente numérico.
