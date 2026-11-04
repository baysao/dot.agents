---
name: paul:register
description: Generate paul.json for an existing PAUL project that predates v1.1 satellite manifest support
argument-hint:
allowed-tools: [Read, Write, Bash]
---

<objective>
Generate `.paul/paul.json` for an existing project that has a `.paul/` directory but no satellite manifest.

**When to use:** Projects initialized before paul-framework v1.1 that are missing `paul.json`. Required so PAUL commands can resolve the project manifest.
</objective>

<execution_context>
@~/.agents/paul-framework/workflows/register-manifest.md
</execution_context>

<context>
Current directory (check for .paul/ and existing paul.json)
</context>

<process>
Follow workflow: @~/.agents/paul-framework/workflows/register-manifest.md

A legacy project predates the debt store: create `.paul/DEBT.toml` here too if it is missing (header comment + `Schema:` pointer to `~/.agents/paul-framework/templates/DEBT.toml.md`, no rows), so the first deferral has somewhere machine-checkable to go.
</process>

<success_criteria>
- [ ] .paul/paul.json created with correct project name and current state
- [ ] Manifest written and readable by PAUL commands
- [ ] `.paul/DEBT.toml` exists and parses with `scripts/debt.py` (created empty if absent)
</success_criteria>
