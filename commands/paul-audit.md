---
name: paul:audit
description: Run enterprise architectural audit or security audit on current plan
argument-hint: "[plan-path] [--security]"
allowed-tools: [Read, Write, Edit, Glob, AskUserQuestion]
---

<objective>
Audit the current PLAN.md before APPLY. Two modes:

- **Architectural** (default): senior principal engineer + compliance review.
  Must-have and strongly-recommended findings are auto-applied to the plan.
  Report saved as `{NN}-{PP}-AUDIT.md` in the phase directory.
- **Security**: routes to the `/paul:security` workflow scoped to this plan's diff.
  Findings become debt rows, not plan edits.

**When to use:** After PLAN phase complete, before APPLY.
**Optional:** Only runs when explicitly invoked or suggested by `enterprise_plan_audit` / `security_audit` config.
</objective>

<execution_context>
@~/.agents/paul-framework/workflows/audit-plan.md
</execution_context>

<context>
Plan path: $ARGUMENTS

@.paul/STATE.md
@.paul/config.md
</context>

<process>
**Follow workflow: @~/.agents/paul-framework/workflows/audit-plan.md**

The workflow implements:
1. Validate preconditions (PLAN exists, loop at PLAN complete)
2. Load and parse the PLAN.md
3. Choose audit mode — architectural (this workflow) or security (`security_audit` config; routes to `/paul:security` with this plan as scope). `--security` skips the prompt.
4. Run `python ~/.agents/paul-framework/scripts/debt.py --run-checks`; a debt row the plan neither schedules nor names out-of-scope is a must-have finding
5. Execute enterprise audit (6-section structured review)
6. Classify findings (must-have, strongly-recommended, can-safely-defer)
7. Auto-apply must-have and strongly-recommended findings to PLAN.md
8. Create AUDIT.md report in phase directory
9. Update STATE.md with audit completion
10. Present summary and route to APPLY
</process>

<success_criteria>
- [ ] Audit mode chosen (architectural / security / both) when both toggles are enabled
- [ ] PLAN.md audited against enterprise standards
- [ ] Debt coverage checked; uncovered overdue rows raised as must-have findings
- [ ] Must-have and strongly-recommended findings applied to PLAN.md
- [ ] AUDIT.md report created in phase directory
- [ ] STATE.md updated to reflect audit completion
- [ ] User presented with next action (run APPLY)
</success_criteria>

<anti_patterns>
- Don't invent requirements not implied by the plan
- Don't assume "future phases" will fix gaps
- Don't say "this is fine for v1" unless justified
- Don't optimize for politeness over correctness
- Don't skip applying findings - the whole point is automatic remediation
</anti_patterns>
