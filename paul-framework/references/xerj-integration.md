# XERJ Integration

Reference for using XERJ (and its Corpus Hub) as PAUL's discovery and search layer for
text and code, toggled per project in `.paul/config.md`.

---

## What XERJ Provides

XERJ is an Elasticsearch-wire-compatible search node plus a CLI. On top of one index it
gives PAUL four different retrievals, each suited to a different question:

| Tool | Question it answers | Citation discipline |
|------|--------------------|--------------------|
| `xerj search "<plain words>"` | Where does the code/docs talk about X? (definition-first: the defining file outranks mere callers) | `path:line` from the printed passage — never the whole file |
| `xerj def "<symbol>"` | Where is this symbol defined, and with what signature? | `file:line` + signature |
| `xerj ask "<question>"` (hub) | What does the upstream source, standard, or regulation actually say? | corpus, pin date + age, licence, `file:line` — state all four |
| `xerj code <corpus> "<q>"` / `xerj_code_search` (MCP) | How did a peer project solve X? | Same citation discipline; watch the licence banner |

Passages beat raw results: a plain `_search` returns whole files. The CLI and
`xerj_search` already return the enclosing block; when composing a raw DSL query, ask
for `fields: ["_passage"]` or you get files, not evidence.

## The Toggle

```yaml
xerj:
  enabled: true                 # master switch for all four retrievals
  index_prefix: akka-pricehub   # ASKED FOR at enable time — never defaulted
  index_root: .\pricehub        # folder passed to autoindex
  index_cwd: C:\dev\apps        # directory autoindex is run FROM (makes index_root replayable)
  binary_path: ""               # full path, only needed when `xerj` is not on PATH
  hub:
    hosted: false               # true allows the hosted hub outside a git repo
```

### Prefix discipline

`paul-config` **prompts for the prefix and stores it**; there is no silent
directory-name default. The prefix is the only thing that ties a later search to this
project's index — get it wrong and the search either finds nothing or, worse, returns
another project's passages from the shared default `ax`.

Index and query with the same prefix, always spelled out:

```bash
xerj autoindex --prefix akka-pricehub .\pricehub     # first run, or incremental
xerj search "margin basket"  --prefix akka-pricehub -k 5
xerj def    "MarginEngine"   --prefix akka-pricehub
```

Omitting `--prefix` on a query searches `ax` and will miss this project entirely.
`index_root` is the positional folder for autoindex; `index_cwd` is the directory it is
run from, so the pair replays the exact command without rediscovering the layout:

```bash
cd <index_cwd> && xerj autoindex --prefix <index_prefix> <index_root>
```

## Refresh After Any Source Write

**A workflow step that creates, edits, deletes, renames, or generates a source file
must re-run autoindex before it reports success.** Reading a stale index after a write
is how a later search cites a line that no longer exists, or misses the file the write
just added — and the failure is silent, because a stale hit looks exactly like a fresh
one.

The rule applies to four points in the loop, all PAUL-owned:

| Where it fires | Workflow step |
|---|---|
| Tasks executed, source written | `apply-phase` → `refresh_index` (after `execute_tasks`, before `finalize`) |
| Minimal fix applied in a debug session | `debug` → `fix_and_verify` |
| UAT issues fixed during verification | `verify-work` → `log` |
| Codebase map regenerated after code changes | `map-codebase` → `index_project` |

The command, always the replay pair:

```bash
cd <index_cwd> && xerj autoindex --prefix <index_prefix> <index_root>
```

Autoindex is incremental, so a no-op write costs a scan, not a rebuild. Two limits:

- **Skip it when the step wrote only `.paul/` files.** Plans, summaries, debt rows, and
  STATE are not indexed source; refreshing after them is pure waste.
- **A failed refresh is a reported gap, not a silent pass.** If the node is down, say
  so and name which searches are now untrustworthy. Do not claim the index is current.

**`enabled: false` or a missing block means: no behavior change.** PAUL uses its
default discovery (Glob/Grep/Explore agents) exactly as before. There is no graceful
middle state — if the toggle is on and the node is down, fail over explicitly, do not
silently degrade.

Five things are wired to the toggle, nothing else:

1. **`map-codebase`** — an `index_project` step runs `xerj autoindex` once per project,
   then answers mapping questions from searches before any Explore agent spawns.
2. **Codebase research (`paul-research`)** — try the index *before* spawning Explore;
   spawn only what the index cannot answer.
3. **Plan-phase context loading (load_context)** — locate files for the phase's work by
   search, then read only those files instead of reflexively chaining summaries.
4. **Apply-phase write refresh** — `apply-phase` re-indexes after `execute_tasks` when
   the tasks wrote source, so UNIFY and later phases search current code.
5. **Debug and verify-write refresh** — `debug`'s `fix_and_verify` and `verify-work`'s
   `log` re-index after they change source, for the same reason.

## Index Lifecycle

Autoindex is incremental. Three rules:

1. **A stale hint is authoritative.** When a search prints the freshness hint (indexed
   files newer than the last run, some removed), it *also* prints the reindex command
   verbatim — run that exact line before trusting the passages. The MCP hits carry the
   same signal as `_xerj.hints: ["index_stale"]`.
2. **Refresh after writes, not before.** Points 4 and 5 above fire on the write, which
   is the only moment the rule can be enforced mechanically. A search is read-only and
   never refreshes on its own.
3. **`.paul/` writes are exempt.** Plans, summaries, debt rows, and STATE are not
   indexed source; a refresh after them costs a scan and changes nothing.

Budget honesty: `xerj_index_budget` (MCP) or `xerj autoindex map` estimates before
hashing. If it answers `decision_required`, show the plan to the user and rerun
autoindex with `--plan <name>` or `--yes`. Never start a run that does not fit the disk.

## Hub: Public Material Only --- and Its Three Exits

`xerj ask` (CLI) or the `xerj_hub_ask/def/find` MCP tools answer from **pre-indexed
public corpora**: library source at a pinned commit, a standard, a regulation, an
advisory feed. This project's own files are never a hub question — the project is a
local autoindex question.

Before answering, check the pin: a question about *the current version* of a dependency
needs a pin date that is not months stale. Always disclose the four-part citation.

When it cannot answer, there are exactly three exits, each with its own action:

| Exit | Meaning | Action |
|------|---------|--------|
| `4` | More than one corpus fits | Candidates print; rerun with `--corpus <slug>` |
| `1` `no hub corpus matches` / `no hub corpus covers this topic` | The hub does not hold it | Say so. Do not answer from memory. A local-index question routes to autoindex |
| `run: xerj hub pull <slug> (<N> MB)` | Pack is above the auto-download limit | Run that line in a shell, then ask again |

`3` = pack failed checksum, discarded, do not use, tell the user. `5` = no hub public
key; a retry will not help. Two MCP-side geometry notes: hub tools answer only from
packs already on this machine, and they never fetch a catalogue — run `xerj hub sync`
in a shell first, then call again. A shell `xerj ask` can pull its own pack, so CLI
first, MCP second, is the robust order.

## Code Search (Peer Corpora)

`xerj code <corpus> "<query>"` (CLI) / `xerj_code_search` (MCP) retrieves how real
codebases solved a problem. Licence posture comes with the answer: AGPL, SSPL,
Elastic, BUSL, GPL, LGPL, MPL hits are **approach-only** — read the technique, do not
copy the code. Indices older than 30 days are refused unless you pass `stale_ok`.
An empty result is a successful "no reference solved it this way", not an error.

## Egress: One Feature Sends Text Off-Node

Local search, semantic, hybrid, `def`, memory, and second-brain operations stay on the
local loopback node (bind default `127.0.0.1`). Exactly three things cross the network:

1. **`rerank`** — an external provider re-judges top hits, sending document text off
   the node. Without an operator key it 503s (`rerank_exception`). *Never use rerank on
   project code or private data unless the user explicitly agreed, and never claim
   "nothing leaves the machine" afterwards.*
2. **`judge`** — zero-token and local, but with no local model armed it is a
   deterministic lexical scorer with no semantic signal; `judged.scorer` tells which
   one ran. Do not overstate it.
3. **Hub/code corpora** — the packs are public material; inside a git repository `xerj`
   answers locally by default. Outside one it may go to the hosted hub; `xerj hub
   config hosted off` forbids that.

Node shutdown honesty: stop only a node you started (`xerj hub stop` for its own; kill
the recorded PID otherwise). Never `pkill xerj` — other nodes may be live.

## What Belongs in Memory vs. the Brain vs. DEBT.toml

XERJ carries two persistence surfaces and it is easy to confuse all three stores:

| Store | What lives there | PAUL analog |
|-------|-----------------|-------------|
| `xerj_memory_store/recall` | Durable agent-only facts, namespaced, dedup'd, semantically recallable | Notes, not project state |
| Second brain (`xerj brain <folder>`) | Browsable link-graph over a folder; links carry evidence quotes | Observation layer, not directional decisions |
| `.paul/DEBT.toml` |**What is owed**, with a runnable check | The only store PAUL gates progress on |

XERJ memory and the brain are PAUL-**external** by design: they hold pointers to
evidence, not scheduling. A plan that defers work still needs a `[[debt]]` row, even
though the context is also stored in `xerj_memory_store` — the row's check discharges
by running, not by recalling.

## Anti-Patterns

1. **Citation by file.** Contract is `path:line` (or `path#locator` for data rows).
   A whole-file hit is a starting point, not evidence.
2. **Treating freshness as a suggestion.** The stale hint names the exact reindex
   command; running a different command, or none, is how stale passages end up cited
   as current.
3. **Hub for own code.** Own files = local autoindex. Hub = what you cannot quote
   from memory.
4. **Fire-and-forget autoindex on unknown size.** Budget, plan, and disk-fit first;
   `decision_required` means the user sees the plan, not the omission.
5. **Approach-only reuse.** GPL-family / BUSL / Elastic hit + copy-paste is the exact
   licence failure XERJ's own warning exists to prevent.
6. **rerank to "improve quality" on private data.** Egress without a stakeholder's
   informed yes is a policy violation dressed as a tuning flag.
7. **Memory as scheduling.** `xerj_memory_store` never replaces `.paul/DEBT.toml`; it
   recalls context, it cannot gate a transition.

---

*Framework: `~/.agents/paul-framework/` — toggled in `.paul/config.md`, wired into
`map-codebase.md` and `plan-phase.md` load_context; hub and node behavior follow the
`xerj` + `xerj-hub` skills.*
