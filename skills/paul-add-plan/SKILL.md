---
name: paul-add-plan
description: Add an explicit plan into an existing phase. Use to expand phase scope or split leftover work.
metadata:
  opencode/slash: "true"
---

## Purpose

Add a new plan into an explicit phase — an additional `PLAN.md` appended to an existing phase directory with the next collision-free plan number.

Use it for scope expansion within a phase, splitting leftover work, follow-up work on a completed phase, or explicitly sequencing another plan without auto-detecting the next phase.

Distinction from plan: `paul-plan` auto-detects the next incomplete phase and routes scope; `paul-add-plan` targets an explicit phase and computes the next plan number there.

## Input

Bring the target phase (required):

- **Works best with:** a phase number or name (e.g. `4`, `04`, `04-api-layer`)
- **Also useful:** the extra scope the plan should cover

Example: `Use paul-add-plan: add a plan to 04-api-layer for rate limiting`

## Key Concepts

### Framework Sources of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, read the same subpaths under `~/.agents/paul-framework/`. If neither exists, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/add-plan.md` — workflow to follow
- `~/.agents/paul-framework/templates/PLAN.md` — plan template
- `~/.agents/paul-framework/references/plan-format.md` — format reference (frontmatter + per-track sections)

### Output Path

`.paul/phases/{NN}-{slug}/{NN}-{PP}-PLAN.md` with the next plan number computed without collision.

## Application

1. Validate the target phase against ROADMAP.md; error with the incomplete-phase list if missing.
2. Follow `add-plan.md`: compute the next plan number, draft the plan per plan-format.
3. Write the PLAN.md to the output path.
4. Update ROADMAP.md phase status (including reopening Complete → In progress) and STATE.md loop position + resume pointer.
5. Verify success criteria:
   - [ ] Target phase validated
   - [ ] Next plan number collision-free
   - [ ] PLAN.md created at the correct path per plan-format
   - [ ] ROADMAP.md and STATE.md updated

## Examples

### Example: Follow-up Plan

Input: phase `04-api-layer`, scope `rate limiting`

Result: `.paul/phases/04-api-layer/04-03-PLAN.md` created, phase reopened in ROADMAP.md if needed.

## Common Pitfalls

- **Guessing the plan number.** Consequence: file collision or ordering gaps. Fix: always compute next number from the phase directory.
- **Forgetting the reopen.** Consequence: completed phase hides new work. Fix: flip Complete → In progress when appending.

## References

- `~/.agents/paul-framework/workflows/add-plan.md`
- `~/.agents/paul-framework/templates/PLAN.md`
- `~/.agents/paul-framework/references/plan-format.md`
- `.paul/PROJECT.md`, `.paul/STATE.md`, `.paul/ROADMAP.md`
