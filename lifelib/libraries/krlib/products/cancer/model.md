# Implementation Notes

**Status:** Draft, 2026-09-03. Built from [`technical-notes.md`](technical-notes.md); the
product those notes describe is specified in [`product-spec.md`](product-spec.md), and every
source tag on this page resolves in [`sources.md`](sources.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The contractual
> mechanics are sourced — the 90일 면책기간 as a hard zero on the invasive tiers and its
> complete absence on 유사암, the one-year 50% 감액기간 measured 보험계약일 to 진단확정일,
> the 200 / 100 / 60 / 20 tier ladder read off a 보험금 지급기준표, the 최초 1회한 form of
> every diagnosis benefit, 고액암 paying *in addition* rather than instead, the waiver's
> exclusion of 특정소액암 and 유사암 by name, the absence of any death benefit beside the
> statutory payment of the 계약자적립액, the nil surrender value of the 미지급형 form during
> the 납입기간, and the 표준해약공제액. **The incidence basis is sourced too**, which makes
> this the one morbidity model in `krlib` that does not open with an apology: 보험개발원
> publishes a dated 「기타피부암 및 갑상선암 이외의 암 발생률」 grid by age and sex on the
> *insured* definition of cancer [R5] [REG-R61]. Everything else is **[std]** — the tier
> decomposition of that grid, the whole post-diagnosis survival model, every care intensity,
> the lapse level, the expense and commission scales, the notional 보험가입금액 and the
> premium — and the 제10회 경험생명표 is released only as 평균수명 and 기대여명 [REG-R33]
> [REG-R34], so `mort_table.csv` is a construction and not a copy. Replace the assumption
> tables with company data and a real 산출방법서 before drawing any conclusion.

## Run it

```bash
python products/cancer/run.py            # the anchor cell, point_id = 1
python products/cancer/run.py 8          # the treatment-cost-only shape
```

`run.py` prints the model point, the derived scalars, the first twelve months of the cash
flow statement, the undiscounted totals grouped four ways, and the ten `check_*` identities.
Everything it prints is ASCII, so the output lands on a Windows console under any code page:
amounts are labelled `KRW`, and the product, the four tiers, the two timing devices, the
suppressed surrender-value form and the account paid on death are romanized in Revised
Romanization. Real output, with the cash-flow rows elided — they are reproduced in full, to
ten decimals, in [`technical-notes.md`](technical-notes.md):

```text
Cancer_KR_S - am boheom (cancer insurance), KRW, monthly grid, man nai
model point 1: KR-CA-0001 - M40, bi-gaengsin (non-renewable)
  cover to man nai 100, 20-year pay, mijigeuphyeong (no surrender value while paying),
  sum insured KRW 30,000,000
  premium = KRW 45,000/month   frame = 721 rows (t = 0 .. 720)   myeonchaek = 3 m   gamaek = 12 m
  tiers: gohaek 100% top-up / ilban 100% / soaek 60% / yusa 20% of the sum insured
  modules: diag=1 hosp=1 surg=1 treat=1   waiver = cancer_diag
  pyojun haeyak gongjeaek (standard surrender charge cap) = KRW 585,000

    [ the t = 0..11 rows of result_cf(), nineteen columns ]
... 709 further months to t = 720

undiscounted totals over the whole projection (per policy issued):
  premiums              8,586,707.28
  claims, diagnosis     8,009,869.07
  claims, care          4,192,693.32
  claims, account       1,474,174.97
  claims, all          13,676,737.37
  expenses              1,810,997.43
  commissions             565,757.97
  net_cf               -7,466,785.49

checks:
  check_canc_dur_ledger      True
  check_cancer_roll_fwd      True
  check_cv_floor             True
  check_hosp_cap             True
  check_net_cf               True
  check_pols_roll_fwd        True
  check_similar_ledger       True
  check_tier_shares          True
  check_treat_ledger         True
  check_waiting_period       True
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/cancer/Cancer_KR_S")
model.Projection[1].result_cf()      # the worked example's anchor cell
model.Projection[1].result_pols()    # counts, decrement rates, ledgers, the account
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a `DataFrame` indexed by policy month `t` with `pols_if` first and
`net_cf` last, the three state counts published beside `pols_if` and the benefit side split
into ten `claims_*` columns; `expenses` there is acquisition plus maintenance, with the claim
handling cost in its own `claim_expenses` column. `result_pols()` publishes the four
diagnosis flows, the three decrement rates, the 유사암 ledger and the 계약자적립액 with both
surrender values beside it — the last because the whole of the 미지급형 form is the gap
between `cv_pp` and `cv_std_pp`. `model.Projection.doc` carries the notes' symbols mapped to
cells names and states the age basis; `model.Data.doc` says what each input file is and,
for the two decrement files, which is published data and which is a construction.

## Three in-force states, and why the reduced tier is not one of them

The model carries three in-force states rather than the chassis's one, and the reason is the
premium waiver rather than the benefit:

| Cells | Meaning | Pays premium | Can lapse | Excess hazard |
|---|---|---|---|---|
| `pols_healthy(t)` | never invasively diagnosed | yes | yes | none |
| `pols_minor(t)` | first invasive diagnosis was a 특정소액암 | **yes** | **yes** | 특정소액암 basis |
| `pols_waived(t)` | has had a 일반암 or 고액암 | no | no | general basis |

The split is contractual, not a refinement. 「특정 소액암 … 은 보험료 납입을 면제하지
않습니다」 [S3 제14조제1항] [S1 제9조제1항]: a 특정소액암 life goes on paying and can still
surrender, while a 일반암 life pays nothing and — on the 미지급형 form during the 납입기간 —
has nothing to surrender. Folding the two together stops a premium the contract goes on
charging. At `t = 240` the 특정소액암 state is **0.0127869424** of the block, 1.77% of the
in-force, and it has been paying ₩45,000 a month for twenty years.

The transition **특정소액암 → 일반암** is modelled: it is folded into `surv_minor` as a
`(1 − i_g · cover)` factor and appears as the second limb of `diag_gen`. The reverse is not.
A 일반암 life's later 특정소액암 and a 고액암 after a plain 일반암 are both **[std]
omissions**, and both understate.

**The 유사암 tier is emphatically not a fourth state.** It is a second benefit at a second
rate on its own once-only ledger; it moves no life anywhere, stops no premium, and carries
**no excess mortality at all** — 갑상선 five-year relative survival is 100.2% and lifetime
갑상선 mortality risk 0.1% [R1], so the tier appears in **no row** of `survival_table.csv`.
Implementing it as a discount on the main diagnosis benefit gets the amount right and the
ledger, the waiver and the waiting period all wrong.

## Six select-duration cohorts, and a thirteen-month delay

Relative survival is steeply select — most of a cancer diagnosis's excess mortality falls in
the first two years, and **62.1%** of Korea's prevalent cancer population is more than five
years out from diagnosis [R1]. A flat hazard fitted to the five-year point therefore kills
long survivors far too fast, and long survivors are exactly whom the inpatient, surgery and
treatment limbs are paid for. Each diagnosed state is resolved into **six cohorts by elapsed
duration** — select years 1 to 5 and an ultimate — and the excess hazard is read per cohort.

The cohorts are tracked **exactly**, as a delay on the entry flow rather than as a transfer
rate. `waived_grad(t, k)` and `minor_grad(t, k)` carry the entrants of a month twelve months
earlier forward on that cohort's own decrements, and the graduation terms telescope out of
the sum — which is what `check_cancer_roll_fwd()` asserts. The delay is **thirteen months,
not twelve**: `waived_grad(t, 1)` reads `diag_gen(t − 13)`, because the entry month is itself
a full month of cohort-1 exposure. That off-by-one is invisible to the roll-forward checks,
which close either way because the graduation terms cancel, so `check_canc_dur_ledger()`
rebuilds cohort 1 independently from the entry history and is the only identity that catches
it.

## Two waiting periods, one of which is zero

`cover(t)` multiplies **every invasive-tier benefit and both invasive transitions**, and is
zero for `t < 3`. In months 0, 1 and 2 the model diagnoses nobody with an invasive cancer,
pays nothing for one, and still collects the premium — so `pols_minor(3)` and `pols_waived(3)`
are exactly **0.0000000000** and every care line at `t = 3` is exactly zero.
`check_waiting_period()` asserts the whole of that, gating the transition and not merely the
claim: a model that suppresses only the benefit leaves a diagnosed population the contract
says does not exist.

`cover_similar(t)` is the second start date and it is **1 from `t = 0`** — 「유사암의
보장개시일은 계약일임」 [S1], with the 면책기간 table marking 유사암 진단비 with a cross
[S1] [S2]. `claims_diag_similar(0) = 177.9475000000` is the only non-zero benefit in the
first three rows of the anchor cell. Reading one `wait_months` off the model point and
applying it to all four tiers is the commonest way to break this product, and at young ages
it is not a small error: at female 만나이 30 the model's 유사암 incidence, 0.001136 a year,
**exceeds** the invasive base rate of 0.001005 that it is a ratio of.

The horizon is set by the contract, not by a table's terminal age: `proj_len() = 12 × (100 −
issue_age) + 1` is the **number** of projected months — the frame's exclusive end, 721 on the
anchor cell, so `result_cf()` has 721 rows indexed `t = 0 … 720` and the frame is
`range(proj_len())`. `t` is 0-based: `t = 0` is the first projected month, the one beginning
at the 보험계약일, and the policy year is the contractual label `t // 12 + 1`. At
`t = proj_len() − 1` the cover ends at the 100세 계약해당일, `pols_maturity` takes the
whole remaining exposure — **0.0103446076** — every cash flow is zero and
`claims(t, "MATURITY")` is zero, because **nothing is paid at expiry** [S8]. The 만기환급형
2종 variant returning 5% of 보험가입금액 [S8] is a different product and is out of scope.

## The 감액기간 is a first-year phenomenon, not a benefit scaling

`reduction_factor(t)` is 0.50 for `t < reduction_months()` and 1.00 after, and it multiplies
the **four diagnosis lines and nothing else** [S1] [S6] [R6]. Baking 0.50 into
`benefit_ratio` halves the liability for sixty years instead of one; on a 갱신계약 the device
is disapplied altogether — 「※ 갱신계약의 경우 감액지급을 적용하지 않습니다」 [S2] [S4] —
which is what model point 3 exercises. The observed designs are 0, 12 and 24 months and
`reduction_months` is a model point column carrying all three.

One refinement is deliberately **not** implemented and the direction is stated. The clock's
second endpoint differs by benefit: it runs to the 진단확정일 for a diagnosis benefit
[S3 별표 1 주2] but to the **수술일** for a surgery or treatment benefit [S4] [S5]. So a
cancer diagnosed in month 10 and operated on in month 14 really does draw a reduced diagnosis
benefit and a full surgery benefit — and so does the model. `reduction_factor` multiplies the
four diagnosis lines **only** and never the care limbs, so the model gives the contract's own
answer whenever the treatment date falls outside the 감액기간, which includes every case in
which the diagnosis itself does, and **overstates** the care limbs of a treatment falling
inside it.

## Two columns that are deliberately zero, and one that is not a death benefit

Three of the ten `claims_*` columns are published as zeros rather than dropped, because a
column of zeros states a product fact where a missing column hides it.

- **`claims_maturity` is zero at every `t`.** Nothing is paid at the 100세 계약해당일 on the
  순수보장형 composite [S8], and the only retrieved surrender-value illustration shows the
  value returning to nil at maturity [S8].
- **`claims_lapse` is identically zero for the whole 납입기간.** `cv_pp(t) = 0` for every
  `t < 240` on the 미지급형 form [S3 제41조], so twenty years of lapses cost nothing in cash.
  On a **전기납** 미지급형 contract — model point 7 — it is zero at *every* duration, because
  the payment period never ends.
- **`claims_death` is not a death benefit.** The composite carries none. What that column
  holds is the **계약자적립액**, which 감독규정 제7-63조제1항제1호 requires a 제3보험 product
  to pay when the insured dies of a cause the policy does not cover [REG-R17], which the
  표준약관 implements — 「회사가 적립한 사망 당시의 계약자적립액」 [REG-R25 제22조](#krlib-reg-r25) — and
  beneath which 상법 제736조 is the floor [REG-R50]. It is `av_pp(t) × pols_death(t)`: zero
  at `t = 0` because the account is nil, and **zero from `t = 447`** because the account is
  exhausted. `LTC_KR_S`, `Child_KR_S` and `Medical_KR_S` inherit the same requirement.

The account itself is a retrospective recursion floored at zero,
`av_pp(t+1) = max(0, (av_pp(t) + prem_alloc_pp(t) − risk_prem_pp(t)) · (1 + i)^(1/12))`, and
the floor **binds on the anchor cell** — because the anchor's ₩45,000 is the figure the
specification states rather than the shipped basis's own equivalence level of ₩66,289, 32.1%
below it. Every other model point carries its own equivalence premium, and only points 1, 2,
4, 5, 6 and 9 exhaust the account at all. A recursion allowed to go negative would carry a
fictitious asset and pay `claims_death` out of it, which `check_net_cf()` would not catch
because the ledger identity balances either way. `risk_prem_pp` deliberately excludes the
DEATH and LAPSE lines: they are payments *out of* the account, so including them makes the
recursion self-referential — modelx raises rather than silently mis-answering, but a hand
implementation will not.

## Two surrender values, and a face amount this product does not have

`cv_pp(t)` is what the contract actually pays and `cv_std_pp(t)` the 표준형 comparator that
cannot be bought on this form; `check_cv_floor()` asserts `0 ≤ cv_pp ≤ cv_std_pp` and that
`cv_pp` is nil for the whole 납입기간 on the 미지급형 base. Two independent mechanisms move
them and conflating the two is the classic error here:

- the **해약공제기간 is capped at seven years** by 제7-66조제1항제2호 [REG-R19], so
  `surr_chg_pp(t) = 0` from `t = 84`;
- the **미지급형 cliff** is at 납입완료, `t = 240`, where the value steps from nil to
  ₩4,078,536.79 [S3 제41조] and the lapse rate steps from 0.1% to 0.8% [REG-R27] in the same
  row, taking `claims_lapse` from ₩0.00 to ₩1,891.71.

Thirteen years apart, and implementing one without the other gives a plausible-looking row
that is wrong by the whole of the other factor.

The 표준해약공제액 needs a **보험가입금액**, and this product has no death benefit to supply
one. [별표 15] 제3호 covers only 일반사망을 보장하는 보장성보험, so a cancer contract falls
into **제9호** and takes a *notional* face amount by scaling a term assurance's by a
risk-premium ratio, computed at the 기준연령 요건 [REG-R21] [REG-R9]. Reproducing that ratio
needs a term assurance's risk-premium scale the model does not carry, so `notional_sa_ratio =
0.60` **[std]** stands in for it. Feeding the ₩30,000,000 headline in instead gives
`459,000 + 300,000 = 759,000` against `459,000 + 180,000 = 639,000` — and because the
13-month cap of **₩585,000** binds either way [REG-R29], **the error is invisible on the
anchor cell and visible wherever the sum insured is low relative to the premium** — only then
does the [별표 14] formula fall below the 13-month cap. Model point 10, the sum-insured floor
of ₩10,000,000 against ₩23,000 a month, is where it shows: the formula gives ₩294,600 against
a cap of ₩299,000, so the notional ratio decides the answer where the headline face amount
would have put it back on the cap. This is the route by which a Korean 제3보험 product with
no face amount acquires one, and `LTC_KR_S` and `Child_KR_S` inherit it — with the
difference that 제9호's third bullet excludes long-term-care risk premium from the ratio
[REG-R21].

## Processing order within month `t`

Stated because nothing in any retrieved document states one, and because two of the six steps
change the answer if they are swapped.

1. **Premium** on `pols_payer(t)` and **maintenance expense** on `pols_if(t)`, at the start
   of the month. Two weights, two lines, one row.
2. **Diagnoses**, at the end: `diag_gen_h` and `diag_minor` out of `pols_healthy`,
   `diag_gen_m` out of `pols_minor`, `diag_high` as a **subset** of the general flow, and
   `diag_similar` on the whole in-force against the once-only ledger.
3. **Diagnosis benefits**, scaled by `reduction_factor(t)` and gated by `cover(t)` for the
   three invasive tiers and `cover_similar(t)` for 유사암.
4. **Care benefits** on the six duration cohorts of both diagnosed states — on the *stock*,
   never on the flow.
5. **Decrements**, in the order **transition → mortality → lapse**, each state on its own
   basis. A life diagnosed in month `t` takes its new state's mortality for the rest of it.
6. **The 계약자적립액 recursion**, then `claims(t, "DEATH")` releasing `av_pp(t)` and
   `claims(t, "LAPSE")` releasing `cv_pp(t)`.

Two consequences fall straight out of the ordering and both are pinned by tests.
**Diagnosis lines ride on flows and care lines ride on stocks**: `claims_diag_*(t)` uses the
month's new diagnoses and `claims_hosp/surgery/treat(t)` uses `pols_diag_dur(t, k)`, the
stock at the start of the month; multiplying a care intensity by a diagnosis flow understates
the care limbs by the mean diagnosed duration — 57 at 만나이 50, 80 at 60 and 148 at 80.
And **the care limbs start one month after the diagnosis limbs**: `claims_hosp(3) = 0` while
`claims_hosp(4) = 13.6639954092`, because a life diagnosed in month 3 is in the diagnosed
stock from month 4.

## The tier algebra: a partition, a subset and an addition

Four monthly incidences come off one published rate, and their algebra differs line by line.
`check_tier_shares()` asserts exactly this and nothing more:

    i_g + i_m = inc_rate / 12       일반암 and 특정소액암 PARTITION the base rate
    i_h <= i_g                      고액암 is a SUBSET, paid in ADDITION
    i_z >= 0                        유사암 is ADDITIVE to the base rate

**고액암 pays in addition, not instead** [S3], so `claims_diag_gen(3) = 1,360.1145372945` and
`claims_diag_high(3) = 49.7602879498` are both paid on overlapping flows: a leukaemia collects
200% of `S` and a stomach cancer 100%. Treating 고액암 as a fifth slice of a partition halves
it. And **유사암 is additive because the published grid excludes it**: the bureau's rate is
stated on invasive cancer excluding 기타피부암 (C44) and 갑상선암 (C73) [R5] [REG-R61], which
is exactly the 유사암 boundary the 약관 draw, so the grid and the reduced tier fit together
rather than needing reconciliation and `similar_share` can and does **exceed 1.0** — 1.60 at
female 만나이 20. A model that constrains the four shares to sum to one prices the reduced
tier out of existence at precisely the ages where it dominates.

## Two ledgers that are per policy and per diagnosed life

`similar_avail(t)` is the 유사암 tier's once-only availability and it rides on **`pols_if`,
not on `pols_healthy`**: a life who has already had an invasive cancer can still collect a
유사암 benefit, because no payment terminates or exhausts the contract [S1] [S3] [S4].
`check_similar_ledger()` asserts `similar_avail(t) + similar_used(t) = 1` with the used side
accumulated off the **published claim line** rather than off the recursion, so the identity
cannot close by construction. At the anchor cell `similar_avail(720) = 0.9172290909`: 8.28%
of policies consume the tier.

`treat_avail(k)` is the 최초 1회한 anti-cancer treatment benefit's availability, and it is a
per-**diagnosed-life** quantity evaluated at the **midpoint** of select year `k`, so
`treat_avail(1) = exp(−1.20 × 0.5) = 0.5488116361` rather than 1.0 or `exp(−1.20)`. Reading
it at the start of the year pays every entrant at full availability; reading it at the end
understates. Weighting it by `pols_cancer` would measure the block's consumption rather than
the individual's and defer exhaustion forever. The **ultimate first-treatment hazard is
exactly zero**, which is what makes the once-only bound hold at any horizon: a life reaching
the ultimate cohort without having drawn the benefit never draws it, so `treat_cum_pp(t)`
converges — to **0.7516253263** on the anchor cell. `check_treat_ledger()` asserts it never
passes 1.

One simplification is stated rather than hidden: the model runs **one aggregate 유사암
ledger** where the contracts pay each of the five members once. That **understates** the
tier, and it is a **[std]** scope decision rather than an approximation.

## Modules that are off in the base run

Four constructions are implemented and held at an inert base value, so the base run
reproduces the worked example while the machinery stays visible and testable.

| Switch | Base | What it does |
|---|---|---|
| `void_adjust` | `False` | Scales `pols_if_init()` by `1 − void_prob()`, de-recognising the **0.0003357124** of policies diagnosed inside the 90-day window. An in-window diagnosis makes the affected cover **무효**, not merely unpayable [S1 제28조제2항] [R7 제644조](#krlib-cancer-r7) — a **de-recognition, not a decrement** — so it releases the premium already collected as well as the future benefit and belongs in a validity adjustment at outset. Putting it in the lapse column keeps premium income the insurer never earned |
| `inc_be_factor` | `1.0` | The best-estimate adjustment to the sourced incidence basis. The shipped rate is a **참조순보험요율**, a net premium rate with a safety loading inside it, not a best estimate [REG-R4]. The claim that the loading is about 10% was seen only in a search summary and is **[unverified]**, so the factor is left at the identity rather than resting the model on an unconfirmed number. What *is* sourced is that the rate carries **no trend allowance at all** — 「현재도 예정위험률 산출 시 미래의 추세를 반영하지 않고 있음」 [R4] — while Korea's crude incidence has risen 161% since 1999 [R1]. Two errors, opposite signs, neither quantified |
| `renew_reprice_rate` | `0.0` | Steps the premium at each ten-year renewal on the 갱신형 chassis flag. Setting `chassis = "gaengsin"` already removes the 면책기간 and the 감액기간 [S2] [S4]; the base run holds the issue rate flat and records the contract-boundary tension rather than resolving it, which is a K-IFRS 1117 question [REG-R60] this model does not answer. Live on model point 3 |
| `lapse_canc_factor` | `1.0` | Inert rather than off: wherever the waiver fires a diagnosed life has no premium to miss and no surrender value to take, so `lapse_rate_canc_mth` returns zero whatever the factor is. It reaches a cash flow only on the `waiver_trigger = "none"` design, model point 9 |

## What is not modelled, and is named so it is not mistaken for absent

Each of these is specified in [`product-spec.md`](product-spec.md) and switched off here,
because its **rate** cannot be sourced even where its **mechanic** can:

- **재진단암.** The two-year clock and the four-limb definition (새로운 원발암 / 전이암 /
  재발암 / 잔여암) are sourced [S1] [S8], and no public source gives a cancer re-diagnosis
  incidence [R1] [R4]. Understates.
- **The 요양병원 limb.** Excluded from the inpatient benefit and its separate 90-day rider
  not carried [S2] [S8] — the market's own structural answer to the most disputed benefit in
  Korea, 2,125 암입원비 complaints in 2018 alone [R3].
- **암 사망, the 다빈치로봇 surgery limb and 비흡연체 rating**, all three of which appear in
  the retrieved wordings [S2] [S3] [S5] with no rate or differential published behind them.
- **Care benefits on the 유사암 tier.** Real contracts pay the inpatient and treatment limbs
  at 20–25% on 유사암 [S1]; the model pays nothing, because attaching invasive care
  intensities to a tier whose survival is 100.2% would credit it with an exposure no
  retrieved statistic measures [R1]. Understates.
- **부활.** Lapse is absorbing. A reinstated Korean cancer policy re-runs the 90 days from
  the 부활일 [S1] [S3] [S7] [REG-R25 제27조](#krlib-reg-r25), so it is not the policy that lapsed; modelling
  reinstatement as a negative lapse restores cover the contract does not restore and deletes
  a real anti-selection control. Conservative.
- **The stage drift.** Survival is a stage story far more than a site story and the mix is
  moving in the policyholder's favour — 국한 45.6% (2005) → 51.8% (2023) [R1] — which raises
  the cost of every post-diagnosis limb. The model holds the survival basis flat.

And one boundary in the other direction: **do not reuse `Medical_KR_S`'s machinery here.**
There is no 급여/비급여 split, no 자기부담금, no annual limit and no 재가입 in this product,
and no benefit here reimburses a cost. The one shared mechanic is the 제3보험 requirement to
pay the 계약자적립액 on death [REG-R17].

## Inputs are external files

Eight CSVs sit beside `run.py`, in the model folder's **parent**; the model folder holds
`__init__.py`, `_system.json` and its two Space folders and nothing else — no `_data/`, no
IOSpec, no embedded values — so a diff of the model shows logic changes only. This is the
`annuallife.TradLife_A` layout; contrast `basiclife.BasicTerm_S`, which keeps its inputs
*inside* the model. The consequence worth knowing: **the model is not portable on its own.**
Copying `Cancer_KR_S` without its parent's CSVs produces a model that reads and then fails on
first evaluation.

```
products/cancer/
    model_point_table.csv     <- inputs live here
    mort_table.csv            incidence_table.csv
    tier_share_table.csv      tier_table.csv
    survival_table.csv        care_table.csv
    lapse_table.csv
    run.py
    model.md  product-spec.md  technical-notes.md  sources.md
    Cancer_KR_S/              <- formulas only
        __init__.py  _system.json
        Data/__init__.py          (reads the CSVs, once per model)
        Projection/__init__.py    (the by-policy projection)
```

| File | Reference | Reader | Index | Contents |
|---|---|---|---|---|
| `model_point_table.csv` | `model_point_file` | `Data.model_point_table()` | `point_id` | ten model points; point 1 is the anchor |
| `mort_table.csv` | `mort_table_file` | `Data.mort_table()` | `sex`, `age` | all-cause mortality of the never-diagnosed, 만나이 15–100 |
| `incidence_table.csv` | `incidence_table_file` | `Data.incidence_table()` | `sex`, `age` | 암 발생률 excluding C44 and C73, on the published ten-year grid |
| `tier_share_table.csv` | `tier_share_file` | `Data.tier_share_table()` | `sex`, `age` | the three tier shares at anchors 20 / 40 / 60 / 80 |
| `tier_table.csv` | `tier_table_file` | `Data.tier_table()` | `tier` | the benefit ladder, each tier's 면책기간, and which tiers waive |
| `survival_table.csv` | `survival_table_file` | `Data.survival_table()` | `sex`, `tier`, `dur_year` | post-diagnosis excess hazard, select years 1–5 and ultimate |
| `care_table.csv` | `care_table_file` | `Data.care_table()` | `dur_year` | admissions, days, operations and first-treatment hazard per diagnosed life |
| `lapse_table.csv` | `lapse_table_file` | `Data.lapse_table()` | `segment` | three segments, not a policy-year grid |

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate ItemSpace
with its own cells cache; readers placed there would re-read every file for every model
point. They live in the unparameterized `Data` Space instead, and
`test_inputs_are_read_once_not_once_per_model_point` asserts the property against the file
set registered in `kr_registry.INPUT_FILES`. `input_dir()` returns `_model.path.parent`,
resolved at run time and never hard-coded, so the model works from any checkout.

**Every assumption CSV carries a `provenance` column and every cell in it begins with a
citation tag.** `model_point_table.csv` is the only exemption, a model point being a
configuration rather than an assumption. On this product the column does more work than
usual, because the eight files sit at three quite different levels of authority and a reader
must be able to tell which by eye: one is published data reproduced verbatim, one is a
construction fitted to public summary statistics, one is read off a 약관, and four are
standardizations with nothing published behind them at all.

### `incidence_table.csv` — published data, reproduced

This is the file that makes the product an exception in this library. 보험개발원, the
statutory 보험요율 산출기관 of 보험업법 제176조 [REG-R4], displays its 장기손해보험
참조순보험요율 in force **적용시점 2024년 4월 1일 이후**, and that display carries a
「기타피부암 및 갑상선암 이외의 암 발생률」 grid by age and sex [R5] [REG-R61]:

| 만나이 | 0 | 10 | 20 | 30 | **40** | 50 | 60 | 70 | 80 |
|---|---|---|---|---|---|---|---|---|---|
| 남자 | 0.000297 | 0.000148 | 0.000230 | 0.000531 | **0.001343** | 0.003567 | 0.008540 | 0.019206 | 0.027892 |
| 여자 | 0.000318 | 0.000152 | 0.000250 | 0.001005 | **0.003382** | 0.004962 | 0.006239 | 0.008626 | 0.011452 |

It is dated, it has a stated effective date, and **its definition is the insured one** —
invasive cancer excluding C44 and C73, classified by 원발부위 — so it already embodies the
tier carve-out the 약관 make and the 원발부위 rule the supervisor imposed from 2011-04-01.
Two things sit on top of it and both are **[std]**: `inc_rate(t)` interpolates **log-linearly**
between the published ten-year ages, which reproduces every published value exactly and is
locally the exponential family the curve follows; and the **two rows above 80**, at 90 and
100, are the age-80 rate × 1.15 held flat, on the deceleration [R1]'s crude bands show. Those
two rows are not decoration — **22.6%** of the anchor cell's diagnosis benefit is earned at
만나이 80 and above, and their `provenance` says so.

A unisex basis is materially wrong at every age and wrong in **opposite directions** either
side of about 55: at 만나이 40 the published female rate is **2.52×** the male, at 80 the
male is **2.44×** the female [R5]. The registry states the crossing in terms — 「50대
초반까지는 여자의 암발생률이 더 높다가, 50대 후반부터 남자의 암발생률이 더 높아지는」 [R1]
— and the published reference rate crosses in the same place. Model point 2 is the anchor's
female twin for exactly this reason.

The independent check is worth carrying: interpolating [R1]'s male all-site crude rates to
exact age 40 and deducting thyroid gives **0.001365** against the bureau's **0.001343**, a
difference of **+1.6%** with the right sign, because C44 could not be deducted — a published
net premium rate and an independently derived crude rate agreeing to within two per cent.

### `mort_table.csv` — a construction, not a copy

The opposite case, and the contrast is the point. Korea's industry table, the **제10회
경험생명표** applied from 2024-04, is **not published in full**: 보험개발원 releases the
평균수명 and the 기대여명 and not the rates [REG-R33] [REG-R34]. There is no Korean
equivalent of the freely downloadable Japanese 標準生命表, so there is no published rate to
anchor on. What is shipped is a Makeham

    q(x) = 1 − exp( −( A + B·c^(x + 0.5) ) )                                       [std]

whose two free parameters are solved so the table reproduces the **국가데이터처 생명표**'s
2024 기대여명 at 40 and 65 exactly — 남 41.9 / 19.5 and 여 47.4 / 23.7 [REG-R38] — and which
then returns 기대수명 at birth of 80.80 and 86.88 against the published 80.8 and 86.6. That
last is a **check, not a target**, and it is the only external validation available. Ages 15
to 100, the composite's issue-age range through to its 100세 만기. Drop a licensed extract in
over the same schema — `sex`, `age`, `mort_rate` — and no formula changes.

`mort_be_factor = 1.0`, and unlike jplib's 1.25 that is right: the shipped table is a
**population all-cause basis** calibrated to public 기대여명, not a valuation table with a
prudential margin, so there is no margin to unwind and scaling it would be inventing one.

### `tier_share_table.csv` and `survival_table.csv` — where the judgement lives

`tier_share_table.csv` splits the sourced base rate into the contract's four tiers and is
**[std] throughout**. The levels are anchored on [R1]'s 2023 all-ages crude site rates per
100,000 — 대장 63.8, 유방 58.4, 전립선 44.3 (the 특정소액암 sites), 갑상선 69.3 and
상피내암 74.7 (the 유사암 sites) against an excluding-thyroid base of 495.0 — and then
**graded in age and split by sex**, because those all-ages figures mix age distributions that
differ violently. Interpolation between the four anchors is **linear**, not log-linear: a
bounded share that may exceed 1.0 has no meaningful log-linear interpolation. **The 유사암
share is a floor**: [R1] does not cover 경계성종양 at all, does not identify 대장점막내암
inside 대장 D010–D012, and does not carry 기타피부암 in its top-ten table. The **고액암**
share is the weakest of the three — none of 골, 뇌 or 백혈병 is in the retrieved top-ten
table, so it has no published anchor at all.

`survival_table.csv` is the post-diagnosis basis, and it exists because a cancer contract
goes on paying after the diagnosis benefit. The public quantity is **relative survival** —
「관찰생존율을 일반인구의 기대생존율로 나누어 구한 값」 [R1] — a *ratio to an expected
general-population survival*, not a cohort curve and not a transition rate, so it converts
into an **excess hazard added to** the base table and never into a replacement for it;
multiplying survivorship by a relative-survival figure double-counts the background. The
calibration is exact where the target is public: the five male general-tier hazards sum to
**0.41703175 = −ln(0.659)**, the published male excluding-thyroid 5년 상대생존율 of 65.9%
[R1], and the five 특정소액암 hazards to **0.13857264 = −ln(0.8706)**, built from 대장 75.6,
유방 94.7 and 전립선 96.9 per cent [R1]. The **grading across the five select years and the
non-zero ultimate** are [std]: a flat hazard reproducing 65.9% would be 0.0834063 a year, and
holding it flat kills long survivors far too fast when 62.1% of the prevalent population is
beyond year five [R1].

### `care_table.csv` — the weakest file, and it says so on every row

**No Korean source publishes cancer admissions, bed-days, operations or treatment courses per
diagnosed patient.** [R1] publishes incidence, survival and prevalence and nothing about
treatment volume, and the one published utilisation series on the 보험개발원 display is a
**질병입원율 for all disease** [R5]. So the file is [std] throughout: its *shape* standardized
on the clinical ordering the contracts' own design implies — treatment front-loaded into the
first two years and decaying to a maintenance level — and its *level* on the 180-day-per-stay
cap those contracts carry [S1] [S4] [R3]. Three properties are worth stating. No row's
`hosp_days_adm` approaches the 180-day cap, so **`check_hosp_cap()` asserts that the
contractual cap is respected, not that it bites**; `surg_open_yr + surg_closed_yr` in select
year 1 is **0.90**, about one operation per newly diagnosed life, which is the sanity check;
and the ultimate first-treatment hazard is **exactly zero**, which is what makes the 최초
1회한 bound hold at any horizon.

### `lapse_table.csv` and `tier_table.csv`

`lapse_table.csv` carries **three segments rather than a policy-year grid**, because the
functional form is *prescribed* rather than observed. 감독규정 제7-66조제4항 permits the
미지급형 form only where the premium or benefit was calculated on a **최적해지율** [REG-R19],
and the FSS's November 2024 계리가정 ruling then fixes the shape: among models converging to
zero lapse at 완납 the **로그-선형 모형** is the 원칙모형, converging to **0.1%**, with a
post-완납 ultimate of **0.8%** [REG-R27]. Those two endpoints are the ruling's own numbers
and are sourced; **only the 4.6% starting level is [std]**, and it has no observed range,
because no public Korean lapse or persistency figure for 암보험 exists [R3]. The
instrument-level caveat is real and is carried at the point of use: the 「IFRS17 주요 계리가정
가이드라인」 attachment was never converted from HWP, so the values are verified from the
보도자료 and **the functional form is [unverified]** at instrument level [REG-R27].

`tier_table.csv` is the benefit ladder itself — 200 / 100 / 60 / 20 per cent of the
보험가입금액 — read directly off the one retrieved 약관 that states every tier as an amount at
보험가입금액 1,000만원 [S3 별표 1]. It also carries **each tier's own `wait_months`**, which
is where the product's two start dates come from, and a `waives_premium` flag that is 1 for
일반암 and 고액암 alone [S3 제14조제1항] [S1 제9조제1항]. It is the most heavily sourced file
in the directory and the only one whose every row is [S#] rather than [std].

### No input file is keyed by the projection index

**Not one of the eight CSVs carries the model's `t`**, so the move to the 0-based frame left
every input file untouched. The time-like columns and what each of them is:

- `survival_table.csv` and `care_table.csv` — **`dur_year`, values 1 to 6.** Elapsed *select
  year since diagnosis*, with 6 standing for the ultimate, on a clock that starts at the
  진단확정일 and not at the 보험계약일. It is a 1-based contractual duration label of the same
  kind as a policy year, read by `excess_hazard(tier, k)`, `treat_avail(k)` and the care limbs
  of `claims(t, kind)` with `k = 1 … 6`, and the only place it is derived from the frame at all
  is `treat_cum_pp(t)`'s `k = min(6, (t − 1) // 12 + 1)` for a life diagnosed at `t = 0`.
  **Left as written.**
- `mort_table.csv`, `incidence_table.csv`, `tier_share_table.csv` — **`age`.** Attained 만나이,
  reached through `age(t) = issue_age() + t // 12`. Not a time index. **Left as written.**
- `model_point_table.csv` — **`wait_months`, `reduction_months`, `pay_term_y`.** Elapsed
  counts, already 0-based by nature: `wait_months = 3` means cover attaches once three whole
  months have elapsed, which on the 0-based frame is `t = 3`, and `reduction_months = 12` means
  the 감액기간 covers `t < 12`. Neither is a point on the frame's axis that has to move with it.
  **Left as written.**
- `tier_table.csv` — **`wait_months`.** The same elapsed count, per tier. **Left as written.**
- `lapse_table.csv` — **`segment`**, three named segments and no policy-year grid; the
  policy-year mapping happens in `lapse_rate(t)` through `policy_year(t) = t // 12 + 1`.
  **Left as written.**

## Sign convention

`net_cf` is **income positive** — premiums less every benefit line, less `expenses`, less
`claim_expenses`, less `commissions` — which is the library-wide sign, so there is no
outgo-positive `liability_cf` companion to publish: one stream, one sign, one name.

The identity `check_net_cf()` asserts, stated in one line: **`premiums` less the ten
`claims_*` columns, less `expenses`, less `claim_expenses`, less `commissions`, equals
`net_cf`, in every projected month.** It is rebuilt from the columns of `result_cf()` rather
than from the `net_cf` cells, so a column wired to the wrong cells, a benefit line dropped
from the table or a double-counted claim expense shows up as a non-zero residual in the very
table a reader is looking at. The benefit side is swept as every column whose name begins
`claims_`, taken as a group rather than enumerated — which it can be, because
**`result_cf()` publishes the ten splits and no bare `claims` subtotal beside them**. The
`claims(t, kind)` cells still returns the total when `kind` is omitted; it is the *column*
that is retired, and `RETIRED_COLUMNS` in the conventions suite keeps it retired.

The asymmetry that defines this product's cash-flow signature sits inside that one line:
**premiums are weighted by `pols_healthy + pols_minor` and three of the benefit lines by the
diagnosed cohorts**, because the waiver fires on the same first invasive diagnosis that
starts every care limb. Meanwhile `expenses` rides on `pols_if`, because a waived policy is
still administered. At `t = 4` the premium weight and `pols_if` differ by ₩4.03; by 납입완료
the gap is 3.69% of the block, and by 만나이 80 the waived state alone is 17.7% of the
in-force. **It is invisible for the first four rows, where the two are equal**, which is
exactly why a first-year test does not catch it. `pols_payer()` is where the choice is made,
and it is a *product* choice: on `waiver_trigger = "none"` — model point 9 — the diagnosed
keep paying and can lapse.

## Naming

Cells names follow lifelib's `basiclife/BasicTerm_S` wherever it has an analogue — `pols_*`
for policy counts, plural nouns for cash flows, `*_rate` for annual rates and `*_rate_mth`
for their monthly counterparts, `claims(t, kind)` with an uppercase `kind` string. The full
notes-symbol-to-cells mapping lives in the `Projection` docstring, headed `Notes symbol`, and
is not repeated here; `test_the_projection_docstring_carries_the_symbol_map` in
`tests/test_model_conventions_kr.py` asserts it carries at least `proj_len` and
`model_point`.

### Names that needed care

| Notes | Cells | Why |
|---|---|---|
| `l_n(t)`, `l_w(t)` | `pols_minor` / `pols_waived` | The two diagnosed states are named for **what the contract does to the premium**, not for the tier that caused them — because that is the only difference that reaches a cash flow. `pols_cancer` is their sum and is published for the roll-forward alone |
| `D_n(t,k)`, `D_w(t,k)` | `pols_minor_dur` / `pols_waived_dur` | The `_dur` suffix marks a count keyed by **elapsed duration since diagnosis**, distinct from `policy_year`. `pols_diag_dur(t, k)` is the union the care limbs ride on |
| `Z(t)` | `similar_avail` / `similar_used` | A once-only ledger per **policy**, with `similar_used` accumulated off the published claim line and not off the recursion, so `check_similar_ledger` cannot close by construction |
| `A(k)` | `treat_avail` | Keyed by the **select year `k`**, not by `t`: a per-diagnosed-life availability, which is why it is not a function of the projection period at all |
| `w(t)` vs `w_c(t)` | `lapse_rate_mth` / `lapse_rate_canc_mth` | Two monthly lapse rates, because the waiver makes one of them identically zero. `lapse_rate` stays the **annual** rate, which the conventions suite asserts |
| `CV(t)` vs `CV_std(t)` | `cv_pp` / `cv_std_pp` | What is paid against the 표준형 comparator that cannot be bought. Publishing only one of the two hides the whole of the 미지급형 form |
| `alpha_cap` | `surr_chg_cap_pp` | The **표준해약공제액**, a statutory cap on `surr_chg_pp`; named for the cap and not for the charge, because the two differ at every duration inside the 해약공제기간 |
| *(no symbol)* | `claims(t, "MATURITY")` | Exists and returns zero at every `t`. A column of zeros states the product fact where a missing column would hide it |

### What this product argued in the cross-model naming review

Three settlements in `RETIRED_NAMES` came out of the review and this model observes all
three. **`yejeong_rate` → `prem_int_rate`**: 예정이율 is the *pricing* rate and must not share
a name with the declared crediting rate `decl_rate` — this model has a 예정이율 and, being
금리확정형, no 공시이율 at all, and the distinction is only visible if the names differ.
**`surr_charge_pp` → `surr_chg_pp`**, with the Korean cap spelled `surr_chg_cap_pp`; this
product is one of the four that computes the cap from [별표 14] rather than reading a
schedule. **`cv_ratio` → `cv_floor_ratio`**, because a bare ratio name said nothing about
which of the two ratios on the 무·저해지 chassis it was; here `cv_floor_ratio = 0.0` is the
미지급형 fraction during the 납입기간 and `cv_post_pay_ratio = 0.5` the fraction afterwards,
and one name could not have carried both.

Two names this product **argued for and kept**: `pols_maturity` rather than `pols_expiry`,
because the count whose cover ends at the scheduled end of the contract is a maturity in the
library's vocabulary whether or not a benefit attaches; and `mort_be_factor` rather than
`mort_ae_factor`, since the library adjusts a table to a best estimate rather than computing
an actual-to-expected ratio, and a name meaning A/E could not have said why this model holds
the factor at 1.0.

## Standardizations used

Every row is **[std]**. The sourced contractual parameters — the 90 days and the 유사암
carve-out from it, the 감액기간, the four tier ratios, the 최초 1회한 form, the waiver
triggers, the 7-year 해약공제기간, the [별표 14] coefficients and the 미지급형 fractions —
are in [`product-spec.md`](product-spec.md) and [`technical-notes.md`](technical-notes.md)
and are not repeated. "Observed range" is what the retrieved documents actually bound;
several of them bound nothing at all, which is said rather than papered over.

| Parameter | Value | Rationale | Observed range |
|---|---|---|---|
| age basis | **만나이** throughout | every decrement the model uses is published on 만나이 — [R1]'s bands, [R5]'s age grid, [REG-R38]'s life table — and converting to the contract's 보험나이 needs a distribution of issue dates within the policy year that no source supplies | the two differ for roughly half of all issue dates; on the steep part of the curve half a year is worth about **3.5%** of the rate [R5] |
| `inc_rate` interpolation | log-linear in age between published grid ages | reproduces every published value exactly and is locally the exponential family the curve follows | linear interpolation of a grid that rises by a factor of 20.8 across the projection understates the mid-decade rate materially |
| incidence above age 80 | age-80 rate × 1.15, flat | the published grid stops at 80 and the anchor projects to 100; the deceleration is [R1]'s own crude bands | log-linear extrapolation of the 70→80 slope reaches 0.0405 at male 90, a decadal step of 1.45 where [R1]'s male 80+ band is only 1.24x its 70-79 band |
| `inc_be_factor` | 1.0 | the shipped rate is a net premium rate, not a best estimate [REG-R4]; the identity is a decision, not an omission | the "about 10%" loading was seen only in a search summary and is [unverified] |
| `tier_share_table.csv` | age-graded, sex-split shares at anchors 20 / 40 / 60 / 80, linearly interpolated | the crude all-ages site rates the registry publishes mix age distributions that differ violently; ungraded shares misprice the reduced tier in both directions | at female 만나이 30 the 유사암 rate is 0.001136 against a general-tier 0.000593; by 60 the ratio is 0.20 |
| 유사암 share | a **floor**, not an estimate | [R1] does not cover 경계성종양, does not identify 대장점막내암 inside D010–D012, and does not carry 기타피부암 in its top-ten table | 10% [S6] [S7], 20% [S3] [S4] and 70% [S8] on the *benefit ratio*; nothing published on the *incidence* share |
| 고액암 share | 0.030 at male 40, graded | none of 골, 뇌 or 백혈병 is in the retrieved top-ten table | **none published at all** — the weakest of the three shares |
| one aggregate 유사암 ledger | one, not five | the contracts pay each of the five members once; the model pays the tier once | understates, and by construction |
| no care benefits on 유사암 | zero | attaching invasive care intensities to a tier at 100.2% relative survival credits it with an exposure no statistic measures [R1] | real contracts pay the inpatient and treatment limbs at **20–25%** on 유사암 [S1] |
| `mort_table.csv` | Makeham fitted to two 기대여명 anchors per sex [REG-R38] | the 제10회 경험생명표 is not published in full [REG-R33] [REG-R34], so there is no rate to anchor on | the fit returns 기대수명 80.80 / 86.88 against the published 80.8 / 86.6 — a check, not a target |
| `mort_be_factor` | 1.0 | a population all-cause basis has no prudential margin to unwind | jplib carries 1.25 against a *valuation* table; the two are not comparable |
| `survival_table.csv` grading | five select years plus a non-zero ultimate of 0.020 / 0.008 | a flat hazard at 0.0834063 kills long survivors far too fast when 62.1% of the prevalent population is beyond year five [R1] | the five-year *totals* are sourced exactly; the shape between them is not |
| `care_table.csv` | [std] on every row | **no Korean source publishes cancer utilisation per diagnosed patient**; the only published series is a 질병입원율 for all disease [R5] | none; the level is anchored on the 180-day cap [S1] [S4] and the year-1 operation count of 0.90 |
| `treat_avail(k)` | mid-cohort, `exp(−Σ hazard × span)` at month `12(k−1)+6` | reading at the start of the year pays every entrant at full availability; at the end, understates | none; the ultimate hazard is set to **exactly zero** so the 최초 1회한 bound holds at any horizon |
| lapse starting level | 4.6% p.a. in policy year 1 | set so the log-linear path from 4.6% to the prescribed 0.1% averages about 1.2% a year over the 20-year 납입기간 | **no public Korean lapse figure for 암보험 exists** [R3]; carried from a disclosed 적용해지율 envelope (4.6% at one carrier, 8.4% at another) |
| lapse is absorbing | 부활 not modelled | a reinstated policy re-runs the 90 days [S1] [S3] [S7] | conservative; nothing published on Korean reinstatement rates |
| `prem_int_rate` | 2.50% p.a., 금리확정형 | anchored on the 2026 **평균공시이율**, which the FSS Governor computes under 감독규정 제1-2조제13호 [REG-R9] [REG-R48] | 연복리 1.5% on one retrieved product [S8]; a 0.5% 최저보증이율 floor on another [S1] |
| `notional_sa_ratio` | 0.60 of the headline sum insured | [별표 15] 제9호's ratio needs a term assurance's risk-premium scale the model does not carry [REG-R21] | working back from the 13-month cap on the specification's illustrative 25% loading gives about 0.60 (footnote 30); on the model's own 15% gross-to-net it gives 0.42, and the cap binds either way at the anchor, so the choice is invisible there and visible on point 10, where the sum insured is low relative to the premium |
| `expense_acq` / `comm_init_rate` | ₩300,000 at issue / 0.6 × annualised premium | together ₩624,000, **13.9 months of premium**, sitting against the FSC's 13-month statement of the [별표 14] cap for a 보장성보험 [REG-R29] [REG-R20] | no Korean carrier publishes an expense basis: [S1] names 계약체결비용 and 계약관리비용 and quantifies neither; [S8] states the deduction without quantifying it |
| `expense_maint` / `inflation_rate` | ₩2,500 a month / 2.0% p.a. | on `pols_if`, because a waived policy is still administered | none published |
| `expense_claim_diag` / `_hosp` | ₩150,000 per diagnosis / ₩30,000 per admission | on the event counts, not on `pols_if` — different weights, so publishing one column would hide a real movement | none published |
| `prem_load_acq` + `prem_load_maint` | 10% + 5% = 15% gross-to-net | drives `prem_alloc_pp` = ₩38,250 a month while `t < 240` | the 산출방법서 is a 기초서류, filed and never published [REG-R2] |
| anchor premium | ₩45,000 a month | the figure `product-spec.md` states; **a modelling input, not a quoted rate** | the shipped basis's own equivalence premium is **₩66,289** — ₩45,000 is 32.1% below it — and that gap is why the anchor's account is exhausted at `t = 447`. Scaling by the 1.2352 PV ratio gives ₩55,586 and is only a lower bound: `claims_death` and `claims_lapse` ride on the 계약자적립액 and so rise with the premium |
| processing order | premium → diagnosis → benefits → transition → mortality → lapse | the transition must precede mortality, or a life diagnosed in month `t` carries the healthy hazard through the month it was diagnosed in | nothing in any retrieved document states a processing order |
| `roll_fwd_tol` | 1e-10, scaled by `sum_assured()` in the money checks | one tolerance closes identities between policy counts; the money identities compare won amounts of order 1e8 | `roll_fwd_tol × S` is ₩0.003 at the anchor, far below the smallest error a reader adding up the statement could see |

## Tests

`tests/test_cancer_kr.py` holds the notes' worked example **hard-coded as module-level
tables**, so a reviewer can lay it beside [`technical-notes.md`](technical-notes.md) and
compare by eye rather than by re-running the model. Money is asserted to the ten decimal
places the notes print, in-force counts and rates to ten, and the ledgers to ten.

- **The derived scalars**: `proj_len() = 721` and `result_cf()` at 721 rows, indexed
  `t = 0 … 720`,
  `pay_months() = 240`, `pols_if_init() = 1.0`, `surr_chg_months() = 84`, and
  **`surr_chg_cap_pp() = 585,000`** from the [별표 14] arithmetic in full, including that the
  13-month cap binds and that the [별표 15] 제9호 notional face amount is what enters it.
- **The benefit ladder and the two start dates**: `benefit_ratio` and `tier_wait_months` for
  all four tiers, and that `cover(2) = 0` while `cover_similar(0) = 1`.
- **The assumption basis at the anchor**: `inc_rate(0) = 0.001343` read verbatim from [R5],
  the log-linear `inc_rate(12) = 0.0014808079`, the three tier shares at 만나이 40 and 41,
  the four monthly tier incidences, `mort_rate(0) = 0.0011068200` and its monthly form, both
  excess-hazard vectors **including that the five general-tier hazards sum to −ln(0.659)**
  and the five 특정소액암 hazards to −ln(0.8706), the six `treat_avail` values, and the three
  per-diagnosed-life-month care amounts — ₩125,000.00, ₩275,000.00 and ₩548,811.64 in select
  year 1, and ₩8,125.00 / ₩10,833.33 / ₩0.00 in the ultimate.
- **The first sixteen months** of `result_cf()` and `result_pols()` row by row, the four hand
  traces the notes carry, **policy year 1 in aggregate** — ₩528,108.33 of premium against
  ₩19,994.28 of benefit, closing at −₩145,503.30 — and the **undiscounted totals over all
  721 months**: ₩8,586,707.2756349239 of premium, ₩8,009,869.07 of diagnosis benefit,
  ₩4,192,693.32 of care benefit, ₩1,474,174.97 of account payments and
  **−₩7,466,785.4889610466** of net cash flow, with the expected-payment counts each line
  implies (0.1971 일반암, 0.0062 고액암, 0.0930 특정소액암, 0.0395 유사암, 0.1960 treatment).
- **The equivalence premium on the shipped basis**: the 152.7418594890-month premium annuity,
  the 1.2352479168 PV ratio and the ₩55,586 lower bound it scales to, against the solved
  equivalence level of ₩66,289 and the shipped ₩45,000.
- **The account, surrender and ledger paths**: `av_pp(447) = 0` and zero thereafter,
  `surr_chg_pp(84) = 0`, `cv_pp(t) = 0` for every `t < 240`, the step to ₩4,078,536.79 at
  `t = 240` with `claims_lapse` moving from ₩0.00 to ₩1,891.71 in that same row,
  `similar_avail(720) = 0.9172290909`, and `treat_cum_pp` converging to 0.7516253263.

Every entry in the notes' **Known modeling pitfalls** list has a test of its own, named after
the pitfall, because each is a way an implementation can look right and be wrong: the two
waiting periods and the 면책기간 stopping the transition as well as the benefit, with the
premium still charged inside it and voidness a de-recognition rather than a decrement;
`premiums` on `pols_healthy + pols_minor` while `expenses` is on `pols_if`; 특정소액암 not
waiving and still able to lapse where a waived life cannot; 고액암 as a subset paid in
addition and 유사암 as additive with a share exceeding 1.0; the 감액기간 as a first-year
phenomenon; diagnosis lines on flows against care lines on stocks, starting a month later;
the thirteen-month cohort delay; the per-life treatment ledger with its zero ultimate hazard
and the 유사암 ledger on `pols_if`; relative survival as an excess hazard rather than a
survivorship multiplier, and 유사암 carrying neither excess mortality nor a care benefit; the
notional 보험가입금액; the 7-year 해약공제기간 against the 납입완료 cliff and the two
prescribed steps landing in one row; `claims_lapse` identically zero; the payment on death
with no death benefit and the account floor binding; `risk_prem_pp` excluding the DEATH and
LAPSE lines; nothing paid at expiry; the ten `claims_*` splits with no `claims` column;
rounded lines not re-adding and `commissions(0) = 323,999.9999999999`; `proj_len()` as the
row count rather than the last index; log-linear against linear interpolation; the [std]
incidence rows above 80 carrying 22.6% of the diagnosis benefit; 부활 re-running the 90
days; and not reusing `Medical_KR_S`'s machinery.

Beyond those: all **ten** `check_*` identities on all **ten** model points, each optional
module in both positions of its switch, the `result_cf()` column vocabulary, the CSVs'
encoding and every assumption file's row-by-row `provenance` tags, an input swapped by
repointing a filename Reference, and a read → write → re-read round trip against the same
golden values.

The ten checks, and what each would catch:

| Check | Identity | What breaks it |
|---|---|---|
| `check_pols_roll_fwd` | `pols_if(t) − pols_if(t+1) = deaths + lapses + maturities` | an exit that is not one of the three — most likely a diagnosis counted as one |
| `check_cancer_roll_fwd` | `pols_cancer(t+1) = Σ_k exposure × survival`, the graduation terms telescoping | a cohort losing or gaining lives at a boundary |
| `check_canc_dur_ledger` | both states' cohort 1 rebuilt independently from the entry history | the thirteen-month delay off by one — the only check that catches it |
| `check_similar_ledger` | `similar_avail(t) + similar_used(t) = 1`, used read off the claim line | the once-only tier paying twice, or the ledger riding on `pols_healthy` |
| `check_treat_ledger` | `treat_cum_pp(t) ≤ 1` at every `t` | a per-block rather than per-life ledger, or a non-zero ultimate hazard |
| `check_tier_shares` | `i_g + i_m = inc_rate/12`; `i_h ≤ i_g`; `i_z ≥ 0` | 고액암 treated as a slice of a partition, or 유사암 constrained to fit inside one |
| `check_waiting_period` | no invasive benefit **and no invasive transition** before `t = 3` | gating the claim but not the transition |
| `check_cv_floor` | `0 ≤ cv_pp ≤ cv_std_pp`, and `cv_pp = 0` for the whole 납입기간 on 미지급형 | the suppression applied to the wrong period, or the cliff at the surrender-charge date |
| `check_hosp_cap` | no cohort's mean stay passes the 180-day per-stay cap | a care intensity raised past what the contract will pay |
| `check_net_cf` | the published statement's own columns rebuild `net_cf(t)` | a benefit kind missing from the table, or a claim expense counted twice |

`tests/test_model_conventions_kr.py` adds the house style, parametrized over
`kr_registry.MODELS` rather than restated here: the two-Space layout, the external inputs
read once per model with no orphan CSV, the `provenance` column on every assumption CSV, the
docstrings and their required phrases, the age basis in the registry metadata — `MONTHLY |
MAN` for this model — against the `Projection` docstring, the retired-name and
retired-column registers, the `result_cf()` contract (indexed by `t`, first column `pols_if`,
a `net_cf` column, all names `lower_snake_case`, no NaN, length equal to `proj_len()` and the
index running `0 … proj_len() − 1`), and
that every `check_*()` returns `True` on **every** shipped model point.

```bash
python -m pytest tests/test_cancer_kr.py -q
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-cancer-r1
[R3]: #krlib-cancer-r3
[R4]: #krlib-cancer-r4
[R5]: #krlib-cancer-r5
[R6]: #krlib-cancer-r6
[REG-R17]: #krlib-reg-r17
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R21]: #krlib-reg-r21
[REG-R27]: #krlib-reg-r27
[REG-R29]: #krlib-reg-r29
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R38]: #krlib-reg-r38
[REG-R4]: #krlib-reg-r4
[REG-R48]: #krlib-reg-r48
[REG-R50]: #krlib-reg-r50
[REG-R60]: #krlib-reg-r60
[REG-R61]: #krlib-reg-r61
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
