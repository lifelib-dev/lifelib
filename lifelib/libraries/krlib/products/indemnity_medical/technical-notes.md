# Technical Notes

**Status:** Draft, 2026-09-03 (all cited sources accessed 2026-09-03).

**Scope note.** These notes turn the standardized composite 4세대 실손의료보험
(*silson uiryo boheom*, fourth-generation indemnity medical insurance) of
`product-spec.md` (same directory) into a reference liability cash-flow projection on
paper, and then into `Medical_KR_S` beside it. **They describe no single insurer's
contract** — and on this product they could not, because the benefit definition is not
written by a carrier at all: it is the 표준약관 (*pyojun yakgwan*, standard policy
conditions) annexed to the 보험업감독업무시행세칙 at 별표 15 under 제5-13조제1항
[S1] [REG-R23] [REG-R25]. [S#] and [R#] tags resolve against `sources.md`, whose numbering
is carried verbatim from `_research/indemnity-medical.md` and is frozen; [REG-R#] tags
resolve against the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is separate and
also frozen. **[std]** marks a standardization introduced for the reference
implementation, always with a rationale and, where one exists, the observed range;
[unverified] marks a claim that could not be confirmed against a retrieved document.

**Every contractual parameter these notes share with `product-spec.md` carries the same
value there.** What these notes add is the whole modelling basis, which the specification
does not carry because none of it is contractual and none of it is public: the claim
**frequencies** by sex and age band, the eight **severity distributions** the deductibles
bite into, the ten-bucket **annual-claim shape** the experience-rating loop runs on, the
mortality and lapse decrements, and the expense and commission split. Every one of them is
introduced below as **[std]**, and the reason is a positive finding rather than a failed
retrieval: 보험개발원 is the statutory 보험요율 산출기관 under 보험업법 제176조
[REG-R4], and 실손의료보험 is **not** among the 장기손해보험 categories whose
참조순보험요율 it publishes [R20]; the 산출방법서, where an insurer's 예정위험률 and
예정사업비율 live, is a 기초서류 that is filed and never disclosed [REG-R2]. There is no
public Korean indemnity-medical morbidity or severity basis at all.

**This product stands alone in `krlib`.** It inherits nothing from
[whole life (종신보험)](../whole_life/technical-notes.md),
[term life (정기보험)](../term_life/technical-notes.md) or
[cancer (암보험)](../cancer/technical-notes.md), and no other product states a delta
against it. The reason is structural. 보험업감독규정 제7-63조제1항제2호 lets a 제3보험
benefit be designed on a 정액 (*jeongaek*, fixed-sum) basis **or** on the basis of
「실제 발생하는 손해(이하 "실손해"라 한다)」 [REG-R17] [R19], and this is the only
contract in the repository that takes the second branch. There is no 보험가입금액 that
*determines* a claim here, only an annual limit that *caps* one. So the model is

    claim = frequency x severity x (co-payment, deductible, per-visit cap,
                                    per-act money and count caps, annual aggregate)

and then — uniquely — the claim feeds back into next year's premium through the
비급여 할인·할증 (*bigeubyeo harin-halchung*, non-covered experience discount and
surcharge). That loop is modelled, not described.

Three structural facts orient everything below and are worth stating before any
arithmetic:

- **The contract is one year long.** It renews annually at the attained age and the
  then-current basis inside a supervisory corridor of ±25% per 위험구분단위, and it
  **re-enters** the then-current generation every five years [S1 제30조] [S1 제23조]
  [REG-R17 제7-63조제2항제3호·제6호나목](#krlib-reg-r17). The projection horizon is a *stated* one,
  not a contractual one.
- **The insured loss is exogenous.** Both halves of it — the statutory co-payment on
  treatment inside the public list and the whole of the treatment outside it — are set by
  the health ministry and by providers, not by the insurer [R7] [REG-R53]. The boundary
  between 급여 (*geubyeo*, treatment covered by 국민건강보험) and the 비급여 outside it moves
  within any realistic projection horizon.
- **Half the claim is truncated by a public scheme.** The 본인부담상한제 refunds a
  member's annual statutory co-payment above an income-graded ceiling, and the 표준약관
  excludes the refundable amount from cover outright [S1 제4조제3항제1호] [S1 제5조제3항]
  [R10] [REG-R53]. The 급여 half of the claim is therefore bounded above, and bounded
  differently by income decile. The 비급여 half is not bounded at all.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows** per policy issued —
  office premiums on the two separately re-rated priced units, the five benefit limbs,
  maintenance expense, claim-handling expense and commission — for a single model point,
  undiscounted and gross of reinsurance. Korea runs three measurement bases over one such
  stream and all three are live: K-IFRS 제1117호 mandatory since 2023-01-01 [REG-R60],
  K-ICS in the same quarter [REG-R13], and the 해약환급금준비금 that has no counterpart
  anywhere else in this repository [REG-R11]. This model stops deliberately before all
  three and keeps the cash flows basis-agnostic. **Discounting, the risk adjustment, the
  CSM, 요구자본 and every reserve are out of scope** and are cited, not reproduced — see
  *Valuation and reserve pointers*.
- **Projection frequency.** Monthly grid, because the product is: 월납 is the only premium
  mode retrieved and the whole published FSS premium series is monthly [S3] [S4] [R7]
  [R8]. `t` is the **policy month** and is **0-based**: the first projected month is
  `t = 0`, the frame is `t = 0, 1, …, proj_len() − 1`, and month `t` is the interval from
  `t` to `t + 1` months after the 계약일. `proj_len()` is the **number** of projected
  months — the exclusive end of the frame, not the last index — so `result_cf()` has
  `proj_len()` rows, 120 on the anchor cell. The **policy year** is the contractual
  1-based label `y = policy_year(t) = ⌊t/12⌋ + 1`, derived from `t` and never used to
  index the frame.
- **But every contractual mechanism is annual.** The 「연간」 of this contract is
  「계약일로부터 매1년 단위로 도래하는 계약해당일 전일까지의 기간」 [S1 제5조제2항] — a
  policy year from the contract date, not a calendar year. All four ₩50,000,000 limits,
  the ₩200,000 per-visit cap, the 100-visit count, the three 3대비급여 sub-limits, the
  ₩2,000,000 inpatient co-payment cap, the relativity lookback and the premium itself run
  on that clock and reset on it. So **every benefit and premium quantity is computed per
  policy year `y` and spread evenly across the twelve months of that year** — the month is
  a presentation grid for an annual quantity, not a unit of account. Cells that live on the
  policy year take `y` and never `t`; the library spells the two clocks apart on purpose.
- **Timing conventions [std].** Office premium received at the **start** of month `t`;
  claims, maintenance expense, claim-handling expense and commission at the **end** of
  month `t`; decrements at the end of month `t` in the order **mortality → lapse →
  suspension → renewal decline**, the renewal decline acting only where
  `(t + 1) mod 12 = 0`, and the maturity count only at `t = proj_len() − 1`. `pols_if(t)` is
  the **start**-of-month in-force probability and is the weight on every cash flow on the
  same `result_cf()` row. Nothing published fixes the decrement order and at these rates it
  is worth less than a basis point a year.
- **Within-year spread [std].** The annual claim is divided by twelve. No within-year
  seasonality for this product was retrieved, and since every contractual mechanism resets
  annually there is nothing for a seasonal pattern to interact with. The consequence to
  keep in view: a limit that binds part-way through a policy year in reality binds
  proportionally across all twelve months here.
- **Age basis — and the two conventions must both be stated.** The projection is on
  **만나이** (*man nai*, age last birthday), `age(t) = x + floor(t / 12)`, incremented at
  the policy anniversary. The **contract** is not: it prices and renews on **보험나이**
  (*boheom nai*, insurance age), the 만나이 at the 계약일 with a fraction under six months
  discarded and six months or more rounded up, and the 표준약관 works the arithmetic in its
  own example — 생년월일 1988-10-02, 계약일 2014-04-13, a difference of 25년 6월 11일 ⇒
  26세 [S1 제21조] [REG-R25]. The model carries 만나이 **[std]** because every calibration
  statistic available for this product is compiled on it — the NHIS coverage ratios by age
  band [R9] [REG-R41], the 생명표 decrement [REG-R38], the FSS premium series [R7] [R8] —
  and because a deterministic single-cell projection cannot represent the distribution of
  issue dates within the year that separates the two. **The two differ for half of all
  issue dates**, so the difference is a half-year of age on average, and it is recorded
  here rather than silently absorbed.
- **Termination and horizon.** `proj_len() = 12 × min(reentry_cycles × reentry_period,
  max_cover_age − x)`, a month **count**, so the last projected month is
  `t = proj_len() − 1`. With `reentry_period = 5`, `reentry_cycles = 2` and
  `max_cover_age = 100`, that is **two five-year 보장내용 변경주기 — ten policy years —**
  on every shipped model point; the age ceiling never binds on the shipped issue ages.
  The horizon is **stated**, and the distinction is the whole point.
  감독규정 제7-63조제2항제6호나목 requires the 보험기간 및 보장내용 변경주기 to be five
  years or less [REG-R17]; at the fifth 계약해당일 a 4세대 contract's benefit terms are
  replaced by whatever the supervisor is then prescribing, at a premium the insurer sets
  for that product [S1 제23조]. **No projection of this contract past the first 재가입 is a
  projection of *this* contract's terms.** The model assumes re-entry on unchanged terms,
  twice over, and says so.
- **Contract boundary.** Genuinely contestable, and this document asserts no answer: a
  one-year term, an unrestricted right to re-rate at renewal, a supervisor-set ±25% cap on
  that re-rating, a five-year re-entry into a wording the insurer does not control, and an
  obligation not to refuse re-entry on health grounds [S1 제23조제1항] [R2]. Nothing
  retrieved states an industry or supervisory position on where the IFRS 17 boundary falls
  for that combination [unverified]. Note the sentence that pulls the other way:
  「종전 계약을 자동갱신하거나 같은 회사의 보험상품에 재가입하는 경우에는 종전 계약의
  보험기간을 연장하는 것으로 보아」 [S1 제3조제6항] — for *benefit* purposes renewal and
  re-entry are continuations, not terminations.
- **Currency and rounding.** KRW throughout. Intermediates at full double precision.
  Displayed cash flows to **₩0.0001** and `pols_if` to ten decimals **[std]** — the
  expected values are fractional, the amounts are small, and the test suite asserts the
  worked example at the displayed precision. Monthly rows rounded for display do **not**
  re-add to the displayed annual totals; the totals are sums of unrounded values.
- **Model points.** One policy at a time, projected on a probability-weighted basis;
  `pols_if(t)` multiplies each per-policy cash flow, so `result_cf()` is a unit projection
  and scales linearly. `Projection` is parameterized by `point_id`; no aggregation logic is
  specified here. Ten model points ship; `point_id = 1` is the anchor cell of the
  *Worked example* below and the test suite's target.
- **Sign convention.** `net_cf` is **income-positive** — premiums less claims, less
  maintenance expense, less claim-handling expense, less commission. That is the
  library-wide sign and these notes' own, so unlike
  [whole life](../whole_life/technical-notes.md) and
  [immediate annuity](../immediate_annuity/technical-notes.md) there is **no
  outgo-positive `liability_cf` companion** to publish: one stream, one sign, one name.

---

## Model point attributes

| Attribute | Type | Anchor cell (`point_id = 1`) | Cells |
|---|---|---|---|
| `sex` | enum {M, F} | M | `sex()` |
| `issue_age` (`x`) | int, **만나이**, 0–65 **[std]** | 40 | `issue_age()` |
| `premium` (`P₀`) | KRW a month, office premium, first policy year only | **11,982** | `premium_mth_pp()` |
| `np_share` (`s`) | 비급여 share of the first-year premium | 0.60 **[std]** | `np_share()` |
| `np_rider` | bool — 실손의료보험 특별약관 (비급여) held | 1 | `np_rider()` |
| `three_np` | bool — 3대비급여형 held (inside the rider) | 1 | `three_np()` |
| `annual_limit` (`L`) | KRW a year per 보장종목 | 50,000,000 | `annual_limit()` |
| `visit_cap` (`Lv`) | KRW per outpatient visit | 200,000 | `visit_cap()` |
| `oop_decile` | int 1–10, NHI-contribution decile; the anchor's rung **[std]**, the scale itself [R10] | 6 | `oop_decile()` |
| `clinic_share` | share of 급여 통원 at the ₩10,000 tier | 0.63 **[std]** | `clinic_share()` |
| `nhi_covered` | bool — inside 국민건강보험 / 의료급여 | 1 | `nhi_covered()` |
| `trend_mult` (`k_trend`) | multiplier on both cost trends **[std]** | 1.0 | `trend_mult()` |
| `util_mult` (`k_util`) | multiplier on every claim frequency **[std]** | 1.0 | `util_mult()` |
| `reld_on` | bool — 요율 상대도 in operation | 1 | `reld_on()` |
| `noclaim_on` | bool — 무사고 할인 in operation | 1 | `noclaim_on()` |
| `suspend_rate` | annual 개인실손 중지 decrement **[std]** | 0.00 | `suspend_rate()` |
| `label` | str | `anchor 40M all covers full limit` | — |

Four of these deserve a note, because each is a model point column somewhere else in the
library and a *state* here.

**`premium` is an input, not a computed quantity, and it has an authoritative anchor.**
The joint FSC/FSS launch release prints **₩11,982** as the 4세대 premium for a 40세 남자 on
a 10-carrier 손해보험 average as at 2021-06, against 1세대 ₩40,749, 2세대 ₩24,738 and
3세대 ₩13,326 for the same insured [R1]. Age 40 male is also the 기준연령 요건 of
감독규정 제1-2조제2호 — 「전기납 및 월납 조건으로 남자가 만 40세」 — so the anchor cell is
the cell Korean supervisory disclosure is quoted on [REG-R9]. No age × sex rate scale
exists in public for any generation: the 손해보험협회 comparison grid is filtered by
성별 and 보험나이 and by nothing else, which is the disclosure's own confirmation that the
scale is an age × sex table, but the grid is POST-driven and returned
「조회된 내용이 없습니다」 to a plain fetcher [S7] [REG-R62]. The other nine model points'
premiums are therefore **[std]** and are round-number levels, set in the neighbourhood of
the anchor carried to the issue age at the 4.0% age slope but not computed from it — they
sit within about ±5% of `11,982 × 1.04^(x − 40)` at ages 35 to 65, further away at age 30,
and the age-0 rung is a floor rather than a slope value. Model point 5 is the exception
and is arithmetic: at `np_share = 0`, ₩4,793 is the anchor's 급여 half to the won. **Only
the first policy year is an input**; every later year is the renewal recursion of
`prem_ge_base` and `prem_np_base`.

**`oop_decile` is a model point attribute and not an assumption**, because the
본인부담상한액 is set by the insured's own income and the spread is nine-fold: on the 2026
scale a 1분위 insured is refunded everything above ₩900,000 a year and a 10분위 insured
everything above ₩8,430,000 [R10]. **The 급여 claim distribution is truncated, and
truncated differently by income.** That is why the 비급여 half, which has no such
truncation, was 57.1% of all claims paid in 2025 against a 15.8% share of national spend
[R7] [R9].

**`nhi_covered` is a state, not an event.** Where the insured falls outside
국민건강보험법 제5조·제53조·제54조 or the 의료급여법 equivalents — most commonly a
suspension of entitlement — reimbursement falls to **40%** of the amount actually borne on
both parts, still within the annual limit [S1 제3조제3항제1호] [S1 특별약관 제3조제8항]. It
persists while entitlement is suspended, so it belongs on the model point and not in a
transition. The wording states the **reimbursement**; this model states the **retention**,
`retain_rate_nonhi = 0.60` **[std]**, with the flat outpatient deductible floors unchanged
on top. `nhi_covered = 0` also switches the 본인부담상한제 off, because a life outside the
scheme is not refunded by it.

**`clinic_share` carries the provider mix, which is a first-order variable here and in
nothing else in the library.** The 표준약관's 급여 통원 deductible table has exactly two
rows — ₩10,000 at 의료법 제3조제2항 institutions other than 종합병원, at
보건소·보건의료원·보건지소, at 보건진료소 and their pharmacies; ₩20,000 at 전문요양기관,
상급종합병원, 종합병원 and their pharmacies [S1 기본형 제3조 <표1>]. 0.63 is the 2025 claim
split by provider class — 의원 32.0%, 병원 21.8%, 요양병원 2.8% against 종합병원 17.6% and
상급종합 15.0% [R7] — normalised over the named classes **[std]**.

---

## State variables

| Variable | Description | Updated | Cells |
|---|---|---|---|
| `pols_if(t)` | In-force probability at the **start** of month `t`; `pols_if(0) = 1` | monthly | `pols_if(t)` |
| `age(t)` | Attained 만나이, `x + floor(t/12)` | annually | `age(t)` |
| `policy_year(t)` | `floor(t/12) + 1`; the clock every contractual limit runs on | annually | `policy_year(t)` |
| `util_band(y)` | Lower edge of the five-year utilisation band at the attained age | annually | `util_band(y)` |
| `prem_ge_base(y)` | 급여 주계약 기준보험료 a month — **a recursion in `y`, and therefore state** | annually | `prem_ge_base(y)` |
| `prem_np_base(y)` | 비급여 특약 기준보험료 a month, likewise | annually | `prem_np_base(y)` |
| `claims_np_rated_pp(y)` | The rated 비급여 claim of year `y`; it is *year `y+1`'s* band input | annually | `claims_np_rated_pp(y)` |
| `band_share(y, b)` | The 요율 상대도 band mix at the renewal opening year `y` | annually | `band_share(y, b)` |
| `noclaim_share(y)` | Share earning the 무사고 할인 — a **two-year** reach-back | annually | `noclaim_share(y)` |
| `mort_rate_mth(t)`, `lapse_rate_mth(t)` | Monthly decrement rates applied in month `t` | lookup | — |
| `net_cf(t)` | Net cash flow of month `t`, insurer perspective, income-positive | monthly | `net_cf(t)` |

**All of this product's memory is in the premium, and none of it is in the benefit.** That
is the exact inverse of the
[jplib medical chassis](../../../jplib/products/medical/technical-notes.md), whose 通算 day
ledgers carry benefit consumption across the whole of life while the premium is level and
never looks back. Here every benefit limit — the four ₩50,000,000 aggregates,
the three 3대비급여 money caps, the two 50-act counters, the 100-visit cap, the ₩2,000,000
inpatient co-payment cap — **resets at each 계약해당일** [S1 제5조제2항], so no benefit
ledger survives a policy year and there is no cross-year benefit state to carry at all. The
premium, by contrast, is a recursion: `prem_ge_base` and `prem_np_base` each depend on their
own prior value, the band mix depends on the prior year's claim, and the 무사고 할인 depends
on the two prior years. A modeller arriving from `jplib` will look for a ledger and should
not build one; a modeller arriving from a level-premium chassis will look for a fixed
premium and must not hard-code one.

**The band state is memoryless, and that is sourced.** 「보험금 지급(사고) 이력이 1년마다
초기화됩니다 … `21년 지급보험금을 많이 받은 경우 → `22년 보험료 할증, `22년 무사고 →
`23년 보험료는 할인등급(1등급)으로 초기화」 [R2]. A single bad year cannot compound into a
permanently higher premium and a single clean year returns the policyholder to the discount
band. So the band at renewal `y` is a function of the claim experience of year `y − 1`
alone: **there is no no-claims ladder and no Markov chain to carry**, and `band_share(y, b)`
is simply the annual-claim distribution of year `y − 1` read against fixed money thresholds.
That is what makes the loop tractable in a projection model at all.

**Four absences are product facts, not gaps.**

- **No surrender-value state.** 「이 상품은 1년만기 순수보장성 상품으로 해약환급금이
  발생하지 않습니다」 [S3], so there is no `cv_pp`, no `claims_lapse`, no
  보험계약대출 and no 보험료 자동대출납입. A missed premium really does lapse the policy:
  a 납입최고 of at least 14 days runs and the contract terminates the day after it ends
  [REG-R25 제26조](#krlib-reg-r25), and 표준약관 제33조 excludes 「순수보장성보험 등」 from policy lending
  anyway. A policyholder who cancels mid-term recovers the 미경과보험료 under
  상법 제649조 [REG-R49], which is a return of premium and not a surrender value.
- **No death benefit.** 감독규정 제7-63조제1항제1호 requires *every* 제3보험 product to
  pay the 계약자적립액 and the 미경과보험료 of 제7-66조제5항 on death from a non-covered
  cause [REG-R17] [REG-R25 제22조](#krlib-reg-r25); on a one-year pure protection contract the
  계약자적립액 is nil to the precision this model works at, so the payment reduces to the
  return of unearned premium and there is no `claims_death`. **This is the only place in
  `krlib` where that provision has no financial content** — in
  [cancer](../cancer/technical-notes.md) and
  [long-term care](../long_term_care/technical-notes.md) the same clause forces an account
  balance into a non-savings product. Mortality here is a pure liability *release*.
- **No waiting period** on the general cover: cover attaches at 보장개시 and the only
  deferred item is a two-year wait on the 불임관련 질환 급여 cover introduced at 4세대
  [S1 제24조] [R1]. That is unusual among Korean health products and is a direct
  consequence of the indemnity form — there is no lump sum to anti-select against.
- **No premium waiver.** No 납입면제 provision appears in either retrieved 실손 wording
  [S1] [S3]. The absence is **[unverified]** as an absence rather than proved, and it is
  the one place these notes would change materially if a wording turned up that had one.

---

## Assumption inputs

### (a) Contractual / guaranteed elements (cited; the insurer cannot change them)

Every row here is a clause of the 표준약관 or of 감독규정 제7-63조. **This product's
benefit half reaches a citation precision no other product in this repository reaches**,
and the reason is that its benefit definition is a piece of published subordinate
legislation rather than a carrier document [S1] [REG-R23] [REG-R25].

| Input | Value | Cells / Reference | Basis |
|---|---|---|---|
| 급여 입원 자기부담률 | **20%** of 본인부담금; benefit is 「본인부담금의 80%」 | `retain_rate_ge_base = 0.20` | [S1 기본형 제3조] |
| 급여 입원 annual co-payment cap | Retained inpatient co-payment above **₩2,000,000** a policy year is reimbursed | `cap_inpatient_retain = 2000000` | [S1 제5조제4항] [REG-R17 제7-63조제2항제2호](#krlib-reg-r17); also in a 2세대 document [S4] |
| 급여 통원 deductible | `max(d_tier, 20% × cost)`, `d_tier` = **₩10,000** clinic tier / **₩20,000** hospital tier | `ded_clinic`, `ded_hospital` | [S1 기본형 제3조 <표1>] |
| Per-visit outpatient cap | **₩200,000**, both limbs | `visit_cap()` | [S1 제5조제5항] |
| 비급여 입원 자기부담률 | **30%** of the non-covered cost excluding the room differential | `retain_rate_np_base = 0.30` | [S1 특별약관 제3조] |
| 상급병실료 차액 | **50%** of the non-covered room charge, capped at **₩100,000 per day averaged over the whole admission** | `room_rate = 0.50`, `room_cap_day = 100000` | [S1 특별약관 제3조] |
| 비급여 통원 deductible | `max(₩30,000, 30% × cost)` — **flat at every provider**, not tiered | `ded_np_out = 30000` | [S1 특별약관 <표1>] |
| 비급여 통원 count cap | **100 visits** a policy year; the only count limit outside 3대비급여 | `visit_limit_np = 100` | [S1 특별약관] |
| Annual limit | **₩50,000,000** a policy year per 보장종목; 상해 and 질병 carry separate limits | `annual_limit()` | ceiling [S1 제5조]; election **[std]** |
| 3대비급여 money limits | 도수·체외충격파·증식 **₩3,500,000**; 주사료 **₩2,500,000**; MRI **₩3,000,000** | `limit_physio`, `limit_inject`, `limit_mri` | [S1 특별약관 제3조(3) <표1>] |
| 3대비급여 count limits | **50 acts** shared by the physical-therapy trio; **50 acts** for injections; **none** for MRI | `act_limit_three = 50` | [S1 특별약관 제3조(3) <표1>] |
| Physical-therapy re-assessment gate | First **10** acts unconditional, then 「10회 단위로」 to 50 on documented clinical improvement | `physio_gate_acts = 10` | [S1] [R2] |
| Injection carve-out | 항암제, 항생제 (항진균제 포함) and 희귀의약품 leave the ₩2,500,000 sub-limit for the main ₩50,000,000 limit | `inject_carve_share` | [S1 특별약관 제3조(3)제2항] |
| Non-NHI branch | Reimbursement falls to **40%** of the amount borne, both parts | `retain_rate_nonhi = 0.60` | [S1 제3조제3항제1호] [S1 특별약관 제3조제8항] |
| 본인부담상한제 exclusion | Amounts refundable ex ante or ex post by the NHIS are **excluded from cover** | `oop_trunc(y)` | [S1 제5조제3항] [S1 제4조제3항제1호] [R10] [REG-R53] |
| 요율 상대도 bands | 1단계 solved; 2단계 **100%**; 3단계 **200%** ≥ ₩1,000,000; 4단계 **300%** ≥ ₩1,500,000; 5단계 **400%** ≥ ₩3,000,000 | `band_thr_3/4/5`, `reld_r2..r5` | [S1 특별약관 제6조제3항] [REG-R25] |
| Surcharge floor | No surcharge at all below **₩1,000,000** of prior-year 비급여 claims | `band_of()` | [S1 특별약관 제6조제4항] |
| Relativity exemptions | 산정특례 conditions, and **all** claims of an insured graded 장기요양 1·2등급 | `reld_exempt_share` | [S1 특별약관 제6조제3항] [REG-R54] |
| Relativity is revenue-neutral | 「상대도 적용 전·후의 총 보험료 수준이 일치하도록」 — the discount is **solved**, not set | `reld_solved(y)` | [S1] |
| Relativity base | The **rider 순보험료 only**; 「비급여 특약 보험료만 할증되며」 | `prem_gross_mth(y)` | [S1] [R2] |
| Renewal corridor | **±25%** a year excluding the age effect, **per 위험구분단위**, applied to the **pre-relativity** premium | `renewal_corridor = 0.25` | [S1 제30조제2항] [S1 특별약관 제6조제2항] [REG-R17 제7-63조제2항제3호·제3의2호](#krlib-reg-r17) |
| 무사고 할인 | **10%** of the whole office premium after **two** consecutive claim-free years | `noclaim_disc = 0.10` | [R1] [S3] |
| 보장내용 변경주기 | **5 years**; re-entry into the generation then on sale, **no health underwriting** | `reentry_period = 5` | [S1 제23조] [REG-R17 제7-63조제2항제6호나목](#krlib-reg-r17) |
| Maximum cover age | 보험나이 **100** | `max_cover_age = 100` | [S3] [S4] |
| Policy year | 「계약일로부터 매1년 단위로 도래하는 계약해당일 전일까지의 기간」 | `policy_year(t)` | [S1 제5조제2항] |
| Surrender value | **Nil** | — | [S3] |
| Death benefit | **Nil** beyond the 미경과보험료 | — | [REG-R17 제7-63조제1항제1호](#krlib-reg-r17) [REG-R25 제22조](#krlib-reg-r25) |
| Indemnity ceiling | 「실제 발생한 손해(비용)를 초과하여 보험금을 지급하지 않습니다」 | `check_indemnity()` | [S1 제37조·제38조] [S3] |

Two contractual mechanics are **specified and implemented but deliberately not exercised**
by the base run, and both are named rather than hidden. The 3대비급여 gates are hard and
neither is pro-rated: the wording works two cases — ₩3,500,000 exhausted after 30 treatments
on 2022-10-31 excludes cover for the following **151 days** to the 계약해당일 2023-04-01;
50 treatments used with only ₩3,000,000 paid excludes cover for **182 days** [S1]. The limit
that binds first stops cover for the rest of the policy year and only the anniversary
restores it, which makes a 3대비급여 claim stream a **censored counting process with an
annual reset**, not a rate. And the counting rules are asymmetric, each a real modelling
instruction [S1 특별약관 제3조(3)제4항]: two or more of the physical-therapy trio at one
visit are **each** counted and **each** separately deducted; two or more injections at one
visit are **one** act with one deduction; MRI at two sites, or the same site twice, are
**separate** acts each with its own deduction. Read against the ₩30,000 per-act floor, the
injection rule is worth money to the insurer and the MRI rule worth money to the insured.

### (b) Insurer-discretionary current elements

This class is small, and what is in it is not what a sister library would expect.

| Input | Snapshot value | Basis |
|---|---|---|
| The **rate scale** itself | The insurer's own, unpublished, in the 산출방법서 | [REG-R2]; there is no 실손 참조순보험요율 to fall back on [R20] |
| 보험가입금액 and per-visit cap menu | Carrier-selected inside the 표준약관's ceiling; ₩50m/₩30m/₩10m with ₩200k/₩150k/₩100k on a 5세대 menu | [S1 제5조] [S3]; composite takes the maximum **[std]** |
| 가입나이 envelope | A 사업방법서 matter, not published; 0–49 on one 2세대 direct product | [S4] [REG-R2]; composite 0–65 **[std]** |
| Band-1 discount level | **Solved** from neutrality, not chosen — but the insurer picks the band distribution it solves on | [S1]; **[std]** cap at 5% |
| 의료급여 수급권자 할인 | 5% of office premium at one carrier; **not** in the composite | [S3]; **[std scope]** |
| Basis increment `b(y)` at renewal | The insurer's own re-rate, bounded at ±25% per 위험구분단위 | [S1 제30조] [REG-R17]; derived here **[std]**, see (c) |

**What is *not* discretionary is the striking part.** There is no policyholder dividend —
the contract is 순수보장성 with no 계약자적립액 to distribute [S3]. There is no 공시이율,
no MVA and no non-guaranteed charge scale. And **the benefit is not discretionary at all**:
it is the supervisor's text, so the whole of what a `jplib` or `uklib` product would treat
as "current benefit practice" is legislation here. The one genuinely discretionary lever the
insurer holds is the **price**, and even that is bounded by a corridor, verified annually
against experience under 감독규정 제7-63조제2항제6호가목, and disclosed at every renewal
as a 보험가격지수 under 제7-45조제7항 [R12] [REG-R17] [REG-R22].

### (c) Behavioral / experience assumptions (modeler's view — all [std])

**Nothing in this subsection is sourced to a rate table, because no rate table for this
product exists in public.** What the supervisor does publish, annually and in quantity, is
*aggregate* experience [R7] [R8] [R12] [REG-R44], and every assumption below is anchored on
it and says which anchor it used. Where an anchor bounds the value the bound is given; where
none does, that is said.

**Mortality.** `mort_table.csv` is a **[std]** Makeham construction,
`q(x) = 1 − exp(−(A + B·c^x))` above age 15 with a log-linear child schedule below it,
fitted to the four summary statistics 국가데이터처 publishes — 기대수명 at birth, 기대여명
at 40 and at 65, and survival to age 80 [REG-R38]. It is **not** a transcription: 제10회
경험생명표, the industry table applied from 2024-04, is not published in full, and the
single-year 완전생명표 qx tables live behind KOSIS and were not downloaded [REG-R39]. The
male fit gives e₀ = 80.585 against a published 80.8, e₄₀ = 42.334 against 41.9, e₆₅ =
19.455 against 19.5 and S(80) = 0.6426 against 0.644; the female fit 86.370 / 47.666 /
23.657 / 0.8215 against 86.6 / 47.4 / 23.7 / 0.822. Parameters: male A = 0.001013180423,
B = 1.866071456e-06, c = 1.136151863; female A = 0.0006442732347, B = 9.693652414e-08,
c = 1.168822705; child schedule log-linear between q(0) = 0.0025, q(1) = 0.0003,
q(5) = 0.0001, q(10) = 0.00008, q(15) = 0.00012; q(110) = 1. Every row carries a
`provenance` column pointing at [REG-R38], never at a copy of a table.

**The direction of prudence on mortality is inverted here and it matters.** On every
protection product in this library an understatement of mortality understates the
liability. On this one **death releases the liability** — the contract pays nothing on
death beyond the 미경과보험료 — so an *over*-statement of mortality is
*anti*-conservative. `mort_rate_mth(t) = 1 − (1 − q)^(1/12)` **[std]**, a uniform force
across the policy year.

**Lapse.** `lapse_table.csv`, annual by policy year, **[std]**: 0.100, 0.060, 0.045, 0.035,
0.030, 0.026, 0.024, 0.022, 0.021, **0.020** for policy years 1–10, the last row applying to
every later year. No 실손-specific persistency table is published. The ultimate is anchored
on the only 실손-specific figure there is — the 1–3세대 in-force block fell **3.3%** in 2025
[R7] — which blends lapse, death and conversion, so 2.0% is what is left of it once
mortality and the renewal decline are taken out. The first-year rate is set against an
[unverified] 장기손해보험 13회차 유지율 of about 86%, from a news summary rather than a
retrieved disclosure. `lapse_rate_mth(t) = 1 − (1 − w)^(1/12)` **[std]**. This is
**non-payment lapse only**; the policyholder's separate right to decline the annual renewal
is a different act and carries its own rate.

**Renewal decline [std].** `renewal_decline_rate = 0.01` a year, acting only in the twelfth
month of each policy year. The asymmetry is contractual: the policyholder may decline
renewal and the insurer may not, within the 변경주기 and the age range and provided the
prior premium was paid [S5] [S3]. So this is a **policyholder option on a contract the
insurer cannot exit**, and it is the residual of the 3.3% blended decay after lapse and
mortality [R7]. No published 실손 renewal-decline series exists.

**Utilisation — the claim frequencies, and what they are frequencies *of*.**
`utilisation_table.csv` carries, per policy per year by sex and five-year age band:
`adm_rate` (admissions), `visit_rate_ge` and `visit_rate_np` (outpatient visits on each
side), `act_rate_physio`, `act_rate_inject` and `act_rate_mri` (3대비급여 acts), plus
`los_days`, the mean length of stay the room-differential daily-average cap is applied
against. These are frequencies of events **giving rise to a paid claim**, averaged over the
whole population including the roughly **65% of insureds who claim nothing in a year**
[R4] [R5], which is why they look low against national utilisation.

- **The level is *solved*, not assumed.** Three scalars — admissions, 급여 outpatient
  visits, and everything 비급여 — are chosen so that the anchor cell's first policy year
  reproduces the published 4세대 2022 상반기 loss ratios on the published 2021 premium
  anchor: 급여 **97.5%** of ₩4,792.80 × 12 and 비급여 **73.0%** of ₩7,189.20 × 12, i.e.
  ₩56,075.8 and ₩62,977.4 [R12] [R1]. The model produces ₩56,076.22 and ₩62,978.25.
  The 비급여 solve additionally needs an **inpatient share of the 비급여 claim** of
  **0.30 [std]**, because one admission drives both halves of the claim.
- **The age curves and sex factors are shapes [std]**, following the NHIS coverage ratios
  by age band [R9] [REG-R41]. There is deliberately **no maternity bump** in the female
  rows, because pregnancy and childbirth are excluded from 4세대 cover.
- **A published grid exists and is not used for the level, and that must be said.**
  보험개발원's 장기손해보험 참조순보험요율 display carries a **질병입원율** grid by age and
  sex [REG-R61]. It is a 장기손해보험 fixed-benefit hospitalization incidence — an
  *insured-event* rate on a 참조순보험요율 (net premium) footing — and not a count of
  admissions producing a payable indemnity claim after a 20% co-payment; and a reference net
  rate is not a best estimate. It is therefore available as an external anchor for the
  **age slope** of `adm_rate` and is not used for the **level**. Substituting it, and
  restating the level solve against it, is the first thing a user with company data should
  try. **실손 위험률 itself remains unpublished** [R20].

**Severity — eight discrete distributions, because a mean is unusable here.**
`severity_table.csv` gives cost-probability pairs per event for `ge_in`, `ge_out`, `np_in`,
`np_room`, `np_out`, `physio`, `inject` and `mri`. The reason the *shape* and not the mean
is needed is the deductible: it is `max(flat floor, percentage × cost)`, a flat amount below
a crossing point and a percentage above it, so the payment is a **kinked** function of cost
and `E[f(X)] ≠ f(E[X])`. The dispersion being standardized over is real and published —
the 건강보험심사평가원 price survey found 도수치료 quoted anywhere between **₩5,000 and
₩600,000** across Seoul hospitals [R2] — and a mean would erase it. *Worked example* below
quantifies the error a mean makes on each stream; on the 비급여 통원 limb it is **+35.8%**.

**The annual-claim shape — the one table whose dispersion is the whole point.**
`claim_shape_table.csv` gives the distribution of a policy's **annual rated 비급여 claim**
across ten buckets as a share and a representative amount. The 요율 상대도 band is decided
by where a policy's annual claim falls against **fixed money thresholds**, so the band mix is
a property of the distribution and not of its average. Bucket 0 carries the **72.9%** of
contracts assessed with no rated claim [R12]; the six 2단계 buckets take their within-band
dispersion from the **six lowest bands** of the published 4세대 claim-size distribution — the
0–10만 / 10–20만 / 20–50만 / 50–100만 / 100–200만 / 200–500만 rows at 3.7 / 6.0 / 16.3 /
17.7 / 18.9 / 22.2% of claimants, normalised over themselves and with each band's midpoint
scaled by one common factor onto the sub-₩1,000,000 range 2단계 occupies [R12]; and the
three upper buckets carry the published commencement shares 0.8 / 0.7 / 0.3 [R12]. The
amounts are scaled so that the tabulated mean equals the anchor's year-1 rated claim, which
is what makes the solved band-1 relativity come out at the specification's 0.9575. The model
reads the amounts as **multiples of the table's own mean** and rescales them to whatever
claim level it is projecting, so the same shape serves every model point and every year.
**The zero-claim mass is held constant at 0.729012 [std]** — the shape trends its amounts
and not its frequency — which is a stated limitation: in reality the frequency of claiming
rises with age too and the 1단계 share would fall.

**Relativity exemptions.** `reld_exempt_share = 0.15` **[std]**: the share of the rider
claim struck out of the rating count for 산정특례 conditions and 장기요양 1·2등급 insureds
[S1 특별약관 제6조제3항] [REG-R54], anchored on the 15.0% of 2025 claims the supervisor
attributes to 암 and 뇌·심혈관질환 [R7]. **The severely ill are exempt from the experience
rating**, and that is a direct statutory cross-reference between this model and
[LTC (간병보험)](../long_term_care/technical-notes.md) — the only such link in the library.

**Cost trends, and the re-rating rule they drive.** `med_trend_ge = 0.010` and
`med_trend_np = 0.081` **[std]**, from the 국민건강보험공단 진료비 실태조사: in 2024 the
scheme's own outlay grew 4.3%, the statutory co-payment **1.0%** and 비급여 **8.1%**
[R9] [REG-R41]. **비급여 is compounding at roughly twice the rate of the whole, and it is
the half of the claim with no public price.** The re-rating rule follows from them and is
itself **[std]**: each priced unit is re-rated at its own claim trend, clipped to the
corridor,

    b_u(y) = clip( med_trend_u × k_trend, −0.25, +0.25 )   for u in {ge, np}

so `b(y)` is **derived and not an input**. It keeps each unit's loss ratio stable against
its own cost trend unless the corridor clips it — which is exactly what happens on model
point 10.

**Age loading.** `age_load = 0.04` — **the only published age-slope datum in any retrieved
document**, and a derived one. The 표준약관's five-year renewal illustration prints
나이증가분 of 560, 728, 946, 1,230 and 1,599 against base premiums of 14,000, 18,200,
23,660, 30,758 and 39,985, and each is exactly **4.0%** of the previous year's base
[S1 제30조]. It is stylised, at an unnamed age, and it is what the model uses.

**Expenses and commission [std].** The only expense datum retrieved for this product is the
aggregate: 손해조사비 plus 사업비 of about **₩2.9조 on ₩18.0조** of 2025 premium — **16.1%**
— which reconciles with the FSS's stated break-even 경과손해율 of 「약 85% 수준」 [R7]. No
상품요약서 with a 사업비 disclosure was obtained for any generation. The split is therefore
**[std]** and `check_expense_split()` ties it back to the published total:

| Component | Rate | Base | Cells |
|---|---|---|---|
| Commission | **6%** | office premium | `comm_rate` |
| Maintenance expense | **7%** | office premium | `expense_maint_rate` |
| Claim handling | **3%** | **claims**, not premium | `expense_claim_rate` |
| Total, the published aggregate rounded | **16%** | office premium | `expense_total_rate` |

The published figure is **16.1%**, and the 16% the model carries is that figure rounded
**[std]**; the three components are a [std] decomposition of it and none of them is
separately published. Two choices inside that table are deliberate. **Claim handling is 3%
of claims and not of premium**, because 손해조사비 is claim-driven and because the
experience-rating machinery makes claim frequency a driver of expense as well as of
benefit; the two bases coincide at a loss ratio of **100%**, which is about where this line
has actually run — 101.0% in 2025 [R7] — and which is why the aggregate can be read either
way. And there is **no month-0 acquisition strain at all** — a product fact rather than an
omission. On a one-year renewable contract renewed on a rolling basis the
acquisition/renewal distinction has no content after the first year, so what a sister
library books as acquisition expense is carried here as a level commission rate on every
premium.
감독규정 제4-32조제5항 caps first-year commission on a 보장성보험 at the first year's
premium and is nowhere near binding at 6% [REG-R22].

**Two behaviour assumptions with no evidence behind them, both stated as such.**
`physio_cont_prob = 0.60` **[std]** is the probability that a physical-therapy course
continues past each ten-act clinical re-assessment boundary; **this is the only place in
`krlib` where a benefit is gated on a clinical review rather than on a definition**, and no
observed range is published. And successive years' claiming is assumed **independent**
**[std]**, which is what lets `noclaim_share(y) = w₁(y−1) × w₁(y)`; nothing published gives
the persistence of claiming from one year to the next.

**Two more [std] shares that bind nowhere and must still be stated.**
`share_injury = 0.15` splits the raw claim between 상해 and 질병 so that each can be capped
at its own ₩50,000,000 limit; and `inject_carve_share = 0.25` is the 항암제·항생제·희귀의약품
share leaving the ₩2,500,000 injection sub-limit for the main 비급여 limit. Given that
non-covered injections were **₩2.81조, 18.5% of all claims, in 2024** [R8], where that
boundary is drawn is a first-order calibration question and not a detail.

---

## Cash flow components and recursions

### Notation

| Symbol | Meaning | Cells |
|---|---|---|
| `t` | policy month, 0-based: `t = 0 … proj_len() − 1` | — |
| `proj_len` | the **number** of projected months, the exclusive end of the frame | `proj_len()` |
| `y`, `y(t)` | policy year, the contractual 1-based label `floor(t/12) + 1` | `policy_year(t)` |
| `x`, `age(t)` | 가입나이 (만나이); attained age `x + floor(t/12)` | `issue_age()`, `age(t)` |
| `b(y)` | lower edge of the five-year utilisation band at `age` in year `y` | `util_band(y)` |
| `l(t)` | in-force probability at the **start** of month `t` | `pols_if(t)` |
| `q(t)`, `w(t)` | monthly mortality, monthly lapse | `mort_rate_mth`, `lapse_rate_mth` |
| `u(t)`, `d_ren(t)` | monthly 개인실손 중지 decrement; renewal decline at the year end | `suspend_rate_mth`, `renewal_decline` |
| `n_adm`, `n_ge`, `n_np` | admissions, 급여 통원 visits, 비급여 통원 visits a year | `adm_rate`, `visit_rate_ge`, `visit_rate_np` |
| `a_ph`, `a_in`, `a_mr` | 3대비급여 acts a year: physio trio, injections, MRI | `act_rate_*` |
| `D(y)` | mean length of stay per admission, days | `los_days(y)` |
| `f_ge(y)`, `f_np(y)` | cumulative cost trend from year 1, `(1 + m_u·k_trend)^(y−1)` | `trend_ge`, `trend_np` |
| `r_ge`, `r_np` | 자기부담률: 0.20 / 0.30, or 0.60 either side outside NHI | `retain_rate_ge/np()` |
| `X_j`, `π_j` | severity point and its probability, per stream | `sev_points(stream)` |
| `μ_S` | mean cost of one event of stream `S` | `sev_mean(stream)` |
| `C_ge(y)` | 급여 본인부담금 incurred in year `y`, before truncation | `oop_incurred_ge(y)` |
| `S` | 본인부담상한액 for the model point's decile | `oop_ceiling()` |
| `τ(y)` | 본인부담상한제 truncation factor, `min(1, S / C_ge(y))` | `oop_trunc(y)` |
| `Λ` | annual limit per 보장종목, `Lv` per-visit cap | `annual_limit()`, `visit_cap()` |
| `σ` | 상해/질병 split of the raw claim, 0.15 | `share_injury` |
| `g_ge(y)`, `g_np(y)` | annual-limit survival factors on the two main limbs | `ge_limit_factor`, `np_limit_factor` |
| `C(y)` | rated 비급여 claim of year `y`, exemptions removed | `claims_np_rated_pp(y)` |
| `ρ_k`, `π_k` | claim-shape bucket `k`'s amount as a multiple of the shape mean, and its share | `shape_rel(k)`, `shape_share(k)` |
| `w_b(y)`, `r_b` | band share and band relativity at the renewal opening year `y` | `band_share(y,b)`, `band_relativity(b)` |
| `Σ(y)` | surcharge pool, `Σ_{b≥2} w_b r_b` | `reld_surcharge(y)` |
| `r₁(y)`, `R(y)` | band-1 relativity after the cap; average relativity applied | `reld_one(y)`, `reld_avg(y)` |
| `nc(y)` | share of contracts earning the 무사고 할인 | `noclaim_share(y)` |
| `a` | age loading at renewal, 0.04 | `age_load` |
| `b_ge(y)`, `b_np(y)` | basis increments, each clipped to ±0.25 | `basis_incr_ge/np(y)` |
| `G_ge(y)`, `G_np(y)` | the two 기준보험료 a month | `prem_ge_base`, `prem_np_base` |
| `G(y)` | office premium a month | `prem_gross_mth(y)` |

**Dimensional check, and the error it catches.** `n_adm`, `n_ge`, `n_np`, `a_ph`, `a_in`,
`a_mr` are **events per policy-year**; `q`, `w`, `u`, `d_ren`, `π_j`, `π_k`, `τ`, `g` and
every `r`, `w_b`, `R` are **dimensionless**; `D` is **days**; `X_j`, `μ_S`, `C_ge`, `S`,
`Λ`, `Lv`, `C`, `G` are **KRW**; `room_cap_day` is KRW/day, so `room_cap_day × D` is KRW per
admission. `n_adm × μ_ge_in` is KRW per policy-year and dividing by 12 gives KRW per
policy-month. The error this catches is the one an actuary arriving from a fixed-benefit
health product makes without noticing: **there is no benefit amount to multiply by.** A rate
times a 보험가입금액 has the dimensions of money but is not this contract's claim, and any
formula in which `annual_limit()` appears as a multiplier rather than inside a `min` is
wrong by construction.

### The reimbursement machinery, in the order it must be applied

Everything in this product is a rule for reducing an incurred cost to a payable amount, and
**the order matters**. The supervisor's own identity — 「실손의료보험은 피보험자(환자)가
부담하여 실제 발생한 의료비[급여 본인부담금 + 비급여] 중 일정 금액을 보상하는
보험상품」 [R7] — fixes what goes in; five steps fix what comes out.

**Step 1 — 본인부담상한제 first, as an exclusion from covered loss.**

    C_ge(y) = ( n_adm(y)·μ_ge_in + n_ge(y)·μ_ge_out ) · f_ge(y)
    τ(y)    = min( 1, S / C_ge(y) )        ( ≡ 1 where nhi_covered = 0 )

and `τ(y)` multiplies **both** 급여 limbs and the 급여 half of the incurred covered loss.
국민건강보험법 제44조제2항 creates the scheme and the NHIS refunds the excess of a member's
annual 본인일부부담금 over the ceiling [REG-R53], operated as 사전급여 and 사후환급 [R10];
the 표준약관 then excludes the refundable amount **twice over**, at 제5조제3항 and at
제4조제3항제1호 [S1]. So the 급여 half of the claim is bounded above, per insured per year,
at roughly `0.80 × S` — ₩720,000 for a 1분위 insured on the 2026 scale and ₩6,744,000 for a
10분위 one.

Two refinements are deliberate simplifications and are marked. **The two years do not
align**: the policy year runs from the 계약해당일 [S1 제5조제2항] while the 본인부담상한제
runs 1 January to 31 December [R10], and this model does not attempt to reconcile the
clocks. And **a proportional truncation of an expectation is not the same thing as
truncating each realisation** — `E[min(X, S)] ≠ min(E[X], S)` — so `τ` understates the
truncation's bite for exactly the reason a limit applied to a mean understates a limit's.
Where it is switched off entirely (`nhi_covered = 0`) that is not a simplification but the
product: a life outside the scheme is not refunded by it, so `oop_ceiling()` returns
infinity.

**Step 2 — the co-payment and the deductible, per event, never on a mean.**

*Inpatient*, both sides, is a flat percentage:

    paid_ge_in(y) = n_adm(y)·μ_ge_in·f_ge(y)·τ(y)·(1 − r_ge)  +  top_up(y)
    top_up(y)     = max( 0, n_adm(y)·μ_ge_in·f_ge(y)·τ(y)·r_ge − 2,000,000 )
    paid_np_in(y) = n_adm(y)·[ μ_np_in·f_np(y)·(1 − r_np)
                               + Σ_j π_j · min( 0.50·X_j·f_np(y), 100,000·D(y) ) ]

The 상급병실료 term is the one place a length of stay enters this model, and it enters
because the ₩100,000 cap is applied to the **daily average** — total non-covered room charge
divided by total days — and not night by night [S1 특별약관 제3조]. **A single expensive
night inside a long stay is therefore smoothed against the stay length rather than capped**,
a materially more generous treatment than a nightly cap.

*Outpatient*, both sides, is a kinked function of cost and the expectation must be taken
over the distribution:

    e(S, φ, r, f) = Σ_j π_j · min( max( 0, X_j·f − max(φ, r·X_j·f) ), Lv )

    paid_ge_out(y) = n_ge(y) · [ κ·e(ge_out, 10,000, r_ge, f_ge(y)·τ(y))
                                 + (1−κ)·e(ge_out, 20,000, r_ge, f_ge(y)·τ(y)) ]
    paid_np_out(y) = min(n_np(y), 100) · e(np_out, 30,000, r_np, f_np(y))
                     + carve(y)

with `κ = clinic_share()`. **The shape matters more than the formula.** The deductible is a
flat floor that becomes a percentage: at the 급여 clinic tier ₩10,000 until the covered cost
reaches ₩50,000 and 20% above it; at the hospital tier ₩20,000 until ₩100,000; on the 비급여
side a flat ₩30,000 until ₩100,000 and 30% above it. So a ₩10,000 clinic visit pays nothing,
a ₩50,000 visit pays ₩40,000, and above the crossing point the payment is a straight
percentage of cost until the ₩200,000 per-visit cap binds — at a covered cost of ₩250,000 on
the 급여 side, **the same crossing point at both provider tiers**. 4세대 merged 외래 and
처방조제 into one visit with one deductible where 3세대 carried a separate ₩8,000 처방조제
deductible on top [S1] [S5], which is why a 3세대 frequency basis cannot be carried across
without adjustment; the visit counts here are counts of **merged** visits **[std]**.

**Step 3 — the ₩2,000,000 annual inpatient co-payment cap, on the retention that survives
step 1.** Written into `paid_ge_in` above as `top_up(y)`. It applies to **inpatient
treatment only**; there is no annual cap on the outpatient deductible. Both this and the
본인부담상한제 reduce the insured's retention on heavy 급여 use, which is precisely why the
order is fixed: **the ceiling first as an exclusion from covered loss, the ₩2,000,000 cap
second on what remains.** Applying them in the other order, or in parallel, double-counts
the relief.

**Step 4 — the 3대비급여 sub-limits, which displace the main limit for their three
classes.** Per act there is no visit cap, only the ₩30,000 floor:

    p(S, f) = Σ_j π_j · max( 0, X_j·f − max(30,000, r_np·X_j·f) )

    a_ph_eff(y) = min(a_ph(y), 50) capped at 10, plus 0.60 × the excess over 10
    a_in_eff(y) = min(a_in(y), 50) × (1 − 0.25)
    carve(y)    = min(a_in(y), 50) × 0.25 × p(inject, f_np(y))

    claims_physio(y) = min( a_ph_eff(y)·p(physio, f_np(y)), 3,500,000 )
    claims_inject(y) = min( a_in_eff(y)·p(inject, f_np(y)), 2,500,000 )
    claims_mri(y)    = min( a_mr(y)·p(mri, f_np(y)),        3,000,000 )

Four contractual facts are in those five lines. The physical-therapy trio — 도수치료,
체외충격파치료, 증식치료 — **share one 50-act counter** and one money limit, so they are one
frequency here [S1 특별약관 제3조(3) <표1>]. Cover beyond the first ten acts is conditional
on a documented clinical re-assessment at each ten-act boundary, on a named test set —
관절가동(ROM), 통증평가척도, 자세평가 및 근력검사(MMT), 초음파 검사 — with the insurer
bearing the whole cost of the assessment [S1] [R2]; a projection can only represent that as a
continuation probability, and 0.60 is **[std]**. The injection carve-out moves the
항암제·항생제·희귀의약품 share **out** of the ₩2,500,000 sub-limit and **into** the main
₩50,000,000 비급여 limit [S1 특별약관 제3조(3)제2항], so the acts are removed from
`a_in_eff` and their payment added to `paid_np_out` — **counted once, in exactly one
place**. And MRI has a money limit and **no** act counter at all, the only one of the three
without one.

**Step 5 — the annual aggregates, per 보장종목 and per policy year.** 상해 and 질병 carry
**separate** ₩50,000,000 limits on each of the two parts [S1 제5조]:

    raw    = paid_in + paid_out                    (each side separately)
    capped = min(σ·raw, Λ) + min((1−σ)·raw, Λ)
    g(y)   = capped / raw

and `g_ge(y)`, `g_np(y)` are applied back to the printed limbs so that the five
`result_cf()` columns still sum to the limited total. The 3대비급여 limbs never pass through
`g_np` — they are already at their own sub-limits, which replace the aggregate rather than
sitting inside it. Where 3대비급여형 is not held those treatments are **not covered at all**
rather than falling back into the main limit.

**A necessary honesty about every limit in step 5, and about the counters in step 4.** On a
deterministic expected-value grid `E[min(X, Λ)] ≠ min(E[X], Λ)`, so a projection that
applies a limit to an expectation **understates** the limit's bite by ignoring dispersion.
On every shipped model point the ₩2,000,000 inpatient cap, the three 3대비급여 money limits,
the two 50-act counters, the 100-visit cap and the four ₩50,000,000 aggregates **do not
bind**, because the expected annual claim of a single cell is two orders of magnitude below
them — the supervisor's own tail figure is that **0.005% of insureds took more than
₩50,000,000 in 2019** [R1]. The machinery is implemented anyway, because it binds under any
seriatim or stochastic run and because `check_annual_limits()` is what proves it is wired
correctly. `check_annual_limits()` returning `True` says the limits are **wired**, not that
they are **exercised**. **Do not delete a limit because it reads slack.** The one limit that
does bind on a shipped model point is the 본인부담상한제 truncation, on model point 8.

**The indemnity ceiling, which is this product's defining constraint and no other's.**

    loss_incurred(y) = C_ge(y)·τ(y)
                     + n_adm(y)·(μ_np_in + μ_np_room)·f_np(y)
                     + n_np(y)·μ_np_out·f_np(y)
                     + ( a_ph(y)·μ_physio + a_in(y)·μ_inject + a_mr(y)·μ_mri )·f_np(y)

    claims_ann(y) ≤ loss_incurred(y)                              [check_indemnity]

「동일한 위험을 보장하는 2개 이상의 계약에 중복 가입 하더라도 실제 발생한 손해(비용)를
초과하여 보험금을 지급하지 않습니다」 [S1 제37조·제38조] [S3]. A co-payment applied as a
multiplier instead of a retention, a deductible subtracted twice, or a per-visit cap applied
to the wrong side of the deduction would all show up here, and nowhere else. `Cancer_KR_S`
and `LTC_KR_S` have no analogue of this check because they have no incurred loss to bound
against — it is the 정액 / 실손해 fork of 감독규정 제7-63조제1항제2호 in one identity
[REG-R17].

### The premium recursion and its corridor

    G_ge(y) = G_ge(y−1) · (1 + a) · (1 + b_ge(y)),     G_ge(1) = (1 − s)·P₀
    G_np(y) = G_np(y−1) · (1 + a) · (1 + b_np(y)),     G_np(1) = s·P₀
    G(y)    = [ G_ge(y) + G_np(y)·R(y) ] · ( 1 − 0.10·nc(y) )

**The order of operations is the thing a careless reading gets wrong**, and the 표준약관's
own illustration settles it. Its column label reads 「기초율 증가분 = 전년도 기준보험료 ×
25%」, but 3,640 is 25% of **14,560 = 14,000 × 1.04**, not of 14,000 [S1 제30조]. So the
corridor applies to the **age-adjusted** prior premium, and only the recursion above
reproduces the illustration's printed row 14,000 → 18,200 → 23,660 → 30,758 → 39,985 →
51,980. Getting it wrong costs 4% of the corridor every year and compounds: on this model's
비급여 unit the correct annual factor is 1.04 × 1.081 = 1.12424 and the additive misreading
gives 1.121, which puts the year-10 rider base premium **2.564% low** — ₩20,096.9929
against ₩20,625.8505.

Three further points, each sourced. The corridor binds **per 위험구분단위**, not on the
portfolio average [S1 제30조제2항] [REG-R17 제7-63조제2항제3호](#krlib-reg-r17), which is why the two units
are clipped separately and `check_renewal_corridor()` tests each. It applies to the
**pre-relativity** premium — 「요율 상대도 적용 전 보험료」 [S1 특별약관 제6조제2항]
[REG-R17 제7-63조제2항제3의2호](#krlib-reg-r17) — so a band-5 policyholder can face
**1.25 × 4.00 = 5.00×** the previous year's base rider rate in a single step, which is the
sharpest number in the product. And the relativity applies to the **순보험료**
(「특별약관의 순보험료 총액을 대상으로 합니다」 [S1]); this model applies it to the rider's
office premium and re-grosses at the same expense ratio, which is arithmetically identical
**[std]** and would fail only if the rider's expense loading contained a fixed per-policy
amount, which no retrieved document states either way.

**The composition reproduces the wording's own five-band table.** At `s = 0.4875` — the
share implied by solving the illustration's own band-2 and band-5 rows — the formula gives
`18,200 × (0.5125 + 0.4875 × 2) = 27,073` at renewal +1 and
`23,660 × (0.5125 + 0.4875 × 4) = 58,263` at +2, reproducing [S1]'s printed 27,073 and
58,263 to the won — the raw products are 27,072.5 and 58,262.75, and the wording's table is
printed rounded. That reproduction is
the check that the composition is the right one. The model itself runs at `s = 0.60`, from
[R2].

### 비급여 할인·할증 — the loop, written out

**This is the mechanism that makes the contract unlike anything else in this repository: the
renewal premium of the 비급여 rider is a function of the individual policyholder's own
prior-year non-covered claim amount.** It is a feedback loop from claims to premium, inside
a single policy, on an annual clock.

    C(y)        = (1 − 0.15) · claims_np(y)                       [exemptions removed]
    band(A)     = 1 if A ≤ 0; 2 if A < 1,000,000; 3 if A < 1,500,000;
                  4 if A < 3,000,000; 5 otherwise
    w_b(y)      = Σ_k π_k · 1{ band( ρ_k · C(y−1) ) = b },        w_b(1) = 1{b = 2}
    Σ(y)        = Σ_{b≥2} w_b(y) · r_b                            r = (1, 2, 3, 4)
    r₁*(y)      = ( 1 − Σ(y) ) / w₁(y)                            [revenue neutrality]
    r₁(y)       = max( r₁*(y), 0.95 )                             [the [std] 5% cap]
    R(y)        = w₁(y)·r₁(y) + Σ(y)      if the relativity is live, else 1
    nc(y)       = w₁(y−1) · w₁(y)         for y ≥ 3, else 0

Six things in those seven lines are load-bearing and each is sourced or flagged.

1. **The discount is solved, not set.** 「매년 상대도 적용 전·후의 총 보험료 수준이
   일치하도록 3~5단계의 할증대상자의 할증재원을 1단계(할인) 대상자들에게 분배할 경우
   산출됨」 [S1]. The scheme is revenue-neutral **within the rider**: the surcharge funds
   the discount and the insurer collects the same rider net premium either way. On the
   commencement band distribution 72.9 / 25.3 / 0.8 / 0.7 / 0.3 [R12] that gives
   `Σ = 0.301988` and `r₁* = 0.698012 / 0.729012 = 0.9574767`, a **4.2523% discount** —
   the specification's 0.9575, produced as a *result* rather than typed in. The published
   values bracket it and one lies outside: 「5% 내외」 at launch [R1], −5% 잠정 at
   commencement [R3], a 95% relativity in the wording's own illustration [S1], and one
   carrier writing it as 「α%」 rather than a number [S3]. On the FSC's alternative
   commencement distribution 62.1 / 36.6 / 1.3 [R3] the same identity gives 0.9791, a
   discount of only **2.1%** — the sensitivity is material, which is why both distributions
   are recorded rather than averaged. Solving rather than hard-coding means a change in the
   band distribution propagates correctly instead of silently breaking neutrality, and
   `check_relativity_neutral()` is the identity that proves it.
2. **The 5% cap is [std] and it eventually binds.** `reld_disc_cap = 0.05` is a floor under
   the discount taken from the two published values [R1] [R3]. It does not bind at
   commencement, where the solved figure is 4.25%. It binds once the claim level has trended
   far enough that contracts migrate into the surcharge bands and the pool would fund more
   than 5% — at which point **the scheme stops being revenue-neutral and the average rider
   premium rises above the base**. That is the loop reaching the aggregate, and it is a
   feature of the design rather than of this implementation.
3. **The thresholds are fixed money amounts and the claim level trends**, so contracts
   migrate into the surcharge bands year after year with nothing in the model changing. That
   migration *is* the loop, and it is why the band mix must be recomputed every year rather
   than fixed at the commencement distribution.
4. **The lookback window.** 「보험료 갱신 전 12개월 이내 기간」 [S1 특별약관 제6조제3항],
   with an operational three-month offset because renewal notices go out about a month ahead
   — 「계약해당일이 속한 달의 3개월 전 말일부터 직전 1년간」 [R12] — which 5세대 writes
   into the standard text [S2]. On an annual grid the offset is invisible; on a model that
   tried to resolve it the point would be that a claims-to-renewal lag of zero **over-states
   the responsiveness of the loop**.
5. **The relativity was deferred three years.** The clause was in the wording from launch
   and its application commenced **2024-07-01** 「충분한 통계 확보 등을 위하여」 [R3] [R1],
   so a 4세대 policy written in 2021 had **three renewals at flat relativity** before the
   loop switched on. `reld_start_year = 4`. The same deferral is being repeated on 5세대,
   whose differential starts 2028-05-06 [S3].
6. **The 무사고 할인 runs alongside and is a different animal.** 「직전 2년간 비급여
   보험금(4대 중증질환 치료를 위한 보험금은 제외) 미수령시 차기 1년간 보험료(급여(주계약)
   + 비급여(특약))의 10%를 할인」 [R1]. It has a **two-year** lookback where the relativity
   has one; it applies to the **whole** office premium where the relativity touches only the
   rider; and it **stacks** with the band-1 discount. The launch release prints a three-year
   timeline in which years 1 and 2 give only the rider discount and year 3 adds the 10%
   [R1]. The model reproduces the **10% leg** of that timeline exactly — `nc(y)` is zero in
   years 1 and 2 and 0.5314584961 from year 3 — and deliberately not the other leg: the
   rider discount was deferred to 2024-07-01 [R3], so on the modelled generation years 1
   to 3 carry no relativity at all (`reld_start_year = 4`).

### Decrement recursion and processing order

For `t = 0, 1, …, proj_len() − 1`:

1. **Start of month.** `premiums(t) = G(y(t)) · l(t)`.
2. **Look up the annual basis.** `age(t)`, hence `util_band(y)` and every frequency; hence
   `f_ge(y)`, `f_np(y)`, `τ(y)` and the whole of the five-step machinery above, computed
   **once per policy year** and divided by twelve.
3. **End of month — claims and expenses.**

       claims(t, kind) = l(t) · claims_ann_pp(y(t), kind) / 12
       expenses(t)       = 0.07 · premiums(t)
       claim_expenses(t) = 0.03 · claims(t)
       commissions(t)    = 0.06 · premiums(t)

4. **End of month — decrements, in order.**

       l_1 = l(t) · (1 − q(t))                          mortality
       l_2 = l_1  · (1 − w(t))                          lapse
       l_3 = l_2  · (1 − u(t))                          개인실손 중지
       l(t+1) = l_3 · (1 − d_ren(t))                    renewal decline, year end only

   exposed as `pols_if_at(t, timing)` at `BEF_DECR` / `BEF_LAPSE` / `BEF_SUSPEND` /
   `BEF_RENEWAL` / `AFT_DECR`, with the five decrement counts `pols_death`, `pols_lapse`,
   `pols_suspend`, `pols_renewal_decline` and `pols_maturity` taken at the matching points.
   `d_ren(t)` is non-zero **only** where `(t + 1) mod 12 = 0`; `pols_maturity(t)` is non-zero
   **only** at `t = proj_len() − 1`, where it absorbs everyone left. Lapse and death both pay
   **nothing**.

**Five decrements, and the middle three are what make this roll-forward different from a
term assurance's.** 개인실손 중지 is a supervisory requirement rather than a product feature
[REG-R17 제7-63조제2항제7호](#krlib-reg-r17); the renewal decline is an option the policyholder holds and the
insurer does not; and the maturity count is the *stated horizon* rather than the end of
cover. Without all three the roll-forward would appear to lose lives with no cause, and
`check_pols_roll_fwd()` would fail.

### Net cash flow

    net_cf(t) = premiums(t) − claims(t) − expenses(t)
                             − claim_expenses(t) − commissions(t)

income-positive, with `claims(t)` the sum of the five limbs `GE_IN`, `GE_OUT`, `NP_IN`,
`NP_OUT`, `NP_THREE`. `result_cf()` publishes the five limbs as separate columns and
**deliberately no `claims` subtotal column**, so that the printed columns sum to `net_cf`
and a limb cannot be double-counted invisibly; the `claims(t, kind)` cells stays. `expenses`
is **maintenance only** and the claim-handling expense stands beside it in its own
`claim_expenses` column, which is what the two names mean library-wide and which keeps a
premium-driven cost and a claim-driven cost from moving together in one figure.

Because every rate in the ledger is proportional, the whole cash flow collapses to a
two-term identity that is worth writing down, since it governs everything the *Worked
example* shows:

    net_cf(t) = 0.87 · premiums(t) − 1.03 · claims(t)

so the sign of `net_cf` in any period is decided by a single number, the loss ratio, against

    LR* = 0.87 / 1.03 = 0.8446601942

**The model's own break-even loss ratio is 84.47%**, which sits just below the FSS's stated
break-even of 「약 85% 수준」 [R7]. The gap is the expense loading, not the basis the claim
handling is charged on: at that loss ratio the 3% of claims is 2.53% of premium, so the
model is carrying 6 + 7 + 2.53 = **15.53%** of premium against the 15% residual an 85%
break-even implies. Charging the claim handling on premium instead would take the model's
break-even **down** to 84.00%, not up — the claims basis narrows the gap rather than
causing it.

### Optional modules (all off, or neutral, in the base run)

| Module | Base-run setting | What switching it on does |
|---|---|---|
| **개인실손 중지** | `suspend_rate = 0` | A fourth decrement at `1 − (1 − r)^(1/12)` a month. Mandatory as a *facility* [REG-R17 제7-63조제2항제7호](#krlib-reg-r17) [R16] [S3]; carried as a decrement and **not** as a state, because the contract that resumes is a different projection. Model point 9 carries 3% a year. |
| **The 40% branch** | `nhi_covered = 1` | Raises `r_ge` and `r_np` to 0.60 and switches the 본인부담상한제 off. Model point 10. |
| **Cost-trend stress** | `trend_mult = 1.0` | Multiplies both `med_trend_*`. At 4.5 the 비급여 re-rate would be 36.45% and the corridor clips it to 25%; model point 10. |
| **Utilisation stress** | `util_mult = 1.0` | Multiplies every frequency. Model point 8 carries 10.0 — a cell inside the top claim decile — and is the only shipped point where the public truncation binds. |
| **요율 상대도 off** | `reld_on = 1` | With it off the contract is a plain attained-age renewable, which is what 1세대 through 3세대 were. Model points 5 and 9. |
| **무사고 할인 off** | `noclaim_on = 1` | Model points 5 and 9. |
| **비급여 특약 off** | `np_rider = 1` | Removes 60% of the premium, the 100-visit cap, the three sub-limits **and the whole loop**. Model point 5. |
| **3대비급여형 off** | `three_np = 1` | Those treatments become uncovered, not reassigned to the main limit. Model point 6. |
| **Lower 보험가입금액 rung** | `annual_limit = 50m`, `visit_cap = 200k` | Model point 7 at ₩10,000,000 / ₩100,000. |

Two things are **not modules and are not modelled at all**, and both are limitations rather
than omissions. **The 재가입 terms change**: the model assumes re-entry on unchanged terms at
`t = 60`, so nothing whatever happens in the cash flows at the first 보장내용 변경주기, and
that no-op is the assumption made visible. A 5세대 re-entry would change the partition, the
비중증 co-payment and the limits at once — see the delta table in `product-spec.md`. And
**the behavioural response to the experience rating**: the supervisor's own worked example
has a policyholder cutting his claims by 93% in response to a surcharge, from ₩10,000,000 to
₩700,000, saving ₩300,000 of premium and ₩2,700,000 out of pocket in one year [R2]. **The
contract is designed to change the insured's behaviour**, and this model projects the
premium's response to claims but not the claims' response to premium.

---

## Policyholder behavior modeling

- **Lapse is real, immediate and unbroken.** There is no surrender value, so there is no
  보험료 자동대출납입 to advance a missed premium and no 보험계약대출 to lend against —
  표준약관 제33조 excludes 「순수보장성보험 등」 from policy lending in terms [REG-R25]. A
  missed premium produces a 납입최고 of at least 14 days and the contract terminates the day
  after it ends [REG-R25 제26조](#krlib-reg-r25). So no lapse-suppression term belongs in the recursion, and
  `claims_lapse` is identically zero. This is the structural fork between the 실손 chassis
  and the [whole life savings chassis (종신보험)](../whole_life/technical-notes.md), whose
  자동대출납입 and 보험계약대출 machinery must **not** be imported here.
- **Declining the renewal is a different act from lapsing, and the contract says so.** The
  policyholder may decline the annual renewal; the insurer may not [S5] [S3]. `renewal_decline`
  is therefore a decrement of its own, non-zero only in the twelfth month of a policy year,
  and it is the decrement this product is genuinely exposed to: on a one-year contract that
  re-rates every year at the attained age, the renewal is where the policyholder actually
  makes a decision. Folding it into `lapse_rate` would make the annual boundary invisible.
- **The re-entry decision is not modelled as a decrement at all.** At the fifth 계약해당일 the
  policyholder may take whichever 실손 product the company is then selling, and 「회사는 이를
  거절할 수 없습니다」 [S1 제23조제2항] [R2]. Where the decision cannot be obtained the
  contract is **extended on the previous terms** [제5항], the policyholder may cancel that
  extension within 90 days with a full refund of premium paid after it [제6항], and the
  extension runs until intention is established — typically the date of the first claim
  [제7항], capped at one year from the end of the 보험기간 at one carrier [S3 제53조제7항].
  None of that is a cash flow this model can produce without a new-business funnel, so `t = 60`
  carries the ordinary 1% renewal decline and nothing more **[std]**. A re-entry into a
  materially different generation would plausibly carry a higher decline, and that is a named
  sensitivity rather than a modelled effect.
- **Suspension is not lapse either.** A policyholder covered by a 단체실손 may suspend the
  individual policy for the duration and resume it within one month of the group cover ending
  [R16] [S3], and the facility is mandatory [REG-R17 제7-63조제2항제7호](#krlib-reg-r17). The resumed contract
  must match on four attributes to count as the same — 보장종목, 보험가입금액, 자기부담금,
  최대 보장가능 보험나이 [S3] — which is precisely why resumption is **not** modelled: the
  contract that resumes is a different projection, entering the product in force at
  resumption. Suspension here ends the cash flows and nothing more.
- **Duplicate cover buys nothing, and that is a behavioural fact about the population rather
  than about the cell.** 「동일한 위험을 보장하는 2개 이상의 계약에 중복 가입 하더라도 실제
  발생한 손해(비용)를 초과하여 보험금을 지급하지 않습니다. (중복 가입 시 비례보상)」 [S3],
  under 표준약관 제37조·제38조. It is why 36.22 million policies can cover about 40 million
  insureds without either number being wrong [R7] [R4], and it is a thing a fixed-sum contract
  could not do. A single-policy projection is unaffected; a *portfolio* model that scaled
  claims by policy count rather than by insured count would double-count.
- **No dynamic lapse from a cash value or an interest rate.** There is no 해약환급금, no
  공시이율, no 예정이율 disclosure on a one-year contract and no MVA, so there is no economic
  surrender trigger to model. Neither the 무해지환급형 surrender-value cliff at 납입완료 nor
  the 유지보너스-date lapse spike that [whole life](../whole_life/technical-notes.md) wires
  to its persistency bonus has any analogue here.
- **Anti-selective lapse is not modelled, and the direction is the *reverse* of a term
  product's.** Healthy lives decline renewal first, so the persisting block is progressively
  impaired on the *morbidity* basis. The natural form,
  `freq_eff(y) = freq(y) × [1 + λ·max(0, cumulative exits − ref)]`, is not implemented and
  λ = 0 is the base run: no Korean 실손 selective-lapse evidence was retrieved. But the
  experience rating makes this product's version of the effect **much sharper than a term
  product's**, because the surcharge is itself a signal — a policyholder facing a 300%
  relativity is a policyholder the model has already identified as a heavy claimant, and
  whether he renews at all is exactly the question λ would answer.
- **The behavioural response to the surcharge is the elephant, and it is not modelled.** The
  FSC/FSS FAQ works the design's intended case in full: a 45-year-old male paying ₩5,000 급여
  plus ₩8,000 비급여 takes about 20 sessions of 도수치료 at ₩500,000 a session, claims
  ₩10,000,000 and receives ₩7,000,000; his rider premium quadruples to about ₩32,000 and his
  total to about ₩40,000; he then shops on the 심평원 price disclosure, cuts his claims to
  ₩700,000, and his rider premium resets to about ₩9,000 including the age increment — a
  saving of ₩300,000 in premium and ₩2,700,000 out of pocket in one year [R2]. **The contract
  is designed to change the insured's behaviour**, and `Medical_KR_S` models the premium's
  response to claims and not the claims' response to premium. Stated as a limitation, and it
  is the single largest one in this document.
- **Elections are not behaviour.** 보장종목, 보험가입금액 and the per-visit cap are chosen at
  issue and are model point attributes; nothing in the projection may vary them over `t`. The
  one thing that *can* change them is 재가입, and that is a scheduled terms change at a
  contractual date, not a policyholder decision the model is entitled to simulate.
- **청약철회 is out of scope.** 15 days from receipt of the 보험증권 or 30 days from
  application, whichever comes first, effective on despatch [REG-R51]; it is a pre-inception
  decrement and modelling it would need a new-business funnel this library does not have.

---

## Worked example

Everything in this section is **read off the shipped model**, not recomputed by hand. The
test module asserts it cell by cell at the precision displayed.

### The anchor cell

**`point_id = 1`** — 남자, **만나이 40** at issue, all five 보장종목 held
(상해급여형 and 질병급여형 in the 주계약; 상해비급여형, 질병비급여형 and 3대비급여형 in the
특약), 연간 보험가입금액 **₩50,000,000 per 보장종목**, 통원 1회당 **₩200,000**, 월납 office
premium **₩11,982** in the first policy year, split 급여 **₩4,792.80** / 비급여
**₩7,189.20** at `s = 0.60`. 본인부담상한제 decile **6** (ceiling ₩3,260,000 on the 2026
scale), 급여 통원 clinic-tier share **0.63**, inside 국민건강보험. Both the 요율 상대도 and
the 무사고 할인 are switched on; `trend_mult = util_mult = 1.0`; `suspend_rate = 0`.

`proj_len() = 120`, so `result_cf()` has **120 rows**, `t = 0 … 119` — **ten policy years,
two five-year 보장내용 변경주기**, ending in the twelfth month of policy year 10 at attained
만나이 49. `pols_if_init() = 1.0`.

**The ₩11,982 is not an assumption of this document; it is the published new-business anchor
for exactly this cell** — 40세 남자, 4세대, 10-carrier 손해보험 average, 2021-06 [R1] — and
age 40 male is the 기준연령 요건 of 감독규정 제1-2조제2호 [REG-R9].

### Every assumption value the anchor cell uses

**Frequencies** — `utilisation_table.csv`, per policy per year, all **[std]**. The anchor
reads `(M, 40)` in policy years 1–5 and `(M, 45)` in years 6–10.

| Band | `adm_rate` | `los_days` | `visit_rate_ge` | `visit_rate_np` | `act_rate_physio` | `act_rate_inject` | `act_rate_mri` |
|---|---|---|---|---|---|---|---|
| **M, 40** | **0.014140** | **7.500000** | **1.885433** | **0.236694** | **0.092047** | **0.078898** | **0.015780** |
| **M, 45** | **0.017674** | **8.250000** | **2.224811** | **0.279298** | **0.112298** | **0.096255** | **0.020198** |
| ratio | 1.2499293 | 1.100000 | 1.1800000 | 1.1799961 | 1.2200072 | 1.2199929 | 1.2799747 |

**Severities** — `severity_table.csv`, all **[std]**, with the expected payment per event at
trend 1.0, which is what policy year 1 uses. The right-hand column is where the *shape*
earns its place: it is not any simple function of the mean.

| Stream | (cost, probability) points | mean `μ_S` | expected payment per event, year 1 |
|---|---|---|---|
| `ge_in` | (250,000, .40) (700,000, .32) (1,800,000, .20) (5,000,000, .07) (15,000,000, .01) | 1,184,000 | **947,200** = 0.80 × mean (flat percentage) |
| `ge_out` | (8,000, .30) (18,000, .30) (40,000, .25) (90,000, .12) (250,000, .03) | 36,100 | clinic tier **24,540**; hospital tier **19,400**; blend at κ = 0.63 → **22,638.20** |
| `np_in` | (400,000, .40) (1,200,000, .33) (3,000,000, .20) (8,000,000, .07) | 1,716,000 | **1,201,200** = 0.70 × mean |
| `np_room` | (0, .55) (300,000, .30) (1,200,000, .15) | 270,000 | **135,000** at `D = 7.5` (daily-average cap ₩750,000 a stay) |
| `np_out` | (45,000, .35) (90,000, .30) (180,000, .22) (400,000, .10) (900,000, .03) | 149,350 | **76,970** |
| `physio` | (80,000, .35) (120,000, .35) (180,000, .22) (400,000, .08) | 141,600 | **97,020** per act |
| `inject` | (60,000, .40) (120,000, .30) (250,000, .20) (700,000, .10) | 180,000 | **121,200** per act |
| `mri` | (450,000, .45) (700,000, .35) (1,100,000, .20) | 667,500 | **467,250** per act |

**Claim shape** — `claim_shape_table.csv`, `shape_mean() = 53,530.7923920000`. The last two
columns are the rescaling in action: the amounts are read as multiples of the table's own
mean and rescaled to the year's rated claim.

| bucket | `claim_amount` | `share` | `shape_rel` | amount at `C(1)` | band at the year-2 renewal |
|---|---|---|---|---|---|
| 0 | 0 | 0.729012 | 0.0000000000 | 0.00 | **1단계** |
| 1 | 2,184 | 0.011039 | 0.0407989477 | 2,184.03 | 2단계 |
| 2 | 6,551 | 0.017901 | 0.1223781623 | 6,551.09 | 2단계 |
| 3 | 15,285 | 0.048628 | 0.2855365915 | 15,285.21 | 2단계 |
| 4 | 32,753 | 0.052805 | 0.6118534499 | 32,753.44 | 2단계 |
| 5 | 65,506 | 0.056385 | 1.2237068998 | 65,506.88 | 2단계 |
| 6 | 152,847 | 0.066230 | 2.8553098725 | 152,849.05 | 2단계 |
| 7 | 1,200,000 | 0.008000 | 22.4170042396 | 1,200,016.10 | **3단계** (→ 4단계 from `y = 5`) |
| 8 | 2,000,000 | 0.007000 | 37.3616737326 | 2,000,026.83 | **4단계** (→ 5단계 from `y = 7`) |
| 9 | 4,500,000 | 0.003000 | 84.0637658985 | 4,500,060.37 | **5단계** |

**Decrements.** `mort_table.csv` [std] Makeham, male: q(40) = **0.00132019**,
q(41) = 0.00136205, q(44) = 0.00152503, q(45) = **0.00159477**, q(49) = **0.00198242**;
`mort_rate_mth(0) = 1 − (1 − 0.00132019)^(1/12) = 0.0001100825`. `lapse_table.csv` [std]:
0.100 in policy year 1 falling to 0.020 by year 10, so
`lapse_rate_mth(0) = 1 − (1 − 0.10)^(1/12) = 0.0087416110` and
`lapse_rate_mth(12) = 1 − (1 − 0.06)^(1/12) = 0.0051430128`.
`renewal_decline_rate = 0.01`, acting at `t = 11, 23, …, 119`. `suspend_rate = 0`.

**본인부담상한액.** `oop_ceiling_table.csv`, 2026 scale [R10]: 900,000 / 1,120,000 /
1,120,000 / 1,730,000 / 1,730,000 / **3,260,000** / 3,260,000 / 4,460,000 / 5,360,000 /
8,430,000 for deciles 1–10. The anchor is decile 6, ceiling **₩3,260,000**, against an
incurred 급여 본인부담금 of **₩84,805.8913** in policy year 1 — headroom of a factor of
**38.4** — so **`oop_trunc(y) = 1.0 throughout on this cell**. The truncation binds on model
point 8 and nowhere else.

**Scalar References, in full.** `reentry_period` 5, `reentry_cycles` 2, `max_cover_age` 100,
`renewal_decline_rate` 0.01, `retain_rate_ge_base` 0.20, `retain_rate_np_base` 0.30,
`retain_rate_nonhi` 0.60, `ded_clinic` 10,000, `ded_hospital` 20,000, `ded_np_out` 30,000,
`cap_inpatient_retain` 2,000,000, `room_rate` 0.50, `room_cap_day` 100,000,
`visit_limit_np` 100, `act_limit_three` 50, `physio_gate_acts` 10, `physio_cont_prob` 0.60,
`limit_physio` 3,500,000, `limit_inject` 2,500,000, `limit_mri` 3,000,000,
`inject_carve_share` 0.25, `share_injury` 0.15, `med_trend_ge` 0.010, `med_trend_np` 0.081,
`age_load` 0.04, `renewal_corridor` 0.25, `band_thr_3/4/5` 1,000,000 / 1,500,000 /
3,000,000, `reld_r2..r5` 1 / 2 / 3 / 4, `reld_disc_cap` 0.05, `reld_start_year` 4,
`reld_exempt_share` 0.15, `noclaim_disc` 0.10, `comm_rate` 0.06, `expense_maint_rate` 0.07,
`expense_claim_rate` 0.03, `expense_total_rate` 0.16, `roll_fwd_tol` 1e-10, `cash_tol`
1e-06, `shape_tol` 1e-09.

**The calibration closing.** Policy year 1 gives a 급여 loss ratio of **0.9750080** and a
비급여 loss ratio of **0.7300099** against published 4세대 2022 상반기 figures of 97.5% and
73.0%, and a combined **0.8280091** against the published **82.8%** [R12]. That is the
solve, and it is the reason the frequency level is what it is.

### The cash flow statement, policy year 1

Per policy issued, income-positive, `pols_if` to ten decimals and cash to ₩0.0001 — the
precision the tests assert. Within a policy year every per-policy quantity is constant, so
**every row below is row `t = 0` scaled by `pols_if(t)`**; the whole of policy year 1 is one
set of rates.

| `t` | `pols_if` | `premiums` | `claims_ge_in` | `claims_ge_out` | `claims_np_in` | `claims_np_out` | `claims_np_three` | `expenses` | `claim_expenses` | `commissions` | `net_cf` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1.0000000000 | 11,982.0000 | 1,116.1173 | 3,556.9008 | 1,574.4890 | 1,717.4122 | 1,956.2861 | 838.7400 | 297.6362 | 718.9200 | 205.4984 |
| 1 | 0.9911492689 | 11,875.9505 | 1,106.2389 | 3,525.4196 | 1,560.5536 | 1,702.2119 | 1,938.9715 | 831.3165 | 295.0019 | 712.5570 | 203.6796 |
| 2 | 0.9823768732 | 11,770.8397 | 1,096.4479 | 3,494.2171 | 1,546.7416 | 1,687.1460 | 1,921.8102 | 823.9588 | 292.3909 | 706.2504 | 201.8769 |
| 3 | 0.9736821197 | 11,666.6592 | 1,086.7435 | 3,463.2907 | 1,533.0518 | 1,672.2136 | 1,904.8008 | 816.6661 | 289.8030 | 699.9995 | 200.0901 |
| 4 | 0.9650643210 | 11,563.4007 | 1,077.1250 | 3,432.6380 | 1,519.4832 | 1,657.4133 | 1,887.9419 | 809.4380 | 287.2380 | 693.8040 | 198.3192 |
| 5 | 0.9565227962 | 11,461.0561 | 1,067.5917 | 3,402.2567 | 1,506.0346 | 1,642.7439 | 1,871.2322 | 802.2739 | 284.6958 | 687.6634 | 196.5639 |
| 6 | 0.9480568701 | 11,359.6174 | 1,058.1427 | 3,372.1442 | 1,492.7051 | 1,628.2044 | 1,854.6705 | 795.1732 | 282.1760 | 681.5770 | 194.8242 |
| 7 | 0.9396658737 | 11,259.0765 | 1,048.7774 | 3,342.2983 | 1,479.4936 | 1,613.7936 | 1,838.2553 | 788.1354 | 279.6785 | 675.5446 | 193.0998 |
| 8 | 0.9313491437 | 11,159.4254 | 1,039.4949 | 3,312.7165 | 1,466.3990 | 1,599.5104 | 1,821.9854 | 781.1598 | 277.2032 | 669.5655 | 191.3908 |
| 9 | 0.9231060229 | 11,060.6564 | 1,030.2946 | 3,283.3965 | 1,453.4203 | 1,585.3536 | 1,805.8595 | 774.2459 | 274.7497 | 663.6394 | 189.6968 |
| 10 | 0.9149358597 | 10,962.7615 | 1,021.1758 | 3,254.3361 | 1,440.5564 | 1,571.3220 | 1,789.8763 | 767.3933 | 272.3180 | 657.7657 | 188.0179 |
| 11 | 0.9068380084 | 10,865.7330 | 1,012.1376 | 3,225.5328 | 1,427.8065 | 1,557.4147 | 1,774.0346 | 760.6013 | 269.9078 | 651.9440 | 186.3538 |

**There is no month-0 strain**, and its absence is the product. `t = 0` is positive at
**₩205.4984** and every row of policy year 1 is positive. A one-year renewable contract with
no reserve accumulation and a level expense rate has no acquisition/renewal distinction to
create one.

### The rows where the product does something

| `t` | `pols_if` | `premiums` | `claims_ge_in` | `claims_ge_out` | `claims_np_in` | `claims_np_out` | `claims_np_three` | `expenses` | `claim_expenses` | `commissions` | `net_cf` |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 11 | 0.9068380084 | 10,865.7330 | 1,012.1376 | 3,225.5328 | 1,427.8065 | 1,557.4147 | 1,774.0346 | 760.6013 | 269.9078 | 651.9440 | 186.3538 |
| 12 | 0.8898237107 | 11,671.5892 | 1,003.0791 | 3,196.9486 | 1,514.5001 | 1,644.1587 | 1,891.8205 | 817.0112 | 277.5152 | 700.2954 | 626.2604 |
| 24 | 0.8269420725 | 11,255.2428 | 941.5160 | 3,001.0022 | 1,521.4795 | 1,636.8789 | 1,909.8972 | 787.8670 | 270.3232 | 675.3146 | 510.9643 |
| 36 | 0.7807303037 | 11,657.8250 | 897.7905 | 2,861.8800 | 1,551.7139 | 1,652.4968 | 1,957.3942 | 816.0477 | 267.6383 | 699.4695 | 953.3941 |
| 47 | 0.7546309860 | 11,268.1113 | 867.7779 | 2,766.2092 | 1,499.8410 | 1,597.2548 | 1,891.9597 | 788.7678 | 258.6913 | 676.0867 | 921.5228 |
| 48 | 0.7447790095 | 12,234.0846 | 865.0133 | 2,757.6339 | 1,592.1640 | 1,686.8368 | 2,022.0773 | 856.3859 | 267.7118 | 734.0451 | 1,452.2165 |
| 59 | 0.7232591474 | 11,880.5894 | 840.0193 | 2,677.9540 | 1,546.1596 | 1,638.0969 | 1,963.6508 | 831.6413 | 259.9764 | 712.8354 | 1,410.2557 |
| 60 | 0.7141205641 | 12,896.5596 | 1,047.0651 | 3,151.5278 | 2,064.9814 | 2,052.2614 | 2,600.0030 | 902.7592 | 327.4752 | 773.7936 | **-23.3071** |
| 72 | 0.6874997399 | 13,729.9031 | 1,018.1132 | 3,064.6451 | 2,138.8820 | 2,113.3143 | 2,709.8504 | 961.0932 | 331.3441 | 823.7942 | 568.8666 |
| 118 | 0.6087150719 | 16,301.6322 | 928.7562 | 2,796.3637 | 2,363.0410 | 2,142.5505 | 3,033.2096 | 1,141.1143 | 337.9176 | 978.0979 | 2,580.5814 |
| 119 | 0.6075906434 | 16,271.5195 | 927.0406 | 2,791.1982 | 2,358.6760 | 2,138.5928 | 3,027.6066 | 1,139.0064 | 337.2934 | 976.2912 | 2,575.8145 |

**What each of those rows is.**

- **`t = 11`** — the last month of policy year 1, and the only month of that year in which
  the **renewal decline** acts: `pols_renewal_decline(11) = 0.0089881183` against
  `pols_lapse(11) = 0.0079263524`. The decline is the **larger** of the two exits at every
  annual boundary, and by policy year 2 it is nearly twice the lapse.
- **`t = 12`** — the **first renewal**. `net_cf` more than **triples**, from ₩186.35 to
  ₩626.26, and the reason is worth stating precisely: the 비급여 base premium rises 12.424%
  while the claim it funds rises only with the 8.1% 비급여 cost trend, and the 급여 base
  rises 5.04% against a 1.0% claim trend. **The premium re-rate outruns the claim trend by
  construction, because the 4% age loading has no counterpart in a utilisation table that
  moves in five-year steps.**
- **`t = 24`** — the first month of policy year 3, and the first month the **무사고 할인**
  applies: `noclaim_share(3) = 0.729012² = 0.5314584961`, so 5.3146% comes off the whole
  office premium. `premiums(24)` is therefore **₩11,255.2428** against the **₩11,886.9868**
  it would have been without the discount, and the year-3 gross premium of ₩13,610.6786 is
  **below** the un-discounted ₩14,374.6306 — the discount gives back more than half of the
  year's 9.590% re-rate, which becomes +3.766% once it is applied. The two-year lookback is
  what the launch release's three-year timeline requires [R1], and the model reproduces
  **that** leg of it: the discount first appears in year 3. It does **not** reproduce the
  release's other leg — R1 shows years 1 and 2 giving the rider discount, and here they give
  nothing, because the 요율 상대도 was deferred to 2024-07-01 [R3] and
  `reld_start_year = 4`.
- **`t = 36`** — policy year 4, where the **요율 상대도 switches on** (`reld_start_year = 4`,
  the three-year deferral to 2024-07-01 [R3]). Nothing at all happens in the cash flows:
  `reld_avg(4) = 1.0000000000` exactly, because the discount cap is slack and the scheme is
  revenue-neutral. **The loop's first live year is the year in which it moves no money**,
  and on a single average cell that is exactly what revenue neutrality means — individual
  policies are re-rated apart, and the average is not.
- **`t = 48`** — policy year 5, where the **discount cap first binds**. `reld_avg` steps to
  **1.0025494000** and the rider premium rises above its base for the first time.
- **`t = 59` → `t = 60`** — the **first 재가입** and the **utilisation band step** at the
  same anniversary. The 재가입 is a **no-op** in this model, by assumption; the band step is
  not. `net_cf` falls from **+₩1,410.2557** to **−₩23.3071**.
- **`t = 72`** — policy year 7, where the year-6 claim has trended enough to push bucket 8
  across ₩3,000,000 into 5단계; `reld_avg` steps again to **1.0095494000**.
- **`t = 119`** — the horizon. `pols_renewal_decline(119) = 0.0060646829` and
  `pols_maturity(119) = 0.6004036091` together absorb the whole remaining in-force, and
  `pols_if(120) = 0`. The maturity count pays **nothing**: there is no 만기보험금 on a
  순수보장성 contract, and what ends here is the *stated horizon*, not the cover.

### The renewal and experience-rating ledger

`result_prem()`, one row per policy year — the frame the product's story is actually in.

| `y` | `claims_np_rated_pp` | `band_1` | `band_2` | `band_3` | `band_4` | `band_5` | `reld_surcharge` | `reld_solved` | `reld_one` | `reld_avg` | `noclaim_share` | `prem_ge_base` | `prem_np_base` | `prem_gross_mth` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 53,531.5106 | 0.000000 | 1.000000 | 0.000000 | 0.000000 | 0.000000 | 1.000000 | 1.0000000000 | 1.0000000000 | 1.0000000000 | 0.0000000000 | 4,792.8000 | 7,189.2000 | 11,982.0000 |
| 2 | 57,893.3650 | 0.729012 | 0.252988 | 0.008000 | 0.007000 | 0.003000 | 0.301988 | 0.9574766945 | 0.9574766945 | 1.0000000000 | 0.0000000000 | 5,034.3571 | 8,082.3862 | 13,116.7433 |
| 3 | 62,514.9072 | 0.729012 | 0.252988 | 0.008000 | 0.007000 | 0.003000 | 0.301988 | 0.9574766945 | 0.9574766945 | 1.0000000000 | 0.5314584961 | 5,288.0887 | 9,086.5419 | 13,610.6786 |
| 4 | 67,434.7704 | 0.729012 | 0.252988 | 0.008000 | 0.007000 | 0.003000 | 0.301988 | 0.9574766945 | 0.9574766945 | 1.0000000000 | 0.5314584961 | 5,554.6084 | 10,215.4538 | 14,931.9489 |
| 5 | 72,600.0553 | 0.729012 | 0.252988 | 0.000000 | 0.015000 | 0.003000 | 0.309988 | 0.9465029382 | 0.9500000000 | 1.0025494000 | 0.5314584961 | 5,834.5607 | 11,484.6218 | 16,426.4626 |
| 6 | 95,944.4532 | 0.729012 | 0.252988 | 0.000000 | 0.015000 | 0.003000 | 0.309988 | 0.9465029382 | 0.9500000000 | 1.0025494000 | 0.5314584961 | 6,128.6225 | 12,911.4712 | 18,059.3589 |
| 7 | 103,291.4952 | 0.729012 | 0.252988 | 0.000000 | 0.008000 | 0.010000 | 0.316988 | 0.9369009015 | 0.9500000000 | 1.0095494000 | 0.5314584961 | 6,437.5051 | 14,515.5924 | 19,970.7757 |
| 8 | 110,408.5397 | 0.729012 | 0.252988 | 0.000000 | 0.008000 | 0.010000 | 0.316988 | 0.9369009015 | 0.9500000000 | 1.0095494000 | 0.5314584961 | 6,761.9553 | 16,319.0096 | 22,001.8621 |
| 9 | 118,056.8805 | 0.729012 | 0.252988 | 0.000000 | 0.008000 | 0.010000 | 0.316988 | 0.9369009015 | 0.9500000000 | 1.0095494000 | 0.5314584961 | 7,102.7579 | 18,346.4834 | 24,262.6066 |
| 10 | 126,324.7368 | 0.729012 | 0.252988 | 0.000000 | 0.008000 | 0.010000 | 0.316988 | 0.9369009015 | 0.9500000000 | 1.0095494000 | 0.5314584961 | 7,460.7369 | 20,625.8505 | 26,780.3985 |

**Five things to read off it.**

1. **The band mix at `y = 2` is exactly the published commencement distribution** —
   72.9 / 25.3 / 0.8 / 0.7 / 0.3 [R12] — because the shape table is calibrated at the
   anchor's year-1 rated claim: `C(1) = 53,531.5106` against a tabulated
   `shape_mean() = 53,530.7924`. The surcharge pool is **0.301988** and the solved band-1
   relativity is **0.9574766945**, a **4.2523%** discount. **That is the specification's
   0.9575 arriving as a result rather than as an input**, and it is the single best evidence
   that the neutrality identity is implemented rather than asserted.
2. **`y = 1` has no prior year, so every contract sits at 2단계** and the printed
   `reld_solved` of 1.0 is the guard value, not a solve. The relativity is not applied in
   year 1 in any case.
3. **The relativity is not applied until `y = 4`,** and when it is applied it moves nothing:
   `reld_avg` is 1.0 exactly at `y = 4`. Revenue neutrality on a single average cell means
   the loop is invisible in the aggregate until the cap binds.
4. **The cap binds from `y = 5`.** The claim level has trended far enough that bucket 7
   (tabulated 1,200,000) crosses ₩1,500,000 and moves from 3단계 to 4단계, so
   `reld_surcharge` rises from 0.301988 to 0.309988 and the solved discount would be
   **5.35%**; the [std] 5% cap holds `reld_one` at 0.95 and `reld_avg` rises to
   **1.0025494**. From `y = 7` bucket 8 crosses ₩3,000,000 into 5단계, the pool reaches
   0.316988, and `reld_avg` reaches **1.0095494**. **The scheme stops being revenue-neutral
   at the moment the discount is capped**, and after that the loop is a net addition to
   premium.
5. **`noclaim_share` is 0.5314584961 = 0.729012² from `y = 3`**, two independent claim-free
   years, giving a **5.3146%** discount on the *whole* office premium.

### Hand traces

Four periods, written out term by term, so that a reader with a calculator can reproduce a
row and watch the processing order do its work. All arithmetic is on the values printed
above.

**Trace, `t = 0` — the annual claim built from nothing, then divided by twelve.**

    Step 0: the year's basis.  y = 1, age = 40, band = 40, f_ge = f_np = 1.0
    Step 1: the public ceiling.
      C_ge(1)  = ( 0.014140 x 1,184,000 + 1.885433 x 36,100 ) x 1.0
               = ( 16,741.7600 + 68,064.1313 )                  =    84,805.8913
      tau(1)   = min( 1, 3,260,000 / 84,805.8913 )              =     1.0000000000
    Step 2 and 3: co-payment, deductible, and the inpatient cap.
      geubyeo inpatient
        cost     = 0.014140 x 1,184,000 x 1.0 x 1.0             =    16,741.7600
        retained = 0.20 x 16,741.7600 = 3,348.3520 < 2,000,000  -> top_up = 0
        paid     = 0.80 x 16,741.7600                           =    13,393.4080
      geubyeo outpatient, per visit, over the distribution
        clinic tier, floor 10,000:
          8,000  -> ded max(10,000, 1,600)  = 10,000 -> pay      0.00 x 0.30
          18,000 -> ded max(10,000, 3,600)  = 10,000 -> pay  8,000.00 x 0.30
          40,000 -> ded max(10,000, 8,000)  = 10,000 -> pay 30,000.00 x 0.25
          90,000 -> ded max(10,000, 18,000) = 18,000 -> pay 72,000.00 x 0.12
          250,000-> ded max(10,000, 50,000) = 50,000 -> pay min(200,000, 200,000) x 0.03
          = 0 + 2,400 + 7,500 + 8,640 + 6,000                   =    24,540.0000
        hospital tier, floor 20,000: 0 + 0 + 5,000 + 8,400 + 6,000
                                                                =    19,400.0000
        blend   = 0.63 x 24,540 + 0.37 x 19,400                 =    22,638.2000
        paid    = 1.885433 x 22,638.2000                        =    42,682.8093
      bigeubyeo inpatient
        base    = 1,716,000 x 1.0 x 0.70                        = 1,201,200.0000
        room    = 0.55 x min(0, 750,000) + 0.30 x min(150,000, 750,000)
                  + 0.15 x min(600,000, 750,000)                =   135,000.0000
        paid    = 0.014140 x ( 1,201,200 + 135,000 )            =    18,893.8680
      bigeubyeo outpatient, per visit
        45,000 -> ded max(30,000, 13,500) = 30,000 -> pay  15,000 x 0.35
        90,000 -> ded max(30,000, 27,000) = 30,000 -> pay  60,000 x 0.30
        180,000-> ded max(30,000, 54,000) = 54,000 -> pay 126,000 x 0.22
        400,000-> ded max(30,000, 120,000)= 120,000-> pay min(280,000, 200,000) x 0.10
        900,000-> ded max(30,000, 270,000)= 270,000-> pay min(630,000, 200,000) x 0.03
        = 5,250 + 18,000 + 27,720 + 20,000 + 6,000              =    76,970.0000
        visits  = min( 0.236694, 100 )                          =     0.2366940
        out     = 0.236694 x 76,970                             =    18,218.3372
    Step 4: the three named classes, and the injection carve-out.
      per act: physio 97,020   inject 121,200   mri 467,250
      physio acts  = min(0.092047, 50) = 0.092047 <= 10, so no gate
        claim      = min( 0.092047 x 97,020, 3,500,000 )        =     8,930.3999
      inject acts  = min(0.078898, 50) x (1 - 0.25) = 0.0591735
        claim      = min( 0.0591735 x 121,200, 2,500,000 )      =     7,171.8282
        carve      = 0.078898 x 0.25 x 121,200                  =     2,390.6094
      mri          = min( 0.015780 x 467,250, 3,000,000 )       =     7,373.2050
      NP_OUT       = 18,218.3372 + 2,390.6094                   =    20,608.9466
      NP_THREE     = 8,930.3999 + 7,171.8282 + 7,373.2050       =    23,475.4331
    Step 5: the annual aggregates.  raw_ge = 56,076.2173, raw_np = 39,502.8146.
      The test is sigma x raw <= 50,000,000 on each bojang jongmok, i.e.
      raw <= 50,000,000 / 0.15 = 333,333,333 and 50,000,000 / 0.85
      = 58,823,529; both raws are three orders below the tighter of
      the two, so g_ge(1) = g_np(1) = 1.0000000000
    claims_ann_pp(1) = 13,393.4080 + 42,682.8093 + 18,893.8680
                     + 20,608.9466 + 23,475.4331                =   119,054.4651
    loss_incurred_pp(1)                                         =   186,006.8254
      -> the claim is 64.005% of the covered loss; the rest is
         the 20/30% retention and the flat deductibles.

    Month 0 itself, at l(0) = 1.0000000000:
      premiums       = 11,982.0000 x 1.0000000000               =    11,982.0000
      claims_ge_in   = 13,393.4080 / 12 x 1.0                   =     1,116.1173
      claims_ge_out  = 42,682.8093 / 12 x 1.0                   =     3,556.9008
      claims_np_in   = 18,893.8680 / 12 x 1.0                   =     1,574.4890
      claims_np_out  = 20,608.9466 / 12 x 1.0                   =     1,717.4122
      claims_np_three= 23,475.4331 / 12 x 1.0                   =     1,956.2861
      claims         = 119,054.4651 / 12                        =     9,921.2054
      expenses       = 0.07 x 11,982.0000                       =       838.7400
      claim_expenses = 0.03 x 9,921.2054                        =       297.6362
      commissions    = 0.06 x 11,982.0000                       =       718.9200
      net_cf         = 11,982.0000 - 9,921.2054 - 838.7400
                       - 297.6362 - 718.9200                    =       205.4984
      cross-check    = 0.87 x 11,982.0000 - 1.03 x 9,921.2054   =       205.4984
    Decrements at the end of month 0 ( (0+1) mod 12 != 0, so no renewal decline ):
      pols_death  = 1.0000000000 x 0.0001100825                 = 0.0001100825
      BEF_LAPSE   = 1.0000000000 x (1 - 0.0001100825)           = 0.9998899175
      pols_lapse  = 0.9998899175 x 0.0087416110                 = 0.0087406487
      l(1)        = 0.9998899175 x (1 - 0.0087416110)           = 0.9911492689

**Trace, `t = 1` — the scaling row, and why every other month of the year is one.**

    l(1) = 0.9911492689.  y = 1 still, age 40 still, so every per-policy quantity
    of the trace above is unchanged and month 1 is month 0 scaled:
      premiums        = 11,982.0000    x 0.9911492689           =    11,875.9505
      claims_ge_in    =  1,116.1173333 x 0.9911492689           =     1,106.2389
      claims_ge_out   =  3,556.9007784 x 0.9911492689           =     3,525.4196
      claims_np_in    =  1,574.4890000 x 0.9911492689           =     1,560.5536
      claims_np_out   =  1,717.4122150 x 0.9911492689           =     1,702.2119
      claims_np_three =  1,956.2860950 x 0.9911492689           =     1,938.9715
      expenses        =    838.7400000 x 0.9911492689           =       831.3165
      claim_expenses  =    297.6361627 x 0.9911492689           =       295.0019
      commissions     =    718.9200000 x 0.9911492689           =       712.5570
      net_cf          =    205.4984156 x 0.9911492689           =       203.6796
      l(2)            = 0.9911492689 x (1 - 0.0001100825)
                                       x (1 - 0.0087416110)     = 0.9823768732

**The whole of policy year 1 is one set of rates and one linear scaling.** That is a
property of this product, not a shortcut: every contractual mechanism resets annually, so
the month carries no information the year does not. The consequence for a reader is that a
monthly grid here buys **timing** and nothing else — and, on an undiscounted projection,
timing buys nothing at all. The grid is monthly because the premium mode is monthly and
because the decrements are, not because the benefit is.

**Trace, `t = 11 → t = 12` — the renewal, decrement first and then the re-rate.**

    Decrements at the end of month 11.  (11+1) mod 12 = 0, so the renewal
    decline acts, after mortality, lapse and suspension:
      l(11)         = 0.9068380084
      pols_death    = 0.9068380084 x 0.0001100825               = 0.0000998270
      BEF_LAPSE     = 0.9068380084 - 0.0000998270               = 0.9067381814
      pols_lapse    = 0.9067381814 x 0.0087416110               = 0.0079263524
      BEF_SUSPEND   = 0.9067381814 - 0.0079263524               = 0.8988118290
      pols_suspend  = 0.8988118290 x 0                          = 0.0000000000
      BEF_RENEWAL   = 0.8988118290
      pols_renewal_decline = 0.8988118290 x 0.01                = 0.0089881183
      l(12)         = 0.8988118290 x (1 - 0.01)                 = 0.8898237107
      roll-forward  = 0.9068380084 - 0.8898237107 - 0.0000998270
                      - 0.0079263524 - 0 - 0.0089881183 - 0     = 0.0000000000

    The re-rate.  y = 2, age 41.  b_ge = clip(0.010, +-0.25) = 0.010;
    b_np = clip(0.081, +-0.25) = 0.081.  The corridor applies to the
    AGE-ADJUSTED prior premium:
      G_ge(2) = 4,792.80 x 1.04 x 1.010 = 4,792.80 x 1.05040    =     5,034.3571
      G_np(2) = 7,189.20 x 1.04 x 1.081 = 7,189.20 x 1.12424    =     8,082.3862
      R(2)    = 1.0  (reld_start_year = 4, so the loop is not yet live)
      nc(2)   = 0    (y < 3)
      G(2)    = ( 5,034.3571 + 8,082.3862 x 1.0 ) x (1 - 0)     =    13,116.7433
      step    = 13,116.7433 / 11,982.0000                       = +9.4704%
                of which the geubyeo unit +5.040% and the
                bigeubyeo unit +12.424%
    Month 12, at l(12) = 0.8898237107:
      premiums        = 13,116.7433 x 0.8898237107              =    11,671.5892
      claims_ge_in    = 13,527.3421 / 12 x 0.8898237107         =     1,003.0791
      claims_ge_out   = 43,113.4649 / 12 x 0.8898237107         =     3,196.9486
      claims_np_in    = 20,424.2713 / 12 x 0.8898237107         =     1,514.5001
      claims_np_out   = 22,172.8241 / 12 x 0.8898237107         =     1,644.1587
      claims_np_three = 25,512.7458 / 12 x 0.8898237107         =     1,891.8205
      claims          = 124,750.6482 / 12 x 0.8898237107        =     9,250.5071
      expenses        = 0.07 x 11,671.5892                      =       817.0112
      claim_expenses  = 0.03 x 9,250.5071                       =       277.5152
      commissions     = 0.06 x 11,671.5892                      =       700.2954
      net_cf          = 0.87 x 11,671.5892 - 1.03 x 9,250.5071  =       626.2604

**The premium *falls* month by month inside a policy year and *rises* at the boundary**, and
both movements are the same fact seen twice: `premiums(t) = G(y) × l(t)`, so inside a year
only `l` moves and it only falls, while at the boundary the +9.4704% re-rate outweighs twelve
months of decrement. The `net_cf` triples because the claim, spread evenly through the year,
rises only with the 8.1% and 1.0% cost trends while the premium rises with those trends
**and** the 4% age loading.

**Trace, `t = 59 → t = 60` — the 재가입 that does nothing and the band step that does
everything.**

    y = 6, age 45, and util_band(6) = 45 for the first time.  The five-year
    bojang naeyong byeongyeong jugi also falls here, and is a NO-OP by
    assumption: nothing in the model changes at re-entry.
    New frequencies, all from the (M, 45) row:
      adm 0.017674 (x1.2499), visits_ge 2.224811 (x1.18),
      visits_np 0.279298 (x1.18), physio 0.112298 (x1.22),
      inject 0.096255 (x1.22), mri 0.020198 (x1.28), los 8.25 (x1.10)
    Trends at y = 6:  f_ge = 1.010^5 = 1.0510100501,
                      f_np = 1.081^5 = 1.4761431304
      C_ge(6) = ( 0.017674 x 1,184,000 + 2.224811 x 36,100 ) x 1.0510100501
              = ( 20,926.0160 + 80,315.6771 ) x 1.0510100501    =   106,406.0369
      tau(6)  = min( 1, 3,260,000 / 106,406.0369 )              =     1.0000000000
      GE_IN   = 0.017674 x 1,184,000 x 1.0510100501 x 0.80      =    17,594.7625
      GE_OUT  = 2.224811 x [ 0.63 x e(clinic) + 0.37 x e(hosp) ]=    52,957.9121
      NP_IN   = 0.017674 x [ 1,716,000 x 1.4761431304 x 0.70
                             + room(8.25 days) ]                =    34,699.7101
      NP_OUT  = 0.279298 x e(np_out) + carve                    =    34,485.9651
      NP_THREE= 16,430.9164 + 13,328.1121 + 13,931.1237         =    43,690.1521
      claims_ann_pp(6)                                          =   183,428.5019
    Premium: G_ge(6) = 6,128.6225, G_np(6) = 12,911.4712,
             R(6) = 1.0025494000, nc(6) = 0.5314584961
      G(6) = ( 6,128.6225 + 12,911.4712 x 1.0025494 )
             x ( 1 - 0.10 x 0.5314584961 )                      =    18,059.3589
    Month 60, at l(60) = 0.7141205641:
      premiums = 18,059.3589 x 0.7141205641                     =    12,896.5596
      claims   = 183,428.5019 / 12 x 0.7141205641               =    10,915.8388
      net_cf   = 0.87 x 12,896.5596 - 1.03 x 10,915.8388        =       -23.3071

    The step, decomposed:  claims x 1.2758, premium x 1.0994, so the
    loss ratio jumps from 0.7294 to 0.8464, through the model's own
    break-even of 0.8447 -- and policy year 6 is the only negative year
    in the projection.

**Why the negative year is a property of a banded table and not a defect.** Holding the
frequencies at the `(M, 40)` row and letting only the trend run would give a year-6 claim of
**₩150,937.05** against the model's ₩183,428.50 — the band step alone is worth **+21.53%**,
or **1.0398 a year compounded over the five years of age it represents**. The 표준약관's
stylised age loading is 1.04 a year, and `1.04^5 = 1.216653` against the table's 1.215265:
**the utilisation table's five-year step and the wording's 4% annual loading agree to within
0.12%**. They simply do not arrive at the same time. The premium takes the age effect
smoothly at every renewal; the claim takes it in one jump every five years. So the loss ratio
saw-tooths, and the trough-to-peak swing is the whole of the model's margin.

### Undiscounted totals over the 120 months

Per policy issued. `pols_if` sums to months of exposure.

| Item | Value |
|---|---|
| `pols_if` (sum) | 88.998122 policy-months = 7.416510 policy-years |
| `premiums` | **1,558,165.4328** |
| `claims_ge_in` | 115,320.6688 |
| `claims_ge_out` | 357,128.9114 |
| `claims_np_in` | 222,875.2985 |
| `claims_np_out` | 223,623.9771 |
| `claims_np_three` | 282,146.3147 |
| **claims, all five limbs** | **1,201,095.1706** |
| `expenses` | 109,071.5803 |
| `claim_expenses` | 36,032.8551 |
| `commissions` | 93,489.9260 |
| **`net_cf`** | **118,475.9008** |
| loss ratio over the projection | **0.770839** |
| margin, `net_cf` ÷ `premiums` | **0.076036** |

Policy-year totals, which is the clock everything runs on:

| policy year | attained age | `pols_if` months | `premiums` | claims, all five | `expenses` | `claim_expenses` | `commissions` | `net_cf` | loss ratio |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 40 | 11.432747 | 136,987.1764 | 113,426.6331 | 9,589.1024 | 3,402.7990 | 8,219.2306 | 2,349.4114 | 0.828009 |
| 2 | 41 | 10.374553 | 136,080.3438 | 107,852.6803 | 9,525.6241 | 3,235.5804 | 8,164.8206 | 7,301.6384 | 0.792566 |
| 3 | 42 | 9.710708 | 132,169.3262 | 105,812.7236 | 9,251.8528 | 3,174.3817 | 7,930.1596 | 6,000.2085 | 0.800585 |
| 4 | 43 | 9.211361 | 137,543.5718 | 105,256.6906 | 9,628.0500 | 3,157.7007 | 8,252.6143 | 11,248.5162 | 0.765261 |
| 5 | 44 | 8.807655 | 144,678.6216 | 105,530.7628 | 10,127.5035 | 3,165.9229 | 8,680.7173 | 17,173.7150 | 0.729415 |
| **6** | **45** | 8.460681 | 152,794.4700 | 129,327.4993 | 10,695.6129 | 3,879.8250 | 9,167.6682 | **−276.1354** | **0.846415** |
| 7 | 46 | 8.152615 | 162,814.0368 | 130,973.1958 | 11,396.9826 | 3,929.1959 | 9,768.8422 | 6,745.8204 | 0.804434 |
| 8 | 47 | 7.871220 | 173,181.5075 | 132,415.0893 | 12,122.7055 | 3,972.4527 | 10,390.8905 | 14,280.3696 | 0.764603 |
| 9 | 48 | 7.610823 | 184,658.3987 | 134,200.7651 | 12,926.0879 | 4,026.0230 | 11,079.5039 | 22,426.0188 | 0.726751 |
| 10 | 49 | 7.365760 | 197,257.9800 | 136,299.1308 | 13,808.0586 | 4,088.9739 | 11,835.4788 | 31,226.3379 | 0.690969 |

The annual per-policy claim quantities behind those totals, which is where the contractual
machinery is visible:

| `y` | age | band | `oop_incurred_ge` | `oop_trunc` | `claims_ge_in_pp` | `claims_ge_out_pp` | `claims_np_in_pp` | `claims_np_out_pp` | `claims_np_three_pp` | `claims_ann_pp` | `loss_incurred_pp` | `claims_np_rated_pp` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 40 | 40 | 84,805.8913 | 1.0000 | 13,393.4080 | 42,682.8093 | 18,893.8680 | 20,608.9466 | 23,475.4331 | 119,054.4651 | 186,006.8254 | 53,531.5106 |
| 2 | 41 | 40 | 85,653.9502 | 1.0000 | 13,527.3421 | 43,113.4649 | 20,424.2713 | 22,172.8241 | 25,512.7458 | 124,750.6482 | 195,052.1600 | 57,893.3650 |
| 3 | 42 | 40 | 86,510.4897 | 1.0000 | 13,662.6155 | 43,548.4269 | 22,078.6373 | 23,753.2315 | 27,715.0809 | 130,757.9921 | 204,769.9545 | 62,514.9072 |
| 4 | 43 | 40 | 87,375.5946 | 1.0000 | 13,799.2417 | 43,987.7386 | 23,850.1902 | 25,399.2461 | 30,085.5877 | 137,122.0043 | 215,214.0760 | 67,434.7704 |
| 5 | 44 | 40 | 88,249.3506 | 1.0000 | 13,937.2341 | 44,431.4435 | 25,653.2049 | 27,178.5880 | 32,580.0369 | 143,780.5073 | 226,442.7489 | 72,600.0553 |
| 6 | 45 | 45 | 106,406.0369 | 1.0000 | 17,594.7625 | 52,957.9121 | 34,699.7101 | 34,485.9651 | 43,690.1521 | 183,428.5019 | 288,743.9336 | 95,944.4532 |
| 7 | 46 | 45 | 107,470.0973 | 1.0000 | 17,770.7101 | 53,492.0076 | 37,333.2268 | 36,886.9549 | 47,299.2243 | 192,782.1238 | 304,577.3636 | 103,291.4952 |
| 8 | 47 | 45 | 108,544.7983 | 1.0000 | 17,948.4172 | 54,031.4440 | 40,180.0584 | 38,542.0111 | 51,170.3302 | 201,872.2610 | 321,617.7532 | 110,408.5397 |
| 9 | 48 | 45 | 109,630.2463 | 1.0000 | 18,127.9014 | 54,576.2748 | 43,257.4834 | 40,317.8373 | 55,315.1269 | 211,594.6238 | 339,962.1105 | 118,056.8805 |
| 10 | 49 | 45 | 110,726.5487 | 1.0000 | 18,309.1804 | 55,126.5540 | 46,584.1798 | 42,237.5054 | 59,795.6522 | 222,053.0718 | 359,715.2940 | 126,324.7368 |

### Reading the shape of the result

The stream is **positive in every policy year but one**, and the one exception is policy year
6, at **−₩276.14**. That is the whole shape, and it decomposes cleanly because the ledger
collapses to `net_cf = 0.87 × premiums − 1.03 × claims`: the sign of any period is decided by
one number, the loss ratio, against the model's own break-even of **0.844660**. Year 1 runs
at **0.828009** — which is not an accident but the calibration, reproducing the published
4세대 2022 상반기 combined 경과손해율 of 82.8% on the published ₩11,982 premium anchor
[R12] [R1] — so the product opens with a margin of about **1.7%** of premium and a claim that
is already 98% of the way to break-even. On a real 4세대 book that margin was not there: the
generation ran 91.5% in 2022, 113.8% in 2023, 111.9% in 2024 and **115.1%** in 2025 [R7]
[R8], and `product-spec.md` explains why a newly launched Korean generation is under-priced
by regulatory construction — the five-year grace on rate-adequacy verification of
감독규정 제7-63조제2항제6호가목 meant 4세대 first re-rated in 2025, and it was priced off
「'16년도 2세대 요율」 to begin with [R12] [REG-R17]. **The model reproduces the published
2022 loss ratio and then lets the contractual re-rating machinery run; the real book did not
get to re-rate for four years.** The gap between this projection's +₩118,476 and the line's
actual −₩1.87조 underwriting result in 2025 [R7] is that four-year freeze, not a difference
of view about the mechanics.

Inside that, the loss ratio **saw-tooths downward**: 0.828, 0.793, 0.801, 0.765, 0.729, then
a jump to 0.846 at the band step, then 0.804, 0.765, 0.727, 0.691. Two forces make the teeth.
The premium takes its 4% age loading **smoothly at every renewal**, nine times over the
projection, compounding to 1.04⁹ = 1.4233; the claim takes its age effect in **one 21.53%
step**, at attained age 45, because the utilisation table is banded in fives and the next step
falls at age 50, one year beyond the horizon. So the projection catches one of the two steps
the age loading is paying for, and the loss ratio drifts down by about a sixth over ten
years. **That drift is a horizon artefact and would reverse at policy year 11**, and saying so
is more useful than smoothing the table would be: a five-year banded basis and an annual age
loading do not compose smoothly, and a ten-year run from an issue age of 40 lands
asymmetrically on the boundary.

The **composition** of the claim is not what the market narrative suggests. 급여 통원 is the
single largest limb at **29.73%** of the ten-year claim, and the whole 급여 half is **39.33%**
against 60.67% 비급여 — close to, and 3.6 points above, the 57.1% 비급여 share the supervisor
reports for 2025 [R7], and far above 비급여's 15.8% share of *national* medical spend [R9]. The
3대비급여 classes alone are **23.49%** of the claim on a cell that is not a heavy user of
them. And the 급여 unit runs at a loss ratio of **0.975** in year 1 against the 비급여 unit's
**0.730** — **the main contract is the worse half, throughout**, which is exactly what the
published 4세대 statistics show (급여 97.5% / 154.6%, 비급여 73.0% / 114.2% between 2022 H1
and 2024 H1 [R12]) and exactly the opposite of what a reader primed by the 비급여 할인·할증
publicity would expect. A model that treats the 급여 unit as the stable half will mis-project
the renewal path.

Finally, **the loop does very little on an average cell, and that is the correct answer.**
Over ten years the experience relativity moves the average rider premium by at most 0.95%
(`reld_avg` reaching 1.0095494), and for the first four years by nothing at all. That is what
revenue neutrality means: the surcharge funds the discount, so the *average* is untouched
until the [std] 5% cap on the discount breaks the neutrality. The scheme's whole effect is
**cross-sectional** — a band-5 policyholder pays 0.40 + 0.60 × 4.00 = **2.80×** the base
total premium while a band-1 policyholder pays 0.40 + 0.60 × 0.9575 = **0.9745×** — and a
single average cell cannot show it. What the average cell *can* show, and does, is the
**migration**: with fixed money thresholds and a trending claim, contracts cross into the
surcharge bands year after year. The 3단계 buckets empty entirely by policy year 5, and the
5단계 contribution to the surcharge pool rises from 0.012 at commencement to **0.040** by
policy year 7 — a factor of 3.33 — while the pool above the 2단계 base goes from 0.049 to
0.064. That migration is the part of the design that compounds, and it is the reason the
discount cap binds at all.

---

## Valuation and reserve pointers

This model projects **gross, undiscounted liability cash flows**. Every valuation layer
below consumes them and is cited, never reproduced. Korea is the only market in this
repository running three of them at once and all three live.

- **책임준비금.** 보험업법 제120조제1항 requires a 책임준비금 and a 비상위험준비금 at each
  결산기, carrying no method and no rate itself [REG-R3]. 시행령 제63조제1항, amended
  2022-12-27, restates the reserve in IFRS 17 vocabulary as
  **보험계약부채 = 발생사고요소 + 잔여보장요소**, both on a 현행추정치 basis, and confines
  비상위험준비금 to non-life business [REG-R8]. **On a one-year indemnity contract the
  weighting inverts relative to every other `krlib` product**: the 잔여보장요소 is at most
  one policy year's unearned premium, and the 발생사고요소 — claims incurred and not yet
  settled — is the material item. That is the reserving consequence of a monthly-mode
  contract with a 3 영업일 / 30 영업일 settlement timetable [S1 제8조] and it is not a
  consequence this projection computes.
- **해약환급금준비금 has nothing to bite on.** 감독규정 제6-11조의6 creates the
  Korea-specific overlay because IFRS 17 measurement can fall below the contractual
  surrender value [REG-R11]. **There is no surrender value here at all** [S3], so the
  overlay is identically nil — the only product in `krlib` of which that is true. The
  표준해약공제액 cap of [별표 14] likewise does not engage [REG-R20], and neither do the
  해약환급금 articles 제7-66조 through 제7-70조 except for the 미경과보험료 limb of
  제7-66조제5항 [REG-R19] [REG-R17].
- **K-ICS.** In force since 2023-01-01. 시행령 제65조제2항제1호 states the requirement in one
  line — 「지급여력비율은 100분의 100 이상을 유지할 것」 [REG-R8] — and
  감독규정 제7-2조제2항 decomposes the 생명·장기손해보험위험액 into seven sub-risks, of
  which three bear directly on this contract: **장해·질병위험액** (a shock to morbidity),
  **해지위험액** (「보험계약자의 옵션행사율 변화 또는 보험계약 대량해지」) and
  **대재해위험액** for epidemics and mass accidents, measured by 위험계수방식 rather than by
  shock [REG-R13]. A one-year renewable indemnity contract is the archetype of a product
  whose charge is dominated by the morbidity shock and by the lapse-**option** risk — the
  renewal decline is literally an 옵션행사율 — and whose interest-rate exposure is
  negligible. What this model owes that regime is the **capability** it demands: a
  frequency and severity basis parameterized so that a shock can be applied per grouping,
  and a decrement structure in which the renewal option is a separate rate. It computes no
  요구자본.
- **IFRS 17, and the boundary.** K-IFRS 제1117호 has been mandatory for Korean insurers
  since 2023-01-01 — **not** voluntary as in Japan [REG-R60]. The boundary question this
  contract raises is genuine and this document asserts no answer: a one-year term, an
  unrestricted right to re-rate, a supervisor-set ±25% cap on that re-rating, a five-year
  re-entry into a wording the insurer does not control, and an obligation not to refuse
  re-entry on health grounds [S1 제23조] [S1 제30조] [REG-R17]. Pulling the other way is
  the wording's own 「종전 계약의 보험기간을 연장하는 것으로 보아」 at 제3조제6항 [S1],
  which makes renewal and re-entry continuations for benefit purposes. Nothing retrieved
  states an industry or supervisory position on where the boundary falls for that
  combination, and the general boundary test was read only in secondary summary form
  [unverified]. `Medical_KR_S` projects to a **stated** horizon on stated terms and computes
  no CSM; a user who takes the boundary at one year should read only `t = 0 … 11`, and a
  user who takes it at the 재가입 should read `t = 0 … 59`. Both readings are available in
  the same frame, which is the point of publishing the whole of it.
- **Rate adequacy is a *supervisory* obligation, and it is what the renewal machinery
  serves.** 감독규정 제7-63조제2항제6호가목 requires 「경험통계 등을 기초로 순보험요율의
  적정성을 매년 검증할 것」, with up to five years' grace for genuinely new cover [R12]
  [REG-R17]. The 보험연구원's principal recommendation is to shorten the grace to three
  years [R12]. And 제7-45조제7항 requires the **보험가격지수** — 보험료총액 ÷ (참조순보험료
  총액 + 보험회사 평균사업비총액) — to be explained to a 실손 policyholder **at every
  renewal**, not only at sale [REG-R22]. For this product that index has no denominator:
  there is no 실손 참조순보험요율 [R20].
- **Not applicable.** 계약자배당 and the surplus-distribution machinery [REG-R12] do not
  attach — the contract is 순수보장성 with no 계약자적립액. 비상위험준비금 is confined to
  non-life business and is asset- and catastrophe-driven rather than a liability projection
  [REG-R8]. 특별계정 does not arise [REG-R6] [REG-R15].
- **Policyholder tax, not modelled.** The premium qualifies for the **보장성보험료
  세액공제** of 소득세법 제59조의4제1항 — a **credit** of 12% of premiums paid, capped at
  ₩1,000,000 of premium a year [REG-R57]. On the anchor cell that is ₩11,982 × 12 =
  ₩143,784 of first-year premium, well inside the cap, for a credit of about **₩17,254**
  before the local surtax. It is a credit and not a deduction, which changes the after-tax
  comparison against every other market in this repository. Benefits are not projected net
  of policyholder tax.
- **What this model does not compute, listed so that nothing downstream assumes it does.**
  No 책임준비금, no CSM, no risk adjustment, no fulfilment cash flow, no K-ICS requirement,
  no 해약환급금준비금, no 비상위험준비금, no discounting and no policyholder tax.

---

## Key sensitivities and model risks

In rough order of leverage on a 실손 block.

1. **The whole claim basis is [std], and it has no public counterpart to be checked
   against.** Frequency, severity, the annual-claim shape and the zero-claim mass are four
   independent constructions on aggregate supervisory experience [R7] [R8] [R12], not an
   insurer's 위험률 — which is unpublished by regulation [REG-R2] — and not a
   참조순보험요율, because none exists for this product [R20]. The **level** is pinned by
   one solve against one published pair of loss ratios in one half-year [R12]; everything
   else about the basis is shape. A user with company data should replace all four tables
   before drawing any conclusion, and the `provenance` column on every row exists for
   exactly that.
2. **The severity *distribution*, not its mean.** The deductible is
   `max(flat floor, percentage)`, so the payment is kinked and the shape decides the claim.
   Substituting each stream's mean for its distribution changes the 비급여 통원 payment by
   **+35.83%** (₩104,545 against ₩76,970) and the 급여 통원 hospital tier by **−17.01%**,
   while leaving MRI unchanged, because every MRI point sits above its crossing. The
   dispersion being standardized over is real and published: 도수치료 quoted between
   **₩5,000 and ₩600,000** across Seoul hospitals [R2].
3. **The 급여/비급여 boundary moves inside any realistic horizon, and the model holds it
   fixed.** 요양급여 covers everything except what the 보건복지부장관 designates
   비급여대상, so 비급여 is a residual defined by exclusion from a list that changes
   [REG-R53]. 5세대's **관리급여** category migrates over-used 비급여 items into the covered
   system at a **95% co-payment** [R6]: if 도수치료 becomes 관리급여 it leaves the rider
   entirely and enters the main contract, changing which unit is re-rated, which claim
   counts for the 요율 상대도, and which limit applies. **A model that assumes a static
   partition will be wrong within the projection horizon.**
4. **The two cost trends carry the whole re-rating, and they are one year's national
   growth rates.** `med_trend_ge = 1.0%` and `med_trend_np = 8.1%` are 2024 figures [R9]
   [REG-R41]. The whole premium path, the loop's band migration and the corridor's bite
   are functions of them. At `trend_mult = 4.5` (model point 10) the 비급여 re-rate would
   be 36.45% and the corridor clips it to 25%.
5. **The corridor is a weaker constraint than it looks.** The ±25% corridor and the 4% age
   loading **compose**, so the wording admits a re-rate of 1.25 × 1.04 = **1.30** a year on
   a single 위험구분단위; the corridor does not bind *economically* below about a 30% claim
   trend. On model point 10, whose 비급여 re-rate is clipped from 36.45% to 25% in every
   one of nine renewals, the ten-year loss ratio still rises only from 0.533 to 0.591. That
   is a model finding worth printing, and it cuts against the intuition that a 25% cap is
   the binding constraint on Korean 실손 pricing.
6. **The band-1 discount is a *solved* quantity and it is sensitive to a distribution nobody
   publishes twice the same way.** On the 손보 commencement mix 72.9 / 25.3 / 0.8 / 0.7 /
   0.3 [R12] the identity gives a 4.25% discount; on the FSC's 62.1 / 36.6 / 1.3 [R3] it
   gives **2.1%**. The published statements bracket both — 「5% 내외」 [R1], −5% 잠정 [R3],
   95% in the wording's illustration [S1] — and the [std] 5% cap is the only thing stopping
   the solve running away once the claim level trends. The cap's level is the single
   assumption with the largest effect on the loop's aggregate behaviour, and it has two
   published anchors and no observed range.
7. **The zero-claim mass is held constant and it would not be.** `claim_shape_table.csv`
   trends its amounts and not its frequency, so 72.9% of contracts have no rated claim in
   every projected year. In reality the frequency of claiming rises with age, the 1단계
   share falls, `w₁` shrinks, and the solved discount deepens for the survivors while the
   surcharge pool grows. Both effects push `reld_avg` up faster than this model shows.
8. **Successive years' claiming is assumed independent, and it is not.** The 무사고 할인
   share is `w₁(y−1) × w₁(y)` = 0.729012² = 0.5315 **[std]**. Real claiming persists, so the
   true share of two-year claim-free contracts is **higher** than the independent product,
   and this model therefore **understates** the discount and overstates the premium. Nothing
   published gives the persistence of claiming.
9. **Mortality runs the wrong way here.** Death **releases** the liability on this contract,
   so an over-statement of mortality is *anti*-conservative — the reverse of every
   protection product in `krlib`. Over the ten projected years the anchor cell loses
   **0.011647** of a policy to death against **0.315540** to lapse and **0.072409** to the
   renewal decline, so the exposure is small here; on a projection to the maximum cover age
   of 100 it would not be.
10. **Lapse and the renewal decline are one published number split three ways.** The 3.3%
    blended in-force decay of the 1–3세대 block [R7] is the only 실손-specific persistency
    figure there is, and it contains lapse, death, conversion and renewal decline together.
    The split into a 10% → 2% lapse curve and a 1% renewal decline is **[std]**, and the
    first-year rate rests on an [unverified] news figure. On a product with no surrender
    value, no policy loan and an annual re-rate, persistency is a first-order driver.
11. **The behavioural response is unmodelled and the supervisor says it is the point.**
    [R2]'s own example has a policyholder cutting claims by 93% under a surcharge. A model
    that projects the premium's response to claims without the claims' response to premium
    **overstates the surcharge revenue and understates the discount take-up** in the same
    breath.
12. **Concentration.** 65% of insureds claim nothing in a year and the top decile takes
    about 74% of all claims [R4] [R5] [R6]. A single cell carrying the population mean
    frequency is not a policyholder anybody would recognise, and it is the reason model
    point 8 exists at `util_mult = 10` — the only shipped point on which the
    본인부담상한제 truncation binds, taking it from 0.8018 in policy year 1 to 0.6024 by
    policy year 10 and driving `reld_avg` to 1.3290.
13. **The 재가입 is modelled as a no-op and it is not one.** At `t = 60` the contract in
    reality re-enters the generation then on sale, at that generation's partition,
    co-payments and limits and at a premium the insurer sets for it. The 5세대 deltas in
    `product-spec.md` change the rider into two riders, the 비중증 co-payment to 50%, the
    비중증 annual limit to ₩10,000,000 and the relativity's scope to 특약2 only [S2] [R5]
    [R6]. Anything this projection says about policy years 6–10 is a statement about
    4세대 terms that will not be in force.
14. **Two clocks that are never reconciled.** The 본인부담상한제 runs on the calendar year
    [R10]; every contractual limit runs on the policy year [S1 제5조제2항]; and the
    insurer's own experience statistics run on the calendar year [R7] [R8]. This model runs
    everything on the policy year and says so.

### Known modeling pitfalls

Each of these is a mistake a competent modeller would actually make on this product, and
each is checkable against the shipped model.

- **Do not multiply a rate by the 보험가입금액.** There is no sum assured here. The
  ₩50,000,000 is an annual **cap**, and it may appear in a formula only inside a `min`. Any
  expression in which `annual_limit()` is a multiplier has the dimensions of money and the
  meaning of nothing. This is the single commonest error made by an actuary arriving from a
  fixed-benefit 제3보험 product, and `check_indemnity()` is the constraint that catches it:
  `claims_ann_pp(y) ≤ loss_incurred_pp(y)`, with year 1 at **119,054.4651 ≤
  186,006.8254**, a ratio of 0.6401.
- **Apply the deductible to the distribution, not to the mean.** For the 비급여 통원 stream
  `E[max(0, X − max(30,000, 0.30X))] = 76,970` while
  `max(0, μ − max(30,000, 0.30μ)) = 104,545` — **+35.83%**. The trap is that the error can
  hide: on the 급여 통원 limb the clinic tier is +6.36% and the hospital tier −17.01%, and
  the blend at `clinic_share = 0.63` comes out only **−1.05%** wrong. A model that checks
  the blend and not the tiers will pass its own test and misprice both providers.
- **The 본인부담상한제 is an exclusion from covered loss, not a cap on the benefit, and it
  goes first.** `oop_trunc(y)` multiplies the incurred cost *inside* `paid_out_per_visit`,
  so it changes where the deductible bites; applying it to the finished claim instead is
  linear on the inpatient limb and **wrong on the outpatient limb**, where the deductible is
  kinked. `check_oop_ceiling()` asserts the statement about the loss —
  `oop_incurred_ge(y) × oop_trunc(y) ≤ oop_ceiling()` — and not a statement about the
  benefit. On the anchor `oop_trunc ≡ 1.0` and the error is invisible; on model point 8 it
  is not, which is why that model point exists.
- **The ₩2,000,000 inpatient co-payment cap sits on the retention that *survives* the
  ceiling.** Both reduce the insured's retention on heavy 급여 use, so applying them in
  parallel, or the cap first, double-counts the relief. `claims_ge_in_pp` computes
  `cost = adm × μ × trend × trunc` and then `top_up = max(0, cost × r_ge − 2,000,000)` in
  that order.
- **The corridor applies to the age-adjusted prior premium, and the wording's own label
  misleads.** 「기초율 증가분 = 전년도 기준보험료 × 25%」 reads as additive, but 3,640 is
  25% of 14,000 × 1.04 [S1 제30조]. `prem_np_base(10) = 20,625.8505` on the correct
  recursion `7,189.20 × (1.04 × 1.081)⁹` and **20,096.9929** on the additive misreading —
  2.564% low, and compounding. `check_renewal_corridor()` measures the move **against the
  age-adjusted prior premium** and per 위험구분단위, so it catches the loading applied on the
  wrong side of the clip.
- **The experience relativity touches the rider and nothing else.** Applying `reld_avg(y)`
  to the whole office premium gives a year-5 gross of **₩16,440.5468** instead of
  **₩16,426.4626**. 「비급여 특약 보험료만 할증되며 보험료 전체가 할증되는 것은
  아닙니다」 [R2].
- **The band-1 relativity is solved, not 0.95.** Hard-coding the illustration's 95% [S1]
  from policy year 2 gives `reld_avg = 0.729012 × 0.95 + 0.301988 = 0.9945494` — a 0.55%
  leak out of a scheme the wording requires be self-financing, growing as the band mix
  moves. `check_relativity_neutral()` asserts `Σ_b w_b r_b = 1` exactly while the discount
  cap is slack, and asserts only that the scheme never funds a discount it has not collected
  once the cap binds.
- **The 무사고 할인 has a two-year lookback and the relativity has one.** `noclaim_share(3)
  = band_share(2, 1) × band_share(3, 1) = 0.729012² = 0.5314584961`, not 0.729012. A
  one-year lookback gives a year-3 office premium of **₩13,326.7028** against the correct
  **₩13,610.6786** — 2.09% low — and hands the 10% discount to policyholders who have earned
  one clean year rather than two. The two reliefs also apply to different bases: the
  relativity to the rider, the 무사고 할인 to the whole premium.
- **There is no no-claims ladder.** 「보험금 지급(사고) 이력이 1년마다 초기화됩니다」 [R2].
  `band_share(y, b)` reads `claims_np_rated_pp(y − 1)` and nothing earlier. A model that
  accumulates band state across years invents a persistence the wording explicitly removes,
  and turns a memoryless one-year lookback into a bonus-malus chain.
- **The injection carve-out must be counted once.** 25% of the injection acts leave the
  ₩2,500,000 sub-limit for the main ₩50,000,000 limit [S1 특별약관 제3조(3)제2항], so
  `acts_inject_eff(1) = 0.75 × 0.078898 = 0.0591735` and the carved payment
  **₩2,390.6094** is added in `claims_np_out_pp`, not in `claims_np_three_pp`.
  Double-counting it inflates the year-1 claim by 2.0%; forgetting the removal from
  `acts_inject_eff` deflates it by the same amount and puts the money under the wrong limit.
- **Read the utilisation table at the *attained* age, not the issue age.** `util_band(6) =
  45` and `adm_rate(6) / adm_rate(5) = 1.2499293`. Freezing the band at issue gives a
  year-6 claim of **₩150,937.05** against **₩183,428.50** — **17.71% low** — and turns the
  projection's only negative policy year into a comfortably positive one, which is the
  worst kind of error because it removes the one thing the projection had to say.
- **`lapse_rate` is annual and `lapse_rate_mth` is monthly, and the library spells them
  apart for this reason.** `lapse_rate(0) = 0.10` against `lapse_rate_mth(0) =
  0.0087416110`. Using the annual rate on the monthly grid takes `pols_if(12)` from
  0.8898237107 to about 0.28.
- **The renewal decline is not lapse and must not be folded into it.** It is non-zero only
  where `(t + 1) mod 12 = 0`, it acts **after** mortality, lapse and suspension, and it is
  the **larger** of the two voluntary exits at every annual boundary —
  0.0089881183 against 0.0079263524 at `t = 11`, and 0.0083529502 against 0.0043181413 at
  `t = 23`. Folding it into `w(t)` makes the annual boundary invisible, and on a contract
  whose whole architecture is annual that is the boundary the model exists to show.
  `check_pols_roll_fwd()` balances either way, so the roll-forward will not catch it.
- **The 3대비급여 limbs never pass through the annual-limit factor.** Their money caps
  **replace** the ₩50,000,000 aggregate for those three classes rather than sitting inside
  it [S1 특별약관 제3조(3) <표1>], so `claims_np_three_pp(y)` is summed apart from
  `claims_np_main_pp(y)` and `np_limit_factor(y)` is applied only to the latter. And where
  3대비급여형 is **not** held those treatments are uncovered — they do not fall back into
  the main limit. Model point 6 is that election.
- **`reld_exempt_share` reduces the *rating count*, never the benefit.**
  `claims_np_pp(1) = 62,978.2477` is paid in full; `claims_np_rated_pp(1) = 0.85 ×
  62,978.2477 = 53,531.5106` is what the band is read against. The severely ill are exempt
  from the **rating**, not from the cover [S1 특별약관 제6조제3항] [REG-R54]. Applying the
  15% to the claim would silently delete a fifteenth of the benefit.
- **The 상급병실료 cap is a daily average, not a nightly cap.** `min(0.50 × charge,
  ₩100,000 × D)` with `D` the whole admission's length [S1 특별약관 제3조]. On the anchor
  the room payment is ₩135,000 over 7.5 days — **₩18,000 a day against a ₩100,000 cap** —
  so the cap is slack by a factor of 5.6 and the largest capped point (0.50 × ₩1,200,000 =
  ₩600,000) sits below the ₩750,000 stay cap. A per-night implementation on a varying
  nightly charge pays strictly less; this model cannot show the difference because it holds
  only the admission total, and that limitation is stated rather than hidden.
- **Do not delete a limit because it reads slack.** `check_annual_limits()` is `True` on
  every shipped model point because `E[min(X, Λ)] ≠ min(E[X], Λ)` and a single cell's
  expected annual claim is two orders of magnitude below every money limit — the
  supervisor's own tail figure is 0.005% of insureds above ₩50,000,000 in 2019 [R1]. The
  check proves the machinery is **wired**, not that it is **exercised**, and every one of
  those limits binds under a seriatim or stochastic run.
- **`result_cf()` publishes the five claim limbs and no `claims` subtotal.** The columns
  must sum to `net_cf` with the three expense limbs, which is what `check_net_cf()`
  asserts; a subtotal column beside the splits invites a limb being counted twice
  invisibly. The `claims(t, kind)` cells stays, and `claims(t)` with no `kind` is the sum.
- **`expenses` is maintenance only and `claim_expenses` is claim-driven.** 7% of premium
  and 3% of **claims** respectively, on a [std] split of one published 16.1% aggregate
  [R7]. Folding the claim expense into `expenses` — or charging it on premium — makes a
  premium-driven cost and a claim-driven cost move together, and it breaks the two-term
  identity `net_cf = 0.87 × premiums − 1.03 × claims` that the whole shape of this
  projection rests on. `check_expense_split()` ties the three rates back to the published
  total.
- **There is no acquisition strain, and inventing one is as wrong as omitting a real one.**
  On a one-year renewable contract renewed on a rolling basis the acquisition/renewal
  distinction has no content after year one, so `commissions(t) = 0.06 × premiums(t)` is
  level and `t = 0` is **positive at ₩205.4984**. A reader who expects the sister
  libraries' month-0 trough will look for a bug that is not there.
- **The two age conventions are both real and neither may be silently dropped.** The model
  runs on 만나이 and the contract prices on 보험나이 [S1 제21조] [REG-R25]; the two differ
  for half of all issue dates, so half a year of age sits between the projection basis and
  the pricing basis. Model point 1's `issue_age = 40` is a 만나이.
- **The premium is an input for policy year 1 only.** `premium_mth_pp()` is
  `prem_ge_base(1) + prem_np_base(1)`; every later year is the recursion. A model that
  re-reads the model point premium in year `y > 1` throws away the entire renewal
  machinery, and on this cell would collect **₩1,066,375.5027** of premium over the 120
  months instead of the projected **₩1,558,165.4328** — 31.6% less — while leaving the claim
  untouched, which turns a +₩118,476 result into a loss of about ₩309,381.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-indemnity_medical-r1
[R10]: #krlib-indemnity_medical-r10
[R12]: #krlib-indemnity_medical-r12
[R16]: #krlib-indemnity_medical-r16
[R19]: #krlib-indemnity_medical-r19
[R2]: #krlib-indemnity_medical-r2
[R20]: #krlib-indemnity_medical-r20
[R3]: #krlib-indemnity_medical-r3
[R4]: #krlib-indemnity_medical-r4
[R5]: #krlib-indemnity_medical-r5
[R6]: #krlib-indemnity_medical-r6
[R7]: #krlib-indemnity_medical-r7
[R8]: #krlib-indemnity_medical-r8
[R9]: #krlib-indemnity_medical-r9
[REG-R11]: #krlib-reg-r11
[REG-R12]: #krlib-reg-r12
[REG-R13]: #krlib-reg-r13
[REG-R15]: #krlib-reg-r15
[REG-R17]: #krlib-reg-r17
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R22]: #krlib-reg-r22
[REG-R23]: #krlib-reg-r23
[REG-R25]: #krlib-reg-r25
[REG-R3]: #krlib-reg-r3
[REG-R38]: #krlib-reg-r38
[REG-R39]: #krlib-reg-r39
[REG-R4]: #krlib-reg-r4
[REG-R41]: #krlib-reg-r41
[REG-R44]: #krlib-reg-r44
[REG-R49]: #krlib-reg-r49
[REG-R51]: #krlib-reg-r51
[REG-R53]: #krlib-reg-r53
[REG-R54]: #krlib-reg-r54
[REG-R57]: #krlib-reg-r57
[REG-R6]: #krlib-reg-r6
[REG-R60]: #krlib-reg-r60
[REG-R61]: #krlib-reg-r61
[REG-R62]: #krlib-reg-r62
[REG-R8]: #krlib-reg-r8
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
