---
name: aegis-resume
description: Resume an interrupted AEGIS audit from checkpoint or phase. Use to continue phases 0-5.
---

## Purpose

Resume an interrupted AEGIS diagnostic audit from the last checkpoint or a specified phase. Reads STATE.md, displays progress, routes to the correct phase workflow, and updates resume/session state.

Routes to audit when no `.aegis/` exists; completed audits route to status/report/transform/fresh instead.

## Input

Optionally bring a phase:

- **Works best with:** a phase number 0-5 (skips the options menu)
- **Also useful:** nothing else; position resolves from `.aegis/STATE.md`

Example: `Use aegis-resume: continue from phase 2`

## Key Concepts

### Framework Sources of Truth

- `phase-0-context.md` … `phase-5-report.md` — delegation targets
- `phase-checkpoint.md` — boundary semantics

### Resume Logic

Active phase with partial completion → resume at next unfinished agent. Last phase complete → start next pending phase. Completed audit → offer status/report/transform/fresh. Fresh-start requires typed DELETE confirmation.

## Application

1. If no `.aegis/STATE.md`: show NO ACTIVE AUDIT with start-new-audit / cancel.
2. Read STATE.md (target, times, current phase, overall + per-phase status, finding counts, resume info, disagreements, session tracking, checkpoint history). If complete: show AUDIT COMPLETE menu.
3. Display the RESUME block (target, started, status, relative session time, phase table, cumulative severity counts, disagreements, checkpoint history, last/next action).
4. Resolve resume point: given phase → validate 0-5 and delegate; otherwise offer last-checkpoint / re-run / jump (warn on skips) / fresh (DELETE confirm) / cancel.
5. Update STATE.md (resume info, increment sessions, stamp last-session, set in_progress) and delegate without re-reading completed phase outputs.
6. Verify success criteria:
   - [ ] Position identified from STATE.md
   - [ ] Progress displayed
   - [ ] Resume point selected
   - [ ] Correct phase workflow delegated
   - [ ] STATE.md updated
   - [ ] Cancellation available at every decision

## Examples

### Example: Paused Mid-Phase-2

Input: none.

Result: resume display, continuation at the next unfinished Phase 2 agent.

## Common Pitfalls

- **Re-reading completed outputs at resume level.** Consequence: context bloat. Fix: let phase workflows + session-handoff load context.

## References

- `~/.agents/aegis/core/workflows/phase-0-context.md` … `phase-5-report.md`
- `~/.agents/aegis/core/workflows/phase-checkpoint.md`
- `.aegis/STATE.md`
