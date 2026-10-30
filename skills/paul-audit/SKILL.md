---
name: paul-audit
description: Run an enterprise audit on a plan and auto-apply findings. Use after PLAN, before APPLY.
metadata:
  opencode/slash: "true"
---

## Purpose

Run a senior principal engineer + compliance review audit on the current `PLAN.md`. Automatically applies must-have and strongly-recommended findings, and produces an `AUDIT.md` report in the same phase directory.

Use it after PLAN completes, before APPLY. Runs only when explicitly invoked or suggested by the `enterprise_plan_audit` config.

## Input

Optionally bring the plan path:

- **Works best with:** a plan path — otherwise the current plan from `.paul/STATE.md` + `.paul/config.md`
- **Also useful:** nothing else

Example: `Use paul-audit: .paul/phases/20-ai-schema/20-01-PLAN.md`

## Key Concepts

### Framework Source of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, read the same subpaths under `~/.agents/paul-framework/`. If neither exists, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/audit-plan.md` — workflow to follow

### Finding Classes

must-have and strongly-recommended findings are auto-applied to PLAN.md; can-safely-defer findings are reported only.

### Anti-Patterns

No invented requirements, no "future phases will fix it", no unjustified "fine for v1", correctness over politeness, never skip applying findings.

## Application

1. Follow `audit-plan.md`: validate preconditions (PLAN exists, loop at PLAN complete); load and parse PLAN.md.
2. Execute the 6-section structured review; classify findings; auto-apply must-have + strongly-recommended to PLAN.md.
3. Create `AUDIT.md` in the phase directory; update STATE.md; present summary and route to APPLY.

### pstack Adversarial Panel (automatic)

pstack is present when `.paul/pstack-models.md` or the global `~/.agents/pstack-models.md` exists, or the `poteto-mode` skill is invocable in this session. If present, run the `interrogate` skill on the PLAN before classifying findings: multiple models try to break the plan, including a strict code-quality lens. Fold its verdicts into the finding classes. For small-looking changes with wide reach, also run `blast-radius` so the audit carries a proven safety fact, not an assertion.
4. Verify success criteria:
   - [ ] PLAN.md audited against enterprise standards
   - [ ] Must-have and strongly-recommended findings applied
   - [ ] AUDIT.md report created in phase directory
   - [ ] STATE.md updated to reflect audit completion
   - [ ] User presented with next action (run APPLY)

## Examples

### Example: Pre-Apply Audit

Input: `.paul/phases/20-ai-schema/20-01-PLAN.md`

Result: remediated plan + AUDIT.md report, routed to apply.

## Common Pitfalls

- **Report-only auditing.** Consequence: findings never land. Fix: auto-apply is the point — always write findings back into the plan.

## References

- `~/.agents/paul-framework/workflows/audit-plan.md`
- `.paul/STATE.md`, `.paul/config.md`
