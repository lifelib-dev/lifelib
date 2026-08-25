# Technical Notes

**Status:** Draft, 2026-08-20 (all cited sources accessed 2026-08-20).

**Scope note.** These notes turn the standardized composite of `product-spec.md` (same
directory) into a reference liability cash-flow projection on paper. They describe no single
insurer's contract. [S#] and [R#] resolve against `sources.md` in this directory, numbering
carried verbatim from `_research/income-guarantee.md` and frozen; [REG-R#] resolves against
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is distinct and
must never be read across. **[std]** marks a standardization introduced for the reference
implementation; [unverified] marks a claim not confirmed against a retrieved document.
**Every contractual parameter here is identical to `product-spec.md`'s.** Two parameters are
new, and both are named as such where they appear: a **rate-class mortality factor**, which
`product-spec.md` footnote 6 explicitly defers to this file because no carrier publishes the
premium differential between classes, and a **per-instalment annuity administration
expense**, which the chassis has no need of because the chassis pays a lump sum.

**This is a death benefit.** Survivor income term (*shūnyū hoshō hoken*, 収入保障保険) pays on the
death of the insured, or on the contractual severe disability state (*kōdo shōgai jōtai*,
高度障害状態) treated as its accelerated equivalent, and pays it as a monthly income. It is **not**
income protection in `uklib`'s sense; `uklib`'s `IP_UK_S` insures disability. Nothing in
this file models a disability decrement.

**This file states deltas.** The [term life technical notes (定期保険)](../term_life/technical-notes.md)
are the library's protection chassis, implemented in
[`Term_JP_A`](../term_life/model.md). Inherited unchanged and **not restated here**: the
decrement recursion and its processing order, the premium chassis, the **[std]** mortality
construction with its 0.80 best-estimate factor, the lapse table, the expense and commission
levels, the age last birthday (*man-nenrei*, 満年齢) / age nearest birthday (*hoken-nenrei*,
保険年齢) age-basis reconciliation, and the treatment of 高度障害 as one decrement with death.
What changes: a monthly grid, a benefit that is an annuity-certain rather than a lump sum, a
premium stream that stops on the annuity event while the benefit stream runs on, and a
projection horizon that is **longer than the policy term**.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows — premiums, the death and
  高度障害 annuity instalments, claim expenses, annuity administration expenses, maintenance
  expenses and commission — for a single-policy model point, in the sense the ESR current
  estimate (*genzai suikei*, 現在推計) requires: probability-weighted future cash flows on
  assumptions re-set at the 基準日 rather than locked in at issue [REG-R15]. The same
  projection is the shape of the item-1 income-and-outgo analysis (*ichi-gō shūshi bunseki*,
  1号収支分析) [REG-R22].
- **Discounting, MOCE, required capital and reserving are out of scope**, cited and not
  reproduced (see Valuation and reserve pointers). `jplib` computes no ratio and builds no
  policy reserve (*sekinin-junbikin*, 責任準備金). The omission matters more on this product
  than on any other protection product in the library, and Key sensitivities quantifies why.
- **Projection frequency.** Monthly — the model is `IncomeTerm_JP_S`. The grid is not a
  refinement here, it is the contract: the benefit is one instalment per monthly payment
  date [S1 第3条第2項] [S5], the instalment count is a month count [S5] [S14] [S15], and the
  minimum payment guarantee period (*saitei shiharai hoshō kikan*, 最低支払保証期間) is stated in
  years but binds in months. An annual grid cannot represent `max(N − m + 1, G)` without
  inventing a within-year convention for both `m` and `G`.
- **Timing conventions [std].** Premium at the **start** of each policy month, in advance,
  on the in-force population only; maintenance expense at the start of the month;
  acquisition expense and initial commission at issue. Claims arise at the **end** of the
  month, and the claim expense with them. The **first annuity instalment falls at the end of
  the month of the insured event** and each later instalment at the end of each later month
  — the contractual timetable is the day before the first monthly policy anniversary falling
  on or after the event, then the day before each subsequent anniversary [S1 第3条第2項] [S5],
  which on a monthly grid is exactly one payment per month starting in the month of the
  event. Lapse at the end of the month, after deaths. **Premium frequency is a timing
  feature, not an inert flag [std]:** on 半年払 and 年払 the premium falls as `12 / f` months'
  premium at the start of each payment period and nothing in between, with no 前納 and no
  frequency discount applied because the discount is insurer-set and unpublished
  [S1 第14条] — so a policy year costs the same at all three frequencies and only the timing
  moves. The worked example is 月払, the frequency the only published rate grid is quoted
  in [S6].
- **Age basis [std].** Issue age (*keiyaku nenrei*, 契約年齢) is 満年齢 with the fraction
  truncated [S1 第37条] [S14]; attained age in month `t` is
  `x + floor((t − 1) / 12)`. 生保標準生命表2018（死亡保険用）is built for a 保険年齢
  basis [REG-R20] [R2], so reading it at 満年齢 reads it
  half a year early and understates mortality. The chassis states the bias and the optional
  `sqrt(q_x · q_{x+1})` shift; both apply here unchanged.
- **Currency.** JPY throughout [S1]. No FX layer.
- **Model points.** Single-policy, on an expected (probability-weighted) basis. The anchor
  cell of the worked example is `point_id = 1`.
- **Termination — and the sentence this product exists to force.** The policy terminates at
  the end of the policy term (*hoken kikan*, 保険期間) with nothing payable on survival: no
  満期保険金, no surrender value (*kaiyaku-henreikin*, 解約返戻金) at any duration [S2] [S5] [S6]
  [S7] [S9] [S15]. **But cash flow does not stop there.** Where the insured event falls so
  late that fewer than `G` months remain, the annuity payment period is **extended past the
  expiry date** until the guarantee has run [S1 第3条第2項] [S3 第3条第3項] [S5] [S12] [S14]. The
  projection horizon is therefore

      T = N + G − 1

  months, not `N`. On the anchor cell `N = 420` and `G = 24`, so `T = 443`: a death in
  policy month 420 pays its twenty-fourth instalment in month 443, twenty-three months after
  cover ended. Terminating the projection at `t = N` truncates real, contractual liability,
  and it is the single easiest error to make in an implementation of this product.
- **Contract boundary.** Unlike the chassis, this contract has no renewal (*kōshin*, 更新) in
  any retrieved document [S5] [S6] [S8], and the premium is level and guaranteed for the
  whole 保険期間 with no review mechanic [S1] [S2] [S5] [S6] [S8] [S12]. The insurer therefore
  has no unilateral repricing right, the boundary is the full term, and the boundary
  argument that dominates the [term life technical notes (定期保険)](../term_life/technical-notes.md) does
  not arise here. The run-off
  tail in months `N + 1 … T` is inside the boundary: it is the settlement of a claim that
  arose inside it.
- **Rounding.** Intermediates at full precision; displayed cash flows to two decimals of a
  yen; in-force to six decimals; **the claim and annuity-ledger populations to nine
  decimals** **[std]**. Nine is not decoration: on a monthly grid at age 30 the monthly
  claim probability is about 3.2e−5, so six decimals leaves the first policy year's claim
  and ledger populations with two significant figures — `D(1) = 0.000031739` displays as
  0.000032, a 0.8% distortion of the largest single component of the benefit, and the
  twelve months of policy year 1 collapse onto four distinct displayed values.

---

## Model point attributes

| Attribute | Type | Anchor cell (`point_id = 1`) |
|---|---|---|
| `sex` | enum {M, F} | M |
| `issue_age` (`x`) | int, 満年齢, 20–70 [S6] [S7] [S14] | 30 |
| `expiry_age` | int, 45–90 [S8]; 歳満了 only, no 年満了 and no 更新 [S5] [S6] | 65 |
| `term_m` (`N`) | int months, `12 × (expiry_age − issue_age)` — derived | 420 |
| `guar_m` (`G`) | int months, from {24, 60} [S3] [S5] [S7] [S9] [S12] | 24 |
| `annuity_mth` (`A`) | JPY/month, ¥50,000 minimum in ¥10,000 steps [S6] [S8] [S12] | 150,000 |
| `rate_class` | enum {非喫煙者優良体, 喫煙者優良体, 非喫煙者標準体, 喫煙者標準体} [S2] [S5] [S14] | 非喫煙者優良体 |
| `class_factor` | float, mortality multiplier for the class | **0.70 [std]** |
| `premium_monthly` (`P_m`) | JPY/month | **2,565** [S6] |
| `premium_mode` | enum {monthly, semiannual, annual} [S1 第12条] | monthly |
| `commutation` | bool (一括受取 at the claim date; base run false) | false |
| `living_needs` | bool (リビング・ニーズ特約; base run false) | false |
| `wop` | bool (保険料払込免除; base run false) | false |
| `reinstatement` | bool (復活 module; base run false) | false |

`P_m` is a **published** figure: ¥2,565 is the 65歳満了 / 保証2年 / 非喫煙優良体型 / 年金月額¥150,000 monthly
rate for a male aged 30, as at 2025年12月2日 [S6]. Two honest qualifications carried over from
`product-spec.md` footnote 7: the publishing carrier runs a **two**-class structure, so its
非喫煙優良体型 is not exactly the composite's 非喫煙者優良体 cell, and the total-benefit illustration the
cell is checked against is written on a 5年 guarantee by a different carrier [S14], which
changes nothing before the last two policy years. **[std]** here covers the choice of cell
and nothing else about the premium.

`term_m` is **derived, not an input**: every published contract example sets the term as
to a stated attained age (*sai manryō*, 歳満了) [S2] [S5] [S6] [S8] [S9] [S12] [S14] [S15]
[S17]. A model point supplying an n-year term is describing a product the composite does not
have.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `l(t)` | In-force probability at the **start** of month t; `l(1) = 1`; **`l(t) = 0` for t > N** | monthly recursion |
| `q(t)` | Best-estimate annual death-and-高度障害 rate (**one** decrement) at attained age | assumption lookup |
| `q_m(t)` | Monthly equivalent, `1 − (1 − q(t))^(1/12)` | derived |
| `w(t)`, `w_m(t)` | Annual and monthly ordinary lapse rate | assumption lookup |
| `D(t)` | Expected new claims in month t = `l(t) × q_m(t)` | monthly |
| `R(t)` | **Annuity streams in payment during month t** — the in-payment ledger | monthly recursion |
| `CF(t)` | Net cash flow of month t, insurer perspective (+ = inflow) | monthly |

`R(t)` is the state variable this product adds to the chassis, and it obeys a rule that has
no analogue anywhere else in `jplib`:

> **The in-payment ledger is never decremented.** Not by the insured's mortality — the
  insured
> is dead, and that is what opened the stream. Not by the recipient's mortality — on the
> composite the instalments carry **no survival condition** [S1] [S5] [S14], so the stream
  is
> an annuity-certain. Not by lapse — a policy in claim cannot lapse, and premiums have
  ceased
> [S1 第12条第2項] [S3 第5条] [S8]. `R(t)` falls only when a stream reaches its contractual last
> instalment.

There is deliberately **no** `cv_pp` and no account value: the composite has no 解約返戻金 for
the whole term [S2] [S5] [S6] [S7] [S9] [S15], and with no cash value there is no automatic
premium loan (*jidō furikae kashitsuke*, 自動振替貸付) and no 契約者貸付 — one carrier states the
absence in terms [S2]. Grace to 失効 to 復活-or-not is the whole persistency machinery, exactly
as on the chassis.

Two contractual clocks are tracked and not monetized in the base run: the **three-year**
suicide 免責期間 and the **two-year** 告知義務違反 contestability window, both running from the
責任開始期 and both restarted only by 復活 [S1] [S3] [S4] [S5] [REG-R34] [REG-R35].

---

## Assumption inputs

Three classes, kept separate.

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Survivor annuity (*izoku nenkin*, 遺族年金) | `A` per month from the insured event to the 保険期間満了日, extended where the guarantee requires | [S1 第3条] [S3 第3条] [S5] [S9] [S12] [S14] |
| 高度障害年金 | **The same `A`**, same timetable, same guarantee; mutually exclusive with the death annuity | [S1 第3条] [S3 第3条] [S5] [S9] |
| Instalment count | `n_pay(m) = max(N − m + 1, G)` | derivation below; [S5] [S14] [S15] |
| Guarantee mechanic | A **term extension past expiry**, not a benefit floor inside the term | [S1 第3条第2項] [S3 第3条第3項] [S5] [S12] [S14] |
| Survival condition | **None**; the stream is an annuity-certain | [S1] [S5] [S14] |
| Premium | Level for the whole 保険期間; 保険料払込期間 = 保険期間; no review, no 更新 | [S1] [S2] [S5] [S6] [S8] [S12] |
| Premium cessation | **On the annuity event**: no further premium once the annuity begins | [S1 第12条第2項] [S3 第5条] [S8] |
| 解約返戻金 | **None**, whole term | [S2] [S5] [S6] [S7] [S9] [S15] |
| Grace (*yūyo kikan*, 猶予期間), 月払 | To the last day of the month after the 払込期月; then 失効 | [S1 第15条] [S3] [S4] |
| 復活 | 3 years from lapse, on fresh underwriting and arrears with interest; rate class carries over | [S1 第17条] [S3] [S5] |
| Suicide 免責 | 3 years from the 責任開始期, reset on 復活; 責任準備金 paid to the owner | [S1] [S3] [S4] [S5] |
| Commutation (一括受取) | Present value of unpaid instalments, in whole, in part, or as the residue | [S2] [S3] [S5] [S7] [S10] [S12] [S14] |
| Residual floor | A partial commutation leaving 年金月額 below ¥50,000 is refused | [S7] [S1 第5条第3項] [S3 第6条第4項] |
| Benefit cap | 年金現価保険金額 ¥300,000,000 — a cap on the **present value** | [S8] |
| リビング・ニーズ特約 | 年金現価 of the designated 年金月額 less 6 months' interest and premium; cap ¥30,000,000; barred in the final year | [S2] [S5] [S7] |
| 保険料払込免除 | 不慮の事故 on or after 責任開始期, 別表4 state within 180 days; disease-based waiver is a rider only | [S1 第6条] [S3 第8条] [S5] [S6] |

**Deriving the instalment count.** With `N` the term in months, `m` the policy month of the
insured event and `G` the guarantee in months, `n_pay(m) = max(N − m + 1, G)` reproduces
every published illustration in the source set. On `N = 420`: 420 instalments for `m = 1`,
240 for `m = 181`, 60 for `m = 361` [S14]; 411 for `m = 10` and 178 for `m = 243` [S15]; and
on a 5年 guarantee, 420 for `m = 1`, 246 for `m = 175`, and **60** for a death 33 years in,
where the remaining term is 24 months and the guarantee binds [S5]. Carriers label elapsed
duration inconsistently — one counts the month of the event, another counts completed months
— but the guarantee case is the only one where the two conventions could not both hold, and
it holds.

The stream opened in month `m` therefore pays its **last** instalment in month

      ends_at(m) = m + n_pay(m) − 1 = max(N, m + G − 1)

which is the whole guarantee mechanic in one expression, and the expression a test should
assert. For `m ≤ N − G + 1` every stream ends at exactly `N`; only later claims run past it.

### (b) Insurer-discretionary current elements

| Input | Snapshot value | Basis |
|---|---|---|
| 契約者配当 | **Nil** — every retrieved product is 無配当 | [S1 第39条] [S2] [S5] [S15] |
| Commutation basis | Annuity-certain at **0.65% p.a. effective**, monthly in arrears | **[std]** (1) |
| 前納 discount, 高額割引 | Insurer-set and unpublished; not modeled | [S1 第14条] [S6]; scope **[std]** |
| Pricing basis (assumed interest rate (*yotei riritsu*, 予定利率), 予定死亡率, 予定事業費率) | **Not published for any 収入保障 contract in the set**; filed under 保険業法第4条第2項第4号 and not public | [REG-R2]; gap |

1. **The most important [std] number in this product, and the best-evidenced.** No direct
   writer publishes the discount basis; the wordings are 「年金月額に所定の係数を乗じた額」 [S6] and
   「将来に発生する利息を差し引いて算出した現在の保険契約の価値」 [S10]. One 特約条項 publishes the **factor tables
   themselves** — 年金の現価相当額 = 基本年金額 × a tabulated rate with **no dependence on the
   annuitant's age or sex**, running 4.975 at a 5-year payment period, 9.801 at 10, 14.474
   at 15, 18.997 at 20, 23.377 at 25, 27.616 at 30 and 39.542 at 45 [S13 別表1]. Fitting an
   annual annuity-due **less a small constant** to those gives about **0.61% p.a.**, and the
   second column of the same table, for a different main contract, about **1.45%**; both
   fits are derivations recorded in `_research/income-guarantee.md`, not published rates,
   and the constant is part of the derivation — a plain annuity-due with no constant fits
   the same seven factors at 0.59%. Three carriers publish a worked
   commutation amount instead: ¥100,000 × 180 to ¥16,594,260 [S6], ¥200,000 × 300 to
   約¥55,310,000 [S10] and ¥100,000 × 300 to 約¥27,640,000 [S17] — ratios of 0.92190, 0.92183
   and 0.92133, implying 1.10%, 0.66% and 0.66% respectively. The two independent anchors —
   0.61% from the factor table and 0.66% from the two 300-instalment amounts — have a
   midpoint of 0.635%; the composite takes that rounded to the nearest 0.05%, **0.65% p.a.
   effective**. Verified numerically at that rate, monthly in arrears: ¥200,000
   × 300 commutes to **¥55,377,890.69** (+0.12% on the published 約 amount) and ¥100,000 ×
   300 to **¥27,688,945.35** (+0.18%), both inside the published rounding. It does **not**
   reproduce the 180-instalment amount: at 0.65% that stream commutes at **¥17,148,368.65**,
   a ratio of **0.952687** against the published 0.921903. That is a fact about the data,
   not a failure of the fit — no single flat rate produces a near-constant ratio at both 180
   and 300 instalments, so either the carriers' bases differ or a term-dependent adjustment
   is in use, and neither is published. **Observed range to test over: 0.61%–1.45%.**

### (c) Behavioral / experience assumptions (modeler's view — all [std])

**Mortality — one decrement.** 生保標準生命表2018（死亡保険用）**includes 高度障害 inside its death rate**
[R2] [REG-R20], and the contract pays one annuity and the other is then not payable [S1
第3条第3・4項] [S3 第3条第6・7項]. Death and 高度障害 are therefore one decrement carrying one benefit.
The table is freely readable at a stable public URL [R1] [REG-R18] but its publisher
prohibits reproduction and transmission without written consent [REG-R21], so the library
**cites** the table, **quotes** the rates the worked example needs, and **ships**
`mort_table.csv` as a **[std]** construction whose `provenance` column points at the IAJ
entries.

| Step | Rule | Basis |
|---|---|---|
| Anchors verified for this product | Male 死亡保険用 `q30 = 0.00068`, `q60 = 0.00653`, `q65 = 0.01015`, `q80 = 0.05006`; female `q60 = 0.00363` | read from the table [R1] [REG-R18] |
| Anchors carried from the chassis | Male `q35 = 0.00077`, `q40 = 0.00118`, `q50 = 0.00285`, `q90 = 0.15760`; female `q30 = 0.00037` | [term life technical notes (定期保険)](../term_life/technical-notes.md) |
| Shipped anchors | The **union** of every anchor any `jplib` product reads from the table: both sexes at ages 20, 22, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80 and 85, plus male 31–34 | one canonical **[std]** file, so a cell carries the same value and the same provenance in every product that ships it |
| Female rates | Read at the female anchors in their own right, not built as a ratio to the male rate | [R1] [REG-R18] |
| Interpolation | Log-linear in `ln q` between the two **neighbouring** anchors, rounded to 5 decimals; no extrapolation anywhere, because every shipped age lies between two sourced anchors | **[std]** |
| Best estimate | `q(t) = 0.80 × class_factor × q_x^tab` | chassis 0.80 **[std]**; class factor **[std]** (2) |
| Monthly conversion | `q_m = 1 − (1 − q)^(1/12)` | **[std]** |
| Improvement | None in the base run | **[std]** |

2. **The rate-class factor is the parameter `product-spec.md` footnote 6 defers to this
   file.** The composite has four classes [S2] [S5] [S14], their qualification is published
   and **measured rather than declared** — BMI 18.0 to under 27.0, 最大血圧 under 140 and 最小血圧
   under 90 mmHg, no tobacco in the past year, verified by a cotinine (コチニン) test [S2] [S5]
   — and **no carrier publishes the premium differential between them.** The reference set
   is therefore wholly **[std]**, given a stated internal structure rather than four free
   numbers:

   | Class | `class_factor` **[std]** |
   |---|---|
   | 非喫煙者優良体 | 0.70 |
   | 非喫煙者標準体 | 0.90 |
   | 喫煙者優良体 | 1.05 |
   | 喫煙者標準体 | 1.35 |

   The structure is a smoker/non-smoker ratio of **1.50** and a preferred/standard ratio of
   **0.778**, applied consistently in both directions, and the levels are pinned by one
   arithmetic constraint: 生保標準生命表2018 is an **all-lives** basis, so the mix-weighted mean of
   the four factors must be 1.00 or the class split silently re-levels the whole table. An
   illustrative mix of 25% / 35% / 10% / 30% gives exactly 1.000:

       0.25 * 0.70 + 0.35 * 0.90 + 0.10 * 1.05 + 0.30 * 1.35 = 1.000

   The mix is **[std]** and illustrative; it is used to check the normalization and is not a
   claim about the market. No observed range can be given, because nothing is published.

**Lapse.** The chassis table, unchanged and reconciled there to the LIAJ's FY2024 個人保険
解約・失効率 of **5.6%** [REG-R31]:

| Policy year | 1 | 2 | 3 | 4 | 5+ |
|---|---|---|---|---|---|
| Annual `w(t)` **[std]** | 9% | 7% | 6% | 5.5% | 5% |

with `w_m(t) = 1 − (1 − w(t))^(1/12)` **[std]**. Lapse pays nothing: there is no 解約返戻金
[S2] [S5] [S6] [S7] [S9] [S15]. Nothing product-specific was found — the national household
survey does not break 収入保障保険 out at all [R11] [REG-R32] — so this table is the chassis's
table used because it is the only one the library has, not because it was calibrated here.

**Expenses and commission.** All chassis levels, unchanged, plus one new item.

| Input | Value | Note |
|---|---|---|
| Acquisition expense `E0` | ¥15,000 per policy at issue | chassis **[std]** |
| Initial commission `c0` | 50% of the first-year annualized premium | chassis **[std]** |
| Renewal commission `c_r` | 5% of premiums from month 13 | chassis **[std]** |
| Maintenance `e_m(t)` | ¥4,000 p.a. inflating 1.0% p.a., taken as `4,000 / 12` per month | chassis **[std]** |
| Claim expense `ec` | ¥30,000 per claim, once, when the stream opens | chassis **[std]** |
| **Annuity expense `ea`** | **¥200 per instalment paid** | **new [std]** (3) |

3. The chassis pays a lump sum and closes the file. This product pays up to 420 instalments
   over up to 35 years after the claim, and the administration of that stream is a real cost
   that no cited document quantifies. `ea` is charged against the **ledger** `R(t)`, not
   against `l(t)` — it is the one expense that survives the end of the policy term. The
   level is a **[std]** placeholder; its cash-flow weight on the anchor cell is small
   (¥591.08 undiscounted per policy issued against ¥443,313.69 of claims) but its
   *structure* is the point: an implementation that attaches every expense to `l(t)` charges
   nothing at all in months 421–443, when instalments are still being paid.

---

## Cash flow components and recursions

### Notation

| Symbol | Meaning | cells |
|---|---|---|
| `t` | policy month, `t = 1 .. T` | — |
| `x` | 契約年齢 (満年齢); attained age in month t is `x + floor((t − 1) / 12)` | `age` |
| `y(t)` | policy year, `1 + floor((t − 1) / 12)` | `policy_year` |
| `N` | 保険期間 in months, `12 × (expiry_age − x)` | `term_m` |
| `G` | 最低支払保証期間 in months | `guar_m` |
| `T` | projection horizon in months, `N + G − 1` | `proj_len` |
| `A` | 年金月額, JPY per month | `annuity_mth` |
| `P_m` | monthly office premium, JPY per month | `premium_mth_pp` |
| `P_due(t)` | office premium falling due at the start of month t | `prem_due_pp` |
| `n_pay(m)` | instalments generated by a claim in month m, `max(N − m + 1, G)` | `pay_count` |
| `ends_at(m)` | month of that stream's last instalment, `max(N, m + G − 1)` | `pay_end` |
| `q(t)`, `q_m(t)` | annual and monthly death-and-高度障害 rate | `mort_rate`, `mort_rate_mth` |
| `w(t)`, `w_m(t)` | annual and monthly ordinary lapse rate | `lapse_rate`, `lapse_rate_mth` |
| `l(t)` | in-force probability at the start of month t | `pols_if` |
| `D(t)` | expected new claims in month t, `l(t) × q_m(t)` | `pols_death` |
| `R(t)` | annuity streams in payment during month t | `annuities_if` |
| `E0`, `c0`, `c_r` | acquisition expense; initial commission; renewal commission rate | `expense_acq`, `commissions` |
| `e_m(t)` | monthly maintenance, `(4,000 / 12) × 1.01^(y(t) − 1)` | `expenses` |
| `ec`, `ea` | claim expense per claim; annuity expense per instalment | `expense_claim`, `expense_annuity` |
| `i_c`, `v` | commutation rate p.a. effective; `v = (1 + i_c)^(−1/12)` | `commute_rate` |
| `CF(t)` | net cash flow of month t (+ inflow) | `net_cf` |

**Dimensional check.** `q`, `q_m`, `w`, `w_m`, `l`, `D`, `R` are dimensionless — `l` and `D`
are probabilities per policy issued, and `R` is a **count of instalments falling due**, also
per policy issued, so it is dimensionless in the same sense and is *not* a population of
policies. `A`, `P_m`, `e_m`, `ea` are JPY **per month**; `E0`, `c0`, `ec` are JPY per event;
`n_pay` and `ends_at` are month counts. Every term of `CF(t)` is JPY per month per policy
issued. The two products that must not be confused: `A × R(t)` is JPY per month (annuity
outgo) while `A × n_pay(m)` is JPY (the total benefit for one claim).

### The in-payment ledger

The ledger is the whole model. For `t = 1 .. T`:

    R(t) = R(t−1) − ended(t) + D(t),        R(0) = 0

    ended(t) = sum of D(s) over all s with ends_at(s) = t − 1

`D(t)` enters `R(t)` in the **same** month, because the first instalment falls at the end of
the month of the event. Two cases exhaust `ended(t)`:

    ended(t) = sum of D(s) for s = 1 .. N − G + 1     if t = N + 1
             = D(t − G)                               if t > N + 1
             = 0                                      otherwise

The first case is the structural fact worth a test: **every stream opened in months 1 … N −
G + 1 pays its last instalment in month `N` exactly**, whenever it opened, because the
expiry date is fixed at issue. It follows immediately that

    R(N) = sum of D(s) for s = 1 .. N

— the ledger at the last month of cover equals every claim the contract has ever made. Two
further identities a model must satisfy:

    R(t) = sum of D(s) over s with s <= t <= ends_at(s)          (direct form)
    sum over t of R(t) = sum over s of D(s) * n_pay(s)           (total instalments)

`check_annuity_ledger()` asserts the recursion against the direct form at every `t` and
returns a single `bool`.

### Processing order

For `t = 1 .. T`, in this order **[std]**:

1. **Start of month — income and standing outgo, on the in-force population only.** Premium
   `P_due(t) × l(t)`; maintenance `e_m(t) × l(t)`; renewal commission `c_r × P_due(t) × l(t)`
   for `t ≥ 13`. At `t = 1` additionally `E0 + c0` per policy issued (`l(1) = 1`). For
   `t > N` all four are zero: cover has expired and `l(t) = 0`. `P_due(t)` is the premium
   *falling due* in month `t`, which on the anchor cell's 月払 is `P_m` every month; see the
   frequency rule in Timing conventions.
2. **Decrement lookup.** `q(t)` at attained age `x + floor((t − 1) / 12)`; `q_m(t)` from it;
   `w(t)` from the lapse table by `y(t)`; `w_m(t)` from it. For `t > N`, all zero.
3. **End of month — new claims.** `D(t) = l(t) × q_m(t)`. Claim expense `ec × D(t)`. **No
   lump sum is paid.** The claim opens an annuity stream; it does not settle one.
4. **End of month — the ledger.** `R(t) = R(t−1) − ended(t) + D(t)`. Annuity outgo `A ×
   R(t)`; annuity expense `ea × R(t)`. This step runs for every `t` up to `T`, including the
   months after the policy term has ended.
5. **End of month — ordinary lapse.** `l(t) × (1 − q_m(t)) × w_m(t)` leave, applied to
   survivors of mortality. **Nothing is paid.**
6. **Roll forward.**

       l(t+1) = l(t) * (1 - q_m(t)) * (1 - w_m(t))     for t < N
       l(t+1) = 0                                       for t >= N

   The identity `l(t) − l(t+1) = D(t) + lapses(t)` holds for `t < N`, and `check_pols_roll_fwd()`
   asserts it over all such `t`. At `t = N` the survivors leave with nothing: on the anchor
   cell that is 0.144342 of the original cohort.

### Net cash flow

    CF(t) = P_due(t) * l(t)                        (premiums)
          - A * R(t)                               (annuity instalments)
          - ea * R(t)                              (annuity administration)
          - ec * D(t)                              (claim expense)
          - e_m(t) * l(t)                          (maintenance)
          - c_r * P_due(t) * l(t) * 1{t >= 13}     (renewal commission)
          - (E0 + c0) * 1{t = 1}                   (acquisition)

`net_cf` is income-positive, per the library convention. Lapse contributes no term: it acts
only through `l(t)`, and `claims_lapse` is identically zero — the zero is the product fact
worth publishing. Note which population multiplies which term: **premiums, maintenance and
commission carry `l(t)`; the annuity instalments and the annuity expense carry `R(t)`; and
`l(t)` and `R(t)` are disjoint populations that must never be added.**

### Optional modules (all off in the base run)

**The numeric values, first.** Each module below is switched off in the base run, so none of
these numbers touches the worked example — but the **[std]** rule is that a quantitative
parameter is written down with its rationale wherever it lives, not left to be read off the
model. Four rows are **contractual and cited** (`ln_defer_m`, `ln_cap`, `reinst_window_m`,
and `commute_rate` through its own footnote); **no retrieved document quantifies any of the
other seven**, so no observed range can be given for them. The "why this value" column says
what each number is chosen to *do*; a user switching a module on should replace the row
rather than calibrate to it.

| Module | Parameter | Value **[std]** | Why this value |
|---|---|---|---|
| リビング・ニーズ特約 | `ln_take_up` | **5%** of the month's claims | A visible but non-dominant election, chosen so the module changes the claim mix without swamping it. The rider's *presence* is sourced [S2] [S5] [S7]; only the take-up is invented |
| リビング・ニーズ特約 | `ln_defer_m` | **6** months | Contractual, not chosen: the payout is the 年金現価 less six months' interest and premium equivalent [S2] [S5] [S7] |
| リビング・ニーズ特約 | `ln_cap` | **¥30,000,000** | Contractual [S2] [S5] [S7] |
| 保険料払込免除 | `wop_inc_rate` | **0.06% p.a.** | An order of magnitude below `q(t)` at the older ages the waiver bites at, because 別表4 is a lower bar than 別表3 but the trigger still requires an 不慮の事故 plus a 180-day survival — a *deliberately* separate rate, so that no reader mistakes it for the 高度障害 incidence |
| 保険料払込免除 | `wop_rec_rate` | **10% p.a.** | A mean stay of about ten years in the waived state: the 別表4 states are permanent impairments, so recovery is slow rather than absent, and a zero recovery rate would make the waived fraction monotone and hide the two-state structure |
| 復活 | `reinst_rate` | **15%** of each month's lapses | Below the mid-range of what a three-year 復活 window could deliver, on the view that a 無解約返戻金型 policy gives an owner nothing to protect by reinstating. It is a single-lag approximation, so this rate carries the whole window's take-up |
| 復活 | `reinst_lag_m` | **6** months | One lag standing for the whole three-year window, set at the point where arrears are still small enough to be paid in one instalment. The model rejects a lag outside `reinst_window_m` by name |
| 復活 | `reinst_window_m` | **36** months | Contractual: 復活 runs three years from lapse [S1 第17条] [S3] [S5] |
| 復活 | `reinst_int_rate` | **0.65% p.a.** | 復活 requires arrears **with interest** [S1 第17条], and no carrier publishes the rate. Set equal to `commute_rate`, the one interest basis this product has any published evidence for, rather than introducing a second unevidenced rate |
| Selective lapsation | `sel_lapse_lambda` | **0** | Off in the base run; the mechanism is real but unquantified (Policyholder behavior modeling) |
| Selective lapsation | `sel_lapse_ref` | **1.0** | The threshold `l_ref` is expressed as a fraction of the original cohort, so 1.0 makes the loading start at issue and grow as the cohort runs off. It has no effect while `λ = 0` |
| 一括受取 | `commute_rate` | **0.65% p.a. effective** | The one **[std]** number here with published anchors; assumption class (b) footnote 1 carries the derivation and the 0.61%–1.45% observed range |

- **Commutation (一括受取).** With `commutation = true`, a claim in month `m` is settled at the
  claim date by a lump sum instead of the stream:

      L(n) = A * v * (1 - v^n) / (1 - v),    v = (1 + i_c)^(-1/12),  n = n_pay(m)

  at `i_c = 0.65%` **[std]**. The ledger is then not opened and the annuity expense
  collapses to one payment. On the anchor cell a death in month 1 commutes ¥63,000,000 of
  instalments to **¥56,352,381.90**, a ratio of **0.894482**; at 300 remaining instalments
  the ratio is **0.922965**, against the 0.92133–0.92190 the three published illustrations
  show [S6] [S10] [S17]. Contractually a full commutation **extinguishes the contract** [S1
  第5条第2項] [S3 第6条第3項] [S12] [S14], so in a projection it changes the shape of the claim
  payment and nothing else. Partial commutation (一部一括受取) is **not** modeled: it is barred
  once the first instalment has been paid [S3 第6条第4項第1号], limited to once during the term at
  two carriers [S10] [S12], and refused where the residual 年金月額 falls below ¥50,000 [S7] —
  three restrictions that make it an election on a claim already open rather than a
  cash-flow shape **[std scope]**.
- **リビング・ニーズ特約.** Acceleration incidence **[std]** (no retrieved document gives one). The
  payout is the 年金現価 of the designated 年金月額 less six months' interest and premium
  equivalent, capped at **¥30,000,000** and barred in the final year [S2] [S5] [S7]. The
  product-specific consequence: because the amount is the present value of an income stream,
  the cap **binds far earlier in the term** than it does on a level sum assured — on the
  anchor cell the full 年金現価 is ¥56,352,381.90 at issue, so the cap bites from month 1 and
  keeps biting until the unpaid stream has run down below ¥30,000,000 of present value.
- **保険料払込免除.** A waiver state on the accident-plus-180-days-plus-別表4 test [S1 第6条] [S3
  第8条] [S5] [S6] with **[std]** incidence. 別表4 is a materially lower bar than the 別表3
  高度障害 schedule, so the waiver incidence is **not** the 高度障害 incidence and must not reuse
  `q(t)`.
- **復活.** The chassis's lapsed-but-reinstatable population with a three-year window [S1
  第17条] [S3] [S5] and a **[std]** reinstatement rate. Off in the base run. The rate class
  carries over unchanged on reinstatement [S3], which matters here because the class is a
  mortality parameter.
- **Recipient-mortality variant.** One carrier alone conditions second-and-later instalments
  on the recipient being alive [S3 第3条第3項], commuting the residue to the 法定相続人 on the
  recipient's death [S3 第7条]. Modeling it requires a post-event mortality basis on a life
  the contract never underwrote, and the 年金開始後用 table stays on the 2007 vintage [REG-R11] —
  a whole second basis for one carrier's wording. Out of scope **[std]**, and the contract
  side confirms the composite's choice: the one published factor table depends on the
  payment period and the type of main contract and explicitly **not** on the annuitant's age
  or sex [S13 別表1]. That is a published statement that the stream is an annuity-certain.

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** reference constructions.

- **No renewal decision.** The chassis's largest behavioural lever, the 更新 decline rate,
  **is absent here** — no retrieved document offers 更新, and one states the absence in terms
  [S5]. A model that imports the chassis's `d(t)` invents a decision this contract does not
  have. Its nearest replacement is 保険契約の変換, conversion into a 定期保険 or 終身保険 without
  underwriting, blocked in the final two years [S6]; that creates a new contract on a
  different chassis at then-current rates, so it produces no liability on the modeled policy
  and is out of scope **[std scope]**.
- **Selective lapsation [std] (optional).** `q_eff(t) = q(t) × [1 + λ × max(0, 1 −
  l(t)/l_ref)]` with `λ` **[std]** and base run `λ = 0`. The mechanism is weaker than on the
  chassis because there is no periodic no-underwriting renewal to select against, but it is
  not absent: the rate class is **fixed at issue and cannot be changed** even if BMI, blood
  pressure or smoking status changes [S2] [S14], so a life whose health deteriorates keeps a
  preferred rate while a life whose health improves cannot get one and may re-shop.
- **Commutation take-up.** Zero in the base run **[std]**. No carrier publishes an election
  frequency. The election is the recipient's, not the policyholder's, and it is made after
  the insured event, so it cannot be driven off any pre-claim behavioural variable.
- **減額.** Permitted above an insurer-set floor; on the 無解約返戻金型 composite it produces **no
  refund at all** [S1 第28条] [S3] [S7]. Not modeled: it changes `A` and `P_m` together, which
  is a model-point re-parameterization rather than a decrement **[std scope]**.
- **クーリング・オフ.** Out of scope: the model begins with cover in force and the eight-day
  statutory population [REG-R36] already out. One carrier contracts for 14 days [S5].

---

## Worked example

**Anchor cell (`point_id = 1`).** Male, 契約年齢 30 (満年齢), **65歳満了** so `N = 420` months,
最低支払保証期間 **2年** so `G = 24` months, **`T = 420 + 24 − 1 = 443` months**, 年金月額
`A = ¥150,000`, rate class 非喫煙者優良体, 月払保険料 `P_m = ¥2,565` [S6]. Base run: no commutation,
no リビング・ニーズ, no waiver, no 復活, no selective lapsation.

Headline arithmetic, for orientation. A death in policy month 1 pays 420 instalments of
¥150,000 = **¥63,000,000** [S14]; total premium if the contract runs to expiry is
¥2,565 × 420 = **¥1,077,300**, about 1.7% of that. A death in policy month 419 pays
`max(420 - 419 + 1, 24) = 24` instalments, running from month 419 to month **442** —
twenty-two months past the expiry date.

**Every assumption value the cell uses.** The mortality anchor `q30 = 0.00068` is **read
from 生保標準生命表2018（死亡保険用）男** [R1] [REG-R18]; it is a sourced value, not an illustration. The
best-estimate rate is `q(t) = 0.80 × 0.70 × q_x^tab` — the chassis's 0.80 [std] factor and
this product's 0.70 [std] 非喫煙者優良体 class factor — so at attained age 30

    q(t)   = 0.80 * 0.70 * 0.00068 = 0.000380800     (annual)
    q_m(t) = 1 - (1 - 0.000380800)^(1/12) = 0.000031738873   (monthly)

Policy-year-1 lapse is 9% **[std]**, so `w_m = 1 − 0.91^(1/12) = 0.007828420342`. Expenses
and commission, all **[std]** chassis levels: `E0 = ¥15,000`; `c0 = 0.50 × 12 × 2,565 =
¥15,390`; `c_r = 5%` from month 13; `e_m(t) = (4,000 / 12) × 1.01^(y(t) − 1)`, so
¥333.333333 a month in policy year 1 and ¥336.666667 in year 2; `ec = ¥30,000`; `ea = ¥200`.

Further table rates used later in the projection. Three are themselves sourced anchors —
`q31 = 0.00069`, `q32 = 0.00070`, `q45 = 0.00177` [R1] [REG-R18] — and three are log-linear
interpolations in `ln q` between the neighbouring anchors, rounded to 5 decimals **[std]**:
`q44 = 0.00163`, `q63 = 0.00851`, `q64 = 0.00929`.

| t | age | `l(t)` | Premiums | `D(t)` | `R(t)` | Annuity claims | Claim + ann. exp | Maint. + acq. | Comm. | `CF(t)` |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 30 | 1.000000 | 2,565.00 | 0.000031739 | 0.000031739 | 4.76 | 0.96 | 30,723.33 | 0.00 | −28,164.05 |
| 2 | 30 | 0.992140 | 2,544.84 | 0.000031489 | 0.000063228 | 9.48 | 0.96 | 330.71 | 0.00 | +2,203.68 |
| 3 | 30 | 0.984342 | 2,524.84 | 0.000031242 | 0.000094470 | 14.17 | 0.96 | 328.11 | 0.00 | +2,181.60 |
| 13 | 31 | 0.909653 | 2,333.26 | 0.000029296 | 0.000394122 | 59.12 | 0.96 | 306.25 | 116.66 | +1,850.27 |
| 420 | 64 | 0.145023 | 371.98 | 0.000063023 | 0.016779783 | 2,516.97 | 5.25 | 67.80 | 18.60 | −2,236.63 |
| 421 | — | 0.000000 | 0.00 | 0.000000000 | 0.001463980 | 219.60 | 0.29 | 0.00 | 0.00 | −219.89 |
| 443 | — | 0.000000 | 0.00 | 0.000000000 | 0.000063023 | 9.45 | 0.01 | 0.00 | 0.00 | −9.47 |

**Trace, month 1.** `l(1) = 1`; premium `= 2,565 × 1 = 2,565.00`. `D(1) = 1 × 0.000031738873
= 0.000031738873`. The claim opens a stream and pays no lump sum, so `R(1) = R(0) − 0 + D(1)
= 0.000031738873` and annuity outgo `= 150,000 × 0.000031738873 = 4.76083098`. Annuity
expense `= 200 × 0.000031738873 = 0.00634777`; claim expense `= 30,000 × 0.000031738873 =
0.95216620`; the two together are 0.95851397. Maintenance `= 4,000 / 12 = 333.33333333`;
acquisition `= E0 + c0 = 15,000.00 + 15,390.00 = 30,390.00`, so the column shows
30,723.33333333. `CF(1) = 2,565.00 − 4.76083098 − 0.00634777 − 0.95216620 − 333.33333333 −
30,390.00 = −28,164.05267828` → **−¥28,164.05**. Roll forward: `l(2) = 1 × (1 −
0.000031738873) × (1 − 0.007828420342) = 0.9921400892`.

**Trace, month 2.** Premium `= 2,565 × 0.9921400892 = 2,544.83932893`. `q_m(2) =
0.000031738873` still — the attained age is unchanged for the first twelve months — so `D(2)
= 0.9921400892 × 0.000031738873 = 0.000031489408`. `R(2) = 0.000031738873 + 0.000031489408 =
0.000063228282`: **nothing ended, because the first stream runs to month 420.** Annuity
outgo `= 150,000 × 0.000063228282 = 9.48424226` — already double month 1's, on 0.99 of the
population, because the ledger accumulates while `l(t)` decays. Annuity expense `= 200 ×
0.000063228282 = 0.01264566`; claim expense `= 30,000 × 0.000031489408 = 0.94468225`.
Maintenance `= 333.33333333 × 0.9921400892 = 330.71336308`. No commission before month 13.
`CF(2) = 2,544.83932893 − 9.48424226 − 0.01264566 − 0.94468225 − 330.71336308 =
+2,203.68439568` → **+¥2,203.68**. Roll forward: `l(3) = 0.9921400892 × (1 − 0.000031738873)
× (1 − 0.007828420342) = 0.9843419567`.

**Trace, month 3.** Premium `= 2,565 × 0.9843419567 = 2,524.83711893`.
`D(3) = 0.9843419567 × 0.000031738873 = 0.000031241905`;
`R(3) = 0.000063228282 + 0.000031241905 = 0.000094470186`; annuity outgo
`= 150,000 × 0.000094470186 = 14.17052794`; annuity expense `= 0.01889404`; claim expense
`= 0.93725714`; maintenance `= 333.33333333 × 0.9843419567 = 328.11398557`.
`CF(3) = 2,524.83711893 − 14.17052794 − 0.01889404 − 0.93725714 − 328.11398557 =
+2,181.59645425` → **+¥2,181.60**.

**Trace, month 13 — the first month of policy year 2.** Three things change at once and an
implementation can get any of them wrong. The attained age moves to 31, so `q(13) = 0.80 ×
0.70 × 0.00069 = 0.000386400` and `q_m(13) = 0.000032205704`. The lapse rate moves to the
year-2 row, `w = 7%`, `w_m = 0.006029308066`. And maintenance inflates: `e_m(13) = (4,000 /
12) × 1.01 = 336.66666667`. With `l(13) = 0.9096534720`: premium `= 2,565 × 0.9096534720 =
2,333.26115568`; renewal commission `= 0.05 × 2,333.26115568 = 116.66305778`, the first one
paid; `D(13) = 0.9096534720 × 0.000032205704 = 0.000029296030`; `R(13) = 0.000364825643 +
0.000029296030 = 0.000394121674`; annuity outgo `= 150,000 × 0.000394121674 = 59.11825109`;
annuity expense `= 0.07882433`; claim expense `= 0.87888091`; maintenance `= 336.66666667 ×
0.9096534720 = 306.25000224`. `CF(13) = 2,333.26115568 − 59.11825109 − 0.07882433 −
0.87888091 − 306.25000224 − 116.66305778 = +1,850.27213932` → **+¥1,850.27**.

**Trace, month 420 — the last month of cover.** `l(420) = 0.1450233243`; premium `= 2,565 ×
0.1450233243 = 371.98482677`, the four-hundred-and-twentieth and last. `q(420) = 0.80 × 0.70
× 0.00929 = 0.005202400`, `q_m(420) = 0.000434570514`, so `D(420) = 0.000063022861`. Nothing
has ended yet, so `R(420) = 0.016716760543 + 0.000063022861 = 0.016779783403` — and this is
exactly the sum of `D(s)` over the whole term, because **every stream is still paying in
month 420**. Annuity outgo `= 150,000 × 0.016779783403 = 2,516.96751047`; annuity expense `=
3.35595668`; claim expense `= 1.89068582`; maintenance `= (4,000/12) × 1.01^34 ×
0.1450233243 = 67.80212570`; commission `= 18.59924134`. `CF(420) = 371.98482677 −
2,516.96751047 − 3.35595668 − 1.89068582 − 67.80212570 − 18.59924134 = −2,236.63069323` →
**−¥2,236.63**. Survivors leave with nothing: `0.1450233243 × (1 − 0.000434570514) × (1 −
0.004265318778) = 0.1443419995`, and `l(421) = 0`.

**Trace, month 421 — the first month past expiry, and the row a wrong model does not have.**
No premium, no maintenance, no commission, no new claims: `l(421) = 0`. Every stream opened
in months 1–397 ended at month 420, so `ended(421) = sum of D(s) for s = 1 .. 397 =
0.015315803299`, and `R(421) = 0.016779783403 − 0.015315803299 + 0 = 0.001463980104` — the
streams from months 398–420, which the guarantee carries past expiry. Annuity outgo `=
150,000 × 0.001463980104 = 219.59701556`; annuity expense `= 0.29279602`. `CF(421) =
−219.59701556 − 0.29279602 = −219.88981158` → **−¥219.89**. From here `ended(t) = D(t −
24)`, so the ledger runs down one month's claims at a time until `R(443) = D(420) =
0.000063022861` and `CF(443) = −9.46603365` → **−¥9.47**. The projection ends at `t = 443`.

**Totals over the 443 months, undiscounted, per policy issued.**

| Line | Amount |
|---|---|
| Premiums | ¥461,030.83 |
| Annuity instalments | ¥443,313.69 |
| Annuity administration | ¥591.08 |
| Claim expense | ¥503.39 |
| Maintenance | ¥67,706.86 |
| Commission (renewal) | ¥21,577.36 |
| Acquisition (`E0 + c0`) | ¥30,390.00 |
| **Net cash flow** | **−¥103,051.56** |

Structural quantities behind those totals: expected claims over the term `sum D(s) =
0.016779783`; expected instalments `sum R(t) = 2.955425` per policy issued, which reconciles
exactly to `sum D(s) × n_pay(s)`; average total benefit per claim **¥26,419,511.96**; lapses
over the term 0.838878 and survivors at expiry 0.144342 of the original cohort. **¥2,645.21
of the claim outgo — 0.5967% — falls in months 421 to 443**, after the policy has expired.

**Read the sign honestly.** The undiscounted net is negative, and the reason is not a bug.
The premium is a *published preferred-non-smoker rate* and the assumption basis is a
**[std]** adjustment of a *valuation* table carrying a 2σ margin [R2] [REG-R20]; the pricing
basis that would reconcile them — 予定利率, 予定死亡率, 予定事業費率 — sits in the 算出方法書 filed under
保険業法第4条第2項第4号 and is not public [REG-R2]. More importantly, on this product an undiscounted
total is close to meaningless: the benefit is paid over up to 35 years *after* a claim that
itself arises over 35 years, so the claim leg discounts far harder than the premium leg.
Present-valuing the same projection at flat annual effective rates gives **−¥103,051.56 at
0%, −¥73,865.82 at 0.5%, −¥49,216.50 at 1% and −¥10,895.85 at 2%.** Discounting is out of
scope for the model and those four numbers are a diagnostic, not a result — but a reader who
takes the undiscounted total as the liability has mis-read this product more badly than on
any other in the library.

---

## Valuation and reserve pointers

This library projects gross cash flows. Every valuation layer consumes them and is cited,
never reproduced.

- Standard policy reserve (*hyōjun sekinin junbikin*, **標準責任準備金**). A conventional
  guaranteed 収入保障 contract is inside the regime: 保険業法第116条第2項 delegates the method and the
  coefficients [REG-R4], and 施行規則第68条 excludes only separate-account-linked contracts,
  contracts with no 保険料積立金, contracts where the insurer has disclosed it may change the
  basis, and residually designated classes — none of which catches this product [R8]
  [REG-R7]. 第69条 requires 保険料積立金, 未経過保険料, 払戻積立金 and contingency reserve (*kiken junbikin*,
  危険準備金) per category [R8] [REG-R8]. 平成8年大蔵省告示第48号 supplies the method — net level premium
  method (*heijun jun-hokenryō-shiki*, **平準純保険料式**) — and the table vintage: contracts
  from 2018-04-01 value on 生保標準生命表2018（死亡保険用）[REG-R10] [REG-R11] [R3]. The discount rate is
  the standard valuation interest rate (*hyōjun riritsu*, **標準利率**), which the supervisory
  guideline defines as 「責任準備金告示に規定する予定利率」 [R9] [REG-R10]; its **current numeric value could
  not be established from any retrieved document and is [unverified]** — the 新旧対照表
  attachments on the regulator's page were not fetched [R10].
- **The valuation table is not this model's basis.** 標準生命表2018 carries a ~2σ margin capped
  at 130% of the unadjusted rate plus a forward improvement allowance [R2] [REG-R20], while
  `q(t)` here is a **[std]** adjustment of it *and* is further multiplied by a **[std]**
  rate- class factor. Three separate departures from the statutory basis sit between this
  projection and a 責任準備金; say which basis is in use at every point.
- **ESR.** From 2026-03-31 insurers report on the 経済価値ベースのソルベンシー規制: assets at fair value,
  liabilities as 現在推計 + MOCE, required capital at 99.5% over one year, early corrective
  action below **ESR 100%** [REG-R15], replacing as the trigger the ソルベンシー・マージン比率 threshold
  of **200%** [REG-R17] [REG-R15]. `jplib` computes neither ratio. What the regime change
  means *for this product* is specific: a benefit whose amount is a function of *when* the
  claim occurs, settled over decades and re-discounted on a curve that moves at every 基準日,
  is far more interest-sensitive than a level sum assured, and a locked-in basis conceals
  that.
- **The professional use of this projection.** 保険業法第121条第1項第1号 requires the 保険計理人's 意見書
  [REG-R6]; the IAJ practice standard turns it into the **1号収支分析** — a forward projection of
  premiums, claims, expenses and surrenders by 区分経理 segment over at least ten future years,
  sufficiency-tested over the first five [REG-R22]. Note the mismatch this product creates:
  a ten-year window on a 35-year contract sees only the earliest, largest instalment counts
  and none of the run-off tail.
- **Accounting.** IFRS 17 is **voluntary** in Japan; IFRS applies as 指定国際会計基準 to insurers
  that elect it [REG-R47]. One projection feeds three measurement bases — J-GAAP [REG-R10],
  ESR [REG-R15] and IFRS where adopted — and conflating them gets wrong which assumptions
  are locked in.
- **On insurer failure**, 生命保険契約者保護機構 covers up to **90% of the 責任準備金** under a rate
  delegated by 保険業法第270条の3 to ordinance [REG-R40] [REG-R41]. Cited, never modeled.
- **Tax is not a model output but changes what the numbers mean.** At the death the object
  taxed for 相続税 is the 年金受給権, valued at the greatest of the surrender value, the lump sum
  available in lieu, and the average annual amount times the 複利年金現価率 at the contract's 予定利率
  [R6] [R5]; on a 無解約返戻金型 design the first limb is zero, so **the commutation basis of
  assumption class (b) is also the tax valuation** — the ¥300,000,000 年金現価 cap [S8] and the
  published factors [S13] are tax-relevant numbers. Instalments are then 雑所得 in part [R4].
  On the premium side the contract sits in the 一般生命保険料 basket [R7] [REG-R43].

---

## Key sensitivities and model risks

In rough order of leverage on the anchor cell. Every figure below is the undiscounted net
cash flow or claim outgo per policy issued, from the same projection.

1. **The rate-class mortality factor.** `class_factor = 0.70` **[std]** is the largest lever
   and the least evidenced parameter in the file, because *no carrier publishes a class
   differential for this product* [S2] [S5] [S6] [S14] [S16]. Annuity outgo runs
   **¥443,313.69 at 0.70, ¥568,289.70 at 0.90, ¥661,538.07 at 1.05 and ¥846,803.38 at 1.35**
   — a factor of 1.9 across the composite's own four classes, on a premium the carrier
   quotes for the cheapest of them.
2. **The chassis's 0.80 best-estimate factor.** Annuity outgo is **¥426,306.73 at 0.769**
   (the arithmetic implied by removing a margin at its 130% cap [REG-R20]), ¥443,313.69 at
   0.80 and **¥552,708.11 at 1.00** (the raw valuation table). Items 1 and 2 multiply: the
   two corners of the joint range give ¥426,306.73 (0.769 × 0.70) and ¥1,053,287.56
   (1.00 × 1.35), **a factor of 2.47**, and no document narrows either input.
3. **Discounting, which this library does not do.** Net cash flow is −¥103,051.56
   undiscounted and −¥10,895.85 at 2% p.a. Nowhere else in `jplib` does the discount rate
   move the answer this far, because nowhere else is the benefit a 35-year stream beginning
   at an uncertain date. Any user comparing this product's undiscounted output with
   the [term life chassis (定期保険)](../term_life/technical-notes.md)'s is comparing two quantities of
   different economic meaning.
4. **The guarantee length.** Annuity outgo is **¥440,668.48 with no guarantee, ¥443,313.69
   at 2年, ¥457,179.73 at 5年 and ¥503,961.05 at 10年** — so the composite's 2年 guarantee is
   worth 0.60% of claims, the 5年 alternative in the composite menu 3.7%, and the 10年 option
   one carrier publishes [S5] **14.4%**, each measured against the no-guarantee run. The
   guarantee is cheap precisely because it binds only in the last `G` months of a 420-month
   term, where few lives remain. The 0-month and 120-month runs are outside the composite's
   menu, so reproducing them means relaxing the model's own `guar_m` validator; the 2年 and
   5年 figures are the two shipped configurations.
5. **Lapse, whose sign is the opposite of the chassis's.** Net cash flow is **−¥269,617.32
   at zero lapse, −¥103,051.56 on the [std] table and −¥68,603.79 at 1.5× those rates.** On
   this assumption set lapse *relieves* the liability, because expected claims exceed
   premiums; on a pricing basis it would not. A sensitivity whose sign flips with the basis
   needs both runs reported, not one.
6. **The commutation basis, if the module is on.** Total claim outgo under full commutation
   at the claim date is **¥415,875.64 at 0.61%, ¥414,176.30 at the [std] 0.65% and
   ¥382,513.43 at 1.45%** — the published range [S13] [S6] [S10] [S17] moves claim outgo by
   8%, and the commutation module itself cuts claim outgo to **93.43%** of the instalment
   total. Off in the base run, so the exposure is latent, not live.
7. **Expense structure on a small premium.** ¥30,780 of annual premium carries ¥4,000 of
   maintenance; the five non-benefit lines total **¥120,768.70** against ¥461,030.83 of
   premium, **26.2%**. The 1.0% **[std]** inflation rate compounds over 35 years and no
   Japanese public source supports any of these levels.

Known modeling pitfalls:

- **The projection horizon is not the policy term.** `T = N + G − 1`, not `N` [S1 第3条第2項]
  [S3 第3条第3項] [S5] [S12] [S14]. Terminating at `t = N` on the anchor cell drops
  **¥2,645.21** of contractual claim outgo, 0.5967% of the total, all of it in months
  421–443. It is the most natural error to make and the least visible, because every
  remaining number still looks reasonable.
- **最低支払保証期間 is a term extension, not a benefit floor.** Both readings pay the same
  `max(N - m + 1, G)` instalments, so an undiscounted *total* cannot distinguish them; they
  differ in **when**. A floor implementation compresses the guaranteed instalments inside
  the term and produces zero cash flow after month 420; the contract pays them after expiry,
  on the same monthly timetable [S1 第3条第2項]. Test months 421–443 individually, not the
  total.
- **The in-payment ledger is never decremented.** Not by the insured's mortality, not by the
  recipient's, not by lapse [S1] [S5] [S14] [S13 別表1]. Applying the surviving-policy factor
  `(1 − q_m)(1 − w_m)` to `R(t)` — the natural thing to do if `R` is mistaken for a
  population of policies — cuts annuity outgo on the anchor cell from ¥443,313.69 to
  **¥245,605.66**, an understatement of **44.6%**. This is the largest single error
  available in this model.
- **Premiums stop on the annuity event; the benefit does not.** Premium income carries
  `l(t)` and only `l(t)` [S1 第12条第2項] [S3 第5条] [S8]. Netting premiums against claims on one
  combined population collects ¥7,535.43 of premium — 1.63% of the total — from policies
  that are in claim and paying nothing.
- **`l(t)` and `R(t)` are disjoint and must never be summed.** `l(t)` is a probability of
  being in force; `R(t)` is a count of instalments falling due. They have different units in
  the model's economics even though both are dimensionless, and `R(420) = 0.016779783` while
  `l(420) = 0.145023` — adding them produces a number with no meaning.
- **The ledger peaks at exactly month `N`.** Every stream opened in months 1 … `N − G + 1`
  ends at month `N` whenever it opened, so `R(N)` equals the sum of `D(s)` over the whole
  term: 0.016779783 on the anchor cell. An implementation that ends streams at
  `m + n_pay(m) - 1` computed with an off-by-one gets this identity wrong by one month's
  claims and nothing else visibly changes.
- **高度障害 is not a second decrement.** 生保標準生命表2018（死亡保険用）includes 高度障害 in its death
  rate [R2] [REG-R20], and the two annuities are mutually exclusive [S1 第3条] [S3 第3条] [S5]
  [S9]. Adding a 高度障害 incidence on top of the table double-counts the benefit.
- **There is no 更新 on this chassis.** No retrieved document offers renewal and one states
  the absence in terms [S5] [S6] [S8]. Importing the chassis's renewal repricing and `d(t)`
  decline invents a decision, a premium ladder and a decrement the contract does not have;
  the term is **歳満了 only** and the premium is level for all `N` months.
- **Lapse pays nothing.** No 解約返戻金 at any duration on the composite [S2] [S5] [S6] [S7] [S9]
  [S15], so `claims_lapse` is identically zero. One carrier in the set *does* write a
  低解約返戻金型 design at 70% of the ordinary value [S12] — and on that design, because
  保険料払込期間 equals 保険期間, there is **no 払込満了 step-up**, so the cliff that characterises
  低解約返戻金型 whole life has no analogue here. A model importing that cliff invents it.
- **There is no 自動振替貸付.** With no cash value there is no collateral, and one carrier states
  the absence in terms [S2]. The APL mechanic specified in the
  [whole life technical notes (終身保険)](../whole_life/technical-notes.md) must not be
  imported; the supervisory guideline in any case requires an APL, where one exists, to run
  at the policyholder's election rather than automatically [REG-R14].
- **A full commutation settles the claim; it does not alter the policy.** Paying the whole
  present value extinguishes the contract [S1 第5条第2項] [S3 第6条第3項] [S12] [S14], so with the
  module on, the ledger must not open at all for that claim. A model that pays the lump sum
  *and* opens the stream doubles the benefit.
- **The リビング・ニーズ cap binds early here, not late.** The payout is the present value of an
  income stream capped at ¥30,000,000 [S2] [S5] [S7], and on the anchor cell the full 年金現価
  at issue is ¥56,352,381.90. The cap therefore bites from month 1 and stops biting only
  once the unpaid stream falls below it — the opposite pattern to a level sum assured, where
  a cap either always binds or never does.
- **Read the table at the right age, and only on the death basis.** 契約年齢 is 満年齢 [S1 第37条]
  [S14] while 標準生命表2018 is built for 保険年齢 [R2] [REG-R20], so the base run reads early and
  understates; the optional shift must move `q` **up**. And the 年金開始後用 table has no role on
  this product at all, because the composite's stream is an annuity-certain [S13 別表1].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #jplib-income_guarantee-r1
[R10]: #jplib-income_guarantee-r10
[R11]: #jplib-income_guarantee-r11
[R2]: #jplib-income_guarantee-r2
[R3]: #jplib-income_guarantee-r3
[R4]: #jplib-income_guarantee-r4
[R5]: #jplib-income_guarantee-r5
[R6]: #jplib-income_guarantee-r6
[R7]: #jplib-income_guarantee-r7
[R8]: #jplib-income_guarantee-r8
[R9]: #jplib-income_guarantee-r9
[REG-R10]: #jplib-reg-r10
[REG-R11]: #jplib-reg-r11
[REG-R14]: #jplib-reg-r14
[REG-R15]: #jplib-reg-r15
[REG-R17]: #jplib-reg-r17
[REG-R18]: #jplib-reg-r18
[REG-R2]: #jplib-reg-r2
[REG-R20]: #jplib-reg-r20
[REG-R21]: #jplib-reg-r21
[REG-R22]: #jplib-reg-r22
[REG-R31]: #jplib-reg-r31
[REG-R32]: #jplib-reg-r32
[REG-R34]: #jplib-reg-r34
[REG-R35]: #jplib-reg-r35
[REG-R36]: #jplib-reg-r36
[REG-R4]: #jplib-reg-r4
[REG-R40]: #jplib-reg-r40
[REG-R41]: #jplib-reg-r41
[REG-R43]: #jplib-reg-r43
[REG-R47]: #jplib-reg-r47
[REG-R6]: #jplib-reg-r6
[REG-R7]: #jplib-reg-r7
[REG-R8]: #jplib-reg-r8
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
