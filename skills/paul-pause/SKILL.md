---
name: paul-pause
description: Create a session handoff and prepare for a break. Use before ending or switching context.
metadata:
  opencode/slash: "true"
---

## Purpose

Create a `HANDOFF.md` file capturing current context and update STATE.md for session continuity.

Use it before ending a session, switching context, or when the context limit approaches.

## Input

Optionally bring a reason:

- **Works best with:** a reason (e.g. `switching to other project`) — included in handoff status
- **Also useful:** nothing else; position comes from `.paul/STATE.md` + `.paul/PROJECT.md`

Example: `Use paul-pause: switching to other project`

## Key Concepts

### Framework Source of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, read the same subpaths under `~/.agents/paul-framework/`. If neither exists, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/pause-work.md` — workflow to follow

## Application

1. Follow `pause-work.md`: detect current position, gather session context (ask user if needed), create `HANDOFF-{date}.md` fully populated (no placeholders), update STATE.md continuity, optional WIP commit, confirmation display.
2. pstack is present when `.paul/pstack-models.md` or the global `~/.agents/pstack-models.md` exists, or the `poteto-mode` skill is invocable in this session. If present, run the poteto-mode **pause-safely** playbook first so in-flight delegated work suspends cleanly, then write the PAUL handoff on top of it.
2. Include the reason argument in handoff status when provided.
3. Verify success criteria:
   - [ ] HANDOFF.md created with complete context (no placeholders)
   - [ ] STATE.md updated with session continuity
   - [ ] Next action is clear and actionable
   - [ ] Resume instructions provided

## Examples

### Example: End of Session

Input: `switching to other project`

Result: populated handoff file + STATE continuity + resume pointer.

## Common Pitfalls

- **Placeholder-filled handoff.** Consequence: next session resumes blind. Fix: populate every section before finishing.

## References

- `~/.agents/paul-framework/workflows/pause-work.md`
- `.paul/STATE.md`, `.paul/PROJECT.md`
