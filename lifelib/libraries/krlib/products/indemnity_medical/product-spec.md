# Product Specification

**Status:** Draft, 2026-09-03 (access date for every citation: 2026-09-03).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modelling of a Korean 실손의료보험 (*silson uiryo boheom*, indemnity
medical insurance) contract. It does not describe any single insurer's product — but the
sense in which it is a composite is unusual and must be stated at the top, because it
governs how the rest of the document reads. **The benefit definition of a Korean 실손
contract is not written by the carrier.** It is written by the supervisor, as the
표준약관 (*pyojun yakgwan*, standard policy conditions) annexed to the
보험업감독업무시행세칙 (*boheomeop gamdok eommu sihaeng sechik*, Detailed Enforcement Rules
for Insurance Business Supervision) at 별표 15, made under 제5-13조제1항 [S1] [REG-R23]
[REG-R25]. A carrier's own 실손 wording reproduces that text; the two carrier booklets
retrieved for this product do so almost verbatim [S3] [S5]. So the composite here is
**not** an average over five carriers' contracts, as it is in the sister libraries. The
benefit half of this document is the 표준약관 itself, cited clause by clause, and the
composite work is confined to the three things a carrier actually chooses — the
보험가입금액 (sum insured / annual limit) menu, the 가입나이 (issue-age) envelope and the
band-1 discount factor — plus the pricing basis, which is never public anywhere in Korea.

Facts carrying a source tag — [S#] (primary product documents: the 표준약관 itself,
carrier 약관 (*yakgwan*, policy conditions), 상품요약서 (*sangpum yoyakseo*, product
summary) and the trade associations' 공시 (*gongsi*, statutory public disclosure)) and
[R#] (product-specific regulatory, supervisory and actuarial references), both numbered per
`_research/indemnity-medical.md` and resolved in `sources.md` (same directory; numbering
frozen, never renumbered), and [REG-R#] (the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is distinct) —
were extracted from the cited document. Values marked **[std]** are standardizations
introduced for the reference implementation; each [std] table row carries a numbered
footnote giving the rationale and, where the research file brackets it, the observed range.
Facts the research file could not verify are flagged [unverified].

**Which generation this is.** The market labels each supervisory redesign a 세대 (*sedae*,
generation), and the 금융감독원 (Financial Supervisory Service, FSS) fixes the sale windows
in its own annual statement [R7]: 1세대 to 2009-09, 2세대 2009-10 to 2017-03, 3세대 2017-04
to 2021-06, **4세대 2021-07 to 2026-05**, 5세대 from 2026-05-06. **The representative
product specified here is 4세대**, the generation whose defining feature is the separation
of 급여 (*geubyeo*, treatment covered by National Health Insurance) from 비급여
(*bigeubyeo*, treatment outside it) into a main contract and a rider priced and re-rated
apart. Two dates bound it. 4세대 stopped being sold on 2026-05-05 and 5세대 has been on
sale since 2026-05-06 [R5]; and the first 4세대 policies reach their five-year 보장내용
변경주기 in **July 2026**, from which point the in-force 4세대 book is progressively
re-entered into 5세대 [R7]. This document therefore specifies a contract that is closed to
new business and whose in-force population is in the first months of a five-year migration.
That is deliberate: the 4세대 wording is the only generation for which the complete
parameter set is stated in one retrieved supervisory table [R5], it is the generation the
house brief fixes for the library, and the mechanics it carries — the 급여/비급여 split,
the annual limits, the 비급여 할인·할증 experience rating, the one-year renewal and the
five-year re-entry — are all carried forward into 5세대 with different levels. Section
*Variations across insurers* states the 5세대 deltas so that a
reader can re-parameterize the model into the live generation without a second document.

**This product stands alone.** It inherits nothing from
[whole life (종신보험)](../whole_life/product-spec.md) or from
[cancer (암보험)](../cancer/product-spec.md), and no other `krlib` product states a delta
against it. The reason is structural rather than editorial: it is the only contract in this
repository whose benefit is a **reimbursement of an incurred cost**. 보험업감독규정
제7-63조 requires a 제3보험 product to be designed so that the amount covered is stated
**either** as a fixed sum **or** on the basis of 「실제 발생하는 손해(이하 "실손해"라
한다)」 [REG-R17] [R19]. 실손해 — *silsonhae*, actual loss — is the root of the product's
name, and this is the only `krlib` product that takes that branch of the sentence. Every
other 제3보험 product in the library ([cancer](../cancer/product-spec.md),
[long-term care](../long_term_care/product-spec.md),
[children's](../child/product-spec.md) and the CI limb of
[CI insurance](../ci_insurance/product-spec.md)) takes the 정액 (*jeongaek*, fixed-sum)
branch. There is consequently **no 보험가입금액 that determines a claim** here, only an
annual limit that caps one; the claim is a draw from the insured's actual medical spend,
passed through a stack of co-payment percentages, per-visit deductibles, per-item money and
count caps and an annual aggregate. The modelling consequence is stated once and should be
carried into every downstream document: this is **claim frequency × claim severity ×
contractual deductible-and-limit machinery**, not a rate times a sum assured.

---

## Product overview and market role

**Statutory classification.** 실손의료보험 is a 제3보험 (*je-sam boheom*, third-sector)
contract. 보험업법 제2조제1호다목 defines a 제3보험상품 as one covering 「사람의 질병ㆍ상해
또는 이에 따른 간병」, expressly carved out of the 손해보험상품 definition in 나목, and
제4조제1항제3호 lists the three licence classes it comprises — 상해보험, 질병보험,
간병보험 [REG-R1]. 보험업법 시행령 제1조의2제4항 closes the list at exactly those three
[REG-R7]. A 실손 contract sits in 질병보험 and 상해보험 at once: the 표준약관 writes the
cover as four 보장종목 (*bojang jongmok*, cover items) paired across the injury/sickness
axis and the 급여/비급여 axis [S1 제1조]. **Both life and non-life insurers write it**, by
force of 보험업법 제4조제3항, which deems a licensee for all 생명보험 종목, or for all
손해보험 종목 excluding 보증 and 재보험, to hold the 제3보험 licence [REG-R1]. At
2025-12-31 the in-force split was 손해보험회사 30.28 million policies against
생명보험회사 5.94 million — the non-life sector holds **83.6%** of the book [R7].

**It is the second national health insurance, and the supervisor says so.** The 금융감독원
uses the phrase 「제2의 건강보험 역할」 in its own annual statement and dates the product's
service in that role to its first sale in **1999** [R7]. The scale supports the phrase:
**36.22 million individual policies** in force at 2025-12-31, about **40 million insured
persons** at 2024-12-31 against a population near 51 million [R4] [R7], **₩17.0 trillion
(17.0조원)** of claims paid in 2025 against **₩18.0 trillion (18.0조원)** of premium income
[R7]. Household penetration reached 3,900만명, about 75% of the population, as early as
2020-12-31 [R1].

**What it actually reimburses, and why that makes it different from every other product
here.** The FSS's own one-line definition: 「실손의료보험은 피보험자(환자)가 부담하여
실제 발생한 의료비[급여 본인부담금 + 비급여] 중 일정 금액을 보상하는 보험상품」 [R7].
The square-bracketed decomposition is the whole model. 국민건강보험법 제41조제2항 defines
요양급여 as covering 「제4항에 따라 보건복지부장관이 비급여대상으로 정한 것을 제외한 일체의
것」 — a **negative list**, so 비급여 is a residual defined by ministerial designation
[REG-R53]. The insured loss this product pays is therefore (i) the statutory co-payment the
patient bears on treatment inside the public list, plus (ii) the whole of the treatment
outside it. Neither leg is under the insurer's control, and the second is not under any fee
schedule's control either: 비급여 prices are set by the provider, and the 건강보험심사평가원
price survey found 도수치료 (manual therapy) quoted anywhere between ₩5,000 and ₩600,000
across Seoul hospitals [R2]. **That is the product's structural problem in one number**,
and it is why the supervisor has redesigned the contract four times in twenty-seven years.

**The public layer underneath.** 국민건강보험공단's 진료비 실태조사 measures the split of
national treatment cost. In 2024 the total was **₩138.6조**, of which the scheme bore
₩90.0조, the patient's statutory co-payment ₩26.8조 and 비급여 ₩21.8조; the coverage ratio
(보장률) was **64.9%**, with 법정 본인부담률 19.3% and 비급여 본인부담률 15.8% [R9]
[REG-R41]. The addressable base for this product is the last two components together —
**₩48.6조** — of which 실손 actually paid **₩15.2조** in 2024 [R8], i.e. **31.3%**. The
growth rates are what matter for pricing: in 2024 the scheme's own outlay grew 4.3%,
statutory co-payment 1.0% and **비급여 8.1%** [R9]. 비급여 is compounding at roughly twice
the rate of the whole, and it is the half of the claim that has no public price.

**Where the money goes is not where public money goes.** Claims by provider class in 2025:
의원 (clinics) 32.0% of claims, 병원 (hospitals) 21.8%, 종합병원 17.6%, 상급종합병원 15.0%
— against NHIS's own 2024 covered-spend shares of 상급종합 22.3%, 종합병원 21.4%, 병원
10.7%, 의원 27.9% [R7]. The 비급여 share **inside** each provider class explains it: 41.2%
at 상급종합, 42.3% at 종합병원, but **70.6% at 병원** and **83.5% at 요양병원** [R7], which
tracks the public statistician's own coverage ratios by class — 상급종합 72.2%, 종합병원
66.7%, **병원 51.1%**, 의원 57.5% [R9] [REG-R41]. Provider mix is a first-order variable in
this product in a way it is in nothing else in the library.

**The experience.** The FSS states the break-even 경과손해율 (earned loss ratio, defined as
발생손해액 ÷ 보험료수익) at 「약 85% 수준」 [R7], the residual 15% being 손해조사비 and
사업비 — which it quantifies for 2025 as about ₩2.9조 on ₩18.0조 of premium, **16.1%**
[R7]. Against that benchmark the whole line ran at 101.0% in 2025, and 4세대 specifically
at 91.5% (2022), 113.8% (2023), 111.9% (2024) and **115.1%** (2025) [R7] [R8]. The
underwriting result was **−₩1.87조** in 2025 [R7]. A model of this product that produces a
self-supporting rate from inception is not modelling the Korean market; § *Rate adequacy,
the five-year grace and why a new generation is under-priced* explains why the
under-pricing is a regulatory artefact and not only an experience one.

**Claim concentration, which no fixed-sum product shares.** 「계약자의 9%가 보험금의 80%를
수령」 and 「계약자의 65%가 보험금을 미수령」 [R4], restated at 2025-12-31 as 65% of
insureds claiming nothing and the **top decile taking about 74% of all claims** across
fourteen carriers [R5] [R6]. A projection that applies a mean claim per policy without a
zero-claim mass of roughly 65% will misstate everything downstream of the deductible,
because the deductible bites hardest exactly where the mass is.

**What is not public, and it is the whole pricing basis.** 보험개발원 (Korea Insurance
Development Institute, KIDI) is the statutory 보험요율 산출기관 under 보험업법 제176조
[REG-R4], and its published 장기손해보험 참조순보험요율 (reference net rates) covers
일반상해, 교통상해, 질병 사망률, 후유장해, 입원율, 암 발생률, 비용손해, 재물손해 and
배상책임 — **실손의료보험 is not among them** [R20]. This is a positive finding, not an
unfetched document: there is **no public Korean indemnity-medical morbidity or severity
basis at all**. The 산출방법서 (statement of the method of calculating premiums and
surrender values), where the 예정위험률 and 예정사업비율 actually live, is a 기초서류 filed
under 보험업법 제5조제3호 and 제127조 and is **not published** [REG-R2]. Every frequency,
severity and expense parameter in `Medical_KR_S` is consequently **[std]**, constructed from
the aggregate experience the supervisor does publish [R7] [R8] [R12] and marked as such at
the point of use. Every *contractual* parameter, by contrast, is sourced to the 표준약관 —
which is why this product's specification reaches a precision no other product in this
repository reaches.

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | 4세대 실손의료보험: 기본형 실손의료보험(급여 실손의료비) as 주계약 plus 실손의료보험 특별약관(비급여 실손의료비) as 특약; 1년만기 순수보장성, no surrender value | [S1] [S3] |
| Generation and sale window | 4세대, sold 2021-07-01 to 2026-05-05 | [R1] [R5] [R7] |
| Regulatory class | 제3보험 — 상해보험 and 질병보험 (보험업법 제2조제1호다목, 제4조제1항제3호; 시행령 제1조의2제4항); writable under either a life or a non-life licence | [REG-R1] [REG-R7] |
| Benefit basis | **실손해** (indemnity for actual loss), the second branch of 감독규정 제7-63조 — the only such product in `krlib` | [REG-R17] [R19] |
| Source of the benefit definition | 보험업감독업무시행세칙 [별표 15] 표준약관, 제5-13조제1항 관련, effective 2021-07-01 — not a carrier document | [S1] [REG-R23] [REG-R25] |
| 보장종목 (cover items) held | All five: 상해급여형, 질병급여형 (주계약); 상해비급여형, 질병비급여형, 3대비급여형 (특약) | [S1 제1조]; election **[std]** (1) |
| Annual limit (연간 보험가입금액) | **₩50,000,000 (5천만원)** per 보장종목 per policy year, inpatient and outpatient combined; 상해 and 질병 carry separate limits | ceiling [S1 제5조] [REG-R17]; election **[std]** (2) |
| Whole-contract annual limit | **₩100,000,000 (1억원)** — 급여 5천만원 + 비급여 5천만원 | [R1] [R5 참고1](#krlib-indemnity_medical-r5) |
| Per-visit outpatient cap | **₩200,000 (20만원)** | ceiling [S1 제5조제5항]; election **[std]** (2) |
| Issue age (가입나이) | **0–65** (만나이) | not retrieved for 4세대; **[std]** (3) |
| Age basis — contract | **보험나이** (*boheom nai*, insurance age): 만나이 at 계약일 with a fraction under six months discarded and six months or more rounded up, incremented at each 계약해당일 | [S1 제21조] [REG-R25] |
| Age basis — model | **만나이** (*man nai*, age last birthday) | **[std]** (4) |
| Policy term (보험기간) | **1 year**, automatically renewed on the day after expiry unless the policyholder declines | [S3] [S5] |
| Renewal (갱신) | Annual, at the 보험요율 in force on the renewal date and at the attained 보험나이; increase capped at **±25% a year excluding the age effect**, per 위험구분단위 | [S1 제30조] [REG-R17 제7-63조제2항제3호](#krlib-reg-r17) [R6] |
| Benefit-change cycle (보장내용 변경주기 / 재가입주기) | **5 years** — the contract re-enters the generation then on sale | [R1] [R2] [REG-R17 제7-63조제2항제6호나목](#krlib-reg-r17) |
| 재가입 나이 (re-entry age ceiling) | To 보험나이 **99** | [S3]; **[std]** (5) |
| Maximum cover age | To the 계약해당일 at 보험나이 **100** | [S3] [S4] |
| Underwriting | 계약 전 알릴 의무 (*gyeyak jeon allil uimu*, pre-contract duty of disclosure) on a written or on-screen questionnaire; no medical examination in the retail and direct channels; **no health underwriting at 재가입** | [S1 제23조제1항] [REG-R25]; channel **[std]** (6) |
| Lives basis | Single life | [S1] [S3] |
| Death benefit | **None.** On death from a cause the policy does not cover, the insurer pays the 계약자적립액 and the 미경과보험료 of 감독규정 제7-66조제5항 and the contract terminates — on a one-year pure protection contract the 계약자적립액 is nil and only unearned premium is returned | [REG-R17 제7-63조제1항제1호](#krlib-reg-r17) [REG-R25 제22조](#krlib-reg-r25); nil level **[std]** (7) |
| Surrender value (해약환급금, *haeyak hwanreupgeum*) | **None** — 「이 상품은 1년만기 순수보장성 상품으로 해약환급금이 발생하지 않습니다」 | [S3] |
| Waiting period (면책기간) | **None** on the general cover; cover attaches at 보장개시. The only deferred item is a **two-year** wait on the 불임관련 질환 급여 cover introduced at 4세대 | [S1 제24조] [R1] |
| **Anchor model cell** | Male, 만나이 **40** at issue, both parts held with all five 보장종목, ₩50,000,000 annual limit per 보장종목, ₩200,000 per-visit cap, 월납 office premium **₩11,982** split 급여 ₩4,793 / 비급여 ₩7,189, band 2 (유지) at inception, 무사고 할인 not yet earned | premium [R1]; split and cell **[std]** (8) |

Footnotes to [std] rows:

1. The 표준약관 makes each 보장종목 separately electable and 5세대's Q&A confirms four
   permitted combinations of base and riders as the design intent [S1 제1조] [R6]. The
   composite holds **all five**, because the 비급여 특약 is the whole point of the
   generation — it is the unit the experience rating applies to — and because the FSS's own
   premium statistics are quoted 「전 담보 기준」, all covers held [R7] [R8]. Holding only
   the 주계약 is a model-point switch, not a separate specification.
2. The 표준약관 sets a **ceiling** and leaves the level to the carrier: 「5천만원 이내에서
   회사가 정한 금액 중 계약자가 선택한 금액」, and 「통원 1회당 20만원 이내에서…」
   [S1 제5조]. No 4세대 carrier menu was retrieved. One carrier's **5세대** menu is
   ₩50,000,000 / ₩30,000,000 / ₩10,000,000 on the 급여 and 중증 covers with the per-visit
   cap stepping ₩200,000 / ₩150,000 / ₩100,000, and ₩10,000,000 / ₩6,000,000 / ₩2,000,000
   on the 비중증 rider [S3]. The composite takes the **maximum** on both, because it is the
   market-standard election, because every published premium comparison is quoted on the
   full limit [R1] [R5] [R7], and because a limit set below the ceiling only ever truncates
   the severity distribution further — a strictly simpler model change than the reverse.
3. **Not retrieved for 4세대 or 5세대.** The 표준약관 sets no issue age; it is a
   사업방법서 matter and the 사업방법서 is not published [REG-R2]. The only retrieved range
   is **0–49** on one direct-channel 2세대 product [S4]. Two boundaries frame the [std]
   choice: 감독규정 제7-63조제2항제6호다목 requires an insurer covering ages 75 and over to
   sell or hold a **노후실손** product [REG-R17], and the 노후실손 and 유병력자실손
   families exist precisely to underwrite lives the standard product declines, with issue
   ages raised to **90** on both from 2025-04-01 [R17]. The composite takes **0–65**: a
   whole-of-working-life envelope that stays clear of the 노후실손 boundary, covers the
   40-year-old anchor and the child issue ages the market writes, and is wide enough to
   exercise the age slope. Flagged as the widest single [std] in this document.
4. **The contract and the model use different age conventions and both must be stated.**
   The contract prices and renews on 보험나이, a nearest-birthday age computed by the
   six-month rule, with the 표준약관's own worked example: 생년월일 1988-10-02, 계약일
   2014-04-13, a difference of 25년 6월 11일 ⇒ **26세** [S1 제21조] [REG-R25]. The model
   carries **만나이**, because every calibration statistic available for this product —
   the NHIS coverage ratios by age band [R9], the 생명표 mortality decrement [REG-R38] and
   the FSS premium series [R7] [R8] — is compiled on 만나이, and because a deterministic
   single-cell projection cannot represent the distribution of issue dates within the year
   that separates the two conventions. The two differ for **half of all issue dates**, so
   the difference is a half-year of age on average and is recorded here rather than
   silently absorbed.
5. The re-entry age ceiling is a carrier parameter within the supervisory framework.
   Observed: **15–99** on a 2세대 product [S4] and **to 99** on a 5세대 product [S3]. No
   4세대 value was retrieved. The composite takes 99, the value both retrieved documents
   share at the upper end, which with the maximum cover age of 보험나이 100 means the last
   re-entry buys a final year of cover.
6. Neither retrieved 4세대-relevant document states an underwriting route. The
   표준약관 family's 계약 전 알릴 의무 clauses assume a written questionnaire [REG-R25], and
   both retrieved carrier products are direct-channel [S3] [S4]. The composite is
   questionnaire-underwritten with no medical examination — the retail norm — and treats
   substandard and declined lives as out of scope, since the market's answer to them is the
   separate **유병력자실손** family [R17].
7. 감독규정 제7-63조제1항제1호 requires *every* 제3보험 product to pay the 계약자적립액 and
   the 미경과보험료 on non-covered death, and the 표준약관 제22조 implements it
   [REG-R17] [REG-R25]. On a one-year contract with no savings element the 계약자적립액
   accrued under the 산출방법서 is nil to the precision this model works at, so the payment
   reduces to the return of unearned premium — which is also what 상법 제649조 gives a
   policyholder who cancels mid-term [REG-R49]. The composite sets it to unearned premium
   and no more. **This is the only place in `krlib` where that provision has no financial
   content**, and it is worth saying because in
   [cancer](../cancer/product-spec.md) and [long-term care](../long_term_care/product-spec.md)
   the same clause forces an account balance into a non-savings product.
8. **₩11,982 per month is the single best published new-business premium anchor for 4세대**:
   the joint FSC/FSS launch release prints it as the 4세대 premium for a **40세 남자** on a
   10-carrier 손해보험 average as at 2021-06, against 1세대 ₩40,749, 2세대 ₩24,738 and
   3세대 ₩13,326 for the same insured [R1]. The 급여/비급여 split is **[std]** at 40/60 —
   see footnote (10) and § *The premium split between the two priced
   units*, which sets out the two published values and why 60% was taken. Age 40 is also the
   기준연령 요건 of 감독규정 제1-2조제2호 — 「전기납 및 월납 조건으로 남자가 만 40세」 —
   so the anchor cell is the cell Korean supervisory disclosure is quoted on [REG-R9].

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium structure | **Natural (step-rated) premium on a one-year renewable term**: no level premium, no reserve accumulation, no 예정이율 discounting over more than one year | [S1 제30조] [S3] |
| Frequency (납입주기) | 월납 (monthly), level within the policy year | [S3] [S4]; **[std]** (9) |
| Premium-paying period | Coterminous with the one-year 보험기간; premiums cease on termination | [S1] [S3] |
| Priced units | **Two**, re-rated separately: the 급여 주계약 and the 비급여 특약. 「급여, 비급여 각각의 손해율에 따라 보험료가 조정되어…」 | [R1]; split level **[std]** (10) |
| 비급여 share of the total premium | **60%** when both parts are held | [R2]; **[std]** (10) |
| Rating factors | 성별 × 보험나이; 보장종목 elected; 보험가입금액 and per-visit cap elected; the 요율 상대도 band on the rider; 무사고 status | [S1] [S7]; composite **[std]** (11) |
| Published rate scale | **None exists.** No age × sex scale for 4세대 or 5세대 was obtainable; the association's comparison grid is form-gated | gap [S6] [S7]; **[std]** (11) |
| Anchor office premium (영업보험료) | **₩11,982** per month total — 급여 ₩4,793, 비급여 ₩7,189 | [R1]; split **[std]** (10) |
| Age loading at renewal | **4.0%** of the age-adjusted prior base premium per year of attained age | [S1 제30조 illustration]; **[std]** (12) |
| Renewal corridor | Base premium may move by at most **±25%** a year excluding the age effect, per 위험구분단위; exception only where the insurer is under 경영개선권고/요구/명령 | [S1 제30조제2항] [S1 특별약관 제6조제2항] [REG-R17 제7-63조제2항제3호](#krlib-reg-r17) [R6] |
| Experience relativity (요율 상대도) | Five bands on the **rider net premium only**: 1단계 (할인), 2단계 100%, 3단계 200%, 4단계 300%, 5단계 400%, keyed to the prior 12 months' 비급여 claims | [S1 특별약관 제6조제3항] [REG-R25]; band-1 factor **[std]** (13) |
| Band-1 discount factor | **−4.25%**, *solved* from revenue neutrality on the [std] band distribution rather than fixed | [S1]; **[std]** (13) |
| Band distribution at commencement | 1단계 72.9%, 2단계 25.3%, 3단계 0.8%, 4단계 0.7%, 5단계 0.3% | [R12]; **[std]** (13) |
| Surcharge floor | No surcharge at all below **₩1,000,000** of prior-year 비급여 claims | [S1 특별약관 제6조제4항] |
| Relativity exemptions | 비급여 claims arising from a 국민건강보험법 산정특례 condition (cancer, cerebrovascular, cardiac, rare and intractable disease), and all claims of an insured graded **장기요양 1등급 or 2등급** | [S1 특별약관 제6조제3항] [REG-R54] |
| 무사고 할인 (no-claim discount) | **10%** of the whole office premium — 급여 and 비급여 together — after **two** consecutive years with no 비급여 claim, excluding 4대 중증질환 claims from the test | [R1] [S3] |
| 의료급여 수급권자 할인 | 5% of the office premium at one carrier; **not** in the composite | [S3]; scope **[std]** (14) |
| Premium waiver (납입면제) | **None.** No 납입면제 provision appears in either retrieved 실손 wording | [S1] [S3]; absence **[unverified]** (15) |
| Expense loading | **16.0%** of office premium (손해조사비 plus 사업비), split acquisition 6% / maintenance 7% / claim handling 3%. `Medical_KR_S` charges the first two on office premium and the third on **claims**, the two bases coinciding at a loss ratio of 100% — about where this line has actually run | aggregate **16.1%** [R7]; the 16.0% rounding, the split and the bases **[std]** (16) |
| Rate-adequacy duty | The net rate's adequacy must be verified **annually** against experience, with up to **five years' grace** for genuinely new cover | [R12] [REG-R17 제7-63조제2항제6호가목](#krlib-reg-r17) |
| Price-index disclosure | The **보험가격지수** must be explained to the policyholder **at every renewal** of a 실손 contract, not only at sale | [REG-R22 제7-45조제7항](#krlib-reg-r22) |

9. Both retrieved carrier products quote monthly premiums and the whole published FSS
   premium series is monthly [R7] [R8] [S3] [S4]. Monthly is why `Medical_KR_S` runs on a
   monthly grid. No 연납 or 일시납 variant was retrieved and none is modelled.
10. **Two published values, and they differ.** The FSC/FSS FAQ states that when both parts
    are held the 비급여 특약 is 「전체 보험료의 60% 수준」 and works an example at 급여
    ₩5,000 + 비급여 ₩8,000 = ₩13,000 for a 45-year-old male, a **61.5%** rider share [R2].
    The 표준약관's own renewal illustration implies something lower: solving its band-2 and
    band-5 rows at renewal +1, `g + n = 18,200` and `g + 4n = 44,818`, gives n = ₩8,873 and
    g = ₩9,327, a **48.75%** rider share [S1 제30조] [S1 특별약관 제6조]. The composite
    takes **60%**, because [R2] is a statement about the market as sold while the 표준약관
    figure is a stylised illustration at an unnamed age, and because 60% sits between the
    illustration and the FAQ's own worked example. The share matters more than its size
    suggests: the experience relativity multiplies **only** the rider, so a band-5
    policyholder pays 0.40 + 0.60 × 4.00 = **2.80×** the base total premium at 60%, but only
    0.5125 + 0.4875 × 4.00 = 2.46× at 48.75%.
11. The rate structure is unobtainable in public. The 손해보험협회 comparison tool is
    filtered by **성별** and **보험나이** and by nothing else, which is the disclosure's own
    confirmation that the scale is an age × sex table [S7]; but the grid is POST-driven and
    returned 「조회된 내용이 없습니다」 to a plain fetcher, and the online marketplace
    returned only its search form [S7]. The scale in `Medical_KR_S` is therefore a **[std]**
    construction anchored on four published point values — ₩11,982 (40세 남, 4세대,
    2021-06) [R1]; ₩22,000 (40대 남, 4세대, 2025) [R7]; ₩178,489 and ₩126,773 (60대 여,
    1세대 and 2세대, 2026) [R5]; ₩16,000 (40대 남, 5세대, 2026) [R5] — and on the age slope
    of footnote (12).
12. **The only published age-slope datum in any retrieved document**, and it is derived
    rather than stated. The 표준약관's renewal illustration prints a 나이증가분 of 560, 728,
    946, 1,230 and 1,599 against base premiums of 14,000, 18,200, 23,660, 30,758 and 39,985
    [S1 제30조]; each is exactly **4.0%** of the previous year's base. The illustration also
    settles the order of operations, which a careless reading gets wrong: its
    「기초율 증가분 = 전년도 기준보험료 × 25%」 is loose, because 3,640 is 25% of
    14,560 = 14,000 × 1.04, not of 14,000. The recursion the illustration actually obeys is
    `P(y) = P(y−1) × (1 + a) × (1 + b)` with a = 0.04 and |b| ≤ 0.25 — the corridor applies
    to the **age-adjusted** prior premium. Reproducing that: 14,000 → 18,200 → 23,660 →
    30,758 → 39,985 → 51,980, matching every printed row. A flat 4% is of course not a real
    age slope; it is a stylised illustration and the composite adopts it as **[std]** only
    because nothing else was obtainable, and because the realised 4세대 increase between the
    two published anchors — ₩11,982 in 2021-06 to ₩22,000 in 2025, a compound **16.4% a
    year** over four renewals [R1] [R7] — shows that the basis component `b`, not the age
    component `a`, is what has driven the premium.
13. **The wording does not fix the discount; it fixes the constraint that determines it.**
    「매년 상대도 적용 전·후의 총 보험료 수준이 일치하도록 3~5단계의 할증대상자의 할증재원을
    1단계(할인) 대상자들에게 분배할 경우 산출됨」 [S1] — the scheme is revenue-neutral
    within the rider, so the surcharge funds the discount. Writing `w_b` for the share of
    rider net premium in band `b` and `r_b` for the relativity, neutrality is
    `Σ_b w_b r_b = 1`, hence `r_1 = (1 − Σ_{b≥2} w_b r_b) / w_1`. Three published band
    distributions exist and they disagree: an ex-ante simulation on 3세대 data giving
    「할증구간(3~5등급) 대상자는 전체 가입자의 1.8%」 [R1]; the FSC's figures at commencement,
    1등급 62.1% / 2등급 36.6% / 3등급 1.3% [R3]; and 보험연구원's, attributed to a
    금융감독원 release of 2024-01-19, 72.9 / 25.3 / 0.8 / 0.7 / 0.3 [R12]. The composite
    takes the **[R12] set**, the only one that resolves all five bands, and **solves** for
    `r_1`: `Σ_{b≥2} w_b r_b` = 0.253 + 0.016 + 0.021 + 0.012 = 0.302, so
    `r_1 = 0.698 / 0.729 = 0.9575` — a **4.25% discount**. The published values bracket it
    and one is outside: 「5% 내외」 at launch [R1], **−5% 잠정** at commencement [R3], the
    wording's own illustration assuming a **95%** relativity [S1], and a carrier writing it
    as 「α%」 rather than a number [S3]. Solving rather than hard-coding is the deliberate
    choice: it makes the scheme self-financing inside the model, which is what the wording
    requires, and it means a change to the band distribution propagates correctly instead of
    silently breaking neutrality. On the FSC distribution [R3] the same solve gives
    `r_1 = 0.608 / 0.621 = 0.9791`, a discount of only **2.1%** — the sensitivity is
    material and is why the two distributions are recorded rather than averaged.
14. A carrier-specific discount for holders of 의료급여 entitlement, 5% of the office
    premium on production of documents [S3]. It is not in the 표준약관, was found at one
    carrier only, and correlates with an income group whose 본인부담상한액 is the lowest —
    so it interacts with the truncation in § *본인부담상한제 —
    the public cap that truncates the 급여 claim* in a way the composite is not positioned
    to model. Out of scope, recorded.
15. Neither the 4세대 표준약관 [S1] nor the retrieved 5세대 carrier wording [S3] contains a
    납입면제 clause for the 실손 covers, which is consistent with a one-year contract whose
    annual premium is small relative to any waiver-triggering event. The 통합형 host
    products to which 실손 covers are sometimes attached do carry 납입면제 on their **other**
    covers [S5]. The composite has no premium waiver. Marked [unverified] because absence
    from two documents is not proof of absence across the market.
16. The only expense datum retrieved for this product is the aggregate: 손해조사비 plus
    사업비 of about **₩2.9조** on **₩18.0조** of 2025 premium — **16.1%** — which reconciles
    with the FSS's stated break-even loss ratio of about **85%** [R7]. No 상품요약서 with a
    사업비 disclosure was obtained for any generation of this product, so the split into
    acquisition, maintenance and claim-handling components is **[std]**. It is set at
    6 / 7 / 3 for three reasons: a one-year renewable contract renewed on a rolling basis
    has no meaningful acquisition/renewal distinction after year one; 감독규정 제4-32조제5항
    caps first-year commission on a 보장성보험 at the first year's premium, which is not
    binding at this level [REG-R22]; and claim handling must be carried separately because
    it is the component the FSS itself separates out as 손해조사비 [R7], and because the
    experience-rating machinery makes claim *frequency* a driver of expense as well as of
    benefit.

### Benefit provisions

The benefit is a reimbursement, so every row below is a rule for reducing an incurred cost
to a payable amount rather than a stated amount. Two words recur and are used strictly:
**보장대상 의료비** is the covered medical cost before any reduction, and **공제금액**
(*gongjegeumaek*) is the deductible subtracted from it. **자기부담률** (*jagibudamnyul*) is
the retained co-payment percentage, which the wording always expresses as its complement —
「본인부담금의 80%」 rather than "20% co-payment".

**기본형 실손의료보험 (급여 실손의료비) — the 주계약.** All rows from S1, 기본형 제3조 and
제5조, cross-checked against the supervisor's 4세대-versus-5세대 comparison table [R5 참고1](#krlib-indemnity_medical-r5).

| Parameter | Representative value | Basis |
|---|---|---|
| Covered loss | The insured's own 본인부담금 under 국민건강보험법 요양급여 or 의료급여법 의료급여 — both 일부본인부담금 and 전액본인부담금 | [S1 기본형 제3조] [REG-R53] |
| Inpatient (입원) reimbursement | **80%** of the 본인부담금 — a **20% 자기부담률** | [S1] [R5 참고1](#krlib-indemnity_medical-r5) |
| Inpatient annual co-payment cap | Where the 20% retained on **inpatient** treatment exceeds **₩2,000,000 (200만원)** in a policy year, the excess is reimbursed within the annual limit | [S1 제5조제4항] [R5 참고1](#krlib-indemnity_medical-r5) [REG-R17] |
| Outpatient (통원) deductible — clinic tier | `max(₩10,000, 20% × 보장대상 의료비)` per visit, at 의료법 제3조제2항 institutions other than 종합병원, at 보건소·보건의료원·보건지소, at 보건진료소 and at their pharmacies | [S1 제3조 <표1>] |
| Outpatient deductible — hospital tier | `max(₩20,000, 20% × 보장대상 의료비)` per visit, at 전문요양기관, 상급종합병원, 종합병원 and their pharmacies | [S1 제3조 <표1>] |
| 통원 definition | 외래 (consultation) **and** 처방조제 (dispensing) merged into a single visit with a single deductible — the 3세대 separate ₩8,000 처방조제 deductible is gone | [S1] vs [S5] |
| Annual limit | **₩50,000,000** per 보장종목 (상해급여 and 질병급여 separately), inpatient and outpatient combined | [S1 제5조] |
| Per-visit cap | **₩200,000** | [S1 제5조제5항] |
| Visit-count cap | **None on the 급여 side** | [S1 제5조]; confirmed absent [R5 참고1](#krlib-indemnity_medical-r5) |
| Where NHI does not apply | Where the insured is outside 국민건강보험법 제5조·제53조·제54조 or the 의료급여법 equivalents (e.g. entitlement suspended), reimbursement falls to **40%** of the amount actually borne, still within the annual limit | [S1 제3조제3항제1호] |
| 본인부담상한제 interaction | Any amount refundable by 국민건강보험공단 ex ante or ex post under the 본인부담금 상한제 is **excluded from cover outright** | [S1 제4조제3항제1호] [S1 제5조제3항] [R10] [REG-R53] |
| 의료급여 mirror | The 의료급여 본인부담금 보상제 and 상한제 reduce the loss in the same way — 50% of the excess over ₩20,000 (1종) or ₩200,000 (2종) per 30 days; the whole excess over ₩50,000 per 30 days (1종) or ₩800,000 a year (2종), rising to ₩1,200,000 above 240 요양병원 days | [S1 제5조의2] |
| Cover widened at 4세대 | 불임관련 질환 (habitual miscarriage, infertility, complications of artificial insemination) from **two years** after inception, excluding 전액본인부담금; 선천성 뇌질환 where the policy was taken out in utero; dermatological conditions recognised as 급여 | [R1] |
| Organ transplant | 장기등의 적출 및 이식 for the insured's own functional recovery, under 장기등 이식에 관한 법률 제42조, reimbursed on the ordinary basis | [S1 제3조제9항] |

**실손의료보험 특별약관 (비급여 실손의료비) — the 특약.** All rows from S1, 특별약관 제3조
and 제5조, cross-checked against [R5 참고1](#krlib-indemnity_medical-r5).

| Parameter | Representative value | Basis |
|---|---|---|
| Covered loss | 비급여 의료비 — treatment designated 비급여대상 by the 보건복지부장관 under 국민건강보험법 or 의료급여법, expressly including the case where the NHI procedure was followed but no covered item arose | [S1 특별약관 제1조 주] [REG-R53] |
| Inpatient reimbursement | **70%** of the 비급여 의료비 excluding 비급여 병실료 — a **30% 자기부담률** | [S1 특별약관 제3조] |
| Private-room differential (상급병실료 차액) | **50%** of the non-covered room charge, capped at **₩100,000 per day averaged over the whole admission** — the average being total non-covered room charge ÷ total days | [S1] |
| Outpatient deductible | `max(₩30,000, 30% × 보장대상 의료비)` per visit — a flat floor, not provider-tiered | [S1 특별약관 <표1>] |
| Outpatient visit cap | **100 visits** per policy year — the count cap the 급여 side does not have | [S1 특별약관] |
| Annual limit | **₩50,000,000** per 보장종목 (상해비급여 and 질병비급여 separately), inpatient and outpatient combined | [S1 특별약관 제5조] |
| Per-visit cap | **₩200,000** | [S1 특별약관 제5조] |
| Where NHI does not apply | **40%**, as on the 급여 side | [S1 특별약관 제3조제8항] |
| Experience rating | The rider net premium — and only the rider — carries the five-band 요율 상대도 | [S1 특별약관 제6조] |

**3대비급여형 — the three named non-covered treatment classes.** These sit inside the
특별약관 but carry their own money and count limits **instead of** the ₩50,000,000
aggregate, and are the sharpest, most model-relevant part of the wording
[S1 특별약관 제3조(3) <표1>].

| Class | Per-act deductible | Annual money limit | Annual count limit |
|---|---|---|---|
| 도수치료 · 체외충격파치료 · 증식치료 (manual therapy, ESWT, prolotherapy) | `max(₩30,000, 30%)` | **₩3,500,000 (350만원)** | **50 acts**, the three sharing **one** counter |
| 주사료 (non-covered injection: the procedure, the drug and the consumables together) | `max(₩30,000, 30%)` | **₩2,500,000 (250만원)** | **50 acts** |
| 자기공명영상진단 (MRI / MRA) | `max(₩30,000, 30%)` | **₩3,000,000 (300만원)** | **none** |

| Parameter | Representative value | Basis |
|---|---|---|
| The 10-visit re-assessment rule | 「도수치료·체외충격파치료·증식치료의 각 치료횟수를 합산하여 **최초 10회** 보장하고, 이후 객관적이고 일반적으로 인정되는 검사결과 등을 토대로 증상의 개선, 병변호전 등이 확인된 경우에 한하여 **10회 단위로** 연간 50회까지 보상합니다」 | [S1 특별약관 제3조(3)] |
| The clinical test behind it | 관절가동(ROM), 통증평가척도, 자세평가 및 근력검사(MMT)를 포함한 이학적 검사 and 초음파 검사, evaluating 체절기능부전 (somatic dysfunction); on disagreement the parties jointly appoint a 종합병원 소속 전문의 as third party and **the insurer bears the whole cost of the assessment** | [S1]; assessment cost also covered [R2] |
| Injection carve-out | 비급여 injections of **항암제, 항생제 (항진균제 포함) and 희귀의약품**, each defined by a 식품의약품안전처 classification instrument, leave the ₩2,500,000 sub-limit and are reimbursed inside the main ₩50,000,000 비급여 limit | [S1 특별약관 제2조, 제3조(3)제2항] |
| Counting — the physical-therapy trio | Two or more of the three at one visit or admission, or the same one twice, are **each counted as one act and each separately deducted** | [S1 특별약관 제3조(3)제4항제1호] |
| Counting — injections | Two or more injections at one visit or admission are **one** act | [S1 제3조(3)제4항제2호] |
| Counting — MRI | MRI at two or more sites, or the same site twice, are **separate** acts, each carrying its own deductible | [S1 제3조(3)제4항제3호] |
| 1회 입원 | An unbroken admission, including a same-day transfer to another provider for the same condition; a re-admission after discharge is a fresh admission even for the same cause | [S1 제3조(3)제5항] |
| Effect of exhausting a sub-limit | **Cover stops for the remainder of the policy year and only the 계약해당일 restores it.** Neither limit is pro-rated: the wording works both cases — ₩3,500,000 exhausted after 30 treatments on 2022-10-31, cover excluded for the following **151 days** to 2023-04-01; and 50 acts used with only ₩3,000,000 paid, cover excluded for the following **182 days** from 2022-10-01 | [S1] |

**Definitions the wording fixes.** 도수치료 is 「치료자가 손(정형용 교정장치 장비 등의 도움을
받는 경우를 포함합니다)을 이용해서 환자의 근골격계통(관절, 근육, 연부조직, 림프절 등)의 기능
개선 및 통증감소를 위하여 실시하는 치료행위」, restricted to a doctor or to a physiotherapist
under a doctor's direction; 체외충격파치료 excludes lithotripsy (체외충격파쇄석술); 증식치료
is prolotherapy; and 주사료 is 「주사치료시 사용된 행위, 약제 및 치료재료대」 — the procedure,
the drug and the consumables together [S1 특별약관 제2조]. These are enumerated definitions of
*procedures*, and 5세대 replaced the first with a fee-schedule reference precisely because
they could be evaded; see § *Variations across insurers*.

**Aggregate exposure and its calibration.** With both parts held, the whole-contract annual
limit is **₩100,000,000 (1억원)** — 「연간 보장한도도 기존과 유사하게 1억원 수준(급여
5천만원, 비급여 5천만원)으로 책정」 [R1]. The launch release prints the calibration
alongside it: in 2019 the proportion of insureds receiving more than ₩50,000,000 of claims
was **0.005%** of all policyholders [R1]. That single figure is the best public evidence on
the thickness of the claim-size tail, and it says the ₩50,000,000 limit binds on about one
insured in twenty thousand.

**Exclusions (면책).**

| Scope | Excluded | Basis |
|---|---|---|
| Both parts | Intentional self-harm (with the mental-incapacity exception); intentional harm by the beneficiary or policyholder; **pregnancy, childbirth including Caesarean, and the puerperium** unless consequent on a covered accident; war and civil disorder; a stay the insured insisted on against medical advice; outpatient cost incurred by disregarding medical instruction | [S1 제4조] |
| Both parts | Hazardous pursuits — 전문등반, gliding, skydiving, scuba, hang-gliding, powerboats, paragliding; motor sport; crew duty aboard ship | [S1 제4조] |
| 급여 side, monetary | Amounts refundable under the 본인부담금 상한제 or the 의료급여 equivalents; amounts recovered under 자동차보험 or 산재보험, net of contributory negligence, the insured's own residual share remaining covered; the **응급의료관리료** charged as a 전액본인부담금 where a non-emergency patient uses a 권역응급의료센터 or an 상급종합병원 emergency department | [S1 제4조제3항] |
| 비급여 side | Dental and 한방 treatment except where performed by a 의사; nutritional and vitamin preparations **except** within the licensed indication and dosage (or three further qualifying routes); hormone therapy, tonics and quasi-drugs; dentures, prostheses, spectacles, contact lenses, hearing aids, crutches, arm slings, orthoses — **but implanted artificial organs are covered**; non-clinical charges (television, telephone, certificates); tests with no clinical indication; **간병비** (nursing care); treatment by a foreign provider; treatment excluded from NHI cover for want of demonstrated economy | [S1 특별약관 제4조] |
| Waiting period | **None** except the two-year wait on 불임관련 질환 급여 cover | [S1 제24조] [R1] |
| Suicide | Not modelled — the product pays no death benefit, so the 상법 인보험 suicide provisions have no benefit to withhold | [REG-R50] |

The nutritional-preparation rule is worked through four named drugs in the FSC's FAQ and the
principle it settles is that **payability follows the drug's licensed indication, not the
prescribing doctor's stated purpose** — thioctic acid for a common cold is not payable;
hepatamine for cirrhosis-related anorexia is [R2]. Both this and the 10-visit re-assessment
rule are 4세대 narrowings on the 비급여 side, introduced in the same amendment that widened
the 급여 side [R1].

### Options

The 표준약관 leaves the policyholder very little to elect, and what it does leave is
structural rather than optional in the sister-library sense. There are no riders in the
jplib sense at all: the 비급여 특약 *is* the rider, and it carries the product's second half.

| Option | Representative treatment | Basis |
|---|---|---|
| 보장종목 election | All five held in the composite; holding the 급여 주계약 alone, or 상해 only, or 질병 only, is a model-point switch | [S1 제1조]; **[std]** (1) |
| 보험가입금액 election | ₩50,000,000 per 보장종목 with a ₩200,000 per-visit cap; lower rungs (₩30,000,000 / ₩10,000,000, per-visit ₩150,000 / ₩100,000) are switches | ceiling [S1]; menu by analogy [S3]; **[std]** (2) |
| 3대비급여형 | Held. It is a 보장종목 of the 특약, not a separate contract, and its sub-limits displace the main 비급여 limit for the three classes | [S1 특별약관 제1조] |
| 무사고 할인 | Modelled: a two-year claim-free lookback on 비급여 claims, excluding 4대 중증질환, giving 10% off the **whole** office premium in the following year, stacking with the band-1 relativity | [R1] [S3] |
| 개인실손 중지·재개 (suspension and resumption) | Parameterized, off in the base run. A policyholder covered by a 단체실손 may suspend the individual policy and resume it within one month of the group cover ending; the facility is **mandatory** under 감독규정 제7-63조제2항제7호 | [R16] [S3] [REG-R17] |
| 계약전환 (conversion between generations) | Out of scope as a decrement; recorded because it is the mechanism by which the in-force book moves generation | [R1] [R2] [R5] |
| 노후실손 / 유병력자실손 | Out of scope — separate product families with their own co-payments, issue ages and three-year change cycles | [R17] [REG-R17 제7-63조제2항제5호](#krlib-reg-r17) |
| 단체실손 (group cover) | Out of scope; excluded from the FSS statistics this model calibrates to | [R7] |
| 해외여행 실손의료보험 | Out of scope — a separate 표준약관 in the same annex | [S1] |
| 의료급여 수급권자 할인 | Out of scope, carrier-specific | [S3]; **[std]** (14) |

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| Surrender value (해약환급금) | **None.** 「이 상품은 1년만기 순수보장성 상품으로 해약환급금이 발생하지 않습니다」 | [S3] |
| Mid-term cancellation | The policyholder may terminate at any time before a claim event and recover the **미경과보험료** (unearned premium) | [REG-R49 제649조](#krlib-reg-r49) |
| Policyholder dividend | None; no maturity benefit exists | [S3] |
| 보험계약대출 / 보험료 자동대출납입 | Neither available in substance. The 표준약관 carries the clauses because the standard text is shared across products, but 제33조 states that 「순수보장성보험 등」 may be excluded from policy lending — and with no surrender value there is nothing to lend against | [REG-R25 제33조](#krlib-reg-r25) [S1]; the pinpoint is the 표준약관's shared general provision, not a clause read out of the 실손 extract |
| Reserve held | The 잔여보장요소 is the unearned premium and the 발생사고요소 the outstanding-claims provision; there is **no 보험료적립금** and no 해약환급금준비금 | [REG-R8] [REG-R11]; **[std]** (17) |
| Grace period (납입최고) | **14 days** from the demand, the contract terminating the day after it ends | [REG-R25 제26조](#krlib-reg-r25); **[std]** (18) |
| Lapse (실효) | From the day after the demand period expires; there is no automatic premium loan to break the fall | [REG-R25 제26조](#krlib-reg-r25) [S1 제27조] |
| Reinstatement (부활) | Within **3 years** of termination, on payment of arrears with interest at a rate within 평균공시이율 + 1%; the insurer **may not refuse** because a claim event occurred before termination | [REG-R25 제27조](#krlib-reg-r25) [S1 제28조]; **[std]** (18) |
| Renewal refusal | The policyholder may decline renewal; the insurer may not, within the 보장내용 변경주기 and the age range, provided the prior premium was paid | [S5] [S3] |
| Re-entry refusal | The insurer 「기존계약의 가입 이후 발생한 상해 또는 질병을 사유로 가입을 거절할 수 없습니다」, and on expiry of automatic renewal must accept the policyholder into whichever 실손 product it is then selling | [S1 제23조제1항·제2항] |
| Cooling-off (청약철회) | **15 days** from receipt of the 보험증권 and never later than **30 days** from the application, effective on despatch, premiums returned within 3 business days | [REG-R25 제17조](#krlib-reg-r25) [REG-R51] |
| 품질보증해지 | Cancellation within **3 months** of formation where the 약관 was not delivered, its important content not explained, or the policyholder did not sign | [REG-R25 제18조제3항](#krlib-reg-r25) [REG-R49 제638조의3](#krlib-reg-r49) |
| Non-disclosure (계약 전 알릴 의무 위반) | Termination barred after **one month** from the insurer learning of it, **two years** from 보장개시일 without a claim event (one year for disease in a 진단계약), or **three years** from the contract date; a causation defence applies; non-disclosure of other insurance held is not a ground | [REG-R25 제13조·제14조](#krlib-reg-r25) [REG-R49 제651조](#krlib-reg-r49) |
| Fraud (사기에 의한 계약) | Cancellation within **five years** of 보장개시일 and one month of discovery | [REG-R25 제15조](#krlib-reg-r25) |
| Duplicate cover | Never more than the actual loss: 「동일한 위험을 보장하는 2개 이상의 계약에 중복 가입 하더라도 실제 발생한 손해(비용)를 초과하여 보험금을 지급하지 않습니다. (중복 가입 시 비례보상)」 | [S1 제37조·제38조] [S3] |
| Prescription (소멸시효) | **3 years** on a claim | [REG-R25 제37조](#krlib-reg-r25) [REG-R49 제662조](#krlib-reg-r49) |
| Deposit protection | ₩100,000,000 per person per insurer on 보험금, in a bucket separate from retirement-pension and 연금저축 claims; the 해약환급금 bucket is empty here because there is no surrender value | [REG-R52] [S3] |
| Expiry | Cover ends at the 계약해당일 at 보험나이 **100** | [S3] [S4] |
| Death of the insured | Contract terminates; the 계약자적립액 (nil in practice) and the 미경과보험료 are paid | [REG-R17] [REG-R25 제22조](#krlib-reg-r25) |
| Run-off after termination | An admission in progress continues to be covered for **180 days** from the day after termination; an outpatient course for visits within 180 days to a maximum of **90 visits** — but **not** on renewal or re-entry, which are treated as extensions of the term | [S1 제3조제4항~제6항] |
| Run-off limit | The unused remainder of the annual limit at the previous policy-year end | [S1 제5조제6항] |

17. 보험업법 시행령 제63조제1항 states the reserve in IFRS 17 vocabulary as
    **보험계약부채** = 발생사고요소 + 잔여보장요소, both on a 현행추정치 basis [REG-R8]. On
    a one-year indemnity contract the weighting is the reverse of every other `krlib`
    product: the 잔여보장요소 is at most one year's unearned premium, and the 발생사고요소 —
    incurred claims not yet settled — is the material item, because reported claim volume is
    large and settlement is fast but not instantaneous [S1 제8조]. The **해약환급금준비금**
    of 감독규정 제6-11조의6, the Korea-specific overlay that exists because IFRS 17
    measurement can fall below the contractual surrender value, has **nothing to bite on
    here** [REG-R11]. `Medical_KR_S` computes neither reserve; it projects the cash flows
    that would feed them.
18. **Neither number was extracted from the 실손 wording itself.** S1 제27조 (납입최고와
    계약의 해지) and 제28조 (부활) were located in the extracted text by heading, but their
    numeric parameters were not read out in the research pass. The values carried here come
    from the 표준약관 family's shared clauses [REG-R25]: a demand period of **at least 14
    days** (7 where the policy term is under one year — which a one-year 실손 contract is
    not), and reinstatement **within three years** where the surrender value has not been
    drawn, which on a no-surrender-value contract is always. Both are marked [std] on that
    reasoning rather than [S1]. The reinstatement window is generous and matters less here
    than on a level-premium product, because a reinstated 실손 contract re-enters at the
    same attained-age rate it would have renewed at.

---

## Contractual mechanics

### The reimbursement identity

Everything in this product is a rule for reducing an incurred cost to a payable amount. The
identity the supervisor itself states is

    covered_loss = 급여 본인부담금 + 비급여 의료비

and it is worth writing down because it is not the identity a fixed-sum health product
obeys [R7]. Both terms are set outside the contract. The first is a percentage of the public
fee schedule, fixed by 국민건강보험법 제44조제1항 and the co-payment schedule made under it —
outpatient 30% at 의원급, 40% at 병원급 (35% 읍·면), 45–50% at 종합병원, and at 상급종합병원
the whole 진찰료 plus 60% of the remainder; inpatient 20% of the covered cost plus half the
meal charge; 처방조제 30% at a pharmacy [R11] [REG-R53]. The second is a residual: 요양급여
covers everything **except** what the 보건복지부장관 designates 비급여대상 under
국민건강보험법 제41조제4항, so 비급여 is defined by exclusion from a list the insurer does
not control and that moves [REG-R53].

Two consequences run through the whole model. **The insured loss is exogenous to the
contract and endogenous to public policy**, so a projection must treat the 급여/비급여
boundary as a moving parameter rather than a constant — 5세대's 관리급여 category, which
migrates over-used 비급여 items into the covered system at a **95% co-payment**, will move
items from the rider to the main contract within any reasonable projection horizon [R6].
And **the two halves behave differently**: 비급여 grew 8.1% in 2024 against 1.0% for the
statutory co-payment [R9], and 비급여 was **57.1%** of all claims paid in 2025 against a
15.8% share of national spend [R7] [R9]. The rider is the smaller share of the medical
system and the larger share of the claim.

### 급여 reimbursement — the main contract

**Inpatient.** The benefit is 「본인부담금 … 의 80%에 해당하는 금액」, taking 일부본인부담금
and 전액본인부담금 alike [S1 기본형 제3조]:

    paid_in(k)     = 0.80 * covered_in(k)
    retained_in(k) = 0.20 * covered_in(k)

with an annual floor under the retention. Where the cumulative 20% retained on **inpatient**
treatment exceeds **₩2,000,000** in a policy year, the excess is reimbursed within the
annual limit [S1 제5조제4항] [R5 참고1](#krlib-indemnity_medical-r5):

    retained_cum(y) = Σ over admissions k in policy year y of retained_in(k)
    top_up(y)       = max(0, retained_cum(y) - 2,000,000)

so that once ₩2,000,000 of inpatient co-payment has been retained, the 자기부담률 on further
inpatient 급여 cost is effectively nil for the rest of the policy year. The cap is not a
4세대 novelty — the identical ₩2,000,000 appears in a 2세대 carrier document [S4] — and it
is now in the regulation itself, 감독규정 제7-63조제2항제2호 [REG-R17]. It applies to
inpatient treatment only; there is no annual cap on the outpatient deductible.

**Outpatient.** Per visit, the covered cost less a deductible drawn from a two-row table
[S1 기본형 제3조 <표1>], then capped:

    d_tier     = 10,000  at 의료법 제3조제2항 institutions other than 종합병원,
                          보건소·보건의료원·보건지소, 보건진료소 and their pharmacies
               = 20,000  at 전문요양기관, 상급종합병원, 종합병원 and their pharmacies
    deduct(v)  = max( d_tier, 0.20 * covered_out(v) )
    paid_out(v)= min( max(0, covered_out(v) - deduct(v)), 200,000 )

The shape matters more than the formula. The deductible is a **flat floor that becomes a
percentage**: at the clinic tier it is ₩10,000 until the covered cost reaches ₩50,000 and
20% thereafter; at the hospital tier ₩20,000 until ₩100,000 and 20% thereafter. So a visit
costing ₩10,000 or less at a clinic pays nothing, a ₩50,000 visit pays ₩40,000, and above
₩50,000 the payment is a straight 80% of cost until the ₩200,000 per-visit cap binds at a
covered cost of ₩250,000 — the same crossing point at both tiers. Three quantities therefore
determine the outpatient claim: the visit-cost distribution, the provider mix and the visit
count, and only the third is capped on this side of the contract.

4세대 merged 외래 and 처방조제 into **one visit with one deductible**. The 3세대 wording
carried a separate ₩8,000 처방조제 deductible on top of the ₩10,000–₩20,000 외래 deductible
[S5]; 4세대 does not [S1]. On a course of treatment involving repeated prescriptions the
change is worth more than it looks, and it is the reason a 3세대 frequency basis cannot be
carried across to 4세대 without adjustment.

**Where NHI does not apply.** If the insured falls outside 국민건강보험법 제5조·제53조·제54조
or the 의료급여법 equivalents — most commonly a suspension of entitlement — the
reimbursement drops to **40%** of the amount actually borne, still within the annual limit
[S1 제3조제3항제1호]. The same 40% applies on the 비급여 side [S1 특별약관 제3조제8항]. This
is a state, not an event: it persists while entitlement is suspended.

### 본인부담상한제 — the public cap that truncates the 급여 claim

The single most important interaction in the product, and the one a model built from the
policy wording alone will miss. 국민건강보험법 제44조제2항 creates the **본인부담상한제**: the
NHIS refunds the excess of a member's annual 본인일부부담금 over an income-graded ceiling
[REG-R53], operated as 사전급여 and 사후환급 over the **calendar year** [R10]. The 표준약관
then excludes that refund from cover twice over — 제5조제3항 limits the reimbursement to what
the insured actually bore net of any amount refundable ex ante or ex post, and 제4조제3항제1호
excludes outright 「국민건강보험 관련 법령에 따라 국민건강보험공단으로부터 사전 또는 사후
환급이 가능한 금액(본인부담금 상한제)」 [S1].

The ceiling is set by the insured's own NHI contribution decile [R10], in 만원:

| 연도 | 1분위 | 2~3분위 | 4~5분위 | 6~7분위 | 8분위 | 9분위 | 10분위 |
|---|---|---|---|---|---|---|---|
| 2023 | 87 | 108 | 162 | 303 | 414 | 497 | 780 |
| 2024 | 87 | 108 | 167 | 313 | 428 | 514 | 808 |
| 2025 | 89 | 110 | 170 | 320 | 437 | 525 | 826 |
| 2026 | 90 | 112 | 173 | 326 | 446 | 536 | 843 |

with a higher scale where the insured spent more than 120 days in a 요양병원 — for 2026,
143 / 181 / 245 / 404 / 580 / 698 / 1,096 만원 [R10]. The 표준약관 requires the insurer to
explain the interaction specifically at point of sale and reproduces the then-current range
in a footnote: 「… 81만원~584만원 … (상기 예시금액은 2021.5월 기준)」 [S1 제5조의2].

**The modelling consequence, stated as arithmetic.** The 급여 half of the claim is bounded
above, per insured per calendar year, at roughly

    급여 claim ≲ 0.80 * 본인부담상한액(decile) + top_up(y)

because everything above the ceiling is refunded by the NHIS and is therefore not an insured
loss at all. In 2026 that means a 1분위 insured's 급여 claim cannot materially exceed
₩900,000 × 0.80 = **₩720,000** for the year, while a 10분위 insured's runs to
₩8,430,000 × 0.80 = **₩6,744,000** — a nine-fold spread driven by income and nothing else.
**The 급여 claim distribution is truncated, and truncated differently by income decile.**
The 비급여 half has no such truncation, which is exactly why it is 57.1% of claims [R7]
against a 15.8% share of national spend [R9].

Two refinements a careful implementation needs. First, **the two years do not align**: the
policy year runs from the 계약일 or 계약해당일 [S1 제5조제2항] while the 본인부담상한제 runs
1 January to 31 December [R10], so the truncation and the annual limit are applied on
different clocks. Second, the ₩2,000,000 inpatient top-up interacts with the ceiling in the
same direction — both reduce the insured's retention on heavy 급여 use — so a model that
applies both without netting will double-count relief. `Medical_KR_S` applies the ceiling
first, as an exclusion from covered loss, and the ₩2,000,000 cap second, on what remains.

### 비급여 reimbursement — the rider

    paid_in(k)   = 0.70 * ( covered_np_in(k) - room_charge(k) )
    room_paid(k) = min( 0.50 * room_charge(k), 100,000 * days(k) )
                   where the ₩100,000 cap is applied to the *daily average*,
                   room_charge(k) / days(k), not night by night
    deduct(v)    = max( 30,000, 0.30 * covered_np_out(v) )
    paid_out(v)  = min( max(0, covered_np_out(v) - deduct(v)), 200,000 )
    visits_np(y) ≤ 100 per policy year

[S1 특별약관 제3조]. Three things separate this from the 급여 arithmetic. The outpatient
deductible is a **flat ₩30,000 floor at every provider**, not tiered — which is why the
wording does not repeat the 급여 side's "highest applicable deductible" rule for multiple
same-day visits [S1 <표1>]. There **is** a visit-count cap, 100 a policy year, and it exists
on this side only. And the private-room differential is averaged over the admission, so a
single expensive night inside a long stay is smoothed against the stay length rather than
capped night by night — a materially more generous treatment than a nightly cap, and one a
per-night implementation will understate.

The 30% co-payment against the 급여 side's 20% is the generation's design statement: 「필수
치료인 급여에 대해서는 보장을 확대하되, 환자의 선택사항인 비급여에 대해서는 의료이용에
따라 보험료가 할인·할증되도록 하였습니다」 [R1].

### 3대비급여 — sub-limits, shared counters and hard annual gates

For the three named classes the ₩50,000,000 aggregate does not apply; each class carries its
own money and count limit instead [S1 특별약관 제3조(3) <표1>]:

    for each class c in {physio_trio, injection, mri}:
        paid(a)      = max(0, cost(a) - max(30,000, 0.30 * cost(a)))   per act a
        paid_cum(c)  ≤ money_limit(c)     350만 / 250만 / 300만원
        acts(c)      ≤ count_limit(c)     50 / 50 / unlimited

The three physical-therapy procedures — 도수치료, 체외충격파치료, 증식치료 — **share one
50-act counter**, and cover beyond the first ten acts is conditional: the wording pays the
first ten unconditionally and then 「10회 단위로」 to fifty, each further block of ten
requiring documented improvement on an enumerated clinical test set [S1]. The insurer bears
the cost of the assessment [R2]. This is the only place in `krlib` where a benefit is gated
on a *clinical review* rather than on a definition, and a model can only represent it as a
continuation probability applied at each ten-act boundary.

**Both gates are hard and neither is pro-rated.** The wording works two cases and they are
worth reproducing because they settle the question a naive implementation gets wrong: where
₩3,500,000 is exhausted after 30 treatments on 2022-10-31, cover is excluded for the
following **151 days** and resumes at the 계약해당일 2023-04-01; where 50 treatments are used
but only ₩3,000,000 paid, cover is excluded for the following **182 days** from 2022-10-01
[S1]. The limit that binds first stops cover for the rest of the policy year, and only the
anniversary restores it. A 3대비급여 claim stream is therefore a **censored counting
process with an annual reset**, not a rate.

The counting rules are asymmetric and each is a real modelling instruction
[S1 특별약관 제3조(3)제4항]: two or more of the physical-therapy trio at one visit are
**each** counted and **each** separately deducted; two or more injections at one visit are
**one** act with one deduction; MRI at two sites, or the same site twice, are **separate**
acts each with its own deduction. Read together with the ₩30,000 per-act floor, the
injection rule is worth money to the insurer and the MRI rule worth money to the insured.

**The injection carve-out moves the largest claims out of the sub-limit.** 비급여 injections
of 항암제, 항생제 (항진균제 포함) and 희귀의약품, each defined by a 식품의약품안전처
classification instrument, leave the ₩2,500,000 injection sub-limit and are reimbursed
inside the main ₩50,000,000 비급여 limit [S1 특별약관 제3조(3)제2항]. So the ₩2,500,000 cap
bites on the discretionary end of injection use — the 영양제 and 비타민제 the same wording
restricts by licensed indication [S1] [R1] — and not on oncology. Given that non-covered
injections were **₩2.81조**, 18.5% of all claims, in 2024 [R8], where the boundary is drawn
is a first-order calibration question and not a detail.

### Annual limits, the policy year and run-off

「연간」 means 「계약일로부터 매1년 단위로 도래하는 계약해당일 전일까지의 기간」 — a policy
year measured from the contract date, not a calendar year [S1 제5조제2항]. All four
₩50,000,000 limits, the ₩200,000 per-visit cap, the 100-visit count, the three
3대비급여 sub-limits and the ₩2,000,000 inpatient co-payment cap run on that clock and reset
at each 계약해당일. The 본인부담상한제 does not (§ *본인부담상한제*), and neither do the
insurer's own experience statistics, which are compiled on calendar years [R7] [R8].

Because 상해 and 질병 carry **separate** ₩50,000,000 limits on each of the two parts, the
whole-contract annual exposure is ₩100,000,000 in the ordinary reading and up to
₩200,000,000 if an insured exhausted injury and sickness limits in the same year — a case
the supervisor's own framing ignores and the tail data says is negligible: 0.005% of
insureds took more than ₩50,000,000 in 2019 [R1].

**Run-off.** An admission in progress when the contract ends continues to be covered for
**180 days** from the day after termination; an outpatient course in progress for visits
within 180 days to a maximum of **90 visits** [S1 제3조제4항·제5항]. The limit available is
the unused remainder of the annual limit at the previous policy-year end [S1 제5조제6항]. But
the run-off provisions **do not apply on renewal or re-entry**: 「종전 계약을 자동갱신하거나
같은 회사의 보험상품에 재가입하는 경우에는 종전 계약의 보험기간을 연장하는 것으로 보아」
[S1 제3조제6항]. Renewal and re-entry are continuations, not terminations. That single
sentence is what makes the one-year contract behave, for benefit purposes, like a continuous
cover with an annually resetting limit — and it is the sentence an IFRS 17 contract-boundary
argument has to engage with.

### Event and visit counting

- Same-day 외래 plus 처방 at the same provider count as **one visit**, aggregated on the
  prescription date [S1 제3조제7항] [S1 특별약관 제3조제6항].
- Two or more visits on one day for the same treatment purpose count as **one**, and on the
  급여 side 「공제금액은 2회 이상의 중복방문 의료기관 중 가장 높은 공제금액을 적용합니다」 —
  the highest applicable deductible [S1 제3조제8항]. The rule is absent on the 비급여 side
  because that deductible does not vary by provider.
- **하나의 질병** is 「발생 원인이 동일한 질병(의학상 중요한 관련이 있는 질병은 하나의
  질병으로 간주하며 …)」, and unrelated conditions treated at one visit are treated as one
  disease [S1 제3조(2)제7항].
- **1회 입원** is an unbroken admission including a same-day transfer to another provider for
  the same condition; a re-admission after discharge is a fresh admission even for the same
  cause [S1 특별약관 제3조(3)제5항].

Note what is **not** here: there is no 180-day re-admission rule joining separate stays into
one hospitalization, as there is in the
[jplib medical chassis](../../../jplib/products/medical/product-spec.md). A Korean 실손
contract has no per-admission day limit to aggregate against, so the question does not
arise. What it has instead is the annual money limit, and the counting rules exist to
determine how many **deductibles** are charged, not how many days are paid.

### The premium split between the two priced units

A 4세대 contract is two priced units, tracked and re-rated separately: 「급여, 비급여 각각의
손해율에 따라 보험료가 조정되어…」 [R1]. Writing `s` for the 비급여 share of the office
premium,

    prem_geubyeo(y) = (1 - s) * prem_total(y)
    prem_bigeubyeo(y) = s * prem_total(y)

with **s = 0.60** [R2] [std]. The share is not a presentational detail: the experience
relativity and the 25% corridor apply to the two units separately, so `s` determines how
much of the contract the feedback loop can move. At s = 0.60 a band-5 policyholder pays
0.40 + 0.60 × 4.00 = **2.80×** the base total premium; at the 48.75% implied by the
표준약관's own illustration the same policyholder pays 2.46× [S1]. The two published values
and the reason for taking 60% are in footnote (10).

The loss ratios of the two units move very differently, and not in the direction the market
narrative assumes. On 손해보험회사 4세대 statistics [R12]:

| 기간 | 급여 | 비급여 | 합산 |
|---|---|---|---|
| 2022 상반기 | 97.5% | 73.0% | 82.8% |
| 2023 상반기 | 139.2% | 100.1% | 115.9% |
| 2024 상반기 | 154.6% | 114.2% | 130.6% |

The **급여 main contract has run worse than the 비급여 rider throughout** — which is exactly
why 5세대 changed the 급여 통원 deductible as well as the 비급여 terms, and why a model that
treats the 급여 unit as the stable half will mis-project the renewal path.

### 비급여 할인·할증 — the experience-rated renewal

**This is the mechanism that makes the contract unlike anything else in this repository: the
renewal premium of the 비급여 rider is a function of the individual policyholder's own
prior-year non-covered claim amount.** It is a feedback loop from claims to premium, inside
a single policy, on an annual clock, and it must be modelled rather than described.

**The lookback.** Let `C(y)` be the sum of 비급여 claims paid to the insured under the rider
in the twelve months ending three months before the renewal date in year `y`. The 4세대
wording says 「보험료 갱신 전 12개월 이내 기간」 [S1 특별약관 제6조제3항]; the three-month
offset is the operational refinement, because renewal notices go out about a month ahead —
「계약해당일이 속한 달의 3개월 전 말일부터 직전 1년간」 [R12] — and 5세대 writes it into the
standard text itself [S2 특별약관2 제6조제3항]. The composite uses the offset window,
because it is what carriers actually apply and because a model that assumes a
claims-to-renewal lag of zero will over-state the responsiveness of the loop.

**Two exclusions from `C`.** 비급여 claims arising from a 국민건강보험법 산정특례 condition —
암질환, 뇌혈관질환, 심장질환, 희귀난치성질환 등 — and **all** claims of an insured graded
장기요양 1등급 or 2등급 under 노인장기요양보험법 are struck out of the count
[S1 특별약관 제6조제3항] [REG-R54]. The severely ill are exempt from the experience rating.
This is a direct statutory cross-reference between `Medical_KR_S` and
[LTC (간병보험)](../long_term_care/product-spec.md), and it is the only such link in the
library.

**The bands** [S1 특별약관 제6조제3항] [REG-R25]:

| 단계 | Prior-12-month 비급여 claims | 요율 상대도 | Press-release form |
|---|---|---|---|
| 1단계 (할인) | ₩0 — no claim | `r₁` (solved) | 할인 |
| 2단계 (유지) | > ₩0 and < ₩1,000,000 | **100%** | — |
| 3단계 (할증) | ₩1,000,000 – < ₩1,500,000 | **200%** | +100% |
| 4단계 (할증) | ₩1,500,000 – < ₩3,000,000 | **300%** | +200% |
| 5단계 (할증) | ≥ ₩3,000,000 | **400%** | +300% |

The 표준약관 states the factor as a **요율 상대도** (a rate relativity) and the press
releases as a 할인·할증율 [R1] [R3]; they are the same numbers, and band 3 pays twice the
base rate, band 4 three times, band 5 four times. A hard floor sits under the surcharge:
「요율 상대도의 할증은 이 특별약관에 따른 보험금 지급실적이 연간 100만원 이상인 계약에 한하여
적용」 [S1 특별약관 제6조제4항] — below ₩1,000,000 of prior-year claims there is no
surcharge at all, which is why band 2 has a relativity of exactly 100%.

**The band is memoryless.** 「보험금 지급(사고) 이력이 1년마다 초기화됩니다 … `21년
지급보험금을 많이 받은 경우 → `22년 보험료 할증, `22년 무사고 → `23년 보험료는 할인등급
(1등급)으로 초기화」 [R2]. It is a **one-year-lookback state, not a no-claims ladder**: a
single bad year cannot compound into a permanently higher premium, and a single clean year
returns the policyholder to the discount band. In a Markov formulation the band at renewal
`y` depends on the claim experience of year `y−1` alone, so the transition matrix is a
function of the annual claim-amount distribution and nothing else — which is what makes the
loop tractable in a projection model at all.

**The discount is solved, not set.** 「매년 상대도 적용 전·후의 총 보험료 수준이 일치하도록
3~5단계의 할증대상자의 할증재원을 1단계(할인) 대상자들에게 분배할 경우 산출됨」 [S1]. The
scheme is revenue-neutral **within the rider**: the surcharge funds the discount and the
insurer collects the same rider premium either way. With `w_b` the share of rider net premium
in band `b`,

    Σ_b w_b r_b = 1        ⟹        r₁ = ( 1 - Σ_{b≥2} w_b r_b ) / w₁

On the composite band distribution (72.9 / 25.3 / 0.8 / 0.7 / 0.3) [R12] this gives
`r₁ = 0.698 / 0.729 = 0.9575`, a **4.25% discount**, against a published 잠정 figure of −5%
[R3], 「5% 내외」 at launch [R1] and a 95% relativity in the wording's own illustration [S1].
On the FSC's commencement distribution (62.1 / 36.6 / 1.3) [R3] the same identity gives
`r₁ = 0.9791`, a 2.1% discount. The composite **solves** rather than hard-codes, so that the
scheme stays self-financing when the band distribution shifts — which it will, because the
distribution is itself an output of the loop.

**Only the rider is surcharged.** 「비급여 특약 보험료만 할증되며 보험료 전체가 할증되는
것은 아닙니다」 [R2]. And the relativity applies to the **순보험료**: 「보험료 갱신시
순보험료(특별약관의 순보험료 총액을 대상으로 합니다)에 아래와 같이 적용할 수 있습니다」
[S1]. `Medical_KR_S` applies the relativity to the rider net premium and re-grosses at the
same expense ratio, which is arithmetically identical to scaling the rider office premium —
a **[std]** simplification that would fail only if the rider expense loading contained a
fixed per-policy amount, which no retrieved document states either way.

**The 무사고 할인 runs alongside and is a different animal.** 「직전 2년간 비급여
보험금(4대 중증질환 치료를 위한 보험금은 제외) 미수령시 차기 1년간 보험료(급여(주계약) +
비급여(특약))의 10%를 할인」 [R1]. It has a **two-year** lookback where the relativity has
one, it applies to the **whole** office premium where the relativity applies only to the
rider, and it **stacks** with the band-1 discount: the launch release prints a three-year
timeline in which years 1 and 2 give only the ~5% rider discount and year 3 adds the 10%
whole-premium discount [R1]. A carrier's 5세대 wording gives the precise scope — the test
excludes 급여 본인부담금 claims and 중증 비급여 claims, and a contract without the
비중증 rider is excluded from the discount altogether [S3].

**The behavioural point the FAQ makes, which is the scheme's whole purpose.** A 45-year-old
male paying ₩5,000 급여 + ₩8,000 비급여 = ₩13,000 a month takes about 20 sessions of
도수치료 at ₩500,000 a session, claims ₩10,000,000 and receives ₩7,000,000, bearing
₩3,000,000. His rider premium quadruples to about ₩32,000 and his total to about ₩40,000. He
then shops on the 심평원 price disclosure, cuts his claims to ₩700,000 with ₩300,000 borne,
and his rider premium resets to about ₩9,000 including the age increment, his total to about
₩15,000 — a saving of ₩300,000 in premium and ₩2,700,000 out of pocket in one year [R2].
**The contract is designed to change the insured's behaviour, and a model that treats claim
frequency as independent of the premium state is modelling only half of it.** `Medical_KR_S`
projects the loop deterministically on a fixed frequency basis and does **not** model the
behavioural response; that is a stated limitation, not an oversight.

**Effective date.** The clause was in the wording from launch but its application was
deferred three years 「충분한 통계 확보 등을 위하여」 and commenced **2024-07-01** [R3] [R1].
A 4세대 policy written in 2021 therefore had three renewals at flat relativity before the
loop switched on. The same two-year deferral is being repeated on 5세대, whose differential
starts **2028-05-06** [S3].

### 1년 갱신 — annual renewal and the ±25% corridor

**The policy term is one year.** 「이 계약의 보험기간은 1년으로 합니다」, with automatic
renewal on the day after expiry unless the policyholder says otherwise, subject to three
conditions: that the renewed term ends within the 보장내용 변경주기, that the insured's age
is within the company's range, and that the prior premium was fully paid [S5] [S3].

**Renewal re-rates on everything.** 「갱신되는 계약의 보험료는 갱신일 현재의 보험요율에 관한
제도를 반영하여 계산된 보험료를 적용하며, 그 보험료는 나이의 증가, 보험료산출에 관한 기초율의
변동 … 등의 사유로 인하여 인상 또는 인하될 수 있습니다」 [S1 제30조제1항]. The increase is
bounded: 「갱신계약의 보험료는 매년 최대 25% 범위(나이의 증가로 인한 보험료 증감분은 제외)
내에서 인상 또는 인하될 수 있습니다」, with an exception only where the insurer is under
경영개선권고, 요구 or 명령 [S1 제30조제2항]. The corridor is now in the regulation itself —
「실손의료보험에서 위험구분단위별로 보험료의 변경이 매년 ±25%를 초과하지 않을 것」
[REG-R17 제7-63조제2항제3호](#krlib-reg-r17) — and the supervisor restates it as a live constraint
[R6]. **It binds per 위험구분단위, not on the portfolio average**, which is why a published
industry average of 7.8% [unverified] and a single carrier's single-cover 21.8% [S6] are not
in conflict.

**The recursion, taken from the wording's own illustration.** The 표준약관 prints a
five-year renewal illustration for an unnamed age, male, starting at ₩14,000 a month with the
25% maximum assumed every year and both parts held [S1 제30조]:

| 구분 | XX세 | +1 | +2 | +3 | +4 | +5 |
|---|---|---|---|---|---|---|
| 나이증가분 (A) | — | 560 | 728 | 946 | 1,230 | 1,599 |
| 기초율 증가분 (B) | — | 3,640 | 4,732 | 6,152 | 7,997 | 10,396 |
| 기준보험료 (C) | 14,000 | 18,200 | 23,660 | 30,758 | 39,985 | 51,980 |
| C with 직전 2년 무사고 10% 할인 | — | — | (21,294) | (27,682) | (35,987) | (46,782) |

Two facts are recoverable from it and both are load-bearing. First, the age loading is a
constant **4.0%** of the previous year's base premium (560/14,000 = 728/18,200 = … =
1,599/39,985 = 0.04) — the only published age-slope datum in any retrieved document, and a
stylised one. Second, and easily got wrong, the column label 「B = 전년도 기준보험료 × 25%」
is loose: 3,640 is 25% of 14,560 = 14,000 × 1.04, not of 14,000. **The corridor applies to
the age-adjusted prior premium**, so the recursion is

    base(y) = base(y-1) * (1 + a) * (1 + b(y)),    a = 0.04,  |b(y)| ≤ 0.25

which reproduces 14,000 → 18,200 → 23,660 → 30,758 → 39,985 → 51,980 exactly. Getting the
order of operations wrong costs 4% of the corridor every year and compounds.

**The full renewal premium.** Composing the corridor, the relativity and the no-claim
discount, and writing `x` for attained 보험나이:

    base(y)   = base(y-1) * (1 + a(x)) * (1 + b(y))
    gross(y)  = base(y) * [ (1 - s) + s * r(band(y)) ] * (1 - 0.10 * noclaim(y))

with `s = 0.60`, `r` from the five-band table and `noclaim(y) = 1` after two consecutive
claim-free years. **The corridor applies to the pre-relativity premium** — 「요율 상대도 적용
전 보험료」 [S1 특별약관 제6조제2항] [REG-R17 제7-63조제2항제3의2호](#krlib-reg-r17) — so a band-5
policyholder can face 1.25 × 4.00 = **5.00×** the previous year's base rider rate in a single
step. That is the sharpest number in the product.

The 표준약관 extends its own illustration across the five bands [S1 특별약관 제6조]:

| 단계 | +1 | +2 | +3 | +4 | +5 |
|---|---|---|---|---|---|
| 1단계 (상대도 95% 가정) | 17,756 | 23,083 (20,775) | 30,008 (27,007) | 39,011 (35,109) | 50,714 (45,642) |
| 2단계 (100%) | 18,200 | 23,660 | 30,758 | 39,985 | 51,980 |
| 3단계 (200%) | 27,073 | 35,194 | 45,753 | 59,478 | 77,322 |
| 4단계 (300%) | 35,945 | 46,729 | 60,747 | 78,971 | 102,663 |
| 5단계 (400%) | 44,818 | 58,263 | 75,742 | 98,464 | 128,003 |

(Parenthesised values add the 10% 무사고 discount.) Every row is reproduced by the formula
above at `s = 0.4875`: at +1, `18,200 × (0.5125 + 0.4875 × 2) = 27,073`; at +2,
`23,660 × (0.5125 + 0.4875 × 4) = 58,263`. That is how the 48.75% rider share of footnote
(10) is recovered, and the reproduction is the check that the formula is the right one.

**What the renewal path has actually done.** ₩11,982 a month for a 40-year-old male in
2021-06 [R1] against ₩22,000 for the same cell in 2025 [R7] is a compound **16.4% a year**
over four renewals — inside the 25% corridor, and far above the 4% age effect. The industry
increase series is 2022 **14.2%** → 2023 **8.9%** → 2024 **1.5%** → 2025 **7.5%** [R4], with
the 2026 average reported at 7.8% and the 4세대 component 「in the 20%s」 [unverified, news
only], against which one carrier's disclosed 상해 담보 figures of 23.9% (2025) and 21.8%
(2026) are consistent [S6].

### Rate adequacy, the five-year grace and why a new generation is under-priced

보험업감독규정 제7-63조제2항제6호가목, quoted verbatim by 보험연구원: 「실손의료보험은 다음
각 목의 내용을 준수하여야 한다. 가. 경험통계 등을 기초로 순보험요율의 적정성을 매년 검증할
것. 다만, 새로운 위험을 보장하는 경우는 5년까지 적정성을 검증하지 아니할 수 있다.」 [R12]
[REG-R17]. The proviso was read conservatively as forbidding — not merely excusing — a rate
change within five years of a new product's launch, so **3세대 first re-rated in 2023-01 and
4세대 first in 2025** [R8] [R12]. 4세대 was moreover priced 「'16년도 2세대 요율을 기초로
하는 등 다소 낮은 가격으로 설계」, because 3세대 had not yet re-rated when 4세대 launched
[R12].

**A newly launched Korean 실손 generation is therefore systematically under-priced for its
first several years by construction**, and its loss ratio is expected to deteriorate before
the first re-rating and to improve after it. The published series shows exactly that shape:
4세대 91.5% (2022) → 113.8% (2023) → 111.9% (2024) → 115.1% (2025) [R7] [R8], with the 2025
re-rating not yet visible in the 2025 earned ratio. A model that assumes a self-supporting
rate from `t = 0` is not modelling this product, and `Medical_KR_S` accordingly takes its
`t = 0` premium from the published 2021 new-business anchor [R1] rather than from a
loss-ratio-neutral calculation. The 보험연구원's principal recommendation is to shorten the
grace to three years [R12].

Two further supervisory constraints ring the rate. 보험업감독규정 제7-73조 requires rates to
rest on 「객관적이고 합리적인 통계자료를 기초로 대수의 법칙 및 통계신뢰도」, permits external
statistics or a modified 참조순보험요율 where a company's own experience is insufficient, and
expressly contemplates rates reflecting 「물가변동, 의료기술발달, 위험변화요인」 [R19]. And
제7-45조제7항 requires the **보험가격지수** — 보험료총액 ÷ (참조순보험료 총액 + 보험회사
평균사업비총액) — to be explained to a 실손 policyholder **at every renewal**, not only at
sale [REG-R22]. So the rate bureau's reference rates become visible to the public only as a
ratio, never as a rate, and for this product not even that: there is no 실손 참조순보험요율
to form the denominator with [R20].

### 5년 재가입 — re-entry into the then-current generation

The second structural peculiarity, and what makes the contract boundary a real question
rather than a formality. 감독규정 제7-63조제2항제6호나목 requires the 보험기간 및 보장내용
**변경주기를 5년 이내로** [REG-R17]; 4세대 shortened it from the 15 years 2세대 carried
[R1] [S4]. S1 제23조, inserted at the 4세대 amendment, is the operative clause:

- **Conditions**: the insured's age at re-entry is within the company's stated range, and the
  prior contract's premium was paid in full [제1항].
- **No health underwriting**: 「이 경우 회사는 기존계약의 가입 이후 발생한 상해 또는 질병을
  사유로 가입을 거절할 수 없습니다」 [제1항]; and on expiry of automatic renewal the
  policyholder may take whichever 실손 product the company is then selling and 「회사는 이를
  거절할 수 없습니다」 [제2항]. The FSC restates it: 「보험회사는 재가입주기 도래 時, 소비자의
  과거 사고 이력 등을 이유로 재가입을 거절하지 못합니다」 [R2].
- **Notice**: at least **twice** before the 변경주기 ends, stating the conditions, what has
  changed in cover, the premium level and the procedure [제3항].
- **Where the policyholder's decision cannot be obtained** (including loss of contact) the
  contract is **extended on the previous terms** [제5항]; the policyholder may cancel that
  extension within **90 days** with a full refund of premium paid after extension [제6항]; the
  extension runs until the insurer establishes the policyholder's intention — typically the
  date of the first claim — whereupon re-entry occurs and the old contract terminates [제7항].
  One carrier caps the limbo at 「보험기간이 종료된 날로부터 1년」 [S3 제53조제7항].

**What this does to the projection.** A 4세대 contract has a contractual life of **five years
in its own form**; at the fifth 계약해당일 its benefit terms are replaced by whatever the
supervisor is then prescribing, at a premium the insurer sets for that product. The FSS's
2026 supervisory programme puts the first wave in terms: 「'21.7월 도입된 4세대 실손의
재가입주기(5년)가 도래하여 순차적인 전환 실시」 [R7]. The policy reason is stated as faster
propagation of NHI coverage changes into the private layer [R2] — which is the same reason
the 관리급여 category can move a treatment from the rider to the main contract mid-projection
[R6].

**The contract boundary is genuinely contestable and this document asserts no answer.** A
one-year term, an unrestricted right to re-rate at each renewal, a supervisor-set 25% cap on
that re-rating, a five-year re-entry into a wording the insurer does not control, and an
obligation not to refuse re-entry on health grounds — no retrieved source states an industry
or supervisory position on where the IFRS 17 boundary falls for that combination, and the
general boundary test was read only in secondary summary form [unverified]. `Medical_KR_S`
projects to a stated horizon on stated terms and computes no CSM; § *Regulatory context*
says what it does and does not compute.

### Suspension, resumption and duplicate cover

**개인실손 중지제도.** A policyholder covered by a 단체실손 (group indemnity cover, typically
employer-provided) may suspend the individual policy for the duration and resume it when the
group cover ends, applying within one month [R16]. The facility is **mandatory**:
감독규정 제7-63조제2항제7호 requires a suspend-and-resume facility for policyholders doubly
covered through a group scheme, and 제8호 a conversion facility from group-only cover to an
individual policy [REG-R17]. A carrier's mechanics: resumption is into the product in force
at suspension unless the 보장내용 변경주기 has passed or the policyholder asks otherwise, in
which case into the current product; the 보장공백기간 must be no more than one month per
contract and three months cumulatively; and four attributes must match for the resumed policy
to count as the same — **보장종목, 보험가입금액, 자기부담금, 최대 보장가능 보험나이** [S3].
5세대 extends the scheme to 노후실손 and 유병력자실손 and adds a suspension right for
insureds with documented long-term overseas residence [R5] [S3]. `Medical_KR_S` carries
suspension as a parameterized decrement, off in the base run.

**다수보험 — proportional sharing.** 「동일한 위험을 보장하는 2개 이상의 계약에 중복 가입
하더라도 실제 발생한 손해(비용)를 초과하여 보험금을 지급하지 않습니다. (중복 가입 시
비례보상)」 [S3], per S1 제37조 (다수보험의 처리) and 제38조 (연대책임). This is why the
policy count (36.22 million) exceeds the insured-person count (about 40 million insureds
across all products including group) in a way that would be impossible on a fixed-sum
contract [R7] [R4]: duplicate 실손 cover buys nothing, and the supervisor tightened the
drafting at 5세대 because carriers were interpreting it inconsistently [R5].

### Claim settlement, documentation and 실손24

**The timetable** [S1 제8조]: payment within **3 영업일** of receipt of the documents; where
investigation is needed the insurer must immediately notify a payment date and the 가지급
option, and that date must fall within **30 영업일** except in six listed cases (litigation,
dispute mediation, criminal investigation, an overseas event, the policyholder's refusal of
consent, referral for a third-party medical opinion); interest runs on late payment at the
rate in the 약관's 붙임2; and on request the insurer must pay **50%** of its own estimate as
a 가지급보험금.

**The documents** [S1 제7조]: 청구서, 사고증명서 (진료비계산서, 진료비세부내역서,
입원치료확인서, 의사처방전) and 신분증. The 사고증명서 must be issued by a **domestic**
provider — 「「의료법」 제3조(의료기관)에서 규정한 국내의 의료기관에서 발급한 것이어야
합니다」 — and treatment by a foreign provider is excluded from cover altogether
[S1 제7조제2항] [S1 특별약관 제4조].

**실손24 changes frequency, not cost, and that matters here more than elsewhere.** The
청구 전산화 (electronic claim submission) scheme was introduced by amendment of the 보험업법,
with 보험개발원 designated the statutory 전송대행기관 [R13] [R14]. Phase 1 (2024-10-25)
covered 병원급 institutions with 30 or more beds plus 보건소 — 7,822 institutions in scope
[R14], of which 4,223 had joined at launch, a weighted participation of 54.7% and an
estimated 56.9% of claims by volume [R13]. Phase 2 (2025-10-25) added 의원 and 약국,
bringing the total in scope to **104,541**, of which 10,920 (10.4%) were connected at
launch [R14]. The documents
transmitted are 계산서·영수증, 진료비 세부산정내역서 and 처방전 [R14]. **A lower friction
cost of claiming raises the reported frequency of small claims, and small claims are exactly
where the deductible bites** — a ₩30,000 outpatient visit at a clinic pays ₩20,000 gross of
nothing else, and whether it is claimed at all is a behavioural question that the electronic
channel has changed within the model's calibration window. It also feeds the experience
rating: a claim not made is a claim not counted in `C(y)`.

**Dispute volume as a model caution.** 신경성형술 disputes alone were about **20%** of all
실손 disputes in 2025 [R7], and the mechanism is that where the insurer will not accept that
admission was medically necessary it pays only the outpatient benefit — ₩200,000–₩300,000 —
against an inpatient limit of ₩50,000,000 [R7]. **The inpatient/outpatient classification of
a claim is worth two orders of magnitude in the benefit, and it is contested.** No projection
model resolves that; it is recorded so that the severity split between the two is read as a
modelling choice with real dispersion behind it.

### 고지의무, 청약철회 and the pre-inception window

**계약 전 알릴 의무** is the Korean duty of disclosure and the 표준약관 states in terms that
it 「상법상 '고지의무'와 같습니다」 [REG-R25 제13조·제14조](#krlib-reg-r25). It is an answer-the-question
duty on a written or on-screen questionnaire, and 상법 제651조의2 presumes material any
matter the insurer asked about in writing [REG-R49]. Termination for breach is barred where
the insurer knew or was negligent in not knowing at formation; after **one month** from the
insurer learning of the breach; after **two years** from the 보장개시일 with no claim event
(**one year** for disease in a 진단계약); after **three years** from the contract date; where
the insurer accepted on a health-examination document and the claim arises from a matter
stated in it; or where the 보험설계사 prevented truthful disclosure [REG-R25]. A causation
defence applies, and non-disclosure of **other insurance held** is expressly not a ground —
which matters on an indemnity product where duplicate cover is real [REG-R25 제14조제5항](#krlib-reg-r25).
Fraud — proxy examination, drugs taken to pass underwriting, forged certificates, concealment
of a pre-application cancer or HIV diagnosis — allows cancellation within **five years** of
the 보장개시일 and one month of discovery [REG-R25 제15조](#krlib-reg-r25).

**청약철회** is the statutory cooling-off right of 금융소비자보호법 제46조제1항제1호:
「「상법」 제640조에 따른 보험증권을 받은 날부터 **15일**과 청약을 한 날부터 **30일** 중
먼저 도래하는 기간」, effective on despatch, with no damages or penalty, and ineffective if
a claim event has already occurred unless the policyholder withdrew knowing it had [REG-R51]
[REG-R25 제17조](#krlib-reg-r25). The 표준약관's exclusion for contracts of 90 days or less does not reach a
one-year 실손 contract. **품질보증해지** allows cancellation within **three months** of
formation where the 약관 was not delivered, its important content not explained, or the
policyholder did not sign, with premiums returned plus 보험계약대출이율 interest — 상법
제638조의3제2항 is the statutory source [REG-R25 제18조제3항](#krlib-reg-r25) [REG-R49]. `krlib` models from
the point cover is in force and treats both windows as out of scope: they are pre-inception
decrements and modelling them would need a new-business funnel this library does not have.

**Cover attaches at 보장개시** — the date the contract is concluded and the first premium
received, or the date of receipt where the premium accompanied the application [S1 제24조].
There is **no general waiting period**, which is unusual among Korean health products and is
a direct consequence of the indemnity form: there is no lump sum to anti-select against. The
one deferred item is the two-year wait on 불임관련 질환 급여 cover introduced at 4세대 [R1].

### Grace, lapse, reinstatement and the persistency basis

A missed premium produces a 납입최고 (demand) of at least **14 days**, after which the
contract terminates the day after the period ends [REG-R25 제26조](#krlib-reg-r25). **There is nothing to
break the fall**: with no surrender value there is no 보험료 자동대출납입 to advance the
premium, and 표준약관 제33조 excludes 「순수보장성보험 등」 from policy lending anyway
[REG-R25]. The lapse is real and immediate — the same structural position as the
[jplib third-sector chassis](../../../jplib/products/medical/product-spec.md), reached by the
same route. **부활** is available within **three years** where the surrender value has not
been drawn, which on this contract is always, on payment of arrears with interest at a rate
within 평균공시이율 + 1%; the insurer may not refuse because a claim event occurred before
termination [REG-R25 제27조](#krlib-reg-r25).

**No 실손-specific persistency table exists in public.** The best retrieved proxy is the
run-off of the closed generations: the 1–3세대 in-force block fell by **99만건 (3.3%)** in
2025, from 137만건 (4.4%) in 2024 [R7]. That rate blends lapse, death and conversion and is
**remarkably low** for a protection product — which is what one expects of cover 65% of whose
holders never claim but almost all of whom expect to. Industry-wide 장기손해보험 13회차 and
25회차 유지율 of 86.3% and 68.3% (2021), and 86.5% and 69.9% (2024 H1), are the only other
figures found and are **[unverified]**, from news summaries. `Medical_KR_S` calibrates
`lapse_rate` against the 3.3% decay with the blending caveat stated at the point of use.

**Mortality runs the other way here.** On a one-year indemnity contract death is a
termination that **releases** the liability, so the direction of prudence in the mortality
basis is opposite to that of the protection products in this library. The 제10회 경험생명표 is
not published in full — only summary statistics are released [REG-R33] — so every mortality
rate in `krlib` is a **[std]** construction on 통계청 완전생명표 data with a `provenance`
column [REG-R38] [REG-R39], and on this product an over-statement of mortality is
*anti*-conservative.

---

## Riders and options

The vocabulary of the sister libraries does not transfer cleanly. A Korean 실손 contract has
no rider menu in the jplib sense: the **비급여 특별약관 is the rider**, it is the second
half of the product, and everything else a carrier attaches sits on the *host* 통합형 policy
rather than on the 실손 covers. What follows lists what `Medical_KR_S` carries.

**In scope (modelled or parameterized):**

- **기본형 실손의료보험 (급여 실손의료비)** — the 주계약, with 상해급여형 and 질병급여형. On
  in the base run and not switchable off: a 실손 contract without it does not exist [S1].
- **실손의료보험 특별약관 (비급여 실손의료비)** — the rider, with 상해비급여형, 질병비급여형
  and 3대비급여형. On in the base run; switchable off, which removes 60% of the premium, the
  100-visit cap, the three sub-limits and **the whole experience-rating loop** [S1] [R2].
- **3대비급여형** — the three sub-limited classes with their shared 50-act counter and the
  10-visit re-assessment gate. On in the base run; switchable off within the rider [S1].
- **요율 상대도 (비급여 할인·할증)** — the five-band experience rating on the rider net
  premium, with the solved band-1 discount. On from the fourth policy year, reflecting the
  2024-07-01 commencement three years after launch [S1] [R3]. Switchable, and switched off
  it makes the contract a plain attained-age renewable.
- **무사고 할인** — the two-year claim-free 10% discount on the whole office premium,
  stacking with the band-1 relativity [R1] [S3]. On in the base run.
- **보험가입금액 election** — ₩50,000,000 / ₩30,000,000 / ₩10,000,000 per 보장종목 with the
  per-visit cap stepping ₩200,000 / ₩150,000 / ₩100,000; the maximum in the base run
  [S1] [S3].
- **개인실손 중지·재개** — a suspension decrement with a resumption rule, off in the base run
  [R16] [S3] [REG-R17].
- **재가입 (five-year re-entry)** — a scheduled terms change at the fifth 계약해당일, with no
  health underwriting. Parameterized as a horizon, not as a decrement [S1 제23조].

**Out of scope:**

- **노후실손의료보험** and **유병력자실손의료보험** — separate families with their own
  co-payments, issue ages (raised to 90 on both from 2025-04-01), cover ages (110 on 노후실손)
  and **three-year** change cycles [R17] [REG-R17 제7-63조제2항제5호](#krlib-reg-r17); the FSS reports them as
  a separate 2.4% block outside the five generations [R7], and their parameter detail is
  [unverified].
- **단체실손의료보험** (group cover) — excluded from the FSS statistics this model calibrates
  to [R7], and the reason the 중지제도 exists.
- **해외여행 실손의료보험**, two further standard wordings in the same annex [S1]; and the
  **의료급여 수급권자 할인**, 5% at one carrier and not in the 표준약관 [S3].
- **계약전환 (generation conversion)** and the 계약재매입 / 선택형 할인 특약 schemes for the
  pre-2013-03 block — supervisory constructs rather than policy rights, commencing 2026-11
  [R5] [R6]. They move policies between generations and are the mechanism behind the in-force
  run-off this model calibrates its lapse rate against, but they are not a decrement of the
  4세대 contract.
- **The behavioural response to the experience rating** — the FAQ's own worked example shows
  a policyholder cutting claims by 93% in response to a surcharge [R2]. `Medical_KR_S`
  projects the loop on a fixed frequency basis and does not model the feedback from premium
  to behaviour. Stated as a limitation.
- **1세대, 2세대, 3세대 and 5세대 wordings** — recorded in § *Variations across insurers* so
  that the model can be re-parameterized, but not implemented.

---

## Variations across insurers

**The honest answer for this product is that carrier variation in the benefit is close to
zero, and all the variation is in price, in the selectable 보험가입금액 and in the
discounts.** That is the opposite of the position in the
[jplib medical chassis](../../../jplib/products/medical/product-spec.md) or a UK critical
illness definition set, and it is a direct consequence of the 표준약관 regime: the
benefit definition is issued by the supervisor under 시행세칙 제5-13조제1항 and reproduced by
the carrier [REG-R23] [REG-R25]. **A `krlib` product spec for 실손의료보험 that named a
representative carrier would be making a category error — the representative contract is the
표준약관.**

| Feature | Set by | Varies? | Observed range |
|---|---|---|---|
| 보장종목 structure (급여 주계약 / 비급여 특약) | 표준약관 [S1] | **No** | identical at every carrier |
| 자기부담률 (급여 20%, 비급여 30%) | 표준약관 [S1] | **No** | identical |
| 통원 공제금액 (₩10,000 / ₩20,000 / ₩30,000) | 표준약관 [S1] | **No** | identical |
| 3대비급여 sub-limits (350 / 250 / 300만원; 50 / 50 / ∞회) | 표준약관 [S1] | **No** | identical |
| 100-visit annual 비급여 통원 cap | 표준약관 [S1] | **No** | identical |
| 급여 입원 연간 자기부담 200만원 | 표준약관 [S1] [REG-R17] | **No** | identical; already present in 2세대 [S4] |
| 요율 상대도 bands (100 / 200 / 300 / 400%) | 표준약관 [S1] | **No** | identical |
| ±25% annual renewal corridor | 표준약관 [S1] / 감독규정 [REG-R17] | **No** | identical |
| 보장내용 변경주기 | supervisory | **No**, within a generation | 15년 (2세대) [S4]; **5년** (4세대) [R1]; 「최대 5년」 (5세대) [S3] |
| 요율 상대도 **discount** factor (band 1) | solved for revenue neutrality [S1] | **Yes** | 「5% 내외」 [R1]; −5% 잠정 [R3]; 「α%」 in a carrier document [S3]; 95% relativity in the wording's illustration [S1]; **4.25% solved** here |
| 연간 보험가입금액 | 표준약관 sets a ceiling; carrier offers a menu | **Yes** | 「5천만원 이내에서 회사가 정한 금액 중 계약자가 선택한 금액」 [S1]; a 5세대 menu is ₩50m / ₩30m / ₩10m [S3] |
| 통원 회당 한도 | ditto | **Yes**, same ceiling | ₩200,000 ceiling [S1]; ₩100,000–₩200,000 observed [S3] |
| 가입나이 | carrier (사업방법서) | **Yes** | 0–49 on one direct-channel 2세대 product [S4]; **no 4세대 or 5세대 range retrieved** |
| 재가입 나이 / 최대 보장 연령 | carrier, within the framework | **Yes** | 재가입 15–99, cover to 보험나이 100 (2세대) [S4]; 재가입 to 99, cover to 보험나이 100 (5세대) [S3] |
| 무사고 할인 | supervisory design, carrier scope | **Slight** | 10% of the whole premium after two claim-free years, 4대 중증질환 excluded [R1]; one carrier's 5세대 wording also excludes 급여 and 특약1 claims from the test and excludes contracts without 특약2 [S3] |
| 의료급여 수급권자 할인 | carrier | **Yes** | 5% of 영업보험료 at one carrier [S3]; not found elsewhere |
| 해약환급금 | product design | **No** | none — 1년만기 순수보장성 [S3]. 통합형 hosts offer 미지급형 / 저지급형 on their **other** covers [S5] |
| Premium level | carrier | **Yes, materially** | the 손해보험협회 publishes per-carrier 인상률 and 손해율 precisely because of this [S6]; one carrier's 상해 담보 rose 23.9% (2025) and 21.8% (2026) against a reported industry average of 7.8% [unverified] |
| 갱신 안내 lead time | carrier | **Yes** | 15 days before expiry at one carrier [S5]; the 표준약관 requires 2회 이상 notice before the 변경주기 ends but sets no annual-renewal lead time [S1 제23조] |
| Re-entry limbo cap | carrier | **Yes** | open-ended in the 표준약관 [S1 제23조제7항]; capped at one year from term end at one carrier [S3] |

**What does not vary at all.** The benefit definition, the co-payment percentages, the
deductibles, the sub-limits, the visit counts, the 10-visit re-assessment rule, the
exclusions, the 180-day run-off, the 재가입 no-decline guarantee, the 보험나이 convention,
the ±25% corridor and the five 요율 상대도 bands. Those are the invariant core, and they are
invariant because they are regulation.

**The three choices this specification actually standardized**, restated in one place because
they are where a reader should look first if the model's numbers surprise them:

1. **The premium split, `s` = 60% to the 비급여 rider** (footnote 10). The two published
   values are 60% [R2] and the 48.75% implied by the 표준약관's own renewal illustration [S1].
   The choice matters because the experience relativity multiplies only the rider: at 60% a
   band-5 policyholder pays 2.80× the base total, at 48.75% only 2.46×.
2. **The band-1 discount solved from revenue neutrality on the [R12] band distribution,
   giving −4.25%**, rather than hard-coding the published −5% 잠정 [R3] (footnote 13). The
   wording defines the discount as the solution to a neutrality constraint, not as a number,
   so solving it keeps the scheme self-financing when the band distribution moves.
3. **The issue-age envelope, 0–65 만나이** (footnote 3). Nothing was retrieved for 4세대 or
   5세대; the only observed range is 0–49 on a 2세대 direct product [S4], and the upper bound
   is set below the 75-year 노후실손 threshold of 감독규정 제7-63조제2항제6호다목 [REG-R17].
   This is the widest single [std] in the document.

A fourth choice is a convention rather than a level and is stated separately for that reason:
the contract prices on **보험나이** and the model carries **만나이** (footnote 4), a
systematic half-year of age between the two.

### The 5세대 deltas — how to re-parameterize this model into the live generation

4세대 stopped being sold on 2026-05-05 and the in-force book begins re-entering 5세대 from
2026-07 [R5] [R7]. The mechanics are unchanged; the levels and the partition are not. Every
row below is a parameter change to the specification above, from the 5세대 표준약관 [S2],
the launch release [R5] and 감독규정 제7-63조제2항제2호·제2의2호·제2의3호 [REG-R17].

| Item | 4세대 (this specification) | 5세대 |
|---|---|---|
| Partition | 급여 주계약 + **비급여 특약** | 급여 주계약 + **특약1 (중증 비급여)** + **특약2 (비중증 비급여)**, all separately selectable — four permitted combinations [R6] |
| Definition of 중증 | — | 국민건강보험 **산정특례 대상 질환** (본인일부부담금 산정특례에 관한 기준 제4조–제5조의3), so the boundary moves when the health ministry moves it [S2] [R5] |
| 급여 입원 | 20% co-payment, ₩2,000,000 annual cap | **unchanged** |
| 급여 통원 deductible | `max(₩10,000 or ₩20,000, 20%)` | `Max[보장대상의료비 × 건강보험 본인부담률, 20%, ₩10,000 or ₩20,000]`, the 본인부담률 **computed from the receipt** as 급여 일부본인부담 본인부담금 ÷ (본인부담금 + 공단부담금) [S2] [S7] [REG-R25] |
| 급여 new cover | — | 임신·출산 (O00–O99) where the policy predates the expected delivery by 280 days; 정신발달장애 (F80–F89) for in-utero policies to 보험나이 18 [S2] [R5] |
| 비급여 입원 | 30% | 특약1 **30%**; 특약2 **50%** [S2] |
| 비급여 통원 | `max(₩30,000, 30%)`, 100 visits | 특약1 `Max[30%, ₩30,000]`, 100 visits; 특약2 `Max[50%, ₩50,000]`, **₩200,000 per day for 100 days** — per day, not per visit [S2] |
| 비급여 annual limit | ₩50,000,000 per 보장종목 | 특약1 ₩50,000,000; 특약2 **₩10,000,000**, with a **₩3,000,000 per-admission** cap at 병·의원 and MRI/MRA capped at ₩2,000,000 a year [S2] [S7] |
| New severe-inpatient cap | — | 특약1: where the deducted amount on 상급종합·종합병원 inpatient care exceeds **₩5,000,000** a year, only ₩5,000,000 is deducted (excluding 근골격계 이학요법·체외충격파 and 주사료) [S2] [REG-R17] |
| 3대비급여 | 도수·체외충격파·증식 350만/50회; 주사료 250만/50회; MRI 300만 | Carried into 특약1 with the same limits, but **근골격계 이학요법치료·체외충격파치료** replaces the three named procedures and is defined by reference to the 「건강보험 행위 급여·비급여 목록표 및 급여 상대가치점수」 — a deliberate anti-substitution definition [S2] |
| Outright exclusions | — | 특약2 excludes 근골격계 이학요법치료, 체외충격파치료, 비급여 주사제 and 미등재 신의료기술 including 첨단재생의료; both riders exclude treatments graded **D (권고하지 않음)** by the 한국보건의료연구원 [S2] [R5] |
| 할인·할증 | On the whole 비급여 특약 | On **특약2 only**; the exemption list narrows to 장기요양 1·2등급, because 산정특례 conditions now sit in 특약1 and outside 특약2 altogether [S2] [R5] |
| 할인·할증 commencement | 2024-07-01, three years after launch [R3] | **2028-05-06**, again two years deferred, at one carrier [S3] |
| Premium level | anchor ₩11,982 (40세 남, 2021-06) [R1] | **−30%** against 4세대, **−50% or more** against 1·2세대; base + 특약1 only ≈ **50%** of the 4세대 premium; 40대 남 ₩16,000 a month in 2026 [R5] |
| 보험가입금액 menu | not retrieved | ₩50m / ₩30m / ₩10m on 급여 and 특약1 (per-visit ₩200k / ₩150k / ₩100k); ₩10m / ₩6m / ₩2m on 특약2 (per-day ₩200k / ₩150k / ₩100k) [S3] |
| 관리급여 | — | A new NHI category at a **95% co-payment**, migrating over-used 비급여 items into the covered system. If 도수치료 becomes 관리급여 it leaves the rider and enters the main contract [R6] |

**A model that assumes the 급여/비급여 boundary is static will be wrong within the projection
horizon**, and the 관리급여 row is the reason. The taxonomy the FSC now publishes has four
tiers, not two [R6]: 급여 (입원 20%, 통원 30–60%), 선별급여 (100% or less, typically 30–80%),
**관리급여 (95%)** and 비급여 (100%).

### The other generations, for context

The in-force book at 2025-12-31, in 만건, with 2025 loss ratios [R7] [R8]:

| 세대 | Sale window | 2025 in force | 점유율 | 2025 경과손해율 | 자기부담률 as sold |
|---|---|---|---|---|---|
| 1세대 (舊실손) | ~2009-09 | 618 | 17.1% | 102.3% | 손보 0%, 생보 20% |
| 2세대 (표준화실손) | 2009-10 ~ 2017-03 | 1,494 | 41.2% | 93.1% | 급여 10%, 비급여 20% 등 |
| 3세대 (착한실손) | 2017-04 ~ 2021-06 | 783 | 21.6% | 120.3% | 급여 10/20%, 비급여 특약 30% |
| **4세대** | **2021-07 ~ 2026-05** | **641** | **17.7%** | **115.1%** | **급여 20%, 비급여 30%** |
| 노후·유병력자 등 | — | 86 | 2.4% | — | 30% 등 [unverified] |

Three facts about the older book bear on this model even though it does not implement them.
**1세대 had no common wording**: 손해보험회사 products frequently reimbursed 100% with no
co-payment at all, 생명보험회사 products 20%, and renewal was every three to five years [R7]
[R8]. **Contracts written before 2013-03 have no 약관변경(재가입) clause at all** — about
1.6천만건, **47.5%** of all in-force 실손 at 2024-12-31 [R4] [R5] — so they cannot be migrated
by the ordinary re-entry mechanism, which is why the 계약재매입 and 선택형 할인 특약 schemes
exist [R5] [R6]. And the per-policy claim in 2025 was 1세대 ₩740,000, 2세대 ₩490,000, 3세대
₩360,000, **4세대 ₩290,000** [R7] — a clean demonstration that the co-payment structure, not
the insured population, drives the claim.

---

## Regulatory context

**Classification.** 실손의료보험 is a **제3보험상품** under 보험업법 제2조제1호다목, in the
질병보험 and 상해보험 limbs of 제4조제1항제3호, closed at exactly three contract types by
시행령 제1조의2제4항 [REG-R1] [REG-R7]. 제4조제3항 deems a licensee for all 생명보험 종목,
or for all 손해보험 종목 excluding 보증 and 재보험, to hold the 제3보험 licence, which is why
both sectors write the identical contract and why the FSS reports them together [REG-R1]
[R7]. Korea does **not** treat sickness and injury as a sub-species of indemnity insurance:
나목 carves them expressly out of 손해보험상품 [REG-R1]. So this product is an indemnity
contract that is not, in Korean law, a 손해보험 — a distinction with no parallel in the other
libraries.

**The public scheme it sits on is not insurance at all.** 보험업법 시행령 제1조의2제1항
excludes 국민건강보험 from 「보험상품」 altogether, alongside 고용보험, 국민연금,
노인장기요양보험 and 산업재해보상보험 [REG-R7]. The private product and the public scheme are
different instruments in law, which is what licenses this document to describe 실손의료보험 as
a reimbursement layer above 국민건강보험 [REG-R53] without any suggestion that the two are the
same thing.

**Where the rules live, in order.** 보험업법 → 보험업법 시행령 → **보험업감독규정**
(금융위원회고시) → **보험업감독업무시행세칙** (금융감독원세칙) → **[별표 15] 표준약관**. The
FSC's 2026 legislative pre-announcement confirms the chain explicitly for this product: the
상품설계기준 sit in the 시행령 and the 감독규정, with the operative detail delegated to the
시행세칙 [R15]. 시행세칙 제5-13조 makes 별표 15 the 표준약관 [REG-R23], and 별표 15 is the
contract [S1] [S2] [REG-R25]. **This is the only product in `krlib` whose benefit definition
is a piece of published subordinate legislation**, and it is why every benefit row in this
document carries a clause reference rather than a carrier reference.

**The design rules — 보험업감독규정 제7-63조.** 제1항제2호 permits a 제3보험 benefit to be
designed on a 정액 or a **실손해** basis, and this product is the library's only 실손해
contract [REG-R17] [R19]. 제1항제1호 requires that on death from a non-covered cause the
계약자적립액 and the 미경과보험료 of 제7-66조제5항 be paid and the contract terminate
[REG-R17] — a provision that forces an account balance into every other `krlib` 제3보험
product and has no financial content here. 제2항 is the 실손 rule set itself, and the
2026-05-06 amendment is 5세대: 제2호 the 급여 co-payments, deductibles and the ₩2,000,000
annual inpatient cap; 제2의2호 and 제2의3호 the two 비급여 riders; **제3호 the ±25%
per-위험구분단위 corridor**; 제3의2호 and 제3의3호 the **요율 상대도** with its
twelve-months-ending-three-months-before window and the corridor applying to the
pre-relativity premium; 제5호 노후실손; and 제6호 the **annual rate-adequacy verification with
five years' grace** (가목) and the **five-year benefit-change cycle** (나목), three years for
노후실손 and 유병력자실손, plus the duty to sell or hold a 노후실손 product where cover
extends to age 75 and over (다목). 제7호 and 제8호 make the group-duplication suspension and
the group-to-individual conversion facilities mandatory [REG-R17].

A provenance note that must travel with those citations. The article text read for this
library is the version **in force from 2026-05-06**, i.e. the 5세대 text [REG-R17]. The
4세대-vintage 제7-63조제2항 was **not retrieved from a primary source**: 국가법령정보센터
serves the article body by JavaScript, and two HWP copies that did download were a pre-2013
vintage whose 제7-63조 has three 호 and no 제2항 at all [R19]. Every 4세대 design parameter in
this document is therefore taken from the 표준약관 that implements the rule [S1] and from the
supervisory releases that announced it [R1] [R2] [R5], and is cross-checked against the
current article where the two overlap. Given that the 표준약관 *is* the contract, the gap is
narrower than it looks, but it is recorded rather than papered over.

**Rate regulation.** Rates must rest on 「객관적이고 합리적인 통계자료를 기초로 대수의 법칙 및
통계신뢰도」 under 감독규정 제7-73조, which permits external statistics or a modified
참조순보험요율 where a company's own experience is insufficient and expressly contemplates
rates reflecting 「물가변동, 의료기술발달, 위험변화요인」 [R19]. 보험개발원 is the statutory
보험요율 산출기관 under 보험업법 제176조, and an insurer applying a filed 참조순보험요율 is
**deemed** to have filed its own net rate [REG-R4]. **But there is no 실손 참조순보험요율**:
the published 장기손해보험 categories are 일반상해, 교통상해, 질병 사망률, 후유장해, 입원율,
암 발생률, 비용손해, 재물손해 and 배상책임, and 실손의료보험 is not among them [R20]. Nor is
the 산출방법서 published: it is a 기초서류 under 보험업법 제5조제3호 and 제127조, filed and
verified but not disclosed [REG-R2]. The 선임계리사 verifies it under 제184조제1항 and is
barred from product development, the CEO role and the CFO role by 제184조제7항 [REG-R5]. The
public sees the result only as a **보험가격지수**, and for 실손 that index must be explained at
**every renewal** [REG-R22 제7-45조제7항](#krlib-reg-r22). **This is the exact boundary at which
`Medical_KR_S` marks its morbidity and severity basis [std]**, and the reason is a positive
finding rather than a failed retrieval.

**What can be calibrated against instead.** The supervisor publishes, annually and in
machine-readable form, more aggregate experience on this product than on any other in the
library: in-force counts by generation, premium income, claims split 급여/비급여, 경과손해율
overall and by generation with a stated break-even, claims by treatment category, claims by
provider class with the 비급여 share inside each, and per-policy claim amounts by generation
[R7] [R8] [REG-R44]. Add the twelve-band claim-size distribution by generation [R12], the 65%
zero-claim mass and top-decile concentration [R4] [R5] [R6], the coverage ratios by provider
class and age band [R9] [REG-R41] and the 본인부담상한제 threshold table [R10], and a
frequency–severity model can be fitted at the level of a whole policy year — which is the
level at which this contract's limits and deductibles operate.

**Reserving.** 보험업법 제120조제1항 requires a 책임준비금 and a 비상위험준비금 at each
결산기, carrying no method and no rate itself [REG-R3]. 시행령 제63조제1항, amended 2022-12-27,
restates the reserve in IFRS 17 vocabulary as **보험계약부채 = 발생사고요소 + 잔여보장요소**,
both on a 현행추정치 basis, and confines 비상위험준비금 to non-life business [REG-R8]. On a
one-year indemnity contract the weighting inverts relative to every other `krlib` product: the
잔여보장요소 is at most one year's unearned premium and the 발생사고요소 is the material item.
The **해약환급금준비금** of 감독규정 제6-11조의6 — the Korea-specific overlay that exists
because IFRS 17 measurement can fall below the contractual surrender value — has nothing to
bite on, because there is no surrender value [REG-R11]. The 표준해약공제액 cap of [별표 14]
likewise does not engage [REG-R20]. **`Medical_KR_S` computes no reserve of any kind**; it
projects the cash flows that would feed one.

**Solvency.** K-ICS has been in force since 2023-01-01 alongside K-IFRS 1117. 시행령
제65조제2항제1호 states the requirement in one line — 「지급여력비율은 100분의 100 이상을
유지할 것」 [REG-R8] — and 감독규정 제7-2조제2항 decomposes the 생명·장기손해보험위험액 into
seven sub-risks, of which three bear directly on this product: **장해·질병위험액** (a shock to
morbidity), **해지위험액** (「보험계약자의 옵션행사율 변화 또는 보험계약 대량해지」) and
**대재해위험액** for epidemics and mass accidents, measured by 위험계수방식 rather than by
shock [REG-R13]. A one-year renewable indemnity contract is the archetype of a product whose
capital charge is dominated by the morbidity shock and by the lapse-option risk, and whose
interest-rate exposure is negligible; `krlib` computes neither.

**IFRS 17 and the contract boundary.** K-IFRS 제1117호 has been mandatory for Korean insurers
since 2023-01-01 — not voluntary as in Japan [REG-R60]. The boundary question this contract
raises is genuine and this document asserts no answer: a one-year term, an unrestricted right
to re-rate at renewal, a supervisor-set ±25% cap on that re-rating, a five-year re-entry into
a wording the insurer does not control, and an obligation not to refuse re-entry on health
grounds. Nothing retrieved states an industry or supervisory position on where the boundary
falls for that combination, and the general boundary test was read only in secondary summary
form [unverified]. What the regime does require of a model is that its projections be
re-runnable on a re-set assumption basis at a stated 기준일, which is what this one is.

**Consumer protection.** 청약철회 is 금융소비자보호법 제46조제1항제1호 — 15 days from receipt
of the 보험증권 or 30 days from application, whichever comes first, effective on despatch, no
penalty, ineffective after a claim event unless the policyholder knew [REG-R51]. 상법
제638조의3제2항 is behind 품질보증해지 [REG-R49]; 제651조 and 제651조의2 behind the
고지의무 regime, with a written question presumed material [REG-R49]; 제649조 gives the
미경과보험료 on mid-term cancellation [REG-R49]; 제662조 the three-year prescription
[REG-R49]. On the 인보험 side 제729조 bars subrogation except by agreement in an 상해보험
[REG-R50] — relevant here because the 급여 exclusions already net off 자동차보험 and 산재보험
recoveries [S1 제4조제3항]. Deposit protection is ₩100,000,000 per person per insurer under
예금자보호법 시행령 제18조제7항, in a bucket for 보험금 separate from retirement-pension and
연금저축 claims; the 해약환급금 leg of that bucket is empty on this contract [REG-R52] [S3].
The 실손24 electronic claim channel rests on an amendment of the 보험업법 designating
보험개발원 the 전송대행기관, which the Act forbids from aggregating the data for any other
purpose on pain of criminal penalty; **the exact article number was not established** and is
not asserted [R13] [R14].

**Tax.** Premiums on this contract qualify for the **보장성보험료 세액공제** of 소득세법
제59조의4제1항 — a **credit** of 12% of premiums paid, capped at ₩1,000,000 of premium a year,
so at most ₩120,000 of tax before the local surtax, on a contract whose 「만기에 환급되는
금액이 납입보험료를 초과하지 아니하는」 test a pure protection 실손 contract passes trivially
[REG-R57]. On the anchor cell that is ₩11,982 × 12 = ₩143,784 of annual premium, capped to
₩1,000,000 without binding, giving a credit of about **₩17,254** — real, and second order.
Note that this is a credit, not a deduction, which changes the after-tax comparison against
every other market in this repository. Benefits are not modelled net of policyholder tax.

**What this model does not compute.** No 책임준비금, no CSM, no risk adjustment, no
fulfilment cash flow, no K-ICS requirement, no 해약환급금준비금, no 비상위험준비금 and no
policyholder tax. `Medical_KR_S` produces a liability cash-flow projection — premiums net of
expenses, less claims, on a monthly grid, through the renewal and re-entry machinery — and
leaves every measurement basis to be applied to it downstream.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-indemnity_medical-r1
[R10]: #krlib-indemnity_medical-r10
[R11]: #krlib-indemnity_medical-r11
[R12]: #krlib-indemnity_medical-r12
[R13]: #krlib-indemnity_medical-r13
[R14]: #krlib-indemnity_medical-r14
[R15]: #krlib-indemnity_medical-r15
[R16]: #krlib-indemnity_medical-r16
[R17]: #krlib-indemnity_medical-r17
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
[REG-R1]: #krlib-reg-r1
[REG-R11]: #krlib-reg-r11
[REG-R13]: #krlib-reg-r13
[REG-R17]: #krlib-reg-r17
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
[REG-R49]: #krlib-reg-r49
[REG-R5]: #krlib-reg-r5
[REG-R50]: #krlib-reg-r50
[REG-R51]: #krlib-reg-r51
[REG-R52]: #krlib-reg-r52
[REG-R53]: #krlib-reg-r53
[REG-R54]: #krlib-reg-r54
[REG-R57]: #krlib-reg-r57
[REG-R60]: #krlib-reg-r60
[REG-R7]: #krlib-reg-r7
[REG-R8]: #krlib-reg-r8
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
