# Tarefa 2.2.3 — Revisão crítica do código gerado (QE-01)

> **Enunciado:** revisar criticamente o código gerado pela IA e identificar ao menos 2 pontos que
> precisariam de ajuste antes de um code review real (problemas reais, não inventados).

**Contexto:** a QE-01 (endpoint `POST /api/query` + validação Zod) foi implementada com o Claude Code.
Além dos 3 arquivos previstos, a geração também criou o logger pino, testes e alterou o `package.json`.

**Arquivos revisados** (em `novatech-assistant/`):
`src/functions/query/handler.ts`, `src/functions/query/validator.ts`, `src/shared/types.ts`,
`src/shared/logger.ts`, `tests/unit/*`, `package.json`, `tsconfig.json`.

Todos os pontos abaixo foram verificados no código (não são hipotéticos).

---

## 1. "Build verde" não prova que o endpoint roda — falta `host.json` e `main`
O projeto compila (`tsc`) e passa 14 testes unitários, mas **não existe `host.json`** e o
`package.json` **não tem o campo `main`**. O Azure Functions v4 (modelo Node) precisa dos dois para
o host descobrir e carregar a function. Os testes exercitam a função isolada (importando o handler),
não o runtime do Functions — então o "tudo verde" dá uma confiança falsa: o endpoint não subiria de
fato.
**Ajuste:** adicionar `host.json` e `main` apontando para o build (ex.: `dist/src/**/*.js`); incluir
ao menos um smoke test que suba o host, não só unit tests da função.

## 2. Vazamento de escopo da task (fere o Spec Driven Development)
A QE-01 era **endpoint + validação**. A implementação também entregou a **QE-07** (logger pino),
criou testes e alterou dependências. É trabalho útil, mas mistura tasks que o `tasks.md` separou:
dificulta o code review, borra as fronteiras do plano e adianta escopo de outra task.
**Ajuste:** manter a QE-01 no escopo definido; o logger entra na QE-07. Se a antecipação for
intencional, atualizar o `tasks.md` para refletir (a spec e o código não podem divergir em silêncio).

## 3. `authLevel: "function"` foi decidido silenciosamente
O handler registra `app.http("query", { authLevel: "function", ... })`. É uma decisão de segurança
que **não estava na spec**, e não há autenticação/autorização para o usuário final (atendente).
**Ajuste:** tornar a decisão explícita e justificada (anônimo atrás de APIM? function key? como a
chave é gerida e rotacionada?), idealmente registrada num ADR ou no `plan.md`.

## 4. Número mágico `MAX_QUESTION_LENGTH = 1000` hardcoded
O limite vive fixo no `validator.ts`. O `AGENTS.md` manda tunables/config via `config.ts`, e o valor
não é justificado contra o context budget da ADR-0002.
**Ajuste:** mover o limite para `config.ts` (lido de env, com default) e justificar o número em
relação ao orçamento de tokens.

## 5. Contrato de erro ad-hoc e `flatten()` vaza internals do Zod
Cada resposta `400` é montada inline como `{ error, details: parsed.error.flatten() }`, sem passar
por `errors.ts` (que está vazio). Isso expõe a estrutura interna da validação ao cliente e tende a
ficar inconsistente entre endpoints.
**Ajuste:** um contrato de erro tipado e centralizado (`src/shared/errors.ts`) mapeando erro → status,
com resposta enxuta e estável para o cliente.

---

## Pontos secundários (config/infra)
- `tsconfig.json` usa `moduleResolution: "Bundler"`, incoerente com o runtime do Functions (Node ESM,
  que pede `NodeNext`/`Node16`) — o código já usa imports com extensão `.js`, o que combina com Node ESM,
  não com Bundler.
- `@types/node` está em `^20`, mas o runtime é Node **22** — versões deveriam casar.
- `npm audit` reportou 5 vulnerabilidades (1 crítica) na árvore transitiva, ainda não triadas.

## Conclusão
Os critérios de aceite funcionais da QE-01 (valida com Zod, `400` com detalhe, `200` no caminho feliz,
tipos em `shared/types.ts`, sem `console.log`) estão atendidos e verificados por teste. Os ajustes
acima são de **prontidão para produção e disciplina de SDD** — os itens 1 e 2 são os que eu bloquearia
num code review real.
