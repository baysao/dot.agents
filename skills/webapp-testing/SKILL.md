---
name: webapp-testing
description: Toolkit for interacting with and testing local web applications using Playwright. Use for browser smoke tests, verifying UI changes on localhost, end-to-end UI flows (login, forms, charts), Playwright MCP browser automation, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
license: Complete terms in LICENSE.txt
---

# Web Application Testing

To test local web applications, write native Python Playwright scripts. On Windows, where the only Playwright is a Node package, use the Node route below instead.

**Helper Scripts Available**:
- `scripts/with_server.py` - Manages server lifecycle (supports multiple servers)

**Always run scripts with `--help` first** to see usage. DO NOT read the source until you try running the script first and find that a customized solution is abslutely necessary. These scripts can be very large and thus pollute your context window. They exist to be called directly as black-box scripts rather than ingested into your context window.

## Windows / Node: launching a browser that actually exists

The Python path above assumes a `pip`-installed Playwright with a matching browser. On a machine where the only Playwright is a **Node package** (e.g. a global `@playwright/cli`), the Python route is unavailable and the bundled browser revision usually does not match the local cache — `browserType.launch` dies with *"Executable doesn't exist at …chromium_headless_shell-1247…"*.

Launch the installed browser instead of the bundled one:

```js
// Node, Windows: require the module by absolute path (bare `playwright` may not resolve)
const { chromium } = require('C:/nvm4w/nodejs/node_modules/@playwright/cli/node_modules/playwright');
const browser = await chromium.launch({ headless: true, channel: 'chrome' }); // channel = use installed Chrome
```

`channel: 'chrome'` (or `'msedge'`) skips the bundled revision entirely. Read `browsers.json` next to `playwright-core` to see which revision is pinned versus what `%LOCALAPPDATA%\ms-playwright` holds.

Four API traps that make a correct script look like a product failure:

- `page.on('request', cb)` - `cb` receives the **Request itself**; there is no `r.request()`.
- `page.waitForResponse(predicate, options)` accepts only `{signal, timeout}`. A predicate that matches `PUT /items/*` resolves to the **first** response ever seen (the create, 201) instead of the later edit (200). Count responses yourself (`page.on('response')`) and slice from a recorded index, or arm the promise immediately before the action and match on status.
- Console errors carry the URL in `consoleMessage.location().url`; the message text is only *"Failed to load resource: the server responded with a status of 404"*. Filter favicon noise by URL, never by text.
- `window.confirm` and `window.prompt` are **dismissed** by default, so the action never runs and the script still looks green: an assertion like "no request was sent" passes because nothing happened. Register `page.on('dialog', d => d.accept())` **before** the click that opens the dialog, and assert the effect you caused (the request, the row in the table) rather than the absence of it.

Scope every network assertion to the request you caused (method + path + status + index), so a stale earlier response cannot satisfy a later check.

## Decision Tree: Choosing Your Approach

```
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         ├─ Success → Write Playwright script using selectors
    │         └─ Fails/Incomplete → Treat as dynamic (below)
    │
    └─ No (dynamic webapp) → Is the server already running?
        ├─ No → Run: python scripts/with_server.py --help
        │        Then use the helper + write simplified Playwright script
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

## Example: Using with_server.py

To start a server, run `--help` first, then use the helper:

**Single server:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**Multiple servers (e.g., backend + frontend):**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

To create an automation script, include only Playwright logic (servers are managed automatically):
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # Always launch chromium in headless mode
    page = browser.new_page()
    page.goto('http://localhost:5173') # Server already running and ready
    page.wait_for_load_state('networkidle') # CRITICAL: Wait for JS to execute
    # ... your automation logic
    browser.close()
```

## Verify scripts must be re-runnable

A verification script that creates data and then dies makes the *next* run fail for the wrong reason. Before you trust a failure, check the script's own residue:

- **Clean your fixture at the start, not just at the end.** Delete the row your script creates (use a code that is unmistakably yours), create it, and delete it again on the way out. Otherwise the second run hits a client-side uniqueness guard, sends **zero** requests, and reads like a broken endpoint.
- **Zero requests is an outcome, not an error.** A client that blocks a duplicate before sending is behaving correctly. Say which of the two happened before filing a defect.
- **To exercise a version-guard branch, mutate the version outside the app.** The UI always sends the version it just read, so it can never produce a stale one. From the script, bump the version between the read and the submit (e.g. `UPDATE ... SET version = version + 1`), read credentials from the environment file rather than hardcoding them, and assert on the exact status the API returns for that branch.

## Reconnaissance-Then-Action Pattern

1. **Inspect rendered DOM**:
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **Identify selectors** from inspection results

3. **Execute actions** using discovered selectors

## Bilingual UI: match every locale's label

In a bilingual app (e.g. English + Vietnamese), the rendered label may not be the English one you expect — a toolbar "Indicators" ships as "Chỉ báo kĩ thuật". An English-only `getByRole('button', { name: 'Indicators' })` then fails or, worse, misses silently while you blame the app. On first contact, grep the source for the control to see *all* its label strings, or match locale-neutral hooks (`data-testid`, `name=`, `aria-label`); when text-matching is unavoidable, use a regex covering every locale: `/Indicators|Chỉ báo/i`.

## Playwright MCP snapshots (`.playwright-mcp/`)

When driving a browser through the Playwright MCP server: each `snapshot` call writes a file under `.playwright-mcp/` in the workspace root, and element refs (`target` for click/type) resolve **only against the current snapshot** — any navigation, re-render, or new snapshot invalidates prior refs. Re-snapshot after every navigation before re-finding/acting; a "ref not found" on a previously valid element means staleness, not a broken page.

### Split-port dev servers (Next + Go, `:3080` + `:8080`)

On a proxied dev setup, the frontend page at `:3080` cannot `fetch()` the backend at `:8080` — CORS blocks browser-page JS even though Next proxies `/api/v1/backoffice/*`. Browser verification must drive the UI flow (or use the Next proxy path), never a direct cross-port fetch from `page.evaluate()`. The MCP tools are named `playwright_browser_*` — close the MCP page (`playwright_browser_close` / tabs close) after ad-hoc verification so refs/snapshots do not carry over between runs.

## Common Pitfall

❌ **Don't** inspect the DOM before waiting for `networkidle` on dynamic apps
✅ **Do** wait for `page.wait_for_load_state('networkidle')` before inspection

## Best Practices

- **Use bundled scripts as black boxes** - To accomplish a task, consider whether one of the scripts available in `scripts/` can help. These scripts handle common, complex workflows reliably without cluttering the context window. Use `--help` to see usage, then invoke directly. 
- Use `sync_playwright()` for synchronous scripts
- Always close the browser when done
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
- Add appropriate waits: `page.wait_for_selector()` or `page.wait_for_timeout()`

## Reference Files

- **examples/** - Examples showing common patterns:
  - `element_discovery.py` - Discovering buttons, links, and inputs on a page
  - `static_html_automation.py` - Using file:// URLs for local HTML
  - `console_logging.py` - Capturing console logs during automation