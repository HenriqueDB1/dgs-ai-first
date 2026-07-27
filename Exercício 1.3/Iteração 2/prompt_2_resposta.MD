# Exportação da Conversa — Sessão Completa

> Exportação literal da conversa, em ordem cronológica, sem resumos, paráfrases ou omissões.

---

## Turno 1 — Usuário

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
Posso devolver carga perigosa?
---
## Documentação disponível para esta consulta
**Chunk 1 — FAQ-ATENDIMENTO** (seção: Perguntas selecionadas (das 47 do documento original) > Item 38 — "Cliente quer saber a política para carga que chegou danificada.")
> Contexto do documento: # FAQ-Atendimento — Perguntas Frequentes do Time de Suporte
**Versão:** Não controlada
**Última atualização:** Diversas (documento colaborativo)
**Responsável:** Nenhum responsável formal — mantido informalmente pelo time de atendimento
**Classificação:** Documento informal — NÃO validado por Compliance ou Operações. Representa o conhecimento prático do time, mas pode conter informações desatualizadas ou imprecisas.
Aviso interno: Este FAQ foi criado organicamente pelo time de atendimento ao longo de 2 anos. As respostas refletem a experiência prática dos atendentes, mas NÃO foram validadas contra os documentos oficiais (POL, PROC, SLA). Use com cautela e sempre confirme informações críticas na documentação normativa.
Carga danificada em trânsito tem processo diferente de devolução. O cliente precisa registrar a ocorrência em até 48h após o recebimento, com fotos e laudo se possível. A NovaTech investiga e, se comprovada responsabilidade nossa, reembolsa integralmente. Mas isso passa pelo Jurídico, não pelo atendimento normal — encaminhe para o e-mail sinistros@novatech.com.br.
---
**Chunk 2 — FAQ-ATENDIMENTO** (seção: Perguntas selecionadas (das 47 do documento original) > Item 3 — "Cliente perguntou se pode devolver carga perigosa. O que respondo?")
> Contexto do documento: # FAQ-Atendimento — Perguntas Frequentes do Time de Suporte
**Versão:** Não controlada
**Última atualização:** Diversas (documento colaborativo)
**Responsável:** Nenhum responsável formal — mantido informalmente pelo time de atendimento
**Classificação:** Documento informal — NÃO validado por Compliance ou Operações. Representa o conhecimento prático do time, mas pode conter informações desatualizadas ou imprecisas.
Aviso interno: Este FAQ foi criado organicamente pelo time de atendimento ao longo de 2 anos. As respostas refletem a experiência prática dos atendentes, mas NÃO foram validadas contra os documentos oficiais (POL, PROC, SLA). Use com cautela e sempre confirme informações críticas na documentação normativa.
Na prática, a gente orienta o cliente a ligar no ramal 4500 (Gestão de Riscos). Oficialmente não pode pelo processo padrão, mas já tiveram casos em que o pessoal de Riscos autorizou exceção. Então não diga que é impossível — diga que precisa de tratamento especial.
---
**Chunk 3 — FAQ-ATENDIMENTO** (seção: Perguntas selecionadas (das 47 do documento original) > Item 22 — "Cliente quer saber sobre seguro de carga. O que falar?")
> Contexto do documento: # FAQ-Atendimento — Perguntas Frequentes do Time de Suporte
**Versão:** Não controlada
**Última atualização:** Diversas (documento colaborativo)
**Responsável:** Nenhum responsável formal — mantido informalmente pelo time de atendimento
**Classificação:** Documento informal — NÃO validado por Compliance ou Operações. Representa o conhecimento prático do time, mas pode conter informações desatualizadas ou imprecisas.
Aviso interno: Este FAQ foi criado organicamente pelo time de atendimento ao longo de 2 anos. As respostas refletem a experiência prática dos atendentes, mas NÃO foram validadas contra os documentos oficiais (POL, PROC, SLA). Use com cautela e sempre confirme informações críticas na documentação normativa.
A NovaTech oferece seguro de carga como adicional. O valor é 0,3% do valor declarado da mercadoria para cargas padrão e 0,8% para cargas perigosas. Detalhe: isso vale para contratos a partir de 2023. Contratos mais antigos podem ter percentuais diferentes — confirme com o Comercial.
---
**Chunk 4 — PROC-042-V2-FRETE-ESPECIAL-REVISADO** (seção: 4. Condições especiais)
> Contexto do documento: # PROC-042-v2 — Procedimento de Cálculo de Frete Especial (Revisado)
**Versão:** 2.0
**Data de emissão:** 10/11/2023
**Responsável:** Diretoria Comercial
**Status:** Este documento não possui indicação formal de que substitui o PROC-042 v1. Ambos coexistem no SharePoint sem hierarquia clara.
- Cargas acima de 5.000kg requerem aprovação prévia do gerente de operações regional.
- Cargas perigosas com peso acima de 500kg seguem tabela específica (PROC-043: Frete de Cargas Perigosas). Nota: a PROC-043 está em processo de revisão pelo Compliance e pode sofrer alterações.
- Descontos de volume: a partir de 8 fretes especiais/mês para o mesmo cliente, aplicar desconto de 5% sobre o multiplicador regional. Acima de 15 fretes/mês, desconto de 10%. Descontos maiores requerem aprovação da Diretoria Comercial.
---
**Chunk 5 — POL-001-POLITICA-DEVOLUCAO** (seção: 3. Regras de Devolução > 3.5. Custos de devolução)
> Contexto do documento: # POL-001 — Política de Devolução de Mercadorias
**Versão:** 3.1
**Última atualização:** 15/01/2024
**Responsável:** Diretoria de Operações
**Classificação:** Documento normativo — uso obrigatório pelo time de atendimento
- Defeito ou erro da NovaTech (carga errada, avaria em trânsito): devolução sem custo para o cliente.
- Desistência do cliente (carga correta, sem defeito): o custo do frete reverso é do cliente, calculado com os mesmos multiplicadores do frete original.
- Prazo expirado (solicitação após 7 dias úteis): não elegível para devolução padrão. Encaminhar ao Comercial para negociação caso a caso.

---

## Turno 2 — Claude

**Resposta:** Não há uma autorização clara na documentação normativa para devolução de carga perigosa. O único material que trata diretamente do tema é o FAQ interno, que orienta o seguinte: oficialmente, a devolução de carga perigosa **não** é permitida pelo processo padrão, mas o cliente deve ser orientado a entrar em contato com a Gestão de Riscos (ramal 4500), pois já houve casos de autorização de exceção. A orientação é não dizer ao cliente que é impossível, e sim que o caso exige tratamento especial e análise da área de Riscos.

Importante: a política normativa de devolução (POL-001) define as regras gerais de devolução e custos, mas **não trata especificamente de carga perigosa**. A documentação normativa disponível também indica que carga perigosa tem tratamento próprio (PROC-043 — Frete de Cargas Perigosas), porém esse documento não foi fornecido nesta consulta e está em revisão pelo Compliance.

**Fonte(s):**
- FAQ-Atendimento, Item 3 ("Cliente perguntou se pode devolver carga perigosa") — fonte informal
- POL-001 seção 3.5 (regras gerais de devolução, sem menção a carga perigosa)
- PROC-042-v2 seção 4 (referência à PROC-043 para cargas perigosas, documento não disponível e em revisão)

**Observação:** Esta orientação sobre devolução de carga perigosa consta **apenas no FAQ interno**, que não foi validado pelo Compliance. Confirme com a área responsável (Gestão de Riscos, ramal 4500) antes de repassar ao cliente. Como se trata de uma pergunta crítica sem respaldo em documento normativo, recomendo escalar/confirmar com a área responsável antes de dar uma resposta definitiva ao cliente — especialmente porque a PROC-043, que rege cargas perigosas, está em processo de revisão.

---

## Turno 3 — Usuário

Exporte toda a conversa desta sessão exatamente como está, sem resumos, sem paráfrases, sem omissões e sem alterações de qualquer tipo. Preserve cada mensagem na íntegra — incluindo perguntas, respostas, formatação, listas, código e qualquer outro elemento presente. Mantenha a ordem cronológica e identifique claramente cada turno com o remetente (Usuário / Claude). Salve o resultado em um arquivo `.md` na pasta de outputs.

---

## Turno 4 — Claude

(Geração desta exportação — arquivo `conversa-sessao.md` criado na pasta de outputs contendo os turnos acima.)
