---
name: paul-security
description: Run security-audit against a plan's diff or the whole tree and schedule findings as debt. Use before a phase ships or when a task touches a trust boundary.
metadata:
  opencode/slash: "true"
---

## Purpose

Run the `security-audit` skill inside the PAUL loop. Guidance mode reviews the trust
surface of the diff in-thread; full audit mode runs the skill's six phases for a scope
that ships. Either way the output is debt rows PAUL's existing gates already evaluate.

Use it when a task touches authentication, authorization, input parsing, a new endpoint,
a file path, a subprocess, or a third-party dependency, or when a phase is about to ship.

## Input

Optionally bring scope:

- **Works best with:** a phase or plan number (e.g. `4`, `04-02`), or `--full`
- **Also useful:** nothing — empty scope means guidance mode on the current plan's diff

Example: `Use paul-security: --full`

## Key Concepts

### Framework Sources of Truth

**Other harnesses.** These paths assume an installation at `~/.agents/paul-framework/`;
any harness can read them there. If that directory is absent, tell the user to install
the PAUL framework (workflows/, templates/, scripts/) before using this skill.

- Workflow: `~/.agents/paul-framework/workflows/security-audit.md`
- Reference: `~/.agents/paul-framework/references/security-audit-integration.md`
- Skill: `~/.agents/skills/security-audit/SKILL.md`
- Debt schema: `~/.agents/paul-framework/templates/DEBT.toml.md`

### Guidance Is the Default

Loading `security-audit` does not authorize the complete workflow. A full audit per
plan is how a gate gets ignored: the cost is paid on every small change. Guidance mode
reads only the companion file the task needs and writes nothing to disk until a finding
becomes a debt row.

Reserve the full audit for a scope that ships — a phase exit or a milestone close.

### Scope Is the Diff

A per-plan audit reviews the files changed since the last phase commit, not the tree.
Only a release trigger widens to the whole tree, and the report must then say `deep`
rather than implying the narrower run covered everything.

A scoped or `quick` run is **partial coverage** and says so. The skill's rule applies
unchanged: a partial ledger contributes only its recorded evidence, never an implied
"the rest is fine."

### Severity Becomes Scheduling

| Audit record | Debt row |
|---|---|
| `confirmed` critical / high | `kind = "tech"`, `blocking = "phase-NN-exit"` |
| `confirmed` medium | `kind = "tech"`, `trigger = "phase:NN"` |
| `confirmed` low / informational | Usually no row; note it in the SUMMARY |
| `needs_validation` | `kind = "reopen"`, `trigger = "phase:NN"`, **no severity** |
| `rejected` | No row |

`needs_validation` records have no severity in the skill's schema. PAUL must not invent
one to make the row fit.

### The Check Is a Regression Test

A confirmed vulnerability is discharged when the fix lands with a test that fails
without it. The row runs that test:

```toml
check = { type = "command", run = "go test ./internal/orders -run TestRejectsForeignTenantID", expect = "ok" }
```

`check` takes **`run`**, not `command`. A row keyed `command =` raises `KeyError: 'run'`
and aborts `debt.py` for every row in the store, not just its own.

A check that greps the report for the finding ID is not a fix check — it discharges
when someone deletes the report. Use that shape only for `needs_validation`, where "the
question is still open" is the state being tracked.

When no test can exist, make it a human risk acceptance instead of a fake check:

```toml
kind = "decision"
owner = "owner"
check = { type = "text_present", path = "docs/security/RISK-ACCEPTED.md", pattern = "SEC-005" }
```

### Windows Cannot Validate

`validate-findings.cjs` and `validate-coverage-ledger.cjs` refuse to read their input
unless `fs.constants.O_NOFOLLOW` and `O_NONBLOCK` are integers. Both are `undefined` on
Windows, so they exit 1 with a capability message before parsing anything.

That is a platform gap, not a finding. A **full audit** becomes
`run_status: "incomplete"` with
`incomplete_reason: "validators_unavailable_on_this_platform"`, and **no `confirmed`
rows are written from that run** — an unvalidated JSON file is a draft. Say so in the
report and the UAT verdict rather than substituting a weaker check.

Guidance mode is unaffected: it writes no `findings.json`, so there is nothing to
validate, and a finding stands on the source evidence quoted in-thread. Do not downgrade
it to `needs_validation` because a validator could not read a file that was never
written.

## Process

1. Check `.paul/config.md` for the `security_audit` block. If `enabled: false`, say so
   and stop unless the user invoked this explicitly.
2. Choose the mode. Guidance for one plan or task; full audit for a shipping phase,
   a milestone close, or `--full`. Ask only when the trigger is genuinely ambiguous.
3. Resolve scope from `git diff --name-only <last-phase-commit>..HEAD` plus the direct
   callers of any changed boundary function.
4. Run the audit per `security-audit/SKILL.md`. For a full audit, write
   `run-metadata.json` before delegating and run all six phases in order.
5. Validate the JSON. On Windows, mark the run incomplete and skip the confirmed rows.
6. Map each record to a debt row using the table above. Write the rows.
7. Run `python ~/.agents/paul-framework/scripts/debt.py --run-checks` and confirm the
   store parses.
8. Route a confirmed critical/high finding to `/paul:plan-fix` with the regression test
   as the first acceptance criterion.

## Output

```
════════════════════════════════════════
SECURITY AUDIT — {run_id}
════════════════════════════════════════

Profile: {profile}   Scope: {N paths}   Source: {ref}

Confirmed:        {N}  (critical {a} / high {b} / medium {c})
Needs validation: {N}
Rejected:         {N}

Validators: {PASS | UNAVAILABLE ({reason})}

Debt rows written: {IDs}
Report: {path}

────────────────────────────────────────
[If confirmed critical/high:]
▶ NEXT: /paul:plan-fix — {SEC-NNN} blocks {phase-NN-exit}

[If none:]
▶ No confirmed boundary violation in scope. Coverage is {profile}, not full.
────────────────────────────────────────
```

## Anti-Patterns

- **Full audit on every plan.** Guidance mode is the default for a reason.
- **Severity invented for `needs_validation`.** A `reopen` row with `owner = "agent"`.
- **A debt check that greps the report.** Discharges on deletion, not repair.
- **Calling a Windows run validated.** The validators did not run; the run is incomplete.
- **Reporting a scanner hit as confirmed.** No boundary, no principal, no result → no finding.
- **Treating the audit as the fix.** The report is evidence; the `plan-fix` is the work.
