# Análise Crítica das Respostas — Rodada 2

**System prompt utilizado:** v2 (9 regras)
**Chunks utilizados:** chunks completos do Anexo B, uma conversa separada por pergunta
**Sessão:** 3 conversas independentes (uma por pergunta)

---

## Pergunta 1 — "Qual o prazo de devolução para carga perigosa?"

### Resposta obtida

> **Resposta:** Cargas perigosas classificadas nas classes 1 a 6 da ANTT **não são elegíveis para devolução pelo processo padrão**. Isso inclui explosivos (classe 1), gases (classe 2), líquidos inflamáveis (classe 3), sólidos inflamáveis (classe 4), oxidantes e peróxidos (classe 5), e substâncias tóxicas e infectantes (classe 6).
>
> Nesses casos, o cliente deve ser direcionado ao setor de **Gestão de Riscos** (ramal 4500) para tratamento individual.
>
> **Fonte(s):** POL-001-B — Seção 3.2: Exceções
>
> **Observação:** A regra geral de 7 dias úteis (POL-001-A, Seção 3.1) **não se aplica** a este caso. A Seção 3.2 é uma exceção explícita que tem prioridade. Antes de repassar ao cliente, confirme a classificação ANTT da carga para garantir que ela se enquadra nas classes 1 a 6.

### A resposta está correta?

**Sim, e de forma completa.** O assistente identificou corretamente a exceção, listou as 6 classes de carga perigosa para referência do atendente, informou o ramal 4500 como próximo passo concreto, e adicionou uma orientação prática de verificar a classificação ANTT antes de repassar ao cliente. Nenhuma informação foi inventada.

### Citou a fonte?

**Sim, com precisão melhorada.** Citou "POL-001-B — Seção 3.2: Exceções" com identificação do chunk específico — mais rastreável do que a citação genérica da Rodada 1. Na observação, também referenciou POL-001-A (Seção 3.1) ao explicar que a regra geral não se aplica.

### Respeitou os guardrails?

| Guardrail | Status | Observação |
|-----------|--------|------------|
| Citar fonte | ✅ | POL-001-B, Seção 3.2, com chunk identificado |
| Não inventar prazos | ✅ | Não atribuiu prazo alternativo |
| Escalar quando sem resposta | ✅ | Ramal 4500 como encaminhamento concreto |
| Português formal e acessível | ✅ | Linguagem clara, lista de classes legível |
| Atenção a exceções | ✅ | Exceção identificada e priorizada |

### Onde errou?

Nenhum erro identificado. A resposta está completa, rastreável e acionável para o atendente.

---

## Pergunta 2 — "Meu cliente é Gold, qual o SLA de resolução?"

### Resposta obtida

> **Resposta:**
> O SLA de resolução para clientes Gold depende do tipo de chamado:
> - **Chamado geral:** resolução em até **24h úteis** (resposta inicial em até 2h úteis)
> - **Incidente crítico:** resolução em até **4h** (resposta inicial em até 30 minutos)
>
> Antes de informar o cliente, verifique se o caso se enquadra como incidente crítico — os prazos são significativamente diferentes.
>
> **Fonte(s):** SLA-2024, Seção 2 (Chunks B e C)
>
> **Observação:** Os prazos para incidentes críticos (Chunk SLA-2024-C) não são em horas úteis, ao contrário dos chamados gerais. Certifique-se de comunicar isso ao cliente caso o chamado seja classificado como crítico.

### A resposta está correta?

**Sim, e com uma adição relevante não explicitada no system prompt.** O assistente diferenciou corretamente os dois tipos de SLA, mas foi além: identificou por conta própria que os prazos de incidentes críticos são em horas corridas (não horas úteis), enquanto os chamados gerais são em horas úteis. Essa distinção não foi instruída explicitamente em nenhuma regra do system prompt — o modelo inferiu a partir dos chunks SLA-2024-B e SLA-2024-C. É uma melhoria de qualidade relevante: um atendente Gold que informe "4h de resolução" sem distinguir horas corridas de horas úteis pode gerar expectativa incorreta no cliente.

### Citou a fonte?

**Sim, com identificação dos dois chunks.** Citou "SLA-2024, Seção 2 (Chunks B e C)", deixando claro que a resposta veio de duas fontes distintas — chamados gerais e incidentes críticos.

### Respeitou os guardrails?

| Guardrail | Status | Observação |
|-----------|--------|------------|
| Citar fonte | ✅ | SLA-2024, Seção 2, Chunks B e C identificados |
| Não inventar prazos | ✅ | Todos os prazos extraídos dos chunks |
| Escalar quando sem resposta | N/A | Informação estava disponível |
| Português formal e acessível | ✅ | Formato de lista facilita leitura rápida |
| Atenção a exceções | ✅ | Alertou proativamente sobre incidentes críticos |
| Regra 6 — diferenciar tipo de chamado | ✅ | Diferenciação central da resposta |

### Onde errou?

Nenhum erro identificado. A observação sobre horas úteis vs. horas corridas foi um acréscimo de qualidade espontâneo que fortalece a resposta.

---

## Pergunta 3 — "Quanto custa o frete para 600kg para Manaus?"

### Resposta obtida

> **Resposta:**
> Para calcular o frete de 600 kg para Manaus (região Norte), aplica-se a seguinte fórmula e os seguintes parâmetros:
> - **Fórmula:** Valor base × Multiplicador regional × Fator de peso
> - **Multiplicador regional (Norte):** 1,8
> - **Fator de peso (500–1.000 kg):** 1,0
>
> **Cálculo:** Valor base × 1,8 × 1,0 = **Valor base × 1,8**
>
> O valor base não consta na documentação disponível para esta consulta. Com o valor base em mãos, basta multiplicá-lo por **1,8** para obter o frete final.
>
> **Fonte(s):**
> - Fórmula: PROC-042v2-A, Seção 2 (novembro/2023)
> - Multiplicador regional Norte (1,8): PROC-042v2-B, Seção 2.1 (novembro/2023)
>
> **Observação:** Existe uma versão anterior deste procedimento (PROC-042-B, março/2023) que indica o multiplicador Norte como 1,6. A versão de novembro/2023 (PROC-042v2-B) prevalece por ser mais recente. Caso o contrato do cliente seja anterior a dezembro/2023, pode haver divergência em relação ao valor que ele espera — oriente o atendente a verificar a data do contrato se houver questionamento.

### A resposta está correta?

**Sim, e de forma completa.** Em relação à Rodada 1, três melhorias concretas: a fórmula agora inclui o fator de peso (1,0 para 600kg), o conflito entre as duas versões da PROC-042 foi identificado e resolvido corretamente, e a orientação sobre contratos anteriores a dezembro/2023 foi mantida e aprimorada.

### Citou a fonte?

**Sim, com o melhor nível de rastreabilidade das 3 perguntas.** Citou as duas fontes separadamente — PROC-042v2-A para a fórmula e PROC-042v2-B para os multiplicadores — identificando o chunk e a data de emissão de cada um. Também mencionou PROC-042-B (versão antiga) na observação, deixando claro qual foi descartado e por quê.

### Respeitou os guardrails?

| Guardrail | Status | Observação |
|-----------|--------|------------|
| Citar fonte | ✅ | Duas fontes citadas separadamente, com datas |
| Não inventar prazos | ✅ | Valor base ausente foi declarado, não inventado |
| Escalar quando sem resposta | ✅ | Orientou buscar valor base no Comercial |
| Português formal e acessível | ✅ | Fórmula apresentada de forma clara |
| Atenção a exceções | ✅ | Tratou corretamente a faixa de peso (500–1.000kg) |
| Prioridade entre fontes | ✅ | Usou v2 por ser mais recente, explicou o motivo |

### Onde errou?

Nenhum erro identificado. A gestão do conflito entre as duas versões da PROC-042 foi o ponto mais exigente da rodada e foi executada corretamente.

---

## Resumo da Rodada 2

| Pergunta | Correta? | Citou fonte? | Guardrails respeitados? | Destaque |
|----------|----------|--------------|------------------------|----------|
| Carga perigosa | ✅ Completa | ✅ Com chunk identificado | ✅ Todos | Ramal 4500 presente |
| SLA Gold | ✅ Completa | ✅ Dois chunks citados | ✅ Todos + inferência extra | Diferenciação horas úteis vs. corridas |
| Frete Manaus | ✅ Completa | ✅ Fontes separadas com datas | ✅ Todos + conflito resolvido | Gestão correta de versões conflitantes |

As três respostas da Rodada 2 estão corretas, completas e acionáveis. As melhorias em relação à Rodada 1 resultaram de duas mudanças combinadas: o system prompt v2 com 9 regras (especialmente a regra 6 sobre diferenciação de SLA) e os chunks do Anexo B, mais completos e separados por seção. Não foram identificados erros de alucinação, invenção de dados ou desobediência a guardrails em nenhuma das três respostas.
