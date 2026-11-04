---
name: paul:resume
description: Restore context from handoff and continue work
argument-hint: "[optional: handoff path, e.g., '.paul/HANDOFF-phase10-audit.md']"
allowed-tools: [Read, Glob, Bash]
---

<objective>
Restore PAUL context after a session break, determine current position, and suggest exactly ONE next action.

**When to use:** Starting a new session on an existing PAUL project.

**Handoff lifecycle:** Detects handoffs, presents content, archives after work proceeds.
</objective>

<execution_context>
@~/.agents/paul-framework/workflows/resume-project.md
</execution_context>

<context>
$ARGUMENTS (optional handoff path)

@.paul/STATE.md
</context>

<process>
**Follow workflow: @~/.agents/paul-framework/workflows/resume-project.md**

The workflow implements:
1. Verify .paul/ exists
2. Detect handoff files (use $ARGUMENTS if provided, else find most recent)
3. Load STATE.md
4. **Run `python ~/.agents/paul-framework/scripts/debt.py --run-checks`** when `.paul/DEBT.toml` exists. An `overdue` row outranks the loop table: report the row id, its title, and the failing check, and make discharging it the next action. `scheduled` and `waiting` rows are not reported; only a passed date is news.
5. Present handoff content if detected
6. Reconcile handoff vs STATE.md
7. Determine exactly ONE next action based on loop position
8. Display resume status with single routing
9. After work proceeds: archive/delete consumed handoff

**Key behavior:** Suggest exactly ONE next action, not multiple options.

**Handoff pattern:** `.paul/HANDOFF-{context}.md` (e.g., `HANDOFF-phase10-audit.md`)
</process>

<success_criteria>
- [ ] Context restored from STATE.md and/or handoff
- [ ] Loop position correctly identified
- [ ] Debt store evaluated; overdue rows surfaced (or confirmed absent)
- [ ] Exactly ONE next action suggested (not multiple options)
- [ ] User can proceed or redirect with context
</success_criteria>
