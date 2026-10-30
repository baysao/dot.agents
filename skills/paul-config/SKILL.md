---
name: paul-config
description: Manage PAUL project configuration and integrations. Use to enable, disable, or view settings.
metadata:
  opencode/slash: "true"
---

## Purpose

Manage PAUL project configuration and integrations by creating or updating `.paul/config.md` at any point in the lifecycle.

Use it to enable SonarQube after init, disable an integration, view current configuration, or change project settings.

## Input

No input required — the skill shows current state and offers choices:

- **Works best with:** zero input; answer the prompts (view, enable/disable, reset)
- **Also useful:** project_key for SonarQube (defaults to directory name)

Example: `Use paul-config: enable SonarQube`

## Key Concepts

### Config File

`.paul/config.md` holds project settings, integrations (SonarQube with project_key; Enterprise Plan Audit toggle; pstack, BASE status), and preferences (auto_commit, verbose_output).

### pstack Integration

pstack is present when `.paul/pstack-models.md` or the global `~/.agents/pstack-models.md` exists, or the `poteto-mode` skill is invocable in this session. Enabling pstack writes the standard skill preset into `.paul/SPECIAL-FLOWS.md` via the paul-flows `pstack` subcommand and records `pstack: enabled` in config.md. Disabling removes the preset rows and records `pstack: disabled`.

### BASE Integration

BASE is present when the `base` CLI resolves (or `~/.base-gbl/` exists). Enabling bootstraps project-scoped context: run `base scaffold` in the project root (creates `.base/` workspace with graph, domains.toml, base.toml), create a project domain named after the project with a path trigger to `.paul/`, add default PAUL-loop rules (unify→base learn/decision/rule, resume→base recall), and register BASE star-commands (`*base`, `*end`) for session sweep. Project workspace tier overlays global; hooks merge scopes on read. Disabling records `base: disabled` in config.md; the `.base/` directory stays for manual removal.

### Effects

Enabling Enterprise Plan Audit inserts an audit prompt between PLAN and APPLY. Enabling SonarQube routes to a first quality-gate scan. Enabling BASE scaffolds `.base/` workspace, creates project domain with `.paul/` path trigger, adds PAUL-loop rules, and registers BASE star-commands for session sweep.

## Application

### Step 1: Show Current State

Check for `.paul/config.md`. If present, display contents and offer: enable/disable integration, view full config, reset to defaults. If absent, offer to create config or cancel.

### Step 2: Handle Choice

For enable/disable, show integrations (SonarQube, Enterprise Plan Audit, pstack, BASE) with status, then Done. For SonarQube enable prompt for project_key; for audit enable inform that audit will be suggested after plan; for pstack enable apply the SPECIAL-FLOWS preset; for BASE enable run `base scaffold` in project root, create project domain with `.paul/` path trigger, add PAUL-loop rules (unify/resume), and register BASE star-commands; for BASE disable note that project context stops injecting; for disables note the reverted behavior.

### Step 3: Write and Confirm

Create or update `.paul/config.md` (project settings, integrations, preferences blocks with timestamp). Display the CONFIG UPDATED confirmation with integration states and next steps (quality-gate scan if SonarQube newly enabled; audit-between-PLAN-and-APPLY note if audit newly enabled; BASE workspace scaffolded and PAUL-loop rules active if BASE newly enabled).

Verify output:
- [ ] `.paul/config.md` created or updated
- [ ] Integration status changed as requested
- [ ] Clear next steps shown where applicable

## Examples

### Example: Enable Audit Gate

Input: enable Enterprise Plan Audit.

Result: config updated; plans now prompt for audit before APPLY.

### Example: Enable BASE

Input: enable BASE.

Result: config updated; `base scaffold` runs in project root, project domain created with `.paul/` path trigger, PAUL-loop rules added (unify→base learn/decision/rule, resume→base recall), BASE star-commands registered; `paul-unify` and `paul-resume` now integrate with base graph.

## Common Pitfalls

- **Toggling without telling the loop.** Consequence: user surprised by new audit prompt or missing scan. Fix: always state the workflow effect on change.

## References

- `.paul/config.md`
- `.paul/STATE.md`
