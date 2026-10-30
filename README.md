# ~/.agents — PAUL × BASE × EGM × AEGIS

This directory is the root of the local agent-skill installation. It contains the **PAUL** phase-loop skills, the **BASE** memory/satellite integration, the **EGM** (Elephant-Goldfish Model) design skills, the **AEGIS** adversarial audit framework, and shared configuration.

### Upstream repositories

| Project | Repository |
|---------|------------|
| **AEGIS** | https://github.com/ChristopherKahler/aegis |
| **PAUL** | https://github.com/ChristopherKahler/paul |
| **BASE** | https://github.com/ChristopherKahler/base |
| **pstack** | https://github.com/backnotprop/pstack |
| **EGM** (Elephant-Goldfish Model) | https://github.com/google/elephant-goldfish-model |

```
~/.agents/
├── README.md              # this file
├── AGENTS.md              # shell/coding conventions (Karpathy + ponytail)
├── PAUL-BASE-CARL-INTEGRATION.md  # BASE-only integration map (CARL removed)
├── pstack-models.md       # pstack model routing configuration
├── skills/                # all installed skills (paul-*, egm-*, aegis-*, etc.)
├── paul-framework/        # PAUL workflows, templates, references, rules
├── aegis/                 # AEGIS adversarial audit framework
├── base/                  # BASE satellite configuration
├── commands/              # legacy command shims
├── rules/                 # global rule store
└── update.ps1             # skill update script
```

---

## 1. paul-pstack — Model Routing for PAUL Phases

**File:** `~/.agents/pstack-models.md`

`paul-pstack` is the model-routing layer consulted by `paul-plan` during **Step 3 (Draft the Plan)**. It maps types of work to the model that should run them, using `pstack-models.md` as the single source of truth.

### Format

One line per role:
```
<work-type>, <work-type>: <model-or-mode>
```

Values:
- `inherit-parent` / `auto` — the role runs on the parent chat model (omit the subagent `model`).
- A model name — forces that model for the role.

### Example

```
feature, refactoring: inherit-parent
bug-fix: inherit-parent
perf-issue: inherit-parent
judgment and prose: inherit-parent
hardest tasks: inherit-parent
```

### How `paul-plan` uses it

When drafting a plan, `paul-plan` populates the plan's `<skills>` section by work type:

| Work type | Default skill |
|-----------|---------------|
| Quick-fix (1 file, 1 change) | `tdd` if a cheap local test path exists, else `poteto-mode` bug-fix playbook |
| Standard feature | `poteto-mode` feature playbook; add `architect` when a task crosses a function boundary |
| Bug fix | `poteto-mode` bug-fix playbook |
| Refactoring | `poteto-mode` refactoring playbook |
| Perf | `poteto-mode` perf-issue playbook |
| Complex (6+ tasks) | `arena` for contested design forks + `swarm` for parallel research slices |
| Docs-heavy phase | `technical-writing` + `unslop` |

Confirm skill choices at plan approval before applying.

---

## 2. paul-base — BASE Memory & Satellite Integration

**Reference:** `~/.agents/PAUL-BASE-CARL-INTEGRATION.md`

`paul-base` is the BASE integration layer (CARL has been fully removed). It provides four integration surfaces across the PAUL skills:

### Surface 1 — Task Tracking (board mirror)

- **`paul-apply`** (`paul-apply:60`): creates **one** base task per plan, named with plan-id prefix (e.g. `08-01 implement auth`). Never per PAUL task — `.paul/` owns fine grain.
- **`paul-unify`** (`paul-unify:77`): finds the task by the same prefix, `base task done <slug>`. On conflict `.paul/` wins.

Commands: `base task done <slug>`, `base reminder add --name "..." --due ...`, `base reminder archive`

### Surface 2 — AST Map (structural queries)

- **`paul-map-codebase`** (`paul-map-codebase:37`): `base sync --ast` before spawning agents. Explore agents use `base ast query` (`--calls`, `-f`, `-c`) before reading files.
- **`paul-plan`** (`paul-plan:62`): measured callers/imports become plan **Facts**; grep fallback when base is absent.
- **`paul-research` / `paul-research-phase`**: AST query injected into the codebase-agent toolkit.

Commands: `base sync --ast`, `base ast query --calls -f <symbol> -c <context>`

### Surface 3 — Memory (decision promotion only)

- **`paul-unify`** (`paul-unify:73`): decisions that outlive their topic → `base decision log`. **Never keep the same fact live in both.**
- **`paul-unify`** (`paul-unify:77`): `*base` memory sweep (handoff/learnings/decisions) runs inside the reflect pass.

Commands: `base decision log --domain <project> --decision "..." --rationale "..." --recall "..."`, `base learn --domain <project> --type insight|correction|commitment|shift --text "..."`

> **Note:** Zero occurrences of `base learn` or `base recall` exist in PAUL skills themselves. The two base rules in the PAUL domain (added 2026-10-29) use session-start injection, which base is explicitly allowed to own.

### Surface 4 — Project Registration

- **`paul-register`** (`paul-register:12`): writes `.paul/paul.json` manifest so the BASE satellite auto-discovers the project.

### Verified wiring (2026-10-29)

- `base context "paul-plan resume the loop"` returns both PAUL rules (learn @0, recall @1) plus the GLOBAL MOP rule.
- `base rule test --domain PAUL` is green (0 misses, 0 false fires).
- `base learn --domain PAUL --type insight` from the workspace persisted successfully.
- `base handoff create --project <p> --doc <abs-path> --slug ` registered and listed.
- `base reminder add --due today` surfaced immediately; `reminder archive`/`remove` cleared it.

### Known blocker

`base graph query` without `--raw` shells out to `claude -p`, which inherits `ANTHROPIC_MODEL=z-ai/glm4.7` (gateway) and fails. Always use `--raw` for graph queries on this machine.


---

## 3. paul-egm — EGM → PAUL Design Handoff

**Reference:** `~/.agents/skills/paul-plan/SKILL.md` (Step 2, Step 4)

`paul-egm` is the integration between **EGM** (Elephant-Goldfish Model) design skills and **PAUL** phase-loop skills. EGM produces design artifacts; PAUL breaks them into executable plans.

### EGM skills (in `~/.agents/skills/egm-*`)

| Skill | Output artifact | Purpose |
|-------|----------------|---------|
| `egm-bootstrap` | `README.md` files | Bootstraps directory-tree context |
| `egm-brainstorm` | `concepts_brief.md` | Multi-lens ideation → RFC summary |
| `egm-draft` | `docs/designs/<FEATURE>.md` | Section-by-section design doc |
| `egm-review` | `comprehension_report.md`, `critic_report.md`, `implementation_readiness_report.md` | 5-stage Goldfish design review |
| `egm-resolve` | edited design doc | Resolve review findings (CONTEST/ESCALATE/PROPOSE FIX/DECLINE) |
| `egm-drift-report` | `{date}_DRIFT_REPORT.md` | Detect design/code drift |

### Handoff flow

```
egm-brainstorm → concepts_brief.md
    ↓ (user gates to proceed)
egm-draft → docs/designs/<FEATURE>.md
    ↓ (egm-review + egm-resolve polish it)
    ↓ HANDOFF: user runs `paul-plan <plan-id>` with design doc as context
paul-plan → PLAN.md + acceptance criteria (ingesting design doc)
    ↓
paul-apply → code
    ↓
paul-unify → SUMMARY.md + STATE.md closure
    ↓ (periodically)
egm-drift-report → drift check
```

### How `paul-plan` ingests EGM

**Step 2 (Load Context)** now probes for an EGM design doc:

> Probe for an EGM design doc: `docs/designs/<FEATURE>.md` (or `<project>/docs/designs/`). If found, ingest it as Priority 1 context — the design doc's decisions, interfaces, and dependencies become plan Facts. Search BASE for prior decisions on this topic (`base recall` / `base decision search`) and inherit them as written decisions, never re-asked or silently re-guessed. If no design doc exists, continue without it.

**Step 4 (Close the Loop)** logs durable decisions to BASE:

> If the user's approval settled a durable judgment call that outlives this plan, log it with `base decision log` (rationale plus recall keywords from the plan topic).

### Handoff gates (documented, zero code)

| EGM step | Output | PAUL input | How to hand off |
|----------|--------|------------|-----------------|
| `egm-draft` | `docs/designs/<FEATURE>.md` | `paul-plan` context | After design finalized, run `paul-plan <plan-id>` |
| `egm-review` findings | review reports | `paul-consider-issues` / `paul-plan-fix` | Review findings become issues → fix plans |
| `egm-drift-report` | `{date}_DRIFT_REPORT.md` | `paul-verify` / `paul-status` | Drift findings feed into PAUL verification cycle |

---

## 4. aegis — Adversarial Audit Framework

**Location:** `~/.agents/aegis/`

AEGIS is an adversarial audit and risk-assessment framework with agents, personas, workflows, domains, rules, schemas, and tools.

### Directory structure

```
~/.agents/aegis/
├── core/                  # Core audit cycle
│   ├── agents/            # 12 core agents (architect, security-engineer, sre, etc.)
│   ├── personas/          # 12 matching personas
│   └── workflows/         # Phases 0-5 + checkpoint + handoff + disagreement-resolution
├── domains/               # 14 domain files (00-context through 13-risk-synthesis)
├── rules/                 # agent-boundaries, disagreement-protocol, epistemic-hygiene
├── schemas/               # confidence, disagreement, finding, report-section, signal
├── tools/                 # checkov, git-history, gitleaks, grype, semgrep, sonarqube, syft, trivy
└── transform/             # Transform/remediation sub-framework
    ├── agents/            # change-risk-modeler, execution-validator, guardrail-generator, etc.
    ├── personas/
    ├── rules/             # change-risk-rules, safety-governance
    ├── schemas/           # change-risk, intervention-level, playbook, verification-plan
    └── workflows/         # Phases 6-8 + transform-safety
```

### Core audit phases

| Phase | File | Purpose |
|-------|------|---------|
| Phase 0 | `core/workflows/phase-0-context.md` | Establish context and scope |
| Phase 1 | `core/workflows/phase-1-reconnaissance.md` | Reconnaissance and asset discovery |
| Phase 2 | `core/workflows/phase-2-domain-audits.md` | Per-domain audits (architecture, data, security, etc.) |
| Phase 3 | `core/workflows/phase-3-cross-domain.md` | Cross-domain synthesis |
| Phase 4 | `core/workflows/phase-4-adversarial-review.md` | Adversarial review (red team) |
| Phase 5 | `core/workflows/phase-5-report.md` | Report generation |

### Transform phases (remediation)

| Phase | File | Purpose |
|-------|------|---------|
| Phase 6 | `transform/workflows/phase-6-remediation.md` | Remediation planning |
| Phase 7 | `transform/workflows/phase-7-risk-validation.md` | Risk validation |
| Phase 8 | `transform/workflows/phase-8-execution-planning.md` | Execution planning |
| Safety | `transform/workflows/transform-safety.md` | Safety governance |

### Key agents (core)

- `architect`, `compliance-officer`, `data-engineer`, `devils-advocate`
- `performance-engineer`, `principal-engineer`, `reality-gap-analyst`
- `security-engineer`, `senior-app-engineer`, `sre`, `staff-engineer`, `test-engineer`

### Key tools

- `checkov`, `git-history`, `gitleaks`, `grype`, `semgrep`, `sonarqube`, `syft`, `trivy`

### Using AEGIS with PAUL

AEGIS feeds into the PAUL loop at the verify/unify boundary:

1. Run an AEGIS audit phase (e.g. `phase-4-adversarial-review`) to produce findings.
2. Findings become issues via `paul-consider-issues` or `paul-plan-fix`.
3. Fix plans are created with `paul-plan-fix` and applied with `paul-apply`.
4. Durable risk decisions are logged with `base decision log` via `paul-unify`.

---

## 5. Full PAUL Skill Reference

All 27 `paul-*` skills live in `~/.agents/skills/paul-*`:

| Skill | Purpose |
|-------|---------|
| `paul-add-phase` | Add a new phase to the roadmap |
| `paul-add-plan` | Add a plan to a phase |
| `paul-apply` | Execute plan tasks; creates base task mirror |
| `paul-assumptions` | Phase assumptions workflow |
| `paul-audit` | Audit plan/code |
| `paul-complete-milestone` | Close a milestone |
| `paul-config` | Configure project/CARL/BASE settings |
| `paul-consider-issues` | Consider issues for a plan |
| `paul-discover` | Discover project context |
| `paul-discuss` | Discuss a phase/plan |
| `paul-discuss-milestone` | Discuss milestone status |
| `paul-flows` | Special flows configuration |
| `paul-handoff` | Register handoffs (BASE-integrated) |
| `paul-help` | PAUL help |
| `paul-init` | Initialize a PAUL project |
| `paul-map-codebase` | AST map of codebase (BASE-integrated) |
| `paul-milestone` | Milestone management |
| `paul-pause` | Pause work (BASE reminder) |
| `paul-plan` | Create/continue a PLAN (EGM + BASE integrated) |
| `paul-plan-fix` | Fix plan from UAT issues |
| `paul-progress` | Progress tracking |
| `paul-register` | Register project with BASE |
| `paul-remove-phase` | Remove a phase |
| `paul-research` | Research with AST queries (BASE-integrated) |
| `paul-research-phase` | Research phase |
| `paul-resume` | Resume a project |
| `paul-status` | Project status |
| `paul-unify` | Reconcile plan vs actual; close loop (BASE-integrated) |
| `paul-verify` | Verify work |

PAUL phase loop: **plan → apply → unify → (fix if issues)**

---

## 6. Quick Start

```bash
# 1. Register your project with BASE
paul-register <project-name>

# 2. (Optional) Run EGM design first
egm-brainstorm          # → concepts_brief.md
egm-draft               # → docs/designs/<FEATURE>.md

# 3. Plan the work (paul-plan ingests EGM design doc if present)
paul-plan <plan-id>

# 4. Route skills via pstack (check pstack-models.md)
#    Confirmed at plan approval

# 5. Apply the plan
paul-apply <plan-id>

# 6. Unify / close the loop (logs decisions to BASE)
paul-unify <plan-path>

# 7. If issues found, create fix plan
paul-plan-fix <plan-id>

# 8. Periodic drift check
egm-drift-report docs/designs/
```

---

## 7. Path Convention

All tool/framework paths in this installation use `~/.agents/` as the root (migrated from `~/.claude/` on 2026-10-30):

- `~/.agents/skills/` — skill definitions
- `~/.agents/paul-framework/` — PAUL workflows/templates/references
- `~/.agents/aegis/` — AEGIS framework
- `~/.agents/pstack-models.md` — pstack model routing
- `~/.agents/PAUL-BASE-CARL-INTEGRATION.md` — BASE integration map (CARL removed)