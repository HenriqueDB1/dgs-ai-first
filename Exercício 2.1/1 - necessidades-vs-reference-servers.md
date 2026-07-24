# Tarefa 1 — Necessidades do projeto × Reference servers (MCP)

> **Enunciado:** mapear cada necessidade do projeto para um reference server gratuito e local
> (`filesystem`, `git`, `memory`, `everything`). Para cada um: **o que expõe** (tools/resources/prompts),
> **quem consome**, e **qual pasta/escopo** recebe.

Todos os servers abaixo são *reference servers* oficiais (`modelcontextprotocol/servers`),
rodam localmente via `npx`/`python` e **não** dependem de serviço pago ou externo.

## Mapa resumido

| # | Necessidade | Server | Acesso | Escopo |
|---|---|---|---|---|
| 1 | Ler/escrever código, specs e skills | `filesystem` | leitura + escrita | `./src ./specs ./skills` |
| 2 | Ler documentação de negócio da NovaTech (era Confluence) | `filesystem` | somente leitura | `./docs/novatech` |
| 3 | "Recuperar" chunks do corpus (era Azure AI Search) | `filesystem` | somente leitura | `./data/retrieval-corpus` |
| 4 | Histórico, diff e branches do repositório (era GitHub) | `git` | leitura | repositório local (`.`) |
| 5 | Memória de decisões + linguagem ubíqua | `memory` | leitura + escrita | grafo local (arquivo JSON) |
| — | (Bônus, aprendizado) Explorar as primitivas de MCP | `everything` | — | — |

---

## Detalhamento por necessidade

### Necessidade 1 — Ler e escrever código, specs e skills
- **Server:** `filesystem`
- **O que expõe:** apenas **Tools** (não tem Resources nem Prompts) — `read_file`, `write_file`,
  `edit_file`, `list_directory`, `directory_tree`, `search_files`, `move_file`.
- **Quem consome:** Desenvolvedores e Tech Lead (via Claude / GitHub Copilot).
- **Escopo:** `./src ./specs ./skills` — leitura **e** escrita.
- **Justificativa (mínimo suficiente):** são as únicas pastas onde o time cria/edita artefatos.
  Ficam de fora as fontes de negócio (necessidades 2 e 3), a `infra/`, o `.git` e o `.env`.

### Necessidade 2 — Ler a documentação de negócio da NovaTech
- **Server:** `filesystem`
- **O que expõe:** **Tools** de leitura — `read_file`, `list_directory`, `search_files`.
- **Quem consome:** todos os papéis (devs, QA, Tech Lead, Product Specialist) que consultam a
  documentação oficial.
- **Escopo:** `./docs/novatech` — **somente leitura**.
- **Justificativa:** é a fonte de verdade da empresa; o agente consulta, mas nunca deve alterá-la.

### Necessidade 3 — "Recuperar" chunks do corpus de busca
- **Server:** `filesystem`
- **O que expõe:** **Tools** de leitura — `read_file`, `search_files`, `list_directory`.
- **Quem consome:** Desenvolvedores e QA (testam o retrieval contra o mapa de cobertura).
- **Escopo:** `./data/retrieval-corpus` — **somente leitura**.
- **Justificativa:** substitui o Azure AI Search localmente; é dado de consulta, nunca de escrita.

### Necessidade 4 — Histórico, diff e branches do repositório
- **Server:** `git`
- **O que expõe:** **Tools** — `git_log`, `git_diff`, `git_show`, `git_status`, `git_create_branch`,
  `git_checkout` (também há tools de escrita como `git_add`/`git_commit`, tratadas como não usadas
  nesta fase — ver análise de riscos).
- **Quem consome:** Desenvolvedores e Tech Lead.
- **Escopo:** repositório local (`.`).
- **Justificativa:** dá visão de histórico/diff sem precisar de GitHub remoto.

### Necessidade 5 — Memória de decisões e linguagem ubíqua
- **Server:** `memory`
- **O que expõe:** **Tools** — `create_entities`, `create_relations`, `add_observations`,
  `read_graph`, `search_nodes`, `open_nodes`.
- **Quem consome:** todos os papéis (memória compartilhada do projeto entre sessões).
- **Escopo:** grafo local (um arquivo JSON gerenciado pelo próprio server; não recebe pasta do repo).
- **Justificativa:** guarda glossário do domínio e decisões persistentes sem base externa.

### Bônus — Explorar as primitivas de MCP (aprendizado)
- **Server:** `everything`
- **O que expõe:** as **três** primitivas — **Tools**, **Resources** e **Prompts** (server de demonstração).
- **Quem consome:** o próprio desenvolvedor, para aprender como MCP funciona.
- **Escopo:** nenhum (não acessa dados do projeto).
- **Justificativa:** não é necessidade de produção; entra só como estudo das primitivas do protocolo.

---

### Observação sobre "somente leitura" (detalhada no Passo 2)
O reference `server-filesystem` concede leitura **e** escrita a toda pasta que recebe. O "somente
leitura" das necessidades 2 e 3 é garantido na configuração (Passo 2): separando essas fontes em
uma instância própria do `filesystem` e/ou negando as tools de escrita no cliente MCP.
