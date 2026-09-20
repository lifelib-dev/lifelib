# Implementation Notes

**Status:** Draft, 2026-09-03. Built from [`technical-notes.md`](technical-notes.md) (the
product as a liability cash flow projection on paper) and [`product-spec.md`](product-spec.md)
(the representative contract those notes model). Source tags resolve against
[`sources.md`](sources.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The contractual
> mechanics are sourced: the charge schedule as percentages of the 기본보험료 (*gibon
> boheomryo*, basic premium) [S1], the nil 해약공제액 [S1], the death benefit as the
> 계약자적립액 (*gyeyakja jeongnibaek*, policyholder account value) and nothing more [S1]
> [S2] [S4] [S6], the 100.1%-of-premiums minimum fund at the 연금개시일 [S2] [S4] [S7], the
> two annuity forms and their two different bases [S1] [S2] [S6], the 0.5%
> 연금수령기간 관리비용 [S1] [S7], and the 공시이율 / 최저보증이율 machinery [S1] [S2] [S4]
> [S13] [REG-R16] [REG-R18]. **The mortality basis is not a published table.** 경험생명표 is
> produced by 보험개발원 and released only as summary statistics [REG-R33] [REG-R34] [R16]
> [R17], so `mort_table.csv` is a **[std]** construction and says so on every row. The lapse
> curve, the best-estimate mortality factor, the cash expenses and the policy-loan rate are
> standardizations. Replace them all with company data, and the mortality with the filed
> 산출방법서 basis, before drawing any conclusion from the numbers.

`Pension_KR_S` is the monthly-grid model of the tax-qualified pension savings composite
(*yeongeum jeochuk boheom*, 연금저축보험). It inherits the **surrender-value machinery** of
the [whole life chassis (종신보험)](../whole_life/model.md) — the 해약공제액, its statutory
cap and the 해약환급금 floor — but **not** that chassis's 계약자적립액 recursion, which is a
net-level accumulation with a survivorship release where this one is a plain account (next
section). It adds the five things the notes specify for the first time in the library:
crediting at a declared rate over a guaranteed floor, the tax layer as a behavioural driver
rather than a cash flow, the statutory 연금수령 conditions as constraints, the annuitisation
step, and the question of **which vintage** of the annuitant table the factor is struck on.

## Run it

```bash
python products/pension_savings/run.py            # the worked example's anchor cell
python products/pension_savings/run.py 9          # another model point
```

`run.py` prints the model point and its module switches, the annuitisation quantities, the
head and tail of `result_cf()`, the undiscounted totals and every `check_*()` cells. Its
output is ASCII only, so it prints on a Windows console under any code page: amounts are
written `KRW` and Korean terms are romanized. Real output below, **abridged to fit the
page**: middle rows and the all-but-constant `claim_expenses`, `commissions` and
`policy_loans` columns are dropped, the header lines are re-wrapped, and a few parenthetical
glosses and the two all-zero module and dividend fields are trimmed. No figure is changed;
run `run.py` for the unabridged text.

```text
model point 1: KR-PEN-0001 - yeongeum jeochuk boheom (tax-qualified pension savings), M40
age basis boheom nai (insurance age); t counts completed policy MONTHS from issue, 0-based
frame t = 0 .. 971 (972 rows, 81 policy years); policy year = t // 12 + 1
gibon boheomryo (basic premium) = KRW 500,000/month (6,000,000 p.a.) for 20 years,
    chuga nabip (additional) = KRW 0 p.a.
premium term ends at t = 240, annuity starts at t = 300 (age 65), payout form = jongsin
    yeongeumhyeong (life annuity) with a 10-year guarantee
modules: mortality vintage = issue   100.1% minimum fund = True   surrender charge = 0.00%
         payment holiday = 0 yrs   policy loan = False   participating = False
         lapse basis = pension   rate scenario = base   gongsi iyul at t=0 = 2.15%

cumulative premiums to t = n     = KRW 120,000,000.00
gyeyakja jeongnibaek AV(n)       = KRW 160,294,805.59
100.1% minimum fund              = KRW 120,120,000.00
annuity fund F, after the floor  = KRW 160,294,805.59
annuity-due factor               = 23.58191602
yeongeum yeonaek B               = KRW 6,763,375 p.a. (KRW 563,615 a month)
implied factor F_net / B         = 23.7004
pyojun haeyak gongjeaek (cap)    = KRW 1,421,988.72
haeyak hwangeupgeum CV(12)/prem  = 96.61%
seaek gongje (tax credit) p.a.   = KRW 990,000  [not an insurer cash flow]
gita sodeukse on surrender at 10y= KRW 10,590,733  [not an insurer cash flow]

cash flow statement, KRW per policy issued per month, income positive
   pols_if   premiums  claims_annuity  claims_death  claims_lapse   expenses     net_cf
t
0     1.00  500000.00            0.00         32.16       1624.38  202500.00  295841.44
1     1.00  498268.47            0.00         64.16       3240.39    2491.34  492470.57
...
300   0.61       0.00       343630.80          0.00          0.00    1667.10 -345297.90
...
971   0.00       0.00           58.79          0.00          0.00       0.85     -59.63

undiscounted total premiums      = KRW 94,113,902.70
undiscounted total annuity outgo = KRW 134,873,106.96
undiscounted total net_cf        = KRW -66,447,581.54

check_pols_roll_fwd()    True
check_av_roll_fwd()      True
check_cv_floor()         True
check_surr_chg_cap()     True
check_min_fund()         True
check_annuity_total()    True
check_annuity_limit()    True
check_mort_law()         True
check_net_cf()           True
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/pension_savings/Pension_KR_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the anchor cell of the notes' worked
example. `result_cf()` returns a `DataFrame` indexed by the 0-based policy **month** index
`t`, running `t = 0 … proj_len() - 1`, with `pols_if` first and `net_cf` last. `result_pols()`
publishes the decrement and value runs beside it —
the two in-force measures, the decrements that move them, and the fund, surrender value and
cumulative premiums that price them — which is where the 환급률 a Korean illustration quotes
becomes legible. `result_tax()` prints the tax layer, which is **not** a cash flow of the
insurer and is in a frame of its own for that reason. `model.Projection.doc` carries the
notes' symbols mapped to the cells names.

## The fund is an account, and there is no mortality in it

This is the structural difference from the two nearest accumulation models in this
repository, and it is not a parameter difference. `Annuity_JP_S`'s 保険料積立金 is a
net-level-premium reserve with a **survivorship release**: the premiums of those who die go
to the survivors net of the death benefit paid, so the recursion divides by `(1 - q')`. So —
and this is the trap, because it is the nearer neighbour and shares the Korean name — does
`WholeLife_KR_S`'s own 계약자적립액, which runs
`V(d) = ((V(d-1) + P·1{d <= m})(1 + i) - q·SA)/(1 - q)`, on **that** model's anniversary
index `d` (`d = 0` at issue), not on this model's period index `t`. **This** 계약자적립액
does none of that. It is a contractual balance:

```
AV(0)   = 0
AV(t+1) = ( AV(t) + NP(t) - C(t) ) ( 1 + j_c(t) )
```

a month at a time, with `j_c(t) = credit_rate_mth(t) = (1 + i_c(t))^(1/12) - 1`, and
`check_av_roll_fwd` asserts exactly that identity. `NP(t)` is the monthly 순보험료 — the
month's 기본보험료 less **both** published charges, 「「계약자적립액」이란
순보험료(기본보험료에서 계약체결비용 및 계약관리비용을 뺀 금액)를 「공시이율」로 … 적립한
금액」 [S1] [S2] — and `C(t)` is the charge taken from the fund in a month when no premium
bears it.

There is no survivorship release because there is nothing to release. Every retrieved
life-insurer 연금저축보험 pays the fund and nothing more on death before annuitisation —
「사망 당시의 계약자적립액을 지급하여 드리고 이 계약은 더는 효력이 없습니다」 [S1] [S2] [S4]
[S6] — and 감독규정 제7-60조제9호's requirement of a death benefit of at least cumulative
premiums exempts a contract whose premium term ends at 80 or below [REG-R16], which this one
does at 60. So **the insurer's deferral-phase mortality strain is exactly zero**, and with
the composite's nil 해약공제액 the death payment and the surrender payment are the same
number at every duration: `claims_death` and `claims_lapse` differ in their decrement rate
and in nothing else. A model that applies a decrement-weighted death strain here is
projecting a strain of zero and should say so rather than compute it.

Mortality enters this contract in one place, `annuity_due_factor_on`, and it is a
**longevity** exposure that begins at the 연금개시일.

## The horizon is the annuitant table's terminal age, and `proj_len()` is a count

The time index `t` is **0-based** and counts policy **months**: `t = 0` is the first
projected policy month, `age(t)` is `x + t // 12`, `pols_if(0)` is `pols_if_init()`, and the
contractual policy year is the derived 1-based label `policy_year(t) = t // 12 + 1`. The
contract has no maturity date, so nothing in it fixes a horizon; `proj_len()` derives one
from the payout form and it is the **number of projected months** — the frame's exclusive
end, `range(proj_len())` — so the last index is `proj_len() - 1`. `proj_years()` carries the
same horizon in years and `proj_len()` is always `12 * proj_years()`.

- On the **확정기간연금형** the contract pays exactly `12k` instalments and ends, so
  `proj_len() = n + 12k` and there are no tail states at all. Model point 5's last row is
  479.
- On the **종신연금형** there is no natural end, so the horizon is the terminal age of the
  annuitant table less the issue age — the last policy year at whose start anyone can still
  be alive. At the anchor cell that last year is `120 - 40 = 80`, so `proj_years()` is
  **81**, `proj_len()` is **972**, `result_cf()` has **972 rows** running `t = 0 … 971`, and
  the terminal policy year is where `q` reaches 1.

ω = 120 is a **[std]**: no Korean industry table publishes a terminal age, because no
Korean industry table is published at all [REG-R33] [REG-R34]. It costs almost nothing to
be generous with it — the last five policy years of the anchor cell's projection carry
0.0249 of combined in-force and ₩170,814 of outgo, 0.12% of the annuity total — while a
horizon short enough to bite would silently truncate a life annuity's tail. Sweeping
`range(proj_len() - 1)` — the off-by-one of reading the exclusive end as the last index
and then subtracting — drops exactly that terminal row; the slip in the other direction,
`range(proj_len() + 1)`, appends an empty row at `t = 972` instead.

At the terminal age the table's `q` is 1, which a monthly grid cannot apply as a monthly
rate. `mort_rate_mth` spreads the certain death uniformly over the twelve months of that
policy year — `1 / (12 - t mod 12)`, so 1/12 in month 960 rising to 1 in month 971 — which
is the uniform distribution of deaths and is what makes the last row of the frame the row
where the in-force actually reaches zero.

## The monthly grid, and the annual assumptions on top of it

Every retrieved contract is 월납, interest accrues 「납입일부터 일자계산을 하여」 — from the
date each instalment is received, not from the anniversary [S1] [S2] — the account accrues
**monthly before 납입완료** under 감독규정 제7-66조제1항제4호 [REG-R19], and the annuity is
paid 매월 [S1] [S2] [S5] [S6] [S7]. The model runs a **monthly** grid, so each of those is
followed directly. The annual grid this replaced ran under the separate annualised-premium
permission of 감독규정 제7-65조제2항, 「계약자적립액은 … 연납보험료를 기준으로 하여 산출할
수 있다」 [REG-R18] — a filed-basis convention rather than a shortcut, but one the monthly
grid does not need.

**The assumptions stay annual and only the grid gets finer.** `credit_rate(t)`,
`mort_rate(t)` and `lapse_rate(t)` are the annual figures the technical notes tabulate — a
공시이율 is declared as an annual rate, the 연금사망률 is an annual table by age, and the
lapse vectors are annual by 경과기간 — and the projection applies their uniform-force
companions:

```
credit_rate_mth(t) = ( 1 + credit_rate(t) ) ** (1/12) - 1
mort_rate_mth(t)   = 1 - ( 1 - mort_rate(t) ) ** (1/12)
lapse_rate_mth(t)  = 1 - ( 1 - lapse_rate(t) ) ** (1/12)
```

Twelve of each compound back to the year's figure exactly, so **the fund and the in-force at
every 계약해당일 reproduce the annual-step model this replaced** — `av_pp` to a relative
1.4e-14, `pols_if` to the last printed digit. That equality is worth stating plainly: it
means the sub-annual timing factor the annual grid carried, `u(t) = (1/12) Σ (1 + i_c)^(−j/12)`
= 0.990316187680581 at 2.15%, was exactly right, and the monthly recursion has replaced it
rather than corrected it. What the monthly grid adds is everything **inside** the policy
year, which the annual grid had no way to state: a 환급률 of 95.67% after one month against
96.61% after one year, a ₩3,350 monthly charge in each of the sixty months between 납입완료
and 연금개시 instead of five annual ones, and a surrender dated to the month.

**Two conversions are deliberately not made.** The 세액공제 ceiling and the 연금수령한도 are
per-**year** statutory figures and 별표 14's 표준해약공제액 is struck on the **연납순보험료**,
so each is computed annually and apportioned across the year's twelve months rather than
restated on a monthly base the law does not use. And the 연금연액 `B` is the annual amount the
contract quotes; `annuity_pp(t)` pays `B / 12`.

**On the way out**, the annuity factor is — and always was — the annuity-due payable
**twelve times a year**. For the certain form that is exact, `(1 - v^k) / d^(12)`; for the
life form it is the annual factor less the standard `(f - 1) / (2f) = 11/24` correction.

That last point is the single most consequential implementation decision in this model,
because it is what makes the payout formula reconstruct the published illustration.
[S2] publishes a fund at annuitisation and five annuities on two interest bases, and the
implied factors are recovered as follows `[derived]`:

| Form | Published implied | Model | Basis |
|---|---|---|---|
| 확정 10년 | 9.06 | 9.061 | 공시이율 2.15% |
| 확정 15년 | 12.92 | 12.918 | 2.15% |
| 확정 20년 | 16.39 | 16.386 | 2.15% |
| 확정 10년 | 9.81 | 9.806 | 최저보증 0.50% |
| 확정 15년 | 14.53 | 14.528 | 0.50% |
| 확정 20년 | 19.13 | 19.134 | 0.50% |
| 종신 10년보증, 남 65 | 23.70 | 23.700 | 2.15% |
| 종신 10년보증, 남 65 | 31.18 | 31.180 | 0.50% |

**All eight, on both interest bases, from one formula.** Read on an *annual* annuity-due the
same `계약자적립액 ÷ ä_n(공시이율) × (1 − 0.005)` misses every one of these by about half a per
cent **in the wrong direction** — it makes the annuity smaller than published where the
published figure is larger than the textbook annual factor. That was the reading of an early
draft of `product-spec.md`; `technical-notes.md` corrected it, its scope note records the
change as a change to a number, and both documents now carry the monthly form. On the anchor
cell the annual reading would give `B` = ₩6,634,429.17 against ₩6,763,374.59, **1.91% low**.

## The crediting machinery is four rates, not one

`decl_rate(t)` is the **공시이율**, the carrier's declared rate. It is not a market rate and
must not be modelled as one: 감독규정 제7-65조제3항 and 시행세칙 별표 27 build it from an
external index rate and the insurer's own 운용자산이익률 with the external weight **capped at
60%** [REG-R18] [REG-R24], so it is majority-weighted to realised investment return. One
carrier's published thirteen-month history falls 57 basis points over a year in steps of two
to seven, never once reversing [S5]. The model therefore treats it as a slow-moving exogenous
**step function of policy year**, read from `decl_rate_table.csv` by scenario — level
across the twelve months of each policy year, not interpolated — and does not model the
조정률 at all, a discretionary carrier margin living in an unpublished 사업방법서.

`min_guar_rate(t)` is the **최저보증이율** ladder, 1.25 / 1.00 / 0.50 at five and ten years
— months 60 and 120 on this grid — [S1] [S2] [S13]. It steps *down* with elapsed duration on every retrieved contract, so the
guarantee is strongest exactly where the fund is smallest, and the ladder is a function of
the product's **판매개시일 rather than of the carrier** — one carrier's shelf runs two
ladders side by side [S13].

`credit_rate(t)` is the greater of the two, and it is what the fund actually earns, through
its monthly companion `credit_rate_mth(t)`. The floor
is a guarantee on the **credited rate**, not on the return: 「공시이율이 0.1%로 낮아지더라도
적립금은 … 최저보증이율로 적립됩니다」 [S8], and expenses are still deducted beneath it [S4].
That is why `charge_from_av_pp` never consults the floor.

A fourth rate is in the model and is neither of these. `prem_int_rate` is the **예정이율**,
연복리 2.50%, the rate the charge and benefit structure was priced on [S1] [S5] [S7]; it is
not a guarantee, its own sources say so, and it appears nowhere in the fund recursion. The
library's retired-name register keeps `prem_int_rate` and `decl_rate` apart for exactly this
reason. A fifth, `avg_decl_rate` — the **평균공시이율**, 2.50% for 2026 [REG-R48] [S14] — is
a supervisory average and enters only as a constraint, inside `surr_chg_cap_pp`.

## The surrender value, and the statutory cap nobody uses

`cv_pp(t) = max(0, AV(t) - SC(t))`, the floor being 감독규정 제7-66조제1항제1호 [REG-R19],
and `check_cv_floor` asserts it. On the composite `SC(t)` is **zero at every duration**,
because the direct-channel product whose complete schedule the composite adopts publishes a
해약공제 table of all zeros [S1] — a design that recovers its acquisition cost entirely
through the level monthly charge and has nothing left to claw back. So `cv_pp == av_pp`
everywhere on the base run, which is a property of the adopted schedule and not of the
product: model point 8 carries the state postal insurer's front-end 해지공제액 instead, 8.67%
of the annual premium at year 1 running off to zero at year 5 [S7], and the two separate.
That schedule is published **by policy year**, so `surr_chg_pp` interpolates it linearly in
the elapsed duration `t / 12`: the published amounts come back exactly at each 계약해당일,
the first policy year carries the year-1 figure throughout, and between anniversaries the
charge falls month by month instead of in four steps.

`surr_chg_cap_pp` computes 별표 14's **표준해약공제액** and `check_surr_chg_cap` holds the
charge inside it on every model point. The computation follows the notes to the letter: 주2
caps the 저축성보험 coefficient at a twelve-year premium term, 주3 defines the 연납순보험료 as
the annual premium less the whole-term loading levelled over the payment term capped at ten
years, 주5 replaces the general 5% with **3% for a 무배당 연금저축보험 and 4% if 배당** —
`par()` reads this — and 주6 subtracts the acquisition amount loaded into the premium
discounted at the 평균공시이율 [REG-R20] [R14]. 주4's 6% concession for a whole-of-life
survival annuity is expressly **denied** to a 연금저축보험, and the second term of the
formula, 보장성보험의 보험가입금액의 10/1000, is nil because the contract has no 보장성
element.

On the anchor cell the model returns **₩1,421,988.72**, about 2.8 months of 기본보험료 and
the order of magnitude 금융위원회 stated for a 저축성보험 in 2019 [REG-R29]. The composite
uses none of it. That is the finding: the regulator has singled this product out for the
tightest surrender-charge coefficient in the schedule, and the reference implementation sits
far inside it. Where 주3 is read the other way — levelling only the first ten years' loading
rather than the whole term's — the cap is **₩1,486,788.72**, 4.56% higher; the model
implements the first reading and the alternative is a one-line change to `surr_chg_cap_pp`.

## The annuitisation transition, and which vintage of the table it is struck on

At `t = n` the fund is fixed, floored at 100.1% of premiums paid, and divided by a factor.

The floor is real if shallow. 「연금개시시의 계약자적립액은 이미 납입한 보험료의 100.1%를
최저보증 합니다」 [S4 별표1 주10] [S2] [S7], with two more carriers writing the functionally
identical 「이미 납입한 보험료 + 1,000원」 [S5] [S6]. Why 100.1% and not 100%: 감독규정
제7-60조제2호 requires a 저축성보험's survival benefits to **exceed** premiums paid
[REG-R16]. It is a **survival** guarantee — a death claim in deferral is not floored at
premiums on this composite — and on the published guaranteed-rate illustration the fund
reaches only 100.5% of premiums at the end of the twenty-year payment term [S2], so on a
persistently low-rate path the floor is close to binding. `check_min_fund` asserts it. Model
point 6 is the one shipped point where it **binds exactly**, at ₩30,030,000 against an
`av_pp(60)` of ₩29,573,776.73; model point 9 carries it **withdrawn**, which is what the
contracts do where a payment holiday or a one-instalment reinstatement caused the shortfall,
deferring the annuity date instead [S4] [S6] [S7].

The factor is where the composite has to take a position the evidence does not settle. Six
independently retrieved contracts carry the same clause — 「연금개시전에 연금사망률의 개정
등에 따라 연금연액이 **증가**하게 되는 경우 연금개시시점의 연금사망률 … 을 기준으로」 [S1
주6] [S2] [S4 별표1 주11] [S6 별표1 주10] [S9 별표2 주9] [S10 주4] — and every version shares
two elements: the trigger is a revision that **increases** the annuity, and the substituted
basis is the table 연금개시 당시. The clause is therefore a **one-way ratchet in the
policyholder's favour**, so the base factor must be something else, and the only candidate is
the annuitant mortality in the 산출방법서 filed for the product — the table **as at 가입**.
Two carriers publish the 연금사망률 in the 상품요약서 handed over at inception [S1] [S7],
which corroborates it, as does trade reporting that a 경험생명표 revision reaches new
business only [R18] [R20].

`mort_vintage` exposes all three readings:

| Value | Behaviour | Model point |
|---|---|---|
| `issue` | the 가입시점 table; the composite's reading | 1–6, 8 |
| `commencement` | the 연금개시시점 table | 7 |
| `ratchet` | the clause itself: whichever vintage gives the **larger** annuity | 9 |

Because successive revisions have **lightened** mortality — the 제10회 raised 평균수명 by 2.8
years for men and cut the monthly annuity on a fixed fund by about 15% [R18] [R19] [REG-R33]
— a revision normally *decreases* the annuity, the ratchet does not bite, and `ratchet`
returns the issue vintage. Model point 9 demonstrates that it does: `mort_table_name()`
returns `annuitant_issue`, because the issue-vintage factor of 22.70113 is smaller than the
revised-vintage 23.43728 and the smaller factor is the larger annuity. The vintage is worth
**2.97%** of the annuity (points 1 against 7), which is why it is a switch and not an
assumption: a model that struck the factor on the 개시시점 table would understate the
annuity, and a model that ignored the ratchet would be right in the base run and wrong under
an improvement scenario.

## The mortality table is a construction, and it ships with its recipe

**No qx table of any Korean industry basis was retrieved in either research pass.** 보험개발원
holds the statutory office of 보험요율산출기관 under 보험업법 제176조 and files 참조순보험요율
with the supervisor with **no publication obligation** [REG-R4] [R16]; the 제10회 경험생명표
is public only as 평균수명 남 86.3세 / 여 90.7세 and 65세 기대여명 남 23.7년 / 여 27.1년
[REG-R33] [R18] [R19]. The KIDI press-release page is JavaScript-driven and the release could
not be opened [R17] [REG-R34]; the big-data portal refused connections [R24].

What *is* public, and what the table is anchored on, are the six annuitant rates two carriers
publish in their statutory product summaries [S1] [S7]. `mort_table.csv` is a Makeham law
`mu(x) = A + B c^y` with `y = max(0, x − setback)`, fitted jointly to those six and to the
annuity factors [S2] implies at **two** interest bases, with the parameters, the female
setback, the vintage improvement factor and the six published anchors all recorded in
`mort_anchor_table.csv`.
`check_mort_law` re-derives every rate the projection reads from those parameters, so the day
someone drops in a real basis the check reports it rather than the model silently claiming a
construction it no longer has.

Three things about the fit are worth stating plainly, because they are the cost of taking the
published illustration as the calibration target:

- **The two ä targets are met to four significant figures and the anchors are not.** The
  model's implied life factors are 23.7004 and 31.1799 against published quotients of 23.7000
  and 31.1768 — inside the rounding of the 만원 figures [S2] publishes. The fitted male rates,
  by contrast, run about 30% above the published anchors at 70 and about 28% below at 80. A
  three-parameter law cannot honour a steep 60–80 gradient and a very light 65+ tail at the
  same time, and the annuity factor is dominated by the tail.
- **The implied longevity is extreme, and it is the illustration's, not the model's.** The
  fitted table gives a male 65 a curtate expectation of life of **33.31 years** against the
  제10회's own published 23.7 [REG-R33] and 국가데이터처's 완전생명표 19.5 [REG-R38]. That gap
  is what the calibration target requires: solving ä_n = 23.70 at 2.15% on the **monthly**
  annuity-due this model uses gives n ≈ 32.9, so the published life annuity is priced like a
  certain annuity running to about age 98 `[derived]` from [S2] — 32.5 and about 97 on the
  annual annuity-due, which is not the form this contract pays.
  A 연금사망률 is a **pricing** table loaded on the survival side for a
  longevity product, and this is what that loading looks like when it is read off a published
  annuity rather than assumed.
- **The female table is the male law set back four years**, the whole-year setback closest to
  the published 65세 기대여명 gap of 3.4 years between the sexes [REG-R33]; it does not
  reproduce it — the model's own gap is **3.66** years. The female published anchors are
  *not* reproduced either: the fitted female rates run 1.9 to 2.8 times the published ones at
  ages 50 to 70. The alternative — fitting the female law independently to the female anchors
  and to the one published female annuity illustration [S5] — was tried and rejected, because
  it comes from a different carrier on a different convention and produces a **female annuity
  larger than the male's at the same age**, which no carrier's rate card does. The sourced sex
  differential was preferred to the sourced female rates, and the reason is written on every
  female row of the file.

`mort_be_factor` is **1.15** and is greater than one deliberately. The table is a loaded
pricing basis, so a best-estimate *death* decrement runs heavier than it, not lighter. The
only direct evidence of the margin's size is that the two carriers who publish annuitant
rates differ by about 9% at age 60 [S1] [S7] `[derived]`; 1.15 sits a little above that and
is a standardization.

**This table must not be shared with `WholeLife_KR_S`.** One is loaded for survival and the
other for death, and using either for both is wrong in a known direction.

## Two decrements that pay the same amount, and three columns that are zero

`result_cf()` publishes nine columns beside `pols_if`, and four of them state a product fact
rather than carry a number.

**`claims_death` and `claims_lapse` are the same benefit under two decrements.** Both pay
`db_pp_net(t+1)` and `cv_pp_net(t+1)`, which are the same number at every deferral duration
on this composite, so the columns differ only in the rate applied and their ratio is exactly
`(1 − q^m(t)) w^m(t) ÷ q^m(t)` — surrenders are taken from the survivors of mortality, so the
`(1 − q^m)` belongs in the identity even though it does not move the displayed figures. At the
anchor cell that runs from **50.5** at `t` = 0 to **3.8** at `t` = 299 as mortality rises
against a lapse rate that steps down, and the two totals come to a ratio of **8.93** over
the whole deferral phase. Splitting them is still right:
the two are separable the moment a model point carries a 해지공제액, as point 8 does.

**`commissions` is zero in every row and is published anyway.** The composite follows a
direct-channel product whose published 모집수수료율 is 0.00% in every year [S1]. A zero
states the fact; a missing column would only hide it, and would make the reader wonder
whether Korean acquisition cost had been forgotten rather than sourced. It is also why the
projection's **month** 0 is positive at **+₩295,841.44** — there is no commission at all, so
a single ₩500,000 instalment still covers the whole ₩200,000 cash expense and the month's
decrements, the acquisition charge living inside the fund. On an annual grid the same
statement was made against a whole year's ₩6,000,000 and proved much less.

**`policy_loans` is zero in the base run** because `loan_on` is off, for the reason given
under the module table below: the rate is the one parameter that had to be invented.

**There is deliberately no `claims` column.** The statement publishes the `claims_*` split so
that its columns sum to `net_cf`; the `claims(t, kind)` cells stays, and is what the split
columns call. `pols_maturity` is likewise a count and never a payment — the contract does not
mature, it annuitises — but the in-force roll-forward does not close without it on the
확정기간연금형 form, where the survivors of the last instalment neither die nor surrender.

## The tax layer is carried and is not a cash flow

`krlib` models contractual cash flows. The tax layer is in this model in full because it
drives the two behavioural assumptions the product cannot be modelled without — whether the
saver persists, and whether the saver annuitises for life — and it is kept out of `net_cf`
because none of it passes through the insurer's account.

- `tax_credit_pp(t)` is the **세액공제**: 15% of contributions where 종합소득금액 is
  ₩45,000,000 or less and 12% otherwise, on up to ₩6,000,000 a year, grossed up for the 10%
  지방소득세 to the 16.5% / 13.2% every consumer document quotes [R1 제59조의3제1항](#krlib-pension_savings-r1) [R8]
  [R10] [REG-R56]. The grossing-up is **[unverified] arithmetic on a verified base**: the
  지방세법 was not retrieved. It is a **credit and not a deduction**, so the after-tax value
  of a contribution *falls* with income — the opposite of every other market in this
  repository. At the anchor cell it is ₩990,000 a year, and the anchor premium of ₩6,000,000
  sits exactly on the cap. The cap is a **per-year** figure, so the monthly grid apportions
  the credit over the year's twelve months: `tax_credit_pp(t)` is ₩82,500 a month.
- `surr_tax_pp(t)` is the **16.5% 기타소득세** on a 연금외수령 [R3] [R5], stated identically
  by nine carrier documents. One carrier's surrender illustration carries a 세후지급 예상액
  column that is uniformly **83.5%** of the surrender value at every duration and on both
  interest bases [S5] `[derived]` — exactly 1 − 16.5%.
- `pension_tax_rate(t)` is the withholding on pension income: 5.5% / 4.4% / 3.3% by 만나이,
  and a flat **3.3% for a 종신계약** from 2026-01-01 [R5] [R9] [R21] [REG-R56]. That is a
  dated, quantified 2.2-percentage-point standing advantage to annuitising for life. One
  caution: 종신계약 is defined by 소득세법 시행령 제187조의2, whose **operative text could not
  be retrieved** [R7], so whether a guarantee period of any length preserves the status is
  **[unverified]**.
- `annuity_limit_pp(t)` is the **연금수령한도**, `평가액 / (11 − 연금수령연차) × 120/100`,
  disapplied from 연금수령연차 11 [R6 제40조의2제4항](#krlib-pension_savings-r6) [S3]. It is a
  per-year figure too, so `check_annuity_limit` asserts that no 연금수령연차's **twelve**
  instalments breach it. At the anchor cell it does not bind at all — a contract taken out
  at 40 could first have drawn at 55, so by 65 the counter has reached 11 — which is exactly
  why the composite annuitises at 65 and states the constraint for the ages at which it does
  bite. Model point 6 annuitises at 55, where the first-year limit is 12% of the 평가액.

`result_tax()` publishes all four beside `cv_pp` and `annuity_pp`. Adding any of them to
`result_cf()` breaks `check_net_cf()` immediately, which is the point of keeping the two
frames apart rather than trusting a comment.

## Why the lapse assumption is not the savings lapse assumption

**There is no public Korean lapse statistic for 연금저축보험 by policy year.** One carrier's
regulatory disclosure carries a 경과기간별 중도해지율 column in which every row reads
「적용안함」 [S13], the supervisor's comparison table returned a stale quarter [S19], and the
behavioural tables of the 2025 whitepaper sit in attachments that did not convert [R13]. So
`lapse_table.csv` is **[std]** and had to be argued from the contract:

1. a surrender costs **16.5%** of essentially the whole payout once the contributions have
   been credited [S5] [S8] — nothing else in this repository's savings products has a
   comparable frictional cost;
2. netting the credit taken against the charge paid, the saver's tax cost of surrendering is
   16.5% × (환급금 − cumulative contributions) `[derived]`, which is *negative* while the
   환급률 is under 100% and positive after — so the expense friction and the tax friction do
   not overlap, they hand off, at almost exactly the duration at which the surrender value
   passes premiums paid;
3. part of what looks like lapse is **계좌이체** to a 연금저축펀드 or an IRP, which is not a
   withdrawal and is not taxed [S1], and the market moved that way hard in 2025 — funds
   +50.7%, insurance −1.2% [R13] [R22].

The shipped `pension` vector is therefore materially flatter than a savings vector, and the
`savings` basis is carried beside it so the two can be run side by side; model point 5 uses
it, and reaches its annuity date with 0.3831301998 in force against the anchor cell's
0.6096911403. The supervisory 무·저해지 lapse guidance [REG-R27] is **not** used: it is
calibrated to 순수보장성 and 무해지 protection business, and this contract has a full
surrender value from the first month and no cliff at 납입완료.

Lapse is **absorbing**. 부활 and 간편부활 are real, common and specific to this product family
— within three years, and the simplified form takes the lapsed months' charges out of the fund
[REG-R25 제27조](#krlib-reg-r25) [S1] [S5] [S7] [S8] — but a premium unpaid at `t` terminates
the contract at `t`: the 14-day 납입최고 state collapses into the month rather than the year,
but it still collapses, and there is no state to re-enter from.
So `lapse_rate` here is a **net-of-부활** rate by construction, and a user substituting a
gross experience rate will over-decrement. The vector runs through `t = n − 1` and is zero
from `t = n`, because surrender is available up to the day before the 연금개시일 [S2] [S4]:
month 299 pays ₩81,886.17 of surrender benefit on the full fund, and zeroing the decrement a
month early deletes it — where on the annual grid the same slip deleted a whole year's
₩987,174.98.

## Modules that are off in the base run

Each is a model point column, so a non-anchor point exercises it and the base run stays the
worked example.

| Column | Off | On at | What it does |
|---|---|---|---|
| `payout_form` | `life_guar` | 4, 5, 6 | 확정기간연금형 over 20 / 10 / 15 years, priced on the declared rate alone |
| `mort_vintage` | `issue` | 7, 9 | the 연금개시시점 vintage, and the ratchet |
| `min_fund_on` | 1 | 9 | the 100.1% floor withdrawn, as after a payment holiday |
| `addl_prem_pp` | 0 | 8 | 연금저축추가납입특약: 계약관리비용 only, no 계약체결비용 |
| `surr_chg_rate` | 0.0 | 8 | the postal insurer's front-end 해지공제액 |
| `holiday_years` | 0 | 9 | 납입유예: premiums stop, charges continue, the annuity date defers by `12h` months |
| `loan_on` | 0 | 9 | 보험계약대출 at a **[std]** rate, drawn on the fifteenth 계약해당일, capped at the surrender value |
| `par` / `div_rate` | 0 | 9 | 배당 form: 별표 14 coefficient 4%, dividend applied as an 증액연금 |
| `lapse_basis` | `pension` | 5 | the savings comparison vector |
| `rate_scenario` | `base` | 6, 8 | the guaranteed-rate path, and the 3.5%-for-five-years hybrid |

The **policy loan rate is the one module parameter that had to be invented**, and it is marked
as such: no retrieved document gives a numeric 보험계약대출이율 for a 연금저축보험 [S1] [S2]
[S4] [S5]. The **[std]** 4.00% is set above the only published rate constraint of that kind in
the standard conditions, the 평균공시이율 + 1% ceiling on reinstatement interest [REG-R25
제27조](#krlib-reg-r25). That is why the module is off in the base run: switching it on switches on a number
nobody published.

Out of scope entirely, each for a stated reason: 계약이전 / 계좌이체 (a wrapper-level movement
rather than an insurer cash flow, carried into the lapse rationale instead), 의료비인출 and
the six 부득이한 사유 withdrawals and 배우자 승계 (real terms with a real tax effect and no
public frequency for any of them), 자유설계연금형 (needs a joint payout state and is offered
by three of eight carriers), prospective commutation by a living annuitant (retrieved only on
a variable annuity), 납입면제 (「보험료 납입면제 사유 : 없음」 [S5]), and 청약철회 /
품질보증해지 / 고지의무 (pre-inception and rescission machinery — the model begins where cover
is in force).

## Inputs are external files

### Read once, in `Data`

Nine CSVs live beside `run.py`, not inside the model, following `annuallife/TradLife_A`
rather than `basiclife/BasicTerm_S`'s embedded IOSpec. The model folder holds `__init__.py`
and `_system.json` and the two Space folders and nothing else, so a diff of the model shows
logic changes only, and an input can be swapped without rewriting a formula.

The readers and every `*_file` Reference live in the **unparameterized** `Data` Space, so
each file is read **once per model** rather than once per model point. That is not tidiness:
`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate ItemSpace
with its own cells cache, and a reader placed there would re-read all nine files for every
policy projected. `Data.input_dir()` resolves to `_model.path.parent` at run time and is
never hard-coded, which is what lets a licensed or company table drop in as a same-schema CSV
with no formula change.

The trade-off, stated in both Space docstrings: **the model is not portable on its own.**
Copying `Pension_KR_S/` without its parent's CSVs produces a model that reads and then fails
on first evaluation.

### The tables, and why each is [std] or sourced

| File | Holds | Provenance |
|---|---|---|
| `model_point_table.csv` | Nine model points, twenty-one columns, indexed by `point_id` | Configuration. Point 1 is the notes' anchor cell: its model point is the one the published illustration is struck on [S2], its charge schedule the direct-channel product's [S1] |
| `mort_table.csv` | Two annuitant vintages, both sexes, ages 0–120 | **[std]** Makeham construction on the annuitant basis. Anchored to six published rates [S1] [S7] and calibrated to the factors [S2] implies at two interest bases. **Not** a copy of any 보험개발원 table — none is public [REG-R4] [REG-R33] [REG-R34] |
| `mort_anchor_table.csv` | The law parameters, the setback, the improvement factor, ω and the six published anchors | Anchors quoted [S1] [S7]; every derived row **[std]**. This is the file `check_mort_law` re-derives the shipped rates from |
| `lapse_table.csv` | Two bases × three segments, **annual** rates by policy year | **[std]** throughout, and argued rather than fitted: no public Korean lapse statistic for this product exists [S13] [S19] [R13]. The projection applies `lapse_rate_mth` |
| `decl_rate_table.csv` | Three **annual** 공시이율 scenarios by policy year | `base` 2.15% is the illustration's rate [S2]; `floor` is that illustration's own second column; `hybrid` is one retrieved design [S11]. Adoption **[std]**. The projection credits `credit_rate_mth`, the monthly equivalent |
| `guar_rate_table.csv` | The 최저보증이율 ladder | [S1] [S2] [S13]; the requirement to set one at all is 감독규정 제7-60조제10호 [REG-R16] |
| `pricing_table.csv` | Charges, frequencies, 별표 14 coefficients, module parameters | [S1] [S7] for the charges, [REG-R20] [R14] for the cap coefficients, **[std]** for `mort_be_factor` and the loan and holiday parameters |
| `expense_table.csv` | Best-estimate cash expenses and commission | **[std, new here]** for the cash levels; the two commission rows are [S1], published as 0.00% in every year |
| `tax_table.csv` | 세액공제, 기타소득세, 연금소득세, the 연금수령 test | [R1] [R3] [R5] [R6] [R8] [R9] [R11] [REG-R56]; the grossing-up for 지방소득세 is [unverified] arithmetic |

Every file but `model_point_table.csv` carries a `provenance` column, and every cell in it
begins with a citation tag or the word `[std]`. That is the library's rule and, here, a
necessity: when every row of the mortality file is a standardization, a populated column says
nothing unless it names which authority the row stands on.

### The time-like columns, and why none of them moved

No shipped CSV is keyed by a column literally named `t`, and **every time-like column stays in
policy years** even though the frame counts months. That is the point of the conversion: the
contract and the assumptions are annual, and only the grid underneath them got finer, so a
year key is read as `t // 12` wherever the model consults one.

| File | Column or item | Decision | Why |
|---|---|---|---|
| `decl_rate_table.csv` | `from_year` | **unchanged, 0-based years** | An elapsed policy-year key, read as `max(y ≤ t // 12)`. Its first value is already `0`, so `hybrid`'s 3.5% "for five years" is `t` = 0…59 |
| `guar_rate_table.csv` | `from_year` | **unchanged, 0-based years** | The same elapsed key; the ladder steps at `t` = 60 and `t` = 120, which is five and ten completed years |
| `lapse_table.csv` | `from_year` | **unchanged, 0-based years** | Elapsed key on the `premium_paying` segment (0, 1, 2, 3, 5, 10), giving the **annual** rate that `lapse_rate_mth` converts. On `paid_up` and `in_payment` the single `0` row is a placeholder key, not a time at all |
| `pricing_table.csv` | `acq_charge_years` = 7, `surr_chg_years` = 5 | **unchanged, a count in years** | Durations, not indexes: the charge runs `t < 84`, i.e. policy years 1–7 |
| `pricing_table.csv` | `holiday_start_year` = 8, `loan_draw_year` = 15 | **unchanged, 0-based years** | Points on the contract's own annual axis, read as `t == 180` / `96 ≤ t < 96 + 12h` |
| `mort_table.csv` | `age` | **unchanged** | Keyed by attained 보험나이, reached through `age(t) = x + t // 12`; an age, not a time index. 보험나이 increments on the 계약해당일, so that expression is exact |
| `model_point_table.csv` | `premium_term_y`, `defer_gap_y`, `payout_term_y`, `guar_term_y`, `holiday_years` | **unchanged, counts in years** | Elapsed-year lengths, as the contract states them |
| `model_point_table.csv` | `issue_age`, `annuity_start_age` | **unchanged** | Ages in 보험나이, not points on the time axis |

What changed is `proj_len()`, which is now `12 * proj_years()` — the number of projected
**months** — and the derived month counts `prem_end_t()` and `annuitisation_t()`. All of them
are derived cells; no input moved.

## Sign convention

`net_cf` is **income positive**, the library-wide sign, and the technical notes print the
stream the same way round, so there is no `liability_cf` companion — that absence is a fact
about which orientation the notes chose, not an omission. A reader comparing the payout years
with a model whose notes print outgo-positive must flip the sign: this model's payout rows
are large negatives.

The identity `check_net_cf()` asserts, in one line:

    net_cf(t) = premiums(t) - claims_annuity(t) - claims_death(t) - claims_lapse(t)
                - expenses(t) - claim_expenses(t) - commissions(t) - policy_loans(t)

for every `t` in `0 … proj_len() - 1` — that is, the columns `result_cf()` publishes add up
to the `net_cf` column it publishes beside them, and nothing else (the tax layer above all) is
folded in. `check_net_cf_resid(t)` is the signed residual.

The shape is a positive ₩295,841.44 at `t = 0`, 240 months of thinning positive margin
as surrender outgo grows against a level premium base, sixty thin negative months through the
gap totalling −₩6,054,921.77, and then 672 months of pure outgo. Undiscounted the anchor
cell sums to **−₩66,447,581.54**; discounted at the monthly equivalent of the rate the fund
itself credits it is +₩3,580,561.01 `[derived]`.

## Naming

The cells names are lifelib's where lifelib has an analogue and the sister libraries' where
they do not: `av_pp` and `cv_pp` from the savings chassis, `pols_if_at(t, timing)` and
`av_pp_at(t, timing)` for the within-year reads, `claims(t, kind)` with an uppercase kind,
`check_*` / `check_*_resid` for the identities, `roll_fwd_tol` for the tolerance, and
`mort_rate` / `lapse_rate` / `credit_rate` for the **annual** assumptions with `_mth`
companions for the monthly conversions the projection applies — the same pairing the other
monthly `krlib` models use. The full mapping
from the notes' actuarial symbols to the cells names is the table in the `Projection`
docstring, headed `Notes symbol`. Four Korean concepts needed a decision, and the cross-model
naming review settled them:

| Concept | Name | Not | Why |
|---|---|---|---|
| 공시이율, the declared crediting rate | `decl_rate` | `gongsi_rate` | It is the same quantity `delib` spells `decl_rate` for the laufende Verzinsung; a transliterated name would hide the analogy for no gain |
| 예정이율, the pricing rate | `prem_int_rate` | `yejeong_rate`, and above all not `decl_rate` | Two different rates, one of which appears nowhere in the fund recursion. The retired-name register keeps them apart |
| 해약공제액 | `surr_chg_pp` | `surr_charge_pp` | The library's settled abbreviation; `_pp` because it is per policy |
| 표준해약공제액, the statutory cap | `surr_chg_cap_pp` | — | Named for what it is — a cap on the line above — rather than for 별표 14, so the pair reads as one mechanic |

Three further names carry a distinction the notes make in prose. `credit_rate` is not
`decl_rate`: it is the greater of the declared rate and the floor, and it is what the fund
earns. `annuity_amount_pp` is not `annuity_pp`: the first is `B`, struck once at `t = n` and
never recomputed, and the second is the instalment payable in a given year, which is `B` or
zero. And `pols_if` is not `lives_if`: inside the 보증지급기간 the obligation is
unconditional, so `pols_if` is flat from `t` = 300 to 419 while `lives_if` falls from
0.9657433263 to 0.9252034626, and not one of those deaths moves a won.

## Standardizations used

Every quantitative parameter is either source-tagged in a CSV `provenance` column or marked
`[std]` there, and every one below is repeated in `technical-notes.md` at the point it is
introduced. The observed range is what the retrieved documents actually bracket; a dash means
nothing public brackets it at all.

| Parameter | Value | Rationale | Observed range |
|---|---|---|---|
| Makeham `A` / `B` / `c` | 5.5583e−04 / 2.3281e−06 / 1.108956 | No Korean industry table is published [REG-R4] [REG-R33] [REG-R34], so the model ships a construction plus its recipe, fitted jointly to six published rates [S1] [S7] and to two published annuity bases [S2] | Six rates only: 연금사망률 at 50/60/70 [S1], 개인연금사망률 at 40/60/80 [S7] |
| Female table | Male law **set back 4 years** | The whole-year setback closest to the published 65세 기대여명 gap of 3.4 years [REG-R33]; it does not reproduce it — the model's gap is 3.66 | An independent female fit gives a female annuity **larger** than the male's, which no rate card does |
| `annuitant_revised` vintage | Issue vintage × **0.85** | One-step lightening of the order the 제9회 → 제10회 revision produced | That revision cut the monthly annuity on a fixed fund by about 15% [R19] |
| Terminal age ω | **120** | No Korean industry table publishes one [REG-R33]; the generosity costs ₩170,814 of tail outgo over `t` = 76–80, 0.12% of the annuity total | — |
| `mort_be_factor` | **1.15** | A loaded pricing basis on the survival side, so a best-estimate death decrement is **heavier**, not lighter | The two carriers publishing annuitant rates differ by about 9% at age 60 [S1] [S7] |
| `lapse_rate`, `pension` | 4.0 → 1.0% by duration, 0% from `t = n` | Argued from the 16.5% friction [S5] [S8] and from 계좌이체 counting as termination [S1] [R13] [R22] | None public: 「적용안함」 on every row of the one carrier disclosure that has the column [S13] |
| `lapse_rate`, `savings` | 8.0 → 2.0% | The non-qualified comparison vector, carried so the two can be run side by side | — |
| Lapse absorbing | No 부활 state | The 14-day 납입최고 collapses into the month; the rate is net-of-부활 by construction | 부활 within three years is real and common [REG-R25 제27조](#krlib-reg-r25) [S1] [S5] [S7] [S8] |
| Cash expenses | ₩200,000 acquisition; ₩30,000 p.a. deferral, ₩20,000 p.a. payout; ₩30,000 per death claim; 2% inflation | Entirely separate from the contractual 계약체결비용 / 계약관리비용, which are loadings **inside** the fund; mixing the two double-counts in one direction and destroys the fund calibration in the other | No carrier publishes a cash expense basis; what is published is the loadings [S1] [S7] |
| 공시이율 adoption | **2.15%**, level, a step function of policy year | The only rate under which the published fund, the published annuities and the reconstructed factors form one consistent set [S2]; a Korean declared rate is majority-weighted to realised return [REG-R18] [REG-R24] | 2.1%–3.0%: 3.01% / 2.82% at 2026-09 [S12], 2.40% at 2026-01 [S1], 2.15% at 2025-12 [S2], 2.3% at 2024-10 [S11] |
| 조정률 | **Not modelled** | A discretionary carrier margin living in an unpublished 사업방법서 | — |
| Annuity-phase charge θ | **0.5%** of the 연금연액 | Adoption **[std]**: it is what makes the payout formula reconstruct eight published figures on two bases | 0.5% at two carriers [S1] [S7]; a third discloses none and runs about 0.6% the other way [S5] |
| 보험계약대출이율 | **4.00%**, module off | **[std] [unverified]**: set above the 평균공시이율 + 1% reinstatement ceiling, the only published constraint of that kind [REG-R25 제27조](#krlib-reg-r25) | No retrieved document gives one for this product [S1] [S2] [S4] [S5] |
| Loan draw | 50% of `cv_pp` on the fifteenth 계약해당일 | A single visible drawdown rather than a behavioural rule nothing supports | — |
| 납입유예 start | The eighth 계약해당일 | Available after three years on two carriers [S5] [S7] | Up to three spells of one year [S8] |
| Monthly conversions | `(1 + i)^(1/12) − 1` on the credited rate, `1 − (1 − q)^(1/12)` on each probability; `(f − 1)/(2f)` = 11/24 on the life factor | The contract is 월납, the account accrues monthly [REG-R19] and the annuity pays 매월, while the filed assumptions are annual | Twelve compound back exactly, so every 계약해당일 reproduces the annual-step figures this model replaced; the annuity correction is worth **1.91%** of `B` |
| 별표 14 주3 reading | Whole-term loading levelled over min(m, 10) | Neither reading is excluded by the text; the model states which it takes | The alternative gives ₩1,486,788.72 against ₩1,421,988.72, **4.56%** apart |
| 연금수령한도 평가액 | Held at the 연금개시 fund throughout | The statute's 평가액 is not defined for a converted annuity with no residual account | — |
| 만나이 / 보험나이 | Both statutory tests read off `age(t)`, which is 보험나이 | The two differ by at most one year, and the anchor cell clears 만 55세 by a decade | Material only where 연금개시나이 sits **on** 55 — model point 6 |
| 세액공제 band | **16.5%** | A contract does not know its owner's income; nothing in `net_cf` depends on it | 13.2% above ₩45,000,000 [R1] [R8] [R10] |
| Annuitisation election | 100% 종신연금형, `g` = 10 | The composite's base election; the certain form runs at points 4, 5 and 6 | Menus of 10/20/30년/100세 보증 and 5–30년 certain [S6] [S9] [S10] |
| Guarantee-period death | **Continuation at 100%**, no commutation | The unpaid guaranteed instalments are paid to the beneficiary, so the stream is unchanged | Commutation at the 공시이율 is available on every retrieved contract [S1] [S2] [S6] |
| 계약자배당 | **0.000%** declared, machinery retained | No carrier publishes a dividend rate on a 연금저축보험, and 무배당 carries the tighter 별표 14 coefficient (3% against 4%) [REG-R20] | One carrier publishes a five-year 계약자배당 history with its 기준율 [S7] |

## Tests

`tests/test_model_conventions_kr.py` asserts the house style for every model in the library:
the folder layout, the `Data` / `Projection` split, the read-once property, the docstring
contract including the `Notes symbol` map, the naming rules and the retired-name register,
`result_cf()`'s column conventions, that every shipped model point projects without NaN at
the stated length, that every `check_*()` returns `True` on every model point, and that
`read → write → re-read` reproduces the same file set and the same numbers.

`tests/test_pension_savings_kr.py` asserts what this product owes on top of that. The notes'
worked example is hard-coded there — the annuitisation quantities (`av_pp(240)` =
₩144,311,957.5668497980, `av_pp(300)` = ₩160,294,805.5909678042, `ä` = 23.58191601796395,
`B` = ₩6,763,374.5893046195, the implied factor 23.7004181085 against the published 23.70,
`surr_chg_cap_pp()` = ₩1,421,988.7174578153), the thirteen rows of policy year 1 and the turn
into year 2, the fund and surrender value at every quoted month-end, the 환급률 column, the
payout rows, the annual-to-monthly conversion round trip, the decrement table and both sets
of totals — so that a reviewer can check it against the notes by eye to the precision the
notes display.

Every pitfall the notes list earns a test named after it: the account recursion with no
survivorship release, the deferral-phase strain that is exactly zero, the best-estimate
factor whose sign is the opposite of a death product's, the decrement order
`W(t) = (l(t) − D(t))w^m(t)`, the lapse decrement that runs through `t = n − 1`, the monthly
annuity-due factor and the eight-row reconstruction above, mortality in the 종신연금형 factor
and its absence from the 확정기간연금형 one, `pols_if` flat inside the guarantee while
`lives_if` falls, `B` struck once, the maintenance charge that outlives the premium, the
acquisition charge that stops at seven years, the floor that guarantees the credited rate and
not the return, the 예정이율 that is not a crediting rate, the tax layer that is not a cash
flow, the 연금수령한도 that is disapplied at 연금수령연차 11, the 표준해약공제액 computed on
the 연납순보험료, `proj_len()` as a count rather than the last index, and the 100.1% floor
as a survival guarantee.
Each of the ten optional modules is asserted in **both** positions, off and on.

Nine `check_*()` cells assert the identities the notes imply, each taking no argument and
returning a `bool` over all `t`, with the signed per-period residual at `check_*_resid(t)`.
All nine return `True` on all nine shipped model points.

| Check | Identity |
|---|---|
| `check_pols_roll_fwd()` | `l(t) − l(t+1) = pols_death(t) + pols_lapse(t) + pols_maturity(t)` |
| `check_av_roll_fwd()` | `(AV(t) + NP(t) − C(t))(1 + j_c(t)) = AV(t+1)` over the deferral phase |
| `check_cv_floor()` | `CV(t) = max(0, AV(t) − SC(t))` — 감독규정 제7-66조제1항제1호 [REG-R19] |
| `check_surr_chg_cap()` | `SC(t) ≤ SC_max` at every duration — 별표 14 [REG-R20] |
| `check_min_fund()` | `F ≥ 100.1% × cumulative premiums` at `t = n`, where the guarantee is on |
| `check_annuity_total()` | the guaranteed instalments are level and total `kB`, or `gB` on the life form |
| `check_annuity_limit()` | no 연금수령연차's twelve instalments exceed the 연금수령한도 [R6 제40조의2제4항](#krlib-pension_savings-r6) |
| `check_mort_law()` | the shipped rates are still the [std] construction `mort_anchor_table.csv` states |
| `check_net_cf()` | the published `result_cf()` columns add up to `net_cf(t)` |

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-pension_savings-r1
[R10]: #krlib-pension_savings-r10
[R11]: #krlib-pension_savings-r11
[R13]: #krlib-pension_savings-r13
[R14]: #krlib-pension_savings-r14
[R16]: #krlib-pension_savings-r16
[R17]: #krlib-pension_savings-r17
[R18]: #krlib-pension_savings-r18
[R19]: #krlib-pension_savings-r19
[R20]: #krlib-pension_savings-r20
[R21]: #krlib-pension_savings-r21
[R22]: #krlib-pension_savings-r22
[R24]: #krlib-pension_savings-r24
[R3]: #krlib-pension_savings-r3
[R5]: #krlib-pension_savings-r5
[R6]: #krlib-pension_savings-r6
[R7]: #krlib-pension_savings-r7
[R8]: #krlib-pension_savings-r8
[R9]: #krlib-pension_savings-r9
[REG-R16]: #krlib-reg-r16
[REG-R18]: #krlib-reg-r18
[REG-R19]: #krlib-reg-r19
[REG-R20]: #krlib-reg-r20
[REG-R24]: #krlib-reg-r24
[REG-R27]: #krlib-reg-r27
[REG-R29]: #krlib-reg-r29
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R38]: #krlib-reg-r38
[REG-R4]: #krlib-reg-r4
[REG-R48]: #krlib-reg-r48
[REG-R56]: #krlib-reg-r56
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
