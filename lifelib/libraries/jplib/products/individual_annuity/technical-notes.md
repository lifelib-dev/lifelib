# Technical Notes

**Status:** Draft, 2026-08-20 (all cited sources accessed 2026-08-20).

**Scope note.** These notes specify a reference liability cash-flow projection model for the
standardized composite defined in `product-spec.md` (same directory) — a fixed individual
annuity insurance (*teigaku kojin nenkin hoken*, 定額個人年金保険) with the tax-qualification rider
(*zeisei tekikaku tokuyaku*, 税制適格特約) attached, implemented as `Annuity_JP_A` on an annual
grid. This is no single insurer's contract. [S#] and [R#] tags resolve against `sources.md`
(ids carried verbatim from `_research/individual-annuity.md`; frozen); [REG-R#] tags resolve
against the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is distinct.
**[std]** marks a standardization introduced for the reference implementation; [unverified]
marks a claim not confirmed against a retrieved document. **Every parameter appearing in
both documents carries the same value here as in `product-spec.md`.** Several parameters are
introduced here that the specification does not carry — each because the specification
explicitly defers it, or because it is a modeling construct with no contractual counterpart
— and each is flagged **new here** at the point of introduction.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows — premiums, deferral-phase
  death benefits, surrender payments, annuity instalments, expenses and commission — for a
  single-policy model point, in the sense the ESR current estimate (*genzai suikei*, 現在推計)
  requires: probability-weighted future cash flows re-measured on assumptions re-set at a
  stated 基準日 rather than locked in at issue [REG-R15]. Discounting, MOCE, required capital
  and every reserve are **out of scope** and are cited, not reproduced (see *Valuation and
  reserve pointers*).
- **Projection frequency.** Annual **[std]**. The contract's own clocks are annual: premiums
  are taken annually in the composite, the annuity payment dates (*nenkin shiharai-bi*, 年金支払日)
  are the 年単位の契約応当日 and its anniversaries [S2] [S4] [S9], and the annuity-certain
  (*kakutei nenkin*, 確定年金) pays once a year. What the annual grid gives up is the
  sub-annual grace period (*haraikomi yūyo kikan*, 払込猶予期間) state and the contractual monthly
  definition of the death benefit; both are handled below.
- **Timing conventions [std].** Premiums and annuity instalments at the **start** of the
  policy year, in advance; maintenance expense and commission at the start of the year;
  death benefits and surrender payments at the **end** of the policy year; deaths before
  lapses. Acquisition expense and first-year commission at `t = 0`.
- **Time index.** `t` is completed policy years since issue, **0-based**, matching
  `product-spec.md`: premiums fall at `t = 0 … m − 1`, the fund accumulates over
  `t = 0 … n`, and the annuity is paid at `t = n … n + k − 1`. `pols_if(t)` is the in-force
  count at the **start** of year `t` and weights that same `result_cf()` row.
- **Age basis.** Insurance age — age nearest birthday (*hoken-nenrei*, 保険年齢). Attained age
  in year `t` is `x + t`, where `x` is the 契約年齢. This is the basis 標準生命表2018 is built for
  [REG-R20]; a model that ages its points on age last birthday (*man-nenrei*, 満年齢) must say so and
  say what it does about the half-year difference.
- **Currency.** JPY throughout. Premiums and benefits are yen amounts on a yen contract [S2]
  [S4] [S5] [S6] [S8] [S9]; there is no currency layer. 外貨建年金 is out of scope, and is a
  different standard-reserve regime besides [REG-R12].
- **Model points.** Single-policy, projected on an expected (probability-weighted) basis;
  survivorship and persistency factors multiply per-policy amounts. No aggregation logic.
- **Termination.** The projection ends at `t = n + k`, the year after the last 年金支払日. There
  are no tail states: the 確定年金 pays exactly `k` instalments and the contract ends [S2] [S4].
  With the life annuity with a guarantee period (*hoshō-kikan-tsuki shūshin nenkin*,
  保証期間付終身年金) module on, `proj_len` runs instead to the terminal age of the payout table — 122
  for a male, 126 for a female [R3] [REG-R19].
- **Contract boundary.** Premiums are level and guaranteed for the whole 保険料払込期間 with no
  review right [S2] [S4] [S5] [S6], so the insurer has no unilateral repricing lever and all
  `m` premiums are projected. The FSA's 第1の柱告示 was not opened in this research pass
  [REG-R16], so the ESR contract-boundary rule itself is [unverified] here; the composite's
  guarantee makes the question moot for this product, but not for a rate-resetting design
  [S12].
- **Rounding.** Intermediate values at full precision. Displayed cash flows to the yen with
  two decimals **[std]**. The basic annuity amount (*kihon nenkin-gaku*, 基本年金額) is rounded
  **down to the nearest ¥100** **[std, new here]** — Japanese specimens are published at
  that granularity [S3] [S5] [S6] [S10], and it is a contractual amount rather than a
  display convention, so the rounding must happen inside the model.

---

## Model point attributes

| Attribute | Type | Anchor cell (`point_id = 1`) |
|---|---|---|
| `policy_id` | str | JP-ANN-0001 |
| `sex` | enum {M, F} | M |
| `issue_age` (`x`) | int, 保険年齢, 20–55 | 30 |
| `premium_term_y` (`m`) | int, years, ≥ 10 under the rider | 30 |
| `defer_gap_y` (`d`) | int, years, 据置期間 | 5 |
| `annuity_start_age` | int, `= x + m + d`, ≥ 60 | 65 |
| `premium_pp` (`P`) | JPY p.a., level | 180,000 |
| `payout_form` | enum {certain, life_guar} | certain |
| `payout_term_y` (`k`) | int, years, 10 or 15 under the rider | 10 |
| `guar_term_y` (`g`) | int, years, life form only | 10 |
| `db_ratio` (`ρ`) | float, death benefit ÷ cumulative premiums | 1.00 |
| `tax_rider` | bool, 税制適格特約 attached | true |
| `apl_on` | bool, 自動振替貸付 module | false |
| `loan_on` | bool, 契約者貸付 module | false |

`db_ratio` is the tontine parameterization — 0.70 on both retrieved tontine designs [S3]
[S10], 1.00 on the composite. It sits on the model point rather than in a code branch
because a tontine is the same chassis with a different death-benefit ratio under the same
surrender ceiling (`product-spec.md`, variation 7). `n = m + d` and `proj_len` are derived,
not supplied. The anchor premium is not a modeling invention: it is the annualization of a
published specimen at the identical model point [S6], which is what makes the calibration
below checkable.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `pols_if(t)` | Contracts with an obligation open at the start of year `t`; `pols_if(0) = 1` | annual recursion |
| `lives_if(t)` | Probability the annuitant is alive at the start of year `t`; `lives_if(0) = 1` | annual recursion |
| `av_pp(t)` | Premium reserve fund (*hokenryō tsumitatekin*, 保険料積立金) per policy at the start of year `t`, before that year's premium | annual recursion |
| `cv_pp(t)` | Surrender value (*kaiyaku-henreikin*, 解約返戻金) per policy at time `t` | derived from `av_pp` |
| `db_pp(t)` | Death benefit (*shibō kyūfukin*, 死亡給付金) payable for a death in year `t − 1` | schedule |
| `annuity_pp(t)` | Annuity instalment per contract payable at the start of year `t` | fixed from `t = n` |
| `mort_rate(t)` | Best-estimate annual mortality rate applied in year `t` | assumption lookup |
| `lapse_rate(t)` | Best-estimate annual 解約・失効 rate applied in year `t` | assumption lookup |

Two in-force measures are carried, following `SPIA_US_S`. **`pols_if` counts contracts with
an obligation open; `lives_if` counts annuitants alive.** In the deferral phase the two
separate because lapse removes a contract without removing a life. In the payout phase they
separate for the opposite reason: on a 確定年金 the instalments are unconditional, so `pols_if`
stays flat through the certain period while `lives_if` runs down on the post-annuitisation
table. Collapsing the two is the single most likely way to build this product wrongly, and
it is the first pitfall below.

`av_pp` occupies the library's account-value slot: a per-policy fund credited with the
premium net of loading, with interest at the assumed interest rate (*yotei riritsu*, 予定利率)
and with a survivorship release. `prem_to_av_pp(t)` is the credited premium, and `cv_pp` —
not `av_pp` — is the surrender quantity, as the library's naming ruling requires.

---

## Assumption inputs

### (a) Contractual / guaranteed elements (cited; the insurer cannot change them)

| Input | Value | Basis |
|---|---|---|
| Office premium `P` | Level, guaranteed for the whole 保険料払込期間; no reviews | [S2] [S4] [S5] [S6] |
| Premium frequency | Annual, in advance, `t = 0 … m − 1` | modes [S4] [R16]; annual **[std]** |
| 死亡給付金 during deferral | `ρ × P × min(t, m)` — cumulative premiums paid; the annual-grid form of 月払保険料 × 経過月数 | [S2] [S4]; 既払込保険料相当額 [S6] |
| Why that shape | 所令211①ロ requires the amount to increase progressively with duration or cumulative premiums | [R10] |
| Deductions from the benefit | Unpaid premiums, 契約者貸付 principal and interest, 自動振替貸付 balances | [S2] [S4] |
| 解約返戻金 ceiling | Never exceeds the 死亡給付金; equal to it after a period | [S2] [S4] |
| Surrender after the 年金支払開始日 | Not available | [S2] [S4] [R16] |
| 年金支払開始日 | The 年単位の契約応当日 at 保険年齢 `annuity_start_age`; instalments there and on `k − 1` anniversaries | [S2] [S4] [S9] |
| 確定年金 instalments | Paid regardless of survival; on death the PV of unpaid instalments is paid, or the recipient elects continuation | [S2] [R16] |
| 保証期間付終身年金 instalments | Unconditional inside the guarantee period, life-contingent after it | [S4] [R16] |
| 年金の一括払 factors | 1.010, 2.016, 3.018, 4.016, 5.010, 6.000, 6.986, 7.968, 8.946, 9.921, 10.891, 11.858, 12.821, 13.780 for 1–14 remaining instalments | [S2] |
| Partial commutation | Refused — a request on one tranche is a request on all | [S1] [S4]; 所令211①ハ [R10] |
| 契約者貸付 rate | 2.40% p.a. compound on the current issue cohort; capped at the 解約返戻金 | [S11] [S8]; limit [S4] [REG-R14] |
| 自動振替貸付 rate cap | 8% p.a. compound | [S4] |
| 復活 window | Three years from lapse, and only before the 年金支払開始日 | [S2] [S4] |
| 自殺免責 | Three years, counted inclusively, from the 責任開始日 or the last 復活日 | [S2] [S4] |
| Underwriting | None — no medical examination, no 告知 | [S2] [S3] [S4] |

### (b) Insurer-discretionary current elements

| Input | Base-run value | Basis |
|---|---|---|
| 予定利率, deferral (`i_d`) | **1.00%** p.a., fixed at issue | [S8]; the lower arm of the banded pair at [S5]; adoption **[std]** |
| 予定利率, payout (`i_p`) | **0.65%** p.a., set separately from the deferral rate | [S5]; adoption **[std]** |
| 予定事業費率 `β` | **6.5%** of each office premium, level over the premium term | [REG-R2]; **[std]** (1), deferred to here by `product-spec.md` footnote 8 |
| 年金支払開始時費用 `θ` | **1.0%** of the 年金原資, charged once at annuitisation | **[std, new here]** (1) |
| 解約控除 base | One annual premium, run off linearly over ten policy years | schedule **[std]**; base amount **[std, new here]** (2) |
| 契約者配当 | **Zero** declared. Machinery retained: accumulate at a declared rate, no withdrawal before annuitisation, apply as a single premium increasing the 基本年金額 | [S4] [S11]; zero base run **[std]** |
| 配当積立利率 | 0.60% p.a. where a non-zero dividend is run | [S11] |
| 税制適格型払戻金の積立利率 | 0.60% p.a. on refunds the rider will not release | [S11] |
| 保証期間付終身年金 basis at annuitisation | Assumed unchanged — 0.65% and the same payout table | **[std]** (3) |
| 自動振替貸付 | Module off | present [S4], absent [S2]; election required [REG-R14]; **[std]** |
| 契約者貸付 | Module off | [S4] [S11]; **[std]** |

1. No retrieved document discloses a 予定事業費率 or a mortality / interest / expense surplus
   (*shisa / risa / hisa*, 死差 / 利差 / 費差) split for this line: the
   保険料及び責任準備金の算出方法書 — the method document for premiums and the policy reserve
   (*sekinin-junbikin*, 責任準備金) — is a 基礎書類 filed with the FSA and not published
   [REG-R2], and 三利源 is practice vocabulary in any
   event — 施行規則第30条の2 permits distribution 「剰余金の生じた原因に応じて」 without naming three sources
   [REG-R9]. Rather than invent a three-way split (新契約費 / 維持費 / 集金費) that no source can
   confirm, the composite carries **one** deferral loading and **one** payout loading and
   calibrates them against a published specimen. At the anchor cell `β` = 6.5% and `θ` =
   1.0% reproduce that carrier's published 年金原資 of approximately ¥6,260,000 as ¥6,261,482,
   its 一括受取率 of approximately 115.9% as 115.9534%, its 基本年金額 of ¥638,300 as ¥638,100
   (−0.03%) and its 年金受取率 of approximately 118.2% as 118.1667% [S6]. Two round [std] numbers
   calibrated against a published outcome are worth more than five invented ones.
2. Both 約款 state the *shape* and not the parameters — 「ご契約後短期間で解約されたときには、解約返還金がない場合が あります」
   [S2] and 「まったくないか、あってもごくわずか」 [S4] — and the formula sits in the unpublished 算出方法書
   [REG-R2]. `product-spec.md` footnote 10 fixes the linear ten-year run-off; the **base
   amount** of one annual premium is introduced here, and it is what makes the sourced
   invariant hold: at the anchor cell `cv_pp(1)` = ¥7,976.18 against ¥180,000 of premium
   paid — nil-or-negligible, as both 約款 require — while `cv_pp(0)` = 0.
3. The life-annuity election is priced on the 基礎率 in force at the 年金支払開始日, thirty-five years
   out [S2] [S9]. No source can give that basis. Holding it at the issue basis is a
   **[std]** modeling choice, and the reason base-run take-up is zero rather than a guess.

### (c) Behavioral / experience assumptions (modeler's view)

**Mortality — two tables, and they are not interchangeable.** For contracts concluded from
2018-04-01 the standard valuation basis is 生保標準生命表2018（死亡保険用）for death cover and
生保標準生命表2007（年金開始後用）— expressly **not** updated in 2018 — for annuities in payment [REG-R10]
[REG-R11], confirmed by 日本アクチュアリー会 for FY2026 [R4]. The 2018 PDF contains four tables and no
年金開始後用 table at all [R2] [REG-R18]; the only public machine-readable source for it is the
combined Excel workbook [R3] [REG-R19]. The publisher's terms prohibit reproduction and
transmission to third parties without written consent [REG-R21], so this library **ships no
copy of either table**. What it ships are two **[std] constructions**, one per table, stated
here in full so that any implementation reproduces them exactly. They are built differently
because their anchor sets are different.

**死亡保険用 — the canonical jplib table.** `mort_table.csv`'s `death_cover_2018` rows are the
library-wide canonical file, shared by every `jplib` product that reads 生保標準生命表2018（死亡保険用）,
so that a given cell carries the same value **and** the same provenance in every product that
ships it. Its **anchor** rows are rates read from the IAJ table and quoted under attribution
[REG-R18]; every other age is graduated **log-linearly in age between the two neighbouring
anchors** — linear in `ln q`:

    q(a) = exp( ln q(a0) + (a - a0)/(a1 - a0) * ( ln q(a1) - ln q(a0) ) )

evaluated in full double precision and rounded to five decimal places on output. Nothing is
extrapolated: both sexes run from an age-0 anchor to a terminal anchor, so every graduated
age lies strictly between two sourced ones. **Both sexes carry their own sourced anchors**;
there is no age setback on this table. Over the ages this product reaches, the anchors are:

| Sex | Anchor ages | Terminal age |
|---|---|---|
| 男 **[REG-R18]** | 18, 20, 22, 25, 30, 31, 32, 33, 34, 35, then every fifth year to 105 | 109 |
| 女 **[REG-R18]** | 18, 20, 22, 25, 30, then every fifth year to 105, and 110 | 113 |

with `q30` = 0.00068, `q60` = 0.00653 and `q90` = 0.15760 male and `q30` = 0.00037, `q60` =
0.00363 and `q90` = 0.09357 female among them [REG-R18]. The ten male anchors at ages 30–35
are why the anchor cell's fund is anchored rather than graduated over its first six years.

**年金開始後用 — a Makeham construction.** Three published male spot rates twenty years apart are
all that was retrieved, so this table is a fitted law rather than a graduation of a full
anchor set:

    mu(x) = A + B * c**x          (Makeham)
    q(x)  = 1 - exp(-mu(x)),      truncated to 1 at the table's terminal age

| Table (male) | Anchors | `A` | `B` | `c` | Terminal age |
|---|---|---|---|---|---|
| 生保標準生命表2007（年金開始後用）**[std]** | q60 = 0.00642, q80 = 0.03357, q100 = 0.17469 [R3] [REG-R19] | 0.000542569 | 3.189261e−05 | 1.090896969 | 122 [R3] |

The three anchors are reproduced exactly by construction. Off-anchor residuals against
published rates, stated rather than hidden: q65 = 0.009609 against a published 0.00966
(−0.5%), q70 = 0.014515 against 0.01411 (+2.9%), q90 = 0.077578 against 0.08318 (−6.7%) and
q110 = 0.367153 against 0.31667 (+15.9%) [R3]. The fit is good over the ages the base run
uses (65–74) and degrades in the far tail, which matters only with the life-annuity module
on. Only male spot rates were retrieved for this table, so its female rows are the male
construction with a **four-year age setback** **[std, new here]** — the setback the published
terminal ages themselves imply, 126 against 122 [R3] [REG-R19].

The Makeham coefficients above are **displayed rounded** and the payout factors are not
reproducible from them; the reference implementation therefore ships the **anchors** rather
than the coefficients. `mort_anchor_table.csv` carries, per table and sex, the anchor ages
and rates and the terminal age; `mort_table.csv` carries the rate the stated graduation
produces at every age; and both files carry a `provenance` column pointing at [REG-R18] and
[REG-R19], marking on each row whether it is a sourced anchor or a graduated value. Neither
is a copy of an IAJ file. `check_mort_graduation()` asserts that the two files still agree —
死亡保険用 log-linear between its anchors, 年金開始後用 on the Makeham law.

**Best-estimate adjustment, and why its sign flips.** Both are **valuation** tables. The
2018 death-cover table carries an explicit roughly-2σ risk-theory margin capped at 130% of
the unadjusted rate, plus a forward improvement allowance of 2.5% p.a. for five years and
1.0% p.a. for three, and it includes 高度障害 inside the death rate [REG-R20]. A best-estimate
basis is therefore an adjustment **downward**: `mort_rate(t) = 0.85 × mort_rate_base(t)` in
the deferral phase **[std, new here]** — 0.85 sits inside the range the margin implies,
which runs from 1/1.30 ≈ 0.77 where the cap binds to 1.00 where no margin does. The payout
table is a valuation basis for a **longevity** liability, so its margin runs the other way:
prudence there means assuming annuitants live *longer*, that is, a table set below best
estimate. The composite therefore uses `mort_rate(t) = 1.10 × mort_rate_base(t)` from `t =
n` **[std, new here]**. The 作成概要 for the 2007 年金開始後用 table was not retrieved, so the *size*
of that margin is [unverified] and 1.10 is a standardization; the *direction* is structural.
A model that applies one factor to both tables has one of the two signs wrong.

**Lapse.** The only public figure is a market-wide 解約・失効率 of **3.4%** for FY2024, whose
denominator is pre-annuitisation in-force 契約高 at the start of the year only [R15] [REG-R31]
— the right decrement in principle, since it excludes contracts already in payment. No
duration curve is public for this line. The reference table is **[std, new here]**,
calibrated so that its **count-weighted** mean over the deferral phase of the anchor cell —
`sum of l(t) w(t)` over `sum of l(t)`, for `t` = 0 … `n` − 1 — is **3.4160%**, against the
published 3.4%:

| Policy year `t` | 0 | 1 | 2 | 3–9 | 10 … m−1 | m … n−2 | n−1 and later |
|---|---|---|---|---|---|---|---|
| `lapse_rate(t)` **[std]** | 6.0% | 5.0% | 4.5% | 4.0% | 3.0% | 1.0% | 0% |

Three features are load-bearing. The 据置期間 rate drops to 1.0% because no premium is due in
those years, so the commonest lapse trigger is absent. The rate is **zero in year `n − 1`**
because that year ends on the 年金支払開始日, where surrender is no longer available [S2] [S4] — a
lapse there would remove a contract against a zero payment — and zero thereafter for the
same reason. And the published rate and this table are not weighted alike: on the anchor
cell the same curve averages **2.4754%** over the same years when weighted by `av_pp`
instead of by `l`, because lapse is front-loaded and the fund is back-loaded. The two
weightings are not interchangeable, and a calibration must say which one it used;
`lapse_rate_mean(weighting)` publishes both.

**Expenses and commission (all levels [std, new here]; structure conventional).**

| Input | Value |
|---|---|
| Acquisition expense `E0` | ¥30,000 per policy at `t = 0` |
| Initial commission `c0` | 40% of the annual premium at `t = 0` |
| Renewal commission `c_r` | 2% of premium, `t = 1 … m − 1` |
| Maintenance expense `e(t)` | ¥4,000 p.a. in deferral, ¥2,000 p.a. in payment, both inflating 1.0% p.a. |
| Claim expense `ec` | ¥5,000 per death claim; none on surrender |
| Expense inflation | 1.0% p.a. flat |

These are best-estimate *cash* expenses and are entirely separate from the 予定事業費率 in class
(b), which is a pricing loading living inside `av_pp`. Mixing the two — charging `β` against
the cash flow, or projecting `e(t)` into the fund — double-counts expense in one direction
and destroys the calibration in the other.

**Option take-up.** Life-annuity election at annuitisation: **0% [std]** (footnote 3 above).
年金の一括払 commutation: **0% [std]**. Both modules run in the non-anchor model points. 減額, 払済
and 復活 are not exercised in the base run **[std scope]** [S1] [S2] [S4].

---

## Cash flow components and recursions

### Notation

| Symbol | Meaning |
|---|---|
| `t` | policy year, 0-based; attained 保険年齢 in year `t` is `x + t` |
| `x`, `m`, `d` | 契約年齢; 保険料払込期間 in years; 据置期間 in years |
| `n`, `k` | `n = m + d`, the year of the 年金支払開始日; `k`, the payment period in years |
| `g` | guarantee period in years, life form only |
| `P` | level office annual premium (`premium_pp`) |
| `β`, `θ` | 予定事業費率 on premium; 年金支払開始時費用 on the 年金原資 |
| `i_d`, `i_p` | 予定利率, deferral (0.0100) and payout (0.0065) |
| `NP(t)` | net premium credited to the fund, `P × (1 − β)` for `t < m` and 0 after (`prem_to_av_pp`) |
| `q'(x)` | 予定死亡率 — the [std] 死亡保険用 table rate, used **only** inside the fund recursion |
| `q(t)` | best-estimate mortality applied in year `t` (`mort_rate`); two tables, by phase |
| `w(t)` | best-estimate 解約・失効 rate applied in year `t` (`lapse_rate`) |
| `ρ` | death-benefit ratio, 1.00 on the composite and 0.70 on a tontine (`db_ratio`) |
| `V(t)` | 保険料積立金 per policy at the start of year `t`, before that year's premium (`av_pp`) |
| `DB(t)` | 死亡給付金 payable for a death in year `t − 1`, paid at `t` (`db_pp`) |
| `SC(t)` | surrender charge (*kaiyaku kōjo*, 解約控除) at time `t` |
| `CV(t)` | 解約返戻金 at time `t` (`cv_pp`) |
| `F` | annuity fund (*nenkin genshi*, 年金原資) `= V(n)` (`annuity_fund_pp`) |
| `ä(k, i)` | annuity-due factor `(1 − (1 + i)^(−k)) / i × (1 + i)` |
| `B` | 基本年金額, the annual instalment (`annuity_pp` while in payment) |
| `l(t)`, `L(t)` | `pols_if(t)`; `lives_if(t)` |
| `D(t)`, `W(t)` | expected deaths and expected lapses in year `t` |
| `E0`, `e(t)` | acquisition expense; maintenance expense (together, `expenses`) |
| `ec` | claim expense per death claim (`claim_expenses`, its own column) |
| `c0`, `c_r` | initial commission rate; renewal commission rate |
| `CF(t)` | net cash flow of year `t`, insurer perspective, **income-positive** (`net_cf`) |

Dimensional check: `q`, `q'`, `w`, `β`, `θ`, `ρ` are dimensionless; `P`, `V`, `DB`, `CV`,
`F`, `B`, `E0`, `e`, `ec` are JPY; `ä` is dimensionless (years of income per unit of annual
income); `l` and `L` are probabilities. `B = F(1 − θ) / ä` is therefore JPY per year, and
because the annual grid carries exactly one instalment per row, no month count ever enters —
unlike the monthly-grid products in this library. Every `CF` component is JPY per policy per
year.

### The 保険料積立金 recursion

The fund is a net-level-premium accumulation carrying a survivorship release, which is what
lets a survival-benefit-weighted (*seizon hoshō jūshi-gata*, 生存保障重視型) design pay a larger
annuity than a pure savings contract of the same premium:

    V(0) = 0
    V(t+1) = [ (V(t) + NP(t)) * (1 + i_d) - q'(x+t) * DB(t+1) ] / (1 - q'(x+t))
             for t = 0 .. n-1,  with NP(t) = P * (1 - beta) for t < m and 0 after

The division by `(1 − q')` is the survivorship credit: the premiums of those who die are
released to the survivors net of the death benefit paid, and because `DB` is capped at
cumulative premiums while `V` is not, that release turns **positive from the duration at
which `V` first exceeds `DB`** — `t` = 13 at the anchor cell. Three consequences. The
recursion uses the **pricing** mortality `q'` at 100% of the [std] table, not the
best-estimate `q`, because `V` is a contractual quantity and not an experience projection.
Lapse does **not** appear: the surrender release is the 解約控除, which accrues to the insurer
and not to the surviving fund. And where actual mortality runs lighter than `q'`, the
insurer credits more survivorship than it earns and takes a 死差損 — the mortality sensitivity
is signed the opposite way round from a death-cover product.

### Deferral-phase benefit amounts

    DB(t) = rho * P * min(t, m)
    SC(t) = P * max(0, (10 - t) / 10)
    CV(t) = min( max(0, V(t) - SC(t)), DB(t) )   for t < n, and 0 for t >= n

`DB(t)` is the annual-grid form of the contractual 月払保険料 × 経過月数 [S2] [S4]. It stops growing
at 払込満了 because no further premium is paid: `DB(t) = ρPm` for every `t ≥ m`. The `min(·,
DB)` in `CV` is the sourced ceiling 「解約返還金は…死亡給付金の額を限度とします」 [S2], and it is what the other
carrier means by 「一定期間経過後は死亡給付金と同額になります」 [S4] — beyond the crossover the two are literally
the same number. Surrender is unavailable from the 年金支払開始日 [S2] [S4], hence the second limb.

### The annuitisation transition

At `t = n` three things happen in one step, in this order:

1. The **年金原資** is struck: `F = V(n)`. It is the accumulated fund out of which the annuity
   is bought, and one carrier pins the definition down by publishing both 一括受取率 (`= F ÷ Pm`)
   and 年金受取率 (`= kB ÷ Pm`) at one model point [S6].
2. The **基本年金額** is derived from it, once, and never recomputed:

       B_certain = floor( F * (1 - theta) / adue(k, i_p) / 100 ) * 100
       B_life    = floor( F * (1 - theta) / adue_life(g, i_p, table) / 100 ) * 100

   where `adue_life` is the guaranteed-plus-life annuity-due factor at `annuity_start_age`
   on the **年金開始後用** table at 100% — a pricing basis, not the best-estimate factor:

       adue_life = sum over j >= 0 of  max( 1{j < g}, jp_(x+n) ) / (1 + i_p)**j

3. The **mortality table switches** from 死亡保険用 to 年金開始後用, and the best-estimate factor
   switches with it, from 0.85 to 1.10.

The rate in step 2 is `i_p` = 0.65%, **not** the deferral rate: the payout phase is priced
on its own 予定利率, published separately and left unchanged when that carrier's deferral rates
moved [S5]. Since `i_p < i_d`, each yen of 年金原資 buys **less** annuity than a single-rate
model would say: at `k` = 10 the factor is `ä(10, 0.65%)` = 9.71433757 against
`ä(10, 1.00%)` = 9.56601758, so buying the annuity at `i_d` would overstate `B` by 1.5505%.

### The payout forms

**確定年金 (base form).** `k` instalments of `B` at `t = n … n + k − 1`, unconditional. The
obligation does not depend on survival, so

    pols_if(t+1) = pols_if(t)   for n <= t < n + k - 1,   and   pols_if(n+k) = 0

while `lives_if` continues to run down on the payout table. On death inside the period the
PV of the unpaid instalments is paid, or the recipient elects continuation to the end of the
term [S2] [R16]; the base run assumes **continuation at 100% [std]**, under which the two
elections produce the same instalment stream and the payout cash flow is deterministic.

**保証期間付終身年金 (module).** Instalments are unconditional for `g` years and life-contingent
after:

    pols_if(t) = pols_if(n) * max( 1{t - n < g}, (t-n)p_(x+n) )

on the best-estimate payout basis, with `proj_len` running to the table's terminal age.
Death inside the guarantee pays the PV of the unpaid guaranteed instalments [S4] [R16]. At
the anchor cell's fund, the life form with `g` = 10 gives `B` = **¥281,300** against
¥638,100 on the certain form — 44.08% of it — because the annuity-due factor is 22.032668
against 9.714338. That ratio is the product fact the module exists to show.

**年金の一括払 (module).** From the 年金支払開始日 to the last 年金支払日 the annuitant may take the PV of the
remaining certain or guaranteed instalments as a lump sum, terminating the contract [S2]
[S4]. The composite uses the published factor table verbatim over 1–14 remaining instalments
and an implied 0.40% p.a. outside it **[std]** [S2]. Base-run take-up is 0%, and one reason
is arithmetic: at `t` = `n` with ten instalments remaining the factor is 9.921, so the lump
sum is 638,100 × 9.921 = **¥6,330,590.10** against a gross 年金原資 of ¥6,261,482.08 — **1.1037%
more**. The factors come from one carrier [S2] and the payout 予定利率 from another [S5], and
the composite does not reconcile them. Switching commutation on therefore switches on a
composite artefact rather than a product feature; a production model must re-derive the
factors on its own payout basis.

### In-force recursion and processing order

For each year `t = 0 … proj_len − 1`:

1. **Start of year — income and outgo per policy in force.** Premium `P × l(t)` for `t < m`.
   Annuity instalment `B × l(t)` for `n ≤ t < n + k`. Maintenance expense `e(t) × l(t)`.
   Renewal commission `c_r × P × l(t)` for `1 ≤ t < m`. At `t = 0` additionally `E0` and `c0
   × P`.
2. **Fund roll-forward.** `V(t+1)` per the recursion above (deferral phase only).
3. **Benefit schedules.** `DB(t+1)` and `CV(t+1)` per the formulas above.
4. **End of year — deaths.** `D(t) = l(t) × q(t)`; death outgo `DB(t+1) × D(t)`; claim
   expense `ec × D(t)`. In the payout phase `D(t) = 0` on both forms inside the certain or
   guaranteed period.
5. **End of year — lapses**, applied to the survivors of mortality **[std order: death
   before lapse]**. `W(t) = l(t) × (1 − q(t)) × w(t)`; surrender outgo `CV(t+1) × W(t)`.
6. **Update.**

       pols_if(t+1)  = pols_if(t) * (1 - q(t)) * (1 - w(t))     (deferral phase)
       lives_if(t+1) = lives_if(t) * (1 - q(t))                 (throughout)

   with the payout-phase `pols_if` rules of the previous section replacing the first line
   from `t = n`.

### Net cash flow

    CF(t) = P * l(t) * 1{t < m}                             (premiums)
          - B * l(t) * 1{n <= t < n + k}                    (annuity instalments)
          - DB(t+1) * D(t)                                  (death benefits)
          - CV(t+1) * W(t)                                  (surrender payments)
          - ec * D(t)                                       (claim expense)
          - e(t) * l(t)                                     (maintenance)
          - c_r * P * l(t) * 1{1 <= t < m}                  (renewal commission)
          - (E0 + c0 * P) * 1{t = 0}                        (acquisition)

**Sign convention.** These notes print the stream **income-positive**, so the model
publishes it as `net_cf` and carries **no `liability_cf` cells** — that absence is a fact
about which orientation the notes chose, not an omission. A reader comparing the payout
years with `SPIA_US_S`, whose notes print outgo-positive, must flip the sign:
`Annuity_JP_A`'s payout rows are large negatives.

**Roll-forward checks.** `check_pols_roll_fwd()` asserts the in-force recursion over all `t`;
`check_lives_roll_fwd()` asserts `L(t) − L(t+1) = L(t) q(t)`;
`check_fund()` asserts `(V(t) + NP(t))(1 + i_d) = q' DB(t+1) + (1 − q') V(t+1)` over the
deferral phase; `check_cv_cap()` asserts `CV(t) ≤ DB(t)` at every deferral duration; and
`check_annuity_total()` asserts that the undiscounted instalments sum to `kB` on the certain
form. Each takes no argument and returns a `bool`; the per-`t` signed residuals live at
`check_*_resid(t)`.

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** reference constructions; calibration evidence is cited
where any exists.

- **Base lapse [std].** The duration table in class (c), anchored to the 3.4% market rate
  [R15] [REG-R31] on a count weighting.
- **払込猶予期間 and 復活, and why neither survives the annual grid [std].** Grace is published only
  in monthly-anniversary terms [S4], and 復活 is available for three years [S2] [S4] —
  Japanese policies really do come back, unlike the UK composite in `uklib`, which
  terminates finally. On an annual grid a premium unpaid at `t` terminates the contract at
  `t`; there is no partial-year grace state and no reinstatement re-entry. The net effect of
  omitting both is a **lapse rate biased upward**, since real reinstatements would return
  some of `W(t)` to the in-force. The monthly-grid products in this library carry the grace
  state; this one does not, so a calibration against this model's `lapse_rate` is a
  net-of-復活 rate by construction.
- **自動振替貸付 (module, off) [std].** With `apl_on = true` the lapse decrement is suppressed
  while `CV(t) ≥ P`: the insurer lends the premium against the surrender value at a rate
  capped at 8% p.a. and the policy stays in force [S4] [REG-R14]. The loan balance compounds
  and is deducted from the death benefit or from the 年金原資. This is **not** a no-lapse rule:
  it is a policyholder election [REG-R14], one carrier's product does not offer it at all
  [S2], and where principal and interest come to exceed the surrender value the contract
  lapses **from the moment the excess arose** [S4].
- **Dynamic lapse [std].** Premiums and the 予定利率 are both fixed at issue, so there is no
  premium-shock lapse and no rate-driven surrender on this chassis. The economic driver runs
  the other way: when new-business 予定利率 rise above the rate at issue — as they did in 2025,
  for the first time in about forty years [S8] — an in-force contract becomes relatively
  unattractive and lapse should rise. A reference multiplier on `lapse_rate`, base run 1.0:

      M(t) = min( 2.0, max( 1.0, 1 + phi * max(0, i_new(t) - i_d) ) )

  with `phi` = 20 **[std]** and `i_new(t)` an external input. The composite's own answer to
  that pressure is the 金利キャッチアップ配当 one carrier pays instead [S12].
- **The surrender ceiling suppresses lapse by construction, and the model must not
  double-count it.** Beyond the crossover the surrender value *is* the death benefit and is
  capped at cumulative premiums, so surrendering returns exactly what was paid in and no
  interest [S4] [R16] — an economic disincentive already fully expressed inside `CV(t)`.
  Loading `lapse_rate` down for it as well would count the same effect twice.
- **Annuitisation-election take-up [std].** 0% in the base run. The election is between a
  guaranteed stream fixed at issue and an option on the insurer's future 基礎率 [S2] [S9], and
  the tax treatment differs: the annuity is 雑所得 where payer and annuitant coincide, while a
  lump sum taken instead of it is 一時所得 [R13] [REG-R46]. That is a tax decision, not a coin
  flip, and no take-up evidence exists in the retrieved set.
- **減額, 払済 and the rider [std scope].** Not exercised. Both are heavily constrained by the
  rider — no paid-up conversion inside ten policy years, and any refund arising on a 減額 is
  not paid out but accumulated at a declared rate and applied as a single premium increasing
  the 基本年金額 [S1] [S2] [S4]. A model that releases that refund as cash breaches 所令211①ニ [R10]
  and is projecting a non-qualifying contract.

---

## Worked example

**Anchor cell (`point_id = 1`).** Male, 保険年齢 30 at issue; level annual premium `P` =
¥180,000 payable at `t` = 0 … 29 (`m` = 30, ¥5,400,000 cumulative); 据置期間 `d` = 5; 年金支払開始日 at
`t` = `n` = 35, age 65; 10年確定年金 (`k` = 10); `ρ` = 1.00; 税制適格特約 attached; 自動振替貸付, 契約者貸付, the
life-annuity election and commutation all **off**; declared dividend zero.

Assumption values used, all listed above: `i_d` = 1.00%, `i_p` = 0.65%, `β` = 6.5%, `θ` =
1.0%, so `NP(t)` = ¥168,300 for `t` < 30; `SC(t)` = ¥180,000 × (10 − `t`)/10; `E0` =
¥30,000, `c0` = 40%, `c_r` = 2%, `e(t)` = ¥4,000 × 1.01^`t` in deferral and ¥2,000 ×
1.01^`t` in payment, `ec` = ¥5,000; lapse 6.0 / 5.0 / 4.5 / 4.0 / 3.0 / 1.0 / 0%; mortality
0.85 × the canonical [std] 死亡保険用 table to `t` = 34 and 1.10 × the [std] 年金開始後用 Makeham
construction from `t` = 35.

**The 死亡保険用 rates below are the canonical `jplib` table's own values.** The ones at ages 30
to 35, 60, 65 and 90 are **sourced anchors** — rates read from the IAJ table and quoted under
attribution [REG-R18] — and the ages between anchors carry the log-linear graduation of
assumption class (c), rounded to five decimal places. The 年金開始後用 rates are [std]
illustrative values from the Makeham construction, whose three anchors are quoted from [R3]
[REG-R19]; no other number here is a published table value.

**Annuitisation quantities.** `V(35)` = `F` = **¥6,261,482.075674**; 一括受取率 = `F` ÷
¥5,400,000 = **115.9534%**; `F(1 − θ)` = ¥6,198,867.2549; `ä(10, 0.65%)` = 9.71433757; `B`
raw = ¥638,115.281, rounded down to the nearest ¥100 → **`B` = ¥638,100**; 年金受取総額 =
¥6,381,000; 年金受取率 = **118.1667%**. Against the same carrier's published specimen at the
identical model point — 年金原資 approximately ¥6,260,000, 一括受取率 approximately 115.9%, 基本年金額
¥638,300, 年金受取総額 ¥6,383,000, 年金受取率 approximately 118.2% [S6] — the model reproduces the
基本年金額 to within 0.04% (¥638,100 against ¥638,300, −0.031%) and the 年金原資 to within 0.03%.

**Deferral phase, first four years.** `expenses` is acquisition plus maintenance only;
`claim_expenses` is its own column, as in `result_cf()`.

| `t` | `pols_if(t)` | `lives_if(t)` | premiums | claims_death | claims_lapse | expenses | claim_expenses | commissions | `net_cf(t)` |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1.00000000 | 1.00000000 | 180,000.00 | 104.04 | 478.29 | 34,000.00 | 2.89 | 72,000.00 | +73,414.78 |
| 1 | 0.93945668 | 0.99942200 | 169,102.20 | 198.36 | 9,278.56 | 3,795.40 | 2.75 | 3,382.04 | +152,445.08 |
| 2 | 0.89196040 | 0.99883584 | 160,552.87 | 286.59 | 15,605.61 | 3,639.56 | 2.65 | 3,211.06 | +137,807.41 |
| 3 | 0.85131535 | 0.99824153 | 153,236.76 | 375.12 | 19,811.26 | 3,508.44 | 2.61 | 3,064.74 | +126,474.60 |

**Fund, benefit and surrender value at the same durations, plus the crossover.**

| `t` | `av_pp(t)` | `SC(t)` | `db_pp(t)` | `cv_pp(t)` |
|---|---|---|---|---|
| 0 | 0.000000 | 180,000 | 0 | 0.000000 |
| 1 | 169,976.183805 | 162,000 | 180,000 | 7,976.183805 |
| 2 | 341,646.281577 | 144,000 | 360,000 | 197,646.281577 |
| 3 | 515,028.264178 | 126,000 | 540,000 | 389,028.264178 |
| 12 | 2,155,556.812834 | 0 | 2,160,000 | 2,155,556.812834 |
| 13 | 2,347,105.257270 | 0 | 2,340,000 | 2,340,000.000000 |
| 34 | 6,191,563.274447 | 0 | 5,400,000 | 5,400,000.000000 |
| 35 | 6,261,482.075674 | 0 | 5,400,000 | 0.000000 |

**The annuitisation transition and the payout phase.**

| `t` | `pols_if(t)` | `lives_if(t)` | premiums | claims_annuity | claims_death | claims_lapse | expenses | claim_expenses | `net_cf(t)` |
|---|---|---|---|---|---|---|---|---|---|
| 29 | 0.34079080 | 0.94857451 | 61,342.34 | 0.00 | 9,354.09 | 54,927.49 | 1,819.15 | 8.66 | −5,993.89 |
| 30 | 0.32888680 | 0.94375291 | 0.00 | 0.00 | 9,857.63 | 17,661.31 | 1,773.16 | 9.13 | −29,301.22 |
| 34 | 0.30795821 | 0.91994710 | 0.00 | 0.00 | 13,131.68 | 0.00 | 1,727.74 | 12.16 | −14,871.58 |
| 35 | 0.30552641 | 0.91268274 | 0.00 | 194,956.41 | 0.00 | 0.00 | 865.62 | 0.00 | −195,822.02 |
| 36 | 0.30552641 | 0.90303627 | 0.00 | 194,956.41 | 0.00 | 0.00 | 874.28 | 0.00 | −195,830.68 |
| 44 | 0.30552641 | 0.79624594 | 0.00 | 194,956.41 | 0.00 | 0.00 | 946.71 | 0.00 | −195,903.12 |

Commission is zero from `t` = 30 and is omitted from the second table. `net_cf(29)` includes
renewal commission of 1,226.85.

### Trace

**Year 0.** `q'(30)` = 0.00068, a sourced anchor [REG-R18], so `q(0)` = 0.85 × 0.00068 =
**0.000578**; `w(0)` = 0.06. Premium = 180,000 × 1 = 180,000.00. `D(0)` = 1 × 0.000578 =
0.000578, and `DB(1)` = 1.00 × 180,000 × min(1, 30) = 180,000, so death outgo = 180,000 ×
0.000578 = **104.04** and claim expense = 5,000 × 0.000578 = 2.89. `W(0)` = 1 × (1 −
0.000578) × 0.06 = 0.05996532. Fund: `V(1)` = [(0 + 168,300) × 1.01 − 0.00068 × 180,000] ÷
(1 − 0.00068) = (169,983.00 − 122.40) ÷ 0.99932 = **169,976.183805**; `SC(1)` = 180,000 ×
9/10 = 162,000, so `CV(1)` = min(max(0, 169,976.183805 − 162,000), 180,000) =
**7,976.183805**, and surrender outgo = 7,976.183805 × 0.05996532 = **478.29**. Expenses =
`E0` + `e(0)` = 30,000 + 4,000 = **34,000.00**, with the claim expense of **2.89** carried in
its own column; commission = 0.40 × 180,000 = **72,000.00**. `CF(0)` = 180,000.00 − 104.04 −
478.29 − 34,000.00 − 2.89 − 72,000.00 = **+73,414.78**. Update: `pols_if(1)` = 1 × (1 −
0.000578) × (1 − 0.06) = **0.93945668**; `lives_if(1)` = 1 × (1 − 0.000578) =
**0.99942200**.

**Year 1.** `q'(31)` = 0.00069, also a sourced anchor [REG-R18], so `q(1)` = 0.85 × 0.00069 =
0.0005865; `w(1)` = 0.05. Premium = 180,000 × 0.93945668 = **169,102.20**. `D(1)` =
0.93945668 × 0.0005865 = 0.0005509913, and `DB(2)` = 360,000, so death outgo = **198.36** and
claim expense = 2.75. `W(1)` = 0.93945668 × (1 − 0.0005865) × 0.05 = 0.0469452844. `V(2)` =
[(169,976.183805 + 168,300) × 1.01 − 0.00069 × 360,000] ÷ (1 − 0.00069) = (341,658.945643 −
248.400000) ÷ 0.99931 = **341,646.281577**; `SC(2)` = 144,000, so `CV(2)` =
**197,646.281577** and surrender outgo = 197,646.281577 × 0.0469452844 = **9,278.56**.
Maintenance = 4,000 × 1.01 × 0.93945668 = **3,795.40**, which is the whole of `expenses(1)`;
renewal commission = 0.02 × 169,102.20 = **3,382.04**. `CF(1)` = 169,102.2024 − 198.3569 −
9,278.5609 − 3,795.4050 − 2.7550 − 3,382.0440 = **+152,445.08**. Update: `pols_if(2)` =
0.93945668 × (1 − 0.0005865) × (1 − 0.05) = **0.89196040**.

**The crossover at `t` = 13.** `av_pp(12)` = 2,155,556.812834 against `db_pp(12)` =
2,160,000 — the fund is still under the ceiling, so `cv_pp(12)` = `av_pp(12)`. One year
later `av_pp(13)` = 2,347,105.257270 against `db_pp(13)` = 2,340,000, and the cap binds:
`cv_pp(13)` = **2,340,000.000000** exactly. From here to `t` = 34 the surrender value and
the death benefit are the same number, which is what 「一定期間経過後は死亡給付金と同額になります」 asserts [S4];
and the excess of `av_pp` over `db_pp` — ¥791,563.274447 by `t` = 34 — is precisely the
survival benefit the design buys.

**Year 34, the last deferral year.** No premium (`t` ≥ 30) and no lapse (`w(34)` = 0,
because the year ends on the 年金支払開始日). `q'(64)` = 0.00929, log-linear between the sourced
anchors at 60 and 65 [REG-R18], so `q(34)` = 0.85 × 0.00929 = 0.0078965 and `D(34)` =
0.30795821 × 0.0078965 = 0.0024317920; death outgo = 5,400,000 × 0.0024317920 =
**13,131.68**; claim expense = 12.16; maintenance = 4,000 × 1.01^34 × 0.30795821 = 1,727.74.
`CF(34)` = −13,131.68 − 1,727.74 − 12.16 = **−14,871.58**. `pols_if(35)` = 0.30795821 × (1 −
0.0078965) = **0.30552641**. Fund: `V(35)` = [6,191,563.274447 × 1.01 − 0.00929 × 5,400,000]
÷ (1 − 0.00929) = (6,253,478.907191 − 50,166.000000) ÷ 0.99071 = **6,261,482.075674** = `F`.

**Year 35, the first 年金支払日.** `B` = 638,100, paid in advance to every contract with an
obligation open: claims_annuity = 638,100 × 0.30552641 = **194,956.41**. No premium, no
death benefit and no surrender: the 確定年金 obligation is unconditional, so `pols_if(36)` =
`pols_if(35)` = 0.30552641 even though `lives_if` falls from 0.91268274 to 0.90303627 on
`q(35)` = 1.10 × 0.00960851 = 0.0105693625 — the payout table, at the payout factor.
Maintenance = 2,000 × 1.01^35 × 0.30552641 = 865.62. `CF(35)` = −194,956.4052 − 865.6191 =
**−195,822.02**.

**Years 36 to 44.** Identical instalments; `net_cf` drifts from −195,830.68 to −195,903.12
on expense inflation alone. At `t` = 44 the tenth and last instalment is paid and
`pols_if(45)` =
0. `lives_if(45)` = 0.77848987: of the annuitants alive at age 65, 14.70% died over the ten
   payout years, and not one of those deaths changed a single yen of projected cash flow.

The shape is the mirror image of `uklib`'s term assurance. A large **positive** year-0 flow
— Japanese annuity acquisition cost is small against a ¥180,000 premium, where UK term
carries 150% of an annualized premium in upfront commission — then thirty years of declining
positive margin as surrender outgo grows against a shrinking premium base, `net_cf` turning
negative at `t` = 27, and then a decade of pure outgo. Summed undiscounted the projection is
−¥516,539.46; at a flat 1% discount it is +¥41,625.62, which is the sense in which the
composite is a profitable but thin contract.

---

## Valuation and reserve pointers

This library projects gross cash flows and builds no reserve. Each layer below consumes them
and is cited, not reproduced.

- **Standard policy reserve (*hyōjun sekinin-junbikin*, 標準責任準備金).** 保険業法第116条第1項
  requires a 責任準備金 at each period end and 第2項
  delegates the method [REG-R4]; 施行規則第68条 fixes which contracts are inside the
  regime, excluding those whose reserve varies with 特別勘定 assets and those whose 約款 lets the
  insurer change the coefficients, with a carve-out where the 約款 floors the 予定利率 at or above
  the standard valuation interest rate (*hyōjun riritsu*, 標準利率) at issue [R5] [REG-R7] —
  which is exactly why the rate-resetting design at [S12] carries a minimum guarantee. 第69条 gives the taxonomy: 保険料積立金, 未経過保険料, 払戻積立金, 危険準備金
  [REG-R8]. 平成8年大蔵省告示第48号 sets the method — net level premium (*heijun jun-hokenryō-shiki*,
  **平準純保険料式**), with no Zillmer adjustment — the 標準利率 reset from JGB yields on a 1 October
  基準日 with banded safety coefficients, and the mortality table by contract vintage
  [REG-R10]. **The current numeric 標準利率 could not be established from a retrieved official
  document**: the mechanism is verified and the level is not, so any figure used downstream
  is **[std]** or [unverified] [REG-R10].
- **The two tables, again, and why the reserve needs both.** 生保標準生命表2018（死亡保険用）for the
  deferral phase and 生保標準生命表2007（年金開始後用）for the annuity in payment [REG-R10] [REG-R11] [R4].
  An annuity reserve computed off the death-cover table is wrong by construction and wrong
  in the expensive direction: the payout table is materially lighter at every adult age —
  male q80 = 0.03357 against 0.05006, q90 = 0.08318 against 0.15760 — and runs to terminal
  ages of 122 and 126 against 109 and 113 [R3] [REG-R18] [REG-R19].
- **危険準備金.** A contingency reserve inside the 第69条 taxonomy [REG-R8]. Not modeled.
- **ESR.** From 2026-03-31 the liability is 現在推計 + MOCE, assets are at fair value, and
  required capital is calibrated to 99.5% over one year, with early corrective action at an
  ESR below 100% where the old ソルベンシー・マージン比率 triggered below 200% [REG-R15] [REG-R17]. The
  cash flows above are the input to the 現在推計; `jplib` computes neither ratio. What a 35-year
  deferral followed by a ten-year payout owes the regime is that the projection be
  re-runnable on a basis re-set at a stated 基準日 — which is why every assumption in class (c)
  is an input and not a constant.
- **保険計理人の実務基準.** 保険業法第121条 requires an 意見書 confirming the reserve is properly accumulated
  [REG-R6], and the 実務基準 sets out how: the **1号収支分析** is a forward income-and-outgo analysis
  run annually by 区分経理 segment over **at least ten future years**, with sufficiency tested
  over the first five [REG-R22]. That is the shape of `result_cf()`.
- **J-GAAP and IFRS 17.** Statutory accounts are J-GAAP with 責任準備金 on the 平準純保険料式 [REG-R10];
  ESR is a regulatory measurement and not an accounting standard [REG-R15]; and Japan has
  **no mandatory IFRS 17** — IFRS applies as 指定国際会計基準 and adoption is voluntary [REG-R47].
  Three bases over one set of projected cash flows.
- **Policyholder protection.** 生命保険契約者保護機構 cover is 90% of the 責任準備金等 at the failure date,
  set in ordinance under the delegation at 保険業法第270条の3, with the 高予定利率契約 reduction
  [unverified] in detail [S4] [REG-R40] [REG-R41]. Not a cash flow in this model.

---

## Key sensitivities and model risks

In rough order of leverage on this block:

1. **The two 予定利率, and the gap between them.** `i_d` drives thirty-five years of
   accumulation and `i_p` converts the result into an annuity; both are fixed at issue and
   neither is a market rate. Moving `i_d` by 25bp moves `F` by +5.76% / −5.42%; moving `i_p`
   by 25bp moves `B` by about 1.1% in the opposite direction from what a single-rate model
   would show. One carrier bands `i_d` by years remaining to annuitisation — 1.20% at 30
   years or more, 1.00% below [S5] — so a model that hard-codes one deferral rate cannot
   price its own issue-age range consistently.
2. **The 予定事業費率 calibration.** `β` is the one free parameter standing between an unpublished
   算出方法書 [REG-R2] and a published specimen [S6]. It is calibrated at a single model point,
   male 30; the specimen table gives five more points [S6], and a production user should
   re-fit across all six rather than inherit a one-point calibration.
3. **Longevity on the payout table, and the sign of its margin.** With the life-annuity
   module on, `B` is bought with an annuity-due factor of 22.032668 instead of 9.714338, so
   it is the payout **table** and not the payout rate that carries the risk there: scaling
   that table by 1.10 moves the factor to 21.316734 and `B` up by 3.34%, and by 1.01 moves
   `B` up by 0.36%. The 2007 年金開始後用 table's construction was not retrieved, so the 1.10
   best-estimate factor is a standardization sitting on an [unverified] margin.
4. **Late-duration surrender, whose sign is the reverse of a savings product.** From the
   crossover the surrender value *is* the death benefit and so is capped at the premiums
   paid to date. A surrender at `t` = 29 therefore pays `cv_pp(29)` = ¥5,220,000 — the
   twenty-nine premiums paid by then, the benefit not reaching its ¥5,400,000 ceiling until
   払込満了 — against an `av_pp(29)` of ¥5,699,454.498584: the insurer *keeps* ¥479,454.50 of
   fund per surrender. Late-duration lapse is therefore **profitable** here, and a prudent
   reserving basis loads lapse down, not up.
5. **Early-duration surrender and the 解約控除.** The base amount of one annual premium is [std]
   and unsourced beyond the two 約款's 「ごくわずか」 [S2] [S4]. It moves `cv_pp` over the first ten
   years and therefore the whole early-duration lapse cost.
6. **Reinstatement, which this grid cannot carry.** 復活 within three years [S2] [S4] returns
   real policies to the in-force, so this model's `lapse_rate` is a net-of-復活 rate. A user
   substituting a gross experience lapse rate will over-decrement.
7. **The 据置期間 as a lever.** One carrier markets it explicitly — a deferral gap between 払込満了
   and the 年金支払開始日 increases the annuity [S6]. On the anchor cell `d` = 5 raises `F` from
   ¥5,929,599.05 to ¥6,261,482.08, +5.60%: 5.10% of it the interest factor 1.01^5 and the
   rest five more years of survivorship release. A model that never separates `m` from `n`
   silently sets `d` = 0.
8. **Dividend re-activation.** The base run's zero declared dividend is a choice, not a
   product fact. Turning it on adds a second interest lever, is subject to 消費者契約法第4条 on
   presenting non-guaranteed elements as certain [REG-R38], and under the rider must be
   applied as a single premium increasing the 基本年金額, never paid in cash [S1] [R10].

Known modeling pitfalls:

- **Two mortality tables in one model, with the margin running opposite ways.** The deferral
  phase reads 生保標準生命表2018（死亡保険用）and the payout phase 生保標準生命表2007（年金開始後用）[REG-R10] [REG-R11].
  Using the death-cover table after annuitisation overstates payout-phase deaths by 49% at
  age 80 and by 89% at age 90 on the **published** rates [R3] [REG-R18]. Those two death-cover
  rates are sourced anchors and come back exactly from `mort_table.csv`; the payout rates do
  not, because that table is anchored only at 60/80/100 and its Makeham construction reads
  0.077578 at age 90 against the published 0.08318, so a reader checking the 89% against the
  model's own tables will find 103% instead. And
  the best-estimate adjustment reverses sign at `t` = `n`: 0.85 on the death-cover table,
  1.10 on the annuity table. A model applying one factor to both has one of the two wrong.
- **確定年金 instalments are certain, not life-contingent.** Do not decrement `pols_if` by
  mortality during the payment period [S2] [R16]. Deaths inside the period pay the PV of the
  unpaid instalments, or the recipient elects continuation; the base run assumes
  continuation, so the stream is unchanged. `lives_if` falls from 0.91268274 to 0.77848987
  over the ten payout years without moving a single cash flow.
- **The surrender value never exceeds the death benefit, but the fund does — and that is the
  product.** `cv_pp(t) ≤ db_pp(t)` at every deferral duration [S2] [S4], with equality from
  `t` = 13 at the anchor cell. Clipping `av_pp` instead of `cv_pp` destroys the 年金原資: it is
  the un-clipped excess of `av_pp` over `db_pp` — ¥791,563.274447 by `t` = 34 — that buys
  the annuity.
- **The lapse decrement must stop before the 年金支払開始日.** A lapse applied in year `n − 1`
  removes contracts at `t` = `n`, where `cv_pp` = 0 and surrender is unavailable [S2] [S4]:
  in-force disappears with no payment and the annuity outgo is understated. `lapse_rate(t)`
  is zero for `t ≥ n − 1`, and there is no lapse and no surrender at all after
  annuitisation.
- **払込満了 and 年金支払開始日 are different dates.** `m` = 30 and `n` = 35 at the anchor cell.
  Collapsing the 据置期間 moves `F` by 5.60% and is not a rounding difference [S6]; a model with
  one "term" parameter cannot express the composite at all.
- **Two 予定利率, not one.** 1.00% accumulating and 0.65% converting [S5] [S8]. Using the
  deferral rate to buy the annuity overstates `B` by 1.55% at `k` = 10 — the payout rate is
  the lower one, so each yen of 年金原資 buys less annuity, not more.
- **The death benefit stops growing at 払込満了.** `db_pp(t)` = `ρPm` for every `t ≥ m`, because
  the contractual base is 月払保険料 × 経過月数 and no further premium is paid [S2] [S4]. A model
  that keeps accruing it to `n` overstates deferral-phase claims by five years' worth of
  premium.
- **The commutation factors are not the model's payout basis.** The published table [S2]
  implies about 0.40% p.a. while the payout 予定利率 is 0.65% [S5]; at `t` = `n` the factor
  9.921 returns ¥6,330,590.10 against a 年金原資 of ¥6,261,482.08, 1.1037% more. Base-run
  take-up is 0% for exactly that reason, and switching commutation on without re-deriving
  the factors builds a composite artefact into the answer.
- **The published lapse rate's denominator is 契約高, not policy count.** The 3.4% for FY2024
  is measured on pre-annuitisation in-force 契約高 [R15] [REG-R31]. The [std] curve averages
  3.4160% count-weighted and 2.4754% `av_pp`-weighted on the anchor cell, both over `t` = 0
  … `n` − 1. Calibrating a count model directly against the published number without saying
  which weighting is meant mis-states the deferral decrement by about a quarter.
- **Dividends are zero in the base run, not absent, and may never be paid in cash.** The
  machinery is contractual [S4]; under the rider the accumulated dividend cannot be
  withdrawn before annuitisation and must be applied as a single premium increasing the
  基本年金額 [S1] [S2], as 所令211①ニ requires [R10]. A model that pays a declared dividend as a
  cash outflow before `t` = `n` is projecting a non-qualifying contract.
- **自動振替貸付 is an election, not a no-lapse rule.** With the module on, the lapse decrement is
  suppressed only while the surrender value can carry the premium, the loan compounds at a
  rate capped at 8% p.a., and the contract lapses from the moment principal and interest
  exceed the surrender value [S4] [REG-R14]. One carrier's product has no such facility at
  all [S2]. Wiring it on by default removes lapse from the model for the wrong reason.
- **The 基本年金額 is fixed at issue on the base form and priced at annuitisation on the elected
  one.** For the 確定年金 chosen at issue, `B` is struck once, at `t` = `n`, from the issue
  basis [S2] [S3]. The 保証期間付終身年金 election is priced on the 基礎率 in force at the 年金支払開始日 [S2]
  [S9], which no model can know; holding it at the issue basis is a **[std]** assumption and
  the reason base-run take-up is zero. Sharing one code path between the two hides that
  distinction, and the two answers are far apart: ¥638,100 against ¥281,300 out of the same
  ¥6,261,482.08.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #jplib-individual_annuity-r10
[R13]: #jplib-individual_annuity-r13
[R15]: #jplib-individual_annuity-r15
[R16]: #jplib-individual_annuity-r16
[R2]: #jplib-individual_annuity-r2
[R3]: #jplib-individual_annuity-r3
[R4]: #jplib-individual_annuity-r4
[R5]: #jplib-individual_annuity-r5
[REG-R10]: #jplib-reg-r10
[REG-R11]: #jplib-reg-r11
[REG-R12]: #jplib-reg-r12
[REG-R14]: #jplib-reg-r14
[REG-R15]: #jplib-reg-r15
[REG-R16]: #jplib-reg-r16
[REG-R17]: #jplib-reg-r17
[REG-R18]: #jplib-reg-r18
[REG-R19]: #jplib-reg-r19
[REG-R2]: #jplib-reg-r2
[REG-R20]: #jplib-reg-r20
[REG-R21]: #jplib-reg-r21
[REG-R22]: #jplib-reg-r22
[REG-R31]: #jplib-reg-r31
[REG-R38]: #jplib-reg-r38
[REG-R4]: #jplib-reg-r4
[REG-R40]: #jplib-reg-r40
[REG-R41]: #jplib-reg-r41
[REG-R46]: #jplib-reg-r46
[REG-R47]: #jplib-reg-r47
[REG-R6]: #jplib-reg-r6
[REG-R7]: #jplib-reg-r7
[REG-R8]: #jplib-reg-r8
[REG-R9]: #jplib-reg-r9
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
