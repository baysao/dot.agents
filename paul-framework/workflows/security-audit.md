<purpose>
Run the security-audit skill against a plan's diff or the whole tree, and turn each confirmed finding into a debt row whose check is a regression test rather than a copy of the report.

Produces source-evidenced findings, a severity-to-schedule mapping, and schedulable rows. Does not modify target source.
</purpose>

<when_to_use>
- A PLAN or APPLY task touches authentication, authorization, input parsing, a new endpoint, a file path, a subprocess, or a third-party dependency
- A phase is about to ship and has not been reviewed for a trust-boundary defect
- A milestone close needs a full-tree pass
- Explicit `/paul:security` invocation
</when_to_use>

<loop_context>
Expected phase: any. Guidance mode fits PLAN and APPLY; full audit fits VERIFY and milestone close.
Prior phase: the plan or phase whose diff is in scope.
Next phase: back to the loop, or a `plan-fix` when a confirmed critical/high finding exists.
</loop_context>

<required_reading>
@.paul/STATE.md
@.paul/config.md
@.paul/DEBT.toml
@src/references/security-audit-integration.md
</required_reading>

<references>
@~/.agents/skills/security-audit/SKILL.md
@~/.agents/skills/security-audit/RECONNAISSANCE.md
@~/.agents/skills/security-audit/HUNTING.md
@~/.agents/skills/security-audit/VALIDATION-AND-REPORTING.md
</references>

<process>

<step name="choose_mode" priority="first">
**Pick guidance or full audit before doing anything else.** Loading the skill does
not authorize the complete workflow.

Read `.paul/config.md`:
```yaml
security_audit:
  enabled: true|false
  default_profile: quick|standard|deep
```

**Guidance mode** when the trigger is one plan or one task. Read only the companion
files the task needs (e.g. `WEB-PROTOCOL-AND-AUTH.md` for an endpoint). Write nothing;
findings stay in the conversation until they become debt rows.

**Full audit mode** when the user invoked `/paul:security`, a phase ships, or a
milestone closes. Run the six phases from `SKILL.md`.

If the request could honestly be either and the cost difference matters, ask one
question. Do not ask when the trigger is unambiguous — a new endpoint is guidance, a
release is an audit.
</step>

<step name="resolve_scope">
**Scope the run to the diff, not the tree.**

1. Find the last phase commit:
   ```bash
   git log --oneline -1 --grep="^feat(" -- .paul/
   ```
2. Compute the review surface:
   ```bash
   git diff --name-only <last-phase-commit>..HEAD
   ```
3. Resolve `scope_paths` from that list, plus the direct callers of any changed
   boundary function.

| Trigger | Profile | Scope |
|---------|---------|-------|
| One plan task, trust surface | `quick` | Changed files |
| `/paul:security` mid-phase | `quick`/`standard` | Diff |
| Phase that ships | `standard` | Diff + callers |
| Milestone close | `deep` | Whole tree |

Record the profile and `scope_paths` in `run-metadata.json`. A scoped or `quick` run
is **partial coverage** and the report must say so — the skill's rule, not PAUL's.

If no `.paul/` commit exists yet, say so and scope to the working-tree diff, or to the
whole tree if the repository is new. Do not silently audit everything when asked about
a phase.
</step>

<step name="run_audit">
**Follow `security-audit/SKILL.md` for the audit itself.** PAUL contributes scope,
gates, and the destination for findings; it does not reimplement hunting.

Full audit setup, in the skill's order:
1. **Output directory** — `~/security-audit-skill/<repo>/run-<N>`, never inside the
   target unless it is gitignored as a whole and the user chose it.
2. **Source ref** — the reviewed commit and whether the worktree is dirty.
3. **`run-metadata.json`** before delegation: `run_id`, `repo`, `target`, `source_ref`,
   `profile`, `scope_paths`, `budget`, `execution_policy`,
   `run_status: "in_progress"`.
4. **Six phases** — reconnaissance → hunting waves → candidate validation →
   structured output → independent record verification → report.

Do not shorten a phase because PAUL is waiting. A partial audit reported as complete is
worse than no audit: it converts "unreviewed" into a false claim of "reviewed".

Execution safety is the skill's, unchanged: no network, an empty environment, a
read-only target, writes only in the assigned `scratch/`, explicit resource limits. If
a control cannot be enforced, **do not execute target code** — report the missing
sandbox capability as a `needs_validation` blocker and give the safe plan.
</step>

<step name="validate_output">
**Validate the JSON before any finding becomes a debt row.**

```bash
node ~/.agents/skills/security-audit/validate-findings.cjs <run>/findings.json
node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <run>/coverage-ledger.json
```

**On Windows both exit 1 without reading the file:**

```
Failed to read findings JSON: OS no-follow and nonblocking input protection is unavailable
```

`fs.constants.O_NOFOLLOW` and `O_NONBLOCK` are undefined there. That is a capability
gap, not a finding. When it happens:

- Set `run_status: "incomplete"` with
  `incomplete_reason: "validators_unavailable_on_this_platform"`.
- **Do not** write `confirmed` rows to `DEBT.toml` from that run. Unvalidated JSON is a
  draft.
- **Guidance mode is unaffected** — it writes no `findings.json`, so there is nothing to
  validate and the finding stands on the source evidence quoted in-thread. Do not
  downgrade it to `needs_validation` because a validator could not read a file that was
  never written.
- State it in the audit report's first section and in the UAT verdict, the same way a
  missing Chrome blocks the visual gate.
- Do not substitute a different check and report a pass.

On POSIX, both must pass. A run that failed validation is not terminal.
</step>

<step name="map_to_debt">
**Severity becomes scheduling. `needs_validation` has no severity.**

| Record | Row |
|---|---|
| `confirmed` critical/high | `kind = "tech"`, `blocking = "phase-NN-exit"`, `owner = "agent"` |
| `confirmed` medium | `kind = "tech"`, `trigger = "phase:NN"` |
| `confirmed` low/informational | Usually no row; note it in the SUMMARY |
| `needs_validation` | `kind = "reopen"`, `trigger = "phase:NN"` |
| `rejected` | No row |

The check must run the regression test the fix will add:

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

`check = { type = "command", ... }` takes **`run`**, not `command`. The field is
`run`; a row keyed `command =` raises `KeyError: 'run'` and kills `debt.py` for every
row in the store, not just its own.

When no test can exist (a deployment topology gap, a vendor default), make it a human
risk acceptance rather than a fake check:

```toml
kind = "decision"
owner = "owner"
check = { type = "text_present", path = "docs/security/RISK-ACCEPTED.md", pattern = "SEC-005" }
```

Then confirm the store still parses:
```bash
python ~/.agents/paul-framework/scripts/debt.py --run-checks
```

A row with a mistyped check field is invisible, not logged.
</step>

<step name="route">
**A confirmed critical/high finding is not fixed by this workflow.**

- If it blocks the phase: offer `/paul:plan-fix` scoped to that finding, with the
  regression test as the first AC.
- If the whole phase's security posture is wrong: route to `/paul:plan` with updated
  intent — the spec, not the code, needs rethinking.
- Otherwise: rows are written, the loop continues, the gate asks at phase exit.

Display:
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
</step>

</process>

<output>
- Audit artifacts under `~/security-audit-skill/<repo>/run-<N>/`
- `DEBT.toml` rows with regression-test checks, or an explicit `run_status: "incomplete"`
- Routing to `plan-fix` or `plan` when a confirmed finding needs work
- A stated coverage claim that matches the profile actually run
</output>

<error_handling>
**Skill not installed:**
- Report `~/.agents/skills/security-audit/SKILL.md` missing and stop. Do not improvise
  a security review from memory — a review that cannot cite `HUNTING.md`'s candidate
  gate produces checklist deviations, not findings.

**Validators unavailable (Windows):**
- A full audit is `run_status: "incomplete"`, reason
  `validators_unavailable_on_this_platform`, with no `confirmed` rows written from it.
  Say which claims are unvalidated.
- Guidance mode writes no `findings.json` and is unaffected; its findings stand on the
  source evidence quoted in-thread.

**Sandbox controls unavailable:**
- Do not execute target code. Static evidence only, and a `needs_validation` record with
  the exact missing capability.

**Budget exhausted mid-run:**
- Follow the skill: mark the rest `deferred`, set `run_status: "incomplete"`, and make
  no complete-coverage claim. A partial report's first section says so.

**No findings:**
- Report clean scope with the profile named. Never imply the tree is clean; only the
  reviewed surface is.
</error_handling>

<success_criteria>
- [ ] Mode chosen deliberately (guidance vs full audit), not by default inertia
- [ ] Scope is the diff unless the trigger is a release, and is stated
- [ ] Six phases run in order for a full audit, or guidance stays in-thread
- [ ] Validators run on POSIX; on Windows a full audit is marked incomplete and no
      `confirmed` row is written from it (guidance mode still yields rows)
- [ ] Every confirmed critical/high has a `blocking` row with a regression-test check
- [ ] `needs_validation` rows carry no severity and use `kind = "reopen"`
- [ ] `debt.py --run-checks` parses the store after the writes
- [ ] Coverage language matches the profile; no "the codebase is clean" claim from a
      scoped run
</success_criteria>

## Extensions
<!-- Extensions are managed by integration installers. Do not edit manually. -->
