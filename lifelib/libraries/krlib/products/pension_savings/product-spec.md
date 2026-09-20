# Product Specification

**Status:** Draft, 2026-09-03 (all cited sources accessed 2026-09-03).

**Scope note.** This is a *standardized composite specification* of a Korean tax-qualified
pension savings contract — 연금저축보험 (*yeongeum jeochuk boheom*), the insurance leg of the
statutory 연금저축 wrapper — assembled for reference liability cash-flow modelling. It
describes no single insurer's contract. Facts carrying a source tag — [S#] (primary product
documents: 약관 (*yakgwan*, policy conditions), 상품요약서 (*sangpum yoyakseo*, the statutory
product summary), 상품안내장 (compliance-approved sales literature) and 공시자료 (regulatory
rate disclosure)) and [R#] (product-specific regulatory, statutory and statistical references),
both numbered per `_research/pension-savings.md` and resolved in `sources.md` (same directory;
numbering frozen, never renumbered), and [REG-R#] (the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is distinct) — were
extracted from the cited document. Values marked **[std]** are standardizations introduced for
the reference implementation; each [std] table row carries a numbered footnote giving the
rationale and, where one exists, the observed range across insurers. Facts the research pass
could not confirm against a retrieved document are flagged [unverified].

Documents from **twelve** carriers were pursued. **Eight 연금저축보험 contracts** yielded
extractable text and are the basis of this composite: two products of one carrier — a
direct-channel 무배당 (*mubaedang*, non-participating) contract whose 상품요약서 publishes a
complete expense, surrender-charge and annuitant-mortality schedule [S1], a tied-channel
participating contract whose leaflet publishes three annuity illustrations on one model point
[S2], and that carrier's own 약관 with the income-tax article and the Enforcement Decree
reproduced verbatim in its 부록 [S3]; a second carrier's 약관 with the declared-rate article
and the minimum-fund guarantee [S4]; a third carrier's 2016-vintage bancassurance leaflet, kept
deliberately because it dates the pre-2023 tax parameters and carries the fullest published
annuity illustration [S5]; a fourth carrier's 약관, the only retrieved contract stating the
보험나이 / 만나이 rule in terms [S6]; the state postal insurer's 상품요약서, the only retrieved
연금저축보험 with a **non-zero** surrender charge [S7]; and a **non-life** insurer's 약관, the
cleanest demonstration of what a 손해보험사 may not write [S8]. Three further documents [S9]
[S10] [S11] serve only as bracketing evidence, and a variable annuity [S10] is cited **only**
for annuitisation machinery. Seven regulatory-disclosure and comparison pages — [S12] to
[S16], [S19] and [S20] — supply declared rates, guarantee ladders and market statistics; the
supervisor's own comparison display returned a four-year-stale quarter [S19] and the life
association's portal returned its category tree and nothing else [S20], so no parameter rests
on either. The two 손해보험협회 공시실 displays the research file carries as S17 and S18 are
cited by no document here and so have no entry in `sources.md`, which records the omission.

The composite is a **무배당, level monthly basic premium, 금리연동형 (interest-sensitive)
연금저축보험**: 보험나이 (*boheom nai*, insurance age) 40 at issue, 20 years of premiums to 60,
a five-year gap, and annuity from 65 as a 종신연금형 (*jongsin yeongeumhyeong*, life annuity)
with a ten-year guarantee. Its two phases — accumulation of a 계약자적립액 (*gyeyakja
jeongnibaek*, policyholder account value) at the declared rate, then payout — run on one
monthly grid in `Pension_KR_S`. The contract inherits the **surrender-value machinery** of the [whole
life chassis (종신보험)](../whole_life/technical-notes.md) — the 해약공제액, its
표준해약공제액 (*pyojun haeyak gongjeaek*, the statutory cap on the surrender charge) and the
해약환급금 (*haeyak hwangeupgeum*, surrender value) floor. It does **not** inherit that
chassis's 계약자적립액 recursion: there the account is a net-level accumulation with a
survivorship release, here it is a plain balance with no mortality in it, and only the name is
shared (*Contractual mechanics* below). To it the product adds four things that chassis does
not have: monthly crediting at the 공시이율 (*gongsi iyul*, declared rate) over a
최저보증이율 (*choejeo bojeung iyul*, guaranteed
floor); the 세액공제 (*seaek gongje*, tax credit) as a behavioural driver rather than an
insurer cash flow; the statutory 연금수령 conditions as constraints on the projection; and a
punitive 기타소득세 (*gita sodeukse*, other income tax) of 16.5% on any withdrawal that misses
them. 변액연금보험 (`VA_KR_S`), 즉시연금 (`Immediate_KR_S`) and the non-qualified 연금보험 are
out of scope and appear below as scope boundaries.

---

## Product overview and market role

연금저축 is not a product but a **tax wrapper defined by the income tax code**. A 연금저축계좌
(*yeongeum gyejwa*, pension account) is an account-opening contract with an authorised
financial institution under 소득세법 제20조의3제1항제2호 and 시행령 제40조의2제1항제1호 [R2]
[R6] [R11] [REG-R56]. Three institutional forms exist and are defined by the same article:
연금저축신탁, a trust contract with a bank; 연금저축펀드, a brokerage contract for
collective-investment securities; and **연금저축보험**, an insurance contract, writable by both
life and non-life insurers [R11] [R12] [S16]. The insurance leg is an actuarial object rather
than a savings account for one reason: it alone can pay a **life annuity**.

| | 연금저축신탁 (은행) | 연금저축펀드 (자산운용사) | 연금저축보험 (생보) | 연금저축보험 (손보) |
|---|---|---|---|---|
| 납입방식 | 자유납 | 자유납 | **정기납** | **정기납** |
| 적용금리 | 실적배당 | 실적배당 | **공시이율** | **공시이율** |
| 연금수령기간 | 확정기간 | 확정기간 | **종신, 확정기간** | 확정기간 (최대 25년) |
| 원금보장 | 보장 | 미보장 | 보장 | 보장 |
| 예금자보호 | 적용 | 미적용 | 적용 | 적용 |

Source: the standard 연금저축 비교공시 boilerplate [S16] and the supervisor's consumer guide
[R12]. 자유납 means the amount and timing are at the saver's discretion; 정기납 means a set
amount on a set cycle. The life-annuity asymmetry is stated by the supervisor in terms —
「생명보험사의 연금저축보험은 가입자가 연금을 종신으로 수령할 수 있도록 선택할 수 있으나,
손해보험사의 연금저축보험은 최대 25년까지 연금수령이 가능합니다」 [R12] — and the retrieved
non-life contract bears it out exactly: its only 연금지급형태 is a 정액형 over a 연금지급기간
of 5 to 25 years, with no life contingency and therefore no annuitant mortality anywhere in the
contract [S8].

**Fee *shape*, not merely fee level, differs by wrapper**, and it is what gives the insurance
leg its distinctive early-duration profile. Banks and asset managers charge on the accumulated
balance, so the charge grows with the fund; insurers charge on the **premium**, so the charge
is concentrated in the payment period and the early-duration return is negative [R12]. The
supervisor states the consequence for the consumer plainly: 「연금저축보험은 납입하신
보험료에서 사업비를 차감한 금액에 공시이율을 적용하여 적립되므로 계약 초기에는 마이너스(-)
수익률이 발생하여 계약해지시 환급금이 납입금액보다 적을 수 있으니 유의하시기 바랍니다」 [R12].
Every retrieved carrier document opens by insisting the contract is not a deposit — 「이 보험은
저축성보험으로 은행의 예⋅적금 및 펀드 등과 다른 상품입니다」 [S6] [S2].

**The block is the largest single wrapper by reserves and is shrinking in absolute terms.** At
end-2025, on the supervisor's own annual whitepaper and its press coverage [R13] [R22]:

| Measure | Value | Change on 2024 |
|---|---|---|
| 적립금 총계 | **₩198.2tn (198.2조원)** | +19.3조원 (+10.8%) |
| — 연금저축보험 | **₩114.1tn (114.1조원)**, 57.6% | **−1.2%** |
| — 연금저축펀드 | ₩61.3tn (61.3조원), 30.9% | +50.7% |
| — 연금저축신탁 | ₩13.8tn (13.8조원), 6.4% | −6.4% |
| 가입자 수 | **8.403m (840.3만명)** | +76.1만명 (+10.0%) |
| 계약건수 | 10.796m (1,079.6만건) | +107.9만건 (+11.1%) |
| 신규 계약건수 | 1.443m (144.3만건) | +51.9% |
| 납입액 | ₩13.5tn (13.5조원) | +18.1% |
| 연간 수익률 (전체) | **10.6%** | +6.9%p |
| — 펀드·ETF | 29.3% | |

Two derived figures shape the modelling. The average balance is **₩23,600,000 (2,360만원) per
saver** and **₩18,360,000 (1,836만원) per contract** `[derived]` from [R13] and [R22] — small
enough that the ₩15,000,000 aggregation threshold of the pension income tax binds on very few
savers, whichever payout term is chosen. And the insurance wrapper's reserves fell 1.2% in a
year in which fund reserves rose 50.7%: the product is a mature, slowly running-off block whose
new business is being written elsewhere in the same wrapper.

**What the product is *for* is the 세액공제.** Korea's individual-pension tax design is unusual
in this repository in two respects, and both are first-order behavioural drivers. First, relief
on the way in is a **tax credit**, not a deduction: a flat 12% or 15% of contributions up to a
cap (13.2% / 16.5% including the local income surtax), so the after-tax value of a contribution
does not rise with the marginal rate — it *falls*, because the higher-income band gets the
lower credit rate [R1] [R8] [R10] [REG-R56]. Second, the tax on the way out is a **withholding
tax banded by the age at which the annuity is taken**, with a further reduction to a flat rate
for a 종신계약 — a life annuity that cannot be surrendered [R5] [R9] [R11] [REG-R56]. That is a
tax code that pays the policyholder to annuitise late and for life. Against it stands a **16.5%
기타소득세** on any withdrawal that misses the statutory 연금수령 conditions [S1] [S2] [S3]
[S4] [S5] [S7] [S8] [S11] [S16], which is why the lapse assumption on this product cannot be
borrowed from a plain savings contract and has to be argued. Both are set out under
*Contractual mechanics* below.

**Underwriting is light or absent, and selection at issue is not a material feature.** The
state postal insurer writes the product 전건 무진단 [S7]; three other carriers reserve a right
to underwrite but describe no medical requirement [S1] [S2] [S8]. That follows from the benefit
design: no retrieved 연금저축보험 carries death cover in excess of the fund, so before
annuitisation there is almost nothing to select against. Issue ages start at **0** on four
contracts [S1] [S7] [S8] and at 만19세 on one [S11].

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | 무배당 연금저축보험 — deferred, level monthly 기본보험료, 금리연동형 | [S1] [S4] [S5] [S6] [S11]; pick **[std]** (1) |
| Statutory wrapper | 연금저축계좌 under 소득세법 제20조의3제1항제2호 and 시행령 제40조의2제1항제1호 | [R2] [R6] [R11] [REG-R56] |
| Supervisory class | 저축성보험 (감독규정 제1-2조제4호); 생명보험, 제1보험 | [REG-R9] [REG-R16]; [S2] [S6] state it |
| Rate class | 금리연동형보험 (감독규정 제1-2조제6호) — the 계약자적립액 rate varies monthly | [REG-R9] [S1] [S2] [S4] [S6] |
| Participation | 무배당 — no 계약자배당 | [S1] [S4] [S5] [S6] [S11]; pick **[std]** (1) |
| Lives basis | Single life; 계약자 = 피보험자 = 연금수익자 | envelope **[std]** (2) |
| Underwriting | None — 무진단, no material selection at issue | [S7]; adoption **[std]** (3) |
| Age basis | **보험나이** throughout the contract; **만나이** for the statutory 만 55세 test | [S6 제20조] [REG-R25 제21조](#krlib-reg-r25) |
| 가입나이 (issue age) | 0 ~ (연금개시나이 − 납입기간); **0–45** on the representative term | [S1] [S7] [S8]; envelope **[std]** (4) |
| 연금개시나이 | 만 55 ~ 80세, elected at issue; representative **65** | [S1] [S7] [S8] [S9] [S11]; pick **[std]** (5) |
| 납입기간 | 5 / 10 / 15 / 20년 / 전기납; representative **20년** | [S1]; pick **[std]** (5) |
| Gap 납입완료 → 연금개시 | **5 years** (age 60 to age 65) | **[std]** (5) |
| 연금개시전 보험기간 | Issue to the 연금개시나이 계약해당일 | [S1] [S2] [S4] [S6] |
| 연금지급기간 | Life, with a 10-year 보증지급기간 (base run); or 10 / 15 / 20 years certain | [S1] [S2]; pick **[std]** (11) |
| 기본보험료 | **₩500,000 a month (₩6,000,000 a year)** | band [S2]; anchor **[std]** (6) |
| 납입주기 | **월납**, in the contract and on the projection grid | [S1] [S2] [S6] [S7]; grid **[std]** (7) |
| 추가납입 | 연금저축추가납입특약, ≤ 200% of the year's basic premiums; **off in the base run** | [S2] [S5] [S7] [S8]; scope **[std]** (8) |
| Annual contribution ceiling | **₩18,000,000 (1,800만원)** across all 연금계좌 at every institution | [R6 제40조의2제2항제1호](#krlib-pension_savings-r6) [R11] [REG-R56] [S1] [S2] [S8] |
| Currency | KRW | all sources |
| 예금자보호 | **₩100,000,000 (1억원)**, in the 연금저축계좌 bucket, separate from the carrier's other 보험금 claims | [REG-R52 제18조제7항](#krlib-reg-r52) [REG-R32]; [S2] [S6] [S11] state ₩100,000,000 |
| **Anchor model cell** | Male, 보험나이 40 at issue; 기본보험료 ₩500,000 a month for 20 years to 보험나이 60 (₩120,000,000 cumulative); annuity from 보험나이 65; 종신연금형 with a 10-year guarantee; 공시이율 2.15%; no 추가납입, no policy loan | **[std]** (6) |

Footnotes to [std] rows:

1. **Participation.** Five of the eight retrieved 연금저축보험 are 무배당 [S1] [S4] [S5] [S6]
   [S11] and three are 배당 [S2] [S7] [S8]; one carrier sells both forms of the same product
   [S1] [S2]. The composite takes 무배당, for two reasons beyond the count. It is the form the
   surrender-charge cap penalises hardest — 별표 14 주5 gives a participating 연금저축보험 a
   coefficient of **4%** of the annual net premium and a 무배당 one **3%** [REG-R20] [R14] — so
   a 무배당 composite states the tighter constraint. And it removes a discretionary,
   unpublished cash flow: no retrieved carrier publishes a dividend *rate* on a 연금저축보험,
   and the only published dividend history is the postal insurer's 기준율, which fell from 4.3
   to **3.5** and whose aggregate fell 70% over 2022–2024 [S7]. A participating run is
   available as a parameterization (footnote 21) and is zero in the base run.
2. **Lives.** No retrieved 연금저축보험 약관 states a policyholder-insured-beneficiary identity
   condition, because the wrapper does not need one: the 연금저축계좌 is the taxpayer's own
   account and the 세액공제 accrues to the contributor [R1] [R11]. (The identity requirement
   that *does* exist in Korean tax law belongs to the **non-qualified** 종신형 연금보험 route
   of 소득세법 시행령 제25조제4항제4호 [REG-R58], which is a different product and is out of
   scope.) The composite nevertheless sets all three roles on one life, so that the annuitant
   mortality basis and the fund are attached to the same person and the model carries one age.
   The one retrieved case where the roles genuinely separate — an issue age of 0, where the
   contributing adult is not the insured [S1] [S7] [S8] — is excluded from the base run and
   noted under *Variations*.
3. **Underwriting.** 전건 무진단 at the postal insurer [S7]; a reserved right to underwrite on
   acceptance guidelines, with no stated medical requirement, at three others [S1] [S2] [S8].
   The composite carries **no selection, no substandard rating and no premium waiver**. The
   design justifies it: with the death benefit equal to the fund (see *Benefit provisions*),
   the insurer carries no mortality risk before annuitisation at all, and the only mortality
   risk in the contract is **longevity** risk from the annuity commencement date. A model that
   applies a select-mortality adjustment to this product is modelling a risk the contract does
   not run.
4. **Issue age.** Observed envelopes: **0세 ~ (연금개시나이 − 납입기간)** at two life carriers
   and one non-life carrier [S1] [S8], with the postal insurer at 0세 ~ (연금개시나이 − 5) [S7]
   and one direct carrier at 만19세 ~ (연금개시나이 − 납입기간) [S11]. One carrier publishes
   the matrix term by term — 5년납 0세~(Y−5), 10년납 0세~(Y−10), 15년납 0세~(Y−15), 20년납
   0세~(Y−20), 전기납 0세~(Y−5) with 가입나이 (Y−9) to (Y−6) barred — and adds the 보험나이
   rider: 「다만, 피보험자가 55세 계약해당일에 만55세 이상이 아닌 경우에는 연금개시나이를
   56세부터 선택할 수 있음」 [S1]. The composite adopts the general rule **0 ~ (Y − m)** and,
   on the representative Y = 65 and m = 20, the envelope **0–45**. The model point table
   exercises the envelope from the low twenties to 45.
5. **연금개시나이, 납입기간 and the gap interlock, and share one rationale.** 연금개시나이 is
   만 55 ~ 80세 at four carriers [S1] [S7] [S8] [S11] and 만55~80세 at a fifth [S9]; 65 is the
   age in every retrieved illustration [S2] [S11]. 납입기간 menus observed: 5 / 10 / 15 / 20년
   / 전기납 [S1]; 5 / 6 / 7년 이상 / 10 / 15 / 20 / 전기납 [S2]; 5년 ~ 전기납 [S7]; 15 / 20 /
   전기납 with a minimum of five years [S8]; 5 / 7 / 10 / 20 [S11]. The composite takes
   **20-year pay to 60 and annuity at 65**, which is the model point one carrier publishes its
   whole illustration set on [S2]. Three properties follow and are the reason for the choice.
   The premium term clears the statutory five-year account-age test [R6 제40조의2제3항제2호](#krlib-pension_savings-r6)
   with fifteen years to spare. The five-year gap between 납입완료 and 연금개시 is a real
   contractual state — premiums have stopped, the maintenance charge has not, and the fund is
   still accumulating — which a model that annuitises at 납입완료 cannot represent. And by 65
   the 연금수령연차 has reached 11, at which point the **연금수령한도 does not apply at all**
   [R6 제40조의2제4항](#krlib-pension_savings-r6) [S3]; the composite therefore projects an unconstrained annuity and
   states the constraint separately for the ages at which it binds.
6. **Anchor cell.** Premium rates for a Korean product are not public: the 예정이율, 위험률 and
   사업비율 live in the 산출방법서 (*sanchul bangbeopseo*, the calculation basis filed with the
   supervisor) [REG-R9] [REG-R18], and a full-text search of the retrieved 감독규정 returns
   **zero** occurrences of 예정이율 [REG-R48]. The anchor is therefore built on a **published
   illustration at an identical model point**: 남자 40세, 기본보험료 월 500,000원, 20년납, 60세
   완납, 65세 개시, on which one carrier publishes the fund at annuitisation (₩156,420,000 at a
   2.15% declared rate, ₩123,460,000 at the guaranteed floor) and the annuity under five forms
   on each basis [S2]. ₩500,000 a month sits inside that carrier's own band (월 12만 ~ 150만원
   for a term of seven years or more) [S2] and inside every other retrieved band [S1] [S7]
   [S11]. It is also **exactly the 세액공제 cap**: ₩6,000,000 a year is the maximum
   credit-eligible 연금저축 contribution [R1] [R8] [R10], so the anchor saver is at the corner
   of the tax schedule and the credit is a clean ₩990,000 a year at 16.5% or ₩792,000 at 13.2%
   [S11] `[derived]`. Male, because the annuity factor differs materially by sex on this
   product (footnote 13) and the male factor is the one the published illustration gives.
7. **Grid.** Every retrieved contract is 월납 [S1] [S2] [S6] [S7] [S11], one adding 연납 [S8],
   and interest accrues **by day from the date each premium is received** — 「순보험료 … 를
   「공시이율」로 납입일부터 일자계산을 하여 적립한 금액」 [S1] [S2], with 감독규정
   제7-66조제1항제4호 accruing the account **monthly before 납입완료** [REG-R19].
   `Pension_KR_S` runs a **monthly** grid, so each instalment is allocated as the ₩500,000 the
   contract collects and the account is credited at `(1 + 공시이율)^(1/12) − 1` a month. The
   **[std]** in the grid is now only that: the day-count inside the month is not modelled, and
   the assumptions stay annual with uniform-force monthly conversions, both specified in
   `technical-notes.md`. The earlier annual grid ran instead under the separate permission of
   감독규정 제7-65조제2항 — 「계약자적립액은 … 연납보험료를 기준으로 하여 산출할 수 있다」
   [REG-R18], a filed-basis convention rather than a shortcut — which the monthly grid no
   longer needs. What the monthly grid still collapses is the sub-annual grace and demand
   mechanics, now into the month rather than the year; footnote 20.
8. **추가납입.** Written through a 제도성특약, the 연금저축추가납입특약, capped at **200% of
   the year's basic premiums** [S2] [S5] [S8] and payable from a stated point after inception
   to a stated point before annuitisation — 「계약일 이후 [n]개월이 지난 후부터 연금개시나이
   [n]세 계약해당일까지」 [S7], 「「연금지급개시나이−2년」 까지」 [S5] — always inside the
   ₩18,000,000 aggregate [S2] [S7] [S8]. It bears a **different and much lighter charge**: the
   additional premium is deducted only for 계약관리비용, not for 계약체결비용 — 「적립순보험료
   : 기본보험료에서 계약체결비용 및 계약관리비용을 공제한 보험료와 추가납입보험료에서
   계약관리비용을 공제한 보험료」 [S8] — at 2.0% [S1] or 0.8% [S7] of the additional premium.
   The composite carries the rider as a **model-point field, zero in the base run**, because
   its cash flow is a different function of premium and merging it into 기본보험료 would
   misstate the expense recovery.

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium basis | Level 기본보험료, guaranteed for the whole 납입기간; no reviews | [S1] [S2] [S4] [S6] [S7] |
| 기본보험료 | ₩500,000 a month, ₩6,000,000 a year, 20 years | anchor **[std]** (6) |
| 계약체결비용 (acquisition) | **1.50% of 기본보험료 a month for the first 7 policy years** | [S1]; adoption **[std]** (9) |
| 계약관리비용 (maintenance) | **3.00% of 기본보험료 a month to policy year 20; 0.67% thereafter** | [S1]; adoption **[std]** (9) |
| Total loading | **4.50%** of premium in years 1–7; **3.00%** in years 8–20; **0.67%** after | [S1] |
| 순보험료 (allocated) | 기본보험료 less both charges, credited from the payment date | [S1] [S2] [S8] |
| 모집수수료 (commission) | **0.00% in every year** — a direct-channel product | [S1]; adoption **[std]** (9) |
| 연금수령기간 관리비용 | **0.5% of the 연금연액**, deducted in payment | [S1] [S7]; adoption **[std]** (10) |
| 추가납입 계약관리비용 | 2.0% of the additional premium; nil in the base run | [S1]; scope **[std]** (8) |
| 공시이율 (crediting rate) | **2.15% p.a.**, reset monthly, fixed for the calendar month | [S2]; adoption **[std]** (12) |
| 최저보증이율 (floor) | **1.25%** to 5 years; **1.00%** over 5 to 10 years; **0.50%** over 10 years — compound annual | [S1] [S2] [S13]; adoption **[std]** (12) |
| 보장부분 적용이율 / 예정이율 | **2.50% 연복리**, used to price the expense and benefit structure; **not** a guarantee | [S1] [S5] [S7] |
| 평균공시이율 (2026) | **2.50%** — a supervisory illustration and discounting constraint, not a crediting rate | [REG-R48] [S2] [S14] |
| 세액공제 rate | 15% where 종합소득금액 ≤ ₩45,000,000 (총급여 ≤ ₩55,000,000), else 12%; **16.5% / 13.2%** including the local surtax | [R1 제59조의3제1항](#krlib-pension_savings-r1) [R8] [R10] [REG-R56] (13) |
| 세액공제 한도 | **₩6,000,000** a year to 연금저축; **₩9,000,000** including 퇴직연금계좌 | [R1] [R8] [R10] [REG-R56] |
| 보험계약대출 (policy loan) | Available within the surrender value; rate not published by any retrieved carrier. **Off in the base run** | [S1] [S2] [S4] [S5] [REG-R25 제33조](#krlib-reg-r25); scope **[std]** (14) |
| 납입유예 (payment holiday) | Up to 3 spells of 1 year at one carrier; charges still taken from the fund; premium dates and the annuity date deferred. **Off in the base run** | [S5] [S7] [S8]; scope **[std]** (14) |
| Refund on a void contract | Premiums returned with interest at the 보험계약대출이율 | [S1] |

9. **Expenses.** Only two retrieved 연금저축보험 publish a complete charge schedule, and the
   two are shaped differently — which is itself the finding. The direct-channel product charges
   a **level monthly percentage and no surrender penalty at all**: 계약체결비용 1.50% of
   기본보험료 a month for seven years, 계약관리비용 3.00% a month for twenty years then 0.67%,
   **해약공제액 0.0% at every duration**, and a 모집수수료율 of **0.00% in every year** [S1].
   The postal product charges less per month in the long run and adds a front-end surrender
   penalty that runs off over four years: 판매보수 1.22% a month for ten years, 유지보수 1.8% a
   month for seven years, 계약관리비용 3.0% a month throughout, and a 해지공제액 of ₩104,000 at
   year 1 falling to zero at year 5 [S7]. First-year totals are **4.50%** and **6.02%** of
   premium respectively `[derived]`; the supervisor's own market rule of thumb, from a 2015
   guide, is 「납입보험료 대비 9%」 over a ten-year payment term [R12], above both. The
   composite adopts the **first** schedule in full — the only complete, currently sold,
   2026-vintage schedule retrieved — for three reasons: it is internally consistent with a zero
   surrender charge, which removes an unpublished amortisation pattern from the model; its 0.5%
   annuity-phase charge reconciles the published certain-annuity factors to three or four
   significant figures (footnote 10);
   and a zero commission rate means the expense schedule is the whole acquisition cost, with no
   unpublished remainder. The cost of the choice is stated openly under *Variations*: the
   composite's early-duration surrender values will look like the direct-channel product's
   (95.9% of premiums at three months) and **not** like the tied-channel product's (43.4%) [S1]
   [S2], even though the anchor model point is taken from the latter. The alternative schedule
   is a model input, not a rewrite.
10. **The annuity-phase charge is a carrier choice, not a market convention, and the composite
    picks the one that is provable.** Two carriers disclose 「연금수령기간 중의 관리비용:
    연금연액의 0.5%」 [S1] [S7]. Dividing one carrier's published fund at annuitisation by its
    published certain annuities recovers implied factors of 9.06, 12.92 and 16.39 at 10, 15 and
    20 years against textbook annuity-due factors of 9.104, 12.978 and 16.464 at the same 2.15%
    — a ratio of **0.995 at all three terms** `[derived]` from [S2]. That is the 0.5% charge.
    A second carrier's five certain-annuity terms give a uniform ratio of **1.006** in the
    *other* direction — a small uplift, consistent with that carrier disclosing no
    annuity-phase charge [S5] `[derived]`. The composite takes 0.5%.

    The residual ratio against the *annual* annuity-due is not a second charge, and the
    technical notes resolve it rather than carrying it: **the instalments are monthly**, so
    the factor is the annuity-due payable twelve times a year. Using `(1 − v^n)/d^(12)` on
    the certain form, and the annual life factor less 11/24 on the life form, with this same
    0.5% charge and nothing else, reconstructs **eight** published implied factors across
    **two** interest bases — 확정 10/15/20년 at 9.061 / 12.918 / 16.386 against a published
    9.06 / 12.92 / 16.39 at 2.15%, and 9.806 / 14.528 / 19.134 against 9.81 / 14.53 / 19.13
    at the 0.5% floor, with 종신 10년보증 남 65 at 23.700 against 23.70 and 31.180 against
    31.18. See [Technical Notes](technical-notes.md).
11. **Annuity form.** See *Benefit provisions — payout phase* and footnote 15.
12. **Rates.** The declared rate is set monthly and fixed for the calendar month — 「공시이율은
    매월 1일에 회사가 정한 이율로 하며, 매월 1일부터 당월 마지막 날일까지 1개월간 확정
    적용합니다」 [S1] [S2] [S4 제6조①] [S5] [S6]. Observed levels on 연금저축 books: **3.01%**
    and **2.82%** at one carrier on 2026-09-01 [S12], **2.40%** at 2026-01 [S1], **2.15%** at
    2025-12 [S2], **2.3%** at 2024-10 [S11] and 2.98% at 2016-03 [S5]; the current market range
    is roughly **2.1% to 3.0%**, with older books at the top and a 19bp spread between two
    vintages inside one carrier on the same date [S12] `[derived]`. The composite takes
    **2.15%**, the rate on which the anchor illustration and every derived annuity factor of
    footnote 10 are struck [S2] — the conservative arm of the range, and the only choice under
    which the published fund, the published annuities and the reconstructed factors are one
    consistent set. Guarantee ladders observed, all compound annual and all stepping *down*
    with elapsed duration: **1.25 / 1.00 / 0.50** at 5 and 10 years [S1] [S2] [S13]; **1.25 /
    1.00 / 0.75** [S15]; **1.0 / 0.5** at 10 years [S6] [S7] [S11]; **1.5 / 1.0** at 10 years
    [S5] [S13]; **2.0 / 1.5** at 10 years on an older generation [S9]; **1.0 / 0.75 / 0.5** at
    3 and 5 years [S4]; and **1.25 / 1.0 / 0.3** on the non-life form [S8]. The observed
    first-band range is **1.0%–2.0%** and the long-duration range **0.3%–1.5%**. The composite
    takes the modal current shape, **1.25 / 1.00 / 0.50**. Two structural facts are carried
    into the model with it: the ladder is a function of **sale date, not of carrier** — one
    carrier's shelf runs two ladders side by side by 판매개시일 [S13] — and the floor is a
    guarantee on the **credited rate**, not on the return, so expenses are still deducted
    beneath it: 「공시이율을 적용하여 적립하는 금액은 공시이율이 0.25%인 경우,
    공시이율(0.25%)이 아닌 최저보증이율 … 로 적립됩니다」 [S4] [S8]. A 최저보증이율 is not
    optional: 감독규정 제7-60조제10호 requires every 금리연동형보험 to set one [REG-R16].
13. **Credit rates.** The statutory rates are **12%** and **15%** [R1 제59조의3제1항](#krlib-pension_savings-r1) [R8]
    [REG-R56]. The 13.2% and 16.5% every Korean consumer document quotes are those figures
    grossed up by the 10% 지방소득세 surtax; the supervisor states the grossed-up pair directly
    [R10], and five carrier documents repeat it [S5] [S11] [S16] [S1] [S2]. The surtax is
    imposed by the 지방세법, which was **not retrieved** in either research pass, so the
    grossed-up pair is **[unverified] arithmetic on a verified base** [REG-R56] and this
    document says so wherever it uses it.
14. **Optional modules, off in the base run.** The **policy loan** exists on the product and
    interacts with the tax rules — one carrier sets the medical-withdrawal limit
    「보험계약대출이 있는 경우, 원금과 이자 상환 및 연금외수령으로 일시에 인출할 때 기타소득세
    원천징수액을 고려하여 회사가 정하는 범위 내로」 [S2] — but **no retrieved document gives a
    numeric 보험계약대출이율 for a 연금저축보험** [S1] [S2] [S4] [S5], so a base-run rate would
    be invented. The **payment holiday** is standard and generous: up to three spells of one
    year at the non-life carrier [S8], available after three years at two others [S5] [S7],
    with the charges still deducted monthly from the fund and both the premium due dates and
    the annuity date deferred by the length of the holiday; the holiday ends prematurely if the
    fund cannot bear the deduction, at which point the ordinary demand process starts [S7]
    [S8]. Both are implemented as switchable modules and are off in the base run, so the base
    projection has one premium state and one lapse decrement.

### Benefit provisions — deferral phase

| Parameter | Representative value | Basis |
|---|---|---|
| 계약자적립액 | 순보험료 accumulated at the 공시이율, floored at the 최저보증이율, computed per the 산출방법서 | [S1] [S2] [REG-R18 제7-65조](#krlib-reg-r18) |
| Death benefit before annuitisation | **The 계약자적립액 at the date of death**; the contract then ends | [S1] [S2] [S4] [S6] |
| Death cover above the fund | **None** | [S1] [S2] [S4] [S6]; adoption **[std]** (15) |
| Why none is required | 감독규정 제7-60조제9호 requires a death benefit of at least cumulative premiums **except where the premium term ends at 80 or below** — here it ends at 60 | [REG-R16 제9호](#krlib-reg-r16) |
| Return-of-premium floor on death | Present at one carrier; **not adopted** | [S7]; scope **[std]** (15) |
| 해약환급금 | **계약자적립액 − 해약공제액**, floored at zero | [S1] [S8] [REG-R19 제7-66조제1항제1호](#krlib-reg-r19) |
| 해약공제액 (surrender charge) | **Zero at every duration** | [S1]; adoption **[std]** (9) |
| 표준해약공제액 cap | 연납순보험료 × **3%** × min(납입기간, 12) for a 무배당 연금저축보험, less 별표 14 주6's discounted loading | [REG-R20 주2·주5·주6](#krlib-reg-r20) [R14] |
| — computed on the composite | ≈ **₩1,420,000**, about 2.8 months of 기본보험료 — headroom the composite does not use | **[std]** (16) |
| 해약공제기간 | The premium term or the acquisition-cost loading period, **capped at 7 years** | [REG-R19 제7-66조제1항제2호](#krlib-reg-r19) |
| 미경과보험료 | Added to the surrender value on termination | [REG-R19 제7-66조제5항](#krlib-reg-r19) |
| Fund floor at 연금개시 | **100.1% of premiums paid** | [S2] [S4] [S7]; adoption **[std]** (17) |
| — disapplication | Withdrawn, and the annuity date deferred instead, where a payment holiday or a one-instalment reinstatement caused the shortfall | [S4] [S6] [S7] |
| Surrender after the first annuity payment | **Not available** on a 종신연금형 | [S2] [S4] [S5] [S9] [S10] |
| 계약이전 (transfer out) | Permitted to another 연금저축 or to an IRP; **not** a withdrawal and not taxed | [S1]; scope **[std]** (18) |

15. **There is no death cover on this product, and that is a design fact rather than an
    omission.** Every retrieved life-insurer 연금저축보험 pays the fund and nothing more:
    「피보험자가 연금개시전 보험기간 중 사망한 경우에는 사망 당시의 계약자적립액을 지급하여
    드리고 이 계약은 더는 효력이 없습니다」 [S1] [S2] [S4] [S6]. The postal insurer adds a
    return-of-premium floor — 「사망시 지급금액이 이미 납입한 보험료보다 적은 경우에는 이미
    납입한 보험료를 계약자에게 지급합니다」 [S7] — and it is the only retrieved contract that
    does. The composite does **not** adopt it, because the regulation that would otherwise
    force it does not apply: 감독규정 제7-60조제9호 requires a death benefit of at least
    cumulative premiums paid **except after annuity payments have begun and except where the
    premium-paying period ends at age 80 or below** [REG-R16], and the composite's premium term
    ends at 60. The consequence for the model is exact and should be stated as a testable
    property: **before annuitisation the insurer carries no mortality risk on this product at
    all**, because the death payment equals the surrender payment equals the fund. Mortality
    enters `Pension_KR_S` in one place only — the annuity factor at the commencement date — and
    a projection that applies a decrement-weighted death strain in deferral is projecting a
    strain of exactly zero. The floor variant is carried as a model-point flag so the postal
    design can be run.
16. **The statutory surrender-charge cap, computed on the composite.** 별표 14 gives
    표준해약공제액 = 연납순보험료의 5% × 해약공제계수 + 보장성보험의 보험가입금액의 10/1000,
    with 주2 setting the coefficient for a 저축성보험 at the **premium term capped at 12**, 주3
    defining the annual net premium as the annual premium less the average loading spread
    evenly over the **payment term capped at 10 years**, 주5 replacing the 5% with **4% for a
    연금저축보험 and 3% for a 무배당 연금저축보험**, and 주6 subtracting the acquisition amount
    loaded into the premium **discounted at the 평균공시이율** [REG-R20] [R14]. Note that 주4's
    6% concession for a whole-of-life survival annuity is expressly **denied** to a
    연금저축보험, and that the second term of the formula is nil here because the contract has
    no 보장성 element. On the composite's own published loading — ₩270,000 a year for seven
    years and ₩180,000 for thirteen, ₩4,230,000 in total, levelled over ten years at ₩423,000 —
    the annual net premium is ≈ **₩5,577,000**, the cap before 주6 is 3% × ₩5,577,000 × 12 ≈
    **₩2,007,700**, and 주6 removes the ₩90,000-a-year acquisition loading discounted over
    seven years at the 2026 평균공시이율 of 2.50%, ≈ **₩585,700**, leaving ≈ **₩1,422,000**
    `[derived]` **[std]** on the reading of 주3 that levels the whole-term loading over the
    ten-year cap. (The alternative reading — levelling only the first ten years' loading —
    gives ₩5,757,000, ₩2,072,500 and ₩1,486,800. The two differ by 4.6% and neither is excluded
    by the text; `technical-notes.md` carries the definitive computation and the switch.) Three
    things follow. The cap is **about 2.8 months of 기본보험료**, the order of magnitude
    금융위원회 stated for a 저축성보험 in 2019 [REG-R29]. The composite's whole acquisition
    cost — 1.50% × ₩500,000 × 84 = **₩630,000** — is well inside it, which is a coherent
    explanation of why the source product's published 해약공제 table is all zeros [S1]. And the
    postal insurer's ₩104,000 first-year charge on a ₩1,200,000 annual premium, **8.7% of
    premiums paid**, scales to ₩520,000 on the anchor premium and is likewise well inside [S7]
    `[derived]`. The cap binds nothing on this product; it is stated because it bounds the
    design space and because `technical-notes.md` must implement the floor of 감독규정
    제7-66조제1항제1호 — a surrender value net of the deduction may not go negative and is set
    to zero [REG-R19].
17. **The 100.1% floor is a real, if shallow, maturity guarantee, and it belongs in the
    model.** Three retrieved contracts guarantee the fund at annuitisation at **100.1% of
    premiums paid** — 「연금개시시의 계약자적립액은 이미 납입한 보험료의 100.1%를 최저보증
    합니다」 [S4 별표1 주10] [S2] [S7] — and two more state the functionally identical 「이미
    납입한 보험료
    + 1,000원」 [S5] [S6 별표1 주4]. Why 100.1% rather than 100%: 감독규정 제7-60조제2호
    requires a 저축성보험's survival benefits to **exceed** premiums paid [REG-R16], so a
    nominal one-tenth of one per cent discharges the definition, and two carriers make the link
    explicit [S7] [S8]. The composite adopts it, with the two published disapplication triggers
    — a payment holiday, and a one-instalment reinstatement — under which the guarantee is
    **withdrawn and the annuity date deferred instead** [S4] [S6] [S7]. It is not decorative:
    on the anchor illustration the guaranteed-rate basis reaches only **100.5% of premiums** at
    the end of the twenty-year payment term [S2], so on a persistently low-rate scenario the
    floor is close to binding, and it is the only element of this product that behaves like an
    option rather than an account.
18. **계약이전 (계좌이체).** The saver may move the contract to another 연금저축 at the same or
    a different institution, or to an 개인형퇴직연금 (IRP); a transfer is **not** a withdrawal
    and attracts no income tax — 「계좌이체하는 경우 관련세법에 따라 연금계좌의 인출로 보지
    않으므로 소득세가 부과되지 않습니다」 — with one exception, that moving a post-2013-03-01
    연금저축 into a pre-2013-03-01 one **is** treated as a withdrawal and is taxed [S1]. A
    lapsed contract whose surrender value has not been taken may be transferred **without first
    being reinstated** [S1]. Five transfers are refused — a breach of the receiving
    institution's contribution ceiling, a split by amount, an attachment or pledge, a
    종신연금형 already in payment (or a disability annuity, a running premium waiver or an
    unresolved claim), and an IRP transfer from a holder under 만 55세 or an account less than
    five years old — and the carrier may charge a fee on the transfer [S1]. **Transfer is out
    of scope of the base run** and is not a lapse:
    it is a movement of the same tax-recognised balance between wrappers. Its existence matters
    to the lapse assumption, because part of what looks like termination on an insurer's book
    is transfer to a 연금저축펀드 — which is exactly the direction the market moved in 2025
    (funds +50.7%, insurance −1.2%) [R13] [R22].

### Benefit provisions — payout phase

| Parameter | Representative value | Basis |
|---|---|---|
| 연금개시일 | The 계약해당일 on which 보험나이 reaches the elected 연금개시나이 (65) | [S1] [S2] [S6] |
| Base annuity form | **종신연금형 (정액형) with a 10-year 보증지급기간** | menu [S1] [S2] [S4] [S6] [S9] [S11]; pick **[std]** (19) |
| Alternative elected at annuitisation | **확정기간연금형** at 10 / 15 / 20 years | [S1] [S2]; menu **[std]** (19) |
| 종신연금형 basis | 연금사망률 **and** 공시이율, per the 산출방법서 | [S1] [S2] [S6] |
| 확정기간연금형 basis | **공시이율 only** — no mortality | [S1] [S2] [S6] |
| 확정기간연금형 formula | 연금연액 = 계약자적립액 ÷ ä<sub>n</sub><sup>(12)</sup>(공시이율) × (1 − 0.005) — the annuity-due payable **monthly**, footnote 10 | `[derived]` from [S2]; adoption **[std]** (10) |
| 종신연금형 formula | 연금연액 = 계약자적립액 ÷ [ä<sub>x</sub><sup>(g)</sup>(연금사망률, 공시이율) − 11/24] × (1 − 0.005) | [S1] [S2] [S6]; **[std]** (10) |
| Implied factor, male 65, 2.15%, 10-year guarantee | **23.70** | `[derived]` from [S2] |
| Implied factor, male 65, 2.15%, 20-year guarantee | 24.14 | `[derived]` from [S2] |
| Implied certain factors, 2.15% | 9.06 / 12.92 / 16.39 at 10 / 15 / 20 years | `[derived]` from [S2] |
| Annuitant mortality vintage | Struck on the **가입시점** table, with a one-way ratchet to the **연금개시시점** table where a revision *increases* the annuity | clause [S1] [S2] [S4] [S6] [S9]; reading `[derived]` **[std]** (20) |
| Instalment frequency | 매월 / 매3개월 / 매6개월, with deferred instalments credited at the 공시이율; **매월** on the projection grid, which pays `연금연액 ÷ 12` a row | [S1] [S2] [S5] [S6] [S7]; grid **[std]** (7) |
| Death inside the guarantee period | The unpaid guaranteed instalments are paid, and may be commuted at the 공시이율 | [S1] [S2] [S6] |
| Death after the guarantee period | Nothing further; the contract ends | [S1] [S2] [S6] |
| Death during a 확정기간 term | The remaining instalments are paid to the count (10 / 15 / 20회) | [S1] [S2] [S4] [S6] |
| Guaranteed total vs the fund | The guaranteed instalments may total **less** than the fund at annuitisation | [S1] [S2] [S6] |
| Contributions after annuitisation | Barred | [R6 제40조의2제2항제2호](#krlib-pension_savings-r6) |
| 상속연금형 | **Not offered** on any retrieved 연금저축보험 | [S1]–[S9] [S11]; treat as absent (19) |

19. **Annuity menus, and why the composite takes a ten-year-guaranteed life annuity.** Observed
    종신연금형 guarantee periods: **10 and 20 years** [S1] [S2]; 10, 20 and 100세 [S4] [S9]
    [S11]; 10, 20 and 30 years [S6]; **20 years only** at the postal insurer [S7]; 10, 20, 30
    and 100세 illustrated at a sixth [S5]; and **none at all** on the non-life form, which has
    no life annuity [S8]. Observed 확정기간연금형 terms: 10 / 15 / 20 [S1] [S2] [S7]; 10 / 15 /
    20 / 25 / 30 [S6] [S11]; 5 / 10 / 15 / 20 / 30 [S5]; 5 / 10 / 15 / 20 / 25 / 30 [S9]; and a
    single 정액형 over 5 to 25 years on the non-life form [S8]. Three carriers allow the fund
    to be **split** across forms, one in 10% units summing to 100% [S6 제19조⑤] [S4 별표1 주7]
    [S2]; the split is out of scope. "100세 보증" is not a century: 「"100세"란 "101세
    계약해당일의 전일까지"를 말합니다. 즉, "100세 보증형"이란 "101세−연금개시나이"년
    보증형입니다」 [S10], which for a 65-year-old is a **36-year** guarantee, and one carrier
    confirms the age basis is the insured's [S4 별표1 주8]. The composite takes **종신연금형
    with a 10-year guarantee** as the base form — the only guarantee period offered by every
    retrieved life carrier that writes a life annuity at all, and the shortest, so the
    composite states the least generous of the observed options — with **확정기간연금형 10 / 15
    / 20** as the election. The cost of lengthening the guarantee is small and readable
    directly from the illustrations: 10 to 20 years costs **1.8%** of the annuity for a
    65-year-old male (660 → 648만원) `[derived]` from [S2], and 10 to 40 instalments costs
    **7.7%** for a 60-year-old female (457 → 422만원) `[derived]` from [S5]. **상속연금형** —
    an inheritance annuity paying interest only and returning the fund on death — is absent
    from all eight retrieved 연금저축보험 and appears only in the variable-annuity taxonomy
    [S10]; the reason is structural, since a form that preserves principal indefinitely sits
    badly with the 연금수령한도 test. "상속연금형 is available on a 연금저축보험" is treated as
    **not established, and on this evidence probably false**.
20. **Which vintage of the annuitant table the factor is struck on.** This is the single
    question on which the payout phase turns, and the evidence settles it only by inference, so
    the composite states its reading and its status. Six independently retrieved contracts
    carry the **same clause**, with each carrier's own name for the table substituted:
    「종신연금형의 경우 연금개시전에 **연금사망률의 개정 등에 따라 연금연액이 증가하게 되는
    경우** 연금개시시점의 연금사망률 및 계약자적립액을 기준으로 산출방법서에 따라 계산한
    연금연액을 지급합니다」 [S1 주6] [S2], and the same in [S4 별표1 주11], [S6 별표1 주10],
    [S9 별표2 주9] and [S10 주4]. Every version shares two operative elements: the trigger is a
    revision that **increases** the annuity, and the substituted basis is the table **연금개시
    당시**. The clause is therefore a **one-way ratchet in the policyholder's favour**, which
    means the base factor must be something else — and the only candidate is the annuitant
    mortality in the 산출방법서 filed for the product, i.e. the table **as at 가입**. That
    reading is corroborated three ways: two carriers publish the 연금사망률 itself in the
    상품요약서 handed over **at inception** [S1] [S7]; and the trade press states in terms that
    a 경험생명표 revision applies to new business only — 「개정된 생명표는 신규 가입자에만
    적용되며, 기가입자는 보험료 변동 영향을 받지 않음」 [R18], 「기존 가입자는 가입 당시
    경험생명표를 바탕으로 이미 보험료가 결정돼 있어 영향을 받지 않는다」 [R20] — although both
    speak about the *premium*, not the annuity factor, so they corroborate without settling.
    Since successive revisions have **lightened** mortality (the 제10회 table raised 평균수명
    by 2.8 years for men and 2.2 for women [R18] [REG-R33] and cut the monthly annuity on a
    fixed fund by roughly **15%** [R19]), a revision normally *decreases* the annuity, the
    ratchet does not bite, and the annuitant keeps the issue-date factor. **The composite
    therefore strikes the factor on the 가입시점 table and carries the ratchet as an option
    that is out of the money in the base run.** The reading is `[derived]`, not stated by any
    retrieved document; carriers differ in how they name the table (연금사망률, 무배당 경험
    개인연금사망률, 경험 연금사망률, 연금생명표, 예정 개인연금 생존·사망률, 개인연금사망률 [S1]
    [S6] [S5] [S9] [S10] [S7]) but not in the clause. A model that struck the factor on the
    개시시점 table instead would understate the annuity, and a model that ignored the ratchet
    entirely would be right in the base run and wrong under an improvement scenario;
    `Pension_KR_S` exposes the vintage as a switch and `technical-notes.md` shows both.

### Options

| Parameter | Representative value | Basis |
|---|---|---|
| Annuitisation election | One binary at the 연금개시일: 종신연금형 10년보증 (default) versus 확정기간연금형 10년 | [S1] [S2]; scope **[std]** (21) |
| When the form may be elected or changed | Set at issue and changeable to the day before the 연금개시일 at three carriers; only after 납입완료 at a fourth; at annuitisation only at a fifth | [S6 제16조·제19조④] [S11] [S10 주9] [S2] [S5]; adoption **[std]** (21) |
| 연금개시나이 change | Electable to the day before the annuity date, in whole years | [S2] [S8 제3조④] |
| 자유설계연금형 (fund split) | Available at three carriers in 10% units; **out of scope** | [S6] [S4] [S2]; scope **[std]** (21) |
| Commutation of unpaid guaranteed instalments | On death, discounted at the 공시이율; prospectively on one contract | [S2] [S10 주7]; scope **[std]** (21) |
| 연금저축추가납입특약 | Optional module, off in the base run | [S2] [S5] [S7] [S8]; scope **[std]** (8) |
| 납입유예 / 납입일시중지 | Optional module, off in the base run | [S5] [S7] [S8]; scope **[std]** (14) |
| 보험계약대출 | Optional module, off in the base run | [S1] [S2] [S4] [S5]; scope **[std]** (14) |
| 의료비인출 | Described, not modelled — a withdrawal taxed as pension income **even above the 연금수령한도** | [S3 제21조②] [S1] [S7] [S8] |
| 부득이한 사유 인출 | Described, not modelled — six statutory reasons, claimed within six months | [S3 제21조④⑥] [S1] [S7] |
| 배우자 승계 (spouse succession) | Described, not modelled | [S1] [S3 제21조⑤] [S6] [S7] [S8] |
| 계약이전 / 계좌이체 | Described, not modelled | [S1]; scope **[std]** (18) |
| 납입면제 (premium waiver) | **None** — 「보험료 납입면제 사유 : 없음」 | [S5]; adoption **[std]** (22) |
| 계약자배당 | None (무배당 composite); machinery retained and set to zero | [S1]; **[std]** (1) |

21. **Election machinery varies widely and is modelled as a single binary.** *When* the form is
    chosen is a real design variable and the retrieved contracts do not agree: set at issue and
    changeable up to the day before the annuity date [S6 제16조·제19조④] [S11] [S10 주9];
    changeable **only once the premiums are fully paid** — 「계약자는 보험료납입이 완료된
    계약에 한하여 연금개시전에 연금지급형태를 변경할 수 있습니다」 [S2]; or set at issue as a
    종신연금형 only, with a change to 확정기간연금형 permitted at the annuity start date [S5],
    on a leaflet whose own two statements are in tension about *when* the change may be made
    and neither of which is a 약관. The composite implements **one election, exercised at the
    연금개시일**, between 종신연금형 with a 10-year guarantee and 확정기간연금형 over 10 years,
    with a **[std]** take-up assumption specified in `technical-notes.md`. That placement is
    deliberate: the tax code prices the election (a 종신계약 draws the lowest withholding band
    [R5] [R9] [R11] [REG-R56]) and the election is the only point in the contract at which the
    policyholder's decision changes the insurer's risk from none to longevity. Excluded, and
    each for a stated reason: the **fund split** across two forms [S6] [S4] [S2], which would
    require a joint payout state and is offered by only three of eight carriers; **prospective
    commutation** of guaranteed instalments by a living annuitant, retrieved only on a variable
    annuity [S10 주7]; and the annuity-date change [S2] [S8], which is a re-projection rather
    than a cash flow.
22. **No premium waiver.** One carrier states it flatly — 「보험료 납입면제 사유 : 없음」 [S5]
    — and no retrieved 연금저축보험 약관 carries one. A second carrier's transfer restrictions
    contemplate a 장해연금 and a 납입면제 on *some* 연금저축 contracts [S1], so the feature
    exists somewhere in the market, but it is absent from every retrieved product's own terms
    and the composite excludes it. This is consistent with the absence of underwriting
    (footnote 3): a waiver is a disability benefit, and a contract that does not underwrite
    health does not usually sell one.

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| 청약철회 (cooling-off) | **15 days** from receipt of the 보험증권 and never after **30 days** from the application; effective on dispatch; premiums returned within 3 business days | [REG-R51 제46조제1항제1호](#krlib-reg-r51) [REG-R25 제17조](#krlib-reg-r25); [S2] [S5] state 15/30 |
| 품질보증해지 | **3 months** from formation where the 약관 was not delivered or explained or the application was not signed; premiums returned with 보험계약대출이율 interest | [REG-R25 제18조제3항](#krlib-reg-r25) [S2] [S5] [S7] |
| 계약 전 알릴 의무 (disclosure) | Termination barred after **2 years** from the cover start (**1 year** for disease in a 진단계약), or **3 years** from the contract date, or **1 month** from the insurer learning of the breach | [REG-R25 제13조·제14조](#krlib-reg-r25); [S1] states 2 years / 1 year |
| 사기에 의한 계약 | Cancellable within **5 years** of the cover start and 1 month of discovery | [REG-R25 제15조](#krlib-reg-r25) [S1] [S7] |
| 납입최고 (demand) | At least **14 days**; the contract terminates the day after the period ends | [REG-R25 제26조](#krlib-reg-r25) [S2]; the postal insurer uses a longer window (23) |
| 실효 (lapse) | Effect lost the day after the demand period ends | [S2] [REG-R25 제26조](#krlib-reg-r25) |
| 부활 (reinstatement) | Within **3 years** of termination, where the surrender value has not been drawn; arrears with interest, capped at 평균공시이율 + 1% | [REG-R25 제27조](#krlib-reg-r25) [S7] [S8] |
| 간편부활 (one-instalment reinstatement) | Pay one month's basic premium; the lapsed months' charges are taken from the fund, with any shortfall paid in; the annuity date shifts and the 100.1% floor is withdrawn | [S1] [S5] [S7] [S8]; scope **[std]** (23) |
| Surrender before annuitisation | Available at any time; proceeds taxed as 기타소득 at **16.5%** | [S4] [S5] [S8]; and see *Contractual mechanics* |
| Surrender after annuitisation | Barred on a 종신연금형 | [S2] [S4] [S5] [S9] [S10] |
| Expiry | On the last guaranteed instalment where the annuitant has died; on the annuitant's death after the guarantee; on the last certain instalment on a 확정기간연금형 | [S1] [S2] [S6] |
| Late-payment interest on benefits | 보험계약대출이율 for 30 days, then **+4.0%**, **+6.0%**, **+8.0%** in successive 30-day bands | [S4 별표2] |
| 소멸시효 | 3 years | [REG-R25 제37조](#krlib-reg-r25) [REG-R49 제662조](#krlib-reg-r49) |

23. **Grace, lapse and reinstatement, and what the projection grid keeps.** The standard demand
    period is **at least 14 days** (7 where the policy term is under a year), stated in the
    표준약관 and reproduced in the retrieved contracts — 「그 때까지 보험료를 납입하지 않을
    경우 납입최고(독촉)기간이 끝나는 날의 다음날 계약이 해지됩니다」 [S2] [REG-R25 제26조](#krlib-reg-r25). The
    postal insurer uses a longer window keyed to calendar months — 「기본보험료 납입유예 기간은
    납입기일부터 납입기일이 속하는 달의 다음 다음달의 마지막 날까지」 [S7]. On the monthly grid
    the composite maps this to a **[std]** rule: a premium unpaid at `t` terminates the
    contract at `t`, with no within-month grace state — a collapse into the month rather than,
    as on the annual grid, into the year. What the grid **must** keep is
    reinstatement, because Korean policies really do come back: within three years of
    termination, provided the surrender value has not been drawn — and the 표준약관 extends
    this expressly to the case where a policy loan consumed it and to the case where there is
    none — on payment of arrears with interest at a rate the insurer sets **within 평균공시이율
    + 1%**, and the insurer may not refuse because a claim event occurred before termination
    [REG-R25 제27조](#krlib-reg-r25) [S7] [S8]. The **간편부활** variant is specific to this product family and
    is the one that touches the model: pay one month's basic premium, and the charges for the
    lapsed months are taken from the fund, with any shortfall paid in [S1] [S5] [S7] [S8]. Its
    consequence is not the cash flow but the date — the premium due dates and the annuity date
    shift by the lapsed period, and the 100.1% floor at annuitisation is **withdrawn** where
    the shortfall was caused by a one-instalment reinstatement or a payment holiday [S4] [S6]
    [S7]. Neither 부활 nor 간편부활 is implemented in `Pension_KR_S`: there is no partial-month
    state to re-enter from, so **lapse is absorbing** and `lapse_rate` is a
    net-of-부활 rate by construction, which `technical-notes.md` states as the reason a user
    substituting a gross experience rate will over-decrement. What the model does keep is the
    consequence — the deferred annuity date and the withdrawn floor — as model point 9's
    payment holiday.

---

## Contractual mechanics

### Timing, the two phases, and the two age bases

Three dates govern the contract. The **계약일** starts the five-year statutory account-age
clock, the contestability clock and the guarantee-ladder clock. The **납입완료일** ends the
premium term but not the maintenance charge. The **연금개시일** is the 계약해당일 on which the
insured's 보험나이 reaches the 연금개시나이 elected at issue [S1] [S2] [S6], and almost no
mechanic survives it: surrender, transfer, policy loans, contributions and the annuity-form
election all stop there, leaving commutation of unpaid guaranteed instalments as the
annuitant's only remaining lever [S2] [S4] [R6 제40조의2제2항제2호](#krlib-pension_savings-r6).

On the monthly grid write `t` for **months** since issue, `m` for the premium term in years
(20 at the anchor cell), `d` for the gap between 납입완료 and 연금개시 in years (5) and
`n = 12(m + d)` (300). Premiums fall at `t = 0 … 12m − 1`; the fund accumulates over
`t = 0 … n`; the annuity is paid at `t = n, n+1, …` for life, with the first 120 instalments
guaranteed. The contractual policy year is the derived label `t // 12 + 1`.

**Two age bases run through the contract and they differ for half of all issue dates.** The
약관 age is 보험나이 — computed from the insured's exact age at the 계약일 by discarding a
remainder under six months and rounding a remainder of six months or more up to a year, then
increasing on each policy anniversary [REG-R25 제21조](#krlib-reg-r25). The statutory tests are on 만나이 (age
last birthday). One retrieved contract states the split in terms, and it is the cleanest
citation in this library for it:

> ① 이 약관에서의 피보험자의 나이는 **보험나이**를 기준으로 합니다. 다만, **연금개시나이가
> 만 55세 이상에 해당되는지 여부의 판단은 실제 만 나이**를 적용합니다. [S6 제20조]

This is not a rounding detail on a product whose annuity date is a statutory threshold. One
carrier states the consequence as a product rule: 「다만, 피보험자가 55세 계약해당일에 만55세
이상이 아닌 경우에는 연금개시나이를 56세부터 선택할 수 있음」 [S1]. The minimum-payout tables
that translate the 연금수령한도 into a term are footnoted 「만나이 기준」 [S3], and the
withholding-rate age bands are on the pensioner's 만나이 [R5] [R9]. `Pension_KR_S` runs on
**보험나이** and declares it in the registry metadata; where a statutory age test enters the
projection the notes state which basis is used and why the difference does not bite at the
anchor cell (65 in 보험나이 is 64 or 65 in 만나이, and both clear 만 55세 by a decade).

### Premium provisions, the contribution ceiling and 추가납입

The 기본보험료 is level and guaranteed for the whole 납입기간 [S1] [S2] [S4] [S6] [S7]; there
are no reviews and no re-rating on this chassis. Payment is monthly by direct debit or an
equivalent route, and the projection grid collects each instalment on its own row, which is
the 월납 account 감독규정 제7-66조제1항제4호 describes [REG-R19]; the annualised-premium
permission of 감독규정 제7-65조제2항 [REG-R18] that the earlier annual grid relied on is no
longer needed.

Two ceilings sit above the premium and they are different in kind.

**The contribution ceiling is ₩18,000,000 a year**, across every 연금계좌 the saver holds at
every institution, excluding rider premiums other than the 연금저축추가납입특약 [R6
제40조의2제2항제1호](#krlib-pension_savings-r6) [R11] [REG-R56]. One carrier states it as 「납입보험료의 연간 합계액
(연금계좌를 취급하는 금융회사에 가입한 연금계좌의 합계액을 말하며, 특약보험료는 제외)은
1,800만원 이내로 하며」 [S1]. It is a **statutory limit on the saver, not on the contract**, so
an insurer cannot police it alone and a model of one contract cannot bind on it. No
contribution may be made at all once annuitisation has been requested [R6 제40조의2제2항제2호](#krlib-pension_savings-r6).

**The credit ceiling is ₩6,000,000 a year** to 연금저축, or ₩9,000,000 counting 연금저축
(within its own ₩6,000,000) plus 퇴직연금계좌 contributions [R1 제59조의3제1항](#krlib-pension_savings-r1) [R8] [R10]
[REG-R56]. The anchor premium of ₩6,000,000 sits exactly on it. Contributions above the credit
cap are **not wasted but are not relieved**, and the contract carries machinery to recycle
them: before requesting annuitisation the saver may ask that previously uncredited
contributions be reclassified into the current tax year — 「이전 과세기간에 납입한 보험료 중
연금계좌세액공제를 받지 않은 금액이 있는 경우로서 … 전환하여 줄 것을 회사에 신청한 경우에는
전환신청한 금액을 연금계좌에서 인출하여 그 신청을 한 날에 다시 해당 연금계좌에 납입한 것으로
봅니다」 [S3 제21조①]. Money that never received a credit is **outside the withdrawal charge
entirely** — 「세액공제를 받은 금액을 초과하여 납입한 금액은 과세되지 않습니다」 [S1] — which
is the reason the 기타소득세 base is not the whole fund (below).

**추가납입** is capped at 200% of the year's basic premiums and bears only the 계약관리비용,
not the 계약체결비용 (footnote 8) [S2] [S5] [S8] [S1] [S7]. It is what makes the ₩18,000,000
ceiling reachable on a ₩6,000,000 contract, and it is off in the base run.

### 계약자적립액 — the accumulation account

The fund is defined identically across the retrieved 2026-vintage documents:

> 「계약자적립액」이란 순보험료(기본보험료에서 계약체결비용 및 계약관리비용을 뺀 금액)를
> 「공시이율」로 납입일부터 일자계산을 하여 적립한 금액으로, 산출방법서에서 정한 바에 따라
> 계산합니다. [S1] [S2]

Four properties of that sentence are load-bearing.

**The charges come off the premium, not off the fund, during the payment term.** The declared
rate applies only to what is left — 「동 이율은 납입한 주계약(또는 적립) 보험료에서
계약체결·유지관리에 필요한 경비 및 위험보장을 위한 보험료를 차감한 금액에 대해서만 적용됩니다」
[S4] [S6]. On the composite there is no risk premium to deduct (footnote 15), so the allocated
premium is simply the basic premium net of the two expense charges.

**Interest accrues by day from the date each premium is received**, not from the policy
anniversary [S1] [S2], so a monthly-premium contract earns a partial year's interest on each
instalment. The monthly grid credits each instalment from the month it is received and leaves
only the day-count inside the month unmodelled; the cross-check that the treatment is right is
in the published illustrations, and it closes. Rolling the
twenty-year surrender value forward the five years from 60 to 65 at the stated rate reproduces
the published fund at annuitisation: ₩140,811,363 × 1.0215⁵ = ₩156,613,630 against a published
₩156,420,000, and ₩120,595,257 × 1.005⁵ = ₩123,640,438 against a published ₩123,460,000
`[derived]` from [S2]. The residuals are **₩193,630 and ₩180,438** — close but not equal, and
both of the order of five years of the post-payment maintenance charge at the
0.67%-of-기본보험료-a-month rate the composite adopts (0.67% × ₩500,000 × 60 = ₩201,000) [S1].
**The accumulation is a plain roll-forward at the declared rate net of a small level
maintenance charge, with no other moving parts.**

**Accrual is monthly before 납입완료 and daily afterwards**, by regulation: 감독규정
제7-66조제1항제4호 states 「보험료 납입이 완료되기 이전에는 … 월별 기간경과에 따라 산출한다」
and 「일별 기간경과에 따라 산출한다」 thereafter [REG-R19]. The two formulas themselves render
as images in the official text and were not retrieved, which is recorded rather than papered
over. The model accrues **monthly throughout**, which follows the regulation's own rule up to
납입완료 and is a **[std]** simplification of the daily accrual after it — the simplification
being worth at most the within-month day-count on a fund that is no longer receiving premiums.

**The maintenance charge does not stop at 납입완료.** 「보험료 납입 완료 후에는 월계약해당일에
계약관리비용 중 유지관련비용(납입후)을 적립액에서 차감합니다」 [S5], and the composite prices
it at 0.67% of the 기본보험료 a month beyond year 20 [S1] — ₩3,350 a month at the anchor cell,
and the monthly grid takes it 월계약해당일에, exactly as the clause says. During the five-year
gap between 납입완료 and 연금개시 the fund is therefore accumulating at the declared rate and
paying a charge with no premium arriving — a state the model must carry explicitly, in each of
the sixty months.

### The crediting machinery — 공시기준이율, 공시이율 and 최저보증이율

The declared rate is not a market rate and must not be modelled as one.

**The chain is 외부지표금리 and 운용자산이익률 → 공시기준이율 → (± 조정률) → 공시이율.** One
carrier states it verbatim: 「제1항의 공시이율은 이 보험의 사업방법서에서 정하는 바에 따라
운용자산이익률과 객관적인 외부지표금리를 가중평균하여 산출된 공시기준이율에서 향후 예상수익
등을 고려한 조정률을 가감하여 결정합니다」 [S4 제6조②]. The two inputs are defined by the
carriers as an index built from 국고채, 회사채, 통화안정증권 and CDs, and a twelve-month
trailing return on invested assets [S1] [S8]. The regulation fixes the same chain: 감독규정
제7-65조제3항 requires the 공시이율 to be the 공시기준이율 adjusted by a 조정률, computes the
운용자산이익률 as 운용자산수익률 less 투자지출률 over the preceding twelve months excluding
insurance finance income and expense, and requires the rate to be **uniform across a product
class** the supervisor defines, with four listed exceptions [REG-R18].

**The weighting is capped, and that is why the rate moves slowly.** 시행세칙 별표 27 gives

> 공시기준이율 = 객관적인 외부지표금리 × α + 운용자산이익률 × (1−α)

with the four yields taken as a three-month weighted moving average ending two months before
application, the sub-weights fixed from the insurer's own prior-year asset balances, and **α
capped at 60%** and held constant through the business year [REG-R24]. A Korean declared rate
is therefore **majority-weighted to the insurer's own realised investment return**, not to
market yields. The retrieved evidence matches: one carrier's published thirteen-month history
runs 3.55% down to 2.98% in steps of 2 to 7 basis points, never once reversing — **57 basis
points over twelve months** [S5] `[derived]`. `Pension_KR_S` therefore treats the crediting
rate as a **slow-moving exogenous scalar**, not as a function of a yield curve, and the 조정률
— a discretionary carrier margin whose permitted range lives in an unpublished 사업방법서 [S1]
[S8] — is not modelled at all.

**The rate is fixed for the calendar month and published monthly** — 「공시이율은 매월 1일에
회사가 정한 이율로 하며, 매월 1일부터 당월 마지막 날일까지 1개월간 확정 적용합니다」 [S1] [S2]
[S4 제6조①] [S5] [S6], with 「회사는 … 공시이율 및 산출방법 등을 매월 회사의 인터넷 홈페이지
등을 통해 공시합니다」 [S4 제6조③]. Carriers run **several parallel declared rates** and assign
each product to one — 「연금저축 공시이율Ⅴ」 [S8], 「신공시이율Ⅳ」 [S7], 「신공시이율(무배당
연금저축Ⅳ)」 [S11] — so a declared rate is a *product-series* constant, not a carrier constant,
and the spread between two vintages inside one carrier reached 19 basis points on one date
[S12].

**The floor is a guarantee on the credited rate.** Where the declared rate falls below the
ladder the fund is credited at the ladder instead — 「최저보증이율이 0.3%인 경우 공시이율이
0.1%로 낮아지더라도 적립금은 공시이율(0.1%)이 아닌 최저보증이율(0.3%)로 적립됩니다」 [S8] — but
**expenses are still deducted beneath it** [S4]. The ladder steps *down* with elapsed duration
on every retrieved contract, which is the opposite of intuition and matters: the guarantee is
strongest exactly where the fund is smallest. The composite's 1.25 / 1.00 / 0.50 at five and
ten years is the modal current shape (footnote 12); the whole observed range and the fact that
the ladder tracks the sale date rather than the carrier [S13] are recorded under *Variations*.

The **평균공시이율** is a third rate and is not a crediting rate at all. It is defined by
감독규정 제1-2조제13호 as the average of all insurers' declared rates as the supervisor
computes it [REG-R9], published to the market through carriers' regulatory disclosure, and
**2.50% for 2026**, down from 2.75% — the first fall in the series since 2021 [REG-R48] [S14]
[S2]. It enters this product in four places and each is a constraint rather than a cash flow:
the illustration rule, which shows the fund on the lesser of the 평균공시이율 and the carrier's
own rate alongside two other bases [S2] [S5]; the 별표 14 주6 discount in the
surrender-charge cap [REG-R20]; the reinstatement interest ceiling of 평균공시이율 + 1%
[REG-R25 제27조](#krlib-reg-r25); and the 저축성보험 design test of 감독규정 제7-60조제3호,
which a whole-life 생존연금 or a 연금저축보험 may run at **평균공시이율 + 0.25%p** [REG-R16].
In 2026 the carrier's own rate (2.15%) is below the average (2.50%), so the middle
illustration basis collapses onto the third and two of the three published illustrations are
numerically identical [S2].

### Expenses, 해약공제액 and the statutory cap

The composite's charges are stated once, in won, at the anchor cell:

| Charge | Basis | Period | Anchor amount |
|---|---|---|---|
| 계약체결비용 | 1.50% of 기본보험료, monthly | policy years 1–7 | ₩7,500 a month, ₩90,000 a year, **₩630,000 total** |
| 계약관리비용 | 3.00% of 기본보험료, monthly | policy years 1–20 | ₩15,000 a month, ₩180,000 a year |
| 계약관리비용 (납입후) | 0.67% of 기본보험료, monthly | after year 20 | ₩3,350 a month, ₩40,200 a year |
| 연금수령기간 관리비용 | 0.5% of 연금연액 | in payment | — |
| 모집수수료 | 0.00% | every year | nil |
| 해약공제액 | — | — | **nil at every duration** |

All amounts are `[derived]` arithmetic on the percentage schedule of [S1] at the anchor
premium. Total loading is **4.50%** of premium in years 1 to 7, **3.00%** in years 8 to 20 and
**0.67%** thereafter [S1].

The **해약공제액** is unamortised acquisition cost, and the non-life carrier gives the cleanest
definition: 「신계약을 청약하고 승낙하는 과정에서 소요되는 비용을 계약체결비용이라 하며,
일정기간 동안 보험료에서 균등하게 공제함. 그러나 계약을 중도에 해지하게 될 경우, 공제하지 못한
계약체결비용을 한꺼번에 공제하게 되는데 이를 해약공제액(미상각 신계약비)라 함」 [S8]. On the
composite it is **zero at every duration**, following the published table of the source product
[S1] — a design in which the acquisition cost is recovered entirely through the level monthly
charge and there is nothing left to claw back on surrender. The surrender value is therefore
simply the fund:

    CV(t) = max( 0, AV(t) − SC(t) ) = AV(t),   SC(t) = 0

with the zero floor imposed by 감독규정 제7-66조제1항제1호 — 「계약자적립액에서 해약공제액을
공제한 금액이 음(陰)의 값인 경우에는 이를 영(零)으로 처리한다」 [REG-R19] — and 미경과보험료
added on termination under 제7-66조제5항 [REG-R19].

The **statutory cap** and its computation on the composite are in footnote 16. Two regulatory
points travel with it. The **해약공제기간** — the period over which any deduction may be taken
— is the premium term or the acquisition-cost loading period, **capped at seven years**
[REG-R19 제7-66조제1항제2호](#krlib-reg-r19), which is exactly the composite's 계약체결비용 period. And 별표 14
주5's coefficient is **3% for a 무배당 연금저축보험 against 4% for a participating one and 5%
for a general 저축성보험**, with 주4's 6% concession for a whole-of-life survival annuity
expressly **denied** to a 연금저축보험 [REG-R20] [R14]: the regulator has singled this product
out for the tightest surrender-charge cap in the schedule, and the reference implementation
sits far inside it.

The wider expense ring is worth one sentence because it bounds the design space, and its two
halves reach this contract differently. The commission caps of 감독규정 제4-32조제5항·제6항 —
first-year remuneration held to the first year's premium, with the projected one-year
surrender value added to the commission side where the contract deducts 80% or more of the
표준해약공제액 — are written for a **보장성보험** and therefore do not bind a 저축성보험 at
all; 제8항's instalment structure, paying no more than **60% of the 표준해약공제액 a year**
where the cap exceeds one year's premiums, is the part of that article a savings design meets
[REG-R22] [REG-R29]. What does bind here is 제7-51조, which requires pre-notification of a
저축성보험 산출방법서 that does **not** spread at least 50% of the acquisition cost evenly over
the premium term — 70% for bancassurance, **100% for online** — over at least seven years where
the payment term is seven years or more [REG-R22]. The composite is an online, direct-channel
design that spreads 100% of its acquisition cost evenly over seven years and pays no commission
at all [S1]; it is inside that requirement by construction, and the commission caps have
nothing to bite on.

### 해약환급금 — the surrender-value shape, and what the composite reproduces

Two published illustrations bracket the shape, both from the same carrier and the same year,
and the gap between them is the single most useful piece of quantitative evidence in the
retrieved set. The first is the direct-channel product whose expense schedule the composite
adopts, on 남자 30세, 월 300,000원, 20년납, 60세 개시, where 해약환급금 equals the fund at
every duration because the surrender charge is zero [S1]:

| 경과기간 | 납입보험료 | 최저보증 환급금 | 환급률 | 2.40% 환급금 | 환급률 |
|---|---|---|---|---|---|
| 3개월 | 900,000 | 861,291 | 95.7% | 862,938 | 95.9% |
| 1년 | 3,600,000 | 3,461,278 | 96.1% | 3,482,694 | 96.7% |
| 3년 | 10,800,000 | 10,514,173 | 97.4% | 10,700,842 | 99.1% |
| 4년 | 14,400,000 | 14,106,878 | 98.0% | 14,440,356 | **100.3%** |
| 5년 | 18,000,000 | 17,744,493 | 98.6% | 18,269,619 | 101.5% |
| 8년 | 28,800,000 | 28,810,373 | **100.0%** | 30,372,398 | 105.5% |
| 10년 | 36,000,000 | 36,446,400 | 101.2% | 39,007,457 | 108.4% |
| 20년 | 72,000,000 | 74,123,274 | 102.9% | 88,897,250 | 123.5% |

Break-even is at **four years on the declared-rate basis and eight years on the guaranteed
basis** `[derived]` from [S1]. The second is the tied-channel participating product from which
the anchor model point is taken — 남자 40세, 월 500,000원, 20년납, 65세 개시 [S2]:

| 경과기간 | 납입보험료 | 2.15% 환급금 | 환급률 | 최저보증 환급금 | 환급률 |
|---|---|---|---|---|---|
| 3개월 | 1,500,000 | 651,477 | **43.4%** | 649,394 | 43.3% |
| 1년 | 6,000,000 | 4,960,704 | 82.7% | 4,933,619 | 82.2% |
| 3년 | 18,000,000 | 16,787,246 | 93.3% | 16,551,491 | 92.0% |
| 5년 | 30,000,000 | 29,118,235 | 97.1% | 28,456,091 | 94.9% |
| 10년 | 60,000,000 | 62,220,046 | 103.7% | 58,880,326 | 98.1% |
| 15년 | 90,000,000 | 99,427,916 | 110.5% | 89,353,054 | 99.3% |
| 20년 | 120,000,000 | 140,811,363 | **117.3%** | 120,595,257 | **100.5%** |

**43.4% against 95.9% at three months, on two products of the same carrier in the same year.**
The tied-channel product carries a real front-end acquisition charge and the direct-channel one
does not; the leaflet does not publish the schedule, so the charge cannot be decomposed, but
the surrender pattern is unambiguous [S2]. The composite adopts the direct-channel schedule
(footnote 9) and will therefore reproduce the **first** shape, with a break-even in the fourth
or fifth policy year, while taking the second product's model point, fund at annuitisation and
annuity illustrations. That combination is deliberate and is the composite's largest single
standardization: it pairs the only fully published expense schedule with the only fully
published annuitisation illustration. `technical-notes.md` states the resulting first-year
환급률 as a model output and the test module asserts it.

Note what the guaranteed-rate column of the second table shows: the contract reaches only
**100.5%** of premiums at the end of the twenty-year payment term, which is the 100.1% floor
doing the work rather than the interest [S2]. And note the postal insurer's third shape, the
only retrieved product with a real surrender charge: 환급률 **86.6%** at one year, **100.0%**
at five and 123.1% at twenty on a ₩100,000-a-month contract, with the gap between two premium
sizes at year 1 (86.6% against 87.1%) showing the fixed component of the charge structure [S7]
`[derived]`.

### Death before annuitisation, and the absence of mortality risk

The death payment is the fund and nothing more (footnote 15). Three consequences are worth
stating as model properties, because each is a testable assertion about `Pension_KR_S`:

1. **Death and surrender pay the same amount at every duration**, since the surrender charge is
   zero. The two decrements differ only in their rate, not in their payment.
2. **The insurer's deferral-phase mortality strain is exactly zero**, so no deferral-phase
   mortality table is needed for the liability. A table is still needed to project the *number*
   of policies in force and hence the expense and charge income, and it is the same
   annuitant-basis table used for the annuity factor.
3. **The 100.1% floor is the only guarantee that bites before annuitisation**, and it bites at
   one date. A death claim in deferral is not floored at premiums paid on the composite
   (footnote 15), so the guarantee is a survival guarantee, payable only to a policy that
   reaches the 연금개시일 in force.

Where a claim is refused for an exclusion the standard Korean life 약관 pays the 계약자적립액
at the date of death to the policyholder [REG-R25 제22조](#krlib-reg-r25) — on this product, the same amount
the benefit itself would have been. The exclusion set therefore has **no cash-flow consequence
here** and is not modelled, and this document does not recite a list lifted from a protection
product.

### 연금개시 — the minimum fund and the annuity factor

At the 연금개시일 the 계약자적립액 is fixed, floored at **100.1% of premiums paid** (footnote
17), and divided by an annuity factor to give the 연금연액.

**확정기간연금형 uses the declared rate alone**: 「연금개시시점의 계약자적립액을 기준으로
공시이율을 적용하여 산출방법서에 따라 계약자가 선택한 확정된 연금지급기간 동안 나누어 계산」
[S1] [S2] [S6]. Mortality does not enter it, and neither does survival: the instalments are
paid to the count whether or not the annuitant lives [S1] [S2] [S4] [S6]. The reconstruction:

    연금연액 = 계약자적립액 ÷ ä_n^(12)(공시이율) × (1 − 0.005)

recovers the published figures to three or four significant digits **once the annuity-due is
taken payable monthly rather than annually**, which is what the contract actually pays. On the
annual factor the same check leaves a residual — 0.995 at 2.15% and 1.003, 1.002, 1.003 at the
guaranteed rate, uniform but running the other way — and an earlier draft of this document
recorded the second of those as unexplained. It is not. Writing `ä_n` as the annuity-due
payable twelve times a year, `(1 − v^n)/d^(12)`, and taking the life form as the annual factor
less 11/24, this one 0.5% charge recovers **eight** published implied factors across **two**
interest bases: 확정 10/15/20년 at 9.061 / 12.918 / 16.386 against a published 9.06 / 12.92 /
16.39 at 2.15%, and 9.806 / 14.528 / 19.134 against 9.81 / 14.53 / 19.13 at the 0.5% floor;
종신 10년보증 남 65 at 23.700 against 23.70, and 31.180 against 31.18. The remaining 1.006 at a
third carrier is that carrier's own absence of an annuity-phase charge [S5] `[derived]`. The
composite implements the monthly form, and exposes the 0.5% as an input.

**종신연금형 uses the annuitant mortality and the declared rate**: 「연금개시시점의
계약자적립액을 기준으로 연금사망률 및 공시이율을 적용하여 산출방법서에 따라 나누어 계산 후
공시이율의 변동을 반영한 연금연액」 [S1] [S2], with the same wording at [S6]. Mortality enters
the life form only. The published illustrations imply the factors directly, on a fund of
₩156,420,000 at 2.15% for a 65-year-old male [S2] `[derived]`:

| Form | Published annuity | Annualised | Implied factor |
|---|---|---|---|
| 종신연금형 10년보증 | 월 55만원 | 660만원 | **23.70** |
| 종신연금형 20년보증 | 월 54만원 | 648만원 | 24.14 |
| 확정연금형 10년 | 월 143만원, 총 17,263만원 | 1,726.3만원 | 9.06 |
| 확정연금형 15년 | 월 100만원, 총 18,164만원 | 1,210.9만원 | 12.92 |
| 확정연금형 20년 | 월 79만원, 총 19,093만원 | 954.7만원 | 16.39 |

The certain forms are annualised from the published **총 지급액** over the term, not from the
rounded monthly figure, which is how [S2] presents them; annualising 월 143만원 directly would
give 1,716만원 and an implied factor of 9.12 rather than 9.06.

and on a fund of ₩123,460,000 at the 0.50% floor, 31.18 and 32.15 for the two life forms and
9.81 / 14.53 / 19.13 for the three certain forms [S2] `[derived]`.

**The implied longevity is the sanity check any annuitant table must pass.** Solving ä_n =
23.70 at 2.15% on the **monthly** annuity-due the contract actually pays gives n ≈ **32.9
years**, so a 65-year-old male's life annuity is priced like a certain annuity running to
about **age 98**; at the guaranteed-rate basis, ä_n = 31.18 at 0.50% gives n ≈ 33.9, to about
**age 99** [S2] `[derived]`. (On the annual annuity-due the two solves give 32.5 and 33.8, to
about 97 and 99; the monthly reading is the consistent one — see footnote 10.) That is
consistent with the extremely
light published annuitant rates (below) and it is the constraint `mort_table.csv` must
reproduce. It is also the number a policyholder is actually choosing between: a 65-year-old
male's 종신연금형 10년보증 pays **38.2%** of what a 10-year certain annuity pays on the same
fund (660 against 1,726만원) [S2] `[derived]`.

**Instalments.** The 연금연액 may be taken 매월, 매3개월 or 매6개월, with the deferred
instalments credited at the declared rate [S6 별표1 주9] [S1] [S2] [S5] [S7]; the projection
grid is annual and that interest is folded into the annual amount.

**Death in payment.** On a 종신연금형 the unpaid guaranteed instalments are paid, and the
contract warns that they may total less than the fund — 「보증지급기간 동안 지급된 연금총액은
"연금개시시점의 계약자적립액" 보다 적을 수 있습니다」 [S1] [S2] [S6] — and may be commuted at
the declared rate on the insurer's consent [S2]. On a 확정기간연금형 the remaining instalments
are paid to the count [S1] [S2] [S4] [S6].

**No surrender after the first annuity payment on a life annuity** — 「종신연금형의 경우 연금
지급이 개시된 후에는 이 계약을 해지할 수 없습니다」 [S10], and the same in [S4 제5조③], [S5]
and [S2]. This is not merely a contractual restriction: it is the feature on which the lowest
withholding band depends (below).

### The annuitant mortality basis and the 경험생명표

The industry table is **not published**. 보험개발원 (Korea Insurance Development Institute)
files 참조순보험요율 with the supervisor under 보험업법 제176조 and has no publication
obligation [REG-R4] [R16]; the 제10회 경험생명표, applied to new business from **2024-04**, is
public only as two summary statistics — 평균수명 **남 86.3세 / 여 90.7세**, up 2.8 and 2.2
years on the 제9회, with 65세 기대여명 남 23.7년 / 여 27.1년 [REG-R33] [R18] [R19]. The KIDI
press-release page is JavaScript-driven and the release itself could not be opened [R17]
[REG-R34]; the KIDI big-data portal refused connections on its port [R24]. **Every
`mort_table.csv` in `krlib` is therefore a `[std]` construction with a `provenance` column on
every row, and `Pension_KR_S`'s is no exception.**

What *is* public, and what the composite's table is anchored on, are the annuitant rates two
carriers publish in their statutory product summaries. These are the only annuitant-mortality
numbers retrieved in this research pass:

| Source | Basis | Age | Male | Female |
|---|---|---|---|---|
| [S1] 「연금사망률」, 가입연령 40세 기준 | by 연금지급개시나이 | 50 | 0.00094 | 0.00044 |
| | | 60 | 0.00150 | 0.00052 |
| | | 70 | 0.00291 | 0.00097 |
| [S7] 「개인연금사망률」, 기준 40세 가입 | by attained age | 40 | 0.00077 | 0.00048 |
| | | 60 | 0.00164 | 0.00056 |
| | | 80 | 0.01346 | 0.00622 |

The two agree closely where they overlap — at 60, 0.00150 against 0.00164 for men (a ratio of
1.09) and 0.00052 against 0.00056 for women (1.08) `[derived]` — which is strong evidence that
both are the bureau's reference annuitant rates carrying different safety margins. **The rates
are extremely light**: a male rate of 0.00164 at exactly 60 and 0.01346 at 80 is far below any
plausible Korean population level, which is what a table loaded on the *survival* side for a
longevity product looks like. The implied ageing gradient over 60–80 is about **11.1% a year
for men and 12.8% for women** on a constant-force fit `[derived]` from [S7]. The public
population anchor sits well below: 국가데이터처's 「2024년 생명표 작성 결과」 gives 기대수명 at
birth 남 80.8 / 여 86.6 and 65세 기대여명 남 19.5 / 여 23.7 [REG-R38], against insured 평균수명
남 86.3 / 여 90.7 and 65세 기대여명 남 23.7 / 여 27.1 [REG-R33] — a gap of about **4.2 years
for men and 3.4 for women at 65**.

Three modelling instructions follow, and they are stated here rather than left to the notes
because they are product facts. **The annuitant table cannot be shared with `WholeLife_KR_S`**:
one is loaded for survival, the other for death, and using one for both is wrong in a known
direction. **The table must reproduce the implied factor of 23.70 at 2.15% for a 65-year-old
male with a ten-year guarantee**, which is the only calibration target the public record
offers. And **the table's vintage is the 가입시점 vintage** (footnote 20), with the
연금개시시점 table available through the ratchet.

The direction of past revisions matters for any improvement scenario. On a fixed ₩200,000,000
fund annuitising at 60, the trade press reports 6차 to 78.4세 at ₩906,000 a month, 9차 to
85.3세 at ₩709,000, and 10차 to 86.3세 at "60만원 후반" — a fall of roughly **15%** in the
monthly annuity from the ninth table to the tenth [R19]. Directionally: annuity and health
products dearer, death products cheaper [R18] [R20] [REG-R33]. A revision that lightens
mortality *reduces* the annuity, which is why the ratchet does not bite.

### The tax layer — 세액공제, 연금수령, 연금소득세 and 기타소득세

`krlib` models contractual cash flows, not the policyholder's tax position. The tax layer is
carried in full because it drives the two behavioural assumptions this product cannot be
modelled without: whether the saver persists, and whether the saver annuitises for life.

**On the way in: a credit, not a deduction.** 12% of contributions to a 연금계좌, or 15% where
종합소득금액 is ₩45,000,000 or less (총급여액 ₩55,000,000 for employment income only), on up to
₩6,000,000 a year to 연금저축 and ₩9,000,000 counting 퇴직연금 [R1 제59조의3제1항](#krlib-pension_savings-r1) [R8]
[REG-R56]. Grossed up for the 10% local surtax the market quotes **16.5% and 13.2%** [R10],
figures this document treats as [unverified] arithmetic on a verified base (footnote 13). At
the ₩6,000,000 anchor contribution the credit is **₩990,000 or ₩792,000 a year** [S11]
`[derived]`; at the ₩9,000,000 combined cap it is ₩1,485,000 or ₩1,188,000 `[derived]`. Where
an 개인종합자산관리계좌 matures into a 연금계좌 the limit is enlarged by **10% of the converted
amount, capped at ₩3,000,000** [R8] [R1 제59조의3제3항](#krlib-pension_savings-r1) [REG-R56]. **The higher-income band
gets the lower credit rate**, so the after-tax value of a contribution *falls* with income —
the opposite of a deduction, and a fact that shapes who buys the product.

**On the way out: three limbs, all of which must hold.** A withdrawal is 연금수령, and taxed as
pension income, only if [R6 제40조의2제3항](#krlib-pension_savings-r6), reproduced verbatim in a filed 약관 부록 [S3]:

1. the saver has applied to begin drawing **after 55** — 「가입자가 55세 이후
   연금계좌취급자에게 연금수령 개시를 신청한 후 인출할 것」;
2. **five years** have passed since the account was opened — disapplied where the account holds
   이연퇴직소득; and
3. the withdrawal is within the **연금수령한도**:

```
                   연금계좌의 평가액          120
연금수령한도  =  ────────────────────────  ×  ─────
                 (11 − 연금수령연차)          100
```

The 연금수령연차 runs from the tax year in which drawing first became possible, and **where it
is 11 or more the formula does not apply at all** [R6 제40조의2제4항](#krlib-pension_savings-r6) [S1] [S3]. Two exceptions
to the starting count: an account opened before 2013-03-01 starts at year 6, and an account
inherited by a spouse starts at the deceased's own 연금수령연차 [R6]. Anything above the limit
is **deemed 연금외수령** [R6 제40조의2제5항](#krlib-pension_savings-r6).

Because the counter climbs by one each tax year, the limit is a **rising fraction of the
balance** — 12% in year 1, 13.3% in year 2, 60% in year 9, 120% in year 10, unlimited from year
11 `[derived]` from [R6]. In practice ten years is the shortest payout the tax code tolerates
for a contract annuitised as early as it can be. One carrier tabulates the same thing as a
minimum payout term by annuitisation age, for a contract taken out before 50 [S3]:

| 연금개시시점 | 55세 | 56 | 57 | 58 | 59 | 60 | 61 | 62 | 63 | 64 | 65세 이후 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 최소 연금지급기간 | 10년 이상 | 9년 | 8년 | 7년 | 6년 | 5년 | 4년 | 3년 | 2년 | 1년 | **요건 없음** |

all footnoted 「균등수령방식 기준, 만나이 기준」 [S3]. **At the anchor cell the constraint does
not bind at all**: a contract taken out at 40 could first have drawn at 55, so by the 65
annuity date the 연금수령연차 has reached 11 and the limit is disapplied. The composite
therefore projects an unconstrained annuity and states the constraint for the ages at which it
does bite. Every retrieved contract makes the default election the tax-efficient one —
「계약자의 특별한 의사 표시가 없는 경우 매년 지급하는 연금액은 관련 세법에서 정한 바에 따라
연금소득으로 인정받을 수 있는 범위 이내로 합니다」 [S3 제21조②] [S5] [S7] [S8] — so the
contract itself enforces the limit where it binds.

**Withholding on pension income**, 소득세법 제129조제1항제5호의2 [R5] [R9] [R11] [REG-R56]:

| Basis | Statutory | Including 지방소득세 |
|---|---|---|
| 연금소득자 70세 미만 | 100분의 5 | 5.5% |
| 70세 이상 80세 미만 | 100분의 4 | 4.4% |
| 80세 이상 | 100분의 3 | 3.3% |
| **종신계약에 따라 받는 연금소득** | **100분의 3** (from 2026-01-01; previously 4) | **3.3%** |

The lowest applicable rate governs, so a fixed-term annuity runs 5.5% / 4.4% / 3.3% by age and
a life annuity is a flat **3.3% at every age from 55** [R9] [R11]. **The reduction from 4% to
3% took effect for pensions received on or after 2026-01-01**, by 법률 제21221호 of 2025-12-23
[R5] [R9] [R21] — the most recent substantive change in this file, and in force at the access
date. Its effect is to make the life-annuity form a **2.2-percentage-point standing advantage**
over a fixed-term annuity for a 55-to-70-year-old, where before 2026 it was 1.1 points. That is
a dated, quantified incentive to annuitise for life and it is a first-order input to the
annuitisation-election assumption.

One caution attaches to it, and it is material. 종신계약 is defined by 소득세법 시행령
제187조의2, whose **operative text could not be retrieved** in either research pass [R7]: the
article's existence, number and title are verified in both languages, and the tax authority
glosses the condition as a contract paid until death that **cannot be surrendered mid-term**
[R9], a gloss consistent with every retrieved 종신연금형 wording. But **whether a guarantee
period of any length is compatible with 종신계약 status is not established**. If a ten-year
guarantee disqualified the contract, the anchor cell's withholding would be 5.5% until 70
rather than 3.3%, and the election economics would change materially. This document does not
assert the answer; `technical-notes.md` carries the base run at 3.3% with the alternative as a
switch.

**Aggregation.** Private pension income of **₩15,000,000 (1,500만원) or less** in a year is
분리과세연금소득: the withholding settles the liability, though the taxpayer may elect to
aggregate [R3 제14조제3항제9호다목](#krlib-pension_savings-r3). Above it, the income enters 종합소득 at the graduated
rates, **or** the taxpayer may elect the special computation of 소득세법 제64조의4, which
applies 100분의 15 — the "16.5% 분리과세" of the trade press [R4] [R9] [R11]. The threshold was
**₩12,000,000** for the 2013–2022 tax years, which is what the older carrier documents still
say [S5] [S1] [S2] [S3]. At the anchor cell the life annuity is ₩6,600,000 a year `[derived]`
from [S2], comfortably inside the threshold, and the average balance across the whole market
implies the same for most savers `[derived]` from [R13].

**Off the way out: 16.5% 기타소득세.** Any amount withdrawn that is not 연금수령 — a surrender,
a lump sum, or the excess over the 연금수령한도 — is 기타소득 under 소득세법 제21조제1항제21호,
separately taxed under 제14조제3항제8호나목 [R3] and withheld at 100분의 15 [R5]. Nine
independent carrier documents state the grossed-up rate identically as **16.5% (지방소득세
포함)** [S1] [S2] [S3 제21조②] [S4] [S5] [S7] [S8] [S11] [S16]. The **base** is the credited
money and its return, not the whole fund, and the non-life contract states it most precisely:

> [해약환급금 − 실제 세액공제 받은 보험료를 초과하여 납입한 보험료의 누계액과 연금수령액 중
> 큰 금액]의 16.5%(지방소득세 포함)를 기타소득세로 원천징수 [S8]

One carrier's surrender illustration carries a 세후지급 예상액 column computed on exactly that
basis, and the column is **uniformly 83.5% of the surrender value at every duration and on both
interest bases** — 86,869,520 / 104,003,740 = 0.83525 and 3,091,800 / 3,701,180 = 0.83536
`[derived]` from [S5], which is 1 − 16.5% to three figures. **On a contract whose
contributions were all within the credit cap the charge falls on essentially the whole
surrender value.**

**The escape hatches.** Where the contract is surrendered for one of six 부득이한 사유 the
amount is taxed at the pension rates instead: the policyholder's death; a natural disaster;
illness or injury of the policyholder or a dependant requiring **three months or more** of
care, relieved up to the sum of ₩2,000,000, medical and carer costs and **₩1,500,000 per month
of leave or business suspension**; bankruptcy or individual rehabilitation; the insurer's
suspension, licence revocation, dissolution or bankruptcy; and emigration — claimed **within
six months of the triggering event** [S3 제21조④⑥] [S1] [S5] [S7]. Separately, **의료비인출**,
an amount withdrawn to meet the saver's own medical costs (excluding cosmetic surgery and
health-promotion medicines), is taxed as pension income **even where it exceeds the
연금수령한도** [S3 제21조②] [S1] [S7] [S8]. Neither is modelled; both are recorded because they
are the only routes out of the 16.5% charge and because they bound any assumption about it.

**Spouse succession.** Where the heir is the spouse, the spouse may take over the contract:
the spouse's 가입일 becomes the date of the deceased's death, but the **two dates that matter
for the tax test are carried over from the deceased** — 「연금수령을 개시할 때 최소납입요건
경과 판정을 위한 가입일 및 연금수령한도 산정을 위한 연금수령연차 기산일은 피상속인(사망한
계약자) 기준으로 적용합니다」 [S1] [S3 제21조⑤] [S6] [S7] [S8] — and the request must be made
within six months of the end of the month of death [S2] [S5] [S6] [S7]. Not modelled; it is the
reason a death in deferral is not always a termination.

### Why the lapse assumption is not the savings lapse assumption

This is the product's own distinctive modelling problem and the spec states it rather than
leaving it to the notes.

**There is no public Korean lapse statistic for 연금저축보험 by policy year.** One carrier's
regulatory disclosure carries a 경과기간별 중도해지율 column in which every row reads
「적용안함」 [S13]; the 유지율 category exists in the supervisor's comparison disclosure but
the table could not be opened [S19] [R12]; and the behavioural tables in the 2025 whitepaper
sit in attachments that did not convert [R13]. **The lapse basis is therefore `[std]` and must
be argued from the contract, not fitted to data.**

Four sourced facts constrain it.

1. **A surrender costs 16.5% of essentially the whole payout** once the contributions have been
   credited [S5] [S8] `[derived]`. Nothing in the savings products of this repository has a
   comparable frictional cost.
2. **The net tax position is worse than it looks, but only above break-even.** The credit taken
   was 16.5% of cumulative contributions; the charge is 16.5% of the surrender value. Netting
   them, the saver's tax cost of surrendering is 16.5% × (해약환급금 − cumulative
   contributions) `[derived]`, which is *negative* while the 환급률 is under 100% and positive
   after. On the composite's shape (break-even in year four or five) the tax turns against the
   surrendering saver at almost exactly the duration at which the expense loading stops hurting
   — so the two frictions do not overlap, they hand off.
3. **The surrender value is below premiums paid for the first four to eight years** on the
   composite's expense schedule [S1], and for far longer on a tied-channel design [S2]. A saver
   who surrenders early loses expense *and* pays no net tax; a saver who surrenders late keeps
   the interest *and* pays the tax on it.
4. **Part of what looks like lapse is transfer.** 계좌이체 to a 연금저축펀드 or an IRP is not a
   withdrawal and is not taxed [S1], and the market moved that way hard in 2025 — funds +50.7%,
   insurance −1.2% [R13] [R22]. An insurer's termination count and the wrapper's persistency
   are different numbers.

The reference implementation therefore uses a **lapse vector materially flatter than a
non-qualified savings contract's**, tagged `[std]` with this paragraph as its rationale, and
exposes it as an assumption-class input with a switch to a savings-product vector so the two
can be compared. It does **not** borrow the supervisory 무·저해지 lapse guidance — the
log-linear decay to 0.1% at 납입완료 and 0.8% thereafter of the 제4차 보험개혁회의 [REG-R27] —
because that guidance is calibrated to 순수보장성 and 무해지 protection business, and this
product is neither: it has a full surrender value from the first month and no cliff at
납입완료. The guidance is cited in `technical-notes.md` as the shape a Korean supervisor
expects a lapse curve to have, not as this product's numbers.

### 청약철회, 품질보증해지 and 계약 전 알릴 의무

These sit outside the projection — the model begins where cover is in force — and are stated
explicitly rather than silently omitted.

**청약철회.** 15 days from receipt of the 보험증권 and never after 30 days from the
application, effective **on dispatch**, with premiums returned within three business days and
late return carrying interest at the 보험계약대출이율 compounded annually [REG-R25 제17조](#krlib-reg-r25). The
statutory source is 금융소비자보호법 제46조제1항제1호 — 「「상법」 제640조에 따른 보험증권을
받은 날부터 15일과 청약을 한 날부터 30일 중 먼저 도래하는 기간」 — with no damages or penalty
on withdrawal and the right lost where a claim event has already occurred unless the
policyholder withdrew knowing it had [REG-R51]. Two carrier documents state the 15/30 pair [S2]
[S5].

**품질보증해지.** Three months from formation where the insurer failed to deliver the 약관 and
the policyholder's copy of the application, failed to explain the important content, or the
policyholder did not sign, with premiums returned plus 보험계약대출이율 interest [REG-R25
제18조제3항](#krlib-reg-r25) [S2] [S5] [S7]. The statutory source is 상법 제638조의3제2항 [REG-R49].

**계약 전 알릴 의무.** The 표준약관 states in terms that this is the 상법 고지의무. Termination
for a breach is barred where the insurer knew or was negligent in not knowing at formation;
where **one month** has passed since it learned of the breach; where **two years** have passed
from the 보장개시일 without a claim event (**one year** for disease in a 진단계약); where
**three years** have passed since the contract date; where the insurer accepted on a health
examination and the claim arises from a matter stated in it; or where the 보험설계사 prevented
truthful disclosure [REG-R25 제13조·제14조](#krlib-reg-r25). One carrier states the two-year and one-year pair
directly [S1]. **On this product the duty is close to inert**, because there is no underwriting
and no death cover above the fund (footnotes 3 and 15): the insurer has almost nothing whose
misstatement would change its risk. It is recorded because it is a term of the contract, not
because it has a cash-flow consequence.

**사기에 의한 계약.** Cancellable within five years of the 보장개시일 and one month of
discovery [REG-R25 제15조](#krlib-reg-r25) [S1] [S7]; premiums are returned with interest at the
보험계약대출이율 on this product [S1].

### Expiry and termination

The contract can end in five ways, and `Pension_KR_S` must be able to reach each of them:

1. **Surrender before annuitisation** — the fund is paid, less any surrender charge (nil on the
   composite) and any policy loan, plus 미경과보험료 [REG-R19 제7-66조제5항](#krlib-reg-r19) [S1] [S8].
2. **Death before annuitisation** — the fund is paid and the contract ends [S1] [S2] [S4] [S6],
   unless a spouse succeeds to it [S1] [S3] [S6] [S7] [S8].
3. **Lapse** at the end of the demand period, with a three-year reinstatement window [REG-R25
   제26조·제27조](#krlib-reg-r25) [S2] [S7] [S8].
4. **Transfer out** to another 연금저축 or an IRP — not a termination of the tax-recognised
   balance, but a termination of this contract [S1].
5. **Death in payment after the guarantee period** on a 종신연금형 — nothing further is paid,
   and **exhaustion** on the last certain instalment of a 확정기간연금형 or the last guaranteed
   instalment where the annuitant died inside the guarantee [S1] [S2] [S4] [S6].

There is no maturity benefit and no maturity date: the deferral phase ends by conversion into
the payout phase, not by payment. On termination the policyholder's protection sits in the
연금저축계좌 bucket of 예금자보호법 시행령 제18조제7항, separate from the ₩100,000,000 covering
their other 보험금 claims against the same insurer [REG-R52]; the 2026-vintage carrier
documents state that limit and the separate bucket [S2] [S6] [S11], the 2024 and 2016 documents
still say ₩50,000,000 [S4] [S5], and a contract held or paid for by a corporation is not
protected at all [S4] [S5].

---

## Riders and options

A Korean policy is a 주계약 (main contract) with 특약 (riders) attached, and practice
distinguishes 제도성특약 — riders that change the contract's own machinery rather than adding
cover — from 보장성특약. On a 연금저축보험 almost every rider is of the first kind.

**In scope (modelled or parameterized):**

- **The annuitisation election** — one binary at the 연금개시일 between 종신연금형 with a
  ten-year guarantee (default) and 확정기간연금형 over ten years, the first computed on the
  annuitant mortality and the declared rate and the second on the declared rate alone [S1] [S2]
  [S6]. Take-up is a **[std]** behavioural assumption in the technical notes, and the tax
  differential of footnote 13 and the withholding table above is its stated driver.
- **The annuitant-mortality ratchet** — modelled as an option that is out of the money in the
  base run, with the vintage exposed as a switch (footnote 20) [S1] [S2] [S4] [S6] [S9].
- **The 100.1% minimum fund at annuitisation** — modelled, with the two disapplication triggers
  represented as flags rather than as states (footnote 17) [S2] [S4] [S7].
- **연금저축추가납입특약** — an optional module, off in the base run, carrying its own lighter
  charge basis (footnote 8) [S2] [S5] [S7] [S8].
- **보험계약대출** — an optional module, off in the base run, because no retrieved document
  gives a rate (footnote 14) [S1] [S2] [S4] [S5] [REG-R25 제33조](#krlib-reg-r25).
- **납입유예 / 납입일시중지** — an optional module, off in the base run; when on, it defers the
  premium dates and the annuity date, keeps the charges running against the fund, and
  **withdraws the 100.1% guarantee** (footnote 14) [S5] [S7] [S8] [S4] [S6].
- **The 계약자배당 machinery** — retained and set to zero on the 무배당 composite, and moved
  from 3% to 4% in 별표 14 by the `par` flag (footnotes 1 and 16) [S2] [S7] [REG-R20].

**Out of scope, each for a stated reason:**

- **자유설계연금형 / the proportional split** across two annuity forms, offered by three
  carriers, one in 10% units summing to 100% [S6 제19조⑤] [S4 별표1 주7] [S2] — it needs a
  joint payout state and is a minority feature.
- **Prospective commutation** by a living annuitant, retrieved only on a variable annuity [S10
  주7]; commutation on death inside the guarantee is in scope as a present-value identity, not
  as a separate decrement.
- **의료비인출**, the six **부득이한 사유** withdrawals and **배우자 승계** [S3 제21조④⑤]
  [S1] [S6] [S7] [S8] — real contract terms with a real tax effect, but no public frequency
  exists for any of them.
- **계약이전 / 계좌이체** [S1] — a wrapper-level movement, not an insurer cash flow beyond the
  transfer fee; its existence is carried into the lapse rationale instead.
- **납입면제 (premium waiver)**, absent from every retrieved product's terms (footnote 22)
  [S5].
- **부활 and 간편부활** — real, common and specific to this product family, but **not
  implemented**: on an annual grid a premium unpaid at `t` terminates the contract at `t` and
  there is no partial-year 납입최고 state to re-enter from, so lapse is absorbing and the lapse
  vector is net-of-부활 by construction (footnote 23) [REG-R25 제27조](#krlib-reg-r25) [S1] [S5]
  [S7] [S8].
- **청약철회, 품질보증해지 and 고지의무** — pre-inception and rescission machinery, scoped out
  explicitly; the model begins where cover is in force [REG-R25] [REG-R51].
- **이연퇴직소득** — retirement money rolled into a pension account changes the five-year test
  and the withholding formula [R6] [R9], but a 연금저축보험 written as pure individual savings
  holds none of it and the reference model does not carry it.

---

## Variations across insurers

1. **최저보증이율 ladder — the sharpest variation in the set, and it tracks the sale date
   rather than the carrier.** Observed: 1.25 / 1.00 / 0.50 at 5 and 10 years [S1] [S2] [S13];
   1.25 / 1.00 / 0.75 [S15]; 1.0 / 0.5 at 10 years [S6] [S7] [S11]; 1.5 / 1.0 at 10 years [S5]
   [S13]; **2.0 / 1.5** at 10 years on an older generation [S9]; **1.0 / 0.75 / 0.5 at 3 and 5
   years** — three bands stepping earlier than anyone else's [S4]; and **1.25 / 1.0 / 0.3** on
   the non-life form, the lowest long-duration floor observed [S8]. One carrier's own shelf
   carries two ladders side by side keyed to each product's 판매개시일 [S13], which is what
   establishes that the ladder is a **vintage** parameter. Composite: **1.25 / 1.00 / 0.50**,
   the modal current shape, with the first-band range 1.0–2.0% and the long-duration range
   0.3–1.5% recorded as the envelope.
2. **Expense shape — a level monthly loading versus a front-end charge recovered on
   surrender.** The direct-channel product charges 4.50% of premium a month for seven years and
   has **no surrender charge at all** [S1]; the postal product charges 6.02% in year 1, then
   4.22% from year 8 when the seven-year 유지보수 stops and 3.0% from year 11 when the ten-year
   판매보수 stops, and adds a 해지공제액 of ₩104,000 running off to zero over four years [S7]
   `[derived]`. No other retrieved carrier publishes either. The choice between the two is a
   **live design variable in this market** and the composite must state which it takes: it
   takes the first (footnote 9), with the second as a model input. It is visible at three
   months — 95.9% of premiums against 43.4% on a tied-channel product of the same carrier and
   year [S1] [S2].
3. **Annuity-phase charge.** 0.5% of the 연금연액 at two carriers [S1] [S7]; none disclosed
   at a third, whose implied factors run 0.6% the *other* way [S5] `[derived]`. Composite:
   0.5%, the only version that recovers the published figures at all (footnote 10).
4. **Annuity-form menu.** Life-annuity guarantee periods run from **20 years only** at the
   postal insurer [S7] through 10/20 [S1] [S2], 10/20/30 [S6], 10/20/100세 [S4] and
   10/20/30/100세 [S9] [S11] to **none at all** on the non-life form [S8]. Certain terms run
   from 10/15/20 [S1] [S2] [S7] to 5/10/15/20/25/30 [S9]. Composite: **종신연금형 10년보증 plus
   확정기간연금형 10/15/20**, the intersection of every life carrier's menu.
5. **Life insurer versus non-life insurer — the structural boundary.** The non-life form of the
   same statutory wrapper has **no 종신연금형, no annuitant mortality anywhere in the
   contract**, and a 연금지급기간 of 5 to 25 years [S8], exactly as the supervisor describes
   [R12]. It also names its rate 「연금저축 공시이율Ⅴ」, defines 해약공제액 as 미상각 신계약비,
   and cites 감독규정 제1-2조's 저축성보험 definition as the reason the annuity date is
   deferred where the fund would not otherwise exceed premiums paid [S8]. Composite: **the
   life-insurer form**; the non-life form is a different product and is not in the `krlib` set.
6. **Fund floor at annuitisation.** 100.1% of premiums paid at three carriers [S2] [S4] [S7];
   the functionally identical 「이미 납입한 보험료 + 1,000원」 at two more [S5] [S6]; not
   stated at two [S9] [S11]; and, on the non-life form, no floor but an **automatic deferral of
   the annuity date** until the 저축성보험 condition is met [S8]. Composite: **100.1%**, with
   the deferral mechanic carried as the disapplication rule (footnote 17).
7. **Participation.** Five 무배당 [S1] [S4] [S5] [S6] [S11] against three 배당 [S2] [S7] [S8],
   with one carrier selling both. The difference is not cosmetic: it changes the 표준해약공제액
   coefficient from 3% to 4% [REG-R20 주5](#krlib-reg-r20), and where a dividend arises it is applied as an
   **increase to the annuity or an addition to the instalment** — 「보험기간 중 발생한 배당금은
   계약소멸할 때 계약자에게 지급하거나 연금 지급개시 이후에 증액연금으로 수익자에게
   지급합니다」 [S2] — not as cash. The only published dividend history is the postal
   insurer's, whose 기준율 fell from 4.3 to 3.5 and whose aggregate fell **70%** over 2022–2024
   [S7] `[derived]`. Composite: **무배당** (footnote 1).
8. **Rate design.** One carrier departs from a pure declared-rate accumulation with a
   **hybrid**: a fixed 연복리 **3.5% 확정이율 for the first five contract years**, then the
   ordinary declared rate, floored at 1.0% / 0.5% [S11]. It is the only such design retrieved.
   Composite: excluded, and the composite is built so that a fixed opening rate is a
   *parameterization* — a crediting-rate vector by policy year — rather than a different
   chassis.
9. **Pricing rate for the expense and benefit structure.** Three carriers disclose it and all
   three give **연복리 2.5%**: 「보장부분에 적용한 적용이율은 연복리 2.50%이며, 동 이율은
   적립액 및 해약환급금을 보증하는 이율은 아닙니다」 [S1]; 예정이율 연단위 복리 2.5% [S7]; 「본
   상품의 계약체결비용 계산시 적용한 이율은 연복리 2.5%입니다」 [S5]. Composite: **2.50%**, and
   the spec repeats the carriers' own warning that it is **not a guarantee**.
10. **Issue age and underwriting.** 0세 at four carriers [S1] [S7] [S8] and 만19세 at one
    [S11]; 전건 무진단 at the postal insurer [S7] against a reserved underwriting right at
    three others [S1] [S2] [S8]. Composite: 0 as the envelope floor, no underwriting, anchor
    40.
11. **What does not vary, and each is a testable model property.** Every retrieved life-insurer
    연금저축보험: accumulates 순보험료 at a monthly-reset 공시이율 over a stepped compound
    floor; deducts 계약체결비용 and 계약관리비용 **monthly as a percentage of the basic
    premium**; pays the fund on death before annuitisation and nothing more; offers a
    종신연금형 with a guarantee period and a 확정기간연금형, computing the first on 연금사망률
    and 공시이율 and the second on 공시이율 alone; carries the annuity-mortality ratchet
    clause; forbids surrender once a life annuity is in payment; defaults the annuity to the
    tax-recognised maximum; allows 추가납입 up to 200% of basic premium inside the ₩18,000,000
    aggregate; and offers a payment holiday, a three-year reinstatement window and a simplified
    one-instalment reinstatement. Those ten are the invariant core of the composite [S1] [S2]
    [S3] [S4] [S5] [S6] [S7] [S9] [S11].

---

## Regulatory context

**Prudential — two regimes, live together since 2023.** K-IFRS 제1117호 「보험계약」, the
Korean adoption of IFRS 17 [REG-R60], and **K-ICS**, the economic-value solvency regime
[REG-R13], both commenced on **2023-01-01** under the same transitional provisions [REG-R14].
Korea switched liability measurement and capital measurement together and is four years into
living with the result; this is the sharpest structural difference from `jplib`, whose
economic-value regime commences in 2026. `krlib` computes neither ratio. What this product owes
the regimes is that its projection be re-runnable on a basis re-set at a stated valuation date,
over a twenty-five-year deferral followed by a life annuity — not a small property.

**The 해약환급금준비금 has no counterpart anywhere else in this repository, and this product is
one of the two it was built for.** Under 감독규정 제6-11조의6, at each balance-sheet date
including quarterly interim closes, the insurer compares its IFRS 17 liability for remaining
coverage against the aggregate **해약환급금 computed under 제7-66조제1항** plus 미경과보험료,
and appropriates any shortfall to a **surrender-value reserve inside 이익잉여금** — at
**company level**, not contract level [REG-R11]. Since 2025-06-11 an insurer whose K-ICS ratio
before transitional measures was 130% or more at the previous quarter-end appropriates only
**80%** of the shortfall [REG-R11]. It exists because a profitable in-force block can carry an
IFRS 17 liability materially below the aggregate contractual surrender value, and distributing
the difference would leave the insurer short if policyholders actually surrendered. On this
product the gap is the whole earnings profile: the 계약자적립액 is a contractual, guaranteed,
daily-accruing quantity and the IFRS 17 liability is not. `Pension_KR_S` does not compute it;
the reserve stood at **₩23.7tn at end-2022 and ₩32.2tn at end-2023** [REG-R11] [REG-R36].

**Product design is prescribed, and three of the prescriptions shape this contract directly.**
감독규정 제7-60조 requires that a 저축성보험's survival benefits **exceed** premiums paid
(제2호); that the 계약자적립액 accumulated at the **평균공시이율** exceed premiums paid at
납입완료, a test a 연금저축보험 may run at **평균공시이율 + 0.25%p** (제3호, 제4호), with a
2023 exemption for an annuity design that delivers a larger fund or annuity at the commencement
date than a compliant design would (제3의2호); that the death benefit be at least cumulative
premiums paid **except where the premium term ends at 80 or below** (제9호); and that every
금리연동형보험 set a **최저보증이율 or a 최저보증금액** (제10호, inserted 2022-12-22)
[REG-R16]. The first is why the 100.1% floor exists; the third is why this product has no death
cover; the fourth is why the guarantee ladder is not optional.

**Surrender values are regulated end to end.** 감독규정 제7-66조 sets the surrender value at
not less than the 계약자적립액 net of the 해약공제액, floored at zero; caps the 해약공제기간 at
seven years; requires the deduction to be the **표준해약공제액 of 별표 14**; and prescribes
monthly accrual of the account before 납입완료 and daily accrual afterwards [REG-R19]. 별표 14
then gives 연금저축보험 its own coefficient — **4% of the annual net premium, 3% if 무배당** —
denies it the 6% concession available to other whole-of-life survival annuities, caps the
저축성보험 coefficient at a twelve-year premium term, and subtracts the acquisition amount
loaded into the premium discounted at the **평균공시이율** [REG-R20] [R14]. The
무해지/저해지환급형 dispensation of 제7-66조제4항, which dominates Korean *protection* sales,
is not used on this product: a 연금저축보험 has a full surrender value from the first month and
no cliff at 납입완료 [REG-R19].

**The crediting rate is a regulated construction, not a company choice.** 감독규정
제7-65조제3항 requires the 공시이율 to be the 공시기준이율 adjusted by a 조정률, and 시행세칙
별표 27 fixes the 공시기준이율 as a weighted average of an external index rate — 국고채(5년),
회사채(무보증 3년, AA-), 통화안정증권(1년) and CD(91일), on a three-month moving average ending
two months before application — and the insurer's own **운용자산이익률**, with the external
weight **α capped at 60%** and held constant through the business year [REG-R18] [REG-R24].
That cap is why Korean declared rates move sluggishly against government-bond yields and why
`krlib` models the crediting rate as a slow-moving `[std]` scalar rather than as a function of
a curve. The **평균공시이율** is defined at 감독규정 제1-2조제13호 and computed by the
supervisor; it is **2.50% for 2026**, down from 2.75%, the first fall in the series since 2021
[REG-R9] [REG-R48].

**Contract law and conduct.** 보험업법 supervises the undertaking; **상법 제4편 보험** governs
the contract and is **one-way mandatory** — 제663조 forbids any agreement varying the Part to
the disadvantage of the policyholder, insured or beneficiary [REG-R49]. Every clause quoted
under *Contractual mechanics* is drafted against it, and 시행세칙 별표 15's 표준약관 is where
the drafting is standardized [REG-R25]: the cooling-off right rests on 금융소비자보호법 제46조
[REG-R51], 품질보증해지 on 상법 제638조의3제2항 and the three-year limitation on 상법 제662조
[REG-R49], and the **보험나이** definition — nearest birthday by a six-month rule, with the
약관's own worked example — is 표준약관 제21조 [REG-R25].

**Tax.** The wrapper is a creature of 소득세법: 제20조의3제1항제2호 and 시행령
제40조의2제1항제1호 define the account; 제59조의3 gives the credit at 12% or 15% on ₩6,000,000
/ ₩9,000,000; 시행령 제40조의2 sets the ₩18,000,000 ceiling, the three-limb 연금수령 test and
the 연금수령한도; 제129조제1항제5호의2 sets the withholding bands and the **3% 종신계약 rate in
force from 2026-01-01**; 제14조제3항 fixes the ₩15,000,000 aggregation threshold and routes
연금외수령 into separate taxation; and 제64조의4 gives the 15% election above the threshold
[R1]–[R6] [R9] [R11] [REG-R56]. Two limitations are recorded rather than hidden. The
**연금수령한도 formula and the withholding age-band table render as images** in the official
text and did not extract at either retrieval; the formula was recovered verbatim from a filed
약관 부록 reproducing 시행령 제40조의2제2항–제5항 [S3] and the bands from the tax authority and
the legislation office [R9] [R11]. And **the 13.2% / 16.5% grossed-up rates are [unverified]
arithmetic**, because the 지방세법 imposing the surtax was not retrieved [REG-R56]. Separately,
the boundary against the non-qualified route is worth naming: a 종신형 연금보험 outside the
연금저축 wrapper is relieved instead under 소득세법 제16조제1항제9호 and 시행령 제25조제4항, on
five conditions including that any guarantee period fall **within the 국가데이터처 기대여명
연수** [REG-R58] [REG-R38] — a different product, a different relief, and out of scope here.

**Depositor protection.** 예금자보호법 시행령 제18조제7항 sets the limit at **₩100,000,000**,
in force from **2025-09-01**, and applies it to four separate buckets, of which the second is
the combined total of **연금저축계좌 claims** [REG-R52] [REG-R32]. A `Pension_KR_S`
policyholder's protection is therefore separate from the ₩100,000,000 covering their other
insurance claims against the same insurer — exactly what the 2026-vintage carrier documents
state [S2] [S6] [S11] and what the 2024 and 2016 documents, still quoting ₩50,000,000, do not
[S4] [S5]. 연금저축펀드 is not covered at all; 신탁 and 보험 are [S16] [R12].

**Actuarial provenance, stated once.** 보험개발원 holds the statutory office of
보험요율산출기관 under 보험업법 제176조 and files 참조순보험요율 with the supervisor; there is
no publication obligation and the retrieved 보도자료 listing carries no 경험생명표 or life-side
참조순보험요율 item [REG-R4] [REG-R34] [R16] [R17]. That is a finding about that channel and
about the life side, not about the bureau, which publishes a dated 장기손해보험 참조순보험요율
display — 암 발생률 and 질병입원율 by age and sex — on another page of the same site
[REG-R61], which is why morbidity elsewhere in `krlib` can be sourced where this product's
mortality cannot. The 제10회 경험생명표, applied to new
business from 2024-04, is public only as summary statistics [REG-R33] [R18]. **No qx
table of any Korean industry basis was retrieved in either research pass.** `Pension_KR_S`'s
`mort_table.csv` is therefore a **[std]** construction on the annuitant basis, carrying a
`provenance` column on every row. It is fitted to the six carrier-published annuitant rates
above [S1] [S7] and calibrated so that the implied factor for a 65-year-old male at 2.15% with
a ten-year guarantee reproduces the **23.70** the published illustrations imply [S2]
`[derived]`. The two published 경험생명표 summary statistics [REG-R33] and the 국가데이터처
population figures [REG-R38] are the public series it is **compared against** and not inputs to
it — the single-year 완전생명표 qx tables [REG-R39] were not downloaded in either research pass
and nothing here rests on them. **It is never presented as the 경험생명표.**

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-pension_savings-r1
[R10]: #krlib-pension_savings-r10
[R11]: #krlib-pension_savings-r11
[R12]: #krlib-pension_savings-r12
[R13]: #krlib-pension_savings-r13
[R14]: #krlib-pension_savings-r14
[R16]: #krlib-pension_savings-r16
[R17]: #krlib-pension_savings-r17
[R18]: #krlib-pension_savings-r18
[R19]: #krlib-pension_savings-r19
[R2]: #krlib-pension_savings-r2
[R20]: #krlib-pension_savings-r20
[R21]: #krlib-pension_savings-r21
[R22]: #krlib-pension_savings-r22
[R24]: #krlib-pension_savings-r24
[R3]: #krlib-pension_savings-r3
[R4]: #krlib-pension_savings-r4
[R5]: #krlib-pension_savings-r5
[R6]: #krlib-pension_savings-r6
[R7]: #krlib-pension_savings-r7
[R8]: #krlib-pension_savings-r8
[R9]: #krlib-pension_savings-r9
[REG-R11]: #krlib-reg-r11
[REG-R13]: #krlib-reg-r13
[REG-R14]: #krlib-reg-r14
[REG-R16]: #krlib-reg-r16
[REG-R18]: #krlib-reg-r18
[REG-R19]: #krlib-reg-r19
[REG-R20]: #krlib-reg-r20
[REG-R22]: #krlib-reg-r22
[REG-R24]: #krlib-reg-r24
[REG-R25]: #krlib-reg-r25
[REG-R27]: #krlib-reg-r27
[REG-R29]: #krlib-reg-r29
[REG-R32]: #krlib-reg-r32
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R36]: #krlib-reg-r36
[REG-R38]: #krlib-reg-r38
[REG-R39]: #krlib-reg-r39
[REG-R4]: #krlib-reg-r4
[REG-R48]: #krlib-reg-r48
[REG-R49]: #krlib-reg-r49
[REG-R51]: #krlib-reg-r51
[REG-R52]: #krlib-reg-r52
[REG-R56]: #krlib-reg-r56
[REG-R58]: #krlib-reg-r58
[REG-R60]: #krlib-reg-r60
[REG-R61]: #krlib-reg-r61
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
