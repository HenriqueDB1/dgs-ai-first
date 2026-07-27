# Tarefa 3 — Evidência de execução (uso real dos MCP servers)

> **Enunciado:** subir os servers e comprovar, com evidência, que o agente consegue (a) listar e
> ler um documento de `docs/novatech/`, (b) recuperar um chunk relevante de
> `data/retrieval-corpus/` (validando contra o gabarito do Anexo B) e (c) ler o histórico do
> repositório via `git`. Cliente MCP usado: **Claude Code**.

## Setup comprovado
| Print | Comprova |
|---|---|
| `1 - mcp list.png` | Os 5 servers do projeto conectados (`mcp-fs-workspace`, `mcp-fs-sources`, `mcp-git`, `mcp-memory`, `mcp-everything`) sob a seção *Project MCPs* do `.mcp.json`. |
| `2 - ... list_allowed_directories.png` | Aprovação/uso da tool de leitura `list_allowed_directories` do `mcp-fs-sources`. |
| `3 - ... list_directory.png` | Uso da tool `list_directory` do `mcp-fs-sources`. |
| `4 - ... read_text_file.png` | Uso da tool `read_text_file` do `mcp-fs-sources`. |
| `7 - ... git_log.png` | Aprovação/uso da tool `git_log` do `mcp-git`. |

As tools acionadas são todas de **leitura** — coerente com o least privilege (o `mcp-fs-sources`
tem as tools de escrita negadas em `.claude/settings.json`).

## Evidência (a) — ler documento de negócio
- **Print:** `5 - resposta item a.png`
- **Pedido:** "Usando o server mcp-fs-sources, liste os arquivos em docs/novatech e leia a seção sobre prazo de devolução do POL-001."
- **Resultado:** o agente chamou `mcp-fs-sources` 3× (list + read), listou os 5 documentos + README e retornou a regra de **7 (sete) dias úteis** (Seção 3.1), com a exceção de cargas perigosas.
- **Validação:** confere com `docs/novatech/POL-001-politica-devolucao.md` (Seção 3.1 e 3.2). ✅

## Evidência (b) — recuperar chunk (validado contra o gabarito)
- **Print:** `6 - resposta item b.png`
- **Pedido:** "Usando o server mcp-fs-sources, leia data/retrieval-corpus/chunks-novatech.md e diga qual chunk recuperar para 'Posso devolver carga perigosa?'"
- **Resultado:** o agente indicou **POL-001-B** (Seção 3.2 — Exceções), com FAQ-03 e POL-001-A como secundários, e apontou as armadilhas (FAQ-03 sem respaldo normativo; inversão de regra).
- **Validação (gabarito, Anexo B):** "Posso devolver carga perigosa?" → **deve recuperar POL-001-B**; podem aparecer FAQ-03, POL-001-A. **Bate exatamente.** ✅

## Evidência (c) — ler o histórico do git
- **Print:** `8 - resposta item c.png`
- **Pedido:** "Usando o server mcp-git, mostre o log de commits deste repositório."
- **Resultado:** via `mcp-git`, retornou o commit `bbdd03a` — *"chore: starter repo (Anexo D) — estrutura + dados semeados dos Anexos A e B"* — autor Trilha AI First, 2026-06-09. Único commit do repositório.
- **Validação:** confere com o `git log` do starter repo. ✅
