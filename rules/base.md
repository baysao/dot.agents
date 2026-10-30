# BASE CLI — Proactive Context Engine

The `base` binary is on PATH. Use these commands proactively during sessions — they write to a knowledge graph that persists across sessions and surfaces context automatically.

### When to call (proactive, not on-demand)

| Trigger | Command |
|---------|---------|
| Navigate code: find functions, callers, imports | `base ast query --contains "name"` or `--file`, `--calls`, `--imports` (add `--target apps/X` to query another app's map) |
| Discover which apps have a code map | `base ast list` |
| A decision is made (architectural, process, tooling) | `base decision log --domain X --decision "..." --rationale "..."` |
| An insight, correction, or lesson emerges | `base learn --text "..." --domain X --type insight\|correction\|decision` |
| User defines or refines a behavioral rule | `base rule add --domain X --text "..." --keywords "a, b" --fires-on "<the user's prompt>"` |
| Before making assumptions about prior context | `base recall --keyword "..."` or `base recall --domain X` |
| User asks to scaffold a new workspace | `base scaffold [path]` |

### Code navigation — MANDATORY FIRST TOOL

**ALWAYS use `base ast query` BEFORE grep, find, Read, or any MCP tool for code exploration.**
The AST graph already knows every function, struct, class, import, and call relationship. Scanning files without checking the graph first is wasteful — the graph gives you the map, then you Read only what matters.

- `base ast query --contains "auth"` (or `base a q -c "auth"`) — find entities by name
- `base ast query --file "main.rs"` (or `base a q -f "main.rs"`) — list entities in a file
- `base ast query --calls "validate"` — find all callers of a function
- `base ast query --imports "config.rs"` (or `base a q -i "config.rs"`) — find importers
- `base ast query --target apps/X -c "auth"` — query a specific app's map from anywhere (e.g. the parent workspace), no `cd` needed
- `base ast list` — see which apps have a code map, with entity counts + paths

Each app keeps its own self-contained map at `<app>/.base-ast/ast.ttl`, registered in the workspace graph and kept current automatically (a Stop hook refreshes the cwd app's map after each turn). Map a new app once with `base sync --ast --target apps/X`; thereafter it stays live.

**Order of operations:** `base ast query` first → understand structure → `Read` specific lines only. Never scan-then-understand when you can understand-then-read.

### GraphRAG — ask questions across a doc corpus

- `base graph extract --target docs/` — LLM pass over markdown → concepts + relationship edges in the graph (no API key, content-cached, ~25s/doc)
- `base graph query "<question>"` — retrieve the relevant subgraph and synthesize a **cited** answer in one command
- `base graph query "<q>" --raw` — return just the retrieved subgraph for the current session to reason over (highest-quality path)
- `base graph analyze` — emergent structure: god nodes (core abstractions), communities, surprising cross-community bridges

**Agentic retrieval** (read-only primitives — drive your own multi-call traversal instead of one-shot query):
- `base graph get-node "<label|slug>"` — one node's type, source, summary, and edges
- `base graph neighbors "<node>" -d N` — the N-hop neighborhood as edge lines
- `base graph path "<from>" "<to>"` — shortest path between two concepts

**Multimodal ingest is OFF by default** (markdown-only, zero extra deps). PDF/image/audio/video need it on:
- `base config set multimodal.enabled true` (or one-shot `base graph extract --multimodal`)
- **No sudo, ever.** PDF → in-process (`pdf-extract` crate, zero dep); image → Claude vision (uses the present `claude`, zero dep); audio/video → Whisper, whose `whisper`+`ffmpeg` install **once** via `pip install --user` (marker-gated), never again. An operator who never enables it — or only feeds docs/images — installs nothing.

### Project management

- `base project add --name "..." --path "src/x"` (or `base p a -n "..." -p "src/x"`) — register a project
- `base project list` (or `base p l`) — list projects
- `base milestone add --project X --name "..."` (or `base m a -p X -n "..."`) — add a milestone
- `base task add --project X --name "..."` (or `base t a -p X -n "..."`) — add a task
- `base task done <slug>` — mark complete

### Deferred work

Deferred means open but paused: a handoff, fork, task or milestone nobody has touched inside its window. Session start does not list it, and every block ends with its count and the command that lists it. Nothing deferred is lost.

Bring one back with `base handoff show <what the user said>` (forks: `base fork show`), which revives a deferred match and prints its doc. A task or milestone the pass deferred comes back at the next session start once a base command has touched it; any deferred task or milestone comes back with `base task update <slug> --status active` or `base milestone update <slug> --status active`. List them with `base handoff deferred`, `base fork deferred`, `base task deferred`, `base milestone deferred` and `base project deferred`.

Config: `[defer] enabled` (off unless set), `mode` (`"asset"` or `"global"`), `global_days` (10 when unset), and one `[defer.days]` key per type: `handoff`, `fork`, `task`, `milestone`, `project`. A project with no key reads `[protocol] stale_days`. Preview the pass with `base reconcile --dry-run`.

### Knowledge & memory

- `base learn --text "..." --domain X --type insight` — structured memory with relational edges
- `base recall --keyword "..." [--domain X]` — graph-backed relational search
- `base decision log --domain X --decision "..." --rationale "..."` — log a decision
- `base decision search --keyword "..."` — find prior decisions
- `base rule add --domain X --text "..." --keywords "a, b" --fires-on "<prompt>"` — add a rule to a domain; inside a session it needs the words from the prompt that should bring it back and that prompt as its first test (a rule for file work also takes `--path`)

### Sync & dashboard

- `base sync` — extract markdown metadata + body into graph
- `base sync --ast` — extract code structure (tree-sitter, 35+ languages)
- `base dashboard` (or `base dash`) — launch Command Center web dashboard

### What happens automatically (via hooks)

- **Session start:** Graph syncs domains, ingests paul.toml projects, runs signals
- **User prompt:** Matches keywords → injects domain rules + decisions + notes from graph
- **Pre-tool-use:** Matches file paths → injects AST file map + domain rules. Intercepts grep with graph hint. Injects markdown extraction contract on Write/Edit of .md files.
- **Post-tool-use:** Updates timestamps. Injects section-specific AST context for partial reads.

### Architecture

- Rules, decisions, notes, and projects are graph entities with relational edges
- `domains.toml` defines triggers only (keywords, paths) — rule content lives in the graph
- `~/.base-gbl/` = global tier, `{workspace}/.base/` = workspace tier
- Built by Chris Kahler · https://docs.basemode.ai
