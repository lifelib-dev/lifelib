# Product Specification

**Status:** Draft, 2026-08-04; AP&P Manual appendix material added 2026-08-06. All cited
sources accessed 2026-08-04 **except** [REG-R151] (AG 33) and [REG-R156] (A-250), accessed
**2026-08-06**.

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling of a U.S. individual deferred variable annuity (VA) carrying
a guaranteed lifetime withdrawal benefit (GLWB/GMWB) and a guaranteed minimum death
benefit (GMDB). It does not describe any single insurer's product. Tag conventions:
**[S#]/[R#]** resolve against the product research file `_research/variable-annuity.md`
(its own local numbering: S1–S8 product documents, R1–R13 regulatory/actuarial
references). **[REG-R#]** resolves against the **single shared cross-product numbering
space R1–R157** curated at `references/regulatory-and-actuarial-references.md`; R1–R34
originate in `_research/regulatory-actuarial.md` (life-origin, several of which also
bind annuities), R35–R72 in `_research/regulatory-actuarial-annuities.md`
(annuity-specific) and **R151–R157** in the AP&P Manual appendix extractions read at
first hand on 2026-08-06 (**AG 33** [REG-R151] and **A-250** [REG-R156] are the two cited
here), with most of the **R73–R149** block unused — one tag prefix, one numbering
space. **[std]** marks a
standardization introduced for the reference implementation; every [std] table row carries
a footnote giving the rationale and the observed range across insurers. **[unverified]**
marks a claim the research file could not confirm against a retrieved document; such flags
are carried forward, never quietly dropped.

**Implementation anchor.** The **Jackson National Perspective II** chassis — statutory
prospectus dated April 28, 2025 [S1], initial summary prospectus [S2], rate sheet
supplement dated April 27, 2026 [S3] — because it is the most contractually explicit
disclosure in the set and exercises every mechanic a general VA model needs [S1]. Two
documented variants ride alongside: the **Corebridge VIX-linked non-discretionary rider
fee formula** [S4] [S6] and the **Equitable formula-linked roll-up rate** (10-year CMT +
1.00%, floored 4%, capped 8%) [S7].

---

## Product overview and market role

A deferred VA has two phases: accumulation and income. Once annuitized, withdrawals and
surrender cease and — with rider-specific exceptions — death and living benefits terminate
[S2] [S4] [S6] [S7] [S8]. During accumulation, premium net of any premium tax buys units in
subaccounts of a registered separate account, each investing in one underlying fund
("Investment Divisions" [S1] [S2]; "Variable Portfolios" [S4] [S6]; "variable investment
options" [S7]; "Subaccounts" [S8]). Contract value follows fund performance with no
insurer guarantee; the guarantees are sold as *riders* tracked on shadow **benefit bases**
that do not follow the market down. The economic content is therefore an investment
wrapper plus two written options: a GLWB (a lifetime payment stream funded by the insurer
once the account is exhausted) and a GMDB (a floor under the death benefit). Both are
path-dependent guarantees on a separate-account balance — which is why their cost cannot
be established deterministically and why the statutory reserve for the whole contract is a
stochastic CTE70 measure under VM-21 [R1] [REG-R35].

VAs are federally registered securities sold on **SEC Form N-4** [R6] [REG-R52], with
layered disclosure under **Rule 498A** (Initial and Updating Summary Prospectuses and a
mandatory Key Information Table) [R7] [REG-R50] [REG-R51]. Modern writers reset GLWB payout
percentages, bonus percentages and rider charges through **rate sheet prospectus
supplements filed on Form 497** rather than by amending the prospectus [S3] [S5] — a
structural fact any model of this product must accommodate, because the parameter set is
versioned by rate-sheet date, not by product name.

---

## Representative specification

### Contract identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Individual flexible-premium deferred variable annuity, non-participating | [S1] [S2] |
| Funding | Separate account only; general-account Fixed Account Options **not available** with the elected Roll-up GMDB | [S1] |
| Subaccounts modeled | 2 (one diversified equity, one fixed income) | **[std]** (1) |
| Allocation | 60% equity / 40% fixed income, no rebalancing | **[std]** (1) |
| Tax status | Non-qualified | **[std]** (2) |
| Maximum issue age | 85 | [S1] |
| Anchor model cell | Male, issue age 60, single Designated Life | **[std]** (3) |
| Premium pattern | Single premium $100,000 at issue | **[std]** (4) |
| Minimum initial premium | $10,000 non-qualified; $5,000 qualified | [S2] |
| Minimum subsequent premium | $500 ($50 under an automatic payment plan) | [S2] |
| Maximum total premiums | $1,000,000 without prior approval | [S2] |
| Premium tax | 0.00% in the base model, within an observed 0.0%–3.5% state range | **[std]** (5); range [S2] |
| Latest Income Date | Contract Anniversary on which the Owner is age 95 | [S2] |

Footnotes to [std] rows:

1. Two subaccounts is the minimum that exercises pro-rata charge allocation and unit
   accounting; real contracts offer far more (Corebridge Build Your Own Allocation lists
   76 options across 12 asset classes [S4]). The 60/40 split is a modeling convention — no
   fetched document prescribes an allocation for this chassis. The *other* designs impose
   hard allocation controls this one does not: Corebridge requires a 20% (Income Max) or
   10% (Daily Flex) general-account Secure Value Account plus mandatory quarterly
   rebalancing [S4]; Equitable walls guarantees into a separate Protection account [S7].
2. Non-qualified keeps the RMD interaction in the GLWB withdrawal rules *disclosed but
   inactive*; RMD relief is a cited mechanic [S1] [S6] and belongs in the model as a switch.
3. Issue age 60 sits inside the GMWB eligible band (35–80 [S1]) and the add-on GMDB band
   (79 or younger at issue [S1]), above the 59½ threshold at which the For Life Guarantee
   is effective from issue [S1], and at or below 69 so the higher 6.00% GMDB roll-up
   percentage applies [S3].
4. Single premium keeps the base recursion minimal. The chassis is flexible-premium
   [S1] [S2]; premium receipt increases the GWB, GAWA and Bonus Base [S1] and is retained
   in the recursion as an active term.
5. Set to zero so GWB(0) equals gross premium and the worked example is checkable; premium
   tax is contractually deducted from the amounts that initialize the guarantee bases [S1].

### Separate account and base contract charges

| Parameter | Representative value | Basis |
|---|---|---|
| Total base contract asset charge | 1.30% p.a. of average daily separate-account value | [S2] |
| — mortality & expense risk (M&E) component | 1.00% p.a. | **[std]** (6) |
| — administrative asset charge component | 0.30% p.a. | [S7] component value; split **[std]** (6) |
| Large-contract reduction | 1.15% p.a. if contract value ≥ $1,000,000 at the later of issue or the most recent Contract Quarterly Anniversary | [S2] |
| Annual contract maintenance charge | $35, waived if contract value ≥ $50,000; deducted proportionally across investment divisions on the Contract Anniversary or on total withdrawal | [S2] |
| Fund expense — equity subaccount | 0.95% p.a. of fund net assets | **[std]** (7) |
| Fund expense — fixed income subaccount | 0.65% p.a. of fund net assets | **[std]** (7) |
| Transfer charge | $25 per transfer after 25 transfers in a Contract Year (reserved right) | [S2] |

6. Jackson blends M&E and administration into one "Core Contract Charge" of 1.30% maximum
   assessed daily on average daily Investment Division value [S2]; its Key Information
   Table shows base contract cost 1.31% minimum = 1.31% maximum including the amortized
   contract fee [S2], i.e. current equals contractual maximum. Equitable alone unbundles —
   Series B: operations 0.80% + administration 0.30% + distribution 0.20% = 1.30% [S7]. The
   composite therefore takes the **0.30% administrative component directly from [S7]** and
   assigns the 1.00% residual to M&E **[std]**, so the parts sum exactly to the cited 1.30%
   total [S2]. Observed totals: Jackson 1.30% [S2]; Corebridge Polaris Choice IV 1.65%
   [S6]; Corebridge Polaris Advisory 0.40% [S4]; Equitable 0.65% (ADV) to 1.70% (C) [S7];
   Lincoln 1.55%–1.90% by elected death benefit [S8].
7. Observed fund expense ranges: 0.52%–2.28% (Jackson, stated as of December 31, 2021, so
   indicative rather than current [S2]); 0.46%–1.85% [S6]; 0.21%–1.60% [S4]; 0.27%–3.48%
   [S8]. The two [std] values sit inside all four with the usual equity/bond ordering.

### Contingent deferred sales charge (withdrawal charge) and free withdrawal

| Parameter | Representative value | Basis |
|---|---|---|
| CDSC basis | Percentage of *Remaining Premium* withdrawn, by **completed years since receipt of that premium** (not contract year) | [S2] |
| CDSC schedule | 0–1 yr 8.5%; 1–2 7.5%; 2–3 6.5%; 3–4 5.5%; 4–5 5.0%; 5–6 4.0%; 6–7 2.0%; 7+ 0.0% | [S2] |
| Remaining Premium | Total premium paid, reduced by withdrawals of premium (including withdrawal charges), before adjustment for MVA or charges | [S2] |
| Free withdrawal | 10% of Remaining Premium each Contract Year that would otherwise incur a charge, **minus earnings**; earnings (contract value less Remaining Premium) come out free first; aged-out premium is also free; RMD withdrawals reduce the allowance | [S1] |
| Guaranteed-withdrawal carve-out | Cumulative withdrawals within the GLWB annual limit incur **no** withdrawal charge | [S1] |
| Terminal illness / extended care waiver | Increases the charge-free amount on a 12-month terminal prognosis or 90 consecutive days' confinement; maximum $250,000 of contract value; exercisable once | [S2] |

### GLWB rider — representative election: Flex GMWB, Single life, "Core" benefit option

| Parameter | Representative value | Basis |
|---|---|---|
| Benefit base name | Guaranteed Withdrawal Balance (GWB) | [S1] |
| GWB at issue | Premium net of premium tax = $100,000 | [S1] |
| Rider charge — current | 1.25% p.a. of the GWB | [S3] |
| Rider charge — assessment | Quarterly, at rate/4 applied to the GWB on the Contract Quarterly Anniversary | frequency [S1]; base [S1] [S3] |
| Rider charge — deduction | Cancelled from subaccounts pro rata to their values | **[std]** (8) |
| Rider charge — guaranteed maximum | 3.00% p.a. | **[std]** (9) |
| Rider charge — maximum single increase | +0.25% per increase (Core-tier options) | [S1] |
| Rider charge — reset mechanism | Discretionary increase permitted on **each fifth Contract Anniversary**, with an irrevocable opt-out | [S1]; selection **[std]** (10) |
| Bonus (roll-up) percentage | 6.00% of the Bonus Base | [S3] |
| Bonus condition | Credited to the GWB at the end of each Contract Year *in which no withdrawal was taken*, within the Bonus Period | [S1] |
| Bonus Period | 10 Contract Years from the endorsement effective date, **restarting** on each Bonus-Base-increasing step-up occurring on or before the anniversary following the Designated Life's 80th birthday | [S1] |
| Step-up basis | Annual Contract Value on each Contract Anniversary | [S3] |
| GWB Adjustment percentage | 105% | [S3] |
| GWB Adjustment Date | Later of the anniversary on/after the Designated Life's 70th birthday and the 12th Contract Anniversary; applies only if no withdrawal has been taken by then | [S1] |
| GAWA% by attained age at first withdrawal | 35–59: 4.00%; 60–64: 4.00%; 65–69: 5.55%; 70–74: 5.75%; 75–80: 5.95%; 81+: 6.20% | [S3] |
| For Life Guarantee | Effective at issue because the Designated Life is 59½ or older | [S1] |
| Benefit base cap | GWB and Bonus Base each capped at $10,000,000 | [S1] |
| Eligible ages | Designated Lives 35–80 | [S1] |

8. The research file records the rider charge's *base* (GWB) and *frequency* (quarterly)
   [S1], and records that the annual contract maintenance charge is deducted
   **proportionally** across investment divisions [S2], but records no allocation rule for
   the rider charge itself. Pro-rata deduction is therefore a **[std]** convention extended
   from the cited contract-fee rule [S2] — near-universal in practice, but not on this
   evidence a cited contract term.
9. Guaranteed maxima in the historical charge appendix run **1.20% to 3.00%** by option and
   vintage — Flex Net GMWB Core max 3.00% / current 1.30%; Flex Net Value max 1.70% /
   current 0.60%; Flex Net Joint Core max 3.00% / current 1.60%; LifeGuard Freedom Net max
   2.90% / current 1.45% [S1]. **No guaranteed maximum is recorded for the
   currently-offered Flex GMWB Single Core option itself**, so 3.00% is a [std] pick at the
   top of the observed band. Cross-insurer maxima: 2.50% with a 0.60% minimum [S4]; 2.75%
   single and joint [S8]; 1.25% [S7].
10. Three reset mechanisms exist in the set; all three are documented under "Contractual
    mechanics" below. The model defaults to the Jackson five-yearly discretionary reset
    **[std]** because it matches the chassis, with the VIX-squared formula as a variant.

### GMDB rider — representative election: Roll-up GMDB

| Parameter | Representative value | Basis |
|---|---|---|
| Benefit form | Greatest of contract value, total Net Premiums, and the roll-up GMDB Benefit Base | [S1] |
| Roll-up percentage | 6.00% p.a. compounded (age 69 or younger at election); 5.00% if age 70 or older | [S3] |
| Roll-up accrual window | From the Issue Date until the Contract Anniversary immediately preceding the oldest Covered Life's **81st** birthday | [S1] |
| Rider charge — current | 0.90% p.a. of the GMDB Benefit Base | [S2] [S3] |
| Rider charge — guaranteed maximum | 1.80% p.a. | [S2] |
| Rider charge — assessment | Quarterly at rate/4 on the GMDB Benefit Base, deducted pro rata | frequency **[std]** (11); base [S3] |
| Withdrawal adjustment | Dollar-for-dollar up to `roll-up% × Benefit Base at the previous anniversary`; **proportional** to the contract-value reduction above that; applied at the **end of the Contract Year** | [S1] |
| Eligibility | Owner age 79 or younger at issue | [S1] |
| Interaction | Fixed Account Options are **unavailable** when this GMDB is elected | [S1] |
| Included basic death benefit (no charge) | Greater of contract value and total premiums reduced for prior withdrawals **in the same proportion the contract value was reduced** — a *proportional* return-of-premium, not dollar-for-dollar | [S1] [S2] |

11. The research file records charge frequency **quarterly** for the GMWB family [S1] but
    does not state the frequency for the add-on GMDB charge; the [std] choice aligns the
    two so a single quarterly charge routine serves both. The charge *base* (GMDB Benefit
    Base) and rate (0.90% current / 1.80% maximum) are cited [S2] [S3].

---

## Contractual mechanics

### Account value and unit accounting

Contract value is the sum over subaccounts of units held times unit value. Unit value
evolves with the fund's gross return less the fund's own expenses less the base contract
asset charge, assessed **daily as a percentage of the average daily account value of the
Investment Divisions** [S2]. Charges assessed per contract rather than per unit of value —
the annual contract maintenance charge [S2] and the two rider charges [S1] [S3] — are
collected by **cancelling units**, leaving unit value undisturbed. The generic
separate-account charge-accrual convention is specified once in
`products/variable_ul/technical-notes.md` and reused here, with two differences that
follow from that being a **life** file: it works at the subaccount-value level and carries
no unit count, so the unit ledger above is stated here rather than inherited; and a VA has
**no cost of insurance and no IRC §7702 corridor**, its guarantees being GMDB and GLWB
benefit bases rather than a death benefit on a net amount at risk.

### GLWB benefit base — the core algebra

All withdrawals count toward the GLWB annual limit, including automatic withdrawals, RMDs,
advisory-fee withdrawals, partial 1035 exchanges and free withdrawals; for guarantee
purposes a withdrawal is the **total amount withdrawn including withdrawal charges, asset
allocation fees, market value adjustments and other charges and adjustments** [S1].
Withdrawals under IRC §72(t)/§72(q) are **not** treated as RMDs for guarantee-preservation
purposes [S1] [R9]. Let `W` be the current partial withdrawal, `ΣW` cumulative withdrawals
in the Contract Year including `W`, and `L = max(GAWA, RMD)` for a qualified contract
(`L = GAWA` otherwise) [S1]:

    Excess Withdrawal  E = min( W , ΣW − L )   if ΣW > L, else 0
    Non-excess portion N = W − E

    If ΣW ≤ L :   GWB_new  = max( GWB_old − W , 0 );      GAWA unchanged
    If ΣW > L :   GWB_new  = max( (GWB_old − N) × (1 − E / CV_pre_excess) , 0 )
                  GAWA_new = min( GAWA_old × (1 − E / CV_pre_excess) , GWB_new )

where `CV_pre_excess` is the contract value after the non-excess portion has been
deducted. This is **dollar-for-dollar for the guaranteed portion, then pro rata to the
contract-value reduction caused by the excess** [S1] — a treatment that is essentially
universal across the set [S1] [S4] [S7] [S8]. If the For Life Guarantee is not in effect and
GWB < GAWA at the end of a Contract Year, GAWA is set equal to GWB [S1].

**Bonus.** `GWB += Bonus% × Bonus Base` at the end of each Contract Year in the Bonus
Period in which no withdrawal was taken; any withdrawal, including an automatic withdrawal
or RMD, kills that year's bonus [S1]. The Bonus Base initializes at GWB, increases by net
premium, is set to `min(GWB_after, BB_before)` on an excess withdrawal and to
`max(GWB_after_step-up, BB_before)` on a step-up, and is otherwise unaffected by
withdrawals; applying the bonus does not change it [S1].

**Step-up.** On each Contract Anniversary, if contract value exceeds the GWB, the GWB
resets to contract value [S1]; the representative basis is the anniversary Contract Value
[S3]. The alternative fixed at election is the **Highest Quarterly Contract Value** — the
highest *quarterly adjusted* contract value over the four most recent Contract Quarterly
Anniversaries, each adjusted for subsequent premiums (net of tax) and withdrawals under the
same dollar-for-dollar / proportional rule [S1]. After the first withdrawal a step-up sets
`GAWA_new = max(GAWA% × GWB_new, GAWA_old)` [S1].

**GWB Adjustment.** A one-shot deferral reward: on the GWB Adjustment Date,
`GWB = max(GWB, GWB Adjustment)`, the adjustment initializing at `105% × GWB at
endorsement` [S3], provided no partial withdrawal has been taken by then; any earlier
withdrawal voids it without value and the provision terminates [S1].

**Contract value zero.** With the For Life Guarantee in effect, annual payments of GAWA
continue for the life of the Designated Life while the contract remains in the
accumulation phase; without it, payments continue until the earlier of death or GWB
depletion, the final payment truncated to the remaining GWB [S1]. All other contract rights
cease: no further premiums, all other endorsements terminate without value, and **no death
benefit is payable on subsequent death** [S1].

### GMDB

The death benefit is the greatest of contract value, total Net Premiums and the roll-up
Benefit Base [S1]; the *guarantee* component — the insurer's general-account cost — is the
excess of that over contract value. Add-on death benefits may retain value on or after the
Income Date: at the Latest Income Date the death benefit becomes `GMDB Benefit Base −
contract value`; at an earlier Income Date the endorsement terminates with no benefit [S1].

### Rider fee reset provisions — three documented mechanisms

1. **Periodic discretionary reset with a forfeiting opt-out ([std] default).** The GMWB
   charge may be increased on each fifth Contract Anniversary, subject to a stated maximum
   single increase (+0.25% Core-tier, +0.15% Value-tier) and an absolute maximum rate. The
   owner may opt out, but doing so forfeits the GWB bonus, the automatic step-up, the GWB
   Adjustment and any other increases to GWB/GAWA; blocks all future premiums; and fixes
   the GAWA% with no future recalculation. The election is irrevocable [S1] [S3].
2. **Step-up-triggered reset with a reversing opt-out.** The fee rate may increase on every
   Account Value Step-up, and after the tenth Benefit Year on every Enhancement if the
   Enhancement Period has renewed. Opting out within 30 days of the Benefit Year
   anniversary reverses *both* the fee rate and the Protected Income Base to their
   pre-step-up levels, for that year only. The rate also rises **with no opt-out** once
   cumulative purchase payments after the first Benefit Year anniversary reach $100,000 [S8].
3. **Non-discretionary VIX-squared formula reset.** For each Benefit Quarter,

       Annual Fee Rate(t) = Initial Annual Fee Rate
                          + 0.05% × [ QuarterlyAverage(Daily VIX²) / 33 − 10 ]

   clipped to a movement band against the prior quarter's rate (±0.40% annualized advisory
   class, ±0.25% commission class) and to an absolute corridor of [0.60%, 2.50%]; the
   quarterly deduction is the annual rate ÷ 4 [S4] [S6]. Disclosed examples: initial rate
   1.45% with quarterly average VIX² of 204.42 gives 1.45% + 0.05% × (−3.81) = **1.26%**
   (quarterly 0.3150%); a VIX² average of 602.30 gives an unclipped 1.86%, but against a
   prior rate of 1.42% the +0.40% band caps it at **1.82%** [S4].

A fourth mechanism resets the **benefit growth rate rather than the fee**: the Equitable
Annual Roll-up rate is the average of daily 10-year U.S. Treasury rates over the 20
calendar days ending on the 15th day of the last month of the preceding calendar quarter,
**plus 1.00%**, rounded to 0.10%, floored at **4%**, capped at **8%**; the
pre-first-withdrawal Deferral bonus rate uses **+1.50%** on the same formula and floor/cap
and terminates permanently on the first withdrawal from the Protection account [S7].

---

## Riders and options

**In scope (modeled).** Flex GMWB Single Core and the Roll-up GMDB, both parameterized in
the tables above [S1] [S3]; the included Basic Death Benefit (no charge, proportional return
of premium) [S1] [S2]; the CDSC and free-withdrawal allowance [S1] [S2].

**Described but not modeled.** Terminal Illness / Extended Care Benefit (free with all
contracts) [S2]; the rider-created annuitization options — Life Income of GAWA, Specified
Period Income of the GAWA (years = GWB ÷ GAWA), and the AutoGuard Fixed Payment Income
Option [S1]; spousal continuation of the GMWB without the For Life Guarantee [S1].

**Out of scope.** Joint-life Flex GMWB, Flex Net GMWB, Flex Strategic Income GMWB
(accelerated-then-standard payout), AutoGuard non-lifetime GMWB at a flat 5.00% GAWA%, and
MarketGuard Stretch [S3]; the Highest Quarterly Anniversary Value and Combination
Roll-up + HQAV GMDBs [S3]; Flex DB, a GMWB-linked death benefit with a 100.00% step-up
percentage [S3]; EarningsMax (40% of earnings if issue age < 70, 25% at 70–75, earnings
capped at 250% of remaining premiums; closed 2023-08-28) [S1]; the Four Year Withdrawal
Charge Schedule option (+0.40%) and the Capital Protection Program, a closed self-funded
GMAB-equivalent [S1]; Fixed Account Options and their market value adjustment, excluded
here by the Roll-up GMDB election [S1]; dollar cost averaging, DCA+, Earnings Sweep and
rebalancing programs [S2]; GMIB/annuitization guarantees such as the Equitable GIB [S7];
payout-phase guarantees such as Lincoln i4LIFE® Advantage [S8]; and Corebridge's mandatory
Secure Value Account allocation [S4]. **No currently-sold GMAB was located in the four
registrations read** — a research gap, not an omission [S1].

---

## Variations across insurers

1. **Where the guarantee sits.** Jackson [S1] and Corebridge [S4] use the mainstream
   design — one contract value, a shadow benefit base, guaranteed withdrawals while
   contract value > 0, insurer-funded payments after zero. Equitable bifurcates into an
   *Investment Performance account* (no guarantees) and a *Protection with Investment
   Performance account* (funds the guarantees), with an annuitization rather than a
   withdrawal guarantee [S7]. Lincoln offers both a conventional GLWB and i4LIFE®, a
   variable annuitization payout rider with a guaranteed floor [S8]. **Chosen:** the
   mainstream withdrawal-phase design — the one a general VA model must handle, and the
   one with published algebra [S1].
2. **How the benefit base grows.** Four mechanics: a bonus on a separate Bonus Base with a
   10-year window that restarts on step-up (Jackson, 5%/6%/7% by option) [S1] [S3]; a 7.00%
   Income Credit on an Income Credit Base that ratchets to Higher Anniversary Values but is
   *not* increased by the credits themselves, making the roll-up simple rather than
   compound (Corebridge Income Max) [S4] [S5]; a formula rate of 10-year CMT + 1.00% floored
   4% capped 8% (Equitable) [S7]; and a flat 6% Enhancement over a 10-year period that does
   **not** reset for current elections (Lincoln) [S8]. **Chosen:** the Jackson
   bonus-with-restarting-window — the restart-on-step-up interaction is the hardest of the
   four to model and subsumes the flat-window designs.
3. **Step-up frequency spans three orders of granularity:** annual anniversary (Jackson
   Value/Core, Lincoln, Corebridge Income Max), highest-of-four-quarters applied annually
   (Jackson Plus), and **daily** (Corebridge Daily Flex, where "on any day that the
   contract value is greater than the Income Base on that day, the Income Base is stepped
   up to that value") [S1] [S3] [S4] [S8]. **Chosen:** annual, with the highest-quarterly
   variant as an election so the model can price the granularity difference.
4. **Rider fee base and frequency.** The base is consistently the *benefit base*, never
   account value: GWB [S3], Income Base [S4], GIB benefit base [S7], Protected Income Base
   [S8]. Frequency is quarterly at Jackson [S1], Corebridge [S4] and Lincoln [S8], while
   Equitable deducts on each contract date anniversary [S7]. (The research file's
   cross-insurer summary calls all four quarterly; this specification follows the
   per-insurer extraction.) **Chosen:** quarterly on the benefit base.
5. **Fee reset mechanism** differs sharply — five-yearly discretionary with a forfeiting
   opt-out [S1], step-up-triggered with a reversing opt-out plus a no-opt-out
   $100,000-premium trigger [S8], and the non-discretionary VIX² formula [S4]. **Chosen:**
   the five-yearly reset as default, with the VIX² formula as a variant because it is the
   only one that is a deterministic function of an observable market variable, and so the
   only one a model can reproduce faithfully.
6. **Investment-risk controls.** Corebridge imposes the strongest — a mandatory Secure
   Value Account (20% with Income Max, 10% with Daily Flex) that cannot be transferred out
   unless the living benefit is cancelled, plus mandatory quarterly rebalancing [S4].
   Equitable restricts which account funds guarantees [S7]; Lincoln uses Investment
   Requirements and managed-risk fund suites [S8]; Jackson restricts the *fixed* account
   instead — Fixed Account Options are unavailable with the Roll-up GMDB, Combination GMDB,
   Flex DB or EarningsMax [S1]. **Chosen:** the Jackson restriction, which removes the
   fixed account and its MVA from the base model.
7. **GMDB growth ceilings** differ by age: Jackson stops all roll-up and ratchet growth at
   the anniversary preceding the oldest Covered Life's **81st** birthday [S1]; Equitable's
   Highest Anniversary Value ratchets to the anniversary following the **85th** and the
   Roll-up to age 85 base stops there [S7]; Corebridge's Maximum Anniversary Value has no
   stated cutoff in the retrieved text, though its spousal-continuation version stops at
   the continuing spouse's 83rd birthday [S6]. **Chosen:** age 81, matching the chassis.
8. **Share-class structure** trades surrender charge against asset charge. Equitable is the
   clearest illustration: Series B 1.30% total with a 7-year schedule; L 1.65% with 4
   years; C 1.70% with none; CP® 1.55% with a 4–5% credit and 9 years; ADV 0.65% with none
   [S7]. Corebridge shows the same trade across two registrations — Polaris Choice IV at
   1.65% with an 8/7/6/5 schedule [S6] versus Polaris Advisory at 0.40% with no withdrawal
   charge [S4]. **Chosen:** a commission-style class with a 7-year CDSC, because the CDSC
   drives both the expiry lapse shock and the free-withdrawal interaction.
9. **Post-depletion payout rate.** Lincoln alone uses a **two-table** structure: Table A
   while contract value > 0, and a materially lower Table B once it reaches zero, at which
   point the payment is recalculated as `Protected Income Base × Table B rate` (Select Max
   ages 70–74: 8.75% single falling to 3.50%) [S8]. Jackson, Corebridge and Equitable
   continue at the same percentage [S1] [S4] [S7]. **Chosen:** single-table continuation,
   with the two-table design noted as a first-order pricing variant.
10. **Rate-sheet volatility.** Every current-rate table carries a "can be superseded at any
    time" clause with a 10-day advance-filing commitment [S3] [S5] [S8], so the parameter set
    is versioned: **Jackson rate sheet dated April 27, 2026** [S3]. The historical tables
    show the de-risking cycle plainly — Flex GMWB bonus options were 5%/6%/7% for issues
    2019-06-24 → 2020-08-09, cut to 4%/5%/6% for 2020-08-10 → 2022-07-31, restored to
    5%/6%/7% from 2022-08-01; the GWB Adjustment fell from 200% through 170/180/190% by
    bonus option to 105% from 2021-03-01 [S1].

---

## Regulatory context

**NAIC Model #250 (Variable Annuity Model Regulation).** *Correction, per the research
file:* **#250 is the Variable Annuity Model Regulation, not the Annuity Disclosure Model
Regulation — that is #245** [REG-R43] [REG-R45], confirmed independently by AG 54, which
cites "NAIC Model 250, Variable Annuity Model Regulation" [REG-R44]. Model #250 governs
insurer qualification, separate accounts, filing, required provisions, nonforfeiture and
reports; its §7.B is the boundary rule — to the extent a VA provides benefits that do not
vary with separate-account performance before the annuity commencement date, those
provisions must satisfy Model #805 [REG-R43]. *Note on the appendix print, which is not a
substitute:* the AP&P Manual's Appendix A item for this subject, **A-250 (Variable
Annuities)**, has now been read in full and is **one page of three paragraphs** — the ¶1
definition of a variable annuity, a ¶2 requirement that each separate account hold assets at
least equal to the reserves and other contract liabilities of that account, and a ¶3
delegation of the reserve to Appendix A-820 [REG-R156]. It carries **none** of the
qualification, filing, required-provisions, nonforfeiture or reports material above, and its
own header names only the **Standard Valuation Law (#820)** and **SSAP No. 56** — it does not
name Model #250 anywhere [REG-R156]. Every Model #250 statement in this paragraph therefore
continues to rest on [REG-R43], not on the appendix.

**Model #805 and the nonforfeiture floor.** *Second correction:* Model #805 **expressly
excludes variable annuities**, so it does not reach the separate account at all [REG-R42];
it bites only on a VA's fixed account, via Model #250 §7.B [REG-R43]. Where it does bite,
its **indexed nonforfeiture rate is the lesser of 3% and the five-year Constant Maturity
Treasury rate (rounded to the nearest 1/20th of one percent) reduced by 125 basis points,
subject to a floor of 15 basis points (0.15%) — not the 1% floor often quoted**; the
minimum nonforfeiture amount accumulates net considerations of **87.5%** of gross, less
prior withdrawals, an annual contract charge of **$50**, premium tax paid and indebtedness
[REG-R42]. None of it is operative here: electing the Roll-up GMDB makes Fixed Account
Options unavailable [S1].

**VM-21 — the statutory reserve standard.** VM-21 covers variable deferred and immediate
annuities with or without GMDB/VAGLB and **constitutes CARVM** for contracts in scope
[R1] [REG-R35]. Aggregate reserve = Stochastic Reserve + additional standard projection
amount + any Alternative Methodology reserve, with the SR being **CTE70** of the scenario
reserves, each contributing the greatest present value of accumulated deficiency
[R1] [REG-R35]. The Alternative Methodology is available only for contracts with no
guaranteed benefits or **only** GMDBs — never a GLWB block [R1] — so this product is
unavoidably stochastic. Effective for valuation dates on or after January 1, 2020, with an
elective 36-month phase-in and a separate economic scenario generator phase-in of 36
months beginning January 1, 2026 [R1] [REG-R35]. *Third correction:* **AG 43 is not simply
superseded** — through reference in AG 43 the VM-21 requirements also reach contracts
issued before January 1, 2017, and the two populations may be aggregated [R1] [REG-R38].

**AG 33 and why it is not the reserve standard here.** AG 33 — "Determining CARVM Reserves
for Annuity Contracts With Elective Benefits" — has been read in full and applies "to all
annuity contracts subject to CARVM, where any elective benefits … are available to the
contract owner under the terms of the contract", with no product list and **no
separate-account exception**; its own examples of elective benefits are full surrenders,
partial withdrawals and full and partial annuitizations, which this contract has [REG-R151].
It is displaced by its own precedence clause — "the product specific actuarial guideline or
regulation will take precedence" — which is why AG 43 and VM-21 govern instead. **The
principle is sourced, the pairing is not:** AG 33 names **no other guideline anywhere in its
eight printed pages** and never mentions separate accounts, variable annuities or the
Valuation Manual, so the AG 43 pairing is this library's inference from the general clause,
**[std, derived]** [REG-R151]. The guideline's printed effective date is **December 31,
1998**, "affecting all contracts issued on or after January 1, 1981", with a grade-in that
reached 100% by December 31, 2000 and so has no live effect on any current valuation
[REG-R151]; the library elsewhere carries **December 31, 1995** under a different title from
IRS Rev. Rul. 2002-6, and because the extracted pages contain **no amendment history** the
reconciliation is **unresolved and neither date is presented as settled**. The mechanics AG 33
does supply impose a behavioral frame — elective incidence maximised over rather than
assumed — which is the opposite of VM-21's prudent-estimate approach, so assumptions must
never be carried between the two frames.

**VM-22 and VM-V — where the post-depletion stream lands.** VM-22 is the PBR framework for
**non-variable** annuities and does not cover VAs, but **fixed income streams from
guaranteed living benefits after account exhaustion** are named in its Reserving Categories
and in VM-V §1's scope [REG-R36] [REG-R37]. *Fourth correction:* in the January 1, 2026
Valuation Manual VM-22 is **entirely** the PBR framework, and maximum valuation interest
rates for income annuities live in **VM-V Section 1**, not VM-22 [REG-R36] [REG-R37].

**C-3 Phase II risk-based capital.** One projection, two outputs: VM-21 §§4.A–4.E and the
RBC requirements are **identical** apart from the elective federal income tax treatment
[REG-R35]. Per LR027, C-3 uses **CTE(98)** — the average of the 2% largest scenario
reserves — on the same process as the reserve, with TAR = pre-phase-in VM-21 reserve + the
C-3 amount; the C-3 amount is then divided by (1 − the enacted maximum federal corporate
income tax rate) and split into interest-rate-risk and market-risk portions [R3]. The 2020
revisions moved the stochastic measure to 25% of CTE 98 from CTE 90 [R4] — which is why the
older C-3 Phase II instructions package still prints the pre-reform **CTE 90** Total Asset
Requirement and a 35% tax rate [REG-R47]: cite it for structure, [R3] for the current level.
The reform's diagnosis — that fully hedging fair value *increased* capital requirements and
volatility — is in the Oliver Wyman QIS II reports [R2] [REG-R48].

**Federal securities law.** Registration is on Form N-4 [R6] [REG-R52], whose Part A order
(Item 2 Overview, Item 3 Key Information, Item 4 Fee Table, in numerical order at the front)
produces the structure every prospectus in the set follows, with Inline XBRL tagging of
specified items [R6] — first-hand from the retrieved form; the cross-product entry
[REG-R52] records a failed fetch and describes the form only through the adopting releases.
Rule 498A authorizes the Initial and Updating Summary Prospectuses and the Key Information
Table [R7] [REG-R50] [REG-R51]. FINRA Rule 2330 governs
recommended purchases, exchanges and **initial subaccount allocations** (not later
reallocations), requires principal review within seven business days and surveillance of
exchanges within the preceding 36 months — the proximate brake on 1035 exchange velocity
and therefore on replacement-driven surrender assumptions [R8] [REG-R54] [REG-R56].

**Federal tax.** IRC §72 supplies the exclusion ratio, the income-first (LIFO) rule for
pre-annuitization distributions, the 10% additional tax under §72(q), and the §72(s)
required-distribution-at-death rules that shape death benefit payout modeling
[R9] [REG-R55]. §817(h) diversification is a *product qualification* condition: under Treas.
Reg. §1.817-5 no more than 55% of the account's total assets may be in any one investment,
70% in any two, 80% in any three, 90% in any four, tested quarterly with a 30-day cure
window and a look-through to underlying RIC assets [R10] [REG-R15]. RMD timing under the
2024 final regulations is a *behavioral* input, not merely a tax one, because GLWB
activation clusters at the RMD age [REG-R57] [REG-R58] [REG-R64 — unverified](#uslib-reg-r64). Tax reserves
under §807 are the greater of net surrender value and 92.81% of the NAIC-prescribed method
(CARVM, i.e. VM-21), capped at statutory [REG-R16] [REG-R72 — unverified](#uslib-reg-r72).

**Disclosure, suitability, accounting and professional standards.** Model #245 largely
exempts registered products complying with SEC and FINRA rules under its §3.D, **but the
Buyer's Guide is still required in variable annuity sales** [REG-R45]; Model #275's
best-interest standard changes exchange and replacement behavior and therefore surrender
assumptions [REG-R46]. Under LDTI the GLWB and GMDB are the paradigm **market risk
benefits**, at fair value through earnings [REG-R34 — **[unverified]**: fasb.org returned
403, so ASU 2018-12 itself was never retrieved and its substance rests on secondary
summaries](#uslib-reg-r34) [REG-R71 for the MRB-vs-insurance-liability classification, which *was*
retrieved](#uslib-reg-r71) — a second consumer of the same cash flows on a risk-neutral basis.
*Fifth correction:* **there is no ASOP for principle-based reserves for annuities** —
ASOP No. 52 is scoped to VM-20 life products, so
any claim that it governs VM-21 is [unverified] and, on the retrieved ASB text, wrong
[R11] [R12] [REG-R31]. The applicable standards are ASOP Nos. 7 [REG-R27], 22 [REG-R29], 56
[REG-R32], 2 (non-guaranteed elements, expressly covering variable deferred annuities and
so governing the rider-charge reset) [REG-R26], 54 [REG-R70] and 10 [REG-R71]; the nearest
VM-21-specific guidance is the non-binding Academy practice note supplement [R4] [REG-R66].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-variable_annuity-r1
[R10]: #uslib-variable_annuity-r10
[R11]: #uslib-variable_annuity-r11
[R12]: #uslib-variable_annuity-r12
[R2]: #uslib-variable_annuity-r2
[R3]: #uslib-variable_annuity-r3
[R4]: #uslib-variable_annuity-r4
[R6]: #uslib-variable_annuity-r6
[R7]: #uslib-variable_annuity-r7
[R8]: #uslib-variable_annuity-r8
[R9]: #uslib-variable_annuity-r9
[REG-R15]: #uslib-reg-r15
[REG-R151]: #uslib-reg-r151
[REG-R156]: #uslib-reg-r156
[REG-R16]: #uslib-reg-r16
[REG-R26]: #uslib-reg-r26
[REG-R27]: #uslib-reg-r27
[REG-R29]: #uslib-reg-r29
[REG-R31]: #uslib-reg-r31
[REG-R32]: #uslib-reg-r32
[REG-R35]: #uslib-reg-r35
[REG-R36]: #uslib-reg-r36
[REG-R37]: #uslib-reg-r37
[REG-R38]: #uslib-reg-r38
[REG-R42]: #uslib-reg-r42
[REG-R43]: #uslib-reg-r43
[REG-R44]: #uslib-reg-r44
[REG-R45]: #uslib-reg-r45
[REG-R46]: #uslib-reg-r46
[REG-R47]: #uslib-reg-r47
[REG-R48]: #uslib-reg-r48
[REG-R50]: #uslib-reg-r50
[REG-R51]: #uslib-reg-r51
[REG-R52]: #uslib-reg-r52
[REG-R54]: #uslib-reg-r54
[REG-R55]: #uslib-reg-r55
[REG-R56]: #uslib-reg-r56
[REG-R57]: #uslib-reg-r57
[REG-R58]: #uslib-reg-r58
[REG-R66]: #uslib-reg-r66
[REG-R70]: #uslib-reg-r70
[REG-R71]: #uslib-reg-r71
[S1]: #uslib-variable_annuity-s1
[S2]: #uslib-variable_annuity-s2
[S3]: #uslib-variable_annuity-s3
[S4]: #uslib-variable_annuity-s4
[S5]: #uslib-variable_annuity-s5
[S6]: #uslib-variable_annuity-s6
[S7]: #uslib-variable_annuity-s7
[S8]: #uslib-variable_annuity-s8
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
