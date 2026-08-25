# Technical Notes

**Status:** Draft, 2026-08-20 (all cited sources accessed 2026-08-20).

**Scope note.** These notes turn the standardized composite whole life assurance (*shūshin
hoken*, 終身保険) of `product-spec.md` (same directory) into a reference liability cash-flow
projection on paper. This is not any single insurer's product. [S#] and [R#] tags resolve
against `sources.md`, whose numbering is carried verbatim from `_research/whole-life.md` and
is frozen; [REG-R#] tags resolve against the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is distinct.
**[std]** marks a standardization introduced for the reference implementation; [unverified]
marks a claim that could not be confirmed against a retrieved document. **Every parameter
value here is identical to `product-spec.md`'s.** Three parameters appear here that the
specification does not name, all of them internal to the surrender-value construction that
specification footnote 15 defers to this document: the cash-value basis rate `i_cv`, the
acquisition-deduction rate `α`, and the reference valuation rate `i_std`. Each is **[std]**
and each is derived, not asserted, below.

This is the library's **savings chassis**. The policy value, the surrender value
(*kaiyaku-henreikin*, 解約返戻金), the suppressed-surrender-value
(*tei-kaiyaku-henreikin-gata*, 低解約返戻金型) cliff and the automatic premium loan, APL
(*jidō furikae kashitsuke*, 自動振替貸付) are specified once, here. The
[endowment technical notes (養老保険)](../endowment/technical-notes.md) and the
[FX whole life technical notes (外貨建終身保険)](../fx_whole_life/technical-notes.md) state deltas against this
file.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows** per policy — premiums,
  death and severe disability (*kōdo shōgai*, 高度障害) claims, surrender benefits, expenses and
  commission — for a single-policy model point, in the sense the ESR current estimate (*genzai
  suikei*, 現在推計) requires: probability-weighted future cash flows on assumptions re-set
  at each 基準日, gross of reinsurance [REG-R15]. It is also what the 保険計理人's **1号収支分析**
  consumes [REG-R6] [REG-R22]. **Discounting, MOCE, required capital and every statutory
  reserve are out of scope** and are cited, not reproduced — see Valuation and reserve
  pointers, which sets out both the 1号収支分析 and the reserving chain.
- **Projection frequency.** **Annual**, on policy years running anniversary to anniversary
  (`WholeLife_JP_A`). The product has no intra-year contractual structure on the composite:
  the sum assured is level for life, the premium is level, and the only date that matters
  inside a year is the 払込満了日, which is an anniversary by construction. The composite pays
  annually, so the grace (猶予期間) and the APL both operate on an annual cycle [S1] [S3] [S10].
- **Timing conventions [std].** Premium at the **start** of each policy year, in advance,
  for years 1 … m; maintenance expense and renewal commission at the start of each year;
  acquisition expense and initial commission at issue (start of year 1); death claims and
  claim expenses at the **end** of the policy year of death; surrenders at the **end** of
  the policy year, **after** deaths, valued on the surrender value at that anniversary.
- **Age basis.** 契約年齢 is attained age (*man-nenrei*, 満年齢) with the fractional year discarded
  at 契約日, incrementing on each 年単位の契約応当日 rather than on the birthday [S1] [S3] [S9]. A
  projection stepped on anniversaries therefore steps the rating age correctly by
  construction, and the attained age in year `t` is `x + t − 1` exactly — no select
  adjustment, no half-year offset. **The mortality table does not share this basis**:
  生保標準生命表2018（死亡保険用）is built for use on a nearest-birthday insurance age
  (*hoken-nenrei*, 保険年齢) 方式 [REG-R20]. The
  reference implementation reads the table at the 満年齢 attained age with no adjustment
  **[std]**, because no public mapping between the two bases exists; the resulting bias
  understates mortality by up to half a year of age. On the male table half a year of age
  is worth 3.6–5.0% of `q` between attained ages 35 and 65, but under 2% in magnitude
  between 23 and 31, where the curve flattens and dips, and as much as 14% between 15 and
  16, where `q` is smallest and climbing steeply. Named here, not hidden.
- **Currency.** JPY throughout. Amounts are written ¥ with thousands separators. There is no
  currency layer on this product; the
  [FX whole life (外貨建終身保険)](../fx_whole_life/technical-notes.md) adds one.
- **Model points.** Single-policy model points projected on an expected
  (probability-weighted) basis: survivorship multiplies per-policy cash flows. `point_id`
  parameterizes `Projection`; `point_id = 1` is the worked-example anchor cell. No
  aggregation logic is specified here.
- **Termination.** There is no maturity date and no 満期保険金 [S1] [S3] [S5] [S7] [S9] [S10].
  The projection runs to the **terminal age of the mortality table**: `T = ω − x + 1`, with
  ω = **109** for males and **113** for females on 生保標準生命表2018（死亡保険用）, the first age at
  which `q(ω) = 1.00000` [REG-R18] [R1]. Every remaining life dies in year `T`; nothing is
  paid at `T` other than the death benefit. There are no tail states.
- **Contract boundary.** The premium is level and guaranteed for the whole of 保険料払込期間 and
  the insurer has no unilateral repricing right [S1] [S3] [S7] [S10], so all `m` years of
  premium and the whole-of-life benefit are inside any defensible boundary. Japan's ESR 柱1
  告示 were not opened in the research pass and their boundary text is [unverified] [REG-R16];
  the model therefore does not implement a boundary test, it projects the whole contract and
  says so.
- **Rounding.** Intermediate values at full precision; displayed cash flows to **two decimal
  places [std]**, which is the precision the tests assert. Contractual amounts a
  policyholder actually receives are integral yen, but the model does not round them: a
  probability-weighted expected value has no contractual denomination.

---

## Model point attributes

| Attribute | Type | Anchor cell (`point_id = 1`) |
|---|---|---|
| `policy_id` | str | `WL-JP-0001` |
| `sex` | enum {M, F} | M |
| `issue_age` (`x`) | int, 満年齢, 15–80 | 30 |
| `sum_assured` (`SA`) | JPY, ¥2,000,000–¥50,000,000 in ¥1,000,000 units | 5,000,000 |
| `prem_term` (`m`) | int years, or 0 for 終身払 | 15 |
| `premium_annual` (`P`) | JPY, level for years 1 … m | 174,960 |
| `low_cv` | bool — 低解約返戻金型 elected | true |
| `low_cv_rate` (`k`) | 解約払戻金支払割合 | 0.70 |
| `apl_elected` | bool — 自動振替貸付 elected (default on) | true |
| `pol_loan_util` | fraction of `cv_pp` drawn as 契約者貸付 | 0.00 |
| `dividend_type` | enum {none, five\_year} | none |

There is **no issue date (契約日) attribute**, and that is a product fact rather than an
omission: the projection runs on policy years, 契約年齢 is fixed at 契約日 and increments on the
年単位の契約応当日 rather than the birthday [S1] [S3] [S9], and the one intra-year date that
matters — the 払込満了日 — is an anniversary by construction. Six further model-point columns
carry the optional modules rather than the contract (`default_rate`, `pol_loan_year`,
`lapse_spike`, `dyn_lapse`, `mort_adj`, `pua_year`); each is specified in the assumption
tables below. The `mort_adj` **column** is read by the `mort_be_factor` cells, which carries
the library-wide name for the multiplier; the column keeps its own spelling.

`prem_term = 0` denotes 終身払, for which `m` is treated as infinite: no 払込満了 date exists, the
suppressed period runs for life [S4], and the cliff never occurs. That point must be in the
table, because it is the one configuration in which the product's signature mechanic is
absent by construction.

The anchor premium is **sourced, not constructed**: ¥14,580 per month for this exact cell is
published [S4], and the annual figure is 12 × that **[std]** (`product-spec.md` footnote 5).
No carrier publishes an annual-mode scale, so the modal discount a real 年払 rate would carry
is not applied and the annual premium is slightly overstated — the direction is stated, not
corrected.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `pols_if(t)` | In-force probability at the **start** of policy year t; `pols_if(1) = 1` | annual recursion |
| `mort_rate(t)` | Mortality rate (incl. 高度障害) in year t | table lookup at `x + t − 1` |
| `lapse_rate(t)` | Voluntary surrender rate in year t | assumption table |
| `default_rate(t)` | Premium-default rate in year t (optional module; 0 in base) | assumption table |
| `pol_val_pp(t)` | `V(t)` — the ordinary, **unsuppressed** surrender value at anniversary t | closed form |
| `cv_pp(t)` | The **payable** 解約返戻金 at anniversary t, after the 低解約返戻金型 multiplier | closed form |
| `surr_charge_pp(t)` | `SC(t)` — the 解約控除 embedded in `pol_val_pp` | closed form |
| `reserve_pp(t)` | 平準純保険料式 policy reserve, reference quantity only — **never a cash flow** | closed form |
| `pols_if_pay(t)` | Of `pols_if(t)`, the premium-paying cohort; `pols_pay_bef_decr(t)` is that cohort after the year's defaults, and is the weight on premium and renewal commission | annual recursion |
| `pols_if_apl(t, s)` | In-force probability on APL at start of year t, having defaulted in year s | annual recursion |
| `loan_apl_pp(t, s)` | Outstanding APL principal and interest per policy in that cohort; `loan_pp(t)` is the paying cohort's 契約者貸付 balance | annual recursion |

`pols_if_apl` and `loan_apl_pp` are indexed by the **entry year `s`** and not collapsed to a
cohort average. That is deliberate: the APL exhausts at a duration that depends on when the
loan started, so an average balance would let early entrants ride on late entrants' headroom
and would move the termination year by decades (below, the same policy exhausts at `t = 3`
or `t = 53` depending only on `s`). The triangle is the honest structure.

The base run carries no loan, no APL cohort and no 契約者貸付: `default_rate ≡ 0` and
`pol_loan_util = 0`, so `loan_pp ≡ 0`, `loan_apl_pp ≡ 0` and every benefit is gross. Both
modules are exercised in both positions in testing.

---

## Assumption inputs

Three classes, kept apart on purpose. The split is not a modelling nicety here: a Japanese
illustration must separate guaranteed (保証) from non-guaranteed (非保証) elements, because
presenting a non-guaranteed element as certain is 断定的判断の提供 under 消費者契約法第4条 [REG-R38].

### (a) Contractual / guaranteed elements (cited; the insurer cannot change them)

| Input | Value | Basis |
|---|---|---|
| Death benefit | `SA`, level for life, net of `L(t)` | [S1] [S3] [S7] [S9] [S10] |
| 高度障害保険金 | Same amount, on the 別表 disability state; extinguishes the contract | [S1] [S3] [S7] [S9] |
| Premium `P` | Level and guaranteed for years 1 … m; none thereafter | [S1] [S3] [S7] [S10] |
| 保険期間 | 終身 — no expiry, no 満期保険金 | [S1] [S3] [S5] [S7] [S9] [S10] |
| 解約払戻金支払割合 `k` | 0.70 during 低解約払戻期間; 1.00 thereafter | [S3] [S7] [S9] [S11] |
| 低解約払戻期間 | Identical to 保険料払込期間, i.e. `m` years | [S3] [S6] [S7] [S11] |
| Clawback | Suppressed basis persists past `m` where premiums in the low period were unpaid | [S3] [S4] [S5] [S9] |
| 解約返戻金 arguments | A function of elapsed months **and** paid months while premiums are due | [S1] [S3] [S10] |
| APL continuation test | Advance plus interest must not exceed the surrender value computed as if the premium had been paid, net of existing loan | [S1] [S3] [S10] |
| APL interest ceiling | 年8% / 半年4% / 月 8/12%; a fourth carrier publishes the 年8% ceiling alone | three ceilings [S1] [S7] [S10]; 年8% [S3] |
| 契約者貸付 limit | 9/10 of `cv_pp` while premiums are paid, 8/10 once 払込済, existing balance deducted first | [S1] [S3] [S7] |
| Loan-excess termination | Contract lapses where loan and interest exceed the surrender value and the top-up is unpaid | [S1] [S3] [S10] |
| 免責 — suicide | 3 years from the 責任開始期, reset on 復活 | [S1] [S3] [S7] [S8] [S9] [S10]; statutory frame [REG-R34] |
| Refused claim | The 保険料積立金 / policy reserve (*sekinin-junbikin*, 責任準備金) is paid to the policyholder, not nothing | [S1] [S9] [S10] |
| 復活 window | 3 years from lapse, barred once the surrender value is claimed | [S1] [S3] [S7] [S10] |
| Policyholder protection | 90% of the 責任準備金 on insurer failure | [REG-R40] [REG-R41] |

### (b) Insurer-discretionary current elements

Unlike a UK guaranteed-premium term policy, this class is **not** nearly empty — it is where
the product's economics live, and every item in it is a rate the insurer sets and may
change.

| Input | Snapshot value | Basis |
|---|---|---|
| APL / 契約者貸付 interest `i_L` | **2.75% p.a.**, compound, held flat | level [S2]; ceilings [S1] [S7] [S10]; pick **[std]** |
| Rate-review calendar | Reviewed each January and July at two carriers, the revision applying to existing loans; not modelled | [S7] [S11]; flat **[std]** |
| Assumed pricing interest rate (*yotei riritsu*, 予定利率) | 1.75% p.a. — a 2010 disclosure, carried as documentation | [S11]; current value [unverified] |
| Cash-value basis rate `i_cv` | **1.468% p.a.** — solved from the published surrender table | derived **[std]**, below |
| Acquisition deduction `α` | **0.0090** of `SA`, grading linearly to zero at `m` | derived **[std]**, below |
| 契約者配当 | None — the composite is 無配当. Variant: 5年ごと利差配当, off in the base run, declaring `div_spread × div_period × V(t)` at every fifth anniversary with `div_spread` = **0.25% p.a.** over `div_period` = **5** years | [S1] [S3] [S5] [S11]; variant [S7]; legal frame [REG-R9]; spread and period **[std]**, below |
| 払済保険 conversion basis | The insurer's own single-premium net rate `A(x+t)`; not modelled in the base run | [S1] [S3] [S7] [S9] [S10] |

**Why `i_cv` is not 1.75%.** The 予定利率, 予定死亡率, 予定事業費率 and the surrender-value formula all
live in the 保険料及び責任準備金の算出方法書, a filed but unpublished 基礎書類 [REG-R2] — no amount of further
research turns them into sourced values. What *is* public is a complete numeric
surrender-value run for one model point [S4], and a second carrier's matched suppressed and
ordinary pair [S7]. The library therefore constructs `V(t)` in closed form and **calibrates
it to the published table**, and the calibrated rate lands at 1.468%, not at the 1.75%
disclosed in a 2010 booklet. The gap is informative rather than embarrassing: the published
table is a 2025 rate page [S4] and the disclosure is fifteen years older [S11]. `i_cv` is
the live model input; 1.75% is carried as a documented fact and a sensitivity anchor, and
appears nowhere in the cash-flow recursion.

**The dividend spread, and why it is 0.25%.** On the 5年ごと利差配当 variant the declaration is
made every five years from inception where the investment return on 責任準備金等 exceeds the
return assumed in pricing, accumulates at a company-set rate as 5年ごと積立配当金 and may be nil
[S7]. The *rate* is a 三利源 calculation inside the unpublished 算出方法書 [REG-R2] and no carrier
publishes it, so `div_spread` = **0.25% p.a. [std]**, applied over `div_period` = **5**
years of `V(t)`. The five-year period is not a standardization — it is in the product name
[S7] [S10]. The only interest-margin figures recovered anywhere in the research pass bracket
the pick from both sides: a **0.2%** asset-management deduction inside one carrier's 積立利率
formula [S11], and a **0.05%** 契約者配当金積立利率 at another [S2]. Neither is a 利差 declaration
rate, so the pick is a standardization and not a reading; it moves only the `dividends`
column, which is zero on every model point but one.

### (c) Behavioral / experience assumptions (modeler's view)

**Mortality.** 生保標準生命表2018（死亡保険用）is the sourced basis, read from the publisher's own PDF
[REG-R18] [R1]. Two facts must be carried together and never blurred. First, the table
**includes 高度障害 inside the death rate** [REG-R20] [R2] — so a projection using it must not
add a separate disability decrement, and the two benefits are one decrement on one amount.
Second, it is a **valuation** table: 2008/2009/2011 experience carried forward by an
improvement allowance of 2.5% p.a. for five years then 1.0% p.a. for three, then loaded by a
数学的危険論による補整 sized to hold the exceedance probability to about 2.28% (a 2σ level), capped at
130% of the unadjusted rate [REG-R20] [R2]. A best-estimate basis is therefore a **[std]**
adjustment *of* a sourced table.

| Input | Value | Basis |
|---|---|---|
| Base table | 生保標準生命表2018（死亡保険用）, sex-distinct, `q` at attained age `x + t − 1` | [REG-R18] [R1] |
| `mort_be_factor` | **1.00** in the base run | **[std]** |
| Terminal age ω | 109 (M) / 113 (F) | [REG-R18] [R1] |
| Improvement overlay | None | **[std]** |

`mort_be_factor = 1.00` is a choice, not a default: it means **the base run is a
valuation-table run, not a best estimate**, and it is taken so that every mortality rate the
worked example quotes is a published one that anyone can download and check. The 2σ margin
pushes rates up and the built-in improvement allowance pushes the best-estimate multiplier
further down,
but no retrieved source sizes either against current insured experience, so no defensible
single haircut exists. `mort_be_factor` is the named lever; a production basis would sit
somewhere below 1.00 and would move claims proportionately.

**The shipped table is a construction, and every figure below is computed on it.** The
IAJ's site terms prohibit reproduction, alteration and transmission of the tables
without written consent [REG-R21], so `jplib` does not distribute a copy of the file.
`mort_table.csv` is a **[std]** construction whose `provenance` column tags every row, and
it is the **canonical `jplib` death table**: one file, built once from the union of the
anchors every product in this library sources, shipped identically by all of them, so a
rate quoted in two products carries the same number **and** the same provenance in both.
This product ships the age range it reads, 15 to ω.

Every row is one of two kinds and its `provenance` says which. An **ANCHOR** row is a rate
**quoted and attributed** to [REG-R18]; an **INTERPOLATED** row is filled by **log-linear
interpolation in ln `q` between the two neighbouring anchors**, evaluated in double
precision and rounded to five decimal places. Nothing is extrapolated: each sex runs from
an age-0 anchor to a terminal anchor, so every interpolated age lies strictly between two
sourced ones. Over the range shipped here, **27 of the 95 male rows and 24 of the 99 female
rows are anchors**; the remaining 68 and 75 are the standardization, and they are not IAJ
values.

**How far an interpolated row sits from the published rate is not known and is not
asserted.** The library reads the anchors and constructs the rest, so it has nothing to
measure the fill against, and an earlier revision of these notes quoted a comparison
against the full published table that the library cannot support. What is known is where
the fill is thinnest: past age 90 the anchors are five and then four years apart while `q`
is turning over, the widest gap in the file. Of the rates the worked example below prints,
`q(30)` … `q(34)` and `q(45)` are anchors and `q(43)` and `q(44)` are interpolated — which
is why the assumption list quotes only the first five as read from the publisher's PDF. A
user who has downloaded the IAJ PDF replaces `mort_table.csv` with a same-schema file and
changes no formula.

**Surrender.** No carrier publishes a lapse or surrender curve by duration; this is the
single largest assumption gap for the product. The only public benchmark is the industry
解約・失効率 of **5.6%** for FY2024 [R12] [REG-R31], and the same report defines it as
surrendered-and-lapsed **sum assured** over opening in-force sum assured, industry-wide
across all product types — an amount-weighted, all-product bound, not a per-policy
whole-life rate. It is used here as a sanity ceiling and nothing more.

| Policy year `t` | 1 | 2 | 3 … m−1 | **m** | m+1 … |
|---|---|---|---|---|---|
| `lapse_rate(t)` **[std]** | 4% | 3% | 2% | **17%** | 2% |

The shape is reasoned, not fitted: a 低解約返戻金型 owner who surrenders during the low period
takes a 30% haircut on a value that is already below cumulative premiums (70.1% of premiums
paid at duration 5 on the published table [S4]), so early surrender is strongly suppressed;
at `t = m` the value steps up by a factor of 1/k and crosses 100% of premiums paid, and the
product has been sold on exactly that crossing. The `m`-year entry is `2% + s` with the
**cliff spike `s` = 15% [std]**, held as a separate parameter so that it can be switched off
and the sensitivity read directly.

**Premium default and the APL (optional module, off in the base run).**

| Input | Value | Basis |
|---|---|---|
| `default_rate(t)` | **0** in the base run; **1% p.a.** for 1 ≤ t ≤ m in the module | **[std]** |
| APL clawback on the defaulting cohort | On — the suppressed basis persists past `m` | [S3] [S4] [S5] [S9] |
| Reinstatement (復活) | Not modelled; every exit is terminal | **[std]**, below |

**Expenses and commission (levels all [std]; no carrier publishes an expense basis at all —
予定事業費率 is named in the 保険契約者保護機構 boilerplate [S1] [S7] and never quantified).**

| Input | Value |
|---|---|
| Acquisition expense `E0` | ¥50,000 per policy at issue **[std]** |
| Initial commission `c0` | 90% of the annual premium at issue **[std]** |
| Renewal commission `c_r` | 3% of premium, years 2 … m **[std]** |
| Maintenance expense `e(t)` | ¥8,000 p.a., **for life**, inflating at 1.0% p.a. **[std]** |
| Claim expense `ec` | ¥20,000 per death claim **[std]** |
| Surrender expense | None — folded into maintenance **[std]** |

Expense inflation of 1.0% **[std]** is deliberately below the 3% a UK or U.S. model would
carry; importing 3% into a Japanese whole-life run over an eighty-year horizon compounds to
a different product. Maintenance expense continuing **after 払込満了, for life** is the
structural point: this is a whole life contract on which premiums stop after `m` years and
obligations do not.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t` | policy year, t = 1 … T; attained age in year t is `x + t − 1` |
| `x`, `T`, `ω` | 契約年齢 at issue; projection length `T = ω − x + 1`; table terminal age |
| `m` | 保険料払込期間 in years (∞ for 終身払) |
| `SA`, `P` | 保険金額; annual premium, payable at the start of years 1 … m |
| `q(t)`, `w(t)`, `u(t)` | mortality rate; voluntary surrender rate; premium-default rate in year t |
| `l(t)` | in-force probability at the start of year t; `l(1) = 1` (`pols_if`) |
| `lp(t)` | of those, the part still **paying premium in cash** in year t, after that year's defaults into the APL state (`pols_pay_bef_decr`); `lp(t) = l(t)` in the base run |
| `D(t)`, `S(t)` | expected deaths in year t; expected surrenders in year t |
| `A(y)`, `ä(y, n)` | whole-life EPV of 1 at age y and n-year annuity-due, on `i_cv` and the table |
| `π` | net level premium on the cash-value basis, `SA × A(x) / ä(x, m)` |
| `W(t)` | prospective net level premium policy value at anniversary t |
| `SC(t)` | 解約控除 — acquisition-cost deduction (`surr_charge_pp`) |
| `V(t)` | ordinary, unsuppressed surrender value (`pol_val_pp`) |
| `k` | 解約払戻金支払割合 — 0.70 when 低解約返戻金型 is on, 1.00 otherwise |
| `CV(t)` | payable 解約返戻金 (`cv_pp`) |
| `L(t)` | loan + APL principal and interest at the **start** of year t |
| `i_cv`, `i_L`, `i_std` | cash-value basis rate; loan rate; reference valuation rate |
| `α` | acquisition-deduction rate, per unit of `SA` |
| `E0`, `e(t)`, `c0`, `c_r`, `ec` | acquisition expense; maintenance; initial and renewal commission; claim expense |
| `CF(t)` | net cash flow of year t, **income-positive** (`net_cf`) |

**Dimensional check.** `q`, `w`, `u`, `k`, `α`, `c0`, `c_r`, `l` and `lp` are dimensionless;
`i_cv`, `i_L`, `i_std` are per annum; `A` and `ä` are pure numbers (`ä` in years of premium,
so `SA × A / ä` is ¥ per year); `SA`, `P`, `W`, `SC`, `V`, `CV`, `L`, `E0`, `e`, `ec` are ¥;
every term of `CF(t)` is ¥ per policy issued per year. No term mixes a per-annum rate with a
stock without an explicit year count.

### 責任準備金 and 解約返戻金 — two quantities, one relationship

They are different objects and a model that conflates them is wrong in both directions.

**責任準備金** is statutory. For an in-scope contract — and
a level-premium 終身保険 with a fixed 予定利率 is in scope [R6] [REG-R7] — it is accumulated
net level premium method (*heijun jun-hokenryō-shiki*, **平準純保険料式**), with **no Zillmer
adjustment**, on the standard valuation rate (*hyōjun riritsu*, 標準利率) and
生保標準生命表2018（死亡保険用）[R7] [R8] [REG-R10] [REG-R11]:

    π*        = SA × A*(x) / ä*(x, m)                     on (i_std, 標準生命表2018)
    reserve_pp(t) = SA × A*(x + t) − π* × ä*(x + t, max(m − t, 0))

**解約返戻金** is contractual. Its formula is in the unpublished 算出方法書 [REG-R2]; what the 約款
publish is its argument list — elapsed months and paid months, the elapsed count capped at
the paid count while premiums are due [S1] [S3] [S10]. The library constructs it as a policy
value of the **same form** on a **different basis**, less a 解約控除 grading to zero **[std]**:

    π         = SA × A(x) / ä(x, m)                       on (i_cv, 標準生命表2018)
    W(t)      = SA × A(x + t) − π × ä(x + t, max(m − t, 0))
    SC(t)     = α × SA × max(0, m − t) / m
    V(t)      = max(0, W(t) − SC(t))

The relationship is then exact and testable. **When the two basis rates coincide** (`i_std =
i_cv`, which is the base-run default so that the identity can be asserted),

    reserve_pp(t) − V(t) = SC(t)          for every t

— the whole difference is the 解約控除, which is precisely what 平準純保険料式 forbids the reserve to
carry [REG-R10]. **When they do not coincide the ordering can fail**: with a 標準利率 below the
pricing basis the statutory reserve exceeds the cash value by far more than `SC(t)`, and in
a deep negative-spread (逆ざや) configuration the reserve can exceed even the sum assured.
`reserve_pp ≥ V ≥ CV` is therefore **not** a model invariant and must not be asserted as
one. `reserve_pp` produces no cash flow; it exists so the identity above can be checked.

### The 低解約返戻金型 cliff

    CV(t) = k × V(t)     for t <  m       (k = 0.70 when 低解約返戻金型 is on)
    CV(t) =     V(t)     for t >= m

and the transition at `t = m` is a **step**, not a ramp. Two carriers' published tables
agree on it to rounding, and one of them settles what the suppression *is*: at duration 40,
well past 払込満了, the suppressed and ordinary products have **identical** surrender values
[S7]. So there is **one** `V(t)` and **one** multiplier — not two reserve runs. Everything
derived from the surrender value is suppressed with it: the 払済保険金額, the 契約者貸付 amount and the
APL amount are all computed off `CV(t)` [S7] [S9] [S11].

Two quantities coexist at `t = m` and a model must publish both: `k × V(m)`, the value an
instant before the step (the published ¥2,047,650 figure), and `CV(m) = V(m)`, the value an
instant after (¥2,928,450) [S4]. **[std] ordering rule:** a surrender occurring in policy
year `m` is paid at the end of year `m` on `CV(m)`, i.e. on the **full** value; the
suppressed value applies to surrenders in years 1 … m−1. The ratio `CV(m) / (k × V(m))` must
equal exactly `1 / k`; anything between is an interpolation the contract does not have.

### 自動振替貸付 as a state

Where the premium is unpaid at grace expiry and there is a surrender value, the insurer
**lends the premium against that value and applies it to the premium**, and the contract
continues in force [S1] [S3] [S7] [S10] [S11]. Lapse on this chassis is therefore a **funded
event, not a behavioural one**. The trigger, stated the same way at three carriers [S1] [S3]
[S10], on the annual grid is

    the APL fires in year t  iff   CV*(t) >= L(t) + P × (1 + i_L)

where `CV*(t)` is the surrender value computed **as if the premium had been paid** — on the
annual grid that is `CV(t)`, the value at the end of year `t` **[std]** — and `L(t)` is the
existing balance at the start of year `t`. The accumulation is compound, with interest
capitalised into principal at each subsequent grace expiry, annually on a 年払 contract [S3]
[S7]:

    L(t + 1) = (L(t) + A(t)) × (1 + i_L),      A(t) = P if the APL fires and t <= m, else 0

Once `t > m` no premium is due, so `A(t) = 0` and the balance rolls up on interest alone
against a value that is still growing — which is why exhaustion after 払込満了 takes decades
rather than years.

**Exhaustion.** If the test fails in year `t`, the contract lapses at that point and the
policyholder may claim the surrender value net of the loan [S1] [S3] [S10]:

    benefit on APL failure = max(0, CV(t − 1) − L(t))

floored at zero, because the loan can exceed the value. The same test, with `A(t) = 0`, is
the **loan-excess termination** the 約款 describe for a 契約者貸付 that outgrows the value [S1]
[S3] [S10]; the notice-and-top-up period is not modelled **[std]**.

**The clawback.** Where not all premiums falling in the suppressed period were paid, the
suppressed basis continues to apply after the period ends [S3] [S4] [S5] [S9]. A cohort
carried through the low period by APL advances has by definition not paid them, so **[std]**
the APL cohort's value is `k × V(t)` for **all** `t` — it never steps up at `m`. This is not
a refinement; it moves the exhaustion year by sixteen years on the anchor cell (below).

### Processing order (policy year t = 1 … T)

1. **Start of year — premium.** Collect `P × lp(t)` if `t ≤ m`. On the APL cohort the premium
   is **not** collected in cash: the advance is applied to it, so it produces no `net_cf`
   entry and appears only as growth in `L`. That is why the weight here is `lp(t)` and not
   `l(t)` — the APL cohort is in force and not paying.
2. **Start of year — expenses.** `e(t) × l(t)`; renewal commission `c_r × P × lp(t)` for `2 ≤
   t ≤ m`. At `t = 1` additionally `E0` and `c0 × P` (per policy issued, `l(1) = lp(1) = 1`).
   Maintenance is carried on the whole in-force population `l(t)`, because the APL cohort
   still has to be administered; commission follows the premium **actually collected**, so
   it is carried on `lp(t)` **[std]**.
3. **Start of year — APL test** (module on). For each entry cohort, apply the trigger above;
   advance or terminate.
4. **Cash values.** Compute `W(t)`, `SC(t)`, `V(t)`, `CV(t)` at the year-end anniversary.
5. **End of year — deaths.** `D(t) = l(t) × q(t)`; outgo `(SA − L(t)) × D(t)`, floored at
   zero; claim expense `ec × D(t)`.
6. **End of year — surrenders**, applied to survivors of mortality **[std order: death
   before lapse]**: `S(t) = l(t) × (1 − q(t)) × w(t)`; outgo `max(0, CV(t) − L(t)) × S(t)`.
7. **End of year — loan roll-up.** `L(t + 1) = (L(t) + A(t)) × (1 + i_L)`.
8. **Update in force.**

       l(t + 1) = l(t) × (1 − q(t)) × (1 − w(t))

9. **At `t = T`** the table's terminal rate is 1, so `l(T + 1) = 0` and the projection ends.
   No maturity payment, no tail states.

### Net cash flow

Income-positive, per policy issued:

    CF(t) = P × lp(t) × 1{t <= m}                         (premiums)
          − (SA − L(t)) × D(t)                            (death and 高度障害 claims)
          − ec × D(t)                                     (claim expense)
          − max(0, CV(t) − L(t)) × S(t)                   (surrender benefits)
          − e(t) × l(t)                                   (maintenance expense)
          − c_r × P × lp(t) × 1{2 <= t <= m}              (renewal commission)
          − (E0 + c0 × P) × 1{t = 1}                      (acquisition)

**Premium and renewal commission are weighted by `lp(t)`, not `l(t)`.** That is the whole
content of step 1: an APL advance is a loan asset and not cash income, so a policy sitting
in the APL state contributes to `l(t)`, to maintenance expense and to every benefit, and to
neither of these two lines. Weighting premium by `l(t)` would book the advanced premium as
income *and* net the loan off the later claim — counting it twice — and would make `net_cf`
move in the year an advance is made, which the pitfalls list below says it must not. The two
weights coincide in the base run, where `default_rate ≡ 0`, which is exactly why the
distinction has to be written down rather than discovered when the module is switched on.

`net_cf` is income-positive throughout; where the notes elsewhere print an outgo-positive
stream that orientation survives as `liability_cf`, with `net_cf(t) == −liability_cf(t)`.
The result columns are `premiums`, `claims_death`, `claims_lapse`, `claim_expenses`,
`expenses`, `commissions`, `dividends` and `net_cf`, with `pols_if` first. `expenses` is
acquisition plus maintenance; the claim handling expense is `claim_expenses` beside it.
`dividends` is a column of zeros on the 無配当 composite and is published rather than dropped,
because the 5年ごと利差配当 variant is a real product in the source set.

**Roll-forward identity.** Because the table terminates, every policy leaves by one of the
two decrements, so

    Σ_t D(t) + Σ_t S(t) = 1     and     l(T + 1) = 0

`check_decrement_sum()` takes no argument and returns a bool over all `t`; the per-`t`
signed residual lives at `check_decrement_sum_resid(t)`.

---

## Policyholder behavior modeling

All dynamic forms are **[std]** reference constructions; there is no public calibration
evidence for any of them on this product.

- **Base surrender.** The duration table in class (c), with the cliff spike held as its own
  parameter. The suppression is a behavioural instrument as much as a pricing one: it costs
  the policyholder 30% of the value to leave early and buys a 16.3% cheaper premium in
  exchange (¥17,040 against ¥20,350 per month on the one carrier that publishes both scales
  for one identical cell [S7]).
- **The spike at 払込満了 is an assumption, not a mechanic.** The step in `CV` is contractual;
  the surge in surrenders at the step is class (c) and nothing else. Nothing in any
  retrieved document quantifies it. Setting `s = 0` and re-running is the correct way to
  read its effect.
- **Dynamic surrender on the 払戻率 [std] (optional module, off in base).** The economically
  natural driver is the ratio of the value to premiums paid:

      w_dyn(t) = w(t) × min(3.0, max(1.0, 1 + β × max(0, CV(t) / cumprem(t) − 1)))

  with `β` = 2.0 **[std]** and `cumprem(t) = P × min(t, m)`. On the anchor cell the ratio
  crosses 1 exactly at the cliff, so this module reproduces the spike endogenously instead
  of imposing it — a useful cross-check on the `s` = 15% choice, not a replacement for it.
- **Premium default and the APL.** Modelled as a decrement `u(t)` out of the premium-paying
  cohort into an APL cohort, **not** as a lapse. A policy does not lapse while the cash
  value can carry the premium, so a whole-life lapse model that applies a lapse rate to
  unpaid premiums without first running the APL test is modelling a decrement the contract
  does not have.
- **Reinstatement (復活) is not modelled [std].** Within three years of lapse, on fresh 告知 and
  payment of arrears, a Japanese policy comes back [S1] [S3] [S7] [S10] — the composite's
  lapse is genuinely not a terminal state, unlike the UK reference set's. Treating every
  exit as terminal **understates** later-duration in force and therefore both premium income
  and claims. The bias is stated rather than corrected because no retrieved source gives a
  reinstatement rate.
- **契約者貸付 take-up.** Static `pol_loan_util` only, base 0. There is no public take-up data.
  Where it is non-zero, the loan is drawn at the anniversary to `pol_loan_util × CV(t)`,
  subject to the contractual 9/10 (in payment) and 8/10 (paid-up) caps [S1] [S3] [S7],
  accrues at `i_L`, and nets off every benefit.
- **払済保険 election.** Modelled as an election at a chosen duration: the contract stops paying
  premiums, `SA` is replaced by `(CV(t) − L(t)) / A(x + t)` on the insurer's own single-
  premium basis, and the suppression switches off for the future — but the conversion itself
  is made on the suppressed value, so the resulting 払済保険金額 is permanently smaller [S3] [S7]
  [S9]. Off in the base run.
- **リビング・ニーズ特約 (a *tokuyaku*, rider) is not an extra benefit.** It accelerates the death benefit on a six-month
  prognosis and reduces `SA` by the amount paid [S1] [S3] [S4] [S7]. Zero incidence in the
  base run **[std]**; modelling it as an addition would double-count.
- **免責 incidence is zero in the base run [std].** Where a claim is refused for an 免責事由 the
  contract does not forfeit — the 保険料積立金 is paid to the policyholder instead [S1] [S9]
  [S10]. Only a policyholder who intentionally caused the death receives nothing. A model
  that treats an exclusion as a zero-payment event overstates the insurer's position.

---

## Worked example

**Anchor cell (`point_id = 1`).** Male, 契約年齢 30 (満年齢), 保険金額 ¥5,000,000, 保険期間 終身, 保険料払込期間 15
years, 低解約返戻金型 **on**, annual premium ¥174,960 (= 12 × the published ¥14,580 monthly premium
for exactly this cell [S4]). `T = 109 − 30 + 1 = 80` policy years, attained ages 30 to 109.

Assumption values used, in full: `q` from 生保標準生命表2018（死亡保険用）男 [REG-R18] [R1] with
`mort_be_factor = 1.00` — **q(30) = 0.00068, q(31) = 0.00069, q(32) = 0.00070, q(33) =
0.00072, q(34) = 0.00074**, all five **anchor rows** of `mort_table.csv`, read from the
publisher's PDF and quoted here because the worked example needs them; `lapse_rate` = 4% /
3% / 2% … 2% / **17%** at t = 15 / 2% **[std]**; `default_rate` = 0 (base run); `E0` =
¥50,000, `c0` = 0.90, `c_r` = 0.03, `e(t)` = ¥8,000 × 1.01^(t−1), `ec` = ¥20,000, all
**[std]**; `i_cv` = 1.468%, `α` = 0.0090, `k` = 0.70; `i_L` = 2.75%, unused
in the base run because `loan_pp ≡ 0`.

### Calibration of the cash-value construction

`π = SA × A(30) / ä(30, 15)` on `i_cv` = 1.468% and the shipped male table gives `A(30) =
0.47678817`, `ä(30, 15) = 13.49765934`, so **π = ¥176,618.83**. `i_cv` was solved so that
`V(15) = SA × A(45)` reproduces the published post-step value, and `α` was set to a round
0.0090 — an initial deduction `SC(0)` of ¥45,000, 25.7% of one annual premium — grading
linearly to `SC(15) = 0`. The fit against the eight published points [S4] is then:

| duration | model `CV(t)` | published 解約払戻金 | difference | model 払戻率 | published 払戻率 |
|---|---|---|---|---|---|
| 5 | 613,589.14 | 613,850 | −260.86 (−0.042%) | 70.14% | 70.1% |
| 10 | 1,306,475.85 | 1,309,400 | −2,924.15 (−0.223%) | 74.67% | 74.8% |
| 15 (pre-step) | 2,050,042.31 | 2,047,650 | +2,392.31 (+0.117%) | 78.11% | 78.0% |
| **15 (post-step)** | **2,928,631.87** | **2,928,450** | **+181.87 (+0.006%)** | 111.59% | 111.5% |
| 20 | 3,128,399.27 | 3,123,700 | +4,699.27 (+0.150%) | 119.20% | 119.0% |
| 30 | 3,547,057.08 | 3,544,650 | +2,407.08 (+0.068%) | 135.16% | 135.0% |
| 40 | 3,977,949.06 | 3,983,950 | −6,000.94 (−0.151%) | 151.58% | 151.8% |
| 50 | 4,386,411.27 | 4,404,300 | −17,888.73 (−0.406%) | 167.14% | 167.8% |

Two closed-form parameters reproduce a carrier's whole published run to within 0.41% at
every duration and to 0.006% at the step. Cumulative premium checks out independently: 15 ×
¥174,960 = **¥2,624,400**, the published 払込保険料累計 [S4]. Note that the published 払戻率 figures
truncate rather than round (2,928,450 / 2,624,400 = 111.586%, printed 111.5%).

**What this construction is not.** `π` = ¥176,618.83 **exceeds** the gross premium of
¥174,960 — a negative expense loading, which no real product carries. The construction uses
the *valuation* table's margin-loaded `q` as a stand-in for the insurer's unpublished 予定死亡率,
and `SC(t)` absorbs the difference. It reproduces the contractual **value**; it is not a
pricing model and `π` is not the priced net premium.

### First periods of the base run

Per policy issued, income-positive, to two decimal places.

| t | age | q(t) | `pols_if(t)` | premiums | claims_death | claims_lapse | claim_expenses | expenses | commissions | net_cf |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 30 | 0.00068 | 1.000000 | 174,960.00 | 3,400.00 | 3,747.52 | 13.60 | 58,000.00 | 157,464.00 | −47,665.12 |
| 2 | 31 | 0.00069 | 0.959347 | 167,847.39 | 3,309.75 | 6,352.17 | 13.24 | 7,751.53 | 5,035.42 | 145,385.28 |
| 3 | 32 | 0.00070 | 0.929925 | 162,699.62 | 3,254.74 | 6,502.46 | 13.02 | 7,588.93 | 4,880.99 | 140,459.49 |
| 4 | 33 | 0.00072 | 0.910688 | 159,334.02 | 3,278.48 | 8,750.23 | 13.11 | 7,506.26 | 4,780.02 | 135,005.91 |
| 5 | 34 | 0.00074 | 0.891832 | 156,034.91 | 3,299.78 | 10,936.27 | 13.20 | 7,424.35 | 4,681.05 | 129,680.27 |
| … | | | | | | | | | | |
| 14 | 43 | 0.00151 | 0.736765 | 128,904.33 | 5,562.57 | 27,910.33 | 22.25 | 6,708.05 | 3,867.13 | 84,833.99 |
| **15** | 44 | 0.00163 | 0.720939 | 126,135.49 | 5,875.65 | **358,347.00** | 23.50 | 6,629.61 | 3,784.06 | **−248,524.33** |
| 16 | 45 | 0.00177 | 0.597404 | 0.00 | 5,287.03 | 35,399.47 | 21.15 | 5,548.54 | 0.00 | −46,256.18 |

`expenses` is **acquisition and maintenance only** and the claim handling expense stands
beside it in its own `claim_expenses` column, which is the settled column vocabulary across
the three libraries; the `dividends` column is zero throughout on this cell and is omitted.
Surrender values at the same anniversaries: `CV(1)` = 93,751.86, `CV(2)` =
220,864.08, `CV(3)` = 349,867.80, `CV(4)` = 480,764.69, `CV(5)` = 613,589.14, `CV(14)` =
1,896,979.14, `CV(15)` = 2,928,631.87, `CV(16)` = 2,968,027.59.

**Trace, year 1.** `D(1) = 1.000000 × 0.00068 = 0.00068`; death claims = 5,000,000 × 0.00068
= 3,400.00; claim expense = 20,000 × 0.00068 = 13.60. Survivors of mortality = 1 − 0.00068 =
0.99932, so `S(1) = 0.99932 × 0.04 = 0.0399728`; `V(1) = W(1) − SC(1) = 175,931.231 − 42,000
= 133,931.231`, and `CV(1) = 0.70 × 133,931.231 = 93,751.8620`, so surrender benefits =
93,751.8620 × 0.0399728 = 3,747.52. Expenses = 50,000.00 + 8,000.00 = 58,000.00;
commission = 0.90 × 174,960 = 157,464.00. `CF(1) = 174,960.00 − 3,400.00 − 13.60 − 3,747.52
− 50,000.00 − 8,000.00 − 157,464.00 = −47,665.12`. Update: `l(2) = 1 × 0.99932 × 0.96 =
0.9593472`.

**Trace, year 2.** Premiums = 174,960 × 0.9593472 = 167,847.39. `D(2) = 0.9593472 × 0.00069
= 0.00066195`; claims = 5,000,000 × 0.00066195 = 3,309.75; claim expense = 13.24. Survivors
= 0.9593472 × 0.99931 = 0.9586853, so `S(2) = 0.9586853 × 0.03 = 0.0287606`; `CV(2)` = 0.70
× 315,520.1189 = 220,864.0832, so surrender benefits = 220,864.0832 × 0.0287606 = 6,352.17.
Maintenance = 8,000 × 1.01 × 0.9593472 = 7,751.53; renewal commission = 0.03 × 174,960 ×
0.9593472 = 5,035.42. `CF(2) = 167,847.39 − 3,309.75 − 13.24 − 6,352.17 − 7,751.53 −
5,035.42 = 145,385.28`. Update: `l(3) = 0.9586853 × 0.97 = 0.9299247`.

**Trace, year 3.** Premiums = 174,960 × 0.9299247 = 162,699.62. `D(3) = 0.9299247 × 0.00070
= 0.000650947`; claims = 3,254.74; claim expense = 13.02. Survivors = 0.9299247 × 0.99930 =
0.929273746, `S(3) = 0.929273746 × 0.02 = 0.018585475`; `CV(3)` = 0.70 × 499,811.1402 =
349,867.7981;
surrender benefits = 349,867.7981 × 0.018585475 = 6,502.46. Maintenance = 8,000 × 1.01² ×
0.9299247 = 7,588.93; renewal commission = 5,248.80 × 0.9299247 = 4,880.99. `CF(3) =
162,699.62 − 3,254.74 − 13.02 − 6,502.46 − 7,588.93 − 4,880.99 = 140,459.49`. Update: `l(4)
= 0.929273746 × 0.98 = 0.910688271`.

**Trace, the cliff at t = 15.** `l(15) = 0.720939`, `q(15) = 0.00163`, so survivors of
mortality = 0.720939036 × (1 − 0.00163) = 0.719763905 and `S(15) = 0.719763905 × 0.17 =
0.122359864`. The value payable is the **post-step** one: `CV(15) = V(15) = 2,928,631.87`,
not `0.70 × 2,928,631.87 = 2,050,042.31`. Surrender benefits = 2,928,631.87 × 0.122359864 =
**358,347.00**, and `CF(15) = 126,135.49 − 5,875.65 − 23.50 − 358,347.00 − 6,629.61 −
3,784.06 = −248,524.33`, the 6,629.61 being maintenance alone, 8,000 × 1.01^14 × 0.720939,
with the 23.50 of claim expense in its own column. One year earlier the same product
produced +84,833.99. **The cliff is the largest single feature of this cash-flow stream and
it is one year wide.** A model that
smooths `CV` across `t = 14 … 16`, or that pays year-15 surrenders on the suppressed basis,
loses or doubles roughly a quarter of a million yen per policy issued in that one year. The
ratio the implementation must reproduce exactly is `CV(15) / (0.70 × V(15)) = 1.4285714286 =
1 / 0.70`.

**Roll-forward check.** Over the full 80 years, `Σ D(t) = 0.305066391` and `Σ S(t) =
0.694933609`, summing to **1.000000000**, with `l(81) = 0`. Undiscounted totals per policy
issued: premiums 2,212,542.21; death claims 1,525,331.95; claim expenses 6,101.33; surrender
benefits 1,692,538.36; expenses 329,814.38; commission 218,591.47; `Σ CF(t)` =
**−1,559,835.29**. Undiscounted, the contract loses money; discounting is out of scope and
is what makes the sign meaningful.

### 自動振替貸付 trace (module on)

The premium plus a year's interest is `P × (1 + i_L) = 174,960 × 1.0275 = ¥179,771.40`. Take
a policy that stops paying at the start of year `s`, with `L(s) = 0`.

**s = 2, 低解約返戻金型 on (k = 0.70).**

    t = 2:  CV(2) = 0.70 × 315,520.1189 = 220,864.08  >=  0 + 179,771.40        -> fires
            L(3) = (0 + 174,960) × 1.0275 = 179,771.40
    t = 3:  CV(3) = 0.70 × 499,811.1402 = 349,867.80  <  179,771.40 + 179,771.40
                                                       = 359,542.80             -> fails
            lapse; benefit = max(0, CV(2) − L(3)) = 220,864.08 − 179,771.40 = 41,092.68

**One advance.** The same default on the **ordinary** form (`k` = 1.00) passes at `t = 3`
(499,811.14 ≥ 359,542.80) and goes on passing: it takes **thirteen** advances, carrying the
policy to `t = 14` and failing at `t = 15`, where `L(15) + P × (1 + i_L)` = 2,764,330.63 +
179,771.40 = 2,944,102.03 finally exceeds `CV(15)` = 2,928,631.87 — reaching the last
premium year all but intact and then paying nothing, because the loan has consumed the
value. **One advance against thirteen, from the same default, at the same duration, on the
same underlying policy value.** That is what running the APL test against 70% of the value
rather than against the value does, and it is why a 低解約返戻金型 contract is simultaneously the
one with the strongest incentive to persist to 払込満了 and the one with the least headroom to
get there.

The first year at which the APL can fund a single premium is `t* = 2` on both forms (`CV(1)`
is 93,751.86 suppressed and 133,931.23 unsuppressed, both under 179,771.40): in year 1 the
APL cannot carry the policy at all, on either form.

**The clawback, priced.** A policy defaulting at `s = 10` takes six advances (years 10 … 15;
after `m` no premium is due and the balance rolls up on interest alone). With the clawback
applied — the correct treatment, since the cohort did not pay its low-period premiums — its
value stays at `0.70 × V(t)` for ever and the loan overtakes it in year **53** (`L(53)` =
3,152,972.42 against `CV(53)` = 3,142,190.57). With the clawback wrongly omitted, the value
steps up at `m` and the same policy survives to year **69**. **Sixteen years of in-force, on
one boolean.**

---

## Valuation and reserve pointers

This library projects gross liability cash flows. Every valuation layer consumes them and is
cited, never reproduced.

- **標準責任準備金.** 保険業法第116条 obliges the reserve and empowers the Prime Minister to prescribe
  the accumulation method and the level of the assumed coefficients for long-term contracts
  [R5] [REG-R4]. 施行規則第68条 fixes the scope — a level-premium 終身保険 with a fixed 予定利率 is in it
  [R6] [REG-R7] — and 第69条 splits the reserve into 保険料積立金, 未経過保険料, 払戻積立金 and contingency
  reserve (*kiken junbikin*, 危険準備金), with 平準純保険料式 as the floor for anything out of scope [R6]
  [REG-R8]. 平成8年大蔵省告示第48号 sets the method (平準純保険料式, **no Zillmer adjustment**), the table
  (生保標準生命表2018（死亡保険用）for contracts concluded from 1 April 2018) and the 標準利率 machinery,
  which for ordinary contracts resets off a 1 October 基準日 against the lower of the
  three-year and ten-year means of 10-year JGB issue yields, with banded safety
  coefficients, a 0.5 percentage-point trigger, 0.25% granularity and effect from the
  following 1 April [R7] [R8] [REG-R10] [REG-R11]. **The current numeric 標準利率 could not be
  established from any retrieved official document**, and the 安全率係数 table for the annual
  case is printed as 「［表略］」 in the retrieved redline [R8] — so `i_std` is **[std]** and
  defaults to `i_cv` so that the `reserve_pp − V = SC` identity is exactly testable. 危険準備金
  is prescribed by sub-class (保険リスク, third sector (*dai-san-bun'ya*, 第三分野) 保険リスク,
  予定利率リスク, 最低保証リスク) [R6] [REG-R8] and is not
  modelled. 価格変動準備金 under 保険業法第115条 is asset-driven and out of scope entirely [REG-R3].
- **ESR.** From **31 March 2026** insurers are supervised on 経済価値ベースのソルベンシー規制, with
  liabilities at 現在推計 plus MOCE, re-measured at each 基準日 on assumptions re-set then,
  discounted on a prescribed curve and calibrated in principle to 99.5%; early corrective
  action triggers below **100%**, replacing the old ソルベンシー・マージン比率 **200%** trigger [REG-R15]
  [REG-R17]. This projection is the 現在推計 cash-flow engine and nothing more: `BEL = Σ_t v(t)
  × [outgo(t) − income(t)]` over the recursion above, with `v(t)`, MOCE and the
  standard-formula coefficients all out of scope — the 柱告示 were not opened and their
  coefficients are [unverified] [REG-R16]. The regime change matters to *this* product
  specifically: the old basis was ロックイン, with mortality, lapse and interest fixed at issue,
  and a 終身保険 written today runs off over eighty years, so a re-projectable,
  assumption-parameterized liability model is the operative artefact rather than a one-off
  pricing exercise [REG-R15].
- **The 意見書 chain.** 保険業法第121条第1項第1号 requires the appointed actuary (保険計理人) to confirm in
  an 意見書 that the reserve is soundly accumulated [REG-R6]; the IAJ 実務基準 turns that into the
  **1号収支分析**, a forward income-and-outgo analysis over at least ten future years by product
  segment under prescribed deterministic or stochastic scenarios, with sufficiency tested
  over the first five [REG-R22]. That is the shape of the output above.
- **Accounting.** **IFRS 17 is not mandatory in Japan** — IFRS applies as 指定国際会計基準 on a
  voluntary basis [REG-R47]. J-GAAP statutory reserving, the ESR economic balance sheet and
  IFRS 17 are three bases over one set of projected cash flows, and this model keeps the
  cash flows basis-agnostic.
- **Disclosure, not valuation, but binding on the model's outputs.** The supervisory
  guideline names 低解約返戻金型 products among those needing extra explanation at the point of
  sale, requires the 解約返戻金 amount or its method to be disclosed, and requires the 自動振替貸付 to
  be at the policyholder's election with prompt notice (監督指針 IV-1-9, IV-1-10, IV-1-12)
  [REG-R14]; the statutory 説明義務 covering a restriction on cancellation is what makes the
  suppression period a disclosable feature rather than a pricing detail [REG-R39]. That is
  why `apl_elected` is a model-point flag with a default and never an unconditional no-lapse
  rule.

---

## Key sensitivities and model risks

In rough order of leverage on this product:

1. **The cash-value construction.** `i_cv` and `α` are two **[std]** parameters carrying the
   entire surrender-benefit stream, which totals ¥1,692,538 against ¥2,212,542 of
   undiscounted premium income on the anchor cell — the largest outgo line after death
   claims. They are
   calibrated to one carrier's published table for one model point [S4]; the fit at other
   issue ages, sexes and payment terms is **unverified**, because no carrier publishes a
   second complete run. A user with a real 算出方法書 replaces `pol_val_pp` and changes nothing
   else.
2. **The cliff spike `s`.** 15% **[std]**, with no public data of any kind behind it. It
   moves year-`m` surrender outgo linearly and it is the assumption a reviewer should
   challenge first. Setting `s = 0` removes it cleanly.
3. **The APL, and whether it is on.** The mechanic is the difference between a lapse model
   and a funded-termination model. Election varies more than any other feature across the
   seven carriers — opt-out at four [S1] [S7] [S10] [S11], opt-in at one [S3], absent at two
   [S8] [S9] — so `apl_elected` is a genuine product variable, not a modelling switch.
4. **The 予定利率 / 標準利率 gap.** Neither current value could be established [R8] [S11] [REG-R10].
   On a level-premium 終身保険 the spread between the pricing rate and the valuation rate is
   what determines whether the statutory reserve behaves at all; a deep 逆ざや inverts the
   `reserve_pp ≥ V` ordering and no model should assert it.
5. **Mortality margin.** `mort_be_factor = 1.00` means the base run is on a valuation table
   with a roughly-2σ margin and an eight-year improvement allowance already inside it
   [REG-R20]. Claims move proportionately with `mort_be_factor`; on an eighty-year
   whole-life run they are the largest single outgo.
6. **The horizon itself.** ω = 109 (M) / 113 (F). More than three quarters of the expected
   death claims on the anchor cell fall after `t = 40` — 0.230566 of 0.305066. Any
   truncation of the projection is a direct understatement.
7. **Expense inflation over eighty years.** 1.0% **[std]** compounds to a factor of 2.19
   over the run; 3% compounds to 10.33. There is no published Japanese expense basis to
   anchor either.
8. **復活.** Not modelled, so in force after a lapse is understated. Japanese policies come
   back for three years [S1] [S3] [S7] [S10]; the UK reference set's terminal lapse is not
   the right intuition here.

Known modeling pitfalls:

- **The cliff is a step, not a ramp.** `CV(t) = k × V(t)` for `t < m` and `V(t)` for `t >=
  m`, with `CV(m) / (k × V(m))` exactly `1 / k` [S3] [S7] [S9] [S11]. Interpolating, grading
  or smoothing across the boundary is wrong; so is a 終身払 point, for which `m` is infinite
  and the step never happens [S4].
- **Off-by-one at the boundary.** Surrenders in policy year `m` are paid on the **full**
  value; the suppressed value applies to years 1 … m−1 **[std]**. Both quantities exist at
  `t = m` and the published table prints both — ¥2,047,650 an instant before and ¥2,928,450
  an instant after [S4] — so a model must be able to produce both and must not lose either.
- **One policy value, one multiplier.** The suppression is a pure haircut on a common
  underlying value: at duration 40 the suppressed and ordinary products have identical
  surrender values [S7]. Running two reserve bases, or two `pol_val_pp` series, is wrong.
- **Lapse is a funded event.** Applying a lapse rate to unpaid premiums without first
  running the APL continuation test models a decrement the contract does not have [S1] [S3]
  [S10]. The premium-default decrement and the voluntary-surrender decrement are different
  objects with different consequences.
- **The APL advance is not cash income.** No cash reaches the insurer; a loan asset is
  created. Booking the advanced premium as `premiums` **and** netting the loan off the claim
  double-counts it. `net_cf` must be unchanged by an APL advance in the year it is made.
  Mechanically this is the choice of weight: premium and renewal commission are carried on
  `lp(t)` and everything else on `l(t)`. The two are equal in the base run, so an
  implementation that weights premium by `l(t)` reproduces the worked example exactly and
  fails only once the APL module is switched on.
- **The APL test runs on the suppressed value.** `CV*(t)`, not `V(t)`. On the anchor cell a
  default at `t = 2` buys **one** advance at `k = 0.70` and **thirteen** at `k = 1.00`;
  running the test on `V` overstates headroom by more than a decade of in force [S7] [S9]
  [S11].
- **The clawback survives the step.** A cohort carried through the low period by unrepaid
  APL advances keeps the suppressed basis after `m` [S3] [S4] [S5] [S9]. On the anchor cell
  that is the difference between exhaustion in year 53 and in year 69.
- **Premiums stop at `m`; nothing else does.** Maintenance expense, death claims, surrender
  benefits and the cash value all continue for life. A projection that ends at 払込満了, or that
  keeps charging renewal commission after it, misses the majority of the liability.
- **Terminal age and table basis.** ω = 109 (M) / 113 (F) on 生保標準生命表2018（死亡保険用） [REG-R18];
  projecting to 100 (a U.S. habit) or to 120 truncates or invents. The table is a
  **valuation** table with a roughly-2σ margin [REG-R20], and it is built for 保険年齢 while
  this product ages on 満年齢 [S1] [S3] [S9] — both must be stated wherever the basis is
  described.
- **高度障害 is inside the death rate, and リビング・ニーズ accelerates.** 生保標準生命表2018（死亡保険用） already
  includes the severe-disability benefit [REG-R20] [R2], so a separate disability decrement
  double-counts; and the living-needs rider reduces the sum assured by what it pays [S1]
  [S3] [S4] [S7], so treating it as an additional benefit double-counts again.
- **Everything is floored at zero.** `V(t) = max(0, W(t) − SC(t))` is negative in principle
  at `t = 0`; the death benefit `SA − L(t)` and the surrender benefit `CV(t) − L(t)` can
  both go negative once a loan has outgrown the value [S1] [S3] [S10]. None of them may
  produce a negative payment.
- **`reserve_pp` is not `cv_pp`.** 平準純保険料式 admits **no Zillmer adjustment** [REG-R10], so
  the statutory reserve carries no 解約控除; `reserve_pp(t) − V(t) = SC(t)` holds **only** when
  the two basis rates coincide, and `reserve_pp ≥ V ≥ CV` is not an invariant under 逆ざや.
  `reserve_pp` must never appear in `net_cf`.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #jplib-whole_life-r1
[R12]: #jplib-whole_life-r12
[R2]: #jplib-whole_life-r2
[R5]: #jplib-whole_life-r5
[R6]: #jplib-whole_life-r6
[R7]: #jplib-whole_life-r7
[R8]: #jplib-whole_life-r8
[REG-R10]: #jplib-reg-r10
[REG-R11]: #jplib-reg-r11
[REG-R14]: #jplib-reg-r14
[REG-R15]: #jplib-reg-r15
[REG-R16]: #jplib-reg-r16
[REG-R17]: #jplib-reg-r17
[REG-R18]: #jplib-reg-r18
[REG-R2]: #jplib-reg-r2
[REG-R20]: #jplib-reg-r20
[REG-R21]: #jplib-reg-r21
[REG-R22]: #jplib-reg-r22
[REG-R3]: #jplib-reg-r3
[REG-R31]: #jplib-reg-r31
[REG-R34]: #jplib-reg-r34
[REG-R38]: #jplib-reg-r38
[REG-R39]: #jplib-reg-r39
[REG-R4]: #jplib-reg-r4
[REG-R40]: #jplib-reg-r40
[REG-R41]: #jplib-reg-r41
[REG-R47]: #jplib-reg-r47
[REG-R6]: #jplib-reg-r6
[REG-R7]: #jplib-reg-r7
[REG-R8]: #jplib-reg-r8
[REG-R9]: #jplib-reg-r9
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
