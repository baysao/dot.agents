---
name: paul-discuss-milestone
description: Explore next milestone vision conversationally. Use before creating a milestone.
metadata:
  opencode/slash: "true"
---

## Purpose

Facilitate vision discussion for the next milestone and create a context handoff (`MILESTONE-CONTEXT.md`).

Use it before creating a new milestone, when scope needs exploration.

## Input

No input required — the conversation surfaces vision:

- **Works best with:** zero input; any hunches about themes or goals help
- **Also useful:** constraints or non-goals for the milestone

Example: `Use paul-discuss-milestone: explore what v2 should be`

## Key Concepts

### Framework Source of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, read the same subpaths under `~/.agents/paul-framework/`. If neither exists, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/discuss-milestone.md` — workflow to follow

### Project Context

- `.paul/PROJECT.md`, `.paul/STATE.md`, `.paul/ROADMAP.md`, `.paul/MILESTONES.md`

## Application

1. Load PROJECT.md, STATE.md, ROADMAP.md, and MILESTONES.md.
2. Follow `discuss-milestone.md`: conversational exploration of themes and goals.
3. Write `MILESTONE-CONTEXT.md` with the articulated vision.
4. Verify success criteria:
   - [ ] MILESTONE-CONTEXT.md created with vision
   - [ ] Key themes and goals articulated
   - [ ] Ready for milestone creation

## Examples

### Example: Milestone Vision

Input: none — guided conversation.

Result: milestone context document ready to feed milestone creation.

## Common Pitfalls

- **Defining phases before vision lands.** Consequence: milestone of disconnected phases. Fix: articulate themes first.

## References

- `~/.agents/paul-framework/workflows/discuss-milestone.md`
- `.paul/PROJECT.md`, `.paul/STATE.md`, `.paul/ROADMAP.md`, `.paul/MILESTONES.md`
