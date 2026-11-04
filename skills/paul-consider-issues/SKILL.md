---
name: paul-consider-issues
description: Review the deferred-debt store against reality. Use before milestone completion, at phase exit, or when the store has accumulated.
metadata:
  opencode/slash: "true"
---

## Purpose

Run the deferred store's own checks and route what survives. Each `.paul/DEBT.toml` row carries a runnable `check`; a row whose check passes is **discharged**, not "reviewed". What remains is categorized as urgent, natural-fit, or can-wait with reasoning.

Use it before milestone completion, at phase exit, or when the store has piled up. There is no cron: this command *is* the review.

## Input

No input required:

- **Works best with:** zero input — it finds all issue files itself
- **Also useful:** a source hint if triaging a subset

Example: `Use paul-consider-issues: triage open issues`

## Key Concepts

### Framework Source of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/consider-issues.md` — workflow to follow
- `~/.agents/paul-framework/scripts/debt.py` — the evaluator (runs every row's check)
- `~/.agents/paul-framework/templates/DEBT.toml.md` — store schema

### The Store Is the Review

`python ~/.agents/paul-framework/scripts/debt.py --run-checks` computes each row's state. Never re-judge a row by reading its title: the check is the verdict. Only rows that survive need human categorization.

- `overdue` — the date passed and the check still fails. Highest priority.
- `scheduled` — the date has not arrived. Not news; leave it.
- `waiting` — gated on an event (`mxv-reply`, `first-commit`). Not news.
- `open` — blocking-only, no date. Read it and decide.

### Legacy Sources

`.paul/ISSUES.md` (if it exists) still holds enhancements with **no landing condition** — a nice-to-have that nobody can turn into a check. It is read after the store, never instead of it. Phase-scoped UAT files (`UAT-NNN`) should already have been mirrored into `kind = "uat"` rows; a UAT issue with no row is a missing write, so add the row rather than only triaging the prose.

## Application

1. Run `python ~/.agents/paul-framework/scripts/debt.py --run-checks`. This single run is the review.
2. For each row the run reports `done`, set `status = "done"` in `.paul/DEBT.toml` — a discharge must be a diff, never a silent flip. Never delete the row.
3. Categorize the surviving rows (urgent / natural fit / can wait) and say why, citing the failing check output.
4. Read `.paul/ISSUES.md` (if present) and any UAT issues lacking a `[[debt]]` row; propose a row for each with a real check.
5. Offer actions: discharge, drop with a written reason, insert a decimal phase, or note for the next plan. Apply only what the user chooses.
6. Report the pile-up count. More than 12 open non-blocking rows means the next PLAN must schedule one.
7. Verify success criteria:
   - [ ] `debt.py --run-checks` executed this session
   - [ ] Every discharged row has `status = "done"` in the store
   - [ ] Surviving rows categorized with reasoning tied to a failing check
   - [ ] UAT/ISSUES items with a testable condition proposed as rows
   - [ ] Actions applied only as directed
   - [ ] Pile-up count reported

## Examples

### Example: Phase-Exit Triage

Input: none.

Result: `debt.py --run-checks` discharges what is done, and the surviving rows are categorized with the failing check quoted.

## Common Pitfalls

- **Categorizing without running the checks.** Consequence: a discharged row lingers and a tested claim is replaced by an opinion. Fix: run `debt.py --run-checks` first; the check is the verdict.
- **Flipping `status` in the store without a diff.** Consequence: the discharge has no artifact and the next session cannot tell it happened. Fix: the TOML edit is the discharge record — commit it.
- **Deleting a row instead of dropping it.** Consequence: the reason it was abandoned disappears. Fix: `status = "dropped"` plus a note.

## References

- `~/.agents/paul-framework/workflows/consider-issues.md`
- `~/.agents/paul-framework/scripts/debt.py`
- `~/.agents/paul-framework/templates/DEBT.toml.md`
- `.paul/DEBT.toml`, `.paul/ISSUES.md`, `.paul/STATE.md`, `.paul/ROADMAP.md`
