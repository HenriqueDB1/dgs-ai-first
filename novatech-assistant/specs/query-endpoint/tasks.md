# Tasks — Query Endpoint

Derivado de `plan.md`. Cada task é atômica (implementável e testável isoladamente).
Estimativa: **P** (pequena), **M** (média), **G** (grande).

Ordem do fluxo: QE-01 → QE-02 → QE-03 → QE-04 → QE-05 → QE-06. QE-07 é transversal.

---

## QE-01 — Endpoint HTTP + validação de input (Zod)
**Descrição:** Criar o HTTP trigger `POST /api/query` (Azure Functions v4) e validar o corpo da
requisição com Zod. Input esperado: `{ question: string, conversationId?: string }`.

**Critérios de aceite:**
- `POST /api/query` com `{ question }` válido responde `200` (com stub de resposta enquanto o fluxo não está completo).
- `question` ausente, vazia ou acima do limite de tamanho → `400` com mensagem clara do erro de validação.
- Schema Zod definido em `validator.ts`; o `handler.ts` usa esse schema (não valida "na unha").
- Tipos do input/output em `src/shared/types.ts`. Sem `console.log` (usar o logger).

**Dependências:** nenhuma.
**Estimativa:** P.

---

## QE-02 — Serviço de embedding da pergunta (Azure OpenAI)
**Descrição:** Função que recebe a pergunta (texto) e retorna o vetor de embedding via Azure
OpenAI, com retry exponencial em falhas transitórias.

**Critérios de aceite:**
- Dada uma pergunta, retorna um array numérico com a dimensão esperada do modelo.
- Falha transitória (`429`/`5xx`) dispara retry com backoff; falha permanente propaga erro tipado.
- Endpoint/deployment/credenciais lidos de `src/shared/config.ts` (env), nunca hardcoded.

**Dependências:** QE-01.
**Estimativa:** M.

---

## QE-03 — Serviço de busca de chunks (Azure AI Search, top-5)
**Descrição:** Função que recebe o embedding e retorna os top-5 chunks mais similares do índice,
com metadados (`source_document`, vigência).

**Critérios de aceite:**
- Retorna até 5 chunks, cada um com score de similaridade e metadados.
- Respeita o metadado de vigência (ADR-0003): não prioriza documentos obsoletos.
- Erros de conexão tratados com retry/backoff.

**Dependências:** QE-02.
**Estimativa:** M.

---

## QE-04 — Prompt builder (respeitando context budget)
**Descrição:** Monta o prompt final (system prompt + chunks + pergunta) respeitando o context
budget (~4K system + ~8K chunks). Seleciona/trunca chunks se exceder.

**Critérios de aceite:**
- Prompt inclui, nesta ordem: system prompt (de `/prompts/system-prompt.md`), os chunks e a pergunta.
- Se os chunks excederem ~8K tokens, aplica uma regra determinística de seleção/truncamento (documentada no código).
- O total não ultrapassa o budget definido.

**Dependências:** QE-03.
**Estimativa:** M.

---

## QE-05 — Serviço de completion (GPT-4o)
**Descrição:** Envia o prompt montado ao GPT-4o (Azure OpenAI) e retorna a resposta textual, com
retry/backoff.

**Critérios de aceite:**
- Dado um prompt válido, retorna a resposta do modelo.
- Retry em falhas transitórias; erro tipado em falha permanente.
- Parâmetros (temperature, max tokens) vêm de `config.ts`.

**Dependências:** QE-04.
**Estimativa:** M.

---

## QE-06 — Response builder + validação de output (Zod)
**Descrição:** Formata a resposta final `{ answer, source_document, ... }` e valida o output com
Zod antes de retornar `200`.

**Critérios de aceite:**
- A resposta inclui `answer` e `source_document` (referente ao(s) chunk(s) usado(s)).
- Output validado por schema Zod; se inválido, retorna `500` com log (não devolve resposta malformada).
- Quando não há chunk relevante, retorna a resposta de "não encontrei / escalar ao supervisor" (guardrail) — não inventa.

**Dependências:** QE-05.
**Estimativa:** P/M.

---

## QE-07 — Logging estruturado (pino) + tratamento de erros transversal
**Descrição:** Configurar o logger `pino` e um utilitário de tratamento de erros para todo o
endpoint, com correlação por `requestId`.

**Critérios de aceite:**
- Logs estruturados (JSON) com `requestId`; nenhum `console.log` no código.
- Erros tipados mapeados para os status HTTP corretos (`400` validação, `500` interno).

**Dependências:** transversal (pode ser feita em paralelo; consumida pelas demais).
**Estimativa:** P.
