---
name: arena
description: "Spawn N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. Use for /arena, 'arena this', 'throw it in the arena', or when one attempt at a non-trivial artifact would lock in the wrong shape."
disable-model-invocation: true
metadata:
  opencode/slash: "true"
---

# Arena

Fan out N parallel attempts at the same task. Read every candidate end to end. Pick the strongest as the base. Graft the best ideas from the others into it. Verify the synthesized result.

## Start

Open a todolist with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Cross-judge
4. Pick
5. Graft
6. Verify

## Phase A: Frame

The N candidates will receive the same prompt, so the prompt is the contract.

1. State the artifact each candidate is producing.
2. Derive the rubric. State what success looks like for *this* task, then turn it into 3-6 concrete gradeable criteria. The rubric is the picker's tool in Phase D. Candidates only see the task.
3. Pick the runners. Use `arena runners` from the pstack settings file when present (`.paul/pstack-models.md` in PAUL projects; otherwise `~/.cursor/rules/pstack-models.mdc` in Cursor, `~/.agents/pstack-models.md` in OpenCode and other harnesses). Otherwise default to one each on `claude-fable-5-1-thinking-max`, `gpt-5.6-sol-max`, `grok-4.6-fast-xhigh`, `claude-opus-5-thinking-xhigh`. Spawn more when the arena covers multiple design directions. Same model N times when the work is generation-bound rather than judgment-sensitive.
4. Assign output paths. Each candidate writes to its own location (a git worktree where possible, otherwise `/tmp/arena-<slug>/candidate-<n>/`), per the **separate-before-serializing-shared-state** principle skill.
5. Ground the prompt in the live system. When the task touches an existing codebase, database, or API, the prompt must tell candidates to **measure** their assumptions against the running system (schema, constraints, current rows) instead of asserting them from a spec or from a message. A candidate that reasons from a stale spec returns the wrong constants, and the wrong constants are what the losing candidate is for.

## Phase B: Fan out

Spawn all N subagents in one message with `run_in_background: true`, each with the task, the path to the shared grounding, its own output path, and instructions to produce both the artifact and a short rationale.

**Other harnesses / OpenCode / Kilo Code / Cline.** In Claude Code use `Agent`, in Codex or Cline `spawn_agent` (Cline: CLI/Desktop only), dropping parameters your tool lacks. OpenCode's and Kilo Code's `task` tool takes only `description` (3-5 words), `prompt`, and `subagent_type` — no `model` or `readonly` — so send all calls in one message to run them concurrently (Kilo also accepts `background: true`). To run a runner or the judge on its configured model, spawn its pin: `subagent_type: pstack-<id>`, `<id>` being the slug lowercased with each non-alphanumeric run replaced by `-` (`grok-4.6-fast-xhigh` → `pstack-grok-4-6-fast-xhigh`). `/setup-pstack` writes the pins under `~/.config/opencode/agents/` (OpenCode) or `~/.config/kilo/agents/` (Kilo Code); create one before spawning if it is missing (`mode: subagent`, `model: <slug>`, body: follow the task prompt). For `inherit-parent`/`auto`, spawn `subagent_type: general` with no pin. **Cline.** Candidates and the judge come from `spawn_agent` (CLI and Desktop only, not the IDE extensions) and run on the session's model — no model parameter, no per-agent model config. Run every candidate and the judge on the session model and tell the user the cross-model comparison is gone.

Each rationale names the alternatives the candidate considered and what it rejected.

If a candidate fails to produce output, proceed with N-1 and note the dropout in the synthesis record.

## Phase C: Cross-judge

After all Phase B candidates complete, choose one model from the `arena cross-judge pool` in the pstack settings file when present (`.paul/pstack-models.md` in PAUL projects; otherwise `~/.cursor/rules/pstack-models.mdc` in Cursor, `~/.agents/pstack-models.md` in OpenCode and other harnesses). Otherwise use `claude-fable-5-1-thinking-max`, `gpt-5.6-sol-max`, `grok-4.6-fast-xhigh`, `claude-opus-5-thinking-xhigh`. Prefer a different model family from the parent's. Spawn one readonly judge subagent on that model. It sees the rubric and the candidates by path label, scores each criterion, and recommends a base with rationale. It runs in parallel with the parent's reading in Phase D, not with the candidates themselves. Don't spawn the judge while candidates are still writing.

## Phase D: Pick a base

Read every candidate end to end before picking.

Score each candidate against the rubric criterion by criterion, not on holistic feel. Compare against the cross-judge. Agreement on the base confirms the pick. Disagreement means one of you is biased or the rubric was ambiguous. Read both rationales before deciding.

Pick the base on which candidate a future maintainer can extend most easily without breaking invariants. Prefer the cleaner boundary or smaller API when two feel tied, per the Laziness Protocol.

Record the pick and the reason in a short synthesis note alongside the base artifact, including the cross-judge's verdict.

## Phase E: Graft

Walk each losing candidate once more and identify what is worth porting into the base. The signal is usually one or two things per candidate, not most of it.

Harvest the loser's **measured facts** separately from its shape. A losing candidate often measured the live system and came back with facts the winner assumed or got wrong: an enum value the database actually stores, a rate, a column scale, a check constraint, a foreign key. Take those facts even when you take the other candidate's shape, and record which candidate each fact came from. The shape decides what to build; the measured facts decide whether it works.

Fold each graft in by hand, per the **redesign-from-first-principles** principle skill. Don't paste mechanically. The result has to remain coherent under one mental model.

Record what was grafted, from which candidate, and what was rejected and why.

When N candidates converge on the same shape, that is a strong agreement signal. Note the convergence in the record and ship the consensus shape. No graft is needed. When N candidates wildly diverge, Phase A was under-specified. Reframe and re-run rather than averaging the divergence.

## Phase F: Verify

The synthesized artifact has to hold up under the same scrutiny as any other output, per the **prove-it-works** principle skill.

If verification surfaces a problem the arena did not catch, either Phase A was wrong (re-frame and re-run) or one candidate caught it and you missed the graft (go back to Phase E). Don't paper over.

## Outputs

One synthesized artifact. One short synthesis note alongside, naming the base, the grafts (with source candidate), the rejections, the dropouts if any, and the verification result.
