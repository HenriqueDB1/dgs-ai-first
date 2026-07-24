# Tarefa 4 — Análise de riscos de segurança (setup local de MCP)

> **Enunciado:** identificar ao menos 2 riscos de segurança no uso de MCP servers **neste
> contexto local** e propor mitigações. Os riscos abaixo são específicos do setup deste projeto
> (Claude Code + reference servers via `npx`/`python`, definidos em `.mcp.json`).

## Risco 1 — Escopo amplo do `filesystem` expõe segredos
**Descrição.** O `server-filesystem` dá acesso a tudo dentro das pastas que recebe. Se fosse
apontado para a raiz do repositório (`.`) ou incluísse `.git`/`.env`, o agente conseguiria ler
credenciais, tokens e configuração sensível — e um documento ou prompt malicioso poderia induzi-lo
a vazar esse conteúdo. Em setup local isso é concreto porque o `.env` e o `.git/config` ficam ao
lado do código.

**Mitigação (aplicada).**
- Escopos mínimos por pasta: `mcp-fs-workspace` → `./src ./specs ./skills`; `mcp-fs-sources` →
  `./docs/novatech ./data/retrieval-corpus`. Nenhum aponta para a raiz.
- `.env`, `.git` e `infra/` ficam **fora** de qualquer escopo.
- Regra operacional: manter segredos fora das pastas expostas e revisar o escopo antes de ampliá-lo.

## Risco 2 — Escrita sem revisão (código e histórico)
**Descrição.** O `mcp-fs-workspace` permite escrita, e o `mcp-git` expõe também tools de escrita
(`git_add`, `git_commit`). Sem controle, o agente poderia alterar código ou o histórico do
repositório sem passar por code review — exatamente o tipo de mudança que deveria ser revisada.

**Mitigação (aplicada em parte).**
- `mcp-fs-sources` com as tools de escrita (`write_file`, `edit_file`, `move_file`,
  `create_directory`) **negadas** em `.claude/settings.json` (`permissions.deny`).
- Exigir aprovação humana para tools de escrita e revisar todo `git diff` antes de aceitar.
- Manter o escopo de escrita mínimo (só as 3 pastas de trabalho) e não usar operações git
  destrutivas.

## Risco 3 — MCP não é sandbox do agente
**Descrição.** O escopo e o read-only do MCP limitam **apenas as tools daquele server**. Um agente
com acesso a arquivos nativo (o próprio Claude Code) ou a um shell pode contornar o read-only do
`mcp-fs-sources` e escrever em `docs/novatech` por fora do MCP. Ou seja, configurar o MCP como
read-only **não** coloca o agente inteiro numa caixa.

**Mitigação.**
- Camada de SO (a mais robusta): marcar `docs/novatech` e `data/retrieval-corpus` como **somente
  leitura** no sistema de arquivos — isso trava até o acesso nativo.
- Alternativa: usar um agente que dependa exclusivamente do MCP (sem file access próprio).
- Tratar conteúdo recuperado (docs/chunks) como **não confiável** e nunca auto-executar instruções
  vindas dele (defesa contra prompt injection via documento).

---

### Resumo
| Risco | Específico do setup local? | Mitigação principal | Estado |
|---|---|---|---|
| 1. Escopo amplo expõe segredos | Sim (`.env`/`.git` ao lado do código) | Escopos mínimos, sem raiz | Aplicada |
| 2. Escrita sem revisão | Sim (write no fs + git) | `deny` de escrita + aprovação + review de diff | Aplicada em parte |
| 3. MCP não é sandbox | Sim (Claude Code tem file access nativo) | Read-only no SO / agente só-MCP | Recomendada |
