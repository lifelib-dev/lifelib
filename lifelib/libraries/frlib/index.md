```{module} frlib
```

# The **frlib** Library

```{warning}
{mod}`frlib` is in its draft stage, and its contents are subject to change as development
continues.
```

## Overview

The **frlib** library packages **nine reference liability cash flow projection models**
for the individual life insurance products sold in France, built with modelx, and, for
each one, the product specification and technical notes the model was built from.

The coverage follows the French market rather than a template. *Assurance vie* is not one
product among several in France — it is the country's savings vehicle, and the split
between its two supports, the guaranteed **fonds en euros** and the **unités de compte**
whose units alone are guaranteed, is the first fact about any French life balance sheet.
So three of the nine slots go to *assurance vie* and its **eurocroissance** hybrid, a
fourth to the **PER** that the *loi PACTE* built on the same chassis, and a fifth to the
**rente viagère** they pay out into. On the protection side, **assurance emprunteur** —
the cover a French borrower buys with a mortgage — is the largest individual protection
market in the country and has no counterpart in
[uslib](../uslib/index.md) or [uklib](../uklib/index.md); it takes a slot of its own
beside plain **temporaire décès**, the **contrat obsèques** French households buy in
volume, and individual **dépendance** cover. Group business, *contrats collectifs*,
*épargne salariale* and *assurance vie luxembourgeoise* are out of scope.

The models are the centre of the library. Each is a by-model-point projection of one
product's gross liability cash flows: *versements*, *prestations*, *rachats*, charges and
expenses, on the product's own processing order and timing. None of them discounts — every
model publishes the cash flows and leaves discounting, *provisions techniques* and capital
to a layer that consumes them.

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

The contractual elements are sourced, and in this library unusually well: French contract
law and the *Code des assurances* are on Légifrance, which serves in full, so the
participation aux bénéfices machinery, the eurocroissance provisions and the *loi Lemoine*
substitution rights are quoted from the instruments themselves rather than from
commentary. **Every decrement basis shipped here is a [std] proxy.** The mortality tables a
French insurer must use — TH 00-02 / TF 00-02 and the generational TGH05 / TGF05 — are
annexed to an *arrêté* and are cited by name throughout, but this library does not
redistribute them, and *tables d'expérience* certified by an actuary are by construction
not public. Nor is there any published rate card: French pricing is quote-driven, and the
*encadré* a contract must carry discloses charge **maxima**, not levels. Replace both with
company data before drawing any conclusion from the numbers. See
[What is French about these models](#frlib-france-specific).
```

## The models

Model names are `<product>_<country>_<grid>`: the short form the French market itself uses
where there is one — `UC`, `PER`, `ADE`, `EC` — a short descriptor where there is none,
then `FR`, then `_A` for an annual step or `_S` for a monthly one. The grid letters follow
lifelib, where `annuallife/TradLife_A` is the annual-step model and `basiclife/BasicTerm_S`
and `savings/CashValue_SE` are the monthly ones. `S` carries a second sense in lifelib —
scalar, one model point at a time, as against the vectorized `_M` models — and that is true
of all nine here.

All nine run on a **monthly** grid, the euro fund, eurocroissance, PER and temporaire décès
models included since their conversion.

Where a product's contractual drivers *are* annual — the *cotisation révisable par âge*
repriced at each renewal, the *taux servi* an insurer declares for the closing financial
year and the PPB's eight-year release clock, eurocroissance's annual rebalancing and its
guarantee at the *échéance*, the *gestion pilotée* allocation grid keyed by years to the
horizon — the model keeps those events on the policy anniversary and derives the policy
year from `t` (`duration(t) = t // 12`), rather than stepping annually. A monthly grid is
not the same thing as a monthly product: what the finer grid resolves is everything that is
*not* a contractual event — mortality, PTIA and *rachat* falling in the month they happen,
provisions accruing month by month so a mid-year exit is valued on the balance it actually
has, and expenses and the elected *fractionnement* falling where they are incurred. The two
grids agree on the in-force at every anniversary and on every anniversary-dated contractual
quantity; they differ on cash flow timing, which is what the monthly grid is for.

**Épargne**

| Product | Model | Grid | Representative design |
|---|---|---|---|
| [Assurance vie — fonds en euros](products/assurance_vie_euro/index.md) | `Euro_FR_S` | monthly | The guaranteed support: *épargne acquise* rolled forward at a *taux servi* the insurer declares each year, floored by the statutory participation aux bénéfices and by a TMG that modern contracts set at zero, with the **effet cliquet** asserted as an invariant and the **PPB** carried as a per-vintage ledger so its eight-year release clock is a real deadline rather than an average. *Prélèvements sociaux* fall **au fil de l'eau**. The crediting machinery is a financial-year statement and lands whole at 31 December; the account movements, the expenses and the decrements are monthly, so a mid-year exit takes the announced floor rate *pro rata temporis* — nil at the TMG every shipped model point carries |
| [Assurance vie — unités de compte](products/assurance_vie_uc/index.md) | `UC_FR_S` | monthly | Modern *multisupport* contract on the classic **unit / non-unit** decomposition: the insurer guarantees the number of units and not their value, charges are taken by cancelling units, and the **garantie plancher** is a net-amount-at-risk cover whose charge is levied on the NAR and whose NAR is zero whenever the units sit above the floor. The euro leg is an allocation share pointing at `Euro_FR_S`, not a second implementation |
| [Eurocroissance](products/eurocroissance/index.md) | `EC_FR_S` | monthly | The statutory hybrid: a *provision mathématique* accumulating at the *taux technique* toward a guarantee that bites **only at the échéance**, and a *provision de diversification* carrying the upside in parts, rebalanced annually. A surrender before term pays the current part value with **no guarantee at all** — the fact an implementation is most likely to floor away. The *provision de diversification* is re-struck monthly at a fractional remaining term, as art. A. 134-5 requires; the two levies, the *versements* and the *apport* stay on the anniversary |

**Retraite**

| Product | Model | Grid | Representative design |
|---|---|---|---|
| [PER assurantiel](products/per_assurance/index.md) | `PER_FR_S` | monthly | The *loi PACTE* plan on the *assurance vie* chassis: three compartments, **gestion pilotée par horizon** shipped as an allocation grid keyed by years to the horizon, and two exits that are decrements but are **not lapses** — *déblocage anticipé* and transfer out, the second capped at 1% and free after five years. The glide path is keyed by years to the horizon and so rebalances on the anniversary, while the account value, the charges and all three decrements run monthly |
| [Rente viagère immédiate](products/rente_viagere/index.md) | `Rente_FR_S` | monthly | Immediate life annuity on the payout chassis this library shares with `PA_UK_S` and `SPIA_US_S`: *terme échu* or *terme à échoir*, *réversion*, *annuités garanties* as an annuity-certain floor, *frais d'arrérages* on every *quittance*, and revalorisation out of the participation aux bénéfices — discretionary, and therefore not an escalation guarantee. Priced on a **generational** table, so no improvement scale sits on top of it |

**Prévoyance**

| Product | Model | Grid | Representative design |
|---|---|---|---|
| [Temporaire décès](products/temporaire_deces/index.md) | `TD_FR_S` | monthly | Individual term cover in the French form: the premium is a **cotisation annuelle révisable par âge** that rises each year with attained age, with the level alternative as a model point column; PTIA accelerates the death capital and is never paid twice; the first-year suicide void; and no surrender or paid-up value of any kind. Contractually annual end to end, so the tariff, the suicide year and the *délai d'attente* sit on the anniversary and the finer grid buys the *fractionnement* and the timing of claims |
| [Assurance emprunteur](products/assurance_emprunteur/index.md) | `ADE_FR_S` | monthly | The cover sold with a mortgage, over a **deterministic amortising loan** the model computes: décès and PTIA paying `CRD × quotité`, ITT paying the *échéance* after a *franchise* and for at most 1 095 days, IPT beyond the 66% threshold — with age limits that differ **by guarantee**, so cover can end before the loan does, and *résiliation à tout moment* under the *loi Lemoine* as the behavioural heart |
| [Contrat obsèques](products/obseques/index.md) | `Obseques_FR_S` | monthly | Small guaranteed-acceptance *vie entière* on three premium forms — *prime unique*, *primes temporaires*, *primes viagères* — the last of which can and does pay in more than the capital. The *délai de carence* is two benefits, not one: a refund of premiums on death by illness inside it, the full capital on accidental death from day one. The capital is revalued annually and is a state variable |
| [Dépendance](products/dependance/index.md) | `Dep_FR_S` | monthly | Individual LTC paying a *rente viagère* on entry into dependence, with *dépendance partielle* at half the *rente totale* and a *capital d'équipement* paid once. A multi-state projection with **state-dependent mortality**, a *carence* that varies by cause and a *franchise* that runs from recognition, and *mise en réduction* — a lapsing policyholder keeps a reduced *rente* rather than nothing |

(frlib-one-shape)=

### One shape, enforced

Every model has the same two Spaces — `Data` reads the input CSVs once per model, and
`Projection` is parameterized by `point_id` — with inputs as **external** CSVs beside
`run.py`, so the model folder holds formulas and nothing else. `Projection`'s docstring
carries the mapping from the technical notes' actuarial symbols to the cells names.

That shape is asserted rather than merely described: `tests/test_model_conventions_fr.py`
applies it to every model in the registry, and each model additionally has its own test
module for its worked example and its product-specific invariants — the notes' "Known
modeling pitfalls" sections are written up there as tests.

The pairing of model name to folder is deliberately *not* derivable from the folder name —
`assurance_emprunteur` spelled out is unusable in a model name — so it is registered once
in `tests/fr_registry.py`, and the conventions suite asserts that the registry, the
directory on disk and the model's own `_name` all agree, along with the country and grid
tags.

The registry is per library; the contract it enforces is the one
[uslib is held to](#uslib-one-shape), and cells names come from lifelib —
`basiclife/BasicTerm_S` first, then `savings/CashValue_SE` — so a name means the same thing
here, in uslib, in uklib and in lifelib. The
[shared vocabulary table](#uslib-shared-vocabulary) is the settled ruling
across the libraries.

The time index is the one every library shares, and the conventions suite asserts it for
every model point. **The time index `t` is 0-based and counts policy months**: `t = 0` is
the issue month of a policy projected from issue, period `t` runs from time `t` to time
`t + 1`, and the attained age is `age_at_entry + duration(t)` with `duration(t) = t // 12`,
so it steps on the policy anniversary rather than on the birthday and rather than monthly.
The convention is written to hold on either grid, because the registry still admits an
annual one: there `duration(t)` is `t` and the attained age is `age_at_entry + t`. **`proj_len()` is the number of periods from `t = 0`**, i.e. the
exclusive end of the frame: `result_cf()` covers `t = t_first, ..., proj_len() - 1`, where
`t_first` is 0 for a point projected from issue and the elapsed periods for an in-force
point — `EC_FR_S`'s in-force model points open partway through the term, at twelve times the
years the policy has already run, which is why the frame's start is asserted as contiguity
from `t_first` rather than pinned to 0. This is lifelib's own convention
(`basiclife/BasicTerm_S`, `savings/CashValue_SE`: `for t in range(proj_len())`). A
contractual policy year is the 1-based label `duration(t) + 1` and is derived, never indexed
by.

(frlib-france-specific)=

### What is French about these models

Four things recur across the set and are worth knowing before reading any one of them.

**Every decrement basis shipped here is a [std] proxy.** French insurers must reserve on
either a *table homologuée* — TH 00-02 and TF 00-02 for death cover, the generational
TGH05 and TGF05 for annuities, annexed to the *arrêté du 1er août 2006* and cited
throughout this library as [REG-R21] [REG-R22] [REG-R23] — or a *table d'expérience*
certified by an actuary, which by construction is the insurer's own and not public. This
library cites the homologated tables by name and article and **does not redistribute
them**; the tables shipped beside the models are INSEE-shaped constructions
[REG-R24], anchored so that each model's best-estimate factor reproduces its own notes'
placeholder rate exactly. **This is the single largest gap between these models and a
production one**, and it is why every `model.md` opens by saying the model is a mechanics
demonstration rather than a pricing or reserving result.

**Discretion is a modelled quantity, not a footnote.** The French savings products do not
credit a contractual rate; they credit a *taux servi* the insurer declares, floored by the
statutory participation aux bénéfices — 85% of the *compte financier* and the technical
result less the insurer's share of the greater of 10% of the credit balance and 4.5% of
premiums [REG-R15] — and smoothed through a *provision pour participation aux bénéfices*
that must be released within eight years [REG-R16]. `Euro_FR_S` carries that whole
machinery, including the PPB as a per-vintage ledger, and `EC_FR_S`, `Obseques_FR_S` and
`Rente_FR_S` consume a revalorisation that comes out of it. A model that treats the
crediting rate as an input rather than as an output of a constrained allocation has
modelled the wrong product — with one deliberate exception, stated here rather than left
to be discovered: `PER_FR_S` does exactly that. It carries no PPB stock and sets the euro
credit at the asset return, because a retirement model's interesting mechanic is the glide
path rather than the crediting rule. Its notes tag the simplification **[std]** and point
at the euro-fund notes for what it is standing in for.

**Unisex pricing sits on top of sex-distinct tables.** Since the Test-Achats ruling was
applied in France to contracts written from 21 December 2012, a tariff may not differ by
sex — while TH 00-02 / TF 00-02 and TGH05 / TGF05 remain sex-distinct. Insurers reconcile
the two with a portfolio mix assumption, and this library carries that reconciliation
explicitly as a **[std]** input rather than quietly pricing on one table: see
`Rente_FR_S`, where the difference between the unisex rate and the annuitant's own table is
about 13% of income, and `TD_FR_S`. The reconciliation is a real French mechanic and each of
the two models writes it up as a modelling pitfall.

**Scope limits are stated and validated against, not faked.** Where a deterministic run
cannot reach a mechanic, that is said rather than smoothed over. `Euro_FR_S` ships no
positive-TMG model point, because the notes' two statements of the TMG are consistent only
at zero and the model implements the notes verbatim rather than tuning to a formula the
notes themselves flag as inactive. The *loi Sapin 2* power to suspend surrenders
[REG-R13] exists, is out of the projection's scope, and is said to be. `EC_FR_S` rejects a
model point electing the *rente viagère* option by name, because such a point would have to
run past the *échéance* at which the projection stops.

### Chassis relationships

Products that share machinery point at the file where it is specified rather than silently
restating it, and each pointer states what it inherits and where it deviates:

- **The euro fund is the library's participating chassis.** The *unités de compte*
  contract's euro leg, the *obsèques* capital revalorisation and the *rente*'s
  revalorisation reference the
  [assurance vie euro technical notes](products/assurance_vie_euro/technical-notes.md) for
  the participation aux bénéfices mechanics rather than restating them. `PER_FR_S` points
  at the same file for the opposite reason — to say what it deliberately does *not*
  implement, its euro credit being a flat rate rather than an output of the PB
  allocation.
- **Temporaire décès is the protection chassis.** `ADE_FR_S` and `Obseques_FR_S` state
  their deltas against the
  [temporaire décès technical notes](products/temporaire_deces/technical-notes.md) — the
  same decrement and premium chassis, with the loan and the multi-state claim machinery on
  one and guaranteed acceptance with a moratorium on the other.
- **Across markets** — `Rente_FR_S` shares the payout **core** with
  [uklib's pension annuity](../uklib/products/pension_annuity/index.md) and
  [uslib's SPIA](../uslib/products/immediate_annuity/index.md): about forty names common to
  all three, including the `lives_if` / `payment_factor` / `certain_floor` machinery and
  `annual_income` for the amount being paid. It is a shared core rather than a shared
  vocabulary — roughly half of `Rente_FR_S`'s cells are the French *revalorisation*,
  *palier*, *arrérages* and unisex layer on top, and a few names the two twins share have
  no French counterpart. Its `model.md` tabulates where the three part, in both
  directions.

## How to use the library

Create your own copy of the *frlib* library, as described in the
{ref}`create-a-project` section. For example, to copy it to *C:\\path\\to\\your\\frlib*:

```python
>>> import lifelib

>>> lifelib.create("frlib", r"C:\path\to\your\frlib")
```

Each model reads from its own directory, so run one directly:

```bash
python products/assurance_vie_euro/run.py
```

or read it and take the cash flow statement:

```python
>>> import modelx as mx

>>> model = mx.read_model("products/assurance_vie_euro/Euro_FR_S")

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
  - One directory per product, holding its documents *and* its model together. Nine of them.
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
  - One module per model for its worked example and invariants, plus `test_model_conventions_fr.py` for the house style, and `fr_registry.py` carrying the model registry.
* - `_research/`
  - The raw research notes every citation traces back to. Provenance, not documentation — shipped but not rendered.
```

`_research/` carries one file per product plus `regulatory-actuarial.md`, and records which
documents were actually retrieved and which fetches failed. Its source lists are **never
renumbered**: the product documents cite against them.

(frlib-citation-conventions)=

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
**specification** citation — the *notice d'information*, *conditions générales* or
*document d'information clé* a number was taken from — which says where a figure came from
rather than what the model must obey. So one reads as a tag on the page and the other as a
link off it.

Numbering is per product — S1 is a different source in each — so tags resolve against the
document's own product rather than one global list.

| Tag | On the page | Meaning |
|---|---|---|
| `[S#]` | bracketed text | Fact taken from a primary product document (*notice d'information*, *conditions générales*, *document d'information clé*, *fiche standardisée d'information*, *tableau de garanties*) listed in the product's `sources.md` |
| `[R#]` | link | Fact taken from a product-specific regulatory/actuarial reference in the product's `sources.md` |
| `[REG-R#]` | link | Fact taken from the cross-product reference library (frozen R-numbering) |

(frlib-std)=

**[std]** — a *standardization introduced for the reference implementation*: a parameter or
convention chosen where sources vary, are proprietary, or are silent. Each carries a
rationale and, where available, the observed range across insurers.

(frlib-unverified)=

**[unverified]** — a claim from general knowledge or a secondary snippet that could **not**
be confirmed against a retrieved document. Treat it as a to-verify item, not an established
fact.

The hard rule throughout: **every quantitative parameter is either source-tagged or marked
[std]**. In this library that rule does most of its work on two things — the decrement
bases, which are **[std]** proxies throughout because the homologated tables are not
redistributed, and the charge levels, because the *encadré* a French contract must carry
discloses maxima rather than levels. See
[What is French about these models](#frlib-france-specific).

## Regulatory and actuarial reference library

The [reference library](references/regulatory-and-actuarial-references.md) is the curated
cross-product bibliography — frozen numbering **R1–R49**, cited as `[REG-R#]` — with a
product-relevance matrix. It spans the prudential frame (Solvabilité II and the *Code des
assurances* technical provisions, the PRE and the PAF, the ACPR, and the *loi Sapin 2* /
HCSF power), the participation aux bénéfices and guaranteed-rate machinery (arts. L. 331-3,
A. 132-10 to A. 132-16-1 and the TMG caps at A. 132-1 to A. 132-3), eurocroissance
(L. 134-1 and R. 134-1 to R. 134-12 with *décret* 2019-1437), the mortality and morbidity
landscape (the two *arrêtés* homologating TH 00-02 / TF 00-02 and TGH05 / TGF05, A. 335-1,
INSEE, and the DREES / CNSA dependency statistics), conduct and distribution
(*renonciation*, the *note d'information* and its *encadré*, surrender and payment on
death, the DDA and PRIIPs), legislation and tax (*loi PACTE* and the PER articles of the
Code monétaire et financier, *loi Lemoine* and the *Code de la consommation*, *loi Eckert*,
and CGI arts. 125-0 A, 990 I, 757 B and 163 quatervicies), the Institut des actuaires
professional standards, IFRS 17, and the France Assureurs market series.

## Known gaps and caveats

Aggregated from the per-product research; each product's documents carry the full list.

- **The homologated tables are not redistributed.** TH 00-02 / TF 00-02 and the
  generational TGH05 / TGF05 are annexed to *arrêtés* and are cited by name and article
  throughout, but the decrement tables shipped here are INSEE-shaped **[std]**
  constructions. *Tables d'expérience* certified by an actuary are the alternative a
  production implementation would use, and they are by construction not public.
- **No public rate card, and charge maxima rather than levels.** French pricing is
  quote-driven and the *encadré* a contract must carry discloses maximum charges. Every
  premium rate, annuity rate and charge level in the library is either a figure taken from
  a retrieved *document d'information clé* or a **[std]** construction, and each says which.
- **One host defeated retrieval; a second was recorded as blocked in error.**
  `eur-lex.europa.eu` sits behind a JavaScript challenge, so **no Solvency II or PRIIPs
  article number in this library was read from the instrument itself** — those entries are
  described from EIOPA and AMF material and are marked accordingly. The **ACPR is not
  blocked**, though the regulatory research file first recorded it as returning HTTP 403 to
  every request. It refuses the plain fetcher and serves `curl` with HTTP 200, identically
  with and without a browser `User-Agent`; and because the host answers a *wrong*
  `/system/files/` path with 403 rather than 404, one mistyped PDF URL was
  indistinguishable from a domain-wide block. The *Analyses et Synthèses* have since been
  retrieved and read, [REG-R11] and [REG-R12] are `Fetched: yes`, and the correction is
  recorded in the reference library's header rather than quietly applied — the figures it
  restored are the average *taux de revalorisation* of *fonds en euros*, its dispersion and
  the average *chargement sur encours*, which is the most load-bearing quantitative source
  in the library.
- **Thin public documentation for two products.** No *notice d'information*, *conditions
  générales* or PRIIPs *document d'information clé* for any eurocroissance support could be
  retrieved, so that product rests on the *Code des assurances* articles, which are
  retrievable in full, plus one published actuarial *mémoire* and third-party fact sheets.
  No French LTC incidence or continuance table is public, so `Dep_FR_S`'s bases are built
  from DREES and CNSA population material with the construction argued rather than asserted.
- **[unverified] items remain** wherever a claim could not be confirmed against a retrieved
  document — a handful of *Code des assurances* article placements where Légifrance served a
  pre-2016 version, the CGI 163 quatervicies carry-forward period where the article text and
  the BOFIP guidance disagree, and the market-share and taux-servi figures that only ACPR
  publishes.

```{toctree}
:hidden:
:maxdepth: 1
:caption: Products

products/assurance_vie_euro/index
products/assurance_vie_uc/index
products/eurocroissance/index
products/per_assurance/index
products/rente_viagere/index
products/temporaire_deces/index
products/assurance_emprunteur/index
products/obseques/index
products/dependance/index
```

```{toctree}
:hidden:
:maxdepth: 1
:titlesonly:
:caption: Reference

references/regulatory-and-actuarial-references
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[REG-R11]: #frlib-reg-r11
[REG-R12]: #frlib-reg-r12
[REG-R13]: #frlib-reg-r13
[REG-R15]: #frlib-reg-r15
[REG-R16]: #frlib-reg-r16
[REG-R21]: #frlib-reg-r21
[REG-R22]: #frlib-reg-r22
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
