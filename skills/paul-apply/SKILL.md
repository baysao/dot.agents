---
name: paul-apply
description: Execute an approved PAUL PLAN with checkpoint handling. Use after plan approval to run tasks sequentially.
metadata:
  opencode/slash: "true"
---

## Purpose

Execute an approved `PLAN.md` file, handling checkpoints as they occur. Runs tasks in sequence, pauses at checkpoints for user input, reports completion.

Use it after PLAN phase is complete and the plan is approved.

## Input

Bring the plan target — rough is fine:

- **Works best with:** a plan path (e.g. `.paul/phases/01-foundation/01-01-PLAN.md`)
- **Also useful:** nothing else; state is loaded from `.paul/STATE.md`

If you supply the path inline, execution starts there — it won't re-ask. With no input, it asks which plan to execute.

Example: `Use paul-apply: execute .paul/phases/01-foundation/01-01-PLAN.md`

## Key Concepts

### Framework Sources of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/apply-phase.md` — execution workflow to follow
- `~/.agents/paul-framework/references/checkpoints.md` — checkpoint semantics

### Checkpoint Types

- `checkpoint:decision` - present options, wait for selection, then append the choice as a `D-NN` row in `.paul/DECISIONS.md` and the same row in the `STATE.md` `### Decisions` table, then continue
- `checkpoint:human-verify` — present build + verification steps, wait for approval or issues, address and re-verify if needed
- `checkpoint:human-action` — present required manual action, wait for done confirmation

### Guard

Derive the SUMMARY path by replacing `PLAN.md` with `SUMMARY.md`. If SUMMARY already exists the plan was already executed — offer re-execute or exit.

### Where a Deviation Goes

A task you skip, a shortcut you take, or a nice-to-have you notice mid-plan is a **deferral** the moment it leaves your hands. It has exactly two destinations:

| The thing you noticed | Where it goes |
|---|---|
| It has a landing condition (a file to delete, a check to re-run, a decision someone must make) | a `[[debt]]` row in `.paul/DEBT.toml`, with a runnable `check` |
| It has none — pure nice-to-have, no way to test it | `.paul/ISSUES.md` |

Do not "record it in the SUMMARY and continue": UNIFY reads a plan, not a transcript, and a deferral whose only trace is prose is a deferral nobody will discharge. **Do not create `.paul/ISSUES.md` for anything with a landing condition** — that file has no checks, so nothing can ever discharge it.

```toml
[[debt]]
id = "DEBT-0NN"                  # next free id
title = "What is owed, one line"
kind = "tech"                    # artifact | reopen | decision | tech | uat
origin = "01-02 task 3"          # phase-plan and task
owner = "agent"                  # agent | owner | phase-NN | vendor
due = "2026-11-05T09:00:00Z"     # omit if event-gated
trigger = "event:probe-close"    # or phase:NN / plan-count:N — at least one of due/trigger/blocking
check = { type = "command", command = "...", expect = "..." }
```

`debt.py` rejects a row that has no `due`, `trigger`, or `blocking` — that is the point. The check must be able to fail; a check that cannot fail reports a deferred item as done.

When a deferral is blocking this plan's own exit, set `blocking = "phase-NN-exit"` so the phase gate will refuse to close until it is discharged or explicitly dropped.

## Application

### Step 1: Validate Plan

1. Confirm the plan file exists; error `Plan not found: {path}` if not.
2. Derive the SUMMARY path.
3. If SUMMARY exists: report `Plan already executed. SUMMARY: {path}` and offer re-execute or exit.

### Step 1.5: Confirm Required Skills (pstack gate)

Read `.paul/SPECIAL-FLOWS.md`. If it declares required skills (for example the pstack preset), confirm each is loaded in this session before the first task. If a required skill is missing, stop and tell the user which skill to load or install. This is the APPLY block: do not start tasks while a required skill is unconfirmed.

If SPECIAL-FLOWS.md also declares CARL required, confirm the `carl-mcp` tools resolve before the first task. On failure, stop and tell the user to enable CARL — same gate shape as the pstack gate.

### Step 1.6: Check for a sibling plan on the same files

Read every other `PLAN.md` in the same phase and compare `files_modified` with this plan's. If a sibling is APPLYING or held (`loop.hold_until` set in `paul.toml`) and both write the same path, stop before the first task. Either wait for the sibling, or record the overlap in `STATE.md` naming both plans, the shared path, and the reason serializing costs more. An undocumented overlap makes every file in that path unusable as routing evidence — the next session cannot tell which plan wrote what.

### Step 1.7: Task Tracking (no external board)

Task tracking is `.paul/`'s job. One entry per plan, never per PAUL task — `STATE.md` and `PLAN.md` own the fine grain, and UNIFY reads the plan id back from them. Do not create a parallel task per PAUL task in any external tracker.

### Step 2: Execute

Follow `apply-phase.md`. For each task sequentially: read definition, execute action, run verification, confirm done criteria.

**Run the debt gate once before the first task.** `python ~/.agents/paul-framework/scripts/debt.py --run-checks` — if an `overdue` row blocks this phase (`blocking = "phase-NN-exit"`), either discharge it as part of this plan or tell the user the phase cannot close. Starting a plan on a phase that is already gated shut produces work that cannot be unified.

Two verification rules that catch the failures a task's own verify command misses:

- **After deleting or renaming a symbol, qualify needs two extra proofs:** (a) the
  parser/compiler accepts the touched files (build, `gofmt -l`, `tsc --noEmit` —
  scoped to the files you touched), and (b) a fresh grep proves no live
  reference to the old symbol remains. A text-based edit can drop the wrong
  neighbour and leave a caller pointing at a function that no longer exists;
  both show up only at compile time, so run them before claiming DONE.
- **Adding a migration:** read the repo's migration runner first. If it
  auto-discovers embedded `*.sql` files (skipping `*.down.sql`, sorted by
  filename, one transaction per file, recording each applied name in a
  migrations table), a new migration is just a new file — verify it by querying
  that table, not by restarting the app. If the runner needs a registry entry,
  the plan must name it.
- **A migration that is already applied — or that came from another branch — is
  immutable.** The runner skips files it has applied, so editing one leaves the
  repo silently diverged from the database. Copy it in byte-for-byte (verify
  with `git hash-object` against the source blob) and put every content change
  in a *new* migration file.
- **A fix in one handler is not a fix in the family.** When you remove client
  control of an identity or audit field (maker/actor ids, tenant ids), grep the
  same field across the sibling handlers in the same file and either fix them
  or enumerate the remaining ones as deviations in the summary. "The one I
  touched" is not a fix when the same spoofable field survives seven endpoints.
- **Changing a table's lookup key needs a migration, and uniqueness needs an
  error mapping.** "The table is empty" is a fact about one database, not about
  the data model: rows written by the old path can still exist. Either ship a
  backfill/CHECK migration or prove the old write path cannot produce bad
  shapes. Separately, map the driver's unique-violation code (PostgreSQL
  `23505`) to the domain sentinel that the HTTP layer maps to **409** - an
  unmapped unique violation surfaces as a generic 500 and hides a real conflict.
- **Map the whole integrity class, not one code.** `23505` (unique) is one
  member of a class: `23503` (foreign key) and `23514` (check) reach the same
  handler and surface as 500 unless each has its own sentinel. A delete that
  another row still references is a user-fixable conflict, so give it a
  sentinel and a 409 with a message that names the referencing table. Name
  every code the plan can trigger, so the family is closed, not just the case
  in front of you.
- **Enumerate the delete rules, not the one that errored.** `NO ACTION` and
  `CASCADE` are the same schema fact with opposite blast radius: `NO ACTION`
  raises an error you can turn into a 409, `CASCADE` deletes the child rows
  **silently**. Read the foreign keys of the table you are about to delete from
  (`pg_constraint` gives `confdeltype` for each) and guard every `CASCADE`
  child, not only the constraint that produced a stack trace.
- **Pre-validate what the database will reject or silently change.** Postgres
  rounds a `NUMERIC(p,s)` input that carries more than `s` decimal places, so
  the value the user typed is not the value that lands: reject it at the
  handler, per column scale. Mirror every `CHECK` constraint the write path can
  violate, including the ones an in-memory fake does not have - a green fake
  test is not evidence that the real write path is safe. Gate the change on
  the real database.
- **A field the server can derive is not the client's to send.** When a value
  is a function of authoritative rows (a converted amount, a total, a derived
  timestamp), the server computes it and ignores the client's copy; remove the
  field from the request struct so no caller thinks it is honoured. Then grep
  the sibling handlers for the same field: a client-controlled money field in
  one handler and a server-computed one in the next is the same defect twice.
- **A version-guard branch is only proven when the version goes stale
  between the read and the write.** The UI always sends the version it just
  read, so it can never produce a conflict on its own. From the verify script,
  bump `version_id` in the database (or otherwise make the stored row newer)
  between the read and the submit, then assert the exact status the API
  returns for that branch. A branch that only ever sees fresh versions is
  untested, however many green cases surround it.
- **Attribute before you repair a vanished dev row.** If a shared dev database
  loses a seeded row, run the suspect packages one at a time and re-count
  between them, then grep for scoped `DELETE`s. If every package alone leaves
  the row intact, the deletion came from outside your change (another session
  on the same database) — restore with the seeding migration's own idempotent
  SQL and say so in the summary.

### pstack Task Routing (automatic)

When the plan's `<skills>` section names pstack skills, execute each `auto` task through `poteto-mode` with the mapped playbook (feature, bug-fix, refactoring, perf-issue). poteto-mode's delegates do the Execute step. The PAUL session keeps the spec and runs the Qualify step in-session against the task's acceptance criteria, using the `prove-it-works` rule: verify against the real artifact, not a self-report. Checkpoint tasks (decision, human-verify, human-action) still gate execution and are never delegated.

### Step 3: Handle Checkpoints

Apply the checkpoint semantics from Key Concepts when a checkpoint task is reached.

When a `checkpoint:human-verify` or `checkpoint:human-action` pauses the loop, record the pending action as a `[[debt]]` row in `.paul/DEBT.toml` (`kind = "decision"`, `owner = "owner"`, `trigger = "event:..."`) **and** a STATE.md Session-Continuity DUE NOW line naming the checkpoint and the date it is owed — the debt row is what the next session machine-checks, the DUE NOW line is what it reads first. Strike the line when the checkpoint is confirmed; do not delete it, so the record shows it was raised and closed. An immortal DUE NOW bullet that no command can evaluate is exactly the failure the store exists to fix.

### Step 4: Complete

Report `APPLY complete. Run /paul:unify to close loop.` (Claude Code; in other harnesses, run the `paul-unify` skill.) Show files modified and the SUMMARY path to create.

Verify success criteria:
- [ ] All tasks executed
- [ ] All checkpoints handled
- [ ] Paused human checkpoints written as `[[debt]]` rows **and** STATE.md DUE NOW lines
- [ ] Every deferral became a debt row with a runnable check, or an ISSUES entry with none possible
- [ ] User informed of completion
- [ ] Next action clear (run unify)

## Examples

### Example: Execute Approved Plan

Input: `.paul/phases/01-foundation/01-01-PLAN.md`

Result: tasks executed in order, checkpoints resolved, completion report with unify as next step.

### Anti-Pattern Example

"Skipped checkpoint:human-verify and unified anyway."

Result: unverified work enters the summary. Always resolve checkpoints before completing.

## Common Pitfalls

- **Re-executing without checking SUMMARY.** Consequence: duplicate work or overwritten results. Fix: always derive and check the SUMMARY path first.
- **Absorbing checkpoint decisions silently.** Consequence: decisions go unrecorded. Fix: present, wait, record, then continue.
- **Parking a deferral in the SUMMARY.** Consequence: UNIFY reads a plan, not a transcript, so the deferral has no check and never discharges. Fix: write the `[[debt]]` row when the deviation happens.

## References

- `~/.agents/paul-framework/workflows/apply-phase.md`
- `~/.agents/paul-framework/references/checkpoints.md`
- `~/.agents/paul-framework/templates/DEBT.toml.md`
- `.paul/STATE.md`, `.paul/DEBT.toml`
