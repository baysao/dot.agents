---
name: paul-consider-issues
description: Triage deferred issues against current codebase. Use periodically or before milestone completion.
metadata:
  opencode/slash: "true"
---

## Purpose

Review all open issues from `ISSUES.md` and phase-scoped UAT files with current codebase context. Categorizes each as resolved, urgent, natural-fit, or can-wait, and routes them — preventing issue pile-up.

Use it periodically or before milestone completion.

## Input

No input required:

- **Works best with:** zero input — it finds all issue files itself
- **Also useful:** a source hint if triaging a subset

Example: `Use paul-consider-issues: triage open issues`

## Key Concepts

### Framework Source of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, read the same subpaths under `~/.agents/paul-framework/`. If neither exists, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/consider-issues.md` — workflow to follow

### Issue Sources

- `.paul/ISSUES.md` (if exists), phase-scoped UAT files (`UAT-NNN`), `ISS-NNN` entries
- `.paul/STATE.md`, `.paul/ROADMAP.md` for position and priority context

## Application

1. Find all issue files (ISSUES.md, phase-scoped UAT files).
2. Parse open issues and analyze each against the codebase: resolved, urgent, natural-fit, or can-wait, with reasoning.
3. Present the categorized report and offer actions (close resolved, insert urgent, note for planning); update files as the user directs.
4. Verify success criteria:
   - [ ] All open issues analyzed against current codebase
   - [ ] Each issue categorized with reasoning
   - [ ] Actions offered based on findings
   - [ ] Files updated if user takes action

## Examples

### Example: Pre-Milestone Triage

Input: none.

Result: categorized report; resolved issues closed, urgent ones routed into work.

## Common Pitfalls

- **Categorizing without codebase evidence.** Consequence: stale resolved issues linger. Fix: check each issue against current code.

## References

- `~/.agents/paul-framework/workflows/consider-issues.md`
- `.paul/ISSUES.md`, `.paul/STATE.md`, `.paul/ROADMAP.md`
