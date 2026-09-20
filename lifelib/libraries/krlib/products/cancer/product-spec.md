# Product Specification

**Status:** Draft, 2026-09-03 (every cited source accessed 2026-09-03).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modelling of a Korean **cancer insurance (암보험, *am boheom*)** contract —
a fixed-benefit (정액, *jeongaek*) 제3보험 (*je-sam boheom*, third-sector) policy whose
benefits are triggered by the **diagnosis** of a disease named in a schedule keyed to the KCD
(한국표준질병·사인분류, the Korean Standard Classification of Diseases), and secondarily by
cancer surgery, cancer inpatient days and anti-cancer drug or radiation treatment. It describes
**no single insurer's contract**, and it must not be read as one.

Facts carrying a source tag — [S#] (primary product documents: 보험약관 (*boheom yakgwan*,
policy conditions), 상품요약서, 상품 공시 페이지) and [R#] (product-specific regulatory,
actuarial, statistical and legal references), both numbered per `_research/cancer.md` and
resolved in `sources.md` in this directory (numbering frozen, never renumbered), and [REG-R#]
(the cross-product reference library `references/regulatory-and-actuarial-references.md`, whose
own R-numbering is distinct and also frozen) — name the document the claim was read from.
Values marked **[std]** are standardizations introduced for the reference implementation; each
[std] row carries a numbered footnote giving the rationale and, where the research file
brackets it, the range observed across insurers. Claims no retrieved document could confirm are
flagged [unverified].

The composite is drawn from **seven carriers**: one 손해보험 (non-life) writer's contract in
two editions eight years apart, so that what changed is visible [S1] [S2]; three contracts
from one 생명보험 (life) writer — a non-renewable stand-alone main contract [S3], a 23-module
renewable product [S4] and a treatment-cost-only product [S5]; two from a second life writer,
one of which has **no waiting period at all** [S6] [S7]; and one non-life product page carrying
the session's only published premium and surrender-value illustration [S8]. Two carrier
documents are consumer-education rather than contractual [S9] [S10], and **Korea's largest life
insurer is not represented by any product document**: its product page returned a JavaScript
shell [S11]. Company and branded product names appear only in `sources.md` and in
`_research/cancer.md`.

**What this document defines for the rest of `krlib`.** `Cancer_KR_S` is the library's
**fixed-benefit 제3보험 chassis**, and five mechanics are specified here once, in full, so that
`LTC_KR_S` (간병보험) and `Child_KR_S` (어린이보험) can state deltas against them rather than
restate them:

1. **Diagnosis-triggered lump sums** graded by a **tier ladder** — 고액암 above, 일반암 in the
   middle, 특정소액암 and 유사암 (*yusa-am*, "similar cancers") below — where the tier is
   decided by a public statistical classification incorporated by reference, not by a clinical
   definition the insurer writes for itself.
2. The **90-day 면책기간** (*myeonchaek gigan*, waiting period) before cover starts, and its
   four carve-outs. A diagnosis inside it does not merely go unpaid: it makes the affected
   cover **무효** (*muhyo*, void), with premiums returned.
3. The **감액기간** (*gamaek gigan*, reduced-benefit period) — a stated fraction of the benefit
   for the first one or two years — sitting *on top of* the waiting period as a second, softer
   anti-selection device.
4. The **유사암** reduced tier, at a stated fraction of the general-tier amount, which is what
   lets a product cover a fast-growing, high-survival decrement without repricing.
5. A **post-diagnosis survival model**. This is the mechanic that distinguishes a cancer
   contract from a death contract: the diagnosis benefit is not the end of the liability. The
   premium waiver runs from the diagnosis until 납입완료 or death, the inpatient, surgery and
   treatment benefits are incurred over months and years after it, and a 재진단암 clock only
   opens two years later. An incidence rate alone cannot say for how long any of that runs.

The incidence basis is **published**, which no other morbidity product in this library can
say: 보험개발원 displays a dated 「기타피부암 및 갑상선암 이외의 암 발생률」 grid by age and
sex on the *insured* definition of cancer [R5] [REG-R61], and the shipped table reproduces it.
It is reconciled below against 국가암등록통계 age-specific incidence and five-year relative
survival [R1] [REG-R40], which is also what the tiers the bureau does not publish are derived
from. Where a rate is nevertheless standardized, it is marked [std] and the public quantity it
is anchored on is named.

**Deltas the two inheriting products will state.** `LTC_KR_S` replaces the KCD-keyed diagnosis
trigger with a **statutory** one, the 노인장기요양보험 등급 [REG-R54] [REG-R55], and replaces
the lump sum with a continuing annuity, so its post-onset survival model is the whole product
rather than a correction to it. `Child_KR_S` inherits the tier ladder and the 감액기간 but
**disapplies the 면책기간** below 보험나이 15 [S2] [R3] [R6], carries no death benefit below
age 15 by force of 상법 제732조 [REG-R50], and runs on a paediatric incidence curve two orders
of magnitude below the adult one [R1].

---

## Product overview and market role

### 제3보험, and why both sides of the market write the same contract

Korean law does not treat sickness and injury cover as a species of indemnity insurance. It
makes them a **third class of insurance product** in their own right. 보험업법 제2조제1호
splits 보험상품 into 생명보험상품, 손해보험상품 — expressly **excluding** 「다목에 따른
질병ㆍ상해 및 간병」 — and **제3보험상품**, being cover 「사람의 질병ㆍ상해 또는 이에 따른
간병에 관하여」 [REG-R1]. 제4조제1항제3호 lists the three 보험종목 of 제3보험업: 상해보험,
질병보험, 간병보험 [REG-R1] [R8]. Cancer insurance is 질병보험.

The provision that makes the class a shared field is **제4조제3항**: a licensee for the whole
of 생명보험업, or for the whole of 손해보험업 excluding 보증보험 and 재보험, 「제3보험업에
해당하는 보험종목에 대한 허가를 받은 것으로 본다」 [REG-R1] [R8]. A life insurer and a non-life
insurer therefore write the identical cancer contract without a further licence, and the
retrieved documents bear that out at the level of the clause: [S1] [S2] [S8] are non-life
contracts and [S3] [S4] [S5] [S6] [S7] are life contracts, carrying the same benefits, the same
definitions and the same 면책기간. 감독규정 제7-61조 applies the whole of the 제3보험 design
rule 제7-63조 to 장기손해보험, so the two are designed identically by regulation and not merely
by convention [REG-R17].

Private-law recognition arrived late and thinly. 상법 제739조의2 (질병보험자의 책임) and
제739조의3 (준용규정) were both **신설 2014-03-11** [REG-R50] [R7]; before that a disease
contract was construed by analogy to life and accident cover, which 제739조의3 now says
expressly. There is no 질병보험 chapter of substance: the contract law of this product is
borrowed law, and its detail lives in the 약관 and in the 표준약관 [REG-R25].

### The public scheme underneath, and why the product is 정액 rather than indemnity

Korea's cancer product is not a bill-reimbursement product, and the reason is statutory. A
registered cancer patient pays **5% of the total 요양급여비용** for **five years** from
registration, inpatient and outpatient alike, under 국민건강보험법 제44조제1항, 시행령
제19조제1항 및 별표 2, and 「본인일부부담금 산정특례에 관한 기준」 제4조 및 별표 3, extendable
where residual, metastatic or recurrent disease is under continuing chemotherapy [R11]. On top
of that sits the 본인부담상한제 of 제44조제2항, which refunds annual co-payments above an
income-graded ceiling [REG-R53].

With the scheduled bill already capped at 5%, there is very little bill left to indemnify.
Every retrieved contract pays 보험가입금액 (*boheom gaipgeumaek*, the sum insured) or a stated
fraction of it on a defined event, and **none of them indemnifies a cost**. What the lump sum
replaces is stated by the research institute rather than by the carriers: 「암은 통상적으로
치료기간이 길고 치료비용이 많이 발생하며 간병비 등 부대비용과 암을 치료하는 기간 동안
경제활동을 하지 못함으로 인하여 발생하는 소득 감소분까지 감안하면」 [R3]. It is an
income-and-incidentals benefit wearing the clothes of a medical one.

That also fixes where the residual exposure sits. The public scheme's boundary is a **negative
list** — 요양급여 covers everything the Minister has not designated 비급여 [REG-R53] — and it
is that residual which Korea's *other* health product, `Medical_KR_S` (실손의료보험), pays.
`Cancer_KR_S` is deliberately blind to the 급여/비급여 boundary, which is why the two sit
beside each other in almost every Korean household's portfolio without overlapping.

One dated cost anchor exists and is quoted with its date: 국립암센터's 2009 release put the
average per-patient economic burden at **₩29,700,000 (2,970만원)**, highest for leukaemia at
₩67,000,000, then 간암 ₩66,200,000, 췌장암 ₩63,700,000, 폐암 ₩46,600,000 [R3]; a carrier
repeats a ₩50,000,000-plus figure for 고액암 without a date [S9]. Both are historical, and the
composite's ₩30,000,000 sum insured is standardized rather than taken from either.

### Market size and where the line sits

Korea's life market is a **protection market with a shrinking savings tail** — the opposite of
the French and German mixes in `frlib` and `delib`. On the research institute's 2026 forecast,
보장성보험 is **52.8%** of life premium against 저축성 at 20.8%, with 보장성 premium rising
from ₩48.6조 (2023) to ₩55.0조 (2024) to a forecast **₩66.2조 (2026)** while 저축성 falls from
₩28.1조 to ₩26.1조; on the non-life side 장기손해보험 — overwhelmingly 장기인보험: health,
cancer, care and accident cover written under the 제4조제3항 deeming provision — runs from
₩64.3조 (2023) to a forecast **₩75.9조 (2026)** [REG-R46] [REG-R47]. Cancer cover is written
inside both aggregates and **no retrieved source splits 암보험 out of them**: there is no
Korean analogue of Japan's per-line policy-count series, and no 암보험 in-force count,
new-business count or market share is asserted anywhere in this document.

What *is* retrievable is the disclosure architecture that makes the product documentable. The
생명보험협회 공시실 carries 상품비교공시 across eleven protection classes, 경영공시 and
기타공시, and is the public route to 약관, 상품요약서 and 해약환급금 illustrations [REG-R45];
every [S#] in this folder was reached through it or through a carrier's own 공시실. A
보장성보험 must publish a **보험가격지수** — 보험료총액 ÷ (참조순보험료 총액 + 보험회사
평균사업비총액) — and a 보장범위지수 in its 상품요약서 [REG-R22], so the rate bureau's
reference rates become visible to the public only as a *ratio*, never as a rate. That is the
single most important fact about pricing transparency in this market.

### The epidemiology that makes the product modellable, and what it constrains

The 국가암등록통계 annex is public, dated and complete enough to build an incidence basis from
[R1] [REG-R40]. Its 2023 headline: **288,613** new cancers (남 151,126 / 여 137,487), 조발생률
**564.3** per 100,000 (남 593.4 / 여 535.5), 연령표준화발생률 **522.9** (남 587.0 / 여 488.9)
on the 2020 주민등록연앙인구 standard [R1], corroborated independently at [R2]. Lifetime risk
of a cancer diagnosis is **41.2%** — **남 44.6%, 여 38.2%** [R1]. Four features are
load-bearing and each constrains a design choice.

**First, the crude and the standardised series disagree violently about trend.** The crude rate
has risen 161% since 1999 (216.0 → 564.3) while the age-standardised rate has risen 30% (402.7
→ 522.9) and has been broadly flat since 2017 [R1]. A cancer contract written to age 100 is
exposed to the **crude** series, because it ages with its policyholder. That is the
quantitative content of the institute's 추세리스크 warning: 「현재도 암 발생률은 상승하고
있으며, 향후 어느 시점에서 암 발생률 상승이 멈출지는 예측하기 어려움」 [R4].

**Second, the male and female curves cross, and the crossing point is published.** 「50대
초반까지는 여자의 암발생률이 더 높다가, 50대 후반부터 남자의 암발생률이 더 높아지는」 [R1]. At
40–49 the female crude rate is **2.43×** the male (590.0 against 243.0); at 80+ the male rate
is **2.25×** the female (2,930.2 against 1,304.5) [R1]. **A unisex cancer basis is materially
wrong at every age, and wrong in opposite directions either side of about 55.** The published
reference-rate table crosses at the same place [R5].

**Third, thyroid cancer is 12.3% of all registered cancers — the single largest site — and its
five-year relative survival is 100.2%**, statistically indistinguishable from the general
population, on a lifetime mortality risk of **0.1%** [R1]. The registry publishes the
excluding-thyroid basis explicitly (253,173 cases, 조발생률 495.0, 표준화 454.0), which is what
makes a *sourced* general-tier incidence rate constructible [R1]. The 유사암 tier is that
arithmetic turned into a contract term, and any incidence table that does not separate C73 will
misprice the product by a wide margin [REG-R40].

**Fourth, the insurable event is survivable and the survival is improving fast.** Five-year
relative survival for 2019–2023 diagnoses is **73.7%** all sites (남 68.2 / 여 79.4) and
**69.6%** excluding thyroid, against 42.9% for 1993–1995 diagnoses [R1]. Prevalence at
2024-01-01 was **2,732,906** persons — **5.3%** of the population — of whom **62.1%** were more
than five years from diagnosis [R1]. A benefit menu built around a diagnosis lump sum, a
premium waiver and a treatment-linked payment stream, rather than around a death benefit,
follows directly; so does the need for a post-diagnosis survival model.

### The two chassis in the market, and where the composite sits

The retrieved contracts fall into two shapes. **Diagnosis-centred**: the main contract pays a
graded diagnosis lump sum and nothing else, with treatment benefits as separate modules — [S3],
[S6] and [S7]. **Event-centred**: the contract pays on surgery, inpatient days and chemotherapy
or radiotherapy, and at one carrier there is **no diagnosis lump sum at all** [S5]. Between
them sit the granular non-life contracts, carrying both plus twenty or more named riders [S1]
[S2], and the modular product in which twenty-three independent 주계약 modules are sold in any
combination [S4]. The composite is **diagnosis-centred with the event benefits attached and
independently switchable**, so that any observed shape is a configuration rather than a
different model. The choice is not neutral and the reason is at footnote (1): the diagnosis
benefit is the only limb whose decrement is sourceable from public data, and it is the limb the
면책기간, the 감액기간 and the tier ladder all attach to.

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | 암보험, 무배당 (*mubaedang*, non-participating), 정액 (fixed-benefit); a stand-alone 주계약 paying graded diagnosis benefits, with inpatient, surgery and anti-cancer treatment benefits attached as 특별약관 modules | [S3] [S4]; menu **[std]** (1) |
| Regulatory class | 제3보험상품 — 질병보험 (보험업법 제2조제1호다목, 제4조제1항제3호) | [REG-R1]; [R8] |
| Written by | Either a 생명보험회사 or a 손해보험회사, on the 제4조제3항 deeming provision; the composite is drafted as a life insurer's contract | [REG-R1]; [S1] [S3]; **[std]** (1) |
| 보장성 / 저축성 | **보장성보험** — the maturity value does not exceed premiums paid at the 기준연령 요건 (감독규정 제1-2조제3호) | [REG-R9]; [REG-R57] |
| Chassis | **비갱신형** (*bi-gaengsinhyeong*, non-renewable): one contract, level premium, cover to the 100세 계약해당일. A **10년 갱신형** flag is carried as a model-point switch | [S3] [S5] vs [S4] [S6] [S7] [S8]; **[std]** (2) |
| Policy term (보험기간) | To the **100세 계약해당일**; no 만기환급금 | [S4] [S7]; [R3]; **[std]** (3) |
| Premium-paying period (보험료 납입기간) | **20년납** default; 10년납, 30년납 and 전기납 as variants | [S1] [S3] [S8]; **[std]** (4) |
| Issue age (가입나이) | **보험나이 15–65** | [S1]; observed 20–60 [S8], to 85 on renewal [S7], to 75 on 간편심사 [R4]; **[std]** (5) |
| Contractual age basis | **보험나이** (*boheom nai*, insurance age): 계약일 현재 만 나이 with a fraction under six months discarded and six months or more rounded up, incrementing at each 계약해당일 | [S3]; [REG-R25 제21조](#krlib-reg-r25) |
| Model age basis | **만나이** (age last birthday) | **[std]** (6) |
| Sum insured (보험가입금액) | **₩30,000,000 (3천만원)** — the 일반암 진단급여금, which is the unit every other diagnosis tier is a ratio of | [S3] [S10]; [R3]; level **[std]** (7) |
| Lives basis | Single life. No retrieved contract writes a joint life and none states the restriction | [S1]–[S8]; observed absence, **[std]** (1) |
| Underwriting | 표준체 with a 계약 전 알릴 의무 questionnaire; **비흡연체형** is a formal 약관 chapter with its own rate basis; **간편심사** (simplified, no hypertension or diabetes question) is what lets the issue age reach 75 | [S3]; [R4]; **[std]** (8) |
| Substandard terms | 보험가입금액 한도 제한, 일부 보장 제외, 보험금 삭감 or 보험료 할증, and a 특정 신체부위·질병 보장제한부 인수 특약 | [S3] |
| 배당 | None — 무배당 | [S1] [S3] [S8]; [REG-R12] |
| Death benefit | **None.** Death from a cause the policy does not cover pays the **계약자적립액** and terminates the contract | [S3]; [REG-R17 제7-63조제1항제1호](#krlib-reg-r17); [REG-R25 제22조](#krlib-reg-r25); [REG-R50 제736조](#krlib-reg-r50) |
| 암보장개시일 | The **91st day** counting the 보험계약일 as day 1 | [S1] [S2] [S3] [S4] [S7]; [R3] [R6]; **[std]** (16) |
| **Anchor model cell (point_id 1)** | Male, **보험나이 40**, 보험기간 to 100세, **20년납**, 보험가입금액 **₩30,000,000**, 표준체, 해약환급금 미지급형, all four benefit modules on — giving 일반암 진단급여금 ₩30,000,000, 고액암 top-up ₩30,000,000, 특정소액암 ₩18,000,000, 유사암 ₩6,000,000, 암 입원급여금 ₩50,000 per day to 180 days per stay, 암 수술급여금 ₩5,000,000 관혈 / ₩1,000,000 비관혈, 항암약물·방사선 치료급여금 ₩10,000,000 최초 1회한, premium waiver on invasive diagnosis, level premium **₩45,000 per month** | **[std]** (9) |

Footnotes to the [std] rows:

1. **The menu, and the licence.** The retrieved contracts carry four irreconcilable menu
   shapes: a graded diagnosis benefit alone, in five tiers [S3] or three [S6] [S7]; a diagnosis
   benefit plus inpatient, surgery, treatment and death modules in one non-life contract [S1]
   [S2]; twenty-three independently purchasable 주계약 modules [S4]; and a
   **treatment-cost-only** contract with no diagnosis lump sum at all [S5]. The composite
   carries a graded diagnosis benefit plus three event modules, **each independently
   switchable**, so that a model point can be configured into the first, second or fourth
   shape, and the third is that shape with the diagnosis limb switched off. It is drafted as a
   **life** insurer's contract because the two cleanest retrieved main contracts are [S3] and
   [S4], because the life form has no 적립부분 / 보장부분 split to carry, and because 감독규정
   제7-61조 makes the non-life form's design rules identical [REG-R17] — so nothing in the
   model turns on the choice. Joint lives are an observed absence, not a stated exclusion.
2. **비갱신형 or 갱신형 is the largest structural choice in this document.** Observed: 비갱신
   at two carriers [S3] [S5]; 갱신 at four, on terms of 10 years, 1–10 years, to a 100세
   계약해당일 and to a 100세 만기 once past 가입나이 85 [S4] [S6] [S7] [S8]; and a **15-year
   term with 재가입** at the two non-life contracts [S1] [S2]. Four of seven renew, so the
   composite departs from the majority, and the reason is that **the 면책기간 and the 감액기간
   are disapplied on every 갱신계약** [S2] [S4] [S6] [S7]. On a renewable chassis the two
   devices this product exists to demonstrate bite once, in the first ten years of a sixty-year
   projection, and are invisible thereafter; on a 비갱신형 chassis they bite once at the start
   and their present-value effect is stated cleanly. The 비갱신형 form is also the only one on
   which a level premium, a 계약자적립액 and a 해약환급금 curve exist over the whole term. The
   renewable form is carried as a flag and specified in *Contractual mechanics*.
3. **100세 만기.** Two retrieved contracts run to a 100세 계약해당일 [S4] [S7], and the
   supervisor's 2013 description of where the market moved reads 보험기간 「통상 80세 이하」 →
   「100세 혹은 사망 시(종신)까지」 [R3]. 종신 was not taken because no retrieved life contract
   is written 종신 and because a terminal age lets the projection end at a stated 계약해당일
   rather than at the terminal age of a [std] mortality table. There is no 만기환급금: one
   non-life product pays **5% of 보험가입금액** at maturity on a 2종 variant [S8] and one
   credits the 적립부분 to a 만기환급금 [S1], but the only retrieved surrender-value
   illustration shows the value falling to **nil at maturity** on the 순수보장형 form [S8].
4. **20년납.** Observed: 5 / 10 / 15년 on a 15-year non-life term [S1]; 전기납 [S8]; and a
   20년납 worked example inside the 해약환급금 article of the cleanest life contract (계약일
   2018-09-01, 납입기간 중 = to 2038-08-31) [S3]. Twenty years is taken for three reasons that
   point the same way. It is the **해약공제계수 cap** for a 보장성보험 in 감독규정 [별표 14] —
   「보험기간(최대 20년)」 — and the payment term that schedule's note 3 forces the
   연납순보험료 to be recomputed on where the policy term is 20 years or more [REG-R20]. It
   puts 납입완료 at a **known date**, which makes the 무해지 surrender-value step-up a cliff
   rather than a curve [S3]. And it leaves 40 years of paid-up cover on the anchor cell, so the
   projection exercises both halves of every recursion. 전기납 is retained as a variant because
   a 전기납 contract on the 미지급형 basis has **no surrender value at any duration** [S3].
5. **Issue ages.** Observed: 만15~65세 [S1]; 20~60세 최초계약 with renewal ages 30–80 and 81–89
   [S8]; renewal to a 100세 만기 once past 가입나이 85 [S7]; and, on 간편심사 products, an
   upper bound of **75** reached only by dropping the hypertension and diabetes questions [R4].
   The composite takes the one range a retrieved 약관 states in terms, **15–65**. The lower
   bound matters more than it looks: at 보험나이 15 the 면책기간 carve-out of footnote (17)
   switches sign, and 15 is the age 상법 제732조 uses for death cover [REG-R50]. The upper
   bound is left at 65 rather than raised to 75, because [R4] names the 61–75 band as the one
   carrying **수준리스크** from an absence of experience — 「가입연령 확대로 새롭게 가입이
   확대된 연령층(61~75세)에 대한 경험 부족」 — and a reference implementation should not
   silently price a band the market itself says it cannot price.
6. **The two age bases, and why the model uses the second.** The contract ages on **보험나이**:
   「계약일 현재 피보험자의 실제 만 나이를 기준으로 6개월 미만의 끝수는 버리고 6개월 이상의
   끝수는 1년으로 하여 계산하며, 이후 매년 계약 해당일에 나이가 증가」, with the 약관's own
   example 생년월일 1988-10-02, 계약일 2018-04-13 ⇒ 29년 6월 11일 ⇒ **보험나이 30세** [S3]; the
   표준약관 carries the identical rule [REG-R25 제21조](#krlib-reg-r25). Because of the six-month rule 보험나이
   differs from 만나이 for **roughly half of all issue dates**, and it increments on the policy
   anniversary rather than on the birthday. **`Cancer_KR_S` projects on 만나이**, because every
   decrement it uses is published on 만나이 — the 국가암등록통계 age bands [R1], the
   참조순보험요율 age grid [R5] and the 국가데이터처 생명표 [REG-R38] — and converting a public
   만나이 rate to a 보험나이 basis would need a distribution of issue dates within the policy
   year that no source supplies. The half-year average offset is a **[std] simplification**,
   recorded here, in the model registry and in `technical-notes.md`, and it is not negligible
   on the steep part of the curve: between 60 and 70 the published male rate roughly doubles
   [R5], so half a year of age is worth about 3.5% of the rate.
7. **The sum insured.** ₩30,000,000 is a **level**, and the level is standardized because the
   retrieved documents give ratios far more often than amounts: the one clean ladder states
   every tier at 보험가입금액 1,000만원, so the ratios are read but the level is not fixed [S3
   별표 1]. The observed anchors are a 금융감독원 분쟁조정 case turning on 일반암 진단비
   **₩30,000,000** against 갑상선암 진단비 ₩3,000,000 [R3]; an earlier case on ₩50,000,000
   [R3]; the supervisor's 2013 illustration at 「예: 5천만 원」 [R3]; and a carrier's 2025
   statement putting **유사암** cover alone at up to ₩30,000,000 [S10]. ₩30,000,000 is the
   middle of that spread and the level at which the composite's 20% tier gives ₩6,000,000. It
   is also the parameter a model point should vary first: at a 최초 1회한 benefit the level
   scales the liability linearly and carries no structure.
8. **Underwriting.** 비흡연체형 is a formal chapter of the retrieved life 약관 — 제8관, with
   제53조 가입자격 and 제54조 흡연상태 변경통지 — and carries its own 보험요율 [S3]; on the
   modular product the split applies to some 세부보장 and not others [S4]. The composite is
   written 표준체 and carries the non-smoker class as a rate-basis switch, because **no
   retrieved document states the differential** and inventing one would be an unsourced pricing
   parameter. 간편심사 is named and not modelled for the same reason plus a stronger one:
   「간편 심사 암보험 상품이 과거에 판매된 적이 없기 때문에 간편 심사가 위험률에 미치는 영향에
   대한 분석이 충분치 못함」 [R4].
9. **The anchor cell.** Male at 보험나이 40 is chosen because it is the **기준연령 요건** of
   감독규정 제1-2조제2호 — 「전기납 및 월납 조건으로 남자가 만 40세에 보험에 가입하는 경우」
   [REG-R9] — the cell at which the 표준해약공제액 comparison [REG-R20], the 보험가입금액
   computation of [별표 15] [REG-R21] and the 보장성/저축성 test are all performed. Using it as
   the model's anchor makes the model point and the regulatory reference point the same cell,
   which no other choice achieves. It is also on the steep part of the incidence curve without
   being in the tail: the published male rate is 0.001343 at 40 against 0.008540 at 60 and
   0.027892 at 80 [R5]. The **₩45,000 monthly premium is a modelling input, not a quoted or
   computed market rate** — footnote (11).

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium basis | **Level** for the whole 납입기간, 무배당, no premium review on the 비갱신형 chassis. On the 갱신형 flag, recomputed at each renewal on the attained age and the rate basis then in force | [S3] [S5] vs [S4]; [REG-R12] |
| Frequency (납입주기) | **월납** (monthly); 3개월납, 6개월납 and 연납 available | [S1]; 월납 only at [S8]; default **[std]** (10) |
| Anchor premium | **₩45,000 per month** at the anchor cell | **[std]** (11) |
| Rating factors | 보험나이, sex, 보험가입금액, benefit modules elected, 납입기간, 흡연 여부, 계약 전 알릴 의무 outcome | [S3] [S4]; composite **[std]** (8) |
| Rate structure | **Not published by any carrier.** The 산출방법서 is a 기초서류 filed with the FSC, not a public document, and the 참조순보험요율 reaches the public only as the 보험가격지수 ratio | [REG-R2]; [REG-R22]; [REG-R4] [REG-R34] |
| Pricing method | **현금흐름방식** (cash-flow pricing) — mandatory for a contract longer than three years, with an adequacy analysis on 최적기초율 and projected cash flows | [REG-R18 제7-64조제1호](#krlib-reg-r18); [R4] |
| 예정이율 (pricing interest rate) | **2.50% p.a., 금리확정형** | **[std]** (12) |
| 계약자적립액 적용이율 | **2.50% p.a.**, equal to the 예정이율 on a 금리확정형 design | [S8] at 1.5%; [S1] floor 0.5%; **[std]** (12) |
| Premium during the waiting period | **Payable from the 보험계약일.** The 유사암 tier and every non-cancer cover are already in force, and the invalidity rule of footnote (18) returns the premium for the affected cover if it bites | [S1] [S2] [S3]; **[std]** (16) |
| Acquisition cost (계약체결비용) | Named in the 약관, **never quantified**; the composite sets it at or below the **표준해약공제액** of 감독규정 [별표 14] | [S1]; [REG-R20]; [REG-R22]; **[std]** (13) |
| Maintenance cost (계약관리비용) | Named, never quantified; a per-policy monthly amount plus a percentage of premium | [S1]; **[std]** (13) |
| Commission | First-year remuneration may not exceed the first year's expected premium; instalment structures pay no more than **60% of the 표준해약공제액** a year | [REG-R22 제4-32조제5항·제8항](#krlib-reg-r22); [REG-R29] |
| Premium waiver (보험료 납입면제) | On the **first diagnosis of an invasive cancer** — 일반암 or 고액암 — on or after the 암보장개시일, or on a 장해지급률 of **50% 이상**. **유사암 and 특정소액암 do not trigger it** | [S3 제14조제1항] [S1 제9조제1항] [S6] [S7]; **[std]** (14) |
| Waiver and renewal | On a 갱신계약 the waiver does **not** carry over; a cancer already waived re-arms only after **5 years** from the renewal's 보장개시일 with no further diagnosis or treatment | [S4]; scope **[std]** (2) |
| Lapse assumption in pricing | A **최적해지율** must have been used to price the 미지급형 form at all; the 표준형 comparator is computed **without** a lapse assumption | [S3]; [REG-R19 제7-66조제4항](#krlib-reg-r19); [REG-R27]; **[std]** (15) |
| 보험료 지수 disclosure | 보험가격지수 and 보장범위지수 published in the 상품요약서 | [REG-R22 제7-45조제7항](#krlib-reg-r22) |

10. **월납** is the dominant retail mode, the only mode at one direct writer [S8], and the mode
    named in the 기준연령 요건 itself [REG-R9]. It is also why `Cancer_KR_S` runs on a
    **monthly grid**: the 90-day waiting period then lands on a grid boundary at `t = 3`, the
    감액기간 at `t = 12`, and the premium stream and the 계약자적립액 recursion share one time
    step. 감독규정 제7-65조제2항 permits the 계약자적립액 to be computed on an **annualised
    premium** basis — 「연납보험료를 기준으로 하여 산출할 수 있다」 — which is the provision
    that lets a monthly-premium Korean product carry an annual account recursion, and it is the
    reconciliation `Cancer_KR_S`, `Medical_KR_S`, `Child_KR_S` and `LTC_KR_S` all use
    [REG-R18].
11. **The anchor premium is a model-point input.** No carrier publishes a rate table for this
    product, and the only retrieved premium figures — ₩119,280, ₩187,332 and ₩347,292 a year at
    남자 40세 / 월납 / 10년납 10년만기 / 순수보장형 [S8] — come with **no stated
    보험가입금액**, so they are price points without a benefit denominator. Consumer-comparison
    snippets offering 「40세 남성, 일반암 진단비 1,000만원 → 월 11,270원」 and 「암진단금
    3,000만원 → 월 4만원 비갱신형」 are not carrier documents and are [unverified]. ₩45,000 is
    anchored by arithmetic rather than by quotation: from age 40 a male's remaining lifetime
    probability of an invasive diagnosis is a little under the **44.6%** lifetime figure [R1],
    and removing thyroid — 12.3% of registered cancers, concentrated below 50 [R1] — leaves
    roughly 0.38 as the probability that the ₩30,000,000 general-tier benefit is ever paid.
    Undiscounted that is ₩11.4m; at the 2.50% 예정이율 over an average deferral near thirty
    years it is nearer ₩5.5m, and the 특정소액암, 유사암, 고액암, inpatient, surgery, treatment
    and waiver limbs together with acquisition and maintenance expense carry it to roughly ₩9m.
    Against a 20-year monthly premium whose annuity factor at 2.50% is about sixteen years'
    worth, that is an annual premium near ₩560,000, or **₩47,000 a month**; ₩45,000 is the
    round figure in that neighbourhood. **`technical-notes.md` performs the equivalence
    calculation on the shipped basis and its figure governs where the two differ**; nothing in
    this library depends on ₩45,000 being a market rate.
12. **Interest.** A full-text search of the 감독규정 returns **zero** occurrences of 예정이율:
    the regulation speaks only of the **계약자적립액 적용이율** and of the 금리확정형 /
    금리연동형 distinction of 제1-2조제6호·제7호 [REG-R9] [REG-R48]. The 예정이율 of a specific
    Korean product is therefore not a published number for any product in this library, and
    every one of them is [std]. The anchor is the **평균공시이율**, which *is* a regulatory
    figure computed by the FSS Governor under 제1-2조제13호 [REG-R9] and which stands at
    **2.50% for 2026**, down from 2.75% in 2024 and 2025 — its first fall since the 2.50% →
    2.25% cut that took effect for 2021 [REG-R48]. The composite takes 2.50% and a
    **금리확정형** design, the natural one for a 비갱신형 protection contract whose
    계약자적립액 is small. The observed bracket is wide and
    both ends are recorded: one non-life product credits its 계약자적립액 at 「연복리
    **1.5%**」 [S8], another the 공시이율 with a 최저보증이율 of 「연단위 복리 **0.5%**」 [S1].
    On a 금리연동형 design the 공시이율 is reset off a published 공시기준이율 under
    제7-65조제3항 [REG-R18]; that machinery belongs to `WholeLife_KR_S` and `Cancer_KR_S` does
    not implement it.
13. **Expenses.** No retrieved document quantifies any expense item for this product. [S1]
    names 계약체결비용 and 계약관리비용 without amounts; [S8] states the surrender value is
    「계약자적립액에서 **해약공제액**을 공제한 금액」 without quantifying the deduction. What
    is available is a statutory ceiling and a practitioner's rule of thumb, and the composite
    sets its acquisition cost between them: [별표 14] caps the deductible acquisition cost at
    the **표준해약공제액** [REG-R20], and the FSC's 2019 expense reform states the same cap as
    **13 months' premium for a 보장성보험** [REG-R29]. Setting 계약체결비용 at or below the
    표준해약공제액 is conservative and keeps the product outside the 계약체결비용지수
    disclosure trigger of 제7-45조제11항 [REG-R22]. The arithmetic is at footnote (30).
14. **The premium waiver, and why it is the product's most interesting decrement.** The trigger
    sets observed are narrow, explicit and different. One life contract waives on
    「'암(직·결장암, 유방암, 여성생식기암, 전립선암, 기타피부암, 갑상선암, 대장점막내암 제외)'
    또는 '중증 갑상선암'으로 진단이 확정되거나 … 장해지급률을 더하여 **50% 이상** 장해상태가
    되었을 경우」, and states expressly that 특정 소액암 and every 유사암 member other than
    중증 갑상선암 do **not** waive [S3 제14조제1항]. A non-life contract waives on 암 (유사암
    제외), 뇌출혈 or 급성심근경색증 [S1 제9조제1항]. Two more waive on 장해 50% and cancer [S6]
    [S7]. One switches the waiver on and off through the **사업방법서** and not through the
    약관 at all, so its presence cannot be read from the policy conditions [S2]. The composite
    takes **invasive cancer plus 장해 50%**, excluding 특정소액암 and 유사암 — the majority
    trigger, and the one that makes the waiver a **correlated** decrement rather than an
    independent one. Every model point that fires the general-tier diagnosis benefit for the
    first time must also stop the premium stream and keep it stopped for as long as the insured
    survives inside the 납입기간, which is what the post-diagnosis survival model of footnote
    (25) is for. The 장해분류표 the disability limb keys to is 표준약관 부표 3, which defines
    장해 as a **permanent** impairment remaining after treatment and excludes temporary states
    [REG-R25].

### Benefit provisions

All amounts are stated at the anchor cell's 보험가입금액 of ₩30,000,000 and, where a module
has its own 보험가입금액, at that module's own level.

| Parameter | Representative value | Basis |
|---|---|---|
| 면책기간 (waiting period) | **90 days.** Cover for 암 attaches on the **암보장개시일**, being the day after 90 days have passed counting the 보험계약일 as day 1 | [S1] [S2] [S3] [S4] [S7]; [R3] [R6]; **[std]** (16) |
| Carve-outs from the waiting period | **유사암**: none. **갱신계약**: none — 암보장개시일 = 갱신일. **보험나이 15 미만**: none — 암보장개시일 = 보험계약일. **부활계약**: restarts from the 부활일 | [S1] [S2] [S4] [S7]; [R3] [R6]; **[std]** (17) |
| Diagnosis inside the waiting period | The **affected cover is 무효** and its premiums are returned; the rest of the contract survives unless the policyholder cancels it, which he may do **within 90 days** of the 진단확정일 | [S1 제28조제2항·제3항] [S2] [S3]; [R7 제644조](#krlib-cancer-r7); **[std]** (18) |
| 감액기간 (reduced-benefit period) | **1 year at 50%**, measured from the 보험계약일 to the 진단확정일, on **every** diagnosis tier; disapplied on a 갱신계약 | [S1] [S6] vs [S3] [S4] [S5] [S7] vs [S2]; [R6]; **[std]** (19) |
| Definition of 암 | By reference to the **제8차 한국표준질병·사인분류** (통계청 고시 제2020-175호, 시행 2021-01-01), with the 악성신생물 분류표 listed in a 별표; **기타피부암 (C44), 갑상선암 (C73), 대장점막내암 and 전암(前癌)상태 are carved out of it** | [S1] [S2] [S3] [S4]; [R3] [R10] |
| KCD vintage rule | The classification **in force at the 진단확정일** decides the tier, both ways; a later revision does not reopen a decided claim | [S3 제12조] [S4]; [R3]; **[std]** (20) |
| 원발부위 기준 | Where C77–C80 (secondary and unspecified sites) is diagnosed and a primary is identifiable, the **primary site** classifies the disease; the 진단확정 *timing* is **not** moved back to the primary's diagnosis date | [S1] [S2] [S3] [S4] [S5]; [R3]; mandated from 2011-04-01 |
| 진단확정 | By a **병리과 또는 진단검사의학과 전문의** on microscopic findings from 조직검사, 미세바늘흡인검사 or 혈액검사; documented clinical evidence admitted only where such a diagnosis is not possible | [S1]–[S7]; [R3] |
| Date of diagnosis | The **결과보고 시점** — the pathology report date, not the date the certificate was issued | [S2] [S3] [S4] [S10] |
| Third-opinion procedure | A 종합병원 소속 전문의 chosen by agreement, **at the insurer's entire expense** | [S1] [S2] [S3]; 의료법 제3조의3 |
| **일반암 진단급여금** | **₩30,000,000** = 100% of 보험가입금액, **최초 1회한** | [S3 별표 1]; **[std]** (21) |
| **고액암 진단급여금** | **₩30,000,000** paid **in addition** to the 일반암 benefit, 최초 1회한, on a named list: **C40–C41 (골 및 관절연골), C70–C72 (뇌 및 중추신경계통), C91–C95 + D47.1 + D47.5 (백혈병)** | [S3]; [S10]; **[std]** (22) |
| **특정소액암 진단급여금** | **₩18,000,000** = 60%, 최초 1회한: 직·결장암, 유방암 (C50), 여성생식기암, 전립선암 (C61) | [S3]; **[std]** (21) |
| **유사암 진단급여금** | **₩6,000,000** = 20%, **each member once**: 기타피부암 (C44), 갑상선암 (C73), 대장점막내암, 제자리암 (D00–D09 less 대장점막내암), 경계성종양 (D37–D48) | [S3] [S4]; [R12]; **[std]** (21) |
| 갑상선암 subdivision | **Not adopted.** C73 pays the flat 유사암 amount | [S3] [S4] vs [S1] [S2] [S6] [S7]; **[std]** (23) |
| **암 직접치료 입원급여금** | **₩50,000 per day** from day 1 of a stay whose direct purpose is cancer treatment, **180 days per stay**; 유사암 at **20%** of the daily amount | [S1] [S4]; [R3]; **[std]** (24) |
| One-stay grouping | Two or more admissions for the same cancer are **one stay**; a stay beginning more than **180 days** after the discharge that ended a paid stay is a new one | [R3]; **[std]** (24) |
| 요양병원 (convalescent-hospital) days | **Excluded** from the composite's inpatient benefit; carried as a separate rider capped at 90 days | [S2] [S8]; [S10]; **[std]** (24) |
| **암 수술급여금** | **₩5,000,000** per 관혈 (open) operation, **₩1,000,000** per 비관혈 — a **5 : 1** split — per qualifying surgery, unlimited count | [S4]; **[std]** (24) |
| Definition of 수술 | By a 수술분류표 plus a general clause; 흡인, 천자, 신경 BLOCK, cosmetic and contraceptive surgery, diagnostic procedures including 생검 and 복강경검사, and 발정술·내고정물제거술 are **excluded**; procedures approved by the 신의료기술평가위원회 are included; 대뇌내시경, 흉강경, 복강경 and 조혈모세포이식 rank as **관혈** | [S4]; [R3] |
| Simultaneous procedures | Where 관혈 and 비관혈 are performed in one operation only the **관혈** amount is paid | [S1] [S4] |
| **항암약물·방사선 치료급여금** | **₩10,000,000**, **최초 1회한**, on the first qualifying 항암화학요법·항암면역요법 drug treatment or 고에너지 전리 방사선 treatment; 유사암 at **20%** | [S1] [S4] [S5]; **[std]** (24) |
| Excluded from 항암약물치료 | Immune-support agents given with **no cancer cells present** (압노바, 헬릭소, 셀레나제 are named) | [S4] |
| Repeating diagnosis benefit | **Out of the base contract**; 재진단암 on a 2-year cycle is a rider, off in the base run | [S1] [S8]; [R4]; scope **[std]** (26) |
| Termination on payment | **None.** Payment of any diagnosis benefit neither terminates nor exhausts the contract; cover runs to the 100세 계약해당일 | [S1] [S3] [S4] |
| Death of the insured | No death benefit. The **계약자적립액 at the date of death** is paid and the contract ends | [S3 제31조제1항] [S4] [S5] [S6] [S7]; [REG-R17]; [REG-R25 제22조](#krlib-reg-r25) |
| Post-mortem crystallisation | Where the insured dies in the policy term and cancer is only then established as the direct cause, the **date of death is treated as the 진단확정일** and the benefit is paid, less any 계약자적립액 already paid out | [S1] [S3] [S4] |
| Exclusions (보험금을 지급하지 않는 사유) | The general 약관 exclusion articles were **not read in full** for this product line | [unverified]; **[std]** (28) |
| Suicide | The composite has **no death benefit**, so the suicide clause has nothing to attach to | [S3]; **[std]** (28) |

15. **The lapse assumption is not free.** 감독규정 제7-66조제4항 permits the 미지급형 form only
    where the premium or benefit was calculated using a **최적해지율** [REG-R19], and the FSS's
    November 2024 ruling then fixes the shape: among models converging to zero lapse at 완납
    the **로그-선형 모형** is the 원칙모형, converging to **0.1%**, with a post-완납 ultimate
    of **0.8%** [REG-R27]. `Cancer_KR_S` uses exactly that, tagged [std], with a 표준형 switch.
    **No public Korean lapse or persistency figure for 암보험 exists** [R3].
16. **The 90 days is a market convention, and this document asserts no more than that.** Every
    retrieved contract but one carries it, in wording stable across carriers and across eight
    years: 「「암」에 대한 보장개시일(책임개시일)은 이 계약의 보험계약일…부터 그 날을 포함하여
    90일이 지난 날의 다음 날로 합니다」, the 약관 printing a worked example — 보험계약일
    2014-04-10 ⇒ 보장개시일 2014-07-09 [S1], the 2026 edition printing the same example eight
    years on [S2] — and the life form adding the 부활 limb 「계약일(계약을 부활(효력회복)하는
    경우 부활(효력회복)일)부터」 [S3]. The institute [R3] and the supervisor [R6] both describe
    it as the norm. **It is not asserted to be a 표준약관 requirement**: the 생명보험 표준약관
    was read in full for the cross-product library and carries no 암보장개시일 clause
    [REG-R25], the 질병·상해보험 표준약관 within the same 별표 was not read in that pass, and
    the product research could not retrieve it separately [R13]. The decisive evidence is in
    the market — one retrieved product has **no waiting period at all**, defining 보장개시일 as
    the day the first premium is received and adding 「또한, 보장개시일을 계약일로 봅니다」
    [S6], which is only possible if the 90 days is permitted rather than required. On a monthly
    grid it is three months and lands on `t = 3`; the model claims no finer precision.
17. **The four carve-outs, each a modelling state.** (i) **유사암 are not subject to the wait**
    — 「유사암의 보장개시일은 계약일임」 [S1], the 면책기간 table marking 유사암 진단비 `×`
    [S1] [S2] and the summary marking the four 유사암 limbs `-` [S7]; one life carrier applies
    the wait to 갑상선암 [S3] [S4] and the composite follows the majority, so the benefit
    vector has **two start dates**, `t = 0` and `t = 3`. (ii) **A 갱신계약 has none** — 「갱신
    계약의 경우 갱신일로 합니다」 [S7], 「※ 갱신계약의 경우 면책기간을 적용하지 않습니다」 [S2]
    [S4]. (iii) **A life under 보험나이 15 has none** — 「단, 보험계약일 기준으로 피보험자의
    보험나이가 **15세 미만**인 경우에는 보험계약일을 보장개시일(책임개시일)로 합니다」 [S2],
    which the institute records as the convention [R3] and the supervisor names 어린이암보험 as
    the exception to [R6]. **This is the carve-out `Child_KR_S` inherits and inverts.** (iv)
    **부활 restarts the clock** from the 부활일 [S1] [S3] [S7].
18. **The invalidity rule is a de-recognition, not a decrement.** The statutory hook is 상법
    제644조: 「보험계약당시에 보험사고가 이미 발생하였거나 또는 발생할 수 없는 것인 때에는 그
    계약은 **무효**로 한다. 그러나 당사자 쌍방과 피보험자가 이를 알지 못한 때에는 그러하지
    아니하다」 [R7], and the institute states the consequence plainly [R3]. The retrieved 약관
    implement it at the level of the **individual cover** rather than the whole contract —
    「…암 진단비(유사암 제외)계약을 무효로 합니다」 [S1 제28조제2항] — and then give the
    policyholder an option, not an automatic unwinding: 「계약자는「암」의 진단확정일부터
    **90일 이내에** 무효가 된 계약 이외의 계약을 취소할 수 있으며」 [S1 제28조제3항]. Premiums
    for the voided cover are returned, with 보험계약대출이율 interest where the insurer was at
    fault [S1] [S3]. The rule reaches forward too: a bone metastasis diagnosed two years after
    a breast cancer itself diagnosed inside the wait is not 「암보장개시일 이후에 최초로 진단
    확정된 암」 (분쟁조정 제2003-64호) [R3], while a **genuine recurrence after clinical cure**
    is a new cancer, 「통상 의학적으로 완치란 5년 이내에 재발이 없는 경우를 의미하므로」
    (제2009-32호) [R3]. The committee's two rules in one sentence: 「암이 **전이**된 경우에는
    원발암이 진행된 것으로 보아 원발암 기준으로 판단을 하고, 암이 치료되었다가 **재발**한
    경우에는 새로운 암으로 보는 입장」 [R3].
19. **The 감액기간, and a deliberate departure from the modal design.** Observed: **none at
    all** on 일반암 in the newest contract, whose 감액지급 table does not list 암 진단비(유사암
    제외) [S2]; **1 year at 50%** across 23 named benefits at the same carrier eight years
    earlier [S1] and at one life carrier [S6]; **2 years at 50%** at four contracts from two
    life carriers [S3 제14조제9항] [S4] [S5] [S7]; and a **two-step** 25% / 50% on robot
    surgery at two [S2] [S5]. Two years is **modal**, at four of seven. The composite
    nevertheless takes **one year**, for reasons stated rather than hidden: it is the median of
    the three distinct designs; it is the level the supervisor describes — 「통상 보험계약일
    이후 1~2년 이내에 암 진단확정시에는 암보험 가입금액의 50%」 [R6]; the direction of travel
    is one-way, the institute recording removals from 2019 [R3] and a carrier confirming in
    2025 that 「일반암에 대한 감액 기간이 축소되는 등」 [S10]; and the 2026 contract shows
    where that landed, with **none on 일반암 and exactly one year on 유사암** [S2].
    `reduction_months` is a parameter and 24 and 0 are switches. What must **not** be done is
    to model the 감액 as a permanent benefit scaling: on a 갱신형 contract it bites only in the
    first policy term [S2] [S4] [S6] [S7], and on a 비갱신형 contract once, at the start.
20. **The KCD vintage rule cuts both ways, and that is recent.** The 2024–25 contracts take the
    symmetrical position — 「① …제8차 개정 한국표준질병·사인분류가 기준이나, 이후 진단 … 당시
    …개정된 경우에는 개정된 기준으로 최종 판단합니다. ② …진단 이후 …개정으로 …분류가
    변경되더라도 …다시 판단하지 않습니다」, with two worked examples in both of which the
    answer is "no benefit" [S3 제12조] [S4]. The older wording was asymmetric and produced
    litigation the policyholder won on the contra proferentem ground twice (분쟁조정
    제2012-14호 and 제2011-35호) [R3]; the Supreme Court then set the rule in a 직장유암종
    case, classification being judged on the KCD in force **at 진단확정** where that brings the
    disease in (대법원 2018. 7. 24. 선고 2017다256828) [R3]; and KIRI recommended the
    symmetrical wording in 2019 [R3], which the retrieved contracts now carry — research
    feeding through into policy wording inside five years. **The model does not implement a KCD
    revision**; it fixes the classification at KCD-8 and records that the benefit definition is
    not frozen at inception.
21. **The tier ladder, and where the ratios come from.** One contract states every tier as an
    amount at 보험가입금액 1,000만원, so the ratios are **read, not inferred** [S3 별표 1]:

    | 급부명칭 | 2년 미만 | 2년 이상 | ratio |
    |---|---|---|---|
    | 특정 고액치료비관련 암진단자금 (+ 암진단자금) | 500만원 (+500) | 1,000만원 (+1,000) | 200% |
    | 암진단자금 (일반암) | 500만원 | 1,000만원 | 100% |
    | 중증 갑상선암 진단자금 | 400만원 | 800만원 | 80% |
    | 특정 소액암 진단자금 | 300만원 | 600만원 | 60% |
    | 소액질병 진단자금 (each 유사암 member, once) | 100만원 | 200만원 | 20% |

    The composite adopts 200 / 100 / 60 / 20 and drops the 80% limb (footnote 23). The **유사암
    ratio of 20%** is the most contested parameter in the product and the observed range is
    enormous: **10%** at both contracts of one life carrier [S6] [S7]; **20%** at both of
    another [S3] [S4]; **70%** on a pre-2022 non-life design [S8]; a separately underwritten
    rider with its own 가입금액 at the two non-life contracts [S1] [S2]; and 「10~20%」 or "up
    to ₩30,000,000 absolute" as carriers' own descriptions [S9] [S10]. What moved it is
    reported but not primary: a 금융감독원 공문 of **August 2022** is said to have cut 유사암
    benefits to about **20%** of the 일반암 level, from a market in which they had reached
    ₩50,000,000 [R12]. **That is a news source and the 공문 was not retrieved**; what is
    sourced is the *effect* — 20% at the two 2024–25 life contracts [S3] [S4] against 70% in
    2021 [S8] — not the instrument. The **특정소액암 60%** limb comes from the same ladder
    [S3]; alternatives put 유방암·전립선암 in a 20% tier of their own [S6] [S7], name five
    sites without a ratio [S1] [S2], or give 유방·전립선 40% / 갑상선 30% / 기타피부 10% [R3].
    Every diagnosis benefit is **최초 1회한** in every retrieved contract without exception
    [S1]–[S7].
22. **고액암 is defined by enumeration and the enumeration is not standard.** Three retrieved
    lists disagree: a tight one, 「특정 고액치료비관련암 분류표」 = **C40–C41, C70–C72, C91–C95
    + D47.1 + D47.5** [S3]; a wide one sold as stacking riders, 「5대 주요암」 and 「10대
    주요암」 [S1] [S2]; and two carrier descriptions, a ten-site list [S9] and a 3 / 5 / 10
    ladder whose base is 「3대 고액암(뇌암, 뼈암, 백혈병)」 [S10]. The composite takes the
    **tight three-site list** — the only one given as KCD ranges rather than Korean site names,
    and the same three sites the carrier calls the market's base definition [S3] [S10]. Two
    consequences: the benefit **adds to** the general tier rather than replacing it [S3], so a
    leukaemia diagnosis pays 200% and a stomach cancer 100% and the model carries the two
    once-only flags separately; and the tier's incidence is **not separately published** — none
    of 골, 뇌 or 백혈병 is in the retrieved 2023 top-ten table [R1] — so the high-tier rate is
    a `[std]` construction and says so at the point of use.
23. **갑상선암 is not subdivided, and the reason is a data reason.** Two life contracts split
    C73 by histology and stage — 「중증 갑상선암」 being 수질암 or 역형성암, 「초기갑상선암」
    being 유두암 or 여포암 under **2.0cm** with no nodal or distant spread, and the remainder
    pushed into 특정 소액암 — so that one contract pays C73 at **80% / 60% / 20%** where the
    market convention is a flat 10–20% [S3] [S4]. The composite does not adopt it, because the
    국가암등록통계 publishes 갑상선 as one site and publishes **no histology and no tumour-size
    split** [R1]: every rate in a subdivided tier would be an unsourced invention. C73 pays the
    flat 유사암 amount and the subdivision is a switch whose rates a user must supply.
24. **The event benefits, and the one simplification that must be flagged.** *Inpatient*:
    observed as 180 days per stay with 유사암 at 「가입금액의 20%」 [S1]; as **상급종합병원
    only, 2일 이상, 1일 초과, 120일 한도** [S4]; and as a 4일 이상 form split into
    요양병원-excluded and 요양병원 riders [S8] [S2]. The institute describes the market as
    「1회 입원당 120일 또는 180일」 with same-cancer admissions summed and 「최종 입원의
    퇴원일부터 **180일이 경과하여 개시한 입원은 새로운 입원**」 [R3]. Composite: ₩50,000 from
    day 1, 180 days per stay, 요양병원 excluded to a separate 90-day rider — the market's own
    structural answer to the most disputed benefit in Korea, where 금융감독원 took **2,125
    complaints about 암입원비 in 2018** and by August 2019 had a TF taking 60–90 new 요양병원
    complaints a week [R3]. *Surgery*: the 5 : 1 관혈 / 비관혈 split is read directly [S4]; one
    carrier sells 최초 1회한 and 1회당 riders and requires both [S1]. *Treatment*: every
    retrieved contract pays it 「최초 1회한」 [S1] [S4] [S5], a sharp contrast with Japan's
    per-month design, and the newest edition splits the modality five ways [S2] where the
    composite carries one. **The simplification**: the composite applies **one 유사암
    relativity of 20%** to the diagnosis, inpatient and treatment limbs, and real contracts do
    not grade uniformly — on one 2018 contract the 유사암 are excluded outright from 암 진단비
    and paid in full under a separate rider, paid at 20% of the daily amount on 입원일당,
    excluded from 암 사망 for 제자리암·경계성종양 but included for 대장점막내암, and paid at
    20% on 항암치료비 **for 기타피부암 and 갑상선암 only** [S1], while another grades the
    treatment benefit at **25%** through a separate limb [S4]. A single relativity makes the
    tier vector one object and lets a user reprice the whole reduced tier by changing one
    number; the non-uniform pattern is recorded so that nobody mistakes the simplification for
    the market.
25. **The post-diagnosis survival model.** Specified in full at *Contractual mechanics → The
    post-diagnosis survival model*, with its calibration targets and their sources. In summary:
    a `[std]` select excess hazard over the base table, **zero** for the 유사암 tier on a
    thyroid five-year relative survival of **100.2%** and a lifetime thyroid mortality risk of
    **0.1%**, and calibrated to **69.6%** five-year relative survival for the general tier
    [R1].
26. **재진단암 is a rider, off in the base run, because its decrement cannot be sourced.** The
    cycle is **2 years** — 「첫 번째 재진단암 : …최초암의 진단확정일부터 그날을 포함하여
    **2년이 지난날의 다음날**임 2. 두 번째 이후 재진단암 : 직전 재진단암의 진단확정일부터
    …2년이 지난 날의 다음날」 [S1] — and the institute records the same convention [R3]. Four
    qualifying events are separately defined: **새로운 원발암** (a different histopathological
    character), **전이암**, **재발암** (the same character, after the cells had been cleared)
    and **잔여암** [S8]; and two termination rules make the rider finite, it lapsing if the
    first cancer has not been diagnosed and fewer than two years of term remain, and again if a
    재진단암 is diagnosed with fewer than two years remaining [S8]. A carrier describes the
    market benefit as 「매 1~2년마다」 [S10] but **no retrieved contract carries a 1-year
    cancer cycle**, so a one-year cycle is [unverified]; the 1-year machinery exists on the 두
    번째 뇌출혈 and 두 번째 급성심근경색증 riders beside the cancer cover [S1]. What cannot be
    sourced is the **rate**: no public source gives a cancer re-diagnosis incidence, the
    closest quantity being the registry's elapsed-time prevalence stock [R1], and the institute
    calls the quantity 「매우 불확실」 while warning that improving survival makes 「3차, 4차
    암 진단보험금 지급이 가능함」 [R4]. The rider is specified so a user can switch it on with
    their own rate.
27. **The surrender basis.** Specified at *Termination and values* and at *Contractual
    mechanics → 계약자적립액, 해약환급금 and the 표준해약공제액*.
28. **An honest gap.** The general 보험금을 지급하지 않는 사유 articles were not read in full
    for this product line and no retrieved document reproduces them [R3]. The composite carries
    **no exclusion set beyond the waiting-period invalidity rule of footnote (18), the 고지의무
    remedy and the 사기 remedy**; 상법 제659조 and 제660조 are named as the statutory floor
    without being read from a contract [REG-R49]. The one absence that is *not* a gap is
    suicide: with no death benefit the clause has nothing to attach to, and it becomes live
    only if the 암 사망 rider is switched on.

### Options

Every item is specified so that a model point can switch it on; the "Base" column says what
the shipped anchor cell does.

| Option | Representative specification | Base | Basis |
|---|---|---|---|
| **10년 갱신형 chassis flag** | Silence renews (objection required **15 days** before expiry); final renewal ends at the **100세 계약해당일**; premium recomputed at the attained age on the rate basis in force at renewal; **보험가입금액 unchanged**; a module that has paid its once-only benefit **does not renew**; no 면책기간, no 감액, no fresh 납입면제 on the renewed contract | off | [S4 제2-11조의6] [S2] [S6] [S7] |
| **재진단암 진단급여금** | 100% of 보험가입금액 on a **2-year** cycle from the previous qualifying diagnosis; 새로운 원발암 / 전이암 / 재발암 / 잔여암; excludes 기타피부암, 갑상선암, 전립선암, 대장점막내암; rider lapses inside the last two years of term | off | [S1] [S8]; [R3]; rate **[std]** (26) |
| **암 요양병원 입원급여금** | ₩20,000 per day, **90 days** per stay, on a stay at a 요양병원 for cancer treatment | off | [S2] [S8]; **[std]** (24) |
| **암 다빈치로봇 수술급여금** | ₩10,000,000 per robot-assisted cancer operation, on a **two-step 감액**: 25% inside 180 days, 50% from day 181 to one year, 100% thereafter | off | [S2] [S5] |
| **암 사망 및 고도후유장해** | 보험가입금액 on death, or on **80% 이상 후유장해**, caused by a cancer diagnosed after the 보장개시일; 대장점막내암 included, **제자리암 and 경계성종양 excluded**; 90-day wait and 1-year 50% 감액 on invasive cancer only | off | [S1] |
| **표준형 surrender basis** | The conventional 해약환급금 of 감독규정 제7-66조제1항, computed **without a lapse assumption**; a pricing comparator that **cannot be bought** — 「'표준형'은 보험료 및 해약환급금(환급률 포함)의 비교 안내만을 위한 상품으로 가입이 불가능하며」 | off (the base is 미지급형) | [S3 제41조]; [REG-R19] |
| **비흡연체형 rate class** | A separate 보험요율 under 약관 제8관, with 제53조 가입자격 and a 제54조 duty to notify a change of smoking status; the differential is **not published** | off | [S3]; **[std]** (8) |
| **간편심사 (simplified underwriting)** | 「최소한의 의적고지」 with **no hypertension or diabetes question**, raising the issue age to 75; the rating effect is **not analysable** on any retrieved source | out of scope | [R4]; **[std]** (8) |
| **만기환급형 (2종)** | **5% of 보험가입금액** returned at maturity where the contract is in force and premiums are fully paid | out of scope | [S8] |
| **5대 / 10대 주요암 riders** | Additional named-site diagnosis benefits stacking on the 일반암 amount, on a wider list than the composite's 고액암 tier | out of scope | [S1] [S2]; **[std]** (22) |
| **Modality-split 항암치료 riders** | 항암 양성자방사선, 항암 세기조절방사선, 표적항암약물허가, 항암 중입자방사선 and plain 항암방사선 as five separate riders, three of which carry a 1-year 50% 감액 that the plain one does not | out of scope | [S2] |
| **특정 신체부위·질병 보장제한부 인수 특약** | A 제도성특약 excluding a named body part or disease at underwriting; a metastasis from an excluded site is **not** a 합병증 and is excluded with it (분쟁조정 제2006-71호) | out of scope | [S3]; [R3] |
| **적립부분 (non-life form)** | A separate accumulation part credited at the 공시이율 with a **최저보증이율 of 0.5%**, from which mid-term withdrawal is allowed after 2 years, up to 4 times a policy year, capped at **80%** of the 적립부분 해지환급금 | out of scope | [S1] |
| **재가입 (non-life form)** | A 15-year term with re-entry at expiry into the insurer's then-current 재가입형 product, guaranteeing on refusal a contract with the same 보험가입금액 and 보장내용 at a repriced premium | out of scope | [S1] [S2] |

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| Surrender value form | **해약환급금 미지급형**: **0%** during the 납입기간, **50% of the 표준형 value** afterwards. A **전기납** contract on this form has no surrender value at any duration | [S3 제41조제2항]; [REG-R19 제7-66조제4항](#krlib-reg-r19); **[std]** (29) |
| Legal basis of the form | 감독규정 제7-66조제4항 — a 순수보장성보험 priced with a **최적해지율** may pay less than the 별표-14-floored value. Not a contractual gimmick: a regulatory dispensation conditional on having used a best-estimate lapse rate in pricing | [REG-R19]; [REG-R28] |
| 환급률 constraint | Where the payment-period value is under 50% of the 표준형's, both the post-payment value must exceed 50% of the 표준형's **and** the post-payment 환급률 must exceed the greater of 100% and the 표준형's 환급률 | [REG-R19 제7-66조제4항제2호](#krlib-reg-r19); [REG-R28] |
| Underlying calculation | 해약환급금 = max(계약자적립액 − 해약공제액, **0**); the negative case is floored at zero, not carried | [REG-R19 제7-66조제1항제1호](#krlib-reg-r19) |
| 해약공제액 | The **표준해약공제액** of 감독규정 [별표 14] | [REG-R20]; **[std]** (30) |
| 해약공제기간 | The 납입기간 or the 신계약비 부가기간, **capped at 7 years** | [REG-R19 제7-66조제1항제2호](#krlib-reg-r19) |
| 계약자적립액 accrual | **Monthly** before 납입완료, **daily** afterwards | [REG-R19 제7-66조제1항제4호](#krlib-reg-r19) |
| Unearned premium | On termination, the **미경과보험료** is added to whatever surrender value is paid | [REG-R19 제7-66조제5항](#krlib-reg-r19) |
| 만기환급금 | **None** — 순수보장형; the surrender value peaks around years 5–7 and falls to nil at maturity | [S8]; **[std]** (3) |
| 보험계약대출 (policy loan) | **Not available during the 납입기간** on the 미지급형 form, because there is no surrender value to lend against; 「순수보장성보험 등 보험상품의 종류에 따라 보험계약대출이 제한될 수도 있습니다」 | [S3]; [REG-R25 제33조](#krlib-reg-r25); [REG-R28] |
| Automatic premium loan | **None.** There is no cash value to advance the premium from, so a missed premium lapses the contract at the end of 납입최고 | [S3]; [REG-R28]; **[std]** (29) |
| 납입최고 (grace) | **At least 14 days** from the demand, the contract terminating the day after it expires | [S1]; [REG-R25 제26조](#krlib-reg-r25) |
| Lapse (해지) | From the day after the 납입최고기간 expires | [S1]; [REG-R25 제26조](#krlib-reg-r25) |
| Reinstatement (부활) | Within **3 years** of termination where the surrender value has not been drawn — **including where there is none**, which is the 무해지 case; arrears with interest at a rate within 평균공시이율 + 1%; underwriting may refuse or restrict; **the 90-day 암보장개시일 restarts from the 부활일** | [S1]; [REG-R25 제27조](#krlib-reg-r25); [S3] [S7]; **[std]** (31) |
| First-premium failure | The insurer's liability never attaches: 상법 제656조 starts cover on receipt of the first premium absent other agreement, and 제650조제1항 voids the contract two months after formation | [REG-R49]; [R7] |
| Non-disclosure (계약 전 알릴 의무) | Termination within **1 month** of the insurer learning of the breach and **3 years** of formation (상법 제651조), narrowed by the 약관 to **2 years from the 보장개시일 with no claim event** — one year for disease in a 진단계약 — with a causation defence | [REG-R49]; [REG-R25 제13조·제14조](#krlib-reg-r25); [S6] [S7] |
| Fraud (사기에 의한 계약) | Voidable within **5 years of the 보장개시일** and one month of discovery; concealment of a pre-application cancer diagnosis is named in the 표준약관 as an instance | [REG-R25 제15조](#krlib-reg-r25); [S6] [S7] |
| 청약철회 (cooling-off) | **15 days** from receipt of the 보험증권 or **30 days** from the application, whichever comes first; effective on despatch; premiums returned within 3 business days | [REG-R51]; [REG-R25 제17조](#krlib-reg-r25); out of scope for the model |
| 품질보증해지 | Cancellation within **3 months** of formation where the 약관 was not delivered, its important content not explained, or the application not signed | [REG-R49 제638조의3](#krlib-reg-r49); [REG-R25 제18조제3항](#krlib-reg-r25); [S3] |
| Benefit claim prescription (소멸시효) | **3 years** on a benefit claim and on a premium or 적립금 refund claim; 2 years on a premium claim | [REG-R49 제662조](#krlib-reg-r49); [REG-R25 제37조](#krlib-reg-r25) |
| Late-payment interest on benefits | 보험계약대출이율 for the first 30 days after the due date, **+4.0%** to day 60, **+6.0%** to day 90 and **+8.0%** thereafter | [S6] [S7] |
| Policyholder protection | 예금자보호법 cover of **₩100,000,000** per person per insurer, applied to 보험금 claims in a bucket that expressly **excludes** benefits payable because the term has ended | [REG-R52]; [REG-R25 제43조](#krlib-reg-r25) |
| Expiry | At the **100세 계약해당일**; nothing is paid | [S4] [S7]; **[std]** (3) |

29. **The 무해지 form is the base, and on this product it is worth less than it looks.** The
    wording is exact: 「② 회사는 **해약환급금 미지급형(납입기간중 0%, 납입기간후 50%)** 계약이
    보험료 납입기간 중 해지될 경우 해약환급금을 지급하지 않으며, 보험료 납입기간이 경과된 이후
    해지될 경우 '표준형' 해약환급금의 **50%**에 해당하는 금액을 지급합니다. 다만, 보험료 납입이
    면제된 이후 … 해지할 경우에는 해약환급금을 지급하지 않으며, … **전기납 계약**의 경우에는 …
    해약환급금을 지급하지 않습니다」 [S3 제41조]. It is the base because that is where the
    market is: the 무·저해지 share of 보장성 초회보험료 ran **11.4% (2018) → 30.4% (2021) →
    47.0% (2023) → 63.8% (2024 H1)** [REG-R27], so a library modelling only 표준형 products
    models a minority of the market. Three consequences follow. The profile is a **cliff at a
    known date**, because 「보험료 납입기간 중이라 함은 계약일로부터 보험료 납입기간이 경과하여
    최초로 도래하는 계약해당일 전일까지의 기간」, with the 약관's own example 계약일
    2018-09-01, 20년납 ⇒ to 2038-08-31 [S3]. The lapse decrement has **no cash-value offset and
    nothing to delay it** — no policy loan during the payment period [REG-R28], no automatic
    premium loan — so a missed premium lapses at the end of the 14-day 납입최고. And **the
    suppressed form's pricing uses a lapse assumption while the comparator does not**:
    「'표준형'의 해약환급금은 … **해지율을 적용하지 않고** 계산합니다」 [S3], the clearest
    retrieved statement of why the assumption is a supervisory issue [REG-R27]. **The caveat**:
    on a 순수보장성 cancer contract there is barely any 계약자적립액 to suppress. The one
    retrieved illustration, 남자 40세 / 월납 / 10년납 10년만기, shows 환급률 of 0.0% (year 1),
    11.3% (3), **21.6% (5)**, 20.5% (7) and **0.0% at maturity** on its cheapest plan and 4.5%
    / 13.7% / 13.9% / 0.0% on its richest [S8]. The value **peaks at years 5–7 and returns to
    nil**, a pure-protection signature rather than a savings one, and the **환급률 falls as the
    plan gets richer**, which is what a fixed 해약공제액 does when spread over a larger
    premium. So the 무해지 form removes a small number here where on `WholeLife_KR_S` it
    removes a large one, and the 환급률 cap of 제7-66조제4항제2호 — which requires the
    post-payment 환급률 to exceed 100% — binds **weakly** on a product whose 표준형 환급률
    never approaches 100% at any duration [S8] [REG-R19]. How the exact-50% wording of [S3] and
    the "must exceed 50%" wording of 제7-66조제4항제2호가목 interact was not resolvable from
    the retrieved documents and is [unverified].
30. **The 표준해약공제액, computed for this product.** [별표 14] states the cap as a formula
    and every input comes from a different note [REG-R20]:

        표준해약공제액 = 연납순보험료 × 5% × 해약공제계수 + 보험가입금액 × 10/1000

    **해약공제계수** for a 보장성보험 is 「보험기간(최대 20년)」, so **20** on a 60-year term
    (note 2). **연납순보험료** is recomputed 「전기납(단, 보험기간이 20년 이상인 경우
    20년납)」, i.e. on the composite's own 20년납 basis (note 3). **보험가입금액** is where the
    Korea-specific mechanic bites, because the product has no death benefit at all: [별표 15]
    제3호 covers only 일반사망을 보장하는 보장성보험, so this product falls into **제9호** —
    보험가입금액 = (위험보험료 ÷ 정기보험의 위험보험료) × 정기보험의 보험가입금액 — computed at
    the **기준연령 요건**, 남자 만 40세, 전기납, 월납, which is the anchor cell of this
    specification [REG-R21] [REG-R9]. **The ₩30,000,000 headline is therefore not the
    보험가입금액 that enters 별표 14.** Two cross-checks bound the result: 제7-66조제1항제2호
    caps the **해약공제기간** at seven years [REG-R19], and the FSC's 2019 reform states the
    same cap as **13 months' premium for a 보장성보험** [REG-R29] — ₩585,000 at the anchor
    cell. Working backwards, at ₩540,000 a year and a loading near 25% the first term is about
    ₩405,000, leaving about ₩180,000 for the second and hence a notional 보험가입금액 near
    **₩18,000,000**, roughly 60% of the diagnosis benefit — a plausible order for a benefit
    paid once on a morbidity trigger rather than on death. That reconciliation is illustrative
    and **[std]**; `technical-notes.md` performs it on the shipped basis and its figures
    govern. The mechanic is stated in full because it is the route by which a Korean 제3보험
    product with no face amount acquires one, and `LTC_KR_S` and `Child_KR_S` inherit it — with
    the difference that 제9호's third bullet **excludes long-term-care risk premium** from the
    ratio [REG-R21].
31. **부활.** Within **3 years** of termination where the surrender value has not been drawn,
    **including where there is none** — the 무해지 case — on arrears with interest within
    **평균공시이율 + 1%**, a ceiling of 3.50% at the 2026 rate [REG-R25] [REG-R48]. The insurer
    may refuse or restrict on health grounds [S1] but may **not** refuse because a claim event
    occurred before termination [REG-R25]. What makes it more than a persistency detail is
    footnote (17): **the 90-day 암보장개시일 re-runs from the 부활일** [S1] [S3] [S7], and
    cover for events between lapse and reinstatement is never restored [S1]. `Cancer_KR_S` does
    not model reinstatement and treats lapse as absorbing — the conservative direction, stated
    as a [std] simplification in `technical-notes.md`.

---

## Contractual mechanics

Throughout, `t` is the number of complete months since the 보험계약일, `S` is the 보험가입금액
(₩30,000,000 at the anchor cell), and the 보험계약일 is the day the first premium is received
[S1].

### Premium provisions

The premium is **level** for the whole 납입기간 and does not vary with the policy year, the
claim history or the insurer's experience: the contract is 무배당, so there is no dividend and
no premium review [S1] [S3] [S8] [REG-R12]. It is payable **monthly in advance** from the
보험계약일, including through the 90-day waiting period, because the 유사암 tier and every
non-cancer cover are already in force from day 1 and because the invalidity rule returns the
premium for the affected cover if it bites. Premium ceases on the earliest of 납입완료 at
`t = 240`, death, lapse, and the operation of the premium waiver.

Non-payment of the second or a later premium opens a 납입최고 of **at least 14 days**, at the
end of which the contract terminates the following day [S1] [REG-R25 제26조](#krlib-reg-r25). Nothing breaks
the fall: the 미지급형 form has no surrender value during the 납입기간, so there is no
보험계약대출 to draw on and no automatic premium loan [S3] [REG-R25 제33조](#krlib-reg-r25) [REG-R28].
Non-payment of the **first** premium is different in kind — liability never attaches, because
상법 제656조 starts cover on receipt of the first premium absent other agreement and
제650조제1항 voids the contract two months after formation [REG-R49] [R7] — so it produces no
in-force policy rather than a lapse decrement.

Pricing is by **현금흐름방식**: 감독규정 제7-64조제1호 requires, for any contract longer than
three years, a premium calculation with an adequacy analysis on **최적기초율** and projected
cash flows [REG-R18]. That is what this library computes, and what the institute called for —
「새롭게 도입된 보험료 산출 방식인 현금흐름 방식하에서, 다양한 리스크에 대한 정확한 분석과
함께 합리적인 현금흐름 가정을 사용한 보험료가 산출되어야 할 것임」 [R4].

### 암보장개시일 — the 90-day 면책기간

Write `d0` for the 보험계약일. Cover for invasive cancer attaches on

    암보장개시일 = d0 + 90 days      (the day after 90 days counting d0 as day 1)

which on a monthly grid is the boundary **`t = 3`**. The composite's benefit vector therefore
has **two start dates**, not one:

    유사암 tier                    : in force from t = 0
    일반암 / 특정소액암 / 고액암   : in force from t = 3

and, on a life aged under 보험나이 15 at issue, or on any 갱신계약, both are `t = 0` [S2] [S4]
[S7]. On 부활 the invasive-cover date is recomputed from the 부활일 and the 유사암 date is not
[S1] [S3] [S7]. The 90 days is a **market convention**, not a statutory or 표준약관 requirement
(footnote 16). Its purpose is stated by the institute: 「보험 가입 전에 이미 암이 발생하였거나
암이 의심되는 사람이 보험금을 받을 목적으로 보험에 가입하는 것을 방지하기 위한 것이다 … 특히
암보험의 경우 고액의 보험금이 지급되므로 사행성이 크다는 점에서 **도덕적 해이에 의한 역선택
방지**를 위해서도 일정 기간의 부담보기간을 두기로 한 것」 [R3].

### Diagnosis inside the waiting period — 무효, not merely unpaid

A diagnosis of an invasive cancer at `t < 3` does not simply go unpaid:

    the 일반암 / 특정소액암 / 고액암 cover is 무효 from inception
    its premiums are returned
    the 유사암 tier and every other cover survive
    the policyholder may cancel the survivors within 90 days of the 진단확정일

[S1 제28조제2항·제3항] [S2] [S3]. Where the insurer was at fault, or knew of the invalidity and
did not refund, the returned premiums carry interest at the **보험계약대출이율** compounded
annually [S1] [S3]. The statutory hook is 상법 제644조 [R7], and the rule reaches forward as
well as back: a cancer diagnosed before the 암보장개시일 that later recurs or metastasises does
not trigger the premium waiver either [S1 제9조제2항].

**For a projection this is a de-recognition, not a decrement.** The cover was never in force,
so it releases premium already collected as well as future benefit, and it belongs in a
validity adjustment at outset rather than in the lapse column. The model applies it as a
scaling of the invasive-cover limb at `t = 0`; the composite adopts **no** outer time limit on
the rule, because no retrieved Korean contract states one.

### 감액기간 — the reduced-benefit period

For a diagnosis whose 진단확정일 falls in the first year,

    benefit = 0.50 x (the amount that would be paid after the 감액기간)

on **every** diagnosis tier [S1] [S6] [R6]. On the monthly grid the boundary is `t = 12`, and
`reduction_months` is a model parameter whose observed values are 0, 12 and 24 (footnote 19).

The clock's two endpoints differ by benefit type, which is a real modelling distinction.
**Diagnosis benefits** — 「지급금액의 경과기간은 **보험계약일부터 진단 확정일까지**의
경과기간입니다」 [S3 별표 1 주2]. **Surgery and treatment benefits** — 「지급금액의 경과기간은
보험계약일부터 **수술일**까지의 경과기간을 말합니다」 [S4] [S5]. A cancer diagnosed at month 10
and operated on at month 14 therefore pays a reduced diagnosis benefit and a full surgery
benefit.

The 감액 **does not apply on a 갱신계약** — 「※ 갱신계약의 경우 감액지급을 적용하지 않습니다」
[S2] [S4], and the same at two more carriers [S6] [S7]. It cannot be modelled as a permanent
benefit scaling: it is a first-year phenomenon, and on the 갱신형 flag a
first-year-of-the-first-term one.

### What "cancer" means — the KCD chassis and the tier ladder

Korean cancer policies **do not define cancer clinically**. They incorporate a public
statistical classification by reference and then list the codes in an annex: 「약관 본문에서
"암이라 함은 제[ ]차 한국표준질병·사인분류에 있어서 별표[ ]에서 정한 질병을 말한다"라고
정의하고, 약관 별표에서 악성 신생물 분류표를 제시하여 그 대상이 되는 악성 신생물의 종류와
분류번호를 열거하고 있다」 [R3]. The classification is the **한국표준질병·사인분류**, published
by 통계청 on the WHO ICD framework; the composite uses the **제8차**, 통계청 고시 제2020-175호,
시행 2021-01-01 [S3] [S4] [R10].

The mechanism that decides the tier is the **행동양식 분류번호**, the fifth digit of the ICD-O
morphology code [R3]:

| 행동양식 | meaning | KCD 제2장 항목 |
|---|---|---|
| `/0` | 양성 신생물 | D10–D36 |
| `/1` | 불확실한 또는 알려지지 않은 성격의 신생물 | D37–D48 |
| `/2` | 제자리신생물 | D00–D09 |
| `/3` | 일차성 악성 신생물 | C00–C76, C80–C97, D45, D46, D47.1, D47.3, D47.4, D47.5 |
| `/6` | 이차성 악성 신생물 | C77–C79 |

「즉, 행동양식 분류번호가 "/3"인 경우에 암(악성종양)에 해당하는 것이며, "/1"인 경우에는
경계성종양, "/2"인 경우에는 제자리암에 해당한다고 이해하면 될 것이다」 [R3]. The retrieved 악성
신생물 분류표 runs C00–C97 by block plus the five myeloid D-codes D45, D46, D47.1, D47.3, D47.4
and D47.5 [S3]. Two features of it matter: **C44 and C73 are inside the annex and then carved
back out by the definition article**, and the five D-codes are inside it, so a handful of
`/1`-behaviour myeloid neoplasms are treated as 암 rather than as 경계성종양 [S3].

The composite's four diagnosis tiers:

    고액암 (특정 고액치료비관련암)  C40-C41, C70-C72, C91-C95 + D47.1 + D47.5      +100% of S
    일반암                          the 악성신생물 분류표 less C44, C73,            100% of S
                                    대장점막내암, 전암상태 and the 특정소액암 sites
    특정소액암                      직·결장암, 유방암 (C50), 여성생식기암,           60% of S
                                    전립선암 (C61)
    유사암                          기타피부암 (C44), 갑상선암 (C73),                20% of S
                                    대장점막내암, 제자리암 (D00-D09 less
                                    대장점막내암), 경계성종양 (D37-D48)

each tier payable **최초 1회한** and each 유사암 member once in its own right [S3] [S4].
기타피부암 and 갑상선암 are pure code definitions (C44, C73), 제자리암 is D00–D09 less
대장점막내암, and 경계성종양 is D37–D48 [S1] [S3]. **대장점막내암 is a defined clinical depth,
not a code**, and it is the only tier member that is: 「대장의 상피세포층(epithelium)에서
발생한 악성종양세포가 기저막(basement membrane)을 뚫고 내려가서 점막고유층(lamina propria) 또는
점막근층(muscularis mucosa)을 침범하였으나 **점막하층(submucosa)까지는 침범하지 않은** 상태의
질병」 [S1] [S2]. That is why it can be carved out of 제자리암 without disturbing the D00–D09
annex, and why its incidence cannot be sourced: the registry files it inside 대장 D010–D012 and
does not identify it separately [R1]. **전암(前癌)상태** — «Premalignant condition or condition
with malignant potential» — is excluded by name in every retrieved cancer definition [S1] [S2]
[S3] [S4] [S5]. 유사암 membership is four members [S6] [S7] [S9] or five [S1] [S2] [S3]; the
composite takes **five**, because a contract that carves 대장점막내암 out of 제자리암 without
giving it a tier leaves it unclassified.

### 진단확정 — who may diagnose, on what evidence, and on what date

The wording is stable across every retrieved contract and is the market form the institute
records [R3]:

> 암의 진단 확정은 **병리과 또는 진단검사의학과 전문의** 자격증을 가진 자에 의하여 내려져야
> 하며, 이 진단은 **조직(Fixed Tissue) 검사, 미세바늘흡인(Fine Needle Aspiration) 검사 또는
> 혈액(Hemic System) 검사에 대한 현미경 소견**을 기초로 하여야 합니다. 그러나 상기에 따른
> 진단이 가능하지 않을 때에는 피보험자가 암으로 진단 또는 치료를 받고 있음을 증명할 만한
> 문서화된 기록 또는 증거가 있어야 합니다.

The newer contracts add two refinements. The **date**: 「이 경우 …의 진단확정 시점은 **상기
검사에 의한 결과보고 시점**으로 합니다」 [S2] [S3] [S4] — the pathology report, not the
certificate — and a carrier tells consumers why: 「암 진단 시점은 진단서 발급일이 아닌 '조직
검사 결과 보고일'이므로 암 진단 일이 면책 기간이나 감액 기간에 해당하는지도 확인하세요」 [S10].
**The date of diagnosis is the variable that decides whether a claim falls inside the 면책기간,
inside the 감액기간, or outside both**, and it is fixed by the laboratory rather than by the
clinician. The **fallback** opens where 「조직검사 등 병리학적 검사를 받을 여유없이 급속한 병증
악화로 사망한 경우」 or where extracting tissue would itself endanger life, with a 사체검안서
excluded from the acceptable record [S3] [S4]; the older wording accepted 「임상학적인 진단」
far more readily and was tightened [R3].

Every contract carries a **third-opinion procedure at the insurer's entire expense**, the third
party chosen from 의료법 제3조's **종합병원 소속 전문의** [S1] [S2] [S3]. And where the insured
dies in the term and the cancer is only then established as the direct cause, 「그 사망일을
진단 확정일로 보고」 the benefit is paid, less any 계약자적립액 already paid out [S1] [S3]
[S4].

### 원발부위 기준 — C77–C80, and the 2011 change that set the pricing basis

A primary cancer that has spread picks up a **secondary-site code** as well as its own. If the
primary is a reduced-tier cancer (C73) and the secondary code is a general-tier one (C77
림프절의 이차성 및 상세불명의 악성 신생물), which tier pays? 「특히 갑상선암이 인접 부위
림프절에 전이된 경우에 대한 분쟁이 다수 발생하였다」 [R3].

The 금융감독원 분쟁조정위원회 sided with the **primary site**. In 제2014-12호 the stake was
갑상선암 진단비 **₩3,000,000** against 일반암 진단비 **₩30,000,000**; on advice from
대한갑상선학회 and 대한병리학회 the committee held that C77 「원발암 수술 시에 동시에 발견된
주변 림프절 전이의 경우에 사용하는 코드가 아니며 … C73 단일 코드로 진단하는 것이 표준」, that
dual coding shows 「갑상선암의 '진행 상태'」 rather than two cancers, and that 중앙암등록본부's
own registration counts such a case as one cancer [R3]. The courts split, some for the primary
site and some for the general tier on the contra proferentem ground, and **no Supreme Court
decision on the point existed as at the report's date** [R3].

The supervisor closed the question prospectively. 금융감독원 보도자료 2011-03-14 required
「이차성 암에 대한 보험금 지급기준 합리화」 to be written into 약관 **from 2011-04-01**: where
the primary site is identifiable the primary decides the benefit, **and the risk rate must be
set accordingly** — 「예를 들어 갑상선의 악성 신생물(C73)과 림프절의 이차성 및 상세불명의 악성
신생물(C77) 중 갑상선을 원발부위로 하는 경우를 갑상선암에 모두 포함한 위험률을 적용하라는
것임」 [R3]. **That is a direct instruction about the pricing basis, and it is why a Korean
일반암 incidence rate is the rate for cancer excluding C44 and C73 *by primary site*** — which
is exactly the table the rate bureau publishes [R5] and the basis the registry's
excluding-thyroid row gives [R1].

The clause is in every retrieved contract, the newer generation adding a timing rider and three
worked examples: 「…다만, 이 경우에도 C77~C80…의 **진단확정 시점은 원발암 진단확정 시점으로
변경되지 않습니다**. 【원발부위 기준 예시】 · C73이 림프절로 전이되어 C77…로 진단된 경우에도
C73…에 해당하는 질병으로 봅니다. · C50이 폐로 전이되어 C78.0…로 진단된 경우에도 C50…에 해당하는
질병으로 봅니다. · C16이 뇌로 전이되어 C79.3…로 진단된 경우에도 C16…에 해당하는 질병으로
봅니다」 [S3] [S4] [S5]. The composite adopts that form. The 2026 non-life edition adds a
carve-out — the timing rule does not hold 「원발부위의 암이 완치되었다면」 [S2] — which the
composite does not adopt, because "완치" is undefined there and the only contractual definition
of cure retrieved anywhere is the five-year rule of the renewal waiver [S4]. Underwriting
exclusions follow the primary too: where a 특정부위 부담보 특약 excluded the thyroid and a
thyroid cancer spread to nodes coded C77 there was no liability, a metastasis not being a
합병증 (제2006-71호) [R3].

### The diagnosis benefits

Let `r(tier)` be 2.00 / 1.00 / 0.60 / 0.20 for 고액암 / 일반암 / 특정소액암 / 유사암, and let
`g(t) = 0.50` for `t < 12` and `1.00` thereafter. On the first diagnosis in a tier on or after
that tier's 보장개시일,

    diagnosis benefit = g(t) x r(tier) x S      each tier once,
                                                each 유사암 member once

with the 고액암 amount **added to** the 일반암 amount rather than replacing it, and neither
paid twice: 「보험기간 중 이미 암진단자금을 지급한 이후 특정 고액치료비관련 암진단자금의
지급사유가 발생한 경우에는 암진단자금을 다시 지급하지 않습니다」 [S3]. The model therefore
carries **four once-only flags and five 유사암 member flags**, not one.

Payment **does not terminate the contract and does not exhaust it**: cover for the other
tiers, for the event benefits and for the premium waiver runs on to the 100세 계약해당일 [S1]
[S3] [S4]. A cancer contract on this chassis cannot pay itself out of existence, which is the
sharpest structural contrast with the accelerated design of `CI_KR_S`, where the
critical-illness payment reduces the death benefit that carries it.

### The inpatient benefit

    inpatient benefit(stay) = D x min(days(stay), 180)      D = 50,000
                              x 0.20 if the stay is for a 유사암

for each stay whose **direct purpose** is cancer treatment [S1] [S4] [R3]. Two or more
admissions for the same cancer are grouped into one stay and their days summed; a stay
beginning more than **180 days** after the discharge that ended a paid stay is a new stay [R3].
Days at a **요양병원** are excluded and fall to the separate 90-day rider [S2] [S8].

That exclusion is not fastidiousness. 「암 환자가 암치료를 받은 후 **요양병원**에 입원한 경우에
이것이 '암의 치료를 직접적인 목적으로 하여 입원을 한 경우'에 해당하는지에 대해 소비자와
보험회사 사이에서 다툼이 발생」, and 금융감독원 received **2,125 complaints about 암입원비 in
2018**, enough to be a principal driver of the year's rise in life-insurer complaints [R3]. The
market's answer was structural — two riders, two prices, and the convalescent-hospital limb
much more tightly capped [S2] [S8] — and the composite copies it.

### The surgery benefit

    surgery benefit = 5,000,000  per 관혈 operation
                    = 1,000,000  per 비관혈 operation        unlimited count

with the **관혈** amount alone paid where both are performed in one operation [S1] [S4]. The
5 : 1 split is read directly from a module schedule at 보험가입금액 500만원 [S4]. 「'관혈수술'
이라 함은 …병변 부위를 육안으로 직접 보면서 수술적 조작을 하기 위해 피부에 절개를 가하고 병변
부위를 노출시켜서 수술을 하는 것」, and 「대뇌내시경, 흉강경수술, 복강경수술 및 조혈모세포이식
수술은 **관혈수술에 준합니다**」 [S4]. What counts as 수술 is a 수술분류표 plus a general
clause, and the exclusion list is the operative part:

> '수술'은 기구를 사용해서 생체에 절단, 절제 등의 조작을 가하는 것(보건복지부 산하
> **신의료기술평가위원회**로부터 안전성과 치료효과를 인정받은 최신 수술기법도 포함됩니다)을
> 말합니다. 다만, **흡인, 천자 등의 조치 및 신경 BLOCK, 미용 성형상의 수술, 피임 목적의 수술,
> …검사 및 진단을 위한 수술[생검, 복강경 검사 등], 발정술 등 내고정물제거술은 '수술'에서
> 제외**합니다. [S4]

The institute describes the same list as the market norm and adds 항암방사선치료 and
항암약물치료 to the exclusions [R3] — they are covered separately, and a model that paid both
would double-count.

### The anti-cancer treatment benefit

    treatment benefit = 10,000,000   on the first qualifying treatment, once ever
                      x 0.20         if the underlying cancer is a 유사암

This is a **treatment-event benefit, not a per-cycle or per-month benefit**: 「(단, 최초
1회한)」 [S4] [S5], 「최초 1회한 지급」 [S1]. That is a sharp structural contrast with Japan,
where the chemotherapy benefit is paid per qualifying calendar month against a lifetime month
cap, and it makes the composite's treatment limb a **single indicator on the first treatment
date** rather than a stream. The definitions are anchored to a specialty rather than to a drug
list: 「'항암약물치료'라 함은 … **항암화학요법 또는 항암면역요법**에 의해 항암약물을 투여하여
치료하는 것 … 단, … **암세포가 없는 상태에서 면역력을 증가시키는 약물(압노바, 헬릭소, 셀레나제
등) 치료는 제외**됩니다」, and 「'항암방사선치료'라 함은 **방사선종양학과 전문의** 자격증을
가진 자가 … **고에너지 전리 방사선(Ionizing Radiation)**을 이용하는 치료법」 [S4]. The named
exclusion of 압노바, 헬릭소 and 셀레나제 is the same immune-support therapy that drove the
요양병원 disputes [R3], written into the definition so the argument cannot be had again. The
alternative market design puts the discount in a separate limb rather than in a multiplier —
항암약물치료자금Ⅰ at 1,000만원 against Ⅱ at 250만원, a **4 : 1** ratio [S4] — and the
composite's uniform 20% is the [std] simplification flagged at footnote (24).

### 보험료 납입면제 — the correlated decrement

    on the first diagnosis of a 일반암 or 고액암 on or after the 암보장개시일,
    or on a cumulative 장해지급률 of 50% or more,
        premiums cease for the remainder of the 납입기간

with 특정소액암 and every 유사암 member expressly excluded [S3 제14조제1항] [S1 제9조제1항].
The 장해분류표 the disability limb keys to is 표준약관 부표 3, which defines 장해 as a
**permanent** impairment remaining after treatment and excludes temporary states [REG-R25], so
it is a percentage scale rather than a binary trigger.

**This is a correlated decrement and that is the modelling point.** Unlike the
disability-triggered waiver of a death-benefit product, this waiver fires on the *same event*
that pays the diagnosis benefit, and then runs for as long as the insured survives inside the
납입기간. Its value is therefore the product of an incidence rate and a **post-diagnosis
survival curve**, which is the first of the four reasons the next section exists.

Two rules narrow it. On a 갱신계약 the waiver does **not** carry over — 「보험료 납입이 면제된
이후에 …계약을 갱신하는 경우 보험료 납입은 **더 이상 면제되지 않으며**」 — and a cancer already
waived cannot waive again on the renewed contract 「이미 보험료의 납입을 면제한 질병의
종양세포가 잔존하거나 재발 또는 전이된 경우」 unless **5 years** pass from the renewal's
보장개시일 with no further diagnosis or treatment [S4]. **That five-year rule is the only
clean, dated, contractual definition of "cured" retrieved anywhere in this product line.** And
on one contract the waiver is switched on and off by the **사업방법서** rather than by the 약관
[S2], so its presence cannot be read off the policy conditions alone — a caution about reading
any Korean 약관 as a complete statement of a product.

### The post-diagnosis survival model

The contract goes on paying after the diagnosis benefit, and four limbs depend on how long: the
premium waiver; the inpatient, surgery and treatment benefits, incurred over the months and
years following diagnosis; the 재진단암 rider, whose clock does not open for two years; and the
계약자적립액 payable on a later death from a cause the policy does not cover. An incidence rate
cannot price any of them.

**The public quantity is relative survival, and it is not a mortality table**: 「관찰생존율을
일반인구의 기대생존율로 나누어 구한 값」 [R1]. It is a ratio to an expected general-population
survival, not a cohort curve and not a transition rate, so **every post-diagnosis survival
model in this library is a `[std]` construction**. The composite's is specified so that its
calibration targets can be re-derived from a public document:

| Target | Value | Source |
|---|---|---|
| 5-year relative survival, all cancers, 2019–2023 diagnoses | 73.7% (남 68.2 / 여 79.4) | [R1] |
| 5-year relative survival, **excluding thyroid** — the general-tier target | **69.6%** (남 65.9 / 여 74.0) | [R1] |
| 5-year relative survival, 갑상선 — the 유사암 target | **100.2%** | [R1] |
| Lifetime cancer mortality risk | 19.6% (남 24.2 / 여 15.6); 갑상선 **0.1%** | [R1] |
| Share of prevalent patients more than 5 years from diagnosis | **62.1%** (1,697,799 of 2,732,906) | [R1] |

The construction is a **select excess hazard over the [std] base mortality table**, zero for
the 유사암 tier and graded downward across five select years for the general tier, calibrated
so that the five-year survival ratio equals 0.696. A constant hazard reproducing that target is
−ln(0.696) / 5 = **0.0725 p.a.**; the excess is front-loaded, so the model grades it and leaves
a small non-zero residual after year 5, because 62% of the prevalent population is beyond year
5 and a step to nil would be visibly wrong [R1].

The **stage decomposition** makes the target credible and gives a user a route to a finer
model. By 요약병기 for 2019–2023 diagnoses, 환자분율 / 5-year survival are 국한 46.1 / 92.7,
국소 28.0 / 75.6, 원격 17.8 / 27.8, 모름 8.2 / 60.5 [R1]. Weighting:

    0.461 x 92.7 + 0.280 x 75.6 + 0.178 x 27.8 + 0.082 x 60.5 = 73.8

against the published all-cancer 73.7 [R1] — a tenth of a point, which confirms the two tables
are on the same population. **Survival is a stage story far more than a site story**: 폐 국한
81.5 against 원격 13.9, 위 97.6 against 7.5, 대장 94.9 against 20.4, 췌장 47.8 against 2.4
[R1]. And the stage mix is moving in the policyholder's favour: 국한 45.6% (2005) → 51.0 (2022)
→ **51.8 (2023)**, with 원격 falling 21.3 → 18.8 [R1]. The composite does not model stage; it
records that the target it is calibrated to is drifting, and that the drift raises the cost of
every post-diagnosis limb.

The registry's **elapsed-time prevalence table** is the closest public quantity to a
persistence curve and is quoted with its limitation: ≤1년 258,721; 1년 초과 2년 이하
**224,013**; 2년 초과 5년 이하 552,373; 5년 초과 1,697,799 [R1]. Those are prevalence stocks,
not incidence flows, so they bound rather than determine the model; what they establish is that
the population inside the 감액기간 window and the population waiting out the 재진단암 clock are
both large and both measurable.

### The incidence basis the benefit definitions imply

The benefit definitions above are what a decrement has to match, and the point of this section
is that the match can be **derived from public data** rather than asserted.

**Step 1 — what is needed.** Four annual incidence rates by age and sex: 일반암 (invasive,
excluding C44, C73, 대장점막내암 and the 특정소액암 sites), 특정소액암, 유사암 and the 고액암
top-up.

**Step 2 — the published rate that already matches the insured definition.** 보험개발원
publishes, for public display, its 참조순보험요율 in force **적용시점 2024년 4월 1일 이후** for
장기손해보험, including a 「기타피부암 및 갑상선암 이외의 암 발생률」 table by age and sex
[R5]:

| 연령 | 남자 | 여자 | | 연령 | 남자 | 여자 |
|---|---|---|---|---|---|---|
| 0 | 0.000297 | 0.000318 | | 50 | 0.003567 | 0.004962 |
| 10 | 0.000148 | 0.000152 | | 60 | 0.008540 | 0.006239 |
| 20 | 0.000230 | 0.000250 | | 70 | 0.019206 | 0.008626 |
| 30 | 0.000531 | 0.001005 | | 80 | 0.027892 | 0.011452 |
| 40 | **0.001343** | **0.003382** | | | | |

It is dated, it has a stated effective date, and **its definition is the insured one** —
invasive cancer excluding C44 and C73, by primary site — so it already embodies the tier
carve-out and the 원발부위 rule. Its sex crossover falls at about age 55–60, matching the
registry's own 「50대 후반부터」 statement [R1] [R5]. Read it beside the cross-product
finding it qualifies: what [REG-R34] establishes is that **no life-side 참조순보험요율 value
reaches the public**, and it records expressly that the **장기손해보험** rates are published
as a numeric display on a different page of the same site [REG-R61]. What is public is this
display on a ten-year age grid, not the filed table.

**Step 3 — reconcile it against the registry, for men.** [R1] gives all-site crude incidence by
ten-year band and, separately, the male thyroid rate in the two bands either side of 40:

    male 30-39  all sites  143.4 per 100,000 ; 갑상선  62.9  =>  excl. C73   80.5
    male 40-49  all sites  243.0 per 100,000 ; 갑상선  60.7  =>  excl. C73  182.3

Interpolating linearly on band midpoints 34.5 and 44.5 to exact age 40 gives 80.5 + (182.3 −
80.5) × 5.5 / 10 = **136.5 per 100,000 = 0.001365**, against the bureau's published
**0.001343** — a difference of **+1.6%** [R1] [R5]. The residual has the right sign: C44 could
not be deducted, because 기타피부암 does not appear in the registry's top-ten site table, so
the registry-derived figure is biased upward by exactly the quantity that is missing. **A
published net premium rate and an independently derived crude rate agree to within two per
cent**, which is what licenses the model to use the registry for the tiers the bureau does not
publish.

**Step 4 — invert the same reconciliation for women, where the thyroid rate is not published.**
[R1] gives female all-site crude 321.2 (30–39) and 590.0 (40–49); interpolating to age 40 gives
469.0 per 100,000. The bureau's female rate at 40 is 338.2, so the implied C73-plus-C44
deduction at that age is 130.8 per 100,000 — **27.9% of all-site incidence** [R1] [R5]. That is
consistent with what the registry does publish: female thyroid crude incidence at 30–39 is
**164.3** per 100,000, 51.2% of the female all-site rate in that band, and 갑상선 is the rank-1
female site to age 39 while 유방 takes rank 1 from 40 [R1]. A thyroid share falling from about
half to about a quarter across the fortieth birthday is what that ranking implies. **The
thyroid tier is overwhelmingly a young-female exposure, which is precisely why it was moved out
of the general tier.**

**Step 5 — size the tiers against each other.** On all-ages crude rates for 2023 [R1]:

    all sites                          564.3
    less 갑상선 (C73)                  -69.3   => 495.0  (the registry's own published row)
    less 대장 63.8, 유방 58.4,
         전립선 44.3  (특정소액암)     -166.5  => 328.5  = the 일반암 tier, approximately
    상피내암 (D00-D09)                  74.7
    plus 갑상선                         69.3   => 144.0  = the 유사암 tier, at least

Applying the composite's tier ratios gives relative expected cost per unit of 보험가입금액 —
일반암 328.5 × 1.00 = 328.5, 특정소액암 166.5 × 0.60 = 99.9, 유사암 144.0 × 0.20 = 28.8, on a
total of 457.2 — so the reduced tier is **22.5% of diagnosis events and 6.3% of diagnosis
cost**. Repricing it at the pre-2022 ratio of 70% [S8] gives 100.8 on a total of 529.2, at
which it is **19.0%** of cost. **The reported August 2022 supervisory intervention therefore
cut the reduced tier's share of the diagnosis-benefit cost from about a fifth to about a
sixteenth** [R12] — the quantitative content of a change otherwise reported only in the trade
press.

**Step 6 — the caveats, none of which is optional.** The Step 5 figures are **all-ages crude**
and the tiers' age mixes differ sharply, thyroid and in-situ being young-skewed and general
cancer old-skewed; `technical-notes.md` computes them by age. **경계성종양 (D37–D48) is not
covered by the cancer registry at all**, which files malignant and in-situ only, and
**대장점막내암 sits inside 대장 D010–D012 and is not separately identified** [R1] — both are
`[std]` and both make the 유사암 figure a floor, as does the absence of a separate 여성생식기암
row from the 특정소액암 figure. The **고액암** tier's own incidence is not in the retrieved
top-ten table [R1] and is a `[std]` construction at the point of use. And the in-situ increment
as a whole is **13.2%** of the invasive count in 2023 (38,204 against 288,613) but **8.1%** of
male invasive cases against **18.9%** of female [R1]: it must not be assumed age-invariant, and
the registry does not publish in-situ by age band.

**Step 7 — the trend, which is where the risk is.** The in-situ age-standardised rate rose from
**9.0 to 71.3** per 100,000 between 1999 and 2023 — a factor of **7.9** — while the invasive
standardised rate rose by a factor of **1.30**; male in-situ standardised incidence rose from
1.2 to 46.7, a factor of **39** [R1]. The reduced tier is exposed to a decrement growing at a
wholly different rate from the one the main tier is exposed to, and the pricing basis contains
no allowance for it: 「암 발생률이 지속적으로 상승하고 있는데 반해, **예정위험률 산출 시 이를
반영하지 못함**에 따라 추세리스크가 존재」, and 「**현재도 예정위험률 산출 시 미래의 추세를
반영하지 않고 있음**」 [R4]. The institute's verdict is explicit — 「현행 안전할증 수준으로는
충분하지 않으며 … 일본의 경우 안전할증 설정 시 **수준리스크, 추세리스크 등을 모두 반영**하여
산출함」 [R4] — and the market's own mitigations are the two devices this product is built
from: 소액화 of the fast-growing sites, which [R4] claims slows the effective growth rate to
「연 2% 수준」, and 10- or 15-year 갱신형 design [R4].

**Step 8 — what the bureau's rate is and is not.** It is a **참조순보험요율**, a net premium
rate with a safety loading already inside it, not a best estimate [REG-R4] [REG-R9
제1-2조제1호](#krlib-reg-r9). The claim that the loading is about 10% was seen only in a search summary and is
[unverified]; what *is* sourced is that it contains **no trend allowance** [R4]. An insurer
need not use it — applying it merely deems the 순보험료 to have been filed under 보험업법
제176조제6항 [REG-R4]. What the composite ships is nevertheless **that published grid
itself**: `incidence_table.csv` reproduces [R5] [REG-R61] verbatim for ages 0–80, with a
`provenance` column on every row naming it, and only the two rows per sex above the
published age-80 endpoint are a **[std]** extrapolation. It is presented for exactly what
it is — a dated 참조순보험요율 display, not a best estimate and not the 경험생명표
[REG-R33] [REG-R34] — and the [std] work on top of it is Step 5's tier decomposition and
the best-estimate adjustment `inc_be_factor`, both of which are marked at the point of use.

### The renewal machinery — what the 갱신형 flag does

Setting the flag replaces the single 60-year contract with a chain of 10-year contracts, and
six things change [S4 제2-11조의6]: **silence renews**, objection being required 「보험기간
만료일 15일전까지」; **the chain ends at the 100세 계약해당일**; **the premium is re-rated at
the attained age** on the rate basis then in force, with the change and the history of past
renewal premiums notified 30 days before expiry; **the 보험가입금액 does not change**; **a
module that has paid its once-only benefit does not renew** — 「보험금이 지급된 세부보장은
**갱신되지 않으며**」; and **the 면책기간, the 감액기간 and the premium waiver all reset off**,
with no fresh 90 days, no 감액, and no second waiver for the same cancer inside five years [S2]
[S4] [S6] [S7].

The institute's assessment of *why* the market went renewable is the most useful sentence in
the research file for a modeller: 「현재의 안전할증 수준에서는 **갱신형으로 상품을 설계하지
않는 한 추세리스크는 항상 존재함**. 갱신형으로 개발할 경우 고연령층으로 갈수록 보험료의 급격한
상승이 예상되며 이로 인해서 계약자들의 보험갱신이 어려워지는 문제점이 있음」 [R4]. The flag
converts a trend-risk exposure into a lapse-risk exposure, and the contract-boundary question —
whether the renewals are inside the contract at all — is a K-IFRS 1117 question the model does
not answer [REG-R60]. The non-life variant is **재가입**: a 15-year term with re-entry into the
insurer's then-current product, guaranteeing on refusal a contract with the same 보험가입금액
and 보장내용 at a repriced premium [S1] [S2] — the structure `Medical_KR_S` runs on a five-year
cycle.

### 계약자적립액, 해약환급금 and the 표준해약공제액

Three quantities have to be distinguished and Korean regulation keeps them apart deliberately.

**The 계약자적립액** is the account the 산출방법서 defines [REG-R18 제7-65조제1항](#krlib-reg-r18), accruing
**monthly before 납입완료 and daily afterwards** [REG-R19 제7-66조제1항제4호](#krlib-reg-r19) and permitted to
be computed on an **annualised premium** basis [REG-R18 제7-65조제2항](#krlib-reg-r18) — the provision that
lets a monthly-grid model carry an annual account recursion. On the composite it is credited at
the 예정이율 of 2.50% (footnote 12).

**It is paid on death**, and that is a design requirement rather than a courtesy. 감독규정
제7-63조제1항제1호 requires a 제3보험 product to be designed so that on **death from a cause
the policy does not cover** the 계약자적립액 and the 미경과보험료 of 제7-66조제5항 are paid and
the contract terminates [REG-R17]; the 표준약관 implements it — 「…회사가 적립한 **사망 당시의
계약자적립액**」 [REG-R25 제22조](#krlib-reg-r25) — and 상법 제736조 is the statutory floor beneath it
[REG-R50]. The life 약관 say it in one line: 「피보험자가 보험기간 중 사망한 경우에는
계약자에게 사망 당시의 **계약자적립액**을 지급하여 드리고 이 계약은 그 때부터 효력이 없습니다」
[S3 제31조제1항] [S4] [S5] [S6] [S7]. **`Cancer_KR_S` therefore has a payment on death even
though it has no death benefit**, and `LTC_KR_S`, `Child_KR_S` and `Medical_KR_S` inherit the
same requirement.

**The 해약환급금** is a different number:

    해약환급금 = max(계약자적립액 - 해약공제액, 0)                  [REG-R19]
    해약공제액 = 표준해약공제액                                     [REG-R19] [REG-R20]
    해약공제기간 = min(납입기간, 신계약비 부가기간, 7 years)        [REG-R19]

overridden on the **미지급형** form to nil during the 납입기간 and to 50% of the 표준형 value
afterwards [S3]. The 표준해약공제액 is computed at footnote (30), and the point to carry
forward is that its 보험가입금액 input is **not the ₩30,000,000 headline**: a 제3보험 product
with no death benefit takes a *notional* 보험가입금액 from [별표 15] 제9호, by scaling a term
assurance's face amount by the ratio of risk premiums at the 기준연령 요건 [REG-R21] [REG-R9].
On termination the **미경과보험료** is added to whatever is paid [REG-R19 제7-66조제5항](#krlib-reg-r19), and
the insurer must give the policyholder a **table of surrender values by elapsed period** at
issue [REG-R25 제32조제3항](#krlib-reg-r25) — which is why [S8]'s illustration exists at all. None of this is a
solvency quantity: the **해약환급금준비금** of 감독규정 제6-11조의6 is computed
**company-wide** and not contract by contract [REG-R11], `Cancer_KR_S` does not compute it, and
on a 순수보장성 product whose surrender value peaks near 20% of premiums paid [S8] the gap it
quarantines is small.

### Exclusions and 면책

The composite carries **three** grounds on which a claim is not paid, and is honest about the
fourth being missing: the **waiting-period invalidity rule**, under which the affected cover is
void from inception and its premiums returned [S1] [S3] [R7]; **non-disclosure**, below; and
**사기에 의한 계약**, voidable within five years of the 보장개시일 and one month of discovery,
with concealment of a **pre-application cancer diagnosis** named in the 표준약관 as an instance
[REG-R25 제15조](#krlib-reg-r25) [S6] [S7].

The general 보험금을 지급하지 않는 사유 articles were **not read in full** for this product
line and no retrieved document reproduces them [R3]; the statutory floor is 상법 제659조 (the
intention or gross negligence of policyholder, insured or beneficiary) and 제660조 (war and
civil disturbance absent agreement), and 제663조 makes the whole Part one-way mandatory, so no
약관 may vary it against the policyholder [REG-R49]. **Suicide has nothing to attach to**,
because the composite has no death benefit; the clause becomes live only if the 암 사망 rider
is switched on. `technical-notes.md` records this as an [unverified] area and models no
exclusion decrement.

### 고지의무 and 계약 전 알릴 의무

The two names are the same duty: the 표준약관 says so, that the 계약 전 알릴 의무 is 「상법상
'고지의무'와 같습니다」 [REG-R25 제13조](#krlib-reg-r25). The statutory rule is 상법 제651조 — rescission for
intentional or grossly negligent misstatement or omission of a material fact, **within one
month of the insurer learning of it and three years of formation**, and not at all where the
insurer knew or was grossly negligent in not knowing; a matter asked about **in writing is
presumed material**; and 제655조 gives the **causation defence**, so the insurer must still pay
where the non-disclosure is proved not to have affected the event [REG-R49].

The 약관 narrow that window in the policyholder's favour, which 상법 제663조 permits. The
insurer may not terminate where **two years** have passed from the 보장개시일 with no claim
event — **one year** for disease in a 진단계약 — nor where it accepted on a health-examination
document and the claim arises from a matter stated in it, nor where the 보험설계사 prevented
truthful disclosure; and 제14조제5항 bars termination for non-disclosure of **other insurance
held** [REG-R25 제13조·제14조](#krlib-reg-r25). The retrieved contracts carry the two-year form [S6] [S7].
Underwriting may also respond short of rescission, by 보험가입금액 한도 제한, 일부 보장 제외,
보험금 삭감 or 보험료 할증 [S3]. Age and sex misstatement is **corrected, not punished** —
「…신분증에 기재된 나이 또는 성별로 **정정**하고, 정정된 나이 또는 성별에 해당하는 보험금 및
보험료로 변경합니다」 [S3] — the contract being void only where the corrected age falls outside
the product's range, and not even then where 「회사가 나이의 착오를 발견하였을 때 이미
계약나이에 도달한 경우」 [S1].

### 청약철회 and 품질보증해지

Two distinct rights, from two different statutes, and they are often confused. **청약철회** is
the cooling-off right of 금융소비자보호법 제46조제1항제1호: a 일반금융소비자 may withdraw
within 「「상법」 제640조에 따른 보험증권을 받은 날부터 **15일**과 청약을 한 날부터 **30일** 중
먼저 도래하는 기간」, no damages or penalty may be charged, and the withdrawal is ineffective
if a claim event has already occurred unless the policyholder withdrew knowing it had
[REG-R51]. The 표준약관 implements it at 제17조, with three exclusions — an insurer-funded
health examination, a contract of **90 days or less**, and a 전문금융소비자 — effectiveness
**on despatch**, and premiums returned within **3 business days** [REG-R25]. **품질보증해지**
is the 상법 제638조의3제2항 right: where the insurer failed to deliver the 약관 and the
policyholder's copy of the application, or failed to explain the important content, or the
policyholder did not sign, the contract may be cancelled **within three months of formation**
with premiums returned plus 보험계약대출이율 interest [REG-R49] [REG-R25 제18조제3항](#krlib-reg-r25) [S3].
Both are **out of scope for the model**: `Cancer_KR_S` projects from the point cover is in
force.

### 실효 and 부활

Lapse is specified at *Termination and values*. What is peculiar to this product is what
happens on the way back. The 표준약관 permits **부활 within three years** of termination where
the surrender value has not been drawn — including where a policy loan consumed it, and
including where there is none, which is the 무해지 case — on payment of arrears with interest
at a rate within **평균공시이율 + 1%**, and the insurer may **not** refuse because a claim
event occurred before termination [REG-R25 제27조](#krlib-reg-r25). It may refuse or restrict on health
grounds: 「회사는 피보험자의 건강상태, 직업, 직무 등에 따라 승낙여부를 결정하며, 합리적인
사유가 있는 경우 부활을 거절하거나 보장의 일부를 제한할 수 있습니다」 [S1]. Cover for events
between lapse and reinstatement is never restored [S1].

And the 90-day clock re-runs: 「부활(효력회복)일을 포함하여 90일이 지난 날의 다음 날로 합니다」
[S1] [S3] [S7]. **A reinstated cancer policy is not the policy that lapsed** — it is a policy
with 90 days of no invasive-cancer cover in front of it, which is a genuine anti-selection
control and a genuine modelling state. `Cancer_KR_S` does not model reinstatement and treats
lapse as absorbing; the simplification is conservative and is recorded in `technical-notes.md`.

### Expiry

The contract ends at the **100세 계약해당일** and nothing is paid: there is no 만기환급금 on
the 순수보장형 form, and the only retrieved surrender-value illustration shows the value
returning to **nil at maturity** [S8]. 「매년 계약 해당일 — 제2차년도 이후 매년의 계약일과
동일한 월, 일. 다만, 해당 월에 동일한 일이 없는 경우에는 해당 월의 말일」 [S3], so the terminal
date is fixed at issue. On the anchor cell that is `t = 720`.

---

## Riders and options

**In the base contract (modelled):** the four-tier diagnosis benefit with its 최초 1회한
flags; the 암 직접치료 입원급여금 at ₩50,000 a day to 180 days per stay, 요양병원 excluded;
the 암 수술급여금 at ₩5,000,000 관혈 / ₩1,000,000 비관혈; the 항암약물·방사선 치료급여금 at
₩10,000,000 최초 1회한; the 보험료 납입면제 on invasive diagnosis or 장해 50%; and the
계약자적립액 payable on death. Each of the three event modules is **independently switchable**,
so that the diagnosis-only shape of [S3] [S6] [S7] and the treatment-only shape of [S5] are
both configurations of the same model.

**Parameterized switches (specified, off in the base run):** the **10년 갱신형** chassis flag
and its six consequences; **재진단암** on a 2-year cycle, whose rate is a [std] construction
and which is off precisely because of that; the **암 요양병원 입원급여금** at ₩20,000 a day to
90 days; the **암 다빈치로봇 수술급여금** with its 180-day / 1-year two-step 감액; the
**암 사망 및 80% 이상 후유장해** rider, which is the only limb that would make the suicide
clause live; the **표준형** surrender basis against the 미지급형 base; the **비흡연체형** rate
class; and `reduction_months` at 0, 12 or 24.

**Out of scope, and named rather than dropped**, because each is a real benefit some Korean
policyholder actually holds: the **5대 / 10대 주요암** riders, which stack a second named-site
diagnosis benefit on a wider list than the composite's three-site 고액암 tier [S1] [S2]; the
five modality-split **항암치료 riders** — 양성자, 세기조절, 표적항암약물허가, 중입자 and plain
방사선 — each with its own 면책 and 감액 [S2]; the **간편심사** underwriting class, whose
rating effect [R4] says cannot yet be analysed; the **만기환급형 (2종)** variant returning 5%
of 보험가입금액 at maturity [S8]; the **적립부분** of the non-life form, credited at the
공시이율 with a 0.5% floor and permitting mid-term withdrawal capped at 80% of its own
해지환급금 [S1]; the **재가입** structure of the 15-year non-life contract [S1] [S2]; the
**특정 신체부위·질병 보장제한부 인수 특약** [S3]; the **중증 갑상선암 / 초기 갑상선암**
subdivision, which no public source can price [S3] [S4]; and the **90일 이내 유방암 10%**
variant, which both the institute and the supervisor describe [R3] [R6] but **no retrieved
약관 contains** — a real but unrepresented market variant, recorded and deliberately not
modelled.

---

## Variations across insurers

1. **Who writes it.** Three of the seven are 손해보험 writers [S1] [S2] [S8] and four are
   생명보험 writers [S3] [S4] [S5] [S6] [S7], carrying materially the same benefits under
   보험업법 제4조제3항 [REG-R1]. Composite: drafted as a life contract; nothing turns on it.
2. **Chassis.** 비갱신형 at two [S3] [S5]; 갱신형 at four, on 10-year, 1–10-year and to-100세
   terms [S4] [S6] [S7] [S8]; a 15-year term with **재가입** at two [S1] [S2]. Composite:
   **비갱신형 to 100세**, against the majority, because the two devices this chassis exists to
   demonstrate are disapplied on every renewal (footnote 2).
3. **Benefit menu.** Diagnosis-only in three tiers [S6] [S7] or five [S3]; twenty-three
   independently purchasable modules [S4]; diagnosis plus twenty-odd riders [S1] [S2]; and
   **treatment-only, with no diagnosis lump sum at all** [S5]. Composite: four diagnosis tiers
   plus three switchable event modules (footnote 1).
4. **면책기간, 일반암.** 90 days at six [S1] [S2] [S3] [S4] [S7] [S8]; **none at all** at one,
   whose product name means "from the first day" [S6]. Composite: 90 days — and the existence
   of [S6] is what proves it is a convention rather than a mandate (footnote 16).
5. **면책기간, 유사암, on a 갱신계약, and below 보험나이 15.** None on 유사암 at five [S1] [S2]
   [S6] [S7], **갑상선암 90 days** at two [S3] [S4]; none on a 갱신계약 and none below 보험나이
   15 wherever stated [S2] [S4] [S6] [S7] [R3] [R6]. Composite: none in all three cases — and
   the under-15 carve-out is the rule `Child_KR_S` inverts.
6. **감액기간, 일반암.** **None** at the newest contract [S2]; **1 year at 50%** at two [S1]
   [S6]; **2 years at 50%** at four [S3] [S4] [S5] [S7], with a **two-step 25% / 50%** on robot
   surgery at two [S2] [S5]. Two years is modal; composite takes **1 year** (footnote 19), with
   0 and 24 as switches.
7. **What the 감액 clock ends at.** 진단확정일 for diagnosis benefits and **수술일** for
   surgery benefits, at every carrier that states it [S3] [S4] [S5]. Composite: the same split.
8. **유사암 membership and ratio.** Four members at four carriers [S6] [S7] [S8] [S9], **five**
   adding 대장점막내암 at three [S1] [S2] [S3] [S4]; ratios of **10%** at two [S6] [S7],
   **20%** at two [S3] [S4], **70%** on a pre-2022 design [S8], a separately underwritten rider
   with its own 가입금액 at two [S1] [S2], and 「10~20%」 as the market description [S9] [S10].
   Composite: five members at **20%** (footnote 21).
9. **Middle tier.** 특정소액암 at **60%** on a four-site list [S3] [S4]; 유방·전립선 at **20%**
   as a tier of its own [S6] [S7]; a named five-site list with no published ratio [S1] [S2];
   and a 2019 example at 유방·전립선 40% / 갑상선 30% / 기타피부 10% [R3]. Composite: **60%**.
10. **갑상선암 subdivided.** Yes at two, into 중증 80% / 특정소액 60% / 초기 20% [S3] [S4]; no
    at five. Composite: **no**, because the registry publishes no histology or size split and a
    subdivided tier could not be priced from any public source (footnote 23).
11. **High tier.** A tight three-site KCD list paid **in addition** [S3] [S4]; 5대 and 10대
    주요암 as separate stacking riders [S1] [S2]; a ten-site description [S9]; a 3 / 5 / 10
    ladder [S10]. Composite: the tight list, at +100%, paid in addition (footnote 22).
12. **Diagnosis frequency.** **최초 1회한** in every retrieved contract without exception
    [S1]–[S7], with 재진단암 as a rider on a **2-year** cycle at two [S1] [S8]. **No retrieved
    contract carries a 1-year cancer cycle** [unverified]. Composite: once, rider off.
13. **Inpatient benefit.** 180 days per stay with 유사암 at 20% [S1]; **상급종합병원 only, 2일
    이상, 1일 초과, 120일 한도** [S4]; **4일 이상** with 요양병원 as a separate rider [S8];
    split into 요양병원-excluded and 요양병원 90일한도 limbs [S2]; absent from the
    diagnosis-only contracts [S3] [S6] [S7]. Composite: day 1, 180 days, 요양병원 to a separate
    rider.
14. **Surgery and treatment benefits.** 최초 1회한 and 1회당 surgery riders sold together [S1];
    **관혈 : 비관혈 = 5 : 1** [S4]; a 다빈치로봇 module in the newest contracts [S2] [S5]. On
    treatment: one rider with 기타피부암·갑상선암 at **20%** [S1]; two limbs at a **4 : 1**
    ratio [S4]; five modality-split riders [S2]; the whole product [S5]. Composite: 5 : 1
    surgery, unlimited count, and one 최초 1회한 treatment rider with 유사암 at 20% (footnote
    24).
15. **Premium waiver trigger.** 암 excluding 소액·유사암, or 장해 50% [S3] [S4]; 암 (유사암
    제외), 뇌출혈 or 급성심근경색증 [S1]; 장해 50% and 암 [S6] [S7]; **set by the 사업방법서
    rather than the 약관** at one [S2]. Composite: invasive cancer plus 장해 50% (footnote 14).
16. **Death cover.** None on any life contract — death pays the **계약자적립액** and ends the
    contract [S3] [S4] [S5] [S6] [S7]; an optional 암 사망 및 고도후유장해 rider on the
    non-life form [S1]; a 질병사망 rider at one [S8]. Composite: none, rider as a switch.
17. **Surrender and maturity.** 표준형 or **해약환급금 미지급형 (납입중 0% / 납입후 50%)**
    [S3]; 적립부분 credited at the 공시이율 with a **0.5%** floor [S1]; 계약자적립액 at
    **연복리 1.5%** with an illustrated 환급률 peaking near 21.6% at year 5 and nil at maturity
    [S8]. Maturity benefit: none at five, the 적립부분 at one [S1], **5% of 보험가입금액** at
    one [S8]. Composite: **미지급형**, no maturity benefit, 표준형 as the comparator switch
    (footnote 29).
18. **Issue ages and premium modes.** 만15~65세 with 월/3개월/6개월/연납 [S1]; 20~60세 with
    월납 only and renewal to 89 [S8]; renewal to a 100세 만기 past 가입나이 85 [S7]; 간편심사
    to 75 [R4]. Composite: 보험나이 15–65, 월납 (footnotes 5 and 10).
19. **What does not vary at all.** Every retrieved contract (i) defines cancer by reference to
    the KCD and lists the codes in a 별표; (ii) requires 진단확정 by a **병리과 또는
    진단검사의학과 전문의** on 조직검사 / 미세바늘흡인검사 / 혈액검사 microscopy, with a
    documented-evidence fallback; (iii) dates the diagnosis to the **검사 결과보고 시점**; (iv)
    carries the **C77–C80 원발부위 기준** clause mandated from 2011-04-01; (v) excludes
    **전암(前癌)상태** by name; (vi) pays the main diagnosis benefit **최초 1회한**; (vii)
    provides a **제3자 (종합병원 전문의)** opinion procedure at the insurer's entire expense;
    and (viii) is **무배당**. Those eight are the invariant core of the composite, and (i),
    (iv) and (vi) are the three a reader coming from `jplib/products/cancer/` must not carry
    over unchanged: Japan's contracts define cancer by ICD annex too, but they have no
    primary-site instruction from a supervisor, and their diagnosis benefit **repeats on a
    two-year cycle** where Korea's is once-only with a separate rider for the repeat.

---

## Regulatory context

**Classification and licence.** 암보험 is a **제3보험상품 — 질병보험**, under 보험업법
제2조제1호다목 and 제4조제1항제3호 [REG-R1] [R8]. Korea does not treat sickness cover as a
species of indemnity insurance: 제2조제1호나목 expressly carves 질병ㆍ상해 및 간병 **out** of
손해보험상품 and 다목 makes them a class of their own, which has no US, UK, French or German
parallel and whose closest analogue is Japan's 第三分野 — a licence *scope* rather than a
product *class* [REG-R1]. 제4조제3항 makes the class a shared field, which is why both a life
and a non-life insurer appear in this composite, and 시행령 제1조의2 confirms that 제3보험상품
is exactly three contracts: 상해보험계약, 질병보험계약, 간병보험계약 [REG-R1] [REG-R7].

**Product design.** 감독규정 **제7-63조제1항제1호** is the rule that shapes this product's
balance sheet: a 제3보험 product must be designed so that on **death from a cause it does not
cover** the 계약자적립액 and the 미경과보험료 are paid and the contract terminates [REG-R17].
That is why `Cancer_KR_S` carries an account balance despite being pure protection, and
제7-61조 applies the whole of 제7-63조 to 장기손해보험, so the non-life form is designed
identically [REG-R17]. 제7-70조 applies the 산출방법서 and 해약환급금 rules of
제7-65조~제7-68조 to 제3보험, so **one surrender-value regime governs all ten `krlib`
products** [REG-R19].

**Pricing and filing.** The 산출방법서 is a **기초서류** filed with the FSC and is not public
[REG-R2]. Its mandatory contents include, for any contract longer than three years, a premium
calculation on **현금흐름방식** with an adequacy analysis on 최적기초율, and a 해약환급금
calculation comparing the 계약체결비용 against the **표준해약공제액** where the former exceeds
the latter at the 기준연령 요건 [REG-R18 제7-64조](#krlib-reg-r18). Insurers may use the rate bureau's
**참조순보험요율**, filed by 보험개발원 with the FSC under 보험업법 제176조, and doing so is
**deemed** to be a filing of the 순보험료 [REG-R4]. There is no obligation to publish it and
the visible KIDI channels carry no 참조순보험요율 item [REG-R34]; what the public sees is the
**보험가격지수**, a ratio of total premium to reference net premium plus average industry
expense, which a 보장성보험 must print in its 상품요약서 [REG-R22]. The exception this product
benefits from is the KIDI 공시 page's illustrative extract of the 장기손해보험 rates in force
from 2024-04-01 [R5]. **Every incidence, morbidity and mortality rate shipped in `krlib` is
nevertheless `[std]`**, constructed from public statistics, carrying a `provenance` column and
never presented as either the 참조순보험요율 or the 경험생명표 [REG-R33] [REG-R34] [REG-R40].

**The mortality basis is not public either.** The industry table is the **제10회 경험생명표**,
applied to new business from **2024-04**, with 평균수명 남 86.3 / 여 90.7 and 65세 기대여명 남
23.7 / 여 27.1 — figures available only through a trade-press report of the KIDI release
[REG-R33]. Only summary statistics are released. `krlib` therefore builds every
`mort_table.csv` from the public 국가데이터처 생명표 — 기대수명 at birth 2024 남 80.8 / 여
86.6, 65세 기대여명 남 19.5 / 여 23.7 [REG-R38] — and adjusts toward insured mortality using
the gap the two pairs imply, about 4.2 years for males and 3.4 for females at 65 [REG-R33]
[REG-R38]. This is the sharpest single contrast with `jplib`, where the IAJ's 標準生命表
numeric tables are downloadable.

**Reserving and the surrender-value floor.** 보험업법 제120조 requires the 책임준비금 and
delegates the method [REG-R3]; 감독규정 제7-66조 sets the surrender value as 계약자적립액 less
the **표준해약공제액** of [별표 14], floored at zero, over a 해약공제기간 capped at seven
years; and 제7-66조제4항 is the legal basis of the **무해지 / 저해지** form — a dispensation
conditional on the insurer having priced with a **최적해지율**, subject to the 환급률 cap the
FSC introduced in November 2020 after finding a 무해지 20-year 환급률 of 134.1% against a
표준형 97.3% on an otherwise identical 종신보험 [REG-R19] [REG-R28]. [별표 15] then supplies
the 보험가입금액 that enters the cap for a product with no death benefit, by scaling a term
assurance's face amount by the ratio of risk premiums at the 기준연령 요건 [REG-R21] — the
mechanic without which the surrender-charge cap could not be computed for this product at all.

**Lapse, and why it is a supervisory question here.** The FSS named the problem in November
2024: with no experience on 무·저해지 business, insurers assumed high lapse right up to 완납,
which flatters profitability, and the resulting switching raised observed 표준형 lapse, which
was fed back into the 무해지 assumption — 「악순환」 [REG-R27]. The ruling adopts the
**로그-선형 모형** as the 원칙모형, converging to **0.1%** at 완납, with a post-완납 ultimate
of **0.8%**, and permits alternatives only within a closed list and only against disclosure of
the difference in CSM, best-estimate liability, K-ICS ratio and net income [REG-R27]. It
matters here because two-thirds of Korean protection new business by first-year premium is
written on the suppressed form — **11.4% (2018) → 63.8% (2024 H1)** [REG-R27] — and because
`Cancer_KR_S`'s base *is* the suppressed form. **No public Korean lapse or persistency data for
암보험 was retrieved** [R3].

**Solvency and measurement.** Korea has run **K-IFRS 1117** and **K-ICS** together since
2023-01-01, live rather than prospective, and K-IFRS 1117 is **mandatory** rather than an
option [REG-R60] [REG-R13]. K-ICS builds 지급여력기준금액 from five risk amounts, of which the
life-and-long-term-health module decomposes into seven sub-risks; five — **사망위험액,
장수위험액, 장해ㆍ질병위험액, 해지위험액, 사업비위험액** — map one-for-one onto this product's
decrements and expense assumptions, and 장해ㆍ질병위험액 is the one the cancer incidence basis
sits in [REG-R13]. On top of both sits the **해약환급금준비금** of 감독규정 제6-11조의6, a
company-level appropriation inside 이익잉여금 of the excess of aggregate contractual surrender
value over the IFRS 17 liability, with an 80% relief where the pre-transitional K-ICS ratio at
the previous quarter-end was **130% or above** [REG-R11]; it has no counterpart anywhere else
in this repository. **`Cancer_KR_S` computes none of them**: it produces one set of projected
cash flows and keeps them basis-agnostic, so the same projection can feed the IFRS 17
measurement, the K-ICS balance sheet and the distributable-earnings test. The IFRS 17 discount
curve — 국고채 yields used directly to a **최종관찰만기 of 20 years**, extending to 30 from
2025 over a three-year phase-in, then convergence to a **장기선도금리 of 4.55%** with a
**유동성프리미엄 of 91bp** [REG-R27] — is likewise not implemented; the model discounts at a
flat [std] rate.

**Conduct.** The 표준약관 of 시행세칙 [별표 15] supplies every contractual mechanic in this
document that is not carrier-specific: 보험나이 (제21조), 청약철회 (제17조), 품질보증해지
(제18조제3항), 계약 전 알릴 의무 (제13조, 제14조), 사기에 의한 계약 (제15조), 납입최고 and 해지
(제26조), 부활 (제27조), 해약환급금 (제32조), 보험계약대출 (제33조), 계약의 소멸 (제22조),
소멸시효 (제37조) and 예금보험에 의한 지급보장 (제43조) [REG-R25]. **What it does not supply is
the 암보장개시일**: the 생명보험 표준약관 was read in full and carries no such clause, the
질병·상해보험 표준약관 within the same 별표 was not read in that pass, and the product research
could not retrieve it separately [REG-R25] [R13]. The 90 days is therefore stated here as a
market convention sourced to carriers' own 약관 and to [R3] and [R6], and is **not** asserted
to be a standard-conditions requirement. Statutory 청약철회 is 금융소비자보호법 제46조
[REG-R51]; policyholder protection on insurer failure is **₩100,000,000 per person per
insurer** under 예금자보호법 시행령 제18조제7항, in a bucket that expressly excludes benefits
payable because the term has ended [REG-R52].

**Contract law.** 상법 제4편 governs and is **one-way mandatory** — 제663조 forbids any
variation to the disadvantage of policyholder, insured or beneficiary [REG-R49]. The articles
this product rests on are 제638조의3 (약관 교부·설명 의무 and the three-month cancellation);
**제644조** (보험사고의 객관적 확정의 효과), the statutory basis of the pre-암보장개시일 무효
rule [R7]; 제650조 and 제650조의2 (first-premium voidness, notice before termination, and the
statutory 부활 right); 제651조 and 제655조 (고지의무위반 and the causation defence); 제656조
(liability from receipt of the first premium — the 「다른 약정」 that the 암보장개시일 clause
is); 제662조 (the **three-year** prescription on a benefit claim) [REG-R49]; and, on the 인보험
side, **제736조** (보험적립금반환의무), the statutory floor beneath the 계약자적립액 that
감독규정 제7-63조제1항제1호 makes explicit, and **제739조의2 / 제739조의3**, the 2014
provisions that recognise the disease-insurance contract at all [REG-R50].

**The public scheme.** 국민건강보험법 제41조 defines 요양급여 by a **negative list** — cover is
everything the Minister has not designated 비급여 — and 제44조 imposes the 본인일부부담금 and
creates the 본인부담상한제 [REG-R53]. On top of that, 「본인일부부담금 산정특례에 관한 기준」
caps a registered cancer patient's share of the scheduled bill at **5% for five years**,
extendable where residual, metastatic or recurrent disease is under continuing chemotherapy
[R11]. That is the fact which makes this product 정액 rather than indemnity, and it is the
boundary between `Cancer_KR_S` and `Medical_KR_S`.

**Tax.** The premium falls in the **보장성보험료 세액공제** of 소득세법 제59조의4제1항: a **12%
credit** — 15% for a 장애인전용보장성보험 — on premiums up to **₩1,000,000 a year**, on a
contract 「만기에 환급되는 금액이 납입보험료를 초과하지 아니하는 보험」 [REG-R57]. That
qualifying test is the *same economic test* 감독규정 제1-2조제3호 uses to define a 보장성보험,
so tax law and supervisory law draw the line in the same place [REG-R9] [REG-R57]. The anchor
cell pays ₩540,000 a year, entirely within the cap, for a credit of **₩64,800** before the
local surtax — real, and second-order. It is a **credit, not a deduction**, which changes the
after-tax comparison against every other market in this repository. Benefit taxation was not
extracted for this product line and is [unverified]; **benefits are not modelled net of
policyholder tax**.

**Professional and actuarial.** Every insurer appoints a **선임계리사** under 보험업법 제181조
and 제184조, who verifies the 기초서류 and the 책임준비금 [REG-R5]. The institute's statement
of what an actuary should worry about on this product names three risks, and this document has
stated all three where they arise: **추세리스크**, because incidence is still rising and the
예정위험률 carries no trend allowance [R4]; **수준리스크**, because the 61–75 issue-age band
and the 간편심사 class have no experience behind them [R4]; and the **uncertainty of the
re-diagnosis rate**, because 「최근에는 의료기술 발달로 인해 재발하더라도 계속적으로 생존할
것으로 예상되고 있으며, 이는 **3차, 4차 암 진단보험금 지급이 가능함**을 의미함」 [R4]. To those
the research adds a fourth finding worth recording: stage-graded benefits were predicted to
fail in Korea because 「암의 진행 단계에 대한 정확한 구분이 어려우며, 이로 인해 민원이 발생할
가능성이 높음」 [R4], and no retrieved Korean contract grades by 병기 — the graded tiers that
emerged grade by **site and histology** instead [S3], which is that prediction proved half
right.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-cancer-r1
[R10]: #krlib-cancer-r10
[R11]: #krlib-cancer-r11
[R12]: #krlib-cancer-r12
[R13]: #krlib-cancer-r13
[R2]: #krlib-cancer-r2
[R3]: #krlib-cancer-r3
[R4]: #krlib-cancer-r4
[R5]: #krlib-cancer-r5
[R6]: #krlib-cancer-r6
[R7]: #krlib-cancer-r7
[R8]: #krlib-cancer-r8
[REG-R1]: #krlib-reg-r1
[REG-R11]: #krlib-reg-r11
[REG-R12]: #krlib-reg-r12
[REG-R13]: #krlib-reg-r13
[REG-R17]: #krlib-reg-r17
[REG-R18]: #krlib-reg-r18
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R21]: #krlib-reg-r21
[REG-R22]: #krlib-reg-r22
[REG-R25]: #krlib-reg-r25
[REG-R27]: #krlib-reg-r27
[REG-R28]: #krlib-reg-r28
[REG-R29]: #krlib-reg-r29
[REG-R3]: #krlib-reg-r3
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R38]: #krlib-reg-r38
[REG-R4]: #krlib-reg-r4
[REG-R40]: #krlib-reg-r40
[REG-R45]: #krlib-reg-r45
[REG-R46]: #krlib-reg-r46
[REG-R47]: #krlib-reg-r47
[REG-R48]: #krlib-reg-r48
[REG-R49]: #krlib-reg-r49
[REG-R5]: #krlib-reg-r5
[REG-R50]: #krlib-reg-r50
[REG-R51]: #krlib-reg-r51
[REG-R52]: #krlib-reg-r52
[REG-R53]: #krlib-reg-r53
[REG-R54]: #krlib-reg-r54
[REG-R55]: #krlib-reg-r55
[REG-R57]: #krlib-reg-r57
[REG-R60]: #krlib-reg-r60
[REG-R61]: #krlib-reg-r61
[REG-R7]: #krlib-reg-r7
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
