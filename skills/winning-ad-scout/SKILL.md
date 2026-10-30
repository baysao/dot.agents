---
name: winning-ad-scout
description: "Find profitable physical products in a niche by scraping the public Meta Ad Library with a self-contained Playwright scraper (no AI API, no keys) and analyzing the results. Use when someone wants product research for a Shopify/dropshipping store, asks 'what should I sell in X niche', 'find winning products', 'scout Meta/Facebook ads for a niche', or wants a product idea validated against real active ads."
---

# Winning Ad Scout

## Purpose

Research a niche against the public Meta Ad Library: scrape active ads for product-level
keywords, group them by underlying product, and produce a ranked shortlist of products most
likely to be profitable for a small Shopify brand — every pick backed by specific ads.

Everything needed lives in this skill folder. There is **no Claude/Anthropic API and no agent
SDK**: the scripts only scrape. The agent session reading this file plays the researcher —
planning keywords, reading scrape results, weighing evidence, and writing the report.

## Layout

```
<skill_dir>/
  SKILL.md            this file
  scripts/
    ad_library.py     scraper core; parses rendered text around "Library ID:" labels
                      (stable across Meta's obfuscated, frequently-changing CSS)
    scout.py          batch CLI: 1+ keywords -> raw_ads.json + compact JSON on stdout
    requirements.txt  playwright only
```

`<skill_dir>` is `~/.agents/skills/winning-ad-scout`
(`C:\Users\Dell\.agents\skills\winning-ad-scout` on this machine).

## Setup (once)

```
cd C:\Users\Dell\.agents\skills\winning-ad-scout\scripts
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m playwright install chromium
```

Run everything through the venv python (no activation needed):
`C:\Users\Dell\.agents\skills\winning-ad-scout\scripts\.venv\Scripts\python.exe`

No API keys, no `.env`. Set `HEADLESS=1` to hide the browser window (default shows it).

## Inputs

- **Required:** a niche phrase, e.g. `"home fitness"`, `"pet grooming"`.
- **Optional:** country code (default `US`, two letters), ads per keyword (default 30),
  output directory.

Inline arguments to the skill count as answers. If no niche is given, ask one question and
proceed on a stated assumption if it goes unanswered.

## Workflow

1. **Plan keywords.** Turn the niche into 2-4 specific product-level phrases — never the bare
   niche word. E.g. "home fitness" → "adjustable dumbbells", "walking pad", "resistance bands".
   Choose phrasings a shopper or advertiser would use.
2. **Scrape.** One batch call:
   ```
   <venv-python> C:\Users\Dell\.agents\skills\winning-ad-scout\scripts\scout.py "adjustable dumbbells" "walking pad" --country US --max 30
   ```
   Writes `outputs/<timestamp>_<slug>/raw_ads.json` under the current working directory (or
   `--out DIR`) and prints compact JSON: per-ad `id`, `advertiser`, `days_running`, `started`,
   `variants`, `copy` snippet, `url`, plus `errors` per failed keyword. If a phrase returns
   nothing, re-plan and scrape a different phrasing before concluding.
3. **Analyze.** Group ads by the underlying product (same item, different advertisers/stores).
   Read full ad copy from `raw_ads.json` when the snippet isn't enough.
4. **Rank.** 3-7 picks, scored 1-10 on the signals below. Be honest when evidence is thin.
5. **Write the report.** `report.md` and `shortlist.csv` next to `raw_ads.json` (formats below).
6. **Evidence guardrail.** Cite only Library IDs that appear in `raw_ads.json`. Never invent one.
   An ad's URL is `https://www.facebook.com/ads/library/?id=<library_id>`.
7. **Summarize** the top picks to the user with evidence (advertiser, days running, variants).

### Signals

| Signal | Meaning |
|---|---|
| Days running | Strongest signal. 30+ days ≈ probably profitable (losing ads get killed fast); 90+ is a strong winner. |
| Creative variants | Many copies of one creative = advertiser is scaling it. |
| Advertiser count | Several small advertisers selling the same product = proven demand. |

Ignore household brands, marketplaces, apps, services, courses, and non-physical offers —
the target is products a small Shopify brand could source and sell. Days running and variants
are proxies, not proof: the Ad Library hides spend and engagement.

### report.md format

```markdown
# Product shortlist: <niche>
_Meta Ad Library, country <CC>, generated <YYYY-MM-DD HH:MM>_

<2-6 line market summary: how crowded, what's working, overall read>

## Ranked picks

### 1. <product> (score <n>/10)
**Why:** <1-3 sentences grounded in the ad data>
**Angle competitors use:** <the marketing hook>
**Risks:** <saturation, seasonality, compliance, shipping>
**Evidence:**
- [<Advertiser>](<ad url>) — 45 days running, 3 variant(s)
```

### shortlist.csv format

Columns: `rank, product, score, why, angle, risks, longest_running_days, evidence_urls`
(evidence_urls pipe-joined).

## Troubleshooting

- **0 ads parsed:** scrape one keyword with `HEADLESS=1` and watch the browser — Meta changed
  the layout or blocked the visit. Also try a different phrasing or country. The parser reads
  rendered text around `Library ID:` labels, not CSS classes, so it usually survives layout churn.
- **Browser error:** chromium may be missing — rerun
  `.venv\Scripts\python -m playwright install chromium`.
- **Thin results:** rerun with more/fewer `--max`, a different country, or narrower phrases
  (brand-agnostic product words beat niche labels).
- **Windows console:** scripts already reconfigure stdout to UTF-8; emoji in ad copy won't crash.

## Extending

New sources (TikTok Creative Center, Minea, PiPiADS) fit as sibling modules next to
`ad_library.py` with a flag in `scout.py`; supplier pricing (AliExpress/CJ) and pushing picks
to Google Sheets or Slack are natural follow-ups. Keep the pattern: scripts scrape and dump
structured data; the agent session does the judgment.
