---
name: paul-init
description: Initialize PAUL in a project via conversational setup. Use when starting PAUL fresh or adding it to a codebase.
metadata:
  opencode/slash: "true"
---

## Purpose

Initialize the `.paul/` structure in a project directory through conversational setup. Creates PROJECT.md, STATE.md, and ROADMAP.md populated from conversation — the user never hand-edits templates.

Use it when starting a new project with PAUL or adding PAUL to an existing codebase.

## Input

No input required. The skill drives the conversation:

- **Works best with:** zero input — just invoke it in the target directory
- **Also useful:** any known project context up front (skips redundant questions)

Example: `Use paul-init: set up PAUL here`

## Key Concepts

### Framework Sources of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, read the same subpaths under `~/.agents/paul-framework/`. If neither exists, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/init-project.md` — setup workflow
- `~/.agents/paul-framework/templates/PROJECT.md` — project template
- `~/.agents/paul-framework/templates/STATE.md` — state template
- `~/.agents/paul-framework/templates/ROADMAP.md` — roadmap template

### Behavior Contract

Ask ONE question at a time and wait. Populate files from answers. End with exactly ONE next action that builds momentum into planning.

## Application

### Step 1: Check Existing

Check for existing `.paul/`. If present, route to resume instead of re-initializing.

### Step 2: Scaffold and Ask

1. Create the directory structure.
2. Ask: "What's the core value this project delivers?"
3. Ask: "What are you building?"
4. Confirm project name (infer from directory).

### Step 3: Populate and Route

Populate PROJECT.md, ROADMAP.md (phases TBD), and STATE.md from answers.

### Step 4: pstack Integration (automatic)

pstack is present when `.paul/pstack-models.md` or the global `~/.agents/pstack-models.md` exists, or the `poteto-mode` skill is invocable in this session. If present, ask ONE question: "pstack detected. Register the pstack skill preset in .paul/SPECIAL-FLOWS.md? (recommended)". On yes, run the paul-flows `pstack` subcommand to write the preset. On no, continue without it.

Display ONE next action: `/paul:plan` (Claude Code; in other harnesses, name the `paul-plan` skill).

Verify success criteria:
- [ ] .paul/ directory created
- [ ] PROJECT.md populated from conversation
- [ ] STATE.md initialized with correct loop position
- [ ] ROADMAP.md initialized
- [ ] pstack preset offered when pstack is present
- [ ] User presented with ONE clear next action

## Examples

### Example: New Project

Input: none.

Result: `.paul/` scaffolded, three files populated from a short Q&A, routed to plan.

## Common Pitfalls

- **Batch-asking all questions at once.** Consequence: thin answers, weak project context. Fix: one question at a time.
- **Letting the user hand-edit templates.** Consequence: malformed frontmatter and drift. Fix: always populate from answers.

## References

- `~/.agents/paul-framework/workflows/init-project.md`
- `~/.agents/paul-framework/templates/PROJECT.md`
- `~/.agents/paul-framework/templates/STATE.md`
- `~/.agents/paul-framework/templates/ROADMAP.md`
