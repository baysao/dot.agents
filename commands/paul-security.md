---
name: paul:security
description: Run security-audit against a plan's diff or the whole tree and schedule findings as debt
argument-hint: "[phase|plan|--full]"
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion]
---

<objective>
Run the `security-audit` skill in guidance mode for a plan's trust surface, or in full
audit mode for a phase that ships or a milestone close, then convert each finding into
a schedulable debt row.

**When to use:** A task touches auth, input parsing, a new endpoint, a file path, a
subprocess, or a dependency; a phase is about to ship; a milestone closes; or the user
asks for a security review.

**Who audits:** the `security-audit` skill. This command owns scope, mode, gates, and
the destination for findings — it does not reimplement hunting.
</objective>

<execution_context>
@~/.agents/paul-framework/workflows/security-audit.md
@~/.agents/paul-framework/references/security-audit-integration.md
</execution_context>

<context>
Scope: $ARGUMENTS (optional)
- `NN` or `NN-PP`: audit that plan's diff
- `--full`: full audit of the tree, `deep` profile
- empty: guidance mode on the current plan's diff

@.paul/STATE.md
@.paul/config.md
@.paul/DEBT.toml
</context>

<process>
**Follow workflow: @~/.agents/paul-framework/workflows/security-audit.md**

The workflow implements:
1. Choose mode deliberately — guidance by default, full audit only for a shipping scope
2. Resolve scope from the diff since the last phase commit, not the tree
3. Run the audit under the skill's six phases and sandbox rules
4. Validate `findings.json` and `coverage-ledger.json` before any row is written
5. Map severity to scheduling: confirmed critical/high blocks the phase exit, medium and `needs_validation` are deferred
6. Write `DEBT.toml` rows whose `check` runs the regression test the fix will add
7. Route a confirmed critical/high finding to `/paul:plan-fix`

Run `python ~/.agents/paul-framework/scripts/debt.py --run-checks` after writing the
rows and confirm the store parses. A row with a mistyped check field is invisible, not
logged.
</process>

<success_criteria>
- [ ] Mode chosen deliberately (guidance vs full audit)
- [ ] Scope is the diff unless the trigger is a release, and is stated
- [ ] Validators run on POSIX; on Windows a full audit is `incomplete` and no
      `confirmed` row is written from it (guidance mode still yields rows)
- [ ] Every confirmed critical/high has a `blocking = "phase-NN-exit"` row with a regression-test check
- [ ] `needs_validation` rows carry no severity and use `kind = "reopen"`
- [ ] Store parses after the write
- [ ] Coverage claim matches the profile actually run
</success_criteria>

<anti_patterns>
- Don't run a full audit per plan — cost per change exceeds the change and the gate gets skipped
- Don't invent a severity for a `needs_validation` record
- Don't write a check that greps the report — it discharges on deletion, not repair
- Don't claim a Windows run was validated; the validators exit before reading
- Don't present an audit as the fix — the report is evidence, `/paul:plan-fix` is the work
</anti_patterns>
