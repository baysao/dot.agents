---
name: aegis-validate
description: Test AEGIS framework and tool installation read-only. Use anytime to diagnose setup.
---

## Purpose

Test the AEGIS installation by verifying framework files, commands, and each OSS analysis tool. Reports pass/fail per component with fix guidance.

Read-only — never modifies files or installs anything. Safe to run anytime.

## Input

No input required. Inspects `~/.agents/aegis/`, `~/.agents/commands/aegis/`, tool binaries, and local `.aegis/STATE.md` when present.

Example: `Use aegis-validate: check my setup`

## Key Concepts

### Standalone

No workflow delegation.

### Detection Order

PATH first, then `~/.local/share/aegis/venvs/{tool}` for Python tools (Semgrep, Checkov); SonarQube passes on ANY of native CLI / Docker scanner image / Docker server container / localhost:9000.

## Application

1. Verify framework dirs (`~/.agents/aegis/` with domains/schemas/rules/tools/core/transform counts; `~/.agents/commands/aegis/` command list); on absence suggest install.sh.
2. Test each tool in order — Semgrep, Trivy, SonarQube (4 checks), Gitleaks, Checkov, Syft, Grype, Git — recording version + location or the specific reinstall hint.
3. If local `.aegis/STATE.md` exists, report project name/status/phase and configured tools; otherwise skip silently.
4. Display the Validation Report (framework ✓/✗, per-tool ✓/✗ + version, pass count, troubleshooting block on failures, project line when present).
5. Verify success criteria:
   - [ ] Framework + commands verified
   - [ ] All 7 OSS tools + git tested
   - [ ] Venv paths checked for Python tools
   - [ ] Docker/localhost SonarQube modes covered
   - [ ] Per-tool pass/fail with fixes
   - [ ] Project state shown when present

## Examples

### Example: Post-Install Check

Input: none.

Result: pass/fail table (e.g. 7/8 available) with targeted fix lines.

## Common Pitfalls

- **Checking only PATH for venv tools.** Consequence: false negatives for Semgrep/Checkov. Fix: always probe the venv fallback.

## References

- `~/.agents/aegis/`, `~/.agents/commands/aegis/`
- `.aegis/STATE.md`
