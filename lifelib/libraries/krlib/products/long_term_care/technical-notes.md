# Technical Notes

**Status:** Draft, 2026-09-03 (all cited sources accessed 2026-09-03).

**Scope note.** These notes turn the standardized composite long-term-care insurance
(*ganbyeong boheom*, 간병보험) of `product-spec.md` (same directory) into a reference
liability cash-flow projection on paper, and then into `LTC_KR_S` beside it. **They
describe no single insurer's contract.** [S#] and [R#] tags resolve against `sources.md`,
whose numbering is carried verbatim from `_research/long-term-care.md` and is frozen;
[REG-R#] tags resolve against the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is separate and
also frozen. **[std]** marks a standardization introduced for the reference
implementation, always with a rationale and, where one exists, the observed range;
[unverified] marks a claim that could not be confirmed against a retrieved document.
**Every contractual parameter value here is identical to `product-spec.md`'s**, and
**every number in the worked example is read off the shipped model** rather than
recomputed by hand.

Seven **assumption inputs** appear here that `product-spec.md` does not carry, because
they are modelling constructs rather than contractual terms, and each is introduced below
as such: the **certification-prevalence curve** by sex and 만나이; the
**prevalence-to-incidence conversion** and its closing assumption `direct_entry_share`;
the **care-state and light-grade mortality multiples**; the **sub-65 gradient** carried
off the one disclosed 예정위험률; the **grade-share vector by age band**; the **lapse**
level; and the **expense and commission** scales together with the **계약자적립액**
reconstruction that drives the surrender-value cliff.

---

## This document's deltas against the cancer chassis

**This document states its deltas against
[the cancer technical notes (암보험)](../cancer/technical-notes.md), the `krlib`
fixed-benefit (정액) 제3보험 chassis, whose model is
[`Cancer_KR_S`](../cancer/model.md).** That document specifies five mechanics once and in
full — the diagnosis-triggered lump sum on a tier ladder, the 90일 면책기간, the 감액기간,
the 유사암 reduced tier, and a post-diagnosis survival model — and this one does not
restate them. It also settles, for the whole library, the 만나이 projection basis, the
표준약관 furniture (보험나이, 청약철회, 품질보증해지, 계약 전 알릴 의무, 납입최고, 실효,
부활), the statutory **계약자적립액** payable on a death the contract does not cover, the
absence of a policy loan on a 미지급형 form, and the surrender-value regime of 감독규정
제7-65조 through 제7-68조 as extended to 제3보험 by 제7-69조 and 제7-70조 [REG-R19].

Six things change, and five of them change the shape of the model rather than a parameter
in it.

1. **The trigger is a statute's, not a classification's — and it is a *state*, not an
   event.** The chassis reads a KCD code that a pathologist assigns and an insurer
   applies. Here a 등급판정위원회 sitting inside 국민건강보험공단 scores an applicant on a
   52-item instrument and **awards a 장기요양등급**, and the 지급사유 is written by
   reference to that award and to nothing else [S1] [S2] [S3] [S4]. The statutory
   definition carries its own six-month duration test — 「6개월 이상 동안 혼자서 일상생활을
   수행하기 어렵다고 인정되는 자」 [REG-R54 제2조제2호](#krlib-reg-r54) — so the contract needs no
   persistence clause of its own, and the point thresholds live in a 대통령령 that can be
   moved without reference to any insurer [REG-R55 제7조제1항](#krlib-reg-r55).
2. **Four compartments, not three, and the middle one is where the claims come from.**
   The chassis carries a never-diagnosed state, a 특정소액암 state that still pays premium
   and a waived state that does not. This model carries a **never-certified** state, a
   **light-grade** state (3~5등급 and 인지지원등급, below the contractual threshold) that
   still pays premium and still lapses, and an absorbing **care** state that pays neither.
   The parallel is exact and it is not a coincidence: in both products the waiver fires at
   a threshold *above* the first insured event, so there is a diagnosed population the
   contract has not yet started paying for. What is new here is that the middle
   compartment is the **dominant route into the benefit**: only 13.3% of current 1등급
   certifications arose from a first application, against 69.5% from a renewal, whereas at
   인지지원등급 — a grade nobody progresses *down* into — the first-application share is
   69.8% [R4 표2-5](#krlib-long_term_care-r4). Severe-grade lives are, in the main, people who entered the scheme
   years earlier at a light grade and deteriorated.
3. **The chassis's incidence basis is sourced; this one's is a prevalence and has to be
   converted.** 보험개발원 publishes a dated 「기타피부암 및 갑상선암 이외의 암 발생률」
   grid by age and sex on its 장기손해보험 참조순보험요율 display [REG-R61], so
   `Cancer_KR_S` reads an incidence directly and spends its judgement on the **tier
   decomposition** of it. **No Korean body publishes a long-term-care incidence table at
   all.** What is published is the 국민건강보험공단 노인장기요양보험 통계연보's 연령별
   인정률 [R4], and an 인정률 is a **prevalence** — a point-in-time count of people
   *holding* a certification. The conversion is the modelling work of this product, it
   needs the mortality of the care state inside it, and it is done in the open in section
   (c) below rather than replaced by an assumed incidence rate.
4. **The post-onset survival model is the product, not a correction to it.** On the
   chassis, survival after diagnosis decides how long the waiver, the inpatient limb and
   the treatment limb run — real, but second-order against a lump sum paid on day one.
   Here the **간병연금** is metered month by month on survival in the care state for up to
   ten years, the waiver stops the premium for as long as that state lasts, and — this is
   the part with no chassis counterpart — **the same care-state mortality multiple is also
   a term of the incidence identity**, so it moves entry and run-off in opposite directions
   at once. There is no number in this model that does not depend on it.
5. **No reduced tier; a threshold ladder instead.** The chassis's 유사암 tier covers a
   high-frequency, high-survival decrement at a fraction of the general amount without
   repricing. There is no analogue here. The light grades are reached by **moving the
   threshold** — 1등급 / 1~2 / 1~3 / 1~4 / 1~5 / 1~인지지원등급, always cumulative from the
   top — which is a different product at a different price, about **4.5 : 1** between
   1~5등급 and 1~2등급 at the same 가입금액 [S2, derived], not a fraction of this one. The
   threshold is a model point field, and widening it changes the frequency **and the
   timing** together.
6. **Two parameter-level deltas.** The 예정이율 is **sourced** here at 연단위 복리 2.0%
   [S1] against the chassis's [std] 2.50%, because one carrier states it in terms in a
   기초서류 extract; it is a 2023-vintage 우정사업본부 rate and the three cautions travel
   with it (see (b) below). And the **표준해약공제액** is taken from the supervisor's
   13-months-of-premium rule of thumb [REG-R29] rather than from the chassis's
   `notional_sa_ratio` route through [별표 15] 제9호, because 제9호's own third bullet
   **excludes** 「치매 또는 일상생활장해 등 타인의 간병을 필요로 하는 상태」 risk premium
   from the ratio that gives a contract with no death benefit its notional 보험가입금액
   [REG-R21]. Read literally, the formula the chassis inherits excludes long-term-care
   risk premium from the very quantity a long-term-care contract needs.

Everything else is the chassis's and is not restated: 무배당 with no policyholder dividend
[REG-R12]; a fixed sum (정액) paid on an event rather than an indemnity against a cost; a
benefit payable **최초 1회한** that extinguishes the benefit line paying it without
terminating the contract; the 해약환급금 미지급형 form with its cliff at 납입완료; the
계약자적립액 on non-covered death [REG-R17] [REG-R25 제22조](#krlib-reg-r25) [REG-R50 제736조](#krlib-reg-r50); and the
absence of a 보험계약대출 and therefore of any automatic premium loan [REG-R28].

**One product this document is not about.** Korean commentary in 2024–2025 uses 간병
overwhelmingly to mean **간병인사용일당**, a hospital-days indemnity whose loss ratios
reached about 100% in the life sector at August 2024 against 18.7% two years earlier
[R15, news](#krlib-long_term_care-r15). It sits inside the same 약관 [S1] [S2] [S4] and shares nothing else;
`LTC_KR_S` does not model it.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows** for a single-policy
  model point of 간병보험: office premiums; the **장기요양진단급여금** on first award of a
  grade at or above the contractual threshold; the **간병연금** metered by an annual
  survival test; the optional **치매진단급여금**; the **계약자적립액** paid on a death from
  a cause the contract does not cover; the **해약환급금** paid on surrender; the premiums
  returned where a certification inside the 보장개시일 window makes the cover **무효**;
  maintenance and claim-handling expense; and commission. Undiscounted and gross of
  reinsurance. Korea runs **three** measurement bases over one such stream and all three
  are live: K-IFRS 제1117호, mandatory since 2023-01-01 [REG-R60]; K-ICS from the same
  quarter [REG-R13]; and the **해약환급금준비금**, which has no counterpart anywhere else
  in this repository [REG-R11]. **Discounting, the risk adjustment, the CSM, 요구자본 and
  every reserve are out of scope** and are cited, not reproduced — see *Valuation and
  reserve pointers*.
- **Projection frequency.** **Monthly grid**, and monthly by construction rather than by
  approximation. 월납 is the dominant retail mode and the mode of every published rate
  card in the file [S1] [S2]; the 90-day 보장개시일 lands on the grid boundary `t = 3`;
  the one-year 감액기간 lands on `t = 12`; and — the mechanic that forces the grid — the
  **간병연금 instalment is monthly** while its survival test is annual, so a model on an
  annual grid cannot represent the twelve-month guarantee at all. **`t` is the policy
  month and it is 0-based**: `t = 0` is the first projected month, `t = 0, 1, …, n − 1`
  with `n = proj_len()`; month `t` is the interval from `t` to `t + 1` months after the
  보험계약일; and the contractual policy year is the derived 1-based label
  `y(t) = floor(t / 12) + 1`.
- **`proj_len()` is the number of projected months, the frame's exclusive end — not the
  last index.** `proj_len = 12 × (term_age − issue_age) + 1`, so **601** on the anchor cell
  and **601 rows** in `result_cf()`, indexed `t = 0 … 600`; the frame is
  `range(proj_len())` and the last index is `proj_len − 1`. The `+ 1` is the terminal row:
  the 600 months of cover are `t = 0 … proj_len − 2`, and month `t = proj_len − 1` is the
  90세 계약해당일 itself, which carries the surviving in-force count, `pols_maturity`
  records the cover ending, and **every cash flow on that row is zero** — 「이 상품은
  순수보장성보험으로 보험계약 만기시 지급받는 금액(만기환급금)이 없습니다」 [S3].
- **The waiting period lands on a grid boundary.** The 장기요양상태 보장개시일 is
  「계약일(부활(효력회복)계약의 경우 부활(효력회복)일)부터 그 날을 포함하여 90일이 지난날의
  다음 날」 [S2]. On a monthly grid that is three whole months, `t = 3` **[std]**, and the
  model claims no finer precision. A certification **inside** the window does not defer the
  claim: the benefit is **무효** and the premiums paid for it come back [S1] [S2]. This is
  the chassis's mechanism with the chassis's consequence, but **without the chassis's
  option** — `Cancer_KR_S` lets the policyholder cancel the rest of the contract within 90
  days of the 진단확정일 [S1 of that product], and no retrieved long-term-care contract has
  any equivalent, nor any revival clause.
- **Timing conventions [std].** Office premium received at the **start** of month `t`, and
  only by lives not on 납입면제; maintenance expense at the start of month `t`; the lump
  sum, the annuity instalment, the dementia benefit, the 계약자적립액 on death, the
  해약환급금 on lapse, the refund on a voided cover and the claim-handling expense at the
  **end** of month `t`; decrements at the end of month `t`, in the order **certification,
  then mortality, then lapse**. Acquisition expense and initial commission at `t = 0`.
- **Claim-date convention [std].** Every claim is dated at the month the **판정일** falls
  in. The determination is due within 30 days of the application, extendable by a further 30
  [R3, citing 법 제16조제1항](#krlib-long_term_care-r3). The 보장개시일 test is measured to the 판정일, so a model
  dating the claim at the application would let a certification through the window the
  contract voids.
- **The annuity's first instalment falls in the month of certification** — 「진단 확정된
  날을 최초로 하여 10년 동안 매년 진단 확정일에 살아있을 때」, 「최초 1년(12개월)
  보증지급」, 「10년(120개월)을 최고한도로 지급」 [S1]. The `u = 0` term of the ledger is the
  entrant cohort itself; there is no deferral.
- **Age basis.** **만나이** (*man nai*, age last birthday), incremented on the policy month
  grid: `age(t) = x + floor(t / 12)`. The contract ages on **보험나이** (*boheom nai*):
  「계약일 현재 피보험자의 실제 만 나이를 기준으로 6개월 미만의 끝수는 버리고 6개월 이상의
  끝수는 1년으로 하여 계산」 [REG-R25 제21조](#krlib-reg-r25), and the two differ for roughly half of all
  issue dates. **The 만나이 basis is not a concession here, as it is on the chassis; it is
  the right basis twice over.** Every public series this model's decrements are built from
  is published on 만나이 — the 통계연보 연령별 인정률 [R4], the 치매역학조사 prevalence
  [R7], and the 생명표 behind the mortality [REG-R38] [REG-R39] — and the benefit
  definition itself **contains a 만나이 test**: 「만 65세 이상 노인」 또는 「노인성 질병을
  가진 만 65세 미만의 자」 [S2] [REG-R54 제2조제1호](#krlib-reg-r54). The 보험나이 offset therefore
  survives only in the premium, which enters this model as an input, so no conversion is
  applied anywhere. The direction is nonetheless stated: the disclosed 예정위험률 the
  conversion is calibrated against is quoted on 보험나이, about half a year older than this
  model's 만나이, which is one of the four reasons the calibration ratio in (c) sits below
  one.
- **Currency.** KRW throughout. There is no minor unit in the contract, but expected values
  are fractional; displayed to the precision each table states.
- **Model points.** One policy at a time, projected on an expected (probability-weighted)
  basis. `Projection` is parameterized by `point_id`; no aggregation logic is specified
  here. **Nine** points are shipped and every one satisfies every `check_*()` cells.
- **Termination.** Cover to the **90세 계약해당일**, `t = proj_len − 1`. The decrements are
  death, lapse, the voided cover of the waiting-period window, and maturity — and **nothing
  else**. There is no benefit-driven termination: payment of the 진단급여금 extinguishes
  that benefit line and leaves the contract, the annuity and the dementia rider running
  [S1] [S2] [S3] [S4].
- **Contract boundary.** The long-term-care benefit is written **비갱신형** on every
  document retrieved [S1] [S2], with a level premium, 무배당, and no insurer repricing
  right on the benefit, so every future premium and benefit is inside the boundary and the
  horizon is the whole term. That is the opposite of the Korean *medical* market, where
  annual renewal is the defining feature, and it is the right answer for a benefit whose
  claim arrives thirty years after issue: a renewable long-term-care rider re-rated at
  attained age would price itself out of existence exactly when it was needed. **The
  renewable form is not modelled.**
- **Rounding.** Intermediates at full double precision. The worked example displays policy
  counts to ten decimals, first-year cash flows to six, milestone rows to four and
  aggregates to four. **Monthly rows rounded for display do not re-add to the displayed
  totals**; the totals are sums of unrounded values.
- **What this model is not.** It is a **mechanics demonstration**. The premium is a model
  point input, the whole morbidity basis is a construction from public administrative
  statistics, the post-onset mortality basis is [std] with no published table behind it
  anywhere, and the expense scales are [std]. Replace the assumption tables with company
  data before drawing any conclusion from the output.

---

## Model point attributes

| Attribute | Type | Anchor cell (`point_id = 1`) |
|---|---|---|
| `policy_id` | str | LTC-000001 |
| `issue_age` (`x`) | int, **만나이**, 30–70 | 40 |
| `sex` | enum {M, F} | M |
| `term_age` | int, 만기나이 | 90 |
| `prem_period_years` (`n_Y`) | int years, 납입기간 | 20 |
| `prem_mode` | enum {monthly} | monthly (월납) |
| `benefit_grade` (`G_B`) | enum {g1, g2, g3, g4, g5, g6} | g2 — 장기요양 1~2등급 |
| `lump_amount` (`A_B`) | 보험가입금액, KRW | 10,000,000 (1,000만원) |
| `annuity_on` | bool — the 간병연금 rider | True |
| `annuity_high` (`A_1`) | KRW per month at an entry grade of 1등급 | 500,000 |
| `annuity_low` (`A_2`) | KRW per month at any other grade in the gate | 300,000 |
| `annuity_max_mths` (`n_A`) | int months, the 최고한도 | 120 |
| `annuity_guar_mths` | int months guaranteed against death | 12 |
| `dementia_rider` | bool — the 치매진단급여금 rider | False |
| `dementia_amount` | KRW (rider off on the anchor) | 10,000,000 |
| `wait_mths` (`W`) | int months, 장기요양상태 보장개시일 on the grid | 3 |
| `red_mths` (`G`) | int months, 감액기간 ∈ {0, 12, 24} | 12 |
| `cv_form` | enum {mijigeup, half_during, pyojun} | mijigeup (해약환급금 미지급형) |
| `lapse_form` | enum {mujihae, pyojun} | mujihae |
| `uw_loading` | float — the 간편심사 premium multiplier | 1.0 (일반심사) |
| `premium` (`P`) | KRW per month, office premium, **model-point input** | 5,600 **[std]** |

Derived scalars on the anchor cell, all read off the model: `proj_len() = 601`,
`prem_period_mths() = 240`, `premium_mth_pp() = 5,600.0`, `pols_if_init() = 1.0`,
`net_prem_ratio() = 0.7931662309087683`, `comm_init_pp() = 43,680.0` and
`sub65_gradient() = 0.12221178050285361`.

**`premium` is an input, not a computed quantity**, and the reason is the same as on the
chassis with one aggravation. No Korean carrier publishes a long-term-care rate card at the
composite's specification: the 산출방법서 and the 사업방법서 are 기초서류 filed with the FSC
and are not public [REG-R2], and the one published card [S2] quotes covers that do not
match the composite one for one. The anchor is therefore **constructed from two rows of
that card**, both at 90세만기, 20년납, 월납, 일반심사형, 보험가입금액 1,000만원:
**₩3,300** for the 주계약 장기요양(1~2등급)급여금 at male 40, plus **₩580** for the
장기요양(1-2등급)재가급여종신지원특약 which pays ₩100,000 a month on the same trigger,
scaled to the composite's grade-weighted ₩400,000 a month — ₩2,320 — giving ₩5,620,
rounded to **₩5,600** **[std]**. The female cell is ₩5,000 + 4 × ₩850 = **₩8,400**
[S2, derived]. Two offsetting differences are recorded rather than adjusted for: the [S2] rider
runs **최대 종신** where the composite caps at 120 months (dearer), and it requires the
insured to be *using* 재가급여 in the month where the composite tests only survival
(cheaper).

**On this model's own basis the anchor premium is not far wrong.** The present value at
the 예정이율 of 2.0% of the anchor cell's long-term-care benefit outgo is **46.03%** of the
present value of premium income, and the present value of expenses, claim expenses and
commission is **20.26%**, against the **20.68%** loading that `net_prem_ratio()` implies
from the published 환급률 progression. Read that pair carefully. The 20.26% is
**calibrated** to the 20.68% — `expense_maint` is set to land near it (see (c) below) — so
their agreement is a construction and the 0.42-point gap is the rounding of `expense_maint` to
a whole ₩200. **What is not calibrated is the 46.03%.** Nothing ties the incidence basis,
built from the 통계연보 [R4], to the premium, built from a rate card [S2]; that a benefit
ratio of 46% and a loading of 21% together leave the contract close to self-supporting at the
disclosed 예정이율 is the finding here, and it is the one figure two unrelated documents had
to agree on without being made to.

The eight other model points exercise both sexes, issue ages 30 to 70, all six thresholds
from 1등급 to 1~인지지원등급, 90 / 95 / 100세만기, 10 / 20 / 30년납, the three
surrender-value forms, the 간병연금 on and off, the 치매 rider on and off, the 간편심사
loading, the 우체국 180-day waiting period with its two-year 감액, and the 표준형 lapse
comparison vector. **Model point 8's positive `net_cf` is an artefact and is described as
one** in *Key sensitivities* below.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `pols_healthy(t)` (`h`) | In force at the start of month `t` and **never certified**; `pols_healthy(0) = pols_if_init()` | monthly recursion |
| `pols_light(t)` (`l_L`) | In force and certified at a grade **below** `benefit_grade()`; `pols_light(0) = 0` | monthly recursion |
| `pols_care(t)` (`l_C`) | In force and certified **at or above** `benefit_grade()`; absorbing; `pols_care(0) = 0` | monthly recursion |
| `pols_act(t)` | `pols_healthy + pols_light` — the **premium-paying, lapse-exposed** population | derived |
| `pols_if(t)` (`l`) | `pols_act + pols_care` — total in force at the start of `t` | derived |
| `pols_healthy_mid(t)`, `pols_light_mid(t)`, `pols_care_mid(t)` | The three counts after the month's certifications, before mortality | derived |
| `pols_dem(t)` | In force and already paid the 치매진단급여금; a **first-event counter**, not a compartment | monthly recursion |
| `av_pp(t)` (`AV`) | **계약자적립액** per policy at the **start** of month `t` | two-branch recursion |
| `cv_pp(t)` (`CV`) | **해약환급금** per policy paid on a lapse in month `t` | derived |
| `age(t)` | Attained **만나이** = `x + floor(t / 12)` | annually |
| `mort_rate(t)`, `mort_rate_light(t)`, `mort_rate_care(t)` | Annual mortality of the three compartments at `age(t)` | lookup / derived |
| `prev_rate_at(x)` (`P`) | All-grade certification prevalence at 만나이 `x` | fitted logistic |
| `prev_care_at(x)` (`P_C`), `prev_light_at(x)` (`P_L`) | Prevalence at or above, and below, `benefit_grade()` | derived |
| `inc_rate_direct_at(x)` (`i_D`) | Annual **direct** entry rate, healthy → care | derived |
| `inc_rate_light_at(x)` (`i_L`) | Annual entry rate, healthy → light grade | derived |
| `prog_rate_at(x)` (`rho`) | Annual **progression** rate, light grade → care | derived |
| `lapse_rate_mth(t)` (`w`) | Monthly lapse, applied to `pols_healthy` and `pols_light` only | derived |
| `red_factor(t)` (`r`) | The 감액 factor applying to a certification **dated** in month `t` | derived |
| `ann_amount_at(s)` (`A(s)`) | The monthly 간병연금 of the cohort certified in month `s`, **frozen at entry** | derived |
| `net_cf(t)` (`CF`) | Net cash flow of month `t`, insurer perspective, **income-positive** | monthly |

**Why four compartments and not three.** The chassis's three states are forced by its
waiver clause; ours are forced by the certification statistics. A light-grade life is
certified — the state is real, and it carries impaired mortality — but **the contract does
nothing for it**: no benefit, no waiver, no annuity, and no retrieved Korean contract pays
anything at a grade below the stated threshold. So a light-grade life **keeps paying
premium and stays exposed to lapse**, exactly like the chassis's 특정소액암 life, and it is
the pool progression draws from. On the composite's 1~2등급 gate the light compartment is
about **six sevenths of all certified lives**: 1·2등급 are 13.28% of the 1,165,030 certified
at end-2024 [R4 표2-5, derived](#krlib-long_term_care-r4). Collapsing the two either stops a premium the contract
goes on charging or invents a benefit at a grade the contract does not cover, and — the
larger error — it makes the severe-grade entry rate a **healthy-life incidence**, which
puts the cash flow years too early.

**The care compartment is absorbing, and the contract is drafted so that it is.** The
진단급여금 cannot be re-triggered [S1] [S2] [S3] [S4]; the 간병연금's amount is fixed by
the grade at **first** certification and 「그 이후에 장기요양등급이 변경되더라도 지급액은
변경되지 않습니다」 [S1]; the instalments are metered on **survival**, not on continued
certification [S1]; the premium is waived [S3]; and surrender is barred — 「최초 지급사유가
발생한 후에는 이 특약을 해지할 수 없습니다」 [S1]. So **no recovery, no downgrade and no
lapse in the care state are a property of the contract before they are an assumption of the
model.** That is worth saying plainly, because grades genuinely move both ways — 107,365 of
the 1,165,030 current certifications arose from a 등급변경신청 [R4 표2-5](#krlib-long_term_care-r4) and one carrier
drafts a rider around exactly that [S3] — and a model of a *utilisation-conditioned* benefit
could not make this simplification at all. See *Key sensitivities*.

**The dementia counter is nested, never added.** `pols_dem(t)` rides on the in-force block
and is held at or below `pols_if(t)` so that `pols_entry_dem` always draws from a
non-negative pool. It is a first-event ledger on the same lives, not a fifth compartment.
Driving it off a *sourced* dementia prevalence [R7] rather than off a share of the
certification rate is deliberate: the two triggers are **correlated but not proportional**
— dementia is the sole qualifying condition for 5등급 and 인지지원등급 [REG-R55 제7조제1항](#krlib-reg-r55)
and is present in 42.3% of certified decedents [R11], yet most CDR 1 lives are nowhere near
a 1·2등급 certification.

**Three absences are product facts, not gaps.** There is **no death benefit** [S1] [S3], so
`claims_death` is a return of the 계약자적립액 and not a sum assured. There is **no
보험계약대출 and no automatic premium loan** during the 납입기간 on the 미지급형 form,
because there is no surrender value to lend against [REG-R25 제33조](#krlib-reg-r25) [REG-R28] — a missed
premium really does lapse the contract at the end of the 14-day 납입최고. And there is **no
만기환급금**: `claims(proj_len − 1, "MATURITY")` is zero and the column exists only so that the
statement's shape matches the rest of the library.

---

## Assumption inputs

### (a) Contractual / guaranteed elements (cited; the insurer cannot change them)

| Input | Value | Basis |
|---|---|---|
| Trigger | Award of a **장기요양등급** at or above `benefit_grade()` by the 등급판정위원회 under 노인장기요양보험법; no company-basis limb, no ADL schedule, no persistence clause | [S1] [S2] [S3] [S4]; [REG-R54 제15조](#krlib-reg-r54) |
| Eligibility gate | 「만 65세 이상 노인」 or a person under 65 with one of the **25 노인성 질병** the 시행령 [별표 1] lists | [S2]; [REG-R54 제2조제1호](#krlib-reg-r54) [REG-R55] |
| Grade point bands | 1등급 95점 이상 · 2등급 75~95 · 3등급 60~75 · 4등급 51~60 · 5등급 45~51 (치매 한정) · 인지지원등급 45점 미만 (치매 한정) | [REG-R55 제7조제1항](#krlib-reg-r55); [R3]; reproduced in a carrier's own document [S2] |
| 장기요양진단급여금 | **`A_B` = ₩10,000,000**, **최초 1회한** on the first award at or above the threshold on or after the 보장개시일; extinguishes that benefit line, **not** the contract | [S1] [S2] [S3] [S4]; threshold **[std]** |
| 장기요양상태 보장개시일 | 「계약일…부터 그 날을 포함하여 **90일**이 지난날의 다음 날」, `t = 3` on the grid, with a carve-back to the 계약일 where the cause is **재해** | [S2]; **[std]**, observed range none / 90 / 180 days |
| Pre-inception certification | The affected cover is **무효** and the premiums paid for it are **returned**; no cancellation option and no revival | [S1] [S2] |
| 감액기간 | **1 year at 50%** where the cause is **질병**; the full amount where the cause is **상해/재해** | [S4]; length **[std]**, observed none / 1yr / 2yr |
| The 감액 is frozen | The reduction decision is fixed at **first certification** and does not change as later instalments fall outside the window | [S1] |
| 간병연금 | Monthly from the 진단확정일: **₩500,000** where the entry grade is 1등급, **₩300,000** otherwise; **annual survival test** on each anniversary of the 진단확정일; **first 12 months guaranteed**; **120 months maximum** | [S1]; shape **[std]** |
| Annuity amount frozen | Set by the grade at first certification and never re-rated — 「그 이후에 장기요양등급이 변경되더라도 지급액은 변경되지 않습니다」 | [S1] |
| Annuity on death | The stream stops; where death follows a paid instalment **no 책임준비금 is returned** | [S1] |
| Surrender after the annuity starts | **Barred** — 「최초 지급사유가 발생한 후에는 이 특약을 해지할 수 없습니다」 | [S1] |
| Proof of life | 「매년 진단 확정일에 피보험자의 **주민등록등본**을 제출하여야 합니다」 — an **annual** administrative event | [S1] |
| 보험료 납입면제 | On the award of **1등급 or 2등급**, waiving the 기본계약 and every attached rider; waived premiums treated as paid | [S3]; threshold **[std]** |
| 치매진단급여금 | Optional: ₩10,000,000 on the first 최종진단확정 of **CDR 1 이상**, once only across the tier set, behind a **one-year 보장개시일** and the definition's own **90-day persistence** test | [S2] [S4]; tier **[std]** |
| Payment on non-covered death | The **계약자적립액** at the date of death plus unearned premium, whereupon the contract ends | [REG-R17] [REG-R25 제22조](#krlib-reg-r25); [REG-R50 제736조](#krlib-reg-r50) |
| General death benefit | **None** | [S1] [S3]; **[std]** |
| 만기환급금 | **None** — 「이 상품은 순수보장성보험으로 …」 | [S3] |
| Surrender value form | **미지급형**: **0%** during the 납입기간, **50% of the notional 기본형 value** afterwards | [S2]; [REG-R19 제7-66조제4항](#krlib-reg-r19) |
| 해약환급금 floor | `max(계약자적립액 − 해약공제액, 0)`; the 해약공제액 may not exceed the **표준해약공제액** of [별표 14]; 해약공제기간 = 납입기간 capped at **7 years** | [REG-R19 제7-66조제1항](#krlib-reg-r19); [REG-R20] |
| 계약자적립액 accrual | **Monthly** before 납입완료, daily afterwards; permitted to be computed on an annualised premium basis | [REG-R19 제7-66조제1항제4호](#krlib-reg-r19); [REG-R18 제7-65조제2항](#krlib-reg-r18) |
| Refusal on a defective certification | Where the grade was obtained by **허위 또는 부당 판정**, nothing is paid; and where the public benefit is restricted under 노인장기요양보험법 제29조 | [S1] [S2] [S4] |
| 납입최고 (grace) | **At least 14 days**; the contract terminates the day after the 납입유예기간 ends | [S1]; [REG-R25 제26조](#krlib-reg-r25) |
| 부활 | Within **three years**; **the 보장개시일 clock restarts from the 부활일** | [S1]; [REG-R25 제27조](#krlib-reg-r25) |
| Expiry | At the **90세 계약해당일**; **nothing is paid** | [S3] |

**The statutory-change clause, which has no chassis counterpart and is not modelled.** No
retrieved contract gives the insurer a 기초율변경권 on the long-term-care benefit. What it
gives instead is a **contract-continuity** provision: where the statute is amended so that
the grades cease to exist or cease to be determinable, the insurer 「객관적이고 합리적인
범위 내에서 기존 계약내용에 상응하는 "장기요양상태"와 관련된 새로운 보장내용으로 이 계약의
내용을 변경합니다」 [S3], and the definition itself names a successor body 「향후 제도변경시
에는 동 위원회와 동일한 기능을 수행하는 기관」 [S4]. **Neither is a repricing right.** The
asymmetry is the central risk of the Korean product and it is real: the 인지지원등급 was
created out of nothing on 2018-01-01 [R6] and enlarged the covered population of every
「1~인지지원등급」 rider overnight, at no additional premium. `LTC_KR_S` models the basis
that exists and carries the risk as a stated model risk, not as a parameter.

### (b) Insurer-discretionary current elements

This class is **nearly empty, and its emptiness is the product fact** — the same position
as the chassis, and for a stronger reason. The composite is **무배당** wherever the dividend
basis is stated [S1] [S2] [S3] [S4], so there is no 계약자배당 and the surplus-distribution
machinery of 감독규정 제6-11조의7 and 제6-13조 does not attach [REG-R12]. The design is
**금리확정형**, so there is no 공시이율 to reset and no 최저보증이율 to bind. There is no
premium review on the 비갱신형 chassis and no MVA. What remains:

| Input | Snapshot value | Basis |
|---|---|---|
| 예정이율 / 계약자적립액 적용이율 | **2.0% 연단위 복리**, 금리확정형 — 「무배당 우체국간병비보험 2309의 주계약 및 특약에 적용한 예정이율은 연단위 복리 2.0%입니다」 | **Sourced [S1]** — the only Korean long-term-care 예정이율 in any retrieved document |
| Incidence basis in the filed rate | The insurer's own, in the **산출방법서**, a 기초서류 filed with the FSC and not published | [REG-R2] |
| 간편심사 pool | A **premium** multiplier of 1.36–1.43× on the main contract [S2, derived]; the pool's own incidence is in no source | multiplier sourced; incidence **[std]** |
| 지정대리청구인 | Always designated; up to two, one as 대표대리인. **No cash-flow effect** and a mandatory operational feature of a product whose claimant usually cannot claim | [S1] [S3] |
| 장애인전용보험전환특약 | Raises the tax credit from 12% to 15% where the insured or beneficiary is a 소득세법 장애인; policyholder-side, not modelled | [S1] [S2]; [REG-R57] |

**Three cautions travel with the 2.0%, and they are why it is the one place in `krlib`
where a sourced number is arguably weaker than a [std] one would be.** It is a
**2023-vintage** rate on a 2309 product, and the 예정이율 moves with the market. It is a
**우정사업본부** rate, and 우체국 insurance is written outside 보험업법. And it prices a
different benefit mix: 우체국's 주계약 pays a **재해사망보험금** and the long-term-care
covers are riders on it. It is nonetheless preferred to an invented figure — and at 2.0%
against the chassis's [std] 2.50% the composite is the **more conservative** of the two on
a benefit payable forty years out. Note also that a full-text search of the 감독규정 returns
**zero occurrences of 예정이율** [REG-R9]: the regulation speaks only of the 계약자적립액
적용이율 and of the 금리확정형 / 금리연동형 distinction [REG-R48], so the 예정이율 of a
specific Korean product is not a published number for any *other* product in this library.

### (c) Behavioral / experience assumptions (modeler's view — all [std])

**Mortality of the never-certified.** `mort_table.csv` is a **construction, not a copy**.
경험생명표 (제10회, applied from 2024-04) is produced by 보험개발원 and is **not released in
full**: what is published is the 평균수명 and the 기대여명, not the rates [REG-R33]
[REG-R34]. What is shipped is a Makeham–Gompertz

    q(x) = 1 − exp( −( A + B c^x ) )                                            [std]

with `A = 0.0003` **[std]** and `c = 1.10` **[std]**, and `B` solved per sex so that the
complete expectation of life at 65 reproduces the published 제10회 경험생명표 65세
기대여명 — **23.7 years for men and 27.1 for women** [REG-R33]. That gives
`B = 1.494698342e-05` (M) and `1.018884285e-05` (F), with a terminal age of 120 where
`q = 1`. The construction is not fitted to anything else and it reproduces the second
published summary statistic without being asked to: the implied 평균수명 at issue age 40 is
**86.4** for men against the published 86.3, and **90.3** for women against 90.7. That is a
**cross-check on the shape, not evidence about any insurer's experience**, and no conclusion
about Korean insured mortality should be drawn from the file.

`mort_rate_mth(t) = 1 − (1 − q(age(t)))^(1/12)` **[std]**. There is **no best-estimate
adjustment factor**: the calibration anchor is an *experience* statistic, not a valuation
table with a prudential margin, so there is nothing to unwind.

**This is a delta against the chassis and it runs the right way.** `Cancer_KR_S` calibrates
its Makeham on the **population** 생명표's 기대여명 at 40 and 65 [REG-R38] — 19.5 years at
65 for a man. This model calibrates on the **insured** table's 23.7 at the same age, so its
healthy lives are materially lighter than the chassis's. On a product whose benefit is a
living one that is the conservative direction: longer survival means more entrants into the
care state and more annuity instalments once there. On a cancer contract the same choice
would be the other way round. Both are [std] and both say which table they used; a reader
comparing lifetime claim rates across the two products should not read the difference as
experience.

**Care-state and light-grade mortality — the multiples, and where they come from.** **No
retrieved source publishes a post-certification mortality table by grade**, and 보험개발원
publishes neither a 장기요양 incidence table nor a post-onset mortality table at all. The
model carries flat multiples:

    mort_rate_care(t)  = min(1, care_mort_mult  × q(age(t))),   care_mort_mult  = 3.0  [std]
    mort_rate_light(t) = min(1, light_mort_mult × q(age(t))),   light_mort_mult = 1.8  [std]

`care_mort_mult = 3.0` is **derived rather than assumed**, from two sourced quantities.
The yearbook roll-forward and the application-route estimator agree that the mean duration
of a certification is near **4 to 5.5 years** (see the conversion below), and the mean
만나이 of a certified decedent is over 75 [R11]. At 만나이 82 on the shipped table a mean
duration of 4.5 years implies a force of 0.222 against a healthy force of 0.075 — a multiple
of **2.96**. The one retrieved study measuring time from certification to death — **516.2
days**, 8.7% inside a month, 45.6% inside a year, on 271,474 people [R11] — is a
**right-censored decedent cohort**: only people who died inside a 4.5-year observation
window are in it, so everybody with a long duration is excluded by construction. It is a
**lower bound** on the mean duration and it fixes the early shape here, not the level.

`light_mort_mult = 1.8` has **no source and no observed range**. It is bounded above by the
care multiple and below by unity, and [R11]'s mean 인정점수 at death of **82.1** — squarely
inside 2등급 — says the deaths of that cohort are concentrated in the severe grades, so a
light-grade life is materially healthier than the cohort the study observed.

**`care_mort_mult` is not only a post-onset assumption.** It is also the excess-mortality
term of the incidence identity below, so it moves the entry rate and the annuity's run-off
**in opposite directions at once**. That coupling is the least obvious property of this
model and it is varied in a sensitivity rather than described.

#### Prevalence to incidence — the conversion, shown rather than assumed

**The published quantity is a prevalence.** The 2024 노인장기요양보험 통계연보's 연령별
인정률 counts people *holding* a valid certification at a point in time, not people
entering one [R4 표2-9, 표1-2, derived](#krlib-long_term_care-r4):

| 연령 | 인정자 | 인구 | **인정률 (T)** | 인정률 (남) | 인정률 (여) |
|---|---|---|---|---|---|
| 65–69 | 66,955 | 3,715,757 | **1.80%** | 1.98% | 1.63% |
| 70–74 | 102,751 | 2,437,413 | **4.22%** | 3.95% | 4.45% |
| 75–79 | 176,578 | 1,796,342 | **9.83%** | 7.45% | 11.76% |
| 80–84 | 320,148 | 1,344,376 | **23.81%** | 15.45% | 29.24% |
| 85+ | 461,622 | 1,105,925 | **41.74%** | 28.63% | 47.31% |
| **65+** | **1,128,054** | **10,399,813** | **10.85%** | **6.87%** | **14.02%** |

Two features of the sourced curve survive everything below and both matter. The gradient
is about **17.0% per year of age** — a factor of 23 over twenty years. And the **sex
crossover is at about 70**: male certification exceeds female below it and female exceeds
male above, which is the reverse of a death-benefit table and is independently confirmed by
the disclosed 예정위험률, whose female-over-male ratio runs 0.357 at 40, 0.575 at 50 and
0.882 at 60 and therefore crosses one in the late sixties [S1, derived]. **The disclosed
pricing basis and the national statistics agree on the sex crossover to within a few
years**, which is the strongest internal consistency check available.

**Step 1 — a prevalence curve by age and sex [std].** A three-parameter logistic

    P(x) = prev_ceil / ( 1 + exp( −prev_beta × (x − prev_x_mid) ) )             [std]

least-squares fitted in log space through the five sourced band rates at representative
ages 67 / 72 / 77 / 82 / **88.5**, the last being the population-weighted mean age of the
85+ band **[std]**. Male `(0.7480, 0.14692252, 91.61515338)`; female
`(0.6310, 0.22384681, 83.31342651)`. Fit residuals are within ±5.2% (M) and ±7.9% (F). The
derivative used below is the **analytic** one,

    P'(x) = prev_beta × P(x) × ( 1 − P(x)/prev_ceil )

and not a difference quotient: `P'` is the leading term of the incidence identity, and a
numerical derivative would put fitting noise straight into the claim rate.

**Nothing above 88.5 is sourced.** The logistic has three parameters and five anchors, so
the fit is over-determined and the ceiling *is* identified in a way the chassis's is not —
but it is identified by extrapolating five points that stop at 88.5, and on this composite
the projection stops at 90 anyway. The sensitivity in *Key sensitivities* shows the
consequence, and it is a smaller one than in the Japanese counterpart for exactly that
reason.

**Step 2 — the grade share, by age and not by all ages [std].** `share_ge_at(G, x)` is the
share of certified lives at grade `G` **or above**, linear in age between six sourced band
representative ages — 60 standing for the whole under-65 band **[std]**, then 67, 72, 77,
82 and 88.5 — and flat outside them [R4 표2-9, derived](#krlib-long_term_care-r4). It is a **proportion of a
population, never a rate**. Then `P_C(x) = share_ge_at(G_B, x) × P(x)` and
`P_L(x) = P(x) − P_C(x)`.

Carrying the share **by age** is load-bearing, because the severe share is **U-shaped**:

| 연령 | 1등급 | 2등급 | 3등급 | 4등급 | 5등급 | 인지지원 | **1·2등급 계** |
|---|---|---|---|---|---|---|---|
| <65 | 11.7% | 10.5% | 30.3% | 36.1% | 8.7% | 2.7% | **22.3%** |
| 65–69 | 6.5% | 8.1% | 26.8% | 45.5% | 10.0% | 3.0% | **14.6%** |
| 70–74 | 5.2% | 7.5% | 25.7% | 46.6% | 11.8% | 3.2% | **12.8%** |
| 75–79 | 4.3% | 7.1% | 24.4% | 47.1% | 13.6% | 3.4% | **11.4%** |
| 80–84 | 3.8% | 7.3% | 24.6% | 47.6% | 14.0% | 2.8% | **11.1%** |
| 85+ | 4.7% | 10.1% | 28.9% | 45.3% | 9.7% | 1.4% | **14.8%** |

The under-65 population is severe because only the 노인성 질병 list gets in at all
[REG-R55]; the 80–84 trough is where the scheme's marginal entrant is a lightly impaired
person newly crossing the 51-point line; the 85+ rise is genuine deterioration. **The shipped
`share_ge` for `g2` below 65 is 0.222**, the sum of the two rounded grade shares in that row;
[R4]'s own derived 1·2등급 계 is 22.3%, and the tenth of a point between them is rounding
inside the source table rather than a second basis. **A model
applying a single all-ages vector at every age is wrong by up to a factor of two** —
22.2% against 11.1% between the ends — and it is wrong at exactly the two ages that matter,
the issue age and the claim age.

The derivative of `P_C` is taken by the **full product rule**,

    P_C'(x) = s_G'(x) × P(x)  +  s_G(x) × P'(x)

with `s_G'` the exact constant slope of the bracketing linear segment. The first term is
**negative over most of the range** for a severe threshold, and dropping it overstates the
inflow badly: at 만나이 65 the second term alone is **1.82×** the correct `P_C'`, and at 75
it is 1.19×.

**Step 3 — the identity, which carries the care state's own mortality in it.** Write
`mu_H`, `mu_L`, `mu_C` for the three forces of mortality — `mu(x) = −ln(1 − q(x))`, in
forces and not in annual rates, because the excess-mortality term is a difference of
hazards and a rate difference is not one — and

    mu_bar(x)   = (1 − P) mu_H  +  P_L mu_L  +  P_C mu_C
    inflow_C(x) = max( 0,  P_C'(x)  +  P_C(x) × ( mu_C(x) − mu_bar(x) ) )
    inflow_L(x) = max( 0,  P_L'(x)  +  P_L(x) × ( rho(x) + mu_L(x) − mu_bar(x) ) )

**The second term is not a refinement.** A rising prevalence understates entry, because the
compartment it measures is simultaneously being drained by an excess mortality the
population around it does not carry. At 만나이 65 the slope term is **83.8%** of the
inflow and the mortality term the other **16.2%**; at the ages where the claims actually
arise the mortality term is a larger share still. And `mu_bar` rather than `mu_H` is what
turns a *count* identity into a *proportion* identity — prevalence is measured against a
living population, and a population that is itself dying faster raises every prevalence it
measures. Using `mu_C` alone in place of `mu_C − mu_bar` inflates the inflow at 65 by
**8.2%**, and by more at older ages.

**Step 4 — the closing assumption.** Two equations carry three unknowns: direct entry,
progression, and light-grade entry. The closing assumption is the one the sources leave
genuinely open, `direct_entry_share = 0.20` **[std]** — the share of gross inflow into the
care state arriving straight from health rather than by progression:

    i_D(x)  = direct_entry_share × inflow_C(x) / ( 1 − P(x) )
    rho(x)  = ( 1 − direct_entry_share ) × inflow_C(x) / P_L(x)     [0 where P_L = 0]
    i_L(x)  = inflow_L(x) / ( 1 − P(x) )

Its anchor is the yearbook's own application-route table [R4 표2-5](#krlib-long_term_care-r4): **13.3%** of current
1등급 certifications arose from a first application (7,371 of 55,340) against 69.5% from a
renewal, whereas at 인지지원등급 — a grade nobody progresses down into — the
first-application share is **69.8%** (19,436 of 27,835). The ratio of the two is where 0.20
comes from. **Getting it wrong does not change the lifetime claim count much; it changes
*when* the claim arrives**, which on a contract priced at 2.0% over fifty years is most of
the answer. Where the gate is `g6` — 1~인지지원등급 — there is no light state at all, so
`rho = 0` and the whole inflow is direct, by construction rather than by assumption.

`prog_rate_cap = 1.0` **[std]** is a guard rather than an assumption: it caps `rho` at a
certainty, no source bounds it because no source gives a progression rate at all, and it does
not bind on any shipped model point.

**Step 5 — below 65 there is no prevalence data at all.** The 인정률 series is published
for the 65-and-over population only, and the statute admits an under-65 applicant only
through the **closed list of 25 노인성 질병** — four dementia codes, one Alzheimer code,
fourteen cerebrovascular codes, four Parkinson-family codes and four others, with **no
cancer, no musculoskeletal condition and no frailty category** on the list [REG-R55 별표 1](#krlib-reg-r55)
[R2]. So the under-65 exposure is both small and violently concentrated: of the 58,271
applicants under 65 in 2024, 뇌혈관질환군 were 49.1% and 치매질환군 26.8%
[R4 표2-3, derived](#krlib-long_term_care-r4). The two entry rates are carried down from their age-65 values on the
log-gradient of the one disclosed Korean long-term-care incidence rate:

    sub65_factor_at(x) = exp( −sub65_gradient × (65 − x) )   for x < 65, else 1   [std]
    sub65_gradient     = ln( i(60) / i(40) ) / 20     on the combined 1·2등급 rate [S1]

which is **0.12221178 for men (13.00% a year)** and **0.16479184 for women (17.91%)**. It
carries the sex ratio with it, so a curve built on it crosses one in the late sixties,
exactly where the population data finds the crossover. **`rho` is not scaled below 65**: it
is a property of a life already certified, not of the gate.

**The disclosed basis, and the calibration gap this model publishes rather than hides.**
Exactly one retrieved document gives a Korean long-term-care incidence rate — the 우체국
상품요약서's 예정위험률 for the 1종(일반가입) form [S1]:

| 위험률 | 성 | 40세 | 50세 | 60세 |
|---|---|---|---|---|
| 요양(1등급) 발생률 | 남 | 0.000028 | 0.000080 | 0.000237 |
| | 여 | 0.000010 | 0.000046 | 0.000209 |
| 요양(2등급) 발생률 | 남 | 0.000018 | 0.000072 | 0.000293 |
| | 여 | 0.000007 | 0.000042 | 0.000250 |

Summing the two rows for a combined 1·2등급 rate is an **upper bound**, the two events
being mutually exclusive at first certification, and the log-linear graduation between the
three quoted ages is **[std]**. `disclosed_inc_ratio_at(x)` publishes the model's own
first-entry rate — direct entry plus progression by lives already certified at a light
grade — over that disclosed rate. **Both terms are read on the sub-65 convention the
projection itself uses**, the whole basis being evaluated at `x_e = max(x, 65)` and carried
down on `sub65_factor_at`:

    model_rate(x) = i_D(x) + P_L(x_e) rho(x_e) sub65_factor_at(x) / ( 1 − P_C(x_e) )

Reading `P_L` and `rho` at `x` itself below 65 — the shorter form the identity suggests —
mixes an unscaled light-grade prevalence with a scaled direct rate and returns 0.2670 at
만나이 40 instead of the 0.2399 below. On the male anchor
cell it runs **0.2399 at 40, 0.2465 at 50 and 0.2399 at 60**: the disclosed pricing rate is
about **4.2 times** the model's best estimate, almost flat in age, rising to 0.58 at 85.

**Four things all point the same way and none is quantified by any retrieved source.** A
예정위험률 is a **loaded pricing rate** for a select, underwritten, 180-day-waited
population, not a best estimate. The conversion reads a **cross-section as a cohort path**
in a scheme whose certified stock grew **71.8%** in six years [R4] [R16], which understates
entry. The care compartment is treated as leaving **only by death**, when 9.2% of
certifications arose from a 등급변경신청 [R4 표2-5](#krlib-long_term_care-r4), which understates entry again. And the
card is quoted on **보험나이**, about half a year older than this model's 만나이. **This is
the largest single uncertainty in the model** and it is carried as a stated sensitivity
rather than closed with an invented factor.

The bracket behind `care_mort_mult` is the same arithmetic. In a stationary population
`prevalence = incidence × mean duration`. [R11]'s 516.2 days used as the duration gives
`I(65+) ≈ 10.85% / 1.414 = 7.67%` a year — transparently impossible, and its own refutation.
The yearbook's application-route bucket gives `E ≈ 318,992 / 1.4 ≈ 228,000` first entries a
year and hence `D ≈ 1,165,030 / 228,000 ≈ 5.1` years [derived]; the stock roll-forward
(1,097,913 → 1,165,030, a net +67,117 [R18]) agrees. `D` is near **4 to 5.5 years** and the
all-grade 65+ entry rate near **2 to 3.5%** a year — a factor-of-two bracket, and the honest
width of what the retrieved evidence supports.

**Monthly conversions [std].** Decrements are converted geometrically,
`1 − (1 − annual)^(1/12)`; incidence and progression are converted **uniformly**,
`annual / 12`, within the policy year. The two conventions differ and the reason is that a
decrement compounds against survivorship while an entry rate is applied to a stock that the
same month's decrements have not yet touched.

**The dementia rider's own basis [std].** A logistic `(0.8298, 0.08706045, 100.12641335)`
fitted to the five sourced band prevalences of the 2023 치매역학조사 — 4.99% at 65–69,
5.03% at 70–74, 10.70% at 75–79, 15.57% at 80–84 and 21.18% at 85+ [R7] — times the sourced
65+ sex factors, **0.9568** (M) and **1.0346** (F) [R7, derived](#krlib-long_term_care-r7), and run through the same
prevalence-to-incidence identity with the dementia state's own excess mortality
(`dem_mort_mult = 2.5` **[std]**, between the light and care multiples). Every dementia case
is CDR 1 or above by definition, CDR 0.5 being 경도인지장애 and not dementia, so this is the
prevalence the composite's 경도이상 tier is exposed to; a benefit at CDR 3 이상 would reach
about a third of it — 경증치매 (CDR 1–2) is **67% of all dementia cases** [R8], and the
market prices the three tiers at **3.05 : 2.06 : 1.00** [S2, derived], which agrees.

**Two weaknesses of that fit are named rather than smoothed.** The 65–69 and 70–74 anchors
are almost equal (4.99% and 5.03%), which no logistic can reproduce, and the fit is out by
**31%** at 70–74. And the sex factor is applied **flat in age** **[std]** while the sourced
series has the male rate above the female at 65–79 and below it at 80 and over [R7] — so the
model does **not** reproduce the market fact that 치매 covers are priced *cheaper* for women
while 장기요양 covers are priced dearer (경도이상치매 여 40 ₩13,920 against 남 ₩17,400, a
ratio of 0.80, in the same document that prices the main contract at 1.52 the other way)
[S2, derived]. A user who turns the rider on should know that the two modules share a sex
basis they should not.

`dementia_wait_mths = 15` is **sourced arithmetic**, not a standardization: the **one-year**
보장개시일 [S2] [S4] plus the **90-day persistence** test written into the definition of the
state itself — 「진단일부터 90일 이상 계속되어 장래에 더 이상의 호전을 기대할 수 없는」 [S2].
The one-year wait is not a carrier choice: it is the settled market answer to the 2019
supervisory intervention that followed the 경증치매 boom [R8] [R10].

**Lapse [std], on a form the regulator prescribes rather than the market observes.**
감독규정 제7-66조제4항 permits the **미지급형** form only where the premium was calculated
using a **최적해지율** [REG-R19], and the FSS's November 2024 계리가정 ruling then fixes the
shape: among models converging to zero lapse at 완납 the **로그-선형 모형** is the
**원칙모형**, converging to **0.1%**, with a post-완납 ultimate of **0.8%**; anything else
is permitted only against disclosure in the audit report and the 경영공시, external
actuarial verification, quarterly reporting of the difference to the FSS in CSM,
best-estimate liability, K-ICS ratio and net income, and submission to an on-site inspection
[REG-R27]. So `lapse_table.csv` carries three segments and a comparison vector, not a
policy-year grid:

| parameter | `lapse_year1` | `lapse_completion` | `lapse_ultimate` | `lapse_level_std` |
|---|---|---|---|---|
| annual rate | **8.0%** | **0.1%** | **0.8%** | **4.0%** |

    lapse_rate(t) = r0 × (r1 / r0)^((y − 1)/(n_Y − 1))  for policy year y ≤ n_Y     [REG-R27]
                  = r2                                   for y > n_Y
    lapse_rate_mth(t) = 1 − (1 − lapse_rate(t))^(1/12)                                  [std]

on the `mujihae` form, and `lapse_level_std` at every duration on the `pyojun` comparison
vector — which is the comparison the guidance requires an insurer to disclose. **Two of the
four are standardizations** — the 8.0% first-year level and the 4.0% 표준형 comparison level,
both **[std]** — while the 0.1% and the 0.8% are the ruling's own numbers.
It has **no observed range**, because no Korean durational persistency series for a
보장성보험 was retrieved. The **instrument-level caveat is real**: the 「IFRS17 주요
계리가정 가이드라인」 attachment was never converted from HWP, so the values are verified
from the 보도자료 and the functional form is **[unverified]** at instrument level [REG-R27]
[R14, secondary](#krlib-long_term_care-r14).

Note what the vector says about a contract with **no soft landing**: with no surrender value
there is no policy loan and therefore no 보험료 자동대출납입, so a missed premium lapses the
contract outright [REG-R25 제33조](#krlib-reg-r25) [REG-R28] — and the assumption nonetheless has lapse
*falling* toward 납입완료. That is the regulator's judgement, not the model's, and it is
applied here as given.

**Lapse applies to the premium-paying compartments only, and that is a constraint rather
than an assumption.** A life in the care state has the premium waived [S3] and is barred
from surrendering [S1], so `pols_care` is not exposed. A light-grade life is exposed on the
same rate as a healthy life, because the contract does nothing for it.

**Expenses and commission (all levels [std]; neither of the two largest is free).** No
사업방법서 and no 보험료 및 해약환급금 산출방법서 was retrieved for any Korean
long-term-care product, so every expense assumption here is a standardization — but the
acquisition scale is bounded from above by regulation and the maintenance scale is
calibrated to a sourced identity.

| Input | Value | Basis |
|---|---|---|
| Acquisition expense | **`expense_acq_mths` = 5.2 × P** = ₩29,120 at `t = 0` | **[std]**, constrained: `13.0 − 7.8` |
| Initial commission | **`comm_init_mths` = 7.8 × P** = ₩43,680 at `t = 0` | Sourced bound [REG-R29] [REG-R22]: 60% of the 표준해약공제액 |
| Renewal commission | **3.0%** of premium income from `t = 12` | **[std]**; no Korean renewal-commission scale was retrieved |
| Maintenance expense | **₩200** per policy per month, inflating 2.0% p.a. at each 계약해당일 | **[std]**, calibrated — see below |
| Claim expense | **₩30,000** per claim **event** | **[std]** |
| Expense inflation | **2.0% p.a.** flat | **[std]**, the Bank of Korea target |
| 표준해약공제액 | **`surr_chg_ratio` = 13.0 × P**, running off straight-line over `surr_chg_years = 7` | [REG-R29]; [REG-R19 제7-66조제1항](#krlib-reg-r19) |

The acquisition expense and the initial commission together are **13 times the monthly
premium**, exactly the 표준해약공제액 of a 보장성보험 in the supervisor's own rule of thumb
[REG-R29], split **5.2 : 7.8** so that the commission sits at the 60% cap the same release
sets and 감독규정 제4-32조제8항 now carries [REG-R22], and bounded from above by [별표 14]
[REG-R20]. `expense_maint` is then set so that the present value of the whole expense and
commission basis at the 예정이율 lands on the **20.68%** loading `net_prem_ratio()` implies
from the published 환급률 progression; it lands at **20.26%**. So the expense basis is
calibrated to the same two sourced facts as the account rather than picked.

**The rule of thumb is used in place of the [별표 14] formula deliberately.** [별표 14]
states the 표준해약공제액 as `연납순보험료 × 5% × 해약공제계수 + 보험가입금액 × 10/1000`
[REG-R20], and the second term needs a 보험가입금액 that a product with no death benefit
does not have. The chassis solves that through [별표 15] 제9호's ratio-of-risk-premiums
construction and a `notional_sa_ratio` **[std]**. That route is **not available here**:
제9호's third bullet excludes 「치매 또는 일상생활장해 등 타인의 간병을 필요로 하는 상태」
risk premium from the very ratio [REG-R21]. Read literally, the formula excludes
long-term-care risk premium from the notional 보험가입금액 of a long-term-care contract. The
13-month rule of thumb is the honest way through, and this document says so rather than
inheriting a construction that does not apply.

**The claim expense is charged per *event*, not per instalment.** The events are the first
certification, **each annual 간병연금 survival test**, and a dementia diagnosis. The
annual — not monthly — unit is contractual: 「매년 진단 확정일에 피보험자의 주민등록등본을
제출하여야 합니다」 [S1]. The level is higher than a cancer chassis's would be because the
evidence is a **장기요양인정서 produced by a public body the insurer neither funds nor
influences**, and because the refusal grounds are administrative — 「허위 또는 부당 판정사실
이 확인되는 경우」 nothing is paid [S1] [S2].

**The 계약자적립액 reconstruction, and why it is derived rather than assumed.** `av_pp(t)`
has two branches meeting at 납입완료. Up to it, the accumulation of the net premium at the
예정이율; after it, a sourced run-off. The run-off anchors are one carrier's published
해약환급금 미지급형 환급률 progression at 40세, 주계약 1,000만원, 90세만기, 20년납, 월납 —
**48.7%** at 20 years, **54.4%** at 30, **50.5%** at 40, **0.0%** at 50 [S2] — **doubled**,
because that form pays 50% of the notional 기본형 value once the premiums are paid and the
해약공제 has expired. Indexing them on the **fraction of the way from 납입완료 to maturity**
rather than on the policy year is **[std]** and is what lets one published progression serve
every term and paying period. Then

    net_prem_ratio() = av_ratio_at(0) × n_P / prem_accum_factor(n_P)

is the fraction of the office premium that, accumulated at the 예정이율 over the paying
period, reproduces the sourced account at 납입완료 — **0.7931662309087683** on the anchor
cell, implying a 예정사업비 loading of **20.68%**. **Deriving it is what makes the
surrender-value cliff reproduce the carrier's own figures instead of merely resembling
them**, and `check_av_continuity()` fails the moment someone replaces the derivation with a
round number.

Two reconstruction steps are **[std]** and are named rather than buried. The published
progression is the *미지급형's* 환급률 against its own premiums, and the model reads the
doubled figure as that contract's own 계약자적립액 — but the 기본형 comparator is a product
that **cannot be bought**, 「'기본형'은 … 가입이 불가능하며 … 해지율을 적용하지 않고
계산합니다」 [S2], and its premium is higher, so the two accounts are not in fact the same
quantity. And the run-off **between** the four anchors is linear, where the real curve bends
with the risk cost.

---

## Cash flow components and recursions

### Notation

| Symbol | Cells | Meaning |
|---|---|---|
| `t` | — | policy month, **0-based**: `t = 0, 1, …, n − 1` where `n = proj_len()` |
| `n` | `proj_len` | the **number** of projected months, the frame's exclusive end; the last index is `n − 1` and the maturity month is `t = n − 1` |
| `x`, `age(t)` | `issue_age`, `age` | 만나이 at the 계약일; attained 만나이 `x + floor(t/12)` |
| `y(t)` | `policy_year` | policy year, the derived 1-based label `floor(t/12) + 1` |
| `n_Y`, `n_P` | `prem_period_years`, `prem_period_mths` | 납입기간 in years and in months, `n_P = 12 n_Y`. **`n` is the length of the projection frame — the horizon is `n − 1` months — and never the paying period** |
| `P` | `premium_mth_pp` | level monthly office premium, `uw_loading × premium` |
| `A_B` | `lump_amount` | 장기요양진단급여금 sum insured |
| `A_1`, `A_2` | `annuity_high`, `annuity_low` | 간병연금 monthly amount at 1등급 / other grades in the gate |
| `G_B` | `benefit_grade` | the contractual 등급 threshold |
| `n_A`, `g_A` | `annuity_max_mths`, `annuity_guar_mths` | 120-month cap; 12-month guarantee |
| `W`, `G` | `wait_mths`, `red_mths` | 보장개시일 and 감액기간, in whole months |
| `P(x)` | `prev_rate_at` | all-grade certification prevalence |
| `s_G(x)` | `share_ge_at` | share of certified lives at grade `G` or above |
| `P_C(x)`, `P_L(x)` | `prev_care_at`, `prev_light_at` | prevalence at/above and below `G_B` |
| `mu_H`, `mu_L`, `mu_C`, `mu_bar` | `mort_force_*_at` | the four forces of mortality |
| `i_D`, `i_L`, `rho` | `inc_rate_direct_at`, `inc_rate_light_at`, `prog_rate_at` | the three annual transition rates; `_mth` = `/12` |
| `q_H(t)`, `q_L(t)`, `q_C(t)` | `mort_rate_*_mth` | monthly mortality of the three compartments |
| `w(t)` | `lapse_rate_mth` | monthly lapse, on the paying compartments only |
| `h`, `l_L`, `l_C`, `l` | `pols_healthy`, `pols_light`, `pols_care`, `pols_if` | the three compartments and their total |
| `n_L`, `n_D`, `n_P*`, `n_C` | `pols_entry_light`, `pols_entry_care_direct`, `pols_entry_care_prog`, `pols_entry_care` | the month's certifications |
| `r(t)` | `red_factor` | 감액 factor applying to a certification **dated** in month `t` |
| `A(s)` | `ann_amount_at` | the frozen monthly annuity of the cohort certified in month `s` |
| `S_C(s, t)` | `care_surv` | care-state survival from month `s` to month `t` |
| `AV(t)`, `CV(t)` | `av_pp`, `cv_pp` | 계약자적립액; 해약환급금 |
| `CF(t)` | `net_cf` | net cash flow, **income-positive** |

**Dimensional check.** `P`, `P_C`, `P_L` and `s_G` are dimensionless **proportions of a
population**; `P'`, `P_C'`, `i_D`, `i_L` and `rho` are **rates per year**; `mu_H`, `mu_L`,
`mu_C`, `mu_bar` are **forces per year**; `q_*`, `w` are probabilities per month. `prev_beta`
carries units of **1/year**, which is why `P' = beta P (1 − P/ceil)` comes out as a rate per
year and can be added to `P_C (mu_C − mu_bar)`, also a rate per year — the two terms of the
identity are dimensionally the same object, and a version that adds a prevalence to a rate is
the commonest way to get this wrong. `A_B` is KRW per event, `A_1` and `A_2` KRW per
instalment, so `A_B r(t) n_C(t)` and `A(s) n_C(s) S_C(·)` are KRW per policy-month. **The
error this check catches is the one that dominates this product: multiplying the published
인정률 — a prevalence, 10.85% at 65+ — by a benefit amount as if it were an annual claim
frequency.**

### The four-compartment chain and its processing order

For `t = 0, 1, …, n − 2` — the months of cover; the terminal month `t = n − 1` is the
maturity row and carries no cash flow — with the state at the **start** of the month being
`h(t)`, `l_L(t)`, `l_C(t)`:

**1. Start of month — premium, maintenance expense, renewal commission.**

    premiums(t)    = P × pols_act(t)              for t < n_P,  else 0
    expenses(t)    = expense_acq_mths × P × 1{t = 0}
                     + expense_maint × (1 + pi)^floor(t/12) × pols_if(t)
    commissions(t) = comm_init_mths × P × 1{t = 0} + 0.03 × premiums(t) × 1{t ≥ 12}

Premium rides on **`pols_act`, never on `pols_if`**: the 납입면제 waives the 기본계약 and
every attached rider from the award of 1·2등급 [S3], and waived premiums are treated as
paid. Maintenance expense rides on **`pols_if`, including lives on waiver** — the policy is
still administered when nobody is paying for it.

**2. Certification, from the start-of-month counts.**

    n_L(t) = h(t)   × i_L(age(t))  / 12
    n_D(t) = h(t)   × i_D(age(t))  / 12
    n_P*(t)= l_L(t) × rho(age(t))  / 12

    n_C(t)   = n_D(t) + n_P*(t)   for t ≥ W ;  0 otherwise
    void(t)  = n_D(t) + n_P*(t)   for t < W ;  0 otherwise

`n_L` is drawn from the never-certified population alone. `n_P*` — progression — is drawn
from the light compartment, and above 65 it is the **dominant** route. Inside the
보장개시일 window a certification does **not** defer the claim: the benefit is 무효, the
premiums paid for it come back, and the life leaves the model. `void` is therefore a
**decrement**, not a claim refusal, and the two are kept apart because the 약관 keep them
apart.

**3. End of month — benefits and the claim-handling expense.**

    claims_lump(t)     = A_B × r(t) × n_C(t)
    claims_annuity(t)  = ann_pay(t)
    claims_dementia(t) = dementia_amount × pols_entry_dem(t)
    claims_death(t)    = AV(t) × pols_death_act(t)
    claims_lapse(t)    = CV(t) × pols_lapse(t)
    claims_void(t)     = cum_prem_pp(t + 1) × void(t)
    claims_maturity(t) = 0
    claim_expenses(t)  = expense_claim × ( n_C(t) + ann_tests(t) + pols_entry_dem(t) )

**4. Mortality**, on the mid-month counts.

    h_mid(t)   = h(t)   − n_L(t) − n_D(t)
    l_L_mid(t) = l_L(t) + n_L(t) − n_P*(t)
    l_C_mid(t) = l_C(t) + n_C(t)                     — the voided are NOT here

    pols_death_act(t)  = h_mid(t) q_H(t) + l_L_mid(t) q_L(t)
    pols_death_care(t) = l_C_mid(t) q_C(t)

Only `pols_death_act` pays: deaths **in** the care state pay nothing, 「지급사유가 발생한 후
사망한 경우에는 별도로 책임준비금을 지급하지 않습니다」 [S1]. That split is a cash-flow
distinction and not bookkeeping.

**5. Lapse**, on the mortality survivors of the paying compartments only.

    pols_lapse(t) = ( h_mid(t) (1 − q_H(t)) + l_L_mid(t) (1 − q_L(t)) ) × w(t)

**6. Roll forward.**

    h(t+1)   = h_mid(t)   × (1 − q_H(t)) × (1 − w(t))
    l_L(t+1) = l_L_mid(t) × (1 − q_L(t)) × (1 − w(t))
    l_C(t+1) = l_C_mid(t) × (1 − q_C(t))
    l(t+1)   = h(t+1) + l_L(t+1) + l_C(t+1)

**7. Maturity** on the frame's last row `t = n − 1`: `pols_maturity(n − 1) = pols_if(n − 1)`,
paying nothing.

`check_pols_roll_fwd()` asserts, over `t = 0 … n − 1`,

    l(t) − l(t+1) = pols_death(t) + pols_lapse(t) + void(t) + pols_maturity(t)

with a tolerance of `roll_fwd_tol = 1e-12`, and `check_nesting()` asserts that the three
compartments are non-negative, add to `pols_if`, and contain the dementia counter.

### The 감액 factor, and the fact that it is frozen

    r(t) = 1 − (1 − red_fraction) × disease_share     for t < G
         = 1                                          for t ≥ G

with `red_fraction = 0.50` **sourced** [S4] and invariant wherever a 감액 is stated. The
약관 test is on the **cause**, not on the grade: a 질병-caused certification inside the
window is paid at 50%, an 상해/재해-caused one in full [S4]. **The relative frequency of the
two is given by no retrieved source**, so `disease_share = 0.95` is **[std]** and the
accident carve-out is named rather than dropped; the blended factor is **0.525**.

`r` is evaluated at the **certification** month `s`, never at the payment month. 「최초 진단
확정일을 기준으로 경과기간 2년미만의 보험금 감액여부가 결정됩니다. 따라서 … 그 이후에
도래하는 매년 진단 확정일이 계약일부터 2년이상에 해당하더라도 … 지급액은 변경되지
않습니다」 [S1]. A claim that starts inside the reduction window stays halved **for the whole
ten years of the annuity**.

### The 간병연금 ledger

The cohort certified in month `s` is paid **monthly** in months `s … s + n_A − 1`. The first
`g_A` instalments are guaranteed against death; each later block of twelve is released only
by the annual survival test on the anniversary of the 진단확정일:

    S_C(s, t)      = product over u = s … t−1 of ( 1 − q_C(u) )
    weight(u)      = 1                                for u < g_A
                   = S_C(s, s + 12 × floor(u/12))     otherwise
    ann_count(t)   = sum over u = 0 … min(t, n_A − 1) of  n_C(t − u) × weight(u)
    ann_pay(t)     = sum over the same u of  A(t − u) × n_C(t − u) × weight(u)
    ann_tests(t)   = sum over k = 1 … n_A/12 − 1 of  n_C(t − 12k) × S_C(t − 12k, t)

with the frozen amount

    A(s) = [ s_1(x_s) A_1 + ( s_G(x_s) − s_1(x_s) ) A_2 ] / s_G(x_s)  ×  r(s)
    x_s  = max( age(s), 65 )

— the age-specific grade blend of `A_1` at 1등급 and `A_2` at every other grade inside the
gate, times the 감액 factor at `s`. **Both the amount and the reduction are frozen at `s`**,
which is what makes a cohort entering at 만나이 68 keep its own amount for all ten years
whatever later cohorts are paid.

Three properties of this ledger deserve to be in front of a reader.

- **The `u = 0` term is `n_C(t)` itself.** The first instalment falls in the **month of
  certification**, not a year later [S1]. Deferring it removes roughly a tenth of the
  annuity liability and misdates all of it.
- **`S_C` is computed as a partial product, never as a ratio of cumulative products.**
  `q_C` is `min(1, 3 q(x))` and the cap binds from 만나이 **108** on the shipped male table
  — `3 × q(108) = 1.0714` — and from **112** on the female one, so a cumulative product
  underflows to zero from there on and the ratio form divides by zero exactly where the tail
  of a 종신 variant of this liability would live.
- **The cap and the maturity truncation bind jointly.** Nothing is paid on the maturity row
  `t = n − 1` or after it, so a life certified at 만나이 85 on a 90세만기 contract gets five
  years of annuity and not ten. That is the **conservative reading** of a question no retrieved
  document resolves **[std]**, and it materially understates the benefit for a late
  entrant.

`check_ann_ledger()` rebuilds `ann_count(t)` by scanning **every** month in the window
`t − n_A < s ≤ t` and re-deriving each cohort's weight from its own age, rather than
stepping back through the same loop. A ledger that paid the first instalment a year late,
that ran past the cap, that lost the twelve-month guarantee, or that used a ratio form of
`S_C`, shows up there.

### The 계약자적립액 and the 해약환급금

    cum_prem_pp(t)      = P × min(t, n_P)          — paid before month t's own premium
    prem_accum_factor(t)= (1 + j) ( (1 + j)^t − 1 ) / j,   j = (1 + 0.02)^(1/12) − 1
    net_prem_ratio()    = av_ratio_at(0) × n_P / prem_accum_factor(n_P)

    AV(t) = net_prem_ratio() × P × prem_accum_factor(t)             for t ≤ n_P
          = av_ratio_at( (t − n_P) / (n − 1 − n_P) ) × P × n_P      for t > n_P

    surr_chg_pp(t) = surr_chg_ratio × P × ( 1 − t / n_chg ),  n_chg = 12 min(7, n_Y)
                   = 0 for t ≥ n_chg

    CV(t) | mijigeup     = 0                for t < n_P ;  0.5 × AV(t) otherwise
          | half_during  = 0.5 × AV(t)      for t < n_P ;  AV(t)       otherwise
          | pyojun       = max( AV(t) − surr_chg_pp(t), 0 )

**Reading 「50%」 without reading which side of 납입완료 it attaches to puts the cliff upside
down**, which is why the form is a model point field and not a switch on a ratio. Four forms
are on the Korean shelf under three nearly identical names and they are **different
products, not variants**: 미지급형 pays nothing during and 50% of a notional 기본형 after
[S2]; 납입중50%해약환급금지급형 pays 50% **during** and 100% after [S4]; 삼성화재 sells the
pure protection form with 「만기환급금 : 없음」 and no 무·저해지 variant in the retrieved
extract [S3]; and 우체국 is a conventional 표준형 with a normal surrender value from year 1,
because 우정사업본부 business is not written under 보험업법 [S1]. `check_cv_form()` asserts
the sign of the cliff, not merely its magnitude.

### Net cash flow

    net_cf(t) = premiums(t)
              − claims_lump(t) − claims_annuity(t) − claims_dementia(t)
              − claims_death(t) − claims_lapse(t)  − claims_void(t)
              − claims_maturity(t)
              − expenses(t) − claim_expenses(t) − commissions(t)

**`net_cf` is income-positive**, which is this library's sign and this document's own, so
there is deliberately **no outgo-positive `liability_cf` companion** to publish and the
conventions suite skips its orientation test on that basis. `check_net_cf()` asserts that
`net_cf` re-adds from exactly the eleven published columns of `result_cf()`, to
`val_tol = 1e-06`: the house contract is that no model's headline number is reconciled only
in prose.

Note that `claims_death` is **not a death benefit**. The contract has none. It is the
**계약자적립액** that 감독규정 제7-63조제1항제1호 makes payable on a death from a cause the
contract does not cover [REG-R17], and on the anchor cell it is **₩326,783.93** undiscounted
against ₩973,533.06 of premium — a third of premium income — because 35.4% of the cohort
dies before maturity and the account is worth close to cumulative premiums at long
durations. **That is a genuine and distinctive Korean result and it should be read, not
smoothed.** The Japanese counterpart has no such payment at all.

### Optional modules (all off in the base run except the 간병연금)

| Module | Switch | Base run |
|---|---|---|
| **간병연금** | `annuity_on` | **On.** It is two thirds of the anchor cell's benefit outgo and the reason the product is a three-state model |
| **치매진단급여금** | `dementia_rider`, `dementia_amount` | **Off.** A different trigger (CDR, a 치매 전문의) with a different sex basis and a 15-month effective wait |
| 간편심사 | `uw_loading` | **Off** (1.0). A **premium** multiplier only: no retrieved source gives the simplified pool's incidence, so on a loaded point the extra premium is pure margin in this model |
| Threshold | `benefit_grade` | `g2`. `g1` … `g6` reachable without a second chassis |
| Surrender-value form | `cv_form` | `mijigeup`. `half_during` and `pyojun` as switches |
| Lapse vector | `lapse_form` | `mujihae`. `pyojun` is the level comparison vector [REG-R27] requires an insurer to disclose |
| Waiting / reduction | `wait_mths`, `red_mths` | 3 / 12. The 우체국 6 / 24 combination is model point 9 |

**Not modelled, and each is a deliberate scope decision.** The **utilisation-conditioned
지원금 riders** [S2] — which pay ₩100,000 a month only where the insured is actually using
재가급여, 시설급여, 주·야간보호 or 복지용구 — need a utilisation rate by grade, by service
type and by duration since certification, which no retrieved source gives; [R4 표3-3](#krlib-long_term_care-r4) gives
급여이용 수급자 by service type as a national aggregate with substantial overlap, not the
cross-tabulation the module would need, and a module whose central assumption would be
**entirely [std]** adds nothing. The **종신 income form** [S2] [S5] carries the whole
longevity tail after onset with no cap on a post-onset mortality basis nobody publishes.
The **두 번째 장기요양지원금(1~2등급)** persistency rider, with its five-year 면책 running
from the first 1·2등급 판정일 [S3], needs exactly the continuance basis that does not exist.
The **간병인사용일당** is a different product. And **교보's premium refund on a 1~4등급
진단** [S5] would materially change the reserve; it is a press-release fact whose mechanics
are [unverified].

---

## Policyholder behavior modeling

- **Lapse stops at the benefit trigger, and here that is a *constraint*, not a
  refinement.** Once 1·2등급 is awarded the premium is waived [S3] and the 약관 bars
  surrender outright — 「최초 지급사유가 발생한 후에는 이 특약을 해지할 수 없습니다」 [S1] —
  so zero lapse in the care state is what the contract says. Applying lapse there is not a
  conservative choice; it is a wrong one, and it is **silent**: the annuity ledger is driven
  by `n_C` and `S_C`, not by `pols_care`, so the annuity does not move at all and the only
  visible effect is a surrender value paid to a life that cannot surrender. See the
  pitfalls.
- **The waiver fires on the same event as the benefit, which inverts the Japanese
  pattern.** In `jplib`'s 介護保険 the waiver fires at a *lower* grade than the lump sum and
  creates a band of lives paying nothing and claiming nothing — the single most
  mis-modelled item in that product. Here `G_W = G_B`, following the only observed
  whole-contract waiver [S3], so **there is no such band**. But the waiver is not free: it
  stops the premium for as long as the insured **survives in the care state**, which is
  exactly the quantity the prevalence-to-incidence conversion cannot pin down. **The waiver
  is where post-onset mortality enters even a lump-sum-only version of this contract.** On
  the anchor cell it costs **₩414.65** of premium income over the paying period, 0.043% of
  the total — small only because the certification rate at issue age 40 is small.
- **The light compartment pays and lapses, and that is the delta against the Japanese
  product and the parallel with the chassis.** A 3~5등급 life has been certified by the
  state, carries impaired mortality, and receives nothing; the contract goes on charging it
  and it can still walk away. Over the anchor cell's projection the light compartment
  accumulates **10.79 policy-months** of exposure against the care compartment's **1.74**.
- **Anti-selection is at the front door, and it is unusually direct.** What is being
  selected against is an application to a public body that leaves a record, which is why the
  간편심사 question set asks 「현재 노인장기요양보험에 의한 장기요양급여 수급자이거나
  **장기요양인정 심의 중**입니까?」 [S2] and why one carrier will not attach its 장기요양
  riders to a simplified chassis at all — 「주계약 1종(일반가입)에 한하여 부가 가능」 [S1].
  That refusal is itself a statement about anti-selection on this trigger. The composite is
  fully underwritten; no selection loading is applied at issue, and the 간편심사 pool is
  carried as a **premium** multiplier with its incidence unchanged, so the true claim cost
  of that pool is **understated** in this model.
- **The waiting period is anti-selection with teeth.** A certification inside the window
  does not merely fail: the benefit is **무효** and premiums come back [S1] [S2]. Unlike the
  chassis there is **no cancellation option** and **no revival**, so an insured certified
  during the window has bought a benefit that can never pay for that certification. And
  **reinstatement is not a rewind**: every waiting period in the file is measured
  「계약일[부활(효력회복)일]부터」 [S1] [S2], so a reinstated contract serves its 90 days
  again from the 부활일. `krlib` treats 부활 as a **new model point**, not as a negative
  lapse, and the base run treats lapse as absorbing **[std scope]**.
- **Thresholds and amounts are elected at issue and cannot move.** `benefit_grade`,
  `lump_amount`, `annuity_high` and `annuity_low` are model-point attributes. A code path
  that varies them over `t` models a contract term that does not exist.
- **청약철회 is out of scope.** A 15-day withdrawal right under 금융소비자보호법 제46조 as
  implemented in 표준약관 제17조 [REG-R25] [REG-R51]; `krlib` models from the point cover is
  in force and has no new-business funnel in which to represent it.
- **The claimant usually cannot claim.** A 지정대리청구인 is designated on every retrieved
  product [S1] [S3]. It has no cash-flow effect in this model and it is the operational fact
  that most distinguishes administering this product from administering the chassis.

---

## Worked example

**Anchor cell (`point_id = 1`, `policy_id = LTC-000001`).** Male, 만나이 40 at the 계약일,
90세만기, 20년납, 월납, 해약환급금 미지급형, 일반심사. 장기요양(1~2등급) 진단급여금
`A_B` = ₩10,000,000; 간병연금 **on** at `A_1` = ₩500,000 / `A_2` = ₩300,000 a month with a
12-month guarantee and a 120-month cap; 치매 rider **off**; 보장개시일 `W` = 3 months;
감액기간 `G` = 12 months; `lapse_form = mujihae`; office premium `P` = ₩5,600 a month.
`proj_len() = 12 × (90 − 40) + 1 = 601`, so `result_cf()` carries **601 rows**, indexed
`t = 0 … 600`.

### Every assumption value the first rows use

All at 만나이 40 and in policy year 1, so one set of rates drives rows `t = 0 … 11`.

| Quantity | Value | Basis |
|---|---|---|
| `mort_rate(0)` = `q(40)` | `0.00097601273` | **[std]** Makeham–Gompertz on the 경험생명표 65세 기대여명 anchor [REG-R33] [REG-R34] |
| `mort_rate_mth(0)` = `q_H` | `0.0000813708009308467` | `1 − (1 − q)^(1/12)` **[std]** |
| `mort_rate_light(0)` | `0.001756822914` | `1.8 × q` **[std]** |
| `mort_rate_light_mth(0)` = `q_L` | `0.0001465199263399608` | **[std]** |
| `mort_rate_care(0)` | `0.00292803819` | `3.0 × q` **[std]** |
| `mort_rate_care_mth(0)` = `q_C` | `0.00024433125292278035` | **[std]** |
| `lapse_rate(0)` | `0.08` | **[std]** first-year level; shape [REG-R27] |
| `lapse_rate_mth(0)` = `w` | `0.006924382628299419` | **[std]** |
| `P(40)` | `0.00038039917723430234` | fitted logistic **[std]** through [R4] |
| `P_C(40)` | `0.00008444861734601512` | `s_g2(40) × P(40)`, `s_g2(40) = 0.222` [R4, derived](#krlib-long_term_care-r4) |
| `P_L(40)` | `0.0002959505598882872` | `P − P_C` |
| `sub65_factor_at(40)` | `0.04710884458012182` | `exp(−0.12221178 × 25)`, the [S1] gradient |
| `i_D(40)` | `0.0000022292964462128687` | direct entry, per year |
| `i_L(40)` | `0.00010426974412244515` | light-grade entry, per year |
| `rho(40)` | `0.03396845379835368` | progression, per year — **not** scaled below 65 |
| `i_D(40)/12` | `0.00000018577470385107238` | monthly **[std]** |
| `i_L(40)/12` | `0.000008689145343537096` | monthly **[std]** |
| `rho(40)/12` | `0.0028307044831961396` | monthly **[std]** |
| `disclosed_inc_at(40)` | `0.000046` | [S1], 요양 1등급 + 2등급 발생률 at 40세 남 |
| `disclosed_inc_ratio_at(40)` | `0.23993880644434135` | the model's own first-entry rate over it |
| `red_factor(t)`, `t < 12` | `0.525` | `1 − 0.5 × 0.95`; `red_fraction` [S4], `disease_share` **[std]** |
| `red_factor(t)`, `t ≥ 12` | `1.0` | [S4] |
| `ann_amount_at(s)`, `s < 12` | `207495.7410562181` | grade blend at 만나이 65 × 0.525 |
| `ann_amount_at(s)`, `12 ≤ s`, 만나이 ≤ 65 | `395229.98296422494` | grade blend at 만나이 65 |
| `expense_acq_mths × P` | `29120.0` | 5.2 months **[std]**, constrained by [REG-R29] |
| `expense_maint` | `200.0` | **[std]**, calibrated to `net_prem_ratio()` |
| `comm_init_pp()` | `43680.0` | 7.8 months, the 60% cap [REG-R29] [REG-R22] |
| `expense_claim` | `30000.0` | per **event** **[std]** |
| `net_prem_ratio()` | `0.7931662309087683` | derived from `av_ratio_at(0) = 0.974` [S2] |

**Every decrement above is a construction.** None is an insurer's basis and none could be:
the 산출방법서 is a 기초서류 and is not public [REG-R2], 경험생명표 is not published in full
[REG-R33] [REG-R34], and 보험개발원 publishes neither a 장기요양 incidence table nor a
post-onset mortality table. The only retrieved Korean long-term-care rate anywhere is one
carrier's 예정위험률 [S1], and this model uses it for its **gradient and sex ratio**, never
for its level.

### The first policy year, cash flow

Values as the model produces them, to six decimal places. `claims_dementia`,
`claims_lapse` and `claims_maturity` are identically zero over this range and are omitted;
they are in the totals below.

| t | `pols_if` | `premiums` | `claims_lump` | `claims_annuity` | `claims_death` | `claims_void` | `expenses` | `claim_expenses` | `commissions` | `net_cf` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1.000000 | 5600.000000 | 0.000000 | 0.000000 | 0.000000 | 0.001040 | 29320.000000 | 0.000000 | 43680.000000 | -67400.001040 |
| 1 | 0.992995 | 5560.769900 | 0.000000 | 0.000000 | 0.359493 | 0.002340 | 198.598925 | 0.000000 | 0.000000 | 5361.809142 |
| 2 | 0.986038 | 5521.814482 | 0.000000 | 0.000000 | 0.714544 | 0.003891 | 197.207660 | 0.000000 | 0.000000 | 5323.888388 |
| 3 | 0.979131 | 5483.131826 | 1.333122 | 0.052689 | 1.065193 | 0.000000 | 195.826137 | 0.007618 | 0.000000 | 5284.847067 |
| 4 | 0.972272 | 5444.720021 | 1.448226 | 0.109927 | 1.411483 | 0.000000 | 194.454337 | 0.008276 | 0.000000 | 5247.287772 |
| 5 | 0.965461 | 5406.577174 | 1.561294 | 0.171634 | 1.753454 | 0.000000 | 193.092148 | 0.008922 | 0.000000 | 5209.989723 |
| 6 | 0.958698 | 5368.701402 | 1.672351 | 0.237731 | 2.091145 | 0.000000 | 191.739501 | 0.009556 | 0.000000 | 5172.951118 |
| 7 | 0.951982 | 5331.090836 | 1.781423 | 0.308138 | 2.424598 | 0.000000 | 190.396330 | 0.010180 | 0.000000 | 5136.170167 |
| 8 | 0.945313 | 5293.743621 | 1.888537 | 0.382778 | 2.753852 | 0.000000 | 189.062569 | 0.010792 | 0.000000 | 5099.645094 |
| 9 | 0.938691 | 5256.657915 | 1.993717 | 0.461576 | 3.078946 | 0.000000 | 187.738151 | 0.011393 | 0.000000 | 5063.374132 |
| 10 | 0.932115 | 5219.831887 | 2.096990 | 0.544455 | 3.399919 | 0.000000 | 186.423012 | 0.011983 | 0.000000 | 5027.355528 |
| 11 | 0.925585 | 5183.263720 | 2.198380 | 0.631342 | 3.716809 | 0.000000 | 185.117086 | 0.012562 | 0.000000 | 4991.587540 |
| 12 | 0.919102 | 5146.951609 | 4.601130 | 0.813192 | 4.308813 | 0.000000 | 187.496714 | 0.013803 | 154.408548 | 4795.309407 |

**Four rows in that table are where the product does something.**

- **`t = 0`** is the new-business strain: one month's premium against 5.2 months of
  acquisition expense, one month of maintenance and the whole 7.8 months of initial
  commission — and, because of the row below, ₩0.001040 of refund on top.
- **`t = 0`, `t = 1` and `t = 2`** carry a non-zero `claims_void` and no other benefit.
  These are the certifications inside the 보장개시일 window: the cover is 무효 and the
  premiums paid for it come back. **The refund is `cum_prem_pp(t + 1)`, not
  `cum_prem_pp(t)`** — premium falls at the *start* of month `t` and the void is recognised
  at the *end* of it, so a life voided in month 0 has paid one month's premium and gets it
  back, which is why `claims_void(0)` is ₩0.001040 rather than nil. Valuing the refund at
  `cum_prem_pp(t)` would leave the insurer holding a month's premium on a cover it had just
  declared never to have existed.
- **`t = 3`** is the **first payable certification**: the 보장개시일 is three whole months,
  so `claims_lump` and `claims_annuity` both start here, and `claim_expenses` with them.
- **`t = 12`** is the **감액기간 expiring and the renewal commission starting**, in the same
  row. `claims_lump` roughly doubles — from 2.198380 to 4.601130 — because `red_factor`
  steps from 0.525 to 1.0, and `commissions` goes from nil to 3% of premium. The
  `expenses` line also steps, from 185.117086 to 187.496714, because the 2% expense
  inflation factor increments at the 계약해당일 even though the in-force count has fallen.

### The compartments, first policy year

Policy counts to ten decimal places.

| t | `pols_healthy` | `pols_light` | `pols_care` | `pols_entry_light` | `pols_entry_care_direct` | `pols_entry_care_prog` | `pols_entry_care` | `pols_void` | `pols_death_act` | `pols_lapse` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1.0000000000 | 0.0000000000 | 0.0000000000 | 0.0000086891 | 0.0000001858 | 0.0000000000 | 0.0000000000 | 0.0000001858 | 0.0000813714 | 0.0069238179 |
| 1 | 0.9929859973 | 0.0000086277 | 0.0000000000 | 0.0000086282 | 0.0000001845 | 0.0000000244 | 0.0000000000 | 0.0000002089 | 0.0000808019 | 0.0068753138 |
| 2 | 0.9860211908 | 0.0000171097 | 0.0000000000 | 0.0000085677 | 0.0000001832 | 0.0000000484 | 0.0000000000 | 0.0000002316 | 0.0000802364 | 0.0068271493 |
| 3 | 0.9791052354 | 0.0000254477 | 0.0000000000 | 0.0000085076 | 0.0000001819 | 0.0000000720 | 0.0000002539 | 0.0000000000 | 0.0000796748 | 0.0067793220 |
| 4 | 0.9722377886 | 0.0000336437 | 0.0000002539 | 0.0000084479 | 0.0000001806 | 0.0000000952 | 0.0000002759 | 0.0000000000 | 0.0000791172 | 0.0067318297 |
| 5 | 0.9654185101 | 0.0000416995 | 0.0000005296 | 0.0000083887 | 0.0000001794 | 0.0000001180 | 0.0000002974 | 0.0000000000 | 0.0000785635 | 0.0066846698 |
| 6 | 0.9586470621 | 0.0000496168 | 0.0000008268 | 0.0000083298 | 0.0000001781 | 0.0000001405 | 0.0000003185 | 0.0000000000 | 0.0000780137 | 0.0066378402 |
| 7 | 0.9519231089 | 0.0000573975 | 0.0000011450 | 0.0000082714 | 0.0000001768 | 0.0000001625 | 0.0000003393 | 0.0000000000 | 0.0000774677 | 0.0065913385 |
| 8 | 0.9452463176 | 0.0000650433 | 0.0000014840 | 0.0000082134 | 0.0000001756 | 0.0000001841 | 0.0000003597 | 0.0000000000 | 0.0000769255 | 0.0065451624 |
| 9 | 0.9386163574 | 0.0000725560 | 0.0000018433 | 0.0000081558 | 0.0000001744 | 0.0000002054 | 0.0000003798 | 0.0000000000 | 0.0000763871 | 0.0064993096 |
| 10 | 0.9320328997 | 0.0000799372 | 0.0000022225 | 0.0000080986 | 0.0000001731 | 0.0000002263 | 0.0000003994 | 0.0000000000 | 0.0000758525 | 0.0064537779 |
| 11 | 0.9254956184 | 0.0000871887 | 0.0000026213 | 0.0000080418 | 0.0000001719 | 0.0000002468 | 0.0000004187 | 0.0000000000 | 0.0000753216 | 0.0064085651 |
| 12 | 0.9190041896 | 0.0000943121 | 0.0000030393 | 0.0000090234 | 0.0000001929 | 0.0000002672 | 0.0000004601 | 0.0000000000 | 0.0000799758 | 0.0050125240 |

Two things to read out of it. **`pols_care(3)` is still zero**: the certifications of month
3 are paid in month 3 but enter the stock at the start of month 4. And
**`pols_entry_care_prog` overtakes `pols_entry_care_direct` between `t = 7` and `t = 8`** —
eight months into the contract, at 만나이 40, with the light compartment still only
0.0000650 of the block. Progression is the dominant route from almost the first year, which
is the whole point of the four-compartment structure.

### Hand traces

**Trace, month 0.** `h(0) = 1`, `l_L(0) = l_C(0) = 0`, so `pols_act(0) = pols_if(0) = 1`.

Premium `= 5,600 × 1 = 5,600.000000`.

Certifications: `n_L(0) = 1 × 0.000008689145343537096 = 0.0000086891`;
`n_D(0) = 1 × 0.00000018577470385107238 = 0.0000001858`; `n_P*(0) = 0 × 0.0028307 = 0` —
there is no light compartment to progress out of yet. Because `0 = t < W = 3`,
**`n_C(0) = 0`** and `void(0) = 0.0000001858 + 0 = 0.00000018577470385107238`.
`claims_void(0) = cum_prem_pp(1) × void(0) = 5,600 × 0.00000018577470385107238
= 0.001040` — the refund is valued on the premiums paid by the **end** of the month, and
one has been: the month-0 premium fell at the start of it.

Mid-month counts: `h_mid(0) = 1 − 0.0000086891 − 0.0000001858 = 0.9999911250799526`;
`l_L_mid(0) = 0 + 0.0000086891 − 0 = 0.000008689145343537096`; `l_C_mid(0) = 0`.

Mortality: `pols_death_act(0) = 0.9999911250799526 × 0.0000813708009308467
+ 0.000008689145343537096 × 0.0001465199263399608 = 0.0000813713519`.
`claims_death(0) = AV(0) × 0.0000813714 = 0 × … = 0.000000`, because the account opens at
nil.

Lapse: `pols_lapse(0) = ( 0.9999911250799526 × (1 − 0.0000813708009308467)
+ 0.000008689145343537096 × (1 − 0.0001465199263399608) ) × 0.006924382628299419
= 0.0069238178955`.

Expenses: `5.2 × 5,600 = 29,120` acquisition plus `200 × 1.02^0 × 1 = 200` maintenance
= **29,320.000000**. Commission `= 7.8 × 5,600 = 43,680.000000`. Claim expense
`= 30,000 × (0 + 0 + 0) = 0`.

`net_cf(0) = 5,600.000000 − 0 − 0 − 0 − 0 − 0.001040 − 29,320.000000 − 0 − 43,680.000000
= −67,400.001040`.

Roll forward: `h(1) = 0.9999911250799526 × (1 − 0.0000813708009308467)
× (1 − 0.006924382628299419) = 0.9929859973`;
`l_L(1) = 0.000008689145343537096 × (1 − 0.0001465199263399608)
× (1 − 0.006924382628299419) = 0.0000086277`; `l_C(1) = 0`;
`pols_if(1) = 0.9929859973 + 0.0000086277 + 0 = 0.992995`.

**Trace, month 1.** Every per-policy rate is unchanged — `age(1) = 40`, policy year still 1.

Premium `= 5,600 × pols_act(1) = 5,600 × 0.992994624977843 = 5,560.769900`. Note it rides on
`pols_act`, which here equals `pols_if` only because the care compartment is still empty.

Certifications: `n_L(1) = 0.9929859973 × 0.000008689145343537096 = 0.0000086282`;
`n_D(1) = 0.9929859973 × 0.00000018577470385107238 = 0.0000001845`;
**`n_P*(1) = l_L(1) × rho/12 = 0.0000086277 × 0.0028307044831961396 = 0.0000000244`** — the
first progression in the model. `1 = t < W = 3`, so `n_C(1) = 0` and
`void(1) = 0.0000001845 + 0.0000000244 = 0.00000020889418843702306`.

`claims_void(1) = cum_prem_pp(2) × void(1) = 11,200 × 0.00000020889418843702306
= 0.002340`.

The account: `AV(1) = net_prem_ratio() × P × prem_accum_factor(1)
= 0.7931662309087683 × 5,600 × 1.0016515813 = 4,449.066773`, so
`claims_death(1) = 4,449.066773 × 0.0000808019 = 0.359493`.

Expenses `= 200 × 1.02^0 × 0.992994624977843 = 198.598925`; no acquisition after `t = 0`, no
renewal commission before `t = 12`, no claim expense because nothing payable happened.

`net_cf(1) = 5,560.769900 − 0.359493 − 0.002340 − 198.598925 = 5,361.809142`.

**Trace, month 3 — the first payable certification.** `h(3) = 0.9791052354319798`,
`l_L(3) = 0.0000254477`, `l_C(3) = 0`.

`n_D(3) = 0.9791052354319798 × 0.00000018577470385107238 = 0.00000018189298515141055`;
`n_P*(3) = 0.0000254477 × 0.0028307044831961396 = 0.00000007203498063473715`. Now
`t = 3 ≥ W = 3`, so **`n_C(3) = 0.00000018189 + 0.00000007203 = 0.0000002539279657861477`**
and `void(3) = 0`.

The lump sum, at the reduced factor because `3 < G = 12`:
`claims_lump(3) = 10,000,000 × 0.525 × 0.0000002539279657861477 = 1.333122`.

The annuity's first instalment falls in the same month. The frozen amount is the grade blend
at `x_s = max(40, 65) = 65`, where `s_g1(65) = 0.07985714285714286` and
`s_g2(65) = 0.1677142857142857`:

    blended = ( 0.07985714285714286 × 500,000
              + (0.1677142857142857 − 0.07985714285714286) × 300,000 ) / 0.1677142857142857
            = ( 39,928.571429 + 26,357.142857 ) / 0.1677142857142857
            = 395,229.98296422494

times `red_factor(3) = 0.525` gives `A(3) = 207,495.7410562181`. With `u = 0` and therefore
`weight = 1`,

    claims_annuity(3) = 207,495.7410562181 × 0.0000002539279657861477 = 0.052689

Claim expense `= 30,000 × (0.0000002539279657861477 + 0 + 0) = 0.007618` — one event, the
certification; the first **annual** survival test is twelve months away.

`claims_death(3) = AV(3) × pols_death_act(3) = 13,369.256441 × 0.0000796748 = 1.065193`.
Expenses `= 200 × 0.9791306831539381 = 195.826137`. Premium
`= 5,600 × 0.9791306831539381 = 5,483.131826`.

`net_cf(3) = 5,483.131826 − 1.333122 − 0.052689 − 1.065193 − 195.826137 − 0.007618
= 5,284.847067`.

**Trace, month 12 — the 감액 expires and the renewal commission starts.** `age(12) = 41`,
policy year 2, so the rates move: `lapse_rate(12) = 0.06352246697177472` on the log-linear
path, and `red_factor(12) = 1.0`.

`n_C(12) = 0.0000001929 + 0.0000002672 = 0.00000046011303806134214`, so
`claims_lump(12) = 10,000,000 × 1.0 × 0.00000046011303806134214 = 4.601130` — a step of
`4.601130 / 2.198380 = 2.09` against month 11, of which a factor of `1/0.525 = 1.90` is the
감액 expiring and the rest is the rising certification rate.

`ann_pay(12)` sums the cohorts certified in months 3 through 12, each at **its own** frozen
amount and each with `u = 12 − s < 12`, so every weight is 1 (the guarantee):
`ann_pay(12) = 0.813192`. The cohorts of months 3–11 are still carried at
`A = 207,495.7410562181`; only the month-12 cohort is at `395,229.98296422494`. **That is the
freeze doing its work**, and it is the reason `claims_annuity` does not step at `t = 12` the
way `claims_lump` does.

Commission `= 0.03 × 5,146.951609 = 154.408548`. Expenses `= 200 × 1.02^1 × 0.9191015410
= 187.496714`. Claim expense `= 30,000 × 0.00000046011303806134214 = 0.013803` — still no
survival test, because the first cohort's first anniversary is month 15.

`net_cf(12) = 5,146.951609 − 4.601130 − 0.813192 − 4.308813 − 187.496714 − 0.013803
− 154.408548 = 4,795.309407`.

**Trace, month 240 — the surrender-value cliff.** `t = 240 = n_P`, so the premium stops and
the account crosses from its accumulation branch to its sourced run-off branch. The two meet
by construction:

    AV(240) = net_prem_ratio() × 5,600 × prem_accum_factor(240)
            = 0.7931662309087683 × 5,600 × 294.7175395152288 = 1,309,056.0000
            = av_ratio_at(0) × 5,600 × 240 = 0.974 × 1,344,000 = 1,309,056.0000

and `check_av_continuity()` asserts exactly that. The surrender value steps with it:
`cv_pp(239) = 0` and **`cv_pp(240) = 0.5 × 1,309,056 = 654,528.0000`**, which against
`cum_prem_pp(240) = 1,344,000` is a 환급률 of **48.700000%**, the published figure [S2]. That
is an **identity, not a check**: `av_table.csv`'s first anchor *is* that published 48.7%,
doubled, so what reproduces here is the arithmetic joining the two branches and nothing about
the basis.

Two things step at once and their product is the cliff. The lapse rate goes from
`lapse_rate(239) = 0.001` — the 납입완료 convergence point — to
`lapse_rate(240) = 0.008`, the post-완납 ultimate [REG-R27], so `pols_lapse` jumps from
`0.0000536909` to `0.0004306951`, a factor of eight. And the value paid on each of those
lapses jumps from nil to ₩654,528. So

    claims_lapse(239) = 0 × 0.0000536909            = 0.0000
    claims_lapse(240) = 654,528.0 × 0.0004306951    = 281.9020

and `net_cf` goes from **+2,496.2682** at `t = 239` to **−1,284.5196** at `t = 240`. **The
contract turns from a net income stream into a net outgo stream in one month**, and the
surrender-value form is a bigger part of that turn than the premium stopping.

### Milestone rows

To four decimal places. `claims_dementia` and `claims_maturity` are zero throughout.

| t | 만나이 | `pols_if` | `pols_act` | `pols_care` | `premiums` | `claims_lump` | `claims_annuity` | `claims_death` | `claims_lapse` | `expenses` | `claim_expenses` | `commissions` | `net_cf` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 12 | 41 | 0.9191 | 0.9191 | 0.0000 | 5146.9516 | 4.6011 | 0.8132 | 4.3088 | 0.0000 | 187.4967 | 0.0138 | 154.4085 | 4795.3094 |
| 120 | 50 | 0.6891 | 0.6889 | 0.0002 | 3857.6317 | 37.4014 | 80.2047 | 69.6691 | 0.0000 | 167.9928 | 0.5636 | 115.7290 | 3386.0712 |
| 239 | 59 | 0.6453 | 0.6442 | 0.0011 | 3607.7963 | 139.1227 | 361.8337 | 311.9062 | 0.0000 | 188.0242 | 2.4075 | 108.2339 | 2496.2682 |
| 240 | 60 | 0.6450 | 0.6439 | 0.0011 | 0.0000 | 101.8715 | 364.1340 | 342.5724 | 281.9020 | 191.6972 | 2.3426 | 0.0000 | -1284.5196 |
| 241 | 60 | 0.6443 | 0.6432 | 0.0011 | 0.0000 | 102.8477 | 366.4506 | 342.5552 | 281.8690 | 191.4910 | 2.3662 | 0.0000 | -1287.5797 |
| 300 | 65 | 0.6016 | 0.5999 | 0.0017 | 0.0000 | 124.6609 | 493.3706 | 534.0717 | 277.9321 | 197.3947 | 3.0831 | 0.0000 | -1630.5131 |
| 360 | 70 | 0.5513 | 0.5488 | 0.0025 | 0.0000 | 252.6475 | 651.6038 | 826.1459 | 268.1912 | 199.7145 | 4.3504 | 0.0000 | -2202.6533 |
| 480 | 80 | 0.4151 | 0.4096 | 0.0056 | 0.0000 | 771.8873 | 1656.5015 | 1546.9336 | 185.4590 | 183.3274 | 11.6465 | 0.0000 | -4355.7552 |
| 540 | 85 | 0.3212 | 0.3128 | 0.0084 | 0.0000 | 1681.5930 | 2788.4692 | 1004.5705 | 70.6471 | 156.5864 | 20.6729 | 0.0000 | -5722.5392 |
| 599 | 89 | 0.2120 | 0.2017 | 0.0103 | 0.0000 | 1844.5927 | 3756.1556 | 17.0540 | 0.7571 | 111.8860 | 24.9810 | 0.0000 | -5755.4264 |
| 600 | 90 | 0.2102 | 0.1999 | 0.0102 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

Rows `t = 299 → 300` and `t = 479 → 480` show the mortality table stepping at the
계약해당일: `claims_death` moves from 487.5506 to 534.0717 at 만나이 65 and from 1,412.0604
to 1,546.9336 at 80, because `q(x)` increments once a year and the account is large.
`claims_lump(240) = 101.8715` is **below** `claims_lump(239) = 139.1227` for a reason worth
naming: the 1·2등급 share `s_g2` is falling with age through this range — 0.1270 at 72 down
to 0.1110 at 82 — and the negative `s_G'` term of the product rule bites hardest where the
share is steepest. **The claim rate on a severe threshold does not rise monotonically with
age even though the all-grade certification rate does.**

`t = 600` is the 90세 계약해당일: `pols_if(600) = 0.2102` reaches it and is paid nothing.

### Undiscounted totals, `t = 0 … 600`

| column | total |
|---|---|
| `pols_if` | 343.1313 |
| `pols_act` | 341.3953 |
| `pols_healthy` | 330.6077 |
| `pols_light` | 10.7877 |
| `pols_care` | 1.7360 |
| `premiums` | **973533.0572** |
| `claims_lump` | **268065.6927** |
| `claims_annuity` | **546912.1402** |
| `claims_dementia` | 0.0000 |
| `claims_death` | **326783.9323** |
| `claims_lapse` | 70149.7799 |
| `claims_void` | 0.0073 |
| `claims_maturity` | 0.0000 |
| `expenses` | 135756.2503 |
| `claim_expenses` | 3774.5847 |
| `commissions` | 70945.8826 |
| `net_cf` | **-448855.2128** |

**Policy year 1 in aggregate** (`t = 0 … 11`, all at 만나이 40, all in policy year 1 — the
strongest single test target in this file, because it exercises the whole annual cycle on
one set of rates):

| line | policy year 1 total |
|---|---|
| `pols_if` | 11.548279 |
| `pols_act` | 11.548268 |
| `pols_light` | 0.000538 |
| `pols_care` | 0.000011 |
| `premiums` | 64670.302783 |
| `claims_lump` | 15.974040 |
| `claims_annuity` | 2.900270 |
| `claims_death` | 22.769436 |
| `claims_void` | 0.007271 |
| `expenses` | 31429.655856 |
| `claim_expenses` | 0.091280 |
| `commissions` | 43680.000000 |
| `net_cf` | **-10481.095370** |

(The totals are sums of unrounded monthly values; the thirteen displayed rows do not re-add
to them.)

**Decrement and state totals over the whole projection**, per policy issued:

| quantity | value |
|---|---|
| lives ever certified at the benefit grade, `Σ pols_entry_care` | **0.026808014544** |
| lives voided inside the 보장개시일 window, `Σ pols_void` | 0.000000626279 |
| cumulative deaths, `Σ pols_death` | 0.354308072159 |
| — of which not yet certified, `Σ pols_death_act` | 0.337733821029 |
| — of which in the care state, `Σ pols_death_care` | 0.016574251130 |
| cumulative lapses, `Σ pols_lapse` | 0.435534876925 |
| reaching the 90세 계약해당일, `pols_if(600)` | 0.210156424636 |
| 간병연금 instalments paid, `Σ ann_count` | 1.453879542900 |
| annual proof-of-life events, `Σ ann_tests` | 0.099011476675 |

### Present values at the 예정이율 of 2.0%

The model does not publish these; they are the calibration check that the premium, the
incidence basis and the expense basis are mutually consistent. `claims_dementia` and
`claims_maturity` are zero, so the nine lines re-add to `net_cf`.

| line | PV |
|---|---|
| `premiums` | 814356.0041 |
| `claims_lump` | 120884.7459 |
| `claims_annuity` | 253930.5911 |
| `claims_death` | 166819.3187 |
| `claims_lapse` | 38211.9050 |
| `claims_void` | 0.0073 |
| `expenses` | 97088.7515 |
| `claim_expenses` | 1746.6060 |
| `commissions` | 66187.8032 |
| `net_cf` | 69486.2754 |
| **PV(lump + annuity) / PV(premiums)** | **0.4602598067** |
| **PV(expenses + claim exp + commission) / PV(premiums)** | **0.2026425297** |

### What the numbers say

**This contract prefunds a cost that essentially does not arise until the block is old, and
then pays it out mostly as something other than the benefit it is sold for.** Year-1
benefit outgo is ₩18.87 against ₩64,670 of premium — **0.029%** — because the direct entry
rate at 만나이 40 is one in 450,000 a year and the progression rate applies to a light
compartment that barely exists yet. By 만나이 85 the all-grade certification prevalence is
20.5% and the model's own first-entry rate into 1·2등급 is 0.70% a year, a factor of 30 on
the age-65 rate. **39.1% of lifetime benefit outgo falls at attained age 85 or over and
63.3% at 80 or over** — and the 90세만기 truncates the exposure at exactly the band with the
highest certification rate of all. Over fifty years only **2.68%** of the cohort is ever
certified at the benefit grade, against 43.6% who lapse and 35.4% who die.

Three consequences follow, and they are what distinguishes this product from its Japanese
counterpart rather than from the chassis. First, **lapse and the interest rate, not the
incidence basis, are the dominant levers**: the lapse assumption removes 43.6% of the block
before the claims arrive, and on the level 표준형 comparison vector — 4.0% at every duration
against a log-linear path that falls to 0.1% — lifetime benefit outgo falls from ₩814,978 to
₩317,016, a **61% cut**, on a basis change the regulator explicitly polices [REG-R27]. It is
the right instinct for a supervisor to have had.

Second, **the 계약자적립액 is the third-largest cash flow in the statement**. `claims_death`
is ₩326,784 undiscounted, a third of premium income and larger than the lump sum, because
35.4% of the cohort dies before maturity with an account worth close to cumulative premiums.
This is not a death benefit and this contract has none; it is 감독규정 제7-63조제1항제1호 in
operation [REG-R17], and a reader arriving from a UK or US long-term-care model will not
expect it.

Third, **the 간병연금 is two thirds of the benefit** — ₩546,912 against ₩268,066 — even
though it is the optional rider and the lump sum is the main contract, and it is the reason
the post-onset survival basis matters here in a way it does not on the chassis. On a
lump-sum-only run of the same cell, undiscounted benefit outgo is ₩268,066 and `net_cf`
turns **positive** at +₩101,027. The whole of this contract's economic content sits in the
module whose central assumption — how long a Korean life survives after certification — is
the one thing nobody publishes.

---

## Valuation and reserve pointers

This library projects **gross, undiscounted** cash flows. Every valuation layer below
consumes them and is cited, never reproduced. Korea is the only market in this repository
running **three** of them over one stream at the same time, live rather than prospective.

- **K-IFRS 제1117호 (IFRS 17)**, mandatory for Korean insurers from **2023-01-01**
  [REG-R60]. The projected stream is the fulfilment cash flow before discounting and the
  risk adjustment; the CSM and its release pattern are out of scope. The **contract boundary
  question does not bite on this product** the way it does on `Medical_KR_S`, because the
  long-term-care benefit is written 비갱신형 on every retrieved document [S1] [S2].
- **The 계리가정 guidance reaches this model directly and by name.** The FSS's November 2024
  ruling on 무·저해지 lapse assumptions [REG-R27] is not background: it fixes the functional
  form of `lapse_rate(t)` and two of its three parameters, and 63.8% of Korean 보장성
  초회보험료 in 2024 H1 was written in a 무·저해지 form. The `pyojun` comparison vector is
  shipped because the guidance requires an insurer using anything other than the 원칙모형 to
  disclose the difference in CSM, best-estimate liability, K-ICS ratio and net income
  quarterly. **The instrument itself was not retrieved and the functional form is
  [unverified] at instrument level** [R14, secondary](#krlib-long_term_care-r14).
- **K-ICS**, in force from the same quarter [REG-R13], with the 경과조치 regime and the
  적기시정조치 thresholds of 제7-17조~제7-19조 [REG-R14]. `LTC_KR_S` computes no required
  capital. What it owes the regime is a projection **re-runnable on a re-set assumption
  basis at a stated 기준일**, which the `Projection` Space's scalar References provide. The
  **대량해지 shock of [별표 22]**, including the 고환급형 test, was **not retrieved** and
  anything resting on it is second-hand and [unverified] [REG-R26].
- **해약환급금준비금**, which has no counterpart anywhere else in this repository
  [REG-R11]. It is a distributable-earnings device sitting on top of the IFRS 17 balance
  sheet and it is **large on exactly this product shape**: a 미지급형 contract has a nil
  statutory surrender value for twenty years and a large one the day after, so the
  difference the reserve is measuring moves discontinuously at 납입완료. `av_pp` and `cv_pp`
  are published per policy so that the layer above can be built on them.
- **표준책임준비금 and 순보험료식 적립.** 보험업법 제120조 requires the 책임준비금
  [REG-R3]; 감독규정 제6-11조 and following set the accumulation [REG-R10]; 제7-64조 and
  제7-65조 govern the 산출방법서 and the 계약자적립액 [REG-R18]; 제7-66조 through 제7-70조
  govern the 해약환급금 and extend the regime to 제3보험 [REG-R19]. **One surrender-value
  regime governs all ten `krlib` products**, which is why this document inherits the
  chassis's rather than restating it. 보험업법 제181조 and 제184조 then put the basis and its
  verification inside the 선임계리사's statutory duty [REG-R5]; the tables here are a
  reference implementation's, not an appointed actuary's.
- **제3보험 design rules.** 감독규정 제7-63조 is the article that makes `claims_death` exist
  at all [REG-R17], and 보험업법 제4조제1항제3호 is what makes 간병보험 a 보험종목 in its own
  right rather than a species of 질병보험, writable by life and non-life carriers alike
  [REG-R1] [REG-R7] [R12] — which is why the five documents behind this composite come two
  from life carriers, two from non-life carriers and one from a state insurer outside
  보험업법 altogether.
- **Policyholder tax, not modelled.** Premiums fall in the **보장성보험료 세액공제** basket
  — a **12% credit** on up to ₩1,000,000 of annual premium, so at most ₩120,000 of relief
  [S1] [REG-R57], 15% under the 장애인전용보험전환특약 [S1] [S2]. **A credit, not a
  deduction**, which is the distinguishing feature of the Korean personal tax treatment
  throughout `krlib`: it is worth the same to a high-rate and a low-rate taxpayer, and worth
  more to the latter as a fraction of premium. The anchor's ₩67,200 annual premium is well
  inside the cap. Benefits are not projected net of policyholder tax. On insurer failure
  contracts are protected under 예금자보호법 to **₩100,000,000** from 2025-09-01, on the
  시행령 제18조 basis [REG-R32] [REG-R52].

---

## Key sensitivities and model risks

In rough order of leverage on this block. Every figure is a re-run of the shipped model on
the anchor cell with one thing changed, and says what was changed.

1. **The care-state mortality multiple, twice over.** `care_mort_mult` sets how long the
   annuity runs **and** it is the excess-mortality term of the incidence identity, so it
   moves entry and run-off in opposite directions at once. Setting it to **1.0** — the
   "there is no impaired-life table so leave it alone" choice — cuts lifetime lump-sum
   claims by **37.7%** (₩268,066 → ₩166,938) and annuity claims by **14.7%**, and cuts
   lives ever certified from 0.026808 to 0.016695. At **2.0** the cuts are 19.2% and 6.6%;
   at **4.0** lump-sum claims rise **20.1%** and annuity claims **5.6%** — note that even
   the annuity rises, because the extra entrants outweigh the shorter run-off at this
   multiple. There is no published table anywhere and the derivation behind 3.0 rests on a
   4-to-5.5-year duration bracket that is itself derived. **This is the model's largest
   quantified sensitivity.**
2. **The calibration gap against the disclosed 예정위험률.** The model's own first-entry
   rate is **24.0%** of the one disclosed Korean long-term-care incidence rate at 만나이 40,
   24.7% at 50 and 24.0% at 60 [S1] — the disclosed rate is about **4.2 times** the model's
   best estimate. Four biases all run the same way and none is quantified: a 예정위험률 is a
   loaded pricing rate; the conversion reads a cross-section as a cohort path in a scheme
   that grew 71.8% in six years; the care compartment leaves only by death when 9.2% of
   certifications came from a 등급변경신청; and the card is on 보험나이. **Scaling the
   model's basis up to the disclosed rate would multiply benefit outgo by roughly four and
   make the [S2]-derived premium impossible**, which is itself evidence that the disclosed
   rate is not a best estimate — but the gap is not closed here and it should not be treated
   as resolved.
3. **The 보험기간 truncation at 90.** Running the same cell to **100세만기** raises
   undiscounted lump-sum claims **70.6%** (₩268,066 → ₩457,418) and annuity claims **59.3%**
   (₩546,912 → ₩871,368), and PV benefit outgo at 2.0% by **46.9%**, taking
   PV(benefit)/PV(premium) from 0.4603 to **0.6762** on an unchanged premium. **95세만기**
   is +41.2% / +37.4%. The composite stops at 90 because that is the modal Korean maturity
   and the term of both published rate anchors [S1] [S2], but it truncates the exposure at
   the band with the highest certification rate of all — 41.7% at 85+, and still rising —
   and it is **materially conservative on claim cost**. This is the first sensitivity a user
   should run.
4. **Lapse, and note that its sign here is the opposite of the naive one.** Switching to the
   `pyojun` comparison vector — a **level 4.0%** at every duration, against a log-linear
   path from 8.0% falling to 0.1% at 납입완료 — cuts lifetime benefit outgo by **61.1%**
   (₩814,978 → ₩317,016) and turns `net_cf` from −₩448,855 to **+₩120,120**. The level
   vector looks lower than the first-year rate but is far higher *on average over fifty
   years*, so it removes most of the block before the claims arrive. **A model whose lapse
   assumption is described only by its first-year value cannot be read at all on this
   product.** Only the 8.0% first-year level is [std]; the shape and the two convergence
   points are the regulator's [REG-R27].
5. **`direct_entry_share` — timing, not level.** At **0.05** lifetime benefit outgo rises
   only 0.7% (₩814,978 → ₩821,073) and at **0.50** it falls 1.8%; but PV at 2.0% moves from
   0.4653 to 0.4485 of PV premium, and the *shape* of the run-off moves far more than the
   total. That is the expected behaviour of a parameter that reallocates one inflow between
   two routes with different delays, and it is why the closing assumption is defensible even
   though it is unsourced: **it is not carrying the level.**
6. **The prevalence ceiling matters less here than on the Japanese counterpart, and the
   reason is the term.** Refitting the male logistic through the same five sourced anchors
   at `prev_ceil` = 0.50 gives `(beta, x_mid) = (0.15902124, 87.333743)` and lifetime
   benefit outgo of ₩819,113 (+0.5%); at 0.35, `(0.17495141, 83.544175)` and ₩812,896
   (−0.3%); at 0.95, `(0.14221416, 94.063820)` and ₩812,401 (−0.3%). The total barely moves
   because a lower ceiling refits to a **steeper** beta and buys back before 85 what it
   gives up after, and because a 90세만기 contract never reaches the region where the
   ceilings differ. **On a 100세만기 or a 종신 variant this sensitivity would be first-order
   and it is not tested here.** Nothing above 만나이 88.5 is sourced.
7. **The grade share, and what "up to a factor of two" means.** Replacing the age-varying
   `s_g2` with the national all-ages figure of **0.1328** moves lifetime benefit outgo only
   +0.8%, but it moves the **split**: lump-sum claims −3.2% and annuity claims +2.7%, and it
   re-times both. The factor of two is a statement about the **rate at a given age** — 0.222
   below 65 against 0.111 at 80–84 — not about the anchor cell's lifetime total, and a
   product issued at 60 to a 1등급 threshold would feel it far more.
8. **The 감액기간, and why it is nearly worthless on this cell and not on others.** Setting
   `red_mths = 0` moves lifetime benefit outgo by **+0.010%** and `red_mths = 24` by
   **−0.023%**, because at issue age 40 almost nothing is certified in the first year or
   two. **It is not a negligible mechanic in general**: see the pitfall below on freezing it,
   where the same mis-modelling is worth 0.31% of annuity outgo at issue age 70 and 0.01% at
   40. A parameter that does nothing on the anchor cell can still be a first-order error at
   the top of the issue-age range, which is why the anchor cell is not the only test target.
9. **The 간편심사 loading is pure margin in this model.** Model point 8 carries
   `uw_loading = 1.40` on a premium already set at the risk level, and the model has **no
   separate incidence basis for the simplified-underwriting pool** because no retrieved
   source gives one. Its positive `net_cf` of +₩1,152,142 is an artefact of that and must be
   described as one. The true claim cost of a simplified pool on this trigger is
   **understated**, and one carrier's refusal to attach its 장기요양 riders to a simplified
   chassis at all [S1] is the market's own view of how much.
10. **Longevity, not mortality, is the tail risk.** On a living-benefit product longer
    survival means more entrants and more instalments. This model's healthy mortality is
    anchored on an **insured** 기대여명 [REG-R33] and is therefore lighter than the chassis's
    population anchor [REG-R38]; that is the right direction here, but the anchor is a single
    summary statistic per sex and the shape between the ages is a Makeham–Gompertz assumption
    with two [std] parameters.
11. **Basis-change risk the insurer does not control, and cannot price.** The grade
    thresholds, the scoring instrument and the very existence of the grades are set by
    대통령령 [REG-R55]. The 인지지원등급 was created out of nothing on 2018-01-01 [R6] and
    enlarged the covered population of every 「1~인지지원등급」 rider overnight at no
    additional premium. What the contracts carry against this is a **contract-continuity**
    clause [S3] and a successor-body definition [S4], **not a repricing right**. The
    asymmetry is unquantifiable, it has no counterpart in `jplib`, `frlib` or `uklib` whose
    triggers are contractual, and it is the reason a Korean insurer's real exposure on this
    product is wider than any sensitivity in this list.
12. **A stock that is still growing.** The certified population grew **71.8%** between 2018
    and 2024 while the 65+ population grew 36.6% [R4] [R16], so roughly half the growth is
    demographic and half is a rising rate — driven partly by the 2018 creation of
    인지지원등급 and partly by the scheme's continuing maturation. The stationary-population
    reading of the cross-section is therefore **known to understate entry**, and the model
    does not project the trend.

### Known modeling pitfalls

Each of these is a mistake a modeller would actually make on this product, and each is
stated so that it can be checked.

- **인정률 is a prevalence, not an incidence — and the ratio is not a constant.** 10.85% of
  the 65+ population held a certification at end-2024 [R4]; 1·2등급 prevalence at 만나이 65
  is 0.246%. The model's own first-entry rate at the same age is **0.02343%**, so the
  prevalence is **10.5 times** the incidence at 65, **6.5 times** at 75 and **3.8 times** at
  85. Multiplying an 인정률 by a benefit amount, or treating it as an annual claim
  frequency, is the single commonest error in a Korean long-term-care model, and using one
  ratio to convert it at every age is the second commonest.
- **The excess-mortality term of the identity is not a refinement, and neither is
  `mu_bar`.** Setting `care_mort_mult = 1` drops the term entirely and cuts lifetime
  lump-sum claims by **37.7%**. Keeping `mu_C` but dropping `mu_bar` — using
  `P_C × mu_C` instead of `P_C × (mu_C − mu_bar)` — goes the other way and inflates the
  inflow at 만나이 65 by **8.2%**. Prevalence is a proportion of a *living* population, so
  the comparison is against the population's own average force, not against zero.
- **Take `P_C'` by the full product rule.** `P_C = s_G(x) P(x)` and `s_G` is **falling with
  age** over most of the range for a severe threshold. Dropping the `s_G'(x) P(x)` term
  leaves `s_G(x) P'(x)`, which at 만나이 65 is **1.82×** the correct `P_C'` and at 75 is
  1.19×. The visible symptom is that `claims_lump` rises monotonically with age, whereas the
  shipped model has it **falling** between `t = 239` and `t = 240` (139.1227 → 101.8715).
- **The 감액 is frozen at first certification and must not be re-tested at each instalment.**
  「최초 진단 확정일을 기준으로 … 그 이후에 도래하는 매년 진단 확정일이 계약일부터 2년이상에
  해당하더라도 … 지급액은 변경되지 않습니다」 [S1]. A model that re-tests it pays the full
  amount from month 12 onward to cohorts certified in the first year, **overstating** annuity
  outgo by **₩64.78** on the anchor cell (+0.012%), by **₩596.60** at issue age 60 (+0.097%)
  and by **₩1,065.24** at issue age 70 (+0.315%). Evaluate `red_factor` at `s`, never at
  `t`.
- **The annuity's first instalment falls in the month of certification.** The `u = 0` term
  of `ann_count(t)` is `n_C(t)` itself [S1]. Deferring it by twelve months removes roughly a
  tenth of the annuity liability and misdates all of it. Related and opposite: the
  instalments are **monthly** while the survival test is **annual**, so a model that pays
  annually gets the amount right and the timing wrong, and a model that tests survival
  monthly gets the timing right and the amount wrong.
- **The claim expense is per event, not per instalment.** The proof of life the 약관 requires
  is annual — 「매년 진단 확정일에 피보험자의 주민등록등본을 제출하여야 합니다」 [S1] — so
  `ann_tests` totals **0.0990** over the projection against `ann_count`'s **1.4539**.
  Charging ₩30,000 per monthly instalment would multiply the annuity's claim expense by
  about fifteen.
- **Compute `care_surv` as a partial product, never as a ratio of cumulative products.**
  `mort_rate_care` is capped at 1 and the cap binds from 만나이 **108** on the shipped male
  table and **112** on the female one, so a cumulative product underflows to zero from there
  on and the ratio form divides by zero exactly where the tail of a 종신 variant lives. It
  does not bite on any shipped model point, which is precisely why it would be found late.
- **Premium rides on `pols_act`, never on `pols_if`.** Charging the whole in-force block
  overstates lifetime premium income by **₩414.65** on the anchor cell, 0.043% — small
  because the certification rate at issue age 40 is small, and much larger at the top of the
  issue-age range. Note that the error here is the *reverse* of the Japanese product's,
  where the waiver fires below the benefit and the band is large: here `G_W = G_B`, so the
  only lives on waiver are lives already claiming.
- **Do not apply lapse to the care compartment, and know that the check will not catch
  you.** The premium is waived [S3] and the 약관 bars surrender [S1]. Applying the lapse
  rate to `pols_care` as well leaves `claims_annuity` **completely unchanged** at
  ₩546,912.14 — the ledger is driven by `n_C` and `care_surv`, not by the compartment — and
  `check_pols_roll_fwd()` still closes, because the roll-forward is consistent. The only
  visible effect is **₩489.73** of extra `claims_lapse`, a surrender value paid to lives the
  contract forbids from surrendering. It is a silent error and the reason `cv_pp` and
  `pols_lapse` should be read together.
- **A certification inside the 보장개시일 window is a decrement, not a deferred claim.**
  「특약을 무효로 하며, 이미 납입한 보험료를 돌려드립니다」 [S1] [S2]. The life leaves the
  model with a refund; it does not sit in the block waiting for the window to close. And
  there is **no cancellation option and no revival** here, unlike the cancer chassis, so a
  model that imports the chassis's 90-day cancellation right invents a term this product
  does not have. And **the refund is `cum_prem_pp(t + 1)`, not `cum_prem_pp(t)`**: premium
  falls at the start of month `t` and the void at the end of it, so a life voided in month 0
  has paid one month and gets it back. `claims_void(0)` is ₩0.001040 and `claims_void(3)` is
  nil — for opposite reasons, the second because the window has closed.
- **The surrender-value cliff has a direction, and three of the four Korean forms differ
  only in which side of 납입완료 the 50% attaches to.** 미지급형 is nil **during** and 50%
  of a notional 기본형 **after** [S2]; 납입중50%해약환급금지급형 is 50% during and 100%
  after [S4]; 표준형 pays the full account less the 해약공제액 from year 1 [S1]. Getting the
  side wrong inverts the whole cash-flow shape and is not caught by any total.
  `check_cv_form()` asserts `cv_pp(t) = 0` **identically** for `t < n_P` on the 미지급형
  form, with its sign, for exactly this reason.
- **`claims_death` is not a death benefit.** This contract has none [S1] [S3]. It is the
  **계약자적립액** that 감독규정 제7-63조제1항제1호 makes payable on a death from a cause the
  contract does not cover [REG-R17], and at ₩326,784 undiscounted it is a third of premium
  income and larger than the lump sum. Reading it as a sum assured, or dropping it because
  "this is a pure protection contract", are both wrong and in opposite directions. And
  **deaths in the care state pay nothing** — 「지급사유가 발생한 후 사망한 경우에는 별도로
  책임준비금을 지급하지 않습니다」 [S1] — which is why `pols_death` is split; on the anchor
  cell 0.0166 of the 0.3543 cumulative deaths pay nothing.
- **The light compartment pays premium and lapses; the care compartment does neither.**
  Collapsing the two into one "certified" state either stops a premium the contract goes on
  charging or invents a benefit at a grade it does not cover, and — the larger error — turns
  the 1·2등급 rate into a healthy-life incidence. On the shipped basis progression overtakes
  direct entry by policy month 8 at issue age 40, and above 65 it is 80% of gross inflow by
  construction. A single-decrement model puts the cash flow **years too early**.
- **`prog_rate_at` is not scaled below 65 and that is deliberate.** `sub65_factor_at`
  applies to `i_D` and `i_L`, which are rates of *entering* the scheme through a gate the
  statute narrows below 65; `rho` is a property of a life **already certified**, and a life
  certified at 만나이 50 got there through the 노인성 질병 list and is, if anything, more
  likely to progress than a 70-year-old. `rho(40) = 0.0340` is therefore **higher** than
  `rho(65) = 0.0153`, which looks wrong on a decrement table and is right here.
- **Widening the threshold is not a re-scaling.** Moving `benefit_grade` from `g2` to `g5`
  on the anchor cell takes lifetime benefit outgo from ₩814,978 to ₩1,978,328 — a factor of
  **2.43** — and PV(benefit)/PV(premium) from 0.4603 to **1.1233**, on an unchanged premium.
  Moving it to `g1` gives 0.1997. The exposure changes in **frequency and in timing
  together**, because the light compartment shrinks as the gate widens and vanishes entirely
  at `g6`. Treating the threshold as a multiplier on one incidence rate is the error the
  market itself prices against at about 4.5 : 1 [S2, derived].
- **The two modules run in opposite sex directions and the model does not reproduce that.**
  장기요양 covers are dearer for women at every age (여/남 = 1.52 at 40 on the main contract)
  and 치매 covers are **cheaper** (0.80 on 경도이상치매), in the same document [S2, derived].
  The certification basis reproduces the first through the sourced prevalence; the dementia
  basis applies a **flat-in-age** sex factor [R7] and therefore does **not** reproduce the
  second. A user who switches the rider on and reads the sex differential off the output is
  reading an artefact of that simplification.
- **The care state is absorbing because the *contract* makes it so, not because the state
  is.** Grades move both ways — 107,365 of 1,165,030 current certifications came from a
  등급변경신청 [R4 표2-5](#krlib-long_term_care-r4) and one carrier drafts a rider around exactly that [S3] — but the
  amount is frozen at first certification, the instalments are metered on **survival**
  rather than on continued certification, and surrender is barred [S1]. So the simplification
  is smaller here than it looks. **It would not be available at all** for the
  utilisation-conditioned 지원금 form [S2], which requires the insured to be *using* a named
  public benefit in the month; a model that ported this chassis to that product without a
  utilisation and recovery basis would be materially wrong.
- **Do not read the disclosed 예정위험률 as a level.** It is used here for its **gradient
  below 65 and its sex ratio**, and `disclosed_inc_ratio_at` publishes the gap rather than
  hiding it. Substituting it as the model's incidence would multiply benefit outgo by
  roughly four and contradict the premium it was quoted alongside.
- **`proj_len()` is a row count, not the last index.** `result_cf()` has `proj_len() = 601`
  rows indexed `t = 0 … 600`, and the last of them is the 90세 계약해당일: an in-force count
  of 0.2102 and **every cash flow zero**. The frame is `range(proj_len())` and the maturity
  row is `t = proj_len() − 1`, which is why the cash-flow cells guard on
  `t >= proj_len() - 1` while the in-force counts guard on `t >= proj_len()`. Writing the
  cash-flow guard as `t >= proj_len()` would put outgo on the maturity row; writing the
  count guard as `t >= proj_len() - 1` would drop the row the roll-forward closes on and
  break `check_pols_roll_fwd()` at the last step.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #krlib-long_term_care-r10
[R11]: #krlib-long_term_care-r11
[R12]: #krlib-long_term_care-r12
[R16]: #krlib-long_term_care-r16
[R18]: #krlib-long_term_care-r18
[R2]: #krlib-long_term_care-r2
[R3]: #krlib-long_term_care-r3
[R4]: #krlib-long_term_care-r4
[R6]: #krlib-long_term_care-r6
[R7]: #krlib-long_term_care-r7
[R8]: #krlib-long_term_care-r8
[REG-R1]: #krlib-reg-r1
[REG-R10]: #krlib-reg-r10
[REG-R11]: #krlib-reg-r11
[REG-R12]: #krlib-reg-r12
[REG-R13]: #krlib-reg-r13
[REG-R14]: #krlib-reg-r14
[REG-R17]: #krlib-reg-r17
[REG-R18]: #krlib-reg-r18
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R21]: #krlib-reg-r21
[REG-R22]: #krlib-reg-r22
[REG-R25]: #krlib-reg-r25
[REG-R26]: #krlib-reg-r26
[REG-R27]: #krlib-reg-r27
[REG-R28]: #krlib-reg-r28
[REG-R29]: #krlib-reg-r29
[REG-R3]: #krlib-reg-r3
[REG-R32]: #krlib-reg-r32
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R38]: #krlib-reg-r38
[REG-R39]: #krlib-reg-r39
[REG-R48]: #krlib-reg-r48
[REG-R5]: #krlib-reg-r5
[REG-R51]: #krlib-reg-r51
[REG-R52]: #krlib-reg-r52
[REG-R55]: #krlib-reg-r55
[REG-R57]: #krlib-reg-r57
[REG-R60]: #krlib-reg-r60
[REG-R61]: #krlib-reg-r61
[REG-R7]: #krlib-reg-r7
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
