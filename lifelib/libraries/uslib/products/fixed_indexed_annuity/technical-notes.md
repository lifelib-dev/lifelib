# Technical Notes

**Status:** Draft, 2026-08-04 (all cited sources accessed 2026-08-04).

**Scope note.** A reference liability cash-flow projection model for the standardized composite
product defined in `product-spec.md` (same directory); not any single insurer's product. **[S#]**
/ **[R#]** tags refer to `_research/fixed-indexed-annuity.md`; **[REG-R#]** tags refer to
`references/regulatory-and-actuarial-references.md`, whose shared numbering now runs **R1–R157**
with most of the **R73–R149** block unused: R1–R34 originate in
`_research/regulatory-actuarial.md`, R35–R72 in
`_research/regulatory-actuarial-annuities.md`, and **R151–R157** are the seven AP&P Manual
appendix items read at first hand on 2026-08-06 — R151 AG 33, R152 AG 35, R153 A-820 with A-821 and
A-822, R154 A-830, R155 A-585, R156 A-250, R157 A-255. **[std]** marks standardizations
introduced for the reference implementation; [unverified] marks claims the research file could not
confirm. **An [unverified] flag leaves that state only when the primary text is read** — which is
what closed the AG 33 and AG 35 mechanics below [REG-R151] [REG-R152]; nothing is upgraded on
recollection, and every flag not closed that way still stands. **Parameter values are identical to
`product-spec.md`.**

**Inherited versus new.** The base contract is the fixed deferred annuity chassis in
`_research/fixed-deferred-annuity.md` and `products/fixed_deferred_annuity/` — the
surrender-benefit composition order and the Model #805 floor construction — whose *structure* is
**referenced, not restated**; the schedules, rates and recursions below are this composite's own
and are **not** that file's. In particular the account-value roll-forward here is index-credit
driven, and the lapse architecture below is **not** that file's renewal/shock-lapse architecture
(see "Policyholder behavior modeling": an in-force GLWB suppresses the shock lapse). `MGV` below
is the same Model #805 floor that file calls `MGSV` — one quantity, two source labels. Two
base-contract items are **restated rather than inherited**, because the FIA composite chooses
differently from the fixed-deferred composite: the **MVA** (ratio form `[(1+i₀)/(1+iₜ)]^(n/12) − 1` with the specimen
limit [S10], against that file's linear `(i₀ − iₜ) × T` with a symmetric surrender-charge cap) and
the **death benefit** (`max(AV, MGV)` [S1] [S2] [S5] [S10], against that file's full account value
floored at the cash surrender benefit). New here: the index crediting engine, the premium bonus
with vesting and clawback, and the GLWB rider (benefit base, rider charge, lifetime withdrawal,
excess-withdrawal adjustment, post-depletion phase).

**Difference from the indexed UL segment engine** (`products/indexed_ul/technical-notes.md`):
the FIA shares the vocabulary of segments, caps, participation rates, floors and credit bases, but
has **no cost of insurance, no net amount at risk and no death benefit corridor**, hence no
COI/NAAR/corridor circularity. There is no premium load, no per-unit charge and no face amount.
The ladder is a **single annual segment per indexed account**, not a monthly sweep ladder of up to
twelve concurrent segments. The rider is a **guaranteed lifetime withdrawal benefit** that
survives account-value exhaustion and pays for life, not a no-lapse guarantee on a death benefit.

---

## Model scope and conventions

- **Purpose.** Project gross liability cash flows (premium, guaranteed and excess withdrawals,
  surrender payments, death benefits, expenses, and the post-depletion guaranteed income stream)
  for a single-contract model point. Reserves are not computed.
- **Projection frequency: annual** **[std]**, with the contract anniversary as the single event
  date. Every mechanic in the composite is annual — annual point-to-point crediting [S2] [S4] [S10],
  the rider charge at the end of each contract year [S9], the annual benefit base update [S9], and
  the annual lifetime withdrawal. A monthly grid is needed only for excluded variants: monthly-sum
  crediting [S4] [R1], one carrier's monthly charge deduction [S1] [S2], daily interim values
  [S10] [S11], mid-year withdrawal crediting [S3] [S10] [S11].
- **Timing.** All transactions occur **at** the anniversary and are processed as the last events
  of the contract year ending there **[std]**. The contract-year surrender charge percentage,
  vesting percentage and free withdrawal amount therefore all apply to a withdrawal at anniversary
  `t`, and the index credit for year `t` is computed on the balance carried from anniversary `t−1`
  — reproducing the rule that "withdrawals are not credited with index interest in the year
  they are taken" [S1].
- **Age basis: age nearest birthday (ANB)** **[std]** — the statutory annuity tables are published
  on that basis (VM-M / Model #821 print the 2012 IAM Period Table for female and male, age
  nearest birthday) [REG-R59], and the AP&P print of the same table at **A-821 Appendices I–IV**
  independently carries the "Age Nearest Birthday" heading for both sexes [REG-R153]. The **[std]**
  stands: it marks the model's choice of a single age basis, not the tables' basis. Attained age at
  anniversary `t` = `issue_age + t`.
- **Model points.** Single-contract, projected on an expected (probability-weighted) basis;
  survivorship and persistency factors multiply per-contract cash flows. No aggregation logic
  specified.
- **Decrement order:** death before surrender **[std]**. **Rounding:** full precision internally,
  cents on reported cash flows **[std]**. **State basis:** one composite state basis **[std]**.

---

## Model point attributes

| Attribute | Type | Example (anchor cell) |
|---|---|---|
| `issue_age` | int (ANB) | 62 **[std]** |
| `sex` | enum {M, F} | M |
| `tax_status` | enum {NQ, Q} | NQ **[std]** |
| `single_premium` | currency | 100,000 **[std]** |
| `bonus_rate` | rate | 0.07 [S5] |
| `alloc_fixed` / `alloc_indexed` | fraction (sums to 1) | 0.00 / 1.00 **[std]** |
| `glwb_elected` / `glwb_basis` | bool / enum {single, joint} | true / single **[std]** |
| `joint_age` | int (ANB), joint only | n/a |
| `income_start_age` | int (ANB), ≥ 50 [S2] [S3] [S9] | 70 **[std]** |
| `utilization_intensity` | fraction of `LW` actually withdrawn | 1.00 **[std]** |
| `sc_schedule` | vector, contract years 1–11+ | 9.1, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0 % [S5] |
| `vesting_vector` | vector, contract years 1–11+ | 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100 % [S5] |
| `mva_index_at_issue` `i₀` | rate | 0.0300 **[std]** |
| `av_initial`, `bb_initial`, `mgv_initial` | currency (in-force cells) | 107,000 / 100,000 / 87,500 |

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `F(t)`, `A(t)` | Fixed / indexed account balance at anniversary `t` after all processing | annually |
| `AV(t)` | Account value = `F(t) + A(t)` | annually |
| `MGV(t)` | Guaranteed minimum (nonforfeiture) value | annually |
| `BB(t)` | GLWB benefit base — notional, no cash value [S1] [S9] | annually |
| `RB(t)` | Rollup base for the guaranteed simple rollup [S2] [S9] | annually / on withdrawal |
| `LW(t)` | Locked annual lifetime withdrawal amount (0 before exercise) | at exercise; ratchet; excess withdrawals |
| `phase(t)` | `ACCUM` / `INCOME` / `DEPLETED` / `TERMINATED` | annually |
| `v(t)`, `sc(t)` | Vested bonus percentage; surrender charge percentage for year `t` [S5] | schedule lookup |
| `FW(t)` | Free withdrawal amount = `0.10 × AV(t−1)` | annually |
| `Wcum(t)` | Cumulative gross withdrawals | on withdrawal |
| `l(t)` | In-force probability at end of year `t`; `l(0) = 1` | annual decrements |
| `rider_in_force(t)` | Boolean; false once the rider terminates [S9] | on events |
| `depletion_cause(t)` | Flag set when an excess withdrawal, surrender charge or MVA touches the account value | in step 5 |

---

## Assumption inputs

Class (a) is contractual and cannot be changed by the insurer; class (b) is the insurer-declared
current scale, a non-guaranteed element under ASOP No. 2 [R6] [REG-R26]; class (c) is the modeler's
view of experience. They must not be mixed in the code.

### (a) Contractual / guaranteed elements

| Input | Value | Basis |
|---|---|---|
| Index credit floor `f` | 0% | [S1] [S4] [S10] [R1] |
| Guaranteed minimum annual cap `c_min` | 0.25% | [S4]; selection **[std]** |
| Guaranteed minimum fixed rate `i_F,min` | 1.00% | [S10]; selection **[std]** |
| Surrender charge schedule `sc(t)` | 9.1, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0% | [S5] |
| Surrender charge base | gross withdrawal − free withdrawal amount | [S10] |
| Free withdrawal | 10% of the prior-anniversary account value, no carry-forward | [S1] [S3] [S5] [S6] [S9] [S10]; combination **[std]** |
| Bonus vesting vector `v(t)` | 0, 10, …, 100% | [S5] |
| Bonus clawback | `(1 − A) × [B/(1+B)] × C` | [S10] |
| MGV base / rate `i_nf` | 87.5% of premium excluding the bonus / 1.00% inside the 0.15%–3% corridor | [S10] [R2]; level **[std]** |
| Guaranteed simple rollup `g(t)` | 5.00% (yrs 1–10), 2.00% (yrs 11–20), 0% after | [S2] |
| Rollup base convention | flat dollar increment on premium adjusted for withdrawals | [S2] [S9] |
| Stacking factor `m` | 150% of dollar credits, floored at 0 | [S8] [S9] |
| Growth period `T_g` | min(first lifetime withdrawal, contract year 20) | [S1] [S2] |
| Lifetime withdrawal percentages `π` | age-band table (`product-spec.md`); joint = single − 0.50% | [S3] [S1]; 80+ band **[std]** |
| Minimum age for lifetime withdrawals | 50 | [S2] [S3] [S9] |
| Rider charge maximum | 1.50%, changeable only after contract year 15 | [S9] |
| Post-depletion guarantee | income continues if depletion is caused by guaranteed withdrawals or rider charges; terminates if caused by excess withdrawals, surrender charges or MVA | [S1] [S9] |
| Death benefit ≥ cash surrender benefit | statutory constraint | [R2 §6](#uslib-fixed_indexed_annuity-r2) |

### (b) Insurer-declared current elements (snapshot; revisable NGEs [R6] [REG-R26])

| Input | Value | Basis |
|---|---|---|
| Declared annual cap `c` | 5.25% | [S2] (rates effective 07/01/2022); selection **[std]** |
| Declared fixed account rate `i_F` | 2.30% | [S2] |
| Rider charge rate `φ` | 0.95% of the benefit base | [S9] |
| Allocation / strategy charge | 0% | current 0%, max 2.50% [S3] [S4]; choice **[std]** |
| MVA reference index level `iₜ` | scenario input | generic **[std]**; Barclay's US Credit Index in the linear-form products [S6] [S7] |

**Caveat.** Every value here is a non-guaranteed element captured only as of the date on its
source document, and one carrier's current rate sheets could not be fetched [S-f1]. Insurers review
caps, participation rates, spreads and triggers frequently (e.g. monthly), targeting the priced
product **option budget** and considering investment yields, option costs, volatility, premium
volumes, competition and profit objectives [R1]. Reference re-declaration rule **[std]**: set
`c(t)` so the one-year call-spread cost equals the option budget `b_opt(t) = earned_rate(t) −
required_spread`, subject to `c(t) ≥ c_min` [R1] [R6]. The base projection holds the snapshot scale
level.

### (c) Behavioral and experience assumptions

| Input | Recommended public basis | Tags |
|---|---|---|
| Annuitant mortality | 2012 IAM Basic / 2012 IAR generational with Projection Scale G2: `q_x^{2012+n} = q_x^{2012} × (1 − G2_x)^n`, rounding applied from the 2012 period rate each time, never by compounding an already-rounded rate | [REG-R59] [REG-R60] |
| Mortality A/E deviation | 2020–2024 Individual Payout Annuity Mortality Experience Study (23 parent groups, >80% of industry sales, 3.1m contract-years, 143,190 deaths), presented against the 2012 IAM Table | [REG-R61]; A/E factor 100% **[std]** |
| Deferred-period mortality | materially under-evidenced — only a 2011–2015 deferred annuity mortality study and a 2006 analysis are public; qualified contracts show lower A/E than non-qualified, and FIAs *without* GLWBs showed an anomalous increasing A/E by account-value band | [R1] [REG-R65] |
| Base surrender | shape: low early, rising through the surrender charge period, spiking in the shock year, then falling back but staying above pre-shock levels | [R1]; table **[std]** |
| Shock lapse | in the year the surrender charge expires, **10% with a GLWB rider versus 33% without** | [R8]; corroborated [unverified] at [REG-R62] |
| GLWB withdrawal incidence | 37% of GLWB contracts took withdrawals in 2019–2020 versus fewer than 30% without | [R8] |
| GLWB withdrawal efficiency | the majority of users withdraw **95%–105% of the maximum**; contracts in that band have the lowest surrender rates; activated GLWBs lapse least | [R1] |
| GLWB activation timing | clusters at the required-minimum-distribution age; withdrawal rates rise with attained age, highest for qualified contracts at 70+ | [R1]; [REG-R64] [unverified]; assumption framework [REG-R67] |
| Additional premium | rare: 2.5% of contracts in years 2–10, 1.9% with a GLWB, 3.3% without | [R8] |
| Maintenance expense | $80 per contract per year, inflating 2.5% p.a. | **[std]** |
| Acquisition expense | 6.0% of single premium at issue | **[std]** |
| Premium tax | 0.0% (composite state basis) | **[std]** |

The Academy's guaranteed-living-benefit resource guide is the checklist to test a utilization
assumption against — moneyness, age and RMD timing, qualified versus non-qualified, distribution
channel, systematic withdrawal plan enrolment, rider type — and is explicitly non-binding, "a list
of considerations and resources" [REG-R67]. The detailed FIA surrender and utilization tables are
behind paid subscriptions [R9] [REG-R62], so every class (c) number is an order-of-magnitude
anchor, not a calibration target.

---

## Cash flow components and recursions

### Notation (defined once)

| Symbol | Meaning |
|---|---|
| `t` | contract year index, `t = 1, 2, …`, and the anniversary ending it; `x` = issue age (ANB); attained age at `t` is `x + t` |
| `P`, `b`, `v(t)` | single premium; bonus rate (0.07 [S5]); vested percentage in year `t` [S5] |
| `F(t)`, `A(t)`, `AV(t)` | fixed / indexed / total account value after all processing at `t` |
| `I(t)`, `R(t)` | index level; `R(t) = I(t)/I(t−1) − 1` (price index, dividends excluded [S6] [R1]) |
| `c`, `c_min`, `f` | declared cap (0.0525 [S2]); guaranteed minimum cap (0.0025 [S4]); floor (0) |
| `p`, `s`, `d`, `c_m` | participation rate; spread / index margin; trigger rate; monthly cap (variants) |
| `cr(t)`, `IC(t)`, `FI(t)` | credit rate; index credit amount; fixed account interest |
| `i_F`, `i_F,min` | declared / guaranteed minimum fixed rate (0.0230 [S2] / 0.0100 [S10]) |
| `φ`, `Φ(t)` | rider charge rate (0.0095 [S9]); rider charge amount |
| `BB(t)`, `RB(t)`, `g(t)`, `m` | benefit base; rollup base; rollup rate [S2]; stacking factor (1.50 [S8] [S9]) |
| `LW(t)`, `π(a, basis)` | annual lifetime withdrawal amount; payout percentage at attained age `a` [S3] |
| `G(t)`, `E(t)`, `ρ(t)` | gross withdrawal; excess above `LW`; proportional reduction factor |
| `FW(t)`, `X(t)` | free withdrawal amount `= 0.10 × AV(t−1)`; chargeable amount |
| `SC(t)`, `CB(t)`, `MVA(t)` | surrender charge; non-vested bonus clawback; MVA (signed) |
| `MGV(t)`, `i_nf` | guaranteed minimum value; nonforfeiture accumulation rate (0.0100 **[std]**) |
| `i₀`, `iₜ`, `n` | MVA index at issue, at withdrawal; months remaining in the MVA period |
| `q(t)`, `w(t)`, `l(t)` | annual mortality rate; surrender rate; in-force probability |

**Dimensional check.** `cr` is dimensionless, so `IC = base × cr` is currency; `Φ = φ × BB` is
currency — a rate applied to a *notional* amount (the benefit base has no cash value [S1] [S9])
producing a real deduction from the account value; `LW = π × BB` is currency per year; `ρ` is
dimensionless. All account-value terms are currency.

### Initialisation (`t = 0`)

    A(0) = alloc_indexed × P × (1 + b)     F(0) = alloc_fixed × P × (1 + b)      [S5]
    AV(0) = P × (1 + b) = 107,000
    BB(0) = P = 100,000        RB(0) = P = 100,000                               [S9]
    MGV(0) = 0.875 × P = 87,500            (bonus excluded)                      [S10] [R2]
    LW(0) = 0     phase(0) = ACCUM     rider_in_force(0) = true

### Processing order at anniversary `t` **[std]**

Fixed for the reference model, following one specimen's stated sequence — the rider charge is
deducted **after** index credits are added [S9] — with the benefit-base update after the charge,
so the charge is always assessed on the *opening* base as `Φ(t) = φ × BB(t−1)`.

1. Index credit and fixed interest. 2. Rider charge. 3. Benefit base: rollup, stack, step-up.
4. Lifetime / excess withdrawal. 5. Charges on the excess and proportional reduction of the
   guarantee. 6. Guaranteed minimum value roll. 7. Phase transition (incl. depletion test).
8. Decrements. Steps 1–3 are skipped in `DEPLETED`; steps 1–7 in `TERMINATED`.

**Step 1 — index credit.**

    cr(t) = max( f , min( c , R(t) ) )                              [S2] [S4] [S10] [R1]
    IC(t) = A(t−1) × cr(t)      FI(t) = F(t−1) × i_F
    AV⁽¹⁾(t) = AV(t−1) + IC(t) + FI(t)

Variants, all floored at `f`: `max(f, p × R)` [S4] [S10] [R1]; `max(f, min(c, p × R))` — worked at
[R1] as `min(80% × 10%, 6%) = 6%`; `max(f, p × R − s)` [S8] [R1]; `d × 1{R ≥ 0}` [R1]; `max(f,
Σ_{k=1..12} min(R_k, c_m))` [S4] [R1].

*Segment bookkeeping.* One annual segment per indexed account, created at anniversary `t−1` with
balance `A(t−1)`, maturing at `t`; the credit locks at maturity and cannot be lost to later
declines [S1]. The credit base is the segment's opening balance less withdrawals from that account
during the segment — the "Interest Credit Basis" [S6] — which collapses to `A(t−1)` here
because all transactions occur at anniversaries **[std]**. Reallocation is permitted at each
anniversary [S1] [S5]; dividends are excluded from `R(t)` [S6] [R1]. **The floor applies to the
credit, not to the account value** — charges do reduce the account value below its prior balance
[S7]. On a monthly grid, mid-segment conventions are: no credit in the year of withdrawal [S1];
prorated for the portion of the year the money stayed in the allocation [S3]; `G × PAR/(1 + PAR)`,
`PAR` being a *Protected Account Return* and not a participation rate [S10]; full
earnings-to-date on the free amount and pro rata above [S11].

**Step 2 — rider charge.**

    Φ(t) = φ × BB(t−1)          AV⁽²⁾(t) = AV⁽¹⁾(t) − Φ(t)                        [S9]

Deducted from the fixed account first, then proportionately across indexed accounts [S9]. `φ` is
fixed for 15 contract years, then resettable but never above 1.50% [S9]. Variants: charge on the
contract value [S5]; no explicit charge, the guarantee funded through lower caps, participation
rates or higher index margins [S3] [S8]. The composite does **not** deduct the charge from `MGV`;
one carrier deducts from both the accumulated value and the minimum guaranteed contract value
except in certain states [S1] [S2], and another deducts its allocation charge from the guaranteed
minimum value in most states [S3] [S4] — implement as a switch **[std]**.

**Step 3 — benefit base.**

    rollup(t) = g(t) × RB(t−1)                    if t ≤ T_g, else 0        [S2] [S9]
    stack(t)  = m × max( 0 , IC(t) + FI(t) )      if t ≤ T_g, else 0        [S8] [S9]
    BB⁽³⁾(t)  = BB(t−1) + rollup(t) + stack(t)
    BB⁽⁴⁾(t)  = max( BB⁽³⁾(t) , AV⁽²⁾(t) )              annual step-up **[std]**

`T_g` = the earlier of the first lifetime withdrawal and contract year 20 [S1] [S2]. The rollup is
a **flat dollar increment**, not simple interest on the grown base — one carrier computes it on
premium less withdrawals [S2], another on the adjusted *initial* base [S9], and the latter's
15-year table confirms a constant $3,000 per year on a $100,000 adjusted initial base [S9]. The
stack is on realised dollar credits net of any strategy fee, floored at zero [S9].

*The step-up is a [std] generalisation.* No retrieved document describes an automatic annual
ratchet during deferral; documented instead are an at-exercise step-up to the contract value [S5],
an annual benefit amount computed on the greater of base and account value at exercise [S9], and a
never-decreasing income amount once withdrawals begin [S3]. Testing once at exercise reproduces
[S5]/[S9]; testing annually is the superset. **Under the blended baseline the step-up rarely
binds** — an extra dollar of credit adds $1 to the account value and $1.50 to the base — so it
binds mainly in the pure-rollup variant (see the worked example). *Rarely, not never:* the
account-value bonus starts `AV(0) = 107,000` above `BB(0) = 100,000`, so a first contract year with
a zero index credit gives `AV⁽²⁾(1) = 106,050` against `BB⁽³⁾(1) = 105,000` and the step-up binds.
Test it at every anniversary rather than assuming the stack dominates.

Three growth mechanisms must be expressible; the baseline is (c):

| | Mechanism | Configuration | Observed at |
|---|---|---|---|
| (a) | Guaranteed deferral rollup only | `m = 0`; `g` simple on `RB`, or compound on `BB` | [S1] [S2] simple, [S5] compound (Options 1, 3, 5), [S9] simple |
| (b) | Index-credit stacking only, no guaranteed rollup | `g = 0`; `m` = 1.50 or 2.50 | [S3] [S4] (150% or 250%, by annual owner election) |
| (c) | **Blended — baseline [std]** | `g` = 5.00%/2.00%, `m` = 1.50 | [S2] [S8] [S9] |

In design (b) the account value is deliberately starved: one carrier's 250% election credits
**250% of index interest to the benefit base but only 50% to the account value**, and the contract
defaults to the 150%/100% election once lifetime withdrawals begin [S3]. Model this as an
account-value interest factor `κ ∈ {0.50, 1.00}` applied to `IC(t)` in step 1, with the
benefit-base factor `m` [S3] [S4]. In the benefit-base-only bonus designs the bonus is added to
`BB(0)` and **never touches the account value or the surrender benefit** [S3] [S4] [S8].

**Step 4 — lifetime and excess withdrawal.** Exercise is permitted from attained age 50
[S2] [S3] [S9]:

    LW(t) = π( x + t , basis ) × BB⁽⁴⁾(t)                                    [S3] [S9]

`π` is locked at first exercise **[std]**; joint = single − 0.50% on the younger life [S1] [S3].
After exercise the ratchet still applies — `LW(t) = max( LW(t−1) , π × BB⁽⁴⁾(t) )` — so income
never decreases [S3]. For a gross withdrawal `G(t)`:

    guaranteed portion = min( G(t) , LW(t) )      E(t) = max( 0 , G(t) − LW(t) )
    AV⁽⁵⁾(t) = AV⁽²⁾(t) − G(t)

Withdrawals up to `LW` carry **no surrender charge, no MVA and no bonus clawback even if `LW`
exceeds the free withdrawal amount** [S9]; unused `LW` does not carry forward [S9] (one carrier
accumulates it without interest as a "cumulative withdrawal amount" [S3]).

**Step 5 — charges on the excess and proportional reduction.**

    X(t)   = max( 0 , G(t) − FW(t) )                      pre-exercise
    X(t)   = max( 0 , E(t) − remaining free withdrawal )  post-exercise **[std]**
    SC(t)  = X(t) × sc(t)                                                    [S5] [S10]
    CB(t)  = ( 1 − v(t) ) × [ b / (1 + b) ] × X(t)                           [S10]
    MVA(t) = X(t) × { [ (1 + i₀) / (1 + iₜ) ]^(n/12) − 1 }                   [S10]

*Whether the guaranteed withdrawal consumes the free withdrawal amount is a* **[std]** *choice.*
[S9] says only that withdrawals up to the annual benefit amount carry no charge "even if greater
than the Free Withdrawal Amount"; it does not say whether they exhaust it. The convention above —
`remaining free withdrawal = max(0, FW(t) − LW(t))` — is the insurer-favourable reading and is what
the worked example uses; the alternative leaves the full `FW(t)` available against the excess.

`MVA` is signed — negative when the reference yield has risen [S10] — and is limited to `|MVA| ≤
max(0, G(t) − SC(t) − CB(t) − MGV(t))`, so a negative MVA combined with charges never reduces the
surrender value below the guaranteed minimum value and the maximum positive MVA cannot exceed the
maximum negative MVA [S10]. `MVA = 0` outside the MVA period and on the death benefit
[S5] [S6] [S7] [S10].

    pre-exercise    ρ(t) = G(t) / AV⁽²⁾(t)                          [S1] [S3] [S5] [S9]
    post-exercise   ρ(t) = E(t) / ( AV⁽²⁾(t) − LW(t) )                       [S9]
    BB(t) = BB⁽⁴⁾(t) × (1 − ρ)     LW(t) ← LW(t) × (1 − ρ)     RB(t) = RB(t−1) × (1 − ρ)

with `ρ = 0` when `E(t) = 0`, and `ρ = 1` (base to zero, rider terminates [S9]) if the
post-exercise denominator is non-positive. The post-exercise denominator is the account value
**after** the guaranteed payment has notionally been taken — verbatim at [S9]: account value
$100,000, base $200,000, annual benefit amount $10,000, withdrawal $28,000 → denominator $90,000,
excess $18,000, reduction 20%, base → $160,000, benefit amount → $8,000. An RMD above `LW` is not
an excess withdrawal after exercise; before exercise it reduces the base pro rata [S1] [S9]. The
alternative rollup-base convention — the dollar subtraction, "Premium minus Withdrawals" [S2]
— is `RB(t) = max(0, RB(t−1) − G(t))`.

**Step 6 — guaranteed minimum value.**

    MGV(t) = max( 0 , MGV(t−1) × (1 + i_nf) − G(t) )                         [R2] [S10]

with `MGV(0) = 0.875 × P` excluding the bonus [S10]. Model #805 §4A also permits an accumulated
**$50 annual contract charge** and accumulated premium tax to be deducted [R2]; both are set to
zero **[std]** because no retrieved product declares an actual annual policy fee, making the
modeled floor slightly conservative. Contractually `i_nf = min(3%, max(0.15%, CMT₅ − 125 bp − Δ))`
where `Δ ≤ 100 bp` is the FIA additional reduction available while the contract provides
substantive participation in an equity indexed benefit [R2]; `Δ` requires an annualized option
cost of the **guaranteed** index features **≥ 25 bp** and then equals `min(100 bp, annualized
option cost)`, certified annually [R3]. Whether the 15 bp floor of §4B(3) survives the §4C
reduction is not stated in the retrieved text [unverified]; the contract language "the interest
rates will range between 0.15% and 3%" suggests it does [S10]. **Correction: the §4B floor is 15
basis points, not 1%** [R2]; the composite's 1.00% is a **[std]** pick inside the corridor, not the
statutory floor.

**Step 7 — phase transitions and the post-depletion liability.**

    ACCUM    → INCOME      first lifetime withdrawal, attained age ≥ 50      [S2] [S3] [S9]
    INCOME   → DEPLETED    AV ≤ 0 attributable only to guaranteed withdrawals
                           and rider charges                                 [S1] [S9]
    INCOME   → TERMINATED  AV ≤ 0 attributable to an excess withdrawal, a
                           surrender charge or an MVA                        [S1] [S5] [S9]
    any      → TERMINATED  death, full surrender, or BB reaching zero        [S9]
    DEPLETED → TERMINATED  death of the covered person only                  [S1] [S9]

**`DEPLETED` is where the economic value of the guarantee sits.** In it the insurer pays `LW`
annually from its own funds for the rest of the covered life [S1] [S3] [S9] [R1]; there is no account
value, so **no rider charge is deducted** [S9] and no index credit is computed; the surrender
value and death benefit are zero; **lapse is impossible**, so every surrender and dynamic-lapse
formula must be switched off and `l(t) = l(t−1) × (1 − q(t))`; under the joint option the payment
continues to the survivor [S1] [S9]. The attribution test is not cosmetic — an account value run to
zero by an excess withdrawal loses the guarantee entirely [S1] [S5] [S9]. Implement it as
`depletion_cause`, set in step 5 whenever `E(t) > 0`, `SC(t) > 0` or `MVA(t) < 0`, and evaluate it
before the depletion test. One carrier's confinement and terminal illness waivers are themselves
**excess withdrawals that terminate the income rider** [S1] — a trap if waivers are added.

**Step 8 — decrements and cash flow outputs.** `l(t) = l(t−1) × (1 − q(t)) × (1 − w(t))`, with
`w(t) = 0` in `DEPLETED`.

| Cash flow | Formula | Weight |
|---|---|---|
| Premium income (+) | `P` at `t = 0` | 1 |
| Guaranteed withdrawal (−) | `min(G(t), LW(t))` | `l(t−1)` |
| Excess withdrawal (−) | `E(t) − SC(t) − CB(t) + MVA(t)` | `l(t−1)` |
| Surrender (−) | `CSV(t) = max( AV(t) − SC(t) − CB(t) + MVA(t) , MGV(t) )` | `l(t−1) × (1 − q(t)) × w(t)` |
| Death benefit (−) | `max( AV(t) , MGV(t) )`, full bonus vesting, no charges | `l(t−1) × q(t)` |
| Post-depletion income (−) | `LW` while `phase = DEPLETED` | `l(t−1)` |
| Acquisition expense (−) | 6.0% of `P` at `t = 0` **[std]** | 1 |
| Maintenance expense (−) | `80 × 1.025^(t−1)` **[std]** | `l(t−1)` |

`SC`, `CB` and `Φ(t)` are *internal* transfers within the account value, not separate cash flows —
they reduce what is ultimately payable. Reporting them as fee income while also projecting the
account value net of them double-counts.

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** reference constructions; the qualitative and order-of-magnitude
evidence is cited, and the tables that would calibrate them are behind paid subscriptions
[R9] [REG-R62].

**Base surrender table [std]** — shape from [R1]: low early, rising through the surrender charge
period, spiking at expiry, then falling back but staying above pre-shock levels.

| Contract year | 1–3 | 4–6 | 7–9 | 10 | 11 (shock) | 12+ |
|---|---|---|---|---|---|---|
| `w_base` | 2% | 3% | 4% | 5% | see below | 6% |

**Shock lapse with rider suppression [std]** — the single most important behavioral fact in the
product. In the year the surrender charge expires the surrender rate was **10% with a GLWB rider
versus 33% without** [R8]:

    w_shock = 0.33   no GLWB rider
    w_shock = 0.10   GLWB in force but not activated
    w_shock = 0.05   GLWB activated (phase = INCOME)

The third row extrapolates **[std]** from the qualitative finding that "contracts with GLWBs lapse
less than those without" and "activated GLWBs lapse least," with the lowest rates where the
withdrawal is 95%–105% of the maximum [R1]. Applying a plain fixed-deferred shock lapse — reported
at roughly 52%–56% for fixed-rate deferred annuities [REG-R63](#uslib-reg-r63) [unverified] — to an FIA with an
in-force rider will materially understate the tail this product is sold for.

**Rider moneyness multiplier [std].** Surrender is further suppressed when the guarantee is in the
money:

    M_money(t) = clamp( 1 − 0.6 × max(0, BB(t)/AV(t) − 1) , 0.2 , 1.0 )
    w(t) = min( 0.35 , w_base(t) × M_shock(t) × M_money(t) ),   w(t) = 0 in DEPLETED

Rational surrender destroys a guarantee worth `BB − AV` in benefit-base terms; the observed
direction is documented [R1] [R8], the functional form is not.

**GLWB activation (utilization timing) [std].** Activation clusters at the
required-minimum-distribution age [R1] [REG-R64](#uslib-reg-r64) [unverified], which makes the RMD regulations a
behavioral input, not merely a tax one [REG-R57] [REG-R58]:

    h(a) = 0.00  for a < 60      h(a) = 0.05  for 60 ≤ a < rmd_age
    h(a) = 0.40  at a = rmd_age  h(a) = 0.15  for a > rmd_age

with `rmd_age = 73` **[std]** as a configurable model parameter — the statutory age is set by IRC
§401(a)(9) as amended by SECURE 2.0 and finalized in T.D. 10001 [REG-R57] [REG-R58], is not printed
in the retrieved research material, and must not be hard-coded. The deterministic base run
activates at the model point's `income_start_age` instead.

**Withdrawal intensity given activation [std].** The majority of users withdraw **95%–105% of the
maximum** [R1], and 37% of GLWB contracts took withdrawals in 2019–2020 versus fewer than 30%
without a rider [R8]. Base assumption: withdraw exactly `LW`, with sensitivities at 0.95 and 1.05.
The 1.05 case **is an excess withdrawal** and triggers the pro-rata reduction in step 5 — a 5%
overdraw permanently reduces the guarantee, which is why efficiency and excess-withdrawal
assumptions cannot be set independently.

**Excess withdrawal incidence [std]:** zero in the base run; any non-zero assumption must route
through step 5 and the `INCOME → TERMINATED` attribution test [S1] [S5] [S9]. **Additional premium
[std]:** none — deposits occur on 2.5% of contracts in years 2–10 and only 1.9% with a GLWB [R8].
**Annuitization [std]:** not modeled; where offered, payments are based on the greater of account
value and cash surrender value — **not** the benefit base [S3] [S10], so annuitization is generally
dominated by the GLWB [S3].

---

## Worked example

Anchor cell: Male 62 ANB, single life, `P = $100,000`, `b = 7%`, GLWB elected at issue, first
lifetime withdrawal at anniversary 8 (attained age 70). Parameters as specified: `c = 5.25%` [S2],
`f = 0%` [S1], `φ = 0.95%` [S9], `g = 5.00%` for years 1–10 [S2], `m = 1.50` [S8] [S9], `π(70,
single) = 5.20%` [S3], `sc(8) = 3%` [S5], `v(8) = 70%` [S5], `i_nf = 1.00%` **[std]**. Opening
state at anniversary 7 (illustrative balances, broadly consistent with a seven-year deferral at
these parameters) **[std]**: `AV(7) = 128,000.00` (100% indexed), `BB(7) = 180,000.00`, `RB(7) =
100,000.00`, `MGV(7) = 93,811.84` (= 87,500 × 1.01⁷), `Wcum(7) = 0`.

| # | Item | Formula | Value |
|---|---|---|---|
| 1 | Index return, year 8 | `5,450 / 5,000 − 1` | 9.0000% |
| 2 | Credit rate | `max(0, min(5.25%, 9.00%))` | 5.2500% |
| 3 | Index credit `IC(8)` | `128,000.00 × 0.0525` | 6,720.00 |
| 4 | Account value after credit | `128,000.00 + 6,720.00` | 134,720.00 |
| 5 | Rider charge `Φ(8)` | `0.0095 × 180,000.00` | 1,710.00 |
| 6 | Account value after charge `AV⁽²⁾` | `134,720.00 − 1,710.00` | 133,010.00 |
| 7 | Guaranteed rollup | `0.0500 × 100,000.00` | 5,000.00 |
| 8 | Stacking credit | `1.50 × 6,720.00` | 10,080.00 |
| 9 | Benefit base before step-up | `180,000.00 + 5,000.00 + 10,080.00` | 195,080.00 |
| 10 | Step-up test | `max(195,080.00, 133,010.00)` | 195,080.00 (does not bind) |
| 11 | Lifetime withdrawal `LW(8)` | `0.0520 × 195,080.00` | 10,144.16 |
| 12 | Free withdrawal amount `FW(8)` | `0.10 × 128,000.00` | 12,800.00 |
| 13 | Excess `E(8)` | `max(0, 10,144.16 − 10,144.16)` | 0.00 → no SC, MVA or clawback [S9] |
| 14 | Account value `AV(8)` | `133,010.00 − 10,144.16` | 122,865.84 |
| 15 | Guaranteed minimum value `MGV(8)` | `93,811.84 × 1.01 − 10,144.16` | 84,605.80 |
| 16 | Closing benefit base `BB(8)` | unchanged by a guaranteed withdrawal [S9] | 195,080.00 |

**Surrender test at the same anniversary.** A full surrender of `G = AV(8) = 122,865.84` with
`12,800.00 − 10,144.16 = 2,655.84` of free amount remaining gives `X = 120,210.00`; `SC = 3% ×
120,210.00 = 3,606.30` [S5] [S10]; clawback `= 0.30 × (0.07/1.07) × 120,210.00 = 2,359.26` [S10];
with `i₀ = 3.00%`, `iₜ = 3.50%` and `n = 24` months remaining, `MVA = 120,210.00 × [(1.03/1.035)²
− 1] = 120,210.00 × (−0.00963850) = −1,158.64` [S10], inside the limit
`max(0, 122,865.84 − 5,965.56 − 84,605.80) = 32,294.48` [S10]. Net proceeds
`= 122,865.84 − 3,606.30 − 2,359.26 − 1,158.64 = 115,741.64`, and
`CSV = max(115,741.64, 84,605.80) = 115,741.64`.

**Where the step-up binds.** Under variant (a) — 3% simple rollup on `RB`, no stacking [S9] — the
same cell carries `BB(7) = 121,000.00`, so `Φ(8) = 1,149.50`, `AV⁽²⁾ = 133,570.50` and `BB⁽³⁾ =
124,000.00`. The step-up then binds: `BB(8) = 133,570.50` and `LW(8) = 0.0520 × 133,570.50 =
6,945.67`. General result: the step-up matters when realised index credits outrun the guaranteed
rollup, and is dominated whenever a stacking factor above 1.0 is present.

**Where the liability lands.** Holding index credits at zero from anniversary 8, the account value
drains by `LW + Φ = 10,144.16 + 0.0095 × 195,080.00 = 11,997.42` a year and is exhausted during
contract year 19, at attained age about 81. From that point the insurer pays $10,144.16 a year for
the rest of the contract holder's life, with no account value, no surrender value, no death
benefit and no possibility of lapse [S1] [S3] [S9] [R1]. That stream is the guarantee.

---

## Valuation and reserve pointers

This library projects **gross liability cash flows**; reserve layers consume them and are cited,
not reproduced.

- **Formulaic statutory (CARVM).** **AG 33** — printed title *"Determining CARVM Reserves for
  Annuity Contracts With Elective Benefits"* — constructs and values the integrated benefit streams
  for annuity contracts with elective benefits; **AG 35** specifies how the index feature enters
  that greatest-present-value calculation, through **four** computational methods with quarterly
  certification and change-notification requirements, "Type 1" and "Type 2" being **the guideline's
  own printed section headings, not industry shorthand** [REG-R151] [REG-R152]. **Both texts have now
  been read in full** from the AP&P Manual Appendix C print — a **free download**, not the paid
  publication recorded earlier [REG-R33] — so their mechanics are no longer [unverified]; titles and
  continued incorporation remain independently confirmed by the VM-C index [REG-R41]. **AG 33's
  effective date, recorded on both sides because the two do not reconcile:** its own *Effective Date*
  block reads "This guideline shall be effective on **December 31, 1998**, affecting all contracts
  issued on or after January 1, 1981", with a grade-in of 33⅓ / 66⅔ / 100% that completed on
  December 31, 2000 and therefore has **no live effect on any current valuation** [REG-R151]; the
  library elsewhere carries **December 31, 1995** for a differently-titled instrument from IRS
  Rev. Rul. 2002-6. The 1981 issue-date reach is common to both, the extracted pages carry **no
  amendment history**, and **the reconciliation is unresolved** — that the guideline was later
  revised is an inference, not something either source states. **AG 35 prints no date at all**; its
  only temporal language is "regardless of the date of issue" [REG-R152]. Two documents in this
  chain remain unavailable and are named rather than glossed: **AG IX-B**, which AG 35 points at
  three times as an alternative source of the valuation interest rate for an indexed contract and
  which this library holds only as a VM-C index entry [REG-R41] [REG-R152], and the **NAIC
  Interest-Indexed Annuity Contracts Model Regulation**, Sections 5 and 6 of which AG 35 supersedes
  and which is not in this library at all [REG-R152].
- **Principle-based statutory.** **VM-22**, effective for valuation dates on or after January 1,
  2026, with a three-year elective transition and mandatory prospective application three years
  after the effective date [REG-R36]; the Academy paper states elective 1/1/2026 and required
  1/1/2029 [R1]; the VM-22 (A) Subgroup handles post-launch monitoring [R7]. An FIA sits in the
  **Accumulation** reserving category, which expressly includes fixed income streams from
  guaranteed living benefits after account exhaustion — the `DEPLETED` phase of this model — and
  **GLB utilization risk** is named among the risks to be reflected; the stochastic reserve is
  CTE70 [REG-R36]. Maximum valuation interest rates for formulaic income-annuity reserves are in
  **VM-V Section 1**, not VM-22 [REG-R36] [REG-R37]. Enabling statute: Model #820 [REG-R1]; parent
  document [REG-R3].
- **Asset adequacy.** ASOP No. 22, meaning the same projection must serve CARVM and cash flow
  testing [REG-R29] [REG-R27]. **AG 35 does not itself impose the requirement** — it directs that
  reserves be tested "to the extent required by law, regulation, or regulatory requirements"
  [REG-R152]. The operative NAIC requirement is **VM-30**, with SVL §6.B, codified as **A-822 ¶3**,
  behind it, and any shortfall becomes an additional reserve
  [REG-R100] [REG-R1] [REG-R153].
- **Nonforfeiture floor.** Model #805 §4 and Model #806 §7 as implemented in step 6
  [R2] [R3] [REG-R42].
- **Tax reserve.** IRC §807: the greater of net surrender value and 92.81% of the NAIC-prescribed
  method — CARVM for annuities — capped at the statutory reserve [REG-R16].
- **GAAP (LDTI).** The **index feature is an embedded derivative**, fair-valued on expected
  current and future index credits (current index period closed-form Black-Scholes); the **GLWB is
  a market risk benefit** at fair value with an adjustment for explicit fees; remaining cash flows
  form the host contract discounted at a host accrual rate set so the total liability at issue
  equals the premium; DAC, DSI and URL are the intangibles [R1] [REG-R34] [REG-R71].
- **Standards for the modeling work.** ASOP No. 56 (modeling) [REG-R32]; ASOP No. 54 (pricing, if
  a profit-metric mode is added) [REG-R70]; ASOP No. 2 for any NGE re-declaration logic
  [R6] [REG-R26].

---

## Key sensitivities and model risks

Dominant assumptions, in rough order of impact on the value of the guarantee:

1. **GLWB activation timing and intensity.** The liability is a function of when the holder starts
   and whether they take 95%, 100% or 105% of the maximum [R1] [R8] [REG-R64] [REG-R67]; activation
   five years earlier compounds directly into the depletion date.
2. **Surrender, specifically the rider-suppressed shock lapse.** 10% versus 33% in the shock year
   [R8] governs how much of the block survives to reach `DEPLETED` at all. Applying a
   fixed-deferred shock lapse to a rider-in-force FIA is the most consequential error available
   here.
3. **Longevity in the `DEPLETED` phase.** The payment is a life annuity written at a payout
   percentage set decades earlier: use the 2012 IAM/IAR family with Scale G2 [REG-R59] [REG-R60]
   and test against the 2020–2024 payout experience [REG-R61]; deferred-period annuitant
   mortality, which governs who reaches the income phase, is served publicly by only two dated
   studies [REG-R65].
4. **Cap re-declaration and the option budget.** The declared cap drives the account value, the
   stacking credit and hence the benefit base; it is an NGE reset against the option budget
   [R1] [R6] [REG-R26] [REG-R68]. Holding the snapshot cap constant for 40 years is a strong implicit
   assumption.
5. **Benefit base growth form.** Blended versus pure rollup versus pure stacking changes both the
   level of the guarantee and its correlation with index performance; pure stacking shifts the
   deferral guarantee from insurer to market and is materially cheaper to hedge [S3] [S4].

Known pitfalls:

- **The behavioral assumptions above must not be reused in a CARVM valuation.** Every dynamic lapse,
  activation, utilization and excess-withdrawal formula in "Policyholder behavior modeling" is an
  *experience* assumption. AG 33 states that for elective benefits "incidence rates should not be
  based on tables reflecting past company experience, industry experience or other expectations" —
  the elective assumption is not an assumption at all but a **decision variable maximised over**,
  with all rates between 0% and 100% theoretically in scope and the greatest present value typically
  occurring at 0% or 100% [REG-R151]. Wiring the projection's behavior module into the reserve run is
  a silent compliance error. The non-elective side is the opposite case: incidence comes from the
  SVL-prescribed tables where one exists, otherwise from company or industry experience **with
  margins for conservatism** (unquantified), and the SVL-prescribed **annuity mortality** table
  discounts every payment in **every** integrated benefit stream for survivorship — the elective
  surrender and withdrawal streams included, so a cash-value stream is **not** valued on a
  mortality-free basis [REG-R151].
- **"Efficient policyholder selection" is not AG 33's language and should not be attributed to it.**
  The phrase appears nowhere in the guideline; the actual construction is the prohibition, the trial
  sets, and the direction to **"consider, not necessarily test"** all potential integrated benefit
  streams [REG-R151].
- **The 0% floor is on the index credit, not the account value.** Rider charges and strategy fees
  can exceed interest credited, "which would result in loss of premium" [S7]. Flooring the account
  value silently removes the charge drag that produces depletion.
- **The clawback factor is `b/(1+b)`, not `b`** [S10] — the account value already contains the
  bonus; using `b` over-recovers by `(1+b)`.
- **The "simple rollup" is a flat dollar increment**, on premium less withdrawals [S2] or on the
  adjusted *initial* base [S9] — never simple interest on the current grown base. Compounding it
  inflates the base and every downstream charge and payment.
- **Attribution at depletion.** Survival of the income stream depends on the *cause* [S1] [S5] [S9];
  a model testing only `AV ≤ 0` will either give the guarantee away after an excess withdrawal or
  destroy it after a legitimate one.
- **No lapse in `DEPLETED`.** Leaving the surrender decrement on silently truncates the most
  expensive part of the liability.
- **Rider charge base and ordering.** The charge is on the **benefit base**, not the account value
  [S1] [S2] [S9], and is taken **after** index credits [S9]. In the worked example the benefit base
  closes at 1.59× the account value at anniversary 8 (195,080.00 against 122,865.84), so charging
  on the account value understates the deduction by a growing margin.
- **Excess-withdrawal denominator.** Post-exercise it is the account value net of the guaranteed
  amount [S9]; pre-exercise it is the gross account value [S1] [S3] [S5] [S9] — the two differ by
  exactly `LW`.
- **MVA sign and collar.** Negative when yields rise [S10]; applies only above the free amount,
  only inside the MVA period, never to the death benefit, never below the nonforfeiture minimum
  [S1] [S5] [S6] [S7] [S10]. The linear form `(i₀ − iₜ) × T` [S6] [S7] is unbounded and must be
  collared separately; the ratio form used here is not.
- **Monthly-sum floor convention is ambiguous.** The Academy's worked example applies a 0% monthly
  floor as well as a 1% monthly cap [R1], which is unusual — most monthly-sum designs cap the
  upside monthly but let negative months subtract in full, and one rate sheet declares a
  1.70% monthly cap with a 0.50% guaranteed minimum without stating the floor [S4]. Verify against
  a contract before implementing that variant.
- **Interim values and index costs.** The baseline has none; adding one requires a different
  structure — a Daily Account Value / Protected Account Value with a 90% protection level
  [S10] or a daily-tracked strategy value [S11], both daily marks of the embedded option
  rather than interpolations. Proprietary volatility-controlled indices separately deduct embedded
  servicing, transaction and financing costs (0.50% p.a. at BNPP MAD 5 and AiPEX [S2]; 2 bp
  change-in-notional plus 12 bp annualized replication at S&P 500 Dynamic Intraday TCA [S10]),
  which reduce `R(t)` *before* the cap or participation rate.
- **Stale and state-varying parameters.** Declared rates are dated 07/01/2022 [S2] and the access
  date [S4]; one carrier's rate sheets [S-f1], another's official host [S-f3] and a third's current
  brochure [S-f4] could not be fetched. State variation in surrender charges, vesting,
  MVA availability and waiver terms is extensive and deliberately not modeled [S2] [S3] [S6] [S7].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-fixed_indexed_annuity-r1
[R2]: #uslib-fixed_indexed_annuity-r2
[R3]: #uslib-fixed_indexed_annuity-r3
[R6]: #uslib-fixed_indexed_annuity-r6
[R7]: #uslib-fixed_indexed_annuity-r7
[R8]: #uslib-fixed_indexed_annuity-r8
[R9]: #uslib-fixed_indexed_annuity-r9
[REG-R1]: #uslib-reg-r1
[REG-R100]: #uslib-reg-r100
[REG-R151]: #uslib-reg-r151
[REG-R152]: #uslib-reg-r152
[REG-R153]: #uslib-reg-r153
[REG-R16]: #uslib-reg-r16
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
[REG-R57]: #uslib-reg-r57
[REG-R58]: #uslib-reg-r58
[REG-R59]: #uslib-reg-r59
[REG-R60]: #uslib-reg-r60
[REG-R61]: #uslib-reg-r61
[REG-R62]: #uslib-reg-r62
[REG-R64]: #uslib-reg-r64
[REG-R65]: #uslib-reg-r65
[REG-R67]: #uslib-reg-r67
[REG-R68]: #uslib-reg-r68
[REG-R70]: #uslib-reg-r70
[REG-R71]: #uslib-reg-r71
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
