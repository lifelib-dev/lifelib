# Technical Notes

**Status:** Draft, 2026-09-03 (all cited sources accessed 2026-09-03).

**Scope note.** These notes turn the standardized composite cancer insurance (*am boheom*,
암보험) of `product-spec.md` (same directory) into a reference liability cash-flow
projection on paper, and then into `Cancer_KR_S` beside it. **They describe no single
insurer's contract.** [S#] and [R#] tags resolve against `sources.md`, whose numbering is
carried verbatim from `_research/cancer.md` and is frozen; [REG-R#] tags resolve against
the cross-product reference library `references/regulatory-and-actuarial-references.md`,
whose own R-numbering is separate and also frozen. **[std]** marks a standardization
introduced for the reference implementation, always with a rationale and, where one exists,
the observed range; [unverified] marks a claim that could not be confirmed against a
retrieved document. **Every parameter value here is identical to `product-spec.md`'s**, and
**every number in the worked example is read off the shipped model** rather than recomputed
by hand.

Nine **assumption inputs** appear here that `product-spec.md` does not carry, because they
are modelling constructs rather than contractual terms, and each is introduced below as
such: the **tier decomposition** of the published incidence grid into 일반암, 특정소액암,
고액암 and 유사암; the **post-diagnosis excess hazard** in its six select-duration bands;
the **admission frequency** and mean stay of a diagnosed life; the **operation frequency**,
split 관혈 / 비관혈; the **first-treatment hazard** that makes the 최초 1회한 treatment
benefit finite; the **lapse** level; the **expense** and **commission** scales; the
**gross-to-net premium loading** that drives the 계약자적립액; and the **notional
보험가입금액** that enters the 표준해약공제액 formula for a product with no face amount.

**This is the library's fixed-benefit (정액) 제3보험 chassis.** Five mechanics are
specified once, here, and inherited rather than restated:

- the **diagnosis-triggered lump sum** graded by a **tier ladder** — 고액암 above, 일반암
  in the middle, 특정소액암 and 유사암 below — where the tier is decided by a public
  statistical classification incorporated by reference [S3] [S4];
- the **90일 면책기간** before invasive cover attaches, and the fact that the 유사암 tier
  is carved out of it, so the benefit vector has **two start dates and not one** [S1] [S2];
- the **감액기간**, a stated fraction of the benefit for the first one or two years, sitting
  on top of the waiting period as a second, softer anti-selection device [S1] [S6];
- the **유사암 reduced tier**, at a stated fraction of the general-tier amount, which is what
  lets a product cover a fast-growing, high-survival decrement without repricing [S3] [S4];
- a **post-diagnosis survival model**, because a cancer contract goes on paying after the
  diagnosis benefit and an incidence rate alone cannot say for how long.

The [long-term care technical notes (간병보험)](../long_term_care/technical-notes.md) and
the [children's insurance technical notes (어린이보험)](../child/technical-notes.md) state
their deltas against this document rather than restating its machinery. `LTC_KR_S` replaces
the KCD-keyed diagnosis trigger with a **statutory** one, the 노인장기요양보험 등급
[REG-R54] [REG-R55], and the lump sum with a continuing annuity, so its post-onset survival
model is the whole product rather than a correction to it. `Child_KR_S` inherits the tier
ladder and the 감액기간 but **disapplies the 면책기간** below 보험나이 15 [S2] [R3] [R6].
The [indemnity medical technical notes (실손의료보험)](../indemnity_medical/technical-notes.md)
share nothing with this chassis but the 제3보험 statutory class: `Medical_KR_S` is the
library's only indemnity product and carries the 급여/비급여 split, 자기부담금, annual
limits and 재가입 that this one deliberately does not.

**Deltas against the protection chassis.** The [term life technical notes
(정기보험)](../term_life/technical-notes.md) carry the decrement and premium recursion and
the 갱신형 / 비갱신형 split; the [whole life technical notes
(종신보험)](../whole_life/technical-notes.md) carry the 계약자적립액, the 해약환급금 and the
무해지 / 저해지 cliff, and this document uses that surrender-value regime unchanged, because
감독규정 제7-69조 and 제7-70조 apply 제7-65조 through 제7-68조 to 장기손해보험 and to
제3보험 *mutatis mutandis* — **one surrender-value regime governs all ten `krlib` products**
[REG-R19]. What changes here, and changes the *shape* of the model rather than a parameter
in it:

1. **A three-state model, not a one-state model.** `Term_KR_S` projects a single in-force
   population and reads a death rate off it. A cancer model cannot: the premium waiver, the
   inpatient, surgery and treatment limbs and the 계약자적립액 payable on a later death all
   run on **how long the insured lives after diagnosis**, and the 특정소액암 tier does not
   stop the premium while the 일반암 tier does. This model therefore carries a
   never-invasively-diagnosed state, a 특정소액암 state that still pays premium, and a
   waived 일반암 state that does not — and it needs a **survival model as well as an
   incidence model**.
2. **The premium waiver is correlated with the insured event**, not independent of it. It
   fires on the same first invasive diagnosis that pays the lump sum [S3 제14조제1항]
   [S1 제9조제1항], so the premium stream is carried by `pols_healthy + pols_minor` and the
   benefits by the diagnosed states, and the two weights are **disjoint by construction**.
3. **Two waiting periods, not one.** The invasive tiers attach at `t = 3`; the 유사암 tier
   attaches at `t = 0` [S1] [S2]. Reading one `wait_months` off the model point and applying
   it to both tiers is the commonest way to break this product.
4. **A payment on death with no death benefit.** The composite has no death cover at all,
   and 감독규정 제7-63조제1항제1호 nevertheless requires a 제3보험 product to pay the
   **계약자적립액** on a death from a cause the policy does not cover [REG-R17] [REG-R25
   제22조](#krlib-reg-r25) [REG-R50 제736조](#krlib-reg-r50). So `claims_death` exists, is small, and is a *return of
   account* rather than a benefit.
5. **Paying a benefit neither terminates nor exhausts the contract** [S1] [S3] [S4]. There
   is no benefit-driven termination anywhere in this product, and nothing is paid at the
   100세 계약해당일.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows** for a single-policy
  model point of 암보험: office premiums; the four diagnosis lump sums (일반암, the 고액암
  top-up, 특정소액암, 유사암); the 암 직접치료 입원급여금, the 암 수술급여금 and the
  항암약물·방사선 치료급여금; the 계약자적립액 paid on death and the 해약환급금 paid on
  surrender; maintenance and claim-handling expense; and commission. Undiscounted and gross
  of reinsurance. Korea runs **three** measurement bases over one such stream and all three
  are live: IFRS 17 (K-IFRS 제1117호, mandatory since 2023-01-01) [REG-R60], K-ICS from the
  same quarter [REG-R13], and the **해약환급금준비금**, which has no counterpart anywhere
  else in this repository [REG-R11]. **Discounting, the risk adjustment, the CSM, 요구자본
  and every reserve are out of scope** and are cited, not reproduced — see *Valuation and
  reserve pointers*.
- **Projection frequency.** **Monthly grid**, and monthly by construction rather than by
  approximation. Three of the product's mechanics live on it: 월납 is the dominant retail
  mode, the only mode at one direct writer [S8], and the mode named in the 감독규정's own
  기준연령 요건 [REG-R9]; the 90-day 면책기간 lands on the grid boundary `t = 3`; and the
  one-year 감액기간 lands on `t = 12`. `t` is the **policy month** and it is **0-based**: the
  first projected month is `t = 0`, month `t` is the interval from `t` to `t + 1` months after
  the 보험계약일, the frame is `t = 0, 1, …, proj_len − 1`, and the policy year is the
  contractual 1-based label `y(t) = floor(t / 12) + 1`.
- **`proj_len()` is the number of projected months — the frame's exclusive end, not the last
  index.** `proj_len = 12 × (expiry_age − issue_age) + 1`, so **721** on the anchor cell and
  **721 rows** in `result_cf()`, indexed `t = 0 … 720`. The `+ 1` is the terminal row: the 720
  months of cover are `t = 0 … 719` and month `t = proj_len − 1` is the 100세 계약해당일
  itself. Every cash flow in it is zero, `pols_maturity` records the cover ending, and
  `claims(t, "MATURITY")` is **0.00** — there is no 만기환급금 on the 순수보장형 form and the only
  retrieved surrender-value illustration shows the value returning to nil at maturity [S8].
- **The waiting period lands on a grid boundary.** The 암보장개시일 is the 91st day counting
  the 보험계약일 as day 1 [S1] [S2] [S3] [S4] [S7], with the 약관's own worked example
  보험계약일 2014-04-10 ⇒ 보장개시일 2014-07-09 [S1]. On a monthly grid that is three
  months, `t = 3` **[std]**, and the model claims no finer precision. A daily implementation
  must separate the two wordings; `product-spec.md` footnote 16 records them.
- **Timing conventions [std].** Office premium received at the **start** of month `t`;
  maintenance expense at the start of month `t`; every diagnosis, every benefit and the
  claim-handling expense at the **end** of month `t`; decrements at the end of month `t`, in
  the order **transition, mortality, lapse**. Acquisition expense and initial commission at
  `t = 0`.
- **Episode convention [std].** A diagnosis arising in month `t` pays its lump sum in month
  `t`, and the diagnosed life is exposed to its **new** state's decrements for the rest of
  that month — that is what `pols_waived_exp` and `pols_minor_exp` are — but enters the
  diagnosed *stock* at the start of `t + 1`. So the inpatient, surgery and treatment
  benefits that follow a diagnosis begin at `t + 1`, and on the anchor cell **`t = 4` is the
  first month with any care benefit at all**. The one-month lag is a timing effect on an
  undiscounted projection; the alternative — recognising a treatment episode in the
  diagnosis month — is named in the pitfalls list.
- **Age basis.** **만나이** (*man nai*, age last birthday), incremented on the policy month
  grid: `age(t) = x + floor(t / 12)`, `x` the model point's `issue_age`. The contract itself
  ages on **보험나이** (*boheom nai*, insurance age): 「계약일 현재 피보험자의 실제 만
  나이를 기준으로 6개월 미만의 끝수는 버리고 6개월 이상의 끝수는 1년으로 하여 계산」,
  incrementing at each 계약해당일 [S3] [REG-R25 제21조](#krlib-reg-r25). The model uses 만나이 because
  **every decrement it reads is published on 만나이** — the 국가암등록통계 age bands [R1],
  the 보험개발원 참조순보험요율 grid [R5] [REG-R61] and the 국가데이터처 생명표 [REG-R38] —
  and converting a public 만나이 rate onto a 보험나이 basis needs a distribution of issue
  dates within the policy year that no source supplies. Because of the six-month rule the
  two differ for roughly **half of all issue dates**, so the model reads its tables for a
  life on average half a year younger than the contract calls him. The offset is **[std]**
  and it is not negligible on the steep part of the curve: between 60 and 70 the published
  male rate roughly doubles [R5], so half a year of age is worth about **3.5%** of the rate.
  The direction is stated: it **understates**.
- **Currency.** KRW throughout. There is no minor unit in the contract, but expected values
  are fractional; displayed to the precision each table states.
- **Model points.** One policy at a time, projected on an expected (probability-weighted)
  basis. `Projection` is parameterized by `point_id`; no aggregation logic is specified here.
  Ten points are shipped and every one of them satisfies every `check_*()` cells.
- **Termination.** Cover to the **100세 계약해당일**, `t = proj_len − 1`. The decrements are
  death and lapse and nothing else: **there is no benefit-driven termination**. Payment of a
  diagnosis benefit neither terminates nor exhausts the contract [S1] [S3] [S4], the
  once-only flags exhaust a *tier* and not the policy, and the 180-day inpatient cap is a cap
  on a **stay** and not on the contract.
- **Contract boundary.** On the 비갱신형 chassis the premium is level and 무배당 with no
  insurer repricing right [S3] [S5] [REG-R12], so every future premium and benefit is inside
  the boundary and the horizon is the whole term. On the **10년 갱신형** flag the renewal
  reprices at the attained age on the rate basis then in force [S4 제2-11조의6], which would
  ordinarily close the boundary at each renewal; `krlib` projects that flag to final expiry
  and **records the tension rather than resolving it**, which is a K-IFRS 1117 question
  [REG-R60] this model does not answer. Exactly as `Term_KR_S` and `Medical_KR_S` do.
- **Rounding.** Intermediates at full double precision. The worked example displays policy
  counts to ten decimals and cash flows to ten decimals in the first-year table, six in the
  milestone table and four in the aggregates. **Monthly rows rounded for display do not
  re-add to the displayed totals**; the totals are sums of unrounded values.
- **What this model is not.** It is a **mechanics demonstration**. The premium is a model
  point input, the expense and commission scales are [std], and the care intensities are the
  weakest file in the model. Replace the assumption tables with company data before drawing
  any conclusion from the output.

---

## Model point attributes

| Attribute | Type | Anchor cell (`point_id = 1`) |
|---|---|---|
| `policy_id` | str | KR-CA-0001 |
| `sex` | enum {M, F} | M |
| `issue_age` (`x`) | int, **만나이**, 15–65 | 40 |
| `expiry_age` | int, 만기나이 | 100 |
| `pay_term_y` | int years, `0` = 전기납 | 20 |
| `sum_assured` (`S`) | 보험가입금액, KRW | 30,000,000 (3천만원) |
| `premium` (`P`) | KRW per month, office premium, **model-point input** | 45,000 **[std]** |
| `chassis` | enum {bi_gaengsin, gaengsin} | bi_gaengsin (비갱신형) |
| `wait_months` (`W`) | int months, 면책기간 on the grid | 3 |
| `reduction_months` (`G`) | int months, 감액기간 ∈ {0, 12, 24} | 12 |
| `similar_ratio` | 유사암 fraction of `S` ∈ {0.10, 0.20, 0.70} | 0.20 |
| `hosp_module` | 0/1 — 암 직접치료 입원급여금 | 1 |
| `surg_module` | 0/1 — 암 수술급여금 | 1 |
| `treat_module` | 0/1 — 항암약물·방사선 치료급여금 | 1 |
| `diag_module` | 0/1 — the four diagnosis lump sums | 1 |
| `waiver_trigger` | enum {cancer_diag, none} | cancer_diag |
| `cv_form` | enum {mijigeup, pyojun} | mijigeup (해약환급금 미지급형) |

Derived scalars on the anchor cell, all read off the model: `proj_len() = 721`,
`pay_months() = 240`, `pols_if_init() = 1.0`, `surr_chg_months() = 84` and
**`surr_chg_cap_pp() = 585,000`**.

**`premium` is an input, not a computed quantity**, and on this product that is a stronger
statement than on any other in the library. No Korean carrier publishes a rate table for a
cancer main contract; the 산출방법서 is a 기초서류 filed with the FSC and not a public
document [REG-R2]; and the 참조순보험요율 reaches the public only as the **보험가격지수**
ratio, 보험료총액 ÷ (참조순보험료 총액 + 보험회사 평균사업비총액) [REG-R22]. The only
retrieved premium figures — ₩119,280, ₩187,332 and ₩347,292 a year at 남자 40세 / 월납 /
10년납 10년만기 / 순수보장형 [S8] — come with **no stated 보험가입금액**, so they are price
points without a benefit denominator. `product-spec.md` footnote 11 reaches ₩45,000 by
arithmetic and states that these notes' figure governs where the two differ. **On the shipped
basis the equivalence premium is ₩66,289 a month**, solved in the worked example; ₩45,000
is 32% below it, and the visible consequence is that the anchor cell is the one model point
whose retrospective 계약자적립액 is exhausted before expiry.

The **modules are independently switchable** and that is a specification requirement, not a
convenience: the retrieved market contains a diagnosis-only shape in three tiers [S6] [S7]
or five [S3], a twenty-three-module product [S4], a diagnosis-plus-twenty-riders non-life
contract [S1] [S2], and a **treatment-cost-only contract with no diagnosis lump sum at all**
[S5]. Model point 8 is that last shape with `diag_module = 0`; model point 7 is the
diagnosis-only shape. They are configurations of one model, not different models.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `pols_healthy(t)` | In force at the start of month `t` and **never diagnosed with an invasive cancer**; `pols_healthy(0) = pols_if_init()` | monthly recursion |
| `pols_minor_dur(t, k)` | In force, first invasive diagnosis was a **특정소액암**, elapsed duration cohort `k = 1 … 6` | monthly recursion |
| `pols_waived_dur(t, k)` | In force, has had a **일반암 or 고액암**, premium waived, cohort `k = 1 … 6` | monthly recursion |
| `pols_minor(t)`, `pols_waived(t)` | Σ over the six cohorts | derived |
| `pols_cancer(t)` | `pols_minor(t) + pols_waived(t)` — the diagnosed in-force population | derived |
| `pols_if(t)` | `pols_healthy(t) + pols_cancer(t)` — total in force at the start of `t` | derived |
| `pols_payer(t)` | The population still paying premium: `pols_healthy + pols_minor` under the waiver, `pols_if` without it | derived |
| `similar_avail(t)` | Probability, per policy, that the 유사암 tier is still unused; `similar_avail(0) = 1` | monthly |
| `treat_avail(k)` | Probability that the **최초 1회한** treatment benefit is still unused at cohort `k` | select-year lookup |
| `av_pp(t)` | **계약자적립액** per policy in force, floored at zero | monthly recursion |
| `cv_std_pp(t)`, `cv_pp(t)` | 표준형 해약환급금; the 미지급형 value actually paid | derived |
| `age(t)` | Attained **만나이** = `x + floor(t / 12)` | annually |
| `mort_rate_mth(t)` | Monthly base mortality, never-diagnosed | lookup |
| `mort_rate_waived_mth(t, k)`, `mort_rate_minor_mth(t, k)` | Monthly mortality of the two diagnosed states, base plus that cohort's excess hazard | derived |
| `lapse_rate_mth(t)` | Monthly lapse on the premium-paying states | lookup |
| `lapse_rate_canc_mth(t)` | Monthly lapse on the waived state — **identically zero** under the waiver | derived |
| `inc_rate(t)` | Annual 암 발생률 excluding C44 and C73, the sourced base rate | lookup |
| `net_cf(t)` | Net cash flow of month `t`, insurer perspective, **income-positive** | monthly |

**Why three states and not two.** The two diagnosed states are not a refinement; they are
what the waiver clause says. The composite waives the premium on 「'암(직·결장암, 유방암,
여성생식기암, 전립선암, 기타피부암, 갑상선암, 대장점막내암 제외)' 또는 '중증 갑상선암'」 and
states in terms that 특정소액암 and every 유사암 member other than 중증 갑상선암 do **not**
waive [S3 제14조제1항] [S1 제9조제1항]. So a 특정소액암 life is diagnosed — it draws every
care benefit, and it carries excess mortality — and it **keeps paying premium and can still
lapse**. Collapsing the two into one diagnosed state either stops a premium the contract goes
on charging or charges one it has waived, and the error is not small: at `t = 240` the
특정소액암 state is **0.0127869424** against the waived state's **0.0265665643**, a third of
the diagnosed population.

**A 특정소액암 life can go on to a 일반암, and that transition is modelled.** It appears as
the `(1 − i_g · cover)` factor inside `surv_minor` and as the second limb of `diag_gen`; on
the anchor cell it is tiny at outset — `diag_gen_m(3) = 0.00000000182660` against
`diag_gen_h(3) = 0.00009067247589` — and grows with the 특정소액암 stock. **The reverse is
not modelled**: a 일반암 life's later 특정소액암, and a 고액암 after a plain 일반암, are
**[std] omissions** and both **understate**.

**The 유사암 tier is emphatically not a fourth state.** It is a second benefit at a second
rate on its own once-only ledger. It does not move the life anywhere, it does not stop the
premium, it does not start any clock, and it carries **no excess mortality at all** —
갑상선 five-year relative survival is **100.2%**, statistically indistinguishable from the
general population, on a lifetime 갑상선 mortality risk of **0.1%** [R1]. It appears in no
row of `survival_table.csv`, by design. Implementing it as a discount on the main diagnosis
benefit gets the amount right and the ledger, the waiver and the waiting period all wrong.

**Six select-duration cohorts, and why a flat hazard will not do.** Relative survival is
steeply select: most of the excess mortality of a cancer diagnosis falls in the first two
years, and **62.1%** of Korea's prevalent cancer population — 1,697,799 of 2,732,906 — is
more than five years out from diagnosis [R1]. A flat hazard fitted to the five-year point
kills long survivors far too fast, and long survivors are exactly who the inpatient, surgery
and treatment limbs are paid for. Each diagnosed state is therefore resolved into **six
cohorts** — select years 1 to 5 and an ultimate — and the excess hazard is read per cohort.
The cohorts are tracked **exactly, as a delay on the entry flow** rather than as a transfer
rate: `waived_grad(t, 1)` and `minor_grad(t, 1)` carry the entrants of month `t − 13`
forward on cohort 1's own decrements — thirteen, not twelve, because the entry month is
itself a full month of cohort-1 exposure — and each later cohort hands on to the next twelve
months after that. The graduation flows telescope out of the state totals.

**Two ledgers, and they are per policy, not per block.** `similar_avail(t)` is the
probability that an individual policy's 유사암 tier is still unused; `treat_avail(k)` is the
probability that an individual diagnosed life's **최초 1회한** treatment benefit is still
unused at select year `k`. Neither is weighted by a population count, and weighting either
one by `pols_if` or `pols_cancer` measures the block's consumption rather than the
individual's and defers the exhaustion forever.

**Three absences are product facts, not gaps.** There is **no death benefit** [S3 제31조제1항]
[S4] [S5] [S6] [S7], so `claims_death` is a return of the 계약자적립액 and not a sum
assured. There is **no 보험계약대출 and no automatic premium loan during the 납입기간** on
the 미지급형 form, because there is no surrender value to lend against [S3] [REG-R28] — so a
missed premium really does lapse the policy at the end of the 14-day 납입최고. And there is
**no 만기환급금**: `claims(proj_len − 1, "MATURITY")` is zero and the column exists only so that
the statement's shape matches the rest of the library.

---

## Assumption inputs

### (a) Contractual / guaranteed elements (cited; the insurer cannot change them)

| Input | Value | Basis |
|---|---|---|
| 면책기간 | **90 days**; invasive cover from the 암보장개시일, `t = 3` on the grid | [S1] [S2] [S3] [S4] [S7]; [R3] [R6]; grid **[std]** |
| 유사암 carve-out from it | **None** — 「유사암의 보장개시일은 계약일임」, so `t = 0` | [S1] [S2] [S7] |
| 갱신계약 carve-out | **None** — 암보장개시일 = 갱신일 | [S2] [S4] [S6] [S7] |
| 보험나이 15 미만 carve-out | **None** — 암보장개시일 = 보험계약일 | [S2]; [R3] [R6] |
| 부활 | The 90 days **re-runs from the 부활일** | [S1] [S3] [S7]; [REG-R25 제27조](#krlib-reg-r25) |
| Diagnosis inside the window | The **affected cover is 무효**, not merely unpayable; premiums for it returned | [S1 제28조제2항] [S2] [S3]; [R7 제644조](#krlib-cancer-r7) |
| Policyholder's option on voidness | May cancel the **rest** of the contract within **90 days** of the 진단확정일 | [S1 제28조제3항] |
| 감액기간 | **1 year at 50%**, 보험계약일 to 진단확정일, on **every** diagnosis tier; disapplied on a 갱신계약 | [S1] [S6]; [R6]; level **[std]** |
| Definition of 암 | By reference to the **제8차 한국표준질병·사인분류**, with 기타피부암 (C44), 갑상선암 (C73), 대장점막내암 and 전암상태 carved out | [S1] [S2] [S3] [S4]; [R3] [R10] |
| KCD vintage rule | The classification **in force at the 진단확정일** decides the tier, both ways | [S3 제12조] [S4]; [R3] |
| 원발부위 기준 | C77–C80 classifies to the identifiable **primary site**; the 진단확정 date is not moved back | [S1]–[S5]; [R3]; mandated 2011-04-01 |
| 일반암 진단급여금 | **100% of `S`**, 최초 1회한 | [S3 별표 1] |
| 고액암 진단급여금 | **100% of `S` in addition**, so 200% in total, 최초 1회한, on C40–C41, C70–C72, C91–C95 + D47.1 + D47.5 | [S3]; [S10] |
| 특정소액암 진단급여금 | **60% of `S`**, 최초 1회한 | [S3 별표 1] |
| 유사암 진단급여금 | **20% of `S`**, each member once | [S3] [S4]; [R12] |
| 암 직접치료 입원급여금 | **₩50,000 per day** from day 1, **180 days per stay** | [S1] [S4]; [R3] |
| 암 수술급여금 | **₩5,000,000** 관혈 / **₩1,000,000** 비관혈, a **5 : 1** split, unlimited count | [S4] |
| 항암약물·방사선 치료급여금 | **₩10,000,000**, **최초 1회한** | [S1] [S4] [S5] |
| 보험료 납입면제 | On the **first 일반암 or 고액암** on or after the 암보장개시일, or 장해 **50% 이상**; **특정소액암 and 유사암 do not trigger it** | [S3 제14조제1항] [S1 제9조제1항] [S6] [S7] |
| Termination on payment | **None** — no diagnosis benefit terminates or exhausts the contract | [S1] [S3] [S4] |
| Death of the insured | No death benefit; the **계약자적립액 at the date of death** is paid and the contract ends | [S3 제31조제1항] [S4]–[S7]; [REG-R17]; [REG-R25 제22조](#krlib-reg-r25); [REG-R50 제736조](#krlib-reg-r50) |
| Surrender value form | **미지급형**: **0%** during the 납입기간, **50% of the 표준형 value** afterwards; a **전기납** contract on this form has none at any duration | [S3 제41조제2항]; [REG-R19 제7-66조제4항](#krlib-reg-r19) |
| 해약환급금 formula | `max(계약자적립액 − 해약공제액, 0)`, floored at zero | [REG-R19 제7-66조제1항제1호](#krlib-reg-r19) |
| 해약공제기간 | 납입기간 or 신계약비 부가기간, **capped at 7 years** | [REG-R19 제7-66조제1항제2호](#krlib-reg-r19) |
| 해약공제액 cap | The **표준해약공제액** of 감독규정 [별표 14] | [REG-R20] |
| 계약자적립액 accrual | **Monthly** before 납입완료, daily afterwards; permitted to be computed on an **annualised premium** basis | [REG-R19 제7-66조제1항제4호](#krlib-reg-r19); [REG-R18 제7-65조제2항](#krlib-reg-r18) |
| 납입최고 (grace) | **At least 14 days** from the demand; the contract terminates the day after it expires | [S1]; [REG-R25 제26조](#krlib-reg-r25) |
| Expiry | At the **100세 계약해당일**; **nothing is paid** | [S4] [S7]; [S8] |

### (b) Insurer-discretionary current elements

This class is **nearly empty, and its emptiness is the product fact.** The composite is
**무배당** wherever the dividend basis is stated [S1] [S3] [S8], so there is no 계약자배당
and the surplus-distribution machinery of 감독규정 제6-11조의7 and 제6-13조 does not attach
[REG-R12]. The design is **금리확정형**, so there is no 공시이율 to reset and no
최저보증이율 to bind — that machinery belongs to `WholeLife_KR_S`. There is no premium review
on the 비갱신형 chassis and no MVA. What remains:

| Input | Snapshot value | Basis |
|---|---|---|
| 예정이율 / 계약자적립액 적용이율 | **2.50% p.a.**, 금리확정형 | **[std]**, anchored on the **평균공시이율** of 2.50% for 2026, a figure the FSS Governor computes under 감독규정 제1-2조제13호 [REG-R9] [REG-R48]; observed 1.5% [S8] and a 0.5% floor [S1] |
| Incidence basis in the filed rate | The insurer's own, in the **산출방법서**, a 기초서류 filed with the FSC and not published | [REG-R2] |
| 갱신형 renewal rates | Recomputed at each renewal at the attained age on the rate basis then in force | [S4 제2-11조의6]; base run holds the issue rate flat, `renew_reprice_rate = 0.0` **[std]** |
| 유사암 ratio | 10% [S6] [S7], **20%** [S3] [S4], 70% on a pre-2022 design [S8]; a model point column | [R12]; the instrument itself was not retrieved and is [unverified] |
| 감액기간 length | 0 [S2], **12** [S1] [S6], 24 months [S3] [S4] [S5] [S7]; a model point column | as cited |
| 비흡연체형 rate class | A formal 약관 chapter with its own 보험요율; **the differential is not published** | [S3]; not modelled **[std]** |

**A full-text search of the 감독규정 returns zero occurrences of 예정이율** [REG-R9]: the
regulation speaks only of the **계약자적립액 적용이율** and of the 금리확정형 / 금리연동형
distinction of 제1-2조제6호·제7호 [REG-R48]. The 예정이율 of a specific Korean product is
therefore not a published number for any product in this library, and every one of them is
**[std]**.

### (c) Behavioral / experience assumptions (modeler's view — all [std])

**Incidence — and this is the one decrement in `krlib` that is genuinely sourced.** For
mortality, Korea's industry table (제10회 경험생명표, applied from 2024-04) is **not
published in full**: 보험개발원 releases the 평균수명 and the 기대여명 and not the rates
[REG-R33] [REG-R34]. For **cancer incidence the position is the opposite**. 보험개발원
publishes, for public display, its 장기손해보험 참조순보험요율 in force 적용시점 2024년 4월
1일 이후, and that display carries a 「기타피부암 및 갑상선암 이외의 암 발생률」 grid by age
and sex [R5] [REG-R61]:

| 만나이 | 0 | 10 | 20 | 30 | **40** | 50 | 60 | 70 | 80 |
|---|---|---|---|---|---|---|---|---|---|
| 남자 | 0.000297 | 0.000148 | 0.000230 | 0.000531 | **0.001343** | 0.003567 | 0.008540 | 0.019206 | 0.027892 |
| 여자 | 0.000318 | 0.000152 | 0.000250 | 0.001005 | **0.003382** | 0.004962 | 0.006239 | 0.008626 | 0.011452 |

It is dated, it has a stated effective date, and **its definition is the insured one** —
invasive cancer excluding 기타피부암 (C44) and 갑상선암 (C73), classified by 원발부위 — so
it already embodies the tier carve-out the 약관 make and the 원발부위 rule the supervisor
imposed from 2011-04-01. It crosses by sex at about 55–60, matching the registry's own
「50대 초반까지는 여자의 암발생률이 더 높다가, 50대 후반부터 남자의 암발생률이 더 높아지는」
[R1]. **A unisex cancer basis is materially wrong at every age and wrong in opposite
directions either side of about 55**: at 만나이 40 the female rate is **2.52×** the male; at
80 the male rate is **2.44×** the female [R5].

The reconciliation against the registry is in `product-spec.md` and its result is the licence
for everything below: interpolating [R1]'s male all-site crude rates to exact age 40 and
deducting thyroid gives **0.001365** against the bureau's published **0.001343**, a
difference of **+1.6%** with the right sign, because C44 could not be deducted [R1] [R5].
**A published net premium rate and an independently derived crude rate agree to within two
per cent.**

Two things are standardized on top of the sourced grid and both say so at the point of use:

    inc_rate(age) = exp( ln r(a) + (age − a)/(b − a) × ( ln r(b) − ln r(a) ) )     [std]

**log-linear in age** between adjacent published grid ages `a` and `b`, which reproduces
every published value exactly and is locally the exponential family the curve follows; and
the **two rows above 80**, at 90 and 100, which are a **[std]** extrapolation at the age-80
rate × 1.15, flat thereafter, on the deceleration [R1]'s crude bands show. Log-linear
extrapolation of the 70-to-80 slope was rejected: it reaches 0.0405 at male 90 — a
decadal step of 1.45 where the registry's own male 80+ band is only **1.24×** its 70–79
band, against a 70–79 / 60–69 step of 1.88 [R1].

    inc_rate_mth = inc_rate(age(t)) / 12        [std, uniform within the policy year]

**`inc_be_factor = 1.0`, and that identity is a decision, not an omission.** The shipped rate
is a **참조순보험요율**, a net premium rate with a safety loading already inside it, not a
best estimate [REG-R4] [REG-R9 제1-2조제1호](#krlib-reg-r9). The claim that the loading is about 10% was
seen only in a search summary and is **[unverified]**, so the adjustment is left at the
identity rather than resting the model on an unconfirmed number. The direction is stated: it
**overstates** best-estimate incidence by whatever the loading is. What *is* sourced is that
the rate contains **no trend allowance at all** — 「현재도 예정위험률 산출 시 미래의 추세를
반영하지 않고 있음」 [R4] — while Korea's crude cancer incidence has risen **161%** since
1999 (216.0 → 564.3 per 100,000) against a 30% rise in the age-standardised series [R1]. A
contract written to age 100 is exposed to the **crude** series, because it ages with its
policyholder. The two errors run in opposite directions and neither is quantified.

**The tier decomposition — where most of this model's judgement lives [std].** The published
grid is a single rate on the insured definition; the contract needs four.
`tier_share_table.csv` carries three shares per (sex, age) anchor at 20 / 40 / 60 / 80,
**linearly interpolated in age [std]**. The anchor cell reads, at 만나이 40 male,
`minor_share = 0.180000`, `high_share = 0.030000`, `similar_share = 0.530000`. Then

    i_g(t) = inc_rate(t) × (1 − minor_share(t)) / 12      일반암, a partition of the base
    i_m(t) = inc_rate(t) × minor_share(t)     / 12        특정소액암, the complement
    i_h(t) = inc_rate(t) × high_share(t)      / 12        고액암, a SUBSET, paid in addition
    i_z(t) = inc_rate(t) × similar_share(t)   / 12        유사암, ADDITIVE to the base

Read the four lines carefully, because their algebra differs and `check_tier_shares()`
asserts exactly this: `i_g + i_m = inc_rate / 12` is a **partition**; `i_h ≤ i_g` is a
**subset** of the general tier that pays a second lump sum rather than a different one, which
is why a leukaemia pays 200% and a stomach cancer 100% [S3]; and `i_z ≥ 0` is **additive**,
because 유사암 sits **outside** the base rate's own definition — the grid excludes C44 and
C73 by construction, which is exactly the 유사암 boundary, so the grid and the reduced tier
fit together rather than needing reconciliation [R5] [REG-R61].

The levels are anchored on [R1]'s 2023 all-ages crude site rates per 100,000 — 대장 63.8,
유방 58.4, 전립선 44.3 (the 특정소액암 sites), 갑상선 69.3 and 상피내암 74.7 (the 유사암
sites), against an excluding-thyroid base of 495.0 — and then **graded in age and split by
sex [std]**, because those all-ages figures mix age distributions that differ violently.
Without the grading the reduced tier is mispriced by a wide margin in both directions: at
female 만나이 30 the model's 유사암 rate is **0.001136** a year against a general-tier rate
of **0.000593**, so the reduced tier is nearly twice the tier it is a fraction of; by 만나이
60 the same ratio is 0.20. **The 유사암 figure is a floor**, and the reason is a data reason:
[R1] does not cover 경계성종양 (D37–D48) at all, does not identify 대장점막내암 inside 대장
D010–D012, and does not carry 기타피부암 in its top-ten table. The **고액암** share is the
weakest of the three: none of 골, 뇌 or 백혈병 is in the retrieved top-ten table [R1], so
`high_share` is a [std] construction with no published anchor at all.

**Mortality of the never-diagnosed [std].** `mort_table.csv` is a **construction, not a
copy**. There is no Korean equivalent of the freely downloadable Japanese 標準生命表, so
there is no published rate to anchor on [REG-R33] [REG-R34]. What is shipped is a Makeham

    q(x) = 1 − exp( −( A + B c^(x + 0.5) ) )                                       [std]

whose two free parameters are solved so that the table reproduces the **국가데이터처 생명표**'s
2024 기대여명 at ages 40 and 65 exactly — 남 41.9 / 19.5 and 여 47.4 / 23.7 [REG-R38] — and
which then returns 기대수명 at birth of 80.80 and 86.88 against the published 80.8 and 86.6.
That last is a **check, not a target**, and it is the only external validation available.
Ages 15 to 100, the composite's issue-age range through to its 100세 만기. At the anchor
cell `q(40) = 0.0011068200` and `mort_rate_mth = 1 − (1 − q)^(1/12) = 0.000092281823`
**[std]**.

**`mort_be_factor = 1.0`, and unlike jplib's 1.25 that is right.** The shipped table is a
**population all-cause basis** calibrated to public 기대여명, not a valuation table with a
prudential margin, so there is no margin to unwind. Scaling it would be inventing one. The
one honest caveat is the same double-count every cancer model carries: the never-diagnosed
carry a population rate that already contains cancer deaths, and the diagnosed carry them
again as an excess hazard. At 만나이 40 the base rate 0.0011068200 is 0.76% of the
first-year general-tier excess hazard and the effect is second-order; at 80 it is not. A
`net_of_cancer` baseline is a switch and the double-count is stated rather than discovered.

**Post-diagnosis survival — the assumption a protection model does not have.** The public
quantity is **relative survival** — 「관찰생존율을 일반인구의 기대생존율로 나누어 구한
값」 [R1] — a *ratio to an expected general-population survival*, not a cohort curve and
not a transition rate. It therefore converts into an **excess hazard added to** the base table
rather than into a replacement for it, and every post-diagnosis survival model in this
library is a **[std]** construction. The calibration targets are all public:

| Target | Value | Source |
|---|---|---|
| 5-year relative survival, all cancers, 2019–2023 diagnoses | 73.7% (남 68.2 / 여 79.4) | [R1] |
| 5-year relative survival **excluding thyroid** — the general-tier target | **69.6%** (남 **65.9** / 여 **74.0**) | [R1] |
| 5-year relative survival, 갑상선 — the 유사암 target | **100.2%** | [R1] |
| Lifetime cancer mortality risk | 19.6% (남 24.2 / 여 15.6); 갑상선 **0.1%** | [R1] |
| Prevalent patients more than 5 years from diagnosis | **62.1%** (1,697,799 of 2,732,906) | [R1] |

`survival_table.csv` is a **select excess hazard by sex, tier and duration year**, graded
downward across five select years with a non-zero ultimate. Male:

| `dur_year` | 1 | 2 | 3 | 4 | 5 | 6 (ultimate) |
|---|---|---|---|---|---|---|
| `general` | 0.14596111 | 0.10425794 | 0.07089540 | 0.05421413 | 0.04170317 | 0.020 |
| `minor` | 0.04850043 | 0.03464316 | 0.02355735 | 0.01801444 | 0.01385726 | 0.008 |

**The first five general-tier hazards sum to 0.41703175 = −ln(0.659)**, so the model's
five-year relative survival is the published male excluding-thyroid **65.9%** exactly [R1].
The 특정소액암 row's five sum to **0.13857264 = −ln(0.8706)**, the [R1]-derived male
특정소액암 figure built from the three named sites' own published five-year survivals — 대장
75.6, 유방 94.7, 전립선 96.9 per cent [R1]. **The 유사암 tier appears in no row of the file
at all**: its excess hazard is zero, by design.

The grading is **[std]** and its shape is defensible rather than fitted: a flat hazard
reproducing 65.9% would be `−ln(0.659)/5 = 0.0834063` a year, and holding it flat kills long
survivors far too fast when 62.1% of the prevalent population is beyond year five [R1]. The
**non-zero ultimate** of 0.020 (general) and 0.008 (minor) is there for the same reason: a
step to nil after year five would be visibly wrong. Then

    mort_rate_waived_mth(t, k) = 1 − (1 − mort_rate_mth(t)) × exp( −mu_gen(k) / 12 )
    mort_rate_minor_mth(t, k)  = 1 − (1 − mort_rate_mth(t)) × exp( −mu_min(k) / 12 )

which is an **addition of hazards**, never a multiplication of survivorships by a
relative-survival figure. The stage decomposition that makes the target credible, and the
route to a finer model, is in `product-spec.md`: 국한 46.1% of patients at 92.7% survival,
국소 28.0 / 75.6, 원격 17.8 / 27.8, 모름 8.2 / 60.5, which reweight to **73.8** against the
published all-cancer **73.7** [R1]. **Survival is a stage story far more than a site story**,
the stage mix is moving in the policyholder's favour — 국한 45.6% (2005) → 51.8% (2023) —
and the drift raises the cost of every post-diagnosis limb [R1]. The model does not project
it.

**Care intensity — the weakest file in the model, and it says so on every row.** **No Korean
source publishes cancer admissions, bed-days, operations or treatment courses per diagnosed
patient.** The one published utilisation series on the 보험개발원 display is a **질병입원율
for all disease**, not for cancer [R5]. So `care_table.csv` is **[std] throughout**, its
*shape* standardized on the clinical ordering the contracts' own design implies — treatment
is front-loaded into the first two years after diagnosis and decays to a maintenance level —
and its *level* on the 180-day-per-stay cap the contracts carry [S1] [S4] [R3]:

| `dur_year` | `hosp_adm_yr` | `hosp_days_adm` | `surg_open_yr` | `surg_closed_yr` | `treat_hazard_yr` |
|---|---|---|---|---|---|
| 1 | 2.00 | 15.0 | 0.60 | 0.30 | 1.20 |
| 2 | 1.00 | 10.0 | 0.10 | 0.10 | 0.20 |
| 3 | 0.75 | 8.0 | 0.05 | 0.06 | 0.08 |
| 4 | 0.50 | 8.0 | 0.04 | 0.05 | 0.05 |
| 5 | 0.40 | 7.5 | 0.03 | 0.04 | 0.04 |
| 6 (ultimate) | 0.30 | 6.5 | 0.02 | 0.03 | **0.00** |

Three properties earn comment. **No row's `hosp_days_adm` approaches the 180-day cap**, so
the cap never binds in the base run; `check_hosp_cap()` asserts that the contractual cap is
respected rather than that it bites, and a user who raises the intensities will find out
which. **`surg_open_yr + surg_closed_yr` in select year 1 is 0.90** — about one operation
per newly diagnosed life, which is the sanity check. And the **ultimate first-treatment
hazard is exactly zero**, which is what makes the 최초 1회한 bound hold at any horizon: a
life that has reached the ultimate cohort without drawing the treatment benefit never draws
it, so `treat_cum_pp(t)` converges. On the anchor cell it converges to **0.7516253263** and
`check_treat_ledger()` asserts it never exceeds 1.

The **treatment availability** ledger is a mid-cohort construction **[std]**:

    treat_avail(k) = exp( − Σ_{j=1}^{min(k,6)} treat_hazard_yr(j) × span(j) )

evaluated at the **midpoint** of select year `k` — `m = 12(k − 1) + 6` months — so that
`treat_avail(1) = exp(−1.20 × 0.5) = 0.5488116361` rather than 1.0 or `exp(−1.20)`. Reading
it at the start of the year overstates the benefit by paying every entrant at full
availability; reading it at the end understates it. The six values are

    0.5488116361, 0.2725317930, 0.2369277587, 0.2220172938, 0.2122479738, 0.2080451824

and the **flattening after year 2 is the signature of a zero ultimate hazard**: nothing more
is consumed, so nothing more is unavailable.

**Lapse [std], on a form the regulator prescribes rather than the market observes.**
감독규정 제7-66조제4항 permits the **미지급형** form only where the premium or benefit was
calculated using a **최적해지율** [REG-R19], and the FSS's November 2024 계리가정 ruling then
fixes the shape: among models converging to zero lapse at 완납 the **로그-선형 모형** is the
원칙모형, converging to **0.1%**, with a post-완납 ultimate of **0.8%** [REG-R27]. So
`lapse_table.csv` carries three segments and not a policy-year grid:

| segment | `first_year` | `at_completion` | `post_payment` |
|---|---|---|---|
| annual rate | **4.6%** | **0.1%** | **0.8%** |

    lapse_rate(t) = r0 × (r1 / r0)^((y − 1)/(n − 1))    for policy year y ≤ n = pay_term
                  = r2                                   for y > n
    lapse_rate_mth(t) = 1 − (1 − lapse_rate(t))^(1/12)                              [std]

The 0.1% and the 0.8% are the ruling's own numbers [REG-R27]; **only the 4.6% starting level
is standardized**, and it has no observed range because **no public Korean lapse or
persistency figure for 암보험 exists** [R3]. It is set so that the geometric path averages
about 1.5% over the twenty-year 납입기간, which is what a log-linear convergence to 0.1%
implies for a contract whose surrender value is nil throughout it. The **instrument-level
caveat is real**: the 「IFRS17 주요 계리가정 가이드라인」 attachment was never converted from
HWP, so the values are verified from the 보도자료 and **the functional form is
[unverified]** at instrument level [REG-R27].

**Lapse applies to the premium-paying states only [std], and that is a product fact.** The
waiver fires on the first invasive diagnosis [S3 제14조제1항], a waived life therefore has no
premium to miss, and there is no surrender value to take on the 미지급형 form during the
납입기간 [S3 제41조] — so `lapse_rate_canc_mth(t)` is **identically zero** whatever
`lapse_canc_factor` is set to. The 특정소액암 state is different: it keeps paying and it can
lapse, on the healthy rate. On the `waiver_trigger = "none"` design — model point 9 — the
diagnosed keep paying and can lapse, and `lapse_canc_factor` becomes live.

**Expenses and commission (all levels [std]; no Korean cancer expense or commission scale is
public).** [S1] names 계약체결비용 and 계약관리비용 **without amounts**; [S8] states the
surrender value is 「계약자적립액에서 해약공제액을 공제한 금액」 **without quantifying the
deduction**. What is available is a statutory ceiling and a supervisory statement, and the
composite sets its acquisition cost between them: [별표 14] caps the deductible acquisition
cost at the **표준해약공제액** [REG-R20], and the FSC's 2019 expense reform states the same
cap as **13 months' premium for a 보장성보험** [REG-R29].

| Input | Value | Basis |
|---|---|---|
| Acquisition expense | **₩300,000** per policy at `t = 0` | **[std]** — 6.7 months of premium, comfortably inside the 13-month cap [REG-R29] |
| Initial commission | **0.6 × annualised premium** at `t = 0` = ₩324,000 | **[std]**; the 제4-32조제5항 first-year cap is the first year's expected premium [REG-R22] and does not bind |
| Renewal commission | **3.0%** of premiums from `t = 12` | **[std]** |
| Maintenance expense | **₩2,500** per policy per month, inflating **2.0% p.a.** at each policy anniversary | **[std]** |
| Claim expense, diagnosis | **₩150,000** per diagnosis trigger, any tier | **[std]** |
| Claim expense, admission | **₩30,000** per cancer admission | **[std]** |
| Expense inflation | **2.0% p.a.** flat | **[std]** |
| Gross-to-net loading | **15%** = `prem_load_acq` 10% + `prem_load_maint` 5% | **[std]**; drives `prem_alloc_pp` |

Together, initial commission and acquisition expense are **₩624,000 at `t = 0` against a
₩45,000 monthly premium** — 13.9 months of premium, and the reason `net_cf(0)` is
−₩581,686.84 on a contract whose first-year benefit outgo is under ₩20,000.

**The notional 보험가입금액, and why a 제3보험 product needs one [std].** [별표 14] states
the 표준해약공제액 as

    표준해약공제액 = 연납순보험료 × 5% × 해약공제계수 + 보험가입금액 × 10/1000     [REG-R20]

with 해약공제계수 = 「보험기간(최대 20년)」 = **20** and the 연납순보험료 recomputed on a
20년납 footing for a term of 20 years or more (note 3). **The second term needs a
보험가입금액 that this product does not have**, because it carries no death benefit at all:
[별표 15] 제3호 covers only 일반사망을 보장하는 보장성보험, so a cancer contract falls into
**제9호** — 보험가입금액 = (위험보험료 ÷ 정기보험의 위험보험료) × 정기보험의 보험가입금액,
computed at the 기준연령 요건, 남자 만 40세, 전기납, 월납 [REG-R21] [REG-R9]. Reproducing
that ratio needs a term assurance's risk-premium scale the model does not carry, so
`notional_sa_ratio = 0.60` **[std]** stands in for it: **60% of the headline sum insured**, a
plausible order for a benefit paid once on a morbidity trigger rather than on death, and the
figure `product-spec.md` footnote 30 reaches independently by working backwards from the
13-month cap. **This is the route by which a Korean 제3보험 product with no face amount
acquires one, and `LTC_KR_S` and `Child_KR_S` inherit it** — with the difference that 제9호's
third bullet **excludes long-term-care risk premium** from the ratio [REG-R21].

---

## Cash flow components and recursions

### Notation

| Symbol | Meaning |
|---|---|
| `t` | policy month, **0-based**: `t = 0, 1, …, proj_len() − 1`, with `T = proj_len() − 1` |
| `x`, `age(t)` | issue 만나이; attained 만나이 `x + floor(t/12)` |
| `y(t)` | policy year, the contractual 1-based label `floor(t/12) + 1` |
| `T`, `m` | `T = proj_len() − 1` = 12 (100 − x), the last projected month, so `proj_len()` = 12 (100 − x) + 1 is the row count; `pay_months()` = 12 × `pay_term_y`, or `T` on 전기납 |
| `S`, `P` | 보험가입금액; level monthly office premium |
| `W`, `W_j` | 면책기간 in months (3); tier `j`'s own 면책기간 (3, 3, 3, **0**) |
| `cover(t)` | `1{t ≥ W_general}` — the invasive gate |
| `cover_z(t)` | `1{t ≥ W_similar}` — the 유사암 gate, **1 from `t = 0`** |
| `G`, `g(t)` | 감액기간 in months (12); `g(t) = 0.50` for `t < G`, else 1.00 |
| `r_j` | tier `j`'s benefit ratio: 1.00 high, 1.00 general, 0.60 minor, 0.20 similar |
| `i(t)` | annual base incidence, 암 발생률 ex C44 and C73 |
| `m(t)`, `h(t)`, `z(t)` | `minor_share`, `high_share`, `similar_share` at `age(t)` |
| `i_g, i_m, i_h, i_z` | the four monthly tier incidences |
| `q(t)`, `q_mth(t)` | annual and monthly base mortality |
| `μ_g(k)`, `μ_n(k)` | annual select excess hazard, general and minor tier, cohort `k` |
| `q_w(t,k)`, `q_n(t,k)` | monthly mortality of the waived and the 특정소액암 state |
| `w(t)`, `w_mth(t)` | annual and monthly lapse on the premium-paying states |
| `w_c(t)` | monthly lapse on the waived state (**0** under the waiver) |
| `s_0(t)` | `surv_healthy(t)` = `(1 − q_mth)(1 − w_mth)` |
| `s_w(t,k)`, `s_n(t,k)` | `surv_waived`, `surv_minor` — the two diagnosed survival factors |
| `l_0(t)` | `pols_healthy(t)` |
| `D_w(t,k)`, `D_n(t,k)` | `pols_waived_dur`, `pols_minor_dur` — the twelve cohort counts |
| `E_w(t,k)`, `E_n(t,k)` | `pols_waived_exp`, `pols_minor_exp` — cohort count **plus the month's entry** |
| `G_w(t,k)`, `G_n(t,k)` | `waived_grad`, `minor_grad` — the graduation flows |
| `l_c(t)`, `l(t)` | `pols_cancer(t)`; `pols_if(t)` |
| `n_g, n_h, n_m, n_z` | `diag_gen`, `diag_high`, `diag_minor`, `diag_similar` |
| `Z(t)` | `similar_avail(t)` — 유사암 tier unused, per policy |
| `A(k)` | `treat_avail(k)` — treatment benefit unused, per diagnosed life |
| `d(t)`, `λ(t)` | `pols_death(t)`, `pols_lapse(t)` |
| `V(t)` | `av_pp(t)` — 계약자적립액 per policy in force |
| `α(t)`, `α*` | `surr_chg_pp(t)`; `surr_chg_cap_pp()` — the 표준해약공제액 |
| `CV*(t)`, `CV(t)` | `cv_std_pp(t)`, `cv_pp(t)` |
| `D`, `L_k` | 입원급여금 daily amount (₩50,000); mean days per admission in cohort `k` |
| `a_k` | admissions per diagnosed life-year in cohort `k` |
| `u_k`, `v_k` | 관혈 and 비관혈 operations per diagnosed life-year in cohort `k` |
| `θ_k` | annual **first**-treatment hazard in cohort `k` |
| `B_o`, `B_c`, `B_tr` | 관혈 ₩5,000,000; 비관혈 ₩1,000,000; 치료급여금 ₩10,000,000 |
| `e(t)`, `ec(t)` | maintenance expense per policy; claim-handling expense |

**Dimensional check.** `i`, `i_g`, `i_m`, `i_h`, `i_z`, `q`, `q_w`, `q_n`, `w` and `w_c` are
dimensionless probabilities **per month**; `μ`, `a_k`, `u_k`, `v_k` and `θ_k` are **per
year** and appear only divided by 12 or inside `exp(−·/12)`. `L_k` is **days**, so `D × L_k`
is KRW per admission and `D × L_k × a_k/12 × D_·(t,k)` is KRW per policy-month. `B_tr` is KRW
per **event**, so `B_tr × θ_k/12 × A(k)` is KRW per diagnosed life-month directly — **no day
count and no month count enters the treatment benefit at all**, because the Korean benefit is
**최초 1회한** and not, as in Japan, a monthly payment [S1] [S4] [S5]. Inserting a duration
into it is the commonest way to break the limb.

**The three benefit amounts scale linearly off a ₩30,000,000 reference [std]**: `hosp_daily`,
`surg_open_amt`, `surg_closed_amt` and `treat_benefit` are each `base × S / sa_ref` with
`sa_ref = 30,000,000`. At the anchor cell they are the contractual amounts exactly:
**₩50,000** a day to **180** days per stay, **₩5,000,000** 관혈, **₩1,000,000** 비관혈,
**₩10,000,000** treatment.

### The two waiting periods

    cover(t)   = 1  if  W_general = min(wait_months, 3) ≤ t < T,  else 0
    cover_z(t) = 1  if  W_similar = min(wait_months, 0) ≤ t < T,  else 0

`cover(t)` multiplies **every invasive-tier benefit and both invasive transitions**: in
months 0, 1 and 2 the model diagnoses nobody with an invasive cancer, pays nothing for one,
and moves nobody into a diagnosed state. It is a **hard zero, not a reduced rate**, and
`check_waiting_period()` asserts it: the residual it sums is `claims_diag_gen +
claims_diag_high + claims_diag_minor + diag_first`, and it is zero for every `t < 3`.

`cover_z(t)` is **1 from `t = 0`** — 「유사암의 보장개시일은 계약일임」 [S1], the 면책기간
table marking 유사암 진단비 `×` [S1] [S2] and the summary marking the four 유사암 limbs `-`
[S7]. One life carrier does apply the wait to 갑상선암 [S3] [S4]; the composite follows the
majority. **The benefit vector therefore has two start dates**, and the first three rows of
the worked example show them: `claims_diag_similar` is the only non-zero benefit at `t = 0`,
`t = 1` and `t = 2`.

`tier_wait_months(tier) = min(wait_months, tier_table.wait_months)` — the **minimum**, so
that a model point setting `wait_months = 0` (the 갱신형 chassis, model point 3) removes both
gates and a model point setting `wait_months = 3` leaves the 유사암 gate open at zero. It is
not a maximum and not an override.

### The 감액기간

    g(t) = 0.50   for  t < G
         = 1.00   for  t ≥ G

and `g(t)` multiplies **all four diagnosis lump sums and nothing else**. It is measured from
the 보험계약일 to the 진단확정일 [S1] [S6] [R6], it is **not** a permanent benefit scaling,
and on a 갱신계약 it is disapplied altogether — 「※ 갱신계약의 경우 감액지급을 적용하지
않습니다」 [S2] [S4]. On a 비갱신형 contract it bites **once, at the start**, and its
present-value effect is stated cleanly, which is the whole reason `product-spec.md` chose the
비갱신형 chassis against the market majority.

One refinement is **not** implemented and the omission is stated with its direction: the
clock's second endpoint differs by benefit, running to the **진단확정일** for a diagnosis
benefit [S3 별표 1 주2] but to the **수술일** for a surgery or treatment benefit [S4] [S5],
so a cancer diagnosed at month 10 and operated on at month 14 really does draw a reduced
diagnosis benefit and a **full** surgery benefit — which is the model's answer too. The
model applies the reduction to the diagnosis tiers **only**, and never to the care limbs, so
it gives the contract's own answer whenever the **treatment** date falls outside `G`, which
includes every case in which the diagnosis itself does; where the treatment date falls
*inside* `G` it **overstates the care limbs slightly**, because the contract would halve
them and the model does not.

### Incidence and the four diagnosis flows

    i_g(t) = i(t) (1 − m(t)) / 12      i_m(t) = i(t) m(t) / 12
    i_h(t) = i(t) h(t) / 12            i_z(t) = i(t) z(t) / 12

    n_gh(t) = l_0(t) i_g(t) cover(t)                                  first, from healthy
    n_m(t)  = l_0(t) i_m(t) cover(t)                                  특정소액암
    n_gm(t) = ( l_n(t) + n_m(t) ) i_g(t) cover(t)                     minor → general
    n_g(t)  = n_gh(t) + n_gm(t)
    n_h(t)  = ( l_0(t) + l_n(t) + n_m(t) ) i_h(t) cover(t)
    n_z(t)  = l(t) Z(t) i_z(t) cover_z(t) × diag_module

    first(t) = n_gh(t) + n_m(t)                                       leaving pols_healthy

Five things in those seven lines are decisions and not algebra.

**`n_gm` is the 특정소액암 → 일반암 transition**, and its exposure is `l_n(t) + n_m(t)`: the
existing 특정소액암 stock **plus this month's new entrants**, because a life diagnosed with a
특정소액암 in month `t` is already in that state for the rest of month `t`. The same
convention puts `n_m(t)` inside `n_h`'s exposure. It is small — at `t = 3` it is
0.00000000182660 against a general-tier flow of 0.00009067430249, five orders of magnitude
down — and it is the only reverse-ordering term in the model, so getting it wrong is
undetectable in the first year and material in the fortieth.

**`n_h` is a subset flow, not a partition flow.** 고액암 pays **in addition to** the general
tier [S3], so a leukaemia diagnosis produces both `n_g` and `n_h` and pays 200%. `n_h` does
not reduce `n_g` and must not.

**`n_z` rides on `l(t)`, the whole in-force population**, and on `Z(t)`, the per-policy
availability ledger — not on `l_0(t)`. A 유사암 is payable to a life who has already had an
invasive cancer, because the tiers are independent once-only benefits and payment of one
neither terminates nor exhausts the contract [S1] [S3] [S4].

**`n_z` carries `diag_module` and the invasive flows do not.** Switching the diagnosis limb
off (model point 8, the treatment-cost-only shape of [S5]) must not switch off the
**transitions**, because the care benefits, the waiver and the excess mortality all still
run: the contract has no diagnosis lump sum, not no cancer. So `diag_module` gates the
diagnosis *claims* — it appears inside `claims(t, "DIAG_*")` — and gates `n_z` only because
`n_z` has no other consequence.

**`first(t)` is what leaves `pols_healthy`, and it excludes `n_h` and `n_gm`.** Both of those
are diagnoses of lives who are already leaving, or have already left, the healthy state, and
double-decrementing them would leak population. `check_pols_roll_fwd()` catches it.

    Z(t + 1) = Z(t) ( 1 − i_z(t) cover_z(t) diag_module )      Z(0) = 1

with `similar_used(t)` its complement, accumulated from the realised flow, and
`check_similar_ledger()` asserting `Z(t) + used(t) = 1` at every `t` with lives in force. On
the anchor cell `Z(720) = 0.9172290909` — **8.28%** of policies have consumed the 유사암 tier
over sixty years.

**One aggregate 유사암 ledger stands in for five [std].** The contract pays each 유사암
member once — 기타피부암, 갑상선암, 대장점막내암, 제자리암, 경계성종양 — so a life may
collect up to five reduced benefits [S3] [S4]. The model carries **one** ledger and one flow.
The direction is stated: it **understates**.

### The diagnosed states and their six cohorts

The two diagnosed states share one recursion shape, written here for the waived state; the
특정소액암 state is identical with `n_m` for `n_g`, `s_n` for `s_w`, and the extra transition
factor inside `s_n`.

    s_0(t)    = (1 − q_mth(t)) (1 − w_mth(t))
    s_w(t,k)  = (1 − q_w(t,k)) (1 − w_c(t))
    s_n(t,k)  = (1 − i_g(t) cover(t)) (1 − q_n(t,k)) (1 − w_mth(t))

    E_w(t,k)  = D_w(t,k) + n_g(t) · 1{k = 1}                exposure, incl. this month's entry
    E_n(t,k)  = D_n(t,k) + n_m(t) · 1{k = 1}

    G_w(t,1)  = n_g(t − 13) · Π_{u = t−13}^{t−1} s_w(u, 1)                    t ≥ 13
    G_w(t,k)  = G_w(t − 12, k − 1) · Π_{u = t−12}^{t−1} s_w(u, k)             k ≥ 2

    D_w(t+1,k) = E_w(t,k) s_w(t,k) + G_w(t+1, k−1) · 1{k ≥ 2} − G_w(t+1, k) · 1{k ≤ 5}

Read the last line with the two before it. A life diagnosed in month `s` enters cohort 1 at
`s`, is exposed to cohort 1's decrements for twelve months, and **graduates to cohort 2 at
`s + 13`** — thirteen, not twelve, because the entry month is a full month of cohort-1
exposure and the delay is measured from the *entry* month rather than from the start of the
following one. `G_w(t, 1)` is exactly that: the month-`t − 13` entrants carried forward on
cohort 1's own survival. Thereafter each cohort hands on to the next twelve months later.
**The graduation terms telescope out of the state total**, `l_w(t) = Σ_k D_w(t,k)`, so
`check_cancer_roll_fwd()` — which rebuilds `l_c(t + 1)` as `Σ_k (E_w s_w + E_n s_n)` without
any graduation term at all — closes to 1e-10. And `check_canc_dur_ledger()` rebuilds cohort 1
**independently, from the entry history**, so an off-by-one in the delay shows up there and
nowhere else.

**`s_n` carries the transition factor and `s_w` does not.** A 특정소액암 life can leave its
state by being diagnosed with a 일반암; a 일반암 life has nowhere to go. That asymmetry is
the `(1 − i_g cover)` factor, and it must appear in `surv_minor`, in `pols_death`'s minor limb
and in `pols_lapse`'s minor limb, or the counts stop rolling forward.

**`w_c(t) = 0` under the waiver, and that is a product fact rather than a refinement.** A
waived life has no premium to miss and no surrender value to take on the 미지급형 form
[S3 제41조] [REG-R28], so there is no mechanism by which a waived policy leaves the book other
than death. On `waiver_trigger = "none"` (model point 9) it is the healthy monthly rate scaled
by `lapse_canc_factor`.

### Decrements, and the order they are applied in

    d(t)  = ( l_0(t) − first(t) ) q_mth(t)
          + Σ_k E_w(t,k) q_w(t,k)
          + Σ_k E_n(t,k) (1 − i_g(t) cover(t)) q_n(t,k)

    λ(t)  = ( l_0(t) − first(t) ) (1 − q_mth(t)) w_mth(t)
          + Σ_k E_w(t,k) (1 − q_w(t,k)) w_c(t)
          + Σ_k E_n(t,k) (1 − i_g(t) cover(t)) (1 − q_n(t,k)) w_mth(t)

    pols_maturity(t) = l(t) · 1{t = T}

Within month `t` the order is **transition, then mortality, then lapse**, and each state is
decremented **on its own basis**. A life diagnosed in month `t` is exposed to its **new**
state's mortality for the rest of that month — that is why `E_w` and `E_n` and not `D_w` and
`D_n` appear above — and a 특정소액암 life who progresses to 일반암 in month `t` takes the
**general** tier's decrements for the rest of it. `check_pols_roll_fwd()` asserts

    l(t) − l(t + 1) − d(t) − λ(t) − pols_maturity(t) = 0

for every `t = 0 … T`, to 1e-10, on every model point. `pols_if_at(t, timing)` publishes the
in-force at three named points inside the month — `BEF_DECR`, `BEF_LAPSE`, `AFT_DECR` — so
that a reader can see where the order bites without re-deriving it.

**`pols_death` and `pols_lapse` are zero at `t = T`.** The contract has already ended;
`pols_maturity(T) = l(T)` records the cover ending and `claims(T, "MATURITY") = 0` records
that nothing is paid for it.

### The benefit lines

    claims_diag_gen(t)     = 1.00 × S × g(t) × n_g(t) × diag_module
    claims_diag_high(t)    = 1.00 × S × g(t) × n_h(t) × diag_module
    claims_diag_minor(t)   = 0.60 × S × g(t) × n_m(t) × diag_module
    claims_diag_similar(t) = 0.20 × S × g(t) × n_z(t)

    P_k(t)            = D_w(t,k) + D_n(t,k)            = pols_diag_dur(t, k)
    claims_hosp(t)    = D × Σ_k ( a_k / 12 ) min(L_k, 180) P_k(t) × hosp_module
    claims_surgery(t) = Σ_k ( B_o u_k / 12 + B_c v_k / 12 ) P_k(t) × surg_module
    claims_treat(t)   = B_tr × Σ_k ( θ_k / 12 ) A(k) P_k(t) × treat_module

    claims_death(t)   = V(t) d(t)
    claims_lapse(t)   = CV(t) λ(t)
    claims_maturity(t)= 0

Note the weights. **The diagnosis lines ride on flows** — `n_g`, `n_h`, `n_m`, `n_z`, the
month's new diagnoses — and **the care lines ride on stocks**, `pols_diag_dur(t, k)`, the
diagnosed population at the start of the month. The two are different objects with
different dimensions, and the care lines are on `D`, not on `E`: the month's own entrants do
not draw a care benefit in their diagnosis month, which is the episode convention above and
the reason `t = 4` is the first month with any care benefit on the anchor cell.

**The care benefits do not distinguish the two diagnosed states.** A 특정소액암 life draws
the same inpatient, surgery and treatment amounts as a 일반암 life, because the contract
grades those limbs by **tier of the diagnosed cancer** only through the 유사암 relativity and
not through the 특정소액암 one [S1] [S4]. What differs between the two states is the
mortality and the premium, and that is exactly what the two states carry.

**The 유사암 tier draws no care benefit at all [std].** Real contracts pay the inpatient and
treatment limbs at 20–25% on a 유사암 [S1] [S4]. The composite's `n_z` moves no life into a
diagnosed state, so it contributes no `D_w` and no `D_n`, and therefore no care benefit. The
direction is stated: it **understates**. Attaching the invasive care intensities to a 유사암
life would credit it with an exposure no retrieved statistic measures.

**`claims_death` is a return of the account, not a benefit.** `V(t)` is the 계약자적립액 at
the start of the month, and `V(t) d(t)` is what 감독규정 제7-63조제1항제1호 requires be paid
on a death from a cause the policy does not cover [REG-R17] [REG-R25 제22조](#krlib-reg-r25). It is **zero at
`t = 0`**, because the account is nil there, and it is **zero from `t = 447`** on the anchor
cell, because the account has been exhausted — the floor in the account recursion is not
decorative.

**`claims_lapse` is zero for the whole 납입기간 on the 미지급형 form.** `CV(t) = 0` for
`t < m`, so the entire first twenty years of lapses cost nothing in cash. On the anchor cell
the first non-zero `claims_lapse` is at **`t = 240`** and it is **₩1,891.71**: the surrender
value steps from nil to ₩4,078,536.79 and the lapse rate steps from 0.1% to 0.8% in the same
month. Two steps in one row, and both of them are prescribed rather than chosen.

### The 계약자적립액, the 해약공제액 and the 해약환급금

    prem_alloc_pp(t) = P × premium_factor(t) × (1 − 0.15) × 1{t < m} × 1{t < T}
    risk_prem_pp(t)  = ( Σ over the seven cancer benefit lines ) / l(t)
    V(t + 1)         = max( 0, ( V(t) + prem_alloc_pp(t) − risk_prem_pp(t) ) × 1.025^(1/12) )
    V(0)             = 0

**This is a retrospective recursion floored at zero, not the prospective reserve of a
산출방법서 [std].** The regulation defines the 계약자적립액 by reference to the 산출방법서
[REG-R18 제7-65조제1항](#krlib-reg-r18), which is not a public document [REG-R2], so no prospective basis can
be reproduced. What is reproduced is its *behaviour*: an account that accrues the allocated
premium, discharges the month's risk premium and accumulates at the 예정이율. The seven lines
inside `risk_prem_pp` are the four diagnosis lines and the three care lines — **the DEATH and
LAPSE lines are excluded**, because they are payments *out of* the account and including them
would make the recursion self-referential.

The **floor at zero** binds on the anchor cell from **`t = 447`** — 만나이 77, 62% of the way
through the term — because the anchor's premium is 32% below the shipped basis's equivalence
level. It is the visible consequence of the premium being a modelling input, and the
worked example states it rather than smoothing it.

    α* = min(  12 P (1 − 0.15) × 0.05 × 20  +  S × 0.60 × 0.01 ,   13 P  )
    α(t) = α* × max( 0, 1 − t / n ),  n = surr_chg_months() = 12 min(max(m/12, 1), 7)
    CV*(t) = max( V(t) − α(t), 0 )
    CV(t)  = CV*(t)                     on the 표준형 form
           = 0                          on 미지급형, 전기납
           = 0.00 × CV*(t)              on 미지급형, t < m
           = 0.50 × CV*(t)              on 미지급형, t ≥ m

On the anchor cell the [별표 14] formula gives **459,000 + 180,000 = 639,000** and the
**13-months-of-premium cap of [REG-R29] binds at 585,000** — the same figure
`product-spec.md` footnote 30 reaches by hand. The **run-off is straight-line over the
해약공제기간 [std]**: [별표 14] states the cap and **not its run-off shape** [REG-R20], and
the 해약공제기간 is `min(납입기간, 신계약비 부가기간, 7년)` [REG-R19 제7-66조제1항제2호](#krlib-reg-r19), so
`α(t) = 0` from **`t = 84`** — thirteen years before 납입완료. `check_cv_floor()` asserts
`0 ≤ CV(t) ≤ CV*(t)` at every `t`, and additionally that `CV(t) = 0` for every `t < m` on the
미지급형 form.

### Premium, expense and commission

    premium_factor(t) = 1                          on 비갱신형, or 갱신형 with no repricing
                      = (1 + ρ)^floor(t / 120)     on 갱신형 with ρ = renew_reprice_rate

    pols_payer(t) = l_0(t) + l_n(t)      under the waiver
                  = l(t)                 on waiver_trigger = "none"

    premiums(t) = P × premium_factor(t) × pols_payer(t) × 1{t < m} × 1{t < T}

    e(t)          = 2,500 × 1.02^floor(t/12) × l(t) × 1{t < T}
    expenses(t)   = e(t) + 300,000 × 1{t = 0}
    ec(t)         = ( 150,000 ( n_g(t) + n_m(t) + n_z(t) )
                    + 30,000 Σ_k ( a_k / 12 ) ( D_w(t,k) + D_n(t,k) ) ) × 1{t < T}
    commissions(t)= 0.6 × 12 P × 1{t = 0} + 0.03 × premiums(t) × 1{t ≥ 12}

**`premiums` rides on `pols_payer` and the maintenance expense on `pols_if`.** A waived
policy is still administered — it still receives statements, it still has a 계약자적립액 to
credit, and it still claims — so `e(t)` is on the whole in-force population while `premiums`
is on the paying subset. The two weights differ by the waived state, which is
**0.0265665643** of **0.7204769811** at `t = 240`, so **3.7% of the block is being serviced
for nothing** at 납입완료 and 17.7% at `t = 480`.

**`ec(t)`'s diagnosis limb counts `n_g + n_m + n_z` and not `n_h`.** A 고액암 is a claim on
the same file as the 일반암 that accompanies it; charging a second handling cost for the
top-up would double-count the event. The admission limb rides on the same admission count as
`claims_hosp`, so the two move together by construction.

**Commission at `t = 0` is `0.6 × 12 P`, not `0.6 × 12 P × pols_if(0)`.** It is paid once, on
the policy, at issue. On the anchor cell it is ₩323,999.9999999999 — the floating-point
residue of `0.6 × 12` is visible at ten decimals and is reproduced here rather than tidied
away, because the test module asserts the model's value and not a hand-cleaned one.

### Net cash flow

    net_cf(t) = premiums(t)
              − claims_diag_gen(t) − claims_diag_high(t)
              − claims_diag_minor(t) − claims_diag_similar(t)
              − claims_hosp(t) − claims_surgery(t) − claims_treat(t)
              − claims_death(t) − claims_lapse(t) − claims_maturity(t)
              − expenses(t) − claim_expenses(t) − commissions(t)

`net_cf` is **income-positive** in the shipped model, per the library convention, and it is
the **only** orientation published: there is no outgo-positive `liability_cf` companion, one
stream, one sign, one name. `check_net_cf()` re-derives the identity from the published frame
— premiums, less every column whose name begins `claims_`, less `expenses`,
`claim_expenses` and `commissions` — and asserts it to 1e-10 × `sum_assured` at every `t`.
That check is the reason `result_cf()` publishes the ten `claims_*` split columns and
**nothing named `claims`**: a statement carrying its own subtotal among its parts is silently
non-additive for any reader who sums the row. The total remains available as the
`claims(t, kind)` cells with `kind` omitted.

**The cash-flow signature of the product is one asymmetry.** Premium is weighted by
`pols_healthy + pols_minor`; the diagnosis benefits by the month's diagnosis flows; the care
benefits by the diagnosed stock. **Every invasive diagnosis simultaneously starts a benefit
stream and stops a premium**, so any error in the incidence basis hits both sides of the
cash flow at once and its effect on `net_cf` is roughly doubled. Weighting the premium by
`pols_if` is the single largest arithmetic error available in this product, and it is
**invisible for the first four months**, because until `t = 4` the two are equal.

### Optional modules (all off in the base run)

| Module | Switch | What it does | Why it is off |
|---|---|---|---|
| **Validity adjustment** | `void_adjust = False` | A diagnosis inside the 90-day window makes the affected cover **무효** [S1 제28조제2항] [R7 제644조](#krlib-cancer-r7) — a **de-recognition, not a decrement**, releasing the premium already collected as well as the future benefit. Switching it on scales `pols_if_init()` down by `void_prob() = 1 − (1 − i(0)/12)^W` | It belongs in a validity adjustment at outset, not in the lapse column. At the anchor cell it is **0.0003357124**, 0.034% of policies against at most three months of premium — stated, not silently absorbed |
| **Best-estimate incidence** | `inc_be_factor = 1.0` | Scales the sourced 참조순보험요율 to a best estimate | The loading inside the reference rate is [unverified] [REG-R4]. Leaving the factor at the identity **overstates** best-estimate incidence by the loading |
| **Renewal repricing** | `renew_reprice_rate = 0.0`, `renewal_months = 120` | On the 갱신형 flag, multiplies the premium by `(1 + ρ)` at each ten-year renewal | Setting the chassis flag already removes the 면책기간, the 감액기간 and the waiver's persistence [S2] [S4] [S6] [S7]. Holding the rate flat **records the contract-boundary tension rather than resolving it** [REG-R60] |
| **Diagnosed lapse** | `lapse_canc_factor = 1.0` | Scales `lapse_rate_canc_mth` | **Inert rather than off**: under the waiver a diagnosed life cannot lapse whatever the factor is. It reaches a cash flow on model point 9 alone |
| **표준형 surrender basis** | `cv_form = "pyojun"` | Pays `CV*(t)` at every duration | The base is 미지급형, because that is where the market is: the 무·저해지 share of 보장성 초회보험료 ran **11.4% (2018) → 47.0% (2023) → 63.8% (2024 H1)** [REG-R27]. Model point 9 carries it |
| **Mortality margin** | `mort_be_factor = 1.0` | Scales the base table | The shipped table is a **population** basis calibrated to public 기대여명 [REG-R38], not a valuation table with a margin to unwind |
| **재진단암** | not implemented | 100% of `S` on a **2-year** cycle from the previous qualifying diagnosis [S1] [S8] | The **cycle is sourced and the rate is not**: no public source gives a cancer re-diagnosis incidence, and the institute calls the quantity 「매우 불확실」 while warning that improving survival makes 「3차, 4차 암 진단보험금 지급이 가능함」 [R4] |
| **암 요양병원 입원급여금** | not implemented | ₩20,000 a day to 90 days [S2] [S8] | 요양병원 days are excluded from the composite's inpatient limb — the market's own structural answer to the most disputed benefit in Korea, where 금융감독원 took **2,125 complaints about 암입원비 in 2018** [R3] |
| **암 다빈치로봇 수술급여금**, **암 사망 및 고도후유장해**, **비흡연체형**, **간편심사** | not implemented | as specified | Each because its rate or its differential cannot be sourced [S2] [S3] [S5] [R4] |
| **부활** | not implemented | Reinstatement within 3 years [REG-R25 제27조](#krlib-reg-r25) | Lapse is **absorbing**, which is the conservative direction: a reinstated Korean cancer policy re-runs the 90 days from the 부활일 [S1] [S3] [S7], so it is not the policy that lapsed |

---

## Policyholder behavior modeling

- **Lapse is real and immediate — for the premium-paying states.** On a product with a
  surrender value the insurer would advance an unpaid premium under an automatic premium
  loan; the composite has **none during the 납입기간** on the 미지급형 form, and no
  보험계약대출 either, because there is no value to lend against — 「순수보장성보험 등
  보험상품의 종류에 따라 보험계약대출이 제한될 수도 있습니다」 [S3] [REG-R28]. So a missed
  premium really does lapse the policy at the end of the **14-day 납입최고** [S1] [REG-R25
  제26조](#krlib-reg-r25), and the model applies lapse at the end of the month in which the premium is missed
  without modelling the notice period.
- **A waived life cannot lapse.** No premium to miss, no surrender value to take
  [S3 제41조]. `lapse_rate_canc_mth(t) = 0` in the base run, and applying the healthy lapse
  rate to the waived state deletes exactly the claimants the product exists to pay.
- **A 특정소액암 life can.** It keeps paying and it keeps the healthy lapse rate, because the
  waiver excludes it by name [S3 제14조제1항]. This is the one place where the two diagnosed
  states behave differently as *behaviour* rather than as mortality.
- **The lapse shape is prescribed, not observed.** The 로그-선형 convergence to 0.1% at
  완납 and the 0.8% ultimate are the FSS's November 2024 계리가정 원칙모형 [REG-R27], and
  the reason they are prescribed is that IFRS 17 CSM on 무·저해지 business is highly
  sensitive to the assumption — which is why the supervisor took an interest in 2024 at all.
  **No public Korean lapse or persistency figure for 암보험 exists** [R3], so the model
  implements the prescribed form and standardizes only its starting level.
- **The step at 납입완료 is a step in *two* quantities at once.** The lapse rate steps from
  0.001 to 0.008 and the surrender value steps from nil to 50% of the 표준형 value, in the
  same month, by two independent instruments — [REG-R27] and [S3 제41조]. On the anchor cell
  that produces the model's only discontinuity in `claims_lapse`: **₩0.00 at `t = 239` and
  ₩1,891.71 at `t = 240`**. A model that implements one step and not the other is wrong in a
  way the row makes obvious.
- **Reinstatement (부활) is not a persistency detail on this product.** Available within
  **3 years** of termination where the surrender value has not been drawn — **including where
  there is none**, which is the 무해지 case — on arrears with interest within 평균공시이율 +
  1%, a ceiling of 3.50% at the 2026 rate [REG-R25 제27조](#krlib-reg-r25) [REG-R48]. What makes it
  structural is that **the 90-day 암보장개시일 re-runs from the 부활일** [S1] [S3] [S7]: a
  reinstated cancer policy is a policy with 90 days of no invasive cover in front of it,
  which is a genuine anti-selection control. It therefore enters the model as a **new model
  point**, not as a negative lapse, and the base run treats lapse as **absorbing**. The
  direction is conservative.
- **No dynamic lapse from surrender value or interest.** The value is nil for the whole
  납입기간, the design is 금리확정형, and there is no MVA, so there is no economic surrender
  trigger. The 무해지 cliff that drives the `whole_life` surrender spike is **much smaller
  here**: on a 순수보장성 cancer contract there is barely any 계약자적립액 to suppress, and
  the one retrieved illustration shows 환급률 of 0.0% (year 1), 11.3% (3), **21.6% (5)**,
  20.5% (7) and **0.0% at maturity** [S8] — a value that peaks at years 5–7 and returns to
  nil, a pure-protection signature rather than a savings one.
- **Anti-selective lapse is not modelled.** Healthy lives lapse first, so the persisting
  never-diagnosed block should be progressively impaired on the *incidence* basis, and the
  waiver amplifies it because the healthiest lives are also the only ones still paying. **No
  Korean evidence was retrieved**, so no `lam` is asserted; the omission **understates** late
  incidence and is named in the pitfalls list.
- **Elections are not behaviour.** `similar_ratio`, `reduction_months` and the module flags
  are fixed at issue. 감액 (benefit reduction) on request is available with fresh
  underwriting for any increase and is not projected. A model that lets them move over `t` is
  modelling a contract term that does not exist.
- **청약철회 is out of scope.** A pre-inception decrement, **15 days** from receipt of the
  보험증권 or 30 days from the application, whichever comes first [REG-R51] [REG-R25 제17조](#krlib-reg-r25).
  Modelling it would need a new-business funnel this library does not have.

---

## Worked example

### The anchor cell

**`point_id = 1`.** Male, **만나이 40** at issue (보험나이 40 in the contract), 비갱신형,
보험기간 to the **100세 계약해당일**, **20년납**, 보험가입금액 **₩30,000,000 (3천만원)**,
표준체, **해약환급금 미지급형**, all four benefit modules on, `waiver_trigger = cancer_diag`,
level office premium **₩45,000 per month**, `wait_months = 3`, `reduction_months = 12`,
`similar_ratio = 0.20`.

It is the cell **Korean regulation itself computes at**: 감독규정 제1-2조제2호's 기준연령
요건 is 「전기납 및 월납 조건으로 남자가 만 40세에 보험에 가입하는 경우」 [REG-R9], and it
is the cell at which the 표준해약공제액 comparison [REG-R20], the 보험가입금액 computation of
[별표 15] [REG-R21] and the 보장성/저축성 test are all performed. Using it as the model's
anchor makes the model point and the regulatory reference point the same cell, which no other
choice achieves.

Derived scalars, read off the model: `proj_len() = 721` (so `result_cf()` has **721 rows**,
`t = 0 … 720`, index name `t`, first column `pols_if`), `pay_months() = 240`,
`pols_if_init() = 1.0`, `surr_chg_months() = 84`, **`surr_chg_cap_pp() = 585,000`**.

**The benefit ladder at `S = 30,000,000`:**

| tier | `benefit_ratio` | amount | `tier_wait_months` | waives premium |
|---|---|---|---|---|
| `high` (고액암) | 1.00 **in addition** | ₩30,000,000, so **₩60,000,000 in total** | 3 | yes |
| `general` (일반암) | 1.00 | ₩30,000,000 | 3 | yes |
| `minor` (특정소액암) | 0.60 | ₩18,000,000 | 3 | **no** |
| `similar` (유사암) | 0.20 | ₩6,000,000 | **0** | **no** |

**Event-module amounts**, each `base × S / 30,000,000`: `hosp_daily() = 50,000` a day,
`hosp_day_cap() = 180` days per stay, `surg_open_amt() = 5,000,000`,
`surg_closed_amt() = 1,000,000`, `treat_benefit() = 10,000,000`.

**Every assumption value the anchor cell uses**, tagged:

- **Incidence, base rate.** `inc_rate(0) = 0.001343` a year — the **published** 보험개발원
  「기타피부암 및 갑상선암 이외의 암 발생률」 at 남자 40, read verbatim [R5] [REG-R61]. Ages
  between the published ten-year points are **log-linear [std]**: `inc_rate(12) = 0.0014808079`
  at 만나이 41, from 0.001343 at 40 and 0.003567 at 50. `inc_be_factor = 1.0`.
- **Tier shares [std]**, at 만나이 40 male: `minor_share = 0.180000`, `high_share = 0.030000`,
  `similar_share = 0.530000`; at 41, linearly interpolated toward the age-60 anchors,
  0.188000 / 0.029500 / 0.511000.
- **Monthly tier incidences at `t = 0 … 11`.** `i_g = 0.00009177166667`,
  `i_m = 0.00002014500000`, `i_h = 0.00000335750000`, `i_z = 0.00005931583333`.
- **Mortality, never-diagnosed.** `mort_rate(0) = 0.0011068200` at 만나이 40 from the [std]
  Makeham calibrated to the 국가데이터처 생명표's 2024 기대여명 [REG-R38];
  `mort_rate_mth = 1 − (1 − 0.0011068200)^(1/12) = 0.000092281823`. `mort_be_factor = 1.0`.
- **Excess hazard, general tier, male [std]:** 0.14596111, 0.10425794, 0.07089540,
  0.05421413, 0.04170317 across select years 1–5 and **0.020** ultimate; the five sum to
  **0.41703175 = −ln(0.659)**, the published male excluding-thyroid 5년 상대생존율 of
  **65.9%** [R1]. Hence `mort_rate_waived_mth(t, 1) = 0.01218091654617` at 만나이 40.
- **Excess hazard, 특정소액암 tier, male [std]:** 0.04850043, 0.03464316, 0.02355735,
  0.01801444, 0.01385726, **0.008** ultimate; the five sum to
  **0.13857264 = −ln(0.8706)** [R1]. Hence `mort_rate_minor_mth(t, 1) = 0.00412545541339`.
- **유사암 excess hazard: zero**, in no row of the table [R1].
- **Lapse [std] [REG-R27].** `lapse_rate(0) = 0.046` in policy year 1,
  `lapse_rate_mth = 0.003916610623`; log-linear to 0.001 at policy year 20; **0.008** from
  policy year 21. `lapse_rate_canc_mth(t) = 0` throughout, because the waiver is on.
- **Care intensity per diagnosed life [std]**, select year 1: `hosp_adm_yr = 2.00`,
  `hosp_days_adm = 15.0`, `surg_open_yr = 0.60`, `surg_closed_yr = 0.30`,
  `treat_hazard_yr = 1.20`; `treat_avail(1) = 0.5488116361`. The six `treat_avail` values are
  0.5488116361, 0.2725317930, 0.2369277587, 0.2220172938, 0.2122479738, 0.2080451824.
- **Per diagnosed life-month in select year 1**, the numbers worth memorising as an
  implementation check: inpatient `50,000 × (2.00/12) × 15.0` = **₩125,000.00**; surgery
  `5,000,000 × 0.60/12 + 1,000,000 × 0.30/12` = **₩275,000.00**; treatment
  `10,000,000 × (1.20/12) × 0.5488116361` = **₩548,811.64**. In the ultimate cohort they are
  **₩8,125.00**, **₩10,833.33** and **₩0.00** — the treatment limb is 최초 1회한 and its
  ultimate hazard is zero.
- **Expenses and commission [std].** `expense_acq = 300,000` at `t = 0`;
  `expense_maint = 2,500` a month inflating at `inflation_rate = 0.02` per policy year;
  `expense_claim_diag = 150,000`; `expense_claim_hosp = 30,000`;
  `comm_init_rate = 0.6` of annualised premium at `t = 0`; `comm_renewal_rate = 0.03` from
  `comm_renewal_start = 12`.
- **Account and surrender [std] and cited.** `prem_int_rate = 0.025`;
  `prem_load_acq = 0.10` + `prem_load_maint = 0.05`, so `prem_alloc_pp = 38,250` a month
  while `t < 240`; `surr_chg_coef = 20.0`, `surr_chg_cap_months = 13.0`,
  `notional_sa_ratio = 0.60`, `surr_chg_period_y = 7`; `cv_floor_ratio = 0.0`,
  `cv_post_pay_ratio = 0.5`.
- **Switches, all inert.** `void_adjust = False`, `lapse_canc_factor = 1.0`,
  `renew_reprice_rate = 0.0`, `renewal_months = 120`, `roll_fwd_tol = 1e-10`.

**Every one of the ten `check_*()` cells returns `True` on this cell** — and on all ten
shipped model points: `check_pols_roll_fwd`, `check_cancer_roll_fwd`, `check_canc_dur_ledger`,
`check_similar_ledger`, `check_treat_ledger`, `check_tier_shares`, `check_waiting_period`,
`check_cv_floor`, `check_hosp_cap`, `check_net_cf`.

### First periods of the base run

The first sixteen months, at the precision the model produces. Policy counts are the state at
the **start** of month `t`; cash flows are the month's.

| `t` | `pols_if` | `pols_healthy` | `pols_minor` | `pols_waived` |
|---|---|---|---|---|
| 0 | 1.0000000000 | 1.0000000000 | 0.0000000000 | 0.0000000000 |
| 1 | 0.9959914690 | 0.9959914690 | 0.0000000000 | 0.0000000000 |
| 2 | 0.9919990063 | 0.9919990063 | 0.0000000000 | 0.0000000000 |
| 3 | 0.9880225475 | 0.9880225475 | 0.0000000000 | 0.0000000000 |
| 4 | 0.9840612075 | 0.9839518955 | 0.0000197422 | 0.0000895698 |
| 5 | 0.9801149387 | 0.9798980147 | 0.0000392427 | 0.0001776813 |
| 6 | 0.9761836936 | 0.9758608358 | 0.0000585040 | 0.0002643538 |
| 7 | 0.9722674247 | 0.9718402900 | 0.0000775283 | 0.0003496064 |
| 8 | 0.9683660844 | 0.9678363090 | 0.0000963178 | 0.0004334576 |
| 9 | 0.9644796254 | 0.9638488243 | 0.0001148748 | 0.0005159263 |
| 10 | 0.9606080001 | 0.9598777680 | 0.0001332015 | 0.0005970306 |
| 11 | 0.9567511612 | 0.9559230725 | 0.0001513001 | 0.0006767886 |
| 12 | 0.9529090613 | 0.9519846704 | 0.0001691728 | 0.0007552182 |
| 13 | 0.9497671846 | 0.9487370834 | 0.0001898413 | 0.0008402599 |
| 14 | 0.9466348029 | 0.9455005753 | 0.0002102819 | 0.0009239457 |
| 15 | 0.9435118979 | 0.9422751081 | 0.0002304966 | 0.0010062932 |

| `t` | `premiums` | `claims_diag_gen` | `claims_diag_high` | `claims_diag_minor` | `claims_diag_similar` |
|---|---|---|---|---|---|
| 0 | 45,000.0000000000 | 0.0000000000 | 0.0000000000 | 0.0000000000 | 177.9475000000 |
| 1 | 44,819.6161043715 | 0.0000000000 | 0.0000000000 | 0.0000000000 | 177.2236791336 |
| 2 | 44,639.9552831831 | 0.0000000000 | 0.0000000000 | 0.0000000000 | 176.5028024875 |
| 3 | 44,461.0146379684 | 1,360.1145372945 | 49.7602879498 | 179.1334279764 | 175.7848580859 |
| 4 | 44,278.7236965491 | 1,354.5380432401 | 49.5562698746 | 178.3953984216 | 175.0696879449 |
| 5 | 44,097.1765825684 | 1,348.9843037453 | 49.3530842834 | 177.6604095480 | 174.3572831176 |
| 6 | 43,916.3702899898 | 1,343.4532268520 | 49.1507278117 | 176.9284488278 | 173.6476346630 |
| 7 | 43,736.3018246864 | 1,337.9447209662 | 48.9491971085 | 176.1995037851 | 172.9407336464 |
| 8 | 43,556.9682043961 | 1,332.4586948569 | 48.7484888362 | 175.4735619952 | 172.2365711397 |
| 9 | 43,378.3664586762 | 1,326.9950576548 | 48.5485996703 | 174.7506110849 | 171.5351382220 |
| 10 | 43,200.4936288586 | 1,321.5537188506 | 48.3495262994 | 174.0306387316 | 170.8364259796 |
| 11 | 43,023.3467680051 | 1,316.1345882941 | 48.1512654254 | 173.3136326638 | 170.1404255064 |
| 12 | 42,846.9229408627 | 2,862.2789611635 | 103.9867356580 | 397.5372102810 | 360.2731924222 |
| 13 | 42,701.7116126315 | 2,852.5784887687 | 103.6343170181 | 396.1810575071 | 359.0626773615 |
| 14 | 42,556.9885736717 | 2,842.9106353042 | 103.2830834255 | 394.8295310933 | 357.8559029089 |
| 15 | 42,412.7522107091 | 2,833.2752929993 | 102.9330309649 | 393.4826152575 | 356.6528614724 |

| `t` | `claims_hosp` | `claims_surgery` | `claims_treat` | `claims_death` | `claims_lapse` |
|---|---|---|---|---|---|
| 0 | 0.0000000000 | 0.0000000000 | 0.0000000000 | 0.0000000000 | 0.0000000000 |
| 1 | 0.0000000000 | 0.0000000000 | 0.0000000000 | 3.5064829465 | 0.0000000000 |
| 2 | 0.0000000000 | 0.0000000000 | 0.0000000000 | 6.9920489980 | 0.0000000000 |
| 3 | 0.0000000000 | 0.0000000000 | 0.0000000000 | 10.5917132184 | 0.0000000000 |
| 4 | 13.6639954092 | 30.0607899003 | 59.9916774089 | 14.1079661237 | 0.0000000000 |
| 5 | 27.1155078447 | 59.6541172583 | 119.0504497901 | 17.6764456658 | 0.0000000000 |
| 6 | 40.3572320206 | 88.7859104453 | 177.1881482675 | 21.2953107206 | 0.0000000000 |
| 7 | 53.3918300637 | 117.4620261402 | 234.4164608907 | 24.9627590288 | 0.0000000000 |
| 8 | 66.2219319043 | 145.6882501894 | 290.7469343496 | 28.6770264535 | 0.0000000000 |
| 9 | 78.8501356613 | 173.4702984548 | 346.1909756681 | 32.4363862524 | 0.0000000000 |
| 10 | 91.2790080240 | 200.8138176528 | 400.7598538775 | 36.2391483628 | 0.0000000000 |
| 11 | 103.5110846284 | 227.7243861826 | 454.4647016704 | 40.0836587013 | 0.0000000000 |
| 12 | 115.5488704295 | 254.2075149449 | 507.3165170339 | 47.1268021938 | 0.0000000000 |
| 13 | 128.7626505282 | 283.2778311620 | 565.3315272335 | 51.1537996721 | 0.0000000000 |
| 14 | 141.7784544051 | 311.9125996912 | 622.4773241996 | 55.2230020278 | 0.0000000000 |
| 15 | 154.5987250024 | 340.1171950053 | 678.7646336531 | 59.3328420042 | 0.0000000000 |

`claims_maturity` is **0.0000000000** in every row of the projection, `t = 0 … 720`
inclusive, and is published so that the statement's shape matches the rest of the library.

| `t` | `expenses` | `claim_expenses` | `commissions` | `net_cf` |
|---|---|---|---|---|
| 0 | 302,500.0000000000 | 8.8973750000 | 323,999.9999999999 | -581,686.8448750000 |
| 1 | 2,489.9786724651 | 8.8611839567 | 0.0000000000 | 42,140.0460858697 |
| 2 | 2,479.9975157324 | 8.8251401244 | 0.0000000000 | 41,967.6377758408 |
| 3 | 2,470.0563687760 | 25.3759454102 | 0.0000000000 | 40,190.1974992572 |
| 4 | 2,460.1530187687 | 25.8186812864 | 0.0000000000 | 39,917.3681681708 |
| 5 | 2,450.2873468075 | 26.2533343329 | 0.0000000000 | 39,646.7843001748 |
| 6 | 2,440.4592340447 | 26.6800107630 | 0.0000000000 | 39,378.4244055737 |
| 7 | 2,430.6685616925 | 27.0988154909 | 0.0000000000 | 39,112.2672158733 |
| 8 | 2,420.9152110277 | 27.5098521483 | 0.0000000000 | 38,848.2916814952 |
| 9 | 2,411.1990633969 | 27.9132230988 | 0.0000000000 | 38,586.4769695119 |
| 10 | 2,401.5200002211 | 28.3090294540 | 0.0000000000 | 38,326.8024614052 |
| 11 | 2,391.8779030002 | 28.6973710878 | 0.0000000000 | 38,069.2477508447 |
| 12 | 2,429.9181063839 | 31.2529895192 | 1,285.4076882259 | 34,452.0683526068 |
| 13 | 2,421.9063208058 | 31.6914742116 | 1,281.0513483789 | 34,227.0801199841 |
| 14 | 2,413.9187473808 | 32.1223350179 | 1,276.7096572102 | 34,003.9673010072 |
| 15 | 2,405.9553395705 | 32.5456687957 | 1,272.3825663213 | 33,782.7114396626 |

**Four features of those sixteen rows are the product, and each is a test target.**

1. **`t = 0, 1, 2` pay a 유사암 benefit and nothing else.** The 면책기간 is a hard zero for
   the three invasive tiers and the 유사암 tier has no waiting period at all [S1], so the two
   start dates are visible in the very first rows.
2. **`t = 3` is the 암보장개시일** and all three invasive lines start together, from a
   diagnosed population that is still **empty**: `pols_minor(3) = pols_waived(3) = 0`, so
   every care line is still zero at `t = 3`.
3. **`t = 4` is the first month with any care benefit.** Nobody is *in* a diagnosed state
   until the month after the first diagnosis, and `claims_death` starts one month earlier
   still, at `t = 1`, because `av_pp(0) = 0`.
4. **`t = 12` is where the 감액기간 ends**, and where the renewal commission starts. Every
   diagnosis line roughly doubles between `t = 11` and `t = 12`: 일반암 **×2.1748**, 고액암
   ×2.1596, 특정소액암 ×2.2937, 유사암 ×2.1175. The excess over 2.0 is the age step from
   만나이 40 to 41 and, for 특정소액암, the tier share moving 0.180 → 0.188.

### Where the product does something else

| `t` | `pols_if` | `premiums` | `claims_diag_gen` | `claims_diag_high` | `claims_diag_minor` | `claims_diag_similar` |
|---|---|---|---|---|---|---|
| 11 | 0.956751 | 43,023.346768 | 1,316.134588 | 48.151265 | 173.313633 | 170.140426 |
| 12 | 0.952909 | 42,846.922941 | 2,862.278961 | 103.986736 | 397.537210 | 360.273192 |
| 119 | 0.785353 | 34,901.656258 | 4,692.290682 | 159.964455 | 944.437226 | 451.865648 |
| 120 | 0.784650 | 34,865.602577 | 5,113.201637 | 172.743299 | 1,073.232817 | 471.395893 |
| 239 | 0.721042 | 31,258.960304 | 9,080.571642 | 278.670238 | 2,657.890070 | 466.293749 |
| 240 | 0.720477 | 0.000000 | 9,780.214009 | 296.370121 | 2,966.565180 | 451.223219 |
| 241 | 0.719468 | 0.000000 | 9,763.318813 | 295.858146 | 2,960.815303 | 450.542932 |
| 446 | 0.434675 | 0.000000 | 14,822.256894 | 461.034429 | 4,456.604822 | 334.746937 |
| 447 | 0.432786 | 0.000000 | 14,744.458887 | 458.614584 | 4,430.480887 | 333.247172 |
| 479 | 0.371671 | 0.000000 | 13,198.968285 | 411.824283 | 3,919.401998 | 259.848037 |
| 480 | 0.369770 | 0.000000 | 13,596.651745 | 424.895367 | 4,052.271541 | 243.921552 |
| 599 | 0.135885 | 0.000000 | 4,993.011333 | 156.031604 | 1,366.066002 | 100.166614 |
| 600 | 0.134236 | 0.000000 | 4,996.240153 | 156.132505 | 1,365.911126 | 100.330241 |
| 719 | 0.010679 | 0.000000 | 347.231748 | 10.850992 | 86.923956 | 7.855782 |
| 720 | 0.010345 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |

| `t` | `claims_hosp` | `claims_surgery` | `claims_treat` | `claims_death` | `claims_lapse` | `expenses` | `claim_expenses` | `commissions` | `net_cf` |
|---|---|---|---|---|---|---|---|---|---|
| 11 | 103.511085 | 227.724386 | 454.464702 | 40.083659 | 0.000000 | 2,391.877903 | 28.697371 | 0.000000 | 38,069.247751 |
| 12 | 115.548870 | 254.207515 | 507.316517 | 47.126802 | 0.000000 | 2,429.918106 | 31.252990 | 1,285.407688 | 34,452.068353 |
| 119 | 489.334401 | 880.077229 | 1,420.255917 | 906.917956 | 0.000000 | 2,346.422980 | 68.585360 | 1,047.049688 | 21,494.454715 |
| 120 | 492.943174 | 886.344818 | 1,429.357941 | 978.544115 | 0.000000 | 2,391.210442 | 72.461331 | 1,045.968077 | 20,738.199034 |
| 239 | 1,151.998683 | 2,027.265221 | 3,078.597257 | 4,120.391242 | 0.000000 | 2,626.054278 | 143.816539 | 937.768809 | 4,689.642576 |
| 240 | 1,159.012327 | 2,039.351451 | 3,095.888707 | 4,450.535298 | 1,891.707642 | 2,676.477235 | 149.922328 | 0.000000 | -28,957.267518 |
| 241 | 1,167.052480 | 2,053.328281 | 3,116.263786 | 4,447.499178 | 1,885.957387 | 2,672.727355 | 150.239115 | 0.000000 | -28,963.602775 |
| 446 | 2,217.452034 | 3,741.323495 | 5,042.783514 | 25.822052 | 1.934041 | 2,261.052691 | 255.173569 | 0.000000 | -33,620.184478 |
| 447 | 2,214.916824 | 3,736.203514 | 5,031.635754 | 0.000000 | 0.000000 | 2,251.226614 | 254.448004 | 0.000000 | -33,455.232240 |
| 479 | 2,094.778916 | 3,508.796918 | 4,602.302173 | 0.000000 | 0.000000 | 2,011.433308 | 235.406752 | 0.000000 | -30,242.760672 |
| 480 | 2,089.888822 | 3,499.843779 | 4,586.811501 | 0.000000 | 0.000000 | 2,041.166555 | 237.864350 | 0.000000 | -30,773.315212 |
| 599 | 932.150480 | 1,505.615216 | 1,708.177851 | 0.000000 | 0.000000 | 896.438531 | 101.361693 | 0.000000 | -11,759.019323 |
| 600 | 921.926541 | 1,488.725694 | 1,687.021137 | 0.000000 | 0.000000 | 903.268232 | 100.728268 | 0.000000 | -11,720.283897 |
| 719 | 78.614795 | 122.553239 | 116.006557 | 0.000000 | 0.000000 | 85.878313 | 8.311038 | 0.000000 | -864.226420 |
| 720 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |

Four boundaries, in the order the product reaches them.

- **`t = 11 → 12`, the 감액기간 ends.** Every diagnosis line steps; nothing else does. The
  renewal commission starts in the same row, so `net_cf` falls by ₩3,617.18 despite the
  premium being almost unchanged.
- **`t = 239 → 240`, 납입완료.** The premium goes from ₩31,258.96 to **zero** in one row and
  the renewal commission with it. The surrender value goes from **nil to ₩4,078,536.79** and
  the lapse rate from **0.1% to 0.8%**, so `claims_lapse` goes from ₩0.00 to **₩1,891.71**.
  `net_cf` swings by **₩33,646.91**, from +₩4,689.64 to −₩28,957.27, and is negative in every
  one of the 480 remaining months.
- **`t = 446 → 447`, the 계약자적립액 is exhausted.** `av_pp(447) = 0` and stays zero to
  expiry, so `claims_death` and `claims_lapse` both fall to **exactly zero** and stay there.
  That is the retrospective account's floor binding, at 만나이 **77**, and it is the visible
  consequence of the anchor's premium being 32% below the shipped basis's equivalence level.
- **`t = 719 → 720`, expiry.** Every cash flow is zero at `t = 720`, `pols_maturity(720) =
  pols_if(720) = 0.0103446076`, and `claims_maturity(720) = 0.00` — **nothing is paid at the
  100세 계약해당일** [S8].

### Hand traces

Five months, written out term by term on the printed rates, so that a reader with a
calculator can reproduce a row and watch the processing order do its work.

**Trace, month 0 — the acquisition month, and the 유사암 tier alone in force.**

    l_0(0) = 1.000000,  l_n(0) = l_w(0) = 0,  Z(0) = 1,  g(0) = 0.50
    cover(0) = 0,  cover_z(0) = 1
    premiums    = 45,000 x 1.0 x (1.000000 + 0)                      = 45,000.0000000000
    n_g = n_h = n_m = 0                                       (cover(0) = 0, a hard zero)
    n_z(0)      = 1.000000 x 1 x 0.00005931583333 x 1              = 0.00005931583333
    claims_diag_similar = 0.20 x 30,000,000 x 0.50 x 0.00005931583333
                        = 3,000,000 x 0.00005931583333             = 177.9475000000
    claims_hosp = claims_surgery = claims_treat = 0            (no diagnosed lives at all)
    claims_death = V(0) x d(0) = 0 x 0.00009228182324              = 0.0000000000
    claims_lapse = CV(0) x lambda(0) = 0 x 0.00391624919073        = 0.0000000000
    expenses    = 2,500 x 1.02^0 x 1.000000 + 300,000              = 302,500.0000000000
    claim_expenses = 150,000 x (0 + 0 + 0.00005931583333) + 30,000 x 0
                                                                   = 8.8973750000
    commissions = 0.6 x 12 x 45,000                                = 323,999.9999999999
    net_cf(0)   = 45,000.0000000000 - 177.9475000000 - 302,500.0000000000
                  - 8.8973750000 - 323,999.9999999999             = -581,686.8448750000

    decrements: d(0)      = 1.000000 x 0.000092281823             = 0.00009228182324
                lambda(0) = 1.000000 x (1 - 0.000092281823) x 0.003916610623
                                                                   = 0.00391624919073
                s_0(0)    = (1 - 0.000092281823)(1 - 0.003916610623) = 0.99599146898603
                l_0(1)    = (1.000000 - 0) x 0.99599146898603      = 0.9959914690
                Z(1)      = 1 x (1 - 0.00005931583333)             = 0.999940684167
    account:    V(1) = max(0, (0 + 38,250 - 177.9475) x 1.025^(1/12)) = 38,150.474695

The month is the whole of the product's front-end cost in one row: **₩624,000 of acquisition
expense and initial commission against ₩45,000 of premium**, 13.9 months' worth, and
₩177.95 of benefit. `commissions` is written to ten decimals as the model produces it: the
`0.6 × 12` product is 7.199999999999999 in binary floating point, and the notes reproduce the
model's value rather than a hand-cleaned 324,000.00, because the test module asserts the
former.

**Trace, month 3 — 암보장개시일, from an empty diagnosed state.**

    l_0(3) = 0.9880225475,  l_n(3) = l_w(3) = 0,  Z(3) = 0.999822063055,  g(3) = 0.50
    cover(3) = 1 for the first time
    premiums    = 45,000 x (0.9880225475 + 0)                      = 44,461.0146379684
    n_gh(3)     = 0.9880225475 x 0.00009177166667 x 1              = 0.00009067247589
    n_gm(3)     = (0 + 0.00001990371422) x 0.00009177166667        = 0.00000000182660
    n_g(3)      = 0.00009067247589 + 0.00000000182660              = 0.00009067430249
    n_m(3)      = 0.9880225475 x 0.00002014500000                  = 0.00001990371422
    n_h(3)      = (0.9880225475 + 0 + 0.00001990371422) x 0.00000335750000
                                                                   = 0.00000331735253
    n_z(3)      = 0.9880225475 x 0.999822063055 x 0.00005931583333 = 0.00005859495270
    claims_diag_gen     = 1.00 x 30,000,000 x 0.50 x 0.00009067430249 = 1,360.1145372945
    claims_diag_high    = 1.00 x 30,000,000 x 0.50 x 0.00000331735253 =    49.7602879498
    claims_diag_minor   = 0.60 x 30,000,000 x 0.50 x 0.00001990371422 =   179.1334279764
    claims_diag_similar = 0.20 x 30,000,000 x 0.50 x 0.00005859495270 =   175.7848580859
    claims_hosp = claims_surgery = claims_treat = 0       (D_w(3,k) = D_n(3,k) = 0 for all k)
    claims_death = 114,687.368900 x 0.00009235291837                  =    10.5917132184
    expenses    = 2,500 x 1.02^0 x 0.9880225475                       = 2,470.0563687760
    claim_expenses = 150,000 x (0.00009067430249 + 0.00001990371422
                                + 0.00005859495270) + 30,000 x 0      =    25.3759454102
    net_cf(3)   = 44,461.0146379684 - 1,360.1145372945 - 49.7602879498
                  - 179.1334279764 - 175.7848580859 - 10.5917132184
                  - 2,470.0563687760 - 25.3759454102                  = 40,190.1974992572

    cohort entry: E_w(3,1) = 0 + 0.00009067430249,  s_w(3,1) = 0.98781908345383
                  D_w(4,1) = 0.00009067430249 x 0.98781908345383   = 0.00008956980637
                  E_n(3,1) = 0 + 0.00001990371422,  s_n(3,1) = 0.99188305665071
                  D_n(4,1) = 0.00001990371422 x 0.99188305665071   = 0.00001974215690

Two things to notice. **`claims_surgery(3)` is exactly zero**, which it would not be on the
Japanese chassis, where an in-situ diagnosis generates a surgery benefit in its own diagnosis
month: here the surgery limb rides on the diagnosed **stock** and the stock is still empty.
And **`n_h` does not reduce `n_g`** — the two lines are ₩1,360.11 and ₩49.76 and both are
paid on the same 0.0000033 of 고액암 diagnoses, which is what "pays in addition" means.

**Trace, month 4 — the diagnosed state is live and the care limbs start.**

    D_w(4,1) = 0.00008956980637,  D_n(4,1) = 0.00001974215690
    pols_diag_dur(4,1) = 0.00008956980637 + 0.00001974215690     = 0.00010931196327
    D_w(4,k) = D_n(4,k) = 0 for k >= 2                     (nobody has graduated yet)
    l_0(4) = 0.9839518955,  l_n(4) = 0.0000197422,  l_w(4) = 0.0000895698
    premiums    = 45,000 x (0.9839518955 + 0.0000197422)
                = 45,000 x 0.9839716377                          = 44,278.7236965491
    claims_hosp    = 50,000 x (2.00/12) x 15.0 x 0.00010931196327
                   = 50,000 x 0.00027327990818                   = 13.6639954092
    claims_surgery = (5,000,000 x 0.60/12 + 1,000,000 x 0.30/12) x 0.00010931196327
                   = 275,000 x 0.00010931196327                  = 30.0607899003
    claims_treat   = 10,000,000 x (1.20/12) x 0.5488116361 x 0.00010931196327
                   = 10,000,000 x 0.00000599916774               = 59.9916774089
    claims_death   = 151,462.528504 x 0.00009314492676           = 14.1079661237
    claim_expenses = 150,000 x (0.00009030253622 + 0.00001982171094
                                + 0.00005835656265)
                     + 30,000 x (2.00/12) x 0.00010931196327
                   = 25.2721214700 + 0.5465598164                = 25.8186812864

**The premium weight is the trace's payload.** `premiums(4)` is 45,000 × **0.9839716377**,
not 45,000 × `pols_if(4)` = 0.9840612075. The difference is the **0.0000895698** of lives
whose premium the waiver has stopped — a difference of ₩4.03 in month 4 and of the whole
premium stream by 납입완료. `expenses(4) = 2,500 × 0.9840612075 = 2,460.1530187687` uses
`pols_if`, because a waived policy is still administered. **Two different weights on two
lines of the same row, and the model publishes both.**

**Trace, month 12 — the 감액기간 ends, the age steps, the renewal commission starts.**

    age(12) = 41,  g(12) = 1.00,  y(12) = 2
    inc_rate(12) = exp( ln 0.001343 + (1/10)(ln 0.003567 - ln 0.001343) ) = 0.0014808079
    minor_share  = 0.180 + (0.340 - 0.180) x 1/20                = 0.188000
    high_share   = 0.030 + (0.020 - 0.030) x 1/20                = 0.029500
    similar_share= 0.530 + (0.150 - 0.530) x 1/20                = 0.511000
    i_g(12) = 0.0014808079 x 0.812 / 12                          = 0.00010020133449
    i_m(12) = 0.0014808079 x 0.188 / 12                          = 0.00002319932375
    i_h(12) = 0.0014808079 x 0.0295 / 12                         = 0.00000364031942
    i_z(12) = 0.0014808079 x 0.511 / 12                          = 0.00006305773636
    n_g(12) = 0.00009539013438 + 0.00000001916432                = 0.00009540929871
    claims_diag_gen = 1.00 x 30,000,000 x 1.00 x 0.00009540929871 = 2,862.2789611635
    D_w(12,1) = 0.00075521819673,  D_n(12,1) = 0.00016917276671
    pols_diag_dur(12,1)                                          = 0.00092439096344
    claims_hosp  = 50,000 x 2.5 x 0.00092439096344               = 115.5488704295
    claims_surgery = 275,000 x 0.00092439096344                  = 254.2075149449
    claims_treat = 10,000,000 x 0.1 x 0.5488116361 x 0.00092439096344 = 507.3165170339
    expenses     = 2,500 x 1.02^1 x 0.9529090613 = 2,550 x 0.9529090613
                                                                 = 2,429.9181063839
    commissions  = 0.03 x 42,846.9229408627                      = 1,285.4076882259
    net_cf(12)   = 42,846.9229408627
                   - (2,862.2789611635 + 103.9867356580 + 397.5372102810
                      + 360.2731924222 + 115.5488704295 + 254.2075149449
                      + 507.3165170339 + 47.1268021938)
                   - 2,429.9181063839 - 31.2529895192 - 1,285.4076882259
                                                                 = 34,452.0683526068

**The 일반암 line goes ×2.1748 across the boundary and the model publishes both factors
separately.** 2.0 of it is `reduction_factor` stepping from 0.50 to 1.00; the residual
1.0874 is the incidence stepping from 0.001343 to 0.0014808079 (×1.1026) against the general
share falling from 0.820 to 0.812 (×0.9902), and the in-force falling 0.9559 → 0.9520
(×0.9959). Note that all six cohort counts are still concentrated in `k = 1`: the first
graduation to cohort 2 cannot occur before `t = 16`, thirteen months after the first
diagnosis at `t = 3`.

**Trace, month 240 — 납입완료, and the only row with two prescribed steps in it.**

    l_0(240) = 0.6811234744,  l_n(240) = 0.0127869424,  l_w(240) = 0.0265665643
    l(240)   = 0.7204769811,  age(240) = 60,  inc_rate = 0.008540
    prem_payable(240) = 0  since t = 240 = pay_months()
    premiums    = 45,000 x 0.6939104168 x 0                        = 0.0000000000
    commissions = 0.03 x 0                                         = 0.0000000000
    i_g = 0.008540 x 0.66 / 12 = 0.0004697        i_m = 0.008540 x 0.34 / 12 = 0.0002419667
    n_gh = 0.6811234744 x 0.0004697                                = 0.00031992369591
    n_m  = 0.6811234744 x 0.0002419667                             = 0.00016480917668
    n_gm = (0.0127869424 + 0.00016480917668) x 0.0004697           = 0.00000608343772
    n_g  = 0.00032600713363
    claims_diag_gen   = 30,000,000 x 1.00 x 0.00032600713363       = 9,780.2140089950
    claims_diag_minor = 18,000,000 x 0.00016480917668              = 2,966.5651802476
    claims_hosp  = 50,000 x ( 2.5 x 0.0050936763 + 0.8333333 x 0.0042511714
                            + 0.5 x 0.0036522475 + 0.3333333 x 0.0031990133
                            + 0.25 x 0.0028328475 + 0.1625 x 0.0203245508 )
                 = 50,000 x 0.0231802465457                        = 1,159.0123272870
    claims_treat = 10,000,000 x ( 0.1 x 0.5488116361 x 0.0050936763
                                + 0.0166667 x 0.2725317930 x 0.0042511714
                                + 0.0066667 x 0.2369277587 x 0.0036522475
                                + 0.0041667 x 0.2220172938 x 0.0031990133
                                + 0.0033333 x 0.2122479738 x 0.0028328475
                                + 0.0000000 x 0.2080451824 x 0.0203245508 )
                 = 10,000,000 x 0.000309588870726                  = 3,095.8887072601
    claims_death = 8,157,073.574228 x 0.00054560440800              = 4,450.5352984474
    claims_lapse = 4,078,536.787114 x 0.00046382017385              = 1,891.7076416342
    expenses     = 2,500 x 1.02^20 x 0.7204769811
                 = 2,500 x 1.485947395978 x 0.7204769811           = 2,676.4772347467
    sum of the ten claim lines
                 = 9,780.2140090 + 296.3701215 + 2,966.5651802 + 451.2232186
                 + 1,159.0123273 + 2,039.3514506 + 3,095.8887073 + 4,450.5352984
                 + 1,891.7076416 + 0                               = 26,130.8679545
    net_cf(240)  = 0 - 26,130.8679545 - 2,676.4772347 - 149.9223284 - 0
                                                                   = -28,957.2675176

Three things happen in that one row and all three are prescribed rather than chosen. **The
premium stops** because `t = pay_months()`. **The lapse rate steps from 0.001 to 0.008**,
because the [REG-R27] 로그-선형 model converges to 0.1% at 완납 and the post-완납 ultimate is
0.8%. **The surrender value steps from nil to 50% of the 표준형 value**, ₩4,078,536.79,
because 「보험료 납입기간이 경과된 이후 해지될 경우 '표준형' 해약환급금의 50%」 [S3 제41조].
The last two produce the model's only discontinuity in `claims_lapse`, from **₩0.00** to
**₩1,891.71**. The `claims_treat` limb is worth reading term by term: the ultimate cohort
holds **0.0203245508** of the 0.0393535067 diagnosed lives — more than half the diagnosed
population — and contributes **nothing at all**, because `treat_hazard_yr` is zero there and
the benefit is 최초 1회한.

### Policy year 1 in aggregate (`t = 0 … 11`)

All twelve months at 만나이 40, all inside the 감액기간, and the last nine inside cover — the
strongest single test target in this file, because it exercises both waiting-period
boundaries and the first nine months of the diagnosed state on one set of rates.

| Line | Policy year 1 total |
|---|---|
| Σ `pols_if` | 11.7388451584 |
| Σ `pols_healthy` | 11.7350500326 |
| Σ `pols_minor` | 0.0006907114 |
| Σ `pols_waived` | 0.0031044144 |
| `premiums` | 528,108.3334792526 |
| `claims_diag_gen` | 12,042.1768917546 |
| `claims_diag_high` | 440.5674472593 |
| `claims_diag_minor` | 1,585.8856330344 |
| `claims_diag_similar` | 2,088.2227399267 |
| `claims_hosp` | 474.3907255562 |
| `claims_surgery` | 1,043.6595962237 |
| `claims_treat` | 2,082.8092019227 |
| `claims_death` | 236.5689464717 |
| `claims_lapse` | 0.0000000000 |
| `claims_maturity` | 0.0000000000 |
| `expenses` | 329,347.1128959327 |
| `claim_expenses` | 270.2399621534 |
| `commissions` | 323,999.9999999999 |
| **`net_cf`** | **−145,503.3005609827** |

Benefit outgo in policy year 1 is **₩19,994.28**, which is **3.79%** of year-1 premium. The
totals are sums of unrounded monthly values and the displayed monthly rows do not re-add to
them.

### The 계약자적립액 and 해약환급금 path

| `t` | `av_pp` | `surr_chg_pp` | `cv_std_pp` | `cv_pp` |
|---|---|---|---|---|
| 0 | 0.000000 | 585,000.000000 | 0.000000 | 0.000000 |
| 12 | 444,655.755936 | 501,428.571429 | 0.000000 | 0.000000 |
| 60 | 2,112,717.620900 | 167,142.857143 | 1,945,574.763757 | 0.000000 |
| 84 | 2,959,163.646787 | 0.000000 | 2,959,163.646787 | 0.000000 |
| 120 | 4,229,470.390949 | 0.000000 | 4,229,470.390949 | 0.000000 |
| 180 | 6,290,272.153544 | 0.000000 | 6,290,272.153544 | 0.000000 |
| 240 | 8,157,073.574228 | 0.000000 | 8,157,073.574228 | **4,078,536.787114** |
| 300 | 7,152,135.393646 | 0.000000 | 7,152,135.393646 | 3,576,067.696823 |
| 360 | 5,077,515.345012 | 0.000000 | 5,077,515.345012 | 2,538,757.672506 |
| 420 | 1,763,350.342298 | 0.000000 | 1,763,350.342298 | 881,675.171149 |
| 446 | 15,717.315280 | 0.000000 | 15,717.315280 | 7,858.657640 |
| 447 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| 480 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| 720 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |

Four things to read off it, and every one is asserted somewhere.

- **`cv_pp` is exactly nil for the whole 납입기간** and steps to 50% of the 표준형 value at
  `t = 240`. The 미지급형 cliff is at a **known date** — 「보험료 납입기간 중이라 함은
  계약일로부터 보험료 납입기간이 경과하여 최초로 도래하는 계약해당일 전일까지의 기간」
  [S3 제41조] — so it is a step, not a curve, and `check_cv_floor()` asserts the nil.
- **The 해약공제액 runs off to zero at `t = 84`, thirteen years before the cliff.** The
  해약공제기간 is capped at **7 years** by 제7-66조제1항제2호 [REG-R19], so
  `surr_chg_months() = 84` on a 20년납 contract and `α(t) = 0` from there. **The step at
  `t = 240` is not the surrender charge running off**, and attributing it to amortisation is
  a detectable error.
- **The 표준형 value first becomes positive between `t = 60` and `t = 84`**, when the account
  overtakes the running-off charge — and even then `cv_pp` stays at nil, because the
  미지급형 multiplier is 0.00. **Both quantities exist at every `t`** and the model publishes
  both.
- **The account peaks at 납입완료 and is exhausted at `t = 447`**, 만나이 77. It stays at the
  zero floor to expiry, and `claims_death` and `claims_lapse` fall to exactly zero with it.

### In force by state

| `t` | 만나이 | `pols_if` | `pols_healthy` | `pols_minor` | `pols_waived` | diagnosed share |
|---|---|---|---|---|---|---|
| 0 | 40 | 1.0000000000 | 1.0000000000 | 0.0000000000 | 0.0000000000 | 0.0000% |
| 12 | 41 | 0.9529090613 | 0.9519846704 | 0.0001691728 | 0.0007552182 | 0.0970% |
| 60 | 45 | 0.8431922656 | 0.8375419523 | 0.0012144885 | 0.0044358248 | 0.6701% |
| 120 | 50 | 0.7846501682 | 0.7714827635 | 0.0033084048 | 0.0098589998 | 1.6781% |
| 240 | 60 | 0.7204769811 | 0.6811234744 | 0.0127869424 | 0.0265665643 | 5.4621% |
| 360 | 70 | 0.5768966301 | 0.4963813345 | 0.0285510129 | 0.0519642827 | 13.9566% |
| 480 | 80 | 0.3697699075 | 0.2690451225 | 0.0354016049 | 0.0653231801 | 27.2399% |
| 600 | 90 | 0.1342357333 | 0.0788584939 | 0.0184172276 | 0.0369600118 | 41.2537% |
| 720 | 100 | 0.0103446076 | 0.0048522513 | 0.0016895927 | 0.0038027636 | 53.0939% |

**The whole cost of this product is in the second half of the projection.** The diagnosed
population is 0.10% of the in-force after twelve months, **5.46%** at 납입완료, **27.24%** at
만나이 80 and **41.25%** at 90. The 특정소액암 state is a third of the diagnosed population
at 납입완료 and it is still paying premium — 1.77% of the in-force paying against 3.69% waived
at that date. A ten-year projection sees almost none of the liability this contract carries.

### Policy-year summary

| year | `premiums` | diagnosis | care | account | `expenses` | `claim_expenses` | `commissions` | `net_cf` |
|---|---|---|---|---|---|---|---|---|
| 1 | 528,108.3335 | 16,156.8527 | 3,600.8595 | 236.5689 | 329,347.1129 | 270.2400 | 324,000.0000 | -145,503.3006 |
| 2 | 504,685.8326 | 43,865.2474 | 14,139.4730 | 833.3878 | 28,635.6020 | 394.1291 | 15,140.5750 | 401,677.4184 |
| 3 | 486,058.3546 | 46,250.3749 | 17,031.4817 | 1,532.3999 | 28,160.4757 | 446.0625 | 14,581.7506 | 378,055.8094 |
| 5 | 458,838.1313 | 52,319.2751 | 20,775.9723 | 3,266.8413 | 27,720.2984 | 537.3050 | 13,765.1439 | 340,453.2955 |
| 10 | 421,209.1499 | 75,412.9020 | 32,167.3867 | 10,299.0744 | 28,295.7767 | 811.6382 | 12,636.2745 | 261,586.0973 |
| 20 | 377,292.4863 | 150,701.6939 | 72,574.8191 | 48,193.7008 | 31,647.9226 | 1,703.3232 | 11,318.7746 | 61,152.2520 |
| 21 | 0.0000 | 160,367.6591 | 78,181.0999 | 75,494.9085 | 31,870.6249 | 1,818.9219 | 0.0000 | -347,733.2144 |
| 30 | 0.0000 | 253,861.6670 | 128,988.1784 | 79,819.9808 | 31,224.4443 | 2,975.4877 | 0.0000 | -496,869.7581 |
| 40 | 0.0000 | 220,968.4916 | 124,332.8961 | 0.0000 | 24,830.5872 | 2,884.0816 | 0.0000 | -373,016.0565 |
| 50 | 0.0000 | 85,584.8773 | 53,091.1787 | 0.0000 | 11,514.6009 | 1,297.6658 | 0.0000 | -151,488.3227 |
| 60 | 0.0000 | 6,560.8739 | 4,570.4500 | 0.0000 | 1,235.0473 | 119.3753 | 0.0000 | -12,485.7465 |

"diagnosis" is the four `claims_diag_*` columns; "care" is `claims_hosp + claims_surgery +
claims_treat`; "account" is `claims_death + claims_lapse + claims_maturity`. **Year 1 is the
only negative year before 납입완료** and year 21 is the first negative one after it; the
swing across the boundary is **₩408,885.47**, and the projection is negative for the whole
of its second half. The account column goes to zero from policy year 39 because `av_pp` and
`cv_pp` are both exhausted.

### Undiscounted totals over the whole 721-month projection

| Column | Total |
|---|---|
| Σ `pols_if` (sum of the monthly counts) | 366.4984840894 |
| Σ `pols_healthy` | 331.1710420033 |
| Σ `pols_minor` | 11.9942246536 |
| Σ `pols_waived` | 23.3332174325 |
| `premiums` | 8,586,707.2756349239 |
| `claims_diag_gen` | 5,914,035.4962362796 |
| `claims_diag_high` | 185,529.4660782705 |
| `claims_diag_minor` | 1,673,333.4821757083 |
| `claims_diag_similar` | 236,970.6303129040 |
| `claims_hosp` | 824,790.0641291471 |
| `claims_surgery` | 1,408,120.3468910458 |
| `claims_treat` | 1,959,782.9114945314 |
| `claims_death` | 1,262,932.8398376363 |
| `claims_lapse` | 211,242.1285261842 |
| `claims_maturity` | 0.0000000000 |
| `expenses` | 1,712,032.6226109765 |
| `claim_expenses` | 98,964.8080386155 |
| `commissions` | 565,757.9682646699 |
| **`net_cf`** | **−7,466,785.4889610466** |

Groupings worth carrying: diagnosis benefits **8,009,869.07**, care benefits
**4,192,693.32**, account payments (death, lapse, maturity) **1,474,174.97**, all benefit
lines together **13,676,737.37**, expense including claim handling **1,810,997.43**, total
outgo **16,053,492.76**.

Read as **expected counts per policy issued** — each benefit line divided by its own amount,
which is exactly what a once-only fixed-benefit product allows:

| | 일반암 | 고액암 top-up | 특정소액암 | 유사암 | treatment |
|---|---|---|---|---|---|
| expected payments | **0.1971** | **0.0062** | **0.0930** | **0.0395** | **0.1960** |

Against a lifetime cancer risk of **44.6%** for Korean men [R1], and a projection starting at
만나이 40 with lapse and mortality removing two-thirds of the block before expiry, an
expected 0.1971 일반암 payments plus 0.0930 특정소액암 payments is the order the epidemiology
implies. The 유사암 count of 0.0395 is the model's own ledger figure: `similar_avail(720) =
0.9172290909`, so **8.28%** of policies consume the 유사암 tier, and 0.0395 of them do so
while still in force to be paid.

### The equivalence premium on the shipped basis

`product-spec.md` footnote 11 states that ₩45,000 is a modelling input and that these notes'
figure governs. Discounting every line of `result_cf()` at the 예정이율 of **2.50% p.a.**,
with factor `1.025^(−t/12)` applied at the start of month `t`:

    PV premiums at P = 45,000                                     =  6,873,383.677006
    PV of all outgo (benefits, expenses, claim handling, commission)
                                                                  =  8,490,332.868460
    ratio                                                         =  1.2352479168
    PV net_cf                                                     = -1,616,949.191455

The premium annuity is **152.7418594890** months of premium at the anchor cell. Scaling the
premium by that ratio — 45,000 × 1.2352479168 = **55,586.16** — is the obvious first move and
it is **not** the equivalence premium: it is a lower bound, because **three outgo lines are
themselves functions of `P`**. `commissions` is proportional to it; and
`claims_death` and `claims_lapse` are `av_pp` and `cv_pp` multiplied by decrements, so they
ride on the **계약자적립액**, which accrues `prem_alloc_pp = 0.85 P` every month of the
납입기간. Between them those two lines are ₩1,474,175 of the anchor cell's ₩16,053,493 of
undiscounted outgo, and raising `P` raises them. At ₩55,586 the model still leaves PV outgo
₩709,217 above PV premiums.

Solved on the shipped basis — `P` such that PV `net_cf` = 0, every other assumption held —
the **equivalence premium is ₩66,289 a month**. The anchor cell's ₩45,000 is **32.1% below
it**, and that gap is not hidden anywhere: it is why `av_pp` is exhausted at `t = 447` and
why the undiscounted `net_cf` total is −₩7,466,785.49.

**The undiscounted `net_cf` being negative is structural, not an error, even at the
equivalence premium.** Premium is collected for 240 months and cover runs for 720, so an
undiscounted comparison necessarily favours the outgo; only the discounted comparison is
meaningful, and at ₩66,289 it balances by construction.

### Reading the shape of the result

**This is a product whose cost is almost entirely in front of it and whose liability is
almost entirely behind it, and the two statements are about different things.** Year-1
benefit outgo is **₩19,994.28** against ₩528,108.33 of premium — **3.79%** — and that low
figure is the product, not an error. Three things drive it. The first quarter pays nothing
for an invasive cancer at all. The diagnosed population starts empty and is still only
**0.0970%** of the in-force after twelve months, so the three care limbs — which ride on the
diagnosed *stock* — contribute ₩3,600.86 in the whole year. And the 감액기간 halves every
diagnosis benefit for the whole of it.

Against that, the *acquisition* cost is ₩624,000 at `t = 0`, 13.9 months of premium, so the
first year closes at **−₩145,503.30** and the contract does not recover it until the second
year, which closes at **+₩401,677.42**. Twenty years of positive margin follow, declining
monotonically as the incidence curve rises: **+₩401,677 (year 2) → +₩261,586 (year 10) →
+₩61,152 (year 20)**. Then the premium stops and the same block goes on claiming for forty
more years: **−₩347,733 (year 21) → −₩496,870 (year 30) → −₩373,016 (year 40)**, the peak
being reached at about 만나이 70 and the decline thereafter being pure survivorship rather
than any easing in the rate.

**The incidence curve is what does it.** The published male rate rises from **0.001343** at
만나이 40 to **0.008540** at 60 to **0.027892** at 80 — a factor of **20.8** across the
projection [R5] — while the block itself falls only from 1.0000 to 0.3698 over the same
span. So the *expected number of diagnoses per month* rises steeply for fifty years, and the
premium that pays for them is level and stops at year twenty.

**The waiver is the second engine and it runs the same way.** By 납입완료, **3.69%** of the
block is waived and 1.77% is in the 특정소액암 state still paying; by 만나이 80 the waived
state alone is **17.7%** of the in-force. Every one of those lives is being serviced at
₩2,500 a month, inflating at 2%, with no premium against it and every benefit still running.

**And the 유사암 tier is bigger than its ratio suggests at young ages and smaller at old
ones.** At 만나이 40 male, `similar_share = 0.530000` — the 유사암 incidence is 53% of the
invasive base rate — and it pays 20% of the benefit, so its cost weight is `0.530 × 0.20 =
0.106` against a total of `0.820 × 1.00 + 0.180 × 0.60 + 0.030 × 1.00 + 0.106 = 1.064`,
i.e. **10.0%** of the diagnosis cost at that age. At 만나이 60 the share is 0.150000 and at
80 it is 0.050000. Over the whole projection the
유사암 line is **₩236,971 of ₩8,009,869** of diagnosis benefit, **2.96%** — but at female
만나이 30 the same tier's incidence **exceeds the invasive rate it is a fraction of**. That
asymmetry, and not the ratio, is what the reported August 2022 supervisory intervention was
about [R12].

### The other nine model points

Each carries its own approximate equivalence premium at the 2.50% 예정이율, which is why
point 1 is the only cell whose account is exhausted anywhere near the middle of its term.
`ratio` is PV outgo ÷ PV premiums on the shipped basis; every point returns `True` on all ten
`check_*()` cells.

| id | sex / 만나이 | 납입 | `S` | `premium` | `proj_len` | ratio | Σ `net_cf` | what it exercises |
|---|---|---|---|---|---|---|---|---|
| 1 | M 40 | 20년 | 30,000,000 | 45,000 | 721 | 1.2352 | −7,466,785.49 | the anchor; the 기준연령 요건 cell [REG-R9] |
| 2 | F 40 | 20년 | 30,000,000 | 54,000 | 721 | 1.0202 | −5,576,954.27 | the female incidence limb — 2.52× the male rate at 40 — and a much larger 유사암 share |
| 3 | M 40 | 전기납 | 30,000,000 | 62,000 | 721 | 0.8769 | −4,619,382.83 | the **갱신형** chassis: `wait_months = 0`, `reduction_months = 0`, no 면책 and no 감액 [S2] [S4] |
| 4 | F 30 | 20년 | 50,000,000 | 65,000 | 841 | 1.0271 | −9,387,556.77 | the modal **24-month** 감액기간 [S3] [S4] [S5] [S7]; young-female 유사암 exposure |
| 5 | M 15 | 20년 | 30,000,000 | 39,000 | 1021 | 1.0478 | −11,195,873.06 | the minimum issue age and the longest projection, 85 years |
| 6 | M 65 | 10년 | 50,000,000 | 331,000 | 421 | 0.9882 | −5,612,192.29 | the maximum issue age and the shortest projection |
| 7 | F 55 | 전기납 | 30,000,000 | 52,000 | 541 | 0.9206 | −2,356,283.74 | the **diagnosis-only** shape [S3] [S6] [S7]; a 전기납 미지급형 contract has **no surrender value at any duration** [S3 제41조] |
| 8 | M 45 | 20년 | 30,000,000 | 34,000 | 661 | 1.0806 | −3,712,985.12 | the **treatment-cost-only** shape of [S5], `diag_module = 0` |
| 9 | F 50 | 20년 | 100,000,000 | 194,000 | 601 | 0.9568 | −10,552,299.99 | **표준형** surrender basis, no 감액기간, and **no premium waiver** — the diagnosed keep paying and can lapse |
| 10 | M 35 | 30년 | 10,000,000 | 23,000 | 781 | 1.1010 | −4,471,108.86 | the pre-2022 **70%** 유사암 ratio [S8], 24-month 감액, the sum-insured floor |

Points **3, 7, 8 and 10** never exhaust their account. Points 2, 4, 5, 6 and 9 exhaust it
only in the last fifth of their term — 96.9%, 80.6%, 86.5%, 89.5% and 97.3% of the way
through, which on the two long-dated cells (points 4 and 5) still leaves 13.6 and 11.5 years
of cover running on a nil account — against the anchor's **62.1%**. Point 3's ratio of
0.8769 is the clearest statement of what the 갱신형 flag does on the shipped basis:
removing the 면책기간 and the 감액기간 raises the benefit, and paying premium for the whole
term instead of twenty years raises the premium PV far more.

---

## Valuation and reserve pointers

This library projects **gross undiscounted cash flows**. Every valuation layer below consumes
them and is cited, never reproduced. The statutory chain is set out once, on the savings
chassis, in the [whole life technical notes (종신보험)](../whole_life/technical-notes.md);
only what differs for a fixed-benefit 제3보험 contract is repeated here.

- **책임준비금 and the 산출방법서.** 보험업법 제120조 requires the reserve and delegates the
  method [REG-R3]; 감독규정 제6-11조 and the 시행세칙 carry the taxonomy [REG-R10]; and
  제7-64조 makes **현금흐름방식** — cash-flow pricing on 최적기초율 with an adequacy analysis
  — mandatory for a contract longer than three years, which every model point here is
  [REG-R18 제7-64조제1호](#krlib-reg-r18) [R4]. The morbidity assumption inside that filing is the insurer's
  own and is **not published** [REG-R2]; what *is* public is the 참조순보험요율 display this
  model reads [R5] [REG-R61] and the **보험가격지수** the 상품요약서 must carry [REG-R22].
  `Cancer_KR_S` computes neither reserve.
- **해약환급금준비금 — the layer with no counterpart anywhere else in this repository.**
  감독규정 제6-11조의6 requires a reserve, computed **company-wide and not contract by
  contract**, quarantining the excess of the surrender value over the IFRS 17 liability from
  distributable earnings [REG-R11]. On a 순수보장성 cancer contract the gap it quarantines is
  small: the surrender value peaks near 20% of premiums paid and returns to nil [S8]. This
  model computes the surrender value it would consume and not the reserve itself.
- **K-ICS.** 감독규정 제7-1조 and following, live since **2023-01-01**, an economic-value
  regime with a 99.5% confidence level [REG-R13], with transitional measures [REG-R35] and a
  2025 재무건전성 package layered on [REG-R30] [REG-R36]. The two shocks a cancer block feels
  most are the **대량해지** shock, whose 별표 22 detail was **not retrieved** and is
  second-hand through [REG-R36] and therefore **[unverified]**, and the **질병·상해** risk
  module, whose incidence stress this model supplies the *capability* for — a re-runnable,
  parameterized incidence basis — and **not** the statutory magnitude. That distinction must
  not be blurred.
- **IFRS 17 (K-IFRS 제1117호), mandatory since 2023-01-01** [REG-R60]. Two questions this
  product raises and this model does not answer. The **contract boundary** on the 갱신형
  flag: the renewal reprices at the attained age on the basis then in force [S4 제2-11조의6],
  which on the ordinary reading closes the boundary at each renewal, and the model projects
  through it and records the tension. And the **lapse assumption** on the 미지급형 form,
  which the FSS's November 2024 계리가정 ruling addressed precisely because CSM is highly
  sensitive to it and the 무·저해지 share of 보장성 초회보험료 had reached **63.8% by 2024
  H1** [REG-R27].
- **The 최적기초율 chain is where this product's own assumptions are supervised.** 감독규정
  제7-66조제4항 permits the 미지급형 form only where a **최적해지율** was used in pricing
  [REG-R19], and the ruling then fixes the model form [REG-R27]. So the lapse basis in these
  notes is not merely an assumption: it is the condition on which the product may be sold at
  all.
- **Not applicable to this chassis.** 계약자배당 and the surplus-distribution machinery of
  제6-11조의7 and 제6-13조 [REG-R12] do not attach: the composite is 무배당 [S1] [S3] [S8].
  There is no 특별계정, so 제5-6조 and following [REG-R15] are irrelevant — that is
  `VA_KR_S`'s territory.
- **Policyholder protection, not modelled.** 예금자보호법 cover of **₩100,000,000** per
  person per insurer, applied to 보험금 claims in a bucket that expressly **excludes**
  benefits payable because the term has ended [REG-R52] [REG-R25 제43조](#krlib-reg-r25). On this product the
  exclusion is close to costless, because nothing is payable at expiry.
- **Policyholder tax, not modelled.** The premium is a **보장성보험료** and attracts a
  **12% tax credit** on up to ₩1,000,000 a year under 소득세법 제59조의4 [REG-R57] — a
  *credit*, not a deduction, which changes the after-tax comparison against every other
  market in this repository. On the anchor cell's ₩540,000 annual premium the credit is
  ₩64,800. Benefits are not projected net of policyholder tax.
- **The public scheme underneath is why the product is 정액 and not indemnity.** A registered
  cancer patient pays **5% of the total 요양급여비용 for five years** under 국민건강보험법
  제44조제1항 and the 산정특례 기준 [R11], with the 본인부담상한제 of 제44조제2항 above it
  [REG-R53]. With the scheduled bill already capped at 5% there is very little bill left to
  indemnify, which is why every retrieved contract pays a fraction of the 보험가입금액 and
  none of them indemnifies a cost.

---

## Key sensitivities and model risks

In rough order of leverage on a Korean cancer block.

1. **The tier decomposition, not the base incidence rate, is the biggest [std] lever — and
   that is the opposite of what a modeller expects.** The base rate is **sourced and dated**
   [R5] [REG-R61], and its independent cross-check against the registry agrees to **1.6%**
   [R1]. What is standardized is the split into four tiers, and the split moves the answer
   far more than the level does: at 만나이 40 male the model puts 53% of the base rate into
   the 유사암 tier and 18% into 특정소액암, and neither share has a published anchor at that
   age. The **고액암** share is weakest of all — none of 골, 뇌 or 백혈병 appears in the
   retrieved top-ten site table [R1] — and it is also the smallest tier, at **0.0062**
   expected payments per policy against 0.1971 for 일반암, so the error it can do is bounded.
2. **The post-diagnosis survival basis, which a protection model does not have at all.**
   Three benefit streams (inpatient, surgery, treatment) and the entire premium waiver are
   integrals over post-diagnosis survival. The five select-year hazards reproduce the
   published **65.9%** five-year figure exactly [R1], so the *five-year point* is sourced;
   the **grading** across those five years and the **non-zero ultimate** are [std], and they
   are what decide the liability, because 62.1% of the prevalent population is beyond year
   five [R1]. A cure-fraction model moves the liability in one direction only: **up**.
3. **The care intensities, which nothing anchors.** `care_table.csv` is the weakest file in
   the model and **no Korean source publishes cancer admissions, bed-days, operations or
   treatment courses per diagnosed patient** [R5]. Together the three care limbs are
   **₩4,192,693** of the anchor cell's ₩13,676,737 of benefit — **30.7%** — on a table whose
   every row is [std]. The one thing that is bounded is the treatment limb, because 최초
   1회한 and a zero ultimate hazard cap it at one payment per diagnosed life.
4. **The trend risk the pricing basis does not carry, and the source says so.** 「현재도
   예정위험률 산출 시 미래의 추세를 반영하지 않고 있음」 and 「현행 안전할증 수준으로는
   충분하지 않으며 … 일본의 경우 안전할증 설정 시 수준리스크, 추세리스크 등을 모두
   반영하여 산출함」 [R4], against a crude incidence rate that has risen **161% since 1999**
   [R1]. On a 비갱신형 contract written to age 100 that exposure is entirely the insurer's.
   The institute's own account of why the market went 갱신형 is the most useful sentence in
   the research file: 「갱신형으로 상품을 설계하지 않는 한 추세리스크는 항상 존재함」 [R4].
5. **The in-situ trend is a different exposure at a different speed.** The in-situ
   age-standardised rate rose from **9.0 to 71.3** per 100,000 between 1999 and 2023, a
   factor of **7.9**, against 1.30 for the invasive standardised rate; male in-situ rose by a
   factor of **39** [R1]. The 유사암 tier is exposed to a decrement growing at a wholly
   different rate from the one the main tier is exposed to, and the base rate this model
   scales by `similar_share` is an **invasive** rate. The tier's ratio was cut to about 20%
   in August 2022 [R12] precisely because of it — a reported change whose instrument was
   never retrieved.
6. **The waiver makes premium and claims anti-correlated by construction.** Every first
   invasive diagnosis simultaneously starts the benefit stream and stops the premium
   [S3 제14조제1항], and the waived life then cannot lapse. Any error in incidence therefore
   hits both sides of the cash flow at once, roughly **doubling** its effect on `net_cf`.
7. **The 미지급형 lapse assumption is a supervised quantity, and the shape is
   [unverified] at instrument level.** The 0.1% convergence and the 0.8% ultimate are
   verified from the 보도자료 [REG-R27]; the guideline's **functional form** and its
   「실무상 수렴점」 come from an HWP attachment that was never converted, so the log-linear
   shape this model implements is [unverified] at that level. Lapse is also the assumption
   the whole 미지급형 dispensation rests on [REG-R19 제7-66조제4항](#krlib-reg-r19).
8. **The premium is an input with no market anchor.** No carrier publishes a rate table, the
   산출방법서 is not public [REG-R2], the only retrieved price points carry **no
   보험가입금액** [S8], and the consumer-comparison snippets are [unverified]. Every
   profitability statement about the anchor cell is a statement about ₩45,000 **[std]**, and
   about the ₩66,289 equivalence level these notes solve for, not about the market.
9. **The 만나이 / 보험나이 offset is half a year of age, one way.** The tables are read for
   a life on average half a year younger than the contract calls him, and between 만나이 60
   and 70 the published male rate roughly doubles [R5], so half a year is worth about 3.5% of
   the rate. It **understates**, systematically, at every age, and it cannot be corrected
   without a distribution of issue dates within the policy year that no source supplies.
10. **Longevity is the tail risk, twice over.** A lighter mortality basis keeps more lives in
    force to reach the steep part of the incidence curve, **and** keeps more diagnosed lives
    alive to draw care benefits. Both effects raise the liability. The base table is a [std]
    Makeham calibrated to public 기대여명 [REG-R38] and its only external validation is the
    기대수명 check, 80.80 against 80.8 and 86.88 against 86.6.
11. **Expense inflation on a level premium that stops.** ₩2,500 a month against a ₩45,000
    premium is 5.6% of premium at issue and, at 2% inflation, **₩8,041.74** a month in the last
    month of cover — on a policy that has paid no premium for forty years. On the waived
    sub-population it runs with no premium against it from the first diagnosis.

### Known modeling pitfalls

The mistakes a modeller would actually make on this product. Each is specific and checkable,
and each is either asserted by a `check_*()` cells or is a test target in
`tests/test_cancer_kr.py`.

- **There are two waiting periods, not one.** The invasive tiers attach at `t = 3` and the
  유사암 tier at `t = 0` [S1] [S2] [S7]. `claims_diag_similar(0) = 177.9475000000` is the
  only non-zero benefit in the first three rows, and a model that reads one `wait_months` off
  the model point and applies it to all four tiers loses it. At young female ages the error
  is not small: at 만나이 30 the model's 유사암 incidence, 0.001136 a year, **exceeds** the
  invasive base rate of 0.001005 that it is a ratio of.
- **The 면책기간 is a hard zero, not a reduced rate, and it stops the transition as well as
  the benefit.** In months 0, 1 and 2 no invasive diagnosis occurs at all, so `pols_minor(3)`
  and `pols_waived(3)` are **exactly 0.0000000000** and every care line at `t = 3` is
  **exactly zero**. `check_waiting_period()` asserts `claims_diag_gen + claims_diag_high +
  claims_diag_minor + diag_first = 0` for every `t < 3`. Gating only the claim and not the
  transition leaves a diagnosed population that the contract says does not exist.
- **The premium is still charged during the 면책기간.** `premiums(0) = 45,000.0000000000`.
  The 유사암 tier and every non-cancer cover are already in force from day 1, and the
  invalidity rule returns the premium for the affected cover if it bites [S1] [S2] [S3].
  Suppressing the premium and the benefit together is a different product.
- **An in-window diagnosis voids the affected cover; it does not lapse it.** 상법 제644조
  makes the cover **무효** and its premiums returnable [S1 제28조제2항] [R7] — a
  **de-recognition, not a decrement**, which releases the premium already collected as well
  as the future benefit and belongs in a validity adjustment at outset. Putting it in the
  lapse column keeps premium income the insurer never earned. With `void_adjust` switched on
  `void_prob()` is **0.0003357124** at the anchor cell; the base run leaves the adjustment
  off, so the cells returns **0.0** and `pols_if_init()` is exactly 1.0: **state it, do not
  silently absorb it.**
- **`premiums` rides on `pols_healthy + pols_minor`, never on `pols_if`.** At `t = 4` the two
  weights are 0.9839716377 and 0.9840612075 and the difference is ₩4.03; by 납입완료 it is
  3.69% of the block. **It is invisible for the first four rows, where the two are equal**,
  which is exactly why it survives a first-year test. Meanwhile `expenses` **does** ride on
  `pols_if`, because a waived policy is still administered — two weights, two lines, one row.
- **특정소액암 does not waive the premium and 유사암 does not either.** The 약관 says so by
  name: 「특정 소액암 … 은 보험료 납입을 면제하지 않습니다」 [S3 제14조제1항] [S1
  제9조제1항]. Folding the 특정소액암 state into the waived state stops a premium the
  contract goes on charging; at `t = 240` that is **0.0127869424** of the block, 1.77% of the
  in-force, paying ₩45,000 a month for another zero months — and for the twenty years before
  it, real money.
- **A 특정소액암 life can still lapse and a waived life cannot.** `lapse_rate_canc_mth(t)` is
  identically zero under the waiver and the 특정소액암 state carries the full healthy rate.
  Applying one rule to both diagnosed states either deletes claimants or keeps ghosts.
- **고액암 pays *in addition*, not instead.** `claims_diag_gen(3) = 1,360.1145372945` and
  `claims_diag_high(3) = 49.7602879498` are both paid, on overlapping diagnosis flows, so a
  leukaemia collects 200% of `S` and a stomach cancer 100% [S3]. `i_h` is a **subset** of the
  general tier, so `check_tier_shares()` asserts `i_h ≤ i_g` and **not** that the four shares
  sum to one. Treating 고액암 as a fifth slice of a partition halves it.
- **유사암 is additive to the base rate, not a slice of it.** The published grid **excludes**
  기타피부암 (C44) and 갑상선암 (C73) by construction [R5] [REG-R61], which is exactly the
  유사암 boundary, so `similar_share` can and does **exceed 1.0** — 1.60 at female 만나이 20.
  A model that constrains the four shares to sum to one prices the reduced tier out of
  existence at precisely the ages where it dominates.
- **The 감액기간 is a first-year phenomenon, not a benefit scaling.** `reduction_factor(t)`
  is 0.50 for `t < 12` and 1.00 after, and it multiplies the four diagnosis lines and
  **nothing else** — not the inpatient, surgery or treatment limbs, whose real clock runs to
  the 수술일 rather than the 진단확정일 [S4] [S5]. On a 갱신계약 it is disapplied altogether
  [S2] [S4]. Baking 0.50 into the benefit ratio halves the liability for sixty years instead
  of one.
- **Diagnosis lines ride on flows and care lines ride on stocks.** `claims_diag_*(t)` uses
  `n_g`, `n_h`, `n_m`, `n_z` — the month's new diagnoses — and `claims_hosp/surgery/treat(t)`
  uses `pols_diag_dur(t, k)`, the stock at the start of the month. Multiplying a care
  intensity by a diagnosis flow understates the care limbs by the mean diagnosed duration,
  which on this basis runs from 57 at 만나이 50 to 80 at 60 and 148 at 80.
- **The care limbs start one month after the diagnosis limbs.** `claims_hosp(3) = 0` and
  `claims_hosp(4) = 13.6639954092`, because a life diagnosed in month 3 is in the diagnosed
  *stock* from month 4. A model that recognises a treatment episode in the diagnosis month
  shifts the whole care stream forward by a month.
- **The cohort delay is thirteen months, not twelve.** `waived_grad(t, 1)` reads
  `diag_gen(t − 13)`, because the entry month is itself a full month of cohort-1 exposure.
  `check_canc_dur_ledger()` rebuilds cohort 1 independently from the entry history and is the
  only check that fails on an off-by-one here; `check_cancer_roll_fwd()` and
  `check_pols_roll_fwd()` both still close, because the graduation terms telescope.
- **The treatment ledger is per diagnosed life and its ultimate hazard is zero.**
  `treat_avail(k)` is a per-life availability, evaluated at the **midpoint** of select year
  `k`, so `treat_avail(1) = exp(−1.20 × 0.5) = 0.5488116361` and not 1.0. Weighting it by
  `pols_cancer` measures the block's consumption rather than the individual's and defers the
  exhaustion forever; and if the ultimate hazard is made non-zero, the **최초 1회한** bound
  stops holding at long horizons. `check_treat_ledger()` asserts `treat_cum_pp(t) ≤ 1`, which
  on the anchor cell converges to **0.7516253263**.
- **The 유사암 ledger is per policy and rides on `pols_if`, not on `pols_healthy`.** A life
  who has already had an invasive cancer can still collect a 유사암 benefit: no payment
  terminates or exhausts the contract [S1] [S3] [S4]. `check_similar_ledger()` asserts
  `similar_avail(t) + similar_used(t) = 1`.
- **Relative survival is not a mortality table.** [R1] publishes 5년 상대생존율, which nets
  out background mortality — 「관찰생존율을 일반인구의 기대생존율로 나누어 구한 값」 — so it
  converts into an **excess hazard added to** the base table, never into a replacement for
  it. Multiplying survivorship by a relative-survival figure double-counts the background.
  The tell is the five select-year hazards summing to `−ln(0.659)` rather than to anything
  resembling a survival probability.
- **유사암 carries no excess mortality and no care benefit.** 갑상선 five-year relative
  survival is **100.2%** and lifetime 갑상선 mortality risk **0.1%** [R1], so the tier
  appears in **no row** of `survival_table.csv` and produces no diagnosed state. Routing
  유사암 into the diagnosed population credits it with an exposure no retrieved statistic
  measures, and gives it a mortality the registry says it does not have.
- **The 표준해약공제액's 보험가입금액 input is not the ₩30,000,000 headline.** This product
  has no death benefit, so it falls into [별표 15] **제9호** and takes a *notional*
  보험가입금액 by scaling a term assurance's face amount by a risk-premium ratio [REG-R21]
  [REG-R9]. Feeding the headline sum insured into the [별표 14] formula gives
  `459,000 + 300,000 = 759,000` instead of `459,000 + 180,000 = 639,000`, and — because the
  13-month cap of ₩585,000 binds either way [REG-R29] — **the error is invisible on the
  anchor cell and visible on a low-premium, high-sum-insured one.** Test it on model point 10.
- **The step at 납입완료 is not the surrender charge running off.** The 해약공제기간 is
  capped at **7 years** by 제7-66조제1항제2호 [REG-R19], so `surr_chg_pp(t) = 0` from
  `t = 84` — **thirteen years before** the 미지급형 cliff at `t = 240`. Two independent
  mechanisms, thirteen years apart; conflating them puts the cliff in the wrong place on
  every model point whose 납입기간 exceeds seven years.
- **Two prescribed steps land in the same row at `t = 240`.** The surrender value steps from
  nil to ₩4,078,536.79 [S3 제41조] and the lapse rate from 0.1% to 0.8% [REG-R27], and
  `claims_lapse` goes from **₩0.00** to **₩1,891.71**. Implementing one and not the other
  gives a plausible-looking row that is wrong by the whole of the other factor.
- **`claims_lapse` is identically zero for the whole 납입기간, and that is a product fact.**
  `cv_pp(t) = 0` for every `t < 240` on the 미지급형 form, so twenty years of lapses cost
  nothing in cash. On a **전기납** 미지급형 contract — model point 7 — it is zero at *every*
  duration, because the payment period never ends [S3 제41조].
- **There is a payment on death and there is no death benefit.** `claims_death(t) = av_pp(t)
  × pols_death(t)` — the 계약자적립액, required by 감독규정 제7-63조제1항제1호 [REG-R17] and
  the 표준약관 [REG-R25 제22조](#krlib-reg-r25). It is **zero at `t = 0`** because the account is nil, and
  **zero from `t = 447`** because the account is exhausted. Modelling it as a sum assured
  invents a benefit; omitting it drops a regulatory requirement that `LTC_KR_S`,
  `Child_KR_S` and `Medical_KR_S` all inherit.
- **The account recursion is floored at zero and the floor binds.** `av_pp(447) = 0` on the
  anchor cell and stays zero to expiry. A recursion allowed to go negative would carry a
  fictitious asset and would keep paying `claims_death` out of it; one whose floor is
  forgotten produces a negative `claims_death`, which `check_net_cf()` will not catch because
  the identity still balances.
- **`risk_prem_pp` excludes the DEATH and LAPSE lines.** They are payments *out of* the
  account, so including them in the account's own outgo makes the recursion self-referential
  and modelx will raise rather than silently mis-answer — but a hand implementation will not.
- **Nothing is paid at the 100세 계약해당일.** `claims_maturity(720) = 0.00` on a
  `pols_maturity(720) = 0.0103446076` of surviving cover [S8]. A maturity benefit is a
  different product — the 만기환급형 2종 variant returning 5% of 보험가입금액 [S8], which is
  out of scope.
- **`result_cf()` publishes ten `claims_*` split columns and nothing named `claims`.** The
  benefit total is a *cells*, `claims(t, kind)` with `kind` omitted, never a column. A
  statement carrying its own subtotal among its parts is silently non-additive for any reader
  who sums the row, and doubles the benefit side of `check_net_cf()`.
- **Rounded lines do not re-add.** The policy-year-1 claim lines displayed to ten decimals
  sum to a figure that differs from the sum of the unrounded monthly values, and the
  displayed monthly rows do not re-add to the year totals. Assert against the unrounded
  aggregation, never against a sum of displayed figures.
- **`commissions(0)` is 323,999.9999999999 and not 324,000.00.** `0.6 × 12` is
  7.199999999999999 in binary floating point. The notes print the model's value; a test
  written against a hand-cleaned 324,000.00 at ten decimals fails, and correctly so.
- **`proj_len()` is the row count, not the last index.** `result_cf()` has `proj_len()` rows,
  indexed `t = 0 … proj_len() − 1`; the last of them is the expiry row, the one row where
  every cash flow is zero and `pols_maturity` is not. Reading `proj_len()` as the last index
  and sweeping `range(proj_len() + 1)` runs a month past the end of the contract; indexing
  `result_cf()` at `proj_len()` is a `KeyError`. The 보험기간 in months is `proj_len() − 1`,
  which is what `pay_months()` returns on a 전기납 model point.
- **`inc_rate` interpolates log-linearly and `tier_share` linearly, and the two must not be
  swapped.** The incidence grid is published on ten-year ages and rises by a factor of 20.8
  across the projection, so linear interpolation of it understates the mid-decade rate
  materially; the tier shares are bounded ratios anchored at 20 / 40 / 60 / 80 and
  log-linear interpolation of a share that may exceed 1.0 is meaningless. The `provenance`
  column of each CSV says which convention its rows are on.
- **The incidence rows above age 80 are [std] and the model reaches them.** The published
  grid stops at 80; the anchor cell projects to 만나이 100. The 90 and 100 rows are the age-80
  rate × 1.15, flat, and every result at 만나이 80 and above — which is **22.6%** of the
  anchor cell's diagnosis benefit — rests on them.
- **부활 re-runs the 90 days.** A reinstated Korean cancer policy has 90 days of no invasive
  cover in front of it [S1] [S3] [S7]. Modelling reinstatement as a negative lapse restores
  cover the contract does not restore and deletes a real anti-selection control. Lapse is
  absorbing here, and that is the conservative direction.
- **Do not reuse `Medical_KR_S`'s machinery.** There is no 급여/비급여 split, no 자기부담금,
  no annual limit and no 재가입 in this product, and no benefit here is a reimbursement of a
  cost. The one shared mechanic is the 제3보험 requirement to pay the 계약자적립액 on death
  [REG-R17]. Conversely, do not reuse *this* chassis's 면책기간 for `Child_KR_S` without
  inverting it: below 보험나이 15 the 암보장개시일 **is** the 보험계약일 [S2] [R3] [R6].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-cancer-r1
[R10]: #krlib-cancer-r10
[R11]: #krlib-cancer-r11
[R12]: #krlib-cancer-r12
[R3]: #krlib-cancer-r3
[R4]: #krlib-cancer-r4
[R5]: #krlib-cancer-r5
[R6]: #krlib-cancer-r6
[R7]: #krlib-cancer-r7
[REG-R10]: #krlib-reg-r10
[REG-R11]: #krlib-reg-r11
[REG-R12]: #krlib-reg-r12
[REG-R13]: #krlib-reg-r13
[REG-R15]: #krlib-reg-r15
[REG-R17]: #krlib-reg-r17
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R21]: #krlib-reg-r21
[REG-R22]: #krlib-reg-r22
[REG-R27]: #krlib-reg-r27
[REG-R28]: #krlib-reg-r28
[REG-R29]: #krlib-reg-r29
[REG-R3]: #krlib-reg-r3
[REG-R30]: #krlib-reg-r30
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R35]: #krlib-reg-r35
[REG-R36]: #krlib-reg-r36
[REG-R38]: #krlib-reg-r38
[REG-R4]: #krlib-reg-r4
[REG-R48]: #krlib-reg-r48
[REG-R51]: #krlib-reg-r51
[REG-R52]: #krlib-reg-r52
[REG-R53]: #krlib-reg-r53
[REG-R54]: #krlib-reg-r54
[REG-R55]: #krlib-reg-r55
[REG-R57]: #krlib-reg-r57
[REG-R60]: #krlib-reg-r60
[REG-R61]: #krlib-reg-r61
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
