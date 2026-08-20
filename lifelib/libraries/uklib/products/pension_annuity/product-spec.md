# Product Specification

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling. It does not describe any single insurer's product. Facts
carrying a source tag — [S#] (primary product documents) and [R#] (regulatory/actuarial
references), both numbered per `_research/pension-annuity.md` and resolved in
`sources.md` (same directory) — were extracted from the cited document. [REG-R#] tags
resolve against the cross-product reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering, distinct
from the product research file's; research provenance in
`_research/regulatory-actuarial.md`). Values marked **[std]** are standardizations
introduced for the reference implementation; each [std] table row carries a footnote
giving the rationale and the observed range across insurers. Facts the research file
could not verify are flagged [unverified]. The implementation anchor for mechanics is
one carrier's pension annuity — the "anchor carrier" of the footnotes below (Key
Features Document [S1]; Terms and Conditions [S2]).

---

## Product overview and market role

A pension annuity (individual immediate lifetime annuity) converts defined-contribution
pension savings into a guaranteed income payable for the annuitant's life: the insurer
pays a regular income for life in return for a one-off single premium of pension funds
[S1] [S2 §1.1] [S5 §3] [S6] [S9]. The statutory chassis is the "lifetime annuity" of
Finance Act 2004 Schedule 28 paragraph 3 — payable by an insurance company the member
had an opportunity to select, until death or the later of death and the end of a term
certain [R7]. Since 6 April 2015 the Taxation of Pensions Act 2014 permits decreasing
annuities and guarantee periods longer than ten years [R6] [R7]; the 30-year guarantee
periods in current products rely on this relaxation [S1] [S4] [S6] [S9]. The contract is
long-term insurance business Class I (life and annuity) under the RAO 2001 Sch 1
Part II [R8], and pension business under s.58 Finance Act 2012 (stated expressly in
one carrier's conditions) [S5 §14.11].

Annuities in payment are non-participating guaranteed business: one carrier states the
policy does not share in profits [S7 §7.9], and the other three carriers' contracts
contain no participation mechanics [S2] [S5] [S9] (that this holds market-wide is
[unverified]). There is no surrender value at any time [S1 p4] [S2 §12] [S5 cl.14.7]
[S7 §7.5] [S9 §3.9] — the feature that makes UK annuity books the canonical
matching-adjustment portfolios under Solvency UK [R1]. Enhanced (medically
underwritten) terms are standard market practice: one carrier underwrites individually
as standard [S4], and the other three all offer enhanced rates for health and lifestyle
factors [S1 p5] [S6] [S9]. Bulk purchase annuities (DB buy-ins/buy-outs) are the
institutional variation of the same liability mechanics [unverified — no BPA document
retrieved; see Variations].

This composite is built on the anchor carrier's pension annuity chassis [S1] [S2]. The
research comparison of four insurers ([S1] [S2]; [S4] [S5]; [S6] [S7]; [S9]) found that
the others differ mainly in parameter bounds and edge mechanics rather than structure,
so one cash-flow engine covers all four with configuration; the chassis choice is **[std]**.

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Single-premium immediate lifetime annuity, individual, non-participating | [S1] [S2 §1.1] [S7 §7.9] |
| Statutory definition | "Lifetime annuity", Finance Act 2004 Sch 28 para 3 | [R7] |
| Legal wrapper | Open Market Option purchase, or Immediate Vesting Personal Pension where the insurer pays the tax-free cash | [S2 §§1.5–1.6] |
| Business classification | Long-term insurance Class I; pension business (s.58 FA 2012, non-BLAGAB) | [R8] [S5 §14.11] [REG-R17] |
| Premium | One single premium; no additions after the start date (a further purchase is a new policy) | [S2 §1.1] [S7 §7.3] |
| Minimum purchase price | £10,000 after tax-free cash and adviser charges | [S1 p4]; composite **[std]** (1) |
| Minimum age at purchase | 55 | [S1 p5] (2) |
| Maximum age at purchase | 90 | [S9]; adoption as composite **[std]** (3) |
| Guarantee-period age limit | Annuitant no older than 100 at the end of the guarantee period | [S1 p10] [S2 §§6.5–6.6] |
| Currency / destination | GBP, paid to a UK bank account | [S2 §1.3] |
| Cooling-off | 30 days from confirmation the annuity has started; options cannot be changed afterwards | [S1 p7] [S2 §13] |
| Surrender value | None, ever | [S1 p4] [S2 §12] [S5 cl.14.7] [S7 §7.5] [S9 §3.9] |
| Anchor calibration point | £100,000 purchase at age 65 buying £6,657 p.a. with 50% value protection (KFD illustration, January 2026; frequency/timing/escalation basis not recorded) | [S1 p11] |

Footnotes to [std] rows:

1. Observed minimum purchase: £10,000 after tax-free cash at three of the four carriers
   [S1 p4] [S6] [S9]; the fourth instead requires at least £2,000 to remain to buy the
   annuity after any lump sums, with no £10k floor stated [S4]. The £10,000 floor is
   the modal rule.
2. Not [std], but note: one carrier states 55 rising to 57 from 6 April 2028 (or 50
   where allowed by law) [S4]; another allows any age for beneficiary annuities [S6].
3. Only one of the four carriers states a maximum issue age (55–90) [S9]; the other
   three state none in the retrieved documents [S1] [S4] [S6], with the anchor carrier
   constraining only the guarantee-period end (age ≤ 100) [S1 p10]. The composite
   adopts 90 so the model has a bounded issue-age domain.

### Income payment options

| Parameter | Representative value | Basis |
|---|---|---|
| Payment frequencies | Monthly, quarterly, half-yearly, yearly | [S1 p8] [S2 §2.2] |
| Payment timing | In advance or in arrears; arrears income is higher than advance | [S1 p8] [S2 §2.3] |
| Proportionate final payment | Arrears policies optionally "with proportion": pro-rata stub from last instalment to date of death; choosing it lowers starting income | [S1 p8] [S2 §4] |
| Escalation menu | nil (level) / fixed ≤ 10% compound / RPI (0-floor with catch-up) / LPI (RPI capped at 5%) | [S1 p8] [S2 §3.2]; menu selection **[std]** (4) |
| Fixed escalation bound | Any rate up to and including 10% p.a., compounded | [S1 p8] [S2 §3.2] |
| RPI measurement window | 12 months ending six months before the policy anniversary, applied on the anniversary | [S2 defs "Retail Prices Index"] |
| RPI floor and catch-up | If RPI falls, income is frozen; increases resume only once RPI exceeds its previous peak | [S2 defs] |
| LPI measurement | RPI capped at 5%, using the September RPI figure; floor 0% | cap/window [S2 §3.2, defs "LPI"]; 0-floor [S5 §7.1.4] [S9 §4.3]; harmonization **[std]** (5) |
| First increase | First policy anniversary | [S2 §3.3] |
| Snapshot escalation for the worked configuration | Fixed 3% p.a. | **[std]** (6) |
| Deterministic RPI assumption | 3.0% p.a. | **[std]** (7) |

4. The four-option menu drops the anchor carrier's RPI-capped-3% variant [S2 §3.2],
   another's pure RPI (income can decrease) and LPI-max-2.5% variants [S4]
   [S5 §§7.1.2, 7.1.5] and a third's LPI 2.5 [S6] [S7 defs]. All are parameterizations
   of the same indexation engine (cap/floor/catch-up parameters); the retained four
   span the mechanics.
5. Observed LPI definitions, one per carrier: RPI capped 5% using the September RPI
   figure [S2 defs "LPI"]; LPI max 5% over 1 October–30 September of the prior year,
   collar 0% [S5 §7.1.4]; RPI for the year ending September [S6] [S7 defs]; declared
   RPI for 1 October–30 September, floor 0 [S9 §4.3]. The composite takes cap 5%,
   floor 0%, September reference year, and no catch-up ratchet (catch-up is recorded
   only for the uncapped RPI option [S2 defs] [S9]).
6. Pure snapshot choice within the contractual range (the anchor carrier's ≤ 10%
   [S1 p8] [S2 §3.2]; 0.1%–10% at another carrier [S6]; a third's cap unstated
   [S4] [S5]). 3% keeps the worked example's escalation visible without dominating it.
7. Modeling assumption for projecting RPI-linked options; no source publishes an
   inflation basis. The RPI floor and LPI collar are inflation options whose value a
   deterministic path cannot capture (see technical notes).

### Death benefits — dependant's (joint-life) income

| Parameter | Representative value | Basis |
|---|---|---|
| Dependant's income percentage | Any percentage up to 100% of the annuitant's income; representative snapshot 50% | [S1 p9] [S2 §5.1]; snapshot **[std]** (8) |
| Dependant basis | Named dependant (named spouse / named financial dependant); "any spouse" variant out of representative scope | [S2 §§5.2–5.7]; scope **[std]** (9) |
| Overlap | With overlap (dependant's income and guarantee payments run together) or without (dependant's income starts at guarantee end); representative default: without overlap | [S1 p9] [S2 §§5.9–5.11]; default **[std]** (10) |
| Dependant amount base | Percentage of the higher of the income at death and the income at the end of the guarantee period; escalates on the same basis as the annuitant's income | [S2 §§5.12–5.13] |
| Dependant underwriting | The second life's health is underwritten and can attract an enhancement | [S6] [S9] |

8. All four insurers allow up to 100% [S1 p9] [S2 §5.1] [S4] [S6] [S7 §3.5.2];
   percentages are free-form at two of them [S1 p9] [S4]; a third quotes 50% as
   a typical example [S6]. Market-standard quoted levels of 50%/67%/100% are
   [unverified]. 50% matches that example [S6] and the anchor's VP% so the
   VP-plus-dependant constraint binds exactly at 100%.
9. Observed bases, one per carrier: named spouse / any spouse (married at least the
   last six months and not 10+ years younger) / named financial dependant
   [S2 §§5.2–5.7]; named individual (survives divorce) or spouse-at-death, with an
   actuarial reduction where the survivor is more than 10 years younger [S7 §§3.5.1,
   3.5.5]; named, absolute or conditional on FA 2004 Sch 28 para 15 dependence
   [S9 §4.6]; named dependant aged 40+ [S4] [S5 §6.1]. A named dependant with
   attributes fixed at outset is the only basis a single-policy model point can carry
   without marriage-state modeling.
10. Both forms are offered by all four insurers [S1 p9] [S2 §§5.9–5.11] [S4]
    [S5 §6.2.2] [S6]. "Without overlap" is the default here because it exercises the
    guarantee/dependant interaction; the overlap flag is a model-point attribute.

### Death benefits — guarantee period and value protection

| Parameter | Representative value | Basis |
|---|---|---|
| Guarantee period range | 1–30 years from the start date; representative default 10 years | [S1 p10] [S2 §§6.5–6.6]; default **[std]** (11) |
| Guarantee form | Remaining instalments continue to beneficiaries/estate at the level as if the annuitant were alive (escalation continues); insurer discretion over recipients | [S2 §6.3] [S7 §4.2]; commutation out of scope **[std]** (12) |
| Value protection (VP) | Lump sum on death = max(0, VP% × purchase price − gross instalments already paid); any VP% up to 100%; representative snapshot 50% | [S1 p11] [S2 §7]; snapshot **[std]** (13) |
| VP trigger basis | On the annuitant's death or on the last survivor's death, chosen at outset; first-death basis costs more | [S1 p11] [S2 §7.3] [S5 §8.4] [S7 §4.3] |
| VP + dependant constraint | VP% + dependant's income % ≤ 100% where VP is paid on the annuitant's death (not on last-survivor basis) | [S2 §7.3] [S4] |
| Guarantee vs VP | Mutually exclusive: a policy has a guarantee period XOR value protection | [S2 §§6.7, 7.6] [S4]; representative rule **[std]** (14) |
| No death benefit selected | Payments stop on death; nothing else is payable | [S1 p6] [S4] [S6] [S9] |
| VP exclusions | Not available on GMP or Section 9(2B) rights; may be limited for the most severe medical conditions | [S2 §7.7] [S4] |

11. Observed ranges, one per carrier: 1–30 years with the age-100 limit [S1 p10]
    [S2 §§6.5–6.6]; 1–30 years [S4]; one month to 30 years [S6]; one year as
    standard, extendable to 30 (capped at 10 where the annuity originates from a DB
    scheme) [S9]. 10 years is a round mid-range default; the model takes the period
    as an input in whole months.
12. One carrier offers a "lump sum basis" guarantee paying the balance of instalments
    [S5 §4.3.2] and another a commuted lump sum (death before 75) discounted at a set
    rate, currently 0.75% compounded [S9 §4.5]; the remaining two pay only
    continuing instalments [S2 §6] [S7 §4.2]. The composite pays continuing
    instalments only.
13. VP% is free-form up to 100% at two of the carriers [S1 p11] [S9]; a third protects
    a percentage of the fund after PCLS and any taxable lump sum [S5 §8.3]; the fourth
    nets off annuitant instalments, guarantee payments due (excluding future RPI/LPI
    increases) and second-annuitant instalments [S7 §4.3]. 50% matches the anchor
    illustration [S1 p11]. The representative formula nets *gross instalments paid*
    (the anchor carrier's form [S1 p11] [S2 §7]).
14. Two of the four carriers: either a guarantee period or value protection, not both
    [S2 §§6.7, 7.6] [S4]. A third's provisions net guarantee payments off the VP lump
    sum, implying the two can coexist [S7 §4.3]; the fourth's extended VP replaces the
    standard one-year guarantee [S9]. The XOR rule is the modal design and keeps the
    death benefit state machine simple; the netting variant [S7 §4.3] is documented
    under Variations.

### Underwriting, charges, tax

| Parameter | Representative value | Basis |
|---|---|---|
| Enhanced/impaired terms | Health and lifestyle rating (smoking, blood pressure, serious conditions; questionnaire, no medical exam); modeled as a mortality rating overlay (qx multiplier or rated age), not a structural variant | existence [S1 p5] [S4] [S6] [S9]; overlay representation **[std]** (15) |
| Mis-statement remedy | Income may be reduced (not below the standard rate) and overpayments reclaimed if medical/lifestyle information is not confirmed | [S1 p4]; interest at BoE base +1% under one carrier's provisions [S7 §3.4] — context, not modeled |
| Explicit charges | None; set-up and administration are priced into the annuity rate | [S1 p6] [S4] [S6] [S9] |
| Adviser charges | Deductible from the premium, shown on the quote; commission priced into rates | [S1 p12] [S4] [S6] [S9] |
| Income tax | Taxed as earned income under PAYE | [S1 p5] [S2 §8] |
| Tax-free cash (context) | PCLS up to 25% of the pot before purchase, capped by the Lump Sum Allowance £268,275; taken before the annuity starts | [S1 p6] [S4] [S6] |
| Death benefit tax | Death before 75: dependant's income normally income-tax-free, lump sums tax-free within the LSDBA £1,073,100; at/after 75: recipient's marginal rate | [S1 p11] [S2 §8] [S4] [S6] |
| IHT (announced) | From 6 April 2027 remaining guarantee-period income and VP lump sums are intended to fall within the estate (not where a dependant's income was chosen, per one carrier's summary); announced-but-not-enacted | [S1 p11] [S4] |
| FSCS | 100% of a valid claim, no upper limit | [S1 p15] [S4] [S6] [S9] |

15. All four insurers price on health and lifestyle [S1 p5] [S4] [S6] [S9]; one is
    individually underwritten as standard [S4]. Enhanced terms change the mortality
    basis, not the contract mechanics, so the reference model represents enhancement
    as a rating overlay (multiplier θ on qx, or a rated-age offset — see technical
    notes); the overlay form itself is a modeling standardization (insurers' rating
    factor structures are not public; the anchor carrier's underwriting guide was
    located but not extracted).

---

## Contractual mechanics

### Premium and establishment

One single premium P is paid from pension funds (after any PCLS and adviser charges);
no money can be added after the start date [S2 §1.1] [S7 §7.3]. Funds arrive via the
Open Market Option (the ceding scheme pays tax-free cash) or an Immediate Vesting
Personal Pension (the insurer pays it) [S2 §§1.5–1.6]. Within the 30-day cancellation
window the contract can be unwound (income received must be repaid; a paid PCLS cannot
be reversed) [S1 p7] [S2 §13] [S4]; after it, options are fixed for life [S1 p4] [S4].

### Income payments

Let A(y) be the annualized income in policy year y and m ∈ {12, 4, 2, 1} the payment
frequency [S1 p8] [S2 §2.2]. Each instalment is

    inst = A(y) / m

paid in advance (first payment on/just after the start date) or in arrears (first
payment at the end of the first payment period) [S1 p8] [S2 §2.3]. Arrears policies
"with proportion" pay a final pro-rata stub from the last instalment date to the date
of death; "without proportion" pays nothing for that stub [S1 p8] [S2 §4]. Payments due
on non-working days are made at least one working day early [S2 §2.4] (ignored in the
model **[std]**).

### Escalation

Applied on each policy anniversary, first on the first anniversary [S2 §3.3]:

- **Level:** A(y+1) = A(y) [S1 p8].
- **Fixed:** A(y+1) = A(y) × (1 + g), g ≤ 10% [S1 p8] [S2 §3.2].
- **RPI with 0-floor and catch-up** [S2 defs]: let I(k) be the RPI reference level for
  anniversary k (the index measured over the 12 months ending six months before the
  anniversary [S2 defs]) and peak(k) = max(I(0), ..., I(k)). Then

      A(y+1) = A(y) × max(1, I(y) / peak(y−1))

  — income never falls; after a fall in RPI it stays frozen and increases resume only
  once the index exceeds its previous historical peak [S2 defs]. (A second carrier
  operates the same held-level-with-catch-up rule on its uncapped RPI option [S9].)
- **LPI (RPI capped 5%)** [S2 §3.2]:

      A(y+1) = A(y) × (1 + min(5%, max(0%, rpi_Sep(y))))

  where rpi_Sep(y) is the September-year RPI change [S2 defs "LPI"]; the 0% floor is
  explicit at two other carriers [S5 §7.1.4] [S9 §4.3] and harmonized here **[std]**
  (spec footnote 5). No catch-up ratchet applies to LPI **[std]**.

If any escalation option is chosen, the starting income is lower than the level-income
equivalent for the same premium [S1 p8] [S4] [S6].

### Dependant's income (joint life)

If chosen, on the annuitant's death a named dependant receives δ × the annuitant's
income for the dependant's remaining life, δ ≤ 100% [S1 p9] [S2 §5.1], escalating on
the same basis [S2 §§5.12–5.13]. Where a guarantee period is also in force, the
dependant's income starts at the annuitant's death ("with overlap": both streams run
during the remaining guarantee; lower starting income) or at the end of the guarantee
period ("without overlap") [S1 p9] [S2 §§5.9–5.11]. The percentage applies to the
higher of the income at death and the income at the end of the guarantee period
[S2 §5.12] — under non-decreasing escalation this equals the income "as if alive" at
the start date of the dependant's stream (see technical notes). If the dependant dies
first, the annuitant's income is unchanged and no dependant benefit is ever paid
[S2 §5].

### Guarantee period (guaranteed minimum payment period)

Income continues for a chosen term of 1–30 years from the start date even if the
annuitant dies within it, with the annuitant no older than 100 at the period end
[S1 p10] [S2 §§6.5–6.6]. Remaining instalments go to nominated beneficiaries or the
estate at the insurer's ultimate discretion [S2 §6.3] [S5 §4.3.3] [S7 §4.1], and
continue "at the same level as if the annuitant was still alive" — escalation
continues [S7 §4.2]. The guarantee is an annuity-certain floor independent of
survival; it is mutually exclusive with value protection [S2 §§6.7, 7.6] [S4].

### Value protection

A lump sum payable on death (annuitant's death or last survivor's death, chosen at
outset [S1 p11] [S2 §7.3] [S5 §8.4]):

    VP lump sum = max(0, v × P − G(death))

where v is the protected percentage (≤ 100%), P the purchase price, and G(death) the
gross instalments already paid at death [S1 p11] [S2 §7]. On the first-death basis
combined with a dependant's income, v + δ ≤ 100% [S2 §7.3] [S4]. VP is not available on
GMP or Section 9(2B) rights [S2 §7.7].

### No surrender, assignment, alteration

The annuity has no cash-in value and cannot be sold, transferred or commuted [S1 p4]
[S2 §12] [S5 cl.14.7] [S7 §7.5] [S9 §3.9]. The only exceptions are statutory: pension
sharing on divorce/dissolution (Welfare Reform and Pensions Act 1999) and Proceeds of
Crime Act 2002 orders [S2 §12.1]; analogous carve-outs exist at the other insurers
[S5 §14.4] [S7 §3.5.6] [S9 §3.9]. There are no paid-up or alteration terms — the
contract is fully paid [S2] [S5] [S7] [S9]. The absence of policyholder options is
precisely matching-adjustment eligibility condition 2.2(4) [R1].

### Contracted-out benefits (GMP / Section 9(2B)) — described, out of model scope

Where the purchase money includes contracted-out rights, statutory minima attach:
survivor minima (50% of GMP to a widow; 50% of post-88 GMP to a widower/civil partner)
[S7 §3.5.4] [S5 §§6.3–6.5] [S9], escalation minima (post-88 GMP at RPI capped 3% from
April/May dates) [S2 §3.3] [S5 §7.2], restriction of benefits to a spouse/civil partner,
and no value protection [S2 §§5.6, 7.7]. The reference model excludes GMP/S9(2B)/COSR
tranches **[std]** (see technical notes).

---

## Riders and options

A pension annuity has no riders in the US sense; the death-benefit and indexation
options above are elected at outset, priced into the annuity rate [S1 p6], and
immutable after the cancellation period [S1 p4] [S4] [S6] [S9].

**In scope (the representative option set):** payment frequency and timing (with the
proportionate final payment option) [S1 p8] [S2 §§2, 4]; the four-option escalation
menu (spec footnote 4); dependant's income δ ≤ 100% with/without overlap [S1 p9]
[S2 §5]; guarantee period 1–30 years XOR value protection with v + δ ≤ 100% on the
first-death basis [S2 §§6–7] [S4]; enhanced underwriting as a rating overlay [S1 p5]
[S4] [S6] [S9].

**Out of scope (listed for completeness):**

- Taxable lump sum at outset alongside PCLS, with ≥ £2,000 retained (one carrier;
  triggers the MPAA) [S4] [S5 §10].
- Lump-sum commutation of the remaining guarantee on death (one carrier: balance of
  instalments [S5 §4.3.2]; another: discounted at a set rate, currently 0.75%
  compounded, death before 75 [S9 §4.5]).
- One carrier's automatic 90-day value protection and extended-VP-replaces-guarantee
  mechanics [S9].
- "Any spouse" and spouse-at-death dependant bases with marriage-condition tests
  [S2 §§5.2–5.7] [S7 §3.5.1].
- GMP / Section 9(2B) / COSR benefit tranches and scheme maximum-benefit mechanics
  [S2 §§3.3, 9] [S5 §§4, 6.3–6.5, 7.2] [S9 §4.4].
- Scheme Pension and Immediate Vesting Pension wrappers as separate forms [S5 §1.2] [S6].
- Beneficiary's/dependant's annuities bought with inherited funds (any age, no death
  benefit options) [S6] [S7].
- Fixed-term annuities (income for a set term plus a guaranteed maturity amount) — a
  distinct product not covered by the retrieved documents [unverified].
- Bulk purchase annuities — institutional variation, see below.

---

## Variations across insurers

| Feature | Carrier A [S1] [S2] | Carrier B [S4] [S5] | Carrier C [S6] [S7] | Carrier D (2019/20) [S9] |
|---|---|---|---|---|
| Minimum purchase | £10,000 after TFC | ≥ £2,000 must remain | £10,000 after TFC | £10,000 after TFC |
| Age at purchase | 55+ (no stated max) | 55+ (57 from 2028) | 55+ (any age, beneficiary annuity) | 55–90 |
| Fixed escalation | ≤ 10% | fixed % (cap unstated) | 0.1%–10% | fixed rate |
| RPI options | RPI (0-floor + catch-up), RPI cap 3%, LPI cap 5% | pure RPI (may decrease), RPI 0-floor, LPI 5%, LPI 2.5% | RPI (may decrease), LPI 5, LPI 2.5 | RPI (0-floor + catch-up), RPI capped |
| Guarantee period | 1–30 yrs; ≤ age 100 at end | 1–30 yrs | 1 month–30 yrs | 1 yr standard; ≤ 30 (10 if DB-sourced) |
| Guarantee vs VP | either, not both | either, not both | combinable (VP nets off guarantee payments) | extended VP replaces standard guarantee |
| Guarantee commutation on death | no | yes (balance of instalments) | no | yes (discounted at 0.75%) |
| Distinctive | proportionate payment option; IVPP wrapper | taxable lump sum at outset; individually underwritten as standard | modular benefit-elements architecture; £1m enhanced premium cap | 90-day automatic VP; £40 rewrite charge; overseas payment charge £2.74 |

Carrier A–D are stable labels for the four surveyed carriers, keyed by the source tags
in the header row and used only in this section; Carrier A is the "anchor carrier"
of the sections above [S1] [S2].

Why the representative choices were made:

1. **Chassis.** Carrier A's product is the cleanest structural representative; the
   others differ in parameter bounds and edge mechanics, so one engine parameterized
   per the tables above covers all four (research conclusion; adoption **[std]**).
2. **Escalation menu.** All observed indexation options are cap/floor/catch-up
   parameterizations of one indexation rule; the composite keeps nil / fixed / RPI
   (floor + catch-up) / LPI-5 and treats the rest as parameter settings (spec
   footnotes 4–5).
3. **Guarantee XOR VP.** The modal rule (Carriers A and B) [S2 §§6.7, 7.6] [S4].
   Carrier C's combinable design instead nets annuitant instalments, guarantee payments
   due (excluding future RPI/LPI increases) and second-annuitant instalments off the
   VP lump sum [S7 §4.3] — implementable in the same engine by extending the G(t)
   accumulator; documented, not defaulted.
4. **Guarantee as instalments.** Commutation variants (Carrier B's lump-sum basis,
   Carrier D's discounted commutation) change the timing but not the undiscounted
   amount of the guarantee obligation and are excluded (spec footnote 12).
5. **Enhanced underwriting.** A rating overlay at every insurer, never a structural
   variant [S1 p5] [S4] [S6] [S9]; Carrier C's £1,000,000 aggregate enhanced-premium
   re-rating right [S7 §6] is an underwriting control, not a cash-flow mechanic.
6. **Carrier D vintage caveat.** The Carrier D evidence is the 10/2019 KFD + 02/2020
   terms retrieved via a third-party mirror [S9]; the current editions (S10, S11) sit
   behind a host that returns HTTP 403 to automated fetches and are kept as known
   references only. Structural features are stable but Carrier D's own details (e.g.
   whether the 90-day standard VP persists) are unconfirmed, and S9's tax content
   predates the 2024 LSA/LSDBA regime.
7. **Institutional variation.** Bulk purchase annuities (buy-ins/buy-outs) transfer
   DB scheme liabilities to insurers; major writers include three of the four carriers
   surveyed here and other specialist bulk annuity writers [unverified — no BPA
   document retrieved]. The individual-annuity mechanics here (GMP tranches, LPI
   escalation, scheme maxima) mirror BPA benefit structures [S2 §9] [S5 §§4–7], so the
   same engine extends to BPA benefit tranches.

---

## Regulatory context

**PRA / Solvency UK.** Technical provisions are a best estimate plus risk margin, the
best estimate being the probability-weighted average of future cash flows discounted
at the risk-free term structure [REG-R1] — exactly what the companion technical notes
project. Annuity liabilities are the canonical matching-adjustment business: MA
eligibility requires (inter alia) no future premiums, underwriting risk limited to
longevity/expense/revision/mortality/recovery-time risk, best estimate not increasing
by more than 5% under the prescribed mortality stress (the worse of +15% level or
+0.15pp additive), and no policyholder options beyond a bounded surrender option, with
MA permission required before use [R1]. The 2023–24 Solvency UK reforms (consulted in
CP19/23 [R2], delivered by PS10/24, effective 30 June 2024) admitted
highly-predictable-cash-flow assets, expanded liability eligibility, introduced the
annual MA attestation and the MALIR return [R2] [REG-R5] [REG-R2]; supervisory
expectations, including the cash-flow matching tests, live in SS7/18 (current version
October 2025) [REG-R8]. The risk margin uses a 4% cost-of-capital rate with a
life-business tapering factor λ = 0.9 (floor 0.25) per SI 2023/1346 [REG-R4].

**FCA conduct.** COBS 19.9 (the "annuity information prompt") applies to firms giving
retail clients a guaranteed pension annuity quote: the firm must generate a
market-leading quote by searching the whole market, ask health and lifestyle questions
to test enhanced-annuity eligibility, and present prescribed comparator information
(cost, annual income, guarantee period, frequency/timing, single vs joint, escalation
basis) with warnings on guaranteed annuity rates, GMP and section 9(2B) rights
[R5]. The KFD disclosure-and-cancellation regime and Pension Wise signposting appear
in every sampled KFD [S1] [S4] [S6] [S9]. Conduct rules shape the point of sale, not the
in-force cash flows.

**Tax.** Annuity income is taxed as earned income under PAYE [S1 p5] [S2 §8] [S4] [S6]
[S9]. The product sits in the Finance Act 2004 pensions tax framework (Sch 28
lifetime-annuity definition [R7]) as amended by the Taxation of Pensions Act 2014
(pension freedoms: annuitization optional, flexible death benefits, MPAA) [R6]. For
the insurer, pension annuities are pension business — non-BLAGAB, taxed on trade
profits rather than I-E [REG-R17] [S5 §14.11] — so policyholder-level fund tax does not
enter the liability cash flows. Death benefit taxation splits at age 75 (pre-75
tax-free within the LSDBA £1,073,100; post-75 at the recipient's marginal rate)
[S1 p11] [S4] [S6], and the announced IHT inclusion of guarantee-balance and VP death
benefits from 6 April 2027 is not yet enacted [S1 p11] [S4]. Protection of last resort
is FSCS at 100% with no upper limit [S1 p15] [S4] [S6] [S9].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uklib-pension_annuity-r1
[R2]: #uklib-pension_annuity-r2
[R5]: #uklib-pension_annuity-r5
[R6]: #uklib-pension_annuity-r6
[R7]: #uklib-pension_annuity-r7
[R8]: #uklib-pension_annuity-r8
[REG-R1]: #uklib-reg-r1
[REG-R17]: #uklib-reg-r17
[REG-R2]: #uklib-reg-r2
[REG-R4]: #uklib-reg-r4
[REG-R5]: #uklib-reg-r5
[REG-R8]: #uklib-reg-r8
[std]: #uklib-std
[unverified]: #uklib-unverified
<!-- END generated citation links -->
