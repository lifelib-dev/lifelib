# Product Specification

**Status:** Draft, 2026-08-26 (all cited sources accessed 2026-08-26).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling of the French **PER individuel assurantiel** — the
individual *plan d'épargne retraite* (retirement savings plan) created by the loi PACTE
and taken out as membership of a *contrat d'assurance de groupe* (group life insurance
contract). It does not describe any single insurer's contract. Facts carrying a source
tag — [S#] (primary product documents: *notices d'information*, *conditions générales*,
regulated fee tables) and [R#] (product-specific regulatory and actuarial references),
both numbered per `_research/per-assurance.md` and resolved against `sources.md` in this
directory — were extracted from the cited document. [REG-R#] resolves against the
cross-product reference library `references/regulatory-and-actuarial-references.md` (its
own frozen R-numbering). Values marked **[std]** are standardizations introduced for the
reference implementation; each [std] table row carries a numbered footnote giving the
rationale and, where recorded, the observed range across insurers. Facts not confirmed
against a retrieved document are flagged [unverified]. The mechanics anchors are five
retrieved *notices* / *conditions générales* [S1] [S2] [S3] [S4] [S7] and the two Cardif
documents published under the fee-transparency arrêté [S8] [S9]; the first of these is
called *the anchor contract* below. French terms of art stay French, glossed on first use.
The model built from this specification is **PER_FR_S**, on a monthly grid.

---

## Product overview and market role

A PER is a savings plan whose object is "l'acquisition et la jouissance de droits viagers
personnels ou le versement d'un capital", payable at the earliest from the liquidation of
a compulsory old-age pension or the age of art. L. 161-17-2 of the Code de la sécurité
sociale [R3 L. 224-1](#frlib-per_assurance-r3). It comes in two legal forms. The *PER bancaire* opens a
*compte-titres* (securities account). The **PER assurantiel** — the subject here — is
membership of a group life insurance contract "dont l'exécution est liée à la cessation
d'activité professionnelle" [R3 L. 224-1](#frlib-per_assurance-r3) [R20] [R21]; the difference the State itself
emphasises is that only the insurance form gives access to a *fonds en euros* (the
capital-guaranteed euro fund) [R21].

Every contract in the sample is a group contract with optional individual membership,
subscribed by an association acting as *souscripteur* — GPBF [S1], Le Cercle des
Épargnants [S2], AMAP [S3], Association Retraite Falguière or Association PERF
[S4] [S5] [S6], SEREP [S7], UFEP [S9] — which charges its own fee: €0,96 per year [S1],
€30 at adhesion [S2], €10 [S3] [S4] [S6], €25 [S5], €20 [S8]. Assets are **ring-fenced**
in a *comptabilité auxiliaire d'affectation* (ring-fenced auxiliary accounting):
creditors other than the plan's policyholders have no claim on them, and under-coverage
triggers a recovery plan agreed with the subscribers or imposed by the ACPR
[R8 L. 142-4 to L. 142-6](#frlib-per_assurance-r8). The carrier may be a life insurer or a *Fonds de Retraite
Professionnelle Supplémentaire* (FRPS) — Cardif Retraite is an FRPS [S9], the other five
sampled carriers are life insurers [S1] [S2] [S3] [S4] [S7]; the prudential consequences
of the FRPS regime were not researched [unverified].

Three features separate the product from an *assurance vie* multisupport, and they are
what this specification exists to capture. **Savings are blocked** until the retirement
maturity, releasable early only on a closed statutory list [R3 L. 224-4](#frlib-per_assurance-r3). **The default
management is a glide path**: unless the holder expressly decides otherwise, sums follow
an allocation that progressively reduces financial risk as the declared liquidation date
approaches [R3 L. 224-3](#frlib-per_assurance-r3) [R5 D. 224-3](#frlib-per_assurance-r5) — *gestion pilotée par horizon*. And the plan
carries **three compartments** keyed to the origin of the money, which decide both the
early-release rules and the exit form [R3 L. 224-2](#frlib-per_assurance-r3) [R3 L. 224-5](#frlib-per_assurance-r3).

The market is young and growing fast: 7,9 million insured and €111,9 bn of *encours* at
31 December 2025, on €20,2 bn of 2025 *versements* [R23] [REG-R46]; across all providers,
12,7 million holders and €141,1 bn at 30 September 2025, of which **PER individuels
€82,4 bn** [R24]. For individual PERs written by insurers at 31 December 2024: 4 195 500
plans in force, 91 % in accumulation; contributions €10 496 m, 65 % into *unités de
compte* (UC, unit-linked supports); provisions €70,7 bn, UC 47 % of them; average balance
**€16 600** in accumulation; benefits €2 837 m, split €93 m death, €1 651 m early releases
and transfers, €516 m annuities in payment, €305 m capital exits and €272 m small
annuities commuted at outset [R22]. That split is the shape of the liability: **early
release and transfer out, not death and not annuity, are the dominant accumulation-phase
outflows** — about 2,6 % of accumulation-phase provisions leaving every year [R22].

This specification standardizes one composite: a **compartment-1 PER individuel
assurantiel** with a euro support and a UC bucket, on the "Équilibré Horizon Retraite"
regulatory glide path, with an entry loading, separate euro and UC management charges, an
arbitrage charge on the annual rebalancing, a 1 % transfer indemnity in the first five
years, a *garantie plancher* death floor, and an exit split between *capital* and *rente
viagère* (life annuity).

---

## Representative specification

### Plan structure and legal form

| Parameter | Representative value | Basis |
|---|---|---|
| Legal vehicle | Individual membership of a *contrat d'assurance de groupe* subscribed by an association | [R3 L. 224-1](#frlib-per_assurance-r3) [S1] [S2] [S3] [S4] [S7] |
| Compartment modelled | **C1** — *versements volontaires* (the holder's own contributions) | [R3 L. 224-2 1°](#frlib-per_assurance-r3); choice **[std]** (1) |
| Minimum age at opening | 18 | [R4 L. 224-28](#frlib-per_assurance-r4) [R20] |
| Declared retirement age (*horizon*) | 64, changeable at any time; the anchor contract bounds it by the L. 161-17-2 minimum and 80, rolls it forward a year if not exercised, then renews tacitly | age **[std]** (2); mechanics [S1] [R5 D. 224-3](#frlib-per_assurance-r5) |
| Minimum initial *versement* | €500 | [S4] [S10]; observed €30 [S8] to €2 000 [S2]; choice **[std]** (3) |
| Association fee | €20, once at adhesion | [S8] |
| Cancellation (*renonciation*) period | 30 calendar days | [S4] [S7] [REG-R29] |
| Asset segregation | *Comptabilité auxiliaire d'affectation*, policyholder priority claim | [R8 L. 142-4](#frlib-per_assurance-r8) [R8 L. 142-5](#frlib-per_assurance-r8) |
| Annual statement | Rights at 31 December and history, contributions by L. 224-2 category, withdrawals, **all charges taken with the total in euros**, transfer value and cost, per-asset gross and net performance, the de-risking schedule | [R5 R. 224-2](#frlib-per_assurance-r5) [R16] [REG-R31] |

Footnotes to [std] rows:

1. Compartments 2 (*épargne salariale*) and 3 (*versements obligatoires*) reach an
   individual retail PER only through an incoming transfer [R3 L. 224-2](#frlib-per_assurance-r3); C1 is the
   primary flow. The model still carries `compartment` as a column, because it changes
   two operative rules — see *Contractual mechanics*.
2. No statute fixes a retirement age for the plan: the holder declares one and may change
   it [R5 D. 224-3](#frlib-per_assurance-r5), inside contract bounds where set [S1]. 64 is a modeling choice; this
   document asserts nothing about the value of the L. 161-17-2 age.
3. Observed minima: €30 [S8]; €500 [S4] [S10]; €1 000 (*gestion libre*) and €2 000
   (piloted), cut to €300 / €1 000 with scheduled contributions [S2]; none in [S1] [S3] [S7].

### Supports

| Parameter | Representative value | Basis |
|---|---|---|
| Rights expressed in | Euros and *unités de compte* | [R3 L. 224-3](#frlib-per_assurance-r3); two-support composite **[std]** (4) |
| Euro-fund capital guarantee | *Versements* net of entry loading, less management charges levied over the plan's life, less benefits paid — the [S1] and [S7] drafting, [S7] stating expressly that it is **not** a floor at gross premiums. [S3] drafts it with euro-fund interest net of charges **added**, and [S2] as "sommes versées nettes de frais"; the modelled quantity is the [S1] one | [S1] [S7] |
| Guaranteed technical rate on the euro support | **0,00 %** gross of charges, for the whole term; no contractual *taux minimum garanti*, no loyalty clause | [R9 A. 142-1](#frlib-per_assurance-r9) [S1] [S7] |
| UC guarantee | None; the insurer commits to the **number** of units, not their value | [S1] [S2] |
| Euro-fund gross asset return, base scenario | 3,38 % p.a. | [S9]; adoption **[std]** (5) |
| UC gross return, base scenario | 5,00 % p.a., net of fund-level charges | **[std]** (5) |
| Fund-level charges inside a UC (context, not an input) | equity 1,43 % p.a. (0,94 % retroceded), bond 0,91 % (0,45 %), real estate 2,00 % (0,50 %), diversified 1,17 % (0,57 %) | [S8] |
| *Provision de diversification* support | Out of scope — see `eurocroissance` | [S4] [S6] |

4. Rights may also be expressed in *parts de provision de diversification* and in *unités
   de rente* [R3 L. 224-3](#frlib-per_assurance-r3); both are excluded. The second exclusion matters legally too:
   L. 224-3's de-risking paragraphs are switched off for such plans [R3] and L. 142-8 sets
   them a special transfer value [R8].
5. **Both return assumptions are standardizations.** No public UC return assumption
   exists for this product [research §18]; 5,00 % is set above the euro asset return so
   the glide path has something to give up, and is stated net of fund-level charges
   because those are large relative to the wrapper charge [S8]. The euro figure has a
   source but not a *forward* one: [S9] reports a single realised historic number — "Taux
   de rendement de l'actif du fonds en euros **en 2025** : 3,38 %", one insurer, one year
   — and carrying it flat over a twelve-year projection is the modelling choice. It is
   the second-largest financial lever in the model after the glide path, and nothing
   behind it supports the extrapolation; treat it as a dial, not as an observed forward
   rate. Neither figure is a projection any insurer publishes.

### Gestion pilotée par horizon — the glide path

*Gestion pilotée par horizon* is the **default management by law** [R3 L. 224-3](#frlib-per_assurance-r3), with a
right to opt out of the minimum de-risking pace on express request [R5 D. 224-3](#frlib-per_assurance-r5).
D. 224-3 delegates the *rythme minimal de sécurisation* and the definition of low-risk
assets to a ministerial *arrêté* [R5]; that arrêté fixes four qualified profiles and, for
each, a minimum share of the plan balance in low-risk assets by distance to the declared
liquidation date [R6 art. 1 part (a)](#frlib-per_assurance-r6):

| Profile | more than 10 years out | 10 to 5 years out | 5 to 2 years out | under 2 years out |
|---|---|---|---|---|
| *Prudent horizon retraite* | 30 % | 60 % | 80 % | 90 % |
| *Équilibré horizon retraite* | — | 20 % | 50 % | 70 % |
| *Dynamique horizon retraite* | — | — | 30 % | 50 % |
| *Offensif horizon retraite* | — | — | 30 % | 50 % |

Suravenir reproduces this grid verbatim as its own product specification [S7] and
Generali's three profiles hit exactly these percentages over exactly these bands [S2].
**In this market the regulatory grid is not a floor insurers beat; it is the product.**
Insurers may sit above it, and the anchor contract does, on **20 one-year bands** rather
than four: its *Équilibré* ladder holds 20 / 22 / 25 / 50 / 70 / 80 % in the euro support
as the horizon closes, against 30 / 45 / 60 / 80 / 95 / 100 % for *Prudent* [S1].

A second minimum bites since 24 October 2024: a minimum share of *versements* routed to
unlisted eligible vehicles (ELTIFs, alternative investment funds, commercial-company
securities managed by portfolio management companies, sustainable collective vehicles),
at 20, 15, 10 and 5 years out — prudent 6 / 4 / 2 / — %, équilibré 8 / 6 / 5 / 3 %,
dynamique 12 / 10 / 7 / 5 %, offensif 15 / 12 / 9 / 6 % — thresholds cut by 30 % for
company plans, compliance by 31 December 2026 [R6 part (b)](#frlib-per_assurance-r6) [R7]. The anchor contract
implements it with a private-equity line at 6 / 4 / 2 / 0 % on its prudent profile [S1];
MACSF states its three profiles comply [S3]. **The reference model does not carve the
unlisted bucket out of the UC bucket**, and this is the one regulatory requirement it
declines to implement, so the reason belongs here rather than in a footnote. Part (b) is a
minimum on the *versements* routed to eligible vehicles, not on the plan balance, so it
does not compose with the part (a) balance grid the model runs on; no retrieved document
gives those vehicles a return, a charge or a liquidity basis of their own, so a third
support would carry nothing but **[std]** assumptions; and on the base scenario it would
change no cash flow, because the model already values the whole UC bucket at one return.
Modelling it means adding a third support with its own return and its own charge, and
re-cutting the glide path on a contribution base rather than a balance base. `model.md`
records the same exclusion.

| Parameter | Representative value | Basis |
|---|---|---|
| Profile modelled | *Équilibré horizon retraite* (the market default) | [S1] [S2] [S4] [S7]; adoption **[std]** (6) |
| Glide-path grid | The regulatory minimum grid above: euro share 0 % / 20 % / 50 % / 70 % | [R6] [S2] [S7] |
| Band-edge convention | The tighter minimum applies at a boundary: k > 10 → 0 %, 10 ≥ k > 5 → 20 %, 5 ≥ k > 2 → 50 %, k ≤ 2 → 70 %, with k the years to the declared horizon | **[std]** (7) |
| "Low risk" realised as | The euro support in full | **[std]** (7) |
| Rebalancing | Annual, in the month that starts the plan year, on both the new *versement* and the existing balance | frequency **[std]** (8); scope [S1] |
| *Frais d'arbitrage* on the rebalancing | 0,30 % of the amount switched | [S1]; adoption **[std]** (9) |
| Holder arbitrage under a horizon profile | Not permitted | [S1] [S2] [S4] |
| Change of declared retirement date | Immediate re-allocation of the whole balance | [S3] [S4] |
| Insurer's right to restate a profile | May unilaterally change a profile's allocation to keep the regulatory de-risking | [S3] [S4] |

6. The sample's default profile is "Équilibré Horizon Retraite" [S1] [S4] [S7], Generali
   selling under "Gestion Horizon Retraite" on the "Équilibré" reference [S2]. No public
   data exists on the mix of profiles actually chosen [research §18].
7. Two conventions are needed and no retrieved text settles either. (i) R6's part (a) grid
   **was** extracted, percentages and band headings both [research §5], and it is the
   table reproduced above. What it does not settle is which side of a boundary year each
   band takes: the headings as rendered read "≥ 10 years out" and "from 10 years out",
   which overlap at `k = 10`, and the same at 5 and at 2. Assigning the boundary year to
   the tighter band is therefore the model's own convention **[std]**, not a reading of
   the text. (Research caveat 12, which flags "jusqu'à N ans" as [unverified], is about
   R6's part (b) unlisted-asset table, not this one.) (ii) The definition of *actifs présentant un profil
   d'investissement à faible risque* is delegated to an arrêté that was not retrieved
   [R5 D. 224-3](#frlib-per_assurance-r5), and the two contract definitions found disagree — SRRI ≤ 3 [S7] against
   ≤ 2 including the euro fund [S3]. Realising the low-risk bucket wholly as the euro
   support is the most conservative reading of both and keeps the model to two supports.
8. Observed frequencies: semi-annual in Q2 and Q4 [S1]; semi-annual [S2]; semi-annual on
   15 March and 15 September [S3]; threshold-driven and at least semi-annual [S4];
   **quarterly** [S7]. Annual is the coarsest, and on the monthly projection grid it is no
   longer forced — it is chosen. The reference model keeps it because the de-risking grid
   is keyed by whole **years** to the horizon, so a sub-annual rebalancing re-imposes the
   *same* target inside the year: it corrects drift rather than de-risking faster, and
   turning it on is an assumption change rather than a finer grid. It still understates the
   glide path's tracking accuracy and overstates each switch, and the cost is now
   measurable rather than merely arguable — on the anchor cell, quarterly rebalancing
   changes the final balance by **−0,0142 %** and the twelve-year arbitrage charge from
   95,75 to 96,21; on the 32-year model point 12, by −0,0343 %.
9. Horizon arbitrage is free at [S2] [S3] [S4] [S5] [S7]; the anchor contract charges
   0,30 % of amounts switched [S1] and Cardif 1 % with no free arbitrages [S8]. The
   non-nil rate makes the cost of the glide path a visible line; zero reproduces the
   majority contract.

### Charges

Every figure below is a **maximum** stated in a *notice* or in a regulated fee table.

| Charge | Representative value | Basis |
|---|---|---|
| *Frais sur versement* (entry loading) | **2,50 %** of each *versement* | [S8] [S10]; adoption **[std]** (10) |
| Euro-support management charge | **0,70 % p.a.** | [S8] [S9]; adoption **[std]** (11) |
| UC management charge | **0,70 % p.a.** | [S8] [S9]; adoption **[std]** (11) |
| *Gestion pilotée par horizon* surcharge | None — inside the 0,70 % | [S8] |
| *Frais d'arbitrage* | 0,30 % of the amount switched | [S1]; adoption **[std]** (9) |
| Charge basis and timing | Levied on the end-of-year balance, after crediting | **[std]** (12) |
| Outgoing transfer indemnity | 1 % of acquired rights before the fifth anniversary of the first *versement*, **nil** thereafter | [R3 L. 224-6](#frlib-per_assurance-r3) [S1] [S2] [S3] [S4] [S5] [S6] [S7] [S8] |
| Additional transfer-value reduction | Up to **15 %** of the value of rights expressed in euros where the transfer right exceeds the asset share backing it; a switch, **off** in the base | [R5 R. 224-6](#frlib-per_assurance-r5) [R3 L. 224-6](#frlib-per_assurance-r3) [S8]; base setting **[std]** (12) |
| Capital exit charge | **0 %** | [S1] [S2] [S3] [S7] [S8] |
| Early-release (*déblocage anticipé*) charge | **0 %** | [S2] [S3] [S7] |
| *Frais d'arrérages* on annuity instalments | **1,50 %** of each gross instalment | [S8]; adoption **[std]** (13) |
| Annuity-phase management charge | 0,80 % p.a. of annuity reserves — cross-referenced, not modelled here | [S7] |

10. Observed entry loadings span the market: 0 % [S4] [S7]; 2,50 % [S8] [S10]; 3 %
    (2,5 % under a *convention d'abonnement*) [S3]; 3,50 % [S6]; 4 % [S1]; 4,50 % [S2];
    4,80 %, on incoming transfers too [S5]. 2,50 % is the figure in the only
    current-regime documents publishing one under the fee-transparency arrêté [R16] [S8].
11. Observed AUM charges: euro 0,50 % [S3] to 2,30 % [S5] [S6]; UC 0,50 % [S3] [S4] to
    1,10 % [S2]. The pair 0,70 % / 0,70 % is Cardif's regulated grid [S8], adopted also
    as the only sampled figure with a matching gross-charge-net triple on the same euro
    fund [S9] — crediting and charge assumptions from one document.
12. Charge timing differs and is load-bearing: end-of-month balance, monthly [S1];
    quarterly on UC, annually on the euro fund at value date 31 December pro rata temporis
    [S2]; annually at 31 December on both [S3]; accrued daily, levied annually on the euro
    fund and monthly on UC [S7]. The monthly projection grid can now carry more than one of
    them, and the reference model deliberately keeps the [S3] convention — the charge
    levied whole at the plan-year end on the post-crediting balance — because that is what
    keeps the *garantie plancher* base exact. The base accumulates a **sum** of charges
    rather than a product of factors, so twelve monthly charges do not add to the annual
    one: measured, a monthly levy leaves the account value at every anniversary unchanged
    but moves the base by up to €71,95 on the anchor cell and €531,57 on model point 12.
    [S1]'s monthly levy on an end-of-month balance is the documented variant and is a new
    assumption rather than a finer grid. The price of the convention is that a mid-year
    exit is valued gross of the plan year's charge, 0,387 % above the anniversary value in
    the anchor cell's last plan year. The 15 % transfer-value reduction is
    nil in the base for a different reason — it is a management action conditional on a
    market state the base scenario does not produce, and in a rising-rate scenario it
    dominates the 1 % fee by an order of magnitude [S3] [S8].
13. Observed *frais d'arrérages*: 0 % [S2] [S5] [S7]; 0,50 % capped at 1 % of the monthly
    social security ceiling per instalment [S4]; 0,50 % [S6]; 1 % [S1]; 1,50 % [S8];
    **3 %** [S3]. 1,50 % is the current-regime regulated figure [S8]; charged on every
    instalment for life, it moves the capital at which the commutation test bites.

### Euro-fund crediting and participation aux bénéfices

| Parameter | Representative value | Basis |
|---|---|---|
| Maximum technical interest rate for a PER | **0 %** | [R9 A. 142-1](#frlib-per_assurance-r9) |
| Guaranteed accumulation rate | 0,00 % — the euro support has a **capital floor plus profit sharing**, not a guaranteed rate | [S1] [S7] [R9] |
| Statutory profit-sharing frame | Minimum PB computed globally from a *compte de participation aux résultats*; the *provision pour participation aux bénéfices* (PPB) is the smoothing device | [REG-R14] [REG-R15] [REG-R16] [S1] |
| PPB release horizon | Eight years generally; **fifteen** for commitments under a *comptabilité auxiliaire d'affectation* per L. 142-4 — which is what a PER is | [REG-R16] [R8 L. 142-4](#frlib-per_assurance-r8) |
| Contractual PB clause | Present at the anchor contract [S1]; **absent** at [S4] [S5] [S6] [S7]; Generali instead announces an annual *taux minimum garanti* [S2] [REG-R18] | [S1] [S2] [S4] [S7] |
| Crediting frequency | Annual, at 31 December | [S3] [S7]; adoption **[std]** (14) |
| Observed gross-charge-net triple | euro-fund asset return **3,38 %** in 2025, management charge **0,70 %**, net rate served **2,75 %** | [S9] |
| UC income treatment | 100 % of coupons and dividends reinvested (90 % on SCPI units at one contract) | [S1] [S4] [S6]; exception [S5] |

14. Observed crediting: **weekly**, at a rate from a quarterly prospective PB assessment,
    definitively acquired each Friday [S1]; daily compounding with the annual PB at value
    date 31 December [S2]; annual at 31 December [S3]; annual with partial exits revalued
    pro rata temporis at the served rate [S7]. The reference model credits both supports
    at `(1 + r)^(1/12) − 1` a month, so twelve months compound back to the published annual
    rate **exactly** and no anniversary balance moves. That is the monthly realisation of
    the one thing every sampled contract agrees on for a **mid-year exit**: [S7]'s pro rata
    temporis revaluation at the served rate, [S1]'s weekly crediting definitively acquired
    each Friday, and [S2]'s daily compounding. Crediting the whole year at the anniversary
    instead would pay every mid-year death, release and transfer on a balance carrying no
    return since the last one.

Note what the [S9] triple says: 3,38 % gross less a 0,70 % charge is 2,68 %, yet the rate
served was **2,75 %** — the extra seven basis points came from somewhere other than the
year's asset return, which is what a PPB is for [REG-R15] [REG-R16]. The reference model
credits the euro support at the asset return, takes the charge on the post-crediting
balance and does **not** model a PPB stock.

### Death benefit during accumulation

| Parameter | Representative value | Basis |
|---|---|---|
| Effect of death before maturity | The plan **closes** | [R3 L. 224-4 II](#frlib-per_assurance-r3) [R21] |
| Contractual benefit | The accumulated savings at the date death is notified, euro part revalued to that date | [S3] |
| *Garantie plancher* (death floor) | Not less than *versements* net of entry loading, less management charges levied over the plan's life, less benefits already paid | [S1] |
| Cessation | The member's **70th birthday** | [S1] [S3] |
| Cap | €762 245 across all contracts [S3]; pro-rating above €800 000 of aggregate net premiums [S1] | [S1] [S3] |
| Charge for it | 0,10 % p.a. on UC balances [S3]; 0,12 % p.a. inside the 1 % management charge [S1] — modelled as **included in the 0,70 %** | inclusion **[std]** (15) |
| Optional death cover (variation) | Reimburses the *capital sous risque*; ages 12 to under 70 at adhesion, one-year waiting period, no medical underwriting, cap €100 000, ends at 75; premium **0,15 ‰ to 5,15 ‰ per month** of capital at risk by age | [S7] |
| Suicide exclusion | First year | [S1] [S7] |

15. Neither published *garantie plancher* charge is separable from its own contract's AUM
    charge in a way that transfers to a 0,70 % composite, and folding it in keeps one
    charge dial per support. It is revisable by agreement between subscriber and insurer
    on demographic grounds in both contracts [S1] [S3], so it is not a contractual
    constant in any case.

**Two draftings of the floor, and this table states one of them.** [S1] guarantees a death
benefit "not less than premiums net of charges minus benefits already paid" — no interest
limb, and [S7] says expressly of its own euro guarantee that it is not a floor at gross
premiums. [S3] drafts the same guarantee the other way: the settled amount "cannot be less
than contributions net of loading **plus euro-fund interest net of management charges**".
The representative value above is [S1]'s, because that is what the reference model
computes; `technical-notes.md` is the source of truth for the recursion and states the
same thing. The choice is load-bearing rather than stylistic: on [S1]'s drafting the gap
between the account value and the floor is exactly the cumulative gross investment return,
so the floor bites only after a loss, and the model asserts that identity; on [S3]'s the
euro leg of that return accrues to the floor too, and on an all-euro plan the floor would
track the account value. [S3] remains the source for the €762 245 cap and, with [S1], for
the cessation at 70 — the *Cessation* and *Cap* rows above.

### Exit at retirement

| Parameter | Representative value | Basis |
|---|---|---|
| Maturity trigger | The earliest of pension liquidation and the L. 161-17-2 age | [R3 L. 224-1](#frlib-per_assurance-r3) |
| Exit menu, C1 and C2 | *Capital* "libéré en une fois ou de manière fractionnée", or a *rente viagère*, or a mix — unless the holder has irrevocably opted for the annuity beforehand | [R3 L. 224-5](#frlib-per_assurance-r3) [R20] [R21] |
| Exit menu, C3 | **Life annuity only** | [R3 L. 224-5](#frlib-per_assurance-r3) [S2] |
| Anchor exit split | 70 % *capital* in one payment, 30 % converted to a *rente viagère* | **[std]** (16) |
| Partial capital exit minima (anchor contract) | €750 per instalment, residual ≥ €750 with ≥ €150 per support, paid within ten working days | [S1] |
| Annuity technical interest rate | **0 %** | [R9 A. 142-1](#frlib-per_assurance-r9) [S2] [S3] [S7] |
| Annuity mortality basis | Homologated generational **TGF05** (female) / **TGH05** (male), or the insurer's own certified experience table, which may never produce a cheaper annuity | [R11 A. 335-1](#frlib-per_assurance-r11) [R12] [REG-R21] [REG-R23] |
| Table vintage | In force at annuity commencement [S2] [S4] [S7]; the anchor contract freezes the table **in force at adhesion** for deductible C1 sums and adhesion-date incoming transfers [S1] | [S1] [S2] [S4] [S7] |
| Annuity factor, anchor cell | **22,0000** per €1 p.a. — male aged 64, annual in arrears, no reversion, 0 % technical rate | **[std]** (17) |
| Payment frequency | Quarterly in arrears [S1] [S2]; monthly in arrears [S7]; anchor **annual in arrears** | **[std]** (17) |
| Small-annuity commutation threshold | Monthly *quittance d'arrérages* not exceeding **€110** including statutory increases, multiplied by the number of months in the payment period; requires the annuitant's agreement | [R10 A. 160-2](#frlib-per_assurance-r10) |
| Take-up in practice, 2024 | Of €1 093 m paid on individual PERs in payment: €516 m annuities, €305 m capital exits, **€272 m small annuities commuted at outset**; averages €1 300 p.a. annuity, €12 500 capital exit, €16 200 commuted | [R22] |

16. No public data exists on the annuity/capital election [research §18]. The 2024
    payment-phase split by amount was 47 % annuity, 28 % capital, 25 % commuted small
    annuity [R22] — but the third is an annuity election that reverses at settlement, so it
    is not an election rate. 70/30 puts the anchor annuity **below** the commutation
    threshold, exercising the reversal.
17. **No sampled insurer publishes an annuity rate card.** The contracts say only "la
    table de mortalité en vigueur" and "le taux d'intérêt technique en vigueur"
    [S1] [S2] [S4] [S7], and the TGF05 / TGH05 rate tables, annexed to a public arrêté
    [R12], were not extracted and are not shipped [REG-R21]. At a 0 % technical rate the
    factor collapses to the tariff table's expected number of instalments, so 22,0000
    asserts 22 further annual payments to a male aged 64 — a placeholder, to be replaced
    by a TGH05 computation before any quantitative use. Annual payment in arrears is fixed
    by `annuity_factor.csv`, which holds an undiscounted **count of annual instalments** —
    not by the projection grid, which is monthly: paying quarterly or monthly means
    replacing that table, not changing a step. The model applies the commutation test on
    the monthly equivalent for exactly that reason.

### Anchor model cell

| Attribute | Value | Basis |
|---|---|---|
| Sex / attained age at the valuation date | M / 52 | **[std]** (18) |
| Declared retirement age | 64 → 12 years to horizon | **[std]** (2) |
| Completed years since the first *versement* | 2 | **[std]** (18) |
| Compartment / profile | C1 / *équilibré horizon retraite* | (1), (6) |
| Opening balance | €16 600, entirely in UC | [R22]; all-UC **[std]** (18) |
| Opening *garantie plancher* base | €16 000 | **[std]** (18) |
| Annual *versement* | €3 000, at the start of each plan year to the horizon | **[std]** (19) |
| Exit | 70 % capital in one payment, 30 % to a *rente viagère* | (16) |
| Deduction elected at entry | Yes — recorded, and **inert in the cash flows** | [R13] [R18] [R20]; see *Regulatory context* |

18. Modeling anchors. €16 600 is the published average accumulation-phase balance on an
    individual PER at 31 December 2024 [R22]; a two-year-old plan holding it implies an
    incoming transfer at adhesion, the common case — 0,2 million of the 1,2 million new
    insured in 2024 arrived by transfer, carrying €4,2 bn [R22]. Holding it all in UC is
    consistent with the *équilibré* grid, whose euro minimum is nil at 12 years out [R6],
    and makes the first band crossing visible. The €16 000 opening floor sits €600 below
    the balance; that gap is the accumulated investment return to date.
19. Implied average annual contribution per individual PER: €10 496 m over 4 195 500 plans
    ≈ €2 502 in 2024 [R22]; €20,2 bn over 7,9 million insured ≈ €2 557 in 2025 [R23].

---

## Contractual mechanics

**Blocage.** Savings are blocked until the earliest of pension liquidation and the
L. 161-17-2 age [R3 L. 224-1](#frlib-per_assurance-r3), and the contracts describe the accumulation phase as
having **no surrender right except in the statutory cases** [S2] [S3] [S4] [S7]. This is
not a surrender charge, not a market value adjustment and not a penalty: the right does
not exist. A model of this product that carries a lapse decrement has mis-stated the
contract.

**The cases of *déblocage anticipé*.** The statutory list, as consolidated at 14 June
2026, is **seven** items [R3 L. 224-4 I](#frlib-per_assurance-r3): (1) death of the spouse or PACS partner;
(2) invalidity of the holder, a child, the spouse or PACS partner, within the 2° and 3°
of art. L. 341-4 of the Code de la sécurité sociale; (2 bis) serious illness, disability
or a particularly grave accident affecting a dependent child; (3) over-indebtedness
within art. L. 711-1 of the Code de la consommation; (4) expiry of unemployment insurance
rights, or a former director or board member without an employment contract or corporate
office for at least two years; (5) cessation of self-employment following a judicial
liquidation, or a situation justified by the president of the commercial court in a
*conciliation*; (6) use of the savings to **acquire the main residence**, from which
rights arising from compulsory contributions (C3) are **excluded**; (7) the holder is
under 18 at the date of the request. The classic "six cas de déblocage anticipé"
formulation is out of date — economie.gouv.fr still says six [R21], service-public.fr
lists the extra cases [R20], and the anchor contract's June 2026 notice reproduces all
seven [S1]. The commencement date and amending instrument for 2° bis and 7° were not
identified [unverified]. Release is paid as a **single payment** of all or part of the
eligible rights, at the holder's choice [R5 D. 224-4](#frlib-per_assurance-r5); the anchor contract requires the
event to fall between adhesion and the planned retirement age, sets a €750 minimum on a
partial release with a €750 residual and €150 per support, and pays within ten working
days [S1]. Three contracts levy **no charge** [S2] [S3] [S7].

**Death before maturity closes the plan** [R3 L. 224-4 II](#frlib-per_assurance-r3) [R21]; the insurance form pays
the accumulated savings to the named beneficiaries under the life insurance rules
[R20] [R21], floored by the *garantie plancher* where granted [S1] [S3].

**The glide path as an operative rule.** At each rebalancing date the target low-risk share
is read off the profile's grid against the years remaining to the declared liquidation
date, and both the incoming *versement* and the existing balance are allocated to that
target [R6] [S1]. Three consequences a projection must respect: the target is a
**minimum**, not an allocation [S1]; changing the declared retirement date triggers an
**immediate** re-allocation of the whole balance [S3] [S4]; and the insurer may restate a
profile's allocation unilaterally [S3] [S4], so a published grid is a snapshot.

**Transfer out.** Rights under accumulation are transferable to **any** other PER, and the
transfer does not alter the surrender or liquidation conditions [R3 L. 224-6](#frlib-per_assurance-r3). The fee
"ne peuvent excéder 1 % des droits acquis" and is **nil** after five years from the first
*versement* in the plan, or where the transfer occurs from the L. 224-1 maturity
[R3 L. 224-6](#frlib-per_assurance-r3); every sampled contract reproduces the rule
[S1] [S2] [S3] [S4] [S5] [S6] [S7] [S8], and MACSF adds that it is nil once the member has
liquidated a compulsory pension or reached the L. 161-17-2 age [S3]. Separately, where the
transfer value of the mathematical provisions exceeds the asset share representing them,
the plan may reduce that value, "sans que cette réduction puisse toutefois excéder
**15 %** de la valeur des droits individuels du titulaire relatifs à des engagements
exprimés en euros" [R5 R. 224-6](#frlib-per_assurance-r5) [S8]. Settlement runs from 10 working days [S1] to
2 months [S4] [S6]. A **different** rule governs transfers *in* from legacy products
(PERP, Madelin, PERCO, article 83, PREFON, COREM, CRH): 1 % of acquired rights, nil after
**ten** years from the first contribution [R5 D. 224-18](#frlib-per_assurance-r5) [R4 L. 224-40](#frlib-per_assurance-r4).

**Exit at maturity.** The irrevocable annuity election may be made at adhesion or later
and the insurer must warn of its character in writing [R3 L. 224-5](#frlib-per_assurance-r3) [S1] [S2] [S4]; once a
fractional capital settlement has begun one contract accepts no further contributions
[S3]; and from five years before retirement the manager must answer questions on rights
and exit options, with six months' advance notification [R4 L. 224-30](#frlib-per_assurance-r4).

**Annuity conversion and commutation.** The annuity depends on the accumulated value net
of social and tax levies, the dates of birth, the mortality table in force, the option
chosen, the frequency, the *annuités garanties*, the technical rate in force and the
service charge; the insurer does not guarantee the amount, and annuities in payment are
revalued through the profit-sharing account [S1] [S4] [S7]. Because the technical rate is
capped at 0 % [R9 A. 142-1](#frlib-per_assurance-r9), the conversion factor is an undiscounted expected-instalment
count — with consequences set out in the technical notes. The insurer may substitute a
single capital payment, with the annuitant's agreement, where the monthly *quittance
d'arrérages* does not exceed €110 including statutory increases, scaled by the number of
months in the payment period [R10 A. 160-2](#frlib-per_assurance-r10); contracts still quote the superseded
PER-specific €240 per quarter [S2] and €80 per month [S4], from the €100 and €80 vintages
of the abrogated art. A. 160-2-1 [R10]. The mechanism is not marginal — €272 m of 2024
individual-PER benefits at an average €16 200 per case [R22], and with the average annuity
in payment at €1 300 p.a., about €108 per month, the average PER annuity sits **just
under** the threshold [R22] [R10]. Every contract also publishes a **minimum
transfer-value table for the first eight years** on maximum charges [S1] [S2] [S3] [S4]
[S7] — the natural external validation target for a projection model.

---

## Riders and options

**In scope (modelled as flags):**

- **Garantie plancher** — a death floor at *versements* net of charges less benefits paid,
  included rather than optional in two contracts, ceasing at the 70th birthday, capped at
  €762 245 across contracts [S3] or pro-rated above €800 000 of aggregate net premiums
  [S1]. Modelled with the cover inside the management charge; footnote (15).
- **Annuity reversion**, statutorily required to be offered [R3 L. 224-1](#frlib-per_assurance-r3) — observed
  50 %–200 % in 10 % steps [S2], 50 %–150 % narrowing to 50 %–100 % with guaranteed
  annuities [S4], **1 %–100 %** [S7], the beneficiary fixed definitively at set-up [S1] —
  and **annuités garanties**, bounded by art. A. 335-1 at life expectancy at the annuity
  effective date **minus five years** [S2] [S4], narrowed by one contract to 5 to 25 years
  in 5-year steps [S7].
- **Exit form and split** — capital in one payment, fractional capital, annuity or a mix
  [R3 L. 224-5](#frlib-per_assurance-r3); carried as model point columns.

**Out of scope for the composite, and why:**

- **Optional death cover** on the *capital sous risque* [S7] — the only published
  mortality rate card in the sample. It is a *gross premium* scale on a no-underwriting
  cover, not a mortality assumption, and must not be read as one.
- **Rente par paliers** (2 or 3 steps, intermediate steps ≤ 10 years, variation limited to
  −50 % and +100 % [S2] [S4] [S7]), **reversion recomputation** where the surviving spouse
  at death is not the one who held that status at liquidation [S7], and the **rente
  temporaire d'éducation** to minor children to their 25th birthday [S2] — option costs no
  sampled tariff quantifies. **Sécurisation des plus-values** (0,50 % of the amount moved)
  and loss-limitation options (0,20 % p.a.) exist only outside a horizon profile [S2].
- **Garanties complémentaires** — death, disability income, loss of autonomy,
  unemployment and a value guarantee, with the loss-of-autonomy benefit capped at
  **twice** the rights otherwise acquired. Both the permission and the cap are
  [R8 L. 142-3](#frlib-per_assurance-r8); [R9 A. 142-2 to A. 142-4](#frlib-per_assurance-r9) carry the loss-of-autonomy cover's
  operating conditions instead — benefit reduction limits, medical underwriting and annual
  revaluation (A. 142-2), presentation in a separate chapter of the policy with its own
  premium (A. 142-3), and annual disclosure of the revalued benefit and the premium paid
  for it (A. 142-4). Chasing the cap to R9 finds nothing, which is why the two are split
  here.
- **Provision de diversification** supports with an 80 % capital guarantee at maturity,
  1 % p.a. plus up to 10 % of positive performance [S4] [S6], which are the
  `eurocroissance` product.

---

## Variations across insurers

1. **The dominant variation is the distributor, not the insurer.** Spirica writes [S4],
   [S5] and [S6] under one licence, with the same *Fonds Euro PER Nouvelle Génération*,
   the same three horizon profiles and the same annuity options — yet the entry loading
   runs 0 % / 4,80 % / 3,50 %, the euro charge 2,00 % / 2,30 % / 2,30 %, the UC charge
   0,50 % / 1,00 % / 1,00 % and the *arrérage* charge 0,50 % / 0 % / 0,50 %. Any statement
   of the form "insurer X charges Y on a PER" is meaningless here; **the contract, not the
   carrier, is the unit of analysis.**
2. **The mechanics, by contrast, are close to uniform,** because the statute fixes them:
   three compartments [R3 L. 224-2](#frlib-per_assurance-r3), seven early-release cases [R3 L. 224-4](#frlib-per_assurance-r3), one exit
   menu [R3 L. 224-5](#frlib-per_assurance-r3), the 1 % / five-year transfer cap [R3 L. 224-6](#frlib-per_assurance-r3), a 0 % maximum
   technical rate [R9 A. 142-1](#frlib-per_assurance-r9) and a de-risking grid most insurers adopt at its
   regulatory minimum [R6] [S2] [S7]. A reference implementation can model **one** PER
   assurantiel and treat the charge basis as a parameter set.
3. **Glide-path granularity and cost.** Twenty one-year bands [S1] against the four
   regulatory bands [S2] [S4] [S5] [S6] [S7] [S8], with one contract driving the ladder
   off the member's age in a financial annex [S3]; rebalancing quarterly [S7],
   semi-annually on fixed dates [S1] [S3] or threshold-driven [S4] [S5]; arbitrage free
   [S2] [S3] [S4] [S5] [S7] against 0,30 % [S1] and 1 % [S8]. Chosen: the four regulatory
   bands, annual rebalancing, 0,30 %.
4. **Euro-fund crediting, profit sharing and death floor.** Crediting weekly [S1],
   daily-compounded with the PB at value date 31 December [S2], or annual
   [S3] [S4] [S5] [S6] [S7]; a contractual PB clause [S1], an announced annual *taux
   minimum garanti* [S2] [REG-R18], or **none at all** [S4] [S5] [S6] [S7]; a death floor
   included as standard to 70 [S1] [S3], optional [S4] [S5] [S6], an age-rated rider [S7]
   or unstated [S2] [S8]. Chosen: annual crediting, no contractual PB clause, floor
   included to 70 with the €762 245 cap.
5. **Annuity basis and charge.** Table vintage frozen at adhesion for deductible C1 sums
   and adhesion-date incoming transfers [S1] against current at liquidation elsewhere
   [S2] [S3] [S4] [S7]; payment quarterly in arrears at 1 % [S1], quarterly at 0 % [S2],
   monthly at 0 % [S7], 3 % per gross instalment [S3], 1,5 % [S8]. Chosen: current at
   liquidation, annual in arrears at 1,50 %. A model that assumes a single conversion
   basis will misprice the [S1]-style frozen-table guarantee, a long-dated option the
   contract gives away.

---

## Regulatory context

**Constitutive law.** Art. 71 of the loi PACTE created the PER as a new Chapitre IV of the
Code monétaire et financier [R1], and the ordonnance n° 2019-766 du 24 juillet 2019
replaced the PERP, Madelin, PERCO and article 83 contracts with one collective, one
category and one individual plan, marketable from 1 October 2019, with transfer rights
from the legacy products [R2] [R4 L. 224-40](#frlib-per_assurance-r4); the two liberalisations that report
identifies are early release for the main residence and free choice between annuity and
capital outside compulsory contributions [R2]. Common rules sit at L. 224-1 to L. 224-8
[R3] [REG-R34], individual-plan rules at L. 224-28 to L. 224-39 [R4], the regulatory layer
at R. 224-1 to D. 224-18 [R5].

**Insurance law.** The insurance-form chapter is L. 142-1 to L. 142-8 of the Code des
assurances [R8]: tariffs from mortality parameters and a contractual technical rate whose
maximum is fixed by arrêté [R8 L. 142-2](#frlib-per_assurance-r8); enumerated and bounded *garanties
complémentaires* [R8 L. 142-3](#frlib-per_assurance-r8); a mandatory ring-fenced *comptabilité auxiliaire
d'affectation*, with legacy commitments moved into it by 1 January 2023 [R8 L. 142-4](#frlib-per_assurance-r8), a
policyholder priority claim [R8 L. 142-5](#frlib-per_assurance-r8) and an ACPR-supervised recovery mechanism on
under-coverage [R8 L. 142-6](#frlib-per_assurance-r8). The maximum technical rate is **0 %** — "Les tarifs
pratiqués par les entreprises d'assurance au titre des plans d'épargne retraite sont
établis d'après un taux d'intérêt technique au plus égal à 0 %" [R9 A. 142-1](#frlib-per_assurance-r9) — which
displaces the general 75 %/60 %-of-TME ceiling [REG-R17] for this product. Mortality bases
follow art. A. 335-1: homologated tables by sex, or the undertaking's own experience tables
certified by an independent actuary, with an explicit floor that an experience-table
annuity tariff may never be cheaper than the homologated one [R11] [REG-R23]. The
homologated annuity tables are the generational **TGF05** and **TGH05** [R12] [REG-R21];
the non-annuity **TH 00-02 / TF 00-02** govern the death benefit during accumulation
[REG-R22] [REG-R23]. No rate table is shipped with this library; the decrement CSVs are
**[std]** proxies built from INSEE population data [REG-R24].

**Conduct, information and macroprudential.** The duty of advice at sale covers the
prospect's situation, financial knowledge, horizon, return expectations, objectives
including sustainability preferences and retirement needs, plus the plan's
characteristics, management methods, availability conditions and tax treatment
[R4 L. 224-29](#frlib-per_assurance-r4) [REG-R12]. The general life regime applies on top — the *note
d'information* and the one-page *encadré* with its four-category fee disclosure
[REG-R30], the thirty-day *renonciation* window [REG-R29], the annual statement and
website publication duties [REG-R31], and for the UC the PRIIPs and AMF
collective-vehicle layer [REG-R33]. Note what the *encadré* does **not** do: it requires
maxima to be disclosed, not levels to be capped [REG-R30] — which is why every charge
level here is a maximum and every adopted level is **[std]**. Separately, the Haut
Conseil de stabilité financière may temporarily limit surrender payments and defer or
restrict arbitrages [REG-R13]; the PER's *blocage* removes the surrender channel, so on
this product the power would reach the early-release and transfer legs and the glide-path
arbitrages — this document's reading, not a statement in the article.

**Taxation — and why it stays out of the projection.** C1 *versements* are deductible
from *revenu net global* under CGI art. 163 quatervicies, within a ceiling equal to the
greater of 10 % of the prior year's professional income capped at 8 PASS and 10 % of the
PASS, less professional retirement contributions already deducted or exempted
[R13] [R17] [REG-R42]; published figures are a €4 710 minimum and a €37 680 maximum, the
ceiling reduced by employer contributions to a PERCO/PERECO/PERO within a €7 419 exempt
limit [R18] [R20]. Those figures mix PASS vintages, so a model must parameterise the PASS
rather than hard-code either [research caveat 7], and the carry-forward is three years or
five depending on vintage — a conflict the official sources leave standing, hence
[unverified] [R13] [R17] [R18] [R20] [R21] [REG-R42]. From 1 January 2026 contributions
after the holder's 70th birthday are no longer deductible [R20] [R21]. **The holder may
decline the deduction, and that election is the pivot of the whole exit tax treatment**
[R19] [R20] [R21] [S7]: where contributions were deducted, a capital exit is taxed on the
contribution part at the progressive scale with no social levies and on the gains at the
flat rate, and an annuity as a pension after the 10 % abatement; where they were not, the
contribution part is exempt from both and the annuity is a *rente viagère à titre onéreux*
taxed on an age-graded fraction — 70 % under 50, 50 % at 50–59, 40 % at 60–69, 30 % at 70
and over [R20] [R21] [S7]. Social levies move from 17,2 % to **18,6 %** from 1 January
2026, taking the flat levy on gains from 30 % to **31,4 %**; the enacting instrument was
not retrieved and the rates are [unverified] [R20] [R21]. Capital from a PERIN is reported
on lines 1AI–1DI at ordinary income-tax rates, without the 7,5 % flat option or the
*quotient* available for PERP capital [R19]. **None of this changes the liability cash
flows this model projects.** The election alters what the holder keeps, not what the
insurer pays; the gross benefit is the same euro amount either way. The model projects
gross-of-tax amounts and carries `deduction_elected` on the model point purely so a
downstream tax layer can find it.

**Death taxation, and the age-70 cliff.** Death before 70 falls under CGI art. 990 I:
€152 500 abatement per beneficiary, then 20 % up to €700 000 and 31,25 % above
[R14] [REG-R41]. Death after 70 falls under art. 757 B, and the PER carve-out is explicit:
sums "dues … à raison du décès **après l'âge de soixante-dix ans du titulaire d'un plan
d'épargne retraite**" enter the inheritance-duty base **in their entirety**, not merely as
to premiums paid after 70, subject to a €30 500 global abatement across all contracts on
the same life [R15] [REG-R41]. The trigger is the **age at death**, not the age at which
each premium was paid — the opposite of ordinary assurance vie. Crossing 70 alive is a
cliff edge in a PER assurantiel, and it coincides with the age at which the *garantie
plancher* stops [S1] [S3] and, from 2026, with the age at which contributions stop being
deductible [R21].

**Prudential — cited, not specified.** PER commitments sit in a ring-fenced *comptabilité
auxiliaire d'affectation* under ACPR supervision [R8] [REG-R10]. Of the eleven statutory
technical provisions of art. R. 343-3, the *provision mathématique*, the *provision pour
participation aux bénéfices* and the *provision pour risque d'exigibilité* reach this
product [REG-R6] [REG-R7], and the *provision pour aléas financiers* mechanics remain live
even though the article carrying them was abrogated in 2016 [REG-R8]. Solvency II
technical provisions, SCR and risk margin [REG-R1] [REG-R2] [REG-R5] were not researched
for this product [unverified].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-per_assurance-r1
[R10]: #frlib-per_assurance-r10
[R11]: #frlib-per_assurance-r11
[R12]: #frlib-per_assurance-r12
[R13]: #frlib-per_assurance-r13
[R14]: #frlib-per_assurance-r14
[R15]: #frlib-per_assurance-r15
[R16]: #frlib-per_assurance-r16
[R17]: #frlib-per_assurance-r17
[R18]: #frlib-per_assurance-r18
[R19]: #frlib-per_assurance-r19
[R2]: #frlib-per_assurance-r2
[R20]: #frlib-per_assurance-r20
[R21]: #frlib-per_assurance-r21
[R22]: #frlib-per_assurance-r22
[R23]: #frlib-per_assurance-r23
[R24]: #frlib-per_assurance-r24
[R3]: #frlib-per_assurance-r3
[R4]: #frlib-per_assurance-r4
[R5]: #frlib-per_assurance-r5
[R6]: #frlib-per_assurance-r6
[R7]: #frlib-per_assurance-r7
[R8]: #frlib-per_assurance-r8
[R9]: #frlib-per_assurance-r9
[REG-R1]: #frlib-reg-r1
[REG-R10]: #frlib-reg-r10
[REG-R12]: #frlib-reg-r12
[REG-R13]: #frlib-reg-r13
[REG-R14]: #frlib-reg-r14
[REG-R15]: #frlib-reg-r15
[REG-R16]: #frlib-reg-r16
[REG-R17]: #frlib-reg-r17
[REG-R18]: #frlib-reg-r18
[REG-R2]: #frlib-reg-r2
[REG-R21]: #frlib-reg-r21
[REG-R22]: #frlib-reg-r22
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R29]: #frlib-reg-r29
[REG-R30]: #frlib-reg-r30
[REG-R31]: #frlib-reg-r31
[REG-R33]: #frlib-reg-r33
[REG-R34]: #frlib-reg-r34
[REG-R41]: #frlib-reg-r41
[REG-R42]: #frlib-reg-r42
[REG-R46]: #frlib-reg-r46
[REG-R5]: #frlib-reg-r5
[REG-R6]: #frlib-reg-r6
[REG-R7]: #frlib-reg-r7
[REG-R8]: #frlib-reg-r8
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
