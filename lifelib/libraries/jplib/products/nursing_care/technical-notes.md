# Technical Notes

**Status:** Draft, 2026-08-20 (all cited sources accessed 2026-08-20).

**Scope note.** These notes turn the standardized composite of `product-spec.md` (same
directory) into a reference liability cash-flow projection model on paper. They describe no
single insurer's product. [S#] and [R#] tags resolve in `sources.md`, whose numbering is
carried verbatim from `_research/nursing-care.md` and is frozen; [REG-R#] tags resolve in
the cross-product reference library `references/regulatory-and-actuarial-references.md`,
whose R-numbering is separate. **[std]** marks a standardization introduced for the
reference implementation, always with a rationale and, where one exists, the observed range;
[unverified] marks a claim not confirmed against a retrieved document. **Every contractual
parameter value here is identical to `product-spec.md`'s.** Five quantities appear here that
`product-spec.md` does not carry, because they are modelling constructs rather than
contractual terms and are introduced below as such: the **certification prevalence curve**,
the **prevalence-to-incidence conversion**, the **care-state mortality multiple**, the
**recovery rate**, and the **sub-65 specified-disease (*tokutei shippei*, 特定疾病) gate**.

**This document states its deltas against
[the medical technical notes](../medical/technical-notes.md), the `jplib` third-sector
chassis, whose model is [`Medical_JP_S`](../medical/model.md).** It inherits that file's
monthly grid, its timing conventions, its age basis, its mortality construction from the
third-sector (*dai-san-bun'ya*, 第三分野) standard table 第三分野標準生命表2018, its lapse table,
its expense
structure and its whole-of-life horizon. It replaces the chassis's benefit machinery
outright. `medical` is **frequency × severity × limit**: a daily amount (*nichigaku*, 日額)
multiplied by paid days, capped per hospitalization and again in aggregate, with two day
ledgers that on the expectation never bind. Nursing care is **incidence into an absorbing
state**: a lump sum on first entry, an annuity while the insured survives after entry, a
premium waiver from a *lower* entry threshold than either, and a payment counter that
**does** bind. There is no `d_pay`, no `d_ben`, no `L1`, no `LA` and no `agg_days_*` ledger
anywhere in this model. What replaces them is a three-state chain — healthy, in care, dead —
whose entry is certified by a municipality and whose exit, in the base run, is only death.

**And the incidence basis is public, which is unique in this library.** `medical` had to
construct incidence from 患者調査 prevalence and a mean length of stay; `uklib` has no public
long-term-care morbidity series at all. Japan publishes a **national census of certified
persons** every year, split by sex, age band and all seven certification grades [R4] [R5]
[REG-R30]. That census is a **prevalence**, not an incidence, and converting one to the
other is the whole modelling problem of this product. Section (c) does it explicitly.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows for a single-policy model
  point of private nursing-care insurance (*kaigo hoken*, 介護保険) on the public-scheme-linked
  (*kōteki kaigo hoken rendō-gata*, 公的介護保険連動型) design: office premiums, care lump sum
  (*kaigo ichijikin*, 介護一時金), care annuity (*kaigo nenkin*, 介護年金), maintenance and claim
  expenses, and commission. The intended sense is the current estimate (*genzai suikei*,
  **現在推計**) the economic-value solvency regime requires — probability-weighted future cash
  flows on assumptions re-set at a stated reporting date (*kijunbi*, 基準日) rather than locked
  in at issue [REG-R15] — and it is also the shape of the 1号収支分析, a forward income-and-outgo
  projection over at least ten future years by 区分経理 segment [REG-R22].
- **Out of scope, cited not reproduced.** Discounting, MOCE, required capital and every
  reserving basis. Standard policy reserve (*hyōjun sekinin-junbikin*, 標準責任準備金), contingency
  reserve (*kiken junbikin*, 危険準備金) including its separately identified third-sector limb,
  the ESR balance sheet and IFRS 17 all consume these cash flows and are pointed at in
  *Valuation and reserve pointers*, not computed here.
- **Projection frequency.** Monthly grid, inherited from the chassis. The unit of account
  here is not a day but an **annual annuity instalment**, and the composite's premium mode
  is monthly (月払) — the mode of every published rate table retrieved [S6] [S8], though
  半年払 and 年払 are also offered [S1]. `t` is the **policy month**,
  `t = 0, 1, …, proj_len − 1`, and month `t` runs from `t` to `t + 1` months after the
  contract date (*keiyakubi*, 契約日).
- **Timing conventions [std].** Office premium received at the **start** of month `t`, and
  only by lives not yet on premium waiver (*hokenryō haraikomi menjo*, 保険料払込免除); maintenance
  expense at the start of month `t`; the lump sum, the annuity instalment and the
  claim-handling expense at the **end** of month `t`; then care incidence, then mortality,
  then lapse, then benefit-driven termination. Acquisition expense and initial commission at
  `t = 0`. The annuity is paid **in advance**: the first instalment falls on the entry month
  itself, not a year later [S1] [S7].
- **Claim-date convention [std].** A certification of need for nursing care (*yō-kaigo
  nintei*, 要介護認定) takes effect **retroactively to the application date**, with the decision
  due within 30 days [R1]. The model dates every claim at the month the trigger is *met*,
  not at notification, which is the contractually correct date and is up to a month earlier
  than a notification-dated projection.
- **Age basis.** Attained age at 契約日 with the fraction discarded (*man-nenrei*, 満年齢),
  incremented at each 年単位の契約応当日 [S1]. `age(t) = x + floor(t / 12)`, `x` the 契約年齢.
  第三分野標準生命表2018 is built for an insurance age (*hoken-nenrei*, 保険年齢) 方式 — nearest
  birthday — basis [REG-R20], so reading it at
  満年齢 understates the valuation age by about half a year; `jplib` accepts the offset in the
  base run and marks it **[std]**, exactly as `medical` does.
- **Currency.** JPY throughout. Expected values are fractional and displayed to ¥0.01.
- **Model points.** One policy at a time on an expected (probability-weighted) basis;
  `Projection` is parameterized by `point_id`. No aggregation logic is specified here.
- **Termination.** Whole-of-life cover with whole-of-life premiums [S1] [S4] [S7] [S8] [S10]
  [S11]. The projection runs to the terminal age of 第三分野標準生命表2018, **116 for males and 118
  for females** [REG-R18] [REG-R20], so `proj_len = 12 × (terminal_age − x + 1)` — 684
  months for the anchor cell. There is no maturity benefit, no 死亡保険金 and no surrender value
  (*kaiyaku-henreikin*, 解約返戻金), so death and lapse are pure liability-releasing
  decrements.
  There **is** a benefit-driven termination: the contract is extinguished on the **tenth**
  annuity instalment, effective retroactively to the date that instalment's trigger was met
  [S1].
- **Contract boundary.** Level 平準払 premiums, non-participating (*mu-haitō*, 無配当), no insurer
  repricing right on the 終身 chassis [S1] [S4] [S7] [S8], so all future premiums and benefits
  are inside the boundary and the horizon is the whole of life.
- **Rounding.** Intermediates at full double precision. Displayed cash flows to ¥0.01, all
  state probabilities to six decimals **[std]**. Monthly rows rounded for display do **not**
  re-add to displayed annual totals; totals are sums of unrounded values.

---

## Model point attributes

| Attribute | Type | Anchor cell (`point_id = 1`) |
|---|---|---|
| `policy_id` | str | — |
| `issue_age` (`x`) | int, 満年齢, 40–79 | 60 |
| `sex` | enum {M, F} | M |
| `lump_amount` (`A_L`) | JPY, ¥500,000–¥3,000,000 in ¥100,000 steps | 3,000,000 |
| `annuity_amount` (`A_N`) | JPY p.a., ¥200,000–¥1,200,000 in ¥100,000 steps | 600,000 |
| `grade_lump` (`G_L`) | enum 要支援1 … 要介護3 | 要介護2 |
| `grade_annuity` (`G_N`) | enum 要支援1 … 要介護3 | 要介護3 |
| `grade_waiver` (`G_W`) | enum 要支援1 … 要介護3 | 要介護1 |
| `annuity_max` (`n_A`) | int, instalments | 10 |
| `annuity_test` | enum {survival, state} | survival |
| `company_limb` | bool — the 180-day / 90-day 満65歳未満 alternative trigger | true |
| `dementia_rider` | bool — the 認知症一時金特約 (*ninchishō ichijikin tokuyaku*), a dementia lump-sum rider (*tokuyaku*, 特約) | false |
| `dementia_amount` | JPY (rider off on the anchor) | 1,000,000 |
| `mci_fraction` | fraction of `dementia_amount` on 軽度認知障害 | 0.10 |
| `rec_rate` | annual recovery out of the care state; read only under `annuity_test = state` | 0.0 **[std]** |
| `sel_lapse_lambda` | anti-selective lapse loading `lam` on incidence | 0.0 **[std]** |
| `waiting_1y` | bool — the 1-year 不担保期間 of the simplified-underwriting design | false |
| `premium` (`P`) | JPY per month, office premium, model-point input | 11,500 **[std]** |
| `prem_mode` | enum {monthly, semiannual, annual} | monthly |
| `prem_period` | enum {whole_life} | whole_life (終身払) |
| `issue_date` | date | — |

`premium` is an **input, not a computed quantity**. No carrier publishes assumed incidence
rate (*yotei hasseiritsu*, 予定発生率), assumed interest rate (*yotei riritsu*, 予定利率) or
予定死亡率 for this product, and the regulator confirms there is nothing standard to publish
for 第三分野 business [R10]; the statement of the method of calculating premiums and reserves
(*sanshutsu hōhō-sho*, 算出方法書) is a 基礎書類 filed with the 金融庁 and is not public
[REG-R2]. The ¥11,500
anchor is the sum of two published specimen rates at male 60, 月払, 終身/終身払 — ¥11,550,
rounded to the nearest ¥500: **¥5,820**
for a ¥3,000,000 要介護2以上 lump sum [S6] and **¥5,730** for a ¥600,000 要介護2以上 annuity on the
5年確定 basis [S6], with a second carrier's **¥5,817** for a ¥3,000,000 要介護3以上 lump sum
corroborating the first to three yen [S8].

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `pols_if(t)` | In-force probability at the **start** of month `t`, alive, not lapsed, not terminated; `pols_if(0) = 1`. Identically `pols_act(t) + care_w(t)` | monthly |
| `pols_act(t)` | **Active**: in force and not yet certified at `G_W`. The premium-paying and lapse-exposed population | monthly |
| `care_w(t)` | In force and has entered 要介護1以上 — waiver running, premium zero, lapse suspended | monthly |
| `care_l(t)` | In force and has entered 要介護2以上 — the lump sum has been paid to these lives | monthly |
| `care_n(t)` | In force and has entered 要介護3以上 — the annuity is in payment | monthly |
| `ann_coh(s, t)` | Survivors at `t` of the cohort that entered `G_N` in month `s`; carries the instalment counter | monthly |
| `age(t)` | Attained 満年齢 = `x + floor(t / 12)` | annually |
| `mort_rate(t)`, `mort_rate_care(t)` | Annual healthy and care-state mortality at `age(t)` | lookup |
| `inc_rate_w/l/n(t)` | Annual entry rate into 要介護1以上 / 要介護2以上 / 要介護3以上 | derived |
| `lapse_rate_mth(t)` | Monthly lapse, applied to `pols_act` only | lookup |
| `net_cf(t)` | Net cash flow of month `t`, insurer perspective, **income-positive** | monthly |

**Four absences are product facts, not gaps.** There is **no cash-surrender-value state**.
Four of the seven carriers publish an outright nil 解約返戻金 and one carries the fact in the
formal product name [S1] [S2] [S7] [S8], so `cv_pp` does not exist and lapse carries no cash
flow. There is **no automatic premium loan (*jidō furikae kashitsuke*, 自動振替貸付) state**: with
no surrender value there is nothing to lend against [S2] [REG-R14]. There is **no death
benefit**: the contract terminates on death with nothing payable [S1] [S11], so
`claims_death` does not exist. And there is **no day ledger of any kind** — the chassis's
`agg_days_dis`, `agg_days_acc` and their 支払限度日数 machinery have no counterpart here.

The three care ledgers are **nested by construction**: `care_n ≤ care_l ≤ care_w ≤ pols_if`
at every `t`. They are three *marginal* first-entry distributions riding on one survival
ledger, not three disjoint compartments, so they must never be added together — the
implementation carries them as cumulative-entry counters and the roll-forward check asserts
the ordering, not a sum.

---

## Assumption inputs

### (a) Contractual / guaranteed elements (cited; the insurer cannot change them)

| Input | Value | Basis |
|---|---|---|
| 介護一時金 | `A_L` = ¥3,000,000, once per contract, on first satisfaction of 要介護2以上; does not terminate the contract | [S1] [S4] [S7] [S12]; threshold **[std]** |
| 介護年金 | `A_N` = ¥600,000 p.a. in advance from first satisfaction of 要介護3以上, on the annual anniversaries of the 介護年金支払基準日, at most **10** instalments | [S1] [S7] [S10]; threshold and cap **[std]** |
| Annuity metering | **Survival-tested** — each instalment needs only that the insured be alive on the payment date; recovery does not stop it | [S4] [S7] [S10] [S12]; **[std]** against [S1] |
| Unpaid lump sum at annuity start | Paid together with the first annuity instalment | [S1] |
| 保険料払込免除 | From 要介護1以上, plus 高度障害状態 and a listed 身体障害状態 within 180 days of an accident; waived premiums treated as paid | [S1] [S2] [S8]; threshold **[std]** |
| Company-basis limb | 約款-defined dependency state persisting **180 days** (90 where dementia-defined), insured 満65歳未満 at diagnosis, with the post-65 continuation relief | [S1] [S2] [S4] [S12]; **[std]** |
| Waiting period | **None** on the care benefits; 180-day 認知症診断責任開始期 on the dementia rider only | [S1] [S2] against [S4] [S5] [S7] |
| 責任開始期前 rule | Nothing paid where the state results from an illness contracted or an accident occurring before the 責任開始期 | [S1] [S2] |
| Contract termination | On the 10th annuity instalment, retroactive to that instalment's trigger date; otherwise death, lapse or rescission | [S1] |
| 解約返戻金 | None at any duration | [S1] [S2] [S7] [S8] |
| Grace, 月払 | To the last day of the month following the 払込期月; lapse (*shikkō*, 失効) the day after | [S2] |
| Reinstatement (*fukkatsu*, 復活) | Within **1 year** of lapse, on fresh declaration (*kokuchi*, 告知); the 責任開始期 resets to the 復活日 | [S1] [S2] |
| 配当金 | None — the chassis is 無配当 | [S1] [S2] [S4]; [REG-R9] |

### (b) Insurer-discretionary current elements

**This class is nearly empty, and its emptiness is the product fact** — the same position as
`medical`. There is no 契約者配当, so the 三利源 (死差 / 利差 / 費差) framing and the surplus-distribution
methods of 施行規則 第30条の2 do not attach [REG-R9]; no premium review on the 終身 chassis; no MVA;
no non-guaranteed charge scale. What remains:

| Input | Snapshot value | Basis |
|---|---|---|
| Incidence basis (危険発生率) | The insurer's own, unpublished, in the 算出方法書 | [REG-R2]; the regulator requires a **test**, not a table [R10] [REG-R13] |
| Right to change base rates (基礎率変更権) | Exists for 第三分野, with a numeric exercise standard that must be disclosed at point of sale; **not modelled** | [R10]; [REG-R39]; **[std scope]** |
| Adjudication of the company-basis limb | Physician diagnosis against the 約款 definition, which the carrier states differs from the public 要介護認定 standard | [S1] [S2]; not modelled **[std scope]** |
| Catastrophe proportionality | War exclusion may be waived where the affected lives would not materially change the liability | [S2]; not modelled **[std scope]** |

The 基礎率変更権 is the one discretionary item with real economic content on this product, and it
is deliberately outside the model: what `jplib` implements is the *capability* the regime
asks for — an incidence basis parameterized so it can be re-set and re-run [R10] [REG-R15] —
not the exercise of the right.

### (c) Behavioral / experience assumptions (modeler's view)

**Mortality of healthy lives.** Inherited from the chassis without change. 第三分野標準生命表2018 is
public, free and machine-readable [REG-R18] [REG-R19], but it is a **valuation** table whose
margin runs the wrong way for a best estimate on a living-benefit product: it is graduated
from the *national* 第21回生命表（2010年）rather than insured experience, it **excludes 高度障害**, and
its risk-theory adjustment is bounded **70% below and 85% above** the unadjusted rate [R9]
[REG-R20]. Male `q60` on it is **0.00548** against 0.00653 on 生保標準生命表2018（死亡保険用）[R8]
[REG-R18]. So:

    mort_rate(age) = mort_be_factor × q_third_sector(age, sex),   mort_be_factor = 1.25 [std]

`mort_be_factor` is the reciprocal of 0.80, a round value inside the sourced 70%–85% band
[REG-R20] — it unwinds the table's stated margin and nothing more — and it is **identical
to `medical`'s**, because it is the same table read for the same reason.
`mort_rate_mth(t) = 1 − (1 − mort_rate(age(t)))^(1/12)` **[std]**. The 日本アクチュアリー会 site
terms restrict reproduction [REG-R21], so `jplib` ships `mort_table.csv` as a **[std]**
construction — quoted anchor rates joined by a log-linear graduation — whose `provenance`
column points at [REG-R18] and [REG-R20] on every row, never as a copy.

**Care-state mortality — the differential, and where it comes from.** No impaired-life table
for the 要介護 state exists in any retrieved source; the 日本アクチュアリー会 publishes a mortality table
for this class and no morbidity or impaired-life table at all [R8] [REG-R23]. The model
therefore carries a flat multiple:

    mort_rate_care(age) = k × mort_rate(age),   k = 2.75 [std]

`k` is anchored on two sourced numbers. 平均余命 at age 75 on 第23回完全生命表 is **12.54 years** for a
male [R13] [REG-R24]; the only quantified duration of care in any retrieved source is the
household survey's average of **55.0 months (4 years 7 months)** [R14]. On a constant-force
approximation life expectancy is the reciprocal of the force, so the ratio 12.54 / 4.583 =
**2.74** is the implied mortality multiple, rounded to 2.75. Both inputs are biased and the
biases are named rather than netted: the 55.0-month figure surveys people who *provided*
care, not certified persons, it is truncated (respondents still caring are counted at
elapsed duration) and it ends on recovery as well as on death — all of which make it **too
short**, so `k` = 2.75 is if anything **too high**; and 12.54 years is population mortality,
not healthy-life mortality, which pushes the other way. There is no observed range. Since
more than 90% of certified 第1号被保険者 are 75 or over [R4], age 75 is the right anchor age for
the comparison.

`k` is **not** only a post-onset assumption. It feeds back into the derived incidence below,
and dropping it (setting `k` = 1) cuts lifetime lump-sum claims on the anchor cell by
**31.0%**. That coupling is the least obvious property of this model.

**Recovery.** The care state is **absorbing in the base run** — `rec_rate` = **0 [std]**.
This is forced by the sources and it is a real simplification, not a harmless one: the
statute provides for a 有効期間 and for the grade to move up **or down** at 要介護更新認定 [R1], a
carrier's own FAQ addresses 「要介護状態が改善された場合」 [S3], and the state-tested annuity design [S1]
cannot be modelled at all without it. It is carried as a **named input set to zero**, with a
suggested placeholder of **5% p.a. [std]** when the `annuity_test = state` switch is on. It
is defensible for the composite because the composite's annuity is survival-tested and one
carrier says in terms that recovery does not stop payment [S7], and because the lump sum,
having been paid once, cannot be unpaid [S1].

**What `rec_rate` means, and the known limit of the `state` switch.** `rec_rate` is the rate
of falling **below the annuity grade `G_N`**, not the rate of returning to health, and it is
applied to `care_n` alone. A life that recovers therefore leaves the annuity ledger, becomes
eligible to re-qualify on a new 介護年金支払基準日, and **keeps its 保険料払込免除 for the rest of the
contract**: it stays in `care_w`, never re-enters `pols_act`, never pays premium again and
is never again exposed to lapse.

For the modelled step that is contractually **right**. `G_N` = 要介護3 and `G_W` = 要介護1, so a
downgrade 要介護3 → 要介護2 stops a state-tested annuity while leaving the waiver running, which
is what the ladder says [S1] [S2] [S8]. What is **not modelled** is recovery below `G_W` —
the downgrade that would end the waiver, restore the premium and put the life back in the
lapse-exposed population. There is no published transition matrix between grades in any
retrieved source, and one rate cannot carry two thresholds, so the model implements the one
it can evidence and states the other as a gap. The consequence, and its direction:

- under `annuity_test = state` with `rec_rate` > 0 the waiver, once started, runs for life,
  so **premium income is a lower bound** and the waived band is an upper bound. It is a
  lower bound in the exact sense that `act(t)`, and therefore every premium, is *identical*
  to the run with `rec_rate` = 0 even though the annuity ledger is materially smaller;
- the one place recovery does reach `care_w` is through the ten-payment cap, and it moves it
  **upward**: a recovered life takes no tenth instalment, so `term(t)` extinguishes fewer
  contracts and more of them stay in force on waiver. Recovery never releases a life back
  into `act(t)`;
- the base run is untouched — `rec_rate` = 0 there, and the whole question is a property of
  a switch that is off;
- reading `rec_rate` as a recovery-to-health rate is the error to avoid. It is a
  recovery-below-`G_N` rate, and this is a **[std scope]** limit of the switch, not a bug in
  it.

**Morbidity — turning a prevalence into an incidence.** This is the centre of the product.

What is published is 要介護（要支援）認定者数 and certification rate (*nintei-ritsu*, 認定率) — a
**point-in-time count of certified persons**, not a flow of new certifications. At 31 March
2024, 認定者数 was **7.08 million** against 35,890 thousand 第1号被保険者, an 認定率 of **19.4%**, split
by age as **4.3%** at 65–74 and **31.1%** at 75 and over [R4] [R5] [REG-R30]. The grade
composition is 要支援1 14.4% · 要支援2 14.1% · 要介護1 20.7% · 要介護2 16.8% · 要介護3 13.1% · 要介護4 12.6% ·
要介護5 8.3% [R4] [REG-R30], from which **要介護1以上 = 71.5%**, **要介護2以上 = 50.8%** and **要介護3以上 =
34.0%** of all certified persons, derived from that composition [R4].

Step 1 — **a prevalence curve by age [std]**. Only two age-banded rates were retrieved; the
five-year-band rates that a finer basis wants sit in the e-Stat release of the same
statistic, which was not fetched [R4] [REG-R33]. The curve is a logistic in attained age:

    prev(x) = prev_ceil / (1 + exp(−beta × (x − x_mid)))

pinned to the two sourced rates at representative ages **70** (the midpoint of the 65–74
band) and **82** (the approximate population mean age of the 後期高齢者 group), with a ceiling
`prev_ceil` = **0.95 [std]**. That gives **beta = 0.194069** and **x_mid = 85.710591**, and
`prev(70) = 0.043`, `prev(82) = 0.311` by construction, to the six decimals the
fitted parameters carry.

**The curve is pinned at 70 and 82 and is unpinned above 82, and above 82 is where the
claims are.** This is the model's largest single piece of unsourced structure and it is
stated here rather than left to be discovered:

- The logistic has **three** parameters and **two** sourced anchors. One degree of freedom
  is therefore not identified by the data at all, and the free parameter is `prev_ceil` —
  the one that governs the tail. `prev_ceil` = 0.95 is a **[std]** choice with no sourced
  value behind it, not a fitted quantity.
- Everything the curve says above age 82 is **extrapolation**. `prev(90) = 0.662` and
  `prev(100) = 0.894` are outputs of that unpinned degree of freedom; neither is sourced,
  and no retrieved document reports a 認定率 at any age above the 75+ band.
- On the anchor cell **40.2%** of lifetime benefit outgo falls at attained age 83 or over
  — that is, in the extrapolated region. Across the eight shipped model points the share
  runs from **40.2%** (issue age 60) to **74.7%** (issue age 79). An extrapolation carrying
  between two-fifths and three-quarters of the claims is a **first-order model risk**, not a
  detail of the fit.
- Read the fitted tail as an **upper bound on the gradient**: because `prev` is convex over
  the 75+ band, pinning at the population mean age assigns the band average to too young an
  age and therefore **overstates** `beta`.
- What the free parameter is worth, on the anchor cell: refitting the same two anchors under
  `prev_ceil` = 0.60, 0.50 and 0.40 gives `prev(90)` = 0.517, 0.459 and 0.388 and moves
  lifetime benefit outgo by **−4.2%**, **−5.8%** and **−6.7%**. The lifetime total is less
  sensitive than the tail rates are, because a lower ceiling refits to a **steeper** beta
  through the anchors and buys back at 70–82 what it gives up at 90+ — which is exactly why
  the ceiling is easy to overlook and why the *timing* of the claims moves more than the
  total does.
- What would fix it is not a better fit but **more data**: the five-year-band 認定率 in the
  unfetched e-Stat release of the same statistic [REG-R33] would pin the curve where it
  currently extrapolates.

Step 2 — **grade composition [std]**. `prev_G(x) = s_G × prev(x)` with `s_W` = **0.715**,
`s_L` = **0.508**, `s_N` = **0.340** [R4] [REG-R30]. Holding the shares constant across ages
is a standardization with a known direction of error: severity composition worsens with age,
so the model **understates** 要介護3以上 prevalence at old ages and overstates it at young ones.
The published composition is a single all-ages figure, so no observed range exists.

Step 3 — **the conversion, which is an identity, not an approximation.** In an illness-death
model with no recovery, write `mu_H` and `mu_C` for the forces of mortality outside and
inside the state and `i_G` for the entry hazard. Differentiating the prevalence `prev_G = C
/ (H + C)` along the age axis gives

    d(prev_G)/dx = (1 − prev_G) × [ i_G − prev_G × (mu_C − mu_H) ]

and therefore

    i_G(x) = prev_G'(x) / (1 − prev_G(x))  +  prev_G(x) × (mu_C(x) − mu_H(x))

**Two terms, and the second is not a refinement.** A rising prevalence understates incidence
because the certified population is simultaneously being drained by its own excess
mortality; on the anchor basis the mortality term is 5.8% of `i_L` at age 60 and a much
larger share at the ages where claims actually happen. Substituting the logistic derivative
`prev_G'(x) = s_G × beta × prev(x) × (1 − prev(x)/prev_ceil)` and `mu_C − mu_H = (k − 1) ×
mort_rate(x)` gives the form the model implements. `inc_rate_G_mth(t) = inc_rate_G(age(t)) /
12` **[std]**, uniform within the policy year, exactly as `medical` treats its incidence.

The conversion rests on a **stationary-population assumption [std]**: the cross-sectional
認定率 by age is read as the prevalence path a cohort will follow. Certified persons have grown
roughly **2.8-fold** in the 23 years since the scheme began [R16] and the 認定率 rose 19.0% →
19.4% in one year [R5], so the cross-section is *not* a cohort path; the assumption is the
same class of standardization `medical` makes on 患者調査 [REG-R26] [REG-R27], and it is stated
rather than hidden.

Step 4 — **the sub-65 gate [std]**. Below 65 the public limb fires only where the care state
arises from one of the **16 特定疾病** listed in 介護保険法施行令 第2条 [R1] [R3], and the company-basis
limb, which partly fills the hole, is restricted to lives 満65歳未満 [S1] [S4] [S12]. So:

    inc_rate_G(x) = f_age(x) × [ the two-term identity above ]
    f_age(x) = 0.20  for x < 65,   1.00  for x ≥ 65        [std]

`f_sub65` = **0.20** is a standardization with a weak anchor and it is named as such:
第2号被保険者 are **131 thousand** of the 7,083 thousand certified persons, **1.85%** of the total
[R4], but the 第2号被保険者 denominator was not retrieved so no rate can be computed. The factor
is set well above 1.85% because the company-basis limb backfills part of the restriction; a
`company_limb = false` run should use **0.05 [std]** instead. There is **no observed
range**. The gate produces a **6.1× step in incidence between age 64 and age 65** on the
anchor basis, which is a real feature of the product and not an artefact to smooth away.

Resulting annual entry rates into 要介護2以上, from the [std] basis: 0.000134 at 60 · 0.000295 at
64 · 0.001795 at 65 · 0.004795 at 70 · 0.012413 at 75 · 0.030456 at 80 · 0.065003 at 85 ·
0.115568 at 90. The 65-to-90 gradient is a factor of **64**.

Every rate in that list is an output of the **[std] proxy mortality**, not of
第三分野標準生命表2018 itself. The identity's second term is `prev_G × (k − 1) × mort_rate(x)`, so
`i_G` reads the mortality basis at every age — but the 日本アクチュアリー会 site terms permit these
documents to quote only the rates the library actually uses [REG-R21]. `mort_table.csv`
quotes and attributes a set of **anchor** rates and interpolates between them (see
`model.md`), so six of the eight ages above — 60, 65, 75, 80, 85 and 90 for a male — sit on
a quoted rate and the other two are graduated. The eight entry rates are reproducible from the
shipped model; a list computed on the published table would not be, and printing one would
publish more of that table than the quoting rule allows.

**Lapse [std].** Inherited from [the medical technical notes](../medical/technical-notes.md)
unchanged, and anchored the same way: the only published industry-wide persistency figure in
Japan is 解約・失効率 **5.6% p.a.** on 個人保険, measured on opening in-force sum assured
[REG-R31], and no Japanese durational curve is public.

| Policy year | 1 | 2 | 3 | 4 | 5 | 6–20 | 21+ |
|---|---|---|---|---|---|---|---|
| `lapse_rate` **[std]** | 9.0% | 7.0% | 6.0% | 5.5% | 5.0% | 4.5% | 3.0% |

`lapse_rate_mth(t) = 1 − (1 − lapse_rate(year(t)))^(1/12)` **[std]**. Lapse applies **only
to `pols_act`** — see *Policyholder behavior modeling*.

**Expenses and commission (all levels [std]).** Inherited from the chassis with one change.

| Input | Value | Basis |
|---|---|---|
| Acquisition expense | ¥20,000 per policy at `t = 0` | **[std]**, as `medical` |
| Initial commission | 1.5 × annualized premium at `t = 0` (¥207,000 on the anchor) | **[std]**, as `medical` |
| Renewal commission | 3.0% of premiums from policy year 2 | **[std]**, as `medical` |
| Maintenance expense | ¥250 per policy per month, inflating 1.0% p.a. at each anniversary | **[std]**, as `medical` |
| Claim expense | **¥5,000** per claim event — the lump sum, and **each** annuity instalment | **[std]**, raised from `medical`'s ¥3,000 |
| Expense inflation | 1.0% p.a. flat | **[std]**, as `medical` |

The claim expense is the one deliberate divergence: a care claim requires verification of a
municipal certification the insurer does not control, or adjudication of a 180-day
persistence test against a 約款 definition the carrier itself says differs from the public
standard [S1] [S2], and every annuity instalment carries an annual survival check [S1] [S7].
Maintenance expense is charged on `pols_if`, including lives on waiver.

---

## Cash flow components and recursions

### Notation

| Symbol | Meaning |
|---|---|
| `t` | policy month, `t = 0, 1, …, proj_len − 1` |
| `x`, `age(t)` | 契約年齢 (満年齢); attained age `x + floor(t/12)` |
| `y(t)` | policy year, `floor(t/12) + 1` |
| `A_L`, `A_N` | 介護一時金額 (JPY); 基準介護年金額 (JPY per instalment) |
| `n_A` | maximum annuity instalments (10) |
| `s_W`, `s_L`, `s_N` | grade shares of certified persons: 0.715 / 0.508 / 0.340 |
| `prev(x)`, `prev_G(x)` | all-grade and grade-`G` certification prevalence at age `x` |
| `beta`, `x_mid`, `prev_ceil` | logistic prevalence parameters: 0.194069 / 85.710591 / 0.95 |
| `k` | care-state mortality multiple (2.75) |
| `f_age(x)` | sub-65 特定疾病 gate: 0.20 below 65, 1.00 at 65 and over |
| `i_W`, `i_L`, `i_N` | annual entry rates into 要介護1以上 / 要介護2以上 / 要介護3以上; `_m` = monthly |
| `q_H(t)`, `q_C(t)` | monthly healthy and care-state mortality at `age(t)` |
| `w(t)` | monthly lapse rate, applied to `pols_act` only |
| `n_W`, `n_L`, `n_N` | expected entrants in month `t` into each of the three states |
| `S_C(s, t)` | care-state survival from month `s` to month `t` |
| `P`, `e(t)`, `ec` | monthly office premium; monthly maintenance expense; claim expense per event |
| `E0`, `c0`, `c_r` | acquisition expense; initial commission; renewal commission rate |

**Dimensional check.** `prev` and `prev_G` are dimensionless **proportions of a
population**; `i_G` is a **rate per year** and `i_G_mth` a probability per month; `q_H`,
`q_C`, `w` are probabilities per month. `beta` carries units of **1 / year**, which is why
`prev_G' = s_G · beta · prev · (1 − prev/prev_ceil)` comes out as a rate per year and can be
added to `prev_G · (k − 1) · mort_rate`, also a rate per year — the two terms of the
identity are dimensionally the same object, and a version of the formula that adds a
prevalence to a rate is the commonest way to get this wrong. `A_L` is JPY per event and
`A_N` JPY per instalment, so `A_L × n_L(t)` and `A_N × ann_count(t)` are JPY per
policy-month. `P`, `e(t)`, `ec`, `E0` are JPY. Every `net_cf` term is JPY per month. The
error this check catches is the one that dominates this product: multiplying the published
認定率 — a **prevalence**, 19.4% — by a benefit amount as if it were an annual claim frequency.

### The three-state chain

Healthy → in care → dead, with the care state absorbing in the base run. Write `act(t) =
pols_act(t)`. Entrants in month `t`:

    n_W(t) = act(t)                 × i_W_m(t)
    n_L(t) = (pols_if(t) − care_l(t)) × i_L_m(t)
    n_N(t) = (pols_if(t) − care_n(t)) × i_N_m(t)

`n_W` is drawn from the active population alone, because a life already certified at 要介護1以上
cannot enter it again. `n_L` and `n_N` are drawn from **everyone in force who has not yet
reached that grade**, which includes lives already in a lower care grade — progression up
the ladder is the dominant route into 要介護3以上, not direct entry from health. Because `i_N_m ≤
i_L_m ≤ i_W_m` at every age (the entry rate is monotone in `prev_G`, and `s_N < s_L < s_W`),
the nesting `care_n ≤ care_l ≤ care_w ≤ pols_if` is preserved by the recursion and does not
need to be imposed.

Roll-forward, with `term(t)` the lives extinguished by their tenth annuity instalment:

    act(t+1)    = ( act(t) − n_W(t) ) × (1 − q_H(t)) × (1 − w(t))
    care_w(t+1) = ( care_w(t) + n_W(t) ) × (1 − q_C(t)) − term(t)
    care_l(t+1) = ( care_l(t) + n_L(t) ) × (1 − q_C(t)) − term(t)
    care_n(t+1) = ( care_n(t) + n_N(t) ) × (1 − q_C(t)) − term(t)
    pols_if(t+1) = act(t+1) + care_w(t+1)

Care-state lives carry `q_C` and **no lapse**; active lives carry `q_H` and lapse. The
`check_pols()` identity is `pols_if(t) == act(t) + care_w(t)` at every `t`, and
`check_nesting()` asserts the three inequalities.

### The annuity ledger and the ten-payment cap

Instalments fall on the annual anniversaries of the 介護年金支払基準日, so the cohort entering in
month `s` is paid in months `s, s+12, …, s+12(n_A − 1)` while it survives [S1] [S7]:

    S_C(s, t)     = product over u = s … t−1 of ( 1 − q_C(u) )
    ann_count(t)  = sum over j = 0 … n_A−1 of  n_N(t − 12j) × S_C(t − 12j, t)
    claims_annuity(t) = A_N × ann_count(t)
    term(t)       = n_N(t − 108) × S_C(t − 108, t)          (the tenth instalment)

The `j = 0` term is `n_N(t)` itself: **payment in advance, on the entry date**. `S_C` must
be computed as a **partial product**, not as a ratio `SC(t)/SC(s)` of cumulative products —
`q_C` reaches 1 at the terminal age, so the cumulative product underflows to zero and the
ratio form fails exactly where the tail of the liability lives.

`term(t)` removes the extinguished lives from `care_n`, `care_l`, `care_w` and hence from
`pols_if`, which is the retroactive extinction of [S1] expressed on a monthly grid. On the
anchor cell the cap **binds**: entrants receive **4.62** instalments on average and
**14.9%** of them reach the tenth, so removing the cap raises lifetime annuity cost by
**11.4%**. This is the sharpest single contrast with `medical`, where the 通算 day limit never
binds on the expectation and the ledger reads zero forever.

Under the `annuity_test = state` switch the instalment additionally requires the care state
to persist, and a lapse of the state resets the schedule: a life that re-qualifies gets a
**new** 介護年金支払基準日 and starts again from instalment 1 [S1] [S2]. That switch is the only
consumer of `rec_rate`, and with `rec_rate` = 0 it is a no-op — which is why the switch and
the recovery rate must be tested together. Recovery moves `care_n` only: a recovered life
keeps its 保険料払込免除, for the reason and with the limit set out under *Recovery* above.

### Processing order

For `t = 0, 1, …, proj_len − 1`:

1. **Start of month.** `premiums(t) = P × act(t)` — **not** `P × pols_if(t)`; maintenance
   `e(t) × pols_if(t)` with `e(t) = 250 × 1.01^floor(t/12)`; renewal commission `c_r ×
   premiums(t)` for `t ≥ 12`. At `t = 0` additionally `E0` and `c0 = 1.5 × 12P`.
2. **Look up the age basis.** `age(t)`, hence `mort_rate`, `mort_rate_care`, `prev(age(t))`
   and the three entry rates; hence `q_H(t)`, `q_C(t)`, `i_W_m`, `i_L_m`, `i_N_m`, `w(t)`.
3. **Incidence.** `n_W(t)`, `n_L(t)`, `n_N(t)` per the formulas above; append `n_N(t)` to
   the annuity cohort ledger.
4. **End of month — claims.**

       claims_lump(t)    = A_L × n_L(t)
       claims_annuity(t) = A_N × ann_count(t)
       claims(t)         = claims_lump(t) + claims_annuity(t)

   and the claim-handling expense `ec × ( n_L(t) + ann_count(t) )`.
5. **End of month — decrements**, mortality **then** lapse **[std order]**, on the state
   each life occupies after step 3; then `term(t)`. Lapse pays **nothing** — there is no
   surrender value [S1] [S2] [S7] [S8] — so `claims_lapse(t)` is identically zero, and that
   zero is a product fact worth publishing.
6. **Ledger update.** Decrement every surviving annuity cohort by `1 − q_C(t)`; drop cohorts
   that have taken their tenth instalment.

### Net cash flow

    net_cf(t) = premiums(t) − claims_lump(t) − claims_annuity(t)
              − expenses(t) − claim_expenses(t) − commissions(t)

with `expenses(t) = e(t)·pols_if(t) + E0·1{t = 0}` — acquisition and maintenance only —
`claim_expenses(t) = ec·(n_L(t) + ann_count(t))` deducted on its own line, and
`commissions(t) = c0·1{t = 0} + c_r·premiums(t)·1{t ≥ 12}`. `net_cf` is **income-positive**
in the shipped model, per the library convention. The worked example's table below prints
`expenses` and `claim_expenses` **added together** in one column, and says so; the model
publishes them as two columns of `result_cf()`.

---

## Policyholder behavior modeling

- **Lapse stops at the waiver trigger, and that is a structural fact, not a refinement.**
  Once 要介護1以上 is certified the premium is waived and treated as paid on each 払込期月の契約応当日 [S1]
  [S2], so there is no premium to miss; and with no 解約返戻金 there is nothing to surrender for.
  Care-state lives therefore carry mortality only. Over the anchor cell's whole projection
  the waiver removes **5.53%** of the premium income the block would otherwise pay, and at
  age 85 **30.1%** of the surviving in-force block is on waiver and paying nothing.
- **The waiver fires strictly *before* the benefit.** `G_W` = 要介護1 sits one grade below
  `G_L` = 要介護2 and two below `G_N` = 要介護3, which is the market pattern [S1] [S8] and the
  reverse of `medical`, where the base waiver is disability-triggered and independent of the
  benefit. There is a real band of lives — 要介護1 lives, 20.7% of all certified persons [R4] —
  for whom the contract has stopped collecting premium and has not yet paid anything.
- **Lapse is real and immediate for everyone else.** No 解約返戻金 means no 自動振替貸付, which
  [REG-R14] treats as a policyholder election in any case, and one carrier's 約款 says the
  contract simply lapses the day after grace expires [S2]. No lapse-suppression term belongs
  in the recursion; the `whole_life` APL machinery must **not** be inherited here.
- **復活 [std scope].** Available within one year on fresh 告知 [S1] [S2], but a reinstated
  policy is **not** the policy that lapsed: the 責任開始期 resets to the 復活日, and the entire
  benefit definition is anchored to 責任開始期以後の傷害または疾病 [S1] [S2]. It belongs in the model as a
  *new model point*, not as a negative lapse; the base run treats lapse as absorbing.
- **Anti-selection is unusually direct here, and it is at the front door rather than in the
  lapse.** What is being selected against is an application to a public body that leaves a
  record, which is why underwriting declines anyone who has ever been certified for, or has
  ever applied for, 要支援 or 要介護 [S1], or who lives in a 高齢者向け施設 [S11]. The composite is fully
  underwritten, so no selection loading is applied at issue; the simplified-underwriting
  design prices its leniency with a 1-year 不担保期間 instead [S7] and is carried as the
  `waiting_1y` model-point flag, off in the base run.
- **Anti-selective lapse [std] (optional module, off in the base run).** Healthy lives lapse
  first, so the persisting block is progressively impaired on the *incidence* basis:
  `inc_eff(t) = inc_rate_G(age(t)) × [1 + lam × max(0, w_cum(t) − w_ref)]` with `w_ref` =
  0.20 and `lam` = 0.30 **[std]**, identical to `medical`'s module. Base run `lam` = 0. No
  Japanese selective-lapse evidence was retrieved.
- **Thresholds and amounts are elected at issue and cannot move.** `G_L`, `G_N`, `G_W`,
  `A_L` and `A_N` are model-point attributes; at one carrier the five 保険契約の型 are mutually
  exclusive and cannot be changed mid-term [S4]. A code path that varies them over `t`
  models a contract term that does not exist.
- **クーリング・オフ.** Out of scope: an eight-day pre-inception right under 保険業法 第309条 [S1]
  [REG-R36], and modelling it would need a new-business funnel this library does not have.

---

## Worked example

**Anchor cell (`point_id = 1`).** Male, 契約年齢 60 (満年齢), 終身 / 終身払, 介護一時金 `A_L` = ¥3,000,000 on
要介護2以上, 介護年金 `A_N` = ¥600,000 per year from 要介護3以上 capped at `n_A` = 10 instalments and
**survival-tested**, 保険料払込免除 from 要介護1以上, company-basis limb **on**, 認知症一時金特約 **off**,
1-year 不担保期間 **off**, office premium `P` = ¥11,500 per month. `proj_len = 12 × (116 − 60 +
1) = 684` months. All four rows below sit at `age = 60` and in policy year 1, so one set of
rates drives them.

Assumption values used, every one of them:

- **Mortality.** 第三分野標準生命表2018 男 `q60` = **0.00548** [R8] [REG-R18], quoted here because a
  worked example needs it and `jplib` quotes only the rates it uses [REG-R21]. Best estimate
  `mort_rate(60) = 1.25 × 0.00548 = 0.00685` **[std]**; care-state `mort_rate_care(60) =
  2.75 × 0.00685 = 0.0188375` **[std]**. Monthly: `q_H = 1 − (1 − 0.00685)^(1/12) =
  0.0005726334`; `q_C = 1 − (1 − 0.0188375)^(1/12) = 0.0015835104`.
- **Lapse.** Policy year 1, `lapse_rate` = 9.0% **[std]**; `w = 1 − (1 − 0.09)^(1/12) =
  0.0078284203`.
- **Prevalence.** `prev(60) = 0.95 / (1 + exp(−0.194069 × (60 − 85.710591))) =
  0.0064240463`, from the logistic **[std]** pinned to the sourced 4.3% at age 70 and 31.1%
  at age 82 [R4] [R5] [REG-R30]. Slope `prev'(60) = 0.194069 × 0.0064240463 × (1 −
  0.0064240463/0.95) = 0.0012382778` per year.
- **Grade shares.** `s_W` = 0.715, `s_L` = 0.508, `s_N` = 0.340 [R4] [REG-R30], so
  `prev_W(60) = 0.0045931931`, `prev_L(60) = 0.0032634155`, `prev_N(60) = 0.0021841757`.
- **Incidence**, from the two-term identity with `f_age(60)` = 0.20 **[std]**. For 要介護2以上:
  slope term `0.508 × 0.0012382778 / (1 − 0.0032634155) = 0.0006311047`; mortality term
  `0.0032634155 × (2.75 − 1) × 0.00685 = 0.0000391202`; annual `i_L = 0.20 × (0.0006311047 +
  0.0000391202) = 0.0001340450`, monthly `i_L_m = 0.0000111704`. Likewise `i_W =
  0.0001889030` (`i_W_m = 0.0000157419`) and `i_N = 0.0000896238` (`i_N_m = 0.0000074686`).
- **Expenses.** `e(t)` = ¥250 (policy year 1); `ec` = ¥5,000; acquisition ¥20,000; initial
  commission `1.5 × 12 × 11,500 = ¥207,000`; renewal commission 3% from `t = 12` — so zero
  in every row below **[std]**.

Every decrement rate above is either quoted from 第三分野標準生命表2018 [REG-R18] or derived from
介護保険事業状況報告 [R4] [R5] [REG-R30] with its citation, or is marked **[std]** as an illustrative
value in the shape of such a table. None of them is an insurer's basis, and none could be:
the 算出方法書 is not published [REG-R2] and there is no standard third-sector incidence table to
publish [R10].

| t | `pols_if` | `care_w` | `premiums` | `claims_lump` | `claims_annuity` | `expenses` | `commissions` | `net_cf` |
|---|---|---|---|---|---|---|---|---|
| 0 | 1.000000 | 0.000000 | 11,500.00 | 33.51 | 4.48 | 20,250.09 | 207,000.00 | −215,788.09 |
| 1 | 0.991604 | 0.000016 | 11,403.26 | 33.23 | 4.44 | 247.99 | 0.00 | +11,117.59 |
| 2 | 0.983278 | 0.000031 | 11,307.33 | 32.95 | 4.41 | 245.91 | 0.00 | +11,024.07 |
| 3 | 0.975022 | 0.000047 | 11,212.21 | 32.67 | 4.37 | 243.85 | 0.00 | +10,931.33 |

The `expenses` column above is the **combined** expense of the month — maintenance, claim
handling, and acquisition at `t = 0`. The model keeps them apart, publishing `expenses`
(acquisition and maintenance) and `claim_expenses` as two columns of `result_cf()`; the
traces below give both parts of every figure in the column.

**Trace, month 0.** `pols_if(0) = 1`, `care_w(0) = 0`, so `act(0) = 1`. Premium `= 11,500 ×
1 = 11,500.00`. Entrants: `n_W = 1 × 0.0000157419 = 0.0000157419`; `n_L = (1 − 0) ×
0.0000111704 = 0.0000111704`; `n_N = (1 − 0) × 0.0000074686 = 0.0000074686`. `claims_lump =
3,000,000 × 0.0000111704 = 33.5112`. The annuity cohort ledger holds one entry, paid
immediately in advance, so `ann_count(0) = 0.0000074686` and `claims_annuity = 600,000 ×
0.0000074686 = 4.4812`. Claim expense `= 5,000 × (0.0000111704 + 0.0000074686) = 0.0932`.
`expenses = 250.00 (maintenance) + 0.0932 (claim) + 20,000.00 (acquisition) = 20,250.0932`.
`commissions = 1.5 × 138,000 = 207,000.00`. `net_cf(0) = 11,500.00 − 33.5112 − 4.4812 −
20,250.0932 − 207,000.00 = −215,788.09`. Roll forward: `act(1) = (1 − 0.0000157419) × (1 −
0.0005726334) × (1 − 0.0078284203) = 0.99158782`; `care_w(1) = (0 + 0.0000157419) × (1 −
0.0015835104) = 0.00001572`; `care_l(1) = 0.00001115`; `care_n(1) = 0.00000746`; `pols_if(1)
= 0.99158782 + 0.00001572 = 0.991604`. `term(0) = 0` — no cohort is 108 months old.

**Trace, month 1.** `pols_if(1) = 0.991604`, `care_w(1) = 0.000016`, so `act(1) =
0.99158782` and `premiums = 11,500 × 0.99158782 = 11,403.2599` — note the premium rides on
`act`, not on `pols_if`, and the two have already parted company in the fifth decimal. Every
per-policy rate is unchanged (`age(1) = 60`, policy year still 1). Entrants: `n_L =
(0.991604 − 0.00001115) × 0.0000111704 = 0.0000110765`, so `claims_lump = 33.2295`; `n_N =
(0.991604 − 0.00000746) × 0.0000074686 = 0.0000074059`. `ann_count(1)` sums the cohorts
entering at `t = 1, −11, −23, …`; only `t = 1` exists, so `ann_count(1) = n_N(1) =
0.0000074059` and `claims_annuity = 4.4435` — the month-0 cohort is one month old, not
twelve, and is **not** paid again until `t = 12`. `expenses = 250 × 0.991604 (maintenance,
247.9009) + 5,000 × (0.0000110765 + 0.0000074059) (claim, 0.0924) = 247.9933`; no
acquisition expense after `t = 0`, no renewal commission before `t = 12`. `net_cf(1) =
11,403.2599 − 33.2295 − 4.4435 − 247.9933 = +11,117.59`. `pols_if(2) = 0.983278`.

**Trace, month 2.** Identical structure: `act(2) = 0.98324640`, `premiums = 11,307.3336`;
`n_L = 0.0000109834`, `claims_lump = 32.9501`; `n_N = 0.0000073436`, `claims_annuity =
4.4062`; `expenses = 245.8194 + 0.0916 = 245.9111`; `net_cf(2) = +11,024.07`. `care_w(3) =
0.000047`, `pols_if(3) = 0.975022`.

**Policy year 1 in aggregate** (`t = 0…11`, all at age 60, all in policy year 1 — the
strongest single test target in this file, because it exercises the whole annual cycle on
one set of rates). `Σ pols_if(t) = 11.461077` and `Σ act(t) = 11.460074`; the gap of
0.001003 is the waiver already biting in year 1.

| Line | Policy year 1 total |
|---|---|
| `premiums` | 131,790.85 |
| `claims_lump` | 384.05 |
| `claims_annuity` | 51.36 |
| `expenses` (acquisition + maintenance) | 22,865.27 |
| `claim_expenses` | 1.07 |
| `expenses` + `claim_expenses` | 22,866.34 |
| `commissions` | 207,000.00 |
| `net_cf` | **−98,510.90** |

with `pols_if(12) = 0.903774`, `care_w(12) = 0.000179`, `care_l(12) = 0.000127` and
`care_n(12) = 0.000085`. (The totals are sums of unrounded monthly values; the four
displayed rows do not re-add to them, and the year-1 `net_cf` differs by ¥0.01 from the sum
of the rounded monthly values.)

**What the numbers say.** Year-1 claims of ¥435.41 are **0.33%** of year-1 premium — an
order of magnitude thinner than `medical`'s 21.5%, because on the [std] basis the entry rate
into 要介護2以上 at age 60 is 0.000134 a year and at age 90 it is 0.115568, a factor of **862**
once the sub-65 gate is included and **64** from 65 to 90. This product prefunds a cost that
essentially does not arise for twenty-five years, which makes the **lapse assumption, not
the incidence basis, the dominant lever**: over the whole projection the [std] table leaves
0.126 of the block in force at age 85, and lifetime claims come to **34.7%** of lifetime
premium against **53.5%** with lapse switched off. Against the two published premium scales
the [std] basis reproduces **41.8%** of the lump-sum limb's premium and **27.3%** of the
annuity limb's as undiscounted expected claims [S6] [S8] — low for a retail loss ratio,
which is the honest signal that the [std] prevalence tail, the constant grade composition
and the inherited lapse table are all calibration targets rather than results.

---

## Valuation and reserve pointers

This library projects gross cash flows. Every valuation layer below consumes them and is
cited, never reproduced.

- **標準責任準備金.** 保険業法 第116条 requires a 責任準備金 at each 決算期 and delegates the accumulation method
  [REG-R4]; 施行規則 第68条 fixes scope [REG-R7]; 平成8年大蔵省告示第48号 sets the method as net level
  premium (*heijun jun-hokenryō-shiki*, **平準純保険料式**) on the standard valuation interest rate
  (*hyōjun riritsu*, 標準利率) and the standard table [REG-R10]. For contracts concluded from
  **1 April 2018** the third-sector valuation mortality is **第三分野標準生命表2018** [REG-R11] [R8]
  [REG-R18]. **The 標準利率 applicable to this class could not be established from a retrieved
  document and is [unverified]**; no value is asserted anywhere in these documents.
- **危険準備金, and the third-sector limb specifically.** 施行規則 第69条 divides the reserve into
  保険料積立金, 未経過保険料, 払戻積立金 and 危険準備金 and requires a separately identified 第三分野保険の保険リスクに備える危険準備金
  [REG-R8]. On top of 標準責任準備金 the 金融庁 requires an annual **ストレステスト** checking that the
  予定事故発生率 covers the 99th percentile of incidence risk over a **ten-year** horizon, a
  **負債十分性テスト** by future cash flow analysis where the 予定発生率 fails to cover risk defined at
  **97.7%**, disclosure of the incidence model used, and a transparent numeric 基礎率変更権
  exercise standard disclosed at point of sale [R10], computed under 平成10年6月8日大蔵省告示第231号
  with the calculating unit separated from internal audit [REG-R13] [REG-R14]. **That
  notification's own text was not retrieved and its stress magnitudes are [unverified].**
  `jplib` implements the *capability* the regime demands — an incidence basis parameterized
  so a shock can be applied per grouping — and **not** the statutory stress. That
  distinction must not be blurred downstream.
- **The regulator's own words are why this model's morbidity basis is [std].** For 第三分野
  business 「標準死亡率、参考純率といったスタンダードな指標が存在しておらず、公的なデータや各社の実績等から給付事由ごとその発生率を見込まざるを得ない」 [R10]:
  each insurer estimates incidence per benefit trigger from public data and its own
  experience. The reference implementation does exactly that, in public, from [R4] and [R5].
- **ESR.** From **31 March 2026** insurers are supervised on the economic-value
  経済価値ベースのソルベンシー規制, liabilities measured as **現在推計 + MOCE** at each 基準日 on assumptions
  re-set then, required capital at **99.5%**, early corrective action below an ESR of
  **100%** [REG-R15]; it supersedes the ソルベンシー・マージン比率 **200%** trigger [REG-R17]. `jplib`
  computes neither. What it owes the regime is a projection re-runnable on a re-set
  assumption basis at a stated 基準日 — which, for a third-sector product, is precisely the
  capability the ストレステスト already demands [R10].
- **1号収支分析.** The 保険計理人 appointed under 第120条 [REG-R5] gives an 意見書 under 第121条 [REG-R6];
  the 実務基準 turns that into a forward income-and-outgo analysis over 「少なくとも将来10年間」 by 区分経理
  segment [REG-R22]. That ten-year horizon is the same horizon the third-sector ストレステスト uses
  [R10].
- **Three bases, one projection.** J-GAAP statutory reserving [REG-R10], the ESR economic
  balance sheet [REG-R15] and IFRS 17 — **voluntary in Japan** [REG-R47] — are three
  measurement bases fed by one set of projected cash flows, which is why these notes keep
  the cash flows basis-agnostic and undiscounted.
- **Not applicable to this chassis.** 契約者配当 and the surplus-distribution methods of 施行規則
  第30条の2 [REG-R9] do not attach: the contract is 無配当 [S1] [S2] [S4]. 価格変動準備金 under 第115条 is
  asset-driven and outside a liability projection entirely [REG-R3]. On insurer failure,
  contracts are compensated up to **90% of the 責任準備金** through the 生命保険契約者保護機構 [REG-R40]
  [REG-R41].
- **Policyholder tax, not modelled.** Premiums fall in the **介護医療保険料** basket of the
  post-2012 生命保険料控除 [R11] [R12] [REG-R43]; the anchor's ¥138,000 annual premium is past the
  ¥80,000 point at which the basket deduction flattens to ¥40,000, so the marginal premium
  yen carries no relief. Benefits are not projected net of policyholder tax.

---

## Key sensitivities and model risks

In rough order of leverage on this block:

1. **Lapse, not incidence.** The claims are twenty-five years out and the [std] lapse table
   removes most of the block before they arrive: lifetime claims are 34.7% of lifetime
   premium on the base table and 53.5% with lapse off, and halving the table lifts the ratio
   to 43.5%. On a product whose liability is concentrated past age 85, persistency is the
   first-order assumption — and the only sourced anchor is a 5.6% sum-assured-weighted
   industry figure on a book of death cover [REG-R31].
2. **The prevalence tail — an extrapolation carrying the claims.** The logistic is pinned at
   ages **70** and **82** and is **unpinned above 82**, and above 82 is where the claims
   are: **40.2%** of lifetime benefit outgo on the anchor cell falls at attained age 83 or
   over, rising to **74.7%** at issue age 79. `prev(90) = 0.662` and `prev(100) = 0.894` are
   therefore **unsourced extrapolations**, not fitted values — the curve has three
   parameters and two anchors, and the unidentified one, `prev_ceil` = 0.95 **[std]**, is
   precisely the one that sets the tail. Refitting the same anchors at `prev_ceil` = 0.60 /
   0.50 / 0.40 gives `prev(90)` = 0.517 / 0.459 / 0.388 and moves lifetime outgo by −4.2% /
   −5.8% / −6.7%; the total moves less than the tail rates do only because a lower ceiling
   refits to a steeper `beta` and re-times the claims earlier, so the shape moves more than
   the sum. Separately, the Jensen bias in the 82 pin overstates `beta`. This is the model's
   largest unsourced structure and its single most improvable input: the five-year-band 認定率
   that would pin the tail sits in the unfetched e-Stat release of the same statistic
   [REG-R33].
3. **The care-state mortality multiple `k`, twice over.** It sets how long the annuity runs
   *and* it is the second term of the incidence identity. Setting `k` = 1 cuts lifetime
   lump-sum claims by 31.0%; `k` = 4 raises them by 12.4% while cutting annuity claims by
   8.3%, because heavier post-onset mortality shortens the annuity it lengthens the
   incidence into. No impaired-life table exists in any retrieved source.
4. **The constant grade composition.** Raising all three shares by 10% relative lifts
   lifetime claims by 7.5%. Since severity mix worsens with age and the model holds it flat,
   the direction of the error is known and unquantified [R4] [REG-R30].
5. **The ten-payment cap.** Removing it raises lifetime annuity cost by 11.4%; cutting it to
   five payments cuts annuity cost by 25.9%. The cap is a contractual parameter at one
   carrier [S1] and a payout-shape election at another [S7], and it is genuinely live on the
   expectation — unlike every limit on the `medical` chassis.
6. **The sub-65 gate.** `f_sub65` = 0.20 changes almost nothing in the lifetime totals (the
   loss ratio moves from 34.7% to 36.1% at `f_sub65` = 1) but it changes the **anchor cell's
   first five years by a factor of five**, so it dominates every early-duration test and
   every issue age below 65 — which is most of the 40–79 issue range.
7. **Survival-tested against state-tested annuity.** The two designs differ by whether a
   recovery decrement exists at all [S1] against [S4] [S7] [S10] [S12], not by a parameter.
   The composite takes the majority survival-tested form; the switch is not a refinement of
   it.
8. **Longevity is the tail risk, not mortality.** On a living-benefit product longer
   survival means more instalments and more entrants, and the valuation table is set
   deliberately **below** national mortality for exactly that reason [R9] [REG-R20]. Using
   it unadjusted as a best estimate is conservative in the reserving direction and material
   over a 57-year projection.

### Known modeling pitfalls

- **認定率 is a prevalence, not an incidence.** 19.4% of 第1号被保険者 are certified at a point in
  time [R4] [R5] [REG-R30]; multiplying that (or 50.8% × 19.4%) by a benefit amount, or
  treating it as an annual claim frequency, is the single commonest error in a Japanese
  nursing-care model. The conversion is the two-term identity above and is an explicit
  **[std]** step.
- **The excess-mortality term of the identity is not a refinement.** Dropping `prev_G ×
  (mu_C − mu_H)` — which is what happens if the care-state mortality multiple is set to 1
  "because there is no impaired-life table" — cuts lifetime lump-sum claims on the anchor
  cell by **31.0%**. A rising prevalence in a population being drained by its own excess
  mortality implies a *higher* incidence than the prevalence slope alone.
- **The care state is absorbing and the benefit does not stop.** `rec_rate` = 0 is a **named
  input**, not an omission [S3] [R1], and one carrier says in terms that recovery does not
  stop the annuity [S7]. The `annuity_test = state` switch is a no-op unless `rec_rate` is
  moved off zero, so the two must be tested together.
- **Lapse stops at the waiver trigger.** Once 要介護1以上 is certified the premium is waived and
  there is no 解約返戻金 to surrender for [S1] [S2], so lapse must apply to `pols_act` only.
  Applying it to `pols_if` destroys the annuity liability it took thirty years to build.
- **Premium income rides on `pols_act`, never on `pols_if`.** The waiver fires two grades
  below the annuity and one below the lump sum [S1] [S8], so a band of lives pays nothing
  and receives nothing. Charging premium to the whole in-force block overstates lifetime
  premium income by **5.85%** on the anchor cell — the same ¥92,738, read as 5.53% of the
  in-force-weighted total the waiver takes it out of. At age 85 the band is 30.1% of the
  surviving block.
- **The three care ledgers are nested, and the nesting must hold at every `t`.** `care_n ≤
  care_l ≤ care_w ≤ pols_if`. Independent entry hazards without the ordering let a life
  start the annuity before its lump sum has been paid, which the contract forbids — the
  unpaid lump sum is paid *with* the first instalment [S1]. They are marginal distributions
  on one survival ledger and must never be summed.
- **The ten-payment cap binds — do not carry `medical`'s intuition across.** Entrants take
  4.62 instalments on average and 14.9% reach the tenth; removing the cap raises annuity
  cost by 11.4%. The 通算 day ledger that reads zero forever on `medical` has no counterpart
  here.
- **The annuity is in advance and starts on the entry date.** The `j = 0` term of
  `ann_count(t)` is `n_N(t)` itself [S1] [S7]. Deferring the first instalment by a year
  removes roughly a tenth of the annuity liability and misdates all of it.
- **Compute care-state survival as a partial product.** `q_C` reaches 1 at the terminal age,
  so a cumulative-product-ratio form of `S_C(s, t)` divides by zero exactly where the tail
  of this liability lives.
- **There is a step in incidence at exactly age 65, and it belongs there.** Below 65 the
  public limb fires only on one of the 16 特定疾病 [R1] [R3] and the company-basis limb is
  restricted to 満65歳未満 [S1] [S4] [S12]; entry into 要介護2以上 jumps **6.1×** between age 64 and
  65 on the [std] basis. A smooth curve through 65 misprices every issue age in the lower
  half of the 40–79 range.
- **"180日" names two different mechanisms and a model must not implement one of them
  twice.** A 不担保期間 or 認知症診断責任開始期 means cover has not started; the 180-day (90-day for
  dementia) test inside the company-basis trigger means the care state must have *persisted*
  [S1] [S2] [S4] [S5] [S7]. The composite has the second and not the first on the care
  benefits. Related timing trap: a certification takes effect **retroactively to the
  application date** [R1], so a claim dated at notification is up to a month late.
- **The prevalence tail is extrapolated, and a reader must not treat it as sourced.** The
  curve is pinned only at ages 70 and 82; `prev(90) = 0.662` and `prev(100) = 0.894` come
  from `prev_ceil` = 0.95 **[std]**, a parameter no retrieved document supports, and
  **40.2%** of the anchor cell's benefit outgo (74.7% at issue age 79) falls in that
  extrapolated region. Quoting a tail rate as though it carried the [R4] [REG-R30]
  provenance of the two anchors misrepresents where this model's evidence stops.
- **A recovery under `annuity_test = state` does not restore the premium.** `rec_rate`
  models the fall **below the annuity grade `G_N`**, not a return to health. A life that so
  falls leaves `care_n` but stays in `care_w`, so its 保険料払込免除 runs for the rest of the
  contract and it is never again exposed to lapse. Under 要介護3 → 要介護2 that is contractually
  right — the waiver fires at 要介護1, two grades lower — but recovery all the way below 要介護1
  is **not modelled at all**, so premium income under that switch is a lower bound. Reading
  `rec_rate` as a recovery-to-health rate overstates the waiver and understates premium.
- **No surrender value, no APL, no death benefit.** `claims_lapse(t)` is identically zero
  [S1] [S2] [S7] [S8], nothing carries a policy through a missed premium [S2] [REG-R14], and
  `claims_death` does not exist [S1] [S11]. Importing the `whole_life` 自動振替貸付 logic
  suppresses lapses that really happen; adding a death benefit invents one that does not.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #jplib-nursing_care-r1
[R10]: #jplib-nursing_care-r10
[R11]: #jplib-nursing_care-r11
[R12]: #jplib-nursing_care-r12
[R13]: #jplib-nursing_care-r13
[R14]: #jplib-nursing_care-r14
[R16]: #jplib-nursing_care-r16
[R3]: #jplib-nursing_care-r3
[R4]: #jplib-nursing_care-r4
[R5]: #jplib-nursing_care-r5
[R8]: #jplib-nursing_care-r8
[R9]: #jplib-nursing_care-r9
[REG-R10]: #jplib-reg-r10
[REG-R11]: #jplib-reg-r11
[REG-R13]: #jplib-reg-r13
[REG-R14]: #jplib-reg-r14
[REG-R15]: #jplib-reg-r15
[REG-R17]: #jplib-reg-r17
[REG-R18]: #jplib-reg-r18
[REG-R19]: #jplib-reg-r19
[REG-R2]: #jplib-reg-r2
[REG-R20]: #jplib-reg-r20
[REG-R21]: #jplib-reg-r21
[REG-R22]: #jplib-reg-r22
[REG-R23]: #jplib-reg-r23
[REG-R24]: #jplib-reg-r24
[REG-R26]: #jplib-reg-r26
[REG-R27]: #jplib-reg-r27
[REG-R3]: #jplib-reg-r3
[REG-R30]: #jplib-reg-r30
[REG-R31]: #jplib-reg-r31
[REG-R33]: #jplib-reg-r33
[REG-R36]: #jplib-reg-r36
[REG-R39]: #jplib-reg-r39
[REG-R4]: #jplib-reg-r4
[REG-R40]: #jplib-reg-r40
[REG-R41]: #jplib-reg-r41
[REG-R43]: #jplib-reg-r43
[REG-R47]: #jplib-reg-r47
[REG-R5]: #jplib-reg-r5
[REG-R6]: #jplib-reg-r6
[REG-R7]: #jplib-reg-r7
[REG-R8]: #jplib-reg-r8
[REG-R9]: #jplib-reg-r9
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
