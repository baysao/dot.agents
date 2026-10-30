---
name: paul-unify
description: Reconcile plan vs actual and close the PAUL loop. Use after APPLY to create SUMMARY.md. Also use for late-reconcile — STATE says pending/awaiting but git shows the work landed (missing SUMMARY, stale loop-position) — and when the user says "continue" / "next steps" after a handoff.
metadata:
  opencode/slash: "true"
---

## Purpose

Reconcile plan versus actual results, create `SUMMARY.md`, and close the loop. Documents what was built, decisions made, and deferred issues.

Use it after APPLY phase completes. Mandatory — never skip UNIFY.

## Input

Bring the plan target:

- **Works best with:** a plan path (e.g. `.paul/phases/01-foundation/01-01-PLAN.md`)
- **Also useful:** nothing else; state is loaded from `.paul/STATE.md` and the PLAN itself

If you supply the path inline, unification starts there. With no input, it asks which plan to unify.

Example: `Use paul-unify: close .paul/phases/01-foundation/01-01-PLAN.md`

## Key Concepts

### Framework Sources of Truth

**Other harnesses.** These paths assume a Claude Code install at `~/.agents/paul-framework/`; any harness can read them there. If that directory is absent, read the same subpaths under `~/.agents/paul-framework/`. If neither exists, tell the user to install the PAUL framework (workflows/, templates/, references/) and stop — don't reinvent the workflow from memory.

- `~/.agents/paul-framework/workflows/unify-phase.md` — reconciliation workflow
- `~/.agents/paul-framework/templates/SUMMARY.md` — summary template

### BASE Integration

BASE is present when `.paul/config.md` shows `BASE: enabled` (or BASE integration status is enabled). When enabled, the reflect pass routes its output to the base graph:

- **Cross-skill behavior rules** (\"always/never do X when Y\") → `base rule add --domain <project> --text \"...\" --rationale \"...\" --keywords \"...\" --fires-on \"...\"`
- **Context-bound judgment calls** (\"we chose X for this project\") → `base decision log --domain <project> --decision \"...\" --rationale \"...\" --recall \"...\"`
- **Insights, corrections, commitments, shifts** → `base learn --domain <project> --type insight|correction|commitment|shift --text \"...\"`

The project domain name derives from the project folder (or `.paul/config.md` project name). The domain has a path trigger to `.paul/` so rules fire on PAUL project files. Record `base: N rules, M decisions, K learnings` in SUMMARY.md. If BASE is not enabled, fall back to `.paul/LEARNINGS.md`.

### Guard

If `SUMMARY.md` already exists alongside the plan, **reconcile — do not abort**. Some projects (check the repo's `AGENTS.md`) write SUMMARY.md during APPLY, so an existing file means "the work is done, the close-out still owes a reconciliation" — not "nothing to do". Update the existing SUMMARY with the AC result, skill audit, and reflect outcome, then close the loop. Report `Loop already closed. SUMMARY: {path}` only when the file already contains that reconciliation.

## Application

### Step 1: Validate Preconditions

1. Confirm PLAN.md exists at the given path.
2. Confirm APPLY was executed (tasks completed). **Verify against the repository, not STATE.md** — STATE records the last writer, not reality: run `git log --oneline --all -n 20 -- <plan-dir>` and check for the plan's files (`*-SUMMARY.md`, listed files_modified). A STATE line saying "awaiting approval+apply" while commits show the work landed is the late-reconcile case: the work is done, only the close-out (SUMMARY + state sync) still owes.
3. If SUMMARY.md exists, treat it as the SUMMARY to reconcile (see Guard) — update it, do not stop.
4. **Reconcile every loop-position claim the plan's name appears in**, not just the live progress bullet: the ASCII-art loop table, and every historical Session-Continuity block's `Resume pointer` / `pending` lines. Those are routing instructions for the next session, not narrative — a stale one routes resume at a closed plan. Strike them (`~~old~~` → point at the UNIFIED bullet) before closing.

### Step 2: Reconcile

Follow `unify-phase.md`. Compare plan to actual: completed as planned, deviations, decisions made, issues deferred.

**Smoke evidence from a dirty tree carries a contamination caveat.** When browser/smoke verification runs against the live dev server while other plans are uncommitted on the same tree (`git status` shows plan work in progress, or STATE marks another plan "chưa commit"), "it still works" does not prove *this* plan's work still works — the running bundle mixes both. Record the caveat in the SUMMARY's verification section (which uncommitted plans shared the tree), or refuse Pass without an isolated checkout (worktree/stash). tsc/build-green only proves the *current* tree compiles, not that the plan's commit is intact.

**The caveat applies whenever verification shares mutable state, not only a dirty tree.** A check deliberately skipped to protect a shared database, seed fixture, or running dev server is partial verification. Declare it partial in the SUMMARY and either name the compensating check (isolated fixture codes, a scripted request sequence, a mocked call) or promote it to a blocking open-risk. A clean `git status` does not turn a skipped write-path check into full proof. **A compensating check only counts when it exercises the same failure class AND the same layer (UI wiring vs logic) as the skipped check — a Go test does not prove a browser dialog/banner branch.**

**Skill-audit evidence grades only what it can observe.** When an earlier leg (e.g. APPLY in another session) left no invocation artifact, record the row as `unverifiable (warn-only)` — never infer a ✓ from a recap. **Silence on a plan-mandated skill is a recorded `gap` (AC failure), not `unverifiable`; silence on an optional skill is `unverifiable (warn-only)` — the plan checklist is the contract.** Each leg writes its invoked skills and gate results into the ledger `result` field or the SUMMARY *as it runs*, so the close-out never needs a manual hand-off. At UNIFY, never accept recap claims ("GATE OK", "PASS", "0 console errors") as proof: re-run whatever is still re-runnable (`npx tsc --noEmit`, a `tomllib` parse, `git diff --stat`). Anything that cannot be re-run stays unverifiable.

### Step 3: Create Summary

Create `SUMMARY.md` beside the PLAN: what was built, acceptance criteria results, deferred issues, decisions, files created/modified.

**A SUMMARY that admits "N FIX rounds via chat, no UAT file" owes one more artifact before closing.** `paul-plan-fix` hard-requires `{plan}-UAT.md`, so a chat-driven FIX chain leaves the ledger with N+ closed FIX entries and no single source for "were all issues ever resolved" — future greps for open issues still hit them. Synthesize a retrospective `{plan}-UAT.md` from the FIX-SUMMARY files (one entry per FIX, resolved-state), or mark the whole chain superseded in a later ledger entry. Either way, the SUMMARY links to it.

**Before flipping status to UNIFIED, reconcile sibling FIX plans against the ledger.** Glob `{plan}*-PLAN.md` beside the SUMMARY: FIX/FIX2/FIX3 siblings share one SUMMARY file, so a section can be missing for a round applied in an earlier session (the ledger `apply` entry exists, the SUMMARY text does not). For each sibling, require a matching `## Quick-FIX {id}` section; write the missing one from the ledger entry + that session's evidence before the flip. A frontmatter `status: UNIFIED` is not evidence the body is complete.

### pstack Close-out (automatic)

pstack is present when `.paul/pstack-models.md` or the global `~/.agents/pstack-models.md` exists, or the `poteto-mode` skill is invocable in this session. If present, write SUMMARY.md per the `technical-writing` skill, run `unslop` on the prose, and reference any `show-me-your-work` decision trail. Then run the `reflect` skill to mine this loop for durable learnings — a required close-out step, not an offer. Skip only when the loop was trivial (no corrections, no surprises, no new conventions) and record `reflect: skipped (trivial loop)` in SUMMARY.md. reflect's approval gate stands: skill edits land only on the user's explicit yes. **The gate follows the artifact:** if the project writes SUMMARY.md during APPLY, run the reflect pass there (or here, against that SUMMARY) so it is never skipped.

### BASE Close-out (automatic)

BASE is present when `.paul/config.md` shows `BASE: enabled` (or BASE integration status is enabled). If present, route the reflect pass's approved items directly to the base graph — no staging gate, rules go live immediately:

- **Cross-skill behavior rules** → `base rule add --domain <project> --text \"...\" --rationale \"...\" --keywords \"...\" --fires-on \"...\"` (injects on next matching prompt)
- **Context-bound judgment calls** → `base decision log --domain <project> --decision \"...\" --rationale \"...\" --recall \"...\"` (durable, revisitable)
- **Insights, corrections, commitments, shifts** → `base learn --domain <project> --type insight|correction|commitment|shift --text \"...\"` (queryable via `base recall`)

The project domain name derives from the project folder (or `.paul/config.md` project name). Record `base: N rules, M decisions, K learnings` in SUMMARY.md. If BASE is not enabled, fall back to `.paul/LEARNINGS.md`.

### base Task Close-out (automatic)

When the `base` binary resolves, list open base tasks, find the one whose name carries this plan's id prefix (created at APPLY Step 1.7), and `base task done <slug>`. One task per plan, never per PAUL task. If no matching task exists, skip silently. Loop state still lives in STATE.md; base is a convenience mirror, and on conflict `.paul/` wins. The `*base` memory sweep (handoff, learnings, decisions) already runs inside the reflect pass — this step only closes the plan's board task, it does not re-sweep memory.

### Step 4: Update State and Report

Update `STATE.md`: loop position PLAN ✓ → APPLY ✓ → UNIFY ✓, phase progress, duration, next action. Display the closed-loop report with plan, summary, and next step.

**Batch UNIFY increments by N, not by 1.** When N plans close in one run, `stats.total_plans` and `phase.plans_completed` each advance by N — the `+1` in toml-sync's trigger matrix is single-plan only. Confirm the delta against `git log -p .paul/paul.toml` precedent before writing (prior batches show +6, +14).

**UNIFIED is a bookkeeping claim, not a durability claim.** If the plan's files
are still uncommitted when the loop closes, say it as an explicit open-risk line
in the SUMMARY *and* in the close report: "UNIFIED ≠ landed, N files uncommitted
until the user commits". Dirt left as an environmental fact in the transcript is
invisible to the next session, which reads STATE.md and believes the work landed.

**Artifact-debt inventory is a required UNIFY step.** Before closing, list every untracked operational file the plan produced or touched but did not commit: plans, screenshots, helper scripts, migrations, HANDOFFs, `.base/` dirs. For each, record the landing decision: `commit now`, `stash`, `discard`, or `owner + due date`. A summary sentence "UNIFIED ≠ LANDED" without this inventory is not a step — it is a claim ahead of evidence.

**Reconcile against the repository, not against your own summary.** The SUMMARY
was written by the same hand as the plan, so it can only confirm itself. Check
`git log <plan-start-sha>..HEAD` and `git status` for what actually landed: a
"do not commit" boundary that the user later overrode, a file that was touched
but never listed, a claim the code does not support. When the plan's boundary
and the repository disagree, the repository wins and the summary records the
deviation (the ledger is append-only — a wrong earlier entry can only be
contradicted by a later one, never edited).

**Assert the closed state with a parser, not with the commit message.** A
commit titled "unify" proves nothing about the state files. After syncing,
parse them and check the facts: the manifest's `loop.position` (and that
`plan`/`plan_path` are gone if the workflow removes them), and that the
ledger holds a `unify` entry for this plan. A title that disagrees with the
parsed state is itself a finding — fix the state, and if the title is
already in history, say so in the summary.

**Propagate every deviation backwards before closing the loop.** A deviation
recorded only in the summary will be read as a rule by the next agent, while
the plan, the acceptance criteria, the repo instructions, and the learning
files still say the old thing. Before closing, check each deviation against
every place that states the rule (plan text, AC, `AGENTS.md`, learning files)
and update the ones that are wrong. Artifacts that contradict each other mean
the loop is not closed yet.

**Edit state files with the editor, then parse them with their parser.** The
project manifest rotates a long note across `note` → `note_prev` → `note_prev2`
keys, and the ledger is a long list of tables: assembling those values through
a shell heredoc corrupts escapes and structure (a stray character after a
closing quote, a duplicated key) in ways a tail-read never shows. Author the
edit as a file, apply it, then re-parse the **whole** file with its parser
(`tomllib` for TOML) and print the entry count - a parser rejects both a syntax
error and a duplicate key for free. **When the edit tool fails with "Found multiple matches" on a rotating-key TOML file (e.g. `note`/`note_prev`/`note_prev2`), the root cause is often pre-existing duplicate keys from a prior bad write — run `tomllib` on the whole file BEFORE adjusting `oldString`; do not fight the match ambiguity.**

Ledger appends: write with `Add-Content -Encoding utf8NoBOM` (never the default
`-Encoding utf8`, never an inline shell rewrite). When splitting ledger text,
split on the literal `[[entry]]` header only — a character-class regex like
`[^\[]*` silently truncates on bracketed values (`phase = [9]`). House entry
extras (`track`, `depends_on`, `result`) are part of the schema: clone the
previous entry's shape, not the reference template's.

A parser proves structure, not layout. A state file with human-read blocks
(ASCII-art progress, aligned columns) can pass every parser and still be
wrong: a patch anchored on a line number shifts when an earlier line grows,
and an empty needle (`replace("", new, 1)`) inserts at position 0 instead of
adding a line. Anchor every patch on a **unique fragment**, never on a line
number, and dump the rendered block and read it before writing.

Verify success criteria:
- [ ] SUMMARY.md created
- [ ] Reflect pass run, or trivial-skip line recorded
- [ ] STATE.md updated with loop closure
- [ ] User knows next action

## Examples

### Example: Close Completed Plan

Input: `.paul/phases/01-foundation/01-01-PLAN.md`

Result: SUMMARY.md beside the plan, STATE.md closed, next phase or plan announced.

## Common Pitfalls

- **Skipping UNIFY.** Consequence: loop never closes, STATE drifts. Fix: always unify before planning the next unit.
- **Thin summary.** Consequence: deferred issues and decisions are lost. Fix: record deviations, decisions, and deferred items every time.
- **Treating reflect as optional.** Consequence: every loop re-derives the same lessons. Fix: run the reflect pass, or spend one line proving the loop was trivial.

## References

- `~/.agents/paul-framework/workflows/unify-phase.md`
- `~/.agents/paul-framework/templates/SUMMARY.md`
- `.paul/STATE.md`
