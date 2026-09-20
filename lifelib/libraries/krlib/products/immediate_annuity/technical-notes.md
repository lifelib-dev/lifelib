# Technical Notes

**Status:** Draft, 2026-09-03 (all cited sources accessed 2026-09-03).

**Scope note.** These notes specify the reference liability cash-flow projection model for
the standardized composite Korean single-premium immediate annuity, 즉시연금
(*jeuksi yeongeum*), defined in `product-spec.md` in this directory. They derive that
specification into arithmetic; where the two disagree the specification governs and this
document is wrong. This is not any single insurer's product, and no currently marketed
product bearing the name was located in the research pass — the caveat is stated once in
`product-spec.md` and is not repeated here.

[S#] tags refer to primary product documents — 약관 (*yakgwan*, policy conditions),
상품요약서 (*sangpum yoyakseo*, the statutory product summary), 상품안내장, 사업방법서
(*saeop bangbeopseo*, business method statement) and 공시 pages — and [R#] to
product-specific regulatory, judicial and statistical references; both are resolved in
`sources.md` here, with numbering carried verbatim from `_research/immediate-annuity.md`
and never renumbered. [REG-R#] tags resolve against the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R1–R62 numbering is
distinct from this product's. **[std]** marks a standardization introduced for the
reference implementation; each is also tagged in `product-spec.md` and carries a rationale
in the `provenance` column of the CSV it lives in. [unverified] marks a claim the research
pass could not confirm against a retrieved document. Parameter values are identical to
those in `product-spec.md`.

The model these notes are implemented as is **`Immediate_KR_S`**, on a **monthly** grid,
with every age in **보험나이** (*boheom nai*, insurance age). It is the library's
**payout-phase chassis**: the accumulation half of the same machinery is `Pension_KR_S`'s
subject, and the interest-crediting mechanic it shares with `WholeLife_KR_S` is specified
there and not redeveloped here. Amounts are in Korean won; because Korean documents quote
in 만원 (10,000) and 억원 (100,000,000), both forms are given where a Korean reader would
expect one — ₩100,000,000 (1억원).

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows for one immediate annuity
  in payment: the 생존연금 (*saengjon yeongeum*, survival annuity), the 사망보험금 (death
  benefit) on the two shapes that keep one, the 만기보험금 (*mangi boheomgeum*, maturity
  benefit) on the inheritance shape, the 해약환급금 (*haeyak hwanreupgeum*, surrender
  value) where surrender is permitted at all, the 모집수수료 (commission) and the expense
  load. Discounting, the 책임준비금, the 해약환급금준비금, the IFRS 17 CSM and the K-ICS
  요구자본 are **not** computed; see *Valuation and reserve pointers*.
- **The single premium is projected as income.** `premiums(0) = P` and nothing thereafter.
  That is not decoration: it is what makes the absence of acquisition strain a property of
  the printed statement. `check_premium_split()` asserts the identity A = B + C + D that
  the 약관 states in words [R1 §1-가](#krlib-immediate_annuity-r1) [S1 주2].
- **There is no premium term, so there is no lapse machinery of the usual kind.** 표준약관
  제26조's 납입최고 and 제27조's 부활 both presuppose a renewal premium that can go
  unpaid [REG-R25]; a single premium leaves nothing to miss. The only decrements are
  mortality and — on two of the three shapes — voluntary surrender. **A cited product
  feature, not an omission.**
- **Three shapes, three liabilities.** 종신연금형 (*jongsin yeongeum-hyeong*, life
  annuity), 상속연금형 만기형 (*sangsok yeongeum-hyeong*, inheritance annuity, term form)
  and 확정기간연금형 (*hwakjeong-gigan yeongeum-hyeong*, annuity-certain) are model point
  **columns of one projection**. Only the first uses mortality in its annuity: 「옵션 중
  사망(생존) 위험률이 적용되는 것은 종신형에 한정된다 … 확정형과 상속형은 사망률을
  사용하지 않는다」 [R12 §III-1](#krlib-immediate_annuity-r12).
- **Projection frequency and origin.** Monthly steps on a **0-based** time index. `t = 0` is
  the first policy month; period `t` runs from time `t` to time `t + 1`; row `t` of
  `result_cf()` carries month `t`; the single premium falls at time 0 on row 0; and **the
  annuity is payable in arrears**, so the payment shown on row `t` falls at the end of month
  `t`, on the 연금지급일. The contractual policy year is the derived 1-based label
  `policy_year(t) = t // 12 + 1`, never the index itself. `N = proj_len()` is the **number of
  projected months**, `12 x proj_years()` and the frame's exclusive end, so the frame is
  `t = 0 … proj_len() − 1` and `len(result_cf()) == proj_len()`: the anchor has 612 rows,
  `t = 0` to `t = 611`.
- **The monthly grid is the mode the market actually writes.** 연단위 pays from the first
  계약해당일 and 월단위 from one month after the 보장개시일, both published side by side by
  one carrier [S1 주1], and **monthly is the market default**. The model therefore pays the
  연금월액 (*yeongeum wolaek*, monthly annuity amount) a row and strikes it on a monthly
  annuity factor; `annuity_pp_annual(t)` publishes the 연금연액 (*yeongeum yeonaek*) a Korean
  illustration quotes, which is twelve times it. The earlier annual-grid model projected the
  연금연액 once a year and reconciled to the monthly mode through the standard
  `i / i^(12)` adjustment — worth 1.14% at 2.50% — on the argument that the deferred portions
  carry interest at the declared rate [S9 주11] [S8 주14]. **That reconciliation is exact only
  where no mortality enters the annuity**, which is the 확정기간연금형 alone; on the
  종신연금형 a monthly annuity also pays part-year instalments to a life that dies inside a
  policy year, so the monthly obligation is genuinely the larger one and the same fund buys
  1.06% less of it. The arithmetic is in the *Worked example*.
- **The declared rate steps twelve times a policy year in reality and once a year here.**
  The declared rate is the 공시이율 (*gongsi iyul*) and the floor under it the 최저보증이율
  (*choejeo bojeung iyul*): 「이 계약의 공시이율은 매월 1일 회사가 정한 이율로 하며,
  당월 말일까지 1개월간 확정 적용한다」 [S6 §9-나] [S1 주6] [S3] [S5] [S7 제7조]. The model
  carries one **annual** rate per policy year and credits its uniform-force monthly
  equivalent `j(t) = (1 + i(t))^(1/12) − 1` — a **[std]** approximation of the reset
  frequency, exact only where the rate is level, which on the representative basis it is.
  The same treatment runs through the decrements: `mort_rate` and `lapse_rate` are the
  **annual** figures the table and the assumption are stated in, and `mort_rate_mth` and
  `lapse_rate_mth` are `1 − (1 − q)^(1/12)`, level inside a policy year and stepping on each
  계약해당일, with twelve compounding back to the year's exactly. **The in-force at every
  계약해당일 is therefore the annual-step model's to the last printed digit.**
- **Age basis.** **보험나이** throughout: 만나이 at the 계약일 with a remainder under six
  months discarded and six months or more rounded up, incrementing on each 계약해당일
  [S7 제23조] [REG-R25 제21조](#krlib-reg-r25). 보험나이 increments on the 계약해당일, which is
  every twelfth period boundary on this grid, so the attained age is
  `age(t) = x + t // 12` exactly and no fractional-age interpolation is needed anywhere. It
  is **not** 만나이, which is what the public 완전생명표 and every Korean population statistic
  are published on [REG-R38] [REG-R39]; the six-month rule makes the two differ for half of
  all issue dates.
- **Model points and rounding.** Single-policy model points on an expected
  (probability-weighted) basis, `pols_if_init = 1.0`, so every monetary cells is per
  policy. No intermediate rounding anywhere; displayed figures are rounded independently.
- **Sign convention.** `liability_cf(t)` is the notes' `CF(t)`, total gross **outgo**.
  `net_cf(t)` is its exact negative, the library-wide **income-positive** orientation, and
  both are published as columns. `net_cf(0)` on the anchor is a large **positive** number,
  because the single premium is income.
- **What the model computes and what it does not.** It computes the 계약자적립액
  (*gyeyakja jeongnimaek*, the policyholder's account balance) and the 해약환급금, both
  contractual quantities defined by the 산출방법서 (*sanchul bangbeopseo*, the filed
  premium and reserve calculation basis) and bounded by a published schedule
  [REG-R19] [REG-R20]. It computes no reserve and no discounted result. **This is a
  mechanics demonstration, not a pricing or reserving result.**

---

## Model point attributes

One row of `model_point_table.csv` per contract, indexed by `point_id`. Ten are shipped;
`Projection[1]` is the anchor of the worked example below.

| Attribute | Type | Anchor value (`point_id = 1`) | Basis |
|---|---|---|---|
| `policy_id` | string | `IA-000001` | identifier only |
| `shape` | enum {`life`, `inheritance`, `certain`} | `life` — 종신연금형 | [S1] [S3] [S6] |
| `sex` | enum {`M`, `F`} | `M` | [S1 §IV-2] |
| `age_at_entry` x | int, **보험나이**, band 45–80 | **60** | [S1] [S2] [S3] [S4] [R27]; band **[std]** |
| `prem_pp` P | currency, 일시납보험료 | **100,000,000** (1억원) | [R12 그림3](#krlib-immediate_annuity-r12); adoption **[std]** |
| `annuity_term` n or g | int years | **10** — the 보증지급기간 | [R12 표7](#krlib-immediate_annuity-r12); adoption **[std]** |
| `retention_basis` | enum {`as_designed`, `as_ordered`} | `as_designed` (inert on this shape) | [R1] [R2] |
| `crediting_basis` | string, row set of `crediting_table.csv` | `decl_2017` | [S1 §IV-4] [S3] |
| `lapse_rate` w | float, **annual** surrender rate | **0.00** — surrender contractually impossible | [S3] [S5 주2] [S7 제31조] |
| `pols_if_init` | float | 1.0 | single-policy basis |

Four columns carry a product fact a reader from another market will not expect.
**`annuity_term` carries three contractual quantities under one name**, the arithmetic
treating them identically: the **보증지급기간** (*bojeung jigeup gigan*, guaranteed
payment period) on the life shape, the **보험기간** on the inheritance shape and the
**연금지급기간** on the certain shape; what differs is what the projection does *after* it.
**`lapse_rate` is an assumption in disguise**, and **no retrieved source gives a surrender
rate for 즉시연금 by duration or by shape at all** — it is carried per model point so that
its effect can be isolated, and on the life shape it is nil as a matter of **contract**
[S3] [S5 주2] [S7 제31조]. **`retention_basis` is the 즉시연금 과소지급 분쟁 in a column**,
meaningful on the inheritance shape alone; points 6 and 7 are the **same contract** on its
two settings. And **there is no `deferral_period`, no `payment_freq`, no
`escalation_rate` and no `mort_basis` switch**, each absence being a product fact: the
즉시형 has no deferral [S1] [S3] [S4], the monthly mode this model runs is the market
default and the 연단위 alternative is a mode rather than a contract variation, no retrieved
carrier offers indexation of any kind [S1]–[S9], and one mortality table serves as both the
pricing basis of the life shape and the decrement of all three.

### The ten shipped model points

`term` and `w` are in years, as the contract states them; `proj_len()` is in months.

| # | shape | sex / age | term | retention | crediting | w | `proj_len()` | premium |
|---|---|---|---|---|---|---|---|---|
| 1 | life | M 60 | 10 | — | `decl_2017` | 0.00 | 612 | ₩100,000,000 |
| 2 | life | F 60 | 10 | — | `decl_2017` | 0.00 | 612 | ₩100,000,000 |
| 3 | life | M 60 | 20 | — | `decl_2017` | 0.00 | 612 | ₩100,000,000 |
| 4 | life | M 45 | 10 | — | `decl_2017` | 0.00 | 792 | ₩10,000,000 |
| 5 | life | F 80 | 10 | — | `decl_2017` | 0.00 | 372 | ₩1,500,000,000 |
| 6 | inheritance | M 60 | 10 | `as_designed` | `decl_2017` | 0.02 | 120 | ₩100,000,000 |
| 7 | inheritance | M 60 | 10 | **`as_ordered`** | `decl_2017` | 0.02 | 120 | ₩100,000,000 |
| 8 | inheritance | F 70 | 20 | `as_designed` | **`min_guar`** | 0.02 | 240 | ₩100,000,000 |
| 9 | certain | M 60 | 10 | — | `decl_2017` | 0.02 | 120 | ₩100,000,000 |
| 10 | certain | F 55 | 30 | — | `decl_2017` | 0.00 | 360 | ₩5,000,000,000 |

The `proj_len()` column is the **number of projected months**, so point 1's 612 is
`t = 0 … 611` and point 6's 120 is `t = 0 … 119`; `proj_years()` carries the same horizon in
policy years.

Both sexes, the issue-age envelope 45 / 55 / 60 / 70 / 80, both guarantee lengths, both
retention bases, both crediting bases and all three shapes are covered; the premium
envelope runs from the ₩10,000,000 minimum [S2] [S3] [S4] [S5] through the ₩100,000,000
median and tax cap [R12] [REG-R58] and the age-banded 상속형 cap of ₩1,500,000,000
[S1 §II-5] to the ₩5,000,000,000 maximum [S1] [S5].

---

## State variables

Every one is a cells of `Projection` and every one is per policy. `av_pp`, `cv_pp` and
`pols_if` are stated at the **start** of the period, so a row of `result_pols()` reads as
the state the period opens in and the flows that period produces.

| Variable | Cells | Description | Updated |
|---|---|---|---|
| V(t) | `av_pp(t)` | 계약자적립액 at time t, before month t's crediting | monthly |
| CV(t) | `cv_pp(t)` | 해약환급금 = max(V(t) − 해약공제액, 0); nil on the life shape | monthly |
| l(t) | `lives_if(t)` | Probability the annuitant is alive at time t | monthly |
| σ(t) | `surr_if(t)` | Probability the contract has not been surrendered by time t | monthly |
| IF(t) | `pols_if(t)` | Probability a **payment obligation remains** at time t | monthly |
| d(t) | `pols_death(t)` | Deaths during month t | monthly |
| — | `pols_lapse(t)` | Surrenders during month t, after the deaths | monthly |
| — | `pols_exit(t)` | Obligations ending in month t, built independently of IF | monthly |
| F(t) | `payment_factor(t)` | Weight on the 생존연금 payable at the end of month t | monthly |
| A(t) | `annuity_pp(t)` | 연금월액 payable at the end of month t, before the weight | monthly |
| 12A(t) | `annuity_pp_annual(t)` | The 연금연액 it makes up, published and never paid | monthly |
| R(t) | `retention_pp(t)` | 만기보험금 지급재원 retained out of month t's interest | monthly |
| i(t) | `crediting_rate(t)` | **Annual** Max[공시이율, 최저보증이율] for the policy year | yearly |
| j(t) | `crediting_rate_mth(t)` | `(1 + i(t))^(1/12) − 1`, the rate the fund actually rolls on | monthly |
| q(t) | `mort_rate(t)` | **Annual** 개인연금사망률 at the attained 보험나이 | yearly |
| q^m(t) | `mort_rate_mth(t)` | `1 − (1 − q)^(1/12)`, the decrement actually applied | monthly |
| w(t) | `lapse_rate(t)` | **Annual** [std] surrender rate | yearly |
| w^m(t) | `lapse_rate_mth(t)` | `1 − (1 − w)^(1/12)`, the decrement actually applied | monthly |
| v(t) | `disc_factor(t)` | PV at inception of ₩1 at time t on the crediting path | monthly |

**`pols_if` is not a policy count and it is not a survival probability**, and the model
says so in that cells' own docstring, using the phrase *payment obligation remains*. Within
the 보증지급기간 the instalments are due whether or not the annuitant lives —
「종신연금형의 경우 연금지급 개시 후 보증지급기간안에 사망시에는 잔여보증지급기간 동안,
미지급된 연금월액을 매월 연금지급일에 드립니다」 [S3] [S1 주5] — so there the obligation
is the *greater* of the survival probability and the guarantee indicator. On the certain
shape it is one until the term ends or the contract is surrendered [R12 §III-1](#krlib-immediate_annuity-r12) [S9 별표1];
on the inheritance shape it is survival and persistency together, because **death itself
triggers a payment** and ends the contract [S1] [S3]. The name is lifelib's and is kept
because it is what the rest of the library weights expense by; the meaning is IF(t).

**A(t), R(t) and V(t) are deterministic given the assumption set.** The annuity level does
not depend on survival on any of the three shapes: only the *weights* F(t) and IF(t) do.
That separation is what lets the whole of the retention arithmetic below be checked with a
calculator against a table of pure interest.

---

## Assumption inputs

Three classes, following the house arrangement. The first is what the contract promises;
the second is what the insurer may change and does; the third is the modeller's own view
and on this product it is thin, entirely unsourced, and says so.

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Premium mode | Single premium (일시납), once at inception; no renewal premium, no 추가납입 on the 즉시형 | [S1] [S2] [S3] [S5] [S6] |
| Premium split | A = 보장계약 보험료 B + 사업비 C + 연금계약 순보험료 D; D becomes the opening 계약자적립액 | [R1 §1-가](#krlib-immediate_annuity-r1) [S1 주2] |
| 계약체결비용 | **2.20%** of P, deducted once at inception | [S1 §VIII]; adoption **[std]** (i) |
| 계약관리비용 | **1.30%** of P, deducted once at inception | [S1 §VIII] |
| Total one-off load c | **3.50%** of P | [S1] [S3]; adoption **[std]** (i) |
| 위험보험료 b | **0.00%** (life); **1.47%** of P (inheritance, certain), once at inception | [S1 §VIII]; adoption **[std]** (ii) |
| Opening fund V(0) | P (1 − c − b): **96.50%** of P on the life shape, **95.03%** on the other two | derived; **[std]** (iii) |
| Accumulation rule | V(t+1) = V(t)(1 + i(t)) − A(t), 「연금개시후에는 생존연금 발생분을 차감한 금액」 | [R1, quoting the 약관 서두](#krlib-immediate_annuity-r1) |
| Crediting rule | i(t) = **Max[공시이율, 최저보증이율]** | [R2 §1](#krlib-immediate_annuity-r2) [S7 제7조] |
| 최저보증이율 exists at all | Compulsory: 감독규정 제7-60조제10호 requires a 금리연동형보험 to set a 최저보증이율 or a 최저보증금액 | [REG-R16] |
| 종신연금형 annuity | 연금개시시의 계약자적립액 ÷ an annuity factor on the 개인연금사망률 and the 공시이율, for life, guaranteed for g | [S7 별표1] [S1] |
| 보증지급기간 g | **10 years**; menu 10 / 20 / 100세 / 기대여명 | [R12 표7](#krlib-immediate_annuity-r12); representative **[std]** |
| Guarantee is a floor, not a stream | Unpaid guaranteed instalments continue on their original dates whether or not the annuitant lives | [S3] [S1 주5] [S7 별표1] |
| 상속연금형 만기형 annuity | Interest on the fund **less the 만기보험금 지급재원** | [R2 §1](#krlib-immediate_annuity-r2) [S7 별표1] [R1] |
| 만기보험금 M | **The gross single premium**, 「만기보험금 : 납입 보험료 총액」 | [R1 §1-가 각주2](#krlib-immediate_annuity-r1) [S1] |
| 확정기간연금형 annuity | 계약자적립액 ÷ an annuity-certain factor over the elected term, payable irrespective of survival | [S3] [S9 별표1] [R12 §III-1](#krlib-immediate_annuity-r12) |
| 사망보험금 ρ | **Nil** on the life shape after annuitisation; **10% of P** plus the fund on the inheritance shape; 10% of P alone on the certain shape | [S5] [S1] [S3] [R1 별표1(2)](#krlib-immediate_annuity-r1) |
| Why the death benefit may be so small | 감독규정 제7-60조제9호's premiums-paid floor excepts contracts after annuity payments have begun; 제7호's 최저사망보험금 excepts annuities | [REG-R16] |
| 해약공제액 | **Nil at every duration** — a published run of zeros, not an assumption | [S1 §VIII] [S10] |
| 해약환급금 | 계약자적립액 less the 해약공제액, floored at zero | [REG-R19 제7-66조제1항제1호](#krlib-reg-r19) [S1 §VI-1] |
| Surrender — life shape | **Impossible** once the annuity is in payment, i.e. from month one on an immediate annuity | [S3] [S5 주2] [S7 제31조] [S8 제33조] |
| Surrender — other two shapes | Permitted at any time before the contract is extinguished | [S1] [S3] [S6] |
| 선지급 (commutation) | Unpaid guaranteed or remaining certain instalments as a lump sum discounted at the **공시이율**, once a year, in whole years | [S3] [S5 주8] [S7 제11조제3항] [S9] |
| Mortality ratchet | Inert: no interval between issue and annuitisation for a table revision to land in | [S6 §10-라]; reasoning **[std]** |
| 100.1% fund floor | Recorded and **not** applied — a deferred-contract mechanic | [S7 별표1 주8] [S9]; non-adoption **[std]** (iv) |

(i) [S1 §VIII] publishes the load by component **and by shape** on a 남자 60세, 일시납
₩50,000,000 basis: 종신연금형 2.61% + 1.30% = 3.91%, 상속연금형(20년만기) 2.19% + 1.30%
= 3.49%. The composite adopts a single **2.20% + 1.30% = 3.50%** across all three shapes
**[std]** rather than carrying the carrier's 0.42-point allocation difference, because a
second, independent document supports the same total: solving the annuity-certain identity
against 교보's four published 확정기간연금형 figures at a 공시이율 of 2.52% reproduces all
four terms within 1.4% on a total first-day deduction of 4.97% [S3]. Two carriers, two
documents, one number. The disputed 2012 contract's 사업비 was **5.325%** [R1 §1-가](#krlib-immediate_annuity-r1), with
the supervisor assuming 6.0% in total [R2 참고](#krlib-immediate_annuity-r2); that vintage is recorded in
`product-spec.md` and is not defaulted.

(ii) [S1 §VIII] publishes three levels on one basis: **0.00%** for 종신연금형 1형, which
pays no death benefit once the annuity has begun; **4.9466%** for 종신연금형 2형, which
keeps one for life; and **1.4669%** for 상속연금형(20년만기). The composite's life shape is
the 1형 design. The 1.47% is disclosed on a **twenty-year** basis at exactly the anchor age
and is applied **unscaled** to a ten-year contract, which is conservative — the true
ten-year risk premium is lower — and the direction of the error is stated rather than
corrected, no source supporting a term scaling. The certain shape carries the same figure
because no carrier publishes one for it: a second **[std]**.

(iii) 100% − 3.50% = 96.50% and 100% − 3.50% − 1.47% = 95.03%. The identity is the one the
약관 states in words: 「연금계약적립액이란 … 연금계약순보험료(사망보장이 있는 경우
납입하신 보험료중 보장을 위한 보험료 및 예정사업비를 차감한 금액)를 공시이율로
납입일부터 일자계산에 의하여 적립한 금액」 [R1, quoting the 약관 서두](#krlib-immediate_annuity-r1) [S1 주2].

(iv) Two carriers guarantee that the 계약자적립액 at annuitisation is at least **100.1%**
of premiums paid [S7 별표1 주8] [S9]. Both statements are made in **deferred** contracts,
where there is an accumulation period in which to earn the guarantee. Applying it here
would erase the whole 3.50% load on day one, and no retrieved 즉시연금 document states
such a floor. The inference that it is a deferred-contract mechanic rather than a
supervisory floor the immediate products silently breach is **[unverified]**, the
regulation behind it never having been retrieved [R31].

### (b) Insurer-discretionary current elements

This class is where the whole of the product's variability lives, and it is small enough
to print.

| Input | Value | Basis |
|---|---|---|
| 공시이율 i_d | **2.50%** a year, reset on the first of each month and fixed for that month | [S1 §IV-4] [S12] [S14] [REG-R48]; adoption **[std]** (v) |
| 최저보증이율 i_g(t) | **1.25%** in policy years 1–5, **1.00%** to year 10, **0.75%** thereafter | [S3]; adoption **[std]** (vi) |
| 모집수수료 κ | **2.00%** of P at t = 0, nil thereafter | [S1 §VII]; adoption **[std]** (vii) |
| 연금수령기간 중 비용 φ | **0.80% of the 연금연액** each year in payment | [S1 §VIII]; treatment **[std]** (viii) |
| Large-contract discount | Not applied | [S6 §10-나] [R27]; scope **[std]** |

(v) Observed declared rates on annuity money: 4.8% at 2011-09 [R27]; 4.5% at 2012-09 on
the disputed contract [R1 §1-라](#krlib-immediate_annuity-r1); 3.40% falling to 2.80% over 2015-03 to 2016-03 [S5];
2.95% at 2016-03 [S4]; 2.83% at 2016-03 [S2]; **2.50% at 2017-04** [S1 §IV-4]; 2.52% at
2017-12 [S3]; 2.80% at 2023-01 [S13]; 2.55% at 2025-01 [S12]; 2.67% at 2026-04 [R28];
2.56% at 2026-09 [S14]. 2.50% is the level the anchor carrier declared on this exact
product and equals the **평균공시이율 for 2026** [REG-R48]; it sits 5 to 17 basis points
**below** the 2.55%–2.67% band of the three most recent observations, and that direction
is recorded rather than smoothed.
**No model in this library derives a Korean declared rate and none should.** 감독규정
제7-65조제3항 makes it the product of a 공시기준이율 and a 조정률, with 시행세칙 별표 27
building the 공시기준이율 as

```
공시기준이율 = 객관적 외부지표금리 x α + 운용자산이익률 x (1 − α),   α <= 60%
```

so it is majority-weighted to the insurer's own realised investment return
[REG-R18] [REG-R24], and the two carriers that publish their weighting publish different
ones — 50/50 with an 80–120% corridor at ABL [S6 §9], 40/60 with a 조정율 of 89.16% at
NH농협 [S12], 35/65 on the disputed 2012 약관 [R1]. The rate is exposed here as a
**scalar**, and `decl_rate()` raises if the shipped table gives more than one value within
a basis.

(vi) Observed schedules by vintage run from 2.5% / 2.0% for the 2007–2014 cohorts [S10] to
1.0% / 0.75% / 0.50% — reaching its terminal step after only five years — at 한화 in 2024
[S7 제7조]. The 교보 2017 schedule **1.25% / 1.00% / 0.75%** is adopted for one reason only:
it is the only three-step schedule published on a contemporaneous 즉시연금 illustration
whose annuity figures this document also uses [S3]. **It is not a middle of the observed
range.** Against the five schedules retrieved for 2017–2026 it is the joint-highest opening
step and the highest terminal step — 0.75% against the 0.50% 하나 (2023), 한화 (2024) and
IBK (2026) all step down to — so the adopted floor sits at the generous end of the current
market, and far under the 2.5% / 2.0% of the 2007–2014 cohorts [S10]. It is inert on the
representative basis and bites on model point 8 alone. **Note what the floor is not: it is
a rate on the fund, never a floor on
the annuity.** That single sentence is the substance of the whole dispute, and model point
8 is the model point that demonstrates it.

(vii) Observed: **2.08%** of P in year one on 종신연금형 and **1.75%** on 상속연금형, nil
in every later year, on a 남자 60세 일시납 1억원 basis [S1 §VII]. 2.00% is a **round figure
inside that pair** and not their mid-point, which is 1.915% **[std]**. What matters
structurally is not the level but that it sits **below**
the 2.20% 계약체결비용, so the acquisition charge taken from the fund at inception covers
the commission paid out of it at the same moment. Every retrieved figure is a
first-year-only rate on a bancassurance sale [S2] [S3] [S4] [S5].

(viii) [S1 §VIII] states the charge as 「연금수령기간 중 비용 — 연금연액의 0.80%」 on all
three shapes and discloses it in the **cost** table rather than the benefit table. The
composite therefore models it as an insurer expense measured on the 연금연액 and does
**not** net it off the policyholder's payment. Whether a carrier's own 산출방법서 builds
it into the annuity factor instead is **[unverified]**: no filed basis document for an
즉시연금 discloses the annuity formula, and [S6], the one 사업방법서 retrieved, does not
reach it.

### (c) Behavioral / experience assumptions (modeler's view — all [std])

| Input | Recommended basis | Basis tags |
|---|---|---|
| Annuitant mortality | A **[std]** Makeham construction on three published anchors; **not** the 경험생명표 | [S1 §IV-2] [REG-R33] [REG-R34]; **[std]** (ix) |
| Limiting age ω | **110**, with q(110) = 1 | **[std]** (x) |
| Mortality improvement | **None applied**, and none should be | **[std]** (xi) |
| Best-estimate vs pricing table | **One table serves both**, on this product only | **[std]** (xii) |
| Surrender rate w | **2.00%** a year on the inheritance and certain shapes; **nil** on the life shape as a matter of contract; **nil in the final period on every shape** | [S3] [S7 제31조]; level **[std]** (xiii) |
| Maintenance expense | **None per policy.** The only recurring charge any retrieved document publishes is measured on the annuity | [S1 §VIII]; **[std]** (xiv) |
| Expense inflation | **None** | **[std]** (xiv) |
| Commutation (선지급) | Right recorded, exercise **not modelled** | [S3] [S5 주8] [S7]; **[std]** (xv) |
| Acquisition strain | **None, by construction**: `acq_expense_rate` = load − commission | **[std]** (xvi) |

(ix) **The 제10회 경험생명표 (*gyeongheom saengmyeongpyo*, KIDI experience life table),
applied from April 2024, is produced by 보험개발원 and is not published in full.** Only
summary statistics are released — 평균수명 남 86.3세 / 여 90.7세 and 65세 기대여명 남
23.7년 / 여 27.1년 — and they reach this library through a trade newspaper rather than
through KIDI itself [REG-R33] [REG-R34]. There is therefore **no Korean annuitant table to
transcribe**; `mort_table.csv` is a **[std]** construction with a `provenance` column on
every row, set out under *The mortality construction* below, and the constraint that
governs everything about it is that **it must never be presented as the 경험생명표.**
Substituting a filed basis means replacing the CSV with a same-schema file keyed on the
same `(sex, age)` in 보험나이. No formula changes.

(x) No retrieved Korean source states a limiting age for an annuitant table. ω = 110 with
q(ω) = 1 is **[std]** and is what makes the life shape's obligation *exhausted* rather
than truncated: `lives_if(51) = 0` on the anchor, so the last row's payment weight is
exactly zero and nothing is thrown away at the horizon.

(xi) The table is a **period** construction on published anchors and carries no trend, and
none is added, because none of the three anchors is dated as a cohort quantity. Adding an
improvement scale, or substituting a generational basis, is a change to the CSV's schema
and not to a formula. This is the opposite posture from `frlib`'s `Rente_FR_S`, whose
mandatory tables are generational and where an improvement factor would double-count.

(xii) The pricing basis and the best-estimate basis are the **same table** here, and
`pricing_factor(t)` and `payment_factor(t)` are written as two separate constructions of
the same weight so that `check_annuity_basis()` compares two things rather than one with
itself. Defensible — no carrier publishes an annuitant table at all, so a second one would
be a second invention — but a real limitation: the model shows **no mortality margin** on
the life shape, and a production basis would separate them.

(xiii) **No retrieved source gives a surrender rate for 즉시연금 at all.** 2.00% is a round
placeholder. Nil in the final period on every shape is a modelling decision: a contract in
its last year runs to its 만기보험금 or its last instalment, and a lapse decrement there
would divert the maturity benefit into a surrender value of the same amount for no reason
any contract states. Note the interaction that makes even a nil assumption defensible on
the inheritance shape: the 만기보험금 equals the **gross** premium while the surrender
value is below it at every duration before maturity [S1 §VI-2], so surrendering early is a
realised loss on a contract bought to be held.

(xiv) There is no maintenance expense per policy and no expense inflation. The one
recurring charge any retrieved 즉시연금 document publishes is φ, measured on the annuity —
not per policy and not per 만원 of fund — and inventing a per-policy expense beside it
would be a number with no source at all. On the anchor the insurer's whole recurring
expense is therefore **0.80% of what it pays out**: read that column as a charge, not as a
cost study.

(xv) The 선지급 right — the unpaid guaranteed or remaining certain instalments taken as a
lump sum discounted at the 공시이율, available on death and on request, once a year and in
whole years [S3] [S5 주8] [S7 제11조제3항] — is **recorded and not exercised**. The
projection pays the guaranteed instalments on their contractual dates. That is
value-neutral **only because the 약관's discount rate is the same 공시이율 that sets the
annuity** [S1 주4] [S3] [S5] [S7] [S9]; the option has real value on a falling-rate path
and none on a rising one, and this model does not price it.

(xvi) `acq_expense_rate` = 3.50% − 2.00% = **1.50%** is a *treatment*, not a disclosure. It
sets the insurer's own acquisition and administration expense equal to the charge it took,
which is what makes `check_premium_split()` close and what makes "no acquisition strain" a
property of the statement rather than a claim in prose.

---

## Cash flow components and recursions

### Notation

| Symbol | Meaning |
|---|---|
| t | **month** index from inception, 0-based; period t runs from time t to time t + 1; t = 0, 1, …, N − 1 |
| N | `proj_len()`, the **number** of projected months — the frame's exclusive end, `12 x proj_years()`; rows run 0 … N − 1 |
| x, x + t//12 | 가입나이 and attained age, both **보험나이** |
| P | 일시납보험료, the single premium |
| n | 보험기간 (inheritance) or 연금지급기간 (certain), in **years**; 12n months |
| g | 보증지급기간 (life), in **years**; 12g months, which is `annuity_term_mths()` |
| c, b | one-off expense load and 위험보험료, as shares of P |
| B | 보장계약 보험료 = P b |
| κ, ε | 모집수수료율 and the insurer's own acquisition expense rate, both on P |
| φ | 연금수령기간 중 비용, as a share of the 연금연액 |
| ρ | 사망보험금 as a share of P (0 or 0.10) |
| V(t) | 계약자적립액 at time t, before period t's crediting |
| CV(t) | 해약환급금 at time t |
| M | 만기보험금 |
| i_d, i_g(t), i(t) | 공시이율, 최저보증이율 for the policy year containing t, and their max — all **annual** |
| j(t) | `(1 + i(t))^(1/12) − 1`, the monthly rate the fund rolls on |
| q(x + t//12) | **annual** 개인연금사망률 at the attained age |
| q^m(t) | `1 − (1 − q)^(1/12)`, and `1/(12 − t mod 12)` where q = 1 |
| l(t), σ(t) | survival and persistency probabilities at time t |
| w, w^m(t) | **annual** surrender rate, and its monthly conversion |
| IF(t) | probability a payment obligation remains at time t |
| d(t) | deaths in month t |
| F(t) | weight on the payment falling at the end of month t |
| A(t) | 연금월액 payable at the end of month t, before the weight |
| R(t) | 만기보험금 지급재원 retained out of month t's interest |
| a(m, j), s(m, j) | annuity-certain and accumulation factors, ₩1 a **month** in arrears over m months |
| ä(x, g, j) | the 종신연금형 factor at commencement, a **monthly** annuity factor |
| v(t) | PV at inception of ₩1 at time t on the crediting path |
| CF(t) | total gross liability outgo in month t |

Dimensional check: P, B, V, CV, M, A, R and every flow are currency; c, b, κ, ε, φ, ρ,
i, j, q, q^m, l, σ, w, IF, F and every factor are dimensionless; a, s, ä and v have
dimensions of months and of pure number respectively, and A × a is currency. Every flow
below is currency per month per policy.

### The premium split at inception

The single premium is divided once and never again [R1 §1-가 각주2](#krlib-immediate_annuity-r1):

```
B    = P b                              보장계약 보험료
C    = P c                              사업비, of which P κ is paid out as commission
                                        and P ε is the insurer's own expense
V(0) = P (1 − c − b)                    연금계약 순보험료 = the opening 계약자적립액
```

with, on the representative basis, `V(0) = 0.9650 P` on the life shape and `0.9503 P` on
the other two. `check_premium_split()` asserts `P = P κ + P ε + B + V(0)` with nothing
left over in either direction. **That identity is the statement that this product has no
acquisition strain**, and it is the structural difference between `Immediate_KR_S` and
every other model in `krlib`: there is no unamortised 신계약비 to recover, which is why
the 해약공제액 can be nil at every duration without the insurer giving anything away
[S1 §VIII] [S10], and why the statutory 표준해약공제액 cap of 별표 14 binds nothing here
[REG-R20].

### The crediting rate

```
i_g(t) = the min_guar_rate of the row whose half-open band [dur_from, dur_to)
         contains t, within the contract's crediting_basis
i(t)   = Max[ i_d , i_g(t) ]
```

The bands are published in **completed policy years** and the grid counts months, so the
band test is on `t // 12`: `t = 0 … 59` is the first band, `t = 60 … 119` the second,
`t >= 120` the third — the floor steps on the 계약해당일 and is level across the twelve
months between. On the representative basis `i_d = 2.50%` exceeds every step of the floor,
so **i(t) is level at 2.50% and the floor is inert**; `check_rate_level()` asserts exactly
that on the life shape, where the model relies on it. On the `min_guar` basis `i_d` is set
to zero, so the Max resolves to the floor at every duration and the stepping is exercised.
The fund is credited at the monthly equivalent

```
j(t) = ( 1 + i(t) )^(1/12) − 1
```

so twelve months compound back to the year's declared rate exactly — 0.2059836% a month at
2.50% **[std]**. The same uniform-force conversion turns the annual 개인연금사망률 and the
annual [std] surrender rate into the monthly decrements the projection applies:

```
q^m(t) = 1 − ( 1 − q(x + t//12) )^(1/12)      and 1/(12 − t mod 12) where q = 1
w^m(t) = 1 − ( 1 − w )^(1/12)
```

Twelve monthly exits compound to the year's rate, so **the in-force at every 계약해당일 is
the annual-step model's to the last printed digit**: `lives_if(120)` = 0.953470025140 on
the anchor, which is the annual grid's `lives_if(10)`. At the limiting age `q = 1`, which
cannot be converted that way, so the certain death is spread uniformly over the twelve
months of that policy year and the last of the in-force leaves in the final month of the
frame rather than all at once on the 계약해당일.

`min_guar` is a **modelling device and not a product** — no carrier sells a contract with
a nil declared rate. It is carried because a guaranteed-rate-only projection is the kind of
basis on which the anchor carrier publishes its 해약환급금 run [S1 §VI-2] — though at [S3]'s
floor levels and not at that carrier's own 1.5% / 1.0% — and because without it no shipped
model point would exercise the duration bands at all.

### The mortality construction

The three published anchors are the six 개인연금사망률 (*gaein yeongeum samangnyul*) rates
of [S1 §IV-2] — 0.00225 / 0.00353 / 0.00728 for men and 0.00097 / 0.00118 / 0.00251 for
women at 보험나이 50 / 60 / 70 — and the 65세 기대여명 of the 제10회 경험생명표, 남 23.7년
/ 여 27.1년 [REG-R33] [REG-R34]. `mort_table.csv` is built from them by a Makeham law
**[std]**:

```
mu(x) = A + B c^(x − 60)
q(x)  = 1 − exp(−mu(x))   for x < 110,        q(110) = 1
```

with three parameters fitted to **three** constraints, so there is no free choice left:

| | A | B | c |
|---|---|---|---|
| M | 0.002541101055 | 0.000995144096 | 1.169559983738 |
| F | 0.000957743344 | 0.000222953404 | 1.214403844358 |

The constraints are q(60) and q(70) at their published values, reproduced **exactly**, and
the complete 65세 기대여명 — the curtate sum from 65 to 110 plus one half — reproduced
exactly at 23.7 and 27.1 years. The **residual is the third published anchor, at
보험나이 50**, and it is reported rather than smoothed away: the fit gives 0.0027451336
against a published 0.00225 for men, **+22.01%**, and 0.0009892120 against 0.00097 for
women, **+1.98%**. That deviation is stated in the `provenance` cell of those two rows and
it is stated here. A three-parameter law that reproduces two rates and a life expectancy
exactly cannot also reproduce a third rate, and the honest thing is to say which one it
missed and by how much.

Selected constructed rates, and the expectations of life the shipped table produces (all
complete, the **annual** curtate sum to age 110 plus one half, which is how the fit's
constraint is stated; the two bold figures are fit anchors and are exact by construction).
The projection's own monthly survival sum divided by twelve gives 28.2208 for `e(60)`
rather than 28.1914 — the same quantity read off the monthly grid, the two differing by the
uniform-death approximation inside each policy year:

| age | q(x), M | q(x), F | | expectation | M | F |
|---|---|---|---|---|---|---|
| 50 | 0.0027451336 | 0.0009892120 | | e(60) | 28.1914 | 31.9090 |
| 60 | 0.0035300000 | 0.0011800000 | | e(65) | **23.7000** | **27.1000** |
| 70 | 0.0072800000 | 0.0025100000 | | e(70) | 19.2968 | 22.3281 |
| 80 | 0.0250432520 | 0.0117394669 | | | | |
| 90 | 0.1058003527 | 0.0737951746 | | | | |
| 100 | 0.4089670957 | 0.4108568270 | | | | |
| 110 | 1.0000000000 | 1.0000000000 | | | | |

Note the gap the table is reproducing:
the 국가데이터처 완전생명표 gives a 65세 기대여명 on **만나이** of 남 19.5년 / 여 23.7년
[REG-R38], so the annuitant table sits about **4.2 years** above the population for men
and **3.4** for women at that age — which is the insured-versus-population margin any
annuitant basis must carry, and is the single strongest reason a Korean immediate-annuity
model may not be run on 완전생명표 rates.

The decrement then runs

```
l(0) = pols_if_init,          l(t) = l(t − 1) (1 − q^m(t − 1))
```

so the rate applied in month `t` is the monthly conversion of the annual rate at the age
attained at the **start of the policy year** that month falls in.
`check_lives_roll_fwd()` rebuilds the same probability as an explicit product of
(1 − q^m) with no reference to the recursion, which is what catches an off-by-one.

### The three annuity constructions

**Life — struck once, level thereafter.**

```
ä(x, g, j) = SUM over t = 0 … N − 1 of  v^(t+1) max[ l(t+1)/l(0) , 1{t + 1 <= 12g} ]
A(t)       = V(0) / ä(x, g, j(0)),   the same value at every t
```

with `v = 1/(1 + j(0))`, so it is a **monthly** annuity factor — about twelve times an
annual one, 239.234686 against the annual grid's 19.502675 on the anchor — and the
instalment it produces is the 연금월액 the contract pays. **No `(f − 1)/(2f)` frequency
correction appears anywhere**, because the frequency is the grid rather than an adjustment
to it. The `max` is the whole point: within the 보증지급기간 the instalment is due whether
or not the annuitant lives, so the guarantee is a **floor on the obligation** and not a
second stream; an additive construction would price 1 + l(t+1) for the whole guaranteed term
and buy an annuity 30% too small (pitfall 2). The sum runs over **exactly the months the
projection carries**, so the pricing and the projection cannot drift apart. The annuity is struck at `i(0)` and never recomputed, which is a **[std]**
reading and needs its warrant stated: [S1 주3] says the 생존연금 moves with the declared
rate — 「공시이율이 변경되면 생존연금도 변경됩니다」 — but the 약관 bases the life-shape
annuity on 「연금개시시의 계약자적립액」, the fund *at commencement* [S7 별표1], and the
mortality ratchet that would otherwise revise it is inert on an immediate annuity
[S6 §10-라]. `check_rate_level()` holds every life-shape point to the level rate this
reading assumes. `annuity_factor()` is **defined on the life shape alone and raises on the
others**, which is 「확정형과 상속형은 사망률을 사용하지 않는다」 [R12 §III-1](#krlib-immediate_annuity-r12) in code.

**Inheritance — interest less the retention, recomputed every month.**

```
R(t) = ( M − V(t) ) / s(12n − t, j(t))          as_designed
     = 0                                        as_ordered
A(t) = V(t) j(t) − R(t)
```

The identity behind it: the level annuity that carries the fund from V(0) to M over 12n
months is `A = [V(0)(1+j)^(12n) − M] / s(12n, j)`, and because
`(1+j)^(12n) = 1 + j·s(12n, j)` that decomposes **exactly** into

```
A = V(0) j     −     (M − V(0)) / s(12n, j)
    ─────────        ────────────────────
    interest         만기보험금 지급재원 (the retention)
```

so the fund follows `V(t) = V(0) + R s(t, j)` and reaches M precisely at t = 12n. Writing
it with V(t) and the remaining term `12n − t` rather than with V(0) and 12n is what makes it
right on a **stepping** rate: R is re-struck every **month** against the fund actually
accumulated, so the fund still lands on M however the rate has moved — model point 8 is
where that matters, and `check_av_roll_fwd()` asserts the reduced form
`V(t) = V(t−1) + (M − V(t−1))/s(12n − t + 1, j)`. **Both terms move against the
policyholder when the rate falls**: the interest falls with j, and the retention *rises*,
because s shrinks. That is why an annuity on this shape can fall by more than half while the
guaranteed floor never moves, and it is the arithmetic the whole dispute is about.

**Certain — the fund divided over the remaining term.**

```
A(t) = V(t) / a(12n − t, j(t))
```

recomputed every month, again so that a moving rate is handled exactly. The fund runs off
as `V(t) = V(t−1) a(m−1, j)/a(m, j)` with `m = 12n − t + 1`, which exhausts to zero at the
end of the last month without being told to; `check_av_terminal()` asserts it.

### The fund recursion

One recursion serves all three shapes, and it is the 약관's own [R1, quoting the 약관 서두](#krlib-immediate_annuity-r1):

```
V(0)     = P (1 − c − b)
V(t + 1) = V(t) (1 + j(t)) − A(t)
CV(t)    = 0                            life shape — surrender is impossible
         = max( V(t) − 해약공제액 , 0 )   = V(t), the deduction being nil
```

What the fund *means* differs by shape and this is worth stating plainly, because it is
where an implementation goes wrong quietly. On the inheritance shape V climbs to M at
maturity under `as_designed` and stands still at V(0) under `as_ordered`. On the certain
shape it exhausts to zero. **On the life shape it is neither**: a life annuity's fund is
not its reserve, and the recursion runs **negative** at about the point where the
annuitant has outlived the factor the fund bought — on the anchor between t = 324 and
t = 330, inside the twenty-eighth policy year, which the monthly grid dates properly where
an annual grid could only place it at a boundary. That is
published, not suppressed: `cv_pp` is nil there, nothing downstream reads the negative
value, and `check_av_terminal()` returns True on that shape *by design* rather than by
tolerance, with `check_annuity_basis()` holding the shape to its basis instead.

### Decrements, the obligation measure and the payment weight

```
σ(0) = pols_if_init,        σ(t) = σ(t − 1) (1 − w^m(t − 1))
w(t) = 0                    on the life shape, and for t >= N − 12 on every shape
     = the model point's lapse_rate otherwise

d(t)         = l(t) σ(t) q^m(t)                               deaths in month t
pols_lapse(t)= 0                                              life
             = σ(t) w^m(t)                                    certain
             = l(t) (1 − q^m(t)) σ(t) w^m(t)                  inheritance
```

Surrenders are taken **after** the deaths, which is why the inheritance branch carries the
`(1 − q^m)` and the certain branch does not: on the certain shape the contract survives the
annuitant, so the surrender decrement bites on the persistency measure alone. The surrender
rate is suppressed over the **whole final policy year** rather than the final month, which is
what makes the monthly in-force reproduce the annual-step model's at every 계약해당일.

The obligation measure and the payment weight are then

```
IF(t) = max( l(t) , 1{t < 12g} )      life
      = σ(t)                          certain
      = l(t) σ(t)                     inheritance

F(t)  = max( l(t+1) , 1{t+1 <= 12g} ) life
      = σ(t)                          certain
      = IF(t) (1 − q^m(t))            inheritance
```

Four things to notice. **IF and F are offset by one month**, because the payment falls at
the *end* of the month. **The survival term the guarantee floor is maxed against differs
between them** — `l(t)` in IF, `l(t + 1)` in F — under one and the same guarantee window:
`t < 12g` and the `t + 1 <= 12g` written in F are the same test on integers, and both
readings of it are right, because the obligation is open at time t for t = 0 … 119 on a
ten-year guarantee and the 120 instalments the guarantee covers fall at the ends of months
0 … 119. **On
the certain shape survival is irrelevant to both** [R12 §III-1](#krlib-immediate_annuity-r12). And **on the inheritance
shape the 생존연금 is payable 「살아있을 때」**, so F carries a further year of survival,
the death benefit taking the place of the payment for those who die.

`pols_exit(t)` is built from the decrements **and the guarantee**, independently of IF, so
that the two can be compared:

```
pols_exit(t) = 0                        life,     t < 12g − 1
             = IF(0) − l(12g)           life,     t = 12g − 1
             = d(t)                     life,     t > 12g − 1
             = pols_lapse(t)            certain
             = d(t) + pols_lapse(t)     inheritance
```

The life branch is the shape's characteristic feature: **a death inside the 보증지급기간
does not end the obligation**, so nothing exits at all until the guarantee expires, and
then everyone who died inside it exits at once, in a single step at t = 12g − 1. An
implementation that decremented the obligation on every death would show a residual in
`check_pols_roll_fwd()` for every period inside the guarantee and would then miss the step
at the end of it.

### Benefit and expense flows

```
E[PREM(t)] = P IF(0)                    t = 0;  0 otherwise
E[ANN(t)]  = A(t) F(t)
E[DTH(t)]  = 0                                          life
           = d(t) ( ρ P + V(t + 1) )                    inheritance
           = d(t) ρ P                                   certain
E[SUR(t)]  = pols_lapse(t) CV(t + 1)
E[MAT(t)]  = IF(t + 1) M                inheritance, t = N − 1;  0 otherwise
                                        with N = 12n, the last projected month
E[COM(t)]  = P κ IF(0)                  t = 0;  0 otherwise
E[EXP(t)]  = φ A(t) F(t)  +  P ε IF(0) at t = 0
```

The death benefit is paid on the fund **carried forward**, V(t + 1), because deaths are
taken at the end of the month after the crediting and after the annuity due to the
survivors — see *Processing order*.  On the monthly grid that convention costs at most a
month of fund growth where on an annual grid it cost a year of it: ₩30,957.20 against
₩30,946.43 on point 6 at t = 0. On the certain shape it is the 10% alone: the
remaining instalments fall due on their own dates and are already inside E[ANN]
[S3] [S9 주7]. On the life shape there is **none**: 「별도의 사망보험금은 지급되지
않습니다」 [S5], the unpaid guaranteed instalments being what survives the annuitant, and
they too are inside E[ANN].

**The annuity charge is carried at the payment's own weight**, `φ A(t) F(t)`, so it is
incurred when a payment is made and not when a policy is in force. That is the direct
consequence of measuring it on the annuity [S1 §VIII] rather than per policy, and it is why
the expense column of the anchor is exactly 0.80% of the annuity column at every `t >= 1`.
On the monthly grid `A(t)` is the 연금월액, so the charge is 0.80% of it a month — which over
twelve months is exactly the 0.80% of the 연금연액 the cost table discloses.

### Processing order (period t = 0 … N − 1)

The order is not a presentational matter: three of the flows above depend on it.

1. **Time t, row 0 only.** The single premium `P` is received; the commission `P κ` is
   paid; the acquisition and administration expense `P ε` is incurred. The 위험보험료
   `P b` is *deducted from the fund* and never appears as a flow — what it buys appears
   instead as E[DTH]. Nothing at `t >= 1`.
2. **The fund is credited** at `j(t) = (1 + Max[공시이율, 최저보증이율(t)])^(1/12) − 1`,
   the floor band being the half-open `[dur_from, dur_to)` in policy years containing
   `t // 12`.
3. **The annuity is struck** — once at t = 0 on the life shape, every month on the other
   two — and **falls at the end of month t**, in arrears, at `A(t) F(t)`, with the 0.80%
   연금수령기간 중 비용 beside it at the same weight.
4. **Deaths are taken at the end of the month**, after the crediting and after the
   annuity due to the survivors. The 사망보험금 is therefore paid on the fund carried
   forward, `V(t + 1)`. **[std]**: a real contract settles a death mid-month and pays the
   연금월액 to the date of death, so a life dying in month t on the inheritance shape
   here receives the post-payment fund and **not** that month's annuity — a convention
   that now costs at most a month of fund growth rather than a year's.
5. **Surrenders are taken after the deaths**, at `CV(t + 1)`, and are suppressed through
   the final policy year (`w(t) = 0` for `t >= N − 12`).
6. **The 만기보험금 falls at the end of the last month** on the inheritance shape alone,
   at `t = N − 1`, weighted by `IF(N)` — the probability of reaching maturity alive **and**
   in force, one further month of decrement past the row that carries it.

The horizon itself, as a **count** of months:

```
N = 12 max( g , ω − x + 1 )    life
  = 12 n                       inheritance, certain
```

so the last projected month is `N − 1`. On the life shape the projection runs to the
limiting age, at which q = 1 and the monthly conversion spreads the certain death over the
twelve months of that policy year, so the obligation is **exhausted rather than truncated**;
the `max` covers the case — impossible on any shipped model point but reachable at a high
enough issue age — where the guarantee outlives the annuitant's limiting age. On the other
two the contract ends at a stated term, so the last month is `12n − 1` and its payment falls
at time 12n, with the 만기보험금 beside it where there is one.

### Net cash flow

```
CF(t)     = E[ANN(t)] + E[DTH(t)] + E[SUR(t)] + E[MAT(t)] + E[COM(t)] + E[EXP(t)]
            − E[PREM(t)]
net_cf(t) = − CF(t)
```

`liability_cf` is CF(t) verbatim, outgo-positive; `net_cf` is its exact negative, the
library-wide income-positive convention, and both are published as columns so that a
reader holding these notes beside the model reads the same sign in both.
`check_net_cf()` rebuilds the identity from `result_cf()`'s **published columns** rather
than from the formulas, so a component missing from the statement fails there rather than
being reconciled only in prose. There is no `claims` column beside the three `claims_*`
columns: a cash flow statement must not publish its own subtotal beside its parts.

### Optional modules (all off in the base run)

There are four switchable behaviours and the anchor exercises none of them.

| Module | Control | State on the anchor | Exercised by |
|---|---|---|---|
| The retention | `retention_basis` | **inert** — the life shape has no 만기보험금 | points 6 (designed) and 7 (ordered) |
| The stepping floor | `crediting_basis` | **inert** — 2.50% exceeds every step | point 8 (`min_guar`) |
| Voluntary surrender | `lapse_rate` | **off** — nil by contract | points 6, 7, 8, 9 |
| The longer guarantee | `annuity_term` | 10 years | point 3 (20 years) |

Everything else a Korean 즉시연금 can carry is **recorded in `product-spec.md` and not
modelled**: the front-loaded life annuity; the 거치형 selling mode with its 추가납입 and
중도인출; the proportional split of the fund across shapes [S8]; 부부계약 [S6]; the
large-contract discount [S6 §10-나] [R27]; the 상속연금형 종신형 sub-shape, only the
만기형 being carried; the 100세 and 기대여명 guarantee options; the partial withdrawal that
survives annuitisation at one carrier [S6 §8-나]; and 선지급, recorded and not exercised.

---

## Policyholder behavior modeling

**On the life shape there is no behaviour to model, and that is a cited product feature.**
「종신연금형(정액형, 집중보장형)의 경우 연금지급개시 이후에는 계약을 해지할 수
없습니다」 [S3]; 「계약자는 계약이 소멸하기 전에 언제든지 계약을 해지할 수
있으며(다만, 종신연금이 지급개시된 이후에는 해지할 수 없습니다)」 [S7 제31조], word for
word at [S8 제33조]; 「순수종신연금형을 선택한 경우, 연금지급이 개시된 이후 해지 불가」
[S5 주2]. On an immediate annuity the annuity begins a month after inception, so **the
contract is irreversible from month one**. Two reasons are given and both are real: the
tax condition of 소득세법 시행령 제25조제4항제4호, which requires a tax-exempt 종신형 not
to be surrendered after the first annuity payment [REG-R58]; and anti-selection,
「종신형에서는 연금지급이 개시된 후 해지를 허용하지 않는다. 이는 사망률이 높은 계약자가
해지함으로써 발생할 수 있는 역선택 위험을 방지하기 위한 장치이다」 [R12 §III-1](#krlib-immediate_annuity-r12).
`check_surr_value()` asserts that every shipped life-shape model point carries a nil rate
and a nil surrender value, rather than leaving that to the table.

**On the other two shapes the only behaviour is a voluntary surrender for which no source
gives a rate.** The **[std]** 2.00% is an **annual** rate carried per model point so that the
reader can set it to zero and read the difference; the projection applies its uniform-force
monthly conversion, 0.1682% a month, twelve of which compound back to the 2.00% exactly. Its direction is not obvious: on the inheritance shape
a surrender before maturity is a **realised loss**, the surrender value being the fund,
which sits below the gross premium the 만기보험금 would return at every duration before
maturity [S1 §VI-2] — the published 환급률 run rising to exactly 100.0% at twenty years is
that fact seen from the other side. On the certain shape a surrender takes the fund and
forfeits instalments whose present value at the crediting rate is the same fund, so the
election is value-neutral on the contract's own basis and is driven by liquidity, which no
model here carries.

Two further behaviours sit at the boundary and are handled outside the projection.
**Commutation (선지급)** is available on death *and on request*, once a year, in whole
years, discounted at the 공시이율 [S3] [S5 주8] [S7 제11조제3항] [S9]: an option with real
value on a falling-rate path and none on a rising one, because the discount rate is the
same rate that sets the annuity — **recorded, not exercised** (assumption (xv)). Proof of
the annuitant's survival and the 지정대리청구서비스특약 shift the timing and the recipient
of a payment but never its amount [S8]; not modelled.

**Anti-selection into the shapes** is the behaviour that matters most and the one the model
does least about. The 종신연금형 buyer is buying longevity cover and self-selects for it;
the 상속연금형 buyer is parking capital for an heir; the 확정기간연금형 buyer's mortality
does not enter his annuity at all — and one table serves all three. On the Korean market
that bites, because **the middle shape dominates**: 73.6% of contracts by count and 75.1%
by premium were 상속형 on the only public micro-dataset, against 18.2% / 18.6% 종신형 and
8.2% / 6.3% 확정형 [R12 표5](#krlib-immediate_annuity-r12), and the paper draws the comparison itself —
「종신형(72%) 즉시연금이 주류를 이루는 미국과 달리 우리나라는 상속형 중심으로 즉시연금에
가입하고 있다」 [R12 §III-2](#krlib-immediate_annuity-r12). **The Korean buyer is, in the main, not hedging longevity**,
and a model calibrated on a US or UK immediate-annuity book will mis-weight this one by a
factor of four. No source quantifies the differential and none is applied [unverified].
Behaviour therefore enters the *choice of model point*, not the projection.

---

## Worked example

Everything in this section was read off `Immediate_KR_S` and can be reproduced by running
it. `tests/test_immediate_annuity_kr.py` asserts these figures against the model cell by
cell to the precision shown, so a discrepancy between this document and the model is a
failure of the library and not a rounding matter.

**One arithmetic caveat governs every trace below.** The model computes in IEEE-754 double
precision with no intermediate rounding, and `0.9503 x 10^8` is not exactly representable
in binary: `av_pp_init()` on the inheritance and certain shapes is
**95,029,999.9999999851**, not 95,030,000 exactly, and the residue propagates. The traces
therefore use the model's own values rather than the round contractual ones. Where a trace
prints an annuity or accumulation factor it prints it **rounded to twelve digits**, so a
figure recomputed by hand from the printed factor can differ from the model in its last
digit or two; every figure quoted as a *result* is the model's own.

```
cd /home/user/lifelib-products
python lifelib/libraries/krlib/products/immediate_annuity/run.py
```

### The anchor cell and every assumption it uses

**Model point 1**, `policy_id` `IA-000001`. 남자, **보험나이 60**, 일시납
**₩100,000,000 (1억원)**, **종신연금형** with a **10-year 보증지급기간**, on the
`decl_2017` crediting basis, `lapse_rate` 0.00, `pols_if_init` 1.0. The premium is the
median of the only public dataset [R12 그림3](#krlib-immediate_annuity-r12) and is exactly the 소득세법 ten-year
exemption cap for contracts made from 2017-04-01 [REG-R58], so the anchor sits on the tax
boundary the product is designed around; the age is the one on which the anchor carrier
publishes its expense breakdown, its commission rate and its mortality anchors
[S1 §VII] [S1 §VIII] [S1 §IV-2]; and the ten-year guarantee is the choice 97.3% of
life-shape buyers actually made [R12 표7](#krlib-immediate_annuity-r12).

Assumption values used, in full, with tags. Every rate below is **annual**, as it is filed
and published; the projection applies the monthly conversions beside them.

| Quantity | Cells | Value | Tag |
|---|---|---|---|
| 계약체결비용 | `acq_charge_rate()` | 0.0220 | [S1 §VIII] |
| 계약관리비용 | `admin_charge_rate()` | 0.0130 | [S1 §VIII] |
| Total load c | `expense_load_rate()` | **0.0350** | derived from the two above |
| 위험보험료 b | `risk_prem_rate()` | **0.0000** | [S1 §VIII], 종신연금형 1형 |
| 모집수수료 κ | `comm_rate()` | 0.0200 | **[std]**, a round figure inside the published 2.08% / 1.75% pair [S1 §VII] |
| Insurer expense ε | `acq_expense_rate()` | 0.0150 | **[std]**, derived: 3.50% − 2.00% |
| Annuity charge φ | `annuity_charge_rate()` | 0.0080 | [S1 §VIII]; treatment **[std]** |
| 사망보험금 ρ | `db_rate()` | 0.00 | [S1] [S5] |
| 공시이율 i_d | `decl_rate()` | 0.0250 a year | [S1 §IV-4]; adoption **[std]** |
| 최저보증이율 i_g | `min_guar_rate(t)` | 0.0125 / 0.0100 / 0.0075 at `t // 12` < 5 / < 10 / >= 10 | [S3]; adoption **[std]** |
| Credited rate i(t) | `crediting_rate(t)` | **0.0250 a year at every t** — the declared rate is above every step of the floor | derived |
| Monthly credited rate j(t) | `crediting_rate_mth(t)` | **0.0020598363** — `(1.025)^(1/12) − 1` | derived **[std]** |
| q(60), q(70) | `mort_rate(0)`, `mort_rate(120)` | **0.00353**, **0.00728** a year | [S1 §IV-2], reproduced exactly |
| q^m(60) | `mort_rate_mth(0)` | 0.0002946437 — `1 − (1 − q)^(1/12)` | derived **[std]** |
| Surrender rate w | `lapse_rate(t)` | 0.00 at every t | [S3] [S7 제31조] — contract, not assumption |
| Limiting age ω | `omega_age` | 110 | **[std]** |

Derived quantities at inception, at the precision the model produces them:

```
av_pp_init()               96,500,000.0000000000     = P (1 − 0.0350 − 0.0000)
annuity_factor()                  239.234685591176   = ä(60, g = 10, j), a MONTHLY factor
annuity_pp(0)                 403,369.6023698976     연금월액, level for life
annuity_pp_annual(0)        4,840,435.2284387713     the 연금연액 it makes up
risk_prem_pp()                      0.0000000000
maturity_benefit()                  0.0000000000
retention_shortfall_pp()            0.0000000000
proj_years()                                   51    ω − x + 1 = 110 − 60 + 1
proj_len()                                    612    rows 0 … 611; 12 x proj_years()
```

The 연금월액 of **₩403,370** is about **40.3만원** a month, and the 연금연액 it makes up is
**₩4,840,435**, about 484만원 a year.

**The reconciliation against the annual-step model this replaced does not close on interest
alone, and the residual is a finding rather than a rounding.** The annual-step model solved
a 연금연액 of ₩4,948,039.16 payable once a year in arrears. Converting that to a
monthly-in-arrears instalment of the same present value — with
`i^(12) = 12[(1.025)^(1/12) − 1] = 0.024718035238` and therefore `i/i^(12) = 1.0114072482`,
so `4,948,039.1569 / 12 x 0.9887214095` — gives **₩407,686.02** a month against a naive
`A/12` of ₩412,336.60, the 1.14% between those two being the within-year interest the
monthly mode pays and the annual mode does not, which is exactly the 「신공시이율로 계산한
이자를 가산합니다」 of [S9 주11] and [S8 주14]. **The model's own monthly annuity is
₩403,369.60, a further 1.06% below that**, and the difference is mortality: a monthly
annuity pays part-year instalments to a life that dies inside a policy year, where an
annual-in-arrears annuity pays that life nothing for the year at all. The monthly
obligation is genuinely the larger one and the same fund therefore buys less of it. The
interest-only conversion is exact **only where no mortality enters the annuity**, which is
the 확정기간연금형 alone — and there the model reproduces it to the won, which is asserted
under *The load cross-check* below.

### The annuity factor, built

The factor is the one quantity in this document a reader cannot check by inspection, so it
is decomposed. At `j(0) = (1.025)^(1/12) − 1` and `v = 1/(1 + j)`:

```
ä(60, 10, j) = SUM t=0..119   v^(t+1) x 1                   the guaranteed 120 months
             + SUM t=120..611 v^(t+1) x l(t+1)              the life-contingent tail
             =          106.222810753287
             +          133.011874837888
             =          239.234685591176
```

The first sum is exactly the monthly annuity-certain `a(120, j) = (1 − (1+j)^-120)/j =
106.222810753287`, because inside the guarantee the weight is one whatever the annuitant
does — which is the arithmetic statement of 「보증지급기간안에 사망시에는 잔여보증지급기간
동안, 미지급된 연금월액을 … 드립니다」 [S3]. **44.4% of the factor is an annuity-certain
and 55.6% is a life annuity**, and only the second half reads `mort_table.csv`.

Note what is **not** in the formula: no `(f − 1)/(2f)` frequency correction, because the
frequency is the grid. The factor is a monthly annuity-immediate and the instalment it
produces is the 연금월액 the contract pays.

Two readings of the number itself. **The gross factor** — the premium divided by the
**annual** annuity — is `100,000,000 / 4,840,435.2284 = 20.6593`, against implied gross
factors of 23.81 (교보, 남자 55, 10년보증, 2.52%) and 23.15 (동양, 남자 55, 10년보증,
2.95%) computed from published illustrations in `product-spec.md`. **Those are not
comparable as they stand and the difference must not be waved at.** Five years of age at
60 is worth **2.13** units of gross factor on this table, not the 3.2 the 교보 comparison
would need; and running the model straight onto 교보's own published cell — 남자 55,
10년보증, 2.52%, the same 3.50% load — gives a monthly factor of **263.1339** and a
연금월액 of **₩366,733**, i.e. **36.7만원 against a published 35만원**. **The model's
annuity comes out about 4.8% high on the one life-shape cell a carrier's own figure can be
reached on** — better than the annual grid's 5.7%, because the monthly grid prices the
monthly stream the carrier is actually quoting — and the residual is basis: the carrier's
own load, its own annuitant table, and whether its 산출방법서 builds the 0.80%
연금수령기간 중 비용 into the factor, none of which [S3] discloses. That is the size of the
error a three-parameter law fitted to two rates and one life expectancy leaves behind, and
it is the first reason a production use of this model must replace `mort_table.csv`.
**The guarantee is cheap at this age**: the same fund converted with no guarantee at all
gives a factor of 237.109770 and a 연금월액 of ₩406,984.50, so the ten-year guarantee costs
**0.89% of income** — less than the annual grid's 0.99%, because a monthly annuity already
pays part-year instalments to a life that dies inside a policy year and there is that much
less for the guarantee to add. That is the quantitative reason 97.3% of buyers take it
[R12 표7](#krlib-immediate_annuity-r12), and it is also why a pure life annuity with no
guarantee may not be sold in Korea without the point being commercially interesting: the
minimum guarantee period is five years [R12 §III-2-라](#krlib-immediate_annuity-r12),
**[unverified]** as to the article text [R31].

Two further sanity checks. Ten years of guarantee at 보험나이 60 sits far inside the
complete `e(60)` of **28.2208** years on the shipped table — the monthly survival sum
divided by twelve — so the anchor clears the 소득세법 시행령 제25조제4항제3호 test that a
guarantee period on a tax-exempt 종신형 lie within the annuitant's statutory 기대여명
[REG-R58]. And had the **gross** premium been converted rather than the fund net of the
load, the 연금월액 would be `100,000,000 / 239.234686 = ₩417,999.59`, **3.63% higher** — the
3.50% load seen from the income side, grossed up by itself, a ratio invariant to the grid.

### First months of the base run

Per policy, income-positive, to two decimal places. `claims_death`, `claims_lapse` and
`claims_maturity` are **0.00 at every t** on this cell — the 종신연금형 pays no death
benefit after annuitisation, cannot be surrendered and has no maturity — and are omitted
from the table; they are columns of `result_cf()` all the same.

| t | `pols_if` | `premiums` | `annuity_payments` | `commissions` | `expenses` | `net_cf` |
|---|---|---|---|---|---|---|
| 0 | 1.000000 | 100,000,000.00 | 403,369.60 | 2,000,000.00 | 1,503,226.96 | **96,093,403.44** |
| 1 | 1.000000 | 0.00 | 403,369.60 | 0.00 | 3,226.96 | −406,596.56 |
| 2 | 1.000000 | 0.00 | 403,369.60 | 0.00 | 3,226.96 | −406,596.56 |
| 11 | 1.000000 | 0.00 | 403,369.60 | 0.00 | 3,226.96 | −406,596.56 |
| 12 | 1.000000 | 0.00 | 403,369.60 | 0.00 | 3,226.96 | −406,596.56 |
| 119 | 1.000000 | 0.00 | 403,369.60 | 0.00 | 3,226.96 | −406,596.56 |
| **120** | **0.953470** | 0.00 | **384,366.72** | 0.00 | 3,074.93 | **−387,441.65** |
| 121 | 0.952890 | 0.00 | 384,132.75 | 0.00 | 3,073.06 | −387,205.82 |
| 239 | 0.837189 | 0.00 | 337,076.63 | 0.00 | 2,696.61 | −339,773.24 |
| 240 | 0.835652 | 0.00 | 336,364.96 | 0.00 | 2,690.92 | −339,055.88 |
| 359 | 0.493177 | 0.00 | 197,347.75 | 0.00 | 1,578.78 | −198,926.53 |
| 360 | 0.489248 | 0.00 | 195,517.24 | 0.00 | 1,564.14 | −197,081.38 |
| 479 | 0.043078 | 0.00 | 16,736.70 | 0.00 | 133.89 | −16,870.60 |
| 480 | 0.041492 | 0.00 | 16,019.08 | 0.00 | 128.15 | −16,147.23 |
| 600 | 0.000000 | 0.00 | 0.12 | 0.00 | 0.00 | −0.13 |
| **611** | 0.000000 | 0.00 | **0.00** | 0.00 | 0.00 | **0.00** |

The state behind those rows, from `result_pols()`. `mort_rate` is the **annual** rate the
table publishes, level across the twelve months of a policy year; `mort_rate_mth` is what
the projection applies.

| t | age | `mort_rate` | `mort_rate_mth` | `lives_if` | `payment_factor` | `av_pp` |
|---|---|---|---|---|---|---|
| 0 | 60 | 0.00353000 | 0.0002946437 | 1.000000000 | 1.000000000 | 96,500,000.00 |
| 1 | 60 | 0.00353000 | 0.0002946437 | 0.999705356 | 1.000000000 | 96,295,404.60 |
| 11 | 60 | 0.00353000 | 0.0002946437 | 0.996763690 | 1.000000000 | 94,226,127.93 |
| 12 | 61 | 0.00369813 | 0.0003087008 | 0.996470000 | 1.000000000 | 94,016,848.73 |
| 119 | 69 | 0.00659390 | 0.0005511592 | 0.953995829 | 1.000000000 | 68,941,669.34 |
| **120** | 70 | **0.00728000** | 0.0006087004 | 0.953470025 | **0.952889648** | 68,680,308.29 |
| 121 | 70 | 0.00728000 | 0.0006087004 | 0.952889648 | 0.952309623 | 68,418,408.87 |
| 239 | 79 | 0.02181222 | 0.0018361145 | 0.837189204 | 0.835652028 | 33,403,315.14 |
| 240 | 80 | 0.02504325 | 0.0021112823 | 0.835652028 | 0.833887731 | 33,068,750.90 |
| 359 | 89 | 0.09151992 | 0.0079666234 | 0.493176902 | 0.489247948 | −12,088,782.79 |
| 360 | 90 | 0.10580035 | 0.0092755649 | 0.489247948 | 0.484709897 | −12,517,053.30 |
| 479 | 99 | 0.36237864 | 0.0368064377 | 0.043077769 | 0.041492230 | −70,322,514.23 |
| 480 | 100 | 0.40896710 | 0.0428772519 | 0.041492230 | 0.039713157 | −70,870,736.70 |
| 600 | 110 | 1.00000000 | 0.0833333333 | 0.000000338 | 0.000000309 | −145,568,384.91 |
| 611 | 110 | 1.00000000 | 1.0000000000 | 0.000000028 | 0.000000000 | −153,383,930.43 |

`mort_rate(0) = 0.00353` and `mort_rate(120) = 0.00728` are the **published** 개인연금사망률
at 보험나이 60 and 70 [S1 §IV-2], reproduced exactly by the construction; every other rate
in the column is the Makeham interpolation between and beyond them. The `mort_rate_mth`
column is `1 − (1 − q)^(1/12)` and twelve of each compound back to the annual figure exactly
— except at 보험나이 110, where `q = 1` and the certain death is spread uniformly over the
twelve months of that policy year: 1/12 in month 600 rising to 1 in month 611, which is why
the in-force reaches zero on the last row of the frame rather than on the 계약해당일.
`cv_pp` is **nil at every t** and is omitted.

Three rows do something and each is traced below: **row 0**, where the premium arrives and
the whole load is taken; **row 120**, the guarantee cliff; and **the months around 330**,
where the 계약자적립액 crosses zero.

### Hand trace, month 0 — the premium, the load, and the first instalment

```
V(0)   = 100,000,000 x (1 − 0.0350 − 0.0000)          = 96,500,000.0000000000
j(0)   = (1.025)^(1/12) − 1                           =        0.002059836270
ä      = 106.222810753287 + 133.011874837888          =      239.234685591176
A(0)   = 96,500,000 / 239.234685591176                =    403,369.6023698976
F(0)   = max( l(1), 1{1 <= 120} ) = max(0.999705, 1)  =        1.000000000000
ANN(0) = 403,369.6023698976 x 1.000000                =    403,369.6023698976
COM(0) = 100,000,000 x 0.0200                         =  2,000,000.0000000000
EXP(0) = 100,000,000 x 0.0150                         =  1,500,000.0000000000
       + 0.0080 x 403,369.6023698976 x 1.000000       =      3,226.9568189592
                                                         ────────────────────
                                                      =  1,503,226.9568189592

net_cf(0) = 100,000,000.0000000000
          −     403,369.6023698976
          −   2,000,000.0000000000
          −   1,503,226.9568189592
          =  96,093,403.4408111423
```

**Read the premium split off that line.** The commission of ₩2,000,000 and the expense of
₩1,500,000 sum to ₩3,500,000, which is exactly the load deducted from the premium to make
V(0); the risk premium is nil on this shape; and `check_premium_split()` closes:
`100,000,000 = 2,000,000 + 1,500,000 + 0 + 96,500,000`. **Nothing is left over in either
direction, which is what "no acquisition strain" means arithmetically.** The whole of the
+₩96.1m of the first row is the premium net of the first month's annuity and the day-one
outgo, and it is the only positive row in the statement.

### Hand trace, month 1 — the recursion, and why the annuity does not move

```
V(1)   = 96,500,000 x (1 + j) − 403,369.6023698976
       = 96,698,774.2000398189 − 403,369.6023698976   = 96,295,404.5976699144
l(1)   = 1 x (1 − 0.0002946437)                       =      0.999705356320
F(1)   = max( l(2), 1{2 <= 120} )                     =      1.000000000000
A(1)   = A(0), struck once at commencement            =    403,369.6023698976
ANN(1) = 403,369.6023698976 x 1.000000                =    403,369.6023698976
EXP(1) = 0.0080 x 403,369.6023698976 x 1.000000       =      3,226.9568189592

net_cf(1) = 0 − 403,369.6023698976 − 3,226.9568189592 = −406,596.5591888567
```

**The annuity does not move and the fund does not matter.** A(1) is A(0) because the life
shape's factor was struck once against 「연금개시시의 계약자적립액」 [S7 별표1] and the
rate is level [S1 §IV-4]; the fund V(1) is falling by roughly ₩2.5m a year and has **no
contractual role at all** on this shape. Rows 1 to 119 are this row repeated, because the
guarantee makes the weight one throughout and nothing else in the row depends on t — the
annual assumptions being flat across a policy year, even the 계약해당일 at t = 12 moves
nothing in the cash flow on this cell.

### Hand trace, month 120 — the guarantee cliff

```
IF(119) = max( l(119), 1{119 < 120} ) = max(0.953995829, 1)  = 1.000000000000
IF(120) = max( l(120), 1{120 < 120} ) = max(0.953470025, 0)  = 0.953470025140
exit(119) = IF(0) − l(120) = 1 − 0.953470025140              = 0.046529974860
          check:  IF(119) − exit(119) − IF(120)
               =  1.000000000000 − 0.046529974860 − 0.953470025140  =  0

F(120)  = max( l(121), 1{121 <= 120} ) = max(0.952889648, 0)
                                                             = 0.952889647577
ANN(120)= 403,369.6023698976 x 0.952889647577                =   384,366.7182455019
EXP(120)= 0.0080 x 384,366.7182455019                        =     3,074.9337459640

net_cf(120) = −( 384,366.7182455019 + 3,074.9337459640 )
            = −387,441.6519914659
```

**Two different things step at t = 120 and they step to two different numbers.** The
obligation `pols_if` steps from 1.000000 to **0.953470025140**, which is `l(120)`: everyone
who died in the first ten years leaves the obligation at once, and `pols_exit(119)` is that
whole cohort, **0.046529974860**, in a single month. Both figures are the annual-step
model's to the last printed digit, which is what twelve compounded monthly decrements are
for. The payment weight steps from 1.000000 to **0.952889647577**, which is `l(121)`,
because the payment on row 120 falls at the end of month 120 and is the first one the
guarantee does not cover. The cash flow falls by 4.71% between rows 119 and 120 and by a
further 0.06% between rows 120 and 121: the first step is the guarantee expiring, the second
is one **month** of mortality where on the annual grid it was a whole year's.

**This is the single feature of the shape that an implementation is most likely to smooth
away.** Decrementing the obligation on death inside the guarantee — the natural thing to
do, and wrong — removes the step from `pols_if` and puts a survival weight on 120
instalments that are due whatever happens. `check_pols_roll_fwd()` and
`check_guarantee_certain()` both fail on that error, the second immediately, at t = 0.

### The tail, and the fund that goes negative

The 계약자적립액 crosses zero **inside the twenty-eighth policy year**, between t = 324 and
t = 330:

```
V(324) =  2,358,767.07
V(325) = 2,358,767.07 x (1 + j) − 403,369.60   =  1,960,256.14
   …
V(330) =                                         −44,645.38
```

and goes on falling to −₩153,383,930.43 at t = 611. **That is a documented feature and not
a defect**, and the monthly grid dates it properly where an annual grid could only place it
at a policy-year boundary. A life annuity's fund is not its reserve: the annuitant still
alive at 87 has drawn more than his own money and is being paid out of the mortality of the
cohort he was priced with. The recursion is published because the recursion is the
contract's, `cv_pp` is nil there so nothing can be paid out of a negative fund, and
`check_av_terminal()` returns True on the life shape *by design*. Flooring `av_pp` at zero
would break `check_av_roll_fwd()`, whose life branch is the retrospective closed form
`V(0)(1 + j)^t − A s(t, j)`, from the crossing onward.

At the far end `lives_if(612) = 0` exactly, because `q(110) = 1` and the monthly conversion
pays the last of the in-force out over the twelve months of that policy year, so
`payment_factor(611)` is zero, **row 611 carries no payment at all**, and the obligation is
exhausted rather than truncated.

### Undiscounted totals

Over t = 0 … 611, per policy, income-positive:

```
pols_if            (sum of the column)        341.116217     months
premiums                              100,000,000.00
annuity_payments                      137,211,311.88
claims_death                                    0.00
claims_lapse                                    0.00
claims_maturity                                 0.00
commissions                             2,000,000.00
expenses                                2,597,690.50
liability_cf                           41,809,002.38
net_cf                                −41,809,002.38
```

Four of those numbers repay a second look.

**`Σ pols_if` = 341.116217 is the expected number of *months* the obligation stays open**,
and it decomposes exactly: `Σ l(t)` over t = 0 … 611 is 338.649237, and the guarantee adds
`120 − Σ l(t)` over t = 0 … 119 = `120 − 117.533020 = 2.466980`. **The ten-year guarantee
extends the obligation by 2.5 months in expectation** on a 60-year-old male: a cheap option,
which the market buys almost universally. The annual grid put the same quantity at 2.2
months, and the monthly figure is the larger because a monthly annuity already pays
part-year instalments to a life that dies inside a policy year.

**`expenses` is 2,597,690.50 and splits cleanly**: ₩1,500,000 is the day-one acquisition
and administration expense, and the remaining **₩1,097,690.50** is exactly
`0.0080 x 137,211,311.88`, the annuity charge on every payment the model makes. No other
expense exists in this projection.

**Total annuity outgo is 1.3721 times the premium**, and the cumulative payments cross the
premium inside month 263: ₩99,745,332.34 by the end of row 262 and ₩100,064,499.96 by the
end of row 263. Row `t` pays at the end of month `t`, so **the undiscounted break-even is
the 264th instalment, at attained age 81** — a date the annual grid could only place to the
nearest year. On the nominal annuity, ignoring the survival weight, the same arithmetic is
the gross factor itself in months — `100,000,000 / 403,369.60 = 247.9` instalments, so the
248th crosses — which is the number a Korean buyer's own arithmetic produces, and why the
shape is a longevity hedge and is understood as one. The sixteen-instalment difference
between the two readings is the mortality the expected stream carries and the buyer's does
not. **`Σ net_cf` = −₩41,809,002.38** is a loss undiscounted and must be: the insurer
receives ₩100m at time 0 and pays out over half a century, and the sign becomes meaningful
only when the stream is discounted, which this library does not do.

**Every total is a little below the annual-step model's** — ₩137.2m of annuity against
₩138.2m, `Σ net_cf` −₩41.8m against −₩42.8m — for the one reason given above: the same fund
buys a smaller instalment once the annuity is valued as the monthly stream the contract
actually pays.

### Reading the shape of the result

The statement has three regions and each says something about the product. **Row 0 is
almost the whole of the insurer's cash**: +₩96.1m, being the premium less the first
instalment and the entire day-one load, and there is never another positive row. **Rows 1
to 119 are a flat annuity-certain**: −₩406,596.56 repeated 119 times, identical to the last
digit, because the guarantee makes survival irrelevant and the level rate makes the annuity
level. **Rows 120 onward are a decaying life annuity**: the same ₩403,369.60 weighted by a
survival probability that falls from 0.9529 to zero over forty years. The liability is
therefore front-loaded in *certainty* and back-loaded in *duration* — a block of 120
unconditional payments followed by a long thin mortality-driven tail — which is exactly the
risk profile that makes longevity, and not interest, the dominant model risk on this shape.
And the whole of the insurer's expense in that half-century is ₩2.6m against ₩137.2m of
benefit outgo, 1.9%: **on a Korean immediate annuity the charges are taken once, at the
door, and almost nothing is taken afterwards.**

### The dispute, from one contract on two bases — model points 6 and 7

Both are 남자 60, 일시납 ₩100,000,000, **상속연금형 만기형**, 보험기간 10년, `decl_2017`,
`lapse_rate` 0.02 a year. They differ in one column: `retention_basis`. On both,
`av_pp_init() = 95,030,000.00` (= P × (1 − 0.0350 − 0.0147)) and
`maturity_benefit() = 100,000,000.00`, and `proj_len() = 120`, so the frame is
`t = 0 … 119`.

**Hand trace, month 0, as designed (point 6).**

```
V(0)   = 100,000,000 x (1 − 0.0350 − 0.0147)     = 95,029,999.9999999851
j      = (1.025)^(1/12) − 1                      =        0.002059836270
s(120, j) = ((1+j)^120 − 1)/j                    =      135.974178286376
R(0)   = (100,000,000 − 95,029,999.9999999851) / s(120, j)
       = 4,970,000.0000000149 / 135.974178286376 =     36,551.0574333656
A(0)   = 95,029,999.9999999851 x j − 36,551.0574333656
       = 195,746.2407231556 − 36,551.0574333656  =    159,195.1832897901
F(0)   = IF(0) x (1 − q^m(60)) = 1 x 0.999705356 =        0.999705356320
ANN(0) = 159,195.1832897901 x 0.999705356320     =    159,148.2774351536
V(1)   = 95,029,999.9999999851 x (1 + j) − 159,195.1832897901
       = 95,225,746.2407231480 − 159,195.1832897901
                                                 = 95,066,551.0574333519
d(0)   = 1 x 1 x 0.000294643680                  =        0.000294643680
DTH(0) = 0.000294643680 x (0.10 x 100,000,000 + 95,066,551.0574333519)
       = 0.000294643680 x 105,066,551.0574333519 =     30,957.1952443041
lapse(0)= 1 x (1 − 0.000294643680) x 1 x w^m     =        0.001681646920
SUR(0) = 0.001681646920 x 95,066,551.0574333519  =    159,868.3727871836
COM(0) = 2,000,000.0000000000
EXP(0) = 1,500,000 + 0.0080 x 159,148.2774351536
       = 1,500,000 + 1,273.1862194812            =  1,501,273.1862194813

net_cf(0) = 100,000,000.00 − 159,148.2774351536 − 30,957.1952443041
          − 159,868.3727871836 − 2,000,000.00 − 1,501,273.1862194813
          = 96,148,752.9683138877
```

**Hand trace, month 0, as ordered (point 7).** One term goes to zero and everything
downstream moves: `R(0) = 0`, so `A(0) = 95,029,999.9999999851 x j = 195,746.2407231556`
and `V(1) = 95,225,746.2407231480 − 195,746.2407231556 = 95,029,999.9999999851`, the fund
standing still. Then `ANN(0) = 195,746.2407231556 x 0.999705356320 = 195,688.5653304506`,
`DTH(0) = 0.000294643680 x (10,000,000 + 95,029,999.9999999851) = 30,946.4257062355`,
`SUR(0) = 0.001681646920 x 95,029,999.9999999851 = 159,806.9068140256` and
`EXP(0) = 1,500,000 + 0.0080 x 195,688.5653 = 1,501,565.5085226437`, giving
`net_cf(0) = 96,111,992.5936266482`.

The two liabilities side by side:

| | as designed (6) | as ordered (7) |
|---|---|---|
| `annuity_pp(t)` — the 연금월액, every t | **159,195.1832897901** | **195,746.2407231556** |
| `annuity_pp_annual(t)` — the 연금연액 | 1,910,342.20 | 2,348,954.89 |
| `retention_pp(0)` | **36,551.0574333656** | 0.0000000000 |
| `av_pp` path | rises 95,030,000.00 → 100,000,000.00 at t = 120 | **flat** at 95,030,000.00 |
| `retention_shortfall_pp()` | 0.00 | **3,882,556.0565769221** |
| Σ `annuity_payments` | 16,976,657.3468 | 20,874,481.1684 |
| Σ `claims_death` | 4,494,012.5082 | 4,385,780.0077 |
| Σ `claims_lapse` | 15,854,560.3876 | 15,517,362.9412 |
| Σ `claims_maturity` | 79,495,349.9719 | 79,495,349.9719 |
| Σ `expenses` | 1,635,813.2588 | 1,666,995.8493 |
| Σ `net_cf` | **−20,456,393.4733** | **−23,939,969.9386** |
| difference in Σ `net_cf` | — | **−3,483,576.4653** |

**The annuity is 22.96% higher on the ordered basis and the contract costs the insurer
₩3.48m more per ₩100m of premium, undiscounted.** With R = 0 the fund never grows, so the
만기보험금 of the **gross** premium has to be found from somewhere the contract does not
fund; `retention_shortfall_pp()` is what that costs at inception,
`(M − V(0)) v(120) = 4,970,000 x 0.781198401726 = ₩3,882,556.0565769221`, and it appears on
the right-hand side of `check_annuity_basis()` rather than being tolerated away, because
under `as_ordered` the pricing identity **does not** close on V(0) and should not.

Note what does **not** change: `claims_maturity` is ₩79,495,349.97 on both, the maturity
benefit being contractually the gross premium either way. **The dispute was never about
whether the ₩100m came back**, but about whether the policyholder had been told that part
of his interest was being taken to fund it — and the 약관 he was handed did not say so
[R1 §1-나, 별표1](#krlib-immediate_annuity-r1) [R2 §4](#krlib-immediate_annuity-r2).

**The retention rises every month even on a level rate.** On point 6, at the ten
계약해당일:

```
t:        0           12           24           36           48
R(t):  36,551.06    37,464.83    38,401.45    39,361.49    40,345.53
t:       60           72           84           96          108
R(t):  41,354.17    42,388.02    43,447.72    44,533.91    45,647.26
```

and inside the first policy year, month by month, 36,551.06 → 36,626.35 → 36,701.79 → …
→ 37,387.82, which is the one thing the annual grid could not show. It rises because the
remaining term shortens faster than the shortfall `M − V(t)` closes. The annuity
nonetheless stays **exactly level at ₩159,195.1833**, the interest `V(t) j` rising by
precisely the same amount — the algebraic content of `V(t) = V(0) + R s(t, j)`. **On a
falling rate the two move the same way instead of opposite ways**, and that is model
point 8.

**The external check.** `product-spec.md` reconstructs the ten-year 만기형 monthly annuity
independently, from published figures, at **₩161,000**; the model pays **₩159,195.18** a
month. Two constructions agreeing to within 1.1%, and the strongest external check the
inheritance shape has; the residual is the within-month interest and the retention's own
monthly re-striking, neither of which the spec's annual reconstruction carries.

### The floor stepping — model point 8

여자 70, ₩100,000,000, 상속연금형 만기형 **20년**, on the `min_guar` basis, so
`decl_rate = 0` and the credited rate is the floor at every duration: **1.25% for
t = 0 … 59, 1.00% for t = 60 … 119, 0.75% from t = 120**.

| t | `crediting_rate` | `annuity_pp(t)` | `retention_pp(t)` | `av_pp(t)` |
|---|---|---|---|---|
| 0 | 0.0125 | 80,175.2482050112 | 18,251.6955717737 | 95,030,000.00 |
| 48 | 0.0125 | 80,175.2482050129 | 19,181.5343519293 | 95,927,747.87 |
| 59 | 0.0125 | 80,175.2482050133 | 19,401.2088066262 | 96,139,840.85 |
| **60** | **0.0100** | **59,974.7776499095** | 19,792.9786825209 | 96,159,242.06 |
| 119 | 0.0100 | 59,974.7776499096 | 20,785.3772540911 | 97,355,568.73 |
| **120** | **0.0075** | **39,588.3970942395** | 21,063.6142111074 | 97,376,354.11 |
| 228 | 0.0075 | 39,588.3970942428 | 22,528.8168917276 | 99,728,726.14 |
| 239 | 0.0075 | 39,588.3970942352 | 22,683.6542366892 | 99,977,316.35 |

**Hand trace across the first step, t = 59 to t = 60.**

```
t = 59: m = 240 − 59 = 181,  i = 0.0125,  j1 = (1.0125)^(1/12) − 1 = 0.001035746015
        s(181, j1)                                      =    198.964878470784
        R(59) = (100,000,000 − 96,139,840.8476033062) / 198.964878470784
                                                        =     19,401.2088066262
        A(59) = 96,139,840.8476033062 x j1 − 19,401.2088066262
              = 99,576.4570116395 − 19,401.2088066262
                                                        =     80,175.2482050133

t = 60: V(60) = 96,139,840.8476033062 x (1 + j1) − 80,175.2482050133
              = 96,239,417.3046149462 − 80,175.2482050133
                                                        = 96,159,242.0564099401
        m = 180,  i = 0.0100,  j2 = (1.01)^(1/12) − 1 = 0.000829538114
        s(180, j2)                                      =    194.046485129689
        R(60) = (100,000,000 − 96,159,242.0564099401) / 194.046485129689
                                                        =     19,792.9786825209
        A(60) = 96,159,242.0564099401 x j2 − 19,792.9786825209
              = 79,767.7563324305 − 19,792.9786825209
                                                        =     59,974.7776499095
```

**The rate falls by one fifth and the annuity falls by one quarter.** `1.25% → 1.00%` is
−20.0%; `80,175.25 → 59,974.78` is **−25.20%**. The extra 5.2 points are the retention
*rising*, from ₩19,401.21 to ₩19,792.98, at the same moment as the interest it is deducted
from falls. At the second step, `1.00% → 0.75%`, the annuity falls a further **33.99%**, and
over the two steps

```
80,175.2482050112  →  39,588.3970942395        =  −50.62%
   (80,175.25/월)         (39,588.40/월)
```

**The annuity falls by half from the first month to the 121st while the guaranteed floor is
honoured on the fund at every single step**, and `av_pp(240) = 100,000,000.00` exactly,
which `check_av_terminal()` asserts. That is the substance of the dispute in one table: the
floor is a rate on the fund, never a floor on the annuity. The disputed 2012 contract's
own published annuity fell **55.4% in five years** on the same mechanism [R1 §1-가](#krlib-immediate_annuity-r1), and
this model point reproduces the mechanism if not the vintage. Note that the annuity is
**level inside each band and steps only on the 계약해당일**: the floor schedule is published
by policy year and the grid reads it at `t // 12`, so the monthly grid refines the fund and
the decrements without inventing a monthly rate schedule the sources do not have.

One further point about this model point, which is what makes it worth shipping: it is the
only shipped point on which `crediting_rate(t)` is not constant, so it is the only one that
exercises `retention_pp` being **re-struck against the remaining term at the current
rate** rather than fixed at inception. An implementation that computed R once at t = 0
would still reach `av_pp(240) = M` on a level rate and would miss it here by ₩6,393,965.

### The load cross-check — model point 9

남자 60, ₩100,000,000, **확정기간연금형** 10년 at 2.50%, `lapse_rate` 0.02 a year.

```
V(0) = 100,000,000 x (1 − 0.0350 − 0.0147)      = 95,029,999.9999999851
j    = (1.025)^(1/12) − 1                       =         0.002059836270
a(120, j) = (1 − (1+j)^-120)/j                  =       106.222810753287
A(0) = 95,029,999.9999999851 / a(120, j)        =    894,628.9344641458
```

**This is the one shape on which the monthly grid and the annual grid it replaced agree to
the won**, and that agreement is worth stating: the 확정기간연금형 carries no mortality in
its annuity at all, so the annual-step model's 연금연액 of ₩10,858,010.26 converted through
the `i^(12)/i` adjustment is precisely ₩894,628.93 — which is what the monthly grid solves
for directly. Everywhere else in this document the two grids differ by the mortality a
monthly annuity picks up; here there is none to pick up.

Against 교보's published **90만원** a month on a 2.52% basis [S3] the model's ₩894,628.93 is
**−0.60%**. `product-spec.md`'s own cross-check table puts the same cell at −0.5% because it
solves the identity on 교보's own 2.52% while this model runs the representative 2.50%; the
0.10-point difference between the two figures is exactly those 0.02 points of declared rate,
and the model reproduces the *mechanism* rather than the spreadsheet's number. **The
annuitant's age and sex are irrelevant to a 확정기간연금형**, so 교보's 남자 55 figure is
directly comparable with the model's 남자 60 one.

Because this shape carries no mortality in its annuity, it is the sharpest available test
of the expense load, and it is the reason the composite adopts the load it does: solving
the same identity against all four of 교보's published terms — 10, 15, 20 and 30 years —
on the representative first-day deduction of 4.97% reproduces every one within **1.4%**
[S3], on a carrier and a document entirely independent of the 하나생명 expense disclosure
the load was taken from [S1 §VIII].

The fund runs off to zero: `av_pp(120) = −0.00000000047`, which is float noise against a
₩100m contract and is what `check_av_terminal()` tolerates. Undiscounted totals:
`annuity_payments` ₩97,370,154.63, `claims_death` ₩417,574.03, `claims_lapse`
₩9,187,258.64, `expenses` ₩2,278,961.24, `Σ net_cf` **−₩11,253,948.54**. Note that
`claims_lapse` is nil through the whole final **policy year** — the surrender rate is
suppressed there on every shape — so a contract in its last year runs to its last
instalment, and the last instalment itself is ₩745,894.87, 0.77% of the annuity total
against the 9.1% the same row carried on an annual grid.

---

## Valuation and reserve pointers

This library projects **gross best-estimate liability cash flows**. Every valuation layer
consumes them and is **cited, not implemented**.

- **책임준비금 (policy reserve), and the 해약환급금준비금 beside it.** 보험업법 제120조
  requires the reserve and delegates its computation to the FSS Governor [REG-R3]; 감독규정
  제6-11조 sets it as a current-estimate quantity, with 제6-11조의4 and 제6-11조의5 on the
  보증준비금 [REG-R10] and 시행세칙 별표 24 giving that basis [REG-R26]. On top of it Korea
  appropriates a **해약환급금준비금** inside retained earnings, to stop a balance sheet
  distributing earnings the contractual surrender-value floor would later demand [REG-R11]
  — **it has no counterpart anywhere else in this repository**, and here it is nearly inert:
  the 해약공제액 is nil so the surrender value *is* the 계약자적립액, and on the 종신연금형
  there is no surrender value at all. The `liability_cf(t)` vector is the input to that
  layer and is not itself a reserve.
- **계약자적립액 and 해약환급금 are the two quantities this model does compute**, both being
  contractual: 감독규정 제7-65조제1항 makes the 계약자적립액 whatever the 산출방법서 says it
  is, and 제7-66조제1항제1호 makes the surrender value the 계약자적립액 less the 해약공제액
  floored at zero, with 별표 14's 표준해약공제액 as the cap [REG-R18] [REG-R19] [REG-R20].
  The cap binds nothing here, and that it binds nothing is observed rather than assumed.
- **K-IFRS 제1117호 and K-ICS have both been in force since 2023-01-01** [REG-R60]
  [REG-R13], so Korea runs an economic-value solvency measure and a CSM-based earnings
  measure together and live. The fulfilment cash flows are this vector with a risk
  adjustment and a CSM layered on; the discount rate and the actuarial-assumption
  guidelines are supervisory work in progress [REG-R27], and the guideline's functional
  form is **[unverified]** at instrument level. **Nothing product-specific to 즉시연금 was
  retrieved on the IFRS 17 or K-ICS treatment of an annuity in payment**; 별표 22, the
  K-ICS shock schedule, was not retrieved either [REG-R26] [unverified].
- **The crediting rate is not a discount rate.** `disc_factor(t)` runs on the
  Max[공시이율, 최저보증이율] path and exists for the pricing identity
  `check_annuity_basis()` and for `retention_shortfall_pp()` only. Both are statements
  about the **contract's own basis**, not about value.
- **Professional and supervisory frame.** The work sits under a 선임계리사's verification
  duties at 보험업법 제181조 and 제184조 [REG-R5], and the 기초서류 are filed under
  제5조제3호 with 제128조의2 requiring compliance [REG-R2]. **The status of that filing as
  against a policyholder is the whole of this product's litigation**: 「산출방법서는
  보험회사 내부의 계리적 서류에 지나지 않는 것으로 … 보험계약관계에 적용될 수는 없다」
  [R1 §3](#krlib-immediate_annuity-r1), refined by the Supreme Court on 2025-10-16 [R6] [R21] [R23].
- **Policyholder taxation does not enter the insurer's liability cash flows** and is
  specified in `product-spec.md` [REG-R58] [REG-R59]. Policyholder protection is
  ₩100,000,000 per person per insurer from 2025-09-01, with a 만기보험금 falling outside
  the insurance bucket [REG-R52] [REG-R32] — which bites harder here than anywhere else in
  `krlib`, the **median** premium being ₩100,000,000 and 38.5% of contracts exceeding it
  [R12].

---

## Key sensitivities and model risks

Dominant assumptions, in order of how far they move the answer.

1. **Longevity, on the life shape only, and it dominates everything else there.** The
   liability is a payment stream with no offsetting decrement — the guarantee removes even
   the partial offset a pure life annuity would have in its first decade — so the mortality
   level is the single largest lever. And the basis is a **[std]** three-parameter law
   fitted to two published rates and one published life expectancy [S1 §IV-2] [REG-R33]
   [REG-R34], which is as thin an anchor as any basis in this library rests on. The +22.0%
   residual at 보험나이 50 for men is the fit's own statement of how much shape it could not
   capture. **Substituting a filed basis is a CSV replacement and no formula changes**, and
   it is the first thing any production use of this model must do.
2. **The declared rate, on the other two shapes, and it dominates everything else there.**
   The 상속연금형 annuity is `V j − R` and the 확정기간연금형 annuity is `V / a(12n, j)`;
   both are first-order in the rate and the first is worse than first-order, because the
   retention moves the other way. Model point 8 quantifies it: a 50-basis-point fall in the
   credited rate over ten years halves the income. The rate itself is unmodellable —
   majority-weighted to the insurer's own 운용자산이익률 under a formula whose weighting
   each carrier sets for itself [REG-R18] [REG-R24] [S6] [S12] — so it is exposed as a
   scalar and a user who wants a rate path substitutes one.
3. **The expense load, because it is taken once and taken from the annuity.** Every won of
   load is a won that never enters V(0) and therefore reduces the annuity by the load
   divided by the factor, for life. The 3.50% load costs the anchor annuitant **3.63% of
   his income**, permanently. The load is corroborated across two independent carriers to
   within 1.4% [S1 §VIII] [S3], which is unusually good for a Korean expense assumption,
   but the **1.47% 위험보험료 applied unscaled from a twenty-year to a ten-year contract**
   is not corroborated at all and is conservative in a stated direction.
4. **The retention switch, on the shape that is three quarters of the market.** Points 6
   and 7 differ by 22.96% of income and ₩3.48m of undiscounted outgo on one boolean. There
   is no "right" setting: the 분조위 ordered one, the Supreme Court restored the other for
   the contracts before it, and the current market states the deduction on the face of the
   약관 [R1] [R2] [R6] [S7 별표1]. A model that hard-codes either cannot express the
   question.
5. **The surrender assumption, which is entirely unsourced.** 2.00% a year is **[std]** and
   no retrieved document supports any figure. On point 6 it produces ₩15.9m of
   `claims_lapse` against ₩17.0m of annuity payments — the surrender stream is the same
   order of magnitude as the benefit the contract exists to pay — so on the two shapes that
   permit surrender this is not a second-order assumption, and its unsourced status is the
   most serious data gap in the model after the mortality table.
6. **The grid itself, now that it is monthly, and what it stopped approximating.** The
   projection pays the 연금월액 the contract pays, so there is no annual-to-monthly
   adjustment left to make: the `i/i^(12) = 1.0114072482` correction the annual grid applied
   is now the grid. That change is **worth 1.06% of the life-shape annuity**, and it is a
   mortality effect rather than an interest one — a monthly annuity pays part-year
   instalments to a life that dies inside a policy year, which an annual-in-arrears annuity
   does not. It leaves the 확정기간연금형 unchanged to the won, that shape carrying no
   mortality in its annuity. What the grid still approximates is much smaller: the declared
   rate resets monthly in reality and is carried as one annual figure a policy year
   [REG-R18] [REG-R24], and the assumptions stay annual with uniform-force monthly
   conversions beneath them — exact wherever the annual figure is level, which on the
   representative basis it is.
7. **Data risk in the sources themselves.** The 경험생명표 is not published [REG-R33]
   [REG-R34]; no filed 산출방법서 for an 즉시연금 was retrieved, so no annuity formula in
   this library was read from a basis document [R31]; the minimum-guarantee-period rule is
   quoted from a paper rather than the regulation [R12 §III-2-라](#krlib-immediate_annuity-r12) [unverified]; the market
   picture rests on one 2012 dataset covering FY2008–FY2009 [R12]; and every aggregate
   about the dispute is news-sourced [R17]–[R25]. None is load-bearing on the recursions.

### Known modeling pitfalls

These are the specific ways an implementation of **this** product looks right and is
wrong. Each is checkable against the shipped model, and most are already asserted by one
of the eleven `check_*()` cells.

1. **Treating `pols_if` as a survival probability.** It is the probability that a **payment
   obligation remains**: on the anchor it is exactly 1.000000 for 120 months while the
   annuitant's survival probability has already fallen to 0.953996 by t = 119, so any
   per-policy quantity weighted by survival inside the guarantee is understated. *Test:*
   `pols_if(t) == 1.0` for t = 0 … 119 on point 1, and `pols_if(119) != lives_if(119)`.
2. **Adding the guarantee to the survival probability instead of taking the max.** The
   `max` makes the 보증지급기간 a floor on the obligation; an additive form pays
   `1 + l(t+1)` for the whole guaranteed term. On the anchor the additive factor is
   **343.332581** against the correct **239.234686**, so the 연금월액 comes out at
   ₩281,068.58 — **69.68%** of the right answer, a 30% under-payment for life.
   *Test:* `check_guarantee_certain()` and `check_payment_factor()`.
3. **Decrementing the obligation on a death inside the guarantee, or confusing the two
   guarantee tests `t < 12g` and `t + 1 <= 12g`.** Nothing exits until the guarantee expires
   and then the whole cohort that died inside it exits at once: `pols_exit(t) = 0` for
   t = 0 … 118 and `pols_exit(119) = 0.046529974860`. The obligation is open at time t for
   t = 0 … 119 while the 120 instalments the guarantee covers fall at the ends of months
   0 … 119, so on the same row `pols_if(120) = l(120) = 0.953470025140` and
   `payment_factor(120) = l(121) = 0.952889647577` are **different numbers**. Either error
   shifts the cliff by a month. *Test:* `check_pols_roll_fwd()`, `pols_exit(118) == 0.0`,
   and both t = 120 weights, on point 1.
4. **`proj_len()` read as the last row index.** It is the **number of projected months**,
   the frame's exclusive end, so the frame is `range(proj_len())` and the last row is
   `proj_len() − 1`. The anchor has 612 rows, 0 … 611, and
   `12(ω − x + 1) = 12 x (110 − 60 + 1) = 612`. An off-by-one either drops the last
   instalment on the term shapes — on point 9 that is ₩745,894.87 of outgo, 0.77% of the
   annuity total, a tenth of what the same slip cost on an annual grid — or projects a month
   past the end of the shipped table. *Test:* `len(result_cf()) == proj_len()` and
   `result_cf().index[-1] == proj_len() − 1` on every model point.
5. **Reading the mortality rate at the wrong end of the policy year.** `lives_if` applies
   the monthly conversion of the annual rate at the age attained at the **start** of the
   policy year, `x + t // 12`. Reading the age at the anniversary that ends it raises the
   factor's mortality by a year throughout and gives a 연금월액 of ₩412,381.78, **+2.23%**
   — close enough to the right answer to look plausible, where on the annual grid the same
   slip at least walked off the end of the table. A second version of the same error is
   available on a monthly grid and is worth naming: **dividing the annual rate by twelve**
   instead of converting it. `q(60)/12 = 0.0000672098` against
   `q^m(60) = 0.0000672347` looks like nothing in the first year and compounds the wrong way
   for fifty. *Test:* `check_lives_roll_fwd()`, which rebuilds the curve as an explicit
   product of `(1 − q^m)`.
6. **Running the model on 만나이 instead of 보험나이.** The tables, the model point column
   and the issue-age band are all 보험나이 [S7 제23조] [REG-R25 제21조](#krlib-reg-r25); the 완전생명표 and
   every Korean population statistic are 만나이 [REG-R38] [REG-R39]. The six-month rule
   makes the two differ for half of all issue dates, so the error is worth about half a
   year of ageing on every row and **raises nothing**. *Test:* the registry metadata
   records the basis per model, and the conventions suite reads it.
7. **Presenting `mort_table.csv` as the 경험생명표.** It is a **[std]** Makeham construction
   on three published anchors, misses the 보험나이 50 anchor by +22.01% for men, and the
   제10회 경험생명표 is not published at all [REG-R33] [REG-R34]. *Test:* every row of the
   CSV carries a `provenance` cell and the two fit-anchor rows say so.
8. **Recomputing the life-shape annuity from the fund each month.** `av_pp` on the life
   shape is **not** the reserve and goes negative around t = 330; an annuity re-struck as
   `V(t)/ä(x+t, ·)` would collapse toward zero and then turn negative. The 약관 bases the
   annuity on 「연금개시시의 계약자적립액」 [S7 별표1] and the ratchet is inert on an
   immediate annuity [S6 §10-라]. *Test:* `annuity_pp(t) == annuity_pp(0)` for every t on
   every life-shape point, and `check_rate_level()`.
9. **Flooring `av_pp` at zero on the life shape.** It hides the fact that a life annuity's
    fund is not its reserve and breaks the retrospective closed form
    `V(0)(1+j)^t − A s(t, j)` from the crossing onward. Nothing downstream reads the
    negative value: `cv_pp` is nil and surrender is impossible there. *Test:*
    `check_av_roll_fwd()`, and `av_pp(330) < 0` on point 1.
10. **Computing the retention once, at inception, instead of every month.** On a level rate
    the two agree and the fund still lands on M, so the error is **invisible on model
    points 6 and 7**. It appears only on a stepping rate: point 8's retention runs
    18,251.70 → 22,683.65 over 240 months and `av_pp(240) = 100,000,000.00` exactly
    because it is re-struck; an implementation that froze it lands ₩6,393,965 short.
    *Test:* `check_av_terminal()` and `check_av_roll_fwd()` on point 8.
11. **Reading the 최저보증이율 as a floor on the annuity.** It is a rate on the fund. Point
    8 is the demonstration: the 연금월액 falls **50.62%** from the first month to the 121st
    while the floor is honoured at every step and the fund reaches its maturity benefit
    exactly. *Test:* `crediting_rate(t) == min_guar_rate(t)` on the `min_guar` basis, and
    the annuity ratio `annuity_pp(120)/annuity_pp(0)` on point 8.
12. **Getting the floor's duration bands wrong.** The bands are half-open
    `[dur_from, dur_to)` in **completed policy years** and the grid counts months, so the
    test is on `t // 12`: `t = 0 … 59` is 1.25%, `t = 60 … 119` is 1.00%, `t >= 120` is
    0.75%. Testing on `t // 12 + 1` moves both steps a year early and testing on `t` itself
    moves them eleven years early. *Test:* `crediting_rate(59) == 0.0125` and
    `crediting_rate(60) == 0.0100` on point 8.
13. **Netting the 0.80% 연금수령기간 중 비용 off the policyholder's payment.** It is
    disclosed in the **cost** table, not the benefit table [S1 §VIII], so it is an insurer
    expense measured on the annuity and the annuitant receives the full amount — on the
    monthly grid, 0.80% of each 연금월액, which over twelve months is exactly the 0.80% of
    the 연금연액 the table discloses. Netting it would cut the anchor's income by ₩3,226.96
    a month and would also break the pricing identity, since the fund bought the gross
    annuity. Whether a carrier's own 산출방법서 builds it into the factor instead is
    **[unverified]**. *Test:* `expenses(t) == 0.008 * annuity_payments(t)` for t >= 1 on
    point 1.
14. **Paying a death benefit on the 종신연금형.** There is none after annuitisation:
    「별도의 사망보험금은 지급되지 않습니다」 [S5], the unpaid guaranteed instalments being
    what survives the annuitant, and they are already inside `annuity_payments`. Adding one
    double-counts the guarantee. *Test:* `claims_death(t) == 0.0` at every t on every
    life-shape point.
15. **Paying the death benefit on the fund at the start of the period.** Deaths are taken
    at the **end**, after the crediting and after the annuity due to the survivors, so the
    사망보험금 on the inheritance shape is `ρP + V(t + 1)` and not `ρP + V(t)`. On point 6
    at t = 0 that is `q^m x 105,066,551.06 = ₩30,957.20` rather than
    `q^m x 105,030,000.00 = ₩30,946.43` — a convention that on the monthly grid costs at
    most a month of fund growth where on an annual grid it cost a year's. *Test:* the traced
    value at point 6, t = 0.
16. **Applying a lapse decrement to the 종신연금형.** Surrender is contractually impossible
    from month one [S3] [S5 주2] [S7 제31조], and a life-shape model point carrying a
    surrender rate is a defect in the table rather than a scenario. *Test:*
    `check_surr_value()`, which asserts a nil rate **and** a nil surrender value at every
    duration on that shape.
17. **Letting a surrender fire in the final policy year.** `lapse_rate(t) = 0` for
    `t >= N − 12` on every shape. Without it a contract in its last year is surrendered a
    moment before its 만기보험금 and the maturity benefit is diverted into a surrender value
    of a different amount for no reason any contract states. Suppressing it over the whole
    year rather than the last month is also what makes the monthly in-force reproduce the
    annual-step model's at every 계약해당일. *Test:* `claims_lapse(t) == 0.0` for the last
    twelve rows of points 6, 7 and 9.
18. **Weighting the 만기보험금 by `pols_if(N − 1)` instead of `pols_if(N)`.** It is payable
    on survival **to** maturity, one further month of decrement away:
    ₩79,495,349.97 on point 6, against ₩79,539,188.73 if the earlier weight were used. The
    gap is now a month of decrement rather than a year's, so the slip is a tenth as
    expensive and correspondingly harder to see. *Test:* the maturity figure at point 6,
    t = 119.
19. **Applying the 100.1%-of-premiums fund floor.** It is a **deferred**-contract mechanic
    [S7 별표1 주8] [S9]; applying it to an immediate annuity would erase the entire 3.50%
    load on day one and make `check_premium_split()` fail by ₩3,600,000. *Test:*
    `av_pp_init() == 96,500,000.00` on point 1, i.e. below P.
20. **Discounting the projected flows at the crediting rate and calling it a reserve.**
    `disc_factor` exists for the pricing identity and for `retention_shortfall_pp()` only;
    the best estimate discounts on a supervisory curve [REG-R27] and the reserve is
    computed under 감독규정 제6-11조 [REG-R10], neither of which is in this model. *Test:*
    the model publishes no discounted column, and must not acquire one.
21. **Publishing a `claims` column beside the `claims_*` columns.** A statement must not
    carry its own subtotal beside its parts, or the columns stop summing to `net_cf`; the
    `claims(t, kind)` cells stays and the column does not. *Test:* `check_net_cf()`, which
    rebuilds the ledger from the **published** columns.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-immediate_annuity-r1
[R12]: #krlib-immediate_annuity-r12
[R17]: #krlib-immediate_annuity-r17
[R2]: #krlib-immediate_annuity-r2
[R21]: #krlib-immediate_annuity-r21
[R23]: #krlib-immediate_annuity-r23
[R25]: #krlib-immediate_annuity-r25
[R27]: #krlib-immediate_annuity-r27
[R28]: #krlib-immediate_annuity-r28
[R31]: #krlib-immediate_annuity-r31
[R6]: #krlib-immediate_annuity-r6
[REG-R10]: #krlib-reg-r10
[REG-R11]: #krlib-reg-r11
[REG-R13]: #krlib-reg-r13
[REG-R16]: #krlib-reg-r16
[REG-R18]: #krlib-reg-r18
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R24]: #krlib-reg-r24
[REG-R25]: #krlib-reg-r25
[REG-R26]: #krlib-reg-r26
[REG-R27]: #krlib-reg-r27
[REG-R3]: #krlib-reg-r3
[REG-R32]: #krlib-reg-r32
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R38]: #krlib-reg-r38
[REG-R39]: #krlib-reg-r39
[REG-R48]: #krlib-reg-r48
[REG-R5]: #krlib-reg-r5
[REG-R52]: #krlib-reg-r52
[REG-R58]: #krlib-reg-r58
[REG-R59]: #krlib-reg-r59
[REG-R60]: #krlib-reg-r60
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
