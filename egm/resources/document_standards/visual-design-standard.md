# Visual Design Standard

This standard defines the quality bar for a design document that specifies a
rendered surface: a landing page, marketing site, portfolio, product page,
one-pager, or an app screen (dashboard, admin, settings, inbox, editor).

It does not score pixels. A reviewer with a fresh context sees a document, so
this standard asks only what a document can answer. The rendered page is
measured later, by `design-taste-frontend`'s `scripts/inspect.mjs`, and that is
the gate a build must pass. This document decides whether the build is worth
gating.

## Core Principle

A visual specification passes if a competent implementer who has never spoken to
the author can build the page without inventing the idea, the content, the
assets, or the layout, and can tell from the document alone whether the result
is correct.

The failure this standard exists to catch is not an ugly design. It is the
**unspecified** one: a document that names a hero, three feature cards, a
testimonial and a footer, and leaves every decision that actually determines the
page — what this subject is, what it says, what pictures exist, why the sections
are in that order — to be re-improvised by whoever implements it. That document
reviewed clean in five fresh contexts and still produced a page indistinguishable
from every other page.

## The Idea Rule

The specification must state, in one sentence:

> On this page, **[something that belongs to this subject]** becomes **[the
> device the composition calls for]**.

And it must survive the **competitor test**: put the nearest real alternative in
the first blank — the other agency, the other bakery, the other console in the
same market. If the sentence still reads true, the idea belongs to the category
and the specification fails this standard.

"Clean, modern, and trustworthy" is not an idea. "A verification surface where
every number carries its own staleness" is one, because a competitor's console
does not.

The document must also name the **one live thing** the visitor can do, or that
differs per visit, made from that idea — what it does, what real content it uses,
and what the plain no-script fallback is. A page with no live thing has no proof
of its claim; a page with three is a playground.

## The Alternatives Rule

The composition must be chosen, not defaulted. The specification must record:

*   the direction taken, named, and **why this one carries the subject** — not
    why it is attractive;
*   at least one direction considered and rejected, with the reason;
*   every deviation from the chosen direction, and what forced it (a brand
    constraint, an asset that does not exist, a section that cannot hold the
    real content).

A specification that proposes one layout without showing it beat another fails
this standard, for the same reason `feature-spec-standard.md` rejects a single
unchallenged architecture.

## The Argument Rule

Sections exist to carry claims. The specification must list the page as
**claims with their proof**, one line per section, and must delete any section
that carries no claim. The stock sequence — hero, logos, three features,
testimonial, pricing, call to action — is a defect when the document cannot say
what each of those sections proves.

## The Content Rule

Where the brief leaves gaps, the specification supplies sample detail so the
design can be judged at full density, and **lists those samples as samples** for
the owner to confirm. Dish names, room rates, project titles and empty-state
copy belong here.

The line is between sample detail, which is expected, and **proof**, which is
never invented. No customers, quotations, reviews, press mentions, customer
logos, or business statistics may appear in a specification unless the owner
supplied them. An invented testimonial is a factual misrepresentation that ships
to production whenever the page is built from this document.

## The Imagery Rule

The specification must state, for each section that shows a picture, **which of
these it is**:

1. the project's own photograph, screenshot, or product shot;
2. an image the team will generate;
3. a real picture of the subject's world from an open collection, with its
    licence and credit line — never presented as the subject's own;
4. a drawing made in code from the subject, for what no honest picture exists of;
5. type and colour alone.

It must count the **real pictures** (photographs, screenshots, maps, engravings,
footage, raster artwork) and show at least four. SVG drawings do not count toward
that floor.

It must not plan around images that do not exist. "A full-bleed photo of the
factory floor" is not a plan when nobody has photographed the floor.

## The States Rule

Every control and every data-bearing region must have its states specified:

*   **Interactive**: default, hover, focus, pressed, disabled, and the
    accessible name a screen reader announces — including icon-only controls.
*   **Data**: loading, empty, partial, stale, and error. For a console or
    dashboard this is the whole product, not an edge case: a screen that only
    specifies the happy path has specified the screenshot, not the surface.
*   **Responsive**: a phone composition that is its own layout, not the desktop
    one squeezed.

Where the surface carries numbers, the document must specify how they align and
format — tabular figures, unit, precision, and the source or timestamp that makes
them verifiable.

## The Gate Rule

The specification must name the check that will decide whether the built page is
finished, and it must be a check with an exit code:

```bash
node <design-taste-frontend>/scripts/lint.mjs <source files>
node <design-taste-frontend>/scripts/inspect.mjs <url | built index.html>
node <design-taste-frontend>/scripts/scenes.mjs <url | built index.html>   # if the page has scroll scenes
```

The document must state the widths, that the gate runs on the **production
build** rather than the dev server, and that every FAIL is fixed while every WARN
is either fixed or defended in one sentence.

"UI matches the mockup" is not a gate. It is true of every rendering and false of
none, so it can never fail — and a check that cannot fail reports unfinished work
as done.

When the environment has no Node 22 or no Chrome, the specification must say so
and name which check will not run. It must not substitute a weaker check and
present it as the gate.

## The Token and Accessibility Gate

When the project carries a token system — a DTCG `design-tokens.json`, or the
ux-ui-agent-skills kit vendored at `~/.agents/ux-ui-agent-skills/` — the
specification must also name the objective gate for that layer. It is a
different layer from taste: these checks judge the source of truth the page is
built from, while `lint.mjs`/`inspect.mjs` judge the rendered page. A document
that specifies tokens names both gates and says which one owns which claim.

```bash
python3 <ux-ui-agent-skills>/scripts/validate_tokens.py <tokens>   # token JSON + alias resolution
python3 <ux-ui-agent-skills>/scripts/validate_contrast.py          # WCAG pairs, light + dark
python3 <ux-ui-agent-skills>/scripts/lint_hardcodes.py <paths>     # no off-theme hex/px/timing
node <ux-ui-agent-skills>/scripts/gate.mjs verify_states.mjs <file> [--dark]   # default/hover/focus contrast
node <ux-ui-agent-skills>/scripts/gate.mjs verify_responsive.mjs <file|dir>    # no overflow 280-951px
```

The kit's own `accuracy_report.mjs` is the kit's self-test, not a project gate;
a document must not cite it as evidence about the project's page.

## Requirements (Non-Exhaustive Examples)

The specification must detail these areas when the surface is in scope:

*   **The subject inventory**: eight to twelve things that belong to this client
    and no competitor, which the idea and the picture search both draw from.
*   **The idea sentence and its competitor test.**
*   **The claims and their proof**, per section, in order.
*   **The copy deck**: every headline with its line count at each width, and the
    one supporting sentence that sits under it.
*   **Type and colour roles**: which faces, which sizes, which ground, ink and
    accent, and where the accent is allowed to appear.
*   **The imagery plan**, per the Imagery Rule, with the picture count.
*   **The live thing** and its fallback.
*   **States**, per the States Rule.
*   **The gate**, per the Gate Rule, and its known gaps.
*   **What must survive**: existing routes, forms, data, brand assets and
    behaviour, when the work is a restyle or redesign rather than a new page.

## Reviewing Against This Standard

A reviewer applies the standard to the document and reports findings as
`Blocker`, `Major`, or `Nit`, citing the section. A finding is a gap the
implementer would have to invent an answer to — not a matter of taste. Where the
document makes a defensible choice the reviewer would have made differently, the
finding is a `Nit` at most, and the reviewer says which rule it does and does not
violate.

The rendered judgement belongs to `design-taste-frontend`'s
`references/critique.md`, which scores a screenshot. Do not restate its rubric
here and do not apply it to prose.
