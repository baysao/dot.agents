# Graphify rule

### Purpose
Use the local Graphify knowledge graph as the primary source for codebase
navigation, architecture questions, dependency tracing, and impact analysis.
Use ygrep (https://github.com/yetidevworks/ygrep) for exact content and
identifier search once the graph has narrowed the scope.

### When to use Graphify
Before grep, broad file reads, or guessing relationships, use Graphify when
the task involves:
- Finding where a symbol, module, API, or concept is used.
- Understanding how two components connect.
- Tracing call paths, imports, inheritance, or data flow.
- Assessing the likely blast radius of a change.
- Explaining an unfamiliar subsystem or architectural concept.

### Required workflow
1. Check that a graph exists:
   - Look for `graphify-out/graph.json`.
   - If missing, run: `graphify extract .` or ask the user before running it.
2. Prefer scoped graph queries over reading many files:
   - Use `graphify query "<natural-language question>"` for discovery.
   - Use `graphify path "<Node A>" "<Node B>"` to trace connections.
   - Use `graphify explain "<Node>"` to understand one concept and its edges.
3. For exact content, string, or identifier search inside the narrowed scope,
   prefer ygrep over raw grep (it is indexed, faster, and returns
   AI-friendly output):
   - `ygrep "<literal text>"` — literal match by default, special chars safe
     (`$var`, `{% block`, `->get(`).
   - `ygrep search "<pattern>" -r` — regex when needed.
   - `ygrep search "<query>" -e go -p internal/` — filter by extension/path.
   - First search in a workspace auto-builds the index; `ygrep index` to
     prebuild, `ygrep index --rebuild` after big changes.
4. Use `GRAPH_REPORT.md` only for high-level architecture review or when a
   scoped query is insufficient.
5. Read individual source files only to verify implementation details,
   inspect exact code, or make an edit.

### Query examples
- `graphify query "what connects authentication to the database?"`
- `graphify path "UserService" "DatabasePool"`
- `graphify explain "RateLimiter"`
- `graphify query "which modules depend on the billing service?"`
- `ygrep "ErrCodeInvestorValidation"`
- `ygrep search "func.*Upsert" -r -e go`

### Interpretation rules
- Treat `EXTRACTED` edges as explicit facts found directly in source.
- Treat `INFERRED` edges as resolved relationships that should be verified
  in source before making a consequential change.
- Do not claim a dependency or call path unless it appears in the graph or
  has been confirmed in source.
- If a node name is ambiguous, inspect the candidates returned by Graphify;
  do not silently choose one.

### Editing workflow
Before changing a core service, shared module, public API, database model,
or cross-cutting concern:
1. Run a Graphify query to identify consumers and related components.
2. Trace the relevant path with `graphify path`.
3. Read the directly affected files.
4. State the expected impact in the implementation plan.
5. After implementation, recommend updating the graph:
   `graphify update .`

### Repository conventions
- Respect `.gitignore`, `.graphifyignore`, and `.graphifyrc`.
- Do not commit generated artifacts unless the team explicitly chooses to:
  `graphify-out/`, `graph.html`, `GRAPH_REPORT.md`, and `graph.json`.
- For ambiguous file extensions, use `.graphifyrc` language declarations
  instead of relying on defaults.

### Fallback
If Graphify is unavailable, no graph exists, or a command fails:
- Say so explicitly.
- Fall back to ygrep for content search, then targeted source reading.
- Do not fabricate graph results, node names, paths, or edge types.

# graphify
- **graphify** (`~/.claude/skills/graphify/SKILL.md`) - any input to knowledge graph. Trigger: `/graphify`
When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

