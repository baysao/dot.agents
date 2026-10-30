# PAUL × base Integration Map

Inventory from all 29 `paul-*/SKILL.md` + `reflect/SKILL.md` (verified 2026-10-29).

## base — 4 integration surfaces

### 1. Task tracking (board mirror)
- **APPLY** (`paul-apply:60`): creates **one** base task per plan, named with plan-id prefix (`08-01 implement auth`). Never per PAUL task — `.paul/` owns fine grain.
- **UNIFY** (`paul-unify:77`): finds the task by the same prefix, `base task done <slug>`. On conflict `.paul/` wins.

### 2. AST map (structural queries)
- **MAP** (`paul-map-codebase:37`): `base sync --ast` before spawning agents; Explore agents use `base ast query` (`--calls`, `-f`, `-c`) before reading files.
- **PLAN** (`paul-plan:62`): measured callers/imports become plan **Facts**; grep fallback when base absent.
- **RESEARCH/RESEARCH-PHASE** (`paul-research:42`, `paul-research-phase:49`): AST query injected into codebase-agent toolkit.

### 3. Memory (decision promotion only)
- **UNIFY** (`paul-unify:73`): decisions that outlive their topic → `base decision log`. **Never keep the same fact live in both.**
- **UNIFY** (`paul-unify:77`): claims `*base` memory sweep (handoff/learnings/decisions) runs inside the reflect pass — **but `reflect/SKILL.md` has zero base mentions**; that sweep lives in `~/.claude/paul-framework/`, not the skill.

### 4. Project registration
- **REGISTER** (`paul-register:12`): writes `.paul/paul.json` manifest so BASE satellite auto-discovers the project.

**Zero occurrences** of `base learn` or `base recall` anywhere in PAUL skills. Two base rules in the PAUL domain (added 2026-10-29) are a new layer on top, justified because they use session-start injection (which base is allowed to own).

## Notable gaps

1. **`base learn`/`base recall` = 0 uses.** The two rules in the base PAUL domain (added 2026-10-29) are the first wiring for it — justified because they use session-start injection (which base is explicitly allowed to own).
2. **`*base` memory sweep is undocumented in reflect** — ✅ **RESOLVED 2026-10-29**: the sweep lives in the framework, not the repo skill. `~/.claude/paul-framework/workflows/unify-phase.md:245-283` (reflect close-out writes `base learn` + `base decision log`, tags `paul,phase-{N},plan-{NN}-{PP}` / `paul,reflect-validated,...`) and `workflows/base-sync.md` (decision search + learn + decision log with worked examples). Milestone close does the same at `complete-milestone.md:436-461`. The repo `reflect/SKILL.md` correctly has zero base — it mines learnings; the framework unify workflow persists them.
3. **paul-handoff has zero base mentions** despite being listed in what the sweep supposedly covers.

## Addendum — verification & suggested wiring (2026-10-29)

### Verified

- **PAUL domain rules inject.** `base context "paul-plan resume the loop"` returns both PAUL rules (learn @0, recall @1) plus the GLOBAL MOP rule. Both rules carry `--fires-on`/`--quiet-on` tests (attached 2026-10-29 via `--supersedes` chains `paul/cli-0→cli-2→cli-3` and `paul/cli-1→cli-4`); `base rule test --domain PAUL` is green (0 misses, 0 false fires). Gotchas: `--supersedes` needs the `domain/slug` form, not the display hash; quiet-on prompts must avoid domain keywords (any `paul*` prompt false-fires keyword `paul`). Write path smoke-tested: `base learn --domain PAUL --type insight` from the workspace persisted successfully.
- **`base help` / local profile** written to `~/.claude/base-help/local/profile.md` (first run on this machine). doctor: HEALTHY; star commands: 4 (`*handoff *fork *base *end`).
- **Wiring #1/#2 smoke-tested live 2026-10-29** from the workspace: `base handoff create --project fcom-trading-platform --doc <tmp> --slug smoke-test` registered and listed (open → archived); `base reminder add --due today` surfaced immediately and `reminder archive`/`remove` cleared it. Note: `base handoff` has no `remove` subcommand — `archive` is the terminal state (inert, never resurfaces).

### Wiring status (1–3 implemented 2026-10-29; 4–6 skipped)

| # | Where | Change | Why |
|---|---|---|---|
| 1 | `paul-handoff` ✅ | Step 3 now registers created docs: `base handoff create --project "<p>" --doc "<abs-path>"` (guarded on `base` resolving) | handoffs are exempt from suppression — surface every session start until acted on |
| 2 | `paul-apply` checkpoint tasks ✅ | Step 3 now runs `base reminder add --name "PAUL checkpoint: ..." --due ...` on `checkpoint:human-action`/`human-verify` pause; closed via `base reminder archive` (there is no `reminder done` subcommand) | lands in session-start DUE NOW; reminder is surfacing only, loop state stays in `.paul/` |
| 3 | `paul-discuss` / `paul-research` ✅ | Step 2/1 now runs `base graph query "<question>" --raw` for open-ended "why" questions (guarded on `base` resolving); session synthesizes from the returned subgraph | traverses edges vs `recall`'s keyword hits. **Gotcha 2026-10-29:** without `--raw`, base shells out to `claude -p` for synthesis, which inherits `ANTHROPIC_MODEL=z-ai/glm4.7` (gateway) and fails (`[claude-code:unrecognized_model]`); `-m haiku` hangs on the same gateway. `--raw` prints the subgraph instantly — qa.md calls it the highest-quality path anyway. |
| 4 | `paul-unify` close | **skipped — redundant.** UNIFY already runs the `*base` memory sweep inside its reflect pass (paul-unify:77); `*end` is for ending a session with work open, not for closing the loop. UNIFY *is* the close-out. | would double-sweep and add a spurious handoff at loop close |
| 5 | multi-session only | **skipped — not used.** `base relay claim` / advisory lock on `.paul/STATE.md` is only needed when parallel sessions write the same project. No evidence of multi-session use yet. | conditional; add when parallel sessions actually happen |
| 6 | pstack | **skipped — too noisy.** A `--tool Task` rule fires on every Task spawn; the model defaults are already in `pstack-models.md` and poteto-mode reads them. The base rule would be a second, global copy that can't be scoped to one project. | not worth the noise; the existing `SPECIAL-FLOWS` preset row already routes base questions to `base-help` |

### Environment blockers

- ~~**No base workspace**~~ ✅ **RESOLVED 2026-10-29**: workspace at `~/project/akka/dev/apps/fcom-trading-platform` existed already; `base scaffold` re-synced it (3 domains, code map kept). `base recall` / `base decision search` now execute from there (empty graph = expected new-project state). Note: commands still refuse from the skills dir itself — run memory commands with that project as cwd (or a session opened there).
- `base domain sync --global` fails without workspace (harmless — rules already written directly to graph and verified via `base context`).
- **Gateway model breaks base's LLM subprocesses** (2026-10-29): `base graph query` without `--raw`, and `base graph extract`, shell out to `claude -p`, which inherits `ANTHROPIC_MODEL=z-ai/glm4.7` (bluesminds gateway) and fails with `[claude-code:unrecognized_model]`; `-m haiku` maps to another gateway id and hangs. Use `--raw` for graph query; any synthesis-requiring base command is unusable on this machine until the gateway publishes a Claude-Code-recognized model id or a model-config window entry.
