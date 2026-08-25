# Technical Notes

**Status:** Draft, 2026-08-20 (all cited sources accessed 2026-08-20).

**Scope note.** These notes turn the standardized composite foreign-currency-denominated
whole life assurance (*gaika-date shūshin hoken*, 外貨建終身保険) of `product-spec.md` (same
directory) into a reference liability cash-flow projection on paper. This is not any single
insurer's product. [S#] and [R#] tags resolve against `sources.md`, whose numbering is
carried verbatim from `_research/fx-whole-life.md` and is frozen; [REG-R#] tags resolve
against the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is distinct.
**[std]** marks a standardization introduced for the reference implementation; [unverified]
marks a claim that could not be confirmed against a retrieved document. **Every parameter
value here is identical to `product-spec.md`'s.** Eight quantities appear here that the
specification names without valuing, because it defers them to this document: the two
premium-charge rates `φ1` and `φ2`, the account-value maintenance rate `μ`, the three
constants of the market value adjustment, MVA (*shijō kakaku chōsei*, 市場価格調整) reconstruction
`A`, `r0` and `d`, and the two experience top-up (*tokubetsu tsumitatekin*, 特別積立金) shares
`σ10` and `σ20`. Each is **[std]**, and each is *derived* below — fitted to a published
table and reported with its fit — not asserted.

**Everything in this file is denominated in the policy currency, the US dollar, and every
yen figure is a translation of a dollar figure at a stated exchange rate.** The model
projects in US dollars; the yen ledger is a published translation, computed from the dollar
ledger by the rules in "The currency layer" below. Mixing the two — reading a yen figure as
a model quantity, or translating a net figure at a single rate — is the error this product
punishes hardest, and it is the first pitfall in the list at the foot of the file.

**This product inherits the savings chassis.** Policy reserve (*sekinin-junbikin*, 責任準備金),
policy loan (*keiyakusha kashitsuke*, 契約者貸付), automatic premium loan, APL (*jidō furikae
kashitsuke*, 自動振替貸付), grace, lapse (失効), reinstatement (復活), reduced paid-up (払済保険),
sum-assured reduction (減額) and the suppressed-surrender-value
(*tei-kaiyaku-henreikin-gata*, 低解約返戻金型) cliff are specified once, in the
[whole life technical notes (終身保険)](../whole_life/technical-notes.md), and are **not restated here**.
This file states the deltas: a monthly grid instead of an
annual one, an account value instead of a closed-form policy value, an MVA, a currency
layer, and a path-dependent conversion rider.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows** per policy — premiums,
  death and severe disability (*kōdo shōgai*, 高度障害) claims, surrender benefits, expenses and
  commission — for a single-policy model point, in the sense the ESR current estimate (*genzai
  suikei*, 現在推計) requires: probability-weighted future cash flows on assumptions re-set
  at each 基準日, gross of reinsurance [REG-R15]. It is also the shape the appointed actuary
  (保険計理人)'s **1号収支分析** consumes, and that practice standard addresses MVA and
  foreign-currency business by name [REG-R6] [REG-R22]. **Discounting, MOCE, required
  capital and every statutory reserve are out of scope** and are cited, not reproduced (see
  Valuation and reserve pointers).
- **Projection frequency.** **Monthly** (`FXWholeLife_JP_S`), stepping on the monthly policy
  anniversary (*getsu-tan'i no keiyaku ōtōbi*, 月単位の契約応当日). This is not a refinement of
  the chassis's annual grid but a requirement: the crediting rate (*tsumitate riritsu*, 積立利率)
  is redeclared monthly and credited from the monthly policy anniversary [S2], the
  death-benefit uplift (*zōka shibō hokenkin-gaku*, 増加死亡保険金額) is recomputed at the same date
  [S2], and the target-value test is made every business day [S9]. `t` counts completed
  policy months from 契約日; `t = 0` is the month beginning at issue.
- **The declaration/application offset is real and is carried, not resolved.** The 重要事項説明書
  of the anchor booklet says the rate is set 毎月1日; 約款第3条第2項 of the same booklet says it is
  applied 月単位の契約応当日ごとに [S2]. The 約款 governs, so the model credits on policy months and never
  on calendar month ends. A model that credits on calendar month ends is wrong by the
  anniversary offset for the whole life of the contract, and the error does not average out.
- **Timing conventions [std].** Premium at the **start** of month `t`; charges deducted from
  the account value at the start of month `t`, in the order below; interest credited at the
  **end** of month `t`; death claims and claim expenses at the end of month `t`; surrenders
  at the end of month `t`, **after** deaths, valued on the account value *after* that
  month's interest. Acquisition expense and initial commission at issue (`t = 0`).
- **Age basis.** 契約年齢 is attained age (*man-nenrei*, 満年齢) with the fractional year discarded
  at 契約日, incrementing on the 年単位の契約応当日; attained age in month `t` is `x + floor(t/12)`
  exactly. 生保標準生命表2018（死亡保険用）is built for an insurance age, nearest birthday
  (*hoken-nenrei*, 保険年齢) basis [REG-R20]; the
  reference implementation reads it at the 満年齢 attained age with no adjustment **[std]**, as
  the chassis does, and the resulting understatement of `q` is named there, not re-argued
  here.
- **Currency.** **US dollars throughout.** Every state variable, every assumption and every
  cash-flow column is in US dollars. Yen figures are produced by a separate translation
  layer and carry a `_jpy` suffix. The exchange rate is a **model point column** `fx_ttm`,
  never a constant inside a formula: an exchange rate buried in a recursion is an economic
  assumption disguised as a product feature, and cannot be varied by the point that owns
  it. A second model point column, `fx_path`, replaces the flat rate with a path read
  **by policy year** — not by month — from `fx_path_table.csv`, its last row carried
  forward; the file is reached through the `fx_path_file` Reference on `Data`.
- **Model points.** Single-policy model points on an expected (probability-weighted) basis:
  survivorship multiplies per-policy cash flows. `point_id` parameterizes `Projection`;
  `point_id = 1` is the worked-example anchor cell.
- **Termination.** No maturity date and no 満期保険金 [S1] [S2] [S3] [S7]. The projection runs to
  the terminal age of the mortality table: `T = 12 × (ω − x + 1)` months, ω = **109** male /
  **113** female on 生保標準生命表2018（死亡保険用）, the first age at which `q(ω) = 1.00000` [REG-R18].
  On the anchor cell `T = 840` months. There are no tail states.
- **Contract boundary.** The premium is level and guaranteed in US dollars for the whole of
  保険料払込期間 and the insurer has no unilateral repricing right [S1] [S2], so the whole contract
  is projected. Japan's ESR 柱1 告示 were not opened and their boundary text is
  [unverified] [REG-R16]; the model implements no boundary test and says so.
- **Rounding.** Intermediate values at full precision; displayed dollar cash flows to **four
  decimal places** and account and surrender values to **two [std]**, which is the precision
  the tests assert. The published surrender-value run is reproduced to the dollar, so the
  monthly interest convention must be stated: the monthly factor is the geometric twelfth
  root `(1 + i)^(1/12)`, not `i/12` **[std]** (`product-spec.md` footnote 11).

---

## Model point attributes

| Attribute | Type | Anchor cell (`point_id = 1`) |
|---|---|---|
| `policy_id` | str | `FXWL-JP-0001` |
| `shape` | enum {LEVEL, SINGLE} | LEVEL |
| `sex` | enum {M, F} | M |
| `issue_age` (`x`) | int, 満年齢 | 40 |
| `currency` | enum {USD} | USD |
| `sum_assured` (`SA`) | US$ | 100,000.00 |
| `premium_mth` (`P`) | US$/month (LEVEL) | 239.60 |
| `single_premium` | US$ (SINGLE; 0 on LEVEL) | 0.00 |
| `prem_months` (`n`) | int months, 0 for 終身払 | 240 (60歳払込満了) |
| `credit_rate` (`ic`) | annual effective, declared | 0.0300 |
| `guar_floor` (`i0`) | annual effective, fixed at issue | 0.0300 |
| `rate_period_y` | 積立利率適用期間, years (SINGLE only) | 0 (n/a on LEVEL) |
| `low_cv` | bool — 低解約返戻金特則 elected | false |
| `idb_ratchet` | bool — the 増加死亡保険金額 ratchet | true |
| `target_on` | bool — target-value rider elected | false |
| `target_g` (`g`) | 目標値, multiple of the yen premium paid | 1.10 |
| `yen_in`, `yen_out` | bool — riders (*tokuyaku*, 円入金特約 / 円支払特約) attached | true, true |
| `fx_ttm` (`e`) | ¥ per US$1, the reference TTM | 159.43 |
| `fx_spread` (`s`) | ¥ per US$1, each way | 0.50 |

Seven further columns are switches rather than contract attributes and are specified where
the mechanic they govern is: `idb_basis` and `target_action` under the two mechanics below,
`mva_delta` under the surrender layer, `apl_on`, `dyn_lapse` and `fx_path` under
policyholder behaviour, and `mort_adj` in assumption class (c), whose cells is
`mort_be_factor`. There is no issue-date
column: `t` counts policy months from 契約日 and no calendar date enters the projection.

`prem_months = 0` denotes 終身払, for which no 払込満了 exists. On the SINGLE shape
`premium_monthly = 0`, `single_premium > 0`, `prem_months = 1`, `low_cv = false` and
`rate_period_y = 15`; the APL is **structurally absent**, because there is no premium to
advance, so that shape's decrement set is smaller, not merely differently rated.

The anchor premium is **sourced, not constructed**: US$239.60 per month is the published
premium for exactly this cell — male, 契約年齢40歳, the sum assured on the main contract
(*shu-keiyaku*, 主契約) (主契約保険金額) 100,000米ドル, 月払, 口座振替, 60歳払込満了, 保険期間終身
— and the same booklet publishes 225.00 for the 低解約返戻金特則 form, a 6.1% reduction [S2].

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `pols_if(t)` | In-force probability at the **start** of month `t`; `pols_if(0) = 1` | monthly recursion |
| `av_pp(t)` | `AV(t)` — the account value (*tsumitate-kin*, 積立金) at the start of month `t`, before that month's premium | monthly recursion |
| `av0_pp(t)` | `AV0(t)` — the same fund on the assumed interest rate (*yotei riritsu*, 予定利率) basis; the benchmark the uplift is measured against | monthly recursion |
| `idb_pp(t)` | `IDB(t)` — 増加死亡保険金額, the ratcheting death-benefit uplift | monthly recursion |
| `cv_pp(t)` | `CV(t)` — the payable surrender value (*kaiyaku-henreikin*, 解約返戻金) | closed form on `AV(t)` |
| `surr_charge_rate(t)` | `sc(t)` — surrender charge rate (*kaiyaku kōjo-ritsu*, 解約控除率) | step function of `t` |
| `mva_rate(t)` | `mva(t)` — 市場価格調整率; zero on LEVEL, signed on SINGLE | closed form |
| `low_cv_rate(t)` | `kl(t)` — 低解約返戻金割合, the suppression factor | step function of `t` |
| `mort_rate(t)`, `mort_rate_mth(t)` | annual and monthly mortality rate (incl. 高度障害) | table lookup at `x + floor(t/12)` |
| `lapse_rate(t)`, `lapse_rate_mth(t)` | annual and monthly voluntary surrender rate | assumption table |
| `target_hit(t)` | bool — the yen-converted `CV(t)` has reached the 目標額 | derived, path-dependent |
| `fx_rate(t)` | `e(t)` — the reference TTM in month `t` | model point or path table |

`av0_pp` and `idb_pp` exist only on the LEVEL shape; on the SINGLE shape the death benefit
is `max(AV(t), CV(t))` and there is no fund-independent sum assured at all [S3]. `cv_pp` is
the chassis name and is used here for the same object; `av_pp` is the new one, and the two
are **not** interchangeable — every charge sits between them.

The base run carries no loan, no APL cohort, no target rider and no 低解約返戻金特則, so the
chassis's `pols_if_apl` / `loan_pp` triangle is absent from the anchor and is exercised in a
dedicated model point.

---

## Assumption inputs

Three classes, kept apart on purpose. The separation is a legal requirement here as much as
a modelling one: presenting a non-guaranteed element as certain is 断定的判断の提供 under 消費者契約法 第4条
[REG-R38], which is why the published illustration prints the guaranteed 3.00% column and
the 3.50% and 4.00% columns as three columns and never as an average [S2] [R8].

### (a) Contractual / guaranteed elements (cited; the insurer cannot change them)

| Input | Value | Basis |
|---|---|---|
| Death benefit, LEVEL | `SA + IDB(t)`; 高度障害 pays the same and extinguishes the contract | [S1] [S2] |
| Death benefit, SINGLE | `max(AV(t), CV(t))` at the date of death | [S3] |
| Premium `P` | US$239.60/month, level and guaranteed for months 0 … 239 | [S2] |
| 保険期間 | 終身 — no expiry, no 満期保険金 | [S1] [S2] [S3] [S7] |
| 最低保証積立利率 `i0` | **3.00%** on LEVEL, equal to the contract's own 予定利率, fixed at issue | [S1] [S2] |
| 最低保証積立利率, SINGLE | **0.01%** | [S3] |
| 解約返戻金 formula | `AV × (1 − mva − sc) × kl` | [S3]; suppression [S2] |
| 解約控除率 `sc(t)` | 7.0% in policy year 1, −0.7pp per completed policy year, zero from year 10; constant within the year; base = the 積立金 | [S3] |
| MVA scope | SINGLE only; not on an 積立利率計算基準日 nor inside a 1-year 積立利率適用期間 | [S3] |
| MVA direction | Symmetric: positive when rates have risen, **negative when they have fallen** | [S3] [R8] |
| 低解約返戻金割合 `kl` | 70% / 77.5% / 85% / 92.5% by 残余保険料払込年数 (≥4 / 3 / 2 / 1), 1.00 from 払込満了 | [S2] |
| 入金用 / 支払用為替レート | TTM ＋50銭 / TTM −50銭, capped at TTS / floored at TTB; first quote of the day | [S1] [S3] [S5] [S7] |
| Conversion base date | The day before the completed documents reach the insurer, rolled back over bank holidays | [S7] |
| 特別積立金 | Added to the 積立金 after 10 and after 20 years in force; never paid to a contract terminating earlier | [S1] [S2] |
| 目標値 test | On the **yen-converted 解約返戻金**, every business day, from month 12 | [S9] [S8] |
| Post-conversion | Death benefit and surrender value fixed in yen; no FX, no MVA, no 解約控除 thereafter | [S8] [S9] |
| 免責 — suicide | 3 years from the 責任開始期, reset on 復活 | [S2] [S7]; statutory frame [REG-R34] |
| Refused claim | The 積立金 or 解約返戻金 is still paid | [S2] |
| Policyholder protection | 90% of the 責任準備金等, **no carve-out for 外貨建 contracts** | [R10] [REG-R40] [REG-R41] |

### (b) Insurer-discretionary current elements

This class is where the product's economics live, and on this product it is larger than on
the yen chassis, because the crediting rate itself is in it.

| Input | Snapshot value | Basis |
|---|---|---|
| 積立利率 `ic`, LEVEL | **3.00%**, held at the guaranteed floor for the whole projection | [S2]; scenario **[std]** (1) |
| 積立利率 `ic`, SINGLE | **4.72%**, the rate declared for the 2026-08-16 window, fixed for 15 years | [S4] |
| Crediting scenario range | LEVEL 3.00 / 3.50 / 4.00% (the published illustration set); SINGLE 4.45–5.29% over twenty fortnightly windows | [S2] [S14] |
| 契約初期費用 `φ1` | **38% of each premium** over policy months 0 … 23 | derived **[std]**, below |
| 契約初期費用 `φ2` | **13% of each premium** over policy months 24 … 239 | derived **[std]**, below |
| 維持費率 `μ` | **0.50% p.a.** of the account value, deducted monthly | derived **[std]**, below |
| 契約初期費用, SINGLE | **4.50%** of the single premium at issue ages 40–69 | [S10] |
| Cost-of-insurance basis | 生保標準生命表2018（死亡保険用）, no further loading, on the net amount at risk | [S1] [S2] structure; basis **[std]** (2) |
| MVA constants `A`, `r0`, `d` | 0.10%, 3.00%, 0.70 | derived **[std]**, below |
| 特別積立金 shares `σ10`, `σ20` | **0.24** and **0.16** of the fund's excess over its 予定利率 benchmark | derived **[std]**, below |
| 契約者配当 | None — 無配当 on both modelled shapes | [S1] [S2] [S3] [S7] |
| APL / 契約者貸付 interest `i_L` | **2.75% p.a.**, compound — the chassis's value, inherited unchanged; unused in the base run because the module is off there | level **[std]** at the [whole life technical notes (終身保険)](../whole_life/technical-notes.md); the 年8% contractual ceiling is cited there |

1. The floor is a contract term and therefore the honest base run: it is the guaranteed
   column of the published table and it is what the 約款 promises [S2]. The declared-rate
   *history* for this shape does not exist in retrievable form — the carrier's rate page is
   a JavaScript shell with no rate content in the served HTML [S16] — so the floor and the
   three illustration rates are the only crediting figures available for it. Holding the
   rate at the floor also makes two mechanics vanish identically (below), which is what
   makes the base run checkable against a public document.
2. The table is a **valuation** table with a margin sized to about 2σ and an improvement
   allowance already inside it [REG-R20], and its publisher restricts redistribution
   [REG-R21], so `jplib` ships `mort_table.csv` as a **[std]** construction whose
   `provenance` column points at the IAJ entry [REG-R18] and quotes only the rates the
   worked example needs.

**Why the charge rates are fitted rather than asserted.** Every carrier in the set refuses
to quantify the mortality-and-expense charge, in identical words [S2] [S7], and the rates
live in the 保険料及び責任準備金の算出方法書, a filed but unpublished 基礎書類 [REG-R2]. What *is* public is a
complete surrender-value run for the anchor cell at nine durations on three crediting
scenarios [S2]. Because the crediting rate on the guaranteed column is a contract term and
the surrender-charge scale is fixed by `product-spec.md` footnote 20, the charge stack is
the residual, and the reference implementation **back-solves it** — `φ1`, `φ2` and `μ` from
nine published dollar figures spanning forty-seven years. The fit is reported in the worked
example. Four independent bounds keep the answer honest: a published front-end scale of 4.50
/ 3.00 / 2.00% of a single premium by age band [S10]; a distributor's 契約時手数料 of 4.00% or
2.60% with a 継続手数料 of up to 0.75% p.a. for at most seven years [S13]; the FSA's L-shaped
5.5% / 0.1% reading of the sector [R5]; and a 2.35% p.a. 保険契約関係費 on a variable sleeve [S13],
which is an upper bound because a variable sleeve carries fund cost a fixed account does
not.

### (c) Behavioral / experience assumptions (modeler's view)

**Mortality.** 生保標準生命表2018（死亡保険用）男 [REG-R18], read at the 満年齢 attained age, with
`mort_be_factor = 1.00` in the base run **[std]** — the base run is a valuation-table run,
not a best estimate, taken so that every number below can be checked against a document
anyone can download. The rates used are the library's **one canonical proxy** for that
table: a single file built once for all nine products by log-linear interpolation in
`ln q` between the
individual rates the library quotes from the published table — among them the **sourced
anchors** `q30 = 0.00068`, `q35 = 0.00077`, `q40 = 0.00118`, `q45 = 0.00177`, `q50 =
0.00285`, `q55 = 0.00422`, `q60 = 0.00653`, `q65 = 0.01015`, `q90 = 0.15760` and the
terminal `q109 = 1.00000` [REG-R18] — rounded to five decimals, with every row's
`provenance` column saying which of the two it is. **The interpolation is [std], the anchors
are not.** The same attained age therefore carries the same rate *and* the same provenance
in the [whole life technical notes (終身保険)](../whole_life/technical-notes.md), the savings chassis this
product is built on, and in
every other product that ships it; the nine files must not diverge.

**`mort_be_factor` moves the decrement and must never move the cost-of-insurance charge.**
The decrement is an experience assumption; the charge basis is a pricing element the
insurer sets [REG-R2]. Wiring one lever to both is the single easiest way to make this
model self-consistent and wrong: raising `mort_be_factor` would then raise claims *and*
raise the charge that funds them, and the account value would absorb the sensitivity
instead of the cash flow showing it.

**Surrender.** Two curves, because the two shapes have two behavioural regimes and the
difference is an order of magnitude.

| Policy year | 1 | 2 | 3 | 4 | 5 … 10 | 11 … 20 | 21 + |
|---|---|---|---|---|---|---|---|
| LEVEL `lapse_rate(t)` **[std]** | 8% | 7% | 6% | 5% | 5% | 4% | 3% |
| SINGLE `lapse_rate(t)` **[std]** | 28% | 23% | 18% | 14% | 8% | 8% | 8% |

The SINGLE curve is **calibrated, not invented**: the FSA reports that about **60% of
外貨建一時払保険 are surrendered within four years** of purchase [R5], and the four rates above give
a cumulative four-year exit of **60.90%**. The companion statistic — an average holding
period of **2.5 years** [R6] — is *not* reproducible by any single hazard curve that also
reproduces the 60%, because it is measured over terminated policies inside a monitoring
window rather than over the whole book; it is quoted as context and is not fitted. Read
against the industry-wide 解約・失効率 of 5.6% of sum assured [REG-R31], the SINGLE curve is a
different behavioural regime, and importing a yen whole life's persistency onto this shape
is wrong by an order of magnitude. The LEVEL curve is a **[std]** judgement with no public
anchor at all: the FSA statistics are about 一時払 business, and no retrieved document reports
persistency on a level-premium FX contract.

**Expenses and commission (levels all [std]; no carrier publishes an expense basis).**

| Input | Value |
|---|---|
| Acquisition expense `E0` | US$300 per policy at issue |
| Initial commission `c0`, LEVEL | 90% of the annualized premium at issue |
| Renewal commission `c_r`, LEVEL | 3% of premium, months 12 … 239 |
| Initial commission, SINGLE | **5.5%** of the 一時払保険料 at issue |
| Trail commission, SINGLE | **0.75% p.a.** of the account value, accrued monthly, for **seven** years |
| Maintenance expense `e_m(t)` | US$60 p.a., **for life**, inflating 1.0% p.a., accrued monthly |
| Claim expense `ec` | US$150 per death claim |

The SINGLE pair is the one commission line in this table whose *pattern* is evidenced even
though its levels are not: a distributor's published schedule is a 契約時手数料 of 4.00% or
2.60% of the single premium with a 継続手数料 of up to 0.75% p.a. of the account value for at
most seven years [S13], and the FSA reads the sector as L-shaped at about 5.5% in year one
against 0.1% thereafter [R5]. The composite takes the FSA's front-end figure and the
published trail, which is a **[std]** splice of two sources rather than either one of them.

Expenses are the insurer's own costs and are incurred in yen; they are held in dollars at
the model's own convenience and translated at the plain TTM, never at a spread rate — they
do not cross the policyholder boundary. This is the one place a dollar figure in this file
is a modelling convenience rather than a contractual amount, and it is stated rather than
hidden.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t` | policy month, `t = 0 … T − 1`; attained age is `x + floor(t/12)` |
| `x`, `T`, `ω` | 契約年齢; projection length in months, `T = 12(ω − x + 1)`; table terminal age |
| `n` | 保険料払込期間 in months (240 on the anchor cell) |
| `SA`, `P` | 基本保険金額; monthly premium, payable at the start of months 0 … n−1 |
| `i0`, `ic` | 予定利率 / guaranteed floor; declared 積立利率 — both annual effective |
| `j` | monthly interest factor exponent: `j = (1 + ic)^(1/12) − 1` |
| `q(t)`, `w(t)` | annual mortality (incl. 高度障害) and surrender rates at month `t` — the **decrements**, so `q` carries `mort_be_factor` |
| `qc(t)` | the **unadjusted** table rate at the same age: the cost-of-insurance *basis*, which `mort_be_factor` never touches. `qc ≡ q` wherever `mort_be_factor = 1`, as it does on every cell below |
| `q_m(t)`, `qc_m(t)`, `w_m(t)` | `1 − (1 − q)^(1/12)` and the same conversion of `qc` and `w` — the monthly rates |
| `l(t)` | in-force probability at the start of month `t`; `l(0) = 1` (`pols_if`) |
| `l_p(t)` | the part of `l(t)` still paying its own premium (`pols_payer`); `l_p ≡ l` without the APL |
| `D(t)`, `S(t)`, `conv(t)` | expected deaths; expected surrenders; expected target conversions, in month `t` |
| `AV(t)`, `AV0(t)` | 積立金 at the start of month `t`; the same fund on the `i0` basis |
| `IDB(t)`, `DB(t)` | 増加死亡保険金額; the death benefit `SA + IDB(t)` (LEVEL) |
| `φ(t)`, `μ` | premium charge rate (`φ1` months 0–23, `φ2` months 24–n−1); annual maintenance rate |
| `C_init`, `C_maint`, `C_coi` | the three account-value charges in month `t` |
| `sc(t)`, `mva(t)`, `kl(t)` | 解約控除率; 市場価格調整率; 低解約返戻金割合 |
| `CV(t)` | payable 解約返戻金 (`cv_pp`) |
| `rem(t)` | years remaining in the current 積立利率適用期間 (SINGLE) |
| `Δ(t)`, `A`, `r0`, `d` | rate move since the contract's rate was set; MVA spread, base rate, damping |
| `e(t)`, `s` | reference TTM at month `t`, ¥ per US$1; the 為替手数料 spread, ¥0.50 |
| `g` | 目標値, a multiple of the yen premium paid |
| `E0`, `e_m(t)`, `c0`, `c_r`, `ec` | acquisition expense; monthly maintenance; initial and renewal commission; claim expense |
| `CF(t)` | net cash flow of month `t`, **income-positive** (`net_cf`), in US dollars |

**Dimensional check.** `q`, `w`, `q_m`, `w_m`, `l`, `φ`, `sc`, `mva`, `kl`, `c0`, `c_r`, `g`
and `d` are dimensionless; `i0`, `ic`, `μ`, `Δ`, `A`, `r0` are per annum and every one of
them is divided by 12 or raised to the power `1/12` before it touches a monthly quantity;
`SA`, `P`, `AV`, `AV0`, `IDB`, `CV`, `E0`, `e_m`, `ec` and every term of `CF(t)` are **US
dollars per policy issued**; `e(t)` and `s` are **¥ per US$1**, so every yen figure in this
file is a product of exactly one dollar quantity and exactly one rate — never a sum of a
dollar and a yen quantity, and never a dollar quantity multiplied by two rates. `rem(t)` is
in years and appears only as the exponent `d × rem(t)`.

### The currency layer

Every crossing of the currency boundary is a spread, not a rate [S1] [S3] [S5] [S7]:

    premium_jpy(t) = P × (e(t) + s)                 [円入金特約, capped at TTS]
    benefit_jpy(t) = benefit_usd(t) × (e(t) − s)    [円支払特約, floored at TTB]
    expense_jpy(t) = expense_usd(t) × e(t)          [never crosses the boundary]

so the yen ledger is **three translations, not one**, and

    net_cf_jpy(t) ≠ net_cf(t) × e(t)

identically. The difference is the insurer's spread income, `s × (premiums + benefits)`, and
the model publishes it as its own column rather than letting it hide inside a translated net
figure. At the reference TTM the round trip costs `(e + s)/(e − s) − 1 = 0.6292%`, and one
leg costs `s/e = 0.3136%` — which is why every carrier warns that a loss can arise with no
exchange-rate movement at all. The base run holds `e(t) = 159.43` flat **[std]**: this
library models contractual cash flows, not an FX view [S11].

### The account value recursion

One line, identical on both shapes, with the order fixed because it changes the answer at
the third decimal and the published run is reproduced to the dollar:

    AVg(t)     = AV(t) + P(t) − C_init(t)
    C_init(t)  = φ(t) × P(t)
    C_maint(t) = (μ / 12) × AVg(t)
    C_coi(t)   = min( qc_m(t) × max(0, DB(t) − (AVg(t) − C_maint(t))),
                      max(0, AVg(t) − C_maint(t)) )
    AV(t+1)    = (AVg(t) − C_maint(t) − C_coi(t)) × (1 + j)

The charge reads `qc`, not `q`: the rate that funds the benefit is a pricing element the
insurer filed [REG-R2], and wiring `mort_be_factor` to it as well would make the account
value absorb the model's own mortality sensitivity instead of the cash flow showing it. On
every cell below `mort_be_factor = 1`, so the two rates coincide and the distinction costs
nothing — which is exactly why it has to be stated rather than discovered at the first
sensitivity.

**`C_coi` carries two bounds, and only the outer one is a standardization.** The inner
`max(0, ·)` is structural: once `AV` overtakes `DB` the net amount at risk is zero and the
charge stops, and the death benefit must **not** be floored at the fund in exchange. The
outer `min(·)` caps the charge at what the fund actually holds, so the 積立金 can never run
negative — it is an account, not a debt. No retrieved document states that cap; it is a
modelling construction and therefore **[std]**. It binds on the 低解約返戻金特則 cell, whose
lower premium the back-solved charge stack does not make self-funding to the terminal age:
the 積立金 is exhausted in the sixth decade, the guaranteed 終身 cover is thereafter carried by
the insurer rather than by the fund, and the surrender value is nil. Without the cap the
shortfall compounds into the net amount at risk and the projection diverges.

**None of the three charges is a cash flow.** They are internal transfers from the account
value to the insurer; the insurer's cash outgo is the expense and commission stream in class
(c). Booking `C_init` as revenue *and* the premium as revenue double-counts the premium,
which is the second pitfall in the list.

### The death benefit and the two mechanics that vanish at the floor

On the LEVEL shape `DB(t) = SA + IDB(t)`, and 約款第46条 defines the uplift as the excess of the
fund actually held over the fund needed to carry the sum assured with no future premiums at
the 予定利率 [S2]:

    IDB(t) = max( IDB(t−1) , AV(t) − AV0(t) ) ,  floored at 0, computed monthly

with the `max` against the previous month being the **ratchet** — sourced to the ご契約のしおり and
not to the extracted 約款 text, therefore [unverified], and carried as the switch
`idb_ratchet` [S2].

`AV0(t)` is the quantity the 約款 does not define numerically, because it rests on the
insurer's unpublished 予定死亡率 and 予定事業費率 [REG-R2]. **[std] definition:** `AV0(t)` is the
account value the *same recursion* produces with `ic ≡ i0`. Under it `IDB(t) ≡ 0` on the
guaranteed run for every `t`, exactly and by construction, which is what the published
guaranteed column requires: it shows 特別積立金 of (0) at both 10 and 20 years and no uplift line
at all [S2]. The alternative reading — `AV0(t)` as the prospective fund at `i0` on the same
charge basis with no future premiums — is implemented as the switch `idb_basis =
"prospective"`, and it does **not** give an identically zero uplift: it gives `AV − AV0` of
−US$21,818.29 at 10 years, **+US$8.73** at 20 years, +US$67.86 at 50 years and
+US$22,617.69 at the terminal month. The near-zero crossing at 払込満了 is a strong independent
check on the fitted charge stack — the contract is almost exactly self-funding at the floor,
which is what actuarial equivalence predicts — but a definition that manufactures a positive
uplift on the guaranteed run contradicts the only document that shows the guaranteed run, so
it is the switch and not the base.

The **特別積立金** is a top-up computed from ten-year investment performance and added at 10 and
20 years in force [S1] [S2]. On the base run it is **identically zero**, and the published
table confirms it: (0) in the 3.00% column at both durations against 147 / 527 at 3.50% and
302 / 1,120 at 4.00% [S2]. A model that produces a non-zero uplift or a non-zero top-up on
the guaranteed run has a bug, and both are tests.

The 約款 does not publish how the top-up is computed, so the amount is a **[std]**
reconstruction, and it is *fitted* rather than assumed. Taking it as a share of the same
excess the uplift is measured against,

    特別積立金(120) = σ10 × max(0, AV(120) − AV0(120))
    特別積立金(240) = σ20 × max(0, AV(240) − AV0(240))

and solving on the four published amounts gives `σ10` = **0.24** and `σ20` = **0.16**. At
3.50% the reconstruction returns 146.89 against a published 147 (−0.1%) and 521.68 against
527 (−1.0%); at 4.00%, 297.79 against 302 (−1.4%) and 1,078.39 against 1,120 (−3.7%) — a
worst deviation of **3.7%** on two parameters against four figures. The 20-year amounts are
computed on a fund that already carries the compounded 10-year top-up, which is what the
recursion does; measuring the 20-year excess without it would understate `σ20` by about a
tenth. Both shares are zero on the SINGLE shape, which has no 特別積立金 [S3].

On the SINGLE shape there is no sum assured above the fund: `DB(t) = max(AV(t), CV(t))`, and
the `max` binds — where the MVA is strongly negative the surrender value exceeds the account
value and the death benefit follows the higher [S3].

### The surrender layer

    CV(t) = AV(t) × (1 − mva(t) − sc(t)) × kl(t)

`sc(t) = 0.07 − 0.007 × floor(t/12)` for `t < 120`, zero thereafter, constant within each
policy year, applied to the **積立金** [S3]. It is a charge: one-sided, never adding value,
disclosed under the 説明義務's restriction-on-cancellation limb [REG-R39].

`mva(t)` is **not** a charge. It is symmetric and can be negative [S3] [R8]. No carrier
publishes a closed form — the 監督指針 asks for an illustration of the deducted proportion,
which is exactly what a rate table is [R3] — so the reference implementation adopts the
published table as the artefact and specifies this **[std]** reconstruction of it:

    mva(t) = 1 − ( 1 + (Δ(t) + A) / (1 + r0) ) ^ ( −d × rem(t) )

with `A` = **0.10%**, `r0` = **3.00%** and `d` = **0.70**, all [std]. `Δ(t)` is the move in
the applicable 基準利率 since the contract's own 積立利率 was set, and `rem(t)` is the years
remaining in the 積立利率適用期間. **The reconstruction reproduces all 140 cells of the published
15-year table exactly at the printed four decimal places**, with a maximum absolute
deviation of 0.000050 before rounding. Two structural facts drop out of the fit rather than
being imposed: the zero column sits at `Δ = −0.1%`, which is what `A` is, so a contract
surrendered with **no rate move at all** still carries a small positive adjustment
(`+0.0095` at 14 years remaining); and the effective duration is `d × rem`, i.e. **0.70 of
the remaining term**, not the remaining term itself. `mva(t) = 0` where `t` falls on an
積立利率計算基準日 or inside a one-year 積立利率適用期間, and identically on the LEVEL shape [S3] [S2].

`kl(t)` is 0.70 while four or more premium-paying years remain, stepping to 0.775, 0.85 and
0.925 at three, two and one remaining years and to 1.00 at 払込満了, with the remaining count
measured from the monthly policy anniversary of the last premium paid and rounded **up** to
whole years [S2]. The step is a cliff; the chassis specifies it and the clawback that keeps
a non-paying cohort suppressed past 払込満了.

### Processing order (policy month `t = 0 … T − 1`)

1. **Start of month — premium.** Collect `P × l_p(t)` if `t < n` — on `l_p`, the cohort
   still paying its own premium, not on the whole of `l`: a policy the 自動振替貸付 is carrying
   credits the 積立金 but pays the insurer nothing, and booking its premium as cash income is
   the pitfall the chassis lists. `l_p ≡ l` on every model point without the APL. On the
   SINGLE shape this is a single collection at `t = 0`.
2. **Start of month — account-value charges,** in the order `C_init`, `C_maint`, `C_coi`.
   These change `AV` and produce no `net_cf` entry.
3. **Start of month — insurer expenses.** `e_m(t) × l(t)`, on the whole of `l`; renewal
   commission `c_r × P × l_p(t)` for `12 ≤ t < n`, on `l_p`, because commission is paid on
   premium actually collected. At `t = 0` additionally `E0` and `c0 × 12P`.
4. **End of month — interest.** Credit `(1 + j)` to give `AV(t+1)`.
5. **End of month — uplift.** Recompute `AV0(t+1)` and `IDB(t+1)`; at `t + 1 = 120` and `t +
   1 = 240` add the 特別積立金 (zero in the base run).
6. **End of month — surrender value.** Compute `sc(t+1)`, `mva(t+1)`, `kl(t+1)`, `CV(t+1)`.
7. **End of month — deaths.** `D(t) = l(t) × q_m(t)`; outgo `DB(t) × D(t)`; claim expense
   `ec × D(t)`.
8. **End of month — surrenders,** applied to survivors of mortality **[std order: death
   before surrender]**: `S(t) = l(t) × (1 − q_m(t)) × w_m(t)`; outgo `CV(t+1) × S(t)`.
9. **End of month — target test** (rider on, SINGLE): if `t + 1 ≥ 12` and `CV(t+1) × (e(t+1)
   − s) ≥ g × P_single × (e(0) + s)`, apply the elected treatment.
10. **Update in force.** `l(t+1) = l(t) × (1 − q_m(t)) × (1 − w_m(t))`.
11. **At `t = T − 1`** the table's terminal rate is 1, so `l(T) = 0` and the projection
    ends.

### Net cash flow

Income-positive, per policy issued, in US dollars:

    CF(t) = P × l_p(t) × 1{t < n}                    (premiums)
          − DB(t) × D(t)                             (death and 高度障害 claims)
          − ec × D(t)                                (claim expense)
          − CV(t+1) × S(t)                           (surrender benefits)
          − CV(t+1) × conv(t)                        (target conversions)
          − e_m(t) × l(t)                            (maintenance expense)
          − c_r × P × l_p(t) × 1{12 <= t < n}        (renewal commission)
          − (E0 + c0 × 12P) × 1{t = 0}               (acquisition)

`l_p(t)` is the cohort still paying its own premium, which is `l(t)` on every model point
without the 自動振替貸付: a policy the APL is carrying credits the 積立金 but pays the insurer
nothing, so the premium and the renewal commission ride on `l_p` while the maintenance
expense rides on the whole of `l`. `conv(t)` is zero unless the target election is
`convert`; under `surrender` the same policies leave through `S(t)` instead, which is why
the two elections move the money between columns and not in total. On the SINGLE shape the
two commission terms are replaced by the pair in class (c).

Result columns: `pols_if` first, then `premiums`, `claims_death`, `claims_lapse`,
`conversions`, `claim_expenses`, `expenses`, `commissions`, `net_cf`, then the translation
block
`net_cf_jpy` and `fx_spread_jpy`, then the state columns `av_pp`, `cv_pp`.
`claim_expenses` is its own column and `expenses` is acquisition and maintenance only: the
two are driven by different levers — the death decrement and the in-force count — and
folding one into the other hides which moved.
`conversions` is the 解約返戻金 leaving the dollar ledger where a target hit is taken as
a conversion rather than as a surrender: it is not a claim — the liability continues in
yen, out of this model's scope — so it is booked apart from `claims_lapse` rather than
inside it, and it is a column of zeros on every model point without the rider.
**Roll-forward identity:** the
table terminates, so every policy leaves by one of the two decrements and `Σ D(t) + Σ S(t) =
1` with `l(T) = 0` — with the target conversion, where the rider is elected, as the third
and only other exit, so the identity is `Σ D(t) + Σ S(t) + Σ conv(t) = 1` in general and
collapses to the first form wherever the rider is off. `check_pols_roll_fwd()` takes no
argument and returns a bool, with the per-`t` residual at
`check_pols_roll_fwd_resid(t)`.

---

## Policyholder behavior modeling

All dynamic forms are **[std]** reference constructions.

- **Base surrender.** The two duration tables in class (c). The LEVEL table has no public
  anchor; the SINGLE table has one good one and is fitted to it.
- **Dynamic surrender on the FX rate [std] (optional module, off in base).** The
  economically natural driver on this product is not the crediting rate but the currency: a
  policyholder in yen profit surrenders, one in yen loss holds on. A reference multiplier on
  the SINGLE shape:

      w_dyn(t) = w(t) × min(2.5, max(0.5, 1 + β × (CV(t) × (e(t) − s) / P_jpy0 − 1)))

  with `β` = 2.0 **[std]** and `P_jpy0` = the yen the policyholder actually paid,
  `single_premium × (e(0) + s)`. Under the base run's flat FX path this multiplier moves
  only with the account value, which is precisely the limitation named below.
- **The target-value rider is a path-dependent option and a deterministic run values it at
  intrinsic only.** On a single deterministic path the rider either converts at one
  determinate month or never converts; its time value — the value of the right to convert on
  whichever future path happens to reach the target first — is **zero by construction**.
  This is the same degeneracy `uklib`'s RPI ratchet suffers under a monotone index path, and
  it must be stated, not smoothed: a deterministic projection can price the conversion
  *event* correctly and cannot price the *option* at all. A scenario set is the only
  instrument that can, and this library does not ship one.
- **What happens at a target hit is an election, not a mechanic.** The contract converts to
  a yen whole life [S8] [S9]. The observed population does something else: at every
  focus-monitored distributor most ターゲット型 policies are **surrendered** on reaching the
  target and the same product is immediately re-sold to the same customer, charging the
  front-loaded commission twice [R5] [R6]. The model carries `target_action ∈ {convert,
  surrender}` with no default, because the contract and the evidence disagree and neither is
  the modeller's to assume silently.
- **The test is on the surrender value, not the account value** [S9]. The worked example
  measures what that costs: thirteen months.
- **The one-year dead zone is contractual** [S9] and interacts with the surrender charge,
  which is 7.0% and 6.3% over exactly that window [S3].
- **自動振替貸付.** Inherited unchanged on the LEVEL shape, absent on the SINGLE shape. A policy
  does not lapse while the account value can carry the premium, so applying a lapse rate to
  unpaid premiums without first running the APL test models a decrement the contract does
  not have (the [whole life technical notes (終身保険)](../whole_life/technical-notes.md)).
- **復活 is not modelled [std],** as on the chassis; every exit is terminal, which understates
  later-duration in force.
- **免責 incidence is zero in the base run [std].** Where a death claim is refused the 積立金 is
  still paid [S2] — a real cash flow on an account-value product, with no analogue on a pure
  protection product.

---

## Worked example

**Anchor cell (`point_id = 1`).** Male, 契約年齢 40 (満年齢), LEVEL shape, 米ドル建, 基本保険金額
**US$100,000**, 保険期間 終身, 保険料払込期間 60歳払込満了 (`n` = 240 monthly premiums), 月払保険料 **US$239.60**
[S2], 低解約返戻金特則 **off**, 積立利率 held at the guaranteed floor **3.00%** [S2], `e` = **¥159.43**
per US$1 held flat [S11], `s` = **¥0.50**. `T = 12 × (109 − 40 + 1) = 840` months, attained
ages 40 to 109.

**Every assumption value the cell uses.** `q` from the canonical proxy for
生保標準生命表2018（死亡保険用）男 with `mort_be_factor = 1.00`, log-linear in `ln q` between the sourced
anchors and rounded to five decimals — **q40 = 0.00118, q41 = 0.00128, q42 = 0.00139, q43 =
0.00151, q44 = 0.00163, q45 = 0.00177** (q40 and q45 are anchors, the four between them are
interpolated), and q50 = 0.00285, q60 = 0.00653, q90 = 0.15760 at the anchors themselves
[REG-R18]; the interpolation is **[std]** and the anchors are not. `lapse_rate` = 8% / 7% /
6% / 5% in policy years 1 to 4, then 5% to year 10, 4% to year 20 and 3% thereafter
**[std]**, by the class (c) table. Charges `φ1` = 0.38, `φ2` = 0.13, `μ` = 0.005
**[std]**, derived immediately below. Expenses `E0` = US$300, `c0` = 0.90, `c_r` = 0.03,
`e_m(t)` = US$60/12 × 1.01^floor(t/12), `ec` = US$150, all **[std]**. Monthly conversions:
`q_m(40) = 1 − (1 − 0.00118)^(1/12) = 0.0000983866`; `w_m(year 1) = 1 − (1 − 0.08)^(1/12) =
0.0069243826`; `1 + j = 1.03^(1/12) = 1.0024662698`.

### Calibration of the charge stack

Three parameters against nine published dollar figures on the guaranteed column [S2],
surrender values taken net of the 解約控除 scale of `product-spec.md` footnote 20:

| duration | `sc` | model `AV` | model `CV` | published 解約返戻金 | difference |
|---|---|---|---|---|---|
| 3 | 4.9% | 5,895.43 | 5,606.56 | 5,557 | +49.56 (+0.89%) |
| 5 | 3.5% | 11,030.45 | 10,644.39 | 10,822 | −177.61 (−1.64%) |
| 7 | 2.1% | 16,389.60 | 16,045.42 | 16,332 | −286.58 (−1.75%) |
| 10 | 0.0% | 24,854.87 | 24,854.87 | 25,082 | −227.13 (−0.91%) |
| 15 | 0.0% | 40,224.87 | 40,224.87 | 40,128 | +96.87 (+0.24%) |
| 20 | 0.0% | 57,431.26 | 57,431.26 | 57,329 | +102.26 (+0.18%) |
| 30 | 0.0% | 69,377.65 | 69,377.65 | 69,516 | −138.35 (−0.20%) |
| 40 | 0.0% | 81,529.59 | 81,529.59 | 81,350 | +179.59 (+0.22%) |
| 50 | 0.0% | 90,686.78 | 90,686.78 | 90,715 | **−28.22 (−0.03%)** |

Three parameters reproduce a carrier's whole published run to within **1.75%** at every one
of nine durations spanning forty-seven years, and to 0.03% at duration 50. The stack is a
back-solve, so it is re-solved whenever its inputs move: adopting the library's canonical
mortality proxy changed `qc` at every attained age above 40 and `φ2` re-solved from 12% to
13% with `φ1` and `μ` unmoved. Cumulative
premium checks independently: 240 × 239.60 = **US$57,504.00**, the published 払込保険料累計額 at 20
years [S2]; 36 × 239.60 = 8,625.60, published as 8,626 because the booklet rounds the
cumulative premium **up** to the whole dollar while rounding surrender values **down** [S2].

Cross-check against the *other* published table — the 低解約返戻金特則 form, premium US$225.00, `kl`
= 0.70 through the suppressed period — with the **same** charge parameters: model CV of
3,669.20 / 6,966.38 / 10,498.61 / 16,252.70 / 26,266.61 at durations 3 / 5 / 7 / 10 / 15
against published 3,560 / 7,081 / 10,824 / 16,892 / 27,706, and 53,475.52 against 53,029 at
duration 20 where `kl` releases to 1.00 [S2]. The worst deviation is **−5.20%** at duration
15. That is a genuine cross-validation and it is looser than the primary fit, as it should
be: the 特則 form is a different contract with a different premium, and its charge rates were
not fitted. One feature of the published 特則 table is **not** reproducible and is flagged
rather than fitted: it prints surrender values at durations 30, 40 and 50 that are
*identical* to the ordinary form's, although the two forms have paid different premiums and
hold different funds at duration 20 (53,029 against 57,329). No recursion produces that
convergence; the identity is [unverified] and the 特則 fit is anchored only on durations ≤ 20.

### First periods of the base run

Per policy issued, income-positive, in **US dollars**. `av_pp` and `cv_pp` are stated at the
**end** of the month, i.e. `AV(t+1)` and `CV(t+1)`.

| t | `pols_if` | premiums | claims_death | claims_lapse | claim_expenses | expenses | commissions | `net_cf` | `av_pp` | `cv_pp` |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1.000000 | 239.6000 | 9.8387 | 0.8951 | 0.0148 | 305.0000 | 2,587.6800 | −2,663.8285 | 139.01 | 129.28 |
| 1 | 0.992978 | 237.9175 | 9.7696 | 1.7795 | 0.0147 | 4.9649 | 0.0000 | +221.3889 | 278.31 | 258.83 |
| 2 | 0.986005 | 236.2468 | 9.7010 | 2.6533 | 0.0146 | 4.9300 | 0.0000 | +218.9479 | 417.92 | 388.67 |
| 3 | 0.979081 | 234.5879 | 9.6328 | 3.5167 | 0.0144 | 4.8954 | 0.0000 | +216.5285 | 557.83 | 518.78 |
| 4 | 0.972206 | 232.9406 | 9.5652 | 4.3697 | 0.0143 | 4.8610 | 0.0000 | +214.1303 | 698.03 | 649.17 |
| 5 | 0.965379 | 231.3049 | 9.4980 | 5.2125 | 0.0142 | 4.8269 | 0.0000 | +211.7532 | 838.54 | 779.84 |
| … | | | | | | | | | | |
| 119 | 0.554213 | 132.7893 | 11.9760 | 58.7416 | 0.0180 | 3.0307 | 3.9837 | +55.0395 | 24,854.87 | 24,854.87 |
| 239 | 0.353031 | 84.5862 | 17.6411 | 68.8206 | 0.0265 | 2.1325 | 2.5376 | −6.5721 | 57,431.26 | 57,431.26 |
| 240 | 0.351656 | 0.0000 | 19.1935 | 51.2541 | 0.0288 | 2.1454 | 0.0000 | −72.6218 | 57,525.60 | 57,525.60 |

**Trace, month 0.** `C_init = 0.38 × 239.60 = 91.0480`; `AVg = 0 + 239.60 − 91.0480 =
148.5520`; `C_maint = (0.005/12) × 148.5520 = 0.0618967`; the fund before the mortality
charge is `148.4901033`, so the net amount at risk is `100,000 − 148.4901033 =
99,851.5098967` and `C_coi = 0.0000983866 × 99,851.5098967 = 9.8240461`; `AV(1) = (148.5520
− 0.0618967 − 9.8240461) × 1.0024662698 = 138.6660572 × 1.0024662698 = 139.0080451`. `sc(1)
= 7.0%`, so `CV(1) = 139.0080451 × 0.93 = 129.2774820`. Decrements: `D(0) = 1 ×
0.0000983866`, death claims `= 100,000 × 0.0000983866 = 9.8386555`; `S(0) = (1 −
0.0000983866) × 0.0069243826 = 0.0069237014`, surrender benefits `= 129.2774820 ×
0.0069237014 = 0.8950787`. Expenses `= 300.00 + 60/12 = 305.0000000` and, on its
own line, claim expense `= 150 × 0.0000983866 = 0.0147580`; commission `= 0.90 × 12 ×
239.60 = 2,587.6800`. `CF(0) = 239.6000 − 9.8386555 − 0.8950787 − 0.0147580 − 305.0000000
− 2,587.6800 = −2,663.8284922`. Update: `l(1)
= (1 − 0.0000983866) × (1 − 0.0069243826) = 0.9929779`.

**Trace, month 1.** Premiums `= 239.60 × 0.9929779 = 237.9175077`. `AVg = 139.0080451 +
148.5520 = 287.5600451`; `C_maint = 0.1198167`; `C_coi = 0.0000983866 × (100,000 −
287.4402284) = 9.8103753`; `AV(2) = (287.5600451 − 0.1198167 − 9.8103753) × 1.0024662698 =
278.3145633`; `CV(2) = 278.3145633 × 0.93 = 258.8325438`. `D(1) = 0.9929779 × 0.0000983866 =
0.0000976956`, claims `= 9.7695676`; `S(1) = 0.9929779 × (1 − 0.0000983866) × 0.0069243826 =
0.0068750825`, surrender benefits `= 258.8325438 × 0.0068750825 = 1.7794951`. Maintenance `=
5.0000 × 0.9929779 = 4.9648896` (the inflation factor is 1.01^0 = 1 for months 0–11); claim
expense `= 0.0146544`; no commission (renewal starts at `t = 12`). `CF(1) = 237.9175077 −
9.7695676 − 1.7794951 − 0.0146544 − 4.9648896 = 221.3889011`.

**Trace, month 2.** Premiums `= 239.60 × 0.9860051 = 236.2468301`. `AVg = 278.3145633 +
148.5520 = 426.8665633`; `C_maint = 0.1778611`; `C_coi = 0.0000983866 × (100,000 −
426.6887022) = 9.7966751`; `AV(3) = 416.8920271 × 1.0024662698 = 417.9201953`; `CV(3) =
388.6657816`. `D(2) = 0.0000970096`, claims `= 9.7009649`; `S(2) = 0.0068268051`, surrender
benefits `= 2.6533455`; maintenance expense `= 4.9300257` and claim expense `= 0.0145514`.
`CF(2) = 236.2468301 − 9.7009649 − 2.6533455 − 0.0145514 − 4.9300257 = 218.9479426`.

**The yen ledger, month 0.** Three translations, not one. Premium `239.6000 × (159.43 +
0.50) = ¥38,319.23`; benefits `(9.8386555 + 0.8950787) × (159.43 − 0.50) = ¥1,705.91`;
expenses and commission `(0.0147580 + 305.0000000 + 2,587.6800) × 159.43 = ¥461,182.33`.
`net_cf_jpy(0) = ¥−424,569.01`, against `net_cf(0) × 159.43 = ¥−424,694.18` — a difference
of **¥125.17**, which is exactly the spread income `0.50 × (239.6000 + 10.7337342)`. The
two figures are both correct and mean different things, and a model that publishes only
the second has
silently given the spread away.

**Whole-run totals**, undiscounted, per policy issued: premiums US$34,036.04; death claims
US$20,911.81; surrender benefits US$23,345.07; claim expense US$31.37; acquisition and
maintenance expense US$1,536.77; commission US$3,525.76; `Σ CF(t)` = **−US$15,314.73**.
`Σ D(t) = 0.209118071` and `Σ S(t) = 0.790881929`, summing to **1.000000000**, with
`pols_if(840) = 0`. In yen: premiums ¥5,443,383; benefits ¥7,033,745; expenses and
commission ¥812,120; `Σ net_cf_jpy` = **¥−2,402,482**, against `Σ net_cf × 159.43 =
¥−2,441,628` — the ¥39,146 gap being the whole-run FX spread income. Two structural facts
fall out of these totals: **85.2%** of expected death claims arrive after 払込満了, and
surrenders take 79.1% of the cohort out against mortality's 20.9%, so this is a lapse-driven
liability wearing a mortality product's clothes.

### The MVA and the target conversion, on the SINGLE shape

Model point: 一時払保険料 **US$100,000**, 基本保険金額 equal to it [S3], issue age 60, 契約初期費用 4.50%
[S10] so the fund after the premium and that charge is `US$95,500.00` — `AV(0)` itself is
zero on the convention above, which reads it *before* the month's premium — 積立利率 4.72%
fixed for a 15-year 積立利率適用期間 [S4], 目標値 `g` = 110%, flat FX and a flat rate path. Yen
premium paid `= 100,000 × 159.93 = ¥15,993,000`; 目標額 `= 1.10 × that = ¥17,592,300`.

At month 36, twelve years remaining, the MVA against a range of rate moves is

| `Δ` | +2.0% | +1.0% | 0.0% | −1.0% | −2.0% |
|---|---|---|---|---|---|
| `mva(36)` | +0.155947 | +0.085368 | **+0.008118** | −0.076506 | −0.169292 |
| `CV(36)`, US$ | 87,194.38 | 94,934.87 | 103,406.90 | 112,687.73 | 122,863.68 |

Two things to read off it. The zero-move column is **not zero** — the published table's zero
column sits at `Δ = −0.1%` [S3], so a contract surrendered with the market exactly where it
started still pays an MVA of 0.81%. And at `Δ = −1.0%` the yen-converted surrender value is
already ¥17,909,461, above the 目標額, at duration three: **a fall in interest rates triggers
the target conversion**, entirely without help from the crediting rate or the currency.

On the flat path the target is reached at **month 52** (four years four months), where `AV =
116,626.82`, `mva = 0.007219`, `sc = 4.2%`, `CV = 110,886.51` and `CV × 158.93 = ¥17,623,193
≥ ¥17,592,300`. Three counterfactuals measure the mechanics that the trigger is easy to get
wrong about: testing the **account value** instead of the surrender value hits at month
**39**, thirteen months early; ignoring the 解約控除 alone hits at month 41; ignoring the MVA
alone hits at month 50. The 解約控除 moves the trigger further than the MVA does because it is
the larger deduction over exactly this window — `sc` of 4.9% at month 41 then 4.2% at month
52, against an `mva` of 0.78% and 0.72% at the same two months — so dropping it must
trigger earlier, and the two counterfactuals order accordingly.
Under the flat path the conversion is exercised once and its option value is zero — see the
note on intrinsic value above.

---

## Valuation and reserve pointers

This library projects gross liability cash flows. Every valuation layer consumes them and is
cited, never reproduced.

- Standard policy reserve (*hyōjun sekinin-junbikin*, **標準責任準備金**). 保険業法第116条 obliges the
  reserve and delegates the method and coefficients [REG-R4]; 施行規則第68条 fixes the scope and
  第69条 the taxonomy — 保険料積立金, 未経過保険料, 払戻積立金, contingency reserve (*kiken junbikin*, 危険準備金)
  [REG-R7] [REG-R8]; 平成8年大蔵省告示第48号 sets 平準純保険料式 with no Zillmer adjustment, the table
  vintages and the standard valuation interest rate (*hyōjun riritsu*, 標準利率) machinery
  [REG-R10]. The product-specific fact is the **date**: USD-
  and AUD-denominated contracts entered the regime only on **1 October 2021**, with the
  平成13年金融庁告示第24号 changes from 1 April 2022, and every other foreign currency remains outside
  the 対象契約 [R1] [REG-R12]. The USD 標準利率 is built from A-rated same-currency corporate bond
  yields at 10 and 20 years through banded 安全率係数, reset off a 基準日 on the 1st of every month
  [R1]. **No retrieved page publishes the resulting numeric rate**, so this library asserts
  none; the carrier-published 基準利率 and 市場価格調整用利率 series [S4] [S12] [S14] are proxies for the
  level, not the statutory rate. An 積立利率変動 contract stays in scope because 施行規則第68条 excludes
  contracts whose 約款 lets the insurer change the **予定利率**, not contracts whose crediting
  rate floats above a fixed one [REG-R7]. 価格変動準備金 is asset-driven and out of scope [REG-R3],
  but carries an FX-specific rule worth naming: computed inside the 責任準備金 of 外貨建て保険 its
  asset scope must come from the matching segment on a segregated basis, and the **危険準備金Ⅱ**
  for those contracts must use the **外貨建て保険 risk coefficient** [R4].
- **ESR.** From **31 March 2026** insurers are supervised on 経済価値ベースのソルベンシー規制, liabilities
  at 現在推計 plus MOCE, re-measured at each 基準日, calibrated in principle to 99.5%, with early
  corrective action below **100%**, replacing the ソルベンシー・マージン比率 **200%** trigger
  [REG-R15] [REG-R17]. This projection is the 現在推計 cash-flow engine and nothing more: `BEL =
  Σ_t v(t) × [outgo(t) − income(t)]`, with `v(t)`, MOCE and the standard-formula
  coefficients out of scope — the 柱告示 were not opened and their coefficients are
  [unverified] [REG-R16]. **為替 is a named market-risk category** in the standard model
  [REG-R15], and this is the one product in the library whose liability is denominated in a
  currency the capital requirement charges for directly. The old basis was ロックイン; a contract
  whose crediting rate is redeclared monthly and whose surrender value moves with market
  rates is exactly the contract a locked-in basis cannot describe.
- **The 意見書 chain.** 保険業法第121条第1項第1号 requires the 保険計理人, appointed under 第120条, to confirm
  the reserve is soundly accumulated [REG-R5] [REG-R6]; the IAJ 実務基準 turns that into the
  **1号収支分析**, a forward income-and-outgo analysis over at least ten future years by segment
  under prescribed scenarios, addressing MVA and foreign-currency business explicitly
  [REG-R22]. That is the shape of the output above.
- **Accounting.** **IFRS 17 is not mandatory in Japan** — IFRS applies as 指定国際会計基準 on a
  voluntary basis [REG-R47]. J-GAAP statutory reserving, the ESR economic balance sheet and
  IFRS 17 are three bases over one set of projected cash flows, and this model keeps the
  cash flows basis-agnostic.
- **Disclosure, binding on the outputs rather than on the valuation.** The 監督指針 requires an
  MVA product to illustrate the proportion deducted from the 保険料積立金 at surrender and to
  disclose the in-force charges, and requires an 外貨建て保険 to state that the yen-converted
  benefit can fall below the yen-converted premium [R3] [REG-R14]; the 適正表示ガイドライン requires
  the 実質的な利回り beside the 積立利率, measured where the MVA, the rate-variation period and the
  surrender charge have **all** expired [R8]. On the anchor cell that point is duration 20,
  and the model can produce it; the library does not publish it, because a yield is a
  pricing statement and this is a cash-flow model.

---

## Key sensitivities and model risks

In rough order of leverage:

1. **The crediting rate.** The base run sits on the guaranteed floor, which is the only
   crediting figure for this shape that is a contract term [S2] — and the only one
   available, since the declared-rate history page is not machine-fetchable [S16]. Moving
   from 3.00% to 4.00% moves the published 50-year surrender value from 90,715 to 141,257, a
   factor of 1.56 [S2]. Every non-guaranteed element in the product — the uplift, the 特別積立金,
   the whole surrender-value run — is a function of this one lever.
2. **The charge stack.** `φ1`, `φ2` and `μ` are three **[std]** parameters carrying the
   entire surrender-benefit stream, calibrated to one carrier's published table for one
   model point [S2]. The fit at other issue ages, sexes and premium terms is **unverified**,
   because no second complete run exists in the retrieved set. A user with a real 算出方法書
   replaces the three and changes nothing else.
3. **The currency layer.** The spread is 0.63% on a round trip and is charged on every
   crossing; the *level* of `e(t)` scales the whole yen ledger linearly and the whole dollar
   ledger not at all. The base run's flat path is a modelling decision, not a forecast, and
   it is the assumption a reviewer should challenge second.
4. **SINGLE-shape persistency.** A four-year exit of 60.9% against an industry 解約・失効率 of
   5.6% [R5] [REG-R31] means the liability is realized in a handful of years, and the
   surrender charge and MVA both bind over exactly that window. The LEVEL curve, by
   contrast, rests on no public evidence at all.
5. **The MVA's deterministic degeneracy.** The reconstruction reproduces the published table
   exactly, but `Δ(t)` is an input, and a deterministic run holds it at zero — which is not
   a neutral choice, because the zero column sits at −0.1% and a flat path therefore still
   charges 0.81% at twelve years remaining. What a deterministic projection **cannot** say
   is anything about the MVA's convexity or about the value of the surrender option it
   prices.
6. **The target rider's option value is zero by construction** in this model. A book of
   ターゲット型 contracts is a book of short options on the FX-and-rate path, and their intrinsic
   valuation understates the liability by whatever the time value is — a number this library
   does not compute and does not estimate.
7. **The uplift's definition.** `AV0` is not a published quantity, and the two defensible
   definitions differ by US$8.73 at 払込満了 and by US$22,617.69 at the terminal month.
8. **The horizon.** ω = 109 male / 113 female; 85.2% of expected death claims fall after
   払込満了. Truncating the projection at 払込満了, or at age 100, is a direct understatement.

Known modeling pitfalls:

- **The policy currency is the model currency; yen is a translation.** Every state variable
  and every cash flow is in US dollars. A yen figure enters only through `e(t)` and `s`, and
  the exchange rate is a model point column, never a literal in a formula.
- **`net_cf_jpy(t) ≠ net_cf(t) × e(t)`.** Premiums translate at `e + s`, benefits at `e −
  s`, expenses and commission at `e`. On the anchor cell the difference is ¥125.17 in month
  0 and ¥39,146 over the run — the insurer's spread income, which disappears if the net
  figure is translated at one rate [S1] [S3].
- **The account-value charges are not cash flows.** `C_init`, `C_maint` and `C_coi` move
  `av_pp` and appear nowhere in `net_cf`. Booking a charge as revenue alongside the premium
  that funded it double-counts the premium.
- **`av_pp` is not `cv_pp`.** `CV = AV × (1 − mva − sc) × kl`, and all three factors can be
  active at once on the SINGLE shape. Paying a surrender on `av_pp` overstates every early
  surrender by up to 7% plus the MVA [S3].
- **The MVA is not a charge.** It is symmetric, it can be negative, and a fall in rates
  **increases** the surrender value [S3] [R8]. Implementing it as a deduction floored at
  zero models a different product. It is also zero on an 積立利率計算基準日 and inside a one-year
  積立利率適用期間, and identically zero on the whole LEVEL shape [S2] [S3] — a discontinuity a
  monthly model must place on the right month.
- **The surrender charge's base is the 積立金.** Three different bases are in use across the
  market — the account value, the 責任準備金 and the 基本保険金額 [S3] [S7] [S13] — and a rate quoted
  against one means nothing against another. Applying 7.0% to `SA` instead of `AV` is wrong
  by a factor of several at early durations.
- **The target test runs on the surrender value, after FX and MVA** [S9]. Testing the
  account value converts thirteen months early on the base SINGLE cell (month 39 against
  month 52), and the error grows with any rate move.
- **The one-year dead zone is real.** A target reached inside the first year does not
  trigger [S9]; a model that converts at month 6 has invented a contract term.
- **The uplift and the top-up are identically zero on the guaranteed run.** `IDB(t) ≡ 0` and
  特別積立金 ≡ 0 whenever `ic = i0`, and the published 3.00% column shows (0) at both 10 and 20
  years [S1] [S2]. A non-zero value on the base run is a bug, not a refinement.
- **`mort_be_factor` must not move the cost-of-insurance charge.** The decrement is an
  experience assumption; the charge basis is a pricing element [REG-R2]. Wiring one lever
  to both makes the model absorb its own mortality sensitivity inside the account value.
- **The APL is absent on the SINGLE shape.** There is no premium to advance, so the two
  shapes have different **decrement sets**, not merely different rates [S2] [S3]. A SINGLE
  point that carries a premium-default decrement is modelling a contract that does not
  exist.
- **The crediting month is the policy month.** The rate is declared on the 1st and applied
  from the 月単位の契約応当日 [S2]; crediting on calendar month ends is wrong for the life of the
  contract.
- **`(1 + ic)^(1/12)`, not `ic/12`.** The convention is **[std]** and the published run is
  reproduced to the dollar, so a nominal-over-12 implementation will miss the fit table
  above.
- **The 低解約返戻金 release is a step.** `kl` moves 0.70 → 0.775 → 0.85 → 0.925 → 1.00 on whole
  remaining years, rounded **up**, with the clawback keeping a non-paying cohort suppressed
  past 払込満了 [S2]. Interpolating across the boundary is wrong, as it is on the chassis.
- **The account value can overtake the sum assured.** On the anchor cell `AV` crosses
  US$100,000 at month **740** (attained age 101), after which the net amount at risk is zero
  and the cost-of-insurance charge stops. In-force there is 0.000579, so the effect is
  immaterial in expectation and structural in the code: `C_coi` must be floored at zero and
  the death benefit must not be silently floored at `AV`.
- **The account value can also be exhausted, and the charge must stop there.** `C_coi` is
  capped at `max(0, AVg(t) − C_maint(t))` **[std]**, so the 積立金 never runs negative. The
  cap binds on the 低解約返戻金特則 cell; without it the shortfall compounds into the net amount
  at risk and the projection diverges.
- **A refused claim still pays the fund.** Where a death benefit is excluded the 積立金 or
  解約返戻金 is paid [S2]. Modelling an exclusion as a zero-payment event overstates the
  insurer's position — a pure protection product's habit that does not transfer.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #jplib-fx_whole_life-r1
[R10]: #jplib-fx_whole_life-r10
[R3]: #jplib-fx_whole_life-r3
[R4]: #jplib-fx_whole_life-r4
[R5]: #jplib-fx_whole_life-r5
[R6]: #jplib-fx_whole_life-r6
[R8]: #jplib-fx_whole_life-r8
[REG-R10]: #jplib-reg-r10
[REG-R12]: #jplib-reg-r12
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
[REG-R5]: #jplib-reg-r5
[REG-R6]: #jplib-reg-r6
[REG-R7]: #jplib-reg-r7
[REG-R8]: #jplib-reg-r8
[std]: #jplib-std
[unverified]: #jplib-unverified
<!-- END generated citation links -->
