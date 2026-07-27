# Relatório de Retrieval — Exercício 1.3 — Iteração 2

**Modelo de embeddings:** paraphrase-multilingual-MiniLM-L12-v2
**Vector store:** ChromaDB
**TOP_K:** 5
**Métrica:** distância L2 (menor = mais similar)

> **Nota sobre os scores:** Os valores de distância da Iteração 2 são numericamente maiores que os da Iteração 1 (ex.: 8.8 vs 0.87). Isso ocorre porque o modelo multilíngue produz embeddings não normalizados para vetores unitários, resultando em distâncias L2 absolutas maiores. A comparação entre iterações deve ser feita pela **cobertura DEVE**, não pelos scores absolutos.

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

| # | Score   | Fonte                               | Seção                                                   |
|---|---------|-------------------------------------|---------------------------------------------------------|
| 1 |  8.8478 | POL-001-politica-devolucao          | 3. Regras de Devolução > 3.1. Prazo geral               |
| 2 | 10.6119 | POL-001-politica-devolucao          | 3. Regras de Devolução > 3.5. Custos de devolução       |
| 3 | 11.5316 | POL-001-politica-devolucao          | 3. Regras de Devolução > 3.3. Procedimento de devolução |
| 4 | 12.0603 | PROC-042-v2-frete-especial-revisado | 3. Prazo de entrega para frete especial                 |
| 5 | 12.7078 | PROC-042-frete-especial-v1          | 3. Prazo de entrega para frete especial                 |

### Avaliação

- ✅ POL-001-A (seção 3.1: Prazo geral) — recuperado em **rank 1**
- ❌ POL-001-B (seção 3.2: Exceções) — **não recuperado**
- ✅ POL-001-C (seção 3.3: Procedimento) — recuperado em rank 3 (PODE)

**Resultado DEVE: 1/2.** Melhora significativa em relação à Iteração 1 (0/2): a seção com o prazo de 7 dias (3.1) foi corretamente recuperada em primeiro lugar. A seção de exceções (3.2) ainda não foi recuperada.

---

## Pergunta 2: _Posso devolver carga perigosa?_

**Tipo:** regra + exceção — risco de inversão

### Gabarito (Anexo B)

- **DEVE:** POL-001-B (seção 3.2: Exceções)
- **PODE:** FAQ-03 (carga perigosa), POL-001-A (seção 3.1: Prazo geral)

### Chunks recuperados

| # | Score   | Fonte                               | Seção                                                          |
|---|---------|-------------------------------------|----------------------------------------------------------------|
| 1 |  9.4585 | FAQ-atendimento                     | Item 38 — "Cliente quer saber a política para carga danificada"|
| 2 | 10.7675 | FAQ-atendimento                     | Item 3 — "Cliente perguntou se pode devolver carga perigosa"  |
| 3 | 11.3455 | FAQ-atendimento                     | Item 22 — "Cliente quer saber sobre seguro de carga"          |
| 4 | 11.3613 | PROC-042-v2-frete-especial-revisado | 4. Condições especiais                                        |
| 5 | 11.5666 | POL-001-politica-devolucao          | 3. Regras de Devolução > 3.5. Custos de devolução             |

### Avaliação

- ❌ POL-001-B (seção 3.2: Exceções) — **não recuperado**
- ✅ FAQ-03 (Item 3: carga perigosa) — recuperado em rank 2 (PODE)

**Resultado DEVE: 0/1.** Igual à Iteração 1. A seção normativa que proíbe devolução de carga perigosa (POL-001 seção 3.2) continua não sendo recuperada. O FAQ-03 (fonte informal com a resposta prática) foi recuperado em rank 2, o que representa uma melhora parcial na cobertura informal.

---

## Pergunta 3: _Meu cliente é Gold. Qual o SLA de resolução?_

**Tipo:** diferenciação de tipo de chamado — regra 6 do system prompt

### Gabarito (Anexo B)

- **DEVE:** SLA-2024-B (seção 2: Tabela de SLAs — chamados gerais)
- **PODE:** SLA-2024-A (seção 1: Classificação), SLA-2024-C (seção 2: incidentes críticos)

### Chunks recuperados

| # | Score   | Fonte                        | Seção                      |
|---|---------|------------------------------|----------------------------|
| 1 |  6.9566 | FAQ-atendimento              | Item 41 — "Qual a diferença entre SLA de resposta e SLA de resolução?" |
| 2 | 11.3049 | SLA-2024-tabela-sla-clientes | 5. Medição e reportes      |
| 3 | 11.9200 | SLA-2024-tabela-sla-clientes | 2. Tabela de SLAs          |
| 4 | 11.9879 | SLA-2024-tabela-sla-clientes | 1. Classificação de clientes|
| 5 | 12.0033 | POL-001-politica-devolucao   | 3. Regras de Devolução > 3.3. Procedimento de devolução |

### Avaliação

- ✅ SLA-2024-B (seção 2: Tabela de SLAs) — recuperado em **rank 3**
- ✅ SLA-2024-A (seção 1: Classificação) — recuperado em rank 4 (PODE)

**Resultado DEVE: 1/1.** Melhora decisiva em relação à Iteração 1 (0/1): a tabela de SLAs por tier (seção 2) foi recuperada. Na Iteração 1, o pipeline trazia apenas seções periféricas do SLA-2024 (seções 3 e 5).

---

## Pergunta 4: _O cliente diz que é Platinum. Qual o SLA dele?_

**Tipo:** tier inexistente — risco de alucinação

### Gabarito (Anexo B)

- **DEVE:** SLA-2024-A (seção 1: Classificação — confirma que o tier não existe)
- **PODE:** FAQ-15 (Item 15: Platinum)

### Chunks recuperados

| # | Score   | Fonte                        | Seção                                                       |
|---|---------|------------------------------|-------------------------------------------------------------|
| 1 |  5.4063 | FAQ-atendimento              | Item 15 — "Cliente diz que é Platinum. Existe esse tier?"   |
| 2 | 11.5577 | FAQ-atendimento              | Item 22 — "Cliente quer saber sobre seguro de carga"        |
| 3 | 12.3498 | PROC-042-v2-frete-especial-revisado | 4. Condições especiais                             |
| 4 | 13.0291 | FAQ-atendimento              | Item 8 — "Como funciona o frete especial?"                  |
| 5 | 13.2393 | SLA-2024-tabela-sla-clientes | 1. Classificação de clientes                                |

### Avaliação

- ✅ SLA-2024-A (seção 1: Classificação) — recuperado em **rank 5**
- ✅ FAQ-15 (Item 15: Platinum) — recuperado em **rank 1** (PODE)

**Resultado DEVE: 1/1.** Melhora em relação à Iteração 1 (0/1): o chunk normativo que confirma a inexistência do tier Platinum foi recuperado (rank 5). Na Iteração 1, dependia exclusivamente do FAQ informal.

---

## Pergunta 5: _Quanto custa o frete para 600kg para Manaus?_

**Tipo:** conflito de versões — risco de misturar v1 e v2

### Gabarito (Anexo B)

- **DEVE:** PROC-042v2-A (seção 2: Fórmula atualizada), PROC-042v2-B (seção 2.1: Multiplicadores atualizados)
- **PODE:** PROC-042-B (seção 2.1 da versão antiga — risco de contradição)

> **Nota de chunking:** na Iteração 2, as seções 2 e 2.1 do PROC-042-v2 foram consolidadas em um único chunk ("2. Fórmula de cálculo"), pois o conteúdo conjunto ficou dentro do limite de MAX_WORDS. Esse chunk cobre tanto PROC-042v2-A quanto PROC-042v2-B.

### Chunks recuperados

| # | Score   | Fonte                               | Seção                      |
|---|---------|-------------------------------------|----------------------------|
| 1 | 16.3193 | PROC-042-frete-especial-v1          | 2. Fórmula de cálculo      |
| 2 | 16.4170 | PROC-042-v2-frete-especial-revisado | 2. Fórmula de cálculo      |
| 3 | 16.8205 | PROC-042-v2-frete-especial-revisado | 4. Condições especiais     |
| 4 | 18.0484 | PROC-042-frete-especial-v1          | 4. Condições especiais     |
| 5 | 18.2867 | PROC-042-v2-frete-especial-revisado | 1. Objetivo                |

### Avaliação

- ✅ PROC-042v2-A+B (seção 2: Fórmula + Multiplicadores, v2) — recuperado em **rank 2**
- ✅ PROC-042-B (seção 2: Fórmula v1, versão antiga) — recuperado em rank 1 (PODE — risco de contradição)

**Resultado DEVE: 1/1** (chunk cobre ambos os gabarito esperados). Melhora decisiva em relação à Iteração 1 (0/2): a fórmula e os multiplicadores foram recuperados. Atenção: a versão antiga (v1) aparece em rank 1, ligeiramente à frente da v2 — o system prompt (regra de prioridade entre fontes) é necessário para garantir que o modelo use a v2.

---

## Síntese comparativa — Iteração 1 vs Iteração 2

| Pergunta | DEVE esperados | It.1 DEVE | It.2 DEVE | Melhora |
|----------|---------------|-----------|-----------|---------|
| 1 — Prazo de devolução | 2 | 0/2 (0%) | 1/2 (50%) | ✅ +1 |
| 2 — Carga perigosa | 1 | 0/1 (0%) | 0/1 (0%) | — |
| 3 — SLA Gold | 1 | 0/1 (0%) | 1/1 (100%) | ✅ +1 |
| 4 — Tier Platinum | 1 | 0/1 (0%) | 1/1 (100%) | ✅ +1 |
| 5 — Frete Manaus 600kg | 2 | 0/2 (0%) | 1/1* (100%) | ✅ +1 |
| **Total** | **7** | **0/7 (0%)** | **4/7 (57%)** | **+4** |

*Seções 2 e 2.1 do PROC-042v2 consolidadas em um chunk na Iteração 2.

## Análise das mudanças

**O que funcionou:**
- A troca para o modelo multilíngue (`paraphrase-multilingual-MiniLM-L12-v2`) resolveu o principal problema de retrieval: o modelo agora associa perguntas em português às seções corretas.
- Incluir o título da seção no texto do embedding eliminou a confusão entre seções de um mesmo documento (ex.: seção 2 vs seção 5 do SLA-2024).
- Chunks com conteúdo numérico (fórmula de cálculo, multiplicadores) passaram a ser recuperados corretamente.

**O que ainda não funcionou:**
- A seção POL-001 > 3.2 (Exceções — carga perigosa proibida no processo padrão) continua não sendo recuperada para a pergunta "Posso devolver carga perigosa?". O FAQ-03 (informal) é recuperado no lugar. Hipótese: a seção 3.2 trata de "exceções ao prazo geral", e o embedding associa "carga perigosa" mais fortemente a contextos de frete do que de devolução.
