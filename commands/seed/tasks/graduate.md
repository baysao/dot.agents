<purpose>
Graduate a completed ideation from docs/projects/{name}/ to the root project ($PROJECT_ROOT) — the repo the user builds in — by re-synthesizing the root README and recording the graduation. No nested app directory is created.
</purpose>

<user-story>
As a builder with a completed PLANNING.md, I want to graduate my project in place at the root project with a synthesized README, so that I can start building without manual setup or a nested directory.
</user-story>

<when-to-use>
- Ideation is complete and PLANNING.md exists in docs/projects/{name}/
- Ready to move from planning to building
- Want the root project's README re-synthesized as the full build brief
</when-to-use>

<context>
@seed.md
@checklists/planning-quality.md (quality gate — loaded before graduation)
</context>

<steps>

<step name="validate_input" priority="first">
## Validate Project

Check `$ARGUMENTS` for a project name.

**If no argument provided:**
Scan `docs/projects/` for directories containing PLANNING.md. List them:

> "Available projects ready for graduation:"
> - {name} ({type from PLANNING.md})
> - {name} ({type})
>
> "Which one? Or provide a name."

Wait for response.

**If argument provided:**
1. Confirm `docs/projects/{name}/PLANNING.md` exists — if not: "No PLANNING.md found at `docs/projects/{name}/`. Run `/seed` to create one first."
2. Confirm PLANNING.md does NOT already contain a `**Graduated:**` note — if it does: "This project was already graduated ({date}). Nothing to do."
3. If either check fails, stop.
</step>

<step name="quality_check">
## Quality Gate

Read `docs/projects/{name}/PLANNING.md` and extract:
- **Type** metadata field — any name with a `data/{type}/` directory (`ls data/`), which includes custom types from `/seed add-type`
- Overall content depth

Reference `checklists/planning-quality.md` to assess whether the PLANNING.md is rich enough for a clean graduation and potential headless PAUL init.

<if condition="Type metadata is missing">
Infer type from content, or ask: "I can't find a Type field in this PLANNING.md. What type of project is this?" — listing `data/` rather than the five built-ins.

Wait for response.

**If the named type has no `data/{type}/` directory:** stop and say so. The PLANNING.md can still graduate — the type only drives the quality gate — but a missing config means no required-section authority to check against, so the gate is "universal checks only", and you must say that explicitly rather than reporting a pass.
</if>

<if condition="PLANNING.md appears too thin">
Warn the user:

> "This PLANNING.md looks light — it may not have enough detail for a strong README or future PAUL init. Want to go back to `/seed` to flesh it out, or graduate as-is?"

Wait for response. If user wants to proceed, continue. If not, exit with suggestion to run `/seed`.
</if>
</step>

<step name="prepare_root">
## Prepare Root Project

The root project ($PROJECT_ROOT) is the build location — no nested app directory and no new git repo. Verify the root repo exists:

```bash
git rev-parse --is-inside-work-tree
```

- **If it is a git repo:** nothing to create — proceed.
- **If not:** ask "The root project isn't a git repo yet. Run `git init` here, or continue without git?" and act on the answer.

Do NOT create `apps/{name}/` — the era of nested app scaffolds is over; the design doc and planning artifacts already live under `$PROJECT_ROOT/docs/projects/{name}/`.
</step>

<step name="synthesize_readme">
## Synthesize README

Read `docs/projects/{name}/PLANNING.md` fully. Re-synthesize **`$PROJECT_ROOT/README.md`** (the repo root contract — if `/egm-bootstrap` wrote a planning-stage contract there, apply the Correction & Modification Policy: replace its contract tables with the full graduation brief, keep the title and status header). The root README is the one project brief everyone and PAUL reads. Do NOT copy the design document anywhere — it stays single-source at `docs/projects/{name}/{name}.md` (the design doc `/egm-draft` wrote) and that path is what `/paul:init` consumes.

**Common sections (all types):**
- Title and one-line description
- Type, Skill Loadout, Quality Gates metadata
- Overview — concise summary of what and why
- Design Decisions — resolved decisions (numbered)
- Implementation Phases — phase breakdown (or "N/A" for small projects)
- Open Questions — unresolved items
- References

**Type-specific sections to add:**

| Type | Additional Sections |
|------|-------------------|
| Application | Stack, Deploy, Data Model, API Surface, Architecture, UI/UX |
| Workflow | Scope Definition, Integration Map, Interaction Design, Output Artifacts |
| Client | Client name, Business Context, Conversion Strategy, Timeline, Tech Approach |
| Utility | Location, Interface (invocation/input/output), Done Criteria |
| Campaign | Goal, Deliverables List, Timeline, Success Metrics |

**Synthesis guidelines:**
- Remove brainstorming artifacts, iteration history, abandoned ideas
- Keep all resolved design decisions
- Keep technical architecture details
- Keep implementation phases
- Preserve tables and structured data (information-dense)
- Preserve Type and Skill Loadout metadata — PAUL uses this for configuration
- The README should be comprehensive enough to run `/paul:init` against
- The design doc at `docs/projects/{name}/{name}.md` is what `/paul:init` receives as input

Present the generated README to the user:

> "Here's the README I synthesized from your PLANNING.md. Take a look — anything to adjust?"

Wait for response.

<if condition="user requests changes">
Apply edits and re-present until approved.
</if>
</step>

<step name="finalize">
## Finalize Graduation

1. **Write the re-synthesized brief** to `$PROJECT_ROOT/README.md` (repo root)

2. **Note graduation in PLANNING.md** — append to `docs/projects/{name}/PLANNING.md`:
   ```
   ---
   **Graduated:** {today's date}
   **Location:** `$PROJECT_ROOT` (root project)
   **README:** `$PROJECT_ROOT/README.md`
   ```

3. **Commit the graduation in the root repo** (root is the build repo — no separate scaffold):
   ```bash
   git add README.md docs/projects/{name}/PLANNING.md
   git commit -m "docs: graduate {name} — README re-synthesized from PLANNING.md"
   ```
   If the root repo has other unrelated staged/unstaged changes, stage only these two files. If not a git repo (user opted out in `prepare_root`), skip silently.

4. **Report:**
   ```
   Graduated: docs/projects/{name}/ → $PROJECT_ROOT (root project)
   README: $PROJECT_ROOT/README.md (root contract re-synthesized)
   Design doc: docs/projects/{name}/{name}.md (/paul:init input, single source)
   Git: Root repo commit created

   Next steps:
   - `/paul:init` in the root project to start a managed build, then enable the default integrations: `paul-flows pstack` preset + `paul-config` Security Audit (profile: standard)
   - `/seed launch {name}` does all of this automatically (graduate + PAUL init + default integrations)

   SEED v1.0 · Chris AI Systems · https://chrisai.cv/skool · https://youtube.com/@chris-ai-systems
   ```
</step>

</steps>

<output>
- `$PROJECT_ROOT/README.md` — root contract re-synthesized into the graduation brief
- `docs/projects/{name}/{name}.md` — finalized design doc (single source, /paul:init input; already exists, not moved)
- Graduation note appended to `docs/projects/{name}/PLANNING.md`
- Root repo commit recording the graduation
</output>

<acceptance-criteria>
- [ ] Input validated: PLANNING.md exists, no prior Graduated note
- [ ] Quality gate checked before graduation
- [ ] Type extracted from PLANNING.md metadata
- [ ] README synthesized with type-specific sections (not copied verbatim)
- [ ] Root repo verified (no `apps/{name}/` created, no nested git init)
- [ ] Design doc NOT copied — stays single-source at docs/projects/{name}/{name}.md
- [ ] Graduation date noted in original PLANNING.md, Location = root project
- [ ] Wait points present at key decisions (git init question, quality warning, README review)
</acceptance-criteria>
