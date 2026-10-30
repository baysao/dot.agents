<!-- karpathy-guidelines:begin -->
---
name: karpathy-guidelines
description: Reduce LLM coding errors. Use writing/reviewing/refactoring code → avoid overcomplication, surgical changes, surface assumptions, define success criteria.
license: MIT
---

# Karpathy Guidelines

Reduce LLM coding errors.

**Tradeoff:** Caution over speed. Trivial tasks → use judgment.

## 1. Think Before Coding

**No assumptions. No hidden confusion. Surface tradeoffs.**

Before coding:
- State assumptions explicitly. Uncertain → ask.
- Multiple options → present all (no silent decisions).
- Simpler way exists → suggest. Push back if needed.
- Unclear → stop, identify confusion, ask.

## 2. Simplicity First

**Minimum code solves problem. No speculative code.**

- No unasked features.
- No abstractions for single-use code.
- No requested flexibility/configurability → don't add.
- No error handling for impossible scenarios.
- 200 lines vs 50 lines → rewrite to 50 lines.

Ask: "Overcomplicated?" → yes → simplify.

## 3. Surgical Changes

**Touch only what is needed. Clean own mess.**

Editing code:
- No adjacent cleanup, comments, or formatting changes.
- No refactoring working code.
- Match existing style.
- Unrelated dead code → mention, don't delete.

Orphaned code:
- Your changes make code unused → remove imports/vars/fns.
- Pre-existing dead code → don't remove unless asked.

Test: Every changed line traces to user request.

## 4. Goal-Driven Execution

**Define success criteria. Loop & verify.**

Convert tasks to verifiable goals:
- "Add validation" → "Write invalid input tests → make pass"
- "Fix bug" → "Write reproduction test → make pass"
- "Refactor X" → "Tests pass before & after"

Plan structure:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Clear success criteria → autonomous loop. Weak criteria ("make work") → clarification needed.
<!-- karpathy-guidelines:end -->
