<purpose>
Show the project ideation pipeline — what's in docs/projects/, what's ready to graduate, and what's already been graduated.
</purpose>

<user-story>
As a builder with multiple ideas in progress, I want to see which projects are in ideation, which are ready to graduate, and which have already graduated to the root project, so that I can decide what to work on next.
</user-story>

<when-to-use>
- Want to see all projects in the pipeline
- Deciding which ideation to continue or graduate
- Checking if a project has already been graduated
</when-to-use>

<steps>

<step name="scan_projects">
## Scan Pipeline

Scan `docs/projects/` for directories containing `PLANNING.md`. For each project found, extract:

1. **Name** — directory name
2. **Type** — read Type metadata from PLANNING.md header
3. **Created** — file creation date of PLANNING.md
4. **Graduated** — check if PLANNING.md contains a `**Graduated:**` line at the bottom (graduation happens in place at the root project, so this note is the single graduation signal — do not scan for `apps/`)

If `docs/projects/` doesn't exist or is empty: "No projects in the pipeline. Run `/seed` to start one."
</step>

<step name="display_pipeline">
## Display Pipeline

Present results as a formatted table:

```
Project Pipeline
═══════════════════════════════════════════════════
Name              Type            Status
───────────────────────────────────────────────────
{name}            {type}          Ready for /seed graduate
{name}            {type}          Graduated → root project
{name}            {type}          In progress (no Type yet)
═══════════════════════════════════════════════════
{N} projects | {M} ready to graduate | {K} graduated
```

**Status logic:**
- Has Type + content depth → "Ready for /seed graduate"
- Has graduation note → "Graduated → root project"
- Missing Type or very thin → "In progress"

If any projects are ready to graduate, suggest: "Run `/seed graduate {name}` to graduate it to the root project."
</step>

</steps>

<output>
- Formatted pipeline table displayed to user
- No files created or modified (read-only)
</output>

<acceptance-criteria>
- [ ] Scans docs/projects/ for directories with PLANNING.md
- [ ] Extracts name, type, and graduation status per project
- [ ] Displays formatted pipeline table
- [ ] Identifies graduated projects (checks for graduation note)
- [ ] Read-only — does not modify any files
- [ ] Handles empty pipeline gracefully
</acceptance-criteria>
