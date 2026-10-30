---
name: paul-assumptions
description: Surface planning assumptions for a phase before planning. Use to catch misconceptions early.
metadata:
  opencode/slash: "true"
---

## Purpose

Surface the planner's assumptions about a phase to validate understanding before planning. Presents assumptions across 5 areas with confidence levels so the user can correct them.

Use it before planning to catch misconceptions early.

Distinction from discuss: assumptions shows what the agent thinks; discuss gathers what the user wants.

## Input

Bring the phase (required):

- **Works best with:** a phase number (e.g. `3`)

Example: `Use paul-assumptions: check phase 3`

## Key Concepts

### Framework Source of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, read the same subpaths under `~/.agents/paul-framework/`. If neither exists, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/phase-assumptions.md` — workflow to follow

### Project Context

- `.paul/PROJECT.md`, `.paul/STATE.md`, `.paul/ROADMAP.md`

## Application

1. Resolve and validate the phase number; error if missing.
2. Follow `phase-assumptions.md`: present assumptions across 5 areas with confidence levels.
3. Collect user corrections and note the path to planning.
4. Verify success criteria:
   - [ ] Assumptions presented across 5 areas
   - [ ] Confidence levels indicated
   - [ ] User can provide corrections
   - [ ] Clear path to planning after validation

## Examples

### Example: Pre-Plan Check

Input: `3`

Result: assumption review with confidence levels, corrections captured before planning.

## Common Pitfalls

- **Treating assumptions as decisions.** Consequence: unvalidated guesses harden into plan scope. Fix: require explicit user validation.

## References

- `~/.agents/paul-framework/workflows/phase-assumptions.md`
- `.paul/PROJECT.md`, `.paul/STATE.md`, `.paul/ROADMAP.md`
