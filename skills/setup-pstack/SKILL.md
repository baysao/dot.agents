---
name: setup-pstack
description: Configure which models pstack uses per role and at what reasoning budget. Detects your available models and writes an always-applied rule that overrides the skill defaults. Use for /setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices.
metadata:
  opencode/slash: "true"
---

# Setup pstack

Write pstack's model settings, one model per role:

- **PAUL project** (a `.paul/` directory exists): `.paul/pstack-models.md` — project-level, versioned with the project. Write this file, not the global one, and treat it as *the* settings file for every harness in this project.
- **Cursor** (no `.paul/`): `~/.cursor/rules/pstack-models.mdc`, an always-applied rule.
- **Every other harness** (no `.paul/`; Claude Code, Codex, Pi, OpenCode, Kilo Code, Cline, and others): `~/.agents/pstack-models.md`. These harnesses don't load Cursor rules, so pstack skills read this file when they pick a model. In OpenCode you also register the file in `instructions` (step 5) so every session loads it the way Cursor loads its rule; in Cline and Kilo Code a one-line pointer in their always-loaded AGENTS.md does the same.

"The settings file" below means `.paul/pstack-models.md` when the project has one, else the file for your harness. When reading, check `.paul/pstack-models.md` first, then the harness path, and use the first that exists.

## Steps

### 1. Detect available models

Enumerate the model slugs you can pass to a subagent in this session (Cursor `Task`, Claude Code `Agent`, OpenCode and Kilo Code `task`, Codex and Cline `spawn_agent`). That is the dependable source. If your harness also has a command that lists the user's models, prefer it for completeness (for example `opencode models` or `pi --list-models`). OpenCode lists `provider/model` slugs (`anthropic/claude-opus-4-5`) with no effort token in them; write them exactly as printed. Kilo Code slugs are `provider/model` too (`anthropic/claude-haiku-4-20250514`, `kilo-auto/free`). If a harness cannot select a model per subagent (Cline's `spawn_agent` has no model parameter or per-agent config), say so when you present the mapping in step 3(c). If you cannot detect any, ask the user to paste the slugs they have access to. Never write a real slug you have not confirmed is available. The aliases `inherit-parent` and `auto` are always valid even though they are not detected slugs.

### 2. Load current state

The default role-to-model mapping is the rule shape shown in step 5 below. If the settings file already exists, read it and treat its `# budget` line and its role values as the current choices. Otherwise start from those defaults.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Prefer your structured-question tool (`AskQuestion` in Cursor, `AskUserQuestion` in Claude Code, `question` in OpenCode and Kilo Code, `ask_followup_question` in Cline) over free text. Offer these four options with these exact labels, and name the current budget when the rule records one.

- `unlimited — keep max`
- `large — xhigh reasoning`
- `medium — high reasoning`
- `small — medium reasoning`

**(b) Apply it.** Build the working table from the skill defaults, and on a re-run keep any role you changed by family, list, or alias (`inherit-parent`, `auto`). `unlimited` leaves every effort as in that table. `large`, `medium`, and `small` set the effort token of every real slug, panel entries included, to `xhigh`, `high`, or `medium`. The effort token is the last token, or the one before a trailing `fast`, on the ladder `max` > `xhigh` > `high` > `medium` > `low`. If the result is not a detected slug, use the same family's detected slug with the highest effort at or below the target, else mark the role as needing a choice. `inherit-parent` and `auto` do not change. So `small` turns `claude-fable-5-1-thinking-max` into `claude-fable-5-1-thinking-medium`, and `grok-4.6-fast-xhigh` into `cursor-grok-4.6-medium-fast` when only that form is detected. If the detected slugs carry no effort token (OpenCode's bare `provider/model`), leave them unchanged, keep the target effort on the `# budget` line only, and express it on the pins (step 5) as the model's variant or a provider option such as `reasoningEffort: high` where the provider accepts one.

**(c) Show the roles and confirm.** Show every role with its model, marking any real slug not in the detected set as needing a choice. Ask whether to accept as-is or change specific roles, offering the detected models plus `inherit-parent` and `auto` (both mean: this role runs on the parent chat model, which is how Auto users stay on Auto) as the options. Prefer your structured-question tool over free text. For panel roles (arena runners, architect runners, interrogate reviewers) the value is a list, and one subagent runs per entry, alias entries included, so the list length sets the count. `arena cross-judge pool` is also a list, but Arena selects one value from it whose model family differs from the parent's when possible. `swarm workers` is the default model for every worker unless a race or comparison assigns another model per arm.

### 4. Validate

Every real slug written must be in the detected set. `inherit-parent` and `auto` always pass. If a chosen real slug is not available, stop and ask again.

### 5. Write the rule

Write the settings file with a `# budget` line with the chosen label and its target effort, and one line per role, using the same labels poteto-mode uses. In a PAUL project, write `.paul/pstack-models.md` without frontmatter and don't touch the global file. Otherwise, in Cursor include the frontmatter below with `alwaysApply: true`; in other harnesses write `~/.agents/pstack-models.md` without the frontmatter (start at the first `#` line). Overwrite the whole file so re-runs stay idempotent. Shape:

```
---
description: pstack per-role model choices (overrides skill defaults)
alwaysApply: true
---
# pstack model configuration. One line per role. Delete a line to fall back to the skill default.
# `inherit-parent` or `auto` as a value: the role runs on the parent chat model (omit the subagent `model`). Alias entries in a panel list still count toward its fan-out.
# budget: unlimited (max)
feature, refactoring: grok-4.6-fast-xhigh
bug-fix: grok-4.6-fast-xhigh
perf-issue: grok-4.6-fast-xhigh
hillclimb: grok-4.6-fast-xhigh
judgment and prose: claude-fable-5-1-thinking-max
hardest tasks: claude-fable-5-1-thinking-max
how explorer: grok-4.6-fast-xhigh
how explainer: claude-fable-5-1-thinking-max
why investigators: grok-4.6-fast-xhigh
why synthesizer: claude-fable-5-1-thinking-max
reflect tooling: gpt-5.6-sol-max
reflect judgment, divergent, synthesizer: claude-fable-5-1-thinking-max
arena runners: claude-fable-5-1-thinking-max, gpt-5.6-sol-max, grok-4.6-fast-xhigh, claude-opus-5-thinking-xhigh
arena cross-judge pool: claude-fable-5-1-thinking-max, gpt-5.6-sol-max, grok-4.6-fast-xhigh, claude-opus-5-thinking-xhigh
swarm workers: grok-4.6-fast-xhigh
architect runners: claude-fable-5-1-thinking-max, gpt-5.6-sol-max, grok-4.6-fast-xhigh, claude-opus-5-thinking-xhigh
interrogate reviewers: claude-fable-5-1-thinking-max, gpt-5.6-sol-max, grok-4.6-fast-xhigh, claude-opus-5-thinking-xhigh
```

**Extras by harness.** Extra writes beyond the settings file:

1. **Register the settings file where the harness always loads instructions.** Register the file you wrote — `.paul/pstack-models.md` in a PAUL project (project-relative path), else the global file. OpenCode: add it to the `instructions` array — `\".paul/pstack-models.md\"` in the project's `opencode.json` for a PAUL project, the absolute global path in `~/.config/opencode/opencode.json` otherwise — creating `{\"instructions\": [...]}` when absent, never duplicating the entry. Cline and Kilo Code: append this line once to the appropriate always-loaded AGENTS.md — the project `AGENTS.md` in a PAUL project, else `~/.agents/AGENTS.md` for Cline (Kilo: project only, with the user's go-ahead): `pstack models: read the settings file (.paul/pstack-models.md or ~/.agents/pstack-models.md) and use its role lines when picking models.` Cursor in a PAUL project: write the project rule `.cursor/rules/pstack-models.mdc` with `alwaysApply: true` and a single pointer line, `Read .paul/pstack-models.md and use its role lines when picking models.`, so the settings load every session without duplicating them. In every case pstack skills still read the settings file directly when no pointer exists.
2. **Write model pins (OpenCode and Kilo Code).** Their `task` tools have no `model` parameter: a spawned subagent runs on the model in its own config, so per-spawn model choice needs a pinned subagent. For every distinct real slug in the mapping, write `~/.config/opencode/agents/pstack-<id>.md` (OpenCode) or `~/.config/kilo/agents/pstack-<id>.md` (Kilo Code), where `<id>` is the slug lowercased with every run of non-alphanumerics replaced by `-` (`anthropic/claude-opus-4-5` → `pstack-anthropic-claude-opus-4-5`):

   ```
   ---
   description: pstack pin for anthropic/claude-opus-4-5
   mode: subagent
   model: anthropic/claude-opus-4-5
   ---
   Follow the task prompt you are given. It carries this role's full instructions.
   ```

   Add the budget's effort as an extra frontmatter option (for example `reasoningEffort: xhigh`) only when the provider accepts one. Skip pins for `inherit-parent` and `auto` — those roles spawn the built-in `general` subagent with no pin. Overwrite pins on re-run; stale `pstack-*.md` files from earlier runs are never referenced and can be deleted.
3. **Cline gets no pins.** Cline supports neither a model parameter on `spawn_agent` nor per-agent model config, so skip pin writes there and restate in step 3(c) that panels will run on the session model.

### 6. Confirm

Tell the user which file was written: `.paul/pstack-models.md` in a PAUL project (commit it so the team and future sessions share it), or the Cursor rule / `~/.agents/pstack-models.md` elsewhere. The registration (OpenCode `instructions`, AGENTS.md pointer, or the Cursor pointer rule in PAUL projects) loads it every session; pstack skills read the settings file directly when nothing registers it. The `pstack-*` pins under `~/.config/opencode/agents/` or `~/.config/kilo/agents/` let `task` spawn each configured model; Cline has no pins and panels there run on the session model. Re-running this skill updates it.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /create-verification-skill." On yes, invoke `/create-verification-skill` (resolves wherever pstack is installed: workspace, user, or plugin). On no, move on without pushing.

### 8. Wire into PAUL (automatic)

If the workspace contains `.paul/STATE.md`, offer once: "PAUL project detected. Register the pstack skill preset so /paul:plan and /paul:apply use these skills automatically?" On yes, invoke the paul-flows skill with the `pstack` subcommand to write `.paul/SPECIAL-FLOWS.md`.
