# Tarefa 2.3.3 (complemento) — Evidência de geração com Copilot + reflexão crítica

> Fecha as lacunas apontadas na avaliação: **D2** (evidência de uso do Copilot — geração →
> avaliação → reescrita) e **D4** (reflexão sobre o output da IA + limitações da abordagem).

## 1. Prompt usado (GitHub Copilot CLI)
```
NÃO leia nem edite nenhum arquivo. Gere do zero e imprima só aqui no chat um SKILL.md
para a skill Foundation "typescript-conventions": frontmatter YAML (name kebab-case + description),
contexto, regras prescritivas numeradas, DO/DON'T em TypeScript, anti-padrões.
Stack: TypeScript strict, ESM ("type":"module"), Zod, pino, Azure Functions v4.
```
(Print do prompt + resposta em `evidencias-copilot/` — anexar a captura de tela.)

## 2. v1 gerado pelo Copilot
Reproduzido verbatim em `evidencias-copilot/copilot-v1-typescript-conventions.md`.

## 3. Avaliação crítica do v1

### Acertos (o que aproveitamos)
- **Frontmatter canônico** (`name` + `description`) correto.
- Estrutura completa: contexto, regras numeradas, DO/DON'T, anti-padrões.
- **Detalhe nas flags strict** (`noUncheckedIndexedAccess`, `noImplicitReturns`, `strictNullChecks`) —
  mais completo que o nosso v1. **→ incorporado à regra 1 do SKILL.md final.**
- Bom uso de **Zod + `z.infer`** e do princípio de validar no entrypoint.

### Erros / limitações reais
1. **API do Azure Functions v3, não v4 (erro técnico grave).** O v1 usa `AzureFunction`, `Context`,
   `export const httpTrigger: AzureFunction = async (context, req) => ...` — esse é o **modelo v3**.
   O projeto usa **v4**: `app.http("query", { handler })` com `HttpRequest`/`HttpResponseInit`/
   `InvocationContext` (ver `src/functions/query/handler.ts`). O Copilot gerou a versão **errada
   apesar de o prompt pedir v4** — provavelmente porque há muito mais exemplo de v3 no treino.
2. **Genérico, não ancorado no projeto.** Fala de "projects using…"; não referencia
   `src/shared/{types,logger,config}.ts`, nem o `AGENTS.md`, nem a estrutura do NovaTech. Uma
   Foundation do projeto precisa apontar os caminhos reais.
3. **Subestima a pegadinha do `.js` em ESM.** Mostra `./x.js` de passagem, mas não eleva a regra
   crítica "import relativo sem `.js` **quebra no runtime Node ESM**" — o anti-padrão de maior valor.
4. **Conselho "não duplicar interface TS + schema Zod" conflita com o projeto.** O NovaTech mantém
   `QueryRequest` em `types.ts` **+** o schema Zod, alinhados por assertion de tipo — então o
   "single source of truth" do v1 precisa de **adaptação**, não adoção cega.

## 4. Decisão v1 → v2 (reescrita crítica)
| Do v1 do Copilot | Decisão no v2 (SKILL.md final) |
|---|---|
| Flags strict detalhadas | **Adotado** (regra 1). |
| Frontmatter + estrutura DO/DON'T | Já tínhamos; mantido. |
| API Azure Functions **v3** | **Corrigido** para v4 (`app.http`, `InvocationContext`). |
| Fraseado genérico | **Reescrito** com caminhos reais (`src/shared/...`) e contexto NovaTech. |
| `.js` de passagem | **Elevado** a regra + anti-padrão explícito (quebra no runtime ESM). |
| "não duplicar interface+schema" | **Adaptado**: mantemos `types.ts` + Zod alinhados (não é adoção cega). |
| Exemplo com `as`/type guard | v2 usa **type guard** `x is T` (sem `as`), coerente com a regra 8. |

## 5. Reflexão — o que o Copilot seguiu vs ignorou, e limitações da abordagem
- **Seguiu:** formato de skill, estrutura DO/DON'T, anti-padrões, imutabilidade, validação com Zod.
- **Ignorou/errou:** a **versão do runtime** (pediu-se v4, veio v3) e a **especificidade do projeto**
  (veio genérico). São exatamente os pontos onde a IA "parece certa" mas erra o alvo.
- **Limitações da abordagem de skills/agentes:**
  1. **Viés de treino sobrepõe a instrução:** mesmo pedindo v4, o modelo puxou v3 (mais frequente no
     treino). A skill precisa ser **explícita sobre a versão** (ex.: "usar `app.http` da v4; nunca
     `AzureFunction`/`Context` da v3") — senão o agente regride ao padrão antigo.
  2. **Skill genérica dá falsa sensação de acerto:** sem exemplos ancorados nos arquivos reais do
     projeto, o output passa numa leitura rápida mas não é utilizável direto.
  3. **Manutenção:** convenções mudam (tsconfig, versões de lib). Uma skill desatualizada vira fonte
     de erro **com ar de autoridade** — precisa de dono e revisão periódica (no nosso mapa: Tech Lead).
  4. **Skill não substitui revisão humana:** o v1 traria a API errada pra produção se aceito sem
     crítica. Skills reduzem variância; não eliminam a necessidade de um humano avaliar o output.
