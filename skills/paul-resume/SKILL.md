---
name: paul-resume
description: Restore PAUL context after a break with one next action. Use at session start, when the user asks "what did we do so far" / "where did we leave off", or when continuing from a handoff.
metadata:
  opencode/slash: "true"
---

## Purpose

Restore PAUL context after a session break, determine current position, and suggest exactly ONE next action.

Use it when starting a new session on an existing PAUL project. Detected handoffs are presented, then archived after work proceeds.

## Input

Optionally bring a handoff path:

- **Works best with:** a handoff path (e.g. `.paul/HANDOFF-phase10-audit.md`) — otherwise the most recent handoff is used
- **Also useful:** nothing else; STATE.md is always loaded

Example: `Use paul-resume: .paul/HANDOFF-phase10-audit.md`

## Key Concepts

### Framework Source of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/resume-project.md` — workflow to follow

### Handoff Pattern

`.paul/HANDOFF-{context}.md`. Suggest exactly ONE next action — never multiple.

### Continuity-Block Authority

STATE.md grows append-only Session-Continuity blocks, each with its own `Resume pointer` / `pending` lines. **Only the newest block's pointer is authoritative** — older blocks are narrative log, not routing. Treat any older `Resume pointer` that names a plan now marked UNIFIED as stale: ignore it when routing, and strike it (`~~…~~` → point at the UNIFIED bullet) the moment you (or a unify pass) notice the mismatch. A stale pointer is a routing instruction to do work that is already done.

### Debt Gate at Session Entry

Before routing, run `python ~/.agents/paul-framework/scripts/debt.py --run-checks` when `.paul/DEBT.toml` exists. This is the scheduler: PAUL has no daemon, so the only moment deferred work gets evaluated is the moment somebody looks.

- An `overdue` row **outranks the loop table**. The one next action is discharging it, or dropping it with a written reason. Report the row id, its title, and the check output that still fails.
- A `scheduled` or `waiting` row is not news. Opening every session with five future dates is how a debt store gets ignored.
- If `--run-checks` reports a row as discharged, offer to set `status = "done"` in the store — a discharge must be a diff, never a silent flip.

### Where Session Context Comes From

Everything session start needs lives in `.paul/`. There is no external store to consult:

- `STATE.md` — loop position, blockers, the `### Decisions` summary table, and every Session-Continuity block. **Only the newest block's Resume pointer is authoritative.**
- `LEARNINGS.md` — the read edge of the improvement loop; `validated` rows are Facts, `candidate` rows matching the plan track are Verification checks.
- `DECISIONS.md` — the full decision record (`D-NN`), with the rationale trail.
- `SPECIAL-FLOWS.md` `## Session Rules` — the always-on behavioral rules (`R-N`).
- `DEBT.toml` — deferred work that carries its own check; `scripts/debt.py` evaluates it.
- A handoff file, when one exists.

These supplement (not replace) each other. A claim in `STATE.md` is a claim; the other three are the corrected record.

## Application

1. Verify `.paul/` exists. Detect handoff files (given path or most recent); load STATE.md. Load `.paul/LEARNINGS.md` when it exists — it is the read edge of the improvement loop and the one artifact `paul-plan` is required to inherit. Load `.paul/DECISIONS.md` and `## Session Rules` in `.paul/SPECIAL-FLOWS.md` when they exist — they are the decision store and the rule store. A checkpoint that is paused and still open should be named in `STATE.md`'s Session-Continuity block; surface it as DUE NOW from there.
1.5. Run `python ~/.agents/paul-framework/scripts/debt.py --run-checks` when `.paul/DEBT.toml` exists, and hold its result. An `overdue` row owned by the user is the next action; an overdue row owned by `agent` is work you do before routing. Do not silently flip a discharged row to `done` — offer it.
2. Follow `resume-project.md`: present handoff content if detected, reconcile handoff vs STATE.md, determine ONE next action from loop position, display resume status.

   **Read the hold before you route.** `loop.position` alone cannot distinguish "APPLY started" from "APPLY finished" — a plan whose evidence waits on a calendar stays APPLYING with every task attempted. Consult `loop.hold_until` / `loop.hold_reason` in `.paul/paul.toml`: a future date means the one next action is **wait**, not unify; a past date means run the plan's exit verification and then unify. Treat prose in STATE.md that describes a wait as a claim, and the toml keys as the routable fact — prose is what let a held plan read as ready to close.
3. **Verify the restored state against the live system before routing.** STATE.md and a handoff are *claims*, not facts: another session, a sibling worktree, a cron job, or a deploy may have changed the database, the branch, or the running processes since they were written. Probe the surfaces they describe — the process/port, one representative endpoint, the rows or schema they assert — and reconcile. A live state that disagrees with STATE.md outranks STATE.md: report the discrepancy and route on what is actually true.
3. pstack is present when `.paul/pstack-models.md` or the global `~/.agents/pstack-models.md` exists, or the `poteto-mode` skill is invocable in this session. If present, run the poteto-mode **session-pickup** playbook to take over any in-flight delegated work, and the `recall` skill to rebuild recent context from chat history and the shared record before acting on the ONE next action.
3. After work proceeds, archive/delete the consumed handoff.
4. Verify success criteria:
   - [ ] Context restored from STATE.md and/or handoff
   - [ ] Loop position correctly identified
   - [ ] Debt store evaluated (`debt.py --run-checks`) when `.paul/DEBT.toml` exists
   - [ ] Exactly ONE next action suggested
   - [ ] User can proceed or redirect with context

## Examples

### Example: New Session

Input: none — most recent handoff auto-detected.

Result: restored context with a single routed next action.

## Common Pitfalls

- **Listing options instead of routing.** Consequence: cold-start drift. Fix: exactly one action.

## References

- `~/.agents/paul-framework/workflows/resume-project.md`
- `.paul/STATE.md`
