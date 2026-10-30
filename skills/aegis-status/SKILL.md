---
name: aegis-status
description: Display AEGIS audit state read-only. Use to check progress without modifying anything.
---

## Purpose

Display the current state of an AEGIS diagnostic audit without modifying anything: phase progress, finding counts, disagreement status, remaining-work estimates, and exactly one next action.

Read-only — never writes state or artifacts. Reports no-audit + audit suggestion when absent.

## Input

No input required. Reads `.aegis/STATE.md` plus filesystem counts.

Example: `Use aegis-status: where is the audit`

## Key Concepts

### Standalone

No workflow delegation. Counts come from STATE.md cross-checked with `.aegis/findings/*/`, `.aegis/signals/*/`, `.aegis/report/`, `.aegis/review/` presence.

### Routing Map

All complete + no report → report. Complete + report → transform. Active phase → resume that phase. Pending next → resume to start it. Paused → resume from last action.

## Application

1. If no `.aegis/STATE.md`: show NO ACTIVE AUDIT with the audit pointer and exit.
2. Read STATE.md (target, times, phase, status, findings, disagreements, sessions) and filesystem counts.
3. Display the STATUS block (target, started, status, version, phase table, severity summary, disagreements, domains, sessions) plus remaining-work estimates for pending phases only (0:1, 1:1, 2:1-8, 3:1-2, 4:1, 5:1 sessions).
4. Suggest exactly one NEXT ACTION per the routing map.
5. Verify success criteria:
   - [ ] STATE.md read
   - [ ] Phase progress with accurate counts
   - [ ] Severity + disagreement status shown
   - [ ] Exactly one next action
   - [ ] No state files modified

## Examples

### Example: Mid-Audit Check

Input: none.

Result: full status table with one routed next step, zero writes.

## Common Pitfalls

- **Suggesting several next steps.** Consequence: decision fatigue. Fix: exactly one action.

## References

- `.aegis/STATE.md`
