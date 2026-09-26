```{module} delib
```

# The **delib** Library

```{warning}
{mod}`delib` is in its draft stage, and its contents are subject to change as development
continues.
```

## Overview

The **delib** library packages **ten reference liability cash flow projection models** for
the individual life, pension and biometric-risk products sold in Germany, built with
modelx, and, for each one, the product specification and technical notes the model was
built from.

The coverage follows the German market rather than a template, and the shape it follows is
the **Drei-Schichten-Modell** the *Alterseinkünftegesetz* imposed on German retirement
saving in 2005. Which layer a contract sits in decides more about it than what it invests
in: **Schicht 1** buys a deductible contribution and a fully taxed pension in exchange for
a product that may not be surrendered, commuted or assigned; **Schicht 2** buys a state
*Zulage* paid into the contract as a real cash flow in exchange for a statutory 100 %
*Beitragsgarantie*; **Schicht 3** buys the light *Ertragsanteil* taxation of a private
annuity and imposes nothing. So [basisrente](products/basisrente/index.md) and
[riester_rente](products/riester_rente/index.md) take a slot each, and four more go to the
Schicht-3 savings forms — the historic
[Kapitallebensversicherung](products/kapitallebensversicherung/index.md), the
[klassische Rentenversicherung](products/klassische_rentenversicherung/index.md) that
replaced it, the [fondsgebundene Rentenversicherung](products/fondsgebundene_rentenversicherung/index.md)
that dominates new business, and the [Indexpolice](products/indexpolice/index.md), a
German construction with no counterpart in the sister libraries. A seventh goes to the
[Sofortrente](products/sofortrente/index.md) they pay out into.

The last three are **Biometrie**, and one of them is the reason a German library looks
different from a French or a British one. The
[Berufsunfähigkeitsversicherung](products/berufsunfaehigkeit/index.md) is the country's
flagship protection product, written against a statutory definition of disability in
§ 172 VVG, and it outsells plain
[Risikolebensversicherung](products/risikolebensversicherung/index.md) in adviser
attention by a wide margin. [Pflegerentenversicherung](products/pflegerentenversicherung/index.md)
completes the set, sitting on top of the *soziale Pflegeversicherung* rather than replacing
it. **Betriebliche Altersversorgung** — *Direktversicherung*, *Pensionskasse*,
*Pensionsfonds*, *Unterstützungskasse* and *Direktzusage* — is out of scope, as is
*Gruppenversicherung*, the substitutive **private Krankenversicherung**, and
*Sterbegeldversicherung*.

The models are the centre of the library. Each is a by-model-point projection of one
product's gross liability cash flows: *Beiträge*, *Leistungen*, *Rückkaufswerte*, charges
and expenses, on the product's own processing order and timing. None of them discounts —
every model publishes the cash flows and leaves discounting, the *Deckungsrückstellung* and
capital to a layer that consumes them.

**Each one of these models reproduces a documented worked example, asserted cell by cell to
the precision the notes display**. The chain is deliberate and complete in both directions:

- `product-spec.md` specifies a *representative* product — a standardized composite built
  from publicly documented real products, not any single insurer's contract. It records
  contractual mechanics, a full parameter set, the observed variation across insurers, and
  the rationale for every representative choice.
- `technical-notes.md` turns that product into a liability cash flow model on paper: model
  point attributes, state variables, assumption inputs, the recursions with their explicit
  processing order, policyholder behaviour, and a numeric worked example.
- The **model** implements those notes, and the library's own `tests/` assert the worked
  example against it. Change an assumption, and the test tells you whether the model and
  the notes have parted company.
- `sources.md` lists every source the first two cite, with URLs where they are known,
  access dates and retrieval status.

Every quantitative parameter in the library is either **source-tagged** or marked
**[std]** — a standardization introduced for the reference implementation, carrying its
rationale and, where available, the observed range across insurers. Facts taken from source
material are never silently mixed with assumptions made to complete a model.

(delib-provenance)=

```{admonition} How much of this library has been checked against the documents it cites
:class: important

**delib was drafted blind and has since been re-verified.** The two conditions are worth
keeping apart, because a reader's confidence in any one claim depends on which applies to it.

**Drafted blind.** The build environment blocked direct HTTP egress to every host outside a
package-registry allowlist — `gesetze-im-internet.de`, `bafin.de`, `aktuar.de`, `gdv.de`,
`destatis.de`, `dejure.org` and `eur-lex.europa.eu` were each tried and each refused at the
gateway — and the session's web-search budget ran out partway through the regulatory
research. The first draft therefore rested on the authoring model's own knowledge of German
insurance law and practice, disciplined by **[std]** and **[unverified]** tags.

**Then re-verified.** The policy was lifted and every citation re-checked against the
document it names. All fifteen German instruments the library cites were read as canonical
XML from gesetze-im-internet, each with its amendment status (*Stand*) recorded, and
**950 statutory section references were checked: 950 were correct**. Insurer *AVB*,
*Verbraucherinformationen* and *Produktinformationsblätter* were retrieved as PDFs and read.

**Where that leaves each claim.** Of 969 source entries, **613 now read `Retrieved: yes`**,
37 were reached in part, and 319 could not be opened — 404 at the cited address, a consent
or JavaScript wall, a paywall, a subscription login, or an address that was never
established. So **two entries in three rest on a document someone opened**; the rest remain
**pointers rather than certificates**, and say so individually.

Read a claim against its own entry. Coverage is uneven by design of the sources rather than
of the library: the statutory core is near-complete, and the products whose primary sources
are carrier wordings behind a document portal are thinnest.

**The re-verification changed things**, which is the strongest argument for reading the
entries. It corrected sourcing, figures and attributions across every product — in one case
retiring a sentence the drafted text had leaned on that does not exist in the document it
was attributed to. Each product's `sources.md` records what changed.
```

```{admonition} These are mechanics demonstrations, not pricing or reserving results
:class: warning

**Every biometric basis shipped here is a [std] proxy.** The tables a German insurer
actually prices and reserves on — **DAV 2008 T** for death cover, **DAV 2004 R** and its
*Bestand* variants for annuities, **DAV 1997 I** and **DAV 1997 TI** for *Berufsunfähigkeit*,
**DAV 2008 P** for *Pflege* — are the property of the Deutsche Aktuarvereinigung, are not
published openly, and are **cited by name throughout this library and never redistributed**.
Nor is there a public rate card: German pricing is quote-driven, and what a *Produktinformationsblatt*
must disclose is the contract's own figures rather than a tariff. Replace both with company
data before drawing any conclusion from the numbers.
```

## The models

Model names are `<product>_<country>_<grid>`: the short form the German market itself uses
where there is one — `KLV`, `RLV`, `BU` — a short descriptor where there is none, then
`DE`, then `_A` for an annual step or `_S` for a monthly one. The grid letters follow
lifelib, where `annuallife/TradLife_A` is the annual-step model and `basiclife/BasicTerm_S`
and `savings/CashValue_SE` are the monthly ones. **All ten models here are `_S`: every model
in this library steps monthly**, which is why the `Grid` column below reads `monthly` on every
row. `S` carries a second sense in lifelib — scalar, one model point at a time, as against the
vectorized `_M` models — and that is true of all ten here as well.

**Kapitalbildende Lebensversicherung und private Rentenversicherung (Schicht 3)**

| Product | Model | Grid | Representative design |
|---|---|---|---|
| [Kapitallebensversicherung](products/kapitallebensversicherung/index.md) | `KLV_DE_S` | monthly | The library's *Überschussbeteiligung* chassis, and the place the German crediting arithmetic is settled: the declared *laufende Verzinsung* **contains** the *Rechnungszins*, so the interest surplus is `max(0, decl_rate − rechnungszins)` — 1,70 pp on a 2,70 % declaration against a 1,00 % guarantee, never 2,70 pp on top of 1,00 — and it is struck on the closing *Deckungskapital*, not on the sum insured and not on the premium. Three reserve constructions travel together and the customer gets the third: the *gezillmerte Deckungskapital*, the § 169 Abs. 3 VVG floor that spreads acquisition cost evenly over the first five contract years, and their maximum. On a long *gezillmert* contract the floor normally binds — 691,06 € at duration 12 on the anchor cell, which a model publishing the Zillmer reserve alone as the surrender value would take from the policyholder. All three *Überschussverwendung* systems ship, and the *Bonussystem*'s higher death benefit against the *verzinsliche Ansammlung*'s higher maturity is arithmetic rather than coincidence. The grid is monthly and the *Überschussbeteiligung* is not: the declaration, the three reserves, the § 169 value, the paid-up purchase and the *Stornoabzug* band all take a policy year and are bit-identical to the annual-step model's, while the months decide **which** of those annual values a claim is paid — and a *gezillmert* contract surrendered inside its first policy year is now paid a guaranteed nil rather than the value the coming anniversary would close at, which is 992,00 € off the projected surrender outgo |
| [Klassische Rentenversicherung](products/klassische_rentenversicherung/index.md) | `RV_DE_S` | monthly | The same chassis with a conversion where the endowment has a maturity, projected to attained age 120 rather than stopped at *Rentenbeginn*. Two accounts, not one balance split in two: the *Deckungskapital* credited at the contract's **own** guarantee vintage and the *Ansammlungsguthaben* at the declared rate, so one run carries 1,00 %, 2,75 % and 0,90 % cohorts at once — and forcing them onto a single rate misallocates between the two accounts while barely moving the total, which is why that error survives a reasonableness check on the headline. Three things happen at the *Rentenbeginn* instant: the *Bewertungsreserven* crystallise, the capital converts at `max(garantierter, aktueller) Rentenfaktor` — applying the guaranteed factor alone understates the anchor's annuity by 12,5 % — and the *Rentengarantiezeit* begins paying on the **annuitised** count rather than on survivors. The grid is monthly and the deferment is not: the premium, both accounts, the § 169 Abs. 3 floor and the surrender value all take a policy year and are bit-identical to the annual-step model's, because § 12 Abs. 1 VVG makes the *Versicherungsperiode* the year and § 169 Abs. 3 pays a mid-period exit the value struck at its end. What the finer grid buys is the *Rente* itself — a *Rentenfaktor* is quoted in euro a **month**, and the annual model paid twelve instalments at the start of each payout year, a compression worth 369,14 € of the anchor's payout phase, all of it outside the *Rentengarantiezeit* where the count is fixed and the two grids agree to the cent |
| [Fondsgebundene Rentenversicherung](products/fondsgebundene_rentenversicherung/index.md) | `FRV_DE_S` | monthly | The insurer guarantees the **number** of *Anteileinheiten* and not their value, so there is no *Rechnungszins*, no *Deckungskapital*, and — the *Anlagestock* being a segregated § 125 VAG asset pool held in the very units the liability is denominated in — no investment-mismatch term anywhere in the model. `net_cf` is the non-unit stream alone; booking the whole *Fondsguthaben* as insurer outgo is the first-order failure mode, and the scale of it on the anchor is 64 869,36 € of benefits against 4,39 € that is actually an insurer cost. The acquisition charge is the 25 ‰ *Höchstzillmersatz* spread over sixty monthly instalments, and the cliff at month 61 where the *Anlagebeitrag* steps from 162,00 € to 192,00 € is why this model is monthly — an annual grid cannot place month 60. Two mortality bases sit in one contract and **no cells reads both files**: DAV 2008 T behind the *Risikobeitrag* on the *Beitragsrückgewähr* amount at risk, DAV 2004 R behind the guaranteed *Rentenfaktor* |
| [Indexpolice](products/indexpolice/index.md) | `Index_DE_S` | monthly | A conventional profit-participating contract with the capital in the *Sicherungsvermögen* and **no unit account, unit price or fund value anywhere**: the index participation is a form of *Überschussverwendung* under § 153 VVG with no independent statutory footing, and the declared *Überschussanteilsatz* **is** the option budget — spent on the option package or credited as interest, and allocated exactly once, which is what `check_surplus_alloc()` says. The payoff is a sum of monthly returns each capped and none floored, floored once at the year: the shipped path reproduces the *Indexjahr* in which the index rose 6,4402 % and the credit was nothing, and four plausible-looking misreadings — flooring each month, compounding the capped returns, flooring the compounded raw return, applying the *Partizipationsquote* to it — each print a different wrong number. The *Höchststandsicherung* ratchets the **ledger of credits**, not the balance, which falls in a year that credits nothing wherever the reserve charge sits at or above the guaranteed rate. The grid is monthly and the *Indexjahr* is not: the cap, the sum, the credit, the ledger and the balance all take a policy year and are bit-identical to the annual-step model's, while the twelve capped monthly returns the *Indexjahr* is made of are now cells of the frame rather than a loop inside one — `index_return_capped_mth(t)` over a policy year sums to that year's `index_sum(k)` — and the months decide which exits are deaths and which surrenders, moving 35,69 € off the anchor's death outgo and 30,42 € onto its surrender outgo, the two unequal because a death is paid the 32 400,00 € *Mindesttodesfallschutz* floor and a surrender the much smaller *Rückkaufswert* |

**Geförderte Altersvorsorge (Schicht 1 und Schicht 2)**

| Product | Model | Grid | Representative design |
|---|---|---|---|
| [Basisrente](products/basisrente/index.md) | `Basis_DE_S` | monthly | Schicht 1 is a list of prohibitions — *nicht vererblich*, *nicht übertragbar*, *nicht beleihbar*, *nicht veräußerbar*, *nicht kapitalisierbar* — and the model is one too: no `cv_pp`, no `claims_lapse`, no *Kapitalwahlrecht*, no surrender decrement at any duration, and § 169 VVG with its *Stornoabzug* simply inoperative. The absences **are** the product, so the test module asserts the name list, a missing cells having no formula to check. The only behavioural exit is § 165 VVG, which removes the *premium* and not the *policy*, so two ledgers run side by side carrying different account values and `pols_if` decrements on mortality alone: by the twenty-third policy year the in-force count has fallen only to 0,932780 while the premium-paying count is 0,512516, and the difference is a cohort still in force, still credited and still converting. Everything paid to a survivor must be paid as an annuity, so the death benefit is the reserve leaving as the single premium of an immediate annuity this model does not project, and the cover is priced through a reduction in the *Rentenfaktor* rather than by scaling the benefit. The grid is monthly and the contract is not: the contribution, the four charges, the declared rate, both account blocks and the § 165 freeze all take a *Versicherungsjahr* and are bit-identical to the annual-step model's, while the *Rente* is what the finer grid buys — a *Rentenfaktor* is quoted in euro a **month**, and where the annual model booked twelve instalments on each payout year's opening count, and named that as its own pitfall, the instalment is now paid to whoever is alive at the start of each month, which is 4 290,52 € — 1,6 % — off the anchor's annuity outgo, and a *Rentengarantiezeit* is `12m` instalments beginning in the month after the death that starts them |
| [Riester-Rente](products/riester_rente/index.md) | `Riester_DE_S` | monthly | The *Zulage* is a **contribution, not a rebate**: the ZfA pays it to the provider, it is credited, counted in the guarantee, invested and taxed at the end like any other *Beitrag*, and on one shipped cell the state pays 76 % of the whole contribution — so it is a published positive income column beside `premiums` and is never folded into it. **Two different lags apply and one offset used twice reproduces neither**: § 86 strikes the *Mindesteigenbeitrag* on the previous *calendar* year's earnings while the cash arrives one *projection* year late, which is why the anchor's Zulage falls between the third and fourth projection years while its premium rises — a Zulage that stops is a contribution the saver must make good. The statutory 100 % *Beitragserhaltungszusage* accumulates contributions **without interest** and is tested exactly once, at *Rentenbeginn*: on the `low` declared-rate cell the account reaches 20 481,72 € against a 21 000,00 € guarantee, and that 518,28 € *Garantielücke*, funded from the insurer's own resources, is the product's signature output — a Riester model on which it is never positive has demonstrated nothing. The grid is monthly and the subsidy is not: the *Eigenbeitrag*, the Zulage and its ZfA lag, the two charges, both balances, the guarantee accumulator and the conversion all take a *Versicherungsjahr* and are bit-identical to the annual-step model's, the *Garantielücke* and the *Kleinbetragsrente* verdict included, while the *Leibrente* the AltZertG requires is now paid one instalment a month — 361,74 € off the anchor's payout phase — and the three accumulation exits compete month by month instead of running in sequence at a year end, moving 5,62 € of death outgo and 2,64 € of surrender outgo onto 8,30 € of transfers |

**Biometrie und Rentenbezug**

| Product | Model | Grid | Representative design |
|---|---|---|---|
| [Sofortrente](products/sofortrente/index.md) | `Sofort_DE_S` | monthly | The payout chassis, and the one model in the library with **no behaviour at all**: § 168 Abs. 3 VVG displaces the right of termination once the *Rentenbezug* has begun, so there is no `lapse_rate`, no *Rückkaufswert*, no *Stornoabzug* and no paid-up state at any duration, and the answer rests more purely on the mortality basis than anywhere else in delib. The *Rentengarantiezeit* is a `max` and not a sum, and both errors it closes off are large and opposite: decrementing the guaranteed instalments for survival pays 7,13 % too little, adding the certain floor pays 92,87 % too much, because `γ + l_a` pays `1 + l_a` for the whole window. The *Kapitalrückgewähr* makes the pricing equation implicit in the annuity and is **solved**, not evaluated — striking the plain annuity and subtracting a refund cost gives 318,7362 € against the correct 298,8348 €, which is not a rounding. The surface is generational and read at (attained age, birth cohort), never at (age, projection year): a period proxy overstates the annuity a given *Einmalbeitrag* buys by 5,1 % |
| [Risikolebensversicherung](products/risikolebensversicherung/index.md) | `RLV_DE_S` | monthly | The protection chassis, and where the *Bruttobeitrag* / *Zahlbeitrag* pair is **derived rather than assumed**: the guaranteed gross premium is struck once by first-order equivalence on tariff survivorship, and the billed premium follows from the surplus mechanic — the MindZV's 90 % minimum allocation of the *Risikoergebnis*, times the tariff's own mortality margin — reaching a ratio of 0,574725 out of the arithmetic. Setting `decl_scale` to zero raises the bill by 74,0 % with no change to any benefit, decrement or guaranteed term, and so with no § 163 procedure, no *Treuhänder* and no remedy: the largest policyholder risk in the product, and a one-Reference change. There is no cash value at any duration — § 169 Abs. 1 VVG reaches only a contract whose insured event is certain to occur — and yet a *Deckungskapital* builds to 7 553,29 € at duration 16 and runs off to exactly zero, so "no *Sparanteil*, therefore no reserve" fails the Thiele check. The § 161 three-year suicide window is a benefit switch on death claims only, applied tranche by tranche, so each *Nachversicherungsgarantie* increment carries its own clock. The grid is monthly and the product is not: every one of those constructions stays on the anniversary and the first-order equivalence is bit-identical to the annual-step model's, while the finer grid puts a claim in the month it happens and collects a modal *Zahlbeitrag* in instalments, which is § 168 VVG's *Versicherungsperiode* modelled rather than approximated |
| [Berufsunfähigkeitsversicherung](products/berufsunfaehigkeit/index.md) | `BU_DE_S` | monthly | A multi-state model with a **return arc**, not a decrement model: *aktiv*, *leistungspflichtig*, and a three-month run-off ledger that is § 174 VVG in arithmetic — where the insurer establishes that its liability has ceased it must still pay to the end of the third month after the notice reaches the policyholder, so a recovery does not stop the annuity in the month it happens, and the tail is 1,6 % of all benefit on the anchor cell. Death and lapse are the only exits; inception, recovery and reactivation are **internal transfers**, and putting them into the in-force recursion is how a multi-state model loses mass invisibly. The *Beitragsbefreiung* is not a benefit but the absence of a premium, and it falls out only if the premium is weighted by `pols_prem` rather than `pols_if` — the classic German BU implementation error, which leaves every total looking plausible, and the reason `check_net_cf()` rebuilds the premium leg from the *Zahlbeitrag* actually billed. Two escalations run on two clocks: the *Beitragsdynamik* on the policy anniversary, the *Leistungsdynamik* on the anniversary of each onset |
| [Pflegerentenversicherung](products/pflegerentenversicherung/index.md) | `Pflege_DE_S` | monthly | Nine states and only two absorbing: five *Pflegegrade* with deterioration and *Herabstufung* between them, a *Karenz* ledger per onset, and the trigger being the statutory *Pflegegrad* of §§ 14, 15 SGB XI rather than a definition the insurer writes. Every grade transition is internal to `pols_if`, and the monthly step holds the forces constant so the competing exits share one survival probability in proportion to them — `p_stay + Σ p_j = 1` exactly, which is what makes the state identity an identity rather than an approximation. Grade and mortality are correlated and the loading is stated on the **force** of active mortality, 1,5 at *Pflegegrad* 1 rising to 9,0 at grade 5, so the highest-paying state is the shortest-lived and pricing this annuity on DAV 2004 R would be prudent in exactly the wrong direction; the benefit is a grade-by-grade sum, and applying the entry-mix mean to the aggregate care population understates the whole benefit by 30 %. The *Wartezeit* runs from inception and gates the incidence force, the *Karenzzeit* runs from onset and needs its own ledger dimension — routinely conflated, and implemented in two different places |

(delib-one-shape)=

### One shape, enforced

Every model has the same two Spaces — `Data` reads the input CSVs once per model, and
`Projection` is parameterized by `point_id` — with inputs as **external** CSVs beside
`run.py`, so the model folder holds formulas and nothing else. `Projection`'s docstring
carries the mapping from the technical notes' actuarial symbols to the cells names.

That shape is asserted rather than merely described: `tests/test_model_conventions_de.py`
applies it to every model in the registry, and each model additionally has its own test
module for its worked example and its product-specific invariants — the notes' "Known
modeling pitfalls" sections are written up there as tests.

The pairing of model name to folder is deliberately *not* derivable from the folder name —
`fondsgebundene_rentenversicherung` spelled out is unusable in a model name — so it is
registered once in `tests/de_registry.py`, and the conventions suite asserts that the
registry, the directory on disk and the model's own `_name` all agree, along with the
country and grid tags.

The registry is per library; the contract it enforces is the one [uslib is held
to](#uslib-one-shape), and cells names come from lifelib — `basiclife/BasicTerm_S` first,
then `savings/CashValue_SE` — so a name means the same thing here, in uslib, in uklib, in
frlib and in lifelib. The [shared vocabulary table](#uslib-shared-vocabulary) is the settled
ruling across the libraries, and the time index is the same in all of them. The time index
`t` is 0-based: `t = 0` is the first period of a policy projected from issue (the issue year
on an annual grid, the issue month on a monthly one), period `t` runs from time `t` to time
`t + 1`, and the attained age is `age_at_entry + t` on an annual grid
(`age_at_entry + duration(t)`, `duration(t) = t // 12`, on a monthly one) — and here `t` is
always a **month**. **`proj_len()` is the number of periods from `t = 0`**, i.e. the exclusive
end of the frame: `result_cf()` covers `t = t_first, ..., proj_len() - 1`, where `t_first` is
0 for a point projected from issue and the elapsed periods for an in-force point. This is
lifelib's own convention (`basiclife/BasicTerm_S`, `savings/CashValue_SE`:
`for t in range(proj_len())`). A
contractual policy year is the 1-based label `t + 1` (`duration(t) + 1` on a monthly grid)
and is derived, never indexed by.

(delib-monthly-grid)=

### Every model steps monthly; no product is thereby a monthly product

The grid is the model's, not the product's. A mechanic the contract states in years stays
annual and is placed in the month the contract places it, which is why five of these models —
`KLV_DE_S`, `RV_DE_S`, `Index_DE_S`, `Basis_DE_S` and `Riester_DE_S` — run on **two clocks**
and say so in their `Projection` docstring: an annual coordinate — `k`, the policy or
projection year — for anything struck per *Versicherungsjahr*, and `t`, the month, for
anything that happens on a date. A cells' argument is the statement of which clock it is on,
and the bridge between them is one cells — `policy_year(t)`, `proj_year(t)`. The *Beitrag* of
a contract written annually is one instalment in month 0 of each policy year rather than a
twelfth every month, because § 12 Abs. 1 VVG makes the *Versicherungsperiode* the year and
the *Beitrag* is payable in advance for it; the declared *laufende Verzinsung* is credited
once a policy year; `Index_DE_S`'s *Wahlrecht* is exercised once, at an anniversary; a
§ 169 Abs. 3 VVG surrender value is struck *zum Schluss der laufenden Versicherungsperiode*
and not at the cancellation date; a § 165 VVG *Beitragsfreistellung* takes effect "für den
Schluss der laufenden Versicherungsperiode" and so falls at an anniversary; and
`Riester_DE_S`'s *Zulage* still reaches the account in the year after the contribution year
it is claimed for.

What the finer grid changes is **when** things happen inside the year. Every annual decrement
is applied twelve times at the **geometric** twelfth `1 − (1 − r)^(1/12)` and never at
`r / 12`, so twelve months compound back to the year's rate exactly and the in force at every
anniversary is the annual-step model's own figure to the last bit; a rate that is a certainty
rather than a probability — the terminal `q = 1` that closes a mortality table — is not
twelfth-rooted but placed whole in the anniversary month. That exactness is what makes the
figures that *do* move readable as product effects rather than discretisation noise: a *Rente*
quoted in euro a month is now paid monthly in advance (`RV_DE_S` −369,14 €, `Basis_DE_S`
−4 290,52 €, `Riester_DE_S` −361,74 €); deaths and surrenders compete month by month, so a
year's total exits are unchanged and their split is not; a policy leaving mid-year bears
administration only for the months it was there; a *Rentengarantiezeit* is a count of monthly
instalments; and the twelve capped monthly observations of `Index_DE_S`'s *Indexjahr* —
always the mechanic the product is named for, but buried inside one cells — are rows on the
frame, where *capped above and not floored below* can be read month by month.

Six models — the five above and `RLV_DE_S` — publish `result_cf_annual()`, which **regroups
the same months** into policy or projection years and is never a second projection, so an
annual comparison is a sum of the frame that was actually run. The balances that an annual
`result_cf()` used to carry — account values, credited interest, in-force counts — live in an
annual **state** frame instead (`result_pols()`, `result_acct()`, `result_index()`,
`result_surplus()`), so a balance cannot be summed down a cash flow statement.

(delib-own-rulings)=

### The two rulings this library added

Each library in this repository settles a convention of its own and asserts it rather than
describing it. delib settled two, and both are enforced by the conventions suite.

**`check_net_cf()` is required of every model.** A cash flow model's headline number is
`net_cf`, and until now it was the one quantity nothing checked: the roll-forward identities
the models publish check policy counts and account values, and the statement that reconciles
them into `net_cf` lived in prose. Every delib model publishes `check_net_cf()`, a bool over
all `t` that reconstructs `net_cf(t)` from the statement's own published parts, with the
per-period residual at `check_net_cf_resid(t)`. The *identity* is a product fact — a term
cover reconciles premiums less claims less expenses, a unit-linked contract has to cross the
unit / non-unit boundary to do it, and a payout annuity has no premium term at all — so each
`model.md` states its own in one line and the conventions suite asserts only that the cells
exists, has the `CashValue_SE` signature, and returns `True` on every model point. frlib
carried the name on five of its nine models; here it is the contract.

**Every assumption CSV carries a `provenance` column.** The hard rule of all five libraries
is that every quantitative parameter is either source-tagged or marked **[std]**. In the
prose that rule is enforced by review; in the shipped input files it was enforced by habit,
and habit is what a table added in a hurry escapes. Here it is a property of the library:
each row of each input CSV carries its own tag — `[S3]`, `[REG-R21]`, `[std]` with a short
rationale — and a file without a populated `provenance` column fails the suite.
`model_point_table.csv` is the single exemption, because a model point is a *configuration*
rather than an assumption: its columns are one policy's own terms, and tagging them row by
row would repeat the same fact once per policy while saying nothing about any assumption.

Given the retrieval conditions above, the second ruling earns its keep twice over. When a
citation is a pointer rather than a certificate, the least a library can do is put the
pointer next to the number.

(delib-germany-specific)=

### What is German about these models

Five things recur across the set and are worth knowing before reading any one of them.

**Every biometric basis shipped here is a [std] proxy.** German insurers price and reserve on
the tables of the **Deutsche Aktuarvereinigung** — DAV 2008 T for death cover, DAV 2004 R and
its *Bestand* variants for annuities, DAV 1997 I / RI / TI for *Berufsunfähigkeit*, DAV 2008 P
for *Pflege* — and those tables are the DAV's property, are not published openly, and are
**cited by name throughout this library and never redistributed** [REG-R47] [REG-R48]
[REG-R49] [REG-R50] [REG-R51]. What ships beside each model is a construction, anchored so
that the model's own worked example reproduces exactly, with the anchor named in the `Data`
docstring: `mort_rate_1st(M, 37) = 0.001200` on `KLV_DE_S`, `q_base(M, 50) = 0.002000` on
`RV_DE_S`, `qx_tariff(37) = 0.00080` on `FRV_DE_S`, `qx(67) = 0.014000` on `Basis_DE_S`,
`ann_factor() = 20.87222879` on `Riester_DE_S`, `inc_rate(30) = 0.001100` on `BU_DE_S`. Each
`model.md` also states what a replacement must **preserve** rather than what it must equal —
that DAV 2004 R's surface is *generational*, so it is read at attained age and birth cohort
and a period proxy overstates `Sofort_DE_S`'s annuity by 5,1 %; that disabled-lives mortality
must exceed active-lives mortality state by state and never be one rate for both; that a
*Pflegetafel* must carry incidence by grade of entry, deterioration dominating recovery above
75, and transition probabilities that sum with the stay probability to one. **This is the
single largest gap between these models and a production one**, and it is why every
`model.md` opens by saying the model is a mechanics demonstration rather than a pricing or
reserving result.

**The declared rate contains the guarantee, and the surplus it credits is a constrained
allocation rather than an assumption.** The German *laufende Verzinsung* **is** the
*Garantieverzinsung* plus the *laufende Zinsüberschussbeteiligung* [REG-R53], so the interest
surplus is a subtraction — `max(0, decl_rate(t) − rechnungszins())` — and never a rate paid on
top of a rate. A model that credits 1,00 % and then a further 2,55 % puts 56,82 € into
`RV_DE_S`'s first year instead of 40,82 € and reaches 63 768,69 € at *Rentenbeginn* against the
correct 58 788,98 €, with the whole error sitting in one of the two accounts. The rate itself
is an **output of a constrained allocation**: § 153 VVG makes participation an entitlement and
the MindZV puts an arithmetic floor under it — at least 90 % of the investment result, 90 % of
the *Risikoergebnis* and 50 % of the *übriges Ergebnis* [REG-R18] [REG-R24] — with § 139 VAG's
*Sicherungsbedarf* test cutting back the *Bewertungsreserven* share [REG-R9]. `KLV_DE_S`
carries the machinery and `RV_DE_S`, `Index_DE_S`, `Basis_DE_S` and `Riester_DE_S` consume a
declared rate from it, `Index_DE_S` spending it as an option budget instead of crediting it.
The guarantee inside that rate is a **cohort fact fixed at conclusion**: an existing contract
keeps the *Höchstrechnungszins* in force when it was written [REG-R14] [REG-R15], the rate
stepped from **0,25 % to 1,00 % on 1 January 2025** — the first increase since 1994 — and a
German book is therefore a layered stack of vintages rather than one rate. Four models carry
the vintage on the model point (`RV_DE_S` runs 1,00 %, 2,75 % and 0,90 % cells in one run;
`Basis_DE_S` runs four vintages; `Index_DE_S` reaches back to 0,25 %; `KLV_DE_S` ships both
DeckRV ceilings in a cohort-keyed table and asserts them), and `Sofort_DE_S` prices each
*Einmalbeitrag* against the cap of its own vintage as an **inequality**, because a carrier may
price below it and one in the corpus is observed doing so.

**The *Bruttobeitrag* and the *Zahlbeitrag* are two different numbers, and only the first is
guaranteed.** This is the German protection signature and it has no counterpart in the sister
libraries: the contract guarantees a gross premium as the maximum the policyholder can ever be
required to pay, and bills a lower net one obtained by crediting anticipated surplus in advance
[REG-R24] [REG-R27]. `RLV_DE_S` **derives** the split from the mechanic rather than assuming it
— the *Sicherheitszuschlag*'s actuarial value at issue, times the MindZV's 90 % minimum
allocation, times the risk share of the gross premium, giving 0,574725 — and publishes
`prem_gross`, `premiums` and `prem_rebate` as three separate columns so the gap is visible in
the frame. `BU_DE_S` publishes the same pair as `premiums` and `surplus_credit`, holding the
ratio at 0,70 and calling that its largest discretionary assumption. The consequence is a real
policyholder exposure and both models make it a one-parameter stress: withdrawing the credit
entirely raises `RLV_DE_S`'s bill by 74,0 % and `BU_DE_S`'s by 42,86 %, with **no change to any
benefit, decrement or guaranteed term**, and therefore no § 163 VVG procedure, no *Treuhänder*
and no remedy. A model carrying one premium column cannot represent the product, and a model
carrying only the billed one has silently assumed the credit is permanent.

**The tax layer is model structure, not a parameter.** Which of the *Drei Schichten* a contract
sits in decides what the model may contain, and delib implements the constraints as absences
and mechanics rather than as flags. In **Schicht 1** the five prohibitions of § 10 Abs. 1
Nr. 2 Buchst. b EStG [REG-R39] mean `Basis_DE_S` has no surrender value at any duration, no
lapse decrement, no `cv_pp`, no *Kapitalwahlrecht* and no lump sum to anyone at any date, and
that everything paid to a survivor is paid as an **annuity** — so a death benefit there is the
released reserve leaving as the single premium of a new contract rather than a payment to a
beneficiary. In **Schicht 2** the AltZertG's 100 % *Beitragserhaltungszusage* is a nominal
accumulator tested once at *Rentenbeginn* [REG-R43], the *Zulage* is a real cash flow paid by
the ZfA to the provider on a statutory lag [REG-R42], the acquisition charge must be spread over
at least five years — tighter than anything the VVG imposes on a Schicht-3 contract — and the
30 % *Teilkapitalauszahlung* cap and the *Kleinbetragsrenten-Abfindung* are computed rather
than assumed. **Schicht 3** imposes none of that and instead leaves a behavioural fingerprint:
the twelve-year and age-62 conditions of § 20 Abs. 1 Nr. 6 EStG [REG-R45] put a step in four
models' surrender tables at the duration the threshold is crossed, and `FRV_DE_S` keys it on
age as well as duration because keying it on duration alone fires fourteen years early on its
anchor cell.

**Scope limits are stated rather than faked.** Where a mechanic could not be established, or a
deterministic run cannot reach it, the models say so instead of shipping a number. `Index_DE_S`
carries **no** optimal-election rule, inertia model or within-year switching for the annual
*Wahlrecht*, because none is established for the product family and a switching rule would put
an unevidenced behavioural assumption at the centre of the result; its base run at `w = 1` is
declared a modelling choice made so the model demonstrates the index arm, with model point 11
shipped as the `RV_DE_S` comparison. `FRV_DE_S` implements none of the hybrid and guarantee
designs — *statisches* and *dynamisches Hybrid*, *Zwei-* and *Drei-Topf-Hybride*, i-CPPI,
*Wertsicherungsfonds* — because each is a reallocation rule along a path and a deterministic
projection has one smooth path, so the rule either never triggers or triggers on a hand-chosen
shock; what would have to be added is named instead. `BU_DE_S` ships the *AU-Klausel* switch
**on** at an uplift of exactly 1,00 on one model point, because no source quantifies what six
months of certified *Arbeitsunfähigkeit* adds to incidence and an inert switch is honest where
an invented loading is not. `RV_DE_S` records a payout-phase administration charge and never
applies it, the *Rentenfaktor* being exogenous and already carrying the tariff's payout
loading. And where a simplification runs one way, the direction is stated: `FRV_DE_S`'s omitted
surplus credit biases the projected *Fondsguthaben* **downward**, its unimplemented paid-up
cohort biases charge income **upward**, `Sofort_DE_S`'s independent joint lives **overstate**
the joint-life annuity, and `Pflege_DE_S`'s aggregate in-care mortality **understates** what a
*Karenzzeit* removes.

### Chassis relationships

Products that share machinery point at the file where it is specified rather than silently
restating it, and each pointer states what it inherits and where it deviates:

- **`KLV_DE_S` is the *Überschussbeteiligung* chassis.** The
  [Kapitallebensversicherung technical notes](products/kapitallebensversicherung/technical-notes.md)
  are the primary home of the declared-rate arithmetic, the four-component German surplus split,
  the three *Überschussverwendung* systems, the *Zillmerung* and the § 169 Abs. 3 VVG floor.
  `RV_DE_S` is the same *Deckungskapital* and surplus machinery with a conversion where the
  endowment has a maturity, and carries the split by pointer rather than by restatement — only
  the *Zinsüberschuss* was established for the annuity, and inventing the other three would be
  inventing three rates. `Basis_DE_S` and `Riester_DE_S` add a tax wrapper and, in the second
  case, a state *Zulage* to the same accumulation; `Index_DE_S` keeps the chassis and **spends**
  the declared surplus on an index participation instead of crediting it, so model point 11,
  electing the *sichere Verzinsung* arm at `w = 0`, is an `RV_DE_S` comparison run inside the
  index model. **`FRV_DE_S` deliberately does not sit on it**: a unit-linked *Rückkaufswert* is
  a *Zeitwert* of fund units and not a *Deckungskapital*, and the contract has no
  *Rechnungszins* to declare a rate above.
- **`RV_DE_S` is the accumulation-and-conversion chassis the two subsidised layers inherit.**
  `Basis_DE_S` states its deltas against it — the same deferred annuity with the Schicht-1
  prohibitions imposed on top — and `Riester_DE_S` points at it for the
  `dk_pp` / `surplus_acct_pp` recursion and for § 169 VVG, adding the Schicht-2 apparatus the
  classic contract has none of. Read in the other direction, `Basis_DE_S` and `Riester_DE_S`
  are the useful contrast with each other: a statutory *Beitragsgarantie*, a permitted 30 %
  *Teilkapitalauszahlung* and a *Kleinbetragsrenten* commutation on one, and none of the three
  on the other.
- **`RLV_DE_S` is the protection chassis**, and it reaches less far inside delib than a reader
  might expect, which is worth saying rather than leaving to be discovered. It shares the
  *Überschussbeteiligung* machinery with `KLV_DE_S` in a different *Überschussverwendung* form —
  surplus netted against the premium rather than credited to a reserve — and it is the file the
  *Bruttobeitrag* / *Zahlbeitrag* split is derived in. It does **not** extend to the two
  biometric models: `BU_DE_S` and `Pflege_DE_S` are monthly multi-state projections and share no
  recursion with it at all.
- **`BU_DE_S` and `Pflege_DE_S` share the monthly multi-state chassis**, and share
  it with frlib's [assurance dépendance](../frlib/products/dependance/index.md). `dis_cohorts`
  and `dep_cohorts`, `pols_dis_dur(t, z)` against `pols_pg(t, g)` against `pols_part` /
  `pols_tot`, and `pols_prem`, `check_states` and `check_pols_roll_fwd` mean the same thing on
  all three. That is the whole of the shared vocabulary, and the two names a reader might
  expect beside them are worth naming as **absent**. `cohort_len` truncates a claim-duration
  cohort vector and so exists only where there is one — `BU_DE_S` and `Dep_FR_S`;
  `Pflege_DE_S`'s ledger is graded rather than aged and carries no such name. And the
  return-to-active transition is named three ways because it is not one transition:
  `Dep_FR_S`'s `pols_recovery` returns a life to autonomy, `Pflege_DE_S`'s `pols_reactiv`
  returns a *Pflegegrad* 1 life to `pols_act` paying and exposed to lapse in the same month,
  while `BU_DE_S`'s `pols_recovery` returns no one — it ends the benefit into a three-month
  run-off out of which the life reappears as `pols_reactivation`. Each `model.md` tabulates
  the rest of where they part: the **ledger dimension** differs — a claim-duration cohort in
  BU, a *Pflegegrad* in the LTC annuity, a two-level French severity in `Dep_FR_S` — and only
  the German LTC model's is a benefit *schedule*. `BU_DE_S`'s `pols_runoff_slot` is the
  counterpart of `Dep_FR_S`'s `pols_red`: a small holding ledger a naive implementation omits,
  and a first-order error in both.
- **`FRV_DE_S` shares the unit-linked chassis with frlib's
  [unités de compte](../frlib/products/assurance_vie_uc/index.md) contract**, `UC_FR_S`, and the
  shared names mean the same thing on both: `av_pp` / `av_pp_at` for the fund at its named
  within-month timings, the unit count and its two movements, and the net amount at risk floored
  at zero — `nar_pp` here against the *garantie plancher* there — as the only part of a death
  benefit the insurer funds. Its `model.md` tabulates the correspondence in both directions,
  including the three German terms of art that keep their German form in the cells names because
  each names a quantity with a statutory definition: `beitragssumme()`, `stornoabzug()` and the
  three `rentenfaktor_*()`.
- **Across markets — the payout core.** `Sofort_DE_S` shares the payout-annuity core with
  [uslib's SPIA](../uslib/products/immediate_annuity/index.md),
  [uklib's pension annuity](../uklib/products/pension_annuity/index.md) and
  [frlib's rente viagère](../frlib/products/rente_viagere/index.md): `duration_mth`,
  `horizon_mths`, `is_payment_mth`, `certain_floor`, `payment_factor`, `lives_if`,
  `lives_death`, `annuity_pp`, `annuity_payments`, `check_lives_roll_fwd` and
  `check_payment_factor` mean the same thing on all four, and `result_pols()` is the same second
  frame. Two names the other three carry are **absent** here and the absence is argued rather
  than accidental: `payment_surv_mth` and `payment_factor_life` separate the survival index of a
  payment from the month it falls in, and in this model the payment instant is the start of
  month `t` under both timings, so the two indices coincide and a second cells would only
  restate `lives_if`. Inside delib, `Sofort_DE_S` is `RV_DE_S`'s payout phase as a product in
  its own right — which is why an immediate-annuity document is direct evidence for a deferred
  contract's conversion basis — it is the survivor's single premium `Basis_DE_S` books and does
  not project, and it is the contract `Riester_DE_S`'s second phase now runs on the same
  monthly grid as.
- **Across markets — the rest.** `KLV_DE_S` copies lifelib's `annuallife/TradLife_A`
  external-input layout, which the whole library then follows, and its nearest conceptual
  relative is frlib's [fonds en euros](../frlib/products/assurance_vie_euro/index.md), the same
  idea under a different statute — with the difference that a French *fonds euros* credits a
  rate to an account **balance** while a German endowment credits it to a **reserve**.
  `RLV_DE_S` and frlib's [temporaire décès](../frlib/products/temporaire_deces/index.md) are the
  same product in two markets, and three differences are named so a reader does not carry one
  across: the French *cotisation* is revisable at attained age and the German *Bruttobeitrag* is
  level; the French product accelerates the death capital on PTIA and the German one has no
  living benefit at all; and `expenses` includes commission there and excludes it here.
  `Index_DE_S`'s nearest relatives are uslib's `FIA_US_S` and `RILA_US_S`, which share the
  cap and participation-rate vocabulary and the annual reset but **not** the German financing
  identity: an FIA's index budget is the insurer's option budget on a fixed-annuity chassis,
  while here it is the declared *Überschuss* and is bounded below by the MindZV.

## How to use the library

Create your own copy of the *delib* library, as described in the
{ref}`create-a-project` section. For example, to copy it to *C:\\path\\to\\your\\delib*:

```python
>>> import lifelib

>>> lifelib.create("delib", r"C:\path\to\your\delib")
```

Each model reads from its own directory, so run one directly:

```bash
python products/klassische_rentenversicherung/run.py
```

or read it and take the cash flow statement:

```python
>>> import modelx as mx

>>> model = mx.read_model("products/klassische_rentenversicherung/RV_DE_S")

>>> model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is each model's worked-example anchor cell.
`result_cf()` returns a tidy `DataFrame` indexed by `t` — a projection **month**, in every
model — with one column per cash flow line. Where a model also publishes
`result_cf_annual()`, that is the same frame summed into policy or projection years, and its
annual **state** frame (`result_pols()`, `result_acct()`, `result_index()`,
`result_surplus()`, `result_fund()`, `result_states()`) is where the balances are.

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
  - One directory per product, holding its documents *and* its model together. Ten of them.
* - `products/<product>/product-spec.md`
  - The representative product specification: mechanics, parameters, variation across insurers.
* - `products/<product>/technical-notes.md`
  - The liability cash flow model on paper: state variables, recursions, processing order, worked example.
* - `products/<product>/model.md`
  - How the model implements those notes — what was standardized, what diverges, what the tests cover.
* - `products/<product>/sources.md`
  - Every source the product's documents cite, with URLs where known, access dates and retrieval status.
* - `products/<product>/<Model>/`
  - The modelx model itself. Formulas only — no embedded data.
* - `products/<product>/*.csv`
  - The model's inputs, external to the model folder so they can be edited or swapped in place. Every assumption file carries a `provenance` column.
* - `products/<product>/run.py`
  - Reads the model and prints its cash flow statement.
* - `references/`
  - The cross-product regulatory and actuarial bibliography, cited as `[REG-R#]`.
* - `tests/`
  - One module per model for its worked example and invariants, plus `test_model_conventions_de.py` for the house style, and `de_registry.py` carrying the model registry.
* - `_research/`
  - The raw research notes every citation traces back to. Provenance, not documentation — shipped but not rendered.
```

`_research/` carries one file per product plus `regulatory-actuarial.md`, and records what
each source is and what could be established about it. Its source lists are **never
renumbered**: the product documents cite against them.

(delib-citation-conventions)=

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
**specification** citation — the *Allgemeine Versicherungsbedingungen*,
*Produktinformationsblatt* or *Basisinformationsblatt* a number was taken from — which says
where a figure came from rather than what the model must obey. So one reads as a tag on the
page and the other as a link off it.

Numbering is per product — S1 is a different source in each — so tags resolve against the
document's own product rather than one global list.

| Tag | On the page | Meaning |
|---|---|---|
| `[S#]` | bracketed text | Fact taken from a primary product document (*Allgemeine Versicherungsbedingungen*, *Produktinformationsblatt*, *Basisinformationsblatt* (PRIIP-KID), *Verbraucherinformation*, *Tarifblatt*, *Musterrechnung*) listed in the product's `sources.md` |
| `[R#]` | link | Fact taken from a product-specific regulatory/actuarial reference in the product's `sources.md` |
| `[REG-R#]` | link | Fact taken from the cross-product reference library (frozen R-numbering) |

(delib-std)=

**[std]** — a *standardization introduced for the reference implementation*: a parameter or
convention chosen where sources vary, are proprietary, or are silent. Each carries a
rationale and, where available, the observed range across insurers.

(delib-unverified)=

**[unverified]** — a claim that **no retrieved document confirms**. Treat it as a to-verify
item, not an established fact. The tag was applied at drafting to every specific paragraph
number, effective date, monetary amount and market figure, because at that point nothing had
been read; the [re-verification](#delib-provenance) then discharged it wherever a document
was opened and supported the claim, so a tag that survives now means the document was
consulted and did not settle the point — or could not be opened at all.

The hard rule throughout: **every quantitative parameter is either source-tagged or marked
[std]**. In this library that rule does most of its work on the biometric bases, which are
**[std]** proxies throughout because the DAV tables are proprietary, and on the charge and
premium levels, because German pricing is quote-driven and no public rate card exists.

## Regulatory and actuarial reference library

The [reference library](references/regulatory-and-actuarial-references.md) is the curated
cross-product bibliography — frozen numbering **R1–R56**, cited as `[REG-R#]` — with a
product-relevance matrix. It spans the prudential frame in two layers, the European one
(Solvabilität II, the *Delegierte Verordnung* (EU) 2015/35, the 2025 review directive and the
EIOPA risk-free term structures) and the *Versicherungsaufsichtsgesetz* it reaches German life
business through (VAG 2016 and its Anlage 1, the §§ 74–110 balance sheet and SCR/MCR, the
§§ 124–125 *Anlagegrundsätze* with the *Sicherungsvermögen* and the *Anlagestock*, § 138 on
*Prämienkalkulation*, § 139 on the *Überschussbeteiligung* and the *Sicherungsbedarf* test,
the RfB provisions of §§ 140 and 145, the *Verantwortlicher Aktuar* and the 1994 deregulation,
Protektor and the supervisor's crisis powers, and the Solvency II transitionals); the reserving
regulation and its rates (DeckRV § 2 and the *Höchstrechnungszins*, the rate history and the
*Sechste Verordnung* of 19 July 2024, § 4's *Höchstzillmersätze*, and § 5 Abs. 3's *Referenzzins*,
*Zinszusatzreserve* and *Korridormethode*); the surplus regulations (the MindZV's 90/90/50
minima, the RfBV, the LVRG 2014, and BaFin's MaGo and *Auslegungsentscheidungen*); the contract
law of the VVG (the statute and § 171's *halbzwingende Vorschriften*, the two *Widerrufsrechte*,
§ 153 and the *hälftige Beteiligung an den Bewertungsreserven*, the *Modellrechnung* and
*Standmitteilung*, the *Selbsttötung* and beneficiary sections, § 163's *Prämien- und
Leistungsänderung*, §§ 165–170 on the paid-up right, the *Rückkaufswert* and the *Stornoabzug*,
and Kapitel 6's §§ 172–177 on *Berufsunfähigkeit*); conduct and disclosure (the VVG-InfoV and
*Effektivkosten*, PRIIPs, the IDD, *Test-Achats* with the AGG, and the 2023 *Wohlverhaltensaufsicht*
Merkblatt); the BGH line of authority and the GDV *Musterbedingungen*; the tax architecture of
the *Drei-Schichten-Modell* (the AltEinkG, the Basisrente deduction and its five prohibitions,
the ZPO *Pfändungsschutz* that shapes them, the *Ertragsanteil* and *Besteuerungsanteil*, the
Riester machinery of § 10a and §§ 79–99, the AltZertG with the BZSt and the
Produktinformationsstelle, the 2026 reform and the *Altersvorsorgedepot*, the 12/62 rule and the
*Mindesttodesfallschutz*, and the ErbStG with the SGB V contributions on an annuity in payment);
the biometric bases and market statistics (*Rechnungsgrundlagen erster und zweiter Ordnung* and
the DAV as owner of the tables, DAV 2008 T, DAV 2004 R and DAV 2004 R-Bestand, the DAV 1997
*Berufsunfähigkeit* family, DAV 2008 P with the § 15 SGB XI *Pflegegrad* break, Destatis, and
the market-in-numbers entry); and the accounting and professional standards (HGB §§ 341–341o
with the RechVersV and BerVersV, IFRS 17 and the Variable Fee Approach, and the DAV
*Fachgrundsätze* with the annual *Höchstrechnungszins* recommendation).

The product-relevance matrix runs the fifty-six entries against the ten products in three
states — load-bearing, qualified or background, and not relevant — so a reader can see at a
glance that R51 (DAV 2008 P and the *Pflegegrad* break) is load-bearing for one product and
background for three, while R34 (unisex) and R47 (the first- and second-order bases) are
load-bearing for all ten. One instrument is deliberately **absent** from the matrix and carries
no id: BaFin's *Kapitalanlagerundschreiben* and the *Anlageverordnung* it interprets bind small
insurers under §§ 212–217 VAG and domestic *Pensionskassen* and *Pensionsfonds*, not the
Solvency II life insurers that write these ten products, which are governed by the qualitative
§ 124 VAG prudent person principle — German market writing routinely cites AnlV quotas as
though they bound everyone, and the circular is discussed inside R7 so that no delib author
misapplies one. Read the page's own retrieval-conditions section first: it is stated in full at
the head, before the first entry, and **every one of the fifty-six entries records `Fetched:
no`**.

## Known gaps and caveats

Aggregated from the per-product research; each product's documents carry the full list, and
each `_research/<slug>.md` closes with its own numbered register.

- **The library was drafted blind, then re-verified; coverage of that re-verification is
  uneven.** Direct HTTP egress was blocked while delib was written — `gesetze-im-internet.de`,
  `bafin.de`, `aktuar.de`, `gdv.de`, `destatis.de`, `dejure.org`, `eur-lex.europa.eu` and
  `de.wikipedia.org` each refused with HTTP 403 at the gateway — and the 200-call `WebSearch`
  budget was spent on a prudential sweep and a contract-law sweep, leaving **the tax and
  biometric sweeps and eight of the ten product files with no research channel at all**. That
  first draft rested on the authoring model's own knowledge. The policy has since been lifted
  and the citations re-checked: **613 of 969 source entries now read `Retrieved: yes`**, 37 were
  reached in part, and **319 could not be opened** — 404 at the cited address, a consent or
  JavaScript wall, a paywall, a subscription login, or an address that was never established.
  The statutory core is near-complete; the thinnest products are those whose primary sources are
  carrier wordings behind a document portal, `fondsgebundene_rentenversicherung` most of all at
  25 of 51. **An entry that still reads `Retrieved: no` is a pointer, not a certificate.**
- **The re-verification corrected the drafted text, so the drafted text was wrong in places.**
  Sourcing, figures and attributions moved in every product. The sharpest case: the
  `klassische_rentenversicherung` corpus had leaned on CosmosDirekt LA 904 A citing *DAV 2004 R*
  at *0 percent p.a.*, and the retrieved document contains neither — it states *"der tarifliche
  Garantiesatz von 0,90 Prozent p. a."*, which is its 2017 vintage's cap. Both facts are now
  sourced to documents that carry them. Elsewhere: DAV 2008 T observes **2001–2004**, not
  2006–2008; the GDV *Stornoquote* is **2,56 % for 2023**; three `kapitallebensversicherung`
  sources cited as endowment wordings are annuity wordings. Each product's `sources.md` records
  its own corrections. **Findings that reach a modelled rate or rule were reported and not
  acted on** — a model change moves the worked example and its golden tests — and each product's
  `model.md` or `sources.md` names them.
- **The DAV tables are proprietary, so every biometric basis here is a [std] proxy.** DAV 2008 T,
  DAV 2004 R and DAV 2004 R-Bestand, DAV 1997 I / RI / TI and DAV 2008 P are the property of the
  Deutsche Aktuarvereinigung, are not public, and are cited by name and never redistributed
  [REG-R47] [REG-R48] [REG-R49] [REG-R50] [REG-R51]. Each shipped table is anchored so the
  model's worked example reproduces exactly and each `Data` docstring says what a replacement
  must preserve, which is the honest form of the claim — but no delib decrement rate is a market
  observation. Two further problems are specific rather than general: **no public German BU or
  *Pflege* decrement table exists in any form**, so `BU_DE_S`'s inception, reactivation and
  disabled-mortality bases and `Pflege_DE_S`'s whole transition matrix are constructions whose
  *shapes* are argued and whose *levels* are invented; and **DAV 2008 P was built on the
  superseded *Pflegestufen***, which the 2017 *Pflegegrad* reform replaced in a way that widened
  the insured population — the largest basis risk in that product, and one a licensed copy of the
  table would not by itself remove. Whether a successor to DAV 1997 I exists could not be
  established, and the DAV table *names* used in the BU file are themselves marked [unverified].
- **There is no public German rate card, and no price point of any kind, for any of the ten
  products.** frlib had one published attained-age grid that `TD_FR_S` reproduces exactly; delib
  has none. Every premium in this library is computed by the model's own equivalence principle on
  [std] bases and **no delib premium reproduces a published figure**. The single highest-value
  missing datum is named in the term-life register: one published *Bruttobeitrag* / *Zahlbeitrag*
  pair at a known age, sum insured and term would pin the *Sicherheitszuschlag* directly and
  re-derive the rest of the scale. The document class that would supply it — a
  *Produktinformationsblatt* — was not located for any product, in specimen or model form, and
  the one PRIIP *Basisinformationsblatt* anywhere in the corpus is for an endowment and its
  figures were not established.
- **Charge levels are [std] throughout, and on one product they are structurally undisclosed
  rather than merely unretrieved.** Not one *Effektivkosten* value, *Abschlusskostenquote*,
  *Verwaltungskostenquote* or commission rate was established for any carrier on any product; the
  only commission figure in the whole corpus is one carrier's 25 ‰, and BaFin's statement that
  *Effektivkosten* "differ considerably" and that it will examine outliers is qualitative. On
  term life the levels would have been missing even with full egress: there is no
  *Effektivkostenquote* because there is no yield, no *Basisinformationsblatt* because the product
  is not a PRIIP, and the *Produktinformationsblatt* quotes premiums rather than loadings. Every
  model therefore sits its acquisition charge **exactly at** the § 4 DeckRV *Höchstzillmersatz* of
  25 ‰ of the *Beitragssumme* [REG-R16], which demonstrates the binding constraint instead of
  inventing an interior point — and which may well be wrong for a slim direct-channel tariff, as
  the term-life register says in terms.
- **No *Rentenfaktor* level, range or time series exists anywhere in the corpus** — for any
  product, at any carrier, in any year. The rating house's own article titled with the question
  returned no level, and the *Rentenfaktor-Check* titled as data and analysis returned none. So
  every factor in the library is a construction with its derivation printed beside it: 32,00 € at
  age 67 on `RV_DE_S`, 25,00 € on `FRV_DE_S` derived as `10 000 / (12 · T_eff)` at a 0 %
  *Rechnungszins* rather than observed, 31,50 € on `Basis_DE_S`, 29,00 € guaranteed on
  `Riester_DE_S`, 25,00 € on `Index_DE_S`. **Both** branches of `max(garantierter, aktueller)`
  are exercised by a shipped model point on `RV_DE_S` and `Basis_DE_S` — the anchor cell
  converts at the current factor on each and model point 13 at the guarantee — and that is the
  point of choosing those two levels. On the other three the base run does not separate the
  branches: `Riester_DE_S`'s guaranteed 29,00 € wins on all
  thirteen points, and the current factor is lifted above it only by a test that substitutes a
  doubled annuitant mortality table; `FRV_DE_S` ships the two equal on twelve points and the
  current factor above the guarantee on point 13, so its guarantee never strictly binds; and
  `Index_DE_S`'s two factors are `Projection` References both fixed at 25,00 € rather than
  model-point columns, so neither branch is distinguished anywhere in the shipped run. None may
  be quoted as a market rate. `Index_DE_S` and `RV_DE_S` additionally record that their [std]
  *Rentenfaktor* and their [std] annuity table are **not calibrated to each other**, which is
  why the annuity there is reported and not computed.
- **No behavioural rate is sourced, on any product.** No German *Stornoquote* was established for
  any of the ten at any duration; the two GDV market-wide measures for 2024 — 2,72 % and 1,2 % —
  are irreconcilable from the search evidence, neither is product-specific or by duration, and
  `RLV_DE_S` deliberately declines to use either. Every lapse table ships with its **shape**
  argued from structure and its **levels** invented: the § 20 Abs. 1 Nr. 6 EStG twelve-year
  threshold puts a visible step at duration 12 on four models, `FRV_DE_S` keys the same step on
  age as well as duration because keying it on duration alone fires fourteen years early, and
  `BU_DE_S`'s unusually low level is a product fact rather than optimism, cover being
  unreplaceable once health has changed. Nor is any take-up rate established: no
  *Beitragsfreistellung* rate, no *Zuzahlung* utilisation, no *Kapitalwahlrecht* or
  *Teilkapitalauszahlung* take-up, no *Nachversicherungsgarantie* exercise pattern, and no
  election distribution for `Index_DE_S`'s annual *Wahlrecht* in either direction. Where a rate
  was needed the mechanic is carried as a **deterministic model-point election** instead, and each
  model says so.
- **Two products rest on no carrier document at all.** For the *Indexpolice*, no
  *Bedingungswerk* for any index tariff was obtained — the file's own central defect — so the
  *Indexjahr* definition, the observation dates, the payoff wording, the base of the
  participation, the *Wahlrecht* timing and any *Mindest-Cap* are all written from knowledge of
  the design family; **no cap level for any insurer in any year was established**, and **no
  documented worked *Indexjahr* was found**, so the two the model reproduces are constructed,
  labelled [std] in every cell and wired into the shipped return path precisely so the mechanic
  is asserted rather than described. For the *Pflegerentenversicherung*, no PIB, IPID or BIB, no
  premium, no charge level, no lapse rate, no rating-agency wording analysis and no count of
  contracts in force was obtained — the GDV life series does not carve the product out and the
  PKV series excludes it by construction, it being life business.
- **Every statutory paragraph number in this library is unverified.** `gesetze-im-internet.de`
  was refused at the gateway, so **no *Fassung* line was ever seen**: every statutory statement
  here is current in substance as reported in August 2026 and none is version-pinned. The
  specifically open items are named rather than smoothed over — whether § 169 Abs. 1 VVG's
  certain-event limitation is the route by which a term assurance has no surrender value; the
  internal paragraph structure of § 169 for the *Zeitwert* branch, so that no delib document
  cites a subsection for it; § 168 Abs. 3 VVG's ending of the termination right at *Rentenbeginn*,
  on which the whole `Sofort_DE_S` specification rests; the MindZV section numbers, where the
  three percentages are used and **no section number is cited anywhere**; the exact range of
  sections § 176 VVG imports, on which the BU surrender value, paid-up right and
  *Überschussbeteiligung* all depend; and whether a pure-risk *Pflegerente* falls inside § 169 at
  all. Four VVG provisions the endowment depends on — §§ 37, 38, 150 and 152 — were never
  searched at all, and nothing is asserted about any of them anywhere in the library.
- **Two source errors are recorded rather than quietly applied, and one document is excluded.**
  A search summary in the corpus conflates § 169 Abs. 3 VVG's five-year spreading of acquisition
  cost with the DeckRV's 2,5 % *Höchstzillmersatz*: they are different rules with different
  functions — a floor on the **value** against a cap on the **charge** — and `KLV_DE_S` asserts
  them in two separate checks for that reason. The `sofortrente` research file puts the
  *nachschüssig* effect at about 5 %; it is **0,34 %** on a monthly annuity, the 5 % being an
  annual-annuity identity applied to a monthly one — the research file is frozen and never
  amended, so the correction lives in that product's technical notes. And an Austrian ERGO AVB
  returned by a German AVB search is excluded and recorded: the VVG, the DeckRV and the MindZV
  do not apply to it, and the same caution applies to any `.at` or `.ch` document a later search
  returns.
- **Market figures are qualitative throughout, and one legal position could not be determined.**
  No endowment-specific new-business or in-force series and no time series showing the effect of
  the 2005 tax change; no size for the index-participation segment, which GDV counts inside
  conventional annuity business and for which probably no separate figure exists; no Riester
  contract count, chassis split or new-business series, and **no official statistic for
  *ruhende Verträge* at all**; no *Sofortrente* volume, average *Einmalbeitrag* or purchase-age
  distribution; no LTC-annuity contract count. Nineteen of the twenty-six carriers named in the
  endowment brief produced no document of any kind, and the variations tables across the library
  are records of absence rather than of variation. The status of the *private Altersvorsorge*
  reform as at the access date could not be established beyond a 2024 draft creating an
  *Altersvorsorgedepot* that did not become law in that parliamentary term, so nothing in this
  library asserts the current legal position on it.
- **[unverified] items remain wherever a claim could not be corroborated by any search result**,
  and under these retrieval conditions the tag does more work than it does in the sister
  libraries. It sits on the intermediate *Höchstrechnungszins* history between 1994 and 2025 and
  on every effective date in it; on the DeckRV amendment's *Bundesgesetzblatt* year, inferred
  from the surrounding chronology and carrying no BGBl citation, none having been returned and
  none being invented; on every *Ertragsanteil* value but the 18 % at age 65; on the § 851c ZPO
  protected amounts, which the Basisrente file states the **shape** of and prints not one level
  of; on the Landgericht Köln *Rentenfaktor* decision, which is reported with no case number,
  date, parties or appeal history, so no delib document gives it a docket; and on the 2025
  statutory *Pflege* benefit amounts, whose 2026 position is unknown.

```{toctree}
:hidden:
:maxdepth: 1
:caption: Products

products/kapitallebensversicherung/index
products/klassische_rentenversicherung/index
products/fondsgebundene_rentenversicherung/index
products/indexpolice/index
products/basisrente/index
products/riester_rente/index
products/sofortrente/index
products/risikolebensversicherung/index
products/berufsunfaehigkeit/index
products/pflegerentenversicherung/index
```

```{toctree}
:hidden:
:maxdepth: 1
:titlesonly:
:caption: Reference

references/regulatory-and-actuarial-references
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R18]: #delib-reg-r18
[REG-R24]: #delib-reg-r24
[REG-R27]: #delib-reg-r27
[REG-R39]: #delib-reg-r39
[REG-R42]: #delib-reg-r42
[REG-R43]: #delib-reg-r43
[REG-R45]: #delib-reg-r45
[REG-R47]: #delib-reg-r47
[REG-R48]: #delib-reg-r48
[REG-R49]: #delib-reg-r49
[REG-R50]: #delib-reg-r50
[REG-R51]: #delib-reg-r51
[REG-R53]: #delib-reg-r53
[REG-R9]: #delib-reg-r9
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
