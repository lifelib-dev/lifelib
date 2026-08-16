# Product Specification

**Status:** Draft, 2026-08-04 (all cited sources accessed 2026-08-04).

**Scope note.** A *standardized composite specification* for reference liability cash-flow
modeling; it describes no single insurer's product. Tags: **[S#]** / **[R#]** = primary product
documents / regulatory-actuarial references numbered per `_research/fixed-indexed-annuity.md`;
**[REG-R#]** = the cross-product library `references/regulatory-and-actuarial-references.md`,
whose shared numbering now runs **R1–R157** with most of the **R73–R149** block unused —
R1–R34 originating in `_research/regulatory-actuarial.md` and R35–R72 in
`_research/regulatory-actuarial-annuities.md`. **[std]** marks standardizations
introduced for the reference implementation, each with a footnote under its table giving the
rationale and the observed range; [unverified] marks claims the research file could not confirm
against a retrieved document.

**Chassis.** The base contract is a single-premium deferred annuity on the fixed-deferred chassis
— surrender charge mechanics and the Model #805 nonforfeiture floor — documented in
`_research/fixed-deferred-annuity.md` and `products/fixed_deferred_annuity/`, whose
*structure* is **referenced, not restated** (the parameters below are this composite's own, and
the schedules, rates and the account-value roll-forward are stated here in full). **Terminology
bridge:** the Model #805 floor is called the **guaranteed minimum value (`MGV`)** here, after
[S10]; `products/fixed_deferred_annuity/` calls the identical quantity the **minimum
guaranteed surrender value (`MGSV`)**, after its own specimen. Same concept, different source
labels — do not model them as two quantities. Two base-contract items are **restated rather than
inherited**,
because the FIA composite selects differently from the fixed-deferred composite: the **MVA family**
(ratio-of-yield-factors [S10] here, against the linear `(i₀ − iₜ) × T` form with a symmetric
surrender-charge cap adopted in `products/fixed_deferred_annuity/product-spec.md`) and the
**death benefit** (`max(account value, guaranteed minimum value)` [S1] [S2] [S5] [S10] here, against
full account value floored at the cash surrender benefit there — numerically the same whenever the
MVA cannot lift the surrender value above the account value, but stated differently). The new
material is index crediting, the premium bonus with vesting and clawback, and the GLWB rider. Index
segment vocabulary is shared with `products/indexed_ul/technical-notes.md`, but an FIA has **no
cost of insurance, no net amount at risk and no death benefit corridor**, and its rider is a
**guaranteed lifetime withdrawal benefit, not a no-lapse guarantee**.

---

## Product overview and market role

An FIA is a general-account, non-registered deferred annuity whose credited interest is linked to
an external index by a formula with a contractual floor, typically 0% [S1] [S6] [S10] [R1]. The
holder is never invested in equities: "The IndexMax ADV 5 is not a registered security and does
not directly participate in stock or equity investments. Index returns do not include dividends"
[S6]; two other currently-sold disclosure documents state the contract is not a security and is
not registered under the Securities Act of 1933 [S9] [S10]. The insurer invests most of the premium
in fixed income and allocates the remainder to an **option/hedge budget** to buy the index
exposure [R1]. The Academy records 2023 U.S. FIA sales of **$95.6 billion**, up 20% year over year
(citing LIMRA) [R1]; the 2023 SOA/LIMRA study covered 17 companies, 57% of new sales and 58% of
assets in force, 2.7 million contracts and $328 billion of surrender exposure [R9].

A GLWB rider is "one of the most popular optional features in FIAs today," paying for life "even
if their account balance is reduced to $0" while — unlike annuitization — leaving the owner access
to the account balance [R1]. It is the economic centre of the product: it converts a savings
vehicle into a deferred-income guarantee whose cost is realised in the tail, when the account
value is exhausted and the insurer pays from its own funds [S1] [S3] [S9] [R1]. It also changes
behaviour — in the year the surrender charge expires the surrender rate was **10% for contracts
with a GLWB rider versus 33% without** [R8].

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Single-premium deferred fixed indexed annuity, general account, not SEC-registered | [S1] [S2] [S6] [S9] [S10] [R1] |
| Premium pattern | Single premium only | [S1] [S2] [S6] [S10]; choice **[std]** (1) |
| Issue ages | 40–80 | [S2] [S3] [S5] [S8] [S10]; band **[std]** (2) |
| Single premium (anchor cell) | $100,000 | **[std]** (2) |
| Minimum / maximum premium | $20,000 / $1,000,000 | [S3] [S8] / [S1] [S2] [S3] |
| State basis | One composite state basis; no state variations modeled | **[std]** (3) |
| Free look | 30 days, refund of premium less withdrawals, excluding the bonus | [S6] [S10] |
| Anchor model cell | Male 62 ANB, single life, $100,000, GLWB elected at issue, lifetime withdrawals from attained age 70 | **[std]** (3) |

1. Observed: single premium only [S1] [S2] [S6] [S10]; flexible premium [S8]; additional premium for
   18 months in $25–$25,000 increments [S3]. Single chosen: subsequent deposits occur on 2.5% of
   contracts in years 2–10, 1.9% *with* a GLWB [R8].
2. Observed issue ages: 35–80 / 35–74 by state group [S2]; maximum 80 [S3]; 18–80 with the rider
   issued 50–80 [S5]; 40–79 and 40–75 [S8]; through 80 implied by the bonus tiers [S10]. 40–80
   spans every income-rider window; $100,000 sits inside all observed minimums ($10,000, $5,000 in
   listed states [S1] [S2]; $20,000 [S3] [S8]) and maximums.
3. State variation materially changes parameters — three Athene charge groups plus a California
   schedule [S2]; Midland CA/DE re-entry schedules and a CA-specific MVA collar [S6] [S7];
   Allianz's state-specific charge naming [S3] — so the research file recommends picking one
   basis. Issue at 62 with income at 70 puts the first withdrawal where utilization concentrates:
   withdrawal rates rise with attained age and are highest for qualified contracts at 70+ on RMDs
   [R1].

### Account structure and index crediting

| Parameter | Representative value | Basis |
|---|---|---|
| Accounts available | One fixed account plus one indexed account: S&P 500 annual point-to-point with cap | [S1] [S2] [S4] [S10]; simplification **[std]** (4) |
| Baseline allocation | 100% indexed | **[std]** (4) |
| Index | S&P 500 price index; dividends excluded | [S2] [S6] [R1] |
| Crediting method | Annual point-to-point, cap and floor | [S2] [S4] [S10] [R1] |
| Declared annual cap (snapshot, non-guaranteed) | 5.25% | [S2]; selection **[std]** (5) |
| Guaranteed minimum annual cap | 0.25% | [S4]; selection **[std]** (5) |
| Index credit floor | 0% | [S1] [S4] [S10] [R1] |
| Fixed account declared rate (snapshot) | 2.30% | [S2] |
| Fixed account guaranteed minimum rate | 1.00% | [S10]; selection **[std]** (6) |
| Reallocation | Permitted at each contract anniversary | [S1] [S5] |
| Bailout cap rate | Contract-stated; 1.00% declared in the 2022 rate sheet; not modeled | [S1] [S2]; scope **[std]** (6) |
| Allocation / strategy charge | 0% | current 0%, maximum 2.5% observed [S3] [S4]; choice **[std]** (6) |

4. Observed: six index strategies plus a fixed strategy [S2]; monthly-sum, annual and 2-/5-year
   participation methods [S4]; one fixed and three "Extendable" indexed accounts [S10]. One
   indexed account keeps the reference recursion to a single annual segment; the rest are
   variations.
5. Declared caps observed: **5.25%** on the S&P 500 1-year point-to-point [S2, effective
   07/01/2022](#uslib-fixed_indexed_annuity-s2) and **4.50%** [S4]; guaranteed minimum annual caps **0.25%** [S4] and **0.50%**
   [S10]. The higher declared cap with the lower guaranteed minimum maximises the
   guaranteed-versus-current gap the model must exercise; all are NGEs revisable under ASOP No. 2
   [R6].
6. Fixed-account guaranteed minimums observed: 0.10% [S4], 0.25% [S6], 1.00% [S10] — second-order
   at a 100% indexed baseline. The bailout provision (charge-free access to the accumulated value
   for 30 days after an anniversary at which the declared cap falls below the contractual bailout
   cap [S1]) is a real option against cap-setting discretion, described but not projected.
   Allianz's allocation charge (0% current, 2.5% maximum, on point-to-point allocations, deducted
   from the accumulation value and in most states the guaranteed minimum value) [S3] [S4] and
   Nassau's "Strategy Fee Amounts" [S9] are set to zero so the rider charge is the only explicit
   deduction.

### Premium bonus, vesting and clawback

| Parameter | Representative value | Basis |
|---|---|---|
| Premium bonus rate `b` | 7% of the single premium | [S5]; selection **[std]** (7) |
| Credited to | Account value at issue, allocated as the premium is allocated | [S5] |
| Vesting vector (contract years 1–11+) | 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100% | [S5] |
| Vesting on death | 100% immediately | [S5] |
| Non-vested bonus recovery | `(1 − A) × [B / (1 + B)] × C`, A = vested %, B = bonus %, C = gross withdrawal less free withdrawal amount | [S10] |
| Free-withdrawal protection | The vested amount cannot be forfeited by a free withdrawal | [S5] |
| Bonus excluded from the nonforfeiture base | Yes | [S10] |

7. Observed **account-value** bonuses with vesting: 3% [S2], 7% [S5], 16% (issue age ≤75) / 14%
   (76–80) [S10]. Observed **benefit-base-only** bonuses: 25% of premium paid in the first 18
   months [S3], 45% [S4], 2% of the GLWB value [S8]. The composite takes the middle account-value
   design (7% [S5]) with its vesting vector [S5] and the verbatim clawback formula [S10]. **Note
   the `B/(1+B)` factor** — it strips the bonus out of a bonus-inclusive account value; applying
   `B` directly over-recovers. Worked at [S10]: contract year 5, bonus 16%, gross $100,000, free
   $7,000 → 70% × 0.1379 × $93,000 = **$8,979**.

### Surrender, withdrawal, MVA, guaranteed minimum value

| Parameter | Representative value | Basis |
|---|---|---|
| Surrender charge, contract years 1–10 | 9.1, 9, 8, 7, 6, 5, 4, 3, 2, 1%; 0% thereafter | [S5]; selection **[std]** (8) |
| Surrender charge base | (gross withdrawal − free withdrawal amount) × charge % | [S10] |
| Free withdrawal amount | 10% of the account value at the preceding anniversary, from contract year 1; no carry-forward | 10% [S1] [S3] [S5] [S6]; year 1 [S1]; base and no carry-forward [S9] [S10]; combination **[std]** (9) |
| MVA period | The 10-year surrender charge period | [S7] [S10] |
| MVA formula | `(gross withdrawal − free withdrawal amount) × { [(1 + i₀)/(1 + iₜ)]^(n/12) − 1 }` | [S10]; selection **[std]** (10) |
| MVA reference index | A declared investment-grade corporate bond yield index | generic **[std]**; the linear-form products name **Barclay's US Credit Index** [S6] [S7] |
| MVA limit | `max(0, gross withdrawal − charges and adjustments − guaranteed minimum value)`; a negative MVA plus charges never reduces the surrender value below the guaranteed minimum value, and the maximum positive MVA cannot exceed the maximum negative MVA | [S10] |
| Guaranteed minimum value (MGV) at issue | 87.5% of premium, **excluding** the bonus | [S10]; 87.5% also at [S5] [S6]; Model #805 §4A(2) [R2] |
| MGV accumulation rate | 1.00% | corridor 0.15%–3% [R2] [S10]; level **[std]** (11) |
| Annual contract charge in the MGV roll | $0 | Model #805 permits $50 [R2]; choice **[std]** (11) |
| Cash surrender value | `max( account value − surrender charge − non-vested bonus recovery ± MVA , MGV )` | [S1] [S6] [S10] |
| Death benefit | `max( account value , MGV )`, 100% bonus vesting, no surrender charge or MVA | [S1] [S2] [S5] [S10] |

8. Observed 10-year schedules: 12/12/12/11/10/9/8/7/6/4 [S2] [S10]; 9.30 grading to 1.05 [S3]; 9.1
   grading to 1 [S5]; 10/10/10/10/10/9/8/6/4/2 [S8]. The research file's mainstream shape is
   "10-year surrender charge grading roughly 9–10% down to 0–1%" [S3] [S5] [S10], of which [S5] is
   the cleanest instance; five-year designs with re-entry into a fresh charge period also exist
   [S6].
9. Varies on percentage (10% [S1] [S3] [S5] [S6]; 7% [S10]; 5% [S8]), base (accumulated value
   [S1] [S5]; paid premium [S3]; beginning-of-year accumulation value [S6]; prior-anniversary daily
   accumulation value [S10]) and first availability (year 1 [S1]; year 2 [S5] [S6] [S10]). Chosen:
   the most common percentage on the most computable base, available immediately so it never binds
   against a first-year lifetime withdrawal.
10. Two verbatim formula families were retrieved: the ratio-of-yield-factors form
    `[(1+i₀)/(1+iₜ)]^(n/12) − 1` [S10] and the linear form `(i₀ − iₜ) × T` [S6] [S7]. The ratio
    form is naturally bounded; the linear form is unbounded and must always be collared — Midland
    collars it at the lesser of the surrender charge and cumulative net interest credited, or
    0.50% of the accumulation value in California [S6] [S7]. Athene instead embeds a **0.25%
    deadband**: rates must fall by more than 0.25% before the MVA turns positive [S1]. No MVA in
    Missouri [S2].
11. **Correction to a common misstatement: the Model #805 §4B floor on the indexed nonforfeiture
    rate is 15 basis points (0.15%), not 1%** [R2]. §4B sets the rate at the lesser of 3% and the
    five-year Constant Maturity Treasury rate (rounded to the nearest 1/20 of 1%, observed no more
    than 15 months before issue or redetermination) reduced by 125 basis points, with the result
    not less than 15 basis points [R2]; Nassau's contract language confirms the range — rates
    "will range between 0.15% and 3%" [S10]. A flat 1.00% is a **[std]** pick inside that
    corridor. The $50 annual contract charge Model #805 permits [R2] is set to zero because no
    retrieved product declares an actual annual policy fee, making the modeled floor slightly
    conservative.

### GLWB rider

| Parameter | Representative value | Basis |
|---|---|---|
| Rider status | Optional, elected at issue, single or joint life; not cancellable before the 10th rider anniversary | [S5] [S9] [S11]; cancellation window [S1] [S2] [S9] |
| Minimum age for lifetime withdrawals | 50 | [S2] [S3] [S9] |
| Initial benefit base `BB(0)` | The single premium — the bonus goes to the account value, not the benefit base | [S9]; combination **[std]** (12) |
| Growth mechanism (baseline) | **Blended**: guaranteed simple rollup **plus** index-credit stacking, plus an annual step-up | [S2] [S8] [S9]; blend **[std]** (13); step-up **[std]** (14) |
| Guaranteed simple rollup rate | 5.00% of the rollup base in contract years 1–10; 2.00% in years 11–20; 0% thereafter | [S2] |
| Rollup base | Premium adjusted for withdrawals — a flat dollar increment, **not** simple interest on the grown base | [S2] [S9] |
| Stacking factor | 150% of the dollar interest credited in the contract year, floored at zero | [S8] [S9] |
| Growth period | To the earlier of the first lifetime withdrawal and 20 contract years | [S1] [S2]; selection **[std]** (13) |
| Annual step-up (ratchet) | `BB ← max(BB, account value)` tested at each anniversary | **[std]** (14) |
| Rider charge | 0.95% p.a. of the **benefit base**, deducted from the account value at the end of each contract year, **after** index credits | [S9] |
| Rider charge maximum | 1.50%; changeable only after contract year 15 | [S9] |
| Charge after account-value exhaustion | Ceases — no account value to deduct from; income continues | [S9] |
| Lifetime withdrawal percentage | Attained-age band table below | [S3]; 80+ band and lock convention **[std]** (15) |
| Joint life | Single-life percentage − 0.50%, on the younger covered person | [S1] [S3] |
| Excess withdrawal treatment | Pro rata to the contract-value reduction measured net of the guaranteed amount | [S9] |
| RMD treatment | Above the guaranteed annual amount, not an excess withdrawal after exercise; before exercise it reduces the base pro rata | [S1] [S9] |

**Lifetime withdrawal percentages (of the benefit base):**

| Attained age band | 50–54 | 55–59 | 60–69 | 70–79 | 80+ |
|---|---|---|---|---|---|
| Single life | 3.70% | 4.20% | 4.70% | 5.20% | 5.70% |
| Joint life | 3.20% | 3.70% | 4.20% | 4.70% | 5.20% |

Basis: [S3] for the 50–80 bands and both columns; the 80+ band extends [S3]'s single "80" row
**[std]**, supported by [S4], which carries an 80–100 band.

12. Observed: Athene's Initial Income Base = Initial Premium × (1 + Income Base bonus), 25%
    (Option 1) or 15% (Option 2) [S2]; Allianz credits 25% [S3] or 45% [S4] to the benefit base
    only; Nassau's Income Benefit Base "equals the premium payment at issue" [S9] while the
    companion contract credits a 16%/14% bonus to the account value [S10]. The composite follows
    the Nassau pair, so `BB(0) = $100,000` while `AV(0) = $107,000`. **In the benefit-base-only
    designs the bonus never touches the surrender benefit** and is forfeited if income is never
    taken [S3] [S4].
13. The blended form is the research file's mainstream 2020s shape: a base "rolling up at a
    guaranteed simple rate for a 10–20 year deferral window plus a stacking credit on realized
    index interest" [S1] [S2] [S9]. The guaranteed rate comes from Athene's *stacking* option
    (5.00%/2.00%) rather than its non-stacking option (10.00%/5.00%), since rollup and stack are
    not both sold at standalone levels [S2]; 150% is the factor at Midland [S8] and Nassau [S9]
    (Athene's stacking option uses 200% [S2]). The 20-year window is Athene's [S1] [S2]; Nassau's
    runs 15 anniversaries [S9].
14. **No retrieved document describes an automatic annual ratchet during deferral.** Documented
    instead: American Equity increases the Income Account Value to the Contract Value on the day
    before income begins if the Contract Value is higher [S5]; Nassau computes the Annual Benefit
    Amount on "the greater of the Income Benefit Base and the Accumulation Value on the exercise
    date" [S9]; Allianz ratchets the *withdrawal amount* upward whenever interest is credited, and
    it can never decrease [S3]. The annual step-up is a **[std]** generalisation — a superset that
    reduces to the documented design if tested once, at exercise.
15. The percentage is fixed by the attained age at the **first** lifetime withdrawal and does not
    re-read the table afterwards **[std]**. Alternatives: Allianz reads the band from "age at the
    most recent contract anniversary," letting it step up with attained age [S3]; Nassau makes it
    depend on both age at issue and age of the youngest covered person at exercise [S9]; Athene
    grades by single year of age 50–90 across three payout options (Level, Earnings-Indexed,
    Inflation-Adjusted) [S1]; American Equity uses **sex-distinct** single-life factors, with
    Montana requiring gender-neutral issue on the female factors [S5].

---

## Contractual mechanics

Only deltas from the fixed-deferred chassis; surrender charge assessment and the Model #805 floor
follow `_research/fixed-deferred-annuity.md`. The MVA family and the death benefit are
specified in the table above rather than inherited (see **Chassis**), because the fixed-deferred
composite adopts the linear MVA form and a full-account-value death benefit.

### Index credit

At each anniversary the indexed account earns `index credit = credit base × cr`, with `cr =
max(floor, min(cap, R))` [S2] [S4] [S10] [R1], where `R` is the point-to-point return of the price
index over the contract year, dividends excluded [S6] [R1], and `floor` = 0% [S1] [S4] [S10]. The
same engine must support: `max(f, p × R)` (participation) [S4] [S10] [R1]; `max(f, min(c, p × R))`
(participation and cap) — worked at [R1] as `min(80% × 10%, 6%) = 6%`; `max(f, p × R − s)` (spread
/ index margin) [S8] [R1]; `d × 1{R ≥ 0}` (performance trigger — a declared rate credited whenever
the return is non-negative) [R1]; and `max(f, Σ₁₂ min(R_k, c_m))` (monthly sum with monthly cap)
[S4] [R1].

Credits **lock in** once applied and cannot be lost to later declines [S1]; reallocation is
permitted at the end of each crediting period, and an eliminated strategy's value moves to the
fixed strategy [S1]. **The 0% floor applies to the index credit, not to the account value** —
Midland states that deductions for riders, strategy fees or enhanced crediting charges "can exceed
interest credited," "which would result in loss of premium" [S7], so a model that floors the
account value at its prior balance is wrong. The **credit base** is Midland's "Interest Credit
Basis": the accumulation value at the beginning of the term less withdrawals from that index
account, with pro rata advisory fees not reducing it [S6]. Mid-year withdrawal crediting varies:
none in the year of withdrawal [S1]; prorated [S3]; `gross × PAR/(1 + PAR)`, where `PAR` is
Nassau's *Protected Account Return*, not a participation rate [S10]; full
earnings-to-date on the free amount and pro rata above [S11]. Volatility-controlled indices deduct
embedded costs from the index return *before* any cap or participation rate — a 0.50% p.a.
servicing cost calculated daily at BNP Paribas MAD 5 and AiPEX [S2] — so they need an index-return
haircut.

### Premium bonus, vesting and clawback

The 7% bonus is credited to the account value at issue and earns index credits from day one [S5];
on death 100% vests immediately [S5]. On a gross withdrawal exceeding the free amount, or on full
surrender, the insurer recovers the non-vested portion [S10]:

    non-vested bonus recovery = (1 − A) × [ B / (1 + B) ] × C

with `A` the vested percentage for the contract year, `B` the bonus percentage and `C` the gross
withdrawal less the free withdrawal amount [S10]. The `B/(1+B)` factor exists because the account
value already contains the bonus; using `B` directly over-recovers by `(1+B)`. Nassau adds that a
premium bonus "should never be considered an 'offset' to a penalty paid under the prior annuity,
because it is repaid to the Company if you make certain withdrawals," and the free-look refund
excludes it [S10].

### GLWB benefit base

The benefit base is **notional**: no cash value, cannot be withdrawn, cannot be taken as a lump
sum [S1] [S9]. At each anniversary during the growth period:

    rollup = g(t) × rollup base                (simple, flat dollar)   [S2] [S9]
    stack  = 150% × max(0, index credit + fixed interest)              [S8] [S9]
    BB     = max( BB(prior) + rollup + stack , account value )         step-up **[std]**

Two distinctions are commonly got wrong. **The rollup is not simple interest on the current base**
— Athene computes it on "the Premium minus Withdrawals" [S2], Nassau on the "Adjusted Initial
Income Benefit Base" [S9]; both give a flat dollar increment, confirmed by Nassau's 15-year
guaranteed-value table at a flat $3,000 per year on a $100,000 adjusted initial base, $103,000 →
$145,000 over 15 years [S9]. **The stack is on realised dollar credits, net of strategy fees,
floored at zero** — Nassau's Echo Amount = 150% × [fixed interest paid over the contract year +
index credit amounts − Strategy Fee Amounts], floored at zero, worked at [S9] as a $3,000 roll-up
plus a $15,000 echo taking a $200,000 base to $218,000. Growth ceases at the earlier of the first
lifetime withdrawal and the end of the growth period [S1] [S9].

### Rider charge

`rider charge = 0.95% × benefit base` [S9], deducted from the account value at the end of each
contract year after index credits are added, from the fixed account first and then proportionately
across indexed accounts [S9]. The rate may be reset after contract year 15 but never above 1.50%,
a proportional charge is taken on surrender or rider termination, and the signature page requires
the owner to acknowledge that the charge "will continue even after the surrender charge period on
my contract has ended" [S9]. **Once the account value is exhausted the charge stops** — there is
nothing to deduct it from, and Nassau is explicit that income continues in that state [S9];
whether Athene's charge continues is not documented in any retrieved source [unverified].
Alternatives: charge on the **contract value** [S5]; **no explicit charge**, funded through the
option budget — Midland discloses that a built-in GLWB "may offer lower credited interest rates,
lower index cap rates, lower participation rates and/or greater index margins" [S8], and Allianz
states there is no additional charge for its benefit-base riders [S3].

### Lifetime withdrawals and excess withdrawals

    LW = payout%( attained age at the first lifetime withdrawal , single/joint ) × BB

Withdrawals up to `LW` incur **no surrender charge, no MVA and no bonus clawback even if `LW`
exceeds the free withdrawal amount** [S9]; unused `LW` does not carry forward [S9] (Allianz is the
exception, accumulating the shortfall without interest as a "cumulative withdrawal amount" [S3]).
A withdrawal is applied **first against the guaranteed annual amount** — that portion reduces the
account value dollar for dollar and leaves `BB` and `LW` unchanged. Only the excess reduces the
guarantee, **pro rata to the contract-value reduction measured net of the guaranteed amount**
[S9]:

    E = max(0, gross withdrawal − LW)
    ρ = E / ( account value before the withdrawal − LW )
    BB ← BB × (1 − ρ)        LW ← LW × (1 − ρ)

Worked verbatim at [S9]: account value $100,000, base $200,000, annual benefit amount $10,000
(5%), withdrawal $28,000 → denominator $90,000, excess $18,000, reduction 20%, base → $160,000,
benefit amount → $8,000. **Before** exercise, any withdrawal (including an RMD) reduces the
benefit base, the rollup base and future income in the same proportion the account value is
reduced — `ρ = gross withdrawal / account value before the withdrawal` [S1] [S3] [S5] [S9]. The
excess above the free withdrawal amount additionally attracts the surrender charge, the MVA and
the bonus clawback.

### Account value exhaustion — the load-bearing rule

Treatment is **cause-dependent**. If lifetime withdrawals and rider charges alone drive the
account value to zero, the contract enters a **depleted-but-in-force** state and the insurer pays
the lifetime withdrawal amount from its own funds for the rest of the covered life
[S1] [S3] [S9] [R1]: Athene's "Extended Income Guarantee Phase" states that if lifetime income
withdrawals "reduce your Accumulated Value to zero, you'll continue to receive the Lifetime Income
Withdrawal amount for the rest of your life" [S1]; Nassau's income continues if the accumulation
value reaches zero "as a result of rider fee deductions or guaranteed income payments" [S9];
Allianz's worked example runs the account value to zero at age 75 with income continuing [S3]. If
**excess withdrawals, surrender charges or MVAs** drive the account value to zero, payments stop
and the rider terminates [S1] [S9]; American Equity: "Should excess withdrawals reduce the Contract
Value to zero, the IAV will also be reduced to zero, and the contract as well as the rider will be
considered Surrendered" [S5]. In the depleted state there is no surrender value, no death benefit
and **no possibility of lapse** — the only exit is death (or of the survivor under the joint
option) [S1] [S9].

### Rider termination and continuation

The rider terminates on the earliest of: death of the (surviving) covered person; the benefit base
reduced to zero; termination of the base contract; assignment; owner cancellation on or after the
earliest cancellation date; or a change in a covered person — with **no refund of past charges**
[S9]. Athene permits cancellation on or after the 10th rider anniversary [S1] [S2] and continues
the rider on spousal continuation in the accumulation phase, but in the income or
extended-guarantee phase only if the joint option was elected [S1]; American Equity requires the
spouse to be sole primary beneficiary, elect continuation, and be at least 50 [S5].

---

## Riders and options

**In scope (modeled):** the GLWB rider above, single life on the anchor cell, with the joint-life
payout column available as a model-point switch [S1] [S3].

**Described, out of scope (not projected):**

- **Income doubler / enhanced income benefit.** Athene: 2× for up to 60 months on confinement to a
  qualified care facility 180 of 250 days, after 1 year in force and while in the income phase;
  not in CA or MA [S1]. Allianz Income Multiplier: 2× after 5 years in force on inability to
  perform ≥2 of 6 ADLs or confinement ≥90 days in a consecutive 120-day period [S3]. American
  Equity Wellbeing Benefit: ADL-driven, home care qualifies, 2-year wait, up to 5 years [S5].
- **Confinement and terminal illness waivers.** Up to 100% of the account value free of charge and
  MVA [S1] [S5] [S6]; Nassau waives the surrender charge only, leaving bonus clawback and MVA in
  force [S10]. At Athene these are **excess withdrawals that terminate the income rider** [S1] — a
  genuine interaction to flag.
- **Other base-contract options:** the bailout cap provision [S1] [S2] (footnote 6); the
  advisory-fee (fee-based / RIA) variant of up to 1.5% of accumulation value annually, treated as
  a partial surrender [S6]; the Minimum Interest Credit true-up at the end of the withdrawal
  charge period, percentage not disclosed [S1]; index-value locks and interim-value designs
  (Allianz Index Lock and Auto Lock [S3]; Nassau's Daily Account Value / Protected Account Value
  with a 90% protection level and Reset/Extend elections [S10]; Nationwide's daily Balanced
  Allocation Value with a one-time lock-in [S11]).
- **Additional index accounts:** multi-year (2- and 5-year) participation strategies [S2] [S4];
  volatility-controlled proprietary indices [S2] [S10]; monthly sum with cap [S4]; performance
  trigger [R1]; threshold participation and daily average with index margin [S8]; term
  participation with annual performance credits on a 5-year re-entry chassis [S6]; the Balanced
  Allocation Strategy [S11].
- **Benefit-base death benefit** — the PIV taken over ≥5 years, limited to 250% of the
  accumulation value, as an alternative to an account-value lump sum [S3] — and **annuitization /
  payout options** [S6] [S10], including Nassau's election of lifetime payments of 1/12 of the
  annual benefit amount at the contract maturity date [S9]. Model #805 §8 fixes the maturity date
  for minimum-value purposes at the later of the anniversary following the annuitant's 70th
  birthday and the 10th contract anniversary [R2].

---

## Variations across insurers

1. **Where the bonus lands — the biggest structural fork.** *Account-value bonus with vesting and
   clawback*: 3% [S2], 7% [S5], 16%/14% [S10]. *Benefit-base-only bonus*: 25% [S3], 45% [S4], 2%
   of the GLWB value [S8]. These need different code — a vesting vector and a clawback on the
   surrender path versus a second value stream that never feeds the surrender benefit. **Chosen:**
   the account-value design, which exercises both the vesting vector and the `b/(1+b)` clawback;
   the other is a strict simplification of it.
2. **Benefit base growth: guaranteed rollup, pure stacking, or blended.** *Rollup*: Athene
   10.00%/5.00% simple on premium less withdrawals [S1] [S2]; American Equity compound (Options 1,
   3, 5) or simple (Options 2, 4) at a declared IAV rate with 15-, 7- and 10-year guarantee
   windows [S5]; Nassau 3% simple on the adjusted initial base over 15 anniversaries [S9]. *Pure
   stacking*: Allianz — the Protected Income Value grows only by 150% (Balanced) or 250%
   (Accelerated) of index credits, and in the Accelerated option **only 50% of index credits reach
   the account value** [S3] [S4]. *Blended*: Athene Option 2 (5.00%/2.00% + 200% stacking) [S2];
   Midland IncomeVantage (2% of the GLWB value + 150% of dollar interest credited) [S8]; Nassau
   (3% roll-up + 150% Echo) [S9]. **Chosen: blended** — the mainstream shape, degenerating to
   either pure form by zeroing one term. Pure stacking shifts the deferral guarantee from insurer
   to market and is cheaper to hedge.
3. **Rider charge base, and whether the rider is optional.** On the **benefit base**: 1.00%
   [S1] [S2], 0.95% [S9] — the classic GLWB charge, which grows as the base rolls up. On the
   **contract value**: American Equity, with Option 1 carrying no fee at all [S5]. **No explicit
   charge**, funded through reduced caps and participation rates: Allianz [S3] [S4] and Midland
   IncomeVantage [S8]. **Built-in and mandatory** (Athene, Midland IncomeVantage) versus
   **optional** (American Equity, Nassau, Nationwide) [S1] [S5] [S8] [S9] [S11]. **Chosen:** optional,
   0.95% of the benefit base [S9] — the largest and most explicit tail exposure and the only one
   with a retrieved verbatim charge base.
4. **Withdrawal percentage structure.** Five bands 50–80 with a flat 0.50% joint reduction [S3];
   three bands 60–100 [S4]; single years of age 50–90 across three payout options [S1]; single
   years of age 50–80 **by sex** plus a joint column [S5]. **Chosen:** the [S3] band table — the
   simplest structure that still shows the age gradient, and its joint column is exactly single −
   0.50%, matching [S1].
5. **What happens at exhaustion.** Universally, lifetime income survives exhaustion by guaranteed
   withdrawals and fees [S1] [S3] [S9] [R1]; universally it does **not** survive exhaustion by excess
   withdrawal [S1] [S5] [S9]. Athene's Earnings-Indexed payout additionally increases 1% annually in
   the extended phase [S1]. **Chosen:** level payments after exhaustion [S1].
6. **Interim value and term structure.** Three interim-value tiers: none — credits only at
   anniversary, no credit in the year of withdrawal [S1]; prorated or partial credit on withdrawal
   [S3] [S10] [S11]; full daily interim value at Nassau [S10] and Nationwide [S11], a daily mark of
   the embedded option and the hardest to model. Most products credit annually with annual
   reallocation [S1] [S3] [S5] [S10], but Midland IndexMax ADV 5 is a **5-year term product with
   automatic re-entry into a second 5-year term carrying a fresh surrender charge and MVA period**
   [S6], and Nassau's Extendable accounts let the owner extend a segment a year at a time,
   participation-rate changes applying **retroactively to the whole segment** and cap changes
   prospectively only [S10]. **Chosen:** no interim value, annual single segment [S1].
7. **MVA formula family and collar** — see footnote 10. **Free withdrawal percentage tracks the
   income orientation of the product:** 10% on accumulation-oriented and hybrid products
   [S1] [S3] [S5] [S6]; 7% with none in year 1 on the high-bonus Nassau Athos [S10]; 5% on the
   income-focused MNL IncomeVantage [S8]. **Chosen:** 10%.
8. **Vintage caveat.** Declared rates are stamped at different dates — Allianz 222 as of the
   access date [S4], Athene as of 07/01/2022 [S2] — and Athene's current rate sheets could not be
   fetched [S-f1]. Declared caps, participation rates, rollup rates and rider charges are
   **non-guaranteed elements** captured only as of those dates; they illustrate parameter levels,
   not durable product constants [R6].

---

## Regulatory context

**Nonforfeiture — NAIC Model #805 and Model #806.** The minimum nonforfeiture amount accumulates
**net considerations of 87.5% of gross considerations** at the §4B rate, less accumulated
withdrawals, an accumulated **$50 annual contract charge**, premium tax paid and indebtedness
[R2] [REG-R42]. **The §4B rate is the lesser of 3% and (five-year CMT − 125 bp), floored at 15
basis points — not 1%** [R2] [REG-R42]; Nassau's contract language confirms the 0.15%–3% range
[S10]. Under §4C, while the contract provides "substantive participation in an equity indexed
benefit" the 125 bp reduction may be increased by **up to an additional 100 bp** if the present
value of the extra reduction does not exceed the market value of the equity benefit [R2]. Model
#806 §7 operationalises that: if the annualized option cost of the **guaranteed** index features
is **≥25 bp**, the reduction is the **lesser of 100 bp and that option cost**, certified by an
Academy member at filing and annually [R3]. Model #806 §6B also permits more than one
nonforfeiture rate per contract, the minimum being the sum of per-benefit minimums with excess
withdrawals deducted from the lowest-rate benefit first [R3]. Model #808 (life nonforfeiture) does
**not** apply to annuities [REG-R2] [REG-R42].

**Disclosure and illustrations — NAIC Model #245, not #250.** The Annuity Disclosure Model
Regulation is **#245**; **#250 is the Variable Annuity Model Regulation**, which by its own
definition reaches only separate-account products and so does not apply to a general-account FIA
[R5] [REG-R43] [REG-R45]. Model #245 §6 requires non-guaranteed elements no more favorable than
current with no assumed improvements, an index in existence at least **10 years** before it may be
illustrated, and three prescribed historical scenarios (most recent 10 calendar years; worst 10
continuous of the last 20; highest 10 consecutive of the last 20) each on the geometric mean
annual effective rate, plus MVA upside/downside requirements [R1] (§6 is the illustration-standards
section and Appendix A the illustration example; the section text itself was not retrieved
[REG-R45]). AG 49 and AG 49-A are illustration guidelines under the **Life Insurance** Illustrations
Model Regulation (#582) and must **not** be reused for FIA illustrations, which run through Model
#245 [REG-R8] [REG-R10] [REG-R45].

**Suitability — NAIC Model #275.** The 2020 best-interest revision requires producers to act in
the consumer's best interest and insurers to supervise recommendations [R4] [REG-R46]. Its
definition of "non-guaranteed elements" — premiums, credited rates including any bonus, benefits,
values, charges or the formula elements behind them, subject to company discretion and not
guaranteed at issue [R4] — is the cleanest available definition of a cap, participation rate,
spread or declared rollup rate. Modelling relevance is indirect but real: best-interest
supervision changes exchange and replacement activity, hence surrender assumptions [REG-R46].

**Statutory valuation — AG 33, AG 35, VM-22.** Reserves run through **AG 33**, printed as
*"Determining CARVM Reserves for Annuity Contracts With Elective Benefits"*, and **AG 35**, *"The
Application of the Commissioners Annuity Reserve Method to Equity Indexed Annuities"*. **Both were
read in full in AP&P Manual Appendix C on 2026-08-06** [REG-R151] [REG-R152] — the manual turned out
to be a **free download**, not the paid publication this file previously recorded [REG-R33] — so
their mechanics are no longer [unverified], and titles and continued incorporation remain confirmed
by the VM-C index [REG-R41]. AG 33 applies "to all annuity contracts subject to CARVM, where any
elective benefits … are available to the contract owner" — no product list, no threshold, no size
test — sorts every benefit into elective or non-elective, **prohibits experience-based elective
incidence** (trial sets are maximised over instead), and determines the SVL §4b parameters at
**contract** level (issue-year versus change-in-fund basis, cash settlement options, interest
guaranteed on considerations received beyond 12 months) and at **benefit** level (guarantee
duration, Plan Type) [REG-R151]. AG 35 applies "to all equity indexed annuity contracts, regardless
of the date of issue, that are subject to CARVM" and supplies four computational methods — **CARVM
with Updated Market Values**, the **Market Value Reserve Method**, its **Black-Scholes Projection
Method** adaptation and the **Enhanced Discounted Intrinsic Method** — each of which ends by handing
the greatest-present-value calculation back to AG 33; **"Type 1" and "Type 2" are the guideline's
own printed section headings, not industry shorthand**, Type 1 (EDIM) gated on the "Hedged as
Required" criteria with quarterly appointed-actuary certification and Type 2 on the Attachment 4
assumption certification [REG-R152]. **Two corrections the reading forces on what this paragraph
used to say.** (1) AG 33's *Effective Date* block reads "This guideline shall be effective on
**December 31, 1998**, affecting all contracts issued on or after January 1, 1981" [REG-R151]; the
library elsewhere carries **December 31, 1995** from IRS Rev. Rul. 2002-6 under a different title.
The 1981 issue-date reach is common to both, but the extracted pages carry **no amendment history**,
so the reconciliation is **unresolved** — "a later revision" would be an inference, not a fact.
(2) AG 35 does **not** free-standingly require asset adequacy testing. Its provision is one
conditional sentence — "**To the extent required by law, regulation, or regulatory requirements**,
reserves established for equity indexed annuity policies must be tested for adequacy using
appropriate methods and assumptions" [REG-R152] — which presupposes the obligation rather than
creating it; the binding authority is SVL §6.B and VM-30, with ASOP No. 22 the standard the analysis
runs under [REG-R1] [REG-R100] [REG-R29], and AG 35 is corroboration. AG 35 also prints **no
effective, adoption or operative date, no transition and no sunset**; its only temporal language is
"regardless of the date of issue", so **no date may be attributed to it** [REG-R152]. **VM-22** is
the principle-based framework for non-variable
annuities, effective for valuation dates on or after **January 1, 2026**, with a three-year
elective transition and mandatory prospective application three years after the effective date
[REG-R36] (the Academy paper states elective 1/1/2026, required 1/1/2029 [R1]; post-launch
monitoring sits with the VM-22 (A) Subgroup [R7]). An FIA falls in VM-22's **Accumulation**
category, which expressly includes "fixed income streams from guaranteed living benefits after
account exhaustion"; **GLB utilization risk** is named among the risks to be reflected and the
stochastic reserve is CTE70 [REG-R36]. **Correction:** in the January 1, 2026 Valuation Manual
VM-22 is *entirely* the PBR framework — maximum valuation interest rates for income annuities are
in **VM-V Section 1**, whose scope also covers guaranteed-living-benefit streams after exhaustion
[REG-R36] [REG-R37]. Enabling statute: Model #820 [REG-R1] [REG-R3].

**Federal securities law — FIAs are not registered.** Three currently-sold disclosure documents
state the contract is not a security and is not SEC-registered [S6] [S9] [S10]. Rule 151A would have
classified indexed annuities as securities; it was vacated by the D.C. Circuit, and Dodd-Frank
§989J then directed the SEC to treat qualifying annuities as exempt securities, returning them to
state regulation [REG-R53] — Model #275's drafting note records that §989J "confirmed this
exemption of certain annuities from the Securities Act of 1933 and confirmed state regulatory
authority" [R4]. The SEC release and Federal Register text could not be fetched [R10]; the vacatur
and the §989J exempt-security direction are carried on the CRS report [REG-R53], and only the
enumerated §989J conditions remain [unverified], never having been read against a primary document. The contrast product, a
registered index-linked annuity exposing the holder to index losses, registers on Form N-4 under
the 2024 SEC rule [REG-R49].

**Federal tax — IRC §72 and the RMD regime.** Pre-annuitization distributions follow the **LIFO /
income-first** rule of §72(e), against ratable basis recovery under the §72(b) exclusion ratio;
§72(q) adds a **10% penalty** on the includible portion of non-qualified distributions with
exceptions including age 59½, death and disability; §72(s) requires the remaining interest to be
distributed within five years of the holder's death before annuitization, subject to a
beneficiary-life-expectancy exception; and all contracts issued by one company to one policyholder
in a calendar year are treated as one contract [REG-R55]. §1035 permits tax-free annuity → annuity
exchanges but **not** annuity → life [REG-R56], making exchange activity a first-class surrender
input. For qualified money the RMD regime finalized in T.D. 10001 (applicable for calendar years
beginning January 1, 2025) is a **behavioral** input as much as a tax one: utilization clusters at
the RMD age [REG-R57] [REG-R58] [REG-R64]. RMDs are free withdrawals contractually at Athene [S1]
and Nassau [S10], and **by current company practice — explicitly not a guarantee** at Midland
[S6] [S8].

**Non-guaranteed elements and other layers.** Declared caps, participation rates, spreads, index
margins, fixed rates, bonuses and declared rollup rates are NGEs under ASOP No. 2, revised **only
if anticipated experience factors have changed** and never to recoup past losses; the guaranteed
minimum caps and participation rates at [S4] and [S10] are the "minimum index parameters" §2.3
names as the guaranteed elements bounding those scales [R6] [REG-R26]. In practice insurers reset
them frequently (e.g. monthly) against the priced product **option budget** [R1] [REG-R68]. Also
binding: ASOP No. 7 (cash flow analysis) [REG-R27]; ASOP No. 22 (asset adequacy — the route AG
35's requirement runs through) [REG-R29]; ASOP No. 54 (pricing) [REG-R70]; ASOP No. 56 (modeling)
[REG-R32]; ASOP No. 10 and FASB ASU 2018-12 (LDTI), under which the **index feature is an embedded
derivative** and the **GLWB is a market risk benefit** at fair value [R1] [REG-R34] [REG-R71]; and
IRC §807, which makes the statutory annuity engine the tax-reserve engine [REG-R16].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-fixed_indexed_annuity-r1
[R10]: #uslib-fixed_indexed_annuity-r10
[R2]: #uslib-fixed_indexed_annuity-r2
[R3]: #uslib-fixed_indexed_annuity-r3
[R4]: #uslib-fixed_indexed_annuity-r4
[R5]: #uslib-fixed_indexed_annuity-r5
[R6]: #uslib-fixed_indexed_annuity-r6
[R7]: #uslib-fixed_indexed_annuity-r7
[R8]: #uslib-fixed_indexed_annuity-r8
[R9]: #uslib-fixed_indexed_annuity-r9
[REG-R1]: #uslib-reg-r1
[REG-R10]: #uslib-reg-r10
[REG-R100]: #uslib-reg-r100
[REG-R151]: #uslib-reg-r151
[REG-R152]: #uslib-reg-r152
[REG-R16]: #uslib-reg-r16
[REG-R2]: #uslib-reg-r2
[REG-R26]: #uslib-reg-r26
[REG-R27]: #uslib-reg-r27
[REG-R29]: #uslib-reg-r29
[REG-R3]: #uslib-reg-r3
[REG-R32]: #uslib-reg-r32
[REG-R33]: #uslib-reg-r33
[REG-R34]: #uslib-reg-r34
[REG-R36]: #uslib-reg-r36
[REG-R37]: #uslib-reg-r37
[REG-R41]: #uslib-reg-r41
[REG-R42]: #uslib-reg-r42
[REG-R43]: #uslib-reg-r43
[REG-R45]: #uslib-reg-r45
[REG-R46]: #uslib-reg-r46
[REG-R49]: #uslib-reg-r49
[REG-R53]: #uslib-reg-r53
[REG-R55]: #uslib-reg-r55
[REG-R56]: #uslib-reg-r56
[REG-R57]: #uslib-reg-r57
[REG-R58]: #uslib-reg-r58
[REG-R64]: #uslib-reg-r64
[REG-R68]: #uslib-reg-r68
[REG-R70]: #uslib-reg-r70
[REG-R71]: #uslib-reg-r71
[REG-R8]: #uslib-reg-r8
[S1]: #uslib-fixed_indexed_annuity-s1
[S10]: #uslib-fixed_indexed_annuity-s10
[S11]: #uslib-fixed_indexed_annuity-s11
[S2]: #uslib-fixed_indexed_annuity-s2
[S3]: #uslib-fixed_indexed_annuity-s3
[S4]: #uslib-fixed_indexed_annuity-s4
[S5]: #uslib-fixed_indexed_annuity-s5
[S6]: #uslib-fixed_indexed_annuity-s6
[S7]: #uslib-fixed_indexed_annuity-s7
[S8]: #uslib-fixed_indexed_annuity-s8
[S9]: #uslib-fixed_indexed_annuity-s9
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
