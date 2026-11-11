<purpose>
Graduate a project and initialize PAUL in one step — the "easy button" from ideation to managed build.
</purpose>

<user-story>
As a builder ready to start building, I want to graduate my project and set up PAUL in a single command, so that I don't have to run separate graduation and initialization steps.
</user-story>

<when-to-use>
- Ideation is complete and you want to start building immediately
- You want PAUL-managed development (structured phases, plans, progress tracking)
- You prefer one command over running `/seed graduate` then `/paul:init` separately
</when-to-use>

<context>
@seed.md
@tasks/graduate.md (delegation target — launch wraps this flow)
</context>

<steps>

<step name="run_graduation" priority="first">
## Run Graduation

Execute the full graduation flow from `tasks/graduate.md` first.

All validation, quality checks, README synthesis, root-repo verification, and tracking updates happen there. Do NOT duplicate that logic here — delegate entirely.

Pass `$ARGUMENTS` through as the project name.

After graduation completes successfully, proceed to PAUL integration below.

<if condition="graduation fails or user exits during graduate flow">
Stop here. Do not proceed to PAUL integration. The graduate task handles its own error reporting.
</if>
</step>

<step name="offer_paul">
## Offer PAUL Integration

After graduation is complete, ask the user:

> "Project graduated to the root project (`$PROJECT_ROOT`). Want to initialize PAUL for a managed build?"
>
> PAUL gives you structured milestones, phases, plans, and progress tracking. Your PLANNING.md has enough detail to set up PAUL without re-answering questions.
>
> **Yes** — initialize PAUL now
> **No** — just the graduation is fine (you can run `/paul:init` later)

Wait for response.

<if condition="user declines">
Report graduation-only result:

> "Graduated: root project (`$PROJECT_ROOT`)"
> "Run `/paul:init` in the root project if you change your mind."

Exit.
</if>
</step>

<step name="check_paul_availability">
## Check PAUL Availability

Check if PAUL is installed via multiple paths:

1. **Skill path (preferred):**
   ```bash
   ls ~/.claude/commands/paul/plan.md 2>/dev/null
   ```

2. **Legacy framework path (fallback):**
   ```bash
   ls ~/.claude/paul-framework/ 2>/dev/null
   ```

<if condition="either path found">
Check for v1.4+ features (paul.toml support):
```bash
grep -l "paul.toml\|paul-toml" ~/.claude/commands/paul/*.md 2>/dev/null || grep -l "paul.toml\|paul-toml" ~/.claude/paul-framework/src/templates/*.md 2>/dev/null
```

- **If paul.toml references found:** PAUL v1.4+ detected. PAUL init can create paul.toml (not paul.json).
- **If not found:** PAUL pre-v1.4 detected. Display:
  ```
  ⚠️ PAUL detected but may be an older version. For full integration
  (paul.toml, domain tags), update PAUL:
  npx paul-framework@latest

  Proceeding with init using current version.
  ```
  Continue with init.
</if>

<if condition="neither path found">
Inform the user:

> "PAUL isn't installed yet."
>
> ```
> Install: npx paul-framework
> ```
>
> "Want to install it now, or skip PAUL for now? You can run `/paul:init` later."

Wait for response.

If user wants to install: run `npx paul-framework --global` then proceed.
If user declines: exit gracefully with graduation-only result.
</if>
</step>

<step name="headless_paul_init">
## Headless PAUL Init

Run `/paul:init` in the root project ($PROJECT_ROOT — graduation happens in place, there is no nested app directory) with headless context:

1. Read `docs/projects/{name}/{name}.md` — the finalized design document (single source, /paul:init's input file)
2. `$PROJECT_ROOT/README.md` (repo root) holds the re-synthesized brief for humans; `docs/projects/{name}/PLANNING.md` holds full planning depth

Pass this context to PAUL init with the instruction:

> "Use the design document `docs/projects/{name}/{name}.md` as the project brief — it is the single source of truth. Derive milestones, phases, and project structure from it. Do NOT re-ask questions that SEED and the design review already answered — the answers are in this document. Propose the project structure and ask for approval."

PAUL will propose a structure (milestones, phases, tech stack). The user reviews and approves — headless means no redundant questions, NOT no approval.

Wait for response (user approves or adjusts PAUL's proposed structure).
</step>

<step name="default_paul_integrations">
## Enable Default PAUL Integrations

After PAUL init is approved, configure the two integrations this workspace runs by default — apply them, do not ask:

1. **pstack preset** — invoke the `paul-flows` skill with subcommand `pstack` (writes the standard pstack mapping preset into `.paul/SPECIAL-FLOWS.md`, carries the R-4/R-5 debt rules, updates the PROJECT.md quick reference, records `pstack: enabled` in `.paul/config.md`). If pstack is not detected (no `.paul/pstack-models.md`, no global `~/.agents/pstack-models.md`, no `poteto-mode` skill invocable), invoke the `setup-pstack` skill first, then apply the preset.
2. **Security Audit toggle** — invoke the `paul-config` skill to enable the Security Audit integration with default profile `standard` (note the POSIX-host validator caveat). Trust-surface plans will name a guidance-mode review; critical/high findings land as phase-exit debt rows.

SonarQube, Enterprise Plan Audit, and XERJ stay opt-in — do not enable them here. Report both enabled integrations in the completion message; the user can disable either later via `/paul-config`.
</step>

<step name="report_completion">
## Report Completion

After PAUL initialization is approved:

```
Launched: {name}
Location: $PROJECT_ROOT (root project)
PAUL: Initialized with {milestone} — {N} phases
Integrations: pstack preset + Security Audit (profile: standard) enabled

Your project is ready for managed development.
Run /paul:plan to start Phase 1.

SEED v1.0 · Chris AI Systems · https://chrisai.cv/skool · https://youtube.com/@chris-ai-systems
```
</step>

</steps>

<output>
- Everything from tasks/graduate.md (root README re-synthesized, graduation note, root repo commit, tracking)
- `.paul/` directory at the root project (PROJECT.md, ROADMAP.md, STATE.md)
- `.paul/SPECIAL-FLOWS.md` with pstack preset + `.paul/config.md` with Security Audit enabled
- Project ready for `/paul:plan`
</output>

<acceptance-criteria>
- [ ] Delegates to tasks/graduate.md without duplicating logic
- [ ] Asks user about PAUL (not filesystem scan for decision)
- [ ] Checks PAUL framework availability before attempting init
- [ ] Prompts installation if PAUL not found
- [ ] Headless PAUL init passes the design doc (`docs/projects/{name}/{name}.md`) as input
- [ ] User still approves PAUL's proposed structure
- [ ] pstack preset applied via paul-flows (setup-pstack first if pstack not detected)
- [ ] Security Audit enabled via paul-config with default profile standard
- [ ] SonarQube / Enterprise Plan Audit / XERJ NOT enabled by default
- [ ] Graceful exit if user declines PAUL at any point
- [ ] Wait points at PAUL offer and structure approval
- [ ] No `apps/{name}/` directory created anywhere in the flow
</acceptance-criteria>
