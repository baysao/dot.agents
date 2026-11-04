---
name: paul-register
description: Generate paul.json for a legacy PAUL project. Use when the satellite manifest is missing.
metadata:
  opencode/slash: "true"
---

## Purpose

Generate `.paul/paul.json` for an existing project that has a `.paul/` directory but no satellite manifest.

Use it for projects initialized before paul-framework v1.1. Creates the `paul.json` satellite manifest so PAUL commands can find this project's `.paul/` directory.

## Input

No input required — it inspects the current directory for `.paul/` and an existing `paul.json`.

Example: `Use paul-register: register this project`

## Key Concepts

### Framework Source of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/register-manifest.md` — workflow to follow
- `~/.agents/paul-framework/templates/DEBT.toml.md` — debt store schema (the store is created here if absent)

## Application

1. Check the current directory for `.paul/`, an existing `paul.json`, and `.paul/DEBT.toml`.
2. Follow `register-manifest.md` to generate `.paul/paul.json` with the correct project name and current state. A legacy project predates the debt store, so create `.paul/DEBT.toml` here too if it is missing (header comment + `Schema:` pointer to `~/.agents/paul-framework/templates/DEBT.toml.md`, no rows). A registered project without a store is one where the first deferral has nowhere to go and ends up as prose.
3. Verify success criteria:
   - [ ] .paul/paul.json created with correct project name and current state
   - [ ] Manifest written and readable by PAUL commands
   - [ ] `.paul/DEBT.toml` exists and parses with `debt.py` (created empty if absent)

## Examples

### Example: Legacy Adoption

Input: none, in a pre-v1.1 project.

Result: manifest created and PAUL commands can resolve this project.

## Common Pitfalls

- **Running inside a non-PAUL directory.** Consequence: manifest with no backing state. Fix: verify `.paul/` exists first.

## References

- `~/.agents/paul-framework/workflows/register-manifest.md`
