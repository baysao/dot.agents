---
name: design-gate
description: Run the one-command quality gate (ux-ui-agent-skills) and report the real N/N result. Use before claiming any build/review is done.
disable-model-invocation: true
---

# ux-ui-agent-skills wrapper

Kit root: `C:/Users/Dell/.agents/ux-ui-agent-skills` (vendored clone of plugin87/ux-ui-agent-skills).

Read and follow `C:/Users/Dell/.agents/ux-ui-agent-skills/.claude/skills/gate/SKILL.md` now. Inside kit files, resolve every `${CLAUDE_SKILL_DIR}/../../../` as the kit root above. Report the gate's real output — never a remembered or reasoned number.

Note: render checks report `SKIPPED` (exit 0) with no browser installed; prefix with `DS_REQUIRE_BROWSER=1` when reading exit codes, or install Chrome via `npx playwright install chrome`.
