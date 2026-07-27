# Tarefas 2.3.1 e 2.3.2 — Árvore de skills + mapeamento de criação/consumo

> **Enunciado:** definir a árvore de skills do projeto (Foundation → Domain → Artifact) e, para
> cada skill: nome, descrição (frase-ativação), quem cria (papel), quem consome (papel + agentes)
> e frequência de uso estimada.

**Time:** Tech Lead (TL), Dev Pleno, Dev Sênior, QA, Product Specialist (PS), Delivery Manager (DM).
**Agentes:** Claude (chat), GitHub Copilot, Claude Code, Claude Cowork, Claude Design.

Skills ficam em `novatech-assistant/skills/{foundation,domain,artifact}/`.

---

## Hierarquia (Tarefa 1)

```
Foundation (convenções globais — base de tudo)
├── typescript-conventions      ← base usada por todas as outras (SKILL.md escrito na Tarefa 3)
├── error-handling
├── logging
├── env-config
└── project-structure

Domain (padrões por camada)
├── azure-functions-endpoint
├── azure-ai-search-integration
├── react-components
└── testing-patterns

Artifact (receitas de geração)
├── create-rag-endpoint         (compõe: azure-functions-endpoint + azure-ai-search-integration + foundation)
├── create-integration-test     (compõe: testing-patterns + foundation)
├── create-react-card           (compõe: react-components + foundation)
├── create-adr                  (documentação técnica)
└── create-spec                 (requirements/plan/tasks — SDD)
```

Princípio: uma **Artifact** compõe **Domain** + **Foundation**; nenhuma skill existe sem consumidor
real (cada Artifact mapeia a um artefato repetido do projeto).

---

## Mapeamento (Tarefa 2)

### Foundation
| Skill | Frase-ativação | Cria | Consome | Frequência |
|---|---|---|---|---|
| `typescript-conventions` | "ao escrever/gerar qualquer código TypeScript" | Tech Lead | Devs, QA · Claude Code / Copilot | Altíssima (toda geração de código) |
| `error-handling` | "ao tratar erros, lançar exceções ou mapear falha → HTTP" | Tech Lead | Devs · Claude Code / Copilot | Alta |
| `logging` | "ao adicionar logs ou instrumentar código" | Tech Lead | Devs · Claude Code / Copilot | Alta |
| `env-config` | "ao ler configuração/segredos de ambiente" | Tech Lead | Devs · Claude Code / Copilot | Média |
| `project-structure` | "ao criar arquivo novo / decidir onde algo vai" | Tech Lead | Devs, todos os agentes | Alta |

### Domain
| Skill | Frase-ativação | Cria | Consome | Frequência |
|---|---|---|---|---|
| `azure-functions-endpoint` | "ao criar/estruturar um endpoint Azure Functions" | Dev Sênior + TL | Devs · Claude Code / Copilot | Alta (vários endpoints) |
| `azure-ai-search-integration` | "ao integrar com Azure AI Search (indexar/buscar)" | Dev Sênior | Devs · Claude Code / Copilot | Média |
| `react-components` | "ao criar componentes React do painel" | Dev (front) + Product Specialist | Devs front · Claude Design / Copilot | Média |
| `testing-patterns` | "ao escrever testes (unit/integration)" | QA + Dev Sênior | Devs, QA · Claude Code / Copilot | Alta |

### Artifact
| Skill | Frase-ativação | Cria | Consome | Frequência |
|---|---|---|---|---|
| `create-rag-endpoint` | "gerar um endpoint novo com padrão RAG" | Dev Sênior | Devs · Claude Code / Copilot | Alta |
| `create-integration-test` | "gerar teste de integração para um endpoint" | QA | Devs, QA · Claude Code / Copilot | Alta |
| `create-react-card` | "gerar card/formulário React do painel" | Dev (front) + Design | Devs front · Claude Design / Copilot | Média |
| `create-adr` | "registrar uma decisão arquitetural (ADR)" | Tech Lead | TL, Devs · Claude / Cowork | Baixa-média |
| `create-spec` | "gerar requirements/plan/tasks de um módulo (SDD)" | PS (requirements) + TL (plan) + Dev (tasks) | PS, TL, Devs · Claude / Cowork | Média (por módulo) |

---

## Amarração com os ADRs do cenário 1
As skills **Artifact** encodam as decisões arquiteturais do cenário 1, pra não serem reinventadas a
cada geração:
- **`create-rag-endpoint`** → ADR-0001 (GPT-4o / Azure OpenAI), **ADR-0002** (context budget: 5 chunks
  ~1.500 tokens, ~4K system + ~8K chunks), **ADR-0003** (metadado de vigência p/ documentos
  contraditórios), **ADR-0004** (chunking de tabelas de frete/SLA). Ver o `SKILL.md` dessa skill.
- **`create-integration-test`** → cenários de falha do QA e as armadilhas do Anexo B (carga perigosa
  NÃO é devolvível; frete < 500 kg não tem cobertura → assistente deve dizer que não encontrou).
- **`create-adr`** → formato de ADR do projeto (`docs/adr/NNNN-titulo.md`).
- **`create-spec`** → context budget e guardrails de produto entram nos `requirements.md`/`plan.md`.

## Visão de time (por que o mapeamento não é só de dev)
- **Tech Lead** é dono das Foundation (convenções que travam o projeto) e dos ADRs.
- **QA** cria `testing-patterns` e `create-integration-test` — os padrões de teste não são "coisa de dev sozinho".
- **Product Specialist** contribui em `react-components` (UX das respostas) e lidera `create-spec` (requirements).
- **Design** entra como agente consumidor em `react-components` / `create-react-card`.
- **Delivery Manager** não cria skill técnica, mas consome o output de `create-spec` para planejamento.
