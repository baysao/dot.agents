# ~/.agents — PAUL × EGM × AEGIS

This directory is the root of the local agent-skill installation. It contains the **PAUL** phase-loop skills, the **EGM** (Elephant-Goldfish Model) design skills, the **AEGIS** adversarial audit framework, and shared configuration.

**BASE is no longer part of PAUL** (removed 2026-11-03). The `base` CLI and the `base-help` skill remain installed; nothing in the PAUL path calls them.

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
├── PAUL-BASE-CARL-INTEGRATION.md  # historical record — base removed from PAUL 2026-11-03
├── pstack-models.md       # pstack model routing configuration
├── skills/                # all installed skills (paul-*, egm-*, aegis-*, etc.)
├── paul-framework/        # PAUL workflows, templates, references, rules
├── aegis/                 # AEGIS adversarial audit framework
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

## 2. paul-base — REMOVED (2026-11-03)

The `base` integration was removed from every PAUL skill, command, and workflow on
2026-11-03. There are now zero `base` CLI calls on the PAUL path and nothing reads
`.base/`.

State that used to route to the graph lives in `.paul/` and nowhere else:

| Item | Store | Read by |
| --- | --- | --- |
| Learnings | `.paul/LEARNINGS.md` | `paul-plan` Step 2, `paul-resume` |
| Decisions | `.paul/DECISIONS.md` + `STATE.md` `### Decisions` | `paul-plan` Step 5, `paul-resume` |
| Rules | `## Session Rules` in `.paul/SPECIAL-FLOWS.md` | `paul-apply`, `paul-resume` |
| Paused checkpoints | `STATE.md` Session-Continuity, as **DUE NOW** lines | `paul-resume` |

`PAUL-BASE-CARL-INTEGRATION.md` is a historical record of the removed integration.
Nothing links to it operationally. The `base` CLI and the `base-help` skill are left
installed and untouched — they are simply no longer part of PAUL.

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
| `egm-drift-report` | `docs/drift/{date}_DRIFT_REPORT.md` | Detect design/code drift |

### Handoff flow

Solid arrows are implemented. The dashed step is not: a drift report has no
consumer in PAUL, so reading it and opening a fix plan is your job, not the loop's.

```
egm-brainstorm → concepts_brief.md
    ↓ (user gates to proceed)
egm-draft → docs/designs/<FEATURE>.md
    ↓ (egm-review + egm-resolve polish it)
    ↓ HANDOFF: user runs `paul-plan <plan-id>` with design doc as context
paul-plan → PLAN.md + acceptance criteria (reads the design doc)
    ↓
paul-apply → code
    ↓
paul-unify → SUMMARY.md + STATE.md closure
    ⋯⋯ (periodically, manual) egm-drift-report → docs/drift/{date}_DRIFT_REPORT.md
```

### How `paul-plan` ingests EGM

**Step 2 (Load Context)** now probes for an EGM design doc:

> Probe for an EGM design doc: `docs/designs/<FEATURE>.md` (or `<project>/docs/designs/`). If found, ingest it as Priority 1 context — the design doc's decisions, interfaces, and dependencies become plan Facts. Read `.paul/DECISIONS.md` for prior decisions on this topic and inherit them as written decisions, never re-asked or silently re-guessed. If no design doc exists, continue without it.

**Step 4 (Close the Loop)** writes durable decisions to `.paul/DECISIONS.md`:

> If the user's approval settled a durable judgment call that outlives this plan, append it to `.paul/DECISIONS.md` as `D-NN` (rationale plus the plan topic), and add the summary row to `STATE.md`'s `### Decisions` table.

### Handoff gates — one is implemented, two are not

Measured against the code on 2026-11-03. Do not read this table as a pipeline.

| EGM step | Output | PAUL input | Status |
|----------|--------|------------|--------|
| `egm-draft` | `docs/designs/<FEATURE>.md` | `paul-plan` Step 2 item 5 | **Implemented.** The only EGM→PAUL mechanism: a read of the design doc as Priority 1 plan context. |
| `egm-review` findings | `comprehension_report.md`, `critic_report.md`, `implementation_readiness_report.md` | `paul-consider-issues` / `paul-plan-fix` | **Manual only.** No PAUL skill names those files. You carry the findings across by hand and open a fix plan. |
| `egm-drift-report` | `docs/drift/{date}_DRIFT_REPORT.md` | none | **No consumer.** Nothing in PAUL reads a drift report; `paul-verify` and `paul-status` contain zero references to one. Read it yourself and, if a finding warrants work, open a `paul-plan-fix`. |

EGM writes nothing into `.paul/`, exposes no gate, and ships no command into
`commands/`. Anything describing EGM as an automated stage of the PAUL loop is
describing an intention, not the install.

### Interaction rules for EGM skills

All seven `egm-*` skills carry `disable-model-invocation: true`. The model cannot
call them; invoke them yourself in prose, e.g. `Use egm-drift-report: docs/designs/`.
There are no `/egm-*` slash commands in this install — references to one in the
upstream EGM docs assume the plugin packaging, not `~/.agents/skills/`.

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
4. Durable risk decisions are logged in `.paul/DECISIONS.md` via `paul-unify`.

---

## 5. Full PAUL Skill Reference

All 30 `paul-*` skills live in `~/.agents/skills/paul-*`:

| Skill | Purpose |
|-------|---------|
| `paul-add-phase` | Add a new phase to the roadmap |
| `paul-add-plan` | Add a plan to a phase |
| `paul-apply` | Execute plan tasks |
| `paul-assumptions` | Phase assumptions workflow |
| `paul-audit` | Audit plan/code |
| `paul-complete-milestone` | Close a milestone |
| `paul-config` | Configure project settings, flows, and integrations |
| `paul-consider-issues` | Consider issues for a plan |
| `paul-discover` | Discover project context |
| `paul-discuss` | Discuss a phase/plan |
| `paul-discuss-milestone` | Discuss milestone status |
| `paul-flows` | Special flows configuration |
| `paul-handoff` | Write and register handoffs |
| `paul-help` | PAUL help |
| `paul-init` | Initialize a PAUL project |
| `paul-map-codebase` | Map the codebase |
| `paul-milestone` | Milestone management |
| `paul-pause` | Pause work |
| `paul-plan` | Create/continue a PLAN (EGM integrated) |
| `paul-plan-fix` | Fix plan from UAT issues |
| `paul-progress` | Progress tracking |
| `paul-register` | Create the project manifest |
| `paul-remove-phase` | Remove a phase |
| `paul-research` | Research a topic |
| `paul-research-phase` | Research phase |
| `paul-resume` | Resume a project |
| `paul-security` | Security audit of the diff; findings become debt rows |
| `paul-status` | Project status |
| `paul-unify` | Reconcile plan vs actual; close loop |
| `paul-verify` | Verify work |

PAUL phase loop: **plan → apply → unify → (fix if issues)**

---

## 6. Quick Start

```bash
# 1. Create your project manifest
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

# 6. Unify / close the loop (writes learnings/decisions to .paul/)
paul-unify <plan-path>

# 7. If issues found, create fix plan
paul-plan-fix <plan-id>

# 8. Periodic drift check (manual — no PAUL consumer; read the report yourself)
#    Ask: Use egm-drift-report: docs/designs/
#    Writes docs/drift/{YYYY-MM-DD}_DRIFT_REPORT.md
```

---

## 7. Path Convention

All tool/framework paths in this installation use `~/.agents/` as the root (migrated from `~/.claude/` on 2026-10-30):

- `~/.agents/skills/` — skill definitions
- `~/.agents/paul-framework/` — PAUL workflows/templates/references
- `~/.agents/aegis/` — AEGIS framework
- `~/.agents/pstack-models.md` — pstack model routing
- `~/.agents/PAUL-BASE-CARL-INTEGRATION.md` — historical record of the removed BASE integration