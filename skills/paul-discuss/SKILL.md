---
name: paul-discuss
description: Explore phase vision conversationally before planning. Use to articulate goals into CONTEXT.md.
metadata:
  opencode/slash: "true"
---

## Purpose

Facilitate vision discussion for a specific phase and create a context handoff (`CONTEXT.md` in the phase directory).

Use it before planning a phase, when goals and approach need exploration.

## Input

Bring the phase (required):

- **Works best with:** a phase number (e.g. `3`) or topic (e.g. `authentication layer`)

Example: `Use paul-discuss: explore phase 3`

## Key Concepts

### Framework Source of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/discuss-phase.md` — workflow to follow

### Project Context

- `.paul/PROJECT.md`, `.paul/STATE.md`, `.paul/ROADMAP.md`
- `.paul/DEBT.toml` — deferred work already pointing at this phase

### Debt Informs the Vision

Run `python ~/.agents/paul-framework/scripts/debt.py --run-checks` before the conversation. Rows whose trigger names this phase are scope the vision has to account for: an unresolved decision, an artefact nobody committed, a check that has been failing since an earlier loop. Naming them in `CONTEXT.md` is how they enter the plan instead of surprising it at UNIFY.

## Application

1. Resolve the phase from input; ask if missing.
2. Follow `discuss-phase.md`: conversational exploration of goals and approach. When an open-ended "why did we choose X" question comes up, read `.paul/DECISIONS.md` for the recorded rationale and `LEARNINGS.md` for the correction history, then synthesize the answer yourself before asking the user from scratch.
3. Write `CONTEXT.md` in the phase directory capturing vision, goals, and approach, plus a `## Carried debt` list of the `DEBT-NNN` rows this phase inherits.
4. Verify success criteria:
   - [ ] CONTEXT.md created in phase directory
   - [ ] Goals and approach articulated
   - [ ] Debt rows naming this phase listed in CONTEXT.md
   - [ ] Ready for plan

## Examples

### Example: Pre-Plan Discussion

Input: `3`

Result: phase CONTEXT.md capturing what the phase should achieve and how.

## Common Pitfalls

- **Jumping to plan without discussion.** Consequence: plan encodes unexamined goals. Fix: discuss first when vision is fuzzy.

## References

- `~/.agents/paul-framework/workflows/discuss-phase.md`
- `.paul/PROJECT.md`, `.paul/STATE.md`, `.paul/ROADMAP.md`
