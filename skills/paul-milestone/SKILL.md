---
name: paul-milestone
description: Create a new milestone with phases. Use when starting a milestone cycle.
metadata:
  opencode/slash: "true"
---

## Purpose

Create a new milestone with defined scope and phases. Groups phases under the milestone in ROADMAP.md and records it in MILESTONES.md and STATE.md.

Use it when starting a new milestone cycle after completing the previous one.

## Input

Bring the milestone idea:

- **Works best with:** a milestone name (e.g. `v2.0 API Redesign`)
- **Also useful:** scope notes or phase sketches

Zero input is fine; the guided flow defines scope conversationally.

Example: `Use paul-milestone: start v2.0 API Redesign`

## Key Concepts

### Framework Source of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, read the same subpaths under `~/.agents/paul-framework/`. If neither exists, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/create-milestone.md` — workflow to follow

### Project Context

- `.paul/PROJECT.md`, `.paul/STATE.md`, `.paul/ROADMAP.md`

## Application

1. Load PROJECT.md, STATE.md, and ROADMAP.md.
2. Follow `create-milestone.md`: guide through milestone definition, create the phase structure, update ROADMAP.md with milestone grouping.
3. Verify success criteria:
   - [ ] Milestone created in MILESTONES.md
   - [ ] ROADMAP.md updated with milestone grouping
   - [ ] STATE.md reflects new milestone

## Examples

### Example: New Milestone

Input: `v2.0 API Redesign`

Result: milestone recorded, phases grouped under it in the roadmap.

## Common Pitfalls

- **Starting a milestone while the previous one is open.** Consequence: overlapping milestones blur progress. Fix: complete-milestone first.

## References

- `~/.agents/paul-framework/workflows/create-milestone.md`
- `.paul/PROJECT.md`, `.paul/STATE.md`, `.paul/ROADMAP.md`
