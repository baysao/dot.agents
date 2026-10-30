---
name: aegis-guardrails
description: Generate AI-assistant rules from remediation patterns. Use after audit + remediation complete.
---

## Purpose

Generate machine-enforceable project rules (Claude MD and/or Cursor rules in `.aegis/remediation/guardrails/`) encoding audit-derived practices as persistent guardrails.

Requires Layer A (`.aegis/report/`) AND Layer B (`.aegis/remediation/playbooks/`) — guardrails derive from remediation patterns, not raw findings. Advisory (Suggesting) level: rules suggest constraints; enforcement depends on the assistant.

## Input

Optionally bring a format:

- **Works best with:** `claude`, `cursor`, or both — otherwise chosen interactively
- **Also useful:** nothing else

Example: `Use aegis-guardrails: both`

## Key Concepts

### Framework Sources of Truth

- `phase-7-risk-validation.md` — guardrail-generator delegate
- `transform-safety.md` — automatic validation

### Outputs

`claude-md-rules.md` (for `.claude/CLAUDE.md`) and `cursorrules.md` (for `.cursorrules`) — review in place, then copy relevant sections to the project root and customize.

## Application

1. Gate Layer A (missing report → CORE AUDIT INCOMPLETE with resume/cancel), then Layer B (missing playbooks → REMEDIATION REQUIRED with remediate-first/cancel).
2. Resolve format (argument pre-select or 4-way: claude / cursor / both / cancel); display GUARDRAIL SCOPE (playbook, pattern, domain counts + what gets codified).
3. Require SAFETY REVIEW confirmation (Suggesting level, pattern counts, no-codebase-changes notice).
4. If guardrail files exist: show EXISTING GUARDRAILS FOUND (per-file status) with view / regenerate / back / cancel.
5. Delegate to the phase-7 guardrail-generator, then show GUARDRAILS GENERATED (files, copy-to-root instructions, transform/Phase-8 next steps).
6. Verify success criteria:
   - [ ] Layer A + B validated
   - [ ] Format selected
   - [ ] Scope displayed
   - [ ] Intervention level shown
   - [ ] Explicit confirmation obtained
   - [ ] Existing guardrails handled
   - [ ] Phase 7 delegated
   - [ ] Usage instructions provided
   - [ ] Cancellation at every decision

## Examples

### Example: Both Formats

Input: `both`.

Result: reviewed guardrail pair ready to copy into project root.

## Common Pitfalls

- **Generating from raw findings.** Consequence: unvalidated rules. Fix: enforce the Layer B prerequisite.

## References

- `~/.agents/aegis/transform/workflows/phase-7-risk-validation.md`
- `~/.agents/aegis/transform/workflows/transform-safety.md`
- `.aegis/STATE.md`, `.aegis/remediation/`, `.aegis/remediation/guardrails/`
