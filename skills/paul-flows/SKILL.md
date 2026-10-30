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

- **Works best with:** nothing (full interactive configuration), or one of `add`, `audit`, `list`, `pstack`
- **Also useful:** skill name + work-type trigger when using `add`

If you supply a subcommand inline it routes directly; with no input it runs full configuration.

Example: `Use paul-flows: audit`

## Key Concepts

### Framework Sources of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, read the same subpaths under `~/.agents/paul-framework/`. If neither exists, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/configure-special-flows.md` — configuration workflow
- `~/.agents/paul-framework/references/specialized-workflow-integration.md` — integration reference

### pstack Detection

pstack is present when `.paul/pstack-models.md` or the global `~/.agents/pstack-models.md` exists, or the `poteto-mode` skill is invocable in this session.

### Subcommands

No argument: full interactive configuration. `add`: quick-add one mapping. `audit`: check current phase against declared flows. `list`: display configuration. `pstack`: write the standard pstack mapping preset.

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
  | base-help | base CLI question or command error | optional |
  | reflect | UNIFY close-out | required |

Verify success criteria:
- [ ] SPECIAL-FLOWS.md created or updated (for config/add/pstack)
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
