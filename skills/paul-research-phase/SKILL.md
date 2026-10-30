---
name: paul-research-phase
description: Identify and research a phase's unknowns with subagents. Use before planning an uncertain phase.
metadata:
  opencode/slash: "true"
---

## Purpose

Analyze a phase for unknowns and research them using parallel subagents. Produces per-unknown files plus a consolidated phase `RESEARCH.md`.

Use it before planning a phase with technical unknowns needing investigation.

Distinction from research: research takes a user-known topic; research-phase has the agent identify what needs researching.

## Input

Bring the phase (required):

- **Works best with:** a phase number (e.g. `10`)

Example: `Use paul-research-phase: research phase 10`

## Key Concepts

### Framework Sources of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, read the same subpaths under `~/.agents/paul-framework/`. If neither exists, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/research.md` — workflow to follow
- `~/.agents/paul-framework/references/subagent-criteria.md` — parallel-agent justification

### Unknown Categories

Codebase (Explore agent), Web/Docs (general-purpose agent), Comparison, Architecture. Max 3 parallel agents; only substantial (15+ min) unknowns qualify.

## Application

### Step 1: Validate Phase

Parse the phase number; error with usage if missing. Validate against ROADMAP.md; list incomplete phases and exit if not found.

### Step 2: Analyze Unknowns

Read ROADMAP.md scope, PROJECT.md context, and any phase CONTEXT.md. Identify and classify unknowns, present the list, and wait for user confirmation.

### Step 3: Spawn Agents

Validate against subagent-criteria, then spawn up to 3 research agents in parallel (Explore for codebase, general-purpose for web). Codebase agents get `base ast query` in their toolkit when the `base` binary resolves — the workspace AST map answers structure questions faster than file fan-out. Other harnesses: `explore`/`general` in OpenCode and Kilo Code (`task` tool), `spawn_agent` in Codex and Cline (CLI/Desktop only) — drop the type where unsupported, or run the agents sequentially yourself when there is no subagent tool.

### Step 4: Consolidate

Write individual findings to `.paul/phases/{NN}-{name}/research/{unknown-slug}.md` and a consolidated `.paul/phases/{NN}-{name}/RESEARCH.md`. Present the summary and offer next steps (review, plan, discuss, done).

Verify success criteria:
- [ ] Phase validated against ROADMAP.md
- [ ] Unknowns identified and classified
- [ ] User confirmed research list
- [ ] Appropriate agents spawned in parallel
- [ ] Findings consolidated into phase RESEARCH.md
- [ ] Summary presented for review

## Examples

### Example: Uncertain Phase

Input: `10`

Result: unknowns researched in parallel, consolidated RESEARCH.md ready for planning.

## Common Pitfalls

- **Skipping user confirmation.** Consequence: research burns on wrong unknowns. Fix: present the list and wait.
- **Over-parallelizing.** Consequence: token blowup. Fix: cap at 3 agents per batch.

## References

- `~/.agents/paul-framework/workflows/research.md`
- `~/.agents/paul-framework/references/subagent-criteria.md`
- `.paul/PROJECT.md`, `.paul/STATE.md`, `.paul/ROADMAP.md`
