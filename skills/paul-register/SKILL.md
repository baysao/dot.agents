---
name: paul-register
description: Generate paul.json for a legacy PAUL project. Use when the satellite manifest is missing.
metadata:
  opencode/slash: "true"
---

## Purpose

Generate `.paul/paul.json` for an existing project that has a `.paul/` directory but no satellite manifest.

Use it for projects initialized before paul-framework v1.1. Required for BASE satellite auto-detection to discover and register the project.

## Input

No input required — it inspects the current directory for `.paul/` and an existing `paul.json`.

Example: `Use paul-register: register this project`

## Key Concepts

### Framework Source of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, read the same subpaths under `~/.agents/paul-framework/`. If neither exists, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/register-manifest.md` — workflow to follow

## Application

1. Check the current directory for `.paul/` and an existing `paul.json`.
2. Follow `register-manifest.md` to generate `.paul/paul.json` with the correct project name and current state.
3. Verify success criteria:
   - [ ] .paul/paul.json created with correct project name and current state
   - [ ] User confirmed BASE will detect the project on next session start

## Examples

### Example: Legacy Adoption

Input: none, in a pre-v1.1 project.

Result: manifest created, BASE detection confirmed for next session.

## Common Pitfalls

- **Running inside a non-PAUL directory.** Consequence: manifest with no backing state. Fix: verify `.paul/` exists first.

## References

- `~/.agents/paul-framework/workflows/register-manifest.md`
