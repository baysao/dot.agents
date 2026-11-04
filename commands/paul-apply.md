---
name: paul:apply
description: Execute an approved PLAN
argument-hint: "[plan-path]"
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion]
---

<objective>
Execute an approved PLAN.md file, handling checkpoints as they occur.

**When to use:** After PLAN phase complete and plan is approved.

Executes tasks in sequence, pauses at checkpoints for user input, reports completion.
</objective>

<execution_context>
@~/.agents/paul-framework/workflows/apply-phase.md
@~/.agents/paul-framework/references/checkpoints.md
</execution_context>

<context>
Plan path: $ARGUMENTS

@.paul/STATE.md
</context>

<process>

<step name="validate_plan">
1. Confirm plan file exists at $ARGUMENTS path
2. Error if not found: "Plan not found: {path}"
3. Derive SUMMARY path (replace PLAN.md with SUMMARY.md)
4. If SUMMARY exists: "Plan already executed. SUMMARY: {path}"
   - Offer: re-execute or exit
</step>

<step name="execute">
Follow workflow: @~/.agents/paul-framework/workflows/apply-phase.md

Before the first task, run `python ~/.agents/paul-framework/scripts/debt.py --run-checks`. An `overdue` row with `blocking = "phase-NN-exit"` gates this phase shut; discharge it in this plan or say the phase cannot close.

Execute tasks sequentially. For each task:
- Read task definition
- Execute action
- Run verification
- Confirm done criteria

A deviation that is a deferral (a skipped task, a shortcut, a nice-to-have noticed) becomes a `[[debt]]` row in `.paul/DEBT.toml` with a runnable check — not a SUMMARY prose line, and not `.paul/ISSUES.md` unless no testable landing condition exists. `debt.py` rejects a row with no `due`, `trigger`, or `blocking`.
</step>

<step name="handle_checkpoints">
When a checkpoint task is reached:

**checkpoint:decision**
- Present decision context and options
- Wait for user selection
- Record decision
- Continue execution

**checkpoint:human-verify**
- Present what was built
- Present verification steps
- Wait for "approved" or issue description
- If issues: address and re-verify
- Continue execution

**checkpoint:human-action**
- Present required action
- Wait for "done" confirmation
- Continue execution
</step>

<step name="complete">
After all tasks complete:
- If a task ended in a calendar wait: report "APPLY held until [date] — [reason]. Do not unify yet." and set `loop.hold_until` / `loop.hold_reason` in `paul.toml`.
- Otherwise report: "APPLY complete. Run /paul:unify to close loop."
- Show files modified
- Show SUMMARY path to create
</step>

</process>

<success_criteria>
- [ ] Debt gate run before the first task; no `overdue` blocking row left unaddressed
- [ ] All tasks executed
- [ ] All checkpoints handled (a paused human checkpoint becomes a debt row **and** a STATE DUE NOW line)
- [ ] Every deferral became a debt row with a runnable check
- [ ] User informed of completion
- [ ] Next action clear (run /paul:unify)
</success_criteria>
