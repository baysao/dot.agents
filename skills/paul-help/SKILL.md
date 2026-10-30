---
name: paul-help
description: Show the PAUL command reference. Use to list the loop, commands, and workflows.
metadata:
  opencode/slash: "true"
---

## Purpose

Display the complete PAUL command reference: the Plan-Apply-Unify loop, quick start, per-command usage, file structure, PLAN.md shape, task types, common workflows, and key principles.

Use it when needing a usage overview rather than project-specific analysis. Output the reference only — no project analysis, git/file context, next-step suggestions, or commentary.

## Input

No input required.

Example: `Use paul-help: list commands`

## Key Concepts

### The Loop

PLAN (define) → APPLY (execute) → UNIFY (reconcile). Never skip UNIFY — every plan needs a summary.

### Command Groups

Core Loop (init, plan, apply, unify, help, progress); Session (pause, resume, progress, handoff); Roadmap (add-phase, remove-phase); Milestone (milestone, complete-milestone, discuss-milestone); Pre-Planning (discuss, assumptions, discover, consider-issues); Research (research, research-phase); Specialized (flows, config, map-codebase); Quality (verify, plan-fix, audit). Status is deprecated in favor of progress.

### Project Shape

`.paul/` holds PROJECT.md, ROADMAP.md, STATE.md, config.md, SPECIAL-FLOWS.md, MILESTONES.md, LEARNINGS.md (candidate/validated learnings from the reflect pass), and `phases/` with `{NN}-{PP}-PLAN.md` / AUDIT.md / SUMMARY.md per plan. Task types: auto, checkpoint:decision, checkpoint:human-verify, checkpoint:human-action.

### Other Harnesses

PAUL was written for Claude Code. Command naming: `/paul:<name>` there; in every other harness the same command is the `paul-<name>` skill — `/paul-<name>` slash in OpenCode and Cline, or name the skill in chat in Kilo Code and Codex. Framework files: read `~/.agents/paul-framework/<subpath>` where it exists, else `~/.agents/paul-framework/<subpath>`. Subagent types: Claude Code's `Explore`/`general-purpose` map to `explore`/`general` in OpenCode and Kilo Code, `spawn_agent` in Codex and Cline (CLI/Desktop only); with no subagent tool run them sequentially yourself. Cline discovers skills only under `.cline/skills/` or `~/.cline/skills/` — symlink or copy the paul-* skills there to use them.

## Application

Emit the reference: loop diagram, quick start (init → plan → apply → unify), per-command usage, files/structure, PLAN.md structure (objective, context, skills, acceptance criteria, tasks, boundaries, verification), task-type table, common workflows (new project, enterprise-with-audit, check-position, resume, pause, pre-planning, roadmap), and key principles (complete the loop, thin commands, tracked state, real boundaries, AC first, enforced skills).

pstack integration: when pstack is installed (`.paul/pstack-models.md` or `~/.agents/pstack-models.md` exists, or the poteto-mode skill is invocable), init offers the skill preset, plans auto-populate the `<skills>` section, apply routes tasks through poteto-mode playbooks with in-session qualification, audit runs an interrogate panel, research fans out via swarm, and unify closes with technical-writing, unslop, and a required reflect pass (skipped only for a trivial loop, one line in SUMMARY.md). Configure the preset with `/paul:flows pstack` (Claude Code) or the `paul-flows` skill in other harnesses.

Getting-help pointer: progress for position, PROJECT.md for context, STATE.md for loop state, ROADMAP.md for phases. Framework v0.4+, 26 commands.

## Examples

### Example: Orientation

Input: none.

Result: full reference output, no extra commentary.

## Common Pitfalls

- **Appending project advice to the reference.** Consequence: noisy output when a clean lookup was asked. Fix: reference only.

## References

- `.paul/PROJECT.md`, `.paul/STATE.md`, `.paul/ROADMAP.md`
