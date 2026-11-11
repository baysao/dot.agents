<purpose>
Guide manual user acceptance testing of recently built features. Extract deliverables from SUMMARY.md, generate test checklist, guide user through each test, log issues to phase-scoped file.

The USER performs all testing — Claude generates the checklist, guides the process, and captures issues.
</purpose>

<template>
@src/templates/UAT-ISSUES.md
</template>

<process>

<step name="identify">
**Determine what to test:**

If $ARGUMENTS provided:
- Parse as phase number (e.g., "4") or plan number (e.g., "04-02")
- Find corresponding SUMMARY.md file(s)

If no arguments:
- Find most recently modified SUMMARY.md

```bash
find .paul/phases -name "*SUMMARY.md" -type f -exec ls -lt {} + | head -5
```

Read the SUMMARY.md to understand what was built.

Key extraction points:
- Acceptance Criteria results
- Files created/modified
- Deviations (if any)
</step>

<step name="extract">
**Extract testable deliverables from SUMMARY.md:**

Parse for:
1. **Acceptance Criteria** - Each AC becomes a test item
2. **Files Created/Modified** - What changed
3. **User-facing changes** - UI, workflows, interactions

Focus on USER-OBSERVABLE outcomes, not implementation details.

**Optional drift input (manual, never a gate):** if `docs/drift/*_DRIFT_REPORT.md`
exists, read the newest one and add any finding that touches this plan's
deliverables as an extra test item, citing the report path as its origin. Skip the
step when no report exists - `egm-drift-report` is user-invoked and this workflow
must not offer to run it, because a verification pass that can generate its own
findings stops being verification by the user.

Map AC to tests:
- AC-1: "Feature X exists" → User can see/use Feature X
- AC-2: "Behavior Y works" → User can trigger and verify Behavior Y
</step>

<step name="generate">
**Generate manual test checklist:**

Create structured test plan:

```
# User Acceptance Test: [Plan Name]

**Scope:** [What was built - from SUMMARY.md]
**Source:** [path to SUMMARY.md]
**Testing:** Manual user validation

## Pre-flight
- [ ] Application builds and runs without errors
- [ ] Application launches to expected state

## Acceptance Criteria Tests

### AC-1: [Criteria from plan]
**What to test:** [User-observable behavior]
**Steps:**
1. [Specific action to take]
2. [What to look for]
3. [Expected result]

### AC-2: [Criteria from plan]
...

## Edge Cases
- [ ] [Relevant edge case based on feature]
- [ ] [Another edge case]

## Visual/UX Check
- [ ] `node ~/.agents/skills/design-taste-frontend/scripts/lint.mjs <changed source files>` exits 0
- [ ] `node ~/.agents/skills/design-taste-frontend/scripts/inspect.mjs <url | built index.html>` exits 0 at 1440, 768, 390
- [ ] Every FAIL read and fixed; every WARN either fixed or defended in one sentence
- [ ] Screenshots the inspector printed were opened and looked at, not just counted

## Security Check
- [ ] `python ~/.agents/paul-framework/scripts/debt.py --run-checks --gate phase-NN-exit` exits 0 with no unpaid security row
- [ ] Every confirmed critical/high finding from this plan has a debt row whose check runs a regression test
- [ ] `node ~/.agents/skills/security-audit/validate-findings.cjs <run>/findings.json` exits 0, or the run is recorded as `incomplete` with the reason
```

Present this checklist to user.

**A visual check must have an exit code.** "UI matches expected design" is not testable: it is true of every screenshot and false of none, so it can never fail, and a check that cannot fail reports work as done. The inspector above measures the page in a real browser and exits 1 on a FAIL, which is what lets the finding become a debt row that discharges itself.

Three things decide what you write in that section:

1. **The build, not the dev server.** Run the last gate on the production build (`vite build && vite preview`, `next build && next start`, or the built `index.html`). Bundlers drop rules the dev server showed; one dropped a `backdrop-filter`.
2. **The final version.** Re-run after the last change. A gate that ran three edits ago proves nothing.
3. **No Node 22, no Chrome, or no skill installed.** Say so in the checklist and record which check you could not run. `lint.mjs` needs only Node 18. Do not substitute a different check and call it the gate, and do not mark the item passed.

When the plan touches no rendered surface, delete the section instead of leaving four unticked boxes the reader has to interpret.

**A security check must have an exit code.** "No vulnerabilities introduced" is not testable — it is true of every diff and false of none. The gate above ties the claim to the debt store, which is the only place a finding can be discharged. Do not write "reviewed for security" as an acceptance criterion; write the row.

Three things decide what you write in that section:

1. **The store, not the report.** A check that greps the audit report for the finding ID discharges when the report is deleted, not when the bug is fixed. The row must run the test the fix adds.
2. **The diff, not the tree.** A plan's security check covers what the plan changed. A clean diff is not a clean repository, and the checklist must not imply otherwise.
3. **Windows cannot validate.** Both validators require `fs.constants.O_NOFOLLOW`, undefined on Windows, so they exit 1 before parsing. Record the run as `incomplete`, name the blocker, and write no `confirmed` rows — the same discipline as a missing Chrome in the visual check.

When the plan touches no trust boundary, delete the section instead of leaving three unticked boxes the reader has to interpret.
</step>

<step name="guide">
**Guide user through each test:**

For each test item, use AskUserQuestion:
- header: "[AC-N or Feature name]"
- question: "[Test description] - Did this work as expected?"
- options:
  - "Pass" — Works correctly
  - "Fail" — Doesn't work as expected
  - "Partial" — Works but with issues
  - "Skip" — Can't test right now

**If Pass:** Move to next test

**If Fail or Partial:**
Follow up with AskUserQuestion:
- header: "Issue details"
- question: "What went wrong?"
- options:
  - "Crashes/errors" — Application error or exception
  - "Wrong behavior" — Does something unexpected
  - "Missing feature" — Expected functionality not present
  - "UI/visual issue" — Looks wrong but functions
  - "Let me describe" — Free-form description needed
</step>

<step name="collect">
**Collect and categorize issues:**

For each failed/partial test, gather:
- Feature/AC affected
- What went wrong (from user input)
- Severity:
  - **Blocker** — Can't use the feature at all
  - **Major** — Feature works but significant problem
  - **Minor** — Small issue, feature still usable
  - **Cosmetic** — Visual only, no functional impact
</step>

<step name="log">
**Log issues to phase-scoped file:**

If any issues found:

1. Create `.paul/phases/XX-name/{phase}-{plan}-UAT.md` if doesn't exist
2. Use template from `@src/templates/UAT-ISSUES.md`
3. Add each issue with UAT-NNN format:

```markdown
### UAT-001: [Brief description]

**Discovered:** [date] during user acceptance testing
**Phase/Plan:** [phase]-[plan] that was tested
**Severity:** [Blocker/Major/Minor/Cosmetic]
**AC:** [Which acceptance criteria this relates to]
**Description:** [User's description of the problem]
**Expected:** [What should have happened]
**Actual:** [What actually happened]
```

**Note:** Issues go to phase-scoped UAT file, NOT global `.paul/ISSUES.md`.

**4. Add a debt row when the finding has a landing condition.**

A UAT finding either gets fixed now or it is deferred. If deferred, it goes in
`.paul/DEBT.toml` with the UAT ID as its origin, so a later session can test whether
it is still real:

```toml
[[debt]]
id = "DEBT-0NN"
title = "UAT-00N: [brief description]"
kind = "uat"
origin = "[phase]-[plan] UAT-00N"
owner = "agent"
trigger = "phase:NN"
check = { type = "text_present", path = ".paul/phases/[phase]/[plan]-UAT.md", pattern = "### UAT-00N" }
```

The check is deliberately about the UAT record, not the fix: it asserts the finding
still exists until the fix plan removes it. When it is fixed, the plan's SUMMARY
carries the AC and the row becomes `status = "done"`.

A Blocker or Major that is deferred rather than fixed should also carry
`blocking = "phase-NN-exit"` — something that stops the user from using the feature
should not be allowed to drift out of a phase silently.

**5. Re-index if this step fixed source.**

When issues are fixed during verification (not merely logged) and `.paul/config.md` has
`xerj: enabled: true`, run the replay pair after the last fix (reference:
`@~/.agents/paul-framework/references/xerj-integration.md`):

```bash
cd <index_cwd> && xerj autoindex --prefix <index_prefix> <index_root>
```

A fix that lands here changes source, so the index UNIFY and the next phase read is
pre-fix until this runs. Note the refresh in the UAT entry. If it fails, record the gap
and name the searches that are now untrustworthy — do not mark the index current.
</step>

<step name="summarize">
**Present test summary:**

```
# Test Results: [Plan Name]

**Tests run:** [N]
**Passed:** [N]
**Failed:** [N]
**Partial:** [N]
**Skipped:** [N]

## Issues Found
[List any issues with severity]

## Verdict
[Based on results:]
- ALL PASS: "All tests passed. Feature validated."
- MINOR ISSUES: "Feature works with minor issues logged."
- MAJOR ISSUES: "Significant issues found - review before proceeding."
- BLOCKERS: "Blocking issues found - must fix before continuing."

## Next Steps
[Based on verdict:]
- If clean: Suggest proceeding to next phase/plan
- If issues: Suggest creating FIX plan to address
```
</step>

<step name="offer">
**Offer next actions based on results:**

Use AskUserQuestion:
- header: "Next"
- question: "What would you like to do?"
- options (based on results):

If all passed:
- "Continue" — Proceed with confidence
- "Test more" — Run additional manual tests
- "Done" — Finish testing session

If issues found:

**Diagnostic classification — classify before fixing, instead of jumping to code patches, because fixing the wrong layer wastes loops and produces fragile patches:**

Use AskUserQuestion:
- header: "Classify Issues"
- question: "Before planning fixes, what went wrong?"
- options:
  - "Intent issue" — The feature needs to work differently than planned
  - "Spec issue" — The plan missed a requirement or got something wrong
  - "Code issue" — The plan was right, the code doesn't match
  - "Log and continue" — Issues logged, proceed without fixing now
  - "Review issues" — Look at logged issues in detail

**Routing per classification:**

**Intent (1):** "Let's re-plan with updated intent."
- Route to `/paul:plan` for affected phase with updated intent
- Previous plan's issues inform the re-plan
- Do NOT create a fix plan — the spec itself needs rethinking

**Spec (2):** "The plan needs updating before we fix code."
- Route to `/paul:plan-fix` with spec-level scope
- Identify which ACs or tasks need revision
- Update the plan FIRST, then generate code fixes from the corrected spec
- This prevents patching code against a wrong spec

**Code (3):** "Standard fix — plan was right, code needs patching."
- Route to `/paul:plan-fix` with code-level scope (existing behavior)
- Generate targeted fix plan from UAT issues

**Log and continue (4):** Issues logged, proceed anyway (existing behavior)

**Review issues (5):** Show logged issues in detail (existing behavior)
</step>

</process>

<success_criteria>
- [ ] Test scope identified from SUMMARY.md
- [ ] Checklist generated based on acceptance criteria
- [ ] User guided through each test via AskUserQuestion
- [ ] All test results captured (pass/fail/partial/skip)
- [ ] Any issues logged to phase-scoped UAT file
- [ ] Summary presented with verdict
- [ ] User knows next steps based on results
</success_criteria>

## Extensions
<!-- Extensions are managed by integration installers. Do not edit manually. -->
