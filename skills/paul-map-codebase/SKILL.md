---
name: paul-map-codebase
description: Map an existing codebase into structured docs. Use before planning on unfamiliar code.
metadata:
  opencode/slash: "true"
---

## Purpose

Analyze an existing codebase and create structured documentation in `.paul/codebase/` via parallel Explore agents covering stack, architecture, conventions, testing, integrations, and concerns.

Use it when adopting PAUL on unfamiliar code or when planning needs a shared codebase picture.

## Input

No input required:

- **Works best with:** zero input — it scans the working tree
- **Also useful:** a refresh/skip decision if `.paul/codebase/` already exists

Example: `Use paul-map-codebase: map this repo`

## Key Concepts

### Framework Source of Truth

- `~/.agents/paul-framework/workflows/map-codebase.md` — workflow to follow

### Agent Split

Four parallel Explore agents: (1) Stack + Integrations, (2) Architecture + Structure, (3) Conventions + Testing, (4) Concerns. Findings aggregate into 7 codebase documents with actionable file paths.

**Other harnesses.** Claude Code's `Explore` type maps to `explore` in OpenCode and Kilo Code (`task` tool), a read-only agent in Codex, and to `spawn_agent` in Cline (CLI/Desktop only). Drop the type parameter where unsupported, and if the harness has no subagent tool run the four agents yourself one after another.

### Structural Questions

Tell each Explore agent to answer structural questions (who calls X, which files import Y, where does type Z live) by grepping for the exact symbol before reading files, and to record the measured answer with its file:line evidence. A map that was not re-measured is a claim, not a fact. Multi-app workspaces: search sibling apps under `apps/X` directly, without changing directory.

### pstack Walkthrough (automatic)

pstack is present when `.paul/pstack-models.md` or the global `~/.agents/pstack-models.md` exists, or the `poteto-mode` skill is invocable in this session. If present, run the `how` skill after mapping to produce a plain-language walkthrough of how the codebase works, and the `swarm` skill if a coverage matrix over packages or directories fits better than the four fixed agent slices.

## Application

1. Follow `map-codebase.md`: if `.paul/codebase/` exists offer refresh/update/skip.
2. Create the directory structure; spawn the 4 parallel Explore agents; collect findings.
3. Write the 7 codebase documents from templates, verify, commit, and offer next steps.
4. **Convert the Concerns document into debt rows.** A concern the map finds but nobody schedules is a paragraph in a document nobody re-reads. For each concrete, testable concern, append a `[[debt]]` row (`kind = "tech"`, `owner = "agent"`, `trigger = "phase:NN"`) whose check asserts the concern stays fixed. Run `python ~/.agents/paul-framework/scripts/debt.py` and confirm the store parses.
5. Verify success criteria:
   - [ ] .paul/codebase/ directory created
   - [ ] All 7 documents populated with findings
   - [ ] Documents include actual file paths (actionable)
   - [ ] Testable concerns from the map exist as debt rows
   - [ ] Codebase map committed
   - [ ] User informed of next steps

## Examples

### Example: Adopt Existing Repo

Input: none.

Result: committed `.paul/codebase/` map with 7 actionable documents.

## Common Pitfalls

- **Mapping without file paths.** Consequence: unactionable overview. Fix: require real paths in every document.

## References

- `~/.agents/paul-framework/workflows/map-codebase.md`
- `.paul/codebase/`
