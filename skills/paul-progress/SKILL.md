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

`.paul/STATE.md` + `.paul/ROADMAP.md` (phase totals, current plan, loop position, blockers, metrics) and `.paul/config.md` audit flags (audit enabled vs audited) for approval-stage routing.

### Routing Table

No plan → plan. Plan awaiting approval + audit enabled + not audited → audit. Awaiting approval otherwise → approve. Approved → apply. Applied → unify. Loop complete + more phases → plan next. Milestone complete → next milestone or ship. Blockers → address blocker. Context DEEP/CRITICAL → pause. User context adjusts the default.

## Application

1. Load STATE.md, ROADMAP.md (and config.md audit flags); compute milestone/phase progress and loop position.
2. Factor in user context if given (bug-first, time-box, finish-phase, stuck).
3. Determine exactly ONE next action per the routing table — never multiple.
4. Display the PAUL PROGRESS block (milestone bars, loop diagram, single NEXT line) plus a context advisory if at DEEP/CRITICAL.
5. Verify success criteria:
   - [ ] Overall progress displayed visually
   - [ ] Current loop position shown
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
