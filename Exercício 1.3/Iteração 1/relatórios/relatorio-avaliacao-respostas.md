# Relatório de Avaliação de Respostas — Exercício 1.3

Avaliação das respostas geradas pelo pipeline RAG para as 5 perguntas do mapa de cobertura do Anexo B.

---

## Pergunta 1: _Qual o prazo de devolução?_

### Resposta gerada

O prazo para solicitar devolução é de 7 dias úteis. Após a aprovação: triagem em até 4h úteis, coleta reversa em até 2 dias úteis, reembolso em até 5 dias úteis após recebimento.

**Fontes citadas pelo modelo:** POL-001 seção 3.5 (prazo de 7 dias) e seção 3.3 (prazos de processo).

### Avaliação

**Conteúdo:** ✅ Correto. O prazo de 7 dias e os prazos de processo foram fornecidos corretamente.

**Fonte:** ⚠️ Imprecisa. O modelo extraiu o prazo de 7 dias da seção 3.5 ("Prazo expirado: após 7 dias úteis"), onde ele aparece de forma indireta como condição de inelegibilidade. A fonte primária é a seção 3.1 (POL-001-A), que declara o prazo explicitamente — mas esse chunk não foi recuperado.

**Lacuna:** ❌ Exceções omitidas. A seção 3.2 (POL-001-B) — que exclui cargas perigosas do processo padrão — não foi recuperada nem mencionada.

**Veredicto:** Parcialmente correta. A informação essencial chegou ao modelo por um caminho alternativo (seção 3.5), mas a resposta está incompleta e a citação de fonte é imprecisa.

---

## Pergunta 2: _Posso devolver carga perigosa?_

### Resposta gerada

"Não encontrei essa informação na documentação disponível. Recomendo escalar para o supervisor ou consultar diretamente a área responsável." Referenciou o PROC-043 (citado indiretamente pelo PROC-042-v2) como documento específico para carga perigosa.

**Fontes citadas pelo modelo:** POL-001 seção 3.5 e PROC-042-v2 seção 4.

### Avaliação

**Conteúdo:** ❌ Incorreto — mas por falha do pipeline, não do modelo. A resposta correta existe na base: POL-001-B (seção 3.2) diz explicitamente que cargas perigosas classes 1 a 6 da ANTT **não são elegíveis para devolução pelo processo padrão** e devem ser encaminhadas ao ramal 4500 (Gestão de Riscos). O modelo aplicou corretamente a regra 3 do system prompt ("quando não encontrar, diga explicitamente"), mas o chunk decisivo não chegou ao contexto.

**Fonte:** O modelo identificou corretamente que os chunks disponíveis não cobriam a pergunta.

**Veredicto:** Falha do pipeline. A resposta correta existe na base de conhecimento mas o chunk POL-001-B (seção 3.2) não foi recuperado pelo sistema de busca.

---

## Pergunta 3: _Meu cliente é Gold. Qual o SLA de resolução?_

### Resposta gerada

Chamado geral: resolução em 24h (resposta em 2h). Incidente crítico: prazos não encontrados na documentação disponível. Incluiu regra de medição do relógio SLA (pausa fora do horário comercial para chamados gerais, sem pausa para incidentes críticos Gold).

**Fontes citadas pelo modelo:** FAQ-Atendimento Item 41 (prazo de 24h), SLA-2024 seção 5 (medição), SLA-2024 seção 3 (definição de incidente crítico).

### Avaliação

**Conteúdo:** ⚠️ Parcialmente correto. O prazo de 24h para chamado geral Gold está correto. Porém o prazo para incidente crítico Gold (4h de resolução, conforme SLA-2024-C) não foi fornecido — o chunk SLA-2024-C não foi recuperado.

**Fonte:** ❌ Problemática. O prazo de 24h foi extraído do **FAQ Item 41** (fonte informal), não do SLA-2024-B (tabela normativa). O modelo deveria ter aplicado a regra 8 ("quando o FAQ for a única fonte, adicione ressalva explícita") — e de fato sinalizou isso na Observação, o que é positivo. Porém a resposta dependeu de uma fonte informal para uma informação contratual.

**Lacuna:** ❌ O SLA de incidente crítico (4h para Gold) ficou fora. O modelo corretamente identificou a ausência e orientou a buscar a informação, mas isso representa uma resposta incompleta para o atendente.

**Veredicto:** Parcialmente correta. A regra de diferenciação por tipo de chamado foi aplicada (regra 6 do system prompt), mas o valor para incidente crítico não foi fornecido por ausência do chunk normativo.

---

## Pergunta 4: _O cliente diz que é Platinum. Qual o SLA dele?_

### Resposta gerada

O tier Platinum não existe na NovaTech. Os tiers são Gold, Silver e Standard. Orientou confirmar o tier real pelo número de contrato. Não forneceu SLA pois os chunks disponíveis não continham a tabela de prazos.

**Fontes citadas pelo modelo:** FAQ-Atendimento Item 15, SLA-2024 seções 3 e 5.

### Avaliação

**Conteúdo:** ✅ Correto para o essencial. A informação de que Platinum não existe foi corretamente fornecida.

**Fonte:** ⚠️ Dependente de fonte informal. O chunk recuperado foi o FAQ-15 — fonte informal. O documento normativo que confirma a inexistência do tier (SLA-2024-A, seção 1: "Não existem outros tiers além dos três listados") não foi recuperado. O modelo aplicou corretamente a regra 8 e adicionou ressalva explícita sobre o FAQ, o que é positivo.

**Veredicto:** Correta para o essencial, mas dependente de fonte informal. Se o FAQ-15 não estivesse disponível, o modelo poderia ter alucindo um SLA para um tier inexistente.

---

## Pergunta 5: _Quanto custa o frete para 600kg para Manaus?_

### Resposta gerada

"Não encontrei essa informação na documentação disponível." O modelo identificou que 600kg se enquadra como frete especial, mas que os chunks disponíveis não continham a fórmula nem os multiplicadores regionais.

**Fontes citadas pelo modelo:** PROC-042-v2 seção 1 e PROC-042 v1 seção 1 (apenas confirmam o escopo de aplicação).

### Avaliação

**Conteúdo:** ❌ Incorreto — mas por falha do pipeline. A resposta correta existe na base: PROC-042v2-A (seção 2) contém a fórmula (Valor base × Multiplicador regional × Fator de peso, fator 1.0 para 500–1.000kg) e PROC-042v2-B (seção 2.1) contém o multiplicador Norte = 1,8. O modelo aplicou corretamente a regra 3 ao identificar a ausência dos chunks necessários.

**Fonte:** O modelo foi preciso ao explicar o que faltava e por que não pôde responder.

**Veredicto:** Falha do pipeline. Os chunks com a fórmula e os multiplicadores existem na base mas não foram recuperados. O modelo se comportou corretamente dado o contexto recebido.

---

## Síntese geral

| # | Pergunta | Chunks DEVE recuperados | Qualidade da resposta | Causa |
|---|----------|-------------------------|----------------------|-------|
| 1 | Prazo de devolução | 0/2 | ⚠️ Parcialmente correta | Info chegou via caminho alternativo; exceções omitidas |
| 2 | Carga perigosa | 0/1 | ❌ Incorreta | Falha de retrieval — chunk decisivo não recuperado |
| 3 | SLA Gold | 0/1 | ⚠️ Parcialmente correta | Prazo geral via FAQ (informal); incidente crítico ausente |
| 4 | Tier Platinum | 0/1 | ✅ Correta (com ressalva) | Dependeu de fonte informal; normativa não recuperada |
| 5 | Frete Manaus 600kg | 0/2 | ❌ Incorreta | Falha de retrieval — fórmula e multiplicadores não recuperados |

**Observação transversal:** O modelo aplicou corretamente as regras do system prompt (regras 3, 6 e 8) nas situações em que os chunks eram insuficientes. As falhas são predominantemente do pipeline de retrieval, não do comportamento do LLM.

---

## Problemas identificados no pipeline

### Problema 1 — Seções erradas dentro do documento correto

Nas perguntas 1, 3 e 4, o pipeline identificou o documento certo (POL-001, SLA-2024) mas recuperou seções periféricas em vez das seções com a informação solicitada. Por exemplo, para "prazo de devolução" trouxe seções 3.3 e 3.5 do POL-001, e não a seção 3.1. Para "SLA Gold" trouxe seções 3 e 5 do SLA-2024, e não a seção 2 (onde estão os valores por tier).

**Causa provável:** O modelo `all-MiniLM-L6-v2` representa semanticamente o conteúdo do chunk, mas não diferencia bem entre seções curtas de um mesmo documento quando os temas são próximos. O título da seção tem peso insuficiente no vetor gerado.

**Correção proposta:** Incluir o título da seção (e o título do documento) no texto do chunk antes de gerar o embedding, em vez de armazená-los apenas como metadado. Isso aumenta o peso semântico dos títulos na representação vetorial.

### Problema 2 — Chunks com conteúdo numérico/tabular não são recuperados por perguntas em linguagem natural

Na pergunta 5, os chunks com a fórmula de cálculo e os multiplicadores regionais (seção 2 e 2.1 do PROC-042v2) não foram recuperados, mesmo sendo os mais relevantes para a pergunta. O pipeline priorizou seções de texto discursivo ("Objetivo") que mencionam frete especial, mas não contêm os parâmetros necessários.

**Causa provável:** O `all-MiniLM-L6-v2` não associa bem perguntas em linguagem natural ("quanto custa o frete") a chunks com conteúdo predominantemente numérico e estruturado (tabelas, fórmulas). A distância semântica entre a pergunta e o chunk de fórmula é alta mesmo que sejam diretamente relacionados.

**Correção proposta:** Adicionar um prefixo descritivo ao texto dos chunks numéricos/tabulares antes da ingestão, descrevendo em linguagem natural o que o chunk contém. Por exemplo: "Este trecho define a fórmula de cálculo do frete especial e os fatores de peso: [conteúdo original]". Isso cria uma ponte semântica entre a pergunta e o chunk.
