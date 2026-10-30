---
name: paul-add-phase
description: Append a new phase to the current milestone roadmap. Use for planned scope expansion.
metadata:
  opencode/slash: "true"
---

## Purpose

Add a new phase to the current milestone's roadmap. Updates ROADMAP.md, creates the phase directory, and records the new phase in STATE.md.

Use it for scope expansion during a milestone when adding planned work.

## Input

Bring the phase idea:

- **Works best with:** a phase name (e.g. `API Authentication Layer`)
- **Also useful:** placement or scope notes if not simply appending

If you supply the name inline, it proceeds — otherwise it asks. Zero input is fine; the guided flow covers it.

Example: `Use paul-add-phase: add API Authentication Layer`

## Key Concepts

### Framework Source of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, read the same subpaths under `~/.agents/paul-framework/`. If neither exists, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/roadmap-management.md` — execute the **add-phase** operation

### Project Context

- `.paul/PROJECT.md`, `.paul/STATE.md`, `.paul/ROADMAP.md`

## Application

1. Load PROJECT.md, STATE.md, and ROADMAP.md.
2. Follow `roadmap-management.md`, executing the **add-phase** operation for the named phase.
3. Verify success criteria:
   - [ ] Phase added to ROADMAP.md
   - [ ] Phase directory created
   - [ ] STATE.md updated with new phase

## Examples

### Example: Append Phase

Input: `API Authentication Layer`

Result: phase appended to ROADMAP.md, directory created, STATE.md updated.

## Common Pitfalls

- **Adding a phase that duplicates existing scope.** Consequence: overlapping plans and confused routing. Fix: check ROADMAP.md for overlap before adding.

## References

- `~/.agents/paul-framework/workflows/roadmap-management.md`
- `.paul/PROJECT.md`, `.paul/STATE.md`, `.paul/ROADMAP.md`
