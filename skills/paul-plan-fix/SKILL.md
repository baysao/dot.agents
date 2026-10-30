---
name: paul-plan-fix
description: Create a fix plan from UAT issues. Use after verify logs issues to a UAT file.
metadata:
  opencode/slash: "true"
---

## Purpose

Create a `{plan}-FIX.md` plan from UAT issues found during verify, ready for execution.

Use it after `paul-verify` logs issues to the phase-scoped UAT file.

## Input

Bring the plan number (required):

- **Works best with:** a plan number (e.g. `04-02`, `10-01`)

If missing, it errors with usage and exits — it cannot infer the target.

Example: `Use paul-plan-fix: 04-02`

## Key Concepts

### Framework Sources of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, read the same subpaths under `~/.agents/paul-framework/`. If neither exists, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/references/plan-format.md` — plan structure
- `~/.agents/paul-framework/references/checkpoints.md` — checkpoint semantics

### Sources

Issues come from `.paul/phases/XX-name/{plan}-UAT.md` (created by verify); the original `.paul/phases/XX-name/{plan}-PLAN.md` is reference only. Output is `.paul/phases/XX-name/{plan}-FIX.md` (+ `{plan}-FIX-SUMMARY.md` after execution).

## Application

### Step 1: Parse and Locate

Parse `XX-NN` from input; error with usage if absent. Locate `.paul/phases/*/{plan}-UAT.md`; if missing, report that no fix plan is needed and exit.

### Step 2: Read and Prioritize

Read the UAT file; parse each issue (ID, title, severity, repro, AC ref); count by severity (Blocker → Major → Minor → Cosmetic).

### Step 3: Write FIX.md

One task per issue (group related minors). Each task names the UAT issue, lists affected files, fix action with original AC reference, test, and done criteria. Write the FIX.md with frontmatter (phase, `{plan}-FIX`, type fix), objective, context (STATE, ROADMAP, UAT + original plan refs), generated acceptance criteria, tasks, boundaries (UAT scope only, no creep), and verification checklist.

If an issue class already survived a previous fix cycle (same root cause in an earlier `{plan}-UAT.md` or `{plan}-FIX-SUMMARY.md`), stage a preventive rule with `carl_v2_stage_proposal` (`source: decisions`) and surface it with the Step 4 approval prompt. Approve on yes, archive on no.

### Step 4: Offer Execution

Display the FIX PLAN CREATED block (severity counts) and ask: approved-run-APPLY, review-first, or pause. On approval: apply the FIX.md.

Verify success criteria:
- [ ] UAT.md found and parsed
- [ ] Fix tasks created for each issue (or grouped)
- [ ] FIX.md written with proper PAUL structure
- [ ] User offered to execute or review

## Examples

### Example: UAT Follow-up

Input: `04-02` with 1 blocker + 2 minors in the UAT file.

Result: `.paul/phases/04-…/04-02-FIX.md` with 2–3 prioritized tasks, offered for apply.

## Common Pitfalls

- **Fixing beyond the UAT file.** Consequence: scope creep inside a fix plan. Fix: boundaries restrict to listed issues only.

## References

- `~/.agents/paul-framework/references/plan-format.md`
- `~/.agents/paul-framework/references/checkpoints.md`
- `.paul/STATE.md`, `.paul/ROADMAP.md`
