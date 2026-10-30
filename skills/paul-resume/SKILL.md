---
name: paul-resume
description: Restore PAUL context after a break with one next action. Use at session start, when the user asks "what did we do so far" / "where did we leave off", or when continuing from a handoff.
metadata:
  opencode/slash: "true"
---

## Purpose

Restore PAUL context after a session break, determine current position, and suggest exactly ONE next action.

Use it when starting a new session on an existing PAUL project. Detected handoffs are presented, then archived after work proceeds.

## Input

Optionally bring a handoff path:

- **Works best with:** a handoff path (e.g. `.paul/HANDOFF-phase10-audit.md`) — otherwise the most recent handoff is used
- **Also useful:** nothing else; STATE.md is always loaded

Example: `Use paul-resume: .paul/HANDOFF-phase10-audit.md`

## Key Concepts

### Framework Source of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, read the same subpaths under `~/.agents/paul-framework/`. If neither exists, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/resume-project.md` — workflow to follow

### Handoff Pattern

`.paul/HANDOFF-{context}.md`. Suggest exactly ONE next action — never multiple.

### Continuity-Block Authority

STATE.md grows append-only Session-Continuity blocks, each with its own `Resume pointer` / `pending` lines. **Only the newest block's pointer is authoritative** — older blocks are narrative log, not routing. Treat any older `Resume pointer` that names a plan now marked UNIFIED as stale: ignore it when routing, and strike it (`~~…~~` → point at the UNIFIED bullet) the moment you (or a unify pass) notice the mismatch. A stale pointer is a routing instruction to do work that is already done.

### BASE Integration

BASE is present when `.paul/config.md` shows `BASE: enabled` (or BASE integration status is enabled). When enabled, session start retrieves durable context from the base graph:

- `base recall --keyword "paul"` — surfaces recent learnings, decisions, rules
- `base decision search --keyword "paul"` — finds project decisions with rationale
- `base rule list --domain <project>` — shows active behavioral rules

The project domain name derives from the project folder (or `.paul/config.md` project name). This context supplements (not replaces) handoff and STATE.md. If BASE is not enabled, fall back to handoff/STATE.md only.

## Application

1. Verify `.paul/` exists. Detect handoff files (given path or most recent); load STATE.md. 
   - If `.paul/config.md` shows `BASE: enabled`, call `base recall --keyword "paul"` and `base decision search --keyword "paul"` to surface recent context, and `base rule list --domain <project>` for active rules — inject these alongside handoff/STATE.md.
2. Follow `resume-project.md`: present handoff content if detected, reconcile handoff vs STATE.md, determine ONE next action from loop position, display resume status.
3. **Verify the restored state against the live system before routing.** STATE.md and a handoff are *claims*, not facts: another session, a sibling worktree, a cron job, or a deploy may have changed the database, the branch, or the running processes since they were written. Probe the surfaces they describe — the process/port, one representative endpoint, the rows or schema they assert — and reconcile. A live state that disagrees with STATE.md outranks STATE.md: report the discrepancy and route on what is actually true.
3. pstack is present when `.paul/pstack-models.md` or the global `~/.agents/pstack-models.md` exists, or the `poteto-mode` skill is invocable in this session. If present, run the poteto-mode **session-pickup** playbook to take over any in-flight delegated work, and the `recall` skill to rebuild recent context from chat history and the shared record before acting on the ONE next action.
3. After work proceeds, archive/delete the consumed handoff.
4. Verify success criteria:
   - [ ] Context restored from STATE.md and/or handoff
   - [ ] Loop position correctly identified
   - [ ] Exactly ONE next action suggested
   - [ ] User can proceed or redirect with context

## Examples

### Example: New Session

Input: none — most recent handoff auto-detected.

Result: restored context with a single routed next action.

## Common Pitfalls

- **Listing options instead of routing.** Consequence: cold-start drift. Fix: exactly one action.

## References

- `~/.agents/paul-framework/workflows/resume-project.md`
- `.paul/STATE.md`
