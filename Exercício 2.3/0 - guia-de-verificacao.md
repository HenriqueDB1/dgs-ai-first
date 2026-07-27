# Guia de verificação — Exercício 2.3 (Estratégia de skills)

> ⚠️ **LEIA ANTES DE AVALIAR — a avaliação só é válida COM a subpasta `novatech-assistant/`.**
>
> Parte dos entregáveis do 2.3 **NÃO está nesta pasta** (`Exercício 2.3/`): o **`SKILL.md` final**
> e a **árvore de skills materializada** vivem em **`novatech-assistant/skills/`**.
>
> Avaliar sem abrir essa subpasta subestima D2 e D3 (o artefato central fica "ausente"). **Se o
> pacote recebido não contém `novatech-assistant/`, PARE e solicite-a antes de pontuar.** Os
> caminhos exatos a inspecionar estão em "Resumo dos caminhos a inspecionar", no fim deste guia.

Caminho base do projeto: `novatech-assistant/` (relativo à raiz do repo do curso `dgs-ai-first`).

---

## Tarefas 1 e 2 — Árvore de skills + mapeamento (criação/consumo/frequência)
| Arquivo | Papel |
|---|---|
| `Exercício 2.3/1 - arvore-e-mapeamento-de-skills.md` | **Entregável:** hierarquia Foundation → Domain → Artifact (estendida para cobrir os 5 artefatos repetidos) + tabela de mapeamento por skill (frase-ativação, quem cria, quem consome + agentes, frequência) + seção de visão de time. |
| `novatech-assistant/skills/foundation/` · `…/domain/` · `…/artifact/` | A árvore **materializada** como pastas/placeholders no repo (espelha o documento acima). |

## Tarefa 3 — SKILL.md da Foundation base
| Arquivo | Papel |
|---|---|
| `novatech-assistant/skills/foundation/typescript-conventions/SKILL.md` | **Entregável:** a skill Foundation mais importante (base das demais), no formato canônico de Agent Skill (frontmatter `name` + `description`, pasta com `SKILL.md`). Contém: contexto, 10 regras prescritivas, exemplos DO/DON'T com código, e anti-padrões. |

> Nota: a `typescript-conventions` foi convertida para o formato canônico (pasta + `SKILL.md`). O
> arquivo achatado antigo `skills/foundation/typescript-conventions.md` deve ser removido (limpeza no
> Windows). As demais skills da árvore permanecem como placeholders vazios (fora do escopo da Tarefa 3).

---

## Evidência de uso do Copilot + reflexão (D2 / D4)
| Arquivo | Papel |
|---|---|
| `Exercício 2.3/2 - evidencia-copilot-e-reflexao.md` | Prompt, avaliação crítica do v1 do Copilot (incl. o erro de API v3 vs v4), decisão v1→v2 e reflexão sobre limitações da abordagem. |
| `Exercício 2.3/evidencias-copilot/copilot-v1-typescript-conventions.md` | v1 gerado pelo Copilot, verbatim. |
| `Exercício 2.3/evidencias-copilot/` (prints) | Captura do prompt + resposta no Copilot CLI (a anexar). |

## Resumo dos caminhos a inspecionar
```
Exercício 2.3/1 - arvore-e-mapeamento-de-skills.md          (esta pasta — Tarefas 1 e 2)
novatech-assistant/skills/foundation/typescript-conventions/SKILL.md   (Tarefa 3)
novatech-assistant/skills/                                  (árvore materializada: foundation/domain/artifact)
Exercício 2.3/2 - evidencia-copilot-e-reflexao.md           (evidência D2 + reflexão D4)
Exercício 2.3/3 - SKILL-v2-final-typescript-conventions.md  (cópia autossuficiente do SKILL.md v2 final)
Exercício 2.3/evidencias-copilot/                           (v1 do Copilot + prints)
```

## Como avaliar (critérios do enunciado)
- **Árvore coerente:** cada skill Artifact mapeia a um artefato repetido real (endpoint RAG, teste de
  integração, card React, ADR, spec SDD) — sem skill órfã.
- **Visão de time:** criação/consumo cruza papéis (TL nas Foundation/ADR, QA nos testes, PS nas
  specs/React, Design como agente consumidor) — não é só de dev.
- **SKILL.md concreto e prescritivo:** regras com exemplos de código reais (DO/DON'T), não abstrações.
- **Anti-padrões úteis:** focam no que a IA geraria de errado sem guidance (ex.: import sem `.js` que
  quebra no runtime ESM, `any`, `as` para calar o compilador, `console.log`).
