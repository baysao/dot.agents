---
name: paul-remove-phase
description: Remove a future not-started phase from the roadmap. Use for scope reduction.
metadata:
  opencode/slash: "true"
---

## Purpose

Remove a future phase from the roadmap and clean up its directory. Renumbers subsequent phases and updates STATE.md.

Use it for scope reduction — only for phases that haven't started.

## Input

Bring the target phase (required):

- **Works best with:** a phase number or name (e.g. `5`, `05-legacy-import`)

If you supply it inline, removal proceeds to validation — otherwise it asks.

Example: `Use paul-remove-phase: drop phase 5`

## Key Concepts

### Framework Source of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/roadmap-management.md` — execute the **remove-phase** operation

### Guard

Never remove completed or in-progress phases. Only future (not started) phases qualify.

### Renumbering Breaks Debt Pointers

Debt rows reference phases by number: `trigger = "phase:05"`, `blocking = "phase-5-exit"`. Removing a phase renumbers everything after it, so those references silently point at the wrong phase — a gate that was meant for phase 6 now blocks phase 5, or blocks nothing at all.

After the renumber, sweep `.paul/DEBT.toml` for `phase:<NN>` and `phase-<NN>-exit` references at or after the removed number and rewrite them to the new numbers. Then:

1. Rows whose phase was **the removed one** are orphans: either retarget them to the phase that now covers that scope, or set `status = "dropped"` with a note naming the removal.
2. Rows pointing **after** the removed phase shift down by one.
3. Run `python ~/.agents/paul-framework/scripts/debt.py` and confirm nothing errors.

## Application

1. Load PROJECT.md, STATE.md, and ROADMAP.md.
2. Validate the phase is future/not-started; refuse completed or in-progress targets.
3. Follow `roadmap-management.md`, executing the **remove-phase** operation: remove from ROADMAP.md, clean up the directory if empty, renumber subsequent phases, update STATE.md.
4. Repair the debt store's phase references (see above).
5. Verify success criteria:
   - [ ] Phase removed from ROADMAP.md
   - [ ] Phase directory cleaned up (if empty)
   - [ ] Subsequent phases renumbered
   - [ ] `DEBT.toml` phase references retargeted or dropped; store parses
   - [ ] STATE.md updated

## Examples

### Example: Drop Future Phase

Input: `5`

Result: phase removed, later phases renumbered, STATE.md consistent.

## Common Pitfalls

- **Removing an active phase.** Consequence: orphaned plans and broken state. Fix: enforce the future-only guard.

## References

- `~/.agents/paul-framework/workflows/roadmap-management.md`
- `.paul/PROJECT.md`, `.paul/STATE.md`, `.paul/ROADMAP.md`
