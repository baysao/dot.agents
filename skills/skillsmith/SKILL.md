---
name: skillsmith
description: Build consistent skills via guided discover-scaffold-distill-audit workflows. Use when creating or maintaining a skill.
---

## Purpose

Meta-skill for creating and maintaining skills. Guides discovery (what to build), scaffolding (compliant files), distilling (chunking source material), and auditing (compliance) using standardized syntax specs.

Use it when building a new skill from scratch, documenting design decisions, generating a compliant directory, distilling raw material, or auditing compliance. Not for using existing skills (invoke directly), runtime testing, or post-creation file edits (edit directly).

## Input

No input required — pick a workflow:

- **Works best with:** a subcommand: `discover`, `scaffold`, `distill`, or `audit`
- **Also useful:** the skill idea or source material at hand

Example: `Use skillsmith: discover a skill for API pagination`

## Key Concepts

### Persona

Senior skill architect: structured interviewer (one question group at a time), opinionated on conventions (cites specs), concise, tabular output. Knows skill anatomy, placeholder conventions (`[square]` prose vs `{curly}` variables), routing patterns (always-load / on-command / on-demand), and tiers (suite / standalone / task-only).

### Subcommands

`discover` (guided design interview), `scaffold` (directory from spec), `distill` (raw material → framework chunks), `audit` (compliance check).

### Loading Model

Lightweight until invoked. Task files load per subcommand; spec files (entry-point, tasks, templates, frameworks, context, checklists, rules) load on demand when referenced.

## Application

1. Route on subcommand (default: ask which of discover/scaffold/distill/audit).
2. Discover: interview one group at a time until the design is captured.
3. Scaffold: generate the compliant directory from the spec.
4. Distill: chunk source material into framework pieces.
5. Audit: check the skill against syntax specs and report corrections by spec name.
6. Verify: the skill directory is compliant and spec references resolve.

## Examples

### Example: New Skill

Input: `discover` with a pagination idea.

Result: captured design ready to scaffold into a compliant skill.

## Common Pitfalls

- **Editing skill files through the suite.** Consequence: roundabout changes. Fix: edit files directly after creation.

## References

- `commands/skillsmith/tasks/discover.md`, `scaffold.md`, `distill.md`, `audit.md`
- `skillsmith-specs/entry-point.md`, `tasks.md`, `templates.md`, `frameworks.md`, `context.md`, `checklists.md`, `rules.md`
