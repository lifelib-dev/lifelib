# Technical Notes

**Status:** Draft, 2026-09-03 (all cited sources accessed 2026-09-03).

**Scope note.** These notes turn the standardized composite whole life assurance
(*jongsin boheom*, 종신보험) of `product-spec.md` (same directory) into a reference
liability cash-flow projection on paper, and then into `WholeLife_KR_S` beside it. **They
describe no single insurer's contract.** [S#] and [R#] tags resolve against `sources.md`,
whose numbering is carried verbatim from `_research/whole-life.md` and is frozen; [REG-R#]
tags resolve against the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R1–R60 numbering is
separate and also frozen. **[std]** marks a standardization introduced for the reference
implementation; [unverified] marks a claim that could not be confirmed against a retrieved
document. **Every parameter value here is identical to `product-spec.md`'s**, and every
number in the worked example is read off the shipped model rather than recomputed by hand.

Three quantities appear here that the specification names but does not fix, all three
internal to the surrender-value and expense construction it defers to this document: the
gross-to-net loading `θ`, the acquisition-cost ratio `a` against the 표준해약공제액 cap, and
the first-year commission share `c₀`. Each is **[std]**, and each is derived, bounded or
calibrated below rather than asserted.

**This is the library's savings/protection chassis.** Five mechanics are specified once,
here, and inherited rather than restated:

- the **계약자적립액** (*gyeyakja jeongnibaek*, the policyholder account) recursion, the
  contractual successor of the 보험료적립금 (*boheomnyo jeongnipgeum*, policy reserve);
- the **해약환급금** (*haeyak hwangeupgeum*, surrender value) and its 해약공제액, capped by
  the **표준해약공제액** of 보험업감독규정 별표 14 [REG-R20];
- the **무해지환급형 / 저해지환급형** suppressed forms — nil, or a stated fraction `k`,
  during 납입기간, stepping up at 납입완료. **A cliff, not a curve**, carried as a model
  point column so the suppressed and the ordinary run appear side by side in one
  projection;
- the **보험계약대출** (policy loan) as a modelled state, unavailable during 납입기간 on a
  무해지환급형 contract because there is no value to lend against; and
- **보험료 납입면제** (premium waiver), a distinct in-force state in which premiums cease
  and are **deemed paid** for benefit and surrender-value purposes.

The [CI technical notes (CI보험)](../ci_insurance/technical-notes.md) inherit the whole of
it and add an accelerated critical-illness payment; the [pension savings technical notes
(연금저축보험)](../pension_savings/technical-notes.md) inherit the accumulation half. The
[term life technical notes (정기보험)](../term_life/technical-notes.md) carry the
protection chassis and its 갱신형 / 비갱신형 split, and share this document's
surrender-value regime, because 감독규정 제7-69조 and 제7-70조 apply 제7-65조 through
제7-68조 to 장기손해보험 and to 제3보험 *mutatis mutandis* — **one surrender-value regime
governs all ten `krlib` products** [REG-R19].

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows** per policy — premiums,
  death claims, surrender benefits, 감액 proceeds, expenses and commission — undiscounted
  and gross of reinsurance. Korea runs **three** measurement bases over one such stream and
  all three are live: IFRS 17 (K-IFRS 제1117호, mandatory since 2023-01-01) [REG-R60], K-ICS
  in the same quarter [REG-R13], and the **해약환급금준비금**, which has no counterpart
  anywhere else in this repository [REG-R11]. **Discounting, the risk adjustment, the CSM,
  요구자본 and every reserve are out of scope** and are cited, not reproduced — see
  *Valuation and reserve pointers*.
- **Time index.** `t` is **0-based** and counts **policy months**: `t = 0` is the first
  policy month, period `t` runs from month-end `t` to month-end `t + 1`, the frame is
  `t = 0 … proj_len − 1` with `proj_len = 12 × proj_years`, and the contractual policy year
  is the derived 1-based label `policy_year(t) = ⌊t/12⌋ + 1`, which is never indexed by.
  The anchor projects 912 rows. Values *at* a point in time — the account `V`, the surrender
  charge `SC`, the surrender values `W` and `CV`, `cumprem` and the loan balance `L` —
  carry a second index, the **month-end** `d = 0 … T` with `d = 0` at issue; the flows of
  month `t` read `d = t` as the opening month-end and `d = t + 1` as the closing one. A
  **계약해당일** is the month-end `d = 12y`, which is where every published 해지환급금 grid
  is quoted and where the value steps up at 납입완료.
- **Contract terms stay in years.** The 납입기간 `m`, the 해약공제기간 `n_sc`, the
  보험계약대출 drawdown year and the 감액 year are all written in policy years, because that
  is how the contract writes them; each has a month-count companion — `prem_period_mths`,
  `surr_chg_period_mths` — for the cells that index the grid. Only the grid is monthly.
- **Projection frequency.** **Monthly** (`WholeLife_KR_S`), and on this product the change
  of grid is not cosmetic. 감독규정 제7-66조제1항제4호 provides that the 계약자적립액 accrues
  **monthly** before 납입완료 and daily afterwards [REG-R19]. An annual grid could carry this
  product only through 제7-65조제2항's separate permission to compute the account on an
  annualised premium basis — 「연납보험료를 기준으로 하여 산출할 수 있다」 [REG-R18] — a
  permission the model used to take and to record as a **[std]** departure. The monthly grid
  does not need it.
- **What the monthly grid moved, and what it did not.** The sourced decrement basis is
  untouched and stays **annual**: both disclosed 적용위험률 grids are annual by age [S2]
  [S8] and the FSS 원칙모형 lapse vector is annual by 경과기간 [REG-R27], so `q(t)` and
  `w(t)` carry them and the monthly decrements `q^m(t)` and `w^m(t)` are
  `1 − (1 − q)^(1/12)` **[std]**, level inside a policy year and stepping at each
  계약해당일. Twelve monthly exits compound to the year's annual rate exactly, so **the
  in-force at every 계약해당일 reproduces the annual-step model this replaced**, to a
  relative 1.1e-14 across the shipped model points. The **계약자적립액 does move, by about
  1.2%**: it now accrues at `(1 + i)^(1/12) − 1` a month and is built from a
  **월납순보험료** struck by monthly equivalence, which is *not* the 연납순보험료 divided by
  twelve — a monthly equivalence discounts eleven of each year's twelve instalments and
  exposes them to the year's mortality, and the difference is about half a year's interest
  at the 예정이율, which is exactly the timing an annual grid gave away. The 연납순보험료
  survives beside it, because 별표 14 names that quantity and the statutory 표준해약공제액 is
  computed from it. Two smaller consequences: the 14-day **납입최고(독촉)기간** still
  collapses, now into the month rather than the year [S5 제25조]
  [REG-R25 제26조](#krlib-reg-r25); and **미경과보험료**, required on termination by
  제7-66조제5항 [REG-R19], is still not added, there being none on a grid with premiums in
  advance and surrenders at the month-end **[std]** — but the unearned amount a real
  contract would owe is now at most one month's premium rather than one year's.
- **Timing conventions [std].** Premium at the **start** of each month, in advance, for the
  months `t = 0 … 12m − 1`, on the paying cohort only; maintenance expense, the
  premium-related expense and renewal commission at the start of each month; acquisition
  expense and initial commission at issue, in month `t = 0`; death claims and claim expenses
  at the **end** of the month of death; surrenders and any 감액 at the **end** of the month,
  **after** deaths, on the surrender value at the month-end `d = t + 1` that closes it; 부활
  **twelve months** after the lapse it follows.
- **Age basis: 보험나이.** 보험나이 (*boheom nai*, insurance age) is the 만 나이 at the
  계약일 with a fraction under six months discarded and six months or more rounded up, and
  it increments on each **계약해당일** rather than on the birthday [S5 제21조] [REG-R25
  제21조](#krlib-reg-r25). A monthly grid anchored at issue steps its 계약해당일 exactly
  twelve months apart, so `⌊t/12⌋` counts them, the ageing is correct by construction, and
  the attained age in month `t` is `x + ⌊t/12⌋` exactly — level through the twelve months of
  a policy year, because interpolating it within the year would be modelling an age the
  contract has no concept of. **The table does
  not share that basis and no conversion is applied [std]:** the statistics
  `mort_table.csv` is calibrated against [REG-R38] are on **만나이**, and no public mapping
  exists. The six-month rule means the two differ for **half of all issue dates**, so the
  model reads the table about half a year of ageing too young — worth roughly 4.6% of `q`
  between attained ages 40 and 60, against a 9.3% step for a full year. Named, not hidden.
- **Currency.** KRW throughout, written ₩ with thousands separators and the Korean
  만원 / 억원 convention alongside where a Korean reader expects it: the anchor's
  ₩100,000,000 is 1억원. `run.py` prints `KRW` and pure ASCII.
- **Model points.** Single-policy, projected on an expected (probability-weighted) basis:
  survivorship multiplies per-policy cash flows. `point_id` parameterizes `Projection` and
  **`point_id = 1` is the worked-example anchor cell.** Ten points ship; no aggregation
  logic is specified here.
- **Termination and horizon.** There is no expiry, no 만기보험금 and no survival benefit at
  any age [S1] [S2] [S4] [S8]. The projection runs to the **terminal age of the mortality
  table**: `T = ω − x + 1` with **ω = 115** for both sexes, the first age at which
  `q(ω) = 1`. `T` is the **number** of policy years projected — the exclusive end of the
  frame, `t = 0 … T − 1` — and ω is itself **[std]**, the 제10회's terminal age being no more
  public than its rates [REG-R33] [REG-R34]. Every remaining life dies in the last period
  `t = T − 1`, nothing is paid there but the death benefit, and **there are no tail states.**
- **Contract boundary.** The premium is level and guaranteed for the whole of 납입기간 with
  no unilateral repricing right on a 금리확정형 contract [S2] [S8], so the whole contract
  sits inside any defensible boundary and no boundary test is implemented. (The question is
  real on this library's **갱신형** products and is specified in [term life
  (정기보험)](../term_life/technical-notes.md), not here.)
- **Rounding.** Intermediate values at full double precision; displayed cash flows and
  surrender values to **two decimal places [std]**, policy counts to six or ten, rates to
  eight or ten — the precision `tests/test_whole_life_kr.py` asserts. Contractual amounts a
  policyholder receives are integral won; the model does not round them, a
  probability-weighted expected value having no contractual denomination.
- **Sign convention.** `net_cf` is **income-positive** — premiums less claims, claim
  expenses, expenses and commission. That is both these notes' sign and the library-wide
  one, so there is **no** outgo-positive `liability_cf` companion: one stream, one sign,
  one name.

---

## Model point attributes

| Attribute | Type | Anchor cell (`point_id = 1`) |
|---|---|---|
| `policy_id` | str | `WL-KR-0001` |
| `sex` | enum {M, F} | M |
| `issue_age` (`x`) | int, **보험나이**, 15–65 | **40** |
| `sum_assured` (`SA`) | KRW, ₩10,000,000–₩1,000,000,000 in ₩1,000,000 units | **100,000,000** (1억원) |
| `prem_term` (`m`) | int years, or **0 for 전기납 (종신납)** | **20** |
| `premium_annual` (`G`) | KRW, level for years 1 … m | **2,776,140** |
| `cv_floor_ratio` (`k`) | 해약환급금 suppression factor, 1.00 / 0.50 / 0.30 / 0.00 | **0.50** — 저해지환급형 |
| `prem_susp_ratio` | the suppressed form's premium as a fraction of the 표준형's | **0.90** |
| `int_basis` | enum {`fixed`, `linked`} — 금리확정형 / 금리연동형 | `fixed` |
| `decl_rate` | 공시이율 on a `linked` point; unused on a `fixed` one | 0.025 |
| `lapse_basis` | enum {`loglinear`, `flat`} — the FSS 원칙모형 or the level comparison | `loglinear` |
| `waiver_rate` | 납입면제 incidence p.a. during 납입기간 | 0.0 |
| `loan_util` / `loan_year` | 보험계약대출 take-up fraction, and the year of the draw | 0.0 / 0 |
| `bonus_rate` | 유지보너스 credited at 납입완료, as a fraction of premiums paid | 0.0 |
| `reduce_year` / `reduce_frac` | 감액 year, and the fraction of `SA` reduced | 0 / 0.0 |
| `reinstate_rate` | 부활 proportion of the previous year's lapses | 0.0 |
| `mort_be_factor` | multiplier on the table rate | 1.0 |

**There is no issue-date attribute**, and that is a product fact rather than an omission:
the projection runs on policy years, 보험나이 is fixed at the 계약일 and increments on the
계약해당일 rather than on the birthday [S5 제21조] [REG-R25 제21조](#krlib-reg-r25), and the one intra-year
date that matters is the 납입완료일, an anniversary by construction.

`prem_term = 0` denotes **전기납 (종신납)**: `m` becomes the whole projection, no 납입완료
date exists, the suppressed period runs for life and **the cliff never happens** —
`cv_mult(d) = k` at every anniversary. That configuration must be in the shipped table because it
is the one in which the product's signature mechanic is absent by construction
(`point_id = 5`).

**The anchor premium is derived from a sourced one, not invented.** DB생명 publishes
₩257,050 a month for the 표준형 at exactly this cell — 남 40세, 1억원, 20년납, 월납 [S4] —
and the annual figure is 12 × that = ₩3,084,600 **[std]**, which is `point_id = 2`. The
anchor's ₩2,776,140 is **0.900 × ₩3,084,600** [std] — a rounding of the **89.9%** ratio
처브라이프 publish at that suppression factor, on their own 5,000만원 / 10년납 cell rather
than this one [S1] — inside the observed 81.5%–95.4% envelope [S1] [S2] [S4] [S6]. No carrier
publishes an annual-mode scale, so the modal discount a real 연납 rate would carry is **not
applied**: the annual premium is slightly overstated and the first year's interest credit
correspondingly understated. Stated, not corrected.

Two attributes need a note. `cv_floor_ratio` is the **suppression factor `k`** and
`refund_ratio(d)` is the **환급률**; the cross-library register retired the bare name
`cv_ratio` because a Korean whole life model carries two ratios on the same object. And
`prem_susp_ratio` is a **price** input, not a value input: it scales the premium, never the
surrender value. The model's own loading rule reproduces the anchor premium to **0.0010%**
— ₩2,776,167.83 against ₩2,776,140 — and the projection uses the model-point value.

---

## State variables

Month quantities are indexed by `t`, month-end quantities by `d`.

| Variable | Description | Updated |
|---|---|---|
| `pols_if(t)` | In-force probability at the **start** of month `t`; `pols_if(0) = 1` | monthly recursion |
| `pols_if_pay(t)` | Of those, the cohort still **paying premium in cash**; the weight on premium and commission | monthly recursion |
| `pols_waived(t)` | Of those, the cohort in the **납입면제** state: in force, paying nothing, accruing value as if paying | monthly recursion |
| `pols_death(t)`, `pols_lapse(t)` | Expected deaths and 해지 in month `t` | decrement |
| `pols_surr(t)` | Of the lapses, those **paid** a surrender value — `pols_lapse(t)` less the 부활 twelve months on | decrement |
| `pols_reinstate(t)` | **부활** at the start of month `t`, from month `t − 12`'s lapses | decrement |
| `mort_rate(t)` | The **annual** 적용위험률 at attained 보험나이 `x + ⌊t/12⌋`, times `mort_be_factor` | table lookup |
| `mort_rate_mth(t)` | Its monthly conversion `1 − (1 − q)^(1/12)`; `1/(12 − t mod 12)` in the terminal year, where `q = 1` | closed form |
| `lapse_rate(t)` | The **annual** 해지율 of the policy year `t` falls in | assumption |
| `lapse_rate_mth(t)` | Its monthly conversion, plus the bonus-date spike in the single month one applies | closed form |
| `waiver_rate(t)`, `waiver_rate_mth(t)` | 납입면제 incidence during 납입기간 only, annual and converted | assumption |
| `pol_val_pp(d)` | `V(d)` — the **계약자적립액**, the 표준형 twin's account at month-end `d` | forward recursion |
| `surr_chg_pp(d)` | `SC(d)` — the **해약공제액**, bounded by the 표준해약공제액 | closed form |
| `cv_std_pp(d)` | `W(d)` — the **표준형 twin's 해약환급금**, `max(0, V − SC)` | closed form |
| `cv_pp(d)` | `CV(d)` — the **해약환급금 actually payable**, after the multiplier and any 유지보너스 | closed form |
| `cv_susp_pp(d)` | `k W(d)` — the suppressed value at **every** `d`, published so the step is visible on both sides | closed form |
| `cum_prem_pp(d)`, `refund_ratio(d)` | Premiums paid by month-end `d`; the **환급률** `CV(d) / cumprem(d)` | recursion / ratio |
| `loan_pp(d)`, `loan_draw(t)` | **보험계약대출** balance at month-end `d`; the draw at the start of month `t` | monthly recursion |
| `sa_factor(d)`, `sum_assured_at(t)` | The 감액 step-down factor at month-end `d`; the sum assured in month `t` | closed form |

Three of these carry design decisions worth stating explicitly.

**There is exactly one policy value in this model.** `pol_val_pp` is the 표준형 twin's
계약자적립액 and the suppression is a multiplier on the surrender value derived from it —
not a second account run, not a second reserve basis. Every carrier that sells the form
names the comparison product in the same sentence and says it is not sold: 「"표준형"의
경우는 … 동일한 보장내용으로 **해지율을 적용하지 않고** … 계산된 상품이며 … 비교안내를
위한 종목으로 **실제로 판매하지 않습니다**」 [S1], with the same sentence at three more
carriers [S2] [S3] [S4]. The published grids confirm it arithmetically: every pre-완납
suppressed/표준형 ratio is exactly `k` (1,164,500 / 2,329,000 = 0.50000 [S1]; 1,526,128 /
5,087,095 = 0.30000 [S4]) and every post-완납 pair is **identical to the won** [S1] [S4]
[S6].

**`pols_waived` is a state, not a rate adjustment.** The waiver's wording forces it:
「그러나 이 경우에도 보험료가 … 정상적으로 납입된 것으로 하여 사망보험금 및 해지환급금을
계산합니다」 [S2], verbatim at two more carriers [S3] [S8]. A waived policy pays nothing and
accrues everything, so it cannot be represented by scaling the premium; and on a suppressed
form it is **the only route to the cliff the policyholder does not have to fund**.

**`pols_reinstate` makes lapse non-terminal**, because the 약관 counts the surrender value
as undrawn 「… 또는 **해지환급금이 없는 경우를 포함**합니다」 [S5 제26조] [REG-R25 제27조](#krlib-reg-r25) —
so **a 무해지 contract is always reinstatable within three years.** Treating every exit as
terminal understates later-duration in force; the parameter exists and is zero in the base
run.

The base run carries **no loan, no waiver, no bonus, no 감액 and no 부활**, so
`loan_pp ≡ 0`, `pols_waived ≡ 0`, `pols_surr ≡ pols_lapse`, `sa_factor ≡ 1` and every
benefit is gross. Each module is exercised on at least one shipped model point.

---

## Assumption inputs

Three classes, kept apart on purpose. The split is not a modelling nicety in Korea: the
**보험가격지수** exists precisely because a Korean consumer cannot see the pricing basis
[REG-R22 제7-45조제7항](#krlib-reg-r22), the 산출방법서 that holds the guaranteed elements is a filed but
**unpublished** 기초서류 [REG-R2], and the November 2024 계리가정 decision draws a hard line
between an assumption an insurer may choose and one the supervisor now sets [REG-R27].

### (a) Contractual / guaranteed elements (cited; the insurer cannot change them)

| Input | Value | Basis |
|---|---|---|
| 사망보험금 | `SA`, **평준형**, level for life, payable on death at any time, net of `L(t)` | [S5 제34조] [S6] [REG-R25 제33조](#krlib-reg-r25) |
| 보험기간 | **종신** — no expiry, no 만기보험금, no survival benefit at any age | [S1] [S2] [S3] [S4] [S6] [S8] |
| Premium `G` | Level and guaranteed for years 1 … m; **none thereafter** | [S2] [S8] |
| Severe-disability benefit | **None.** Korea puts no 고도장해보험금 at the sum assured on this chassis | [S2] [S3] [S6] [S8] |
| 보험료 납입면제 | On a **50% 장해지급률** aggregated across body parts from one cause, accident or disease; premiums cease and are **deemed paid** to the end of 납입기간 for benefit *and* surrender-value purposes | [S2] [S3] [S6] [S8] [REG-R25 부표 3](#krlib-reg-r25) |
| 해약환급금 identity | **계약자적립액 − 해약공제액**, floored at zero — a negative difference 「이를 영(零)으로 처리한다」 | [S2] [S8] [REG-R19 제7-66조제1항제1호](#krlib-reg-r19) |
| 해약공제액 | 미상각신계약비, 「이미 지출한 계약체결비용 해당액으로서 산출방법서에서 정한 방법에 따라 계산한 금액」, **capped at the 표준해약공제액** | [S5 제2조] [S8] [R6] [REG-R19] [REG-R20] |
| 표준해약공제액 | **연납순보험료 × 5% × 해약공제계수 + 보험가입금액 × 10/1000**; for a 보장성보험 the 계수 is the 보험기간 capped at **20**, and the 연납순보험료 is recomputed on a **20년납** footing for a term of 20 years or more | [REG-R20 별표 14 주2·주3](#krlib-reg-r20) |
| 보험가입금액 entering the cap | The 일반사망보험금, taken **before any 체증 or 체감** | [REG-R21 별표 15 제3호·제8호](#krlib-reg-r21) |
| 해약공제기간 | **납입기간 or 신계약비 부가기간, capped at 7년** | [REG-R19 제7-66조제1항제2호](#krlib-reg-r19) |
| Suppression factor `k` | Applies for elapsed duration **< 납입기간**; `k = 1` from 납입완료 | [S1] [S4] [S6] [S7] [S8] |
| What `k` multiplies | The **표준형 twin's** 해약환급금 — a non-marketed comparison product with identical benefits priced **with the lapse assumption switched off** | [S1] [S2] [S3] [S4] |
| Post-cliff equality | From 납입완료 the suppressed and 표준형 values are **identical** in every published grid | [S1] [S4] [S6] |
| Clawback | Where premiums falling in the suppressed period were unpaid, they must be made good before the post-cliff basis applies | [S2] [S3] [S8] |
| Waived premiums | Count as **paid** for the surrender-value computation | [S2] [S3] [S6] [S8] |
| 보험계약대출 limit | Within the 해약환급금 net of existing principal and interest, 「그러나, 순수보장성보험 등 보험상품의 종류에 따라 보험계약대출이 제한될 수 있습니다」 | [S5 제34조] [REG-R25 제33조](#krlib-reg-r25) |
| Loan settlement | Deducted from any benefit, from the 해약환급금, and **즉시** on 해지 | [S5 제34조] [REG-R25 제26조·제33조](#krlib-reg-r25) |
| 감액 | The reduced portion is **treated as surrendered** and pays the corresponding 해약환급금 | [S5 제20조] [REG-R25] |
| 납입최고(독촉)기간 | **14일 이상** from the day after the 계약해당일; the contract is 해지 the day after it ends | [S5 제25조] [REG-R25 제26조](#krlib-reg-r25) |
| 부활 | Within **3년** of 해지, on fresh 고지 and arrears with interest; available **even where the 해약환급금 was nil** | [S5 제26조] [REG-R25 제27조](#krlib-reg-r25) |
| 면책 — suicide | No death benefit where the insured takes their own life within **2년** of the 계약일; zero incidence modelled | [S1] [S3] [S6] [S7]; [REG-R49 제659조](#krlib-reg-r49) [REG-R50 제732조의2](#krlib-reg-r50) |
| Refused claim | The insurer must still pay 「보험수익자를 위하여 적립한 금액」 — in practice the 계약자적립액 | [REG-R50 제736조](#krlib-reg-r50) [REG-R25 제22조](#krlib-reg-r25) |
| Minimum death benefit | At least cumulative premiums paid, except where the 납입기간 ends at age 80 or below — which the anchor (완납 at 보험나이 60) satisfies | [REG-R16 제7-60조제9호](#krlib-reg-r16) |

**The suppression is a regulatory dispensation, not a contractual gimmick**, and the
condition attached to it is what makes the lapse vector a first-class model input.
제7-66조제4항 permits an insurer to pay **less than** the 제1항 value that 별표 14 floors
only where the premium or benefit was computed 「**최적해지율**을 사용하여」 — using a
best-estimate lapse rate [REG-R19]. 제4항제1호 bars the form outright for a 변액보험 (so
`VA_KR_S` may not use it), and 제4항제2호 attaches two further conditions **only where** the
surrender value during 납입기간 is **less than 50%** of an otherwise identical 표준형
product's [REG-R19]. **The anchor sits exactly at that threshold and not below it**, which
is the most likely reason three independent carriers chose 50% [S1] [S6] [S7].

### (b) Insurer-discretionary current elements

Unlike a UK guaranteed-premium term policy, this class is not nearly empty — it is where
the product's economics live. Korea differs from Japan in one respect that matters
throughout: **the pricing rate is published**, in the 상품요약서, and so is a sample of the
적용위험률 and the 적용해지율 envelope [S2] [S8]. What is *not* published is the
산출방법서 itself, so a disclosure of a parameter is what this library has, never the
filing [REG-R2].

| Input | Model value | Basis |
|---|---|---|
| 예정이율 `i` (`prem_int_rate`) | **2.50% p.a., 연복리, flat** | Disclosed range 2.25%–2.75% at six carrier documents [S1] [S2] [S5] [S6] [S7] [S8]; centre **[std]**, and equal to the 2026 평균공시이율 [REG-R48] |
| 최저보증이율 (`min_guar_rate`) | **0.75% p.a.**, floor on a `linked` point | Stated verbatim in the one full 약관: 「최저보증이율은 연복리 0.75%를 적용」 [S5 제32조] |
| 공시이율 (`decl_rate`) | **2.75%** on the one `linked` model point, held flat | Mechanism sourced [S5 제32조] [REG-R18 제7-65조제3항](#krlib-reg-r18) [REG-R24 별표 27](#krlib-reg-r24); the level **[std]** |
| Accrual rate `i_acc` (`acc_int_rate`) | `i` on a 금리확정형 point; `max(공시이율, 최저보증이율)` on a 금리연동형 one | [REG-R16 제7-60조제10호](#krlib-reg-r16) [REG-R18] |
| 보험계약대출이율 `i_L` | **예정이율 + 1.5% = 4.00% p.a.**, compound, flat, and a **vintage** rate | Formula at three carriers independently [S9] [S11] [S13]; level **[std]** |
| 보험계약대출 limit | **80%** of the *payable* 해약환급금 | Observed 50%–85% [S11] and 50%–80% [S13]; pick **[std]** |
| Gross-to-net loading `θ` (`prem_loading`) | **1.4642** | **[std]**, calibrated once so the 표준형 anchor reproduces 12 × ₩257,050 [S4] |
| Acquisition-cost ratio `a` (`acq_cost_ratio`) | **1.00** — 계약체결비용 set **at** the 표준해약공제액 | **[std]**, bounded by the 1.4 × tolerance of 제7-45조제11항 [REG-R22] |
| First-year commission share `c₀` (`comm_init_share`) | **0.65** of 계약체결비용, capped at one year's premium | Cap sourced [REG-R22 제4-32조제5항](#krlib-reg-r22); share **[std]** |
| Renewal commission `c_r` | **3.0%** of premium, years 2 … m | **[std]** |
| 계약관리비용 per policy `e` | **₩5,000 a month** for life, inflating at 2.0% on each 계약해당일 | **[std]** |
| 유지관련비용 on premium | **2.0%** of premium collected | **[std]** |
| Claim handling expense `ec` | **₩300,000** per death claim | **[std]** |
| Expense inflation | **2.0% p.a.**, the Bank of Korea target | **[std]** |
| 유지보너스 | **13.8%** of total premiums at 납입완료 on the one 7년납 point | Published 10.8% / 13.8% / 15.0% by 납입기간 [S7]; off in the base run |
| 계약자배당 | **None.** The composite is 무배당, as is every product in the retrieved set | [S2] [S8] [R8]; frame not implemented [REG-R12] |

**Why the expense parameters are all [std], and what bounds them.** Both 상품요약서 in the
set define 계약체결비용 and 계약관리비용 in words and then give **no number** [S2] [S8];
the 약관 defines 부가보험료 and 해약공제액 by reference to the 산출방법서 [S5 제2조]
[REG-R2]. **No Korean expense rate as a percentage of premium was obtained from any source
in this research pass.** Four public handles bound the standardization instead, and the
model is built to sit inside all four:

1. **The 표준해약공제액 itself** [REG-R20]. The model sets 계약체결비용 exactly at it —
   `acq_cost_ratio = 1.00` — so the acquisition cost is by construction recoverable within
   the statutory surrender charge and no more.
2. **The 1.4 × disclosure tolerance** of 제7-45조제11항, under which a whole-life
   death-benefit 보장성보험 need not publish a 계약체결비용지수 provided its 계약체결비용
   stays within 1.4 × the 표준해약공제액 [REG-R22]. On the anchor that outer bound is
   ₩4,349,380.75 and the model sits at ₩3,106,700.54, comfortably inside it.
   `check_acq_cost_cap()` asserts it.
3. **The first-year remuneration cap** of 제4-32조제5항: first-year distributor remuneration
   may not exceed the first year's expected premium, with the projected one-year surrender
   value added to the commission side where the contract deducts 80% or more of the
   표준해약공제액 — which is exactly what a 무·저해지 design does [REG-R22] [REG-R29]. The
   model caps `comm_init_pp()` at `1.00 × premium_pp()` and the same check asserts it. On
   the anchor the cap does **not** bind: 0.65 × ₩3,106,700.54 = ₩2,019,355.35 against a
   premium of ₩2,776,140.
4. **The 보험가격지수**, whose observed range of **85.4%–110.9%** across two carriers at
   this very cell bounds how far a Korean whole-life product's total loading can sit from
   the industry mean [S2] [S8].

The 60%-a-year instalment structure of 제4-32조제8항 [REG-R22] [REG-R29] governs how the
cost is *paid* rather than how much it is; it is cited and not modelled.

### (c) Behavioral / experience assumptions (modeler's view — all [std])

**Mortality.** The 제10회 경험생명표 (*gyeongheom saengmyeongpyo*), produced by 보험개발원
and applied to new business from **2024-04**, is **not published in full**: only 평균수명
and 기대여명 are released, and even those reached this library through a trade newspaper
[REG-R33] [REG-R34]. The 참조순보험요율 the bureau files for life mortality are likewise
never published, becoming visible only as the 보험가격지수 [REG-R4] [REG-R22]. **There is
therefore no published Korean insured mortality rate to anchor a proxy on** — the sharp
contrast with `jplib`, where the 生保標準生命表 is free to read and only its redistribution
is restricted.

`mort_table.csv` is accordingly a **[std] construction** and its `provenance` column says
so row by row. Three kinds of row:

| Row kind | Construction | Basis |
|---|---|---|
| **ANCHOR** (보험나이 20, 40, 60) | The **mean** of the only two Korean insured rates in the public domain at those ages | Rates sourced [S2] [S8]; the mean **[std]** |
| **CONSTRUCTED** below 60 | Log-linear in `ln q` between anchors | **[std]** |
| **CONSTRUCTED** above 60 | Gompertz in `ln q` with a quadratic deceleration, two parameters solved so 65세 기대여명 is **23.7 (M) / 27.1 (F)** and `q(115) = 1` | Targets from [REG-R38] plus the reported 제10회 gap [REG-R33]; the form **[std]** |
| **TERMINAL** | `q = 1` at **ω = 115** | **[std]**; the 제10회 terminal age is not public |

Two unfitted checks are worth recording because neither was used in the calibration: the
resulting **평균수명 at birth is 85.4 (M) / 90.4 (F)** against the 86.3 / 90.7 reported for
the 제10회 [REG-R33]. **No row of this file is a 경험생명표 value and the table must never
be presented as one.**

| Input | Value | Basis |
|---|---|---|
| Base table | `mort_table.csv`, sex-distinct, `q` at attained 보험나이 `x + t` | **[std]** on [S2] [S8] [REG-R33] [REG-R38] |
| `mort_be_factor` | **1.00** in the base run | **[std]** |
| Terminal age ω | **115**, both sexes | **[std]** |
| Improvement overlay | None | **[std]** |
| 만나이 → 보험나이 conversion | **None applied** | **[std]**; no public mapping exists |

`mort_be_factor = 1.00` is a choice, not a default: **the base run is a pricing-table run,
not a best estimate.** The two disclosed grids differ by **up to 24%** — 18%–24% at five of
the six published cells (남 40세 0.000780 [S2] against 0.00092 [S8], 여 60세 0.001730
against 0.00214) and not at all at 여 20세, where both print 0.00018 — so they **bracket**
rather than fix a level, and one is labelled 「무배당 **예정 경험**사망률」, the
giveaway that it is a 경험생명표 derivative carrying a 무배당 loading rather than the table
[S2] [S8]. A production basis would sit below 1.00 and move claims proportionately;
`point_id = 10` runs at 0.90 so the lever is exercised.

**Lapse — and this is the assumption the whole product turns on.** Two independent public
bases exist in Korea, they are disclosed, and they do not agree.

The **pricing basis is published in the 상품요약서**, which has no counterpart anywhere else
in this repository. One carrier: 「「…(해지환급금 일부지급형)」에 적용한 해지율은
**1%~10%**이며, **일반형에는 적용해지율이 적용되지 않습니다**」 [S2]. Another: 「적용해약률은
… 보험료 납입기간 중 **연 0%~연 13.4%**를 적용합니다. 보험료 납입기간 이후에는 **연
1.0%~연 11.3%**의 해약률을 적용합니다」 [S8]. Neither publishes the *shape*, only the
envelope.

The **valuation basis was set by the supervisor in November 2024** and it is far lower. The
problem the FSS named: with no experience on 무·저해지 business, insurers assumed high lapse
right up to 완납 on contracts where lapsing pays nothing, booking CSM that would never be
realised and pricing low enough to tilt the market toward the form [REG-R27] [R3]. The
remedy: among models converging to zero at 완납 the **로그-선형 (log-linear) 모형** is the
**원칙모형**, with a convergence point of **0.1% at 납입완료**, an ultimate rate of **0.8%**
after it, permission to depart only against audited disclosure of the difference in CSM,
BEL, K-ICS ratio and net income, and an **additional lapse of at least 30%** at a 단기납
bonus date [REG-R27] [R3] [R7].

`lapse_table.csv` therefore ships **both**, as three parameters each rather than a rate per
policy year — the convergence point is 납입완료, which is a model point attribute:

| `lapse_basis` | `first_year_rate` | `completion_rate` | `ultimate_rate` | Basis |
|---|---|---|---|---|
| `loglinear` | 0.10 | 0.001 | 0.008 | Endpoints [REG-R27] [R3] and the top of the disclosed 1%~10% envelope [S2]; the interpolation **[std]** |
| `flat` | 0.04 | 0.04 | 0.04 | **[std]** level comparison basis, inside both disclosed envelopes [S2] [S8] |

Writing `y = t // 12 + 1` for the contractual policy year of month `t`, the **annual** rate is

    w(t) = w1 * (wm / w1) ^ ((y - 1) / (m - 1))      for 1 <= y <= m
    w(t) = wu                                        for y > m

and the monthly grid applies its uniform-force conversion

    w^m(t) = 1 - (1 - w(t)) ^ (1/12)

so that the twelve months of a policy year compound back to exactly that year's `w(t)`.
On the anchor that is `w(0) = 0.10` exactly, `w(228) = 0.001` exactly in the policy year
납입완료 falls in, and a flat 0.008 from `t = 240`; the corresponding monthly rates are
0.0087416, 0.0000834 and 0.0006691. **Dividing by twelve instead would be wrong here in a way
it rarely is**: across a vector spanning two orders of magnitude the two conventions disagree
by 4.9% of the rate in the first year alone, and only the compounding one reproduces the
supervisor's tabulated annual figure. **The 표준형 twin is priced with no lapse assumption at
all** [S1], which is why the `flat` basis is level rather than shaped: it is a comparison, not
a second estimate.

**Everything else in class (c).**

| Input | Base value | Note |
|---|---|---|
| 납입면제 incidence `u(t)` | **0** in the base run; **0.4% p.a.** during 납입기간 on `point_id = 7` | **[std]**. No Korean 장해 incidence at the 50% 장해지급률 threshold was retrieved |
| 보험계약대출 take-up | **0**; a single draw of 100% of the contractual room at `loan_year` on points 3 and 6 | **[std]**. No Korean take-up data is public |
| Loan repayment | **None modelled** | **[std]**. Repayment is free of fee at every carrier that states one [S11] [S13], so a real book repays; the model does not |
| 부활 rate | **0**; **20%** of the lapses of twelve months earlier on `point_id = 10` | **[std]** |
| 감액 | **Off**; 50% of `SA` at duration 15 on `point_id = 10` | **[std]** |
| 자동대출납입 (APL), 감액완납, 연장정기보험 | **Not modelled, because none was found in any retrieved Korean document** | [unverified] [S5] — see below |
| 청약철회, 품질보증해지, 위법계약해지권; 우량체 / 건강등급 discounts, 선납, 중도인출, 추가납입 | Out of scope; the projection starts from cover in force, and each is named in `product-spec.md` | **[std]** [REG-R25] [REG-R51] |

**The single sharpest Korea/Japan difference, and it is a negative finding.** `jplib`'s
whole life chassis turns on the 自動振替貸付, which advances the premium against the
surrender value at the end of grace, so lapse there is a **funded** event. **No 자동대출납입
provision was found in any Korean document retrieved for this library.** The 생명보험
표준약관 is understood to contain such an article, but the retrieved 별표 15 extract does not
carry it [REG-R25], and the one full Korean 약관 in the set handles non-payment through a
월대체보험료 deduction from the account — a 유니버셜 mechanic, not an APL [S5 제24조].
`WholeLife_KR_S` therefore models lapse as a **behavioural decrement at the end of a 14-day
납입최고기간**, and the absence is tagged **[unverified]**: the highest-value single item for
the next research pass, because a 표준약관 article found later would change this chassis
**in kind**. The consumer consequence runs the opposite way to Japan's — in Korea there is
no buffer at all, and a 무해지 policyholder who misses fourteen days receives **nothing**,
which is the finding behind the FSS's 2019 소비자경보 [R4] [REG-R28].

---

## Cash flow components and recursions

### Notation

Defined once, used throughout, and identical to `product-spec.md`'s. The
`Projection` docstring carries the same table mapping every symbol to its cells name.

| Symbol | Meaning | Cells |
|---|---|---|
| `t` | the 0-based **month** index, `t = 0 … T − 1`; month `t` is in policy year `⌊t/12⌋ + 1` and runs from month-end `t` to month-end `t + 1`; the attained 보험나이 in it is `x + ⌊t/12⌋` | `age(t)`, `policy_year(t)` |
| `d` | the month-end, `d = 0 … T`, `d = 0` at issue; month `t` opens at `d = t` and closes at `d = t + 1`; a 계약해당일 is `d = 12y` | (the value cells' argument) |
| `x`, `T_y`, `T`, `ω` | 가입나이 (보험나이); policy years projected, `T_y = ω − x + 1`; **months** projected, `T = 12 T_y`; table terminal age | `age_at_entry()`, `proj_years()`, `proj_len()`, `omega_age()` |
| `m`, `12m` | 납입기간 in policy years, a 1-based count, `m = T_y` on a 전기납 contract; the same in months | `prem_period()`, `prem_end()`, `prem_period_mths()` |
| `n_sc`, `12 n_sc` | 해약공제기간 `= min(m, 7)` years; the same in months | `surr_chg_period()`, `surr_chg_period_mths()` |
| `SA`, `SA(t)` | 보험가입금액 at issue, and in month `t` after any 감액 | `sum_assured()`, `sum_assured_at(t)` |
| `G`, `G^m` | annual 영업보험료 (a report and the commission base); the **monthly** premium, the month's income, level for `t < 12m` | `premium_pp()`, `premium_mth_pp()`, `premium_mth_at_pp(t)` |
| `P`, `P^m`, `P₂₀` | 연납순보험료 over `m`, the 별표 14 quantity; the **월납순보험료** the account consumes; the annual premium on the 별표 14 **20년납** footing | `prem_net_level_pp()`, `prem_net_level_mth_pp()`, `prem_net_20yr_pp()` |
| `i`, `j`, `i_acc`, `j_acc`, `i_L`, `j_L` | 예정이율 and its monthly equivalent; the account accrual rate and its monthly equivalent; 보험계약대출이율 `= i_acc + 1.5%` and its monthly equivalent | `prem_int_rate`, `prem_int_rate_mth()`, `acc_int_rate()`, `acc_int_rate_mth()`, `loan_int_rate()`, `loan_int_rate_mth()` |
| `q(t)`, `w(t)`, `u(t)` | the **annual** 적용위험률, 해지율 and 납입면제 incidence of the policy year month `t` falls in | `mort_rate(t)`, `lapse_rate(t)`, `waiver_rate(t)` |
| `q^m(t)`, `w^m(t)`, `u^m(t)` | their monthly conversions `1 − (1 − q)^(1/12)` **[std]** — what the roll-forward applies | `mort_rate_mth(t)`, `lapse_rate_mth(t)`, `waiver_rate_mth(t)` |
| `A(y)`, `ä(y, n)` | whole-life EPV of 1 at 보험나이 `y`; `n`-year annuity-due, both on `i` and the table | `epv_death(y)`, `annuity_due(y, n)` |
| `A^m(u)`, `ä^m(u, n)` | their **monthly** counterparts, indexed by months from issue and payable monthly, on `j` and the converted table rates | `epv_death_mth(u)`, `annuity_due_mth(u, n)` |
| `l(t)`, `lp(t)`, `lw(t)` | in force at the start of month `t`; of those, paying; of those, waived | `pols_if(t)`, `pols_if_pay(t)`, `pols_waived(t)` |
| `D(t)`, `S(t)`, `Sp(t)`, `R(t)` | deaths; 해지; 해지 **paid** a value; 부활 | `pols_death(t)`, `pols_lapse(t)`, `pols_surr(t)`, `pols_reinstate(t)` |
| `V(d)` | 계약자적립액 at month-end `d` | `pol_val_pp(d)` |
| `SC(d)`, `SC*` | 해약공제액 at `d`; the **표준해약공제액** cap | `surr_chg_pp(d)`, `surr_chg_cap_pp()` |
| `W(d)` | 표준형 twin's 해약환급금, `max(0, V(d) − SC(d))` | `cv_std_pp(d)` |
| `k`, `κ(d)` | suppression factor; the multiplier actually applied at month-end `d` | `cv_floor_ratio()`, `cv_mult(d)` |
| `CV(d)` | 해약환급금 payable at `d` | `cv_pp(d)` |
| `B(d)` | 유지보너스 credited at 납입완료 | `bonus_pp(d)` |
| `cumprem(d)`, `ρ(d)` | premiums paid by month-end `d`; **환급률** `CV(d) / cumprem(d)` | `cum_prem_pp(d)`, `refund_ratio(d)` |
| `L(d)`, `Δ(t)` | 보험계약대출 balance at month-end `d`; the draw at the start of month `t` | `loan_pp(d)`, `loan_draw(t)` |
| `AC`, `c₀`, `c_r`, `e`, `ec`, `π` | 계약체결비용; first-year commission share; renewal rate; per-policy 계약관리비용; claim expense; expense inflation | `acq_cost_pp()`, `comm_init_share`, `comm_renewal_rate`, `expense_maint_pp`, `expense_claim_pp`, `inflation_rate` |
| `CF(t)` | net cash flow of month `t`, **income-positive** | `net_cf(t)` |

**Dimensional check.** `q`, `q^m`, `w`, `w^m`, `u`, `u^m`, `k`, `κ`, `ρ`, `c₀`, `c_r`, `l`,
`lp`, `lw` and the `sa_factor` are dimensionless; `i`, `i_acc`, `i_L`, `π` are per annum and
`j`, `j_acc`, `j_L` are their per-month equivalents; `A` and `ä` are pure numbers, the annual
pair in years of premium and the monthly pair `A^m`, `ä^m` in months of it, so `SA × A / ä`
is ₩ per year and `SA × A^m / ä^m` is ₩ per **month**; `SA`, `G`, `G^m`, `P`, `P^m`, `V`,
`SC`, `W`, `CV`, `B`, `L`, `AC`, `e`, `ec` are ₩; every term of `CF(t)` is ₩ per policy
issued per **month**. The annual rates are **probabilities** and are converted by compounding,
never by dividing — the sister model `LTC_KR_S` divides its transition intensities by twelve
for the opposite reason, those being rates per year and not probabilities. No term mixes a
per-annum rate with a stock without an explicit period count.

### The net premium, and the two annuities that are not the same

The 표준형 twin's net level premium is fixed at issue by equivalence over the 납입기간, on
the 예정이율 and the 적용위험률:

    P × ä(x, m) = SA × A(x)          =>      P = SA * A(x) / ä(x, m)

with `A` and `ä` evaluated end-year and premium-in-advance respectively:

    A(y)      = v * ( q(y) + (1 - q(y)) * A(y + 1) ),     A(y) = 0 for y > omega
    ä(y, n)   = 1 + v * (1 - q(y)) * ä(y + 1, n - 1),     ä(y, 0) = 0
    v         = 1 / (1 + i)

**A second annuity is required and it is not the same object.** 별표 14 note 3 says the
연납순보험료 entering the 표준해약공제액 is recomputed on a **20년납** footing where the
보험기간 is 20 years or more — which for a 종신 contract it always is [REG-R20]. So

    P     = SA * A(x) / ä(x, m)             the pricing net premium, over m years
    P20   = SA * A(x) / ä(x, 20)            the 별표 14 net premium, over 20 years

and `P₂₀ = P` **only when `m = 20`**, which is the anchor's case and is exactly why the
anchor was chosen. On the 7년납 point they differ substantially, and a model that reuses `P`
in the cap formula overstates the statutory surrender charge on every short-pay design.
`prem_net_20yr_pp()` exists as a separate cells for that reason alone.

**The gross premium is an input, not an output.** `G` comes from the model point, sourced
[S4]; the model also carries its own loading rule, `prem_gross_calc_pp() = θ × P ×
prem_susp_ratio` with `θ = 1.4642` **[std]**, calibrated once against the 표준형 anchor and
reported in the worked example. **The projection uses the model-point value.** A loading
that reproduces a sourced premium to five significant figures is a documented fit, not a
pricing model, and is not allowed to drive cash flows.

### 계약자적립액 — the account recursion this chassis defines

The 표준형 twin's account is the classical net-level recursion on the **monthly** grid, with
the death benefit falling at the **end** of the month:

    V(0)                 = 0
    V(d) * (1 - q^m(d-1)) = ( V(d-1) + P^m * 1{d <= 12m} ) * (1 + j_acc) - q^m(d-1) * SA
    V(T)                := 0

on the **month-end** index `d`, solved forward; `q^m(d-1)` is the monthly conversion of the
table rate at attained age `x + ⌊(d−1)/12⌋`, the rate of the policy year the month just ended
falls in, and `j_acc = (1 + i_acc)^(1/12) − 1`. Rearranged as the model computes it,

    V(d) = ( ( V(d-1) + P^m * 1{d <= 12m} ) * (1 + j_acc) - q^m * SA ) / (1 - q^m)

Read as a roll over month `t` — the form `check_pol_val_roll_fwd_resid(t)` asserts — the
same statement is

    ( V(t) + P^m * 1{t < 12m} ) * (1 + j_acc) = q^m(t) * SA + (1 - q^m(t)) * V(t+1)

**This is the step 감독규정 제7-66조제1항제4호 names.** The rule requires the account to accrue
**monthly** until 납입완료 and daily after it; the annual-step model this replaced needed
제7-65조제2항's separate permission to carry a monthly-premium product's account on an annual
one — 「연납보험료를 기준으로 하여 산출할 수 있다」 [REG-R18] — and the monthly grid does not.
The account is **1.2% higher at every 계약해당일** in consequence, which is twelve instalments
earning interest from the month each is paid rather than one notional annual premium earning
it from the start of the year. Only the daily accrual after 납입완료 remains a **[std]**
approximation [REG-R19].

**`P` and `P^m` are different numbers and both are needed.** 별표 14 writes the
표준해약공제액 in terms of the **연납순보험료**, so `prem_net_level_pp()` stays annual and the
surrender charge is untouched by the conversion; the account consumes
`prem_net_level_mth_pp()`, solved from `P^m · ä^m(0, 12m) = SA · A^m(0)` on the monthly
counterparts of the same EPVs. `12 P^m` is **2.4% above** `P`, which is the ordinary modal
loading of paying monthly in advance, and confusing the two would silently move both the
account and the statutory cap.

Three further properties are contractual rather than conventional and a model must not lose
them.

**It is net level premium.** The acquisition cost is **not** Zillmerised into the account;
it is deducted **from** it, and the deduction is what 별표 14 caps [REG-R20]. The
consequence is visible in the worked example's first row: `V(1)` is ₩173,073.54 while
`SC(1)` is ₩3,069,716.01, so `W(1) = max(0, V − SC) = 0` and the surrender value is nil for
the first fifteen months — which is what every published Korean grid shows at duration 1
[S1] [S4] [S6] [S8], and the monthly grid dates the crossing to `d = 15` rather than leaving
it somewhere inside policy year 2.

**It runs on the 표준형 net premium**, not on the sold form's lower one. `CV(d)` is
therefore **independent of the sold form's own premium**, and that single fact is the whole
of the 환급률 arithmetic that sells the product: the suppressed form's post-완납 surrender
value is identical to the 표준형's while its premiums are lower, so its refund ratio is
mechanically higher. Nothing is credited that the 표준형 does not get; the **denominator is
smaller**.

**It is bounded below by nothing.** The account may be smaller than the surrender charge, in
which case the 해약환급금 is zero and never negative [REG-R19 제7-66조제1항제1호](#krlib-reg-r19).

Two identities are asserted rather than assumed. `check_pol_val_roll_fwd()` re-derives the
recursion residual over every month. `check_pol_val_prosp()` compares the forward account
against its **prospective** form at every month-end,

    prosp_val_pp(d) = SA * A^m_acc(d) - P^m * ä^m_acc(d, max(12m - d, 0))

on the accrual rate, and asserts equality to `val_tol × SA`. Its tolerance carries a factor of
**twelve** and nothing else: in the terminal policy year `q = 1`, the recursion divides by
`1 − q^m` twelve times over, and whatever float noise the account carries into that year is
multiplied by exactly that. Every month-end before it closes to a hundredth of a won, and the
largest residual over the anchor's 912 months is ₩0.73 on a ₩100,000,000 sum assured.
**It is defined as zero on a
금리연동형 point**, and that is not a dodge: once the crediting rate can differ from the
pricing rate the account is genuinely path-dependent and the retrospective and prospective
forms are different numbers. On `point_id = 9` — 여 45세, 금리연동형 at 2.75% against a
2.50% pricing rate — the forward account at `d = 240` runs **9.12% above** its prospective
form (₩54,077,741.85 against ₩49,559,710.78). A model that asserts the identity
unconditionally will fail there and, worse, may be "fixed" by discounting the account on the
wrong rate.

**The 금리연동형 variant, and why the crediting rate is a slow scalar.** 공시이율 =
공시기준이율 ± 조정률, the 공시기준이율 being
`외부지표금리 × α + 운용자산이익률 × (1 − α)` on a three-month weighted moving average with
**α capped at 60%**, uniform across a product class of which 보장성보험(종신보험) is one, and
floored by a mandatory 최저보증이율 [REG-R18] [REG-R24 별표 27](#krlib-reg-r24) [REG-R23] [REG-R16]. The α
cap is the modelling point: a Korean declared rate is majority-weighted to the insurer's
**own realised** 운용자산이익률, not to market yields, which is why `decl_rate` is a
slow-moving [std] scalar and not a function of a yield curve.

### 해약공제 and the 표준해약공제액 cap

별표 14 states the cap in one line [REG-R20]:

    표준해약공제액 = 연납순보험료 × 5% × 해약공제계수 + 보장성보험의 보험가입금액 × 10/1000

For a 보장성보험 the 해약공제계수 is the **보험기간 capped at 20 years** [REG-R20 주2](#krlib-reg-r20), and
a 종신 contract's 보험기간 always exceeds 20, so the coefficient is 20 and 5% × 20 = 1.0.
For this product the formula therefore collapses to **one year's net premium plus one per
cent of the sum assured**:

    SC*  =  0.05 * 20 * P20  +  0.01 * SA  =  P20 + 0.01 * SA

with `SA` taken as the 일반사망보험금 **before any 체증 or 체감** [REG-R21 별표 15 제3호,
제8호](#krlib-reg-r21). The *level* of the charge is set at the cap **[std]**, and only its *shape between
the ends* is standardized — a straight line to `n_sc`:

    SC(d) = SC* * max(0, 1 - d / (12 * n_sc)) * sa_factor(d),   n_sc = min(m, 7) years

with `d` the month-end, so `SC(0) = SC*` at issue and `SC(12 n_sc) = 0`. The monthly grid
runs the line off in 84 steps rather than seven on a 20년납 contract, which puts the balance
at the month a surrender is actually taken instead of at the last 계약해당일 before it.

**The duration is fixed by regulation and it is short.** 제7-66조제1항제2호: 「해약공제기간은
보험료 납입기간 또는 신계약비 부가기간으로 하되 … **7년 이상일 때에는 7년으로** 한다」
[REG-R19]. On the anchor's 20년납 contract the charge is fully amortised by the month-end
`d = 84` — **thirteen years before the cliff.** That separation is the single most important
structural fact in this section, because it means the step at 납입완료 has nothing whatever to
do with the surrender charge running off: by then it has been gone for over a decade.
`check_surr_chg_cap()` asserts both limbs — never above `SC*`, and exactly zero from
`12 n_sc`.

That is the honest position on the three components: the **cap is sourced and exact**, the
**level is set at the cap** and defended by the four public bounds in class (b), and only
the **shape between the ends** is [std].

### 해약환급금 and the 무해지 / 저해지 cliff

    W(d)  = max( 0, V(d) - SC(d) )                          the 표준형 twin's value
    kappa(d) = k    for d <   12m   (and for all d on a 전기납 contract)
    kappa(d) = 1    for d >= 12m
    CV(d) = kappa(d) * W(d) + B(d)                          the payable value
    CVs(d) = k * W(d)                                       the suppressed value at every d

on the month-end index, and the transition at `d = 12m` is a **step, not a
ramp**. `CV(12m) / (k W(12m))` is exactly `1 / k` and **anything between is an interpolation
the contract does not have.** Both quantities exist at `d = 12m` and the model publishes both,
`cv_pp` and `cv_susp_pp`, side by side in `result_val()` so the step can be read off one row
rather than inferred — the row of month `12m − 1`, whose closing month-end that is. **The
monthly grid is what makes the claim checkable**: the two month-ends either side of the cliff
are one month apart, so a doubling between them is visibly a single-row event rather than an
artefact of comparing two balances a year apart.

**[std] ordering rule.** A surrender occurring in the last paying month — `t = 12m − 1` — is
paid at the end of it on `CV(12m)`, the **full** value. The suppressed value applies to the
month-ends `d = 1 … 12m − 1`. This
is a convention and it is stated because it is worth real money: on the
anchor the difference between the two readings of that one month is a factor of two on
₩52,023,973.59.

`check_cv_cliff()` asserts three things: that `CV(d) − B(d) = κ(d) W(d)` at every month-end,
that the payable value net of any bonus **never exceeds the 표준형 twin's**, and that at
`d = 12m` they are **equal**. It deliberately does **not** assert the FSC press-release framing 「전(全)
보험기간 동안 표준형 보험의 환급률(기납입보험료대비) 이내로」 [REG-R28], because the
denominators differ and the two statements can disagree: on `point_id = 3` the 무해지 form's
post-완납 환급률 is **1.081135** against the 표준형's 0.843286, which satisfies
제7-66조제4항제2호 나목 as recorded in the 고시 [REG-R19] and contradicts the press-release
reading. `product-spec.md` records both statements as they stand and so does this document;
neither resolves them, because the operative article text and the press-release sentence
were retrieved from different documents and no third document reconciles them.

**Everything derived from the surrender value is suppressed with it.** The 보험계약대출
limit and the 감액 proceeds are computed off `CV(d)`, so during 납입기간 both are `k` times
their 표준형 size — and on a **무해지** contract the policy loan **does not exist at all**,
which the FSS said in terms in its 2019 alert and the 표준약관 repeats as 「순수보장성보험 등
보험상품의 종류에 따라 보험계약대출이 제한될 수도 있습니다」 [R4] [REG-R28] [REG-R25 제33조](#krlib-reg-r25)
— the one full 약관 in the set carries the same sentence without 도 [S5 제34조].
`point_id = 3` is that case and draws **exactly nothing**.

### 유지보너스, and the lapse spike that is not optional

On a 단기납 design the insurer credits a persistency bonus to the 계약자적립액 at 납입완료:
**10.8% (5년납) / 13.8% (7년납) / 15.0% (10·15년납)** of total 주보험 premiums, with a
second 18.5% credit at duration 10 on the 5·7년납 forms [S7]. The model carries the first
credit only, and **as an addition to the payable surrender value from the month-end
`d ≥ 12m`** rather than as a credit inside the account recursion **[std]**, no crediting
formula being published:

    B(d) = bonus_rate * cumprem(12m)   for d >= 12m on a term-pay contract,  else 0

**The supervisor requires an additional lapse of at least 30% at any such bonus date**, or a
rate backed out of the 표준형 product's cumulative persistency, calibrated against the
29.4%–30.2% eleventh-year lapse observed on single-premium bancassurance savings [REG-R27]
[R3]. `lapse_spike()` therefore turns on **with** the bonus and cannot be switched on
separately: on `point_id = 8` the monthly lapse rate of the single month the bonus is credited
in — `t = 83`, the last month of the 7년납 period — is **0.300083** against a converted base of
0.000083.
**The spike is the one decrement that is not converted to a monthly force, and deliberately.**
It is a lump of elective exits on a date, not a rate spread over a year: the supervisor's
「30% 이상」 is an additional *lapse*, and spreading it over twelve months would both delay it
and, through the compounding, change its size. So it is added to that one month's converted
base rate and to no other — the same treatment the sister model `Term_KR_S` gives its renewal
decline, and the opposite of what `LTC_KR_S` does with its transition intensities, which are
rates per year and are divided by twelve.
Turning the bonus on without the spike would misstate the liability in the insurer's favour,
which is exactly what the guidance exists to prevent.

### 보험계약대출 as a modelled state

    L(0)     = 0
    L(t+1)   = ( L(t) + Delta(t) ) * (1 + j_L)
    Delta(t) = util * max( 0, 0.80 * CV(t) - L(t) )   in month t = 12 * (loan_year - 1), else 0

`L` is indexed by the month-end, so `L(t)` is the balance opening month `t` and `L(t+1)`
the balance closing it; the draw is made at the opening month-end and reads the payable
value there. The roll runs on `j_L = (1 + i_L)^(1/12) − 1`, so twelve months compound back to
exactly the annual 보험계약대출이율 the 약관 quotes. Every payment is made **net of the
opening balance and floored at zero**:

    death benefit    = max(0, SA(t) - L(t))
    surrender payout = max(0, CV(t+1) - L(t))
    감액 proceeds     = reduce_frac * max(0, CV(t+1) - L(t))

Four features of the Korean loan matter and none is optional. **The rate is a vintage
rate** — 「예정이율 + 1.5%」 on a 금리확정형 contract, 「공시이율 + 1.5%」 on a 금리연동형
one, at three carriers independently [S9] [S11] [S13] — so one carrier's live range spans
**연 3.5% ~ 10.5%** across its in-force book [S11]. **The limit is a fraction of the
*payable* value**, so on a suppressed form it is suppressed too. **There is no
early-repayment fee** [S11] [S13]. And **the loan is settled first on every exit**, 즉시 on
해지 [S5 제34조] [REG-R25 제26조](#krlib-reg-r25): Korea has **no equivalent of the Japanese
loan-excess-lapse notice**, so the balance never terminates the contract — it absorbs the
payout instead.

**No repayment is modelled [std]** and the draw is a single event, so the balance compounds
untouched: on `point_id = 6` a draw of ₩8,265,310.25 at the month-end `d = 108` — the start
of policy year 10 — crosses the ₩100,000,000 sum assured at **`d = 871`**, seven months into
policy year 73, and reaches **₩114,044,264.36 by `d = 911`**, so every later payment floors at
zero. The crossing month is a number the annual grid could not produce at all; it could only
say which policy year the balance overtook the cover in. A real book repays; this one does
not, and the floor is where it shows.

`check_loan_roll_fwd()` asserts the recursion over every month.

### 보험료 납입면제 as a state transition

Within month `t`, **before** the premium is taken:

    waiver(t)   = lp(t) * u^m(t)                    moves out of the paying cohort
    lp_exp(t)   = lp(t) - waiver(t)                 pays the premium this month
    lw_exp(t)   = lw(t) + waiver(t)                 accrues value, pays nothing

Both cohorts then carry the **same** mortality and the **same** lapse rate **[std]** — no
Korean source distinguishes the persistency of a waived contract — and both roll forward
together:

    lp(t+1) = lp_exp(t) * (1 - q^m(t)) * (1 - w^m(t)) + R(t+1)
    lw(t+1) = lw_exp(t) * (1 - q^m(t)) * (1 - w^m(t))
    l(t)    = lp(t) + lw(t)

The premium is weighted by `lp_exp(t)`, everything else by `l(t)`. **That is the whole
content of the waiver in cash-flow terms**: a waived policy contributes to the in-force
count, to maintenance expense and to every benefit, and to neither premium nor commission.
The two weights coincide in the base run, where `u ≡ 0`, which is exactly why the
distinction has to be written down rather than discovered when the module is switched on.
`point_id = 7` runs it at 0.4% p.a. — converted month by month like every other decrement, so
twelve compound back to it — and reaches `pols_waived(240) = 0.044660`. The monthly grid also
places the transition in the month of the 장해 rather than at the next 계약해당일, which is
what the deemed-paid rule actually says.

### 감액 as a partial surrender

감액 is universal and the 약관 treats the reduced portion as terminated: 「그 감액된 부분은
해지된 것으로 보며, 이로써 회사가 지급하여야 할 해지환급금이 있을 때에는 … 지급합니다」
[S5 제20조]. On a suppressed contract the accompanying warning is the main event rather than
a caveat: a reduction made during 납입기간 pays at `k W(d)`, and on a 무해지 contract it
pays **nothing at all**. The reduction falls at the end of policy year `reduce_year` — the
month `t = 12 × reduce_year − 1` — on the 계약해당일 `d = 12 × reduce_year` that closes it,
the same contractual date the annual grid used and now located to the month:

    claims(t, "REDUCTION") = reduce_frac * max(0, CV(t+1) - L(t)) * l_after_decrements(t)
                                                  in month t = 12 * reduce_year - 1
    sa_factor(d) = 1 - reduce_frac     for d > 12 * reduce_year

The restatement is exact here because **every** quantity carrying the 가입금액 is
proportional to it: `SA`, `G`, `V(d)`, `SC(d)` and therefore `W(d)` all step down by
the same factor from the month-end `12 × reduce_year + 1`. The 약관's pro-rata restatements of 이미 납입한 보험료,
중도인출 누적액 and 초과납입액 [S5 제20조] matter only on designs whose death benefit is a
function of premiums paid, which the 평준형 composite is not. `point_id = 10` reduces 50%
of a ₩1,000,000,000 cover at duration 15.

### 부활 as a twelve-month re-entry

    R(t) = reinstate_rate * S(t - 12)       into the paying cohort at the start of month t
    Sp(t) = S(t) - R(t + 12)                the lapses actually paid a surrender value

The substantive effect is not the count but the **payment**: a reinstated policyholder is
not paid a surrender value, because 부활 requires that the 해약환급금 has not been drawn and
the 약관 expressly includes the case where there was none to draw [S5 제26조] [REG-R25
제27조](#krlib-reg-r25). A twelve-month lag is a **[std]** simplification of a three-year
window — the same year it always was — and no arrears cash flow is modelled for the twelve
instalments that now fall inside it **[std]**. The monthly grid makes that omission visible as
twelve missing rows where the annual grid could state it as "no instalment falls inside a
one-year gap". `point_id = 10` runs it at 20%.

### Processing order (month `t = 0 … T − 1`, i.e. policy years 1 … T_y)

The order is explicit because two steps in it are worth money and one is a convention.

1. **Start of the month — the in-force split.** `l(t) = lp(t) + lw(t)`. This is the
   `result_cf()` row's `pols_if` and the weight on every non-premium cash flow in it.
2. **Start of the month — 납입면제 transition.** `waiver(t) = lp(t) × u^m(t)` moves out of
   the paying cohort **before** the premium is taken.
3. **Start of the month — premium.** `premiums(t) = G^m(t) × lp_exp(t)` for `t < 12m`, in
   advance, on the paying cohort only. **Zero from `t = 12m` onwards, for ever.**
4. **Start of the month — expenses and commission.** Acquisition expense and initial
   commission at `t = 0` only, on `l(0)`; the commission is computed on the **annualized**
   premium, because that is the unit a Korean commission scale is written in. Maintenance
   expense `e × (1 + π)^⌊t/12⌋ × l(t)` at the start of **every** month, for life. The
   premium-related expense on every premium collected, months `t = 0 … 12m − 1`; the renewal
   commission on the premium of months `t = 12 … 12m − 1` (policy years 2 … m).
5. **Start of the month — 보험계약대출 draw**, where one is elected, off `CV(t)`, the value
   at the opening month-end.
6. **Cash values.** `V(t+1)`, `SC(t+1)`, `W(t+1)`, `CV(t+1)` at the month-end that closes
   the month.
7. **End of the month — deaths.** `D(t) = l(t) × q^m(t)`, paid `max(0, SA(t) − L(t))` each,
   plus `ec × D(t)` of claim expense.
8. **End of the month — 해지**, on the survivors of mortality — **death before lapse [std
   order]**: `S(t) = l(t) × (1 − q^m(t)) × w^m(t)`, of which `Sp(t) = S(t) − R(t + 12)` is
   paid `max(0, CV(t + 1) − L(t))`.
9. **End of the month — 감액**, at the same month-end, on those continuing after both
   decrements.
10. **End of the month — loan roll-up.** `L(t + 1) = (L(t) + Δ(t)) × (1 + j_L)`.
11. **Start of month `t + 12` — 부활.** `R(t + 12)` of month `t`'s lapses returns to the
    paying cohort, and is **not** paid a surrender value.
12. **Update in force**, per the two-cohort recursion above.
13. **In the terminal policy year** the table's rate is 1 and `q^m(t) = 1 / (12 − t mod 12)`
    spreads that certain death evenly over its twelve months, so `l(T) = 0` at `t = T − 1`
    and the projection ends. `V(T) := 0` by definition. No maturity payment, no tail states.

**Death before lapse is a [std] ordering** and it is not neutral: reversing it applies the
lapse rate to the full in-force count instead of to survivors, moving both the surrender
outgo and the roll-forward. Asserted by `check_pols_roll_fwd()`.

**The account recursion runs on its own clock.** `V(d)` is a function of `d`, `P^m`, `j_acc`
and `q^m` alone — **not of `l(t)`, `w(t)` or `u(t)`** — because it is a per-policy contractual
quantity. That is why the 표준형 twin can be priced 「해지율을 적용하지 않고」 [S1] and still
be the same object the sold form's value is a fraction of.

### Net cash flow

Income-positive, per policy issued:

    CF(t) =   G^m(t) * lp_exp(t) * 1{t < 12m}                    (premiums)
            - max(0, SA(t) - L(t)) * D(t)                        (claims_death)
            - max(0, CV(t+1) - L(t)) * Sp(t)                     (claims_lapse)
            - reduce_frac * max(0, CV(t+1) - L(t)) * l_aft(t)    (claims_reduction)
            - ec * D(t)                                          (claim_expenses)
            - ( AC - c0*AC ) * 1{t = 0} * l(0)                   (expenses: acquisition)
            - e * (1 + pi)^floor(t/12) * l(t)                    (expenses: maintenance)
            - 0.02 * premiums(t)                                 (expenses: premium-related)
            - min(c0 * AC, G) * 1{t = 0} * l(0)                  (commissions: initial)
            - c_r * premiums(t) * 1{12 <= t <= 12m - 1}          (commissions: renewal)

`result_cf()` publishes these as `pols_if`, `premiums`, `claims_death`, `claims_lapse`,
`claims_reduction`, `claim_expenses`, `expenses`, `commissions`, `net_cf` — `pols_if` first,
`net_cf` last, **no `claims` subtotal column**, so the columns sum exactly to `net_cf`.
`expenses` is acquisition plus maintenance plus the premium-related component; the claim
handling expense stands beside it, the settled vocabulary across the six libraries.
`claims_reduction` is zero on the anchor and published rather than dropped, 감액 being
universal on this chassis. `check_net_cf()` asserts the ledger at every `t`.

**Two roll-forward identities close the projection.**

    l(t) - l(t+1) - D(t) - S(t) + R(t+1) = 0                    check_pols_roll_fwd()
                                                                (R(t+1) = 0 unless t+1 >= 12)
    l(0) + sum R - sum (D + S) - l(t+1)  = 0                    check_decrement_sum()

Because the table terminates, every policy leaves by one of the two decrements, so
`Σ D(t) + Σ S(t) = 1` in the base run and `l(T) = 0`. Each `check_*()` takes **no
argument and returns a bool** over all `t`, with the per-`t` signed residual at
`check_*_resid(t)`. Nine of them ship and all nine are `True` on all ten model points.

### Optional modules (all off in the base run)

| Module | Switch | Base | Exercised on |
|---|---|---|---|
| 보험계약대출 | `loan_util`, `loan_year` | 0 | `point_id = 6` (저해지) and `3` (무해지, draws zero) |
| 보험료 납입면제 | `waiver_rate` | 0 | `point_id = 7`, 0.4% p.a., converted monthly |
| 유지보너스 + the mandatory ≥ 30% lapse spike | `bonus_rate` | 0 | `point_id = 8`, 13.8% on a 7년납 design |
| 금리연동형 crediting | `int_basis`, `decl_rate` | `fixed` | `point_id = 9`, 공시이율 2.75% |
| 감액 | `reduce_year`, `reduce_frac` | 0 | `point_id = 10`, 50% at duration 15 |
| 부활 | `reinstate_rate` | 0 | `point_id = 10`, 20% |
| `flat` lapse basis | `lapse_basis` | `loglinear` | `point_id = 10`, and re-run on the anchor below |
| Best-estimate mortality lever | `mort_be_factor` | 1.00 | `point_id = 10`, 0.90 |

Each module is implemented and switched off so the base run reproduces the worked example
while the machinery stays visible and testable. **Nothing here is a placeholder**: every one
produces a signature number asserted in `tests/test_whole_life_kr.py`.

---

## Policyholder behavior modeling

All dynamic forms are **[std]** reference constructions. There is no public calibration
evidence for any of them on this product, and the one place where a supervisor has
substituted its own judgement — the lapse vector — is precisely the place where that
absence became a systemic problem.

- **Base surrender.** The `loglinear` vector of class (c): 10% in policy year 1 decaying
  log-linearly to 0.1% at 납입완료, then 0.8% for life. It is the FSS 원칙모형 [REG-R27]
  [R3] with its start pinned to the top of a disclosed 적용해지율 envelope [S2]. The
  disclosed *pricing* envelopes are much higher — 1%–10% [S2], 0%–13.4% [S8] — and the two
  bases serve different purposes and cannot be reconciled from public data. **This is the
  single largest assumption gap for this product.**
- **The 표준형 twin carries no lapse assumption at all** [S1] — which is what makes it a
  pure account run-off, and why the `flat` basis here is level rather than shaped.
- **The shape between the ends is [std] and it does the work.** The endpoints are
  regulatory; the log-linear interpolation is this library's. Alternatives — 선형-로그,
  로그-로그 — are permitted to a Korean insurer only against audited disclosure of the
  difference in **CSM, BEL, K-ICS ratio and net income**, external validation, quarterly FSS
  reporting and an on-site inspection [REG-R27] [R3]. The shipped `flat` basis runs that
  comparison in one line; it is exercised below.
- **No dynamic lapse function is implemented [std].** The natural driver here is the 환급률
  crossing 1, which on the anchor happens at the month-end `d = 280`, three years and four
  months after the cliff; a form keyed on `refund_ratio(d)` would generate a spike there
  endogenously, and the monthly grid would place it in the month it belongs to. It is deliberately
  **not** shipped: the November 2024 decision fixes the base vector, and an overlay on a
  supervised assumption is a departure requiring the disclosure regime above [REG-R27]. The
  hook is `lapse_rate(t)`; adding one changes no other formula.
- **The spike at a 유지보너스 date is a mechanic, not a behaviour, in one direction only.**
  The bonus credit is contractual [S7]; the ≥ 30% additional lapse is a supervisory
  requirement on the assumption [REG-R27]. Modelling the first without the second is not a
  simplification, it is an error, and `lapse_spike()` is wired to `bonus_rate()` so it cannot
  be done by accident.
- **Lapse is behavioural and terminal only by choice.** With no APL in evidence [S5]
  [REG-R25], a Korean policyholder who misses the 14-day 납입최고기간 loses the contract
  whatever its cash value. But 부활 within three years is available **even where the
  해약환급금 was nil** [S5 제26조] [REG-R25 제27조](#krlib-reg-r25), so the exit is not terminal in the
  contract. `reinstate_rate` is zero in the base run, which **understates** later-duration
  in force and therefore both premium income and claims. The bias is stated rather than
  corrected because no retrieved source gives a Korean reinstatement rate.
- **보험계약대출 take-up is static, and the loan does not terminate the contract.** Korea
  has no loan-excess-lapse notice [S5] [REG-R25], so unlike `jplib`'s APL the loan cannot end
  the policy — it only absorbs the payout, which on `point_id = 6` it eventually does in
  full.
- **The premium waiver is an option with value, not a protection feature.** Because waived
  premiums count as paid [S2] [S3] [S6] [S8], the waiver is the only route to the cliff the
  policyholder does not have to fund. On a 무해지 contract that asymmetry is extreme: the
  waiver converts a contract worth nothing on surrender into one that steps to the full
  표준형 value at 납입완료 without another won being paid. No incidence rate for the 50%
  장해지급률 trigger was retrieved, so the 0.4% p.a. on `point_id = 7` is **[std]** and its
  purpose is to exercise the state, not to size the option.
- **The disease riders that extend the waiver trigger are not modelled.** 3대질병, 6대질병
  and their 90-day 면책기간 belong to the incidence machinery of [cancer
  (암보험)](../cancer/technical-notes.md) and [CI (CI보험)](../ci_insurance/technical-notes.md)
  [S1] [S2] [S3] [S5] [S6].
- **면책 incidence is zero in the base run [std], and refusal is not forfeiture.** On an
  면책사유 the insurer must still pay 「보험수익자를 위하여 적립한 금액」, in practice the
  계약자적립액 [REG-R50 제736조](#krlib-reg-r50) [REG-R25 제22조](#krlib-reg-r25). The composite carries no exclusion
  incidence, so nothing is deducted; **treating an exclusion as a zero-payment event
  overstates the insurer's position** by the account, not by the claim.

---

## Worked example

### The anchor cell

**`point_id = 1`** — 남자, 보험나이 **40세**, 보험가입금액 **₩100,000,000 (1억원)**,
보험기간 **종신**, 납입기간 **20년**, 월납, **저해지환급형 `k = 0.50`**, monthly premium
**₩231,345.00** (annual ₩2,776,140). `T_y = 115 − 40 + 1 = 76` policy years and
`T = 912` months — `t = 0 … 911` — attained 보험나이 40 to 115.
Every optional module is off: `waiver_rate = loan_util = bonus_rate = reduce_frac =
reinstate_rate = 0`, `int_basis = fixed`, `lapse_basis = loglinear`, `mort_be_factor = 1.00`.

The premium is **0.900 × ₩3,084,600 [std]**, a rounding of the 89.9% ratio published at a
50% suppression [S1], and ₩3,084,600 is 12 × the published
₩257,050 monthly rate for exactly this cell [S4], which is `point_id = 2` — **the 표준형
comparison twin, same cell, `k = 1.00`.** The two run side by side throughout.

**Assumption values used, in full.** `i = i_acc = 2.50%` **[std]** on the disclosed
2.25%–2.75% band [S1] [S2] [S5] [S6] [S7] [S8]; `q` from `mort_table.csv` 남 at attained
보험나이 with `mort_be_factor = 1.00`, **[std]** construction anchored on [S2] [S8] and
calibrated to [REG-R38] and [REG-R33]; `w` the `loglinear` vector, endpoints [REG-R27] [R3]
and [S2], interpolation **[std]**; `SC* ` from 별표 14 [REG-R20] with the 7-year 해약공제기간
of [REG-R19]; `AC = SC*` and `c₀ = 0.65` **[std]** inside [REG-R22]; `c_r = 3.0%`,
`e = ₩5,000` a month inflating at 2.0% a year, 2.0% of premium, `ec = ₩300,000` per claim, all
**[std]**; `i_L = 4.00%` [S9] [S11] [S13], unused here because `loan_pp ≡ 0`.

**Derived scalars, at full precision.**

| Quantity | Cells | Value |
|---|---|---|
| Terminal age ω | `omega_age()` | 115 |
| Number of policy years `T_y` | `proj_years()` | **76** |
| Number of policy months `T` | `proj_len()` | **912** (frame `t = 0 … 911`) |
| 납입기간 `m`, in years | `prem_period()`, `prem_end()` | 20 |
| 납입기간 in months | `prem_period_mths()` | 240 |
| 해약공제기간 `n_sc`, in years | `surr_chg_period()` | **7** |
| 해약공제기간 in months | `surr_chg_period_mths()` | 84 |
| `A(40)` | `epv_death(40)` | 0.332153184440 |
| `ä(40, 20)` | `annuity_due(40, 20)` | 15.766511588794 |
| 연납순보험료 `P` — the 별표 14 quantity | `prem_net_level_pp()` | **₩2,106,700.5378440050** |
| **월납순보험료 `P^m`** — what the account consumes | `prem_net_level_mth_pp()` | **₩179,777.0581452671** |
| 연납순보험료, 20년납 footing `P₂₀` | `prem_net_20yr_pp()` | ₩2,106,700.5378440050 |
| 영업보험료 `G`, annual | `premium_pp()` | **₩2,776,140.0000000000** |
| 영업보험료 `G^m`, the month's income | `premium_mth_pp()` | **₩231,345.00** |
| Loaded premium on the model's own rule | `prem_gross_calc_pp()` | ₩2,776,167.8347600726 |
| **표준해약공제액** `SC*` | `surr_chg_cap_pp()` | **₩3,106,700.5378440050** |
| 계약체결비용 `AC` | `acq_cost_pp()` | ₩3,106,700.5378440050 |
| First-year commission | `comm_init_pp()` | ₩2,019,355.3495986033 |
| Acquisition **expense** at `t = 0` | `acq_cost_pp() − comm_init_pp()` | ₩1,087,345.1882454017 |
| Accrual rate `i_acc`, annual | `acc_int_rate()` | 0.025 |
| Accrual rate `j_acc`, per month | `acc_int_rate_mth()` | 0.0020598316 |
| Loan rate `i_L`, annual | `loan_int_rate()` | 0.04 |

**`12 P^m = ₩2,157,324.70` is 2.4% above `P`, and that is not a rounding.** A monthly
equivalence discounts eleven of each year's twelve instalments and exposes them to the
year's mortality, where an annual one collects the whole premium at the anniversary; the
account built from `P^m` is correspondingly about half a year's interest at the 예정이율
above the one an annual grid produced. `P` survives because 별표 14 names the 연납순보험료
and the statutory `SC*` is computed from it, and because `prem_gross_calc_pp` loads it.

`P₂₀ = P` here because `m = 20` exactly — the one configuration in which the two annuities
coincide, and part of why the anchor is the regulator's own reference cell [REG-R9]
[REG-R20]. **`prem_gross_calc_pp()` misses the sourced premium by 0.0010%**
(₩2,776,167.83 against ₩2,776,140.00, a fit of 1.0000100), and the projection uses the
sourced number. On the 표준형 twin the same rule gives ₩3,084,630.93 against ₩3,084,600 —
the identical relative error, because `θ` was calibrated on that cell once and applied
unchanged.

**Two cross-checks on the statutory cap, neither used to fit it.** The FSC states the same
cap as 「보장성보험 월 보험료의 13배 수준」 [REG-R29], and 13 × ₩257,050 = ₩3,341,650; the
model's ₩3,106,700.54 is **7.0% below** that rule of thumb. And the net-premium ratio the
model computes is `P / G_표준형` = **0.682974**, not the 80% `product-spec.md` uses to
*illustrate* the cap — so the specification's ₩3,470,000 illustration and the model's
₩3,106,700.54 differ by 10.5%, entirely because the model derives `P` from equivalence
rather than assuming a loading ratio. The model's is what is projected.

**The anchor's mortality and lapse rates, policy years 1 … 25.** One row per policy year,
read at its first month `t = 12(y − 1)` and level through all twelve: 보험나이 steps on the
계약해당일 and both vectors are published by year, so a within-year drift in either would be
an invention. The **annual** rates are the sourced quantities; `q^m` and `w^m` are their
`1 − (1 − q)^(1/12)` conversions **[std]**, and are what the roll-forward applies.

| y | attained age | `mort_rate` | `mort_rate_mth` | `lapse_rate` | `lapse_rate_mth` |
|---|---|---|---|---|---|
| 1 | 40 | 0.00085000 | 0.0000708609 | 0.1000000000 | 0.0087416110 |
| 2 | 41 | 0.00092944 | 0.0000774863 | 0.0784759970 | 0.0067873987 |
| 3 | 42 | 0.00101630 | 0.0000847311 | 0.0615848211 | 0.0052828967 |
| 4 | 43 | 0.00111127 | 0.0000926530 | 0.0483293024 | 0.0041195089 |
| 5 | 44 | 0.00121513 | 0.0001013173 | 0.0379269019 | 0.0032168852 |
| 6 | 45 | 0.00132869 | 0.0001107917 | 0.0297635144 | 0.0025147858 |
| 7 | 46 | 0.00145286 | 0.0001211524 | 0.0233572147 | 0.0019675882 |
| 8 | 47 | 0.00158864 | 0.0001324832 | 0.0183298071 | 0.0015404689 |
| 9 | 48 | 0.00173710 | 0.0001448737 | 0.0143844989 | 0.0012066846 |
| 10 | 49 | 0.00189944 | 0.0001584246 | 0.0112883789 | 0.0009456007 |
| 11 | 50 | 0.00207696 | 0.0001732450 | 0.0088586679 | 0.0007412367 |
| 12 | 51 | 0.00227106 | 0.0001894523 | 0.0069519280 | 0.0005811815 |
| 13 | 52 | 0.00248330 | 0.0002071776 | 0.0054555948 | 0.0004557737 |
| 14 | 53 | 0.00271538 | 0.0002265638 | 0.0042813324 | 0.0003574797 |
| 15 | 54 | 0.00296914 | 0.0002477657 | 0.0033598183 | 0.0002804169 |
| 16 | 55 | 0.00324662 | 0.0002709551 | 0.0026366509 | 0.0002199869 |
| 17 | 56 | 0.00355003 | 0.0002963183 | 0.0020691381 | 0.0001725919 |
| 18 | 57 | 0.00388180 | 0.0003240603 | 0.0016237767 | 0.0001354155 |
| 19 | 58 | 0.00424458 | 0.0003544050 | 0.0012742750 | 0.0001062517 |
| 20 | 59 | 0.00464125 | 0.0003875960 | 0.0010000000 | 0.0000833716 |
| 21 | 60 | 0.00507500 | 0.0004239036 | 0.0080000000 | 0.0006691237 |
| 22 | 61 | 0.00551816 | 0.0004610138 | 0.0080000000 | 0.0006691237 |
| 23 | 62 | 0.00600277 | 0.0005016124 | 0.0080000000 | 0.0006691237 |
| 24 | 63 | 0.00653292 | 0.0005460469 | 0.0080000000 | 0.0006691237 |
| 25 | 64 | 0.00711315 | 0.0005947038 | 0.0080000000 | 0.0006691237 |

`q(40) = 0.00085` and `q(60) = 0.005075` are **ANCHOR** rows — the mean of 하나생명's
0.000780 [S2] and KDB생명's 0.00092 [S8] at 40, and of 0.004550 and 0.00560 at 60; the rates
are sourced, the mean is **[std]**. Everything between is log-linear in `ln q`. `w(0) = 0.10`
and `w(19) = 0.001` at 납입완료 are exact by construction, and `w(20) = 0.008` is the FSS
ultimate rate [REG-R27].

### The first policy year of the base run, and the milestone months

Per policy issued, income-positive, to two decimal places — the precision the tests assert.
The statement runs to `t = 911`; printed here are the whole of policy year 1 and the turn
into year 2, then the months around 납입완료 and four spread over the sixty years after it.

| t | age | `pols_if(t)` | premiums | claims_death | claims_lapse | claim_expenses | expenses | commissions | net_cf |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 40 | 1.000000 | **231,345.00** | **7,086.09** | **0.00** | **21.26** | **1,096,972.09** | **2,019,355.35** | **−2,892,089.79** |
| 1 | 40 | 0.991188 | 229,306.42 | 7,023.65 | 0.00 | 21.07 | 9,542.07 | 0.00 | 212,719.63 |
| 2 | 40 | 0.982454 | 227,285.81 | 6,961.76 | 0.00 | 20.89 | 9,457.99 | 0.00 | 210,845.18 |
| 3 | 40 | 0.973797 | 225,283.00 | 6,900.42 | 0.00 | 20.70 | 9,374.64 | 0.00 | 208,987.24 |
| 4 | 40 | 0.965216 | 223,297.84 | 6,839.61 | 0.00 | 20.52 | 9,292.04 | 0.00 | 207,145.67 |
| 5 | 40 | 0.956710 | 221,330.17 | 6,779.34 | 0.00 | 20.34 | 9,210.16 | 0.00 | 205,320.34 |
| 6 | 40 | 0.948280 | 219,379.84 | 6,719.60 | 0.00 | 20.16 | 9,129.00 | 0.00 | 203,511.08 |
| 7 | 40 | 0.939924 | 217,446.70 | 6,660.39 | 0.00 | 19.98 | 9,048.55 | 0.00 | 201,717.77 |
| 8 | 40 | 0.931641 | 215,530.59 | 6,601.70 | 0.00 | 19.81 | 8,968.82 | 0.00 | 199,940.27 |
| 9 | 40 | 0.923432 | 213,631.37 | 6,543.53 | 0.00 | 19.63 | 8,889.79 | 0.00 | 198,178.42 |
| 10 | 40 | 0.915295 | 211,748.88 | 6,485.87 | 0.00 | 19.46 | 8,811.45 | 0.00 | 196,432.10 |
| 11 | 40 | 0.907229 | 209,882.98 | 6,428.71 | 0.00 | 19.29 | 8,733.81 | 0.00 | 194,701.17 |
| 12 | 41 | 0.899235 | 208,033.52 | 6,967.84 | 0.00 | 20.90 | 8,746.77 | 6,241.01 | 186,057.00 |

| t | age | `pols_if(t)` | premiums | claims_death | claims_lapse | claim_expenses | expenses | commissions | net_cf |
|---|---|---|---|---|---|---|---|---|---|
| 60 | 45 | 0.708946 | 164,011.16 | 7,854.53 | 9,201.72 | 23.56 | 7,193.89 | 4,920.33 | 134,817.12 |
| 120 | 50 | 0.637513 | 147,485.53 | 11,044.60 | 5,535.20 | 33.13 | 6,835.34 | 4,424.57 | 119,612.69 |
| 228 | 59 | 0.597934 | 138,328.95 | 23,175.67 | 1,223.61 | 69.53 | 7,121.96 | 4,149.87 | 102,588.32 |
| 239 | 59 | 0.594843 | **137,614.06** | **23,055.90** | **2,579.03** | **69.17** | **7,085.15** | **4,128.42** | **100,696.39** |
| 240 | 60 | 0.594563 | **0.00** | **25,203.75** | **20,722.80** | **75.61** | **4,417.45** | **0.00** | **−50,419.61** |
| 241 | 60 | 0.593914 | 0.00 | 25,176.21 | 20,734.74 | 75.53 | 4,412.62 | 0.00 | −50,399.10 |
| 276 | 63 | 0.570828 | 0.00 | 31,169.90 | 21,116.60 | 93.51 | 4,500.69 | 0.00 | −56,880.71 |
| 468 | 79 | 0.402873 | 0.00 | 91,539.53 | 19,702.26 | 274.62 | 4,360.59 | 0.00 | −115,877.00 |
| 708 | 99 | 0.067131 | 0.00 | 114,443.72 | 4,053.15 | 343.33 | 1,079.70 | 0.00 | −119,919.90 |
| 911 | 115 | 0.000000 | 0.00 | 4.21 | 0.00 | 0.01 | 0.00 | 0.00 | −4.22 |

The `age` column is `x + ⌊t/12⌋` and the contractual policy year is `⌊t/12⌋ + 1`. The
`claims_reduction` column is identically **0.00** on this cell and is omitted from the
display; it is published in `result_cf()` rather than dropped, because 감액 is universal on
this chassis and `point_id = 10` uses it.

**Five rows do something.** `t = 0` carries the whole acquisition cost against **one
month's** premium and is the only negative month before 완납 — ₩2,892,089.79 of strain,
12.5 times the month's premium, where an annual step netted the same charge against a year
and printed ₩531,338. `t = 12` is the 계약해당일 closing policy year 1, where three things
move at once: the attained 보험나이 turns 41, the expense inflation factor makes its first
step, and the renewal commission starts. `t = 239` is the last paying month and the
**cliff**: the payable surrender value doubles at the month-end that closes it. `t = 240` is
the **first premium-free month**, where the stream turns permanently negative — premium and
commission both go to zero in the same row while every outgo continues. `t = 911` is the
horizon: the table's terminal rate has run the surviving cohort to nothing over the last
twelve months, and nothing is paid but the death benefit.

### Surrender values at the same month-ends

Keyed by the **month-end** `d`, not by the month: these are values at a point in time, and
the row of month `t` in `result_val()` carries the month-end `d = t + 1` that closes it. A
**계약해당일 is `d = 12y`**, which is where every published 해지환급금 grid is quoted;
`d = 1` and `d = 6` are printed because a monthly account has values **inside** the policy
year that an annual grid could not state at all.

| d | `pol_val_pp(d)` | `surr_chg_pp(d)` | `cv_std_pp(d)` | `cv_pp(d)` | `cv_susp_pp(d)` | `cum_prem_pp(d)` | `refund_ratio(d)` |
|---|---|---|---|---|---|---|---|
| 1 | 173,073.54 | 3,069,716.01 | 0.00 | 0.00 | 0.00 | 231,345.00 | 0.000000 |
| 6 | 1,043,988.88 | 2,884,793.36 | 0.00 | 0.00 | 0.00 | 1,388,070.00 | 0.000000 |
| 12 | 2,101,396.55 | 2,662,886.18 | 0.00 | 0.00 | 0.00 | 2,776,140.00 | 0.000000 |
| 24 | 4,249,377.45 | 2,219,071.81 | 2,030,305.64 | 1,015,152.82 | 1,015,152.82 | 5,552,280.00 | 0.182835 |
| 36 | 6,444,786.36 | 1,775,257.45 | 4,669,528.91 | 2,334,764.46 | 2,334,764.46 | 8,328,420.00 | 0.280337 |
| 48 | 8,688,485.75 | 1,331,443.09 | 7,357,042.66 | 3,678,521.33 | 3,678,521.33 | 11,104,560.00 | 0.331262 |
| 60 | 10,981,357.96 | 887,628.73 | 10,093,729.24 | 5,046,864.62 | 5,046,864.62 | 13,880,700.00 | 0.363589 |
| 72 | 13,324,313.14 | 443,814.36 | 12,880,498.78 | 6,440,249.39 | 6,440,249.39 | 16,656,840.00 | 0.386643 |
| **84** | 15,718,292.14 | 0.00 | 15,718,292.14 | 7,859,146.07 | 7,859,146.07 | 19,432,980.00 | 0.404423 |
| 96 | 18,164,272.12 | 0.00 | 18,164,272.12 | 9,082,136.06 | 9,082,136.06 | 22,209,120.00 | 0.408937 |
| 108 | 20,663,275.63 | 0.00 | 20,663,275.63 | 10,331,637.81 | 10,331,637.81 | 24,985,260.00 | 0.413509 |
| 120 | 23,216,376.79 | 0.00 | 23,216,376.79 | 11,608,188.39 | 11,608,188.39 | 27,761,400.00 | 0.418141 |
| 132 | 25,824,712.38 | 0.00 | 25,824,712.38 | 12,912,356.19 | 12,912,356.19 | 30,537,540.00 | 0.422836 |
| 144 | 28,489,495.44 | 0.00 | 28,489,495.44 | 14,244,747.72 | 14,244,747.72 | 33,313,680.00 | 0.427595 |
| 180 | 36,836,090.86 | 0.00 | 36,836,090.86 | 18,418,045.43 | 18,418,045.43 | 41,642,100.00 | 0.442294 |
| 216 | 45,745,067.40 | 0.00 | 45,745,067.40 | 22,872,533.70 | 22,872,533.70 | 49,970,520.00 | 0.457721 |
| 228 | 48,848,924.03 | 0.00 | 48,848,924.03 | 24,424,462.02 | 24,424,462.02 | 52,746,660.00 | 0.463052 |
| **239** | 51,755,813.04 | 0.00 | 51,755,813.04 | 25,877,906.52 | 25,877,906.52 | 55,291,455.00 | 0.468027 |
| **240** | 52,023,973.59 | 0.00 | 52,023,973.59 | 52,023,973.59 | 26,011,986.79 | 55,522,800.00 | 0.936984 |
| 241 | 52,110,834.07 | 0.00 | 52,110,834.07 | 52,110,834.07 | 26,055,417.03 | 55,522,800.00 | 0.938548 |
| 252 | 53,080,662.78 | 0.00 | 53,080,662.78 | 53,080,662.78 | 26,540,331.39 | 55,522,800.00 | 0.956016 |
| 276 | 55,226,450.40 | 0.00 | 55,226,450.40 | 55,226,450.40 | 27,613,225.20 | 55,522,800.00 | 0.994663 |
| 288 | 56,314,255.07 | 0.00 | 56,314,255.07 | 56,314,255.07 | 28,157,127.53 | 55,522,800.00 | 1.014255 |
| 300 | 57,411,045.18 | 0.00 | 57,411,045.18 | 57,411,045.18 | 28,705,522.59 | 55,522,800.00 | 1.034008 |
| 360 | 63,000,180.99 | 0.00 | 63,000,180.99 | 63,000,180.99 | 31,500,090.50 | 55,522,800.00 | 1.134672 |
| 480 | 74,269,001.52 | 0.00 | 74,269,001.52 | 74,269,001.52 | 37,134,500.76 | 55,522,800.00 | 1.337631 |
| 720 | 92,405,944.03 | 0.00 | 92,405,944.03 | 92,405,944.03 | 46,202,972.01 | 55,522,800.00 | 1.664288 |
| 900 | 98,673,877.93 | 0.00 | 98,673,877.93 | 98,673,877.93 | 49,336,938.96 | 55,522,800.00 | 1.777178 |
| 912 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 55,522,800.00 | 0.000000 |

**Read the step off month-ends 239 and 240.** `cv_pp` goes from **₩25,877,906.52** to
**₩52,023,973.59** — exactly `1 / k = 2.0` on the same underlying value — while `cv_std_pp`
moves from ₩51,755,813.04 to ₩52,023,973.59, **one month's accrual of 0.5%**. The whole of
the step is the removal of `k`, and the monthly grid is what makes that arithmetically
obvious: an annual step compared the doubling against a 6.5% year and a reader could still
wonder whether some of it was growth. **The surrender charge reached zero at `d = 84`**,
thirteen years earlier, so nothing about the step is a surrender-charge effect either.
`cv_susp_pp` continues on the other side of the boundary — ₩26,011,986.79 at `d = 240` — so
both quantities are visible at the boundary rather than inferred. Both sit on the
`result_val()` row of month `t = 239`.

**The surrender value becomes payable inside a policy year**, which is a statement an annual
grid could not make: `cv_std_pp` is nil at `d = 12` and positive from **`d = 15`**, the third
month of policy year 2, because that is when the account overtakes the unamortised
해약공제액. The suppression applies to it from that instant.

**Month-end 1 is nil in both columns**, the surrender charge biting exactly as the
regulation bounds it: `V(1)` = ₩173,073.54 against `SC(1)` = ₩3,069,716.01, so
`max(0, V − SC)` is zero and 「이를 영(零)으로 처리한다」 does the flooring [REG-R19]. Every
published Korean grid in the set shows nil at duration 1 [S1] [S4] [S6] [S8].
**Month-end 912 is zero throughout**: at the terminal age everyone has died and `V(T)` is
defined as zero, so `refund_ratio(912)` is 0.000000 and not a crossing.

**The 환급률 crosses 100% at `d = 280`** — the fourth month-end of policy year 24, a date
rather than a year. The 표준형 twin, `point_id = 2`, reaches the **identical policy value**
and crosses at **`d = 347`**, the eleventh month-end of policy year 29 — five and a half years
later, on the same account, purely because its denominator is ₩257,050 a month instead of
₩231,345. **That is the whole of the refund-ratio argument that sells this product**, stated
in two numbers.

### Hand traces

Five months, written out term by term, so that a reader with a calculator can reproduce a
row and watch the processing order do its work. Flows carry the month index `t`; the
account, the deduction and the surrender values carry the month-end `d`, and the one that
closes month `t` is `d = t + 1`. All arithmetic is on the printed rates and on the
full-precision values above. `j_acc = (1 + 0.025)^(1/12) − 1 = 0.0020598316` and
`P^m = ₩179,777.0581452671`.


**Trace, month `t = 0` (policy year 1) — the acquisition month.**

    l(0) = 1.0000000000,  q^m(0) = 0.0000708609,  w^m(0) = 0.0087416110
    premiums   = 231,345.00 x 1.0000000000 = 231,345.00
    D(0)      = 1.0000000000 x 0.0000708609 = 0.0000708609
    claims_death   = max(0, 100,000,000 - 0) x 0.0000708609 = 7,086.09
    claim_expenses = 300,000 x 0.0000708609 = 21.26
    V(1)  = ( (0.0000 + 179,777.0581) x 1.0020598363 - 0.0000708609 x 1e8 )
            / (1 - 0.0000708609) = 173,073.5392
    SC(1) = 3,106,700.5378 x (1 - 1/84) = 3,069,716.0076
    W(1)  = max(0, 173,073.5392 - 3,069,716.0076) = 0.0000
    CV(1) = 0.50 x 0.0000 = 0.0000
    survivors of mortality = 1.0000000000 x (1 - 0.0000708609) = 0.9999291390562
    S(0)  = 0.9999291390562 x 0.0087416110 = 0.0087409915159
    claims_lapse   = 0.0000 x 0.0087409915159 = 0.00
    expenses  = 5,000 x 1.0000 x 1.0000000000 = 5,000.00
              + (3,106,700.5378 - 2,019,355.3496) = 1,087,345.1882   (acquisition)
              + 0.02 x 231,345.0000 = 4,626.90
                                             = 1,096,972.09
    commissions = min(0.65 x 3,106,700.5378, 1.00 x 2,776,140.00) = 2,019,355.35
    CF(0) = 231,345.00 - 7,086.09 - 0.00 - 21.26 - 1,096,972.09 - 2,019,355.35 = -2,892,089.79
    l(1)  = 0.9999291390562 x (1 - 0.0087416110) = 0.9911881475403

The first month is the only negative one before 완납, and the reason is distributional:
**₩3,106,700.54 of acquisition cost against ₩231,345.00 of premium.** The commission cap of
제4-32조제5항 does not bind — 0.65 × the cost is ₩2,019,355.35, inside the first year's
expected premium of ₩2,776,140 — and the residual ₩1,087,345.19 is booked as acquisition
expense. The surrender value is nil, so the first month's lapse costs nothing in cash:
**the first-year lapse benefit is zero by construction, on the suppressed and the standard
form alike.**

The strain is ₩2,892,089.79, **12.5 times the month's premium**. An annual step netted the
same charge against a whole year's premium and printed ₩531,338, which is a true statement
about a year and not about the cash flow that happens at issue.

**Trace, month `t = 1` — the first ordinary month.**

    l(1) = 0.9911881475,  q^m(1) = 0.0000708609,  w^m(1) = 0.0087416110
    premiums   = 231,345.00 x 0.9911881475 = 229,306.42
    D(1)      = 0.9911881475 x 0.0000708609 = 0.0000702365
    claims_death   = max(0, 100,000,000 - 0) x 0.0000702365 = 7,023.65
    claim_expenses = 300,000 x 0.0000702365 = 21.07
    V(2)  = ( (173,073.5392 + 179,777.0581) x 1.0020598363 - 0.0000708609 x 1e8 )
            / (1 - 0.0000708609) = 346,515.8719
    SC(2) = 3,106,700.5378 x (1 - 2/84) = 3,032,731.4774
    W(2)  = max(0, 346,515.8719 - 3,032,731.4774) = 0.0000
    CV(2) = 0.50 x 0.0000 = 0.0000
    survivors of mortality = 0.9911881475 x (1 - 0.0000708609) = 0.9911179110127
    S(1)  = 0.9911179110127 x 0.0087416110 = 0.0086639671883
    claims_lapse   = 0.0000 x 0.0086639671883 = 0.00
    expenses  = 5,000 x 1.0000 x 0.9911881475 = 4,955.94
              + 0.02 x 229,306.4220 = 4,586.13
                                             = 9,542.07
    commissions = 0.00
    CF(1) = 229,306.42 - 7,023.65 - 0.00 - 21.07 - 9,542.07 - 0.00 = 212,719.63
    l(2)  = 0.9911179110127 x (1 - 0.0087416110) = 0.9824539438244

Nothing is exceptional in this row and that is what it is for: one month's premium, one
month's decrements, one month's maintenance expense and **no commission at all**, the
renewal commission being a policy-year-2 charge that starts at `t = 12`. The account has
still not overtaken the unamortised 해약공제액, so the surrender value is nil and the
month's lapses cost nothing.

**Trace, month `t = 12` — the 계약해당일 closing policy year 1.**

    l(12) = 0.8992350000,  q^m(12) = 0.0000774863,  w^m(12) = 0.0067873987
    premiums   = 231,345.00 x 0.8992350000 = 208,033.52
    D(12)      = 0.8992350000 x 0.0000774863 = 0.0000696784
    claims_death   = max(0, 100,000,000 - 0) x 0.0000696784 = 6,967.84
    claim_expenses = 300,000 x 0.0000696784 = 20.90
    V(13)  = ( (2,101,396.5549 + 179,777.0581) x 1.0020598363 - 0.0000774863 x 1e8 )
            / (1 - 0.0000774863) = 2,278,300.3596
    SC(13) = 3,106,700.5378 x (1 - 13/84) = 2,625,901.6451
    W(13)  = max(0, 2,278,300.3596 - 2,625,901.6451) = 0.0000
    CV(13) = 0.50 x 0.0000 = 0.0000
    survivors of mortality = 0.8992350000 x (1 - 0.0000774863) = 0.8991653215643
    S(12)  = 0.8991653215643 x 0.0067873987 = 0.0061029935543
    claims_lapse   = 0.0000 x 0.0061029935543 = 0.00
    expenses  = 5,000 x 1.0200 x 0.8992350000 = 4,586.10
              + 0.02 x 208,033.5211 = 4,160.67
                                             = 8,746.77
    commissions = 0.03 x 208,033.5211 = 6,241.01
    CF(12) = 208,033.52 - 6,967.84 - 0.00 - 20.90 - 8,746.77 - 6,241.01 = 186,057.00
    l(13)  = 0.8991653215643 x (1 - 0.0067873987) = 0.8930623280099

Three things move on this row and on no other: the attained 보험나이 turns 41 and with it
the annual `q`, the expense inflation factor makes its first step to 1.02, and the renewal
commission starts at 3% of the month's premium. On an annual grid all three were simply
"year 2"; here each is a date.

`l(12) = 0.899235` is the annual-step model's own `l(1)` **to the last bit**: twelve monthly
exits at `1 − (1 − q)^(1/12)` compound to the year's annual rate exactly, so the 계약해당일
survivorship is unchanged and only the exposure inside the year has moved.

**Trace, month `t = 239` (the last paying month) — the cliff.**

    l(239) = 0.5948434384,  q^m(239) = 0.0003875960,  w^m(239) = 0.0000833716
    premiums   = 231,345.00 x 0.5948434384 = 137,614.06
    D(239)      = 0.5948434384 x 0.0003875960 = 0.0002305590
    claims_death   = max(0, 100,000,000 - 0) x 0.0002305590 = 23,055.90
    claim_expenses = 300,000 x 0.0002305590 = 69.17
    V(240)  = ( (51,755,813.0357 + 179,777.0581) x 1.0020598363 - 0.0003875960 x 1e8 )
            / (1 - 0.0003875960) = 52,023,973.5884
    SC(240) = 0.00   (d >= 12 n_sc = 84)
    W(240)  = max(0, 52,023,973.5884 - 0.0000) = 52,023,973.5884
    CV(240) = 1.00 x 52,023,973.5884 = 52,023,973.5884
    survivors of mortality = 0.5948434384 x (1 - 0.0003875960) = 0.5946128794463
    S(239)  = 0.5946128794463 x 0.0000833716 = 0.0000495737987
    claims_lapse   = 52,023,973.5884 x 0.0000495737987 = 2,579.03
    expenses  = 5,000 x 1.4568 x 0.5948434384 = 4,332.87
              + 0.02 x 137,614.0553 = 2,752.28
                                             = 7,085.15
    commissions = 0.03 x 137,614.0553 = 4,128.42
    CF(239) = 137,614.06 - 23,055.90 - 2,579.03 - 69.17 - 7,085.15 - 4,128.42 = 100,696.39
    l(240)  = 0.5946128794463 x (1 - 0.0000833716) = 0.5945633056476

**The ratio the implementation must reproduce exactly is `CV(240) / CVs(240) = 2.0`**,
i.e. `1 / k`. Both quantities exist at the month-end `d = 240` and the model publishes both.
The [std] ordering rule pays the surrenders of the last paying month on the **full** value;
paying them on ₩26,011,986.79 instead would halve `claims_lapse` in that row.

The monthly grid is what makes the step legible for what it is. `cv_std_pp` moves from
₩51,755,813.04 to ₩52,023,973.59 across the boundary — **one month's accrual, 0.5%** —
against a payable value that doubles. An annual step compared the doubling against a 6.5%
year, and a reader could still wonder whether some of the step was growth.

**Trace, month `t = 240` — the first premium-free month, and where the stream turns.**

    l(240) = 0.5945633056,  q^m(240) = 0.0004239036,  w^m(240) = 0.0006691237
    premiums   = 231,345.00 x 0.5945633056 = 0.00
    D(240)      = 0.5945633056 x 0.0004239036 = 0.0002520375
    claims_death   = max(0, 100,000,000 - 0) x 0.0002520375 = 25,203.75
    claim_expenses = 300,000 x 0.0002520375 = 75.61
    V(241)  = ( (52,023,973.5884 + 0.0000) x 1.0020598363 - 0.0004239036 x 1e8 )
            / (1 - 0.0004239036) = 52,110,834.0667
    SC(241) = 0.00   (d >= 12 n_sc = 84)
    W(241)  = max(0, 52,110,834.0667 - 0.0000) = 52,110,834.0667
    CV(241) = 1.00 x 52,110,834.0667 = 52,110,834.0667
    survivors of mortality = 0.5945633056 x (1 - 0.0004239036) = 0.5943112681279
    S(240)  = 0.5943112681279 x 0.0006691237 = 0.0003976677418
    claims_lapse   = 52,110,834.0667 x 0.0003976677418 = 20,722.80
    expenses  = 5,000 x 1.4859 x 0.5945633056 = 4,417.45
                                             = 4,417.45
    commissions = 0.00
    CF(240) = 0.00 - 25,203.75 - 20,722.80 - 75.61 - 4,417.45 - 0.00 = -50,419.61
    l(241)  = 0.5943112681279 x (1 - 0.0006691237) = 0.5939136003861

**Premiums stop at `12m` and nothing else does.** In one row the income line goes from
₩137,614.06 to zero, commission from ₩4,128.42 to zero, and every outgo continues:
maintenance expense for life, death claims for life, surrender benefits for life on a value
that is still growing. `net_cf` swings by **₩151,116.00** between `t = 239` and `t = 240` —
a month either side, where the annual grid's ₩1,819,705.57 compared two whole years — and is
negative in every one of the remaining 671 months. A projection that ends at 납입완료 misses
the entire liability.

Surrender outgo is **eight times** the previous month's, because the annual rate returned
from its 0.1% convergence point to the 0.8% ultimate against a value that has just doubled.
### Undiscounted totals per policy issued, `t = 0 … 911`

| Column | Total |
|---|---|
| `pols_if` | 338.873413 |
| `premiums` | 37,680,384.400292 |
| `claims_death` | 50,620,740.892497 |
| `claims_lapse` | 9,294,573.995749 |
| `claims_reduction` | 0.000000 |
| `claim_expenses` | 151,862.222677 |
| `expenses` | 4,604,344.667170 |
| `commissions` | 3,070,402.823829 |
| **`net_cf`** | **−30,061,540.201631** |

**Roll-forward check.** Over the full 912 months `Σ D(t) = 0.5062074089` and
`Σ S(t) = 0.4937925911`, summing to **1.0000000000** with `l(912) = 0`; every policy leaves
by one of the two decrements because the table terminates. `pols_if` sums to **338.873413**
policy-months of exposure — 28.24 policy-years, against the annual grid's 28.70, because the
monthly step stops counting a whole year of exposure for a life that leaves in its first
month. All nine `check_*()` cells return `True`.

**Against the annual grid this replaced.** Premium income falls 1.37%, from ₩38,202,010.27,
which is the whole of the change and is not a rounding: an annual step collected a full
year's premium from lives that died or lapsed during the year. Death claims fall 0.38% with
it, by less, because the benefit is now paid in the month of death rather than a year later
on a cohort thinned in between. `net_cf` is 0.88% more negative. The **in-force at every
계약해당일 is unchanged** to a relative 1.1e-14, which is the statement that the change of
grid re-timed the exposure and left the survivorship the sourced annual rates imply.

### Reading the shape of the result

`net_cf` is **income-positive**, so the total of **−₩30,061,540.20** says outgo exceeds
income by ₩30.1m per policy issued over 76 undiscounted years. **That is the expected shape
of a whole-life stream and not a defect.** The contract must eventually pay ₩100,000,000 to
someone: expected death claims of ₩50.62m plus surrender benefits of ₩9.29m come to
₩59.92m of benefit against ₩37.68m of premium, and the ₩22.23m gap is closed by nothing in
this model, because everything that closes it — the investment return on the account,
discounting, the CSM — belongs to a layer this projection deliberately stops before. There
is no `liability_cf`.

Four features of the stream are worth reading off directly. **The liability is back-ended
even by whole-life standards:** 69.6% of expected death claims — 0.352136 of 0.506207 —
fall from `t = 480` on, when the insured is over 79 and has paid no premium for twenty
years. **The premium-paying period is profitable and the rest is not:** `Σ net_cf` over
`t = 0 … 239` is **+₩27,631,707.90** and over `t = 240 … 911` is **−₩57,693,248.10**. **The
surrender benefit is small relative to the death benefit** — ₩9.29m against ₩50.62m —
because the `loglinear` lapse vector empties out long before the value is large; on the
`flat` basis the same product pays ₩23.29m of surrender benefit and only ₩17.70m of death
claims, which is a different product economically on the same contract. And **expenses are
dominated by the first month**: ₩1,096,972.09 of the ₩4,604,344.67 total, 23.8% of the
lifetime expense in a single month — which is what the 표준해약공제액 exists to bound, and
which the monthly grid states as the one-row cliff it is.

### Calibration against the published grid

The model's 표준형 surrender value `cv_std_pp(d)` against DB생명's published 1종 표준형 grid
at the identical cell — 남 40세, 1억원, 20년납, 월납 [S4]. A published grid quotes a
**policy year**, so this table is keyed by the year and the model is read at the 계약해당일
`d = 12y`:

| policy year | model `cv_std_pp(12y)` | published 해지환급금 | model / published |
|---|---|---|---|
| 1 | 0.00 | 0 | — (both nil) |
| 3 | 4,669,528.91 | 5,087,095 | 0.9179 |
| 5 | 10,093,729.24 | 10,940,547 | 0.9226 |
| 10 | 23,216,376.79 | 25,283,000 | 0.9183 |
| 15 | 36,836,090.86 | 40,501,000 | 0.9095 |
| 20 | 52,023,973.59 | 57,838,000 | 0.8995 |
| 40 | 74,269,001.52 | 86,326,000 | 0.8603 |
| 60 | 92,405,944.03 | 104,604,000 | 0.8834 |

**The monthly account improves the fit at every sourced duration**, by the same 1.2% it
raises the whole account. That is not a coincidence and it is worth naming: the published
grid is a real Korean contract, whose own 계약자적립액 accrues **monthly** as
제7-66조제1항제4호 requires, and the annual grid was reading it with an annual account.

**Durations 3 to 20 sit in a 0.899–0.923 band** — a level offset, not a shape error — and
the first year is nil in both, which is the surrender charge biting exactly as 별표 14
bounds it. The offset is what a construction that sets 계약체결비용 **at** the statutory cap
should produce against a real product that presumably charges less: a higher deduction and a
slightly lower value at every duration.

**The widening past duration 20 has a stated cause and is not a fit failure.** The [S4]
product carries a **전환나이 60세** step-up in its death benefit, so its late-duration values
belong to a **rising** benefit the 평준형 composite does not have. The tell is in the grid
itself: its duration-60 value of ₩104,604,000 **exceeds the ₩100,000,000 sum assured**,
which a level whole-life account cannot do. The table records the divergence rather than
tuning the model to close it.

### The `flat` basis, and the disclosure the guidance obliges

Re-running the identical cell with `lapse_basis = flat` — 4.0% level, the comparison basis
the November 2024 decision requires an insurer to disclose against the 원칙모형 [REG-R27] —
changes the product:

| Quantity | `loglinear` (base) | `flat` |
|---|---|---|
| `lapse_rate(228)` / `(239)` / `(240)` | 0.0012742750 / 0.0010000000 / 0.0080000000 | 0.04 / 0.04 / 0.04 |
| `claims_lapse(228)` | 1,223.61 | 36,851.71 |
| `claims_lapse(239)` | **2,579.03** | **74,889.03** |
| `claims_lapse(240)` | 20,722.80 | 74,727.62 |
| `net_cf(239)` | **+100,696.39** | **−1,267.84** |
| `pols_if(239)` | 0.594843 | 0.424042 |
| `Σ claims_lapse` | 9,294,573.996 | 23,294,606.96 |
| `Σ claims_death` | 50,620,740.892 | 17,702,650.52 |
| `Σ net_cf` | −30,061,540.20 | −10,160,522.69 |

**The cliff moves far less cash than a reader expects on the base vector, and that is the
finding.** On the `loglinear` basis the payable value doubles at the month-end `d = 240` but
the annual lapse rate of the month closing there, `t = 239`, is **0.1%**, so `claims_lapse`
is only ₩2,579.03 — against ₩1,223.61 eleven months earlier and ₩20,722.80 the month after,
when the rate returns to 0.8% against a value that has already doubled. **The step is in the
value, and the cash the step moves is set by the rate the supervisor fixed.** On the `flat`
basis the same step lands on a 4% annual rate and turns the last paying month **negative**:
`net_cf(239)` falls from **+₩100,696.39** to **−₩1,267.84**, so the best month of the
projection becomes a loss-making one. That contrast **is** the disclosure the guidance
obliges [REG-R27], and it is the reason the base vector is not a free choice for a Korean
insurer.

One second-order effect is worth naming because a reader may misread the headline. The
`flat` run's undiscounted `net_cf` is **better** — −₩10.16m against −₩30.06m — but only
because a 4% lapse rate empties the book before the expensive years: `Σ claims_death` falls
by 65.0%. A high lapse rate looks profitable undiscounted on a product whose 환급률 has not
yet crossed 1, and the sign reverses once the value exceeds premiums paid — which is exactly
why the K-ICS 대량해지위험 shock splits by whether surrender **reduces or increases** net
assets [REG-R36] [R7].

### The other nine model points, and what each one is for

| # | Cell | What it demonstrates | Signature number |
|---|---|---|---|
| 1 | M40, 1억, 20년납, `k = 0.50` | the anchor | cliff ratio exactly **2.0** at the month-end `d = 240` |
| 2 | M40, 1억, 20년납, `k = 1.00` | the 표준형 comparison twin | 환급률 crosses 100% at **`d = 347`** against the anchor's 280, on the identical account |
| 3 | M40, 1억, 20년납, `k = 0.00`, loan in policy year 10 | 무해지 + **the loan that cannot exist** | `cv_pp(239) = 0.0`; `loan_draw(108) = 0.0` |
| 4 | F30, 5,000만, 30년납, `k = 0.50` | female, long pay, the long horizon | `proj_len() = 1032` |
| 5 | M65, 1,000만, **전기납**, `k = 0.50` | no 납입완료, so **no cliff at all** | `cv_mult(d) = 0.5` for life |
| 6 | M40, 1억, 20년납, `k = 0.50`, loan in policy year 10 | the loan on a suppressed value | `loan_draw(108) = 8,265,310.25`; the balance passes `SA` at `d = 871` — the seventh month of policy year 73 — so every payment floors at zero from there |
| 7 | M45, 1억, 20년납, waiver 0.4% p.a. | 납입면제 as a **state** | `pols_waived(240) = 0.044660` |
| 8 | M40, 1억, **7년납**, bonus 13.8% | 단기납 유지보너스 + the mandatory spike | `lapse_rate_mth(83) = 0.300083` in **one month** and nowhere else; 환급률 0.972448 at 완납 |
| 9 | F45, 1억, 20년납, **금리연동형** 2.75% | the declared-rate account | `pol_val_pp(240)` runs **9.12%** above its prospective form |
| 10 | M50, **10억**, 10년납, `k = 0.30`, 감액 in policy year 15, 부활 20%, `flat` lapse, `mort_be_factor` 0.90 | 감액 + 부활 + the level basis + the SA ceiling | `claims_reduction(179) = 165,583,123.99`; `net_cf(179) = −166,799,687.05` |

Point 3 is the one to read next after the anchor. On a **무해지** contract the payable
value is zero throughout 납입기간, so the policy loan the point elects **draws exactly
nothing** — `loan_util = 1.0`, `loan_draw(108) = 0.0` — which is the FSS's 2019 consumer
alert reproduced as arithmetic [R4] [REG-R28]. At `d = 240` the value steps from zero to the
full ₩52,023,973.59 and the 환급률 to **1.081135**, above the 표준형 twin's 0.843286:
제7-66조제4항제2호 나목 is the article that permits it [REG-R19].

---

## Valuation and reserve pointers

This library projects gross liability cash flows. Every valuation layer consumes them and is
cited, never reproduced. Korea is the only market in this repository running **three** of
them at once.

- **IFRS 17 — K-IFRS 제1117호, mandatory since 2023-01-01**, not voluntary as in Japan
  [REG-R60]. The liability is fulfilment cash flows plus a risk adjustment plus the CSM,
  discounted on a 국고채-based curve with 관찰금리 to a **20-year** last observable maturity
  extending to 30 years over three years from 2025, an LTFR of **4.55%** and a liquidity
  premium of **91bp**, and **every assumption is re-set at every reporting date** [REG-R27]
  [REG-R60]. `result_cf()` is the fulfilment-cash-flow engine and nothing more; `v(t)`, the
  risk adjustment and the CSM roll-forward are out of scope. **This product is the reason
  the November 2024 계리가정 decision exists**: the supervisor's own framing — 「무·저해지
  상품은 납입기간 중 해지 시 환급금이 없거나 적은 상품임에도 완납 직전까지 해지가
  발생한다고 가정하여 …」 — is a description of this contract's economics [REG-R27] [R7].
- **K-ICS** — the 신지급여력제도, live in the same quarter. 요구자본 comes from five risk
  modules, of which the life module alone carries seven shock-based sub-risks including
  **해지위험액** and **사업비위험액**; the floor is **100%** and the 적기시정조치 ladder
  starts below it [REG-R13] [REG-R14]; the industry ratio after 경과조치 at 2025-09-30 was
  **210.8%** overall and **201.4%** for life insurers [REG-R30]. The 대량해지위험 shock bears
  directly on this product's design: it splits by whether surrender
  **reduces or increases** net assets, adding **+35%p** or **+25%p** to the next year's lapse
  rate on 순자산 감소상품 and applying **× (1 − 40%)** on 순자산 증가상품, against a flat 25%
  (보장성) or 35% (저축성) mass-lapse on the 표준형 [REG-R36] [R7]. **Those figures come from
  시행세칙 별표 22, which was not retrieved**, so they are second-hand and **[unverified] as
  regulatory text** [REG-R26] [REG-R36] — a gap that matters most to exactly this product,
  whose 고환급형 forms are what the test is about.
- **해약환급금준비금 — Korea's own, with no counterpart anywhere else in this repository.**
  At every balance-sheet date the insurer compares, company-wide, the IFRS 17 잔여보장요소
  against the aggregate contractual 해약환급금 **computed under 제7-66조제1항 — on that rule
  even for the 제7-66조제4항 products that may contractually pay less** — and appropriates
  the shortfall inside 이익잉여금 [REG-R11]. **So a 무해지 contract whose contractual
  surrender value is zero still enters the test at its 별표-14-floored value.** The reserve
  stood at **₩23.7조 at end-2022 and ₩32.2조 at end-2023** [REG-R36] [R7] and is graded by
  K-ICS ratio, a well-capitalised insurer appropriating only **80%** [REG-R11].
  `WholeLife_KR_S` does not compute it; it is named because it is why a Korean insurer's
  economics here depend on the **surrender value**, and because `cv_std_pp(t)` is precisely
  the quantity the test needs.
- **책임준비금.** 보험업법 제120조 delegates the mechanics entirely [REG-R3], and 감독규정
  제6-11조 **delegates the calculation to the FSS Governor** — ten paragraphs of the pre-2023
  article, which carried accumulation rules, having been deleted on 2022-12-21 [REG-R10].
  That deletion is the visible trace of the switch from a locked-in statutory reserve to a
  current-estimate one, and it is why **`pol_val_pp` here is a 계약자적립액 and not a
  reserve**. The same drift shows in the product documents — a pre-2023 상품요약서 writes
  「순보험료식 책임준비금에서 해지공제액을 공제한 금액」 and a 2024 one 「계약자적립액에서
  미상각신계약비를 공제한 금액」 for the identical identity [S2] [S8] — and in the renaming of
  the filing from 「보험료 및 **책임준비금** 산출방법서」 to 「보험료 및 **해약환급금**
  산출방법서」 between the 2023 and 2026 editions [REG-R9]. The *causal* reading is
  **[unverified]**; the wording change is sourced twice.
- **The 산출방법서, and why no further research fixes the pricing basis.** 보험업법
  제5조제3호 names the 기초서류, and the 산출방법서 — where the 예정이율, the 적용위험률, the
  예정사업비율 and the surrender-value formula actually live — is **not published** [REG-R2];
  감독규정 제7-64조 lists its five 필수기재사항, the third being the 해약환급금 calculation
  and, where 계약체결비용 exceeds the 표준해약공제액 at the 기준연령 요건, a comparison of the
  two [REG-R18]. **No amount of further research converts an expense or pricing parameter in
  this document into a sourced value**; what research can do, and did, is bound them by
  published caps and published cash values. The 선임계리사 who verifies the 기초서류 is,
  since 2022, barred from product development and from the CEO and CFO roles — a harder
  separation of pricing from sign-off than the UK Chief Actuary split [REG-R5].
- **Disclosure, not valuation, but binding on the model's outputs.** 제7-45조제7항 requires
  a 보장성보험 to publish a **보험가격지수** and a 보장범위지수 [REG-R22] — how a Korean
  consumer sees the price of a product whose pricing basis is confidential; the two observed
  at this cell are **85.4% / 86.2%** and **110.3% / 110.9%** [S2] [S8]. And the 무(저)해지
  form drew an FSS **소비자경보** in 2019, warning that it is unsuitable as savings and
  **cannot support a policy loan during the payment period** [R4] [REG-R28] — which is why
  `point_id = 3` exists.

---

## Key sensitivities and model risks

In rough order of leverage on this product:

1. **The lapse vector, and it is not close.** It is the assumption the supervisor took away
   from insurers on exactly this product [REG-R27] [R3], and switching the anchor from
   `loglinear` to `flat` moves undiscounted `net_cf` from **−₩30,061,540.20 to
   −₩10,160,522.69**, expected death claims from ₩50.62m to ₩17.70m and surrender benefits
   from ₩9.29m to ₩23.29m. Two of those move in opposite directions, so no single-signed
   intuition survives. The shape between the two regulatory endpoints is **[std]** and no
   Korean lapse curve by duration is public.
2. **The suppression factor `k` and where the cliff falls.** `k` is a model point column and
   the market runs 0.00 / 0.30 / 0.50 / 1.00 [S1] [S4] [S6] [S7] [S8]. **Where the cliff
   falls is not universal**: at 납입완료 on three of the five observed designs, at **seven
   years** on a formula design whose payment period runs to twenty [S2], and at **납입기간 +
   3년** on a third [S3]. The composite hard-codes 납입완료 and a model reproducing another
   carrier must expose that date as a parameter.
3. **The expense and acquisition-cost block.** `AC = SC*`, `c₀ = 0.65`, `c_r = 3.0%`,
   ₩5,000 a **month** + 2.0% of premium, ₩300,000 a claim, 2.0% inflation stepping at the
   계약해당일 — **every one [std], because no Korean expense rate as a percentage of premium
   was obtained from any source.** `expenses` and `commissions` together total ₩7,674,747.49
   of the ₩37.68m premium stream, 20.4%, and the first **month** alone is ₩3,116,327.44 of
   it; the ₩300,000-a-claim handling expense is a further ₩151,862.22, published in its own
   column, which takes the block to ₩7,826,609.71 and 20.8%. The four public bounds in class (b) constrain it; nothing
   fixes it.
4. **The mortality table is a construction and `mort_be_factor` is the lever.** Every row of
   `mort_table.csv` is [std]; the two disclosed carrier grids differ by **up to 24%** and
   bracket rather than fix a level [S2] [S8]; and the 제10회 경험생명표 is not published
   [REG-R33] [REG-R34]. Claims move proportionately with `mort_be_factor`, and on a 76-year
   run they are the largest single outgo at ₩50.62m.
5. **The 보험나이 / 만나이 gap.** No conversion is applied and none is public. The table is
   read about half a year of ageing too young, systematically, which understates `q` by
   roughly 4.6% at the ages that matter most on this cell. It is a **one-directional** bias
   and it is not corrected.
6. **The horizon itself.** ω = 115 is [std]. **69.6% of expected death claims fall from
   `t = 480` on**, so any truncation of the projection is a direct and large understatement,
   and moving ω moves the tail rather than the shape.
7. **The 예정이율, and the account's sensitivity to it.** 2.50% is the [std] centre of a
   sourced 2.25%–2.75% band [S1] [S2] [S5] [S6] [S7] [S8]. It enters **twice** — through `P`
   (equivalence) and through the accrual — so it moves the surrender value in the same
   direction from both ends, and the 환급률 crossing date with it. A market-wide 예정이율 cut
   in 2025 and again for 2026 was reported in search results and **could not be confirmed
   against any retrieved carrier document** [unverified]; the 평균공시이율 series that *is*
   sourced fell from 2.75% to **2.50%** for 2026, its first fall since the 2.50% → 2.25%
   step in 2021 [S10] [REG-R48].
8. **Expense inflation over 76 years.** 2.0% **[std]** compounds to a factor of **4.42**;
   a UK or US habit of 3% would compound to 9.18. No published Korean expense basis anchors
   either. **부활 is likewise not modelled**, so later-duration in force is understated —
   Korean lapse is genuinely non-terminal, including on a 무해지 contract where there was no
   value to draw [S5 제26조] [REG-R25 제27조](#krlib-reg-r25).
9. **The absence of an APL is [unverified].** If a 자동대출납입 article is found in the
   생명보험 표준약관 in a later research pass, the lapse mechanics of this chassis change
   **in kind**: lapse becomes a funded event with a continuation test, as in `jplib`, and
   every suppressed-form conclusion about who reaches 납입완료 has to be re-derived.

### Known modeling pitfalls

The mistakes a modeller would actually make on this product. Each is specific and checkable,
and each is either asserted by a `check_*()` cells or by a test in
`tests/test_whole_life_kr.py`.

- **The cliff is a step, not a ramp.** `CV(d) = k W(d)` for `d < 12m` and `W(d)` for
  `d ≥ 12m`, with `CV(12m) / (k W(12m))` exactly `1 / k` — **2.0 on the anchor at the
  month-end `d = 240`**, against ₩25,877,906.52 one month earlier
  [S1] [S4] [S6]
  [S8]. Interpolating, grading or smoothing across the boundary is wrong. So is assuming the
  step always exists: on a **전기납** point `m` is the whole projection, `cv_mult(d) = k` for
  life, and the cliff never happens (`point_id = 5`).
- **Off-by-one at the boundary.** Surrenders in the last paying month — `t = 12m − 1` —
  are paid on the **full** value; the suppressed value applies to the month-ends
  `d = 1 … 12m − 1` **[std]**. Both quantities exist at
  `d = 12m` — ₩52,023,973.59 and ₩26,011,986.79 — and the model publishes both as `cv_pp` and
  `cv_susp_pp`. A model that loses either cannot state the ordering rule it is using. On the
  monthly grid the off-by-one costs one **month**, where on an annual grid it cost a year.
- **One policy value, one multiplier.** The suppression is a pure haircut on a **common**
  underlying account: at 납입완료 the suppressed and 표준형 values are **identical to the
  won** in every published grid [S1] [S4] [S6]. Running two account recursions, or deriving
  the suppressed form's value from the suppressed form's own premium, is wrong — and it is
  wrong in a way that destroys the product's economics, because `CV(d)` being independent of
  the sold premium is the **whole** of the refund-ratio argument.
- **The step is not the surrender charge running off.** The 해약공제기간 is capped at **7년**
  by 제7-66조제1항제2호 [REG-R19], so on the anchor's 20년납 contract `surr_chg_pp(d) = 0`
  from `d = 84` — **thirteen years before the cliff**. Attributing the step to amortisation,
  or grading the charge to `12m` instead of to `12 min(m, 7)`, is a common and detectable
  error:
  `check_surr_chg_cap()` fails on it.
- **`P` and `P₂₀` are different annuities.** 별표 14 주3 recomputes the 연납순보험료 on a
  **20년납** footing for a 보험기간 of 20 years or more [REG-R20]. They coincide only when
  `m = 20`, which the anchor satisfies — so a model tested **only** on the anchor will not
  catch the confusion. Test it on the 7년납 and 10년납 points, where reusing `P` in the cap
  formula overstates the statutory surrender charge.
- **The 보험가입금액 entering the cap is taken before any 체증 or 체감** [REG-R21 별표 15
  제8호](#krlib-reg-r21), and is the 일반사망보험금 for a 보장성보험 covering 일반사망 [REG-R21 제3호](#krlib-reg-r21). On a
  design with a 전환나이 step this is not the benefit in force at duration `d`.
- **Premiums stop at `12m`; nothing else does.** At `t = 240` premium and renewal
  commission go
  to zero in the same row while maintenance expense, death claims and surrender benefits all
  continue for life. `net_cf` swings by **₩151,116.00** across that boundary — a month either
  side, where the annual grid compared two whole years and printed ₩1,819,705.57 — and is
  negative in all 672 remaining months. A projection that stops at 납입완료, or that keeps
  charging renewal commission past it, misses the majority of the liability. So does one that
  keeps the premium-related expense running on zero premium.
- **The policy loan does not exist on a 무해지 contract during 납입기간.** There is no value
  to lend against, so `loan_draw` must be **exactly zero** even at `loan_util = 1.0` — which
  is `point_id = 3` [R4] [REG-R28] [REG-R25 제33조](#krlib-reg-r25). A model that computes the limit off
  `cv_std_pp` instead of `cv_pp` lends against a value the policyholder cannot claim, and on
  a 저해지 contract lends exactly twice too much.
- **Everything is floored at zero, and on this product the floor bites.** `W(d) =
  max(0, V(d) − SC(d))` is zero at `d = 1` on the anchor; the death benefit `SA(t) − L(t)`
  and the surrender payout `CV(t+1) − L(t)` both go negative once an unrepaid loan outgrows
  the value, which happens on `point_id = 6` at the month-end `d = 871` — the seventh month
  of policy year 73, a date an annual grid could only place in a year — where the balance exceeds the
  ₩100,000,000 sum assured. None of the three may produce a negative payment.
- **Booking the 유지보너스 without the mandatory lapse spike.** The supervisor requires an
  **additional lapse of at least 30%** at any bonus date [REG-R27] [R3]; on `point_id = 8`
  that takes `lapse_rate_mth(83)` — the single month the bonus is credited in — from 0.000083
  to **0.300083**. The spike is **not** converted to a monthly force and must not be: it is a
  lump of exits on a date, so it is added to that one month and spread over no others.
  Turning the bonus on alone misstates
  the liability in the insurer's favour, which is precisely what the guidance exists to
  prevent. `lapse_spike()` is wired to `bonus_rate()` so the pair cannot be separated by
  accident.
- **The prospective identity does not hold on a 금리연동형 point.** Once the crediting rate
  differs from the pricing rate the account is path-dependent: on `point_id = 9`
  `pol_val_pp(240)` runs **9.12% above** `prosp_val_pp(240)`. `check_pol_val_prosp()` is
  defined as zero there rather than asserted. Asserting it unconditionally fails; "fixing" it
  by discounting the account on the pricing rate silently changes the product.
- **`pol_val_pp` is a 계약자적립액, not a reserve, and never a cash flow.** Under K-IFRS
  제1117호 the insurer books no 보험료적립금 [REG-R60] [REG-R10], and the model computes no
  책임준비금, no CSM, no 요구자본 and no 해약환급금준비금. None of `pol_val_pp`, `cv_std_pp`
  or `cv_pp` may be read as a reserve or appear in `net_cf`.
- **Waived premiums count as paid, and a waived policy is a state.** 「보험료가 … 정상적으로
  납입된 것으로 하여 사망보험금 및 해지환급금을 계산합니다」 [S2] [S3] [S8]. Modelling the
  waiver by scaling the premium down, or by suppressing the account accrual, breaks the one
  route to the cliff the policyholder does not have to fund. The premium is weighted by the
  paying cohort and everything else by the whole in-force count; the two are equal in the
  base run, so an implementation that weights premium by `pols_if(t)` reproduces this worked
  example exactly and fails only once the waiver module is switched on.
- **Lapse is behavioural in Korea, not funded.** There is **no 자동대출납입** in any
  retrieved Korean document [S5] [REG-R25], so no continuation test precedes the decrement
  and a policyholder who misses fourteen days loses the contract whatever its cash value.
  Importing `jplib`'s APL machinery models a mechanic Korea has not been shown to have — and
  the reverse import is just as wrong: `jplib`'s lapse rate applied without the APL test
  models a decrement **that** contract does not have.
- **감액완납 and 연장정기보험 are not Korean features on this evidence.** Neither appears in
  the 60-article 약관 or in any 상품요약서 in the set [S5], and both are **[unverified]**
  rather than established. A reader arriving from `jplib` — where 払済保険 and 延長定期保険
  are both in the 約款 — will reach for them. What Korea offers in that slot is **감액**, a
  partial surrender paying `k W(d)` during 납입기간 and nothing at all on a 무해지 contract
  [S5 제20조].
- **A refused claim is not a zero payment.** 상법 제736조 obliges the insurer to pay 「보험
  수익자를 위하여 적립한 금액」, in practice the 계약자적립액 [REG-R50] [REG-R25 제22조](#krlib-reg-r25).
  Modelling an exclusion as forfeiture overstates the insurer's position by the account, not
  by the claim. The composite carries no exclusion incidence, so nothing is deducted.
- **There is no 고도장해 benefit to add.** Korea puts no severe-disability acceleration at
  the sum assured on this chassis [S2] [S3] [S6] [S8]; the slot is filled by the premium
  waiver, which **continues** the contract instead of extinguishing it. Adding a disability
  decrement at `SA` — the Japanese habit — invents a benefit and double-counts a decrement.
- **The 환급률 test and the value test are not the same test.** `check_cv_cliff()` asserts
  that the payable **value** never exceeds the 표준형 twin's, which `k ≤ 1` guarantees. It
  does **not** assert the press-release framing 「전(全) 보험기간 동안 표준형 보험의 환급률
  이내로」 [REG-R28], because the denominators differ: on `point_id = 3` the 무해지 form's
  post-완납 환급률 is **1.081135** against the 표준형's **0.843286**, which satisfies
  제7-66조제4항제2호 나목 as recorded in the 고시 [REG-R19] and contradicts the press-release
  reading. Both statements are recorded as they stand and **neither is resolved here**; a
  model that asserts the press-release form will fail on a legal design.
- **Dividing an annual probability by twelve is not the monthly rate.** Every decrement on
  this chassis is tabulated as an **annual probability** and converted by
  `1 − (1 − q)^(1/12)`, so that twelve months compound back to exactly the year's figure.
  Dividing instead understates the early months and overstates the late ones, and on the
  `loglinear` lapse vector — which spans two orders of magnitude — the two conventions differ
  by 4.9% of the first year's rate. The one decrement that is **not** converted is the
  유지보너스 spike, because it is a date, not a rate; and the one that is **divided** is
  none of these — the sister model `LTC_KR_S` divides its transition intensities by twelve
  precisely because they are rates per year rather than probabilities.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R3]: #krlib-whole_life-r3
[R4]: #krlib-whole_life-r4
[R6]: #krlib-whole_life-r6
[R7]: #krlib-whole_life-r7
[R8]: #krlib-whole_life-r8
[REG-R10]: #krlib-reg-r10
[REG-R11]: #krlib-reg-r11
[REG-R12]: #krlib-reg-r12
[REG-R13]: #krlib-reg-r13
[REG-R14]: #krlib-reg-r14
[REG-R16]: #krlib-reg-r16
[REG-R18]: #krlib-reg-r18
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R22]: #krlib-reg-r22
[REG-R23]: #krlib-reg-r23
[REG-R25]: #krlib-reg-r25
[REG-R26]: #krlib-reg-r26
[REG-R27]: #krlib-reg-r27
[REG-R28]: #krlib-reg-r28
[REG-R29]: #krlib-reg-r29
[REG-R3]: #krlib-reg-r3
[REG-R30]: #krlib-reg-r30
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R36]: #krlib-reg-r36
[REG-R38]: #krlib-reg-r38
[REG-R4]: #krlib-reg-r4
[REG-R48]: #krlib-reg-r48
[REG-R5]: #krlib-reg-r5
[REG-R50]: #krlib-reg-r50
[REG-R51]: #krlib-reg-r51
[REG-R60]: #krlib-reg-r60
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
