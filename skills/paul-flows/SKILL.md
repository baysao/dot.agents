---
name: paul-flows
description: Configure specialized workflow skill integrations. Use to set up, add, audit, or list skill mappings.
metadata:
  opencode/slash: "true"
---

## Purpose

Configure, amend, or audit specialized skill integrations for a PAUL project (`.paul/SPECIAL-FLOWS.md` + PROJECT.md quick reference).

Use it when setting up skill dependencies for a new project, adding a skill mapping, checking required skills were used in the current phase, or viewing configuration.

## Input

Optionally bring a subcommand:

- **Works best with:** nothing (full interactive configuration), or one of `add`, `audit`, `list`, `pstack`, `uxui`
- **Also useful:** skill name + work-type trigger when using `add`

If you supply a subcommand inline it routes directly; with no input it runs full configuration.

Example: `Use paul-flows: audit`

## Key Concepts

### Framework Sources of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/configure-special-flows.md` — configuration workflow
- `~/.agents/paul-framework/references/specialized-workflow-integration.md` — integration reference

### pstack Detection

pstack is present when `.paul/pstack-models.md` or the global `~/.agents/pstack-models.md` exists, or the `poteto-mode` skill is invocable in this session.

### Subcommands

No argument: full interactive configuration. `add`: quick-add one mapping. `audit`: check current phase against declared flows. `list`: display configuration. `pstack`: write the standard pstack mapping preset. `uxui`: write the standard ux-ui-agent-skills design mapping preset.

### The Debt Rules Are Part of the Preset

Any `SPECIAL-FLOWS.md` this skill writes should carry the two session rules that make `.paul/DEBT.toml` operational, because a store nobody is told to read is a file, not a scheduler:

- **R-4 — deferred work lives in `.paul/DEBT.toml`, one `[[debt]]` row per item, each with a check that can fail.** Not a STATE bullet, not a SUMMARY prose row, not `.paul/ISSUES.md` unless there is no testable landing condition at all.
- **R-5 — evaluate the store at the gates the loop already passes:** session entry (`debt.py --run-checks`, an `overdue` blocking row is the next action), plan drafting (an uncovered row is a plan defect), phase exit (`--gate phase-NN-exit` is the only gate that can refuse a close), loop close (discharge becomes a TOML diff). No daemon.

When generating a new SPECIAL-FLOWS.md, include both with a rationale line. When auditing, report a missing R-4/R-5 as a configuration gap — the rest of the preset assumes they exist.

## Application

Route on subcommand:

- **Full configuration:** follow `configure-special-flows.md` — interactive discovery and mapping, generate `.paul/SPECIAL-FLOWS.md`, update PROJECT.md quick reference. If pstack is detected, offer the `pstack` preset as the starting point.
- **add:** ask skill name, work-type trigger, priority (required/optional); append to SPECIAL-FLOWS.md table; confirm.
- **audit:** read SPECIAL-FLOWS.md + STATE.md + ROADMAP.md phase requirements; display required skills; remind to verify invocations before UNIFY.
- **list:** read SPECIAL-FLOWS.md; display project-level skills with priority, phase overrides, templates/assets count.
- **pstack:** if pstack is detected, write the standard pstack mapping preset to SPECIAL-FLOWS.md (drop rows the project does not need) and update the PROJECT.md quick reference:

  | Skill | Work-type trigger | Priority |
  |---|---|---|
  | poteto-mode | any execute-type plan task | required |
  | architect | code crossing a function boundary | required |
  | interrogate | contested design, pre-ship review | optional |
  | swarm | research and coverage matrices | optional |
  | technical-writing | docs, RFCs, PR descriptions | optional |
  | show-me-your-work | multi-session or autonomous runs | optional |
  | design-taste-frontend | building, restyling, or reviewing a rendered page or app screen | optional |
  | paul-security | task touches auth, input parsing, a new endpoint, a path, or a dependency; or a phase ships | optional |
  | reflect | UNIFY close-out | required |

  The design row is `optional` on purpose: it needs Node 22 and a Chrome, so a project that never renders a page should not carry a required row whose gate cannot run. Write it when the project renders one, and drop it when it does not — a required row nobody can execute trains the reader to ignore the audit.

  The security row is `optional` for the same reason: guidance mode runs anywhere, but a full audit's `findings.json` cannot be validated on Windows (`O_NOFOLLOW` is undefined), so an unvalidatable run must not gate a phase. Add it when the project has a trust boundary worth reviewing; expect `blocking` rows only on a POSIX host or when the finding is evidenced statically.

  ### The uxui Preset

  When the user supplies `uxui` (or a project renders UI and has the kit vendored at `~/.agents/ux-ui-agent-skills/`), offer these rows as the starting point, replacing the plain `design-taste-frontend` row — the kit's objective gates own tokens/components/a11y/code, and `design-taste-frontend` keeps rendered-taste critique. Drop rows for work the project does not do:

  | Skill | Work-type trigger | Priority |
  |---|---|---|
  | design-doctrine | first design/UI session of any phase | required |
  | design-tokens | creating or changing a color palette, type scale, spacing, or theme | required |
  | design-component | speccing a new component (before code) | required |
  | design-code | implementing component or screen code | required |
  | a11y-audit | every UI phase, before exit | required |
  | apply-aesthetic | phase start when a look/direction is chosen | optional |
  | design-gate | UNIFY evidence on every UI phase | required |
  | design-taste-frontend | rendered-taste critique of a built page or screen | required |

  The gate row is `required` only because UI phases have a rendered artifact; the kit's render checks need Node 22 + Chrome (`npx playwright install chrome`), its 13 file-based checks (tokens, contrast math, hardcodes, emoji) run anywhere. If the environment has neither, demote `design-gate` to `optional` — a required row nobody can execute trains the reader to ignore the audit.

Verify success criteria:
- [ ] SPECIAL-FLOWS.md created or updated (for config/add/pstack/uxui)
- [ ] PROJECT.md quick reference updated (for config)
- [ ] Current phase skills displayed (for audit)
- [ ] Configuration summary shown (for list)

## Examples

### Example: Quick Add

Input: `add`

Result: one skill mapping appended to SPECIAL-FLOWS.md with trigger and priority.

## Common Pitfalls

- **Declaring flows but never auditing.** Consequence: APPLY-time skill blocks surprise the user. Fix: audit before UNIFY.

## References

- `~/.agents/paul-framework/workflows/configure-special-flows.md`
- `~/.agents/paul-framework/references/specialized-workflow-integration.md`
- `.paul/PROJECT.md`, `.paul/STATE.md`, `.paul/SPECIAL-FLOWS.md`
