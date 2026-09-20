# Technical Notes

**Status:** Draft, 2026-09-03 (all cited sources accessed 2026-09-03).

**Scope note.** These notes turn the standardized composite critical illness assurance
(*CI boheom*, CI보험, also sold as 중대질병보험 — *jungdae jilbyeong boheom*) of
`product-spec.md` (same directory) into a reference liability cash-flow projection on
paper, and then into `CI_KR_S` beside it. **They describe no single insurer's contract.**
[S#] and [R#] tags resolve against `sources.md`, whose numbering is carried verbatim from
`_research/ci-insurance.md` and is frozen; [REG-R#] tags resolve against the cross-product
reference library `references/regulatory-and-actuarial-references.md`, whose own R1–R60
numbering is separate and also frozen. **[std]** marks a standardization introduced for the
reference implementation; [unverified] marks a claim that could not be confirmed against a
retrieved document. **Every parameter value here is identical to `product-spec.md`'s**, and
every number in the worked example is read off the shipped model rather than recomputed by
hand.

**This document states its deltas against the [whole life chassis
(종신보험)](../whole_life/technical-notes.md) and does not restate it.** The chassis
specifies, once, for the whole library: the 계약자적립액 (*gyeyakja jeongnibaek*, the
policyholder account) recursion and the 예정이율 that accrues it; the 해약환급금
(*haeyak hwangeupgeum*, surrender value) as that account net of a 해약공제액 bounded by the
statutory 표준해약공제액 of 별표 14 [REG-R20] and running off inside seven years [REG-R19];
the 무해지환급형 / 저해지환급형 suppression, the non-marketed 표준형 twin it multiplies and
the step at 납입완료; 보험계약대출 (policy loan) as a modelled state; 보험료 납입면제
(premium waiver) as a state rather than a rate adjustment; 감액; 부활; the 14-day
납입최고(독촉)기간 and the chassis's negative finding that Korea has **no 자동대출납입**, so
that lapse here is behavioural and not funded; and 보험나이 (*boheom nai*, insurance age) as
the age basis. All of it applies here unchanged unless this document says otherwise.

**What is new is acceleration, and it is the whole content of this file.** One decrement
produces **two payments at two dates on one sum assured**. A 중대한 질병 (*jungdaehan
jilbyeong*, "critical" disease) pays a stated fraction — the 선지급 비율, 80% on the
composite — of the 기본보험금 at once; the contract does **not** terminate; the death
benefit becomes the residual complement, floored at 105% of the account; the premium stops;
and the surrender value jumps to its unsuppressed level. Between the two payments the
contract is a genuinely different liability, so the projection carries **two in-force
states**, and the second is indexed by the anniversary it was entered at, because the
residual it carries was fixed at that date.

Five quantities appear here that the specification names but does not fix, because all five
are internal to the decrement and expense construction the specification defers to this
document: the post-CI mortality multiple, the post-CI lapse factor, the breast-cancer share
of 중대한 암, the first-year proration of the 90-day 중대한 암 보장개시일 onto an annual
grid, and the expense and commission basis. Each is **[std]** and each is derived, bounded
or stated as a defect below rather than asserted.

The [term life technical notes (정기보험)](../term_life/technical-notes.md) carry the
protection chassis and the 갱신형 / 비갱신형 split; the [cancer technical notes
(암보험)](../cancer/technical-notes.md) carry the fixed-benefit 제3보험 chassis whose 진단비
riders displaced this product in the market; the [long-term care technical notes
(간병보험)](../long_term_care/technical-notes.md) own the 노인장기요양 등급 inception
construction that this model's `ltc` incidence limb is a placeholder for.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows** per policy — premiums,
  CI accelerations, pre-CI and post-CI death claims, pre-CI and post-CI surrender benefits,
  claim expenses, maintenance and acquisition expense and commission — for a single model
  point, undiscounted and gross of reinsurance. The chassis's three live measurement bases
  — IFRS 17 (K-IFRS 제1117호) [REG-R60], K-ICS [REG-R13] and the 해약환급금준비금 [REG-R11] —
  all consume this stream and none is reproduced. **Discounting, the risk adjustment, the
  CSM, 요구자본 and every reserve are out of scope** and are cited in *Valuation and reserve
  pointers*.
- **Time index.** `t` is **0-based and counts months**: `t = 0` is the first policy month,
  month `t` runs from time `t` to time `t + 1`, the attained age is `x + ⌊t/12⌋`, and the
  contractual **policy year label is `⌊t/12⌋ + 1`**. `T_y = proj_years()` is the number of
  projected policy years and `T = proj_len() = 12 T_y` the number of **months**, the
  exclusive end of the frame, so the projection covers `t = 0 … T − 1` and `result_cf()` has
  `T` rows. A second, **month-end** index runs `0 … T` with 0 at the 계약일 and carries the
  contract's *state* — `V`, `SC`, `W`, `CV`, `CV'`, `B`, `L`, `Δ`, the loan room, and the
  post-CI cohort label `s`. It does not move with the frame: month `t` **opens** at
  month-end `t` and **closes** at month-end `t + 1`, so a claim or a surrender arising in
  month `t`, which falls at the end of it, is paid the month-end-`t + 1` amount. A
  계약해당일 is a month-end `d = 12y`.
  Both are written `t`; every formula below says which one it means, and the `+ 1` is written
  out wherever the two meet.
- **Projection frequency.** **Monthly**, which is the mode every published Korean premium
  scale in the source set is quoted in and the mode the 기준연령 요건 itself names
  [REG-R9]. The annual-step model this replaced leaned on 감독규정 제7-65조제2항, which
  allows the 계약자적립액 of a monthly-premium contract to be computed on an annualised
  premium basis [REG-R18]; that permission is no longer needed.
- **Annual assumptions stay annual; only the grid underneath them is monthly.** Every rate
  the sources tabulate — the 적용위험률, the five-cause CI incidence, the 해지율, the
  납입면제 incidence — is held as the **annual** figure of the policy year the month falls
  in, and its monthly companion applies

      q^m = 1 − (1 − q)^(1/12)     **[std]**

  so that the twelve months of a policy year compound back to exactly the year's tabulated
  rate. Dividing by twelve would not, and on the `log_linear` lapse vector — which spans
  two orders of magnitude — the two conventions differ by 4.9% of the first year's rate.
  Contractual terms quoted in policy years are unchanged and multiplied out where the grid
  needs them: the 납입기간 `12m`, the 해약공제기간 `12 n_sc`, the CI cover period
  `12(100 − x)`, the first-year 감액 over months `t = 0 … 11`, and the loan's 계약해당일.
- **What the monthly grid fixes, and what it still approximates [std].** Three things the
  annual grid could not express, and one it still cannot. (i) The **90-day 중대한 암
  보장개시일** is a *date*: the monthly grid gives no 중대한 암 or 장기요양 cover in months
  0 and 1, a twenty-fifth of a month's in month 2, and all of it from month 3 — where the
  annual grid prorated the whole first year by `1 − 90/365 = 0.7534246575` on the assumption
  that incidence is uniform within it. The twelve monthly factors sum to twelve times the
  annual one, so the wait is **moved, not resized**. (ii) A life accelerating in month `t`
  is paid at the **end** of it — month-end `t + 1` — and joins the post-CI state at the
  **start** of month `t + 1`, so the two payments are one **month** apart where they were a
  year apart; the post-CI cohort is exposed to its own mortality from the month after the
  claim rather than from the next 계약해당일, and the post-CI in-force at the twentieth
  계약해당일 is 1.1% lower for that reason alone. The one-month lag remains deliberate and
  defensible on the contract's own terms: the 장해분류표 defers assessment of a 중대한
  뇌졸중 for **twelve months** after onset [REG-R25 부표 3](#krlib-reg-r25) [S1 별표3], so a
  CI claim and the death that follows are not simultaneous on any grid. (iii) The
  suppression is released at the **month-end** at which the CI event is recognised, and the
  residual is fixed at that month's 기본보험금, which is what 「지급사유 발생 당시」 says.
  What is still **[std]** is the day: the 약관's cancel-and-refund right where 중대한 암 is
  diagnosed before the 보장개시일, and its five-year revival of a pre-inception cancer, are
  not modelled at all [S1 제7조⑤⑥].
- **Timing conventions [std].** Premium at the **start** of each policy month, in advance,
  `t = 0 … 12m − 1`, on the paying pre-CI cohort only; maintenance expense at the start of
  each month and renewal commission on each premium collected from the second policy year;
  acquisition expense and initial commission at issue, the commission computed on the
  **annualised** premium because that is the unit a Korean commission scale is written in;
  **the CI acceleration at the end of the month of the event**; death claims and claim
  expenses at the end of the month of death; surrenders at the end of the month, **after**
  the CI transition and **after** deaths.
- **Age basis: 보험나이**, the chassis's. 보험나이 is the 만 나이 at the 계약일 with a
  fraction under six months discarded and six months or more rounded up, incrementing on
  each 계약해당일 [S1 제26조] [REG-R25 제21조](#krlib-reg-r25). Attained age in month `t` is
  `x + ⌊t/12⌋` **exactly** — the age steps on the 계약해당일 and nowhere else, so one table
  rate holds for the twelve months of a policy year and the floor division is the contract's
  own rule rather than an approximation of it. **The disclosed rate grid this model is built on is itself stated on 보험나이**
  [S3], which is the one respect in which this product's basis is cleaner than the chassis's:
  the chassis calibrates against 만나이 population statistics and carries a known half-year
  bias, while [S3]'s six 예정위험률 rows are contractual-age rates to begin with. The
  national statistics used to sanity-check the constructions — 국가데이터처 생명표 [REG-R38]
  and the 국가암등록통계 [REG-R40] — are still on 만나이, and **no conversion is applied
  [std]**, so every check against them carries the half-year.
- **Two horizons, not one.** Death cover is **종신**; **CI cover ends at the 100세
  계약해당일** [R1] [R13]. The projection therefore has an inner boundary at
  `n_CI = 12(100 − x)` months and an outer boundary at `T = 12(ω − x + 1)` months. Both
  are **counts**: the last CI-covered month is `t = n_CI − 1` and the last projected month is
  `t = T − 1`. On the anchor cell that is `n_CI = 720` and `T = 852`, so CI cover runs
  `t = 0 … 719` and the projection `t = 0 … 851`. `ci_rate(t)` is identically zero from
  `t = 720`; nothing else stops there. A projection that runs the CI decrement to the end of
  the table over-states accelerations at ages the contract does not cover, and a projection that stops
  at `n_CI` throws away eleven years of residual death claims — ₩183,916.56 of them.
- **Terminal age.** `ω = 110` for both sexes, the first age at which the shipped
  `mort_table.csv` reaches `q = 1`. It is a **[std]** choice and it is **not** the chassis's
  115: the two tables are different constructions on different anchors, the chassis's fitted
  to 기대여명 targets from [REG-R38] and this one to [S3]'s three disclosed 예정 경험
  사망률 rates, and neither is a 경험생명표, whose terminal age is not published any more
  than its rates are [REG-R33] [REG-R34]. **The two files must not be swapped.**
- **Currency.** KRW throughout, written ₩ with thousands separators and given in the Korean
  만원 / 억원 convention where a Korean reader would expect it: the anchor's ₩100,000,000 is
  1억원. `run.py` prints `KRW` and pure ASCII.
- **Model points.** Single-policy model points projected on an expected
  (probability-weighted) basis. `point_id` parameterizes `Projection`; **`point_id = 1` is
  the worked-example anchor cell.** **Nine** points ship, one fewer than the chassis's ten,
  because this product has no 금리연동형 base run to exercise — the interest-sensitive CI
  variant exists [S1 제36조] but is carried as a documented variant rather than as a model
  point, the whole of its machinery being the chassis's.
- **Rounding.** Intermediate values at full double precision; displayed cash flows and
  surrender values to **two decimal places [std]**, policy counts to six or ten, rates to
  eight or ten. Rates are displayed as the **annual** figures the sources tabulate wherever
  the notes quote an assumption, and as their monthly conversions wherever the notes trace a
  roll-forward; each table says which. That is the precision `tests/test_ci_insurance_kr.py` asserts.
- **Sign convention.** `net_cf` is **income-positive** — premiums less claims, claim
  expenses, expenses and commission — the library-wide sign, so there is **no**
  outgo-positive `liability_cf` companion.

---

## Model point attributes

| Attribute | Type | Anchor cell (`point_id = 1`) |
|---|---|---|
| `policy_id` | str | `CI-KR-0001` |
| `sex` | enum {M, F} | M |
| `issue_age` (`x`) | int, **보험나이**, 15–60 | **40** |
| `sum_assured` (`SA`) | KRW, ₩10,000,000–₩200,000,000 | **100,000,000** (1억원) |
| `prem_term` (`m`) | int years, 0 for 전기납 | **20** |
| `premium_annual` (`G`) | KRW, level for `t = 0 … m − 1` | **3,680,880** |
| `accel_rate` (`a`) | 선지급 비율, strictly in (0, 1) | **0.80** |
| `cv_floor_ratio` (`k`) | 해약환급금 suppression factor, 1.00 / 0.50 / 0.00 | **0.50** — 저해지환급형 |
| `first_year_scope` | enum {`breast`, `all`} — scope of the first-year 감액 | `breast` |
| `resid_floor_mult` (`c`) | 계약자적립금 floor multiple under the residual | **1.05** |
| `lapse_basis` | enum {`log_linear`, `table`} — the FSS 원칙모형 or the 표준형 curve | `log_linear` |
| `waiver_rate` | 장해 50%+ 납입면제 incidence p.a., during 납입기간 | **0.0003** |
| `pol_loan_util` / `pol_loan_year` | 보험계약대출 take-up fraction, and the **anniversary** of the draw | 0.0 / 0 |
| `mort_adj` | best-estimate multiplier on the table death rate | 1.0 |
| `ci_adj` | best-estimate multiplier on the CI incidence rate | 1.0 |
| `mort_ci_factor` | post-CI mortality multiple | **3.0** |
| `pols_if_init` | policies in force at the start of the first year, `t = 0` | 1 |

**Five of these are the product**, and each is a column rather than a constant for a
reason. `accel_rate` is the choice the whole document turns on and both observed values —
0.50 and 0.80 — appear in every complete 약관 retrieved [S1] [S2] [S3] [S4] [S5] [S6].
`resid_floor_mult` is a carrier and vintage parameter, not a constant: the CI-generation
약관 floor the residual at **105%** of the 계약자적립금 [S1 별표1 주8] and the older
universal version of the same product uses **110%** [S3], which is why `point_id = 9`
carries 1.10. `first_year_scope` distinguishes the CI-generation design, which halves only
for **breast cancer in the first policy year** [S1 별표1] [S2 별표1], from the
GI-generation design, which halves **every** trigger in year one [S4]; it is a flag, not a
separate product, and `point_id = 4` runs it. `mort_ci_factor` is the post-CI mortality
multiple and has no Korean source at all. `waiver_rate` is the **residual** waiver
incidence — the 장해 50%+ limb only — because on this chassis the CI event itself waives
the premium and is already in `ci_rate`.

**There is no issue-date attribute**, for the chassis's reason: the projection runs on
policy years, 보험나이 is fixed at the 계약일, and the two dates inside a year that matter
— the 납입완료일 and the 100세 계약해당일 — are anniversaries by construction. The **90-day
보장개시일 is the exception**, and it is handled by a rate proration rather than by a date.

**`prem_term = 0` denotes 전기납 (종신납)**, in which `m` is the whole projection, the
suppression never lifts by 납입완료 and **the only exit from it is a CI event**. That
configuration is not in the shipped table on this product — every published Korean CI rate
card in the source set quotes a fixed 납입기간 [S3] [S4] — but the code path is the
chassis's and is live.

**The anchor premium is sourced.** ₩306,740 a month is published for exactly this cell —
남 40세, 1억원, 20년납, 월납, 80% 선지급형, 저해지환급형 — and the annual figure is
12 × that = **₩3,680,880 [std]**, no carrier in the set publishing an annual-mode scale
[S4]. The annual premium is therefore slightly overstated relative to a real 연납 rate and
the first year's interest credit correspondingly understated; the direction is stated, not
corrected. On the other eight points the gross premium is this model's own
`prem_net_level_pp()` grossed up by the loading the anchor implies (**1.2399868**, computed
below) and multiplied by the published 저해지-to-기본환급형 form factor — 1.10224 for the
기본환급형 [S4], 1.000 for the 저해지 form the anchor is on, 0.937 for the 무해지 form
**[std]**.

---

## State variables

The chassis carries one in-force count split into a paying and a waived cohort. **This
model carries two states and four counts**, and the split is the delta.

| Variable | Description | Updated |
|---|---|---|
| `pols_if_pre(t)` | `l0(t)` — in force and **pre-CI** at the start of month `t`; `= 1` at `t = 0` | monthly recursion |
| `pols_if_ci_at(t, s)` | `l1(t, s)` — in force and **post-CI**, among those paid at month-end `s` | closed form |
| `ci_surv(t)`, `ci_cohort_entrants(s)` | the shared post-CI survivorship, and a cohort's entry count — what makes that closed form possible | monthly recursion |
| `pols_if_ci(t)` | `l1(t)` — the post-CI cohort in total | monthly recursion |
| `pols_if(t)` | `l(t) = l0(t) + l1(t)` — **total** in force; the first `result_cf()` column | sum |
| `pols_if_pay(t)` | `lp(t)` — of the pre-CI cohort, those still paying in cash | `l0 − lw` |
| `pols_waived(t)` | `lw(t)` — of the pre-CI cohort, those in **납입면제** on the 장해 50%+ limb | monthly recursion |
| `pols_ci(t)` | `C(t)` — accelerations in month `t` | decrement |
| `pols_ci_in(t, s)` | entrants into post-CI cohort `s` in month `t` | allocation |
| `pols_death(t)`, `pols_death_ci(t)` | `D(t)`, `D'(t)` — deaths pre- and post-CI | decrement |
| `pols_lapse(t)`, `pols_lapse_ci(t)` | `S(t)`, `S'(t)` — surrenders pre- and post-CI | decrement |
| `ci_rate(t)` | `q_ci(t)` — the **annual** CI rate of the policy year of `t`, a **first-event rate across the whole trigger set** | table lookup |
| `ci_rate_mth(t)` | `q_ci^m(t)` — its monthly conversion, with the 보장개시일 applied where it falls | closed form |
| `mort_rate(t)`, `mort_rate_ci(t)` | `q(t)`, `q'(t) = q(t) × mort_ci_factor`, both **annual** | table lookup |
| `mort_rate_mth(t)`, `mort_rate_ci_mth(t)` | their monthly conversions — what the roll-forward applies | closed form |
| `lapse_rate(t)`, `lapse_rate_ci(t)` | `w(t)`, `w'(t)` — the **annual** pre- and post-CI surrender rates | assumption |
| `lapse_rate_mth(t)`, `lapse_rate_ci_mth(t)` | their monthly conversions | closed form |
| `pol_val_pp(t)` | `V(t)` — the **계약자적립액** of the 표준형 twin at month-end `t`, on the three-state pricing basis | prospective |
| `surr_chg_pp(t)` | `SC(t)` — the 해약공제액, bounded by the 표준해약공제액 | closed form |
| `cv_std_pp(t)` | `W(t) = max(0, V − SC)` — the 표준형 twin's 해약환급금 | closed form |
| `cv_pp(t)`, `cv_pp_ci(t)` | `CV(t) = κ(t) W(t)`, `CV'(t) = W(t)` — payable pre- and post-CI | closed form |
| `base_benefit_pp(t)` | `B(t)` — the **기본보험금**, itself a maximum of three things | closed form |
| `accel_benefit_pp(s)`, `resid_nominal_pp(s)` | `a B(s)` and `r B(s)` for cohort `s` | closed form |
| `resid_db_pp(t, s)`, `resid_db_avg_pp(t)` | `max(r B(s), c V(t))`, and its in-force mean | closed form |
| `resid_nom_total_pp(t)`, `resid_db_total_pp(t)` | the cohort sums the cash flow actually needs — count times nominal, and count times payable | monthly recursion |
| `loan_pp(t)`, `pol_loan_draw(t)` | `L(t)` — 보험계약대출 balance at time `t`, and the draw at month-end `t` | monthly recursion |
| `loan_avail_pp(t)`, `loan_avail_ci_pp(t)` | the limit off `CV(t)` and off `CV'(t)` — **they differ by 1/k** | closed form |

Four of these carry design decisions that a reader must not skip.

**`pols_if` is the total in force, both states.** It is `l0 + l1`, it is the first column of
`result_cf()`, and it is the weight on maintenance expense. Where these notes write `l(t)`
they mean it; where they mean the pre-CI cohort they write `l0(t)` and the cells is
`pols_if_pre`. A reader coming from the chassis, where there is only one count, will reach
for the wrong one. The `Projection` docstring's symbol map distinguishes all three.

**The post-CI state is indexed by its entry month and this is not tidiness.**
A cohort is labelled `s`, the month-end at which its acceleration was paid, so a life
accelerating in month `t` carries the label `s = t + 1`. The residual a
post-CI policy carries was fixed at **its own** acceleration date, at `r` times the
기본보험금 *then* — 「CI/LTC보험금 지급사유 발생당시의 기본보험금」 [S1 별표1 주8], which
is a date and on this grid a month — and the 기본보험금 grows with the account and with
cumulative premiums [S1 별표1 주7]. Collapsing the post-CI cohort to one average residual
lets a policy that accelerated at duration 3 inherit the larger residual of one that
accelerated at duration 40. On the anchor cell that error is invisible for six years —
every cohort's nominal residual is ₩20,000,000 while the 기본보험금 is flat at `SA` — and
then becomes the whole of the answer, because from the month-end 79 every full cohort is on
the **shared** floor `c V(t)` and from the month-end 730 the 기본보험금 itself starts to
grow.

**The cohort dimension is twelve times longer than the annual grid's, so the aggregates are
carried as their own recursions.** Every post-CI cohort runs the same two decrements, so
the totals the cash flow actually needs — the count `l1(t)`, the nominal sum
`resid_nom_total_pp(t)` and the payable sum `resid_db_total_pp(t)` — roll forward exactly
as a single cohort would, and are computed that way rather than by summing a
(month × cohort) table in every month. The payable sum has a closed form in the two
regimes where `c V(t + 1)` is below every cohort's nominal or at or above all of them, and
falls back to a cohort-by-cohort sum in the window where they straddle it — a year or two
on every shipped point. `pols_if_ci_at(t, s)` itself is written as
`entrants(s) × ci_surv(t) / ci_surv(|s|)`, which is the same number a step-by-step
recursion gives and is what `tests/test_ci_insurance_kr.py` asserts it against.

**The negative labels are the first-year 감액 cohorts, and they are a different amount, not
a different rate.** A breast-cancer claim in the first policy year, months `t = 0 … 11`, is
paid `a f B(t + 1)` at the month-end `t + 1` with `f = 0.5` and leaves a residual of
`(1 − a f) B(t + 1)` — 40% and 60% of the 기본보험금 on the 80% form [S1 별표1]
[S2 별표1]. Its label is `−(t + 1)`, free because nothing can be accelerated at month-end 0
and no full claim carries a negative label. **The monthly grid turns one such cohort into
twelve and empties the first two**, no 중대한 암 being covered before the 보장개시일; the
third carries a twenty-fifth of a month's worth. They are carried as cohorts rather than as
a scaling because their residual, 60% of `SA`, is **three times** every other cohort's and
survives for the whole projection.

**There is exactly one policy value in this model**, `pol_val_pp`, and it is the 표준형
twin's 계약자적립액 — the chassis's architecture, unchanged. The suppression is a
multiplier on the surrender value derived from it, not a second account run. What is new is
that the **multiplier has two exits**, so three surrender values coexist at every duration:
`cv_std_pp` the twin's, `cv_pp` the pre-CI payable one, and `cv_pp_ci` the post-CI payable
one, which equals the twin's at **every** duration.

The base run carries **no policy loan**: `pol_loan_util = 0`, so `loan_pp ≡ 0` and every
`max(0, benefit − L)` is the benefit. It does carry a **non-zero 장해 50%+ waiver** at
0.03% p.a., unlike the chassis's base run, because on this product the waiver is not an
optional module — the CI event itself waives the premium — and the residual limb has to be
visible somewhere.

---

## Assumption inputs

Three classes, kept apart on the chassis's terms and for the chassis's reason: the
보험가격지수 exists precisely because a Korean consumer cannot see the pricing basis
[REG-R22 제7-45조제7항](#krlib-reg-r22), the 산출방법서 is a filed but **unpublished** 기초서류 [REG-R2],
and the November 2024 계리가정 decision draws a hard line between an assumption an insurer
may choose and one the supervisor now sets [REG-R27].

### (a) Contractual / guaranteed elements (cited; the insurer cannot change them)

| Input | Value | Basis |
|---|---|---|
| CI/LTC보험금 | **`a` = 80%** of the 기본보험금, payable **once only** across 중대한 질병 (eight), 중대한 수술 (four), 중대한 화상 및 부식 and 장기요양상태 | [S1 별표1] [S2] [S3] [S4] [S5] [S6]; the 80% choice **[std]** |
| The complement | Residual death benefit `r = 1 − a` = **20%**, exactly. 「사망보험금은 CI/LTC보험금을 수령한 경우에는 기본보험금의 50%(50%선지급형) 또는 20%(80%선지급형) 만 지급합니다」 | [S1]; 50 + 50, 80 + 20, 25 + 75 and 40 + 60 all hold exactly [S1] [S2] |
| The contract survives its own acceleration | 감독규정 제7-60조제8호 — a contract must not be extinguished while the risk it covers remains effective | [REG-R16 제7-60조제8호](#krlib-reg-r16) |
| Residual floor | The later death benefit is 「… 기본보험금의 20%와 … 계약자적립금의 **105%** 중 큰 금액」, so `max(r B(t_CI), c V(s))` with `c = 1.05` | [S1 별표1 주8]; `c = 1.10` on the older universal version [S3] |
| 기본보험금 `B(t)` | `max(기본사망보험금, 이미 납입한 보험료, c × V(t))`, with 기본사망보험금 = 보험가입금액 − 중도인출금액 + 추가납입보험료 | [S1 별표1 주7] |
| 사망보험금, no prior CI | **100%** of `B(t)` | [S1] |
| Premium waiver on a CI event | Any CI/LTC 지급사유 waives all future 기본보험료 | [S1 별표1 주4] [S1 제7조] |
| Premium waiver, residual limb | A **50%** 장해지급률 aggregated across body parts from one accident or one non-accidental cause | [S1 별표1 주4]; scale at [REG-R25 부표 3](#krlib-reg-r25) |
| Suppression carve-out | `k` applies only 「CI/LTC보험금 지급사유가 발생하지 않은 경우」 / 「「선지급 진단보험금」 지급사유 발생 전 납입기간 동안」 — **so the suppression has two exits** | [S2] [S4] |
| 중대한 암 보장개시일 | **90 days** from the 계약일 (or 부활일), counting that day; cover attaches the day after the ninetieth | [S1 제7조] [S1 별표1 주1] [S2] [S3] [S4] |
| Everything else | Covered from the **계약일** — no waiting period on the other seven diseases, the four surgeries or the burn | [S1] [S2 별표1 주1] |
| 장기요양상태 보장개시일 | **90 days**, waived where the state arises directly from a 재해 | [S1 별표1 주2] |
| First-year 감액 | Breast cancer within the first policy year pays **`a f` = 40%**, residual 60%; `f = 0.5` | [S1 별표1] [S2 별표1] [S4] [S5] |
| Survival period | **None**, anywhere. The benefit is payable even where the insured dies of the CI cause | [R1] |
| CI cover period | To the **100세 계약해당일**, while death cover runs 종신 | [R1] [R13]; adoption **[std]** |
| 해약환급금 identity | 계약자적립액 less 미상각신계약비(해지공제액), floored at zero; 「순보험료식 책임준비금에서 미상각신계약비(해지공제액)를 공제한 금액」 in a CI product's own words | [S3]; [REG-R19 제7-66조제1항제1호](#krlib-reg-r19) |
| 표준해약공제액 | 연납순보험료 × 5% × 해약공제계수 + 보험가입금액 × 10/1000, the 계수 being the 보험기간 capped at **20** for a 보장성보험 | [REG-R20 별표 14 주2·주3](#krlib-reg-r20) |
| The 보험가입금액 entering the cap | The **일반사망보험금 before any 증감** — i.e. the **pre-acceleration** ₩100,000,000, not the ₩20,000,000 residual | [REG-R21 별표 15 제3호·제8호](#krlib-reg-r21) |
| 해약공제기간 | 납입기간 or 신계약비 부가기간, **capped at 7년** | [REG-R19 제7-66조제1항제2호](#krlib-reg-r19) |
| Post-acceleration surrender | The **full** 표준형 value at every duration | [S2] [S4] |
| 보험계약대출 | Within the **payable** 해약환급금 net of principal and interest; settled first on every exit | [S1]; [REG-R25 제33조·제26조](#krlib-reg-r25) |
| 예정위험률 revision right | From **5 years**, with 금융위원회 approval; an increase is applied by **reducing the benefit** unless the policyholder funds it | [S3] |
| 자살면책 | **2년** from the 보장개시일, reset on 부활 | [S1 제10조] |
| 부활 restarts the 90-day wait | 「계약일(부활(효력 회복)일)부터」 — so a reinstated contract is uncovered for 중대한 암 for ninety days | [S1 별표1 주1] [REG-R25 제27조](#krlib-reg-r25) |
| 예금자보호 | **₩100,000,000** per person per insurer since 2025-09-01 | [REG-R52] [REG-R32] |

**Two of these rows are the reason this product is a life-insurer instrument.** The
acceleration exists only because 제7-60조제8호 forbids the contract to close on payment
[REG-R16], and it can only be built at all by a carrier that may write 질병사망 as the
주보험 — which a 손해보험회사 may not, so the non-life market's answer to the same disease
list is a 독립급부 특약 with no acceleration in it [R1] [REG-R1].

**And one is a quiet regulatory advantage.** Because the contract covers death from any
cause, 별표 15 제3호 applies directly and the 보험가입금액 entering the 표준해약공제액 is
the **pre-acceleration** death benefit [REG-R21]. The 제3보험 siblings in this library —
[cancer (암보험)](../cancer/technical-notes.md) and [children's insurance
(어린이보험)](../child/technical-notes.md) — have no 일반사망 cover and must construct a
notional 보험가입금액 through 제9호's risk-premium ratio instead. The acceleration form buys
this product a simpler regulatory position than the standalone form would have.

### (b) Insurer-discretionary current elements

| Input | Model value (cells / Reference) | Basis |
|---|---|---|
| 예정이율 `i` (`prem_int_rate`) | **2.50% p.a., 연복리, flat** | Chassis, inherited unchanged **[std]**; equal to the 2026 평균공시이율 [REG-R48]. CI evidence brackets it too far away to be useful: 연복리 4.0% on a 2011 product [S3], 「약 2.75%」 for 종신보험 in 2019 [S4] |
| 최저보증이율 (금리연동형 variant) | 연복리 **1.5%** to ten years, **0.5%** beyond — not modelled | [S1 제36조]; required by [REG-R16 제7-60조제10호](#krlib-reg-r16) |
| 보험계약대출이율 `i_L` (`i_loan`) | **4.00% p.a.** = 예정이율 + 1.5%, compound, a **vintage** rate | Chassis, formula at three carriers; level **[std]** |
| 보험계약대출 limit (`loan_cap_rate`) | **80%** of the **payable** 해약환급금 | Chassis range 50%–85%; pick **[std]**; [REG-R25 제33조](#krlib-reg-r25) |
| Net-premium ratio for the cap (`net_prem_ratio`) | **0.80** — the 연납순보험료 entering 별표 14 is taken as 0.80 × `G` | Chassis ratio **[std]**, so the cap rests on published figures alone |
| 표준해약공제액 coefficients | `surr_chg_rate` 0.05, `surr_chg_coef_cap` 20, `surr_chg_sa_rate` 0.01 | [REG-R20 별표 14](#krlib-reg-r20) |
| 해약공제기간 (`surr_chg_years_cap`) | **7** years, then a straight-line run-off **[std]** | [REG-R19 제7-66조제1항제2호](#krlib-reg-r19); the shape **[std]** |
| Acquisition expense `E0` (`expense_acq`) | **₩500,000** per policy at issue | **[std]** |
| Maintenance expense `e` (`expense_maint`) | **₩60,000** p.a. for life, inflating at 1.0% | **[std]** |
| Claim handling expense `ec` (`expense_claim`) | **₩300,000** per **claim event** — CI, pre-CI death and post-CI death alike | **[std]** |
| Expense inflation `π` (`inflation_rate`) | **1.0% p.a.** | **[std]**; 3% compounds to 7.9 over a 71-year horizon |
| Initial commission `c₀` (`comm_init_rate`) | **0.80** of one annual premium at `t = 0` | **[std]**, below the 1,200% rule [REG-R29] |
| Renewal commission `c_r` (`comm_renewal_rate`) | **3.0%** of premium collected, `t = 1 … m − 1` | **[std]** |
| 계약자배당 | **None.** Every CI product in the retrieved set is 무배당 | [S1] [S2] [S3] |

**Every expense parameter here is [std] and nothing in the source set bounds it from
below.** [S1] names the components — 계약체결비용 and 계약관리비용, the latter split into
유지관련비용 and 기타비용, deducted as part of the 월대체보험료 [S1] — and gives no number;
[S3]'s 예정사업비율 table did not extract. Three public handles bound the construction from
above and the model sits inside all three: the **표준해약공제액** itself [REG-R20], the
**보험료지수 of 130.1%** disclosed at exactly this cell [S3], and the 2019 사업비 reform's
first-year remuneration cap [REG-R29]. The model's own gross-to-net loading is
**1.2399868** — ₩3,680,880 over a net level premium of ₩2,968,483.20 — which is of the same
order as the 130.1% 보험료지수 but is **not** the same ratio, the index being computed
against the 금융감독원's prescribed 표준순보험료 rather than against this model's own net
premium. The agreement is an order check, not a fit.

**The claim expense is charged on the CI event as well as on death**, which the chassis has
no occasion to do. That is a **[std]** decision with a real consequence: on the anchor cell
0.433 accelerations and 0.548 deaths occur per policy issued, so the claim-expense stream is
about **79%** larger than a death-only chassis would produce — 0.981006 claim events per
policy issued against 0.548006 deaths.

### (c) Behavioral / experience assumptions (modeler's view — all [std])

**Korea publishes neither table this product needs, and the reason is structural.** The
제10회 경험생명표, applied from 2024-04, is released only as 평균수명 and 기대여명
[REG-R33] [REG-R34]. The 참조순보험요율 is defined by 감독규정 제1-2조제1호 as the 위험률
the bureau **files** with the supervisor, not as a published table [REG-R4]; the 장기손해보험
참조순보험요율 display that *is* public carries a 「기타피부암 및 갑상선암 이외의 암
발생률」 grid and a 질병입원율 grid [REG-R61] — the first is what `Cancer_KR_S` sources its
incidence from, and the second is what `Medical_KR_S` uses as an external anchor for the *age
slope* of its admission rate and expressly **not** for the level. **Neither reaches this
product**, because the 중대한 암 definition is not the insured-cancer definition that grid is
stated on. What exists is a
single 2011 상품요약서 that prints its 예정위험률 by sex at ages 20, 40 and 60 [S3]. **Both
decrement files in this product are built on it and nothing else.**

[S3]'s grid, reproduced exactly, is the whole public evidence base:

| 예정위험률 (연) | 남20 | 남40 | 남60 | 여20 | 여40 | 여60 |
|---|---|---|---|---|---|---|
| 예정 경험 사망률 | 0.00051 | 0.00068 | 0.00290 | 0.00027 | (0.00068) | (0.00290) |
| 중대한 암 발생률 | 0.000144 | 0.001023 | 0.011063 | 0.000291 | 0.002220 | 0.006010 |
| 중대한 급성심근경색증 발생률 | 0.000027 | 0.000589 | 0.004371 | 0.000009 | 0.000148 | 0.001814 |
| 중대한 뇌졸중 발생률 | 0.000038 | 0.000907 | 0.003999 | 0.000040 | 0.000399 | 0.002764 |

The two parenthesised female mortality values extract **identical to the male ones**, which
is not plausible for a Korean life table and is almost certainly a PDF column-merge
artefact; they are **[unverified]** and are not used [S3].

**Mortality — `mort_table.csv`, sex × attained age 15 … 110.** A **[std]** construction with
a `provenance` column on every row.

| Row kind | Construction | Basis |
|---|---|---|
| **ANCHOR** (male 20, 40, 60) | [S3]'s three disclosed male 예정 경험 사망률 taken as given | [S3] |
| **FIT** (male, to 60) | A Makeham form fitted **exactly** to those three, **in the rate itself and not in the force**: `q(y) = A + B c^y` with `A = 4.960424e−04`, `B = 1.077496e−06`, `c = 1.1371590` | **[std]** |
| **RAMP** (male, above 60) | Log-linear in `q` from the age-60 anchor to `q(110) = 1`: `q(y) = 0.00290 × 1.1240^(y−60)` | **[std]** |
| **FEMALE** (every age) | `q_F(y) = 0.5294 × q_M(y)`, the ratio being [S3]'s own female/male ratio at age 20 (0.00027 / 0.00051) | **[std]** on [S3] |
| **TERMINAL** | `q = 1` at `ω = 110` | **[std]** |

Two properties of this file must be stated rather than discovered. **The old-age shape is a
separate rule, not a continuation**: extrapolated, the fitted Makeham reaches `q = 1` at about
attained age **107** — inside this projection's own horizon, and a third above the shipped
ramp by age 100 (0.412 against 0.311) — so continuing the fit would move ω and the whole
old-age level, and it is not an option. And the female construction is a **known defect**: a
flat ratio gives a 15-to-80 death probability ratio of **0.560** (0.128367 / 0.229205 on the
shipped table) against the **0.500** implied by 국가데이터처's survival to age 80 of 남 64.4% /
여 82.2% [REG-R38], so it **understates the female advantage**. Age 20 is the only usable
female anchor because [S3]'s female rates at 40 and 60 are the corrupted ones.

**CI incidence — `ci_incidence_table.csv`, long form sex × attained age 15 … 100 × cause.**
Five causes, each with its own `provenance` tag, because they do not rest on the same thing.

| Cause | What it covers | Construction |
|---|---|---|
| `cancer`, `ami`, `stroke` | 중대한 암, 중대한 급성심근경색증, 중대한 뇌졸중 | **[S3]** at ages 20, 40 and 60; log-linear in `ln(rate)` between and below; above 60 the 40-to-60 log-slope **decaying geometrically at 0.90 a year** **[std]** |
| `other` | the five remaining 중대한 질병, the four 중대한 수술, 중대한 화상 및 부식 | **10.5%** of the three headline rates **[std]** |
| `ltc` | 장기요양상태 on 노인장기요양 1·2등급 | nil below 65, then `0.0012 × 1.14^(y−65)` **[std]** |

**`other` is the one construction in this file with a derivation rather than a shape.**
[S4] publishes the office-premium step from its 3대보장형 to its 17대보장형 at 남40 / 50% /
기본환급형 — 295,960 to 311,640, a **5.30%** increase — and [S3]'s 보장위험별 연간보험료
disclosure gives the CI benefit **50.6%** of the risk premium at male 40 (₩165,419 of
₩327,136 per 1,000만원) [S3] [S4]. Loading a 5.30% office-premium step onto a benefit
carrying 50.6% of the risk cost implies a **10.5%** uplift on the CI rate, which is the
number the file carries. It is [std] because the step is an office premium and the divisor
is a comparison metric — the two are not the same denominator — but it is a derivation from
two published figures rather than a guess, and it reproduces [S4]'s own headline finding
that **the three headline diseases carry almost all the cost**.

**`ltc` is the weakest limb in the model and is named as such.** The CI research pass
retrieved no 장기요양 1·2등급 inception rate, so the level here is scaled only to the order
implied by [REG-R42]'s 154,688 1·2등급 인정자 (53,844 + 100,844) at an assumed three-year mean
duration, and the shape is proportional where a real inception curve is not. **That is a
finding about this product's own source set and not about Korea**, and the distinction has to
be drawn because it is not true of the library: `LTC_KR_S` sources a **disclosed** 요양 1등급 /
2등급 발생률 grid at ages 40, 50 and 60 by sex from a retrieved 상품요약서, on which the male
1·2등급 rate at 60 is 0.000530 — about 2.5% of this model's total CI rate at that age. This
limb is therefore a **placeholder for the construction
[`LTC_KR_S`](../long_term_care/technical-notes.md) owns**, and holding it at nil below 65 —
together with the 노인성 질병 route below 65 [REG-R55], which is not modelled at all —
**understates the CI decrement at every insured age below 65 by a second-order but non-zero
amount [std]**. On the anchor cell it contributes nothing before `t = 25` and then
becomes the largest single limb at the oldest ages — 0.1033 of a total 0.1586 at age 99 — so a
reader taking any conclusion from the tail of this projection is taking it from this
construction.

**Three properties of the incidence basis are contractual and a modeller must not lose
them.**

**It is a first-event rate across a competing-risk set, not a sum of marginal incidences.**
The benefit is payable **once only** across every trigger [S1 별표1], and Korea's supervisor
required the overlap between CI causes to be priced in rather than ignored: 「국내의 경우
위험률과 담보 간 일치에 대한 규제가 강하고 … CI 질병들 간 중복해서 발생할 수 있는 확률을
최대한 반영한 최종 위험률로 검증받고 사용하였다」 [R1]. Building the table by adding
published site-specific incidences is wrong in exactly the direction the regulation
addresses.

**It already contains the lives who die of the CI cause.** There is no survival period
anywhere in Korean CI, the supervisor having refused one on consumer-protection grounds
[R1], so a life who suffers a qualifying event and dies of it the same week generates
**both** payments. [R1] records that the underlying diagnosis statistics do not capture
those lives, an acknowledged upward bias in exposure that the filed rate absorbs. A model
that imports the overseas 30-day requirement understates the CI decrement and overstates the
death decrement by the same lives.

**The narrowness of 중대한 lives in the level of the rate, not in the prose.** An ordinary
뇌졸중 진단비 rider pays on I60–I63 with no severity condition; the CI trigger adds a
**25% 장해지급률** gate on the statutory 장해분류표 [REG-R25]. An ordinary 암 rider pays on
any C code; the CI trigger removes C44, C61, C73, melanoma at or below T2aN0M0, 대장점막내암,
제자리암 (D00–D09), 경계성종양 and 전암상태 [S1 별표4 Ⅰ]. **How much narrower is not
established** — no Korean population stroke incidence and no CI 부지급률 statistic was
retrieved [R1] — so the model does not apply a narrowing factor to a broader rate. It uses
[S3]'s **already-narrow** disclosed rates directly, which is the only defensible route: the
0.001023 at male 40 is a 중대한 암 rate, not a cancer rate. The check is the registry
arithmetic in `product-spec.md`: 갑상선 is 12.3% of Korean registered cancers and 전립선
7.8%, so those two exclusions alone remove about a fifth of registered incidence before the
rest are taken out [REG-R40].

**Everything else in class (c).**

| Input | Value | Note |
|---|---|---|
| `mort_be_factor`, `ci_be_factor` | **1.00** on every point but `point_id = 9` (0.85 / 0.75) | **[std]**. [S3]'s rates are 예정위험률 carrying a 안전할증 whose regulatory cap was 30%, then 50% from 2015, then removed from 2017 [R1]. **The base run is a valuation-basis run, not a best estimate** |
| Post-CI mortality multiple (`mort_ci_factor`) | **3.00** | **[std]**, and the single largest unsourced number in the file. No Korean post-CI mortality is published; the multiple is anchored qualitatively on 69.6% five-year cancer survival excluding thyroid [REG-R40]. `point_id = 9` runs 2.00 |
| 90-day 보장개시일 (`ci_wait_days`) | **90**: no `cancer` or `ltc` cover in months 0–1, 0.0411 of a month's in month 2, all of it from month 3. The twelve factors sum to `12 × (1 − 90/365) = 9.0410958904` months | The 90 days sourced at four documents [S1 제7조] [S2] [S3] [S4]; placing them by month is arithmetic, not a **[std]** shape |
| First-year 감액 factor (`first_year_factor`) | **0.5** | [S1 별표1] [S2 별표1] [S4] [S5] |
| Breast share of 중대한 암 (`breast_share_m` / `_f`) | **0.005 (M) / 0.268 (F)** | **[std]** on [REG-R40]: 유방 29,871 cases over the female burden less the 19.0% that is 갑상선. A registry share is on 만나이 but a **share** is insensitive to the half-year |
| Pre-CI lapse, `log_linear` basis | `lapse_ll_first` **0.10** → `lapse_ll_target` **0.001** at 납입완료, then `lapse_post_paidup` **0.008** | Endpoints [REG-R27] [R3]; the first-year level **[std]** at the top of a disclosed 적용해지율 envelope; the interpolation **[std]** |
| Pre-CI lapse, `table` basis | `lapse_table.csv`: 0.09 / 0.07 / 0.055 / 0.045 / 0.038 / 0.032, then 0.028 for life | **[std]** 표준형 comparison curve, bounded only by disclosed 적용해지율 envelopes; **no CI lapse experience of any kind was retrieved** [R1] |
| Post-CI lapse factor (`lapse_ci_factor`) | **0.50** of the ultimate rate, i.e. 0.004 flat | **[std]**, and the **direction is genuinely ambiguous** — see *Policyholder behavior modeling* |
| 장해 50%+ waiver incidence | **0.03% p.a.** during 납입기간; **0.05%** on `point_id = 9` | **[std]**. No Korean inception rate at the 50% 장해지급률 threshold is published |
| 보험계약대출 take-up | **0**; a single draw of 50% of the contractual room at the 계약해당일 `d = 144` on `point_id = 7` | **[std]**. No Korean take-up data is public; no repayment is modelled |
| Tolerances | `roll_fwd_tol` = 1e−10 on counts; `val_tol` = 1e−08, scaled by `SA`, on values | conventions |

**The lapse assumption is the chassis's and the inheritance is not free.** 감독규정
제7-66조제4항 permits the suppressed form **only** where the premium was computed
「최적해지율을 사용하여」 — using a best-estimate lapse rate [REG-R19] — so the lapse vector
is a condition of the product's legality and not only an earnings assumption. The November
2024 계리가정 decision makes the **로그-선형 원칙모형** the default, converging to 0.1% at
납입완료 with a 0.8% ultimate, with departure permitted only against audited disclosure of
the CSM, BEL, K-ICS and net-income differences [REG-R27] [R3]. `CI_KR_S` uses it and ships
the 표준형 `table` basis beside it, which is exactly the comparison the guideline requires an
insurer to disclose. **The functional form of the guideline's model is [unverified] at
instrument level**: the 보도자료 values were retrieved and the HWP attachment carrying the
form was not, so the log-linear interpolation between the two endpoints is this library's
reading.

**One delta on the chassis is worth stating: there is no 완납 lapse spike here.** The
chassis wires a mandatory ≥ 30% additional lapse to the 유지보너스 date [REG-R27]; this
product's composite carries no 유지보너스, so no spike is imposed. The eightfold step in
`lapse_rate` at `t = 240` — 0.001 to 0.008 — is produced by the guideline's own shape and is
not an added assumption.

**The whole vector is annual, and the decay runs on the policy year.** `lapse_rate(t)` is
level across the twelve months of a policy year, which is how the guideline states it, and
`lapse_rate_mth(t)` is its uniform-force conversion. The three monthly figures worth having
are 0.0087416110 in policy year 1, 0.0000833716 in the year 납입완료 falls in and
0.0006691237 thereafter; twelve of each compound back to 0.10, 0.001 and 0.008 exactly.

---

## Cash flow components and recursions

### Notation

Defined once, used throughout, identical to `product-spec.md`'s, and carried in the
`Projection` docstring's symbol map.

| Symbol | Meaning | Cells |
|---|---|---|
| `t` | **month**, 0-based: `t = 0 … T − 1`; policy year label `= ⌊t/12⌋ + 1` | `policy_year(t)` |
| `s` | post-CI cohort label — the **month-end** its acceleration was paid at; negative for a first-year reduced cohort | — |
| `x`, `T_y`, `T`, `ω` | 가입나이 (보험나이); `T_y = ω − x + 1` policy years; `T = 12 T_y` **months**; table terminal age | `age_at_entry()`, `proj_years()`, `proj_len()`, `omega_age()` |
| `m`, `12m` | 납입기간 in years; in months, so premiums fall at `t = 0 … 12m − 1`; `m = T_y` on a 전기납 contract | `prem_period()`, `prem_period_mths()` |
| `n_CI` | **number** of CI-covered months, `= 12(100 − x)`; the last is `t = n_CI − 1` | `ci_cover_end()` |
| `n_sc`, `12 n_sc` | 해약공제기간, `= min(m, 7)` years; the same in months | `surr_chg_period_mths()` |
| `SA`, `G`, `G^m` | 보험가입금액; annual 영업보험료 (the commission base); the monthly instalment `G/12`, level for `t < 12m` | `sum_assured()`, `premium_pp()`, `premium_mth_pp()` |
| `a`, `r` | 선지급 비율; residual fraction `r = 1 − a` | `accel_rate()`, `resid_rate()` |
| `c`, `f`, `k` | residual account-floor multiple; first-year 감액 factor; suppression factor | `resid_floor_mult()`, `first_year_factor`, `cv_floor_ratio()` |
| `i`, `j`, `v^m`, `i_L`, `j_L` | 예정이율 and its monthly equivalent; `v^m = 1/(1+j)`; 보험계약대출이율 and its monthly equivalent | `prem_int_rate`, `prem_int_rate_mth()`, `disc_factor_mth()`, `i_loan`, `i_loan_mth()` |
| `q_ci(t)`, `q_ci^m(t)` | the **annual** CI rate, first-event across the trigger set, and its monthly conversion net of the 보장개시일 | `ci_rate(t)`, `ci_rate_mth(t)` |
| `q(t)`, `q'(t)` | pre-CI and post-CI **annual** death rate; `q' = q × mort_ci_factor` | `mort_rate(t)`, `mort_rate_ci(t)` |
| `q^m(t)`, `q'^m(t)` | their monthly conversions — what the roll-forward applies | `mort_rate_mth(t)`, `mort_rate_ci_mth(t)` |
| `w(t)`, `w'(t)` | pre-CI and post-CI **annual** surrender rate | `lapse_rate(t)`, `lapse_rate_ci(t)` |
| `w^m(t)`, `w'^m(t)` | their monthly conversions | `lapse_rate_mth(t)`, `lapse_rate_ci_mth(t)` |
| `u(t)`, `u^m(t)` | 장해 50%+ waiver incidence, annual and converted | `waiver_rate(t)`, `waiver_rate_mth(t)` |
| `φ(t)` | share of month `t`'s accelerations routed to a reduced cohort; nil outside the first policy year | `ci_reduced_share(t)` |
| `A1(t)`, `A0(t)`, `ä(t)` | EPV of the residual post-CI; EPV of all benefits pre-CI; EPV of 1 **a month** while pre-CI | `epv_resid(t)`, `epv_ben(t)`, `annuity_due(t)` |
| `P^m`, `P`, `V(t)` | 월납순보험료 `A0(0)/ä(0)`; its annualisation `12 P^m`; 계약자적립액 at month-end `t` | `prem_net_level_mth_pp()`, `prem_net_level_pp()`, `pol_val_pp(t)` |
| `B(t)` | 기본보험금 | `base_benefit_pp(t)` |
| `SC*`, `SC(t)`, `W(t)` | 표준해약공제액; 해약공제액; 표준형 twin's 해약환급금 | `surr_chg_cap_pp()`, `surr_chg_pp(t)`, `cv_std_pp(t)` |
| `κ(t)`, `CV(t)`, `CV'(t)` | suppression multiplier; payable value pre-CI; payable value post-CI | `cv_mult(t)`, `cv_pp(t)`, `cv_pp_ci(t)` |
| `l(t)`, `l0(t)`, `l1(t)`, `l1(t,s)` | in force total; pre-CI; post-CI; post-CI cohort `s` | `pols_if(t)`, `pols_if_pre(t)`, `pols_if_ci(t)`, `pols_if_ci_at(t,s)` |
| `lp(t)`, `lw(t)` | paying; waived on the 장해 limb | `pols_if_pay(t)`, `pols_waived(t)` |
| `C(t)`, `C(t,s)` | accelerations in month `t`; entrants into cohort `s`, which is `s = t + 1` or `s = −(t + 1)` | `pols_ci(t)`, `pols_ci_in(t,s)` |
| `D(t)`, `D'(t)`, `S(t)`, `S'(t)` | pre-CI deaths; post-CI deaths; pre-CI surrenders; post-CI surrenders | `pols_death(t)`, `pols_death_ci(t)`, `pols_lapse(t)`, `pols_lapse_ci(t)` |
| `L(t)`, `Δ(t)` | 보험계약대출 balance at time `t`, the opening balance of month `t`; the draw at month-end `t` | `loan_pp(t)`, `pol_loan_draw(t)` |
| `E0`, `e`, `ec`, `π`, `c₀`, `c_r` | acquisition expense; per-policy maintenance; claim expense; inflation; initial and renewal commission | `expense_acq`, `expense_maint`, `expense_claim`, `inflation_rate`, `comm_init_rate`, `comm_renewal_rate` |
| `CF(t)` | net cash flow of month `t`, **income-positive** | `net_cf(t)` |

**Dimensional check.** `q`, `q'`, `q_ci`, `w`, `w'`, `u` and their `^m` conversions, and
`a`, `r`, `k`, `κ`, `f`, `φ`, `c`,
`c₀`, `c_r`, `l`, `l0`, `l1`, `lp`, `lw` are dimensionless; `i`, `i_L`, `π` are per annum
and `j`, `j_L` their per-month equivalents;
`A0`, `A1` are ₩ (they carry `SA` inside the recursion) and `ä` is a pure number in
**months** of premium, so `A0 / ä` is ₩ per month; `SA`, `G`, `G^m`, `P`, `P^m`, `V`, `B`,
`SC`, `W`, `CV`, `L`, `E0`, `e`, `ec` are ₩; every term of `CF(t)` is ₩ per policy issued
per **month**. **`c` multiplies a ₩ stock and `a` multiplies a ₩ stock; neither is a rate**,
which is worth saying because both are written as decimals near a page of rates. And every
annual rate in the table above is a **probability**, converted by compounding and never by
dividing — the sister model `LTC_KR_S` divides its transition intensities by twelve for the
opposite reason, those being rates per year rather than probabilities.

### The pricing basis: three states, two annuities that are the same, and one that is not

The chassis prices a two-state contract (alive, dead). This one prices a **three-state**
contract — pre-CI, post-CI, dead — and the recursions are stated forward from the last year
because that is how the model computes them. All three run on the **pricing** decrements,
`ci_rate_base` and `mort_rate_base`, unadjusted by `mort_be_factor` or `ci_be_factor`, which
is what makes the reserve identity testable at all.

    j      = (1 + i) ** (1/12) - 1
    vm     = 1 / (1 + j)

    A1(t)  = vm * [ q'm(t) * r * SA  +  (1 - q'm(t)) * A1(t+1) ]          t = 0 .. T-1
    A1(t)  = 0                                                            t >= T

    A0(t)  = vm * [ q_cim(t) * a * SA
                  + (1 - q_cim(t)) * qm(t) * SA
                  + q_cim(t) * A1(t+1)
                  + (1 - q_cim(t)) * (1 - qm(t)) * A0(t+1) ]              t = 0 .. T-1
    A0(t)  = 0                                                            t >= T

    ad(t)  = 1 + vm * (1 - q_cim(t)) * (1 - qm(t)) * ad(t+1)              t = 0 .. 12m-1
    ad(t)  = 0                                                            t >= 12m

    Pm     = A0(0) / ad(0)

    V(t)   = A0(t) - Pm * ad(t),           V(0) = 0,  V(T) = 0

Every index here is a **month**, and `ad` is measured in months of premium, so `A0/ad` is a
**monthly** net premium. `A0` and `ad` are on the month clock, `V` on the month-end one;
they meet because `A0(t)` and `ad(t)` are both EPVs *at the start of* month `t`, which is
month-end `t`. `V(0) = 0` is the equivalence principle itself and `V(T) = 0` is the empty
tail.

**`P` survives beside `P^m` as its annualisation, `12 P^m`.** It is published so that the
loading can be read against the annual gross the model point carries — both sides of that
ratio being twelve times a monthly figure — and it is **not** an annual-equivalence premium.
On the anchor it is ₩3,051,133.35, which is **2.78% above** the ₩2,968,483.20 the
annual-step model solved for: the ordinary modal effect of paying monthly in advance, since
eleven of the twelve instalments arrive later and are exposed to the year's decrements
before they do. The model point file's premiums were derived from the annual-step figure and
are **unchanged** — they are inputs, not outputs — so the loading the anchor implies is now
**1.2063976173** where it was 1.2399868.

Read `A0` term by term, because each term is a contractual clause. `q_ci · a · SA` is the
acceleration. `(1 − q_ci) · q · SA` is the pre-CI death benefit, paid only to those who did
**not** accelerate first — the ordering is in the pricing basis, not only in the cash-flow
projection. `q_ci · A1(t+1)` is the value of the residual handed to the post-CI state, and
it enters at `t + 1` because the acceleration and the residual death are one step apart.
And `(1 − q_ci)(1 − q) · A0(t+1)` continues the pre-CI state.

**The premium annuity carries the CI decrement.** `ad(t)` discounts on `(1 − q_ci^m)(1 − q^m)`,
not on `(1 − q^m)`, because the premium stops on a CI event as surely as on death
[S1 별표1 주4]. A model that prices a CI acceleration off an ordinary life annuity-due
over-values the premium stream by the whole of the CI decrement — on the anchor cell that is
the difference between `ad(0) = 178.7102998490` months and the ordinary-life value of
**187.9209941962** on the same table, a **5.2%** over-statement of the annuity and a **4.9%**
under-statement of `P^m` (₩241,798.85 against ₩254,261.11).

**Two simplifications inside the pricing recursion are [std] and are stated rather than
hidden.** `A0` values the acceleration at `a · SA` and `A1` values the residual at `r · SA`,
ignoring both the 기본보험금 floors and the **105% account floor** — pricing the second one
in would make `V` self-referential, since the floor is a multiple of `V` itself. Both floors
are applied in full in the cash-flow projection, where `check_resid_floor()` asserts them.
The consequence is quantified in *Key sensitivities*: the reserve is priced on a residual of
₩20,000,000 and the projection pays a residual averaging four times that at long durations.

**The gross premium is an input, not an output**, on the chassis's terms. `G` is the model
point's; the model's own loading ratio is reported and never allowed to drive cash flows.

### 기본보험금 — the floored base every percentage applies to

    B(t) = max( SA - withdrawals + additional_premiums,  cumprem(t),  c * V(t) )
    cumprem(t) = G^m * min(t, 12m)

with 중도인출 and 추가납입 held at **zero [std]** so the first limb is `SA`. They are named
rather than dropped because they are **arguments of the 기본보험금 definition**
[S1 별표1 주7]: a model that silently omits them has changed the benefit definition, not
just the parameterisation.

On the anchor cell neither floor binds for sixty-one years and then the third one does.
`cumprem(240) = ₩73,617,600` never reaches ₩100,000,000, and the monthly grid makes it the
running total it actually is — 이미 납입한 보험료 grows twelve times a year, not once.
`c V(t)` first exceeds `SA` at the **month-end 730** (attained age 100), where
`1.05 × V(730) = ₩100,027,274.71`, and `B` then grows to ₩103,607,571.76 by the month-end
840. `B`, `cumprem` and `V` are all on the month-end clock, so a claim arising in month `t`
is paid off `B(t + 1)`.

The premiums-paid limb is the contractual
form of 감독규정 제7-60조제9호 [REG-R16], whose exception for a 납입기간 ending at age 80 or
below means the rule does not strictly bite here — the floor is market practice that happens
to coincide with the rule.

### The acceleration, the residual, and the two exits from the suppression

    accel_benefit(s)   = a * B(s)                            for s >= 1
    accel_benefit(s)   = a * f * B(-s)                       for s <= -1, reduced cohorts
    resid_nominal(s)   = r * B(s)                            for s >= 1
    resid_nominal(s)   = (1 - a * f) * B(-s)                 for s <= -1
    resid_db(t, s)     = max( resid_nominal(s),  c * V(t) )

Both indices here are **month-ends**: `s` is the month-end the acceleration was paid at,
negated for a first-year reduced cohort, and `t` is the month-end the residual death benefit
is paid at, so a post-CI death in month `t` is paid `resid_db(t + 1, s)`.

`check_accel_complement()` asserts `a B(s) + r B(s) = B(s)` and
`a f B(d) + (1 − a f) B(d) = B(d)` cohort by cohort in every month; exactly two cohorts can
be formed in a month, so the check reads those two and no others. **The acceleration never
adds cover**, and that identity is the one thing in this product that is exact rather than
standardized [S1] [S2].

**The residual floor is two-sided and both limbs must be live.** `resid_db` is a maximum,
not a switch: the nominal binds early and the account binds late, and
`check_resid_floor()` asserts that the paid residual is at or above **both**. On the anchor
cell the crossing is a single **month**: `1.05 × V(78) = ₩19,973,041.04` is below the
nominal ₩20,000,000 and `1.05 × V(79) = ₩20,244,219.60` is above it, so the crossing is the
seventh month of policy year 7 rather than somewhere inside it. From there the residual is
the account and not the stated complement, and by the month-end 469 the in-force mean
residual is **₩86,883,253.97** — 4.34 times the nominal. The first-year reduced cohorts,
whose nominal is three times larger, cross eleven years later, at the month-end **212**.

`check_resid_floor()` is asserted in two forms, because the cohort dimension is now the
acceleration month and a full cohort-by-cohort sweep of every month would be quadratic: the
**aggregate** statement — the total payable residual against the total nominal and against
the floor times the count, which is the same statement summed — in every month, and the
cohort-by-cohort sweep at every 계약해당일.

The 기본보험금 also carries the surrender-value machinery, unchanged from the chassis except
for the multiplier:

    SC*    = net_prem_ratio * G * 0.05 * 20  +  0.01 * SA
    SC(t)  = SC* * (12 n_sc - t) / (12 n_sc)   for t < 12 n_sc, else 0,  n_sc = min(m, 7)
    W(t)   = max( 0, V(t) - SC(t) )
    kappa(t) = k   for t <  12m
    kappa(t) = 1   for t >= 12m
    CV(t)  = kappa(t) * W(t)                pre-CI  payable value
    CV'(t) = W(t)                           post-CI payable value, at EVERY duration

Every line here is on the **month-end** clock, `t = 0 … T`: `SC(0) = SC*` is the whole
charge outstanding at issue and `V(0) = 0`, so `CV(0) = 0`. A surrender arising in month `t`
falls at the end of it and is paid `CV(t + 1)`. The 해약공제액 now runs off in **84 monthly
steps** rather than seven annual ones on the anchor's 20년납 contract, of ₩46,960.76 each,
so the balance deducted is the balance outstanding in the month a surrender is actually
taken; the payable value first becomes positive at the month-end **15**. The 표준해약공제액
itself is unchanged: 별표 14 is written in terms of the 연납순보험료 and this model takes
80% of the **annual** gross, which the monthly grid does not touch.

**`CV'(t) = W(t)` at every duration is the CI-specific delta on the chassis and it is
contractual**, conditioned in [S2] on 「CI/LTC보험금 지급사유가 발생하지 않은 경우」 and in
[S4] on 「「선지급 진단보험금」 지급사유 발생 전 납입기간 동안」. On the chassis the cliff is
a deterministic function of duration and a model can place it at the 계약해당일 `12m`. Here
it is at `min(12m, t_CI)` — **a random date, correlated with the product's own decrement,
and on this grid a month rather than a policy year.**
`check_cv_carve_out()` asserts the consequence the carve-out exists to produce: a CI claimant
is never worse off on surrender than an unaccelerated policyholder at the same duration.

The same carve-out **doubles the policy loan** at the acceleration date, because the limit is
computed off the payable value:

    loan_avail(t)     = loan_cap_rate * CV(t)
    loan_avail_ci(t)  = loan_cap_rate * CV'(t)        = loan_avail(t) / k  while t < 12m
                                                        (month-end clock, like CV)

**The step at 납입완료 is `1 / k` on the same month-end**, not between adjacent periods, and
the monthly grid is what makes the distinction sharp — see the worked example, where
`CV(240) / (k W(240))` is exactly 2.0000000000 while the month-on-month ratio
`CV(240) / CV(239)` is 2.0103. The annual grid's adjacent-period ratio was 2.1290, a
mixture of the step with a whole year of account growth; a month of it is a twelfth as
large, so the step is visibly the whole of the movement. And, as on the chassis, **the step
is not a surrender-charge effect**: `12 n_sc = 84`, so on a 20년납 contract the charge has
been zero for thirteen years by then.

### Decrements, and the state transition

Within month `t`, the CI transition happens **first**, death **second** among those who
did not accelerate, and surrender **third** among those who neither accelerated nor died.
All three rates are the **monthly** conversions.

    C(t)   = l0(t) * q_cim(t)
    D(t)   = l0(t) * (1 - q_cim(t)) * qm(t)
    S(t)   = l0(t) * (1 - q_cim(t)) * (1 - qm(t)) * wm(t)
    D'(t)  = l1(t) * q'm(t)
    S'(t)  = l1(t) * (1 - q'm(t)) * w'm(t)

    l0(t+1) = l0(t) - C(t) - D(t) - S(t)             l0(0) = pols_if_init
    l1(t+1, s) = C(t, s) + l1(t, s) * (1 - q'm(t)) * (1 - w'm(t))
    l1(t+1)    = l1(t) * (1 - q'm(t)) * (1 - w'm(t)) + C(t)
    l(t)       = l0(t) + l1(t)

with the allocation of month `t`'s accelerations to cohorts

    phi(t)     = 0                                             for t >= 12
    phi(t)     = 1                                             if first_year_scope = "all"
    phi(t)     = breast_share * cancer_rate_m(t) / q_cim(t)    if first_year_scope = "breast"
    C(t, -(t+1)) = C(t) * phi(t)                               the reduced cohort
    C(t, t+1)    = C(t) * (1 - phi(t))                         the full cohort

The aggregate `l1(t+1)` is written as its own recursion rather than as a sum over the cohort
table: every post-CI cohort runs the same two decrements, so the two are the same number and
one of them is linear in the horizon where the other is quadratic. The cohort-level
`l1(t, s)` is kept and is a closed form,
`C(s-1, s) × ci_surv(t) / ci_surv(|s|)`, because a cohort has exactly one entry month.

**A life that accelerates in month `t` is paid at month-end `t + 1`, carries the cohort
label `s = t + 1`, and is not exposed to the residual death benefit until month `t + 1`.**
That is a one-**month** lag where the annual grid made it a year, and it is the single
largest number the conversion moves on this product: the post-CI in-force at the twentieth
계약해당일 is 1.1% lower than the annual-step model reported. It is asserted rather than
assumed: `check_ci_state_roll_fwd()` requires the
pre-CI cohort to lose exactly its accelerations, deaths and surrenders **and** the post-CI
cohort to gain exactly the accelerations, at every `t`.

**The CI transition is deliberately not in the total roll-forward.**
`check_pols_roll_fwd()` asserts `l(t) − l(t+1) = D + D' + S + S'` — four exits, not five —
because an acceleration is a **transition**, not an exit, and a policy that accelerates is
still in force. Adding `C(t)` to that identity is the most natural mistake on this product
and it would double-count every CI claimant out of the population.

The 장해 50%+ waiver rides on the pre-CI cohort only, since a CI event waives the premium
anyway:

    lw(t+1) = [ lw(t) + (l0(t) - lw(t)) * um(t) ]
              * (1 - q_cim(t)) * (1 - qm(t)) * (1 - wm(t))
    lw(0)   = 0
    lp(t)   = l0(t) - lw(t)                                    for t < 12m,  else 0

The waived subset stays inside the pre-CI cohort, carries the same three decrements
**[std]** — no Korean source distinguishes the persistency of a waived contract — and keeps
accruing surrender value on the full premium scale, the chassis's 「보험료가 … 정상적으로
납입된 것으로 하여」 rule.

### Benefits, expenses and the loan

    premiums(t)         = Gm * lp(t)                                     for t < 12m

    claims_ci(t)        = sum over s of  C(t, s) * accel_benefit(s)
    claims_death(t)     = max(0, B(t+1) - L(t)) * D(t)
    claims_death_ci(t)  = sum over s of  l1(t,s) * q'm(t) * max(0, resid_db(t+1,s) - L(t))
    claims_lapse(t)     = max(0, CV(t+1)  - L(t)) * S(t)
    claims_lapse_ci(t)  = max(0, CV'(t+1) - L(t)) * S'(t)

    claim_expenses(t)   = ec * ( C(t) + D(t) + D'(t) )
    expenses(t)         = E0 * l(0) * 1{t = 0}  +  e * (1 + pi)^floor(t/12) * l(t)
    commissions(t)      = c0 * G * l(0) * 1{t = 0}
                          +  c_r * premiums(t) * 1{12 <= t < 12m}

    L(0)     = 0
    L(t)     = ( L(t-1) + Delta(t) ) * (1 + jL)
    Delta(t) = pol_loan_util * loan_avail(t)   at t = 12 * pol_loan_year,  else 0

Every benefit falls at the **end** of month `t`, which is month-end `t + 1`, so each
amount is read one step ahead of the row: `B(t+1)`, `CV(t+1)`, `CV'(t+1)`,
`resid_db(t+1, s)`. `L(t)` is the balance the month **opens** with, at time `t`, and the
draw `Delta` falls at the 계약해당일 `12 × pol_loan_year` — the same contractual date the
annual grid used, now located to the month — so a draw carries one **month's** interest in
the month it is taken **[std]**, this model's own arithmetic
and identically immaterial in the base run, where nothing is drawn. The loan rolls on
`jL = (1 + i_L)^(1/12) − 1`, so twelve months compound back to exactly the annual
보험계약대출이율 the 약관 quotes. The **annual** premium survives in the commission line
because that is the unit a Korean commission scale is written in, and the 1,200% rule caps
first-year 모집수수료 at twelve times the monthly premium — one annual premium [REG-R29].

Five of these lines carry a decision.

**`claims_death_ci` respects the cohorts, and gets the answer in one line where it can.**
The residual differs across cohorts whenever the nominal binds — the month-end 78 and
earlier on the anchor's full cohorts, and the month-end 211 on the reduced ones — so an
average will not do. `resid_db_total_pp(t)` is the sum the line needs and is exact in three
cases: the floor below every nominal, in which case the answer is the nominal total; the
floor at or above all of them, in which case it is the floor times the count; and the window
in which they straddle it, where the cohorts are summed one at a time. On every shipped
point that window is a year or two. `resid_db_avg_pp(t)` is published for reading, not for
computing.

**`expenses` is weighted by `l(t)`, the total in force, post-CI included.** A post-CI policy
is still a policy: it is administered, it can surrender, it can claim. Weighting maintenance
expense by `l0(t)` alone would drop **60.1%** of the in-force count at the month-end where
the post-CI share peaks, and 21.8% of the projection's person-months.

**`claim_expenses` is charged on the acceleration too.** Two payments, two claim events, two
handling costs.

**Nothing is netted against the loan except the payments.** The acceleration itself is paid
**gross**, not net of `L(t)`: no retrieved document says the 선지급 is reduced by the loan
balance, and the 표준약관's netting rule speaks to 보험금 payment and to 해지 [REG-R25
제33조](#krlib-reg-r25). That is a **[std]** reading and it is the conservative one for the policyholder; on
`point_id = 7`, the only point with a loan, it is also the reading that keeps the loan
balance intact into the residual, which is where it does bite.

### Processing order (month `t = 0 … T − 1`)

Explicit, because three steps in it are worth money and two are conventions.

1. **Start of month — the two-state split.** `l(t) = l0(t) + l1(t)`. This is the
   `result_cf()` row's `pols_if` and the weight on maintenance expense and claim expense.
2. **Start of month — the 장해 50%+ waiver transition**, out of the paying cohort, before
   the premium is taken.
3. **Start of month — premium.** `G^m × lp(t)` for `t < 12m`, in advance, on the **pre-CI
   paying** cohort only. **The post-CI cohort never pays**, at any duration, because the CI
   event waived it [S1 별표1 주4].
4. **Start of month — expenses and commission.** `E0` and `c₀ G` at `t = 0` on `l(0)`, the
   commission on the **annualised** premium; maintenance `e (1+π)^⌊t/12⌋ l(t)` every month
   for life; renewal commission on the premium actually collected, `t = 12 … 12m − 1`.
5. **Start of month — 보험계약대출 draw**, where one is elected, off the loan room.
6. **Values, at the month-end that closes the month, `t + 1`.** `V(t+1)`, `SC(t+1)`,
   `W(t+1)`, `CV(t+1)`, `CV'(t+1)`, `B(t+1)`.
7. **End of month — the CI transition, first.** `C(t) = l0(t) q_ci^m(t)`, paid `a B(t+1)`
   (or `a f B(t+1)` for the reduced part of the first policy year) **gross of the loan**.
   Entrants take the label `s = t + 1`, or `−(t + 1)` if reduced, and join the post-CI state
   at the **start of month `t + 1`**.
8. **End of month — deaths, second, among those who did not accelerate.**
   `D(t) = l0(t)(1 − q_ci^m)q^m`, paying `max(0, B(t+1) − L(t))`. Post-CI deaths
   `l1(t,s) q'^m(t)` pay `max(0, max(r B(s), c V(t+1)) − L(t))`, respecting the cohorts.
9. **End of month — surrenders, third, among those who neither accelerated nor died.**
   `S(t) = l0(t)(1 − q_ci^m)(1 − q^m)w^m`, paying `max(0, CV(t+1) − L(t))`. Post-CI
   surrenders pay `max(0, CV'(t+1) − L(t))`, the **full** 표준형 value.
10. **End of month — loan roll-up.** `L(t+1) = (L(t) + Δ(t+1))(1 + j_L)`.
11. **Update in force**, per the two-state recursion above.
12. **From `t = n_CI`** the CI decrement is zero; the projection continues. **In the
    terminal policy year** the table's rate is 1 and `q^m(t) = 1/(12 − t mod 12)` spreads
    that certain death evenly over its twelve months, so `l(T) = 0` and `V(T) := 0`.

**"CI before death before lapse" is a [std] ordering and it is not neutral.** Reversing the
first two would apply the death rate to the full pre-CI count and route lives that would
have accelerated into the death decrement, which on [S3]'s three disclosed rates is a
decrement 3.7 times smaller at male 40 and 6.7 times smaller at male 60 [S3] — 4.09 and 7.40
times on this model's own five-cause rate. It is stated here, asserted by
`check_ci_state_roll_fwd()`, and should be the first thing a reader checks against their own
convention.

**The account recursion runs on its own clock** — the month-end one, 0 at issue. `V(t)`
is a function of that index, `P^m`, `j`,
`q_ci^m` and `q^m` alone — **not of `l`, `l0`, `l1`, `w` or `u`**. It is a per-policy
contractual quantity, so the decrements' *incidence* enters it through the pricing basis and
the decrements' *population* does not.

### Net cash flow

Income-positive, per policy issued:

    CF(t) =   premiums(t)
            - claims_ci(t)
            - claims_death(t)
            - claims_death_ci(t)
            - claims_lapse(t)
            - claims_lapse_ci(t)
            - claim_expenses(t)
            - expenses(t)
            - commissions(t)

`result_cf()` publishes exactly these as, in order, `pols_if`, `premiums`, `claims_ci`,
`claims_death`, `claims_death_ci`, `claims_lapse`, `claims_lapse_ci`, `claim_expenses`,
`expenses`, `commissions`, `net_cf` — `pols_if` first, `net_cf` last, **no `claims`
subtotal column**, so the columns sum exactly to `net_cf`. The `claims(t, kind)` cells
stays, with `kind` in {`CI`, `DEATH`, `DEATH_CI`, `LAPSE`, `LAPSE_CI`}, and
`check_net_cf()` asserts the ledger at every `t`.

**The five-way claims split is the point of the publication order.** A three-column
statement — premiums, claims, expenses — would hide the entire subject of this document,
which is that `claims_ci` and `claims_death_ci` are two payments arising from **one**
decrement at two different dates, and that on the 80% form the second is the larger of the
two.

**Nine identities close the projection.** Each `check_*()` takes no argument and returns a
bool over all `t`, with the per-`t` signed residual at `check_*_resid(t)`. All nine are
`True` on all nine model points.

| Check | The identity | What breaks it |
|---|---|---|
| `check_pols_roll_fwd` | `l(t) − l(t+1) = D + D' + S + S'` — **four** exits | putting the CI transition in the identity |
| `check_ci_state_roll_fwd` | the pre-CI cohort loses exactly `C + D + S` **and** the post-CI cohort gains exactly `C` | a policy leaving one state and not arriving in the other |
| `check_decrement_sum` | every policy issued leaves by a modelled decrement | a residual population, a tail state |
| `check_pol_val_roll_fwd` | `(V(t) + P^m·1{t<12m})(1+j)` = the month's expected outgo plus `(1−q_ci^m)(1−q^m)V(t+1)` | the CI decrement left out of the premium annuity, or an annual rate where its conversion belongs |
| `check_accel_complement` | `a B + r B = B`, and `a f B + (1 − a f) B = B`, cohort by cohort | an acceleration that adds or destroys cover |
| `check_resid_floor` | the residual is at or above **both** `r B(s)` and `c V(t)` — in aggregate every month, cohort by cohort at every 계약해당일 | a one-sided max, or the floor read off the wrong month |
| `check_cv_carve_out` | `CV'(t) ≥ CV(t)` at every `t` | the suppression applied to the post-CI cohort |
| `check_loan_roll_fwd` | `L(t+1) = (L(t) + Δ(t+1))(1 + j_L)` | a balance not accumulating at the monthly equivalent of `i_loan` |
| `check_net_cf` | `net_cf` equals the sum of the published `result_cf()` columns | a benefit kind missing from the statement |

Tolerances: `roll_fwd_tol = 1e−10` on the count identities, `val_tol × SA = 1e−08 × SA` on
the value identities.

### Optional modules (all off in the base run)

| Module | Switch | Base | Exercised on |
|---|---|---|---|
| 보험계약대출 | `pol_loan_util`, `pol_loan_year` | 0 | `point_id = 7`, 50% of the room at the 계약해당일 `d = 144` |
| 50% 선지급형 | `accel_rate` | 0.80 | `point_id = 3` (기본환급형) and `8` (저해지) |
| 무해지환급형 / 기본환급형 | `cv_floor_ratio` | 0.50 | `point_id = 4` (`k` = 0.00), `3` and `6` (`k` = 1.00) |
| All-trigger first-year 감액 | `first_year_scope` | `breast` | `point_id = 4` |
| 표준형 lapse curve | `lapse_basis` | `log_linear` | `point_id = 3`, `6`, `8` |
| 110% residual floor | `resid_floor_mult` | 1.05 | `point_id = 9` |
| Best-estimate levers | `mort_adj`, `ci_adj`, `mort_ci_factor` | 1.00 / 1.00 / 3.00 | `point_id = 9`, at 0.85 / 0.75 / 2.00 |

**Nothing in this list is a placeholder**, and the 장해 50%+ waiver is deliberately not in
it: it runs on **every** shipped point — at 0.03% p.a. on eight of the nine and at 0.05% on
`point_id = 9`, which carries the alternative level so that it too is exercised somewhere —
because on this product the waiver is part of the main contract rather than an option
[S1 별표1 주4].

**Not modelled, and named so that it is not mistaken for absent.** 중도인출 and 추가납입,
held at zero although they are arguments of the 기본보험금 definition [S1 별표1 주7]; 부활
and the 90-day cancer wait it restarts [S1 별표1 주1]; the pre-inception cancer carve-out and
its five-year revival [S1 제7조⑥]; the 예정위험률 revision right, which takes effect as a
**benefit reduction** rather than as a lapse [S3]; 가지급제도 [S1 제13조]; 감액; 연금전환,
which appears in no retrieved CI 약관; the 다중지급 (multi-pay) generation [R1]; the 100%
선지급플러스형, which is not a pure acceleration because it replaces the residual with a
separately funded 유족위로금 [S4]; the 80세 two-period design of the 2002 product [S6] [R1];
and the chassis's clawback, whose interaction with the CI carve-out is **[unverified]** —
`CI_KR_S` assumes it does not gate it. No 요구자본 anywhere.

---

## Policyholder behavior modeling

All dynamic forms are **[std]** reference constructions, and on this product the evidence
base is thinner than on the chassis: **no CI lapse experience of any kind was retrieved**
[R1].

- **Pre-CI surrender.** The `log_linear` vector of class (c): 10% in year 1 decaying
  log-linearly to 0.1% at 납입완료, then 0.8% for life, the FSS 원칙모형 [REG-R27] [R3].
  The decay constant is `λ = ln(0.10/0.001)/(m − 1) = 0.2423773782` on the anchor and runs
  on the **policy year**, so the annual rate is level across the twelve months of a year and
  `w = 0.10` in policy year 1 and `0.001` in policy year 20 are exact by construction; the
  monthly decrement is `1 − (1 − w)^(1/12)`, which is 0.0087416110 and 0.0000833716. The
  표준형 `table` basis
  runs beside it, and the two produce **materially different products**: re-running the
  anchor on a level 4% rate through the 납입기간, the 0.8% post-완납 ultimate unchanged,
  gives an undiscounted `Σ net_cf` of **−₩34,030,199.11** against the base run's
  **−₩51,625,819.94**, a third of the whole liability, because a higher lapse rate removes
  lives before the acceleration reaches them.
- **Post-CI surrender is the assumption whose *direction* is unknown.** `lapse_ci_factor` is
  **0.50** of the ultimate rate, i.e. 0.004 flat, and the argument runs both ways with equal
  force. A CI claimant has just received 80% of the sum assured in cash, has no premium to
  pay, and holds a contract whose surrender value has doubled — every one of which is a
  reason to surrender. Against that, the claimant is uninsurable elsewhere, the residual is
  now floored at 105% of a growing account, and the contract costs nothing to keep. **No
  Korean source settles it.** Setting the factor to 1.00 instead of 0.50 moves the
  undiscounted `Σ net_cf` from −₩51,625,819.94 to **−₩51,275,060.15**, a 0.7% swing on the
  whole liability, so the level does not matter much in aggregate; **the sign of the
  behavioural story does**, and it is unresolved.
- **The 환급률 crossing is not modelled as a driver.** On the chassis the economically
  natural dynamic-lapse trigger is the refund ratio crossing 1. Here there are **two**
  candidate triggers — the refund ratio, and the CI event itself, which doubles the value
  overnight — and no dynamic form is shipped for either **[std]**. The reason is the
  chassis's: the November 2024 decision fixes the base vector, and a dynamic overlay on a
  supervised assumption is a departure requiring the full disclosure regime [REG-R27]. The
  hook is `lapse_rate(t)` and `lapse_rate_ci(t)`; a user adding one changes no other formula.
- **The premium waiver is not an independent decrement on this chassis, and that is a
  simplification with a direction.** A CI event waives the premium [S1 별표1 주4], so on
  essentially every CI claim the waiver and the acceleration fire together and the waiver is
  already inside `ci_rate`. What remains is the 장해 50%+ limb, at 0.03% p.a. **[std]**.
  **But the trigger sets are of different widths and the model uses one rate for the narrow
  one.** [S4]'s GI product waives on a 50%+ disability **or** on 암 including 특정암 (breast
  and prostate, which it does **not** accelerate), 뇌출혈, 급성심근경색증, 중증질환, 중대한
  화상 및 부식 or a 중대한 수술 [S4]; one carrier advertises **25** distinct waiver triggers
  [R11]. A modern Korean accelerated product therefore has **a narrow trigger set for the
  money and a wide one for the premium waiver**, and this model has only the narrow one. The
  waiver incidence is understated by the whole of the difference, which is unquantified.
- **보험계약대출 take-up is static and the loan does not terminate the contract.** A single
  draw of a chosen fraction of the contractual room at a chosen year, no repayment, and the
  balance netted off every payment except the acceleration and floored at zero. Korea has no
  loan-excess-lapse notice [REG-R25], so the balance can only absorb a payout. **What is new
  here is that the room itself doubles on a diagnosis**: on `point_id = 7` at the
  계약해당일 `d = 144` the pre-CI limit is ₩23,945,646.45 and the post-CI limit at the same
  duration is ₩47,891,292.89.
- **부활 is not modelled and the omission is larger here than on the chassis.** 부활 within
  three years restarts the **90-day 중대한 암 보장개시일** [S1 별표1 주1], so a reinstated CI
  contract is uncovered for cancer for ninety days — a decrement the chassis has no
  counterpart for, and one the monthly grid could now express exactly as
  :func:`ci_wait_factor_mth` expresses the original. There is no reinstatement switch in `CI_KR_S`: omitting 부활 altogether
  understates later-duration in force and therefore both premium income and claims, and it
  also removes a real ninety-day gap in cover. Both biases are stated rather than corrected
  because no Korean reinstatement rate was retrieved.
- **The pre-inception cancer carve-out is a state this model does not have.** A cancer
  diagnosed before the 보장개시일 puts the policyholder in a position where the premium is
  **not** waived and the cancer is **not** covered, with cover reviving only after five
  claim-free years [S1 제7조⑥] [S1 별표1 주5]. It is a third in-force state with its own
  economics and it is out of scope; a policyholder in it pays premiums on cover they cannot
  claim.
- **면책 incidence is zero in the base run [std], and refusal is not forfeiture.** The
  chassis's finding carries over: where a claim is refused for an 면책사유 the insurer must
  still pay 「보험수익자를 위하여 적립한 금액」 [REG-R50 제736조](#krlib-reg-r50) [REG-R25 제22조](#krlib-reg-r25). **On this
  product the refusal rate is the whole consumer story** — the 중대한 definitions are the
  most litigated wording in the Korean market [R5] [R6] [R7] [R10] [R16] — and **no Korean CI
  부지급률 statistic exists in any retrieved source** [R1]. A model that treated a refused CI
  claim as a zero-payment event would be wrong by the amount of the account, not by the
  amount of the claim.

---

## Worked example

### The anchor cell

**`point_id = 1`, `CI-KR-0001`** — 남자, 보험나이 **40세**, 보험가입금액 **₩100,000,000
(1억원)**, 보험기간 **종신** with **CI 보장 to the 100세 계약해당일**, 납입기간 **20년**,
월납, **80% 선지급형**, **저해지환급형 `k = 0.50`**, first-year 감액 scope
`breast`, residual floor `c = 1.05`, lapse basis `log_linear`, monthly premium
**₩306,740** (annual ₩3,680,880). `T_y = 110 − 40 + 1 = 71` policy years and `T = 852`
months, `t = 0 … 851`, attained 보험나이 40 to
110; `n_CI = 12 × (100 − 40) = 720` months of CI cover, `t = 0 … 719`. The policy loan is
off (`pol_loan_util = 0`), the best-estimate levers are at 1.00, and the 장해 50%+ waiver
runs at 0.0003 p.a.

**Assumption values used, in full.** `i = 2.50%` **[std]**, the chassis's, on a disclosed
2.25%–2.75% band and equal to the 2026 평균공시이율 [REG-R48], with monthly equivalent
`j = 0.0020598362698427`; `q` from `mort_table.csv`
남 at attained 보험나이 with `mort_be_factor = 1.00`, a **[std]** Makeham fit to [S3]'s
three disclosed anchors; `q' = 3.00 q` **[std]**, applied to the **annual** probability and
then converted; `q_ci` from `ci_incidence_table.csv`
summed over five causes with `ci_be_factor = 1.00`, **[S3]** at ages 20, 40 and 60 and
**[std]** elsewhere; the 90-day 보장개시일 applied **month by month** to the `cancer` and
`ltc` limbs, sourced at four documents
[S1 제7조] [S2] [S3] [S4]; `w` the `log_linear` vector, endpoints [REG-R27] [R3] and the
interpolation **[std]**; `w' = 0.50 × 0.008 = 0.004` **[std]**; `u = 0.0003` **[std]** —
every one of those five an **annual** rate, converted by `1 − (1 − q)^(1/12)`;
`f = 0.5` [S1 별표1] [S2 별표1]; `breast_share_m = 0.005` **[std]** on [REG-R40];
`SC*` from 별표 14 [REG-R20] with the 7-year 해약공제기간 of [REG-R19] and a **[std]**
straight-line run-off over 84 months; `E0 = ₩500,000`, `e = ₩5,000` **a month** inflating at
1.0% a year on the 계약해당일, `ec = ₩300,000` per claim event, `c₀ = 0.80` of the annual
premium, `c_r = 3.0%`, all **[std]**; `i_L = 4.00%` with monthly equivalent
`j_L = 0.0032737397821989`, unused here because `loan_pp ≡ 0`.

**Derived scalars, at full precision.**

| Quantity | Cells | Value |
|---|---|---|
| Terminal age ω | `omega_age()` | **110** |
| Projection length, in policy years | `proj_years()` | **71** |
| Projection length `T`, in **months** | `proj_len()` | **852** (`t = 0 … 851`) |
| CI-covered months `n_CI` | `ci_cover_end()` | **720** (last is `t = 719`, attained age 99) |
| 납입기간 `m`, `12m` | `prem_period()`, `prem_period_mths()` | 20 years, **240 months** |
| 해약공제기간 `n_sc`, `12 n_sc` | `surr_chg_period_mths()` | 7 years, **84 months** |
| `v^m` | `disc_factor_mth()` | 0.9979443979338495 |
| `A0(0)` | `epv_ben(0)` | **₩45,439,079.6117764339** (0.454391 × `SA`) |
| `A1(0)` | `epv_resid(0)` | ₩8,242,810.7636089316 |
| `ä(0)`, in **months** of premium | `annuity_due(0)` | **178.7102998490** |
| 월납순보험료 `P^m` | `prem_net_level_mth_pp()` | **₩254,261.1122592268** |
| its annualisation `P = 12 P^m` | `prem_net_level_pp()` | ₩3,051,133.3471107213 |
| 영업보험료 `G^m`, `G` | `premium_mth_pp()`, `premium_pp()` | **₩306,740.00** a month; ₩3,680,880.00 a year |
| Gross-to-net loading `G / P` | — | **1.2063976173** |
| **표준해약공제액** `SC*` | `surr_chg_cap_pp()` | **₩3,944,704.00** |
| 선지급 비율 `a` / residual `r` | `accel_rate()`, `resid_rate()` | 0.80 / 0.20 |
| Breast share of 중대한 암 | `breast_share()` | 0.005 |
| 보장개시일, first policy year | `sum ci_wait_factor_mth(t)`, `t < 12` | **9.0410958904 months** = 12 × (1 − 90/365) |
| Ultimate pre-CI lapse | `lapse_rate_ult()` | 0.008 |

`P^m × ä(0) = 254,261.1122592268 × 178.7102998490 = ₩45,439,079.61` reproduces `A0(0)` to
the won, which is the equivalence principle asserted rather than assumed. **`ä(0)` is in
months**, so the premium it solves for is a monthly one.

**`P` is 2.78% above the annual-step model's own net premium** of ₩2,968,483.20, which is
the ordinary modal effect of paying monthly in advance: eleven of the twelve instalments
arrive later and are exposed to the year's decrements before they do. The model point file's
premiums were derived from that annual figure and are **unchanged** — they are inputs, not
outputs — so the loading the anchor implies is 1.2064 where it was 1.2400, and the file's
own construction rule is asserted in `tests/test_ci_insurance_kr.py` against the
annual-equivalence premium it was written on.

**The 표준해약공제액 arithmetic, in one line, from published figures alone:**

    SC* = 0.80 * 3,680,880 * 0.05 * 20  +  0.01 * 100,000,000
        = 2,944,704.00 + 1,000,000.00  =  KRW 3,944,704.00

against the FSC's 「보장성보험 월 보험료의 13배 수준」 rule of thumb of
13 × ₩306,740 = **₩3,987,620** — the two independent statements of the same cap agree to
**1.1%** [REG-R20] [REG-R29]. 별표 14 is written in terms of the **연납순보험료** and this
model takes 80% of the annual gross, so the cap is untouched by the conversion; the monthly
grid changes only the number of steps it runs off in, 84 of **₩46,960.7619047619** each.

**Floating-point note.** `resid_rate()` is computed as `1.0 − 0.8` and is therefore
`0.19999999999999996` in binary; `resid_nominal_pp(s)` prints as ₩19,999,999.9999999963.
It is the exact complement in the sense the model asserts — `check_accel_complement()`
closes to `1e−08 × SA` = ₩1 — and it is written **₩20,000,000** throughout this document.

### Two cross-checks that fell out of the model rather than being imposed

| Quantity | Model | Published | Gap |
|---|---|---|---|
| 80% form net premium ÷ 50% form, 남 40 | **1.0782** | **1.085** [S4] | 0.7% |
| 표준해약공제액 at the anchor | **₩3,944,704** | ₩3,987,620 on the 13× rule [REG-R29] | 1.1% |

The first is the more interesting of the two, because nothing in the construction was fitted
to it. Re-running the pricing recursion with `a = 0.50` on the same table gives
`A0(0) = ₩42,142,821.74` and `P^m = ₩235,816.41`, so the 80% form costs **1.0782** times the
50% form; [S4]'s published 144-cell grid gives 338,100 / 311,640 = **1.085** at 남40 / 17대 /
기본환급형. Two independent routes to the price of thirty percentage points of acceleration
agree to seven parts in a thousand.

**And one that does not agree, stated as such.** The gross-to-net loading of **1.2064** sits
beside a disclosed 보험료지수 of **130.1%** [S3]. They are not the same ratio — the index is
computed against the 금융감독원's prescribed 표준순보험료, this is against the model's own
net premium — so the agreement is one of order only, and neither figure was used to
calibrate the other.

### The decrement basis at the anchor, policy years 1 … 25

The unsuffixed columns are the **annual** rates the sources tabulate; the `^m` columns are
the monthly conversions the roll-forward applies, and twelve of each compound back to the
annual figure exactly. Read at the **last month of each policy year**, which is where the
90-day 보장개시일 of the first three months does not interfere. `q_ci` is the sum of five
causes; `q' = 3.00 q` on the annual probability; `w'` is flat at 0.004.

| policy year | age | `ci_rate` | `ci_rate_mth` | `mort_rate` | `mort_rate_mth` | `mort_rate_ci` | `lapse_rate` | `lapse_rate_mth` |
|---|---|---|---|---|---|---|---|---|
| 1 | 40 | 0.0027834950 | 0.0002322544 | 0.00068000 | 0.0000566843 | 0.00204000 | 0.1000000000 | 0.0087416110 |
| 2 | 41 | 0.0030721810 | 0.0002563763 | 0.00070525 | 0.0000587898 | 0.00211575 | 0.0784759970 | 0.0067873987 |
| 3 | 42 | 0.0033921090 | 0.0002831162 | 0.00073395 | 0.0000611831 | 0.00220185 | 0.0615848211 | 0.0052828967 |
| 4 | 43 | 0.0037467810 | 0.0003127692 | 0.00076660 | 0.0000639058 | 0.00229980 | 0.0483293024 | 0.0041195089 |
| 5 | 44 | 0.0041401050 | 0.0003456652 | 0.00080372 | 0.0000670014 | 0.00241116 | 0.0379269019 | 0.0032168852 |
| 6 | 45 | 0.0045764400 | 0.0003821723 | 0.00084593 | 0.0000705215 | 0.00253779 | 0.0297635144 | 0.0025147858 |
| 7 | 46 | 0.0050606550 | 0.0004227026 | 0.00089392 | 0.0000745239 | 0.00268176 | 0.0233572147 | 0.0019675882 |
| 8 | 47 | 0.0055981780 | 0.0004677161 | 0.00094850 | 0.0000790760 | 0.00284550 | 0.0183298071 | 0.0015404689 |
| 9 | 48 | 0.0061950720 | 0.0005177277 | 0.00101056 | 0.0000842524 | 0.00303168 | 0.0143844989 | 0.0012066846 |
| 10 | 49 | 0.0068581080 | 0.0005733133 | 0.00108113 | 0.0000901388 | 0.00324339 | 0.0112883789 | 0.0009456007 |
| 11 | 50 | 0.0075948480 | 0.0006351179 | 0.00116137 | 0.0000968324 | 0.00348411 | 0.0088586679 | 0.0007412367 |
| 12 | 51 | 0.0084137370 | 0.0007038632 | 0.00125261 | 0.0001044441 | 0.00375783 | 0.0069519280 | 0.0005811815 |
| 13 | 52 | 0.0093242150 | 0.0007803585 | 0.00135635 | 0.0001130995 | 0.00406905 | 0.0054555948 | 0.0004557737 |
| 14 | 53 | 0.0103368310 | 0.0008655108 | 0.00147431 | 0.0001229423 | 0.00442293 | 0.0042813324 | 0.0003574797 |
| 15 | 54 | 0.0114633740 | 0.0009603373 | 0.00160843 | 0.0001341347 | 0.00482529 | 0.0033598183 | 0.0002804169 |
| 16 | 55 | 0.0127170250 | 0.0010659796 | 0.00176092 | 0.0001468619 | 0.00528276 | 0.0026366509 | 0.0002199869 |
| 17 | 56 | 0.0141125250 | 0.0011837200 | 0.00193430 | 0.0001613347 | 0.00580290 | 0.0020691381 | 0.0001725919 |
| 18 | 57 | 0.0156663570 | 0.0013149989 | 0.00213143 | 0.0001777929 | 0.00639429 | 0.0016237767 | 0.0001354155 |
| 19 | 58 | 0.0173969630 | 0.0014614368 | 0.00235554 | 0.0001965072 | 0.00706662 | 0.0012742750 | 0.0001062517 |
| **20** | 59 | 0.0193249700 | 0.0016248567 | 0.00261034 | 0.0002177890 | 0.00783102 | 0.0010000000 | 0.0000833716 |
| **21** | 60 | 0.0214734650 | 0.0018073127 | 0.00290000 | 0.0002419885 | 0.00870000 | 0.0080000000 | 0.0006691237 |
| 22 | 61 | 0.0236169160 | 0.0019897067 | 0.00325949 | 0.0002720308 | 0.00977847 | 0.0080000000 | 0.0006691237 |
| 23 | 62 | 0.0257338530 | 0.0021702051 | 0.00366355 | 0.0003058097 | 0.01099065 | 0.0080000000 | 0.0006691237 |
| 24 | 63 | 0.0278056050 | 0.0023471993 | 0.00411769 | 0.0003437901 | 0.01235307 | 0.0080000000 | 0.0006691237 |
| 25 | 64 | 0.0298164800 | 0.0025193236 | 0.00462814 | 0.0003864989 | 0.01388442 | 0.0080000000 | 0.0006691237 |

`q(40) = 0.00068` and `q(60) = 0.00290` are **ANCHOR** rows, [S3]'s own disclosed 예정 경험
사망률 at those ages, and so is `q(20) = 0.00051`; everything between is the Makeham fit.
In policy year 21 (attained 60) the three headline CI rates read **0.011063 / 0.004371 /
0.003999** exactly — [S3]'s disclosed anchors, again — summing with `other` (0.002040465) and
`ltc` (0) to the 0.0214734650 in the table. **The CI decrement is 4.09 times the death
decrement in the first policy year and 7.40 times it at attained 60** —
0.0027834950 / 0.00068 and 0.0214734650 / 0.00290 —
which is why a projection of this product is a morbidity projection
with a mortality tail rather than the reverse.

**The annual CI rate in policy year 1 is now the table sum itself.** Where the annual-step
model prorated it to 0.0025312484, the 보장개시일 belongs to the month and not to the year:

| month `t` | `ci_wait_factor_mth(t)` | `ci_rate_mth(t)` | what is covered |
|---|---|---|---|
| 0 | 0.0000000000 | 0.0001468954 | no 중대한 암, no 장기요양 |
| 1 | 0.0000000000 | 0.0001468954 | no 중대한 암, no 장기요양 |
| 2 | 0.0410958904 | 0.0001504033 | the 보장개시일 falls here |
| 3 | 1.0000000000 | 0.0002322544 | everything, from here on |

The twelve factors sum to `12 × (1 − 90/365) = 9.0410958904` months of exposure, so the first
policy year carries exactly the 275 days of cover the contract gives it: **the conversion
moves the wait without resizing it**. The other three limbs — the seven remaining 중대한
질병, the four 중대한 수술 and 중대한 화상 및 부식 — are covered from the 계약일 and are
never withheld, which is why the first two months' rate is not zero.

Per-cause incidence, male, at the ages worth printing:

| attained age | `cancer` | `ami` | `stroke` | `other` | `ltc` | sum |
|---|---|---|---|---|---|---|
| 20 | 0.000144000 | 0.000027000 | 0.000038000 | 0.000021945 | 0 | 0.000230945 |
| 40 | 0.001023000 | 0.000589000 | 0.000907000 | 0.000264495 | 0 | 0.002783495 |
| 50 | 0.003364142 | 0.001604531 | 0.001904493 | 0.000721682 | 0 | 0.007594848 |
| 60 | 0.011063000 | 0.004371000 | 0.003999000 | 0.002040465 | 0 | 0.021473465 |
| 80 | 0.028353209 | 0.009653117 | 0.007188769 | 0.004745485 | 0.008565526 | 0.058506106 |
| 99 | 0.031734378 | 0.010613464 | 0.007711596 | 0.005256241 | 0.103263346 | 0.158579025 |

The rows at 20, 40 and 60 are [S3]'s for the first three columns; the 80 and 99 rows are the
damped log-slope extrapolation, and the `ltc` column above 65 is the placeholder discussed
above. **Read the last row with the warning attached**: at attained 99 the 장기요양 limb is
two thirds of the whole CI rate and rests on nothing published.

### The first-year 감액 cohorts

| Quantity | Cells | Anchor (male) | Female twin (`point_id = 2`) |
|---|---|---|---|
| Share of month 3's accelerations routed to the reduced cohort | `ci_reduced_share(3)` | **0.0018376178** | **0.1945881241** |
| The same in months 0 and 1 | `ci_reduced_share(0)` | **0** | **0** |
| The same in month 2 | `ci_reduced_share(2)` | 0.0001166165 | 0.0263256424 |
| Accelerations in the first policy year | `Σ pols_ci(t)`, `t < 12` | 0.0024029515 | 0.0023722599 |
| Into the reduced cohorts | `Σ pols_ci_in(t, −(t+1))` | 0.0000036240 | 0.0004217215 |
| `accel_benefit_pp(−d)` / `resid_nominal_pp(−d)` | — | ₩40,000,000 / ₩60,000,000 | same |
| `accel_benefit_pp(d)` / `resid_nominal_pp(d)` | — | ₩80,000,000 / ₩20,000,000 | same |

**The male number is a rounding error and the female number is material**, which is exactly
what the 2003–2005 claim experience would predict: women bought about 150% of the male policy
count and generated about 244% of the male claim count, on breast and thyroid cancer, and the
market's answer from 2008 was a 180-day breast-cancer 부담보 whose lineal descendant this
clause is [R1]. On `point_id = 4`, where `first_year_scope = all`, the share is **1.00000**
in every month of the first policy year and every one of its accelerations is halved — the
GI-generation design [S4].

**The monthly grid turns one reduced cohort into twelve and empties the first two**, which
is the 보장개시일 showing up in the cohort structure rather than only in the rate.

### First months of the base run

Per policy issued, income-positive, to two decimal places — the precision the tests assert.
`pols_if` is the **total** in force, pre-CI and post-CI together, and `t` counts **months**.

| t | `pols_if` | premiums | claims_ci | claims_death | claims_death_ci | claims_lapse | claims_lapse_ci | claim_expenses | expenses | commissions | net_cf |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **0** | 1.000000 | 306,740.00 | 11,751.63 | 5,667.60 | 0.00 | 0.00 | 0.00 | 61.07 | 505,000.00 | 2,944,704.00 | −3,160,444.31 |
| 1 | 0.991203 | 303,989.10 | 11,646.53 | 5,616.91 | 0.50 | 0.00 | 0.00 | 60.53 | 4,956.02 | 0.00 | 281,708.60 |
| 2 | 0.982486 | 301,262.87 | 11,817.32 | 5,566.66 | 1.00 | 0.00 | 0.00 | 61.03 | 4,912.43 | 0.00 | 278,904.44 |
| 3 | 0.973846 | 298,560.04 | 18,069.60 | 5,516.40 | 1.50 | 0.00 | 0.00 | 84.39 | 4,869.23 | 0.00 | 270,018.92 |
| 11 | 0.907472 | 277,610.47 | 16,805.04 | 5,130.35 | 7.47 | 0.00 | 0.00 | 78.58 | 4,537.36 | 0.00 | 251,051.68 |
| **12** | 0.899508 | 275,097.32 | 18,399.84 | 5,272.75 | 8.49 | 0.00 | 0.00 | 84.94 | 4,542.51 | 8,252.92 | 238,535.87 |
| **78** | 0.681762 | 203,191.05 | 22,444.30 | 4,944.17 | 81.78 | 12,429.67 | 114.76 | 100.21 | 3,618.52 | 6,095.73 | 153,361.90 |
| 79 | 0.680398 | 202,685.36 | 22,389.00 | 4,931.98 | 84.12 | 12,598.18 | 118.35 | 99.98 | 3,611.28 | 6,080.56 | 152,771.89 |
| 120 | 0.643074 | 187,204.63 | 31,102.38 | 5,923.71 | 287.83 | 6,907.06 | 314.67 | 137.10 | 3,551.77 | 5,616.14 | 133,363.97 |
| 238 | 0.606214 | 156,116.70 | 66,553.12 | 11,132.51 | 4,285.20 | 1,408.90 | 2,079.56 | 301.48 | 3,661.86 | 4,683.50 | 62,010.56 |
| **239** | 0.605967 | 155,812.20 | 66,424.98 | 11,111.08 | 4,341.08 | 2,826.89 | 2,106.68 | 301.08 | 3,660.37 | 4,674.37 | 60,365.68 |
| **240** | 0.605719 | 0.00 | 73,741.61 | 12,319.65 | 4,868.12 | 22,667.51 | 2,125.48 | 334.39 | 3,695.46 | 0.00 | −119,752.21 |
| 241 | 0.605154 | 0.00 | 73,541.28 | 12,286.18 | 4,915.89 | 22,633.78 | 2,146.33 | 333.71 | 3,692.01 | 0.00 | −119,549.20 |
| 348 | 0.531791 | 0.00 | 95,102.91 | 23,839.03 | 30,875.10 | 17,161.62 | 4,667.32 | 546.14 | 3,548.39 | 0.00 | −175,740.51 |
| 420 | 0.450576 | 0.00 | 80,183.35 | 32,574.97 | 78,000.34 | 12,328.73 | 5,766.25 | 678.33 | 3,191.43 | 0.00 | −212,723.41 |
| 468 | 0.371825 | 0.00 | 65,052.01 | 37,511.32 | 123,279.12 | 9,195.05 | 5,613.40 | 782.15 | 2,740.58 | 0.00 | −244,173.64 |
| 708 | 0.003217 | 0.00 | 2,941.30 | 6,751.46 | 8,788.88 | 156.83 | 17.59 | 57.74 | 28.93 | 0.00 | −18,742.74 |
| **719** | 0.001913 | 0.00 | 1,852.44 | 4,252.10 | 3,986.07 | 98.67 | 7.98 | 31.71 | 17.20 | 0.00 | −10,246.18 |
| **720** | 0.001829 | 0.00 | 0.00 | 4,746.85 | 5,509.41 | 95.63 | 6.96 | 30.84 | 16.62 | 0.00 | −10,406.31 |
| 840 | 0.000000 | 0.00 | 0.00 | 1.07 | 0.00 | 0.01 | 0.00 | 0.00 | 0.00 | 0.00 | −1.08 |
| 851 | 0.000000 | 0.00 | 0.00 | 1.02 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | −1.03 |

**Seven rows do something.**

- **`t = 0`** carries the whole acquisition cost — ₩500,000 of expense plus ₩2,944,704 of
  commission, both of them annual-scale numbers — against **one month's** premium of
  ₩306,740, so `net_cf(0)` is ten times the month's income and negative. That is the
  acquisition strain stated properly: the annual grid netted a whole year's premium against
  it and printed −₩94,960.46, which read as a shallow strain and was an artefact of the
  step. `claims_lapse` is **zero** because `CV(1) = 0`: `V(1) = ₩236,200.67` against
  `SC(1) = ₩3,897,743.24`, so `max(0, V − SC) = 0` and 「이를 영(零)으로 처리한다」 does the
  flooring [REG-R19]. The payable value stays nil until the month-end **15**.
- **`t = 12`** is the first month of policy year 2 and the first with renewal commission;
  the expense inflation factor steps to 1.01 on the same 계약해당일.
- **`t = 78`** is the month the **105% account floor first binds**: `1.05 × V(79) =
  ₩20,244,219.60` overtakes the ₩20,000,000 nominal residual, where `1.05 × V(78) =
  ₩19,973,041.04` did not. The annual grid could say only that the crossing fell inside
  policy year 7.
- **`t = 239`** is the last paying month, and the **cliff** closes it: `cv_pp` goes from
  ₩26,453,920.22 at month-end 239 to ₩53,180,840.12 at month-end 240, exactly `1 / k = 2.0`
  on the same month-end's twin value.
- **`t = 240`** is the **first premium-free month**. Premium and commission both go to zero,
  the pre-CI lapse rate steps eightfold from 0.001 to 0.008, and `net_cf` falls from
  **+₩60,365.68** to **−₩119,752.21** — a swing of ₩180,117.89 between two adjacent
  **months**, where the annual grid compared two whole years and printed ₩2.18m.
- **`t = 420`** is where the **post-CI cohort peaks** at 0.217817 policies in force,
  attained age 75; its share of the in-force count peaks later still, at **60.1%** in month
  552. The 20% residual has long since become the larger stream.
- **`t = 719`** is the **last CI-covered month** (attained age 99).
- **`t = 720`** is the first month with `claims_ci = 0.00`. Nothing else stops: death claims,
  surrenders and expenses all continue for another eleven years, and carry ₩183,916.56.
- **`t = 851`** is the horizon: the table's rate is 1 in the final policy year, the monthly
  conversion spreads that certain death evenly over its twelve months rather than killing
  the cohort in the first of them, and nothing is paid but the pre-CI death benefit.

### The values run beside them

The row is the frame's month `t`, and each state column is the value at the month-end
that **closes** it, `t + 1` — the amount a surrender arising in that month is actually paid.
So the `t = 0` row carries `V(1)`, and the issue-instant values `V(0) = 0` and
`SC(0) = SC* = ₩3,944,704` sit one step above the top of the table.

| t | `pol_val_pp` | `surr_chg_pp` | `cv_std_pp` | `cv_pp` (pre-CI) | `cv_pp_ci` (post-CI) | `resid_db_avg_pp` |
|---|---|---|---|---|---|---|
| 0 | 236,200.67 | 3,897,743.24 | 0.00 | 0.00 | 0.00 | 0.00 |
| 1 | 472,933.85 | 3,850,782.48 | 0.00 | 0.00 | 0.00 | 20,000,000.00 |
| 2 | 709,893.51 | 3,803,821.71 | 0.00 | 0.00 | 0.00 | 20,000,000.00 |
| 11 | 2,802,441.49 | 3,381,174.86 | 0.00 | 0.00 | 0.00 | 20,059,094.14 |
| **14** | 3,502,979.17 | 3,240,292.57 | 262,686.60 | 131,343.30 | 262,686.60 | 20,050,662.03 |
| 59 | 14,444,029.87 | 1,127,058.29 | 13,316,971.59 | 6,658,485.79 | 13,316,971.59 | 20,010,759.51 |
| **78** | 19,280,209.15 | 234,803.81 | 19,045,405.34 | 9,522,702.67 | 19,045,405.34 | 20,251,912.32 |
| **83** | 20,581,370.16 | 0.00 | 20,581,370.16 | 10,290,685.08 | 20,581,370.16 | 21,617,332.91 |
| 119 | 30,195,074.67 | 0.00 | 30,195,074.67 | 15,097,537.34 | 30,195,074.67 | 31,707,981.03 |
| 227 | 62,465,421.89 | 0.00 | 62,465,421.89 | 31,232,710.94 | 62,465,421.89 | 65,588,692.98 |
| 238 | 66,134,800.56 | 0.00 | 66,134,800.56 | 33,067,400.28 | 66,134,800.56 | 69,441,540.59 |
| **239** | 66,476,050.15 | 0.00 | 66,476,050.15 | 66,476,050.15 | 66,476,050.15 | 69,799,852.66 |
| 251 | 67,476,674.44 | 0.00 | 67,476,674.44 | 67,476,674.44 | 67,476,674.44 | 70,850,508.16 |
| 348 | 74,766,740.78 | 0.00 | 74,766,740.78 | 74,766,740.78 | 74,766,740.78 | 78,505,077.82 |
| 468 | 82,745,956.16 | 0.00 | 82,745,956.16 | 82,745,956.16 | 82,745,956.16 | 86,883,253.97 |
| 708 | 94,916,943.77 | 0.00 | 94,916,943.77 | 94,916,943.77 | 94,916,943.77 | 99,662,790.95 |
| 840 | 98,775,050.80 | 0.00 | 98,775,050.80 | 98,775,050.80 | 98,775,050.80 | 0.00 |

`base_benefit_pp(t)` is on the month-end clock: a flat ₩100,000,000 from month-end 1 to
month-end 729 and then rising with the account — ₩100,027,274.71 at 730, ₩103,607,571.76 at
840. `accel_benefit_pp(s)` is correspondingly ₩80,000,000 until then, and
`resid_nominal_pp(s)` ₩20,000,000.

**Four readings of this table are the substance of the product.**

**The payable value is nil for fifteen months and then is not.** `cv_pp(14) = 0` and
`cv_pp(15) = ₩40,655.29` on the chassis's identical arithmetic — a date an annual grid could
only place inside policy year 2.

**The step at 납입완료 is exactly `1/k` on one month-end.** `cv_pp(240) / (k × cv_std_pp(240))
= 2.0000000000`. The month-on-month ratio `cv_pp(240) / cv_pp(239) = 2.0103` mixes the step
with one month's account accrual, which is a twelfth of the annual grid's 2.1290 — so on
this grid the step is visibly the whole of the movement and **the adjacent-period ratio is
no longer a trap**.

**The 해약공제액 is gone at month-end 84**, thirteen years before the cliff, running off in
**84 equal steps** of `3,944,704 / 84 = ₩46,960.7619047619` from `SC(0) = SC*`. Nothing about
the step at month-end 240 is a surrender-charge effect.

**`resid_db_avg_pp` is exactly ₩20,000,000 in the first two months, and that is the
보장개시일.** No 중대한 암 is covered before it, so no reduced cohort exists to lift the
average; from month 2 the reduced cohorts' ₩60,000,000 enters it and the mean reads
₩20,060,358.33 at the first 계약해당일, decaying toward ₩20,000,000 as the full cohorts
accumulate. From the month-end 79 the average tracks `1.05 V(t+1)` and the decay reverses:
₩21,888,878.45 at `t = 84`, ₩31,993,802.89 at `t = 120` and ₩86,883,253.97 at `t = 468`.
**The "20% residual" is a ₩20,000,000 promise for six years and an account-value promise for
the following sixty-five.**

The policy-loan room at the same month-ends, showing the doubling the carve-out produces.
This table is keyed by the **month-end**, and it includes the two either side of 납입완료,
where the monthly grid shows the step as the single-row event it is:

| month-end | `loan_avail_pp` (pre-CI) | `loan_avail_ci_pp` (post-CI) | ratio |
|---|---|---|---|
| 60 | 5,326,788.64 | 10,653,577.27 | 2.00 |
| 84 | 8,232,548.06 | 16,465,096.13 | 2.00 |
| 120 | 12,078,029.87 | 24,156,059.74 | 2.00 |
| 180 | 18,958,250.95 | 37,916,501.90 | 2.00 |
| 228 | 24,986,168.76 | 49,972,337.51 | 2.00 |
| **239** | 26,453,920.22 | 52,907,840.45 | 2.00 |
| **240** | 53,180,840.12 | 53,180,840.12 | **1.00** |
| 252 | 53,981,339.55 | 53,981,339.55 | **1.00** |


### Hand trace, the first month (`t = 0`)

Counts. `l0(0) = 1.000000000`, `l1(0) = 0`, `l(0) = 1.000000000`, `lw(0) = 0`, so
`lp(0) = 1.000000000`.

    premiums(0)    = 306,740 * 1.000000000                       =   306,740.00
    expenses(0)    = 500,000 * 1 + 5,000 * 1.01^0 * 1            =   505,000.00
    commissions(0) = 0.80 * 3,680,880 * 1                        = 2,944,704.00

The commission is computed on the **annual** premium, because that is the unit a Korean
commission scale is written in and the 1,200% rule caps the first year's 모집수수료 at
twelve times the monthly premium [REG-R29].

CI transition, first. The annual first-event rate at attained 40 is the table sum
0.0027834950; its monthly conversion is 0.0002322544, and in this month the 중대한 암 and
장기요양 limbs are not yet covered, so

    q_cim(0) = 0.0002322544 * (1 - 0.3675235630)                = 0.0001468954
    C(0)     = 1.000000000 * 0.0001468954                 = 0.0001468954155330
    phi(0)   = 0                                              no 중대한 암 cover yet
    C(0, -1) = 0                                              the reduced cohort is empty
    C(0,  1) = 0.0001468954155330                        the full cohort

The two cohort labels are month-ends: `−1` is the reduced cohort, empty here, and `1` is the
month-end at which this month's full claims are paid.

    claims_ci(0) = 0.0001468954155330 * 80,000,000       =  11,751.63

Death, second, among those who did not accelerate. The annual `q(0) = 0.00068`, so
`qm(0) = 1 − (1 − 0.00068)^(1/12) = 0.0000566843`:

    D(0)  = 1.000000000 * (1 - 0.0001468954) * 0.0000566843  = 0.0000566760087853
    claims_death(0) = max(0, 100,000,000 - 0) * 0.0000566760087853 =  5,667.60

Surrender, third, paid the value at the month-end that closes the month. The annual
`w(0) = 0.10`, so `wm(0) = 0.0087416110`:

    S(0)  = 1.000000000 * 0.999853104584 * 0.999943315665 * 0.0087416110 = 0.0087398314125
    CV(1) = 0.50 * max(0, 236,200.67 - 3,897,743.24) = 0.50 * 0 = 0.00
    claims_lapse(0) = 0.00 * 0.0087398314125              =         0.00

Claim expense, on **two** kinds of event:

    claim_expenses(0) = 300,000 * (0.0001468954155330 + 0.0000566760087853 + 0)
                      = 300,000 * 0.0002035714243183            =        61.07

    CF(0) = 306,740.00 - 11,751.63 - 5,667.60 - 0.00 - 0.00 - 0.00
                     -      61.07 - 505,000.00 - 2,944,704.00
          = −3,160,444.31

**That is the acquisition strain, stated properly.** A whole year's acquisition cost against
a single month's premium; the annual grid netted twelve instalments against the same cost
and printed a shallow −₩94,960.46.

Update. `l0(1) = 1 − 0.0001468954 − 0.0000566760 − 0.0087398314 = 0.9910565971631780`;
`l1(1) = C(0) = 0.0001468954155330`; `l(1) = 0.9912034925787109`. And the waiver, on
the **monthly** conversion `um(0) = 1 − (1 − 0.0003)^(1/12) = 0.0000250034382`:
`lw(1) = 0.0000247798223`, so `lp(1) = 0.9910318173408387`.

### Hand trace, the second month (`t = 1`) — the first residual death claim

Counts at the start: `l0(1) = 0.9910565971631780`, `l1(1) = 0.0001468954155330`,
`l(1) = 0.9912034925787109`, `lp(1) = 0.9910318173408387`.

    premiums(1)    = 306,740 * 0.9910318173408387          =   303,989.10
    expenses(1)    = 5,000 * 1.01^0 * 0.9912034925787109    =     4,956.02
    commissions(1) = 0.00      renewal commission starts in policy year 2

The inflation factor is still 1: it steps on the **계약해당일**, not every month.

CI transition. The 중대한 암 limb is still not covered, so `q_cim(1) = q_cim(0)`, and
`phi(1) = 0`:

    C(1)     = 0.9910565971631780 * 0.0001468954      = 0.0001455816706570
    claims_ci(1) = 0.0001455816706570 * 80,000,000       =    11,646.53

Pre-CI death, on `qm(1) = 0.0000566843`:

    D(1)  = 0.9910565971631780 * (1 - q_cim) * qm      = 0.0000561691324076
    claims_death(1) = 100,000,000 * 0.0000561691324076    =     5,616.91

**Post-CI death.** `q'm(1) = 1 − (1 − 3 × 0.00070525)^(1/12) = 0.0001701592`. **One** cohort
exists — the reduced one is empty, the 보장개시일 not having passed — and the residual is
read at the month-end that closes the month: `1.05 × V(2) = ₩496,580.55`, far below the
nominal, so the cohort is on its nominal:

    l1(1, 1) = 0.0001468954155330   resid_db(2, 1) = max(20,000,000, 496,580.55) = 20,000,000
    claims_death_ci(1) = 0.0001468954155330 * 0.0001701592 * 20,000,000 = 0.50

and `resid_db_avg_pp(1) = ₩20,000,000.00` **exactly** — a reading the annual grid could not
produce, its single first-year cohort carrying the whole year's reduced claims.

Surrenders. `wm(1) = 0.0087416110`, `w'm(1) = 0.0003339460`:

    S(1)  = 0.9910565971631780 * ... * 0.0087416110  = 0.0086616675795
    CV(2) = 0.50 * max(0, 472,933.85 - 3,850,782.48) = 0.00      still nil
    claims_lapse(1) = 0.00,  claims_lapse_ci(1) = 0.00

    claim_expenses(1) = 300,000 * 0.0002017757987            =        60.53
    CF(1) = 303,989.10 - 11,646.53 - 5,616.91 - 0.50 - 60.53 - 4,956.02
          = 281,708.60

**The carve-out is not visible in this row and that is the point of the fifteen-month
nil.** Both surrender lines are zero because the payable value is zero on both sides of the
CI transition until the month-end 15; at the month-end 20 the post-CI policyholder is paid
₩1,676,113.01 and the pre-CI one ₩838,056.50 — exactly twice — which is the
carve-out in one row, nineteen years before the chassis's cliff would have produced it.


### Hand trace, the month the 105% floor takes over (`t = 78`)

Counts: `l0(78) = 0.6637142821915645`, `l1(78) = 0.0180480553322628`,
`l(78) = 0.6817623375238273`, `lw(78) = 0.0012931755802854`,
`lp(78) = 0.6624211066112791`. This is the seventh month of policy year 7.

    premiums(78)    = 306,740 * 0.6624211066112791          =   203,191.05
    expenses(78)    = 5,000 * 1.01^6 * 0.6817623375
                   = 5,000 * 1.0615201506010 * 0.6817623375     =     3,618.52
    commissions(78) = 0.03 * 203,191.05                     =     6,095.73

The floor, read at the month-end that closes the month.
`V(79) = ₩19,280,209.15`, so `c V(79) = 1.05 × 19,280,209.15 =
₩20,244,219.60`. One **month** earlier `c V(78) = ₩19,973,041.04`, **below** the
₩20,000,000 nominal. The crossing is a single month, and from the month-end 79 every full
cohort's residual is the same number:

    resid_db(79, s) = max(20,000,000.00, 20,244,219.60) = 20,244,219.60   for s >= 1
    resid_db(79, s) = max(60,000,000.00, 20,244,219.60) = 60,000,000.00   for s <= -1

**Seventy-eight full cohorts and ten reduced ones are in force**, where the annual grid had
six and one. The model does not sum them row by row: every post-CI cohort runs the same two
decrements, so the count and the two residual totals are carried as their own recursions and
the cohort loop runs only in the months where the floor sits between the smallest and the
largest nominal — which is this month and its neighbours.

    l1(78)  = 0.0180480553322628
    resid_nom_total_pp(78)  = 361,100.80
    resid_db_total_pp(78)   = 365,507.63
    resid_db_avg_pp(78)     = 20,251,912.32

    q'm(78) = 1 - (1 - 3 * 0.00089392)^(1/12)              = 0.0002237552
    D'(78)  = 0.0180480553322628 * 0.0002237552            = 0.0000040383455043
    claims_death_ci(78) = 0.0002237552 * 365,507.63      =       81.78

`surr_chg_pp(79) = ₩234,803.81` — the charge is still running off, five months from zero at
the month-end 84, and the annual grid could only step it once a year. `cv_std_pp(79) =
₩19,045,405.34`, `CV(79) = 0.50 × that = ₩9,522,702.67` and `CV'(79) = ₩19,045,405.34`.
The rest of the row follows the previous trace's pattern and closes at
`CF(78) = +₩153,361.90`.

**What this row shows.** From here on, the reserve the model priced — which values the
residual at a flat `r SA` — and the benefit the model pays diverge, permanently and in one
direction. That divergence is the subject of the first entry in *Key sensitivities*.

### Hand trace, the first premium-free month (`t = 240`)

Counts: `l0(240) = 0.5100224688890150`, `l1(240) = 0.0956967694066161`,
`l(240) = 0.6057192382956311`. **`lp(240) = 0`** — `pols_if_pay` is defined as zero from
`t = 12m` — so premium and renewal commission are both zero.

    premiums(240)    = 0.00
    commissions(240) = 0.00
    expenses(240)    = 5,000 * 1.01^20 * 0.6057192382956311
                     = 5,000 * 1.2201900399480 * 0.6057192383    =      3,695.46

    C(240)  = 0.5100224688890150 * 0.0018073127            = 0.0009217700918919
    claims_ci(240) = 0.0009217700918919 * 80,000,000     =    73,741.61

    D(240)  = 0.5100224688890150 * (1 - q_cim) * qm  = 0.0001231965034270
    claims_death(240) = 100,000,000 * 0.0001231965034270  =     12,319.65

    q'm(240) = 1 - (1 - 3 * 0.0029)^(1/12)                 = 0.0007279071
    D'(240)  = 0.0956967694066161 * 0.0007279071           = 0.0000696583587527
    c V(241) = 1.05 * 66,557,770.20                        = 69,885,658.71
    every cohort, the reduced ones included, is on that floor
    claims_death_ci(240) = 0.0000696583587527 * 69,885,658.71   =     4,868.12

    wm(240) = 0.0006691237  (the eightfold step, from 0.0000833716 at t = 239)
    S(240) = 0.5100224688890150 * ... * wm            = 0.0003405688984958
    CV(241) = 1.00 * 66,557,770.20                     the suppression is gone
    claims_lapse(240) = 66,557,770.20 * 0.0003405688984958 =    22,667.51

    S'(240) = 0.0956967694066161 * (1 - q'm) * w'm     = 0.0000319342922532
    claims_lapse_ci(240) = 66,557,770.20 * 0.0000319342922532 =     2,125.48

    claim_expenses(240) = 300,000 * 0.0011146249541          =       334.39

    CF(240) = 0.00 - 73,741.61 - 12,319.65 - 4,868.12 - 22,667.51 - 2,125.48
                   -    334.39 -  3,695.46
            = −119,752.21

**Three things change in this one row and only one of them is the premium.** The premium
stops; the renewal commission stops; and the pre-CI lapse rate steps from 0.001 to 0.008,
multiplying pre-CI surrender outgo eightfold on a value that has itself just doubled. A
fourth has already happened: the 105% floor overtook the reduced cohorts' ₩60,000,000 at the
month-end 212, so
by now **every** post-CI cohort carries the same residual. `net_cf` goes from +₩60,365.68
to −₩119,752.21 and never returns to positive — a swing of ₩180,117.89 between two adjacent
**months**, where the annual grid compared two whole years and printed ₩2,180,009.33.


### Roll-forward and undiscounted totals

Every policy issued leaves by one of **four** decrements — the CI transition is not one of
them:

| Decrement | Total over `t = 0 … 851` | Share |
|---|---|---|
| `pols_death` (pre-CI) | 0.1400281094 | 14.00% |
| `pols_death_ci` (post-CI) | 0.4045046008 | 40.45% |
| `pols_lapse` (pre-CI) | 0.4326271583 | 43.26% |
| `pols_lapse_ci` (post-CI) | 0.0228401315 | 2.28% |
| **the four exits** | **1.0000000000** | **100.00%** |
| `pols_ci` (accelerations — a **transition**, not an exit) | **0.4273447323** | 42.73% |

`pols_if(852) = 0`. Person-**months**, twelve to a policy year: `Σ pols_if = 315.7478320763`, of
which `Σ pols_if_pre = 246.9486445020` and `Σ pols_if_ci = 68.7991875744`;
`Σ pols_if_pay = 155.0451674103`. The post-CI cohort peaks at **0.2178167855 policies in
force at `t = 420`**, attained age 75.

**42.73% of the cohort accelerates; 40.45% die having accelerated and 14.00% die without.**
Of the 54.45% who die in force, three quarters die post-CI. That single pair of numbers is
the product.

Undiscounted totals per policy issued, over `t = 0 … 851`:

| Column | Total (KRW) |
|---|---|
| `premiums` | 47,558,554.65 |
| `claims_ci` | 34,187,433.63 |
| `claims_death` | 14,003,973.11 |
| `claims_death_ci` | **36,093,568.46** |
| `claims_lapse` | 6,186,437.80 |
| `claims_lapse_ci` | 1,713,420.66 |
| `claim_expenses` | 291,563.23 |
| `expenses` | 2,441,629.84 |
| `commissions` | 4,266,347.86 |
| **`net_cf`** | **−51,625,819.94** |

Split by phase: `Σ net_cf` over `t = 0 … 239` is **+₩30,170,319.26** and over `t = 240 … 851`
is **−₩81,796,139.20**.

### Reading the shape of the result

The stream is a twenty-year accumulation followed by a fifty-one-year run-off, and the
undiscounted total of −₩51.6m is not a defect. The contract is balanced on the 2.50%
예정이율 — `P^m × ä(0)` reproduces `A0(0)` to the won — and undiscounted benefits falling
forty to seventy years out necessarily dwarf undiscounted premiums that stop at year twenty.
What is worth reading is the **composition**, and it says three things that no whole-life
chassis can say.

**The 20% residual is the larger of the two payments.** `claims_death_ci` totals
₩36,093,568.46 against `claims_ci`'s ₩34,187,433.63 and `claims_death`'s ₩14,003,973.11. A
benefit specified as one fifth of the sum assured pays out more, undiscounted, than the four
fifths paid at the acceleration — because 40% of the cohort reaches it and because the 105%
account floor has by then replaced the nominal. **Multiply the post-CI death stream by its
nominal residual instead and it collapses to ₩8,090,217.24**: the floor is worth **4.46×**
the nominal complement over the life of this contract. Anyone who reads "80% now, 20% later"
as a description of where the money goes has the product backwards.

**The morbidity decrement, not the mortality decrement, drives the liability.** Total
benefits are ₩92,184,833.65, of which the two CI-originated streams — the acceleration and
the residual death benefit it creates — are ₩70,281,002.09, or **76.2%**. The pre-CI death
benefit, which is the whole of the chassis's liability, is 15.2% of it. This is a health
product wearing a whole-life chassis, and the 예정위험률 grid is where its risk lives.

**And the acceleration is expensive.** Re-running the pricing recursion with `a = 0` on the
identical table and decrements — the same three-state contract, paying the full sum assured
on death whenever it falls — gives `A0(0) = ₩36,649,058.63` and `P^m = ₩205,075.25` against
the anchor's ₩254,261.11. **The acceleration costs 24.0% of the net premium**, purely for
moving four fifths of one sum assured forward in time and flooring the remainder at 105% of
the account. Against the market, [S4]'s published ₩306,740 is **1.19 times** the ₩257,050
표준형 종신 monthly premium the **chassis** publishes at the same cell, and **1.33 times** the
chassis's own 저해지 anchor — which is that same ₩257,050 at the chassis's **[std]** 90.0%
suppression discount, so the second ratio has a published numerator and a constructed
denominator. The model's 24.0% is a **net-premium** figure on a **fixed decrement basis**
while both market ratios are office premiums across different products and different
carriers, so they agree in order and are not comparable line by line. **The monthly grid
makes the market comparison the direct one it should always have been**: `premium_mth_pp()`
is the published ₩306,740 itself, not twelve times it and back again.

---

## Valuation and reserve pointers

This library projects gross liability cash flows. Every valuation layer consumes them and is
cited, never reproduced. **The chassis sets out all three Korean layers in full** — IFRS 17
(K-IFRS 제1117호, mandatory since 2023-01-01) [REG-R60], K-ICS [REG-R13], the
해약환급금준비금 [REG-R11], the 책임준비금 delegation [REG-R3] [REG-R10], the unpublished
산출방법서 [REG-R2] [REG-R18] and the 선임계리사 sign-off [REG-R5]. Four things are
CI-specific and are stated here.

- **`pol_val_pp` is a 계약자적립액 on a three-state basis, and it is not a reserve.** The
  chassis's point that under K-IFRS 제1117호 the insurer no longer books a 보험료적립금 as a
  separate statutory reserve carries over unchanged. What is new is that the account
  recursion this model asserts, `check_pol_val_roll_fwd()`, carries the **CI decrement in the
  premium annuity and the residual EPV in the outgo term**. A reserve computed on an ordinary
  two-state whole-life recursion is a different number, and on this product it is a wrong
  one: it over-values the premium annuity by 4.8%, and under-states `P` by 4.6%.
- **The 해약환급금준비금 test creates an asymmetry the carve-out makes visible.** The
  appropriation compares the IFRS 17 잔여보장요소 against the surrender value computed
  **under 제7-66조제1항 — on that basis even for the 제7-66조제4항 products that may
  contractually pay less** [REG-R11]. So a CI event **doubles** the contractual surrender
  value from one day to the next and changes the reserve the appropriation is measured
  against **not at all**, because that reserve was already on the unsuppressed 별표-14 basis.
  The carve-out is a pure transfer to the CI claimant, visible in the fulfilment cash flows
  and invisible in the surrender-value reserve. `cv_std_pp(t)` is exactly the quantity the
  test needs and is published for that reason.
- **K-ICS: this product loads a sub-risk the chassis barely touches.** The life and
  long-term-health module's seven sub-risks include **장해ㆍ질병위험액**, which on an ordinary
  종신보험 is negligible and here carries 76.7% of the benefit stream. **해지위험액** matters
  for the chassis's reason — the 무·저해지 form and the 대량해지 shock — and **사업비위험액**
  and **사망위험액** are unchanged. The 대량해지 shock magnitudes live in 시행세칙 별표 22,
  which was **not retrieved**, so everything resting on them is second-hand and
  **[unverified]** [REG-R26] [REG-R36]. No `krlib` model computes 요구자본.
- **The 예정위험률 revision right is an unmodelled option inside the liability and it is
  asymmetric.** From five years, with 금융위원회 approval, the insurer may revise the
  예정위험률; where the change raises the premium or the reserve, the default position for a
  policyholder who does not fund the increase is a **reduced sum assured**, not a lapse [S3].
  So the exercise of the right shows up as benefit erosion, not as a decrement, and a
  contract-boundary or CSM analysis that treats it as a repricing right of the ordinary kind
  will mis-place it. It is named here and nowhere modelled.

**And the negative finding that bounds every parameter in this document.** For mortality the
chassis can at least bracket the level from two carriers' published 적용위험률 grids. For CI
morbidity there is **exactly one disclosed table in the whole of Korea and it is fifteen
years old** [S3]. The bureau's 참조순보험요율 is filed and never published [REG-R4]; the
장기손해보험 display that *is* public [REG-R61] is stated on the insured-cancer definition
that excludes C44 and C73, which is not the 중대한 암 definition. **No amount of further
research converts a decrement in this document into a sourced value**; what research can do,
and did, is anchor it on three ages and bound it by two published premium relativities.

---

## Key sensitivities and model risks

In rough order of leverage on this product:

1. **The residual floor multiple `c`.** One number, `1.05`, carries a stream of
   ₩36,093,568.46 — the largest benefit line in the projection. Removing the floor and
   paying the nominal `r B(s)` collapses it to ₩8,090,217.24, a factor of **4.46**. `c` is
   sourced at 1.05 [S1 별표1 주8] and at 1.10 on an older version of the same product [S3],
   so it is a carrier and vintage parameter and is a model point column for that reason;
   `point_id = 9` runs 1.10. **The floor is the single largest structural feature of this
   liability and the easiest to omit.**
2. **The post-CI mortality multiple.** `mort_ci_factor = 3.00` **[std]**, with **no Korean
   source of any kind**. It determines how long the post-CI cohort survives to collect the
   floored residual, and it moves `claims_death_ci` and the post-CI cohort's size in
   opposite directions, so its net effect is not monotone and cannot be reasoned about
   without running it. `point_id = 9` runs 2.00. A user with reinsurer data replaces this
   number first.
3. **The lapse vector.** The `log_linear` 원칙모형 against a level 4% paying-period rate —
   the same 0.8% post-완납 ultimate either way — changes the undiscounted `Σ net_cf` from
   −₩51,625,819.94 to **−₩34,030,199.11**, a third of the liability, because lapse removes
   lives before the acceleration reaches them. Both
   endpoints are supervisory [REG-R27]; the interpolation is **[std]** and the guideline's
   functional form is **[unverified]** at instrument level.
4. **The `ltc` incidence limb above age 65.** A placeholder scaled to an order of magnitude
   [REG-R42] and proportional in shape where a real inception curve is not. It is nil before
   `t = 300` and two thirds of the CI rate at attained 99. Anything read off the tail
   of this projection is read off it.
5. **The `other` limb, at 10.5% of the three headline rates.** Derived from two published
   figures with different denominators [S3] [S4], and flat as a proportion across every age,
   which no real set of seventeen conditions is.
6. **The 90-day 보장개시일 is no longer a proration, and that is the conversion's gain
   here.** It is placed month by month, so the *mechanism* is now the contract's own; setting
   the wait to zero moves the undiscounted `Σ net_cf` by only **₩25,804.50** (0.05%), so the
   *level* stays immaterial. What remains **[std]** is the day inside the month, and the
   unmodelled 부활, which restarts the ninety days [S1 별표1 주1].
7. **The first-year 감액 scope.** Immaterial on a male cell — moving `first_year_factor` to
   1.00 changes `Σ net_cf` by ₩140.28 — and material on a female one, where
   `ci_reduced_share(3) = 0.1946` against the male 0.0018. A model tested only on the anchor
   will not notice a bug here.
8. **The horizon and the two boundaries.** `ω = 110` **[std]**; CI cover ends at
   `n_CI = 720` months. The eleven post-CI-cover years still carry **₩183,916.56** of
   claims, and **69.0%** of the post-CI death benefit and **42.3%** of all benefits fall from
   the fortieth 계약해당일. Truncating the projection at the end of CI cover, or at attained
   age 100, understates materially.
9. **Expense inflation over seventy-one years.** 1.0% **[std]** compounds to **2.01** over
   the run; 3% compounds to **7.92**. There is no published Korean expense basis to anchor
   either.
10. **The base run is a valuation-basis run.** `mort_be_factor = ci_be_factor = 1.00` on
    [S3]'s 예정위험률, which carry a 안전할증 whose cap was 30%, then 50% from 2015, then
    removed from 2017 [R1]. A best-estimate basis sits below 1.00 on both and `point_id = 9`
    is where the levers are exercised.

### Known modeling pitfalls

Each of these is a mistake a competent modeller would actually make on this product, and
each is checkable.

- **The acceleration is a transition, not an exit.** `check_pols_roll_fwd()` asserts
  `l(t) − l(t+1) = D + D' + S + S'` — **four** terms. Adding `C(t)` removes every CI
  claimant from the population on the day they claim, which is precisely what 감독규정
  제7-60조제8호 forbids the contract to do [REG-R16]. The symptom is a decrement sum above 1
  and a post-CI cohort that never accumulates.
- **The residual floor is two-sided.** `max(r B(s), c V(t))`, not `r B(s)` and not `c V(t)`.
  A one-sided max is right for most of the projection and wrong at the ends: before the
  month-end 79
  the nominal binds and after it the account does, and the reduced cohorts' ₩60,000,000 stays
  on the nominal until the month-end 212. `check_resid_floor()` tests both limbs separately
  for a reason.
- **The floor is read off the current month-end and the nominal off the entry month-end.**
  `resid_db_pp(t, s) = max(r B(s), c V(t))` mixes two month-ends on
  purpose: `B(s)` is the 기본보험금 at the acceleration date — a **date**, which on this
  grid is a month — and `V(t)` the account **now**.
  Reading both
  off `t`, or both off `s`, is wrong in opposite directions and neither error shows up before
  the month-end 79.
- **Collapsing the post-CI cohorts loses the first-year reduced ones.** They carry
  ₩60,000,000 where every other cohort carries ₩20,000,000, and they survive the whole
  projection. On a male cell a reduced claim is 0.18% of a month's accelerations and the
  error is invisible;
  on the female twin it is 19.5% and it is not. Test on `point_id = 2` or `4`, never only on
  `point_id = 1`. **And there are twelve of them, not one**, the first two empty because the
  보장개시일 has not passed.
- **The premium annuity must carry the CI decrement.** `ä` discounts on
  `(1 − q_ci^m)(1 − q^m)`.
  Using an ordinary life annuity gives 187.9209941962 months against the correct
  178.7102998490 —
  a 5.2% over-statement, and a monthly net premium of ₩241,798.85 against ₩254,261.11 — and
  `check_pol_val_roll_fwd()` fails immediately, which is what it is for.
- **The monthly decrements are compounded, not divided.** Every rate the sources tabulate is
  an **annual probability**, and `1 − (1 − q)^(1/12)` is what makes twelve months reproduce
  it; `q/12` does not, and on the `log_linear` lapse vector the two differ by 4.9% of the
  first year's rate. The excess post-CI mortality multiplies the **annual** rate and is then
  converted, because the 3.00 behind it is a statement about a year's survival. The sister
  model `LTC_KR_S` divides by twelve for the opposite reason — its transition intensities
  are rates per year, not probabilities.
- **The post-CI cohort never pays a premium.** `pols_if_pay(t)` is
  `pols_if_pre(t) − pols_waived(t)` and the post-CI count is nowhere in it, because a
  CI/LTC 지급사유 waives all future
  기본보험료 [S1 별표1 주4]. Weighting premium by `pols_if(t)` reproduces the base run's
  first month exactly and diverges from `t = 1` onward — a slow, quiet error worth
  **9.150272** person-**months** of spurious premium inside the 납입기간, ₩2,806,754.28, of
  which the post-CI cohort is **8.730436** (₩2,677,973.86) and the 장해 50%+ waived subset
  the remaining 0.4198358 (₩128,780.42).
- **The suppression has two exits, and one of them is random.** `cv_pp_ci(t) = cv_std_pp(t)`
  at **every** duration, not from anniversary `m`. Applying `k` to the post-CI cohort halves
  the
  surrender benefit of exactly the policyholders the carve-out exists to protect, and
  `check_cv_carve_out()` catches it. Over the whole projection the carve-out is worth only
  **₩64,704.62** — ₩1,713,420.66 paid against ₩1,648,716.04 on the suppressed counterfactual,
  a **3.8%** uplift — because most post-CI surrenders happen after 납입완료 anyway. So this
  bug is **nearly invisible in the totals and factor-of-two wrong at every individual
  duration inside 납입기간**. Test it at the month-ends, not on the sum.
- **The step at 납입완료 is `1/k` on one month-end.** `cv_pp(240) / (k × cv_std_pp(240))
  = 2.0000000000` exactly. The adjacent-**month** ratio `cv_pp(240) / cv_pp(239) = 2.0103`
  includes one month of account accrual, a twelfth of the annual grid's 2.1290, so on this
  grid the step is visibly the whole of the movement. Interpolating, grading or smoothing the
  boundary is wrong; so is paying the last paying month's surrenders on the suppressed basis.
- **The step is not a surrender-charge effect.** `surr_chg_pp(d) = 0` from the month-end 84,
  thirteen
  years before the cliff, running off in **84** equal steps of ₩46,960.7619047619. A model
  that ties the two together will place the cliff at the wrong duration on any point where
  `m ≠ 7`.
- **The 표준해약공제액 uses the pre-acceleration sum assured.** ₩100,000,000, not the
  ₩20,000,000 residual: 별표 15 제3호 read with 제8호 takes the 일반사망보험금 before any
  증감 [REG-R21]. Using the residual would cut the statutory cap from ₩3,944,704 to
  ₩3,144,704, a 20% under-statement of the surrender charge.
- **CI before death before lapse.** Reversing the first two routes lives that would have
  accelerated into the death decrement, which is 4.09 times smaller in the first policy year
  and 7.40 times smaller at attained 60. The order is [std] and it is asserted; state your
  own convention before comparing numbers with anyone.
- **The two payments are one step apart, not simultaneous.** A life accelerating in month `t`
  is paid at month-end `t + 1`, takes the cohort label `s = t + 1`, joins the post-CI state
  at the **start of month `t + 1`** and is not exposed to `q'^m` until then. **That step is
  now a month where it was a year**, and it is the single largest number the conversion
  moves on this product: the post-CI in-force at the twentieth 계약해당일 is 1.1% lower.
  Paying an acceleration and a residual death benefit in the same step on the same life
  double-counts the claim expense and mis-times the residual.
- **The CI decrement stops at `n_CI` and nothing else does.** `ci_rate(t) = 0` from
  `t = 720` on the anchor; premiums stop at `t = 240`; death claims, surrenders and
  maintenance expense run to `t = 851`. Three different end dates in one projection, and only
  one of them is the horizon.
- **`ci_rate` is a first-event rate, not a sum of marginal incidences.** The benefit is
  payable once across the whole trigger set [S1 별표1], and the Korean supervisor required
  the overlap to be in the filed rate [R1]. Building the table by adding published
  site-specific incidences double-counts every life with two qualifying conditions.
- **There is no survival period.** Importing the overseas 30-day requirement moves lives from
  the CI decrement to the death decrement and changes the benefit they are paid from
  `a B + later r B` to `B` once. The Korean supervisor refused the requirement expressly
  [R1].
- **`pols_if` is the total in force, both states.** It is the weight on maintenance expense
  and it is **not** the pre-CI count. Weighting maintenance by `pols_if_pre` drops **60.1%**
  of the in-force count at its peak month; weighting premium by `pols_if` adds a cohort that
  pays nothing.
- **The claim expense is charged on three events, not one.** CI, pre-CI death and post-CI
  death. Charging it on deaths alone under-states the expense stream by 44%.
- **Everything the loan touches is floored at zero, and the acceleration is not netted at
  all.** `max(0, B − L)`, `max(0, resid_db − L)`, `max(0, CV − L)`, `max(0, CV' − L)`; the
  선지급 is paid gross **[std]**, no retrieved document saying otherwise. And the loan room
  itself is computed off the **payable** value, so it doubles at the acceleration date —
  ₩23,945,646.45 against ₩47,891,292.89 at the 계약해당일 `d = 144` on `point_id = 7`. The
  balance rolls on the **monthly** equivalent of the 4.00% the 약관 quotes, so twelve months
  compound back to exactly it.
- **The two decrement tables are not the chassis's.** `ω = 110` here against 115 there, and
  the two files are fitted to different anchors on different bases. Swapping them changes the
  horizon by five years and the whole mortality level.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-ci_insurance-r1
[R10]: #krlib-ci_insurance-r10
[R11]: #krlib-ci_insurance-r11
[R13]: #krlib-ci_insurance-r13
[R16]: #krlib-ci_insurance-r16
[R3]: #krlib-ci_insurance-r3
[R5]: #krlib-ci_insurance-r5
[R6]: #krlib-ci_insurance-r6
[R7]: #krlib-ci_insurance-r7
[REG-R1]: #krlib-reg-r1
[REG-R10]: #krlib-reg-r10
[REG-R11]: #krlib-reg-r11
[REG-R13]: #krlib-reg-r13
[REG-R16]: #krlib-reg-r16
[REG-R18]: #krlib-reg-r18
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R21]: #krlib-reg-r21
[REG-R25]: #krlib-reg-r25
[REG-R26]: #krlib-reg-r26
[REG-R27]: #krlib-reg-r27
[REG-R29]: #krlib-reg-r29
[REG-R3]: #krlib-reg-r3
[REG-R32]: #krlib-reg-r32
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R36]: #krlib-reg-r36
[REG-R38]: #krlib-reg-r38
[REG-R4]: #krlib-reg-r4
[REG-R40]: #krlib-reg-r40
[REG-R42]: #krlib-reg-r42
[REG-R48]: #krlib-reg-r48
[REG-R5]: #krlib-reg-r5
[REG-R52]: #krlib-reg-r52
[REG-R55]: #krlib-reg-r55
[REG-R60]: #krlib-reg-r60
[REG-R61]: #krlib-reg-r61
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
