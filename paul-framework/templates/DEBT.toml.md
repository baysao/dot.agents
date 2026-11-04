# DEBT.toml Template

Template for `.paul/DEBT.toml` — the project's debt store, evaluated at the PAUL gates.

**Purpose:** Holds every deferred item that is not a task in the current plan: an artifact that has to land later, a decision only the owner can make, a check that must re-run after a window closes, a UAT finding parked on purpose. Each row carries a **machine-runnable check**, so "is this done?" is answered by the repository, not by memory.

**Location:** `.paul/DEBT.toml` (project-level, not phase-level)

**Evaluator:** `python ~/.agents/paul-framework/scripts/debt.py`

---

## Why a store instead of prose

Deferred work used to live in three places that could not see each other: a `### Deferred Issues` table in STATE.md, free-text `## Carried forward` / `## Artifact-debt inventory` tables in each SUMMARY.md, and bullets in a resume note. Nothing said *when* to look, so nothing was looked at — and an item whose evidence decomposed was re-derived from scratch three sessions later.

A debt row is a claim with a test. **A row that cannot be tested is not debt, it is a wish**, and `debt.py` rejects it at load time.

---

## File Template

```toml
# .paul/DEBT.toml — the debt store for this project.
#
# A SET with state, not a log: a row is edited in place, so every discharge is a
# diff. Contrast `.paul/ledger.toml`, which is append-only.
#
# Written by: apply-phase deviation #5, unify-phase `## Carried forward` /
#             `## Artifact-debt inventory`, verify-work UAT findings.
# Read by:    scripts/debt.py at the gates PAUL already passes — session entry,
#             plan drafting, phase exit.
#
# status: open | done | dropped     (overdue/scheduled/waiting are COMPUTED)

[[debt]]
id = "DEBT-001"
title = "Dispatch the legal request; record recipient and send date"
kind = "decision"                 # artifact | reopen | decision | tech | uat
origin = "00-01 AC-3"
owner = "owner"                   # owner | agent | phase-NN | vendor
blocking = "phase-0-exit"         # omit when it blocks nothing
due = "2026-11-05T00:00:00Z"      # omit when unschedulable by date
check = { type = "text_absent", path = "docs/phase0/legal-request.md", pattern = "[owner to fill after dispatch" }
```

---

## Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | `DEBT-NNN`, monotonic, never reused. |
| `title` | string | Yes | One line, imperative. What is still owed, not what was noticed. |
| `kind` | string | Yes | `artifact` (a file that must land), `reopen` (a question that must be asked again), `decision` (only a human can answer), `tech` (a check or migration), `uat` (a finding from verify-work). |
| `origin` | string | No | Where it came from: a plan ID, an AC, a SUMMARY section, a decision ID. |
| `owner` | string | Yes | `owner` (the human), `agent`, `phase-NN`, or `vendor`. Determines who a gate is allowed to nag. |
| `blocking` | string | No | Gate name, e.g. `phase-0-exit`. `debt.py --gate NAME` exits 1 while this row is unfinished. |
| `due` | string | No | ISO 8601 with timezone. Past tense: the row becomes **overdue** and interrupts. Future: **scheduled**, silent. |
| `trigger` | string | No | `event:<name>`, `phase:<NN>`, or `plan-count:<n>` — a condition no clock can test. Until it fires the row is **waiting** and silent. |
| `status` | string | No | `open` (default), `done`, `dropped`. The only state a human writes. |
| `check` | table | Yes | See check types. |

**At least one of `due`, `trigger`, `blocking` is required.** A row with none of them can never be surfaced by any gate.

---

## Check Types

| `type` | Fields | Passes when |
|--------|--------|-------------|
| `file_exists` | `path` (glob) | At least one file matches. |
| `file_absent` | `path` (glob) | No file matches. |
| `text_present` | `path` (glob), `pattern` (substring) | The pattern appears in at least one matching file. |
| `text_absent` | `path` (glob), `pattern` (substring) | The pattern appears in none of the matching files. |
| `command` | `run` (shell), `expect` (substring, optional) | Exit code 0, and stdout+stderr contains `expect`. |

Paths are relative to the project root.

**Choose a check that can fail.** `expect = "11"` passes against a docstring; `expect = "flip count = 11"` fails until the measurement actually printed that line. A check that cannot fail is worse than no check, because it reports work as done.

---

## Computed States

`debt.py` derives one state per row at read time. Nothing writes them back.

| State | Meaning | Effect on the agent |
|-------|---------|---------------------|
| `overdue` | `due` has passed, check still fails | Interrupt the user; leads the next-action report |
| `scheduled` | `due` is in the future | Silent. Mentioned in the summary counts only. |
| `waiting` | `trigger` has not fired | Silent. Fires when that phase/event/count arrives. |
| `open` | No date, no trigger, only a blocking gate | Silent at session entry; asked at `--gate` |
| `done` | `status = "done"`, or `--run-checks` passed | Excluded from gates |
| `dropped` | `status = "dropped"` | Excluded from gates; the decision to abandon is on record |

**Why this split matters:** a scheduled row must not nag, or every session opens with five false alarms and the gate gets ignored. Only `overdue` and `open`-at-gate are allowed to cost the user attention.

---

## Triggers

| Trigger form | Fires when |
|--------------|------------|
| `event:<name>` | The named event is observed by a workflow (e.g. `event:legal-dispatch`, `event:first-commit`, `event:mxv-reply`). “Waiting on a person or counterparty” is always `event`, never `due` — a guessed date generates false overdue reports. |
| `phase:<NN>` | `DEBT.toml` is read while planning or exiting phase `NN`. |
| `plan-count:<n>` | The project has completed `n` plans since the row was written. Used to stop a deferred item from surviving an entire milestone. |

---

## Evaluator Usage

```bash
python ~/.agents/paul-framework/scripts/debt.py --run-checks        # what landed?
python ~/.agents/paul-framework/scripts/debt.py --gate phase-0-exit # release gate
python ~/.agents/paul-framework/scripts/debt.py --root /path/to/app # run from anywhere
```

Root discovery walks up from the current directory to the nearest `.paul/DEBT.toml`.

---

## Where It Plugs In

| Gate | Workflow | Behaviour |
|------|----------|-----------|
| Session entry | `resume-project`, `paul-progress` | Report `overdue` rows first. An overdue `blocking` row outranks the loop table and becomes the single next action. |
| Plan drafting | `plan-phase` (`load_context`) | Every `waiting` row whose trigger is this phase, and every `overdue` row, becomes an AC in the plan or is named out of scope with a reason. Silent omission is a plan defect. |
| Phase exit | `transition-phase` | `--gate phase-<N>-exit`; exit 1 refuses the transition and states the row IDs. |
| Loop close | `unify-phase` | Writes rows for what the plan did not do; reports the open count. |
| Mid-plan | `apply-phase` deviation #5 | An enhancement noticed during execution is a row, not a note in a log. |

---

## Design Notes

- **Not append-only.** Unlike `ledger.toml`, rows are edited in place: a discharge is `status = "open"` → `"done"` in the same block, so the diff says what was paid. History lives in git.
- **Not a task list.** Anything needed to satisfy the current plan's ACs belongs in the PLAN, not here. Debt is what was deliberately deferred.
- **SUMMARY tables are views.** `## Carried forward` and `## Artifact-debt inventory` in a SUMMARY are generated from the store for the reader's convenience. When they disagree with `DEBT.toml`, the store wins.
- **No daemon.** PAUL runs in the foreground, so evaluation happens when the agent already has a reason to look. A scheduler nobody runs is a wish with a cron expression.
- **Pile-up cap.** More than 12 open non-blocking rows means the next plan must schedule one. The cap exists because an unbounded store becomes the same unread prose it replaced.
- **Sessions that must not fail.** A row with `owner = "owner"` is expected to be discharged by a human, so a gate names it and stops — it does not retry, invent a substitute, or mark itself done.

---

## Relationship to ISSUES.md

`ISSUES.md` holds enhancements with no test attached ("add a loading spinner"). It stays a markdown log because there is nothing to check. `DEBT.toml` holds anything that can be verified, which is everything with a landing condition. When a row is purely aspirational, it belongs in `ISSUES.md`; when it can be tested, it belongs here.

---

*Template added: v1.4 debt scheduler*
