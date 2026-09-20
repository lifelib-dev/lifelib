# Technical Notes

**Status:** Draft, 2026-09-03 (all cited sources accessed 2026-09-03).

**Scope note.** These notes turn the standardized composite of
[`product-spec.md`](product-spec.md) (same directory) into a reference liability cash-flow
projection on paper, and into `Term_KR_S` in fact. They describe no single insurer's
contract. [S#] and [R#] resolve against [`sources.md`](sources.md) in this directory,
numbering carried verbatim from `_research/term-life.md` and frozen; [REG-R#] resolves
against the cross-product library
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is distinct and
**must never be read across** — this product's [R9] and the library's [REG-R9] are
different documents. **[std]** marks a standardization
introduced for the reference implementation; [unverified] marks a claim that could not be
confirmed against a retrieved document.

**Every contractual parameter here is identical to `product-spec.md`'s.** What is new is
the assumption basis — a constructed mortality table and the best-estimate factor over it,
a lapse curve interpolated between disclosed endpoints, a renewal-decline rate, an expense
and commission structure, a shortened-pay equivalence and a premium scale beyond the
published cells. Korea publishes more of this than any other market in this repository:
the office premium at the anchor cell is a **published** figure appearing twice
independently [S12] [S4], the whole 갱신형 (*gaengsinhyeong*, renewable) premium ladder is
published [S7], the pricing lapse endpoints are published [S12] [S1] and their shape is
supervisory [REG-R27]. What is not published is the industry mortality table [REG-R33]
[REG-R34], the margin inside a carrier's 예정 경험사망률 [REG-R2], any expense or commission
rate [S1] [S6] [S8] [S10] [S11] [S12], and any renewal-decline rate for any Korean product
at all. Those are **[std]** with their rationale given where they are introduced.

**This is the library's protection chassis.** The decrement recursion, the premium
recursion, the processing order and the 갱신형 / 비갱신형 (*bi-gaengsinhyeong*,
non-renewable) split are specified here once. The
[critical illness technical notes (CI보험)](../ci_insurance/technical-notes.md) and the
[cancer technical notes (암보험)](../cancer/technical-notes.md) state only their deltas
against this file and do not restate the machinery. The savings machinery this product
deliberately does **not** carry — the 계약자적립액 (*gyeyakja jeongnibaek*, policyholder
account balance) as a projected quantity, the 표준형 해약환급금 (*haeyak hwangeupgeum*,
surrender value) curve, the 보험계약대출 (*boheom gyeyak daechul*, policy loan) — belongs to
the
[whole life technical notes (종신보험)](../whole_life/technical-notes.md), which is the
savings chassis.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows — premiums, death claims,
  claim expenses, acquisition and maintenance expenses and commission — for a
  single-policy model point of 정기보험 (*jeonggi boheom*, level term life), in the shape
  both live Korean regimes consume. K-ICS measures liabilities on the 건전성감독기준
  재무상태표 at "경제적이고 시장가격과 일관된 가치" [REG-R13], and K-IFRS 제1117호 measures
  the 이행현금흐름 as probability-weighted future cash flows on assumptions re-set at each
  reporting date [REG-R60]. Both commenced **2023-01-01** [REG-R14], so unlike Japan this
  is a description of the regime in force and not of one coming.
- **Discounting, 책임준비금, 해약환급금준비금, CSM and K-ICS 요구자본 are out of scope**,
  cited and not reproduced (see *Valuation and reserve pointers*). `krlib` computes no
  ratio and builds no reserve. The output is an **undiscounted** gross liability cash-flow
  stream and nothing else, which is why a savings-shaped model point loses money on it
  (worked example, model point 6).
- **Projection frequency.** **Monthly** — the model is `Term_KR_S`, and every model in
  this library now steps monthly. The grid is the one the contract is paid on: 월납 is the
  only premium mode on seven of the retrieved products, is the disclosure's basis [S5] and
  is half of the 감독규정 기준연령 요건 [REG-R9], and the rate card is quoted per month
  [S12]. The composite has little intra-year *benefit* structure — the sum assured is
  level, the premium is level within each 보험기간, and there is no account value to credit
  — so what the monthly step buys here is not a benefit the annual grid could not reach but
  **exposure measured where the cash actually moves**: premium collected only from lives
  still in force when the month opens, death benefit paid in the month of death rather than
  at the next anniversary, and the 갱신 decline and 납입완료 landing on their own dates. The
  one intra-year mechanic the notes call out, the 납입최고(독촉)기간 of **14 days**
  [S2 제27조] [REG-R25 제26조](#krlib-reg-r25), still sits inside a decrement represented as
  a rate; a 14-day grid is not proposed.
- **Time index.** `t` is **0-based** and counts **policy months**: `t = 0` is the first
  policy month of a policy projected from issue, period `t` runs from time `t` to time
  `t + 1`, the attained 보험나이 is `x + ⌊t / 12⌋`, and the contractual **policy year** is
  the derived 1-based label `policy_year(t) = ⌊t / 12⌋ + 1`, which is never indexed by.
  `proj_len` is the **number** of projected months — `12 × proj_years`, the exclusive end
  of the frame — so `result_cf()` covers `t = 0, 1, …, proj_len − 1` and has `proj_len`
  rows; the anchor cell projects 240 of them. This is lifelib's own convention
  (`basiclife/BasicTerm_S`: `for t in range(proj_len())`) and it is the convention of every
  model in this library.
- **Contractual terms stay in years.** 보험기간, 납입기간 and the 보험나이 80 renewal
  ceiling are annual quantities and the model reads them as such: `proj_years` is the
  horizon in years, `pay_term` is the 납입기간 in years, and 전기납 resolves against
  `proj_years` and not against the month count. Only the grid is monthly.
- **Timing conventions [std].** Premiums at the start of each **month**; maintenance
  expense at the start of the month; acquisition expense and initial commission at
  issue, which is the start of month `t = 0`;
  death claims and their claim expense at the end of the month in which they arise;
  ordinary lapse at the end of the month, **after** deaths; the renewal (갱신,
  *gaengsin*) decline at the end of the **last month of a cycle**, **after** ordinary
  lapse; the 만기보험금 of the 만기환급형 variant at the end of the final month
  `t = N − 1`.
- **The premium is a monthly cash flow, and `P_a = 12 × P_m` is now only a report.** The
  office premium is quoted monthly [S12] and the model collects `P_m` in the month it falls
  due, which is what the contract collects. Twelve monthly premiums is what the
  policyholder pays in a policy year and no Korean carrier retrieved publishes a mode
  discount [S12], so `P_a = 12 × P_m` remains exact as an **amount** — and it is carried,
  because the commission scale is written on an annualized premium and because a reader
  comparing this model against a disclosure needs the annual figure. What it is no longer
  is a **timing** convention. The annual grid collected all twelve at the start of the
  year, which at the 적용이율 (*jeogyong iyul*, the pricing interest rate) of 2.50%
  overstated the present value of a year's premium by `12 / 11.865256 − 1 =` **1.136%**,
  the mean deferral of the twelve payments being 5.5/12 of a year. That overstatement is
  gone, and so is its offsetting partner, the death benefit paid a year late. The pair is
  removed rather than netted: the residual timing error is half a month either way.
- **What the change of grid moved, and what it did not.** The sourced basis is untouched:
  every 예정 경험사망률 disclosure and the supervisor's 적용해지율 vector are **annual**
  rates [S12] [REG-R27], so `mort_rate` and `lapse_rate` still carry them and the monthly
  decrements `mort_rate_mth` and `lapse_rate_mth` are `1 − (1 − q)^(1/12)` [std] — the
  uniform-force conversion, level inside a policy year and stepping at each 계약해당일.
  Twelve monthly exits compound to the year's annual rate exactly, so the in-force **at
  each 계약해당일 is unchanged to the last bit** and so is the count reaching maturity;
  what moved is the exposure inside the year, and with it premium income, the mortality
  cost, and every quantity that weights a cash flow by it. Where a figure in these notes
  changed, that is why.
- **Age basis [std in nothing — it is contractual].** Every age in this model is
  **보험나이** (*boheom nai*, insurance age): 만나이 with fractions of six months or more
  rounded up, incrementing on the **policy anniversary** and not on the birthday
  [S2 제22조] [REG-R25 제21조](#krlib-reg-r25). Attained age in month `t` is `x + ⌊t/12⌋`,
  stepping at the 계약해당일 and level for the twelve months between it. The
  premium table, the mortality table and the model point ages are all on that one basis,
  so **no age shift is applied anywhere** — the opposite of `jplib`, where a 満年齢 issue
  age must be read against a 保険年齢 table and the mismatch has to be corrected. The one
  place Korean practice uses 만나이 instead is the 상법 제732조 voidness test for a life
  under 만 15 [S2 제22조제1항 단서] [REG-R50], which is an issue rule and not a projection
  quantity.
- **Currency.** KRW throughout [S1] [S12]. Amounts are given in won, with the Korean
  만원 / 억원 forms where a Korean reader would expect them: ₩100,000,000 (1억원).
- **Model points.** Single-policy, on an expected (probability-weighted) basis:
  survivorship multiplies per-policy cash flows. No aggregation logic is specified here.
  `point_id = 1` is the worked example's anchor cell, and it is the one cell in Korea that
  is doubly prescribed — the 감독규정's **기준연령 요건** [REG-R9] and the 생명보험협회
  disclosure's **대표계약** [S5] — so the premium it carries is quoted on one prescribed
  basis right across the disclosure, and read off two independent documents that agree to
  the won [S12] [S4]. (The disclosure's own like-for-like reach is narrower than its 45
  rows: the 경영인 rows are 90세만기 contracts and cannot be on the 20-year basis [S4].)
- **Termination.** A 비갱신형 contract ends at the end of its 보험기간. On the
  representative 순수보장형 nothing is payable then: no 만기보험금, no 해약환급금 at any
  duration, no run-off, no tail state [S1] [S2 제33조제2항] [S12]. On the 만기환급형
  variant the final year pays 100% of 「이미 납입한 주계약 보험료」 and the contract ends
  [S1] [S8] [S12]. A 갱신형 contract ends at the **renewal ceiling of 보험나이 80** [S6],
  because until then it renews.
- **Contract boundary — the paragraph this product forces.** A 비갱신형 contract
  guarantees its premium for the whole 보험기간, so the boundary is the term and there is
  nothing to argue about. A 갱신형 contract guarantees it only **within** the current
  cycle: at each 갱신 the insurer recomputes the premium at attained 보험나이 on the whole
  기초율 then in force — 적용이율, 계약체결비용, 계약관리비용 and 위험률, each named in the
  carriers' own words [S9] [S15] — and issues the renewal on a **new product code** [S9]
  [S15]. Against that, the renewal takes **no 고지 and no underwriting** [S6] [S9] [S15],
  so the repricing is a scale-level right and not an individual one, and an impaired life
  renews at the price a healthy life of the same attained age pays. Nothing retrieved in
  this session settles which reading a Korean insurer takes — not the 감독규정 [REG-R9]
  [REG-R19], not the 표준약관 [REG-R25], not the IFRS17 계리가정 가이드라인 [REG-R27], and
  K-IFRS 제1117호 itself is a standard and not a Korean application note [REG-R60] — so
  the reading is **[unverified]** and the model does not rule. It **projects to the
  ceiling in the base run [std]** and carries `contract_boundary = current_term`
  truncating at the end of the cycle in force. The two differ by far more than a rounding:
  on the same 갱신형 cell undiscounted net cash flow is **+₩2,919,193.21** to the ceiling
  and **−₩181,055.18** over the current cycle. Reporting either without naming the
  convention says nothing.
- **Rounding.** Intermediates at full float precision. The premium rounds to the **nearest
  10 won** before annualization, which is the granularity the anchor carrier quotes [S12].
  Displayed cash flows in this document are to two decimals of a won and in-force
  probabilities to ten decimals; the test suite asserts the worked example at exactly
  those precisions.

---

## Model point attributes

| Attribute | Cells | Type | Anchor cell (`point_id = 1`) |
|---|---|---|---|
| Policy identifier | — | string | `KR-TL-0001` |
| Sex | `sex()` | enum {M, F} | M |
| 가입나이 (`x`) | `age_at_entry()` | int, **보험나이**, 19–65 | 40 |
| Renewal structure | `renewal_type()` | enum {`gaengsin`, `bi_gaengsin`} | `bi_gaengsin` |
| 보험기간 (`n`) | `policy_term()` | int years; on a 갱신형 point this is the **cycle** | 20 |
| 세만기 expiry age | (via `policy_term()`) | int; `term_y = 0` selects it | — |
| 납입기간 (`n_p`) | `pay_term()` | int years; `pay_term_y = 0` = 전기납 | 20 (전기납) |
| Renewal ceiling (`w_r`) | `renew_ceiling()` | int 보험나이 | 80 (inert here) |
| 보험가입금액 (`SA`) | `sum_assured()` | KRW, ₩30,000,000–₩500,000,000 | ₩100,000,000 (1억원) |
| Rate class | `rate_class()` | enum {`standard`, `nonsmoker`, `preferred`, `super_preferred`} | `standard` (표준체) |
| 해약환급금/만기 form | `maturity_form()` | enum {`pure`, `rop`} | `pure` (순수보장형) |
| 납입주기 | `premium_mode()` | enum {`monthly`} | `monthly` (월납) |
| Contract boundary | `contract_boundary()` | enum {`ceiling`, `current_term`} | `ceiling` |
| 재해사망 uplift | `acc_death()` | bool | false |
| 보험료 납입면제 | `waiver()` | bool | false |
| 선지급서비스특약 | `accel()` | bool | false |
| 부활 | `reinstatement()` | bool | false |

Derived, and printed for the anchor cell: `horizon_ceiling() = 20`, `proj_years() = 20`,
`proj_len() = 240` months, `premium_mth_pp(0) = 15,080`, `prem_pp(0) = 180,960`.

**The premium is not a model point attribute.** `P_m` is *derived* from the premium scale
keyed on the maturity form, sex, the 보험나이 at the start of the cycle in force and that
cycle's length, then scaled by the rate class and the shortened-pay factor and by the sum
assured. That is what makes the repricing at 갱신 fall out of the same lookup as the issue
premium instead of needing a second column. Carrying the premium on the model point would
freeze it at the issue value and **silently convert a 갱신형 into a 비갱신형 at the wrong
price**.

Two attributes deserve a sentence because they interact in a way a reader will not expect.
`pay_term_y = 0` means 전기납 and resolves to `pay_term() = proj_years()` — the horizon in
**years**, because a 납입기간 is a contractual term in years and not a row count. On a `ceiling`
point that is the ceiling horizon; on a `current_term` point it is the truncated horizon.
So truncating a 갱신형 point at the current cycle also **compresses the 적용해지율
(*jeogyong haejiyul*, the pricing lapse rate) curve**, which decays from its first-year
rate to 0.1% over the 납입기간 — forty years on model
point 3, ten on model point 4. The two boundary readings therefore differ by more than
truncation, and the worked example prints both so the difference is visible rather than
discovered.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `l(t)` | In-force probability at **time** `t`, the start of month `t`; `l(0) = 1` | monthly recursion |
| `k(t)` | Renewal index: 1 in the original cycle, 2 after the first 갱신, … | boundary months |
| `P_m(t)` | Monthly office premium in force in month `t`; level within a cycle, and the month's income | boundary months |
| `P_a(t)` | `12 × P_m(t)`, the annualized premium: the commission base and the reporting figure | boundary months |
| `q(t)`, `q^m(t)` | Best-estimate death rate, **annual** and its monthly conversion — **one** decrement, one benefit | annual lookup, stepping at 계약해당일 |
| `w(t)`, `w^m(t)` | Ordinary lapse rate, annual and monthly, end of month, after deaths | annual lookup, stepping at 계약해당일 |
| `d(t)` | Renewal-decline rate; non-zero **only** in the last month of a cycle, and **not** converted — it is an election on a date, not a force | boundary months |
| `D(t)` | Expected death claims in month `t` = `l(t) × q^m(t)` | monthly |
| `u(t)` | Fraction of the in-force whose premiums are waived (납입면제 state) | monthly; **resets at 갱신** |
| `lap(t)` | Lapsed-but-reinstatable population inside the 36-month 부활 window | monthly |
| `CF(t)` | Net cash flow of month `t`, insurer perspective (+ = income) | monthly |

Three of these a Korean term model needs. `k(t)`, because the premium is a function of the
renewal index rather than of the policy year. `d(t)`, because leaving at a renewal boundary
is a different event, at a different date, from a different population, than lapsing
mid-cycle. And `u(t)`, because Korea's disability state does not pay a benefit — it
**switches the premium off** — and because that state is **extinguished by a renewal**
[S6], which is a cash-flow rule with no analogue anywhere else in this repository.

Two clocks are contract state the base run tracks in prose and does not monetize: the
two-year suicide window and the contestability window (2년 generally, 1년 for disease on a
진단계약, and a 3년 outer limit from the contract date), both running from the 보장개시일
and **neither restarting on 갱신** [S2 제6조] [S2 제14–15조] [REG-R25 제13–14조](#krlib-reg-r25). Only 부활
restarts the suicide window [S2 제28조]. The 사기 취소 window of **5년** [S2 제16조] is the
real outer limit on unwinding a Korean life policy and is longer than either.

There is deliberately **no** `cv_pp` and no account value. On the representative 전기납
무해지 contract the 약관 pays nothing at any duration — 「보험료 납입기간이 보험기간과
동일한 계약 … 의 경우에는 보험기간 중 계약이 해지될 경우 해약환급금을 지급하지
않습니다」 [S2 제33조제2항] — and 한화생명's published 해약환급금 예시 for the same shape
prints 환급률 0.0% at all eleven durations for both sexes [S1]. With no surrender value
there is no collateral, so 보험계약대출 and 자동대출납입 are granted by the 약관 and
inoperative in fact [S2 제26조·제34조] [REG-R28]. 납입최고 (14일) → 실효 → 부활-or-not is
the whole persistency machinery here, which is part of why this is the right chassis to
specify first.

---

## Assumption inputs

Three classes, kept separate. The first is cited and the insurer cannot change it; the
second is discretionary and, on a 무배당 protection product, nearly empty except for the
one lever that dominates a 갱신형; the third is the modeler's view.

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| 사망보험금 | `SA`, on death within the 보험기간; payment terminates the contract immediately and automatically | [S1] [S2 제4조·제23조] [S8] [S10] [S11] [S12] |
| What counts as death | Includes a court 실종선고 (deemed at the end of the 실종기간) and a 관공서 disaster notification (the date entered in the 가족관계등록부) | [S2 제5조제2항] |
| Withdrawal of life-sustaining treatment | Expressly does **not** affect the cause of death or the payment | [S2 제5조제3항] |
| Disability benefit | **None.** There is no Korean analogue of the Japanese 高度障害保険金 | [S2 제5조]; contrast `Term_JP_S` |
| 만기보험금 | None on the 순수보장형; 100% of premiums paid on the 만기환급형, computed **as if waived premiums had been paid** | [S1] [S8] [S12] [S17] |
| 해약환급금 | **Nil at every duration** on the representative 전기납 무해지 form | [S1] [S2 제33조제2항] [S12] |
| — shortened-pay 무해지 | Nil during the 납입기간; **50% of the 표준형's** thereafter. Not computed by this model | [S1] [S2 제33조제2항] [S12] |
| — where premiums were waived | **Nil even after 납입완료**: the step-up is forfeited | [S2 제33조제2항 단서] [S12] |
| Premium | Level within the 보험기간, monthly in advance over the 납입기간; **not** guaranteed beyond a 갱신 | [S1] [S2] [S8] [S12] [S9] [S15] |
| Premium structure | Per-mille of `SA`; **no separable flat policy element** can be identified | [S1] [S8] [S11] [S12] [S14] |
| 적용이율 | **2.50% 연복리** at the anchor carrier | [S1] [S8] [S11] [S12] |
| 갱신 | Automatic and **negative-option** — renews unless the policyholder objects 15 days before expiry; **no 고지, no underwriting, no health condition**; repriced at attained 보험나이 on the whole 기초율 then in force; issued on a new product code | [S6] [S9] [S15] |
| Renewal ceiling | 보험나이 80, the final cycle truncated to the remainder | [S6] |
| Waiver carry-over at 갱신 | **None** — 「갱신 전 보험료 납입면제 사유로 인한 보험료 납입면제를 적용하지 않고, 보험료를 계속 납입하여야 합니다」 | [S6] |
| 보험료 납입면제 | In the **주계약** at no separate premium, on a 장해지급률 of **50% or more** from 「동일한 재해 또는 재해이외의 동일한 원인」 — **cause-neutral** | [S1] [S2 제5조제1항] [S6] [S8] [S9] [S10] [S11] [S12] |
| — determination | 장해지급률 fixed at **180일** from the accident or confirmed diagnosis if not settled sooner; look-back **2년** where the term is ten years or more, **1년** where shorter | [S2 제5조제4항·제5항] |
| — effect | 「차회 이후의 보험료 납입을 면제」 — future premiums only, no refund; cover continues | [S2 제5조제1항] |
| 선지급서비스특약 | Remaining life expectancy of **12개월 이하** judged by a specialist at a 종합병원; up to **50% of the 사망보험금**, aggregated across the insurer's contracts to **₩50,000,000**; up to **₩10,000,000** may be 100% | [S2 제3조·제4조] [S10] [S12] [S17] |
| — computation | The accelerated amount discounted over the remaining life expectancy at the **평균공시이율**, less the similarly discounted premiums on it and less any outstanding 보험계약대출 | [S2 제4조제6항] |
| Suicide exclusion | No death benefit where the 피보험자 intentionally takes their own life within **2년** of the 보장개시일 (or of the 부활 application date); **does not restart on 갱신**; no time bar where the act occurred in a state of 심신상실 | [S1] [S2 제6조] [S3] [S6] [S8] [S10] [S11] [S13] [S17] |
| Other 면책사유 | Intentional killing by the 보험수익자 (other beneficiaries' shares still paid) or by the 계약자 — **three limbs in total, in every 약관 retrieved** | [S1] [S2 제6조] [S6] [S8] [S10] [S11] [S17] |
| Gross negligence | **Not an exclusion**, by statute | [REG-R50 제732조의2](#krlib-reg-r50) [R4] |
| War, aviation, hazardous pursuits | **Absent from every 약관 and 상품요약서 retrieved**; occupational risk is handled at underwriting through the 위험등급 | [S2 제24조제4항] [S3] [S6] |
| 납입최고(독촉)기간 | **14일** from the demand (7일 where the term is under a year), extended to the next business day; a claim arising within it is paid | [S2 제27조] [REG-R25 제26조](#krlib-reg-r25) |
| 부활 | **3년** from termination, expressly including where 「해약환급금이 없는 경우를 포함합니다」, so a 무해지 policy is always eligible; arrears at 「평균공시이율+1% 범위 내」 | [S2 제28조] [REG-R25 제27조](#krlib-reg-r25) |
| 보험계약대출 / 자동대출납입 | Granted by the 약관 and **inoperative in fact**, there being no surrender value | [S2 제26조·제34조] [REG-R28] |
| 감액완납 / 연장정기 | **Neither exists** in any retrieved 약관 or 상품요약서 | [S1] [S2] [S6] [S8] [S10] [S11] [S12] |
| 계약자배당 | **Nil** — 「이 계약은 무배당보험이므로 계약자 배당금이 없습니다」; all 45 disclosed products are 무배당 | [S2 제35조] [S4] |
| Claim timetable | **3영업일** from complete documents; **10영업일** where investigation is needed; a payment date within **30영업일** except in six named cases; a 가지급보험금 of up to 50% on request | [S2 제9조] |
| 예금자보호 | 해약환급금 plus 기타지급금 to **₩100,000,000 per person**, and 사고보험금 to a **separate and additional ₩100,000,000**; corporate policyholders not protected | [S3] [S11] [S13] [REG-R52 제18조제7항](#krlib-reg-r52) [REG-R32] |

### (b) Insurer-discretionary current elements

On 무배당 protection business this class is nearly empty, which is why the classes are
separated at all: on the
[whole life technical notes (종신보험)](../whole_life/technical-notes.md) and the
[pension savings technical notes (연금저축보험)](../pension_savings/technical-notes.md)
the 공시이율 and the 최저보증이율 live here. On a Korean 정기보험 there is **no 공시이율 and
no 최저보증이율 at all** — the disclosure's guarantee columns are empty for every 정기보험
row [S4]. Four residual items:

| Input | Snapshot value | Basis |
|---|---|---|
| Renewal rate scale | The scale in force at each future 갱신 is the insurer's, and the contract says the **whole 기초율** moves, not just the age | mechanic [S9] [S15]; scale **[std]** (1) |
| 단체취급 discount | 1.5%–5% of the 영업보험료 for a group of five or more; **not applied** | [S1] [S10]; scope **[std]** |
| 고액할인 | Offered above ₩100,000,000 at one carrier, **rate unpublished**; not applied | [S9]; scope **[std]** |
| 걷기할인형 / 선납 | −10% of the 영업보험료 for the **first twelve premiums only** on 8,000 steps a day on 20 days a month; 선납 at an insurer-set unpublished discount. Neither applied | [S8] [S12]; scope **[std]** |

1. **This is the one genuinely discretionary lever with a large cash-flow effect, and it is
   invisible.** The model reproduces the published 갱신 ladder — ₩9,000 → ₩21,000 →
   ₩56,000 → ₩201,000 a month at attained 보험나이 40/50/60/70 [S7] — but 흥국생명's own
   caveat on that ladder is essential and is reproduced rather than smoothed over: the path
   「최초계약 가입 당시의 보험료율을 기준으로 산출(연령증가만 반영)하였으므로, 갱신시
   보험료율이 변동될 경우 갱신시점의 보험료는 상기 예시와 크게 달라질 수 있습니다」 [S7].
   It holds the rate scale frozen at its issue level and reflects **age alone**. A
   projection that also moved 위험률 and 적용이율, as the contract permits, would differ,
   and nothing published bounds by how much. Treating the current scale as persistent is a
   **[std]** assumption, not a neutral one.

Two discounts not applied are worth a line each for the direction of the bias. The 단체취급
discount is a distribution feature (an affinity group of five or more) rather than a
product feature, so leaving it out overstates premium income on group-sold business only.
The 걷기할인형 is a twelve-month acquisition discount dressed as a wellness feature [S8],
so leaving it out overstates first-year premium at the one carrier that offers it and
nothing thereafter.

### (c) Behavioral / experience assumptions (modeler's view — all [std])

**Mortality — one decrement, one benefit.** A Korean term policy pays the 보험가입금액 on
death within the 보험기간 and nothing else, and payment terminates the contract immediately
[S2 제4조·제23조]. There is **no 高度障害保険金 analogue**, so unlike `Term_JP_S` this model
carries no competing benefit on one sum assured and no double-count to avoid. What Korea
has instead is a second, smaller decrement that switches the premium off without
terminating the contract — the 50% 장해 waiver — which is a *state*, modelled in
`wop_waived_frac`, and not a claim.

The industry table is the **경험생명표** (*gyeongheom saengmyeongpyo*, experience life
table), prepared by 보험개발원 every five years; the current edition is the **제10회**,
applied to new business from April 2024. **It is not published.** What is released is the
summary — 평균수명 남 86.3 / 여 90.7 and 65세 기대여명 남 23.7 / 여 27.1 — and not the
rates [REG-R33] [REG-R34]. **Even those four numbers reach this library through a trade
newspaper**: 보험개발원's own announcement was not retrievable and [REG-R33] is a 보험매일
report of it, so the tilt target below is second-hand and is tagged as such wherever it is
used. The 참조순보험요율 behind each carrier's own basis is not public for mortality
either [REG-R4] [R19] [R20]. This is the sharpest documentary contrast in this
repository with `jplib`, whose 標準生命表2018 is a free public PDF of `qx` by single year of
age; and it is why the carriers' own 예정 경험사망률 disagree by a factor of **1.77 at male
40** (0.000480 to 0.000850 across seven carriers) [S1] [S6] [S8] [S10] [S11] [S12] [S17],
where every Japanese carrier prices off one table.

`mort_table.csv` is therefore **[std] throughout**, with a `provenance` column on every row:

| Step | Rule | Basis |
|---|---|---|
| Anchors | The anchor carrier's disclosed 예정 경험사망률 at ages 20 / 40 / 60: male **0.000280 / 0.000650 / 0.003390**, female **0.000200 / 0.000430 / 0.001390** | [S12], as the 상품요약서 must print |
| Law | Makeham `q(x) = A + B c^x`, fitted **exactly** — three anchors, three parameters, so an interpolation and not a regression | **[std]** (2) |
| Tilt above 60 | `q(x) → q(x) · k^(x−60)`, one free parameter per sex, solved so the table's complete expectation of life at 65 is **exactly** the published 경험생명표 figure — 23.7 male, 27.1 female | **[std]**, target [REG-R33] |
| Range | Ages 19 to 120, so the `e65` claim is checkable from the shipped file rather than taken on trust | **[std]** |
| Best estimate | `q(t) = 0.85 × c_q(class, sex) × q_x^tab` | **[std]** (3) |
| Age read | At 보험나이, unshifted — the table, the rate card and the model point are one basis | contractual [S2 제22조] |
| Improvement | None in the base run | **[std]** (4) |
| Suicide-exclusion offset | None: years 1–2 claims are not reduced for excluded suicides | clause [S2 제6조]; offset **[std]** (5) |

2. Fitted parameters, quotable and checkable against the shipped file:
   male `A = 0.0002222362869`, `B = 7.800209431e-06`, `c = 1.105293057`, `k = 1.0098862619`;
   female `A = 0.0001275342466`, `B = 1.736158676e-05`, `c = 1.074056604`,
   `k = 1.0592847691`. Sample shipped rates: male `q(65) = 0.00572256`,
   `q(80) = 0.02883008`; female `q(65) = 0.00257678`, `q(80) = 0.01707668`; `q(120) = 1`
   caps both sexes. The expectation the tilt targets is the **complete** one on the usual
   uniform-deaths convention, `e65 = sum_{j>=1} j_p_65 + 0.5`, which on the shipped file is
   23.200000 + 0.5 = **23.7** male and 26.600000 + 0.5 = **27.1** female; the curtate figure
   alone does not reproduce the published number and a reader checking it must add the
   half-year. The tilts are
   small and **upward** — an unconstrained Makeham extrapolation of three disclosed rates
   leaves slightly too much life at 65. The resulting table sits **4.2 years (male) and 3.4
   years (female) above** the public 완전생명표's own 65세 기대여명 of 19.5 and 23.7
   [REG-R38]. That gap is underwriting selection, and a constructed Korean insured-lives
   table that does not reproduce it is not an insured-lives table. Reproducing it is the
   one external check available.
3. **`mort_be_factor = 0.85` is this model's largest lever and its least evidenced number.**
   The shipped table is a **pricing** rate — a carrier's 예정 경험사망률, which carries a
   margin over experience that **no public Korean document sizes**, the 산출방법서 being a
   기초서류 filed with the FSC and never published [REG-R2]. Japan can argue its factor from
   the publisher's own stated margin (a ~2σ adjustment capped at 130%); Korea cannot,
   because nothing is stated. What *can* be bracketed is the scale of carrier-to-carrier
   dispersion: at male 40 seven carriers run 0.000480 to 0.000850 around the anchor's
   0.000650, so the cheapest pricing basis in the market is **0.74×** the anchor's before
   any margin is removed at all [S1] [S6] [S8] [S10] [S11] [S12] [S17]. 0.85 is a round
   central choice inside that. A user with own experience should replace it before anything
   else in this file; the sensitivity is quantified below.
4. Two years of improvement since the 제10회 table's April 2024 application are not
   projected **[std]**. A production basis applying an improvement scale must re-derive
   footnote 3, because part of the 0.85 stands in for it.
5. Immaterial at these claim levels and unsupported by any incidence split in the sources.
   Note the direction: on a 무해지 form the suicide 면책 pays the 계약자적립액, which on this
   contract is not the same as the (nil) 해약환급금, so even a modelled exclusion is not a
   clean claim saving.

**Rate-class relativities — sourced, not standardized, which no other library here can
say.** Two carriers publish a full 예정 경험사망률 table per class [S11] [S12]. The shipped
`rate_class_table.csv` carries both a `mort_ratio` and a `prem_ratio` at male and female 40
from the anchor carrier [S12]: 표준체 1.000 / 1.000; 비흡연자 0.828 / 0.956; 건강체 0.723 /
0.907; 슈퍼건강체 0.583 / 0.856 (mortality), against premium ratios 0.865 / 0.964, 0.763 /
0.890, 0.586 / 0.846. **The premium ratio exceeds the mortality ratio in the three male
classes and in the female 비흡연자** — which is what a loading that does not scale with the
risk does — **and falls marginally below it in the other two female cells**: 0.890 against
0.907 at 건강체 and 0.846 against 0.856 at 슈퍼건강체. Nothing retrieved explains the
reversal, and the cross-sex comparison runs the same way rather than the other, so it is
not evidence of a flat loading either: the female 표준체 premium is **53%** of the male one
where female mortality is **66%** of male [S12] [S4]. Holding the ratios flat across ages
is the **[std]** step; the disclosures are at three ages and the ratios move little between
them.

**Accidental mortality.** `acc_mort_rate` is the 예정 재해사망률 of a *different* carrier
[S6], log-linear in `ln q` between its disclosed anchors at 20/40/60 with the 40–60 slope
extended above 60 and capped at the all-cause rate **[std]**. Pairing two carriers is
defensible here in a way that pairing two all-cause tables would not be: the two carriers
publishing accidental rates agree to **three significant figures at age 20** and to within
10% everywhere [S6] [S10], strong evidence that both take the 보험개발원 참조 재해사망률
almost unadjusted, where the all-cause rates are heavily adjusted. It is used only to
**split** the existing death decrement for the 재해사망 uplift variant, never as a decrement
of its own.

> **A number in `_research/term-life.md` that does not reproduce, and is corrected here.**
> The research file reads its own two published tables as giving accidental death at 「3–4%
> of all-cause mortality at male 60 and 15–25% at male 20」 [S6] [S10]. The arithmetic on
> those tables does not give that. On 흥국생명's own pair the share is
> `0.000355 / 0.003940 = 9.0%` at male 60 and `0.000097 / 0.000310 = 31.3%` at male 20
> [S6]. On the **shipped** pairing — [S12] all-cause with [S6] accidental — it is
> **10.47%** at male 60, **16.92%** at male 40 and **34.64%** at male 20. `product-spec.md`
> footnote 17 and `model.md` carry the corrected shares, the model uses the shipped pairing,
> and the worked example's model point 10 prints it. The qualitative point the research
> draws from the number survives intact: a doubled benefit on a tenth of the deaths is
> cheap, which is why carriers bundle it into a product 형 rather than pricing it as a
> rider.

**Lapse — the one assumption in this repository whose chain from supervisory guideline to
disclosed pricing parameter runs end to end, though not at instrument level throughout.**
The **shape** is supervisory, not chosen: the
2024 IFRS17 계리가정 가이드라인 makes a **로그-선형 model converging to 0.1%** the 원칙모형
for 무·저해지 business, permits 선형-로그 (to 0%) and 로그-로그 (to 0.1%) only as exceptions
on onerous disclosure conditions, and sets a post-완납 ultimate of **0.8%** [REG-R27]. The
guideline's **values** are verified from the 보도자료; its 별첨 was never converted from HWP,
so the functional form itself is **[unverified]** at instrument level and the log-linear
interpolation below rests on the 보도자료's description of it. The
**endpoints** are disclosed in the 상품요약서 wherever a 무해지 form is sold: 「납입기간
이내에 대하여 경과기간별로 연 0.1%~4.6%, 납입기간 이후에 대하여 경과기간별로 연
0.7%~1.6%」 at the anchor carrier [S12] and 「연 0.1%~8.4%, 납입기간 이후 연 0.8%」 at
another [S1]. `lapse_table.csv` ships three rows, not a curve, because that is what Korea
discloses:

| Segment | Rate | Basis |
|---|---|---|
| `in_payment_start` | **4.6%**, applied in the first policy year, `t = 0` | [S12]; the other observed upper endpoint is 8.4% [S1] |
| `in_payment_end` | **0.1%**, reached at 납입완료, `t = n_p − 1` | [S12] [S1] disclosed **and** [REG-R27] prescribed |
| `post_payment` | **0.8%**, thereafter, `t ≥ n_p` | [S1] disclosed **and** [REG-R27] prescribed |

The curve between the first two is the prescribed log-linear one, on the 0-based index:

    w(t) = 0.046 * (0.001 / 0.046) ** (t / (n_p - 1))     for t <  n_p
    w(t) = 0.008                                          for t >= n_p

Two **[std]** steps sit inside `lapse_be_factor = 1.0`, and neither is small.

- **The disclosed endpoints are on a 10년납 basis and the composite is 전기납 over twenty
  years.** The model stretches the same endpoints over the point's own 납입기간, so the
  anchor's curve decays from 4.6% to 0.1% over twenty years rather than ten. **Model point
  5 is the only shipped point that reproduces the disclosed shape at its disclosed
  length**, being a genuine 10년납 contract. It and model point 9 — a 35-year term bought
  20년납 — are the only two shipped points whose 납입기간 ends before their cover does, so
  they are the only two that reach the `post_payment` row at all.
- **A 적용해지율 for a 무해지 form is a pricing rate, deliberately low by regulatory
  design, and is not a best estimate.** 감독규정 제7-66조제4항 permits the reduced surrender
  value precisely *because* premiums were calculated using a 최적해지율 [REG-R19]
  [REG-R20], which is what makes the assumption a supervisory matter and not only an
  earnings one. Nothing retrieved discloses a best-estimate term lapse rate. The only
  Korean experience datum available is a whole-life one and it points one way: a 5·7년납
  저해지 단기납 종신보험 ran a **37회차 유지율 of 50.2% against an assumed 71.5%** [R18].
  The *direction* of that error, not its size, is why the base run sets
  `lapse_be_factor = 1.0` and the sensitivity below moves it rather than pretending the
  number is known.

Resulting anchor-cell curve: simple mean over the twenty years **1.238%**, in-force
weighted mean **1.341%**. Lapse pays nothing — there is no 해약환급금 [S1] [S2 제33조제2항]
[S12] — so `claims_lapse` is a published column of zeros.

**Renewal decline [std].** At each 갱신 boundary a fraction `d` of survivors leaves rather
than accept the repriced contract. **It is published nowhere in Korea, for any product**,
and that is a real gap and not a research failure: the mandatory 예상 갱신보험료 예시 shows
the *price* path and never the *persistency* path [S7] [S16]. `renewal_decline_base = 0.20`
is argued from three directions, not chosen:

- The option is **negative** and the notice period is **15일** [S9] [S15] — the shortest
  and most negative arrangement in this repository — so inertia dominates and the rate must
  sit well below a positive-election rate.
- The step is large and **disclosed in advance**: ×2.33 at the first renewal on the
  published path [S7]. An insurer expecting no reaction would not need to print the
  projection at all.
- The nearest Korean supervisory calibration of a behavioural jump at a discrete
  contractual event is the FSS's floor of **at least 30% additional lapse** at the point a
  단기납 종신보험's refund ratio peaks, itself calibrated to the 29.4%–30.2% eleventh-year
  lapse observed on single-premium bancassurance savings [REG-R27]. A renewal offers the
  policyholder **no cash and no maturing option, only a higher price**, so 20% sits
  deliberately below that floor.

Arguable range roughly **5% to 40%**; `renewal_decline_max = 0.40` is set at the top of it,
and the sensitivity below runs the range rather than reporting a point estimate as a fact.

**Expenses and commission (all levels [std]; no Korean carrier publishes any of them).**
Every 상품요약서 defines 계약체결비용 and 계약관리비용 in the same words — 「보험회사가
보험계약의 체결, 유지 및 관리 등에 필요한 경비로 사용하기 위하여 보험료 중 일정비율을
책정한 것」 — and **not one publishes a rate** [S1] [S6] [S8] [S10] [S11] [S12].

| Input | Cells / Reference | Value | Note |
|---|---|---|---|
| Acquisition expense `E0` | `expense_acq` | ₩120,000 per policy at issue | **[std]** (6) |
| Initial commission `c0` | `comm_init_rate` | **60%** of `P_a(0)`, at issue | **[std]** (6) |
| Renewal commission `c_r` | `comm_renewal_rate` | **3%** of premium income from `t = 1` | **[std]** |
| Commission at a 갱신 | `comm_new_term_rate` | **0** in the base run | **[std]** (7) |
| Maintenance expense `e(t)` | `expense_maint`, `inflation_rate` | ₩2,000 per **month** (₩24,000 p.a.), inflating **2.0%** p.a. as `1.02^⌊t/12⌋` | **[std]** |
| Claim expense `ec` | `expense_claim` | ₩300,000 per death claim | **[std]** |

6. Two public handles bound the acquisition assumption and neither pins it. The first is
   the **보험가격지수** — an index of 88.1 (male) / 85.5 (female) at the anchor means the
   product's total premium is 88.1% of the industry-average net premium plus the
   industry-average expense loading [S1] [S4] — and the *dispersion* of that index across
   the 45 disclosed products, **51.6% to 239.1%**, bounds what an expense assumption may
   plausibly be. The second is the **별표 14 표준해약공제액**, which caps recoverable
   acquisition cost by formula: `연납순보험료의 5% × 해약공제계수 + 보험가입금액의 10/1000`,
   with 해약공제계수 the 보험기간 capped at 20 years [REG-R20] [R9]. At the anchor cell the
   sum-assured limb **alone** is `₩100,000,000 × 10/1000 = ₩1,000,000`, which is 5.5 years'
   gross premium, against a modelled year-1 acquisition charge of `120,000 + 108,576 =`
   **₩228,576**. The statutory cap is nowhere near binding on this product, which is worth
   stating because on a savings product it is the binding constraint.
7. A Korean 갱신 is issued on a **new product code** [S9] [S15], which is an argument for
   paying acquisition commission at each renewal; it takes no 고지 and issues no new
   underwriting decision, which is an argument against. No document in the set discloses a
   commission scale at all, so the base run pays **nothing** at a renewal and exposes the
   switch. It is not a small choice: setting `comm_new_term_rate = 0.60` on the 갱신형
   anchor turns `t = 120` from **+₩4,689.19** to **−₩83,085.07** and cuts the forty-year
   total from **+₩2,919,193.21** to **+₩2,238,679.76**. On a monthly grid the charge lands
   in one row as a cliff of the same shape as the acquisition commission at issue, rather
   than being netted against a year of the repriced premium. The pitfall list tests it.

**Waiver, acceleration and reinstatement incidence — three arbitrary placeholders, said so
plainly.** `wop_inc_rate = 0.0008` with `wop_rec_rate = 0`, `accel_take_up = 0.10` and
`reinstate_rate = 0.10` drive modules that are off on the anchor cell. No Korean document
publishes a 50%-plus 장해 incidence, an acceleration take-up or a 부활 rate, and the
참조순보험요율 behind the first is not public for disability [REG-R4] [R19]. One deliberate
non-derivation: **`wop_inc_rate` is not scaled off `mort_rate()`**. The waiver trigger is
cause-neutral — 「동일한 재해 또는 재해이외의 동일한 원인」, sickness qualifying equally
with accident [S2 제5조제1항] — so a number derived from `q` would be a false derivation
dressed as a real one. Beside them, two **sourced** parameters: `reinstate_window = 3`
years [S2 제28조] and `accel_disc_rate = 0.025`, the 2026 평균공시이율 [S12] [REG-R48],
which is the rate the 약관 itself names for this discount [S2 제4조제6항], together with
`accel_prognosis_months = 12` [S2 제3조]. Only the **take-up** is [std].

---

## Cash flow components and recursions

### Notation

| Symbol | Meaning | Cells |
|---|---|---|
| `t` | Policy **month** index, **0-based**: `t = 0, 1, …, N − 1`; policy year = `⌊t/12⌋ + 1` | index of `result_cf()` |
| `x` | 가입나이 in 보험나이; attained age at time `t` is `x + t` | `age_at_entry`, `age` |
| `n` | 보험기간 — the whole term on a 비갱신형 point, **one cycle** on a 갱신형 one | `policy_term` |
| `n_p` | 납입기간; `pay_term_y = 0` (전기납) resolves to `N` | `pay_term` |
| `w_r` | Renewal ceiling in 보험나이, 80 | `renew_ceiling` |
| `N` | **Number** of projected periods — the exclusive end, so the last index is `N − 1` | `proj_len` |
| `k` | Renewal index, `k(t) = 1 + floor(t / n)` on a 갱신형 point, else 1; 1-based | `term_index` |
| `x_k` | 보험나이 at the start of cycle `k`, `x + (k − 1)n` | `term_start_age` |
| `m_k` | Length of cycle `k`, `min(n, w_r − x_k)` — truncated at the ceiling | `term_len` |
| `m_k^p` | Paying years inside cycle `k` | `term_pay_years` |
| `SA` | 보험가입금액, level | `sum_assured` |
| `i_p` | 적용이율, 2.50% | `prem_int_rate` |
| `g(k)` | Shortened-pay uplift | `pay_factor` |
| `c_p`, `c_q` | Rate-class premium and mortality ratios | `class_prem_ratio`, `class_mort_ratio` |
| `r(form, sex, x_k, m_k)` | Monthly office rate per ₩100,000,000 of cover, 표준체 | `prem_rate_mth` |
| `qbar(x, m)` | Mean **table** rate over `m` years from age `x` | `mort_table_mean` |
| `P_m(k)`, `P_a(k)` | Monthly and annualized office premium in cycle `k` | `premium_mth_pp`, `prem_pp` |
| `q_x^tab` | 표준체 table rate at an attained age | `mort_rate_at_age` |
| `q(t)` | Best-estimate **annual** death rate at `age(t)` | `mort_rate` |
| `q^m(t)` | Monthly death decrement, `1 − (1 − q(t))^(1/12)` **[std]** | `mort_rate_mth` |
| `a_q(t)` | Accidental share of `q(t)`, a ratio of annual table rates | `acc_mort_share` |
| `w(t)` | Ordinary **annual** lapse rate | `lapse_rate` |
| `w^m(t)` | Monthly lapse decrement, `1 − (1 − w(t))^(1/12)` **[std]** | `lapse_rate_mth` |
| `d(t)` | Renewal-decline rate, **not** converted; 0 unless `t` is a boundary month, `(t + 1) mod 12n = 0` | `renewal_decline_rate` |
| `l(t)` | In-force at time `t`, the start of month `t`; `l(0) = 1` | `pols_if`, `pols_if_init` |
| `D(t)` | Expected death claims, `l(t) q^m(t)` | `pols_death` |
| `u(t)` | Waived fraction of the in-force | `wop_waived_frac` |
| `lap(t)`, `rho` | 부활 pool and reinstatement rate | `pols_lapse_pool`, `reinstate_rate` |
| `E0`, `e(t)` | Acquisition expense; maintenance `2,000 × 1.02^⌊t/12⌋` per policy per month | `expense_acq`, `expenses` |
| `c0`, `c_r` | Initial commission `0.60 × P_a(0)`; renewal rate 0.03 | `comm_init_pp`, `comm_renewal_rate` |
| `ec` | Claim expense per death claim, ₩300,000 | `expense_claim` |
| `A`, `a(t)`, `i_s` | Accelerated amount, take-up, 평균공시이율 | `accel_amount`, `accel_share`, `accel_disc_rate` |
| `CF(t)` | Net cash flow of month `t` (+ = income) | `net_cf` |

Dimensional check: `q`, `q^m`, `w`, `w^m`, `d`, `u`, `l`, `D`, `a_q`, `a` are dimensionless
probabilities; `SA`, `E0`, `e`, `ec`, `P_a`, `A` are KRW per policy; `P_m` and `r` are KRW
**per month**, and on this grid that is the grid's own unit, so `P_m` enters `CF(t)`
directly and the `× 12` survives only where an annualized figure is wanted; `r` is per
₩100,000,000 of cover, so `r × SA / 100,000,000` is KRW per month. `q` and `w` are
**annual probabilities** and are converted by compounding, never by dividing: the
distinction matters, and the sister model `LTC_KR_S` divides its transition intensities by
twelve for the opposite reason — those are rates per year and not probabilities. Every term of `CF(t)`
is KRW per month per policy issued, except `expense_acq` and `comm_init_pp`, which are
one-off amounts at `t = 0`, the latter computed on the **annualized** premium.

### The premium chassis

Korean rate cards are published and the anchor cell is published twice, so the **level** is
sourced where `jplib`'s and `uklib`'s are not:

    P_m(k) = round_10( r(form, sex, x_k, m_k) * c_p(class, sex) * g(k) * SA / 100,000,000 )
    x_k    = x + (k - 1) * n
    m_k    = min(n, w_r - x_k)
    P_a(k) = 12 * P_m(k)

`round_10` is rounding to the nearest 10 won, the anchor carrier's quoting granularity
[S12]. At the anchor cell `r(pure, M, 40, 20) = 15,080`, `c_p = 1`, `g = 1` and
`SA / 100,000,000 = 1`, so `P_m(1) = 15,080` and `P_a(1) = 180,960` — the published figure
reproduced exactly, because it *is* the published figure [S12] [S4]. In the model's index
that is `premium_mth_pp(0) = 15,080` and `prem_pp(0) = 180,960`, cycle 1 running from
`t = 0`.

**No flat policy element can be separated out.** Unlike `jplib`'s オリックス生命 grid, from
which a ¥248 monthly policy fee could be extracted exactly because the card varies the sum
assured, **every Korean grid retrieved fixes the sum assured and varies age, sex, rate class
or product form instead** [S1] [S8] [S11] [S12] [S14]. The office premium is therefore
treated as strictly proportional in `SA` and the approximation is recorded rather than
hidden. One consequence is visible in the data and is worth keeping in view when reading
the worked example's female twin: female premiums run at **52–56% of male across the six
direct writers** on the same cell, and anywhere from **47% to 90%** across the eleven
face-to-face and simplified-issue rows [S4]. A per-policy loading that does not scale with
the risk pushes that ratio up as the loading grows, and the face-to-face band does reach
higher — but it also reaches *lower* than the direct writers' band, so the channel spread is
consistent with a flat fee without establishing one, and no rate card lets it be measured.

**The shortened-pay uplift `g(k)` [std].** No Korean document retrieved publishes a
shortened-pay premium for a **term** contract at all, so an equivalence had to be chosen.
The model uses the annuity-certain ratio at the 적용이율:

    g(k) = a-due(m_k) / a-due(m_k^p) = (1 - v^m_k) / (1 - v^m_k^p),   v = 1 / (1 + 0.025)

giving `g = 1.781198` for a 20-year term bought 10년납 (model point 5) and `g = 1.484695`
for a 35-year term bought 20년납 (model point 9). A **certain** annuity rather than a life
annuity overstates the uplift slightly, by the mortality that would have been shed between
the two periods; at these ages and durations that is a small overstatement, and it is
stated rather than buried.

**The scale extension beyond the published cells [std].** Twenty premium cells are shipped:
twelve 20-year cells (순수보장형 and 만기환급형, male and female, ages 30/40/50) from the
anchor carrier [S12], and eight 10-year cells that are the published 갱신형 ladder of the
one carrier printing a mandatory 예상 갱신보험료 예시 [S6] [S7] — whose **four female rows
are on 2형(보장추가형)**, that carrier not selling its 1형(기본형) to women at all [S4] [S6],
so they are not the same cover as the male rows and no shipped model point reads one.
Where a model point needs a
cell that is not shipped, the rate is extended off the `is_anchor` row of the matching form
and sex — the age-40 20-year cell — in the ratio of mean **table** mortality over the term:

    r(sex, x, m) = r_anchor * qbar(x, m) / qbar(x_a, m_a),
    qbar(x, m)   = mean of q_a^tab over a = x .. x + m - 1

Note `qbar` averages the **table** rate `mort_rate_at_age`, unadjusted. Feeding the
best-estimate rate into a premium extension would move a premium scale by an assumption
that has nothing to do with pricing. Diagnostic values, all checkable from the shipped
table: `qbar(40,20) = 0.00152337` (M) and `0.00077569` (F); `qbar(30,20) = 0.00070037` (M);
`qbar(65,15) = 0.01348403` (M); `qbar(45,35) = 0.00370477` (F); `qbar(19,30) = 0.00053910`
(M); `qbar(55,20) = 0.00655454` (M).

Model points 1, 2, 3, 4, 5 and 6 read **published cells only**; points 7, 8, 9 and 10 use
the extension. The 10-year rows and the 20-year rows come from **different carriers** and
the model never mixes them: a 갱신형 point reaches published 10-year cells, and the
extension for an unpublished cell runs off the 20-year anchor. That the two carriers are at
the same level is checkable — on the disclosure basis the 흥국생명 비갱신형 20-year premium
is ₩15,000 against the anchor's ₩15,080 [S4] — which is what makes carrying both defensible.

### Decrement recursion and processing order

For `t = 0..N−1`, **in this order**, and the order is load-bearing:

1. **Start of the month, time `t`.** `l(t)` is the opening exposure and the weight on
   **every** cash flow of that `result_cf()` row. `l(0) = pols_if_init() = 1`.
2. **Premium and start-of-month expense.** Premium income `P_m(k(t)) × pols_payer(t)` —
   one month's office premium, which is what the contract collects — where
   `pols_payer(t) = l(t) · 1{t < 12 n_p} − pols_waived(t)`; maintenance
   `2,000 × 1.02^⌊t/12⌋ × l(t)`; renewal commission `c_r × premiums(t)` for `t ≥ 12`. At
   `t = 0` additionally `E0 × l(0)` and `c0 × l(0)`, the latter on the **annualized**
   premium.
3. **Decrement lookup.** `q(t) = 0.85 × c_q × q^tab_{x+⌊t/12⌋}` and
   `q^m(t) = 1 − (1 − q(t))^(1/12)`; `w(t)` from the interpolated lapse curve, read at the
   0-based policy year `⌊t/12⌋`, and `w^m(t) = 1 − (1 − w(t))^(1/12)`; `d(t) = d_0`, **not
   converted**, if `(t + 1) mod 12n = 0` and `t < N − 1` on a 갱신형 point, else 0.
4. **End of the month — death.** `D(t) = l(t) × q^m(t)`. Claim outgo
   `SA × (1 − a(t)) × D(t)`,
   claim expense `ec × D(t)`. One decrement, one benefit; nothing is added on top.
   `pols_if_at(t, "BEF_LAPSE") = l(t) × (1 − q^m(t))`.
5. **End of the month — ordinary lapse**, on the survivors of mortality.
   `pols_lapse(t) = l(t)(1 − q^m(t)) w^m(t)`. **Pays nothing.**
   `pols_if_at(t, "BEF_DECLINE") = l(t)(1 − q^m(t))(1 − w^m(t))`.
6. **End of the last month of a cycle — renewal decline**, on the survivors of both.
   `pols_decline(t) = l(t)(1 − q^m(t))(1 − w^m(t)) d(t)`. **Pays nothing.**
   `pols_if_at(t, "AFT_DECR") = l(t)(1 − q^m(t))(1 − w^m(t))(1 − d(t))`.
7. **부활 reinstatement and maturity.** `pols_reinstate(t) = lap(t) × rho` is added back,
   `rho` being the monthly reinstatement rate and the window 36 months.
   In the last month only, `pols_maturity(N−1) = pols_if_at(N−1, "AFT_DECR") +
   pols_reinstate(N−1)`
   removes everything remaining and pays `cum_prem_pp(N−1)` on a `rop` point and **nothing**
   on a `pure` one.

   Because the twelve monthly decrements of a policy year compound to that year's annual
   rates exactly, `l` at each 계약해당일 — and `pols_maturity(N−1)` at the end — are
   **unchanged** from what an annual step produced. The month-by-month exposure between
   anniversaries is what moved, and every cash flow weighted by it moved with it.

The roll-forward identity, asserted at every `t` by `check_pols_roll_fwd()`:

    l(t) - l(t+1) - D(t) - pols_lapse(t) - pols_decline(t) - pols_maturity(t)
        + pols_reinstate(t) = 0

with `l(N) = 0` exactly on every model point — `l` is defined one step past the frame, at
the time the horizon is reached. The reinstatement and maturity terms are
carried in the identity whether or not the modules are on, so the same residual closes in
both positions of every switch rather than one form of the check being right for each.

**Why the order matters, in one number.** The multiplicative roll-forward is
order-invariant: `l(t+1)` is the same however the three factors are permuted. The
**decomposition is not**. On the 갱신형 anchor at the first boundary (`t = 119`, the last
month of the tenth
policy year,
`l = 0.7268743823`, `q^m = 0.0000903865`, `w^m = 0.0015983709`, `d = 0.20`) the shipped
order gives deaths **0.0000656996**, lapses 0.0011617099 and declines **0.1451293946**.
Applying the decline first gives deaths **0.0000525597** — **20% fewer** — with `l(120)`
identical to the last digit. Since claims are `SA × D(t)`, a model that reverses the order
books **₩5,255.97** of boundary-month death claims instead of **₩6,569.96** and never
notices, because its policy roll-forward still closes.

The monthly grid also settles what the decline *is*. It is the only rate in this model that
is **not** converted: `q` and `w` are forces acting through a period and are compounded down
to the month, while `d` is a discrete election on a single date and enters at its own level
in the one month the boundary falls in. The three exits then stand at roughly 2,200 : 18 : 1
— where an annual step mixed the election with a whole year of continuous lapse and made it
look like 90.7% of a mixed population.

### Net cash flow

    CF(t) = P_m(k(t)) * pols_payer(t)                       (premiums, one month's)
          - SA * (1 - a(t)) * D(t)                          (death claims)
          - SA * a_q(t) * (1 - a(t)) * D(t) * 1{acc_death}  (재해사망 uplift)
          - accel_payout_pp(t) * a(t) * D(t)                (선지급)
          - cum_prem_pp(t) * pols_maturity(t) * 1{rop}      (만기보험금)
          - 0                                               (claims_lapse: nil, always)
          - ec * D(t)                                       (claim expense)
          - (E0 * l(0)) * 1{t = 0} - e(t) * l(t)            (acquisition + maintenance)
          - (c0 * l(0)) * 1{t = 0} - c_r * premiums(t) * 1{t >= 1}   (commission)

`net_cf` is **income-positive**, per the library convention, and there is no outgo-positive
`liability_cf` companion: one stream, one sign, one name. Ordinary lapse and renewal
decline contribute **no term at all** — they act only through `l(t)`. `claims_lapse` is a
published column of zeros rather than an omitted column, because the 표준형 comparator *does*
have a surrender value [S2 제33조] [S12] and a reader must not infer the nil from the
product class.

`check_net_cf()` re-derives the residual **from the published `result_cf()` columns**, not
from the cells behind them, so the identity a reader adds up by hand with a calculator is
the identity the model asserts. It is the reason no `claims` aggregate column is published:
the split columns must sum to `net_cf` with the expense and commission columns, and an
aggregate beside them would double-count.

The seven checks, all argument-free and all returning a real `bool`, all `True` on all ten
shipped model points:

| Check | Identity |
|---|---|
| `check_pols_roll_fwd` | the roll-forward above, tolerance `1e-12` |
| `check_lapse_pool` | `lap(t) − lap(t+1) − pols_reinstate(t) − pols_lapse_expire(t) + pols_lapse(t) = 0` |
| `check_pols_payer` | `l(t)·1{t < n_p} − pols_payer(t) − pols_waived(t) = 0` |
| `check_prem_level` | `P_a(t) = P_a(t−1)` **within** a cycle — the premium is level, and only within |
| `check_decline_timing` | `d(t) > 0` **iff** `(t + 1) mod n = 0` on a 갱신형 point and `t < N − 1` |
| `check_waiver_reset` | `u(t) = 0` at `t = 0` and in the **first month of every renewed cycle** [S6] |
| `check_net_cf` | the ledger above, read back off `result_cf()`, tolerance `1e-6` |

### Optional modules (all off in the base run)

- **보험료 납입면제** (`waiver`). A waived-fraction state, not a claim:

      u(0) = 0;  u(t) = u(t-1) * (1 - r_rec) + (1 - u(t-1)) * i_wop
      u(t) = 0   whenever t is the first month of a renewed cycle, or t >= 12 n_p

  with `i_wop = 0.0008` and `r_rec = 0` **[std]**, and the reset **sourced** [S6]. While
  the waiver runs, premium income stops and cover continues [S2 제5조제1항]; on the
  만기환급형 the maturity benefit is still computed as if the waived premiums had been paid
  [S1] [S12]; and on a 무해지 shortened-pay form entering the state **destroys the
  post-완납 surrender-value step-up** [S2 제33조제2항 단서] [S12]. On for model points 3 and
  4, which are 갱신형, so that the reset is exercised and not merely asserted.
- **선지급서비스특약** (`accel`). Amount `A = SA` where `SA ≤ ₩10,000,000`, else
  `min(0.5 × SA, ₩50,000,000)` [S2 제4조]; payout

      accel_payout_pp(t) = A * v^1 - (12 * P_m(t) * A / SA * 1{t < n_p}) * v^0.5,
      v = 1 / (1 + 0.025)

  at the 평균공시이율 the 약관 names [S2 제4조제6항] [S12] over the sourced 12-month
  prognosis [S2 제3조]; take-up `a(t) = 0.10` **[std]**. The accelerated share is taken
  **out of** the death claim (`claims_death` carries `1 − a(t)`) rather than added beside
  it, because the 보험가입금액 is treated as reduced by the amount paid from the payment
  date [S2 제4조]. **At the anchor's ₩100,000,000 the cap is exactly reached and reduces
  nothing**: `0.5 × 100,000,000 = 50,000,000 = accel_cap`, so `accel_cap_binds()` is
  `False` on a **strict** inequality. On for model points 7 (cap does not bind, `A =
  ₩15,000,000`) and 9 (cap binds, `A = ₩50,000,000` against `0.5 × SA = ₩100,000,000`).
- **부활** (`reinstatement`). A lapsed-but-reinstatable pool carried by vintage over the
  sourced three-year window [S2 제28조], carried as **36 months** so that it closes on the
  month it actually closes on — the window runs from **each life's own 실효**, so a single
  indicator on one balance drops a whole cohort early or late:

      lap(t)             = sum over s in [t - W, t - 1] of pols_lapse(s) * (1 - rho)^(t-1-s)
      pols_reinstate(t)  = lap(t) * rho
      pols_lapse_expire(t) = pols_lapse(t - W) * (1 - rho)^W

  with `rho = 1 − (1 − 0.10)^(1/12)` — the monthly equivalent of the **[std]** 10% annual
  placeholder — and `W = 36` months **[S2 제28조]**. The pool is tracked whether or
  not the module is on, so `check_lapse_pool()` closes in both positions. **Renewal
  declines never enter it**: a declined renewal is an expiry, not a 실효, and there is
  nothing to reinstate. 부활 restarts the suicide window [S2 제6조·제28조] — the only event
  that does. On for model point 8.
- **재해사망 uplift** (`acc_death`). The product 형 two carriers sell, paying **2×** the sum
  assured on 재해사망 and 1× otherwise [S6] [S10], modelled as a **split of the existing
  decrement** using the published 예정 재해사망률 and never as a second decrement:
  `claims_acc_death(t) = SA × a_q(t) × (1 − a(t)) × D(t)`, beside the full
  `claims_death(t)`. On for model point 10.
- **Contract boundary** (`contract_boundary`). `current_term` truncates at the end of the
  cycle in force. `ceiling` on model point 3, `current_term` on model point 4 — the same
  cell, both readings.
- **Renewal-decline elasticity** (a Reference, not a column).
  `d(t) = min(d_max, d_0 × (P_a(k+1) / P_a(k))^beta)` with `beta = 0` in the base run
  giving the flat 20%, `d_0 = 0.20` and `d_max = 0.40`.
- **Commission at a 갱신** (a Reference). `comm_new_term_rate = 0` in the base run, paid on
  the first month of each renewed cycle, `t = 12(k − 1)n`, when set.

### What the third-sector chassis inherits

Unchanged from this file in the
[critical illness technical notes (CI보험)](../ci_insurance/technical-notes.md) and the
[cancer technical notes (암보험)](../cancer/technical-notes.md): the seven-step processing
order, the roll-forward identity and its check, the premium chassis
`P_m = r × c_p × g × SA / 100,000,000` with its 갱신 repricing and its ceiling truncation,
the renewal-decline treatment and its ordering, the [std] mortality construction and the
0.85 factor over it, the lapse curve and its two [std] steps and the annual-to-monthly
conversion over it, the monthly grid itself, the expense and commission structure, the
보험나이 age basis and the timing conventions. What changes there: a
**second decrement that is not death** — 진단 incidence — with its own 면책기간 and 감액기간,
and, on `Cancer_KR_S`, an incidence basis that is
**sourced** from the published 참조순보험요율 [REG-R61] rather than standardized, which this
product's mortality cannot be.

---

## Policyholder behavior modeling

All dynamic forms are **[std]** reference constructions. Korean public evidence on
behaviour is thin in a specific way: the *pricing* lapse assumption is published and its
functional form is prescribed [S12] [S1] [REG-R27], while *experience* is not published at
all for term business, and renewal take-up is not published for any product.

- **Base lapse [std].** The prescribed log-linear curve between disclosed endpoints, above.
  `lapse_be_factor = 1.0` sets the best estimate equal to the pricing basis, which is a
  choice and a questionable one — a 무해지 pricing rate is deliberately low by regulatory
  design [REG-R19 제7-66조제4항](#krlib-reg-r19) — and the only Korean experience datum in the set points at
  a **materially higher** true rate [R18]. Channel is not represented, and the disclosure
  shows it should be: nine of the nineteen retail rows are CM (online) products [S4], and
  direct-sold and agent-sold persistency are not the same. No split is published.
- **Renewal decline [std].** `d = 20%`, flat, non-zero only in the last month of a cycle and zero in
  the last projected month `t = N − 1`, where cover ends at the ceiling rather than
  renewing. It is the one behavioural rate that is **not** converted to a monthly
  equivalent, being an election on a single date rather than a force acting through a
  period. The
  refinement the flat rate defers is that decline should rise with the size of the
  repricing step, and on the published path the step **accelerates**: ×2.33, then ×2.67,
  then ×3.59 [S7]. The elasticity form is implemented and switched off:

      d(t) = min(d_max, d_0 * (P_a(k+1) / P_a(k)) ** beta)

  with `beta = 0` in the base run. The cap is a guard on the form rather than a behavioural
  view: at `beta = 1` the largest observed jump (×3.59) reaches 72% and the cap binds at
  every boundary, so a user turning the elasticity on must re-argue `d_max` at the same
  time.
- **Selective lapsation [std scope] — specified, not implemented, and the omission is
  one-directional.** The Korean 갱신 takes **no 고지 and no underwriting** [S6] [S9] [S15],
  so a life that has become uninsurable elsewhere renews at the portfolio price while a
  healthy life re-shops. The mechanism is exactly the one that makes the *long* reading of
  the contract boundary arguable, and the base run's constant `q` understates late-cycle
  claims by construction. A reference form is
  `q_eff(t) = q(t) × [1 + lambda × max(0, 1 − l(t))]`; the model carries `lambda = 0`
  implicitly by not carrying the term at all, and this file says so rather than leaving the
  absence to be discovered.
- **Rate-class transitions — a Korean peculiarity with no analogue anywhere in this
  repository.** The Korean rate class is a **state**, not an attribute fixed at issue. A
  class rider tracks the insured's smoking status for the life of the contract and moves in
  **both** directions [S2 건강체서비스특약Ⅱ 제4조]. If the life smokes for 30 days or more
  the policyholder must notify without delay; the insurer recovers a **정산차액** and
  reverts to the 표준체 scale, or, if arrears go unpaid, **reduces the 보험가입금액 in the
  ratio of the two premiums**. In the other direction a standard life who quits and passes
  the tests may upgrade mid-term, and the same path exists at two more carriers for a life
  originally accepted under a substandard rider [S11] [S12]. `Term_KR_S` carries the class
  as a **parameter only**. A model that later needs the movement will need a *transition*,
  not a relabelling.
- **감액.** Permitted, premium reset, and on this form **no payment arises**, there being no
  surrender value to release [S2] [S12]. Not modelled: it changes `SA` and `P_a` together,
  which is a model-point re-parameterization rather than a decrement **[std scope]**.
  **증액 is not available at all**; a new contract with fresh underwriting is required
  [S1] [S12].
- **청약철회.** Out of scope: the projection begins with cover in force and the statutory
  population — 15일 from receipt of the 보험증권 and never more than 30일 from application,
  45일 for a policyholder aged 65 or over contracting by telephone — already out
  [S2 제18조] [REG-R25 제17조](#krlib-reg-r25) [REG-R51].
- **위법계약의 해지.** Not modelled and **not nil**. It returns the whole **계약자적립액**
  with no surrender charge, within 1년 of learning of a selling-rule breach and 5년 of the
  contract date [S2 제30조의2] [REG-R25 제29조의2](#krlib-reg-r25). On a form whose ordinary surrender pays
  nothing this is worth the entire value of the contract to the policyholder who invokes
  it. No incidence of mis-selling findings is published, so it cannot be sized; it is stated
  because a Korean model treating the surrender value as uniformly nil would be wrong about
  a real if small cash flow.
- **Claim lag.** The timetable is contractual and real — 3영업일 / 10영업일 / 30영업일 with
  a 가지급보험금 of up to 50% [S2 제9조] — but no Korean document publishes the mix of claims
  falling into the three bands, so any split would be invented. The model pays at the
  projection step in which the claim arises and says so.

---

## Worked example

**Anchor cell (`point_id = 1`, `KR-TL-0001`).** Male, 가입나이 **보험나이 40**, **20년만기
전기납**, 비갱신형, 보험가입금액 **₩100,000,000 (1억원)**, **표준체**, 순수보장형 해약환급금
미지급형, 월납. Renewal ceiling 80 (inert on a 비갱신형 point). Base run: no 재해사망
uplift, no 납입면제, no 선지급, no 부활, boundary = `ceiling`. Horizon
`proj_years() = 20` years, `N = proj_len() = 240` **months**; 납입기간 `n_p = 20` years
(전기납, `pay_term_y = 0` resolving to `proj_years()`).

This is the cell that is doubly prescribed in Korea — the 감독규정's 기준연령 요건 [REG-R9]
and the 생명보험협회 disclosure's 대표계약 [S5] — so the premium below is not a
standardization but a **published figure appearing twice independently**, in the carrier's
own 상품요약서 grid and as that product's row in the cross-carrier disclosure, agreeing to
the won [S12] [S4]. Observed premiums for the same risk at other carriers: ₩14,400 /
₩15,000 / ₩16,000 / ₩16,000 / ₩16,100 / ₩18,400 [S4].

**Every assumption value the cell uses.**

| Quantity | Value | Tag |
|---|---|---|
| `prem_rate_mth(0)` | **15,080** per month per ₩100,000,000 — the published cell `(pure, M, 40, 20)`, read directly and not extended | [S12] [S4] |
| `class_prem_ratio()` | 1.000000 (표준체 is the reference class) | [S12] |
| `pay_factor(1)` | 1.0 (전기납: `m_p = m`, so no uplift; the argument is the **cycle** `k = 1`) | mechanic |
| `premium_mth_pp(0)` | `round_10(15,080 × 1 × 1 × 1) = ` **₩15,080** | [S12] [S4] |
| `prem_pp(0)` | `12 × 15,080 = ` **₩180,960**, a reporting quantity and the commission base | annualization, exact in amount |
| `premiums(0)` | **₩15,080** — the month's actual income, one month's premium | mechanic |
| `mort_be_factor` | **0.85** | **[std]** |
| `class_mort_ratio()` | 1.000000 | [S12] |
| `mort_rate_mth(0)` | `1 − (1 − 0.00055250)^(1/12) = ` **0.0000460533** | conversion **[std]** |
| `lapse_be_factor` | **1.0** — the best estimate is set equal to the disclosed 적용해지율 | **[std]** |
| Lapse endpoints | 4.6% in policy year 1, 0.1% in policy year `n_p = 20`; `post_payment` 0.8% never reached | [S12] [S1] [REG-R27] |
| `lapse_rate_mth(0)` | `1 − (1 − 0.046)^(1/12) = ` **0.0039166106** | conversion **[std]** |
| `expense_acq` | **₩120,000**, `t = 0` only | **[std]** |
| `expense_maint` | **₩2,000** per **month** — the same ₩24,000 a year — `× 1.02^⌊t/12⌋` | **[std]** |
| `expense_claim` | **₩300,000** per death claim | **[std]** |
| `comm_init_rate` | **0.60** of `prem_pp(0)`, at `t = 0` | **[std]** |
| `comm_renewal_rate` | **0.03** of `premiums(t)`, from `t = 12` (policy year 2) | **[std]** |
| `comm_new_term_rate` | **0** (no boundary on this point in any case) | **[std]** |
| `renewal_decline_rate(t)` | **0 at every `t`** — a 비갱신형 point has no boundary | mechanic [S1] [S12] |
| `wop_waived_frac(t)` | **0 at every `t`** — module off | mechanic |

**The decrement basis, policy year by policy year.** One row per policy year `y`, read at
its first month `t = 12(y − 1)` and level through all twelve: 보험나이 increments on the
계약해당일 and not on the birthday [S2 제22조], and the published rates are annual, so a
within-year interpolation would be modelling an age the contract does not recognize.
`q_x^tab` is the shipped 표준체 pricing rate at attained **보험나이** `x + y − 1`; the age-40
row is a **disclosed anchor** [S12] and every other row is the [std] Makeham fit.
`q = 0.85 × q_x^tab` and `w = 0.046 × (0.001/0.046)^((y−1)/19)` are the **sourced annual**
quantities; `q^m = 1 − (1 − q)^(1/12)` and `w^m = 1 − (1 − w)^(1/12)` are the [std]
conversions the roll-forward actually applies. `l` is the in-force at the start of the
year, i.e. at `t = 12(y − 1)`.

| y | 보험나이 | `q_x^tab` | `q` | `q^m` | `w` | `w^m` | `l` |
|---:|---:|---|---|---|---|---|---|
| 1 | 40 | 0.00065000 | 0.00055250 | 0.0000460533 | 0.0460000000 | 0.0039166106 | 1.0000000000 |
| 2 | 41 | 0.00069504 | 0.00059078 | 0.0000492453 | 0.0376048847 | 0.0031890865 | 0.9534729150 |
| 3 | 42 | 0.00074482 | 0.00063310 | 0.0000527734 | 0.0307418990 | 0.0025986464 | 0.9170755621 |
| 4 | 43 | 0.00079985 | 0.00067987 | 0.0000566737 | 0.0251314254 | 0.0021188032 | 0.8883201687 |
| 5 | 44 | 0.00086067 | 0.00073157 | 0.0000609846 | 0.0205448773 | 0.0017284095 | 0.8654066502 |
| 6 | 45 | 0.00092789 | 0.00078871 | 0.0000657493 | 0.0167953857 | 0.0014105066 | 0.8470068787 |
| 7 | 46 | 0.00100219 | 0.00085186 | 0.0000710162 | 0.0137301857 | 0.0011514463 | 0.8321242517 |
| 8 | 47 | 0.00108431 | 0.00092166 | 0.0000768378 | 0.0112243924 | 0.0009402128 | 0.8199999093 |
| 9 | 48 | 0.00117508 | 0.00099882 | 0.0000832730 | 0.0091759127 | 0.0007678942 | 0.8100486275 |
| 10 | 49 | 0.00127541 | 0.00108410 | 0.0000903865 | 0.0075012856 | 0.0006272667 | 0.8018140251 |
| 11 | 50 | 0.00138630 | 0.00117836 | 0.0000982493 | 0.0061322822 | 0.0005124655 | 0.7949366641 |
| 12 | 51 | 0.00150887 | 0.00128254 | 0.0001069412 | 0.0050131253 | 0.0004187234 | 0.7891309148 |
| 13 | 52 | 0.00164435 | 0.00139770 | 0.0001165495 | 0.0040982174 | 0.0003421613 | 0.7841678848 |
| 14 | 53 | 0.00179408 | 0.00152497 | 0.0001271696 | 0.0033502824 | 0.0002796198 | 0.7798626566 |
| 15 | 54 | 0.00195959 | 0.00166565 | 0.0001389104 | 0.0027388475 | 0.0002285243 | 0.7760646153 |
| 16 | 55 | 0.00214252 | 0.00182114 | 0.0001518887 | 0.0022390010 | 0.0001867752 | 0.7726499798 |
| 17 | 56 | 0.00234471 | 0.00199300 | 0.0001662355 | 0.0018303777 | 0.0001526596 | 0.7695160610 |
| 18 | 57 | 0.00256820 | 0.00218297 | 0.0001820964 | 0.0014963292 | 0.0001247797 | 0.7665767149 |
| 19 | 58 | 0.00281521 | 0.00239293 | 0.0001996297 | 0.0012232453 | 0.0001019943 | 0.7637587538 |
| 20 | 59 | 0.00308823 | 0.00262500 | 0.0002190132 | 0.0010000000 | 0.0000833716 | 0.7609991050 |

The whole `q` column is a **[std]** construction save the single age-40 anchor, and the `w`
column is a prescribed shape between two disclosed endpoints. That asymmetry — a sourced
premium against a constructed basis — is the shape of every Korean product document in this
library.

### The cash flow statement, the first policy year

All amounts in won, to two decimals, exactly as `result_cf()` produces them. The statement
runs to `t = 239`; printed here are the **first policy year**, `t = 0 … 12`, and then the
milestone rows, which is how every monthly model in this library prints its worked example.
`claims_acc_death`, `claims_accel`, `claims_maturity` and `claims_lapse` are **0.00 in
every row** of this model point and are omitted from the table; they are published columns
and their zeros are asserted, not implied.

| t | `pols_if` | `premiums` | `claims_death` | `claim_expenses` | `expenses` | `commissions` | `net_cf` |
|---:|---|---:|---:|---:|---:|---:|---:|
| 0 | 1.0000000000 | 15,080.00 | 4,605.33 | 13.82 | 122,000.00 | 108,576.00 | **−220,115.15** |
| 1 | 0.9960375164 | 15,020.25 | 4,587.08 | 13.76 | 1,992.08 | 0.00 | 8,427.33 |
| 2 | 0.9920907341 | 14,960.73 | 4,568.91 | 13.71 | 1,984.18 | 0.00 | 8,393.93 |
| 3 | 0.9881595909 | 14,901.45 | 4,550.80 | 13.65 | 1,976.32 | 0.00 | 8,360.67 |
| 4 | 0.9842440247 | 14,842.40 | 4,532.77 | 13.60 | 1,968.49 | 0.00 | 8,327.54 |
| 5 | 0.9803439739 | 14,783.59 | 4,514.81 | 13.54 | 1,960.69 | 0.00 | 8,294.54 |
| 6 | 0.9764593770 | 14,725.01 | 4,496.92 | 13.49 | 1,952.92 | 0.00 | 8,261.68 |
| 7 | 0.9725901728 | 14,666.66 | 4,479.10 | 13.44 | 1,945.18 | 0.00 | 8,228.94 |
| 8 | 0.9687363002 | 14,608.54 | 4,461.35 | 13.38 | 1,937.47 | 0.00 | 8,196.33 |
| 9 | 0.9648976985 | 14,550.66 | 4,443.68 | 13.33 | 1,929.80 | 0.00 | 8,163.86 |
| 10 | 0.9610743072 | 14,493.00 | 4,426.07 | 13.28 | 1,922.15 | 0.00 | 8,131.51 |
| 11 | 0.9572660661 | 14,435.57 | 4,408.53 | 13.23 | 1,914.53 | 0.00 | 8,099.29 |
| 12 | 0.9534729150 | 14,378.37 | 4,695.41 | 14.09 | 1,945.08 | 431.35 | **7,292.44** |

The thirteenth row is the first month of policy year 2, where three things change at once:
the attained 보험나이 turns 41, the expense inflation factor makes its first step, and the
renewal commission starts. Beyond it, the **milestone rows** — the first month of policy
years 6 and 11, the first month of the second half of the term, and the last projected
month:

| t | `pols_if` | `premiums` | `claims_death` | `claim_expenses` | `expenses` | `commissions` | `net_cf` |
|---:|---|---:|---:|---:|---:|---:|---:|
| 12 | 0.9534729150 | 14,378.37 | 4,695.41 | 14.09 | 1,945.08 | 431.35 | 7,292.44 |
| 60 | 0.8470068787 | 12,772.86 | 5,569.01 | 16.71 | 1,870.33 | 383.19 | 4,933.63 |
| 120 | 0.7949366641 | 11,987.64 | 7,810.20 | 23.43 | 1,938.05 | 359.63 | 1,856.34 |
| 180 | 0.7726499798 | 11,651.56 | 11,735.68 | 35.21 | 2,079.77 | 349.55 | −2,548.64 |
| 239 | 0.7584718208 | 11,437.76 | 16,611.54 | 49.83 | 2,209.90 | 343.13 | **−7,776.65** |

The rows where the product does something: **`t = 0`**, the acquisition strain, the only
month carrying `expense_acq` and `comm_init_pp`, and where the whole acquisition charge —
₩228,576 — stands against **one month's** premium of ₩15,080 rather than against a year's;
**`t = 12`**, the turn of the policy year; **`t = 155/156`**, where the monthly margin
crosses zero as the level premium falls behind the rising mortality cost; and
**`t = 239`**, the maturity month, where `pols_maturity(239) = 0.7582424843` removes the
entire surviving cohort and **pays nothing**, `maturity_form` being `pure`. That last
count is the annual grid's own to the last bit, which is the check that the change of grid
re-timed the exposure and left the survivorship the sourced annual rates imply. There is no
renewal row on this point, and `check_decline_timing()` asserts that there is none.

Load-bearing values at full float64 precision, for a reader reconciling to the model rather
than to this table:

    pols_if(0)         1.0
    pols_if(1)         0.9960375164203861
    pols_if(12)        0.9534729149999999  (the annual grid's own l(1), to the last bit)
    pols_if(24)        0.9920907341168909 x ... = 0.917075562112279 at t = 24
    pols_if(120)       0.7949366641324892
    pols_if(239)       0.7584718208001523
    pols_if(240)       0.0
    premium_mth_pp(t)  15080.0             (every t: the premium is level, 비갱신형)
    prem_pp(t)         180960.0            (12 x P_m, the commission base and the report)
    premiums(1)        15020.245747619421
    mort_rate_mth(0)   4.605332987672739e-05
    lapse_rate_mth(0)  0.003916610622698213
    claims_death(0)    4605.332987672738   (= 100,000,000 x q^m(0); prints 4,605.33)
    claim_expenses(0)  13.815998963018217
    expenses(0)        122000.0            (= 120,000 acquisition + 2,000 maintenance)
    commissions(0)     108576.0            (= 0.60 x 180,960, the annualized premium)
    net_cf(0)          -220115.14898663576
    net_cf(1)          8427.325030154227
    net_cf(12)         7292.4400417024035
    net_cf(120)        1856.3392698344896
    net_cf(239)        -7776.65049712519

### Hand traces

**`t = 0`, the first policy month — the acquisition strain.** `l(0) = 1`,
`prem_payable(0) = 1`,
`wop_waived_frac(0) = 0`, so `pols_payer(0) = 1`.

    premiums(0)       = 15,080 x 1                        =  15,080.00
    q(0)              = 0.85 x 1.000000 x 0.00065         = 0.0005525        (annual)
    q^m(0)            = 1 - (1 - 0.0005525)^(1/12)        = 0.0000460533
    pols_death(0)     = 1 x 0.0000460533                  = 0.0000460533
    claims_death(0)   = 100,000,000 x (1 - 0) x 0.0000460533 =   4,605.33
    claim_expenses(0) = 300,000 x 0.0000460533            =      13.82
    expenses(0)       = 120,000 x 1 + 2,000 x 1.02^0 x 1  = 122,000.00
    commissions(0)    = 0.60 x 180,960 x 1                = 108,576.00
    net_cf(0)         = 15,080.00 - 4,605.33 - 13.82 - 122,000.00 - 108,576.00
                      = -220,115.15

Roll forward, in the processing order and no other. After mortality,
`1 × (1 − 0.0000460533) = 0.9999539467`. `w(0) = 0.046` annual, so
`w^m(0) = 1 − (1 − 0.046)^(1/12) = 0.0039166106`,
`pols_lapse(0) = 0.9999539467 × 0.0039166106 = 0.0039164302` and after ordinary lapse
**`l(1) = 0.9960375164203861`**. `d(0) = 0`, `pols_reinstate(0) = 0`,
`pols_maturity(0) = 0`.

The first **month's** outgo is ₩235,195.15 against ₩15,080.00 of premium, and the
acquisition charge alone — ₩228,576 — is **15.2 times** the month's premium. That ratio is
the one the monthly grid exists to print. An annual step netted the same charge against a
whole year of premium and reported 126%, which is a true statement about a year and not
about the cash flow that happens at issue; the strain a Korean protection contract actually
starts from is this one, and it is why the first months' lapse rates decide how long it
takes to recover. The initial commission is nonetheless computed on `prem_pp(0)`, the
**annualized** premium, because that is the unit a Korean commission scale is written in
[REG-R29].

**`t = 1` — the first ordinary month, and the only kind of row where nothing at all is
exceptional.**

    premiums(1)       = 15,080 x 0.9960375164203861       =  15,020.24574762
    q^m(1)            = 0.0000460533                      (unchanged: still 보험나이 40)
    pols_death(1)     = 0.9960375164 x 0.0000460533       = 0.00004587084431
    claims_death(1)   = 100,000,000 x 0.00004587084431    =   4,587.08443133
    claim_expenses(1) = 300,000 x 0.00004587084431        =      13.76125329
    expenses(1)       = 2,000 x 1.02^0 x 0.9960375164     =   1,992.07503284
    commissions(1)    = 0                                 (policy year 1: none)
    net_cf(1)         = 15,020.24574762 - 4,587.08443133 - 13.76125329
                        - 1,992.07503284 - 0
                      = 8,427.32503015

Roll forward: after mortality `0.9960375164 − 0.0000458708 = 0.99599164557607`;
`w^m(1) = 0.0039166106` still, so `pols_lapse(1) = 0.00390091145918` and
`l(2) =` **0.9920907341168909**. There is **no acquisition expense, no initial commission
and no renewal commission** in this row: `expense_acq` and `comm_init_pp` are `t = 0` only,
and the renewal commission does not start until policy year 2.

**`t = 12` — the turn of the policy year, where three things move at once.**

    premiums(12)       = 15,080 x 0.953472915             =  14,378.37155820
    q(12)              = 0.85 x 0.00069504                = 0.00059078400   (보험나이 41)
    q^m(12)            = 1 - (1 - 0.000590784)^(1/12)     = 0.0000492453
    pols_death(12)     = 0.953472915 x 0.0000492453       = 0.00004695409395
    claims_death(12)   = 100,000,000 x 0.00004695409395   =   4,695.40939497
    claim_expenses(12) = 300,000 x 0.00004695409395       =      14.08622818
    expenses(12)       = 2,000 x 1.02 x 0.953472915       =   1,945.08474660
    commissions(12)    = 0.03 x 14,378.37155820           =     431.35114675
    net_cf(12)         = 14,378.37155820 - 4,695.40939497 - 14.08622818
                         - 1,945.08474660 - 431.35114675
                       = 7,292.44004170

The attained 보험나이 turns 41, the expense inflation factor makes its first step, and the
renewal commission starts — all on the 계약해당일 and none of them before it. `l(12) =`
**0.9534729149999999**, which is the annual-grid model's own `l(1)` to the last bit: twelve
monthly exits at `1 − (1 − q)^(1/12)` compound to the year's annual rate exactly, so the
anniversary in-force is unchanged and only the exposure inside the year has moved.

**`t = 239`, the last projected month — the maturity month, where the 순수보장형 pays
nothing.**

    premiums(239)       = 15,080 x 0.7584718208001523     =  11,437.75505767
    q(239)              = 0.85 x 0.00308823               = 0.00262499550   (보험나이 59)
    q^m(239)            = 1 - (1 - 0.0026249955)^(1/12)   = 0.0002190132
    pols_death(239)     = 0.7584718208 x 0.0002190132     = 0.00016611537844
    claims_death(239)   = 100,000,000 x 0.00016611537844  =  16,611.53784435
    claim_expenses(239) = 300,000 x 0.00016611537844      =      49.83461353
    expenses(239)       = 2,000 x 1.02^19 x 0.7584718208  =   2,209.90044518
    commissions(239)    = 0.03 x 11,437.75505767          =     343.13265173
    net_cf(239)         = 11,437.75505767 - 16,611.53784435 - 49.83461353
                          - 2,209.90044518 - 343.13265173
                        = -7,776.65049713

Roll forward, and this is the row where the maturity mechanic shows. After mortality
`0.7584718208 × (1 − 0.0002190132) = 0.75830570542171`. `w(239) = 0.001` annual — the
disclosed convergence point reached at 납입완료 [S12] [REG-R27], held level through the
whole of the twentieth policy year — so `w^m(239) = 0.0000833716`,
`pols_lapse(239) = 0.00006322112370` and after ordinary lapse `0.75824248429801`.
`d(239) = 0`, so `pols_if_at(239, "AFT_DECR") = 0.75824248429801` and
**`pols_maturity(239) = 0.7582424842980076`**, removing the entire surviving cohort — the
annual grid's own count, again to the last bit.
`claims_maturity(239) = cum_prem_pp(239) × pols_maturity(239) × 1{rop} = 0` because
`maturity_form()` is `pure`. `l(240) = 0` **exactly**,
which is what `check_pols_roll_fwd()` asserts at `t = 239`. On the `rop` variant the same
row would pay `cum_prem_pp(239) = ₩3,619,200` per surviving policy — 240 monthly premiums
of ₩15,080, which is exactly what twenty annualized premiums came to on the annual grid:
the amount is not a grid quantity, only its timing was [S1] [S8] [S12].

### Undiscounted totals over `t = 0..239`

| Column | Total |
|---|---:|
| `pols_if` (the exposure column summed, now over 240 months) | 196.5791307004 |
| `premiums` | **₩2,964,413.29** |
| `claims_death` | **₩2,063,167.17** |
| `claims_acc_death` / `claims_accel` / `claims_maturity` / `claims_lapse` | **0.00** each |
| `claim_expenses` | ₩6,189.50 |
| `expenses` | ₩594,050.31 |
| `commissions` | ₩192,196.36 |
| **`net_cf`** | **+₩108,809.94** |

Premium income falls ₩20,147.75 against the annual grid's ₩2,984,561.04, which is the whole
of the change and is not a rounding: the annual step collected a full year's premium from
lives that lapsed or died during the year, and the monthly step does not. Death claims fall
with it, by less, because the benefit is now paid in the month of death rather than a year
later on a cohort thinned in between.

Decrement totals over the same twenty years: `sum pols_death = 0.0206316717`,
`sum pols_lapse = 0.2211258440`, `pols_maturity(239) = 0.7582424843`, and
`pols_if(240) = 0.0`. Those four sum to 1.0000000000 to the last displayed digit, which is
the roll-forward identity read as a cohort decomposition: of a hundred policies issued,
**2.07 die, 22.10 lapse and 75.82 reach the end of the twenty years**, and there is no
renewal decline on this point at all.

### Reading the shape

Cumulative `net_cf` runs −220,115.15 at `t = 0`, back through zero **during month 30**
(−3,612.96 at `t = 29`, +2,934.05 at `t = 30`), up to a peak of **+₩436,338.80 at
`t = 155`**, and then down to +₩108,809.94 at `t = 239`. That is the protection shape in
its purest form and every part of it is mechanical. The first **month** is a deep strain
because ₩228,576 of acquisition cost meets ₩15,080 of premium, and it takes **two and a
half years** to earn that back — which is the honest statement of the recovery period, and
the one an annual grid could only round to "during year 3". Months 30 to 155 are the
level-premium surplus: the premium is flat at ₩15,080 per policy in force while `q` is
still small, so margin runs at roughly half the premium and decays only as the in-force
does. From `t = 156` the level premium falls behind the mortality cost — the table rate has
multiplied by **4.75** between 보험나이 40 and 59 while the premium has not moved at all —
and the last seven years give back **₩327,528.85**, 75% of the peak. Over the whole term
premium income is **1.44×** death claims, and expenses plus commission are **26.5%** of
premium, of which **29%** falls in the first month.

The peak falls at `t = 155`, which is **inside** policy year 13 and not on its anniversary.
That is the other thing the grid buys: the turn happens when a month's premium stops
covering that month's mortality cost, which is an event with a date, and an annual step can
only report the year it fell in.

Three readings follow directly and none of them requires a discount curve. First, **the
product's profit is a timing profit**: the insurer is ahead by ₩436,339 at `t = 155` and
finishes ₩108,810 ahead, so three quarters of the peak is an interest-earning float rather
than an underwriting result, which is exactly why the 적용이율 of 2.50% is a rating factor
[S1] [S12] and why an undiscounted projection is a description of cash and not of value.
Second, **the answer is a difference of large numbers**: ₩2.96m of premium against ₩2.86m of
outgo, so a 4% error anywhere flips the sign — and the female twin (model point 2), on
identical expenses and a premium 47% lower, is **−₩184,214.97**. Third, **lapse is the
insurer's friend here, and by more than the annual grid could see**: raising
`lapse_be_factor` to 2.0 moves the total from +₩108,809.94 to +₩99,649.28 and halving it to
0.5 gives +₩110,995.14, a range of ₩11,000 on a ₩109,000 answer. On a no-surrender-value
form a lapse forfeits a paying policy and saves its claims in almost equal measure, so the
lever is still modest — a **fourfold** move in the assumption is worth 10% of the answer,
against the 60% a hundred-basis-point move in `mort_be_factor` is worth. But the annual
grid reported a range of ₩3,000 and called the sensitivity third-order, and that number was
an artefact of its own timing convention: collecting a year's premium in advance and only
then applying the year's lapse credited the insurer with premium from policies that had
gone. Stepping monthly stops doing that, and the assumption's real leverage becomes
visible. On a savings chassis this sensitivity is the dominant one; here it is second-order,
and that contrast is still the single clearest statement of what a 무해지 순수보장형 term
contract is.

### The 갱신형, on one cell, both boundary readings

The signature mechanic of this product does not appear on the anchor cell at all, so the
worked example carries a second panel. **Model points 3 and 4 are the same policy** — male
40, **10년만기 갱신형** 전기납, ₩100,000,000, 표준체, 납입면제 module on, published issue
premium **₩9,000** a month [S6] [S7] [S4] — differing **only** in `contract_boundary`.

The premium ladder is read straight off the published table with **no extension**:

| cycle `k` | months `t` | policy years | attained 보험나이 | `premium_mth_pp` | `prem_pp` | index | jump |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | 0–119 | 1–10 | 40 | **₩9,000** | ₩108,000 | 1.00 | — |
| 2 | 120–239 | 11–20 | 50 | **₩21,000** | ₩252,000 | 2.33 | ×2.33 |
| 3 | 240–359 | 21–30 | 60 | **₩56,000** | ₩672,000 | 6.22 | ×2.67 |
| 4 | 360–479 | 31–40 | 70 | **₩201,000** | ₩2,412,000 | 22.33 | ×3.59 |

(The cycle index `k` is the contractual 1-based renewal label, not the time index;
`k(t) = 1 + ⌊⌊t/12⌋ / n⌋` and the policy-year column is `⌊t/12⌋ + 1`. The premium is level
for all 120 months of a cycle and steps once, on the 계약해당일 the 갱신 falls on — which is
a date the monthly grid can state and an annual one could only place in a year.)

That is 흥국생명's mandatory 예상 갱신보험료 예시 reproduced to the won [S7], with the
`(pure, M, 40, 10)` cell also being the cross-carrier disclosure figure [S4] and the
carrier's own 상품요약서 figure [S6] — **three independent appearances of one rate**.

Boundary rows, on the long reading (model point 3, `proj_len() = 480`):

| t | `pols_if(t)` | `renewal_decline_rate(t)` | `pols_decline(t)` | `wop_waived_frac(t)` | `net_cf(t)` |
|---:|---|---:|---|---|---:|
| 108 | 0.7405136863 | 0.0 | 0.0 | 0.0071770030 | −2,065.00 |
| 119 | 0.7268743823 | **0.2** | **0.1451293946** | 0.0079050974 | −2,031.58 |
| 120 | 0.5805175782 | 0.0 | 0.0 | **0.0** | **+4,689.19** |
| 239 | 0.5080959106 | **0.2** | 0.1015364175 | 0.0079050974 | −2,373.66 |
| 240 | 0.4061456699 | 0.0 | 0.0 | **0.0** | **+11,060.04** |
| 359 | 0.3708404546 | **0.2** | 0.0741053844 | 0.0079050974 | −4,501.81 |
| 360 | 0.2964215375 | 0.0 | 0.0 | **0.0** | **+36,093.65** |
| 479 | 0.2533886360 | **0.0** | 0.0 | 0.0079050974 | +897.53 |

Cycle by cycle the same statement without the noise: `net_cf` sums to **−₩172,034.54** over
the first ten years, then **+₩172,101.53**, **+₩496,178.04** and **+₩2,422,948.18**. A
contract that reprices to attained age every ten years earns nothing in the cycle carrying
its acquisition cost and progressively more in each one after it, and the whole 갱신형
economics is in those four numbers.

**Trace, `t = 119` (the last month of policy year 10) — the boundary month, on the old
premium.** `l(119) = 0.7268743822842945`,
`u(119) = 0.007905097430285151`, so
`pols_payer(119) = 0.7268743823 × (1 − 0.0079050974) = 0.7211283695` and
`premiums(119) = 9,000 × 0.7211283695 = 6,490.16` — the **old** premium, because the
repricing takes effect at `t = 120` and not before.
`q(119) = 0.85 × 0.00127541 = 0.0010840985` annual, so `q^m(119) = 0.0000903865`,
`pols_death(119) = 0.0000656996` and
`claims_death(119) = 6,569.96`; `claim_expenses(119) = 19.71`;
`expenses(119) = 2,000 × 1.02^9 × 0.7268743823 = 1,737.36`;
`commissions(119) = 0.03 × 6,490.16 = 194.70`; and
`net_cf(119) = 6,490.16 − 6,569.96 − 19.71 − 1,737.36 − 194.70 = −2,031.58`.

Roll forward, in the processing order: after mortality
`0.7268743823 × (1 − 0.0000903865) = 0.7268086827`; after ordinary lapse
`× (1 − 0.0015983709) = 0.7256469728`; after the renewal decline
`× (1 − 0.20) =` **0.5805175782**. The three exits at `t = 119` are **0.0000656996** deaths,
**0.0011617099** ordinary lapses and **0.1451293946** renewal declines — the decline is
**99.2% of all exits in the boundary month**, in a ratio of roughly 2,200 : 18 : 1.

That ratio is the argument, and the monthly grid is what makes it arithmetic rather than
rhetoric. The renewal decline is **not** converted to a monthly rate and must not be: it is
a discrete election on a single date, not a force acting through a period, so it enters at
its own 20% in the one month the boundary falls in. An annual step mixed it with a whole
year of continuous lapse and reported it as 90.7% of the year's exits, which reads like a
large share of a mixed population; it is not a mixed population at all. A model folding the
decline into `w(t)` cannot see the boundary; a model applying it before mortality books 20%
fewer death claims in that row — ₩5,255.97 instead of ₩6,569.96 — and still balances its
policy roll-forward to the last digit.

**Trace, `t = 120` — the repriced cycle.** Attained 보험나이 at renewal is `40 + 10 = 50`, so
`prem_rate_mth(120) = 21,000` [S7] and `prem_pp(120) = 252,000`. The waiver **resets**:
`wop_waived_frac(120) = 0` exactly, because 흥국생명's 「갱신 전 보험료 납입면제 사유로 인한
보험료 납입면제를 적용하지 않고, 보험료를 계속 납입하여야 합니다」 [S6] means a disabled life
resumes paying — so `pols_payer(120) = l(120)` in full.

    premiums(120)       = 21,000 x 0.5805175782471496     =  12,190.87
    q(120)              = 0.85 x 0.0013863                = 0.001178355   (annual)
    q^m(120)            = 1 - (1 - 0.001178355)^(1/12)    = 0.0000982493
    pols_death(120)     = 0.5805175782471496 x 0.0000982493 = 0.00005703546
    claims_death(120)   = 100,000,000 x 0.00005703546     =   5,703.55
    claim_expenses(120) = 300,000 x 0.00005703546         =      17.11
    expenses(120)       = 2,000 x 1.02^10 x 0.5805175782  =   1,415.30
    commissions(120)    = 0.03 x 12,190.87                =     365.73
    net_cf(120)         = 12,190.87 - 5,703.55 - 17.11 - 1,415.30 - 365.73
                        = +4,689.19

Premium income is **88% higher than `t = 119`'s despite 20% fewer policies in force**,
because the premium multiplied by 2.33. That is the saw-tooth the product generates and it
is worth stating in full: `net_cf` runs −182,419.15 in the first month, positive from
`t = 1`, decaying through the cycle to −2,065.00 at `t = 108` and −2,031.58 in the boundary
month, then jumping to **+4,689.19 at `t = 120`**, and the same shape repeats three more
times with larger amplitude. Every negative month is one before a repricing and every jump
is the month after.

**The contract boundary, both ways, on the same cell.** Undiscounted net cash flow is
**+₩2,919,193.21** on the long reading (to the ceiling, 480 months, model point 3) against
**−₩181,055.18** on the short one (the cycle in force, 120 months, model point 4). It is not
only a difference of sign but of *sign convention for the whole product*: on the short
reading a 갱신형 policy is a loss-making ten-year contract that the insurer writes because
it expects to renew it, and on the long reading it is a forty-year contract that earns most
of its money after age 60. Neither number is an IFRS 17 measurement on its own, because
nothing retrieved settles the boundary [REG-R60] and the reading is [unverified].

Note also that the two are **not** the first 120 rows of one projection. Model point 4's
`net_cf` over ten years is −₩181,055.18 while model point 3's first 120 rows sum to
−₩172,034.54, and the difference is the 전기납 resolution described above: `pay_term()`
follows `proj_years()`, so the 적용해지율 decays to 0.1% over ten years on point 4 and over
forty on point 3. Truncating the horizon truncates the lapse curve with it. That is a
modelling consequence of the boundary reading, not a bug, and it is printed here so that a
reader diffing the two does not conclude otherwise.

### The other eight shipped model points, undiscounted

| pt | cell | `proj_len` (months) | years | `premium_mth_pp(0)` | `premiums` | claims | **`net_cf`** |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | M40 비갱신 20/20 1억 표준체 pure (**anchor**) | 240 | 20 | 15,080 | 2,964,413.29 | 2,063,167.17 | **+108,809.94** |
| 2 | F40, the same doubly prescribed cell | 240 | 20 | 8,010 | 1,580,824.99 | 1,063,462.97 | **−184,214.97** |
| 3 | M40 갱신 10y cycles to 80, 납입면제 on, boundary = ceiling | 480 | 40 | 9,000 | 11,517,624.04 | 7,375,134.92 | **+2,919,193.21** |
| 4 | the same cell, boundary = current_term | 120 | 10 | 9,000 | 968,241.62 | 700,446.17 | **−181,055.18** |
| 5 | M30 비갱신 20년만기 **10년납** 5천만 | 240 | 20 | 6,620 | 716,061.64 | 508,324.88 | **−485,830.35** |
| 6 | F50 비갱신 20/20 3천만 **rop (만기환급형)** | 240 | 20 | 44,250 | 8,690,062.33 | 8,740,412.26 | **−1,214,843.72** |
| 7 | M65 세만기 80 (15y) 3천만, **선지급 on** (cap does not bind) | 180 | 15 | 40,040 | 5,860,602.54 | 3,839,438.58 | **+1,075,806.25** |
| 8 | M19 비갱신 30/30 5억 **슈퍼건강체**, **부활 on** | 360 | 30 | 15,640 | 4,564,295.78 | 3,173,412.41 | **+243,765.26** |
| 9 | F45 세만기 80 (35y) **20년납** 2억 **비흡연자**, **선지급 on** (cap binds) | 420 | 35 | 109,490 | 21,576,403.98 | 13,656,519.59 | **+5,476,158.69** |
| 10 | M55 비갱신 20/20 1억 **건강체**, **재해사망 uplift on** | 240 | 20 | 49,480 | 9,566,175.55 | 6,702,926.27 | **+1,633,298.41** |

Three of these need a sentence rather than a row.

**Model point 6's loss is correct and expected.** A 만기환급형 hands back 100% of premiums
paid at maturity — **₩8,016,046.20** of `claims_maturity` on this point, beside ₩724,366.05
of `claims_death`, against ₩8,690,062.33 of premium — and is financed out of investment
income at a 적용이율 of 2.25% against the 순수보장형's 2.50% at the same carrier and at one
other [S8] [S12]; no retrieved document gives the reason for the gap, and the natural
reading — a longer-duration, tighter-guaranteed savings element — is an inference **[std]**
and not a sourced one. This model projects **undiscounted** gross liability cash flows and
never credits interest, so an undiscounted loss is what a savings-shaped contract **must**
show here. It is not evidence that the product loses money; it is evidence that an
undiscounted stream is the wrong lens for it, which is the whole reason the 종신보험 chassis
exists separately.

**Model points 2 and 5 are negative for a different and more interesting reason** — a flat
₩2,000 per-policy per-month maintenance charge against a small premium. Point 2's premium is
47% below point 1's on identical expenses, and point 5 collects ₩716,061.64 of premium over
the whole term against the anchor's ₩2,964,413.29 — 76% less, being 10년납 on half the sum
assured — while paying 240 months of the same flat ₩2,000 charge. That is the same
effect the market shows: female premiums run at 52–56% of male across the six direct
writers on the same cell and from 47% to 90% across the face-to-face and simplified-issue
rows [S4] — a spread far wider than the 66% mortality ratio at the same cell, and one no
Korean rate card lets you decompose into a rate and a per-policy fee.

**Model point 10 prints the accidental split.** On the shipped pairing the accidental share
of all-cause mortality is `acc_mort_share = 0.1236207830` at 보험나이 55, 0.0871551347 at
64 and 0.0536694127 at 74 — a ratio of two **annual** table rates, level through each policy
year and read at one attained age, so `claims_acc_death` totals ₩472,623.02 against
₩6,230,303.25 of `claims_death` — a **7.6%** uplift in claim cost for a doubled benefit. That is the
order of magnitude that lets a carrier bundle 재해사망 into a product 형 rather than pricing
it as a rider [S6] [S10].

---

## Valuation and reserve pointers

This library projects gross undiscounted cash flows. Every valuation layer consumes them
and is cited, never reproduced. Korea's stack is denser than any other in this repository
because two regimes commenced together and a third, purely Korean, layer sits on top.

- **Both regimes are live.** K-IFRS 제1117호 (IFRS 17) and K-ICS both commenced
  **2023-01-01** [REG-R14] [REG-R60], so Korea runs an economic-value solvency measure and a
  CSM-based earnings measure simultaneously and in fact, not prospectively. The 감독규정's
  reserving article is the visible trace of the switch: paragraphs ⑤ to ⑩ of the old
  제6-11조 were **deleted** on 2022-12-21, so the 고시 that used to carry accumulation rules
  now carries a taxonomy and a delegation [REG-R10]. 책임준비금 is split into
  보험계약부채 / 재보험계약부채 / 투자계약부채, each of the first two into 잔여보장요소 and
  발생사고요소, with the detailed calculation delegated to the FSS Governor [REG-R10]
  [REG-R23].
- **해약환급금준비금 — the Korean layer with no counterpart anywhere else in this
  repository.** 보험업법 제120조 → 시행령 제65조제2항제3호 → 감독규정 제6-11조의6 requires a
  **company-level** appropriation inside 이익잉여금 wherever the IFRS 17 liability restricted
  to the 잔여보장요소 falls below the aggregate 해약환급금 computed under 제7-66조제1항
  [REG-R3] [REG-R8] [REG-R11]. Two features matter to *this* product. The comparison is on
  **제7-66조제1항 even for the 제7-66조제4항 products that may contractually pay less**, so a
  무해지 form is measured against the surrender value it does **not** pay; and since
  2025-06-11 an insurer whose pre-transitional K-ICS ratio at the previous quarter-end was
  **130% or more** appropriates only **80%** of the shortfall [REG-R11]. `Term_KR_S`
  computes none of it; on the representative 전기납 form the 제7-66조제1항 value is in any
  case nil at every duration [S2 제33조제2항], so the layer bites on the **shortened-pay**
  variant and on the savings chassis rather than here.
- **The surrender-value rules this product does not exercise, and why they are still
  cited.** 감독규정 제7-66조제1항제1호 floors the surrender value at 계약자적립액 less
  해약공제액, never negative; 제1항제2호 caps the 해약공제기간 at the 납입기간 or the
  신계약비 부가기간, **capped at seven years**; 제4항 is the 무해지 dispensation itself;
  제5항 adds 미경과보험료 on termination [REG-R19]. 별표 14 caps the 해약공제액 at
  `연납순보험료의 5% × 해약공제계수 + 보험가입금액의 10/1000` [REG-R20] [R9]. On the anchor
  cell the sum-assured limb alone is ₩1,000,000 against ₩228,576 of modelled year-1
  acquisition charge, so the cap is nowhere near binding. **The binding constraint on a
  Korean term surrender value is the seven-year 해약공제기간, not the 별표 14 amount** — and
  neither is exercised by this model, whose surrender value is nil by construction.
- **K-ICS.** 감독규정 제7-2조제2항 decomposes the life and long-term-health module into seven
  sub-risks; four of them map one-for-one onto this model's assumptions — **사망위험액**
  (`mort_be_factor`), **해지위험액** (`lapse_be_factor` **and** `renewal_decline_base`),
  **사업비위험액** (`expense_acq`, `expense_maint`, `inflation_rate`) and **장해·질병위험액**
  (`wop_inc_rate`, where the waiver module is on) [REG-R13]. The sensitivities below are
  named in that vocabulary deliberately, because it is the vocabulary a Korean actuary uses.
  **해지위험액** is why the 무·저해지 lapse assumption is a supervisory issue and not only an
  earnings issue: the 대량해지 shock magnitudes, including the **고환급형** test that a
  무·저해지 form can trip, live in 시행세칙 **[별표 22]**, which was **not retrieved** and is
  known here only at second hand through 보험연구원 [REG-R26] [REG-R36]. **Anything in this
  file resting on 별표 22 is [unverified] at instrument level and says so.** `krlib` computes
  no 요구자본.
- **The IFRS17 계리가정 가이드라인 [REG-R27] is verified in its values and not in its
  form.** The lapse endpoints, the 0.1% convergence point, the 0.8% post-완납 ultimate and
  the 30%-additional-lapse floor are all verified from the 보도자료. The attachment carrying
  the **functional form** of the lapse model and the 실무상 수렴점 was never converted from
  HWP, so where this file leans on the guideline's *shape* rather than its *levels* the
  claim is **[unverified]** at instrument level.
- **The professional use of this projection.** 보험업법 제181조 and 제184조 put the
  선임계리사 behind the 기초서류 and the reserving [REG-R5], and 제5조·제127조 make the
  산출방법서 a **기초서류** filed with the FSC and **never published** [REG-R2]. That single
  fact is why `mort_be_factor` is [std] here and can be argued from a published margin in
  `jplib`.
- **Early corrective action.** 감독규정 제7-17조제1항제1호 makes a 경영개선권고 **mandatory**
  where the K-ICS ratio falls between **50% and 100%**, with 경영개선요구 and 경영개선명령 as
  the next two rungs [REG-R14]. The same 부칙 carries a **five-year 적기시정조치 deferral to
  the 2027-12-31 closing** for insurers caught by the transition [REG-R14]. `krlib` computes
  no ratio and the old and new triggers are not comparable quantities.
- **Tax, because it changes the after-tax comparison and nothing else in this repository
  works this way.** A 보장성보험료 attracts a **세액공제** — a 12% tax **credit** on premiums
  up to ₩1,000,000 a year, 15% where the 장애인전용보험전환특약 is attached — and not a
  deduction [REG-R57] [S1] [S10] [S11] [S12] [S17]. On the anchor cell's ₩180,960 of annual
  premium — which is 18% of the basket, so the whole of it attracts relief — that is
  ₩21,715 a year, **12% of the gross premium**, and worth rather less than half the 28%
  spread between the cheapest and dearest carrier on the same risk [S4]. It is not a
  cash flow of the insurer and the model does not carry it; it is the reason a Korean buyer's
  effective price is not the price on the rate card.
- **On insurer failure**, 해약환급금 plus 기타지급금 are protected to **₩100,000,000 per
  person** and 사고보험금 to a **separate and additional ₩100,000,000** [REG-R52 제18조제7항](#krlib-reg-r52)
  [REG-R32] [S3] [S11] [S13]. On this product the first limb is worth nothing, the surrender
  value being nil, and the second is worth the whole benefit up to the cap. **Corporate
  policyholders are not protected at all** — which matters to the 경영인정기보험 form this
  composite excludes. Cited, never modelled.

---

## Key sensitivities and model risks

In rough order of leverage, with the K-ICS sub-risk each corresponds to named [REG-R13].

1. **The best-estimate mortality factor (사망위험액).** `mort_be_factor = 0.85` **[std]** is
   the largest single lever and the least evidenced number in the file, because the margin
   inside a Korean 예정 경험사망률 is inside a 기초서류 that is never published [REG-R2].
   Undiscounted `net_cf` on the anchor cell runs **+₩352,224.81 at 0.75, +₩108,809.94 at
   0.85 and −₩255,045.47 at 1.00** — a range that crosses zero inside a plausible band and
   is more than five times the whole answer. A user with own experience should replace this
   before anything else in this file.
2. **The renewal-decline rate (해지위험액), on a 갱신형 point.** `renewal_decline_base = 0.20`
   **[std]** is published nowhere in Korea for any product [S7] [S16]. Undiscounted `net_cf`
   on the 갱신형 anchor runs **+₩5,550,691.22 at d = 0%, +₩4,789,398.01 at 5%,
   +₩2,919,193.21 at 20% and +₩1,258,323.02 at 40%** — a factor of **4.4** across a range no
   document narrows, driven almost entirely by premium income, which runs ₩19.67m to ₩6.19m
   over the same range. It has no `uklib` and no `uslib` analogue.
3. **Contract boundary.** Whether the liability runs to the ceiling or to the end of the
   cycle in force changes the **sign** of the undiscounted answer on the same cell —
   +₩2,919,193.21 against −₩181,055.18 — and also changes the lapse curve through the 전기납
   resolution of `pay_term()`. The model does not rule; nothing retrieved settles it
   [REG-R60] [unverified].
4. **The renewal rate scale beyond the published ladder (a discretionary risk, not a
   modelling one).** The shipped ladder is the carrier's own projection with the **rate
   scale frozen at its issue level, reflecting 연령증가 alone**, and the carrier says so
   [S7]. The contract permits 위험률 and 적용이율 to move too [S9] [S15]. A projection that
   moved them would differ and nothing published bounds by how much. This is the assumption
   that most deserves a stress and is least amenable to one.
5. **Expense level and inflation (사업비위험액) on a small premium.** No Korean carrier
   publishes any expense rate at all [S1] [S6] [S8] [S10] [S11] [S12]. ₩2,000 a month of
   maintenance against ₩15,080 of premium is 13% of the anchor's premium and **25% of the
   female twin's** ₩8,010, which is why point 2 is negative and point 1 is not on identical
   contractual terms. The 2.0% **[std]** inflation rate steps at each 계약해당일 and compounds
   over twenty years to a 45.7% higher charge in the final policy year. The 보험가격지수 dispersion of 51.6% to 239.1%
   across the 45 disclosed products [S4] is the only public handle and it is a wide one.
6. **The best-estimate lapse level (해지위험액) on a 비갱신형 point — modest, and how
   modest was itself a grid artefact.** Moving `lapse_be_factor` over 0.5 / 1.0 / 2.0 moves
   the anchor's total over +₩110,995.14 / +₩108,809.94 / +₩99,649.28: a **fourfold** move in
   the assumption is worth 10% of the answer, against the 60% a hundred-basis-point move in
   `mort_be_factor` is worth. On a no-surrender-value protection form a lapse forfeits a
   paying policy and saves its claims in nearly equal measure, so the leverage that dominates
   a savings chassis is second-order here.

   The annual-grid version of this model reported a range of ₩3,000 on this test and called
   the sensitivity third-order. **That number was an artefact of the timing convention**: an
   annual step collected a whole year's premium in advance and applied the year's lapse only
   at the end of it, so a lapsing policy was credited with premium for the year it left in
   and the premium lost to lapse was understated by construction. Stepping monthly stops
   crediting premium to lives that have gone, and the real leverage shows. The corollary is
   unchanged and is still the real risk: **on a 무해지 form the lapse assumption is a CSM and
   해약환급금준비금 question rather than a cash-flow question** [REG-R11] [REG-R27], and this
   model does not compute either.
7. **Commission at a 갱신.** `comm_new_term_rate = 0` is a choice against a Korean fact that
   argues the other way — the renewal is issued on a **new product code** [S9] [S15]. Setting
   it to 0.60 turns `t = 120` of the 갱신형 anchor from +₩4,689.19 to **−₩83,085.07** and the
   forty-year total from +₩2,919,193.21 to **+₩2,238,679.76**.
8. **The shortened-pay equivalence.** `pay_factor` uses an annuity **certain** at the
   적용이율 because **no Korean document retrieved publishes a shortened-pay term premium at
   all**. It gives 1.781198 on model point 5 and 1.484695 on model point 9, and it overstates
   the uplift by the mortality that would have been shed between the two periods. Nothing
   published lets the size of the overstatement be measured.
9. **Selective lapsation across renewals.** Renewal takes **no 고지** [S6] [S9] [S15], so the
   anti-selection is structural and repeats three times on the 갱신형 anchor. The base run
   carries no term for it and therefore understates late-cycle claims by construction. This
   is also the mechanism that makes the *long* boundary reading arguable, so the two risks
   are not independent.

### Known modeling pitfalls

Each of these is a mistake a competent modeller would actually make on this product, and
each is checkable against the shipped model.

- **The renewal decline is not lapse, it is not converted to a monthly rate, and the order
  is not cosmetic.** `d(t)` is non-zero **only** in the last month of a cycle, it enters at
  its own 20% because it is a discrete election on a date rather than a force acting through
  a period, and the exits it produces are taken **after** mortality and **after** ordinary
  lapse. The policy roll-forward is order-invariant, so a model that applies the decline
  first still balances — and books **20% fewer death claims** in the boundary month: on
  model point 3 at `t = 119`, ₩5,255.97 instead of **₩6,569.96**, with
  `l(120) = 0.5805175782` either way. Folding the decline into `w(t)` instead is worse: it
  makes the boundary invisible, and on that row the decline is **0.1451293946 of
  0.1463568040 total exits, 99.2% of everyone who leaves in that month**.
- **Truncation at the ceiling shortens the cycle, not the horizon.** 「갱신일부터 최종
  갱신계약의 보험기간 종료일까지가 10년미만일 경우에는 갱신일부터 갱신계약의 보험기간
  종료일까지 이 계약의 보험기간으로 합니다」 [S6], so `term_len(k) = min(n, w_r − x_k)`. An
  issue age of 45 on a ten-year cycle has a final cycle of **five** years — 60 months, over
  all of which the premium is level — and the projection still ends exactly at 보험나이 80,
  at `t = 419`. Shortening the *horizon* instead invents or destroys cover.
- **비갱신형 never renews.** Such a point has one 보험기간, one premium and no repricing
  [S1] [S12]. `renewal_decline_rate(t)` must be **0 at every `t`** on it, and
  `check_decline_timing()` asserts exactly that in both directions — non-zero **iff** the
  point is 갱신형, `t + 1` is a multiple of `12n`, and `t < proj_len() - 1`. Applying the
  renewal
  machinery to a 비갱신형 point invents cover the contract does not have; failing to zero the
  final boundary invents a decline in the month cover ends.
- **The premium is a function of the renewal index, not of the policy year.** On model
  point 3, indexing the premium by `t` and freezing it at the issue value collects
  ₩2,195,589.29 of premium over forty years instead of **₩11,517,624.04** — it converts a
  갱신형 into a 비갱신형 at one-fifth of the right price. `check_prem_level()` asserts the
  complement: the premium is level **within** a cycle and must **change** across a boundary.
- **A premium waiver does not survive a 갱신, and this is sourced, not assumed.** 흥국생명,
  verbatim: 「다만, 새로이 갱신되는 계약에서는 갱신 전 보험료 납입면제 사유로 인한 보험료
  납입면제를 적용하지 않고, 보험료를 계속 납입하여야 합니다」 [S6]. `wop_waived_frac` is
  therefore **0.0 exactly** at `t = 0, 120, 240, 360` on model point 3, and rebuilds to
  0.0079050974 by the last month of each cycle. The incidence itself is stated **annually**,
  because that is the unit a 장해 incidence would be published in, and is converted to the
  monthly chain by `1 − (1 − wop_inc_rate)^(1/12)`: it is a probability over the year, so
  the monthly equivalent sits slightly **above** a twelfth of it and a model dividing by
  twelve would understate the waived population. `check_waiver_reset()` asserts it. A model that
  carries the waived fraction across the boundary loses premium income the contract entitles
  the insurer to collect.
- **The suicide and contestability clocks, by contrast, do *not* reset at a 갱신.** They run
  from the original 보장개시일 and restart only on **부활** [S2 제6조·제28조]. So the
  contract is fresh for pricing and for the waiver and continuous for the exclusions.
  Treating each renewed cycle as a fresh policy gets persistency, the strain pattern and
  both clocks wrong at once — and `pols_if` is continuous across every boundary, never reset
  to 1.
- **The waiver is cause-neutral, so its incidence must not be scaled off `mort_rate()`.**
  The trigger is a 장해지급률 of 50% or more from 「동일한 재해 또는 재해이외의 동일한
  원인」 — sickness qualifies equally with accident [S2 제5조제1항] — so `wop_inc_rate` is an
  **arbitrary placeholder** and deliberately not a function of `q`. A number derived from `q`
  would be a false derivation dressed as a real one, and it would also import the mortality
  best-estimate factor into a disability assumption.
- **재해사망 is a split of the death decrement, never a second decrement.** The uplift pays
  **2×** the sum assured on 재해사망 and 1× otherwise [S6] [S10], so
  `claims_acc_death(t) = SA × a_q(t) × (1 − a(t)) × D(t)` sits **beside**
  `claims_death(t)`, which carries the matching `(1 − a(t))`, and the total on an accidental
  death is exactly `2 × SA` when the acceleration module is off, as it is on every model
  point that switches the uplift on. Adding an
  accidental incidence as a decrement of its own double-counts the deaths and breaks the
  roll-forward. Guard: `acc_mort_share` is capped at 1.0.
- **Lapse pays nothing, and the zero must be published rather than inferred.**
  `claims_lapse` is identically 0.00 on every model point [S1] [S2 제33조제2항] [S12], but the
  **표준형 comparator does have a surrender value** [S2 제33조] [S12] and a shortened-pay
  무해지 contract acquires 50% of it after 납입완료 [S1] [S12]. A Korea term chassis therefore
  cannot assume the absence the way a UK one can; the zero is asserted from the composite's
  form, not from the product class. On model point 5 that omitted post-완납 value is a real
  quantity this model does **not** compute — the 순보험료식 계약자적립액 being
  `WholeLife_KR_S`'s.
- **The 전기납 resolution couples `pay_term()` to `proj_years()`, and therefore to the
  contract boundary.** `pay_term_y = 0` means 전기납 and resolves to `proj_years()` — the
  horizon in **years**, not the month count — so truncating a 갱신형 point at the current
  cycle also compresses the 적용해지율 curve from forty years to ten. Model point 3's first
  120 `net_cf` rows sum to −₩172,034.54 and model point 4's total is **−₩181,055.18**; the
  two are *not* the same projection truncated. A model that expects them to match has
  mis-specified one of them.
- **`qbar` in the premium extension is a mean of *table* rates, not of best-estimate
  rates.** `mort_table_mean` averages `mort_rate_at_age`, unadjusted by `mort_be_factor` and
  unadjusted by the rate class. Feeding `mort_rate(t)` in instead moves a premium **scale**
  by an assumption that has nothing to do with pricing, and — because the factor is
  constant — it would cancel in the ratio anyway on a single-class point while silently
  failing on a preferred-class one, which is the worst kind of error.
- **The premium rounds to 10 won *before* annualization.** `round_10(r × c_p × g × SA/1e8)`
  then `× 12`. Rounding after annualization, or not at all, breaks the reproduction of the
  published ₩15,080 / ₩180,960 at the anchor and of ₩9,000 / ₩108,000 on the 갱신형 point,
  and those are the figures three independent documents agree on [S12] [S4] [S6] [S7].
- **`P_a = 12 × P_m` is now a report, not a cash flow, and nothing is left to correct.**
  The month's premium income is `P_m` on the lives in force when the month opens, which is
  what the contract collects; `P_a` survives because the commission scale is written on an
  annualized premium and because a reader comparing this model with a disclosure needs the
  annual figure. The annual grid's pair of offsetting timing errors — a year's premium taken
  in advance from lives that then left, worth 1.136% of a year's premium at the 적용이율,
  against a death benefit paid a year late — is **removed rather than netted**, so do not
  apply a half-year premium adjustment on top of this grid: there is no longer an
  end-of-year claim timing for it to be the matched pair of. One visible consequence: a
  year's premium income now sits **below** one annualized premium on the opening exposure,
  by 2.2% in the first policy year of the anchor, and that difference is exactly the premium
  the annual grid collected from lives that had already gone.
- **The 선지급 cap is per insured, aggregated across the insurer's contracts, and it is
  reached exactly at the anchor.** `A = min(0.5 × SA, ₩50,000,000)` above the ₩10,000,000
  full-payment floor [S2 제4조]. At `SA = ₩100,000,000` that is `0.5 × SA = ₩50,000,000 =
  accel_cap`, so the cap is **exactly reached and reduces nothing**: `accel_cap_binds()`
  returns `False` on a strict inequality. A model reporting the cap as binding there has a
  strict-versus-weak inequality error. Model point 9 (`SA = ₩200,000,000`) is the point
  where it genuinely binds.
- **The accelerated amount comes out of the death benefit, not beside it.** The
  보험가입금액 is treated as reduced by the amount paid, from the payment date, and **no
  surrender value arises on the reduction** [S2 제4조]. So `claims_death` carries
  `(1 − a(t))` and `claims_accel` carries `a(t)`; adding the acceleration on top of a full
  death claim pays the benefit twice.
- **The 부활 window runs from each life's own 실효, so the pool is carried by vintage.**
  `reinstate_window = 36` is the **sourced** three years [S2 제28조] carried in the
  projection's own months, so the window closes on the month it actually closes on rather
  than at the next anniversary: a life that lapsed in month 5 leaves the pool in month 41.
  The clause expressly covers a policy with no surrender value — 「해약환급금이 없는 경우를
  포함합니다」 — so a 무해지 policy is **always** eligible. A single indicator on one balance
  drops a whole cohort early or late; `check_lapse_pool()` closes in both positions of the switch because the pool is
  tracked either way. **Renewal declines never enter the pool**: a declined renewal is an
  expiry, not a 실효, and there is nothing to reinstate.
- **Read the tables at 보험나이 and at nothing else.** 보험나이 is 만나이 with fractions of
  six months or more rounded up, incrementing on the **policy anniversary** [S2 제22조]
  [REG-R25 제21조](#krlib-reg-r25), and the premium grid, the mortality table and the model point ages are
  all on that basis, and on a monthly grid the age steps at the 계약해당일 and holds for
  the twelve months between — interpolating it within the policy year would be modelling an
  age the contract has no concept of. Reading the anchor cell at 만나이 — one year of ageing
  early on every row, decrements and survivorship together — cuts total death claims from
  ₩2,063,167.17 to **₩1,897,843.01**, an **8.0% understatement**, and flatters `net_cf` by
  more than the entire answer. Unlike `jplib`, **no shift is
  correct here**; the temptation to import one is the error.
- **The disability state is not a benefit.** Korea has no 高度障害保険金 analogue [S2 제5조].
  Adding a disability claim on top of the death decrement invents a benefit the contract
  does not carry — the 장해 state waives premiums and nothing more [S2 제5조제1항] — and
  doing it on the Japanese pattern also double-counts, because there the table already
  includes the second event.
- **Do not publish a `claims` aggregate column beside the split columns.** `claims(t, kind)`
  is a cells and stays one; `result_cf()` publishes the five `claims_*` split columns so
  that they sum with the expense and commission columns to `net_cf`, and `check_net_cf()`
  re-derives that identity **from the published frame**. An aggregate column beside the
  splits double-counts the whole benefit outgo.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R18]: #krlib-term_life-r18
[R19]: #krlib-term_life-r19
[R20]: #krlib-term_life-r20
[R4]: #krlib-term_life-r4
[R9]: #krlib-term_life-r9
[REG-R10]: #krlib-reg-r10
[REG-R11]: #krlib-reg-r11
[REG-R13]: #krlib-reg-r13
[REG-R14]: #krlib-reg-r14
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R23]: #krlib-reg-r23
[REG-R25]: #krlib-reg-r25
[REG-R26]: #krlib-reg-r26
[REG-R27]: #krlib-reg-r27
[REG-R28]: #krlib-reg-r28
[REG-R29]: #krlib-reg-r29
[REG-R3]: #krlib-reg-r3
[REG-R32]: #krlib-reg-r32
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R36]: #krlib-reg-r36
[REG-R38]: #krlib-reg-r38
[REG-R4]: #krlib-reg-r4
[REG-R48]: #krlib-reg-r48
[REG-R5]: #krlib-reg-r5
[REG-R50]: #krlib-reg-r50
[REG-R51]: #krlib-reg-r51
[REG-R57]: #krlib-reg-r57
[REG-R60]: #krlib-reg-r60
[REG-R61]: #krlib-reg-r61
[REG-R8]: #krlib-reg-r8
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
