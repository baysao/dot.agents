"""
scout.py — batch scraper for the public Meta Ad Library. No AI, no API keys.

Scrapes one or more keywords, dedupes by Library ID, and dumps every ad seen
to raw_ads.json plus a compact JSON summary on stdout. The research agent that
invoked it does the planning, grouping, ranking, and report writing.

Usage:
    python scout.py "posture corrector" --max 20
    python scout.py "adjustable dumbbells" "walking pad" --country US --max 30 --out ./outputs
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from ad_library import search_ads

AD_URL = "https://www.facebook.com/ads/library/?id={library_id}"


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40] or "niche"


async def _gather(keywords: list[str], country: str, max_ads: int) -> tuple[list[dict], list[str]]:
    seen: dict[str, dict] = {}
    errors: list[str] = []
    for kw in keywords:
        try:
            ads = await search_ads(kw, country=country.upper(), max_ads=max_ads)
        except Exception as exc:
            errors.append(f"{kw}: browser error: {exc}")
            continue
        if not ads:
            errors.append(f"{kw}: no ads parsed (no results, or the page changed/blocked us)")
            continue
        for ad in ads:
            seen.setdefault(ad.library_id, asdict(ad))
        print(f"[scout] {kw}: {len(ads)} ads ({len(seen)} unique so far)", file=sys.stderr)
    merged = sorted(seen.values(), key=lambda a: a["days_running"] or 0, reverse=True)
    return merged, errors


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows console safety

    ap = argparse.ArgumentParser(description="Scrape the Meta Ad Library for keywords (no AI, no cost).")
    ap.add_argument("keywords", nargs="+", help="product-level search phrases, e.g. 'posture corrector'")
    ap.add_argument("--country", default="US", help="two-letter Ad Library country code")
    ap.add_argument("--max", type=int, default=30, help="max ads per keyword, 10-40 sensible")
    ap.add_argument("--out", default=None, help="output dir (default ./outputs/<ts>_<slug>)")
    args = ap.parse_args()

    max_ads = max(5, min(args.max, 40))
    merged, errors = asyncio.run(_gather(args.keywords, args.country, max_ads))

    if args.out:
        out_dir = Path(args.out)
    else:
        slug = _slug(" ".join(args.keywords))
        out_dir = Path.cwd() / "outputs" / f"{datetime.now():%Y%m%d-%H%M}_{slug}"
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / "raw_ads.json"
    raw_path.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")

    # Compact summary for the calling agent; full data is in raw_ads.json.
    compact = [
        {
            "id": a["library_id"],
            "advertiser": a["advertiser"],
            "days_running": a["days_running"],
            "started": a["started"],
            "variants": a["variant_count"],
            "copy": a["ad_text"][:160],
            "url": AD_URL.format(library_id=a["library_id"]),
        }
        for a in merged
    ]
    print(json.dumps({
        "keywords": args.keywords,
        "country": args.country.upper(),
        "ads_found": len(merged),
        "saved_to": str(raw_path),
        "errors": errors,
        "ads": compact,
    }, ensure_ascii=False))

    for err in errors:
        print(f"[scout] {err}", file=sys.stderr)
    if not merged:
        sys.exit(1)


if __name__ == "__main__":
    main()
