# Implementation Notes

**Status:** Draft, 2026-09-03. Built from
[`technical-notes.md`](technical-notes.md); the product those notes describe is specified in
[`product-spec.md`](product-spec.md), and every source tag on this page resolves in
[`sources.md`](sources.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics are sourced — the 태아가입특칙 (*taea gaip teukchik*, foetal
> enrolment special provision) verbatim [S8 제53조~제61조], the two ages a foetal contract
> carries [S8 제58조] [S8 제60조], the 면책기간 (*myeonchaek gigan*, waiting period)
> disapplied below 보험나이 15 and entirely on a 태아 cover [S3] [S11] [R5], the 감액
> removed from foetal contracts by a 2015 변경권고 [R2], the statutory bar on a death
> benefit below 만 15세 and the 계약자적립액 (*gyeyakja jeongnipaek*, policyholder account)
> paid instead [R7] [REG-R17] [REG-R25] [REG-R50], the two premium waivers with the
> P코드 carve-out [S2] [S10 제22조], the 3년만기 갱신형 liability block [S2] [S5], the
> published 해약환급금 grid and the 무해지 cliff [S1] [S2]. **Almost everything
> quantitative is a [std] standardization.** Nothing on Korean child incidence was
> retrieved from 보험개발원, 국가암정보센터 or 통계청 **in this product's own research
> pass** — the 장기손해보험 참조순보험요율 display that 보험개발원 does publish under
> 보험업법 제176조제9항, and whose age grid reaches 연령 0 and 10, was opened in the
> `cancer` and `indemnity_medical` passes and not in this one [REG-R61], so the shipped
> incidence rows are [std] as **unreconciled** constructions rather than for want of a
> public grid. The life-side 참조순보험요율 is filed and not published [REG-R4]; the
> 산출방법서 that holds each carrier's own 적용위험률 and 예정사업비율 is an undisclosed
> 기초서류 [REG-R2]; the 제10회 경험생명표 is released only as summary statistics
> [REG-R33] [REG-R34]. **Exactly one 적용위험률 is published anywhere in this
> product's source set** — 일반상해 후유장해 발생률(3~100%), 기본계약, 5세, 상해 1급:
> 남자 0.0001823, 여자 0.0001163 [S1] — and it is the calibration point of the basic
> contract's decrement. Replace the tables with company data and a real 산출방법서 before
> drawing any conclusion from the numbers.

`Child_KR_S` is the executable counterpart of [`technical-notes.md`](technical-notes.md):
a monthly, by-policy projection of gross best-estimate liability cash flows for
어린이보험 (*eorini boheom*, children's insurance). It states its deltas against the
[cancer 정액 chassis (암보험)](../cancer/technical-notes.md) rather than restating the
diagnosis machinery, and it adds two things that have no counterpart in any sister
library: **태아가입**, under which the projection opens on a life that does not yet exist,
and a **납입면제 (premium waiver) on the 계약자**, a decrement on a life who is not the
insured.

---

## Run it

```bash
python products/child/run.py            # the anchor cell, point_id = 1
python products/child/run.py 4          # the 무해지 (mijigeuphyeong) point
python products/child/run.py 9          # the 30세만기 short-term point
```

`run.py` prints the model point, the cash flow statement and the account, surrender and
decrement tables at the durations where the product does something, the undiscounted totals,
the equivalence premium and the thirteen `check_*` identities. Everything it prints is
ASCII, so the output lands on a Windows console under any code page: amounts are labelled
`KRW`, and the product, the two age bases and the three surrender-value forms are romanized.
Real output, elided in the middle — the statement is reproduced in full in
[`technical-notes.md`](technical-notes.md):

```text
Child_KR_S - eorini boheom (children's insurance), monthly grid, boheom nai
model point 1: CH-KR-0001 - sex M, taea gaip (written in utero), gyeyak nai 0, birth at policy month 5
term to boheom nai 100 (t = 0 .. 1200, 1201 rows), premium term 20 years (t = 0 .. 239), monthly
form: pyojunhyeong (standard surrender value)
premium: KRW 28,000 core + KRW 3,000 taea module to t = 16, so KRW 31,000 to t = 16 and KRW 28,000 after
napip myeonje (premium waiver) on: child + gyeyakja (M33, man nai)
...
pyojun haeyak gongjeaek (statutory surrender charge cap) = KRW 364,000.00   over 84 months
notional bohom gaipgeumaek (byeolpyo 15 no. 9) = KRW 132,306,409 from a first-year risk premium of KRW 145,537.05
acquisition cost = KRW 327,600.00 (11.70 months of premium) of which first-year commission KRW 212,940.00

      [ result_cf(), result_val() and result_pols() at t = 0, 1, 4, 5, 6, 16, 17,
        239, 240, 241, 600, 1140, 1200 ]

undiscounted totals per policy issued (KRW):
premiums              5458037.93     claims_death          3693345.73
claims_disability      957652.52     claims_lapse          2695713.64
claims_diagnosis      2844503.44     claims_maturity             0.00
claims_surgery        1094506.30     claims_void               306.90
claims_hospital       5033285.22     claim_expenses          79991.42
claims_event           466414.73     expenses              1009668.24
claims_liability       195939.36     commissions            365814.73
claims_neonatal        106330.72     net_cf              -13085435.00

equivalence on the shipped basis, at the bojang bubun applied rate of 2.75%:
  EPV of all outgo  KRW 4,694,583.11   over 151.0504 monthly premium units
  equivalence monthly premium  KRW 31,079.59   against a shipped KRW 28,000.00

checks: all thirteen True - policy count roll forward, paying / waived split, every exit
accounted for, no cover before birth, once-only benefit ledgers, taea module inside its
terms, surrender value form floor, gyeyakja jeongnipaek bounds, surrender charge under cap,
acquisition cost under cap, published hwangeuplyul grid, equivalence premium identity, net
cash flow ledger
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/child/Child_KR_S")
model.Projection[1].result_cf()      # the worked example's anchor cell
model.Projection[1].result_pols()    # the decrement run, both compartments, both ages
model.Projection[1].result_val()     # the account, the charge and the two surrender values
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell — a
**태아가입** contract, priced male, 계약나이 0 at the 계약일, birth at policy month 5, running
to a 100세 만기 with a 20년 납입기간. `result_cf()` returns a `DataFrame` indexed by policy
month `t` with one column per cash flow line, `pols_if` first and `net_cf` last; `expenses`
there is acquisition plus maintenance, with the claim handling expense in its own
`claim_expenses` column. `result_pols()` publishes the decrement run — the paying and waived
compartments and the two ages side by side — and `result_val()` the account and the surrender
values. `model.Projection.doc` maps the notes' symbols to cells names and states the age
basis; `model.Data.doc` says what each input file is and, for the mortality table, what it is
**not**. The time index `t` is the policy month and is **0-based** on the library-wide
convention: `t = 0` is the first projected month, the policy year containing month `t` is
`t // 12 + 1`, `proj_len()` is the **number** of projected months, and the frame is
`t = 0 … proj_len() − 1`. The anchor projection is **1,201 rows**, `t = 0` to
`t = proj_len() − 1 = 1200`: the
longest in `krlib`, and the product rather than an artefact of it.

## The horizon, and eighty years that are paid up

`proj_len()` is `12 × (term_age() − issue_age()) + 1`, and on a 태아 contract `issue_age()`
is zero because 「계약일에 있어서의 피보험자의 계약나이는 0세로 합니다」 [S8 제60조]. So the
projection runs 1,200 months to the 100세 계약해당일 — `t = 0 … 1199`, with the 계약해당일
itself published as the terminal row `t = 1200` — and the premium runs over the first
240 of them. **Eighty of the hundred years are paid-up**, which is the whole shape of the
liability: `net_cf(t)` is positive for twenty years and negative for eighty, and the
undiscounted total on the anchor cell is **−₩13,085,435.00** against premiums of
**₩5,458,037.93**. That is not a defect in the projection. It is what a hundred-year
contract with a twenty-year premium term looks like before discounting, and it is why
`equiv_premium_mth_pp()` exists.

The terminal date is fixed by the **계약일** and not by the birth, so the insured's 만나이
at expiry is 100 less the pre-birth period — **99 years and 7 months** on the anchor cell,
and `age_man(1200)` is 99. `result_pols()` prints `age` (보험나이) and `age_man` (만나이) in
adjacent columns so the five-month offset can be read off any row. Across the shipped points
the horizon runs 360 months (point 9, 30세만기) to 1,320 (point 6, 110세만기 from 태아), and
none of them is read off a mortality table: this is a **term** contract, not a 종신 one, so
the omega age of `mort_table.csv` has no part in setting it.

## The pre-birth period is the part with no analogue anywhere

Months `t = 0 … 4` on the anchor cell carry premium income on all three streams, a **void**
decrement, and nothing else. `born(t)` is false, so every cover on the child's own life is
identically zero and there is neither mortality nor morbidity on the insured: `mort_rate(t)`
is 0 and `age_man(t)` returns −1. `check_cover_at_birth()` asserts it over
`t < birth_month()`, summing the seven child-life claim kinds and requiring zero.

The decrement is `pols_void`, and it is not a lapse. 「태아가 유산 또는 사산에 의해
출생하지 못한 경우에는 **계약을 무효로 합니다** … 이미 납입한 보험료를 돌려드립니다」
[S8 제56조] [S9]: nothing is retained, the contract is de-recognised rather than
terminated, and the cash flow is a refund of **every** premium paid — the 태아 module's own
stream included, which is why `claims(t, "VOID")` adds `prem_foetal_paid_pp(t)` to
`cum_prem_pp(t)`. It is published in its own `claims_void` column so that it is never
netted into `claims_lapse`, where it would look like a surrender value on a contract that
does not have one. On the anchor cell it totals **₩306.90**, and it is non-zero on exactly
the four 태아 model points — 1, 4, 6 and 10.

The 태아 module is the one thing that pays in respect of an event before the insured legally
exists, and it pays **from the date of birth** [S8 제59조], so it is excluded from
`check_cover_at_birth()` and tested separately by `check_neonatal_term()`. The void rate
itself is a `[std]` construction and the cells says so: **no Korean source retrieved gives a
foetal-loss rate.** What the sources fix is the mechanic.

## Two decrement lives, and a premium that stops on the earlier of two events

The in-force block is carried in two compartments:

`pols_pay(t)`
: in force and still paying premium. Exposed to the void decrement, the waiver, mortality
  and lapse.

`pols_waived(t)`
: in force with the premium waived. Cover continues in full and payment of the 적립보험료
  stops with it [S2]; **not** exposed to lapse, a policy paying nothing having nothing to
  lapse for.

`pols_if(t)` is their sum and the weight on every `result_cf()` row;
`check_waiver_split()` asserts the identity month by month. On the anchor cell
`pols_waived(240)` is **0.0334654434**, 4.36% of the block at 납입완료, and it then carries
mortality for eighty years without ever meeting a lapse rate again.

The entry rate `waiver_rate(t)` is `1 − (1 − child)(1 − payer)`. The child's limb is the
cancer, cerebrovascular and cardiac incidences plus `waiver_disab_share` of the two
후유장해 incidences, standing for the 7대질병, the 50% 이상 후유장해 and the
중대한특정상해수술 triggers of [S2]. The 계약자's limb is that life's own mortality grossed
up by `payer_disab_ratio` for the 50% 장해 limb of [S10 제22조]. **The two are read from
two different rows of the same table**, at two different ages, and the second life is 33
years older than the first.

Three implementation points are worth stating because they are choices:

1. **The P코드 carve-out is implemented, not averaged away.** 「출생전후기에 기원한 특정
   병태(P코드) 진단시 납입면제를 적용하지 않음」 [S2]. On a 태아 contract
   `waiver_rate_child(t)` returns zero for `t < foetal_cover_end()`, so the covers most likely
   to pay in the first year of a foetal contract are precisely the ones that cannot stop the
   premium. The signature is the step in `waiver_rate` from 0.0009071625 at `t = 16` to
   **0.0011521489** at `t = 17`; a model without the carve-out has no step.
2. **The 계약자 limb runs from `t = 0`**, before the insured exists — the 생명보험 wording
   makes the 피보험자 「계약자와 가입자녀」 [S10 제3조], so the policyholder is an insured in
   his own right and his death is a contractual event from the 계약일.
3. **The two decrements are independent [std]** and the 계약자 is held fixed for the whole
   projection. A change of 계약자 would change the decrement life mid-projection and no
   retrieved wording says how the waiver responds; the point is [unverified].

`waiver_rate(240)` is zero, and that is not an accident. A waiver of premium on a contract
with no premium moves policies into a compartment whose only remaining property is that it
cannot lapse — which would silently suppress eighty years of lapses, and with them the
₩2,695,713.64 of `claims_lapse` that is 15.8% of all benefit outgo on the anchor cell.

## Processing order, and the identity it closes

Within month `t` the order is **void, then the waiver, then mortality, then lapse**
`[std order]`:

```
l_P(t+1) = ( l_P(t) (1 - v(t)) - e(t) ) (1 - q(t)) (1 - w(t))
l_W(t+1) = ( l_W(t) (1 - v(t)) + e(t) ) (1 - q(t))
```

with `e(t) = pols_waiver_entry(t)`. Summing them gives

```
l(t+1) = l(t) - pols_void(t) - pols_death(t) - pols_lapse(t)
```

exactly, which is `check_pols_roll_fwd()`. There are **four exits, not two**, and the first
of them is what makes this product different: a voided contract has not lapsed and has not
died, and netting it into either would hide a decrement and mis-state the cash flow that
goes with it. `check_exit_total()` is the global companion — the four decrements sum over
the projection to `pols_if_init()`, and on the anchor cell 0.0049757330 + 0.4688979472 +
0.5103916457 + 0.0157346742 = 1 exactly, so no mass is lost at either end.

`pols_if_at(t, timing)` exposes the intermediate states, `"BEF_DECR"` / `"BEF_LAPSE"` /
`"AFT_DECR"`, on the same convention the sister libraries use.

## The benefit is a bundle, and one limb of it is a percentage scale

`benefit_pp(t, kind)` returns the expected outgo per policy in force; `claims(t, kind)`
weights it by `pols_if(t)`. Seven morbidity kinds and four decrement kinds, published as
eleven `claims_*` columns that sum, with the three expense lines, to `net_cf`.

**`"DISABILITY"` is not a lump sum.** The 기본계약 pays 보험가입금액 × 장해지급률 on a
continuous 3~100% scale, payable more than once with the percentages accumulating
[R12] [S1] [S2] [S11], and 장해 is a **settled** impairment — 「치유된 후 신체에 남아 있는
영구적인」 [REG-R25] — so its incidence lags the accident. The model multiplies the
incidence by `disab_severity` = 0.12 `[std]`. The accident limb costs **₩555,177.98** over
the term at that severity and **₩4,626,483.18** at severity 1.0: a factor of 8.3, landing
on the largest sum insured in the contract, and the single largest modelling trap in the
product.

**`"DIAGNOSIS"` is four 최초 1회한 ledgers.** Each of 암(유사암 제외), 유사암, 뇌출혈 and
급성심근경색증 carries its own `frac_open(t, cause)` — the probability that a policy in
force at `t` has not yet claimed that benefit — recursed as
`frac_open(t) = frac_open(t-1) (1 - i_m(t-1))`. It is carried **per policy** and never
weighted by `pols_if`: weighting it by the in-force probability measures the block's
consumption rather than the policyholder's and defers exhaustion indefinitely, which on a
hundred-year term is worth a great deal. `check_once_only()` asserts each ledger stays in
`[0, 1]` and never rises. The general tier runs from 1.0000 to **0.4023261296** over the
term — paediatric cancer incidence is two orders of magnitude below the adult rate, so the
ledger is almost untouched for thirty years and then drains fast.

**`"HOSPITAL"` is metered in days, not events.** The `hosp_acc` and `hosp_dis` causes are
**expected days per policy year**, multiplied by `hosp_daily()` and by `hosp_cap_factor` =
0.92 `[std]` for what survives the 1~180일 per-stay limit. They never route through
`inc_rate_mth`: `hosp_dis` at 만나이 0 is 2.40 days a year, and `1 − (1 − 2.40)^(1/12)` is
not a wrong number but a **complex** one. They are divided by twelve instead. **No 180-day
one-hospitalization memory is implemented**, no retrieved Korean child wording stating a
re-admission grouping rule. This is the largest single benefit line on the anchor cell —
**₩5,033,285.22 undiscounted, 47.0% of all morbidity outgo and 92.2% of the whole premium
collected** — and the infant peak is visible in the statement: `claims_hospital` falls from
₩7,164.01 at `t = 16` to ₩3,512.46 at `t = 17`, which is 만나이 turning from 0 to 1.

**`"LIABILITY"` is the only limb whose claim is a third party's loss**, and the only one a
non-life licence is needed to write [R5] [S5]. It is also where the renewal mechanic has its
one cash consequence: the 누수사고 limb's 90-day 보장개시일 **resets at every renewal** of the
3년만기 갱신형 block [S3] [S5], so `leak_share` = 0.40 `[std]` of the cost is off for the
first three months of each 36-month cycle. The 갱신형 chassis proper — the whole product
written of 20년/30년 renewable blocks with cover-group ceilings [S7] — is **not** implemented.

**`"NEONATAL"` runs on two terms of its own.** `neonatal_cost_pp("birth")` = **₩47,000** per
birth is the 태아보장기간 limbs — 출생위험 on its three tiers and 조산 진단 — paid at
`t = birth_month()`; `neonatal_cost_pp("block")` = **₩63,450** is the 1년만기 신생아 block,
spread evenly over its twelve months. Two of the limbs are **day-capped rather than
amount-capped**, and the table holds expected paid days after the contractual deduction and
inside the cap:

```
incubator benefit = 50,000 x max(0, min(days_used, 60) - 2)          [S1]
perinatal cash    = 10,000 x max(0, min(stay_days, 120) - 3),        [S1] [S8]
                    payable only where stay_days >= 4
```

The module's cost is therefore a length-of-stay question rather than an amount question,
which is why the supervisor's own worked claim — ₩16,836,420 on a birth at 32 weeks and
1.84 kg, of which ₩4,200,000 was neonatal day benefits [R3] — is the useful datum. On the
anchor cell the module costs **₩106,330.72** undiscounted against a module premium of
₩3,000 × 17 = ₩51,000, and every won of it falls inside the first thirteen months of a
hundred-year contract. It does not pay for itself on the shipped basis, and that is
reported rather than tuned away.

## The 면책기간 is tested at the 계약일, once, and never again

```
암보장개시일 =
    the day the first premium is received     if 보험나이 < 15 at the 계약일
    the 91st day counting 계약일 as day 1      if 보험나이 >= 15 at the 계약일
    the day the first premium is received     if the cover is a 태아가입용 form
```

`waiting_mths()` is a model point input and `cover_open(t, cover)` applies it to the two
cancer limbs alone. **A model that re-tests the rule at each anniversary is wrong**: the
wording is 「계약일 현재 보험나이 15세 미만 피보험자의 경우」 [S11] and 「최초계약과
부활계약의 면책기간은 보험나이 15세 이상인 경우에만 적용」 [S3], so a contract issued at
계약나이 0 has no cancer waiting period at any point in its hundred-year life, including the
eighty-five years during which the insured is an adult. Model point 7, issued at 보험나이 15,
is the cell on which the switch is on.

`reduction_mths()` returns **zero whatever the model point says on a 태아 contract**, because
the 2015 변경권고 inserted 「단, 피보험자가 보험가입 당시 태아(胎兒)인 경우에는 보험금의
100%를 지급합니다」 across 17 carriers and 56 products [R2]. The disapplication lives in the
cells rather than in the data, so that it cannot be switched off by editing a CSV.

## Death pays the account, because a death benefit would be void

`claims(t, "DEATH")` is `(av_pp(t) + unearned_prem_pp(t)) × pols_death(t)` and it is **not a
death benefit**. 상법 제732조 makes a contract on the death of a person under 15 무효
[R7] [REG-R50], 표준약관 제19조제2호 restates it and 제19조제3호 refuses to extend the
age-correction saving to it [REG-R25]; what is paid instead is the 계약자적립액 at the date
of death plus the 미경과보험료, which is what 감독규정 제7-63조제1항제1호 requires of a
제3보험 contract on a death it does not cover [REG-R17] and what 상법 제736조 floors
[REG-R50].

On the anchor cell that is **₩3,693,345.73 undiscounted** — the second largest outgo line
after hospital cash — because the 표준형's account crosses premiums paid at about `t = 353`
and keeps rising, and most deaths on a hundred-year contract are late ones. On the 미지급형
switch (model point 4) the same line is close to nil for the whole payment period, and a
family whose child dies in year 10 receives almost nothing. That is a real and uncomfortable
property of the suppressed form, and the model reproduces it rather than smoothing it.

## The account is recovered from a published grid, and the first two years are [std]

`av_table.csv` carries the 표준형 환급률 grid a current 상품요약서 publishes on a named
specimen contract [S2] as a `build` curve indexed by duration in years, and a `taper` curve
indexed by the fraction of the term run off. `refund_ratio(t)` is their product,
`cv_std_pp(t) = refund_ratio(t) × cum_prem_pp(t)`, and `check_refund_grid()` asserts that
the model returns the published figure at every node it reaches — 0.0% at 1 year, 45.6% at
3, 62.5% at 5, 73.7% at 10, 78.3% at 15, 82.6% at 20, 101.2% at 30, 122.5% at 40, 144.1% at
50 and 158.9% at 60. It is the one check in the model that ties a computed quantity to a
number a reader can look up.

Splitting the progression in two is what lets one shipped grid serve a 30세만기, a 100세만기
and a 110세만기 point; the taper node at 0.95 is calibrated so that a 100세만기 contract
reproduces the published **16.0% at 95 years** and pays nothing at 만기.

**Recovering the 계약자적립액 from that grid is where a [std] enters.** What the 상품요약서
publishes is 「순보험료식 계약자적립액에서 해약공제액을 공제한 금액」 [S2] — already net of
the charge and floored at zero — so the account can be recovered by adding the unamortised
charge back only where the floor is not binding. Where it is, the identity gives no more than
`0 ≤ AV ≤ 해약공제액`, and `av_pp(t)` is capped instead at the cumulative **net** premium,
the most a 순보험료식 reserve can have accumulated before interest or mortality:
`min(cv_std_pp + surr_chg_pp, max(cv_std_pp, net_prem_ratio × cum_prem_pp))`. It therefore
starts at nil as it must, rather than at the surrender charge — a model adding the charge
back unconditionally holds ₩364,000 on a contract that has collected nothing.
`check_av_bounds()` asserts the three inequalities the derivation allows.

## The surrender charge is computed from the regulation, and both its readings are carried

`surr_chg_cap_pp()` is the **표준해약공제액** of 감독규정 [별표 14] [REG-R20]:

```
5% x 연납순보험료 x 해약공제계수  +  보장성보험의 보험가입금액 x 10/1000
```

`surr_chg_prem_rate` is the schedule's 5% and `surr_chg_sa_rate` its **10/1000 — one per
cent, `0.01`**, not one per mille; both are read off the schedule and neither is a
standardization.

The 해약공제계수 is the policy term capped at 20 — 「보험기간(최대 20년)」 — and binds at 20
on every model point here. The second term is the harder half, and it is the one place where
this product's lack of a death benefit changes the arithmetic: **[별표 15] 제3호 does not
apply and 제9호 does**, 「보험가입금액 = (위험보험료 / 정기보험의 위험보험료) × 정기보험의
보험가입금액」 [REG-R21]. A term policy's risk premium per unit of face is its mortality
rate, so the notional amount is the first policy year's risk premium divided by that rate at
the 기준연령 요건, 남자 만 40세 [REG-R9 제1-2조제2호](#krlib-reg-r9). On the anchor cell:

| Quantity | Value |
|---|---|
| first-year risk premium `risk_prem_ann_pp()` | ₩145,537.05 |
| notional 보험가입금액 `sa_notional_pp()` | ₩132,306,409 |
| 연납순보험료 `prem_net_ann_pp()` | ₩252,000.00 |
| [별표 14] formula limb, at 10/1000 = 1% | ₩1,575,064.09 = **56.25 months** of premium |
| 13 x monthly premium, `surr_chg_cap_months` = 13.0 [REG-R29] | ₩364,000.00 |
| **표준해약공제액 `surr_chg_cap_pp()`**, the lesser of the two | **₩364,000.00** |
| 계약체결비용 `acq_cost_pp()` at 90% of the cap | ₩327,600.00 |
| the same, in months of premium `acq_cost_months()` | **11.70** |

**The two readings of one ceiling are 4.33 times apart on this product, and the formula limb
does not bind.** [별표 14] and the FSC's 2019 expense reform describe the *same* cap, the
reform stating it as **보장성보험 13배** of the monthly premium [REG-R29]; here the formula
gives 56.25 months against thirteen, because 제9호 divides this contract's whole first-year
risk premium by a 40-year-old's mortality rate and a bundled child stack has a large risk
premium and a very small death rate. `surr_chg_cap_pp()` therefore takes the **lesser** of the
two — the treatment `Cancer_KR_S` states for the same mechanic, and the reason
`surr_chg_cap_months` is a Reference here — and **the thirteen-month limb binds on all ten
shipped model points**, the formula limb running ₩245,582 to ₩1,654,269 across them.
`acq_cost_months()` publishes the ratio actually reached, **11.70**, rather than asserting the
two readings equal. `check_acq_cost_cap()` tests the bound; `check_surr_chg_cap()` tests that
the deducted charge never exceeds it, over a 해약공제기간 capped at seven years
[REG-R19 제7-66조제1항제2호](#krlib-reg-r19). Evaluating [별표 15] 제9호 at the *insured's* own age instead of
at 남자 만 40세 is a second trap: at 만나이 5 the mortality rate is 0.00012 and the formula
limb comes out at ₩12,380,087.45 — **442.1 months** of premium.

## The three surrender-value forms

```
cv_pp(t) = cv_std_pp(t)                                       [pyojunhyeong]
         = 0                                        t < m     [mijigeuphyeong]
         = k x cv_std_pp(t)                         t >= m
         = 0                                        t < m     [mijigeuphyeong III]
         = min(0.05 (1 + (t-m)//24), k) x cv_std_pp(t)  t >= m
```

`check_cv_floor()` asserts all three, including that the suppressed value is **exactly nil**
through the whole 납입기간: the cliff is a contractual fact and not an approximation, and the
「60원」 and 「550원」 entries in the published grid are rounding on a nominally zero quantity
[S2]. The graded ladder is the published ten-step one — 5% from the day after the end of year
M to the day before the M+2 계약해당일, then 10, 15, 20, 25, 30, 35, 40, 45 and finally 50%
from M+18 [S1].

**`Child_KR_S` ships the 표준형 as its base, which is the opposite of `Cancer_KR_S`.** The
market is in the suppressed forms — 63.8% of 보장성 초회보험료 by 2024 H1 [R11] [REG-R27] —
and the cancer chassis ships one. This product ships the standard form because the 적립부분
credited at the 공시이율 exists only there, the suppressed forms being 순수보장성 and showing
「-」 for it on the board [S2] [S11]; and because the 표준형's value **exceeds premiums paid
from about `t = 353`**, a shape only a hundred-year term produces. Shipping the two forms on
two products lets a reader compare them without either model carrying both.

## Columns that are deliberately zero

`claims_maturity` is **identically zero on every one of the ten shipped model points** and is
published rather than dropped. There is no 만기환급금 on the protection part [S1] [S2] and the
shipped taper reaches zero at 만기, so the 1.57% of anchor-cell policies reaching the 100세
계약해당일 receive nothing. The column stays because the residual 적립부분 is a real quantity
on a contract whose term ends earlier, and because `pols_maturity` is a real decrement whose
absence from the roll-forward would lose 1.57% of the block with no cause. A model that pays
`av_pp` at maturity without the taper pays ₩10,678,080 to those policies.

`claims_void` is zero on the six non-태아 points and non-zero only before birth on the other
four: a column and not a netting, because a void is not a surrender. And unlike the
[cancer chassis](../cancer/model.md), whose 미지급형 base makes `claims_lapse` identically zero
for the whole 납입기간 before it steps up at 납입완료, this product's 표준형 base pays a
surrender value on a lapse from about year 3 — the 환급률 grid is 0.0% through the first policy
year, so `claims_lapse` is the 미경과보험료 alone there and a real amount thereafter.

## Discounting, and the one place the model does discount

The projection publishes **undiscounted gross liability cash flows**, as every model in this
library does; discounting, the 책임준비금, the IFRS 17 CSM and the K-ICS 요구자본 belong to a
layer that consumes them.

The exception is a set of pricing diagnostics that are not in `result_cf()`. `pv_factor(t)`
discounts at the **보장부분 적용이율 of 2.75%** — the modal value of the comparison board's
column, whose observed range is 2.50%–3.00% [S11], and the pricing rate under another name,
the 감독규정 speaking only of the 계약자적립액 적용이율 [REG-R9] [REG-R48]. Then

```
equiv_premium_mth_pp() = epv_outgo_pp() / epv_prem_unit_pp()
```

On the anchor cell that is **₩31,079.59** against a shipped ₩28,000, from an EPV of outgo of
₩4,694,583.11 over 151.0504 discounted monthly premium units. It is a **first-order**
equivalence — the expense basis is held at the level the shipped premium produces rather than
re-scaled with the answer — and `check_equiv_premium()` verifies that the two 1,201-term
summations reproduce each other. `epv_prem_unit_pp()` is the model's whole behaviour in one
number: out of 240 scheduled instalments the projection expects to collect the discounted
equivalent of **151.05, or 62.9%**.

**Where the equivalence premium and the shipped premium differ, the computed figure governs.**
Nothing in the model depends on the model point's premium being a market rate: no carrier
publishes a rate table by age and duration, and the board's own specimen premiums vary by a
factor of seven on a nominally standardised basis — ₩21,502 to ₩148,250 for a male 5-year-old
— because carriers include different compulsory sets in the quoted 보장보험료 [S11]. That the
shipped basis lands **11.00% short** of its own equivalence premium is the calibration
finding, and it is the honest one.

## Modules that are off in the base run, and modules that are not modelled

Off but switchable, on a model point: the **해약환급금 미지급형** and **미지급형Ⅲ** (points 4
and 5), the **감액기간** (`reduction_mths`, observed 0 and 12; point 7), the **면책기간**
(`waiting_mths`, observed 0 and 3; points 7 and 8), the **broad 뇌혈관질환 / 허혈성심장질환
definitions** (`broad_def`, at `broad_def_factor` = 4.0 `[std]`; point 8), the **2026 저출산
premium discount** (1%–5% for twelve months [R6]; point 10 at 5%), **110세만기** (point 6),
the two **waiver** modules, the **태아** module, and the three lapse bases. Each is asserted
in both positions of its switch.

Not modelled, and deliberately: the full **갱신형 chassis** [S7]; the **임신·출산질환 module**
written on the mother and the **부양자 benefit stack** written on the parent [S2] [S5] [S11],
the second of which the composite replaces with the waiver — because a benefit and a decrement
are not the same cash flow, and their expected values differ by more than an order of
magnitude; **다태아** plans [R4] [R5]; the named-cancer riders and the 후유장해 생활지원금
annuity forms [S1] [S11]; **일반상해사망 from 만 15세** [S1] [S4]; **부활**; the **공시이율
reset**, which the model carries by reference to `WholeLife_KR_S`; and **실손의료비 riders of
any kind**, which have not been attachable to a child policy since April 2018 and are a
statutory impossibility rather than a design choice [R9] [R10] [REG-R17]. No exclusion
decrement is modelled: the general 보험금을 지급하지 않는 사유 articles were not read in full
for this product line, and that gap is stated rather than filled.

## Inputs are external files

Seven CSVs live beside `run.py` in `products/child/`, not inside the model folder. The model
folder holds `__init__.py` and `_system.json` and its two Space folders and nothing else — no
`_data/`, no IOSpec, no embedded values — so a diff of the model shows logic changes only.
This is the `annuallife.TradLife_A` layout; contrast `basiclife.BasicTerm_S`, which keeps its
inputs inside the model. The consequence worth knowing: **the model is not portable on its
own.** Copying `Child_KR_S` without its parent's CSVs produces a model that reads and then
fails on first evaluation.

| File | Reference | Reader | Contents |
|---|---|---|---|
| `model_point_table.csv` | `model_point_file` | `Data.model_point_table()` | ten model points, indexed by `point_id`; point 1 is the anchor |
| `mort_table.csv` | `mort_table_file` | `Data.mort_table()` | annual `mort_rate` by sex and 만나이 0–120, for the child **and** the 계약자 |
| `incidence_table.csv` | `incidence_file` | `Data.incidence_table()` | eleven causes x two sexes x fourteen pivot ages |
| `basis_table.csv` | `basis_file` | `Data.basis_table()` | thirteen scalar [std] parameters that turn an incidence into a cost |
| `neonatal_table.csv` | `neonatal_file` | `Data.neonatal_table()` | the 태아 module's nine limbs, with timing, frequency, amount and units |
| `lapse_table.csv` | `lapse_table_file` | `Data.lapse_table()` | three lapse bases, three parameters each |
| `av_table.csv` | `av_table_file` | `Data.av_table()` | the published 환급률 `build` grid and the `taper` that takes it to 만기 |

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate ItemSpace
with its own cells cache; readers placed there would re-read every file for every policy. They
live in the unparameterized `Data` Space instead, and
`test_inputs_are_read_once_not_once_per_model_point` asserts the property against the file set
registered in `kr_registry.INPUT_FILES` — the *set*, not merely whatever happened to be read,
so a file that stops being read fails rather than dropping quietly out of the count.
`input_dir()` returns `_model.path.parent`, resolved at run time and never hard-coded.

**Every assumption CSV carries a `provenance` column and every cell in it begins with a
citation tag.** `model_point_table.csv` is the only exemption, a model point being a
configuration rather than an assumption. To swap in a company basis, replace the files with
same-schema ones or point the filename References at different names, then clear the cache.
No formula changes.

### `mort_table.csv` — one construction, two lives

The industry table is the **경험생명표** (*gyeongheom saengmyeongpyo*), prepared by
보험개발원; the current edition is the 제10회, applied from April 2024. **It is not
published** — what is released is the summary, 평균수명 and 65세 기대여명, and not the rates
[REG-R33] [REG-R34]. `mort_table.csv` is therefore a **[std] construction**, log-linear
between fourteen anchor 만나이 shaped on the 통계청 완전생명표 age pattern [REG-R38]
[REG-R39], and every row's `provenance` says so. **It must never be called the 경험생명표.**

What it must have, and what a table graduated from age 20 upwards would not, are the three
features a child policy is exposed to: the **infant peak** (male `q(0)` = 0.0025, about
twenty times `q(5)`), the **childhood trough** at about age 10 and the **adolescent turn**.
The infant peak falls on the anchor cell in exactly the twelve months when the 태아 module is
also paying, which is why it is in the table rather than smoothed out of it.

The same file is read for **two lives**: the insured at `age_man(t)` and the 계약자 at
`payer_age + t // 12`, whose rate at issue, `q(33)` = 0.00067713, drives the whole waiver
decrement for the first policy year. `mort_be_factor` is **1.0**, and that identity is a
decision: the shipped table is a population all-cause construction with no prudential margin
to unwind, so scaling it would invent one. Model point 10 runs at 1.10. On a child policy
mortality **releases** the liability, so understating it **overstates** the liability.

### `incidence_table.csv` — one published rate, and ten shapes around it

Eleven causes by sex at pivot 만나이 0, 1, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90 and 100,
graduated **log-linearly** between adjacent pivots and returned **exactly at a pivot**. The
logarithm is not decoration: these rates span two or more orders of magnitude across the age
range — general-tier cancer incidence rises about two-hundredfold from 만나이 10 to 80 — and a
linear interpolation between decade pivots is wrong by a factor of two mid-span.

**Exactly one rate in the file is published anywhere**: `disability` at 만나이 5, 「일반상해
후유장해 발생률(3~100%), 기본계약, 5세, 상해 1급 — 남자 0.0001823, 여자 0.0001163」 [S1]. It
is a **적용위험률**, already a priced rate rather than a best estimate, and it is the point the
basic contract's whole decrement is calibrated on; it reproduces to its printed digits only
because the interpolator short-circuits at a pivot. Everything else is a shape drawn around it,
and each row's `provenance` names the authority its *shape* rests on — 국가암등록통계 연령별
발생률 [REG-R40], the 「기타피부암 및 갑상선암 이외의 암 발생률」 and 질병입원율 grids of the
참조순보험요율 display [REG-R61], the 국민건강보험 진료비 실태조사 [REG-R41] — rather than a
source for its level. The sex direction is **male-heavier**, following that one published pair
(a ratio of 1.57) against a market with no fixed sign: four carriers on the board price the
female above the male and seven below, the spread running 62% to 114% [S11].

**The two `hosp_*` causes are expected days, not probabilities**, so the file's `rate` column
carries two different units. `hosp_dis` at 만나이 0 is 2.40 **days** a year. That is the single
most important dimensional fact in the input set, and why `benefit_pp(t, "HOSPITAL")` divides
by twelve rather than calling `inc_rate_mth`.

### `basis_table.csv` — thirteen scalars that turn an incidence into a cost

Every one is a standardization with no published anchor, tagged in its own `provenance` cell
and listed with its rationale in *Standardizations used* below. It is a file rather than a
set of References in `Projection` for one reason: these are the parameters a user replacing
the model's basis changes first, and a CSV is the thing to hand them.

### `neonatal_table.csv` — nine limbs, two timings, two of them day-capped

Each limb carries a frequency per birth, an amount (fixed, or a ratio to the module's own
₩10,000,000 가입금액), an expected number of units and a `timing` — `birth` for the four
태아보장기간 limbs paid at `t = birth_month()`, `block` for the five limbs of the 1년만기
신생아 block, spread evenly over its twelve months. The two day-capped limbs are implemented
**as written**, so their `units` are expected paid days *after* the contractual deduction and
*inside* the cap. The `neonatal_haem` frequency carries a caveat in its provenance cell: it
is **regime-dependent rather than stationary**, because the 2013-09 supervisory decision
requiring neonatal claims to be paid on the diagnosis name rather than the KCD code ended
refusals of 뇌출혈 coded P52 and raised frequency sharply [R5].

### `lapse_table.csv` — three bases, and the vector is the argument

`lapse_rate(t)` is the **annual** rate and `lapse_rate_mth(t)` the monthly one, per the house
convention.

- **`loglinear`** — the 2024-11-07 계리가정 guideline's 원칙모형: a log-linear decay from the
  first-year rate to **0.1% at 납입완료** and **0.8%** thereafter [R11] [REG-R27]. The
  guideline's functional form was never converted from HWP and is **[unverified]** at
  instrument level; the two endpoints are verified from the 보도자료. The 5.0% start is the top
  band of the only 적용해지율 any Korean child product publishes [S1], so unlike every other
  lapse assumption in this library it has an observed anchor.
- **`disclosed`** — the step function one carrier discloses for its suppressed forms, 5.0% for
  ten years, 3.0% to fifteen, 1.0% thereafter in payment and 0.5% after 납입완료 [S1]: the
  comparison the guideline obliges an insurer departing from the 원칙모형 to disclose. The two
  produce visibly different contracts — model point 5 runs on `disclosed` and totals
  **−₩8,061,541.17** against the anchor's −₩13,085,435.00.
- **`flat`** — a level vector, the nearest a projection can come to the **synthetic** 표준형
  the 환급률 comparison is made against, priced with no lapse assumption at all [S1] [S3].

**Lapse is absorbing.** 부활 is available within three years even where there is no surrender
value [S8] [REG-R25 제27조](#krlib-reg-r25), every waiting period re-runs from the 부활일 [S3], and below
보험나이 15 there is no cancer waiting period to re-run — so a reinstated child policy is,
uniquely in this library, very nearly the policy that lapsed. The model does not carry it; the
simplification is conservative on a protection product and is recorded as one.

### `av_table.csv` and `model_point_table.csv`

`av_table.csv` holds **thirteen** `build` rows and five `taper` rows. Eleven of the build rows
are the published 환급률 progression on a named specimen contract — 표준형, 남자 5세, 상해 1급,
100세만기 20년납 월납 at 월납 50,000원, 공시이율 1.7% at 2026-07 [S2] — and the remaining two,
at 70 and 100 years, are `[std]` shaping between the published 60-year and 95-year figures; the
whole `taper` curve is `[std]` calibration. `check_refund_grid()` asserts the **ten** published
durations the grid reaches while the taper is still 1 (1, 3, 5, 10, 15, 20, 30, 40, 50 and 60
years), and the taper is calibrated so that 1.589 × 0.1007 reproduces the published 16.0% at
95 years.

`model_point_table.csv` covers both sexes; 태아가입 on four points and issue 보험나이 0, 5,
15 and 30 on the rest; 30세, 100세 and 110세 만기; 20년납 and 30년납; all three
surrender-value forms; both waiver modules in both positions; the 면책기간 and 감액기간
switches; the broad adult-disease definitions; the 2026 저출산 discount; and all three lapse
bases. Its ten premiums are **[std]** inputs, not computed quantities — see *Discounting*.

### No input file is keyed by the frame's `t`

Recorded here because the 0-based time-index convention turns on it: **not one of the seven
CSVs is keyed by the projection's time index**, so none of them carries a column that moves
with the frame.

| File | Time-like column | Decision |
|---|---|---|
| `av_table.csv` | `key`, `curve = build` | **unchanged** — an elapsed **duration in years** (0, 1, 3, …, 60, 70, 100), read through `refund_build(duration_years(t))` with `duration_years(t) = t / 12`. It is already 0-based: duration 0 years is `t = 0`, and the values are continuous keys interpolated between, not row indices |
| `av_table.csv` | `key`, `curve = taper` | **unchanged** — a **runoff fraction** on `[0, 1]`, read through `refund_taper(runoff(t))` with `runoff(t) = t / (proj_len() − 1)`. Dimensionless; 0 at the 계약일 and 1 on the terminal row, both before and after the redefinition of `proj_len()` |
| `mort_table.csv` | `age` | **unchanged** — an attained **만나이**, read at `age_man(t)` for the insured and `payer_age() + t // 12` for the 계약자. An age key, not a time key |
| `incidence_table.csv` | `age` | **unchanged** — an attained **만나이** pivot, read at `min(age_man(t), 100)` |
| `model_point_table.csv` | `birth_month` | **unchanged** — a point on the frame's own time axis (the policy month of birth, 5 on the anchor cell), and the frame's rows do not move, so the values stand |
| `model_point_table.csv` | `waiting_mths`, `reduction_mths`, `prem_discount_mths`, `prem_period_years`, `issue_age`, `term_age`, `payer_age` | **unchanged** — elapsed counts and ages, 0-based by nature and compared with `t <` rather than indexed by |
| `lapse_table.csv`, `basis_table.csv`, `neonatal_table.csv` | none | no time-like column at all |

## Sign convention

`net_cf` is **income positive** — premiums less benefits, claim handling expense, acquisition
and maintenance expense and commission. That is the library-wide sign and it is the notes'
own, so unlike the payout-annuity models there is no outgo-positive `liability_cf` companion
to publish: one stream, one sign, one name.

The shape to expect is a deep month-0 strain — ₩327,600 of acquisition cost and initial
commission against one month's ₩31,000 premium, giving `net_cf(0)` = **−₩298,646.21** — then
one negative month at birth as the 태아 module pays, then a positive stretch of nearly twenty
years averaging about ₩14,000 a month, and then **eighty years of pure outgo with not a single
positive month in it**.

## The identity `check_net_cf()` closes

`net_cf(t)` = `premiums` − `claims_disability` − `claims_diagnosis` − `claims_surgery` −
`claims_hospital` − `claims_event` − `claims_liability` − `claims_neonatal` − `claims_death` −
`claims_lapse` − `claims_maturity` − `claims_void` − `claim_expenses` − `expenses` −
`commissions` — the fifteen cash-flow columns of `result_cf()`, read back out of the frame
row by row so that a reader adding up the printed statement gets the printed total.

Reading it back out of the frame rather than recomputing it is the point: it is the check that
catches a benefit kind that exists in `claims(t, kind)` but was never given a column, which
would leave the statement silently short of outgo the model is charging. It is also why
`result_cf()` publishes the eleven `claims_*` split columns and **no aggregate `claims`
column** — an aggregate beside the splits would double-count the whole benefit outgo, which is
the ruling `RETIRED_COLUMNS` carries across all six libraries. `check_net_cf_resid(t)` gives
the signed per-month residual; the tolerance is `val_tol` scaled by the largest sum insured,
so it is far below one won on amounts of order 1e8.

## Naming

House vocabulary throughout: `model_point`, `proj_len`, `age`, `pols_if`, `mort_rate`,
`claims`, `expenses`, `net_cf`, `result_cf`; `pols_death`, `pols_lapse`, `pols_maturity`,
`pols_if_init`, `pols_if_at`, `premium_mth_pp`, `mort_rate_mth`, `lapse_rate` /
`lapse_rate_mth`, `av_pp`, `cv_pp`, `surr_chg_pp`, `cv_floor_ratio`, `refund_ratio`,
`mort_be_factor`, `check_pols_roll_fwd`, `check_net_cf`, `roll_fwd_tol`, `val_tol`.

### The notes' symbols, and where they live

The full map is in the `Projection` Space docstring, which is where a reader holding the notes
beside the model will look for it. Six cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `l_P(t)`, `l_W(t)` | `pols_pay` / `pols_waived` | Two compartments of one block, not two blocks. `pols_if` is their sum and is the weight on every cash flow row; naming either of them `pols_if_*` would invite a reader to weight a claim by the wrong one |
| `v(t)` | `void_rate_mth` / `pols_void` | The notes' rate is *monthly* and says so in the suffix, beside `mort_rate_mth` and `lapse_rate_mth`. The count it produces is a different quantity and gets its own name. Not `pols_lapse`, and never netted into it |
| `ω(t)` | `waiver_rate` / `waiver_rate_mth` | Annual and monthly, on the house convention; the two limbs are `waiver_rate_child` and `waiver_rate_payer` so that neither can be read as the total |
| `y(t)` | `age_man` | The second age. `age` is 보험나이, the contract's own clock; `age_man` is 만나이, which is what every public series the decrements are built from is published on. Both are printed in `result_pols()` because the offset is a modelled quantity on this product and not a footnote |
| *(no symbol)* | `born` | The birth gate. A boolean cells rather than a comparison inlined at each call site, so that `check_cover_at_birth()` tests one thing and a reader can find every cover that respects it |
| *(no symbol)* | `frac_open(t, cause)` | A 최초 1회한 ledger, named for what it holds — the fraction of policies for which that benefit is still open — rather than for a letter. Per policy, never per block |

Product-specific names are kept English and descriptive — `neonatal_cost_pp` for the 태아
module, `cover_open` for the 면책기간 gate, `reduction_factor` for the 감액,
`prem_foetal_paid_pp` for the second premium stream, `sa_notional_pp` for the notional
보험가입금액 of [별표 15] 제9호, `equiv_premium_mth_pp` for the pricing diagnostic — and **no
romanized Korean appears in a cells identifier**.

### What this product argued in the cross-model naming review

This is the model with the most Korean-specific machinery in the library, so it is where the
temptation to romanize was strongest and where three of the register's rulings were settled:

- **`decl_rate`, not `gongsi_rate`**, and **`prem_int_rate`, not `yejeong_rate`**. 공시이율 is
  the declared crediting rate under the definition `delib` settled for the laufende
  Verzinsung, and 예정이율 is the pricing rate, a different quantity. This product carries
  **both** at once, exactly the case that would have made two romanized names look natural.
- **`cv_floor_ratio`, not `cv_ratio`.** This model carries two ratios on the same chassis, the
  suppressed fraction `k` and the 환급률, and a bare `cv_ratio` said nothing about which;
  `refund_ratio` is the other, named for the published quantity a supervisor regulates.
- **`surr_chg_pp` with `surr_chg_cap_pp` beside it**, against `surr_charge_pp`. The savings
  chassis owns the first name; the Korean addition is the *cap*, from the 표준해약공제액, a
  different cells with a different formula and its own check.

Two more the register already carried and this product would otherwise have broken:
`pols_maturity` rather than `pols_expiry` — 1.57% of the block here, against a
`claims_maturity` of zero — and `check_net_cf` rather than `check_cf_ledger`.

## Standardizations used

Every row is **[std]**. The sourced contractual and pricing parameters are in
[`product-spec.md`](product-spec.md) and [`technical-notes.md`](technical-notes.md) and are not
repeated here. "Observed range" is what the retrieved documents actually bound, and for this
product most of them bound nothing at all — which is said rather than papered over.

| Parameter | Value | Rationale | Observed range |
|---|---|---|---|
| every rate in `incidence_table.csv` **but the two [S1] rows** | eleven causes x two sexes x fourteen pivots | nothing on Korean child incidence was retrieved from 보험개발원, 국가암정보센터 or 통계청; each row's provenance names the authority its *shape* rests on [REG-R40] [REG-R41] [REG-R61] | one observation only: 일반상해 후유장해 발생률(3~100%) at 5세, 상해 1급 — 남 0.0001823 / 여 0.0001163 [S1], which the file reproduces exactly |
| incidence graduation | log-linear between pivots | the rates span two or more orders of magnitude; a linear interpolation is wrong by a factor of two mid-span, and only a log-linear one returns the published pivot exactly | none published |
| `mort_table.csv` construction | log-linear between fourteen anchors on the 완전생명표 age pattern | the 제10회 경험생명표 is published only as 평균수명 and 기대여명 [REG-R33] [REG-R34]; the 참조순보험요율 for mortality is filed and never published [REG-R4] | none; the shape check is the infant peak, male `q(0)` = 0.0025 against `q(5)` = 0.00012 |
| `mort_be_factor` | 1.0 | the shipped table is a population all-cause construction with no prudential margin to unwind; scaling it would invent one | none published; model point 10 runs 1.10 |
| `disab_severity`, `disease_disab_severity` | 0.12, 0.15 | the 기본계약 pays `S x 장해지급률` on a continuous 3~100% band [R12] [S1] [S2] [S11]; the severity distribution is published nowhere | none; the sensitivity is a factor of 8.3 on the accident limb, ₩555,177.98 at 0.12 against ₩4,626,483.18 at 1.0 |
| `surgery_rate_cancer/_cerebral/_cardiac` | 0.85, 0.50, 0.70 | the 수술비 limb pays per qualifying operation [R12]; no Korean operation-given-diagnosis rate was retrieved | none published |
| `liability_severity` | ₩600,000 | mean paid on a 가족일상생활배상책임 claim | the ₩100,000,000 limit and the ₩200,000 / ₩500,000 대물 deductibles are sourced [S5]; the severity is not |
| `hosp_cap_factor` | 0.92 | the share of expected 입원 days surviving the 1~180일 per-stay cap | the cap is sourced [R12] [S2]; **no Korean child wording states a re-admission grouping rule**, so no 180-day memory is modelled — a real difference from the Japanese third-sector chassis |
| `waiver_disab_share`, `payer_disab_ratio` | 0.08, 0.25 | the 50% 이상 threshold that fires the waiver [S2], and the 계약자's 50% 장해 incidence as a ratio to mortality [S10 제22조] | **no Korean disability incidence table is public** |
| waiver independence | `1 − (1−child)(1−payer)` | nothing in the sources relates the two lives, and nothing the model can see does | none |
| 계약자 age and sex | 만 33, male, fixed for the projection | mid-point of the band the mother-side riders state | 20~47세 [S2]; a change of 계약자 mid-term is [unverified] |
| P코드 carve-out scope | child limb off over `t < foetal_cover_end()` | the carve-out itself is sourced [S2]; its exact scope over the 1년만기 block is the standardization | none published |
| `leak_share` | 0.40 | the 누수사고 share of the liability cost, being the limb whose 90-day 보장개시일 resets at each renewal | the reset is sourced [S3] [S5]; the share is not |
| `void_rate_ann` | 0.012 | **the most exposed number in the file.** No Korean source retrieved gives a foetal-loss rate; what is sourced is the mechanic — 무효, whole premium returned [S8 제56조] [S9] | none at all; worth ₩306.90 on the anchor cell, so small in cash and large in principle |
| `broad_def_factor` | 4.0 | broad 뇌혈관질환 / 허혈성심장질환 ranges against the narrow 뇌출혈 / 급성심근경색증 the comparison basis prices | both definitions are sourced [S2] [S11] [R12]; the ratio is not |
| `net_prem_ratio` | 0.75 | 순보험료 as a share of 영업보험료, used **only** in the 표준해약공제액 formula of [별표 14] [REG-R20] | no Korean 예정사업비율 is published: the 산출방법서 is an undisclosed 기초서류 [REG-R2] |
| `acq_cost_ratio`, `comm_init_share`, `comm_renewal_rate` | 0.9 of the cap, 0.65, 0.03 | no Korean carrier publishes any expense or commission figure for this product; the statutory ceiling is all there is | the cap is ₩364,000.00 = **13.00 months** of premium on the anchor and the 90% of it deducted is **11.70 months**; the [별표 14] formula limb is ₩1,575,064.09 = 56.25 months and does **not** bind, so the FSC's 13-month reading of the same cap governs [REG-R29]; commission is capped at the first year's expected premium, instalments at 60% of the 표준해약공제액 a year [REG-R22 제4-32조제5항·제8항](#krlib-reg-r22) |
| which limb of the cap binds | the **lesser** of [별표 14] and 13 x monthly premium | [REG-R20] and [REG-R29] are two readings of one ceiling and disagree by 4.33x here; taking the lesser is the treatment `Cancer_KR_S` states for the same mechanic | neither reading is [std] — `surr_chg_prem_rate` 0.05, `surr_chg_sa_rate` 0.01 and `surr_chg_cap_months` 13.0 are all read off the instruments; what is [std] is the choice between them |
| `expense_maint_pp`, `expense_maint_prem_rate`, `expense_claim_pp` | ₩400/month, 5% of premium, ₩30,000/claim | both 상품요약서 define 계약체결비용 and 계약관리비용 and then give no number | none published; 보험가격지수 dispersion on the board is the only indirect handle [S11] [REG-R22 제7-45조제7항](#krlib-reg-r22) |
| `inflation_rate` | 2.0% p.a. | the Bank of Korea's own target; **not a detail on this product** — it compounds to x7.24 over a hundred years and the ₩400 charge is ₩2,898 a month at `t = 1200` | none published |
| lapse shape | log-linear between the two prescribed endpoints | the guideline's functional form was never converted from HWP and is **[unverified]** at instrument level | the endpoints are prescribed, 0.1% at 납입완료 and 0.8% after [R11] [REG-R27]; the 5.0% start is the top band of the only published 적용해지율 [S1], whose full disclosed vector ships beside it as `disclosed` |
| lapse absorbing | no 부활 inflow | reinstatement within three years is sourced [S8] [REG-R25 제27조](#krlib-reg-r25) and no take-up rate is published; below 보험나이 15 there is no waiting period to re-run [S3], so the simplification is larger here than on the chassis | none published; direction stated — it **understates** persistency |
| decrement order | void, waiver, mortality, lapse | fixed by the contract's own sequence: a void de-recognises the contract, a waiver changes who pays, and only a paying policy can lapse | not a disclosure question |
| 해약공제액 release | linear over the 해약공제기간 | the regulation caps the **amount** and not the shape [REG-R19] [REG-R20] | the seven-year cap is sourced [REG-R19 제7-66조제1항제2호](#krlib-reg-r19) |
| `av_pp` before the grid opens | capped at `max(cv_std_pp, net_prem_ratio x cum_prem_pp)` | the published grid is 「순보험료식 계약자적립액에서 해약공제액을 공제한 금액」, already net and floored at zero [S2], so the identity gives only `0 <= AV <= 해약공제액` there | none; the constraint is that `av_pp(0)` must be 0 |
| `taper` calibration | node 0.95 set so 1.589 x 0.1007 = 16.0% | one shipped grid must serve a 30세, a 100세 and a 110세 만기 | the published nodes it reproduces [S2] |
| `prem_int_rate`, `decl_rate`, `min_guar_rate`, `avg_decl_rate` | 2.75%, 1.70%, 0.30%, 2.50% | the modal value of each published column is the standardization; the columns themselves are sourced. Only `prem_int_rate` is read by a formula — `pv_factor()`. The other three are **declared and not used**: they are the interest basis on which [S2] computed the 환급률 grid the model reads, recorded so a reader can see what the shipped account is priced on, and the 공시이율 reset itself is carried by reference to `WholeLife_KR_S` | 2.50–3.00%, 1.60–2.20%, 0.20–0.50% [S2] [S11] |
| the ten office premiums | ₩3,026 to ₩71,000 | model point inputs, not computed quantities; no carrier publishes a rate table by age and duration [REG-R2] [REG-R4] | the board's specimen premiums for a male 5-year-old run ₩21,502 to ₩148,250, a factor of seven, because carriers quote different compulsory sets [S11] |
| `roll_fwd_tol`, `val_tol` | 1e-10, 1e-7 | one closes an identity between cells evaluated in one expression; the other re-reads won amounts of order 1e8 back out of a `DataFrame` | both far below one won |

## Tests

`tests/test_child_kr.py` is this model's own suite. It asserts the notes' worked example
**hard-coded** as a module-level table rather than pickled, so a reviewer can check it against
the notes by eye:

- **The pre-birth months** `t = 0 … 4` line by line — premium on all three streams, the void
  refund of ₩122.13 at `t = 4`, and **every child-life claim column exactly zero**, asserted as
  zeros rather than left implied.
- **The month of birth and the month after**, `t = 5` and `t = 16 / 17`, where the 태아 module
  pays, `age_man` turns from 0 to 1 and `claims_hospital` falls from ₩7,164.01 to ₩3,512.46.
- **The policy-year-1 aggregate** and the undiscounted totals over all 1,201 rows, line by
  line on unrounded values — ₩5,458,037.93 of premium against ₩17,087,999 of benefit and
  ₩1,455,474 of expense and commission, for **−₩13,085,435.00** — and the four exits summing
  to one: 0.0049757330 + 0.4688979472 + 0.5103916457 + 0.0157346742.
- **The pricing diagnostics** `epv_outgo_pp()` = 4,694,583.10870084, `epv_prem_unit_pp()` =
  151.0503621937853 and `equiv_premium_mth_pp()` = 31,079.588559199034; the **published 환급률
  grid** at all ten checkable nodes and the 16.0% at 95 years; and the **[별표 14] chain**
  ₩145,537.05 → ₩132,306,409 → a formula limb of ₩1,575,064.09 that does not bind → the
  13-month cap ₩364,000.00 → ₩327,600.00 → 11.70 months.

Each of the notes' **Known modeling pitfalls** earns a test named after it, and each fails if
its pitfall is committed: cover attaching at the 계약일 rather than at birth, the void netted
into lapse, the projection run on one age, the monthly conversion applied to a day count, the
면책기간 re-tested at the claim date, a 감액 applied to a foetal contract, the child's waiver
limb running over the 신생아 block, the parent modelled as a benefit rather than a decrement,
the waiver running after 납입완료, the waived compartment exposed to lapse, the 기본계약
treated as a lump sum, `frac_open` ledgers weighted by `pols_if`, renewal commission from
`t = 1` or after 납입완료, a 만기환급금 paid, the account started at the surrender charge, the
notional 보험가입금액 computed at the insured's own age, an exit dropped from the roll-forward,
the incidence grid interpolated linearly, the female rate assumed below the male, and monthly
rounding assumed to re-add. The optional modules are asserted in **both** switch positions.

`tests/test_model_conventions_kr.py` adds the house style, parametrized over
`kr_registry.MODELS` rather than restated here: the two-Space layout with no orphan CSV beside
the model, the `provenance` column with a citation tag on every assumption row, the docstrings
and their required phrases, the age basis declared in the `Projection` docstring and matching
the registry's `BOHEOM` metadata, the retired-name register, the `result_cf()` contract —
indexed by `t`, first column `pols_if`, a `net_cf` column, all names `lower_snake_case`, no
NaN, contiguous, starting at a non-negative index and ending at `proj_len() − 1` — the
read-once property against
`kr_registry.INPUT_FILES`, and the read → write → re-read round trip.

**Thirteen `check_*` cells** carry this product's own identities. Each takes no argument and
returns a real `bool` over all `t`, with the signed per-`t` residual at `check_*_resid(t)`, and
**all thirteen return `True` on all ten shipped model points**.

| Check | What it closes |
|---|---|
| `check_pols_roll_fwd` | `pols_if(t) − pols_if(t+1)` = voids + deaths + lapses, under the stated order |
| `check_waiver_split` | `pols_pay(t) + pols_waived(t) = pols_if(t)`, month by month |
| `check_exit_total` | the four exits sum over the projection to `pols_if_init()` — no mass lost at either end |
| `check_cover_at_birth` | every cover on the child's own life is identically zero for `t < birth_month()`, and so is the insured's mortality |
| `check_once_only` | each `frac_open` ledger stays in `[0, 1]` and never rises |
| `check_neonatal_term` | the 태아 module pays inside `birth_month() ≤ t < foetal_cover_end()` and nowhere else |
| `check_cv_floor` | the suppressed forms pay **exactly** nil through the 납입기간, and the graded ladder never exceeds `k` |
| `check_av_bounds` | the account is never negative, never below the amount payable on surrender, and never above that amount grossed up by the whole unamortised 해약공제액 |
| `check_surr_chg_cap` | the deducted charge never exceeds the 표준해약공제액, over a 해약공제기간 capped at seven years |
| `check_acq_cost_cap` | the acquisition cost is inside the [별표 14] bound |
| `check_refund_grid` | the model returns the **published** 환급률 at every node it reaches |
| `check_equiv_premium` | the two 1,201-term summations behind `equiv_premium_mth_pp()` reproduce each other |
| `check_net_cf` | the printed statement adds to `net_cf`: no claim kind counted twice or dropped |

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #krlib-child-r10
[R11]: #krlib-child-r11
[R12]: #krlib-child-r12
[R2]: #krlib-child-r2
[R3]: #krlib-child-r3
[R4]: #krlib-child-r4
[R5]: #krlib-child-r5
[R6]: #krlib-child-r6
[R7]: #krlib-child-r7
[R9]: #krlib-child-r9
[REG-R17]: #krlib-reg-r17
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R21]: #krlib-reg-r21
[REG-R25]: #krlib-reg-r25
[REG-R27]: #krlib-reg-r27
[REG-R29]: #krlib-reg-r29
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R38]: #krlib-reg-r38
[REG-R39]: #krlib-reg-r39
[REG-R4]: #krlib-reg-r4
[REG-R40]: #krlib-reg-r40
[REG-R41]: #krlib-reg-r41
[REG-R48]: #krlib-reg-r48
[REG-R50]: #krlib-reg-r50
[REG-R61]: #krlib-reg-r61
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
