---
name: verify-and-stop
description: Prove existing work meets acceptance conditions without expanding scope. Use for validation-only tasks, completion checks, focused gate runs, last-mile proof, and when citing a guard/style/lint test as evidence that work passes.
---

# Verify and stop

Translate acceptance conditions into smallest sufficient proof set.

- Reuse still-current results with matching repository state.
- Run focused checks before wider gates.
- Distinguish pass, fail, unavailable, and blocked exactly.
- A guard you have never seen fail proves nothing: inject one violation, confirm the check fails at the right location, restore, then trust the pass.
- Do not edit product code unless verification request includes fixes.
- Do not add polish, cleanup, or unrelated tests after criteria pass.

Stop immediately when acceptance proof is complete. Report commands, results, and unresolved risk only.
