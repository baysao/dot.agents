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

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/discuss-milestone.md` — workflow to follow

### Project Context

- `.paul/PROJECT.md`, `.paul/STATE.md`, `.paul/ROADMAP.md`, `.paul/MILESTONES.md`
- `.paul/DEBT.toml` — the backlog the last milestone left behind, which is often the honest input to "what should the next one be"

## Application

1. Load PROJECT.md, STATE.md, ROADMAP.md, and MILESTONES.md.
2. Run `python ~/.agents/paul-framework/scripts/debt.py --run-checks`. Group surviving rows by theme and use them as raw material: a cluster of unowned `decision` rows is a milestone theme nobody planned; ten `artifact` rows is a "land what we built" milestone. The store is a better predictor of the needed work than a brainstorm.
3. Follow `discuss-milestone.md`: conversational exploration of themes and goals.
4. Write `MILESTONE-CONTEXT.md` with the articulated vision and a `## Inherited debt` list of row ids the milestone must absorb or explicitly abandon.
5. Verify success criteria:
   - [ ] MILESTONE-CONTEXT.md created with vision
   - [ ] Key themes and goals articulated
   - [ ] Debt store reviewed; inherited rows named (absorbed or abandoned with a reason)
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
