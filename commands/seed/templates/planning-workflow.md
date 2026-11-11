---
description: "{One-line description from ideation}"
type: Planning
about: "{project-name}"
project_type: "workflow"
seed_version: "1.0.0"
seed_source: "https://chrisai.cv/skool"
---

# {Project Name}

> Building {this workflow} to {fix the broken/slow/missing step} — {measurable effect on the work it touches}.

**Created:** {date}
**Type:** Claude Code Workflow
**Skill Loadout:** {skills relevant to building this — e.g., /paul:audit}
**Quality Gates:** {quality checks — e.g., governance review, integration testing}

---

## Problem Statement

{What workflow pain or gap does this solve? Be specific about what's broken, slow, or missing. Evidence beats opinion — how often does this hurt, and who hits it? Tag unvalidated claims inline as 🔶 **Assumption** until observed in real use.}

### Who Hits This?
{Which sessions, projects, or roles run into the gap?}

### What's Broken Today?
{The current manual steps, failure mode, or missing capability.}

### Cost of the Pain
{Time lost, errors introduced, or steps skipped — rough numbers are fine.}

---

## Success Metrics

{How do we know the workflow is worth keeping?}

### Primary Metric
**{e.g., time per run of the task / error rate / adoption (runs per week)}**
- **Current:** {manual baseline}
- **Target:** {goal}
- **Measured:** {how — timing a run, log count, usage over first N weeks}

### Guardrail Metrics
{What must not regress — existing flows the workflow touches.}

- {e.g., existing commands still behave identically; no new required steps for users who don't opt in}

---

## Scope Definition

{What components make up this workflow? Check all that apply and describe each.}

### Components
- [ ] Slash command(s): {list}
- [ ] Skill(s): {list}
- [ ] CARL domain(s): {new or modified}
- [ ] Hook(s): {list}
- [ ] MCP server tool(s): {list}
- [ ] Templates / file generators: {list}
- [ ] Modifications to existing commands: {list}

### Out of Scope
- {Explicitly excluded items}

---

## Integration Map

### Systems Touched

| System | How It's Touched | Changes Needed |
|--------|-----------------|----------------|
| {e.g., CARL} | {e.g., new domain, rule updates} | {specific changes} |
| {e.g., PAUL} | {e.g., new input format} | {specific changes} |
| {e.g., Existing commands} | {e.g., /graduate modification} | {specific changes} |

### Systems NOT Touched
- {List systems explicitly unaffected to prevent scope creep}

---

## Interaction Design

{Map the user experience as conversation flows.}

### Entry Point
```
User: /{command}
Claude: {what happens}
```

### Conversation Flow
{Step-by-step: what Claude asks, what user provides, what Claude does with it. Include branching logic if applicable.}

### Session End
{What artifacts are produced? What does Claude report? What's the next step prompt?}

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| {file/command/domain} | {path} | {what it does} |

---

## Downstream Handoff

{How does the output connect to the next stage? What metadata travels? What does the next tool expect?}

---

## Skill/Tool Discovery

{Skills or tools that could enhance this workflow but don't exist yet.}

| Skill | When It Would Fire | What It Would Do |
|-------|-------------------|-----------------|
| {name} | {trigger} | {description} |

---

## Edge Cases & Constraints

{What shouldn't this workflow do? When does it NOT apply? What happens with unexpected input?}

- {Edge case and how to handle it}

---

## Design Decisions

1. **{Decision}**: {choice} — {rationale}

---

## Open Questions

1. {Question}

---

## Next Actions

- [ ] {First concrete step}

---

## References

- {Links, related files, prior art}

---

*Last updated: {date}*
*Planned with SEED v1.0 · Chris AI Systems · For the official Agentic OS and to permanently remove attribution, visit https://chrisai.cv/skool*
