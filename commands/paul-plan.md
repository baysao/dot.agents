---
name: paul:plan
description: Enter PLAN phase for current or new plan
argument-hint: "[phase-plan]"
allowed-tools: [Read, Write, Glob, AskUserQuestion]
---

<objective>
Create or continue a PLAN for the specified phase.

**When to use:** Starting new work or resuming incomplete plan.
</objective>

<execution_context>
@~/.agents/paul-framework/workflows/plan-phase.md
@~/.agents/paul-framework/templates/PLAN.md
@~/.agents/paul-framework/references/plan-format.md
</execution_context>

<context>
$ARGUMENTS

@.paul/PROJECT.md
@.paul/STATE.md
@.paul/ROADMAP.md
</context>

<process>
Follow workflow: @~/.agents/paul-framework/workflows/plan-phase.md

Before drafting, run `python ~/.agents/paul-framework/scripts/debt.py --run-checks`. Every `overdue` row, every `open` row, and every `waiting` row whose trigger names this phase must become an acceptance criterion or be named out-of-scope with a reason. Silent omission is a plan defect.
</process>

<success_criteria>
- [ ] PLAN.md created in correct phase directory
- [ ] All acceptance criteria defined
- [ ] Debt rows touching this phase scheduled or named out-of-scope
- [ ] STATE.md updated with loop position
</success_criteria>
