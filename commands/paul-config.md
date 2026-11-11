<objective>
Manage PAUL project configuration and integrations. Create or update .paul/config.md at any point in the project lifecycle.
</objective>

<when_to_use>
- Enable SonarQube after project init
- Disable an integration
- View current configuration
- Change project settings
</when_to_use>

<process>

**Step 1: Check for existing config**

```bash
ls .paul/config.md 2>/dev/null
```

**If config exists:**
```
Current configuration:

[Display config.md contents]

What would you like to do?
[1] Enable/disable integration
[2] View full config
[3] Reset to defaults
```

**If config doesn't exist:**
```
No configuration found.

Would you like to set up project configuration?
[1] Yes, create config
[2] Cancel
```

**Step 2: Handle user choice**

**For new config or "Enable/disable integration":**

```
Available integrations:

[1] SonarQube - Code quality scanning
    Status: [enabled/disabled/not configured]
[2] Enterprise Plan Audit - Architectural review gate
    Status: [enabled/disabled/not configured]
[3] Security Audit - Vulnerability review, scheduled as debt
    Status: [enabled/disabled/not configured]

[4] Done - save and exit
```

**If user selects SonarQube:**

```
SonarQube integration:

Current: [enabled/disabled/not configured]

[1] Enable
[2] Disable
[3] Back
```

**If enabling:**
- Prompt for project_key (default: directory name)
- Create/update config.md with sonarqube.enabled = true

**If disabling:**
- Update config.md with sonarqube.enabled = false

**If user selects Enterprise Plan Audit:**

```
Enterprise Plan Audit:

Current: [enabled/disabled/not configured]

[1] Enable
[2] Disable
[3] Back
```

**If enabling:**
- Create/update config.md with enterprise_plan_audit.enabled = true
- Inform: "After /paul:plan, you'll be prompted to run /paul:audit before APPLY."

**If disabling:**
- Update config.md with enterprise_plan_audit.enabled = false
- Inform: "Plans will go directly from PLAN to APPLY without audit suggestion."

**If user selects Security Audit:**

```
Security Audit:

Current: [enabled/disabled/not configured]

[1] Enable
[2] Disable
[3] Back
```

**If enabling:**
- Prompt for default_profile (`quick` / `standard` / `deep`; default `quick`)
- Create/update config.md with security_audit.enabled = true and the profile
- Inform: "Trust-surface plans will name a guidance-mode review. `/paul:security` runs the full audit when a phase ships."
- Note: "Validating `findings.json` requires a POSIX host; on Windows a run is marked incomplete and no confirmed rows are written."

**If disabling:**
- Update config.md with security_audit.enabled = false
- Inform: "`/paul:security` will not run unless invoked explicitly."

**If user selects Security Audit:**

```
Security Audit:

Current: [enabled/disabled/not configured]

[1] Enable
[2] Disable
[3] Back
```

**If enabling:**
- Prompt for default_profile (`quick`/`standard`/`deep`; default `standard`)
- Create/update config.md with security_audit.enabled = true
- Inform: "Trust-surface plans will name a guidance-mode review; confirmed
  critical/high findings block the phase exit. Note: validators need POSIX; on
  Windows a full audit is `incomplete` and writes no `confirmed` rows."

**If disabling:**
- Update config.md with security_audit.enabled = false

**If user selects XERJ:**

```
XERJ Discovery & Search:

Current: [enabled/disabled/not configured]

[1] Enable
[2] Disable
[3] Back
```

**If enabling:**
- Probe the binary: `xerj --version`; if not on PATH, prompt for `binary_path`
- **Prompt for `index_prefix` and store it — do not default it.** Suggest
  `<repo-dir>-<project-dir>` (e.g. repo `akka` + project `pricehub` → `akka-pricehub`)
  and show what it means:
  "the prefix ties every later search to this index; omitting it on a query
  searches the shared `ax` and misses this project."
- Prompt for `index_root` (default `.` = repo root; use a path such as `.\pricehub`
  when the indexed folder is a subdirectory of the shell's working directory)
- **Store `index_cwd` (absolute).** It is the directory the autoindex command runs
  *from*, so the pair `index_cwd` + `index_root` replays the exact index command later
  without rediscovering the layout. Default: the directory the user is about to index
  from (their shell cwd).
- Offer to index now: `cd <index_cwd> && xerj autoindex --prefix <index_prefix> <index_root>`
  (run via `binary_path` when set)
- Create/update config.md with xerj.enabled = true
- Inform: "`/paul:map` will answer mapping questions from the index with `path:line` citations before spawning Explore agents; codebase research and `load_context` also consult it first. **Every step that writes source re-indexes before reporting success** (`apply-phase`, `debug`, `verify-work`); `.paul/`-only writes are exempt. Re-running the same autoindex line is incremental."

**If disabling:**
- Update config.md with xerj.enabled = false
- Inform: "Discovery reverts to Glob/Grep and Explore agents; the index stays on disk."

**Step 3: Write config**

Create or update `.paul/config.md`:

```markdown
# Project Config

**Project:** [project_name]
**Updated:** [timestamp]

## Project Settings

```yaml
project:
  name: [project_name]
  version: [version or "0.0.0"]
```

## Integrations

### SonarQube

```yaml
sonarqube:
  enabled: [true/false]
  project_key: [key]
```

### Enterprise Plan Audit

```yaml
enterprise_plan_audit:
  enabled: [true/false]
```

### Security Audit

```yaml
security_audit:
  enabled: [true/false]
  default_profile: [quick/standard/deep]
```

### XERJ

```yaml
xerj:
  enabled: [true/false]
  index_prefix: [prefix]     # asked at enable time; NEVER defaulted
  index_root: [folder]       # "." = repo root, e.g. ".\pricehub"
  index_cwd: [abs dir]       # directory autoindex runs from; makes index_root replayable
  binary_path: ""            # only when xerj not on PATH
```

### Security Audit

```yaml
security_audit:
  enabled: [true/false]
  default_profile: [quick/standard/deep]
```

## Preferences

```yaml
preferences:
  auto_commit: false
  verbose_output: false
```

---
*Config updated: [timestamp]*
```

**Step 4: Confirm**

```
════════════════════════════════════════
CONFIG UPDATED
════════════════════════════════════════

Integrations:
  SonarQube: [enabled/disabled]
  Enterprise Plan Audit: [enabled/disabled]
  Security Audit: [enabled/disabled] (profile: [quick/standard/deep])

Config saved to: .paul/config.md

────────────────────────────────────────
[If SonarQube just enabled:]
▶ NEXT: /paul:quality-gate
  Run your first code quality scan.

[If Enterprise Plan Audit just enabled:]
▶ Enterprise audit will run between PLAN and APPLY.
  After /paul:plan, you'll be prompted to run /paul:audit.

[If Security Audit just enabled:]
▶ Trust-surface plans name a guidance-mode review.
  /paul:security runs the full audit when a phase ships.

[If XERJ just enabled and indexed:]
▶ The index is live. /paul:map and codebase research search before spawning agents.

[If XERJ just enabled and not indexed:]
▶ NEXT: cd <index_cwd> && xerj autoindex --prefix <index_prefix> <index_root>   (binary_path if not on PATH)

[Otherwise:]
Configuration complete.
────────────────────────────────────────
```

</process>

<output>
- `.paul/config.md` created or updated
- Integration status changed as requested
- Clear next steps if applicable
</output>
