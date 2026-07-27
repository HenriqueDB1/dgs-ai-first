# Tarefa 2 — `.mcp/mcp.json` + justificativa de least privilege

> **Enunciado:** escrever o `.mcp/mcp.json` do projeto aplicando **least privilege** de forma
> concreta — o `filesystem` recebe só as pastas necessárias, e as fontes de leitura
> (`docs/novatech`, `data/retrieval-corpus`) são tratadas como **read-only**; justificar por que
> cada escopo é o mínimo suficiente.

## `mcp.json` final

Localização: `novatech-assistant/.mcp/mcp.json`

```json
{
  "mcpServers": {
    "mcp-fs-workspace": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./src", "./specs", "./skills"]
    },
    "mcp-fs-sources": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./docs/novatech", "./data/retrieval-corpus"]
    },
    "mcp-git": {
      "command": "python",
      "args": ["-m", "mcp_server_git", "--repository", "."]
    },
    "mcp-memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    "mcp-everything": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-everything"]
    }
  }
}
```

Todos os servers são locais e gratuitos (`npx` / `python`), sem nenhum serviço pago ou externo.

## Justificativa de escopo por server (mínimo suficiente)

| Server | Escopo | Por que é o mínimo suficiente |
|---|---|---|
| `mcp-fs-workspace` | `./src ./specs ./skills` (leitura + escrita) | São as únicas pastas onde o time cria/edita artefatos. Fora dela ficam as fontes de negócio, `infra/`, `.git` e `.env` — nada de escrita nem exposição desnecessária. |
| `mcp-fs-sources` | `./docs/novatech ./data/retrieval-corpus` (só leitura) | Fontes de consulta (documentação oficial + corpus de retrieval). Server separado justamente para poder ser tratado como read-only. |
| `mcp-git` | repositório local (`.`) | Só precisa do histórico/diff/branches do próprio repo. Não recebe caminho externo. |
| `mcp-memory` | grafo local (JSON gerenciado pelo server) | Não recebe pasta do repositório; guarda apenas o grafo de decisões/linguagem ubíqua. |
| `mcp-everything` | nenhum | Server de aprendizado; não acessa dado do projeto. |

### Por que dividir o `filesystem` em dois
O reference `server-filesystem` concede **leitura e escrita** a toda pasta que recebe. Uma única
instância com as 5 pastas tornaria `docs/novatech` e `data/retrieval-corpus` graváveis — violando
o read-only exigido. Separando em `mcp-fs-workspace` (escrita) e `mcp-fs-sources` (fontes), a
fronteira de permissão fica explícita e auditável.

## Como o "somente leitura" é de fato garantido
O JSON, sozinho, **não** trava escrita — o `server-filesystem` expõe tools de escrita por padrão.
O read-only do `mcp-fs-sources` é garantido por uma destas camadas (idealmente combinar 1 e 2):

1. **No cliente MCP:** negar/não aprovar as tools de escrita (`write_file`, `edit_file`,
   `move_file`, `create_directory`) para o server `mcp-fs-sources`.
   → **Implementado** em `novatech-assistant/.claude/settings.json`, na lista `permissions.deny`,
   usando o padrão do Claude Code `mcp__mcp-fs-sources__<tool>` (a regra `deny` sempre vence):
   ```json
   {
     "permissions": {
       "deny": [
         "mcp__mcp-fs-sources__write_file",
         "mcp__mcp-fs-sources__edit_file",
         "mcp__mcp-fs-sources__move_file",
         "mcp__mcp-fs-sources__create_directory"
       ]
     }
   }
   ```
2. **No sistema operacional:** marcar `docs/novatech` e `data/retrieval-corpus` como somente
   leitura — trava até o acesso nativo do agente (Read/Write do Claude Code, por exemplo).
3. **No server (só via Docker):** o `server-filesystem` rodando por `npx` **não** tem flag de
   read-only — todas as pastas passadas por argumento ficam leitura + escrita. O único read-only
   "no server" documentado é rodando via Docker e montando a pasta com o sufixo `,ro`
   (ex.: `--mount type=bind,src=.../docs,dst=/projects/docs,ro`). Como usamos `npx`, esta opção
   não se aplica ao nosso setup. (Confirmado no README oficial de `modelcontextprotocol/servers`.)

> **Apoio à camada 1:** o server marca cada tool com a anotação `readOnlyHint` (as tools de
> leitura têm `readOnlyHint: true`; `write_file`/`edit_file`/`move_file`/`create_directory` têm
> `false`). O cliente MCP pode usar essas anotações para aprovar só as tools de leitura do
> `mcp-fs-sources` — é o que torna a camada 1 (cliente) viável na prática.

> **Nota importante — MCP não é sandbox do agente.** O escopo do MCP limita apenas as tools
> daquele server. Um agente com acesso a arquivos nativo (Claude Code) ou a Bash pode contornar o
> read-only do MCP. Por isso a camada de SO (item 2) é a garantia mais robusta. Este ponto é
> retomado na análise de riscos (Tarefa 4).

## Observação sobre caminhos relativos
Os escopos usam caminhos relativos (`./src`, `./docs/novatech`, …). Eles resolvem a partir do
diretório em que o cliente MCP inicia o server — que deve ser a **raiz do `novatech-assistant`**.
Se o cliente iniciar de outro diretório, usar caminhos absolutos.
