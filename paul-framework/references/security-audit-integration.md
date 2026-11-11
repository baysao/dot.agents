# Security Audit Integration

Reference for running the `security-audit` skill inside the PAUL loop.

---

## Overview

`security-audit` finds vulnerabilities that cross a real trust boundary and returns
source evidence, a bounded reproduction, a severity, and the smallest effective fix.
PAUL is a foreground loop with gates. The integration point is **not** "run an audit
somewhere" — it is *which gate asks, what makes it fail, and where a finding lands so
it can discharge*.

The skill is authoritative on how to audit. This document is authoritative on when
PAUL asks for one and what it does with the answer.

---

## Two Modes, One Skill

Loading `security-audit` does not authorize the full workflow. PAUL must pick the mode
deliberately, because the modes have different costs and write different things.

| Mode | When PAUL uses it | Writes | Cost |
|------|-------------------|--------|------|
| **Guidance** | A PLAN or APPLY task touches auth, input parsing, a new endpoint, a trust boundary, or a third-party dependency | Nothing. Findings stay in the conversation. | One thread |
| **Full audit** | Explicit `/paul:security`, or a phase that ships before a milestone close | `~/security-audit-skill/<repo>/run-<N>/` — six phase artifacts, outside the repo | Recon agents + hunter waves + verifiers |

**Default to guidance.** A full audit per plan is how a gate gets ignored: the cost is
paid on every small change and the findings are mostly the ones the diff already
showed. Reserve the full workflow for a scope that ships.

Do not ask the user which mode when the trigger is unambiguous. A task adding an
endpoint is guidance; a milestone close is a full audit. Ask only when the plan's own
text makes it genuinely unclear.

---

## Scope: Diff, Not Repository

The single most useful scoping decision is that a per-plan audit reviews **the diff
since the last phase commit**, not the tree.

| Trigger | Scope (`scope_paths`) | Profile |
|---------|----------------------|---------|
| PLAN or APPLY task touches a trust surface | Changed files only | `quick` |
| `/paul:security` mid-phase | `git diff --name-only <last-commit>..HEAD` | `quick` or `standard` |
| Phase exit that ships | Changed files + their callers | `standard` |
| Milestone close / release | Whole tree | `deep` |

A scoped run is **partial coverage and must say so**. The skill's own rule applies
unchanged: a scoped or `quick` ledger contributes only its recorded evidence, never an
implied "the rest is fine."

---

## Severity Becomes Scheduling

The skill assigns severity only to `confirmed` records. `needs_validation` records
have **no severity** — they are a blocked hypothesis with an exact missing fact, and
PAUL must not invent a severity to fit them into the debt schema.

| Audit record | PAUL destination | Debt row shape |
|---|---|---|
| `confirmed` critical / high | Blocks the phase that ships it | `blocking = "phase-NN-exit"`, `kind = "tech"`, `owner = "agent"` |
| `confirmed` medium | Scheduled, not blocking | `trigger = "phase:NN"`, `kind = "tech"` |
| `confirmed` low / informational | Read it; usually no row | — |
| `needs_validation` | A question to ask again | `kind = "reopen"`, `trigger = "phase:NN"` |
| `rejected` | Nothing. It is recorded in the report. | — |

### The check is a regression test, not the report

A confirmed vulnerability is discharged when the fix lands **with a test that fails
without it**. So the row's check runs that test:

```toml
[[debt]]
id = "DEBT-0NN"
title = "SEC-003: cross-tenant read via unvalidated tenant_id in /orders"
kind = "tech"
origin = "security-audit run-2 SEC-003"
owner = "agent"
blocking = "phase-4-exit"
check = { type = "command", run = "go test ./internal/orders -run TestRejectsForeignTenantID", expect = "ok" }
```

The fix plan must create `TestRejectsForeignTenantID`. Until it exists the command
exits non-zero, which is the correct answer: an unfixed vulnerability is not fixed
because the report was written.

**A check that asserts the report still contains the finding is not a fix check.** It
discharges when someone deletes the report. Reserve that shape for `needs_validation`,
where "the question is still open" *is* the state being tracked:

```toml
check = { type = "text_present", path = "findings.json", pattern = "SEC-004" }
```

### When no test can exist

Some confirmed findings cannot be tested in the project's harness: a deployment
topology gap, a vendor default, a CAP that no repository file records. Do not fake a
check. Make it a human risk acceptance:

```toml
kind = "decision"
owner = "owner"
blocking = "phase-4-exit"
check = { type = "text_present", path = "docs/security/RISK-ACCEPTED.md", pattern = "SEC-005" }
```

The row discharges when a human writes the acceptance and the reason. A gate that
cannot be discharged by the agent is honest; a gate that discharges itself is not.

---

## The Gates That Ask

| Gate | Workflow | What happens |
|------|----------|--------------|
| PLAN drafting | `plan-phase` | A plan touching a trust surface names the guidance-mode review as a task; the debt store's open `tech`/`reopen` rows become ACs or explicit out-of-scope |
| APPLY | `apply-phase` | Guidance mode for the task in hand; a confirmed critical/high finding opens a debt row at the moment of deferral |
| VERIFY | `verify-work` | `## Security Check` — a command with an exit code, beside `## Visual/UX Check` |
| TRANSITION | `transition-phase` | The existing `debt_gate` refuses the close while a `blocking = "phase-NN-exit"` security row is unpaid |
| Milestone close | `complete-milestone` | Full audit, `deep` profile, whole tree |

No new gate was invented. Security findings ride the debt store that R-4/R-5 already
evaluate, which is why a security row is schedulable the moment it is written.

---

## Platform: The Validators Are POSIX-Only

`validate-findings.cjs` and `validate-coverage-ledger.cjs` refuse to read their input
unless `fs.constants.O_NOFOLLOW` and `O_NONBLOCK` are integers. Both are `undefined`
on Windows, so on this platform they exit 1 with:

```
Failed to read findings JSON: OS no-follow and nonblocking input protection is unavailable
```

That is a **capability message, not a finding**. The consequences for PAUL:

1. The audit itself still runs — reconnaissance, hunting, and reporting are not
   blocked, only schema validation of the output.
2. A **full audit** whose validators could not execute is `run_status: "incomplete"`,
   and its findings **must not** be written to `DEBT.toml` as `confirmed` rows. An
   unvalidated JSON file is a draft.
3. **Guidance mode is unaffected.** It writes no `findings.json`, so there is nothing
   to validate; a finding survives on the source evidence quoted in-thread, which is
   the same bar the skill's candidate gate applies. Do not downgrade it to
   `needs_validation` merely because a validator could not run on a file that does not
   exist.
4. Record the blocker in the UAT verdict and in the audit report's first section, the
   same way a missing Chrome blocks the visual gate. Do not substitute a different
   check and call it the gate.

On POSIX, both validators must pass before a run is terminal:

```bash
node ~/.agents/skills/security-audit/validate-findings.cjs <run>/findings.json
node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <run>/coverage-ledger.json
```

---

## What This Integration Does Not Do

- **It does not modify target source.** The skill is explicit: the audit describes
  fixes. A fix is a `paul-plan-fix` plan, reviewed like any other.
- **It does not probe live systems.** Bounded local evidence inside the skill's sandbox
  controls, or `needs_validation`. Never a deployed endpoint, shared service, or
  production identity.
- **It does not write into `.paul/`.** Audit artifacts stay in the skill's output
  directory; only the debt rows are PAUL's.
- **It does not replace `aegis-audit`.** AEGIS is an adversarial design-risk framework
  across 14 domains; `security-audit` is a source-first vulnerability hunt with a
  reproduction. Use both when both apply, and do not present one as the other.

---

## Anti-Patterns

1. **Full audit on every plan.** Cost per change exceeds the change, and the gate gets
   skipped. Use guidance mode.
2. **Severity invented for `needs_validation`.** The skill forbids it. A `reopen` row
   with `owner = "agent"` is the correct shape.
3. **A debt check that greps the report.** It discharges on deletion, not on repair.
4. **Marking a Windows run validated.** The validators did not run; the run is
   incomplete and says so.
5. **Reporting a scanner's finding as confirmed.** The skill's candidate gate applies
   unchanged: no boundary, no principal, no result → no finding.
6. **Treating the audit as the fix.** The report is evidence; the `plan-fix` is the work.

---

*Reference: `skills/security-audit/SKILL.md`, `.paul/DEBT.toml`, R-4/R-5 in `.paul/SPECIAL-FLOWS.md`*
