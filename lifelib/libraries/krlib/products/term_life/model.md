# Implementation Notes

**Status:** Draft, 2026-09-03. Built from [`technical-notes.md`](technical-notes.md); the
product those notes describe is specified in [`product-spec.md`](product-spec.md), and every
source tag on this page resolves in [`sources.md`](sources.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics are sourced: attained-age repricing at 갱신 (*gaengsin*, renewal)
> with no 고지 (*goji*, disclosure) and no underwriting, truncation of the final cycle at
> the 보험나이 80 ceiling, the premium waiver **not** surviving a renewal, the nil
> 해약환급금 (*haeyak hwangeupgeum*, surrender value) at every duration on the
> representative 전기납 무해지 form and hence the absence of any policy loan, the
> 선지급서비스특약 (accelerated death benefit) cap, and the three-year 부활
> (*buhwal*, reinstatement) window. So, unusually for this repository, are the
> **premiums**: the 생명보험협회 publishes a statutory cross-carrier comparison on one
> prescribed basis and every 상품요약서 prints a premium grid, so the anchor cell's
> ₩15,080 a month is a published figure appearing twice independently [S12] [S4], and the
> whole 갱신형 renewal ladder is published [S7]. Everything else is **[std]** — the
> best-estimate mortality factor, the best-estimate lapse level, the renewal-decline rate,
> the shortened-pay equivalence, the expense and commission levels — and `mort_table.csv`
> is a documented **construction**, not the 경험생명표, which is not published at all.
> Replace it all with company data before drawing any conclusion from the numbers.

## Run it

```bash
python products/term_life/run.py            # the anchor cell, point_id = 1
python products/term_life/run.py 3          # the 갱신형 cell, to the ceiling
```

`run.py` prints the model point, the first twelve months of the cash flow statement, the
undiscounted totals and the seven `check_*` identities. Everything it prints is ASCII, so
the output lands on a Windows console under any code page: amounts are labelled `KRW`, and
the product, the two renewal structures and the age basis are romanized. Real output, with
the twelve-row statement elided — it is reproduced in full in
[`technical-notes.md`](technical-notes.md):

```text
Term_KR_S - jeonggi boheom (level term life), KRW, monthly grid, boheom nai
model point 1: KR-TL-0001 - M40, bi-gaengsin (non-renewable)
  20-year term, jeongi-nap (whole-term pay), sunsu bojanghyeong (pure protection), standard class, cover KRW 100,000,000
  premium = KRW 15,080/month (180,960 p.a.)   horizon = 240 months (20 years) to boheom nai 60   boundary = ceiling
  modules: acc_death = False   waiver = False   accel = False   reinstatement = False

    [ the t = 0..11 rows of result_cf(), eleven columns ]
... 228 further months to t = 239

undiscounted totals: premiums 2,964,413.29   claims 2,063,167.17   claim exp+expenses+commissions 792,436.18   net_cf +108,809.94

checks:
  check_decline_timing     True
  check_lapse_pool         True
  check_net_cf             True
  check_pols_payer         True
  check_pols_roll_fwd      True
  check_prem_level         True
  check_waiver_reset       True
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/term_life/Term_KR_S")
model.Projection[1].result_cf()      # the worked example's anchor cell
model.Projection[3].result_pols()    # the counts, the decrements and the renewal ladder
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a `DataFrame` indexed by the **0-based** policy **month** `t` —
`t = 0` is the first policy month, the frame runs `t = 0 … proj_len() - 1` with
`proj_len() = 12 × proj_years()`, and the contractual policy year of row `t` is the derived
label `policy_year(t) = t // 12 + 1` — one column per cash flow
line; `result_pols()` prints the counts, decrement rates, renewal index and premium beside
them, which is where a renewal boundary becomes legible — the row whose
`renewal_decline_rate` is non-zero and whose `prem_pp` changes on the next row.
`model.Projection.doc` carries the notes' symbols mapped to the cells names, and names the
age basis; `model.Data.doc` says what each input file is and, for the mortality table, what
it is **not**.

## The age basis is 보험나이, everywhere, with no shift

Every age in the model is **보험나이** (*boheom nai*, insurance age): 만나이 with fractions
of six months or more rounded up, incrementing on the **policy anniversary** and not on the
birthday [S2 제22조] [REG-R25 제21조](#krlib-reg-r25). The model point ages, the premium table and the
mortality table are all on that one basis, so `age(t) = x + t // 12` is exact rather than
approximate — 보험나이 steps on the 계약해당일, which on a monthly grid anchored at issue is
exactly twelve months apart — and **no age-basis shift is applied anywhere**, which is the
opposite of
`Term_JP_S`, whose 満年齢 model points read a 保険年齢 table and carry an optional
correction for it. The one place Korean practice uses 만나이 instead is the 상법 제732조
voidness test for a life under 만 15 [S2 제22조제1항 단서] [R4], which is an issue rule and
not a projection quantity.

`kr_registry.MODELS` records the basis and `test_model_conventions_kr.py` asserts that the
`Projection` docstring names it. A 만나이 model point read against this table would
understate the rate by about half a year of ageing on every row, silently: reading the
anchor cell a full year of ageing early — decrements and survivorship together — cuts total
death claims from ₩2,063,167.17 to ₩1,897,843.01, an 8.0% understatement that flatters
`net_cf` by more than the whole answer.

## The horizon is the renewal ceiling, not the term

On a **비갱신형** (*bi-gaengsinhyeong*, non-renewable) point `proj_years()` is
`policy_term()` and there is nothing more to say. On a **갱신형** point it is
`renew_ceiling() - age_at_entry()`, because the contract renews automatically and
negative-option until it reaches 보험나이 80 [S6], and the 보험기간 of the contract in
force is one **cycle**. A ten-year cycle issued at 40 is projected for forty years across
four separately priced cycles.

Three cells carry it. `term_index(t)` is the notes' `k`, the state variable a Korean
protection model needs: **the premium is a function of the renewal index and not of the
policy year**, so a model that indexes the premium by `t` cannot represent the product, and
one that carries a single level premium across a boundary silently converts a 갱신형 into a
비갱신형 at the wrong price — on model point 3, ₩2,195,589.29 of premium over forty years
instead of ₩11,517,624.04. `term_start_age(k)` is the attained 보험나이 the cycle is priced
at, and `term_len(k)` is `min(n, w_r - x_k)`, where truncation lives — 「갱신일부터 최종
갱신계약의 보험기간 종료일까지가 10년미만일 경우에는 … 이 계약의 보험기간으로 합니다」
[S6]. Truncation shortens the **cycle**, not the horizon; an issue age of 45 on a ten-year
cycle has a final cycle of five years — 60 months, over all of which the premium is level —
and still ends exactly at 보험나이 80, at `t = 419`.

`check_prem_level()` asserts that the premium is level inside every cycle and moves only at
a boundary. On model point 3 the ladder is the published one to the won:
₩9,000 → ₩21,000 → ₩56,000 → ₩201,000 a month [S6] [S7].

## Both contract-boundary readings are published, and the model does not rule

Nothing retrieved settles where a Korean term renewal's IFRS 17 boundary falls [REG-R60],
and the Korean facts pull both ways. The insurer may reprice the **entire** 기초율 at
renewal, 위험률 included, and says so in terms [S9] [S15]; the renewal is issued on a **new
product code** [S9] [S15]; and a waiver already running is extinguished [S6]. Against that,
the renewal is **guaranteed-issue** — no 고지, no underwriting, no health condition [S6]
[S9] [S15] — so the repricing is at portfolio level and cannot reflect the risks of the
*particular* policyholder, which is the test that keeps a renewal inside the boundary.

`contract_boundary` is therefore a model point column, `ceiling` in the base run and
`current_term` on model point 4. Model points 3 and 4 are the same cell on the two
readings and they differ by far more than a rounding: **+₩2,919,193.21** against
**−₩181,055.18** of undiscounted net cash flow. A model that can project to the ceiling can
always be truncated to one cycle; the reverse is not true, which is why the long reading is
the base.

The two are **not** the same projection truncated, and the model prints the reason rather
than hiding it. `pay_term_y = 0` means 전기납 and resolves to `proj_years()` — the horizon
in **years**, a 납입기간 being a contractual term and not a row count — so shortening the
horizon also compresses the 적용해지율 decay from forty years to ten: model point 3's first
120 `net_cf` rows sum to −₩172,034.54 against model point 4's −₩181,055.18. A reader
diffing the two should expect the gap, not treat it as a defect.

## Renewal decline is its own decrement

`renewal_decline_rate(t)` is non-zero **only** in a boundary month — the last month of a
cycle, `(t + 1) % (12 * n) == 0` with `t < proj_len() - 1` — and the exits it produces
are taken **after** mortality and **after** ordinary lapse, on the survivors of both. It is
also the one rate in the model that is **not** converted to a monthly equivalent: `q` and
`w` are forces acting through a period and are compounded down to the month, while the
decline is a discrete election on a single date and enters at its own 20% in the one month
the boundary falls in.

The ordering is not cosmetic: the policy roll-forward is order-invariant, so a model that
applies the decline first still balances and still books 20% fewer death claims in the
boundary month — ₩5,255.97 instead of ₩6,569.96 at `t = 119` on model point 3, with
`l(120) = 0.5805175782` either way. `check_decline_timing()` asserts that the rate is
non-zero in exactly the boundary months and nowhere else — including the last month, where
cover ends at the ceiling rather than renewing, and including every month of a 비갱신형 point
— which is the check that catches the decline being smuggled in as a lapse loading. At that
boundary row the decline is 0.1451293946 of 0.1463568040 total exits: **99.2% of everyone
who leaves in that month**, in a ratio of roughly 2,200 : 18 : 1. Folded into `w(t)` it
would be invisible — and the monthly grid is what makes how badly arithmetic rather than
rhetoric, an annual step having mixed the election with a whole year of continuous lapse
and reported it as 90.7% of a mixed population that is not mixed at all.

The rate is **[std] 20%** and is published nowhere in Korea for any product: the disclosure
requires the *price* path and not the *persistency* path [S7] [S16]. The three-way argument
for the level is in `technical-notes.md` and in the cells docstring; the arguable range is
roughly 5% to 40%, and `renewal_decline_max = 0.40` is the top of it. `renewal_decline_beta`
switches on the elasticity `d = min(d_max, d_0 (P_a(k+1)/P_a(k))^beta)`, which responds to a
premium jump that is 2.33x at the first renewal and 3.59x at the third [S7].

## One decrement, one benefit — and the waiver Korea has instead

A Korean term policy pays the 보험가입금액 on death and nothing else, and payment
terminates the contract immediately [S2 제4조·제23조]. There is **no Korean analogue of the
Japanese 高度障害保険金**, so unlike `Term_JP_S` there is no competing benefit on one sum
assured and nothing to double-count. What the 장해 (*janghae*, disability) state does
instead is **switch the premium off**: 보험료 납입면제 on a 장해지급률 summing to **50% or
more** from any cause, in the 주계약 at no separate premium, in identical words at eight
carriers [S1] [S2 제5조] [S6] [S8] [S9] [S10] [S11] [S12].

Two Korean rules make the waived state a real state rather than a cash-flow adjustment, and
both are implemented:

- **It does not survive a renewal.** 「다만, 새로이 갱신되는 계약에서는 갱신 전 보험료
  납입면제 사유로 인한 보험료 납입면제를 적용하지 않고, 보험료를 계속 납입하여야
  합니다」 [S6]. `wop_waived_frac(t)` resets to zero in the first **month** of every cycle
  and `check_waiver_reset()` asserts it. Model points 3 and 4 are where it bites: the waived
  fraction reaches 0.0079050974 at `t = 119` and is exactly 0.0 at `t = 120`. The incidence
  behind it is stated annually and converted by `1 − (1 − wop_inc_rate)^(1/12)`: it is a
  probability over the year, so the monthly equivalent sits slightly above a twelfth of it
  and dividing by twelve would understate the waived population.
- **On the 만기환급형 the maturity benefit is computed as if the waived premiums had been
  paid** [S1] [S12], so `cum_prem_pp(t)` sums the *scheduled* premium and
  `wop_waived_frac` does not enter it.

The trigger is **cause-neutral** — sickness qualifies equally with accident, 「동일한 재해
또는 재해이외의 동일한 원인」 [S2 제5조제1항] — so `wop_inc_rate` is a general disability
incidence and is deliberately **not** scaled off `mort_rate()`. No Korean document publishes
a 50%-plus 장해 incidence and the 참조순보험요율 behind it is not public [REG-R4] [R19], so
it is an arbitrary placeholder and the module is off on eight of the ten shipped points.

## `claims_lapse` is a column of zeros, deliberately

On the representative 전기납 무해지 contract the 약관 pays **nothing at any duration**:
「보험료 납입기간이 보험기간과 동일한 계약 … 의 경우에는 보험기간 중 계약이 해지될 경우
해약환급금을 지급하지 않습니다」 [S2 제33조제2항], and 한화생명's published 해약환급금
예시 for the same shape prints 환급률 0.0% at all eleven durations for both sexes [S1]. So
an ordinary lapse is a pure decrement: it moves `pols_if` and pays nothing. The column is
published rather than dropped because the 표준형 comparator *does* have a value, reaching
46% of premiums paid by duration six [S10], and a reader must not infer nil from the product
class the way a `uklib` reader could.

**What the model deliberately does not compute** is the value that arises on a
*shortened-pay* 무해지 contract after 납입완료 — 50% of the 표준형's surrender value [S1]
[S2 제33조제2항] [S12]. The 표준형 해약환급금 is the 순보험료식 계약자적립액 less the
해약공제액, which is the savings chassis's quantity and belongs to `WholeLife_KR_S`;
projecting it here would duplicate that machinery in the one product that exists to
demonstrate the decrement recursion without it. Model point 5 (20년만기 10년납) exercises
what this chassis *does* carry at 납입완료: the 적용해지율 reaching its 0.1% convergence
point in policy year 10, the last paying year, and then stepping to the 0.8% ultimate from
`t = 120`, and the premium ceasing at the same month.

For the same reason the **표준해약공제액** of 별표 14 is not computed. It caps a surrender
charge, and this product has no surrender value for it to cap; at the anchor its
sum-assured limb alone is ₩100,000,000 × 10/1000 = ₩1,000,000, which is 5.5 years' gross
premium against a modelled month-0 acquisition charge of ₩228,576, so it is very far from
binding in any case [REG-R20] [R9]. The constraint that actually shapes a Korean term
surrender value is 제7-66조제1항제2호's **해약공제기간, capped at seven years** [REG-R19].

There is likewise **no 보험계약대출 and no 자동대출납입 in fact**. Both are granted by the
약관 [S2 제26조·제34조] and both are inoperative, there being nothing to lend against — a
point the supervisor made of the 무해지 form generally [REG-R28]. 납입최고 (14일), then
실효, then 부활-or-not is the whole persistency machinery here, which is part of why this is
the right chassis to specify first.

## The premium chassis is mostly sourced

```text
P_m(k) = round_10( r(form, sex, x_k, m_k) * c_p(class, sex) * g(k) * SA / 100,000,000 )
x_k    = x + (k - 1) * n
m_k    = min(n, w_r - x_k)
P_a(k) = 12 * P_m(k)
```

The rounding to the nearest ₩10 happens **before** annualization, which is the granularity
the anchor carrier quotes [S12]; rounding after, or not at all, breaks the reproduction of
₩15,080 / ₩180,960 at the anchor and of ₩9,000 / ₩108,000 on the 갱신형 point, and those
are figures three independent documents agree on [S12] [S4] [S6] [S7].

Twenty cells are published and read directly: the anchor carrier's 20-year grid at ages 30,
40 and 50 for both sexes and both maturity forms [S12], and the 갱신형 ladder at ages 40,
50, 60 and 70 on a ten-year cycle [S6] [S7]. Unpublished cells use the **[std]** extension
off the `is_anchor` row of the matching form and sex,
`r = r_anchor * qbar(x, m) / qbar(x_a, m_a)`, built on the **table** rate rather than on
`mort_rate()`: a premium scale is not a best-estimate quantity, and feeding the
best-estimate rate in would cancel on a 표준체 point and fail silently on a preferred one,
which is the worst kind of error.

**No flat policy element can be separated out.** Unlike `jplib`'s オリックス生命 grid, from
which a ¥248 monthly policy element decomposes exactly because the card varies the sum
assured, **every Korean grid retrieved fixes the sum assured** and varies age, sex, rate
class or product form instead [S1] [S8] [S11] [S12] [S14]. The office premium is therefore
proportional in the sum assured and the approximation is recorded rather than hidden. One
consequence is visible in the output: model point 2, the female anchor twin, runs a negative
undiscounted net cash flow where the male anchor runs a positive one, because the same flat
per-policy expense is charged against a premium 47% smaller. That is the same effect the
market shows — female premiums run at 52–56% of male across the six direct writers on the
same cell and from 47% to 90% across the face-to-face and simplified-issue rows [S4].

`g(k)`, the shortened-pay uplift, is **[std]**: `ä(m_k) / ä(m_k^p)` at the 적용이율 of
2.50% [S1] [S12], 1.781198 on model point 5 (20년만기 10년납) and 1.484695 on model point 9.
No Korean document retrieved publishes a shortened-pay premium for a term contract at all,
so an equivalence had to be chosen; a certain annuity rather than a life annuity overstates
the uplift by the mortality that would have been shed, and nothing published sizes the
overstatement.

The **10-year rows and the 20-year rows are different carriers**, and the model never mixes
them: the shipped 갱신형 points reach published cells only, and the extension runs off the
20-year anchor. That the two carriers are at the same level is checkable — 흥국생명's
비갱신형 20-year premium on the disclosure basis is ₩15,000 against the anchor's ₩15,080
[S4].

## Modules that are off in the base run

Five model point columns and two References. Each module is live on at least one shipped
point, so the machinery is exercised rather than merely present.

| Module | Column | On at | What it demonstrates |
|---|---|---|---|
| 보험료 납입면제 | `waiver` | 3, 4 | the waiver **not** surviving a 갱신 [S6] |
| 선지급서비스특약 | `accel` | 7, 9 | the cap not binding (7) and binding (9) [S2 제4조] |
| 부활 | `reinstatement` | 8 | the three-year window and its vintage ledger [S2 제28조] |
| 재해사망 uplift | `acc_death` | 10 | 2x the sum assured on 재해사망, as a decrement split [S6] [S10] |
| Contract boundary | `contract_boundary` | 4 | the short reading against point 3's long one |

`renewal_decline_beta = 0` and `comm_new_term_rate = 0` are the two References. The second
is worth naming: a Korean renewal is issued on a **new product code** [S9] [S15], which is
an argument that acquisition commission *should* fall at each boundary; setting it to 0.60
turns `t = 120` of the 갱신형 anchor from +₩4,689.19 to −₩83,085.07 — a single-month cliff
of the same shape as the acquisition commission at issue — and the forty-year total from
+₩2,919,193.21 to +₩2,238,679.76.

At the anchor's ₩100,000,000 of cover the acceleration cap is **exactly reached and reduces
nothing**: `A = min(0.5 × SA, ₩50,000,000)` gives ₩50,000,000 = `accel_cap`, so
`accel_cap_binds()` is a **strict** inequality and returns `False` there. A model reporting
it as binding has a strict-versus-weak error or has read the clause as per-contract rather
than per-insured [S2 제4조]. Model point 9, at ₩200,000,000 of cover, is where it genuinely
binds. The accelerated amount comes **out of** the death benefit, never beside it:
`claims_death` carries `(1 − a(t))` and `claims_accel` carries `a(t)`.

## Inputs are external files

Five CSVs in `products/term_life/`, beside `run.py`, read at run time. The model folder
holds `__init__.py` and `_system.json` and its two Space folders, and nothing else — no
`_data/`, no IOSpec, no embedded values — so a diff of the model shows logic changes only.
This is the `annuallife.TradLife_A` layout; contrast `basiclife.BasicTerm_S`, which keeps
its inputs inside the model. The consequence worth knowing: **the model is not portable on
its own.** Copying `Term_KR_S` without its parent's CSVs produces a model that reads and
then fails on first evaluation.

| File | Reference | Reader | Contents |
|---|---|---|---|
| `model_point_table.csv` | `model_point_file` | `Data.model_point_table()` | ten model points, indexed by `point_id` |
| `mort_table.csv` | `mort_table_file` | `Data.mort_table()` | 예정 경험사망률 and 예정 재해사망률 by sex and 보험나이 19–120 |
| `rate_class_table.csv` | `rate_class_file` | `Data.rate_class_table()` | four classes x two sexes, mortality and premium relativities |
| `prem_rate_table.csv` | `prem_rate_file` | `Data.prem_rate_table()` | twenty published premium cells per ₩100,000,000 |
| `lapse_table.csv` | `lapse_table_file` | `Data.lapse_table()` | the three disclosed 적용해지율 endpoints |

**No input file is keyed by the time index**, so the move to the 0-based `t` changed no CSV
value in this product. Column by column: `lapse_table.csv` is keyed by `segment` and holds
three scalar endpoints, the time dependence being computed in `lapse_rate(t)` rather than
tabulated; `mort_table.csv` is keyed by `(sex, age)`, an attained 보험나이 that the model
reaches through `age(t) = x + t`, never by `t`; `prem_rate_table.csv` is keyed by
`(form, sex, issue_age, term_y)`, where `issue_age` is an age and `term_y` a contract
**length**, not an index; `rate_class_table.csv` is keyed by `(rate_class, sex)` and carries
no time at all; and `model_point_table.csv` is keyed by `point_id`, its `term_y`,
`expiry_age`, `pay_term_y` and `renew_ceiling` columns being lengths and ages rather than
points on the frame, with no `duration_init` or other elapsed-time column — every shipped
model point is new business projected from issue, so every frame opens at `t = 0`.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate
ItemSpace with its own cells cache; readers placed there would re-read every file for every
policy. They live in the unparameterized `Data` Space instead, and
`test_inputs_are_read_once_not_once_per_model_point` asserts the property against the file
set registered in `kr_registry.INPUT_FILES`. `Data.prem_anchor_table()` is derived from
`prem_rate_table()` rather than read from a sixth file, so it costs no extra read.
`input_dir()` returns `_model.path.parent`, resolved at run time and never hard-coded.

**Every assumption CSV carries a `provenance` column and every cell in it begins with a
citation tag.** `model_point_table.csv` is the only exemption, a model point being a
configuration rather than an assumption.

### `mort_table.csv` is a construction, and there was no alternative

The industry table is the **경험생명표** (*gyeongheom saengmyeongpyo*), prepared by
보험개발원; the current edition is the 제10회, applied to new business from April 2024. **It
is not published.** What is released is the summary — 평균수명 남 86.3 / 여 90.7 and 65세
기대여명 남 23.7 / 여 27.1 — and not the rates [REG-R33] [REG-R34], and even those four
numbers reach this library through a **trade newspaper** rather than through 보험개발원,
whose own announcement was not retrievable. The 참조순보험요율
behind each carrier's own basis is not public either for mortality [REG-R4] [R19] [R20].
This is the sharpest contrast in this repository with `jplib`, whose 標準生命表2018 is a
free public PDF with `qx` by single year of age; and it is why the carriers' own 예정
경험사망률 disagree by a factor of **1.77 at male 40** — 0.000480 to 0.000850 across seven
carriers [S1] [S6] [S8] [S10] [S11] [S12] [S17] — where every Japanese carrier prices off
one table.

The file is built from the two things that *are* public and is **[std]** throughout:

1. A **Makeham law** `q(x) = A + B c^x` fitted *exactly* to the anchor carrier's three
   disclosed 예정 경험사망률 — male 0.000280 / 0.000650 / 0.003390 and female 0.000200 /
   0.000430 / 0.001390 at ages 20 / 40 / 60 [S12]. Three anchors, three parameters, so it
   is an interpolation and not a regression, and the shipped rows at those ages are the
   disclosed rates to the digit.
2. Above age 60 the fitted law is tilted by `k^(x - 60)`, one free parameter per sex, solved
   so that the **complete expectation of life at 65 on the shipped table is exactly the
   published 경험생명표 figure** — 23.7 years male and 27.1 female [REG-R33]. The solved
   tilts are k = 1.0098862619 (male) and k = 1.0592847691 (female), so the correction is
   small and upward: an unconstrained extrapolation of three disclosed rates leaves slightly
   too much life at 65.
3. The result sits **4.2 years (male) and 3.4 years (female) above** the public 완전생명표's
   own 65세 기대여명 of 19.5 and 23.7 [REG-R38]. That gap is underwriting
   selection, and a constructed Korean table that does not reproduce it is not an
   insured-lives table. Reproducing it is the one external check available, and it is why
   the file runs to age 120 rather than stopping at the highest age the model points reach:
   step 2 can then be checked from the shipped file rather than taken on trust.

The shipped `mort_rate` is a **pricing** rate — a carrier's 예정 경험사망률 carries a margin
over experience that no public document sizes, the 산출방법서 being a 기초서류 filed with
the FSC and never published [REG-R2], with the 선임계리사 standing behind it and behind the
reserving [REG-R5] — so `Projection.mort_be_factor` removes it.
It is also the **표준체** rate; `rate_class_table.csv` scales it. `acc_mort_rate` is the
예정 재해사망률 of a *different* carrier [S6]; pairing the two is defensible where pairing
two all-cause tables would not be, because the two carriers publishing accidental rates
agree to three significant figures at age 20 and to within 10% everywhere [S6] [S10], while
the all-cause rates differ by a factor of 1.77 at male 40.

### The other three assumption tables

- **`rate_class_table.csv` is sourced, which no other library here can say.** Two carriers
  publish a full 예정 경험사망률 table per rate class [S11] [S12]; the shipped file carries
  the anchor carrier's `mort_ratio` and `prem_ratio` at male and female 40 [S12]. The
  premium ratio exceeds the mortality ratio in the three male classes and in the female
  비흡연자, as a loading that does not scale with the risk implies, and falls marginally
  below it at 건강체 여 (0.890 against 0.907) and 슈퍼건강체 여 (0.846 against 0.856),
  which nothing retrieved explains. Holding the ratios flat across ages is the **[std]**
  step.
- **`prem_rate_table.csv` is twenty published cells and one flag.** `is_anchor` marks the
  `(pure, M/F, 40, 20)` rows the [std] extension runs off — the cell that is doubly
  prescribed in Korea, being both the 감독규정 기준연령 요건 [REG-R9] and the disclosure's
  대표계약 [S5], and therefore the one cell where a Korean premium can be read off two
  independent documents [S12] [S4].
- **`lapse_table.csv` ships three rows, not a curve, because that is what Korea
  discloses.** The **shape** is supervisory — the 2024 IFRS17 계리가정 가이드라인 makes a
  로그-선형 model converging to 0.1% the 원칙모형 for 무·저해지 business and sets the
  post-완납 ultimate at 0.8% [REG-R27] — and the **endpoints** are disclosed in the
  상품요약서 [S12] [S1]. This is the one assumption in this product whose chain from
  supervisory guideline to disclosed pricing parameter is complete. The **[std]** step
  inside `lapse_be_factor = 1.0` is that the endpoints are disclosed on a 10년납 basis and
  are stretched over each point's own 납입기간; model point 5 is the only shipped point
  that reproduces the disclosed shape at its disclosed length, and it and model point 9 —
  a 35-year term bought 20년납 — are the only two whose 납입기간 ends before their cover
  does and therefore the only two that reach the `post_payment` row at all.

## Sign convention

`net_cf` is **income positive** — premiums less claims, claim expense, expenses and
commission — which is the library-wide sign, so there is no outgo-positive `liability_cf`
companion. Premiums are **monthly** in advance, claims fall at the end of the month of
death, and the decrements act inside the month they belong to. The annual grid this model
was first written on carried a matched pair of offsetting distortions — a whole year's
premium collected from lives that died or lapsed during the year, worth 1.136% of a year's
premium at the 적용이율, against a death benefit paid a year late — and the monthly step
removes both rather than netting them, so no half-year adjustment belongs on top of this
grid. The residual timing error is half a month either way.

`P_a = 12 × P_m` survives as a **report**, not as a cash flow convention. The policyholder
does pay twelve monthly premiums a year and no mode discount is published [S12], so the
annualized amount is exact; it is carried because the commission scale is written on an
annualized premium and because a reader comparing this model against a Korean disclosure
needs the annual figure.

The model projects **undiscounted gross best-estimate liability cash flows** and nothing
else. The 책임준비금 [REG-R3] [REG-R10] [REG-R23], the 해약환급금준비금 [REG-R11], the
IFRS 17 CSM and risk adjustment [REG-R60] and the K-ICS 요구자본 [REG-R13] [REG-R30] are
cited and left to a layer that consumes the cash flows. One consequence to expect: model
point 6, the 만기환급형, returns a negative undiscounted net cash flow, because a contract
that hands back 100% of premiums at maturity is financed out of investment income this
model does not project.

## Naming

`lower_snake_case` throughout, reusing lifelib's `basiclife.BasicTerm_S` vocabulary where
there is an analogue: `pols_*` for policy counts, plural nouns for cash flows, `*_rate` for
rates, `*_pp` for per-policy amounts, `claims(t, kind)` with an uppercase `kind` string,
`pols_if_at(t, timing)` for the within-month in-force reads.

### The notes' symbols, and where they live

`model.Projection.doc` carries the full table; the load-bearing rows are these.

| Notes symbol | Cells | Meaning |
|---|---|---|
| `t` | the index of `result_cf()` | policy **month** index, **0-based** |
| `y(t)` | `policy_year(t)` | policy year label, `t // 12 + 1`; derived, never indexed by |
| `x` | `age_at_entry()` | 가입나이, on 보험나이 |
| `x + ⌊t/12⌋` | `age(t)` | attained 보험나이 in month `t` |
| `n`, `n_p` | `policy_term()`, `pay_term()` | 보험기간, 납입기간 |
| `w_r` | `renew_ceiling()` | ceiling age |
| (horizon) | `horizon_ceiling()` | years from entry to the ceiling |
| `N_y` | `proj_years()` | horizon in policy **years**; what 전기납 resolves against |
| `N` | `proj_len()` | number of projected **months**, `12 N_y` (exclusive end); the frame is `t = 0..N−1` |
| `k` | `term_index(t)` | renewal index, 1-based, 1 in the first cycle |
| `x_k`, `m_k`, `m_k^p` | `term_start_age(k)`, `term_len(k)`, `term_pay_years(k)` | cycle start age, length, paying years |
| `SA`, `i_p`, `g` | `sum_assured()`, `prem_int_rate`, `pay_factor(k)` | cover, 적용이율, shortened-pay uplift |
| `r(sex, x, m)`, `qbar(x, m)` | `prem_rate_mth(t)`, `mort_table_mean(x, m)` | rate per ₩100,000,000, mean **table** rate |
| `P_m(k)`, `P_a(k)` | `premium_mth_pp(t)`, `prem_pp(t)` | monthly and annualized office premium |
| `q(t)`, `q^m(t)` | `mort_rate(t)`, `mort_rate_mth(t)` | **annual** death rate at `age(t)`, and the monthly decrement `1 − (1 − q)^(1/12)` |
| `a_q(t)` | `acc_mort_share(t)` | accidental share of `q(t)`, a ratio of annual table rates |
| `w(t)`, `w^m(t)` | `lapse_rate(t)`, `lapse_rate_mth(t)` | **annual** ordinary lapse rate, and the monthly decrement |
| `d(t)`, `d_0` | `renewal_decline_rate(t)`, `renewal_decline_base` | renewal decline — **not** converted, an election on a date |
| `l(t)`, `D(t)` | `pols_if(t)`, `pols_death(t)` | in force at time `t`, `l(0) = 1`; expected deaths |
| `lap(t)`, `rho` | `pols_lapse_pool(t)`, `reinstate_rate` | reinstatable stock, 부활 rate |
| `u(t)` | `wop_waived_frac(t)` | fraction premium-waived |
| `A`, `a(t)`, `i_s` | `accel_amount()`, `accel_share(t)`, `accel_disc_rate` | 선지급 amount, take-up, 평균공시이율 |
| `CF(t)` | `net_cf(t)` | net cash flow, income positive |

Four of them needed care and the reasons are in the `Projection` docstring: `d(t)` is a
different event at a different time from a different population than `w(t)`; `qbar` averages
`mort_rate_at_age`, unadjusted, and is not `mort_rate`; `P_m(k)` is indexed by the cycle in
the notes and by `t` here, with `term_index` resolving between them; and `lap(t)` is a
**stock** where `pols_lapse` is the period's **flow** into it.

### Three names settled in krlib's cross-model review

Recorded in `RETIRED_NAMES` so no krlib model reintroduces them:

- `renewal_decline_rate`, not `renew_rate` — the proportion who decline a 갱신 is a
  decrement, and `renew_rate` reads as its complement. `Medical_KR_S` uses the same name for
  the same event on a one-year cycle.
- `prem_int_rate`, not `yejeong_rate` — the 적용이율 is the *pricing* interest rate and must
  not share a name with a declared crediting rate (공시이율), which this product does not
  have at all but `WholeLife_KR_S` does.
- `pols_maturity`, not `pols_expiry` — the count whose cover ends at the scheduled end of
  the contract, whether or not anything is paid for it. On the 순수보장형 anchor,
  `pols_maturity(239) = 0.7582424843` and `claims_maturity(239) = 0.00` — the same count the
  annual grid produced, to the last bit.

## The identity `check_net_cf()` closes

`net_cf(t)` = `premiums` − `claims_death` − `claims_acc_death` − `claims_accel` −
`claims_maturity` − `claims_lapse` − `claim_expenses` − `expenses` − `commissions`, read
back out of the published `result_cf()` columns so that a reader adding up the printed
statement gets the printed total.

Reading it back out of the frame rather than recomputing it is the point: it is the check
that catches a benefit kind that exists in `claims(t, kind)` but was never given a column,
which would leave the statement silently short of outgo the model is charging. It is also
why `result_cf()` publishes the five `claims_*` split columns and no aggregate `claims`
column — an aggregate beside the splits would double-count the whole benefit outgo.

The other six checks are `check_pols_roll_fwd` (the roll-forward, with the 부활 inflow as
its own term), `check_lapse_pool` (the pool's one inflow and two outflows),
`check_pols_payer` (payers and waived lives partition the in-force), `check_prem_level`,
`check_decline_timing` and `check_waiver_reset`. All seven take no argument, return a real
`bool`, and are `True` on every one of the ten shipped model points. Five close to
`roll_fwd_tol = 1e-12`, an identity between cells evaluated in one expression;
`check_decline_timing` compares a boolean against a boundary test and takes no tolerance at
all; and `check_net_cf` closes to a separately named `cash_tol = 1e-6`, because it re-reads
won amounts of order 1e7 back out of a `DataFrame` and the round trip through column
construction leaves float64 rounding in absolute won. `cash_tol` is far below one won, the
smallest error a reader adding up the printed statement could see.

## Standardizations used

Every row is **[std]**. The sourced contractual and pricing parameters are in
[`product-spec.md`](product-spec.md) and [`technical-notes.md`](technical-notes.md) and are
not repeated. "Observed range" is what the retrieved documents actually bound, and several
of them bound nothing at all — which is said rather than papered over.

| Parameter | Value | Rationale | Observed range |
|---|---|---|---|
| `mort_be_factor` | 0.85 | removes the unpublished margin in a 예정 경험사망률; the 산출방법서 that would size it is a 기초서류 never published [REG-R2] | none for the margin itself; seven carriers' 예정 경험사망률 at male 40 span 0.000480–0.000850 around the anchor's 0.000650, so the cheapest market basis is 0.74x before any margin is removed [S1] [S6] [S8] [S10] [S11] [S12] [S17] |
| mortality construction | Makeham `A + B c^x` fitted exactly to three anchors, tilted by `k^(x−60)` above 60 | the 제10회 경험생명표 is not published; the fit reproduces the three disclosed rates and the published 65세 기대여명 exactly [REG-R33] [REG-R34] | check: the shipped table sits 4.2 / 3.4 years above the public 완전생명표 at 65 [REG-R38], which is the selection gap it must show; the single-year `qx` tables behind that table are distributed through KOSIS and were not fetchable [REG-R39] |
| mortality improvement | none | two years since the 제10회 table's April 2024 application are not projected; part of `mort_be_factor` stands in for it | none published |
| `class_mort_ratio`, `class_prem_ratio` | held flat across ages | the disclosures are at three ages and the ratios move little between them | 표준체 1.000; 비흡연자 0.828 / 건강체 0.723 / 슈퍼건강체 0.583 on mortality at male 40 [S11] [S12] |
| `acc_mort_rate` pairing | [S6] accidental rates against [S12] all-cause | the two carriers publishing accidental rates agree to three significant figures at age 20 and within 10% everywhere [S6] [S10] | resulting share of all-cause: 34.6% at male 20, 16.9% at 40, 10.5% at 60 |
| `lapse_be_factor` | 1.0 | the best estimate is set equal to the disclosed 적용해지율; nothing retrieved discloses a best-estimate term lapse rate | the one Korean experience datum is whole-life and points one way: 37회차 유지율 50.2% against an assumed 71.5% [R18] |
| 적용해지율 stretch | disclosed 10년납 endpoints applied over each point's own 납입기간 | the composite is 전기납 over twenty years and the disclosure is on ten | upper endpoint varies 4.6% [S12] to 8.4% [S1]; the 0.1% convergence and 0.8% ultimate do not vary and are prescribed [REG-R27] |
| `renewal_decline_base` | 0.20 | argued, not chosen: bounded above by the FSS's floor of at least 30% additional lapse at a discrete contractual event that hands the policyholder cash [REG-R27], below by the negative option and the 15일 notice [S9] [S15] | nothing published for any Korean product; arguable 5%–40%, over which the 갱신형 anchor's total runs +₩4,789,398.01 to +₩1,258,323.02 |
| `renewal_decline_beta`, `_max` | 0.0, 0.40 | elasticity module off in the base run; the cap sits at the top of the arguable range | as above |
| `expense_acq`, `expense_maint`, `inflation_rate` | ₩120,000 at `t = 0`, ₩2,000 per **month** (₩24,000 p.a.), 2.0% a year stepping at the 계약해당일 | no Korean carrier publishes any expense rate at all [S1] [S6] [S8] [S10] [S11] [S12] | 보험가격지수 dispersion 51.6%–239.1% across the 45 disclosed products [S4]; the sum-assured limb of the 별표 14 cap alone is ₩1,000,000 at the anchor, 5.5 years' gross premium, so the cap is nowhere near binding [REG-R20] [R9] |
| `expense_claim` | ₩300,000 per death claim | round, and immaterial at these claim levels | none published |
| `comm_init_rate`, `comm_renewal_rate` | 0.60, 0.03 | no commission scale is disclosed anywhere in the set, and the nearest public handle — the 2019 rule of thumb sizing the 표준해약공제액 at 13 months' premium for a 보장성보험 [REG-R29] — is calibrated on a premium-to-cover ratio nothing like a term policy's and does not transfer | none published |
| `comm_new_term_rate` | 0.0 | a 갱신 is issued on a new product code [S9] [S15], which argues for paying again; it takes no 고지, which argues against; the base run pays nothing and exposes the switch | none published; at 0.60 the forty-year total falls to +₩2,238,679.76 |
| `prem_int_rate` used as the shortened-pay discount rate | 0.025 | the 적용이율 itself is sourced [S1] [S12]; using it to discount `pay_factor` is the standardization | 적용이율 across the set: 2.00%–2.75% [S6] [S8] [S12] [S17] |
| `pay_factor(k)` | `ä(m_k) / ä(m_k^p)`, annuity **certain** | no Korean document retrieved publishes a shortened-pay term premium at all | 1.781198 at 20년만기 10년납, 1.484695 on model point 9; overstates by the shed mortality, unmeasurably |
| premium extension | `r_anchor × qbar(x, m) / qbar(x_a, m_a)` off the `is_anchor` row | the published grid is three ages × two sexes × two forms; everything else must be extended, and a premium scale is not a best-estimate quantity | published cells reproduce exactly; 흥국생명's 20-year cell is ₩15,000 against the anchor's ₩15,080 on the same basis [S4] |
| monthly decrement conversion | `q^m = 1 − (1 − q)^(1/12)`, and the same for `w` | the sourced rates are **annual probabilities**, so the monthly equivalent is the uniform-force conversion and not a twelfth; twelve of them compound back to the annual rate exactly, which is what leaves the anniversary in-force unmoved | exact by construction; `LTC_KR_S` divides instead, its transition intensities being rates per year rather than probabilities |
| `P_a = 12 P_m` | rounded to ₩10 before annualizing; a report, not a cash flow | twelve monthly premiums are actually paid and no mode discount is published, so the amount is exact; the month's income is `P_m` itself [S12] | none needed |
| `accel_take_up` | 0.10 | **arbitrary placeholder**; module off in the base run | none published, and nothing bounds it |
| `wop_inc_rate`, `wop_rec_rate` | 0.0008, 0.0 | **arbitrary placeholder**, deliberately *not* scaled off `mort_rate()`, the trigger being cause-neutral [S2 제5조제1항] | none published; the 참조순보험요율 behind it is not public [REG-R4] [R19] |
| `reinstate_rate` | 0.10 a year, converted to the month | **arbitrary placeholder**; `reinstate_window = 36` months beside it is the **sourced** three years [S2 제28조], carried in months so the window closes on the month it closes on | none published |
| decrement order | death, then ordinary lapse, then renewal decline | the decline is a discrete event on the survivors of the month; reversing it books 20% fewer death claims in the boundary month and still balances | fixed by the contract's own sequence, not by a disclosure |
| `roll_fwd_tol`, `cash_tol` | 1e-12, 1e-6 | one closes an identity between cells in one expression; the other re-reads won amounts of order 1e7 out of a `DataFrame` | both far below one won |

**Three of these are arbitrary placeholders, and are labelled as such rather than dressed up
as estimates**: `accel_take_up`, `wop_inc_rate` and `reinstate_rate`. No retrieved document
gives an acceleration take-up, a 50%-plus 장해 incidence or a reinstatement rate for any
Korean carrier; no observed range can be quoted for any of the three; and nothing in the
sources bounds them. Two are deliberately round so that no reader mistakes them for
measurements. The only defence any of the three has is the switch: **the module each one
drives is off in the base run**, so the worked example and every headline figure this model
publishes are independent of all three. Replace all three before reading anything off model
points 7, 8 and 9.

**`renewal_decline_base = 0.20` is not in that list**, and the distinction matters. It is
also unpublished, but it is *argued* rather than chosen, it is live on model points 3 and 4,
which are the points the renewal machinery exists for, and the technical notes carry it with
an explicit sensitivity rather than as a point estimate.

## Tests

`tests/test_term_life_kr.py` asserts the notes' worked example **hard-coded**, so a reviewer
can check it by eye rather than by re-running the model:

- The anchor cell's premium chassis — `prem_rate_mth(0) = 15,080`, `premium_mth_pp(0) =
  15,080`, `prem_pp(t) = 180,960` level at every `t` — against the two documents that publish
  it [S12] [S4].
- The decrement basis policy year by policy year: the **annual** `mort_rate(t)` and
  `lapse_rate(t)` the sources publish, the monthly `mort_rate_mth(t)` and
  `lapse_rate_mth(t)` the roll-forward applies, and `pols_if(t)` to the ten decimals the
  notes print — including `pols_if(12) = 0.953472915` exactly, which is the annual-grid
  model's own `pols_if(1)`, and `pols_if(239) = 0.7584718208001523`, with
  `pols_if(240) = 0.0` one step past the frame.
- That the monthly decrements compound back to the annual ones, in both directions:
  `1 − (1 − q^m)^12 = q` term by term, and `pols_if` at every 계약해당일 reproducing the
  annual grid's in-force to the last bit. That is the check that the change of grid re-timed
  the exposure and left the survivorship the sourced annual rates imply.
- The first policy year's cash flow statement, `t = 0 … 12`, and the milestone rows at
  `t = 12 / 60 / 120 / 180 / 239`, to the won — and the four columns that are `0.00` in
  every row — `claims_acc_death`, `claims_accel`, `claims_maturity`, `claims_lapse` —
  asserted as zeros rather than left implied.
- The undiscounted totals: ₩2,964,413.29 of premium, ₩2,063,167.17 of death claims and
  **+₩108,809.94** of net cash flow, with the cohort decomposition 0.0206316717 deaths +
  0.2211258440 lapses + 0.7582424843 maturities summing to 1.
- The 갱신형 panel: the published ladder ₩9,000 → ₩21,000 → ₩56,000 → ₩201,000 [S6] [S7]
  held level for all 120 months of each cycle, the boundary rows at
  `t = 108 / 119 / 120 / 239 / 240 / 359 / 360 / 479`, `wop_waived_frac` exactly 0.0 at
  `t = 0, 120, 240, 360` and 0.0079050974 at each cycle end, and the two boundary readings
  **+₩2,919,193.21** against **−₩181,055.18** — together with the fact that model point 3's
  first 120 rows sum to −₩172,034.54 and therefore do *not* equal model point 4.
- The other eight model points' `proj_len`, `proj_years`, `premium_mth_pp(0)`, premium,
  claims and net cash flow totals, as the notes tabulate them.
- The three sensitivities the notes quantify: `mort_be_factor` at 0.75 / 0.85 / 1.00
  (+₩352,224.81 / +₩108,809.94 / −₩255,045.47), `renewal_decline_base` at 0 / 5 / 20 / 40%
  on the 갱신형 anchor, and `lapse_be_factor` at 0.5 / 1.0 / 2.0 — the last of which the
  monthly grid widens to a ₩11,000 range from the annual grid's ₩3,000, because an annual
  step credited the insurer with premium from policies that had already lapsed.

Each of the notes' pitfalls earns a test named after it — that 재해사망 is a split of the
death decrement and never a second one, that truncation shortens the cycle and not the
horizon, that a 비갱신형 point has `renewal_decline_rate(t) = 0` at every `t`, that the
waiver resets at a 갱신 while the suicide and contestability clocks do not, that `qbar` is a
mean of table rates, that the premium rounds to ₩10 *before* annualization, that the 선지급
cap is exactly reached at the anchor and does **not** bind, and that reading the anchor at
만나이 instead of 보험나이 cuts death claims by 8.0%. The optional modules are asserted in
**both** positions of their switch.

`tests/test_model_conventions_kr.py` adds the house style, parametrized over
`kr_registry.MODELS` rather than restated here: the two-Space layout, the external inputs
with no orphan CSV, the `provenance` column on every assumption CSV, the docstrings and
their required phrases, the `result_cf()` contract — indexed by the 0-based `t`, the index
being exactly `range(0, proj_len())` so the last row is `proj_len() - 1` and the frame has
`proj_len()` rows, first column `pols_if` opening at `pols_if_init()`,
a `net_cf` column, all names `lower_snake_case`, no NaN — and
that every `check_*()` returns `True` on **every** shipped model point.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R18]: #krlib-term_life-r18
[R19]: #krlib-term_life-r19
[R20]: #krlib-term_life-r20
[R4]: #krlib-term_life-r4
[R9]: #krlib-term_life-r9
[REG-R10]: #krlib-reg-r10
[REG-R11]: #krlib-reg-r11
[REG-R13]: #krlib-reg-r13
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R23]: #krlib-reg-r23
[REG-R27]: #krlib-reg-r27
[REG-R28]: #krlib-reg-r28
[REG-R29]: #krlib-reg-r29
[REG-R3]: #krlib-reg-r3
[REG-R30]: #krlib-reg-r30
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R38]: #krlib-reg-r38
[REG-R39]: #krlib-reg-r39
[REG-R4]: #krlib-reg-r4
[REG-R5]: #krlib-reg-r5
[REG-R60]: #krlib-reg-r60
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
<!-- END generated citation links -->
