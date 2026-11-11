# Project Config Template

Template for `.paul/config.md` - project-specific configuration and integrations.

**Purpose:** Store project settings and optional integration flags. Allows PAUL to adapt behavior based on available tools.

---

## File Template

```markdown
# Project Config

**Project:** [project-name]
**Created:** [YYYY-MM-DD]

## Project Settings

```yaml
project:
  name: [project-name]
  version: [current-version or "0.0.0"]
```

## Integrations

Optional integrations that enhance PAUL functionality.

### SonarQube

Code quality scanning and static analysis.

```yaml
sonarqube:
  enabled: false
  project_key: [project-key]  # Must match sonar-project.properties
  server_url: http://localhost:9000  # Optional, for reference
```

**When enabled:**
- `/paul:quality-gate` runs scans and updates CONCERNS.md
- Quality metrics inform planning decisions
- Issues feed into tech debt tracking

**Requirements:**
- SonarQube server running (local or cloud)
- `sonar-project.properties` in project root
- SonarQube MCP server configured

### Enterprise Plan Audit

Architectural review gate between PLAN and APPLY phases.

```yaml
enterprise_plan_audit:
  enabled: false
```

**When enabled:**
- `/paul:plan` suggests running `/paul:audit` before APPLY
- `/paul:audit` performs enterprise-grade architectural review
- Must-have and strongly-recommended findings auto-applied to plan
- Audit report saved alongside PLAN.md as `{NN}-{PP}-AUDIT.md`

**Requirements:**
- No external dependencies (runs within Claude Code session)
- Best suited for commercial, regulated, or enterprise-grade projects

### Security Audit

Source-first vulnerability review, scoped to the diff by default.

```yaml
security_audit:
  enabled: false
  default_profile: quick  # quick | standard | deep
```

**When enabled:**
- A plan touching auth, input parsing, a new endpoint, a path, or a dependency names a guidance-mode review as a task
- `/paul:security` runs a full audit when a phase ships or a milestone closes
- Confirmed critical/high findings become `blocking = "phase-NN-exit"` debt rows, so the existing phase-exit gate refuses the close until they are fixed
- `needs_validation` findings become `kind = "reopen"` rows with no severity

**Requirements:**
- `~/.agents/skills/security-audit/SKILL.md` installed
- POSIX (Linux/macOS/WSL) to validate `findings.json` and `coverage-ledger.json`; on Windows the validators cannot read their input and a run is marked `incomplete`

### XERJ Discovery & Search

Zero-config code search, definitions, and passage-level citations for planning. The prefix is **asked for at enable time and stored** — it is the only thing that ties searches to this project's index.

```yaml
xerj:
  enabled: false
  index_prefix: [asked-at-enable]  # e.g. akka-pricehub — never defaulted
  index_root: "."                  # folder passed to autoindex (`.` = repo root)
  index_cwd: "[dir autoindex runs from]"  # absolute; makes index_root replayable
  binary_path: ""                  # only needed when `xerj` is not on PATH
```

**When enabled:**
- `/paul:map` indexes the tree once (`cd <index_cwd> && xerj autoindex --prefix <prefix> <index_root>`), answers mapping questions from searches before spawning Explore agents
- **Every write to source re-indexes before the step reports success** — `apply-phase` after `execute_tasks`, `debug`'s `fix_and_verify`, and `verify-work`'s `log`; `.paul/`-only writes are exempt
- Codebase research (`/paul:research --codebase`) tries the index before spawning
- `load_context` locates phase files by `xerj search`/`xerj def --prefix <prefix>` instead of reflexively chaining summaries
- Feedback auto-submits via `xerj feedback --submit` — set `XERJ_DISABLE_FEEDBACK=true` to opt out

**Requirements:**
- `xerj` CLI or a running local node (default `http://localhost:9200`)
- `xerj autoindex --prefix <prefix> <index_root>` run once; incremental after
- Every query repeats `--prefix <prefix>`; omitting it searches the shared default `ax` and misses this project

### Future Integrations

Reserved for future use:

```yaml
# linting:
#   enabled: false
#   config_file: .eslintrc

# testing:
#   enabled: false
#   coverage_threshold: 80
```

## Preferences

Optional user preferences for PAUL behavior.

```yaml
preferences:
  auto_commit: false          # Auto-commit after successful tasks
  verbose_output: false       # Show detailed step output
  parallel_agents: false      # Allow parallel agent spawning (advanced)
```

---

*Config created: [timestamp]*
*Edit anytime - changes take effect on next command*
```

---

## Good Example

```markdown
# Project Config

**Project:** expense-tracker
**Created:** 2026-01-28

## Project Settings

```yaml
project:
  name: expense-tracker
  version: 0.2.0
```

## Integrations

### SonarQube

```yaml
sonarqube:
  enabled: true
  project_key: expense-tracker
  server_url: http://localhost:9000
```

### Enterprise Plan Audit

```yaml
enterprise_plan_audit:
  enabled: false
```

### Security Audit

```yaml
security_audit:
  enabled: true
  default_profile: quick
```

### XERJ Discovery & Search

Zero-config code search, definitions, and passage-level citations for planning. The prefix is **asked for at enable time and stored** — it is the only thing that ties searches to this project's index.

```yaml
xerj:
  enabled: false
  index_prefix: [asked-at-enable]  # e.g. akka-pricehub — never defaulted
  index_root: "."                  # folder passed to autoindex (`.` = repo root)
  index_cwd: "[dir autoindex runs from]"  # absolute; makes index_root replayable
  binary_path: ""                  # only needed when `xerj` is not on PATH
```

**When enabled:**
- `/paul:map` indexes the tree once (`cd <index_cwd> && xerj autoindex --prefix <prefix> <index_root>`), answers mapping questions from searches before spawning Explore agents
- **Every write to source re-indexes before the step reports success** — `apply-phase` after `execute_tasks`, `debug`'s `fix_and_verify`, and `verify-work`'s `log`; `.paul/`-only writes are exempt
- Codebase research (`/paul:research --codebase`) tries the index before spawning
- `load_context` locates phase files by `xerj search`/`xerj def --prefix <prefix>` instead of reflexively chaining summaries
- Feedback auto-submits via `xerj feedback --submit` — set `XERJ_DISABLE_FEEDBACK=true` to opt out

**Requirements:**
- `xerj` CLI or a running local node (default `http://localhost:9200`)
- `xerj autoindex --prefix <prefix> <index_root>` run once; incremental after
- Every query repeats `--prefix <prefix>`; omitting it searches the shared default `ax` and misses this project

### Future Integrations

```yaml
# linting:
#   enabled: false
```

## Preferences

```yaml
preferences:
  auto_commit: false
  verbose_output: false
  parallel_agents: false
```

---

*Config created: 2026-01-28*
```

---

## Guidelines

**What belongs in config.md:**
- Project identification (name, version)
- Integration toggles (enabled/disabled flags)
- Integration-specific settings (project keys, URLs)
- User preferences for PAUL behavior

**What does NOT belong here:**
- Sensitive credentials (use environment variables)
- Build configuration (use native config files)
- Project requirements (that's PROJECT.md)
- Roadmap information (that's ROADMAP.md)

**When to create config.md:**
- During `/paul:init` if user enables integrations
- Manually when adding integrations later
- Not required for basic PAUL usage

**Git behavior:**
- Can be committed (no secrets)
- Or gitignored if preferences are personal
- Recommend: commit integration flags, gitignore preferences
