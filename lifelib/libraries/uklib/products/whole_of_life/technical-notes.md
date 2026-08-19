# Technical Notes

**Status:** Draft, 2026-08-03 (all cited sources accessed 2026-08-03; see `sources.md`).

**Scope note.** These notes specify a reference liability cash flow projection model for the
standardized composite product defined in `product-spec.md` (same directory). This is not any
single insurer's product. [S#]/[R#] tags refer to the source list in
`_research/whole-of-life.md` via `sources.md`; [REG-R#] tags refer to the cross-product
reference library `references/regulatory-and-actuarial-references.md` (its own
R-numbering; research provenance in `_research/regulatory-actuarial.md`). **[std]** marks
standardizations introduced for the reference implementation; [unverified] marks claims not
confirmed against a retrieved document. Parameter values are identical to those in
`product-spec.md`. Two cells share one engine:

- **RefWOL-UW** (underwritten guaranteed; the chassis-carrier pattern [S10]) — anchor: male,
  entry age 40, non-smoker, £150,000 sum assured, level cover, £101.25/month **[std]**.
- **RefWOL-O50** (over-50s guaranteed acceptance; the direct-sold pattern [S1] [S4]) — anchor:
  entry age 70 **[std]**, non-smoker, £30/month, £5,000 cash sum ([R2] stylised pair).

Neither cell carries any account value, unit fund, or surrender value [S1] [S4] [S7] [S9] [S10]:
both are **pure-decrement protection models** — the projection is premiums in, death benefits
and expenses out, weighted by survivorship. This is the deliberate contrast with the US
cash-value whole life chassis (no CSV schedule, no dividends, no loans).

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows (premium income, death
  outgo, expenses; no surrender outgo exists) for single-policy model points of the two
  cells, on a monthly grid. Reserves, discounting, risk margin and capital are pointed to,
  not computed (see Valuation and reserve pointers).
- **Projection frequency.** Monthly **[std]**. Premiums are monthly Direct Debit in the O50
  cell [S1] [S4] [S7] [S9] and monthly or annual in the UW cell [S10]; monthly is the natural grid.
- **Timing conventions [std].** Premiums (and premium-linked commission) at the beginning of
  the policy month (BOM); deaths during the month resolved at end of month (EOM) against the
  BOM in-force; lapses at EOM after deaths (death-before-lapse order). Escalation steps
  (increasing cover, RPI variants) apply at policy anniversaries [S4] [S10]. Annual-grid
  implementations must preserve the month-13 moratorium boundary.
- **Age basis.** Age last birthday (ALB) **[std]**. Rationale: the UW chassis defines entry
  age x as "before the (x+1)th birthday" [S10], which is ALB; the O50 documents price on "age at
  outset" without stating a basis [S1]. All age lookups in this model are ALB.
- **Currency / units.** GBP. Sum assured in £; premiums in £/month; mortality and lapse
  rates dimensionless per annum, converted to monthly as q_m = 1 − (1 − q)^(1/12) **[std]**.
- **Model points.** Single-policy expected-value projection: survivorship probabilities
  multiply per-policy cash flows. No aggregation logic here. Aggregation caps across
  same-insurer policies (£10,000/£18,000, £100/month [S1] [S4] [S9]) are immaterial to a
  per-policy model.
- **Claims settlement.** Immediate at EOM of the death month **[std]**; contractual claims
  interest (BoE base − 0.5%, floor 0.5% p.a., between death and payment [S1] [S9]) is
  excluded as a settlement-lag refinement, not a liability driver.
- **Rounding.** Full precision carried; cash flows reported to pence **[std]**.

---

## Model point attributes

| Attribute | Type | Example (O50 anchor) | Example (UW anchor) |
|---|---|---|---|
| `cell` | enum {O50, UW} | O50 | UW |
| `entry_age` | int (ALB) | 70 | 40 |
| `sex` | enum {M, F} | F **[std]** (pick for the anchor cell; attribute carried for basis lookup — O50 pricing itself does not rate by sex in the fetched documents, which state age and smoker status as the rate factors [S1] [S4]) | M |
| `smoker` | enum {NS, S} | NS | NS (the chassis 3-state definition [S10] collapsed to 2 **[std]**) |
| `sum_assured` | currency (£) | 5,000 | 150,000 |
| `monthly_premium` | currency (£/month) | 30.00 | 101.25 **[std]** |
| `escalation` | enum {level, fixed_5pct, rpi} | level | level (fixed_5pct variant) |
| `cessation_months` | int (∞ for UW) | 240 (anniversary on/after 90th birthday **[std]**) | none — premiums payable for life [S10] |
| `moratorium_months` | int | 12 [S1] [S4] [S7] [S9] | 0 (suicide-only clause instead [S10]) |
| `variant_adb_2x` | bool (accidental multiplier, one plan [S7]) | false | n/a |
| `variant_paid_up` | bool (pro-rata paid-up value, one plan [S9]) | false | n/a |
| `variant_rpi_increasing` | bool (RPI indexation, one plan [S4]) | false | n/a |
| `issue_date` | date | month 1 | month 1 |

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `l(t)` | In-force probability at end of month t; l(0) = 1 | monthly (deaths, lapses) |
| `CumPrem(t)` | Cumulative premiums paid to end of month t (year-1 refund base; crossover tracking) | monthly |
| `N_paid(t)` | Count of monthly payments made (pro-rata paid-up numerator [S9]) | monthly |
| `SA(t)` | Current sum assured / cash sum (escalating variants) | anniversaries |
| `P(t)` | Current monthly premium (escalating variants; 0 after cessation) | anniversaries / cessation |
| `paid_up` | Pro-rata paid-up state: policy premium-free with reduced payout PU [S9] | on qualifying lapse |
| `PU` | Paid-up payout = SA x N_paid / N_expected (pro-rata paid-up variant) [S9] | on paid-up conversion |
| `in_moratorium(t)` | Indicator t <= 12 (O50) | monthly |
| `attained_age(t)` | entry_age + floor((t−1)/12) (ALB) | monthly |

---

## Assumption inputs

Three classes are distinguished explicitly.

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Premium level at issue | Fixed at outset by age and smoker status (O50 [S1] [S4]) / full underwriting (UW [S10] [S11]); guaranteed never to increase [S1] [S4] [S7] [S9] [S10] | anchors: £30/month for £5,000 at 70 [R2]; £101.25/month for £150,000 at 40 **[std]** |
| O50 moratorium | 12 months; non-accidental death → return of premiums paid (no interest stated); accidental death → full cash sum from day 1 | [S1] [S4] [S7] [S9] |
| O50 premium cessation | Anniversary on/after 90th birthday; cover continues | [S4] [S5] [S9]; pick **[std]** |
| UW terminal illness | Sum assured accelerated on 12-month prognosis; pays once, policy ends | [S10] [S12] |
| UW suicide clause | Suicide/intentional self-inflicted injury within 12 months of start (or increase) → refund of premiums for that cover | [S10] [S11] |
| UW escalation (variant) | SA +5%/year, premium +10%/year (2% premium per 1% cover) | [S10]; 5% pick **[std]** |
| O50 RPI variant (one plan) | Cash sum +RPI (floor 0%, cap 10%); premium +RPI x 1.5 (cap 15%); freeze on first declined increase; cash-sum indexation continues post-90 | [S4] |
| Pro-rata paid-up value (one plan's variant) | If N_paid >= N_expected/2 at premium stop: paid-up payout = SA x N_paid/N_expected; else cancellation with nothing | [S9] |
| Arrears | 60 days to make good; death in window → claim reduced by unpaid amounts; then lapse with no value | [S4] [S9]; pick **[std]** |
| Surrender value | None at any time, either cell | [S1] [S4] [S5] [S7] [S9] [S10] |

### (b) Insurer-discretionary current elements

**This class is nearly empty — the defining feature of both modern cells.** Premiums are
guaranteed [S1] [S4] [S7] [S9] [S10]; there are no bonus rates, no reviewable premiums, no
unit-linked charges, no asset shares and no MVRs in either cell (those mechanisms belong to
with-profits and unit-linked business, out of scope here). The discretionary layer reduces
to:

- **New-business rate tables.** Insurers do not publish full premium rate tables (research
  file gap); only quote anchors exist (£20/month at 50 NS → £5,694 [S2]; £25/month NS →
  £7,643/£6,046/£3,701/£1,893 at 50/60/70/80 [S6]) plus the FCA per-£1,000 averages (£71.73
  O50, £8.10 underwritten) [R2]. The model takes premium as a model-point input; any shipped
  rate table is a **[std]** snapshot calibrated to these anchors.
- **Claims interest rate.** Contractual formula, BoE-base-linked (base − 0.5%, floor 0.5%)
  [S1] [S9]; excluded from the base model **[std]** (conventions).
- **Legacy variation only:** the unit-linked reviewable design's review basis (mortality
  charge scale, review outcomes) is insurer-discretionary [S15]; it is documented as a
  closed-book variation, not modeled.

### (c) Behavioral / experience assumptions (modeler's view)

CMI access is honestly restricted: current tables and the Projections Model are limited to
Authorised Users/Subscribers; older publications are free — so a reference basis must be a
**[std]** proxy shaped like the named tables, and cannot redistribute current qx values
[REG-R22] [R7].

| Input | Recommended public basis | Basis tags |
|---|---|---|
| UW mortality | Assured-lives shape: CMI "00" series permanent assurances AMC00/AMS00/AMN00, AFC00/AFS00/AFN00 (publicly downloadable; the latest published assured-lives whole of life base tables) x A/E factor 100% **[std]**; AM92/AF92 as the teaching-table alternative shape | [R6] [R7] [REG-R24]; factor **[std]** |
| O50 mortality | Population-level: ONS national life tables qx (single year of age, sex; freely downloadable under OGL) x anti-selection loading 120%, level across durations **[std]** | [REG-R32]; loading **[std]** (see below) |
| Mortality improvement | None in base **[std]**; sensitivity: "CMI_20xx with long-term rate p% [std]" is the market-standard expression, but the model is subscriber-restricted — a flat 1% p.a. improvement is the [std] sensitivity proxy | [REG-R30] [REG-R22] |
| O50 accidental-death share of year-1 deaths | 3% **[std]** — accidental deaths are a small minority at 70+; no public split was found (research gap) | **[std]** |
| UW suicide share of year-1 deaths | 1% **[std]** — refund instead of sum assured; immaterial, carried for completeness | **[std]** |
| Terminal illness acceleration (UW) | Model TI claims as deaths accelerated by 6 months on average; base model ignores the acceleration (pays at death) **[std]** | timing **[std]**; benefit [S10] |
| Lapse | [std] tables below; no public UK WoL lapse study was retrieved (research gap); the FCA documents the lapse-supported dependence qualitatively | [R2]; tables **[std]** |
| Expenses | O50: acquisition £150/policy + commission 25% of year-1 premiums **[std]**; maintenance £30/policy/year inflating 3% p.a. **[std]**. UW: acquisition £300/policy + initial commission **[std]**; maintenance £50/policy/year inflating 3% **[std]**. Commission existence per one plan's disclosure (intermediary "paid by commission as a percentage of total annual premium" [S1]); all levels **[std]** | [S1]; levels **[std]** |

**Why the O50 basis is population-plus-loading, not assured lives.** Guaranteed acceptance
removes underwriting, so the pool cannot be better than population and self-selects worse:
the CMI is analysing *non-underwritten* whole of life experience separately from underwritten
— direct recognition of the anti-selection distinction [R7] — and the FCA's price
differential (£71.73 vs £8.10 per £1,000) reflects guaranteed-acceptance anti-selection,
older entry ages and shorter durations [R2]. No insurer discloses its guaranteed-acceptance
pricing basis (expected — proprietary; research file gap), so the 120% loading on ONS
population rates is a **[std]** placeholder to be calibrated; population mortality is itself
heavier than insured experience [REG-R32], so the loading is deliberately modest. The UW cell
uses an assured-lives shape ("00" series [R6]) because full underwriting restores select
experience.

Reference base lapse tables **[std]** (annual rates; shapes are drafting constructions —
no public product-specific study; replace with experience):

| Policy year | 1 | 2 | 3–5 | 6+ | after premium cessation |
|---|---|---|---|---|---|
| O50 `w_base` | 8% | 6% | 4% | 4% | 0% (no premiums due — no lapse) |
| UW `w_base` | 6% | 5% | 3% | 2% | n/a (premiums for life) |

---

## Cash flow components and recursions

### Notation (defined once, used throughout; shared with product-spec.md)

| Symbol | Meaning |
|---|---|
| t | policy month, t = 1, 2, ...; y = policy year = floor((t−1)/12) + 1 |
| a(t) | attained age (ALB) = entry_age + floor((t−1)/12) |
| P(t) | monthly premium due at BOM of month t (0 after cessation / in paid-up state) |
| SA(t) | sum assured / cash sum in month t (constant unless escalating variant) |
| T_cess | months from start to premium cessation (O50: to anniversary on/after 90th birthday; anchor 240); ∞ for UW |
| CumPrem(t) | Σ_{s<=t} P(s) |
| q(y) | annual mortality rate for policy year y (basis per cell, class (c)) |
| q_m(y) | monthly mortality = 1 − (1 − q(y))^(1/12) **[std]** |
| w(y), w_m(y) | annual / monthly lapse rates, w_m = 1 − (1 − w)^(1/12) **[std]** |
| δ_acc | accidental share of year-1 deaths (O50), 0.03 **[std]** |
| δ_su | suicide share of year-1 deaths (UW), 0.01 **[std]** |
| l(t) | in-force probability at end of month t; l(0) = 1 |
| DB_na(t), DB_ac(t) | death benefit for non-accidental / accidental death in month t (O50) |
| k_adb | accidental multiplier after year 1: 1 (base) or 2 (one plan's variant [S7]) |
| E[·] | expectation over decrements (survivorship weighting) |

Dimensional check: premiums and benefits are £; q_m, w_m, δ are dimensionless; every expected
cash flow below is £ per month per policy issued.

### Monthly processing order (both cells) **[std]**

At month t while in force and not paid-up:

1. BOM: premium P(t) received if t <= T_cess (O50) or always (UW); commission/premium
   expense deducted as an expense flow, not from any fund (there is no fund).
2. BOM: maintenance expense for the month.
3. Anniversary (t ≡ 1 mod 12, t > 12): apply escalation to SA and P (variants only)
   [S4] [S10].
4. EOM: deaths at rate q_m(y) applied to l(t−1); benefit per the rules below.
5. EOM: lapses at rate w_m(y) applied to survivors of step 4; death-before-lapse **[std]**.
   In the pro-rata paid-up variant a "lapse" with N_paid >= N_expected/2 converts to paid-up
   (state change, no cash flow) instead of termination [S9].
6. Update l(t) = l(t−1) x (1 − q_m(y)) x (1 − w_m(y)).

Paid-up policies (the pro-rata paid-up variant) and post-cessation O50 policies skip steps 1
and 5 (no premiums due, so no lapse decrement **[std]**) and continue steps 2, 4, 6 with
w_m = 0. Step 3 is also skipped, with one exception: in the RPI-increasing variant the cash
sum continues to index at anniversaries after premiums cease at 90 [S4] (the premium step,
being zero, stops).

### RefWOL-O50 recursions

Premiums (level base design):

    P(t) = P x 1{t <= T_cess},        CumPrem(t) = P x min(t, T_cess)

Death benefit split during the 12-month moratorium [S1] [S4] [S7] [S9]:

    DB_na(t) = CumPrem(t)   if t <= 12          (return of premiums paid, no interest)
             = SA           if t >  12
    DB_ac(t) = SA           if t <= 12          (full cash sum from day 1)
             = k_adb x SA   if t >  12          (k_adb = 2: one plan's variant [S7])

Expected cash flows in month t (per policy issued):

    E[premium](t) = l(t−1) x P(t)
    E[death outgo](t) = l(t−1) x q_m(y) x [ (1−δ_acc) x DB_na(t) + δ_acc x DB_ac(t) ]   if t <= 12
                      = l(t−1) x q_m(y) x [ (1−δ_acc) + δ_acc x k_adb ] x SA           if t >  12
    E[expenses](t) = l(t−1) x [maintenance(t)] + commission/acquisition at their BOM timing

(with k_adb = 1 the post-moratorium death outgo is simply l(t−1) q_m SA). Lapse generates
**no cash flow**: there is no surrender value [S1] [S4] [S5] [S7] [S9] — its entire effect is
through l(t). That is the arithmetic meaning of "lapse-supported": every lapse extinguishes
a paid-up-style liability for nothing, and the FCA records that without the continuing-payer
cross-subsidy "insurers would need to rely on lapses to remain profitable" [R2].

Crossover (tipping point): cumulative premiums first exceed the cash sum at

    t* = floor(SA / P) + 1    (months, level premiums, t* <= T_cess)

Anchor: floor(5000/30) + 1 = 167 months = 13 years 11 months, reproducing the FCA's stylised
example exactly [R2]. Total premiums payable are capped at P x T_cess (anchor: £7,200 vs
£5,000 cash sum). A crossover exists iff SA < P x T_cess; the FCA notes entrants at 79–80 are
most exposed and that the majority of policies still pay out more than premiums paid [R2].

Pro-rata paid-up variant [S9]: on premium stop at month t with N_paid(t) >= N_expected/2
(N_expected = T_cess):

    PU = SA x N_paid(t) / N_expected        (worked example: 180/240 x £3,500 = £2,625 [S9])

thereafter DB_na = DB_ac = PU (the moratorium is long past), premiums 0, lapse 0 **[std]**.

RPI-increasing variant (one plan [S4]), r_y = RPI inflation for year y:

    SA(y+1) = SA(y) x (1 + min(max(r_y, 0), 0.10))
    P(y+1)  = P(y)  x (1 + min(max(1.5 x r_y, 0), 0.15))       while y < cessation
    SA continues to index after premiums cease at 90; first declined increase freezes both
    (premium step floored at 0 **[std]** — [S4] defines an increase only, no decrease).

### RefWOL-UW recursions

Premiums guaranteed level (base): P(t) = P for all t; no cessation age [S10]. Escalating
variant (5% **[std]**), applied at anniversaries [S10]:

    SA(y) = SA_0 x 1.05^(y−1),      P(y) = P_0 x 1.10^(y−1)

Death/terminal-illness benefit: the sum assured is paid once on death or earlier terminal
illness diagnosis (12-month prognosis), and the policy ends [S10] [S12]. The base model pays
SA(y) at death (TI acceleration ignored **[std]**; a TI module would move a fraction of
claims ~6 months earlier **[std]** with no change in amount). Suicide within 12 months
refunds premiums [S10]:

    E[death outgo](t) = l(t−1) x q_m(y) x [ (1−δ_su) x SA(y) + δ_su x CumPrem(t) ]   if t <= 12
                      = l(t−1) x q_m(y) x SA(y)                                      if t >  12

Lapse (2 months' unpaid premiums, no reinstatement [S10]) again generates no cash flow — no
cash-in value at any time [S10] — and only reduces l(t). Milestone-benefit exercises and
requested increases are out of scope (they would step SA and P; anti-selection flagged in
model risks) [S10] [S12].

### Cash flow outputs (per policy issued, month t)

| Cash flow | Formula | Sign |
|---|---|---|
| Premium income | l(t−1) x P(t) | + |
| Death outgo | per cell formulas above | − |
| Acquisition expense + initial commission | at t = 1 (and commission % x premiums in year 1, O50) **[std]** | − |
| Maintenance expense | l(t−1) x (annual maintenance / 12) x (1.03)^(y−1) **[std]** | − |
| Surrender outgo | **none — identically zero in both cells** [S1] [S4] [S7] [S9] [S10] | — |
| Claims interest | excluded **[std]** (contractual BoE−0.5% floor 0.5% between death and payment [S1] [S9]) | — |

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** reference constructions; no public UK whole of life
lapse/persistency study was retrieved (research gap), so shapes are drafting assumptions
with the qualitative anchors cited.

- **Base lapse [std].** Duration-declining tables above; converted monthly. Rationale for the
  declining shape: sunk premiums with zero surrender value and (O50) the approaching
  paid-out-in-full status discourage late lapse.
- **Moratorium-completion effect (O50) [std].** No extra lapse spike at month 13: the
  moratorium gives no incentive to lapse (lapsing returns nothing at any time). The year-1
  rate is set highest instead (affordability/buyer's-remorse attrition; the 30-day
  cooling-off with full refund [S1] [S4] is modeled as never-issued business, out of scope).
- **Crossover-aware lapse (O50) [std].** Sensitivity module, off in base:
  `w(t) = w_base(y) x (1 + β x 1{CumPrem(t) > SA})`, β = 0.5. Rationale: Consumer Duty
  communications must enable informed choice about the over-payment risk [R2], which could
  raise post-tipping-point lapses; the FCA has seen no evidence that a significant proportion
  of customers reach the premium caps [R2]. β is a pure stress dial.
- **Pro-rata paid-up selection (one plan's variant) [std].** Once N_paid >= N_expected/2, all
  would-be lapses convert to paid-up (rational: forfeiture is strictly dominated; mechanics
  per [S9]); before the halfway point, lapse means total loss, so the base w applies. This
  converts lapse profit into a retained pro-rata liability — the variant exists precisely to
  remove the forfeiture cliff, and materially weakens lapse support (sensitivity mandatory).
- **Premium reduction options [std].** One-off reductions (three of the O50 plans
  [S1] [S4] [S9]) are not modeled; they are economically a partial lapse with proportionate
  SA reduction.
- **Escalation opt-out (UW variant) [std].** Increasing-cover holders decline an increase
  with probability 10% per anniversary; three declines remove the option [S10]; base model
  assumes full take-up.
- **Payment holidays (one plan [S9])** are ignored **[std]** (≤ 12 months' premiums deferred or
  netted; second-order).

---

## Worked example

RefWOL-O50 anchor cell: entry age 70 (ALB), non-smoker, P = £30/month, SA = £5,000, T_cess =
240 months (anniversary on/after 90th birthday **[std]**), base design (k_adb = 1, no
pro-rata paid-up value). Illustrative walk-through basis **[std]** (placeholder, not attributable to any
table): q(y) = 0.024 x 1.10^(y−1) — i.e. a 0.020 population-style rate at 70 x the 120%
anti-selection loading, with 10% p.a. age progression; lapse 8%/6%/4%/4% (years 1/2/3–5/6+),
0 after cessation; δ_acc = 3%. Monthly rates: q_m(1) = 1 − (1−0.024)^(1/12) = 0.0020223;
w_m(1) = 1 − (1−0.08)^(1/12) = 0.0069244. Expenses omitted from the table for clarity.
`E[death outgo](t)` = l(t−1) x q_m x (0.97 x DB_na + 0.03 x DB_ac) for t <= 12, and
l(t−1) x q_m x 5,000 thereafter. All £, full precision carried, displayed rounded.

| t | y | CumPrem | DB non-acc | DB acc | l(t−1) | E[premium] | E[death outgo] |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 30.00 | 30.00 | 5,000 | 1.00000 | 30.00 | 0.36 |
| 6 | 1 | 180.00 | 180.00 | 5,000 | 0.95613 | 28.68 | 0.63 |
| 12 | 1 | 360.00 | 360.00 | 5,000 | 0.90601 | 27.18 | 0.91 |
| 13 | 2 | 390.00 | 5,000.00 | 5,000 | 0.89792 | 26.94 | 10.00 |
| 24 | 2 | 720.00 | 5,000.00 | 5,000 | 0.82785 | 24.84 | 9.22 |
| 60 | 5 | 1,800.00 | 5,000.00 | 5,000 | 0.66359 | 19.91 | 9.88 |
| 120 | 10 | 3,600.00 | 5,000.00 | 5,000 | 0.42564 | 12.77 | 10.31 |
| 166 | 14 | 4,980.00 | 5,000.00 | 5,000 | 0.27420 | 8.23 | 9.85 |
| 167 | 14 | 5,010.00 | 5,000.00 | 5,000 | 0.27131 | 8.14 | 9.74 |
| 240 | 20 | 7,200.00 | 5,000.00 | 5,000 | 0.09992 | 3.00 | 6.57 |
| 241 | 21 | 7,200.00 | 5,000.00 | 5,000 | 0.09828 | 0.00 | 7.16 |

Trace, month 1: E[death] = 1.0 x 0.0020223 x (0.97 x 30 + 0.03 x 5,000) = 0.0020223 x 179.10
= £0.36 — the year-1 death outgo is dominated by the small accidental tail paying the full
cash sum, not the premium refund. Trace, month 13: the moratorium ends and the full £5,000
becomes payable for any death: E[death] = 0.89792 x 0.0022271 x 5,000 = £10.00 (q(2) = 0.0264
→ q_m = 0.0022271) — a ~11x jump in expected death outgo at the month-12/13 boundary, the
signature discontinuity of this product. Month 167 is the crossover: CumPrem = £5,010 first
exceeds the £5,000 cash sum (13 years 11 months, reproducing [R2]). Month 241: premiums have
ceased (E[premium] = 0) but death outgo continues — and rises, because lapses stop **[std]**
and mortality steps up at the year-21 anniversary; the post-cessation period is pure outgo,
funded by the pre-cessation premium margins and lapse releases.

---

## Valuation and reserve pointers

This library projects gross best-estimate liability cash flows; valuation layers consume
them and are cited, not reproduced:

- **Solvency UK best estimate.** The best estimate is the probability-weighted average of
  future cash flows discounted at the relevant risk-free term structure, on realistic
  assumptions, gross of reinsurance (PRA Rulebook Technical Provisions 3.1) [REG-R1] —
  exactly what this model's expected cash flows feed. Technical provisions = best estimate +
  risk margin, market-consistent (2.3, 2.4) [R3] [REG-R1].
- **Risk margin.** Cost-of-capital method at 4% (Solvency UK rate, effective 31 December
  2024 definitions) [R3], with the life-business risk-tapering factor lambda = 0.9 (floor
  0.25) from SI 2023/1346 [REG-R4]. Requires an SCR runoff — cited-not-specified.
- **Solvency UK frame.** Assimilated Solvency II law was revoked 31 December 2024 and
  restated into PRA rules effective the same date; the PRA Rulebook, not EU text, is the
  operative source [R4]. Legacy back-books (the unit-linked variation [S15]) may carry TMTP,
  which adjusts technical provisions, not projected cash flows [REG-R3].
- **Realistic-lapse warning.** A best estimate on realistic assumptions [REG-R1] *embeds the
  lapse-support profits*: raising assumed lapses lowers the BEL of the O50 cell. The FCA's
  articulation of the reliance on lapses [R2] makes lapse the assumption to govern hardest
  (TAS 100 justified-assumptions discipline [R8]).
- **IFRS 17.** UK-adopted IFRS 17 (adopted 16 May 2022, effective 1 January 2023, replacing
  IFRS 4) applies to IFRS reporters [REG-R38]; the fulfilment-cash-flow engine consumes the
  same projections with different discounting/aggregation layers.
- **Professional standards.** TAS 100 v2.0 (effective 1 July 2023) applies to all UK
  technical actuarial work including this modeling [R8]; TAS 200: Insurance v2.0 (effective
  1 January 2025) applies additionally to insurance technical actuarial work [REG-R34].

---

## Key sensitivities and model risks

Dominant assumptions, in order, for a guaranteed-acceptance (O50) block:

1. **Lapse — sensitivity analysis mandatory.** With no surrender value, every lapse is a
   pure profit release; the FCA itself records the reliance on lapses for profitability [R2].
   BEL is monotonically decreasing in lapse rates; run at 0.5x / 1x / 2x base lapse and at
   zero lapse (the conduct-stress floor). The pro-rata paid-up variant [S9] converts
   post-halfway lapses into paid-up liabilities and collapses most of the lapse sensitivity —
   model it as a separate variant, never as a small adjustment.
2. **Guaranteed-acceptance mortality and anti-selection.** The 120% x ONS loading is a [std]
   placeholder; the true basis is proprietary and the CMI's non-underwritten whole of life
   analysis was pending as of the fetched announcement [R7] [REG-R32]. Year-one anti-selection
   interacts with the moratorium: the refund design exists precisely because year-1
   non-accidental mortality is anti-selected.
3. **Longevity past the crossover and past cessation.** Post-90 the policy is pure outgo;
   improvement assumptions (CMI_20xx-style, subscriber-restricted [REG-R30]) directly
   lengthen it. For the UW cell, whole-of-life duration makes the liability improvements- and
   discount-dominated.
4. **Expense inflation vs fixed premiums.** Premiums are small (£30/month anchor) and level;
   maintenance expenses inflate. The expense margin erodes mechanically — a per-policy
   expense assumption error compounds over 20+ year horizons.
5. **Escalation take-up (UW variant).** Premium escalates at 2x the benefit rate [S10]; the
   variant is premium-margin-accretive but lapse-sensitive (escalating premiums into fixed
   incomes); opt-out behavior (three declines end the option [S10]) is unobserved **[std]**.

Known modeling pitfalls:

- **Moratorium boundary.** The month-12/13 discontinuity (~11x jump in expected death outgo
  in the worked example) must not be smoothed by annual-grid interpolation; if projecting
  annually, split year 1 explicitly.
- **Refund base.** The year-1 non-accidental benefit is *cumulative premiums paid*, not the
  cash sum and not an annualized premium; with the arrears rule, claims in the 60-day window
  are further reduced by unpaid amounts [S9].
- **Lapse after cessation.** There are no premiums to stop paying after T_cess; applying a
  lapse decrement there silently destroys liability. Set w = 0 post-cessation **[std]** (and
  in paid-up states).
- **Accidental-multiplier double-count.** The 2x applies to *accidental* death on/after the
  first anniversary only [S7]; applying it in year 1 (where accidental already pays 1x SA in
  the base plans, and that variant's own year-1 accidental benefit is 1x the cash sum [S7])
  or to all deaths overstates outgo.
- **Anti-selective options (UW).** Milestone-benefit increases without underwriting [S10]
  and smoker-status reviews [S10] are exercised against the office; excluding them is a
  [std] scope choice that understates tail risk on large-sum business.
- **Terminal illness timing (UW).** TI pays the same amount earlier; ignoring acceleration
  understates the present value slightly. Do not model TI as an *additional* decrement —
  it accelerates the death benefit, it does not add one [S10] [S12].
- **Basis mixing.** The O50 cell uses a population-plus-loading basis, the UW cell an
  assured-lives shape [R6] [REG-R32]; feeding either cell the other's basis produces
  plausible-looking but wrong margins (the FCA's £71.73 vs £8.10 differential [R2] is the
  scale of the error).
- **Claims interest.** Excluded [std]; if added, it is a settlement-lag uplift at BoE − 0.5%
  (floor 0.5%) on death claims [S1] [S9], not a discounting change.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R2]: #uklib-whole_of_life-r2
[R3]: #uklib-whole_of_life-r3
[R4]: #uklib-whole_of_life-r4
[R6]: #uklib-whole_of_life-r6
[R7]: #uklib-whole_of_life-r7
[R8]: #uklib-whole_of_life-r8
[REG-R1]: #uklib-reg-r1
[REG-R22]: #uklib-reg-r22
[REG-R24]: #uklib-reg-r24
[REG-R3]: #uklib-reg-r3
[REG-R30]: #uklib-reg-r30
[REG-R32]: #uklib-reg-r32
[REG-R34]: #uklib-reg-r34
[REG-R38]: #uklib-reg-r38
[REG-R4]: #uklib-reg-r4
[std]: #uklib-std
[unverified]: #uklib-unverified
<!-- END generated citation links -->
