# Product Specification

**Status:** Draft, 2026-09-03 (all cited sources accessed 2026-09-03).

**Scope note.** This is a *standardized composite specification* of Korean whole life assurance
— 종신보험 (*jongsin boheom*, whole-of-life cover) — including the suppressed-surrender-value
forms that now dominate its sales, 무해지환급형 (*muhaeji hwangeuphyeong*, the
no-surrender-value form) and 저해지환급형 (*jeohaeji hwangeuphyeong*, the low-surrender-value
form), assembled for reference liability cash-flow modelling. **It describes no single
insurer's contract.** Facts carrying a source tag — [S#] (primary product documents: 약관
(*yakgwan*, policy conditions), 상품요약서 (*sangpum yoyakseo*, the statutory product summary),
상품안내장 / 보험안내자료 (brochures) and published rate disclosures) and [R#] (regulatory and
actuarial references specific to this product), both numbered per `_research/whole-life.md` and
resolved in `sources.md` (same directory; numbering frozen, never renumbered), and [REG-R#]
(the cross-product reference library `references/regulatory-and-actuarial-references.md`, whose
R1–R60 numbering is separate and also frozen) — were extracted from the cited document. Values
marked **[std]** are standardizations introduced for the reference implementation; each [std]
table row carries a numbered footnote giving the rationale and, where the research pass
established one, the observed range across insurers. Claims that could not be confirmed against
a retrieved document are flagged [unverified].

**Composite base.** Ten carriers' documents were retrieved and read: 처브라이프생명 [S1],
하나생명 [S2] [S9] [S10], KB라이프생명 [S3], DB생명 [S4], KDB생명 [S5] [S8], ABL생명 [S6],
삼성생명 [S7], 교보생명 [S11] [S15], AIA생명 [S12] and 신한라이프 [S13]. **Five of them publish
complete numeric surrender-value grids** for both the suppressed form and its non-marketed
comparison twin [S1] [S2] [S4] [S6] [S8], which is what makes this product's signature mechanic
measurable rather than described. **Two publish the pricing interest rate, the sample mortality
rates and the pricing lapse assumption** in the 상품요약서 [S2] [S8] — a level of disclosure
with no counterpart in `jplib`, `uklib` or `delib`. Against that, **exactly one full 약관 was
retrieved** [S5], and it is a 유니버셜 (universal life) contract rather than a conventional
level-premium one, so contractual articles taken from it are labelled where the chassis
difference could matter. Company and branded product names appear in `sources.md` and in
`_research/whole-life.md` only.

**A note on spelling, kept once.** Korean documents write the surrender value as both
**해약환급금** (*haeyak hwangeupgeum*) and **해지환급금** (*haeji hwangeupgeum*); they are the
same object. The regulation and the 표준약관 (*pyojun yakgwan*, standard policy conditions) use
해약환급금 [REG-R19] [REG-R25], and this library follows them for the *value*. The *forms* keep
the market's own generic pair, 무해지환급형 and 저해지환급형, because that is the supervisor's
own vocabulary — 무(저)해지환급금 보험 [REG-R28]. Carriers market the same mechanic under at
least five further names: 해지환급금 일부지급형 [S1] [S2] [S6], 해약환급금 과소지급형 [S3],
저해지환급형 [S4], 저해약환급금형 [S7] and 해약환급금 미지급형 [S8].

**This product is the library's savings/protection chassis.** It specifies, once and here, the
계약자적립액 (*gyeyakja jeongnibaek*, the policyholder account) recursion and its 보험료적립금
(*boheomnyo jeongnipgeum*, policy reserve) ancestor; the 해약환급금 and its 표준해약공제액
(*pyojun haeyak gongjeaek*)-capped surrender charge; the suppressed 무해지환급형 and
저해지환급형 forms and the step at 납입완료 (*nabip wallyo*, completion of premium payment);
the 보험계약대출 (*boheom gyeyak daechul*, policy loan) as a modelled state; and 보험료
납입면제 (*boheomnyo nabip myeonje*, premium waiver). The [CI product spec
(CI보험)](../ci_insurance/product-spec.md) inherits all of it and adds an accelerated
critical-illness payment; the [pension savings product spec
(연금저축보험)](../pension_savings/product-spec.md) inherits the accumulation half and adds the
연금계좌 tax wrapper and the payout phase. The [term life product spec
(정기보험)](../term_life/product-spec.md) is the protection chassis and states its own
decrement machinery; it shares this document's surrender-value regime, because **one
surrender-value regime governs all ten `krlib` products** [REG-R19 제7-69조·제7-70조](#krlib-reg-r19).
Mechanics specified here are stated once, here.

---

## Product overview and market role

종신보험 is whole-of-life cover: a level premium buys a 사망보험금 (*samang boheomgeum*, death
benefit) payable whenever the insured dies, with no expiry date and no 만기보험금 (maturity
benefit). Every product in the retrieved set states 보험기간 종신 — a whole-of-life policy term
— and none pays anything on survival [S1] [S2] [S3] [S4] [S6] [S8]. One carrier classifies it
in the 상품요약서 in the two words that decide its regulatory treatment: 「보장성보험 /
개인형」 — an individual protection product [S2]. Because the contract must eventually pay, it
accumulates a 계약자적립액 and therefore a 해약환급금, which is what makes it a savings product
sold on protection wording, and what makes every mechanic in this document turn on the
surrender value rather than on the sum assured.

It is a **생명보험상품** (*saengmyeong boheom sangpum*, life insurance product) under 보험업법
제2조제1호가목 — insurance on the survival or death of a person — written under a 제1호가목
생명보험 licence [REG-R1], and 시행령 제1조의2제2항 closes the life list to two contract types,
생명보험계약 and 연금보험계약 [REG-R7]. That places it outside **제3보험** (*je-sam boheom*,
"third insurance"), the statutory category of 상해·질병·간병 cover that both life and non-life
insurers may write [REG-R1 제4조제3항](#krlib-reg-r1) and in which four of this library's ten products sit.
Within life business it is a **보장성보험** (*bojangseong boheom*, protection product), because
at the 기준연령 요건 (*gijun yeollyeong yogeon*, the reference-age condition — "전기납 및 월납
조건으로 남자가 만 40세에 보험에 가입하는 경우") the maturity value does not exceed premiums
paid [REG-R9 제1-2조제2호·제3호](#krlib-reg-r9). Tax law draws the line in exactly the same place, which is
why the classification is a design boundary and not a label: 소득세법 제59조의4 gives the
premium credit to a contract "만기에 환급되는 금액이 납입보험료를 초과하지 아니하는 보험"
[REG-R57].

**Market history, and why the product is young.** 동방생명 (now 삼성생명) offered a 종신보험 in
**March 1959** and it did not sell; the product's real start was 푸르덴셜생명's late-1990s Life
Planner channel, which built a university-graduate male agent force around it and made it the
life industry's biggest single seller of the early 2000s, with 삼성생명 entering in **1999**
[R8]. New business by policy count peaked in 2001 and roughly halved by 2005 [R8]. Everything
the Korean market has invented since has been bolted onto this chassis: **변액종신 (2001), CI
선지급 종신 (2002), 유니버셜 종신 (2004)** [R8], and from the mid-2010s the 무·저해지환급형
forms. The research institute reads the whole arc as a response to falling rates — 「저금리
상황에서 이차역마진 해소와 보험가격 인상 억제를 위한 방향으로 전개 … 금리연동형, 투자연계형
상품의 개발, 변액종신보험, 우량체 할인, **저해지 종신보험**의 개발이 이에 해당한다」 [R8]. The
suppressed form is, in its originator's own framing, an interest-margin device.

**The suppressed forms are not a niche; they are the market.** Life insurers began selling them
in **July 2015** and non-life insurers in **July 2016**, and about **4 million contracts** had
been written by March 2019 [R4] [REG-R28]. By July 2020, **20 of 24 life insurers and 11 of 14
non-life insurers** were selling the form as a flagship line [R2] [REG-R28]. Their share of
protection first-year premium ran **11.4% (2018) → 30.4% (2021) → 47.0% (2023) → 63.8% (2024
H1)** [REG-R27] [R7]. Nearly two thirds of new Korean protection business by first-year premium
is now written in a form whose surrender value is nil or suppressed until 납입완료. **A Korean
reference library that modelled only the 표준형 (*pyojunhyeong*, standard form) would be
modelling a minority of the market**, which is why the suppression here is a model point column
and not a separate model.

**Demand drivers a US or UK reader will not assume.** First, **inheritance**: 상속세 및
증여세법 제8조제1항 deems a death benefit received on the death of the policyholder to be
estate property, while a policy taken out and genuinely paid for by the beneficiary on a
parent's life falls outside 제8조 and is taxed, if at all, under 제34조 — which is why Korean
종신보험 is sold as an inheritance-planning vehicle and why a policy bought at 55 is a normal
transaction [REG-R59]. Second, the **보장성보험료 세액공제**: a **12% tax credit** (15% for a
장애인전용 contract) on premiums up to **₩1,000,000 (100만원)** a year — a credit, not a
deduction, so its value does not rise with the marginal rate [REG-R57]. Third, and specific to
the suppressed forms, a **환급률** (*hwangeumnyul*, the ratio of surrender value to cumulative
premiums paid) engineered to cross 100% shortly after 납입완료, which is precisely the sales
narrative the supervisor named as mis-selling: 「저축성보험처럼 환급률만을 강조하며 판매」 [R2]
[REG-R28].

**Market size is not directly citable from this research pass.** The 생명보험협회 공시실 and
its 금융통계월보 render their tables client-side and returned no figures [R13] [S16] [REG-R45],
and the 손해보험협회 종신보험 comparison returned 「해당 상품이 없습니다」 [S17]. What is
sourced: **보장성보험 수입보험료 of ₩44.3조 (2020), ₩44.3조 (2021), ₩46.5조 (2022), ₩48.0조
(2023) and ₩26.5조 (2024 H1)**, with 초회보험료 up 36.6% year on year in 2024 H1 on
무·저해지환급형 건강보험, 단기납 종신보험, 일시납 연금보험 and 변액보험, and a forecast 9.2%
industry-wide 초회보험료 decline for 2025 [R9]. Widely reported 2024 종신보험 new-business
figures (217만 건 / ₩58조) are trade-press only and are **[unverified]**. What *is* citable and
useful is the **industry comparison basis** Korean disclosure uses for 종신보험 — 보험가입금액
1억원, 종신, 20년납, 월납 [S17] — which the representative model point adopts.

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Level-premium 종신보험; **무배당** (*mubaedang*, non-participating); **금리확정형** (*geumni hwakjeonghyeong*, fixed pricing rate); carries a 계약자적립액 and a 해약환급금; not 유니버셜, not 변액 | [S2] [S8] [R8]; default **[std]** (1) |
| Policy term (보험기간) | **종신** — whole of life. No expiry, no 만기보험금, no survival benefit | [S1] [S2] [S3] [S4] [S6] [S8] |
| Regulatory class | 생명보험상품, 보험업법 제2조제1호가목 and 제4조제1항제1호가목; **보장성보험** at the 기준연령 요건 | [REG-R1] [REG-R7] [REG-R9] |
| Surrender-value form | **Model-point column**, not a separate model. Three values: 표준형 `k = 1.00`; **저해지환급형 `k = 0.50`** (composite default); 무해지환급형 `k = 0.00`. Suppressed period identical to 보험료 납입기간; full value from 납입완료 | Factors: [S1] [S4] [S6] [S7] [S8]. Period: [S1] [S4] [S6] [S7]. Default **[std]** (2) |
| Premium-paying period (납입기간) | 5 / 7 / 10 / 15 / 20 / 30년납, 60 / 65 / 70세납, and 전기납 (종신납) | [S1] [S4] [S6] [S8] [S18]; menu **[std]** (3) |
| Issue age (가입나이) | **보험나이 15–65**, women admitted 3–8 years higher at the same payment term | [S4]; envelope **[std]** (4) |
| Age basis | **보험나이** (*boheom nai*, insurance age): 만 나이 at 계약일 with a fraction under six months discarded and six months or more rounded up, incrementing on each 계약해당일 (policy anniversary), **not** on the birthday | [S5 제21조] [REG-R25 제21조](#krlib-reg-r25) |
| Sum assured (보험가입금액) | **₩10,000,000 – ₩1,000,000,000** (1,000만원 ~ 10억원) in ₩1,000,000 units | [S1] [S8]; adoption **[std]** (5) |
| Sex | Rated separately. The female premium is **84%–91%** of the male at 보험나이 40 across the three published grids — 87%–91% on their 평준형 rows, down to 84% on the 체감형 and 2종 ones | [S1] [S4] [S6] |
| Lives basis | Single life; 계약자 (policyholder) and 피보험자 (insured) the same person. A policy on another's life needs that person's written consent (상법 제731조) and is void below age 15 (제732조) | [REG-R50]; scope **[std]** (6) |
| **Anchor model cell** | 남자, 보험나이 **40세**, 보험가입금액 **₩100,000,000 (1억원)**, 보험기간 **종신**, 납입기간 **20년**, 월납, 저해지환급형 `k = 0.50`. 표준형 월보험료 **₩257,050** (annualized ₩3,084,600) | [S4] [S17] [REG-R9] [REG-R20]; annualization and `k` **[std]** (7) |

Footnotes to [std] rows:

1. **무배당 is not a choice so much as the market.** All eight products in the retrieved set
   are 무배당, and two carriers state the reason in the same words: 「무배당 상품은
   배당상품보다 상대적으로 저렴한 보험료로 가입하실 수 있습니다」 [S2] [S8]. It is also the
   historical design decision that made the product sell — the first successful Korean 종신보험
   was deliberately 무배당 at a time when most Korean products were 유배당, and the lower
   premium was the selling point [R8]. The regulation still carries a full surplus-sharing
   apparatus — 감독규정 제6-13조제1항 caps the shareholder share of 유배당보험이익 at 100분의
   10 — but Korean retail protection is overwhelmingly non-participating and **`krlib` models
   no dividend** [REG-R12]. 금리확정형 is taken over 금리연동형 for the same evidential reason:
   the 상품요약서 that publish complete cash values are 금리확정형 [S8], and the one 금리연동형
   contract retrieved is a 유니버셜 chassis whose account mechanics belong to `Pension_KR_S`
   and `VA_KR_S` [S5]. The 금리연동형 variant is parameterized, not dropped — see *Riders and
   options*.
2. **0.50 is the modal factor and the only one that does not trigger the extra statutory
   conditions.** Observed factors: **30%** at one carrier [S4]; **50%** at three [S1] [S6]
   [S7]; a formula on premiums paid at a fourth [S2]; a straight line on premiums paid to
   납입기간 + 3년 at a fifth [S3]; and **0%** — nil throughout the payment period — at a sixth
   [S8]. 감독규정 제7-66조제4항제2호 attaches two further design conditions only where the
   surrender value during 납입기간 is **less than 50%** of an otherwise identical 표준형
   product's [REG-R19]. A design at exactly 50% therefore sits at the threshold rather than
   below it, which is a plausible reason why 50% is the value three independent carriers chose.
   The 0.00 and 0.30 columns are carried in the model point table so the cliff can be seen at
   all three depths, and the 표준형 column at `k = 1.00` is the comparison twin the contract
   itself names — see *Contractual mechanics*.
3. Observed menus: 7 / 10 / 15 / 20년납 and 전기납 [S1]; 20년납 only [S2]; 5 / 7 / 10년납 [S3];
   5 / 7 / 10 / 15 / 20 / 25 / 30년납 and 50 / 55 / 60 / 65 / 70세납 [S4]; 5 / 7 / 10 / 15 /
   20년납 [S6]; 10 / 12 / 15 / 20년납 [S8]; and 3 / 5 / 7 / 10 / 15 / 20년납, 80 / 90세납 and
   전기납 [S18]. The composite takes the union of the terms that appear at three or more
   carriers, plus 전기납 because it is the 기준연령 요건's own basis [REG-R9]. Two structural
   observations travel with the menu and are not incidental: Korean payment terms are **shorter
   and denser at the front** than Japanese ones — 5년납 and 7년납 appear everywhere — and
   전기납 is offered but is the default nowhere. That is the 단기납 (*dangi-nap*, short-pay)
   market structure showing through.
4. Observed envelopes: 만15~52세 (7년납, 남) to 만15~63세 (15년납, 여) [S1]; 만15~62세 남 /
   만15~67세 여 [S2]; **54~72세 남 / 61~76세 여** on an explicitly senior product [S3];
   만15세~65세 [S4]; 만15세~70세 [S6]; 만15~58세 남 to 만15~66세 여 [S8]. The composite adopts
   [S4]'s 15–65 because it is the only single-figure envelope stated without a
   payment-term-by-sex grid, and because 65 is the mainstream ceiling in the set. **The maximum
   issue age is much lower than Japan's 80**, and the minimum is 15 for a statutory reason:
   상법 제732조 voids a policy on the death of a person under 15 [REG-R50]. One further
   mismatch is recorded rather than resolved: brochures state envelopes in **만 나이** while
   the 약관 rates on **보험나이** [S5 제21조] [REG-R25]; `krlib` treats the published envelope
   as 보험나이 throughout, which shifts a boundary by at most one year.
5. The band is the union of two published ranges: 1,000만원 ~ 10억원 [S1] and 100만원 ~ 30억원
   with a ₩10,000 minimum premium [S8]. The composite takes the narrower floor and the lower
   ceiling because a ₩1,000,000 minimum is what the mainstream products in the set write and
   because a ₩3,000,000,000 case is an underwriting question rather than a product one.
6. No joint-life 종신보험 appears in the retrieved set, so the composite is single-life
   throughout. Third-party-policyholder arrangements are treated as a tax question rather than
   a cash-flow one [REG-R59], and the written-consent and under-15 rules of 상법 제731조 and
   제732조 are stated because they bound who may be insured, not because anything is modelled
   from them [REG-R50].
7. The anchor is chosen so that four independent things line up on one cell. (i) It **is** the
   regulator's own reference cell: 감독규정 제1-2조제2호 defines the 기준연령 요건 as a **만
   40세 male on monthly premiums**, and every Korean product-regulation computation — the
   표준해약공제액 comparison, the 보장성/저축성 test, the 보험가입금액 scaling — is performed
   at it [REG-R9] [REG-R21]. (ii) It is the **industry comparison basis** for 종신보험
   disclosure: 1억원, 종신, 20년납, 월납 [S17]. (iii) It is the basis of **별표 14 note 3**,
   which for a 보장성보험 with a term of 20 years or more recomputes the 연납순보험료 on a
   **20년납** footing — so a 종신 contract's statutory surrender-charge cap is already
   normalised to 20-year pay [REG-R20]. (iv) Three carriers publish a complete surrender-value
   grid at 남 40세 / 1억원 [S4] [S6] [S8], and one of them publishes it at exactly 1억원 /
   20년납 / 월납 for both the 표준형 and the suppressed form [S4]. The published pair at that
   cell is a **30%** design; the composite applies its own `k = 0.50` to the same 표준형 curve,
   which is legitimate precisely because the surrender value is defined by reference to the
   twin and is factor-independent — see *Contractual mechanics*. `WholeLife_KR_S` runs on a
   **monthly** grid, which is the mode every published scale in the set is quoted in, so the
   composite collects the published ₩257,050 a month directly; the model point table still
   carries the annual figure ₩3,084,600 = 12 × it, because a commission scale and a comparison
   disclosure are written in annual units, and the model divides it back. No carrier in the
   set publishes an annual-mode scale, so no modal loading is invented in either direction.

### Premiums

| Parameter | Representative value | Basis |
|---|---|---|
| Premium basis | Level and guaranteed for the whole of 납입기간; 금리확정형, so no review and no crediting-rate feedback into the premium | [S8]; [S2] |
| Mode (납입주기) | 월납 / 3개월납 / 6개월납 / 연납; composite **월납**, collected on the monthly grid | [S1] [S2] [S4] [S6] [S8]; default **[std]** (8) |
| Rating factors | 보험나이, sex, 납입기간, 보험가입금액 (via 고액계약할인), the surrender-value form, and 건강등급 where offered | [S1] [S4] [S6] |
| Pricing interest rate (예정이율 / 적용이율) | **연복리 2.50%**, flat for the whole term | disclosed range 2.25%–2.75% [S1] [S2] [S5] [S6] [S7] [S8]; level **[std]** (9) |
| Price of the suppression | The 저해지환급형 premium is **90.0%** of the 표준형's at the anchor cell | observed 81.5%–95.4% [S1] [S2] [S4] [S6]; pick **[std]** (10) |
| Volume discount (고액계약할인) | **1.5%** of the 주계약 영업보험료 at 보험가입금액 ≥ ₩30,000,000 (3,000만원), riders excluded, re-tested on any change of 가입금액 | [S1]; embedded in the published scale at [S4]; threshold **[std]** (11) |
| Health-grade discount (건강등급 할인) | Up to **8%** on the 주계약 and 10% on 선택특약, graded at 청약 and **recomputed every year**. Named, not modelled | [S6]; scope **[std]** (12) |
| Advance payment (선납) | Up to 11 months excluding the current one, discounted at the 적용이율 or at the 평균공시이율 depending on carrier. Out of scope | [S2] [S3] [S5] [S6]; scope **[std]** (12) |
| Expense loading (계약체결비용 / 계약관리비용) | Contractually named and split — 계약체결비용, and 계약관리비용 subdivided into 유지관련비용 and 기타비용 — but **no rate is published by anyone**. Every expense parameter is **[std]**, bounded above by the 표준해약공제액 and by the 1.4 × disclosure tolerance | [S2] [S5] [S8] [REG-R20] [REG-R22]; **[std]** (13) |
| Price index (보험가격지수) | Published per product: **85.4% 남 / 86.2% 여** at one carrier, **110.3% / 110.9%** at another, both at 40세 / 종신 / 20년납 / 1억원 | [S2] [S8] [REG-R22 제7-45조제7항](#krlib-reg-r22) |
| Pricing lapse assumption (적용해지율) | **Disclosed in the 상품요약서.** 연 1%~10% during 납입기간 at one carrier, with the explicit statement that the 일반형 comparison product carries none; 연 0%~13.4% during 납입기간 and 연 1.0%~11.3% after it at another | [S2] [S8] |
| Premium waiver (보험료 납입면제) | On a **50% 장해지급률** from one cause; premiums cease and are **deemed paid** to the end of 납입기간 for benefit and surrender-value purposes | [S2] [S3] [S6] [S8] [REG-R25 부표 3](#krlib-reg-r25) |
| Preferred-life rating | 우량체 할인 exists in the market [R8] but no scale was retrieved; not modelled | scope **[std]** (12) |

### Benefit provisions

| Parameter | Representative value | Basis |
|---|---|---|
| 사망보험금 | **보험가입금액**, level for life, payable on death at any time, net of any outstanding 보험계약대출 원금과 이자 | [S5 제34조] [S6] [REG-R25 제33조](#krlib-reg-r25) |
| Benefit shape | **평준형** (level) only | [S6]; scope **[std]** (14) |
| Shapes named and excluded | 체증형 (+5% of 가입금액 a year, capped, to 150%) [S1] [S6]; 체감형 (−5% a year from age 60 to a flat 50%) [S6]; a 전환나이 step at 55/60/65/70 [S4]; **max(보험가입금액, cumulative premiums × a published ratio)** [S2] [S3] [S8]; 보험기간 이원화, a reduced disease-death benefit for the first five years [S7] | [S1] [S2] [S3] [S4] [S6] [S7] [S8] |
| Minimum death benefit | 감독규정 제7-60조제9호 requires the death benefit to be **at least cumulative premiums paid**, except after annuity payments begin and except where the 납입기간 ends at age 80 or below. The anchor (납입완료 at 60) sits inside the exception | [REG-R16] |
| Severe-disability benefit | **None.** Korea has no analogue of Japan's 高度障害保険金 paid at the sum assured; the slot is filled by 보험료 납입면제, which continues the contract instead of extinguishing it | [S2] [S3] [S6] [S8] |
| 면책 — suicide | No death benefit where the insured takes their own life **within 2년 of the 계약일** | [S1] [S3] [S6] [S7]; statutory frame [REG-R49 제659조](#krlib-reg-r49) [REG-R50 제732조의2](#krlib-reg-r50) |
| 면책 — other | The intentional act of the 계약자, the 피보험자 or the 보험수익자; war and civil disturbance absent contrary agreement. Gross negligence does **not** exclude a death benefit, and where one of several beneficiaries kills the insured the others are still paid | [REG-R49 제659조·제660조](#krlib-reg-r49) [REG-R50 제732조의2](#krlib-reg-r50) |
| Payment when a benefit is refused | The contract does not simply forfeit: 상법 제736조 obliges the insurer to pay "보험수익자를 위하여 적립한 금액" — in practice the 계약자적립액 — where it is discharged under 제659조 or 제660조 or the contract is terminated for non-disclosure | [REG-R50 제736조](#krlib-reg-r50) [REG-R25 제22조](#krlib-reg-r25) |
| Pre-contract disclosure (계약 전 알릴 의무) | Termination within **1개월** of the insurer learning of a breach, and not after **2년** from the 보장개시일 without a claim event (**1년** for disease on a 진단계약), nor after **3년** from the 계약일. Causation defence available; non-disclosure of other insurance held is not a ground | [S2] [REG-R25 제13조·제14조](#krlib-reg-r25) [REG-R49 제651조·제655조](#krlib-reg-r49) |
| Fraud (사기에 의한 계약) | Cancellable within **5년** of the 보장개시일 and **1개월** of discovery | [S2] [S8] [REG-R25 제15조](#krlib-reg-r25) |
| Claim settlement | 해약환급금 and claim proceeds paid **within 3영업일** of the claim, with interest thereafter per the 약관's 부표; 상법 제658조's 10-day rule applies where no period is agreed | [S5 제31조] [REG-R25 제32조](#krlib-reg-r25) [REG-R49] |
| Underwriting | 표준체 basis. Substandard lives are taken by 할증 (premium loading) or 부담보 (exclusion period); neither is modelled | scope **[std]** (12) |

### Options

| Parameter | Representative value | Basis |
|---|---|---|
| Policy loan (보험계약대출) | Available at any time within **80%** of the 해약환급금 net of existing loan principal and interest; **repayable at any time without fee**; principal and interest deducted from any benefit, from the 해약환급금 and immediately on 해지 | [S5 제34조] [S11] [S13] [REG-R25 제33조](#krlib-reg-r25); limit **[std]** (15) |
| Policy loan rate | **예정이율 + 1.5% = 4.00% p.a.**, compound, and a **vintage** rate: the base is the contract's own 예정이율, so a policy written in a high-rate era carries a high loan rate for life | formula [S9] [S11] [S13]; level **[std]** (15) |
| Loan on a suppressed form | **None at all during 납입기간 on a 무해지환급형 contract** — there is no value to lend against — and only 80% of the *suppressed* value on a 저해지환급형 one | [R4] [REG-R28] [REG-R25 제33조](#krlib-reg-r25) |
| Automatic premium loan (자동대출납입) | **Not evidenced in any retrieved Korean document, and not modelled.** The 표준약관 is understood to contain such an article but the retrieved extract does not carry it, and the one full 약관 in the set handles non-payment through a 월대체보험료 mechanism instead | [S5]; **[unverified]**; scope **[std]** (16) |
| Sum-assured reduction (감액) | Permitted; the reduced portion is **treated as surrendered** and pays the corresponding 해약환급금, on the suppressed basis if made during 납입기간 | [S5 제20조] [REG-R25] |
| Partial withdrawal (중도인출) and 추가납입 | Belong to the 유니버셜 chassis — 12 withdrawals a 보험년도, a 50% single-withdrawal cap and a residual-account floor — and to an 추가납입특약 on a conventional one. Specified for inheritance by `Pension_KR_S` and `VA_KR_S`; not modelled here | [S1] [S5 제33조]; scope **[std]** (16) |
| Annuity conversion (연금전환특약) | A **제도성특약** — attachable at no extra premium. The annuity basis (연금사망률, 계약관리비용, 공시이율, 최저보증이율) is the **rider's at conversion**, not the base contract's at issue. Eligibility gates of 7 or 10 years elapsed and age 45–80 appear at one carrier | [S2] [S3] [S6]; tax basis [REG-R58 시행령 제25조제9항·제10항](#krlib-reg-r58) |
| Persistency bonus (유지보너스) | A 단기납 feature: **10.8% (5년납) / 13.8% (7년납) / 15.0% (10·15년납)** of total 주보험 premiums credited to the 계약자적립액 at 납입완료, with a second 18.5% credit at duration 10 on 5·7년납. Parameterized, **off in the base run** | [S7]; scope **[std]** (17) |
| Reduced paid-up (감액완납) and extended term (연장정기보험) | **Do not appear in any retrieved Korean 약관 or 상품요약서.** Not offered, not modelled | [S5]; **[unverified]** |
| Living-benefit acceleration | One carrier offers a 사망보험금 연금선지급 전환제도 [S7]; another a 생활설계자금 that pays an income by automatically reducing the sum assured [S6]. Both named, both excluded | [S6] [S7]; scope **[std]** (12) |

### Termination and values

| Parameter | Representative value | Basis |
|---|---|---|
| 해약환급금 identity | **계약자적립액 − 해약공제액**, floored at zero: 감독규정 제7-66조제1항제1호 says a negative difference "이를 영(零)으로 처리한다" | [S2] [S8] [REG-R19] |
| 해약공제액 | Unrecovered acquisition cost — 미상각신계약비 (*misangak sin-gyeyakbi*), defined in the 약관 as 「이미 지출한 계약체결비용 해당액으로서 산출방법서에서 정한 방법에 따라 계산한 금액」 — **capped at the 표준해약공제액** | [S5 제2조] [S8] [R6] [REG-R19 제1항제3호](#krlib-reg-r19) [REG-R20] |
| 표준해약공제액 | **연납순보험료 × 5% × 해약공제계수 + 보험가입금액 × 10/1000.** For a 보장성보험 the 해약공제계수 is the **보험기간 capped at 20**, and the 연납순보험료 is recomputed on a 전기납 basis, or on a **20년납** basis where the term is 20 years or more — which for a 종신 contract it always is | [REG-R20 별표 14](#krlib-reg-r20) [R6] |
| 표준해약공제액 at the anchor | ≈ **₩3,470,000** — 1.0 × 연납순보험료 (₩2,467,680 at a **[std]** net-premium ratio of 80%) + 1% of ₩100,000,000. Cross-check: the practitioner rule of thumb for a 보장성보험 is **13 × the monthly premium** = ₩3,341,650, agreeing within 4% | [REG-R20] [REG-R29]; net-premium ratio **[std]** (13) |
| 해약공제기간 | **납입기간 or 신계약비 부가기간, capped at 7년.** On the anchor's 20년납 contract the surrender charge is therefore fully run off by duration 7, thirteen years before the cliff | [REG-R19 제7-66조제1항제2호](#krlib-reg-r19) |
| 계약자적립액 accrual | **Monthly** before 납입완료, **daily** afterwards. The two accrual formulas are images in the 고시 and did not extract | [REG-R19 제7-66조제1항제4호](#krlib-reg-r19) |
| Suppression factor | `k = 0.50` for elapsed duration < 납입기간; `k = 1.00` from 납입완료 | [S1] [S6] [S7]; **[std]** (2) |
| What the factor multiplies | **The 표준형 twin's 해약환급금** — a non-marketed comparison product with identical benefits priced with the lapse assumption switched off — not the sold product's own account | [S1] [S2] [S3] [S4] |
| The step at 납입완료 | A **discontinuity**, and the product's signature. On the one grid published at 남 40세 / 5,000만원 / 10년납 the value goes from **₩25,640,000 at duration 9 to ₩57,655,500 at duration 10** — a 2.25 × step in one year — and the 환급률 from **49.9% to 101.0%** | [S1] |
| Post-cliff equality | From 납입완료 the suppressed and 표준형 surrender values are **identical** in every published grid | [S1] [S4] [S6] |
| Clawback | Where premiums falling in the suppressed period were not paid, they must be made good before the post-cliff basis applies | [S2] [S3] [S8] |
| Waived premiums | Months waived under 납입면제 **count as paid** for the surrender-value computation, so a waiver does not push the policyholder back down the ramp | [S2] [S3] [S6] [S8] |
| 미경과보험료 | Added to the 해약환급금 on termination — 「해약환급금에 미경과보험료 등을 가산한 금액을 … 지급하여야 한다」 | [REG-R19 제7-66조제5항](#krlib-reg-r19) |
| 만기보험금 | **None** | [S1] [S2] [S4] [S8] |
| Demand period (납입최고 / 독촉) | **14일 이상** from the day after the monthly 계약해당일, extended to the next business day if it would end on a non-business day; the contract is **해지 the day after it ends** | [S5 제25조] [REG-R25 제26조](#krlib-reg-r25) |
| Lapse (해지) | **Behavioural, not funded.** With no 자동대출납입 in evidence, a Korean contract lapses at the end of a 14-day demand period whatever its cash value | [S5] [REG-R25]; contrast **[std]** (16) |
| Loan-driven termination | On 해지 the loan principal and interest are deducted from the 해약환급금 **immediately**, and the demand notice must say so | [S5 제25조·제34조] [REG-R25 제26조](#krlib-reg-r25) |
| Reinstatement (부활) | Within **3년** of 해지, on fresh 고지 and payment of arrears with interest at a company rate **within 평균공시이율 + 1%**. Available even where the 해약환급금 was **nil** — the 무해지 case is expressly included | [S5 제26조] [REG-R25 제27조](#krlib-reg-r25) |
| Cooling-off (청약철회) | **15일** from receipt of the 보험증권 and never later than **30일** from the application, whichever comes first; **45일** for a distance sale to a policyholder aged 65 or over. Effective on despatch; premiums returned within 3영업일. Out of scope | [S1] [REG-R25 제17조](#krlib-reg-r25) [REG-R51]; scope **[std]** (18) |
| Quality-guarantee cancellation (품질보증해지) | Within **3개월** of formation where the 약관 was not delivered, its important content not explained, or the application not signed; premiums returned with 보험계약대출이율 interest | [REG-R25 제18조제3항](#krlib-reg-r25) [REG-R49 제638조의3](#krlib-reg-r49) |
| Unlawful-contract cancellation (위법계약해지권) | Within **1년** of learning of the breach and **5년** of the contract; the 계약자적립액 is returned | [S1] [REG-R25 제29조의2](#krlib-reg-r25) |
| Prescription (소멸시효) | 보험금청구권 **3년**; 보험료 또는 적립금의 반환청구권 **3년**; 보험료청구권 2년 | [REG-R49 제662조](#krlib-reg-r49) |
| Policyholder protection | **₩100,000,000 per person per insurer** since 2025-09-01, applied separately to four claim buckets, with maturity proceeds expressly outside the insurance-claim bucket | [REG-R52] [REG-R32]; the carrier documents in the set still print the superseded ₩50,000,000 [S1] [S2] |

Footnotes to the [std] rows above, continuing the numbering:

8. Every published premium scale in the set is quoted **monthly** [S1] [S2] [S4] [S6] [S7]
   [S8], monthly is the 기준연령 요건's own mode [REG-R9], and one carrier bars the annual mode
   outright for a 납입면제 rider [S1]. `WholeLife_KR_S` is **monthly-step**, so the composite
   pays the published monthly figure in the month it falls due, and the two errors the earlier
   annual-step composite had to state — an overstated annual premium and an understated
   first-year interest credit — no longer arise. No carrier publishes the modal loading a real
   연납 scale carries, so the annual column is exactly 12 × the monthly rate and no loading is
   invented in either direction.
9. **Unlike Japan, Korea publishes the pricing rate**, and six values were read from carrier
   documents: **연복리 2.3%** (2022-04) [S1]; **2.3%** on the 예정적립금 of a 유니버셜 contract
   (2021-05) [S5]; **2.25%** (a 2023 vintage) [S2]; **2.25% for ten years then 1.75%** — a term
   structure inside one carrier's pricing basis (2023-09) [S7]; **2.75%** on a 금리확정형
   contract (2024-01) [S8]; and **2.50%** on an 추가납입특약 (2025-09) [S6]. The composite
   takes **2.50%** because it sits at the centre of the 2.25%–2.75% band actually read, because
   it is a quarter-point value on the 0.25%p grid Korean rate-setting uses, and because it
   equals the **2026 평균공시이율** [REG-R48], which is the regulatory reference rate against
   which product design is tested [REG-R16]. Two cautions. The rate is a *pricing* rate and
   lives in the unpublished 산출방법서 [REG-R2]; what carriers publish is a disclosure of it,
   not the filing. And search results reporting a market-wide 예정이율 cut in April 2025 and
   again for 2026 could not be confirmed against any retrieved carrier document and are
   **[unverified]** — what is sourced is the 평균공시이율 series, which fell from 2.75% to
   **2.50%** for 2026, its first fall since the 2.50% → 2.25% step in 2021 [S10] [REG-R48].
10. The suppression is paid for in premium, and the discount is much smaller than the
    surrender-value haircut. Measured directly wherever a carrier publishes both scales for one
    cell: **89.9%** at a 50% factor [S1]; **94.3% 남 / 92.9% 여** on the formula design [S2];
    **81.5%** (1종) and **86.8%** (2종) at a 30% factor [S4]; **94.4% / 95.4% / 94.0%** across
    three 종 at a 50% factor [S6]. The observed range on real products is **81.5%–95.4%**, with
    the deepest discount at the deepest suppression. The FSC's own illustration of a
    post-amendment design shows **62.2%** [R1] [REG-R28], which is a much larger discount than
    any sold product in the set and is best read as an illustration of returning the whole
    give-up as premium rather than as a market observation. The composite takes **90.0%** at a
    50% factor, which is a rounding of the 89.9% 처브라이프 observation at that suppression
    factor [S1] and sits between the 30%-factor and the shallower 50%-factor observations.
    The ratio is a **price** input and never touches the surrender value: the anchor's premium
    is 90.0% of the sourced 표준형 figure, and the model's own loading rule multiplies its
    equivalence net premium by the same ratio, so the two agree by construction and
    `technical-notes.md` reports the fit.
11. Only one carrier states a threshold: 「주계약의 보험가입금액이 3,000만원 이상인 계약에
    대하여 주계약 영업보험료를 1.5% 할인하여 이를 영수합니다. (단, 부가특약은 제외)」, with a
    re-test on any later change of 가입금액 [S1]. A second states that its published scale
    already embeds a 고액계약할인 and a 장기납입계약할인 without naming either [S4]. The
    composite adopts the one stated rule. Note that it **bites at the anchor**: 1억원 is well
    above 3,000만원, so the published anchor premium is a post-discount figure, and a model
    that applies the discount a second time double-counts it.
12. Excluded because it changes the premium or the benefit *stream* without changing any
    mechanic this chassis exists to demonstrate, and because each needs an unpublished basis to
    model: the annually re-rated 건강등급 discount (a premium re-rated every year on a health
    measure has no analogue anywhere else in this repository, and its four-grade scale runs
    374,440 / 378,510 / 386,650 / 394,790 against an ungraded 407,000, i.e. 8.0% down to 3.0%)
    [S6]; 선납 [S2] [S3] [S5] [S6]; 우량체 할인 [R8]; substandard 할증 and 부담보; and the
    living-benefit accelerations [S6] [S7]. Each is named here so that a reader meeting it in
    the market knows it is real and knows this library does not model it.
13. **This is the largest quantitative gap in the file.** Both 상품요약서 in the set define
    계약체결비용 and 계약관리비용 — 「보험회사가 보험계약의 체결, 유지 및 관리 등에 필요한
    경비로 사용하기 위하여 보험료 중 일정비율을 책정한 것」 — and then give **no number** [S2]
    [S8]; the 약관 defines 부가보험료 and 해약공제액 by reference to the 산출방법서, which is a
    filed but unpublished 기초서류 [S5] [REG-R2]. **No Korean expense rate as a percentage of
    premium was obtained from any source in this research pass.** Four public handles bound the
    [std] assumption instead: the **표준해약공제액** itself [REG-R20]; the **1.4 × tolerance**
    of 감독규정 제7-45조제11항, under which a whole-life death-benefit 보장성보험 need not
    publish a 계약체결비용지수 provided its 계약체결비용 stays within 1.4 × the 표준해약공제액
    — so a reference implementation setting 계약체결비용 at or below the cap is conservative
    and defensible [REG-R22]; the **first-year commission cap** of 제4-32조제5항, under which
    first-year remuneration may not exceed the first year's expected premium, with the
    projected one-year surrender value added to the commission side where the contract deducts
    80% or more of the 표준해약공제액 [REG-R22]; and the **보험가격지수**, whose observed range
    of **85.4%–110.9%** across two carriers bounds how far a Korean whole-life product's total
    loading can sit from the industry mean [S2] [S8]. The **80% net-premium ratio** used to
    illustrate the 표준해약공제액 above is itself [std] on the same evidence, and the
    illustration is offered as an order of magnitude, not as a computed cap.
14. 평준형 is the only shape common to the whole set and the only one on which the cliff can be
    isolated. A 체감형 or a 전환나이 step-down would collide with the suppression boundary at
    or near the same date; a 체증형 changes the reserve run-off; and the max(가입금액, premiums
    × ratio) designs make the benefit a function of the premium stream, which would entangle
    the death decrement with the lapse assumption in exactly the place this model needs them
    separable. The last of those is worth understanding rather than merely excluding, because
    it exists for a regulatory reason: 감독규정 제7-60조제9호 requires a death benefit of at
    least cumulative premiums paid, and a design whose payment period runs past age 80 cannot
    use the exception [REG-R16]. Published ratios, by issue age and sex, run 남 30세 240% /
    40세 197% / 50세 163% and 여 30세 267% / 40세 218% / 50세 178% [S2].
15. **The limit varies more in Korea than anywhere else in this repository**: 「해약환급금의
    50% ~ 85%까지」 at one carrier, varying by product within that band [S11]; 「해약환급금의
    50 ~ 80%이내」 at another [S13]; and the whole 해약환급금 net of existing loan in the one
    full 약관, subject to 「순수보장성보험 등 보험상품의 종류에 따라 보험계약대출이 제한될 수
    있습니다」 [S5 제34조] [REG-R25 제33조](#krlib-reg-r25). The composite takes **80%**, the top of the
    narrower published range and inside the wider one. The **rate** is better evidenced than
    the limit: 「적용이율 + 1.5%」 or 「예정이율 + 1.5%」 on a 금리확정형 contract and
    「공시이율 + 1.5%」 on a 금리연동형 one, at three carriers independently [S9] [S11] [S13],
    with a 가산금리 of +1.40%~1.50% at one [S11]. The composite therefore sets the loan rate at
    **예정이율 + 1.5% = 4.00%** and holds it flat, and the vintage banding tells the modeller
    the right thing: one carrier's published historical schedule runs +1.50% (2026) back
    through +1.90% (2020–2024), +2.00% (2018–2020), +2.50% (2013–2018) and fixed 8.50% and
    10.00% bands in the 2000s, all under a 최고 적용 대출이율 of 9.90% [S12], and a live
    published range of **연 3.5%~10.5%** spans the whole in-force book at one carrier [S11].
    Small concessions — −0.10%p for insureds aged 65 and over, or on contracts whose 예정이율
    is 5.5% or 7% and above — are real but immaterial to a new-business projection [S11] [S12]
    [S13].
16. **The single sharpest Korea/Japan difference in this document, and it is a negative
    finding.** `jplib`'s whole life chassis turns on the 自動振替貸付, which advances the
    premium against the surrender value at the end of grace and keeps the contract in force, so
    that lapse there is a *funded* event. **No 자동대출납입 provision was found in any Korean
    document retrieved in this research pass.** The 생명보험 표준약관 is understood to contain
    such an article, but the retrieved 별표 15 extract does not carry it [REG-R25] and three
    independent routes to the standard-form text failed; the one full Korean 약관 in the set
    handles non-payment through a 월대체보험료 deduction from the account, which is a 유니버셜
    mechanic and not an APL [S5]. `WholeLife_KR_S` therefore **does not implement an automatic
    premium loan**, and Korean lapse is modelled as a behavioural decrement acting at the end
    of a 14-day demand period. The claim that Korea has no APL is **[unverified]** and is the
    highest-value single item for the next research pass, because if a 표준약관 article is
    found the lapse mechanics of this chassis change in kind. 중도인출 and 추가납입 are
    excluded for a different reason: they are evidenced [S1] [S5] but belong to the 유니버셜
    chassis, which `Pension_KR_S` and `VA_KR_S` inherit and specify.
17. The 유지보너스 (*yuji boneoseu*) is parameterized and off by default because it is a
    **단기납** feature, not a whole-life one: it appears on 5년납 and 7년납 designs and is the
    thing that produced the 2023–24 refund-ratio competition. Its published rates are 주보험
    10.8% (5년납), 13.8% (7년납) and 15.0% (10·15년납) of total premiums credited to the
    계약자적립액 at 납입완료, with 체증형보장특약 rates of 9.5% / 12.6% / 31.5% and a second
    18.5% credit at duration 10 on 5·7년납 [S7]. Two consequences make it worth specifying even
    unmodelled. It produces a **second step** in the surrender-value curve — on the published
    grid the 환급률 goes 41.5% at duration 5 to 99.7% at 7 (납입완료) to **120.5% at 10** and
    on to 206.7% at 50 [S7]. And 감독규정 aside, the supervisor now requires an **additional
    lapse of at least 30%** at any such bonus date, or a rate backed out of the 표준형
    product's cumulative persistency, calibrated to the 29.4%–30.2% eleventh-year lapse
    observed on single-premium bancassurance savings [REG-R27] [R3]. Turning the bonus on
    without turning that spike on would misstate the liability in the insurer's favour, which
    is exactly what the guidance exists to prevent.
18. The statutory cooling-off applies to every contract in this composite — the exclusion for
    terms of 90 days or less cannot bite on a 종신 contract [REG-R51] [REG-R25 제17조](#krlib-reg-r25). `krlib`
    projects from the point cover is in force and scopes the window out, stated here rather
    than silently omitted because it is a real early-duration decrement that a first-year study
    would see. The same applies to 품질보증해지 and to the 위법계약해지권.

---

## Contractual mechanics

Notation used below and carried into `technical-notes.md`:

    x       가입나이 (보험나이) at issue
    t       completed months since the 계약일 (the monthly grid step); policy year = t // 12 + 1
    m       보험료 납입기간 in years, 12m in months; m = infinity on a 전기납 (종신납) contract
    n_sc    해약공제기간 = min(m, 7) years, 12 n_sc in months
    SA      보험가입금액
    G       annual gross premium (영업보험료); G^m = G / 12 is the monthly instalment,
            level for t < 12m and zero for t >= 12m
    P       annual net premium (순보험료) on the 표준형 basis -- the 연납순보험료 별표 14
            names; P^m is its monthly equivalent, the one the account consumes
    i       예정이율, the pricing interest rate per annum; j = (1+i)^(1/12) - 1 per month
    q(x+t)  the pricing mortality rate (적용위험률) at attained 보험나이 x+t, an ANNUAL
            probability; q^m = 1 - (1-q)^(1/12) is its monthly conversion
    d       the month-end the value cells are indexed by, d = 0 at issue; a 계약해당일 is
            d = 12y, and the flows of month t open at d = t and close at d = t + 1
    V(d)    계약자적립액 of the 표준형 twin at d
    SC(d)   해약공제액 at d, capped at the 표준해약공제액
    W(d)    표준형 해약환급금 at d = max(0, V(d) - SC(d))
    CV(d)   the 해약환급금 actually payable at d
    k       the suppression factor: 1.00 표준형, 0.50 저해지환급형, 0.00 무해지환급형
    L(d)    outstanding 보험계약대출 principal and interest at d
    i_L     the 보험계약대출이율 = i + 1.5% per annum; j_L its monthly equivalent

### The death benefit, and what happens when a benefit is refused

The 사망보험금 is `SA`, level for life, payable on death at any time and reduced by `L(t)` [S5
제34조] [REG-R25 제33조](#krlib-reg-r25). There is **no severe-disability acceleration**: Korea does not put a
고도장해보험금 at the sum assured on this chassis, and the slot that Japanese whole life fills
that way is filled here by **보험료 납입면제**, which stops the premiums and continues the
contract rather than extinguishing it [S2] [S3] [S6] [S8]. For modelling this is a
simplification and a complication at once — one decrement on one benefit amount, but a second
state (premium-waived, in force) that the Japanese design does not have.

The **suicide exclusion runs two years** from the 계약일, at four carriers independently [S1]
[S3] [S6] [S7] — one year shorter than the three-year period uniform across the Japanese
market, and the difference is real rather than presentational. Its statutory frame is 상법
제659조, which discharges the insurer where the insured event arises from the intention of the
보험계약자, 피보험자 or 보험수익자, read with 제732조의2, which provides that **gross
negligence does not exclude a death benefit** and that where one of several beneficiaries
intentionally kills the insured the others are still paid [REG-R49] [REG-R50]. The two-year
window is therefore a contractual narrowing of an open-ended statutory exclusion in the
policyholder's favour, which 상법 제663조 permits and the reverse would not be. The 표준약관
article stating the two-year period was **not itself in the retrieved extract**, so the
attribution of the specific two-year figure to the standard form rather than to carrier
practice is **[unverified]**; the figure itself is sourced four times over.

Where a benefit is refused for an 면책사유, the contract does **not** simply forfeit. 상법
제736조 obliges the insurer, on discharge under 제659조 or 제660조 and on termination under
제649조, 제650조, 제651조 or 제652조~제655조, to pay "보험수익자를 위하여 적립한 금액" — the
amount it has accumulated for the beneficiary, in practice the 계약자적립액 [REG-R50]. The
표준약관 makes the same idea explicit for a 제3보험 contract in 제22조 (계약의 소멸), paying
"산출방법서에서 정하는 바에 따라 회사가 적립한 사망 당시의 계약자적립액" [REG-R25], and
감독규정 제7-63조제1항제1호 turns it into a design requirement for that class [REG-R17]. **A
model that treats an exclusion as a zero-payment event overstates the insurer's position**; the
composite treats a refused death claim as a payment of the account balance.

### 계약자적립액 — the account, and the recursion this chassis defines

Korea has two names for the same object and the difference between them dates the document. A
pre-2023 상품요약서 writes 「보험료 계산시 적용한 위험률로 산출한 **순보험료식 책임준비금**
에서 **해지공제액**을 공제한 금액을 해지환급금으로 지급합니다」 [S2]; a 2024 one writes
「보험료 계산시 적용한 위험률로 산출한 **계약자적립액**에서 **미상각신계약비**를 공제한 금액을
해약환급금으로 지급합니다」 [S8]. The identity is the same in both wordings —

    해약환급금 = 적립금 − 해약공제액

— and the change of name is the visible trace of IFRS 17: under K-IFRS 제1117호 the insurer no
longer books a 보험료적립금 as a separate statutory reserve [REG-R60], so the surrender basis
had to be re-anchored on a contractually defined policyholder account rather than on a
balance-sheet reserve. The same drift is visible in the regulation itself, where the filing
document is renamed from 「보험료 및 **책임준비금** 산출방법서」 to 「보험료 및 **해약환급금**
산출방법서」 between the 2023 and 2026 editions of the 고시 [REG-R9]. The *causal* reading is
**[unverified]** — no retrieved document states it — but the wording difference is sourced
twice [S2] [S8], and the modelling consequence is not in doubt: **the quantity a `krlib` whole
life model computes is the 계약자적립액, and it is a contractual quantity, not a reserve.**

감독규정 제7-65조제1항 says only that "계약자적립액은 보험료 및 책임준비금 산출방법서에 따라
계산한 금액으로 한다" and 제2항 permits it to be computed on an **annualised premium** basis —
"연납보험료를 기준으로 하여 산출할 수 있다" [REG-R18]. That permission is what let an annual
grid carry a monthly-premium product's account; **`WholeLife_KR_S` no longer needs it**.
제7-66조제1항제4호 states the accrual convention the account is actually owed: it accrues
**monthly before 납입완료 and daily afterwards**. The two formulas render as images in the
고시 and did not extract, so a monthly step remains a **[std]** reading of them — but it is
the step the rule names, and the daily accrual after 납입완료 is the one part still
approximated [REG-R19].

The composite therefore defines the 표준형 twin's account by the classical net-level recursion,
on the pricing basis and on the monthly grid:

    V(0) = 0
    V(d+1) = ( V(d) + P^m ) * (1 + j) - q^m * ( SA - V(d+1) )       end-month benefit

solved forward, with the net premium `P` fixed at issue by equivalence over the 납입기간 —

    P * a-due(x, m) = SA * A(x)

— where `a-due(x, m)` is the annuity-due of premium payments and `A(x)` the whole-life
assurance, both on the 예정이율 `i` and the 적용위험률 `q`. Three properties of this recursion
are contractual rather than conventional and a model must not lose them. It is **net level
premium**: the acquisition cost is not Zillmerised into the account, it is deducted from it,
and the deduction is what 별표 14 caps. It runs on the **표준형** net premium, not on the sold
form's lower one — see the cliff section below. And it is bounded below by nothing: the account
may be smaller than the surrender charge, in which case the 해약환급금 is zero and not negative
[REG-R19 제7-66조제1항제1호](#krlib-reg-r19).

The **금리연동형 variant** replaces `i` in the accrual step with a declared 공시이율 (*gongsi
iyul*) reset monthly, floored at a 최저보증이율 (*choejeo bojeung iyul*). The mechanism is set
out verbatim in the one full 약관: 「이 계약의 계약자적립금 계산시 적용되는 이율은 매월 1일
회사가 정한 신공시이율(최저보증이율은 연복리 0.75%를 적용)로 합니다 … 이 계약의 사업방법서에서
정하는 바에 따라 운용자산수익률과 외부지표금리를 가중평균하여 산출된 일반계정
신공시기준이율에서 향후 예상수익 등을 고려한 조정률을 가감하여 결정합니다」 [S5 제32조]. The
regulatory chain behind that sentence is complete and public: 공시이율 = 공시기준이율 ± 조정률
[REG-R18 제7-65조제3항](#krlib-reg-r18); the 공시기준이율 is `외부지표금리 × α + 운용자산이익률 × (1 − α)` with
the four index rates being 국고채(5년), 회사채(무보증 3년, AA−), 통화안정증권(1년) and
양도성예금증서(91일) on a three-month weighted moving average, and **α capped at 60%** [REG-R24
별표 27](#krlib-reg-r24) [REG-R23 제5-16조제3항](#krlib-reg-r23); the 공시이율 must be **uniform across a product class**, and
**보장성보험(종신보험) is a class of its own** [REG-R23 제5-16조제4항](#krlib-reg-r23); and a 금리연동형
product **must** set a 최저보증이율 or a 최저보증금액 [REG-R16 제7-60조제10호](#krlib-reg-r16). The α cap is
the modelling point: a Korean declared rate is majority-weighted to the insurer's own realised
운용자산이익률, not to market yields, which is why a crediting-rate assumption in this library
is a slow-moving [std] scalar rather than a function of a yield curve. A claimed ±30% cap on
the 조정률 could not be confirmed against any retrieved document and is **[unverified]**.

### 해약공제 and the 표준해약공제액 cap

The surrender charge is **unrecovered acquisition cost**, defined by reference to what was
actually spent — 「이미 지출한 계약체결비용 해당액으로서 산출방법서에서 정한 방법에 따라 계산한
금액」 [S5 제2조] — and it is capped by a published schedule. That cap has no US or UK analogue
at this level of prescription, and it is the reason a `krlib` surrender-value construction can
be defended at all when no insurer publishes an expense rate.

별표 14 to the 보험업감독규정 states it in one line [REG-R20]:

    표준해약공제액 = 연납순보험료 × 5% × 해약공제계수 + 보장성보험의 보험가입금액 × 10/1000

with, for a 보장성보험, a **해약공제계수 equal to the 보험기간 capped at 20 years** and a
**연납순보험료 recomputed on a 전기납 basis, or on a 20년납 basis where the 보험기간 is 20
years or more** [REG-R20 주2·주3](#krlib-reg-r20). A 종신 contract always falls in the second case, so for this
product the formula collapses to

    표준해약공제액 = 1.0 × 연납순보험료(20년납 기준) + 0.01 × 보험가입금액

— **one year's net premium plus one per cent of the sum assured**. The 보험가입금액 that enters
it is not simply the face amount: 별표 15 제3호 sets it, for a 보장성보험 covering 일반사망, to
the 일반사망보험금, and 제8호 takes it **before any 체증 or 체감** [REG-R21]. On the anchor
cell that is ₩100,000,000 exactly, contributing ₩1,000,000, and a **[std]** 80% net-premium
ratio puts the whole cap at about **₩3,470,000**. The practitioner's rule of thumb — the FSC
states the same cap as 「보장성보험 월 보험료의 13배 수준」 [REG-R29] — gives 13 × ₩257,050 =
₩3,341,650, within 4%. Two forms of the same rule agreeing to that tolerance is the strongest
available check on a parameter that no carrier publishes.

Two further bounds sit on top and both are public. 감독규정 제7-45조제11항 exempts a whole-life
death-benefit 보장성보험 from publishing a 계약체결비용지수 provided its 계약체결비용 stays
within **1.4 ×** the 표준해약공제액 — an explicit tolerance, and therefore an outer bound for a
[std] acquisition-cost assumption [REG-R22]. 제4-32조제5항 caps first-year distributor
remuneration at the first year's expected premium, adding the projected one-year surrender
value to the commission side where the contract deducts **80% or more** of the 표준해약공제액 —
which is exactly what a 무해지 or 저해지 design does — and 제8항 obliges the insurer to offer
an instalment structure paying **no more than 60% of the 표준해약공제액 a year** [REG-R22]
[REG-R29]. A research presentation to the FSC's own public hearing records that competition had
pushed carriers past the cap — 「보험회사 간 경쟁심화로 표준해약공제액을 초과하는 사업비를
부가하는 상품 존재」 — and that the policy answer was a disclosure obligation rather than a
prohibition [R6] [REG-R37].

**The duration over which the charge runs is fixed by regulation and it is short.** 감독규정
제7-66조제1항제2호: "해약공제기간은 보험료 납입기간 또는 신계약비 부가기간으로 하되 … **7년
이상일 때에는 7년으로** 한다" [REG-R19]. On the anchor's 20년납 contract the charge is fully
amortised by duration 7 — **thirteen years before the cliff**. That separation matters, because
it means the step at 납입완료 has nothing whatever to do with the surrender charge running off;
by then it has been gone for over a decade. The *shape* of the run-off inside the seven years
is in the unpublished 산출방법서, so the composite takes a straight line —

    SC(t) = 표준해약공제액 × max(0, 1 − t / n_sc),     n_sc = min(m, 7)

— as a **[std]** construction calibrated to reproduce the published grids at the anchor, with
the fit reported in `technical-notes.md`. That is the honest position: the *cap* is sourced and
exact, the *level* is calibrated to published cash values, and only the *shape between points*
is standardized.

### 해약환급금 and the 무해지 / 저해지 cliff

The payable surrender value is

    W(t)  = max( 0, V(t) - SC(t) )                     the 표준형 twin's value
    CV(t) = k * W(t)      for t <  m       (k = 0.50 저해지, 0.00 무해지, 1.00 표준형)
    CV(t) =     W(t)      for t >= m

and the transition at `t = m` is a **step**. This is the product's signature and the one thing
a model must not smooth.

**The factor multiplies the twin, not the sold product's own account.** Every carrier that
sells a Design-A form names a comparison product in the same sentence and says it is not sold:
「"표준형"의 경우는 "해지환급금 일부지급형"과 동일한 보장내용으로 **해지율을 적용하지 않고** 이
보험의 「보험료 및 책임준비금 산출방법서」에 따라 계산된 상품이며 … 비교안내를 위한 종목으로
**실제로 판매하지 않습니다**」 [S1], with the same sentence and their own product names at
three more carriers [S2] [S3] [S4]. That clause is the most important actuarial statement in
the whole source set, and it settles three things at once. The 표준형 curve is the account
run-off computed **with the lapse assumption switched off**; the sold product's surrender value
is a stated fraction of it; and after 납입완료 the two are the **same number**. The published
grids confirm the last point exactly: at 납입완료 the suppressed and 표준형 values are
identical to the won — ₩57,655,500 at duration 10 [S1], ₩57,838,000 and ₩26,764,000 at duration
20 on two 종 [S4], ₩45,772,000, ₩26,294,000 and ₩67,148,000 at duration 10 on three 종 [S6].
And the suppression ratios during the payment period are exact: 1,164,500 / 2,329,000 = 0.50000
and 25,640,000 / 51,280,000 = 0.50000 [S1]; 1,526,128 / 5,087,095 = 0.30000, 7,584,900 /
25,283,000 = 0.30000 and 12,150,300 / 40,501,000 = 0.30000 [S4]; every pre-완납 ratio exactly
0.5 across three 종 [S6].

**So a model needs one `W(t)` and one multiplier, not two account runs** — and, critically,
`CV(t)` is **independent of the sold form's own premium**. That single fact explains the whole
of the 환급률 arithmetic that sells the product. Because the suppressed form's premiums are
lower while its post-완납 surrender value is identical, its refund ratio after the cliff is
mechanically higher than the 표준형's: 116.4% against 94.9% at duration 20 on one grid [S4],
101.0% against 90.9% at duration 10 on another [S1], 114.4% against 108.0% at duration 20 on a
third [S6]. Nothing is being credited to the policyholder that the 표준형 does not get; the
denominator is smaller.

**The cliff, measured.** On the fullest published run — 남 40세, 5,000만원, 10년납, 월납, a 50%
factor — the surrender value goes from **₩25,640,000 at duration 9 to ₩57,655,500 at duration
10**, a **2.25 × step in one year**, and the 환급률 from **49.9% to 101.0%** [S1]. On the nil
form the same event is starker still: **exactly zero at every duration through fifteen years**,
then ₩52,320,000 at duration 20 — 100.0% of premiums paid — climbing to 161.1% at duration 60
[S8]. A model of that form has **no surrender cash flow at all until 납입완료**, which is
precisely why the lapse assumption over that period is worth so much CSM and why the supervisor
intervened.

Five contractually distinct suppression designs exist and a model that assumes one of them is
universal will be wrong at most carriers. They are set out in *Variations across insurers*
below. Three consequences of the design the composite adopts are contractual rather than
incidental:

**Everything derived from the surrender value is suppressed with it.** The 보험계약대출 limit
and the 감액 proceeds are computed off `CV(t)`, so during the suppressed period both are half
their 표준형 size — and on a 무해지 contract **the policy loan does not exist at all**, a point
the FSS made in terms in its 2019 consumer alert and the 표준약관 repeats as 「순수보장성보험
등 보험상품의 종류에 따라 보험계약대출이 제한될 수도 있습니다」 [R4] [REG-R28] [REG-R25
제33조](#krlib-reg-r25).

**A clawback survives the step.** Where premiums falling in the suppressed period were not
paid, they must be made good before the post-cliff basis applies — 「납입하지 않은 보험료가
있는 경우, 미납된 보험료를 모두 납입하여야 … 해당하는 해약환급금을 지급합니다」 [S2] [S3] [S8].
Conversely, **waived premiums count as paid** [S2] [S3] [S6] [S8], so 납입면제 is the one route
to the cliff that does not require the policyholder to fund it — which makes the waiver a
genuine option with value on this design and not merely a protection feature.

**The step is not a surrender-charge effect.** As set out above, the 해약공제기간 is capped at
seven years [REG-R19], so on any contract with a payment period longer than that the charge is
long gone before the cliff. The step is the removal of the multiplier `k`, nothing else.

### The regulatory permission behind the cliff — 감독규정 제7-66조제4항

The suppressed form is not a contractual gimmick. It is a **regulatory dispensation conditional
on having priced with a best-estimate lapse rate.** 제7-66조제4항 permits an insurer, for a
순수보장성보험 or a whole-life 생존연금 "보험료 또는 보험금을 **최적해지율**을 사용하여 산출한
경우", to pay **less than** the 제1항 value that 별표 14 floors — "제1항에서 정한 해약환급금
미만으로 지급할 수 있다" [REG-R19]. Three qualifications ride on it:

- **제4항제1호** (신설 2020-11-19) bars the form outright for a **변액보험**, which is why
  `VA_KR_S` may not use it and must carry a full 별표-14-floored surrender value [REG-R19].
- **제4항제2호** attaches two further conditions **only where** the surrender value during the
  payment period is **less than 50%** of an otherwise identical 표준형 product's: 가. the
  post-payment surrender value must exceed 50% of the 표준형's, and 나. the post-payment 환급률
  must exceed the greater of 100% and the 표준형's 환급률 [REG-R19].
- The FSC's own announcement of the amendment, effective **2020-11-19**, describes the same
  rule in the opposite direction — that such a product must be designed 「전(全) 보험기간 동안
  표준형 보험의 환급률(기납입보험료대비) 이내로」 — and carries the worked comparison that
  produced it, on a 종신보험 at 20년납 / 1,000만원 / 남 40세 [R1] [REG-R28]:

  | 구분 | 표준형 | 무해지 (개정 전) | 무해지 (개정 후) |
  |---|---|---|---|
  | 월 보험료 | 23,300원 | 16,900원 | 14,500원 |
  | 10년 환급률 | 86.5% | 0.0% | 0.0% |
  | 20년 환급률 | 97.3% | **134.1%** | **97.3%** |

  Both statements of the rule are recorded as they stand; the operative article text was read
  in the 고시 [REG-R19] and the framing sentence in the press release [REG-R28]. **The
  representative design sits comfortably inside either reading**, because at `k = 0.50` the
  surrender value during 납입기간 is exactly 50% of the 표준형's — at the threshold of
  제4항제2호 rather than below it — and after 납입완료 it is identical to the 표준형's.

The arithmetic of the published grids is consistent with the article as recorded. DB생명's 30%
design clears both limbs: its post-완납 value equals the 표준형's (so it exceeds 50% of it) and
its post-완납 환급률 of 116.4% exceeds max(100%, 94.9%) [S4]. KDB생명's nil design satisfies 나
by construction, since its post-완납 payout is defined as 「이미 납입한 보험료 × max(기준상품
해약환급률, 100%)」 [S8]. And 하나생명's formula design never falls below 50% of its 일반형's
value except in the first year, so 제4항제2호 does not bite on it at all [S2]. **The single
most useful sentence a Korean drafter can carry away is that the deep forms are legal only
because they clear a post-completion refund test, and the 50% form is legal without having
to.**

One further regulatory consequence of the form sits outside this model and is stated because it
shapes the insurer's economics. The **해약환급금준비금** (*haeyak hwangeupgeum junbigeum*,
surrender value reserve) compares, company-wide at every balance-sheet date, the IFRS 17
잔여보장요소 against the aggregate contractual 해약환급금 **computed under 제7-66조제1항 — on
that rule even for the 제7-66조제4항 products that may contractually pay less** — and
appropriates the shortfall inside 이익잉여금 [REG-R11]. So a 무해지 contract whose contractual
surrender value is zero still enters the test at its 별표-14-floored value. The reserve stood
at **₩23.7조 at end-2022 and ₩32.2조 at end-2023** [REG-R36] [R7], it is graded by the
insurer's K-ICS ratio, and a well-capitalised insurer (K-ICS ≥ 130% before transitionals at the
previous quarter-end) appropriates only **80%** of the shortfall [REG-R11]. **`WholeLife_KR_S`
does not compute it**; it is named because it is the reason a Korean insurer's economics on
this product depend on the surrender value and not only on the fair-valued liability.

### The lapse assumption is not free

Two independent bases for the lapse rate exist in Korea, they are disclosed, and they do not
agree with each other. Both bound the [std] vector this library uses.

**The pricing basis is published in the 상품요약서**, which has no counterpart anywhere else in
this repository. One carrier: 「「…(해지환급금 일부지급형)」에 적용한 해지율은 **1%~10%**이며,
**일반형에는 적용해지율이 적용되지 않습니다**」 [S2]. Another: 「적용해약률은 보험료 납입기간
및 경과기간별로 상이하며, 보험료 납입기간 중 **연 0%~연 13.4%**를 적용합니다. 보험료 납입기간
이후에는 **연 1.0%~연 11.3%**의 해약률을 적용합니다」 [S8]. Neither publishes the *shape*, only
the envelope — so a duration-by-duration curve is a [std] construction bounded by these.

**The valuation basis was set by the supervisor in November 2024**, and it is much lower. The
problem the FSS named was that, with no experience on 무·저해지 business, insurers assumed high
lapse right up to 완납 on contracts where lapsing pays nothing, booking CSM that would never be
realised and pricing low enough to distort the whole market toward the form [REG-R27] [R3]. The
remedy: among models converging to zero at 완납 the **로그-선형 (log-linear) 모형** is adopted
as the **원칙모형**, with a practical convergence point of **0.1% at 납입완료**; **after
납입완료 the ultimate rate is 0.8%**, from overseas statistics, or a **20% relativity** to the
standard form's rate; alternatives (선형-로그, 로그-로그) are permitted only against
audit-report and management disclosure of the difference in **CSM, best-estimate liability,
K-ICS ratio and net income**, external actuarial validation, quarterly FSS reporting and an
on-site inspection; and on a **단기납 종신** design carrying a bonus, an **additional lapse of
at least 30%** must be assumed at the bonus date [REG-R27] [R3] [R7]. Effective from the 2024
year-end close.

`WholeLife_KR_S` therefore carries a **log-linear decay to 0.1% at 납입완료 and 0.8%
thereafter** as its [std] base vector, with a switch to a flat 표준형 assumption so that the
two can be run side by side — which is exactly the comparison the guidance obliges an insurer
to disclose [REG-R27]. **No Korean lapse curve by duration was obtained from any public
source**; the two bases above are the whole of the evidence, they serve different purposes, and
they cannot be reconciled from public data. This is the single largest assumption gap for this
product.

One asymmetry is worth naming because it is counter-intuitive. On a design whose post-완납
surrender value exceeds premiums paid, a **high** lapse rate is a cost to the insurer, not a
profit source — which is why the K-ICS 대량해지위험 shock splits by whether surrender reduces
or increases net assets, applying a **+35%p** or **+25%p** addition to the next year's lapse
rate on 순자산 감소상품 and a **× (1 − 40%)** reduction on 순자산 증가상품, against a flat 25%
(보장성) or 35% (저축성) mass-lapse on the 표준형 [REG-R36] [R7]. Those figures come from
시행세칙 별표 22, which was **not retrieved**, so they are quoted through the research report
that reproduces them and are **[unverified] as regulatory text** [REG-R26] [REG-R36].

### Premium payment, 납입최고 and 해지 — and why Korean lapse is behavioural

Premiums are due on the monthly 계약해당일 for the chosen mode. Non-payment starts the
**납입최고(독촉)기간**, which is **14일 이상** — seven days where the policy term is under a
year — running from the day after the anniversary and extended to the next business day if it
would end on a non-business day; the contract is **해지 on the day after it ends** [S5 제25조]
[REG-R25 제26조](#krlib-reg-r25). The notice must state the arrears, the consequence of non-payment, and that
「계약이 해지되는 때에는 즉시 해지환급금에서 보험계약대출의 원금과 이자가 차감된다」; an
electronic notice requires the policyholder's prior consent and a confirmed receipt, failing
which the insurer must re-notify by post or recorded call [S5 제25조].

**Fourteen days is far shorter than Japan's one to two months, and there is no automatic
premium loan behind it.** That combination is the sharpest structural difference between this
chassis and `jplib`'s. In Japan the 自動振替貸付 advances the premium against the surrender
value at the expiry of grace and the contract continues, so lapse there is a *funded* event and
a model that applies a lapse rate without first testing the loan condition is modelling a
decrement the contract does not have. **In Korea, on the evidence retrieved, there is no such
test.** No 자동대출납입 provision was found in any retrieved 약관 or 상품요약서; the 표준약관
is understood to contain such an article but the retrieved 별표 15 extract does not carry it
[REG-R25], and the one full 약관 in the set handles non-payment on a 유니버셜 chassis through a
월대체보험료 deduction from the account instead [S5 제24조]. The composite therefore models
lapse as a **behavioural decrement acting at the end of the demand period**, with the loan
balance settled against whatever surrender value exists — and flags the absence of an APL as
**[unverified]**, because a 표준약관 article found in a later research pass would change the
mechanics of this chassis in kind rather than in degree.

The consequence for the suppressed forms is sharp and runs the opposite way to Japan's. In
Japan the cliff bites through the APL, by shrinking the value the contract can borrow against.
In Korea there is no such buffer at all: a 무해지 policyholder who misses fourteen days loses
the contract and receives **nothing**, and the whole of the accumulated value is forfeited to
the fund. That is the consumer-detriment finding behind the 2019 alert [R4] [REG-R28] and it is
the reason the lapse assumption on this form became a supervisory matter rather than an
actuarial one.

### 보험계약대출 as a modelled state

The 보험계약대출 is universal on this chassis and its 약관 wording is unusually uniform across
carriers [S5 제34조] [REG-R25 제33조](#krlib-reg-r25):

> ① 계약자는 이 계약의 해지환급금(다만, 보험계약대출의 원금과 이자를 차감한 금액) 범위 내에서
> 회사가 정한 방법에 따라 대출을 받을 수 있습니다. 그러나, 순수보장성보험 등 보험상품의
> 종류에 따라 보험계약대출이 제한될 수 있습니다.
> ② 계약자는 … 언제든지 상환할 수 있으며 상환하지 않은 때에는 회사는 보험금, 해지환급금 등의
> 지급사유가 발생한 날에 지급금에서 보험계약대출의 원금과 이자를 차감할 수 있습니다.
> ③ 회사는 … 계약이 해지되는 때에는 즉시 해지환급금에서 보험계약대출의 원금과 이자를
> 차감합니다.

Modelled as a state, on the monthly grid, the balance rolls up at compound interest and is
extinguished against any exit. The rate is quoted per annum and the roll runs on its monthly
equivalent `j_L = (1 + i_L)^(1/12) - 1`, so twelve months compound back to exactly `1 + i_L`:

    L(0)   = 0
    L(t+1) = ( L(t) + D(t) - R(t) ) * (1 + j_L)
    D(t)  <= 0.80 * CV(t-1) - L(t)      the limit, tested at the draw and not after it
    with  claims, surrenders and lapses paid net of L(t), floored at zero

where `D(t)` is the amount drawn and `R(t)` the amount repaid at `t`. Take-up and repayment
behaviour are **[std]** behavioural assumptions with no public Korean data behind them; the
limit and the rate are sourced. Four features of the Korean loan matter and none of them is
optional:

**The rate is a vintage rate, not a market rate.** The formula is 「예정이율 + 1.5%」 (or
「적용이율 + 1.5%」) on a 금리확정형 contract and 「공시이율 + 1.5%」 on a 금리연동형 one, at
three carriers independently [S9] [S11] [S13], with a 가산금리 stated as +1.40%~1.50% at one
[S11]. Because the base is the **contract's own** 예정이율, a policy written in a high-rate era
carries a high loan rate for life — one carrier's published live range spans **연 3.5% ~
10.5%** across its in-force book [S11], and its historical 가산금리 schedule runs +1.50% (from
2026) back through +1.90%, +2.00%, +2.50% and fixed 8.50% and 10.00% bands in the 2000s, all
under a 최고 적용 대출이율 of **9.90%** [S12]. A 금리연동형 loan is priced off the 최저보증이율
where the 공시이율 falls below it [S9].

**The limit is a fraction of the *payable* surrender value**, so on a suppressed form it is
suppressed too: half its 표준형 size on a 저해지 contract during 납입기간, and **zero on a
무해지 one** [R4] [REG-R28]. The observed limits are 50%–85% [S11] and 50%–80% [S13]; the
composite takes 80%.

**There is no early-repayment fee** at any carrier that states one [S11] [S13], and the loan
term runs to the contract's own maturity — for a 종신 contract, indefinitely [S11].

**The loan is settled first on every exit.** Principal and interest are deducted from a death
claim, from a voluntary 해약 and — 즉시, immediately — from the 해약환급금 on 해지 for
non-payment [S5 제34조] [REG-R25 제26조](#krlib-reg-r25). Korea has no equivalent of the Japanese
loan-excess-lapse notice: the deduction is automatic and the contract's termination is driven
by the demand period, not by the loan balance.

### 보험료 납입면제 — the waiver, and why it is an option with value

The Korean substitute for Japan's severe-disability acceleration, and structurally different
from it: the contract continues, the premiums stop, and **the death benefit and the surrender
value are computed as if the premiums had been paid.**

The base trigger is disability, worded almost identically at four carriers: 「보험료 납입기간
중 피보험자가 장해분류표 중 동일한 재해 또는 재해 이외의 동일한 원인으로 여러 신체 부위의
장해지급률을 더하여 **50% 이상**의 장해상태가 되었을 경우에는 다음 회 이후의 보험료 납입을
면제」 [S2] [S3] [S6] [S8]. Two features of that sentence are load-bearing. It **aggregates
across body parts from one cause**, so it is a percentage test on the 장해분류표 scale rather
than a binary event; and it covers **both 재해 (accident) and non-accident causes**. The
장해분류표 itself is 부표 3 to the 생명보험 표준약관, which defines 장해 as "상해 또는 질병에
대하여 치유된 후 신체에 남아 있는 **영구적인** 정신 또는 육체의 훼손상태 및 기능상실 상태",
expressly excluding temporary states during treatment [REG-R25]. It is the common percentage
scale behind premium waiver in every Korean protection product, which is why `Term_KR_S`,
`CI_KR_S`, `Cancer_KR_S` and `Child_KR_S` can all state a waiver without re-defining one.

**The "deemed paid" rule is what makes it a modelling problem**: 「그러나 이 경우에도 보험료가
보험료 납입기간 종료일까지 월계약해당일에 정상적으로 납입된 것으로 하여 사망보험금 및
해지환급금을 계산합니다」 [S2], carried verbatim at two more carriers [S3] [S8]. A waived
policy therefore accrues surrender value on the full premium scale while paying nothing — and
on a suppressed form it is **the only way to reach the cliff without funding it**. In a
projection the waived state is a distinct state with its own persistency: no premium income,
full benefit outgo, full account accrual, and the ordinary mortality decrement.

**Disease riders extend the trigger** and are the commercial heart of the modern product. Three
shapes appear: **3대질병** — 암, 뇌출혈, 급성심근경색증, with cancer excluding 기타피부암,
갑상선암 and 대장점막내암 at one carrier and the narrower 「기타피부암, 중증갑상선암 이외의
갑상선암 및 대장점막내암 제외」 at another [S1] [S2] [S3]; **6대질병** [S6]; and a menu of
2종(장해50%) / 3종(재해장해50%) / 3대질병형 / 6대질병형 as separate riders [S5]. A **90-day
면책기간 applies to the cancer trigger** — 「암 … 에 대한 보장개시일은 계약일로부터 그 날을
포함하여 90일이 지난날의 다음 날부터입니다」 [S3] [S5] — and two rules travel with it: a
policyholder diagnosed before the 암보장개시일 may cancel the rider within 90 days of diagnosis
and have the premiums returned, and if they do not, a later recurrence or metastasis of that
same cancer never triggers the waiver unless five years pass from the 암보장개시일 with no
further diagnosis or treatment [S1]. Attachment is controlled: one carrier requires the 주계약
and every rider to share the same 납입기간, bars mid-term attachment, caps the combined monthly
premium at ₩500,000 aggregated across the insured's existing waiver riders, and bars the annual
mode [S1].

### 감액, and the two options Korea does not have

**감액 (sum-assured reduction) is universal and is a partial surrender.** The 약관 treats the
reduced portion as terminated: 「그 감액된 부분은 해지된 것으로 보며, 이로써 회사가 지급하여야
할 해지환급금이 있을 때에는 … 해지환급금을 계약자에게 지급합니다」, with the warning that
「보험가입금액을 감액하면 해지환급금이 없거나 최초 가입할 때 안내한 해지환급금보다 적어질 수
있습니다」 [S5 제20조]. On a suppressed contract that warning is not a caveat but the main
event: a reduction made during 납입기간 pays at `k × W(t)`, and on a 무해지 contract it pays
nothing at all.

The 약관 also gives the pro-rata restatements that follow a reduction, and they matter because
several Korean designs make the death benefit a function of premiums paid [S5 제20조]:

    감액 후 이미 납입한 보험료 = 감액 전 값 × (감액 후 적립금 / 감액 전 적립금)
    감액 후 중도인출 누적액     = 감액 전 값 × (감액 후 가입금액 / 감액 전 가입금액)
    감액 후 초과납입액          = 감액 전 값 × (감액 후 가입금액 / 감액 전 가입금액)

with a worked example in the 약관 itself: 이미 납입한 보험료 1,000만원 and 계약자적립금
1,200만원 reduced to 600만원 gives 감액 후 이미 납입한 보험료 = 1,000 × 600 / 1,200 =
**500만원** [S5]. One carrier turns 감액 into a product feature — a **생활설계자금** paying an
annual income for 2 to 20 years from 납입완료 to age 90 by automatically reducing the sum
assured and paying the resulting surrender value, subject to the remaining sum assured staying
at least the greater of 20% of the pre-application amount and ₩20,000,000, with any policy loan
repaid first [S6]. That is a decumulation option built out of partial surrender and it has no
analogue elsewhere in this repository; it is named and excluded.

**감액완납 (reduced paid-up) and 연장정기보험 (extended term) do not appear in any retrieved
Korean document.** The 60-article 약관 in the set has no such article — 제20조 offers only
보험가입금액, 계약자 and 「기타 계약의 내용」 as variables — and every 상품요약서 in the set is
silent [S5]. Search results describe both as generally available Korean maintenance options,
but neither was confirmed against a primary document, so both are **[unverified]** as features
of a Korean 종신보험 and `WholeLife_KR_S` does not model them. This is the clearest case in the
file where a reader arriving from `jplib` — where 払済保険 and 延長定期保険 are both in the
約款 — would import a feature Korea has not been shown to have. What Korea offers in that slot,
and what *is* sourced, is 감액 above and the payment holiday on a 유니버셜 chassis.

### 고지의무, 사기, and the contestability clocks

The **계약 전 알릴 의무** is the 상법 고지의무 in contractual dress, and the 표준약관 says so
in terms [REG-R25 제13조·제14조](#krlib-reg-r25). The insurer may not terminate for a breach where: it knew or
was negligent in not knowing at formation; **one month** has passed since it learned of the
breach; **two years** have passed from the 보장개시일 without a claim event — **one year** for
disease on a 진단계약; **three years** have passed since the 계약일; it accepted on a
health-examination document and the claim arises from a matter stated in it; or the 보험설계사
prevented truthful disclosure. Two defences travel with it: the **causation defence** of
제14조제4항, matching 상법 제655조, under which the insurer must still pay where the
non-disclosure is proved not to have affected the event; and 제14조제5항, which bars
termination for non-disclosure of **other insurance held** [REG-R25] [REG-R49]. The statutory
frame is 상법 제651조 — termination within one month of learning and within **three years** of
formation, with a matter asked about in writing presumed material [REG-R49]. One carrier states
the contractual windows directly as 2년 / 1년 [S2].

**사기에 의한 계약** is separate and longer: proxy examination, drug use to pass underwriting,
forged certificates or concealment of a pre-application cancer or HIV diagnosis are cancellable
**within five years of the 보장개시일 and one month of learning of the fraud** [REG-R25 제15조](#krlib-reg-r25)
[S2] [S8].

Both clocks **restart on 부활**, because reinstatement resets the 보장개시일 [REG-R25 제27조](#krlib-reg-r25).

### 청약철회, 품질보증해지 and the 위법계약해지권

Three exits sit in front of the projection and all three are scoped out of the model.

**청약철회** — the statutory cooling-off of 금융소비자보호법 제46조제1항제1호, which the
표준약관 제17조 implements: 「「상법」 제640조에 따른 보험증권을 받은 날부터 **15일**과 청약을
한 날부터 **30일** 중 먼저 도래하는 기간」, extended to **45일** for a distance sale to a
policyholder aged 65 or over [S1] [REG-R25] [REG-R51]. It is effective **on despatch**, no
penalty may be charged, premiums are returned within 3영업일 with 보험계약대출이율 interest
thereafter, and it is ineffective if a claim event has already occurred unless the policyholder
withdrew knowing it had. Three contracts are excluded, none of which can be a 종신보험: an
insurer-funded health examination, a term of 90 days or less, and a 전문금융소비자.

**품질보증해지** — cancellation within **three months** of formation where the 약관 and the
policyholder's copy of the application were not delivered, the important content was not
explained, or the policyholder did not sign, with premiums returned plus interest [REG-R25
제18조제3항](#krlib-reg-r25). Its statutory source is 상법 제638조의3제2항 [REG-R49].

**위법계약해지권** — under the 금융소비자보호법, exercisable within **one year** of learning of
the breach and **five years** of the contract [S1]; on exercise the 계약자적립액 is returned
rather than the 해약환급금 [REG-R25 제29조의2](#krlib-reg-r25).

### 부활

Within **three years** of a 해지 under 제26조, and provided the 해약환급금 has not been drawn,
the policyholder may apply to reinstate on fresh 고지 and payment of the arrears with interest,
at a company-set rate **within 평균공시이율 + 1%** [S5 제26조] [REG-R25 제27조](#krlib-reg-r25). The insurer
may **not** refuse because a claim event occurred before termination.

The parenthesis in the 약관 is the operative point for this product: the surrender value counts
as undrawn 「보험계약대출 등에 따라 해지환급금이 차감되었으나 받지 않은 경우 또는
**해지환급금이 없는 경우를 포함**합니다」 [S5]. **A 무해지 contract is therefore always
reinstatable within three years**, because there was never a surrender value to draw. That
makes lapse on this chassis a non-terminal state, and the reinstatement assumption a [std]
behavioural input rather than an omission. On reinstatement the 보장개시일 resets, restarting
the two-year suicide clock and both contestability clocks [S1] [REG-R25].

### Expiry, prescription and policyholder protection

A 종신 contract has no expiry: it terminates on death, on 해지, on a 위법계약 cancellation, or
on the exhaustion of the sum assured through 감액. There is no 만기보험금 and no survival
benefit at any age [S1] [S2] [S4] [S8]. The projection therefore runs to the terminal age of
the mortality table, and `technical-notes.md` states which age that is and why.

**소멸시효**: 보험금청구권 and 보험료 또는 적립금의 반환청구권 prescribe in **three years**,
보험료청구권 in two [REG-R49 제662조](#krlib-reg-r49) [REG-R25 제37조](#krlib-reg-r25). **예금자보호**: since **2025-09-01**
the limit is **₩100,000,000** per person per insurer, applied separately to four claim buckets,
with proceeds payable because a policy term has ended expressly outside the insurance-claim
bucket [REG-R52] [REG-R32]. Every carrier document in the retrieved set still prints the
superseded ₩50,000,000 [S1] [S2] — a reminder that a brochure is evidence of the product, not
of the law in force when it is read.

### 계약자배당 — why there is none

On the 무배당 composite there is no dividend layer at all, and both 상품요약서 in the set state
the trade in the same words: 「무배당 상품은 배당상품보다 상대적으로 저렴한 보험료로 가입하실
수 있습니다」 [S2] [S8]. The legal frame survives regardless, and is cited rather than
implemented. 감독규정 제6-13조제1항 splits a life insurer's residual surplus into
유배당보험손익, 무배당보험손익 and 자본계정운용손익, gives the second and third wholly to
shareholders and caps the shareholder share of **유배당보험이익 at 100분의 10**; 제3항
ring-fences the policyholder share; 제4항 makes any shareholder dividend conditional on a
**지급여력비율 of 100% or more** at the year end [REG-R12]. Interest on a declared but unpaid
dividend must be at least the prior year's 평균공시이율 [REG-R12] [REG-R48].

One vocabulary caution belongs here because Korean actuarial writing uses it constantly. The
three-source framing — **위험률차 / 이자율차 / 사업비차**, the direct analogue of Japan's
三利源 — was regulatory language until recently: the 2023 text of 제6-11조의7 named
위험률차배당준비금, 이자율차배당준비금 and 사업비차배당준비금 separately, and the 2026 text has
collapsed them into a 총괄배당준비금 [REG-R12]. `krlib` uses the vocabulary and **does not
attribute it to the current regulation.**

---

## Riders and options

**In scope (modelled or parameterized):**

- **무해지환급형 / 저해지환급형** — a **model point column** carrying the suppression factor
  `k` and the suppressed period, not a separate model, so the cliff and the ordinary curve
  appear side by side in one projection. Shipped values 1.00 / 0.50 / 0.30 / 0.00 [S1] [S4]
  [S6] [S7] [S8] [REG-R19].
- **보험계약대출** — modelled as a state: an available balance capped at 80% of the payable
  해약환급금, a compound accrual at 예정이율 + 1.5%, settlement against every exit, and **zero
  availability on a 무해지 contract during 납입기간**. Take-up and repayment are [std]
  behavioural inputs [S5] [S9] [S11] [S12] [S13] [R4].
- **보험료 납입면제** — modelled as a distinct in-force state entered on a 50% 장해지급률, with
  premiums ceasing and **deemed paid** for benefit and surrender-value purposes. The disease
  riders that extend the trigger are parameterized as an incidence loading, off in the base run
  [S2] [S3] [S6] [S8] [REG-R25].
- **감액** — modelled as a partial surrender at the payable 해약환급금, with the sum assured
  and the cumulative-premium record restated pro rata [S5 제20조].
- **부활** — parameterized as a re-entry proportion applied to lapses within three years, off
  in the base run, with the 무해지 case explicitly reinstatable [S5 제26조] [REG-R25 제27조](#krlib-reg-r25).
- **금리연동형 crediting** — parameterized: the accrual rate becomes a declared 공시이율
  floored at a 최저보증이율 (observed **연복리 0.75%** [S5]), off in the base run, which is
  금리확정형 at 2.50% [REG-R16] [REG-R18] [REG-R23] [REG-R24].
- **유지보너스** — parameterized at the published 10.8% / 13.8% / 15.0% rates with the
  mandatory ≥ 30% additional lapse at the bonus date, off in the base run [S7] [REG-R27].
- **연금전환특약** — specified and priced at zero, as it is in the market; not modelled as a
  cash flow, because the annuity basis is the rider's at conversion and belongs to
  `Immediate_KR_S` and `Pension_KR_S` [S2] [S3] [S6].

**Out of scope, and named so that a reader meeting them knows they are real:** 건강등급 할인, a
premium re-rated annually on a health measure, up to 8% on the 주계약 [S6]; 선납 [S2] [S3] [S5]
[S6]; 고액계약할인 beyond the single 1.5% threshold adopted [S1] [S4]; 중도인출 and 추가납입,
which belong to the 유니버셜 chassis [S1] [S5]; the payment holiday available once 24 premiums
have been paid on that chassis [S5 제24조]; 생활설계자금, an automatic-감액 income drawdown
[S6]; 사망보험금 연금선지급 [S7]; the 체증형, 체감형, 전환나이-step, premiums-multiple and
보험기간 이원화 benefit shapes [S1] [S2] [S3] [S4] [S6] [S7] [S8]; 우량체 할인 [R8];
substandard 할증 and 부담보; 청약철회, 품질보증해지 and the 위법계약해지권 [S1] [REG-R25]
[REG-R51]; and the attachable protection and 제3보험 riders — 정기특약, 재해사망특약, 진단특약
and the medical riders — whose shape belongs to [term life
(정기보험)](../term_life/product-spec.md), [CI (CI보험)](../ci_insurance/product-spec.md),
[cancer (암보험)](../cancer/product-spec.md) and [indemnity medical
(실손의료보험)](../indemnity_medical/product-spec.md).

**Not offered, on the evidence retrieved:** 자동대출납입 (automatic premium loan) [unverified];
감액완납 (reduced paid-up) [unverified]; 연장정기보험 (extended term) [unverified]. Each is a
feature a reader arriving from `jplib` or `uslib` would assume, and none of the three is
evidenced by any Korean document read in this research pass [S5].

**Scope boundaries at the edge of this chassis.** Three neighbouring shapes are excluded and
named. **유니버셜 종신보험** is a distinct chassis rather than an option — free premium payment
within a 납입한도, a monthly 월대체보험료 deduction from the 계약자적립금, 중도인출 up to 12
times a 보험년도 with a 50% single-withdrawal cap and a residual-account floor, and payment
holidays once 24 premiums are paid [S5]. **변액종신보험** puts the account in a 특별계정 under
보험업법 제108조 [REG-R6] and is barred from the suppressed forms outright by 감독규정
제7-66조제4항제1호 [REG-R19]; its guarantees and their 보증비용 belong to [variable annuity
(변액연금보험)](../variable_annuity/product-spec.md). **단기납 종신보험** — 5년납 or 7년납 with
a 유지보너스 — is the same contract on a compressed payment period and is modelled here only
through the payment-term menu and the parameterized bonus, because its distinctive risk is the
lapse spike at the bonus date rather than a different benefit [S7] [REG-R27].

---

## Variations across insurers

1. **The suppression design — five arithmetically different mechanics under one name.** This is
   the largest source of divergence in the file and the one a model most easily gets wrong.
   **Design A, a fixed percentage of the 표준형 해약환급금**: 30% at one carrier [S4], 50% at
   three [S1] [S6] [S7]. **Design B, a formula on premiums paid ramping to 100%**: 「① 1년 이내
   : 0% ② 1년 초과 7년 이내 : 10% + [90% × 보험료 납입횟수 / 84회] ③ 7년 초과 : 100%」, with
   the ramp continuing on the 1–7년 basis if 84 payments have not been made [S2]. **Design C, a
   straight line on premiums paid to 납입기간 + 3년**: 「해약환급금 = 납입보험료 누계금액 ×
   경과개월수 / (「납입기간 + 3년」 × 12)」, nil in year one, capped at 100% at 납입기간 + 3년,
   with two independent gates — one year elapsed **and** twelve premiums paid [S3]. **Design D,
   nil throughout then a floor of premiums paid**: 「보험료 납입기간 중 — 없음; 납입기간 경과
   후 — 이미 납입한 보험료 × max(기준상품 해약환급률, 100%)」 [S8]. **Design E, a suppression
   plus a persistency bonus** [S7]. Composite: **Design A at 50%**, for the reasons in footnote
   2.
2. **Where the cliff falls.** At 납입완료 on Designs A, D and E [S1] [S4] [S6] [S7] [S8]; at
   **seven years** — long before the twenty-year payment period ends — on Design B [S2]; at
   **납입기간 + 3년** on Design C [S3]. Composite: 납입완료. This is the parameter a model must
   expose rather than hard-code, because it is not the same date at every carrier and on two of
   the five designs it is not 납입완료 at all.
3. **Whether the post-cliff value is capped.** Designs A and E track the 표준형 for ever, so
   the 환급률 keeps climbing — 151.9% at duration 30 [S1], 173.7% and 210.5% at durations 40
   and 60 [S4], 206.7% at duration 50 on the bonus design [S7]. Design B is **flat at exactly
   100.00% from duration 7 to duration 40** while its comparison product runs on to 150.07%: a
   cliff *and* a permanent ceiling, under which the policyholder never participates in the
   account above premiums paid [S2]. Design C is likewise capped at 100% of premiums [S3].
   Composite: uncapped, tracking the 표준형.
4. **The price of the suppression.** 81.5% and 86.8% at a 30% factor [S4]; 89.9% at a 50%
   factor [S1]; 94.0%–95.4% at a 50% factor on three 종 [S6]; 92.9%–94.3% on the formula design
   [S2]. Range **81.5%–95.4%**, deepest discount at deepest suppression. Composite: **90.0%**
   at a 50% factor.
5. **The death-benefit shape.** 평준형 at one [S6, 1종]; 체증형 at two, one adding +5% of
   가입금액 a year for 30 years and the other +5% a year from duration 10 to a flat 150% from
   duration 20 [S1] [S6, 3종]; 체감형 stepping down 5% a year from age 60 to a flat 50% [S6,
   2종]; a 전환나이 step at 55/60/65/70, up on one 종 and down on another [S4]; **max(보험가입
   금액, cumulative premiums × a published ratio)** at three [S2] [S3] [S8]; and a **보험기간
   이원화** paying 30%–90% of 가입금액 on disease death for the first five years and 100%
   thereafter [S7]. Composite: **평준형**.
6. **The policy loan limit.** 「해약환급금의 50% ~ 85%까지」, varying by product [S11]; 「해약
   환급금의 50 ~ 80%이내」 [S13]; the whole 해약환급금 net of existing loan, subject to a
   product-type restriction, in the one full 약관 [S5]. Composite: **80%**. The **rate
   formula**, by contrast, does not vary: 예정이율 (or 적용이율) + 1.5% on 금리확정형 and
   공시이율 + 1.5% on 금리연동형, at three carriers [S9] [S11] [S13], with +1.40%~1.50% at one
   [S11]. This is Korea's sharpest contrast with Japan's uniform 9/10-and-8/10 split: the
   *rate* is standard and the *limit* is not.
7. **The pricing interest rate, and whether it has a term structure.** 2.3% [S1]; 2.3% on a
   예정적립금 [S5]; 2.25% [S2]; **2.25% for ten years then 1.75%** [S7]; 2.75% [S8]; 2.50% on
   an 추가납입특약 [S6]. Composite: **2.50% flat**. The split rate at one carrier is a genuine
   term structure inside a pricing basis and a model wanting to reproduce that carrier's grid
   would need it.
8. **What is disclosed at all.** Two carriers publish the 적용이율, sample 적용위험률 at ages
   20 / 40 / 60 by sex, the 적용해지율 envelope and the 보험가격지수 in the 상품요약서 [S2]
   [S8]; the other six publish none of it. The two disclosed mortality grids differ by
   **up to 24%** — 18%–24% at five of the six published cells (남 40세 0.000780 against
   0.00092, 여 60세 0.001730 against 0.00214) and not at all at 여 20세, where both print
   0.00018 — so they **bracket** rather than fix a Korean insured mortality level, and
   one of them is labelled 「무배당 **예정 경험**사망률」, which is the giveaway that it is a
   경험생명표 derivative with a 무배당 loading rather than the table itself [S2] [S8].
9. **The issue-age envelope, and who the product is for.** 만15세~65세 [S4] and 만15세~70세
   [S6] are mainstream; 만15~52세 to 만15~63세 by payment term and sex is tighter [S1]; and one
   product is an explicitly **senior** design with a *minimum* issue age of 51–54 and a maximum
   of 72–78 [S3]. Issue ages run **3–8 years higher for women** at the same payment term
   everywhere they are stated [S1] [S2] [S8]. Composite: 15–65.
10. **The suicide exclusion.** Two years at four carriers [S1] [S3] [S6] [S7], not stated in
    the retrieved extract at the others. No three-year period appears anywhere in the Korean
    set, against a uniform three years across the Japanese one. Composite: **2년**.
11. **Premium discounts.** A **1.5% 고액계약할인** at ≥ 3,000만원 [S1]; an embedded
    고액계약할인 plus a 장기납입계약할인 at another [S4]; an annually recomputed **건강등급
    할인** of up to 8% on the 주계약 and 10% on riders, with all four grades published [S6];
    선납 discounted at the 적용이율 at two [S2] [S5] and at the **평균공시이율** at two more
    [S3] [S6]. Composite: the 1.5% volume discount only.
12. **What does not vary.** Uniform wherever the retrieved documents state it: a **종신** term
    with no 만기보험금 and no survival benefit [S1] [S2] [S3] [S4] [S6] [S8]; **무배당** at
    every one of the eight products in the set [S2] [S8] [R8]; the absence of any
    severe-disability acceleration and its replacement by a **50% 장해지급률 premium waiver**
    with premiums **deemed paid** [S2] [S3] [S6] [S8]; the identity **해약환급금 = 적립금 −
    해약공제액** [S2] [S8]; the fact that the comparison twin is priced **without a lapse
    assumption** and is **not sold** [S1] [S2] [S3] [S4]; the **equality of the suppressed and
    표준형 values from 납입완료** [S1] [S4] [S6]; the clawback for unpaid premiums [S2] [S3]
    [S8]; **보험나이** on the six-month rule incrementing on the 계약해당일 [S5] [REG-R25]; the
    **14-day** 납입최고기간 and the **3-year** 부활 window [S5] [REG-R25]; 감액 treated as
    partial surrender [S5] [REG-R25]; and the policy loan rate formula [S9] [S11] [S13]. Those
    are the invariant core of the composite, and every one is a fact a model can rely on
    without a [std] tag.
13. **What no carrier in the set offers.** 자동대출납입, 감액완납 and 연장정기보험 appear in no
    retrieved Korean document [S5]. Their absence is stated as a finding rather than an
    omission, and each is **[unverified]** rather than established, because the 생명보험
    표준약관 text was not retrieved.

---

## Regulatory context

**The ladder, and where the numbers live.** A Korean actuary works down five rungs — 법률 →
시행령 → 시행규칙 → **보험업감독규정** (an FSC 고시) → **보험업감독업무시행세칙** (an FSS 세칙)
→ 별표 — and **nearly every operative number for this product sits on the last two** [REG-R1]
[REG-R9] [REG-R23]. 보험업법 governs the undertaking; **상법 제4편 보험** governs the contract,
is one-way mandatory under 제663조, and is sponsored by a different ministry [REG-R49]. This
document cites the chain and implements none of it.

**What a Korean product filing is, and why every pricing parameter here is [std].** 보험업법
제5조제3호 names the **기초서류**: 「사업방법서, 보험약관, 보험료 및 해약환급금의 산출방법서」
[REG-R2]. The 산출방법서 is where the 예정이율, the 적용위험률, the 예정사업비율 and the
surrender-value formula actually live, and it is **not published** — only the 약관, the
상품요약서 and the 공시 disclosures are. 제127조제2항 makes prior notification to the FSC the
exception rather than the rule, and 제128조 lets the FSC require verification of the 산출방법서
by the FSS, the 보험요율 산출기관 or an 독립계리업자 [REG-R2]. 감독규정 제7-64조 then lists the
five 필수기재사항 of the 산출방법서, of which the third is the **해약환급금 calculation
including the 해약공제액 and, where the 계약체결비용 exceeds the 표준해약공제액 at the 기준연령
요건, a comparison of the two** [REG-R18]. **No amount of further research converts an expense
or pricing parameter in this document into a sourced value**; what research *can* do, and did,
is bound them by published caps and by published cash values.

**Reserving — cited, not computed.** 보험업법 제120조 obliges an insurer to hold 책임준비금 and
비상위험준비금 and delegates the mechanics entirely [REG-R3]. 감독규정 제6-11조 splits
책임준비금 into 보험계약부채, 재보험계약부채 and 투자계약부채 with a 잔여보장요소 /
발생사고요소 split inside the first two, and **delegates the calculation to the FSS Governor**
— ten paragraphs of the pre-2023 article, which carried accumulation rules, were deleted on
2022-12-21, which is the visible trace of the switch from a locked-in statutory reserve to a
current-estimate one [REG-R10]. On top sits the **해약환급금준비금** [REG-R11], described in
the cliff section above. `WholeLife_KR_S` computes **none** of these. What it does compute —
the **계약자적립액** and the **해약환급금** — it computes because both are contractual
quantities with a **published bound**, 별표 14 [REG-R20], and because the surrender-value
reserve cannot be discussed at all without them.

**Three measurement bases, all live, over one set of cash flows.** This is where Korea differs
most from every other library in this repository, and a document that conflates them will be
wrong about which assumptions are fixed and which are re-set. **IFRS 17** — K-IFRS 제1117호,
**mandatory** since 2023-01-01, not voluntary as in Japan [REG-R60] — measures the liability as
fulfilment cash flows plus a risk adjustment plus the CSM, discounted on a 국고채-based curve
with 관찰금리 to a **20-year** last observable maturity extending to 30 years over three years
from 2025, an LTFR of **4.55%** and a liquidity premium of **91bp**, and **everything is re-set
at every reporting date** [REG-R27] [REG-R60]. **K-ICS** — the 신지급여력제도, live in the same
quarter — re-measures the same balance sheet at economic value and sets a 지급여력기준금액 from
five risk modules, of which the life module alone carries seven shock-based sub-risks including
**해지위험액** and **사업비위험액**; the floor is **100%** and the 적기시정조치 ladder starts
below it [REG-R13] [REG-R8] [REG-R14]. 요구자본 rose from **₩67.9조 under RBC at 2022-12-31 to
₩118.9조 under K-ICS at 2024-09-30**, and the industry ratio after 경과조치 at 2025-09-30 was
**210.8%** overall and **201.4%** for life insurers [REG-R30]. **The 해약환급금준비금** is the
third and is Korea's own [REG-R11]. `krlib` keeps the cash flows basis-agnostic, publishes
`result_cf()` as a gross best-estimate stream, and stops deliberately before all three.

**Why this product in particular is the reason the guidance exists.** The November 2024
계리가정 decision is directed at exactly this contract: the lapse assumption on a 무·저해지
form, the 0.1% convergence at 납입완료, the 0.8% ultimate rate, the 30% additional lapse at a
단기납 bonus date, and the disclosure regime around any departure from the 원칙모형 [REG-R27]
[R3]. Its own framing of the problem — 「무·저해지 상품은 납입기간 중 해지 시 환급금이 없거나
적은 상품임에도 완납 직전까지 해지가 발생한다고 가정하여 낮은 보험료로 인해 상품의 쏠림현상이
심화됨」 — is a description of this product's economics, and the 63.8% first-year-premium share
it quotes is the measure of how far the distortion went [REG-R27] [R7]. **A whole-life
liability model that does not expose the lapse vector as a parameter cannot be used in Korea at
all.**

**Mortality basis, and the position it forces.** The industry table is the **제10회
경험생명표** (*gyeongheom saengmyeongpyo*, experience life table), produced by 보험개발원 and
applied to new business from **April 2024**. It is **not published in full**: only summary
statistics are released — 평균수명 남 **86.3세** / 여 **90.7세**, 65세 기대여명 남 **23.7년** /
여 **27.1년** — and even those were retrieved only through a trade newspaper, because the KIDI
보도자료 index carries no 경험생명표 item and its 빅데이터 플랫폼 refused connection [REG-R33]
[REG-R34] [R12]. The 참조순보험요율 the bureau files with the FSC are likewise never published,
becoming visible to the public only as the **보험가격지수** ratio [REG-R4] [REG-R22]. **Every
`mort_table.csv` in `krlib` is therefore a [std] construction**, anchored on the public
국가데이터처 완전생명표 — 2024 기대수명 at birth 남 **80.8년** / 여 **86.6년**, 65세 기대여명
남 **19.5년** / 여 **23.7년** [REG-R38] — scaled toward insured level by the roughly **4.2-year
(male) and 3.4-year (female)** gap at age 65 that the two sets of figures imply, and
sanity-checked against the two carriers' published 적용위험률 grids [S2] [S8]. Every row
carries a `provenance` column and **the library's tables must never be presented as the
경험생명표**. One further conversion is required and stated wherever it bites: the public
statistics are on **만나이** while this product rates on **보험나이** [REG-R25] [REG-R38].

**Conduct and disclosure.** 감독규정 제7-45조제7항 requires a 보장성보험 to publish a
**보험가격지수** and a 보장범위지수 in its 상품요약서 [REG-R22], which is how a Korean consumer
sees the price of a product whose pricing basis is confidential. The 무(저)해지 form was itself
the subject of an FSS **소비자경보** in 2019, warning that it is a 보장성보험 unsuitable as
savings and that it **cannot support a policy loan during the payment period** [R4] [REG-R28].
청약철회 is 15 days from the 보험증권 and 30 from the application, with no penalty [REG-R51].
On insurer failure, 예금자보호 covers **₩100,000,000** per person per insurer, applied bucket
by bucket [REG-R52] [REG-R32].

**Tax.** Three regimes drive this product's design. **Inheritance**: a death benefit received
on the death of the policyholder is deemed estate property under 상속세 및 증여세법 제8조제1항,
and 제8조제2항 extends that to a policy nominally held by another where the deceased in
substance paid the premiums; where beneficiary and premium payer differ, 제34조 treats the
benefit attributable to the other person's premiums as a gift [REG-R59]. **Premium relief**: a
**12% tax credit** on premiums up to **₩1,000,000** a year for a contract whose maturity value
does not exceed premiums paid — a credit rather than a deduction, and the same economic test
the supervisor uses to define a 보장성보험 [REG-R57] [REG-R9]. **The 연금전환 route**: 소득세법
시행령 제25조제9항 and 제10항, new on 2025-06-30, treat a reduction of a 보장성보험's sum
insured whose released amount is drawn as an annuity as **conversion to a 저축성보험**,
resetting the first-premium date for the ten-year 보험차익 exemption — **unless** the original
contract was 월적립식 with a sum insured of **₩900,000,000 (9억원) or less**, premiums were
fully paid before the first annuity date, policyholder, insured and beneficiary are the same
person, and the annuity starts at **55 or later**. That provision is the tax basis of the
연금전환특약 this product carries [REG-R58]. `krlib` models contractual cash flows, not the
policyholder's tax position.

**Professional and design constraints, collected.** The 선임계리사 appointed under 보험업법
제181조제2항 verifies the 기초서류 and, since the 2022 amendment, is barred from direct product
development, from the CEO role and from the CFO role — a harder separation of pricing from
sign-off than the UK Chief Actuary split [REG-R5]. 감독규정 제7-60조 sets the design rules this
product must satisfy: **제7호**, a 금리연동형 product must set a 최저사망보험금; **제8호**, a
contract must not be extinguished while the risk it covers remains effective; **제9호**, the
death benefit must be at least cumulative premiums paid except where the payment period ends at
age 80 or below; **제10호**, a 금리연동형 product **must** set a 최저보증이율 or a 최저보증금액
[REG-R16]. And 감독규정 제7-69조 and 제7-70조 apply the whole surrender-value regime — 제7-65조
through 제7-68조 — to 장기손해보험 and to 제3보험 *mutatis mutandis*, which is why the
machinery specified in this document governs every one of the ten `krlib` products and is
specified here once [REG-R19].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #krlib-whole_life-r1
[R12]: #krlib-whole_life-r12
[R13]: #krlib-whole_life-r13
[R2]: #krlib-whole_life-r2
[R3]: #krlib-whole_life-r3
[R4]: #krlib-whole_life-r4
[R6]: #krlib-whole_life-r6
[R7]: #krlib-whole_life-r7
[R8]: #krlib-whole_life-r8
[R9]: #krlib-whole_life-r9
[REG-R1]: #krlib-reg-r1
[REG-R10]: #krlib-reg-r10
[REG-R11]: #krlib-reg-r11
[REG-R12]: #krlib-reg-r12
[REG-R13]: #krlib-reg-r13
[REG-R14]: #krlib-reg-r14
[REG-R16]: #krlib-reg-r16
[REG-R17]: #krlib-reg-r17
[REG-R18]: #krlib-reg-r18
[REG-R19]: #krlib-reg-r19
[REG-R2]: #krlib-reg-r2
[REG-R20]: #krlib-reg-r20
[REG-R21]: #krlib-reg-r21
[REG-R22]: #krlib-reg-r22
[REG-R23]: #krlib-reg-r23
[REG-R24]: #krlib-reg-r24
[REG-R25]: #krlib-reg-r25
[REG-R26]: #krlib-reg-r26
[REG-R27]: #krlib-reg-r27
[REG-R28]: #krlib-reg-r28
[REG-R29]: #krlib-reg-r29
[REG-R3]: #krlib-reg-r3
[REG-R30]: #krlib-reg-r30
[REG-R32]: #krlib-reg-r32
[REG-R33]: #krlib-reg-r33
[REG-R34]: #krlib-reg-r34
[REG-R36]: #krlib-reg-r36
[REG-R37]: #krlib-reg-r37
[REG-R38]: #krlib-reg-r38
[REG-R4]: #krlib-reg-r4
[REG-R45]: #krlib-reg-r45
[REG-R48]: #krlib-reg-r48
[REG-R49]: #krlib-reg-r49
[REG-R5]: #krlib-reg-r5
[REG-R50]: #krlib-reg-r50
[REG-R51]: #krlib-reg-r51
[REG-R52]: #krlib-reg-r52
[REG-R57]: #krlib-reg-r57
[REG-R58]: #krlib-reg-r58
[REG-R59]: #krlib-reg-r59
[REG-R6]: #krlib-reg-r6
[REG-R60]: #krlib-reg-r60
[REG-R7]: #krlib-reg-r7
[REG-R8]: #krlib-reg-r8
[REG-R9]: #krlib-reg-r9
[std]: #krlib-std
[unverified]: #krlib-unverified
<!-- END generated citation links -->
