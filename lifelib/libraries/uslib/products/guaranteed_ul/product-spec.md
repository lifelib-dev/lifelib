# Product Specification

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03).

Scope note: this is a standardized composite specification assembled for reference
liability-modeling purposes. It does not describe any single insurer's product.
Facts carrying a source tag ([S#] = product source, [R#] = regulatory/actuarial source,
both per `_research/guaranteed-ul.md`; [REG-R#] = cross-product reference library
`references/regulatory-and-actuarial-references.md`, research provenance in
`_research/regulatory-actuarial.md`, same R-numbering) were extracted from retrieved
documents. Items marked **[std]** are standardizations introduced for the reference
implementation; each **[std]** table row carries a footnote with the rationale and the
observed range across insurers. Items marked [unverified] were recorded in the research
notes without a verifiable retrieved source and remain flagged.

---

## Product overview and market role

Guaranteed universal life (GUL, also "no-lapse guarantee UL" or ULSG) is
flexible-premium universal life whose distinguishing feature is a secondary guarantee:
a conditional guarantee that the policy remains in force even if its fund (account)
value is exhausted [R2 VM-01 definition; S2, S4, S9](#uslib-guaranteed_ul-r2). The owner elects a guarantee
horizon — commonly anywhere from attained age 90 up to lifetime/age 121 — and funds it
with a solved level "no-lapse premium"; higher premiums buy longer guarantees or
shorter payment periods [S1], [S2], [S9]. Carriers state plainly that a policy sustained
solely by the no-lapse guarantee builds no cash value [S2] and that "cash value
accumulation is unlikely" [S7]: the product is bought as guaranteed permanent death
benefit protection, not accumulation.

Two secondary-guarantee families exist in the market and are the only two recognized
by regulation: shadow-account designs (a notional parallel account with its own loads,
charges and credited rates; the policy cannot lapse while the shadow value, net of
indebtedness, is positive) and cumulative-premium-test designs (in force while
premiums paid, less withdrawals/indebtedness, meet a required accumulated-premium
schedule) [R1 AG 38 8E Designs #1/#2; R2; S4](#uslib-guaranteed_ul-r1). Flagship lifetime-GUL products use
shadow accounts [S2], [S4], [S9]; cumulative premium tests persist as short initial
guarantees layered underneath [S4] and as the whole design for limited-duration
guarantees [S5]. The target market is risk-averse buyers of permanent protection —
estate/legacy planning at ages 45–70 and income replacement at 30–50 [S4].

The economics are lapse-supported: funded lifetime guarantees exhibit very low lapse
(lifetime-SG lapse rates run 45% below non-lifetime-SG rates on both count and amount
bases in 2015–2021 industry experience [R7]), and insurers rate lapse and tail
investment returns as the most critical ULSG assumptions [R8]. This specification
adopts the shadow-account design as representative (AG 38 8E Policy Design #1,
matching the VM-20 ULSG machinery directly [R1], [R2]) and documents the
cumulative-premium design as the principal variation.

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Product type | Flexible-premium UL with secondary guarantee (single shadow account) | [S2], [S4]; [R1] 8E Design #1; [R2] |
| Death benefit option | Level only (Option 1): DB = greater of face amount and minimum corridor death benefit | [S2], [S4] |
| Face increases | Not permitted (new policy required) | [S2] |
| Face decreases | Once per year after policy year 1, minimum decrease $1,000, not below product minimum face | [S2] |
| Issue ages | 18–80 | [S6]; [S4] (18–80 for four of six classes; S4's Standard classes extend to 85) |
| Age basis | Age nearest birthday (ANB) | [S2], [S4], [S6] |
| Underwriting classes | 4 non-tobacco (Preferred Plus, Preferred, Standard Plus, Standard), 2 tobacco (Preferred, Standard) | [S4] |
| Minimum face amount | $100,000 | [S4], [S6] |
| Maximum face amount | None | [S3] |
| Face bands (per-unit rates/charges) | Band A $100,000–$249,999; B $250,000–$499,999; C $500,000–$999,999; D $1,000,000+ | [S2], [S7]; **[std]** (note 1) |
| Premium modes | Annual, semi-annual, quarterly; monthly by EFT only; non-annual modes carry modal factors | [S2] |
| Maturity | No maturity date; premiums and all charges cease at attained age 121, coverage continues | [S7] |

**[std] notes:**
1. Band structure: two of the carriers surveyed use five bands with identical
   breakpoints from $25K/$50K up ([S2], [S7]). Because the representative minimum face
   is $100,000 [S4], [S6], the sub-$100K band is dropped and the remaining four sourced
   breakpoints are kept. Observed minimum faces range $25,000 [S2] to $100,000
   [S4], [S6].

### Secondary guarantee

| Parameter | Representative value | Basis |
|---|---|---|
| Guarantee mechanism | Single shadow account (notional "guarantee value") with its own premium load, charges and credited rate | [S2], [S4], [S9]; [R1] 8E #1; [R2] |
| In-force test | Policy cannot lapse while shadow account value minus policy indebtedness > 0 | [S4] (indebtedness deduction); [S2], [S9] |
| Guarantee duration election | Owner elects any attained age from 90 to 121 (lifetime) at issue | [S1], [S2], [S9] |
| Funding | Level "no-lapse guarantee premium" solved at issue so the shadow account stays positive to the elected guarantee age | [S1], [S2]; solve mechanics **[std]** (note 1) |
| Guarantee scope | Death benefit only; the guarantee provides no cash or surrender value | [S2], [S3] |
| Premium timing tolerance | Premiums up to one month early or one month late do not impair the guarantee | [S9] |
| Catch-up | Unlimited right to restore a lapsed guarantee by paying the accumulated shortfall (shadow-account deficit grossed up for the shadow premium load) | [S2], [S7] (restoration permitted, cost may exceed illustrated premiums); [R1] example 7 (unlimited catch-up = unexpired SG); formula **[std]** (note 2) |
| Effect of withdrawals | Withdrawals reduce the shadow account dollar-for-dollar | [S4] (partial surrenders subtract from guarantee measure); exact treatment **[std]** (note 3) |
| Effect of loans | Indebtedness is deducted from the shadow account in the in-force test (guarantee value itself not reduced) | [S4], [S2] |

**[std] notes:**
1. Carriers publish only that a level guaranteed premium exists for the elected
   duration [S1], [S2], [S7]; no public document discloses the solve. The reference
   implementation solves by bisection/secant on a level premium (technical notes,
   "Funding-premium solve"). Observed market framing ranges from continuous duration
   election [S1], [S2], [S9] to a discrete menu (age 90/95/100/105/110/121) [S8].
2. No retrieved contract text discloses a catch-up formula (specimen policy forms were
   not retrievable — research Gaps). The [std] formula (shortfall = negative net
   shadow balance, i.e. shadow value less indebtedness, grossed up for the shadow
   premium load) is the minimal design consistent
   with AG 38's treatment of unlimited catch-up rights [R1] and with carrier
   statements that restoration premiums "may be significantly higher than the premiums
   illustrated" [S7].
3. Observed range: withdrawals reduce the guarantee measure (one carrier subtracts
   partial surrenders and fees [S4]; two others state that loans and withdrawals
   impair the guarantee value or duration [S2], [S3], [S7]); another carrier's
   premium-test design subtracts withdrawals from premiums paid [S5]. Dollar-for-dollar
   reduction of the shadow account is the simplest representative treatment.

### Base (real) account parameters

| Parameter | Representative value | Basis |
|---|---|---|
| Premium expense charge (load) | 25% of every premium, all years | [S3], [S7] |
| Monthly per-policy charge | $5.50 per month, ceasing at attained age 121 | [S3], [S7] |
| Monthly per-unit expense charge | $0.20 per $1,000 of initial face amount per month, all years to age 121 | **[std]** (note 1) |
| Guaranteed maximum COI rates | 2017 CSO, sex-distinct, smoker-distinct, ANB, converted to monthly rates | **[std]** (note 2); [R3] (maxima must be stated in policy); [REG-R17] |
| Current COI rates | 65% of guaranteed maximum, all durations | **[std]** (note 3) |
| Guaranteed minimum credited rate | 2.0% annual effective | [S3], [S5], [S7] |
| Current credited rate | 3.5% annual effective (declared; snapshot) | **[std]** (note 4) |
| Charge cessation | All charges cease at attained age 121 | [S3], [S7] |

**[std] notes:**
1. Per-unit charge structure (monthly, per $1,000 of initial face, varying by
   age/sex/class) is sourced [S3], [S7]; no carrier publishes the scale. $0.20/month is a
   single representative level chosen so total non-COI charges are material but
   secondary to COI; the observed range is undisclosed (only the structure is public).
2. Model 585 requires guaranteed maximum mortality charges to be stated in the policy
   [R3]; carriers do not publish their COI tables (research Gaps). Using the statutory
   valuation table (2017 CSO [REG-R17]) as the contractual maximum is the
   standardization; it makes the guaranteed basis reproducible from public tables.
3. Current COI scales are not published by any carrier (research Gaps). A flat 65% of
   the CSO maximum is a standardization chosen to give realistic positive spread
   between guaranteed and current bases; no observed range is available.
4. Current credited rates are discretionary and reset periodically [S3], [S5]; levels are
   not published in the retrieved documents. 3.5% is a snapshot standardization 150 bps
   above the sourced 2.0% guaranteed floor [S3], [S5], [S7].

### Shadow account parameters (all standardized)

Public documents do not disclose shadow-account parameters for any carrier; only the
charge/credit categories are described [S4], [S9] and AG 38 8E caps guaranteed
shadow-account interest credits at a Moody's-composite-yield-based index + 3% for
reserve classification [R1]. The reference implementation therefore uses the following
**[std]** parametrization, calibrated so that the solved level no-lapse premium is in
the range of observed market premiums for lifetime-guarantee GUL (see technical notes,
"Calibration").

| Parameter | Representative value | Basis |
|---|---|---|
| Shadow premium load | 8% of every premium, all years | **[std]** (note 1) |
| Shadow credited rate (guaranteed) | 5.5% annual effective, all years | **[std]** (note 2) |
| Shadow COI rates | 55% of 2017 CSO guaranteed maximum (same table basis as base account) | **[std]** (note 3) |
| Shadow per-unit charge | $0.05 per $1,000 of initial face per month | **[std]** (note 4) |
| Shadow per-policy charge | None | **[std]** (note 5) |
| Shadow charge cessation | Age 121 (same as base) | **[std]** (note 5) |

**[std] notes:**
1. No shadow load is published anywhere (research Gaps). 8% sits near the 7% "average
   premium load level" AG 38 8B uses as its market-wide load allowance [R1], and well
   below the 25% base-account load [S3], [S7] — the shadow account must credit premiums
   more generously than the base account for the guarantee to outlast the cash value.
2. Guaranteed shadow credits are contractual internal parameters, distinct from the
   base credited rate [R2 shadow-account definition; S4 mechanics](#uslib-guaranteed_ul-r2); AG 38 8E caps them
   at Moody's composite corporate yield + 3% for Design #1 classification [R1]. 5.5%
   is a standardization comfortably below plausible values of that cap and above the
   2.0% base guarantee [S3], [S5], [S7], producing the long-lived guarantee value the
   design requires.
3. Not disclosed publicly. 55% of the CSO maximum keeps shadow COI below current base
   COI (65% [std]) so the shadow account depletes more slowly than the base account —
   the defining behavior of the product [S2], [S7].
4. Not disclosed publicly; a nominal per-unit charge is retained so the shadow account
   is not charge-free (AG 38 8E describes shadow accounts with expense charges [R1]).
5. Not disclosed publicly; omitting a per-policy shadow charge is the simplest
   representative choice.

### Surrender values, return of premium, loans, withdrawals, grace

| Parameter | Representative value | Basis |
|---|---|---|
| Surrender charge period | 15 years, declining linearly to zero | **[std]** (note 1) |
| Surrender charge amount | SC(t) = $18 per $1,000 of face × max(0, (180 − t)/180), t = policy month | **[std]** (note 1) |
| Return of premium (ROP) endorsement | Exercise during the 60 days following policy anniversaries 20 (refund 50% of premiums paid) and 25 (100% of premiums paid); refund capped at 40% of face amount; full surrender required | [S1] (percentages, anniversaries, 40%-of-face cap); [S3], [S4] (60-day window mechanics) |
| Withdrawals (partial surrenders) | Available after policy year 1; $25 fee per withdrawal; minimum $500; maximum = net surrender value less the greater of $500 or three months of deductions; may reduce face amount and impairs the guarantee | [S2], [S3], [S4], [S7] (availability/fee); [S4] (min/max) |
| Policy loans | Available after policy year 1; loan interest 5.0% annual charged in arrears; loaned account value credited 3.0%, both guaranteed | [S4] |
| Maximum loan | Net surrender value less three months of deductions | [S4] |
| Grace period | 61 days from the monthiversary on which net cash value cannot cover the monthly deduction and the guarantee is not in effect; written notice required | [S7]; [R3] (minimum 30 days + notice) |
| Reinstatement | Within 3 years of lapse, with evidence of insurability and payment of required premiums; guarantee restored only via catch-up payment | **[std]** (note 2) |
| Contestability / suicide | Two years | [S3] |
| Misstatement of age/sex | Benefit adjusted using the most recent mortality charge basis | [S3]; [R3] |

**[std] notes:**
1. Observed surrender-charge periods span the full range: none [S7], 9 years [S3],
   19 years (also applied to face decreases and withdrawals) [S2], 20 years [S4].
   A 15-year linearly declining schedule is chosen as a mid-range representative;
   the $18/$1,000 initial level is a standardization (carriers do not publish scales,
   which vary by age/sex/class [S3]).
2. Reinstatement terms were not captured in any retrieved document (specimen policy
   forms unavailable — research Gaps). A 3-year reinstatement right with evidence and
   back-payment is standard UL policy language; treat the details as [std].

---

## Contractual mechanics

Notation here matches the technical notes; both documents use the same representative
parameter values.

### Premium provisions

Premiums are flexible in amount and timing after the first premium [S2], [S4]. The
policy is illustrated and sold with a level no-lapse guarantee premium `P*` solved for
the elected guarantee age; paying more than `P*` shortens the payment period or
extends/pre-funds the guarantee, and single-pay/1035 funding is an explicit design
"sweet spot" [S1], [S2]. Each premium is subject to the premium expense charge: net
premium to the account value is `(1 − 0.25) × P` [S3], [S7], and net premium to the
shadow account is `(1 − 0.08) × P` **[std]**. Premiums paid within one month of the
scheduled date do not impair the guarantee [S9]. Premium payments are permitted to
attained age 121, when charges cease [S7]; cf. premiums-to-120 with maturity extension
in one observed design [S4].

### Death benefit provisions

Level option only: `DB_t = max(F, κ(x_t) × AV_t)` where `F` is face amount and
`κ(x_t)` is the applicable corridor factor at attained age `x_t` required for the
guideline premium test [S2, S4 level-only design; R4 corridor requirement]. Because
GUL account values are deliberately thin, `DB_t = F` in almost all months. The death
proceeds equal `DB_t` less outstanding indebtedness and any due and unpaid charges
**[std]** (standard UL practice; the retrieved documents state indebtedness/unpaid-
charge offsets expressly only for the ROP refund [S4], not for death proceeds).

### Account value mechanics (base account)

On each monthiversary, in order: (1) net premium credited; (2) per-policy and per-unit
expense charges deducted; (3) cost of insurance deducted, computed on the net amount
at risk `NAAR_t = max(DB_t/(1+j) − max(AV_t', 0), 0)` where `j` is the monthly
equivalent of the 2.0% guaranteed rate and `AV_t'` is the account value after steps
(1)–(2), floored at zero so an exhausted account never inflates the NAAR; (4)
interest credited at the declared rate (guaranteed floor 2.0% [S3], [S5], [S7]), with the
loaned portion credited at the guaranteed loaned rate 3.0% [S4]. The full recursion,
including the flooring of `AV` at zero while the guarantee is active, is specified in
the technical notes. Structure of the charge deductions follows the sourced charge
lists [S2], [S3], [S4], [S7]; the processing-order details are **[std]**.

### Shadow account mechanics

The shadow account `SG_t` is a notional account that "typically consist[s] of premium
and interest credits and cost of insurance and expense charges" [R2] and exists only
to run the in-force test — it is never payable [S2], [S3]. It follows the same monthly
recursion as the base account but with the shadow parameter set ([std] table above)
and is not floored at zero: a negative balance measures the catch-up shortfall. The
policy cannot lapse while `SG_t − L_t > 0`, where `L_t` is the loan balance
[S4; S2, S9].

### Charges and credits

All charge categories are sourced: premium expense charge, monthly COI, monthly
administrative (per-policy) charge, monthly expense (per-unit) charge, rider charges
[S2], [S3], [S4], [S7], [S9]. Guaranteed maxima for charges and guaranteed minimum interest
must be stated in the policy, and interest credits may not remain conditional longer
than 24 months [R3]. Current (non-guaranteed) COI and credited scales are declared at
insurer discretion subject to the guaranteed bounds; determination of such
nonguaranteed elements is governed by ASOP No. 2 [REG-R26].

### Loans

After year 1, the owner may borrow up to the net surrender value less three months of
deductions [S4]. Loan interest of 5.0% accrues in arrears; the loaned portion of the
account value is credited at a guaranteed 3.0% (200 bps guaranteed spread) [S4].
Indebtedness is deducted from the guarantee in-force test (subtracted from the
shadow account) [S4]; its deduction from death proceeds and the surrender value is
standard UL treatment **[std]**. Observed variation: 300 bps spread
(5%/2%) [S7]; adjustable declared loan rates [S5]; and one design in which any loan
voids the guarantee outright [S5].

### Withdrawals

After year 1; $25 fee each [S2], [S3], [S4], [S7]; minimum $500, maximum = net surrender
value less the greater of $500 or three months of deductions [S4]. A withdrawal
reduces the account value dollar-for-dollar plus fee, may reduce the face amount
(never below the product minimum [S4]), reduces the shadow account dollar-for-dollar
**[std]** (see note 3 under "Secondary guarantee"), and within the surrender-charge
period may trigger a surrender charge in some observed designs [S2].

### Grace, lapse and reinstatement

On a monthiversary where net cash value (account value less surrender charge less
indebtedness) cannot cover the monthly deduction AND the guarantee is not in effect
(`SG_t − L_t ≤ 0`), the policy enters a 61-day grace period [S7]. Lapse occurs only if
the grace period expires without payment of the required premium. While the guarantee
is in effect, exhaustion of the account value does not trigger grace — the account
value is floored at zero and coverage continues [S2], [S3], [S9]. A lapsed policy may be
reinstated within 3 years **[std]**; the guarantee itself is restored only by paying
the catch-up shortfall [S7; R1 example 7; formula **[std]**].

### Renewal / conversion / maturity

Not a renewable-term structure: coverage is permanent. There is no maturity date;
at attained age 121 premiums and charges cease and coverage continues [S7] (observed
variation: maturity at 120 with a maturity-extension provision [S4]). No conversion
features apply to the base contract.

---

## Riders

### In scope for the reference implementation

- **Terminal illness accelerated death benefit.** Prepayment of up to 75% of the death
  benefit, maximum $500,000, on a life expectancy of 12 months or fewer [S2], [S9].
  No premium; benefit modeled as an actuarial discount of the death benefit — the
  reference model treats acceleration as neutral to gross liability cash flows
  **[std]** (see technical notes).
- **Return of premium endorsement.** Built into the representative contract (see
  specification table): 50%-of-premium refund at anniversary 20, 100% at anniversary
  25, capped at 40% of face [S1], 60-day exercise windows [S3], [S4]. Modeled as an
  elevated-surrender event with a distinct surrender benefit.

### Out of scope (listed for completeness; all observed in retrieved documents)

- Chronic illness accelerated benefit riders (2-of-6 ADL / severe cognitive
  impairment triggers; per-diem caps) [S1], [S2], [S5], [S7], [S9]
- Long-term care rider (true LTC, including informal care) [S4]
- Longevity/income riders: death benefit converted to income from age 85 [S1];
  guaranteed installment death benefit payout endorsements [S4], [S7]
- Waiver of monthly deductions during disability [S2], [S4], [S5] — note the guarantee
  gap: one observed design waives monthly deductions but not the full no-lapse
  premium [S4]
- Waiver of specified premium [S7]; disability completion benefit [S5]
- Children's term riders with conversion privileges [S2], [S5], [S9]
- Accidental death benefit; additional insured term; guaranteed increase option;
  overloan protection; business exchange riders [S4], [S5], [S6]

---

## Variations across insurers

1. **Guarantee mechanism.** Shadow accounts dominate flagship lifetime GUL
   ("extended no-lapse guaranteed value" [S4]; "net no-lapse guarantee value"
   [S2], [S9]); cumulative-premium tests appear as 5-year initial guarantees layered
   under the shadow account [S4] and as the entire design for limited (≤30-year)
   guarantees [S5]. Regulation recognizes exactly these two families and treats
   multi-charge-set variants punitively [R1 Designs #1–#3; R2](#uslib-guaranteed_ul-r1). **Choice:** single
   shadow account — it is the flagship-product design and maps 1:1 onto AG 38 8E
   Design #1 and the VM-20 ULSG NPR machinery [R1], [R2], which the reference library
   must exercise. The cumulative-premium test is documented as the main variation: in
   that design the in-force test is `cumulative premiums paid − withdrawals −
   indebtedness ≥ required accumulated premium schedule` [S4, S5; R1 Design #2], and
   the technical notes state how to swap it in.
2. **Guarantee duration menu.** Continuous election through funding [S1], [S2], [S9]
   vs. discrete menu 90/95/100/105/110/121 [S8] vs. dual chassis age-120/age-70 with
   an upgrade option [S4] vs. hard 30-year cap [S5]. **Choice:** continuous election
   age 90–121 (superset of the menus; the solve is identical).
3. **Loans vs. the guarantee.** Mainstream: indebtedness deducted from the guarantee
   value [S2], [S4]. Harshest: any loan nullifies the guarantee [S5]. **Choice:**
   indebtedness deduction — it is the majority design and keeps loan utilization
   modelable rather than terminal.
4. **Missed premiums.** Some designs shorten the guarantee age gracefully (guarantee
   to 105 falling to 96 after two skipped premiums [S3]); shadow-account designs
   re-derive the horizon endogenously — a shortfall shows up as earlier shadow
   exhaustion. **Choice:** endogenous (shadow-account) treatment; the catch-up
   provision restores the original horizon [S7; R1].
5. **Surrender charges.** Observed: none [S7]; 9 years [S3]; 19 years including
   withdrawals/face decreases [S2]; 20 years [S4]. **Choice:** 15-year declining
   **[std]** — mid-range, long enough to interact with the ROP windows.
6. **ROP exit windows.** Nearly universal but heterogeneous: years 15/20/25 by band
   [S2], [S9]; 16/21 [S4]; 20/25 [S1]; 21/26 [S3]; flat 25% any time after year 10
   [S7]. Caps: 40% of face/DB [S1], [S2], [S4] vs. 50% of lowest DB [S3], [S7].
   **Choice:** 20/25 with 40%-of-face cap [S1] — the built-in (no-election) variant
   with the modal cap.
7. **Death benefit options.** Guarantee-focused carriers restrict to level-only
   [S2], [S4]; accumulation-oriented designs keep level + increasing [S5]. **Choice:**
   level-only, matching the guarantee-focused segment and the task of modeling
   protection business.
8. **Charge transparency.** One carrier publishes its load structure (25% load,
   $5.50/month) [S3], [S7]; others disclose categories only [S2], [S4]. No carrier
   publishes COI tables or shadow parameters — hence the **[std]** parametrization
   above.

---

## Regulatory context

**NAIC Model 585 (Universal Life Insurance Model Regulation).** Provides the UL
chassis rules: definitions, CRVM-for-UL valuation via the guaranteed maturity
premium/fund with the r-ratio, retrospective minimum nonforfeiture values, mandatory
policy provisions (stated guaranteed maxima/minima, ≥30-day grace with notice, annual
reports, disclosure that coverage may not continue to maturity even if scheduled
premiums are paid), and a drafting note that secondary guarantees "should be taken
into consideration" for minimum nonforfeiture benefits. Its low-cash-value clause lets
the commissioner require higher cash values where substantially level benefit charges
develop little or no cash value — directly relevant to thin-AV GUL designs.
[R3; REG-R5](#uslib-guaranteed_ul-r3)

**AP&P Appendix A-830 (cited in this library until 2026-08-06 as Model 830, "Regulation XXX")
+ Actuarial Guideline 38 ("AXXX").** For
policies issued before PBR (and in-force blocks), the appendix sets minimum reserves for UL
with provisions letting a policyholder keep the policy in force over a secondary guarantee
period, and AG 38 interprets it for secondary guarantees. **Citation correction, from the AP&P
print read at first hand on 2026-08-06:** the appendix is a **flat sequence of paragraphs
¶¶1–32 plus an unnumbered Attachment and has no Sections at all**, and the words "Model #830"
and "Regulation XXX" appear nowhere in it — the ULSG material is at **¶¶29–32**, so the
"Model 830 Section 7" citation this specification previously carried does not resolve against
this text. (It may still resolve against the separately published model regulation [REG-R6];
that was not re-read against the appendix print, so no view is taken.) [REG-R154]

What ¶¶29–32 prescribe: basic reserves for the secondary guarantee are the **segmented
reserves over the secondary guarantee period**, computed with gross premiums **set equal to
the specified premiums, if any, or otherwise to the minimum premiums**, on segments from the
¶5 contract segmentation method — **no unitary leg**; deficiency reserves run the ¶22
construction on the same substitution; and the minimum reserve during the guarantee period is
the greater of that sum and "the minimum reserves required by other appendices governing
universal life plans", a limb the appendix **does not name** and which must not be resolved to
A-585. Where more than one secondary guarantee is unexpired, the reserve is the **greatest of
the stand-alone reserves of each, every one valued ignoring the others**. A **scope test this
specification did not previously carry**: a UL policy is outside the appendix entirely where
**all three** of ¶3.a.ii hold — secondary guarantee period **five years or less**, specified
premium not less than the net level reserve premium for that period, and initial surrender
charge not less than **100% of the first-year annualized specified premium**. The
representative lifetime guarantee is inside the appendix on the first limb alone. A-830's own
basic reserves, deficiency comparator and maximum valuation interest rates are cross-references
into **A-820** ¶¶11–13, ¶¶19–20 and ¶¶7–10, also now read. [REG-R154 ¶¶3.a.ii, 4, 6, 8, 29–32;
REG-R153](#uslib-reg-r154)

AG 38 then supplies what A-830 contains **nothing** of — no shadow account, no funding ratio,
no minimum-gross-premium definition, no 8C/8D/8E analogue [REG-R154]: the reserve interpolates
between basic+deficiency reserves and the net
single premium for the guarantee via a funding ratio measured on the shadow account or
excess cumulative premiums (with a 7% load allowance), less an adjusted
surrender-charge offset, under prescribed conservative lapse (2%/1%/0% patterns).
Section 8E (issues on/after 1/1/2013) defines minimum gross premiums per policy
design — Design #1 is exactly this specification's shadow account — and caps
guaranteed shadow credits at a Moody's-based index + 3%. [R1; REG-R6; REG-R7](#uslib-guaranteed_ul-r1)

**NAIC Valuation Manual — VM-01/VM-20 (PBR).** VM-01 defines "secondary guarantee" and
"shadow account"; ULSG is its own VM-20 reserving category with reserve = NPR floor
plus excesses of deterministic and stochastic reserves. The ULSG NPR during the SG
period is the greater of an SG-based amount — min(ASG/FFSG, 1) × NSP − amortized
expense allowance — and the non-SG amount, with a prescribed dynamic lapse formula
driven by the funding ratio. Material-SG business cannot use the life PBR exemption
and generally cannot avoid deterministic/stochastic modeling. [R2; R9; REG-R3;
REG-R23](#uslib-guaranteed_ul-r2)

**NAIC Model 787 / AG 48 (reserve financing).** ULSG "redundant" reserve financing
through captives is constrained: Primary Security must at least equal a VM-20-based
Required Level (greater of DR and NPR; greatest of DR/SR/NPR if the stochastic
exclusion fails), with reserve credit disallowed on non-compliance. AG 48 applied the
framework before state adoption of Model 787. [R6; REG-R11; REG-R12](#uslib-guaranteed_ul-r6)

**IRC 7702 / 7702A.** The contract must qualify as life insurance via CVAT or
GPT + corridor; level-DB GUL is typically GPT/corridor-tested [R4 for the tests;
design attribution](#uslib-guaranteed_ul-r4) [unverified]. The 2021 change to dynamic "insurance interest
rates" (2% transition rate for 2021) materially affects GUL premium/corridor limits
[R4; REG-R13](#uslib-guaranteed_ul-r4). Heavy prefunding (single-pay/short-pay, the 1035 "sweet spot" [S2])
can create a MEC under the 7702A 7-pay test, taxing loans/withdrawals income-first
with a 10% additional tax before age 59½; benefit reductions within 7 years force
retesting [R5; REG-R14; S4](#uslib-guaranteed_ul-r5). Accelerated benefit riders are designed to qualify under
IRC 101(g) [S1], [S2].

**Illustrations and NGE governance.** GUL is general-account (not variable) business:
the Illustrations Model Regulation applies (disciplined current scale, self-support
and lapse-support certification) [REG-R4; REG-R30](#uslib-reg-r4), and insurer determination of
current COI/credited scales is governed by ASOP No. 2 [REG-R26]. Note that GUL is not
SEC-registered; no prospectuses exist on EDGAR (verified empirically in the research
notes).

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-guaranteed_ul-r1
[R2]: #uslib-guaranteed_ul-r2
[R3]: #uslib-guaranteed_ul-r3
[R7]: #uslib-guaranteed_ul-r7
[R8]: #uslib-guaranteed_ul-r8
[REG-R154]: #uslib-reg-r154
[REG-R17]: #uslib-reg-r17
[REG-R26]: #uslib-reg-r26
[REG-R6]: #uslib-reg-r6
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
