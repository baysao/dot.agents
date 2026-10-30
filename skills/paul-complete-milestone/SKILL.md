---
name: paul-complete-milestone
description: Archive the current milestone and evolve the project. Use when all phases verify complete.
metadata:
  opencode/slash: "true"
---

## Purpose

Complete the current milestone, archive it, and evolve PROJECT.md. Creates a git tag for the version and updates STATE.md.

Use it when all phases in the current milestone are complete and verified.

## Input

Optionally bring the version:

- **Works best with:** a version (e.g. `v0.3`) — otherwise derived from project state
- **Also useful:** milestone summary notes

Example: `Use paul-complete-milestone: close out v0.3`

## Key Concepts

### Framework Source of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, read the same subpaths under `~/.agents/paul-framework/`. If neither exists, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/complete-milestone.md` — workflow to follow

### Project Context

- `.paul/PROJECT.md`, `.paul/STATE.md`, `.paul/ROADMAP.md`, `.paul/MILESTONES.md`

## Application

1. Load PROJECT.md, STATE.md, ROADMAP.md, and MILESTONES.md.
2. Follow `complete-milestone.md`: verify all phases complete, archive the milestone with summary, evolve PROJECT.md with learnings, create the git tag, update STATE.md.
3. Verify success criteria:
   - [ ] Milestone archived with summary
   - [ ] PROJECT.md evolved with learnings
   - [ ] Git tag created for version
   - [ ] STATE.md updated to reflect completion

## Examples

### Example: Close Milestone

Input: `v0.3`

Result: milestone archived, tag created, project evolved for the next cycle.

## Common Pitfalls

- **Closing with unverified phases.** Consequence: incomplete work gets archived as done. Fix: verify every phase before completing.

## References

- `~/.agents/paul-framework/workflows/complete-milestone.md`
- `.paul/PROJECT.md`, `.paul/STATE.md`, `.paul/ROADMAP.md`, `.paul/MILESTONES.md`
