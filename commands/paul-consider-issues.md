---
name: paul:consider-issues
description: Review debt rows and deferred issues with codebase context, triage and route
allowed-tools: [Read, Bash, Grep, Glob, Edit, AskUserQuestion]
---

<objective>
Review open debt from `.paul/DEBT.toml` (each row carries a runnable check) plus any legacy ISSUES.md entries and phase-scoped UAT files. Identify resolved, urgent, and waiting items. Prevents debt pile-up.

**When to use:** Periodically or before milestone completion.
</objective>

<execution_context>
@~/.agents/paul-framework/workflows/consider-issues.md
</execution_context>

<context>
@.paul/DEBT.toml (if exists)
@.paul/ISSUES.md (legacy, if exists)
@.paul/STATE.md
@.paul/ROADMAP.md
</context>

<process>
**Follow workflow: @~/.agents/paul-framework/workflows/consider-issues.md**

The workflow implements:
1. Run the debt store (`scripts/debt.py --run-checks`); it is the primary source
2. Find other issue files (legacy ISSUES.md, phase-scoped UAT files)
3. Parse open rows (DEBT-NNN, ISS-NNN, UAT-NNN format)
4. Analyze each against codebase (resolved? urgent? natural-fit?)
5. Present categorized report with computed debt counts
6. Offer actions (close resolved, insert urgent, note for planning)
7. Update files as needed — setting `status = "done"` is the discharge
</process>

<success_criteria>
- [ ] Debt checks run; rows that pass are discharged by editing `status`
- [ ] All open issues analyzed against current codebase
- [ ] Each issue categorized (resolved/urgent/natural-fit/can-wait)
- [ ] Clear reasoning provided for each categorization
- [ ] Actions offered based on findings
- [ ] Files updated if user takes action
</success_criteria>
