# Product Specification

**Status:** Draft, 2026-08-04 (all cited sources accessed 2026-08-04).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling of a U.S. individual **multi-year guaranteed annuity
(MYGA)** — a single-premium, book-value fixed deferred annuity with a market value
adjustment. It does not describe any single insurer's product. Facts carrying a source
tag — [S#] (primary product documents) and [R#] (regulatory/actuarial references), both
numbered per `_research/fixed-deferred-annuity.md`, and [REG-R#] (the cross-product
reference library `references/regulatory-and-actuarial-references.md`, whose shared
R-numbering now runs **R1–R157** with most of the **R73–R149** block unused; provenance in
`_research/regulatory-actuarial.md` for R1–R34,
`_research/regulatory-actuarial-annuities.md` for R35–R72, and the AP&P Manual appendix
extractions `_research/appp-ag33.md`, `appp-ag35.md`,
`appp-a820-a821-a822.md` and `appp-a585-a250-a255-a270.md` for R151–R157, all accessed
**2026-08-06**) — were extracted from
the cited document. Values marked **[std]** are standardizations introduced for the
reference implementation; each [std] table row carries a footnote giving the rationale and
the observed range across insurers. Facts the research file could not verify are flagged
[unverified].

**Role in this library.** This is the **deferred annuity base chassis**. The **fixed-indexed
annuity** documents reference the *structure* specified here — the surrender-benefit
composition order (account value, less surrender charge, plus or minus MVA, floored at the
nonforfeiture value) and the Model #805 floor construction — rather than restating it.
They do **not** inherit this contract's parameters or its two most distinctive mechanics:
an FIA's account-value roll-forward is index-credit driven, and its lapse architecture is
**not** this chassis's renewal/shock-lapse architecture (an FIA's shock lapse is suppressed
by an in-force GLWB rider, roughly 10%/33% with and without a rider, against the 52%–56%
reported for fixed-rate deferred annuities — see
`products/fixed_indexed_annuity/technical-notes.md`). That file also restates, rather
than inherits, the MVA family and the death benefit; both differences are itemized there.
The **variable annuity** documents deliberately do **not**: a VA
is a separate-account contract that Model #805 expressly excludes, and the nonforfeiture
floor reaches it only through Model #250 §7.B on any fixed account
[REG-R42] [REG-R43] — do not import the recursions below into a VA model.

**Composite anchors.** Charges and nonforfeiture follow one carrier's five-year MVA annuity
[S10] [S11] [S12]; the MVA algebra follows a second carrier's linear family
[S5] [S8] [S9]; a third carrier's registered contract [S4] is the arithmetic
unit-test anchor for the geometric MVA branch, being the only retrieved source with fully
worked MVA numbers. This pairing is the research file's own recommended composite.

---

## Product overview and market role

A MYGA is a single-premium deferred annuity whose entire purchase payment is credited to
an account value growing at an insurer-declared effective annual rate, **guaranteed for a
stated multi-year guarantee period** (typically 3–10 years), after which a new rate is
declared [S1] [S2] [S5] [S16]. There is no index feature and no separate account: the account
is a **book-value** account. Interest is credited daily and quoted as an annual effective
rate [S4] [S5] [S16]. Typical designs carry no front-end load and no annual administration
fee — 100% of premium is credited [S5] [S10] [S13] [S16].

Liquidity is bounded by three contractual devices that between them define the product's
economics: a declining **surrender charge** over the guarantee period, an annual
**free-withdrawal allowance** exempt from that charge, and a two-sided **market value
adjustment (MVA)** transferring interest-rate risk on early exit back to the contract
holder [S2] [S8] [S9] [S10] [S13]. Underneath all three sits a statutory floor: the **minimum
nonforfeiture amount** of NAIC Model #805, an accumulation of 87.5% of gross considerations
at an indexed rate [R1] [REG-R42].

The product competes on declared rate against bank CDs and other MYGAs, and its single most
important behavioral feature is the **shock lapse at the end of the guarantee period /
surrender charge period**. Industry experience shows surrender rates peaking in the year the
surrender charge expires and remaining elevated afterward, decreasing as the guaranteed
minimum interest rate rises, decreasing as the credited rate rises, and increasing with the
excess of market rate over credited rate — with the shock-year rate high **regardless** of
the interest-rate environment [R8] [REG-R63]. The NAIC's prescribed standard-projection
assumption puts base lapse at **75% in the year of a guarantee-period expiry** against 1%
inside a multi-year guarantee period [R2] [REG-R36].

MYGAs are not SEC-registered. Two of the retrieved contracts *are* registered [S3] [S4];
the research file's reading is that this follows from their MVAs carrying **no cap or
collar at all** [S3] [S4], where the retail MYGAs cap or floor the adjustment
[S2] [S8] [S9] [S12] [S13]. Treat that as the research file's observation, not a stated
legal test [unverified].

---

## Representative specification

### Contract identity, issue rules and premium

| Parameter | Representative value | Basis |
|---|---|---|
| Legal form | Individual single-premium deferred annuity (SPDA), non-participating, non-registered, with a market value adjustment | [S10] [S11] [S13] [S16] |
| Premium pattern | Single premium; no additional purchase payments | [S5] [S10] [S13] |
| Minimum initial premium | $10,000 | [S10] [S16]; pick **[std]** (1) |
| Maximum without company approval | $1,000,000 | [S1] [S2]; pick **[std]** (1) |
| Issue ages (age last birthday) | 0–85, qualified and non-qualified | **[std]** (2) |
| Initial guarantee period | 5 years | [S10] [S11] |
| Front-end load | None; 100% of premium credited | [S5] [S10] [S13] [S16] |
| Annual contract / maintenance fee | $0 | [S5] [S10] [S13] [S16] |
| Premium tax deducted from the contract | 0% | [S3] [S16]; pick **[std]** (3) |
| Free look | 10 days; refund = purchase payment (no MVA) | [S3]; pick **[std]** (4) |
| Anchor model cell | Male 60, non-qualified, $100,000 single premium, 5-year period | **[std]** (5) |

1. Observed minima: $5,000 [S1] [S13]; $10,000 [S2] [S3] [S10] [S16]; $50,000 [S5] [S6] [S7].
   Observed maxima: $1,000,000 with more on approval [S1] [S2]; >$1,000,000 with consent
   [S3]; >$2,000,000 needs approval [S13]. $10,000 / $1,000,000 is the modal retail pair.
   The $100,000 anchor premium is chosen so the source's own $100,000-and-over rate band
   applies [S11].
2. Observed: 0–80 [S1] [S2]; 0–89, inherited 0–75 [S10]; 0–85 non-qualified and 18–85
   tax-qualified [S13]; up to 90 [S5]; specimen maximum annuitant age [85] [S14]. 0–85 is
   the modal upper bound; the composite drops the qualified-money lower-age distinction.
   Only [S1] [S2] state an age basis ("actual age"), so ALB is the **[std]** reading of the
   *eligibility* rule. The technical notes run *mortality* on age nearest birthday, the
   basis VM-22 prescribes [R2 §6.B.8](#uslib-fixed_deferred_annuity-r2); the anchor cell is taken as age 60 on both bases at
   issue **[std]**, so no conversion is applied in the reference run.
3. Observed premium tax deducted by the insurer: 0%–4% by jurisdiction [S3]; 0%–3.5% [S16];
   deductible from accumulation value or death benefit where the state requires [S5] [S9].
   Set to 0% so premium tax is a switch, not a baked-in level; Model #805 permits premium
   tax actually paid to be deducted from the nonforfeiture floor [R1] [REG-R42].
4. Observed: 10 days, refund of purchase payment [S3]; 10 days, refund of contract value
   **including any applicable MVA** [S4]; 30 days, refund of premium less withdrawals [S9].
   Model #245 §5.A requires a free look of **not less than 15 days** where the disclosure
   document and Buyer's Guide are not delivered at or before application [R4] [REG-R45].
5. Issue age 60 puts surrender-charge expiry after the IRC §72(q) age-59½ boundary and
   before the RMD applicable age, so neither tax cliff dominates the behavior module [R6].

### Interest crediting and renewal

| Parameter | Representative value | Basis |
|---|---|---|
| Initial declared rate, guaranteed for the 5-year initial term | **4.45%** effective annual | [S11] (eff. 09/22/25, purchase payments $100,000+; 4.10% under $100,000) |
| Declared rate shape within the initial term | Level for the whole term | [S11]; choice **[std]** (6) |
| Crediting frequency (contract) | Daily compounding to the declared annual effective rate | [S4] [S5] [S16] |
| Guaranteed minimum interest rate (GMIR) | **0.25%** | [S11] |
| Renewal architecture | Roll into a new 5-year guarantee period at a redeclared rate, with a fresh (shorter) surrender charge and MVA schedule | [S1] [S2] [S5] [S11]; choice **[std]** (7) |
| Renewal surrender charge (renewal years 1→5) | 5%, 4%, 3%, 2%, 1% | [S2]; adoption **[std]** (8) |
| Attained-age cap on the renewal charge | 4% at 94, 3% at 95, 2% at 96, 1% at 97, 0% at 98–100 | [S1] [S2] |
| Renewal declared rate | Company discretion, never below the GMIR | [S1] [S2] [S11] [S16]; projection rule **[std]** (technical notes) |
| Guarantee-period-end window | 30 days: withdraw, surrender, renew or annuitize at **full account value**, no charge and no MVA | [S1] [S2] [S5] [S6]; adoption **[std]** (9) |
| Default at window expiry | Automatic renewal into a period of the same duration | [S1] [S5] |
| Bailout rate provision | None | (10) |

6. Observed: level rate guaranteed to the fifth anniversary [S11]; an escalating design on
   the same product's earlier brochure — base +0.25% bonus in term year 1, then base +0.10%
   cumulatively per year (illustrated 3.25%, 3.10%, 3.20%, 3.30%, 3.40% on a 3.00% base)
   [S10]; multiple rates within one term, not permitted in New York [S3]. Level is modal and
   single-parameter; the escalating variant is a *guaranteed* element and must be disclosed
   as such rather than illustrated [R4 §6.F(8)](#uslib-fixed_deferred_annuity-r4) [REG-R45].
7. Two camps. **Camp A** rolls into a new multi-year guarantee period with a fresh, usually
   lower, surrender charge — three of the carriers surveyed [S1] [S2] [S5] [S6] [S11],
   including the charge anchor, whose charges and MVA apply "during each initial term
   **or any renewal terms**" [S11]. **Camp B** drops to annually redetermined rates with
   **no** new surrender charge — a single carrier's contract, where the renewal rate is set
   each anniversary and, for New York issues, the GMIR itself is redetermined annually at
   not less than 1.00% [S13]. Camp A matches the charge and nonforfeiture anchor [S11]; the
   two produce entirely different lapse patterns and the technical notes carry both as a
   **model-point switch**.
8. Observed: one carrier's California form 9/8/7/6/5/4/3 initial vs 5/5/5/5/5/4/3 renewal
   [S1]; its New York form 7/6/5/4/3 initial vs 5/4/3/2/1 renewal [S2]. The two registered
   contracts instead measure the charge from the **original purchase payment date**, so
   reinvestment never restarts the clock [S3] [S4]. The composite adopts that New York
   renewal schedule and age cap [S2].
9. Not described in the charge anchor's documents [S10] [S11] [S12]; taken from two other
   carriers [S1] [S2] [S5] [S6], where it is the retail norm. One registered contract's
   analogue is 90 days' notice with unelected money defaulting into a liquid transition
   account free of MVA and CDSC [S4]; the other's is 18 days' notice with a 5-day election
   deadline and auto-reinvestment [S3].
10. **No bailout-rate provision appears in any retrieved document.** The bailout feature (a
    stated renewal rate below which the owner may surrender charge-free) is a real MYGA/FIA
    feature [unverified] but is not evidenced here; the 30-day free-out window is the
    mechanism actually documented [S1] [S2] [S5] [S6].

### Surrender charges and liquidity

| Parameter | Representative value | Basis |
|---|---|---|
| Surrender charge, initial term (years 1→5) | 9%, 8%, 7%, 6%, 5%; 0% from year 6 | [S10] |
| Surrender charge base | The portion of the withdrawal/surrender **in excess of** the free allowance | [S8] [S9] |
| Free allowance, contract year 1 | 10% of purchase payments | [S10] |
| Free allowance, contract years 2+ | 10% of the account value at the most recent anniversary | [S10] |
| Carry-forward | None; non-cumulative within a contract year, multiple withdrawals permitted up to the allowance | [S4] [S16]; adoption **[std]** (11) |
| Free amount exempt from charge **and** MVA, including at full surrender | Yes | [S8] [S11]; convention **[std]** (12) |
| Minimum partial withdrawal | $500 | [S2]; pick **[std]** (13) |
| RMD treatment | Exempt from charge and MVA even above the free allowance | [S15]; adoption **[std]** (14) |
| Nursing-home / extended-care waiver | After year 1; confinement ≥90 consecutive days; up to 100% of account value free of charge; no rider cost | [S10] (trigger and charge waiver); MVA also waived per [S2] [S5] [S13] |
| Terminal-illness waiver | After year 1; prognosis of survival 12 months or less; up to 100% of account value free of charge; no rider cost | [S10]; MVA also waived per [S2] [S13] |

11. Observed: explicitly non-cumulative [S4]; multiple partial withdrawals permitted up to
    the allowance [S16]; one carrier restricts the exemption to the **first** withdrawal of
    each calendar year and charges the rest even if the 10% was unused [S3].
12. Confirmed in one carrier's worked example — the fixed **index** annuity source, not a
    MYGA illustration [S8]: on a full surrender at accumulation value $115,927 with an
    $11,593 free amount and a 3% charge, the charge is $3,130 = 3% × ($115,927 − $11,593)
    and the MVA runs on the same $104,334 base "before the reduction for any surrender
    charge" [S8]; the charge anchor states charges and MVA "do not apply to amounts covered
    by the 10% free withdrawal allowance" [S11]. **The opposite convention is real and
    material:** the two registered contracts [S3] [S4] both apply the MVA to free-amount
    withdrawals taken before maturity.
13. Observed: $500 partial / $100 systematic [S2]; $100 with a $2,000 account-value floor
    after the withdrawal [S13]; $50 minimum systematic interest payment [S5].
14. Observed: exempt even above the free amount [S15]; exempt by *current company practice*
    only, explicitly not a contractual guarantee [S5] [S6]; exempt when the insurer
    calculates the RMD [S13]; exempt on the enhanced-liquidity version only [S2]. **Worst
    treatment observed:** RMDs treated as any other withdrawal and fully charged unless
    taken in the 30-day window [S1] [S2]. One registered contract sets the free amount at
    the greater of 10% of contract value or the RMD, but the MVA still applies [S4].

### Market value adjustment

| Parameter | Representative value | Basis |
|---|---|---|
| Formula family | Linear duration × rate change: `μ = (i0 − it) × T` | [S8] [S9] |
| `i0`, `it` | MVA reference yield at issue (locked for the guarantee period) and at surrender | [S8] [S9] |
| `T` | (days from the surrender date to the end of the current contract year ÷ 365) + whole years remaining in the MVA period | [S8] |
| Reference index | A published corporate credit index yield (source design: Barclay's US Credit Index) | [S8] [S9]; model treatment **[std]** (15) |
| Application base | The portion of the surrender exceeding the free amount, **before** the surrender charge deduction | [S8] |
| Cap | **Symmetric**: the adjustment, positive or negative, may not exceed the surrender charge amount | [S2]; pick **[std]** (16) |
| MVA period | Equal to the surrender charge period; resets at each renewal | [S8] [S11] |
| Not applied to | Death benefit [S2] [S4] [S8] [S13] [S16]; the 30-day window [S2]; annuitization [S16]**[std]** (17); RMDs and waiver withdrawals [S2] [S5] [S13]; after the MVA period [S8] [S13] [S16] | as cited |
| Floor on the adjusted value | Surrender value after MVA and charge may not fall below the state minimum nonforfeiture value | [S8] [S9] [S12] |

15. The index is Barclay's US Credit Index for the linear-duration family adopted here, and
    the formula "varies by state" [S8]. Observed references market-wide: Treasury notes
    maturing in the last quarter of the term [S3]; interest rate swaps + 25 bp [S4];
    Barclay's US Credit Index [S8] [S9]; 5-Year Treasury CMT and/or the BofA Merrill Lynch
    5-10 Year US Corporate Bond Index [S12]; the company's own new-money declared rate
    [S14]; an unnamed reference-index YTM, with Treasury CMT plus corporate bond indexes in
    New York [S13].
    **[std]:** the model takes a single scalar reference-yield series as input rather than
    hard-coding an index, because the index is a state-filed variable.
16. Observed cap/collar designs — the largest single cross-carrier divergence: symmetric cap
    at the withdrawal charge [S2]; cap at min(surrender charge, interest credited) both ways
    [S8] [S9]; **asymmetric**, positive capped at the early withdrawal charge and negative
    limited only by the standard nonforfeiture law minimum [S12]; floored at premiums
    accumulated at the GMIR, with the surrender charge still able to breach that level
    [S13]; **no cap at all** [S3] [S4]. The symmetric cap is the cleanest to specify and is
    the design that, on the research file's reading, keeps the contract non-registered
    [S3] [S4] [unverified]. All five are first-class model parameters in the technical notes.
17. Observed: not applied on annuitization [S16], "may not apply" [S8]; applied on
    annuitization before maturity [S4]; applied but **only when positive** for amounts used
    to start a lifetime payout option [S3]. The composite takes the retail form.

### Minimum guaranteed surrender value (Model #805 nonforfeiture floor)

| Parameter | Representative value | Basis |
|---|---|---|
| Statutory basis | NAIC Standard Nonforfeiture Law for Individual Deferred Annuities, Model #805 | [R1] [REG-R42] |
| Net consideration ratio | **87.5%** of gross considerations credited in the contract year | [R1 §4.A(2)](#uslib-fixed_deferred_annuity-r1) [REG-R42] |
| Contract GMSV accumulation rate | **2.80%** | [S11] |
| Statutory corridor, indexed nonforfeiture rate | `min(3.00%, round(5-yr CMT, nearest 1/20 of 1%) − 1.25%)`, **floored at 0.15% (15 bp)** | [R1 §4.B](#uslib-fixed_deferred_annuity-r1) [REG-R42] |
| CMT observation date | A date or averaging period stated in the contract, no longer than **15 months** before issue or redetermination | [R1 §4.B](#uslib-fixed_deferred_annuity-r1) [REG-R42] |
| Annual contract charge deducted from the floor | **$0** (statutory maximum $50, accumulated at the same rate) | [S11]; [R1 §4.A](#uslib-fixed_deferred_annuity-r1) [REG-R42]; pick **[std]** (18) |
| Withdrawal deduction convention | **Gross** — not reduced by early withdrawal charges or negative MVAs — accumulated at the GMSV rate | [S11]; convention **[std]** (19) |
| Redetermination | Permitted if the contract says so; none during the initial term | [R1 §4.B](#uslib-fixed_deferred_annuity-r1); **[std]** |
| Death benefit floor | At least the cash surrender benefit | [R1 §6](#uslib-fixed_deferred_annuity-r1) [REG-R42] |
| Equity-index carve-out (§4.C, up to a further 100 bp) | Not applicable — no index benefit on this chassis | [R1 §4.C](#uslib-fixed_deferred_annuity-r1) [REG-R42] |

**Correction, stated explicitly.** The commonly repeated description of Model #805 puts a
**1% floor** under the indexed nonforfeiture rate. The retrieved Fall 2020 print sets the
floor at **15 basis points (0.15%)**, giving a corridor of **0.15% ≤ i ≤ 3.00%** with
`i = round(5-yr CMT, 1/20 of 1%) − 1.25%` [R1 §4.B](#uslib-fixed_deferred_annuity-r1) [REG-R42]. The 1% figure reflects the
2003 amendment as originally adopted and is **[unverified]** against any retrieved
document; do not implement it. The representative 2.80% GMSV rate [S11] sits inside the
corrected corridor.

18. The statute permits a $50 annual contract charge, accumulated at the same rates, to be
    deducted [R1 §4.A](#uslib-fixed_deferred_annuity-r1) [REG-R42]. The one retrieved product-level GMSV definition does not
    take it: "87.5% of purchase payments minus all prior withdrawals ... plus interest
    credited daily at the GMSV rate of 2.80%" [S11]. The composite follows the product and
    exposes the charge as a parameter set to $0.
19. Two conventions are in the market and differ materially. [S11] deducts withdrawals
    **excluding** early withdrawal charges and negative MVAs — the floor falls by the gross
    amount taken. [S9] deducts surrenders "**after** MVA or reduction for surrender charges"
    — by the net proceeds, keeping the floor higher. The composite takes [S11] and exposes
    the other as a switch.

### Death benefit and annuitization

| Parameter | Representative value | Basis |
|---|---|---|
| Death benefit before annuitization | **Full account value** at the date of death; no surrender charge, no MVA | [S1] [S2] [S13] |
| Statutory floor | Not less than the cash surrender benefit, hence not less than the minimum nonforfeiture amount | [R1 §6](#uslib-fixed_deferred_annuity-r1) [REG-R42] |
| Alternative design (not adopted) | Greater of accumulation value and the minimum surrender value | [S5] [S6] |
| Annuitization availability | After the first contract year | [S1] [S2] ([S10] lists the income options but is silent on timing) |
| Annuitization proceeds basis | Surrender value during the surrender charge period; **full account value** in the 30-day window and after that period | [S1] [S2] [S5]; composition **[std]** (20) |
| Income options | Fixed period; life; life with 10- or 20-year certain; joint and one-half survivor | [S1] [S2] [S10] |
| Deemed maturity date (statutory) | Later of the anniversary next following the annuitant's 70th birthday and the 10th contract anniversary | [R1 §8](#uslib-fixed_deferred_annuity-r1) [REG-R42] |
| Annuitization bonus | None | (21) |

20. Observed: cash surrender value except in the 30-day window, where full accumulation
    value applies [S1]; full accumulation value at all times after year 1 [S2]; surrender
    value, with accumulation value granted by *current company practice* for life options
    after year 1 or after five years in force with payments over ≥5 years, and accumulation
    value in Florida [S5]; contract value with an MVA but no charge if in force ≥2 years
    [S4]. The composite is the modal retail rule.
21. **No annuitization bonus appears in any retrieved document.** The nearest analogues are
    the current-company-practice accumulation-value concession [S5] and the 30-day-window
    full-account-value treatment [S1] [S2].

---

## Contractual mechanics

Notation, reused verbatim in `technical-notes.md`: `P` single purchase payment; `AV(t)`
account value; `i_cr` declared credited rate; `sc(y)` surrender charge rate in contract
year `y`; `FW(t)` available free-withdrawal allowance; `E(t)` amount exposed to charge and
adjustment; `μ(t)` MVA rate; `M(t)` MVA amount (signed); `C(t)` surrender charge amount;
`MGSV(t)` minimum guaranteed surrender value; `SB(t)` surrender benefit paid. Note on
labels: **`MGSV` is this library's term across the annuity family** for the Model #805
nonforfeiture floor; the specimen contract [S11] calls the same quantity the "GMSV" and
its accumulation rate the "GMSV rate", and that wording is preserved wherever [S11] is
quoted below. `products/fixed_indexed_annuity/` calls the same floor the **guaranteed
minimum value (`MGV`)**, following its own source [S10] — one concept, three labels.

**Account value.** 100% of premium at issue, accreting at the declared effective annual
rate compounded daily [S4] [S5] [S16], reduced by the gross amount of any withdrawal. No
charges are deducted from the account value — no front-end load, no annual fee, no rider
charges on the base contract [S5] [S10] [S13] [S16]. Over a period of length `dt` years with
no withdrawal, `AV(t) = AV(t − dt) × (1 + i_cr)^dt`, with `i_cr` the initial declared rate
for the whole initial guarantee period [S11] and the renewal declared rate — never below
the 0.25% GMIR [S11] — thereafter.

**Free withdrawal.** Each contract year the owner may withdraw, free of surrender charge
and MVA, up to 10% of purchase payments in year 1 and 10% of the account value at the most
recent anniversary thereafter [S10]. The allowance is non-cumulative and may be taken in
one or several withdrawals [S4] [S16] [std]. A free withdrawal reduces the account value by
the amount paid and reduces the Model #805 floor by the same gross amount [S11].

**Partial withdrawal above the free amount.** For a requested **gross** withdrawal `W`
(the amount removed from the account value) with `FW` of allowance remaining,
`E = max(0, W − FW)`, `C = sc(y) × E` [S8] [S9] [S10], `M = clamp(μ × E, −C, +C)` [S8] [S2],
and the cash paid is `W + M − C`. Charge and adjustment are both computed on `E` before
either is deducted [S8]. Contracts promising a stated net check gross up instead — one
registered prospectus works the case, requiring a $2,099.08 withdrawal to deliver a $2,000
check at an MVA factor of 0.9528 [S3].

**Full surrender — composition order: account value → MVA → surrender charge →
nonforfeiture floor.** With `FW(t)` the unused allowance and `E(t) = AV(t) − FW(t)`:

    C(t)  = sc(y) × E(t)
    M(t)  = clamp( μ(t) × E(t),  −C(t),  +C(t) )
    SV(t) = AV(t) + M(t) − C(t)
    SB(t) = max( SV(t), MGSV(t) )                                    [S8] [S9] [S12]

When the allowance is zero — or when the alternative convention applying the MVA to the
whole account value is selected, as the two registered contracts do [S3] [S4] — this
collapses to the multiplicative form `SB(t) = max( AV(t) × (1 + μ(t) − sc(y)), MGSV(t) )`,
the identity to use when checking dimensional consistency: `μ` and `sc` are both pure rates
on the same currency base. **Whether the MVA reaches inside the free amount differs by
insurer:** it does not for the retail MYGAs [S2] [S9] [S10] [S15] [S16], it does for the two
registered contracts [S3] [S4]. Representative convention: MVA-free inside the free amount
**[std]**, with a switch for the alternative.

**Market value adjustment.** `μ(t) = (i0 − it) × T(t)` with `T(t)` = (days from the
surrender date to the end of the current contract year ÷ 365) + whole years remaining in
the MVA period [S8] [S9]. `i0` is locked at the start of the guarantee period; rising
reference yields give a negative adjustment and falling yields a positive one
[S5] [S9] [S13]. Worked reference (taken from the fixed **index** annuity carrying this MVA
text — do not read the numbers as a MYGA illustration [S8]): 7-year MVA period, $100,000
premium, accumulation value $115,927 at the end of contract year 5, free amount $11,593,
3% charge = $3,130, reference rate 3.00% at issue, `T` = 2. Rate falls to 2.00% →
μ = +2.00%, MVA = +$2,086.69, surrender value $114,884; rate rises to 4.00% → μ = −2.00%,
MVA = −$2,086.69, surrender value $110,711 [S8].

**Minimum guaranteed surrender value.** `MGSV(0) = 0.875 × P` [R1 §4.A(2)](#uslib-fixed_deferred_annuity-r1) [S11] and
`MGSV(t) = [MGSV(t − dt) − withdrawals(t) − charge(t)] × (1 + i_nf)^dt`, with `i_nf` the
contract GMSV rate (2.80% [S11]) constrained to the statutory corridor [R1 §4.B](#uslib-fixed_deferred_annuity-r1) [REG-R42],
`charge(t)` the annual contract charge ($0 representative, $50 statutory maximum [R1] [S11])
and withdrawals deducted gross [S11] [std]. Premium tax actually paid and indebtedness are
further permitted deductions, accumulated at `i_nf`, and are zero here [R1 §4.A](#uslib-fixed_deferred_annuity-r1). Model
#805 §6 separately requires the cash surrender value to be at least the present value of the
accrued paid-up annuity benefit discounted at a rate not more than 1% above the contract
accumulation rate [R1 §6](#uslib-fixed_deferred_annuity-r1); on a book-value MYGA with no richer purchase-rate guarantee the
minimum nonforfeiture amount is the binding leg, and the paid-up-annuity leg is noted but
not implemented **[std]**.

**Guarantee-period end, renewal and shock.** In the 30 days before each guarantee period
ends the owner may withdraw any amount, surrender, renew or elect an income option, in every
case at the **full account value** with no charge and no MVA [S1] [S2] [S5] [S6]. Absent
instruction the contract automatically begins a new period of the same duration at a newly
declared rate [S1] [S5]; under Camp A a fresh 5/4/3/2/1 surrender charge and MVA period
begins [S2] [S11], while under Camp B the contract receives a new rate each anniversary with
no further surrender charge [S13].

**Annuitization.** Available after the first contract year [S1] [S2], at the surrender
value during the surrender charge period and the full account value in the window or after
that period [S1] [S2] [S5] [std]. Payout factors are **not** specified here: no retrieved
product document contains an annuity rate table [S4], so factor construction must come from
the 2012 IAM Basic / Projection Scale G2 machinery [R9] [REG-R59] [REG-R60] plus a chosen
valuation rate, with VM-V §1 governing the statutory maximum valuation rate for the income
stream [REG-R37].

---

## Riders and options

**In scope** (modeled as features of the base contract, no explicit charge):

- **Extended-care / nursing-home waiver.** After contract year 1, confinement to a nursing
  home or LTC facility for ≥90 consecutive days permits withdrawal of up to 100% of the
  account value with no early withdrawal charge; no rider cost [S10]. Trigger variation
  observed: 90 days [S2] [S10]; 45 days with a 3-year request window [S3]; 180 continuous
  days [S4]; 60 days [S13] [S15]; qualified nursing care center after year 1 [S5] [S6].
- **Terminal-illness waiver.** After contract year 1, prognosis of survival of 12 months or
  less permits withdrawal of up to 100% of the account value with no charge; no cost
  [S10] [S2] [S13] [S15].
- **RMD exemption.** RMD amounts free of charge and MVA even above the free allowance
  [S15] [std] (footnote 14).

Where several waivers apply, the highest single free-withdrawal amount applies, not the sum
[S2].

**Out of scope (described, not modeled):** enhanced beneficiary benefit rider paying 40% of
policy earnings at death for issue ages ≤70, capped at 100% of adjusted premiums, charged
0.30% annually as 0.075% of accumulation value each policy quarter and ending after the
25th anniversary [S13]; enhanced spousal continuance rider [S13]; chronic and critical
illness waiver requiring age ≤65 at issue [S15]; disability and unemployment waivers [S13];
SEPP waiver [S2]; small-balance and involuntary termination provisions below $2,500 [S3];
advisory-fee withdrawals of up to 1.50% of contract value annually on RIA-distributed
variants, treated as partial surrenders subject to charge and MVA above the free amount
[S5] [S6]; enhanced-liquidity product variants [S2]; care-benefit variants [S7]. **No
guaranteed living benefit rider appears on any retrieved MYGA** — which is why the shock
lapse here is unsuppressed; the contrast with FIA and VA blocks is the presence or absence
of exactly such a rider [REG-R62] [REG-R64].

---

## Variations across insurers

1. **MVA formula family.** (i) **Geometric discount factor**, `[(1+a)/(1+b)]^t`, on the
   SEC-registered modified guaranteed annuities — one on Treasury note yields with no
   spread [S3], the other on swaps with a 25 bp expense adder [S4]. (ii) **Linear
   duration × rate change**, `(i0 − it) × T`, on the retail MYGAs [S8] [S9]. (iii) **Linear
   declared-rate differential**, `W × (Ic − In) × Fs`, on the insurer's own new-money rate
   against a contractual duration-factor table [S14]. Model #245 §4.I recognizes both the
   external-index and company-declared-rate branches [R4] [REG-R45]. *Chosen:* family (ii) —
   the most common retail form and the one the charge/nonforfeiture anchor pairs with; all
   three are implemented in the technical notes.
2. **MVA caps.** The biggest divergence: symmetric at the withdrawal charge [S2];
   min(charge, interest credited) both ways [S8] [S9]; asymmetric, positive capped and
   negative floored only by the nonforfeiture law [S12]; floored at premium accumulated at
   the GMIR [S13]; uncapped [S3] [S4]. *Chosen:* symmetric at the surrender charge, with the
   cap a first-class model parameter rather than a hard-coded rule.
3. **Free-withdrawal design.** 10% of account value is the convention
   [S2] [S4] [S9] [S10] [S15] [S16], but one carrier's RIA-distributed contract uses an
   **interest-only** allowance equal to the prior year's credited interest [S5] [S6] and
   another a **greatest-of** rule reaching 100% of policy gain for premiums ≥$100,000
   [S13]. *Chosen:* 10% of account value — it is the modal design, it is the design the
   charge and nonforfeiture anchor actually carries [S10] [S11], and it is the only one of
   the three that makes the free amount a *fixed known base* at each anniversary, which is
   what the free-amount/MVA interaction and the `E(t) = AV − FW` composition below both
   need. The interest-only design is channel-specific (RIA/fee-based) and the greatest-of
   design is premium-band conditional, so neither generalizes. Whether the MVA reaches
   inside the free amount also differs (see mechanics).
4. **Renewal architecture.** Camp A — new multi-year period with a fresh, lower charge
   [S1] [S2] [S5] [S11]; Camp B — annually redeclared rates, no new charge [S13]. *Chosen:*
   Camp A, with Camp B as a switch: the two produce entirely different lapse patterns and
   VM-22's own worked examples are built around the distinction [R2] [REG-R36].
5. **Surrender charge shape.** Declining 7%–9% schedules dominate the commission-paid retail
   market (9/8/7/6/5/4/3 [S1]; 9/8/7/6/5 [S10]; the Camp B carrier's 7/6/5/4/3/2/1 in New
   York [S13]); that same carrier's non-New York schedule holds 7% flat for three years
   first [S13]; one registered contract caps the charge at 5% and steps down in pairs [S4];
   an RIA-distributed contract uses a **level 3%** every year paired with the interest-only
   free withdrawal [S5] [S6]. *Chosen:* 9/8/7/6/5 [S10] — it is the schedule of the
   charge/nonforfeiture anchor itself, it is exactly five rates for a five-year guarantee
   period (one per guarantee year, expiring with the term, so the surrender-charge clock and
   the guarantee-period clock coincide and the shock lapse has a single unambiguous date),
   and its 9% first-year level is the steepest in the retail set, which makes the Model #805
   floor bind in the worked example rather than sit inert.
6. **Guaranteed minimum interest rate.** From an explicit 1% renewal floor [S1] [S2], to a
   contract GMIR of 0.25% [S9] [S11] or 1.50% [S14], to **none at all** on one of the
   registered contracts: "there is no minimum Specified Interest Rate for any of the
   Guaranteed Period Options" [S4]. Not cosmetic — VM-22's GMIR Factor steps prescribed base
   lapse by 1.25 / 1.00 / 0.70 across the ≤1.0% / 1.0–2.5% / >2.5% bands [R2] [REG-R36].
   *Chosen:* 0.25% [S11] → GMIR Factor 1.25 — it is the GMIR on the anchor's current ICC24
   form (the 2023 brochure's "1% or higher" [S10] is the superseded print), and it falls in
   VM-22's lowest band, which carries the **highest** base-lapse multiplier. Taking the
   contemporaneous value therefore also takes the conservative end of the prescribed lapse
   scale rather than an assumption-flattering one.
7. **Death benefit.** Full accumulation value, no charge, no MVA [S1] [S2] [S13]; greater of
   accumulation value and minimum surrender value [S5] [S6]; account value only if paid
   within six months of the annuitant's death, MVA-adjusted afterwards or if owner ≠
   annuitant [S3]. *Chosen:* full account value — modal, and it keeps the death benefit
   outside the MVA module entirely.
8. **Guarantee-period-end handling and the surrender-charge clock.** 30-day free-out window
   [S1] [S2] [S5] [S6]; 90 days' notice defaulting into a liquid transition account [S4]; 18
   days' notice with a 5-day election deadline and auto-reinvestment [S3]. The clock runs
   from the start of the current guarantee period [S1] [S2] [S5] [S11] or from the **original
   purchase payment date**, never restarting [S3] [S4]. *Chosen:* the 30-day window with a
   per-period clock — that is what creates the repeating shock lapse under Camp A.

---

## Regulatory context

**NAIC Standard Nonforfeiture Law for Individual Deferred Annuities (Model #805)**
[R1] [REG-R42]. The load-bearing regulation. The minimum nonforfeiture amount is an
accumulation of net considerations (87.5% of gross) at the indexed nonforfeiture rate,
decreased by prior withdrawals, an annual contract charge of up to $50, premium tax actually
paid and indebtedness, all accumulated at the same rate [R1 §4.A](#uslib-fixed_deferred_annuity-r1). The indexed rate is
`min(3%, round(5-yr CMT to the nearest 1/20 of 1%) − 1.25%)` **floored at 15 basis points**
[R1 §4.B](#uslib-fixed_deferred_annuity-r1) — not 1%. The cash surrender benefit may never be less than the minimum
nonforfeiture amount, and the death benefit never less than the cash surrender benefit
[R1 §6](#uslib-fixed_deferred_annuity-r1). Scope exclusions set the library's boundaries: Model #805 does **not** reach
variable annuities, immediate annuities, or a deferred annuity after annuity payments have
commenced [R1 §2](#uslib-fixed_deferred_annuity-r1), nor a compliant index-linked variable annuity, which runs through Model
#250 §7 and AG 54 [REG-R43] [REG-R44]. Model #808, the life nonforfeiture law, has no
application here [REG-R2].

**NAIC Annuity Disclosure Model Regulation (Model #245)** [R4] [REG-R45]. **The correct model
number is #245, not #250; #250 is the Variable Annuity Model Regulation**
[R4] [REG-R43] [REG-R45]. It sets minimum disclosure standards and, in §6, standards for
annuity illustrations. Its §4.I definition of an MVA — "a positive or negative adjustment
... based on **either** the movement of an external index **or** on the company's current
guaranteed interest rate being offered on new premiums or new rates for renewal periods" —
is the regulatory recognition of both MVA branches the model implements [R4]. Delivery:
disclosure document and Buyer's Guide at or before application face-to-face, else within
five business days, failing which a free look of **not less than 15 days** applies
[R4 §5.A](#uslib-fixed_deferred_annuity-r4). Illustrated non-guaranteed elements may be no more favourable than current
elements, may assume no future improvement and must reflect planned changes after an initial
guaranteed period [R4 §6.F(8)](#uslib-fixed_deferred_annuity-r4) — which is why an escalating declared-rate design must be
sold as a guaranteed element rather than a projection [S10].

**NAIC Suitability in Annuity Transactions Model Regulation (Model #275)** [R5] [REG-R46].
The 2020 best-interest revision requires producers to act in the consumer's best interest
and insurers to supervise recommendations [R5 §1.A](#uslib-fixed_deferred_annuity-r5). §6.A(1)(j) requires the producer, on
any exchange or replacement, to consider whether the consumer will incur a surrender charge
or start a **new surrender period**, and whether the consumer has had another exchange or
replacement **within the preceding 60 months** [R5]. That look-back is a genuine behavioral
brake on MYGA-to-MYGA churn at surrender-charge expiry and belongs in the qualitative
justification of any shock-lapse calibration.

**VM-22, Principle-Based Reserves for Non-Variable Annuities** [R2] [REG-R36]. For in-scope
contracts VM-22 **constitutes CARVM** [R2 §1.A](#uslib-fixed_deferred_annuity-r2) and applies for **valuation dates on or
after January 1, 2026** [R2 §2.B](#uslib-fixed_deferred_annuity-r2). A company may keep business issued in the first three
years after the effective date on VM-A/VM-C/VM-M/VM-V; once elected for a block VM-22 PBR
must continue; and all applicable blocks must be on VM-22 PBR prospectively starting three
years after the effective date [R2 §2.B](#uslib-fixed_deferred_annuity-r2) (2029 is arithmetic — the text prints the rule, not
the date [unverified]). A MYGA sits in the **Accumulation Reserving Category** [R2].
Aggregate reserve = stochastic reserve + deterministic reserve for contracts passing the
Single Scenario Test + reserves for excluded contracts valued formulaically; the additional
standard projection amount is **disclosure-only** under VM-31 [R2 §3](#uslib-fixed_deferred_annuity-r2).

**Formulaic CARVM — A-820, AG 33 and the VM-C guideline family**
[REG-R153] [REG-R151] [R7] [REG-R41]. Where VM-22 PBR does not apply (transition election,
exclusion test), the reserve remains formulaic CARVM — the greatest-of-excesses
construction printed at **AP&P Appendix A-820 ¶15**, whose ¶14 scope gate admits this
contract (¶15 reaches all annuity contracts other than qualified-plan group annuity
business, which ¶13.b routes to a CRVM-consistent method) [REG-R153 ¶¶13.b, 14, 15](#uslib-reg-r153) —
read through **Actuarial Guideline XXXIII**, whose text has now been **read in full** as
printed in the AP&P Manual Appendix C [REG-R151] (superseding the title-only record at
[REG-R39]). Its applicability sentence reaches "all annuity contracts subject to CARVM,
where any elective benefits … are available to the contract owner", so this chassis — full
surrender, partial withdrawal, annuitization by option — is squarely inside
[REG-R151 *Purpose*](#uslib-reg-r151). **Two records this file previously carried are corrected.** The
printed title is **"Determining CARVM Reserves for Annuity Contracts With Elective
Benefits"**, not the Rev. Rul. 2002-6 wording; and the printed *Effective Date* block reads
"This guideline shall be effective on **December 31, 1998**, affecting all contracts issued
on or after January 1, 1981" [REG-R151 *Effective Date*](#uslib-reg-r151), against the **December 31, 1995**
date carried here from Rev. Rul. 2002-6 for a differently-titled instrument [R7]. **Both
dates are recorded and the reconciliation is unresolved**: the extracted pages carry no
amendment history, so the natural reading — that the guideline was later revised — is an
inference, not a fact from either source. The 1 January 1981 issue-date reach is common to
both, and the guideline's 33⅓ / 66⅔ / 100% grade-in ran off by December 31, 2000, so it has
**no live effect on any current valuation** [REG-R151 *Effective Date*](#uslib-reg-r151). AG 33 contains **no
formulas, tables or factors** beyond the 7% expense-allowance cap and those phase-in
percentages, and it **never cites SVL §5a by number** — the §5a mapping used throughout this
library is the library's own, made on content [REG-R151] [REG-R1 §5a.B](#uslib-reg-r1). Mechanics are in the
primary-text extractions `_research/appp-a820-a821-a822.md` and `_research/appp-ag33.md`.
VM-C is the
authoritative index of which guidelines the Valuation Manual incorporates, including AG
VIII, AG XIII, AG XXXIII and AG XLI [REG-R41]. For the payout phase VM-V §1 carries the
statutory maximum valuation interest rate and supersedes the interest guidance in AG IX-B
and IX-C [REG-R37].

**SEC registration** [S3] [S4] [REG-R49]. A fixed deferred annuity whose MVA is not adequately
limited is sold as a registered **modified guaranteed annuity**: both uncapped-MVA contracts
in the source set are SEC-registered with statutory prospectuses [S3] [S4], while the capped
retail MYGAs are not [S2] [S8] [S9] [S12] [unverified as a legal test]. The SEC's 2024
rulemaking moved registered index-linked and **registered market value adjustment**
annuities onto **Form N-4** with tailored disclosure of contract adjustments and surrender
charges and a prescribed Key Information Table; effective September 23, 2024, compliance
date May 1, 2026 [REG-R49; that entry flags the compliance date](#uslib-reg-r49) [unverified]. The
representative contract has a capped MVA and is outside that regime. **That SEC category is
not the statutory instrument of the same name.** AP&P Appendix A-255, "Modified Guaranteed
Annuities", defines the term by asset location — "a deferred annuity contract … the
underlying assets of which are held in a separate account", with "nonforfeiture values that
are based upon a market-value adjustment formula if held for shorter periods", the assets
having to be in that separate account "during the period or periods when the contract holder
can surrender the contract" [REG-R157 ¶1](#uslib-reg-r157). This chassis is a general account obligation with
no separate account, so **A-255 does not reach it**; where it does reach a contract it
delegates the reserve method itself to A-820 and adds one floor — the separate account
liability at least equal to the surrender value produced by **the contract's own**
market-value-adjustment formula, with a transfer of assets to make good any shortfall
[REG-R157 ¶5](#uslib-reg-r157). A-255 prints **no MVA formula, no parameters for one, and does not mention
CARVM** [REG-R157].

**Federal tax — IRC §72 and §1035** [R6] [REG-R55] [REG-R56]. Pre-annuitization withdrawals
are taxed **income-first (LIFO)**: the taxable portion is the excess of "the cash value of
the contract (determined **without regard to any surrender charge**) immediately before the
amount is received" over the investment in the contract [R6 §72(e)(3)(A)](#uslib-fixed_deferred_annuity-r6) — the tax base is
the **account value, not the surrender value**. Annuity payments use the exclusion ratio of
investment in the contract to expected return at the annuity starting date, capped at
unrecovered investment [R6 §72(b)](#uslib-fixed_deferred_annuity-r6). A 10% penalty applies to the includible portion of
premature distributions under §72(q), with exceptions for age 59½, death, disability, SEPP
and immediate annuities [R6]; all annuity contracts issued by the same company to the same
policyholder in one calendar year are treated as one contract [REG-R55]. §1035 permits
tax-free annuity-to-annuity exchange but **not** annuity-to-life [REG-R56] — the mechanism
behind most shock-lapse outflow. Under IRC §807 the tax reserve is the greater of the net
surrender value and, post-TCJA, **92.81% of** the NAIC-prescribed method reserve (CARVM),
capped at the statutory reserve [R7] [REG-R16], so one projection feeds both engines.

**Actuarial standards.** ASOP No. 2 governs redetermination of the declared renewal rate as
a non-guaranteed element, its scope expressly covering fixed deferred annuities [REG-R26];
ASOP No. 7 is the general standard for the asset/liability cash-flow analysis this model
performs — the disintermediation, reinvestment and MVA exposure that defines a MYGA block
[REG-R27]; ASOP No. 22 governs
asset-adequacy opinions, the classic MYGA exposure [REG-R29]; ASOP No. 56 is the
model-governance frame [REG-R32], ASOP No. 54 the pricing standard [REG-R70], and ASOP No.
10 with FASB ASU 2018-12 the U.S. GAAP (LDTI) measurement frame [REG-R71] [REG-R34].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-fixed_deferred_annuity-r1
[R2]: #uslib-fixed_deferred_annuity-r2
[R4]: #uslib-fixed_deferred_annuity-r4
[R5]: #uslib-fixed_deferred_annuity-r5
[R6]: #uslib-fixed_deferred_annuity-r6
[R7]: #uslib-fixed_deferred_annuity-r7
[R8]: #uslib-fixed_deferred_annuity-r8
[R9]: #uslib-fixed_deferred_annuity-r9
[REG-R151]: #uslib-reg-r151
[REG-R153]: #uslib-reg-r153
[REG-R157]: #uslib-reg-r157
[REG-R16]: #uslib-reg-r16
[REG-R2]: #uslib-reg-r2
[REG-R26]: #uslib-reg-r26
[REG-R27]: #uslib-reg-r27
[REG-R29]: #uslib-reg-r29
[REG-R32]: #uslib-reg-r32
[REG-R34]: #uslib-reg-r34
[REG-R36]: #uslib-reg-r36
[REG-R37]: #uslib-reg-r37
[REG-R39]: #uslib-reg-r39
[REG-R41]: #uslib-reg-r41
[REG-R42]: #uslib-reg-r42
[REG-R43]: #uslib-reg-r43
[REG-R44]: #uslib-reg-r44
[REG-R45]: #uslib-reg-r45
[REG-R46]: #uslib-reg-r46
[REG-R49]: #uslib-reg-r49
[REG-R55]: #uslib-reg-r55
[REG-R56]: #uslib-reg-r56
[REG-R59]: #uslib-reg-r59
[REG-R60]: #uslib-reg-r60
[REG-R62]: #uslib-reg-r62
[REG-R63]: #uslib-reg-r63
[REG-R64]: #uslib-reg-r64
[REG-R70]: #uslib-reg-r70
[REG-R71]: #uslib-reg-r71
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
