---
name: paul:add-plan
description: Add a new plan into an existing phase
argument-hint: "<phase-number-or-name>"
allowed-tools: [Read, Write, Glob, Bash, AskUserQuestion]
---

<objective>
Add a new plan into phase PHASE — an additional PLAN.md appended to an existing phase directory.

**When to use:** Scope expansion within a phase, splitting leftover work, adding follow-up work to a completed phase, or explicitly sequencing another plan without auto-detecting the next phase.

**Distinction from /paul:plan:**
- `/paul:plan [phase]` — auto-detects next incomplete phase, routes scope, creates next plan
- `/paul:add-plan <phase>` — targets an explicit phase, computes next plan number in that phase, creates the plan there
</objective>

<execution_context>
@~/.claude/paul-framework/workflows/add-plan.md
@~/.claude/paul-framework/templates/PLAN.md
@~/.claude/paul-framework/references/plan-format.md
</execution_context>

<context>
Phase: $ARGUMENTS (required — phase number or name, e.g., "4", "04", "04-api-layer")

@.paul/PROJECT.md
@.paul/STATE.md
@.paul/ROADMAP.md
</context>

<process>
Follow workflow: @~/.claude/paul-framework/workflows/add-plan.md
</process>

<success_criteria>
- [ ] Target phase validated against ROADMAP.md
- [ ] Next plan number computed without collision
- [ ] PLAN.md created at `.paul/phases/{NN}-{slug}/{NN}-{PP}-PLAN.md`
- [ ] Plan follows plan-format (frontmatter + required sections per track)
- [ ] ROADMAP.md phase status updated (including Complete → In progress reopen)
- [ ] STATE.md updated with loop position and resume pointer
</success_criteria>
