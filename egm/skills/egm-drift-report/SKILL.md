---
name: egm-drift-report
license: Apache-2.0
disable-model-invocation: true
description: >-
  Runs drift detection on all design documents to check for document and
  code consistency. Produces an actionable report with differences. Use when the
  user asks to detect drift or check for consistency across all design documents
  or READMEs in a directory.
---

# Detect Drift In Designs and Code

When running in Codex or ChatGPT Work, first read [Codex integration](../../docs/codex.md).
In Claude Code or Cowork, read `${CLAUDE_PLUGIN_ROOT}/docs/claude.md` first.

When the user asks to detect drift across all designs or a set of READMEs, the
goal is to identify all instances where the codebase has diverged or failed to
implement the specifications described by those designs or READMEs.

1.  **Check Input**: Verify a directory containing design documents or READMEs
    is provided. If not provided, ask the user to specify the target directory.
2.  **List Documents**: List all files in the design directory.
3.  **Analyze**: For EACH design document:

    *   **Contextualize**: Read the design document. Identify the intent,
        proposed changes, and specific filenames/symbols mentioned.
    *   **Locate Source**: Find the corresponding source code files in the
        source tree. If paths aren't explicit, use code search or grep to
        locate the relevant classes, functions, or API endpoints mentioned in
        the doc. Prompt the user to add missing links to the document to make
        future detection cheaper.
    *   **Verify**: Read the current state of those source files.
    *   **Detect Drift**: Compare the design vs. reality. Look specifically for:
        *   Missing Features: Logic described in the doc but absent in the code.
        *   Incomplete Models: Dataclasses/Classes/Structs/Protos missing fields
            specified in the design.
        *   Logic Shortcuts: Hardcoded values where dynamic logic was planned.
        *   Architectural Divergence: Implementation using different
            patterns/libraries than proposed.
        *   Token Drift: when the design names a token file (DTCG
            design-tokens.json) or the project vendors the ux-ui-agent-skills
            kit (`~/.agents/ux-ui-agent-skills/`), run the kit's file-based
            checks on the code the design claims — `python3
            ~/.agents/ux-ui-agent-skills/scripts/lint_hardcodes.py <paths>`
            and `python3 ~/.agents/ux-ui-agent-skills/scripts/validate_tokens.py
            <token file>` — and report each failure as drift. When the project
            has neither, skip silently.
    *   **Filter**: Report ONLY the differences. Do not describe what is working
        or what matches. If the code matches the design perfectly, output "No
        drift detected."

4.  **Report**: Produce a single report listing all discrepancies found.

    *   Write the analysis for each file to `docs/drift/{YYYY-MM-DD}_DRIFT_REPORT.md`
        using your file-writing tool, creating `docs/drift/` if absent. **Never
        write to the repository root** - a bare dated filename lands in whatever
        the working directory happens to be, where nobody looks for it and where
        it is easy to commit by accident. If the project has a different
        convention (a `.paul/` tree, a `reports/` directory), use it and say which
        path you chose in the report's first line.
    *   Strict Format:

        ```markdown
        ## <DESIGN_DOC_NAME>

        <Bulleted list of specific divergences found>
        <Or "No drift detected">
        ```

5.  **Guidance**

    -   Be rigorous. If a design doc mentions a specific object, field or file
        name and the code doesn't have it, that is a reportable drift. Double
        check for coverage.
    -   **Undocumented code is out of scope for this report.** A function the
        design never mentions is not drift; it may be an unplanned addition, a
        utility, or a deliberate extension. Report it only when the design
        *claims* the area - a file, class, or behaviour the document describes -
        and the code inside that claim does something else. Widening the rule to
        "any logic not referenced by a design" makes every partially-documented
        repository a permanent drift case and the report degenerates into a file
        inventory, which is why the scope stops at the design's own claims.
    -   Read files liberally to ensure you are looking at the current state
        of the code, not relying on memory.
    -   Process the files sequentially to ensure the tool output buffer doesn't
        overflow.
