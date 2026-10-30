---
name: aegis-playbook
description: Generate a remediation playbook for one finding. Use for targeted single-finding fixes.
---

## Purpose

Generate a remediation playbook for a single finding — both human-readable `.md` and machine-consumable `.yaml` in `.aegis/remediation/playbooks/`.

Most targeted Transform operation. Existing playbooks offer view / regenerate. Requires completed Layer A.

## Input

Bring the finding ID (required):

- **Works best with:** a finding ID (e.g. `F-04-001`) — otherwise it lists IDs for selection
- **Also useful:** nothing else; context resolves from `.aegis/findings/`

Example: `Use aegis-playbook: F-04-001`

## Key Concepts

### Framework Sources of Truth

- `phase-6-remediation.md` — single-finding delegate
- `transform-safety.md` — automatic validation

### Playbook Contents

Root cause, 4-layer remediation strategy (abstract → framework → language → project), before/after examples, educational context, verification steps. Nothing is applied to the codebase.

## Application

1. If no `.aegis/report/`: show CORE AUDIT INCOMPLETE with resume / cancel.
2. Without an ID: show FINDING ID REQUIRED (usage, example, status hint) with list-all-IDs / cancel; validate a given ID against `.aegis/findings/*/` with near-miss suggestions.
3. Display FINDING DETAILS (id, domain, severity, agent, confidence, summary).
4. If the playbook pair exists: show EXISTING PLAYBOOK FOUND with view / regenerate / cancel.
5. Require SAFETY REVIEW confirmation (confidence → intervention level, contents list, no-changes notice), delegate to phase-6 scoped to the finding, then show PLAYBOOK GENERATED (both paths, level, remediate/guardrails next steps).
6. Verify success criteria:
   - [ ] Layer A validated
   - [ ] Finding ID validated
   - [ ] Context displayed
   - [ ] Existing playbook options presented
   - [ ] Intervention level shown pre-generation
   - [ ] Explicit confirmation obtained
   - [ ] Phase 6 delegated single-finding
   - [ ] Both output paths communicated
   - [ ] Cancellation at every decision

## Examples

### Example: Single Fix

Input: `F-04-001`.

Result: `.aegis/remediation/playbooks/F-04-001.md` + `.yaml` ready for review.

## Common Pitfalls

- **Guessing the finding ID.** Consequence: wrong-fix playbook. Fix: validate against findings/ and suggest near misses.

## References

- `~/.agents/aegis/transform/workflows/phase-6-remediation.md`
- `~/.agents/aegis/transform/workflows/transform-safety.md`
- `.aegis/STATE.md`, `.aegis/findings/`, `.aegis/remediation/playbooks/`
