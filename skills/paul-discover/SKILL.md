---
name: paul-discover
description: Decide technical options before planning a phase. Use when library or architecture choices are open.
metadata:
  opencode/slash: "true"
---

## Purpose

Execute discovery to inform planning decisions. Produces `DISCOVERY.md` with findings, recommendation, and confidence level.

Use it before planning a phase with technical unknowns (library selection, architecture decisions, integration approaches).

Distinct from research: research gathers documentation/information; discover makes technical decisions.

## Input

Bring the target:

- **Works best with:** a phase number or topic (e.g. `4`, `auth approach`)
- **Also useful:** known constraints or options under consideration

Example: `Use paul-discover: decide auth approach for phase 4`

## Key Concepts

### Framework Sources of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/discovery.md` — workflow to follow
- `~/.agents/paul-framework/templates/DISCOVERY.md` — discovery template

### Project Context

- `.paul/STATE.md`, `.paul/ROADMAP.md`
- `.paul/DEBT.toml` — a row that names a technical option (which library, which chain, which vendor) is a discovery question that was parked instead of answered

### Debt Rows Become Discovery Questions

Run `python ~/.agents/paul-framework/scripts/debt.py --run-checks` and read the `kind = "decision"` / `kind = "tech"` rows. Each `open` or `overdue` one is a decision the phase inherited: it is already the question, phrased by whoever was blocked. Fold them into the unknowns list rather than discovering around them, and when the recommendation settles one, name the `DEBT-NNN` in `DISCOVERY.md` — the row discharges when the plan applies the choice, not when discovery mentions it.

## Application

1. Determine depth level (quick/standard/deep) and identify unknowns for the phase.
2. Follow `discovery.md`: research options using subagents, cross-verify findings.
3. Create `DISCOVERY.md` (for standard/deep) with recommendation and confidence level.

### pstack Discovery Aids (automatic)

pstack is present when `.paul/pstack-models.md` or the global `~/.agents/pstack-models.md` exists, or the `poteto-mode` skill is invocable in this session. If present, run the poteto-mode **investigation** playbook for read-only questions, the **prototype** playbook to settle design forks empirically instead of asking, and the `arena` skill when two or more designs deserve parallel attempts before a recommendation.

4. Verify success criteria:
   - [ ] Discovery depth determined
   - [ ] Unknowns identified
   - [ ] Options researched with sources
   - [ ] DISCOVERY.md created (for standard/deep)
   - [ ] Recommendation provided with confidence
   - [ ] Ready for plan

## Examples

### Example: Library Decision

Input: `auth approach for phase 4`

Result: DISCOVERY.md comparing options with a confident recommendation feeding the plan.

## Common Pitfalls

- **Discovering without deciding.** Consequence: findings never become a recommendation. Fix: always end with a choice + confidence.

## References

- `~/.agents/paul-framework/workflows/discovery.md`
- `~/.agents/paul-framework/templates/DISCOVERY.md`
- `.paul/STATE.md`, `.paul/ROADMAP.md`
