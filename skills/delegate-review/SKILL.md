---
name: delegate-review
description: Review changed code via OCR delegation — OCR selects files and rules, you perform the review. Use for PR or workspace reviews.
---

## Purpose

Run OpenCodeReview (OCR) in delegation mode: OCR handles file selection and review rules while the host agent performs the actual code review with its own capabilities.

Use it when reviewing a PR, commit, range, or workspace diff.

## Input

Optionally bring scope and context:

- **Works best with:** zero input (workspace mode: staged + unstaged + untracked), a commit (`--commit`/`-c`), or a range (`--from`/`--to`), all passed through as-is
- **Also useful:** business context via `--background`/`-b`

If `ocr` is missing, install it first: `npm i -g @alibaba-group/open-code-review`.

Example: `Use delegate-review with --background "checkout flow"`

## Key Concepts

### Mode Resolution

Default is workspace mode. Commit/range flags pass through untouched. Diffs resolve per mode: range via `git diff <merge_base>..<to> -- <path>`, commit via `git show <commit> -- <path>`, workspace via `git diff HEAD -- <path>` (read untracked files directly).

### Review Bar

Comment only on changed (+ lines) code across correctness, security, performance, error handling, concurrency, maintainability.

## Application

1. Preview: run `ocr delegate preview [user-args]` to get mode/ref metadata and the reviewable file list.
2. Rules: run `ocr delegate rule <path1> <path2> ...` for per-file checklists.
3. Diffs + review: per file, fetch the mode-appropriate diff and review against the bar.
4. Report and fix: classify High (bugs, security, data loss — precise fix proposals), Medium (reasonable concerns, perf, manual-work fixes), Low (discard silently). Auto-fix safe, well-defined High/Medium issues.

## Examples

### Example: Workspace Review

Input: none.

Result: workspace files reviewed; High/Medium issues reported and safe ones fixed; Low noise discarded.

## Common Pitfalls

- **Commenting on unchanged lines.** Consequence: noisy, unactionable review. Fix: restrict every comment to + lines.

## References

- `ocr delegate preview`, `ocr delegate rule`
