---
name: aegis-audit
description: Run a full or targeted AEGIS diagnostic audit on a codebase. Use to start the Core audit (phases 0-5).
---

## Purpose

Initiate a new AEGIS diagnostic audit on a target codebase. Primary entry point for all Core audit operations: scope selection, domain targeting, tool configuration, confirmation, then Phase 0 delegation.

Routes to init when no `.aegis/` exists, and to resume when an audit is already in progress.

Produces Phase 0 (Context & Threat Modeling) output onward through the phase execution loop.

## Input

Optionally bring the target:

- **Works best with:** a repo path (e.g. `./my-repo`) — otherwise the current working directory
- **Also useful:** nothing else; scope and tools are chosen interactively

If you supply the path inline it validates and proceeds — otherwise it uses cwd.

Example: `Use aegis-audit: audit ./my-repo`

## Key Concepts

### Framework Sources of Truth

- `~/.agents/aegis/core/workflows/phase-0-context.md` through `phase-5-report.md` — phase workflows
- `phase-checkpoint.md` — between-phase gate (Continue / Pause / Abort)
- `session-handoff.md`, `disagreement-resolution.md` — intra-phase mechanics
- Init logic mirrors `aegis-init` (git validation, tool detection, .gitignore)

### State

- `.aegis/STATE.md` — status (initialized / in_progress / paused), current phase, scope, session tracking
- `.aegis/MANIFEST.md` — version-locked framework references

### Scopes

Full (phases 0-5, all 14 domains), Targeted (selected domains; 00 Context always included), Quick scan (phases 0-2 only). Tools default all-on (SonarQube, Semgrep, Trivy, Gitleaks, Checkov, Syft+Grype, git-history); Checkov auto-skips without IaC, git-history/Gitleaks degrade without .git.

## Application

### Step 1: Resolve Target

Use the given path or cwd. Validate it exists and is a directory; warn (not block) when `.git/` is absent. Display for confirmation.

### Step 2: Ensure Initialized

If `.aegis/STATE.md` exists and status is in_progress/paused: show EXISTING AUDIT DETECTED (target, phase, status, finding count) and offer resume / fresh-start (archives state via init logic) / cancel. If no `.aegis/`: run the init process (STATE.md, MANIFEST.md, findings/) first.

### Step 3: Analyze and Configure

Display TARGET REPOSITORY (path, languages, frameworks, size, last commit). Present AUDIT SCOPE (full / targeted with 14-domain checklist / quick / cancel), then AUDIT CONFIGURATION (tool toggles, ok/back).

### Step 4: Confirm and Loop

Display the AUDIT PLAN (target, scope, phases, domains, tools, estimated sessions ~8-10 full, ~4-5 quick). On start: set STATE.md phase 0 + in_progress, record scope/tools, stamp session tracking. Execute phases sequentially, invoking phase-checkpoint after each; honor Continue/Pause/Abort. Final checkpoint reports core-audit complete with report/transform next steps.

Verify success criteria:
- [ ] Target identified and validated
- [ ] Scope defined and confirmed
- [ ] Tool configuration confirmed
- [ ] .aegis/ initialized with STATE.md and MANIFEST.md
- [ ] Phase 0 delegation begins
- [ ] Cancellation available at every decision point

## Examples

### Example: First Run

Input: `./my-repo`, full scope.

Result: initialized project, confirmed plan, Phase 0 executing with per-phase checkpoints.

## Common Pitfalls

- **Starting fresh over an active audit.** Consequence: archived state and lost findings. Fix: always surface the existing-audit gate first.

## References

- `~/.agents/aegis/core/workflows/phase-0-context.md` … `phase-5-report.md`
- `~/.agents/aegis/core/workflows/phase-checkpoint.md`, `session-handoff.md`, `disagreement-resolution.md`
- `.aegis/STATE.md`, `.aegis/MANIFEST.md`
