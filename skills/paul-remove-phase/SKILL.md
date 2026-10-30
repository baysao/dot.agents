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

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, read the same subpaths under `~/.agents/paul-framework/`. If neither exists, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/roadmap-management.md` — execute the **remove-phase** operation

### Guard

Never remove completed or in-progress phases. Only future (not started) phases qualify.

## Application

1. Load PROJECT.md, STATE.md, and ROADMAP.md.
2. Validate the phase is future/not-started; refuse completed or in-progress targets.
3. Follow `roadmap-management.md`, executing the **remove-phase** operation: remove from ROADMAP.md, clean up the directory if empty, renumber subsequent phases, update STATE.md.
4. Verify success criteria:
   - [ ] Phase removed from ROADMAP.md
   - [ ] Phase directory cleaned up (if empty)
   - [ ] Subsequent phases renumbered
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
