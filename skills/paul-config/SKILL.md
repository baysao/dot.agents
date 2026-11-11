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

`.paul/config.md` holds project settings, integrations (SonarQube with project_key; Enterprise Plan Audit toggle; Security Audit toggle with default_profile; XERJ discovery toggle with index_prefix + index_root + index_cwd + binary_path; pstack status), and preferences (auto_commit, verbose_output).

### pstack Integration

pstack is present when `.paul/pstack-models.md` or the global `~/.agents/pstack-models.md` exists, or the `poteto-mode` skill is invocable in this session. Enabling pstack writes the standard skill preset into `.paul/SPECIAL-FLOWS.md` via the paul-flows `pstack` subcommand and records `pstack: enabled` in config.md. Disabling removes the preset rows and records `pstack: disabled`.

### Effects

Enabling Enterprise Plan Audit inserts an audit prompt between PLAN and APPLY. Enabling SonarQube routes to a first quality-gate scan. Enabling Security Audit makes trust-surface plans name a guidance-mode review and turns confirmed critical/high findings into phase-exit debt rows; the profile sets how wide a default run is scoped. With both audit toggles on, `/paul:audit` offers architectural, security, or both — security findings land as debt rows, never as plan edits. Enabling XERJ makes `paul-map` index the tree once and answer planning questions with searches + `path:line` passage citations before Explore agents spawn; `index_prefix` is asked for and stored at enable time (never defaulted) because omitting it on a query searches the shared `ax` and misses the project; `index_cwd` + `index_root` make the index command replayable; `binary_path` adds the CLI when `xerj` is not on PATH. **Every step that writes source re-indexes before reporting success** — `apply-phase` after its tasks, `debug` after its fix, `verify-work` after UAT fixes; `.paul/`-only writes are exempt.

## Application

### Step 1: Show Current State

Check for `.paul/config.md`. If present, display contents and offer: enable/disable integration, view full config, reset to defaults. If absent, offer to create config or cancel.

Also show the debt store's health in the same block when `.paul/DEBT.toml` exists: run `python ~/.agents/paul-framework/scripts/debt.py` and print its counts line. A project can be configured perfectly and still be five overdue rows deep; the config screen is where that is cheap to notice.

### Step 2: Handle Choice

For enable/disable, show integrations (SonarQube, Enterprise Plan Audit, Security Audit, XERJ, pstack) with status, then Done. For SonarQube enable prompt for project_key; for audit enable inform that audit will be suggested after plan; for Security Audit enable ask for the default profile (`quick`/`standard`/`deep`) and note that a POSIX host is required to validate audit output; for XERJ enable **prompt for `index_prefix` and store it (never default it — suggest `<repo-dir>-<project-dir>`, e.g. `akka-pricehub`)**, prompt for `index_root` (default `.`, or a path such as `.\pricehub` when indexing a subfolder) **and store `index_cwd`, the absolute directory autoindex runs from (default: the shell cwd being indexed)**, probe `xerj --version` (using `binary_path` when not on PATH) and offer to run `cd <index_cwd> && xerj autoindex --prefix <prefix> <index_root>` now; for pstack enable apply the SPECIAL-FLOWS preset; for disables note the reverted behavior.

### Step 3: Write and Confirm

Create or update `.paul/config.md` (project settings, integrations, preferences blocks with timestamp). Display the CONFIG UPDATED confirmation with integration states and next steps (quality-gate scan if SonarQube newly enabled; audit-between-PLAN-and-APPLY note if audit newly enabled; guidance-vs-full-audit note and the POSIX validator caveat if Security Audit newly enabled).

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

### Example: Enable Security Audit

Input: enable Security Audit, default profile `standard`.

Result: config updated; trust-surface plans name a guidance-mode review; `/paul:security` defaults to a `standard` diff-scoped run; confirmed critical/high findings land as `blocking = "phase-NN-exit"` rows.

### Example: Enable XERJ

Input: enable XERJ, prefix `akka-pricehub`, index root `.\pricehub`.

Result: config updated with `index_prefix: akka-pricehub` and `index_root: ".\pricehub"`; `/paul:map` runs `xerj autoindex --prefix akka-pricehub .\pricehub` then answers mapping questions with cited passages before any Explore agent spawns; `/paul:research --codebase` and `load_context` query with `--prefix akka-pricehub`. Re-running the same autoindex line refreshes incrementally.

## Common Pitfalls

- **Toggling without telling the loop.** Consequence: user surprised by new audit prompt or missing scan. Fix: always state the workflow effect on change.

## References

- `.paul/config.md`
- `.paul/STATE.md`
