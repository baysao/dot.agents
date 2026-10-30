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

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, read the same subpaths under `~/.agents/paul-framework/`. If neither exists, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/discuss-phase.md` — workflow to follow

### Project Context

- `.paul/PROJECT.md`, `.paul/STATE.md`, `.paul/ROADMAP.md`

## Application

1. Resolve the phase from input; ask if missing.
2. Follow `discuss-phase.md`: conversational exploration of goals and approach. When an open-ended "why did we choose X" question comes up and the `base` binary resolves, run `base graph query "<question>" --raw` for the matching subgraph, then synthesize the answer yourself before asking the user from scratch (`--raw` skips base's broken subprocess synthesis on gateway models).
3. Write `CONTEXT.md` in the phase directory capturing vision, goals, and approach.
4. Verify success criteria:
   - [ ] CONTEXT.md created in phase directory
   - [ ] Goals and approach articulated
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
