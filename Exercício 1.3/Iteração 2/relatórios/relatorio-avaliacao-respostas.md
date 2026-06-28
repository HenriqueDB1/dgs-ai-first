# Relatório de Avaliação de Respostas — Exercício 1.3 — Iteração 2

Avaliação das respostas geradas pelo pipeline RAG para as 5 perguntas do mapa de cobertura do Anexo B, com comparativo direto à Iteração 1.

---

## Pergunta 1: _Qual o prazo de devolução?_

### Resposta gerada

> O cliente pode solicitar a devolução de mercadorias em até 7 (sete) dias úteis após a data de recebimento confirmada no sistema de tracking. A contagem de dias úteis exclui sábados, domingos e feriados nacionais.
>
> **Fonte(s):** POL-001 — Política de Devolução de Mercadorias (v3.1, 15/01/2024), seção 3.1 — Prazo geral.
>
> **Observação:** Se a solicitação for feita após os 7 dias úteis, o caso não é elegível para devolução padrão e deve ser encaminhado ao Comercial para negociação caso a caso (POL-001, seção 3.5). Os demais documentos disponíveis nesta consulta (PROC-042) tratam de prazo de entrega de frete especial, não de devolução, e por isso não se aplicam a esta pergunta.

### Avaliação

**Conteúdo:** ✅ Correto e completo — 7 dias úteis, exclusão de feriados nacionais, orientação para prazo expirado.

**Fonte:** ✅ POL-001 seção 3.1 como fonte primária — exatamente o chunk POL-001-A esperado pelo gabarito.

**Comportamento:** ✅ Identificou e descartou explicitamente os chunks de frete especial (PROC-042) como irrelevantes para a pergunta.

**Lacuna:** ❌ Exceções (POL-001 seção 3.2 — carga perigosa não elegível) ausentes, pois esse chunk não foi recuperado.

**Vs. Iteração 1:** Na Iteração 1 a resposta citava seção 3.5 como fonte do prazo (imprecisa). Agora cita seção 3.1 corretamente.

**Veredicto: ✅ Correta**

---

## Pergunta 2: _Posso devolver carga perigosa?_

### Resposta gerada

> Não há uma autorização clara na documentação normativa para devolução de carga perigosa. O único material que trata diretamente do tema é o FAQ interno, que orienta: oficialmente, a devolução de carga perigosa não é permitida pelo processo padrão, mas o cliente deve ser orientado a entrar em contato com a Gestão de Riscos (ramal 4500), pois já houve casos de autorização de exceção. A orientação é não dizer ao cliente que é impossível, e sim que o caso exige tratamento especial e análise da área de Riscos.
>
> **Fonte(s):** FAQ-Atendimento Item 3 (fonte informal); POL-001 seção 3.5 (regras gerais, sem menção a carga perigosa); PROC-042-v2 seção 4 (referência à PROC-043, documento não disponível e em revisão).
>
> **Observação:** Esta orientação consta apenas no FAQ interno, não validado pelo Compliance. Confirme com Gestão de Riscos (ramal 4500) antes de repassar ao cliente.

### Avaliação

**Conteúdo:** ✅ Direção correta — "não permitida pelo processo padrão" e encaminhamento para Gestão de Riscos (ramal 4500).

**Fonte:** ⚠️ Ainda dependente do FAQ informal. A seção normativa (POL-001 seção 3.2) que proíbe explicitamente a devolução de carga perigosa não foi recuperada.

**Comportamento:** ✅ Regra 8 aplicada corretamente (ressalva de FAQ). Regra 3 aplicada para o PROC-043 ausente.

**Vs. Iteração 1:** Na Iteração 1 a resposta foi "não encontrei essa informação" — inútil para o atendente. Na Iteração 2 a resposta é acionável: diz o que fazer e por quê.

**Veredicto: ⚠️ Parcialmente correta** — melhora prática significativa, mas sem respaldo normativo formal.

---

## Pergunta 3: _Meu cliente é Gold. Qual o SLA de resolução?_

### Resposta gerada

> Para clientes Gold, o SLA de resolução depende do tipo de chamado:
> - Chamados gerais: até 24h úteis
> - Incidentes críticos: até 4h
>
> Como o tipo de chamado não foi informado, verifique se o caso se enquadra como incidente crítico antes de informar o cliente. Vale lembrar que, para incidentes críticos de clientes Gold, o relógio de SLA não pausa fora do horário comercial (diferente dos chamados gerais, em que o relógio pausa fora de 08h–18h em dias úteis).
>
> **Fonte(s):** SLA-2024, seção 2 (Tabela de SLAs) e seção 5 (Medição e reportes), versão 2024.1.
>
> **Observação:** O FAQ-Atendimento também traz prazos de resolução para Gold (24h), mas é documento informal e não validado pelo Compliance. Como há respaldo no documento contratual (SLA-2024), este foi usado como fonte oficial.

### Avaliação

**Conteúdo:** ✅ Correto e completo — ambos os SLAs (24h geral e 4h crítico) com os valores corretos.

**Fonte:** ✅ SLA-2024 seção 2 como fonte primária — exatamente o chunk SLA-2024-B esperado pelo gabarito.

**Comportamento:** ✅ Regras 6 e 8 aplicadas: diferenciou tipo de chamado; priorizou fonte normativa sobre o FAQ.

**Vs. Iteração 1:** Na Iteração 1 o valor de 24h veio do FAQ Item 41 (informal) e o SLA de incidente crítico (4h) estava ausente. Agora ambos vieram do documento normativo SLA-2024 seção 2.

**Veredicto: ✅ Correta**

---

## Pergunta 4: _O cliente diz que é Platinum. Qual o SLA dele?_

### Resposta gerada

> Não existe o tier "Platinum" na NovaTech. A documentação confirma que existem apenas três tiers: Gold, Silver e Standard.
>
> Critérios de classificação:
> - Gold: contrato anual acima de R$ 500.000 OU mais de 200 operações/mês
> - Silver: contrato anual entre R$ 100.000 e R$ 500.000 OU entre 50 e 200 operações/mês
> - Standard: todos os demais
>
> **Fonte(s):** SLA-2024, seção 1 — "Não existem outros tiers além dos três listados acima." (documento contratual); FAQ-Atendimento Item 15 (fonte secundária/informal).
>
> **Observação:** A confirmação está respaldada em documento normativo/contratual (SLA-2024), não apenas no FAQ. Os chunks disponíveis não trazem os prazos numéricos de SLA — se necessário após identificar o tier real, consultar a tabela completa do SLA-2024.

### Avaliação

**Conteúdo:** ✅ Correto — confirmação normativa da inexistência do tier, com critérios de classificação detalhados.

**Fonte:** ✅ SLA-2024 seção 1 como fonte primária — o chunk SLA-2024-A esperado pelo gabarito.

**Comportamento:** ✅ Não aplicou ressalva desnecessária de FAQ — comunicou com segurança usando o documento normativo. Autoconsciente: alertou que os valores numéricos de SLA não estavam nos chunks disponíveis.

**Vs. Iteração 1:** Na Iteração 1 a resposta dizia "consta apenas no FAQ interno — confirme com a área responsável antes de afirmar ao cliente", gerando insegurança desnecessária. Agora afirma com respaldo normativo.

**Veredicto: ✅ Correta**

---

## Pergunta 5: _Quanto custa o frete para 600kg para Manaus?_

### Resposta gerada

> **Valor do frete = Valor base × Multiplicador regional × Fator de peso**
>
> Aplicando os parâmetros da versão vigente (PROC-042-v2):
> - Multiplicador regional (Norte): **1.8**
> - Fator de peso (600 kg, faixa 500–1.000 kg): **1.0**
> - Valor base: tarifa da tabela mensal de fretes — **não disponível nesta consulta**
>
> **Valor do frete = Valor base × 1.8**
>
> **Fonte(s):** PROC-042-v2 seção 2 (fórmula e fator de peso) e seção 2.1 (multiplicador Norte = 1.8); emissão 10/11/2023.
>
> **Observação:** Conflito entre versões — v1 (mar/2023) traz multiplicador Norte 1.6; v2 (nov/2023) traz 1.8. Pela regra de prioridade (documento mais recente), foi usada a v2. Se o contrato for anterior a dezembro/2023, confirmar com o Comercial qual versão se aplica.

### Avaliação

**Conteúdo:** ✅ Correto — fórmula correta, multiplicador correto (v2 = 1,8), fator de peso correto (1,0), conflito de versões identificado e resolvido.

**Fonte:** ✅ PROC-042v2 seções 2 e 2.1 — os chunks PROC-042v2-A e PROC-042v2-B esperados pelo gabarito.

**Comportamento:** ✅ Regra de prioridade aplicada corretamente (v2 sobre v1). Regra 3 aplicada para o valor base ausente.

**Vs. Iteração 1:** Na Iteração 1 a resposta foi "não encontrei a informação" — os chunks de fórmula e multiplicadores não foram recuperados. Agora a resposta é completa e acionável.

**Veredicto: ✅ Correta**

---

## Síntese comparativa — Iteração 1 vs Iteração 2

| # | Pergunta | Veredicto It.1 | Veredicto It.2 | Melhora |
|---|----------|---------------|---------------|---------|
| 1 | Prazo de devolução | ⚠️ Parcialmente correta (fonte imprecisa) | ✅ Correta | ✅ |
| 2 | Carga perigosa | ❌ Incorreta (escalou sem resposta útil) | ⚠️ Parcialmente correta (direção certa, sem normativo) | ✅ |
| 3 | SLA Gold | ⚠️ Parcialmente correta (via FAQ informal, SLA crítico ausente) | ✅ Correta (via normativo, ambos os SLAs) | ✅ |
| 4 | Tier Platinum | ✅ Correta (com ressalva desnecessária) | ✅ Correta (com segurança normativa) | ✅ |
| 5 | Frete Manaus 600kg | ❌ Incorreta (chunks não recuperados) | ✅ Correta | ✅ |

**Iteração 1:** 0 respostas totalmente corretas · 2 parcialmente corretas · 2 incorretas · 1 correta com ressalva excessiva

**Iteração 2:** 4 respostas totalmente corretas · 1 parcialmente correta · 0 incorretas

## Conclusão

As duas mudanças aplicadas na Iteração 2 — troca do modelo de embedding para multilíngue (`paraphrase-multilingual-MiniLM-L12-v2`) e inclusão do título da seção no texto do embedding — produziram melhora expressiva e mensurável: de 0/7 chunks DEVE recuperados para 4/7 (57%), com reflexo direto na qualidade das respostas.

O único caso ainda não resolvido é POL-001 seção 3.2 (exceções — carga perigosa proibida no processo padrão de devolução). Uma próxima iteração poderia explorar a adição de perguntas-espelho nos chunks normativos (ex.: "Carga perigosa pode ser devolvida?") para melhorar a associação semântica nesse caso específico.
