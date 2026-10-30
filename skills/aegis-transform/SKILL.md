---
name: aegis-transform
description: Run the full AEGIS Transform pipeline (phases 6-8). Use on a completed Core audit.
---

## Purpose

Initiate the full Transform pipeline (Phase 6 remediation → Phase 7 risk validation → Phase 8 execution planning) on a completed Core audit, with explicit scope and safety confirmation first.

Master entry point for Transform. Targeted work uses remediate/playbook/guardrails instead.

Produces Layer B (playbooks, patterns, guardrails) and Layer C (change graph, risk scores, PAUL project). Plans only — nothing touches the codebase without explicit PAUL execution.

## Input

No input required — scope is chosen interactively:

- **Works best with:** zero input; answer full / selective / playbooks-only
- **Also useful:** domain or severity filters when going selective

Example: `Use aegis-transform: transform the completed audit`

## Key Concepts

### Framework Sources of Truth

- `phase-6-remediation.md`, `phase-7-risk-validation.md`, `phase-8-execution-planning.md` — in-sequence delegates
- `transform-safety.md` — automatic safety checkpoints per phase

### Scopes

Full (all findings, phases 6-8), Selective (domain checklist or severity threshold), Playbooks-only (Phase 6, skip 7-8).

## Application

1. Gate on Layer A: no `.aegis/` → NO ACTIVE AUDIT (start-audit/cancel); report missing/incomplete → CORE AUDIT INCOMPLETE (per-phase statuses, resume/cancel).
2. Analyze scope: total/domain/severity/confidence distributions, estimated playbook count, max intervention level; display PIPELINE OVERVIEW.
3. Present TRANSFORM SCOPE (full/selective/playbooks-only/cancel) with domain-count checklist or severity threshold when selective.
4. Require SAFETY REVIEW confirmation (per-level finding counts, confidence summary, plans-only notice) before proceeding; allow scope modification.
5. Execute 6 → (7 → 8 unless playbooks-only), stamping STATE.md at initiation; display TRANSFORM COMPLETE (Layer B/C paths + PAUL-execution next steps).
6. Verify success criteria:
   - [ ] Layer A validated
   - [ ] Scope selected and confirmed
   - [ ] Intervention levels + confidence shown pre-output
   - [ ] Explicit confirmation obtained
   - [ ] Phases run in sequence 6 → 7 → 8
   - [ ] Output locations communicated
   - [ ] Cancellation at every decision

## Examples

### Example: Full Pipeline

Input: full scope confirmed.

Result: playbooks, patterns, guardrails, change graph, risk scores, and PAUL project ready for review.

## Common Pitfalls

- **Skipping the safety confirmation.** Consequence: unexpected Authorizing-level plans. Fix: always show levels and require confirmation.

## References

- `~/.agents/aegis/transform/workflows/phase-6-remediation.md`
- `~/.agents/aegis/transform/workflows/phase-7-risk-validation.md`
- `~/.agents/aegis/transform/workflows/phase-8-execution-planning.md`
- `~/.agents/aegis/transform/workflows/transform-safety.md`
- `.aegis/STATE.md`, `.aegis/report/`, `.aegis/findings/`
