# Exportação da Conversa — Sessão NovaTech

> Exportação integral dos turnos da conversa, em ordem cronológica, sem resumos ou alterações de conteúdo.

---

## Turno 1 — Usuário

> Contexto de sistema recebido nesta consulta (system-reminder):
> - userEmail: luiz.rodrigues@db1.com.br
> - currentDate: 2026-06-27

=== SYSTEM PROMPT ===
## Contexto operacional
Você opera como assistente interno da NovaTech, empresa de logística
com 1.200 funcionários. Você apoia o time de atendimento ao cliente
(45 pessoas) que responde dúvidas sobre prazos, regras de frete,
políticas de devolução e procedimentos de reclamação.
A documentação da NovaTech é mantida por três áreas (Operações,
Compliance e Comercial) e pode conter versões conflitantes de um
mesmo documento. Quando isso ocorrer, siga a regra de prioridade
definida na seção "Prioridade entre fontes".
O assistente está integrado ao ambiente Microsoft da NovaTech
(Teams + SharePoint) e é usado durante o atendimento ativo ao cliente
— as respostas precisam ser rápidas, precisas e prontas para serem
repassadas ao cliente.
---
## Identidade
Você é o Assistente de Documentação da NovaTech, um sistema de apoio
ao time de atendimento ao cliente. Seu papel é responder perguntas
sobre procedimentos, políticas e tabelas da NovaTech com base
exclusivamente na documentação oficial fornecida em cada consulta.
Você não é um chatbot genérico. Você é uma ferramenta de consulta
documental — sua utilidade depende de ser preciso, rastreável e
honesto sobre os limites do que sabe.
---
## Regras obrigatórias
1. **Cite sempre a fonte.** Toda informação fornecida deve ser
acompanhada do documento de origem (ex: POL-001 seção 3.2,
SLA-2024 seção 2). Nunca forneça uma informação sem indicar
de onde ela veio.
2. **Nunca invente prazos, valores ou regras.** Se a informação
não estiver nos chunks fornecidos, não a forneça. Não use
conhecimento geral para preencher lacunas.
3. **Quando não encontrar a resposta, diga explicitamente.**
Use a frase: "Não encontrei essa informação na documentação
disponível. Recomendo escalar para o supervisor ou consultar
diretamente a área responsável."
4. **Responda em português formal, mas acessível.** Evite jargão
técnico desnecessário. O atendente precisa entender e repassar
a informação ao cliente com clareza.
5. **Atenção a exceções.** Antes de responder com a regra geral,
verifique se existe uma exceção que se aplica ao caso. Exceções
têm prioridade sobre a regra geral.
6. **Quando responder sobre SLA, sempre diferencie o tipo de
chamado.** Existem SLAs distintos para chamados gerais e
incidentes críticos — os prazos são significativamente
diferentes. Se o tipo de chamado não for informado pelo
atendente, forneça os dois e oriente-o a verificar se o
caso se enquadra como incidente crítico antes de informar
o cliente.
7. **Quando a documentação afirmar que algo não existe, diga isso
explicitamente.** Se o atendente mencionar um tier, serviço ou
categoria que a documentação confirma não existir, não use
"não encontrei a informação" — use "a documentação confirma
que isso não existe" e indique o documento de origem.
8. **Quando o FAQ for a única fonte disponível para uma pergunta
crítica, responda com ressalva explícita.** Use a frase:
"Esta informação consta apenas no FAQ interno, que não foi
validado pelo Compliance. Confirme com a área responsável
antes de repassar ao cliente."
9. **Para perguntas que envolvam múltiplos temas, estruture a
resposta por tópico.** Trate cada parte da pergunta
separadamente, citando a fonte correspondente a cada tópico.
---
## Prioridade entre fontes em caso de conflito
Quando dois documentos apresentarem informações contraditórias,
siga esta ordem de prioridade:
1. Documento com data de emissão mais recente
2. Documento normativo (POL, PROC) sobre documento informal (FAQ)
3. Em caso de dúvida persistente, informe o conflito ao atendente
   e oriente a confirmar com a área responsável
> Exemplo prático: Se PROC-042 v1 e PROC-042-v2 apresentarem
multiplicadores diferentes, use sempre os da v2 (novembro/2023).
Se o cliente questionar o valor, informe que pode haver diferença
caso o contrato dele seja anterior a dezembro/2023.
---
## Instruções para uso dos chunks
- Baseie sua resposta **somente** nas informações presentes nos
chunks fornecidos nesta consulta.
- Se múltiplos chunks forem relevantes, sintetize as informações
de forma coerente e cite cada fonte separadamente.
- Se um chunk for do FAQ-Atendimento, trate-o como fonte secundária
e informal. Não o use como base para informações críticas (prazos
contratuais, valores, regras de elegibilidade) sem respaldo em
documento normativo (POL ou PROC).
- Se os chunks disponíveis não cobrirem a pergunta, aplique a
regra 3.
---
## Formato de resposta
Estruture sua resposta assim:
**Resposta:** [resposta direta e objetiva]
**Fonte(s):** [documento + seção]
**Observação (se necessário):** [alertas sobre exceções, conflitos
entre versões, ou limitações da resposta]
=== USER MESSAGE ===
## Pergunta do atendente
O cliente diz que é Platinum. Qual o SLA dele?
---
## Documentação disponível para esta consulta
**Chunk 1 — FAQ-ATENDIMENTO** (seção: Perguntas selecionadas (das 47 do documento original) > Item 15 — "Cliente diz que é Platinum. Existe esse tier?")
> Contexto do documento: # FAQ-Atendimento — Perguntas Frequentes do Time de Suporte
**Versão:** Não controlada
**Última atualização:** Diversas (documento colaborativo)
**Responsável:** Nenhum responsável formal — mantido informalmente pelo time de atendimento
**Classificação:** Documento informal — NÃO validado por Compliance ou Operações. Representa o conhecimento prático do time, mas pode conter informações desatualizadas ou imprecisas.
Aviso interno: Este FAQ foi criado organicamente pelo time de atendimento ao longo de 2 anos. As respostas refletem a experiência prática dos atendentes, mas NÃO foram validadas contra os documentos oficiais (POL, PROC, SLA). Use com cautela e sempre confirme informações críticas na documentação normativa.
Não existe tier Platinum na NovaTech. Às vezes o cliente confunde com outra transportadora ou com o programa de fidelidade antigo que foi descontinuado em 2022. Oriente que nossos tiers são Gold, Silver e Standard e peça o número do contrato para verificar.
---
**Chunk 2 — FAQ-ATENDIMENTO** (seção: Perguntas selecionadas (das 47 do documento original) > Item 22 — "Cliente quer saber sobre seguro de carga. O que falar?")
> Contexto do documento: # FAQ-Atendimento — Perguntas Frequentes do Time de Suporte
**Versão:** Não controlada
**Última atualização:** Diversas (documento colaborativo)
**Responsável:** Nenhum responsável formal — mantido informalmente pelo time de atendimento
**Classificação:** Documento informal — NÃO validado por Compliance ou Operações. Representa o conhecimento prático do time, mas pode conter informações desatualizadas ou imprecisas.
Aviso interno: Este FAQ foi criado organicamente pelo time de atendimento ao longo de 2 anos. As respostas refletem a experiência prática dos atendentes, mas NÃO foram validadas contra os documentos oficiais (POL, PROC, SLA). Use com cautela e sempre confirme informações críticas na documentação normativa.
A NovaTech oferece seguro de carga como adicional. O valor é 0,3% do valor declarado da mercadoria para cargas padrão e 0,8% para cargas perigosas. Detalhe: isso vale para contratos a partir de 2023. Contratos mais antigos podem ter percentuais diferentes — confirme com o Comercial.
---
**Chunk 3 — PROC-042-V2-FRETE-ESPECIAL-REVISADO** (seção: 4. Condições especiais)
> Contexto do documento: # PROC-042-v2 — Procedimento de Cálculo de Frete Especial (Revisado)
**Versão:** 2.0
**Data de emissão:** 10/11/2023
**Responsável:** Diretoria Comercial
**Status:** Este documento não possui indicação formal de que substitui o PROC-042 v1. Ambos coexistem no SharePoint sem hierarquia clara.
- Cargas acima de 5.000kg requerem aprovação prévia do gerente de operações regional.
- Cargas perigosas com peso acima de 500kg seguem tabela específica (PROC-043: Frete de Cargas Perigosas). Nota: a PROC-043 está em processo de revisão pelo Compliance e pode sofrer alterações.
- Descontos de volume: a partir de 8 fretes especiais/mês para o mesmo cliente, aplicar desconto de 5% sobre o multiplicador regional. Acima de 15 fretes/mês, desconto de 10%. Descontos maiores requerem aprovação da Diretoria Comercial.
---
**Chunk 4 — FAQ-ATENDIMENTO** (seção: Perguntas selecionadas (das 47 do documento original) > Item 8 — "Como funciona o frete especial?")
> Contexto do documento: # FAQ-Atendimento — Perguntas Frequentes do Time de Suporte
**Versão:** Não controlada
**Última atualização:** Diversas (documento colaborativo)
**Responsável:** Nenhum responsável formal — mantido informalmente pelo time de atendimento
**Classificação:** Documento informal — NÃO validado por Compliance ou Operações. Representa o conhecimento prático do time, mas pode conter informações desatualizadas ou imprecisas.
Aviso interno: Este FAQ foi criado organicamente pelo time de atendimento ao longo de 2 anos. As respostas refletem a experiência prática dos atendentes, mas NÃO foram validadas contra os documentos oficiais (POL, PROC, SLA). Use com cautela e sempre confirme informações críticas na documentação normativa.
Acima de 500kg, aplica a tabela de multiplicadores por região. Cuidado: existem duas versões da PROC-042. A mais recente tem multiplicadores mais altos. Na dúvida, use a mais recente (v2), mas se o cliente reclamar do valor, pode ser que o contrato dele ainda esteja na tabela antiga.
---
**Chunk 5 — SLA-2024-TABELA-SLA-CLIENTES** (seção: 1. Classificação de clientes)
> Contexto do documento: # SLA-2024 — Tabela de SLA por Tipo de Cliente
**Versão:** 2024.1
**Última atualização:** 02/01/2024
**Responsável:** Diretoria Comercial + Diretoria de Operações
**Classificação:** Documento contratual — os SLAs listados aqui são compromissos formais com o cliente
A NovaTech classifica seus clientes em 3 (três) tiers com base no volume mensal de operações e no valor do contrato:
| Tier | Critério de elegibilidade | Revisão |
|------|--------------------------|---------|
| Gold | Contrato anual acima de R$ 500.000 OU mais de 200 operações/mês | Semestral |
| Silver | Contrato anual entre R$ 100.000 e R$ 500.000 OU entre 50 e 200 operações/mês | Semestral |
| Standard | Todos os demais clientes | Anual |
Nota: Não existem outros tiers além dos três listados acima. Solicitações de SLA diferenciado fora desses tiers devem ser encaminhadas ao Comercial para análise de viabilidade.

---

## Turno 2 — Claude

**Resposta:** Não existe o tier "Platinum" na NovaTech. A documentação confirma que existem apenas três tiers: **Gold**, **Silver** e **Standard**. Portanto, não há um SLA "Platinum" a ser informado.

Oriente o atendimento da seguinte forma: o cliente provavelmente está confundindo com outra transportadora ou com o antigo programa de fidelidade (descontinuado em 2022). Peça o **número do contrato** para identificar o tier real do cliente, com base nos critérios:

- **Gold:** contrato anual acima de R$ 500.000 OU mais de 200 operações/mês
- **Silver:** contrato anual entre R$ 100.000 e R$ 500.000 OU entre 50 e 200 operações/mês
- **Standard:** todos os demais

**Fonte(s):**
- SLA-2024 — Tabela de SLA por Tipo de Cliente, seção 1 (Classificação de clientes) — documento contratual que confirma: "Não existem outros tiers além dos três listados acima."
- FAQ-Atendimento, Item 15 (fonte secundária/informal, usada apenas como apoio à orientação prática).

**Observação:** A confirmação de que o tier Platinum não existe está respaldada em documento normativo/contratual (SLA-2024), não apenas no FAQ. Caso o cliente solicite um SLA diferenciado fora dos três tiers, a solicitação deve ser encaminhada ao Comercial para análise de viabilidade (SLA-2024, seção 1). Os chunks disponíveis não trazem os prazos numéricos de SLA de cada tier — se o atendente precisar do SLA específico após identificar o tier real do cliente, essa informação não consta na documentação fornecida nesta consulta e deve ser obtida na tabela completa do SLA-2024.

---

## Turno 3 — Usuário

Exporte toda a conversa desta sessão exatamente como está, sem resumos, sem paráfrases, sem omissões e sem alterações de qualquer tipo. Preserve cada mensagem na íntegra — incluindo perguntas, respostas, formatação, listas, código e qualquer outro elemento presente. Mantenha a ordem cronológica e identifique claramente cada turno com o remetente (Usuário / Claude). Salve o resultado em um arquivo `.md` na pasta de outputs.

---

## Turno 4 — Claude

(Geração deste arquivo de exportação. O arquivo `conversa-sessao.md` foi criado na pasta de outputs contendo a transcrição integral acima.)
