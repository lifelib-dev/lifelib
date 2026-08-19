```{module} uklib
```

# The **uklib** Library

```{warning}
{mod}`uklib` is in its draft stage, and its contents are subject to change as development
continues.
```

## Overview

The **uklib** library packages **seven reference liability cash flow projection models**
for the individual life insurance products sold in the United Kingdom — plus the pension
annuity — built with modelx, and, for each one, the product specification and technical
notes the model was built from.

Annuities are core long-term insurance business and the dominant liability of UK life
insurers, and the centrepiece of the Solvency UK matching adjustment, so a UK library
without them would misrepresent the market. The coverage differs in kind from
[uslib](../uslib/index.md)'s: the UK retail deferred-annuity market is negligible, and
the pension annuity bought with a pension pot is the product that matters. Group
protection, pensions wrappers (drawdown, SIPPs) and bulk purchase annuities are out of
scope.

The models are the centre of the library. Each is a by-model-point projection of one
product's gross liability cash flows: premiums, claims, surrenders, expenses and
commission, on the product's own processing order and timing. None of them discounts —
every model publishes the cash flows and leaves discounting, reserving and capital to a
layer that consumes them.

**Each one of these models reproduces a documented worked example, asserted cell by cell
to the precision the notes display**. The chain is deliberate and complete in both
directions:

- `product-spec.md` specifies a *representative* product — a standardized composite built
  from publicly available documentation of real products, not any single insurer's
  contract. It records contractual mechanics, a full parameter set, the observed variation
  across insurers, and the rationale for every representative choice.
- `technical-notes.md` turns that product into a liability cash flow model on paper: model
  point attributes, state variables, assumption inputs, the recursions with their explicit
  processing order, policyholder behaviour, and a numeric worked example.
- The **model** implements those notes, and the library's own `tests/` assert the worked
  example against it. Change an assumption, and the test tells you whether the model and
  the notes have parted company.
- `sources.md` lists every source the first two cite, with URLs, access dates and whether
  the document was actually retrieved.

Every quantitative parameter in the library is either **source-tagged** or marked
**[std]** — a standardization introduced for the reference implementation, carrying its
rationale and, where available, the observed range across insurers. Facts taken from source
material are never silently mixed with assumptions made to complete a model.

```{admonition} These are mechanics demonstrations, not pricing or reserving results
:class: warning

The contractual elements are sourced. **Every decrement basis shipped here is a [std]
proxy**, because the CMI tables that a UK insurer would actually use are restricted to
Authorised Users and cannot be redistributed — see
[What is UK-specific about these models](#uklib-uk-specific). Nor is there any public
premium rate card: UK protection and annuity pricing is quote-driven. Replace both with
company data before drawing any conclusion from the numbers.
```

## The models

Model names are `<product>_<country>_<grid>`: the short name the product is actually known
by — `CI`, `IP`, `WOL`, `ULB`, `WP`, `PA` — then `UK`, then `_A` for an annual step or `_S`
for a monthly one. The grid letters follow lifelib, where `annuallife/TradLife_A` is the
annual-step model and `basiclife/BasicTerm_S` and `savings/CashValue_SE` are the monthly
ones. `S` carries a second sense in lifelib — scalar, one model point at a time, as against
the vectorized `_M` models — and that is true of all seven here, whether or not they carry
the letter.

**Protection**

| Product | Model | Grid | Representative design |
|---|---|---|---|
| [Term assurance](products/term_assurance/index.md) | `Term_UK_A` | annual | Guaranteed-premium term in three benefit shapes — level, decreasing at a client-selected mortgage rate, and family income benefit — with terminal illness benefit included and optional RPI indexation; expires at end of term, with no U.S.-style post-level-term tail |
| [Critical illness cover](products/critical_illness/index.md) | `CI_UK_S` | monthly | Accelerated life-or-CI level term on the **term-assurance chassis**: ~40 ABI-aligned full-payment conditions including TPD, 25%/£25k additional-payment conditions, 50%/£25k children's cover, 14-day survival period; standalone variant minus the death benefit |
| [Income protection](products/income_protection/index.md) | `IP_UK_S` | monthly | Full-term guaranteed-premium own-occupation IP: two-band earnings cap (65% to £60k, 50% above), deferred periods 4–52 weeks, RPI escalation in claim, proportionate benefit on partial return to work — the one **three-state** model here, healthy / sick / dead |
| [Whole of life](products/whole_of_life/index.md) | `WOL_UK_S` | monthly | Two cells: underwritten guaranteed whole of life, protection-only with no cash value — unlike U.S. whole life — and over-50s guaranteed acceptance, a fixed cash sum with a 12-month moratorium, premiums ceasing at 90, lapse-supported |

**Savings**

| Product | Model | Grid | Representative design |
|---|---|---|---|
| [With-profits](products/with_profits/index.md) | `WP_UK_A` | annual | 90:10 proprietary fund on retrospective asset shares: 80–120% payout target range, smoothing caps, MVR bounded by the asset-share shortfall; unitised WP as the primary cell and conventional WP endowment as the legacy one |
| [Unit-linked investment bond](products/unit_linked_bond/index.md) | `ULB_UK_S` | monthly | Modern clean-charge onshore single-premium bond: 100.1% death uplift, segmented mini-policies, AMC-based charges, the 5% p.a. tax-deferred withdrawal machinery; modeled through the classic UK **unit / non-unit** cash flow decomposition |

**Annuity**

| Product | Model | Grid | Representative design |
|---|---|---|---|
| [Pension annuity](products/pension_annuity/index.md) | `PA_UK_S` | monthly | Immediate lifetime annuity on a single carrier's pattern: single or joint life, escalation nil / fixed / RPI-floored / LPI, guarantee period XOR value protection, enhanced terms as a mortality-rating overlay. Longevity is the model |

### One shape, enforced

Every model has the same two Spaces — `Data` reads the input CSVs once per model, and
`Projection` is parameterized by `point_id` — with inputs as **external** CSVs beside
`run.py`, so the model folder holds formulas and nothing else. `Projection`'s docstring
carries the mapping from the technical notes' actuarial symbols to the cells names.

That shape is asserted rather than merely described: `tests/test_model_conventions_uk.py`
applies it to every model in the registry, and each model additionally has its own test
module for its worked example and its product-specific invariants — the notes' "Known
modeling pitfalls" sections are written up there as tests.

The pairing of model name to folder is deliberately *not* derivable from the folder name —
`unit_linked_bond` spelled out is unusable in a model name — so it is registered once in
`tests/uk_registry.py`, and the conventions suite asserts that the registry, the directory
on disk and the model's own `_name` all agree, along with the country and grid tags.

The registry is per library; the contract it enforces is the one
[uslib is held to](#uslib-one-shape), and cells names come from lifelib —
`basiclife/BasicTerm_S` first, then `savings/CashValue_SE` — so a name means the same thing
here, in uslib, and in lifelib. The
[shared vocabulary table](#uslib-shared-vocabulary) is the settled ruling for both
libraries.

(uklib-uk-specific)=

### What is UK-specific about these models

Three things recur across the set and are worth knowing before reading any one of them.

**Every mortality and morbidity basis shipped here is a [std] proxy.** The CMI's tables —
the "16" Series assured-lives tables, SAPS S3/S4, IP11, the CI diagnosis tables — are
restricted to Authorised Users, so no current UK insured rate can be redistributed. The
decrement tables shipped here — `mort_table.csv`, and the CI, inception and termination
tables beside them — are ONS-shaped or notes-derived constructions, anchored so that the
model's best-estimate factor reproduces the notes' own placeholder rate exactly. **This is
the single largest gap between these models and a production one**, and it is why every
`model.md` opens by saying the model is a mechanics demonstration rather than a pricing or
reserving result.

**Where a worked example is on a different basis from a realistic run, the basis is a
model point column** rather than a switch buried in a formula — the `mort_basis` column in
both `Term_UK_A` and `PA_UK_S` — following
[uslib's immediate annuity](../uslib/products/immediate_annuity/index.md) precedent. The
alternative, silently running the notes' illustrative basis as if it were the projection
basis, is the failure this pattern exists to prevent.

**Scope limits are stated and validated against, not faked.** With-profits' smoothed-fund
(PruFund) chassis is out of scope because its smoothing limits are daily and quarterly and
an annual grid smooths away the mechanics that define it, so `WP_UK_A.chassis()` rejects it
by name; the stochastic guarantee valuation the with-profits notes require is out of scope,
and the model says what it does and does not produce. Where a deterministic run cannot
reach a mechanic, that is stated rather than smoothed over: `PA_UK_S`'s RPI catch-up
ratchet degenerates to fixed escalation under a monotone inflation path, because the zero
floor, the ratchet and the LPI cap are all inflation options that a deterministic path
values at intrinsic only; and `IP_UK_S` holds the amount-payable ratio at 1, which
overstates outgo and understates nothing.

### Chassis relationships

Products that share machinery point at the file where it is specified rather than silently
restating it, and each pointer states what it inherits and where it deviates:

- **Critical illness** states only its deltas against the
  [term assurance technical notes](products/term_assurance/technical-notes.md) — the same
  decrement and premium chassis, with the accelerated benefit and the overlap factor on
  top.
- **The unit-linked bond's** smoothed-fund (PruFund) variation cross-references the
  [with-profits mechanics](products/with_profits/technical-notes.md) rather than restating
  the smoothing rules, and records why that chassis is out of scope for an annual grid.

## How to use the library

Create your own copy of the *uklib* library, as described in the
{ref}`create-a-project` section. For example, to copy it to *C:\\path\\to\\your\\uklib*:

```python
>>> import lifelib

>>> lifelib.create("uklib", r"C:\path\to\your\uklib")
```

Each model reads from its own directory, so run one directly:

```bash
python products/term_assurance/run.py
```

or read it and take the cash flow statement:

```python
>>> import modelx as mx

>>> model = mx.read_model("products/term_assurance/Term_UK_A")

>>> model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is each model's worked-example anchor cell.
`result_cf()` returns a tidy `DataFrame` indexed by `t` with one column per cash flow line.

The tests ship inside the library and run against *your* copy:

```bash
python -m pytest tests -q
```

## Library contents

```{list-table}
:header-rows: 1
:widths: 28 72

* - File or folder
  - Description
* - `products/<product>/`
  - One directory per product, holding its documents *and* its model together. Seven of them.
* - `products/<product>/product-spec.md`
  - The representative product specification: mechanics, parameters, variation across insurers.
* - `products/<product>/technical-notes.md`
  - The liability cash flow model on paper: state variables, recursions, processing order, worked example.
* - `products/<product>/model.md`
  - How the model implements those notes — what was standardized, what diverges, what the tests cover.
* - `products/<product>/sources.md`
  - Every source the product's documents cite, with URLs, access dates and retrieval status.
* - `products/<product>/<Model>/`
  - The modelx model itself. Formulas only — no embedded data.
* - `products/<product>/*.csv`
  - The model's inputs, external to the model folder so they can be edited or swapped in place.
* - `products/<product>/run.py`
  - Reads the model and prints its cash flow statement.
* - `references/`
  - The cross-product regulatory and actuarial bibliography, cited as `[REG-R#]`.
* - `tests/`
  - One module per model for its worked example and invariants, plus `test_model_conventions_uk.py` for the house style, and `uk_registry.py` carrying the model registry.
* - `_research/`
  - The raw research notes every citation traces back to. Provenance, not documentation — shipped but not rendered.
```

`_research/` carries one file per product plus `regulatory-actuarial.md`, and records which
documents were actually retrieved and which fetches failed. Its source lists are **never
renumbered**: the product documents cite against them.

(uklib-citation-conventions)=

## Citation conventions

Whether a citation tag is a link tells you what kind of source it is. `[R1]` and
`[REG-R18]` are links: the first lands on entry R1 in **that product's** `sources.md`, the
second on entry R18 of the shared
[reference library](references/regulatory-and-actuarial-references.md). `[S6]` is not a
link. It stays on the page as you see it, brackets and all, and names entry S6 in that
product's `sources.md` for you to look up.

That asymmetry is deliberate, and it is the same line the `sources.md` files draw between
their own sections. A regulatory or actuarial reference is an **authority** the model is
held to, and following it is part of reading the document. A primary product source is a
**specification** citation — the key features document or policy conditions a number was
taken from — which says where a figure came from rather than what the model must obey. So
one reads as a tag on the page and the other as a link off it.

Numbering is per product — S1 is a different source in each — so tags resolve against the
document's own product rather than one global list.

| Tag | On the page | Meaning |
|---|---|---|
| `[S#]` | bracketed text | Fact taken from a primary product document (key features document, policy conditions, terms and conditions, PPFM, fund guide) listed in the product's `sources.md` |
| `[R#]` | link | Fact taken from a product-specific regulatory/actuarial reference in the product's `sources.md` |
| `[REG-R#]` | link | Fact taken from the cross-product reference library (frozen R-numbering) |

(uklib-std)=

**[std]** — a *standardization introduced for the reference implementation*: a parameter or
convention chosen where sources vary, are proprietary, or are silent. Each carries a
rationale and, where available, the observed range across insurers.

(uklib-unverified)=

**[unverified]** — a claim from general knowledge or a secondary snippet that could **not**
be confirmed against a retrieved document. Treat it as a to-verify item, not an established
fact.

The hard rule throughout: **every quantitative parameter is either source-tagged or marked
[std]**. In this library that rule does most of its work on the decrement bases, which are
**[std]** proxies throughout because the CMI tables cannot be redistributed — see
[What is UK-specific about these models](#uklib-uk-specific).

## Regulatory and actuarial reference library

The [reference library](references/regulatory-and-actuarial-references.md) is the curated
cross-product bibliography — frozen numbering **R1–R38**, cited as `[REG-R#]` — with a
product-relevance matrix. It spans the prudential framework (Solvency UK: technical
provisions and BEL, risk margin, the matching adjustment and its 2023–24 reforms, the PRA
Rulebook and supervisory statements), FCA conduct rules (COBS 20 with-profits and PPFMs,
COBS 21.3 permitted links, Consumer Duty), legislation and tax (FSMA/RAO long-term business
classes, ITTOIA 2005 chargeable events, I-E and BLAGAB, Insurance Act 2015 and CIDRA,
pension freedoms), the CMI/ONS mortality and morbidity landscape, FRC Technical Actuarial
Standards and IFoA APS, and IFRS 17.

## Known gaps and caveats

Aggregated from the per-product research; each product's documents carry the full list.

- **CMI tables are subscriber-restricted.** The current UK experience tables (the "16"
  Series assured-lives tables, SAPS S3/S4 annuitant tables, IP11 income-protection rates,
  CI diagnosis tables) and the CMI Mortality Projections Model are available only to CMI
  authorised users. The reference bases here are honest **[std]** proxies built from public
  materials — ONS national life tables, older public table families — with the CMI
  framework cited by name for structure. A production implementation must license the real
  tables.
- **No public premium rate cards.** UK protection and annuity pricing is quote-driven; no
  insurer publishes rate tables. Pricing anchors are example quotes captured from key
  features documents — £100,000 at 65 buying £6,657 p.a. with 50% value protection, January
  2026 — with **[std]** rate scales constructed around them.
- **Bot-blocked primary sources.** The ABI Guide to Minimum Standards for Critical Illness
  Cover, parts of the FCA Handbook (JS-rendered), PRA PS10/24 and SS7/18, and one insurer's
  with-profits PPFMs could not be machine-fetched; facts relying on them are triangulated
  from secondary material and tagged accordingly.
- **Vintage issues.** Some retrieved documents are older editions — a single insurer's
  pension annuity terms of 2019/20 via a mirror, and its over-50s pages dated 2016.
  Structural mechanics are stable but parameter details may be stale; disclosed wherever
  used.
- **[unverified] items remain** wherever a claim could not be confirmed against a retrieved
  document: the ICOBS chapter mapping for pure protection, market-share claims, one
  provider's funeral benefit partner option.

```{toctree}
:hidden:
:maxdepth: 1
:caption: Products

products/term_assurance/index
products/critical_illness/index
products/income_protection/index
products/whole_of_life/index
products/with_profits/index
products/unit_linked_bond/index
products/pension_annuity/index
```

```{toctree}
:hidden:
:maxdepth: 1
:titlesonly:
:caption: Reference

references/regulatory-and-actuarial-references
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[std]: #uklib-std
[unverified]: #uklib-unverified
<!-- END generated citation links -->
