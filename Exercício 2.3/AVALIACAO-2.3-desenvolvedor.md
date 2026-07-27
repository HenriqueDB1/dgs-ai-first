# Avaliação do Exercício 2.3 — Definição de estratégia de skills do projeto
**Papel:** Desenvolvedor · **Cenário 2 — Estruturação do Trabalho** · Trilha de Certificação AI First (DGS / DB1 Global Software)

### Resumo
Entregável forte e maduro: a árvore Foundation → Domain → Artifact é coerente, sem skills órfãs, e o mapeamento de criação/consumo cruza papéis de verdade (TL, QA, PS, Design, DM). O SKILL.md Foundation é prescritivo e ancorado no NovaTech, e — diferente de submissões que só descrevem o processo — há evidência real de uso do Copilot (v1 verbatim + print do CLI) com uma crítica não-cosmética que corrige um erro técnico genuíno (API v3 vs v4). Os pontos que travavam a nota anterior (v2 e prints fora do pacote) foram resolvidos nesta submissão.

### Scores por Dimensão

| Dimensão | Score | Justificativa |
|----------|-------|---------------|
| D1 — Domínio Conceitual | 3 | Domina a hierarquia Skills (Foundation→Domain→Artifact) com o princípio de composição explícito (Artifact = Domain + Foundation), usa o formato canônico de Agent Skill (frontmatter `name`+`description`, pasta + `SKILL.md`), e encoda os ADRs nas skills Artifact. Nuance real: distinção v3/v4 do Azure Functions e o `.js` obrigatório no runtime ESM. A conexão com AGENTS.md é reconhecida, porém tratada de forma leve (mencionada, não desenvolvida). |
| D2 — Uso de Ferramentas | 3 | Evidência real de geração→avaliação→reescrita: prompt documentado, v1 do Copilot reproduzido verbatim, **print do Copilot CLI** presente (`evidencias-copilot/prompt.png`, batendo com o v1), crítica com 4 problemas concretos e tabela de decisão v1→v2 com diffs reais (v3→v4, genérico→ancorado, `.js` elevado a regra). Não é v1≈v2 nem prompt único aceito acriticamente — as regras de corte de D2 não disparam. |
| D3 — Qualidade do Entregável | 3 | Artefato central machine-readable e prescritivo: SKILL.md com 10 regras acionáveis, DO/DON'T em TypeScript real e anti-padrões específicos. A árvore + mapeamento estão completos e outro membro do time usaria sem pedir esclarecimento. Ressalva menor: a árvore *materializada* (pastas/placeholders em `novatech-assistant/skills/`) é descrita mas não veio no pacote — mitigada pela cópia autossuficiente do v2 (`3 - SKILL-v2-final...md`). |
| D4 — Pensamento Crítico | 3 | Julgamento próprio evidente: identifica o erro v3/v4 **e diagnostica a causa** (viés de treino puxa o padrão mais frequente mesmo contra a instrução), adapta em vez de adotar cegamente (mantém `types.ts` + Zod alinhados contra o "single source of truth" do Copilot), e lista 4 limitações reais da abordagem de skills/agentes (viés de treino, falsa sensação de acerto, manutenção/dono, skill não substitui revisão humana). |
| D5 — Aplicabilidade ao Projeto | 3 | Profundamente conectado: amarra ADR-0001/0002/0003/0004 e o context budget nas skills Artifact, referencia as armadilhas do Anexo B (carga perigosa não-devolvível; frete < 500 kg sem cobertura), respeita a estrutura do Anexo C (`/skills/{foundation,domain,artifact}/`) e aponta caminhos reais (`src/shared/{types,logger,config}.ts`). |

**Score do exercício: 3.0**

### Verificação de Artefatos Machine-Readable
O SKILL.md Foundation é prescritivo, não narrativo — um agente conseguiria segui-lo. **Bom (prescritivo):** frontmatter canônico com `name`/`description` acionável; regras numeradas com verbo imperativo ("`strict: true` sempre", "ESM com extensão `.js` nos imports relativos", "Sem `console.*` — usar `pino` de `src/shared/logger.ts`"); DO/DON'T com código TypeScript concreto (type guard `x is T` vs `any`; named export + import ESM vs `export default`); anti-padrões que a IA de fato gera (`any` implícito em `catch`, import sem `.js` que quebra no runtime, `as`/`!` para calar o compilador, redeclarar tipos de domínio). **A observar:** as demais skills da árvore são placeholders (fora do escopo da Tarefa 3, correto), e a seção "Como as outras skills usam esta" é curta — poderia mostrar 1 exemplo de referência cruzada concreta. Nada disso é narrativo demais; o artefato passa no teste de "agente segue".

### Pontos Fortes
- Crítica ao Copilot ancorada em erro técnico verificável (API v3 vs v4) com diagnóstico de causa raiz — exatamente o tipo de "parece certo mas erra o alvo" que o exercício quer expor.
- Mapeamento criação/consumo com visão de time real: QA dono de `testing-patterns`/`create-integration-test`, PS em `create-spec`/`react-components`, Design como agente consumidor, DM consumindo output de spec.
- Skills Artifact que encodam os ADRs do cenário 1, evitando reinvenção a cada geração — aplicabilidade de nível 3.

### Pontos de Melhoria
- Incluir a árvore *materializada* (`novatech-assistant/skills/…`) no pacote de submissão, não só descrita — evita a dependência de "abrir a subpasta" que já custou nota na rodada anterior.
- Desenvolver a conexão com AGENTS.md: mostrar como o AGENTS.md referencia/aciona estas skills (1 trecho concreto) elevaria D1 de "reconhecido" para "demonstrado".
- Na Foundation, adicionar um exemplo curto de skill de Domain referenciando a base ("seguir `typescript-conventions`") para tornar o princípio de composição verificável no próprio artefato.

### Classificação
**Aprovado com distinção (3.0)**

### Tópicos da Trilha para Reforço
Nenhum obrigatório (score ≥ 2.5). Aprofundamento opcional: **AGENTS.md** — como o arquivo raiz orquestra e aciona a árvore de skills (o elo mais leve deste entregável).
