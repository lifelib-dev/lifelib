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
- **Projection frequency.** **Monthly**, on policy months (`WholeLife_JP_S`). The contract is
  quoted in years — the sum assured is level for life, the premium is level and annual, the
  保険料払込期間 and the lapse curve are stated in policy years — so the monthly step is finer
  than the guarantees rather than finer than the product, and the contractual value
  construction stays annual (see the second bullet below). What the finer grid buys is three
  things the annual step could not do. The **年払 premium** falls in one month out of twelve
  instead of being smeared across a year, which is what a 年払 contract actually looks like.
  The **払込満了 cliff** is one month wide rather than one year: the surrender value steps up by
  `1 / k` at the anniversary and the behavioural surge lands in the month after the last
  premium, beside the step that provokes it. And the **[std ordering]** the annual grid needed
  — paying every surrender in policy year `m` the post-step value, because the step and the
  grid landed on the same year — is retired: eleven of those twelve months are inside the
  保険料払込期間 and are paid the suppressed value, which is what the contract says.
- **Time index [0-based].** `t` is the **0-based policy-month** index: `t = 0` is the first
  policy month, month `t` runs from time `t` to time `t + 1`, and the frame is `t = 0 … T − 1`,
  where `T` is the **number** of policy months projected (`proj_len()`, the exclusive end of
  the frame). The contractual **policy year is the 1-based label `y(t) = 1 + ⌊t/12⌋`** and
  `duration(t) = ⌊t/12⌋` is the count of completed policy years; both are derived and never
  indexed by. The attained age in month `t` is `x + ⌊t/12⌋`, so it steps on the anniversary.
- **The contractual values stay annual, and that is the point of the split.** Everything this
  product guarantees is defined at a 年単位の契約応当日, so the value family keeps the
  **anniversary** index `d = 0 … T_y` with `d = 0` at issue, where `T_y = ω − x + 1` is the
  number of policy years: `W(d)`, `SC(d)`, `V(d)`, `CV(d)`, `CV*(d)`, `cumprem(d)` and the loan
  balance `L(d)` are amounts *at a point in time* on that clock, and **none of their numbers
  moved** when `t` became a month. The 保険料積立金 construction is calibrated to one carrier's
  published **annual** surrender-value run, so re-deriving it monthly would move a fitted
  number rather than a modelled one.
  A benefit falling **between** anniversaries reads `V(u)`, the value at elapsed month `u`, by
  **linear interpolation in the elapsed months [std]**: the 算出方法書 that would state the real
  within-year rule is a 基礎書類 filed with the 金融庁 and is not published [REG-R2], and linear
  interpolation is the market's ordinary convention for a value quoted by policy year. A
  surrender in month `t` is paid on `CV(t + 1)` on that reading, and is settled net of the
  loan balance at the anniversary `⌊t/12⌋`, which is the balance actually outstanding.
- **Timing conventions [std].** Premium at the **start** of the anniversary months
  `t = 0, 12, …, 12(m − 1)`, in advance and zero in the eleven months between each pair;
  maintenance expense at the start of each month, a twelfth of the annual amount, inflating
  once a policy year; renewal commission with the premium it is a percentage of; acquisition
  expense and initial commission at issue, the start of month `t = 0`; death claims and claim
  expenses at the **end** of the month of death; surrenders at the **end** of the month,
  **after** deaths, valued on the surrender value at that instant; the 払込満了 surrender surge
  as a one-off proportion in the single month `t = 12m`.
- **Rate conversion [std].** Mortality and ordinary surrender are quoted per annum and applied
  per month on the **effective** convention `r_m = 1 − (1 − r)^(1/12)`, so twelve months
  compound back to the annual rate exactly and survivorship at every anniversary is what an
  annual projection of the same bases produces. Three things are **not** converted, because
  they are not rates per unit time: the cliff surge, which is a decision taken on a date; the
  premium default that feeds the APL, which is the failure to pay one premium on one date; and
  the loan interest, which the 約款 capitalises once a year at the 契約応当日.
- **Age basis.** 契約年齢 is attained age (*man-nenrei*, 満年齢) with the fractional year discarded
  at 契約日, incrementing on each 年単位の契約応当日 rather than on the birthday [S1] [S3] [S9]. A
  projection stepped on anniversaries therefore steps the rating age correctly by
  construction, and the attained age in period `t` is `x + t` exactly — no select
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
  The projection runs to the **terminal age of the mortality table**, with ω = **109** for
  males and **113** for females on 生保標準生命表2018（死亡保険用）, the first age at which
  `q(ω) = 1.00000` [REG-R18] [R1]. On the monthly grid that is `T = 12(ω − x) + 1` months: the
  table's terminal rate is 1, so its monthly equivalent `1 − (1 − 1)^(1/12)` is 1 as well and
  every life still in force at the start of the terminal policy year dies in its **first
  month**. The frame stops at that month rather than carrying eleven rows of zeros after it.
  Nothing is paid there other than the death benefit, and `l(T) = 0`. There are no tail
  states.
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
| `premium_annual` (`P`) | JPY, level for policy years 1 … m | 174,960 |
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
| `pols_if(t)` | In-force probability at the **start** of month t; `pols_if(0) = 1` | monthly recursion |
| `mort_rate(t)`, `mort_rate_mth(t)` | Mortality rate (incl. 高度障害), annual and `1 − (1 − q)^(1/12)` | table lookup at `x + ⌊t/12⌋` |
| `lapse_rate(t)`, `lapse_rate_mth(t)` | Ordinary voluntary surrender rate, annual and per month | assumption table |
| `lapse_spike_rate(t)` | The 払込満了 surge: a one-off **proportion** in the single month `t = 12m`, never converted | model point |
| `default_rate(t)` | Premium-default rate, applied once per premium at an anniversary month (optional module; 0 in base) | model point |
| `pol_val_pp(d)` | `V(d)` — the ordinary, **unsuppressed** surrender value at anniversary d | closed form |
| `pol_val_at_m(u)` | `V(u)` — the same value at elapsed month u, linear between anniversaries **[std]** | interpolation |
| `cv_pp(d)`, `cv_at_m(u)` | The **payable** 解約返戻金, at an anniversary and at an elapsed month | closed form |
| `surr_charge_pp(d)` | `SC(d)` — the 解約控除 embedded in `pol_val_pp` | closed form |
| `reserve_pp(d)` | 平準純保険料式 policy reserve, reference quantity only — **never a cash flow** | closed form |
| `pols_if_pay(t)` | Of `pols_if(t)`, the premium-paying cohort; `pols_pay_bef_decr(t)` is that cohort after the month's defaults, and is the weight on premium and renewal commission | monthly recursion |
| `pols_if_apl(t, s)` | In-force probability on APL at the start of **month** t, having defaulted at **anniversary** s | monthly recursion |
| `loan_apl_pp(d, s)` | Outstanding APL principal and interest per policy in that cohort, at anniversary d; `loan_pp(d)` is the paying cohort's 契約者貸付 balance | annual recursion |

`pols_if_apl` and `loan_apl_pp` are indexed by the **entry anniversary `s`** and not collapsed
to a cohort average. That is deliberate: the APL exhausts at a duration that depends on when
the loan started, so an average balance would let early entrants ride on late entrants'
headroom and would move the termination by decades. The triangle is the honest structure.

Note which of the two moves monthly and which does not. The **population** on APL is
decremented every month like any other in-force population; the **balance** compounds once a
year, because the 約款 states a 年利 capitalised at the 契約応当日, and the continuation test
that spends it is the question the insurer asks when an annual premium goes unpaid. A benefit
in month `t` is therefore settled net of `loan_apl_pp(⌊t/12⌋, s)`.

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
| Premium `P` | Level and guaranteed for policy years 1 … m; none thereafter | [S1] [S3] [S7] [S10] |
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
| 契約者配当 | None — the composite is 無配当. Variant: 5年ごと利差配当, off in the base run, declaring `div_spread × div_period × V(d)` at every fifth anniversary `d` with `div_spread` = **0.25% p.a.** over `div_period` = **5** years | [S1] [S3] [S5] [S11]; variant [S7]; legal frame [REG-R9]; spread and period **[std]**, below |
| 払済保険 conversion basis | The insurer's own single-premium net rate `A(x+d)` at the conversion anniversary; not modelled in the base run | [S1] [S3] [S7] [S9] [S10] |

**Why `i_cv` is not 1.75%.** The 予定利率, 予定死亡率, 予定事業費率 and the surrender-value formula all
live in the 保険料及び責任準備金の算出方法書, a filed but unpublished 基礎書類 [REG-R2] — no amount of further
research turns them into sourced values. What *is* public is a complete numeric
surrender-value run for one model point [S4], and a second carrier's matched suppressed and
ordinary pair [S7]. The library therefore constructs `V(d)` in closed form and **calibrates
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
years of `V(d)`. The five-year period is not a standardization — it is in the product name
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
| Base table | 生保標準生命表2018（死亡保険用）, sex-distinct, `q` at attained age `x + t` | [REG-R18] [R1] |
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

The rows of `lapse_table.csv` are keyed by the **contractual policy year**, the 1-based label
`t + 1`, so the first projected period `t = 0` reads the `policy_year = 1` row:

| Policy year (`t + 1`) | 1 | 2 | 3 … m−1 | **m** | m+1 … |
|---|---|---|---|---|---|
| Period `t` | 0 | 1 | 2 … m−2 | **m−1** | m … |
| `lapse_rate(t)` **[std]** | 4% | 3% | 2% | **17%** | 2% |

The shape is reasoned, not fitted: a 低解約返戻金型 owner who surrenders during the low period
takes a 30% haircut on a value that is already below cumulative premiums (70.1% of premiums
paid at duration 5 on the published table [S4]), so early surrender is strongly suppressed;
at the anniversary `d = m` the value steps up by a factor of 1/k and crosses 100% of premiums
paid, and the product has been sold on exactly that crossing. The `m`-year entry is `2% + s`
with the
**cliff spike `s` = 15% [std]**, held as a separate parameter so that it can be switched off
and the sensitivity read directly.

**Premium default and the APL (optional module, off in the base run).**

| Input | Value | Basis |
|---|---|---|
| `default_rate(t)` | **0** in the base run; **1% p.a.** in policy years 1 … m, i.e. `0 ≤ t ≤ m − 1`, in the module | **[std]** |
| APL clawback on the defaulting cohort | On — the suppressed basis persists past `m` | [S3] [S4] [S5] [S9] |
| Reinstatement (復活) | Not modelled; every exit is terminal | **[std]**, below |

**Expenses and commission (levels all [std]; no carrier publishes an expense basis at all —
予定事業費率 is named in the 保険契約者保護機構 boilerplate [S1] [S7] and never quantified).**

| Input | Value |
|---|---|
| Acquisition expense `E0` | ¥50,000 per policy at issue **[std]** |
| Initial commission `c0` | 90% of the annual premium at issue **[std]** |
| Renewal commission `c_r` | 3% of premium, policy years 2 … m, falling in the anniversary months `t = 12, 24, …` with the premium **[std]** |
| Maintenance expense `e_m(t)` | ¥8,000 p.a. taken as ¥8,000/12 a month, **for life**, inflating 1.0% **a year** **[std]** |
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
| `t` | **0-based policy-month** index, t = 0 … T − 1; the contractual policy year is `y(t) = 1 + ⌊t/12⌋`; attained age in month t is `x + ⌊t/12⌋` |
| `d` | **anniversary** index in years, d = 0 … T_y, `d = 0` at issue; month t opens inside the policy year running from `d = ⌊t/12⌋` to `d = ⌊t/12⌋ + 1` |
| `u` | an **elapsed month** at which an interpolated value is read; `u = 12d` reproduces the anniversary value exactly |
| `x`, `T`, `T_y`, `ω` | 契約年齢 at issue; number of policy **months** projected, `T = 12(ω − x) + 1`; number of policy years, `T_y = ω − x + 1`; table terminal age |
| `m` | 保険料払込期間 in years (∞ for 終身払); `12m` is the month 払込満了 falls at |
| `SA`, `P` | 保険金額; annual premium, payable at the start of the months `t = 0, 12, …, 12(m − 1)` |
| `q(t)`, `w(t)` | **annual** mortality and ordinary surrender rates in month t; `q_m`, `w_m` are `1 − (1 − r)^(1/12)` |
| `s(t)`, `u(t)` | the 払込満了 surge, a one-off proportion in the month `t = 12m`; the premium-default proportion, applied once per premium |
| `l(t)` | in-force probability at the start of month t; `l(0) = 1` (`pols_if`) |
| `lp(t)` | of those, the part still **paying premium in cash** in month t, after that month's defaults into the APL state (`pols_pay_bef_decr`); `lp(t) = l(t)` in the base run |
| `D(t)`, `S(t)` | expected deaths in month t; expected surrenders in month t, ordinary plus any surge |
| `A(y)`, `ä(y, n)` | whole-life EPV of 1 at age y and n-year annuity-due, on `i_cv` and the table |
| `π` | net level premium on the cash-value basis, `SA × A(x) / ä(x, m)` |
| `W(d)` | prospective net level premium policy value at anniversary d |
| `SC(d)` | 解約控除 — acquisition-cost deduction (`surr_charge_pp`) |
| `V(d)` | ordinary, unsuppressed surrender value (`pol_val_pp`) |
| `k` | 解約払戻金支払割合 — 0.70 when 低解約返戻金型 is on, 1.00 otherwise |
| `CV(d)`, `CV*(d)` | payable 解約返戻金 (`cv_pp`); the value the APL test runs on (`apl_test_val`) |
| `cumprem(d)` | premiums paid per policy by anniversary d, `P × min(d, m)`; `cumprem(u) = P × min(⌈u/12⌉, m)` at an elapsed month, a **step** function because the premium is annual |
| `L(d)` | loan + APL principal and interest at anniversary d; it compounds once a year, so a benefit in month t is settled net of `L(⌊t/12⌋)` |
| `i_cv`, `i_L`, `i_std` | cash-value basis rate; loan rate; reference valuation rate |
| `α` | acquisition-deduction rate, per unit of `SA` |
| `E0`, `e(t)`, `c0`, `c_r`, `ec` | acquisition expense; maintenance; initial and renewal commission; claim expense |
| `CF(t)` | net cash flow of month t, **income-positive** (`net_cf`) |

**Dimensional check.** `q`, `w`, `s`, `u`, `k`, `α`, `c0`, `c_r`, `l` and `lp` are
dimensionless — but `q` and `w` are rates **per year** while `q_m`, `w_m`, `s` and `u` apply to
a **month**, and the last two are applied unconverted because they are proportions rather than
rates. `i_cv`, `i_L`, `i_std` are per annum; `A` and `ä` are pure numbers (`ä` in years of
premium, so `SA × A / ä` is ¥ per year, which is what makes `P` an annual amount); `SA`, `P`,
`W`, `SC`, `V`, `CV`, `L`, `E0`, `ec` are ¥ and `e_m` is ¥ per **month**; every term of
`CF(t)` is ¥ per policy issued per **month**. No term mixes a per-annum rate with a stock
without an explicit period count.

### 責任準備金 and 解約返戻金 — two quantities, one relationship

They are different objects and a model that conflates them is wrong in both directions.

**責任準備金** is statutory. For an in-scope contract — and
a level-premium 終身保険 with a fixed 予定利率 is in scope [R6] [REG-R7] — it is accumulated
net level premium method (*heijun jun-hokenryō-shiki*, **平準純保険料式**), with **no Zillmer
adjustment**, on the standard valuation rate (*hyōjun riritsu*, 標準利率) and
生保標準生命表2018（死亡保険用）[R7] [R8] [REG-R10] [REG-R11]:

    π*        = SA × A*(x) / ä*(x, m)                     on (i_std, 標準生命表2018)
    reserve_pp(d) = SA × A*(x + d) − π* × ä*(x + d, max(m − d, 0))

**解約返戻金** is contractual. Its formula is in the unpublished 算出方法書 [REG-R2]; what the 約款
publish is its argument list — elapsed months and paid months, the elapsed count capped at
the paid count while premiums are due [S1] [S3] [S10]. The library constructs it as a policy
value of the **same form** on a **different basis**, less a 解約控除 grading to zero **[std]**:

    π         = SA × A(x) / ä(x, m)                       on (i_cv, 標準生命表2018)
    W(d)      = SA × A(x + d) − π × ä(x + d, max(m − d, 0))
    SC(d)     = α × SA × max(0, m − d) / m
    V(d)      = max(0, W(d) − SC(d))

all four **at the anniversary `d`**, `d = 0` at issue: `W(0) = 0` by construction and
`W(T) = 0` because the table terminates.

The relationship is then exact and testable. **When the two basis rates coincide** (`i_std =
i_cv`, which is the base-run default so that the identity can be asserted),

    reserve_pp(d) − V(d) = SC(d)          for every anniversary d ≥ 1

— the whole difference is the 解約控除, which is precisely what 平準純保険料式 forbids the reserve to
carry [REG-R10]. (At `d = 0` both sides are zero: the reserve is nil and the floor in `V`
absorbs `SC(0)`, which is what `check_reserve_identity_resid` tests.) **When they do not
coincide the ordering can fail**: with a 標準利率 below the
pricing basis the statutory reserve exceeds the cash value by far more than `SC(d)`, and in
a deep negative-spread (逆ざや) configuration the reserve can exceed even the sum assured.
`reserve_pp ≥ V ≥ CV` is therefore **not** a model invariant and must not be asserted as
one. `reserve_pp` produces no cash flow; it exists so the identity above can be checked.

### The 低解約返戻金型 cliff

    CV(u) = k × V(u)     for u <  12m     (k = 0.70 when 低解約返戻金型 is on)
    CV(u) =     V(u)     for u >= 12m

and the transition at the anniversary `d = m` is a **step**, not a ramp. Two carriers' published tables
agree on it to rounding, and one of them settles what the suppression *is*: at duration 40,
well past 払込満了, the suppressed and ordinary products have **identical** surrender values
[S7]. So there is **one** `V(d)` and **one** multiplier — not two reserve runs. Everything
derived from the surrender value is suppressed with it: the 払済保険金額, the 契約者貸付 amount and the
APL amount are all computed off `CV(d)` [S7] [S9] [S11].

Two quantities coexist at the anniversary `d = m` and a model must publish both: `k × V(m)`,
the value an instant before the step (the published ¥2,047,650 figure), and `CV(m) = V(m)`,
the value an instant after (¥2,928,450) [S4]. The ratio `CV(m) / (k × V(m))` must equal
exactly `1 / k`; anything between is an interpolation the contract does not have.

**The monthly grid puts the step where the contract puts it, and retires a [std] in doing
so.** On an annual step the step and the grid landed on the same year, so the notes had to
rule that a surrender anywhere in policy year `m` was paid at the anniversary `d = m` on the
**full** value — an ordering convention, not a reading of the clause. Here the suppression
ends at the elapsed month `u = 12m`: a surrender at `u = 12m − 1` is still inside the
保険料払込期間 and is paid `k × V(u)`, and one at `u = 12m` is not and is paid `V(m)`. Eleven of
the twelve months of policy year `m` move from the post-step side to the pre-step side, and on
the anchor cell that is the single largest difference between the two grids.

The **behavioural surge** moves with it. The 15% spike **[std]** is not a rate spread over a
year but the proportion of owners who were waiting for the step, so it falls as a one-off in
the single month **after** the last premium, `t = 12m`, beside the step that provokes it — on
the anchor cell, month 180, where the surrender outgo is ¥313,122.87 against ¥3,480.77 the
month before. The annual grid put the surge in policy year `m`, which is a year *before* the
event that causes it.

### 自動振替貸付 as a state

Where the premium is unpaid at grace expiry and there is a surrender value, the insurer
**lends the premium against that value and applies it to the premium**, and the contract
continues in force [S1] [S3] [S7] [S10] [S11]. Lapse on this chassis is therefore a **funded
event, not a behavioural one**. The trigger, stated the same way at three carriers [S1] [S3] [S10], is an **annual** test —
one annual premium, one 契約応当日 — and stays annual on the monthly grid:

    the APL fires at anniversary d  iff   CV*(d + 1) >= L(d) + P × (1 + i_L)

where `CV*(d)` is the surrender value computed **as if the premium had been paid**, and the
anniversary that matters is the one the advanced premium would carry the contract to, `d + 1`
**[std]**; `L(d)` is the existing balance at `d`. The accumulation is compound, with interest
capitalised into principal at each subsequent grace expiry, annually on a 年払 contract
[S3] [S7]:

    L(d + 1) = (L(d) + A(d)) × (1 + i_L),      A(d) = P if the APL fires and d < m, else 0

Once `d >= m` no premium is due, so `A(d) = 0` and the balance rolls up on interest alone
against a value that is still growing, which is why exhaustion after 払込満了 takes decades
rather than years.

What the monthly grid changes about this module is the **population**, not the ledger: the
cohort on APL is decremented every month like any other in-force population, while its
balance and its test move once a year. A benefit falling in month `t` is settled net of
`L(⌊t/12⌋, s)`, the balance actually outstanding at the anniversary that opened its policy
year.

**Exhaustion.** If the test fails at anniversary `d`, the contract lapses in the month
`t = 12d` and the policyholder may claim the surrender value net of the loan [S1] [S3] [S10]
— the value at that anniversary, which is the last one the loan had not yet overtaken:

    benefit on APL failure = max(0, CV*(d) − L(d))

floored at zero, because the loan can exceed the value. The same test, with `A(t) = 0`, is
the **loan-excess termination** the 約款 describe for a 契約者貸付 that outgrows the value [S1]
[S3] [S10]; the notice-and-top-up period is not modelled **[std]**.

**The clawback.** Where not all premiums falling in the suppressed period were paid, the
suppressed basis continues to apply after the period ends [S3] [S4] [S5] [S9]. A cohort
carried through the low period by APL advances has by definition not paid them, so **[std]**
the APL cohort's value is `k × V(d)` for **all** `d` — it never steps up at `m`. This is not
a refinement; it moves the exhaustion by sixteen years on the anchor cell (below).

### Processing order (month t = 0 … T − 1)

1. **Start of month — premium.** Collect `P × lp(t)` in the anniversary months
   `t = 0, 12, …, 12(m − 1)`, and nothing in the eleven between each pair. On the APL cohort
   the premium is **not** collected in cash: the advance is applied to it, so it produces no
   `net_cf` entry and appears only as growth in `L`. That is why the weight here is `lp(t)`
   and not `l(t)` — the APL cohort is in force and not paying.
2. **Start of month — expenses.** `e_m(t) × l(t)`, a twelfth of the annual amount inflating
   once a policy year; renewal commission `c_r × P × lp(t)` in the same anniversary months as
   the premium, for policy years 2 … m. At `t = 0` additionally `E0` and `c0 × P` (per policy
   issued, `l(0) = lp(0) = 1`).
   Maintenance is carried on the whole in-force population `l(t)`, because the APL cohort
   still has to be administered; commission follows the premium **actually collected**, so
   it is carried on `lp(t)` **[std]**.
3. **At an anniversary month — premium default and the APL test** (module on). The default
   proportion `u` is applied once per premium, never spread; for each entry cohort, apply the
   trigger above and advance or terminate.
4. **Cash values.** Read `V(t + 1)` and `CV(t + 1)` at the end of the month, interpolating
   between the anniversaries that bracket it **[std]**.
5. **End of month — deaths.** `D(t) = l(t) × q_m(t)`; outgo `(SA − L(⌊t/12⌋)) × D(t)`, floored
   at zero; claim expense `ec × D(t)`.
6. **End of month — ordinary surrenders**, applied to survivors of mortality **[std order:
   death before lapse]**: `l(t) × (1 − q_m(t)) × w_m(t)`.
7. **End of month — the cliff surge**, applied to the survivors of *that*, and only in the
   month `t = 12m`: `l(t) × (1 − q_m(t)) × (1 − w_m(t)) × s(t)`. Both exits are paid
   `max(0, CV(t + 1) − L(⌊t/12⌋))`, and `S(t)` is their sum.
8. **At an anniversary — loan roll-up.** `L(d + 1) = (L(d) + A(d)) × (1 + i_L)`.
9. **Update in force.**

       l(t + 1) = l(t) × (1 − q_m(t)) × (1 − w_m(t)) × (1 − s(t))

   Because the two conversions are the effective ones, `l` at every anniversary is exactly
   what an annual projection of the same bases gives — the arithmetic check that the grid
   changed and the basis did not.
10. **At `t = T − 1`**, the first month of the terminal policy year, the table's rate is 1 and
    so is its monthly equivalent, so `l(T) = 0` and the projection ends. No maturity payment,
    no tail states.

### Net cash flow

Income-positive, per policy issued:

    CF(t) = P × lp(t) × 1{t mod 12 = 0 and t < 12m}       (premiums, once a year)
          − (SA − L(d)) × D(t)                            (death and 高度障害 claims)
          − ec × D(t)                                     (claim expense)
          − max(0, CV(t + 1) − L(d)) × S(t)               (surrender benefits)
          − e_m(t) × l(t)                                 (maintenance expense)
          − c_r × P × lp(t) × 1{t mod 12 = 0, 12 <= t < 12m}   (renewal commission)
          − (E0 + c0 × P) × 1{t = 0}                      (acquisition)

with `d = ⌊t/12⌋`, the anniversary that opened the month's policy year.

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

    Σ_t D(t) + Σ_t S(t) = 1     and     l(T) = 0

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

      w_dyn(t) = w(t) × min(3.0, max(1.0, 1 + β × max(0, CV(t+1) / cumprem(t+1) − 1)))

  with `β` = 2.0 **[std]** and `cumprem(d) = P × min(d, m)`, both read at the anniversary
  `d = t + 1` that closes the period, which is where the surrender is paid. On the anchor cell the ratio
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
  Where it is non-zero, the loan is drawn at the anniversary `d` to `pol_loan_util × CV(d)`,
  subject to the contractual 9/10 (in payment) and 8/10 (paid-up) caps [S1] [S3] [S7],
  accrues at `i_L`, and nets off every benefit.
- **払済保険 election.** Modelled as an election at a chosen anniversary `d`: the contract stops
  paying premiums, `SA` is replaced by `(CV(d) − L(d)) / A(x + d)` on the insurer's own single-
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
for exactly this cell [S4]). `T = 109 − 30 + 1 = 80` policy years, so the frame is
`t = 0 … 79` and the attained ages are 30 to 109.

Assumption values used, in full: `q` from 生保標準生命表2018（死亡保険用）男 [REG-R18] [R1] with
`mort_be_factor = 1.00` — **q(30) = 0.00068, q(31) = 0.00069, q(32) = 0.00070, q(33) =
0.00072, q(34) = 0.00074**, all five **anchor rows** of `mort_table.csv`, read from the
publisher's PDF and quoted here because the worked example needs them; `lapse_rate` = 4% /
3% / 2% … 2% **[std]**, with the 15% cliff surge held apart as a one-off proportion in the
single month `t = 180`;
`default_rate` = 0 (base run); `E0` =
¥50,000, `c0` = 0.90, `c_r` = 0.03, `e(t)` = ¥8,000 × 1.01^t, `ec` = ¥20,000, all
**[std]**; `i_cv` = 1.468%, `α` = 0.0090, `k` = 0.70; `i_L` = 2.75%, unused
in the base run because `loan_pp ≡ 0`.

### Calibration of the cash-value construction

`π = SA × A(30) / ä(30, 15)` on `i_cv` = 1.468% and the shipped male table gives `A(30) =
0.47678817`, `ä(30, 15) = 13.49765934`, so **π = ¥176,618.83**. `i_cv` was solved so that
`V(15) = SA × A(45)` reproduces the published post-step value, and `α` was set to a round
0.0090 — an initial deduction `SC(0)` of ¥45,000, 25.7% of one annual premium — grading
linearly to `SC(15) = 0`. The fit against the eight published points [S4] is then, by
**anniversary** (`d`, equivalently the duration in completed policy years):

| duration `d` | model `CV(d)` | published 解約払戻金 | difference | model 払戻率 | published 払戻率 |
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
and `SC(d)` absorbs the difference. It reproduces the contractual **value**; it is not a
pricing model and `π` is not the priced net premium.

### First months of the base run

Per policy issued, income-positive, to two decimal places. The index is the 0-based **policy
month** `t`; the contractual policy year is `y(t) = 1 + ⌊t/12⌋`, and `CV(t + 1)` below is the
interpolated surrender value at the end of the month **[std]**, which is the amount a
surrender there is paid.

| t | y(t) | age | `pols_if(t)` | premiums | claims_death | claims_lapse | claim_exp | expenses | commissions | net_cf | `CV(t+1)` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 30 | 1.000000 | 174,960.00 | 283.42 | 26.53 | 1.13 | 50,666.67 | 157,464.00 | −33,481.75 | 7,812.66 |
| 1 | 1 | 30 | 0.996547 | 0.00 | 282.44 | 52.88 | 1.13 | 664.36 | 0.00 | −1,000.82 | 15,625.31 |
| 2 | 1 | 30 | 0.993107 | 0.00 | 281.47 | 79.04 | 1.13 | 662.07 | 0.00 | −1,023.71 | 23,437.97 |
| 11 | 1 | 30 | 0.962671 | 0.00 | 272.84 | 306.48 | 1.09 | 641.78 | 0.00 | −1,222.20 | 93,751.86 |
| 12 | 2 | 31 | 0.959347 | 167,847.39 | 275.90 | 253.75 | 1.10 | 645.96 | 5,035.42 | +161,635.25 | 104,344.55 |
| … | | | | | | | | | | | |
| 179 | 15 | 44 | 0.706653 | 0.00 | 480.29 | 3,480.77 | 1.92 | 541.52 | 0.00 | −4,504.50 | 2,928,631.87 |
| **180** | **16** | 45 | 0.705369 | 0.00 | 520.63 | **313,122.87** | 2.08 | 545.94 | 0.00 | **−314,191.52** | 2,931,914.84 |
| 181 | 16 | 45 | 0.598466 | 0.00 | 441.73 | 2,954.44 | 1.77 | 463.20 | 0.00 | −3,861.14 | 2,935,197.82 |

`expenses` is **acquisition and maintenance only** and the claim handling expense stands
beside it in its own `claim_expenses` column, which is the settled column vocabulary across
the three libraries; the `dividends` column is zero throughout on this cell and is omitted.

**Two columns are non-zero in one month out of twelve**, and that is the shape of a 年払
contract rather than an artefact: the premium and the renewal commission fall at the
anniversary and nowhere else, while claims, surrenders and maintenance run every month
against them.

The **anniversary** surrender values are the same numbers the annual-grid model published,
because the value construction did not move: `CV(1)` = 93,751.86, `CV(2)` = 220,864.08,
`CV(3)` = 349,867.80, `CV(4)` = 480,764.69, `CV(5)` = 613,589.14, `CV(14)` = 1,896,979.14,
`CV(15)` = 2,928,631.87, `CV(16)` = 2,968,027.59. What is new is the reading between them —
`CV(1)` at the elapsed month 1 is ¥7,812.66, a twelfth of the way from a first-anniversary
value of nil to ¥93,751.86, which is what "解約返還金がない場合があります" in the first months
[S1] looks like on a grid fine enough to show it.

**Trace, `t` = 0 (the first policy month).** `q(0) = 0.00068` is the annual table rate and
`q_m(0) = 1 − (1 − 0.00068)^(1/12) = 0.0000566843` the decrement applied, so
`D(0) = 0.0000566843`; death claims = 5,000,000 × 0.0000566843 = 283.42; claim expense =
20,000 × that = 1.13. Survivors of mortality = 0.9999433157, and
`w_m(0) = 1 − (1 − 0.04)^(1/12) = 0.0033960532`, so `S(0) = 0.9999433157 × 0.0033960532 =
0.0033958607`. `V(0) = max(0, W(0) − SC(0)) = max(0, −45,000) = 0` and
`V(1) = 175,931.231 − 42,000 = 133,931.231`, so the interpolated `V` at elapsed month 1 is
`133,931.231 / 12 = 11,160.94` and `CV(1) = 0.70 × 11,160.94 = 7,812.66`; surrender benefits
= 7,812.66 × 0.0033958607 = 26.53. Expenses = 50,000.00 + 8,000/12 = 50,666.67; commission =
0.90 × 174,960 = 157,464.00. `CF(0) = 174,960.00 − 283.42 − 1.13 − 26.53 − 50,666.67 −
157,464.00 = −33,481.75`. Update: `l(1) = 1 × 0.9999433157 × 0.9966039468 = 0.996547`.

**Trace, `t` = 12 (the first month of policy year 2).** The premium falls again — one of the
twelve months that carry it — at `174,960 × 0.959347 = 167,847.39`, and the renewal
commission with it at `0.03 × 167,847.39 = 5,035.42`. The attained age steps to 31, so
`q(12) = 0.00069` and `q_m(12) = 0.0000575182`; claims = 275.90. The lapse rate steps to 3%,
so `w_m(12) = 0.0025350`, and surrender benefits = 253.75 on the interpolated value
¥104,344.55. Maintenance = `(8,000 / 12) × 1.01 × 0.959347 = 645.96`.
`CF(12) = 167,847.39 − 275.90 − 1.10 − 253.75 − 645.96 − 5,035.42 = +161,635.25`.

**Trace, the cliff at `t` = 180 — one month wide.** 払込満了 is the anniversary `d = 15`, which
is the elapsed month 180. `l(180) = 0.705369`; the ordinary surrender decrement of that month
takes 0.001186355 and the **cliff surge** takes a further 0.105611722 — 15% of the survivors
of it, in one month, as a one-off proportion and not a rate. Both are paid the **post-step**
value at the end of the month, `CV(181) = 2,931,914.84`, so surrender benefits =
`0.106798077 × 2,931,914.84 = 313,122.87` and
`CF(180) = −520.63 − 2.08 − 313,122.87 − 545.94 = −314,191.52`. The month before produced
−4,504.50 and the month after −3,861.14.

**The cliff is the largest single feature of this cash-flow stream and on this grid it is one
month wide.** The annual grid could say it cost a year and could not say what a month of it
looked like. Two things it also gets right that the annual grid had to approximate. The
eleven months of policy year 15 that close *before* 払込満了 are inside the 保険料払込期間 and are
paid the **suppressed** value — a surrender at the end of month 178 gets
`CV(179) = 2,037,287.04`, and one a month later gets `CV(180) = 2,928,631.87`, the step itself
— where the annual grid paid the whole of policy year 15 post-step under a stated
**[std ordering]** rule. And the surge falls **after** the step rather than in the year before
it. The ratio the
implementation must reproduce exactly is still `CV(15) / (0.70 × V(15)) = 1.4285714286 =
1 / 0.70`.

**Roll-forward check.** Over the full 949 months, `t = 0 … 948`, `Σ D(t) = 0.303360114` and
`Σ S(t) = 0.696639886`, summing to **1.000000000**, with `l(T) = 0`. Undiscounted totals per
policy issued: premiums 2,212,542.21; death claims 1,516,800.57; claim expenses 6,067.20;
surrender benefits 1,667,588.91; expenses 326,003.34; commission 218,591.47; `Σ CF(t)` =
**−1,522,509.28**. Undiscounted, the contract loses money; discounting is out of scope and
is what makes the sign meaningful.

**Why the totals moved, and why the premium did not.** Premium income is *identical* to the
annual grid's ¥2,212,542.21, because the premium is annual and falls at the same anniversaries
on the same survivorship. What moved is the benefit side, and almost all of it is the cliff
ruling: claims are settled in the month they arise rather than at a year-end, and eleven
twelfths of policy year 15's surrenders are now paid the suppressed value. The undiscounted
result improves by ¥37,326.01, 2.4% of it.

**The same statement by policy year.** `result_cf()` grouped on `⌊t/12⌋`, with `l` read at the
anniversary. Note where the cliff sits: policy year **16**, the year opened by 払込満了, and not
policy year 15.

| y − 1 | `l` | premiums | claims_death | claims_lapse | claim_exp | expenses | commissions | net_cf |
|---|---|---|---|---|---|---|---|---|
| 0 | 1.000000 | 174,960.00 | 3,337.21 | 2,017.67 | 13.35 | 57,849.82 | 157,464.00 | −45,722.06 |
| 1 | 0.959347 | 167,847.39 | 3,263.99 | 4,668.65 | 13.06 | 7,641.95 | 5,035.42 | +147,224.31 |
| 2 | 0.929925 | 162,699.62 | 3,224.80 | 5,401.15 | 12.90 | 7,516.71 | 4,880.99 | +141,663.08 |
| 13 | 0.736765 | 128,904.33 | 5,511.41 | 26,907.95 | 22.05 | 6,641.76 | 3,867.13 | +85,954.04 |
| 14 | 0.720939 | 126,135.49 | 5,821.61 | 29,562.69 | 23.29 | 6,563.72 | 3,784.06 | +80,380.12 |
| **15** | 0.705369 | 0.00 | 5,335.43 | **345,505.53** | 21.34 | 5,594.79 | 0.00 | **−356,457.10** |
| 16 | 0.586532 | 0.00 | 5,666.09 | 35,031.24 | 22.66 | 5,446.56 | 0.00 | −46,166.56 |

### 自動振替貸付 trace (module on)

The premium plus a year's interest is `P × (1 + i_L) = 174,960 × 1.0275 = ¥179,771.40`. The
whole module is on the **anniversary** clock — one annual premium, one 契約応当日, one test —
so it reads exactly as it did on the annual grid, and every number in this trace is
unchanged. Take a policy that stops paying at the anniversary `s`, with `L(s) = 0`.

**s = 1 (the anniversary opening policy year 2, the month `t = 12`), 低解約返戻金型 on
(k = 0.70).**

    d = 1:  CV*(2) = 0.70 × 315,520.1189 = 220,864.08  >=  0 + 179,771.40       -> fires
            L(2) = (0 + 174,960) × 1.0275 = 179,771.40
    d = 2:  CV*(3) = 0.70 × 499,811.1402 = 349,867.80  <  179,771.40 + 179,771.40
                                                       = 359,542.80             -> fails
            lapse in the month t = 24; benefit = max(0, CV*(2) − L(2))
                                              = 220,864.08 − 179,771.40 = 41,092.68

**One advance.** The same default on the **ordinary** form (`k` = 1.00) passes at `d = 2`
(499,811.14 ≥ 359,542.80) and goes on passing: it takes **thirteen** advances, carrying the
policy to `d = 13` and failing at `d = 14` — the month `t = 168` — where
`L(14) + P × (1 + i_L)` = 2,764,330.63 + 179,771.40 = 2,944,102.03 finally exceeds
`CV*(15)` = 2,928,631.87 — reaching the last
premium year all but intact and then paying nothing, because the loan has consumed the
value. **One advance against thirteen, from the same default, at the same duration, on the
same underlying policy value.** That is what running the APL test against 70% of the value
rather than against the value does, and it is why a 低解約返戻金型 contract is simultaneously the
one with the strongest incentive to persist to 払込満了 and the one with the least headroom to
get there.

The first anniversary at which the APL can fund a single premium is `d = 1` on both forms
(`CV(1)` is 93,751.86 suppressed and 133,931.23 unsuppressed, both under 179,771.40): in the
first policy year the APL cannot carry the policy at all, on either form.

**The clawback, priced.** A policy defaulting at `s = 9` (the anniversary opening policy year
10) takes six advances, `d = 9 … 14`, policy years 10 … 15; after `m` no premium is due and
the balance rolls up on interest alone. With the clawback applied — the correct treatment,
since the cohort did not pay its low-period premiums — its value stays at `0.70 × V(d)` for
ever and the loan overtakes it at `d` = **52**, the month `t` = 624. With the clawback wrongly
omitted, the value steps up at `m` and the same policy survives to `d` = **68**.
**Sixteen years of in-force, on one boolean.**

What the monthly grid changes here is only *when the population leaves*: the cohort is
decremented month by month while it is carried, and it terminates in the single month
`12 × apl_fail_year(s)` rather than being attributed to a year.

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
   entire surrender-benefit stream, which totals ¥1,667,589 against ¥2,212,542 of
   undiscounted premium income on the anchor cell — the largest outgo line after death
   claims. They are
   calibrated to one carrier's published table for one model point [S4]; the fit at other
   issue ages, sexes and payment terms is **unverified**, because no carrier publishes a
   second complete run. A user with a real 算出方法書 replaces `pol_val_pp` and changes nothing
   else.
2. **The cliff surge `s`.** 15% **[std]**, with no public data of any kind behind it. It moves
   the surrender outgo of the single month `t = 12m` linearly and it is the assumption a
   reviewer should challenge first. Setting `s = 0` removes it cleanly. On the monthly grid it
   is visibly a one-off proportion rather than a rate, which is worth knowing before
   calibrating it against anything expressed per annum.
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
   death claims on the anchor cell fall after policy year 40, i.e. from the month `t = 480`.
   Any truncation of the projection is a direct understatement.
7. **Expense inflation over eighty years.** 1.0% **[std]** compounds to a factor of 2.19
   over the run; 3% compounds to 10.33. There is no published Japanese expense basis to
   anchor either.
8. **復活.** Not modelled, so in force after a lapse is understated. Japanese policies come
   back for three years [S1] [S3] [S7] [S10]; the UK reference set's terminal lapse is not
   the right intuition here.

Known modeling pitfalls:

- **The cliff is a step, not a ramp.** `CV(d) = k × V(d)` for `d < m` and `V(d)` for `d >=
  m`, with `CV(m) / (k × V(m))` exactly `1 / k` [S3] [S7] [S9] [S11]. Interpolating, grading
  or smoothing across the boundary is wrong; so is a 終身払 point, for which `m` is infinite
  and the step never happens [S4].
- **Off-by-one at the boundary — and the monthly grid moves where it falls.** The suppression
  ends at the elapsed month `12m`, so a surrender settled at `u < 12m` is paid `k × V(u)` and
  one settled at `u >= 12m` is paid `V(u)`. Eleven of the twelve months of policy year `m`
  close before 払込満了 and are therefore paid the **suppressed** value; only the last of them
  closes on the step. The annual grid, which could not draw that line, ruled **[std ordering]**
  that the whole of policy year `m` was paid post-step. Both quantities exist at `d = m` and
  the published table prints both — ¥2,047,650 an instant before and ¥2,928,450 an instant
  after [S4] — so a model must be able to produce both and must not lose either.
- **One policy value, one multiplier.** The suppression is a pure haircut on a common
  underlying value: at the anniversary `d = 40` the suppressed and ordinary products have identical
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
- **The APL test runs on the suppressed value.** `CV*(d)`, not `V(d)`. On the anchor cell a
  default at `s = 1` — policy year 2 — buys **one** advance at `k = 0.70` and **thirteen** at
  `k = 1.00`; running the test on `V` overstates headroom by more than a decade of in force
  [S7] [S9] [S11].
- **The clawback survives the step.** A cohort carried through the low period by unrepaid
  APL advances keeps the suppressed basis after `m` [S3] [S4] [S5] [S9]. On the anchor cell
  that is the difference between exhaustion at the anniversary `d = 52` and at `d = 68` —
  the months `t = 624` and `t = 816`.
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
- **Everything is floored at zero.** `V(d) = max(0, W(d) − SC(d))` is negative in principle
  at the issue anniversary `d = 0`; the death benefit `SA − L(d)` and the surrender benefit
  `CV(t + 1) − L(d)` can
  both go negative once a loan has outgrown the value [S1] [S3] [S10]. None of them may
  produce a negative payment.
- **`reserve_pp` is not `cv_pp`.** 平準純保険料式 admits **no Zillmer adjustment** [REG-R10], so
  the statutory reserve carries no 解約控除; `reserve_pp(d) − V(d) = SC(d)` holds **only** when
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
