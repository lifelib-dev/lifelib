# Product Specification

**Status:** Draft, 2026-09-03 (access date for every citation: 2026-09-03).

**Scope note.** This is a *standardized composite specification* of a Korean **CI보험** (*CI
boheom*, critical illness insurance), also sold as 중대질병보험 (*jungdae jilbyeong boheom*)
— a whole-life contract carrying an **acceleration clause**, under which a contractually
defined 중대한 질병 (*jungdaehan jilbyeong*, "critical" disease) pays a stated fraction of
the death benefit early and the contract continues on the balance. It does not describe any
single insurer's product. Facts carrying a source tag — [S#] (primary product documents: 약관
(*yakgwan*, policy conditions), 상품요약서, 상품안내장 and industry-association annexes) and
[R#] (product-specific regulatory, actuarial, judicial and market references), both numbered
per `_research/ci-insurance.md` and resolved in `sources.md` (same directory; numbering
frozen, never renumbered), and [REG-R#] (the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is distinct) —
were extracted from the cited document. Values marked **[std]** are standardizations
introduced for the reference implementation; each [std] table row carries a numbered footnote
giving the rationale and, where the research pass recorded one, the observed range across
insurers. Facts the research pass could not confirm against a retrieved document are flagged
[unverified].

The composite rests on two complete 약관 from one carrier's product family — the 1,207-page
1904 edition [S1] and the 1,339-page 1705 저해지환급형 edition [S2] — one 상품요약서 that
publishes a **disclosed CI morbidity basis** [S3], one brochure carrying a 144-cell published
premium grid [S4], an industry-association cross-section of the CI and GI products then on
sale [S5], and two third-party mirrors of a second carrier's wordings [S6] [S7]. The market
leader's current product could not be retrieved and is present only at second hand [S8].

**This product states its deltas against the [whole life chassis
(종신보험)](../whole_life/product-spec.md), and does not restate it.** Everything the chassis
specifies — the 계약자적립액 (*gyeyakja jeongnibaek*, policyholder account) recursion and the
예정이율 that accrues it; 해약환급금 (*haeyak hwangeupgeum*, surrender value) as 계약자적립액
less a 해약공제액 capped by the 표준해약공제액 and running off inside seven years; the
무해지환급형 / 저해지환급형 suppression, the 표준형 comparison twin it multiplies and the
step at 납입완료; 보험계약대출 as a modelled state; 보험료 납입면제; 감액; 보험나이; the
14-day 납입최고 and the absence of any 자동대출납입 behind it; and 부활 — applies here
unchanged unless this document says otherwise. This document also keeps the chassis's
spelling convention: the *value* is written **해약환급금**, following the regulation and the
표준약관, while the *forms* keep the supervisor's generic pair 무해지환급형 / 저해지환급형;
carrier wordings are quoted as they stand, and the CI documents in this set write both
해지환급금 and 해약환급금 for the same object.

What is new is **acceleration**: one decrement produces **two payments at two dates**, and
between them the contract is still in force with a reduced sum assured, a waived premium, a
surrender value that has jumped to its unsuppressed level, and a reserve that has to carry
the residual. That is the whole of this product's actuarial content, and every section below
is written to serve it.

**Scope boundaries.** Four neighbouring shapes are named and excluded. **GI보험** (*General
Illness*) replaces the 약관 정의 방식 with the 한국표준질병·사인분류 (KCD) code and keeps the
acceleration, the whole-life chassis and the residual death benefit unchanged [R9] [R11] [S4]
[S5]; it is a parameterized variant of the trigger, described in *Variations across
insurers*, not a separate product. **SI** (staged payment as severity progresses, from 2017)
and **WI** (wider scope on standard classifications, from June 2020) are trade labels for
later generations of the same chassis [R12] [R13]. **다중지급 (multi-pay) CI** — a second
payment on a different disease group, with a three-year bar on a second cancer — is recorded
in the research file and not modelled [R1]. **변액CI** belongs to [variable annuity
(변액연금보험)](../variable_annuity/product-spec.md) for its separate-account machinery
[R14]. The 진단비 (*jindanbi*, fixed diagnosis-benefit) riders that displaced this product in
the market belong to [cancer (암보험)](../cancer/product-spec.md); the public long-term-care
scheme whose grades are one of this product's triggers belongs to [long-term care
(간병보험)](../long_term_care/product-spec.md).

---

## Product overview and market role

CI보험 is a **종신보험 with an acceleration clause, written as first-sector life business**.
The main contract promises a death benefit; the CI payment is a *pre-payment of part of that
death benefit*, not a separate sum. [S1] states the whole structure in one line of its
주요내용 요약서: 「사망보험금은 CI/LTC보험금을 수령한 경우에는 기본보험금의 50%(50%선지급형)
또는 20%(80%선지급형) 만 지급합니다」 [S1]. The complement identity holds exactly at every
observed fraction — 50 + 50, 80 + 20, and, on the first-year breast-cancer reduction, 25 + 75
and 40 + 60 [S1]. **The acceleration never adds cover.**

The health element rides on **제3보험** (*je-sam boheom*, third insurance), which 보험업법
제4조제1항제3호 defines as 상해보험, 질병보험 and 간병보험 [REG-R1] [R4]. Both life and
non-life insurers may write 제3보험. What they may not both write is the *main contract*: a
손해보험회사 cannot make 질병사망 the 주보험, and therefore cannot construct an acceleration
at all. [R1] records the consequence in terms — when a life insurer launched a women's CI
product, the non-life market's answer was the same disease list written as **독립급부 특약**
attached to a 통합보험, 「손해보험회사는 생명보험회사와 달리 질병사망을 주보험으로 설계할 수
없어 선지급 형태로 설계하지 못하고, 독립급부 형태로 상품을 설계함」 [R1]. This is a
**licensing** line, not a product-design choice, and it is the sharpest structural boundary
in the Korean health market: the acceleration is a life-insurer-only instrument.

**Origin.** CI was devised in South Africa in 1983 by a cardiac surgeon who had taken part in
the first heart transplant and watched his patients survive their disease and lose their
livelihoods to the cost of it; it reached the UK in 1985, Australia 1987, Hong Kong 1988,
Taiwan 1990 and **Korea in 2002년 5월** [R1]. The launch was the market leader's, developed
jointly with a reinsurer that had offered the design to another carrier first and been
refused, and the motive was defensive: the carrier had stopped selling health insurance in
2001 after a women's product's loss experience, and non-life insurers were taking the health
market it had vacated with 실손 riders on five-year renewable contracts [R1]. Roughly **40%**
of the risk was ceded, about 2,000,000 policies were written in four years, the reinsurer
opened a Korean branch on 2004-12-20 on the strength of it, and every other carrier followed
with a reinsurer of its own [R1]. Carrier and product names are in `sources.md` and
`_research/ci-insurance.md`, as elsewhere in `krlib`.

**Market position: a large legacy block, and a product the market has moved past.** The only
retrieved new-business series stops in 2004, and it is steep [R1], from 금융감독원's
2005-03-29 정례브리핑, excluding 변액CI, with the share of total life business in
parentheses:

| | CY2002 | CY2003 | CY2004 |
|---|---|---|---|
| 신계약 건수 (천 건) | 131 (0.5%) | 719 (3.2%) | **2,107 (9.9%)** |
| 초회보험료 (억 원) | 131 (0.2%) | 916 (1.5%) | **7,096 (11.1%)** |
| 수입보험료 (억 원) | 370 (0.1%) | 4,847 (1.0%) | **27,879 (5.3%)** |

— that is, 2004 first-year premium of ₩709.6bn (7,096억원) and premium income of ₩2,787.9bn
(27,879억원), growth of +193.1% in policy count and +674.3% in first-year premium on 2003
[R1]. Peak volume was about **1.8 million policies a year** in the mid-2000s [R1]. **No CI
series after 2004 was retrieved from any source.** The 생명보험협회 statistical series that
would carry one — the 금융통계월보(생명보험편), a 통계청 국가승인통계 built from insurers'
업무보고서 — reports 보유계약, the 보장성/저축성 split and 지급유형별 보험금 [REG-R45], and
the research pass found no CI line inside those breakdowns. The displacement of CI by 진단비
중심 건강보험 is therefore a **qualitative** claim throughout this library, resting on the
product mix in [S5], on the market leader's own 2020 move to GI [R11] and on the
four-generation account in [R12] — never on a market-share series.

**What went wrong, and why it matters to the incidence basis.** Two things failed at once.
First, **thyroid cancer**: nobody in the 2002 pricing discussion anticipated the incidence
surge — the reinsurer's team were Australian and had debated skin and prostate cancer instead
— and thyroid incidence then grew at 22.6% a year against 3.5% for all cancers [R1]. Second,
**sex mix**: over 2003–2005 women bought about 150% of the male policy count and generated
about 244% of the male claim count, on breast and thyroid cancer [R1]. Thyroid cancer is
still the single most common cancer in Korea — 35,440 cases in 2023, 12.3% of all cancers,
with a five-year relative survival of **100.2%**, statistically indistinguishable from the
general population [REG-R40]. Carriers responded by moving early thyroid cancer out of the
main contract into a rider and, from **2008**, by imposing a **180-day 부담보** on breast
cancer [R1]. The modern descendants of that bar are the first-year 50% reduction on breast
cancer in [S1] and [S2] and the general first-year 50% reduction in [S4] — both specified
below.

**The product's defining fact is the word 중대한.** Korea has no market standard for the
disease definitions: the UK has the ABI Guide to Minimum Standards, and [R1] says in terms
that Korea lacks any equivalent and recommended one — 「질병 정의에 대한 회사 간 경쟁을
지양하고 궁극적으로는 보험회사 공통의 표준화된 정의를 사용하여 … 혼란을 사전에 방지할 필요가
있다」 [R1]. What Korea *does* have is a statutory **장해분류표** (disability schedule)
inside the 표준약관 [REG-R25], and the 중대한 뇌졸중 definition points at it — so the
*severity gate* is standardised even though the *disease definition* is not. The result is a
trigger with a regulated numerator and an unregulated denominator, and it is the source of
every dispute in [R5], [R6], [R7], [R10] and [R16]. The market's answer was not
standardisation but **GI**: it removed the word rather than defining it [R11] [R12].

**Two further structural facts separate the Korean product from the UK accelerated CI cover
in `uklib` and the 三大疾病 riders in `jplib`.** There is **no survival period** anywhere:
overseas practice prices CI on a 30-day survival requirement, and the Korean supervisor
refused it on consumer-protection grounds, holding that requiring survival would create
disputes where the insured died and that paying on a post-mortem finding of the CI cause was
better protection [R1]. That refusal is the direct reason the acceleration form became the
market default, because on it the insurer is largely indifferent to whether the CI event is
followed by early death: the two benefits share one sum assured [R1]. And because the chassis
is whole-life, the contract carries a 계약자적립액, a 해약환급금, a 보험계약대출 and a
납입면제, and — in the modern generation — the Korean 무해지/저해지 suppression of that
surrender value during the premium-paying period [S2] [S4]. A UK standalone CI policy has
none of it.

---

## Representative specification

The composite is a **modern (post-2015) 무배당 CI종신보험, 80% 선지급형, written on the
저해지환급형 form**, with the full CI-era benefit menu of eight 중대한 질병, four 중대한
수술, 중대한 화상 및 부식 and 장기요양상태. The acceleration fraction is the representative
choice this document exists to argue; the chassis parameters are inherited and only their
CI-specific deltas are stated. Every level in the tables below is either read off a retrieved
document and tagged, or marked **[std]** with a numbered footnote.

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Level-premium 종신보험 with an acceleration clause; **무배당** (non-participating); **금리확정형**; carries 계약자적립액 and 해약환급금 | [S1] [S2] [S3] [S4]; 무배당 and 금리확정형 **[std]** (1) |
| Regulatory class | 생명보험 main contract (보험업법 제4조제1항제1호), with the health element in **제3보험** (제4조제1항제3호). A 손해보험회사 may not write the acceleration | [REG-R1] [R4] [R1] |
| Policy term (보험기간) | **종신** for the death benefit; **CI/LTC cover to the 100세 계약해당일** | 종신: [S1] [S3] [S4]; CI to 100세: [R1] [R13]; adoption **[std]** (2) |
| Premium-paying period (납입기간) | 20년납. Menu: 5 / 10 / 15 / 20 / 25 / 30년납 and 55 / 60 / 65 / 70 / 75 / 80세납; 5년납 and 10년납 on the 기본환급형 only | [S3] [S4]; representative 20년납 **[std]** (3) |
| Issue age (가입나이) | **보험나이 15–60**. Five years below the chassis's 15–65 ceiling, and invariant across every CI source | [S3] [S4] [R13]; age basis [S1 제26조] [REG-R25 제21조](#krlib-reg-r25) |
| Age basis | **보험나이** (*boheom nai*, insurance age): 만 나이 at 계약일 with a fraction under six months discarded and six months or more rounded up, incrementing on each 계약해당일. The one exception is 계약의 무효, which uses 만나이 | [S1 제26조]; identical in the 표준약관 [REG-R25] |
| Sum assured (보험가입금액) | ₩100,000,000 (1억원). Envelope ₩10,000,000 – ₩200,000,000, with the **accelerated** exposure capped rather than the face amount. The ceiling is a fifth of the chassis's ₩1,000,000,000 | [S3] [S4] [R1]; envelope **[std]** (4) |
| 선지급 비율 (acceleration fraction) | **80%** of the 기본보험금, paid once only across all triggers. Residual death benefit 20% | [S1] [S2] [S3] [S4] [S5] [S6]; choice **[std]** (5) |
| Surrender-value form | **저해지환급형**, `k = 0.50` applied to the 표준형 twin's 해약환급금 through 납입기간; `k = 1.00` from 납입완료 — **and from the date of any CI/LTC 지급사유** | Grades and rule: [S2]; carve-out: [S2] [S4]; factor **[std]** (6) |
| Sex | Male and female rated separately. Female premium runs **0.808–0.872** of male across the published grid; the CI incidence relation is the opposite at young ages — see *Premiums* footnote (10) | [S4] [S3] |
| Lives basis | Single life; the insured is normally the policyholder. Third-party contracts require the insured's written consent | [S1 제24조] |
| Underwriting | 일반심사 (full underwriting). 간편심사 and 무심사 forms exist on other Korean products and are a different axis from GI | [R2]; scope **[std]** (7) |
| **Anchor model cell** | 남자, 보험나이 **40**, 80% 선지급형, 보험가입금액 **₩100,000,000 (1억원)**, 보험기간 종신 (CI 보장 100세), 납입기간 **20년**, 월납, 저해지환급형 `k = 0.50`. 월보험료 **₩306,740**, which the monthly grid collects directly; the model point column carries the annualization **₩3,680,880** for the commission scale | [S4]; construction **[std]** (8) |
| Anchor cell against the chassis's | The chassis anchors the identical cell — 남 40, 1억원, 종신, 20년납, 월납, `k = 0.50` — at a **published** 표준형 월보험료 of ₩257,050, and its own 저해지 model point at ₩231,345, that figure at the chassis's **[std]** 90.0% suppression discount. **The acceleration and the CI cover therefore cost about a third more than the same whole-life contract**: 306,740 / 231,345 = **1.33** (published over constructed), or **1.19** against the published 표준형 | computed across [S4] and the chassis's anchor; comparability caveat in footnote (8) |

Footnotes to [std] rows:

1. Every CI 약관 and 상품요약서 retrieved is 무배당, and the word is in the product name at
   three carriers [S1] [S2] [S3]. **금리확정형** is the chassis's representative choice and
   is carried over unchanged: the retrieved 상품요약서 that publish complete cash-value
   tables are fixed-rate products, and a 금리연동형 CI exists in the set — [S1] credits the
   계약자적립금 at the 공시이율 with a two-tier 최저보증이율 of 연복리 **1.5%** for elapsed
   periods up to ten years and **0.5%** beyond [S1 제36조] — and is retained as a
   parameterized variant rather than dropped. The 최저보증이율 is not optional: 감독규정
   제7-60조제10호 **requires** a 금리연동형 product to set one [REG-R16].
2. The 2002 design put the acceleration inside a **two-period contract** — 제1보험기간 from
   계약일 to the day before the 80세 계약해당일, 제2보험기간 from the 80세 계약해당일
   종신토록 [S6] — and [R1] gives its economics: 「최초 판매된 선지급형 CI보험은 80세까지
   발생하는 중대질병에 대해 사망보험금을 선지급(50%, 80%)하며, 80세 이후부터는 사망보험금을
   100% 지급하도록 설계되었다」 [R1]. From **2008** the CI cover was extended to **100세**
   while the death cover stayed 종신 [R1], and the 2013 Stage product carries cover to 100
   [R13]. The composite takes the post-2008 design because it is the one a contract written
   today has, and because the 80세 split is a second, separate discontinuity that would
   collide with the 저해지 cliff in a model point trying to isolate either. The legacy split
   is named here so a reader meeting a 2002–2007 in-force policy knows it is real and knows
   this library does not model it.
3. Payment-term menus: 일시납, 5·10·15·20년납, 55·60·65·70·80세납 at [S3]; 5–30년납 in fives
   and 55–80세납 at [S4], with 5년납 and 10년납 available on the 기본환급형 only — the
   short-pay periods are **not** offered on the suppressed-value form [S4]. 20년납 is taken
   because it is the term every published rate card and every 해약환급금 illustration in the
   set is quoted on [S3] [S4], and because it puts 납입완료 at attained age 60 on the anchor
   cell, well inside the CI cover period, so the surrender-value cliff and the acceleration
   can be observed separately.
4. [S3] publishes envelopes by acceleration form: 50% 선지급형 ₩20,000,000–150,000,000
   (2,000만–1억5,000만원); 80% 선지급형 ₩10,000,000–90,000,000 (1,000만–9,000만원) [S3]. The
   80% form's ceiling is lower **precisely because the acceleration is larger** — 0.8 ×
   9,000만 = 7,200만원 against 0.5 × 1억5,000만 = 7,500만원, so the two forms are capped at
   almost the same *accelerated* exposure. That is the underwriting rule the composite
   adopts: **the cap binds the accelerated amount, not the face amount.** [R1] records market
   practice at a 2억원 maximum with 1억6천만원 accelerated at 80%, and [S4] publishes an 80%
   form at 1억원, so the 2011 9,000만원 ceiling is a single-carrier, single-vintage position
   and is not adopted. [S4] also creates **dead bands** where a contract may not be written
   at all — 6,900만–7,000만, 9,900만–1억, 1억9,800만–2억 — an artefact of its 고액계약할인
   thresholds [S4]; they are recorded and not modelled.
5. **This is the choice the product turns on.** Observed fractions, main contract, first CI
   event after year one: **50%** at [S1] [S2] [S3] [S4] [S5] [S6] [R13]; **80%** at [S1] [S2]
   [S3] [S4] [S5] [S6]; **100%** at [S4] [S5] [R11] [R14]; a policyholder-selected 30–80%
   band on one women's product and an age-varying fraction at one carrier in 2009, both [R1].
   The **50%/80% pair is the settled CI-generation design** and appears together in every
   complete 약관 retrieved. The composite takes **80%** for three reasons. It maximises the
   quantity this product exists to demonstrate: on the 50% form the residual death benefit
   equals the acceleration and the two halves of the liability are symmetric, whereas on the
   80% form the residual is a quarter of the amount already paid and the reserve after
   acceleration is visibly a different object. It is the form on which the residual's
   **floor** at 105% of the 계약자적립금 [S1] actually binds within a normal projection,
   because a 20% nominal residual is overtaken by the account value at moderate durations
   while a 50% one is not. And it is the form whose price is separately published on both a
   2011 CI rate card [S3] and a 2019 grid [S4], so the premium can be sourced rather than
   solved. The 50% form is a model-point flag, not a separate product; the **100%
   선지급플러스형 is not a pure acceleration at all** and is excluded — see footnote (13).
6. The suppressed-value design reached CI early and is stated in terms. [S2], in force
   2017-07-01, offers **30% 저해지환급형** and **50% 저해지환급형**: 「'30% 저해지환급형' 및
   '50% 저해지환급형'의 계약이 보험료 납입기간 중 … 해지될 경우의 해지환급금은 '30%
   저해지환급형'의 경우 '기본형' 해지환급금의 **30%**에 해당하는 금액으로 하며, '50%
   저해지환급형'의 경우 '기본형' 해지환급금의 **50%**에 해당하는 금액으로 합니다. 다만,
   보험료 납입기간이 완료된 이후 계약이 해지되는 경우에는 '기본형'의 해지환급금과 동일한
   금액으로 합니다」 [S2]. 50% is taken because it is the modal fraction on the chassis and
   one of the two grades this carrier offers on the CI product itself. [S4] rebrands the same
   mechanic as **해지환급금이 적은 유형** and prices it 9–12% below the 기본환급형 (see
   *Premiums*); [S5] records one carrier's 해지환급금일부지급형 as up to 30% cheaper than the
   표준형 and another's as a 저해지 30%형. **The CI-specific delta is the carve-out**, and it
   is contractual: the suppression is expressly conditioned on 「제7조 … 제2호의 CI/LTC보험금
   지급사유가 발생하지 않은 경우」 [S2], and [S4] words the same thing as applying only
   「「선지급 진단보험금」 지급사유 발생 전 납입기간 동안」 [S4]. A post-acceleration
   surrender gets the **full 기본형 value**, at any duration. The chassis has no such rule.
7. The 유병자 (impaired-life) market is a different axis from GI: **GI relaxes the benefit
   trigger, 간편심사 relaxes the underwriting** [R2]. CI has been sold into it and failed —
   the **당뇨CI보험**, a 가입한정형 product open only to diabetics without complications and
   with HbA1c ≤ 8%, paying on 뇌졸중, 말기신부전, 실명 and 족부절단, could not find enough
   eligible lives and was withdrawn [R2]. The taxonomy 일반심사 / 간편심사 / 무심사, from a
   금융감독원 보도자료 of 2013-05-15, is recorded in the research file [R2] and is out of
   this composite.
8. The anchor is [S4]'s published cell for **남 40, 80% 선지급형, 17대보장형, 해지환급금이
   적은 유형, 1억원, 20년납, 월납, 고액계약할인 적용**: ₩306,740 a month. Three things
   justify taking it. The **17대보장형** is the closest published menu to the composite's
   benefit list — eight 중대한 질병, four 중대한 수술, 중대한 화상 및 부식 and 장기요양상태
   [S1] against [S4]'s three headline diseases plus the 중증질환 group and the same four
   surgeries [S4]. The product it is quoted on is a **GI** product, so its trigger is
   code-based where the composite's is definition-based; the direction of the resulting error
   is genuinely ambiguous, because GI is broader on cancer and narrower on cerebrovascular
   disease (GI's 뇌출혈 cover is often I60–I62 where 중대한 뇌졸중 reaches I63) [R9] [S4]
   [S5], and [R9]'s claim that CI runs about 2% dearer is a secondary assertion with no basis
   stated and is [unverified]. And the level cross-checks: [S3]'s 2011 CI rate card gives
   ₩276,100 a month for the 80% form at 9,000만원 on male 40, which scales to **₩306,778 per
   1억원** — 0.01% from [S4]'s figure. The two are not like-for-like (a 2011 universal 기본형
   at a 4.5% 적용이율 against a 2019 저해지 form at about 2.75%), so the agreement is
   coincidence and is recorded only as a sanity check on the level. **The cell is
   deliberately the chassis's own anchor**, which is in turn the regulator's 기준연령 요건 —
   만 40세 male on monthly premiums [REG-R9 제1-2조제2호](#krlib-reg-r9) — and the industry comparison basis
   for 종신보험 disclosure, 1억원 / 종신 / 20년납 / 월납. Only the **×1.19** relativity in
   the row above is between two *published* cells: the ×1.33 divides that same published CI
   premium by the chassis's 저해지 **model point**, which is the published ₩257,050 at the
   chassis's own **[std]** 90.0% suppression discount, so its denominator is constructed.
   Both are also across **different carriers and eight years apart** (a 2019 GI product
   against a whole-life scale of a different vintage), so each is an order-of-magnitude
   statement about what the CI cover costs and not a like-for-like price comparison;
   `technical-notes.md` reproduces the split from the model instead. `CI_KR_S` runs an
   **annual** grid, so the annual premium is standardized as 12 × the monthly figure =
   **₩3,680,880**; no carrier publishes an
   annual-mode premium for this cell, so the modal discount a real 연납 scale would carry is
   not applied and the direction of the error — annual premium slightly overstated — is
   stated in `technical-notes.md` rather than hidden. The published figure is already net of
   the 고액계약할인 [S4], so a model applying that discount again double-counts it.

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium basis | Level and guaranteed for 납입기간, subject to the statutory 위험률 revision right below. No renewal mechanic on the main contract | [S1] [S3] [S4] |
| Mode (납입주기) | 월납 in the market; the composite pays **연납** at 12 × the monthly rate | [S3] [S4]; annualization **[std]** (8) |
| Rating factors | 보험나이, sex, 보험가입금액 (via 고액계약할인), 납입기간, 선지급 비율, benefit menu, and whether the 저해지환급형 form is taken | [S3] [S4] |
| Price of the acceleration fraction | 80% form costs **2.8–9.4%** more than the 50% form on the same age, sex and menu; the 100% form **29.6–38.2%** more | computed on [S4]'s 144 cells (9) |
| Price of the benefit menu | Across 2대 → 암 → 3대 → 17대 the spread is only **12.8%**; the fourteen conditions beyond the three headline diseases add about **5.3%** | computed on [S4] (9) |
| 저해지환급형 premium discount | **9–12%** below the 기본환급형 on the published grid (i.e. 88%–91% of it); up to 30% claimed elsewhere. The band brackets the chassis's chosen 90.0% at the same `k = 0.50` | [S4] computed; range [S5] |
| Sex differential | Female premium **0.808–0.872** of male at the same cell (0.830 at 남40/여40, 17대, 50%); **0.774** on the 2011 CI card at age 40 | [S4] [S3] (10) |
| Age slope | 남 30 → 40 on 17대 / 50% is ×1.293 over ten years, a compound 2.6% a year — flat, because a 20-year-pay whole-life premium is dominated by the savings element | computed on [S4] |
| Assumed interest rate (예정이율) | **연복리 2.50%, flat** — the chassis's value, inherited unchanged | chassis; CI evidence [S3] [S4]; [REG-R48]; **[std]** (11) |
| 최저보증이율 (금리연동형 variant only) | 연복리 **1.5%** for elapsed periods to ten years, **0.5%** beyond | [S1 제36조] |
| Volume discount (고액계약할인) | 7,000만–1억원 미만 **1%**; 1억–2억원 미만 **2%**; 2억원 이상 **3%**, applied to the main-contract premium. Anchor cell takes 2% and the published rate is discount-inclusive | [S4]; adoption **[std]** (12) |
| Preferred-risk discount (건강인우대) | Criteria published — 직전 1년간 비흡연, 수축기 혈압 110–139 mmHg, BMI 20.0–27.9 kg/m², 가입나이 20–60 — **discount percentage not published** | criteria [S4]; level [unverified] |
| Substandard rating | 특별조건부특약 (할증보험료법); the loading is added to the main-contract premium **before** the 고액계약할인 is taken | [S3] |
| 효도특약 | 2% of the office premium including riders, where the insured is the policyholder's or spouse's parent aged 50 or over and the beneficiary is the policyholder or the insured | [S4] |
| Risk-rate revision right | From **5 years** after the contract, with 금융위원회 approval, the insurer may change the 예정위험률; where the change raises the premium or the reserve it is applied by **reducing the benefit or the sum assured** unless the policyholder funds the increase over the remaining premium term, or in a lump sum if paid up | [S3] |
| 보험료지수 | **130.1%** on the 80% form, 130.9% on the 50% form, at 남 40세 월납 | [S3] |

9. Computed here from the 144 published cells of [S4] — three acceleration forms x four
   benefit menus x six age/sex columns, on each of the two return forms — stated as
   arithmetic on that source. At
   남40 / 17대보장형 / 기본환급형 the three acceleration forms run 311,640 → 338,100 (×1.085)
   → 428,260 (×1.374); at 남30 / 17대, 241,080 → 263,620 (×1.093) → 333,200 (×1.382). Those
   are the *steepest* cells: **the 80 : 50 step ranges over the whole grid from ×1.0278 (여35
   / 2대보장형 / 기본환급형) to ×1.0935 (남30 / 17대 / 기본환급형), and the 100 : 50 step from
   ×1.2959 (여30 / 2대 / 저해지) to ×1.3821 (남30 / 17대 / 기본환급형)** — the step widens
   with the menu, because the acceleration fraction multiplies a larger disease list. **The
   100% jump is much larger than the 50 → 80 step because it is not a re-weighting**: on that
   form the death benefit is extinguished and replaced by a separately funded 유족위로금 —
   see footnote (13). On the menu, at 남40 / 50% / 기본환급형, 2대 → 암 → 3대 → 17대 runs
   276,360 → 284,200 → 295,960 → 311,640. **The three headline diseases carry almost all the
   cost**, which is the single most useful pricing fact in this file and is consistent with
   the morbidity basis in *Contractual mechanics*: 중대한 암, 중대한 급성심근경색증 and
   중대한 뇌졸중 are the whole of the CI decrement to two significant figures.
10. The published premium relation and the published incidence relation point in **opposite
    directions at young ages**, and a reader must not read one off the other. On [S3]'s
    disclosed 예정위험률 the three headline CI rates sum to 0.002767 for a female 40 against
    0.002519 for a male 40 — female incidence is **1.10×** male — while female premium is
    0.83× male [S4]. The reconciliation is that the premium is dominated by the death benefit
    and by old-age CI incidence, where the female rates are far below the male ones (0.010588
    against 0.019433 at 60), and by the savings element, which is sex-neutral.
11. **The 예정이율 is the chassis's and is not re-derived here**, because no CI-specific
    pricing rate later than 2011 was retrieved and the two CI figures that exist bracket it
    from too far away to be useful. [S3] states 「무배당 베스트유니버셜CI보험의 보장부분에
    적용한 예정이율은 **연복리 4.0%**입니다」 for a January 2011 product, with an 적용이율 of
    4.5% and a **flat 연복리 4.0%** 최저보증이율 [S3]; [S4]'s 종신 versus 연금 comparison,
    prepared on the 생명보험협회 상품공시시행세칙 basis, states 「종신보험의 예정이율(약
    **2.75%**)」 as at 2019 [S4]. The chassis reads six values off 2021–2025 carrier
    documents spanning **2.25%–2.75%** and takes the mid-point **2.50%**, which is also the
    **2026 평균공시이율** — down from 2.75% and its first fall since 2020 [REG-R48]. This
    product takes the same rate, because a reference library whose CI product and whose
    whole-life product discounted on different rates would make the acceleration's cost
    impossible to read off the difference between them. **Interest matters less here than on
    the chassis**, which is the reason the inheritance is safe: [S3]'s own 보장위험별
    연간보험료 disclosure shows that at male 40 on a 50% acceleration **half the risk cost is
    the CI benefit**, and a CI benefit is paid a decade or more before the death benefit it
    accelerates, so the liability is shorter in duration than the chassis's and less
    sensitive to the rate. Note also that **예정이율 is not a regulatory term in Korea**: a
    full-text search of the 감독규정 returns zero occurrences, and the regulation speaks only
    of the 계약자적립액 적용이율 and of the 금리연동형 / 금리확정형 distinction [REG-R9]
    [REG-R48].
12. Two published scales exist and they differ in depth and vintage. [S3], 2011:
    3,000만–4,900만원 1.0%; 5,000만–9,800만원 2.0%; 1억–1억9,500만원 3.0%; 2억–2억9,600만원
    5.0%; 3억원 이상 6.0% [S3]. [S4], 2019, is shallower and starts higher: nothing below
    7,000만원, then 1% / 2% / 3% [S4]. [S5] records one carrier discounting 3~4% of the
    영업보험료 at 1억원 or more and another discounting above 5,000만원 [S5]. The composite
    takes [S4]'s scale as the most recent published, and records the flattening over the
    decade as the visible trace of the 2019 사업비 reform [REG-R29].

### Benefit provisions

All percentages below are of the **기본보험금**, which is itself a floored quantity — see
*Contractual mechanics*. Amounts in the right-hand column are the anchor cell's, at a
보험가입금액 of ₩100,000,000 (1억원).

| Benefit | Representative provision | At the anchor cell |
|---|---|---|
| **CI/LTC보험금** | **80%** of the 기본보험금, payable **once only**, on the first of 중대한 질병 (eight), 중대한 수술 (four), 중대한 화상 및 부식, or 장기요양상태 [S1] [S2] | ₩80,000,000 (8,000만원) |
| — first-year breast cancer | The percentage **halves** to 40% where the trigger is breast cancer within one year of the 계약일 [S1] [S2] | ₩40,000,000 (4,000만원) |
| **사망보험금**, no prior CI/LTC payment | **100%** of the 기본보험금 [S1] | ₩100,000,000 (1억원) |
| **사망보험금**, after a CI/LTC payment | the greater of **20%** of the 기본보험금 at the date the CI/LTC 지급사유 arose and **105% of the 계약자적립금** after it [S1 별표1 주8] | ≥ ₩20,000,000 (2,000만원), rising with the account |
| **사망보험금**, after a first-year breast-cancer payment | **60%** of the 기본보험금, on the same floor [S1] | ₩60,000,000 (6,000만원) |
| **기본보험금** | max(기본사망보험금, 이미 납입한 보험료, **105%** of the 계약자적립금), where 기본사망보험금 = 보험가입금액 − 중도인출금액 + 추가납입보험료 [S1 별표1 주7] | ≥ ₩100,000,000 |
| **납입면제** | All future 기본보험료 waived on **either** a 장해지급률 of 50% or more from one accident or one non-accidental cause across several body parts, **or** any CI/LTC 지급사유 [S1 별표1 주4] | — |
| Complement identity | 80 + 20 = 100 and 40 + 60 = 100 exactly. The acceleration never adds cover | [S1] [S2] |

The worked benefit illustration [S2] publishes for the 80% form at ₩100,000,000 is exactly
this table, and is reproduced because it is the cleanest published statement of the mechanic
[S2, 용어해설 「보험금 지급 예시」]:

| Case | CI/LTC payment | Later death payment |
|---|---|---|
| CI/LTC event, not first-year breast cancer | ₩80,000,000 (8,000만원) | ₩20,000,000 (2,000만원) |
| First-year breast-cancer CI/LTC event | ₩40,000,000 (4,000만원) | ₩60,000,000 (6,000만원) |
| Death with no CI/LTC event | — | ₩100,000,000 (1억원) |

| Parameter | Representative value | Basis |
|---|---|---|
| 중대한 암 보장개시일 | **90 days** from 계약일 (or 부활일), counting that day — cover attaches on the day after the ninetieth | [S1 제7조] [S1 별표1 주1] [S2] [S3] [S4] |
| Other 중대한 질병, 중대한 수술, 중대한 화상 및 부식 | Covered **from the 계약일** — no waiting period | [S1] [S2 별표1 주1] |
| 장기요양상태 보장개시일 | **90 days**, waived where the state arises directly from a 재해 (accident), which is covered from the 계약일 | [S1 별표1 주2] |
| Survival period | **None**, anywhere. The benefit is payable even where the insured dies of the CI event | [R1] |
| 감액기간 (reduced-benefit period) | **First policy year, breast cancer only, ×½** | [S1] [S2]; choice **[std]** (14) |
| 자살면책 | No death benefit where the insured intentionally kills himself, save (가) an act in a state of 심신상실, and (나) **two years** from the 보장개시일, reset on 부활 | [S1 제10조]; 2 years, not Japan's 3 |
| Other 면책 | The intentional act of the 계약자 or of the 사망보험금 수취인, with the usual part-beneficiary carve-out | [S1 제10조] |
| Contestability (계약 전 알릴 의무) | Rescission barred where the insurer knew or negligently did not know; **1개월** from learning of the breach; **2년** from the 보장개시일 with no claim event (**1년** for disease on a 진단계약); **3년** from the contract date unconditionally; acceptance on submitted medical evidence; or intermediary obstruction | [S1 제19조]; identical in the 표준약관 [REG-R25] |
| 사기에 의한 계약 | Cancellable within **5년** of the 보장개시일 and one month of discovery | [REG-R25] |
| Pre-inception cancer | Diagnosed before the 보장개시일: the policyholder may **cancel and recover the premiums**; if not, that cancer is permanently outside cover, including recurrence and metastasis, and does **not** waive premiums — **but** cover revives if five years pass from the 보장개시일 with no further diagnosis or treatment for it (routine screening excluded). The identical five-year revival applies to 장기요양상태 | [S1 제7조⑤⑥] [S1 별표1 주5, 주6] |

13. **The 100% 선지급플러스형 is not a pure acceleration and is excluded.** On [S4]'s version
    the whole sum assured is paid on diagnosis after year one and 사망보험금 없음 thereafter;
    what remains is a separate **유족위로금** of 보험가입금액의 1% paid monthly for 30 months
    — 30% of the sum assured in instalments, funded as its own benefit rather than as a
    residue [S4]. The variable sibling describes the same 30% as an annuity to the family
    [R14], and one carrier's KLIA entry shows a flat 30% residue [S5]. Where a first-year
    event triggers the 100% form the acceleration is 50% and the residual death benefit is
    50% [S4]. One further 100% design pays it only on the 최중증 states — stage IV cancer,
    blood and lymphatic cancers — with 50% on stages I–III (20% for breast cancer) and a
    further 50% if a stage I–III cancer progresses to stage IV [R13]; that is the SI
    generation and is out of scope. The composite keeps the fraction in [0, 1] with an exact
    complement, because that is what makes the acceleration a redistribution of one sum
    assured across two dates rather than two benefits.
14. Two 감액 designs are in the sources and they differ in **scope**, not in depth — both
    halve. [S1] and [S2] reduce **only for breast cancer, only in the first policy year**:
    50% 선지급형 pays 25%, 80% 선지급형 pays 40%, with the death benefit's complement rising
    to 75% and 60% [S1 별표1] [S2 별표1]. [S4]'s GI product reduces **every trigger** in the
    first policy year by half — 25% / 40% / 50% for the 50% / 80% / 100% forms against 50% /
    80% / 100% thereafter — with the single carve-out running the other way, a first-year
    중대한 화상 및 부식 claim on the 17대보장형 being paid at the post-first-year rate [S4].
    [S5] records a third carrier at 「보험가입금액의 100%를 「건강진단보험금」으로 선지급
    (단, 1년미만 50%)」 [S5], the same halving. The composite takes the
    **breast-cancer-only** design because it is the CI-generation design in both complete
    약관 retrieved, and because it is the only one with an identifiable experience rationale:
    it is the lineal descendant of the 180-day breast cancer 부담보 imposed across the market
    from 2008 after the female claim excess of 2003–2005 [R1]. The all-trigger halving is a
    GI-generation simplification and is a model-point flag (`first_year_reduction_scope` ∈
    {breast, all}), not a separate product. **The modelling consequence is real**: the
    breast-cancer-only design requires the female 중대한 암 incidence to be split into a
    breast component and the rest, which the composite supplies as a **[std]** share
    calibrated on the national cancer registry — 유방 29,871 cases in 2023, 10.3% of all
    cancers, taken against a female burden of 137,487 less the **19.0%** of that burden
    which is 갑상선 and which 중대한 암 excludes as C73 [REG-R40].

### Options

| Parameter | Representative value | Basis |
|---|---|---|
| 저해지환급형 switch | Model-point column, as on the chassis: `k` ∈ {1.00 표준형, 0.50 저해지, 0.00 무해지}, applied to the 표준형 twin's 해약환급금 through 납입기간 — **and released by either 납입완료 or a CI/LTC 지급사유, whichever comes first** | [S2] [S4]; factor **[std]** (6) |
| 선지급 비율 switch | Model-point flag ∈ {0.50, 0.80}; the residual death fraction is its exact complement | [S1] [S2] [S3] [S4] |
| 납입면제 | Not an option — part of the main contract, on the two triggers above. **On this chassis it fires with essentially every CI claim**, so it is not an independent decrement | [S1 별표1 주4] |
| 보험계약대출 (policy loan) | Chassis mechanic: **80%** of the *payable* 해약환급금 net of existing principal and interest, at **예정이율 + 1.5% = 4.00%** compound. During 납입기간 the base is therefore the **suppressed** value — and it **doubles the moment a CI/LTC 지급사유 arises** | [REG-R25 제33조](#krlib-reg-r25) [S1]; chassis limit and rate; CI carve-out **[std]** (15) |
| 감액 (sum-assured reduction) | Permitted; the reduced portion is treated as surrendered and pays the corresponding 해약환급금. On a suppressed contract before 납입완료 that is the suppressed value; after a CI event it is the full one | [REG-R25]; chassis mechanic |
| 중도인출 / 추가납입 | Present on the universal-chassis forms in the set [S1] [S3]; both enter the 기본보험금 definition (− 중도인출금액, + 추가납입보험료) and neither is modelled | [S1 별표1 주7]; scope **[std]** (16) |
| 연금전환 | Not offered on any retrieved CI 약관 | — |
| 감액완납 / 연장정기보험 | **Do not appear in any retrieved Korean 약관** and are not features of this product | chassis finding; [unverified] as market features |
| 가지급제도 | Where the insurer cannot settle within the statutory window it must advance up to **50%** of the estimated benefit | [S1 제13조] |

15. The limit (80%) and the rate (예정이율 + 1.5%, so 4.00% at a 2.50% 예정이율) are the
    chassis's, argued there against published Korean ranges of 「해약환급금의 50% ~ 85%」 and
    「50 ~ 80%이내」. **The CI-specific point is the interaction with the carve-out** in
    footnote (6): before a CI event the borrowing base is 50% of the 표준형 value, and the
    moment the CI event occurs it becomes the whole of it at the same duration — the
    available loan **doubles on a diagnosis**. Nothing in the retrieved documents restricts
    the loan after a CI payment, so the post-acceleration contract carries a full-value loan
    facility against a sum assured that is now 20% of its original size; whether any carrier
    applies a further restriction there is **[unverified]**. The FSS's finding that a
    **무해지** contract cannot support a policy loan at all during the payment period
    [REG-R28] [REG-R25 제33조](#krlib-reg-r25) does not bite on a 저해지 form, which has a suppressed but
    non-zero value to lend against — a distinction the composite keeps, and one reason the
    representative form here is 저해지 rather than 무해지.
16. 중도인출 and 추가납입 belong to the universal (유니버셜) chassis and are specified there.
    They are named in this table only because they are **arguments of the 기본보험금
    formula** [S1 별표1 주7], so a model that ignores them must say it holds them at zero
    rather than silently dropping them from the definition — which is what `CI_KR_S` does.

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| 해약환급금 identity | 계약자적립액 less 해약공제액 (미상각신계약비), floored at zero, then multiplied by `k` where it applies. [S3] words it identically for a CI product: 「순보험료식 책임준비금에서 미상각신계약비(해지공제액)를 공제한 금액」 | chassis; [S3]; [REG-R19 제7-66조제1항제1호](#krlib-reg-r19) |
| 해약공제기간 | 납입기간 or 신계약비 부가기간, **capped at 7 years** — so on the anchor's 20년납 contract the charge is gone by duration 7, long before either exit from suppression | [REG-R19 제7-66조제1항제2호](#krlib-reg-r19) |
| 해약공제액 cap | The statutory **표준해약공제액**: 연납순보험료 × 5% × 해약공제계수 + 보험가입금액 × 10/1000, the coefficient being the 보험기간 capped at **20 years** for a 보장성보험, so on a 종신 contract it is **one year's net premium plus 1% of the sum assured** | [REG-R20]; the 보험가입금액 that enters it: [REG-R21] (17) |
| 표준해약공제액 at the anchor | ≈ **₩3,940,000** — 1.0 × 연납순보험료 (₩2,944,704 at the chassis's **[std]** 80% net-premium ratio on ₩3,680,880) + 1% of ₩100,000,000. Cross-check: the FSC's 보장성보험 rule of thumb of **13 × the monthly premium** gives ₩3,987,620, agreeing within **1.1%** | [REG-R20] [REG-R29]; ratio **[std]**, chassis (17) |
| Suppression period | Identical to 납입기간, **and it ends on the earlier of 납입완료 and a CI/LTC 지급사유** | [S2] [S4] |
| The step at 납입완료 | A discontinuity, not a ramp, and not a surrender-charge effect — the charge has been gone for thirteen years. On the chassis's published grids the suppressed and 표준형 values are identical to the won from 납입완료 onward | chassis; [S2] |
| Post-acceleration surrender | Full 표준형 value at every duration, before and after 납입완료 | [S2] [S4] |
| Clawback | The chassis's rule — unpaid premiums falling in the suppressed period must be made good before the post-cliff basis applies — is not restated in either CI 약관, and **whether it also gates the CI carve-out is not established** | chassis; here **[unverified]** |
| 미경과보험료 | Added to the 해약환급금 on termination | [REG-R19 제7-66조제5항](#krlib-reg-r19) |
| 만기보험금 | None — 보험기간 종신 | [S1] [S3] [S4] |
| 납입최고(독촉)기간 | **14일 이상**, from the day after the due date; the contract is 해지 the day after it ends. Policy-loan principal and interest are deducted from the 해약환급금 immediately. **There is no 자동대출납입 behind it** — the chassis's negative finding — so Korean lapse is behavioural, not funded | [S1]; 표준약관 [REG-R25 제26조](#krlib-reg-r25); chassis |
| Running on the account | Within the first **3년 (36회 납입)** the 기본보험료 must be paid when due; after that a universal-chassis contract may run on the 월대체보험료 drawn from the 해약환급금 | [S1 제29조] |
| 부활 (reinstatement) | Within **3년** of termination, provided the 해약환급금 has not been drawn — including where there is none. Fresh 계약 전 알릴 의무; arrears with interest at a company rate **within 평균공시이율 + 1%**; the insurer may decline or restrict on health, occupation or job type | [S1]; [REG-R25 제27조](#krlib-reg-r25) |
| What 부활 restarts | The **90-day 중대한 암 보장개시일**, the **2-year 자살면책** clock and both contestability clocks — the first two drafted 「계약일(부활(효력회복)일)부터」 | [S1 별표1 주1] [S1 제10조] [REG-R25 제27조](#krlib-reg-r25) |
| 청약철회 | **15 days** from receipt of the 보험증권, never after **30 days** from the application, **45일** for a distance sale to a policyholder aged 65 or over, and **not at all on a 진단계약**; effective on despatch; premiums returned within 3영업일 | [S1]; [REG-R51]; [REG-R25 제17조](#krlib-reg-r25) |
| 품질보증해지 | **3개월** from formation where the 약관 was not delivered, its important terms not explained, or the proposal not signed; premiums returned with 보험계약대출이율 interest | [S1]; [REG-R25 제18조제3항](#krlib-reg-r25); [REG-R49 제638조의3](#krlib-reg-r49) |
| 위법계약해지권 | Within **1년** of learning of the breach and **5년** of the contract; the **계약자적립액** is returned, not the 해약환급금 — which on a suppressed contract is materially more | [REG-R25 제29조의2](#krlib-reg-r25) |
| 소멸시효 | 보험금청구권 and 적립금 반환청구권 **3년**; 보험료청구권 2년 | [REG-R49 제662조](#krlib-reg-r49) [REG-R25 제37조](#krlib-reg-r25) |
| 계약의 무효 | Where a third-party death contract lacks the insured's written consent; where the insured is under 15 or lacks capacity; or where the age was outside the permitted range — the one case rated on **만나이** rather than 보험나이 | [S1 제24조] [S1 제26조①] |
| Claim timetable | **3영업일** from complete documents; **10영업일** where investigation is needed; beyond that the insurer must notify the reason, the expected date (within **30영업일**, save for litigation or a 분쟁조정신청) and the 가지급제도 | [S1 제13조] |
| Policyholder protection | 예금자보호법: **₩100,000,000** per person per insurer on 보험금 claims, in a bucket separate from 연금저축 claims, and **excluding** benefits payable because the policy term has ended | [REG-R52]; [REG-R25 제43조](#krlib-reg-r25) |

17. The 보험가입금액 that enters the 표준해약공제액 formula is **not automatically the face
    amount**, and this product's position is worth stating because it differs from its
    제3보험 siblings. 감독규정 [별표 15] 제3호 provides that 「일반사망을 보장하는
    보장성보험은 일반사망보험금으로 한다」, and 제8호 that the figure is taken **before any
    increase or decrease** [REG-R21]. A CI contract covers death from any cause, so 제3호
    applies directly and the 보험가입금액 is the **pre-acceleration** death benefit —
    ₩100,000,000 at the anchor cell, not the ₩20,000,000 residual. [cancer
    (암보험)](../cancer/product-spec.md) and [children's insurance
    (어린이보험)](../child/product-spec.md), which have no 일반사망 cover, must instead build
    a *notional* 보험가입금액 through 제9호's risk-premium ratio against a term policy
    [REG-R21]. **That is a clean instance of the acceleration form buying the product a
    simpler regulatory position than the standalone form would have.**

---

## Contractual mechanics

Notation. The chassis's symbols are used unchanged — `x` 가입나이 on 보험나이, `t` completed
policy years, `m` 납입기간, `n_sc = min(m, 7)` the 해약공제기간, `SA` 보험가입금액, `G` and
`P` the annual gross and net premiums, `i` the 예정이율, `q(x+t)` the 적용위험률, `V(t)` the
표준형 twin's 계약자적립액, `SC(t)` the 해약공제액, `W(t) = max(0, V(t) − SC(t))` the 표준형
해약환급금, `CV(t)` the payable 해약환급금, `k` the suppression factor, `L(t)` the
보험계약대출 balance and `i_L = i + 1.5%` its rate. This product adds:

    a        선지급 비율, the acceleration fraction (0.80 on the composite)
    r        the residual death fraction, r = 1 - a (0.20)
    B(t)     기본보험금 at t — the floored base every percentage applies to
    c        the 계약자적립금 floor multiple under the residual (1.05)
    f        the 감액 factor in the first policy year (0.5, breast cancer only)
    n_CI     the last policy year of CI cover — the 100세 계약해당일, so n_CI = 100 - x
    q_ci(t)  the CI decrement: a first-event rate across the whole trigger set
    t_CI     the policy year of the CI/LTC 지급사유, if any

### What this product adds to the chassis, in one table

| Chassis mechanic | What CI changes |
|---|---|
| One decrement (death), one payment | **Two payments from one decrement**, at different dates, sharing one sum assured |
| Death benefit level at `SA` for life | Death benefit is `SA` before the CI event and `max(r × B(t_CI), c × V(s))` after it — a **floored, growing** residual |
| Premium level to `m`, waived on 장해 50%+ | Waived on 장해 50%+ **or any CI/LTC 지급사유**, so the waiver is not an independent decrement on the CI limb |
| Suppression released at `t = m`, a deterministic date | Released at `min(m, t_CI)` — a **random** date, correlated with the product's own decrement |
| Policy loan base `0.80 × k × W(t)` | Same, but the base **doubles at `t_CI`** because `k` goes to 1 |
| No severe-disability acceleration; the slot is filled by 납입면제 | The slot is filled by the **acceleration itself**, and 납입면제 rides on top of it |
| Mortality is the whole decrement basis | **Morbidity dominates**: the CI decrement is 3.7× the death decrement at male 40 and 6.7× at male 60 [S3] |
| Cover ends only on death | Death cover 종신, but **CI cover ends at the 100세 계약해당일** — a second, later boundary |
| No waiting period | **90 days** on 중대한 암 and on 장기요양상태; nothing on the rest |

### The acceleration, and what the model has to carry between the two payments

The mechanic in one line: **one decrement, two payments, one sum assured.** On the first
qualifying event the insurer pays `a × B(t)`; the contract does **not** terminate; the death
benefit becomes `max(r × B(t_CI), c × V(s))` for `s > t_CI`; and the premium stops. Three of
those four clauses are contractual deltas on the chassis, and each has to be modelled.

**The contract continues, and that is a regulatory requirement rather than a design choice.**
감독규정 제7-60조제8호 provides that, except where severe injury or disease makes cover
impracticable, a contract must **not be extinguished while the risk it covers remains
effective** [REG-R16 제7-60조제8호](#krlib-reg-r16). A Korean accelerated product therefore cannot pay its CI
benefit and close; it must carry the residual. That is the rule behind the whole post-CI half
of this liability, and it is the same rule that makes Korean cancer products continue after a
diagnosis payment rather than terminating.

**The benefit is payable once only, across the whole trigger set.** [S1] pays **one**
CI/LTC보험금, on the first of 중대한 질병, 중대한 수술, 중대한 화상 및 부식 **or**
장기요양상태 [S1 별표1]. The LTC state is not an additional benefit; it is another way into
the same acceleration. For a model this means `q_ci(t)` is a **first-event rate across a
competing risk set**, not a sum of marginal incidences — and Korea's supervisor required
exactly that in pricing. [R1] records it: overseas practice ignores the correlation between
CI causes for rate stability, whereas 「국내의 경우 위험률과 담보 간 일치에 대한 규제가
강하고 … CI 질병들 간 중복해서 발생할 수 있는 확률을 최대한 반영한 최종 위험률로 검증받고
사용하였다」 [R1]. A `CI_KR_S` incidence table built by adding published site-specific
incidences would therefore be wrong in the direction the Korean regulator specifically
legislated against, and `technical-notes.md` states the overlap adjustment it applies.

**There is no survival period, and the rate absorbs the consequence.** Overseas CI is priced
on a minimum 30-day survival requirement; the Korean supervisor refused it, holding that
requiring survival would create disputes where the insured died and that paying on a
post-mortem finding was better consumer protection [R1]. So the CI rate includes lives who
die of the CI cause without a separate diagnosis event — which [R1] notes the underlying
diagnosis statistics do not capture, an acknowledged upward bias in the exposure that the
rate must absorb [R1]. Two modelling consequences follow. The CI and death decrements are
**not** independent competing risks in the usual sense: a fraction of what would be a death
claim on an ordinary 종신보험 is a CI claim followed shortly by a residual death claim here.
And the insurer is largely indifferent to the ordering, which is the whole risk-management
logic of the design — [R1] describes CI as 「종신보험의 사망보험금을 선지급하는 상품으로
개발되어 건강보험이 가질 수 있는 보험리스크를 축소」 [R1].

**The residual is not a constant.** [S1] floors the post-CI death benefit: where a death
claim follows a CI payment the insurer pays 「CI/LTC보험금 지급사유 발생당시의 기본보험금의
50%(80%형은 20%)와 CI/LTC보험금 지급사유 발생 후 계약자적립금의 105% 중 큰 금액」 [S1 별표1
주8]. So

    death benefit after acceleration = max( r * B(t_CI), c * V(s) )   for s > t_CI, c = 1.05

and on a long-surviving post-CI policy the residual **grows above its nominal complement** as
the account accumulates. **The floor binds early on the 80% form, and that is measurable
rather than rhetorical.** At the anchor cell `r × B = 0.20 × ₩100,000,000 = ₩20,000,000`, so
the floor takes over as soon as `V(t) > ₩19,050,000` — which on a ₩3,680,880 annual premium
happens well inside the premium-paying period. On the 50% form the same test needs `V(t) >
₩47,600,000` and is not reached until much later, if at all. **So on the 80% form the
residual death benefit is, for most of the contract's life, the account value and not the
stated complement**, and a model that hard-codes 20% of the sum assured understates the
post-CI liability by a growing margin. That asymmetry is one of the three reasons the
composite takes the 80% fraction. [S3]'s older universal version of the same product uses
**110%** rather than 105% [S3], so `c` is a carrier and vintage parameter and is carried as
such rather than hard-coded.

**The premium stops.** Any CI/LTC 지급사유 waives all future 기본보험료 [S1 별표1 주4], so
the post-CI state carries no premium income at all, and the residual death benefit is funded
entirely out of the reserve standing at the acceleration date. [S4] states the reserving
consequence in terms: where the waiver fires because of a CI event, the insurer computes the
reserve on the post-acceleration basis — 「「선지급 진단보험금」 발생 이후 기준의
책임준비금을 계산」 [S4].

### 기본보험금 — the floored base every percentage applies to

Every benefit in this contract is a percentage of the **기본보험금**, and the 기본보험금 is
itself a maximum of three things [S1 별표1 주7]:

    B(t) = max( 기본사망보험금, 이미 납입한 보험료, c * V(t) )
    기본사망보험금 = 보험가입금액 - 중도인출금액 + 추가납입보험료

This is a distinctive Korean floor and it is not decorative. The **premiums-paid** limb means
the CI benefit on the 80% form cannot fall below 80% of cumulative premiums paid, and the
**account-value** limb means that on a long-dated contract the base itself grows.

**At the anchor cell neither of the two floors on `B(t)` binds within the premium-paying
period**, and it is worth saying so plainly so that a model is not built around a clause that
never fires: cumulative premiums at 납입완료 are ₩3,680,880 × 20 = **₩73,617,600**, well
under ₩100,000,000, and `c × V(t)` reaches ₩100,000,000 only when `V(t)` exceeds ₩95,238,095,
which happens at a long duration on a 1억원 contract. The floors bind in exactly the two
places a Korean designer would want them to — a short-pay or high-premium cell, where
premiums paid can overtake the face amount, and a very old attained age, where the account
can. The floor on the **residual** is a different matter and binds early, as the previous
section shows.

The premiums-paid limb is the contractual form of a supervisory design rule: 감독규정
제7-60조제9호 requires the death benefit to be **at least cumulative premiums paid**, except
after annuity payments have begun and except where the premium-paying period ends at age 80
or below [REG-R16]. On the anchor cell 납입기간 ends at attained age 60, so the exception
applies and the rule does not strictly bite; the floor is therefore read here as market
practice that happens to coincide with the rule, not as compliance with it. The reading is
this document's, not the research file's, and is flagged as such.

### 중대한 암 — the definition, and where the narrowing actually is

[S1] 별표4 Ⅰ, quoted:

> 「"중대한 암"이라 함은 악성종양세포가 존재하고 또한 주위 조직으로 악성종양세포의
> 침윤파괴적 증식으로 특징지을 수 있는 악성종양을 말하며, 다음 각 목에 해당하는 경우는
> 보장에서 제외합니다.」

The operative words are **침윤파괴적 증식** — invasive, destructive proliferation into
surrounding tissue. The definition names no stage, no size and no grade; it names a
*behaviour*. [R1]'s comparison table makes the essential point: read on its own terms the
opening sentence 「암에 대한 일반적인 특징(진행성, 침윤성)을 설명한 것으로 일반암에도 해당할
수 있는 사항임」 — it would cover most cancers. **The narrowing is done by the exclusion
list, not by the opening sentence** [S1 별표4 Ⅰ①]:

- **가.** six named malignancies: 피부의 악성흑색종 (melanoma) at **T2aN0M0 이하** on the TNM
  classification; 기타피부암 (**C44**); 전립선암 (**C61**); 갑상선암 (**C73**); a cancer
  arising before the 중대한 암 보장개시일 that recurs or metastasises after it; and
  **대장점막내암** — a colorectal malignancy (C18–C20) whose cells have breached the 기저막
  into the 점막고유층 or the 점막근층 but **not** the 점막하층
- **나.** 병리학적으로 전암(前癌)상태, **제자리암** (carcinoma in situ, D00–D09) and
  **경계성종양** (D37–D48, excluding D45, D46, D47.1, D47.3, D47.4, D47.5)
- **다.** any currently benign tumour, whatever the body site

[S1] then does something a UK CI wording does not: it publishes a **positive KCD code list**
of what *is* 중대한 암, on the 7th revision of the 한국표준질병·사인분류 (통계청고시
제2015-309호, in force 2016-01-01) — C00–C14, C15–C26, C30–C39, C40–C41, C43, C45–C49, C50,
C51–C58, C60, C62, C63, C64–C68, C69–C72, C74, C75, C76–C80, C81–C96, C97, plus the
myeloproliferative group **D45** (진성 적혈구 증가증), **D46** (골수형성이상증후군),
**D47.1** (만성 골수증식질환), **D47.3** (본태성 혈소판혈증), **D47.4** (골수섬유증) and
**D47.5** (만성 호산구성 백혈병) [S1 별표4 Ⅰ②]. So the 약관 is **simultaneously code-based
and definition-based**: the code list bounds the universe, and the 침윤파괴적 증식 test and
the exclusions cut it down. GI's innovation was to keep the first half and delete the second
[R9] [R11].

Diagnostic evidence [S1 별표4 Ⅰ③–⑥]: the diagnosis, 원발병소, type and stage must be settled
by a 병리 or relevant specialist (**치과의사 제외**) at a 의료법 제3조 institution; it must
rest on the microscopic findings of a 조직검사, 미세바늘흡인검사, 혈액검사 or 골수검사, with
documented evidence of diagnosis or treatment sufficing where none is possible; staging
follows the **AJCC Cancer Staging Manual 제7판** or the edition current at diagnosis; and
staging is **병리학적** where possible and 임상적 otherwise. Under the KCD selection rules,
secondary and unspecified sites C77–C80 are classified to the **원발부위** where a primary is
identified [S1 별표4 Ⅰ, 유의사항] — a detail that matters to any model reasoning about
metastases.

**The exclusions are where the money is, and every one has a history.** Melanoma below
T2aN0M0, other skin cancer, prostate and thyroid are each either a low-severity
high-frequency site or a site that produced adverse experience; thyroid and breast are the
two that broke the original pricing [R1]. **대장점막내암 was written out expressly after
litigation of exactly that lesion.** In [R5] — 서울중앙지방법원 2016. 1. 14. 선고
2014가단242567 — the insured was diagnosed in June 2014 with a colorectal carcinoma confined
to the mucosa. The court held that the 약관's 침윤파괴적 증식 test was **not** satisfied by a
mucosa-confined lesion and rejected the ₩53,000,000 CI claim; but it allowed the ordinary 암
rider claim, because the diagnosis carried the KCD code **C18** (결장의 악성 신생물), and
allowed the surgery benefit for the endoscopic polypectomy — award ₩13,000,000 [R5]. **The
same histology is 암 for the rider and not 중대한 암 for the main contract.** That sentence
is the product's defining consumer problem in one line, and it is why the incidence basis for
`CI_KR_S` cannot be the national cancer registry's headline rate.

The gap is quantifiable from public data, and `technical-notes.md` sizes it: on the 2023
registry, 갑상선 is 12.3% of all cancers and 전립선 7.8%, so those two exclusions alone
remove about a fifth of registered incidence before 제자리암, 경계성종양, 기타피부암, early
melanoma and 대장점막내암 are taken out [REG-R40]. The registry's own thyroid figures show
why: five-year relative survival of **100.2%** [REG-R40].

### 중대한 급성심근경색증 — the conjunction, and the excluded modern diagnosis

[S1] 별표4 Ⅱ, quoted:

> 「"중대한 급성심근경색증"이라 함은 관상동맥의 폐색으로 말미암아 심근으로의 혈액공급이
> 급격히 감소되어 해당 심근조직의 비가역적인 괴사를 가져오는 질병으로서 한국표준질병·
> 사인분류 중 '중대한 급성심근경색증 대상 질병분류표'에 해당하는 질병 중에서 발병 당시
> 다음의 3가지 특징을 모두 보여야 합니다.
> 가. 의사가 작성한 진료기록부상 전형적인 흉통의 존재
> 나. 급성 심근경색의 전형적인 심전도 변화(ST분절, T파, Q파)가 새롭게 출현
> 다. CK-MB를 포함한 심근효소의 발병당시 새롭게 상승」

Four narrowings sit on that, and none of them is in the disease name:

- **All three features must be present**, and the 약관 says so twice — 「상기 가.~다. 중 하나
  또는 두 개의 특징만을 가지고 있는 경우 보장에서 제외합니다」 — with two worked negatives, a
  diagnosis on cardiac enzymes alone and a diagnosis on ECG alone [S1 별표4 Ⅱ②].
- **Modern imaging does not qualify as the basis.** A diagnosis founded on 심초음파검사,
  핵의학검사, MRI or 양전자방출단층촬영술 rather than on 가.~다. is excluded [S1 별표4 Ⅱ③];
  [R1]'s version of the clause adds 관상동맥촬영술.
- **All angina is excluded**, named in terms — 안정협심증, 불안정 협심증, 변형협심증, 「모든
  종류의 협심증은 보장에서 제외합니다」 [S1 별표4 Ⅱ④]. [R1] gives the reason plainly: angina
  is KCD **I20** and the covered code is **I21**.
- **The covered code is a single item**, 급성 심근경색증 **I21** [S1 별표4 Ⅱ⑤], where an
  ordinary 급성심근경색증 진단비 rider typically covers **I21–I23** [R1].

What is *not* narrowed is the clinical picture: [R1]'s comparison notes that ECG change plus
enzyme rise is the ordinary basis for diagnosing an infarction — 「이는 일반적인 급성
심근경색증과 동일함」. **The narrowing is the conjunction and the exclusion of imaging-based
and silent infarctions**, which is precisely the case the reinsurer's physician raised in the
2002 design meeting: a myocardial infarction can be discovered incidentally at a health check
with no symptoms the patient ever noticed, and a code-based trigger would have to pay for it
[R1].

### 중대한 뇌졸중 — and the 25% disability gate

This is where the product's dispute record lives. [S1] 별표4 Ⅲ:

> 「"중대한 뇌졸중"이라 함은 지주막하출혈, 뇌내출혈, 기타 비외상성 두개내 출혈, 뇌경색증이
> 발생하여 뇌혈액 순환의 급격한 차단이 생겨 그 결과 영구적인 신경학적 결손(언어 장애,
> 운동실조, 마비 등)이 나타나는 질병을 말합니다.」

and then the clause that decides almost every claim:

> 「'영구적인 신경학적 결손'이란 주관적인 자각증상(symptom)이 아니라 신경학적인 검사를
> 기초로 한 객관적인 신경학적 이상소견(sign)로 나타난 장애로서 장해분류표에서 정한
> "신경계에 장해가 남아 일상생활 기본동작에 제한을 남긴때"의 **지급률이 25% 이상인
> 장해상태**」 [S1 별표4 Ⅲ②]

**The disease scope is not narrowed at all.** 지주막하출혈 **I60**, 뇌내출혈 **I61**, 기타
비외상성 두개내출혈 **I62**, 뇌경색증 **I63** — the same range an ordinary 뇌출혈·뇌경색
rider covers, and *wider* than the GI products that stop at I62 [R1] [R9] [S4]. **The
narrowing is entirely the 25% gate**, and [R1] says so: 「중대한 뇌졸중은 일반적인 뇌졸중의
범위와 크게 다르지 않으나, 영구적인 신경학적인 결손(장해지급률 25% 이상) 조건이 요구되기
때문에 영업현장 및 고객의 입장에서 이해가 쉽지 않은 측면이 있다」 [R1].

Diagnostic basis: CT, MRI, 뇌혈관조영술, PET, SPECT or 뇌척수액검사, showing findings
**새롭게 출현** at onset and **consistent with** the permanent deficit; a diagnosis on CT
alone, or on the deficit alone, is excluded [S1 별표4 Ⅲ③④]. Excluded absolutely: **일과성
허혈 발작 (TIA)** and **가역적 허혈성 신경학적 결손 (RIND)** — the 약관's glossary fixes both
numerically, TIA resolving within **24 hours** and RIND after 24 hours but within **one
week** — and any 뇌출혈/뇌경색 caused by trauma, by a brain tumour, as a complication of
brain surgery, or by occlusion of the **안동맥** (ophthalmic artery) [S1 별표4 Ⅲ⑤].

**The gate is a supervisory parameter, not a carrier one.** It sits in the 장해분류표 that
every Korean life policy carries, which is 부표 3 of the 생명보험 표준약관 at
보험업감독업무시행세칙 [별표 15] [REG-R25]. [S1] 별표3 item 13 defines 「"신경계에 장해를
남긴 때"라 함은 뇌, 척수 및 말초신경계 손상으로 "<붙임>일상생활 기본동작(ADLs) 제한
장해평가표"의 5가지 기본동작 중 하나 이상의 동작이 제한되었을 때를 말한다」 with a headline
range of **10~100%**, and ratings below **10%** are not a recognised disability at all [S1
별표3]. The ADLs schedule, reproduced from [S1] 별표3 with the percentages exactly as
printed:

| Domain | Rating band |
|---|---|
| **이동동작** | 40% / 30% / 20% / 10% |
| **음식물섭취** | 20% / 15% / 10% / 5% |
| **배변·배뇨** | 20% / 15% / 10% / 5% |
| **목욕** | 10% / 5% / 3% |
| **옷 입고 벗기** | 10% / 5% / 3% |

with, at the top of each band [S1]: 이동동작 **40%** — cannot leave the room without
continuous help even with a special aid, or needs continuous help for wheelchair transfer and
movement; **30%** — cannot leave the room without a wheelchair or another person's help, or
cannot walk but can propel a wheelchair unaided; **20%** — cannot walk independently without
crutches or a walker; **10%** — walks unaided but with a limp, cannot manage stairs without a
handrail, or cannot walk 100 m on the flat continuously. 음식물섭취 **20%** — cannot eat by
mouth at all; **15%** — cannot use utensils and cannot eat without continuous help. 배변·배뇨
**20%** — needs continuous help with a stoma or catheter, or has an indwelling catheter,
방광루, 요도루 or 장루. 목욕 **10%** — needs continuous help with all personal hygiene. 옷
입고 벗기 **10%** — needs continuous help to dress and undress upper and lower body.

**The arithmetic of the gate.** The domain maxima sum to 40 + 20 + 20 + 10 + 10 = **100%**.
To reach 25% the claimant must be in roughly one of:

- **이동동작 alone at 30% or 40%** — wheelchair-dependent or worse; or
- 이동동작 **20%** (walker-dependent) plus any one of 음식물섭취 5–15%, 배변·배뇨 5–15%, 목욕
  3–10% or 옷 입고 벗기 3–10% summing to ≥ 5%; or
- a combination of the four non-mobility domains totalling ≥ 25%, which needs impairment in
  at least **three** of them.

**An independently mobile stroke survivor with cognitive impairment and no ADL restriction
scores zero on this table.** That single sentence explains the entire dispute record, and it
is why the CI stroke incidence in the pricing basis is far below the population stroke
incidence.

Two further features of the gate that a projection must respect. **Timing**: 「뇌졸중,
뇌손상, 척수 및 신경계의 질환 등은 발병 또는 외상 후 **12개월** 동안 지속적으로 치료한 후에
장해를 평가한다」, with a further six-month deferral where function is still improving or
death is expected shortly [S1 별표3, 13-나-1)-라)] — so a CI stroke claim is, by
construction, **not assessable for a year**, and on this model's monthly grid the payment
lags the event by one step — one month, where an annual grid made it a year, which remains
well inside the twelve months the 장해분류표 defers the assessment by. And **who assesses**: a 재활의학과, 신경외과 or 신경과 전문의 [S1 별표3]. An
independent loss adjuster records the insurer's working rule as **six months or more of
rehabilitation with an ADL-based rating of 25% or higher** [R16]; that six-month practice
point is the adjuster's, not the 약관's, and is recorded as practice.

The dispute record is almost entirely stroke, and that is what the arithmetic above predicts:
the cancer and infarction definitions are narrow **at the margin** of the distribution, while
the stroke definition is narrow **in the middle** of it, because most strokes leave the
survivor independently mobile. [R10] (2015): a ten-year policyholder with 지주막하출혈 and
surgery, declined because no disability was diagnosed. [R6] (2023): a confirmed 지주막하출혈
with ICU admission below the 25% rating, and a 뇌경색증 with documented cognitive decline
likewise below it. [R16]: a 뇌경색 claim on a 2006 policy — main contract ₩35,000,000, 50%
acceleration ₩17,500,000 — declined for want of a permanent deficit and then paid in full
once a 후유장해진단서 established a permanent ADL restriction. [R7] (2026-04-06): a 뇌경색
claimant fifteen years into a CI policy, using a mobility aid, declined on the ground that
daily living remained possible at some level. **No claim-denial or 부지급률 statistic for
CI보험 was found from any source**; [R1] reports adjusters' perception that it runs "several
times" the rate of ordinary health cover — 「지급심사 담당자들에 따르면 CI보험금 부지급률이
일반적인 건강보험 상품보다 몇 배로 높다고 인지하고 있다」 — but publishes no number [R1].
Against that, [R8] records 금융감독원 as having found no particular mis-selling problem in
the CI sales process — the only regulator statement on CI recovered [R8]. **This is the
single largest quantitative hole in the product's evidence base**, and it bears directly on
any claim-frequency or lapse assumption.

### The remaining five 중대한 질병

[S1] 제3조 defines 중대한 질병 as a closed list of **eight**: 중대한 암, 중대한
급성심근경색증, 중대한 뇌졸중, 말기신부전증, 말기간질환, 말기폐질환, 중증 재생불량성빈혈 and
루게릭병 [S1 제3조①]. The three headline diseases are above; the remaining five, from [S1]
별표4, are all end-stage or code-defined and together carry about **5.3%** of the premium
(footnote 9):

- **말기신부전증 (Ⅳ)** — 「양쪽 신장 모두가 비가역적인 기능 부전을 보이는 말기신질환(End
  Stage Renal Disease)으로서 보존 요법으로는 치료가 불가능하여 혈액투석이나 복막투석을 받고
  있거나 받은 경우」, with 「일시적으로 투석치료를 필요로 하는 신부전증」 excluded [S1].
  **The gate is dialysis in fact**, not a creatinine or eGFR threshold — an unusually
  operable definition by this product's standards.
- **말기간질환 (Ⅴ)** — end-stage liver disease producing cirrhosis and requiring **all
  three** of 영구적 황달, 복수 and 간성뇌병증, confirmed on periodic physical examination,
  blood tests and imaging [S1]. The same conjunction structure as the infarction definition.
- **말기폐질환 (Ⅵ)** — a chronic respiratory-failure state requiring **both** permanent
  oxygen therapy for hypoxia **and** **FEV1.0 ≤ 25% of predicted** on lung-function testing,
  within a 폐질환분류표 of J09–J18, J20–J22, J40–J47, J60–J70, J80–J86 and J90–J99. The 약관
  notes that gas-analysis and spirometry results fluctuate, so the assessment must rest on
  the test best representing the disease course [S1].
- **중증 재생불량성 빈혈 (Ⅶ)** — the most numerically explicit definition in the annex. An
  irreversible severe aplastic anaemia with marrow hypocellularity and peripheral
  pancytopenia, under continuing treatment by transfusion, haematopoietic growth factor or
  immunosuppression, with a specialist's opinion that haematopoietic stem-cell
  transplantation is needed. "Irreversible severe" means marrow **cellularity < 25%** (or
  25–50% with haematopoietic cells < 30%) **and** at least two of 절대호중구수 **< 500/μL**,
  혈소판 **< 20,000/μL** and 교정망상적혈구수 **< 1%** [S1].
- **루게릭병 (Ⅷ)** — amyotrophic lateral sclerosis, defined **by KCD code**: **G12.20**
  (가족성 근위축측삭경화증) and **G12.21** (산발형 근위축측삭경화증), diagnosed by a 신경과
  전문의 on history, neurological examination, blood tests, CSF, muscle biopsy, EMG, cervical
  X-ray, MRI or myelography [S1].

**The list grew over time** and its length is the main axis of product differentiation [R1]:
eight conditions at launch in 2002 (three diseases, three cardiac surgeries, 말기신부전,
장기이식수술); eleven from 2003 with 말기간질환, 말기폐질환 and 중대한 화상; LTC added as a
covered state from 2008; thirteen in one carrier's 2013 Stage product [R13]; and by the GI
generation a "17대 질병" menu folding in 중증루프스신염, 중증세균성수막염, 다발경화증 and
원발성폐동맥고혈압 [S4]. [S5] records one product widening 「보장 대상 질병/수술 기존
28개에서 45개로」 — a count that must include riders, since no main contract in the retrieved
set names more than 21 [S5].

### 중대한 수술 and 중대한 화상 및 부식

[S1] 제4조 and 별표5 define **four** surgeries, and the drafting is uniformly hostile to
catheter-based technique:

- **관상동맥(심장동맥)우회술** — CABG performed by **개흉술** with an autologous graft
  (대복재 정맥, 내유동맥) anastomosed distal to the stenosis. Excluded in terms:
  **관상동맥성형술 (PTCA), 스텐트삽입술, 회전죽상반절제술** and any catheter or
  non-thoracotomy procedure [S1].
- **대동맥인조혈관치환수술** — by 개흉술 or 개복술, and must **both** excise the aortic
  lesion **and** replace it with an artificial graft. 대동맥 means the thoracic or abdominal
  aorta only; branch arteries are excluded, as expressly is **경피적 혈관내 대동맥류수술
  (EVAR)** [S1].
- **심장판막수술** — 개흉술 **and** 개심술, then either complete excision and replacement
  with a prosthetic or bioprosthetic valve, or valvuloplasty. Excluded: catheter procedures,
  expressly **경피적 판막성형술**, and anything not involving both thoracotomy and open heart
  [S1].
- **5대장기이식수술** — transplantation of 간장, 신장, 심장, 췌장 or 폐장 from another person
  into a recipient in chronic organ failure, at a government-recognised transplant
  institution. **랑게르한스소도세포이식수술** (islet-cell transplantation) is excluded [S1].

**This is a quantifiable morbidity effect, not a drafting nicety**: the excluded percutaneous
techniques are now the majority of coronary and aortic intervention, so the surgery triggers
have drifted steadily out of the money since 2002 without a word of the 약관 changing. The GI
generation reacts by adding the excluded procedures back **as riders** — one carrier pairs
관상동맥우회술 with 관상동맥성형술, 대동맥류인조혈관치환수술 with 경피적대동맥류 중재술, and
심장판막수술 with 경피적심장판막 성형술 [S5]. Note that the four surgeries survive into GI
**unchanged**: GI de-defines diseases, not surgeries [S4].

**중대한 화상 및 부식 (별표6)** — third-degree burns or chemical corrosion over **20% or more
of total body surface**, measured by the **Rule of 9's**, the **Lund & Browder** chart or an
equivalent standardised chart [S1 별표6]. Its cover starts on the **계약일**, not after the
90-day wait [S2 별표1 주1]. It is neither a disease nor a surgery and is the one trigger [S4]
carves *out* of its first-year halving [S4].

### 장기요양상태 — a statutory trigger inside a private contract

CI and LTC were welded together in **2008**, when one carrier added 일상장해상태 and 중증치매
to its CI product because standalone LTC would not sell: the buying ages were too young, the
state was hard to explain, and the premium was too small to pay a meaningful commission [R1].
「장기간병 상품 단독으로는 성공하지 못하였으나 CI와 결합하여 판매한 장기간병담보는 성공적으로
안착하게 되었다」 [R1]. In the same year the private definition was **realigned to the public
scheme** [R1], and [S1] shows the modern result:

> 「"장기요양상태"라 함은 「만 65세 이상 노인」 또는 「노인성 질병을 가진 만 65세 미만의
> 자」로서 거동이 현저히 불편하여 장기요양이 필요하다고 판단되어 **노인장기요양보험법에 따라
> 등급판정위원회에서 장기요양 1등급 또는 장기요양 2등급으로 판정받은 경우**」 [S1 제6조]

**There is no medical definition in the contract at all.** The trigger is a *public
administrative decision*, and 노인성 질병 is defined by 대통령령 — a closed list of 25
diseases with KCD codes, four dementia codes, one Alzheimer code, fourteen cerebrovascular
codes, four Parkinson-family codes plus 척수성 근위축, 다발경화증, 중풍후유증 and 진전 [S1
제6조] [REG-R55 별표 1](#krlib-reg-r55). The grades themselves are point bands set by 노인장기요양보험법
시행령 제7조제1항: **1등급** at 장기요양인정 점수 95 or more, **2등급** at 75 to under 95,
with 3–5등급 and 인지지원등급 below that [REG-R55]. Underneath the grade sits a statutory
duration test — 장기요양급여 is for a person 「**6개월 이상** 동안 혼자서 일상생활을 수행하기
어렵다고 인정되는 자」 [REG-R54 제2조제2호](#krlib-reg-r54) — which is the natural definition of a disability
inception for a three-state model.

Two consequences. **The benefit definition belongs to a statute, so it moves when the statute
moves**, and the private insurer has no control over the incidence of its own trigger; the
only definitional freedom the contract retains is which grades it pays on and how much. And
**the trigger shares the CI benefit**: it is not an additional payment but another way into
the same acceleration, subject to the same once-only rule and its own 90-day 보장개시일 with
the 재해 carve-out [S1 별표1 주2]. The same 1·2등급 trigger is carried into the GI generation
[R11], so this is one of the few parameters the CI → GI transition left alone.

For the incidence basis, `LTC_KR_S` is the library's home for the 등급별 인정자 statistics
[REG-R42] [REG-R43] and, on its own primary sources, for a **disclosed** 요양 1·2등급
발생률 grid at ages 40, 50 and 60 by sex — so a Korean 1·2등급 inception rate at insured ages
*is* published, in a 상품요약서, and this product does not use it. `CI_KR_S` runs a **[std]**
ramp of its own instead, nil below 65 and calibrated only to the order of magnitude implied by
[REG-R42]; the consequence, stated in `technical-notes.md` rather than hidden, is that the
장기요양 limb of this model's CI decrement is **nil at every insured age below 65** where the
sister product's disclosed rates are not. The earlier *private*
definitions are recorded for context in the research file — a 1992 product borrowed from
Japan paying on bed-boundedness plus restriction in 3 of 4 ADLs, relaxed to 1 of 4 in 2003,
which raised the incidence and the price and did not sell [R1]; and a 중증치매 rider
requiring CDR **3점 이상** persisting **90일 이상** after a **2-year** waiting period [S3].

### 보장개시일, the first year, and the absence of a survival period

Three timing rules govern when cover attaches, and they are the most invariant parameters in
this file.

**The 90-day wait applies to 중대한 암 alone, and it is drafted as a coverage start date
rather than as an exclusion.** [S1]: 「"CI/LTC보험금"중 "중대한 암"의 보장개시일은
계약일(부활(효력 회복)일)부터 그 날을 포함하여 **90일이 지난날의 다음날**」 [S1 제7조] [S1
별표1 주1]. The other seven 중대한 질병, the four 중대한 수술 and 중대한 화상 및 부식 are
covered from the 계약일 [S1] [S2 별표1 주1]; 장기요양상태 has its own 90-day wait with the
재해 carve-out [S1 별표1 주2]. [S2] words the same thing as a single 「중대한 질병 및 수술
보장개시일」 at 90 days with the burn carved back to the 계약일 [S2]; [S3]'s 2011 wording is
the same 90 days, again excepting the burn [S3]; [S4]'s GI product calls it 「암 보장개시일」
and uses the same 90 days [S4]. **The 90-day cancer wait is invariant across every document
retrieved.**

**Two consumer protections ride on it**, and both are unusual enough to specify. If 중대한 암
is diagnosed before the 보장개시일 the policyholder may **cancel the contract and recover the
premiums** [S1 제7조⑤]. If the policyholder does not cancel, the pre-inception cancer is
permanently outside cover — 「동일하거나 다른 신체기관에 재발 또는 전이되어 "중대한 암"으로 …
지급사유가 발생한 경우라도 CI/LTC보험금을 지급하지 않으며, 보험료의 납입을 면제하지
않습니다」 — **but cover revives** if five years pass from the 보장개시일 with no further
diagnosis (routine screening excluded) or treatment for it: 「「중대한 암 보장개시일」부터
5년이 지난 이후에는 보장하여 드립니다」 [S1 제7조⑥] [S1 별표1 주5]. The identical five-year
revival applies to 장기요양상태 [S1 별표1 주6]. Note the second limb of the exclusion: the
pre-inception cancer suspends **the premium waiver as well as the benefit**, so a
policyholder in that position pays premiums on cover they cannot claim.

**감액기간.** The composite halves the acceleration for **breast cancer in the first policy
year** only: 40% instead of 80%, with the residual death benefit rising to 60% [S1 별표1] [S2
별표1]. The alternative all-trigger halving is a flag — see footnote (14).

**No survival period.** Nothing in any retrieved Korean CI document requires the insured to
survive the CI event for any period [R1]. A model that imports the overseas 30-day
requirement would understate the CI decrement and overstate the death decrement by the same
lives.

### 납입면제 — and why it is not an independent decrement

[S1] waives all future 기본보험료 on **either** of two events during the premium-paying
period: a disability state of **50% or more** on the 장해분류표, aggregated across several
body parts from one accident or one non-accidental cause; **or any CI/LTC보험금 지급사유**
[S1 별표1 주4] [S1 제7조]. Because a CI event triggers the waiver, **the waiver and the
acceleration fire together in essentially every CI claim**, and on this chassis the waiver is
therefore not an independent decrement. That is a genuine simplification relative to the
chassis, where the waiver is a separate disability trigger sitting alongside death.

Three deltas nonetheless remain and have to be modelled. The **50% 장해** limb fires without
a CI event and is a real, if second-order, decrement — the same 장해분류표 percentage scale
the chassis uses [REG-R25], not a binary trigger. The **"deemed paid" rule** the chassis
specifies carries over: a waived policy accrues surrender value on the full premium scale
while paying nothing, so on a suppressed contract the waiver is the only route to the cliff
without paying. And the **pre-inception cancer carve-out** above suspends the waiver as well
as the benefit [S1 제7조⑥].

The waiver is also the feature the market competed on hardest after CI lost the argument on
definitions. [S3]'s universal version splits the two thresholds, waiving on 50%–80%
disability or a CI event and **terminating** the contract at 80% or more, because on that
product an 80% disability is itself a death-benefit trigger [S3]. [S4]'s GI product widens
the waiver well beyond its own acceleration: it fires on a 50%+ disability **or** on 암
including 특정암 (breast and prostate, which are *not* accelerated on that product), 뇌출혈,
급성심근경색증, 중증질환, 중대한 화상 및 부식, or a 중대한 수술 — expressly excluding
기타피부암, 갑상선암 (other than 중증갑상선암), 대장점막내암 and 비침습방광암 [S4]. One
carrier advertises **25** distinct waiver triggers [R11]. **A modern Korean accelerated
product therefore has two trigger sets of different widths — a narrow one for the money and a
wide one for the premium waiver** — and a model that uses one rate for both is wrong on the
second.

### 해약환급금 on a CI chassis — the cliff, and the second exit from it

The chassis specifies the surrender value in full: `W(t) = max(0, V(t) − SC(t))` on the
표준형 twin, with `SC(t)` bounded by the statutory 표준해약공제액 [REG-R20] and running off
inside seven years [REG-R19]; and `CV(t) = k × W(t)`, where the factor multiplies **the twin,
not the sold product's own account**. [S3] states the same identity in a CI product's own
words — 「보험료 계산시 적용한 위험률로 산출한 **순보험료식 책임준비금**에서
**미상각신계약비(해지공제액)**를 공제한 금액을 해지환급금으로 지급합니다」 [S3] — and [S1]'s
약관 sends the calculation to the 산출방법서, a filed but unpublished 기초서류 [REG-R2]. [S2]
names its twin **기본형** where the chassis's carriers name theirs 표준형 or 일반형; it is
the same non-marketed comparison product priced with the lapse assumption switched off. On
this product the payable value is

    CV(t) = k(t) * W(t),   k(t) = 0.50  while  t < m  and no CI/LTC 지급사유 has occurred
                           k(t) = 1.00  otherwise

**and there are therefore two exits from the suppression, not one: 납입완료, and a CI/LTC
지급사유.** The second is the CI-specific delta and it is contractual, conditioned in [S2] on
「제7조 … 제2호의 CI/LTC보험금 지급사유가 발생하지 않은 경우」 [S2] and in [S4] on 「「선지급
진단보험금」 지급사유 발생 전 납입기간 동안」 [S4]. As on the chassis, the step is **not** a
surrender-charge effect: the 해약공제기간 is capped at seven years [REG-R19], so on a 20년납
contract the charge is fully amortised by duration 7, thirteen years before 납입완료 and, on
most lives, before any CI event.

**The interaction is the sharpest single fact in this section.** On the chassis, the
suppressed period and the premium-paying period coincide exactly, so the cliff is a
deterministic function of duration and the model can place it at `t = m`. Here the cliff is
at `min(m, t_CI)` — a **random** date, correlated with the decrement the product is built on.
Three consequences follow, and each is a modelling requirement rather than a nicety:

1. **A surrendering post-CI policyholder is paid the full 표준형 value**, so the surrender
   strain on the post-CI cohort is materially larger than on the pre-CI cohort at the same
   duration. A projection that applies one surrender-value scale to a single aggregate policy
   count understates outgo.
2. **The policy loan available jumps at the same date** (footnote 15), because it is computed
   off the payable value.
3. **The premium waiver fires at the same date too**, so from `t_CI` the contract pays no
   premium, holds a full-value surrender right, and owes only the residual death benefit.
   That combination is what makes the post-CI state a genuinely different liability rather
   than a scaled-down version of the pre-CI one, and it is why `CI_KR_S` carries the two
   states separately rather than netting the acceleration off the death benefit.

The chassis's **"waived premiums count as paid"** rule reinforces the carve-out rather than
duplicating it: waived months count toward the surrender-value computation, so even without
the carve-out a post-CI policyholder would reach 납입완료 without funding it. The two rules
together mean **a CI claimant is never worse off on surrender than a 표준형 policyholder at
the same duration**, which is a consumer-protection design and not an actuarial accident. The
chassis's **clawback** — unpaid premiums in the suppressed period must be made good before
the post-cliff basis applies — is stated in neither CI 약관, and whether it also gates the CI
carve-out is **[unverified]**; `CI_KR_S` assumes it does not, and says so.

**The suppression is a haircut on one underlying value, not a second reserve run.** The
chassis establishes this from published grids on which the suppressed and 표준형 products
have *identical* surrender values from 납입완료 onward, and on which the suppression ratio is
exact at every earlier duration. `CI_KR_S` therefore needs one `W(t)` and one multiplier, and
— the consequence the chassis draws and this product inherits — `CV(t)` is **independent of
the sold form's own premium**, which is the whole of the 환급률 arithmetic that sells the
form.

**The price of the suppression** is 9–12% of premium on [S4]'s published pair (see
*Premiums*), against "up to 30%" claimed for one carrier's variant [S5]. A model that
suppresses the value without discounting the premium mis-prices the product.

**What the suppressed form is legally.** It is not a contractual gimmick but a **regulatory
dispensation**: 감독규정 제7-66조제4항 permits an insurer to pay less than the
별표-14-floored surrender value on a 순수보장성보험 **whose premiums were calculated using a
최적해지율** — a best-estimate lapse rate [REG-R19]. The permission is conditional on having
used one, which is why the lapse assumption on this product is a supervisory matter and not
only an earnings one. Two limits ride on the permission and both bind here: a **변액보험 may
never use it** (제7-66조제4항제1호), and where the surrender value during the payment period
is under 50% of an otherwise identical 표준형's, the post-payment value must exceed 50% of
the 표준형's **and** the post-payment 환급률 must exceed the greater of 100% and the 표준형's
환급률 [REG-R19] [REG-R28]. The composite's 50% suppression sits exactly at that threshold.

### The lapse assumption, and why it is not free

The chassis specifies the lapse basis and this product inherits it, but the inheritance is
worth restating because it is the one assumption a Korean supervisor has written down. The
**IFRS17 주요 계리가정 가이드라인** of 2024-11-07 adopts the **로그-선형 (log-linear) 모형**
as the 원칙모형 for 무·저해지 lapse rates, converging to **0.1%** at 납입완료, with a
post-완납 ultimate rate of **0.8%**; departure from the 원칙모형 is permitted only within a
closed list of alternatives and only on disclosure, in the audit report and the 경영공시, of
the CSM, best-estimate liability, K-ICS and net-income differences against the principle
model, plus quarterly reporting to the FSS and an on-site inspection [REG-R27] [R3].
`CI_KR_S` uses the principle model, tagged **[std]** with that entry as its rationale, and
carries a switch to a 표준형 assumption so the two can be compared — which is exactly the
comparison the guideline requires an insurer to disclose.

The problem the supervisor named applies to this product with particular force. Because there
is no experience on 무·저해지 business, insurers assumed high lapse right up to 완납, which
flatters profitability; the resulting switching out of 표준형 products raised observed 표준형
lapse, which was fed back into the 무해지 assumption — 「악순환」 [REG-R27]. The 무·저해지
share of 보장성 first-year premium ran 11.4% (2018) → 30.4% (2021) → 47.0% (2023) → **63.8%
(2024 H1)** [REG-R27], so this is the majority of the Korean protection market.

**No CI lapse experience of any kind was retrieved** — [R1] gives one cession ratio and no
lapse data at all — so every duration-by-duration lapse rate in `CI_KR_S` is **[std]**
bounded by [REG-R27]. What the chassis *does* supply is a real bound from Korean disclosure:
상품요약서 publish the **적용해지율** used in pricing, in envelope form, and one carrier's
protection product discloses 0%–13.4% during the payment period and 1.0%–11.3% after it,
against 1%–10% at another. That post-완납 range is far above the supervisor's 0.8% reference,
and the gap is the subject of [REG-R27].

### Premium provisions, and the risk-rate revision right

Premiums are level and guaranteed for 납입기간 [S1] [S3] [S4], with the exception that the
**예정위험률 may be revised from five years after the contract**, with 금융위원회 approval;
where the change raises the premium or the reserve, the insurer applies the increase by
**reducing the benefit or the sum assured** unless the policyholder pays the increase over
the remaining premium term, or in a lump sum where paid up [S3]. That is a real, unmodelled
optionality in the liability, and it is worth naming precisely because it is asymmetric: the
policyholder's default position on an unaffordable increase is a **reduced sum assured**, not
a lapse, so the exercise of the right shows up as benefit erosion rather than as a decrement.

The rates it applies to are 예정위험률 — **pricing rates carrying a safety margin, not
best-estimate experience.** [R1] records the margin regime: 안전할증 on the 기초발생률 was
capped at **30%** in the early 2000s, raised to **50%** by the 2015 보험산업 경쟁력 강화
로드맵, and the cap was **removed from 2017** [R1]. Any best-estimate basis derived from a
disclosed 예정위험률 is therefore a **[std]** adjustment and must say so.

Two statutory comparison metrics are published alongside the premium and are the closest
thing to an expense disclosure this product provides. **보험료지수** — the ratio of the
office premium to the 표준순보험료 computed on the 금융감독원's prescribed rates and interest
— is **130.1%** on the 80% form and 130.9% on the 50% form at 남 40세 월납 [S3]. And
**보장위험별 연간보험료** splits the annual comparison premium by benefit [S3], 월납, 남자
40세:

| Product / benefit | 연간보험료 | 기준보험금 |
|---|---|---|
| **50% 선지급형**, CI 진단 | ₩165,419 | 1,000만원 |
| 50% 선지급형, CI 진단 전 사망 (80%+ 장해 포함) | ₩79,002 | 1,000만원 |
| 50% 선지급형, CI 진단 후 사망 | ₩82,715 | 1,000만원 |
| **80% 선지급형**, CI 진단 | ₩164,025 | 1,000만원 |
| 80% 선지급형, CI 진단 전 사망 | ₩78,336 | 1,000만원 |
| 80% 선지급형, CI 진단 후 사망 | ₩82,019 | 1,000만원 |

**This is the most useful single table in this file for a pricing model, and it must be read
with care.** On the 50% form the three components sum to ₩327,136 per 1,000만원, of which the
CI acceleration is ₩165,419 — **50.6%**. Scaling by ten to the illustration's 1억원 basis
gives ₩3,271,360 a year against the illustration's actual first-year 납입보험료 of
₩3,308,400, a residue of ₩37,040 attributable to a 1,000만원 rider: the disclosure is
internally consistent, and it says plainly that **on a 50% acceleration at male 40, half the
risk cost is the CI benefit and half is the death benefit.** The same scaling does **not**
work on the 80% rows — ₩324,380 × 9 = ₩2,919,420 against that illustration's ₩3,313,200,
leaving a residue ten times too large for the same rider — so the 연간보험료 disclosure is a
**per-benefit comparison metric and not a decomposition of the office premium** on that form.
The 80% rows are reproduced as published and used only for the *relativities* between the
three components, never for a level. The 약관's own definitions support that reading:
연간보험료 is 「1년동안 위험보장을 받는데 필요한 영업보험료」, meaningful only for comparing
carriers, and 「납입보험료와 직접적인 관계가 없습니다」 [S3].

### The morbidity basis — a disclosed Korean CI incidence table

[S3] publishes the product's **예정위험률**, per annum, by sex at ages 20, 40 and 60. **This
is the only disclosed Korean CI morbidity basis found**, and no published 참조순보험요율
reaches it. 보험개발원 *does* publish a dated **장기손해보험 참조순보험요율** display, carrying
a 「기타피부암 및 갑상선암 이외의 암 발생률」 grid and a 질병입원율 grid [REG-R61] — the
first is what `Cancer_KR_S` sources its incidence from — but it is stated on the
insured-cancer definition, which is not the 중대한 암 definition and carries no 중대한 질병
item, so it is not a check on these rates. The **life** 참조순보험요율 is filed with the FSC
and never published, and becomes visible only as the 보험가격지수 ratio [REG-R4] [REG-R34].
It is reproduced exactly [S3]:

| 예정위험률 (연) | 남20 | 남40 | 남60 | 여20 | 여40 | 여60 |
|---|---|---|---|---|---|---|
| 예정 경험 사망률 | 0.00051 | 0.00068 | 0.00290 | 0.00027 | 0.00068 | 0.00290 |
| 중대한 암 발생률 | 0.000144 | 0.001023 | 0.011063 | 0.000291 | 0.002220 | 0.006010 |
| 중대한 급성심근경색증 발생률 | 0.000027 | 0.000589 | 0.004371 | 0.000009 | 0.000148 | 0.001814 |
| 중대한 뇌졸중 발생률 | 0.000038 | 0.000907 | 0.003999 | 0.000040 | 0.000399 | 0.002764 |

**Health warning on the mortality row.** The female values at 40 and 60 extract identical to
the male values (0.00068 and 0.00290), which is not plausible for a Korean life table and is
almost certainly a column-merge artefact of the PDF extraction. The three morbidity rows are
fully differentiated by sex and are treated as sound; **the female mortality rates at 40 and
60 are [unverified] and must not be used** [S3].

What the morbidity rows say, computed here:

| Quantity | 남20 | 남40 | 남60 | 여20 | 여40 | 여60 |
|---|---|---|---|---|---|---|
| Sum of the three CI rates | 0.000209 | 0.002519 | 0.019433 | 0.000340 | 0.002767 | 0.010588 |
| Ratio to the death rate | 0.41 | **3.70** | **6.70** | 1.26 | (4.07) | (3.65) |
| Female / male CI ratio | | | | **1.63** | **1.10** | **0.54** |

Three facts follow and all three shape the model.

**CI incidence dominates mortality on this chassis.** At male 40 the CI decrement is **3.7×**
the death decrement; at male 60, **6.7×**. That is why the CI benefit takes half the risk
premium at a 50% acceleration despite paying only half the sum assured [S3], and it is why a
projection of this product is a morbidity projection with a mortality tail rather than the
reverse. (The female ratios in parentheses use the suspect mortality row and are indicative
only.)

**The sex crossover in 중대한 암 is the product's defining experience feature.** At 40 the
female rate is **2.17×** the male (0.002220 against 0.001023); at 60 it is **0.54×**
(0.006010 against 0.011063). The young-female excess is breast and thyroid cancer — exactly
the exposure that broke the 2002 pricing [R1] — and it is why breast cancer alone carries the
first-year halving in [S1].

**The age slopes are steep, and they are not constant.** Male 중대한 암 rises ×7.1 from 20 to
40 (0.001023 / 0.000144) and ×10.8 from 40 to 60 (0.011063 / 0.001023) — cancer is the one
cause whose log-slope *steepens* with age, where male AMI runs ×21.8 then ×7.4 and male
stroke ×23.9 then ×4.4, both flattening. 중대한 급성심근경색증 is the most male-skewed cause
(4.0× at 40, 2.4× at 60); 중대한 뇌졸중 is close
to unisex at 20 and runs 2.3× male at 40 and 1.45× at 60. A **[std]** CI incidence
construction for `CI_KR_S` must reproduce those slopes, and `technical-notes.md` states the
interpolation and the extrapolation beyond 60 explicitly.

The narrowness of the 중대한 definitions relative to ordinary 진단비 cover **belongs in this
basis, not only in the prose**, and this table is where it is carried: an ordinary 뇌졸중
진단비 rider pays on the same code range I60–I63 with no severity condition at all, so its
incidence must exceed 0.000907 at male 40 by the whole of the 25% gate's effect. **How much
is not established** — no Korean population stroke incidence was retrieved and no CI
부지급률 statistic exists in any source [R1] — so the gap is a **[std]** calibration in
`technical-notes.md` and not a sourced ratio. The relation, cause by cause:

| Cause | CI trigger | Ordinary 진단비 rider trigger | Where the narrowing sits |
|---|---|---|---|
| 암 | 침윤파괴적 증식, within a positive KCD list, less the exclusions | any C code (일반암), with 유사암 as a reduced tier | C44, C61, C73, melanoma ≤ T2aN0M0, 대장점막내암, D00–D09 제자리암, 경계성종양, 전암상태 |
| 급성심근경색증 | **I21** plus all three of chest pain, new ECG change and newly raised CK-MB | I21–I23 | the conjunction; imaging-based diagnosis; all angina (I20); silent infarction |
| 뇌졸중 | I60–I63 **plus 장해지급률 ≥ 25%** on the ADLs schedule | I60–I63, or I60–I62 on many GI products | the 25% gate alone — the disease scope is not narrowed, and is wider than GI's |
| 말기신부전증 | dialysis in fact | — | no ordinary counterpart; the gate is operable |
| 수술 4종 | open surgery only | catheter procedures covered separately | PTCA, stent, EVAR, 경피적 판막성형술 all excluded |

---

## Riders and options

**In scope (modelled or parameterized):**

- **The acceleration itself** — `선지급 비율` as a model-point flag ∈ {0.50, 0.80}, with the
  residual death fraction its exact complement and the 105% account floor beneath it [S1]
  [S2].
- **저해지환급형** — a model-point flag carrying the suppression factor 0.50, the suppressed
  period, **and the CI-event carve-out that ends it early** [S2] [S4].
- **납입면제** — part of the main contract, not a rider; fires on 장해 50%+ or any CI/LTC
  지급사유, and therefore is not an independent decrement on the CI limb [S1].
- **장기요양상태** — the fourth acceleration trigger, on 노인장기요양 1·2등급, with its own
  90-day wait and the 재해 carve-out [S1] [REG-R54] [REG-R55].
- **First-year 감액** — a flag over {breast cancer only, all triggers}, factor 0.5 [S1] [S2]
  [S4] [S5].
- **보험계약대출** — an available balance computed off the *payable* surrender value and an
  interest accrual; take-up is a **[std]** behavioural assumption [REG-R25 제33조](#krlib-reg-r25).
- **고액계약할인** — a premium scale parameter, 1/2/3% by band [S4].

**Out of scope, and named:**

- **건강인우대특약** (preferred risk) — criteria published, discount not [S4]; a rating
  question rather than a cash-flow one.
- **효도특약** — a 2% office-premium discount on a relationship condition [S4].
- **특별조건부특약** (substandard rating by 할증보험료법) [S3].
- **CI플러스추가보장특약** and the 진단비 riders attached to a CI main contract — [S3]'s
  illustration carries a ₩10,000,000 rider whose annual cost is recoverable at ₩37,040, and
  [R15] records that 갱신형 riders on legacy CI blocks terminate at **80** [R15]. Their shape
  belongs to [cancer (암보험)](../cancer/product-spec.md).
- **중증치매 rider** — CDR 3점 이상 persisting 90일 이상 after a 2-year waiting period [S3];
  belongs to [long-term care (간병보험)](../long_term_care/product-spec.md).
- **The catheter-procedure riders the GI generation added back** — 관상동맥성형술,
  경피적대동맥류 중재술, 경피적심장판막 성형술 [S5]; they are the market's answer to the
  surgery exclusions and are named so that a reader knows the exclusions are commercially
  answered rather than simply endured.
- **중도인출 and 추가납입** — universal-chassis machinery; arguments of the 기본보험금
  formula, held at zero [S1 별표1 주7].
- **연금전환특약** — a 제도성특약 on the chassis, attachable at no extra premium and
  converting the account into an annuity on the rider's own basis. **It appears in no
  retrieved CI 약관**, and its absence makes sense: a contract whose sum assured may already
  have been cut by 80% is a poor annuity source. Recorded as a delta, not as a certainty.
- **감액완납 and 연장정기보험** — absent here as on the chassis, and [unverified] as features
  of any Korean contract.

**The GI boundary.** **GI보험** keeps every mechanic in this document and replaces only the
trigger philosophy: 「진단받은 질병코드를 통해 보험금을 지급함으로써 보험금 지급기준을
CI보험 대비 완화함」 [S5]. It is not a regulatory category but practitioner shorthand, adopted
first by foreign-owned insurers whose agents were used to selling on ICD codes [R1]. **GI does
not simply dominate CI**, and a model should not assume it does: GI's cerebrovascular scope is
often *narrower*, covering 뇌출혈 I60–I62 only and leaving 뇌경색 to a rider, where 중대한
뇌졸중 covers I60–I63 behind the gate [R9] [S4] [S5]; its headline disease count is smaller
unless the full 17대보장형 menu is bought; and the four 중대한 수술 survive into it unchanged,
because GI de-defines diseases, not surgeries [S4]. `CI_KR_S` models the **CI trigger set**;
the GI variant is a different incidence table on the same machinery.

---

## Variations across insurers

The observed range is given wherever more than one document states the parameter. The
composite's choices are justified against this table.

1. **Acceleration fraction.** 50% at [S1] [S2] [S3] [S4] [S5] [S6] [R13]; 80% at [S1] [S2]
   [S3] [S4] [S5] [S6]; 100% at [S4] [S5] [R11] [R14]; a policyholder-selected 30–80% on one
   women's product and an age-varying fraction (higher at old ages) at one carrier in 2009,
   both [R1]. Composite: **80%**, with 50% as a flag, and the 100% forms excluded because
   they are not pure accelerations — see *Benefit provisions* footnote (13).
2. **What remains payable on death.** The complement of the fraction, floored at **105%** of
   the 계약자적립금 [S1]; the same complement floored at **110%** [S3]; nil plus a 유족위로금
   of 1% of the sum assured monthly for 30 months [S4]; nil plus a 30% annuity to the family
   [R14]; a flat 30% at one carrier [S5]. Composite: **the complement with a 105% account
   floor**, the multiplier parameterized because two values are observed.
3. **First-year reduction.** Breast cancer only, ×½ [S1] [S2]; all triggers, ×½ [S4] [S5];
   none stated [S3]. **Where it exists it always halves** — the depth does not vary, only the
   scope. Composite: breast cancer only, as a flag.
4. **중대한 암 waiting period.** 90 days at [S1] [S2] [S3] [S4]. **No variation.**
5. **Other CI waiting periods.** None — cover from the 계약일 at [S1] [S2] [S3] [S4]. **No
   variation.** 장기요양상태's own 90 days with the 재해 carve-out rests on one source [S1].
6. **중대한 뇌졸중 gate.** 장해지급률 **25% 이상** at [S1] [S6] [R1] [R6] [R9] [R10]. **No
   variation**, and it could not vary without leaving the statutory 장해분류표 [REG-R25].
7. **중대한 수술.** The same four everywhere — CABG, 대동맥인조혈관치환, 심장판막,
   5대장기이식 — each requiring open surgery and each excluding the catheter technique [S1]
   [S2] [S4] [S5]. **No variation.**
8. **Number of 중대한 질병 in the main contract.** 8 at launch in 2002 including surgeries
   [R1]; 11 from 2003 [R1]; 8 diseases + 4 surgeries + burn at [S1] [S2]; 13 at [R13]; 17 at
   [S4] [R14]; 18 + 3 at [R11]; "45 질병/수술" including riders at [S5]. Observed range in
   the main contract: **8–17**. Composite: [S1]'s list, which is the CI generation's settled
   shape.
9. **중대한 암 exclusions.** The modern list — early melanoma ≤ T2aN0M0, C44, C61, C73,
   대장점막내암, 제자리암, 경계성종양, 전암상태, pre-inception recurrence — is settled [S1].
   An older wording adds an HIV-related malignancy exclusion and "초기갑상샘암" [S6] [R1];
   the HIV item is a legacy of the 2002–2007 drafting and is not carried into the composite.
10. **LTC trigger.** 노인장기요양 **1등급 or 2등급** [S1] [R11]; earlier private ADL/CDR
    definitions at [R1] and [S3]. Public grades since 2008. Composite: 1·2등급.
11. **가입나이.** 만 15세–60세 at [S3] [S4] [R13]. **No variation.**
12. **가입한도.** 50%형 2,000만–1억5,000만원 and 80%형 1,000만–9,000만원 at [S3]; a 2억원
    maximum with 1억6천만원 accelerated at [R1]; 1억원 quoted on the 80% form at [S4]; dead
    bands around the discount thresholds at [S4]. Ceiling range **9,000만–2억원**. Composite:
    the cap binds the **accelerated** exposure — footnote (4).
13. **납입기간 menu.** 일시납, 5/10/15/20년납, 55/60/65/70/80세납 [S3]; 5–30년납 in fives and
    55–80세납 [S4], with 5년납 and 10년납 on the 기본환급형 only. Composite: 20년납.
14. **Surrender-value form.** 기본형 [S3]; 30% 저해지 and 50% 저해지 [S2]; 해지환급금이 적은
    유형 [S4]; 저해지 30%형 [R11]; 해약환급금일부지급형 up to 30% cheaper than the 표준형
    [S5]. Observed suppression: **30%–50% of the 기본형 value in the paying period**.
    Composite: 50%, with the CI-event carve-out, which is stated at both carriers that
    publish the form on a CI product [S2] [S4].
15. **저해지 premium discount.** 9–12% computed on [S4]'s published pair; "up to 30%" at one
    carrier [S5]. Composite: the computed 9–12%, because it is the only figure derived from
    two published scales for the same cell.
16. **최저보증이율.** 연복리 **4.0% flat** in 2011 [S3]; **1.5% for ten years then 0.5%** in
    2019 [S1]. The guarantee collapsed over the decade, and any CI in-force projection has to
    carry that stratification by vintage.
17. **예정이율.** 4.0% for the protection element in 2011 [S3]; about 2.75% on a 2019 종신
    illustration basis [S4]. Observed **2.75%–4.0%** on CI documents, against the chassis's
    2.25%–2.75% on 2021–2025 documents. Composite: **2.50%**, the chassis's mid-point,
    inherited unchanged — footnote (11).
18. **기본보험금 floor multiple on the 계약자적립금.** 105% [S1]; 110% [S3]. Composite: 105%,
    parameterized.
19. **고액계약할인.** 1/2/3/5/6% by band from 3,000만원 in 2011 [S3]; 1/2/3% from 7,000만원
    in 2019 [S4]; 3~4% at 1억원 and a 5,000만원 threshold at two carriers [S5]. **Shallower
    over time.** Composite: [S4]'s scale.
20. **납입면제 trigger.** 장해 50%+ or any CI/LTC event [S1] [S2]; 장해 50–80% or a CI event,
    with 80%+ terminating the contract [S3]; 장해 50%+ or any of 암 including 특정암, 뇌출혈,
    AMI, 중증질환, 화상, 중대한 수술 [S4]; "25 triggers" [R11]. **Widening steadily**, and by
    the GI generation the waiver trigger set is materially wider than the acceleration
    trigger set. Composite: [S1]'s pair, with the widening named.
21. **Trigger philosophy.** 약관 정의 (CI) [S1] [S2] [S3] [S6]; KCD code (GI) [S4] [S5] [R9]
    [R11]; staged (SI) [R13]; wide-scope code (WI) [R12]. **Four generations coexist in the
    market**, and legacy CI blocks remain large enough to be a standing consumer-advice topic
    in 2024 [R15] and a live complaint topic in 2026 [R7]. Composite: CI.
22. **What does not vary.** Six things are identical in every document retrieved and are the
    product's fixed spine rather than choices: (1) the CI benefit is an **acceleration of the
    death benefit**, paid **once only** across all triggers, with the death benefit reduced
    by exactly what was paid; (2) the 중대한 암 waiting period is **90 days** from 계약일 or
    부활일 and applies to cancer alone; (3) 중대한 뇌졸중 requires a **장해지급률 25% 이상**
    on the 표준약관's ADLs schedule; (4) 중대한 급성심근경색증 requires **all three** of
    typical chest pain, new characteristic ECG change and newly raised cardiac enzymes
    including CK-MB, with all angina excluded and the covered code **I21** alone; (5) the
    four 중대한 수술 are CABG, aortic graft replacement, heart-valve surgery and five-organ
    transplantation, each requiring open surgery and each excluding the catheter technique;
    (6) **no survival period** is required anywhere. Every one of these is a fact a model can
    rely on without a [std] tag.

---

## Regulatory context

**Classification and the licensing line.** The main contract is 생명보험 under 보험업법
제4조제1항제1호 and the health element is 제3보험 under 제4조제1항제3호 — 상해보험, 질병보험,
간병보험 — which 제4조제3항 deems a fully licensed life insurer *or* a fully licensed
non-life insurer to hold [REG-R1] [R4]. The asymmetry that decides this product's shape is
not in 제3보험 at all: it is that a 손해보험회사 may not write 질병사망 as the 주보험, so it
cannot build an acceleration and must sell the same disease list as **독립급부 특약** on a
통합보험 [R1]. **The Korean CI product is therefore a life-insurer instrument by operation of
the licensing rules**, and the non-life market's answer to it is a structurally different
product that this library models separately.

**Product-design rules that bind this contract.** Three articles of 감독규정 제7-60조 reach
it directly [REG-R16]. **제8호** — a contract must not be extinguished while the risk it
covers remains effective — is why the contract survives its own acceleration. **제9호** — the
death benefit must be at least cumulative premiums paid, except where the payment period ends
at age 80 or below — is mirrored by [S1]'s 기본보험금 floor, though the exception means the
rule does not strictly bite on the anchor cell. **제10호** — a 금리연동형보험 must set a
최저보증이율 — is why [S1]'s interest-sensitive variant carries the 1.5%/0.5% ladder. One
제3보험 rule is worth naming for what it does *not* do here: 감독규정 제7-63조제1항제1호
requires a 제3보험 product to pay the 계약자적립액 on **death from a cause the policy does
not cover** and terminate [REG-R17], which is a first-order modelling requirement for
`Cancer_KR_S`, `LTC_KR_S`, `Medical_KR_S` and `Child_KR_S` — and does not bite on this main
contract at all, because a CI contract covers death from any cause. It bites on the 제3보험
riders attached to it.

**The surrender-value regime is the chassis's, and it reaches this product by
cross-reference.** 감독규정 제7-69조 and 제7-70조 apply 제7-65조 through 제7-68조 to
장기손해보험 and to **제3보험** *mutatis mutandis*, so **one surrender-value regime governs
all ten `krlib` products** [REG-R19] and this document does not re-derive [별표 14]. Two
things about it are CI-specific and both are stated above rather than here: the 보험가입금액
that enters the 표준해약공제액 is the **pre-acceleration** death benefit, by [별표 15] 제3호
read with 제8호 [REG-R21] (*Termination and values* footnote 17); and the cap at this
product's anchor works out at about **₩3,940,000**, against **₩3,987,620** on the FSC's
13-times-monthly-premium rule of thumb — a 1.1% agreement between two independent statements
of the same cap, tighter than the chassis's own 4% [REG-R20] [REG-R29]. The 무·저해지
permission of 제7-66조제4항 and its 환급률 cap are set out in *Contractual mechanics*.

**Accounting and solvency, both live.** Korea has run **K-IFRS 제1117호** (the Korean
adoption of IFRS 17) and **K-ICS** (신지급여력제도) together since **2023-01-01**, under the
same 부칙 [REG-R60] [REG-R13]. The chassis sets out the **해약환급금준비금**
(*haeyak-hwangeupgeum junbigeum*, surrender-value reserve) that sits on top of them — a
company-level appropriation inside 이익잉여금, a distributable-earnings device rather than a
solvency one, with no counterpart anywhere else in this repository [REG-R11]. **What is
CI-specific is an asymmetry the carve-out creates.** The appropriation test measures the IFRS
17 잔여보장요소 against the surrender value computed **under 제7-66조제1항 — on that basis
even for the 제7-66조제4항 products that may contractually pay less** [REG-R11]. So the
CI-event release of `k` changes the *contractual* surrender value sharply, doubling it from
one day to the next, and changes the reserve the appropriation is measured against **not at
all**, because that reserve was already computed on the unsuppressed 별표-14 basis. The
carve-out is therefore a pure transfer of value to the CI claimant, visible in the fulfilment
cash flows and invisible in the surrender-value reserve — which is exactly the kind of
divergence a reader arriving from any other library in this repository will not expect.

K-ICS decomposes the life and long-term-health module into seven sub-risks, of which five map
one-for-one onto this product's decrements and assumptions: **사망위험액**, **장수위험액**,
**장해ㆍ질병위험액** (the CI decrement), **해지위험액** (option exercise and mass lapse) and
**사업비위험액**, each measured by 충격시나리오방식 [REG-R13]. **해지위험액** is why the
무·저해지 lapse assumption is a supervisory issue and not only an earnings issue. The shock
magnitudes live in 시행세칙 [별표 22], which was not retrieved [REG-R26], and **no `krlib`
model computes 요구자본**; `technical-notes.md` names the sub-risk each sensitivity
corresponds to, because that is the vocabulary a Korean actuary uses.

**The valuation and pricing bases are not public, and that is structural.** The 보험료 및
해약환급금 산출방법서 is one of the 기초서류 filed with the FSC and not published [REG-R2];
the **경험생명표** is released only as summary statistics, as the chassis sets out [REG-R33]
[REG-R34]; and — the point that bites hardest here — the **life 참조순보험요율** is defined
by 감독규정 제1-2조제1호 as the 위험률 the bureau **files** with the FSC, not as a published
table [REG-R4] [REG-R34]. The exception is the **장기손해보험 참조순보험요율** display
보험개발원 does publish, whose 「기타피부암 및 갑상선암 이외의 암 발생률」 and 질병입원율
grids [REG-R61] are what `Cancer_KR_S` and `Medical_KR_S` source from; it carries no
중대한 질병 item and its insured-cancer definition is not this product's, so nothing on it
reaches `CI_KR_S`. **For mortality the chassis can at least bracket the level from two
carriers' published 적용위험률 grids; for CI morbidity there is exactly one disclosed table
in the whole of Korea, and it is [S3]'s, fifteen years old.** Consequently every mortality,
morbidity and incidence rate in `CI_KR_S` is a **[std]** construction with a `provenance`
column on every row, anchored on the public 국가데이터처 생명표 [REG-R38] [REG-R39], on the
national cancer registry [REG-R40], on `LTC_KR_S`'s 등급 inception construction [REG-R42]
[REG-R43] and on [S3]. **The library's tables must never be presented as the 경험생명표 or as
a 참조순보험요율.** Nothing in the file supplies a numeric expense loading either: [S1] names
the components as 계약체결비용 and 계약관리비용, the latter split into 유지관련비용 and
기타비용, deducted as part of the 월대체보험료 [S1], and [S3]'s 예정사업비율 table did not
extract — so **every 사업비 parameter in `CI_KR_S` is [std]**, bounded above by the
표준해약공제액 [REG-R20] and by the 보험료지수 of 130.1% [S3].

**Contract law and conduct.** 보험업법 supervises the undertaking; **상법 제4편 보험**
governs the contract and is one-way mandatory — 제663조 forbids any agreement varying the
Part to the disadvantage of the policyholder, insured or beneficiary [REG-R49]. Every general
article in [S1] follows the **생명보험 표준약관** at 보험업감독업무시행세칙 [별표 15]
[REG-R25], and the chassis specifies them: 보험나이, 청약철회, 품질보증해지, the
contestability limbs, 사기에 의한 계약, the 14-day 납입최고, 부활, the surrender-value table
as a contractual deliverable and the policy-loan restriction on 순수보장성보험. **Two of
those articles carry more weight here than on the chassis.** 부활 (제27조) restarts not only
the suicide and contestability clocks but the **90-day 중대한 암 보장개시일**, because the CI
약관 drafts it 「계약일(부활(효력회복)일)부터」 [S1 별표1 주1] — so a reinstated CI contract
is uncovered for cancer for ninety days, which is a decrement a chassis model has no
counterpart for. And the **장해분류표** at 부표 3 of the same schedule is the source of both
the **25% stroke gate** and the 50% waiver threshold — the one place where a Korean CI
benefit trigger is set by a supervisory schedule rather than by the carrier. It defines 장해
as 「상해 또는 질병에 대하여 치유된 후 신체에 남아 있는 **영구적인** 정신 또는 육체의
훼손상태 및 기능상실 상태」, excluding temporary states during treatment [REG-R25].
Identifying [S1]'s general articles with the current edition of [별표 15] rests on their
form: the schedule text was retrieved [REG-R25] but the CI 약관 in the set are the 2017 and
2019 editions, so the **edition-level** match is [unverified].

Korea's **two-limb contestability window** — 2 years claim-free *and* a hard 3-year longstop
— is worth naming against Japan's single 2-year rule, as is the **2-year** suicide exclusion
against Japan's 3 and the UK's 1 [S1 제10조]. So is the **14-day** 납입최고: Korean lapse
timing is far tighter than the one-to-two-month Japanese grace, and there is **no
자동대출납입 (automatic premium loan)** article in any retrieved Korean 약관 — a conventional
Korean contract lapses at the end of a 14-day demand period, and a universal-chassis one runs
on the 월대체보험료 instead [S1 제29조]. A model that imports the Japanese APL machinery onto
this chassis would remove a decrement the contract has.

**Tax.** The premium qualifies for the **보장성보험료 세액공제** on the chassis's terms — a
12% credit, not a deduction, on premiums up to ₩1,000,000 a year, on the same maturity-value
test the supervisor uses to define a 보장성보험 [REG-R57] [REG-R9] — and the death benefit
falls into the estate on the chassis's terms under 상속세 및 증여세법 제8조 and 제34조
[REG-R59]. **The acceleration changes the second of those in a way the chassis has no
occasion to state.** The CI payment is a living benefit received by the insured, so it leaves
the contract before death and enters the insured's own estate as cash rather than as
insurance proceeds; the sum that falls into the estate under 제8조 is then the **residual** —
20% of the 기본보험금 on the composite, or its 105%-of-account floor, not 100%. On the 80%
form that is four fifths of the benefit re-characterised. `krlib` models contractual cash
flows and not the policyholder's tax position, and it asserts **nothing** about the
income-tax treatment of the CI payment itself, which no retrieved document establishes.

**Policyholder protection.** 예금자보호법 시행령 제18조제7항 sets the limit at
**₩100,000,000** per person per insurer — not ₩50,000,000, which survives only in pre-2025
material — applied separately to four buckets, of which 보험금 claims against an insurer are
one, expressly **excluding** benefits payable because the policy term has ended [REG-R52]. On
a 종신 contract there is no term-end benefit, so the whole of this product's protection sits
in the 보험금 bucket. 표준약관 제43조 requires the cross-reference to appear in the 약관
[REG-R25].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-ci_insurance-r1
[R10]: #krlib-ci_insurance-r10
[R11]: #krlib-ci_insurance-r11
[R12]: #krlib-ci_insurance-r12
[R13]: #krlib-ci_insurance-r13
[R14]: #krlib-ci_insurance-r14
[R15]: #krlib-ci_insurance-r15
[R16]: #krlib-ci_insurance-r16
[R2]: #krlib-ci_insurance-r2
[R3]: #krlib-ci_insurance-r3
[R4]: #krlib-ci_insurance-r4
[R5]: #krlib-ci_insurance-r5
[R6]: #krlib-ci_insurance-r6
[R7]: #krlib-ci_insurance-r7
[R8]: #krlib-ci_insurance-r8
[R9]: #krlib-ci_insurance-r9
[REG-R1]: #krlib-reg-r1
[REG-R11]: #krlib-reg-r11
[REG-R13]: #krlib-reg-r13
[REG-R16]: #krlib-reg-r16
[REG-R17]: #krlib-reg-r17
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R21]: #krlib-reg-r21
[REG-R25]: #krlib-reg-r25
[REG-R26]: #krlib-reg-r26
[REG-R27]: #krlib-reg-r27
[REG-R28]: #krlib-reg-r28
[REG-R29]: #krlib-reg-r29
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R38]: #krlib-reg-r38
[REG-R39]: #krlib-reg-r39
[REG-R4]: #krlib-reg-r4
[REG-R40]: #krlib-reg-r40
[REG-R42]: #krlib-reg-r42
[REG-R43]: #krlib-reg-r43
[REG-R45]: #krlib-reg-r45
[REG-R48]: #krlib-reg-r48
[REG-R49]: #krlib-reg-r49
[REG-R51]: #krlib-reg-r51
[REG-R52]: #krlib-reg-r52
[REG-R54]: #krlib-reg-r54
[REG-R55]: #krlib-reg-r55
[REG-R57]: #krlib-reg-r57
[REG-R59]: #krlib-reg-r59
[REG-R60]: #krlib-reg-r60
[REG-R61]: #krlib-reg-r61
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
