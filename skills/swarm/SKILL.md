---
name: swarm
description: "Fan out N parallel workers, drain them, and return one report. Use for /swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration."
disable-model-invocation: true
metadata:
  opencode/slash: "true"
---

# Swarm

Fan out N parallel cloud workers. They may cover separate slices, race the same brief, or mix both. The parent waits, aggregates, and returns one report.

## Start

Open a todolist with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Set N from the user or derive it from the shape. N is total workers, not the cloud concurrency limit.
4. Pick the worker model from `swarm workers` in the pstack settings file when present (`.paul/pstack-models.md` in PAUL projects; otherwise `~/.cursor/rules/pstack-models.mdc` in Cursor, `~/.agents/pstack-models.md` in OpenCode and other harnesses). Otherwise use `grok-4.6-fast-xhigh`. For a model race, name each arm's model up front.
5. Give each worker its own writable output when it writes.

## Phase B: Fan out

Spawn all N workers in one message with `subagent_type: generalPurpose`, `environment: "cloud"`, `run_in_background: true`, and the configured model. Use `environment: "local"` only when the worker needs access to something on the user's computer.

When a worker must start from a non-default pushed branch, pass `cloud_base_branch`.

**Other harnesses.** These parameters belong to Cursor's `Task` tool, and `environment: "cloud"` runs a Cursor cloud agent. In another harness, use its subagent tool: `Agent` in Claude Code (`subagent_type: general-purpose`), `task` in OpenCode and Kilo Code (`subagent_type: general`), `spawn_agent` in Codex and in Cline. Workers run locally there, so give each one its own worktree or output path. Keep the brief and, where your tool accepts one, the model. Drop parameters your tool doesn't have. If your harness has no subagent tool, as in Pi without an extension, run the workers yourself, one after another.

**OpenCode / Kilo Code.** Their `task` tool takes only `description` (3-5 words), `prompt`, and `subagent_type` — no `model` or `readonly` — so send all worker calls in one message to run them concurrently (Kilo's `task` also accepts `background: true`). To run a configured model (a `swarm workers` entry or a race arm), spawn its pin: `subagent_type: pstack-<id>`, `<id>` being the slug lowercased with each non-alphanumeric run replaced by `-` (`grok-4.6-fast-xhigh` → `pstack-grok-4-6-fast-xhigh`). `/setup-pstack` writes the pins under `~/.config/opencode/agents/` (OpenCode) or `~/.config/kilo/agents/` (Kilo Code); create one before spawning if it is missing (`mode: subagent`, `model: <slug>`, body: follow the task prompt). For `inherit-parent`/`auto`, spawn `subagent_type: general` with no pin. **Cline.** Workers come from `spawn_agent` (CLI and Desktop only, not the IDE extensions) and run on the session's model — no model parameter, no per-agent model config. Run every arm on the session model and tell the user a model race can't differentiate there.

Every brief stands alone. Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence.

If a worker drops out, proceed with N-1 and note it.

## Phase C: Aggregate

Read the terminal results. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

Keep a compact result table, one-line evidenced issues, and explicit gaps or dropouts.

## Phase D: Report

Return one consolidated in-chat report with the table, issue one-liners, gaps or dropouts, and the race rule when used.
