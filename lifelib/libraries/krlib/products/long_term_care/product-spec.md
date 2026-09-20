# Product Specification

**Status:** Draft, 2026-09-03 (all cited sources accessed 2026-09-03).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modelling. It does not describe any single insurer's product. Facts
carrying a source tag — [S#] (primary product documents: policy conditions (*yakgwan*,
약관), product summary (*sangpum yoyakseo*, 상품요약서), pre-sale disclosure
(*boheom annae jaryo*, 보험안내자료) and carrier press releases) and [R#]
(product-specific regulatory, statutory, statistical and actuarial references), both
numbered per `_research/long-term-care.md` and resolved in `sources.md` (same directory;
numbering frozen, never renumbered), and [REG-R#] (the cross-product reference library
`references/regulatory-and-actuarial-references.md`, whose own R-numbering is distinct and
frozen at R1–R62) — were extracted from the cited document. Values marked **[std]** are
standardizations introduced for the reference implementation; each [std] table row carries a
numbered footnote giving the rationale and, where the research file brackets it, the observed
range across insurers. Facts the research file could not confirm against a retrieved document
are flagged [unverified]. The composite is drawn from **five carriers'** current retail
long-term-care and dementia contracts: a state-run insurer's 상품요약서, the only retrieved
document that publishes a **pricing basis** — an 예정이율 and an 예정위험률 table containing
Korean long-term-care incidence rates [S1]; a life carrier's full pre-sale disclosure with a
25-cover premium rate card and a published surrender-value progression [S2]; two non-life
carriers' complete 약관, which supply the verbatim benefit articles [S3] [S4]; and a fifth
carrier's product launch release [S5]. Only [S3] and [S4] are full contract documents; [S1]
is a statutory extract of the 기초서류, [S2] is the regulated pre-sale disclosure under
보험업법 제95조, and [S5] is marketing copy. Where a retrieved document is silent this
specification says so rather than inferring.

**This document states its deltas against
[the cancer product specification](../cancer/product-spec.md), the `krlib` fixed-benefit
(정액) 제3보험 chassis.** That document specifies **five mechanics once and in full** so that
this one need not restate them, and the deltas are best read against its own numbering:

| Chassis mechanic | `LTC_KR_S` delta |
|---|---|
| **1. Diagnosis-triggered lump sums graded by a severity ladder** (고액암 / 일반암 / 특정소액암 / 유사암), the tier decided by a public **classification** the insurer applies | Replaced by a **threshold ladder on one statutory scale**, the grade decided by a public **committee** the insurer does not sit on. The ladder runs *cumulatively from the top* — 1등급, 1~2, 1~3, 1~4, 1~5, 1~인지지원 — so widening the gate does not scale the amount, it changes the **frequency and the timing** together |
| **2. The 90-day 면책기간 and its four carve-outs**, a pre-inception event making the affected cover **무효** with premiums returned | Inherited, with the same 90-day construction and the same 무효 consequence — but the carve-outs differ (a **재해 carve-back to 계약일**, no 유사암 analogue, no under-15 rule, and a **one-year** clock on the dementia module), and there is **no revival option**: the chassis lets a policyholder cancel within 90 days, this product simply voids the benefit |
| **3. The 감액기간 sitting on top of the waiting period** | Inherited at the same **1 year at 50%**, but keyed to **causation** (질병 halved, 상해/재해 full) rather than applying to every tier, and **frozen at first certification** for the whole life of the annuity |
| **4. The 유사암 reduced tier**, letting one contract cover a high-frequency decrement without repricing | **No analogue.** There is no reduced tier and no fractional benefit; the light grades are reached by moving the threshold, which is a different product at a different price (about 4.5 : 1) rather than a fraction of this one |
| **5. A post-diagnosis survival model** — a correction that decides how long the waiver, the inpatient and treatment benefits and the 재진단암 clock run | **The whole product.** The benefit here is an annuity metered on survival in the care state, the waiver stops premium for the duration of that state, and there is no incidence rate anywhere that does not depend on how long the state lasts |

Everything else is taken over unchanged and is **not restated below except where this product
narrows it**: non-participating (*mubaedang*, 무배당) with no policyholder dividend; a fixed
sum (*jeongaek*, 정액) paid on an event rather than an indemnity against a cost; a benefit
payable **최초 1회한** (once only) that extinguishes the benefit line paying it without
terminating the contract; the 해약환급금 미지급형 (*haeyak hwangeupgeum mijigeup-hyeong*,
no-surrender-value) form with its cliff at 납입완료, its 별표 14 floor and its 환급률 cap; the
statutory payment of the **계약자적립액** on death from a cause the contract does not cover;
the absence of a policy loan and of an automatic premium loan; and the whole of the 표준약관
furniture — 보험나이, 청약철회, 품질보증해지, 계약 전 알릴 의무, 사기에 의한 계약, 납입최고,
실효 and 부활.

**What it replaces is the trigger, and with it the shape of the liability.** Cancer cover
pays on a **pathological event**: a named specialist reads a specimen, the diagnosis is dated
to the report, the contract carries a KCD annexe, a 원발부위 기준 clause and an evidentiary
chain, and the benefit is a point in time. Long-term-care cover pays on an **administrative
determination of the state**: a 등급판정위원회 (grade assessment committee) sitting inside
국민건강보험공단 scores an applicant on a 52-item instrument and awards a
장기요양등급 (*janggi yoyang deunggeup*, long-term-care grade), and the contract's
지급사유 is written by reference to that grade and to nothing else [S1] [S2] [S3] [S4]. Both
products outsource their definition to a public instrument, and the difference between the
two instruments is the difference between the two liabilities: the KCD is a **classification**
that a pathologist and then an insurer *apply*, and it is published, stable and appealable on
its own terms; the 장기요양등급 is a **decision** that a statutory committee *makes*, on a
scoring instrument set by 고시, and the insurer's only role is to read the certificate. Four
consequences run through everything below.

1. **The benefit definition belongs to a statute, not to a carrier.** The grades, the scoring
   instrument, the point thresholds and the eligibility gate are set in the
   노인장기요양보험법 and its 시행령 [REG-R54] [REG-R55], and can be moved by 대통령령
   without reference to any insurer. No retrieved contract carries a 기초율변경권 on the
   long-term-care benefit; what it carries instead is a *contract-continuity* clause letting
   the insurer rewrite the cover if the grades cease to exist [S3] and a definitional fallback
   naming a successor body [S4]. Neither is a repricing right. **That asymmetry is the central
   risk of the Korean product** and it has no counterpart in the cancer chassis, whose
   definition the insurer drafts.
2. **The insured event is a state with a duration, not an event with a date.** Cancer's
   진단확정 is absorbing only in the trivial sense that the benefit is paid once;
   장기요양상태 is a state in which the insured *lives*, drawing an annuity, having stopped
   paying premiums, and dying at a rate materially above that of a healthy life of the same
   age. `LTC_KR_S` is therefore a **three-state model** — healthy / in long-term care / dead —
   with the care state absorbing and carrying its own mortality basis. `Cancer_KR_S` needs no
   such basis.
3. **The basis is a prevalence, not an incidence.** The one large public dataset — the
   국민건강보험공단 노인장기요양보험 통계연보 연령별 인정률 [R4] — counts people *holding*
   a certification, not people entering one. Converting it is the actuarial work that matters
   in this product, it cannot be done from the yearbook alone, and it is set out in
   "Product overview and market role" below rather than assumed away. The cancer chassis has
   no such step: 보험개발원 publishes an 「기타피부암 및 갑상선암 이외의 암 발생률」 grid
   by age and sex on its 장기손해보험 참조순보험요율 display, on the insured definition, so
   `Cancer_KR_S` reads an **incidence** [REG-R61]. Nothing on that display reaches this
   trigger.
4. **The 만나이 projection basis, which the chassis introduces as an approximation, is here
   exact where it matters.** Both models project on **만나이** (*man nai*, age last birthday)
   while the contract ages on **보험나이** (*boheom nai*, nearest birthday under the six-month
   rule of
   표준약관 제21조) [REG-R25], and in `Cancer_KR_S` that half-year offset is a named [std]
   simplification adopted because the public decrements are published on 만나이. Here the
   same convention is additionally **the contract's own**: the benefit definition contains a
   statutory age test written 「만 65세 이상 노인」 or 「노인성 질병을 가진 만 65세 미만의
   자」 [S2] [REG-R54], and the issue-age grids of three of the five carriers are themselves
   quoted 「만」 [S1] [S3]. So the one place where age enters this product's *trigger* is a
   만나이 test, and the model represents it without conversion. The offset survives only in
   the premium, and the technical notes carry it there.

**And this is private cover written on top of a compulsory public scheme, not the public
scheme.** 노인장기요양보험 (*noin janggi yoyang boheom*) is social insurance under the
노인장기요양보험법 of 2007, in force since July 2008, run by 국민건강보험공단, paying for
services **in kind** (현물급여) against a certification of need, with the recipient meeting a
본인일부부담금 [REG-R54] [R1]. The product specified here is a private 제3보험 contract that
pays **cash** (정액) to the insured and borrows the public scheme only as a **benefit
trigger** [R9]. Nothing in this document describes an entitlement under 노인장기요양보험.

**One more thing this document is not about.** Korean market commentary in 2024 and 2025
uses the word 간병 overwhelmingly to mean **간병인사용일당**, a daily indemnity for hiring a
private carer during a hospital stay, whose loss ratios reached about 100% in the life sector
at August 2024 against 18.7% two years earlier and whose premium at the five largest non-life
carriers grew roughly twenty-fold in four years [R15]. It is a hospital-days
frequency-severity product; it sits inside the same 약관 as the grade-triggered benefits [S1]
[S2] [S4]; and it shares nothing with them except the word. It is **out of scope** and
`LTC_KR_S` does not model it. A reader who knows the Korean market only through that coverage
will otherwise attribute its exposures to this product, which has none of them: the trigger
here is a public administrative decision the insurer neither funds nor influences, and it
fires once.

---

## Product overview and market role

**The statutory class.** 간병보험 (*ganbyeong boheom*, long-term-care insurance) is not a
species of 질병보험. 보험업법 제4조제1항제3호 names 제3보험업 as comprising 상해보험,
질병보험 and **간병보험**, three coordinate 보험종목, and 제4조제3항 deems a fully licensed
life insurer or a fully licensed non-life insurer to hold the third-sector licence [R12]
[REG-R1]. That is why the four contract documents behind this specification come two from
life-side writers [S1] [S2] and two from non-life writers [S3] [S4] and describe a
recognisably identical benefit. It is also why the 제3보험 design rules of 감독규정
제7-63조 and the surrender-value rules of 제7-66조~제7-70조 reach this product directly
[REG-R17] [REG-R19].

**The private product predates the public scheme by five years.** 간병보험 was first written
in **August 2003**; 노인장기요양보험 began in **July 2008** [R9]. The first generation
therefore carried the carriers' own definitions — 중증치매 or 활동불능상태, each requiring
the state to have persisted **90 days or more** with no expectation of improvement [R9]. The
supervisor's own taxonomy, from a 금융감독원 release of 2012, recognises three trigger
archetypes [R9]:

| Type | 보험금 지급사유 |
|---|---|
| ① 회사기준 (company basis) | 중증치매 or 활동불능상태 diagnosed on the carrier's own definition |
| ② 공적기준 (public basis) | award of a 장기요양등급 under the public scheme |
| ③ 혼합형 (hybrid) | a stated grade **and** an activity-limitation or severe-dementia test |

Every grade-triggered benefit in [S1] – [S4] is type ②, and the literature records that
「일반적으로 간병보험에서는 공적기준을 적용하는 경향이 있다」 [R9]. Every CDR-graded
dementia benefit in [S2] and [S4] is type ①. **No type ③ benefit appears in any retrieved
document**; the hybrid form is described in the literature but was not observed on sale, and
any statement that it is still written is [unverified]. This specification is of a type ②
contract with a type ① dementia module attached.

**The public scheme the trigger points at.** 노인장기요양보험법 제2조제1호 defines 「노인등」
as a person **65 or over**, or under 65 with one of the **노인성 질병** the 시행령 lists
[REG-R54] [REG-R55]. So the scheme is not an age-65 scheme. 제2조제2호 defines 장기요양급여
as the support given to a person recognised under 제15조제2항 as unable to perform daily life
alone **for six months or more** [REG-R54] — a duration test that lives in the statute, which
is the Korean equivalent of the 180-day persistence tests that Japanese and French private
contracts have to write into their own conditions. Korea does not need to, because the state
has already applied one. 제15조제2항 then sends the grade boundaries themselves to the
시행령, where they can be moved by decree [R1 제15조](#krlib-long_term_care-r1) [REG-R54].

The score is built from a home visit covering **12개 영역 90개 항목**, of which **52개 항목**
enter the 장기요양인정점수 across 기본적 일상생활활동 (ADL), 수단적 일상생활활동 (IADL),
인지기능, 행동변화, 간호처치 and 재활 [R6]. The bands are 시행령 제7조제1항, verbatim
[REG-R55], corroborated by the 법제처 restatement [R3] and reproduced inside a carrier's own
disclosure [S2]:

| 등급 | 장기요양인정점수 | 심신의 기능상태 |
|---|---|---|
| 1등급 | **95점 이상** | 일상생활에서 **전적으로** 다른 사람의 도움이 필요 |
| 2등급 | **75점 이상 ~ 95점 미만** | 일상생활에서 **상당 부분** 다른 사람의 도움이 필요 |
| 3등급 | **60점 이상 ~ 75점 미만** | 일상생활에서 **부분적으로** 다른 사람의 도움이 필요 |
| 4등급 | **51점 이상 ~ 60점 미만** | 일상생활에서 **일정 부분** 다른 사람의 도움이 필요 |
| 5등급 | **45점 이상 ~ 51점 미만** | **치매환자** (시행령 제2조의 노인성 질병에 해당하는 치매로 한정) |
| 인지지원등급 | **45점 미만** | **치매환자** (동일한 한정) |

Three structural points that a model must not blur, and that the benefit design turns on.

- **5등급 and 인지지원등급 are not the bottom of a severity ladder; they are a separate
  gate.** A person scoring below 51 points receives nothing at all unless the impairment is a
  **dementia within the 시행령 제2조 list**, in which case they receive 5등급 (45–51) or
  인지지원등급 (below 45) [REG-R55] [R3] [S2]. A model that treats the six grades as an
  ordered scale and interpolates between them is wrong at exactly the two grades carrying the
  fastest-growing private cover.
- **인지지원등급 did not exist before 2018-01-01.** It was created to let 경증치매 patients
  with relatively intact physical function use services, absorbing part of the former 등급외
  population [R6]. Any experience series crossing that date carries a level shift — and every
  「1~인지지원등급」 rider in force on that date had its covered population enlarged
  overnight, at no additional premium [S2] [R6].
- **The score is not a linear function of anything an underwriter observes.** The mean
  인정점수 of the 271,474 certified decedents studied in [R11] is **82.1 (SD 21.8)** —
  squarely inside 2등급 — decomposed as 신체기능 25.5 of 13–36, 인지기능 4.3 of 0–7,
  행동변화 1.3 of 0–14, 간호처치 0.4 of 0–9 and 재활 14.8 of 10–30. Physical function and
  rehabilitation dominate; cognition contributes at most 7 points of about 100. That is why a
  dementia sufferer with intact mobility falls below 51 and needs the 5등급 gate, and it is
  why the CDR-triggered dementia benefits of the type ① line exist at all.

**The route in below 65.** 노인장기요양보험법 시행령 [별표 1] carries a **closed list of 25
diseases with KCD codes** — four dementia codes, one Alzheimer code, fourteen cerebrovascular
codes, four Parkinson-family codes, plus 척수성 근위축, 다발경화증, 중풍후유증 and 진전
[REG-R55] [R2]. Of the **58,271** applicants under 65 in 2024 the causes split
뇌혈관질환군 **28,628 (49.1%)**, 치매질환군 **15,640 (26.8%)**, 파킨슨질환군 **4,086
(7.0%)**, 그 밖의 질병 1,122 (1.9%) and 기타 8,795 (15.1%) [R4 표2-3, shares derived](#krlib-long_term_care-r4). There
is **no cancer on the list**, no musculoskeletal condition and no frailty category, so a
person under 65 disabled by cancer or by a hip fracture cannot be certified at all. That is
the single largest difference from the Japanese scheme, whose 16 特定疾病 include terminal
cancer, and it makes the Korean under-65 exposure both smaller and far more concentrated.

**Which grades may use which benefit — and why 1·2등급 is the modal private trigger.** Under
the 보건복지부 고시 on 급여 provision, 「수급자 중 장기요양등급이 1등급 또는 2등급인 자는
재가급여 또는 시설급여를 이용할 수 있고, 3등급부터 5등급까지인 자는 재가급여만을 이용할 수
있다」, with three exceptions on which the committee may permit 시설급여 [R6]. **1·2등급 is
the statutory boundary between home care and institutional care**, which is the structural
reason it is where the private market puts its main trigger.

### The public statistics, and what they are and are not

The quantitative basis for this product is the **2024 노인장기요양보험 통계연보**, an official
national statistic (국가승인통계) published by 국민건강보험공단 빅데이터사업실 on 2025-06-30
[R4]. Two independent checks sit behind it. The 공단's own 경영공시 table at **2026-06-30**
reports 총 등급판정 1,411,466, 인정자 1,275,370 and a grade split of 1등급 3.8% / 2등급 7.1% /
3등급 23.6% / 4등급 42.8% / 5등급 10.7% / 인지지원 2.2% **of all assessed** [REG-R42] — a
later as-of date and a wider denominator than the table below, but the same shape, and the
same 1·2등급 concentration. And the yearbook's launch coverage reproduces its headline figures
[R18], as does a trade summary whose own figures are [unverified] and are used nowhere here
[REG-R43].

**Headline stocks and flows, 2024** [R4 표1-1, 표2-1, 표2-5](#krlib-long_term_care-r4):

| Quantity | 2024 |
|---|---|
| 의료보장 적용인구, 65세 이상 | **10,399,813** (남 4,613,166 / 여 5,786,647) |
| 인정 신청자 | **1,477,948**, of which 58,271 aged under 65 |
| 등급 판정 (계) | **1,301,069** |
| — 인정자 | **1,165,030** |
| — 등급외 | 136,039 |
| 판정 대비 인정률 (derived) | **89.5%** |
| 급여이용 수급자 | 1,140,725 |

**인정자 by grade** [R4 표2-5](#krlib-long_term_care-r4):

| 등급 | 인원 | 구성비 (derived) |
|---|---|---|
| 1등급 | 55,340 | 4.75% |
| 2등급 | 99,429 | 8.53% |
| 3등급 | 310,717 | 26.67% |
| 4등급 | 536,261 | 46.03% |
| 5등급 | 135,448 | 11.63% |
| 인지지원등급 | 27,835 | 2.39% |
| **계** | **1,165,030** | 100.00% |

Women are **70.9%** of the certified population (826,316 of 1,165,030) [R4 표2-5, derived](#krlib-long_term_care-r4).
**1·2등급 together are only 13.28%** of all certified lives. That single figure is the most
important calibration fact in this product: the comparable Japanese quantity, 要介護2以上, is
50.8% of certified persons, so a Korean 「1~2등급」 promise is a far narrower one than a
Japanese 「要介護2以上」 promise. The two scales are constructed differently and the
comparison is not exact, but the direction is unambiguous.

**The certification rate by age band, 2024**, computed as (계 − 등급외) over population [R4
표2-9 and 표1-2, derived](#krlib-long_term_care-r4):

| 연령 | 인정자 | 인구 | **인정률 (계)** | 인정률 (남) | 인정률 (여) |
|---|---|---|---|---|---|
| 65–69 | 66,955 | 3,715,757 | **1.80%** | 1.98% | 1.63% |
| 70–74 | 102,751 | 2,437,413 | **4.22%** | 3.95% | 4.45% |
| 75–79 | 176,578 | 1,796,342 | **9.83%** | 7.45% | 11.76% |
| 80–84 | 320,148 | 1,344,376 | **23.81%** | 15.45% | 29.24% |
| 85+ | 461,622 | 1,105,925 | **41.74%** | 28.63% | 47.31% |
| **65+** | **1,128,054** | **10,399,813** | **10.85%** | **6.87%** | **14.02%** |

and the same quantity restricted to the grades the composite pays on [R4 표2-9 and 표1-2,
derived](#krlib-long_term_care-r4):

| 연령 | 1·2등급 인정자 | 인구 | **1·2등급 인정률** |
|---|---|---|---|
| 65–69 | 9,801 | 3,715,757 | **0.264%** |
| 70–74 | 13,121 | 2,437,413 | **0.538%** |
| 75–79 | 20,124 | 1,796,342 | **1.120%** |
| 80–84 | 35,377 | 1,344,376 | **2.631%** |
| 85+ | 68,112 | 1,105,925 | **6.159%** |

Four readings, all load-bearing.

1. **The gradient is a doubling roughly every five years to 80 and steeper after** — 1.80% to
   41.74% across four bands, a factor of 23 over twenty years, or about **17.0% per year of
   age** on the prevalence scale [derived, `(0.41741/0.01802)^(1/20) − 1`]. The 1·2등급 curve
   runs at essentially the same slope, so it is close to a parallel shift of the all-grade
   curve at about one seventh of its level.
2. **The sex crossover is at about age 70.** Below 70 male certification exceeds female
   (1.98% against 1.63%); by 75–79 female exceeds male by 58% and by 85+ by 65%. This is the
   reverse of a death-benefit table, and it reappears in every published premium card
   ("Variations across insurers", item 10).
3. **The severe share is U-shaped in age** — 1·2등급 is 22.3% of certified lives under 65,
   falls to 11.1% at 80–84, and rises again to 14.8% at 85+ [R4 표2-9, derived](#krlib-long_term_care-r4). The under-65
   population is severe because only the 노인성 질병 list gets in at all [REG-R55]; the 80–84
   trough is where the marginal entrant is a lightly-impaired person newly crossing the
   51-point line. **A model applying one grade-mix vector at all ages will mis-price a 1·2등급
   benefit by up to a factor of two.**
4. **The published 인정률 series is on a different denominator from the table above.** The
   figure Korean commentary quotes — 11.20% for 2024 — divides *all* 인정자, including
   under-65s, by the *65-and-over* population [R4 표1-1; R16; R18](#krlib-long_term_care-r4). The demographically honest
   65+ rate is **10.85%**. They differ by 0.35 points and a document that quotes one and
   compares it against the other is wrong.

### The basis is a prevalence, and the conversion is the modelling work

Everything above counts people **holding** a certification at a point in time. A cash-flow
model of a 진단급여금 needs the rate at which lives **enter** the certified state, and a model
of a 간병연금 needs that entry rate **and** a post-entry survival basis. This subsection
records what the retrieved evidence can and cannot establish, because the answer bounds every
figure in the technical notes.

**The identity.** In a stationary population,

    prevalence  =  incidence  x  mean duration in the state

so `I(x) ≈ P(x) / D`, with `D` the mean time from certification to exit — exit being death
or, rarely, recovery. The Korean certified stock grew **6.1%** in 2024 [R18], so the
population is not stationary and the identity understates incidence by roughly the growth
rate. It is a first-order estimate, not an equality.

**What is known about `D`, and the estimate that must not be used.** One retrieved study
measures it: [R11] followed **271,474** people certified between 2008-07-01 and 2012-12-31
**who also died inside that window**, and found the mean time from 등급인정 to death to be
**516.2 days (1.414 years, SD 430.4)**, with **8.7%** dying within one month and **45.6%**
within one year. That figure is a **lower bound and not an estimate of `D`**, because the
design excludes by construction everybody certified early in the window who was still alive at
the end of it — that is, everybody with a long duration. Substituting it into the identity at
65+ gives `I ≈ 10.85% / 1.414 = 7.67%` per annum, which is its own refutation: the same
identity has the certified stock turning over entirely every **1.414 years**, about seventeen
months, whereas only **27.4%** of it (318,992 of 1,165,030) arose from a first application at
all [R4 표2-5, derived](#krlib-long_term_care-r4). The arithmetic is recorded here so that nobody repeats it.

**Two independent estimators that do work.** First, from the yearbook's own application-route
table. [R4 표2-5](#krlib-long_term_care-r4) classifies the 1,165,030 current certifications by the application type that
produced them — 인정신청 (first application) **318,992**, 갱신신청 639,659, 등급변경신청
107,365, 재신청 98,983, 직권재조사 31. The 인정신청 bucket approximately holds the
first-time entrants of the trailing two years who are still alive, still certified and have
not yet renewed or changed grade, the base 유효기간 being two years [R13, unverified](#krlib-long_term_care-r13). Writing
`E` for annual first entries and using [R11]'s survival shape for the in-bucket persistence
gives `∫₀² s(t) dt` of order 1.3–1.5, hence `E ≈ 318,992 / 1.4 ≈ 228,000` per annum and
therefore `D ≈ 1,165,030 / 228,000 ≈ **5.1 years**` [derived, assumption-dependent]. Second,
from the roll-forward: 인정자 went from 1,097,913 (2023) to 1,165,030 (2024), a net **+67,117**
[R18], and in near-steady state `E − stock/D = 67,117` gives

| assumed `D` | implied exits | implied entries | implied 65+ entry rate | implied `I(65+) = P/D` |
|---|---|---|---|---|
| 3.0 years | 388,000 | 455,000 | 4.4% | 3.62% |
| 4.0 years | 291,000 | 358,000 | 3.4% | 2.71% |
| 5.1 years | 228,000 | 295,000 | 2.8% | 2.13% |
| 5.5 years | 212,000 | 279,000 | 2.7% | 1.97% |

(derived; the entry rate divides by the 65+ population, so it carries the same mixed
convention as the published 인정률). **The two routes agree: `D` is near 4–5.5 years and the
all-grade 65+ entry rate is near 2–3.5% per annum.** That factor-of-two bracket is the honest
width of what the retrieved evidence supports, and the technical notes carry it as a stated
sensitivity rather than hiding it inside a point estimate.

**Why the same conversion is wrong for a 1·2등급 benefit — and why this product is
three-state.** Applying `I = P/D` to the 1·2등급 prevalence curve at 65–69 with `D = 4` gives
about **0.0685%** (male) and **0.0635%** (female) per annum [derived]. But the 1·2등급 *stock*
is not built from direct entries. Only **13.3%** of current 1등급 certifications arose from a
first application (7,371 of 55,340) against **69.5%** from a renewal, whereas at 인지지원등급
the first-application share is **69.8%** (19,436 of 27,835) [R4 표2-5, derived](#krlib-long_term_care-r4). **Severe-grade
lives are, in the main, people who entered the scheme years earlier at a lighter grade and
deteriorated into it.** A single-decrement model that treats `I₁₂` as a healthy-life incidence
overstates the direct entry rate, understates the delay, and puts the cash flow years too
early. The structurally correct representation is multi-state — healthy → light grade (3–5,
인지지원) → severe grade (1–2) → dead — with the light-grade state's exit split between
progression and death; `LTC_KR_S` is built that way, and where the reference implementation
collapses a transition the collapse is named and marked [std] in the technical notes.

**The one disclosed incidence basis, and the cross-check it provides.** Exactly one retrieved
document publishes Korean long-term-care incidence rates: the 우체국 상품요약서's 예정위험률
table [S1]. It is a *pricing* basis for an underwritten, 180-day-waited, two-year-reduced
product, covering three ages and only grades 1 and 2 — but it is the only hard anchor
available, and every [std] incidence assumption in `LTC_KR_S` is calibrated against it.

| 예정위험률 (1종 일반가입) | 성 | 40세 | 50세 | 60세 |
|---|---|---|---|---|
| **요양(1등급) 발생률** | 남 | **0.000028** | **0.000080** | **0.000237** |
| | 여 | **0.000010** | **0.000046** | **0.000209** |
| **요양(2등급) 발생률** | 남 | **0.000018** | **0.000072** | **0.000293** |
| | 여 | **0.000007** | **0.000042** | **0.000250** |

Four things the table says, all derived from it [S1].

- **Age gradient.** The male 1등급 rate multiplies by 2.86 from 40 to 50 and 2.96 from 50 to
  60 (11.1% and 11.5% a year); the female by 4.60 and 4.54 (16.5% and 16.3% a year); the
  2등급 rate grows at 14.9%/15.1% (남) and 19.6%/19.5% (여). The population prevalence
  gradient is 17.0% a year. The female pricing gradient sits on it; the male gradient is
  materially flatter, which is the selection effect an underwritten first-entry basis carries
  and a population prevalence does not.
- **Sex ratio and the crossover.** Female over male on the 1등급 rate is 0.357 at 40, 0.575 at
  50 and 0.882 at 60; on the 2등급 rate 0.389 / 0.583 / 0.853. Extrapolating puts the
  crossover between about **62 and 68**, precisely where the population data finds it (male
  above female at 65–69, reversing by 70–74). **The disclosed pricing basis and the national
  statistics agree on the sex crossover to within a few years**, which is the strongest
  internal consistency check available, and it is why the model's incidence table is built
  with a sex ratio crossing one in the late sixties.
- **1등급 exceeds 2등급 at 40 and falls below it by 60**, for both sexes. The inversion is
  real: below 65 the only route in is a 노인성 질병 catastrophe, which lands at a high grade,
  and the population data confirms it (22.3% of under-65 certified lives are 1·2등급 against
  11.1% at 80–84). At older ages the light-grade entry route opens and 2등급 becomes the more
  common first landing.
- **Combined 1·2등급 incidence** (summing the rows, an upper bound since the two are mutually
  exclusive at first certification) is 남 0.000046 / 0.000152 / 0.000530 and 여 0.000017 /
  0.000088 / 0.000459 at 40 / 50 / 60 [derived]. Against the prevalence-implied 0.000685 (남)
  and 0.000635 (여) at 65–69 with `D = 4`, the disclosed rates would need to grow only 3.7%
  and 4.7% a year over the intervening seven years of age, far below the 11–20% the same table
  shows at younger ages. **The gap is selection plus progression**; the quantitative split
  between the two is established by no retrieved source and is [std] in the model.

**What has to be [std], stated once.** No retrieved source gives a post-certification
mortality table by grade, a recovery or grade-improvement rate, a progression rate between
grades, a select period or underwriting-selection factor, a utilisation rate by grade and
service type, or a lapse table for a Korean 간병보험. 보험개발원 publishes neither a
장기요양 incidence table nor a post-onset mortality table publicly, and no reference to one
appears in any retrieved document [R9]. 보험개발원 does publish a numeric **장기손해보험
참조순보험요율** display, and it carries an 암 발생률 grid and a 질병입원율 grid [REG-R61] —
which is why `Cancer_KR_S`'s incidence basis is source-tagged and this one's is not — but **it
carries nothing for 장기요양** [REG-R4] [REG-R61].
All of these are [std] in `LTC_KR_S`, constrained where possible by [R11]
(post-onset mortality shape), [R4 표2-5](#krlib-long_term_care-r4) (progression versus direct entry), [S1] (the level of
the 1·2등급 rate at 40/50/60) and [REG-R27] (the log-linear lapse shape on the 무해지 form).

### Market position

Long-term-care cover is the **least-penetrated major protection line in Korea**, and the
gap between holding and intending to hold is the largest in the market. A 보험연구원 consumer
survey puts 간병보험 가입률 at **2.5%** overall — 0.5% in the twenties, 1.4% in the thirties,
1.2% in the forties, 3.4% in the fifties and **4.8%** at 60 and over — against a stated
가입 의향 of **10.0%** overall and 16.0% at 60 and over, and **67.5%** among people the same
study identified as actually needing care [R9]. Set that against 실손의료보험, held by about
two thirds of the population, and 암보험, held by a large majority. A 생명보험협회 survey in
2022 found **40.8%** naming 간병보험 as the cover they would buy next [R16, news](#krlib-long_term_care-r16).

The line's history is a contraction followed by a rediscovery, and the turn is dated by the
public scheme. Life-sector in-force count fell **12.6%** between 2008 and 2013 — from 143
thousand contracts and ₩2,443bn to 125 thousand and ₩1,588bn, the private product being
displaced by the arrival of 노인장기요양보험 — and then grew **111.2%** to **264 thousand
contracts and ₩4,539bn** by 2018 as the market rediscovered it as a supplement, new business
rising from 9 to 42 thousand contracts over the same decade [R9, from 생명보험협회 통계 via
KOSIS](#krlib-long_term_care-r9). At 2019-05 there were **99 products** on sale, 46 life and 53 non-life, the largest
shelves being 현대해상 (14) and 신한생명 (12) [R9]. Trade press puts 2023 penetration at
**3.85% of non-life new business** and **2.8% of life new business**, up 2.5 and 1.7
percentage points since 2020, and reports 치매·간병보험 초회보험료 of **₩88.4bn (883억
6,606만 원)** for January–November 2024, **+70.2%** year on year [R16] [R17]. Both are news
figures and inherit that weakness.

**Benefit adequacy, for scale.** The 2019 재가급여 월 한도액 by grade was 1등급 ₩1,456,400 /
2등급 ₩1,294,600 / 3등급 ₩1,240,700 / 4등급 ₩1,142,400 / 5등급 ₩980,800 / 인지지원등급
₩551,800 [R6, 2019 values, now stale — the current 보건복지부 고시 was not retrieved](#krlib-long_term_care-r6). The
composite's 간병연금 of ₩500,000 a month at 1등급 is therefore about a third of the public
재가 ceiling as at 2019, and roughly twice the recipient's own 본인부담 on that ceiling at a
15% co-payment rate [derived; the co-payment rate is [unverified], from a 2012-vintage mirror
of 법 제40조, and 제40조 in its current form provides for reductions of up to 60% for listed
low-income groups [REG-R54]]. Across the whole scheme the 2024 monthly 급여비용 averaged
**₩1,495,694** per recipient with a 공단부담금 of **₩1,365,413** [R18]. Private cover is a
supplement to a public benefit that already meets most of the direct service cost, and it is
sold as cash against the costs the public benefit does not reach.

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | 간병보험, **공적기준 (type ②)** grade-triggered, 무배당, sold in the **해약환급금 미지급형** form; stand-alone 주계약 (*ju-gyeyak*, main contract) paying a 장기요양진단급여금, with a 간병연금 and a 치매진단급여금 attached as 특약 (*teugyak*, riders) | [S2] [S3]; form **[std]** (1) |
| Regulatory class | **제3보험 — 간병보험**, 보험업법 제4조제1항제3호; writable by life and non-life carriers alike | [R12] [REG-R1] [REG-R7] |
| Chassis | Fixed-benefit (정액) third-sector protection. No maturity value (만기환급금 없음), no general death benefit; on death from a cause the contract does not cover it pays the **계약자적립액** and terminates, as 감독규정 제7-63조제1항제1호 requires of every 제3보험 product | [S3]; [REG-R17] [REG-R25 제22조](#krlib-reg-r25) |
| Renewal architecture | **비갱신형** (non-renewable), level premium, coterminous riders | [S1] [S2]; universal on the LTC benefit — see footnote (2) |
| Issue age (가입나이), 만나이 | **30–70** | observed 만15–75; **[std]** (3) |
| Age basis | **만나이** at 계약일, incremented on each 계약해당일. The market prices on 보험나이 — 계약일 현재 실제 만 나이 with 6개월 미만의 끝수는 버리고 6개월 이상의 끝수는 1년으로 — and the reference implementation states the offset rather than hiding it | [REG-R25 제21조](#krlib-reg-r25); basis **[std]** (4) |
| Policy term (보험기간) | **90세만기** (to attained 만나이 90) | observed 85 / 90 / 95 / 100세만기 and 종신; **[std]** (5) |
| Premium-paying period (납입기간) | **20년납** | observed 10 / 15 / 20 / 30년납, 전기납, 80세납; **[std]** (5) |
| Lives basis | Single life only | [S1] [S2] [S3] [S4] |
| 진단급여금 sum insured (보험가입금액) | **₩10,000,000 (1,000만원)** | the unit of both published rate cards [S1] [S2]; **[std]** (6) |
| Amount limits by age | 가입금액 capped where the insured is older at issue — 우체국 caps the 1~2등급 rider at ₩20,000,000 (2,000만원) and fixes the 1~5등급 and 간병비 riders at ₩5,000,000 (500만원) where 가입나이 ≥ 61 | [S1]; carried as a model-point constraint, not modelled as a decrement |
| Underwriting | **일반심사** (full declaration underwriting, no medical examination). Four-question **간편심사** is a switch, the fourth question being 「현재 노인장기요양보험에 의한 장기요양급여 수급자이거나 **장기요양인정 심의 중**입니까?」 | [S2]; scope **[std]** (7) |
| Participation | **무배당** — no policyholder dividend | [S1] [S2] [S3] [S4]; [REG-R12] |
| Pricing interest rate (예정이율) | **2.0% annual compound** | [S1] — the only Korean LTC 예정이율 in any retrieved document |
| **Anchor model cell** | **Male, 만나이 40, 90세만기, 20년납, 월납, 해약환급금 미지급형**; 장기요양(1~2등급)진단급여금 ₩10,000,000; 간병연금 on at ₩500,000 / ₩300,000 a month (1등급 / 2등급), 12-month guarantee, 120-month cap; 치매 module off; level monthly premium **₩5,600** | **[std]** (8) |

Footnotes to [std] rows:

1. Four surrender-value forms are on the shelf and they are **different products, not
   variants**, though the Korean names look almost identical. ABL's 「해약환급금 미지급형」
   pays **nothing** during the premium-paying period and **50% of a notional 기본형** value
   afterwards [S2]. 한화손해보험's 「납입중50%해약환급금지급형」 pays **50% of the 표준형
   value during** the paying period and **100% of it after** [S4]. 삼성화재 sells the pure
   protection form with 「만기환급금 : 없음」 and describes no 무·저해지 variant in the
   retrieved extract [S3]. 우체국 is a conventional **표준형** with a normal surrender value
   from year 1 — it is 우정사업본부 business, not written under 보험업법, and is not obliged
   to follow the industry's practice [S1]. The composite takes the 미지급형: it is the
   strongest form, it is the one whose surrender-value progression is published in full [S2],
   and **63.8% of Korean 보장성 초회보험료 in 2024 H1 was written in a 무·저해지 form**
   [REG-R27], so a reference library that modelled only 표준형 would be modelling a minority
   of the market.
2. Every retrieved document writes the long-term-care benefit **비갱신형** and coterminous
   with the main contract, and attaches the 갱신형 machinery to the hospital-carer and
   노인성 질환 riders travelling with it: 우체국 puts the 장기요양 riders on the 주계약's own
   term and the 간병인 riders on 5년 / 10년 갱신 [S1]; ABL does the same split, its 노인성
   질환 riders being 10년 만기 자동갱신부 [S2]. This is the opposite of the Korean *medical*
   market, where annual renewal is the defining feature, and it is the right answer for a
   benefit whose claim arrives thirty years after issue: a renewable long-term-care rider
   re-rated at attained age would price itself out of existence exactly when it was needed.
   The renewable form is **not modelled**.
3. Observed: 만15~70 on the 우체국 주계약, 30~70 on its 장기요양 riders (30~65 at 20년납 and
   30~55 at 30년납) [S1]; 25~75 (일반심사) and 30~75 (간편심사) at ABL [S2]; 만15~60 at
   삼성화재, tightening to **만15~37** on a 100세만기 전기납 1~4등급 rider — the narrowest
   envelope in the file [S3]; 30~75 at 교보 [S5]; not published at 한화손해보험 [S4]
   [unverified]. The composite takes 30–70: 30 is the modal lower bound on the *long-term-care
   benefit itself* rather than on the chassis that carries it, and 70 is the modal upper
   bound. Note that the envelope narrows as the term lengthens, which is the ordinary
   consequence of a level premium on a benefit concentrated at the far end.
4. **The two age bases, and why this product's use of the second is narrower than the
   chassis's.** The contract ages on 보험나이 — 계약일 현재 실제 만 나이 with a fraction
   under six months discarded and six months or more rounded up, incrementing at each
   계약해당일 [REG-R25 제21조](#krlib-reg-r25) — and the two differ for roughly half of all issue dates.
   `Cancer_KR_S` projects on 만나이 and records the half-year offset as a [std]
   simplification, because its decrements are published on 만나이 and no source gives the
   distribution of issue dates within a policy year that a conversion would need. `LTC_KR_S`
   inherits that convention **and needs it less as an approximation**, for two reasons.
   First, the incidence basis is 만나이 by construction — the yearbook's age bands [R4] and
   the 생명표 behind the mortality decrement [REG-R38] [REG-R39] are all 만나이. Second, and
   unlike the cancer chassis, the **contract's own trigger contains a 만나이 test**: 「만
   65세 이상 노인」 or 「노인성 질병을 가진 만 65세 미만의 자」 [S2] [REG-R54]. Three of the
   five carriers state their issue-age grids in 만 as well — 만15~55세, 만15~57세, 만15~60
   [S1] [S3]. The offset therefore survives only in the premium and not in the benefit, and
   the issue-age envelope in the row above is stated on 만나이 accordingly.
5. Observed 보험기간: 85 / 90 / 100세만기 [S1]; 90 / 95 / 100세만기 [S2]; 90 / 100세만기
   [S3]; 종신 [S5]; not published [S4]. **Nothing in the file matures before 85**, which is
   the minimum term at which the benefit means anything given the age gradient above.
   Observed 납입기간: 10 / 15 / 20 / 30년납 [S1] [S2]; 전기납 / 80세납 / 20년납 [S3];
   5 / 10 / 15 / 20년납 [S5]. The composite takes 90세만기 and 20년납 because they are the
   basis of **both** published rate cards [S1 at 50세; S2 at 40 / 50 / 60세], so the anchor
   premium and the anchor benefit are consistent with each other. 20년납 is also structurally
   necessary to the 미지급형 form: the cliff is a step at **납입완료**, and the chassis's own
   약관 confirms that a **전기납 계약** on a suppressed-value form gets no surrender value at
   any duration at all. A 전기납 contract has no step because it has no 납입완료 before
   maturity. 20년납 is also the 해약공제계수 cap for a 보장성보험 in 별표 14 and the pay
   basis its note 3 forces the 연납순보험료 to be recomputed on where the term is 20 years or
   more [REG-R20] — the chassis's reasoning, inherited unchanged. **The one delta worth
   flagging is the term itself.** `Cancer_KR_S` runs to the 100세 계약해당일; this composite
   stops at 90, which is the modal Korean long-term-care maturity and the term of both
   published anchors [S1] [S2] — but it truncates the exposure at exactly the band carrying
   the highest certification rate of all (41.74% at 85+, and still rising). The truncation is
   **materially conservative on claim cost**, it is a model-point parameter with 95세만기 and
   100세만기 available, and a run at 100세만기 is the first sensitivity the technical notes
   carry.
6. Both published cards quote at a 보험가입금액 of **₩10,000,000 (1,000만원)** — 우체국's
   장기요양(1~2등급)특약 pays ₩10,000,000 at a 특약 가입금액 of ₩10,000,000 [S1], and ABL's
   main-contract rate card is 주계약 보험가입금액 1,000만 원 [S2]. Taking that unit makes the
   anchor premium and the anchor benefit two halves of one published quotation rather than two
   independent guesses. Note 우체국's ten-to-one ratio of sums insured between its two
   thresholds at the same 특약 가입금액 — ₩10,000,000 at 1~2등급 against ₩1,000,000 at
   1~5등급 [S1] — which is the carrier's own statement of the relative frequency of the two
   gates and reconciles closely with the 13.28% 1·2등급 share of the certified stock. **The
   level is a third of the chassis's ₩30,000,000**, and the difference is a real market fact
   rather than a scaling choice: a Korean cancer 진단비 is written to replace lost income
   during treatment, whereas a long-term-care 진단급여금 sits on top of a public benefit that
   already meets most of the direct service cost, and it is the *annuity* rather than the
   lump sum that does the work here. The sum insured is nevertheless the parameter to vary
   first, because on a 최초 1회한 benefit it scales the liability linearly and carries no
   structure.
7. The 간편심사 loading is the cleanest published measure of the price of relaxed underwriting
   in Korean long-term care: **1.36–1.43×** on the main contract at every age and sex,
   **1.25–1.40×** on the 1~5등급 rider, and **1.65–1.80×** on the 간병인사용 rider [S2,
   derived]. 우체국's 2종(간편가입) runs 1.16× (male) and 1.31× (female) on the main contract
   [S1, derived], but its 장기요양 riders are 「주계약 1종(일반가입)에 한하여 부가 가능」 —
   **the long-term-care cover cannot be bought on simplified underwriting at all** — and no
   요양 발생률 is published for the 2종 form [S1]. The composite is fully underwritten; the
   loading is carried as a model-point multiplier, not as a second chassis, since it is a
   different risk pool and no retrieved source gives its incidence separately.
8. **No Korean carrier publishes a long-term-care rate card at the composite's exact
   specification**, so the anchor premium is a constructed modelling value and not a quote. It
   is built from two rows of the one published card, both at 90세만기, 20년납, 월납,
   일반심사형, 보험가입금액 1,000만 원 [S2]: **₩3,300** for the 주계약 장기요양(1~2등급)급여금
   at male 40, and **₩580** for the 장기요양(1-2등급)재가급여종신지원특약, which pays
   ₩100,000 a month for life on the same trigger. Scaling the second to the composite's
   grade-weighted expected monthly amount of ₩400,000 — the mean of ₩500,000 at 1등급 and
   ₩300,000 at 2등급, the two being close to a 50 : 50 split at first certification on the
   disclosed 예정위험률 [S1, derived: 61 : 39 at 40, 53 : 47 at 50, 45 : 55 at 60] — gives
   ₩2,320, and ₩3,300 + ₩2,320 = ₩5,620, rounded to **₩5,600**. Two offsetting differences
   are treated as cancelling and are recorded rather than adjusted for: the ABL rider runs
   **최대 종신** where the composite caps at 120 months (dearer), and it requires the insured
   to be *using* 재가급여 in the month where the composite tests only survival (cheaper). The
   corresponding female cell is ₩5,000 + 4 × ₩850 = ₩8,400 [S2, derived]. Age 40 is the
   Korean regulatory reference age — 감독규정 제1-2조제2호's **기준연령 요건** is 「남자가 만
   40세」 [REG-R9] — and it is one of the three ages at which the card publishes.

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium basis | **Level 평준납입** for a fixed 납입기간, 무배당 — no dividend, no premium review, no renewal re-rating, no 기초율변경권 on the long-term-care benefit | [S1] [S2] [S3]; and see "Basis-change risk" below |
| Rating factors | **Sex and age at 계약일 only.** No smoker class, occupation class or amount band was disclosed on any long-term-care cover in any retrieved document | [S1] [S2]; absence [unverified] |
| Frequency (납입주기) | **월납** (monthly) default; 3개월납 / 6개월납 / 연납 available | [S1] [S2]; default **[std]** (9) |
| Pricing interest rate (예정이율) | **연단위 복리 2.0%, 금리확정형** — 「무배당 우체국간병비보험 2309의 주계약 및 특약에 적용한 예정이율은 연단위 복리 2.0%입니다」 | [S1]; see footnote (9a) |
| 계약자적립액 적용이율 | **2.0%**, equal to the 예정이율 on a 금리확정형 design | [S1]; **[std]** (9a) |
| Rate structure | Not published at the composite's specification by any carrier; the office premium is a **model-point input**, backed by a [std] incidence basis constructed from the certification statistics and calibrated to the one disclosed 예정위험률 | [S1] [R4]; **[std]** (8) |
| Anchor premium | **₩5,600** a month (male 40); **₩8,400** (female 40) | **[std]** (8) |
| Sex differential, LTC covers | **Female rates exceed male at every age and widen with it** — the main contract runs 여/남 = 1.52 at 40, 1.55 at 50 and **1.61** at 60, and the 1-2등급 시설급여종신 rider reaches **2.18** at 60 | [S2, derived]; matches the population sex ratio |
| Sex differential, dementia covers | **Female rates fall *below* male on every 치매 cover** — 경도이상치매 여 40 ₩13,920 against 남 ₩17,400, a ratio of **0.80** | [S2, derived]; see footnote (10) |
| Threshold price ladder | 1~5등급 against 1~2등급 at the same 가입금액 is about **4.5 : 1** (남 40: ₩15,010 against ₩3,300) | [S2, derived]; footnote (10) |
| Dementia severity ladder | 경도이상 : 중등도이상 : 중증 = **3.05 : 2.06 : 1.00** (남 40: ₩17,400 / ₩11,750 / ₩5,710) | [S2, derived] |
| Premium waiver (납입면제) | On award of **장기요양 1등급 or 2등급**, waiving the premiums of the main contract **and of every attached rider** from the next due date; it fires simultaneously with the 진단급여금 trigger | [S3]; threshold **[std]** (11) |
| Grace (납입유예기간), 월납 | 「납입기일부터 납입기일이 속하는 달의 **다음 다음달의 마지막 날**까지」; the contract terminates 「유예기간이 끝나는 날의 다음 날」, the insurer having given a 납입최고 of **at least 14 days** inside that window | [S1]; [REG-R25 제26조](#krlib-reg-r25) |
| Lapse assumption shape | Log-linear decay converging to **0.1% at 납입완료** and **0.8%** thereafter, as the FSC/FSS 원칙모형 for 무·저해지 business requires | [REG-R27]; [R14, secondary](#krlib-long_term_care-r14); **[std]** (12) |

9. Monthly is the dominant retail mode and the mode of every published rate card in the file
   [S1] [S2], which is also why the model runs on a monthly grid. 감독규정 제7-65조제2항
   expressly permits the 계약자적립액 to be computed 「연납보험료를 기준으로」 [REG-R18], and
   that permission is how a Korean monthly-premium product reconciles a monthly grid with an
   annually-recursed account — the same device the cancer chassis uses.
9a. **This is the one place in `krlib` where the pricing interest rate is a retrieved figure
    rather than a [std] one, and it is 50 basis points below the chassis's.** `Cancer_KR_S`
    carries a [std] 예정이율 of 2.50%, because no Korean carrier publishes one for that
    product; 우체국 publishes **2.0%** for this one, in terms, in a 기초서류 extract [S1].
    The composite takes the retrieved figure. Three cautions travel with it. It is a
    **2023-vintage** rate on a 2309 product, and the 예정이율 moves with the market. It is a
    **우정사업본부** rate, and 우체국 insurance is written outside 보험업법. And it is a rate
    for a contract whose 장기요양 riders sit on a 재해사망 main contract, so it prices a
    different mix from the composite's. It is nonetheless preferred to a [std] value because
    a retrieved number with three stated caveats is better evidence than an invented one, and
    because at 2.0% against 2.50% the composite is the **more conservative** of the two
    reference implementations on a benefit payable forty years out. The 계약자적립액 accrues
    at the same rate: no retrieved Korean long-term-care contract is 공시이율-linked, and a
    금리확정형 design on a 비갱신 protection contract is what all four documents describe.
10. Two facts here deserve to be read together, because they are in the same document and
    point in opposite directions [S2]. Long-term-care grade covers are **more expensive for
    women at every age**, matching the population certification rate (women are 70.9% of
    certified lives, and female 인정률 exceeds male from about 70 onward). Dementia diagnosis
    covers are **cheaper for women**, which is what the epidemiology predicts: the male
    dementia prevalence exceeds female at 65–79 and the female advantage appears only at 80+
    [R7], by which age much of the male exposure has died, so a CDR-triggered benefit picks up
    the male excess before the competing risk removes it. A model treating the two modules as
    sharing a sex basis will be wrong on one of them. On the threshold ladder: a 4.5 : 1 price
    ratio against a frequency ratio of about 7.5 : 1 implied by the 13.28% 1·2등급 share says
    that severe-grade claims arrive **later** on average, which is exactly what the
    progression argument above predicts, and is the best available market confirmation of it.
11. The waiver threshold is where this product differs most sharply from its Japanese
    counterpart. Observed: 삼성화재 makes the **award of 1등급 or 2등급 the 기본계약's own
    waiver event**, waiving the 기본계약 and every attached rider [S3]; 우체국 waives only the
    간병자금 rider's own premiums, on that rider's own trigger [S1]; ABL waives on a 장해지급률
    **50% 이상** state arising from one accident, i.e. on the ordinary 장해분류표 scale and
    not on the grade at all [S2]; 교보 refunds premiums on a 1~4등급 diagnosis, a materially
    different feature whose mechanics are not described and are [unverified] [S5]; not stated
    at 한화손해보험 [S4]. The composite takes **1·2등급, the same threshold as the benefit**,
    which is [S3]'s design and the only observed whole-contract waiver. The consequence is
    worth stating because it inverts the Japanese pattern: there, the waiver fires at a
    *lower* grade than the benefit and creates a band of lives paying nothing and claiming
    nothing, which is the single most mis-modelled item in that product. Here the waiver and
    the benefit fire on the **same event**, so the waiver is not an independent decrement —
    but it is not free either, because premiums stop for as long as the insured **survives in
    the care state**, and that duration is exactly the quantity the prevalence-to-incidence
    conversion above cannot pin down. The waiver is where post-onset mortality enters even a
    lump-sum-only version of this contract.
12. The lapse vector on a 무해지 form is not free. Following the 2024 계리가정 guidance, among
    models converging to zero lapse at 완납 the **로그-선형 (log-linear) 모형** is the
    **원칙모형** with a practical convergence point of **0.1%**, alternatives being permitted
    only within a closed list and only against disclosure in the audit report and the
    경영공시, external actuarial verification, quarterly reporting of the difference to the
    FSS in CSM, best-estimate liability, K-ICS ratio and net income, and submission to an
    on-site inspection; the post-완납 ultimate rate is **0.8%** [REG-R27]. The FSS named the
    problem it was fixing: with no experience on 무·저해지 business, insurers assumed high
    lapse right up to 완납, which flatters profitability, and the resulting switching out of
    표준형 products raised observed 표준형 lapse, which was then fed back into the 무해지
    assumption — 「악순환」 [REG-R27]. Applied from the 2024 year-end close. The technical
    notes carry a switch to a 표준형 assumption so the two can be compared, which is the
    comparison the guidance requires an insurer to disclose.

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| **장기요양진단급여금** (LTC diagnosis benefit) | **₩10,000,000**, paid **once only** (최초 1회한) on the first award of **장기요양 1등급 or 2등급** on or after the 장기요양상태 보장개시일. Payment extinguishes this benefit line; it does **not** terminate the contract | [S1] [S2] [S3] [S4]; threshold **[std]** (13) |
| 장기요양상태 보장개시일 | **계약일(부활일)부터 그 날을 포함하여 90일이 지난 날의 다음 날**, i.e. cover from day 91, with a **carve-back to 계약일 where the cause is 재해** (an accident within the 재해분류표) | [S2]; **[std]** (14) |
| 감액기간 (reduced-benefit period) | **1년, 50%** — where the certification is caused by 질병, 계약일부터 1년 미만 pays **50%** of the sum insured and 1년 이상 the full amount; where the cause is **상해/재해**, the full amount from the 보장개시일 | [S4]; **[std]** (14) |
| Pre-inception certification | Where 1·2등급 was awarded **before** the 보장개시일, that benefit is **무효** and **the premiums paid for it are returned** — 「특약을 무효로 하며, 이미 납입한 보험료를 돌려드립니다」 | [S1] [S2]; uniform where stated |
| **간병연금** (care annuity) | Monthly instalments beginning on the first 진단확정일 (판정일): **₩500,000 a month at 1등급, ₩300,000 at 2등급**, the amount set by the grade at **first** certification and never re-rated. Metered by an **annual survival test** on each anniversary of the 진단확정일, each passed test releasing the next 12 monthly instalments; the **first 12 months are guaranteed** against death; **120 months (10 years) maximum** | [S1]; shape **[std]** (15) |
| 간병연금 and the 감액 | The 감액 decision is **frozen at first certification**: a claim starting inside the reduction window is paid at 50% **for the whole ten years**, even though later instalments fall after the window closes | [S1] |
| 간병연금 on death | The stream terminates; where death follows a paid instalment **no 책임준비금 is returned** | [S1] |
| Surrender after the annuity starts | **Barred** — 「최초 지급사유가 발생한 후에는 이 특약을 해지할 수 없습니다」 | [S1] |
| **치매진단급여금** (dementia benefit) | Optional rider, **off in the base run**: ₩10,000,000 on the first 최종진단확정 of **경도치매상태 (CDR 1) or worse**, once only across the tier set, subject to a **one-year 보장개시일** and the definition's own **90-day persistence** requirement | [S2] [S4]; tier **[std]** (16) |
| Payment on non-covered death | The **계약자적립액 at the date of death** plus unearned premium, whereupon the contract terminates — the mandatory 제3보험 design rule of 감독규정 제7-63조제1항제1호, implemented by 표준약관 제22조 | [REG-R17] [REG-R25 제22조](#krlib-reg-r25); statutory floor [REG-R50 제736조](#krlib-reg-r50) |
| General death benefit | **None.** No retrieved life-side long-term-care contract pays a general death benefit; 우체국's main contract pays a **재해사망보험금** only, returning the 책임준비금 on non-accidental death | [S1] [S3]; **[std]** (17) |
| 만기환급금 | **None** — 「이 상품은 순수보장성보험으로 보험계약 만기시 지급받는 금액(만기환급금)이 없습니다」 | [S3] |
| Exclusions (면책) | 피보험자의 고의, 보험수익자의 고의, 계약자의 고의 [S1]; on the non-life side additionally 알코올중독·습관성 약품 또는 환각제, 전쟁·외국의 무력행사·혁명·내란·사변·폭동, and 임신·출산·산후기 [S4] | [S1] [S4] |
| Refusal on a defective certification | Where the grade was obtained by **허위 또는 부당 판정**, nothing is paid; ABL adds refusal where the public benefit is restricted under **노인장기요양보험법 제29조 (장기요양급여의 제한)** | [S1] [S2] [S4] |
| Contract termination | On maturity at 90세; on death (paying the 계약자적립액); on lapse; on rescission. **Payment of a benefit does not terminate the contract** — it extinguishes only the benefit line that paid | [S1] [S2] [S3]; **[std]** (18) |

13. **The threshold is the widest genuinely structural spread in this product, and every
    carrier draws it from the top of the scale downward.** Observed: **1등급 only** [S3] [S4];
    **1~2등급** [S1] [S2 as the main contract] [S3 as the 기본계약] [S4]; **1~3등급** [S3] [S4
    (1804)]; **1~4등급** [S3] [S4] [S5 for a premium refund]; **1~5등급** [S1] [S2] [S4] [S5];
    **1~인지지원등급** [S2] [S5]. **No retrieved document sells a 3등급-only or 5등급-only
    benefit**: the thresholds are always cumulative from 1등급. The composite takes **1~2등급**
    because it is the modal main-contract trigger, because it is the **statutory boundary
    between 재가급여 and 시설급여** [R6] and therefore the point at which the public scheme
    itself changes character, and because it is the only threshold for which a Korean carrier
    publishes an incidence rate [S1]. The threshold is a **model-point parameter** spanning
    1등급 to 1~인지지원등급 so that the whole observed spread is reachable without a second
    chassis — but note that widening it is not a re-scaling: at 1~5등급 the benefit is exposed
    to a population **7.5 times larger** on frequency and arriving materially earlier, which
    the market prices at about 4.5 : 1 [S2, derived].
14. **The waiting period and the reduction period are the least uniform parameters in this
    library, and the composite's combination is not observed in any single document — which is
    why it is justified here rather than asserted.** The observed range:

    | Carrier | 장기요양상태 보장개시일 | 감액기간 |
    |---|---|---|
    | 우체국 [S1] | **180일** — 「계약일[부활(효력회복)일]부터 그 날을 포함하여 180일이 지난 날의 다음날」; carve-back to 계약일 where the cause is 재해 | **2년, 50%**; disapplied where the cause is 재해 and on a 갱신계약 |
    | ABL생명 [S2] | **90일**, same construction; 재해 carve-back | **none stated** on the 장기요양 covers |
    | 삼성화재 [S3] | **none stated** | **none stated** |
    | 한화손보 [S4] | **none stated** | **1년, 50%** where 질병 is the cause; full amount where 상해 |

    So the market runs from **no waiting period at all** through 90 days to 180 days, and from
    **no reduction** through one year at 50% to two years at 50%. The composite takes **90
    days and one year at 50%** — the median of each range independently, and the combination
    of [S2]'s waiting period with [S4]'s reduction. Three reasons. First, taking the median of
    each separately is the only defensible rule when the two mechanisms are drafted
    independently and no carrier writes both at their extremes. Second, 90 days aligns the
    long-term-care benefit with the **90-day 암보장개시일** of the cancer chassis, so the two
    `krlib` third-sector products share one waiting-period mechanic and a reader can see the
    difference in the trigger rather than in the plumbing. Third, a **one-year** reduction is
    the level the cancer chassis also adopts, and adopting the two-year form would make the
    long-term-care module the only place in `krlib` where a 감액기간 runs past the first
    policy anniversary. Both are named [std] parameters and either can be set to zero. **Note
    the two mechanisms are different in kind and the 약관 keep them apart**: before the
    보장개시일 the *contract is void for that benefit and premiums come back*; inside the
    감액기간 cover has started and the benefit is merely halved.
15. Three architecturally different income forms were observed and the difference between them
    is the difference between a two-state and a three-state model.
    - **우체국 [S1]**: a survival-tested annuity — 「진단 확정된 날을 최초로 하여 **10년 동안
      매년 진단 확정일에 살아있을 때**」, with 「최초 1년(12개월) 보증지급」 and
      「10년(120개월)을 최고한도로 지급」, the monthly amount set by the grade at first
      certification and
      「그 이후에 장기요양등급이 변경되더라도 지급액은 변경되지 않습니다」.
    - **삼성화재 [S3]**: 장기요양 생활자금, 「**5년간 매월 가입금액**」, 최초 1회한. Whether
      the stream is 확정 (paid to the estate) or 생존-conditional is **not resolved** by the
      retrieved extract and is [unverified].
    - **ABL생명 [S2]**: six utilisation-tested 지원금 riders, each paying a flat **₩100,000
      per month** at 「"판정후 보험월" 기준 월 1회 한도」 but each conditioned on the insured
      *actually using* a named public benefit — 재가급여, 시설급여, 주·야간보호 or 복지용구 —
      with 특별현금급여 expressly excluded from counting as either 재가급여 or 시설급여, and
      two of the six payable 「최대 **종신**」.
    - **교보생명 [S5]**: 「매월 생활자금을 평생 지급」 with a **36-instalment (three-year)
      guarantee** on early death; the trigger is the CDR tier, not the grade.

    The composite takes the **우체국 shape**, for a reason that is about evidence rather than
    prevalence: every one of its six mechanical rules is stated verbatim in a **기초서류
    extract** [S1], so a reference implementation can reproduce the design exactly instead of
    inferring it. The ABL form is described in "Variations across insurers" and is **not
    modelled**, because a utilisation module's central assumption — a utilisation rate by
    grade, by service type and by duration since certification — is given by no retrieved
    source. [R4 표3-3](#krlib-long_term_care-r4) gives 급여이용 수급자 by service type (방문요양 675,070; 복지용구
    600,141; 노인요양시설 261,051; 주야간보호 213,428; 방문목욕 130,904; 방문간호 22,128;
    단기보호 2,372; 노인요양공동생활가정 18,965; 통합재가 2,347, out of 1,140,725 recipients
    with substantial overlap), which is a national aggregate and not the cross-tabulation the
    module would need. A module whose central assumption would be **entirely [std]** adds
    nothing to a reference implementation. **The 종신 form is a separate warning**: it carries
    the whole of the longevity tail after onset with no cap, on a post-onset mortality basis
    that nobody publishes.
16. Dementia cover is the second, quite separate line trading under the word 간병, and its
    trigger is the **CDR 척도** (한국판 Expanded Clinical Dementia Rating, 2001) assessed by a
    치매 전문의, not a public committee [S2] [S4]. The seven-point scale runs 0, 0.5, 1, 2, 3,
    4, 5, 점수가 높을수록 중증 [S2], and the contracts use 1 = 경도치매, 2 = 중등도치매,
    3 이상 = 중증치매. Two drafting conventions coexist: ABL defines 경도치매상태 as CDR
    **exactly 1** and must therefore write the 경도이상 benefit as an *or* across three states
    [S2], while 한화 defines 경증이상치매상태 as 「90일 이상 CDR척도 **1점 이상**」 so the
    tiering falls out of the definition [S4]. The economics are identical; the wording is not.
    The composite takes the **CDR 1 이상 (경도이상)** tier at ₩10,000,000, the commercially
    dominant form in the 2020s [R17] and the most expensive of the three, with the tier as a
    model-point parameter spanning CDR 1 / 2 / 3 and the observed **3.05 : 2.06 : 1.00** price
    ladder as its scaling check [S2, derived]. The epidemiology agrees with that ladder to a
    remarkable degree: 경증치매 (CDR 1–2) is **67% of all dementia cases** and 중증 the
    remaining 33% [R8], implying about 3 : 1 on prevalence alone against a 3.05 : 1.00 market
    price. The module is **off in the base run** because it is a rider on a different trigger
    with a different sex basis, and because it needs its own one-year waiting period.
17. No retrieved contract pays a general death benefit on the long-term-care cover.
    우체국's is the informative case: its 주계약 pays only a 재해사망보험금 — 「보험기간 중
    **재해를 직접적인 원인으로** 사망하였을 때」 — and returns the 책임준비금 on
    non-accidental death [S1], which is why that contract's headline premium runs male above
    female (item 9 of "Variations across insurers"). The composite pays nothing on death
    beyond the statutory 계약자적립액, which makes death a decrement with a small, non-zero
    cash flow attached — not the pure decrement it is in the Japanese product, and a direct
    consequence of 감독규정 제7-63조제1항제1호 [REG-R17].
18. Every 진단급여금 in the file is **최초 1회한** and extinguishes the rider paying it [S1]
    [S2] [S3] [S4], but the contract survives. That distinction matters in a contract carrying
    a lump sum, an annuity and a dementia benefit on one life: paying the lump sum leaves the
    annuity running and the dementia rider in force. One genuinely repeating benefit exists
    and is out of scope — 삼성화재's **두 번째 장기요양지원금(1~2등급)**, with a 「면책기간
    최초 1등급 또는 2등급의 장기요양등급판정일부터 **5년**」 and a re-test at that date [S3];
    see "Riders and options".

### Options

| Option | Representative value | Basis |
|---|---|---|
| Threshold parameter (`G_B`) | **1~2등급** in the base run; a model-point field spanning 1등급 / 1~2 / 1~3 / 1~4 / 1~5 / 1~인지지원등급 | [S1] [S2] [S3] [S4] [S5]; footnote (13) |
| 간병연금 module | **On** in the base run, on the 우체국 shape | [S1]; footnote (15) |
| 치매진단급여금 module | **Off** in the base run; CDR 1 이상, ₩10,000,000, one-year 보장개시일, 90-day persistence | [S2] [S4]; footnote (16) |
| 간편심사 (simplified underwriting) | **Off**; carried as a premium multiplier of 1.36–1.43× on the main cover, **not** as a second incidence basis | [S2]; footnote (7) |
| Surrender-value form | **해약환급금 미지급형** in the base run; **납입중50%지급형** and **표준형** as switches | [S1] [S2] [S4]; footnote (1) |
| 지정대리청구인 (designated proxy claimant) | Always designated. 「계약자가 본인을 위한 계약을 체결하는 경우 체신관서는 **원칙적으로 지정대리청구인을 지정하도록 하여야 합니다**」; eligible persons are 「피보험자의 가족관계등록부상의 배우자 또는 3촌 이내의 친족」, up to two, one as 대표대리인 | [S1]; 삼성화재 requires a handwritten or voice-recorded acknowledgement at proposal [S3]. No cash-flow effect; a mandatory operational feature of a product whose claimant usually cannot claim |
| 장애인전용보험전환특약 | Converts the contract into the 장애인전용 보장성보험 basket where the insured or beneficiary is a 소득세법 장애인, raising the tax credit from 12% to 15% | [S1] [S2]; [REG-R57] |
| 보험료 자동대출납입 / 보험계약대출 | **Neither is available during the premium-paying period** on the 미지급형 form: there is no surrender value to lend against, so a missed premium lapses the contract outright | [REG-R25 제33조](#krlib-reg-r25) [REG-R28]; **[std]** (19) |

19. 표준약관 제33조 permits a policy loan 「이 계약의 해약환급금 범위 내에서」 but adds
    「그러나 **순수보장성보험 등** 보험상품의 종류에 따라 보험계약대출이 제한될 수도 있습니다」
    [REG-R25]; the FSS made the same point explicitly in its 2019 consumer alert — a
    무해지환급금 contract **cannot support a policy loan during the payment period**
    [REG-R28]. With no loan there is no automatic premium loan, and with no automatic premium
    loan there is nothing to break the fall: the lapse is real and immediate. This is inherited
    from the cancer chassis unchanged and is stated again here because it interacts with the
    log-linear lapse assumption of footnote (12): the assumption says lapse **falls** toward
    납입완료 on a contract that has no soft landing at all.

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| 해약환급금 during 납입기간 | **Nil.** 「보험료 납입기간 중 계약이 해지될 경우 **해약환급금을 지급하지 않으며** …」 | [S2]; **[std]** (1) |
| 해약환급금 after 납입완료 | **50% of the notional 기본형 value.** 「보험료 납입기간이 완료된 이후 … '기본형' 해약환급금의 **50%**에 해당하는 금액」 | [S2] |
| The 기본형 comparator | A notional product that **cannot be bought**: 「'기본형'은 보험료 및 해약환급금(환급률 포함)의 비교, 안내만을 위한 상품으로 가입이 불가능하며, '기본형'의 해약환급금은 … **해지율을 적용하지 않고** 계산합니다」 | [S2] |
| Published progression (ABL, 40세, 주계약 1,000만원, 90세만기, 20년납, 월납, 일반심사형) | 남 환급률 0.0% at 1 / 5 / 10 / 15년, **48.7%** at 20년, 54.4% at 30년, 50.5% at 40년, 0.0% at 50년; 여 0.0% / **51.7%** / 61.1% / 59.6% / 0.0% on the same durations | [S2] |
| Shape | A **cliff, not a curve** — nil for the whole premium-paying period, a step at 납입완료, a slow rise to a peak around duration 30, and a decline to nil at the 90세 maturity of a pure protection contract | [S2]; and see [REG-R28] |
| Statutory floor | 해약환급금 = **계약자적립액 − 해약공제액**, floored at zero; the 해약공제액 may not exceed the **표준해약공제액** of 별표 14; the 해약공제기간 is the premium-paying period **capped at 7 years** | [REG-R19 제7-66조제1항](#krlib-reg-r19) [REG-R20] |
| Legal basis of the suppressed form | 감독규정 제7-66조제4항 permits a 순수보장성보험 whose premiums were calculated using a **최적해지율** to pay less than that floor, subject to the 환급률 conditions of 제4항제2호 | [REG-R19]; [REG-R28] |
| 계약자적립액 | Accrues **monthly before 납입완료 and daily afterwards**, per the 산출방법서, at the 예정이율 of 2.0% | [REG-R19 제7-66조제1항제4호](#krlib-reg-r19) [REG-R18]; rate [S1] |
| Unearned premium on termination | 「보험회사는 보험계약이 해지되는 경우 해약환급금에 **미경과 보험료 등을 가산한 금액**을 … 지급하여야 한다」 | [REG-R19 제7-66조제5항](#krlib-reg-r19) |
| Policyholder dividend | **None** — 무배당 | [S1] [S2] [S3] [S4]; [REG-R12] |
| 청약철회 (cooling off) | **15 days** from receipt of the 보험증권 and never after **30 days** from the application date; effective on despatch; premiums returned within 3 business days. Out of scope — the model starts from the point cover is in force | [REG-R25 제17조](#krlib-reg-r25) [REG-R51]; scope **[std]** (20) |
| 품질보증해지 | Cancellation **within three months of formation** where the 약관 or the policyholder's copy of the application was not delivered, the important content was not explained, or the policyholder did not sign; premiums returned with 보험계약대출이율 interest | [REG-R25 제18조제3항](#krlib-reg-r25); [REG-R49 제638조의3제2항](#krlib-reg-r49) |
| 실효 (lapse) | The day after the 납입유예기간 ends, the insurer having given a 납입최고 of at least 14 days | [S1]; [REG-R25 제26조](#krlib-reg-r25) |
| 부활 (reinstatement) | **Within three years** of termination, where the 해약환급금 has not been drawn — which on the 미지급형 form includes the case where there is none — on payment of arrears with interest within **평균공시이율 + 1%**; the insurer may not refuse because a claim event occurred before termination. **Reinstatement restarts the 보장개시일 clock** | [S1] [REG-R25 제27조](#krlib-reg-r25); footnote (21) |
| 계약 전 알릴 의무 | Rescission barred once **two years** have passed from the 보장개시일 without a claim event, or three years from the contract date, or one month from the insurer's discovery | [REG-R25 제13조·제14조](#krlib-reg-r25); [REG-R49 제651조](#krlib-reg-r49) |
| 사기에 의한 계약 | Cancellable **within five years of the 보장개시일 and one month of learning of the fraud** | [REG-R25 제15조](#krlib-reg-r25) |
| 소멸시효 | Three years on a claim | [REG-R49 제662조](#krlib-reg-r49) |
| Death of the insured | Contract terminates; the **계약자적립액** at death is paid | [REG-R17] [REG-R25 제22조](#krlib-reg-r25) |
| Maturity | 90세 계약해당일; **nothing payable** | [S3] |

20. 청약철회 is the 15-day withdrawal right of 금융소비자보호법 제46조 as implemented in
    표준약관 제17조, with three exclusions — an insurer-funded health examination, contracts
    of 90 days or less, and a 전문금융소비자 [REG-R25] [REG-R51]. `krlib` models from the
    point cover is in force and has no new-business funnel in which to represent a withdrawal,
    so the window is scoped out consistently across every product.
21. Reinstatement is **not a rewind**. Every waiting period in the file is measured
    「계약일[**부활(효력회복)일**]부터」 [S1] [S2], so a reinstated contract serves its 90-day
    long-term-care wait and its one-year dementia wait again from the 부활일. That matters more
    here than in the cancer chassis, because the pre-inception rule voids the benefit and
    returns premiums rather than merely refusing a claim: an insured certified during a lapse
    and reinstated afterwards has bought a benefit that can never pay for that certification.
    삼성화재's 두 번째 장기요양지원금 makes the reinstatement clock behaviour depend on what
    had happened before the lapse [S3], which is the only retrieved contract that addresses the
    interaction at all.

---

## Contractual mechanics

### The trigger, which is the whole product

Write `g` for a certification grade on the ordered scale

    1등급  >  2등급  >  3등급  >  4등급  >  5등급* ,  인지지원등급*

(the two starred grades being a **separate dementia gate**, not the bottom of the ladder —
see "Product overview"), and write `G_B` for the contractual threshold of the benefit,
1·2등급 in the composite. Then

    trigger(G_B, t) = 1  if the 등급판정위원회 has, at or before t, awarded the insured a
                         grade at or above G_B under the 노인장기요양보험법, and that
                         award is the first such award, and t is on or after the
                         장기요양상태 보장개시일
                    = 0  otherwise

There is **no second limb**. No retrieved Korean contract carries a company-basis ADL
schedule, a 180-day dependency test or an alternative definition of any kind [S1] [S2] [S3]
[S4] [S5]. That is the sharpest single contrast with the Japanese product, whose trigger is
always a disjunction of a public certification and a carrier-defined care state, and with the
French *assurance dépendance*, whose AGGIR grid is contractual. **The Korean insurer has
outsourced its claim definition to a statute and its claim adjudication to a public
committee.** The benefit clause therefore reduces to a cross-reference — 우체국's begins
「"장기요양상태"라 함은 거동이 현저히 불편하여 장기요양이 필요하다고 판단되어
「노인장기요양보험법」 및 관련 법령에 따라 등급판정위원회에서 장기요양 1등급 또는 2등급으로
판정받은 경우를 말하며 …」 [S1]. 한화손해보험's, from the article itself:

> 제1조(보험금의 지급사유) 「회사는 피보험자가 이 보장의 보험기간 중에 **노인장기요양보험
> 1등급 수급대상으로 인정된 경우**에는 **최초 1회에 한하여** 아래의 금액을 장기요양진단비로
> 보험수익자에게 지급합니다.」 … 「제1항의 "노인장기요양보험 1등급 수급대상으로 인정된
> 경우"라 함은 「노인장기요양보험법」에 따라 「**국민건강보험공단 장기요양등급판정위원회**」
> (향후 제도변경시에는 동 위원회와 동일한 기능을 수행하는 기관)에 의하여 "1등급"의
> 장기요양등급을 판정받은 경우를 말합니다.」 [S4]

and ABL's writes the statutory eligibility gate into the definition explicitly:

> 「"1~2등급 장기요양상태"라 함은 「만 65세 이상 노인」 또는 「**노인성 질병을 가진 만 65세
> 미만의 자**」로서 … 「노인장기요양보험법」에 따라 장기요양등급판정위원회에서 장기요양
> 1등급 또는 장기요양 2등급으로 판정받은 경우를 말합니다.」 [S2]

Four properties of the public limb belong in a model rather than in a footnote.

- **The claim date is the 판정일, and the determination is due within 30 days of the
  application**, extendable by up to a further 30 where a detailed investigation is needed
  [R3, citing 법 제16조제1항](#krlib-long_term_care-r3). On a monthly grid that lag is immaterial, but it interacts with
  the 보장개시일 arithmetic: the 90-day wait is measured from 계약일 to the **판정일**, and the
  insured's condition may have existed for months before that date. **Whether the award takes
  effect retroactively to the application date is not established by any retrieved
  document and is [unverified]**; the composite dates the claim at the 판정일, which is what
  the contracts say.
- **The certification has a finite 유효기간 and must be renewed, and the grade moves both
  ways.** The base period is two years; on renewal at the same grade it lengthens — before
  2025-07-01, 1등급 4년 / 2~4등급 3년 / 5등급·인지지원 2년, and from that date 1등급 **5년** /
  2~4등급 **4년** with the lightest two unchanged
  [R13, a vendor restatement](#krlib-long_term_care-r13) [REG-R55] — the decree text was not
  retrieved, so these values are [unverified] and are used only inside a sensitivity.
  **107,365** current certifications — 9.2% of the stock — arose from a
  등급변경신청 [R4 표2-5](#krlib-long_term_care-r4), so re-grading in both directions plainly happens; no retrieved
  source gives a transition matrix.
- **The composite's benefit is insensitive to all of that, and its annuity is deliberately
  insensitive too.** The 진단급여금 pays once on **first** award and cannot be re-triggered,
  and the 간병연금's amount is 「최초로 진단 확정된 장기요양등급(1등급 또는 2등급)을 기준으로
  … 지급액이 결정되며, 그 이후에 장기요양등급이 **변경되더라도 … 지급액은 변경되지
  않습니다**」 [S1], with instalments metered on **survival** rather than on continued
  certification. The care state is therefore **absorbing for cash-flow purposes**, and the
  contract is drafted so that it is. That is a real simplification the *contract* makes, not
  one the model imposes — and it is why a Korean 간병연금 needs a post-onset **mortality**
  basis but not a recovery basis, whereas a state-tested design would need both. The one
  retrieved contract that does contemplate recovery is 삼성화재's 두 번째 장기요양지원금
  ([S3], out of scope), which pays where the insured is at 3등급 이하 — 「장기요양상태가 아닌
  경우도 포함」 — five years after a first 1·2등급 award and is later re-certified.
- **The statute can move and the insurer cannot reprice.** No retrieved 간병보험 document
  gives the insurer a 기초율변경권 on the long-term-care benefit. What it gives instead is a
  wholesale rewriting clause:

  > 「법령의 개정에 따라 장기요양상태 판정기준이 폐지되거나 보험금 지급사유에 해당하는
  > 장기요양 등급 판정이 불가능한 경우 및 기타 금융위원회의 명령이 있는 경우에는 회사는
  > **객관적이고 합리적인 범위 내에서 기존 계약내용에 상응하는** "장기요양상태"와 관련된
  > 새로운 보장내용으로 이 계약의 내용을 변경합니다」 [S3]

  and the successor-body fallback inside the definition itself [S4]. **Both are
  contract-continuity provisions, not repricing provisions.** They keep the contract alive if
  the state abolishes the grades; they do not let the insurer raise the premium if the state
  loosens them. That asymmetry realised itself in 2018, when the creation of 인지지원등급 out
  of nothing enlarged the covered population of every 「1~인지지원등급」 rider overnight at no
  additional premium [R6] [S2]. A `krlib` sensitivity that shifts the grade thresholds is
  therefore not an academic exercise; it is the product's principal uninsurable risk.

### 장기요양진단급여금

    lump_sum(t) = A_B * 1{ t = first t at which trigger(G_B, t) = 1 } * r(t)

    r(t) = 0.50   where the certification is 질병-caused and t is inside the 감액기간
         = 1.00   otherwise

with `A_B` = ₩10,000,000 and the 감액기간 one year from 계약일. The benefit is paid **최초
1회에 한하여** and extinguishes this benefit line; the contract, the 간병연금 and any dementia
rider continue [S1] [S2] [S3] [S4]. Where the composite's threshold parameter is widened to a
multi-grade gate the benefit is still paid **once**, on the first award at or above the gate,
and never again on a subsequent deterioration — which is what makes a 1~5등급 benefit a much
earlier claim than a 1~2등급 one rather than a larger one.

Two drafting details worth carrying. The non-life documents add a causation limb — 「보험기간
중 **상해 또는 질병을 직접적인 원인으로** 장기요양상태가 되어」 [S3], and identically in [S4]
— which no retrieved life-side document has, and no retrieved document explains what a
certification *not* caused by 상해 또는 질병 would be. And the 감액 test is on the **cause**,
not the grade: [S4] pays the full amount inside the reduction window where the cause is 상해
and half where it is 질병. **The relative frequency of 상해 against 질병 as the cause of
certification is given by no retrieved source** [unverified], which is why the composite's
`r(t)` is written as a single fraction with the accident carve-out named but the split marked
[std] in the technical notes.

### 간병연금

    ann_start   = the 진단확정일 of the first award at or above G_B, on or after the
                  장기요양상태 보장개시일
    A_ann       = W500,000 per month  if that first award is 1등급
                = W300,000 per month  if that first award is 2등급          [frozen]
    r_ann       = 0.50 if ann_start falls inside the 감액기간, else 1.00    [frozen]

    test(k)     = 1{ insured alive on ann_start + k years },   k = 0 .. 9
    paid months = 12 for k = 0 (guaranteed), and 12 * test(k) for k = 1 .. 9
    annuity     = A_ann * r_ann * (paid months), capped at 120 months in total

The shape is: **a monthly amount, metered by an annual survival test, with the first twelve
months guaranteed against death and a hard 120-month ceiling** [S1]. Six mechanical rules
attach and each is a modelling decision, all six stated verbatim in the 상품요약서 [S1]:

1. **The premium waiver fires on the same event** — 「보험료 납입기간 중 … 간병자금 지급사유가
   발생하였을 때에는 **차회 이후의 이 특약의 보험료 납입을 면제**합니다」.
2. **The amount is frozen at the entry grade** — a life entering at 2등급 and deteriorating to
   1등급 keeps the ₩300,000 rate for all ten years.
3. **The 감액 decision is likewise frozen** — 「최초 진단 확정일을 기준으로 경과기간
   2년미만의 보험금 감액여부가 결정됩니다. 따라서 … 그 이후에 도래하는 매년 진단 확정일이
   계약일부터 2년이상에 해당하더라도 … 지급액은 변경되지 않습니다」. A claim starting inside
   the reduction window stays halved for the whole term of the annuity. **This is the single
   most easily mis-modelled rule in the product**: a model that re-tests the 감액 at each
   instalment date will overstate the benefit on every claim arising in the first policy year.
4. **The contract cannot be surrendered once the annuity starts** — 「최초 지급사유가 발생한
   후에는 이 특약을 해지할 수 없습니다」. Lapse is therefore zero in the care state, which is
   a constraint on the lapse vector and not merely an assumption.
5. **Death terminates the stream and returns nothing** — 「지급사유가 발생한 후 사망한
   경우에는 별도로 책임준비금을 지급하지 않습니다」. Where death precedes any claim the
   책임준비금 at death is paid to the 계약자, which is the general 제3보험 rule of
   제7-63조제1항제1호 [REG-R17] appearing in its product-specific form.
6. **Annual proof of life is required** — 「매년 진단 확정일에 피보험자의 **주민등록등본**을
   제출하여야 합니다」 [S1, 구비서류]. The survival test is an administrative event, not an
   actuarial abstraction.

**Why this benefit is the reason the model is three-state.** The lump sum needs only an entry
rate. The annuity needs the entry rate **and** a survival curve in the care state, and so does
the premium waiver, which stops the premium income for as long as the insured lives in the
state. The only retrieved evidence on that curve is [R11]: a right-censored decedent cohort
with a mean of 516.2 days, 8.7% dying within a month and 45.6% within a year, at a mean
인정점수 of 82.1 and with 74.7% of the decedents aged 75 or over. **It gives no survival
curve, no split by grade at entry and no age-specific rates**, so the post-onset mortality
basis in `LTC_KR_S` is entirely [std] — anchored on that cohort's one-month and one-year
figures for its early shape and on the 국가데이터처 완전생명표 [REG-R38] [REG-R39] for its
level, with a multiplicative impairment factor that the technical notes state, justifies and
varies in a sensitivity. The **120-month cap is the composite's protection against that
uncertainty**, and it is one reason the 우체국 shape was preferred over ABL's uncapped
종신 지원금 form.

### 납입면제

    premium(t) = 0  for every t after the first date at which trigger(G_W, t) = 1

with `G_W` = `G_B` = 1·2등급 [S3]. The waiver covers the main contract **and every attached
rider**, and waived premiums are treated as paid, so the contract continues in full force.

Because `G_W` equals `G_B` rather than sitting below it, the waiver is **not an independent
decrement** and the composite has no band of lives paying nothing and claiming nothing. But it
is not costless: it converts a level premium into a stream that stops at an uncertain date and
stays stopped for the duration of the care state. On the composite's specification — issue at
40, 20년납, a claim expected in the eighties — the waiver rarely bites inside the paying
period at all, which is exactly why the *interaction* between the waiver threshold and the
premium term is worth a sensitivity: at issue age 65 with a 10-year pay, it bites often.

**One observed design would need different machinery and is out of scope.** ABL waives on a
장해지급률 **50% 이상** state arising from one accident [S2] — that is, on the 표준약관's
장해분류표 percentage scale [REG-R25 부표 3](#krlib-reg-r25), a **continuous** disability measure with no
relation to the long-term-care grade. A contract carrying both waiver limbs has two decrements
into premium cessation, one of which is a scale and not a state.

### 보장개시일 and 감액기간 — two mechanisms that both get called "waiting period"

Korean practice keeps them apart and so must a model.

- **보장개시일** is the date cover *starts*. Before it nothing is payable, and the consequence
  of a pre-inception event is not that the claim is refused but that **the benefit is void and
  the premiums paid for it come back**: 「장기요양상태 보장개시일 전일 이전에 장기요양 1등급
  또는 2등급으로 진단 확정된 경우에는 **특약을 무효로 하며, 이미 납입한 보험료를
  돌려드립니다**」 [S1], and identically 「이 계약을 무효로 하며, 이미 납입한 보험료를 돌려
  드립니다」 [S2]. **The long-term-care covers have no revival clause**: unlike the cancer
  chassis, where a pre-inception diagnosis gives the policyholder a cancellation option and a
  five-year revival if untreated, here the benefit is simply gone.
- **감액기간** is a period during which cover *has* started and the benefit is paid at a
  stated fraction — invariably 50% in every retrieved document — measured from 계약일 to the
  판정일 [S1] [S4].

The composite runs a **90-day 보장개시일 with a 재해 carve-back to 계약일** and a **one-year
50% 감액 on a 질병-caused certification**, both [std] (footnote 14). Neither survives
reinstatement: both clocks restart from the 부활일 [S1] [S2].

**The dementia module runs a different and longer clock**, and its length is the market's
post-2019 settlement rather than a carrier choice. Both retrieved dementia contracts apply a
**one-year 보장개시일** — ABL as a waiting period with a carve-back to 계약일 where the cause
is 「재해로 인한 뇌의 손상」 [S2], 한화 as a flat one-year exclusion written into the benefit
name [S4] — and both additionally require, *inside the definition of the state itself*, that
the CDR state 「진단일부터 **90일 이상 계속되어** 장래에 더 이상의 호전을 기대할 수 없는」
[S2] [S4]. **The two together defer a mild-dementia claim by at least fifteen months from
inception and at least three months from first diagnosis**, and the effect on the first two
policy years' claim cost is large. A naive prevalence-based pricing of a CDR 1 benefit will be
badly wrong at short durations for that reason alone. ABL further grants a cancellation right
where the state arose before the 보장개시일 — 「진단일로부터 **90일 이내에 이 특약을 취소**할
수 있으며 … 이미 납입한 보험료를 돌려 드립니다」 — and provides that a policyholder who does
not cancel can never claim for that state, even on a later re-diagnosis after the 보장개시일
[S2].

### The dementia module, and why its waiting period is what it is

The one-year 면책 is the direct product of a supervisory intervention and is worth recording,
because a Korean 치매 experience series spanning 2019 is contaminated at the level of the
**benefit definition**, not merely of the rate [R8] [R10].

1. **Pre-2017**, 치매보험 covered 중증치매 (CDR 3 이상) only, which reaches about a third of
   dementia cases [R8].
2. **From 2017 H2** carriers began including 경증치매 (CDR 1 or 2), and in late 2018 the
   market moved within weeks. 치매보험 초회보험료 for 2018 was **약 233억 원, 3.5× the prior
   year**, and at non-life carriers **약 46억 원, 6.5×** [R8].
3. **The abuse**, named by the supervisor's own analyst: 경증치매 sums insured set 「증상에
   비해 지나치게 높게」, with **최대 3천만 원** offered for a CDR 1 diagnosis; unbounded
   duplicate purchase across carriers; and 약관 requiring 「CDR 척도**뿐만 아니라 뇌영상검사
   등을 기초로 한** 진단」, which [R8] predicted would generate mass dispute on the fact
   pattern 「CDR 1점 + 뇌 영상자료상 기질적 이상 없음」 [R8].
4. **March 2019**: 금융감독원 issues a 유의사항 안내 and a 보도참고자료; carriers respond with
   a self-imposed market-wide aggregate limit of **₩30,000,000** [R8].
5. **July 2019, the durable intervention**: a **약관 변경권고** requiring (i) diagnosis on a
   comprehensive clinical assessment of which 뇌영상검사 is one component, and (ii) deletion of
   특정 치매질병코드 and 약제투약 conditions added without rational basis, so that the benefit
   is payable 「전문의에 의해 치매로 진단되고, 보장대상 CDR척도 기준에 부합하는 경우」.
   Revised products on sale from **October 2019** [R10].

The settled wording, which the composite adopts [S2]:

> 「… 의료기관의 **치매 전문의(신경과 또는 정신건강의학과)**에 의한 진단서에 의하며, 이
> 진단은 병력청취, 인지기능 및 정신상태 평가, 신체진찰과 신경계진찰, 신경심리검사,
> 일상생활능력평가, 검사실검사, **뇌영상검사** 등 … 종합적인 평가를 기초로 정해지며,
> **뇌영상검사 등 일부 검사에서 치매의 소견이 확인되지 않았다 하더라도 다른 검사에 의한
> 종합적인 평가를 기초로 치매를 진단할 수 있습니다.**」

The final clause is the single most important sentence in the Korean dementia-insurance canon:
**brain imaging is an input, not a gate.** A dementia-specific exclusion travels with it —
「정신분열병이나 우울증과 같은 정신질환으로 인한 인지기능의 장애 및 알콜중독, 의사의 처방에
의하지 않는 약물의 투여로 인한 인지기능의 장애를 원인으로 발생한 "치매" …는 보장대상에서
제외합니다」 [S2].

**The two triggers are correlated, and the model must not treat them as independent.** Dementia
is simultaneously (i) a route *into* the public grade — four of the 25 노인성 질병 codes
[REG-R55], the **sole** qualifying condition for 5등급 and 인지지원등급 [REG-R55], and present
in **42.3%** of certified decedents [R11] — and (ii) an independent CDR-graded private trigger
[S2] [S4]. A contract carrying both a 장기요양(1~인지지원등급) rider and a 경도이상치매 rider
will pay both on the same underlying event, at different times and on different evidence.
That is not double counting — they are separate benefits with separate sums insured — but the
correlation is close to one at the light tiers, and a model treating them as independent
decrements understates the tail. `LTC_KR_S` makes the dementia module a rider on the **same
life with a shared underlying state**, not an independent process.

### 무해지환급형 — the surrender-value cliff and the regulation under it

**The machinery is the chassis's and is not restated here**: 해약환급금 = max(계약자적립액 −
해약공제액, 0), the 해약공제기간 capped at seven years, the 해약공제액 capped at the
**표준해약공제액** of 별표 14, the 제7-66조제4항 dispensation for a 순수보장성보험 priced on a
**최적해지율**, and the 제4항제2호 환급률 cap whose worked example is the FSC's 20년납
종신보험 at a 표준형 환급률 of 97.3% against a 무해지 134.1% [REG-R19] [REG-R20] [REG-R28].
Four things are specific to this product.

- **The Korean long-term-care market runs four forms, not two, and the names look almost
  identical.** ABL's 「해약환급금 미지급형」 pays **nil during** the paying period and **50%
  of a notional 기본형** after it [S2]; 한화손해보험's 「납입중50%해약환급금지급형」 pays
  **50% during** and restores to **100% after** [S4]; 삼성화재 sells the 순수보장성 form with
  no maturity value and describes no suppressed variant [S3]; and 우체국 is a conventional
  **표준형** with a normal surrender value from year 1, because it is 우정사업본부 business
  written outside 보험업법 and is not obliged to follow the industry's practice [S1]. A model
  that reads 「50%」 without reading which side of 납입완료 it attaches to will have the cliff
  upside down.
- **The published progression is a real cliff and is the cleanest in the library.** At 40세,
  주계약 1,000만원, 90세만기, 20년납, 월납, 일반심사형: 남 환급률 **0.0%** at years 1, 5, 10
  and 15, **48.7%** at year 20, 54.4% at 30, 50.5% at 40, and **0.0%** at 50 — nil for fifteen
  published durations, a step at 납입완료, a slow rise to a peak around duration 30, and a
  decline to nothing at the 90세 maturity of a pure protection contract; 여 51.7% / 61.1% /
  59.6% on the same durations [S2]. Those figures sit far below the 제4항제2호 ceiling, which
  is what one expects: on a pure protection contract there is very little 계약자적립액 to
  suppress in the first place, so the *headline* of the 미지급형 form overstates what it
  actually withholds.
- **The comparator is a fiction with a legal definition, and it is the link to the lapse
  vector.** The 「기본형」 cannot be bought — 「'기본형'은 보험료 및 해약환급금(환급률 포함)의
  비교, 안내만을 위한 상품으로 가입이 불가능하며, '기본형'의 해약환급금은 … **해지율을
  적용하지 않고** 계산합니다」 [S2]. That is the clearest retrieved statement that the
  suppressed form's pricing *does* use a lapse assumption while its comparator does not, and
  it is why footnote (12)'s lapse vector is a regulated quantity rather than a free one.
- **The disclosure obligation attaches to the form itself.** The insurer must compare and
  explain the 미지급형 and 기본형 premiums and 환급률 at formation, under an obligation set
  out in the **사업방법서 별첨 제1호** and requiring a signed acknowledgement [S2]. That
  사업방법서 is not published, which is the same document-availability gap that leaves every
  expense assumption in this product [std].

### 고지의무 and 계약 전 알릴 의무

Underwriting is by written declaration; no retrieved long-term-care product requires a medical
examination. The front door is narrow in exactly the place the anti-selection is, and the
simplified-underwriting card shows where: the fourth 간편고지 question is 「현재
노인장기요양보험에 의한 장기요양급여 수급자이거나 **장기요양인정 심의 중**입니까?」, alongside
the standard 3개월 / 2년 / 5년 questions, the five-year one naming 「암, 간경화증, 뇌졸중,
**경도인지장애, 치매** 또는 파킨슨병」 [S2]. **The thing being selected against is an
application to a public body that leaves a record**, and the questions are drafted to reach
both the award and the pending application.

The remedies are the chassis's unchanged — rescission barred one month after the insurer
learns of the breach, or **two years** from the 보장개시일 with no claim event, or **three
years** from the contract date, with the causation defence of 제14조제4항 and fraud separately
voidable within **five years** of the 보장개시일 [REG-R25 제13조·제14조·제15조](#krlib-reg-r25) [REG-R49
제651조](#krlib-reg-r49). One of them earns a mention here that it does not earn on the chassis: **제14조제5항
bars termination for non-disclosure of other insurance held**, and the dementia line's 2019
episode was in part a duplicate-purchase problem that carriers had to answer with a voluntary
₩30,000,000 market-wide aggregate limit rather than with a disclosure remedy [R8].

The composite is fully underwritten on the 일반심사 basis and carries the 간편심사 loading as
a premium multiplier only, for the reason given in footnote (7): the two are different risk
pools and no retrieved source gives the simplified pool's incidence separately.

### 청약철회, 품질보증해지, 실효, 부활 and expiry

The chassis specifies all five [REG-R25] [REG-R51] [REG-R49]; four points are this product's.

- **납입유예 and 실효.** The 요약서 states the grace period in its own words — 「납입기일부터
  납입기일이 속하는 달의 **다음 다음달의 마지막 날**까지」, the contract terminating
  「유예기간이 끝나는 날의 다음 날」 [S1] — within which the insurer must give a 납입최고 of
  **at least 14 days** [REG-R25 제26조](#krlib-reg-r25). With no surrender value, no policy loan and therefore
  no automatic premium loan, there is nothing to break the fall.
- **부활 restarts the cover, not the calendar.** Reinstatement is available for **three years**
  where the 해약환급금 has not been drawn — including the 무해지 case where there is none — on
  arrears with interest within 평균공시이율 + 1%, and the insurer may not refuse merely because
  a claim event occurred before termination [REG-R25 제27조](#krlib-reg-r25) [S1]. But **every 보장개시일 clock
  restarts from the 부활일** [S1] [S2], and because a pre-보장개시일 certification *voids the
  benefit* rather than merely going unpaid, an insured certified during a lapse and reinstated
  afterwards holds a benefit that can never pay for that certification.
- **품질보증해지** — three months from formation where the 약관 was not delivered or its
  important content not explained [REG-R25 제18조제3항](#krlib-reg-r25) [REG-R49 제638조의3제2항](#krlib-reg-r49). Out of
  scope, but worth noting that a product whose entire benefit definition is a cross-reference
  to a decree is exactly the kind on which the explanation duty bites hardest.
- **Expiry, and the annuity that can outlive the contract.** The contract ends on the 90세
  계약해당일 with nothing payable [S3]. The 간병연금's 120-month ceiling can therefore run past
  the policy term where the first certification occurs late — an insured certified at 85 has
  five years of term and ten years of annuity. **No retrieved document resolves whether
  instalments continue past maturity** and the question is [unverified]; the composite
  truncates the annuity at the earlier of the 120-month cap and the maturity date and marks
  the truncation [std], which is the conservative reading and materially understates the
  benefit for late entrants.

### Claim administration, and why it is a contractual mechanic here

Two features exist because the person entitled to claim usually cannot.

- **지정대리청구인.** 우체국's 요약서 makes designation near-compulsory — 「계약자가 본인을
  위한 계약을 체결하는 경우 체신관서는 **원칙적으로 지정대리청구인을 지정하도록 하여야
  합니다**」 — and requires the office to operate 「장기요양상태로 인한 보험금 청구불능을
  방지하기 위한 적정한 관리 체계」; eligible persons are 「피보험자의 가족관계등록부상의
  배우자 또는 3촌 이내의 친족」, up to two, one designated 대표대리인 [S1]. 삼성화재 requires
  a handwritten or voice-recorded acknowledgement at proposal for the same reason [S3].
- **Evidence.** The document proving the trigger is the **장기요양인정서**, and for the annuity
  the insured must submit a **주민등록등본** on each anniversary of the 진단확정일 [S1]. Both
  are administrative documents produced by the state, which is the whole character of this
  product's claims process: there is no adjudication of a clinical question, only production
  of a certificate. That is why the Korean 간병보험 claims record is nothing like the Korean CI
  claims record, where the word 중대한 generated a decade of litigation.

The corresponding refusal grounds are administrative too: 「피보험자가 장기요양등급을 판정
받았으나 **허위 또는 부당 판정사실이 확인되는 경우**」 nothing is paid [S1] [S2], and ABL adds
refusal where the public benefit is restricted under **법 제29조 (장기요양급여의 제한)** [S2]
[S4] — a private benefit conditioned on the continued availability of a public one.

---

## Riders and options

**In scope (modelled or parameterized):**

- **장기요양진단급여금** — ₩10,000,000 at 1·2등급, 최초 1회한, behind a 90-day 보장개시일 with
  a 재해 carve-back and a one-year 50% 감액 on 질병 causation [S1] [S2] [S3] [S4].
- **간병연금** — ₩500,000 / ₩300,000 a month by entry grade, annual survival test, 12-month
  guarantee, 120-month cap, amount and 감액 both frozen at first certification [S1]. On in the
  base run; switchable off, which reduces the contract to a lump-sum-only cover and removes
  most (not all) of the dependence on the post-onset mortality basis.
- **납입면제** — on award of 1·2등급, covering the main contract and every rider [S3]. Always
  on; the threshold is a parameter and may be set below `G_B`.
- **치매진단급여금** — ₩10,000,000 at CDR 1 이상, once only across the tier set, behind a
  one-year 보장개시일 and a 90-day persistence test inside the definition [S2] [S4]. Off in
  the base run; the tier is a parameter spanning CDR 1 / 2 / 3.
- **Threshold parameter `G_B`** — a model-point field spanning 1등급, 1~2, 1~3, 1~4, 1~5 and
  1~인지지원등급, so the entire observed market spread is reachable on one chassis [S1] [S2]
  [S3] [S4] [S5].
- **Surrender-value form** — 미지급형 (base), 납입중50%지급형, 표준형 [S1] [S2] [S4].
- **간편심사 loading** — a premium multiplier of 1.36–1.43× [S2], off in the base run.
- **장애인전용보험전환특약** — a tax-basket switch with no cash-flow effect in the model [S1]
  [S2] [REG-R57].

**Out of scope:**

- **간병인사용일당 / 입원간병인사용 riders** — 우체국's mandatory 입원간병인사용특약 pays
  「8시간미만 3만원 / 8시간이상 6만원」 per day of carer use in a non-요양병원 hospital [S1],
  and ABL and 한화 carry equivalents [S2] [S4]. A hospital-days frequency-severity product
  with an acute Korean loss-ratio problem [R15]; it shares nothing with the grade-triggered
  benefit but the word 간병. The one published rate for it is a **frequency, not a
  probability**: 「질병 및 재해 입원간병인사용률」 runs 0.494541 to 2.303485 across ages and
  sexes and is expressed in days [S1].
- **ABL's utilisation-conditioned 지원금 riders** — 재가급여지원, 시설급여지원,
  주야간보호지원, 복지용구지원, each ₩100,000 a month conditioned on actual use of the
  corresponding public benefit, two of them 「최대 종신」 [S2]. Described in "Variations
  across insurers"; not modelled, for the reason in footnote (15).
- **삼성화재's 두 번째 장기요양지원금(1~2등급)** — a genuine **persistency** benefit with a
  「면책기간 최초 1등급 또는 2등급의 장기요양등급판정일부터 **5년**」, paying where at that
  date the insured still holds 1·2등급, or has been re-graded to 3등급 이하 (「장기요양상태가
  아닌 경우도 포함」) and is later re-certified within the term; it extinguishes itself where
  no 1·2등급 award has occurred and fewer than five years of term remain [S3]. It needs exactly
  the continuance basis that nobody publishes.
- **삼성화재's 장기요양 생활자금 (5년 월지급형)** — 「5년간 매월 가입금액」, survival test
  unstated and [unverified] [S3].
- **교보생명's premium refund on a 1~4등급 diagnosis** and its lifetime dementia annuity with a
  36-instalment guarantee [S5] — press-release facts whose reserve mechanics are not
  described.
- **치매 통원급여금 and the 노인성 질환 riders** (관절염수술, 인공관절치환,
  중증무릎관절연골손상, 대상포진, 통풍), which are 10년 만기 자동갱신부 [S2].
- **급여가정간호치료보장특약**, **CDR 검사지원비 특약** [R17] and the 레켐비 (lecanemab)
  covers appearing in 2024–2025 launches [R17].
- **청약철회** and the new-business funnel [REG-R25 제17조](#krlib-reg-r25) [REG-R51].
- **The long-term-care acceleration inside `CI_KR_S`** — a critical-illness contract whose
  장기요양상태 trigger is 1·2등급 with its own 90-day 보장개시일. The two products share a
  statutory trigger and nothing else: `CI_KR_S` pays **one** accelerated benefit on the first
  of several events, `LTC_KR_S` pays a standalone benefit on the grade alone. See
  [the CI product specification](../ci_insurance/product-spec.md).

---

## Variations across insurers

The consolidated comparison, five carriers. "—" means the retrieved documents for that carrier
do not state it.

| Feature | 우체국 [S1] | ABL생명 [S2] | 삼성화재 [S3] | 한화손보 [S4] | 교보생명 [S5] |
|---|---|---|---|---|---|
| Sector | 우정사업본부 (outside 보험업법) | 생보 | 손보 | 손보 | 생보 |
| Document type | 상품요약서 (기초서류 extract) | 보험안내자료 | **약관** | **약관** | press release |
| Vintage | 2023 (2309) | 2025-09 (2504) | 2018-08 (1808.2) | 2023-07 | 2026-02 |
| Main-contract benefit | 재해사망보험금 | **장기요양(1~2등급)급여금** | 상해사망 + **장기요양지원금(1~2등급)** | 장기요양진단비 (plan-dependent) | 치매 진단자금 + 장기요양 |
| Grade thresholds offered | 1~2, 1~5 | 1~2, 1~5, **1~인지지원** | **1, 1~2, 1~3, 1~4** | **1, 1~2, 1~3, 1~4, 1~5** | 1~5, 인지지원 |
| Income form | **10-year monthly annuity**, survival-tested, 12-month guarantee, 120-month cap | **utilisation-tested monthly 지원금**, ₩100,000/month, two of them 종신 | **5년 월지급형 생활자금**, 가입금액 per month | — | **lifetime monthly**, 36-instalment guarantee |
| Annuity amount graded by grade | **yes** — 1등급 ₩500,000 / 2등급 ₩300,000 | no (flat ₩100,000) | no | — | not stated |
| Dementia cover | none | **CDR 1 / 2 / 3 이상** + 통원 riders | none in retrieved extract | **CDR 1 / 2 / 3 이상 (90일 이상)** + 파킨슨병 | 경도 / 중등도 / 중증 |
| 장기요양 보장개시일 | **180일** (재해 carve-back) | **90일** (재해 carve-back) | **none stated** | **none stated** | — |
| 장기요양 감액기간 | **2년, 50%** | none stated | none stated | **1년, 50%** (질병 only) | — |
| 치매 보장개시일 | n/a | **1년** | n/a | **1년** (full exclusion) | — |
| Repeat / persistency benefit | no | no | **두 번째 장기요양지원금**, 5-year 면책 | no | no |
| Surrender-value form | **표준형** (normal CV from year 1) | **미지급형** — nil in period, 50% of 기본형 after | 순수보장성, **만기환급금 없음** | **납입중50%지급형** — 50% in, 100% after | — |
| 갱신형 | LTC riders 비갱신; 간병인 riders 5/10년 갱신 | LTC/치매 비갱신; 노인성질환 riders 10년 갱신 | not stated | not stated | — |
| 가입나이 | 만15~70 (1종) / 30~70 (특약) | 25~75 (일반) / 30~75 (간편) | 만15~60 | — | 30~75 |
| 보험기간 | 85 / 90 / 100세만기 | 90 / 95 / 100세만기 | 90 / 100세만기 | — | 종신 |
| Simplified underwriting | **yes**, 2종, 3 questions; LTC riders **not attachable** | **yes**, 4 questions incl. current 장기요양 status | not stated | 유병자 plans referenced | — |
| Published rates | **예정이율 2.0%; 예정위험률 incl. 요양 1·2등급 발생률** | **full 월납 card, 25 covers × 3 ages × 2 sexes** | none | none | none |
| 납입면제 | on the annuity trigger (that rider only) | 장해지급률 50% 이상 | **1·2등급 award waives 기본계약 and all riders** | — | premium refund at 1~4등급 |

The itemised divergences, in descending order of how much they change the model.

1. **Benefit-threshold menu.** 1등급 only [S3] [S4]; **1~2등급** [S1] [S2] [S3] [S4]; 1~3등급
   [S3] [S4]; 1~4등급 [S3] [S4] [S5]; **1~5등급** [S1] [S2] [S4] [S5]; 1~인지지원등급 [S2]
   [S5]. Always cumulative from the top; no 3등급-only or 5등급-only benefit anywhere.
   Composite: **1~2등급** (footnote 13). This is the widest structural spread in the product,
   and widening the gate does not scale the benefit — it changes both the frequency and the
   timing.
2. **Income form.** This is the **most model-relevant divergence** and the three designs do not
   differ by a parameter, they differ by what basis they need. A 우체국-style annuity needs
   only a post-onset **survival** basis — instalments run for up to ten years on survival
   alone, regardless of recovery, re-grading, or whether services are used [S1]. An ABL-style
   지원금 needs, in addition, a **utilisation** basis: the insured must be receiving the named
   public benefit in the month [S2], and Korean utilisation is high in aggregate (급여이용
   수급자 1,140,725 against 인정자 1,165,030, 97.9% [R4]) but is not published by grade,
   service type and duration. An ABL 종신 rider needs a **lifetime** post-onset survival basis
   with no cap. Composite: the 우체국 shape (footnote 15).
3. **Waiting period and reduction period.** None / 90일 / 180일 and none / 1년 50% / 2년 50%,
   in every combination observed except the composite's own (footnote 14). This is a wider
   spread than any comparable parameter in `krlib` and is the reason the composite's choice is
   justified against the range rather than asserted as market convention.
4. **Premium waiver trigger.** The **1·2등급 award itself**, waiving the whole contract [S3];
   the annuity trigger, waiving only that rider's premiums [S1]; a 장해지급률 50% 이상 state
   from one accident, on the 장해분류표 scale and unrelated to the grade [S2]; a premium
   *refund* at 1~4등급 [S5]. Composite: the [S3] design (footnote 11).
5. **Surrender-value form.** 표준형 with a normal value from year 1 [S1]; 미지급형, nil during
   / 50% after [S2]; 순수보장성 with no maturity value and no 무·저해지 variant described
   [S3]; 납입중50%지급형, 50% during / 100% after [S4]. Composite: 미지급형 (footnote 1).
6. **Dementia cover.** Present as three CDR-graded riders plus 통원 riders [S2]; present as
   three CDR-graded covers plus 파킨슨병진단비, all behind a one-year exclusion [S4];
   present as a three-tier lifetime-annuity design [S5]; **absent** at two carriers [S1]
   [S3]. Where
   present, the CDR thresholds, the 90-day persistence test and the one-year waiting period are
   **invariant**. Composite: a rider at CDR 1 이상, off in the base run (footnote 16).
7. **Renewal architecture, and issue-age and term envelopes.** Every retrieved document
   writes the long-term-care benefit **비갱신형** and attaches renewal to the hospital-carer
   and 노인성 질환 riders travelling with it [S1] [S2]; nothing to standardize, and the
   invariance is the finding (footnote 2). Envelopes: 만15~70 / 85–100세만기 [S1]; 25~75 /
   90–100세만기 [S2]; 만15~60, tightening to **만15~37** on a 100세만기 전기납 rider [S3];
   30~75 / 종신 [S5]. The whole market issues from about 15–30 to about 70–75 — far younger
   than the age at which any claim can arise. **A 30-year-old buying a 1·2등급 benefit is
   buying a claim expected around age 85.** Composite: 30–70 to 90세 (footnotes 3 and 5).
8. **Simplified underwriting.** Present at both life-side writers [S1] [S2] and referenced at
   one non-life writer [S4], with loadings of 1.16–1.31× [S1] and 1.25–1.80× [S2] depending on
   the cover. **우체국 will not attach its 장기요양 riders to the simplified chassis at all**
   [S1], which is itself a statement about anti-selection on this trigger. Composite: fully
   underwritten (footnote 7).
9. **The sex direction, and the fact that it reverses inside one document.** Female rates
   exceed male on **every** 장기요양 cover at **every** age, the ratio running 1.19–1.61 and
   widening with age (여 60 / 남 60 = 2.18 on the 1-2등급 시설급여종신 rider); female rates
   fall **below** male on **every** 치매 cover (경도이상치매 여 40 ₩13,920 against 남
   ₩17,400, a ratio of 0.80) [S2, derived]. 우체국's headline male premium of 2.375 times the
   female is neither of these — it is a **재해사망** ratio on that carrier's main contract
   [S1, derived], and reading it as a long-term-care premium is the easiest mistake in the
   file.
10. **What does not vary, and this is the invariant core of the composite.** Every product
    defines its long-term-care trigger **solely** by reference to a 장기요양등급 awarded by the
    등급판정위원회 under the 노인장기요양보험법 [S1] [S2] [S3] [S4] [S5]; **no product carries
    a company-basis ADL alternative**; every 진단급여금 is **최초 1회에 한함** and extinguishes
    the benefit line that pays it [S1] [S2] [S3] [S4]; every product is **무배당** [S1] [S2]
    [S3] [S4]; every one names **허위 또는 부당 판정** as a ground for refusal [S1] [S2]; every
    one contemplates a **지정대리청구인** because the claimant cannot claim [S1] [S3]; every
    dementia benefit uses the **CDR 척도** with a **90-day persistence** test and a
    **one-year** waiting period [S2] [S4]; and **no carrier other than 우체국 publishes any
    rate, incidence or interest, at all** [S1].

---

## Regulatory context

**The shared frame is specified in full by the cancer chassis and is not restated here.** The
제3보험 licence and its 제4조제3항 deeming provision [REG-R1] [R12], the closed 보험상품 scope
of 시행령 제1조의2 [REG-R7], the 기초서류 filing regime [REG-R2], the 산출방법서's five
필수기재사항 and the 현금흐름방식 requirement for a contract longer than three years
[REG-R18 제7-64조](#krlib-reg-r18), the surrender-value regime of 제7-66조 through 제7-70조 [REG-R19] with its
별표 14 cap [REG-R20], the expense and commission bounds [REG-R29] [REG-R22], the 표준약관's
contractual furniture [REG-R25], the 상법 제4편 floor beneath it [REG-R49] [REG-R50], the
K-ICS and IFRS 17 measurement regimes and the 해약환급금준비금 that sits on top of them
[REG-R13] [REG-R60] [REG-R11], and the 예금자보호법 limit of **₩100,000,000 (1억원)** per
person per insurer [REG-R52] [REG-R32] all apply here unchanged. What follows is what is
different, and it is mostly about the *definition* of the insured event rather than about the
insurer.

**Classification, and the thing on the other side of the trigger.** 간병보험 is a **named
보험종목 in its own right**, not a species of 질병보험: 보험업법 제4조제1항제3호 lists
상해보험, 질병보험 and 간병보험 as three coordinate 종목 [R12] [REG-R1]. The public scheme the
trigger points at is **not insurance business at all**: it is social insurance under the
노인장기요양보험법, administered by 국민건강보험공단, with the Minister setting the 급여비용
annually by benefit type and grade and a 본인부담금 imposed on the recipient, reducible by up
to 60% for listed low-income groups [REG-R54]. Nothing in the Korean insurance-supervision
ladder reaches that scheme, and nothing in the health-and-welfare ladder reaches the insurer.

**Product design.** 감독규정 제7-63조제1항제1호 requires a 제3보험 product to pay, on **death
from a cause the policy does not cover**, the **계약자적립액** and the 미경과보험료 of
제7-66조제5항, and to terminate [REG-R17]; 표준약관 제22조 implements it and 상법 제736조 is
the floor beneath it [REG-R25] [REG-R50]. Inherited from the chassis unchanged, and repeated
here only because it is the reason `LTC_KR_S` carries an account balance despite being pure
protection: **death is a decrement with a cash flow attached**, and on this product the
insured dies in the care state more often than not.

**A surrender-value consequence that is unique to this product.** 별표 14 caps the surrender
charge at **연납순보험료의 5% × 해약공제계수 + 보장성보험의 보험가입금액의 10/1000**
[REG-R20]. But a long-term-care contract has **no
보험가입금액 in the ordinary sense**, because it pays no death benefit, and 별표 15 supplies
the substitute: where 제3호 (일반사망보험금) does not apply, 제9호 computes a notional amount
at the 기준연령 요건 as

> **보험가입금액 = (위험보험료 / 정기보험의 위험보험료) × 정기보험의 보험가입금액**

excluding from that risk premium, among other items, 「**치매 또는 일상생활장해 등 타인의
간병을 필요로 하는 상태** 및 이로 인한 치료 등의 위험 발생시 지급하는 보험금을 위한 부분」
[REG-R21]. **Read literally, the schedule excludes long-term-care risk premium from the very
ratio that gives a care-only contract its notional 보험가입금액.** The consequence — that a
pure 간병보험's 표준해약공제액 is driven almost entirely by the 연납순보험료 term and barely at
all by the 10/1000 term — is an inference from the schedule's text rather than a statement made
anywhere in it, and the technical notes carry it as such. It has no counterpart in `uslib`,
`uklib`, `jplib`, `frlib` or `delib`, where no regulation prescribes the surrender charge at
this level.

**Reserving and capital: cited, not specified, and one point about the horizon.** 책임준비금
[REG-R3] [REG-R10], the **해약환급금준비금** [REG-R11], the K-ICS 요구자본 and its 경과조치
[REG-R13] [REG-R35] and the IFRS 17 risk adjustment and CSM [REG-R60] are cited and not
implemented, as they are on the chassis. What is worth adding here is the **duration**: the
IFRS 17 discount curve uses 관찰금리 to a **최종관찰만기 currently 20 years** — extending to
30 from 2025 over a three-year phase-in — then interpolates to 60 years and converges on a
**장기선도금리 currently 4.55%**, with a **유동성프리미엄 currently 91bp** added [REG-R27]. A
contract issued at 40 to a 90세 maturity puts the modal claim **forty-five years out**, deep
inside the extrapolated segment, so on this product more of the liability's measured value is
determined by the LTFR and the convergence rule than by any observable market rate. What the
regimes require of the projection is that it be re-runnable on a re-set assumption basis at a
stated 기준일 — which, for a contract whose benefit definition sits in a decree, is not a
formality.

**The actuarial basis, and where the [std] boundary falls.** Two holes, both structural rather
than researchable.

- **Mortality.** 보험개발원 releases only 평균수명 and 기대여명 summary statistics for the
  **제10회 경험생명표** applied from 2024-04; the qx table itself goes to member insurers
  [REG-R33] [REG-R34]. There is no Korean analogue of a downloadable standard table. **Every
  `mort_table.csv` in `krlib` is therefore a [std] construction** anchored on the public
  국가데이터처 생명표 [REG-R38] [REG-R39] and the two published KIDI summary figures, carrying
  a `provenance` column on every row. This product needs **two** such tables — a healthy-life
  decrement and a post-onset impaired-life decrement — and only the first has even a public
  anchor.
- **Morbidity.** 참조순보험요율 are filed with the FSC under 보험업법 제176조 [REG-R4], and on
  the **life** side they stay unpublished, becoming visible only as the ratio called the
  보험가격지수 [REG-R22]. For **장기손해보험** the 제176조제9항 publication permission is
  exercised: 보험개발원 puts a dated numeric display on its own site carrying, among others, an
  「기타피부암 및 갑상선암 이외의 암 발생률」 grid and a 질병입원율 grid by age and sex,
  which is why `Cancer_KR_S`'s incidence basis is source-tagged rather than [std] [REG-R61].
  **That display carries nothing for 장기요양**, and **보험개발원 publishes no 장기요양
  incidence table and no post-onset mortality table at all** [R9] [REG-R61].
  The morbidity hole is filled here by public administrative data — the 인정률 and grade
  composition of the 통계연보 [R4] [REG-R42] — which is a **prevalence** and requires the
  conversion set out above. The only disclosed pricing basis in the file is one carrier's own
  예정위험률 [S1], and it is a rate card for a select underwritten population, not an estimate
  of population incidence. **The reference implementation does that construction in public, row
  by row, in `model.md`,** which is the same discipline the third-sector regime elsewhere
  imposes on insurers privately.

**Lapse.** The 계리가정 guidance of 2024-11 is the binding constraint and is described in
footnote (12): a **log-linear** decay to **0.1%** at 납입완료 as the 원칙모형, **0.8%**
thereafter, with a closed list of permitted alternatives and heavy disclosure attached
[REG-R27] [R14, secondary](#krlib-long_term_care-r14). Applied from the 2024 year-end close.

**Expenses.** No 사업방법서 and no 보험료 및 해약환급금 산출방법서 was retrieved for any
Korean long-term-care product — [S2] refers to both by name but neither is published — so
**no 예정사업비율, no 표준해약공제액 application and no 신계약비 상각 schedule appears in any
source behind this specification**, and every expense assumption in `LTC_KR_S` is [std]. It is
bounded from above by 별표 14 [REG-R20] and cross-checked against the FSC's rules of thumb —
**13 times the monthly premium** for a 보장성보험's 표준해약공제액, annual commission not
exceeding **60%** of it, and the instalment total at least 5% above the up-front total
[REG-R29] [REG-R22]. The 산출방법서's five 필수기재사항 — including, for a contract longer
than three years, an adequacy analysis on **최적기초율** with projected cash flows — are
제7-64조 [REG-R18].

**Conduct — and the word the 표준약관 uses for this product.** The 표준약관 clauses this
specification relies on are the chassis's and are enumerated there [REG-R25]. Two items in it
belong specifically to 간병보험. Its **제3조** lists the five categories a Korean life policy
pays on, and the fifth is 「입원보험금 등」 — 「질병이 진단확정되거나 입원, 통원, 요양, 수술
또는 **수발**이 필요한 상태가 되었을 때」 — so **수발**, the need to be cared for by another,
is the 표준약관's own word for what this product pays on, and 간병보험 is the only `krlib`
product that attaches to it. Its **장해분류표 (부표 3)** defines 장해 as a **permanent**
impairment remaining after treatment, expressly excluding temporary states during treatment,
and is the percentage scale behind ABL's alternative waiver limb [REG-R25] [S2] — a
**continuous** measure of impairment sitting alongside a **discrete** statutory grade in the
same contract.

**A statutory cross-reference between two `krlib` products.** The 실손의료보험 표준약관's
**비급여 할인·할증**
five-band table, effective 2024-07 and re-cut in the 2026-05-06 fifth generation, excludes the
claims of insureds holding **장기요양 1등급 or 2등급** under the 노인장기요양보험법 from the
twelve-month claims count that sets the relativity [REG-R25] [REG-R54]. So the same statutory
grade that triggers this product's main benefit also shields a `Medical_KR_S` policyholder from
a surcharge. It is the only direct statutory link between two `krlib` products.

**Tax.** Premiums fall in the **보장성보험료 세액공제** basket — a credit of **12%** of
premiums on a contract 「만기에 환급되는 금액이 납입보험료를 초과하지 아니하는 보험」, capped
at **₩1,000,000 (100만원)** of premium a year, so at most **₩120,000** of relief, and **15%**
for a 장애인전용보장성보험 [REG-R57]. 우체국 states it in its own 요약서 [S1] and both
life-side carriers ship a 장애인전용보험전환특약 [S1] [S2], which is a live option on a product
whose buyers are, by construction, people anticipating dependency. Two product-specific points.
The composite's anchor premium of ₩5,600 a month is **₩67,200 a year**, so the cap does not
bind and **every won of this product's premium attracts the credit** — which is not true of
the cancer chassis's ₩45,000 a month, ₩540,000 a year, where a second protection contract in
the same household would exhaust the basket. And on a **무해지** contract the qualifying test
is satisfied trivially: there is no maturity value at all, so the contract cannot fail the
「만기 환급금 ≤ 납입보험료」 condition however long it runs.

**The residual risk, stated once more because it is the product.** Every regime above regulates
the insurer. None of them regulates the thing that determines whether this contract pays: the
장기요양등급 판정기준 in 노인장기요양보험법 시행령 제7조, and the 보건복지부 고시 measuring
the 장기요양인정 점수 that feeds it — **which was not retrieved and whose content is therefore
not established here** [REG-R55]. The insurer's contractual response to a change in that
standard is a rewriting clause and a successor-body fallback [S3] [S4], neither of which is a
repricing right. A Korean 간병보험 book is short a call on the state's own definition of
dependency, at a fixed premium, for up to sixty years.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-long_term_care-r1
[R10]: #krlib-long_term_care-r10
[R11]: #krlib-long_term_care-r11
[R12]: #krlib-long_term_care-r12
[R15]: #krlib-long_term_care-r15
[R16]: #krlib-long_term_care-r16
[R17]: #krlib-long_term_care-r17
[R18]: #krlib-long_term_care-r18
[R2]: #krlib-long_term_care-r2
[R3]: #krlib-long_term_care-r3
[R4]: #krlib-long_term_care-r4
[R6]: #krlib-long_term_care-r6
[R7]: #krlib-long_term_care-r7
[R8]: #krlib-long_term_care-r8
[R9]: #krlib-long_term_care-r9
[REG-R1]: #krlib-reg-r1
[REG-R10]: #krlib-reg-r10
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
[REG-R32]: #krlib-reg-r32
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R35]: #krlib-reg-r35
[REG-R38]: #krlib-reg-r38
[REG-R39]: #krlib-reg-r39
[REG-R4]: #krlib-reg-r4
[REG-R42]: #krlib-reg-r42
[REG-R43]: #krlib-reg-r43
[REG-R49]: #krlib-reg-r49
[REG-R50]: #krlib-reg-r50
[REG-R51]: #krlib-reg-r51
[REG-R52]: #krlib-reg-r52
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
