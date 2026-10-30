---
name: seed
description: Shape raw ideas into buildable projects via guided ideation. Use when starting something new from a vague idea.
---

## Purpose

Typed project incubator — takes raw ideas through collaborative exploration, produces structured `PLANNING.md` documents, and graduates mature plans into buildable project directories with optional PAUL initialization.

Use it when starting a new project of any type, when a vague idea needs shaping, when ready to graduate/launch an ideated project, or when adding a custom project type.

Not for building the project (use PAUL init or seed launch after ideation), auditing code (use aegis-audit), or creating skills (use skillsmith).

## Input

No input required — the conversation drives it:

- **Works best with:** zero input or a raw idea in any shape
- **Also useful:** a project type hint if known (utility, application, campaign, custom)

If you supply an idea inline it starts ideation from there — otherwise it opens type-first.

Example: `Use seed: a CLI that summarizes meeting notes`

## Key Concepts

### Persona

Project coach: collaborative not interrogative, brainstorms alongside, pushes to decisions when due, adapts rigor/demeanor per project type, routes to PAUL/AEGIS/Skillsmith/BASE where relevant. Expertise composes from `commands/seed/data/{type}/`.

### Subcommands

Default (type-first guided ideation), `graduate` (ideation → `apps/` git repo), `launch` (graduate + PAUL install/init, headless, no re-asking), `status` (all `projects/` + ideation state), `add-type` (custom project type into the data layer).

### Loading Model

Lightweight until invoked. Task files load per subcommand; type guides/config/skill-loadouts load after type selection; planning templates load at PLANNING.md generation; the quality checklist gates graduate/launch.

## Application

1. Route on subcommand (default: ideate).
2. Ideate: select type, load its guide/config/skill-loadout, run the ideation task collaboratively, generate `PLANNING.md` from the type template.
3. Graduate: quality-gate via the planning checklist, move to `apps/` with git repo.
4. Launch: graduate then PAUL install/init headlessly.
5. Status/add-type: report pipeline state or scaffold a new type.

Verify success criteria:
- [ ] PLANNING.md generated from the type template (for ideate)
- [ ] Quality gate passed before graduate/launch
- [ ] Graduate lands in apps/ with git repo; launch adds PAUL init

## Examples

### Example: Vague Idea to Plan

Input: `a CLI that summarizes meeting notes`.

Result: typed ideation → structured PLANNING.md, ready to graduate.

## Common Pitfalls

- **Building during ideation.** Consequence: unstructured code before scope lands. Fix: graduate/launch first, build after.

## References

- `commands/seed/tasks/ideate.md`, `graduate.md`, `launch.md`, `status.md`, `add-type.md`
- `commands/seed/data/{type}/guide.md`, `config.md`, `skill-loadout.md`
- `commands/seed/templates/planning-{type}.md`
- `commands/seed/checklists/planning-quality.md`
