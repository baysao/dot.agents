---
name: paul-status
description: Deprecated loop-position display. Use paul-progress instead for routed status.
metadata:
  opencode/slash: "true"
---

## Purpose

Display current loop position (PLAN/APPLY/UNIFY) and phase progress.

Deprecated: use `paul-progress` instead — it provides the same information plus visual milestone progress, single-action routing, and an optional context argument.

## Input

No input required. Reads `.paul/STATE.md` and `.paul/ROADMAP.md`.

Example: `Use paul-progress instead of paul-status.`

## Key Concepts

### Sources

`.paul/STATE.md` (milestone, phase X of Y, plan status, loop position, last activity) and `.paul/ROADMAP.md`.

### Loop Suggestion Map

PLAN needed → run plan. PLAN ready → approve then apply. APPLY complete → unify. UNIFY complete → loop closed, ready for next phase.

## Application

1. Read STATE.md: extract milestone, phase, plan status, loop position, last activity.
2. Display the status block (milestone, phase, plan, loop diagram, last, next).
3. Suggest the next action per the loop map.
4. Verify success criteria:
   - [ ] Loop position displayed clearly
   - [ ] Phase progress shown
   - [ ] Next action suggested

## Examples

### Example: Legacy Check

Input: none.

Result: status block. For routing, prefer `paul-progress`.

## Common Pitfalls

- **Using this for routing.** Consequence: weaker guidance than progress. Fix: default to `paul-progress`.

## References

- `.paul/STATE.md`, `.paul/ROADMAP.md`
