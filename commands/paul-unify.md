---
name: paul:unify
description: Reconcile plan vs actual and close the loop
argument-hint: "[plan-path]"
allowed-tools: [Read, Write, AskUserQuestion]
---

<objective>
Reconcile plan versus actual results, create SUMMARY.md, and close the loop.

**When to use:** After APPLY phase complete. This is MANDATORY - never skip UNIFY.

Creates SUMMARY.md documenting what was built, decisions made, and any deferred issues.
</objective>

<execution_context>
@~/.agents/paul-framework/workflows/unify-phase.md
@~/.agents/paul-framework/templates/SUMMARY.md
</execution_context>

<context>
Plan path: $ARGUMENTS

@.paul/STATE.md
@{plan-path} (the PLAN.md being unified)
</context>

<process>

<step name="validate_preconditions">
1. Confirm PLAN.md exists at $ARGUMENTS path
2. Confirm APPLY phase was executed (tasks completed)
3. If SUMMARY.md already exists: "Loop already closed. SUMMARY: {path}"
</step>

<step name="reconcile">
Follow workflow: @~/.agents/paul-framework/workflows/unify-phase.md

Compare plan to actual:
- Which tasks completed as planned?
- Any deviations from plan?
- Decisions made during execution?
- Issues discovered but deferred?
</step>

<step name="create_summary">
Create SUMMARY.md in same directory as PLAN.md:
- Document what was built
- Record acceptance criteria results
- Deferred items as `[[debt]]` rows (the table is a generated view of `.paul/DEBT.toml`, never the store)
- Capture decisions made
- List files created/modified
</step>

<step name="update_debt_store">
Run `python ~/.agents/paul-framework/scripts/debt.py --run-checks`, then:
- Rows the run reports `done` → set `status = "done"` in `.paul/DEBT.toml` (the TOML diff is the discharge record; never delete)
- Rows this loop abandoned → `status = "dropped"` plus a `note` saying why
- New deferrals (including every uncommitted artifact) → a row with a check that can fail
- Report `DEBT: N overdue · N waiting · N open · N discharged`; more than 12 open non-blocking means the next PLAN schedules one
</step>

<step name="update_state">
Update STATE.md:
- Loop position: PLAN ✓ → APPLY ✓ → UNIFY ✓
- Phase progress if plan completes phase
- Performance metrics (duration)
- Session continuity (next action)
</step>

<step name="report">
Display:
```
Loop Closed
════════════════════════════════════════

Plan: {plan-path}
Summary: {summary-path}

PLAN ──▶ APPLY ──▶ UNIFY
  ✓        ✓        ✓

Next: [phase complete message or next plan]

════════════════════════════════════════
```
</step>

</process>

<success_criteria>
- [ ] SUMMARY.md created
- [ ] `.paul/DEBT.toml` synced: discharged rows flipped, abandoned rows dropped with a reason, new deferrals appended
- [ ] Debt counts reported
- [ ] STATE.md updated with loop closure
- [ ] User knows next action
</success_criteria>
