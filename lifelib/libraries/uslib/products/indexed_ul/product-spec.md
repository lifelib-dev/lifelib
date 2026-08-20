# Product Specification

**Status:** Draft, 2026-08-03.
**Scope note:** This is a standardized *composite* specification assembled for reference
liability-model implementation. It does not describe any single insurer's product. Facts
carry source tags: [S#]/[R#] refer to the sources catalogued in `sources.md` (extraction
provenance in `_research/indexed-ul.md`); [REG-R#] refers to the cross-product
reference library (`references/regulatory-and-actuarial-references.md`; research
provenance in `_research/regulatory-actuarial.md`, same R-numbering). **[std]** marks a
standardization introduced for the reference implementation (choice among observed carrier
practices, or a placeholder where carrier values are not public); every **[std]** table row
has a footnote giving the rationale and the observed range. Items the research notes flag
as [unverified] remain flagged here. All "current" (non-guaranteed) rates are snapshots as
of each source document's print date and change frequently [S3] [S4].

---

## Product overview and market role

Indexed universal life (IUL) is a flexible-premium universal life chassis in which cash
value allocated to indexed accounts earns interest "based in part on the performance of
market-based indexes"; the policy is not directly invested in the market [S1]. The NAIC
Valuation Manual defines an IUL policy as "any universal life (UL) insurance policy where
the interest credits are linked to an external reference" [R3]. Some carriers brand the
identical design "fixed index universal life" (FIUL) [S8]. Mechanically, IUL is
current-assumption UL plus one or more indexed accounts: all premium, charge, death
benefit, loan, and lapse provisions follow the UL pattern (base chassis:
`products/universal_life/product-spec.md` and the technical notes in that
directory); only the interest-crediting engine differs.

IUL is sold primarily for cash-value accumulation and distribution (policy loans in
retirement); one carrier states a target market of ages 30–55 [S5]. Competition centers on
illustrated performance: current illustrated rates for S&P 500-style accounts across 16
carriers ranged 5.61%–7.38% in a 3/2026 benchmarking snapshot [S6]. IUL policies are
state-regulated fixed products; none of the five carriers researched references an SEC
prospectus, and IUL products are generally not SEC-registered ([unverified] as a general
proposition — EDGAR was not searched for product documents) [see research notes, Gaps].

The representative baseline below is deliberately the **AG 49-A Benchmark Index Account
(BIA) design** — 1-year S&P 500 point-to-point, annual cap, 0% floor, 100% participation,
no multipliers/bonuses/enhancements [R1] — because it is the one account design every
researched carrier offers [S2] [S3] [S5] [S6] and the regulatory canonical form [R1].

---

## Representative specification

### Table 1 — Chassis and coverage

| Parameter | Representative value | Basis |
|---|---|---|
| Policy type | Flexible-premium indexed universal life | [S1] [S3] [R3] |
| Issue ages | 0–85 | [S3] |
| Age basis | Age nearest birthday (ANB) | **[std]** (F1) |
| Minimum face amount | $100,000 | [S5] [S7] (F2) |
| Underwriting classes | Preferred Elite / Preferred Plus / Preferred / Non-Tobacco / Preferred Tobacco / Tobacco / Juvenile (0–17) | [S3] |
| Death benefit options | A (level), B (increasing = face + account value) | [S3] [S5] [S7] (F3) |
| DB option changes | Allowed after policy year 3, once per year, not after age 95 | [S3] |
| Tax qualification test | Guideline Premium Test + cash value corridor (§7702) | **[std]** (F4) |
| Corridor factors | 250% at attained ages 0–40 grading to 100% at ages 90–95 | [R4] |
| Maturity age | Attained age 121; policy continues in force, no further charges [unverified] | **[std]** (F5) |
| No-lapse guarantee | Cumulative-premium test; no-lapse period by issue age: 0–45: 20 yrs; 46–60: to age 65; 61+: 5 yrs | [S3] (F6) |
| Grace period | 61 days | [S3] |
| Reinstatement | Within 3 years of lapse, evidence of insurability; lapsed time does not count toward surrender-charge period | [S3] |
| Face increases | After year 1, to age 85, min $25,000, underwritten; new charge/surrender layers | [S3] |
| Face decreases | After year 3, min $25,000, ≤20% p.a. before later of age 65 / end of surrender period, subject to §7702 | [S3] |

Footnotes:
- **F1 [std]:** Observed both ways — one carrier uses age last birthday [S3], another age
  nearest birthday [S7]. ANB chosen because the 2017 CSO / 2015 VBT table families publish
  ANB variants directly usable for guaranteed and best-estimate mortality [REG-R17] [REG-R18].
- **F2:** Observed range $25,000 (band 1 of one carrier) [S3] to $100,000 (two other
  carriers) [S5] [S7]. $100,000 chosen as the modal modern accumulation-IUL minimum; also
  the threshold for preferred classes at the $25,000-minimum carrier [S3].
- **F3:** A Graded option (increasing to 70, grading level at 95) [S3] and a Return of
  Premium option [S5] exist; excluded from baseline as minority designs.
- **F4 [std]:** §7702 allows CVAT or GPT+corridor [R4]. GPT chosen because one carrier's
  Overloan Protection Rider attaches only to GPT non-MEC policies [S3], indicating GPT as
  the operative accumulation-IUL administration basis; CVAT documented as a variation.
- **F5 [std]:** No retrieved document states maturity mechanics explicitly; age 121 is
  inferred ([unverified]) from charges running to age 120 and a rider (Additional Insured)
  terminating at base insured age 121 [S3]. Confirm against specimen policy forms before
  relying on it.
- **F6:** Structure and periods from one carrier's Minimum Monthly No-Lapse Premium
  (MNLP) design: no lapse during the no-lapse period while cumulative premiums less
  loans/withdrawals ≥ cumulative MNLP [S3] [S4]. Comparators: 20 yrs (issue ages
  0–55) / (75 − issue age) yrs (56–69) / 5 yrs (70+) at a second carrier [S5]; an age-90
  NLG rider plus an optional lifetime-duration rider at a third [S1].

### Table 2 — Accounts and index crediting (baseline = AG 49-A Benchmark Index Account design [R1])

| Parameter | Representative value | Basis |
|---|---|---|
| Fixed account, current rate | 4.50% (first-year rate locked) | [S2] (F7) |
| Fixed account, guaranteed minimum | 1.00% | [S2] (F7) |
| Indexed account: index | S&P 500 price return (dividends excluded) | [S2] [S3] [S5] [R1] |
| Crediting method | Annual point-to-point (1-year segment term) | [S2] [S3] [S5] [R1] |
| Participation rate | 100%, guaranteed | [S2] [R1] |
| Current cap | 10.00% (snapshot, 11/2024 print; caps are redeclared at each segment start and highly variable) | [S2] (F8) |
| Guaranteed minimum cap | 2.00% | [S2] (F8) |
| Floor | 0% annual, guaranteed | [S2] [S5] [S6] [S8] [R1] (F9) |
| Segment starts (sweep dates) | Monthly, on the policy monthiversary | **[std]** (F10) |
| Segment term / max segments | 12 months; up to 12 concurrent segments per account | [S3] [S4] |
| Holding (interim) account | Net premium held in the fixed account and credited at fixed-account rates until the next sweep date | [S1] **[std]** (F10) |
| Matured segment value | Rolls into a new segment per standing allocation instructions | [S3] **[std]** (F11) |
| Mid-segment values | Death benefit/CSV reflect segment balance without unrealized index credit; amounts leaving a segment mid-term receive no index credit | [S3] (F9) |

Footnotes:
- **F7:** Fixed-account guarantees observed 1.00% [S2] [S5] to 2.00% [S3] [S4]; currents
  4.25% [S5] to 4.50% [S2]. The [S2] pair (4.50%/1.00%) is used as the internally
  consistent snapshot.
- **F8:** Current caps observed for 1-yr S&P 500 PTP accounts: 10.00% [S2], 10.25% [S5],
  10.50% [S7], 12.00%–13.75% (same product, two print dates — caps fell between prints)
  [S3] [S4]. Guaranteed minimum caps observed 0.25% [S8] to 4.00% on a charge-funded
  high-cap account [S2]; one carrier instead guarantees the cap never below its current
  declared-account rate [S3] [S4]. Treat any current cap as a calibration snapshot, not a
  fixed parameter.
- **F9:** Floor-design variation: one carrier credits a guaranteed 0.75% *during* the
  segment and nets it out of excess index interest [S3]; another expresses its guarantee
  as a 2% cumulative average tested at death or termination [S7]. The 0% annual floor is
  the dominant design [S2] [S5] [S6] [S8] and the BIA definition [R1]; the retrospective
  cumulative guarantee is documented under Variations.
- **F10 [std]:** Carrier practice varies: one carrier sweeps on the 15th of each month
  [S1]; another creates segments on monthly policy dates, transfers into index
  accounts only on the first day of a policy month [S3]. Baseline standardizes sweep =
  policy monthiversary so segment dates align with monthly processing. A third carrier's
  minimum required fixed-interest strategy allocation (an estimate of the coming year's
  charges held back in the fixed strategy) [S5] is documented as a variation, not baseline.
- **F11 [std]:** Automatic re-entry per standing instructions per [S3] (its automatic
  transfer rule). Baseline: 100% of matured value rolls into a new segment of the same
  account; reallocation to the fixed account is a policyholder option.

### Table 3 — Charges

| Parameter | Representative value | Basis |
|---|---|---|
| Premium load | 5.00% of each premium, all years, current; 8.00% guaranteed maximum | **[std]** (F12) |
| Monthly policy fee | $10.00/month current; $15.00 guaranteed maximum | [S3] [S5] / **[std]** (F13) |
| Per-unit (per-$1,000) charge | $0.30 per $1,000 of face per month, policy years 1–10 current (re-starts on face increases); guaranteed maximum $0.40 payable all years | structure [S3] [S5]; amounts **[std]** (F14) |
| Cost of insurance (COI) | Monthly rate × net amount at risk / 1,000; varies by age, sex, class, duration, band; guaranteed maximum = 2017 CSO ANB smoker-distinct ultimate; current = 65% of guaranteed | structure [S3]; guaranteed basis **[std]**/[REG-R17]; current ratio **[std]** (F15) |
| Indexed-account asset charge | None in baseline (BIA has no charge-funded enhancement) | [R1] (F16) |
| Surrender charge | Per $1,000 of initial face (and of each increase layer), 10-year period; initial $25.00 per $1,000 declining linearly to 0 at year 11 | period [S1] [S5] [S7]; scale **[std]** (F17) |
| Withdrawal fee | $25 per withdrawal; minimum withdrawal $500; CSV may not fall below $500 | [S3] |

Footnotes:
- **F12 [std]:** Observed at three carriers: 4% current all years / 6% guaranteed (6%/8%
  Puerto Rico) [S3]; 8% year 1, 6% years 2+ current / 10% guaranteed [S5]; a load of
  undisclosed amount [S1]. A level 5% current / 8% guaranteed is a mid-range
  standardization avoiding year-shape complexity.
- **F13:** $10/month current is common to [S3] [S5]. Guaranteed maxima observed $12 [S3]
  and $20 [S5]; $15 **[std]** is a rounded mid-range value.
- **F14 [std]:** Structure (currently charged years 1–10, guaranteed for all years,
  varying by issue age/sex/band/tobacco, re-start on face increases) is sourced [S3] [S5];
  the dollar scales live in policy data pages and are not public (research notes, Gaps),
  so the level is a modeling placeholder chosen to be a realistic secondary expense
  charge; calibrate to pricing targets in use.
- **F15 [std]:** COI structure and re-rating discipline (changeable up to guaranteed
  maximums, changes must be based on expectations of future cost factors) are sourced
  [S3]; NGE re-determination practice is governed by ASOP 2 [REG-R26]. Carrier COI tables
  are not public (research notes, Gaps). Guaranteed = 2017 CSO (the statutory
  valuation/nonforfeiture basis for new issues [REG-R17]) is the conventional guaranteed
  ceiling **[std]**; the 65% current-to-guaranteed ratio is a placeholder **[std]** —
  replace with a scale calibrated to 2015 VBT / ILEC experience plus margin
  [REG-R18] [REG-R19].
- **F16:** Charge-funded high-cap/multiplier accounts exist across carriers — ongoing
  asset charges of 0.72%/yr [S3] or 0.80%/yr [S2], or up-front strategy charges of
  0.65%–1.0% at segment creation [S5] — and fund a Supplemental Hedge Budget under
  AG 49-A [R1]. Excluded from baseline; see Variations.
- **F17 [std]:** Period: 10 years is modal [S1] [S5] [S7] (15 years at one carrier [S3]);
  re-starts on face increases [S3] [S7]. Dollar scales are not public (research notes,
  Gaps); the $25/$1,000 linear-decline scale is a placeholder of realistic magnitude.

### Table 4 — Loans and withdrawals

| Parameter | Representative value | Basis |
|---|---|---|
| Standard (declared-rate) loan — charged | 3.00% effective annual, in arrears, all years | **[std]** (F18) |
| Standard loan — credited on collateral | 2.00% years 1–10; 3.00% (wash) years 11+ | **[std]** (F18) |
| Participating (indexed) loan — charged | 5.00% current; 8.00% guaranteed maximum | [S5] [S7] (F19) |
| Participating loan — credited | Loaned value remains credited at indexed-account rates | [S5] (F19) |
| Loan sourcing | Fixed account first, then pro rata across index accounts/segments | [S3] |
| Minimum loan | $500 | [S3] |
| Withdrawals | After free-look; pro rata across unloaned accounts; $500 minimum; $25 fee | [S3] |
| Illustration constraint | Illustrated loan credited rate ≤ illustrated loan charged rate + 50 bps | [R1] |

Footnotes:
- **F18 [std]:** Observed declared-rate designs at three carriers: charged 2.75% current /
  3% guaranteed, credited 2%, preferred loans years 11+ charged 2% current / 2.25% max on
  gains [S3] [S4]; charged 3.90% years 1–10, 3.00% years 11+ (0% net from year 11),
  credited 3.00% current / 1.00% guaranteed [S5]; charged 4%, credited 3% years 1–10 /
  4% years 11+ [S7]. The standardization keeps the universal pattern (net loan spread ~1%
  early, →0% "wash" after year 10) with round numbers. The baseline liability model uses
  standard loans only **[std]**; participating loans are a variation.
- **F19:** One carrier's alternative loan: charged 5% current / 8% guaranteed max, credited
  at indexed strategy rates, may be mixed or switched [S5]; a second carrier's indexed loans
  charged 5% [S7]; a third routes loaned value to a dedicated lower-par volatility-control
  account via rider (current par 160%, guaranteed min 20%) [S2]. At that second carrier a
  fixed-rate loan triggers a 12-month lockout on fixed-to-indexed transfers [S6];
  short-term loans are interest-free if repaid within 90 days [S7].

---

## Contractual mechanics

### Premium provisions
Premiums are flexible: the owner may increase, decrease, skip, or stop premiums provided
the no-lapse guarantee is in effect or cash surrender value covers monthly deductions
[S3]. Each premium is reduced by the premium load; the net premium is credited to the
fixed account (which doubles as the interim/holding account) and becomes eligible for
transfer to indexed segments at the next monthly sweep date [S1] **[std]** (F10). Premiums
are limited by §7702 guideline premiums (GPT baseline, F4) [R4]; premiums beyond the 7-pay
limit in the first seven years make the contract a MEC under §7702A, changing distribution
taxation [R5].

### Death benefit provisions
- Option A: DB = max(Face, corridor factor × account value). Option B: DB = Face + account
  value, similarly corridor-tested [S3] [R4].
- Corridor factors per §7702(d): 250% at attained ages 0–40 grading to 100% at 90–95 [R4].
- Death proceeds are reduced by outstanding loan balance and any unpaid monthly deductions
  **[std]** (universal UL practice; loan-netting implicit in loan design [S3] [S5]).
- During a segment, the death benefit reflects the segment balance without unrealized
  index credit [S3] (0%-floor baseline: segments simply carry no interim interest, F9).

### Account value mechanics
Account value = fixed account + sum of active segment balances + loan collateral account
**[std]** (decomposition; components per [S1] [S2] [S3] [S5]). On each monthiversary, in the
processing order specified in `technical-notes.md`: premiums are received net of load;
monthly deductions (policy fee + per-unit charge + COI + rider charges) are taken from the
fixed account first, then pro rata from active segments **[std]** (sourcing convention;
carrier practice varies — one carrier sources loans fixed-first/pro-rata [S3] and adjusts
the index-credit base for mid-segment deductions [S3]); eligible fixed-account balance is
swept into a new 12-month segment [S3] **[std]**.

### Index crediting
For a segment created at time m with index level I(m):

    index change  r = I(m+12) / I(m) − 1        (price return, dividends excluded) [S2] [S3]
    credited rate = max(floor, min(cap, par × r)) = max(0%, min(10.00%, 100% × r)) [S2] [S3]
    index credit  = credited rate × segment balance at maturity (after all deductions)  **[std]**

The credit-base convention is standardized: the credit applies to the actual remaining
segment balance at maturity, i.e., amounts withdrawn, borrowed (standard loans), or
deducted mid-segment earn no index credit (withdrawal/loan forfeiture [S3]; extension to
mid-segment deductions **[std]**). One carrier's contractual variant instead credits
(adjusted index change %) × (adjusted beginning value) − (interest already credited at
the guaranteed minimum during the segment), where the adjusted beginning value subtracts
withdrawals, loan transfers, and one-half of monthly deductions and index-account charges
taken during the segment [S3] — documented as a variation because it presumes
an in-segment guaranteed rate (0.75% [S3]) the baseline does not have.

Caps (and, on other designs, participation rates and spreads) are non-guaranteed elements
declared at each segment start [S3] [S4] [S8], subject to contractual guaranteed minima
(Table 2), and economically set by the option budget — see `technical-notes.md`,
option-budget section [R1] [R6].

### Charges and credits
Monthly deduction = policy fee + per-unit charge + COI on net amount at risk + rider
charges (+ indexed-account asset charges on enhanced accounts, not in baseline)
[S1] [S3] [S5]. COI rates may be re-rated up to guaranteed maximums based on expectations of
future mortality, interest, persistency, expense, reinsurance, and tax experience [S3];
ASOP 2 governs the re-determination discipline [REG-R26]. The fixed account is credited
monthly at the declared rate (guaranteed minimum 1.00% [S2]); segments receive their index
credit only at maturity [S3].

### Loans
Standard loans move loaned value into a loan collateral account credited at a fixed rate
while the loan accrues at the charged rate (Table 4) **[std]**/[S3] [S5]; the net cost
grades to ~0% ("wash") after year 10 [S3] [S5] [S7]. Participating loans leave loaned value
exposed to indexed crediting while charging a fixed rate [S5] [S7] — positive expected
spread, negative in 0%-floor years; baseline models standard loans only **[std]** (F18).
Loans reduce the death benefit and, if unpaid, accrue against the account; an Overloan
Protection Rider can convert the policy to paid-up status to prevent loan-induced lapse
and tax recognition (one-time charge on exercise: 5% of policy value at ages 75–90 grading
to 1% at 94–120) [S3].

### Withdrawals
Partial withdrawals after free-look, pro rata across unloaned accounts, $500 minimum, $25
fee [S3]; mid-segment withdrawals forfeit index credit on the withdrawn amount [S3].
Withdrawals reduce Option A death benefit dollar-for-dollar **[std]** (standard UL
practice; not explicit in retrieved brochures). Withdrawals within the first 15 policy
years associated with benefit reductions can be taxable under §7702(f)(7)(B) [S1].

### Grace, lapse, reinstatement
If cash surrender value cannot cover the monthly deduction and the no-lapse test fails,
a 61-day grace period begins [S3]; the policy lapses if the required premium is unpaid at
grace end. No-lapse test: cumulative premiums less loans/withdrawals ≥ cumulative minimum
monthly no-lapse premium during the no-lapse period [S3] [S4] (representative MNLP rate:
male non-tobacco issue age 45, band 1: $20.80 per $1,000 face annually [S3]).
Reinstatement within 3 years with evidence of insurability [S3].

### Renewal / conversion / maturity
No renewal or conversion mechanics (permanent policy). Maturity at attained age 121
**[std]**, [unverified] inference (F5): charges cease at age 120 (one carrier's index
account monthly charge runs to age 120 [S3]) and coverage continues.

---

## Riders

**In scope for the reference model:**
- **No-lapse guarantee** (integral or rider): age-banded no-lapse period with cumulative
  premium test [S3] [S5]; one carrier implements it as an automatically issued age-90 NLG
  rider (issue ages ≤79, DB options A/B) plus an optional flexible-duration NLG to
  lifetime [S1]. Modeled: the baseline MNLP test (Table 1, F6).
- **Overloan Protection Rider:** on GPT non-MEC policies; converts to paid-up on exercise,
  preventing loan-induced lapse/taxation; one-time exercise charge 5% of policy value at
  ages 75–90 grading to 1% at 94–120 [S3]. Described; exercised-state modeling optional.

**Out of scope (listed for completeness, all observed in research):** term riders on base
or additional insureds [S3]; children's benefit [S3]; guaranteed insurability [S3]; waiver
of monthly deductions / waiver of premium [S3]; accidental death benefit [S3]; accelerated
death benefits for terminal/critical/chronic illness [S3]; long-term care riders
[S1] [S3] [S5]; enhanced performance factor (multiplier) riders [S1]; surrender value
enhancement [S5]; change of insured [S5]; income settlement endorsements [S3].

---

## Variations across insurers

1. **Floor design.** 0% annual floor is dominant [S2] [S5] [S6] [S8]; one carrier credits a
   guaranteed 0.75% during the segment, netted out of excess index interest (its declared
   account guarantees 2%) [S3]; another guarantees a 2% cumulative average tested
   retrospectively at death or termination [S7]. *Choice:* 0% annual floor — dominant
   practice and the AG 49-A BIA definition [R1]; the retrospective cumulative guarantee is
   a documented variation requiring a shadow accumulation in the model.
2. **Index menu.** Every carrier offers 1-yr S&P 500 PTP with cap and 100% participation
   [S2] [S3] [S5] [S6]. Beyond it: multi-index best-performer blends (a global 50/30/20
   blend [S3]; a multi-index monthly-average 50/30/20 [S5]; a third such blend [S7]);
   uncapped S&P 500 with spread (5.75% spread [S5]) or declared participation (a
   dynamic-participation account, illustrations at 50% par [S2]); multi-year segments
   (2-yr cap 24%/5-yr par 110%, same carrier [S2]); uncapped volatility-controlled
   proprietary indexes at high participation (200% [S2], up to 320% [S5], 215% [S7], 160%
   [S8]). *Choice:* BIA-style S&P 500 account only — canonical [R1], universal, and the
   post-2023 illustration regime caps other accounts' illustrated leverage at the BIA's
   anyway [R1] [R6].
3. **Charge-funded enhancements.** Ongoing asset charge (0.80%/yr buys cap 12.0% vs 10.0%
   at one carrier [S2]; 0.72%/yr on all index accounts at another [S3]) vs up-front
   segment charge (0.65%–1.0% buys cap 25.00%/13.25% vs 14.00%/10.25% at a third [S5]);
   multiplier riders for a monthly charge [S1]. Persistency bonuses: 0.20% annualized from
   year 16 (guaranteed if the premium test is met) [S5]; bonus products may carry higher
   surrender charges or lower caps [S8]. *Choice:* excluded — the BIA explicitly has no
   multipliers/bonuses/enhancements [R1], and post-AG 49-A these designs cannot illustrate
   net benefit anyway [R6].
4. **Guaranteed crediting minima.** Guaranteed minimum caps 0.25% [S8] – 4.00% [S2];
   guaranteed participation 5% [S2] [S8] – 105% [S2]; cap floored at declared-account rate
   [S3]. *Choice:* 2.00% guaranteed cap, 100% guaranteed par [S2] — from the same source
   as the baseline current cap.
5. **Premium loads.** Level (4%/6% gtd [S3]) vs front-loaded (8%/6%, 10% gtd [S5]).
   *Choice:* level 5%/8% **[std]** (F12).
6. **Surrender charge period.** 10 years [S1] [S5] [S7] vs 15 years [S3]; all re-start on
   face increases [S3] [S7]. *Choice:* 10 years (modal).
7. **Loan design.** All carriers: declared-rate loan trending to ~0% net cost after ~year
   10 plus an indexed/participating loan charged ~5% [S3] [S4] [S5] [S7]; one carrier
   dedicates a lower-par VC account to loaned value [S2]; another imposes a 12-month
   fixed→indexed lockout after fixed loans [S6]. *Choice:* both described; standard loan
   modeled in baseline **[std]** — it decouples loan modeling from index scenarios.
8. **Interim-account and sweep mechanics.** Sweep on the 15th [S1] vs first day of policy
   month [S3]; charge-holdback in the fixed strategy [S5]. *Choice:* monthiversary
   sweep, no holdback **[std]** (F10).

---

## Regulatory context

- **NAIC UL Model Regulation (Model #585).** The UL chassis regulation: valuation,
  nonforfeiture, mandatory policy provisions, disclosure, annual policyowner statements.
  Section 10 adds interest-indexed UL requirements: filings describing how the insurer
  addresses the risk of the indexed rate falling, description of assets held for
  interest-indexed policies, and an annual Statement of Actuarial Opinion for
  interest-indexed UL [R10] [REG-R5]. **Do not substitute the AP&P Appendix A print for
  it.** Appendix item **A-585** has now been read in full and carries the **valuation
  half only** — definitions and valuation requirements, with no nonforfeiture provisions,
  no mandatory policy provisions, no annual-report requirements and **no interest-indexed
  UL section**; it names only the **Standard Valuation Law (#820)** as its relevant model
  law and does not name Model #585 anywhere, so everything in this bullet stays cited to
  [R10] [REG-R5] [REG-R155].
- **NAIC Life Illustrations Model Regulation (Model #582) + AG 49-A.** Model 582 defines
  the disciplined current scale, self-support and lapse-support tests, and the
  illustration actuary's annual certification [R2]. AG 49-A (policies sold on/after
  12/14/2020, as revised 2023 — colloquially "AG 49-B") layers IUL-specific limits: the
  Benchmark Index Account definition, the maximum illustrated rate (25-year lookback mean
  capped at 145% of the Annual Net Investment Earnings Rate), illustrated option-leverage
  of other accounts capped at the BIA's, the 50 bp loan-spread limit, and alternate-scale
  disclosure [R1] [REG-R10]. History and design intent per the SOA lineage article
  [R6] [REG-R9]; practice guidance in the AAA Life Illustrations Practice Note and ASOP
  No. 24 (current revision Dec. 2024) [R8] [REG-R30].
- **Valuation: Standard Valuation Law + VM-20.** Statutory reserves for IUL follow the
  Valuation Manual as a life product under VM-20 (net premium reserve plus deterministic/
  stochastic reserves as applicable); VM-01 defines "index credit" broadly (any credit,
  multiplier, bonus, or charge reduction linked to an index; may be positive or negative);
  VM-20 requires cash-flow modeling of the assets hedging indexed credits under the
  clearly-defined-hedging-strategy (CDHS) framework [R3] [REG-R3]; enabling statute Model
  #820 [REG-R1]; NLG (secondary-guarantee) designs interact with AG 38 for pre-PBR
  cohorts [REG-R7]. The **formulaic** leg — pre-2017 issues, and the *All Other* net
  premium reserve where VM-20 §3.B.6 routes indexed UL with no deterministic or
  stochastic reserve to VM-A/VM-C — is the **A-585** universal life CRVM adaptation, now
  read at first hand: a guaranteed-maturity-premium / guaranteed-maturity-fund
  construction, not the §5.A modified-net-premium one, whose GMP is solved on policy
  guarantees at issue "excluding guarantees linked to an external referent", i.e. with
  the index-linked crediting stripped out. That exclusion is the **only** index-specific
  reserve rule in the item; every rate, table and factor it uses is delegated to **A-820**
  by year of issue [REG-R155] [REG-R153] [REG-R110]. Mechanics, the alternative minimum
  reserve and the A-830 ULSG branch are read at first hand in
  `_research/appp-a585-a250-a255-a270.md` and `_research/appp-a830.md`.
- **Nonguaranteed elements.** Caps, participation rates, declared rates, COI rates, and
  loads are NGEs; determination and revision practice is governed by ASOP No. 2 [REG-R26].
- **Federal tax.** §7702 definition of life insurance (CVAT or GPT+corridor; floating
  "insurance interest rate" replacing fixed 4%/6% for post-2020 issues) [R4]; §7702A MEC
  7-pay test with §72 taxation of MEC distributions [R5]; tax reserves per IRC §807
  (greater of net surrender value and 92.81% of the NAIC-method reserve, capped at
  statutory) [REG-R16].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-indexed_ul-r1
[R10]: #uslib-indexed_ul-r10
[R2]: #uslib-indexed_ul-r2
[R3]: #uslib-indexed_ul-r3
[R4]: #uslib-indexed_ul-r4
[R5]: #uslib-indexed_ul-r5
[R6]: #uslib-indexed_ul-r6
[R8]: #uslib-indexed_ul-r8
[REG-R1]: #uslib-reg-r1
[REG-R10]: #uslib-reg-r10
[REG-R110]: #uslib-reg-r110
[REG-R153]: #uslib-reg-r153
[REG-R155]: #uslib-reg-r155
[REG-R16]: #uslib-reg-r16
[REG-R17]: #uslib-reg-r17
[REG-R18]: #uslib-reg-r18
[REG-R19]: #uslib-reg-r19
[REG-R26]: #uslib-reg-r26
[REG-R3]: #uslib-reg-r3
[REG-R30]: #uslib-reg-r30
[REG-R5]: #uslib-reg-r5
[REG-R7]: #uslib-reg-r7
[REG-R9]: #uslib-reg-r9
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
