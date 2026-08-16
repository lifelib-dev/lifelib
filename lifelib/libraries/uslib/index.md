```{module} uslib
```

# The **uslib** Library

```{warning}
{mod}`uslib` is in its draft stage, and its contents are subject to change as development
continues.
```

## Overview

The **uslib** library packages **twelve reference liability cash flow projection models**
for the individual life insurance and annuity products sold in the United States, built
with modelx — and, for each one, the product specification and technical notes the model
was built from.

The models are the centre of the library. Each is a by-model-point projection
of one product's gross liability cash flows: premiums, claims, surrenders, withdrawals,
expenses and commissions, on the product's own processing order and timing. None of them
discounts — every model publishes the cash flows and leaves discounting, reserving and
capital to a layer that consumes them.

**Each one of these models reproduces a documented worked example,
asserted cell by cell to the precision the notes display**. The chain is deliberate and
complete in both directions:

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

The contractual elements are sourced; most behavioural and expense assumptions are
**[std]**, because no public source carries them. Current non-guaranteed scales — declared
crediting rates, current COI, IUL caps — are not public at all. Replace them with company
data before drawing any conclusion from the numbers.
```

## The models

Model names are `<product>_<country>_<grid>`: the short name the product is actually known
by — `MYGA`, `FIA`, `RILA`, `SPIA`, `DIA`, `ULSG` — then `US`, then `_A` for an annual step
or `_S` for a monthly one. The grid letters follow lifelib, where `annuallife/TradLife_A` is
the annual-step model and `basiclife/BasicTerm_S` and `savings/CashValue_SE` are the monthly
ones. `S` carries a second sense in lifelib — scalar, one model point at a time, as against
the vectorized `_M` models — and that is true of all twelve here, whether or not they carry
the letter.

**Life**

| Product | Model | Grid | Representative design |
|---|---|---|---|
| [Level premium term](products/term_life/index.md) | `Term_US_A` | annual | Guaranteed level premiums for 10/20/30 years, then jump-to-ART renewal at unchanged face to attained age 95; convertible until min(end of level period, age 70); no cash value |
| [Whole life](products/whole_life/index.md) | `WholeLife_US_A` | annual | Participating level-premium WL on a 2017 CSO / 4% nonforfeiture basis, three-factor contribution dividends, paid-up-additions default; plus a non-par final-expense variant |
| [Universal life](products/universal_life/index.md) | `UL_US_S` | monthly | Flexible-premium current-assumption UL: monthly deductions, declared crediting over a guaranteed minimum, GPT corridor, DB options A/B — the **base chassis** for the three below |
| [Indexed UL](products/indexed_ul/index.md) | `IUL_US_S` | monthly | UL chassis + S&P 500 annual point-to-point index account with cap, 100% participation, 0% floor — the AG 49-A benchmark design |
| [Variable UL](products/variable_ul/index.md) | `VUL_US_S` | monthly | UL chassis + unitized separate-account subaccounts and a fixed option; SEC-registered, so charges are anchored on prospectus fee tables |
| [Guaranteed UL](products/guaranteed_ul/index.md) | `ULSG_US_S` | monthly | UL chassis + shadow-account secondary guarantee (AG 38 §8E Design #1), funded by a solved level no-lapse premium; lapse-supported economics |

**Annuity**

| Product | Model | Grid | Representative design |
|---|---|---|---|
| [Fixed deferred (MYGA)](products/fixed_deferred_annuity/index.md) | `MYGA_US_S` | monthly | Single-premium book-value annuity: multi-year declared rate, surrender charge plus market value adjustment, Model #805 floor — the **deferred base chassis** |
| [Fixed indexed (FIA)](products/fixed_indexed_annuity/index.md) | `FIA_US_S` | monthly | Index-linked credits at a 0% floor, premium bonus with vesting, and a guaranteed lifetime withdrawal benefit that continues after the account value is exhausted |
| [Variable annuity](products/variable_annuity/index.md) | `VA_US_S` | monthly | Separate-account deferred annuity: subaccount units net of M&E, a guaranteed minimum death benefit, and a lifetime withdrawal rider fee-assessed on the benefit base |
| [Registered index-linked (RILA)](products/registered_index_linked_annuity/index.md) | `RILA_US_S` | monthly | SEC-registered buffered annuity: point-to-point terms with a downside buffer and upside cap, and an AG 54 interim value |
| [Immediate (SPIA)](products/immediate_annuity/index.md) | `SPIA_US_S` | monthly | Single premium converted immediately into a payment stream; life only, period certain, joint and survivor, refund forms, compound COLA — the **payout chassis** |
| [Deferred income (DIA/QLAC)](products/deferred_income_annuity/index.md) | `DIA_US_S` | monthly | Flexible-premium contract with **no account value**: each premium buys a paid-up income slice, with a return-of-premium deferral death benefit and a QLAC variant |

(uslib-one-shape)=

### One shape, enforced

Every model has the same two Spaces — `Data` reads the input CSVs once per model, and
`Projection` is parameterized by `point_id` — with inputs as **external** CSVs beside
`run.py`, so the model folder holds formulas and nothing else. `Projection`'s docstring
carries the mapping from the technical notes' actuarial symbols to the cells names.

That shape is asserted rather than merely described: `tests/test_model_conventions.py`
applies it to every model in the registry, and each model additionally has its own test
module for its worked example and its product-specific invariants — the notes' "Known
modeling pitfalls" sections are written up there as tests.

The pairing of model name to folder is deliberately *not* derivable from the folder name —
`registered_index_linked_annuity` spelled out is unusable and the industry says RILA — so it
is registered once in `tests/us_registry.py`, and the conventions suite asserts that the
registry, the directory on disk and the model's own `_name` all agree.

(uslib-shared-vocabulary)=

### Shared vocabulary

Cells names come from lifelib — `basiclife/BasicTerm_S` first, then `savings/CashValue_SE` —
so a name means the same thing in every model here and the same thing it means in lifelib.
Where a cross-model review found one concept under two names, the conflict was settled once
and the ruling is asserted, not merely documented:

| Convention | Settled as |
|---|---|
| In-force count | `pols_if(t)` is the count at the **start** of period `t`, and is the weight on that same `result_cf()` row's cash flows. End-of-period state is reachable through `pols_if_at(t, timing)` |
| Rates | `mort_rate` / `lapse_rate` are **annual**; `mort_rate_mth` / `lapse_rate_mth` are monthly |
| Net cash flow | `net_cf` is **income-positive** in every model. Where a product's notes print the stream outgo-positive (whole life, both payout annuities), that orientation survives verbatim as `liability_cf`, and `net_cf(t) == -liability_cf(t)` |
| Roll-forward checks | `check_*()` takes no argument and returns `bool` over all `t` (the `CashValue_SE` form); a per-`t` residual lives at `check_*_resid(t)` |
| Account value | `av_pp_at(t, timing)` / `av_at(t, timing)` with the `CashValue_SE` timing strings; `prem_to_av_pp` is the premium credited to it |
| Withdrawals | `withdrawals(t)`, in a `withdrawals` column — an owner election, not a claim |
| Benefit columns | `claims_death`, `claims_lapse`, `claims_maturity`, … named for the `kind` argument that produces them |

Absences are product facts, not gaps: a SPIA has no `premiums` and no lapse decrement, the
payout annuities model `lives_if` (annuitant survival) alongside `pols_if` (contracts with
an obligation open), and whole life has a cash value `cv_pp`, not an account value.

### Chassis relationships

Products that share machinery point at the file where it is specified rather than silently
restating it, and each pointer states what it inherits and where it deviates:

- **Life** — the UL-family documents (indexed, variable, guaranteed) reference the
  [universal life technical notes](products/universal_life/technical-notes.md) for the
  shared base-chassis recursion, anchored on a retrieved specimen policy; deviations, such
  as VUL's prospectus-sourced NAAR convention, are flagged explicitly.
- **Annuity, deferred** — the fixed-indexed and variable annuity documents inherit the
  *structure* of the [fixed deferred annuity](products/fixed_deferred_annuity/technical-notes.md)
  chassis — surrender benefit composition, nonforfeiture floor, death benefit at account
  value — while carrying their own recursions and parameters.
- **Annuity, payout** — the deferred income annuity and the annuitization phase of the RILA
  reference the [immediate annuity](products/immediate_annuity/technical-notes.md) payout
  chassis symbol-for-symbol, stating their deltas.
- **Across families** — where an annuity document borrows from a life document, it states
  the differences: an annuity has no cost of insurance, no net amount at risk, and no death
  benefit corridor.

## How to use the library

Create your own copy of the *uslib* library, as described in the
{ref}`create-a-project` section. For example, to copy it to *C:\\path\\to\\your\\uslib*:

```python
>>> import lifelib

>>> lifelib.create("uslib", r"C:\path\to\your\uslib")
```

Each model reads from its own directory, so run one directly:

```bash
python products/term_life/run.py
```

or read it and take the cash flow statement:

```python
>>> import modelx as mx

>>> model = mx.read_model("products/term_life/Term_US_A")

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
  - One directory per product, holding its documents *and* its model together. Twelve of them.
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
  - One module per model for its worked example and invariants, plus `test_model_conventions.py` for the house style, and `us_registry.py` carrying the model registry.
* - `_research/`
  - The raw research notes every citation traces back to. Provenance, not documentation — shipped but not rendered.
```

## Citation conventions

Every citation tag is a link. `[S6]` in a product document lands on entry S6 in **that
product's** `sources.md`, and `[REG-R18]` lands on entry R18 of the shared
[reference library](references/regulatory-and-actuarial-references.md). Numbering is per
product — S1 is a different source in each — so tags resolve against the document's own
product rather than one global list.

| Tag | Meaning |
|---|---|
| `[S#]` | Fact taken from a primary product document (brochure, specimen policy, prospectus, producer guide) listed in the product's `sources.md` |
| `[R#]` | Fact taken from a product-specific regulatory/actuarial reference in the product's `sources.md` |
| `[REG-R#]` | Fact taken from the cross-product reference library (frozen R-numbering) |

(uslib-std)=

**[std]** — a *standardization introduced for the reference implementation*: a parameter or
convention chosen where sources vary, are proprietary, or are silent. Each carries a
rationale and, where available, the observed range across insurers.

(uslib-unverified)=

**[unverified]** — a claim from general knowledge or a secondary snippet that could **not**
be confirmed against a retrieved document. Treat it as a to-verify item, not an established
fact.

The hard rule throughout: **every quantitative parameter is either source-tagged or marked
[std]**.

## Regulatory and actuarial reference library

The [reference library](references/regulatory-and-actuarial-references.md) is the curated
cross-product bibliography — frozen numbering **R1–R157**, cited as `[REG-R#]` — with
separate product-relevance matrices for the life and annuity products. R1–R34 are
life-origin entries, several of which also bind annuity models; R35–R72 are
annuity-specific; R151–R157 are the seven AP&P Manual appendix items read at first hand.
Most of the R73–R149 block is unused: it was allocated to a statutory accounting and capital
research stream since retired from the library. Unused is not missing — the invariant is
that numbers are never reused or renumbered.

- **Life** — NAIC statutory framework (Standard Valuation Law, Standard Nonforfeiture Law,
  the Valuation Manual and VM-20, Models 582/585/787/830, AG 38/48/49/49-A/49-B), federal
  tax (IRC §§ 7702, 7702A, 807, 817), mortality tables and experience studies (2017 CSO,
  2015 VBT, ILEC, SOA persistency and post-level-term), AAA practice notes and ASOPs.
- **Annuity** — VM-21 and VM-22, formulaic CARVM under AG 33 and AG 35, AG 54 for
  index-linked interim values, Model #805 nonforfeiture and Models #245/#250/#275, C-3
  Phase II capital, SEC Form N-4 and the 2024 rule bringing RILAs onto it, IRC § 72 and the
  QLAC regulations as amended by SECURE 2.0, and the 2012 IAM/IAR tables with Scale G2.

## Known gaps and caveats

The significant ones, aggregated from the per-product research; each product's documents
carry the full list.

**Life**

- **Current non-guaranteed scales are not public.** Declared crediting rates, current COI
  scales and IUL caps/participation rates are producer-portal-only or point-in-time
  snapshots; the specs carry **[std]** values calibrated to observed ranges. Guaranteed
  elements are far better sourced.
- **Full rate and charge tables are largely proprietary.** The exceptions captured here: a
  complete guaranteed COI table and processing order from a UL specimen, a complete
  guaranteed premium schedule from a term specimen, final-expense WL premium rates per
  $1,000, and VUL prospectus fee tables.
- **ULSG shadow-account parameters are unobservable**, so that parametrization is wholly
  **[std]**, calibrated so the solved no-lapse premium resembles observed market premiums.
- **Era mixing.** Some retrieved specimens are 2001-CSO-era while the representative specs
  are stated on a 2017 CSO basis; disclosed wherever it occurs.

**Annuity**

- **No public payout factors or purchase rates**, for SPIAs, DIAs, or the annuitization
  option of any deferred product. Income figures in these documents are captured
  illustrations, never derived rates, so no pricing test against public data is possible.
- **Market value adjustment algebra is thinly sourced.** Three MVA families were retrieved
  with sharply differing cap treatments, but no retrieved *MYGA* document states its own MVA
  algebra — the representative formula is inferred from same-family documents and says so.
- **Commutation and interim-value formulas are unpublished** for fixed SPIAs and DIAs.
  RILA interim values are the exception: AG 54 mandates their structure.
- **Behavioural assumptions are order-of-magnitude anchors.** Surrender-charge-expiry shock
  lapse, its suppression when a lifetime-withdrawal rider is in force, and rider utilization
  are the first-order drivers of annuity liability value, yet the calibrating studies are
  paywalled; the shipped values are **[std]** with their evidence quality stated.

```{toctree}
:hidden:
:maxdepth: 1
:caption: Products

products/term_life/index
products/whole_life/index
products/universal_life/index
products/indexed_ul/index
products/variable_ul/index
products/guaranteed_ul/index
products/fixed_deferred_annuity/index
products/fixed_indexed_annuity/index
products/variable_annuity/index
products/registered_index_linked_annuity/index
products/immediate_annuity/index
products/deferred_income_annuity/index
```

```{toctree}
:hidden:
:maxdepth: 1
:titlesonly:
:caption: Reference

references/regulatory-and-actuarial-references
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
