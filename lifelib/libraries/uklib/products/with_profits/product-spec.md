# Product Specification

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling. It does not describe any single insurer's product or fund.
Facts carrying a source tag — [S#] (primary product/firm documents) and [R#]
(regulatory/actuarial references), both numbered per `_research/with-profits.md` and
resolved against `sources.md` in this directory — were extracted from the cited
document. [REG-R#] resolves against the cross-product reference library
`references/regulatory-and-actuarial-references.md` (its own R-numbering; research
provenance in `_research/regulatory-actuarial.md`). Values marked **[std]** are
standardizations introduced for the reference implementation; each [std] table row
carries a footnote giving the rationale and the observed range across insurers.
Facts the research file could not confirm against a retrieved document are flagged
[unverified]. The mechanics anchors are the published PPFMs of three proprietary
insurers [S1] [S4] [S5]; the with-profits fund documented in the first of these is
called *the anchor fund* below. The modern smoothed-fund variation is anchored to the
PruFund PPFM, customer guide and policy provisions [S2] [S9] [S11].

---

## Product overview and market role

With-profits business is participating long-term insurance in which premiums are pooled
in a with-profits fund and policy payouts combine guaranteed benefits with discretionary
bonuses. Two bonus types are universal: **regular** (annual/reversionary) bonuses, which
increase guaranteed benefits and become a contractual right only once added, and a
**final** (terminal) bonus payable at claim [S1]. The fairness benchmark for payouts is
the **asset share** — a retrospective accumulation, per policy or specimen policy, of
premiums and investment return less expenses, tax, risk and guarantee charges and
shareholder transfers [S1] [S4] [R8]. The exercise of discretion is governed by each
firm's published Principles and Practices of Financial Management (PPFM) [R2], with
FCA conduct rules setting target-range, smoothing and market value reduction (MVR)
constraints [R1] and a With-Profits Committee and With-Profits Actuary overseeing the
discretion [R4] [R5].

Three liability chassis coexist in the UK market [S1] [S4]: (a) **conventional**
(traditional) with-profits — a basic sum assured (the minimum maturity amount) to which
declared bonuses are added [S1]; (b) **unitised** (accumulating) with-profits — premiums
buy units whose price rises with declared regular bonuses, with a final bonus at
encashment and MVR machinery on non-guaranteed exits [S1] [S4]; and (c) **smoothed
funds** (PruFund-style) — no bonus declarations; the unit price grows daily at a
published Expected Growth Rate with rule-based adjustments toward the unsmoothed net
asset value [S2] [S9] [S11]. Under the Regulated Activities Order, conventional
with-profits assurances and annuities fall in Class I (life and annuity), with
unitised/linked structures typically involving Class III [R9; per-product allocation
unverified](#uklib-with_profits-r9).

Most conventional and unitised with-profits funds are legacy books: one consolidator
alone runs 18 internally segregated funds inherited from many acquired offices [S4], and
most UK conventional funds are closed to new business [unverified as a market-wide
statement]. Documented open with-profits business today comprises smoothed funds (the
PruFund range, currently marketed [S10] [S13]), mutuals (one with an open fund [S7],
another distributing profits annually [S6]), friendly societies (with-profits
ISAs [S12]) and new niche forms (credit-matched with-profits, added 2026 [S1] [S3]).

This specification standardizes a single composite: a **proprietary 90:10 with-profits
fund** carrying two product chassis — a **unitised with-profits bond** (primary cell,
representative of the largest open/recently-open retail block) and a **conventional
with-profits endowment** (legacy cell) — with the PruFund-style smoothed fund and the
mutual profit-distribution model described as variations.

---

## Representative specification

### Fund structure and profit sharing

| Parameter | Representative value | Basis |
|---|---|---|
| Fund type | Proprietary with-profits sub-fund within a long-term fund; ring-fenced | [S1] [R6]; choice **[std]** (1) |
| Profit sharing basis | 90:10 — at least 90% of divisible profit distributed to policyholders, balance to shareholders | [S1] [S8] |
| Shareholder transfer | 10% of each distribution = one-ninth of the cost of bonus declared/paid; charged to asset shares | equivalence and charging **[std]** (2); components [S1] [S5] [S8] [R1] |
| Distribution floor | Policyholder share not less than the "required percentage"; shareholder transfers reduced proportionately if adjustments (MVRs, bonus cuts) reduce policyholder distributions below the required percentage | [R1] |
| Estate (inherited estate) | Residual working capital of the fund; supports smoothing, guarantees and investment freedom; no distribution expectation in the base model | [S1]; base-model treatment **[std]** (3) |
| New business status of composite | Conventional cell closed; unitised and smoothed cells open | [S4] [S10] [S13]; composite **[std]** (4) |

Footnotes to [std] rows:

1. Proprietary 90:10 is the representative historical design: the anchor fund
   distributes at least 90% of divisible profit to policyholders [S1]; at another
   proprietary insurer shareholders currently receive 10% of distributed surplus
   [S5]; the consumer statement is "up to 10%" to shareholders [S8]. Variants
   observed: 100:0 classes and defined-charge (DCPSF) structures in the anchor fund's
   own long-term fund [S1] [S2]; two mutuals with no shareholder [S6] [S7]. That 90:10
   is the typical proprietary basis generally is [unverified]; the COBS 20.2.17R
   "required percentage" floor was not separately captured
   [R1 note](#uklib-with_profits-r1).
2. One-ninth is the arithmetic restatement of 90:10 — if policyholders receive a bonus
   cost of 90 units, shareholders receive 10 = 90/9. Charging the transfer to asset
   shares follows one insurer's documented practice [S5] and the PRA retrospective
   asset-share item list [R8]. The measurement basis for "cost of bonus" varies by
   firm and is not fully recorded in the retrieved PPFMs; the reference measurement is
   defined in `technical-notes.md` as **[std]**.
3. Observed estate behavior ranges from no-distribution working capital (the anchor
   fund [S1]) to active distribution (reattribution special bonuses at another
   proprietary insurer [S5]; an annual mutual profit distribution [S6]; excess-surplus
   unit price enhancements in the anchor fund [S1] [S2]) and estate-floor triggers (one
   consolidated closed fund's estate ≥0.5% of aggregate asset shares [S4]). The base
   model holds the estate as a residual with no scheduled distribution; COBS 20.2.21R
   requires at least annual excess-surplus determination [R1].
4. Mirrors the market split: consolidated closed conventional books [S4] [S5] against
   currently marketed unitised/smoothed business [S10] [S12] [S13].

### Chassis A — unitised with-profits bond (primary cell)

| Parameter | Representative value | Basis |
|---|---|---|
| Product form | Single-premium, whole-of-life unitised with-profits investment bond | [S4] [S10]; choice **[std]** (5) |
| Issue ages (lives assured) | 3 months to 85 (age next birthday) at outset | [S10]; adoption **[std]** (6) |
| Minimum premium | £10,000 single premium; top-ups permitted (minimum £10,000) | [S10]; adoption **[std]** (6) |
| Premium allocation rate | 100% of premium buys units | proportion-less-charges design [S4]; 100% **[std]** (7) |
| Regular bonus delivery | Unit price increases daily at the equivalent of the declared annual rate; unit price never falls (declared bonus ≥ 0) | [S1] [S4] |
| Snapshot regular bonus rate | 2.00% p.a. | **[std]** (8) |
| Annual management charge (AMC) | 1.00% p.a. of asset share, deducted from credited return | percentage-of-asset-share application [S5]; rate **[std]** (9) |
| Guarantee/smoothing charge | 0.10% p.a. of asset share, deducted from credited return; lifetime cumulative deduction capped at 2% of asset shares | cap [S1]; annual rate **[std]** (10) |
| Death benefit | 101% of (unit face value plus any final bonus); MVR never applies on death | 101% **[std]** (11); no-MVR-on-death [S5] |
| MVR-free guarantee date | 10th policy anniversary (full encashment free of MVR) | [S4]; single-date choice **[std]** (12) |
| MVR-free regular withdrawals | Up to 5% p.a. of the original premium | **[std]** (13) |
| Surrender benefit | Unit face value + final bonus − MVR (see Contractual mechanics) | [S1] [S4] [S5] [R1] |
| Anchor model cell | £25,000 single premium, male, age 55 at entry, units purchased at £1.0000 | **[std]** (14) |

5. Single-premium whole-of-life bonds with guarantee dates are the documented unitised
   retail shape (one consolidator: "single-premium bonds: whole-of-life; some have
   guarantee dates at which encashment is MVR-free" [S4]); the currently marketed
   retail bond is the same wrapper on PruFund [S10]. A regular-premium unitised
   endowment/pension is the same recursion with a premium vector (supported by the
   technical notes).
6. Adopted from the currently marketed retail bond [S10] — the only such limits
   retrieved; closed-book originals are unpublished (research gap 4).
7. PPFMs state that "a proportion of each premium less charges" buys units [S4] without
   publishing allocation rates; 100% allocation with explicit AMC is the cleanest
   composite and matches modern single-premium practice [S10 charges structure].
8. Current declared bonus rates are not collected in the research file (they live in
   annual bonus declarations, not PPFMs — research gap 3). 2.00% is a pure modeling
   snapshot chosen below the composite fund-return assumption (5.0% p.a., technical
   notes) so that a substantial final-bonus proportion emerges, per the PPFM bonus
   philosophy [S1].
9. Observed levels: 1% p.a. expense-charge cap on many pension contracts in the anchor
   fund since April 2001 [S1]; a 1% p.a. total charge restriction for certain
   pre-Dec-2000 unitised business at another proprietary insurer [S5]. Modern PruFund
   bonds charge less (0.30%–0.575% tiered AMC [S10]); 1.00% is representative of the
   legacy unitised block.
10. The anchor fund caps the total lifetime guarantee/smoothing deduction for most
    traditional WP policies at 2% of asset shares, built up gradually (4% for
    post-March-2019 AVCs) [S1]. Other observed forms: a 0.7% p.a. unit charge for the
    first 10 years on certain products [S5]; conditional deficit-triggered charges
    capped at 10%/25% of asset shares in one consolidated closed fund [S4]; a charging
    ladder of 1.0% p.a. with a 7.0% lifetime cap in another [S4]; a charge taken by
    deduction or reduced credited return at a mutual [S6]. A level 0.10% p.a. against
    the [S1] 2% lifetime cap is the composite.
11. Observed death benefits: 100.1% of bid value of units (the currently marketed
    retail bond) [S10] [S11]; 101% guarantee on net money paid in (a friendly society's
    with-profits ISA) [S12]. 101% of unit face value is adopted as the round composite.
12. Observed MVR-free points: contractual guarantee dates varying by tranche, with no
    (or limited) MVR at the 10th policy anniversary for with-profits bonds in one
    consolidated fund [S4]; MVR-free guarantee periods in the anchor fund [S1];
    policy-condition dates at another proprietary insurer [S5]; one mutual tapers the
    MVR to zero at selected retirement date [S7]. A single 10th-anniversary guarantee
    date is the minimal composite.
13. Taken from one consolidator ("some policies allow small regular encashments
    MVR-free" [S4]) and sized to the familiar 5% p.a. tax-deferred withdrawal
    allowance for UK bonds [S10] [REG-R15]. The 5% MVR-free level itself is a
    standardization.
14. Pure modeling choice; used in the technical-notes worked example (year-6 state:
    asset share £30,000, unit price £1.104081 after five 2.00% declarations).

### Chassis B — conventional with-profits endowment (legacy cell)

| Parameter | Representative value | Basis |
|---|---|---|
| Product form | Regular-premium with-profits endowment assurance, closed to new business | [S1] [S4] [S8]; anchor **[std]** (15) |
| Term / anchor cell | 25 years; male, age 35 at entry | **[std]** (15) |
| Basic sum assured (SA) | £20,000 — the minimum maturity amount before bonuses | role [S1]; amount **[std]** (15) |
| Premium | £60 per month, level, payable throughout the term | **[std]** (15) |
| Reversionary bonus form | Compound: declared rate applied to SA + attaching bonuses | form [unverified] convention; choice **[std]** (16) |
| Snapshot reversionary bonus rate | 1.50% p.a. compound | **[std]** (16) |
| Bonus hardening | A regular bonus becomes a contractual right only once added; guaranteed at maturity and death only | [S1] [S8] |
| Interim bonus | Claims between declarations accrue interim bonus at the last declared rate | practice [S1] [S7]; rate equality **[std]** (17) |
| Death benefit | SA + attaching reversionary bonuses + interim bonus + any final bonus | [S4] [S8] |
| Maturity benefit | SA + attaching reversionary bonuses + terminal bonus | [S1] [S4] [S8] |
| Terminal bonus | max(0, smoothed target payout − guaranteed benefit) at claim | principle [S1] [S4]; formalization **[std]** (18) |
| Surrender value | Formula-based on SA + bonuses, parameters reviewed annually to target asset shares | [S1] [S5]; parametrization **[std]** (19) |

15. Original conventional policy conditions (issue-age ranges, premium tables) are not
    republished for closed books — a recorded research gap (gap 4). The 25-year
    endowment on a 35-year-old male with SA £20,000 and £60/month is a pure modeling
    anchor shaped like the classic mortgage-endowment sale; the premium level is not a
    priced value.
16. The retrieved PPFMs describe bonus additions generically; explicit
    compound/super-compound classification per product was not found and is flagged
    [unverified] in the research file (which records that UK conventional bonuses are
    commonly compound or super-compound as an unverified convention). Compound form is
    chosen as the simpler standard; the rate 1.50% is a snapshot standardization (bonus
    declarations not collected — research gap 3).
17. Interim bonus rates are set as the best estimate of the next declaration (one
    mutual sets them annually [S7]; the anchor fund applies interim rates between
    declaration and claim [S1]); equating the interim rate to the last declared rate is
    the modeling simplification.
18. The anchor fund sets final bonus by reference to asset shares of sample policies
    subject to smoothing [S1]; one consolidator pays guaranteed benefits plus any final
    bonus [S4]. The max(0, ·) formalization makes the guarantee floor explicit.
19. In the anchor fund, conventional surrender values are formula-based with parameters
    set to broadly target asset shares over the long term, based on sum assured,
    regular bonus and final bonus, reviewed normally annually [S1]; another
    proprietary insurer reviews surrender bases when market indicators move 5% [S5].
    The reference parametrization (clamped asset-share targeting) is defined in
    `technical-notes.md`.

### Bonus framework (both chassis)

| Parameter | Representative value | Basis |
|---|---|---|
| Declaration frequency | Annual, for the forthcoming bonus year; final bonus scales normally reviewed yearly, ad hoc reviews after large market moves | [S1] [S4] [S5] |
| Regular bonus change discipline | Changes not expected to exceed ±1.00% p.a. in normal circumstances; zero declaration permitted; no limit where policyholder protection requires | [S1]; cross-firm adoption **[std]** (20) |
| Bonus philosophy | Keep a substantial proportion of payout in non-guaranteed (final bonus) form; reference guarantee-fill target θ = 80% of projected asset share | philosophy [S1]; θ **[std]** (21) |
| Final bonus scale scope | Same scale applies at maturity, death and surrender | [S1] |

20. Observed change limits: "not expected to exceed 1% p.a." with full discretion
    to declare zero in the anchor fund [S1]; 1% compound y/y (traditional), 1.25%/1.5%
    (unitised, by product) at a mutual [S7]. ±1.00% adopted for both chassis.
21. PPFMs state the philosophy qualitatively [S1] but publish no guarantee-fill
    parameter. θ = 80% (regular-bonus path aims for guaranteed benefits ≈ 80% of the
    projected maturity asset share, leaving ≈ 20% as final bonus) is the reference
    parametrization; see technical notes for the bonus-setting rule.

### Payout targets, smoothing and MVR

| Parameter | Representative value | Basis |
|---|---|---|
| Payout target | 100% of unsmoothed asset share on average | [S5] [S7] [S8]; range must include 100% [R1] |
| Target range | 80%–120% of asset share, with the aim that ≥90% of policies pay within the range | [S1]; ≥90% test structure [R1]; adoption **[std]** (22) |
| Year-on-year smoothing cap | Payouts for the same class and duration normally change by no more than ±10% y/y | [S1]; adoption **[std]** (23) |
| Smoothing cost | Tracked in a smoothing account within the estate; intended broadly neutral over time | [S1] [S2] [S5] [S6]; PPFM expected to state neutrality intent (COBS 20.3.8G guidance) [R2] |
| MVR trigger | Exit outside MVR-free events while unit face value (incl. attached bonuses) exceeds the asset share | [S1] [S4] [S5] [S6] |
| MVR bound | MVR no greater than necessary to reflect the excess of unit value over the underlying asset value | [R1 COBS 20.2.16R](#uklib-with_profits-r1); post-MVR payouts target 100% of asset share [S5] |
| Final bonus / MVR interaction | Never applied simultaneously to the same policy | [S4]; adoption **[std]** (24) |

22. Observed maturity target ranges: 80–120% (the anchor fund, aim ≥90% of policies
    within [S1]; a consolidator's typical funds, before smoothing [S4]; another
    proprietary insurer's group payouts [S5]); 80–130% conventional / 75–125% unitised
    (one mutual [S6]); 75–125% / 85–111% / 80–120% by product (another mutual [S7]).
    80–120% with the ≥90% test is the modal design and matches the COBS structure
    (range must include 100% of unsmoothed asset share; payments may fall outside if
    ≥90% of the group is within) [R1].
23. Observed smoothing formulations: ±10% y/y in normal circumstances in the anchor
    fund, smoothed vs unsmoothed value rarely >20% apart [S1] [S8]; stepped 5%/7.5%
    limits with a 15% annual maximum and a smoothing account recycled at year-end
    (maximum deduction 2.5% of asset shares p.a.) at another proprietary insurer [S5];
    ≤15% y/y with hard floor/cap at the range edges at one mutual [S7]; formulaic
    pull-to-asset-share with no fixed maximum at another mutual [S6]. The ±10% cap
    plus a cost-neutral smoothing account is the most transferable abstraction.
24. In one consolidated with-profits fund, final bonus and MVR do not apply
    simultaneously to any policy class; in some other funds they may [S4]. Exclusivity
    is adopted because it follows automatically from the reference one-sided formulas
    (technical notes).

### Modern open variation — PruFund-style smoothed fund

| Parameter | Representative value | Basis |
|---|---|---|
| Bonus mechanism | None. Unit price grows daily at the Expected Growth Rate (EGR), an annualised rate (can be negative) set quarterly by the Board from expected long-term returns | [S2] [S11] |
| Snapshot EGR | 5.0% p.a. | **[std]** (25) |
| Daily smoothing rule | If spot NAV/unit AND the 5-working-day rolling average NAV/unit differ from the smoothed price by ≥ the Daily Smoothing Limit, the price is immediately adjusted to within the Gap After Adjustment | [S2] [S9] [S11] |
| Quarterly smoothing rule | On each quarter date, while the gap between NAV per unit and the price is ≥ the Quarterly Smoothing Limit, the price is moved by half the difference, repeatedly | [S2] [S9] [S11] |
| Smoothing limits (growth funds) | Daily 5.0% / Quarterly 10.0% / Gap After Adjustment 2.5% of unsmoothed price | [S9] |
| Smoothing limits (cautious and Risk Managed 1–2 funds) | 4.0% / 8.0% / 2.0% | [S9] |
| Protective machinery | Unit Price Reset to NAV; suspension of smoothing (price tracks NAV); unit cancellations on switches/transfers/withdrawals may be deferred up to 28 days (day-28 price applies) | [S2] [S10] [S11] |
| Charges | Tiered AMC 0.30%–0.575% by fund size; guarantee/smoothing charge typically within the AMC | [S10] [S2] |
| Death benefit | 100.1% of the bid value of units | [S10] [S11] |
| Optional guarantees | Minimum fund value at chosen guarantee dates for an annual charge taken by unit cancellation | [S10] |

25. EGRs are set quarterly and published per fund [S2]; current EGR values were not
    collected (research gap 3). 5.0% p.a. matches the composite fund-return assumption
    in the technical notes so the smoothed and unsmoothed paths coincide in the base
    deterministic scenario.

### Ownership variation — mutual profit distribution

| Parameter | Representative value | Basis |
|---|---|---|
| Shareholder transfer | None (mutual) | [S6] [S7] |
| Distribution mechanism | Annual discretionary profit distribution from the Estate (may be zero): extra regular bonus plus asset-share enhancement for conventional/unitised WP; bonus units for unit-linked WP | [S6] |
| Relative rate | CWP/UWP distribution rate = 8× the unit-linked WP rate for pre-2022 policies; multiple variable (independent actuarial advice required below 6 or above 10) | [S6] |
| Estate protection | The distribution may be reduced to zero and asset-share charges introduced if the Estate becomes too low | [S6] |

The base model sets the mutual distribution to zero (proprietary composite); the mutual
variation replaces the shareholder-transfer deduction with an optional
profit-distribution addition.

---

## Contractual mechanics

**Unitised account and bonus hardening.** The policy account is `FV(t) = U(t) · Q(t)`,
where `U(t)` is units held and `Q(t)` the with-profits unit price. The declared regular
bonus `b(t) ≥ 0` is delivered through unit-price growth, `Q(t) = Q(t−1) · (1 + b(t))`
[S1] [S4]. The unit price never falls; once added, bonus (unit-price growth) cannot be
removed — but the *face value* is payable in full only at guarantee events. Guarantees
bite at death, at maturity (where a term applies) and at contractual MVR-free guarantee
dates [S1] [S4] [S5].

**Unitised claim values.** At a guarantee event the payout is
`FV(t) + FB(t)` with final bonus `FB(t) = max(0, S(t) − FV(t))`, where `S(t)` is the
smoothed target payout derived from the asset share (technical notes). On surrender
outside guarantee events the payout is `FV(t) + FB(t) − MVR(t)` with
`MVR(t) = min( max(0, FV(t) − S(t)), max(0, FV(t) − AS(t)) )`: the MVR recovers the
shortfall of the smoothed payout below face value but may never exceed the excess of
unit value over the underlying asset share [R1 COBS 20.2.16R](#uklib-with_profits-r1), and post-MVR payouts
target 100% of asset share [S5]. This one-sided pair reproduces the observed practice
that the MVR reduces final bonus first, then unit face value [S5], and that final bonus
and MVR do not apply simultaneously [S4]. On partial withdrawal, the asset share is
reduced pro rata to the pre-MVR policy value [S1].

**Conventional guaranteed benefit stack.** With compound reversionary bonuses at rate
`b_rev(t)`, the guaranteed benefit `G(t) = SA + attaching bonuses` evolves as
`G(t) = G(t−1) · (1 + b_rev(t))`, `G(0) = SA` **[std]** (16). `G(t)` is payable at
death or maturity only [S1] [S8]; surrender values are not guaranteed. The maturity
payout is `G(n) + TB(n)` with terminal bonus `TB(n) = max(0, S(n) − G(n))` (18); the
death payout during the term is `G(t)` plus interim bonus accrual at the last declared
rate plus final bonus per the same scale [S1] [S4] [S8].

**Conventional surrender value.** Formula-based, targeting asset shares over the long
term with parameters reviewed at least annually [S1]: the reference form is
`SV(t) = clamp( AS(t), 0.85 · PV_g(t), 1.15 · PV_g(t) )`, where
`PV_g(t) = G(t) · (1 + i_sv)^−(n−t)` is the discounted guaranteed benefit at the
surrender-basis rate `i_sv = 4.0%` **[std]** (19). Surrender payouts progress into
maturity values near the term end [S1]; no formal smoothing applies to surrenders
[S5] [S6].

**Deferred annuity note.** Conventional with-profits deferred annuities carry a basic
annuity p.a. plus bonuses; cash claims reflect the current cost of the deferred annuity
[S1]. Out of scope for the composite cells but relevant to the GAO rider below.

**Smoothed-fund (PruFund) contractual smoothing.** The policy conditions define the
Expected Growth Rate, Daily Smoothing Limit, Quarterly Smoothing Limit and Gap After
Adjustment as contractual terms [S11]. Daily: if both the spot NAV per unit and the
5-working-day average breach the Daily Smoothing Limit relative to the smoothed price,
the price is adjusted to the Gap After Adjustment; quarterly: while the gap is ≥ the
Quarterly Smoothing Limit the price moves by half the difference, repeatedly [S9] [S11].
The insurer may reset the unit price to NAV or suspend smoothing to protect the fund
[S2] [S11]. Pay-out value = units held × unit price, less policy-condition deductions,
at the transaction date [S2].

---

## Riders and options

**In scope (modeled as flags):**

- **Guaranteed annuity option (GAO)** — legacy pension cells only. A guaranteed rate of
  annuity conversion at retirement, present in several closed funds (deferred annuities
  and retirement annuity contracts in one acquired book; unit-linked GAO risk in
  another); GAO liabilities are backed by fixed-interest assets and GAO
  interest-rate risk is an identified fund business risk [S4]. Historical market
  significance (a major UK office's closure in 2000 after the House of Lords ruling on
  GAO costs) is [unverified] context. Parametrized in the technical notes as a flag with a
  **[std]** guaranteed annuity rate.
- **Guarantee-date capital guarantees (smoothed-fund variation)** — optional minimum
  fund value at chosen guarantee dates for an explicit annual charge taken by unit
  cancellation [S10].

**Out of scope for the composite:** with-profits annuities (smoothing caps 11–12% on
income rises [S1]); credit-matched with-profits (guaranteed benefit at outset,
prospective asset shares [S1] [S3]); cash accumulation business (bonuses added to
contributions; regular bonus guaranteed to the next revision date [S1]); unit-linked
with-profits (bonus units, no asset shares or smoothing [S6]); deposit
administration [S6]; Industrial Branch business [S1]; return-of-premium death
guarantees on modern bonds [S10]; protection riders (waiver, critical illness) —
original conventional policy conditions are unpublished (research gap 4).

---

## Variations across insurers

1. **Chassis split.** Conventional (sum assured + declared bonus stack, formulaic
   surrender values [S1] [S4] [S8]), unitised (unit account, bonus-driven price growth or
   bonus units, MVR machinery [S4] [S5] [S6] [S7]) and smoothed funds (EGR + rule-based
   price adjustment, no declarations [S2] [S9] [S11]). The composite models (a) and (b)
   as core chassis and (c) as the open-business variation because that is where the
   respective blocks of UK liability sit [S4] [S10] [S13].
2. **Target ranges.** All firms target 100% of asset share on average, but ranges
   differ: 80–120% (three proprietary funds [S1] [S4] [S5]); 80–130%/75–125% (one
   mutual [S6]); 75–125%, 85–111%, 80–120% by product (another mutual [S7]). 80–120%
   with the ≥90%-of-policies test is chosen as modal and as the direct implementation
   of the COBS structure [R1].
3. **Smoothing formulation** varies more than any other feature: y/y payout caps (10%
   in the anchor fund [S1]; 15% at one mutual [S7]; stepped 5%/7.5% with a 15% annual
   max at another proprietary insurer [S5]), explicit smoothing accounts recycled to
   asset shares (maximum deduction 2.5% p.a. [S5]; bonus smoothing accounts within the
   Estate in the anchor fund [S1] [S2]), or pure formulaic pull-to-asset-share with no
   stated cap (another mutual [S6]). Chosen: ±10% cap plus a neutral smoothing
   account — the most transferable abstraction.
4. **MVR triggers.** Shortfall-based (three proprietary funds [S1] [S4] [S5] — all
   capped at the asset-value shortfall per COBS 20.2.16R [R1]); explicit numeric
   trigger/taper (one mutual: MVR when asset share <90% of unit value, linear
   smoothing-in between 85% and 90%, taper to zero over 3 years to retirement [S7]).
   MVR-free events are universal: death [S5], contractual guarantee dates
   [S1] [S4] [S5], frequently the 10th anniversary for bonds [S4]. Chosen: the
   shortfall-capped form — it is the regulatory bound itself.
5. **Ownership/distribution.** Proprietary 90:10 (the anchor fund [S1]; another
   proprietary insurer, transfer charged to asset shares [S5]) vs mutual (an annual
   profit distribution at an 8× multiple [S6]; another mutual [S7]) vs defined-charge
   (a DCPSF alongside the anchor fund in the same long-term fund: explicit charges
   only, shareholder bears expense differences [S1] [S2]). Chosen: 90:10 proprietary
   as the representative historical design, with the mutual variation specified
   separately.
6. **Guarantee charging.** Lifetime caps as % of asset share (2%/4% in the anchor fund
   [S1]), time-limited unit charges (0.7% × 10 years [S5]), conditional
   deficit-triggered charges (10%/25% caps, reversible, in one consolidated closed fund
   [S4]; a 1% p.a./7% lifetime ladder in another [S4]), or annual deductions from
   credited return (with-profits annuities in the anchor fund [S1]; an option at a
   mutual [S6]). Chosen: a level annual deduction with the [S1] 2% lifetime cap — a
   configurable single dial.
7. **Estate handling.** From pure working capital (the anchor fund [S1]) to
   reattribution with special bonuses (a 2009 scheme backed by an external
   inherited-estate support account [S5]), an annual mutual profit distribution [S6]
   and estate-floor triggers (a consolidator [S4]). Chosen: residual estate, no
   distribution — the least model-intrusive and the stance documented for the anchor
   fund [S1].

---

## Regulatory context

**Prudential — PRA / Solvency UK.** With-profits funds are ring-fenced: a firm must
hold assets in each with-profits fund sufficient to cover the with-profits policy
liabilities of the business written in or transferred into that fund, and its
distribution strategy for discretionary benefits must be affordable and sustainable
[R6]. Technical provisions are best estimate plus risk margin; the best estimate must
include all expected payments to policyholders "whether or not ... contractually
guaranteed" — the basis for including future discretionary benefits (FDB) in the BEL —
with a carve-out for surplus funds (the estate, which counts as own funds rather than
insurance obligations) [R7] [R8]. Financial guarantees and options must be valued with
realistic, dynamic policyholder-behavior assumptions [R7]. The PRA Surplus Funds Part
codifies the retrospective asset-share item list used throughout this specification
[R8]. The post-2023/24 "Solvency UK" risk margin uses a 4% cost-of-capital rate with a
0.9 risk-tapering factor for long-term business [R7] [REG-R4].

**Conduct — FCA.** COBS 20.2 requires maturity-payment target ranges expressed as
percentages of unsmoothed asset share that include 100%, a ≥90%-within-range test,
the MVR shortfall bound, the required-percentage distribution floor with proportionate
shareholder-transfer reduction, at-least-annual excess surplus determination, new
business only on terms unlikely to adversely affect existing policyholders, and a
run-off plan within three months of closing to material new with-profits business
[R1]. COBS 20.3 requires a maintained PPFM covering amounts payable, bonus approach,
smoothing limits, investment strategy, business risk, charges, the inherited estate,
new business volumes and shareholder equity [R2]; COBS 20.4 requires PPFM provision to
policyholders, three months' notice of principle changes and an annual
PPFM-compliance report [R3]; COBS 20.5 requires a With-Profits Committee (≥3 members,
expected to meet at least quarterly) — or, for smaller/simpler funds, an advisory
arrangement — advising on bonus rates, smoothing and MVRs [R4]. SUP 4.3 defines the With-Profits Actuary function, including advising whether
the FDB assumptions in technical provisions are consistent with the PPFM [R5]. The
Consumer Duty applies to retail with-profits business (Principles 6/7 disapplied where
it applies) [REG-R12].

**Professional standards.** With-Profits Actuaries must hold a practising certificate
and manage conflicts under IFoA APS L1, which also requires oversight of asset-share
calculation where it is not the WPA's direct responsibility [R12]. Technical actuarial
work on with-profits reserving falls under FRC TAS 100 (v2.0, effective 1 July 2023
[REG-R33]) and TAS 200: Insurance (v2.0, effective 1 January 2025) [R11].

**Tax.** With-profits life business is BLAGAB under Finance Act 2012 Part 2, taxed on
the I-E basis — policyholder-level tax is effectively borne inside the fund, and asset
shares are charged tax accordingly (pensions business is credited gross returns)
[S1] [S2] [REG-R17] [REG-R18]. Policyholder taxation of with-profits bonds follows the
chargeable event gains regime (ITTOIA 2005 Part 4 Chapter 9): part surrenders within
the cumulative 5%-of-premium annual allowance are not immediately taxable, shaping
withdrawal behavior [REG-R15] [REG-R16]. With-profits ISA wrappers carry the £20,000
annual subscription limit [S12]. Classification: conventional with-profits assurances
and annuities are Class I long-term business under the RAO; unitised/linked structures
typically involve Class III [R9; per-product allocation unverified](#uklib-with_profits-r9).

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uklib-with_profits-r1
[R11]: #uklib-with_profits-r11
[R12]: #uklib-with_profits-r12
[R2]: #uklib-with_profits-r2
[R3]: #uklib-with_profits-r3
[R4]: #uklib-with_profits-r4
[R5]: #uklib-with_profits-r5
[R6]: #uklib-with_profits-r6
[R7]: #uklib-with_profits-r7
[R8]: #uklib-with_profits-r8
[REG-R12]: #uklib-reg-r12
[REG-R15]: #uklib-reg-r15
[REG-R16]: #uklib-reg-r16
[REG-R17]: #uklib-reg-r17
[REG-R18]: #uklib-reg-r18
[REG-R33]: #uklib-reg-r33
[REG-R4]: #uklib-reg-r4
[std]: #uklib-std
[unverified]: #uklib-unverified
<!-- END generated citation links -->
