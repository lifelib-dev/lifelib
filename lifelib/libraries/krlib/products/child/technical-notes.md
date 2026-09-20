# Technical Notes

**Status:** Draft, 2026-09-03 (all cited sources accessed 2026-09-03).

**Scope note.** These notes turn the standardized composite children's insurance
(*eorini boheom*, 어린이보험) of `product-spec.md` (same directory) into a reference
liability cash-flow projection on paper, and then into `Child_KR_S` beside it. **They
describe no single insurer's contract.** [S#] and [R#] tags resolve against `sources.md`,
whose numbering is carried verbatim from `_research/child.md` and is frozen; [REG-R#] tags
resolve against the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is separate and
also frozen. **[std]** marks a standardization introduced for the reference implementation,
always with a rationale and, where one exists, the observed range across insurers;
[unverified] marks a claim that could not be confirmed against a retrieved document.
**Every contractual parameter these notes share with `product-spec.md` carries the same
value there**, and **every number in the worked example is read off the shipped model**
rather than recomputed by hand.

What these notes add, and `product-spec.md` does not carry because none of it is
contractual, is the whole modelling basis: the **foetal-loss rate** over the pre-birth
months; the **eleven-cause incidence grid** and its severity parameters; the **length-of-day
basis** of the two hospital-cash limbs; the **nine-limb 태아 module** with its frequencies
and its expected paid days; the **계약자's disability-to-mortality ratio**, which is what
turns a mortality table into a waiver decrement on a second life; the **lapse** curve; the
**expense and commission** scales; and the **notional 보험가입금액** that lets a product with
no death benefit enter the 표준해약공제액 formula at all. Every one of them is introduced
below as **[std]**, with the direction of the error it carries.

---

## Deltas against the 정액 제3보험 chassis

The [cancer 정액 chassis (암보험)](../cancer/technical-notes.md) specifies, once, the
machinery this product inherits: a diagnosis-triggered lump sum on a tier ladder, the 90일
면책기간 (*myeonchaek gigan*, waiting period) before invasive cover attaches, the 감액기간
(*gamaek gigan*, reduced-benefit period) sitting on top of it as a second and softer
anti-selection device, the 유사암 (*yusaam*, borderline and in-situ cancer) reduced tier at a
stated fraction of the general amount, the premium waiver correlated with the diagnosis, and
the **계약자적립액 (*gyeyakja jeongnipaek*, the policyholder's account balance) paid on a
death the contract does not cover**. It also settles, for the whole library, the
surrender-value regime of 감독규정 제7-65조 to 제7-70조, which 제7-69조 and 제7-70조 apply to
장기손해보험 and to 제3보험 *mutatis mutandis* [REG-R19]. None of that is restated here.

Nine things change, and the first two have **no counterpart in `uslib`, `uklib`, `jplib`,
`frlib` or `delib`**.

1. **태아가입 (*taea gaip*, foetal enrolment) — the contract is written before the insured
   exists.** A 태아 (*taea*, foetus) has no legal
   personality and cannot be the 피보험자 of an 인보험 contract, so the 태아가입특칙 makes
   the foetus the insured **at birth**: 「제53조의 태아는 출생시에 피보험자가 됩니다」
   [S8 제54조] [R3]. The projection therefore opens on a life that does not yet exist.
   Months `t = 0` to `t = b − 1` carry premium income on three streams, the pre-birth limbs
   of the 태아 module, **no mortality and no morbidity on the insured at all**, and a
   **void** decrement rather than a lapse one — 유산 or 사산 makes the contract 무효 and
   every premium paid is returned [S8 제56조] [S9]. `born(t)` gates every cover on the
   child's own life and `check_cover_at_birth()` asserts the gate. The chassis has no such
   state and no such decrement.
2. **보험료 납입면제 (*boheomnyo naip myeonje*, premium waiver) on the 계약자 (*gyeyakja*,
   the policyholder) — a premium-waiver decrement on a life who is not the insured.** The
   chassis waives on the insured's own first invasive diagnosis. Here the
   waiver fires on the child's trigger set **or on the policyholder's death or 50% 이상
   장해**: 「보험료 납입기간 중 가입자녀가 암으로 진단확정되거나 … 또는 **계약자가 사망**
   또는 … 장해지급률이 50% 이상인 장해상태가 되었을 때에는 차회 이후의 보험료 납입을
   면제하여 드립니다」 [S10 제22조제1항]. It is lawful in one clause because that wording
   makes the 피보험자 of the contract 「계약자와 가입자녀」 [S10 제3조]. So the model carries
   **two decrement lives** and the premium stream stops on the earlier of two events drawn
   from **two different rows of one mortality table**. On the 손해보험 chassis the same
   economics arrive instead as a compulsory 부양자 death rider on the parent's own life
   [S5] [S11] — a *benefit*, not a decrement — and modelling one as the other is wrong in
   both level and shape.
3. **Both of the chassis's anti-selection devices are switched off, and by supervisory
   action rather than by drafting taste.** The 90-day 면책기간 is disapplied below 보험나이
   15 — 「최초계약과 부활계약의 면책기간은 **보험나이 15세 이상인 경우에만 적용**」 [S3],
   and 「보장개시일(계약일로부터 90일이 지난날의 다음날, **계약일 현재 보험나이 15세 미만
   피보험자의 경우 1회 보험료를 받은 때**)」 [S11] — and entirely on a 태아가입용 cover
   [S3]. The 감액기간 was removed from foetal contracts by a 변경권고 of 2015-06-17 across
   17 carriers and 56 products [R2]. **The test is applied at the 계약일 and not at the
   claim date**, so a contract issued at 계약나이 0 has no cancer waiting period at any
   point in its hundred-year life, including the eighty-five years in which the insured is
   an adult. `waiting_mths = 0` and `reduction_mths = 0` on the anchor cell.
4. **Thirteen benefit limbs, not four, and the largest is a day benefit.** The chassis is a
   diagnosis product with care limbs bolted on. This one is a **bundled stack** on the
   손해보험협회 comparison basis [R12] — a 상해후유장해 기본계약 and its 질병 twin, four
   diagnosis limbs, a 수술비, two hospital-cash limbs, 골절 and 화상, a liability rider and a
   태아 module. Over
   the whole projection `claims_hospital` is **47.0%** of morbidity outgo and
   `claims_diagnosis` **26.6%**; on the chassis those proportions are reversed.
5. **A third-party liability cover, which only a non-life licence may write.** 가족일상생활
   배상책임 is the one limb whose claim is a **third party's loss** rather than a state of
   the insured [R5] [S5]. It is a **3년만기 갱신형** block inside a 비갱신형 core [S2] whose
   누수사고 limb carries a 90-day 보장개시일 **resetting at every renewal** [S5] [S3] — the
   only place in this model where the 갱신형 mechanic has a cash consequence.
6. **Two ages, and on a foetal contract the offset is exact.** The chassis projects on 만나이
   with a [std] half-year offset against 보험나이. Here the model carries **both**: `age(t)`
   is 보험나이 and `age_man(t)` is 만나이, and on a 태아 contract 「보험금 지급기준표에서
   적용하는 피보험자 나이는 **피보험자가 출생한 날부터** 계산합니다」 [S8 제58조] while
   「계약일에 있어서의 피보험자의 계약나이는 0세로 합니다」 [S8 제60조], so the two differ by
   exactly `birth_month()` months for the life of the contract. **The contract expires when
   the insured is 99 years and 7 months old, not 100.**
7. **The 표준형 (*pyojunhyeong*, the standard surrender-value form) is the base run, not the
   무해지 (*muhaeji*, no-surrender-value) form.** `Cancer_KR_S` ships the 미지급형,
   which is where the market is. `Child_KR_S` deliberately ships the **표준형**: the 적립부분
   credited at the 공시이율 exists only there — the suppressed forms are 순수보장성 and show
   「-」 for it on the board [S11] [S2] — and the 표준형's surrender value **exceeds premiums
   paid from about year 30** on the published grid [S2], a shape no other `krlib` protection
   product produces and only a hundred-year term can. Model points 4 and 5 carry the
   suppressed forms.
8. **The notional 보험가입금액 is computed, not assumed.** The chassis stands in a
   `notional_sa_ratio` of 0.60 for the [별표 15] 제9호 ratio it cannot evaluate [REG-R21].
   Here it is evaluated: 제9호 reads 보험가입금액 = (위험보험료 ÷ 정기보험의 위험보험료) ×
   정기보험의 보험가입금액, and a term policy's risk premium per unit of face is its mortality
   rate, so the notional amount is **the first policy year's risk premium divided by the
   mortality rate at the 기준연령 요건, 남자 만 40세** [REG-R9 제1-2조제2호](#krlib-reg-r9). At a child age
   `q` is so small that the [별표 14] formula limb exceeds **thirty-six years** of premium; at
   40 it is still **56.25 months of core premium**, so on this product it never binds and the
   표준해약공제액 is the [REG-R29] reading of the same cap — **13 months**, ₩364,000.00 — of
   which the 90% the model deducts is **11.70 months**.
9. **The horizon.** At 계약나이 0 to a 100세 만기 the projection runs **1,200 monthly
   periods** — `t = 0 … 1,199`, plus the terminal 계약해당일 row at `t = 1,200` — the
   longest in `krlib`, with premium over the first 240. **Eighty of the
   hundred years are paid-up** and they decide the contract: **89.4% of all outgo falls after
   `t = 240`**, against nil premium.

The [long-term care technical notes (간병보험)](../long_term_care/technical-notes.md) state
their own deltas against the same chassis. The [indemnity medical technical notes
(실손의료보험)](../indemnity_medical/technical-notes.md) share nothing with it but the
제3보험 statutory class — and are the reason this product has **no indemnity limb at all**:
from April 2018 실손의료보험 must be sold as a standalone product of indemnity-medical cover
only, under 감독규정 제7-63조제2항제1호 as amended 2017-03-22 [R9] [R10] [REG-R17]. A Korean
family buys the indemnity layer as `Medical_KR_S` and the fixed-benefit layer as
`Child_KR_S`, as two contracts, and the split is statutory rather than a modelling choice.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows** for a single-policy
  model point of 어린이보험: office premium on three streams; the 상해후유장해 기본계약 and
  its 질병 twin; four diagnosis lump sums; the 수술비; two hospital-cash limbs; 골절 and
  화상; the 가족일상생활배상책임 rider; the nine-limb 태아 module; the **계약자적립액 plus
  미경과보험료** paid on a death the contract does not cover; the **해약환급금 plus
  미경과보험료** paid on surrender; the **refund of every premium** on a pre-birth void;
  maintenance and claim-handling expense; and commission. Undiscounted and gross of
  reinsurance. Korea runs **three** measurement bases over one such stream and all three are
  live: IFRS 17 (K-IFRS 제1117호, mandatory since 2023-01-01) [REG-R60], K-ICS from the same
  quarter [REG-R13], and the **해약환급금준비금**, which has no counterpart anywhere else in
  this repository [REG-R11]. **Discounting, the risk adjustment, the CSM, 요구자본 and every
  reserve are out of scope** and are cited, not reproduced — see *Valuation and reserve
  pointers*.
- **Projection frequency.** **Monthly grid**, and monthly by construction. Four of the
  product's mechanics live on it: 월납 is the mode every published premium in the file is
  quoted on [R12] [S11]; **birth falls on a month boundary**, which is what makes the
  pre-birth period a whole number of grid steps; the 태아 module's 1년만기 신생아 block is
  twelve of them; and the 납입최고 window is operated as a calendar-month one, 「납입기일
  다음날부터 납입기일이 속하는 달의 다음달 마지막 날까지」 [S8]. `t` is the **policy
  month** and is **0-based**, on the library-wide convention: `t = 0` is the first projected
  month, month `t` is the interval from `t` to `t + 1` months after the 계약일, the
  contractual (1-based) policy year containing it is `policy_year(t) = t // 12 + 1`, and
  the frame is `t = 0, 1, …, proj_len − 1`.
- **`proj_len()` is the number of projected months — the exclusive end of the frame.**
  `proj_len = 12 × (term_age − issue_age) + 1`, so **1,201** on the anchor cell and **1,201
  rows** in `result_cf()`, indexed `t = 0 … 1,200`. Throughout these notes `n = proj_len − 1`
  is the **terminal 계약해당일 index**, `12 × (term_age − issue_age)` = **1,200** on the
  anchor cell: the 1,200 months of the 보험기간 are `t = 0 … 1,199` and month `t = n` is the
  100세 계약해당일 itself, where every cash
  flow is zero, `pols_maturity` records the cover ending, and `claims(t, "MATURITY")`
  is **0.0000** — there is **no 만기환급금** on the protection part [S1] [S2] and the shipped
  환급률 progression reaches zero at 만기.
- **Two ages, and which one does what.** The contract's clock is **보험나이** (*boheom nai*,
  insurance age): 「계약일 현재 피보험자의 실제 만 나이를 기준으로 6개월 미만의 끝수는
  버리고 6개월 이상의 끝수는 1년으로 하여 계산하며, 이후 매년 계약해당일에 나이가 증가」,
  identical in both 표준약관, reproduced verbatim by every carrier, with the worked example
  생년월일 1988-10-02 / 계약일 2014-04-13 ⇒ 25년 6월 11일 ⇒ **26세**
  [R8] [S7 제27조] [S8 제30조] [S12 제30조] [REG-R25 제21조](#krlib-reg-r25). `age(t) = issue_age + t // 12`
  is that clock and it governs the premium, the 갱신형 anniversary and the 보험나이 15
  thresholds; **the registered age basis for this model is 보험나이**, deliberately, because
  on a foetal contract it is the *only* age defined at `t = 0`. Every decrement table is
  nonetheless read at **만나이**, `age_man(t) = issue_age_man + (t − b) // 12`, because every
  public series they are built from is published on it [REG-R38] [REG-R39] [REG-R40]
  [REG-R41] and no source supplies the distribution of issue dates a conversion would need.
  On an ordinary contract the offset is taken as zero **[std]**; on a 태아 contract it is
  exactly `b` months, and `age_man(t) = −1` before birth because the insured does not exist.
- **Timing conventions [std].** Office premium and maintenance expense at the **start** of
  month `t`; every morbidity benefit, the 계약자적립액 on death, the 해약환급금 on lapse, the
  premium refund on a pre-birth void and the claim-handling expense at the **end** of month
  `t`; decrements at the end of month `t`, in the order **void, waiver, mortality, lapse**.
  Acquisition expense and initial commission at `t = 0`.
- **Cover attaches at birth.** This is not a timing convention but a contractual one, and it
  was enforced: in July 2016 sixteen carriers and nineteen products were ordered to stop
  advertising 「태아 때부터 보장」, 「엄마 뱃속에서부터 보장」 and 「태어나기 전부터 보장」
  under 감독규정 제4-35조제3항 [R2]. The one carve-out is the 태아보장기간 itself, whose
  limbs pay **from the date of birth** even where the insured event preceded it
  [S8 제59조] — which is why they are gated by `t == b` rather than by `born(t)`, and tested
  separately by `check_neonatal_term()`.
- **Model points.** One policy at a time, on an expected (probability-weighted) basis.
  `Projection` is parameterized by `point_id`; no aggregation logic is specified here. Ten
  points are shipped and **every one satisfies every `check_*()` cells**.
- **Termination.** Cover to the **100세 계약해당일**. Four exits and not two: the pre-birth
  **void**, death, lapse, and maturity. Paying a benefit neither terminates nor exhausts the
  contract; the `frac_open` ledgers exhaust a **cover** and not the policy.
- **Contract boundary.** The core covers are 비갱신형, level-premium and 무배당 with no
  insurer repricing right [S1] [S2] [S12] [REG-R12], so every future premium and benefit on
  them is inside the boundary and the horizon is the whole term. The **갱신형 blocks** —
  가족일상생활배상책임 at 3년만기 [S2], and named riders at one to three years [S3] [S5] —
  reprice at attained age at each renewal, which would ordinarily close the boundary there.
  `krlib` projects them to final expiry and **records the tension rather than resolving it**,
  exactly as `Term_KR_S`, `Cancer_KR_S` and `Medical_KR_S` do. It is a K-IFRS 1117 question
  [REG-R60] this model does not answer.
- **Currency.** KRW throughout. There is no minor unit in the contract, but expected values
  are fractional; displayed to the precision each table states.
- **Rounding.** Intermediates at full double precision. The worked example displays `pols_if`
  and every policy count to **ten decimals** and every cash flow to **four**. **Monthly rows
  rounded for display do not re-add to the displayed totals**; the totals are sums of
  unrounded values.
- **What this model is not.** It is a **mechanics demonstration**. The office premium is a
  model-point input, every incidence rate but one is a [std] construction, and the expense
  and commission scales are [std] throughout. Replace the assumption tables with company data
  before drawing any conclusion from the output.

---

## Model point attributes

| Attribute | Type | Anchor cell (`point_id = 1`) |
|---|---|---|
| `policy_id` | str | CH-KR-0001 |
| `sex` | enum {M, F} | **M** — priced male because the sex is unknown at issue |
| `issue_age` (`x`) | int, **보험나이**, 0–15 (태아 = 0) | **0** |
| `foetal` | 0/1 — 태아가입 | **1** |
| `birth_month` (`b`) | int policy months, 0 unless `foetal` | **5** |
| `term_age` | int, 만기 보험나이 ∈ {30, 100, 110} | 100 |
| `prem_period_years` | int years | 20 |
| `premium_mth` (`P_core`) | KRW/month, office, **model-point input** | **28,000** **[std]** |
| `premium_foetal_mth` (`P_foet`) | KRW/month, 태아 module, 전기납 | **3,000** **[std]** |
| `cv_form` | enum {std, susp, graded} | std (표준형) |
| `cv_floor_ratio` (`k`) | suppressed form's post-완납 fraction | 1.0 (inert on `std`) |
| `waiver_child` | 0/1 — the child's 납입면제 | **1** |
| `waiver_payer` | 0/1 — the **계약자's** 납입면제 module | **1** |
| `payer_age` | int, **만나이** of the 계약자 at the 계약일 | **33** **[std]** |
| `payer_sex` | enum {M, F} | M |
| `sa_disability` | 기본계약 일반상해후유장해, KRW | 100,000,000 (1억원) |
| `sa_disease_disab` | 질병후유장해, KRW | 10,000,000 (1천만원) |
| `sa_cancer` / `sa_minor_cancer` | 암(유사암 제외) / 유사암, KRW | 10,000,000 / 2,000,000 |
| `sa_cerebral` / `sa_cardiac` | 뇌출혈 / 급성심근경색증, KRW | 10,000,000 / 10,000,000 |
| `sa_surgery` | 수술비 per named-disease operation, KRW | 5,000,000 (500만원) |
| `hosp_daily` | 입원일당 per day, 1~180일 basis, KRW | 40,000 (4만원) |
| `sa_fracture` / `sa_burn` | 골절진단비 / 화상진단비, KRW | 400,000 / 200,000 |
| `sa_liability` | 가족일상생활배상책임 per occurrence, KRW | 100,000,000 (1억원) |
| `sa_neonatal` | the 태아 module's own 가입금액, KRW | 10,000,000 |
| `broad_def` | 0/1 — broad 뇌혈관질환 / 허혈성심장질환 definitions | 0 |
| `waiting_mths` (`W`) | 면책기간 in months | **0** |
| `reduction_mths` (`G`) | 감액기간 in months ∈ {0, 12} | **0** |
| `prem_discount_rate` / `_mths` | the 2026 저출산 discount [R6] | 0 / 0 |
| `lapse_basis` | enum {loglinear, disclosed, flat} | loglinear |
| `mort_be_factor` | multiplier from table to best estimate | 1.0 |

Derived scalars on the anchor cell, all read off the shipped model:

| Cells | Value |
|---|---|
| `proj_len()` (the number of months; the frame is `t = 0 … 1200`) | **1201** |
| `prem_period_mths()` / `prem_end()` | 240 / 239 |
| `foetal_cover_end()` / `foetal_prem_end()` | **17** / **16** |
| `pols_if_init()` | 1.0 |
| `risk_prem_ann_pp()` | 145,537.04939942522 |
| `sa_notional_pp()` | 132,306,408.54493201 |
| `prem_net_ann_pp()` | 252,000.0 |
| `surr_chg_coef()` | 20 |
| [별표 14] formula limb (does **not** bind) | 1,575,064.08544932 |
| `surr_chg_cap_pp()` (표준해약공제액) | **364,000.0** |
| `surr_chg_period()` | 84 months |
| `acq_cost_pp()` | 327,600.0 |
| `acq_cost_months()` | **11.7** |
| `comm_init_pp()` | 212,940.0 |
| `neonatal_cost_pp("birth")` / `("block")` | 47,000.0 / 63,450.0 |

**`premium_mth` is an input, not a computed quantity.** No Korean carrier publishes a rate
table by age and duration: a carrier's own 적용위험률 and 예정사업비율 live in the 산출방법서,
an undisclosed 기초서류 [REG-R2], and the bureau's 참조순보험요율 is filed with the FSC under
보험업법 제176조제4항 with no general obligation to publish [REG-R4] — and the 장기손해보험
display that **is** published under 제176조제9항 carries risk rates, not office premiums
[REG-R61]. What *is* published is a specimen
premium per product on a standardised basis — 보험나이 5세, 상해 1급, 100세만기 20년납, 월납,
the 보장보험료 of the compulsory covers only [R12] — and on that nominally standardised
basis the observed levels vary **by a factor of seven**, ₩21,502 to ₩148,250 for a male
five-year-old, because carriers include different compulsory sets in the quoted figure [S11].
₩27,000 is the tight cluster of the three mid-market carriers whose compulsory sets are
closest to [R12]'s — ₩26,841, ₩26,999 and ₩27,480 [S11] — and the anchor cell adds ₩1,000
for the 계약자 waiver module, one carrier publishing that waiver as a benefit in its own
right at a 가입금액 of ₩100,000 [S11]. **Nothing in this model depends on ₩28,000 being a
market rate.** `equiv_premium_mth_pp()` computes the premium the shipped basis implies and,
per `product-spec.md`, **where the two differ these notes' figure governs**: on the anchor
cell it is **₩31,079.59**, which is 11.00% above the shipped premium.

**The 태아 module's premium is a second stream, and it is a real feature of the contract.**
「계약체결일부터 출생시점(출산 또는 분만 과정에서 보험금 지급사유가 발생하는 경우 포함)
까지의 기간을 보험기간으로 하여 아래의 보험기간 및 보험료 납입기간을 **추가로 부가**
합니다」 [S2], written elsewhere as a fixed 「1~10월만기 전기납 태아 월납」 sub-term [S1]. It
is 전기납 and payable monthly in advance, so a term ending at `t = 17` collects in months 0
to 16, giving an office premium of **₩31,000 to `t = 16` and ₩28,000 from `t = 17` to
`t = 239`**.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `pols_pay(t)` | In force at the start of month `t` and **still paying premium**; `pols_pay(0) = pols_if_init() = 1` | monthly recursion |
| `pols_waived(t)` | In force with the premium **waived**, on either life; `pols_waived(0) = 0` | monthly recursion |
| `pols_if(t)` | `pols_pay(t) + pols_waived(t)` — total in force at the start of `t` | derived |
| `pols_waiver_entry(t)` (`e`) | Policies whose waiver fires in month `t`, drawn from the paying compartment after the void | derived |
| `pols_void(t)` | Contracts de-recognised in month `t` because the pregnancy did not go to term; zero from birth | derived |
| `pols_death(t)`, `pols_lapse(t)`, `pols_maturity(t)` | The other three exits | derived |
| `frac_open(t, j)` | Probability that a policy in force at `t` has **not yet claimed** cover `j`, for the four 최초 1회한 diagnosis limbs; `frac_open(0, j) = 1` | monthly recursion |
| `cum_prem_pp(t)` | Cumulative **scheduled** core office premium per policy, at time `t` | derived |
| `prem_foetal_paid_pp(t)` | Cumulative 태아 module premium per policy, at time `t` | derived |
| `refund_ratio(t)` | 환급률 of the notional 표준형 at time `t`: `refund_build × refund_taper` | derived |
| `cv_std_pp(t)`, `cv_pp(t)` | The notional 표준형 해약환급금; the amount this form actually pays — both at time `t` | derived |
| `surr_chg_pp(t)` | Unamortised 해약공제액 at time `t` | derived |
| `av_pp(t)` | **계약자적립액** per policy at time `t`, recovered from the published surrender value | derived |
| `age(t)`, `age_man(t)` | Attained **보험나이**; attained **만나이**, `−1` before birth | annually |
| `born(t)` | `t >= b` — the gate on every cover written on the child's own life | derived |
| `mort_rate(t)`, `mort_rate_payer(t)` | Annual mortality of the **insured** (zero before birth) and of the **계약자** | lookup |
| `lapse_rate(t)`, `void_rate_mth(t)`, `waiver_rate(t)` | The three behavioural decrements | lookup |
| `net_cf(t)` | Net cash flow of month `t`, insurer perspective, **income-positive** | monthly |

**Every state variable here is a time-point value at time `t`, not a closing balance of
period `t`.** `cum_prem_pp`, `prem_foetal_paid_pp`, `refund_ratio`, `cv_std_pp`, `cv_pp`,
`surr_chg_pp` and `av_pp` are read at time `t` (`t = 0` at the 계약일), that is at the start
of month `t` and **before that month's premium**: `cum_prem_pp(0) = 0`, `av_pp(0) = 0`, and
twelve instalments stand at `t = 12`; `surr_chg_pp` is full at `t = 0` and nil at `t = 84`.
The counts `pols_if`, `pols_pay` and `pols_waived` are likewise at the start of month `t`.
The four exit payments of month `t` fall at its **end** and are valued on those
start-of-month quantities **[std]** — see *Processing order* below.

**Two compartments, not three, and not one.** The chassis needs three in-force states because
a 특정소액암 life is diagnosed, keeps paying and carries excess mortality. This product needs
**two**, and for a different reason: the waiver moves a policy from `pols_pay` to
`pols_waived` **without changing `pols_if`**, because cover continues in full — 「보장보험료
납입이 면제되며」, and payment of the 적립보험료 stops as well [S2]. A waived life carries the
same morbidity and the same mortality as a paying one; what it does not carry is **lapse**.
A policy paying nothing has nothing to lapse for, and no retrieved wording describes a
voluntary surrender out of a waived state; the treatment is **[std]** and is the one the
sister libraries use for a waived or claiming cohort. `check_waiver_split()` asserts
`pols_pay + pols_waived = pols_if` in every month, which is what says the second decrement
life has been carried without leaking policies into or out of the projection.

**The void is a fourth exit and it is not a lapse.** 「태아가 유산 또는 사산에 의해 출생하지
못한 경우에는 **계약을 무효로 합니다** … 이미 납입한 보험료를 돌려드립니다」 [S8 제56조]
[S9]. Nothing is retained, the contract is de-recognised rather than terminated, and the cash
flow is a **refund of premiums already collected** — the whole of both streams — rather than
a surrender value. Netting it into the lapse column would hide a decrement and mis-state the
cash flow that goes with it, and on the anchor cell it would mis-state it by the full
premium: `claims_void(4)` is ₩122.13 against a `cv_pp(4)` of **nil**. It has its own
decrement, its own `"VOID"` claim kind and its own column.

**The `frac_open` ledgers are per policy, not per block.** Each diagnosis benefit is 최초
1회한 [S1] [S2] [S11], so the exposed population is not the in-force block but the part of it
whose benefit line is still open. `frac_open(t+1, j) = frac_open(t, j) × (1 − i_j,m(t))`,
with incidence taken as independent of the exit decrements **[std]**. Weighting the ledger by
`pols_if` would measure the block's consumption rather than the individual's and defer the
exhaustion forever. On this product the quantity is worth watching in a way it is not on the
chassis: paediatric cancer incidence is two orders of magnitude below the adult rate, so the
general-tier ledger is almost untouched for thirty years and then drains fast — from
`frac_open(120, cancer) = 0.9987524571` at age 10 to **0.4023261296** at the 100세 계약해당일.
**Nearly 60% of the general-tier line has been used by the end of the term**, and that is
what a level premium on a 100세만기 child policy has to fund.

**Three absences are product facts, not gaps.** There is **no death benefit and the
prohibition is statutory** — 상법 제732조 makes a contract on the death of a person under 만
15세 void [R7] [REG-R50], 표준약관 제19조제2호 restates it and 제19조제3호 refuses to extend
the age-correction saving to it [R8] [REG-R25] — so `claims_death` is the **계약자적립액 plus
the 미경과보험료** and not a sum assured. There is **no 만기환급금**, so `claims_maturity` is
a column of zeros, published rather than dropped because the residual 적립부분 is a real
quantity on a contract whose term ends earlier. And there is **no 실손 limb of any kind**,
which is a regulatory fact and not a design choice [R9] [R10].

---

## Assumption inputs

### (a) Contractual / guaranteed elements (cited; the insurer cannot change them)

| Input | Value | Basis |
|---|---|---|
| 태아가입특칙 — the insured | 「태아는 **출생시에** 피보험자가 됩니다」 | [S8 제54조]; [S9 제45조]; [R3] |
| Cover attachment | **At birth**, not at the 계약일; sixteen carriers ordered in 2016 to stop advertising otherwise | [R2]; 감독규정 제4-35조제3항 |
| 유산 / 사산 | The contract is **무효** and **every premium paid is returned** | [S8 제56조]; [S9 제47조] |
| 계약나이 of a foetus | **0세 at the 계약일** | [S8 제60조] |
| Benefit-scale age of a foetus | Runs **from the date of birth** | [S8 제58조] |
| Late birth | Where birth falls **more than six months** after the 계약일 the 계약일 is moved back to six months before it and premiums and reserves re-set | [S8 제61조] |
| Pre-birth insured event | Paid, but **from the date of birth** | [S8 제59조] |
| 태아보장기간 | 계약체결일 ~ 출생시점, an **additional** 보험기간 with its own 전기납 premium | [S2]; [S1] (1~10월만기) |
| 신생아 block | **1년만기 전기납** from birth | [S2] [S5]; [R5] |
| 기본계약 | 일반상해후유장해, paid as **보험가입금액 × 장해지급률** on a continuous 3~100% band, payable more than once with the percentages accumulating | [R12]; [S1] [S2] [S11] |
| 면책기간, 보험나이 < 15 | **None** — 암보장개시일 = 제1회 보험료를 받은 때 | [S3]; [S11]; [R5] |
| 면책기간, 태아가입용 cover | 「면책기간 없음」 at all, including the 10-day waits | [S3] |
| 감액기간 | **None**; where one survives it is a first-year 50% | [S1] [S3] [S11] vs [S6] [S11] |
| 감액 on a foetal contract | **Never** — 「피보험자가 보험가입 당시 태아인 경우에는 보험금의 100%를 지급합니다」, inserted across 17 carriers and 56 products | [R2]; [S8] |
| 납입면제, the child | 50% 이상 후유장해 (상해 or 질병), one of the **7대질병**, or a 중대한특정상해수술 | [S2] |
| 납입면제, the P코드 carve-out | 「**출생전후기에 기원한 특정 병태(P코드) 진단시 납입면제를 적용하지 않음**」 | [S2] |
| 납입면제, the 계약자 | The **계약자's death or 50% 이상 장해**, in the main clause | [S10 제22조제1항]; [S10 제3조] |
| Waiver carries the riders | 「주계약의 보험료 납입이 면제되었을 때에는 이 특약의 차회 이후의 보험료 납입을 면제」 | [S8] |
| 입원일당 | **₩40,000 per day**, 1~180일 per stay | [R12]; [S2] |
| 배상책임 | **₩100,000,000** per occurrence, 대인 / 대물(누수) / 대물(비누수) each; 자기부담금 ₩500,000 누수 / ₩200,000 otherwise; **3년만기 갱신형** | [S5]; [S2] |
| 배상책임 누수 보장개시일 | **90 days** from the 계약일, **resetting to the renewal date at each renewal** | [S5]; [S3] |
| 저체중아 인큐베이터 일당 | 「최고 **60일**을 한도로 실제 사용일수에서 **2일을 공제**하고 1일당 가입금액」 | [S1] |
| 주산기질환 입원일당 | Continuous stay of **4 days or more**, **3일 초과 1일당**, **1회 입원당 120일 한도** | [S8]; [S1] |
| Death of the insured | No 사망보험금 below 만 15세; the **계약자적립액 + 미경과보험료** is paid and the contract ends | [R7]; [REG-R50 제732조·제736조](#krlib-reg-r50); [REG-R17 제7-63조제1항제1호](#krlib-reg-r17); [REG-R25 제22조](#krlib-reg-r25); [REG-R19 제7-66조제5항](#krlib-reg-r19) |
| 해약환급금 formula | 「**순보험료식 계약자적립액에서 해약공제액을 공제한 금액**」, floored at zero | [S2]; [S1]; [REG-R19 제7-66조제1항제1호](#krlib-reg-r19) |
| 미지급형 floor | **0%** during the 납입기간, **50% of the 표준형 value** afterwards | [S2] [S11]; [REG-R19 제7-66조제4항제2호](#krlib-reg-r19) |
| The 표준형 comparator is synthetic | 「해지율을 적용하지 않은 상품이며, 비교안내를 위한 종목으로 **실제로 판매하지 않음**」 | [S3]; [S1] |
| 납입최고 (grace) | **At least 14 days**; operated as a calendar-month window | [REG-R25 제26조](#krlib-reg-r25); [S8] |
| 부활 | Within **3 years** where no surrender value has been taken, subject to fresh underwriting; waiting periods re-run from the 부활일 | [S8]; [S3]; [REG-R25 제27조](#krlib-reg-r25) |
| Expiry | At the **100세 계약해당일**; there is no 만기환급금 on the protection part | [S1] [S2] [S11] |

### (b) Insurer-discretionary current elements

This class is **nearly empty, and its emptiness is a product fact.** The contract is
**무배당** at every carrier examined [S1]–[S6] [S11], so there is no 계약자배당 and the
surplus-distribution machinery of 감독규정 제6-11조의7 and 제6-13조 does not attach
[REG-R12]. There is no premium review on the 비갱신 core and no MVA. What remains:

| Input | Snapshot value | Basis |
|---|---|---|
| 보장부분 적용이율 | **2.75%** | **[std]**, the modal value of the comparison board's column; observed range **2.50%–3.00%** across ten carriers [S11] |
| 공시이율 (적립부분) | **1.70%**, named 「보장성 공시이율Ⅴ」, at 2026-07 | [S2]; observed 1.60%–2.20% [S11] |
| 최저보증이율 | **0.30%** | [S2]; observed 0.20%–0.50% [S11] |
| 평균공시이율 | **2.50%** for 2026, capped at the selling-date 공시이율 | [S2]; [REG-R9 제1-2조제13호](#krlib-reg-r9); [REG-R48] |
| 공시기준이율 formula | 외부지표금리수익률 × α + 운용자산이익률 × (1 − α) | [S1]; [REG-R24]; the α bracketing is **[unverified]** and nothing here depends on it |
| The 적용해지율 of a suppressed form | 5.0% / 3.0% / 1.0% during the 납입기간 by duration band, 0.5%–0.65% afterwards | [S1] — the **only** Korean child-policy lapse basis in public |
| 갱신형 renewal rates | Recomputed at attained age at each renewal | [S7 제29조]; base run holds the issue rate flat **[std]** |
| The 2026 저출산 discount | **1%–5% for one year**, per insurer | [R6]; off in the base run |
| 다자녀 / 출산 discounts | 1%–3% of 영업보험료 at five carriers | [S11]; not modelled **[std]** |

**A full-text search of the 감독규정 returns zero occurrences of 예정이율** [REG-R9]; what
the comparison board publishes instead is the **보장부분 적용이율**, the pricing rate under
another name, and that is what `prem_int_rate` is. It is used **only** by the equivalence
diagnostics — the projection itself does not discount.

### (c) Behavioral / experience assumptions (modeler's view — all [std])

**The data position for this product is the worst in the library, and it must be said
first.** Nothing on Korean child incidence — cancer, cerebrovascular disease, congenital
anomaly, low birth weight, NICU admission, paediatric length of stay — was retrieved from
보험개발원, 국가암정보센터 or 통계청 **in this product's own research pass**. **Every incidence
rate in `incidence_table.csv` is therefore a [std] construction**, each row's `provenance` cell
naming the authority its *shape* rests on rather than a source for its level, with exactly one
exception: the row the basic contract is calibrated on.

**That is a gap in the pass and not a gap in the public record, and the difference matters.**
보험개발원 publishes a dated **장기손해보험 참조순보험요율** display carrying, by age and sex,
a 「기타피부암 및 갑상선암 이외의 암 발생률」 grid on the insured definition that excludes C44
and C73, a 질병입원율 grid stated in expected days per life-year, and 후유장해 rates — and its
age grid reaches **연령 0 and 10** [REG-R61]. The `cancer` and `indemnity_medical` passes
opened it; this one did not, and [REG-R61] records the omission. So the shipped rows are
`[std]` because they were **never reconciled to that grid**, not because no grid exists. Two
consequences are carried rather than hidden. A 참조순보험요율 is a **net premium rate with a
safety loading in it, not a best estimate** [REG-R9] [REG-R61], so any use of it would still
need a [std] step down. And the divergence has no single sign: on the general cancer tier the
shipped paediatric anchors sit at about **0.6 (male) and 0.5 (female)** of the published rate
at 연령 0 and 10, while the adult anchors sit near or slightly above it. A later pass should
**re-base** these rows off [REG-R61] rather than rescale them.

**Mortality [std], and it serves two lives.** 경험생명표 — the industry table, 제10회 applied
from 2024-04 — is **not published in full**: 보험개발원 releases the 평균수명 and the 기대여명
and not the rates [REG-R33] [REG-R34]. `mort_table.csv` is a construction, log-linear between
anchor ages shaped on the 통계청 완전생명표 age pattern [REG-R38] [REG-R39], carrying the
three features a child policy is actually exposed to and that a table graduated from age 20
upwards would not have: the **infant peak**, the **childhood trough** at about age 10 and the
**adolescent turn**. Male 만나이 anchors:

| 만나이 | 0 | 1 | 5 | 10 | 15 | 20 | 33 | 40 | 50 | 60 | 70 | 80 | 90 | 100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `q(x)` | **0.0025** | 0.00025 | 0.00012 | 0.00009 | 0.00016 | 0.00035 | **0.00067713** | 0.0011 | 0.0026 | 0.006 | 0.015 | 0.043 | 0.13 | 0.31 |

`q(0) = 0.0025` is **about twenty times `q(5)`**, and it falls onto the anchor cell in exactly
the twelve months when the 태아 module is also paying. The table is read for the **insured** at
`age_man(t)` and for the **계약자** at `payer_age + t // 12`, and the two are the same file:
one Korean mortality construction, two lives, and the 계약자's rate at issue, `q(33) =
0.00067713`, is what drives the whole waiver decrement for the first policy year.
`mort_rate_mth(t) = 1 − (1 − q)^(1/12)` **[std]**.

**`mort_be_factor = 1.0`, and that identity is a decision.** The shipped table is a
population all-cause construction, not a valuation table with a prudential margin, so there is
nothing to unwind and scaling it would be inventing one; the hook is carried for a user
substituting a company table, and model point 10 runs at 1.10. On a child policy mortality
**releases** the liability, so an understatement of it **overstates** the liability.

**Morbidity — eleven causes, fourteen pivot ages, one published rate.** `incidence_table.csv`
carries eleven causes by sex at pivot 만나이 0, 1, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90
and 100, graduated **log-linearly** between adjacent pivots and returned **exactly at a
pivot**, so the one published rate reproduces to its printed digits:

    i_j(x) = exp( ln r(a) + (x − a)/(b − a) × ( ln r(b) − ln r(a) ) )               [std]

A logarithmic graduation is right because every one of these rates spans two or more orders of
magnitude across the age range — general-tier cancer incidence rises about two-hundredfold
from 만나이 10 to 80 — and a linear interpolation between decade pivots is wrong by a factor
of two mid-span. Male rates at the three ages the anchor cell's first eighteen months use:

| Cause | 만나이 0 | 만나이 1 | 만나이 5 | Unit |
|---|---|---|---|---|
| `disability` (일반상해후유장해 3~100%) | 0.000100265 | 0.00012761 | **0.0001823** | events/yr |
| `disease_disab` (질병후유장해 3~100%) | 0.0026 | 0.0009 | 0.0006 | events/yr |
| `cancer` (암, 유사암 제외) | 0.00018 | 0.00015 | 0.00012 | events/yr |
| `minor_cancer` (유사암) | 0.00003 | 0.000025 | 0.00002 | events/yr |
| `cerebral` (뇌출혈, narrow) | 0.00004 | 0.000012 | 0.00001 | events/yr |
| `cardiac` (급성심근경색증, narrow) | 0.000002 | 0.000001 | 0.000001 | events/yr |
| `fracture` (골절진단) | 0.004 | 0.009 | 0.02 | events/yr |
| `burn` (화상진단) | 0.006 | 0.005 | 0.003 | events/yr |
| `hosp_acc` (상해 입원) | 0.10 | 0.13 | 0.15 | **days**/yr |
| `hosp_dis` (질병 입원) | **2.40** | **1.10** | 0.55 | **days**/yr |
| `liability` (배상책임) | 0.004 | 0.006 | 0.009 | claims/yr |

**The one published rate is `disability` at 만나이 5**: 「일반상해 후유장해 발생률(3~100%),
기본계약, 5세, 상해 1급 — **남자 0.0001823, 여자 0.0001163**」 [S1]. It is the only
observation of a Korean child morbidity rate anywhere in the research file, it is a
**적용위험률** and therefore already a priced rate rather than a best estimate, and it is the
point the basic contract's whole decrement is calibrated on. Everything else in the table is a
shape drawn around it, and each row says which authority the shape rests on — the
국가암등록통계 연령별 발생률 [REG-R40], the 「기타피부암 및 갑상선암 이외의 암 발생률」 and
질병입원율 grids of the 참조순보험요율 display [REG-R61], and the 국민건강보험 진료비
실태조사 [REG-R41].

**The two `hosp_*` causes are expected days, not probabilities**, and that is the single most
important dimensional fact in this file. `hosp_dis` at 만나이 0 is **2.40 days a year**, not a
frequency of 240%: it is the infant peak — colds, fevers, bronchiolitis and the perinatal
tail — and it collapses to 1.10 at 만나이 1 and 0.55 at 5. Applying the monthly conversion
`1 − (1 − i)^(1/12)` to a number greater than one does not merely give a wrong answer, it
gives a **complex** one. These two causes are divided by twelve instead, and `benefit_pp` for
the `"HOSPITAL"` kind never calls `inc_rate_mth`.

**Sex, and why the composite reproduces the male-heavier direction.** The comparison board's
published premiums show the sex relativity with **no fixed sign**: four carriers price the
female above the male and seven below, the spread running from 62% to 114% of the male rate
[S11]. That is a benefit-mix effect and not a pure morbidity effect — the products differ in
whether the compulsory set is dominated by accident (male-heavy) or by cancer and thyroid
(female-heavy) limbs. The shipped table takes the **male-heavier** direction, because the
comparison basis it prices is dominated by a ₩100,000,000 accident-disability 기본계약 [R12]
and because the one published pair of rates runs that way — 0.0001823 male against 0.0001163
female at 만나이 5, a **ratio of 1.57** [S1]. Model point 3 is the female calibration cell
and prices out at **₩29,281.80** against model point 2's male **₩31,112.91**, a ratio of
**0.9411**.

**Severity — turning an incidence into a cost [std].** `basis_table.csv` carries thirteen
scalars, every one of them a standardization with no published anchor:

| Parameter | Value | What it stands over |
|---|---|---|
| `disab_severity` | **0.12** | The mean 장해지급률 on a 3~100% 일반상해후유장해 event. The cover is a **percentage scale, not a lump sum** [R12] [S1] [S2] [S11] and the modal childhood accident impairment is small. **A model treating it as a lump sum at `S` overstates the liability by about eight times.** |
| `disease_disab_severity` | 0.15 | The same for a disease impairment, above the accident figure because a disease impairment that settles at all tends to settle higher |
| `surgery_rate_cancer` | 0.85 | P(qualifying 암수술 \| 암 진단) |
| `surgery_rate_cerebral` | 0.50 | P(qualifying 뇌출혈수술 \| 뇌출혈 진단) |
| `surgery_rate_cardiac` | 0.70 | P(qualifying 급성심근경색증수술 \| 진단) |
| `liability_severity` | **₩600,000** | Mean paid on a 가족일상생활배상책임 claim, well inside the ₩100,000,000 limit and net of the ₩200,000 / ₩500,000 대물 deductibles [S5] |
| `hosp_cap_factor` | **0.92** | The share of expected 입원 days surviving the 1~180일 per-stay cap [R12] [S2] |
| `waiver_disab_share` | 0.08 | The share of 3~100% 후유장해 events reaching the 50% 이상 threshold that fires the 납입면제 [S2] |
| `payer_disab_ratio` | **0.25** | The 계약자's 50% 이상 장해 incidence as a ratio to mortality at the same age — **no Korean disability incidence table is public** |
| `leak_share` | 0.40 | The 누수사고 대물 share of the liability loss cost, being the limb whose 보장개시일 resets at each renewal [S5] [S3] |
| `void_rate_ann` | **0.012** | The annualised foetal-loss rate over the pre-birth months |
| `broad_def_factor` | 4.0 | Broad 뇌혈관질환 / 허혈성심장질환 against narrow 뇌출혈 / 급성심근경색증 [S11] [S2] [R12] |
| `net_prem_ratio` | 0.75 | 순보험료 as a share of 영업보험료, used **only** in the 표준해약공제액 formula [REG-R20] |

**The foetal-loss rate is the most exposed number in the file.** No Korean source retrieved
gives one; what the sources fix is the **mechanic** — that the contract is 무효 and the whole
premium comes back [S8 제56조] [S9] — and not the level. 1.2% a year over five months costs
the anchor cell ₩306.90 of refunded premium in total, so it is small in the cash flow and
large in principle: it is the only decrement in `krlib` that de-recognises a contract rather
than terminating it.

**No 180-day one-hospitalization memory is implemented.** No retrieved Korean child wording
states a re-admission grouping rule — this is a real difference from the Japanese third-sector
chassis, where the 180-day rule is in every 約款 — so the per-stay cap enters as a single
`hosp_cap_factor` of 0.92 rather than as a ledger. Inventing a grouping rule would be
inventing an unsourced benefit mechanic.

**The 태아 module [std] — nine limbs, two timings, and two of them day-capped.**
`neonatal_table.csv` gives each limb a frequency per birth, an amount (fixed or a ratio to the
module's own ₩10,000,000 가입금액), an expected number of units and a `timing`:

| Item | timing | freq | amount | ratio | units | expected cost |
|---|---|---|---|---|---|---|
| `birth_risk_low` (저체중아 출생) | birth | 0.0120 | — | 0.10 | 1 | ₩12,000 |
| `birth_risk_disab` (장해 출생) | birth | 0.0020 | — | 0.20 | 1 | ₩4,000 |
| `birth_risk_severe` (심한 장애 출생) | birth | 0.0006 | — | 1.00 | 1 | ₩6,000 |
| `preterm` (27주 이내 출생) | birth | 0.0025 | — | 1.00 | 1 | ₩25,000 |
| **`neonatal_cost_pp("birth")`** | | | | | | **₩47,000** |
| `incubator` (저체중아 인큐베이터 일당) | block | 0.0600 | ₩50,000 | — | 8.0 days | ₩24,000 |
| `perinatal_cash` (주산기질환 입원일당) | block | 0.1100 | ₩10,000 | — | 7.5 days | ₩8,250 |
| `congenital_diag` (선천이상 진단비) | block | 0.0200 | ₩1,000,000 | — | 1 | ₩20,000 |
| `congenital_surg` (선천이상 수술비) | block | 0.0080 | ₩1,000,000 | — | 1 | ₩8,000 |
| `neonatal_haem` (신생아 뇌출혈) | block | 0.0016 | — | 0.20 | 1 | ₩3,200 |
| **`neonatal_cost_pp("block")`** | | | | | | **₩63,450** |

The two day-capped limbs are implemented **as written**, which is why their `units` are
expected paid days after the contractual deduction and inside the cap:

    incubator benefit = 50,000 × max(0, min(days_used, 60) − 2)                      [S1]
    perinatal cash    = 10,000 × max(0, min(stay_days, 120) − 3),  stay_days ≥ 4      [S8]

**The module's cost is a length-of-stay question, not an amount question**, and the useful
datum is the supervisor's own worked claim: a birth at 32 weeks and 1.84 kg, congenital
atresia of the small intestine, enterostomy, incubator, in hospital from 2007-12-07 to
2008-05-01, total paid **₩16,836,420** of which the neonatal day benefits were ₩4,200,000 —
capped by **days**, not by amount [R3]. The `neonatal_haem` frequency carries a caveat of its
own: it is **regime-dependent rather than stationary**, because the 2013-09 supervisory
decision requiring neonatal claims to be paid on the diagnosis name rather than the KCD code
ended refusals of 뇌출혈 coded **P52** and raised frequency sharply [R5].

**Lapse [std], on a form the regulator prescribes rather than the market observes.** Three
bases ship. The base run is **`loglinear`**, the 2024-11-07 계리가정 guideline's 원칙모형: a
log-linear decay from a first-year rate to **0.1% at 납입완료**, with a post-완납 ultimate of
**0.8%** [REG-R27] [R11]:

    lapse_rate(t) = exp( ln r0 + (t / m) × ( ln r1 − ln r0 ) )     for t < m = 240
                  = r2                                             for t >= m
    lapse_rate_mth(t) = 1 − (1 − lapse_rate(t))^(1/12)                              [std]

| basis | `first_year_rate` | `completion_rate` | `ultimate_rate` | Source |
|---|---|---|---|---|
| `loglinear` | 5.0% | **0.1%** | **0.8%** | endpoints [REG-R27] [R11]; start [S1]; shape **[std]** |
| `disclosed` | 5.0% (<=10y) / 3.0% (10–15y) / 1.0% (>15y) | 1.0% | 0.5% | **[S1]** verbatim |
| `flat` | 3.0% | 3.0% | 3.0% | **[std]** comparison vector |

The 0.1% and the 0.8% are the ruling's own numbers [REG-R27]; the **5.0% starting level is
the top band of the only 적용해지율 any Korean child product publishes** [S1], so unlike every
other lapse assumption in this library it has an observed anchor. What is **[unverified]** is
the functional form: the 「IFRS17 주요 계리가정 가이드라인」 attachment was never converted
from HWP, so the values are verified from the 보도자료 and the log-linear shape is not.
Shipping `disclosed` beside `loglinear` is exactly the comparison the guideline obliges an
insurer departing from the 원칙모형 to disclose, and the two produce visibly different
contracts: model point 5 runs on `disclosed` and its undiscounted `net_cf` is −₩8,061,541
against the anchor's −₩13,085,435.

**Lapse is absorbing [std].** 부활 is available within three years even where no surrender
value has been taken [S8] [REG-R25 제27조](#krlib-reg-r25), and below 보험나이 15 there is **no cancer waiting
period to re-run** [S3] — so a reinstated child policy is very nearly the policy that lapsed,
which is a stronger statement than the chassis can make. The simplification is nonetheless
conservative on a protection product and is recorded as one.

**Expenses and commission (all levels [std]; no Korean expense or commission scale for this
product is public).** Both 상품요약서 in the set define 계약체결비용 and 계약관리비용 and then
give no number, and the 산출방법서 that holds the 예정사업비율 is a filed but undisclosed
기초서류 [REG-R2]. What is available is a statutory **ceiling** — 감독규정 [별표 14] caps the
deductible acquisition cost at the 표준해약공제액 [REG-R20], and the FSC's 2019 expense reform
states the same cap as roughly **thirteen months' premium** for a 보장성보험 [REG-R29] — and
a commission cap: first-year remuneration within the first year's expected premium, with an
obligation to offer an instalment structure paying no more than 60% of the 표준해약공제액 a
year [REG-R22 제4-32조제5항·제8항](#krlib-reg-r22) [REG-R29]. **It is the thirteen-month reading that
binds here**: the [별표 14] formula gives ₩1,575,064.09 on the anchor cell, 56.25 months of
core premium, so `surr_chg_cap_pp()` takes the lesser of the two — see *The 표준해약공제액*
below.

| Input | Value | Anchor-cell amount |
|---|---|---|
| Acquisition cost `acq_cost_ratio` | **0.9 × 표준해약공제액** | ₩327,600.0000 = **11.70 months** of core premium |
| Initial commission `comm_init_share` | **0.65 × acquisition cost** | ₩212,940.0000 |
| Non-commission acquisition expense | the remainder, at `t = 0` | ₩114,660.0000 |
| Renewal commission `comm_renewal_rate` | **3.0%** of premium, `t = 12` to `prem_end()` | ₩880.93 at `t = 12` |
| Maintenance `expense_maint_pp` | **₩400** per policy per month, inflating | ₩400.00 at `t = 0` |
| Maintenance, premium-related | **5.0%** of premium income while premiums are paid | ₩1,550.00 at `t = 0` |
| Claim handling `expense_claim_pp` | **₩30,000** per benefit event, uninflated | ₩30.17 at `t = 0` |
| Expense inflation `inflation_rate` | **2.0% p.a.**, the Bank of Korea's own target | ×**7.24** by `t = 1200` |

**Two of those deserve a sentence each.** Acquisition cost and initial commission together are
₩327,600 at `t = 0` against a ₩31,000 first-year office premium — **10.57 months of it** — and
that is why `net_cf(0)` is −₩298,646.2076 on a contract whose first-year benefit outgo is
₩141,963. And **expense inflation is not a detail on this product**: 2% a year compounds to
**7.24 over a hundred years**, per-policy maintenance runs for the whole term rather than to
납입완료, and the ₩400-a-month charge is ₩2,898 a month by the 100세 계약해당일. Maintenance
over the eighty paid-up years is the largest single expense item in the projection, which is
why it is held as its own parameter.

**No renewal commission is paid after 납입완료.** A projection that keeps charging it there is
charging commission on a premium nobody pays, and on this product that would be eighty years
of it.

---

## Cash flow components and recursions

### Notation

| Symbol | Cells | Meaning |
|---|---|---|
| `t` | — | policy month, 0-based: `t = 0, 1, …, proj_len − 1` (= `n`) |
| — | `proj_len` | the **number** of projected months, `12 × (term_age − issue_age) + 1` = 1,201 |
| `n` | `proj_len − 1` | the terminal 계약해당일 index, `12 × (term_age − issue_age)` = 1,200 |
| `m` | `prem_period_mths` | 납입기간 in months = 240; last premium at `m − 1` |
| `b` | `birth_month` | the policy month of birth = 5; 0 on a non-foetal point |
| `f` | `foetal_cover_end` | `b + 12` = 17, the end of the 태아 module's cover |
| `x` | `issue_age` | 보험나이 at the 계약일 = 0 |
| `x + ⌊t/12⌋` | `age` | attained **보험나이** in month `t` |
| `y(t)` | `age_man` | attained **만나이**; `−1` for `t < b` |
| `S_j` | `sum_assured(j)` | 보험가입금액 of cover `j` |
| `D`, `κ` | `hosp_daily`, `basis_param("hosp_cap_factor")` | 입원일당 per day; the per-stay cap factor, which is a `basis_table.csv` parameter and not a cells of its own |
| `P_core`, `P_foet` | `premium_mth`, `premium_foetal_mth` | the two premium streams |
| `P(t)` | `premium_mth_pp` | office premium due in month `t`, all streams |
| `d(t)` | `prem_discount_factor` | the 2026 저출산 discount factor; 1 in the base run |
| `q(t)`, `q_m(t)` | `mort_rate`, `mort_rate_mth` | annual / monthly mortality of the **insured** |
| `q^P(t)` | `mort_rate_payer` | annual mortality of the **계약자** |
| `v(t)` | `void_rate_mth` | monthly pre-birth 무효 rate |
| `w(t)`, `w_m(t)` | `lapse_rate`, `lapse_rate_mth` | annual / monthly lapse |
| `ω_C`, `ω_P`, `ω`, `ω_m` | `waiver_rate_child`, `_payer`, `waiver_rate`, `_mth` | the two waiver limbs and their combination |
| `i_j(t)`, `i_j,m(t)` | `inc_rate`, `inc_rate_mth` | annual / monthly incidence of cause `j` |
| `φ_j(t)` | `frac_open` | probability cover `j` is still unclaimed |
| `c_j(t)` | `cover_open` | 1 where cover `j` is on risk |
| `ρ(t)` | `reduction_factor` | 감액 factor; 1 throughout the base run |
| `e(t)` | `pols_waiver_entry` | waiver entries in month `t` |
| `l_P(t)`, `l_W(t)`, `l(t)` | `pols_pay`, `pols_waived`, `pols_if` | the two compartments and their sum |
| `A(t)` | `av_pp` | 계약자적립액 **at time `t`** (start of month `t`, before that month's premium; `t = 0` is the 계약일) |
| `CV(t)` | `cv_pp` | 해약환급금 payable **at time `t`**, same convention |
| `X(t)` | `surr_chg_pp` | unamortised 해약공제액 **at time `t`**, same convention |
| `U(t)` | `unearned_prem_pp` | 미경과보험료, half a month's premium **[std]** |
| `CF(t)` | `net_cf` | net cash flow, **income-positive** |

**Dimensional check, and it catches the commonest error in this product.** `q`, `w`, `v`, `ω`
and every `i_j` **except two** are dimensionless probabilities per year. `i_hosp_acc` and
`i_hosp_dis` are **days per policy year**, so `D × (i_hosp_acc + i_hosp_dis)/12 × κ` is
KRW per policy-month; `S_j × i_j,m` is KRW per policy-month for an event cause. `A`, `CV`,
`X`, `U`, `P` are KRW per policy; `l` is dimensionless. `i_hosp_dis(t) = 2.40` at 만나이 0,
so `1 − (1 − i)^(1/12)` is **not a real number** — the model divides the two day counts by
twelve and never routes them through `inc_rate_mth`.

### The pre-birth period

For `t < b` the insured does not exist. `born(t)` is false, `y(t) = −1`, `q(t) = 0`, every
`i_j(t) = 0`, `c_j(t) = 0` and every benefit written on the child's own life is identically
zero. What is in force is the premium on **all three streams**, the void decrement, and — at
`t = b` and not before — the 태아보장기간 limbs, which pay in respect of events of the
pregnancy and the delivery **from the date of birth** [S8 제59조]. The 계약자's waiver limb
also runs from `t = 0`: the policyholder is an insured of the contract in his own right
[S10 제3조], so his death is a contractual event from the 계약일 whether or not the child has
been born.

    v(t) = 1 − (1 − void_rate_ann)^(1/12)      for foetal and t < b, else 0

`check_cover_at_birth()` asserts that the sum of `claims(t, k)` over `k ∈ {DISABILITY,
DIAGNOSIS, SURGERY, HOSPITAL, EVENT, LIABILITY, DEATH}` is zero for every `t < b` — the loop
runs to `t = b`, where the residual is identically zero because the child is born and the
covers are properly open. The 태아
module is deliberately **not** in that sum — it is the one thing that may pay in respect of an
event before the insured legally exists — and is tested separately by
`check_neonatal_term()`.

### The two premium waivers

    ω_C(t) = 0                                                    if t > m − 1, or not born(t),
                                                                  or (foetal and t < f)
           = i_cancer(t) + i_cerebral(t) + i_cardiac(t)
             + waiver_disab_share × ( i_disability(t) + i_disease_disab(t) )      otherwise

    ω_P(t) = 0                                                    if t > m − 1
           = q^P(t) × ( 1 + payer_disab_ratio )                                   otherwise

    ω(t)   = 1 − ( 1 − ω_C(t) ) ( 1 − ω_P(t) )        ω_m(t) = 1 − (1 − ω(t))^(1/12)

The child's limb stands for the three sourced trigger limbs of [S2] — the **7대질병**
diagnosis limb (암 유사암 제외, 뇌혈관질환, 중대한재생불량성빈혈, 양성뇌종양 and three
심혈관질환 limbs), the **50% 이상 후유장해** limb, and the **중대한특정상해수술** limb — as
`cancer + cerebral + cardiac + 0.08 × (disability + disease_disab)` **[std]**. The 계약자's
limb is that life's own mortality grossed up by 25% for the 50% 이상 장해 limb of
[S10 제22조제1항] **[std]**, no Korean disability incidence table being public. The two are
treated as **independent**, which is a [std] simplification: nothing in the sources relates
them and nothing the model can see could.

**The P코드 carve-out is implemented rather than averaged away**, and it is the sharpest
interaction in the product. 「출생전후기에 기원한 특정 병태(P코드) 진단시 납입면제를 적용하지
않음」 [S2]. The 태아 module's whole reason for existing is the perinatal chapter of the KCD,
so on a 태아 contract the child's limb **does not operate at all over the 1년만기 신생아
block**: the covers most likely to pay in the first year of a foetal contract are precisely
the ones that cannot stop the premium. It is coherent — a neonatal condition is not a lifelong
impairment — and it is a **[std]** implementation of a sourced carve-out rather than an exact
one. On the anchor cell it is visible as a step: `ω(16) = 0.0009071625`, the 계약자's limb
alone; `ω(17) = 0.0011521489`, once the child's limb switches on.

**Both limbs stop at 납입완료.** A waiver is a waiver of premium, and after `t = m − 1` there
is no premium to waive: `ω(240) = 0`. A model that keeps the waiver running for the eighty
paid-up years is transferring policies into a compartment that no longer differs from the one
they came from — except that it is not exposed to lapse, which silently suppresses eighty
years of lapses.

### The in-force recursion, in two compartments

Within month `t` the order is **void, then the waiver, then mortality, then lapse**
**[std order]**. For `0 <= t < n`, with `l_P(0) = 1` and `l_W(0) = 0`:

    e(t)       = l_P(t) ( 1 − v(t) ) ω_m(t)

    l_P(t+1)   = ( l_P(t) ( 1 − v(t) ) − e(t) ) ( 1 − q_m(t) ) ( 1 − w_m(t) )
    l_W(t+1)   = ( l_W(t) ( 1 − v(t) ) + e(t) ) ( 1 − q_m(t) )
    l(t)       = l_P(t) + l_W(t)

and the four exits:

    pols_void(t)     = l(t) v(t)                                    [zero from birth]
    pols_death(t)    = ( l(t) − pols_void(t) ) q_m(t)               [zero before birth]
    pols_lapse(t)    = ( l_P(t) ( 1 − v(t) ) − e(t) ) ( 1 − q_m(t) ) w_m(t)
    pols_maturity(t) = l(t)  if t = n, else 0

Four properties follow and each has a check. The roll-forward
`l(t) − l(t+1) = pols_void + pols_death + pols_lapse + pols_maturity` closes **exactly**, to
`roll_fwd_tol = 1e-10`, in every month (`check_pols_roll_fwd`). The compartments sum to the
block (`check_waiver_split`). The four decrements sum over the whole projection to
`pols_if_init()` — on the anchor cell **0.0049757330 voids, 0.4688979472 deaths, 0.5103916457
lapses and 0.0157346742 maturities**, totalling exactly 1 (`check_exit_total`). And every
decrement is nil at `t = n`, with `l(n+1) = 0`.

**The void applies to the whole block and mortality to the survivors of it**, in that order,
because a contract that turns out never to have been valid cannot also have produced a death
of an insured who was never born. **Waived policies carry mortality but not lapse.**

### Benefit components, per policy in force

    cover_open(t, j)  = 0   if not born(t), or t >= n,
                            or ( j ∈ {cancer, minor_cancer} and t < W )
                      = 1   otherwise
    reduction_factor  = 0.5 if t < G, else 1        [G = 0 on a foetal contract, always]

    benefit_DISABILITY(t) = S_dis · 0.12 · i_disability,m(t)
                          + S_ddis · 0.15 · i_disease_disab,m(t)

    benefit_DIAGNOSIS(t)  = ρ(t) · Σ_{j∈{cancer, minor_cancer, cerebral, cardiac}}
                                     S_j · i_j,m(t) · φ_j(t) · c_j(t)

    benefit_SURGERY(t)    = S_surg · Σ_{j∈{cancer, cerebral, cardiac}}
                                     s_j · i_j,m(t) · φ_j(t) · c_j(t)

    benefit_HOSPITAL(t)   = D · ( i_hosp_acc(t) + i_hosp_dis(t) ) / 12 · κ

    benefit_EVENT(t)      = S_frac · i_fracture,m(t) + S_burn · i_burn,m(t)

    benefit_LIABILITY(t)  = i_liability,m(t) · σ_L · ( S_liab / 100,000,000 ) · g(t)
        with g(t) = 1 − leak_share   if t mod 36 < 3,   else 1

    benefit_NEONATAL(t)   = neonatal_birth + neonatal_block / 12     if t = b
                          = neonatal_block / 12                      if b < t < f
                          = 0                                        otherwise

    φ_j(t+1) = φ_j(t) ( 1 − i_j,m(t) ),      φ_j(0) = 1

and `claims(t, k) = benefit_k(t) × l(t)` for each of the seven morbidity kinds.

**The 기본계약 is a percentage scale, not a lump sum.** 보험가입금액 × 장해지급률 on a
continuous 3~100% band, payable more than once with the percentages accumulating
[R12] [S1] [S2] [S11]. That is why `benefit_DISABILITY` carries a severity of 0.12 and no
`frac_open` ledger, and why it is the one benefit whose cost a naive implementation
**overstates by about eight times**.

**The liability rider's renewal is the one place the 갱신형 mechanic bites.** The 누수사고
limb's 90-day 보장개시일 runs from the 계약일 and **resets to the renewal date at each
renewal** of the 3년만기 block [S5] [S3], so 40% of the loss cost is off for the first three
months of every 36-month cycle. On the anchor cell that is `t ∈ {0,1,2, 36,37,38, 72,73,74,
…}` — and at `t = 0` to `t = 4` it is invisible, because the child is not yet born and the
whole rider is off.

**The 태아 module has two terms, and they are not the same term.** The 태아보장기간 runs
계약체결일 ~ 출생시점 [S2] and its limbs pay **at birth, all at once**: ₩47,000 per birth.
The 신생아 block is a **1년만기 전기납** term from birth [S2] [S5] [R5] and its ₩63,450 is
spread evenly over twelve months at ₩5,287.50 each. So `t = b` carries both — ₩52,287.50 per
policy in force — and `t = b+1 … b+11` carry only the block. `check_neonatal_term()` asserts
the module pays inside `b <= t < f` and nowhere else, and pays nothing at all on a contract
that is not a 태아가입.

### The account, the surrender charge and the surrender value

    cum_prem_pp(t)   = P_core × min(t, m)
    refund_ratio(t)  = refund_build( t/12 ) × refund_taper( t/n )
    cv_std_pp(t)     = refund_ratio(t) × cum_prem_pp(t)
    X(t)             = surr_chg_cap_pp × max( 0, 1 − t / surr_chg_period )          [std]
    A(t)             = min( cv_std_pp(t) + X(t),
                            max( cv_std_pp(t), net_prem_ratio × cum_prem_pp(t) ) )  [std]
    U(t)             = 0.5 × P(t)                                                   [std]

    CV(t) = max(0, cv_std_pp(t))                                    cv_form = std
          = 0                                    for t < m         cv_form = susp
          = max(0, k × cv_std_pp(t))             for t >= m        cv_form = susp
          = max(0, cv_grade_ratio(t) × cv_std_pp(t))               cv_form = graded

**The 환급률 progression is published and the model reproduces it exactly.** `refund_build` is
a current 상품요약서's grid on a named specimen contract — 0.0% at 1 year, 45.6% at 3, 62.5%
at 5, 73.7% at 10, 78.3% at 15, 82.6% at 20, 101.2% at 30, 122.5% at 40, 144.1% at 50 and
158.9% at 60, at 공시이율 1.7% (2026-07), 평균공시이율 2.5% and 최저보증이율 0.3% [S2] —
linearly interpolated in duration and held flat beyond 60 years. `refund_taper` is the
terminal collapse, 1.0 until 85% of the term has run and then down to zero at 만기, indexed on
the **fraction of the term run off** rather than on a duration, and calibrated so that a
100세만기 contract reproduces the published **16.0% at 95 years** [S2]. Splitting the
progression in two is what lets one shipped grid serve a 30세만기, a 100세만기 and a 110세만기
contract without re-basing the published figures. `check_refund_grid()` asserts every
published node the contract reaches.

**The 계약자적립액 is recovered from the published surrender value, and the first two years
are where the [std] enters.** What the 상품요약서 publishes is 「순보험료식 계약자적립액에서
해약공제액을 공제한 금액」 [S2] — already net of the charge and floored at zero — so the
account can be recovered by adding the unamortised charge back **only where the floor is not
binding**. Where it is, the identity gives no more than `0 <= A <= X`, and the account is
capped instead at the cumulative **net** premium, `0.75 × cum_prem_pp(t)`, which is the most a
순보험료식 reserve can have accumulated before any interest or mortality. **The account
therefore starts at nil, as it must, rather than at the surrender charge.**
`check_av_bounds()` asserts `CV(t) <= A(t) <= cv_std_pp(t) + X(t)` and `A(t) >= 0` in every
month. The **공시이율 reset is not implemented**; it is carried by reference to
`WholeLife_KR_S`.

**The 표준해약공제액 (*pyojun haeyak gongjeaek*, the statutory cap on the surrender charge),
and how a product with no death benefit acquires a face amount.**
감독규정 [별표 14] states

    표준해약공제액 = 연납순보험료 × 5% × 해약공제계수 + 보험가입금액 × 10/1000     [REG-R20]

with 해약공제계수 = 「보험기간(최대 20년)」 = **20** and note 3 requiring the 연납순보험료 to
be recomputed on a 20년납 footing where the term is 20 years or more. The second term needs a
보험가입금액 this contract does not have — [별표 15] 제3호 covers only 일반사망을 보장하는
보장성보험, so it falls into **제9호**: 보험가입금액 = (위험보험료 ÷ 정기보험의 위험보험료) ×
정기보험의 보험가입금액, computed at the **기준연령 요건, 남자 만 40세, 전기납, 월납**
[REG-R21] [REG-R9 제1-2조제2호](#krlib-reg-r9). A term policy's risk premium per unit of face is its
mortality rate, so

    sa_notional_pp = risk_prem_ann_pp / q(40, M)
                   = 145,537.04939942522 / 0.0011 = 132,306,408.54493201

    formula limb    = 0.05 × 252,000 × 20 + 0.01 × 132,306,408.54493201
                    = 252,000 + 1,323,064.08544932  = 1,575,064.08544932

    surr_chg_cap_pp = min( 1,575,064.08544932, 13 × 28,000 ) = 364,000.0

**The 10/1000 of the schedule is one per cent, not one per mille, and at that rate the formula
limb does not bind on this product — which is itself a finding.** [별표 14] and the FSC's 2019
expense reform are two readings of **one** ceiling, the reform stating it as **보장성보험
13배** of the monthly premium [REG-R29], and here they are 4.33 times apart: ₩1,575,064.09
against ₩364,000.00, **56.25 months** of core premium against thirteen. The gap is structural.
제9호 divides this contract's whole first-year risk premium by a 40-year-old's mortality rate,
and a bundled child stack has a large risk premium and a very small death rate, so the notional
보험가입금액 it produces is ₩132.3 million against the ₩100 million of accidental-disability
cover actually written. `surr_chg_cap_pp()` therefore takes the **lesser** of the two, which is
the treatment `Cancer_KR_S` states for the same mechanic, and **the thirteen-month limb binds
on all ten shipped model points**: the formula limb runs from ₩245,582 on point 9 to
₩1,654,269 on point 6 and clears thirteen months' premium on every one of them.
`acq_cost_months()` publishes the ratio actually reached — **11.70**, or 0.9 × 13 — so the two
readings can be compared rather than asserted equal, and `check_acq_cost_cap()` asserts the
acquisition cost stays inside the cap.

**Evaluating 제9호 at the 기준연령 rather than at a child age is a substantive finding too, not
a convenience.** At 만나이 0 the mortality rate is 0.0025 and at 5 it is 0.00012; using the
latter would put the notional 보험가입금액 at ₩1,212,808,745 and the formula limb at
₩12,380,087.45 — **442.1 months of premium**, which is absurd on its face. At 남자 만 40세 it
lands at ₩1,575,064.09, or 56.25 months. The reference age therefore decides the notional
amount by a factor of nine even though, on this product, the binding limb is the other one.

### Processing order

For `t = 0, 1, …, n`:

1. **Start of month.** `premiums(t) = P(t) · d(t) · l_P(t)` — carried on the **paying
   compartment alone**, a waived policy paying nothing while its premiums are *deemed paid*
   for every benefit purpose. Maintenance expense `400 · (1.02)^(t/12) · l(t)` plus
   `0.05 · premiums(t)`. Renewal commission `0.03 · premiums(t)` for `12 <= t <= m − 1`. At
   `t = 0` additionally the acquisition expense `(acq_cost_pp − comm_init_pp) · l(0)` and the
   initial commission `comm_init_pp · l(0)`.
2. **Look up both ages.** `age(t)` decides the premium and the 보험나이 15 thresholds;
   `age_man(t)` decides every rate. Hence `q(t)`, `q^P(t)`, `w(t)`, `v(t)`, every `i_j(t)`,
   and hence `ω_C`, `ω_P`, `ω`.
3. **End of month — morbidity benefits**, each `benefit_k(t) × l(t)`, with the `φ_j` ledgers
   read at their start-of-month values and the 태아 module on its own two terms.
4. **End of month — the four exit payments.**

       claims_death(t)    = ( A(t) + U(t) ) × pols_death(t)
       claims_lapse(t)    = ( CV(t) + U(t) ) × pols_lapse(t)
       claims_maturity(t) = A(t) × pols_maturity(t)
       claims_void(t)     = ( cum_prem_pp(t) + prem_foetal_paid_pp(t) ) × pols_void(t)

   and the claim-handling expense
   `30,000 × ( claim_count_pp(t) · l(t) + pols_death(t) + pols_void(t) )`.
5. **End of month — decrements**, in the order **void, waiver, mortality, lapse**, per the
   recursion above.
6. **Ledger update.** `φ_j(t+1) = φ_j(t)(1 − i_j,m(t))` for each of the four 최초 1회한
   diagnosis covers.

Everything except the exit payments is nil at `t = n`: no premium, no morbidity benefit, no
maintenance expense, no commission. `claims_maturity(n)` is the residual 계약자적립액, which
on the shipped progression is **zero**.

### Net cash flow

    CF(t) = premiums(t)
          − claims_disability(t) − claims_diagnosis(t) − claims_surgery(t)
          − claims_hospital(t)   − claims_event(t)     − claims_liability(t)
          − claims_neonatal(t)   − claims_death(t)     − claims_lapse(t)
          − claims_maturity(t)   − claims_void(t)
          − claim_expenses(t) − expenses(t) − commissions(t)

`net_cf` is **income-positive**, the library-wide sign and these notes' own, so there is no
outgo-positive `liability_cf` companion. `expenses` is acquisition and maintenance only; the
claim-handling expense is a line of its own, with its own cells, its own subtraction and its
own column, which keeps the acquisition strain and the morbidity-driven handling cost from
moving together in one figure. **No bare `claims` subtotal is published** beside its own
parts: `result_cf()` carries the eleven kinds and `check_net_cf()` asserts that they rebuild
`net_cf(t)` in every month, so a twelfth kind added to `claims()` and left out of the
statement shows up rather than silently vanishing.

### Optional modules (all off in the base run)

| Module | Switch | Base | What turns on |
|---|---|---|---|
| 해약환급금 미지급형 | `cv_form = "susp"`, `cv_floor_ratio = 0.5` | `std` | `CV(t) = 0` for the whole 납입기간 and `0.5 × cv_std_pp` after it — **a cliff, not a curve** [S2]. Model point 4 |
| 미지급형Ⅲ, graded | `cv_form = "graded"` | `std` | the published ten-step ladder: 5% from M to M+2 years rising 5 points every two years to 50% from M+18 [S1]. Model point 5 |
| 면책기간 | `waiting_mths = 3` | 0 | the two cancer limbs closed for three months; only reachable at 보험나이 >= 15. Model points 7 and 8 |
| 감액기간 | `reduction_mths = 12` | 0 | every diagnosis benefit at 50% for a year; **disapplied unconditionally on a 태아 contract** [R2]. Model point 7 |
| Broad adult-disease definitions | `broad_def = 1` | 0 | 뇌혈관질환 and 허혈성심장질환 in place of 뇌출혈 and 급성심근경색증, at `broad_def_factor = 4.0`. Model point 8 |
| The 계약자 waiver | `waiver_payer = 0` | **on** | removes the second decrement life entirely. Model points 2, 3, 7, 8, 9, 10 |
| The child waiver | `waiver_child = 0` | **on** | model point 8 |
| 태아가입 | `foetal = 0` | **on** | removes the void decrement, the 태아 module, the second premium stream and the age offset in one switch. Model points 2, 3, 5, 7, 8, 9 |
| The 2026 저출산 discount | `prem_discount_rate`, `_mths` | 0 / 0 | a 1%–5% haircut on the office premium for twelve months [R6]. Model point 10 at 5% |
| Lapse basis | `lapse_basis` | `loglinear` | `disclosed` (point 5), `flat` (point 8) |
| Mortality best-estimate scalar | `mort_be_factor` | 1.0 | 1.10 on point 10 |

**Deliberately not modelled, and stated as such rather than omitted silently.** The
임신·출산질환 module written on the **mother** — 모성사망, 임신·출산질환 입원일당 and 수술,
분만전후출혈, 유산 진단·수술·입원, 출산전특정태아이상진단, all running 계약일 ~ 분만 후 42일
at mother's issue ages 20~47세 [S2] [S5]. The **부양자 benefit stack** on the parent's own
life, of which one death rider is **compulsory on a 태아 contract** [S5] [S11] — the model
carries the parent as a *decrement* and not as a benefit, and the two are not
interchangeable. **다태아 plans**, priced at roughly 2× for twins and 3× for triplets [R5]
[R4]. The named-cancer riders (다발성소아암, 16대특정암, 5대고액치료비암, 전이암, 재진단암).
The 후유장해 **생활지원금** annuity forms [S11]. **일반상해사망 from 만 15세** [S1] [S4].
The 공시이율 reset. And **실손 riders of any kind**, statutorily unattachable since April 2018
[R9] [R10]. **No exclusion decrement is modelled**: the general 보험금을 지급하지 않는 사유
articles were never read in full, so no lapse or claim leakage for them is carried.

---

## Policyholder behavior modeling

- **Lapse is real, immediate and absorbing.** A missed premium opens a 납입최고 of at least 14
  days [REG-R25 제26조](#krlib-reg-r25), operated in practice as a calendar-month window running 「납입기일
  다음날부터 납입기일이 속하는 달의 다음달 마지막 날까지」, so a premium due on 15 September
  is in grace to 31 October and the contract lapses on 1 November [S8]. That is why the
  monthly grid is the right one for it. The base run applies lapse at the end of the month in
  which the premium is missed and does not model the grace lag — a one-month timing effect on
  an undiscounted projection.
- **부활 is not modelled, and on this product the simplification is a real one.** Reinstatement
  is available within **three years** of lapse where no surrender value has been taken
  [S8] [REG-R25 제27조](#krlib-reg-r25), subject to fresh underwriting, and waiting periods re-run from the
  부활일 [S3] — but below 보험나이 15 **there is no cancer waiting period to re-run** [S3], so
  a reinstated child policy is very nearly the policy that lapsed. On the chassis the same
  simplification is conservative because the 90 days re-runs; here it is conservative only
  because the projection loses the premium. Treating lapse as absorbing is **[std]** and the
  direction is stated: it **understates** persistency.
- **On the 표준형 there is a surrender value and therefore a real economic surrender
  decision.** `CV(t)` reaches ₩1,050,000 at `t = 60` and crosses premiums paid at
  **`t = 353`**, so a policyholder in the second decade has something to take. On the
  **미지급형** there is nothing at all through the whole 납입기간, no 보험계약대출 and no
  automatic premium loan to break the fall [REG-R28] — which is exactly why the lapse
  assumption over that
  period is worth so much CSM and why it became a supervisory matter [R11] [REG-R27]. The two
  forms carry the same `lapse_rate` in the shipped model; **no dynamic lapse term is modelled**
  and that is a named gap, not an oversight.
- **The waived cohort cannot lapse.** See *State variables*. On the anchor cell
  `pols_waived(240)` is **0.0334654434**, 4.36% of the in-force block at 납입완료, and it
  carries mortality for the remaining eighty years without ever being exposed to a lapse rate
  again.
- **Elections are not behaviour.** `cv_form`, `term_age`, `prem_period_years`, the rider set
  and the 태아 module are elected at issue and cannot be changed. They are model-point
  attributes; a code path that varies them over `t` models a contract term that does not
  exist. The one genuine mid-term option is a **change of 계약자**, which would change the
  second decrement life; no retrieved wording states how the waiver responds, so the composite
  holds the 계약자 fixed and marks the point **[unverified]**.
- **청약철회 is out of scope**: 15 days from receipt of the policy and not more than 30 from
  application [S8] [REG-R51], a pre-inception decrement needing a new-business funnel this
  library does not have.
- **The 2026 저출산 discount is a behaviour the supervisor created.** From 2026-04-01 every
  insurer operates a **1%–5% discount for one year** where the policyholder or spouse is
  within a year of a birth, on 육아휴직, or on 육아기 근로시간 단축 [R6]; on the birth limb it
  applies to a **sibling's** policy, not the newborn's own. 어린이보험 is expressly
  **excluded** from the companion 보험료 납입유예 scheme [R6], so there is no deferral state
  to model — only a premium haircut, off in the base run. Whether it bites on the 영업보험료
  or the 보장보험료 is not stated and is **[unverified]**; the model applies it to the whole
  office premium.

---

## Worked example

**Anchor cell (`point_id = 1`, `CH-KR-0001`).** A **태아가입** contract: 계약나이 **0** at
the 계약일, priced **male** because the sex is unknown at issue [R3] [S8], **birth at policy
month 5**, 보험기간 to the **100세 계약해당일** (`n = 1200`), **20년납** (`m = 240`), 월납,
**표준형**, with **both** premium waivers on and the 계약자 male 만 33. 기본계약 상해후유장해
₩100,000,000; the [R12] rider set at 질병후유장해 ₩10,000,000, 암진단비(유사암 제외)
₩10,000,000, 유사암진단비 ₩2,000,000, 뇌출혈진단비 ₩10,000,000, 급성심근경색증진단비
₩10,000,000, 수술비 ₩5,000,000 each on the three named diseases, 상해·질병 입원일당 ₩40,000
per day, 골절진단비 ₩400,000, 화상진단비 ₩200,000, 가족일상생활배상책임 ₩100,000,000; 태아
module 가입금액 ₩10,000,000 running to `t = 17`. Office premium **₩31,000 a month to `t = 16`
and ₩28,000 from `t = 17` to `t = 239`**. `waiting_mths = 0`, `reduction_mths = 0`,
`broad_def = 0`, `prem_discount_rate = 0`, `lapse_basis = loglinear`, `mort_be_factor = 1.0`.

**Every assumption value the first eighteen months use, and its tag.**

| Quantity | Value | Tag |
|---|---|---|
| `void_rate_ann` | 0.012 | **[std]** — no Korean foetal-loss rate was retrieved |
| `v(t)`, `t < 5` | `1 − (1 − 0.012)^(1/12)` = **0.0010055425391276573** | derived |
| `q(t)`, `t < 5` | **0** — a 태아 has no mortality in this contract [R3] | derived |
| `q(t)`, `t = 5…16` (만나이 0) | **0.0025**; `q_m` = 0.00020857243058891584 | **[std]** [REG-R38] [REG-R39] |
| `q(t)`, `t = 17…` (만나이 1) | **0.00025**; `q_m` = 0.00002083572086741814 | **[std]** |
| `q^P(0)` (계약자, 만나이 33) | **0.00067713** | **[std]** |
| `q^P(12…)` (만나이 34) | 0.00072573 | **[std]** |
| `ω_P(t)`, `t = 0…11` | `0.00067713 × 1.25` = **0.0008464125**; `ω_m` = 0.00007056175284536614 | **[std]** `payer_disab_ratio = 0.25` |
| `ω_C(t)`, `t < 17` | **0** — the P코드 carve-out over the 신생아 block [S2] | **[std]** |
| `ω_C(17)` | `0.00015 + 0.000012 + 0.000001 + 0.08 × (0.00012761 + 0.0009)` = **0.0002452088** | **[std]** |
| `w(0)` | **0.05**; `w_m(0)` = 0.004265318777560645 | [S1]; [REG-R27] |
| `w(t)` | `exp( ln 0.05 + (t/240)(ln 0.001 − ln 0.05) )` | shape **[std]** |
| `i_disability` at 만나이 0 / 1 | 0.000100265 / 0.00012761 | **[std]**, shaped on the 만나이 5 anchor |
| `i_disability` at 만나이 5, 남자 | **0.0001823** | **[S1]** — the only published rate |
| `i_disease_disab` at 만나이 0 / 1 | 0.0026 / 0.0009 | **[std]** |
| `i_cancer` at 만나이 0 / 1 | 0.00018 / 0.00015 | **[std]** [REG-R40] [REG-R61] |
| `i_minor_cancer` at 만나이 0 / 1 | 0.00003 / 0.000025 | **[std]** |
| `i_cerebral` at 만나이 0 / 1 | 0.00004 / 0.000012 | **[std]** |
| `i_cardiac` at 만나이 0 / 1 | 0.000002 / 0.000001 | **[std]** |
| `i_fracture` at 만나이 0 / 1 | 0.004 / 0.009 | **[std]** |
| `i_burn` at 만나이 0 / 1 | 0.006 / 0.005 | **[std]** |
| `i_hosp_acc` at 만나이 0 / 1 | **0.10 / 0.13 days a year** | **[std]** [REG-R41] |
| `i_hosp_dis` at 만나이 0 / 1 | **2.40 / 1.10 days a year** | **[std]** [REG-R41] |
| `i_liability` at 만나이 0 / 1 | 0.004 / 0.006 claims a year | **[std]** |
| `disab_severity` / `disease_disab_severity` | 0.12 / 0.15 | **[std]** |
| `surgery_rate_cancer / _cerebral / _cardiac` | 0.85 / 0.50 / 0.70 | **[std]** |
| `hosp_cap_factor` (κ) | 0.92 | **[std]** [R12] [S2] |
| `liability_severity` (σ_L) | ₩600,000 | **[std]** [S5] |
| `leak_share` | 0.40 | **[std]** [S5] [S3] |
| `neonatal_cost_pp("birth")` / `("block")` | ₩47,000 / ₩63,450 | **[std]** [S1] [S2] [S8] |
| `expense_maint_pp` / `_prem_rate` / `inflation_rate` | ₩400 / 5% / 2% | **[std]** |
| `expense_claim_pp` | ₩30,000 | **[std]** |
| `acq_cost_pp` / `comm_init_pp` / `comm_renewal_rate` | ₩327,600.0000 / ₩212,940.0000 / 3% | **[std]**, capped by [REG-R20] [REG-R29] |
| `prem_int_rate` (diagnostics only) | 2.75% | **[std]**, observed 2.50%–3.00% [S11] |

### The first eighteen policy months

`result_cf()`, rows `t = 0` to `t = 17`, at the precision the model produces. `pols_if` is the
**start-of-month** count and is the weight on every cash flow of the same row.

| `t` | `pols_if` | `premiums` | `claims_disability` | `claims_diagnosis` | `claims_surgery` | `claims_hospital` | `claims_event` | `claims_liability` | `claims_neonatal` |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1.0000000000 | 31,000.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 1 | 0.9947337283 | 30,834.5604 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 2 | 0.9895656205 | 30,672.1777 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 3 | 0.9844932382 | 30,512.7761 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 4 | 0.9795142152 | 30,356.2821 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 5 | 0.9746262555 | 30,202.6242 | 414.8570 | 185.1917 | 70.8281 | 7,472.1346 | 227.9207 | 195.2835 | 50,960.7703 |
| 6 | 0.9706008315 | 30,075.7076 | 413.1436 | 184.4245 | 70.5346 | 7,441.2730 | 226.9793 | 194.4770 | 5,132.0519 |
| 7 | 0.9666551736 | 29,951.2731 | 411.4641 | 183.6725 | 70.2469 | 7,411.0230 | 226.0566 | 193.6864 | 5,111.1892 |
| 8 | 0.9627873748 | 29,829.2615 | 409.8177 | 182.9353 | 69.9649 | 7,381.3699 | 225.1521 | 192.9114 | 5,090.7382 |
| 9 | 0.9589955828 | 29,709.6152 | 408.2037 | 182.2126 | 69.6884 | 7,352.2995 | 224.2654 | 192.1516 | 5,070.6891 |
| 10 | 0.9552779980 | 29,592.2781 | 406.6213 | 181.5040 | 69.4173 | 7,323.7980 | 223.3960 | 191.4068 | 5,051.0324 |
| 11 | 0.9516328712 | 29,477.1960 | 405.0697 | 180.8091 | 69.1515 | 7,295.8520 | 222.5436 | 190.6764 | 5,031.7588 |
| 12 | 0.9480585027 | 29,364.3159 | 403.5483 | 180.1277 | 68.8909 | 7,268.4485 | 221.7077 | 189.9602 | 5,012.8593 |
| 13 | 0.9445532569 | 29,253.4383 | 402.0562 | 179.4595 | 68.6352 | 7,241.5750 | 220.8880 | 189.2579 | 4,994.3253 |
| 14 | 0.9411155266 | 29,144.6625 | 400.5929 | 178.8041 | 68.3845 | 7,215.2190 | 220.0841 | 188.5691 | 4,976.1483 |
| 15 | 0.9377437493 | 29,037.9400 | 399.1577 | 178.1613 | 68.1386 | 7,189.3687 | 219.2956 | 187.8935 | 4,958.3201 |
| 16 | 0.9344364051 | 28,933.2234 | 397.7499 | 177.5307 | 67.8973 | 7,164.0124 | 218.5221 | 187.2308 | 4,940.8325 |
| 17 | 0.9311920157 | 26,040.4216 | 223.6387 | 130.3535 | 52.0636 | 3,512.4563 | 358.2944 | 280.1288 | 0.0000 |

| `t` | `claims_death` | `claims_lapse` | `claims_void` | `claim_expenses` | `expenses` | `commissions` | `net_cf` |
|---|---|---|---|---|---|---|---|
| 0 | 0.0000 | 66.0413 | 0.0000 | 30.1663 | 116,610.0000 | 212,940.0000 | -298,646.2076 |
| 1 | 0.0000 | 64.6018 | 31.0077 | 30.0074 | 1,940.2787 | 0.0000 | 28,768.6648 |
| 2 | 0.0000 | 63.1986 | 61.6931 | 29.8515 | 1,930.7437 | 0.0000 | 28,586.6907 |
| 3 | 0.0000 | 61.8306 | 92.0653 | 29.6985 | 1,921.3905 | 0.0000 | 28,407.7911 |
| 4 | 0.0000 | 60.4968 | 122.1330 | 29.5483 | 1,912.2146 | 0.0000 | 28,231.8894 |
| 5 | 24.4953 | 59.2432 | 0.0000 | 47.4875 | 1,903.2117 | 0.0000 | -31,358.7996 |
| 6 | 28.6453 | 58.0199 | 0.0000 | 47.2914 | 1,895.8889 | 0.0000 | 14,382.9781 |
| 7 | 32.7629 | 56.8258 | 0.0000 | 47.0991 | 1,888.7182 | 0.0000 | 14,318.5284 |
| 8 | 36.8488 | 55.6602 | 0.0000 | 46.9107 | 1,881.6959 | 0.0000 | 14,255.2563 |
| 9 | 40.9041 | 54.5223 | 0.0000 | 46.7259 | 1,874.8187 | 0.0000 | 14,193.1339 |
| 10 | 44.9297 | 53.4112 | 0.0000 | 46.5448 | 1,868.0831 | 0.0000 | 14,132.1337 |
| 11 | 48.9264 | 52.3262 | 0.0000 | 46.3671 | 1,861.4858 | 0.0000 | 14,072.2293 |
| 12 | 52.8951 | 51.2664 | 0.0000 | 46.1930 | 1,855.0237 | 880.9295 | 13,132.4657 |
| 13 | 56.8367 | 72.6440 | 0.0000 | 46.0222 | 1,848.6861 | 877.6031 | 13,055.4490 |
| 14 | 60.7520 | 96.5221 | 0.0000 | 45.8547 | 1,842.4776 | 874.3399 | 12,976.9142 |
| 15 | 64.6417 | 122.7277 | 0.0000 | 45.6904 | 1,836.3953 | 871.1382 | 12,897.0114 |
| 16 | 67.0866 | 151.0962 | 0.0000 | 45.5292 | 1,830.4361 | 867.9967 | 12,817.3027 |
| 17 | 6.7821 | 177.0176 | 0.0000 | 50.1247 | 1,685.0952 | 781.2126 | 18,783.2542 |

`claims_maturity` is 0.0000 in every row above and in every row of the projection.

The same months in `result_pols()`, which is where the two ages, the two compartments and the
void decrement can be read side by side:

| `t` | `pols_pay` | `pols_waived` | `pols_void` | `pols_death` | `pols_lapse` | `age` | `age_man` | `mort_rate` | `lapse_rate` | `waiver_rate` |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1.0000000000 | 0.0000000000 | 0.0010055425 | 0.0000000000 | 0.0042607292 | 0 | **−1** | 0.00000000 | 0.0500000000 | 0.0008464125 |
| 1 | 0.9946632375 | 0.0000704908 | 0.0010002471 | 0.0000000000 | 0.0041678607 | 0 | −1 | 0.00000000 | 0.0491916016 | 0.0008464125 |
| 2 | 0.9894250860 | 0.0001405345 | 0.0009950503 | 0.0000000000 | 0.0040773320 | 0 | −1 | 0.00000000 | 0.0483962733 | 0.0008464125 |
| 3 | 0.9842830996 | 0.0002101386 | 0.0009899498 | 0.0000000000 | 0.0039890731 | 0 | −1 | 0.00000000 | 0.0476138039 | 0.0008464125 |
| 4 | 0.9792349051 | 0.0002793102 | 0.0009849432 | 0.0000000000 | 0.0039030165 | 0 | −1 | 0.00000000 | 0.0468439855 | 0.0008464125 |
| 5 | 0.9742781992 | 0.0003480564 | 0.0000000000 | 0.0002032802 | 0.0038221439 | 0 | **0** | 0.00250000 | 0.0460866134 | 0.0008464125 |
| 6 | 0.9701841153 | 0.0004167162 | 0.0000000000 | 0.0002024406 | 0.0037432174 | 0 | 0 | 0.00250000 | 0.0453414865 | 0.0008464125 |
| 7 | 0.9661701006 | 0.0004850729 | 0.0000000000 | 0.0002016176 | 0.0036661811 | 0 | 0 | 0.00250000 | 0.0446084068 | 0.0008464125 |
| 8 | 0.9622342426 | 0.0005531322 | 0.0000000000 | 0.0002008109 | 0.0035909810 | 0 | 0 | 0.00250000 | 0.0438871795 | 0.0008464125 |
| 9 | 0.9583746833 | 0.0006208996 | 0.0000000000 | 0.0002000200 | 0.0035175649 | 0 | 0 | 0.00250000 | 0.0431776130 | 0.0008464125 |
| 10 | 0.9545896174 | 0.0006883806 | 0.0000000000 | 0.0001992447 | 0.0034458821 | 0 | 0 | 0.00250000 | 0.0424795187 | 0.0008464125 |
| 11 | 0.9508772907 | 0.0007555805 | 0.0000000000 | 0.0001984844 | 0.0033758841 | 0 | 0 | 0.00250000 | 0.0417927112 | 0.0008464125 |
| 12 | 0.9472359982 | 0.0008225044 | 0.0000000000 | 0.0001977389 | 0.0033075069 | **1** | 0 | 0.00250000 | 0.0411170080 | 0.0009071625 |
| 13 | 0.9436593010 | 0.0008939558 | 0.0000000000 | 0.0001970078 | 0.0032407225 | 1 | 0 | 0.00250000 | 0.0404522295 | 0.0009071625 |
| 14 | 0.9401504048 | 0.0009651219 | 0.0000000000 | 0.0001962908 | 0.0031754866 | 1 | 0 | 0.00250000 | 0.0397981991 | 0.0009071625 |
| 15 | 0.9367077416 | 0.0010360077 | 0.0000000000 | 0.0001955875 | 0.0031117567 | 1 | 0 | 0.00250000 | 0.0391547431 | 0.0009071625 |
| 16 | 0.9333297866 | 0.0011066185 | 0.0000000000 | 0.0001948977 | 0.0030494917 | 1 | 0 | 0.00250000 | 0.0385216905 | 0.0009071625 |
| 17 | 0.9300150566 | 0.0011769591 | 0.0000000000 | 0.0000194021 | 0.0029891516 | 1 | **1** | 0.00025000 | 0.0378988730 | **0.0011521489** |

**The five-month offset is on every row.** 보험나이 turns 1 at `t = 12`; 만나이 turns 1 at
`t = 17`. `age_man = −1` for `t < 5` because the insured does not yet exist, and the model
returns `q = 0` and `i_j = 0` from that fact rather than from a special case.

### The months where the product does something

| `t` | What happens |
|---|---|
| **0** | Issue. Acquisition expense and initial commission fall; `net_cf` is −₩298,646.2076 |
| **1–4** | Pre-birth. Premium on three streams, the void decrement, `claims_void` rising with `cum_prem_pp`, and **every child-life column identically zero** |
| **5** | **Birth.** The 태아보장기간 limbs pay ₩47,000 per birth all at once, plus one twelfth of the ₩63,450 신생아 block; every child-life cover switches on; `net_cf` is negative for **exactly one month** |
| **12** | 보험나이 turns 1; **renewal commission starts** |
| **17** | The 태아 module's cover and premium both end; **만나이 turns 1**; `claims_hospital` falls by half and `claims_event` and `claims_liability` rise; the child's waiver limb switches on |
| **36, 72, …** | The 3년만기 liability block renews; the 누수 limb is off for three months |
| **239 → 240** | **납입완료.** Premium and renewal commission stop; the 해약공제액 is long since released; `net_cf` changes sign for the remaining eighty years |
| **1200** | The 100세 계약해당일. Nothing is paid; `claims_maturity` is zero |

| `t` | `pols_if` | `premiums` | `claims_diagnosis` | `claims_hospital` | `claims_death` | `claims_lapse` | `expenses` | `commissions` | `net_cf` |
|---|---|---|---|---|---|---|---|---|---|
| 17 | 0.9311920157 | 26,040.4216 | 130.3535 | 3,512.4563 | 6.7821 | 177.0176 | 1,685.0952 | 781.2126 | 18,783.2542 |
| 120 | 0.7926463831 | 21,873.0675 | 79.3435 | 1,353.1380 | 15.6820 | 1,149.8680 | 1,480.1460 | 656.1920 | 15,651.7364 |
| 239 | 0.7675760087 | 20,562.2638 | 183.5349 | 1,515.4096 | 106.0073 | 344.4363 | 1,483.5920 | 616.8679 | 14,908.0252 |
| 240 | 0.7674946541 | 0.0000 | 183.5125 | 1,515.2490 | 106.2627 | 2,726.2032 | 456.1827 | 0.0000 | -6,391.6508 |
| 241 | 0.7669843661 | 0.0000 | 183.3875 | 1,514.2415 | 106.3913 | 2,729.4233 | 456.6323 | 0.0000 | -6,393.3820 |
| 360 | 0.7078397483 | 0.0000 | 420.1765 | 1,703.7898 | 210.9298 | 3,069.2282 | 512.8615 | 0.0000 | -7,124.0431 |
| 600 | 0.5935620502 | 0.0000 | 2,415.7974 | 2,921.8469 | 1,143.9560 | 3,634.3597 | 639.0498 | 0.0000 | -12,923.9553 |
| 720 | 0.5298765721 | 0.0000 | 4,738.1131 | 4,570.1874 | 2,608.6828 | 3,560.3727 | 695.4165 | 0.0000 | -19,465.9226 |
| 1080 | 0.1441715821 | 0.0000 | 2,342.3611 | 7,506.8138 | 8,685.6915 | 519.2086 | 342.7324 | 0.0000 | -21,825.3293 |
| 1140 | 0.0614770783 | 0.0000 | 920.2036 | 3,665.8156 | 1,110.9823 | 40.1461 | 161.3576 | 0.0000 | -6,998.6611 |
| 1199 | 0.0161892160 | 0.0000 | 223.1971 | 1,078.0805 | 7.9723 | 0.1737 | 46.8367 | 0.0000 | -1,662.7690 |
| 1200 | 0.0157346742 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

And the account, at the nodes the 상품요약서 publishes and the model must reproduce
(`check_refund_grid()`):

| `t` | years | `cum_prem_pp` | `refund_ratio` | `cv_std_pp` = `cv_pp` | `surr_chg_pp` | `av_pp` | [S2] published |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0.00000000 | 0.0000 | 364,000.0000 | 0.0000 | — |
| 12 | 1 | 336,000 | 0.00000000 | 0.0000 | 312,000.0000 | 252,000.0000 | **0.0%** |
| 36 | 3 | 1,008,000 | 0.45600000 | 459,648.0000 | 208,000.0000 | 667,648.0000 | **45.6%** |
| 60 | 5 | 1,680,000 | 0.62500000 | 1,050,000.0000 | 104,000.0000 | 1,154,000.0000 | **62.5%** |
| 84 | 7 | 2,352,000 | 0.66980000 | 1,575,369.6000 | **0.0000** | 1,575,369.6000 | — |
| 120 | 10 | 3,360,000 | 0.73700000 | 2,476,320.0000 | 0.0000 | 2,476,320.0000 | **73.7%** |
| 180 | 15 | 5,040,000 | 0.78300000 | 3,946,320.0000 | 0.0000 | 3,946,320.0000 | **78.3%** |
| 240 | 20 | 6,720,000 | 0.82600000 | 5,550,720.0000 | 0.0000 | 5,550,720.0000 | **82.6%** |
| 360 | 30 | 6,720,000 | 1.01200000 | 6,800,640.0000 | 0.0000 | 6,800,640.0000 | **101.2%** |
| 480 | 40 | 6,720,000 | 1.22500000 | 8,232,000.0000 | 0.0000 | 8,232,000.0000 | **122.5%** |
| 600 | 50 | 6,720,000 | 1.44100000 | 9,683,520.0000 | 0.0000 | 9,683,520.0000 | **144.1%** |
| 720 | 60 | 6,720,000 | 1.58900000 | 10,678,080.0000 | 0.0000 | 10,678,080.0000 | **158.9%** |
| 1140 | 95 | 6,720,000 | 0.16001230 | 1,075,282.6560 | 0.0000 | 1,075,282.6560 | **16.0%** |
| 1200 | 100 | 6,720,000 | 0.00000000 | 0.0000 | 0.0000 | 0.0000 | **0.0%** |

The 해약공제액 is released linearly over `surr_chg_period() = 84` months and is nil from
`t = 84`. The surrender value crosses premiums paid (₩6,720,000) between `t = 240` and
`t = 360` — **exactly as [S2]'s published grid says it does at about year 30** — and collapses
to nil at 만기, there being no 만기환급금 on the protection part.

### Hand traces

**Month 0 — issue, and the insured does not exist.** `l(0) = l_P(0) = 1`, `l_W(0) = 0`,
`born(0)` false.

    premiums(0)  = ( 28,000 + 3,000 ) × 1.0 × 1 = 31,000.0000
    every child-life benefit                    = 0.0000        [born(0) is false]
    claims_void(0) = ( cum_prem_pp(0) + prem_foetal_paid_pp(0) ) × pols_void(0)
                   = ( 0 + 0 ) × 0.0010055425391276573          = 0.0000
    claims_lapse(0) = ( CV(0) + U(0) ) × pols_lapse(0)
                    = ( 0 + 0.5 × 31,000 ) × 0.004260729152353977
                    = 15,500 × 0.004260729152353977             = 66.0413018615
    claim_expenses(0) = 30,000 × ( 0 × 1 + 0 + 0.0010055425391276573 )
                                                                = 30.1662761738
    expenses(0)  = ( 327,600.0000000000 − 212,940.0000000000 ) × 1
                   + 400 × 1.0 × 1 + 0.05 × 31,000
                 = 114,660.0000000000 + 400.0000 + 1,550.0000    = 116,610.0000000000
    commissions(0) = 212,940.0000000000 × 1                      = 212,940.0000000000

    net_cf(0) = 31,000.0000 − 66.0413018615 − 30.1662761738
                − 116,610.0000000000 − 212,940.0000000000        = −298,646.2075780353

Note that `claims_void(0)` is **zero and not nil by accident**: no premium has yet been
collected at the start of month 0, so there is nothing to refund. The decrement is there —
0.10055% of contracts are voided in the month — and it costs nothing.

**Decrements, month 0**, in the order **void → waiver → mortality → lapse**:

    v(0)   = 1 − (1 − 0.012)^(1/12)                     = 0.0010055425391276573
    ω(0)   = 1 − (1 − 0) (1 − 0.0008464125)             = 0.0008464125
    ω_m(0) = 1 − (1 − 0.0008464125)^(1/12)              = 0.00007056175284536614
    e(0)   = 1 × ( 1 − 0.0010055425391276573 ) × 0.00007056175284536614
           = 0.9989944574608723 × 0.00007056175284536614 = 0.00007049080000124472
    q_m(0) = 0                                          [no insured yet]
    w_m(0) = 1 − 0.95^(1/12)                            = 0.004265318777560645

    pols_void(0)  = 1 × 0.0010055425391276573           = 0.0010055425391276573
    pols_death(0) = ( 1 − 0.0010055425 ) × 0            = 0.0000000000
    pols_lapse(0) = ( 0.9989944574608723 − 0.0000704908 ) × 1 × 0.004265318777560645
                  = 0.9989239666608711 × 0.004265318777560645 = 0.0042607291523540
    l_P(1)        = 0.9989239666608711 × 1 × ( 1 − 0.004265318777560645 )
                                                        = 0.9946632375085172
    l_W(1)        = ( 0 + 0.00007049080000124472 ) × 1  = 0.0000704908000012
    l(1)          = 0.9946632375085172 + 0.0000704908   = 0.9947337283085184

and the roll-forward closes: `1 − 0.9947337283085184 = 0.0052662716914816`, against
`0.0010055425391277 + 0 + 0.0042607291523540 = 0.0052662716914816`.

**Month 5 — birth, and the one month in which the contract loses money after issue.**
`l(5) = 0.9746262555490346`, `l_P(5) = 0.9742781992`, `born(5)` true, `age_man(5) = 0`.

    premiums(5) = 31,000 × 1.0 × 0.9742781992         = 30,202.6241744982

Per policy in force, at 만나이 0:

    benefit_DISABILITY = 100,000,000 × 0.12 × 0.000008355800662718238
                       + 10,000,000 × 0.15 × 0.00021692529081551726
                       = 100.2696079526 + 325.3879362233        = 425.6575441759
    benefit_DIAGNOSIS  = 10,000,000 × 0.000015001237642309206 × 1 × 1
                       +  2,000,000 × 0.000002500034375629845
                       + 10,000,000 × 0.0000033333944460256504
                       + 10,000,000 × 0.00000016666681945665118
                       = 150.0123764231 + 5.0000687513 + 33.3339444603 + 1.6666681946
                                                                = 190.0130578292
    benefit_SURGERY    = 5,000,000 × ( 0.85 × 0.000015001237642309206
                                     + 0.50 × 0.0000033333944460256504
                                     + 0.70 × 0.00000016666681945665118 )
                       = 5,000,000 × 0.000014534415992595306     = 72.6720799630
    benefit_HOSPITAL   = 40,000 × ( 0.10 + 2.40 ) / 12 × 0.92
                       = 40,000 × 0.2083333333333 × 0.92         = 7,666.6666666667
    benefit_EVENT      = 400,000 × 0.0003339460107422143
                       + 200,000 × 0.0005013802940021517
                       = 133.5784042969 + 100.2760588004         = 233.8544630973
    benefit_LIABILITY  = 0.0003339460107422143 × 600,000 × 1.0 × 1.0
                                                                = 200.3676064453
    benefit_NEONATAL   = 47,000 + 63,450 / 12 = 47,000 + 5,287.50 = 52,287.5000000000

Weighted by `l(5) = 0.9746262555490346`, those give the row's 414.8570184264, 185.1917150575,
70.8281171773, 7,472.1346258759, 227.9206997120, 195.2835300031 and **50,960.7703370201**.
Then

    claims_death(5) = ( A(5) + U(5) ) × pols_death(5)
                    = ( 105,000.0000 + 15,500.0000 ) × 0.00020328016703563597
                    = 120,500 × 0.00020328016703563597           = 24.4952601278
    claims_lapse(5) = ( 0 + 15,500 ) × 0.003822143851874877      = 59.2432297041
    claims_void(5)  = 0                                          [t = b, v(5) = 0]
    claim_expenses(5) = 30,000 × ( 0.0014155547402482371 × 0.9746262555490346
                                   + 0.00020328016703563597 + 0 )
                                                                = 47.4875094915
    expenses(5)     = 400 × 1.0082852288053106 × 0.9746262555490346
                      + 0.05 × 30,202.6241744982
                    = 393.0805028304 + 1,510.1312087249          = 1,903.2117115553
    commissions(5)  = 0.0000

`commissions(5)` is the trap in this row. Renewal commission is `0.03 × premiums(t)` for
`12 <= t <= prem_end()` only, so it is nil here and worth about ₩900 a month if the lower
bound is dropped.

    net_cf(5) = 30,202.6241744982
                − ( 414.8570184264 + 185.1917150575 + 70.8281171773 + 7,472.1346258759
                    + 227.9206997120 + 195.2835300031 + 50,960.7703370201 )
                − 24.4952601278 − 59.2432297041
                − 47.4875094915 − 1,903.2117115553 − 0.0000
              = 30,202.6241744982 − 61,561.4237541510            = −31,358.7995796528

**₩50,960.77 of that is the 태아 module in a single month**, and it is 85.6% of the month's
₩59,526.99 of morbidity outgo. The neonatal cost is not spread: the 태아보장기간 limbs are
paid on events of the pregnancy and the delivery and they are paid **at birth**.

**Month 17 — the 태아 module ends, and 만나이 turns 1.** Two structural things happen in the
same month and they pull in opposite directions. `l(17) = 0.9311920157360853`,
`l_P(17) = 0.9300150566`, `age(17) = 1`, `age_man(17) = 1`.

    P(17)       = 28,000 only                       [foetal_prem_end() = 16]
    premiums(17)= 28,000 × 1.0 × 0.9300150566        = 26,040.4215845963
    benefit_HOSPITAL = 40,000 × ( 0.13 + 1.10 ) / 12 × 0.92
                     = 40,000 × 0.1025 × 0.92        = 3,772.0000000000
        against 7,666.6667 at 만나이 0 — hosp_dis falls 2.40 → 1.10 days a year
    benefit_EVENT    = 400,000 × 0.0007531116566323881
                     + 200,000 × 0.000417624589193033
                     = 301.2446626530 + 83.5249178386 = 384.7695804916
        against 233.8545 — fracture rises 0.004 → 0.009
    benefit_LIABILITY = 0.0005013802940021517 × 600,000 = 300.8281764013
        against 200.3676 — liability rises 0.004 → 0.006
    benefit_NEONATAL  = 0.0000                       [t = f = 17, the module has ended]

    claims_death(17) = ( A(17) + U(17) ) × pols_death(17)
                     = ( 335,553.3333333334 + 14,000.0000 ) × 0.000019402056913845515
                     = 349,553.3333333334 × 0.000019402056913845515 = 6.7820536678
    claims_lapse(17) = ( 45,220.0000 + 14,000.0000 ) × 0.002989151566722004
                     = 59,220 × 0.002989151566722004  = 177.0175557813
    expenses(17)     = 400 × 1.028450933381417 × 0.9311920157360853
                       + 0.05 × 26,040.4215845963
                     = 383.0741190965 + 1,302.0210792298 = 1,685.0951983263
    commissions(17)  = 0.03 × 26,040.4215845963        = 781.2126475379

    net_cf(17) = 26,040.4215845963 − 7,257.1673721150  = 18,783.2542124813

**`U(17)` is ₩14,000 and not ₩15,500**, because the 미경과보험료 is half of *that month's*
office premium and the 태아 stream has stopped. And the waiver rate steps up in the same
month: `ω(17) = 1 − (1 − 0.0002452088)(1 − 0.0009071625) = 0.0011521489`, the child's limb
switching on as the 신생아 block — and with it the P코드 carve-out — ends.

**Month 240 — 납입완료.** `l(240) = 0.7674946541379640`, `P(240) = 0`, `U(240) = 0`,
`ω(240) = 0`, `w(240)` steps from 0.0010164337 to the ultimate **0.008**.

    premiums(240)    = 0.0000
    commissions(240) = 0.0000                        [no renewal commission after 납입완료]
    expenses(240)    = 400 × 1.485947395978355 × 0.7674946541379640 + 0.05 × 0
                     = 594.3789583913 × 0.7674946541379640 = 456.1826730974
    claims_lapse(240)= ( 5,550,720.0000 + 0 ) × 0.0004911440743415418 = 2,726.2032363291
    claims_death(240)= ( 5,550,720.0000 + 0 ) × 0.000019143942790725917 = 106.2626661273

    net_cf(240) = 0 − ( 459.6209777245 + 183.5124600595 + 63.8868013892
                        + 1,515.2489675306 + 575.2275491970 + 244.5978916122 )
                    − 106.2626661273 − 2,726.2032363291
                    − 60.9075982374 − 456.1826730974
                = −6,391.6508213043

**The sign change is not gradual.** `net_cf(239)` is **+₩14,908.0252** and `net_cf(240)` is
**−₩6,391.6508**, a swing of ₩21,299.68 in one month. Four things move at once: the premium
stops (−₩20,562.26), renewal commission stops (+₩616.87), expense falls (+₩1,027.41 — the
premium-related maintenance of ₩1,028.11 going, against ₩0.70 more of inflating per-policy
maintenance) and `claims_lapse` jumps (−₩2,381.77) — because the ultimate lapse rate is
**eight times** the rate an instant before 납입완료 and the surrender value it is paid on is
now ₩5,550,720. **From `t = 240` there is not one positive month in the remaining eighty
years.**

### Policy year 1 in aggregate

`t = 0 … 11`, spanning the pre-birth period, the birth and seven months of the 신생아 block.
`Σ pols_if(t) = 11.6888828896`.

| Line | Policy year 1 total |
|---|---|
| `premiums` | 362,213.7519 |
| `claims_disability` | 2,869.1771 |
| `claims_diagnosis` | 1,280.7497 |
| `claims_surgery` | 489.8319 |
| `claims_hospital` | **51,677.7500** |
| `claims_event` | 1,576.3138 |
| `claims_liability` | 1,350.5931 |
| `claims_neonatal` | **81,448.2301** |
| `claims_death` | 257.5124 |
| `claims_lapse` | 706.1779 |
| `claims_maturity` | 0.0000 |
| `claims_void` | 306.8991 |
| `claim_expenses` | 477.6984 |
| `expenses` | 137,488.5297 |
| `commissions` | 212,940.0000 |
| **`net_cf`** | **−130,655.7114** |

Benefit outgo of ₩141,963.2351 is **39.2%** of year-1 premium, and **57.4% of it is the 태아
module**. Against that, ₩327,600.0000 of acquisition expense and initial commission at
`t = 0` — **10.57 months of the ₩31,000 first-year office premium** — produce the
characteristic new-business strain.

### Undiscounted totals over the whole 1,201-month projection

| Line | Total |
|---|---|
| `pols_if` | 651.7356 |
| `premiums` | **5,458,037.9345** |
| `claims_disability` | 957,652.5232 |
| `claims_diagnosis` | 2,844,503.4398 |
| `claims_surgery` | 1,094,506.2990 |
| `claims_hospital` | **5,033,285.2166** |
| `claims_event` | 466,414.7324 |
| `claims_liability` | 195,939.3565 |
| `claims_neonatal` | 106,330.7157 |
| `claims_death` | **3,693,345.7287** |
| `claims_lapse` | **2,695,713.6444** |
| `claims_maturity` | **0.0000** |
| `claims_void` | 306.8991 |
| `claim_expenses` | 79,991.4163 |
| `expenses` | 1,009,668.2371 |
| `commissions` | 365,814.7255 |
| **`net_cf`** | **−13,085,434.9998** |

Morbidity outgo is ₩10,698,632.2832 and account-driven outgo — death, lapse, maturity, void —
is ₩6,389,366.2722; the four exits account for **0.0049757330** voids, **0.4688979472**
deaths, **0.5103916457** lapses and **0.0157346742** maturities, summing exactly to one.

### The equivalence premium

| Cells | Value |
|---|---|
| `epv_outgo_pp()` | 4,694,583.10870084 |
| `epv_prem_unit_pp()` | **151.0503621937853** |
| `equiv_premium_mth_pp()` | **31,079.588559199034** |

At the 보장부분 적용이율 of 2.75%, the discounted outgo of ₩4,694,583.11 divided by the
discounted, in-force-weighted count of premium instalments actually collected gives a level
core premium of **₩31,079.59**, against a shipped ₩28,000. **The shipped basis is 11.00%
short** and, per `product-spec.md`, this figure governs. `check_equiv_premium()` asserts the
identity closes over 1,201 terms spanning eight orders of magnitude.

**`epv_prem_unit_pp()` is where the whole model's behaviour is visible in one number.** Out of
240 scheduled instalments the projection expects to collect the discounted equivalent of
**151.05 — 62.9%**. Lapse, the two waivers, mortality, the void and discounting between them
destroy 37.1% of a level premium stream over twenty years, and that is on a product whose
lapse assumption converges to 0.1% at 납입완료.

### What the numbers say

The shape is a hundred-year contract with a twenty-year premium in one line: a new-business
strain of ₩298,646 at issue, one negative month at birth, a positive stretch of nearly twenty
years averaging about ₩14,000 a month, and then **eighty years of pure outgo** with not a
single positive month in it. Undiscounted, ₩5,458,038 of premium meets ₩17,087,999 of benefit
and ₩1,455,474 of expense and commission, for a total of −₩13,085,435 — and that is not a
defect in the projection but what such a contract looks like before discounting. Discounted at
2.75% the two sides balance at ₩31,079.59 a month.

Three of the totals are worth reading directly. **`claims_hospital` is the largest benefit
line at ₩5,033,285 — 47.0% of all morbidity outgo and 92.2% of the whole premium collected.**
That is what a ₩40,000-a-day 입원일당 written to 100세 costs on the shipped basis, and it is
the opposite of the chassis, where the diagnosis limbs dominate. **`claims_death` at
₩3,693,346 is the second largest line and is not a death benefit at all**: it is the
계약자적립액 plus the 미경과보험료 paid on a death 상법 제732조 forbids covering, and it
becomes the biggest single monthly outgo after about `t = 700` because the account is then
₩10.7 million and mortality is finally material. **`claims_maturity` is identically zero**:
there is no 만기환급금 on the protection part and the shipped 환급률 taper reaches zero at
만기, so the 1.57% of policies that survive to the 100세 계약해당일 receive nothing.

Two more read against the product's own history. The **태아 module costs ₩106,330.72 in
total** — **0.9627** of its ₩110,450 per-birth cost, the shortfall being the 3.7% of contracts
already voided or lapsed by the time the block runs — and **every won of it falls inside the
first thirteen months of a hundred-year contract**. And the **general-tier `frac_open` ledger
runs from 1.0000 to 0.4023 over the term**: paediatric cancer incidence is two orders of
magnitude below the adult rate, so the ledger is almost untouched for thirty years and then
drains fast, which is the arithmetic behind [R5]'s premium-by-issue-age index — a 0세 issue
pays 100 against a 30세 issue's 264 for the same cover, because the child's premium is being
collected against eighty years of exposure that has not begun.

---

## Valuation and reserve pointers

This model projects **gross, undiscounted liability cash flows**. Every valuation layer below
consumes them and is cited, never reproduced. Korea is unusual in running three of them at
once and live.

- **IFRS 17 (K-IFRS 제1117호)** has been mandatory since **2023-01-01** [REG-R60]. The
  fulfilment cash flows, the risk adjustment and the CSM all consume a stream of this shape and
  none is computed here. Two features bear directly on the measurement: the **contract
  boundary** question raised by the 갱신형 blocks inside a 비갱신형 core, recorded as
  unresolved; and the **eighty paid-up years**, which mean the CSM of a child policy is
  dominated by cash flows beginning two decades after issue — what makes the lapse assumption
  over the payment period worth so much, and what the supervisor moved against in 2024 [R11]
  [REG-R27].
- **K-ICS** applies from the same quarter [REG-R13] [REG-R30]. The **대량해지 shock** and its
  고환급형 test live in 보험업감독규정 [별표 22], which **was not retrieved**; everything
  resting on it is second-hand through [REG-R36] and carries **[unverified]** [REG-R26]. It
  matters here because model points 4 and 5 are 무해지 forms, which is what the 고환급형 test
  is about.
- **해약환급금준비금** — the Korea-specific layer with no counterpart anywhere else in this
  repository [REG-R11]. Under IFRS 17 a profitable in-force block can carry a liability
  materially below the aggregate contractual surrender value, and the reserve quarantines the
  difference inside 이익잉여금 at **company level**, not contract level, under 감독규정
  제6-11조의6 (and 제6-18조의6 on the non-life side). It stood at ₩23.7조 at end-2022 and
  ₩32.2조 at end-2023 [REG-R11] [REG-R36]. On this product the gap it is built to catch is
  visible directly: `cv_pp(t)` exceeds `cum_prem_pp(t)` from **`t = 353`**, which is a
  surrender obligation an IFRS 17 liability need not hold. **No `krlib` model computes it.**
- **책임준비금** under 감독규정 제6-11조 [REG-R10] and the 계약자적립액 under 제7-65조 and
  제7-66조 [REG-R18] [REG-R19]. This model **reads a published surrender value and recovers
  the account from it**: it runs neither the 순보험료식 recursion nor the 공시이율 reset, both
  of which are carried by reference to `WholeLife_KR_S`.
- **The 표준해약공제액 and the 해약공제기간** are computed here, at [별표 14] and 제7-66조
  제1항제2호 [REG-R20] [REG-R19], because they bound the surrender value and the deductible
  acquisition cost and therefore change the cash flows. They are the only regulatory
  computation this model performs, and `check_surr_chg_cap()` and `check_acq_cost_cap()`
  assert both bounds.
- **Not applicable.** 계약자배당 and the surplus-distribution machinery of 제6-11조의7 and
  제6-13조 do not attach — the contract is 무배당 [REG-R12] — and there is no 특별계정
  [REG-R15] and no 보증준비금 for a guarantee this product does not write.
- **Policyholder tax, not modelled.** The premium is a 보장성보험료 attracting a **12% tax
  credit** on up to ₩1,000,000 a year under 소득세법 제59조의4 [REG-R57] — a *credit*, not a
  deduction, which is what makes the Korean after-tax comparison differ from every other
  market in this repository. The anchor cell's ₩372,000 of first-year premium sits inside the
  cap. Benefits are not projected net of policyholder tax.
- **예금자보호** to **₩100,000,000** per person per insurer since 2025-09-01, in a bucket that
  expressly excludes benefits payable because the term has ended [REG-R52]; the ₩50,000,000 of
  the 약관 wording retrieved here is the pre-2025 figure [S8]. A structural fact about the
  liability, not a cash flow.

---

## Key sensitivities and model risks

In rough order of leverage on a book of this product.

1. **The morbidity basis is the whole model and it is [std] with one exception.** Eleven
   causes at fourteen pivot ages, and the only published Korean child morbidity rate anywhere
   in the research is 일반상해 후유장해 발생률(3~100%) at 5세, 상해 1급 — 남자 0.0001823,
   여자 0.0001163 [S1]. Everything else is a shape drawn around it, and **no shipped row was
   reconciled to the one public reference grid there is** — the 장기손해보험 참조순보험요율
   display, published under 보험업법 제176조제9항 and reaching 연령 0 and 10 [REG-R61], which
   this product's pass did not open. A carrier's own 적용위험률 stays out of reach either way:
   the 산출방법서 is an undisclosed 기초서류 [REG-R2] and the life-side 참조순보험요율 is filed
   and not published [REG-R4].
2. **The two hospital-cash limbs carry 47.0% of all morbidity outgo**, and they are driven by
   a **day count**, not a frequency. `hosp_dis` runs 2.40 days a year at 만나이 0, 0.55 at 5,
   0.35 at 10 and 20.0 at 100 — a **fifty-seven-fold** range with a U-shape whose left arm is
   the infant peak and whose right arm is old age. The cap factor κ = 0.92 is a single number
   standing over a whole length-of-stay distribution the model does not carry.
3. **Expense inflation over a hundred years.** 2% a year compounds to **7.24**. Per-policy
   maintenance is ₩400 a month at issue and ₩2,898 at the 100세 계약해당일, it runs for the
   whole term rather than to 납입완료, and it is the largest single expense item in the
   projection. At 1% it would be ₩1,081.93 at the end and at 3% **₩7,687.45**, a spread of
   seven times on the same charge. **The assumption is not a detail on this product.**
4. **The lapse assumption over the payment period, and the supervisor agrees.** The shipped
   `loglinear` basis converges to 0.1% at 납입완료; `disclosed` sits at 5.0/3.0/1.0% and then
   0.5%. On model point 5 the two produce undiscounted `net_cf` of −₩8,061,541 against the
   anchor's −₩13,085,435, and on a 무해지 form the difference is worth still more because
   `claims_lapse` is identically zero over the period. This is the sensitivity the 2024
   계리가정 guideline exists to constrain [R11] [REG-R27] and the reason it is a supervisory
   matter at all.
5. **The 계약자's mortality is a second, uncorrelated exposure, and it is the larger waiver
   limb for the first fifteen years.** At `t = 0` the 계약자's limb is 0.0008464125 a year and
   the child's is **zero**; at `t = 239` they are 0.0038416625 and 0.0003484597. The waiver's
   whole value is concentrated in the twenty years in which a 33-to-53-year-old parent might
   die or become severely disabled, which is why the module is cheap enough to be compulsory —
   and why an error in `payer_age` moves more than an error in any child incidence rate.
   `payer_disab_ratio = 0.25` is pure [std]: **no Korean disability incidence table is
   public**.
6. **The 태아 module's severity is a length-of-stay question and the file has no published
   anchor.** The incubator limb is ₩50,000 × (days − 2) capped at 60 and the perinatal-cash
   limb ₩10,000 × (days − 3) capped at 120 [S1] [S8]; the shipped 8.0 and 7.5 expected paid
   days are [std]. The supervisor's own worked claim ran to ₩4,200,000 of day benefits on a
   32-week, 1.84 kg birth [R3], against the module's ₩110,450 expected cost per birth — so
   the tail is two orders of magnitude above the mean and the module is a **frequency**
   assumption dressed as a severity one.
7. **The `disab_severity` of 0.12 carries a ₩100,000,000 sum insured.** The 기본계약 is the
   largest single 보험가입금액 in the contract and the most heavily standardized parameter
   attached to it. The accident limb alone costs **₩555,177.98** over the term at 0.12; read
   as a lump sum at the full 가입금액 it would cost **₩4,626,483.18**, 85% of the whole
   premium collected.
8. **The term, not the age.** [R5]'s own index puts a 0세 issue at 100 against a 30세 issue's
   264 for the same cover over 20년납 to 100세 만기, and the two short-horizon cells are the
   two whose premiums come closest: model point 8 at **+0.57%** and model point 9 — the
   30세만기 female cell — at **−1.90%**, ₩3,026 shipped against ₩2,968.47 computed, so that
   it and model point 5 are the only two cells whose shipped premium is *above* its own
   equivalence premium. Across the ten the computed premium runs from 11.75% below the
   shipped figure to 43.78% above it. **The term extension of 2011 is what makes this
   product hard to price and easy to under-price** [R5].
9. **Longevity is the tail risk, not mortality.** Only 1.57% of policies reach the 100세
   계약해당일 on the shipped basis, yet `claims_hospital` peaks at **₩10,877.56 at `t = 965`**
   and `claims_death` at **₩15,452.17 at `t = 1013`** — and **`claims_death` is the largest
   single column in every one of the 166 months from `t = 929` to `t = 1094`** (and again at
   `t = 1097` and `t = 1098`), after which the in-force block has thinned so far that
   `claims_hospital` takes the lead back for the last eight years. The liability is
   concentrated in the ages where the survival assumption is least certain and where a [std]
   mortality construction is least defensible.
10. **The 실손 boundary could move.** The reason this product has no indemnity limb is
    regulatory, not economic [R9] [R10], and a 5세대 실손 reform is under way [REG-R31]. A
    change to 감독규정 제7-63조제2항제1호 would change what an 어린이보험 *is*.

### Known modeling pitfalls

Each of these is a mistake a competent modeller would actually make on this product, and each
is checkable against the shipped model.

- **Attaching cover at the 계약일 rather than at birth.** Every benefit on the child's own
  life must be **identically zero** for `t < b`, and the insured's mortality with it
  [S8 제54조] [R2] [R3]. `check_cover_at_birth()` asserts it. A model that lets the hospital
  or disability limbs run from `t = 0` adds five months of the **infant** rate — the highest
  in the whole table — to a period in which nobody is at risk, and overstates year-1 benefit
  outgo by about 30%.
- **Treating the pre-birth void as a lapse.** 유산 or 사산 makes the contract **무효** and
  returns **every premium paid on both streams** [S8 제56조] [S9]. On the 표준형 the surrender
  value at `t = 4` is nil and the refund is ₩122.13; on a 무해지 point the surrender value is
  nil for twenty years and the refund is unchanged. Netting the void into `claims_lapse`
  destroys the refund entirely and loses a decrement from the roll-forward.
- **Running the projection on one age.** 보험나이 and 만나이 differ by exactly `b` months for
  the life of a foetal contract. Reading the decrement tables at 보험나이 ages the insured by
  five months everywhere, and — worse — makes `age_man` non-negative before birth, which
  quietly re-enables the covers the birth gate exists to suppress. The contract expires when
  the insured is **99 years and 7 months old**, and `age_man(1200) = 99`.
- **Applying the monthly conversion to a day count.** `hosp_acc` and `hosp_dis` are **expected
  days per policy year**. `1 − (1 − 2.40)^(1/12)` is a complex number, and
  `1 − (1 − 0.55)^(1/12)` is a real number that is simply wrong. Divide by twelve.
  `benefit_pp(t, "HOSPITAL")` must never route through `inc_rate_mth`.
- **Re-testing the 면책기간 at the claim date.** The under-15 disapplication is decided **at
  the 계약일** [S3] [S11]. A contract issued at 계약나이 0 has **no cancer waiting period at
  any point in its hundred-year life**, including the eighty-five years in which the insured
  is an adult. A model that switches the 90 days back on at 보험나이 15 is modelling a
  contract nobody sells.
- **Applying a 감액 to a foetal contract.** `reduction_mths()` returns **zero on a 태아
  contract whatever the model point says**, because the 2015 변경권고 inserted 「단, 피보험자가
  보험가입 당시 태아인 경우에는 보험금의 100%를 지급합니다」 across 17 carriers and 56
  products [R2] [S8]. Reading `reduction_mths` straight off the model point re-imposes a
  reduction the supervisor removed.
- **Letting the child's waiver limb run over the 신생아 block.** 「출생전후기에 기원한 특정
  병태(P코드) 진단시 납입면제를 적용하지 않음」 [S2]. The covers most likely to pay in the
  first year of a foetal contract are precisely the ones that cannot stop the premium. The
  signature is the step in `waiver_rate` from 0.0009071625 at `t = 16` to **0.0011521489** at
  `t = 17`; a model without the carve-out has no step.
- **Modelling the parent as a benefit rather than as a decrement — or the reverse.** On the
  생명보험 chassis the 계약자's death is a **waiver trigger** in the main clause
  [S10 제22조제1항]; on the 손해보험 chassis the same economics arrive as a compulsory 부양자
  death **rider** paying a lump sum or an education annuity [S5] [S11]. They are not
  interchangeable: one removes a premium stream, the other adds an outgo, and their expected
  values differ by more than an order of magnitude.
- **Running the waiver after 납입완료.** `ω(240) = 0`. A waiver of premium on a contract with
  no premium transfers policies into a compartment whose only remaining difference is that it
  is **not exposed to lapse** — silently suppressing eighty years of lapses, and with them the
  ₩2,695,714 of `claims_lapse` that is **15.8% of all benefit outgo**.
- **Exposing the waived compartment to lapse.** The mirror error. `pols_lapse(t)` is drawn
  from `pols_pay` alone; `check_waiver_split()` and `check_pols_roll_fwd()` both fail if it is
  not.
- **Treating the 기본계약 as a lump sum.** It is 보험가입금액 × 장해지급률 on a continuous
  3~100% band [R12] [S1] [S2] [S11]. The accident limb costs **₩555,177.98** over the term at
  `disab_severity = 0.12` and **₩4,626,483.18** at severity 1.0. **The error is a factor of
  8.3 and it lands on the largest sum insured in the contract.**
- **Weighting the `frac_open` ledgers by `pols_if`.** They are **per policy**, not per block.
  Weighting them by the in-force probability measures the block's consumption and defers the
  exhaustion forever, which on a hundred-year term is worth a great deal:
  `frac_open(1200, cancer)` is **0.4023261296**, not something near 1.
- **Charging renewal commission from `t = 1`, or after 납입완료.** It runs `12 <= t <= 239`
  only. The first error is worth about ₩900 a month in months 1–11; the second is worth
  eighty years of commission on a premium nobody pays.
- **Paying a 만기환급금.** There is none on the protection part [S1] [S2]. `claims_maturity`
  is a column of zeros and `refund_ratio(1200)` is 0.0. A model that pays `av_pp` at maturity
  without the taper pays ₩10,678,080 to the 1.57% of policies that get there.
- **Starting the 계약자적립액 at the surrender charge.** The published grid is 「순보험료식
  계약자적립액에서 해약공제액을 공제한 금액」 [S2], already net and floored at zero, so adding
  the unamortised charge back where the floor binds gives an account of ₩364,000 at `t = 0` on
  a contract that has collected nothing. The cap at `net_prem_ratio × cum_prem_pp(t)` is what
  makes `av_pp(0) = 0`; `check_av_bounds()` asserts the three inequalities.
- **Computing the notional 보험가입금액 at the insured's own age.** [별표 15] 제9호 is
  evaluated at the **기준연령 요건, 남자 만 40세** [REG-R21] [REG-R9 제1-2조제2호](#krlib-reg-r9). At 만나이
  5 the mortality rate is 0.00012 and the [별표 14] formula limb comes out at ₩12,380,087.45,
  **442.1 months of premium**; at 40 it is ₩1,575,064.09, or **56.25 months**. Neither binds:
  the FSC's thirteen-month reading of the same cap does [REG-R29], at ₩364,000.00, and the
  계약체결비용 at 90% of it at **11.70 months**.
- **Dropping the void or the maturity from the roll-forward.** There are **four** exits, not
  two. `check_exit_total()` requires them to sum to `pols_if_init()` over the projection —
  0.0049757330 + 0.4688979472 + 0.5103916457 + 0.0157346742 = 1 exactly.
- **Interpolating the incidence grid linearly.** The rates span two or more orders of
  magnitude between adjacent pivots; log-linear interpolation reproduces every pivot exactly
  and a linear one is wrong by a factor of two mid-span. The published 0.0001823 at 만나이 5
  must come back to its last digit, which it does only because the interpolator short-circuits
  at a pivot.
- **Assuming the female rate is below the male.** The comparison board shows the sex
  relativity with **no fixed sign** — four carriers price the female higher and seven lower,
  the spread running 62% to 114% [S11] — so the male-rate convention on a 태아 contract [R3]
  [S8] no longer implies a refund on the birth of a girl. The composite does not model the
  true-up, and a model that assumes its direction is asserting something the market
  contradicts.
- **Monthly rounding does not re-add.** The displayed rows are rounded to four decimals; the
  year-1 and whole-projection totals are sums of unrounded values, and the two differ in the
  last displayed digit. Assert against the unrounded aggregation.

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
[R8]: #krlib-child-r8
[R9]: #krlib-child-r9
[REG-R10]: #krlib-reg-r10
[REG-R11]: #krlib-reg-r11
[REG-R12]: #krlib-reg-r12
[REG-R13]: #krlib-reg-r13
[REG-R15]: #krlib-reg-r15
[REG-R17]: #krlib-reg-r17
[REG-R18]: #krlib-reg-r18
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R21]: #krlib-reg-r21
[REG-R24]: #krlib-reg-r24
[REG-R25]: #krlib-reg-r25
[REG-R26]: #krlib-reg-r26
[REG-R27]: #krlib-reg-r27
[REG-R28]: #krlib-reg-r28
[REG-R29]: #krlib-reg-r29
[REG-R30]: #krlib-reg-r30
[REG-R31]: #krlib-reg-r31
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R36]: #krlib-reg-r36
[REG-R38]: #krlib-reg-r38
[REG-R39]: #krlib-reg-r39
[REG-R4]: #krlib-reg-r4
[REG-R40]: #krlib-reg-r40
[REG-R41]: #krlib-reg-r41
[REG-R48]: #krlib-reg-r48
[REG-R50]: #krlib-reg-r50
[REG-R51]: #krlib-reg-r51
[REG-R52]: #krlib-reg-r52
[REG-R57]: #krlib-reg-r57
[REG-R60]: #krlib-reg-r60
[REG-R61]: #krlib-reg-r61
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
