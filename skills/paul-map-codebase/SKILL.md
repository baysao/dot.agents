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

### base AST (automatic)

base is present when the `base` binary resolves (`base --version`). If present, run `base sync --ast` before spawning agents so the workspace AST map is fresh, and tell each Explore agent to answer structural questions (who calls X, which files import Y, where does type Z live) with `base ast query` (`--calls`, `-f`, `-c`) before reading files. Record the sync time in the generated docs. A stale map is a claim, not a fact. Multi-app workspaces map sibling apps with `base sync --ast --target apps/X` and query them with `base ast query -t apps/X` without changing directory.

### pstack Walkthrough (automatic)

pstack is present when `.paul/pstack-models.md` or the global `~/.agents/pstack-models.md` exists, or the `poteto-mode` skill is invocable in this session. If present, run the `how` skill after mapping to produce a plain-language walkthrough of how the codebase works, and the `swarm` skill if a coverage matrix over packages or directories fits better than the four fixed agent slices.

## Application

1. Follow `map-codebase.md`: if `.paul/codebase/` exists offer refresh/update/skip.
2. Create the directory structure; spawn the 4 parallel Explore agents; collect findings.
3. Write the 7 codebase documents from templates, verify, commit, and offer next steps.
4. Verify success criteria:
   - [ ] .paul/codebase/ directory created
   - [ ] All 7 documents populated with findings
   - [ ] Documents include actual file paths (actionable)
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
