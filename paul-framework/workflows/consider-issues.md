<purpose>
Review all open issues with current codebase context. Categorize as resolved, urgent, natural-fit, or can-wait. Offer triage actions. Prevents issue pile-up by closing the loop on deferred work.
</purpose>

<when_to_use>
- Before milestone completion (clean up before release)
- Periodically during active development
- When planning new phase (check for natural fits)
- After significant refactoring (issues may be resolved)
</when_to_use>

<process>

<step name="find_issues">
**Locate all issue sources:**

1. Check for the debt store — this is the primary source:
   ```bash
   python ~/.agents/paul-framework/scripts/debt.py --run-checks
   ```
   Every row already carries its own check, so rows that pass are discharged, not
   re-derived. If the store exists, this run is the review; you are confirming its
   output with the user, not searching for issues from scratch.

2. Check for global enhancements:
   ```bash
   ls .paul/ISSUES.md 2>/dev/null
   ```
   (Legacy projects may still use this file. Prefer `.paul/DEBT.toml` for anything
   with a landing condition; `ISSUES.md` is for untestable nice-to-haves.)

3. Check for phase-scoped UAT files:
   ```bash
   find .paul/phases -name "*-UAT.md" -type f 2>/dev/null
   ```

4. If none of the three exist:
   ```
   No issues to review.

   Issue sources are created by:
   - Deferrals during APPLY → .paul/DEBT.toml rows
   - Deferred enhancements without a test → .paul/ISSUES.md
   - UAT testing findings → .paul/phases/XX-name/{plan}-UAT.md

   All clear - continue with current work.
   ```
   Exit workflow.
</step>

<step name="parse_issues">
**Parse all open issues:**

From `.paul/DEBT.toml` (via `debt.py` output):
- Debt ID, title, computed state (`overdue` / `scheduled` / `waiting` / `open`)
- Origin, owner, blocking gate, trigger
- The check, and whether it currently passes

From `ISSUES.md` "## Open Enhancements" section:
- ISS number (ISS-001, ISS-002, etc.)
- Brief description
- Discovered phase/date
- Type (Bug/Enhancement/Technical Debt/UX)
- Effort estimate

From UAT files:
- UAT number (UAT-001, UAT-002, etc.)
- Severity (Blocker/Major/Minor/Cosmetic)
- Related AC
- Description

Build consolidated list with source reference.
</step>

<step name="analyze_each">
**For each open issue, analyze against codebase:**

1. **Check if still relevant:**
   - Search for related code/files mentioned
   - If code no longer exists or significantly refactored → likely resolved

2. **Check if accidentally resolved:**
   - Look for changes that may have addressed this
   - For debt rows, this is already answered: run `--run-checks`. A row that passes is
     resolved regardless of what the prose around it claims.

3. **Assess current urgency:**
   - Blocking upcoming phases?
   - Pain point in recent work?
   - Affecting actively-touched code?
   - Is the row `overdue`, or does its `blocking` gate belong to the phase that is closing?

4. **Check natural fit:**
   - Aligns with upcoming phase in roadmap?
   - Would touch same files as current work?
   - Does its `trigger` name the phase being planned next?

**Categorize:**
- **Resolved** - Can be closed (check passes, code changed, no longer applicable)
- **Urgent** - Should address before continuing (blocking gate, overdue, problematic)
- **Natural fit** - Good candidate for upcoming phase X
- **Can wait** - Keep deferred, no change in status
</step>

<step name="report">
**Present categorized report:**

```
# Issue Review

**Analyzed:** [N] open issues
**Date:** [today]

## Resolved (can close)

### ISS-XXX: [description]
**Reason:** [Why resolved - code changed, implemented elsewhere]
**Evidence:** [What you found]

---

## Urgent (should address now)

### UAT-XXX: [description]
**Why urgent:** [What changed - blocking, causing problems]
**Recommendation:** Insert plan or add to current phase
**Effort:** [Quick/Medium/Substantial]

---

## Natural Fit for Upcoming Work

### ISS-XXX: [description]
**Fits with:** Phase [X] - [phase name]
**Reason:** [Same files, same subsystem]

---

## Can Wait (no change)

[List issue IDs with brief status]
```
</step>

<step name="offer_actions">
**Offer actions based on findings:**

Use AskUserQuestion with relevant options:

**If resolved issues exist:**
- "Close resolved" - Move to closed section
- "Review each first" - Show details before closing

**If urgent issues exist:**
- "Insert urgent phase" - Create decimal phase (e.g., 10.3)
- "Add to current plan" - Include in next plan
- "Defer anyway" - Keep as-is

**If natural fits exist:**
- "Note for phase" - Update issue with suggested phase
- "Keep as-is" - No annotation needed

**Always include:**
- "Done for now" - Exit without changes
</step>

<step name="execute_actions">
**Execute selected actions:**

**Closing resolved issues:**
1. For debt rows: set `status = "done"` in `.paul/DEBT.toml` with the check result as
   evidence. Do not delete the row — the diff is the record.
2. For `ISSUES.md`: move from "## Open Enhancements" to "## Closed Enhancements"
3. For UAT findings: mark resolved with the fixing plan/commit
4. Update STATE.md deferred line by running `debt.py` again, not by hand-counting

**Inserting urgent phase:**
- Suggest command: `/paul:plan 10.3 Address urgent issues [list]`

**Noting for phase:**
- Update issue entry with "Suggested: Phase [X]"
</step>

</process>

<success_criteria>
- [ ] All issue sources discovered (DEBT.toml first, then ISSUES.md and UAT files)
- [ ] Debt checks executed; rows that pass are discharged by editing `status`
- [ ] All open issues parsed
- [ ] Each issue analyzed against codebase
- [ ] Each issue categorized with reasoning
- [ ] Actions offered based on findings
- [ ] Files updated if actions taken
</success_criteria>
