---
name: aegis-init
description: Initialize AEGIS state in a target project. Use once per repo before auditing.
---

## Purpose

Initialize AEGIS in a target project by creating the `.aegis/` structure (STATE.md, MANIFEST.md, findings/) with tool inventory and .gitignore entry.

Setup only — never starts an audit. Run `aegis-audit` after init to begin. Existing `.aegis/` offers resume / fresh-start / cancel.

## Input

Optionally bring the target:

- **Works best with:** a repo path — otherwise the current working directory
- **Also useful:** nothing else

Example: `Use aegis-init: set up AEGIS here`

## Key Concepts

### Standalone

No workflow delegation. All logic lives in this skill.

### State Files

STATE.md tracks target, overall status (`initialized`), all six phases pending, resume pointer (`Run /aegis:audit`), and empty session/checkpoint history. MANIFEST.md records framework version/paths plus per-tool detection (PATH, `~/.local/share/aegis/venvs/{tool}`, Docker image for SonarQube).

## Application

1. Resolve target (given path or cwd); validate directory; warn-and-confirm when `.git/` is absent.
2. If `.aegis/STATE.md` exists: show EXISTING PROJECT DETECTED (status, phase, timestamp) with resume / fresh-start (rename to `.aegis-backup-{timestamp}/`) / cancel.
3. Create `.aegis/` with STATE.md, MANIFEST.md, findings/; detect tools into MANIFEST.md.
4. Update `.gitignore` (append `.aegis/` block if missing; create file if absent) and report.
5. Display the initialized summary (target, state, manifest, tool count) with validate → audit next steps.
6. Verify success criteria:
   - [ ] Target identified and validated
   - [ ] Existing .aegis/ handled
   - [ ] .aegis/ created with STATE.md, MANIFEST.md, findings/
   - [ ] Tool inventory recorded
   - [ ] .aegis/ added to .gitignore

## Examples

### Example: New Repo

Input: none (cwd is the repo).

Result: scaffolded `.aegis/`, 8-tool inventory, routed to validate then audit.

## Common Pitfalls

- **Re-initializing over an active audit.** Consequence: lost findings. Fix: always offer resume/fresh/cancel first.

## References

- `.aegis/STATE.md`, `.aegis/MANIFEST.md`
