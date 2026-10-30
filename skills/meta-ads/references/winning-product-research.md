# winning-product-research

> Pre-flight gate for eCommerce / dropshipping: validate a product idea against a
> 6-criterion scorecard before committing ad budget. Runs *before* Flight Plan
> stage 0. Complements the `winning-ad-scout` skill, which supplies the Meta Ad
> Library scrape this module scores.

## The 6-criterion scorecard (1-5 each, total /30)

| # | Criterion | What to check | Pass (4-5) | Fail (1-2) |
|---|---|---|---|---|
| 1 | **Pain point** | Is the problem specific, frequent, emotional? Mine review/Ad-Library copy for how shoppers phrase it. | Sharp, recurring, painful enough to pay now ("my dog chews every bed in 2 days") | Vague nice-to-have, novelty/gadget, "cool but not urgent" |
| 2 | **Demoability** | Can the value be proven visually in the first 3-5s of a vertical video? | Instant visual transformation / satisfying action / visible problem-solved | Needs verbal explanation, abstract benefit, slow payoff |
| 3 | **Margin** | Landed cost (product + shipping + duties) vs realistic sell price after ads. | ≥3× markup; sell price ≥ $25-30; leaves room for ≥$10 contribution after ~$12-18 CAC | Commodity with race-to-bottom pricing; sell < $15 |
| 4 | **Shipping risk** | Size, weight, fragility, batteries/liquids, return cost. | Small, light, durable, no battery/liquid; low breakage and return rate | Bulky, fragile, lithium battery, liquid, high restocking cost |
| 5 | **Policy risk** | Sensitivity under Meta ad policy (see list below). | Neutral product; no restricted claims needed to sell it | Requires health/weight/medical claims, before-after imagery, or sits in a restricted category |
| 6 | **Competitor saturation** | How many advertisers, how long, how identical the creatives are (Ad Library + TikTok). | Early-mid: several advertisers prove demand, but angles/creatives still vary | Saturated: same UGC everywhere, identical hooks, pure price war |

**Gates:** any score ≤2 on shipping or policy = hard reject (don't test). Total
≥20/30 = test with a small budget; 16-19 = only with a clear differentiation
angle; <16 = drop.

## Research sources

| Source | How to use | Signals to extract |
|---|---|---|
| **Meta Ad Library** | Use the `winning-ad-scout` skill (`scout.py`) — 2-4 product-level keywords, country code of target market, ~30 ads/keyword. | `days_running` (30+ ≈ probably profitable, 90+ = strong winner), creative variant count (scaling), advertiser count (proven demand), hook angles from ad copy |
| **TikTok Creative Center** (ads.tiktok.com/business/creativecenter) | Top Ads board + keyword search for the product; also check trending hashtags. Manual browse — no scraper needed for a first pass. | Recency + engagement of top ads, whether the format is still rising or fading, spark-ad patterns competitors reuse |
| **Customer reviews** | Amazon top/2-3★ reviews, Reddit (r/<niche>), TikTok comment sections on competing ads. Read 20-30 reviews. | Pain phrases (copy into hooks), objections ("does it work for X?"), failure modes (product improvement + risk flag), desired features |
| **Search keywords** | Google Trends (12-month view, rising not decaying; check seasonality), Amazon search autocomplete for the product phrase. | Demand trend (rising/stable), seasonality spikes (Christmas-only = risky), regional interest |

## Workflow

1. **Shortlist** 3-5 product candidates in the niche (brand-agnostic product
   words, not niche labels).
2. **Scrape Meta** via `winning-ad-scout`:
   ```
   <venv-python> C:\Users\Dell\.agents\skills\winning-ad-scout\scripts\scout.py "product phrase" --country US --max 30
   ```
   Ignore household brands, marketplaces, services, courses — physical products only.
3. **Cross-check TikTok** Creative Center for the same phrases.
4. **Mine reviews/comments** — extract 3-5 pain phrases and top 3 objections per product.
5. **Check search demand** — Google Trends + Amazon autocomplete (rising, non-seasonal).
6. **Score** on the 6-criterion table; apply hard gates; rank survivors.
7. **Hand off** winners to the Flight Plan: pain phrases → stage 6 hooks/copy;
   objections → stage 2 offer + FAQ; UPSYD default start = Solution Aware.

## Meta policy-sensitive categories (policy-risk screen)

Reject or heavily discount products that need any of these to sell:
personal-health-attribute implications (acne, weight, hair loss, ED), weight-loss
or body-transformation claims, before/after imagery, medical devices/cures,
tobacco/vapes, weapons, adult products, financial "get rich" claims. Even
compliant products in adjacent spaces (e.g. posture, sleep) need claim-free
angles — factor that into the demoability score.

## Output template

```markdown
# Winning-product shortlist: <niche>
_Sources: Meta Ad Library (<CC>) + TikTok Creative Center + reviews + search, <date>_

| Rank | Product | Score | Pain | Demo | Margin | Ship | Policy | Saturation | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 1 | <product> | 24/30 | 5 | 5 | 4 | 4 | 3 | 3 | TEST |

### 1. <product> (24/30)
**Pain phrase (verbatim from reviews/ads):** "..."
**Angle competitors use:** ...
**Objections to handle in offer/copy:** ...
**Evidence:** <advertiser — days running — variants> | TikTok: <format/engagement read> | Trends: <rising/flat/seasonal>
**Risks:** ...
```

Cite only Library IDs found in `scout.py` output — never invent evidence.
