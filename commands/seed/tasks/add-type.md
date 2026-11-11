<purpose>
Guide the creation of a new project type for SEED's composable data layer — produces guide.md, config.md, and skill-loadout.md in a new data/{type}/ directory.
</purpose>

<user-story>
As a builder with a project category SEED doesn't cover, I want to add a custom type with its own conversation guide and rigor settings, so that /seed ideate gives me type-appropriate guidance for my specific kind of project.
</user-story>

<when-to-use>
- The 5 built-in types don't fit your project (enumerate them with `ls data/` — the listing, not this sentence, is authoritative)
- You have a recurring project category that deserves its own guided flow
- You want type-specific rigor, demeanor, and section structure
</when-to-use>

<context>
@data/application/guide.md (reference for guide structure)
@data/application/config.md (reference for config structure)
@data/application/skill-loadout.md (reference for loadout structure)
</context>

<steps>

<step name="get_type_name" priority="first">
## Name the Type

Ask for the new type name — lowercase, hyphenated, singular (e.g., "microservice", "chrome-extension", "course").

**Enumerate existing types from disk, never from memory:**

```bash
ls data/
```

Every directory name is an existing type. Check the name against that listing:
- **If exists:** "{name} already exists as a type. Want to edit it, or pick a different name?"
- **If new:** Proceed.

Show the listing you actually read:
> "Current types: {comma-separated from ls data/}"
> "What's the new type called?"

Validate the name before writing: lowercase, hyphenated, singular. Reject a name with spaces, uppercase, or a directory separator — it becomes a path segment under `data/` and under `templates/planning-{type}.md`.

Wait for response.
</step>

<step name="define_sections">
## Define Conversation Sections

Ask the user to define the conversation sections for this type. These become the guide.md structure.

> "What sections should the ideation conversation cover for a **{type}** project?"
>
> For reference, here's how existing types are structured — read them rather than trusting this:
>
> ```bash
> for d in data/*/; do
>   printf '%s: ' "$(basename "$d")"
>   grep -c '^## Section' "$d/guide.md" 2>/dev/null
>   grep '^## Section' "$d/guide.md" 2>/dev/null | sed 's/^## Section [0-9]*: //'
> done
> ```
>
> List your sections in order of importance. Each will get an Explore prompt and a Suggest prompt.

Wait for response.
</step>

<step name="define_config">
## Configure Rigor and Demeanor

Ask about the type's personality:

> "How should SEED behave during **{type}** ideation?"
>
> **Rigor level:** (how thorough)
> - `tight` — Fast, resist expansion (like utilities)
> - `standard` — Balanced exploration (like workflows, clients)
> - `deep` — Thorough, architecture matters (like applications)
> - `creative` — Loose, generative (like campaigns)
>
> **Demeanor:** One sentence describing the coaching style for this type.
>
> **Required sections:** Which of your sections must be covered? (Others become optional)

Wait for response.
</step>

<step name="create_guide">
## Create Guide File

Generate `data/{type}/guide.md` with the user's sections. For each section:

```markdown
## Section {N}: {Name}
**Explore:** {question prompts based on what the user described}
**Suggest:** {coaching suggestions — what to offer when the user is stuck}
**Depth:** {required | optional}
```

Present the draft guide for review:

> "Here's the conversation guide I drafted for **{type}**. Each section has an Explore prompt and a Suggest prompt. Anything to adjust?"

Wait for response.

Apply any edits the user requests before writing.
</step>

<step name="create_supporting_files">
## Create Config and Skill Loadout

**Create data/{type}/config.md:**
```markdown
# {Type} — Configuration

| Setting | Value |
|---------|-------|
| Rigor | {from step 3} |
| Demeanor | {from step 3} |
| Sections | {count} |

## Required Sections
- {list from step 3}

## Optional Sections
- {list from step 3}
```

**Create data/{type}/skill-loadout.md:**

> "Which ecosystem tools are useful for **{type}** projects? Here are some options:"
> - PAUL, AEGIS, Skillsmith, ui-ux-pro-max, sonarqube
> - content-flywheel-strategist, geo
>
> "List the relevant ones with priority (required/recommended/optional)."

Wait for response.

Write the skill-loadout.md with the user's selections.
</step>

<step name="verify_consistency">
## Verify the Three Files Agree

The three files are read independently at different moments (config for rigor and required sections, guide for section prompts, loadout for tools), so a disagreement is silent until ideation runs and skips a section nobody prompts for — or the quality gate demands a section the guide never asks about.

Check, and fix before continuing:

| Must match | In | Against |
|---|---|---|
| Section count | `config.md` `\| Sections \|` | number of `## Section` headings in `guide.md` |
| Section names | `config.md` Required + Optional lists | `guide.md` section headings, in order |
| `Depth:` values | each `guide.md` `**Depth:**` line | `config.md` required/optional split |
| Required count | `config.md` Required list | total minus Optional list |
| Rigor | `config.md` | one of `tight`, `standard`, `deep`, `creative` |

```bash
grep -c '^## Section' data/{type}/guide.md
grep '^## Section' data/{type}/guide.md
grep '^| Sections' data/{type}/config.md
grep -n 'Depth:' data/{type}/guide.md
```

Then verify mechanically:

- every `Depth: required` section appears in Required Sections, and every `Depth: optional` in Optional;
- no section is in `config.md` but missing from `guide.md`, or the reverse;
- the `Sections` count equals the `## Section` heading count;
- every `## Section` has both **Explore:** and **Suggest:** — a section with no Suggest prompt strands the user the moment they get stuck, which is exactly the failure `add-type` exists to prevent.

Report any mismatch and fix it before moving on. Do not proceed to the template with a known disagreement: the template is generated *from the guide*, so a guide that disagrees with config produces a PLANNING.md that fails its own quality gate.
</step>

<step name="create_template">
## Generate Planning Template

Generate `templates/planning-{type}.md` from the user's defined sections so the full ideate → graduate round-trip works immediately.

**Structure:**

1. **YAML frontmatter** (same as built-in types):
   ```yaml
   ---
   description: "{One-line description from ideation}"
   type: Planning
   about: "{project-name}"
   project_type: "{type}"
   seed_version: "1.0.0"
   seed_source: "https://chrisai.cv/skool"
   ---
   ```

2. **Title and metadata block:**
   ```markdown
   # {Project Name}

   > {One-line description}

   **Created:** {date}
   **Type:** {Type (capitalized)}
   **Skill Loadout:** {from skill-loadout.md selections}
   **Quality Gates:** {infer from type or use "TBD"}
   ```

3. **For each section defined in guide.md**, create a corresponding template section:
   ```markdown
   ---

   ## {Section Name}

   {Placeholder prompt derived from the section's Explore question}
   ```

4. **Common closing sections** (all types get these):

   Built-ins close with `## Skill Loadout & Quality Gates`, `## Design Decisions`, `## Open Questions`, `## Next Actions`, `## References`, and `utility`/`campaign` add `### PAUL Decision`. Mirror that so `/seed graduate` and `/seed launch` find what they read: the graduate gate looks for design decisions, open questions, next actions, and the skill loadout, and PAUL init reads the phase breakdown.

   ```markdown
   ---

   ## Skill Loadout & Quality Gates

   ### Skills Used During Build

   {from skill-loadout.md}

   ### Quality Gates

   {what must be true before this counts as done}

   ---

   ## Design Decisions

   | # | Decision | Rationale |
   |---|----------|-----------|

   ---

   ## Open Questions

   - {Unresolved items from ideation}

   ---

   ## Next Actions

   - [ ] {First concrete step}

   ---

   ## Implementation Phases

   {High-level phase breakdown — or "TBD during /paul:plan"}

   ---

   ## References

   - {Links, related files, prior art}

   ---

   *Last updated: {date}*
   *Planned with SEED v1.0 · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
   ```

Present the generated template to the user:
> "Here's the planning template I generated for **{type}**. Anything to adjust?"

Wait for response. Apply edits if requested.

Write to `templates/planning-{type}.md`.
</step>

<step name="confirm_and_report">
## Confirm

Run a real round-trip smoke test before claiming the type works. `/seed` routes by enumerating `data/`, so prove it with the same call the router makes:

```bash
ls data/{type}/          # guide.md, config.md, skill-loadout.md
test -f templates/planning-{type}.md && echo template-ok
```

Then confirm the listing the user will see during ideation now contains the new type.

Report what was created:

```
New type created: {type}

Files:
  data/{type}/guide.md             ({N} sections)
  data/{type}/config.md            (rigor: {level}, {R} required / {O} optional)
  data/{type}/skill-loadout.md     ({T} tools)
  templates/planning-{type}.md     ({N} sections from guide)

Routing: /seed now lists {type} (it enumerates data/, so no registry to update).
Verify:  /seed {type} starts at "{first section}" with {rigor} rigor.
Gate:    data/{type}/config.md is the required-section authority for /seed graduate and /seed launch.

SEED v1.0 · Chris AI Systems · https://chrisai.cv/skool · https://youtube.com/@chris-ai-systems
```

Do not say "immediately available" without the two commands above having run. If either fails, the type is not created yet — finish the file that is missing.
</step>

</steps>

<output>
- `data/{type}/guide.md` — conversation sections with Explore + Suggest
- `data/{type}/config.md` — rigor, demeanor, required/optional sections
- `data/{type}/skill-loadout.md` — ecosystem tool recommendations
- `templates/planning-{type}.md` — PLANNING.md template with frontmatter and sections from guide
</output>

<acceptance-criteria>
- [ ] New type name validated against `ls data/` (lowercase, hyphenated, singular, no collision, no path separator)
- [ ] Guide created with Explore + Suggest per section
- [ ] Config created with rigor level and required/optional sections
- [ ] Skill loadout created with prioritized tool recommendations
- [ ] Planning template auto-generated from guide sections with standard frontmatter and closing sections
- [ ] Template includes provenance footer
- [ ] Wait points at every user input boundary
- [ ] Three files cross-checked: section count, names, `Depth` values, and required/optional split agree
- [ ] Smoke test ran: `ls data/{type}/` shows three files, `templates/planning-{type}.md` exists
- [ ] `/seed` enumerates `data/` so the type is routable with no registry edit — verified, not assumed
- [ ] A type whose config is later deleted degrades to "universal checks only" at the graduate gate, stated aloud
</acceptance-criteria>
