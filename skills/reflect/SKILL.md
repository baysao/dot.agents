---
name: reflect
description: Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect.
disable-model-invocation: true
metadata:
  opencode/slash: "true"
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

## When to invoke

Invoke when the user says "reflect" or "/reflect", and automatically from the paul-unify reflect pass. Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## Process

### 1. Locate the active transcript

The parent finds its own transcript file before fanning out. Use only the active workspace's transcript directory. Never glob across every project's directory. That crosses workspace boundaries and reads private chats from unrelated projects.

Where the transcript lives depends on your harness:

- **Cursor:** the system prompt names the active workspace's `agent-transcripts/` directory. Use that path.

  ```bash
  ls -t <agent-transcripts>/*.jsonl <agent-transcripts>/*/*.jsonl <agent-transcripts>/*/subagents/*.jsonl 2>/dev/null | head -10
  ```

  Three transcript layouts: legacy flat (`<id>.jsonl`), current nested (`<id>/<id>.jsonl`), and subagent (`<parent>/subagents/<child>.jsonl`).
- **Claude Code:** `~/.agents/projects/<slug>/<session-id>.jsonl`, where `<slug>` is the workspace path with every character that isn't a letter or digit turned into "-".
- **Pi:** `~/.pi/agent/sessions/--<slug>--/*.jsonl`, where `<slug>` is the workspace path with the leading slash dropped and each "/" turned into "-".
- **Codex:** `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`. Keep only files whose first line has `payload.cwd` equal to the workspace path.
- **OpenCode:** no session transcript store — `~/.local/share/opencode` holds only `log/`, `repos/`, `snapshot/`. Skip the hunt and go straight to the digest fallback.
- **Other harnesses:** check the harness's session directory for this workspace.

Take the newest candidates first. Confirm a candidate by finding the conversation's opening user prompt in its first user message. Take the matching path. If no path resolves, mine the project's durable learning record *before* writing the digest: grep `.paul/ledger.toml` result fields for `REFLECT_` (prior reflect passes store their findings there) and read the skill-audit tables in recent `*-SUMMARY.md` files, then fold the relevant entries into the digest so reviewers do not re-derive learnings the project already recorded. **A digest is the reviewers' entire world** — it must include: the session arc (what was done, what the user asked), environment facts worth preserving (commands, ports, creds-keys-not-values, tool failures), and the **skills/MCPs actually invoked** (findings not attributable to a used skill are dropped by every reviewer).

When using the digest fallback (no transcript store), the digest must also carry a **parent-independent artifact block**: raw facts the parent did not author this session — `git status --short` / `git log --oneline -n 10` tails for touched paths, parser outputs (tomllib counts, tsc exit codes), and file/line counts pulled fresh from disk. Without it, reviewers can only audit the parent's retrospective summary against the parent's own claims, and "verified X" is unfalsifiable from inside the panel.

### Re-run protocol (pass 2+)

If reflect is invoked again on the same session without prior Accepted items being applied:
1. Surface the prior pass's Accepted table + apply-status (applied/awaiting approval) in the digest before spawning new reviewers.
2. Re-read any skill the current digest marks as edited since the prior pass — rejection reasons may be stale against the new body.
3. Merge restatements of prior Accepted findings into the existing rows instead of creating new ones; note them as "(extends pass-1 A#)" in the synthesizer.

### 2. Spawn three reviewers in parallel

One message, three `Task` calls, `subagent_type: generalPurpose`, explicit `model:` on each, agent mode (`readonly: false`). Reviewers need MCP access for context lookups (tickets, chat threads, observability traces referenced in the transcript). Readonly strips MCPs.

**Other harnesses.** The spawns in this skill use Cursor's `Task` tool. In another harness, use its subagent tool: `Agent` in Claude Code (`subagent_type: general-purpose`), `task` in OpenCode and Kilo Code (`subagent_type: general`), `spawn_agent` in Codex and in Cline. Keep the prompt and, where your tool accepts one, the model. Drop parameters your tool doesn't have. If your harness has no subagent tool, as in Pi without an extension, run each role yourself, one after another. "Your configured ... model" means the matching line in the pstack settings file. Cursor loads `~/.cursor/rules/pstack-models.mdc` automatically. In other harnesses, read `~/.agents/pstack-models.md` if it exists. In any harness, `.paul/pstack-models.md` wins when the project has one.

**OpenCode / Kilo Code.** Their `task` tool takes only `description` (3-5 words), `prompt`, and `subagent_type` — no `model` or `readonly` — so send all calls in one message to run them concurrently and drop the rest (Kilo's `task` also accepts `background: true`). Their built-in read-only `explore` subagent fits a readonly role running on the parent model. To run a configured model, spawn its pin: `subagent_type: pstack-<id>`, `<id>` being the slug lowercased with each non-alphanumeric run replaced by `-` (`claude-fable-5-1-thinking-max` → `pstack-claude-fable-5-1-thinking-max`). `/setup-pstack` writes the pins under `~/.config/opencode/agents/` (OpenCode) or `~/.config/kilo/agents/` (Kilo Code); create one before spawning if it is missing (`mode: subagent`, `model: <slug>`, body: follow the task prompt). For `inherit-parent`/`auto`, spawn `subagent_type: general` with no pin. **Cline.** Subagents come from `spawn_agent` (CLI and Desktop only, not the IDE extensions) and run on the session's model — no model parameter, no per-agent model config. Run the panel on the session model and tell the user the cross-model signal is gone.

| Lens | `model` | Prompt template |
|---|---|---|
| Judgment | your configured reflect-judgment model (default `claude-fable-5-1-thinking-max`) | `references/judgment-reviewer.md` |
| Tooling | your configured reflect-tooling model (default `gpt-5.6-sol-max`) | `references/tooling-reviewer.md` |
| Divergent | your configured reflect-judgment model (default `claude-fable-5-1-thinking-max`) | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings in the `Task` response body.

### 3. Synthesize

One `Task` call, `subagent_type: generalPurpose`, using your configured reflect-judgment model (default `claude-fable-5-1-thinking-max`), agent mode (`readonly: false`). The synthesizer's quality check includes spot-verifying citations, which can require MCP access. Readonly strips MCPs. Use `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. The synthesizer returns a structured Accepted / Rejected / Backlog list.

### 4. Structural enforcement check

Sanity-check the synthesizer's Accepted list. For any item that would be enforced more reliably by a lint rule, script, metadata flag, or runtime check, move it from Accepted to Backlog. See the **encode-lessons-in-structure** principle skill.

### 5. Apply

Before applying any Accepted edit, present the synthesizer's full Accepted/Rejected/Backlog output to the user and wait for explicit approval. The user picks which subset to apply and may redirect routings. Skill changes affect every future agent in the org. Do not auto-apply.

Backlog items file to whatever devex / backlog tracker your team uses automatically. Only the Accepted list waits for approval.

**Evidence tiers gate the route.** An item with direct evidence in this transcript — a user correction, a reproduced failure, a fix verified by a check — keeps the routing below. An item that is only plausible (a pattern that looks better, a once-seen workaround) is filed first as a candidate learning, not a skill edit: in a PAUL project append it to `.paul/LEARNINGS.md` with a `candidate` status (date, evidence, rule); elsewhere write it to `.paul/learnings/inbox/` following the repo's Self-Improvement Protocol when that structure exists, else the project's `LEARNINGS.md` backlog. Promote a filed learning to a skill edit only after validation evidence exists — a passing check, an explicit user or reviewer confirmation, or three independent occurrences with the same cause — flipping its status to `validated` when you do. Never promote on reflection alone.

For each approved Accepted item, follow the Routing field exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): parent does directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): hand to your harness's skill-authoring skill and run its draft / test / iterate loop. That is `create-skill` in Cursor (built in) or Anthropic's `skill-creator`. If you have neither, follow the Agent Skills format at agentskills.io. "`create-skill`" below means whichever of these you use.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): hand to `create-skill` and run its description-optimization loop.
- `new skill via create-skill: <kebab-name>`: hand creation to `create-skill`. Do not invent the shape ad hoc.
- Rule-shaped, cross-skill item (applies beyond one skill, phrased as "always/never do X when Y"): stage it with `carl_v2_stage_proposal` (`source: decisions`, rationale citing the evidence). Staging is not application — `carl_v2_approve_proposal` runs only on the user's yes, bundled with the same approval. A context-bound judgment ("we chose X for this project") goes to `carl_v2_log_decision` after that yes. Skip when the carl MCP is absent.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done. Skip this step if it doesn't.

### 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
