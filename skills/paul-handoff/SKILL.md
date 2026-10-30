---
name: paul-handoff
description: Generate a thorough session handoff document. Use for context breaks needing decisions and gaps.
metadata:
  opencode/slash: "true"
---

## Purpose

Generate a comprehensive handoff document (`.paul/HANDOFF-{date}-{context}.md`) synthesizing session activity, decisions, gaps, and next actions.

Use it at end of session, on context break, or when decisions need documentation. More thorough than pause.

## Input

Optionally bring context notes:

- **Works best with:** inline notes (decisions, gaps, thoughts) supplementing detected session context
- **Also useful:** nothing else; conversation context is the primary source

Example: `Use paul-handoff: phase10-audit`

## Key Concepts

### Sources

STATE.md (phase, plan, loop position, continuity) plus conversation mining: files created/modified, commands executed, explicit/implicit decisions, questions, gaps, stated intentions. Inline input overrides or supplements detection.

### Decision/Gap Signals

Decisions: "I want to…", "Let's do…", "Decision:", approvals. Gaps: "Missing…", "We need…", GAP/TODO. Thoughts: "I think…", reasoning. Priorities: numbered lists, "First…", effort/impact talk.

## Application

### Step 1: Gather

From STATE.md take position and continuity. From conversation extract accomplishments, decisions (+rationale), questions, gaps, intentions, reference files. Fold in inline notes.

### Step 2: Synthesize

Combine into accomplishments, decisions table, gap analysis (CREATE/DEFER/INTENTIONAL with effort + source refs), open questions, reference files, prioritized next actions, state summary with resume pointer.

### pstack Enrichment (automatic)

pstack is present when `.paul/pstack-models.md` or the global `~/.agents/pstack-models.md` exists, or the `poteto-mode` skill is invocable in this session. If present, fold in any `show-me-your-work` decision trail for the session, and note in-flight pstack delegate work so the resume path runs the poteto-mode **session-pickup** playbook before the PAUL next action.

### Step 3: Generate

Write `.paul/HANDOFF-{date}-{context}.md` per the handoff template and display the HANDOFF CREATED confirmation (counts + `resume → read handoff` pointer).

When the `base` binary resolves, register the doc so it resurfaces at the next session start: `base handoff create --project "<project>" --doc "<absolute-doc-path>"` (project name from PROJECT.md; registering archives any prior open handoff, so re-running is safe). An unregistered doc is just a file nobody opens.

Verify success criteria:
- [ ] STATE.md read for current position
- [ ] Session context extracted (not just prompted)
- [ ] User's inline input incorporated
- [ ] Structured handoff generated
- [ ] Reference files included
- [ ] Next actions prioritized
- [ ] Handoff registered with base (when base resolves)

## Examples

### Example: Audit Break

Input: `phase10-audit`

Result: `.paul/HANDOFF-{date}-phase10-audit.md` with decisions, gaps, and ranked next actions.

## Common Pitfalls

- **Prompting instead of mining.** Consequence: thin handoff that restates the obvious. Fix: extract from conversation first, prompt only for gaps.

## References

- `.paul/STATE.md`
