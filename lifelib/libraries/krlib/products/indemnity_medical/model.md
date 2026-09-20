# Implementation Notes

**Status:** Draft, 2026-09-03. The product this implements is specified in
[`product-spec.md`](product-spec.md) and the projection is derived in
[`technical-notes.md`](technical-notes.md); the sources for both are in
[`sources.md`](sources.md). The worked example of the notes is read **off this model**
rather than the other way round. Every parameter value below is one of theirs, and where
this document adds one it says so and tags it **[std]**.

> **This is a mechanics demonstration, not a pricing or reserving result.** The contractual
> mechanics are sourced clause by clause, and to a precision no other product in this
> repository reaches — the benefit definition of a Korean 실손 contract is the supervisor's
> 표준약관 at 시행세칙 별표 15 and not a carrier document [S1] [REG-R23] [REG-R25] — but
> **every quantitative input is a standardization.** The published 장기손해보험
> 참조순보험요율 of 보험개발원, the statutory rate bureau [REG-R4], does not cover
> 실손의료보험 at all [R20] [REG-R61]; the 산출방법서 where the 예정위험률 and 예정사업비율
> live is a 기초서류 that is filed and never published [REG-R2]; and 제10회 경험생명표
> releases only summary statistics [REG-R33]. There is no public Korean indemnity-medical
> morbidity or severity basis and no public Korean mortality table. Replace the assumption
> tables with company data before drawing any conclusion from the output.

`Medical_KR_S` is a monthly, by-policy projection of gross best-estimate liability cash
flows for 4세대 실손의료보험 (*silson uiryo boheom*, fourth-generation indemnity medical
insurance). **It stands alone in `krlib`**: it inherits nothing and nothing states a delta
against it, because it is the only contract in this repository whose benefit is a
reimbursement of an incurred cost — the 실손해 branch of 보험업감독규정 제7-63조제1항제2호
[REG-R17] [R19] — rather than a stated sum. There is no 보험가입금액 that *determines* a
claim here, only an annual limit that *caps* one.

Two Spaces, the house layout. `Data` is unparameterized and holds eight cells: seven CSV
readers and `input_dir()`. `Projection` carries **120 cells and 47 References** and is
parameterized by `point_id`, so every `Projection[N]` is a separate ItemSpace with its own
cells cache.

---

## Run it

```bash
python products/indemnity_medical/run.py        # anchor cell, point_id = 1
python products/indemnity_medical/run.py 8      # the cell where the public cap binds
```

`run.py` prints the model point, the first thirteen months of the cash flow statement, the
ten policy-year totals, the renewal and experience-rating ledger, the undiscounted totals
and the ten `check_*` identities. Everything it prints is ASCII, so the output lands on a
Windows console under any code page: amounts are labelled `KRW`, and both priced units are
romanized — `geubyeo` for 급여 (covered by 국민건강보험) and `bigeubyeo` for 비급여. Real
output, with the three wide frames elided — they are in
[`technical-notes.md`](technical-notes.md) in full — and with four header lines continued
onto an indented second line so that this page stays inside its column width; the text is
otherwise what `run.py` prints, character for character:

```text
Medical_KR_S - silson uiryo boheom (4th-generation indemnity medical), monthly grid
model point 1: anchor 40M all covers full limit - M40 (man nai, age last birthday),
    inside National Health Insurance
annual limit = KRW 50,000,000 per bojang jongmok   per-visit cap = KRW 200,000
    boninbudam sanghanaek = KRW 3,260,000 (decile 6)
first-year premium = KRW 11,982.00/month, split geubyeo 4,792.80 / bigeubyeo 7,189.20
retention: geubyeo 20% inpatient, bigeubyeo 30% inpatient;
    projection = 120 months, 10 policy years to age 49
modules: bigeubyeo rider = True   3-dae bigeubyeo = True   yoyul sangdaedo = True
         musago halin = True
         suspension rate = 0.00%   cost-trend multiplier = 1.00   utilisation multiplier = 1.00

    [ result_cf() t = 0..12; the ten policy-year totals; result_prem() by policy year ]

Undiscounted totals over the projection (KRW)
  premiums            1,558,165.43
  claims              1,201,095.17
  expenses              109,071.58
  claim_expenses         36,032.86
  commissions            93,489.93
  net_cf                118,475.90
  loss ratio                0.7708

Roll-forward and contractual identities
    [ the ten check_* cells, each True; they are tabulated under Tests below ]
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/indemnity_medical/Medical_KR_S")
model.Projection[1].result_cf()      # the worked example's anchor cell
model.Projection[1].result_prem()    # the renewal and 요율 상대도 ledger, by policy year
model.Projection[1].result_pols()    # the five decrements
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a `DataFrame` indexed by policy month `t`, one column per cash flow
line; `result_prem()` is the frame a reader needs to follow the experience-rating loop,
because it is indexed by **policy year**, which is the clock that mechanism runs on.
`model.Projection.doc` carries the notes' symbols mapped to the cells names and states the
age basis; `model.Data.doc` says what each input file is and, for the mortality table, what
it is **not**.

## Two clocks, and the model keeps them apart in its naming

Cash flows run on the policy **month** and take `t`. Everything the contract itself does —
every limit, every counter, the co-payment cap, the annual aggregate, the renewal, the
experience-rating window — runs on the policy **year** and takes `y`. The year is the
「계약일로부터 매1년 단위로 도래하는 계약해당일 전일까지의 기간」 of [S1 제5조제2항], and
every limit resets on it.

`policy_year(t) = t // 12 + 1` is the only bridge between the two, and the annual claim is
spread evenly across the twelve months of its year **[std]**: nothing published gives a
within-year seasonality, and on this product the month is a presentation grid for an annual
quantity rather than a unit of account. It shows in the printed statement — within a policy
year every per-policy amount is constant and every row is the year's first row scaled by
`pols_if(t)`.

**A cells that takes `y` never takes `t` and vice versa**, which is the whole of the
convention. `claims_ge_in_pp(y)` is a policy-year amount per surviving policy;
`claims(t, "GE_IN")` is the month's cash flow weighted by `pols_if(t)`. Mixing them is the
easiest way to project a year's claim twelve times.

`t` is **0-based**: the first projected month is `t = 0`, the frame is
`range(proj_len())`, and `proj_len()` is the **number** of projected policy months — the
exclusive end of the frame, the library-wide meaning of `proj_len` — `120` on every
shipped model point, so `result_cf()` has 120 rows indexed `t = 0 … 119`. The policy year
`y` is the contractual 1-based label `t // 12 + 1`, derived from `t` and never used to
index the frame; `result_prem()` is indexed by that label, `1 … 10`.

**CSV time keys.** No input file is keyed by the model's `t`. `lapse_table.csv` is keyed
`policy_year` `1 … 10`, a contractual 1-based label read through `policy_year(t)`, so its
values are unchanged; `mort_table.csv` is keyed `(sex, age)` and read at `age(t)`;
`utilisation_table.csv` is keyed `(sex, age_start)` and read at `util_band(y)`;
`severity_table.csv` `(stream, point)`, `claim_shape_table.csv` `bucket`,
`oop_ceiling_table.csv` `decile` and `model_point_table.csv` `point_id` carry no time
axis at all, and `model_point_table.csv` holds no duration or in-force column. Nothing in
the inputs moved with the frame.

## The horizon is two 재가입 cycles, and it is stated rather than contractual

Ten policy years — two five-year 보장내용 변경주기 [S1 제23조]
[REG-R17 제7-63조제2항제6호나목](#krlib-reg-r17) — or the run to `max_cover_age = 100` on 보험나이 if that
comes first, which on the shipped model points it does not.

The distinction is the point, and it is why `reentry_cycles = 2` is a Reference rather than
a hard-coded 120. At the fifth 계약해당일 a 4세대 contract's benefit terms are replaced by
whatever the supervisor is then prescribing — on the real calendar, 5세대, whose 비급여 특약
is split 중증 / 비중증 and which excludes 근골격계 이학요법치료, 체외충격파치료 and 주사료
outright [S2] [R5] [R6]. **Nothing past the first 재가입 is a projection of *this*
contract's terms.** The model assumes re-entry on unchanged terms, twice, and says so; set
`reentry_cycles = 1` for a projection that stops where the specified contract does.

`pols_maturity(t)` carries the survivors out at the horizon. **Nothing is paid** — a
순수보장성 contract has no maturity benefit and there is no `claims(t, "MATURITY")` limb —
but without the count the in-force roll-forward would appear to lose lives with no cause in
the final month. What ends there is the *stated horizon*, not the contract.

## The reimbursement machinery, in the order it must be applied

This is the part of the model that *is* the product, and the order is not optional. Applying
these five reductions in any other sequence produces a number that is not a claim under this
contract.

**1. 본인부담상한제 first, as an exclusion from covered loss** — `oop_trunc(y)`. The NHIS
refunds a member's annual 본인일부부담금 above an income-graded ceiling [R10] [REG-R53], and
the 표준약관 excludes anything so refundable from cover twice over, at 제5조제3항 and at
제4조제3항제1호 [S1]. The 급여 half of the claim is therefore bounded above at roughly
`0.80 × 본인부담상한액` — ₩720,000 for a 1분위 insured on the 2026 scale against ₩6,744,000
for a 10분위 one, a **nine-fold spread driven by income and nothing else**. It is applied
**inside** `paid_out_per_visit`, on the incurred cost, so it changes where the deductible
bites; applied to the finished claim it is wrong on the kinked outpatient limb.

**2. The co-payment and the deductible, per event** — `claims_ge_in_pp`, `claims_ge_out_pp`,
`claims_np_in_pp`, `claims_np_out_pp` and the shared `paid_out_per_visit`. Inpatient
reimbursement is a flat percentage: 80% 급여 [S1 기본형 제3조], 70% 비급여
[S1 특별약관 제3조], 40% on either where 국민건강보험 entitlement does not apply
[S1 제3조제3항제1호]. Outpatient reimbursement is the cost less
`max(flat floor, 자기부담률 × cost)`, then capped per visit at ₩200,000 [S1 제5조제5항];
the floor is ₩10,000 clinic-tier and ₩20,000 hospital-tier on the 급여 side
[S1 기본형 제3조 표1] and a flat ₩30,000 at every provider on the 비급여 side
[S1 특별약관 표1], which is why the 급여 side needs a provider mix (`clinic_share`) and the
비급여 side does not.

**The deductible is applied to the cost *distribution*, never to its mean**, and that is the
single most important implementation decision in the model. The rule is a flat amount below
a crossing point and a percentage above it: at the clinic tier ₩10,000 until ₩50,000 of
covered cost and 20% above it, so a ₩10,000 visit pays nothing, a ₩50,000 visit pays
₩40,000, and the ₩200,000 per-visit cap binds at ₩250,000. `E[f(X)] ≠ f(E[X])` for a kinked
`f`: on the 비급여 통원 stream the mean gives ₩104,545 against the distribution's ₩76,970,
**+35.83%**. `severity_table.csv` exists for exactly this reason, and the error hides — the
급여 통원 blend at `clinic_share = 0.63` is 1.05% wrong while its tiers are +6.36% / −17.01%.

**3. The ₩2,000,000 annual inpatient co-payment cap, on what remains** — the `top_up` term
of `claims_ge_in_pp` [S1 제5조제4항] [REG-R17 제7-63조제2항제2호](#krlib-reg-r17). Applied second, and to
the retention that *survives* the truncation, because both reliefs run in the same direction
and applying them in parallel double-counts.

**4. The 3대비급여 sub-limits, which displace the main limit for their three classes** —
`claims_physio_pp`, `claims_inject_pp`, `claims_mri_pp`, summed in `claims_np_three_pp`.
도수·체외충격파·증식치료 share one 50-act counter and ₩3,500,000; 주사료 has its own 50 acts
and ₩2,500,000; MRI has ₩3,000,000 and no counter [S1 특별약관 제3조(3) 표1]. These caps
**replace** the ₩50,000,000 aggregate for those three classes rather than sitting inside it,
so `np_limit_factor(y)` is applied to `claims_np_main_pp(y)` and never to
`claims_np_three_pp(y)`. Where 3대비급여형 is not held those treatments are simply uncovered
and do **not** fall back into the main limit — model point 6 is that election.

Two gates inside this limb are worth naming. Cover beyond the first ten physical-therapy
acts is conditional on a documented clinical re-assessment every ten acts [S1] [R2] — the
only benefit in `krlib` gated on a *clinical review* rather than on a definition — which a
projection can represent only as a continuation probability at the boundary,
`physio_cont_prob = 0.60` **[std]**. And non-covered injections of 항암제, 항생제 and
희귀의약품 leave the ₩2,500,000 sub-limit for the main 비급여 limit
[S1 특별약관 제3조(3)제2항]: `inject_carve_share = 0.25` **[std]** draws that boundary, the
carved payment is added in `claims_np_out_pp` and removed from `acts_inject_eff(y)`, and
since non-covered injections were 18.5% of all 2024 claims [R8] it is a first-order
calibration question rather than a detail.

**5. The annual aggregate, per 보장종목 and per policy year** — `ge_limit_factor(y)`,
`np_limit_factor(y)`. 상해 and 질병 carry separate ₩50,000,000 limits on each of the two
parts [S1 제5조], so the raw claim is split by `share_injury = 0.15` **[std]** and each part
capped — a whole-contract annual exposure of ₩100,000,000 in the ordinary reading.

### What a deterministic projection can and cannot say about the limits

`E[min(X, Λ)] ≠ min(E[X], Λ)`. A projection that applies a limit to an expectation
**understates** the limit's bite by ignoring dispersion. On every shipped model point the
₩2,000,000 inpatient cap, the three 3대비급여 money limits, the two 50-act counters, the
100-visit cap and the ₩50,000,000 annual limits do **not** bind: the expected annual claim
of a single cell is two orders of magnitude below them, and the supervisor's own tail figure
is that 0.005% of insureds took more than ₩50,000,000 in 2019 [R1].

The machinery is implemented anyway, for two reasons: it binds under any seriatim or
stochastic run, which is where the dispersion an expected-value grid averages away lives;
and `check_annual_limits()` proves it is **wired**, which is a different claim from proving
it is **exercised**. **Do not delete a limit because it reads slack.**

The one limit that *does* bind on a shipped point is the 본인부담상한제 truncation, on model
point 8 — a high-utilisation cell (`util_mult = 10`) on the lowest 본인부담상한액 decile —
where `oop_trunc(y)` runs from **0.801828** in policy year 1 to **0.602441** in year 10,
with a visible step at the utilisation band change in year 6. On the anchor it is
identically 1.0, the incurred 급여 본인부담금 of ₩84,805.89 sitting a factor of 38.4 below
the ₩3,260,000 ceiling, so the error a wrong ordering would make is invisible. That is why
model point 8 exists.

## The experience-rating loop is the model's reason to exist

The renewal premium of the 비급여 rider is a function of the individual policyholder's own
prior-year non-covered claim amount [S1 특별약관 제6조제3항] [R2] [R3]: a feedback loop from
claims to premium, inside a single policy, on an annual clock, **modelled rather than
described**, which is the whole reason this product is in the library.

**The band is memoryless**, so there is no chain to carry: 「보험금 지급(사고) 이력이
1년마다 초기화됩니다」 [R2]. `band_share(y, b)` reads `claims_np_rated_pp(y − 1)` and nothing
earlier, so the band distribution at renewal `y` is simply the distribution of the annual
rated claim in year `y − 1` — `claim_shape_table.csv` rescaled by `shape_rel(k)` to that
year's mean and read against the **fixed money thresholds** ₩1,000,000 / ₩1,500,000 /
₩3,000,000 [S1 특별약관 제6조제3항]. Because the thresholds are fixed money and the claim
level trends, contracts migrate into the surcharge bands year by year with nothing in the
model changing. **That migration is the loop.** On the anchor the 3단계 buckets empty by
policy year 5 and the 5단계 contribution to the surcharge pool rises from 0.012 at
commencement to 0.040 by policy year 7.

**The discount is solved, not set.** The wording defines it as the solution to a
revenue-neutrality constraint — 「상대도 적용 전·후의 총 보험료 수준이 일치하도록」 [S1] —
so `reld_solved(y) = (1 − Σ_{b≥2} w_b r_b) / w_1`. The shape table is calibrated so that at
the anchor cell's first-year claim level the band mix reproduces the published commencement
distribution 72.9 / 25.3 / 0.8 / 0.7 / 0.3 [R12] exactly, which makes the solved
discount come out at **0.957477 — the specification's 0.9575, a 4.25% discount** — as a
*result* rather than as an input. Hard-coding the illustration's 0.95 instead gives
`reld_avg = 0.9945494`, a 0.55% leak out of a scheme the wording requires be self-financing,
growing as the band mix moves. `check_relativity_neutral()` is the identity that proves it.

A **[std]** cap of 5% sits under the discount, `reld_disc_cap = 0.05`, from the two
published values — 「5% 내외」 at launch [R1] and −5% 잠정 at commencement [R3]. It is slack
at commencement and binds from policy year 5 on the anchor cell; from there the scheme stops
being revenue-neutral and the average relativity rises above 1 — `reld_avg` reaching
1.0025494 at year 5 and 1.0095494 from year 7, and **1.329009** on the high-utilisation
model point 8. **That is the loop reaching the aggregate**, and it is a feature of the
design rather than of this implementation.

Two things run alongside and are different animals. The **무사고 할인** takes 10% off the
*whole* office premium after **two** consecutive claim-free years [R1] [S3], where the
relativity has a one-year lookback and touches only the rider:
`noclaim_share(y) = band_share(y − 1, 1) × band_share(y, 1) = 0.729012² = 0.5314584961` on
the anchor, the two years treated as independent **[std]**. A one-year lookback would hand
the discount to policyholders who had earned one clean year and cost 2.09% of the year-3
office premium. And the **three-year deferral**, `reld_start_year = 4`, reflects the
2024-07-01 commencement three years after launch [R3]: the anchor cell's first three
renewals are a plain attained-age re-rate, which is what 1세대 through 3세대 were.

`reld_exempt_share = 0.15` **[std]** strikes 산정특례 conditions and all claims of an
insured graded 장기요양 1·2등급 out of the **rating count** and never out of the benefit
[S1 특별약관 제6조제3항] [REG-R54]: `claims_np_pp(1) = 62,978.2477` is paid in full while
`claims_np_rated_pp(1) = 53,531.5106` is what the band is read against. Applying the 15% to
the claim would silently delete a fifteenth of the cover. This exemption is the only direct
statutory cross-reference between this model and [`LTC_KR_S`](../long_term_care/model.md).

## The renewal recursion, and one order of operations

    base(y) = base(y-1) × (1 + a) × (1 + b(y)),   a = 0.04,  |b(y)| ≤ 0.25

The 표준약관's own renewal illustration labels its basis increment
「기초율 증가분 = 전년도 기준보험료 × 25%」, which reads as additive — but 3,640 is 25% of
`14,000 × 1.04 = 14,560` and **not** of 14,000: the corridor applies to the **age-adjusted**
prior premium [S1 제30조]. Reproducing the illustration's printed row
14,000 → 18,200 → 23,660 → 30,758 → 39,985 → 51,980 requires it. Getting it wrong costs 4%
of the corridor every year and compounds — `prem_np_base(10) = 20,625.8505` on the correct
recursion against 20,096.9929 on the additive misreading, 2.564% low.

`b(y)` is **not an input**. Each priced unit is re-rated at **its own** claim trend, clipped
to the corridor — `basis_incr_ge(y)` at `med_trend_ge = 0.010` and `basis_incr_np(y)` at
`med_trend_np = 0.081`, the 2024 growth rates of the statutory co-payment and of non-covered
spend [R9] [REG-R41]. That **[std]** re-rating rule is what keeps each unit's loss ratio
stable unless the corridor clips it, and it is why the two units are re-rated separately:
the corridor binds **per 위험구분단위** and not on the portfolio average
[S1 제30조제2항] [REG-R17 제7-63조제2항제3호](#krlib-reg-r17), which is what `check_renewal_corridor()` tests
— each unit, against the age-adjusted prior premium.

The relativity is applied **only to the rider**, in `prem_gross_mth(y)` and never to
`prem_np_base(y)`: 「비급여 특약 보험료만 할증되며 보험료 전체가 할증되는 것은
아닙니다」 [R2]. Applying `reld_avg(y)` to the whole office premium gives a year-5 gross of
₩16,440.5468 against the correct ₩16,426.4626.

**A finding worth recording.** The corridor and the age loading compose multiplicatively, so
the wording admits a re-rate of `1.25 × 1.04 = 1.30` a year. A claim trend below 30% is
therefore fully recoverable and the corridor does not bind *economically* even where it
bites arithmetically: model point 10 carries `trend_mult = 4.5`, its 비급여 re-rate is
clipped from 36.45% to 25%, and its loss ratio still rises only from 0.5333 to 0.5913 over
ten years. **The ±25% corridor is a much weaker constraint than it looks.**

## Renewal decline is its own decrement, and not a lapse

`renewal_decline_rate = 0.01` a year **[std]**, acting only in the twelfth month of each
policy year, `pols_renewal_decline(t)` non-zero only where `(t + 1) mod 12 = 0`. It is a
**separate decrement** from `pols_lapse` because it is a separate act: a lapse is a missed
premium and a decline is the exercise of a contractual option at a contractual date, on a
contract the insurer cannot exit [S5] [S3]. On a one-year renewable product the second is
what the product is exposed to, and it is the **larger** of the two voluntary exits at every
annual boundary — 0.0089881183 against 0.0079263524 at `t = 11`, and 0.0083529502 against
0.0043181413 at `t = 23`.

Folding it into `lapse_rate_mth(t)` makes the annual boundary invisible, and
`check_pols_roll_fwd()` balances either way, so the roll-forward will not catch it. On a
contract whose whole architecture is annual, that boundary is what the model exists to show.
The five decrements are applied in the order mortality, lapse, suspension, renewal decline
**[std]**; nothing published fixes it, and at these rates the ordering is worth less than a
basis point a year.

## Three absences that are product facts

Each of these is a missing cells, so nothing in the output points at it; the test module
asserts the name list instead.

- **No death benefit.** On death from a non-covered cause the contract pays the 계약자적립액
  and the 미경과보험료, and on a one-year pure protection contract the 계약자적립액 is nil
  [REG-R17 제7-63조제1항제1호](#krlib-reg-r17) [REG-R25 제22조](#krlib-reg-r25). Mortality is therefore a pure
  **liability-releasing** decrement, there is no `claims_death`, and the direction of
  prudence is inverted with it: an *over*-statement of mortality is *anti*-conservative.
- **No surrender value.** 「이 상품은 1년만기 순수보장성 상품으로 해약환급금이 발생하지
  않습니다」 [S3]. There is no `cv_pp`, no `claims_lapse` column, no 보험계약대출 and no
  보험료 자동대출납입 — so there is **nothing to break the fall** on a missed premium, which
  is the reason the first-year lapse rate is what it is. The 표준해약공제액 cap of [별표 14]
  has nothing to bite on either [REG-R20] [REG-R19].
- **No waiting period.** Unusual among Korean health products, and a direct consequence of
  the indemnity form: there is no lump sum to anti-select against, so no 면책기간 and no
  감액기간 of the kind [`Cancer_KR_S`](../cancer/model.md) carries.

A fourth absence is easy to misread as a bug. **There is no acquisition strain**:
`commissions(t)` and `expenses(t)` are level rates on every premium and `t = 0` is
**positive at ₩205.4984**, because on a rolling one-year renewable the acquisition/renewal
distinction has no content after year one. A reader who expects the sister libraries'
month-0 trough will look for a bug that is not there.

## Modules that are off in the base run

Each is implemented, off on the anchor so the base run reproduces the worked example, and
exercised somewhere in the shipped table.

| Module | Off position | Switched on |
|---|---|---|
| **개인실손 중지·재개** — suspension while a 단체실손 is in force, mandatory as a facility under 감독규정 제7-63조제2항제7호 [REG-R17] [R16] | `suspend_rate = 0` on nine of ten points; `suspend_rate_mth(t)` is then identically zero | Model point 9 at 3% a year. **Resumption is not modelled**: the contract that resumes is a different projection, so this is carried as a decrement and not as a state |
| **The 40% branch**, where 국민건강보험 entitlement does not apply [S1 제3조제3항제1호] [S1 특별약관 제3조제8항] | `nhi_covered = 1`, retention 20% / 30% | Model point 10: retention rises to `retain_rate_nonhi = 0.60` on **both** parts and the 본인부담상한제 switches off, because a life outside the scheme is not refunded by it |
| **요율 상대도** [S1 특별약관 제6조] | `reld_on = 0`; `reld_active(y)` false, `reld_avg(y) ≡ 1` | On on eight points. Off on 5 and 9, where the contract is a plain attained-age renewable — which is what 1세대 through 3세대 were |
| **무사고 할인** [R1] [S3] | `noclaim_on = 0`; `noclaim_share(y) ≡ 0` | On on eight points; off on 5 and 9 beside the relativity |
| **3대비급여형** [S1 특별약관 제3조(3)] | `three_np = 0`; `claims_np_three_pp(y) ≡ 0` and those treatments are uncovered, not folded into the main limit | Model point 6 is the not-held election |
| **The 비급여 특약 itself** [S1 특별약관] | `np_rider = 0`; the whole rider limb and the relativity with it | Model point 5 is 급여-only, at `np_share = 0`. This is the 주계약 standing alone, which is a permitted 가입 유형 [R6] |

`trend_mult` and `util_mult` are stress multipliers rather than modules — 1.0 on the anchor,
4.5 on point 10 (cost trend, which runs the corridor into its clip) and 10.0 on point 8
(utilisation, which is what makes the public truncation bind).

### Named and not modelled

- **The behavioural response to the experience rating.** The supervisor's own worked example
  has a policyholder cutting his claims by 93% in response to a surcharge, saving ₩300,000
  of premium and ₩2,700,000 of out-of-pocket cost in one year [R2]. The contract is
  *designed* to change the insured's behaviour; this model projects the premium's response
  to claims and not the claims' response to premium. A stated limitation, not an oversight.
- **The frequency half of the claim distribution.** `claim_shape_table.csv` trends its
  amounts and holds its zero-claim mass fixed at 0.729012, so the 1단계 share is constant
  while the size of a claim grows. In reality claiming frequency rises with age too.
- **재가입 into a *different* generation** — which is what will actually happen at the fifth
  anniversary [R7] — and with it **계약전환**, the 계약재매입 and 선택형 할인 schemes of the
  2026 reform [R5], **노후실손 / 유병력자실손** [R17], **단체실손**, **해외여행 실손**, and
  the resumption half of 중지·재개 [R16].
- **Any measurement basis.** No 책임준비금 [REG-R3] [REG-R8], no CSM [REG-R60], no risk
  adjustment, no K-ICS 요구자본 [REG-R13], no 해약환급금준비금 [REG-R11], no policyholder
  tax [REG-R57]. On a one-year indemnity contract the 잔여보장요소 is at most one year's
  unearned premium and the 발생사고요소 is the material item, and the 해약환급금준비금 has
  nothing to bite on because there is no surrender value at all.

## Inputs are external files

Seven CSVs in `products/indemnity_medical/`, beside `run.py`, read at run time. The model
folder holds `__init__.py`, `_system.json` and its two Space folders and nothing else — no
`_data/`, no IOSpec, no embedded values — so a diff of the model shows logic changes only.
This is the `annuallife.TradLife_A` layout; contrast `basiclife.BasicTerm_S`, which keeps
its inputs inside the model. The consequence worth knowing: **the model is not portable on
its own** — copy `Medical_KR_S` without its parent's CSVs and it reads cleanly, then fails
on first evaluation.

| File | Reference | Reader | Contents |
|---|---|---|---|
| `model_point_table.csv` | `model_point_file` | `Data.model_point_table()` | ten policy configurations, indexed by `point_id` |
| `mort_table.csv` | `mort_table_file` | `Data.mort_table()` | **[std]** Makeham construction, sex × 만나이 0–110, 222 rows |
| `lapse_table.csv` | `lapse_table_file` | `Data.lapse_table()` | **[std]** annual lapse by policy year 1–10, last row applying onward |
| `utilisation_table.csv` | `utilisation_table_file` | `Data.utilisation_table()` | **[std]** annual claim frequencies and mean stay, sex × five-year band, 36 rows |
| `severity_table.csv` | `severity_table_file` | `Data.severity_table()` | **[std]** discrete cost distribution per event, eight streams, 33 points |
| `claim_shape_table.csv` | `claim_shape_file` | `Data.claim_shape_table()` | **[std]** ten-bucket distribution of the annual rated 비급여 claim |
| `oop_ceiling_table.csv` | `oop_ceiling_file` | `Data.oop_ceiling_table()` | 본인부담상한제 ceiling by income decile, 2026 scale — **transcribed** [R10] |

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so readers placed there would re-read every
file for every policy. They live in the unparameterized `Data` Space instead, and
`test_inputs_are_read_once_not_once_per_model_point` asserts the property against the file
set registered in `kr_registry.INPUT_FILES`. `input_dir()` returns `_model.path.parent`,
resolved at run time and never hard-coded, so the model works from any checkout.

**Every assumption CSV carries a `provenance` column and every cell in it begins with a
citation tag.** `model_point_table.csv` is the only exemption, a model point being a
configuration rather than an assumption.

To swap in a company basis, replace the CSVs with same-schema files, or point the `*_file`
References at different names, and clear the cache. No formula changes.

### Six of the seven tables are constructions, and that is a finding

It is worth being exact about *why*, because it is a positive result about what Korea
publishes rather than a list of documents this pass failed to fetch. The published
장기손해보험 참조순보험요율 covers 일반상해, 교통상해, 질병 사망률, 후유장해, 입원율,
암 발생률, 비용손해, 재물손해 and 배상책임 — **실손의료보험 is not among them** [R20]
[REG-R61] — and the 산출방법서 is never published [REG-R2]. What the supervisor *does*
publish, annually and in quantity, is **aggregate** experience [R7] [R8] [R12] [REG-R44],
and every table below is anchored on that.

**`mort_table.csv`, and the prudence that runs backwards.** A **[std]** Makeham
construction, `q(x) = 1 − exp(−(A + B·c^x))` above age 15 with a log-linear child schedule
below it, fitted to the four summary statistics 국가데이터처 publishes [REG-R38]. It is
**not** a transcription: 제10회 경험생명표 is not published in full [REG-R33] and the
single-year 완전생명표 `qx` tables live behind KOSIS and were not downloaded [REG-R39]. Male
`q(40) = 0.00132019`. As noted above, on this product an over-statement of mortality is
anti-conservative — the reverse of every other model in the library — so the usual instinct
to load the table is wrong here.

**`lapse_table.csv`.** 0.100 falling to **0.020** over policy years 1–10, the last row
applying onward. No 실손-specific persistency table is published anywhere. The ultimate is
anchored on the only 실손-specific figure there is — the 1–3세대 in-force block fell **3.3%**
in 2025 [R7] — which blends lapse, death and conversion, so 2.0% is what is left once
mortality and the renewal decline are taken out. The first-year rate is set against an
**[unverified]** 장기손해보험 13회차 유지율 of about 86%, from a news summary.

**`utilisation_table.csv`, and how its level was solved.** The age-40 male row is not chosen;
it is solved from three published quantities, and the solve is what makes the anchor cell
reproduce the market rather than resemble it:

1. the **premium** is the published 2021 new-business anchor, ₩11,982 a month for a 40세
   남자 on a 10-carrier 손해보험 average [R1] — and male 40 is the 기준연령 요건 of
   감독규정 제1-2조제2호 [REG-R9], so it is the prescribed disclosure cell as well;
2. the **loss ratios** are the published 4세대 2022 첫 반기 figures — 급여 **97.5%**,
   비급여 **73.0%**, combined **82.8%** [R12] — applied to that premium on the 40/60 split
   [R2], giving targets of ₩56,075.8 and ₩62,977.4 of first-year claim;
3. the **inpatient share of the 비급여 claim** is set at **0.30 [std]**, which is what fixes
   the admission frequency, since one admission drives both halves of the claim.

Three scalars — one on admissions, one on 급여 outpatient visits, one on everything 비급여 —
are then solved so that the model's own year-1 arithmetic hits both targets: the model
produces ₩56,076.22 and ₩62,978.25, a first-year combined loss ratio of **0.8280091**. The
age curves and the sex factors around the solved row are **[std]** shapes following the NHIS
coverage ratios by age band [R9] [REG-R41], and there is deliberately **no maternity bump**
in the female rows, because pregnancy and childbirth are excluded from 4세대 cover.

One thing must be said plainly here. 보험개발원 **does** publish a 질병입원율 grid by age
and sex on the same display [REG-R61]. It is a 장기손해보험 fixed-benefit hospitalization
incidence on a 참조순보험요율 (net premium) footing, not a count of admissions producing a
payable indemnity claim after a 20% co-payment, and a reference net rate is not a best
estimate. It is therefore available as an external anchor for the **age slope** of
`adm_rate` and is not used for the **level**; substituting it, and restating the level solve
against it, is the first thing a user with company data should try. **실손 위험률 itself
remains unpublished** [R20].

**`severity_table.csv`.** Eight discrete distributions — `ge_in`, `ge_out`, `np_in`,
`np_room`, `np_out`, `physio`, `inject`, `mri` — because a single mean is unusable against a
kinked deductible, as above. The dispersion being standardized over is real and published:
the 건강보험심사평가원 price survey found 도수치료 quoted anywhere between **₩5,000 and
₩600,000** across Seoul hospitals [R2].

**`claim_shape_table.csv`.** Tabulated in KRW at the anchor's first-year level and read as a
*shape*: `shape_rel(k)` divides each bucket by `shape_mean() = 53,530.7924`, so the same
distribution serves every model point and year and only the **level** comes from the model.
Bucket 0 carries the 72.9% no-claim mass, the six small buckets take their dispersion from
the **six lowest bands** of the published 4세대 claim-size distribution [R12] — those bands'
shares normalised, and their midpoints scaled by a single factor onto the sub-₩1,000,000
range 2단계 occupies — and the three tail buckets sit inside the surcharge bands at the
published 0.8 / 0.7 / 0.3 shares [R12]. `check_claim_shape()` asserts both
normalisations — `Σ share = 1` and
`Σ share × rel = 1` — because a shape that does not integrate to its own mean makes
`reld_solved()` divide by the wrong denominator.

**`oop_ceiling_table.csv` is the only transcription in the set** — the 2026 본인부담상한제
scale, ₩900,000 at 1분위 to ₩8,430,000 at 10분위 [R10] — and it is the single most important
interaction in the product, because it is where a public scheme reaches inside a private
contract and truncates half of its claim, differently by income.

## Sign convention

`net_cf` is **income positive** — premiums less every claim limb, less maintenance expense,
less claim handling expense, less commission — the library-wide sign and the notes' own, so
unlike the whole life and payout annuity models there is no outgo-positive `liability_cf`
companion to publish: one stream, one sign, one name.

The shape to expect is unlike anything else in the library. The whole ledger collapses to
`net_cf = 0.87 × premiums − 1.03 × claims`, so the sign of any period is decided by one
number — the loss ratio, against the model's own break-even of **0.844660**. Year 1 runs at
0.828009, which is the calibration closing rather than an accident, so the product opens on
a margin of about 1.7% of premium with a claim already 98% of the way to break-even. The one
negative year is policy year 6, at **−₩276.14**, where the utilisation band steps at
attained age 45 while the premium takes its age loading smoothly.

## The identity `check_net_cf()` closes

One line, and it is the one a reader adding up the printed statement is checking:

    net_cf = premiums − claims_ge_in − claims_ge_out − claims_np_in − claims_np_out
             − claims_np_three − expenses − claim_expenses − commissions

`check_net_cf_resid(t)` computes it as `net_cf(t) − (premiums(t) − claims(t) − expenses(t) −
claim_expenses(t) − commissions(t))`, with `claims(t)` summing over exactly the five kinds
`result_cf()` prints. Reading the benefit back out of the same `claims(t, kind)` machinery
the columns are built from is the point: it catches a benefit kind that exists in
`claims(t, kind)` but was never given a column, which would leave the statement silently
short of outgo the model is charging.

It is also why `result_cf()` publishes the five `claims_*` split columns and **no aggregate
`claims` column** — an aggregate beside its parts stops the columns summing to `net_cf`
without knowing which to skip, which is why `claims` is in the library's `RETIRED_COLUMNS`
register. The `claims(t, kind)` cells stays, and `claims(t)` with no `kind` is the sum.
`check_net_cf()` closes to `cash_tol = 1e-6` rather than to `roll_fwd_tol = 1e-10`, because
it re-reads won amounts through a chain of annual-to-monthly divisions; `check_claim_shape()`
has a third tolerance, `shape_tol = 1e-9`, closing a probability distribution and not an
amount.

## Naming

`lower_snake_case` throughout, reusing lifelib's `basiclife.BasicTerm_S` vocabulary wherever
there is an analogue: `pols_*` for counts, plural nouns for cash flows, `*_rate` annual with
`*_rate_mth` monthly, `*_pp` per policy, `claims(t, kind)` with an uppercase `kind`, and
`pols_if_at(t, timing)` for the within-month reads. Quantities on the **policy year** take
`y` and never `t`.

### The notes' symbols, and where they live

`model.Projection.doc` carries the full 80-row table; the load-bearing rows are these.

| Notes symbol | Cells | Meaning |
|---|---|---|
| `x`, `age(t)`, `y(t)` | `issue_age()`, `age(t)`, `policy_year(t)` | 가입나이 on 만나이, attained 만나이, `t // 12 + 1` |
| `P0`, `s` | `premium_mth_pp()`, `np_share()` | first-year office premium; 비급여 share of it |
| `L`, `Lv` | `annual_limit()`, `visit_cap()` | 연간 보험가입금액 per 보장종목; 통원 1회당 한도 |
| `q(t)`, `w(t)`, `d_ren(t)` | `mort_rate_mth(t)`, `lapse_rate_mth(t)`, `renewal_decline(t)` | the three voluntary and involuntary monthly decrements |
| `l(t)` | `pols_if(t)` | in force at the **start** of month `t` |
| `n_adm(y)`, `n_ge(y)`, `n_np(y)` | `adm_rate(y)`, `visit_rate_ge(y)`, `visit_rate_np(y)` | annual frequencies at the attained band |
| `r_ge`, `r_np` | `retain_rate_ge()`, `retain_rate_np()` | 자기부담률, 20% / 30%, or 60% off-scheme |
| `C_ge(y)`, `S`, `tau(y)` | `oop_incurred_ge(y)`, `oop_ceiling()`, `oop_trunc(y)` | 급여 본인부담금 incurred, the 상한액, the truncation |
| `paid_*(y)` | `claims_ge_in_pp(y)` … `claims_np_three_pp(y)` | the five per-policy annual claim limbs |
| `C(y)` | `claims_np_rated_pp(y)` | the **rated** 비급여 claim, exemptions removed |
| `w_b(y)`, `r_b` | `band_share(y, b)`, `band_relativity(b)` | the five-band 요율 상대도 mix and its factors |
| `r_1` solved / applied | `reld_solved(y)`, `reld_one(y)`, `reld_avg(y)` | before the cap, after the cap, the average applied |
| `a`, `b_u(y)` | `age_load`, `basis_incr_ge/np()` | the 4% age loading; the clipped basis increment |
| `base_u(y)`, `gross(y)` | `prem_ge_base(y)`, `prem_np_base(y)`, `prem_gross_mth(y)` | the two 기준보험료 and the office premium |
| `CF(t)` | `net_cf(t)` | net cash flow, income positive |

Four needed care, and the reasons are in the `Projection` docstring. `oop_trunc(y)` is a
factor on the *incurred loss* and not on the benefit, which makes its position in the
calculation order legible from its name. `claims_np_rated_pp(y)` is a different quantity
from `claims_np_pp(y)` and not a netting of it — one is paid, the other is rated.
`reld_solved` / `reld_one` are spelled apart because the gap between them *is* the discount
cap binding. And `band_share(y, b)` takes the year whose renewal it prices, reading the
claim of `y − 1`, so no caller has to remember the offset.

### Names this product argued for in krlib's cross-model review

Three. Two of them retired a rival name into the shared `RETIRED_NAMES` register, so no
krlib model reintroduces it; the third is a structural argument about which limb a claim
belongs to and has no retired counterpart, though the `claims` subtotal column it depends
on being absent is in `RETIRED_COLUMNS`.

- **`renewal_decline_rate`, not `renew_rate`.** The proportion who *decline* a 갱신 is a
  decrement, and the shorter name read as its complement to half the models that tried it.
  [`Term_KR_S`](../term_life/model.md) uses the same name for the same event on a ten-year
  cycle; this product uses it on a one-year cycle, which is where it matters most.
- **`claims_np_three` as a column and a limb of its own.** The three 3대비급여 classes sit
  inside the 특별약관 but carry their own money and count limits **instead of** the
  ₩50,000,000 aggregate, so folding them into `claims_np_in` or `claims_np_out` would lose
  the distinction the contract makes and route them through `np_limit_factor(y)`.
- **`pols_maturity`, not `pols_expiry`.** The count whose cover ends at the scheduled end,
  paid or not. This product pays nothing for it and publishes it anyway, which is the case
  the register exists to settle: `claims(t, "MATURITY")` would be the payment, and there is
  none.

One name was argued *against*. `retain_rate_*` holds the fraction the insured **keeps**
(0.20, 0.30, 0.60), not the fraction reimbursed, because 자기부담률 is the wording's own
quantity and inverting it would put the model and the 표준약관 in different units at the
exact clause where they must agree.

## Standardizations used

Every row is **[std]**; the sourced contractual parameters are in
[`product-spec.md`](product-spec.md) and [`technical-notes.md`](technical-notes.md) and are
not repeated. "Observed range" is what the retrieved documents actually bound, and several
bound nothing at all — which is said rather than papered over.

| Parameter | Value | Rationale | Observed range |
|---|---|---|---|
| `reentry_cycles` | 2 | two 보장내용 변경주기, so the horizon is ten policy years; past the second 재가입 the terms projected are not the terms specified [S1 제23조] | the cycle length itself is sourced at 5 years [S1] [REG-R17]; 2세대 wrote 15 [S4], and the number of cycles to project is a choice nothing bounds |
| `renewal_decline_rate` | 0.01 | no published 실손 renewal-decline series exists; the residual of the 3.3% blended 1–3세대 in-force decay [R7] once mortality and lapse are taken out | none published for any Korean product |
| lapse curve | 0.100 → 0.020 over ten years | anchored on the same 3.3% blended decay [R7]; nothing to break the fall on a contract with no surrender value [S3] | first year set against an **[unverified]** 장기손해보험 13회차 유지율 of about 86% |
| utilisation **level** | solved on three published quantities | the anchor cell's year-1 급여 and 비급여 claims are made to reproduce the published 4세대 2022 loss ratios [R12] on the published 2021 premium anchor [R1] | the solve reproduces 97.5% / 73.0% / 82.8% exactly; the level itself is not otherwise bounded, 실손 위험률 being unpublished [R20] |
| inpatient share of the 비급여 claim | 0.30 | needed to close the 비급여 solve, one admission driving both halves of the claim | none published |
| utilisation **shape** | NHIS coverage ratios by age band | age curves and sex factors follow the public coverage-ratio profile [R9] [REG-R41]; no maternity bump, pregnancy being excluded from cover [S1] | the 질병입원율 grid of [REG-R61] is an external anchor for the **slope** and is deliberately not used for the level |
| severity distributions | eight discrete grids | a kinked deductible makes `E[f(X)] ≠ f(E[X])`; a mean overstates the 비급여 통원 claim by 35.83% | the dispersion is real and published — 도수치료 ₩5,000 to ₩600,000 across Seoul hospitals [R2] |
| claim-shape zero mass | 0.729012, held constant | the shape trends its amounts and not its frequency; a stated limitation, since claiming frequency rises with age too | the 72.9% commencement share is sourced [R12]; the FSC's own commencement mix [R3] resolves only three bands and puts 1등급 at 62.1%; nothing published gives the trend of either |
| `physio_cont_prob` | 0.60 | the ten-act clinical re-assessment gate is the only benefit in `krlib` conditioned on a clinical review [S1] [R2] | **none published**; nothing bounds it |
| `inject_carve_share` | 0.25 | the 항암제·항생제·희귀의약품 share leaving the ₩2,500,000 sub-limit [S1 특별약관 제3조(3)제2항] | none published; non-covered injections were 18.5% of all 2024 claims [R8], so the boundary is first-order |
| `share_injury` | 0.15 | splits the claim between 상해 and 질병 so each can be capped at its own ₩50,000,000 limit [S1 제5조] | none published; binds nowhere on the shipped points |
| `med_trend_ge`, `med_trend_np` | 0.010, 0.081 | 2024 growth of the statutory co-payment and of non-covered spend [R9] [REG-R41]; the re-rating rule `b_u(y) = clip(trend × k, ±0.25)` is derived from them | scheme outlay grew 4.3% on the same measure; 비급여 compounds at about twice the whole |
| `age_load` | 0.04 | **the only published age-slope datum in any retrieved document**, derived: the 표준약관's renewal illustration prints 나이증가분 that are each exactly 4.0% of the prior base [S1 제30조] | stylised, at an unnamed age; a flat 4% is not a real age slope and over-recovers against the utilisation curve at these ages |
| `reld_disc_cap` | 0.05 | a floor under the solved discount, from the two published values 「5% 내외」 [R1] and −5% 잠정 [R3] | those two figures are the range; the wording itself sets no cap |
| `reld_exempt_share` | 0.15 | the 산정특례 and 장기요양 1·2등급 exemptions from the **rating count** [S1 특별약관 제6조제3항] [REG-R54], anchored on 암 and 뇌·심혈관 claims at 15.0% of 2025 claims [R7] | the 15.0% claim share is sourced; the exempt fraction of it is not |
| `reld_start_year` | 4 | the 2024-07-01 commencement, three years after the 2021-07-01 launch [R3] [R1] | dates sourced; nothing to bound |
| `noclaim_share(y)` | `w_1(y−1) × w_1(y)` | successive years' claiming treated as independent; the 무사고 할인 has a two-year lookback [R1] [S3] | nothing published gives the persistence of claiming |
| `comm_rate`, `expense_maint_rate`, `expense_claim_rate` | 0.06, 0.07, 0.03 | a split of the one published aggregate — 손해조사비 plus 사업비 of about **16.1%** of 2025 premium [R7]; claim handling is charged on **claims** because 손해조사비 is claim-driven | no 상품요약서 with a 사업비 disclosure was obtained for any generation; 감독규정 제4-32조제5항 caps first-year commission at one year's premium and is nowhere near binding [REG-R22] |
| mortality construction | Makeham above 15, log-linear child schedule below | 제10회 경험생명표 is not published in full [REG-R33] and the KOSIS single-year `qx` tables were not downloaded [REG-R39]; fitted to the four published summary statistics [REG-R38] | male e₀ 80.585 against 80.8, e₆₅ 19.455 against 19.5; female 86.370 against 86.6 and 23.657 against 23.7 |
| `oop_trunc(y)` as a proportional scaling | one factor a year | a proportional truncation of an expectation is not the same as truncating each realisation, and the NHIS ceiling runs on the **calendar** year while every contractual limit runs on the **policy** year | the ceiling table itself is transcribed [R10]; the deterministic representation is the standardization |
| within-year claim spread | uniform over twelve months | no published seasonality; the contract's own machinery is annual, so the month is a presentation grid | none published |
| decrement order | mortality, lapse, suspension, renewal decline | nothing published fixes it; worth less than a basis point a year at these rates | none |
| 보험가입금액 election | ₩50,000,000 with ₩200,000 per visit on nine points, the ₩10,000,000 / ₩100,000 rung on point 7 | the **ceiling** is sourced [S1 제5조]; which rung a carrier sells is a 사업방법서 matter | a 5세대 menu offers ₩50m / ₩30m / ₩10m against ₩200k / ₩150k / ₩100k [S3] |
| 가입나이 envelope | 0–65 | not published; a 사업방법서 matter [REG-R2] | 0–49 on one 2세대 direct product [S4]; 노후·유병력자 families run to 90 [R17] |
| `roll_fwd_tol`, `cash_tol`, `shape_tol` | 1e-10, 1e-6, 1e-9 | one closes an identity between cells in a single expression, one re-reads won amounts through annual-to-monthly division, one closes a probability distribution | all far below one won, or one part in 1e9 of a probability |

**Two of these are the ones to replace first.** `inject_carve_share` sits on 18.5% of the
national claim; and the utilisation level is a solve against a *published loss ratio* rather
than against experience, so it reproduces the market's 2022 result exactly and carries none
of the 2023–2025 deterioration that ran the generation to **115.1%** by 2025 [R7] [R8]. That
gap is not a difference of view about the mechanics: it is the five-year grace on
rate-adequacy verification of 감독규정 제7-63조제2항제6호가목 [R12] [REG-R17], under which
4세대 first re-rated in 2025. **The model re-rates from year 2; the real book could not.**

## Tests

`tests/test_model_conventions_kr.py` applies the house style, parametrized over
`kr_registry.MODELS` rather than restated here: the two-Space layout, the external inputs
with no orphan CSV, the `provenance` column and citation tag on every assumption CSV row,
the docstrings and their required phrases, the age basis declared in the `Projection`
docstring (**만나이** here, and the model says so because the contract prices on 보험나이 and
the two differ for half of all issue dates [S1 제21조] [REG-R25]), the `result_cf()` contract
— indexed by `t`, first column `pols_if`, a `net_cf` column, all names `lower_snake_case`, no
NaN, and the 0-based frame `range(proj_len())`: 120 rows, `t = 0 … 119`, last index
`proj_len() - 1` — that every `check_*()` returns `True` on **every** shipped model point, and
the read → write → re-read round trip. The ten `check_*()` cells each take no argument and
return a real `bool`, with the signed residual under `check_*_resid`.

| Check | What it asserts, and what it would catch |
|---|---|
| `check_pols_roll_fwd` | the five decrements account for every life leaving the in-force; catches a decrement dropped or double-counted |
| `check_net_cf` | the printed statement adds to `net_cf` in every month; catches a claim limb with no column, or a claim expense folded into `expenses` |
| `check_claim_shape` | the claim-shape distribution sums to 1 and has mean 1; catches a shape that makes `reld_solved()` divide by the wrong denominator |
| `check_band_shares` | the five 요율 상대도 bands partition the contracts in every year |
| `check_relativity_neutral` | `Σ_b w_b r_b = 1` exactly while the discount cap is slack, and — once it binds — that the scheme never funds a discount it has not collected |
| `check_renewal_corridor` | neither priced unit moves more than ±25% a year against the **age-adjusted** prior premium; catches the loading applied on the wrong side of the clip |
| `check_annual_limits` | no money or count limit is exceeded — **wiring, not exercise** |
| `check_indemnity` | `claims_ann_pp(y) ≤ loss_incurred_pp(y)`: the claim never exceeds the incurred covered loss. The defining constraint of this product and of no other in the repository |
| `check_oop_ceiling` | `oop_incurred_ge(y) × oop_trunc(y) ≤ oop_ceiling()` — a statement about the **loss**, not about the benefit |
| `check_expense_split` | the three expense rates reconcile to the published 16% aggregate |

`tests/test_indemnity_medical_kr.py` is this model's own suite, and it asserts the notes'
worked example **hard-coded** as a module-level table rather than pickled, so a reviewer can
check it against [`technical-notes.md`](technical-notes.md) by eye:

- **The anchor cell's basis, value by value** — every frequency and severity row the notes
  print, `shape_mean() = 53,530.7924`, the ten `shape_rel` multiples, male `q(40) =
  0.00132019` and `mort_rate_mth(0) = 0.0001100825`, `lapse_rate_mth(0) = 0.0087416110`, and
  the ₩3,260,000 ceiling at decile 6.
- **The policy-year-1 cash flow statement**, all twelve printed rows to ₩0.0001 and
  `pols_if` to ten decimals, including `pols_if(12) = 0.8898237107`, together with the rows
  where the product does something — `t = 11, 12, 24, 36, 47, 48`.
- **The undiscounted totals**: ₩1,558,165.4328 of premium, ₩1,201,095.1706 of claims across
  the five limbs, **+₩118,475.9008** of net cash flow, a loss ratio of 0.770839, and the one
  negative policy year at **−₩276.1354**.
- **The renewal and experience-rating ledger** row by row: `reld_solved(2) = 0.957477` as a
  *solved* value, `reld_one(y) = 0.95` from year 5 where the cap binds, `reld_avg` reaching
  1.0095494, `noclaim_share = 0.5314584961`, and `prem_np_base(10) = 20,625.8505`.
- **Every entry in the notes' Known modeling pitfalls list**, one test each, named after the
  pitfall it protects — twenty-two of them, from multiplying a rate by the 보험가입금액 through
  the deductible on the mean, the ordering of the two 급여 reliefs, the corridor on the
  age-adjusted base, the relativity applied to the whole premium, the hard-coded 0.95, the
  one-year versus two-year lookback, the injection carve-out counted twice, the utilisation
  table read at the issue age, `lapse_rate` used on the monthly grid, the renewal decline
  folded into lapse, `reld_exempt_share` applied to the benefit, the `claims` subtotal
  column, the invented acquisition strain, and the premium re-read in year `y > 1`.
- **Each optional module in both positions** — the 비급여 rider, 3대비급여형, the relativity,
  the 무사고 할인, suspension at 0 and 3%, and `nhi_covered` in both branches.
- **The structural product facts**: that `claims_death`, `cv_pp` and `claims_lapse` do not
  exist; that `pols_maturity` is a count with no payment; that `t = 0` is positive; that
  `oop_trunc(y) ≡ 1` on the anchor and runs 0.801828 → 0.602441 on model point 8; that model
  point 10's 비급여 basis increment is clipped to exactly 0.25; and that every assumption row
  carries a provenance tag.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-indemnity_medical-r1
[R10]: #krlib-indemnity_medical-r10
[R12]: #krlib-indemnity_medical-r12
[R16]: #krlib-indemnity_medical-r16
[R17]: #krlib-indemnity_medical-r17
[R19]: #krlib-indemnity_medical-r19
[R2]: #krlib-indemnity_medical-r2
[R20]: #krlib-indemnity_medical-r20
[R3]: #krlib-indemnity_medical-r3
[R5]: #krlib-indemnity_medical-r5
[R6]: #krlib-indemnity_medical-r6
[R7]: #krlib-indemnity_medical-r7
[R8]: #krlib-indemnity_medical-r8
[R9]: #krlib-indemnity_medical-r9
[REG-R11]: #krlib-reg-r11
[REG-R13]: #krlib-reg-r13
[REG-R17]: #krlib-reg-r17
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R22]: #krlib-reg-r22
[REG-R23]: #krlib-reg-r23
[REG-R25]: #krlib-reg-r25
[REG-R3]: #krlib-reg-r3
[REG-R33]: #krlib-reg-r33
[REG-R38]: #krlib-reg-r38
[REG-R39]: #krlib-reg-r39
[REG-R4]: #krlib-reg-r4
[REG-R41]: #krlib-reg-r41
[REG-R44]: #krlib-reg-r44
[REG-R53]: #krlib-reg-r53
[REG-R54]: #krlib-reg-r54
[REG-R57]: #krlib-reg-r57
[REG-R60]: #krlib-reg-r60
[REG-R61]: #krlib-reg-r61
[REG-R8]: #krlib-reg-r8
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
