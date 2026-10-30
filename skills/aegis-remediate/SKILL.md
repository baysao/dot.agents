---
name: aegis-remediate
description: Generate remediation playbooks for all findings or one domain. Use after the Core audit completes.
---

## Purpose

Generate remediation knowledge (Layer B) for all findings or one domain, optionally continuing through risk validation (Phase 7) and execution planning (Phase 8).

Existing remediation offers view / missing-only / regenerate. Produces playbooks, patterns, and optionally risk scores + execution plans.

## Input

Optionally bring a domain:

- **Works best with:** a domain number 0-13 for scoped runs — otherwise all findings
- **Also useful:** nothing else

Example: `Use aegis-remediate: domain 4`

## Key Concepts

### Framework Sources of Truth

- `phase-6-remediation.md` — playbook delegate
- `phase-7-risk-validation.md`, `phase-8-execution-planning.md` — continuation targets
- `transform-safety.md` — automatic validation

### Gates

Requires `.aegis/report/` (completed Layer A) or routes to resume. Invalid domain numbers and empty domains exit early.

## Application

1. If Layer A incomplete: show CORE AUDIT INCOMPLETE with resume / cancel.
2. Resolve scope (validate 0-13 for domain runs; exit when the domain has no findings); display REMEDIATION SCOPE with severity counts.
3. If `.aegis/remediation/` exists: show EXISTING REMEDIATION FOUND (playbook/pattern counts) with view / missing-only / regenerate-all / cancel.
4. Require SAFETY REVIEW confirmation (per-level counts, low-confidence capping note, no-codebase-changes notice).
5. Delegate to phase-6, show REMEDIATION GENERATED (counts + locations), then offer continue 7+8 / 7-only / stop-here / cancel and delegate accordingly.
6. Verify success criteria:
   - [ ] Layer A validated
   - [ ] Scope correctly determined
   - [ ] Existing remediation options presented
   - [ ] Levels shown pre-output
   - [ ] Explicit confirmation obtained
   - [ ] Phase 6 delegated with correct scope
   - [ ] Continuation offered
   - [ ] Cancellation at every decision

## Examples

### Example: Single Domain

Input: `4` with 12 security findings.

Result: domain playbooks generated, continuation offered.

## Common Pitfalls

- **Regenerating everything by default.** Consequence: wasted runs over unchanged findings. Fix: offer missing-only first.

## References

- `~/.agents/aegis/transform/workflows/phase-6-remediation.md`
- `~/.agents/aegis/transform/workflows/phase-7-risk-validation.md`
- `~/.agents/aegis/transform/workflows/phase-8-execution-planning.md`
- `~/.agents/aegis/transform/workflows/transform-safety.md`
- `.aegis/STATE.md`, `.aegis/report/`, `.aegis/findings/`, `.aegis/remediation/`
