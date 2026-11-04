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

`.paul/config.md` holds project settings, integrations (SonarQube with project_key; Enterprise Plan Audit toggle; pstack status), and preferences (auto_commit, verbose_output).

### pstack Integration

pstack is present when `.paul/pstack-models.md` or the global `~/.agents/pstack-models.md` exists, or the `poteto-mode` skill is invocable in this session. Enabling pstack writes the standard skill preset into `.paul/SPECIAL-FLOWS.md` via the paul-flows `pstack` subcommand and records `pstack: enabled` in config.md. Disabling removes the preset rows and records `pstack: disabled`.

### Effects

Enabling Enterprise Plan Audit inserts an audit prompt between PLAN and APPLY. Enabling SonarQube routes to a first quality-gate scan.

## Application

### Step 1: Show Current State

Check for `.paul/config.md`. If present, display contents and offer: enable/disable integration, view full config, reset to defaults. If absent, offer to create config or cancel.

Also show the debt store's health in the same block when `.paul/DEBT.toml` exists: run `python ~/.agents/paul-framework/scripts/debt.py` and print its counts line. A project can be configured perfectly and still be five overdue rows deep; the config screen is where that is cheap to notice.

### Step 2: Handle Choice

For enable/disable, show integrations (SonarQube, Enterprise Plan Audit, pstack) with status, then Done. For SonarQube enable prompt for project_key; for audit enable inform that audit will be suggested after plan; for pstack enable apply the SPECIAL-FLOWS preset; for disables note the reverted behavior.

### Step 3: Write and Confirm

Create or update `.paul/config.md` (project settings, integrations, preferences blocks with timestamp). Display the CONFIG UPDATED confirmation with integration states and next steps (quality-gate scan if SonarQube newly enabled; audit-between-PLAN-and-APPLY note if audit newly enabled).

Verify output:
- [ ] `.paul/config.md` created or updated
- [ ] Integration status changed as requested
- [ ] Clear next steps shown where applicable

## Examples

### Example: Enable Audit Gate

Input: enable Enterprise Plan Audit.

Result: config updated; plans now prompt for audit before APPLY.

### Example: Enable pstack

Input: enable pstack.

Result: config updated; the pstack skill preset is written into `.paul/SPECIAL-FLOWS.md`; `paul-plan` auto-populates the `<skills>` section and `paul-unify` closes with the reflect pass.

## Common Pitfalls

- **Toggling without telling the loop.** Consequence: user surprised by new audit prompt or missing scan. Fix: always state the workflow effect on change.

## References

- `.paul/config.md`
- `.paul/STATE.md`
