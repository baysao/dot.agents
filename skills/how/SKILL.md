---
name: how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation."
disable-model-invocation: true
metadata:
  opencode/slash: "true"
---

# How

Explore the codebase to answer "how does X work?" questions. Produce architectural explanations at the level of a senior engineer onboarding onto a subsystem, enough to build a working mental model, not so much that it reads like annotated source code.

## Step 1. Assess Complexity

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

- **Simple** (a single module, a small utility, a narrow question such as "how does function X work"): no explorers. One explainer explores and explains in a single pass. Go to Step 2b.
- **Complex** (a subsystem spanning multiple files or services, a cross-cutting feature, a full architectural overview): spawn parallel explorers first, then hand off to the explainer. Go to Step 2a.

When in doubt, take the simple path.

**base AST first.** When the `base` binary resolves, explorers and explainers run `base ast query` (`-c`, `-f`, `--calls`) for every named symbol before reading files. The map answers placement and ownership; file reads confirm behavior. Run `base sync --ast` first when the map may be stale.

**Other harnesses.** The spawns in this skill use Cursor's `Task` tool. In another harness, use its subagent tool: `Agent` in Claude Code (`subagent_type: general-purpose`), `task` in OpenCode and Kilo Code (`subagent_type: general`), `spawn_agent` in Codex and in Cline. Keep the prompt and, where your tool accepts one, the model. Drop parameters your tool doesn't have. If your harness has no subagent tool, as in Pi without an extension, run each role yourself, one after another. "Your configured ... model" means the matching line in the pstack settings file. Cursor loads `~/.cursor/rules/pstack-models.mdc` automatically. In OpenCode and other harnesses, read `~/.agents/pstack-models.md` if it exists. In any harness, `.paul/pstack-models.md` wins when the project has one.

**OpenCode / Kilo Code.** Their `task` tool takes only `description` (3-5 words), `prompt`, and `subagent_type` — no `model` or `readonly` — so send all calls in one message to run them concurrently and drop the rest (Kilo's `task` also accepts `background: true`). Their built-in read-only `explore` subagent fits a readonly role running on the parent model. To run a configured model, spawn its pin: `subagent_type: pstack-<id>`, `<id>` being the slug lowercased with each non-alphanumeric run replaced by `-` (`grok-4.6-fast-xhigh` → `pstack-grok-4-6-fast-xhigh`). `/setup-pstack` writes the pins under `~/.config/opencode/agents/` (OpenCode) or `~/.config/kilo/agents/` (Kilo Code); create one before spawning if it is missing (`mode: subagent`, `model: <slug>`, body: follow the task prompt). For `inherit-parent`/`auto`, spawn `subagent_type: general` with no pin. **Cline.** Subagents come from `spawn_agent` (CLI and Desktop only, not the IDE extensions) and run on the session's model — no model parameter, no per-agent model config. Run the panel on the session model and tell the user the cross-model signal is gone.

## Step 2a. Explore (complex questions only)

Decompose the question into 2 to 4 exploration angles, each a distinct slice of the subsystem. Spawn all explorers in a single message:

- `subagent_type`: `generalPurpose`
- `model`: your configured how-explorer model (default `grok-4.6-fast-xhigh`)
- `readonly`: `true`

Each explorer gets the prompt in `references/explorer-prompt.md` with its angle filled in. Then go to Step 3.

## Step 2b. Direct Explain (simple questions)

Spawn one Task subagent that explores and explains in one pass:

- `subagent_type`: `generalPurpose`
- `model`: your configured how-explainer model (default `claude-fable-5-1-thinking-max`)
- `readonly`: `true`

Build its prompt from `references/explainer-prompt.md` without the explorer-findings section. Go to Step 4.

## Step 3. Synthesize (complex questions only)

Once all explorers have returned, spawn one Task subagent to synthesize their findings into one explanation:

- `subagent_type`: `generalPurpose`
- `model`: your configured how-explainer model (default `claude-fable-5-1-thinking-max`)
- `readonly`: `true`

Build its prompt from `references/explainer-prompt.md` with every explorer's findings filled in.

## Step 4. Present

Present the explainer's output to the user. Light edits for clarity or context from the conversation are fine. Do not substantially rewrite it.

## Output Format

The explanation uses the sections defined in `references/explainer-prompt.md`, dropping any that do not apply: Overview, Key Concepts, How It Works, Where Things Live, Gotchas.
