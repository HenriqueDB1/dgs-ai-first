# Exercício 3.1 — Structured output + harness (schema, validator e code review)

> **Entregável:** o schema Zod, o `response-validator.ts` e o code review com as correções.
> Código final em `novatech-assistant/src/services/response-validator.ts`. v1 do Copilot e os prints
> das gerações estão em `Evidência copilot/`.

## Ferramentas (divisão do enunciado)
- **Copilot** — schema Zod (tarefa 1) e `response-validator.ts` com os 2 guardrails (tarefa 2).
- **Claude** — code review crítico + correções (tarefa 3, este documento).

## Prompt/geração (evidência D2)
Schema e validator gerados no Copilot CLII com prompts self-contained (referenciando `AGENTS.md` +
`@workspace`, stack e regras inline). Saídas capturadas em `Evidência copilot/`.

## Code review — problemas reais no v1 do Copilot

**1. (crítico) Guardrail 2: a checagem de negação é burlável e ao mesmo tempo bloqueia demais.**
O v1 marca `hasNegation` se *qualquer* palavra negativa aparece em *qualquer* posição do texto.
- Falso negativo: "A carga perigosa **não** precisa de laudo, e a devolução **é permitida**" → tem
  "não" → passa, mesmo afirmando que pode devolver.
- Falso positivo: negação correta com "**proibida/vedada/excluída/não elegível**" (fora da lista) →
  `hasNegation=false` → bloqueia resposta certa.
A ausência de uma palavra-chave não prova que a resposta afirma que pode devolver.

**2. (crítico) Gatilhos perdem variações → o guardrail nem dispara.**
`mentionsDevolucao` só casa "devolução/devolucao" (não "devolver/devolvida"); `mentionsCarga` só o
singular "carga perigosa" (não "cargas perigosas"). "Posso **devolver** a **carga perigosa**? Sim." →
não dispara → resposta perigosa passa.

**3. (real) `z.string().min(1)` aceita string só de espaços.** `" "` passa. `answer`/`source_document`
podem vir em branco. O Guardrail 1 só compensa isso pro `source_document`.

**Menor:** `SAFE_RESPONSE` inventa `source_document: "N/A - encaminhar ao supervisor"` para satisfazer
o schema — código a jusante pode tratar como citação real.

## Correções aplicadas (v2)
- **Schema:** `answer` e `source_document` passam a usar `.trim().min(1)` (rejeita whitespace).
- **Normalização:** `normalize()` remove acentos + caixa, para casar variações de forma determinística.
- **Gatilhos por radical:** `HAZARD_RE = /cargas?\s+perigosas?/`, `RETURN_RE = /devolu|devolv/`.
- **Guardrail 2 fail-closed:** se menciona carga perigosa + devolução e **não** contém uma negativa
  **explícita** (`EXPLICIT_DENIAL_RE`), **bloqueia**. Falhar fechado é o modo seguro para uma regra
  de segurança (melhor over-block do que deixar passar uma afirmação errada).
- `SAFE_RESPONSE.source_document` reduzido a `"N/A"`.

**Trade-off honesto:** o fail-closed pode bloquear uma resposta correta cuja negativa use um fraseado
fora do `EXPLICIT_DENIAL_RE` (falso positivo). Numa regra de segurança, esse é o erro preferível — e a
lista de negativas é ajustável. A alternativa mais robusta seria ancorar no documento-fonte
(POL-001-B: carga perigosa "não elegível para devolução") em vez de análise textual da resposta.

## Prompt (probabilístico) vs código (determinístico)
O **prompt** pede ao modelo para citar fonte e não afirmar devolução de carga perigosa — mas isso é
**probabilístico**: o modelo pode "esquecer". O **harness** (este validator) é **determinístico**:
o schema Zod *garante* os campos, e os guardrails *bloqueiam* programaticamente o que o prompt só
*pede*. É a diferença entre "instruir" e "impor".
