# Implementation Notes

**Status:** Draft, 2026-09-03. Built from [`technical-notes.md`](technical-notes.md); the
product those notes describe is specified in [`product-spec.md`](product-spec.md), and
every source tag on this page resolves in [`sources.md`](sources.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics are sourced — the acceleration and its exact complement, the
> once-only rule across the whole trigger set, the 105% 계약자적립금 floor under the
> residual, the 90-day 중대한 암 보장개시일 and the absence of a waiting period on
> everything else, the first-year halving for breast cancer, the premium waiver on any
> CI/LTC 지급사유, the release of the 저해지 suppression by that same event, CI cover
> ending at the 100세 계약해당일 while death cover runs 종신, and the statutory
> 표준해약공제액. **Every quantitative assumption is a [std] standardization**, and in
> Korea that is structural rather than lazy: the 산출방법서 is a 기초서류, filed and never
> published [REG-R2]; the 경험생명표 is released only as 평균수명 and 기대여명 [REG-R33]
> [REG-R34]; and the **life** 참조순보험요율 is defined as the rate the bureau *files*, not
> one it publishes [REG-R4] — the 장기손해보험 display 보험개발원 does publish carries an
> insured-cancer 발생률 grid and a 질병입원율 grid [REG-R61] and no 중대한 질병 item at all,
> so nothing on it reaches here. There is exactly one disclosed Korean CI
> morbidity table in public — six rates at three ages, in a 2011 상품요약서 [S3] — and
> both decrement files in this directory are built on it. Replace them with company data
> and a real 산출방법서 before drawing any conclusion from the numbers.

## Run it

```bash
python products/ci_insurance/run.py            # the anchor cell, point_id = 1
python products/ci_insurance/run.py 7          # the 보험계약대출 point
```

`run.py` prints the model point, the derived scalars, the first policy year of the
cash flow statement and the months around 납입완료, the undiscounted totals, the
acceleration at three 계약해당일 and the nine `check_*` identities. Everything it prints is
ASCII, so the output lands on a Windows console under any code page: amounts are labelled
`KRW`, and the product, the 선지급 비율 and the suppressed surrender-value form are
romanized. Real output, with the cash-flow rows elided — they are reproduced in full in
[`technical-notes.md`](technical-notes.md):

```text
CI_KR_S - CI boheom (jungdae jilbyeong boheom, critical illness), monthly grid
age basis: boheom nai (insurance age, six-month rounding)
model point 1: CI-KR-0001 - M40, cover KRW 100,000,000, 20-year premium term, jeohaeji hwangeup-hyeong, k = 0.50
seonjigeup biyul a = 0.80   residual r = 0.20   account floor c = 1.05   first-year reduction: breast
gross premium = KRW 306,740.00/month (3,680,880.00 p.a.)   net level premium = KRW 254,261.11/month (3,051,133.35 p.a.)
projection = 852 months (71 years, t = 0 .. 851) to attained age 110   CI cover runs 720 months (60 years), to age 100
pyojun haeyak gongje-aek (statutory surrender-charge cap) = KRW 3,944,704.00
modules: lapse basis = log_linear   loan utilisation = 0.00% at policy year 0 (month-end 0)   mort_be_factor = 1.00   ci_be_factor = 1.00   post-CI mortality x 3.00

t is 0-based and counts months; policy year = t // 12 + 1.  The first policy year and the turn of it, and the months around napip wallyo:
    [ the t = 0..12, 238, 239, 240 rows of result_cf(), eleven columns ]

undiscounted totals per policy issued (KRW):
pols_if                 315.75
premiums           47558554.65
claims_ci          34187433.63
claims_death       14003973.11
claims_death_ci    36093568.46
claims_lapse        6186437.80
claims_lapse_ci     1713420.66
claim_expenses       291563.23
expenses            2441629.84
commissions         4266347.86
net_cf            -51625819.94

the acceleration, at three gyeyak haedangil (per policy, KRW):
  month-end  60 = policy year  5 (the close of month t =  59)  account V =     14,444,030   surrender pre-CI =      6,658,486   post-CI =     13,316,972
          accelerated a*B = 80,000,000   nominal residual r*B =   20,000,000   loan limit pre/post = 5,326,789 / 10,653,577
  month-end 120 = policy year 10 (the close of month t = 119)  account V =     30,195,075   surrender pre-CI =     15,097,537   post-CI =     30,195,075
          accelerated a*B = 80,000,000   nominal residual r*B =   20,000,000   loan limit pre/post = 12,078,030 / 24,156,060
  month-end 240 = policy year 20 (the close of month t = 239)  account V =     66,476,050   surrender pre-CI =     66,476,050   post-CI =     66,476,050
          accelerated a*B = 80,000,000   nominal residual r*B =   20,000,000   loan limit pre/post = 53,180,840 / 53,180,840

checks: pols True  ci states True  decrements True  account True  complement True
        residual floor True  carve-out True  loans True  net cf True
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/ci_insurance/CI_KR_S")
model.Projection[1].result_cf()      # the worked example's anchor cell
model.Projection[1].result_val()     # the account, both surrender values, the benefits
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a `DataFrame` indexed by the **0-based month** `t` with one
column per cash flow line, `pols_if` first and `net_cf` last; `expenses` there is acquisition plus
maintenance, with the claim handling expense in its own `claim_expenses` column.
`result_pols()` publishes the two states and their four decrements beside it, and
`result_val()` the account, **both** surrender values and the benefit levels — the second
because the whole product turns on the difference between the pre-CI and the post-CI value
at the same duration, and printing that only inside a cash flow is not enough.
`result_val()` is indexed by the same `t`, and each of its state columns is read at the
month-end that **closes** the month, `t + 1` — the amount a claim or a surrender arising
in that month is actually paid.
`model.Projection.doc` carries the notes' symbols mapped to cells names and states the age
basis; `model.Data.doc` says what each input file is and, for both decrement files, what
they are **not**.

## One decrement, two payments, one sum assured

The model exists to carry the acceleration, and everything structural about it follows
from one line: on the first qualifying event the insurer pays `a B(s)` at the month-end
`s` that closes the month of the event, the contract does **not** terminate, the death
benefit becomes `max(r B(s), c V(k))` at every later month-end `k`, and the premium stops. The contract's survival is a regulatory requirement rather than a
design choice — 감독규정 제7-60조제8호 forbids a contract to be extinguished while the risk
it covers remains effective [REG-R16].

So the projection runs **two states**. `pols_if_pre(t)` is the pre-CI cohort and
`pols_if_ci(t)` the post-CI one; `pols_ci(t)` is the transition between them and is
deliberately **absent from `check_pols_roll_fwd`**, because it is not an exit. A model in
which an acceleration reduced the in-force count would be modelling a standalone 진단비
benefit and not an acceleration at all.

The post-CI cohort is carried **by the month in which it accelerated**,
`pols_if_ci_at(t, s)`: a life accelerating in month `t` is paid at month-end `t + 1` and
takes the label `s = t + 1`; a reduced first-year claim takes `−(t + 1)`, a label no full
claim can carry. That is not tidiness. The residual a post-CI policy owns was fixed
at its own acceleration date — 「지급사유 발생 당시의 기본보험금」, which is a **date** and
on this grid a month — at `r` times the 기본보험금 *then*, and the 기본보험금 grows
with the account and with cumulative premiums; collapsing the cohorts to one average
residual would let a policy that accelerated at duration 3 inherit the larger residual of
one that accelerated at duration 40.

**The monthly grid turns the annual model's single first-year 감액 cohort into twelve, and
empties the first two**, no 중대한 암 being covered before the 90-day 보장개시일. It also
multiplies the whole cohort dimension by twelve, so the aggregates the cash flow needs —
the post-CI count and the two residual totals — are carried as their own recursions rather
than rebuilt by summing the cohort table in every month; every post-CI cohort runs the same
two decrements, so the two routes give the same number and only one of them is linear in
the horizon.

On the anchor cell 40.5% of the cohort dies having accelerated, 14.0% dies without, 43.3%
surrenders pre-CI and 2.3% surrenders post-CI. **Those four exits sum to 1.000000**, which
is what `check_decrement_sum()` asserts: every policy issued leaves by a modelled
decrement, and there is no residual population and no tail state anywhere in the model.
**42.7% of the cohort accelerates**, and that number sits outside the sum because an
acceleration is not an exit. The post-CI cohort peaks at 0.217817 policies in force at
`t = 420`.

## The complement is exact, and it is checked

`resid_rate()` is `1 − accel_rate()` arithmetically rather than a second model point
column, and `check_accel_complement()` asserts, cohort by cohort, that what is accelerated
and what is left add to exactly the 기본보험금 that was in force when the claim arose —
`a B + r B = B`, and `a f B + (1 − a f) B = B` for the first-year cohort [S1] [S2]. **The
acceleration never adds cover.** It is a redistribution of one sum assured across two
dates, which is why `epv_ben()` differs from an ordinary whole-life EPV only by the
*timing* of `a SA`: on the anchor cell the acceleration is worth 24.0% of the net level
premium against the same contract without it.

`resid_rate()` is computed as `1.0 − 0.8` and is therefore `0.19999999999999996` in
binary, so `resid_nominal_pp(s)` evaluates to ₩19,999,999.9999999963 and not to a round
₩20,000,000. The complement is exact in the sense the model asserts — the check closes to
`val_tol × SA` = ₩1 — and the documents write ₩20,000,000 throughout. Anyone re-deriving
the residual from `1 − a` in a spreadsheet will see the same last-place digits.

## Two horizons, and neither is the contract's

**The time index `t` is 0-based and counts months.** `t = 0` is the first policy month,
month `t` runs from
time `t` to time `t + 1`, the attained age is `age_at_entry() + t // 12` — 보험나이 steps on
the 계약해당일, so the floor division is exact — and the contractual
policy year label is `t // 12 + 1`. `proj_years()` = `omega_age() − age_at_entry() + 1` is
the number of projected policy years and `proj_len()` is twelve times it, the exclusive end
of the frame, so the projection
covers `t = 0 … proj_len() − 1`, `result_cf()` carries `proj_len()` rows and the frame is
`range(proj_len())`. A second, **month-end** index runs `0 … proj_len()` with 0 at issue
and carries the contract's state — `pol_val_pp`, `surr_chg_pp`, `cv_std_pp`, `cv_pp`,
`cv_pp_ci`, `base_benefit_pp`, `cum_prem_pp`, `resid_db_pp`, `loan_avail_pp`,
`pol_loan_draw` and the cohort label `s`; it does not move with the frame, month `t`
opens at month-end `t` and closes at month-end `t + 1`, and a 계약해당일 is a month-end
`d = 12y`.

There is no
maturity date and no 만기보험금 [S1] [S3] [S4], so the **death-cover horizon is the
terminal age of the constructed table, ω = 110** **[std]**; every remaining life dies in
the final policy **year**, where the table's rate is 1 and `mort_rate_mth` spreads that
certain death uniformly over its twelve months as `1 / (12 − j)` rather than killing the
cohort in the first of them, and `pols_if(proj_len())` is zero.

**CI cover ends earlier.** `ci_cover_end()` is `12(100 − x)`, the 100세 계약해당일, so on
the anchor cell the CI decrement is live for 720 of the 852 projected months and the last
eleven years carry a death benefit alone. Those eleven years are not empty: they still carry
₩183,916.56 of claims. This is the post-2008 design; the 2002 product put the acceleration
inside a 제1보험기간 running to the 80세 계약해당일 and paid 100% of the death benefit
thereafter [S6] [R1], and that legacy split is named in `product-spec.md` and deliberately
not modelled — a second discontinuity at 80 would collide with the 저해지 step in any model
point trying to isolate either.

**Three different end dates sit in one projection and only one of them is the horizon.**
`ci_rate(t)` is zero from `t = 720`; `premiums(t)` and `commissions(t)` are zero from
`t = 240`; death claims, surrenders and maintenance expense run to `t = 851`.

## Annual assumptions, a monthly grid

Every rate the sources tabulate is an **annual** figure and stays one: `mort_rate`,
`mort_rate_ci`, `ci_rate`, `lapse_rate`, `lapse_rate_ci` and `waiver_rate` return the rate
of the policy year the month falls in, and each has a `_mth` companion applying
`1 − (1 − q)^(1/12)` so that twelve months compound back to exactly it. The roll-forward
applies the companions and nothing else. Dividing by twelve instead would understate the
early months and overstate the late ones; on the `log_linear` lapse vector, which spans two
orders of magnitude, the two conventions differ by 4.9% of the first year's rate.

Three cells depart from that pattern, each for a stated reason.

**`mort_rate_mth` at the terminal age.** `q = 1` there and admits no twelfth root, so the
certain death is spread uniformly over the year as `1 / (12 − j)` — the UDD convention,
which closes the table exactly instead of killing the cohort in one month and leaving
eleven empty rows.

**`ci_rate_mth` and the 90-day 보장개시일.** The wait is a **date**, and this is the
conversion's clearest gain on the product. `ci_wait_factor_mth(t)` is the fraction of month
`t` falling after it: zero in months 0 and 1, 0.0411 in month 2, one thereafter. The
중대한 암 and 장기요양 limbs are withheld in that proportion and the other three limbs —
covered from the 계약일 [S1] [S2 별표1 주1] — never are. The twelve factors sum to
`12 × (1 − 90/365) = 9.041096` months, so the conversion **moves** the wait without
resizing the first policy year's exposure; the annual grid could only smear it across the
whole year as a 0.7534 proration. `ci_rate(t)` is consequently the table sum itself in
policy year 1, where the annual-step model prorated it.

**`mort_rate_ci_mth` and the excess multiple.** `mort_ci_factor = 3.00` multiplies the
**annual** probability and the result is then converted, not the other way round: a factor
of three on a monthly force is not a factor of three on the year, and the 3.00 that stands
behind this number is a statement about a year's survival [REG-R40].

Contractual terms quoted in policy years are unchanged and multiplied out where the grid
needs them — the 납입기간 `12m`, the 해약공제기간 `12 n_sc`, the CI cover period, the
first-year 감액 over months 0 … 11, and `pol_loan_year`'s 계약해당일. The interest rates
are quoted per annum and roll on their monthly equivalents, `prem_int_rate_mth()` and
`i_loan_mth()`, so twelve months compound back to exactly the quoted figure.

## One policy value, three surrender values, two exits from the suppression

There is a single `V(t)` in the model, `pol_val_pp()`, the 계약자적립액 of the **표준형
twin** — the non-marketed comparison contract — at **month-end** `t`, `t = 0` at issue.
The 해약환급금 is `W(t) = max(0, V(t) − SC(t))` and what is actually payable is a multiplier
on it. All four are on the month-end clock, so a surrender arising in month `t` is paid
`cv_pp(t + 1)`:

| Cells | Payable value | When |
|---|---|---|
| `cv_pp(t)` | `k W(t)` | pre-CI, inside the 납입기간 |
| `cv_pp(t)` | `W(t)` | pre-CI, from 납입완료 |
| `cv_pp_ci(t)` | `W(t)` | post-CI, at **every** duration |

**The suppression therefore has two exits, not one: 납입완료, and a CI/LTC 지급사유.** The
second is the CI-specific delta on the whole life chassis, whose cliff is a deterministic
function of duration; here it is at `min(12m, t_CI)`, a **random** date correlated with the
product's own decrement and, on this grid, a month rather than a policy year. It is contractual — [S2] conditions the suppression on 「제7조 …
제2호의 CI/LTC보험금 지급사유가 발생하지 않은 경우」 and [S4] on 「「선지급 진단보험금」
지급사유 발생 전 납입기간 동안」.

The step at 납입완료 is a **step, not a ramp**: `cv_pp(12m) / (k × cv_std_pp(12m))` is
exactly `1 / k = 2.000000` on the anchor cell, and the monthly grid is what makes the claim
checkable — the adjacent-**month** ratio is 2.0103 against the annual grid's 2.1290, so the
step is visibly the whole of the movement rather than a mixture of it with a year of account
growth. It is not a surrender-charge effect and cannot be
explained as one — the 해약공제기간 is capped at seven years [REG-R19 제7-66조제1항제2호](#krlib-reg-r19),
so on a 20년납 contract `surr_chg_pp(d)` is zero from the month-end 84, thirteen years
earlier, having run off in 84 monthly steps rather than seven annual ones.

`check_cv_carve_out()` asserts what the carve-out exists to produce: **a CI claimant is
never worse off on surrender than an unaccelerated policyholder at the same duration.** It
is not tautological — it fails the moment the suppression is applied to the post-CI cohort,
which is the natural mistake to make when one surrender-value scale is run over one
aggregate policy count. Over the whole projection the carve-out is worth only ₩64,704.62,
a 3.8% uplift on `claims_lapse_ci`, because most post-CI surrenders fall after 납입완료
anyway; **at an individual duration inside the 납입기간 it is a factor of two.** Test it at
the month-ends, never on the totals.

The same carve-out **doubles the policy loan** at the acceleration date, because the loan
is computed off the payable value: at the 계약해당일 `d = 120` on the anchor cell
`loan_avail_pp` is ₩12,078,030 and `loan_avail_ci_pp` is ₩24,156,060, at the same duration,
with nothing else about the contract changed [REG-R25 제33조](#krlib-reg-r25).

## The residual is not a constant

`resid_db_pp(t, s)` is `max(r B(s), c V(t))` — 「CI/LTC보험금 지급사유 발생당시의
기본보험금의 20%와 CI/LTC보험금 지급사유 발생 후 계약자적립금의 105% 중 큰 금액」
[S1 별표1 주8]. It mixes two clocks on purpose: `B(s)` is the 기본보험금 at the
acceleration date and `V(t)` the account **now**; both are month-ends, and a post-CI
death in month `t` is paid `resid_db_pp(t + 1, s)`. `check_resid_floor()` asserts it
against both limbs separately — in aggregate every month and cohort by cohort at every
계약해당일 — so a one-sided `max` written the wrong way round, or a floor
read off the wrong month, fails.

**On the 80% form the floor binds early and stays bound.** At the anchor cell `r B` is
₩20,000,000 and `1.05 V(d)` passes it at the month-end **79** — the seventh month of policy
year 7, thirteen years before 납입완료, and a date the annual grid could only place in a
year; by
`t = 120` the in-force mean residual is ₩32.0m and by `t = 468`, ₩86.9m. So for most of the
contract's life the residual death benefit **is the account value and not the stated
complement**, and a model that hard-codes 20% of the sum assured understates the post-CI
liability by a growing margin — over the anchor's life, by a factor of **4.46**:
₩36,093,568.46 paid against ₩8,090,217.24 on the nominal. On the 50% form the same test
needs `V > ₩47,600,000` and is reached far later. That asymmetry is one of the three
reasons the composite takes the 80% fraction, and it is the single most useful thing
`result_val()` prints.

## The pricing basis, and the two things it deliberately leaves out

`pol_val_pp(t) = epv_ben(t) − P^m a(t)` at month-end `t`, a prospective net level premium
reserve on the 예정이율 and the shipped tables, with
`P^m = prem_net_level_mth_pp() = A0(0) / a(0)` — the equivalence principle, which is why
`V(0) = 0` falls out of the formula rather than being imposed. Every index is a month and
`a(t)` is measured in **months** of premium, so what it solves for is a monthly net
premium. The two-state recursion is

```
A1(t) = vm [ q'm r SA + (1 - q'm) A1(t + 1) ]
A0(t) = vm [ q_cim a SA + (1 - q_cim) qm SA
             + q_cim A1(t + 1) + (1 - q_cim)(1 - qm) A0(t + 1) ]
a(t)  = 1 + vm (1 - q_cim)(1 - qm) a(t + 1),   t < 12m
```

and `check_pol_val_roll_fwd()` asserts its retrospective form at every month-end. **The
CI decrement is in the annuity as well as in the benefit**, because any CI/LTC 지급사유
waives all future 기본보험료 [S1 별표1 주4]; a premium stream that ran on through the
post-CI state would over-fund the contract by the whole of the waiver. An ordinary life
annuity gives `ä(0) = 187.9209941962` months against the correct `178.7102998490`, a 5.2%
over-statement, and a monthly net premium of ₩241,798.85 against ₩254,261.11.

Two simplifications are **[std]** and are stated rather than hidden. The pricing recursion
values benefits at `SA` and the residual at `r SA`, **ignoring both floors on the
기본보험금 and the 105% floor under the residual**; pricing the second in would make `V`
self-referential, the floor being a multiple of `V` itself. And the reserve runs on the
**pricing** decrements and not the best-estimate ones, which is what makes the identity
testable at all. Both floors are applied in full in the cash-flow projection.

On the anchor cell `A0(0) = 0.454391 SA`, `ä(0) = 178.710300` months and
`P^m = ₩254,261.11` against a gross of ₩306,740 a month — a loading of 20.6%. The
annualisation `P = 12 P^m = ₩3,051,133.35` is published beside it, and is **2.78% above**
the ₩2,968,483.20 the annual-step model solved for: the ordinary modal effect of paying
monthly in advance. The model point file's premiums were derived from that annual figure
and are unchanged, so the loading the anchor implies moved with the grid and the file did
not. That is close to, and a different
quantity from, the **보험료지수 of 130.1%** [S3] publishes for the same form, which is
against the 표준순보험료 computed on the supervisor's prescribed rates rather than on this
model's basis. The 연납순보험료 that enters the 표준해약공제액 is a third quantity again:
`surr_chg_cap_pp()` follows the chassis in taking **80% of the gross** **[std]**, so the
statutory cap can be reproduced from published figures alone. It comes to
0.80 × ₩3,680,880 × 5% × 20 + 1% × ₩100,000,000 = **₩3,944,704** [REG-R20], against the
FSC's 13-times-monthly-premium rule of thumb of ₩3,987,620 — a **1.1%** agreement between
two independent statements of the same cap [REG-R29].

The cap is computed on the **pre-acceleration** 보험가입금액, ₩100,000,000, and not on the
₩20,000,000 residual: 별표 15 제3호 read with 제8호 takes the 일반사망보험금 before any
증감 [REG-R21]. Using the residual would cut it to ₩3,144,704, a 20% under-statement.

## The premium waiver is not one decrement but two

[S1] waives all future 기본보험료 on **either** a 장해지급률 of 50% or more, **or** any
CI/LTC 지급사유 [S1 별표1 주4]. The second limb fires with essentially every CI claim, so
it is **not modelled as an independent decrement**: it is implicit in the post-CI cohort,
which pays nothing at all. What is left is the first limb, `waiver_rate(t)` at 0.03% a year
**[std]**, which moves a policy into `pols_waived(t)` — a *subset* of the pre-CI cohort,
not a third state. A waived policy keeps its full death cover, stays exposed to the CI
decrement, and, under the chassis's **"waived premiums count as paid"** rule, continues to
accrue surrender value on the full premium scale. It is therefore the only route to the
저해지 step without funding it.

`pols_if_pay(t)` is `pols_if_pre(t) − pols_waived(t)`, and the post-CI count is nowhere in
it. Weighting premium by `pols_if(t)` instead reproduces the first month exactly and
diverges from `t = 1` onward — 9.150272 person-**months** of spurious premium inside the
납입기간, ₩2,806,754.28, of which the post-CI cohort is 8.730436 (₩2,677,973.86) and the
waived subset the rest — which is the quietest available error in this model.

A modern Korean accelerated product has **two trigger sets of different widths**: a narrow
one for the money and a wide one for the waiver, which by the GI generation runs to 25
named triggers [R11]. A model using one rate for both is wrong on the second. This one uses
two, and says that the second is a standardization.

## Lapse, and the two bases carried side by side

`lapse_basis` is a model point column with two values. `log_linear` is the **로그-선형
원칙모형** the IFRS17 주요 계리가정 가이드라인 of 2024-11-07 prescribes for 무·저해지
business: geometric decay from a first-year 10% **[std]** to the **0.1%** the guideline
sets at 납입완료 — reached in the last paying policy year — then a **0.8%** post-완납
ultimate from `t = 12m` [REG-R27] [R3]. All three are **annual** rates and the decay runs on
the policy year, so the rate is level across the twelve months of one; `lapse_rate_mth`
converts it. `table` is the 표준형
duration curve in `lapse_table.csv`. Carrying both is the comparison the guideline itself
requires an insurer to disclose, and it is why the table survives on a product whose
representative form does not use it. The choice is worth a third of the liability: a level
4% comparison moves the undiscounted `Σ net_cf` from −₩51,625,819.94 to −₩34,030,199.11,
because lapse removes lives before the acceleration reaches them.

**No separate 완납 surrender spike is imposed.** The eightfold step from 0.1% to 0.8% at
납입완료 is produced by the guideline's own shape; the contractual step in `cv_pp` that
provokes a real surge is a different object from the behavioural assumption about it, and
conflating the two counts the spike twice. The chassis's mandatory ≥ 30% additional lapse
at a 유지보너스 date [REG-R27] does not arise here: this composite carries no 유지보너스.

`lapse_rate_ci(t)` is the ultimate rate of whichever basis is in force times
`lapse_ci_factor = 0.50` **[std]**, level in `t`: a post-CI policy is premium-waived and so
is in the paid-up state by construction. **The direction of that factor is genuinely
ambiguous** — a CI claimant has no premium to fund and may value the residual highly, which
argues for less surrender, but the carve-out has just doubled the cash available, which
argues for more — and nothing in any retrieved document bears on it. It is a lever, not a
finding.

## Processing order

Within month `t`, **[std order]**: premium, acquisition expense, maintenance expense
and commission at the start of the month; then the CI transition; then death among those who
did not accelerate; then surrender among those who neither accelerated nor died. A life
accelerating in month `t` receives `a B(t + 1)` at the end of it — month-end
`t + 1` — and joins the post-CI cohort at the start of month `t + 1`, so it is not exposed
to the residual death benefit until the following month.

**That lag is now a month where the annual grid made it a year, and it is the single
largest number the conversion moves on this product**: the post-CI cohort is exposed to its
own mortality from the month after the claim rather than from the next 계약해당일, and the
post-CI in-force at the twentieth 계약해당일 is 1.1% lower for that reason alone. The lag
itself remains deliberate. The 장해분류표 defers assessment of a 중대한 뇌졸중 for **twelve
months** after onset, with a further six-month deferral where function is still improving
[S1 별표3], so a CI claim and the death that may follow it are not simultaneous events on
any grid. Paying an acceleration and a residual death benefit in the same step on
the same life would double-count the claim expense and mis-time the residual.

Reversing the first two steps routes lives that would have accelerated into the death
decrement, which is **4.09 times smaller** in the first policy year and **7.40 times
smaller** at attained 60. The order is a standardization and it is asserted; state your own
convention before comparing numbers with anyone.

**The 90-day 중대한 암 보장개시일 is no longer a proration.** It is a date, and the monthly
grid places it: `ci_wait_factor_mth(t)` gives no `cancer` or `ltc` cover in months 0 and 1,
0.0411 of a month's in month 2 and all of it from month 3, against the annual grid's
`1 − 90/365 = 0.7534246575` smeared across the whole first year. The other seven diseases,
the four surgeries and the burn are covered from the 계약일 and are never withheld
[S1] [S2 별표1 주1]. The twelve monthly factors sum to twelve times the annual one, so the
first policy year still carries exactly its 275 days of cover.

## Modules that are off in the base run

Four constructions are implemented and switched off, so the base run reproduces the worked
example while the machinery stays visible and testable.

| Module | Switch | Off value | Exercised on | What it does |
|---|---|---|---|---|
| 보험계약대출 | `pol_loan_util` | `0.0` | point 7 | A single capped drawdown at the 계약해당일 `12 × pol_loan_year`, `loan_cap_rate` = 0.80 of the **payable** value [REG-R25 제33조](#krlib-reg-r25), accumulating at the monthly equivalent of `i_loan` = 4.00%. Point 7 draws at the month-end **144**, inside the 납입기간, so the suppressed base binds and the doubling at a CI event is visible: ₩23,945,646.45 of room pre-CI against ₩47,891,292.89 post-CI at the same duration. No policy leaves because of a loan — a balance that outgrows a benefit floors the payment at zero |
| The 표준형 lapse basis | `lapse_basis` | `log_linear` | points 3, 6, 8 | Reads `lapse_table.csv` by the contractual 1-based `policy_year` label — month `t` reads row `policy_year(t)` — instead of running the 원칙모형 formula |
| The all-trigger first-year 감액 | `first_year_scope` | `breast` | point 4 | Routes **every** acceleration of the first policy year into the reduced cohorts rather than only the breast-cancer share — the GI-generation simplification [S4] [S5]. `ci_reduced_share(t)` goes from 0.0018376178 on the anchor to 1.0 in each of the twelve months |
| The best-estimate levers | `mort_be_factor`, `ci_be_factor` | `1.00` | point 9 | Scale the two decrements off the valuation basis. At 1.00 the base run is a **valuation-basis run and not a best estimate**: [S3]'s rates are 예정위험률 carrying a 안전할증 whose regulatory cap was 30% in the early 2000s, 50% from the 2015 로드맵 and removed from 2017, and no retrieved source sizes the margin against current Korean insured experience [R1] |

Model point 9 also carries the **110%** residual floor multiple [S3] publishes instead of
105%, a post-CI mortality factor of 2.00 instead of 3.00, and a 0.05% waiver rate, so that
every carrier-and-vintage parameter is live on at least one shipped point.

`loan_pp(t)` is therefore **identically zero in the base run**, and so are
`pol_loan_draw(t)` and the residual of `check_loan_roll_fwd()`. The check is published
anyway: it is trivial on eight points and non-trivial on the ninth, which is the point of
it. `claims_lapse` is likewise **zero for the first fifteen months** on the anchor, and on
every point with a surrender charge for some such stretch, and that is contractual rather
than incidental — the value at the month-end that closes the first month is
`V(1) = ₩236,200.67` against `SC(1) = ₩3,897,743.24`, so `max(0, V − SC)` is nil and
「이를 영(零)으로 처리한다」 does the flooring [REG-R19]. The payable value first becomes
positive at the month-end **15**, a date an annual grid could only place inside policy year
2. Every published Korean 해약환급금 grid shows nil at duration 1.

## What is not modelled, and is named so it is not mistaken for absent

중도인출 and 추가납입 are **arguments of the 기본보험금 definition** [S1 별표1 주7] and are
held at zero rather than dropped — a model that ignores them must say it holds them at zero
rather than silently leaving them out of the definition. Also outside the model: 부활 and
the 90-day 중대한 암 보장개시일 it restarts [S1 별표1 주1]; the pre-inception cancer
carve-out and its five-year revival [S1 제7조⑤⑥]; the 예정위험률 revision right from five
years, which takes effect as a **benefit reduction** rather than as a lapse [S3];
가지급제도; 감액; 연금전환, which appears in no retrieved CI 약관; the 다중지급 (multi-pay)
generation; and the 100% 선지급플러스형, which is not a pure acceleration at all [S4]. The
clawback the chassis applies to unpaid premiums in the suppressed period is stated in
neither CI 약관, and whether it gates the CI carve-out is **[unverified]**; this model
assumes it does not.

No `krlib` model computes 요구자본. The projection produces gross liability cash flows and
leaves the 책임준비금 [REG-R3] [REG-R10], the IFRS 17 CSM [REG-R60], the 해약환급금준비금
[REG-R11] and the K-ICS 장해ㆍ질병위험액 [REG-R13] to a layer that consumes them.
`cv_std_pp(t)` is published for one of those layers specifically: the 해약환급금준비금 test
measures against a surrender value computed on the 제7-66조제1항 basis **even for the
제7-66조제4항 products that may contractually pay less** [REG-R11], so the unsuppressed twin
value is the quantity that test needs.

## Inputs are external files

Four CSVs sit beside `run.py`, in the model folder's **parent**; the model folder holds
`__init__.py`, `_system.json` and its two Space folders and nothing else — no `_data/`, no
IOSpec, no embedded values — so a diff of the model shows logic changes only. This is the
`annuallife.TradLife_A` layout; contrast `basiclife.BasicTerm_S`, which keeps its inputs
*inside* the model. The consequence worth knowing: **the model is not portable on its own.**
Copying `CI_KR_S` without its parent's CSVs produces a model that reads and then fails on
first evaluation.

| File | Reference | Reader | Index | Contents |
|---|---|---|---|---|
| `model_point_table.csv` | `model_point_file` | `Data.model_point_table()` | `point_id` | nine model points; point 1 is the anchor |
| `mort_table.csv` | `mort_table_file` | `Data.mort_table()` | `sex`, `age` | the death decrement, 15 to ω = 110 |
| `ci_incidence_table.csv` | `ci_incidence_file` | `Data.ci_incidence_table()` | `sex`, `age`, `cause` | the CI decrement by cause, 15 to 100 |
| `lapse_table.csv` | `lapse_table_file` | `Data.lapse_table()` | `policy_year` | the 표준형 surrender curve |

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate
ItemSpace with its own cells cache; readers placed there would re-read every file for every
model point. They live in the unparameterized `Data` Space instead, and
`test_inputs_are_read_once_not_once_per_model_point` asserts the property against the file
set registered in `kr_registry.INPUT_FILES`. `input_dir()` returns `_model.path.parent`,
resolved at run time and never hard-coded, so the model works from any checkout.

**Every assumption CSV carries a `provenance` column and every cell in it begins with a
citation tag.** `model_point_table.csv` is the only exemption, a model point being a
configuration rather than an assumption. That escalation matters more here than on most
products, because in this one every row of every decrement file is either an anchor read
off [S3] or a construction resting on something else, and the two must be distinguishable
by eye.

### `mort_table.csv` — a Makeham fit to three anchors, and a female defect

The male rates are a Makeham form fitted **exactly** to [S3]'s three disclosed male
예정 경험 사망률 anchors — q(20) = 0.00051, q(40) = 0.00068, q(60) = 0.00290 — **in the rate
itself and not in the force**, `q(y) = A + B c^y` with `A = 4.960424e−04`,
`B = 1.077496e−06`, `c = 1.1371590`, used to age 60. Extrapolated, that fit reaches
`q = 1` at about attained age **107** — inside this projection's own horizon — and stands a
third above the shipped ramp by age 100 (0.412 against 0.311), so **the old-age shape is a
separate [std] rule and not a continuation**:
log-linear in `q` from the age-60 anchor to `q(110) = 1`, i.e.
`q(y) ≈ 0.00290 × 1.1240^(y − 60)`.

The female rates are **0.5294 × the male rates at every age below ω**, that being [S3]'s own
disclosed female-to-male ratio at age 20 (0.00027 / 0.00051) — the only usable female
anchor, because [S3]'s female rates at 40 and 60 extract identical to the male ones and are
a PDF column-merge artefact expressly [unverified]; at ω = 110 both sexes carry the terminal
`q = 1`. **The construction understates the female advantage**: it gives a 15-to-80 death
probability ratio of **0.560** (0.128367 / 0.229205) against the 0.500 implied by
국가데이터처's survival to age 80 of 남 64.4% / 여 82.2% [REG-R38]. That is a stated defect
of this file and not a finding about Korean insured mortality.

This table is **not the chassis's.** ω is 110 here against 115 there, and the two files are
fitted to different anchors on different bases. Swapping them changes the horizon by five
years and the whole mortality level.

### `ci_incidence_table.csv` — five causes, five provenances

Long form — one row per `(sex, age, cause)` — so that each cause carries its own tag, which
matters because they do not rest on the same thing.

| cause | what it covers | basis |
|---|---|---|
| `cancer`, `ami`, `stroke` | 중대한 암 / 급성심근경색증 / 뇌졸중 | **[S3]** at ages 20, 40 and 60; **[std]** elsewhere |
| `other` | five further 중대한 질병, four 중대한 수술, 중대한 화상 및 부식 | **[std]**, 10.5% of the three |
| `ltc` | 장기요양상태 on 노인장기요양 1·2등급 | **[std]**, nil below 65 |

Between and below the anchors the three headline rates are log-linear in `ln(rate)`. Above
60 the 40-to-60 log-slope **decays geometrically at 0.90 a year** **[std]**; run undamped,
male 중대한 암 would reach 1.29 by age 100. The `other` loading of 10.5% is derived rather
than assumed: [S4]'s published 3대-to-17대 office premium step is 5.30%, and [S3]'s
보장위험별 연간보험료 disclosure puts the CI benefit at 50.6% of the risk premium at male
40, so 0.0530 / 0.506 = 0.105. The `ltc` ramp — 0.12% at 65 growing 14% a year — is a
**placeholder for the construction [`LTC_KR_S`](../long_term_care/model.md) owns**, scaled
so the 65+ mean is of the order implied by [REG-R42]'s 154,688 1·2등급 인정자 at an assumed
three-year mean duration; it is the weakest number in the file, it is proportional in shape
where a real inception curve is not, and at attained 99 it is two thirds of the whole CI
rate.

**Summing the five causes is legitimate only because the shipped rates are themselves
first-event rates.** The benefit is payable once only across every trigger [S1 별표1], and
Korea's supervisor required the overlap between CI causes to be reflected in the filed rate
rather than ignored for rate stability as overseas practice does — 「CI 질병들 간
중복해서 발생할 수 있는 확률을 최대한 반영한 최종 위험률로 검증받고 사용하였다」 [R1]. A
table built by adding published site-specific incidences would be wrong in exactly the
direction the regulation addresses.

**And the narrowness of 중대한 is in the level of these rates, not in the prose.** The
model applies no narrowing factor to a broader published rate, because it does not start
from one: [S3]'s 0.001023 at male 40 is a 중대한 암 rate, already net of C44, C61, C73,
melanoma at or below T2aN0M0, 대장점막내암, 제자리암 and 경계성종양 [S1 별표4 Ⅰ], and the
뇌졸중 rate is already behind the 25% 장해지급률 gate [REG-R25]. The 장기손해보험
참조순보험요율 that *is* public carries a 「기타피부암 및 갑상선암 이외의 암 발생률」 grid
[REG-R61] — the basis `Cancer_KR_S` sources from — and it does **not** reach this product,
because the insured-cancer definition it is stated on is not the 중대한 암 definition.

### `lapse_table.csv` and `model_point_table.csv`

`lapse_table.csv` is six duration rows and a level tail of **annual** rates: 0.09 / 0.07 /
0.055 / 0.045 / 0.038 / 0.032, then 0.028 read for policy year 7 and every later year. The
file is keyed by the contractual `policy_year` label and is untouched by the grid; month `t`
reads row `policy_year(t)` and `lapse_rate_mth` converts what it finds. It is **[std]** —
no CI lapse experience of any kind was retrieved [R1] — and bounded only by the 적용해지율
envelopes Korean 상품요약서 publish for protection business. It is the 표준형 comparison
curve, not the representative form's basis; the tail sits well above the 0.8% post-완납
ultimate the guideline sets, which is why the two bases are carried side by side rather
than one being a stress on the other [REG-R27].

`model_point_table.csv` ships **nine** points: both sexes, issue ages 15 / 30 / 35 / 40 /
45 / 50 / 60 across the 보험나이 15-60 envelope, sums assured ₩10,000,000 to ₩200,000,000,
premium terms of 10 / 20 / 30 years, both acceleration fractions, all three surrender-value
forms (`k` = 1.00 / 0.50 / 0.00), both first-year 감액 scopes, both lapse bases, the policy
loan and the best-estimate levers. Projection lengths run from 612 to 1,152 months (51 to
96 policy years). Every point projects without raising and every `check_*` is `True` on
every one of them.

The anchor's premium is **sourced**: ₩306,740 a month is published for exactly that cell
[S4], the `premium_annual` column carries twelve times it, and `premium_mth_pp()` divides it
back — so on the monthly grid the projection collects the published rate itself and no modal
loading is invented in either direction. On the other eight points the column is the
**annual-step model's** own `prem_net_level_pp()` grossed up by the loading that model
implied (1.2399868) times
the published 저해지-to-기본환급형 form factor — 1.10224 for the 기본환급형 [S4], 1.000 for
the 저해지 form, 0.937 for the 무해지 form **[std]**. The file is an input and did not
change with the grid; `tests/test_ci_insurance_kr.py` asserts the rule against the
annual-equivalence premium it was written on, which this model still reproduces from its own
EPVs.

### What the monthly grid did to the input files: nothing

Every time-like column in this product's CSVs is a **contractual term quoted in policy
years**, and the contract did not become monthly — only the grid underneath it did. So **no
CSV value moved**. The decisions, column by column:

| File | Column | Decision | Reason |
|---|---|---|---|
| `lapse_table.csv` | `policy_year` | **unchanged**, values 1 … 7 | A contractual **1-based** label, not the model's time index. `lapse_rate_base(t)` reads row `policy_year(t)`, clamped into the file's range, so every month of policy year 1 takes the first-year 9% — and `lapse_rate_mth` converts it |
| `model_point_table.csv` | `pol_loan_year` | **unchanged**, 12 on point 7 | A duration in **policy years**, "duration 12". The draw falls at the 계약해당일 `12 × pol_loan_year`, month-end 144, which is the same date it always was |
| `model_point_table.csv` | `prem_term` | **unchanged**, 10 / 20 / 30 | A duration in years, a count and not an index. It reads as "premiums fall at `t = 0 … 12 × prem_term − 1`" |
| `model_point_table.csv` | `premium_annual` | **unchanged** | An annual premium, the unit a commission scale and a 보험료지수 are written in; `premium_mth_pp()` is one twelfth of it |
| `model_point_table.csv` | `issue_age` | **unchanged** | An age, and the attained age is `issue_age + t // 12` |
| `mort_table.csv` | `age` | **unchanged**, 15 … 110 | Keyed by attained age, reached through `age(t)`; no time index in the file |
| `ci_incidence_table.csv` | `age` | **unchanged**, 15 … 100 | The same, by `(sex, age, cause)` |

## Sign convention

`net_cf()` is **income positive** — premiums less the five kinds of benefit, claim expense,
acquisition and maintenance expense and commission — which is the notes' own sign and the
library-wide one, so there is no outgo-positive `liability_cf` companion to publish.

The identity, in one line:

> **`net_cf` = `premiums` − `claims_ci` − `claims_death` − `claims_death_ci` −
> `claims_lapse` − `claims_lapse_ci` − `claim_expenses` − `expenses` − `commissions`.**

That is what `check_net_cf()` asserts, with the per-`t` signed residual at
`check_net_cf_resid(t)` — the library-wide names for this check on every model. It
reconstructs the total from the five benefit kinds the statement actually publishes, so a
sixth kind added to `claims(t, kind)` and never given a column shows up here rather than
silently vanishing from the statement. `result_cf()` publishes the five `claims_*` split
columns and **no** aggregate `claims` column, so the printed columns sum to the printed
total with nothing to skip and nothing double-counted.

`check_net_cf()` closes to `val_tol × sum_assured()`, which is ₩1 at the anchor, rather
than to the `roll_fwd_tol = 1e-10` used on counts: it compares won amounts of order 1e8 and
float64 leaves rounding there that a policy count does not have.

The model projects **undiscounted gross liability cash flows** and nothing else. One
consequence to expect: the anchor's undiscounted `Σ net_cf` is **−₩51,625,819.94**, and
that is not a defect. The contract balances on the 2.50% 예정이율 — `P^m × ä(0)` reproduces
`A0(0)` to the won — and undiscounted benefits falling forty to seventy years out
necessarily dwarf undiscounted premiums that stop at year twenty.

## Naming

`lower_snake_case` throughout, reusing lifelib's `basiclife.BasicTerm_S` and
`savings.CashValue_SE` vocabulary wherever there is an analogue — `pols_*` for policy
counts, plural nouns for cash flows, `*_rate` for rates, `*_pp` for per-policy amounts,
`claims(t, kind)` with an uppercase `kind` string, `pols_if_at(t, timing)` for the
within-month in-force reads. The library's own settled spellings carry the Korean
quantities: `prem_int_rate` for the 예정이율 (never `yejeong_rate`), `decl_rate` for a
공시이율 (not used here — the composite is 금리확정형), `cv_floor_ratio` for the
무해지/저해지 suppression factor, `surr_chg_pp` for the 해약공제액 and `surr_chg_cap_pp`
for the 표준해약공제액 that bounds it. This is a 계약자적립액 and not an account value in
the `savings` sense, so it is `pol_val_pp` and `cv_pp`, and there is no `av_pp` anywhere.
**`lapse_rate` is the annual rate** and `lapse_rate_mth` its monthly conversion, which is
the library-wide convention on every monthly model: the unsuffixed name always holds the
rate the source tabulates and the `_mth` companion always holds `1 − (1 − rate)^(1/12)`.
The same pairing runs through `mort_rate`, `mort_rate_ci`, `ci_rate` and `waiver_rate`, and
through the interest cells as `prem_int_rate`/`prem_int_rate_mth` and `i_loan`/`i_loan_mth`.
`prem_net_level_mth_pp` is the monthly net premium the account is built from and
`prem_net_level_pp` its annualisation.

### The notes' symbols, and where they live

`model.Projection.doc` carries the full table and names the age basis, **보험나이**. The
rows a reader holding the technical notes needs most are these.

| Notes symbol | Cells | Meaning |
|---|---|---|
| `a`, `r = 1 − a` | `accel_rate()`, `resid_rate()` | 선지급 비율 and its exact complement |
| `c` | `resid_floor_mult()` | the 계약자적립금 floor multiple under the residual |
| `k` | `cv_floor_ratio()` | the 저해지 suppression factor |
| `f` | `first_year_factor` | the first-year 감액 factor |
| `q_ci(t)`, `q(t)`, `q'(t)` | `ci_rate`, `mort_rate`, `mort_rate_ci` | the three **annual** rates, pre- and post-CI |
| `q_ci^m`, `q^m`, `q'^m` | `ci_rate_mth`, `mort_rate_mth`, `mort_rate_ci_mth` | their monthly conversions — what the roll-forward applies |
| `A0(t)`, `A1(t)`, `ä(t)` | `epv_ben`, `epv_resid`, `annuity_due` | the pricing recursion's three series |
| `V(t)`, `W(t)`, `CV(t)`, `CV'(t)` | `pol_val_pp`, `cv_std_pp`, `cv_pp`, `cv_pp_ci` | one account, one 표준형 value, two payable values |
| `B(t)` | `base_benefit_pp(t)` | the 기본보험금 every percentage applies to |
| `max(rB, cV)` | `resid_db_pp(t, s)` | the residual death benefit of cohort `s` at month-end `t` |
| (sums) | `resid_nom_total_pp`, `resid_db_total_pp` | the cohort aggregates the cash flow needs, carried as recursions |
| `l(t)`, `l0(t)`, `l1(t)`, `lp(t)` | `pols_if`, `pols_if_pre`, `pols_if_ci`, `pols_if_pay` | one total, two states, one paying subset |
| `C(t)`, `D(t)`, `D'(t)`, `S(t)`, `S'(t)` | `pols_ci`, `pols_death`, `pols_death_ci`, `pols_lapse`, `pols_lapse_ci` | one transition and four exits |
| `n_CI` | `ci_cover_end()` | number of CI-covered **months**; the last is `t = n_CI − 1` |
| `T_y`, `T` | `proj_years()`, `proj_len()` | projected policy years, and months — the frame's exclusive end |

### Five names that needed care

`pols_if(t)` is the **total** in force, pre-CI plus post-CI. A CI claimant's contract is
still in force — that is the whole point of an acceleration — so counting only the pre-CI
cohort under that name would understate the exposure maintenance expense is charged on, by
60.1% at the peak month on the anchor. The split is `pols_if_pre` and `pols_if_ci`.

`pols_ci(t)` is the CI **decrement** out of the pre-CI cohort, matching `pols_death` and
`pols_lapse`; `pols_if_ci(t)` is the resulting in-force count. The two are a month apart and
mixing them is the easiest mistake in this model to make.

`accel_benefit_pp(s)` and `resid_nominal_pp(s)` are indexed by the **cohort label** `s` and
not by the projection month, because both are fixed at the acceleration date. A negative
label is a first-year reduced cohort, and there are twelve of them.

`mort_rate_ci` is the post-CI death decrement and `mort_rate_ci_base` its pricing-basis
twin; the model point column that scales both keeps its own spelling, `mort_ci_factor`.

`expenses` is **acquisition plus maintenance only**, and the claim handling expense is
`claim_expenses`, deducted explicitly in `net_cf` and published in its own column. That is
the settled meaning across all six libraries, so an `expenses` column means the same thing
in every one of them. Here it is not a formality: the claim expense is charged on the CI
event as well as on both kinds of death, so it runs 79% above what a death-only chassis
would produce — 0.981006 claim events per policy issued against 0.548006 deaths — and
burying it inside `expenses` would hide exactly that.

`ci_surv` and `ci_cohort_entrants` are the two cells the monthly conversion added for
performance rather than for meaning: a cohort has exactly one entry month, and every post-CI
cohort runs the same two decrements, so `pols_if_ci_at(t, s)` is a closed form rather than a
chain of monthly steps. The test module asserts the closed form against the recursion it
replaces.

krlib's cross-model review settled two of these against alternatives. `pols_if` was argued
for the pre-CI count on the ground that a post-CI policy is "no longer a normal in-force
policy"; it lost, because `pols_if` is the library-wide weight on maintenance expense and a
model whose `pols_if` means something different from every other model's is unreadable.
And `pols_ci_in(t, s)` was argued down to `pols_ci(t)` alone; it kept its cohort argument,
because collapsing it loses cohort 0 — 0.15% of the first year's accelerations on a male
cell and
**17.86%** on the female twin.

## Standardizations used

Every row is **[std]**. The sourced contractual parameters — the acceleration and its
complement, the 105% floor, the 90 days, the first-year halving, the waiver triggers, the
carve-out, the 7-year 해약공제기간, the 별표 14 coefficients and the anchor premium — are in
[`product-spec.md`](product-spec.md) and [`technical-notes.md`](technical-notes.md) and are
not repeated. "Observed range" is what the retrieved documents actually bound; several of
them bound nothing at all, which is said rather than papered over.

| Parameter | Value | Rationale | Observed range |
|---|---|---|---|
| `prem_int_rate` | 2.50% p.a., 연복리, flat | the chassis's 예정이율, inherited unchanged; equal to the 2026 평균공시이율 [REG-R48] | CI evidence brackets it too far away to be useful: 연복리 4.0% on a 2011 product [S3], 「약 2.75%」 for 종신보험 in 2019 [S4] |
| `i_loan` | 4.00% p.a. | 예정이율 + 1.5%, the chassis's formula at three carriers; the *formula* is sourced, the level is a vintage | none published for a CI product |
| `loan_cap_rate` | 0.80 | inside the contractual limit the 표준약관 sets on the **payable** value [REG-R25 제33조](#krlib-reg-r25) | the chassis's published 「해약환급금의 50% ~ 85%」 band |
| `net_prem_ratio` | 0.80 | the 연납순보험료 entering 별표 14 is taken as 0.80 × gross, so the statutory cap rests on published figures alone [REG-R20] | cross-check: ₩3,944,704 against the FSC's 13× monthly rule of thumb, ₩3,987,620 — 1.1% [REG-R29] |
| surrender-charge run-off | straight line over `12 × surr_chg_years_cap` = 84 months | the 7-year cap is statutory [REG-R19 제7-66조제1항제2호](#krlib-reg-r19); the schedule inside it is in the unpublished 산출방법서 [REG-R2] | none published; 84 equal steps of ₩46,960.7619047619 at the anchor |
| ω (`omega_age`) | 110 | the 제10회 경험생명표's terminal age is not published [REG-R33] [REG-R34] | the chassis ships 115 on a differently anchored table |
| mortality construction | Makeham form in `q` (not in the force) fitted exactly to three anchors to 60, log-linear in `q` from 60 to `q(110) = 1` | the fit reproduces [S3]'s three disclosed male rates exactly; extrapolated it passes `q = 1` at about attained age 107 and stands a third above the ramp at 100, so the ramp is a separate rule | female = 0.5294 × male on [S3]'s age-20 ratio; the check **fails** — a 15-to-80 ratio of 0.560 against the 0.500 implied by [REG-R38] |
| CI incidence above 60 | 40-to-60 log-slope damped at 0.90 a year | undamped, male 중대한 암 reaches 1.29 by age 100 | none published above 60; [S3] stops there |
| `other` limb | 10.5% of the three headline rates | 5.30% office-premium step from 3대 to 17대 [S4] divided by the CI benefit's 50.6% share of the risk premium at male 40 [S3] | a derivation from two published figures with different denominators, and flat across age where seventeen conditions are not |
| `ltc` limb | nil below 65, `0.0012 × 1.14^(y−65)` above | scaled to the order implied by [REG-R42]'s 154,688 1·2등급 인정자 at an assumed three-year mean duration | **this product's own source set retrieved none**, but the library's does: `LTC_KR_S` sources a disclosed 요양 1·2등급 발생률 grid at ages 40 / 50 / 60 by sex, on which the male 1·2등급 rate at 60 is 0.000530 — about 2.5% of this model's CI rate there. Holding this limb at nil below 65, and not modelling the 노인성 질병 route below 65 [REG-R55], understates the decrement at insured ages by that order |
| `ci_wait_days` | 90, placed **month by month** on the `cancer` and `ltc` limbs: nil in months 0–1, 0.0411 in month 2, one thereafter | the 90 days are sourced four times over [S1] [S2] [S3] [S4]; the monthly grid places them where the contract does rather than prorating the year, and the twelve factors sum to twelve times `1 − 90/365` | setting the wait to zero moves the anchor's `Σ net_cf` by ₩25,804.50, or 0.05% |
| `breast_share_m` / `_f` | 0.005 / 0.268 | 유방 29,871 cases over the female burden less the 19.0% that is 갑상선 [REG-R40]; a registry share is on 만나이 but a *share* is insensitive to the half-year | male breast cancer is under 1% of breast cases; the male figure is a rounding error and the female one is 17.86% of year-1 accelerations |
| `mort_ci_factor` | 3.00 | **the single largest unsourced number in the model.** No Korean post-CI mortality is published; anchored qualitatively on 69.6% five-year cancer survival excluding thyroid [REG-R40] | none; point 9 runs 2.00, and the effect is **not monotone** — it moves `claims_death_ci` and the cohort's size in opposite directions |
| `lapse_ll_first` | 0.10 | the 원칙모형's two endpoints are supervisory [REG-R27] [R3]; its start and the interpolation between are not, and the guideline's functional form is [unverified] at instrument level | the disclosed 적용해지율 envelopes Korean 상품요약서 publish for protection business, 0%–13.4% at one carrier and 1%–10% at another |
| `lapse_table.csv` | 0.09 → 0.028 | the 표준형 comparison curve, carried because the guideline requires the departure to be disclosed against it | as above; **no CI lapse experience of any kind was retrieved** [R1] |
| `lapse_ci_factor` | 0.50 | a post-CI policy is premium-waived and paid-up by construction | nothing retrieved bears on it, and **the direction is genuinely ambiguous** — no premium to fund argues down, a doubled surrender value argues up |
| `waiver_rate` | 0.03% p.a. | the residual 장해 50%+ limb only; the CI limb of the waiver is already inside `ci_rate` | no Korean inception rate at the 50% 장해지급률 threshold is published |
| `expense_acq` | ₩500,000 at issue | no Korean carrier publishes an expense basis at all — [S1] names 계약체결비용 and 계약관리비용 and quantifies neither | bounded above by three public handles the model sits inside: the 표준해약공제액 ₩3,944,704 [REG-R20], the 보험료지수 130.1% [S3], the 2019 사업비 reform [REG-R29] |
| `expense_maint` | ₩5,000 **a month**, on the **total** in force, for life, inflating on the 계약해당일 | a post-CI policy costs the same to administer as a pre-CI one; there is no separate surrender expense, it is folded in here | as above |
| `expense_claim` | ₩300,000 per claim event | charged on CI, pre-CI death and post-CI death alike — probably generous on the CI event, whose whole dispute record is about adjudication | as above; charging it on deaths alone under-states the stream by 44% |
| `inflation_rate` | 1.0% p.a. | over a 71-year horizon 1% compounds to 2.01 and 3% to 7.92, so importing a Western rate produces a different product rather than a stressed one | no published Korean expense basis to anchor either figure |
| `comm_init_rate` / `comm_renewal_rate` | 0.80 / 0.03 | the initial rate sits below the 1,200% rule's one-annual-premium first-year cap [REG-R29], and renewal follows premium **actually collected**, so neither the waived subset nor the post-CI cohort produces any | none published |
| premium scale, the eight non-anchor points | anchor loading 1.2399868 × the published form factor | keeps every point on one rule, so a premium hand-edited into the CSV fails the suite rather than drifting quietly | published form factors: 1.10224 기본환급형 [S4], 1.000 저해지, 0.937 무해지 **[std]** |
| processing order | premium → CI → death → lapse, on the **monthly** conversions | the CI transition must precede death: the CI rate is 4.09× the death rate in policy year 1 and 7.40× at attained 60, so reversing them re-routes claims wholesale | nothing in any retrieved document states a processing order |
| monthly conversion | `1 − (1 − q)^(1/12)` on every tabulated annual probability | twelve months then compound back to exactly the year's rate; `q/12` does not, and differs by 4.9% of the first year's lapse rate | the terminal age, where `q = 1` and the certain death is spread as `1/(12 − j)`; and the 보장개시일, which is placed rather than converted |
| `roll_fwd_tol` / `val_tol` | 1e-10 / 1e-08 scaled by `sum_assured()` | one closes an identity between policy counts; the other compares won amounts of order 1e8 | `val_tol × SA` is ₩1 at the anchor, far below the smallest error a reader adding up the statement could see |

**One row above is not a standardization at all and is listed only so it is not looked for
elsewhere**: the two endpoints of the `log_linear` lapse basis, 0.1% at 납입완료 and 0.8%
after it, are prescribed by the supervisor [REG-R27] and are sourced. What is [std] is the
10% start, the interpolation between the endpoints, and the reading that the guideline's
model is log-linear at all — the 보도자료 values were retrieved and the HWP attachment
carrying the functional form was not.

## Tests

`tests/test_ci_insurance_kr.py` holds the notes' worked example **hard-coded as
module-level tables**, so that a reviewer can lay it beside the notes and compare by eye
rather than by re-running the model. Money is asserted to the two decimal places of the won
that the notes print, in-force counts and rates to ten decimals, and the decrement totals to
ten.

- **The derived scalars**: `omega_age() = 110`, `proj_years() = 71`, `proj_len() = 852`,
  `ci_cover_end() = 720`,
  `disc_factor_mth()`, `epv_ben(0) = ₩45,439,079.6117764339`, `annuity_due(0) =
  178.7102998490` months, `prem_net_level_mth_pp() = ₩254,261.1122592268`, the equivalence
  principle `P^m × ä(0) = A0(0)` asserted rather than assumed, that twelve of each monthly
  interest rate compound back to its annual parent, and
  `result_cf().index[-1] == proj_len() − 1`.
- **The 표준해약공제액**, ₩3,944,704.00, from the 별표 14 arithmetic in full, with the 13×
  rule-of-thumb cross-check at ₩3,987,620 held to its stated 1.1%.
- **The decrement basis**, policy years 1 … 25, **both** the annual rates and their monthly
  conversions, with the statement that twelve of each compound back to the annual figure —
  including that `mort_rate` at attained 40 and 60 returns [S3]'s
  anchors 0.00068 and 0.00290 unmodified, that the three headline CI rates at attained 60
  read 0.011063 / 0.004371 / 0.003999 exactly, and that `ci_rate` in policy year 1 is now the
  age-40 table sum itself, the 90-day 보장개시일 having moved to the month.
- **The 보장개시일, month by month**: zero cover in months 0 and 1, 0.0410958904 of a
  month's in month 2, one thereafter, and the twelve factors summing to
  `12 × (1 − 90/365) = 9.0410958904` months.
- **The `t = 0 … 851` cash flow statement** at the rows the notes print, to the won, and the
  undiscounted totals — ₩47,558,554.65 of premium, ₩34,187,433.63 of acceleration,
  ₩36,093,568.46 of residual death benefit and **−₩51,625,819.94** of net cash flow —
  together with the phase split, +₩30,170,319.26 over `t = 0 … 239` against
  −₩81,796,139.20 after.
- **The values run** at the same month-ends: `pol_val_pp`, `surr_chg_pp`, `cv_std_pp`,
  `cv_pp`, `cv_pp_ci` and `resid_db_avg_pp`, including `surr_chg_pp(0) = SC*`,
  `surr_chg_pp(84) = 0`, `pol_val_pp(0) = 0`, `cv_pp(14) = 0` with `cv_pp(15) > 0`, and the
  loan-room doubling at every month-end inside the 납입기간.
- **The decrement split**: 0.1400281094 + 0.4045046008 + 0.4326271583 + 0.0228401315 = 1
  exactly, with `pols_ci` at 0.4273447323 **outside** that sum, and the post-CI peak of
  0.2178167855 at `t = 420`.
- **The two cross-checks that fell out of the model** rather than being fitted: the 80%
  form at 1.0782 times the 50% form against [S4]'s published 1.085, and the cap agreement
  above.

Every entry in the notes' **Known modeling pitfalls** list has a test of its own, named
after the pitfall, because each is a way an implementation can look right and be wrong: the
acceleration as a transition and not an exit; the two-sided residual floor and its two
clocks; the collapsed cohorts, asserted on `point_id = 2` and `4` where cohort 0 is
material and not only on the anchor; the CI decrement inside the premium annuity; the
post-CI cohort paying nothing; the carve-out at the month-ends rather than on the totals;
the step at 납입완료 as exactly `1/k` on one month-end and not the 2.0103 adjacent-month
ratio; the
step's independence from the surrender charge; the 표준해약공제액 on the pre-acceleration
sum assured; CI before death before lapse; the one-**month** lag between the two payments;
the three end dates; `ci_rate` as a first-event rate; the absence of a survival period;
`pols_if` as the total in force; the claim expense on three events; the zero floor on every
loan-netted payment; the monthly decrements compounding back to the annual ones; and the two
decrement tables not being the chassis's.

Beyond those: all **nine** `check_*` identities on all nine model points, each optional
module in **both** positions of its switch, the `result_cf()` column vocabulary and its
five `claims_*` splits with no aggregate `claims` column, the sensitivities the notes
quantify, the CSVs' encoding and both decrement files' row-by-row provenance tags, an input
swapped by repointing a filename Reference, and a read → write → re-read round trip against
the same golden values.

The nine checks, and what each would catch:

| Check | What breaks it |
|---|---|
| `check_pols_roll_fwd` | an exit that is not one of the four — most likely the acceleration counted as one |
| `check_ci_state_roll_fwd` | a policy leaving one state and not arriving in the other |
| `check_decrement_sum` | a residual population, or a tail state |
| `check_pol_val_roll_fwd` | the CI decrement left out of the premium annuity |
| `check_accel_complement` | an acceleration that adds or destroys cover |
| `check_resid_floor` | a one-sided `max`, or the floor read off the wrong month |
| `check_cv_carve_out` | the suppression applied to the post-CI cohort |
| `check_loan_roll_fwd` | a loan balance not accumulating at the monthly equivalent of `i_loan` |
| `check_net_cf` | a benefit kind missing from the published statement |

`tests/test_model_conventions_kr.py` adds the house style, parametrized over
`kr_registry.MODELS` rather than restated here: the two-Space layout, the external inputs
read once per model with no orphan CSV, the `provenance` column on every assumption CSV,
the docstrings and their required phrases, the age basis in the registry metadata against
the `Projection` docstring, the `result_cf()` contract — indexed by `t`, first column
`pols_if`, a `net_cf` column, all names `lower_snake_case`, no NaN, an index that is exactly
`range(index[0], proj_len())` so that `index[-1] == proj_len() − 1` — and that every
`check_*()` returns `True` on **every** shipped model point.

```bash
python -m pytest tests/test_ci_insurance_kr.py -q
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-ci_insurance-r1
[R11]: #krlib-ci_insurance-r11
[R3]: #krlib-ci_insurance-r3
[REG-R10]: #krlib-reg-r10
[REG-R11]: #krlib-reg-r11
[REG-R13]: #krlib-reg-r13
[REG-R16]: #krlib-reg-r16
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R21]: #krlib-reg-r21
[REG-R25]: #krlib-reg-r25
[REG-R27]: #krlib-reg-r27
[REG-R29]: #krlib-reg-r29
[REG-R3]: #krlib-reg-r3
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R38]: #krlib-reg-r38
[REG-R4]: #krlib-reg-r4
[REG-R40]: #krlib-reg-r40
[REG-R42]: #krlib-reg-r42
[REG-R48]: #krlib-reg-r48
[REG-R55]: #krlib-reg-r55
[REG-R60]: #krlib-reg-r60
[REG-R61]: #krlib-reg-r61
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
