# Product Specification

**Status:** Draft, 2026-09-03 (all cited sources accessed 2026-09-03).

**Scope note.** This is a *standardized composite specification* of the Korean
single-premium immediate annuity, 즉시연금 (*jeuksi yeongeum*), assembled for reference
liability cash-flow modelling as `Immediate_KR_S`. It does not describe any single
insurer's contract. Facts carrying a source tag — [S#] (primary product documents:
약관 (*yakgwan*, policy conditions), 상품요약서 (*sangpum yoyakseo*, the statutory
product summary), 상품안내장 (sales leaflet), 사업방법서 (*saeop bangbeopseo*, business
method statement) and 공시 (disclosure) pages) and [R#] (regulatory, statutory, judicial
and statistical references), both numbered per `_research/immediate-annuity.md` and
resolved in `sources.md` in this directory (that numbering is frozen and is never
renumbered) — were extracted from the cited document. [REG-R#] tags resolve against the
cross-product reference library `references/regulatory-and-actuarial-references.md`,
whose own R-numbering runs R1–R62 and is distinct from this product's. Values marked
**[std]** are standardizations introduced for the reference implementation; each [std]
table row carries a numbered footnote giving the rationale and, where the research
bracketed one, the observed range across insurers. Claims the research pass could not
confirm against a retrieved document are flagged [unverified].

Korean terms are written in Hangul with an English gloss and, on first use, a Revised
Romanization in italics. Amounts are in Korean won; because Korean documents quote in
만원 (10,000) and 억원 (100,000,000), both forms are given where a Korean reader would
expect it — ₩100,000,000 (1억원). Ages are 보험나이 (*boheom nai*, insurance age) unless
a population statistic is quoted, in which case they are 만나이 (age last birthday); the
distinction is stated at every point of use because the six-month rule makes the two
differ for half of all issue dates [S7 제23조] [REG-R25 제21조](#krlib-reg-r25).

The mechanics anchor is 하나생명's 「무배당 행복knowhow즉시연금보험」 상품요약서 [S1] —
the only complete statutory product summary for an 즉시연금 retrieved, and the only
document in the corpus that publishes the expense load by component, the annuitant
mortality rates and the surrender-value run — with 교보생명 [S2] [S3], 동양생명 [S4] and
삼성생명 [S5] as the illustration set, ABL생명's filed 사업방법서 [S6] as the only
retrieved 기초서류 (*gicho seoryu*, filed basis documents), and 한화생명's 2024 약관 [S7]
as the post-dispute drafting. 푸본현대 [S8], 우체국보험 [S9], 하나생명 [S13] and IBK연금
[S14] are **deferred** annuities and are cited only for payout-phase machinery, never
for an issue-age, premium or expense parameter.

**One caveat governs the whole document and is not repeated at every point of use.**
Every 즉시연금-specific product document retrieved is of 2011–2017 vintage, and no
currently marketed product bearing that name was located at a major carrier in this
research pass; the 2023–2026 sources are deferred annuities offering immediate-style
payout elections [S7] [S13] [S14]. Whether the product is still written under that name
is therefore **[unverified]**, and this specification is written **to the mechanism**
rather than to a named live product. The market picture in the next section rests on a
single academic dataset covering FY2008–FY2009 [R12] and is fifteen to eighteen years
old; no aggregate for any later year was obtained.

---

## Product overview and market role

즉시연금 is the payout phase of a life-insurance annuity standing alone. The
supervisor's own definition: 「즉시연금은 보험을 가입할 때 보험료 전액을 일시에 납입하고,
그 다음달부터 매월 연금이 지급되는 보험상품」 [R2 §1](#krlib-immediate_annuity-r2). A single premium is paid, the
insurer deducts an acquisition and administration load and, where a death benefit is
attached, a risk premium — all once, at inception — and the residue is credited at a
declared rate and drawn down as an annuity from one month after the 보장개시일 (cover
commencement date). There is no premium term, no accumulation phase, no lapse decrement
and no acquisition strain after t = 0. Everything the liability does happens on the
payout side, which is exactly why this product sits in `krlib` alongside — and not
inside — `Pension_KR_S`, whose subject is the accumulation half of the same machinery.

Contractually the product is **two contracts sold as one**: 「계약자는 다음에 정하는
보장계약과 연금계약을 동시에 체결하여야 합니다」 — a 보장계약 (protection contract)
funding the death benefit and a 연금계약 (annuity contract) funding the 생존연금
(*saengjon yeongeum*, survival annuity) and, where the shape has one, the 만기보험금
(*mangi boheomgeum*, maturity benefit) [R1, quoting the 약관 제3조](#krlib-immediate_annuity-r1). The single premium
A splits three ways — 보장계약 보험료 B, 사업비 C, and the residue D = A − B − C which
becomes the 연금계약 적립액, elsewhere and hereafter the **계약자적립액**
(*gyeyakja jeongnimaek*, the policyholder's account balance) [R1 §1-가](#krlib-immediate_annuity-r1).

**Korea writes the product in three shapes, and they are not variants of one design but
three genuinely different liabilities.** The vocabulary is stable across every retrieved
carrier and the model treats the shape as a model-point column, not as a rider:

- **종신연금형** (*jongsin yeongeum-hyeong*, life annuity) divides the fund by an annuity
  factor built from an annuitant mortality table and the declared rate and pays for life,
  with a 보증지급기간 (*bojeung jigeup gigan*, guaranteed payment period) of 10 or 20
  years, or to age 100, or equal to the annuitant's statutory 기대여명
  (*gidae yeomyeong*, life expectancy). It cannot be surrendered once in payment
  [S3] [S5] [S7 제31조].
- **상속연금형** (*sangsok yeongeum-hyeong*, inheritance annuity) pays **interest only**
  and returns the capital — on death in every case, and at maturity in the 만기형 (term)
  sub-shape. It uses no mortality in the annuity calculation at all and remains
  surrenderable throughout [S1] [S3] [R12 §III-1](#krlib-immediate_annuity-r12).
- **확정기간연금형** (*hwakjeong-gigan yeongeum-hyeong*, annuity-certain) divides the
  fund over a fixed term irrespective of survival, again without mortality, and also
  remains surrenderable [S3] [S9 별표1] [R12 §III-1](#krlib-immediate_annuity-r12).

**In the Korean market the middle shape dominates, and that single fact reorients the
product.** On the only public micro-dataset — 1,414 contracts written by one insurer over
FY2008–FY2009, said to be about 30% of the market's premium — 73.6% of contracts by count
and 75.1% by premium were 상속형, against 18.2% and 18.6% 종신형 and 8.2% and 6.3%
확정형 [R12 표5](#krlib-immediate_annuity-r12). The paper draws the comparison itself: 「종신형(72%) 즉시연금이 주류를
이루는 미국과 달리 우리나라는 상속형 중심으로 즉시연금에 가입하고 있다」 [R12 §III-2](#krlib-immediate_annuity-r12).
The Korean buyer is, in the main, **not hedging longevity**. The buyer is parking a large
sum in a tax-privileged wrapper, drawing the interest, and preserving the principal for
an heir. A model calibrated on a US or UK immediate-annuity book — where the life shape
is the product — will mis-weight this one by a factor of four.

The buyer profile is equally particular: 70% female, mean issue age 66.6 and median 68 on
a 45–85 range, mean premium ₩185,000,000 (1억 8,500만원) and **median ₩100,000,000
(1억원)**, with 38.5% of contracts at or above ₩100,000,000 and a maximum of
₩4,000,000,000 (40억원) [R12 표2, 그림3](#krlib-immediate_annuity-r12). Ages 65 and over are 63% of contracts and 70
and over are 44% [R12 표4](#krlib-immediate_annuity-r12). Of 종신형 buyers, **97.3% chose the ten-year guarantee** and
2.7% chose twenty [R12 표7](#krlib-immediate_annuity-r12); of 확정형 buyers, 77.6% chose ten years, 13.8% fifteen and
8.6% twenty. Those two distributions are why this composite's representative terms are
ten years on every shape and not a longer round number.

Every retrieved 즉시연금 document is a **방카슈랑스** (bancassurance) leaflet or a
bank-channel summary — 하나은행 [S2] [S4] [S5], SC제일은행 [S3], 우체국 [R27]. The
product is sold across a bank counter to a customer with a large deposit, and the very
low commission rates in the one document that publishes them — 2.08% of the single
premium in year one on the life shape and 1.75% on the inheritance shape, nil thereafter
[S1 §VII] — are consistent with that channel and with nothing else in Korean retail life
insurance.

**The single most consequential thing about this product in Korea is a dispute, and it
belongs in the specification rather than in a footnote.** The 만기환급형 variety of
상속연금형 promises both a monthly annuity and the return of the whole single premium at
maturity — but the premium *net* of expenses is less than the maturity benefit, so part
of each period's interest must be retained to rebuild the fund. That retention was set
out in the 산출방법서 (*sanchul bangbeopseo*, the filed premium and reserve calculation
basis) and **not** in the 약관 handed to the policyholder. On 14 November 2017 the
금융감독원's 금융분쟁조정위원회 (*geumnyung bunjaeng jojeong wiwonhoe*, Financial Dispute
Resolution Committee) held in 조정결정 제2017-17호 that the retention could not be
asserted against the policyholder [R1]; the supervisor extended the ruling to the whole
industry on 15 March 2018 [R2 §4](#krlib-immediate_annuity-r2); insurers litigated, lost at first instance across four
carriers, won on appeal, and were finally upheld by the Supreme Court on 16 October 2025
[R6] [R21] [R22]. News reporting put the disputed sum at up to ₩1,000,000,000,000 (1조원)
across about 160,000 contracts, with no supervisory document stating any aggregate
[R17] [R18] [R19] [R24] — every figure of that kind in this document is news-sourced and
says so. No other product in this repository carries a dispute of that shape: a mismatch
between the actuarial basis and the contract wording, adjudicated on the law of
standard-form contracts. **Any Korean immediate-annuity model that does not carry the
retention as an explicit, switchable term is modelling the wrong liability**, and the
representative specification below carries it as a switch with two settings.

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Single-premium immediate annuity; **무배당** (non-participating); **금리연동형보험** (*geumni yeondonghyeong boheom*, interest-sensitive), the 계약자적립액 credited at a monthly-reset 공시이율 with a duration-stepped guaranteed floor | [S1] [S3] [S6] [S7]; chassis **[std]** (1) |
| Regulatory class | 생명보험 / 저축성보험 (*jeochukseong boheom*, savings insurance) in the sense of 감독규정 제1-2조제4호; **연금보험** for the purposes of the 공시이율 product-class uniformity rule | [REG-R9 제1-2조](#krlib-reg-r9) [REG-R23 제5-16조제4항](#krlib-reg-r23) |
| Payout shapes | Three, elected at inception and irrevocable: **종신연금형**, **상속연금형 만기형**, **확정기간연금형**. Each is a model-point column of one projection | [S1] [S3] [S6]; scope **[std]** (2) |
| Selling mode | **1종 / 즉시형** only — the annuity commences one month after the 보장개시일. The 2종 / 거치형 (1–5 year deferral) is out of scope | [S3] [S4] [S5] [S6]; scope **[std]** (3) |
| Issue age (가입나이) | **45–80**, 보험나이 | [S1] [S2] [S3] [S4] [R27]; adoption **[std]** (4) |
| Age basis | **보험나이**: 만나이 at the 계약일 with a remainder under six months discarded and six months or more rounded up to a year, incrementing on each 계약해당일 | [S7 제23조] [REG-R25 제21조](#krlib-reg-r25) |
| Annuity commencement age (연금개시나이) | Equal to the issue age; there is no deferral | [S1] [S3] [S4] |
| Sex | Male and female rated separately on the life shape only; the other two shapes use no mortality in the annuity calculation | [S1 §IV-2] [R12 §III-1](#krlib-immediate_annuity-r12) |
| Lives basis | Single life; 계약자 = 피보험자 = 수익자 on the life shape, which is a tax condition and not a preference | [REG-R58 영 제25조제4항제4호](#krlib-reg-r58); scope **[std]** (5) |
| Currency | KRW | [S1]–[S9] |
| Participation | 무배당 (non-participating) throughout | [S1] [S5] [S6]; adoption **[std]** (6) |
| Underwriting | Light but not absent: a health examination may be required on the basis of age, other cover held and the 계약 전 알릴 의무 answers, and a substandard-acceptance rider is offered | [S1 §II-6] [S1 §III-1] |
| **Anchor model cell** | Male, **보험나이 60**, single premium **₩100,000,000 (1억원)**, 종신연금형 with a **10-year 보증지급기간**, 공시이율 2.50%, annual payment grid | [S1] [R12]; adoption **[std]** (7) |

Footnotes to [std] rows:

1. Every retrieved carrier writes the product as a non-participating interest-sensitive
   contract crediting a monthly-reset 공시이율 over a duration-stepped floor
   [S1 §IV-4] [S3] [S5] [S6 §9] [S7 제7조]. No 금리확정형 (fixed-rate) 즉시연금 and no
   participating one was retrieved. The chassis is therefore not a choice between
   observed alternatives; it is the only shape observed, and the **[std]** tag records
   that no negative evidence was sought.
2. Observed menus differ sharply in what they omit rather than in what they contain:
   확정기간연금형 is **absent** from 하나생명 [S1], 동양생명 [S4], 삼성생명 [S5] and the
   2016 교보 vintage [S2], while 상속연금형 appears on all seven retrieved 즉시연금
   products and is absent only from the state provider's deferred contract [S9]. Where
   확정기간연금형 is absent the 상속연금형 만기형 does the same commercial job in a
   different shape. All three are carried because two of them — the ones with no
   mortality in the annuity — are the market's centre of gravity [R12 표5](#krlib-immediate_annuity-r12) and because
   the reference implementation needs a shape whose liability is pure interest
   arithmetic to isolate the crediting mechanic.
3. Almost every retrieved product is sold in both modes [S3] [S4] [S5] [S6]. The 거치형
   is an accumulation contract with a payout election attached, and its 추가납입
   (top-up premium), 중도인출 (partial withdrawal) and pre-annuitisation 사망보험금 are
   `Pension_KR_S`'s subject, not this one's. Excluding it keeps `Immediate_KR_S` to the
   payout phase standing alone, which is what this product exists in the library to
   demonstrate.
4. Observed bands: **45–80** at 하나생명 [S1], 교보생명 [S2] [S3], 동양생명 [S4] and
   우체국 [R27]; **40–85** at 삼성생명 [S5]; **45–75** at ABL [S6]. The realised range in
   the one dataset is 45–85 [R12 표2](#krlib-immediate_annuity-r12), and the paper reports the market-wide position for
   2008–2010 as 「가입연령도 45세~85세로 한정」 [R12 §III-2-가](#krlib-immediate_annuity-r12). 45–80 is adopted as the
   modal published band; it also bounds the projection sensibly, because a life annuity
   issued at 85 has a guarantee period longer than its expected payment period.
5. No retrieved document requires 계약자 = 피보험자 = 수익자 as a matter of product
   design. 소득세법 시행령 제25조제4항제4호 requires it for the 종신형 tax exemption
   [REG-R58], and one carrier's summary states the consequence rather than the condition:
   「순수종신연금형을 선택한 경우, 연금지급이 개시된 이후 해지 불가」 [S5 주2]. Third-party
   arrangements exist — 삼성 publishes a 연금선수익자 / 연금후수익자 mechanism [S5] and
   ABL a 부부계약 (joint-life) form [S6] — and both are out of scope (see Riders and
   options). Single-life, single-party is the reference basis.
6. 무배당 appears in the product name of five of the seven retrieved 즉시연금 products —
   하나 [S1], 교보 [S2], 동양 [S4], 삼성 [S5] and ABL [S6]; the two that do not are the 2017
   교보 vintage [S3] and the state provider's 2011 contract [R27]. (The 무배당 in the names
   of [S7] and [S8] is not evidence about this product line: both are deferred contracts
   and are cited for payout-phase machinery only.) ABL's 사업방법서 contemplates a
   participating sibling and
   requires that 「'다'의 공시이율은 동종상품의 배당보험 공시이율보다 높게 적용한다」
   [S6 §9-라], i.e. the non-participating declared rate must be the higher of the two.
   No participating 즉시연금 rate scale was retrieved, and 계약자배당 [REG-R12] is
   therefore neither specified nor modelled.
7. 감독규정 제1-2조제2호 defines the **기준연령 요건** as a 40-year-old male on
   whole-term, monthly-premium terms, and provides that where a 40-year-old male cannot
   buy the product — which is the case here, the floor being 45 — the **mid-point of the
   issue-age range** is used instead [REG-R9]. On a 45–80 band that is 62 or 63. Age
   **60** is adopted in preference because it is the age on which the one carrier that
   publishes an expense breakdown publishes it (남자 60세, 일시납) [S1 §VIII], the age
   on which the same carrier publishes its 모집수수료율 (남자 60세, 일시납 1억원)
   [S1 §VII], and the age at which the published 개인연금사망률 anchors are densest
   [S1 §IV-2]; and because it sits inside the modal 60–74 age band, which is 54% of
   contracts [R12 표4](#krlib-immediate_annuity-r12). The premium is the dataset's **median** [R12 그림3](#krlib-immediate_annuity-r12) and is exactly
   the 소득세법 ten-year exemption cap for contracts made from 2017-04-01 [REG-R58], so
   the anchor cell sits on the tax boundary the product is designed around. The
   ten-year guarantee is the choice 97.3% of life-shape buyers actually made [R12 표7](#krlib-immediate_annuity-r12).

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium mode | **Single premium (일시납)**, paid once at inception. There is no premium-paying period, no renewal premium and no 추가납입 on the 즉시형 | [S1] [S2] [S3] [S5] [S6] |
| Representative premium | **₩100,000,000 (1억원)** | [R12 그림3](#krlib-immediate_annuity-r12); adoption **[std]** (8) |
| Minimum premium | **₩10,000,000 (1,000만원)** | [S2] [S3] [S4] [S5] [R12 §III-2-가](#krlib-immediate_annuity-r12); adoption **[std]** (9) |
| Maximum premium | **₩5,000,000,000 (50억원)**, stepping down by age band on the inheritance shape | [S1 §II-5] [S5]; adoption **[std]** (10) |
| Premium unit | ₩1,000,000 (100만원) | [S1] [S2] [S3] [S4] |
| Premium split at inception | 단일 보험료 A = 보장계약 보험료 B + 사업비 C + 연금계약 순보험료 D; D becomes the opening 계약자적립액 | [R1 §1-가](#krlib-immediate_annuity-r1) [S1 주2] |
| 계약체결비용 (*gyeyak chegyeol biyong*, acquisition cost) | **2.20%** of the single premium, deducted once at inception | [S1 §VIII]; adoption **[std]** (11) |
| 계약관리비용 (*gyeyak gwalli biyong*, administration cost) | **1.30%** of the single premium, deducted once at inception | [S1 §VIII] |
| Total one-off expense load | **3.50%** of the single premium | [S1] [S3]; adoption **[std]** (11) |
| 위험보험료 (*wiheom boheomnyo*, risk premium) | **0.00%** on 종신연금형; **1.47%** of the single premium, deducted once at inception, on 상속연금형 and 확정기간연금형 | [S1 §VIII]; adoption **[std]** (12) |
| Opening 계약자적립액 | 96.50% of the single premium on 종신연금형; **95.03%** on the two shapes carrying the death benefit | derived from the rows above; **[std]** (13) |
| Annuity-period charge | **0.80% of the 연금연액** (*yeongeum yeonaek*, annual annuity amount) each year in payment, treated as an insurer expense cash flow measured on the annuity rather than as a reduction of the payment | [S1 §VIII]; treatment **[std]** (14) |
| 모집수수료 (commission) | **2.00%** of the single premium at t = 0, nil thereafter | [S1 §VII]; adoption **[std]** (15) |
| Surrender deduction | **Nil at every duration** | [S1 §VIII] [S10] |
| Large-contract discount | Not applied | [S6 §10-나] [R27]; scope **[std]** (16) |
| 중도인출 / 추가납입 | Not available on the 즉시형 | [S2] [S3] [S5] [S6]; single exception at [S6 §8-나] (17) |

8. ₩100,000,000 is the median premium of the only public dataset [R12 그림3](#krlib-immediate_annuity-r12) and one of
   the two round figures every retrieved illustration is built on (the other being
   ₩50,000,000 at [S1 §VI-2]). It is also the 소득세법 cap, which makes it the modal
   contract size for a reason rather than by accident [REG-R58].
9. Observed minima: **₩10,000,000** at 교보 [S2] [S3], 동양 [S4] and 삼성 [S5];
   **₩40,000,000** at 하나 [S1]; **₩50,000,000** at ABL [S6]; **₩5,000,000** at the state
   provider in 2011 [R27]. A consumer explainer reports the spread directly —
   「M사는 1천만원, S사는 3천만원 등」 [R16, secondary](#krlib-immediate_annuity-r16). ₩10,000,000 is modal among the
   commercial carriers and matches the dataset's observed minimum [R12 표2](#krlib-immediate_annuity-r12).
10. 하나생명 steps its 상속형 cap **down** with age — ₩5,000,000,000 for ages 45–60,
    ₩3,000,000,000 for 61–70 and ₩1,500,000,000 for 71–80 — while capping the 종신형 at
    ₩10,000,000,000 (100억원) [S1 §II-5]; 삼성 caps at ₩5,000,000,000 [S5]; the state
    provider capped at ₩250,000,000 [R27]. The age-stepped inheritance cap is an
    anti-selection and estate-planning control rather than a mortality one, and it is
    adopted in outline — a flat ₩5,000,000,000, the age-banding recorded in this footnote
    and nowhere else — because the model's premium domain needs a bound and not a
    schedule. The Variations table below carries the minimum premium by carrier and not
    the maximum.
11. [S1 §VIII] publishes the load by component **and by shape** on a 남자 60세, 일시납
    ₩50,000,000 basis: 종신연금형 계약체결비용 2.61% + 계약관리비용 1.30% = 3.91%;
    상속연금형(20년만기) 2.19% + 1.30% = 3.49%. The composite adopts a single
    **2.20% + 1.30% = 3.50%** across all three shapes rather than carrying the carrier's
    0.42-point allocation difference, because a second, independent document supports the
    same total: solving the annuity-certain identity against 교보's published
    확정기간연금형 figures at a 공시이율 of 2.52% reproduces all four published terms
    within 1.4% on a total first-day deduction of 4.97% (3.50% expense plus 1.47% risk
    premium) — see the cross-check under Contractual mechanics. Two carriers, two
    documents, one number. The disputed 2012 contract's load was higher —
    사업비 5.325% [R1 §1-가](#krlib-immediate_annuity-r1) plus a 보장계약 보험료 the determination does not state, with
    the supervisor's worked example assuming 6.0% of a ₩100,000,000 premium in total
    [R2 참고](#krlib-immediate_annuity-r2) — and that vintage is recorded under Variations, not defaulted.
12. [S1 §VIII] publishes three risk-premium levels on the same basis: **0.00%** for
    종신연금형 1형, which pays no death benefit once the annuity has begun; **4.9466%**
    for 종신연금형 2형, which keeps one for life; and **1.4669%** for 상속연금형
    (20년만기). The composite's life shape is the 1형 design and therefore carries none;
    the two shapes that keep a 10%-of-premium death benefit carry 1.47%. The figure is
    disclosed on a **twenty-year** 상속 basis at exactly the anchor age, so applying it
    unscaled to a ten-year contract is conservative — the true ten-year risk premium is
    materially lower — and the direction of the error is stated rather than corrected,
    because no source supports a term scaling.
13. 100% − 3.50% = 96.50% and 100% − 3.50% − 1.47% = 95.03%. The identity is the one the
    약관 states in words: 「연금계약적립액이란 … 연금계약순보험료(사망보장이 있는 경우
    납입하신 보험료중 보장을 위한 보험료 및 예정사업비를 차감한 금액)를 공시이율로
    납입일부터 일자계산에 의하여 적립한 금액」 [R1, quoting the 약관 서두](#krlib-immediate_annuity-r1), and which the
    상품요약서 repeats [S1 주2].
14. [S1 §VIII] states the charge as 「연금수령기간 중 비용 — 연금연액의 0.80%」 on all
    three shapes and discloses it in the cost table rather than in the benefit table. The
    composite therefore models it as an insurer expense measured on the 연금연액 and does
    **not** net it off the policyholder's payment. Whether a carrier's own 산출방법서
    builds it into the annuity factor instead is **[unverified]** — no filed basis
    document for an 즉시연금 discloses the annuity formula, and [S6], the one 사업방법서
    retrieved, does not reach it.
15. Observed: **2.08%** of the single premium in year one on 종신연금형 and **1.75%** on
    상속연금형, nil in every later year, on a 남자 60세 일시납 1억원 basis [S1 §VII].
    2.00% is a **round figure inside that pair** and not their mid-point, which is 1.915%;
    it is carried in preference to 1.915% because the sub-basis-point precision would be
    spurious across two shapes and one carrier. The internal consistency that matters is
    that it sits
    **below** the 2.20% 계약체결비용, so the acquisition cost taken from the fund at
    inception covers the commission paid out of it at the same moment; the reference
    implementation has no acquisition strain and no deferred acquisition cost to
    amortise, which is the structural difference between this product and every other in
    `krlib`.
16. One carrier publishes a size discount and it is the only place in the retrieved
    corpus where a Korean annuity price varies with contract size: 0.3% of the single
    premium for ₩100,000,000–₩200,000,000, rising through four bands to 1.5% of the
    excess over ₩500,000,000 plus ₩3,500,000, with 「계약자가 원할 경우 할인된 금액을
    연금계약 순보험료에 더하여 적립한다」 [S6 §10-나]; the state provider gave a flat
    0.5% for premiums of ₩100,000,000 or more [R27]. It is excluded because it is a
    single-carrier feature and because it enters the model as nothing more than a
    reduction of the load, which the load parameter already spans.
17. 추가납입 and 중도인출 are 거치형 features on every retrieved product [S2] [S3] [S5]
    [S6]. On an 즉시연금 there is no accumulation phase in which to pay more in or take
    money out. The single retrieved exception is ABL's 상속연금형 종신플랜, where partial
    withdrawal survives annuitisation: 「'가'에도 불구하고 상속연금형 종신플랜의 경우
    연금이 개시된 이후에도 연금계약 계약자적립금의 일부를 인출할 수 있다」 [S6 §8-나]. It
    is recorded and not modelled. Where any carrier does allow a withdrawal the charge is
    the most uniform parameter in the entire corpus — 「인출금액의 0.2% (2,000원 한도)」
    with four free withdrawals a year, identical at 교보 [S3], ABL [S6 §8-마], 삼성 [S5],
    한화 [S7 제35조] and 우체국 [S9 주10].

### Benefit provisions

The three shapes pay three different benefit sets out of one fund. The table below is the
representative set; the arithmetic that produces each annuity is in Contractual mechanics.

| Parameter | Representative value | Basis |
|---|---|---|
| Benefit taxonomy | **생존연금** (the periodic annuity), **사망보험금** (death benefit) and, on the inheritance shape only, **만기보험금** (maturity benefit) | [S1] [S3] [S7 별표1] [R1 별표1](#krlib-immediate_annuity-r1) |
| Payment grid | **Monthly, in arrears** — the market default: the first 연금월액 (*yeongeum wolaek*) falls due one month after the 보장개시일. The 연단위 alternative pays the 연금연액 from the first 계약해당일 | [S1 주1] [S3] [R2 §1](#krlib-immediate_annuity-r2); grid **[std]** (18) |
| 종신연금형 — 생존연금 | 연금개시시의 계약자적립액 ÷ an annuity factor computed from the annuitant mortality table and the 공시이율, payable while the annuitant lives and **guaranteed for the 보증지급기간 whether or not the annuitant lives** | [S7 별표1] [S1] |
| 종신연금형 — 보증지급기간 | **10 years** | [R12 표7](#krlib-immediate_annuity-r12); adoption **[std]** (19) |
| 종신연금형 — 사망보험금 | **None after annuitisation.** The unpaid guaranteed instalments continue on their original dates, or may be commuted | [S5] [S1 주5] [S3] |
| 상속연금형 만기형 — 생존연금 | Interest on the 계약자적립액 at Max[공시이율, 최저보증이율], **less the 만기보험금 지급재원** — the retention that rebuilds the fund to the maturity benefit | [R2 §1](#krlib-immediate_annuity-r2) [S7 별표1] [R1] |
| 상속연금형 만기형 — 보험기간 | **10 years** | [R12]; adoption **[std]** (20) |
| 상속연금형 만기형 — 만기보험금 | **The single premium**, ₩100,000,000, paid on survival to maturity | [S1] [S3] [S4] |
| 상속연금형 만기형 — 사망보험금 | **10% of the single premium plus the 계약자적립액 at death**, on death at any time | [S1] [S3] [R1 별표1(2)](#krlib-immediate_annuity-r1) |
| 확정기간연금형 — 생존연금 | 계약자적립액 ÷ an annuity-certain factor at the 공시이율 over the elected term, **payable irrespective of survival** | [S3] [S9 별표1] [R12 §III-1](#krlib-immediate_annuity-r12) |
| 확정기간연금형 — 연금지급기간 | **10 years** | [R12 표7](#krlib-immediate_annuity-r12); adoption **[std]** (20) |
| 확정기간연금형 — 사망보험금 | **10% of the single premium**, plus the remaining instalments on their dates or commuted | [S3] |
| Annuity level | **Not level.** The annuity is recomputed when the declared rate moves: 「생존연금의 계산은 공시이율을 적용하여 계산되므로 공시이율이 변경되면 생존연금도 변경됩니다」 | [S1 주3] [S4] [R1 별표1 주1](#krlib-immediate_annuity-r1) [S9 주13] |
| 공시이율 (*gongsi iyul*, declared crediting rate) | **2.50% a year**, reset on the first of each month and fixed for that month | [S1 §IV-4] [S12] [S14] [REG-R48]; adoption **[std]** (21) |
| 최저보증이율 (*choejeo bojeung iyul*, guaranteed floor) | **1.25%** to five years, **1.00%** over five to ten, **0.75%** thereafter | [S3]; adoption **[std]** (22) |
| Crediting rule | The 계약자적립액 is credited at **Max[공시이율, 최저보증이율]** | [R2 §1](#krlib-immediate_annuity-r2) [S7 제7조] |
| Annuitant mortality | 개인연금사망률 (*gaein yeongeum samangnyul*), used by **종신연금형 alone** | [S1 §IV-2] [R12 §III-1](#krlib-immediate_annuity-r12); table **[std]** (23) |
| Mortality ratchet | **Not applicable** on an immediate annuity | [S6 §10-라]; reasoning **[std]** (24) |
| Fund floor at annuitisation | **Not applied** | [S7 별표1 주8] [S9]; non-adoption **[std]** (25) |

18. The one document that publishes both modes states them side by side: 연단위 pays from
    the first 계약해당일, 월단위 from one month after the 보장개시일 [S1 주1]. Monthly is
    the market default and is often the only frequency offered on an 즉시연금 [S3];
    quarterly and half-yearly appear on the deferred contracts, with interest added on
    the deferred portions — 「연금을 매월, 3개월, 6개월로 분할하여 지급하는 경우
    신공시이율로 계산한 이자를 가산합니다」 [S9 주11], and identically [S8 주14].
    `Immediate_KR_S` is a **monthly-grid** model per the library's product table, so it
    projects the 연금월액 the market default actually pays and publishes the 연금연액 beside
    it. The earlier annual-grid model projected the 연금연액 and reconciled to the monthly
    mode through the interest addition above; that reconciliation is **exact only where no
    mortality enters the annuity** — the 확정기간연금형 — and on the 종신연금형 the monthly
    mode is genuinely worth 1.06% more, because it pays part-year instalments to a life that
    dies inside a policy year. The technical notes carry the arithmetic.
19. 97.3% of 종신형 buyers chose ten years and 2.7% chose twenty, a mean of 10.3 years
    [R12 표7](#krlib-immediate_annuity-r12). The US comparator in the same paper is a mean guarantee of 13 years. Ten
    years is also the tax-minimum shape: 소득세법 시행령 제25조제4항제3호 requires any
    guarantee period on a tax-exempt 종신형 to sit **within** the annuitant's statutory
    기대여명 [REG-R58], and a ten-year guarantee at age 60 clears that test on any
    published table [REG-R38].
20. 확정형 buyers chose ten years in 77.6% of cases, fifteen in 13.8% and twenty in 8.6%
    [R12 표7](#krlib-immediate_annuity-r12); no comparable distribution was published for the 상속형 term. Ten years is
    adopted on both term shapes because it is the modal 확정형 choice, because it is the
    term of the contract at the centre of 조정결정 제2017-17호 [R1 §1](#krlib-immediate_annuity-r1) and therefore the
    cell on which the dispute arithmetic is documented, and because it is the **shortest
    term that can meet the ten-year interest-income exemption** on the inheritance shape
    [REG-R58]. It is worth stating plainly that the modal 확정기간연금형 choice does
    **not** qualify: 시행령 제25조제3항제1호's carve-out excludes a contract whose premium
    is drawn down 「확정된 기간 동안 연금형태로 분할하여 지급받는 경우」 before the tenth
    anniversary, which is exactly what a ten-year annuity-certain does [REG-R58]
    [R12 §III-1 각주4](#krlib-immediate_annuity-r12). The inheritance shape escapes it because it pays only the
    interest and returns the principal at maturity.
21. Observed declared rates on annuity money, with their dates: 4.8% at 2011-09 [R27];
    4.5% at 2012-09 on the disputed contract [R1 §1-라](#krlib-immediate_annuity-r1); 3.40% falling to 2.80% over
    2015-03 to 2016-03 [S5]; 2.95% at 2016-03 [S4]; 2.83% at 2016-03 [S2]; 2.50% at
    2017-04 [S1 §IV-4]; 2.52% at 2017-12 [S3]; 2.80% at 2023-01 [S13]; 2.55% at 2025-01
    [S12]; 2.67% at 2026-04 [R28, a commercial content site](#krlib-immediate_annuity-r28); 2.56% at 2026-09 [S14]. The
    arc is a fall from about 4.8% in 2011 to about 2.6% in 2026. **2.50%** is adopted
    because it is the level the anchor carrier declared on this exact product [S1] and
    because it equals the **평균공시이율 for 2026** [REG-R48], which is the rate the
    illustration rules make a carrier show beside its own [S11] [S5]. It sits **5 to 17
    basis points below** the 2.55%–2.67% band of the three most recent observations, and
    that direction is recorded rather than smoothed: the adopted rate is at the
    supervisory average and a little under the market's latest declarations. No model
    in this library derives a Korean declared rate: 감독규정 제7-65조제3항 and 시행세칙
    별표 27 make it the product of a 공시기준이율 whose own weighting α is capped at 60%
    and is majority-weighted to the
    insurer's realised 운용자산이익률 [REG-R18] [REG-R24], and the two carriers who
    publish their weighting publish different ones [S6] [S12]. The rate is a slow-moving
    **[std]** scalar and is exposed as such.
22. Observed schedules, by vintage: 2.5% / 2.0% at ten years for the 2007–2014 cohorts
    [S10] and industry-wide in the 2008–2010 sample [R12 표2 주1](#krlib-immediate_annuity-r12); 2.5% / 2.0% / 1.0% at
    ABL in 2012 [S6 §9-마]; 2.5% / 1.5% on the disputed 2012 contract [R1]; 2.0% / 1.5% /
    1.0% at 동양 in 2016 [S4]; 1.5% / 1.0% at 삼성 [S5], 교보 [S2] and 하나 [S1 §V] in
    2016–2017; **1.25% / 1.00% / 0.75%** at 교보 in 2017-12 [S3]; 1.25% / 1.15% / 0.75%
    at 푸본현대 around 2020 [S8]; 1.25% / 1.00% / 0.50% at 하나 in 2023 [S13] and at IBK
    in 2026 [S14]; and 1.0% / 0.75% / 0.50% — reaching its terminal step after only
    **five** years — at 한화 in 2024 [S7 제7조]. The 교보 2017 schedule is adopted for one
    reason only: it is the only three-step schedule published on a contemporaneous
    즉시연금 illustration whose annuity figures this document also uses [S3]. **It is not
    a middle of the observed range and is not presented as one.** Against the five
    schedules retrieved for 2017–2026 it is the joint-highest opening step and the
    highest terminal step — 0.75% where 하나 (2023), 한화 (2024) and IBK (2026) all step
    down to 0.50% — so the adopted floor is at the generous end of the current market and
    well under the 2.5% / 2.0% the 2007–2014 cohorts carried [S10]. The direction is
    recorded rather than smoothed, and it bites on model point 8 alone: on the
    representative basis the declared rate is above every step and the floor is inert.
    That a floor exists at all is not optional:
    감독규정 제7-60조제10호 requires a 금리연동형보험 to set a 최저보증이율 or a
    최저보증금액 [REG-R16]. The 약관 explains it with a worked example — 「공시이율이
    0.25%인 경우, 공시이율(0.25%)이 아닌 최저보증이율 … 로 적립됩니다」 [S7 제7조]. Note
    what the floor is **not**: it is a rate on the fund, never a floor on the annuity.
23. [S1 §IV-2] is the only 즉시연금 document retrieved that prints annuitant rates, and
    it prints three ages: 개인연금사망률 at 50 / 60 / 70 of **0.00225 / 0.00353 /
    0.00728** for men and **0.00097 / 0.00118 / 0.00251** for women, stated on a
    가입나이 50 basis. Those six numbers are the only public anchors for a Korean
    annuitant table, because the **제10회 경험생명표** (*gyeongheom saengmyeongpyo*)
    applied from April 2024 is an industry table published only as summary statistics —
    평균수명 남 86.3세 / 여 90.7세 and 65세 기대여명 남 23.7년 / 여 27.1년 [REG-R33]
    [REG-R34]. Every `mort_table.csv` in `krlib` is therefore a **[std]** construction
    with a `provenance` column on every row, anchored on those six rates, on the public
    국가데이터처 완전생명표 [REG-R38] [REG-R39] and on the KIDI summary statistics; the
    construction is specified in `technical-notes.md` and the tables **must never be
    presented as the 경험생명표**. One property of the anchors is worth recording here
    because it constrains any construction: the male/female ratio runs 2.32 at 50, 2.99
    at 60 and 2.90 at 70, and the 하나생명 rate at 60 is roughly twice the deferred-
    annuity rates published in the sister research for `Pension_KR_S` — the two are not
    the same table, and the reason (a table loaded on the mortality side because the
    contract also carries a death benefit) is an inference and is **[unverified]**.
24. Every retrieved carrier carries a ratchet clause: 「종신연금형의 경우 연금지급 개시전
    연금사망률의 개정 등에 따라 연금액이 증가하게 되는 경우 연금개시 당시의 연금사망률 및
    계약자적립액을 기준으로 산출한 연금액을 지급합니다」 [S7 별표1 주9], and equivalently
    [S3] and [S8 주15]. One states its scope expressly — 「**거치형에 한하여**, 종신연금형의
    경우 연금개시전에 연금생명표의 개정 등에 따라 …」 [S6 §10-라]. On an immediate annuity
    there is no interval between issue and annuitisation for a table revision to land in,
    so the ratchet is inert and `Immediate_KR_S` needs no ratchet logic; the deferred
    sibling does. The one-way character of the clause — it operates only where the
    annuity would **increase** — is why the sister model needs it. A 2024 table revision
    is reported to have cut the annuity on a fixed fund by about 15% [R13, a news
    article](#krlib-immediate_annuity-r13), and in-force contracts are unaffected because the factor was fixed the
    month the premium was paid [R14, a news article](#krlib-immediate_annuity-r14).
25. Two independent carriers guarantee that the 계약자적립액 at annuitisation is at least
    **100.1%** of premiums paid: 「연금개시시의 계약자적립액은 이미 납입한 보험료 … 의
    100.1%를 최저보증 합니다」 [S7 별표1 주8], and identically [S9]. Both statements are
    made in **deferred** contracts, where there is an accumulation period in which to
    earn the guarantee. Applying it to an immediate annuity would be incoherent: the fund
    at annuitisation is the premium net of a 3.5% load, so a 100.1% floor would erase the
    whole acquisition and administration charge on day one. No retrieved 즉시연금
    document states such a floor. It is therefore recorded and **not** applied, and the
    inference that it is a deferred-contract mechanic — rather than a supervisory floor
    the immediate products silently breach — is **[unverified]**, the regulation behind
    it never having been retrieved [R31].

### Options

Every option is elected at inception, priced into the basis, and irrevocable thereafter.
There are no riders in the US sense; what a Korean 즉시연금 offers is a menu of payout
shapes and a small number of administrative facilities.

| Option | Representative rule | Basis |
|---|---|---|
| Payout shape | Elected at inception from 종신연금형 / 상속연금형 / 확정기간연금형; irrevocable | [S1] [S3] [S6] |
| Proportional split across shapes | **Not offered.** One deferred carrier allows the fund to be split across shapes in 5% units | [S8]; scope **[std]** (26) |
| 보증지급기간 menu (종신연금형) | **10년**, 20년, 100세, 기대여명 | [S7 별표1] [S3]; representative **10년** (19) |
| Meaning of the 100세 option | 「보증지급기간이 100세인 경우에는 [보증지급기간−연금개시나이+1]년을 보증지급」 — a 41-year guarantee at the anchor age of 60, not a hundred years | [S7 별표1 주6] [S9] |
| Meaning of the 기대여명 option | The 성별·연령별 기대여명 연수 of the 통계청 table **in force at inception**, decimals discarded, floored at five years | [S7 제2조제6호가목] [S5 주5] |
| Minimum guarantee period | **Five years.** A pure life annuity with no guarantee period may not be sold in Korea | [R12 §III-2-라](#krlib-immediate_annuity-r12) citing 보험업감독규정 제7-60조 4; **[unverified]** as to text [R31] (27) |
| 연금지급기간 menu (확정기간연금형) | 5년, **10년**, 15년, 20년, 30년 | [S6] [S9]; 10/15/20/30년 at [S3], out to 50년 at [S8] and to 60년/100세 at [S14] |
| 보험기간 menu (상속연금형) | 종신형, or 만기형 of **10년**, 15년, 20년, 30년 | [S1] [S3] [S5] |
| Front-loaded life annuity | **Not in the representative set** | [S2] [S3] [S5] [S8] [S9] [S13]; scope **[std]** (28) |
| 선지급 (*seonjigeup*, commutation) | The beneficiary may take the unpaid guaranteed or remaining certain instalments as a lump sum discounted at the **공시이율**, on death or on request, once a year and in whole years | [S3] [S5 주8] [S7 제11조제3항] [S9]; frequency limit from [S3] |
| Payment frequency | Monthly, quarterly or half-yearly, with interest at the 공시이율 on the deferred portions; monthly is the default on an 즉시연금 | [S8 주14] [S9 주11] [S1 주1] [S3] |
| 지정대리청구서비스특약 | Available; a nominated relative may claim where the insured cannot | [S8]; scope note (29) |
| 표준하체인수특약 (substandard acceptance) | Offered as a 제도성특약 | [S1 §III-1] |
| 부부계약 (joint life) | **Not in scope** | [S6] [S5]; scope **[std]** (30) |
| Indexation or escalation | **Not offered by any retrieved carrier.** The annuity moves only because the declared rate moves | [S1]–[S9] |

26. 푸본현대's deferred contract lets the fund be divided across payout forms in 5% units
    and adds a 노후설계자금 lump-sum election of up to 50% of the fund [S8]. Neither
    appears on any retrieved 즉시연금. A proportional split is implementable in the same
    engine as a weighted sum of three model points and is documented rather than
    defaulted; the lump-sum election is excluded outright because 소득세법 시행령
    제25조제4항제2호 requires a tax-exempt 종신형 to pay 「연금 외의 형태로 보험금ㆍ수익
    등을 지급하지 아니할 것」 [REG-R58].
27. The rule is quoted in the academic source — 「우리나라는 종신형이라 하더라도
    순수종신형은 허용되지 않으며 적어도 5년 이상 보증기간을 설정해야 한다(보험업감독규정
    제7-60조 4)」 [R12 §III-2-라](#krlib-immediate_annuity-r12) — and the regulation text itself could not be retrieved
    in the product research pass [R31]. The cross-product reference library did retrieve
    제7-60조 and records its ten operative items without a five-year annuity guarantee
    among them [REG-R16], so the citation is carried on the paper's authority and the
    **effect** is corroborated behaviourally: none of the eleven retrieved products
    offers a life-only option, and the shortest guarantee observed anywhere is ten years.
    Treat the article number as **[unverified]** and the five-year floor as a market
    regularity.
28. Every carrier offers a front-loaded life annuity under a different name — 집중보장형
    at 교보, which doubles the annuity for the guarantee period 「연금액의 100%를 추가로
    지급」 [S3]; 브릿지연금형 at 삼성, a multiple over a 브릿지횟수 between five years and
    the guarantee period [S5 주6]; 소득보장형 at ABL [S6]; 핵심기간집중형 at 푸본현대,
    fixed at 2× for ten years [S8]; 조기집중연금형 at 우체국, 200% or 300% over five or
    ten years [S9]; and 활동기집중형 at 하나, the most aggressive retrieved at **3× or
    5×** over five or ten years [S13]. The demand it serves is a bridge to the state
    pension — 「은퇴 후 국민연금 수령 전까지 가교연금이 필요할 경우」 [R12 §III-1](#krlib-immediate_annuity-r12). It is
    excluded from the representative set because it is a deterministic step function
    applied to an annuity the model already computes, and because no source publishes the
    factor adjustment that pays for the step. It is a documented variant, not a defaulted
    one, and the observed parameter space is 2×, 3×, 5× (or 200%/300%) over five years,
    ten years, or the whole guarantee period.
29. The 지정대리청구 rider exists because a 종신연금형 annuitant may lose capacity while
    the contract still has to pay. It is a claims-administration facility with no cash
    flow of its own and is listed for completeness.
30. ABL writes a 부부계약 (joint-life) form and raises the minimum annuity age to 48 where
    the principal insured is male [S6]; 삼성 contemplates a 부부형 in passing [S5]. No
    retrieved document gives the joint-life mechanics or a factor, so anything beyond
    "one carrier offers it and raises the minimum age by three years for a male principal
    insured" is **[unverified]**. Single-life only.

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| Surrender — 종신연금형 | **Not permitted at any time after the annuity has begun.** On an immediate annuity that means from month one: the contract is irreversible | [S3] [S5 주2] [S7 제31조] [S8 제33조] [REG-R58 영 제25조제4항제4호](#krlib-reg-r58) |
| Surrender — 상속연금형, 확정기간연금형 | **Permitted at any time** before the contract is extinguished | [S1] [S3] [S6] |
| 해약환급금 (*haeyak hwanreupgeum*, surrender value) | 계약자적립액 less the 해약공제액, floored at zero | [REG-R19 제7-66조제1항제1호](#krlib-reg-r19) [S1 §VI-1] |
| 해약공제액 (*haeyak gongjeaek*, surrender charge) | **Nil at every duration** | [S1 §VIII] [S10]; observed, not standardized (31) |
| Statutory cap on the surrender charge | 표준해약공제액 = 6% of the 연납순보험료 for a whole-life 생존연금보험, with a 해약공제계수 of **1** for a single premium, subject to the 5% × 12 ceiling | [REG-R20 별표 14 주2, 주4](#krlib-reg-r20) [REG-R19 제7-66조제1항제3호](#krlib-reg-r19) (32) |
| Effect of a surrender on the annuity | The contract is extinguished; there is no paid-up or reduced-annuity form | [S1] [S3] |
| 미경과보험료 | Not applicable — there is no unearned premium on a single-premium contract already fully credited | [REG-R19 제7-66조제5항](#krlib-reg-r19); reasoning **[std]** (33) |
| 위법계약의 해지 (*wibeop gyeyagui haeji*) | Returns the **계약자적립액**, not the surrender value | [S7 제34조제5항] [REG-R25 제32조](#krlib-reg-r25) |
| 청약철회 (*cheongyak cheolhoe*, cooling-off) | 15 days from receipt of the 보험증권 and never more than 30 days from the application date; premium returned within 3 business days | [REG-R51 제46조제1항제1호](#krlib-reg-r51) [REG-R25 제17조](#krlib-reg-r25) |
| 품질보증해지 (*pumjil bojeung haeji*) | Cancellation within **three months** of formation where the 약관 was not delivered, the important content not explained, or the application not signed | [REG-R25 제18조제3항](#krlib-reg-r25) [REG-R49 제638조의3](#krlib-reg-r49) |
| 실효 (*silhyo*, lapse) and 부활 (*buhwal*, reinstatement) | **Cannot arise.** There is no renewal premium to miss | [REG-R25 제26조, 제27조](#krlib-reg-r25); reasoning **[std]** (34) |
| Lapse decrement in the model | **Zero on 종신연금형** (surrender is contractually impossible); a **[std]** scalar on the other two shapes | [S3] [S7 제31조]; level **[std]** (35) |
| Expiry — 종신연금형 | On the later of the annuitant's death and the end of the 보증지급기간 | [S7 별표1] [S1 주5] |
| Expiry — 상속연금형 만기형 | On payment of the 만기보험금 at the end of the 보험기간, or earlier on death | [S1] [S3] |
| Expiry — 확정기간연금형 | At the end of the 연금지급기간, death not accelerating it | [S3] [S9 주7] |
| 소멸시효 (prescription) | Three years on a claim, three on a refund of premium or account balance, two on a premium | [REG-R49 제662조](#krlib-reg-r49) [S7] |
| 예금자보호 (*yegeumja boho*) | ₩100,000,000 (1억원) per person per insurer, from 2025-09-01 | [REG-R52 제18조제7항](#krlib-reg-r52) [REG-R32]; see (36) |

31. This is one of the few parameters in the library that needs no standardization,
    because it is published as a complete run and it is a run of zeros: 「경과시점 1년 …
    7년이상 / 해지공제금액(만원) 0 … 0 / 해지공제비율 0.0% … 0.0%」 [S1 §VIII]. The same
    carrier's rate disclosure independently confirms that its three 즉시연금 products
    carry no 중도해지율 at all, unlike its savings contracts [S10]. The reason is
    structural rather than generous: a single-premium annuity has no unamortised
    acquisition cost to recover, because the cost was taken in full at inception. The
    published surrender-value run makes the point from the other side — on a 정기상속
    연금형 (20년지급), 가입나이 60, 일시납 ₩50,000,000, male, on the guaranteed-rate
    basis, the 환급률 runs 96.6% at three months, 96.7% at one year, 97.1% at three,
    97.6% at five, 98.0% at seven, 98.6% at ten, 99.5% at fifteen and **exactly 100.0% at
    twenty** [S1 §VI-2]. The curve rises to par because it is a 만기형: the retention is
    visible from the surrender side.
32. 별표 14's formula is 표준해약공제액 = 연납순보험료의 5% × 해약공제계수 +
    보장성보험의 보험가입금액의 10/1000, with note 4 substituting **6%** for a
    보험기간이 종신인 생존연금보험 that is not a 연금저축보험 — which is what the life
    shape of this product is — subject to a ceiling computed at 5% with a coefficient of
    12, and note 2 fixing the coefficient at **1** for a single premium
    [REG-R20]. The cap is therefore of the order of a few per cent of the net single
    premium rather than the double-digit multiple a twelve-year-pay savings contract can
    reach. What the exact 연납순보험료 is for a single premium was not tested against a
    filed 산출방법서 and the resulting won amount is **[unverified]**; the point that
    matters is that the cap **binds nothing here**, because every retrieved carrier
    deducts zero.
33. 감독규정 제7-66조제5항 requires the insurer to add 미경과보험료 to the surrender value
    on termination [REG-R19]. On a single-premium contract whose whole load was taken and
    whose whole residue was credited at inception there is no unearned premium in the
    ordinary sense, and no retrieved 즉시연금 document mentions one. The reasoning is the
    composite's, not a carrier's, and it is **[std]**.
34. 표준약관 제26조's 납입최고 and 제27조's 부활 both presuppose a renewal premium that can
    go unpaid [REG-R25]. A single-premium contract has none, so neither article can
    operate and neither is modelled. This is a real structural difference from every
    other product in `krlib`, all of which carry a lapse decrement driven by premium
    payment, and it is why this product's only decrements are mortality and — on two of
    the three shapes — voluntary surrender.
35. **No retrieved source gives a surrender rate for 즉시연금 by duration or by shape.**
    On the life shape the question does not arise, because surrender is contractually
    impossible from month one. On the other two shapes the assumption is entirely
    unsourced and must be **[std]**; the reference implementation carries it as a
    per-model-point scalar so that its effect can be isolated, and `technical-notes.md`
    states the level and the sensitivity. Note the interaction that makes a nil
    assumption defensible on the inheritance shape: the 만기보험금 equals the gross
    premium and the surrender value is below it at every duration before maturity
    [S1 §VI-2], so surrendering early is a realised loss on a contract bought to be held.
36. Every retrieved leaflet from 2016–2017 recites the then-current ₩50,000,000 limit
    [S1 §I] [S2] [S3] [S4] [S5]. The limit is now **₩100,000,000**, in force from
    2025-09-01 [REG-R52 제18조제7항](#krlib-reg-r52) [REG-R32]. The point bites harder on this product
    than anywhere else in `krlib`: the **median** premium is ₩100,000,000 and 38.5% of
    contracts exceed it [R12], so the great majority of the money in this line sits
    **outside** the protection limit on either the old figure or the new one. Note also
    that 예금자보호법 시행령 제18조제7항 excludes benefits payable because the policy term
    has ended from the insurance bucket, which puts a 상속연금형's 만기보험금 into the
    residual bucket with the depositor's other claims [REG-R52].

---

## Contractual mechanics

### The premium split, the opening fund, and the accumulation identity

The single premium A is divided at inception and never again. The determination's own
table sets the division out in the clearest form anywhere in the corpus [R1 §1-가 각주2](#krlib-immediate_annuity-r1):

| 구분 | Premium component | Benefit it funds |
|---|---|---|
| 보장계약 | 사망보험금 산출에 필요한 보험료 (B) | 사망보험금 — 납입보험료의 10% |
| 연금계약 | 사업비 (C); 만기보험금 및 생존연금 재원 (D = A − B − C) | 만기보험금 — 납입 보험료 총액; 생존연금 |

The residue D is the opening **계약자적립액**. The 상품요약서 states the same identity
prospectively: 「「연금계약 적립액」은 연금계약 순보험료(기본보험료에서 보장계약 순보험료,
계약체결비용 및 계약관리비용을 뺀 금액)를 기준으로 공시이율을 적용하여 계산한 금액으로
보험료 및 책임준비금 산출방법서에서 정한 바에 따라 계산됩니다」 [S1 주2]. On the
representative basis:

- 종신연금형: V(0) = P × (1 − 0.0350) = 0.9650 P — no risk premium, because the shape
  pays no death benefit once the annuity has begun [S1 §VIII] [S5];
- 상속연금형 만기형 and 확정기간연금형: V(0) = P × (1 − 0.0350 − 0.0147) = 0.9503 P.

Thereafter the fund runs a single recursion, stated in the 약관 for both phases —
「연금개시 전에는 연금계약순보험료를 … 공시이율로 납입일부터 일자계산에 의하여 적립한
금액이며, 연금개시후에는 생존연금 발생분을 차감한 금액」 [R1, quoting the 약관 서두](#krlib-immediate_annuity-r1). On
the monthly grid, with the annuity payable in arrears:

```
V(t+1) = V(t) × (1 + j(t)) − A(t),
j(t)   = ( 1 + Max[공시이율, 최저보증이율(t)] )^(1/12) − 1
```

A(t) is `technical-notes.md`'s own index convention: the 연금월액 struck in month t and
falling **at the end of that month**, in arrears on the 연금지급일. Everything that
distinguishes the three shapes is the definition of A(t) out of V(t), and everything the
model does after t = 0 is that recursion plus a decrement. There is no
premium income after t = 0, no acquisition strain to amortise, and — because the whole
load was taken at inception and the surrender deduction is nil — no unamortised
acquisition cost bounded by 별표 14 [REG-R20]. That is what makes this the library's
payout-phase chassis: the accumulation half of the machinery is `Pension_KR_S`'s.

### The crediting rate — 공시이율, 공시기준이율 and 최저보증이율

The rate applied to the fund is the higher of the declared rate and the guaranteed floor:
「보험료*에 일정한 이율**을 곱하여 산출한 금액 … \*\* Max [공시이율, 최저보증이율]」
[R2 §1](#krlib-immediate_annuity-r2). Three properties matter to a model.

**It is reset monthly and fixed within the month.** 「이 계약의 공시이율은 매월 1일 회사가
정한 이율로 하며, 당월 말일까지 1개월간 확정 적용한다」 [S6 §9-나], identically at
[S1 주6], [S3], [S5] and [S7 제7조]. `Immediate_KR_S` carries one **annual** declared rate a
policy year and credits its monthly equivalent, so the grid is finer than the rate is: a rate
that in reality steps twelve times a policy year is projected as one level figure.
`technical-notes.md` records the approximation, which is exact wherever the declared rate is
level — as on the representative basis it is.

**It is regulated in construction but not in level.** 감독규정 제7-65조제3항 makes the
공시이율 the product of a **공시기준이율** and a 조정률, and requires the 공시기준이율 to
be a weighted average of an objective external index rate and the insurer's own
운용자산이익률, computed as the FSS Governor prescribes and written into the 기초서류
[REG-R18]. 시행세칙 별표 27 gives the construction [REG-R24]:

```
공시기준이율 = 객관적 외부지표금리 × α + 운용자산이익률 × (1 − α)
객관적 외부지표금리 = 국고채(5년) × β1 + 회사채(무보증 3년, AA−) × β2
                     + 통화안정증권(1년) × β3 + 양도성예금증서(91일) × β4
```

with the four yields taken as a three-month weighted moving average, the βs set from the
insurer's own prior-year bond and CD balances and rounded to half a point, and **α capped
at 60%** [REG-R24]. A Korean declared rate is therefore majority-weighted to the
insurer's own realised investment return, which is why it moves sluggishly against
government bond yields.

The two carriers that publish their own weighting publish different ones, and the
disputed contract used a third. ABL's filed 사업방법서 gives 「공시기준이율 산출식 =
(내부지표 + 외부지표) ÷ 2」 with the external indicator a 국고채 / 회사채 blend weighted
by the share of government bonds in the insurer's own book, rounded to five points, and
— decisively — 「공시이율은 산출공시기준이율의 **80% ~ 120%** 범위내에서 정한다」
[S6 §9]. NH농협생명 publishes 「공시기준이율 = 외부지표금리 × 40% + 운용자산이익률 ×
60%」 with 「적용이율 = 공시기준이율 × 조정율」, and at 2025-01 a 공시기준이율 of 2.86%
with a 조정율 of 89.16% giving an annuity 적용이율 of **2.55%** [S12]. The disputed 2012
약관 used 「공시기준이율 = 운용자산이익률 × 0.65 + 외부지표금리 × 0.35」 with the same
80%–120% corridor [R1, quoting 약관 제16조](#krlib-immediate_annuity-r1). The internal/external split therefore ranges
over 50/50, 60/40 and 65/35 on the retrieved evidence. **Any model that treats the
공시이율 as an exogenous scalar is defensible; any model that claims to derive it is
not**, and `Immediate_KR_S` exposes it as a scalar.

**The floor is a rate on the fund, never a floor on the annuity.** That single sentence
is the substance of the whole dispute. A policyholder reading 「10년 이내 연복리 2.5% 최저
보증」 in the 약관 [R1 별표1 주7](#krlib-immediate_annuity-r1) naturally reads it as a floor under the income; it is
not, and on a 만기형 the income can fall far below it while the floor is honoured on the
fund. The representative schedule steps 1.25% / 1.00% / 0.75% at five and ten years [S3];
the 약관 illustrates the mechanic with its own worked example [S7 제7조]. That a floor
must exist is regulatory: 감독규정 제7-60조제10호 requires a 금리연동형보험 to set a
최저보증이율 or a 최저보증금액 [REG-R16].

Alongside the declared rate sits the **평균공시이율** (*pyeonggyun gongsi iyul*), the
average of all insurers' declared rates computed as the FSS Governor prescribes
[REG-R9 제1-2조제13호](#krlib-reg-r9), published to the market through carriers' regulatory disclosure
[REG-R48] and defined in the 상품요약서 as 「감독원장이 정하는 바에 따라 산정한 전체
보험회사 공시이율의 평균으로 … 보험계약의 체결시점의 평균공시이율을 보험기간 동안
적용합니다」 [S11]. It is 2.50% for 2026, having been 2.75% in 2024–2025 and 2.25% in
2021–2023 [REG-R48] [S11]. It matters to this product in two ways. It is the rate the
disclosure rules make a carrier show beside its own — the illustrations show three
columns, the declared rate, **Min[평균공시이율, 공시이율]** and the floor [S5] — and in
every retrieved illustration from 2016 onward the declared rate is *below* the average,
so the middle column duplicates the first and carries no information [S2] [S3] [S4] [S5].
And it is the rate at which 감독규정 제7-60조제3호's accumulation test is run [REG-R16].

### 종신연금형 — the annuity factor, the guarantee, and what "in force" means

The life shape converts the fund once, at inception. The 약관 wording is
「연금개시시의 계약자적립액을 기준으로 피보험자가 생존한 기간 동안(연금개시시점부터
계약자가 선택한 보증지급기간(10년, 20년, 100세, 기대여명)동안 보증) 산출방법서에서 정한
방법에 따라 연금액을 분할 계산하여 매년 보험계약해당일에 지급」 [S7 별표1]. Formally,
with V(0) the opening fund, the annuity is

```
A = V(0) / ä(x, g, i)
```

where ä is the actuarial present value of ₩1 a year payable while the annuitant aged x
lives or the guarantee of g years runs, whichever is longer, discounted at i and using
the 개인연금사망률. **No carrier publishes a factor**, and no filed 산출방법서 for an
즉시연금 was retrieved [R31], so every annuity factor in this library is computed by the
model from a **[std]** table and stated in `technical-notes.md`. What can be published is
the factor **implied** by carriers' own illustrations, computed as the single premium
divided by the annual annuity — the whole of the following table is **[std]** arithmetic
on published figures and no carrier states any of it:

| Source | Basis | Monthly annuity | Gross factor (P ÷ annual annuity) | Net of load |
|---|---|---|---|---|
| [S3] | 남자 55세, ₩100,000,000, 10년 보증, 공시이율 2.52% | 35만원 | 23.81 | 22.98 |
| [S3] | 남자 55세, 20년 보증, same basis | 34만원 | 24.51 | 23.65 |
| [S3] | 남자 55세, 100세 보증, same basis | 29만원 | 28.74 | 27.73 |
| [S4] | 남자 55세, ₩100,000,000, 10년 보증, 공시이율 2.95% | 36만원 | 23.15 | 22.34 |
| [S5] | 여자 40세, ₩100,000,000, 120회 보증, 공시이율 2.80% | 27만원 | 30.86 | 29.78 |

The "net of load" column divides by 0.9650 P, the fund the representative expense basis
leaves. Two readings. The 동양 factor at 55 sits 2.8% below the 교보 factor on the same
age and shape, which is what a declared rate 0.43 points higher produces. And a female
annuitant fifteen years younger carries a factor about 30% higher, which is the joint
effect of age and sex on a longevity basis — the only quantification of the sex effect
the corpus permits, since the 개인연금사망률 anchors give male rates 2.3 to 3.0 times the
female rates at 50, 60 and 70 [S1 §IV-2].

**The guarantee period is not a rider; it is the reason the projection's in-force measure
is not a survival probability.** Within the 보증지급기간 the instalments are due whether
or not the annuitant lives: 「종신연금형의 경우 연금지급 개시 후 보증지급기간안에
사망시에는 잔여보증지급기간 동안, 미지급된 연금월액을 매월 연금지급일에 드립니다」 [S3],
and identically [S1 주5]. What a model must carry through time is therefore the
probability that a **payment obligation remains** — on the life shape, the greater of the
survival probability and the indicator that the guarantee is still running; on the
annuity-certain shape, one until the term ends; on the inheritance term shape, one until
maturity or death, since death itself triggers a payment. Naming that quantity `pols_if`
follows lifelib's vocabulary and not its ordinary meaning, and the model says so in the
cells' own docstring.

Three further properties of the shape follow from the tax statute rather than from
underwriting, and are dealt with under Regulatory context: the guarantee period may not
exceed the annuitant's statutory 기대여명 if the exemption is to be kept; the contract may
not be surrendered once in payment; and no benefit may be paid in a form other than an
annuity [REG-R58 영 제25조제4항](#krlib-reg-r58). A pure life annuity with no guarantee at all may not be
sold [R12 §III-2-라](#krlib-immediate_annuity-r12), **[unverified]** as to the article text [R31].

### 상속연금형 — interest only, and the 만기보험금 지급재원

The inheritance shape pays the interest and keeps the capital. In the 종신형 sub-shape:
「연금지급 개시시점의 연금계약 책임준비금을 기준으로 공시이율로 계산한 이자를 생존연금
으로 지급하고, 사망시에는 해당 시점의 연금계약 책임준비금에 기본보험료의 10%를 더하여
일시금으로 지급하며, 만기형의 경우 만기생존시에 만기환급금을 지급하는 형태」 [S3]. It
uses no mortality in the annuity calculation at all — 「옵션 중 사망(생존) 위험률이
적용되는 것은 종신형에 한정된다 … 확정형과 상속형은 사망률을 사용하지 않는다」
[R12 §III-1](#krlib-immediate_annuity-r12) — which is the single most important modelling consequence in the product:
two of the three shapes are pure interest arithmetic and only 종신연금형 reads
`mort_table.csv` for its annuity.

For the **만기형** the maturity benefit is the gross single premium — 「만기보험금 :
납입 보험료 총액」 [R1 §1-가 각주2](#krlib-immediate_annuity-r1), and 「연금계약 적립액(기본보험료 해당액)」 [S1] —
while the fund starts at the premium *net* of the load. That mismatch is the whole of the
mechanic. Writing M for the maturity benefit, n for the term and s(n) = ((1+i)^n − 1)/i
for the accumulation factor of ₩1 a year in arrears, the level annuity that takes the
fund from V(0) to M over n years is

```
A = [ V(0)(1 + i)^n − M ] / s(n)
```

which, because (1 + i)^n = 1 + i·s(n), decomposes exactly into

```
A = V(0) · i        −        (M − V(0)) / s(n)
    ─────────                ─────────────────
    interest on the fund     만기보험금 지급재원 (the retention)
```

and the fund follows V(t) = V(0) + R·s(t) with R the retention, reaching M precisely at
t = n. **Both terms move against the policyholder when the rate falls**: the interest
falls with i, and the retention *rises*, because s(n) shrinks. That is why an annuity on
this shape can fall by more than half while the guaranteed floor never moves, and it is
the arithmetic the next section is about.

The supervisor's own restatement is the cleanest specification of the liability anywhere
[R2 §1](#krlib-immediate_annuity-r2):

> 만기환급형 즉시연금은 보험계약자가 낸 보험료\*에 일정한 이율\*\*을 곱하여 산출한 금액
> 중에서 … 만기보험금 지급을 위한 재원(이하 '만기보험금지급재원')을 공제한 금액을 매월
> 연금으로 지급하는 구조
> \* 보험설계사에게 지급되는 수당 및 위험 보장을 위한 보험료 등을 제외한 순보험료
> \*\* Max [공시이율, 최저보증이율]

The 종신형 sub-shape has no maturity benefit to fund, so R = 0 and the annuity is simply
V(0) · i, with the fund returned on death. On the representative basis at a 공시이율 of
2.52% the two are, per ₩100,000,000 of premium and expressed monthly: **₩197,000** for
the 종신형 against a published 19만원 [S3], and **₩161,000** for the 10-year 만기형
against a published 17만원 [S3]. Both are **[std]** arithmetic; the first is 3.8% above
the published figure and the second 5.4% below it, and the residual on both is the
combination of the risk premium's true level and the 0.80% annuity-period charge, neither
of which [S3] discloses. On the expense load alone, with no risk premium, the 만기형
figure is ₩175,000, 2.7% above the published one — so the published annuity is bracketed
by the two treatments, which is the most that can honestly be said.

### The 즉시연금 과소지급 분쟁 — the retention, the determination, and the switch

**What went wrong.** The retention above was set out in the 산출방법서 and not in the
약관. The 약관 said only this [R1 §1-나, 별표1](#krlib-immediate_annuity-r1):

> 상속연금형 — 피보험자가 보험기간(10년, 15년, 20년, 30년)중 매년 계약 해당 일에
> 살아있을 때 — 보장개시일로부터 만1개월 이후 계약해당일부터 연금지급개시시의 연금계약의
> 적립액을 기준으로 계산한 연금월액을 매월 계약해당일에 지급

with note 1 that the annuity moves with the declared rate, note 6 that
「연금계약적립액은 이 보험의 산출방법서에서 정한 바에 따라 계산한 금액으로 합니다」 and
note 7 stating the floor. **Nowhere does that 약관 mention the retention.** The
supervisor's later reconstruction records that the same sentence had been reused from a
product with no maturity benefit — 「만기보험금을 지급하지 않는 즉시연금 약관(순수종신
연금형의 기본형, 부부형)과 동일하게 사용」 [R2 §4](#krlib-immediate_annuity-r2). The defect was drafting reuse, not
design.

**The case.** On 2012-09-12 a policyholder wrote a ₩1,000,000,000 (10억원) 즉시상속형 for
a ten-year term, monthly, with himself as policyholder, insured and beneficiary
[R1 §1](#krlib-immediate_annuity-r1). The declared rate at inception was 4.5%, the floor 2.5% within ten years and
1.5% beyond, the death benefit 10% of premiums and the 사업비 **5.325%** of the premium
[R1]. The annuity actually paid ran [R1 §1-가](#krlib-immediate_annuity-r1):

| Period | Monthly 생존연금 |
|---|---|
| 2012-10 ~ 2013-09 | 약 305만원 |
| 2013-10 ~ 2014-09 | 약 259만원 |
| 2014-10 ~ 2015-09 | 약 250만원 |
| 2015-10 ~ 2016-09 | 약 184만원 |
| 2016-10 ~ 2017-09 | 약 138만원 |
| 2017-10 | 약 136만원 |

a fall of **55.4% in five years** while the guaranteed floor never moved. The insurer's
own description of why is the clearest statement of the mechanism in the corpus
[R1 §2](#krlib-immediate_annuity-r1):

> 동 상품은 계약체결 당시 일시납 보험료에서 공제(보장계약보험료와 예정사업비)한 연금계약
> 순보험료 … 를 공시이율 … 로 적용하여 산출한 운용수익으로 만기보험금(일시납보험료
> 상당액) 지급을 위해 일정액을 충당하고 잔여액은 생존연금으로 지급된다. … 공시이율이
> 하락할 경우에는 만기보험금 지급을 위해 유보하여야 할 금액이 커지게 되므로 생존연금이
> 줄어들 수 있다.

**The arithmetic reproduces the published annuity**, which is worth stating because it
shows the model in this specification is the model that was litigated. All of the
following is **[std]** reconstruction from the figures at [R1] and [R2], monthly in
arrears at the monthly rate (1 + i)^(1/12) − 1 throughout. Solving the identity above at
a declared rate of 4.5% over ten years on a ₩1,000,000,000 premium gives a first-year
monthly annuity of ₩3,125,000 on a load of 5.325% (the 사업비 alone), ₩3,056,000 on the
supervisor's round 6.0% assumption [R2 참고](#krlib-immediate_annuity-r2), and **₩3,050,000 — the published figure —
on a total load of 6.054%**, which is solved for rather than observed. The reconstruction
therefore recovers a 보장계약 보험료 of about **0.73%** of premium for a death benefit of
10% of premiums over ten years, a figure the determination does not state, and vindicates
the supervisor's 6% assumption to two significant figures. At the guaranteed floor of
2.5% the same identity on that 6.054% load gives **₩1,490,000** a month as designed,
against **₩1,935,000** on the determination's own order — interest on the net fund with
no retention, a **29.9% uplift**. The applicant himself claimed ₩2,083,333, which is
2.5% ÷ 12 of the **gross** premium — simple monthly interest on the whole ₩1,000,000,000
— and is the one figure of the three the determination records rather than this document
computing it [R1 §2](#krlib-immediate_annuity-r1); on the compounding convention used above the same claim would be
₩2,060,000.

**The determination.** 조정결정 제2017-17호, 2017-11-14, reasoned in three moves
[R1 §3](#krlib-immediate_annuity-r1). First, objective construction: 「약관의 내용은 개개 계약체결자의 의사나 구체적
사정을 고려함이 없이 평균적 고객의 이해가능성을 기준으로 하여 객관적·획일적으로 해석하여야
한다」, on which basis the 약관 makes clear that the annuity may fall but not that it may
fall below what the stated floor implies. Second, the status of the 산출방법서:
「약관이 보험계약자를 향하고 있는데 비하여 산출방법서는 보험회사 내부의 계리적 서류에
지나지 않는 것으로 … 원칙적으로 보험계약자를 구속하는 등 사법(私法)관계인 보험계약관계에
적용될 수는 없다」 — incorporable only where a pointer clause specifies the content, the
content concerns rights and duties, and the duty of explanation has been discharged. Note
6 incorporated only the calculation of the **계약자적립액**, not the annuity formula.
Third, the duty of explanation under 상법 제638조의3 [REG-R49] and 약관규제법 제3조제4항.
The 주문 ordered payment of interest on the fund at Max[공시이율, 최저보증이율] with no
retention, on a fund net of the death-benefit premium and expenses — so neither party won
outright.

**What happened next**, in one table [R1] [R2] [R3] [R6] [R17] [R18] [R19] [R21] [R22]
[R24]; every aggregate figure in it is from news reporting and no supervisory document
states any of them:

| Date | Event |
|---|---|
| 2012-08-08 | Government announces removal of the ten-year exemption for 즉시연금 from the following year [R5] |
| 2012-09-26 | FSS issues a 소비자경보 against 절판마케팅 of 즉시연금 [R5] |
| 2017-11-14 | 금융분쟁조정위원회 조정결정 제2017-17호 [R1] |
| 2018-01 | The insurer amends the 약관 so that 약관 and 산출방법서 agree [R2 §4](#krlib-immediate_annuity-r2) |
| 2018-02 | The insurer accepts the determination; acceptance has the force of a 재판상의 화해 [R2 §3](#krlib-immediate_annuity-r2) |
| 2018-03-15 | FSS notifies **every life insurer** to handle its own cases the same way [R2 §4](#krlib-immediate_annuity-r2) |
| 2018-06 | A second 분조위 determination to the same effect [R3 §1](#krlib-immediate_annuity-r3) |
| 2018-08 | One carrier's board declines blanket payment; another refuses the determination [R17] |
| 2018-09-04 | FSS advises policyholders to file a dispute application to interrupt the three-year limitation [R3] |
| 2021–2022 | Four class actions won by consumers at first instance; all appealed [R18] [R19] |
| 2022-11 | 서울고등법원 reverses, holding the 산출방법서 part of the 약관 — quoted from a search snippet only, **[unverified]** |
| 2025-10-16 | 대법원 2022다225897 (파기환송) and 2022다308747·308754 (상고기각) [R6] [R21] |
| 2025-10 | FSS announces a consumer-protection inspection into 즉시연금 selling [R24] [R25] |

The Supreme Court held that a pointer clause 「그 문서에 따라 계산한다」 to an undelivered
document containing only formulae does **not** discharge the duty of explanation; that
the contract nonetheless survives with the offending term severed and is then construed
objectively by the understanding of an average customer; and that severance does not
change the annuity payable [R6] [R21] [R23]. The number of plaintiffs is reported as 57
in one trade title and 51 in two others of the same judgment day; the discrepancy is
unresolved and both are recorded [R21] [R22] [R25].

**The 약관 amendment**, printed side by side by the supervisor [R2 §4](#krlib-immediate_annuity-r2):

| 개정 전 | 개정 후 |
|---|---|
| 연금계약의 적립액을 기준으로 계산한 연금월액 | 연금계약의 **연금재원**을 기준으로 **만기보험금 지급을 위한 재원을 제외하여** 계산한 연금월액 |

and the same repair, six years later, in a live 약관: 「「연금개시시의 계약자적립액을
기준으로 공시이율에 의해 계산한 이자 상당액」에서 **소정의 사업비를 차감하여** 매년
보험계약 해당일에 지급」 [S7 별표1]. **The current market states the deduction on the
face of the contract, and that is the disclosure state a 2026 reference product models.**

**What the model must therefore carry.** The retention is implemented as an explicit,
switchable term with two settings — *as designed*, A = V(0)·i − (M − V(0))/s(n), and *as
ordered*, A = V(0)·i with the maturity benefit funded from the insurer's own resources —
so that both liabilities can be projected from the same model point and the difference
read off. That is not a modelling nicety. The entire legal history of the product is
about whether that one term is part of the contract, and a specification that buries it
inside an annuity factor cannot express the question.

### 확정기간연금형 — the annuity-certain, and the load cross-check

The certain shape divides the fund over an elected term: 「연금지급개시시점의 적립금액을
기준으로 계약자가 선택한 연금지급기간동안 나누어 계산한 금액을 연금지급기간동안 매년
지급」 [S9 별표1]. Payment does not depend on survival — 「확정형에서는 가입자가 선택한
지급기간 동안 가입자의 생존여부에 관계없이 연금급여를 지급한다」 [R12 §III-1](#krlib-immediate_annuity-r12) — and death
inside the term leaves the remaining instalments payable on their dates or commutable
[S9 주7]. With a(n) = (1 − (1 + i)^−n) / i,

```
A = V(0) / a(n)
```

and that is the whole of it. Because the shape carries no mortality, it is the sharpest
available test of the expense load, and the test is the reason this document adopts the
load it does. Solving the identity monthly in arrears against 교보's four published
확정기간연금형 figures — 남자 55세, ₩100,000,000, 공시이율 2.52% at 2017-12 [S3] — on the
representative first-day deduction of 4.97% gives, all **[std]**:

| Term | Published [S3], 만원/월 | Representative basis, computed | Difference |
|---|---|---|---|
| 10년 | 90 | 89.5 | −0.5% |
| 15년 | 64 | 63.3 | −1.1% |
| 20년 | 50 | 50.3 | +0.6% |
| 30년 | 37 | 37.5 | +1.4% |

Four terms, one basis, a maximum error of 1.4%, on a carrier and a document entirely
independent of the 하나생명 expense disclosure the load was taken from [S1]. The certain
shape is also **the one shape on which the choice of grid changes nothing at all**: it
carries no mortality in its annuity, so the monthly instalment the model now solves for
directly is exactly the annual-step model's 연금연액 converted through the within-year
interest, to the won. The advance convention would move the figures above by about 0.2
points, which is the only timing question left open on this shape.

One consequence of the shape has nothing to do with cash flow and belongs in the
specification anyway: the **modal 확정기간연금형 term does not qualify for the interest-
income exemption**. 소득세법 시행령 제25조제3항제1호 excludes a contract whose premiums are
drawn down 「확정된 기간 동안 연금형태로 분할하여 지급받는 경우」 before the tenth
anniversary [REG-R58], which a ten-year annuity-certain does by construction
[R12 §III-1 각주4](#krlib-immediate_annuity-r12); and the shape is not a 종신형, so the 제25조제4항 route is closed too.
The buyer of the most popular certain term is buying a taxable product.

### 사망보험금, and the exclusions that qualify it

The death benefit is small by design and shape-dependent. The near-universal Korean
design on an 즉시연금 is **10% of the single premium plus the fund at death**: it appears
at 교보 [S2] [S3], 하나 [S1] and in the disputed contract 「이미 납입한 보험료의 10% +
사망 당시 연금계약적립액」 [R1 별표1(2)](#krlib-immediate_annuity-r1). It is small enough not to disturb the annuity —
the risk premium that buys it is 1.47% of the single premium on a twenty-year inheritance
shape [S1 §VIII] — and large enough to make the contract a contract of insurance.

The shapes differ in what survives annuitisation:

| Shape | Before annuitisation | After annuitisation | Source |
|---|---|---|---|
| 종신연금형 (교보) | 사망당시의 연금계약 책임준비금 + 1,000만원 | unpaid guaranteed instalments only | [S3] |
| 종신연금형 (삼성, 순수종신) | — | 「별도의 사망보험금은 지급되지 않습니다」 | [S5] |
| 상속연금형 (교보) | 책임준비금 + 1,000만원 | 책임준비금 + 1,000만원 | [S3] |
| 상속연금형 (하나) | — | 기본보험료의 10% plus 사망 당시 연금계약 적립액 | [S1] |
| 상속연금형 (한화, 2024) | — | 「피보험자 사망시에는 사망시점 계약자적립액 지급」 | [S7 별표1] |
| 확정기간연금형 (교보) | 책임준비금 + 1,000만원 | 1,000만원 plus the remaining instalments | [S3] |

On an immediate annuity the "before annuitisation" column is a month long, so the
composite carries only the second: **none on the life shape**, and 10% of the single
premium plus the fund on the other two. One carrier makes the fork explicit as a product
code — its 종신연금형 1형 carries a 위험보험료 of 0.00% and its 2형 of 4.9466% [S1 §VIII]
— which is exactly the with-and-without-death-benefit choice priced.

That a Korean annuity may pay so little on death is a regulatory permission, not an
oversight. 감독규정 제7-60조제9호 requires the death benefit of a life product to be at
least cumulative premiums paid, **except after annuity payments have begun**
[REG-R16]; and 제7-60조제7호's requirement that a 금리연동형보험 set a 최저사망보험금
excepts annuities [REG-R16]. Both carve-outs exist for this product and its siblings.

**Exclusions and 면책** (*myeonchaek*). The 약관 form is 「피보험자가 고의로 자신을 해친
경우 … 다만, 피보험자가 심신상실 등으로 자유로운 의사결정을 할 수 없는 상태에서 자신을
해침으로 … 보험금을 지급합니다」 [S7 제6조], with the leaflet stating the period plainly:
「고의적 사고 또는 **2년 이내의 자살**의 경우 사망보험금 지급이 제한될 수 있습니다」
[S3] [S4]. The suicide exclusion period is **two years**, not the three years a reader
coming from `jplib` will expect. Above the 약관 sit the statutory exclusions: 상법 제659조
discharges the insurer for the intention or gross negligence of policyholder, insured or
beneficiary, and 제660조 for war and civil disturbance absent agreement [REG-R49]; but
상법 제732조의2 provides that **gross negligence does not exclude a death benefit** in
인보험, and that where one of several beneficiaries intentionally kills the insured the
others are still paid [REG-R50]. Nothing in the retrieved corpus makes an 즉시연금
death benefit conditional on cause beyond those.

### 계약 전 알릴 의무, 사기에 의한 계약, and misstatement of age

**계약 전 알릴 의무** (*gyeyak jeon allil uimu*, the pre-contract duty of disclosure) is
the 약관's name for the 상법 고지의무 (*gojiuimu*) and the 표준약관 says so in terms
[REG-R25 제13조](#krlib-reg-r25). The insurer may not terminate for breach where it knew or was negligent
in not knowing at formation; where **one month** has passed since it learned of the
breach; where **two years** have passed from the 보장개시일 without a claim event, or one
year for disease under a 진단계약; where **three years** have passed since the contract
date; where it accepted on a health-examination document and the claim arises from a
matter stated in it; or where the 보험설계사 prevented truthful disclosure
[REG-R25 제13조, 제14조](#krlib-reg-r25) [S1] [S7 제16조]. 상법 제651조 sets the outer statutory bounds at
one month from discovery and three years from formation, and 제655조 carries the causation
defence — the insurer must still pay where the non-disclosure is proved not to have
affected the event [REG-R49]. 제14조제5항 bars termination for non-disclosure of **other
insurance held** [REG-R25], which on this product would otherwise be a live issue given
the per-person tax and protection caps.

**사기에 의한 계약** is cancellable within **five years** of the 보장개시일 and one month
of learning of the fraud [S1 §III-3-다] [S7 제17조] [REG-R25 제15조](#krlib-reg-r25).

**Misstatement of age adjusts rather than voids**: 「청약서류상 피보험자의 나이 또는
성별에 관한 기재사항이 신분증에 기재된 사실과 다른 경우에는 신분증에 기재된 나이 또는
성별로 정정하고, 정정된 나이 또는 성별에 해당하는 보험금 및 보험료로 변경합니다」
[S7 제23조제3항]. On an immediate annuity the correction runs to the **annuity**, since
the age and sex select the factor. An age outside the permitted band voids the contract
with a refund, saved where the insured has already reached the entry age by the time the
error is found [S7 제21조]. Both matter more here than on a protection product because the
whole price is one number computed once from age and sex.

### 청약철회, 품질보증해지 and 위법계약의 해지

Three exits sit outside the surrender machinery and all three return more than the
surrender value.

**청약철회** (cooling-off): 15 days from receipt of the 보험증권 and never more than 30
days from the application date, whichever comes first; effective on despatch; premium
returned within three business days, with interest at the 보험계약대출이율 if late
[REG-R51 제46조제1항제1호](#krlib-reg-r51) [REG-R25 제17조](#krlib-reg-r25). The statutory right bars any damages or
penalty [REG-R51 제46조제4항](#krlib-reg-r51) and is ineffective if a claim event has occurred, unless the
policyholder withdrew knowing it had [REG-R51 제46조제5항](#krlib-reg-r51). On a single-premium contract
with a first annuity due a month after cover starts, the cooling-off window and the first
payment date very nearly coincide, and a model that treats t = 0 as a clean boundary is
approximating a fortnight of real ambiguity.

**품질보증해지**: cancellation within **three months** of formation where the 약관 and the
policyholder's copy of the application were not delivered, the important content was not
explained, or the policyholder did not sign, with premiums returned plus interest
[REG-R25 제18조제3항](#krlib-reg-r25), on the authority of 상법 제638조의3제2항 [REG-R49]. This is the
route the 즉시연금 litigation did **not** take — the plaintiffs sued for the unpaid
annuity rather than to unwind — and the Supreme Court's observation that voiding the
contracts outright would leave policyholders worse off is the reason [R22].

**위법계약의 해지** under 금융소비자 보호에 관한 법률 제47조 returns the **계약자적립액**
rather than the surrender value: 「위법계약이 해지되는 경우 회사가 적립한 해지 당시의
계약자적립액을 반환하여 드립니다」 [S7 제34조제5항] [REG-R25 제32조](#krlib-reg-r25). On a product whose
surrender deduction is nil the two coincide, so the distinction is inert here and real
elsewhere in `krlib`.

### Surrender, and why 실효 and 부활 cannot arise

The asymmetry between the shapes is the sharpest contractual fact in the product after
the retention. **종신연금형 cannot be surrendered once the annuity is in payment**:
「종신연금형(정액형, 집중보장형)의 경우 연금지급개시 이후에는 계약을 해지할 수 없습니다」
[S3]; 「계약자는 계약이 소멸하기 전에 언제든지 계약을 해지할 수 있으며(다만, 종신연금이
지급개시된 이후에는 해지할 수 없습니다)」 [S7 제31조], word for word at [S8 제33조]; and
「순수종신연금형을 선택한 경우, 연금지급이 개시된 이후 해지 불가」 [S5 주2]. On an
immediate annuity the annuity begins a month after inception, so **the contract is
irreversible from month one**. Two reasons are given and both are real. The tax
condition: 소득세법 시행령 제25조제4항제4호 requires that a tax-exempt 종신형 not be
surrendered after the first annuity payment [REG-R58] — a contractual term written to
satisfy a statute. And anti-selection: 「종신형에서는 연금지급이 개시된 후 해지를 허용하지
않는다. 이는 사망률이 높은 계약자가 해지함으로써 발생할 수 있는 역선택 위험을 방지하기
위한 장치이다」 [R12 §III-1](#krlib-immediate_annuity-r12).

**상속연금형 and 확정기간연금형 remain surrenderable throughout** [S1] [S3] [S6]. The
surrender value is the 계약자적립액 less the 해약공제액 with a floor of zero
[REG-R19 제7-66조제1항제1호](#krlib-reg-r19), and the deduction is nil at every duration on every
retrieved product [S1 §VIII] [S10] — see the published run reproduced at footnote 31.
Where a surrender is taken after annuitisation on a shape that permits it, one carrier
requires the beneficiary's consent: 「제1항에 따라 연금지급개시 이후에 계약을 해지하는
경우에는 보험수익자의 동의를 얻어야 합니다」 [S8 제33조제2항].

**실효 and 부활 cannot arise on this product.** 표준약관 제26조's 납입최고 — a demand
period of at least 14 days, terminating the contract the day after it ends — and
제27조's 부활, reinstatable within three years on payment of arrears with interest within
평균공시이율 + 1%, both presuppose a renewal premium that can go unpaid [REG-R25]. A
single premium leaves nothing to miss. The consequence for the model is that its only
decrements are mortality — on the life shape alone — and a voluntary surrender on the
other two shapes for which **no source gives a rate at all**; the assumption is **[std]**
and its level and sensitivity live in `technical-notes.md`.

### 선지급 — commutation and instalment frequency

**Commutation of unpaid instalments is available on every retrieved product**, and — the
point a reader from another market will not expect — on survival as well as on death:
「종신연금형의 보증지급기간 안에 보험수익자가 신청한 경우 잔여보증지급기간의 전부 또는
일부(연단위)에 해당하는 연금액을 보험료 및 책임준비금 산출방법서에 따라 공시이율로
할인하여 선지급 할 수 있습니다.(연 1회)」 [S3] — note the annual limit and the
whole-year granularity. The same right, extended to the certain shape, is in the current
약관: 「보험수익자는 종신연금형의 경우 보증지급기간 … 동안의 지급되지 않은 연금액,
확정기간연금형의 경우 연금지급기간 … 동안의 지급되지 않은 연금액을 산출방법서에 따라
공시이율로 할인하여 일시금으로 선지급 받을 수 있으며, 피보험자가 사망한 경우 또한
같습니다」 [S7 제11조제3항, 별표1 주7], and at [S5 주8] and [S1 주5]. One carrier extends
it to a whole policy year's twelve instalments taken in advance [S5 주9]. **The discount
rate is the 공시이율 in every retrieved document** [S1 주4] [S3] [S5] [S7] [S9]; no
retrieved contract uses a separate commutation basis.

The commutation right is a policyholder option with real value on a falling-rate path and
none on a rising one, because the discount rate is the same rate that sets the annuity.
The reference implementation does **not** model its exercise; it records the right and
projects the guaranteed instalments on their contractual dates. That is a **[std]**
simplification and the technical notes say so.

**Instalment frequency.** The 연금연액 may be split monthly, quarterly or half-yearly with
interest at the declared rate on the deferred portions — 「연금을 매월, 3개월, 6개월로
분할하여 지급하는 경우 신공시이율로 계산한 이자를 가산합니다」 [S9 주11], and
identically [S8 주14]. On an 즉시연금 monthly is the default and often the only frequency
offered [S1 주1] [S3]. `Immediate_KR_S` runs that **monthly** mode: it strikes the annuity
on a monthly factor and pays the 연금월액 a row, with `annuity_pp_annual()` publishing the
연금연액 an illustration quotes. The quarterly and half-yearly splits, and the 연단위 mode
[S1 주1], are not separately projected — the interest addition above is what makes them
equivalent in value, and only the monthly one is the market default.

### Expiry and 계약의 소멸

The contract ends differently on each shape, and on none of them at a fixed maturity age:

- **종신연금형** ends on the later of the annuitant's death and the end of the
  보증지급기간, the unpaid guaranteed instalments running on after death unless commuted
  [S3] [S1 주5] [S7 별표1]. Where the 100세 guarantee is elected the guarantee runs to the
  계약해당일 before age 100 — 「보증지급기간이 100세인 경우에는 [보증지급기간−연금개시
  나이+1]년을 보증지급」 [S7 별표1 주6] — which at the anchor age of 60 is a 41-year
  guarantee and not a hundred-year one.
- **상속연금형 만기형** ends on payment of the 만기보험금 at the end of the 보험기간, or
  earlier on death, when the fund and the 10%-of-premium death benefit are paid [S1]
  [S3]. The 종신형 sub-shape ends only on death.
- **확정기간연금형** ends at the end of the 연금지급기간; death does not accelerate it,
  the remaining instalments falling due on their dates or being commutable [S9 주7] [S3].

A note on the tax condition that shapes the first of these: 소득세법 시행령 제25조제4항
제3호 requires that a tax-exempt 종신형 「보험계약 및 연금재원이 소멸할 것」 on death,
with the guarantee period counted only where it sits within the statutory 기대여명 and the
contract extinguishing at the end of that period where the annuitant dies inside it
[REG-R58]. The 약관's own definition tracks it: the 기대여명 is the 통계청 figure for the
annuitant's sex and age at **inception**, decimals discarded, floored at five years, with
the express warning that 「기대여명이 5년 미만일 경우 기대여명은 5년으로 하며, 이 경우에는
관련 세제혜택이 제한될 수 있습니다」 [S7 제2조제6호가목]. A product whose contractual floor
breaks the statutory ceiling, and which says so on its own face.

---

## Riders and options

An 즉시연금 has no riders in the US sense. The payout shape, the guarantee period and the
term are elected at inception, priced into the basis and irrevocable; what remains are two
administrative 제도성특약 and a set of design variants offered by some carriers and not
others.

**In scope (the representative option set):** the three payout shapes; the 보증지급기간 on
the life shape (10년 / 20년 / 100세 / 기대여명, representative 10년); the 연금지급기간 on
the certain shape and the 보험기간 on the inheritance shape; the payment frequency; and
the 선지급 (commutation) right, recorded and not exercised in the projection.

**제도성특약 carried but not modelled:** 표준하체인수특약, the substandard-acceptance
rider offered on this product [S1 §III-1]; and 지정대리청구서비스특약, under which a
nominated relative may claim where the insured cannot [S8] — a facility that matters on a
contract whose annuitant may lose capacity while the contract still has to pay.

**Out of scope, listed for completeness:**

- **The front-loaded life annuity** — 집중보장형 [S2] [S3], 브릿지연금형 [S5],
  소득보장형 [S6], 핵심기간집중형 [S8], 조기집중연금형 [S9], 활동기집중형 [S13]. Same
  mechanic under six names: a multiple of the later annuity paid over a concentration
  period, observed at 2×, 3×, 5× (or 200% / 300%) over five years, ten years, or the whole
  guarantee period. It bridges the gap to the state pension [R12 §III-1](#krlib-immediate_annuity-r12). Implementable as
  a deterministic step on an annuity the model already computes; excluded because no
  source publishes the factor adjustment that pays for the step.
- **The 거치형 (deferred) selling mode** — a 1–5 year deferral at 교보, 삼성 and 동양
  [S3] [S4] [S5], or to a chosen 연금개시나이 at ABL [S6]. This is `Pension_KR_S`'s
  subject, and with it go 추가납입, 중도인출 and the pre-annuitisation death benefit of
  Max[이미 납입한 보험료, 사망당시의 계약자적립액] [S7 제24조제2항].
- **The proportional split across shapes in 5% units** and the 노후설계자금 lump-sum
  election of up to 50% of the fund, both at 푸본현대 [S8]; the second is barred outright
  for a tax-exempt 종신형 by 소득세법 시행령 제25조제4항제2호 [REG-R58].
- **부부계약 / 부부형 (joint life)** [S6] [S5] — mechanics and factors **[unverified]**.
- **The 상속연금형 종신플랜 partial-withdrawal right** that survives annuitisation at one
  carrier [S6 §8-나], the single retrieved exception to the rule that an 즉시연금 has no
  withdrawal facility.
- **연금선수익자 / 연금후수익자** [S5] — a beneficiary-sequencing mechanism, not a cash
  flow.
- **The large-contract discount** [S6 §10-나] [R27] and the **변액즉시연금** (separate
  account), which is `VA_KR_S`'s subject and was not retrieved for this line at all.

---

## Variations across insurers

| Feature | 하나생명 [S1] [S10] | 교보생명 [S2] [S3] | 동양생명 [S4] | 삼성생명 [S5] | ABL생명 [S6] | 한화생명 [S7] (2024, 거치) | 우체국 [S9] (거치) |
|---|---|---|---|---|---|---|---|
| 종신 guarantee menu | 10년, 20년 | 10년/12년, 20년, 30년, 100세 | 10년, 20년, 30년 | rule-based: 10년 min / 기대여명 / (100 − 개시나이) max | 10년, 20년, 100세 | 10년, 20년, 100세, 기대여명 | 20년, 30년, 90세, 100세 |
| Front-loaded variant | none | 집중보장형 (100% uplift) | none | 브릿지연금형 (2×) | 소득보장형 | none in 별표1 | 조기집중연금형 (200%/300%, 5/10년) |
| 상속연금형 | 종신 + 정기 10/15/20년 | 종신 + 만기 10/15/20/30년 | 종신 + 만기 10/20년 | 종신 + 만기 10/15/20/30년 | 종신플랜 + 환급플랜 10/15/20년 | 종신 only | **none** |
| 확정기간연금형 | none | none (2016) / 10·15·20·30년 (2017) | none | none | 5/10/15/20/30년 | 10/15/20년 | 5/10/15/20/30년 |
| 가입나이 (즉시) | 45–80 | 45–80 | 45–80 | **40–85** | 45–75 | n/a | n/a |
| Minimum premium | 4,000만원 | 1,000만원 | 1,000만원 | 1,000만원 | **5,000만원** | n/a | n/a |
| 최저보증이율 as sold | 2.5%/2.0% → 1.5%/1.0% | 1.5%/1.0% → 1.25%/1.0%/0.75% | 2.0%/1.5%/1.0% | 1.5%/1.0% | 2.5%/2.0%/1.0% | **1.0%/0.75%/0.5%** | not extracted |
| 공시기준이율 weighting | prose only | not published | not published | not published | (내부+외부)/2, 80–120% band | prose only | not extracted |
| Death benefit | 기본보험료의 10% + 적립액 | 책임준비금 + 기본보험료의 10% | not extracted | 순수종신: none after annuitisation | not extracted | Max[납입보험료, 적립액] pre-annuitisation | 재해장해보험금 only |
| Commutation | yes, at 공시이율 | yes, 연 1회, 연단위 | not extracted | yes, incl. a whole policy year | not extracted | yes, on death or on request | yes |
| Fund floor at annuitisation | not stated | not stated | not stated | not stated | not stated | **100.1% of premiums** | **100.1% of premiums** |
| Distinctive feature | the only full **상품요약서**, with published 개인연금사망률 and a nil 해지공제 run | the widest illustration table; a 12년 → 10년 guarantee shift between vintages | 즉시 and 거치 on one model point | the tax statute written straight into the 보증지급횟수 rule | the only retrieved **사업방법서**, with the 공시이율 algebra and a size discount | the **post-dispute** 상속연금형 wording naming the deduction | a state provider with **no 상속연금형 at all** |

**What does not vary.** Every retrieved carrier takes its whole expense load once, at
inception, and applies no surrender deduction thereafter; credits a monthly-reset 공시이율
with a duration-stepped floor; recalculates the annuity when the rate moves; forbids
surrender of a 종신연금형 once in payment; permits commutation of unpaid guaranteed
instalments discounted at the 공시이율; offers the annuity monthly, quarterly or
half-yearly with interest on the deferred portion; charges 0.2% of a withdrawal capped at
₩2,000 with four free a year where withdrawals exist at all; and uses 보험나이 on the
six-month rule. Those nine are the product, and none of them is standardized here.

**Why the representative choices were made.**

1. **Chassis and anchor carrier.** 하나생명's 상품요약서 [S1] is the only retrieved
   statutory product summary for an 즉시연금 and the only document that publishes the
   expense load by component and by shape, the 개인연금사망률, the 모집수수료율, a
   fifteen-row surrender-value illustration and a 해지공제액 run of zeros. Every other
   retrieved 즉시연금 document is a two- or four-page leaflet. Choosing it as the anchor
   is a research conclusion; the adoption is **[std]**.
2. **All three shapes, not the life shape alone.** The market's own weights are 73.6%
   상속형, 18.2% 종신형 and 8.2% 확정형 by contract count [R12 표5](#krlib-immediate_annuity-r12). A library that
   modelled only the longevity shape would model 18% of the Korean market and none of its
   litigation. Two of the three shapes use no mortality, which also gives the reference
   implementation a clean interest-only branch against which the crediting mechanic can
   be tested in isolation.
3. **Ten years everywhere.** 97.3% of 종신형 buyers and 77.6% of 확정형 buyers chose ten
   years [R12 표7](#krlib-immediate_annuity-r12); the disputed contract was a ten-year 상속만기형 [R1]; and ten years is
   the shortest term that meets the interest-income exemption on the inheritance shape
   [REG-R58]. One number, four independent reasons.
4. **A 3.50% expense load with a 1.47% risk premium on the death-benefit shapes.** Taken
   from the one carrier that publishes the split [S1] and confirmed on an independent
   carrier's published annuity-certain figures to within 1.4% across four terms [S3]. The
   2012-vintage 6.054% load recovered from the determination [R1] [R2] is a different
   cohort, priced when the declared rate was 4.5%, and is documented rather than adopted.
5. **A 2.50% declared rate with a 1.25% / 1.00% / 0.75% floor.** The declared rate is the
   anchor carrier's own on this product [S1] and equals the 2026 평균공시이율 [REG-R48];
   it sits 5 to 17 basis points **below** the 2.55%–2.67% band of the three most recent
   observations [S12] [S14] [R28], which is stated rather than smoothed. The floor
   is the only three-step schedule published on a contemporaneous 즉시연금 illustration
   whose annuity figures this document also uses [S3], and sits mid-way between the
   2007–2014 cohorts' 2.5%/2.0% [S10] and the 2024 한화 schedule's 1.0%/0.75%/0.5%
   [S7 제7조]. Both are exposed as scalars because no carrier publishes a derivable rate.
6. **The retention as an explicit switch.** Neither the as-designed liability nor the
   determination's liability is "the" right one: the first is what the 산출방법서 said,
   the second is what the 조정결정 ordered [R1], the appellate courts and finally the
   Supreme Court restored the first for the contracts before them [R6] [R21], and the
   current market states the deduction on the face of the 약관 [S7 별표1]. A composite
   that picked one would misrepresent the product. Carrying both is **[std]** and is the
   single most important design decision in this specification.
7. **Vintage and coverage caveats.** Every 즉시연금-specific product document retrieved is
   from 2011–2017 and the market data is from FY2008–FY2009 [R12]; the 2023–2026 sources
   are deferred contracts [S7] [S13] [S14]. 삼성's own 약관 was downloaded but is a scan
   with no text layer, so the richest leaflet in the set [S5] has no 약관 behind it. No
   claim of market-wide coverage is made, and no figure here is presented as current
   market practice without its date.

---

## Regulatory context

**Where the product sits in law.** 즉시연금 is 생명보험 written under 보험업법 제4조's
life licence, and a 연금보험 within the meaning of 보험업감독규정 제1-2조제5호
[REG-R1] [R11]. It is a **저축성보험** at the 기준연령 요건 test of 감독규정 제1-2조제4호,
because the survival benefits exceed the premium paid [REG-R9], which puts it on the
savings side of the boundary 소득세법 제59조의4 draws in the same place [REG-R57]. Two
statutes govern it in parallel and Korean practice keeps them apart: 보험업법 supervises
the undertaking, and **상법 제4편 보험** governs the contract and is one-way mandatory —
제663조 forbids any special agreement varying the Part to the policyholder's disadvantage
[REG-R49]. The statutory hook that lets a life insurer pay a lump-sum entitlement as an
income stream at all is 상법 제727조제2항, added in 2014 [REG-R50].

**기초서류, and the status of the 산출방법서.** A Korean insurer files three 기초서류 —
약관, 사업방법서 and 보험료 및 해약환급금 산출방법서 — under 보험업법 제5조제3호, with
제127조 governing filing and 제128조의2 requiring compliance with them [REG-R2]. 감독규정
제7-64조 lists the 산출방법서's five mandatory contents: the premium calculation, the
reserve calculation, the 해약환급금 calculation including the 해약공제액 and its
comparison against the 표준해약공제액, the calculation where benefits or premiums change,
and the calculation of any 보증비용 [REG-R18]. **The dispute at the centre of this product
is about what that filing does to a policyholder**, and the 분조위 answered: 「산출방법서는
보험회사 내부의 계리적 서류에 지나지 않는 것으로 보험회사가 보험감독당국으로부터 감독이나
명령 등을 받는 공법관계의 근거가 될 뿐이다」 [R1 §3](#krlib-immediate_annuity-r1). A filing that binds the insurer to
the supervisor does not, without more, bind the policyholder. The Supreme Court's
refinement in 2025 is that a bare pointer clause to an undelivered document of formulae
does not discharge the duty of explanation, but that the contract survives with the
offending term severed [R6] [R23]. Both propositions are about 기초서류 rather than about
annuities, and both reach far beyond this product.

**Product design — 감독규정 제7-60조 does most of the work.** Five of its items bear
directly on this product [REG-R16]:

- **제2호** requires a 저축성보험's survival benefit to exceed premiums paid, **except for
  an annuity paying a 생존연금** and for 변액보험. That carve-out is what allows an
  immediate annuity, whose fund is drawn down from month one, to exist at all.
- **제3호 and 제4호** run the accumulation test at the **평균공시이율**: the 계약자적립액
  so accumulated must exceed premiums paid at 납입완료, which for a **single premium is
  fifteen months**, with risk premium, guarantee charge and separate-account fee set to
  zero in the test. How that test is satisfied by a contract that is paying an annuity out
  of the fund over those fifteen months is not settled by anything retrieved; **제3의2호**
  (신설 2023-06-27) provides the escape, exempting an annuity whose 계약자적립액 or annuity
  amount at commencement, computed at the 평균공시이율, exceeds that of a 제3호-compliant
  design provided the two are compared and explained to the customer. Which route a filed
  즉시연금 산출방법서 actually takes is **[unverified]** — no filed basis document for this
  product reaches the question [S6] [R31].
- **제7호** requires a 금리연동형보험 to set a 최저사망보험금 **other than for annuities**,
  and **제9호** requires the death benefit to be at least cumulative premiums paid **except
  after annuity payments have begun**. The two carve-outs together are why a Korean
  immediate annuity may pay 10% of premiums plus the fund on death, and why the life shape
  may pay nothing at all.
- **제10호** (신설 2022-12-22) requires a 금리연동형보험 to set a 최저보증이율 or a
  최저보증금액. The floor is not a commercial courtesy; it is compulsory, and only its
  level is a company matter.

**계약자적립액 and the crediting rate.** 감독규정 제7-65조제1항 makes the 계약자적립액
whatever the 산출방법서 says it is; 제7-65조제3항 requires the 공시이율 to be the
공시기준이율 times a 조정률, with the 공시기준이율 a weighted average of an objective
external index and the insurer's own 운용자산이익률 computed as the FSS Governor
prescribes, and requires the rate to be **uniform across a product class** [REG-R18]. The
class list is at 시행세칙 제5-16조제4항 and **연금보험 is a class of its own** for life
insurers [REG-R23], so an insurer may not declare a different rate on this product than on
its other annuity business. The construction itself is 시행세칙 별표 27, with α capped at
60% [REG-R24]; the four external yields are 국고채(5년), 회사채(무보증 3년, AA−),
통화안정증권(1년) and 양도성예금증서(91일) [REG-R23 제5-16조제3항](#krlib-reg-r23). The **평균공시이율** is
defined at 감독규정 제1-2조제13호 and published through carriers' regulatory disclosure
[REG-R9] [REG-R48].

**Surrender.** 감독규정 제7-66조제1항 sets the 해약환급금 at the 계약자적립액 less the
해약공제액 with a floor of zero, caps the 해약공제기간 at the premium-paying period or
seven years, and fixes the deduction at the **표준해약공제액 of 별표 14**
[REG-R19] [REG-R20]. 별표 14's note 4 gives a 보험기간이 종신인 생존연금보험 that is not a
연금저축보험 a rate of 6% of the 연납순보험료 subject to a 5% × 12 ceiling, and its note 2
fixes the 해약공제계수 at **1 for a single premium** [REG-R20]. None of it binds here,
because the retrieved carriers deduct nothing [S1 §VIII] [S10]; but the cap is what makes
a nil deduction a choice made inside a bounded space rather than an unconstrained one, and
it is the sharpest single difference between Korean surrender-value regulation and the US
or UK equivalents. The 무해지 / 저해지 dispensation of 제7-66조제4항 is unavailable to this
product, which is neither a 순수보장성보험 nor priced on a 최적해지율 [REG-R19].

**Acquisition-cost spreading, and why a single premium is a filing question.** 감독규정
제7-51조 requires a 산출방법서 to be pre-notified where a 저축성보험 does not spread at
least half its acquisition cost evenly over the premium-paying period — 40% for a
whole-life 생존연금, **70% for bancassurance** — the period being at least **fifteen
months for a single premium** [REG-R22]. A bancassurance 즉시연금 that takes its whole
계약체결비용 at inception, as every retrieved product does [S1] [R1], does not spread it,
so the reading that its filing falls inside 제7-51조 is a natural one; whether it is the
reading the FSC takes is **[unverified]**, no filed 즉시연금 산출방법서 having been
retrieved. The companion rule, 제4-32조제5항's cap on first-year commission at the premium
expected in the first year, **does not reach this product at all**: it is confined to
보장성보험 other than general non-life and motor, and an 즉시연금 is a 저축성보험 at
제1-2조제4호 [REG-R9] [REG-R22]. Were it to apply, a 2% commission on a single premium
would satisfy it many times over [S1 §VII], and the observation is worth making only
because it is one of the two places a Korean commission is capped at all.

**The 표준약관 supplies every contractual mechanic that is not carrier-specific**
[REG-R25]: the 보험나이 six-month rule and its worked example (제21조), 청약철회 at 15/30
days (제17조), 품질보증해지 at three months (제18조제3항), the 계약 전 알릴 의무 and its
six bars on termination (제13조, 제14조), 사기에 의한 계약 at five years (제15조), 납입최고
and 부활 (제26조, 제27조 — both inert here), the 해약환급금 article and the requirement
that the insurer hand the policyholder a table of surrender values by elapsed period
(제32조), the 위법계약 return of the 계약자적립액, 소멸시효 (제37조) and the 예금자보호
sentence (제43조). It is drafted against 상법 제4편, whose operative provisions for this
product are 제638조의2 (30 days to accept), 제638조의3 (delivery and explanation), 제649조
(termination at will and the 미경과보험료), 제651조 and 제655조 (non-disclosure and the
causation defence), 제659조 and 제660조 (exclusions) and 제662조 (three-year prescription)
[REG-R49], together with 제727조, 제730조–제733조 and 제736조 in 인보험 [REG-R50]. The
cooling-off right itself is statutory, at 금융소비자보호법 제46조 [REG-R51]; policyholder
protection is ₩100,000,000 per person per insurer from 2025-09-01, with a maturity benefit
falling outside the insurance bucket [REG-R52] [REG-R32].

**Mortality basis.** The industry table is the **제10회 경험생명표**, produced by
보험개발원 and applied to new business from April 2024, and **it is not published**: only
평균수명 (남 86.3세 / 여 90.7세) and 65세 기대여명 (남 23.7년 / 여 27.1년) are public, and
they come to this library through a trade newspaper rather than through KIDI itself
[REG-R33] [REG-R34]. The public anchors are the 국가데이터처 완전생명표 and 간이생명표,
whose 2024 edition gives 기대수명 at birth of 남 80.8년 / 여 86.6년 and 65세 기대여명 of
남 19.5년 / 여 23.7년 on 만나이 [REG-R38], with the single-year qx tables distributed
through KOSIS and not downloaded in this pass [REG-R39]. The gap between the two — about
4.2 years for men and 3.4 for women at 65 — is the insured-versus-population margin any
annuitant table must reproduce. On top of those sit the only carrier-published annuitant
rates in the corpus [S1 §IV-2]. **`Immediate_KR_S`'s `mort_table.csv` is therefore a
[std] construction with a `provenance` column on every row, it is used by the 종신연금형
alone, and it must never be presented as the 경험생명표.** A revision of the industry table
does not touch a contract in payment: 「기가입자는 보험료 변동 영향을 받지 않는다」
[R14, a news article](#krlib-immediate_annuity-r14), and on this product the point is unambiguous because the factor was
fixed the month the premium was paid.

**Tax — and it is the reason the product is shaped the way it is.** 소득세법
제16조제1항제9호 makes the 보험차익 of a 저축성보험 interest income, **except** (가) a
contract held ten years or more meeting the Decree's conditions and (나) a 종신형 연금보험
meeting them [REG-R58]. Two routes are therefore open to an 즉시연금 and they shape
different parts of the product:

- **The ten-year route** (시행령 제25조제3항제1호) requires aggregate premiums per
  policyholder across all such policies not to exceed **₩100,000,000 (1억원)** for
  contracts made from 2017-04-01 — ₩200,000,000 before — and excludes a contract whose
  premium is drawn down as a fixed-term annuity beginning before the tenth anniversary
  [REG-R58]. A 확정기간연금형 of ten years fails; a 상속연금형 만기형 of ten years does
  not, because it pays the interest and returns the principal. The cap explains why the
  anchor premium is exactly ₩100,000,000. **The history of that cap before 2017-04-01 is
  second-hand and the two accounts do not agree.** The retrieved 시행령 puts the cut at
  2017-04-01, ₩200,000,000 applying to 2017-03-31 [REG-R58]; a bank glossary dates a cut
  to ₩100,000,000 per person to the February 2013 amendment that followed the announcement
  of 2012-08-08 [R29, a secondary source](#krlib-immediate_annuity-r29) [R5]. The amendment itself was not retrieved, the
  discrepancy is unresolved, and the pre-2017 figure is therefore **[unverified]**; nothing
  in this document rests on it. What the two accounts agree on is the announcement of
  2012-08-08, and that announcement is what produced the surge of new business in September
  2012 that the FSS warned against, and with it the cohort at the centre of the dispute
  [R5] [R17].
- **The 종신형 route** (시행령 제25조제4항) sets five conditions, and four of them are
  visible in the contract: annuity payable **from age 55 until death**; **no payment in
  any form other than an annuity**; the contract and the annuity fund must extinguish on
  death, with any guarantee period **within the 국가데이터처 기대여명 연수** and the
  contract extinguishing at the end of that period where the annuitant dies inside it;
  and **policyholder, insured and beneficiary the same person, with no surrender after the
  first annuity payment**. The fifth caps the annual annuity by a formula that renders as
  an image on every mirror and **was not retrieved**; it is **[unverified]** and nothing
  here depends on it [REG-R58]. Conditions three and four are why 삼성's 보증지급횟수 is a
  rule rather than a menu — a minimum of ten years or the 기대여명 if shorter, floored at
  five, a middle option equal to the 기대여명 and a maximum of (100 − 연금개시나이) years
  [S5 주4] — and why every retrieved carrier forbids surrender of a 종신연금형 in payment.

**The product is not a 연금계좌**, and that boundary is worth stating because it is the
line between this product and `Pension_KR_S`. The 연금저축 regime — the 12%/15% tax credit
of 소득세법 제59조의3, the ₩6,000,000 and ₩9,000,000 caps, the 연금수령한도 and the
withholding rates including the **3% rate for a 종신계약** — applies to a 연금계좌
[REG-R56]. An 즉시연금 written as an ordinary 저축성보험 is outside it: its income is
이자소득 under 제16조, exempt or not, and no credit is available on the premium.

**Estate and gift tax.** 상속세 및 증여세법 제8조 treats a death benefit received on the
deceased's death under a policy of which the deceased was the policyholder as estate
property, and extends that where the deceased in substance paid the premiums; 제34조 makes
a benefit attributable to another's premiums a gift where beneficiary and payer differ
[REG-R59]. Where an 즉시연금 in payment falls into an estate, a 국세청 예규 of 2021-01-19
values it at 「상속개시 당시 해지환급금 상당액」 [R26, a tax trade report; the ruling
itself was not retrieved](#krlib-immediate_annuity-r26). A competing account puts the valuation at the higher of the
유기정기금 figure and the surrender value, with the 시행령 제62조 discount rate cut to 3%
in 2016 [R29] — **[unverified]**, neither the article nor the amendment having been
retrieved. This is why the 상속연금형 exists at all: 「상속연금형(만기형)을 선택하시면
만기에 수령하는 만기보험금을 상속 및 상속세 재원으로 활용할 수 있습니다」 [S4], and
「연금을 수령하면서 상속세 납부재원을 마련할 수 있는 방법을 제시해드립니다」 [S5].

**Measurement, capital and what this library does not compute.** Korea has run **K-IFRS
제1117호 「보험계약」** and **K-ICS** together since 2023-01-01 [REG-R60] [REG-R13], with a
**해약환급금준비금** appropriated inside retained earnings on top of both to stop an
IFRS 17 balance sheet distributing earnings the contractual surrender-value floor would
later demand [REG-R11], and a 보증준비금 taken after it [REG-R10]. 책임준비금 under
보험업법 제120조 and 감독규정 제6-11조 is a current-estimate quantity delegated to the
FSS Governor [REG-R3] [REG-R10]. **None of it is computed here.** `Immediate_KR_S`
projects gross best-estimate liability cash flows; the reserving and capital layers are
cited, not implemented, in the same way `uklib` treats the SCR. What the library does
compute is the **계약자적립액** and the **해약환급금**, because those are contractual
quantities defined by the 산출방법서 and bounded by a published schedule [REG-R20]. The
work sits under a 선임계리사's verification duties at 보험업법 제181조 and 제184조
[REG-R5]. Nothing product-specific to 즉시연금 was retrieved on the IFRS 17 or K-ICS
treatment of an annuity in payment, and the longevity sub-module is outside this document.

**Supervisory record specific to this product.** Four FSS releases carry 즉시연금 in their
titles: the 소비자경보 of 2012-09-26 against end-of-line selling ahead of the tax change
[R5]; the 보도자료 of 2018-04-09 publishing 조정결정 제2017-17호 and the structural
explanation [R2]; the 보도참고자료 of 2018-09-04 advising policyholders to file a dispute
application to interrupt the three-year limitation under 금융위원회의 설치 등에 관한 법률
제53조의2, and announcing the dedicated 즉시연금 corner on the 파인 portal [R3]; and a 2019
response to press reports about a revived comprehensive examination [R4]. After the
Supreme Court judgment the FSS announced a consumer-protection inspection into the selling
of 즉시연금 [R24] [R25], both news-sourced. The supervisor's own consumer page announced
at [R3 §2](#krlib-immediate_annuity-r3) no longer resolves, and nothing here rests on it.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-immediate_annuity-r1
[R11]: #krlib-immediate_annuity-r11
[R12]: #krlib-immediate_annuity-r12
[R17]: #krlib-immediate_annuity-r17
[R18]: #krlib-immediate_annuity-r18
[R19]: #krlib-immediate_annuity-r19
[R2]: #krlib-immediate_annuity-r2
[R21]: #krlib-immediate_annuity-r21
[R22]: #krlib-immediate_annuity-r22
[R23]: #krlib-immediate_annuity-r23
[R24]: #krlib-immediate_annuity-r24
[R25]: #krlib-immediate_annuity-r25
[R27]: #krlib-immediate_annuity-r27
[R28]: #krlib-immediate_annuity-r28
[R29]: #krlib-immediate_annuity-r29
[R3]: #krlib-immediate_annuity-r3
[R31]: #krlib-immediate_annuity-r31
[R4]: #krlib-immediate_annuity-r4
[R5]: #krlib-immediate_annuity-r5
[R6]: #krlib-immediate_annuity-r6
[REG-R1]: #krlib-reg-r1
[REG-R10]: #krlib-reg-r10
[REG-R11]: #krlib-reg-r11
[REG-R12]: #krlib-reg-r12
[REG-R13]: #krlib-reg-r13
[REG-R16]: #krlib-reg-r16
[REG-R18]: #krlib-reg-r18
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R22]: #krlib-reg-r22
[REG-R23]: #krlib-reg-r23
[REG-R24]: #krlib-reg-r24
[REG-R25]: #krlib-reg-r25
[REG-R3]: #krlib-reg-r3
[REG-R32]: #krlib-reg-r32
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R38]: #krlib-reg-r38
[REG-R39]: #krlib-reg-r39
[REG-R48]: #krlib-reg-r48
[REG-R49]: #krlib-reg-r49
[REG-R5]: #krlib-reg-r5
[REG-R50]: #krlib-reg-r50
[REG-R51]: #krlib-reg-r51
[REG-R52]: #krlib-reg-r52
[REG-R56]: #krlib-reg-r56
[REG-R57]: #krlib-reg-r57
[REG-R58]: #krlib-reg-r58
[REG-R59]: #krlib-reg-r59
[REG-R60]: #krlib-reg-r60
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
