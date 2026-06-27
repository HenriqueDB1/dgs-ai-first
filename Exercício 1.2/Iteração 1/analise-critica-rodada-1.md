# Análise Crítica das Respostas — Rodada 1

**System prompt utilizado:** v1 (5 regras)
**Chunks utilizados:** A, B e C do enunciado (simplificados)
**Sessão:** única conversa com as 3 perguntas em sequência

---

## Pergunta 1 — "Qual o prazo de devolução para carga perigosa?"

### Resposta obtida

> Cargas classificadas como perigosas (classes 1 a 6 da ANTT) são **exceção à política geral de devolução** e, portanto, **não estão elegíveis para devolução** no prazo padrão de 7 dias úteis. A documentação disponível exclui expressamente esse tipo de carga da regra geral, mas não define um prazo ou procedimento alternativo específico para elas.
>
> **Fonte(s):** POL-001, seção 3.2
>
> **Observação:** A documentação disponível indica apenas que cargas perigosas estão excluídas da política padrão de devolução, sem detalhar o tratamento aplicável a esses casos. Não encontrei essa informação complementar na documentação disponível. Recomendo escalar para o supervisor ou consultar diretamente a área responsável antes de repassar qualquer prazo ou procedimento ao cliente.

### A resposta está correta?

**Parcialmente.** O núcleo da resposta está correto: carga perigosa não é elegível para devolução pelo processo padrão. A identificação da exceção e a recusa em inventar um prazo alternativo demonstram comportamento adequado. Porém, o assistente afirmou que "a documentação não define um procedimento alternativo" — o que é impreciso, pois o Chunk A continha a frase "O cliente deve abrir chamado no portal e anexar fotos da mercadoria", embora essa instrução se aplique à regra geral, não à exceção. A informação mais crítica ausente — o ramal 4500 da Gestão de Riscos — não estava no chunk, então a omissão é de responsabilidade do dado fornecido, não do modelo.

### Citou a fonte?

**Sim, mas de forma genérica.** Citou "POL-001, seção 3.2", sem separar o chunk da regra geral (seção 3.1) do chunk da exceção (seção 3.2). Em produção, essa distinção seria importante para rastreabilidade.

### Respeitou os guardrails?

| Guardrail | Status | Observação |
|-----------|--------|------------|
| Citar fonte | ✅ | Citou POL-001, seção 3.2 |
| Não inventar prazos | ✅ | Não atribuiu prazo alternativo |
| Escalar quando sem resposta | ✅ | Orientou escalação ao supervisor |
| Português formal e acessível | ✅ | Linguagem clara e direta |
| Atenção a exceções | ✅ | Identificou a exceção e a priorizou |

### Onde errou?

O assistente não informou o ramal 4500 (Gestão de Riscos), que é a orientação prática central para o atendente nesse cenário. Sem essa informação, o atendente sabe o que **não fazer** (processo padrão), mas não sabe **o que fazer** — deixando o cliente sem direcionamento concreto. A causa raiz é o Chunk A do enunciado, que não continha essa informação.

---

## Pergunta 2 — "Meu cliente é Gold, qual o SLA de resolução?"

### Resposta obtida

> **Resposta:** Para clientes Gold, o SLA de resolução é de **até 24 horas**, com tempo de resposta inicial de **até 2 horas**.
>
> **Fonte(s):** Tabela SLA-2024

### A resposta está correta?

**Parcialmente.** A informação fornecida está correta para chamados gerais, mas está incompleta. Existe um segundo SLA para clientes Gold em incidentes críticos (resolução em até 4h, resposta em até 30min) que é drasticamente diferente. Um atendente que recebesse esse dado poderia informar "resolução em 24h" para um chamado crítico onde o compromisso contratual é de 4h — uma violação de SLA sem que o atendente soubesse. O Chunk B do enunciado não continha o SLA de incidentes críticos, e o system prompt v1 também não tinha regra orientando a diferenciação.

### Citou a fonte?

**Sim, mas de forma incompleta.** Citou "Tabela SLA-2024" sem indicar a seção. A fonte está correta, mas a ausência de seção dificulta a rastreabilidade.

### Respeitou os guardrails?

| Guardrail | Status | Observação |
|-----------|--------|------------|
| Citar fonte | ⚠️ | Citou o documento, mas sem seção específica |
| Não inventar prazos | ✅ | Informação extraída do chunk |
| Escalar quando sem resposta | N/A | Havia informação disponível |
| Português formal e acessível | ✅ | Linguagem clara |
| Atenção a exceções | ❌ | Não alertou sobre a existência de SLA diferente para incidentes críticos |

### Onde errou?

Dois problemas combinados: o Chunk B não continha o SLA de incidentes críticos, e o system prompt v1 não tinha instrução para diferenciar os dois tipos de chamado. A resposta passou a impressão de completude quando estava incompleta — o que é mais perigoso do que uma resposta claramente parcial, pois o atendente não percebe que falta informação.

---

## Pergunta 3 — "Quanto custa o frete para 600kg para Manaus?"

### Resposta obtida

> **Resposta:** O frete para 600 kg com destino a Manaus (Região Norte) é calculado da seguinte forma:
> **Valor base × 1,8**
> Por se tratar de carga acima de 500 kg, aplica-se o multiplicador regional de frete especial. Para a Região Norte, esse multiplicador é **1,8**.
>
> **Fonte(s):** PROC-042-v2, seção 2
>
> **Observação:** A documentação fornece apenas o multiplicador regional — o **valor base** não consta nos chunks disponíveis para esta consulta. Para calcular o valor final, é necessário aplicar o multiplicador ao valor base do contrato do cliente. Caso não tenha esse valor em mãos, consulte a tabela de valores base com a área Comercial.

### A resposta está correta?

**Sim, dentro dos limites do chunk disponível.** O assistente aplicou corretamente o multiplicador regional para a região Norte (1,8), identificou que 600kg é frete especial (acima de 500kg), e reconheceu corretamente que o valor base não estava disponível na documentação fornecida.

O único elemento ausente é o fator de peso, que faz parte da fórmula completa (Valor base × Multiplicador regional × Fator de peso). Para 600kg o fator é 1,0 — o que não altera o resultado neste caso — mas a omissão da fórmula completa poderia gerar erros em cargas acima de 1.000kg. A causa raiz é o Chunk C, que continha apenas os multiplicadores regionais sem a fórmula com fator de peso.

### Citou a fonte?

**Sim.** Citou "PROC-042-v2, seção 2" de forma adequada.

### Respeitou os guardrails?

| Guardrail | Status | Observação |
|-----------|--------|------------|
| Citar fonte | ✅ | PROC-042-v2, seção 2 |
| Não inventar prazos | ✅ | Não inventou valor base |
| Escalar quando sem resposta | ✅ | Orientou consultar área Comercial |
| Português formal e acessível | ✅ | Linguagem clara, cálculo bem apresentado |
| Atenção a exceções | ✅ | Identificou limite de 500kg para frete especial |

### Onde errou?

Não apresentou a fórmula completa com o fator de peso, o que pode induzir o atendente a usar apenas "Valor base × multiplicador" para qualquer peso acima de 500kg — gerando cálculos incorretos para cargas acima de 1.000kg. Causa raiz: limitação do Chunk C.

---

## Resumo da Rodada 1

| Pergunta | Correta? | Citou fonte? | Guardrails respeitados? | Principal problema |
|----------|----------|--------------|------------------------|--------------------|
| Carga perigosa | ⚠️ Parcial | ✅ Genérica | ✅ Todos | Ramal 4500 ausente (chunk) |
| SLA Gold | ⚠️ Parcial | ⚠️ Sem seção | ❌ Faltou exceção | SLA crítico ausente (chunk + prompt) |
| Frete Manaus | ✅ Sim | ✅ | ✅ Todos | Fórmula incompleta (chunk) |

O padrão dominante da Rodada 1 é que os erros não são de alucinação nem de desobediência a guardrails — são de incompletude causada por chunks insuficientes. O system prompt v1 funcionou dentro de suas limitações, mas não compensou as lacunas dos dados fornecidos.
