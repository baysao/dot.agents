---
name: paul-plan
description: Create or continue a PAUL phase PLAN with acceptance criteria. Use when starting new work or resuming an incomplete plan.
metadata:
  opencode/slash: "true"
---

## Purpose

Create or continue a PLAN for a specified PAUL phase. Produces a `PLAN.md` in the correct phase directory with acceptance criteria defined and `STATE.md` loop position updated.

Use it when starting new work or resuming an incomplete plan.

## Input

Bring the plan target — rough is fine; the workflow resolves the rest:

- **Works best with:** a phase-plan identifier (e.g. `08-01`, `08-auth`)
- **Also useful:** nothing else required; project context is loaded from `.paul/PROJECT.md`, `.paul/STATE.md`, and `.paul/ROADMAP.md`

If you supply the phase-plan inline with your request (e.g., "plan 08-01"), the skill starts with that context — it won't re-ask for what you already gave. With no input, it asks which phase-plan to create or continue.

Example: `Use paul-plan: plan 08-01`

## Key Concepts

### Framework Sources of Truth

The plan format and phase workflow are defined outside this skill — follow them, don't reinvent:

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, read the same subpaths under `~/.agents/paul-framework/`. If neither exists, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/plan-phase.md` — phase workflow to follow
- `~/.agents/paul-framework/templates/PLAN.md` — PLAN file template
- `~/.agents/paul-framework/references/plan-format.md` — plan format reference

### Project Context

- `.paul/PROJECT.md` — project definition
- `.paul/STATE.md` — current loop position (update on completion)
- `.paul/ROADMAP.md` — phase/plan roadmap

### Plan All Before Applying Any

Per PAUL workflow rules: create ALL plans for a phase before applying any of them, so cross-plan dependencies and shared types are visible upfront.

## Application

### Step 1: Resolve Target

1. Determine the phase-plan from the request.
2. If none given, ask which phase-plan to create or continue.
3. If resuming, load the existing partial `PLAN.md` for that phase-plan.
4. **Check the identifier is free.** Plan ids address a shared namespace — a sibling session or branch may already hold `NN-MM`. If `.paul/phases/<phase>/` already has that number, take the next free one; never overwrite another plan's history.

### Step 2: Load Context

1. Read `.paul/PROJECT.md`, `.paul/STATE.md`, and `.paul/ROADMAP.md`.
2. Read the workflow, template, and format reference listed under Framework Sources of Truth.
3. **Reconcile the live surfaces before drafting.** State files are claims, not facts. When the project shares a dev database between worktrees or sessions, check the applied-migration set against the repo's migration files, and look for sibling worktrees or other sessions' commits (`git worktree list`, `git log --all --oneline`). A migration version present in the database but missing from `migrations/` means another session changed the database behind your back — reconcile that first, before planning work that touches it.
4. Probe for an EGM design doc: `docs/designs/<FEATURE>.md` (or `<project>/docs/designs/`). If found, ingest it as Priority 1 context — the design doc's decisions, interfaces, and dependencies become plan Facts. Search BASE for prior decisions on this topic (`base recall` / `base decision search`) and inherit them as written decisions, never re-asked or silently re-guessed. If no design doc exists, continue without it.
5. When the `base` binary resolves and a workspace AST map exists, query every touched symbol with `base ast query` (`--calls`, `-f`, `-c`) and write the measured callers/imports into Facts. Run `base sync --ast` first when the map may be stale; fall back to grep when base is absent. This is the code-side twin of measuring Facts with the live database.

### Step 3: Draft the Plan

Follow `plan-phase.md`. The resulting `PLAN.md` must define:

- Scope and task breakdown for the phase-plan
- Acceptance criteria per task
- Verification steps per task

Two rules that keep the plan honest for the person who applies it:

- **Record decisions the user did not make.** If a scope question is dismissed,
  ignored, or answered ambiguously, adopt the recommended default **and write it
  into the plan** (the assumption + its rationale). A later reader must inherit a
  written decision, never a silent guess.
- **A plan that removes a control must say so loudly.** Removing an approval
  step, an RBAC gate, a validation, or an audit trail is a risk, not a
  simplification. Such a plan carries a visible risk block (what control is
  gone, which spec it deviates from, what the compensating control is) plus a
  backlog item, and both are surfaced at approval time.
- **Facts come from the live system, not from the request.** When the plan
  touches an existing database, measure the enums, the rates, the column
  scales, and the constraints with the database itself (`psql`) and write the
  measured values into Facts. A value taken from a spec or from a message is a
  hypothesis; if the database disagrees, the plan is wrong before anyone
  applies it. Record the value the database actually holds.
- **A plan that adds a screen must add it to the guard list, and the AC must
  prove the guard bites.** Two tasks: name the file in the style/enum guard's
  list, and require a **mutation test** in the AC (break the rule on purpose,
  assert the guard fails, restore the file, assert it passes again). A guard
  that has never failed is a self-report, and a guard list that nobody updated
  silently stops covering the new screen.

Acceptance criteria and verification must assert the **specific** error code or
branch, not just a status class, and any new fixture must fit the schema
constraints of the columns it touches — a fixture that violates a length or
CHECK constraint is caught by an earlier validation and the test then passes for
the wrong reason.

Two more rules that keep a plan honest:

- **An AC phrased as a client affordance does not certify a server invariant.**
  "The client blocks it and sends 0 requests" proves the guard exists, not that
  the server rejects the write. If the invariant must hold, the AC needs a
  server-side case too (direct API call, concurrent create, or the driver's
  error mapping) — otherwise removing the client guard silently breaks it.
- **A table that currently holds zero rows has no exercised read path.** A plan
  touching one must include a verify step that creates a representative row —
  NULL in every nullable column, inserted via raw SQL so the test does not
  exercise the very code it is testing — and must name each column's
  nullability in the Facts section. Otherwise the first real row breaks a scan
  path that no test ever ran.

When a task takes code from another branch, worktree, or session, import the
**smallest unit that solves the problem** (`git show <commit>:<path>`, then
extract the one function) and apply it by hand so it matches the local schema
shape. A whole foreign file carries that branch's assumptions — a column it
still scans, a different table set — and silently regresses local work. Record
that import boundary in the task so the next reader knows what came in and what
did not.

### pstack Skill Routing (automatic)

pstack is present when `.paul/pstack-models.md` or the global `~/.agents/pstack-models.md` exists, or the `poteto-mode` skill is invocable in this session. If present, populate the plan's `<skills>` section by work type, and confirm the choices at plan approval:

- Quick-fix (1 file, 1 change): `tdd` when a cheap local test path exists, else the `poteto-mode` bug-fix playbook
- Standard feature: `poteto-mode` feature playbook; add `architect` when a task crosses a function boundary
- Bug fix: `poteto-mode` bug-fix playbook
- Refactoring: `poteto-mode` refactoring playbook
- Perf: `poteto-mode` perf-issue playbook
- Complex (6+ tasks): add `arena` for contested design forks and `swarm` for parallel research slices
- Docs-heavy phase: `technical-writing` and `unslop`

Write it to the correct phase directory per the template.

### Step 4: Close the Loop

1. Update `STATE.md` with the new loop position.
2. If the user's approval settled a durable judgment call that outlives this plan, log it with `base decision log` (rationale plus recall keywords from the plan topic).
3. Verify success criteria:
   - [ ] PLAN.md created in correct phase directory
   - [ ] All acceptance criteria defined
   - [ ] STATE.md updated with loop position

## Examples

### Example: New Plan

Input: `plan 08-01`

Result:
- `.paul/phases/08-<name>/08-01-PLAN.md` created from template with tasks + acceptance criteria
- `STATE.md` loop position set to plan `08-01`

### Anti-Pattern Example

"Planned 08-01, immediately applied it, then planned 08-02 and discovered a shared type conflict."

Result: rework. Plan all phase plans first, then apply sequentially.

## Common Pitfalls

- **Applying before planning the whole phase.** Consequence: cross-plan dependencies surface late and force rework. Fix: finish all `PLAN.md` files for the phase before any apply.
- **Vague acceptance criteria.** Consequence: apply phase has nothing verifiable to execute against. Fix: every task gets explicit done criteria.
- **Skipping the STATE.md update.** Consequence: loop position drifts and resume lands in the wrong place. Fix: always update `STATE.md` before reporting done.
- **A dismissed scope question treated as "the user said yes".** Consequence: the plan encodes an assumption nobody made. Fix: adopt the recommended default, write it into the plan with its rationale, and flag it at approval.
- **Removing a control without a risk block.** Consequence: an approval step, gate, or validation disappears and nobody notices until an audit. Fix: risk block + backlog item, surfaced at approval.
- **A verify that only checks a status class.** Consequence: a test can pass while exercising the wrong validation branch. Fix: assert the specific error code/branch, and keep new fixtures inside the schema's limits.

## References

- `~/.agents/paul-framework/workflows/plan-phase.md`
- `~/.agents/paul-framework/templates/PLAN.md`
- `~/.agents/paul-framework/references/plan-format.md`
- `.paul/PROJECT.md`, `.paul/STATE.md`, `.paul/ROADMAP.md`
