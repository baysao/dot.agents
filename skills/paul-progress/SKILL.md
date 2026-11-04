---
name: paul-progress
description: Show smart PAUL status with exactly one next action. Use for mid-session routing.
metadata:
  opencode/slash: "true"
---

## Purpose

Show current progress and route to exactly ONE next action, preventing decision fatigue.

Use it for mid-session checks, after resume for more context, when unsure what to do next, or to get a suggestion tailored to a stated constraint.

## Input

Optionally bring context:

- **Works best with:** zero input (state-only routing), or a constraint (e.g. `I only have 30 minutes`, `I need to fix a bug first`)
- **Also useful:** a stuck-point description to reroute around

Example: `Use paul-progress: I only have 30 minutes`

## Key Concepts

### Sources

`.paul/STATE.md` + `.paul/ROADMAP.md` (phase totals, current plan, loop position, blockers, metrics), `.paul/DEBT.toml` via `scripts/debt.py` (overdue rows outrank the loop), and `.paul/config.md` audit flags (audit enabled vs audited) for approval-stage routing.

### Routing Table

An **overdue** debt row outranks everything below it: report the row ID, its title, and the check that still fails, and make discharging it the single next action. A `scheduled` or `waiting` row is not reported — only a date that has passed is news.

No plan → plan. Plan awaiting approval + audit enabled + not audited → audit. Awaiting approval otherwise → approve. Approved → apply. **Applied but `loop.hold_until` is in the future → wait; name the date and reason, and do not unify.** Applied → unify. Loop complete + more phases → plan next. Milestone complete → next milestone or ship. Blockers → address blocker. Context DEEP/CRITICAL → pause. User context adjusts the default.

**"Applied" means the plan's own exit condition was observed, not that its tasks ran.** A task that waits on a calendar (a probe window, a counterparty reply, a batch job) leaves the plan APPLYING on purpose.

## Application

1. Load STATE.md, ROADMAP.md (and config.md audit flags); compute milestone/phase progress and loop position.
2. Run `python ~/.agents/paul-framework/scripts/debt.py` when `.paul/DEBT.toml` exists; an `overdue` row pre-empts the routing table.
3. Factor in user context if given (bug-first, time-box, finish-phase, stuck).
4. Determine exactly ONE next action per the routing table — never multiple.
5. Display the PAUL PROGRESS block (milestone bars, loop diagram, single NEXT line) plus a context advisory if at DEEP/CRITICAL.
6. Verify success criteria:
   - [ ] Overall progress displayed visually
   - [ ] Current loop position shown
   - [ ] Overdue debt surfaced (or confirmed absent)
   - [ ] Exactly ONE next action suggested
   - [ ] User context considered if provided
   - [ ] Context advisory shown if needed

## Examples

### Example: Time-Boxed Check

Input: `I only have 30 minutes`

Result: progress display with one scope-fitting next action.

## Common Pitfalls

- **Suggesting several options.** Consequence: decision fatigue the skill exists to prevent. Fix: exactly one action, always.

## References

- `.paul/STATE.md`, `.paul/ROADMAP.md`, `.paul/config.md`
