---
name: aegis-report
description: Generate or view the AEGIS diagnostic report. Use on a completed Core audit (phases 0-4).
---

## Purpose

Generate, regenerate, or display the final AEGIS diagnostic report (executive-summary.md, findings-by-domain.md, disagreements.md, remediation-roadmap.md in `.aegis/report/`).

Requires phases 0-4 complete (Phase 5 is what this triggers). Existing reports offer view / section-view / regenerate.

## Input

Optionally bring a section:

- **Works best with:** a section name (e.g. `executive-summary`) for single-section generation — otherwise full report
- **Also useful:** nothing else; state resolves from `.aegis/STATE.md`

Example: `Use aegis-report: executive-summary`

## Key Concepts

### Framework Source of Truth

- `~/.agents/aegis/core/workflows/phase-5-report.md` — generation delegate

## Application

1. If no `.aegis/STATE.md`: show NO ACTIVE AUDIT with start-audit / cancel.
2. Verify phases 0-4 complete from STATE.md; if gaps, show AUDIT INCOMPLETE (per-phase statuses + incomplete list) with resume / cancel.
3. If `.aegis/report/` exists: show EXISTING REPORT FOUND (timestamp, per-file exists/missing) with view-all / view-section (4-way selector) / regenerate / cancel.
4. On generate: confirm scope (full vs single section, finding/disagreement/domain counts), delegate to phase-5-report, then show REPORT GENERATED (location, files, transform/archival next steps).
5. Verify success criteria:
   - [ ] Prerequisites validated
   - [ ] Existing report options presented
   - [ ] Phase 5 workflow delegated
   - [ ] Report files created
   - [ ] Next steps communicated
   - [ ] Cancellation at every decision

## Examples

### Example: Full Report

Input: none, phases 0-4 complete, no report yet.

Result: four report files generated with transform as the next step.

## Common Pitfalls

- **Generating over incomplete phases.** Consequence: report synthesizes gaps as findings. Fix: enforce the 0-4 gate.

## References

- `~/.agents/aegis/core/workflows/phase-5-report.md`
- `.aegis/STATE.md`, `.aegis/report/`
