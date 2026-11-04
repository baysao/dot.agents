---
name: paul-research
description: Research a topic with subagents and save findings. Use to gather info before planning or implementing.
metadata:
  opencode/slash: "true"
---

## Purpose

Research a specific topic using subagents and save findings for review (`.paul/research/{topic}.md`).

Use it when information must be gathered before planning or implementing.

Research is the appropriate subagent use per subagent-criteria: self-contained, clear scope, parallelizable, 15–30 min per task.

## Input

Bring the topic (required):

- **Works best with:** a topic (e.g. `JWT best practices 2026`)
- **Also useful:** flags `--codebase` (Explore agent) or `--web` (general-purpose agent); no flag auto-detects

**Other harnesses.** `Explore`/`general-purpose` are Claude Code's subagent types; in OpenCode and Kilo Code use `explore`/`general` (`task` tool), in Codex and Cline `spawn_agent` (Cline: CLI/Desktop only). Drop the type where unsupported; with no subagent tool, run the agents yourself one after another.

Example: `Use paul-research: JWT best practices 2026 --web`

## Key Concepts

### Framework Sources of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/research.md` — workflow to follow
- `~/.agents/paul-framework/references/subagent-criteria.md` — subagent justification

### Project Context

- `.paul/PROJECT.md`, `.paul/STATE.md`
- `.paul/DEBT.toml` — a row whose trigger is an event (`vendor-reply`, `mxv-reply`) is research with a due date

## Application

1. Validate the topic is non-trivial; pick agent type by flag or auto-detect. Codebase agents answer structural questions by grepping for the exact symbol and citing file:line. For open-ended prior-work questions ("why is X like this", "what did we decide about Y"), read `.paul/DECISIONS.md` and `LEARNINGS.md` first and synthesize from those before searching externally.
2. Follow `research.md`: spawn the research subagent, save findings to `.paul/research/{topic}.md`.
3. Present a summary for review.
4. **Discharge the debt row the research answers.** If a `DEBT-NNN` row was waiting on this topic, the research is its evidence: say so in the summary and point the row's `check` at the research file (or at the artifact the finding enables) rather than leaving the row's trigger dangling. Research that answers a parked question but leaves the row `waiting` has produced a document, not a decision.

### pstack Fan-out (automatic)

pstack is present when `.paul/pstack-models.md` or the global `~/.agents/pstack-models.md` exists, or the `poteto-mode` skill is invocable in this session. If present and the topic has parallelizable slices, run the `swarm` skill instead of a single subagent: one worker per slice, one aggregated report. Keep the output rule the same: findings land in `.paul/research/{topic}.md`, summaries in-session, raw payloads in files.
4. Verify success criteria:
   - [ ] Topic validated (not trivial)
   - [ ] Appropriate agent type selected
   - [ ] Subagent spawned for research
   - [ ] Findings saved to `.paul/research/{topic}.md`
   - [ ] Summary presented for review

## Examples

### Example: Pre-Plan Research

Input: `JWT best practices 2026 --web`

Result: research file saved plus a reviewable summary.

## Common Pitfalls

- **Researching trivia via subagent.** Consequence: wasted tokens and latency. Fix: handle trivial lookups in-session.

## References

- `~/.agents/paul-framework/workflows/research.md`
- `~/.agents/paul-framework/references/subagent-criteria.md`
- `.paul/PROJECT.md`, `.paul/STATE.md`
